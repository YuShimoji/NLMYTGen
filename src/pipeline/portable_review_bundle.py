from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import zipfile
from html import escape
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


BUNDLE_SCHEMA = "nlmytgen.portable_review_bundle.v1"
RECIPIENT_OPEN_SCHEMA = "nlmytgen.review_bundle_recipient_open.v1"
DESCRIPTOR_SCHEMA = "nlmytgen.portable_review_bundle_descriptor.v1"
SCHEMA_VERSION = "1.0"
NORMALIZED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
MAX_ARCHIVE_FILES = 64
MAX_FILE_BYTES = 128 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024
MAX_COMPRESSION_RATIO = 200
CONTROL_FILES = (
    "portable_bundle_manifest.json",
    "recipient_open_receipt.template.json",
    "checksums.sha256",
)
EXECUTABLE_SUFFIXES = {
    ".bat",
    ".cmd",
    ".com",
    ".dll",
    ".exe",
    ".js",
    ".msi",
    ".ps1",
    ".scr",
    ".vbs",
}
ARCHIVE_SUFFIXES = {
    ".7z",
    ".bz2",
    ".gz",
    ".rar",
    ".tar",
    ".tgz",
    ".xz",
    ".zip",
}
MIME_TYPES = {
    ".html": "text/html",
    ".json": "application/json",
    ".md": "text/markdown",
    ".mp4": "video/mp4",
    ".png": "image/png",
    ".sha256": "text/plain",
}


class PortableReviewBundleError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        code: str,
        field_path: str,
        consumer_effect: str,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.field_path = field_path
        self.consumer_effect = consumer_effect

    def as_payload(self) -> dict[str, Any]:
        return {
            "schema": "nlmytgen.portable_review_bundle_result.v1",
            "schema_version": SCHEMA_VERSION,
            "status": "failed",
            "error_code": self.code,
            "field_path": self.field_path,
            "message": str(self),
            "consumer_effect": self.consumer_effect,
            "boundaries": {
                "source_packet_regeneration_count": 0,
                "source_packet_mutation_count": 0,
                "yymm4_launch_count": 0,
                "render_driver_launch_count": 0,
                "full_render_count": 0,
                "transcode_count": 0,
                "playback_count": 0,
                "system_volume_operation_count": 0,
                "network_request_count": 0,
                "external_transfer_count": 0,
            },
        }


def _fail(
    message: str,
    *,
    code: str,
    field_path: str,
    consumer_effect: str,
) -> None:
    raise PortableReviewBundleError(
        message,
        code=code,
        field_path=field_path,
        consumer_effect=consumer_effect,
    )


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _mapping(
    value: Any,
    *,
    field_path: str,
    required: set[str] | None = None,
    allowed: set[str] | None = None,
) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail(
            "expected an object",
            code="review_bundle_contract_invalid",
            field_path=field_path,
            consumer_effect="bundle creation remains undispatched",
        )
    if required is not None:
        missing = sorted(required - set(value))
        if missing:
            _fail(
                f"required fields are missing: {', '.join(missing)}",
                code="review_bundle_contract_invalid",
                field_path=field_path,
                consumer_effect="bundle creation remains undispatched",
            )
    if allowed is not None:
        extra = sorted(set(value) - allowed)
        if extra:
            _fail(
                f"unsupported fields are present: {', '.join(extra)}",
                code="review_bundle_contract_invalid",
                field_path=field_path,
                consumer_effect="bundle creation remains undispatched",
            )
    return value


def _exact(
    actual: Any,
    expected: Any,
    *,
    code: str,
    field_path: str,
    consumer_effect: str = "identity drift stops before bundle creation",
) -> None:
    if actual != expected:
        _fail(
            f"expected {expected!r}, observed {actual!r}",
            code=code,
            field_path=field_path,
            consumer_effect=consumer_effect,
        )


def _portable_path(
    value: Any,
    *,
    field_path: str,
    allow_archive: bool = False,
) -> str:
    if not isinstance(value, str) or not value:
        _fail(
            "portable path must be a non-empty string",
            code="review_bundle_path_unsafe",
            field_path=field_path,
            consumer_effect="unsafe path is rejected before extraction or write",
        )
    if "\\" in value or "\x00" in value or re.match(r"^[A-Za-z]:", value):
        _fail(
            "portable path contains an absolute or platform-specific prefix",
            code="review_bundle_path_unsafe",
            field_path=field_path,
            consumer_effect="unsafe path is rejected before extraction or write",
        )
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        _fail(
            "portable path is absolute, empty, or traverses",
            code="review_bundle_path_unsafe",
            field_path=field_path,
            consumer_effect="unsafe path is rejected before extraction or write",
        )
    normalized = pure.as_posix()
    if normalized != value or normalized.startswith("."):
        _fail(
            "portable path is not in canonical relative form",
            code="review_bundle_path_unsafe",
            field_path=field_path,
            consumer_effect="unsafe path is rejected before extraction or write",
        )
    suffix = pure.suffix.lower()
    if suffix in EXECUTABLE_SUFFIXES:
        _fail(
            "portable bundle cannot contain an executable",
            code="review_bundle_executable_forbidden",
            field_path=field_path,
            consumer_effect="hidden executable content is never transported",
        )
    if suffix in ARCHIVE_SUFFIXES and not allow_archive:
        _fail(
            "portable bundle cannot contain a nested archive",
            code="review_bundle_nested_archive_forbidden",
            field_path=field_path,
            consumer_effect="nested archive expansion is never delegated",
        )
    return normalized


def _repo_path(
    repo_root: Path,
    value: str | Path,
    *,
    field_path: str,
    require_exists: bool = True,
    allow_archive: bool = False,
) -> tuple[str, Path]:
    locator = _portable_path(
        Path(value).as_posix(),
        field_path=field_path,
        allow_archive=allow_archive,
    )
    root = repo_root.resolve()
    resolved = (root / Path(*PurePosixPath(locator).parts)).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        _fail(
            "repository locator escapes the workspace",
            code="review_bundle_path_unsafe",
            field_path=field_path,
            consumer_effect="unsafe path is rejected before read or write",
        )
    if require_exists and not resolved.exists():
        _fail(
            "required source bundle artifact is unavailable",
            code="source_bundle_unavailable",
            field_path=field_path,
            consumer_effect=(
                "absence remains explicit and does not trigger packet "
                "regeneration, render, network, or private copy"
            ),
        )
    return locator, resolved


def _load_json(path: Path, *, field_path: str) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PortableReviewBundleError(
            "JSON input is unavailable or invalid",
            code="review_bundle_json_invalid",
            field_path=field_path,
            consumer_effect="invalid evidence is rejected before bundle creation",
        ) from exc
    return _mapping(value, field_path=field_path)


def _scan_text(
    text: str,
    *,
    field_path: str,
    allow_relative_lineage: bool,
) -> None:
    patterns = (
        (r"(?i)(?:^|[^A-Za-z])[A-Za-z]:[\\/]", "drive letter"),
        (r"(?i)(?:^|[\\/])Users[\\/][^\\/]+", "user profile path"),
        (r"(?i)\b(?:password|credential|cookie)\b\s*[:=]", "secret field"),
        (r"(?i)\b(?:bearer|api[_-]?key)\b", "credential marker"),
        (r"(?i)file://", "file URL"),
    )
    for pattern, label in patterns:
        if re.search(pattern, text):
            _fail(
                f"portable text contains a forbidden {label}",
                code="review_bundle_private_path",
                field_path=field_path,
                consumer_effect="machine-specific or secret data is never bundled",
            )
    if not allow_relative_lineage and re.search(
        r"(?i)(?:auto_video_runs|local_outputs|generated_project\.local|"
        r"internal_review_.+\.mp4)",
        text,
    ):
        _fail(
            "portable control file contains a private source locator",
            code="review_bundle_private_path",
            field_path=field_path,
            consumer_effect="bundle control files expose identities without locators",
        )


def _snapshot(paths: Mapping[str, Path]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
            "mtime_ns": path.stat().st_mtime_ns,
        }
        for name, path in sorted(paths.items())
    }


def _validate_descriptor(
    *,
    repo_root: Path,
    descriptor_path: str | Path,
) -> tuple[str, Mapping[str, Any]]:
    locator, path = _repo_path(
        repo_root,
        descriptor_path,
        field_path="$.descriptor",
    )
    descriptor = _load_json(path, field_path="$.descriptor")
    required = {
        "schema",
        "schema_version",
        "bundle_id",
        "bundle_version",
        "authority_id",
        "contract",
        "source_packet",
        "output",
        "recipient_test",
        "constraints",
    }
    _mapping(
        descriptor,
        field_path="$.descriptor",
        required=required,
        allowed=required,
    )
    _exact(
        descriptor["schema"],
        DESCRIPTOR_SCHEMA,
        code="review_bundle_contract_invalid",
        field_path="$.descriptor.schema",
    )
    _exact(
        descriptor["schema_version"],
        SCHEMA_VERSION,
        code="review_bundle_contract_invalid",
        field_path="$.descriptor.schema_version",
    )
    _exact(
        descriptor["bundle_version"],
        1,
        code="review_bundle_contract_invalid",
        field_path="$.descriptor.bundle_version",
    )
    contract = _mapping(
        descriptor["contract"],
        field_path="$.descriptor.contract",
        required={"bundle_schema", "recipient_open_schema"},
        allowed={"bundle_schema", "recipient_open_schema"},
    )
    for key, expected_id in (
        ("bundle_schema", BUNDLE_SCHEMA),
        ("recipient_open_schema", RECIPIENT_OPEN_SCHEMA),
    ):
        bound = _mapping(
            contract[key],
            field_path=f"$.descriptor.contract.{key}",
            required={"path", "sha256"},
            allowed={"path", "sha256"},
        )
        _, schema_path = _repo_path(
            repo_root,
            bound["path"],
            field_path=f"$.descriptor.contract.{key}.path",
        )
        _exact(
            sha256_file(schema_path),
            bound["sha256"],
            code="review_bundle_schema_hash_mismatch",
            field_path=f"$.descriptor.contract.{key}.sha256",
        )
        schema = _load_json(
            schema_path,
            field_path=f"$.descriptor.contract.{key}",
        )
        _exact(
            schema.get("$id"),
            expected_id,
            code="review_bundle_schema_identity_mismatch",
            field_path=f"$.descriptor.contract.{key}.path",
        )
    constraints = _mapping(
        descriptor["constraints"],
        field_path="$.descriptor.constraints",
    )
    expected_constraints = {
        "no_overwrite": True,
        "source_packet_regeneration": False,
        "source_packet_mutation": False,
        "network": False,
        "playback": False,
        "yymm4": False,
        "render": False,
        "external_transfer": False,
        "human_open": False,
        "content_decision": False,
        "rights": False,
        "production": False,
        "publication": False,
    }
    for key, expected in expected_constraints.items():
        _exact(
            constraints.get(key),
            expected,
            code="review_bundle_contract_invalid",
            field_path=f"$.descriptor.constraints.{key}",
        )
    return locator, descriptor


def _find_descriptor(repo_root: Path, packet_locator: str) -> str:
    root = repo_root.resolve() / "production_pilots"
    matches: list[str] = []
    if root.exists():
        for path in root.rglob("*portable_review_bundle_descriptor.json"):
            if not path.is_file():
                continue
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                continue
            source = value.get("source_packet") if isinstance(value, dict) else None
            if isinstance(source, dict) and source.get("path") == packet_locator:
                matches.append(path.relative_to(repo_root.resolve()).as_posix())
    if len(matches) != 1:
        _fail(
            "exact portable review bundle descriptor is unavailable or ambiguous",
            code="review_bundle_descriptor_not_unique",
            field_path="$.descriptor",
            consumer_effect="bundle creation remains bound to one exact descriptor",
        )
    return matches[0]


