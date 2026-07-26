"""Build one immutable cue-level review derivative from rendered evidence."""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

from src.pipeline.factory_queue import (
    canonical_json_bytes,
    sha256_file,
    sha256_json,
)


PACKET_SCHEMA = "nlmytgen.cue_review_packet.v1"
PACKET_SCHEMA_VERSION = "1.0"
def _packet_filenames(cue_id: str) -> tuple[str, ...]:
    return (
        f"{cue_id}_review_excerpt.mp4",
        f"{cue_id}_render_frame.png",
        f"{cue_id}_materialized_source_view.png",
        "README_REVIEW.md",
        "packet_manifest.json",
    )
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_PRIVATE_PATH = re.compile(r"(?:[A-Za-z]:[\\/]|\\\\|/Users/|/home/)")


class CueReviewPacketError(RuntimeError):
    """Fail-closed packet source, output, or tool boundary."""

    def __init__(self, message: str, *, code: str, field_path: str) -> None:
        super().__init__(message)
        self.code = code
        self.field_path = field_path


def _fail(message: str, *, code: str, field_path: str) -> None:
    raise CueReviewPacketError(message, code=code, field_path=field_path)


def _mapping(value: Any, *, field_path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail(
            "derived artifact contract section must be an object",
            code="derived_artifact_contract_invalid",
            field_path=field_path,
        )
    return value


def _sha(value: Any, *, field_path: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        _fail(
            "derived artifact identity must be a lowercase SHA-256",
            code="derived_artifact_identity_invalid",
            field_path=field_path,
        )
    return value


def _repo_path(
    repo_root: Path,
    locator: Any,
    *,
    field_path: str,
    require_file: bool,
) -> tuple[str, Path]:
    if not isinstance(locator, str) or not locator:
        _fail(
            "derived artifact locator must be a non-empty string",
            code="derived_artifact_locator_invalid",
            field_path=field_path,
        )
    pure = PurePosixPath(locator)
    if (
        pure.is_absolute()
        or "\\" in locator
        or ":" in locator
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        _fail(
            "derived artifact locator must be safe and repo-relative",
            code="derived_artifact_locator_unsafe",
            field_path=field_path,
        )
    root = repo_root.resolve()
    resolved = (root / Path(*pure.parts)).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        _fail(
            "derived artifact locator escapes the repository",
            code="derived_artifact_locator_unsafe",
            field_path=field_path,
        )
    if require_file and not resolved.is_file():
        _fail(
            "required rendered source artifact is unavailable",
            code="derived_artifact_source_unavailable",
            field_path=field_path,
        )
    return pure.as_posix(), resolved


def _bound_file(
    repo_root: Path,
    value: Any,
    *,
    field_path: str,
    allow_unavailable: bool,
) -> dict[str, Any]:
    bound = _mapping(value, field_path=field_path)
    if set(bound) != {"path", "sha256"}:
        _fail(
            "derived artifact bound file fields are not exact",
            code="derived_artifact_contract_invalid",
            field_path=field_path,
        )
    locator, resolved = _repo_path(
        repo_root,
        bound["path"],
        field_path=f"{field_path}.path",
        require_file=False,
    )
    expected = _sha(bound["sha256"], field_path=f"{field_path}.sha256")
    available = resolved.is_file()
    if not available and not allow_unavailable:
        _fail(
            "required rendered source artifact is unavailable",
            code="derived_artifact_source_unavailable",
            field_path=f"{field_path}.path",
        )
    if available and sha256_file(resolved) != expected:
        _fail(
            "rendered source artifact identity changed",
            code="derived_artifact_source_hash_mismatch",
            field_path=f"{field_path}.sha256",
        )
    return {
        "path": locator,
        "resolved_path": resolved,
        "sha256": expected,
        "available": available,
    }


def _load_json(path: Path, *, field_path: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CueReviewPacketError(
            "derived artifact JSON evidence is unreadable",
            code="derived_artifact_json_invalid",
            field_path=field_path,
        ) from exc


def _unique(
    rows: list[Mapping[str, Any]],
    *,
    code: str,
    field_path: str,
) -> Mapping[str, Any]:
    if len(rows) != 1:
        _fail(
            "cue binding must resolve to exactly one evidence row",
            code=code,
            field_path=field_path,
        )
    return rows[0]


def _walk_mappings(value: Any) -> list[Mapping[str, Any]]:
    rows: list[Mapping[str, Any]] = []
    if isinstance(value, Mapping):
        rows.append(value)
        for child in value.values():
            rows.extend(_walk_mappings(child))
    elif isinstance(value, list):
        for child in value:
            rows.extend(_walk_mappings(child))
    return rows


def _exact(value: Any, expected: Any, *, code: str, field_path: str) -> None:
    if value != expected:
        _fail(
            "cue review packet binding disagrees with canonical evidence",
            code=code,
            field_path=field_path,
        )


def _sanitize_payload(value: Any, *, field_path: str) -> None:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if _PRIVATE_PATH.search(encoded):
        _fail(
            "packet manifest contains a private or absolute path",
            code="packet_manifest_private_path",
            field_path=field_path,
        )


def inspect_cue_review_packet(
    *,
    repo_root: Path,
    package_id: str,
    descriptor_path: str,
    descriptor_sha256: str,
    authority_id: str,
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate all immutable cue bindings without writing packet outputs."""

    root = repo_root.resolve()
    derived = _mapping(contract, field_path="$.derived_artifact")
    required_fields = {
        "packet_id",
        "cue_id",
        "canonical_text_sha256",
        "canonical_script",
        "generated_project",
        "source_mp4",
        "cue_visual_readback",
        "run_receipt",
        "materialized_source",
        "output_root",
        "expected",
    }
    if set(derived) != required_fields:
        _fail(
            "derived artifact fields are not exact",
            code="derived_artifact_contract_invalid",
            field_path="$.derived_artifact",
        )
    descriptor_locator, descriptor_file = _repo_path(
        root,
        descriptor_path,
        field_path="$.descriptor_path",
        require_file=True,
    )
    _exact(
        sha256_file(descriptor_file),
        _sha(descriptor_sha256, field_path="$.descriptor_sha256"),
        code="derived_artifact_descriptor_hash_mismatch",
        field_path="$.descriptor_sha256",
    )
    descriptor = _mapping(
        _load_json(descriptor_file, field_path="$.descriptor_path"),
        field_path="$.descriptor",
    )
    _exact(
        descriptor.get("package", {}).get("package_id"),
        package_id,
        code="derived_artifact_wrong_package",
        field_path="$.descriptor.package.package_id",
    )
    _exact(
        descriptor.get("lifecycle", {}).get("state"),
        "rendered",
        code="derived_artifact_lifecycle_invalid",
        field_path="$.descriptor.lifecycle.state",
    )

    packet_id = derived["packet_id"]
    cue_id = derived["cue_id"]
    if not isinstance(packet_id, str) or not packet_id:
        _fail(
            "packet ID is invalid",
            code="derived_artifact_contract_invalid",
            field_path="$.derived_artifact.packet_id",
        )
    if not isinstance(cue_id, str) or not cue_id:
        _fail(
            "cue ID is invalid",
            code="derived_artifact_wrong_cue",
            field_path="$.derived_artifact.cue_id",
        )
    expected = _mapping(
        derived["expected"],
        field_path="$.derived_artifact.expected",
    )
    expected_fields = {
        "scene_id",
        "start_frame",
        "end_frame",
        "fps",
        "materialized_visual_id",
        "source_id",
        "source_sha256",
        "crop",
        "fit_mode",
    }
    if set(expected) != expected_fields:
        _fail(
            "derived artifact expected cue fields are not exact",
            code="derived_artifact_contract_invalid",
            field_path="$.derived_artifact.expected",
        )
    start_frame = expected["start_frame"]
    end_frame = expected["end_frame"]
    fps = expected["fps"]
    if (
        isinstance(start_frame, bool)
        or isinstance(end_frame, bool)
        or isinstance(fps, bool)
        or not all(isinstance(value, int) for value in (start_frame, end_frame, fps))
        or start_frame < 0
        or end_frame <= start_frame
        or fps <= 0
    ):
        _fail(
            "cue frame interval is invalid",
            code="derived_artifact_frame_interval_mismatch",
            field_path="$.derived_artifact.expected",
        )

    canonical = _bound_file(
        root,
        derived["canonical_script"],
        field_path="$.derived_artifact.canonical_script",
        allow_unavailable=False,
    )
    canonical_payload = _mapping(
        _load_json(
            canonical["resolved_path"],
            field_path="$.derived_artifact.canonical_script",
        ),
        field_path="$.canonical_script",
    )
    canonical_rows = [
        row
        for row in canonical_payload.get("cues", [])
        if isinstance(row, Mapping) and row.get("cue_id") == cue_id
    ]
    canonical_cue = _unique(
        canonical_rows,
        code="derived_artifact_cue_not_unique",
        field_path="$.canonical_script.cues",
    )
    canonical_text = canonical_cue.get("text")
    if not isinstance(canonical_text, str):
        _fail(
            "canonical cue text is unavailable",
            code="derived_artifact_text_mismatch",
            field_path="$.canonical_script.cues.text",
        )
    canonical_text_sha256 = sha256_json({"text": canonical_text})
    _exact(
        canonical_text_sha256,
        _sha(
            derived["canonical_text_sha256"],
            field_path="$.derived_artifact.canonical_text_sha256",
        ),
        code="derived_artifact_text_mismatch",
        field_path="$.derived_artifact.canonical_text_sha256",
    )
    _exact(
        canonical_cue.get("scene_id"),
        expected["scene_id"],
        code="derived_artifact_scene_mismatch",
        field_path="$.canonical_script.cues.scene_id",
    )

    local_roles = (
        "generated_project",
        "source_mp4",
        "cue_visual_readback",
        "run_receipt",
        "materialized_source",
    )
    sources = {
        role: _bound_file(
            root,
            derived[role],
            field_path=f"$.derived_artifact.{role}",
            allow_unavailable=True,
        )
        for role in local_roles
    }
    unavailable = sorted(
        role for role, source in sources.items() if not source["available"]
    )
    output_locator, output_path = _repo_path(
        root,
        derived["output_root"],
        field_path="$.derived_artifact.output_root",
        require_file=False,
    )
    if unavailable:
        return {
            "status": "source_artifact_unavailable",
            "package_id": package_id,
            "cue_id": cue_id,
            "descriptor": {
                "path": descriptor_locator,
                "sha256": descriptor_sha256,
            },
            "canonical_text_sha256": canonical_text_sha256,
            "output_root": output_locator,
            "unavailable_roles": unavailable,
            "source_local_availability": False,
        }

    generated_project = _mapping(
        _load_json(
            sources["generated_project"]["resolved_path"],
            field_path="$.derived_artifact.generated_project",
        ),
        field_path="$.generated_project",
    )
    project_rows = _walk_mappings(generated_project)
    voice = _unique(
        [
            row
            for row in project_rows
            if "VoiceItem" in str(row.get("$type", ""))
            and row.get("Serif") == canonical_text
        ],
        code="derived_artifact_voice_item_not_unique",
        field_path="$.generated_project",
    )
    _exact(
        voice.get("Frame"),
        start_frame,
        code="derived_artifact_frame_interval_mismatch",
        field_path="$.generated_project.VoiceItem.Frame",
    )
    _exact(
        voice.get("Length"),
        end_frame - start_frame,
        code="derived_artifact_frame_interval_mismatch",
        field_path="$.generated_project.VoiceItem.Length",
    )
    image = _unique(
        [
            row
            for row in project_rows
            if "ImageItem" in str(row.get("$type", ""))
            and row.get("Remark") == f"internal-review-real-media:{cue_id}"
        ],
        code="derived_artifact_image_item_not_unique",
        field_path="$.generated_project",
    )
    _exact(
        image.get("Frame"),
        start_frame,
        code="derived_artifact_frame_interval_mismatch",
        field_path="$.generated_project.ImageItem.Frame",
    )
    _exact(
        image.get("Length"),
        end_frame - start_frame,
        code="derived_artifact_neighboring_cue_inclusion",
        field_path="$.generated_project.ImageItem.Length",
    )
    image_path = image.get("FilePath")
    if not isinstance(image_path, str):
        _fail(
            "generated project image locator is unavailable",
            code="derived_artifact_source_mismatch",
            field_path="$.generated_project.ImageItem.FilePath",
        )
    try:
        image_resolved = Path(image_path).resolve()
    except OSError:
        image_resolved = Path()
    _exact(
        image_resolved,
        sources["materialized_source"]["resolved_path"],
        code="derived_artifact_source_mismatch",
        field_path="$.generated_project.ImageItem.FilePath",
    )

    cue_readback = _mapping(
        _load_json(
            sources["cue_visual_readback"]["resolved_path"],
            field_path="$.derived_artifact.cue_visual_readback",
        ),
        field_path="$.cue_visual_readback",
    )
    cue_row = _unique(
        [
            row
            for row in cue_readback.get("rows", [])
            if isinstance(row, Mapping) and row.get("cue_id") == cue_id
        ],
        code="derived_artifact_cue_not_unique",
        field_path="$.cue_visual_readback.rows",
    )
    cue_comparisons = (
        ("scene_id", expected["scene_id"], "derived_artifact_scene_mismatch"),
        ("frame", start_frame, "derived_artifact_frame_interval_mismatch"),
        ("end_frame", end_frame, "derived_artifact_frame_interval_mismatch"),
        (
            "materialized_visual_id",
            expected["materialized_visual_id"],
            "derived_artifact_source_mismatch",
        ),
        (
            "source_provenance_id",
            expected["source_id"],
            "derived_artifact_provenance_mismatch",
        ),
        (
            "asset_sha256",
            sources["materialized_source"]["sha256"],
            "derived_artifact_source_mismatch",
        ),
    )
    for field, expected_value, code in cue_comparisons:
        _exact(
            cue_row.get(field),
            expected_value,
            code=code,
            field_path=f"$.cue_visual_readback.rows.{field}",
        )

    mappings = descriptor.get("media_provenance", {}).get("asset_mappings", [])
    provenance = _unique(
        [
            row
            for row in mappings
            if isinstance(row, Mapping) and row.get("cue_id") == cue_id
        ],
        code="derived_artifact_provenance_mismatch",
        field_path="$.descriptor.media_provenance.asset_mappings",
    )
    provenance_comparisons = (
        ("source_id", expected["source_id"]),
        ("sha256", expected["source_sha256"]),
        ("crop", expected["crop"]),
    )
    for field, expected_value in provenance_comparisons:
        _exact(
            provenance.get(field),
            expected_value,
            code="derived_artifact_provenance_mismatch",
            field_path=f"$.descriptor.media_provenance.asset_mappings.{field}",
        )

    run_receipt = _mapping(
        _load_json(
            sources["run_receipt"]["resolved_path"],
            field_path="$.derived_artifact.run_receipt",
        ),
        field_path="$.run_receipt",
    )
    materialization = run_receipt.get("visual_materialization", {})
    records = (
        materialization.get("records", [])
        if isinstance(materialization, Mapping)
        else []
    )
    materialized = _unique(
        [
            row
            for row in records
            if isinstance(row, Mapping) and row.get("cue_ids") == [cue_id]
        ],
        code="derived_artifact_source_mismatch",
        field_path="$.run_receipt.visual_materialization.records",
    )
    receipt_comparisons = (
        (
            "materialization_id",
            expected["materialized_visual_id"],
            "derived_artifact_source_mismatch",
        ),
        (
            "source_provenance_id",
            expected["source_id"],
            "derived_artifact_provenance_mismatch",
        ),
        (
            "source_sha256",
            expected["source_sha256"],
            "derived_artifact_provenance_mismatch",
        ),
        (
            "png_sha256",
            sources["materialized_source"]["sha256"],
            "derived_artifact_source_mismatch",
        ),
        ("crop", expected["crop"], "derived_artifact_crop_recomputation"),
        ("fit_mode", expected["fit_mode"], "derived_artifact_crop_recomputation"),
    )
    for field, expected_value, code in receipt_comparisons:
        _exact(
            materialized.get(field),
            expected_value,
            code=code,
            field_path=f"$.run_receipt.visual_materialization.records.{field}",
        )

    _exact(
        descriptor.get("generated_project", {}).get("sha256"),
        sources["generated_project"]["sha256"],
        code="derived_artifact_generated_project_hash_mismatch",
        field_path="$.descriptor.generated_project.sha256",
    )
    _exact(
        descriptor.get("render_validation", {}).get("mp4_sha256"),
        sources["source_mp4"]["sha256"],
        code="derived_artifact_source_mp4_hash_mismatch",
        field_path="$.descriptor.render_validation.mp4_sha256",
    )
    _exact(
        descriptor.get("shape", {}).get("fps"),
        fps,
        code="derived_artifact_frame_interval_mismatch",
        field_path="$.descriptor.shape.fps",
    )

    status = "ready"
    existing_manifest: dict[str, Any] | None = None
    if output_path.exists():
        existing_manifest = validate_cue_review_packet(
            repo_root=root,
            output_root=output_locator,
            expected={
                "packet_id": packet_id,
                "package_id": package_id,
                "descriptor_sha256": descriptor_sha256,
                "generated_project_sha256": sources["generated_project"]["sha256"],
                "source_mp4_sha256": sources["source_mp4"]["sha256"],
                "cue_id": cue_id,
                "canonical_text_sha256": canonical_text_sha256,
                "authority_id": authority_id,
            },
        )
        status = "valid_existing"

    return {
        "status": status,
        "packet_id": packet_id,
        "package_id": package_id,
        "cue_id": cue_id,
        "canonical_text": canonical_text,
        "canonical_text_sha256": canonical_text_sha256,
        "scene_id": expected["scene_id"],
        "start_frame": start_frame,
        "end_frame": end_frame,
        "length_frames": end_frame - start_frame,
        "fps": fps,
        "start_seconds": start_frame / fps,
        "end_seconds": end_frame / fps,
        "descriptor": {
            "path": descriptor_locator,
            "sha256": descriptor_sha256,
        },
        "content_identity_sha256": descriptor["identities"][
            "content_identity_sha256"
        ],
        "source_project": copy.deepcopy(descriptor["source_project"]),
        "generated_project": {
            "path": sources["generated_project"]["path"],
            "sha256": sources["generated_project"]["sha256"],
        },
        "source_mp4": {
            "path": sources["source_mp4"]["path"],
            "sha256": sources["source_mp4"]["sha256"],
        },
        "canonical_script": {
            "path": canonical["path"],
            "sha256": canonical["sha256"],
        },
        "cue_visual_readback": {
            "path": sources["cue_visual_readback"]["path"],
            "sha256": sources["cue_visual_readback"]["sha256"],
        },
        "run_receipt": {
            "path": sources["run_receipt"]["path"],
            "sha256": sources["run_receipt"]["sha256"],
        },
        "materialized_source": {
            "path": sources["materialized_source"]["path"],
            "sha256": sources["materialized_source"]["sha256"],
            "resolved_path": sources["materialized_source"]["resolved_path"],
            "materialized_visual_id": expected["materialized_visual_id"],
            "source_id": expected["source_id"],
            "source_sha256": expected["source_sha256"],
            "crop": copy.deepcopy(expected["crop"]),
            "fit_mode": expected["fit_mode"],
        },
        "output_root": output_locator,
        "resolved_output_root": output_path,
        "source_local_availability": True,
        "existing_manifest": existing_manifest,
    }


def _run(command: list[str], *, code: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise CueReviewPacketError(
            "cue review packet media operation failed",
            code=code,
            field_path="$.derived_artifact.outputs",
        ) from exc


def _ffprobe(path: Path) -> dict[str, Any]:
    completed = _run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            (
                "format=duration,size:"
                "stream=index,codec_name,codec_type,width,height,r_frame_rate,"
                "sample_rate,channels"
            ),
            "-of",
            "json",
            str(path),
        ],
        code="review_packet_ffprobe_failed",
    )
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise CueReviewPacketError(
            "ffprobe returned invalid JSON",
            code="review_packet_ffprobe_failed",
            field_path="$.derived_artifact.outputs",
        ) from exc


def _decode(path: Path, *, maps: tuple[str, ...] = ()) -> None:
    command = ["ffmpeg", "-v", "error", "-nostdin", "-i", str(path)]
    for stream in maps:
        command.extend(["-map", stream])
    command.extend(["-f", "null", os.devnull])
    _run(command, code="review_packet_decode_failed")


def _file_identity(path: Path, *, role: str, locator: str) -> dict[str, Any]:
    return {
        "role": role,
        "path": locator,
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def _readme(binding: Mapping[str, Any], *, authority_id: str) -> str:
    return (
        "# Cue Review Packet\n\n"
        "This packet is the starting artifact for human review of one exact cue.\n"
        "It is not creative acceptance, a production asset, rights approval, or "
        "publication authority.\n\n"
        f"- Package: `{binding['package_id']}`\n"
        f"- Cue: `{binding['cue_id']}`\n"
        f"- Scene: `{binding['scene_id']}`\n"
        f"- Frame interval: `[{binding['start_frame']}, "
        f"{binding['end_frame']})` at `{binding['fps']} fps\n"
        f"- Time interval: `[{binding['start_seconds']:.10f}, "
        f"{binding['end_seconds']:.10f})` seconds\n"
        f"- Materialized source: "
        f"`{binding['materialized_source']['materialized_visual_id']}`\n"
        f"- Source provenance: `{binding['materialized_source']['source_id']}`\n"
        f"- Technical authority: `{authority_id}`\n\n"
        "The excerpt has zero context handle and makes no conclusion about "
        "neighboring cues. The materialized source view is a byte-preserving "
        "copy of the exact image referenced by the generated project; this "
        "builder does not recompute crop or rerasterize a source page.\n"
    )


def generate_cue_review_packet(
    *,
    repo_root: Path,
    package_id: str,
    descriptor_path: str,
    descriptor_sha256: str,
    authority_id: str,
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Create one packet; the caller must consume one-shot authority first."""

    binding = inspect_cue_review_packet(
        repo_root=repo_root,
        package_id=package_id,
        descriptor_path=descriptor_path,
        descriptor_sha256=descriptor_sha256,
        authority_id=authority_id,
        contract=contract,
    )
    if binding["status"] == "source_artifact_unavailable":
        _fail(
            "required rendered source artifact is unavailable",
            code="derived_artifact_source_unavailable",
            field_path="$.derived_artifact",
        )
    if binding["status"] == "valid_existing":
        _fail(
            "derived artifact output already exists",
            code="derived_artifact_overwrite_forbidden",
            field_path="$.derived_artifact.output_root",
        )

    output_root: Path = binding["resolved_output_root"]
    if output_root.exists():
        _fail(
            "derived artifact output collides with existing evidence",
            code="derived_artifact_output_collision",
            field_path="$.derived_artifact.output_root",
        )
    output_root.mkdir(parents=True, exist_ok=False)
    cue_prefix = binding["cue_id"]
    excerpt = output_root / f"{cue_prefix}_review_excerpt.mp4"
    render_frame = output_root / f"{cue_prefix}_render_frame.png"
    source_view = output_root / f"{cue_prefix}_materialized_source_view.png"
    readme = output_root / "README_REVIEW.md"
    manifest_path = output_root / "packet_manifest.json"
    source_mp4 = (
        repo_root.resolve()
        / Path(*PurePosixPath(binding["source_mp4"]["path"]).parts)
    )
    start_seconds = binding["start_seconds"]
    end_seconds = binding["end_seconds"]
    frame_filter = (
        f"[0:v:0]trim=start_frame={binding['start_frame']}:"
        f"end_frame={binding['end_frame']},setpts=PTS-STARTPTS[v];"
        f"[0:a:0]atrim=start={start_seconds:.10f}:"
        f"end={end_seconds:.10f},asetpts=PTS-STARTPTS[a]"
    )
    _run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-nostdin",
            "-i",
            str(source_mp4),
            "-filter_complex",
            frame_filter,
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(binding["fps"]),
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-map_metadata",
            "-1",
            "-movflags",
            "+faststart",
            str(excerpt),
        ],
        code="review_packet_excerpt_failed",
    )
    _run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-nostdin",
            "-i",
            str(source_mp4),
            "-vf",
            f"select=eq(n\\,{binding['start_frame']})",
            "-frames:v",
            "1",
            "-fps_mode",
            "vfr",
            str(render_frame),
        ],
        code="review_packet_frame_failed",
    )
    shutil.copyfile(binding["materialized_source"]["resolved_path"], source_view)
    readme.write_text(
        _readme(binding, authority_id=authority_id),
        encoding="utf-8",
        newline="\n",
    )

    _decode(excerpt, maps=("0:v:0", "0:a:0"))
    _decode(render_frame, maps=("0:v:0",))
    _decode(source_view, maps=("0:v:0",))
    excerpt_probe = _ffprobe(excerpt)
    video_streams = [
        row
        for row in excerpt_probe.get("streams", [])
        if row.get("codec_type") == "video"
    ]
    audio_streams = [
        row
        for row in excerpt_probe.get("streams", [])
        if row.get("codec_type") == "audio"
    ]
    if len(video_streams) != 1 or len(audio_streams) != 1:
        _fail(
            "review excerpt stream shape is invalid",
            code="review_packet_decode_failed",
            field_path="$.outputs.review_excerpt",
        )
    video = video_streams[0]
    audio = audio_streams[0]
    expected_rate = f"{binding['fps']}/1"
    for actual, expected, field in (
        (video.get("codec_name"), "h264", "video_codec"),
        (audio.get("codec_name"), "aac", "audio_codec"),
        (video.get("width"), 1920, "width"),
        (video.get("height"), 1080, "height"),
        (video.get("r_frame_rate"), expected_rate, "fps"),
    ):
        _exact(
            actual,
            expected,
            code="review_packet_media_contract_mismatch",
            field_path=f"$.outputs.review_excerpt.{field}",
        )

    output_locator = binding["output_root"]
    outputs = [
        _file_identity(
            excerpt,
            role="review_excerpt",
            locator=f"{output_locator}/{excerpt.name}",
        ),
        _file_identity(
            render_frame,
            role="rendered_frame",
            locator=f"{output_locator}/{render_frame.name}",
        ),
        _file_identity(
            source_view,
            role="materialized_source_view",
            locator=f"{output_locator}/{source_view.name}",
        ),
        _file_identity(
            readme,
            role="review_readme",
            locator=f"{output_locator}/{readme.name}",
        ),
    ]
    manifest = {
        "schema": PACKET_SCHEMA,
        "schema_version": PACKET_SCHEMA_VERSION,
        "packet_id": binding["packet_id"],
        "package_id": binding["package_id"],
        "descriptor": binding["descriptor"],
        "content_identity_sha256": binding["content_identity_sha256"],
        "source_project": binding["source_project"],
        "generated_project": binding["generated_project"],
        "source_mp4": binding["source_mp4"],
        "cue": {
            "cue_id": binding["cue_id"],
            "scene_id": binding["scene_id"],
            "canonical_text_sha256": binding["canonical_text_sha256"],
            "start_frame": binding["start_frame"],
            "end_frame": binding["end_frame"],
            "length_frames": binding["length_frames"],
            "fps": binding["fps"],
            "start_seconds": round(binding["start_seconds"], 10),
            "end_seconds": round(binding["end_seconds"], 10),
            "context_handle_frames": 0,
        },
        "source_binding": {
            "canonical_script": binding["canonical_script"],
            "cue_visual_readback": binding["cue_visual_readback"],
            "run_receipt": binding["run_receipt"],
            "materialized_source": {
                key: copy.deepcopy(binding["materialized_source"][key])
                for key in (
                    "path",
                    "sha256",
                    "materialized_visual_id",
                    "source_id",
                    "source_sha256",
                    "crop",
                    "fit_mode",
                )
            },
            "crop_recomputed": False,
            "source_page_rerasterized": False,
        },
        "decode": {
            "excerpt_full_video": "passed",
            "excerpt_full_audio": "passed",
            "rendered_frame_png": "passed",
            "materialized_source_png": "passed",
            "video_codec": video["codec_name"],
            "audio_codec": audio["codec_name"],
            "width": video["width"],
            "height": video["height"],
            "source_fps": binding["fps"],
            "excerpt_fps": video["r_frame_rate"],
        },
        "technical_generation": {
            "effect_class": "derived_artifact",
            "operation": "review_packet_generation",
            "authority_id": authority_id,
            "one_shot_use_count": 1,
            "no_overwrite": True,
            "lifecycle_transition": False,
            "content_identity_changed": False,
            "generated_project_changed": False,
            "source_mp4_changed": False,
            "yymm4_launched": False,
            "render_driver_launched": False,
            "full_video_rendered": False,
            "playback_performed": False,
        },
        "states": {
            "technical_generation": True,
            "human_review_opened": False,
            "human_creative_acceptance": False,
            "rights_approved": False,
            "production_approved": False,
            "publication_approved": False,
            "upload_performed": False,
            "release_performed": False,
            "recipient_open_status": "unverified",
            "source_local_availability": True,
        },
        "outputs": outputs,
    }
    _sanitize_payload(manifest, field_path="$.packet_manifest")
    temporary = manifest_path.with_name(".packet_manifest.json.tmp")
    with temporary.open("xb") as handle:
        handle.write(canonical_json_bytes(manifest))
        handle.flush()
    temporary.replace(manifest_path)
    validated = validate_cue_review_packet(
        repo_root=repo_root,
        output_root=output_locator,
        expected={
            "packet_id": binding["packet_id"],
            "package_id": binding["package_id"],
            "descriptor_sha256": descriptor_sha256,
            "generated_project_sha256": binding["generated_project"]["sha256"],
            "source_mp4_sha256": binding["source_mp4"]["sha256"],
            "cue_id": binding["cue_id"],
            "canonical_text_sha256": binding["canonical_text_sha256"],
            "authority_id": authority_id,
        },
    )
    return {
        "schema": "nlmytgen.cue_review_packet_generation_result.v1",
        "status": "succeeded",
        "effect_performed": True,
        "effect_class": "derived_artifact",
        "operation": "review_packet_generation",
        "package_id": package_id,
        "cue_id": binding["cue_id"],
        "output_root": output_locator,
        "packet_manifest_sha256": validated["packet_manifest_sha256"],
        "outputs": copy.deepcopy(validated["outputs"]),
        "boundaries": {
            "yymm4_launch_count": 0,
            "render_driver_launch_count": 0,
            "ffmpeg_encode_count": 1,
            "playback_count": 0,
            "system_volume_operation_count": 0,
            "private_artifact_copy_count": 1,
            "product_write_count": 5,
            "human_or_rights_action_count": 0,
            "public_action_count": 0,
        },
    }


def validate_cue_review_packet(
    *,
    repo_root: Path,
    output_root: str,
    expected: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate a completed packet without writing or repairing it."""

    locator, root = _repo_path(
        repo_root,
        output_root,
        field_path="$.output_root",
        require_file=False,
    )
    if not root.is_dir():
        _fail(
            "review packet output root is unavailable",
            code="derived_artifact_source_unavailable",
            field_path="$.output_root",
        )
    expected_names = set(_packet_filenames(str(expected["cue_id"])))
    actual_names = {path.name for path in root.iterdir() if path.is_file()}
    if actual_names != expected_names:
        _fail(
            "review packet output collides with foreign or incomplete evidence",
            code="derived_artifact_output_collision",
            field_path="$.output_root",
        )
    manifest_path = root / "packet_manifest.json"
    manifest = _mapping(
        _load_json(manifest_path, field_path="$.packet_manifest"),
        field_path="$.packet_manifest",
    )
    _sanitize_payload(manifest, field_path="$.packet_manifest")
    comparisons = (
        (manifest.get("packet_id"), expected["packet_id"], "packet_id"),
        (manifest.get("package_id"), expected["package_id"], "package_id"),
        (
            manifest.get("descriptor", {}).get("sha256"),
            expected["descriptor_sha256"],
            "descriptor.sha256",
        ),
        (
            manifest.get("generated_project", {}).get("sha256"),
            expected["generated_project_sha256"],
            "generated_project.sha256",
        ),
        (
            manifest.get("source_mp4", {}).get("sha256"),
            expected["source_mp4_sha256"],
            "source_mp4.sha256",
        ),
        (manifest.get("cue", {}).get("cue_id"), expected["cue_id"], "cue.cue_id"),
        (
            manifest.get("cue", {}).get("canonical_text_sha256"),
            expected["canonical_text_sha256"],
            "cue.canonical_text_sha256",
        ),
        (
            manifest.get("technical_generation", {}).get("authority_id"),
            expected["authority_id"],
            "technical_generation.authority_id",
        ),
    )
    for actual, expected_value, field in comparisons:
        _exact(
            actual,
            expected_value,
            code="derived_artifact_existing_identity_mismatch",
            field_path=f"$.packet_manifest.{field}",
        )
    outputs = manifest.get("outputs")
    if not isinstance(outputs, list) or len(outputs) != 4:
        _fail(
            "packet output inventory is invalid",
            code="derived_artifact_output_collision",
            field_path="$.packet_manifest.outputs",
        )
    for index, output in enumerate(outputs):
        if not isinstance(output, Mapping):
            _fail(
                "packet output inventory is invalid",
                code="derived_artifact_output_collision",
                field_path=f"$.packet_manifest.outputs[{index}]",
            )
        path_locator, path = _repo_path(
            repo_root,
            output.get("path"),
            field_path=f"$.packet_manifest.outputs[{index}].path",
            require_file=True,
        )
        try:
            path.relative_to(root)
        except ValueError:
            _fail(
                "packet output inventory escapes its root",
                code="derived_artifact_locator_unsafe",
                field_path=f"$.packet_manifest.outputs[{index}].path",
            )
        _exact(
            path_locator.startswith(f"{locator}/"),
            True,
            code="derived_artifact_locator_unsafe",
            field_path=f"$.packet_manifest.outputs[{index}].path",
        )
        _exact(
            sha256_file(path),
            output.get("sha256"),
            code="derived_artifact_existing_identity_mismatch",
            field_path=f"$.packet_manifest.outputs[{index}].sha256",
        )
        _exact(
            path.stat().st_size,
            output.get("size_bytes"),
            code="derived_artifact_existing_identity_mismatch",
            field_path=f"$.packet_manifest.outputs[{index}].size_bytes",
        )
    return {
        "status": "passed",
        "output_root": locator,
        "packet_manifest_sha256": sha256_file(manifest_path),
        "packet_manifest_size_bytes": manifest_path.stat().st_size,
        "outputs": copy.deepcopy(outputs),
    }


__all__ = [
    "CueReviewPacketError",
    "generate_cue_review_packet",
    "inspect_cue_review_packet",
    "validate_cue_review_packet",
]