def inspect_source_packet(
    *,
    repo_root: Path,
    packet_path: str | Path,
    descriptor_path: str | Path | None = None,
) -> dict[str, Any]:
    packet_locator, packet_root = _repo_path(
        repo_root,
        packet_path,
        field_path="$.packet",
    )
    if not packet_root.is_dir():
        _fail(
            "source packet locator is not a directory",
            code="source_bundle_unavailable",
            field_path="$.packet",
            consumer_effect="absence does not trigger packet regeneration",
        )
    if descriptor_path is None:
        descriptor_path = _find_descriptor(repo_root, packet_locator)
    descriptor_locator, descriptor = _validate_descriptor(
        repo_root=repo_root,
        descriptor_path=descriptor_path,
    )
    source_contract = _mapping(
        descriptor["source_packet"],
        field_path="$.descriptor.source_packet",
        required={
            "path",
            "tracked_receipt_path",
            "tracked_receipt_sha256",
            "packet_id",
            "manifest_sha256",
        },
        allowed={
            "path",
            "tracked_receipt_path",
            "tracked_receipt_sha256",
            "packet_id",
            "manifest_sha256",
        },
    )
    _exact(
        source_contract["path"],
        packet_locator,
        code="source_packet_identity_mismatch",
        field_path="$.descriptor.source_packet.path",
    )
    receipt_locator, receipt_path = _repo_path(
        repo_root,
        source_contract["tracked_receipt_path"],
        field_path="$.descriptor.source_packet.tracked_receipt_path",
    )
    _exact(
        sha256_file(receipt_path),
        source_contract["tracked_receipt_sha256"],
        code="source_packet_receipt_hash_mismatch",
        field_path="$.descriptor.source_packet.tracked_receipt_sha256",
    )
    receipt = _load_json(receipt_path, field_path="$.tracked_receipt")
    manifest_path = packet_root / "packet_manifest.json"
    if not manifest_path.is_file():
        _fail(
            "source packet manifest is unavailable",
            code="source_bundle_unavailable",
            field_path="$.packet.packet_manifest",
            consumer_effect="absence does not trigger packet regeneration",
        )
    manifest_hash = sha256_file(manifest_path)
    _exact(
        manifest_hash,
        source_contract["manifest_sha256"],
        code="source_packet_hash_mismatch",
        field_path="$.descriptor.source_packet.manifest_sha256",
    )
    manifest = _load_json(manifest_path, field_path="$.packet_manifest")
    _exact(
        manifest.get("schema"),
        "nlmytgen.cue_review_packet.v1",
        code="source_packet_manifest_contradiction",
        field_path="$.packet_manifest.schema",
    )
    _exact(
        manifest.get("packet_id"),
        source_contract["packet_id"],
        code="source_packet_manifest_contradiction",
        field_path="$.packet_manifest.packet_id",
    )
    _exact(
        receipt.get("packet", {}).get("path"),
        packet_locator,
        code="source_packet_manifest_contradiction",
        field_path="$.tracked_receipt.packet.path",
    )
    _exact(
        receipt.get("packet", {}).get("manifest_sha256"),
        manifest_hash,
        code="source_packet_manifest_contradiction",
        field_path="$.tracked_receipt.packet.manifest_sha256",
    )

    cue = _mapping(manifest.get("cue"), field_path="$.packet_manifest.cue")
    cue_id = cue.get("cue_id")
    expected_names = {
        f"{cue_id}_review_excerpt.mp4",
        f"{cue_id}_render_frame.png",
        f"{cue_id}_materialized_source_view.png",
        "README_REVIEW.md",
        "packet_manifest.json",
    }
    actual_names = {path.name for path in packet_root.iterdir() if path.is_file()}
    _exact(
        actual_names,
        expected_names,
        code="source_packet_file_set_mismatch",
        field_path="$.packet",
    )
    packet_files = {name: packet_root / name for name in sorted(expected_names)}
    receipt_files: dict[str, Mapping[str, Any]] = {}
    for item in receipt.get("packet", {}).get("outputs", []):
        if isinstance(item, Mapping) and isinstance(item.get("name"), str):
            receipt_files[item["name"]] = item
    receipt_files["packet_manifest.json"] = {
        "sha256": receipt.get("packet", {}).get("manifest_sha256"),
        "size_bytes": manifest_path.stat().st_size,
    }
    manifest_files = {
        PurePosixPath(item["path"]).name: item
        for item in manifest.get("outputs", [])
        if isinstance(item, Mapping) and isinstance(item.get("path"), str)
    }
    file_identities: list[dict[str, Any]] = []
    for name, path in sorted(packet_files.items()):
        if path.is_symlink():
            _fail(
                "source packet contains a symlink",
                code="source_packet_symlink_forbidden",
                field_path=f"$.packet.{name}",
                consumer_effect="linked source data is never bundled",
            )
        identity = {
            "name": name,
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
            "mtime_ns": path.stat().st_mtime_ns,
        }
        expected = receipt_files.get(name)
        if expected is None:
            _fail(
                "tracked receipt omits a source packet file",
                code="source_packet_manifest_contradiction",
                field_path=f"$.tracked_receipt.packet.outputs.{name}",
                consumer_effect="incomplete source identity stops packaging",
            )
        _exact(
            identity["sha256"],
            expected.get("sha256"),
            code="source_packet_hash_mismatch",
            field_path=f"$.packet.{name}.sha256",
        )
        _exact(
            identity["size_bytes"],
            expected.get("size_bytes"),
            code="source_packet_size_mismatch",
            field_path=f"$.packet.{name}.size_bytes",
        )
        if name not in {"packet_manifest.json", "README_REVIEW.md"}:
            manifest_item = manifest_files.get(name)
            if manifest_item is None:
                _fail(
                    "source manifest omits a packet output",
                    code="source_packet_manifest_contradiction",
                    field_path=f"$.packet_manifest.outputs.{name}",
                    consumer_effect="manifest contradiction stops packaging",
                )
            _exact(
                identity["sha256"],
                manifest_item.get("sha256"),
                code="source_packet_manifest_contradiction",
                field_path=f"$.packet_manifest.outputs.{name}.sha256",
            )
            _exact(
                identity["size_bytes"],
                manifest_item.get("size_bytes"),
                code="source_packet_manifest_contradiction",
                field_path=f"$.packet_manifest.outputs.{name}.size_bytes",
            )
        file_identities.append(identity)

    source_receipt = _mapping(
        receipt.get("source_identities"),
        field_path="$.tracked_receipt.source_identities",
    )
    materialized = _mapping(
        source_receipt.get("materialized_source"),
        field_path="$.tracked_receipt.source_identities.materialized_source",
    )
    source_binding = _mapping(
        manifest.get("source_binding"),
        field_path="$.packet_manifest.source_binding",
    )
    manifest_materialized = _mapping(
        source_binding.get("materialized_source"),
        field_path="$.packet_manifest.source_binding.materialized_source",
    )
    comparisons = (
        (
            manifest.get("package_id"),
            receipt.get("cue", {}).get("package_id", manifest.get("package_id")),
            "package_id",
        ),
        (
            manifest.get("descriptor", {}).get("sha256"),
            source_receipt.get("descriptor", {}).get("sha256"),
            "descriptor.sha256",
        ),
        (
            manifest.get("content_identity_sha256"),
            source_receipt.get("content_identity_sha256"),
            "content_identity_sha256",
        ),
        (
            manifest.get("source_project", {}).get("sha256"),
            source_receipt.get("source_project_identity_sha256"),
            "source_project.sha256",
        ),
        (
            manifest.get("generated_project", {}).get("sha256"),
            source_receipt.get("generated_project", {}).get("sha256"),
            "generated_project.sha256",
        ),
        (
            manifest.get("source_mp4", {}).get("sha256"),
            source_receipt.get("source_mp4", {}).get("sha256"),
            "source_mp4.sha256",
        ),
        (
            manifest_materialized.get("source_id"),
            materialized.get("source_id"),
            "source_binding.materialized_source.source_id",
        ),
        (
            manifest_materialized.get("source_sha256"),
            materialized.get("source_sha256"),
            "source_binding.materialized_source.source_sha256",
        ),
        (
            manifest_materialized.get("sha256"),
            materialized.get("sha256"),
            "source_binding.materialized_source.sha256",
        ),
        (
            manifest_materialized.get("crop"),
            materialized.get("crop"),
            "source_binding.materialized_source.crop",
        ),
        (
            manifest_materialized.get("fit_mode"),
            materialized.get("fit_mode"),
            "source_binding.materialized_source.fit_mode",
        ),
    )
    for actual, expected, field in comparisons:
        _exact(
            actual,
            expected,
            code="source_packet_manifest_contradiction",
            field_path=f"$.packet_manifest.{field}",
            consumer_effect="source identity contradiction stops packaging",
        )
    receipt_cue = _mapping(receipt.get("cue"), field_path="$.tracked_receipt.cue")
    cue_comparisons = (
        ("cue_id", "cue_id"),
        ("scene_id", "scene_id"),
        ("canonical_text_sha256", "canonical_text_sha256"),
        ("start_frame", "start_frame_inclusive"),
        ("end_frame", "end_frame_exclusive"),
        ("length_frames", "length_frames"),
        ("fps", "fps"),
        ("start_seconds", "start_seconds"),
        ("end_seconds", "end_seconds"),
        ("context_handle_frames", "context_handle_frames"),
    )
    for manifest_key, receipt_key in cue_comparisons:
        _exact(
            cue.get(manifest_key),
            receipt_cue.get(receipt_key),
            code="source_packet_manifest_contradiction",
            field_path=f"$.packet_manifest.cue.{manifest_key}",
        )

    _scan_text(
        manifest_path.read_text(encoding="utf-8"),
        field_path="$.packet.packet_manifest",
        allow_relative_lineage=True,
    )
    _scan_text(
        (packet_root / "README_REVIEW.md").read_text(encoding="utf-8"),
        field_path="$.packet.README_REVIEW",
        allow_relative_lineage=True,
    )
    return {
        "status": "passed",
        "descriptor_locator": descriptor_locator,
        "descriptor": copy.deepcopy(descriptor),
        "packet_locator": packet_locator,
        "packet_root": packet_root,
        "packet_id": manifest["packet_id"],
        "packet_schema": manifest["schema"],
        "packet_manifest_sha256": manifest_hash,
        "tracked_receipt_locator": receipt_locator,
        "tracked_receipt_sha256": sha256_file(receipt_path),
        "package_id": manifest["package_id"],
        "cue": copy.deepcopy(cue),
        "source_identities": {
            "descriptor_sha256": source_receipt["descriptor"]["sha256"],
            "content_identity_sha256": source_receipt[
                "content_identity_sha256"
            ],
            "source_project_sha256": source_receipt[
                "source_project_identity_sha256"
            ],
            "generated_project_sha256": source_receipt["generated_project"][
                "sha256"
            ],
            "source_mp4_sha256": source_receipt["source_mp4"]["sha256"],
            "source_id": materialized["source_id"],
            "source_sha256": materialized["source_sha256"],
            "materialized_source_sha256": materialized["sha256"],
            "crop": copy.deepcopy(materialized["crop"]),
            "fit_mode": materialized["fit_mode"],
        },
        "file_identities": file_identities,
        "packet_files": packet_files,
        "source_snapshot": _snapshot(packet_files),
        "decode": copy.deepcopy(manifest.get("decode")),
    }


def _mime_type(path: str) -> str:
    suffix = PurePosixPath(path).suffix.lower()
    return MIME_TYPES.get(suffix, "application/octet-stream")


def _file_identity(path: str, data: bytes, role: str) -> dict[str, Any]:
    return {
        "role": role,
        "path": path,
        "mime_type": _mime_type(path),
        "sha256": sha256_bytes(data),
        "size_bytes": len(data),
    }


def _offline_html(binding: Mapping[str, Any]) -> bytes:
    cue = binding["cue"]
    cue_id = str(cue["cue_id"])
    package_id = str(binding["package_id"])
    excerpt = f"packet/{cue_id}_review_excerpt.mp4"
    render_frame = f"packet/{cue_id}_render_frame.png"
    source_view = f"packet/{cue_id}_materialized_source_view.png"
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Review bundle: {escape(cue_id)}</title>
  <style>
    body {{ margin: 0 auto; max-width: 960px; padding: 24px; color: #1f2933;
      background: #ffffff; font: 16px/1.55 system-ui, sans-serif; }}
    h1 {{ font-size: 1.6rem; margin: 0 0 0.5rem; }}
    h2 {{ font-size: 1.2rem; margin-top: 2rem; }}
    img, video {{ display: block; max-width: 100%; height: auto; margin: 0.75rem 0; }}
    video {{ width: 100%; background: #111111; }}
    code {{ overflow-wrap: anywhere; }}
    ul {{ padding-left: 1.4rem; }}
    .boundary {{ border-left: 4px solid #59636e; padding-left: 12px; }}
  </style>
</head>
<body>
  <main>
    <h1>Human review starting artifact</h1>
    <p class="boundary">This offline bundle covers package
      <code>{escape(package_id)}</code>, cue <code>{escape(cue_id)}</code>,
      scene <code>{escape(str(cue["scene_id"]))}</code>, frames
      <code>[{cue["start_frame"]}, {cue["end_frame"]})</code> at
      <code>{cue["fps"]} fps</code>. It makes no conclusion about neighboring
      cues.</p>
    <p>This is not creative acceptance and not a production asset.
      Rights and publication remain unresolved.</p>

    <h2>Cue excerpt</h2>
    <video controls muted preload="metadata" src="{excerpt}"
      aria-label="Cue excerpt"></video>

    <h2>Rendered frame</h2>
    <img src="{render_frame}" alt="Rendered frame from the exact cue">

    <h2>Materialized source view</h2>
    <img src="{source_view}" alt="Exact materialized source view used by the generated project">

    <h2>Files and identity</h2>
    <ul>
      <li><a href="{excerpt}">Cue excerpt MP4</a></li>
      <li><a href="{render_frame}">Rendered-frame PNG</a></li>
      <li><a href="{source_view}">Materialized-source PNG</a></li>
      <li><a href="packet/README_REVIEW.md">Source packet README</a></li>
      <li><a href="packet/packet_manifest.json">Source packet manifest</a></li>
      <li><a href="README_OPEN.md">Offline open instructions</a></li>
      <li><a href="portable_bundle_manifest.json">Portable bundle manifest</a></li>
      <li><a href="checksums.sha256">Checksums</a></li>
      <li><a href="recipient_open_receipt.template.json">Recipient-open template</a></li>
    </ul>
  </main>
</body>
</html>
"""
    return document.encode("utf-8")


def _readme_open(binding: Mapping[str, Any]) -> bytes:
    cue = binding["cue"]
    text = (
        "# Offline Review Bundle\n\n"
        "Open `index.html` directly in a local browser. No server, network, "
        "account, extension, or repository checkout is required.\n\n"
        f"- Package: `{binding['package_id']}`\n"
        f"- Cue: `{cue['cue_id']}`\n"
        f"- Frame interval: `[{cue['start_frame']}, {cue['end_frame']})` "
        f"at `{cue['fps']}` fps\n"
        f"- Source boundary: `{binding['source_identities']['source_id']}` / "
        f"`{binding['source_identities']['materialized_source_sha256']}`\n\n"
        "The video control is user-operated, muted by default, and has no "
        "autoplay. Machine-open verification does not establish human open. "
        "This bundle is a human review starting artifact; it is not creative "
        "acceptance, a production asset, rights approval, or publication "
        "authority.\n"
    )
    return text.encode("utf-8")


def _recipient_template(
    *,
    bundle_id: str,
    manifest_sha256: str,
) -> bytes:
    value = {
        "schema": RECIPIENT_OPEN_SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "bundle": {
            "bundle_id": bundle_id,
            "bundle_version": 1,
            "manifest_sha256": manifest_sha256,
            "archive_sha256": None,
        },
        "recipient_id": None,
        "transport": "not_started",
        "identity_check": "unknown",
        "machine_open": "unverified",
        "machine_open_evidence_id": None,
        "human_open": "unverified",
        "human_open_evidence_id": None,
        "content_decision": "none",
        "content_decision_receipt_id": None,
        "rights": {"approved": False, "authority_id": None},
        "production": {"approved": False, "authority_id": None},
        "publication": {"approved": False, "authority_id": None},
        "delivery_complete": False,
    }
    return canonical_json_bytes(value)


def _contract_stable_id(value: Any, *, field_path: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) > 160
        or re.fullmatch(
            r"[A-Za-z0-9]+(?:[A-Za-z0-9_.:-]*[A-Za-z0-9])?",
            value,
        )
        is None
    ):
        _fail(
            "portable manifest stable identity is invalid",
            code="review_bundle_manifest_invalid",
            field_path=field_path,
            consumer_effect="schema-invalid bundle is rejected",
        )
    return value


def _contract_sha256(value: Any, *, field_path: str) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        _fail(
            "portable manifest SHA-256 identity is invalid",
            code="review_bundle_manifest_invalid",
            field_path=field_path,
            consumer_effect="schema-invalid bundle is rejected",
        )
    return value


def _contract_int(
    value: Any,
    *,
    field_path: str,
    minimum: int,
) -> int:
    if type(value) is not int or value < minimum:
        _fail(
            "portable manifest integer is invalid",
            code="review_bundle_manifest_invalid",
            field_path=field_path,
            consumer_effect="schema-invalid bundle is rejected",
        )
    return value


def _contract_number(
    value: Any,
    *,
    field_path: str,
    minimum: float,
    exclusive: bool = False,
) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or (value <= minimum if exclusive else value < minimum)
    ):
        _fail(
            "portable manifest number is invalid",
            code="review_bundle_manifest_invalid",
            field_path=field_path,
            consumer_effect="schema-invalid bundle is rejected",
        )
    return float(value)


def _exact_contract_object(
    value: Any,
    *,
    field_path: str,
    expected: Mapping[str, Any],
) -> Mapping[str, Any]:
    result = _mapping(
        value,
        field_path=field_path,
        required=set(expected),
        allowed=set(expected),
    )
    for key, expected_value in expected.items():
        if isinstance(expected_value, bool) and type(result[key]) is not bool:
            _fail(
                "portable manifest boolean is invalid",
                code="review_bundle_manifest_invalid",
                field_path=f"{field_path}.{key}",
                consumer_effect="schema-invalid bundle is rejected",
            )
        _exact(
            result[key],
            expected_value,
            code="review_bundle_manifest_invalid",
            field_path=f"{field_path}.{key}",
            consumer_effect="schema-invalid bundle is rejected",
        )
    return result


def _validate_portable_manifest_contract(
    value: Mapping[str, Any],
) -> Mapping[str, Any]:
    top_level = {
        "schema",
        "schema_version",
        "bundle_id",
        "bundle_version",
        "source_packet",
        "package",
        "cue",
        "source_identities",
        "payload_files",
        "control_files",
        "bundle_files",
        "offline_entrypoint",
        "states",
        "retention_policy",
        "archive_policy",
    }
    manifest = _mapping(
        value,
        field_path="$.bundle.manifest",
        required=top_level,
        allowed=top_level,
    )
    _exact(
        manifest["schema"],
        BUNDLE_SCHEMA,
        code="review_bundle_manifest_invalid",
        field_path="$.bundle.manifest.schema",
    )
    _exact(
        manifest["schema_version"],
        SCHEMA_VERSION,
        code="review_bundle_manifest_invalid",
        field_path="$.bundle.manifest.schema_version",
    )
    _contract_stable_id(
        manifest["bundle_id"],
        field_path="$.bundle.manifest.bundle_id",
    )
    bundle_version = _contract_int(
        manifest["bundle_version"],
        field_path="$.bundle.manifest.bundle_version",
        minimum=1,
    )
    _exact(
        bundle_version,
        1,
        code="review_bundle_manifest_invalid",
        field_path="$.bundle.manifest.bundle_version",
    )

    source_packet_keys = {
        "packet_id",
        "packet_schema",
        "manifest_sha256",
        "tracked_receipt_sha256",
        "portable_root",
    }
    source_packet = _mapping(
        manifest["source_packet"],
        field_path="$.bundle.manifest.source_packet",
        required=source_packet_keys,
        allowed=source_packet_keys,
    )
    _contract_stable_id(
        source_packet["packet_id"],
        field_path="$.bundle.manifest.source_packet.packet_id",
    )
    _exact(
        source_packet["packet_schema"],
        "nlmytgen.cue_review_packet.v1",
        code="review_bundle_manifest_invalid",
        field_path="$.bundle.manifest.source_packet.packet_schema",
    )
    for field in ("manifest_sha256", "tracked_receipt_sha256"):
        _contract_sha256(
            source_packet[field],
            field_path=f"$.bundle.manifest.source_packet.{field}",
        )
    _exact(
        source_packet["portable_root"],
        "packet",
        code="review_bundle_manifest_invalid",
        field_path="$.bundle.manifest.source_packet.portable_root",
    )

    package_keys = {
        "package_id",
        "descriptor_sha256",
        "content_identity_sha256",
    }
    package = _mapping(
        manifest["package"],
        field_path="$.bundle.manifest.package",
        required=package_keys,
        allowed=package_keys,
    )
    _contract_stable_id(
        package["package_id"],
        field_path="$.bundle.manifest.package.package_id",
    )
    for field in ("descriptor_sha256", "content_identity_sha256"):
        _contract_sha256(
            package[field],
            field_path=f"$.bundle.manifest.package.{field}",
        )

    cue_keys = {
        "cue_id",
        "scene_id",
        "canonical_text_sha256",
        "start_frame_inclusive",
        "end_frame_exclusive",
        "length_frames",
        "fps",
        "start_seconds",
        "end_seconds",
        "context_handle_frames",
    }
    cue = _mapping(
        manifest["cue"],
        field_path="$.bundle.manifest.cue",
        required=cue_keys,
        allowed=cue_keys,
    )
    for field in ("cue_id", "scene_id"):
        _contract_stable_id(
            cue[field],
            field_path=f"$.bundle.manifest.cue.{field}",
        )
    _contract_sha256(
        cue["canonical_text_sha256"],
        field_path="$.bundle.manifest.cue.canonical_text_sha256",
    )
    start_frame = _contract_int(
        cue["start_frame_inclusive"],
        field_path="$.bundle.manifest.cue.start_frame_inclusive",
        minimum=0,
    )
    end_frame = _contract_int(
        cue["end_frame_exclusive"],
        field_path="$.bundle.manifest.cue.end_frame_exclusive",
        minimum=1,
    )
    length_frames = _contract_int(
        cue["length_frames"],
        field_path="$.bundle.manifest.cue.length_frames",
        minimum=1,
    )
    _contract_int(
        cue["fps"],
        field_path="$.bundle.manifest.cue.fps",
        minimum=1,
    )
    start_seconds = _contract_number(
        cue["start_seconds"],
        field_path="$.bundle.manifest.cue.start_seconds",
        minimum=0,
    )
    end_seconds = _contract_number(
        cue["end_seconds"],
        field_path="$.bundle.manifest.cue.end_seconds",
        minimum=0,
        exclusive=True,
    )
    context_handle = _contract_int(
        cue["context_handle_frames"],
        field_path="$.bundle.manifest.cue.context_handle_frames",
        minimum=0,
    )
    _exact(
        context_handle,
        0,
        code="review_bundle_manifest_invalid",
        field_path="$.bundle.manifest.cue.context_handle_frames",
    )
    if end_frame - start_frame != length_frames or end_seconds <= start_seconds:
        _fail(
            "portable manifest cue interval is contradictory",
            code="review_bundle_manifest_invalid",
            field_path="$.bundle.manifest.cue",
            consumer_effect="contradictory cue identity is rejected",
        )

    source_keys = {
        "source_project_sha256",
        "generated_project_sha256",
        "source_mp4_sha256",
        "source_id",
        "source_sha256",
        "materialized_source_sha256",
        "crop",
        "fit_mode",
    }
    sources = _mapping(
        manifest["source_identities"],
        field_path="$.bundle.manifest.source_identities",
        required=source_keys,
        allowed=source_keys,
    )
    for field in (
        "source_project_sha256",
        "generated_project_sha256",
        "source_mp4_sha256",
        "source_sha256",
        "materialized_source_sha256",
    ):
        _contract_sha256(
            sources[field],
            field_path=f"$.bundle.manifest.source_identities.{field}",
        )
    _contract_stable_id(
        sources["source_id"],
        field_path="$.bundle.manifest.source_identities.source_id",
    )
    crop = sources["crop"]
    if (
        not isinstance(crop, list)
        or len(crop) != 4
        or any(
            isinstance(item, bool)
            or not isinstance(item, (int, float))
            or item < 0
            or item > 1
            for item in crop
        )
    ):
        _fail(
            "portable manifest crop is invalid",
            code="review_bundle_manifest_invalid",
            field_path="$.bundle.manifest.source_identities.crop",
            consumer_effect="schema-invalid source identity is rejected",
        )
    if sources["fit_mode"] not in {"cover", "contain", "stretch"}:
        _fail(
            "portable manifest fit mode is invalid",
            code="review_bundle_manifest_invalid",
            field_path="$.bundle.manifest.source_identities.fit_mode",
            consumer_effect="schema-invalid source identity is rejected",
        )

    payload = manifest["payload_files"]
    if not isinstance(payload, list) or not 7 <= len(payload) <= 32:
        _fail(
            "portable manifest payload inventory is invalid",
            code="review_bundle_manifest_invalid",
            field_path="$.bundle.manifest.payload_files",
            consumer_effect="schema-invalid payload is rejected",
        )
    for index, item in enumerate(payload):
        field_path = f"$.bundle.manifest.payload_files[{index}]"
        keys = {"role", "path", "mime_type", "sha256", "size_bytes"}
        identity = _mapping(
            item,
            field_path=field_path,
            required=keys,
            allowed=keys,
        )
        _contract_stable_id(
            identity["role"],
            field_path=f"{field_path}.role",
        )
        _portable_path(
            identity["path"],
            field_path=f"{field_path}.path",
        )
        if (
            not isinstance(identity["mime_type"], str)
            or not 3 <= len(identity["mime_type"]) <= 128
        ):
            _fail(
                "portable manifest MIME type is invalid",
                code="review_bundle_manifest_invalid",
                field_path=f"{field_path}.mime_type",
                consumer_effect="schema-invalid payload is rejected",
            )
        _contract_sha256(
            identity["sha256"],
            field_path=f"{field_path}.sha256",
        )
        size = _contract_int(
            identity["size_bytes"],
            field_path=f"{field_path}.size_bytes",
            minimum=1,
        )
        if size > MAX_FILE_BYTES:
            _fail(
                "portable manifest payload exceeds the size ceiling",
                code="review_bundle_size_ceiling",
                field_path=f"{field_path}.size_bytes",
                consumer_effect="oversized payload is rejected",
            )

    for field, minimum, maximum in (
        ("control_files", 3, 3),
        ("bundle_files", 10, 34),
    ):
        values = manifest[field]
        if (
            not isinstance(values, list)
            or not minimum <= len(values) <= maximum
            or len(values) != len(set(values))
        ):
            _fail(
                "portable manifest file list is invalid",
                code="review_bundle_manifest_invalid",
                field_path=f"$.bundle.manifest.{field}",
                consumer_effect="schema-invalid inventory is rejected",
            )
        for index, path in enumerate(values):
            _portable_path(
                path,
                field_path=f"$.bundle.manifest.{field}[{index}]",
            )
    _exact(
        set(manifest["control_files"]),
        set(CONTROL_FILES),
        code="review_bundle_manifest_invalid",
        field_path="$.bundle.manifest.control_files",
    )
    _exact(
        manifest["offline_entrypoint"],
        "index.html",
        code="review_bundle_manifest_invalid",
        field_path="$.bundle.manifest.offline_entrypoint",
    )
    _exact_contract_object(
        manifest["states"],
        field_path="$.bundle.manifest.states",
        expected={
            "transport": "not_started",
            "identity_check": "valid",
            "machine_open": "unverified",
            "human_open": "unverified",
            "content_decision": "none",
            "delivery_complete": False,
            "rights_approved": False,
            "production_approved": False,
            "publication_approved": False,
        },
    )
    _exact_contract_object(
        manifest["retention_policy"],
        field_path="$.bundle.manifest.retention_policy",
        expected={
            "immutable": True,
            "no_overwrite": True,
            "versioned_successor_required": True,
        },
    )
    _exact_contract_object(
        manifest["archive_policy"],
        field_path="$.bundle.manifest.archive_policy",
        expected={
            "format": "zip",
            "compression": "stored",
            "normalized_timestamp": "1980-01-01T00:00:00Z",
            "encrypted": False,
            "symlinks": False,
            "hardlinks": False,
            "nested_archives": False,
            "executables": False,
        },
    )
    return manifest


def validate_recipient_open_receipt(
    value: Mapping[str, Any],
    *,
    expected_recipient_id: str | None = None,
) -> dict[str, Any]:
    required = {
        "schema",
        "schema_version",
        "bundle",
        "recipient_id",
        "transport",
        "identity_check",
        "machine_open",
        "machine_open_evidence_id",
        "human_open",
        "human_open_evidence_id",
        "content_decision",
        "content_decision_receipt_id",
        "rights",
        "production",
        "publication",
        "delivery_complete",
    }
    receipt = _mapping(
        value,
        field_path="$.recipient_open",
        required=required,
        allowed=required,
    )
    _exact(
        receipt["schema"],
        RECIPIENT_OPEN_SCHEMA,
        code="recipient_open_schema_invalid",
        field_path="$.recipient_open.schema",
    )
    _exact(
        receipt["schema_version"],
        SCHEMA_VERSION,
        code="recipient_open_schema_invalid",
        field_path="$.recipient_open.schema_version",
    )
    axes = {
        "transport": {"not_started", "completed", "failed"},
        "identity_check": {"unknown", "valid", "invalid"},
        "machine_open": {"unverified", "verified", "failed"},
        "human_open": {"unverified", "verified", "failed"},
        "content_decision": {"none", "pending", "recorded"},
    }
    for field, allowed in axes.items():
        if receipt[field] not in allowed:
            _fail(
                "recipient-open state is unsupported",
                code="recipient_open_state_invalid",
                field_path=f"$.recipient_open.{field}",
                consumer_effect="state inference is rejected",
            )
    recipient_id = receipt["recipient_id"]
    if expected_recipient_id is not None and recipient_id != expected_recipient_id:
        _fail(
            "recipient identity does not match the bounded destination",
            code="recipient_identity_mismatch",
            field_path="$.recipient_open.recipient_id",
            consumer_effect="delivery state cannot move to another recipient",
        )
    if receipt["machine_open"] == "verified" and not receipt[
        "machine_open_evidence_id"
    ]:
        _fail(
            "machine-open verified requires machine evidence",
            code="machine_open_inference_forbidden",
            field_path="$.recipient_open.machine_open_evidence_id",
            consumer_effect="machine-open is not inferred from transport",
        )
    if receipt["human_open"] == "verified" and not receipt[
        "human_open_evidence_id"
    ]:
        _fail(
            "human-open verified requires a human evidence identity",
            code="human_open_inference_forbidden",
            field_path="$.recipient_open.human_open_evidence_id",
            consumer_effect="human-open is not inferred from machine-open",
        )
    if receipt["content_decision"] == "recorded" and not receipt[
        "content_decision_receipt_id"
    ]:
        _fail(
            "recorded content decision requires its own receipt",
            code="content_decision_inference_forbidden",
            field_path="$.recipient_open.content_decision_receipt_id",
            consumer_effect="content decision is not inferred from open state",
        )
    for field in ("rights", "production", "publication"):
        axis = _mapping(
            receipt[field],
            field_path=f"$.recipient_open.{field}",
            required={"approved", "authority_id"},
            allowed={"approved", "authority_id"},
        )
        if axis["approved"] is True and not axis["authority_id"]:
            _fail(
                f"{field} approval requires independent authority",
                code="approval_inference_forbidden",
                field_path=f"$.recipient_open.{field}.authority_id",
                consumer_effect="approval is not inherited from content or open state",
            )
    if receipt["delivery_complete"] is True:
        requirements = (
            receipt["transport"] == "completed",
            receipt["identity_check"] == "valid",
            receipt["human_open"] == "verified",
            bool(receipt["recipient_id"]),
            bool(receipt["bundle"].get("archive_sha256")),
        )
        if not all(requirements):
            _fail(
                "delivery complete requires exact transport, identity, recipient, "
                "archive, and human-open evidence",
                code="delivery_complete_inference_forbidden",
                field_path="$.recipient_open.delivery_complete",
                consumer_effect="isolated machine transport is not named delivery",
            )
    return copy.deepcopy(dict(receipt))


def _assemble_bundle_files(binding: Mapping[str, Any]) -> dict[str, bytes]:
    descriptor = binding["descriptor"]
    bundle_id = descriptor["bundle_id"]
    files: dict[str, bytes] = {
        "index.html": _offline_html(binding),
        "README_OPEN.md": _readme_open(binding),
    }
    for name, path in sorted(binding["packet_files"].items()):
        files[f"packet/{name}"] = path.read_bytes()
    roles = {
        "index.html": "offline_entrypoint",
        "README_OPEN.md": "offline_instructions",
        f"packet/{binding['cue']['cue_id']}_review_excerpt.mp4": "review_excerpt",
        f"packet/{binding['cue']['cue_id']}_render_frame.png": "rendered_frame",
        (
            f"packet/{binding['cue']['cue_id']}_materialized_source_view.png"
        ): "materialized_source_view",
        "packet/README_REVIEW.md": "source_packet_readme",
        "packet/packet_manifest.json": "source_packet_manifest",
    }
    payload = [
        _file_identity(path, data, roles[path])
        for path, data in sorted(files.items())
    ]
    bundle_file_names = sorted(
        set(files)
        | {
            "portable_bundle_manifest.json",
            "recipient_open_receipt.template.json",
            "checksums.sha256",
        }
    )
    manifest = {
        "schema": BUNDLE_SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "bundle_id": bundle_id,
        "bundle_version": 1,
        "source_packet": {
            "packet_id": binding["packet_id"],
            "packet_schema": binding["packet_schema"],
            "manifest_sha256": binding["packet_manifest_sha256"],
            "tracked_receipt_sha256": binding["tracked_receipt_sha256"],
            "portable_root": "packet",
        },
        "package": {
            "package_id": binding["package_id"],
            "descriptor_sha256": binding["source_identities"][
                "descriptor_sha256"
            ],
            "content_identity_sha256": binding["source_identities"][
                "content_identity_sha256"
            ],
        },
        "cue": {
            "cue_id": binding["cue"]["cue_id"],
            "scene_id": binding["cue"]["scene_id"],
            "canonical_text_sha256": binding["cue"][
                "canonical_text_sha256"
            ],
            "start_frame_inclusive": binding["cue"]["start_frame"],
            "end_frame_exclusive": binding["cue"]["end_frame"],
            "length_frames": binding["cue"]["length_frames"],
            "fps": binding["cue"]["fps"],
            "start_seconds": binding["cue"]["start_seconds"],
            "end_seconds": binding["cue"]["end_seconds"],
            "context_handle_frames": binding["cue"]["context_handle_frames"],
        },
        "source_identities": {
            "source_project_sha256": binding["source_identities"][
                "source_project_sha256"
            ],
            "generated_project_sha256": binding["source_identities"][
                "generated_project_sha256"
            ],
            "source_mp4_sha256": binding["source_identities"][
                "source_mp4_sha256"
            ],
            "source_id": binding["source_identities"]["source_id"],
            "source_sha256": binding["source_identities"]["source_sha256"],
            "materialized_source_sha256": binding["source_identities"][
                "materialized_source_sha256"
            ],
            "crop": copy.deepcopy(binding["source_identities"]["crop"]),
            "fit_mode": binding["source_identities"]["fit_mode"],
        },
        "payload_files": payload,
        "control_files": list(CONTROL_FILES),
        "bundle_files": bundle_file_names,
        "offline_entrypoint": "index.html",
        "states": {
            "transport": "not_started",
            "identity_check": "valid",
            "machine_open": "unverified",
            "human_open": "unverified",
            "content_decision": "none",
            "delivery_complete": False,
            "rights_approved": False,
            "production_approved": False,
            "publication_approved": False,
        },
        "retention_policy": {
            "immutable": True,
            "no_overwrite": True,
            "versioned_successor_required": True,
        },
        "archive_policy": {
            "format": "zip",
            "compression": "stored",
            "normalized_timestamp": "1980-01-01T00:00:00Z",
            "encrypted": False,
            "symlinks": False,
            "hardlinks": False,
            "nested_archives": False,
            "executables": False,
        },
    }
    manifest_bytes = canonical_json_bytes(manifest)
    _scan_text(
        manifest_bytes.decode("utf-8"),
        field_path="$.portable_bundle_manifest",
        allow_relative_lineage=False,
    )
    files["portable_bundle_manifest.json"] = manifest_bytes
    files["recipient_open_receipt.template.json"] = _recipient_template(
        bundle_id=bundle_id,
        manifest_sha256=sha256_bytes(manifest_bytes),
    )
    checksum_lines = [
        f"{sha256_bytes(data)}  {path}"
        for path, data in sorted(files.items())
    ]
    files["checksums.sha256"] = (
        "\n".join(checksum_lines) + "\n"
    ).encode("ascii")
    return dict(sorted(files.items()))


def _zip_bytes(files: Mapping[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(
        buffer,
        mode="w",
        compression=zipfile.ZIP_STORED,
        allowZip64=False,
    ) as archive:
        for path, data in sorted(files.items()):
            safe = _portable_path(path, field_path=f"$.archive.{path}")
            info = zipfile.ZipInfo(safe, NORMALIZED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.flag_bits = 0x800
            archive.writestr(info, data)
    return buffer.getvalue()


def _semantic_inventory(files: Mapping[str, bytes]) -> list[dict[str, Any]]:
    return [
        {
            "path": path,
            "sha256": sha256_bytes(data),
            "size_bytes": len(data),
        }
        for path, data in sorted(files.items())
    ]


def _semantic_identity(files: Mapping[str, bytes]) -> str:
    return sha256_bytes(canonical_json_bytes(_semantic_inventory(files)))


def _write_directory(root: Path, files: Mapping[str, bytes]) -> None:
    root.mkdir(parents=True, exist_ok=False)
    for relative, data in sorted(files.items()):
        path = root / Path(*PurePosixPath(relative).parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(data)


def build_portable_review_bundle(
    *,
    repo_root: Path,
    packet_path: str | Path,
    output_path: str | Path,
    archive_path: str | Path,
    descriptor_path: str | Path | None = None,
) -> dict[str, Any]:
    binding = inspect_source_packet(
        repo_root=repo_root,
        packet_path=packet_path,
        descriptor_path=descriptor_path,
    )
    descriptor = binding["descriptor"]
    output_locator, output_root = _repo_path(
        repo_root,
        output_path,
        field_path="$.output",
        require_exists=False,
    )
    archive_locator, archive = _repo_path(
        repo_root,
        archive_path,
        field_path="$.archive",
        require_exists=False,
        allow_archive=True,
    )
    _exact(
        output_locator,
        descriptor["output"]["directory"],
        code="review_bundle_output_identity_mismatch",
        field_path="$.output",
    )
    _exact(
        archive_locator,
        descriptor["output"]["archive"],
        code="review_bundle_output_identity_mismatch",
        field_path="$.archive",
    )
    if output_root.exists() or archive.exists():
        _fail(
            "portable bundle output already exists",
            code="review_bundle_overwrite_forbidden",
            field_path="$.output",
            consumer_effect="versioned output is never overwritten",
        )
    before = binding["source_snapshot"]
    files_first = _assemble_bundle_files(binding)
    files_second = _assemble_bundle_files(binding)
    if files_first != files_second:
        _fail(
            "portable bundle assembly is not deterministic",
            code="review_bundle_determinism_failed",
            field_path="$.bundle",
            consumer_effect="nondeterministic bytes are not transported",
        )
    archive_first = _zip_bytes(files_first)
    archive_second = _zip_bytes(files_second)
    if archive_first != archive_second:
        _fail(
            "portable ZIP bytes are not deterministic",
            code="review_bundle_determinism_failed",
            field_path="$.archive",
            consumer_effect="nondeterministic archive is not transported",
        )
    _write_directory(output_root, files_first)
    archive.parent.mkdir(parents=True, exist_ok=True)
    with archive.open("xb") as handle:
        handle.write(archive_first)
    after = _snapshot(binding["packet_files"])
    if after != before:
        _fail(
            "source packet changed during bundle creation",
            code="source_packet_mutated",
            field_path="$.packet",
            consumer_effect="source mutation is never accepted as packaging",
        )
    validated_dir = validate_portable_review_bundle(
        bundle_path=output_root,
        check_machine_open=False,
    )
    validated_zip = validate_portable_review_bundle(
        bundle_path=archive,
        check_machine_open=False,
    )
    _exact(
        validated_dir["semantic_identity_sha256"],
        validated_zip["semantic_identity_sha256"],
        code="review_bundle_directory_archive_mismatch",
        field_path="$.archive",
        consumer_effect="directory and archive must carry the same bytes",
    )
    return {
        "schema": "nlmytgen.portable_review_bundle_build_result.v1",
        "schema_version": SCHEMA_VERSION,
        "status": "succeeded",
        "bundle_id": descriptor["bundle_id"],
        "authority_id": descriptor["authority_id"],
        "source_packet": {
            "packet_id": binding["packet_id"],
            "manifest_sha256": binding["packet_manifest_sha256"],
            "tracked_receipt_sha256": binding["tracked_receipt_sha256"],
            "source_file_mismatch_count": 0,
        },
        "output": {
            "directory": output_locator,
            "archive": archive_locator,
            "archive_sha256": sha256_bytes(archive_first),
            "archive_size_bytes": len(archive_first),
            "manifest_sha256": sha256_bytes(
                files_first["portable_bundle_manifest.json"]
            ),
            "semantic_identity_sha256": _semantic_identity(files_first),
            "file_count": len(files_first),
        },
        "determinism": {
            "assembly_count": 2,
            "directory_payload_byte_identical": True,
            "archive_byte_identical": True,
            "normalized_zip_timestamp": "1980-01-01T00:00:00Z",
        },
        "states": {
            "transport": "not_started",
            "identity_check": "valid",
            "machine_open": "unverified",
            "human_open": "unverified",
            "content_decision": "none",
            "delivery_complete": False,
        },
        "boundaries": {
            "source_packet_regeneration_count": 0,
            "source_packet_mutation_count": 0,
            "transcode_count": 0,
            "yymm4_launch_count": 0,
            "render_driver_launch_count": 0,
            "full_render_count": 0,
            "playback_count": 0,
            "network_request_count": 0,
            "external_transfer_count": 0,
        },
    }


class _OfflineIndexParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []
        self.video_attrs: list[dict[str, str | None]] = []
        self.image_sources: list[str] = []
        self.focusable_tags: list[str] = []
        self.svg_count = 0

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        values = dict(attrs)
        if tag == "svg":
            self.svg_count += 1
        for key in ("href", "src"):
            value = values.get(key)
            if value:
                self.references.append(value)
        if tag == "video":
            self.video_attrs.append(values)
            self.focusable_tags.append("video")
        elif tag == "a" and values.get("href"):
            self.focusable_tags.append("a")
        if tag == "img" and values.get("src"):
            self.image_sources.append(str(values["src"]))


def _validate_offline_index(
    files: Mapping[str, bytes],
) -> dict[str, Any]:
    raw = files.get("index.html")
    if raw is None:
        _fail(
            "offline entrypoint is missing",
            code="review_bundle_entrypoint_missing",
            field_path="$.bundle.index.html",
            consumer_effect="bundle cannot be machine-opened",
        )
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PortableReviewBundleError(
            "offline entrypoint is not UTF-8",
            code="review_bundle_html_invalid",
            field_path="$.bundle.index.html",
            consumer_effect="invalid offline surface is not opened",
        ) from exc
    _scan_text(
        text,
        field_path="$.bundle.index.html",
        allow_relative_lineage=False,
    )
    parser = _OfflineIndexParser()
    parser.feed(text)
    if parser.svg_count:
        _fail(
            "offline entrypoint contains SVG",
            code="review_bundle_html_visual_scope_invalid",
            field_path="$.bundle.index.html",
            consumer_effect="offline surface remains plain and document-first",
        )
    if re.search(r"(?i)\b(?:https?:)?//|url\s*\(", text):
        _fail(
            "offline entrypoint contains an external resource",
            code="review_bundle_external_resource",
            field_path="$.bundle.index.html",
            consumer_effect="offline open performs no network request",
        )
    if len(parser.video_attrs) != 1:
        _fail(
            "offline entrypoint must contain one video control",
            code="review_bundle_video_contract_invalid",
            field_path="$.bundle.index.html.video",
            consumer_effect="review media remains explicit and user-controlled",
        )
    video = parser.video_attrs[0]
    if "autoplay" in video:
        _fail(
            "offline video enables autoplay",
            code="review_bundle_autoplay_forbidden",
            field_path="$.bundle.index.html.video.autoplay",
            consumer_effect="machine open never starts playback",
        )
    if "controls" not in video or "muted" not in video:
        _fail(
            "offline video must expose controls and default muted",
            code="review_bundle_video_contract_invalid",
            field_path="$.bundle.index.html.video",
            consumer_effect="review media remains user-controlled and silent",
        )
    if video.get("preload") not in {"metadata", "none"}:
        _fail(
            "offline video preload must be metadata or none",
            code="review_bundle_video_contract_invalid",
            field_path="$.bundle.index.html.video.preload",
            consumer_effect="machine open remains bounded",
        )
    normalized_refs: list[str] = []
    for index, reference in enumerate(parser.references):
        if reference.startswith("#"):
            continue
        normalized = _portable_path(
            reference,
            field_path=f"$.bundle.index.html.references[{index}]",
        )
        if normalized not in files:
            _fail(
                "offline entrypoint contains an unresolved bundle link",
                code="review_bundle_link_unresolved",
                field_path=f"$.bundle.index.html.references[{index}]",
                consumer_effect="recipient receives no broken local links",
            )
        normalized_refs.append(normalized)
    if len(parser.image_sources) != 2:
        _fail(
            "offline entrypoint must show both exact PNG review surfaces",
            code="review_bundle_image_contract_invalid",
            field_path="$.bundle.index.html.img",
            consumer_effect="machine-open verifies both required images",
        )
    return {
        "status": "passed",
        "reference_count": len(normalized_refs),
        "image_count": len(parser.image_sources),
        "video_count": 1,
        "autoplay": False,
        "muted_default": True,
        "preload": video.get("preload"),
        "focusable_surface_count": len(parser.focusable_tags),
        "external_resource_count": 0,
    }


def _directory_files(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        _fail(
            "bundle directory is unavailable",
            code="source_bundle_unavailable",
            field_path="$.bundle",
            consumer_effect="absence remains explicit",
        )
    files: dict[str, bytes] = {}
    normalized_seen: set[str] = set()
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            relative = path.relative_to(root).as_posix()
            _fail(
                "bundle contains a symlink",
                code="review_bundle_symlink_forbidden",
                field_path=f"$.bundle.{relative}",
                consumer_effect="linked data is never transported",
            )
        if path.is_dir():
            continue
        relative = path.relative_to(root).as_posix()
        normalized = _portable_path(
            relative,
            field_path=f"$.bundle.{relative}",
        )
        key = normalized.casefold()
        if key in normalized_seen:
            _fail(
                "bundle contains a duplicate normalized path",
                code="review_bundle_duplicate_path",
                field_path=f"$.bundle.{relative}",
                consumer_effect="ambiguous paths are never transported",
            )
        normalized_seen.add(key)
        if path.stat().st_nlink > 1:
            _fail(
                "bundle contains a hardlink",
                code="review_bundle_hardlink_forbidden",
                field_path=f"$.bundle.{relative}",
                consumer_effect="linked data is never transported",
            )
        if path.stat().st_size > MAX_FILE_BYTES:
            _fail(
                "bundle file exceeds the declared size ceiling",
                code="review_bundle_size_ceiling",
                field_path=f"$.bundle.{relative}",
                consumer_effect="oversized payload is rejected before transport",
            )
        files[normalized] = path.read_bytes()
    return files


def _archive_files(path: Path) -> dict[str, bytes]:
    try:
        archive = zipfile.ZipFile(path, mode="r")
    except (OSError, zipfile.BadZipFile) as exc:
        raise PortableReviewBundleError(
            "portable ZIP is unavailable or invalid",
            code="review_bundle_archive_invalid",
            field_path="$.bundle",
            consumer_effect="invalid archive is never extracted",
        ) from exc
    with archive:
        infos = archive.infolist()
        if len(infos) > MAX_ARCHIVE_FILES:
            _fail(
                "archive contains too many files",
                code="review_bundle_size_ceiling",
                field_path="$.bundle",
                consumer_effect="archive bomb is rejected before extraction",
            )
        files: dict[str, bytes] = {}
        normalized_seen: set[str] = set()
        total_size = 0
        for index, info in enumerate(infos):
            if info.is_dir():
                _fail(
                    "archive directory entries are not canonical",
                    code="review_bundle_path_unsafe",
                    field_path=f"$.bundle.entries[{index}]",
                    consumer_effect="archive inventory remains file-only and exact",
                )
            normalized = _portable_path(
                info.filename,
                field_path=f"$.bundle.entries[{index}].path",
            )
            if (
                info.date_time != NORMALIZED_ZIP_TIME
                or info.compress_type != zipfile.ZIP_STORED
            ):
                _fail(
                    "archive metadata violates the deterministic storage policy",
                    code="review_bundle_archive_policy_invalid",
                    field_path=f"$.bundle.entries[{index}]",
                    consumer_effect="noncanonical archive metadata is rejected",
                )
            key = normalized.casefold()
            if key in normalized_seen:
                _fail(
                    "archive contains a duplicate normalized path",
                    code="review_bundle_duplicate_path",
                    field_path=f"$.bundle.entries[{index}]",
                    consumer_effect="ambiguous paths are never extracted",
                )
            normalized_seen.add(key)
            mode = (info.external_attr >> 16) & 0xFFFF
            if stat.S_ISLNK(mode):
                _fail(
                    "archive contains a symlink",
                    code="review_bundle_symlink_forbidden",
                    field_path=f"$.bundle.entries[{index}]",
                    consumer_effect="linked data is never extracted",
                )
            if info.flag_bits & 0x1:
                _fail(
                    "archive is encrypted",
                    code="review_bundle_encryption_forbidden",
                    field_path=f"$.bundle.entries[{index}]",
                    consumer_effect="recipient receives inspectable bytes",
                )
            if info.file_size > MAX_FILE_BYTES:
                _fail(
                    "archive member exceeds the declared size ceiling",
                    code="review_bundle_size_ceiling",
                    field_path=f"$.bundle.entries[{index}]",
                    consumer_effect="archive bomb is rejected before extraction",
                )
            total_size += info.file_size
            if total_size > MAX_TOTAL_BYTES:
                _fail(
                    "archive exceeds the total declared size ceiling",
                    code="review_bundle_size_ceiling",
                    field_path="$.bundle",
                    consumer_effect="archive bomb is rejected before extraction",
                )
            compressed = max(info.compress_size, 1)
            if info.file_size > 1024 and info.file_size / compressed > (
                MAX_COMPRESSION_RATIO
            ):
                _fail(
                    "archive member has an unsafe compression ratio",
                    code="review_bundle_size_ceiling",
                    field_path=f"$.bundle.entries[{index}]",
                    consumer_effect="archive bomb is rejected before extraction",
                )
            try:
                files[normalized] = archive.read(info)
            except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
                raise PortableReviewBundleError(
                    "archive member failed integrity read",
                    code="review_bundle_archive_hash_mismatch",
                    field_path=f"$.bundle.entries[{index}]",
                    consumer_effect="corrupt archive is never extracted",
                ) from exc
        return files


def _parse_checksums(raw: bytes) -> dict[str, str]:
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        raise PortableReviewBundleError(
            "checksum file is not ASCII",
            code="review_bundle_checksum_invalid",
            field_path="$.bundle.checksums",
            consumer_effect="unverifiable bundle is rejected",
        ) from exc
    result: dict[str, str] = {}
    for index, line in enumerate(lines):
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match is None:
            _fail(
                "checksum line is invalid",
                code="review_bundle_checksum_invalid",
                field_path=f"$.bundle.checksums[{index}]",
                consumer_effect="unverifiable bundle is rejected",
            )
        path = _portable_path(
            match.group(2),
            field_path=f"$.bundle.checksums[{index}].path",
        )
        if path in result:
            _fail(
                "checksum file contains a duplicate path",
                code="review_bundle_duplicate_path",
                field_path=f"$.bundle.checksums[{index}]",
                consumer_effect="ambiguous checksums are rejected",
            )
        result[path] = match.group(1)
    return result


def _run_media(command: list[str], *, code: str) -> str:
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PortableReviewBundleError(
            "portable media decode validation failed",
            code=code,
            field_path="$.bundle.packet",
            consumer_effect="invalid media is not promoted to machine-open",
        ) from exc
    return completed.stdout


def _probe_media(root: Path, manifest: Mapping[str, Any]) -> dict[str, Any]:
    payload = manifest["payload_files"]
    roles = {
        item["role"]: item["path"]
        for item in payload
        if isinstance(item, Mapping)
    }
    excerpt = root / Path(*PurePosixPath(roles["review_excerpt"]).parts)
    frame = root / Path(*PurePosixPath(roles["rendered_frame"]).parts)
    source = root / Path(
        *PurePosixPath(roles["materialized_source_view"]).parts
    )
    probe_text = _run_media(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            (
                "format=duration:"
                "stream=codec_name,codec_type,width,height,r_frame_rate,"
                "sample_rate,channels"
            ),
            "-of",
            "json",
            str(excerpt),
        ],
        code="review_bundle_media_probe_failed",
    )
    try:
        probe = json.loads(probe_text)
    except json.JSONDecodeError as exc:
        raise PortableReviewBundleError(
            "ffprobe returned invalid JSON",
            code="review_bundle_media_probe_failed",
            field_path="$.bundle.packet.review_excerpt",
            consumer_effect="invalid media is not promoted to machine-open",
        ) from exc
    streams = probe.get("streams", [])
    video = next(
        (row for row in streams if row.get("codec_type") == "video"),
        None,
    )
    audio = next(
        (row for row in streams if row.get("codec_type") == "audio"),
        None,
    )
    if (
        not isinstance(video, Mapping)
        or not isinstance(audio, Mapping)
        or video.get("codec_name") != "h264"
        or audio.get("codec_name") != "aac"
        or video.get("width") != 1920
        or video.get("height") != 1080
    ):
        _fail(
            "portable excerpt media properties differ from the packet contract",
            code="review_bundle_media_contract_invalid",
            field_path="$.bundle.packet.review_excerpt",
            consumer_effect="unexpected media is not promoted to machine-open",
        )
    _run_media(
        [
            "ffmpeg",
            "-v",
            "error",
            "-nostdin",
            "-i",
            str(excerpt),
            "-map",
            "0:v:0",
            "-map",
            "0:a:0",
            "-f",
            "null",
            os.devnull,
        ],
        code="review_bundle_media_decode_failed",
    )
    for image in (frame, source):
        _run_media(
            [
                "ffmpeg",
                "-v",
                "error",
                "-nostdin",
                "-i",
                str(image),
                "-f",
                "null",
                os.devnull,
            ],
            code="review_bundle_image_decode_failed",
        )
    return {
        "status": "passed",
        "video_codec": "h264",
        "audio_codec": "aac",
        "width": 1920,
        "height": 1080,
        "fps": video.get("r_frame_rate"),
        "sample_rate": audio.get("sample_rate"),
        "channels": audio.get("channels"),
        "full_video_decode": "passed",
        "full_audio_decode": "passed",
        "png_decode_count": 2,
        "playback_count": 0,
        "audio_output_count": 0,
        "transcode_count": 0,
    }


def _extract_file_map(root: Path, files: Mapping[str, bytes]) -> None:
    root.mkdir(parents=True, exist_ok=False)
    for relative, data in sorted(files.items()):
        path = root / Path(*PurePosixPath(relative).parts)
        resolved = path.resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            _fail(
                "extracted path escapes destination",
                code="review_bundle_path_unsafe",
                field_path=f"$.extract.{relative}",
                consumer_effect="unsafe archive is never extracted",
            )
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(data)


def validate_portable_review_bundle(
    *,
    bundle_path: str | Path,
    check_machine_open: bool = False,
) -> dict[str, Any]:
    path = Path(bundle_path).resolve()
    archive_sha256: str | None = None
    if path.is_dir():
        files = _directory_files(path)
        source_kind = "directory"
    elif path.is_file() and path.suffix.lower() == ".zip":
        files = _archive_files(path)
        source_kind = "zip"
        archive_sha256 = sha256_file(path)
    else:
        _fail(
            "portable bundle directory or ZIP is unavailable",
            code="source_bundle_unavailable",
            field_path="$.bundle",
            consumer_effect="absence remains explicit and triggers no fallback",
        )
    if len(files) > MAX_ARCHIVE_FILES:
        _fail(
            "portable bundle contains too many files",
            code="review_bundle_size_ceiling",
            field_path="$.bundle",
            consumer_effect="oversized bundle is rejected",
        )
    total_size = sum(len(data) for data in files.values())
    if total_size > MAX_TOTAL_BYTES:
        _fail(
            "portable bundle exceeds the total size ceiling",
            code="review_bundle_size_ceiling",
            field_path="$.bundle",
            consumer_effect="oversized bundle is rejected",
        )
    manifest_raw = files.get("portable_bundle_manifest.json")
    if manifest_raw is None:
        _fail(
            "portable bundle manifest is missing",
            code="review_bundle_manifest_missing",
            field_path="$.bundle.portable_bundle_manifest",
            consumer_effect="unidentified bundle is rejected",
        )
    try:
        manifest = json.loads(manifest_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PortableReviewBundleError(
            "portable bundle manifest is invalid",
            code="review_bundle_manifest_invalid",
            field_path="$.bundle.portable_bundle_manifest",
            consumer_effect="unidentified bundle is rejected",
        ) from exc
    manifest = _validate_portable_manifest_contract(
        _mapping(manifest, field_path="$.bundle.manifest")
    )
    declared_files = manifest.get("bundle_files")
    if not isinstance(declared_files, list):
        _fail(
            "bundle manifest file inventory is invalid",
            code="review_bundle_manifest_invalid",
            field_path="$.bundle.manifest.bundle_files",
            consumer_effect="incomplete inventory is rejected",
        )
    normalized_declared = [
        _portable_path(
            item,
            field_path=f"$.bundle.manifest.bundle_files[{index}]",
        )
        for index, item in enumerate(declared_files)
    ]
    _exact(
        sorted(normalized_declared),
        sorted(files),
        code="review_bundle_file_set_mismatch",
        field_path="$.bundle.manifest.bundle_files",
        consumer_effect="directory and manifest inventory must be exact",
    )
    checksum_raw = files.get("checksums.sha256")
    if checksum_raw is None:
        _fail(
            "bundle checksum file is missing",
            code="review_bundle_checksum_invalid",
            field_path="$.bundle.checksums",
            consumer_effect="unverifiable bundle is rejected",
        )
    checksums = _parse_checksums(checksum_raw)
    expected_checksum_paths = sorted(set(files) - {"checksums.sha256"})
    _exact(
        sorted(checksums),
        expected_checksum_paths,
        code="review_bundle_checksum_invalid",
        field_path="$.bundle.checksums",
        consumer_effect="checksum coverage must be exact",
    )
    for relative, expected_hash in checksums.items():
        _exact(
            sha256_bytes(files[relative]),
            expected_hash,
            code="review_bundle_archive_hash_mismatch",
            field_path=f"$.bundle.{relative}.sha256",
            consumer_effect="modified archive or file bytes are rejected",
        )
    payload = manifest.get("payload_files")
    if not isinstance(payload, list):
        _fail(
            "bundle payload inventory is invalid",
            code="review_bundle_manifest_invalid",
            field_path="$.bundle.manifest.payload_files",
            consumer_effect="incomplete payload inventory is rejected",
        )
    payload_paths: set[str] = set()
    for index, item in enumerate(payload):
        item = _mapping(
            item,
            field_path=f"$.bundle.manifest.payload_files[{index}]",
        )
        relative = _portable_path(
            item.get("path"),
            field_path=f"$.bundle.manifest.payload_files[{index}].path",
        )
        if relative in payload_paths:
            _fail(
                "payload inventory contains a duplicate path",
                code="review_bundle_duplicate_path",
                field_path=f"$.bundle.manifest.payload_files[{index}]",
                consumer_effect="ambiguous payload is rejected",
            )
        payload_paths.add(relative)
        if relative not in files:
            _fail(
                "payload inventory references a missing file",
                code="review_bundle_file_set_mismatch",
                field_path=f"$.bundle.manifest.payload_files[{index}]",
                consumer_effect="incomplete payload is rejected",
            )
        _exact(
            sha256_bytes(files[relative]),
            item.get("sha256"),
            code="review_bundle_archive_hash_mismatch",
            field_path=f"$.bundle.manifest.payload_files[{index}].sha256",
        )
        _exact(
            len(files[relative]),
            item.get("size_bytes"),
            code="review_bundle_archive_hash_mismatch",
            field_path=f"$.bundle.manifest.payload_files[{index}].size_bytes",
        )
        _exact(
            _mime_type(relative),
            item.get("mime_type"),
            code="review_bundle_manifest_invalid",
            field_path=f"$.bundle.manifest.payload_files[{index}].mime_type",
        )
    _exact(
        manifest.get("offline_entrypoint"),
        "index.html",
        code="review_bundle_entrypoint_missing",
        field_path="$.bundle.manifest.offline_entrypoint",
    )
    offline = _validate_offline_index(files)
    template_raw = files.get("recipient_open_receipt.template.json")
    if template_raw is None:
        _fail(
            "recipient-open template is missing",
            code="recipient_open_schema_invalid",
            field_path="$.bundle.recipient_open",
            consumer_effect="recipient clocks cannot be separated",
        )
    try:
        recipient = json.loads(template_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PortableReviewBundleError(
            "recipient-open template is invalid",
            code="recipient_open_schema_invalid",
            field_path="$.bundle.recipient_open",
            consumer_effect="recipient clocks cannot be separated",
        ) from exc
    recipient_result = validate_recipient_open_receipt(recipient)
    _exact(
        recipient_result["bundle"]["manifest_sha256"],
        sha256_bytes(manifest_raw),
        code="recipient_open_bundle_identity_mismatch",
        field_path="$.bundle.recipient_open.bundle.manifest_sha256",
    )
    _scan_text(
        manifest_raw.decode("utf-8"),
        field_path="$.bundle.manifest",
        allow_relative_lineage=False,
    )
    _scan_text(
        files["README_OPEN.md"].decode("utf-8"),
        field_path="$.bundle.README_OPEN",
        allow_relative_lineage=False,
    )
    media = {
        "status": "not_requested",
        "playback_count": 0,
        "audio_output_count": 0,
        "transcode_count": 0,
    }
    if check_machine_open:
        if source_kind == "directory":
            media = _probe_media(path, manifest)
        else:
            with tempfile.TemporaryDirectory(
                prefix="nlmytgen-portable-review-validate-"
            ) as temp:
                temp_root = Path(temp) / "bundle"
                _extract_file_map(temp_root, files)
                media = _probe_media(temp_root, manifest)
    return {
        "schema": "nlmytgen.portable_review_bundle_validation.v1",
        "schema_version": SCHEMA_VERSION,
        "status": "passed",
        "source_kind": source_kind,
        "bundle_id": manifest["bundle_id"],
        "bundle_version": manifest["bundle_version"],
        "manifest_sha256": sha256_bytes(manifest_raw),
        "archive_sha256": archive_sha256,
        "semantic_identity_sha256": _semantic_identity(files),
        "file_count": len(files),
        "total_size_bytes": total_size,
        "inventory": _semantic_inventory(files),
        "offline_index": offline,
        "media_decode": media,
        "states": copy.deepcopy(manifest["states"]),
        "path_safety": {
            "absolute_paths": 0,
            "traversal_paths": 0,
            "duplicate_normalized_paths": 0,
            "symlinks": 0,
            "hardlinks": 0,
            "executables": 0,
            "nested_archives": 0,
            "encrypted_files": 0,
        },
        "boundaries": {
            "network_request_count": 0,
            "playback_count": 0,
            "audio_output_count": 0,
            "transcode_count": 0,
            "source_packet_regeneration_count": 0,
            "yymm4_launch_count": 0,
            "render_driver_launch_count": 0,
        },
    }


def transport_portable_review_bundle(
    *,
    archive_path: str | Path,
    destination_root: str | Path,
    recipient_id: str,
    expected_recipient_id: str,
) -> dict[str, Any]:
    if recipient_id != expected_recipient_id:
        _fail(
            "recipient identity does not match the bounded test recipient",
            code="recipient_identity_mismatch",
            field_path="$.recipient_id",
            consumer_effect="transport cannot move to another recipient",
        )
    if not re.fullmatch(r"[A-Za-z0-9]+(?:[A-Za-z0-9_.-]*[A-Za-z0-9])?", recipient_id):
        _fail(
            "recipient identity is not sanitized",
            code="recipient_identity_mismatch",
            field_path="$.recipient_id",
            consumer_effect="tracked evidence stores no machine or user identity",
        )
    archive = Path(archive_path).resolve()
    destination = Path(destination_root).resolve()
    if destination.exists():
        _fail(
            "recipient destination already exists",
            code="recipient_destination_exists",
            field_path="$.destination",
            consumer_effect="recipient transport never overwrites prior evidence",
        )
    archive_validation = validate_portable_review_bundle(
        bundle_path=archive,
        check_machine_open=False,
    )
    source_hash = sha256_file(archive)
    destination.mkdir(parents=True, exist_ok=False)
    incoming = destination / "incoming" / archive.name
    incoming.parent.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(archive, incoming)
    copied_hash = sha256_file(incoming)
    _exact(
        copied_hash,
        source_hash,
        code="recipient_archive_copy_mismatch",
        field_path="$.destination.archive",
        consumer_effect="transport identity must be byte-exact",
    )
    files = _archive_files(incoming)
    extracted = destination / "extracted" / archive.stem
    extracted.parent.mkdir(parents=True, exist_ok=False)
    _extract_file_map(extracted, files)
    extracted_validation = validate_portable_review_bundle(
        bundle_path=extracted,
        check_machine_open=False,
    )
    _exact(
        extracted_validation["semantic_identity_sha256"],
        archive_validation["semantic_identity_sha256"],
        code="recipient_extraction_identity_mismatch",
        field_path="$.destination.extracted",
        consumer_effect="recipient extraction must preserve every bundle byte",
    )
    return {
        "schema": "nlmytgen.portable_review_bundle_transport.v1",
        "schema_version": SCHEMA_VERSION,
        "status": "passed",
        "recipient_id": recipient_id,
        "archive_sha256": source_hash,
        "copied_archive_sha256": copied_hash,
        "archive_copy_mismatch_count": 0,
        "extracted_semantic_identity_sha256": extracted_validation[
            "semantic_identity_sha256"
        ],
        "extracted_file_count": extracted_validation["file_count"],
        "destination": destination,
        "extracted_bundle": extracted,
        "states": {
            "transport": "completed",
            "identity_check": "valid",
            "machine_open": "unverified",
            "human_open": "unverified",
            "content_decision": "none",
            "delivery_complete": False,
        },
        "boundaries": {
            "overwrite_count": 0,
            "private_source_copy_count": 0,
            "network_request_count": 0,
            "external_transfer_count": 0,
        },
    }



REGISTRY_SCHEMA = "nlmytgen.review_bundle_registry.v1"
INGEST_AUTHORITY_SCHEMA = "nlmytgen.review_bundle_ingest_authority.v1"
INGEST_RESULT_SCHEMA = "nlmytgen.review_bundle_ingest_result.v1"
ARTIFACT_STATUSES = {"active", "revoked", "superseded"}
TRANSPORT_MODES = {"local_ingest", "named_terminal_delivery"}
_REGISTRY_FIELDS = {"schema", "schema_version", "recipient_id", "entries"}
_REGISTRY_ENTRY_FIELDS = {
    "registry_key_sha256",
    "bundle_id",
    "bundle_version",
    "archive_sha256",
    "recipient_id",
    "manifest_sha256",
    "semantic_identity_sha256",
    "transport_authority_id",
    "transport_mode",
    "artifact_status",
    "named_terminal_id",
    "named_terminal_transport",
    "machine_open",
    "human_open",
    "content_decision",
    "delivery_complete",
}


def _registry_object(
    value: Any,
    *,
    fields: set[str],
    field_path: str,
    code: str,
) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != fields:
        _fail(
            "review bundle recipient-registry object is not exact",
            code=code,
            field_path=field_path,
            consumer_effect="ambiguous recipient state is rejected",
        )
    return value


def _registry_stable_id(value: Any, *, field_path: str, code: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) > 160
        or re.fullmatch(
            r"[A-Za-z0-9]+(?:[A-Za-z0-9_.:-]*[A-Za-z0-9])?",
            value,
        )
        is None
    ):
        _fail(
            "review bundle recipient-registry identity is invalid",
            code=code,
            field_path=field_path,
            consumer_effect="unbound recipient or authority identity is rejected",
        )
    return value


def _registry_sha256(value: Any, *, field_path: str, code: str) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        _fail(
            "review bundle recipient-registry SHA-256 is invalid",
            code=code,
            field_path=field_path,
            consumer_effect="unverifiable artifact identity is rejected",
        )
    return value


def _registry_bundle_version(value: Any, *, field_path: str, code: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        _fail(
            "review bundle recipient-registry version is invalid",
            code=code,
            field_path=field_path,
            consumer_effect="unversioned artifact identity is rejected",
        )
    return value


def _review_bundle_registry_key(
    *,
    bundle_id: str,
    bundle_version: int,
    archive_sha256: str,
    recipient_id: str,
) -> tuple[str, int, str, str]:
    return bundle_id, bundle_version, archive_sha256, recipient_id


def _review_bundle_registry_key_sha256(
    key: tuple[str, int, str, str],
) -> str:
    return sha256_bytes(
        canonical_json_bytes(
            {
                "bundle_id": key[0],
                "bundle_version": key[1],
                "archive_sha256": key[2],
                "recipient_id": key[3],
            }
        )
    )


def empty_review_bundle_registry(*, recipient_id: str) -> dict[str, Any]:
    recipient = _registry_stable_id(
        recipient_id,
        field_path="$.recipient_id",
        code="review_bundle_registry_invalid",
    )
    return {
        "schema": REGISTRY_SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "recipient_id": recipient,
        "entries": [],
    }


def validate_review_bundle_registry(
    value: Any,
    *,
    expected_recipient_id: str | None = None,
) -> dict[str, Any]:
    registry = _registry_object(
        value,
        fields=_REGISTRY_FIELDS,
        field_path="$",
        code="review_bundle_registry_invalid",
    )
    if (
        registry["schema"] != REGISTRY_SCHEMA
        or registry["schema_version"] != SCHEMA_VERSION
    ):
        _fail(
            "review bundle recipient-registry schema is unsupported",
            code="review_bundle_registry_invalid",
            field_path="$.schema",
            consumer_effect="unknown recipient state is rejected",
        )
    recipient_id = _registry_stable_id(
        registry["recipient_id"],
        field_path="$.recipient_id",
        code="review_bundle_registry_invalid",
    )
    if expected_recipient_id is not None and recipient_id != expected_recipient_id:
        _fail(
            "review bundle recipient-registry is bound to another recipient",
            code="recipient_identity_mismatch",
            field_path="$.recipient_id",
            consumer_effect="one recipient cannot ingest another recipient's registry",
        )
    if not isinstance(registry["entries"], list):
        _fail(
            "review bundle recipient-registry entries must be an array",
            code="review_bundle_registry_invalid",
            field_path="$.entries",
            consumer_effect="malformed recipient state is rejected",
        )

    entries: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, int, str, str]] = set()
    seen_versions: dict[tuple[str, int, str], str] = {}
    for index, raw_entry in enumerate(registry["entries"]):
        field_path = f"$.entries[{index}]"
        entry = _registry_object(
            raw_entry,
            fields=_REGISTRY_ENTRY_FIELDS,
            field_path=field_path,
            code="review_bundle_registry_invalid",
        )
        bundle_id = _registry_stable_id(
            entry["bundle_id"],
            field_path=f"{field_path}.bundle_id",
            code="review_bundle_registry_invalid",
        )
        bundle_version = _registry_bundle_version(
            entry["bundle_version"],
            field_path=f"{field_path}.bundle_version",
            code="review_bundle_registry_invalid",
        )
        archive_sha256 = _registry_sha256(
            entry["archive_sha256"],
            field_path=f"{field_path}.archive_sha256",
            code="review_bundle_registry_invalid",
        )
        entry_recipient = _registry_stable_id(
            entry["recipient_id"],
            field_path=f"{field_path}.recipient_id",
            code="review_bundle_registry_invalid",
        )
        if entry_recipient != recipient_id:
            _fail(
                "review bundle recipient-registry entry has another recipient",
                code="review_bundle_registry_invalid",
                field_path=f"{field_path}.recipient_id",
                consumer_effect="cross-recipient registry state is rejected",
            )
        for identity_field in ("manifest_sha256", "semantic_identity_sha256"):
            _registry_sha256(
                entry[identity_field],
                field_path=f"{field_path}.{identity_field}",
                code="review_bundle_registry_invalid",
            )
        _registry_stable_id(
            entry["transport_authority_id"],
            field_path=f"{field_path}.transport_authority_id",
            code="review_bundle_registry_invalid",
        )
        if entry["transport_mode"] not in TRANSPORT_MODES:
            _fail(
                "review bundle recipient-registry transport mode is invalid",
                code="review_bundle_registry_invalid",
                field_path=f"{field_path}.transport_mode",
                consumer_effect="unknown transport state is rejected",
            )
        if entry["artifact_status"] not in ARTIFACT_STATUSES:
            _fail(
                "review bundle recipient-registry artifact status is invalid",
                code="review_bundle_registry_invalid",
                field_path=f"{field_path}.artifact_status",
                consumer_effect="unknown artifact disposition is rejected",
            )
        terminal_id = entry["named_terminal_id"]
        if terminal_id is not None:
            _registry_stable_id(
                terminal_id,
                field_path=f"{field_path}.named_terminal_id",
                code="review_bundle_registry_invalid",
            )
        if entry["named_terminal_transport"] not in {
            "not_requested",
            "completed",
        }:
            _fail(
                "review bundle named-terminal state is invalid",
                code="review_bundle_registry_invalid",
                field_path=f"{field_path}.named_terminal_transport",
                consumer_effect="unproven named delivery is rejected",
            )
        required_states = {
            "machine_open": "unverified",
            "human_open": "unverified",
            "content_decision": "none",
            "delivery_complete": False,
        }
        for state_field, expected in required_states.items():
            if entry[state_field] != expected:
                _fail(
                    "recipient ingest cannot infer later acceptance state",
                    code="review_bundle_registry_invalid",
                    field_path=f"{field_path}.{state_field}",
                    consumer_effect="transport remains separate from acceptance",
                )
        key = _review_bundle_registry_key(
            bundle_id=bundle_id,
            bundle_version=bundle_version,
            archive_sha256=archive_sha256,
            recipient_id=entry_recipient,
        )
        if entry["registry_key_sha256"] != _review_bundle_registry_key_sha256(key):
            _fail(
                "review bundle recipient-registry key identity is invalid",
                code="review_bundle_registry_invalid",
                field_path=f"{field_path}.registry_key_sha256",
                consumer_effect="mis-keyed recipient state is rejected",
            )
        if key in seen_keys:
            _fail(
                "review bundle recipient-registry contains a duplicate key",
                code="review_bundle_registry_invalid",
                field_path=field_path,
                consumer_effect="duplicate recipient state is rejected",
            )
        seen_keys.add(key)
        version_key = bundle_id, bundle_version, entry_recipient
        previous_hash = seen_versions.get(version_key)
        if previous_hash is not None and previous_hash != archive_sha256:
            _fail(
                "review bundle recipient-registry contains a version conflict",
                code="review_bundle_registry_invalid",
                field_path=field_path,
                consumer_effect="one version cannot identify multiple archive bytes",
            )
        seen_versions[version_key] = archive_sha256
        entries.append(dict(entry))
    return {
        "schema": REGISTRY_SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "recipient_id": recipient_id,
        "entries": entries,
    }


def validate_review_bundle_ingest_authority(value: Any) -> dict[str, Any]:
    authority = _registry_object(
        value,
        fields={
            "schema",
            "schema_version",
            "authority_id",
            "recipient_id",
            "artifact",
            "transport",
        },
        field_path="$",
        code="review_bundle_ingest_authority_invalid",
    )
    if (
        authority["schema"] != INGEST_AUTHORITY_SCHEMA
        or authority["schema_version"] != SCHEMA_VERSION
    ):
        _fail(
            "review bundle ingest authority schema is unsupported",
            code="review_bundle_ingest_authority_invalid",
            field_path="$.schema",
            consumer_effect="unknown transport authority is rejected",
        )
    authority_id = _registry_stable_id(
        authority["authority_id"],
        field_path="$.authority_id",
        code="review_bundle_ingest_authority_invalid",
    )
    recipient_id = _registry_stable_id(
        authority["recipient_id"],
        field_path="$.recipient_id",
        code="review_bundle_ingest_authority_invalid",
    )
    artifact = _registry_object(
        authority["artifact"],
        fields={"bundle_id", "bundle_version", "archive_sha256", "status"},
        field_path="$.artifact",
        code="review_bundle_ingest_authority_invalid",
    )
    normalized_artifact = {
        "bundle_id": _registry_stable_id(
            artifact["bundle_id"],
            field_path="$.artifact.bundle_id",
            code="review_bundle_ingest_authority_invalid",
        ),
        "bundle_version": _registry_bundle_version(
            artifact["bundle_version"],
            field_path="$.artifact.bundle_version",
            code="review_bundle_ingest_authority_invalid",
        ),
        "archive_sha256": _registry_sha256(
            artifact["archive_sha256"],
            field_path="$.artifact.archive_sha256",
            code="review_bundle_ingest_authority_invalid",
        ),
        "status": artifact["status"],
    }
    if normalized_artifact["status"] not in ARTIFACT_STATUSES:
        _fail(
            "review bundle artifact disposition is invalid",
            code="review_bundle_ingest_authority_invalid",
            field_path="$.artifact.status",
            consumer_effect="unknown artifact disposition is rejected",
        )
    transport = _registry_object(
        authority["transport"],
        fields={"mode", "named_terminal_id", "named_terminal_available"},
        field_path="$.transport",
        code="review_bundle_ingest_authority_invalid",
    )
    mode = transport["mode"]
    if mode not in TRANSPORT_MODES:
        _fail(
            "review bundle transport mode is invalid",
            code="review_bundle_ingest_authority_invalid",
            field_path="$.transport.mode",
            consumer_effect="unknown transport route is rejected",
        )
    named_terminal_id = transport["named_terminal_id"]
    if named_terminal_id is not None:
        named_terminal_id = _registry_stable_id(
            named_terminal_id,
            field_path="$.transport.named_terminal_id",
            code="review_bundle_ingest_authority_invalid",
        )
    named_terminal_available = transport["named_terminal_available"]
    if not isinstance(named_terminal_available, bool):
        _fail(
            "named-terminal availability must be boolean",
            code="review_bundle_ingest_authority_invalid",
            field_path="$.transport.named_terminal_available",
            consumer_effect="unproven terminal availability is rejected",
        )
    if mode == "local_ingest" and (
        named_terminal_id is not None or named_terminal_available
    ):
        _fail(
            "local ingest cannot claim a named terminal",
            code="review_bundle_ingest_authority_invalid",
            field_path="$.transport",
            consumer_effect="local ingest remains separate from named delivery",
        )
    if mode == "named_terminal_delivery" and named_terminal_id is None:
        _fail(
            "named-terminal delivery requires an exact terminal identity",
            code="review_bundle_ingest_authority_invalid",
            field_path="$.transport.named_terminal_id",
            consumer_effect="unnamed delivery is rejected",
        )
    return {
        "schema": INGEST_AUTHORITY_SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "authority_id": authority_id,
        "recipient_id": recipient_id,
        "artifact": normalized_artifact,
        "transport": {
            "mode": mode,
            "named_terminal_id": named_terminal_id,
            "named_terminal_available": named_terminal_available,
        },
    }


def _load_review_bundle_registry(
    registry_path: Path,
    *,
    recipient_id: str,
) -> dict[str, Any]:
    if not registry_path.exists():
        return empty_review_bundle_registry(recipient_id=recipient_id)
    if registry_path.is_symlink() or not registry_path.is_file():
        _fail(
            "review bundle recipient-registry is not a regular local file",
            code="review_bundle_registry_invalid",
            field_path="$.registry",
            consumer_effect="unsafe recipient state is rejected",
        )
    try:
        value = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PortableReviewBundleError(
            "review bundle recipient-registry cannot be read",
            code="review_bundle_registry_invalid",
            field_path="$.registry",
            consumer_effect="unreadable recipient state is rejected",
        ) from exc
    return validate_review_bundle_registry(
        value,
        expected_recipient_id=recipient_id,
    )


def _write_review_bundle_registry(
    registry_path: Path,
    registry: Mapping[str, Any],
) -> None:
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=f".{registry_path.name}.",
            suffix=".tmp",
            dir=registry_path.parent,
            delete=False,
        ) as temporary:
            temporary.write(canonical_json_bytes(registry))
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, registry_path)
        temporary_path = None
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def ingest_portable_review_bundle(
    *,
    archive_path: str | Path,
    registry_path: str | Path,
    destination_root: str | Path,
    authority: Mapping[str, Any],
    expected_recipient_id: str,
    available_named_terminal_id: str | None = None,
) -> dict[str, Any]:
    validated_authority = validate_review_bundle_ingest_authority(authority)
    recipient_id = validated_authority["recipient_id"]
    if recipient_id != expected_recipient_id:
        _fail(
            "review bundle ingest authority is bound to another recipient",
            code="recipient_identity_mismatch",
            field_path="$.authority.recipient_id",
            consumer_effect="one recipient cannot ingest another recipient's bundle",
        )
    artifact = validated_authority["artifact"]
    if artifact["status"] in {"revoked", "superseded"}:
        _fail(
            f"review bundle artifact is {artifact['status']}",
            code=f"review_bundle_artifact_{artifact['status']}",
            field_path="$.authority.artifact.status",
            consumer_effect="inactive artifact bytes are not transported or registered",
        )
    source = Path(archive_path)
    if source.is_symlink() or not source.is_file():
        _fail(
            "authorized local review bundle archive is unavailable",
            code="review_bundle_archive_missing",
            field_path="$.archive",
            consumer_effect="absence triggers no network or regeneration fallback",
        )
    source = source.resolve()
    if sha256_file(source) != artifact["archive_sha256"]:
        _fail(
            "local review bundle archive does not match ingest authority",
            code="review_bundle_archive_identity_mismatch",
            field_path="$.authority.artifact.archive_sha256",
            consumer_effect="unauthorized archive bytes are rejected",
        )
    validation = validate_portable_review_bundle(
        bundle_path=source,
        check_machine_open=False,
    )
    for field in ("bundle_id", "bundle_version", "archive_sha256"):
        if validation[field] != artifact[field]:
            _fail(
                "validated review bundle identity does not match ingest authority",
                code="review_bundle_archive_identity_mismatch",
                field_path=f"$.authority.artifact.{field}",
                consumer_effect="misbound archive bytes are rejected",
            )

    registry_file = Path(registry_path)
    if registry_file.is_symlink():
        _fail(
            "review bundle recipient-registry path cannot be a symlink",
            code="review_bundle_registry_invalid",
            field_path="$.registry",
            consumer_effect="unsafe recipient state is rejected",
        )
    registry_file = registry_file.resolve()
    registry = _load_review_bundle_registry(
        registry_file,
        recipient_id=recipient_id,
    )
    key = _review_bundle_registry_key(
        bundle_id=artifact["bundle_id"],
        bundle_version=artifact["bundle_version"],
        archive_sha256=artifact["archive_sha256"],
        recipient_id=recipient_id,
    )
    for index, entry in enumerate(registry["entries"]):
        existing_key = _review_bundle_registry_key(
            bundle_id=entry["bundle_id"],
            bundle_version=entry["bundle_version"],
            archive_sha256=entry["archive_sha256"],
            recipient_id=entry["recipient_id"],
        )
        if existing_key == key:
            if entry["artifact_status"] in {"revoked", "superseded"}:
                _fail(
                    f"review bundle registry marks artifact {entry['artifact_status']}",
                    code=f"review_bundle_artifact_{entry['artifact_status']}",
                    field_path=f"$.registry.entries[{index}].artifact_status",
                    consumer_effect="inactive artifact bytes are not transported again",
                )
            _fail(
                "review bundle recipient-registry already contains this ingest key",
                code="review_bundle_registry_duplicate",
                field_path=f"$.registry.entries[{index}]",
                consumer_effect="duplicate ingest is rejected before transport",
            )
        if (
            entry["bundle_id"] == artifact["bundle_id"]
            and entry["bundle_version"] == artifact["bundle_version"]
            and entry["recipient_id"] == recipient_id
            and entry["archive_sha256"] != artifact["archive_sha256"]
        ):
            _fail(
                "review bundle version is bound to different archive bytes",
                code="review_bundle_registry_version_conflict",
                field_path=f"$.registry.entries[{index}]",
                consumer_effect="one bundle version cannot identify multiple archives",
            )

    transport = validated_authority["transport"]
    named_terminal_state = "not_requested"
    if transport["mode"] == "named_terminal_delivery":
        if (
            not transport["named_terminal_available"]
            or available_named_terminal_id != transport["named_terminal_id"]
        ):
            _fail(
                "authorized named terminal is not currently available",
                code="review_bundle_named_terminal_unavailable",
                field_path="$.authority.transport.named_terminal_id",
                consumer_effect="named delivery requires exact live-terminal evidence",
            )
        named_terminal_state = "completed"

    transported = transport_portable_review_bundle(
        archive_path=source,
        destination_root=destination_root,
        recipient_id=recipient_id,
        expected_recipient_id=expected_recipient_id,
    )
    entry = {
        "registry_key_sha256": _review_bundle_registry_key_sha256(key),
        "bundle_id": artifact["bundle_id"],
        "bundle_version": artifact["bundle_version"],
        "archive_sha256": artifact["archive_sha256"],
        "recipient_id": recipient_id,
        "manifest_sha256": validation["manifest_sha256"],
        "semantic_identity_sha256": validation["semantic_identity_sha256"],
        "transport_authority_id": validated_authority["authority_id"],
        "transport_mode": transport["mode"],
        "artifact_status": "active",
        "named_terminal_id": transport["named_terminal_id"],
        "named_terminal_transport": named_terminal_state,
        "machine_open": "unverified",
        "human_open": "unverified",
        "content_decision": "none",
        "delivery_complete": False,
    }
    registry["entries"].append(entry)
    registry["entries"].sort(
        key=lambda item: (
            item["bundle_id"],
            item["bundle_version"],
            item["archive_sha256"],
            item["recipient_id"],
        )
    )
    registry = validate_review_bundle_registry(
        registry,
        expected_recipient_id=recipient_id,
    )
    _write_review_bundle_registry(registry_file, registry)
    return {
        "schema": INGEST_RESULT_SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "status": "succeeded",
        "registry_key_sha256": entry["registry_key_sha256"],
        "bundle_id": entry["bundle_id"],
        "bundle_version": entry["bundle_version"],
        "archive_sha256": entry["archive_sha256"],
        "recipient_id": recipient_id,
        "transport_authority_id": entry["transport_authority_id"],
        "transport_mode": entry["transport_mode"],
        "named_terminal_id": entry["named_terminal_id"],
        "named_terminal_transport": entry["named_terminal_transport"],
        "copied_archive_sha256": transported["copied_archive_sha256"],
        "extracted_semantic_identity_sha256": transported[
            "extracted_semantic_identity_sha256"
        ],
        "extracted_file_count": transported["extracted_file_count"],
        "states": {
            "registry": "recorded",
            "transport": "completed",
            "machine_open": "unverified",
            "human_open": "unverified",
            "content_decision": "none",
            "delivery_complete": False,
        },
        "boundaries": {
            "overwrite_count": 0,
            "private_path_registry_field_count": 0,
            "network_request_count": 0,
            "regeneration_count": 0,
            "external_transfer_count": 0,
        },
    }

__all__ = [
    "BUNDLE_SCHEMA",
    "DESCRIPTOR_SCHEMA",
    "PortableReviewBundleError",
    "RECIPIENT_OPEN_SCHEMA",
    "REGISTRY_SCHEMA",
    "INGEST_AUTHORITY_SCHEMA",
    "INGEST_RESULT_SCHEMA",
    "build_portable_review_bundle",
    "empty_review_bundle_registry",
    "ingest_portable_review_bundle",
    "canonical_json_bytes",
    "inspect_source_packet",
    "sha256_bytes",
    "sha256_file",
    "transport_portable_review_bundle",
    "validate_portable_review_bundle",
    "validate_review_bundle_ingest_authority",
    "validate_review_bundle_registry",
    "validate_recipient_open_receipt",
]
