"""Executable Factory Package v2 validation and v1 compatibility adapter.

The v2 descriptor is a tracked, deterministic description of an existing
episode package.  It binds v1 authorities by path and hash without rewriting
them, and keeps live/private artifact availability separate from contract
validity.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping


FACTORY_PACKAGE_SCHEMA = "nlmytgen.factory_package.v2"
FACTORY_PACKAGE_VERSION = "2.0"
VALIDATION_RESULT_SCHEMA = "nlmytgen.factory_package_validation.v2"
FIELD_INVENTORY_SCHEMA = "nlmytgen.factory_contract_field_inventory.v2"

SECTION_SCHEMAS = {
    "contract": "nlmytgen.factory_contract.v2",
    "package": "nlmytgen.factory_package.package_identity.v2",
    "source_intake": "nlmytgen.factory_package.source_intake.v2",
    "claim_support": "nlmytgen.factory_package.claim_support.v2",
    "canonical_content": "nlmytgen.factory_package.canonical_content.v2",
    "shape": "nlmytgen.factory_package.shape.v2",
    "media_provenance": "nlmytgen.factory_package.media_provenance.v2",
    "episode_execution": "nlmytgen.factory_package.episode_execution.v2",
    "source_project": "nlmytgen.factory_package.source_project.v2",
    "generated_project": "nlmytgen.factory_package.generated_project.v2",
    "render_validation": "nlmytgen.factory_package.render_validation.v2",
    "identities": "nlmytgen.factory_package.identities.v2",
    "resume_identity": "nlmytgen.factory_package.resume_identity.v2",
    "human_decision": "nlmytgen.factory_package.human_decision.v2",
    "authority": "nlmytgen.factory_package.authority.v2",
    "extensions": "nlmytgen.factory_package.extensions.v2",
}

SECTION_FIELDS = {
    "contract": {
        "schema",
        "schema_path",
        "schema_sha256",
        "field_inventory_path",
        "field_inventory_sha256",
    },
    "package": {
        "schema",
        "package_id",
        "episode_id",
        "title",
        "content_authority",
    },
    "source_intake": {
        "schema",
        "authority_path",
        "authority_sha256",
        "source_count",
        "source_backed",
    },
    "claim_support": {
        "schema",
        "authority_path",
        "authority_sha256",
        "factual_cue_ids",
        "nonfactual_cue_ids",
        "unsupported_factual_units",
    },
    "canonical_content": {
        "schema",
        "path",
        "sha256",
        "cue_sequence",
    },
    "shape": {
        "schema",
        "cue_count",
        "scene_count",
        "scene_mapping",
        "speaker_mapping",
        "speaker_counts",
        "timeline_frames",
        "fps",
        "duration_seconds",
        "asset_count",
        "source_count",
    },
    "media_provenance": {
        "schema",
        "path",
        "sha256",
        "asset_mappings",
    },
    "episode_execution": {
        "schema",
        "manifest_path",
        "manifest_sha256",
        "manifest_schema",
        "run_id",
        "project_filename",
        "mp4_filename",
        "render_settings_sha256",
    },
    "source_project": {
        "schema",
        "strategy",
        "path",
        "sha256",
        "identity_source",
        "live_required_for_contract",
    },
    "generated_project": {
        "schema",
        "path",
        "sha256",
        "identity_source",
        "availability_claim",
    },
    "render_validation": {
        "schema",
        "technical_receipt_path",
        "technical_receipt_sha256",
        "technical_status",
        "mp4_path",
        "mp4_sha256",
        "container",
        "video_codec",
        "audio_codec",
        "width",
        "height",
        "fps",
        "duration_seconds",
        "availability_claim",
    },
    "identities": {
        "schema",
        "protected_input_policy",
        "content_identity_policy",
        "content_identity_sha256",
        "content_identity_excludes",
    },
    "resume_identity": {
        "schema",
        "policy",
        "completed_run_observed",
        "semantic_drift_fail_closed",
    },
    "human_decision": {
        "schema",
        "state",
        "receipt_path",
        "receipt_sha256",
        "artifact_sha256",
    },
    "authority": {
        "schema",
        "rights",
        "production",
        "publication",
        "upload",
        "release",
    },
    "extensions": {"schema", "values"},
}

TOP_LEVEL_FIELDS = {
    "schema",
    "schema_version",
    *SECTION_SCHEMAS,
}

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")
EXTENSION_NAME_RE = re.compile(
    r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){2,}$"
)
FORBIDDEN_KEY_PARTS = {
    "credential",
    "credentials",
    "password",
    "token",
    "cookie",
    "account_identifier",
    "private_bytes",
    "payload_base64",
    "blob",
}
CONTENT_IDENTITY_FORBIDDEN_PARTS = {
    "timestamp",
    "started_at",
    "completed_at",
    "pid",
    "process_id",
    "machine_path",
    "absolute_path",
}


class FactoryContractError(ValueError):
    """A field-level, consumer-aware Factory Contract validation failure."""

    def __init__(
        self,
        message: str,
        *,
        code: str,
        section: str,
        field_path: str,
        consumer_effect: str,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.section = section
        self.field_path = field_path
        self.consumer_effect = consumer_effect

    def as_payload(self) -> dict[str, Any]:
        return {
            "schema": VALIDATION_RESULT_SCHEMA,
            "status": "failed",
            "error_code": self.code,
            "section": self.section,
            "field_path": self.field_path,
            "consumer_effect": self.consumer_effect,
            "message": str(self),
        }


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _fail(
    message: str,
    *,
    code: str,
    section: str,
    field_path: str,
    consumer_effect: str,
) -> None:
    raise FactoryContractError(
        message,
        code=code,
        section=section,
        field_path=field_path,
        consumer_effect=consumer_effect,
    )


def _load_json(path: Path, *, section: str, field_path: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail(
            f"JSON authority is unreadable: {path.name}",
            code="authority_unreadable",
            section=section,
            field_path=field_path,
            consumer_effect="contract normalization cannot establish an exact authority",
        )
        raise AssertionError("unreachable") from exc
    if not isinstance(value, dict):
        _fail(
            "JSON authority root must be an object",
            code="authority_root_invalid",
            section=section,
            field_path=field_path,
            consumer_effect="contract normalization cannot address authority fields",
        )
    return value


def _walk(value: Any, path: str = "$") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            yield child_path, str(key), child
            yield from _walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def _validate_safe_tracked_payload(payload: Mapping[str, Any]) -> None:
    for path, key, value in _walk(payload):
        key_lower = key.lower()
        if key_lower in FORBIDDEN_KEY_PARTS:
            _fail(
                f"forbidden secret/private field: {key}",
                code="tracked_private_field_forbidden",
                section=path.split(".", 2)[1] if "." in path else "root",
                field_path=path,
                consumer_effect="tracked contract could expose private or credential state",
            )
        if not isinstance(value, str):
            continue
        if (
            WINDOWS_ABSOLUTE_RE.match(value)
            or value.startswith("\\\\")
            or value.startswith("/")
            or value.startswith("file://")
        ):
            _fail(
                "private or absolute path is forbidden in a tracked descriptor",
                code="private_absolute_path_forbidden",
                section=path.split(".", 2)[1] if "." in path else "root",
                field_path=path,
                consumer_effect="descriptor would not be portable to a tracked-only checkout",
            )


def _validate_sha(value: Any, *, section: str, field_path: str) -> str:
    text = str(value).lower()
    if not SHA256_RE.fullmatch(text):
        _fail(
            "expected a lowercase SHA-256 identity",
            code="sha256_invalid",
            section=section,
            field_path=field_path,
            consumer_effect="artifact identity cannot be compared deterministically",
        )
    return text


def _resolve_repo_path(
    repo_root: Path,
    relative: Any,
    *,
    section: str,
    field_path: str,
) -> Path:
    text = str(relative)
    pure = PurePosixPath(text)
    if (
        not text
        or pure.is_absolute()
        or ".." in pure.parts
        or "\\" in text
        or WINDOWS_ABSOLUTE_RE.match(text)
    ):
        _fail(
            "path must be a normalized repository-relative POSIX path",
            code="repo_path_invalid",
            section=section,
            field_path=field_path,
            consumer_effect="authority resolution could escape or depend on one machine",
        )
    root = repo_root.resolve()
    resolved = (root / Path(*pure.parts)).resolve()
    if resolved != root and root not in resolved.parents:
        _fail(
            "path escaped the repository root",
            code="repo_path_escape",
            section=section,
            field_path=field_path,
            consumer_effect="authority resolution could read outside the repository",
        )
    return resolved


def _require_exact_fields(
    section_value: Any,
    *,
    section: str,
) -> dict[str, Any]:
    if not isinstance(section_value, dict):
        _fail(
            "section must be an object",
            code="section_type_invalid",
            section=section,
            field_path=f"$.{section}",
            consumer_effect="section cannot be normalized",
        )
    expected = SECTION_FIELDS[section]
    actual = set(section_value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing:
        _fail(
            f"required section fields are missing: {', '.join(missing)}",
            code="required_field_missing",
            section=section,
            field_path=f"$.{section}",
            consumer_effect="a contract consumer lacks required normalized state",
        )
    if unknown:
        _fail(
            f"unknown unversioned section fields: {', '.join(unknown)}",
            code="unknown_section_field",
            section=section,
            field_path=f"$.{section}",
            consumer_effect="a consumer could silently interpret an unversioned field",
        )
    expected_schema = SECTION_SCHEMAS[section]
    if section_value.get("schema") != expected_schema:
        _fail(
            f"section schema must be {expected_schema}",
            code="section_schema_invalid",
            section=section,
            field_path=f"$.{section}.schema",
            consumer_effect="section version cannot be selected deterministically",
        )
    return section_value


def _verify_bound_file(
    repo_root: Path,
    section_value: Mapping[str, Any],
    *,
    section: str,
    path_key: str,
    hash_key: str,
) -> Path:
    path = _resolve_repo_path(
        repo_root,
        section_value[path_key],
        section=section,
        field_path=f"$.{section}.{path_key}",
    )
    expected = _validate_sha(
        section_value[hash_key],
        section=section,
        field_path=f"$.{section}.{hash_key}",
    )
    if not path.is_file():
        _fail(
            f"bound tracked authority is missing: {section_value[path_key]}",
            code="bound_authority_missing",
            section=section,
            field_path=f"$.{section}.{path_key}",
            consumer_effect="v1 compatibility binding cannot be established",
        )
    actual = sha256_file(path)
    if actual != expected:
        _fail(
            f"bound authority hash mismatch: {section_value[path_key]}",
            code="bound_authority_hash_mismatch",
            section=section,
            field_path=f"$.{section}.{hash_key}",
            consumer_effect="existing v1 authority changed after descriptor creation",
        )
    return path


def _availability(
    repo_root: Path,
    *,
    section: str,
    path_value: Any,
    sha_value: Any,
    check_live: bool,
) -> dict[str, Any]:
    path = _resolve_repo_path(
        repo_root,
        path_value,
        section=section,
        field_path=f"$.{section}.path",
    )
    expected = _validate_sha(
        sha_value,
        section=section,
        field_path=f"$.{section}.sha256",
    )
    row = {
        "artifact_class": section,
        "locator": str(path_value),
        "expected_sha256": expected,
        "contract_required": False,
    }
    if not path.is_file():
        return {**row, "status": "receipt_only_no_live_file", "actual_sha256": None}
    if not check_live:
        return {**row, "status": "live_file_present_not_hashed", "actual_sha256": None}
    actual = sha256_file(path)
    if actual != expected:
        _fail(
            f"live artifact hash mismatch: {path_value}",
            code="live_artifact_hash_mismatch",
            section=section,
            field_path=f"$.{section}.sha256",
            consumer_effect="live execution cannot use an identity that differs from its receipt",
        )
    return {**row, "status": "live_file_hash_exact", "actual_sha256": actual}


def _validate_authority_clocks(authority: Mapping[str, Any]) -> None:
    for clock in ("rights", "production", "publication", "upload", "release"):
        value = authority[clock]
        if not isinstance(value, dict) or set(value) != {"approved", "record"}:
            _fail(
                "authority clock must declare only approved and record",
                code="authority_clock_invalid",
                section="authority",
                field_path=f"$.authority.{clock}",
                consumer_effect="approval state cannot be audited independently",
            )
        approved = value["approved"]
        record = value["record"]
        if not isinstance(approved, bool):
            _fail(
                "authority approved value must be boolean",
                code="authority_clock_invalid",
                section="authority",
                field_path=f"$.authority.{clock}.approved",
                consumer_effect="approval state is ambiguous",
            )
        if approved and not isinstance(record, dict):
            _fail(
                f"{clock} approval requires an exact authority record",
                code="authority_record_required",
                section="authority",
                field_path=f"$.authority.{clock}.record",
                consumer_effect=f"{clock} cannot be enabled from a technical receipt",
            )
        if not approved and record is not None:
            _fail(
                f"unapproved {clock} clock must not carry an authority record",
                code="authority_record_contradiction",
                section="authority",
                field_path=f"$.authority.{clock}.record",
                consumer_effect=f"{clock} state is contradictory",
            )


def _validate_human_decision(
    repo_root: Path,
    *,
    package: Mapping[str, Any],
    human: Mapping[str, Any],
    render_validation: Mapping[str, Any],
) -> None:
    state = human["state"]
    if state == "not_human_accepted":
        if any(
            human[key] is not None
            for key in ("receipt_path", "receipt_sha256", "artifact_sha256")
        ):
            _fail(
                "not_human_accepted must not inherit a decision receipt or artifact",
                code="silent_human_acceptance_inheritance",
                section="human_decision",
                field_path="$.human_decision",
                consumer_effect="technical validity could be misreported as creative acceptance",
            )
        if package["content_authority"] != "internal_factory_canary_not_human_accepted":
            _fail(
                "canary human state contradicts the content authority boundary",
                code="human_authority_contradiction",
                section="human_decision",
                field_path="$.package.content_authority",
                consumer_effect="creative clock would not match package authority",
            )
        return
    if state != "accepted_exact_artifact":
        _fail(
            "unsupported human decision state",
            code="human_decision_state_invalid",
            section="human_decision",
            field_path="$.human_decision.state",
            consumer_effect="creative decision cannot be interpreted",
        )
    for key in ("receipt_path", "receipt_sha256", "artifact_sha256"):
        if not human[key]:
            _fail(
                "accepted human decision requires exact receipt and artifact identity",
                code="human_decision_identity_missing",
                section="human_decision",
                field_path=f"$.human_decision.{key}",
                consumer_effect="acceptance would not be bound to exact bytes",
            )
    receipt_path = _verify_bound_file(
        repo_root,
        human,
        section="human_decision",
        path_key="receipt_path",
        hash_key="receipt_sha256",
    )
    receipt = _load_json(
        receipt_path,
        section="human_decision",
        field_path="$.human_decision.receipt_path",
    )
    reviewed = receipt.get("reviewed_artifact")
    artifact_sha = _validate_sha(
        human["artifact_sha256"],
        section="human_decision",
        field_path="$.human_decision.artifact_sha256",
    )
    if (
        not isinstance(reviewed, dict)
        or str(reviewed.get("sha256", "")).lower() != artifact_sha
        or artifact_sha != str(render_validation["mp4_sha256"]).lower()
    ):
        _fail(
            "human decision does not bind the package MP4 identity",
            code="contradictory_accepted_identity",
            section="human_decision",
            field_path="$.human_decision.artifact_sha256",
            consumer_effect="acceptance could be inherited from another artifact or topic",
        )


def _validate_extensions(extensions: Mapping[str, Any]) -> None:
    values = extensions["values"]
    if not isinstance(values, dict):
        _fail(
            "extensions.values must be an object",
            code="extensions_invalid",
            section="extensions",
            field_path="$.extensions.values",
            consumer_effect="topic-specific extensions cannot be namespaced",
        )
    invalid = [name for name in values if not EXTENSION_NAME_RE.fullmatch(name)]
    if invalid:
        _fail(
            f"invalid namespaced extensions: {', '.join(sorted(invalid))}",
            code="invalid_namespaced_extension",
            section="extensions",
            field_path="$.extensions.values",
            consumer_effect="shared consumers could confuse topic data with core contract state",
        )


def _validate_content_identity(identities: Mapping[str, Any]) -> None:
    _validate_sha(
        identities["content_identity_sha256"],
        section="identities",
        field_path="$.identities.content_identity_sha256",
    )
    excluded = identities["content_identity_excludes"]
    if not isinstance(excluded, list) or not excluded:
        _fail(
            "content identity must explicitly exclude run-local state",
            code="content_identity_exclusions_missing",
            section="identities",
            field_path="$.identities.content_identity_excludes",
            consumer_effect="run identity could pollute content identity",
        )
    lowered = {str(value).lower() for value in excluded}
    required = {"timestamp", "pid", "machine_path", "run_id"}
    if not required.issubset(lowered):
        _fail(
            "content identity exclusions must cover timestamp, PID, machine path, and run ID",
            code="content_identity_pollution_risk",
            section="identities",
            field_path="$.identities.content_identity_excludes",
            consumer_effect="equivalent content could receive machine-specific identities",
        )
    for path, key, value in _walk(identities):
        if (
            any(part in key.lower() for part in CONTENT_IDENTITY_FORBIDDEN_PARTS)
            and path != "$.identities.content_identity_excludes"
            and value not in (None, False)
        ):
            _fail(
                "run-local field is forbidden inside content identity state",
                code="content_identity_polluted",
                section="identities",
                field_path=path,
                consumer_effect="resume and content comparison would become nondeterministic",
            )


def validate_factory_package(
    *,
    repo_root: Path,
    descriptor_path: Path,
    check_live: bool = False,
) -> dict[str, Any]:
    """Validate and normalize one v2 descriptor without mutating any authority."""

    repo_root = repo_root.resolve()
    if not descriptor_path.is_absolute():
        descriptor_path = repo_root / descriptor_path
    descriptor_path = descriptor_path.resolve()
    if descriptor_path != repo_root and repo_root not in descriptor_path.parents:
        _fail(
            "descriptor path escaped repository root",
            code="descriptor_path_escape",
            section="root",
            field_path="$",
            consumer_effect="validator could read an untracked external descriptor",
        )
    payload = _load_json(descriptor_path, section="root", field_path="$")
    actual_top = set(payload)
    missing_top = sorted(TOP_LEVEL_FIELDS - actual_top)
    unknown_top = sorted(actual_top - TOP_LEVEL_FIELDS)
    if missing_top:
        _fail(
            f"required top-level sections are missing: {', '.join(missing_top)}",
            code="required_section_missing",
            section="root",
            field_path="$",
            consumer_effect="factory package cannot be normalized",
        )
    if unknown_top:
        _fail(
            f"unknown unversioned top-level fields: {', '.join(unknown_top)}",
            code="unknown_top_level_field",
            section="root",
            field_path="$",
            consumer_effect="shared code could hide topic-specific behavior",
        )
    if (
        payload.get("schema") != FACTORY_PACKAGE_SCHEMA
        or payload.get("schema_version") != FACTORY_PACKAGE_VERSION
    ):
        _fail(
            "unsupported Factory Package schema/version",
            code="factory_package_schema_invalid",
            section="root",
            field_path="$.schema",
            consumer_effect="validator version cannot be selected deterministically",
        )
    _validate_safe_tracked_payload(payload)

    sections = {
        name: _require_exact_fields(payload[name], section=name)
        for name in SECTION_SCHEMAS
    }
    _validate_extensions(sections["extensions"])
    _validate_content_identity(sections["identities"])
    _validate_authority_clocks(sections["authority"])

    contract_schema_path = _verify_bound_file(
        repo_root,
        sections["contract"],
        section="contract",
        path_key="schema_path",
        hash_key="schema_sha256",
    )
    inventory_path = _verify_bound_file(
        repo_root,
        sections["contract"],
        section="contract",
        path_key="field_inventory_path",
        hash_key="field_inventory_sha256",
    )
    contract_schema = _load_json(
        contract_schema_path,
        section="contract",
        field_path="$.contract.schema_path",
    )
    if contract_schema.get("$id") != FACTORY_PACKAGE_SCHEMA:
        _fail(
            "bound JSON Schema identity does not match Factory Package v2",
            code="contract_schema_identity_mismatch",
            section="contract",
            field_path="$.contract.schema_path",
            consumer_effect="schema file could describe a different contract",
        )
    inventory = _load_json(
        inventory_path,
        section="contract",
        field_path="$.contract.field_inventory_path",
    )
    if inventory.get("schema") != FIELD_INVENTORY_SCHEMA:
        _fail(
            "field inventory schema identity is invalid",
            code="field_inventory_schema_invalid",
            section="contract",
            field_path="$.contract.field_inventory_path",
            consumer_effect="field classifications cannot be audited",
        )
    inventory_rows = inventory.get("fields")
    if not isinstance(inventory_rows, list) or not inventory_rows:
        _fail(
            "field inventory must contain classified fields",
            code="field_inventory_empty",
            section="contract",
            field_path="$.contract.field_inventory_path",
            consumer_effect="required/variable/optional/forbidden boundaries are implicit",
        )
    classification_counts = Counter(
        str(row.get("classification"))
        for row in inventory_rows
        if isinstance(row, dict)
    )
    required_classes = {
        "required",
        "variable",
        "optional",
        "forbidden",
        "topic-extension",
        "run-local",
        "evidence-only",
    }
    if not required_classes.issubset(classification_counts):
        _fail(
            "field inventory does not exercise every required classification",
            code="field_inventory_classification_gap",
            section="contract",
            field_path="$.contract.field_inventory_path",
            consumer_effect="a contract boundary remains implicit",
        )

    source_path = _verify_bound_file(
        repo_root,
        sections["source_intake"],
        section="source_intake",
        path_key="authority_path",
        hash_key="authority_sha256",
    )
    claim_path = _verify_bound_file(
        repo_root,
        sections["claim_support"],
        section="claim_support",
        path_key="authority_path",
        hash_key="authority_sha256",
    )
    canonical_path = _verify_bound_file(
        repo_root,
        sections["canonical_content"],
        section="canonical_content",
        path_key="path",
        hash_key="sha256",
    )
    provenance_path = _verify_bound_file(
        repo_root,
        sections["media_provenance"],
        section="media_provenance",
        path_key="path",
        hash_key="sha256",
    )
    manifest_path = _verify_bound_file(
        repo_root,
        sections["episode_execution"],
        section="episode_execution",
        path_key="manifest_path",
        hash_key="manifest_sha256",
    )
    technical_receipt_path = _verify_bound_file(
        repo_root,
        sections["render_validation"],
        section="render_validation",
        path_key="technical_receipt_path",
        hash_key="technical_receipt_sha256",
    )

    source_authority = _load_json(
        source_path,
        section="source_intake",
        field_path="$.source_intake.authority_path",
    )
    claim_authority = _load_json(
        claim_path,
        section="claim_support",
        field_path="$.claim_support.authority_path",
    )
    canonical = _load_json(
        canonical_path,
        section="canonical_content",
        field_path="$.canonical_content.path",
    )
    provenance = _load_json(
        provenance_path,
        section="media_provenance",
        field_path="$.media_provenance.path",
    )
    manifest = _load_json(
        manifest_path,
        section="episode_execution",
        field_path="$.episode_execution.manifest_path",
    )
    technical_receipt = _load_json(
        technical_receipt_path,
        section="render_validation",
        field_path="$.render_validation.technical_receipt_path",
    )
    del source_authority, claim_authority, canonical

    package = sections["package"]
    episode = sections["episode_execution"]
    shape = sections["shape"]
    if manifest.get("schema") != episode["manifest_schema"]:
        _fail(
            "episode manifest schema contradicts the descriptor",
            code="episode_manifest_schema_mismatch",
            section="episode_execution",
            field_path="$.episode_execution.manifest_schema",
            consumer_effect="existing video pipeline cannot select its manifest loader",
        )
    if manifest.get("episode_id") != package["episode_id"]:
        _fail(
            "episode identity contradicts the v1 manifest",
            code="episode_identity_mismatch",
            section="package",
            field_path="$.package.episode_id",
            consumer_effect="descriptor could bind another topic's execution manifest",
        )
    if (
        manifest.get("source_package") != sections["source_intake"]["authority_path"]
        or manifest.get("provenance_manifest_path")
        != sections["media_provenance"]["path"]
    ):
        _fail(
            "source or provenance authority contradicts the v1 manifest",
            code="v1_authority_binding_mismatch",
            section="episode_execution",
            field_path="$.episode_execution.manifest_path",
            consumer_effect="v1 adapter would normalize a different authority chain",
        )
    manifest_locks = {
        str(row.get("path")): str(row.get("sha256", "")).lower()
        for row in manifest.get("content_locks", [])
        if isinstance(row, dict)
    }
    canonical_declared = str(sections["canonical_content"]["path"])
    if (
        manifest_locks.get(canonical_declared)
        != str(sections["canonical_content"]["sha256"]).lower()
    ):
        _fail(
            "canonical content is not protected by the v1 manifest",
            code="canonical_content_lock_missing",
            section="canonical_content",
            field_path="$.canonical_content.path",
            consumer_effect="content identity would not bind the declared canonical script",
        )

    cue_rows = manifest.get("cue_mapping")
    if not isinstance(cue_rows, list) or not cue_rows:
        _fail(
            "v1 manifest cue mapping is missing",
            code="cue_mapping_invalid",
            section="shape",
            field_path="$.episode_execution.manifest_path",
            consumer_effect="cue/scene/speaker shape cannot be normalized",
        )
    cue_ids = [str(row.get("cue_id")) for row in cue_rows if isinstance(row, dict)]
    expected_sequence = sections["canonical_content"]["cue_sequence"]
    if cue_ids != expected_sequence:
        _fail(
            "cue sequence/order differs from the v1 manifest",
            code="cue_sequence_mismatch",
            section="canonical_content",
            field_path="$.canonical_content.cue_sequence",
            consumer_effect="canonical dialogue order could drift",
        )
    if int(shape["cue_count"]) != len(cue_ids):
        _fail(
            "cue count differs from the v1 manifest",
            code="cue_count_mismatch",
            section="shape",
            field_path="$.shape.cue_count",
            consumer_effect="pipeline sizing would be incorrect",
        )
    scene_mapping = {
        str(row["cue_id"]): str(row["scene_id"])
        for row in cue_rows
        if isinstance(row, dict)
    }
    speaker_mapping = {
        str(row["cue_id"]): str(row["speaker"])
        for row in cue_rows
        if isinstance(row, dict)
    }
    if (
        scene_mapping != shape["scene_mapping"]
        or speaker_mapping != shape["speaker_mapping"]
    ):
        _fail(
            "scene or speaker mapping differs from the v1 manifest",
            code="shape_mapping_mismatch",
            section="shape",
            field_path="$.shape",
            consumer_effect="project generation would use a contradictory shape",
        )
    scene_count = len(set(scene_mapping.values()))
    speaker_counts = dict(Counter(speaker_mapping.values()))
    if (
        int(shape["scene_count"]) != scene_count
        or shape["speaker_counts"] != speaker_counts
    ):
        _fail(
            "scene count or speaker distribution differs from the v1 manifest",
            code="shape_count_mismatch",
            section="shape",
            field_path="$.shape",
            consumer_effect="observed variation axes would be misstated",
        )
    yymm4 = manifest.get("yymm4") or {}
    if (
        int(shape["timeline_frames"]) != int(yymm4.get("timeline_frames", -1))
        or int(shape["fps"]) != int(yymm4.get("fps", -1))
        or abs(
            float(shape["duration_seconds"])
            - float(yymm4.get("duration_seconds", -1))
        )
        > 0.000001
    ):
        _fail(
            "timeline shape differs from the v1 manifest",
            code="timeline_shape_mismatch",
            section="shape",
            field_path="$.shape.timeline_frames",
            consumer_effect="duration/frame variation would be misstated",
        )
    if (
        sections["source_project"]["path"] != yymm4.get("source_project_path")
        or str(sections["source_project"]["sha256"]).lower()
        != str(yymm4.get("source_project_sha256", "")).lower()
    ):
        _fail(
            "source-project identity differs from the v1 manifest",
            code="source_project_identity_mismatch",
            section="source_project",
            field_path="$.source_project",
            consumer_effect="dry-run could inspect a different project",
        )
    output = manifest.get("output") or {}
    if any(
        (
            episode["run_id"] != output.get("run_id"),
            episode["project_filename"] != output.get("project_filename"),
            episode["mp4_filename"] != output.get("mp4_filename"),
        )
    ):
        _fail(
            "run/output identity differs from the v1 manifest",
            code="run_identity_mismatch",
            section="episode_execution",
            field_path="$.episode_execution.run_id",
            consumer_effect="resume/output routing would target another run",
        )
    if sha256_json(manifest.get("render_settings")) != episode["render_settings_sha256"]:
        _fail(
            "render settings identity differs from the v1 manifest",
            code="render_settings_identity_mismatch",
            section="episode_execution",
            field_path="$.episode_execution.render_settings_sha256",
            consumer_effect="dry-run would not describe the bound execution settings",
        )

    if provenance.get("schema") != "nlmytgen.real_media_provenance.v1":
        _fail(
            "unsupported media provenance schema",
            code="media_provenance_schema_invalid",
            section="media_provenance",
            field_path="$.media_provenance.path",
            consumer_effect="cue-to-asset provenance cannot be normalized",
        )
    sources = provenance.get("sources")
    assets = provenance.get("assets")
    if not isinstance(sources, list) or not isinstance(assets, list):
        _fail(
            "media provenance sources/assets must be arrays",
            code="media_provenance_shape_invalid",
            section="media_provenance",
            field_path="$.media_provenance.path",
            consumer_effect="source and media coverage cannot be counted",
        )
    if (
        int(shape["source_count"]) != len(sources)
        or int(sections["source_intake"]["source_count"]) != len(sources)
        or int(shape["asset_count"]) != len(assets)
    ):
        _fail(
            "source or asset counts differ from provenance",
            code="provenance_count_mismatch",
            section="media_provenance",
            field_path="$.shape",
            consumer_effect="observed variation axes would be misstated",
        )
    provenance_by_id = {
        str(row.get("asset_id")): row for row in assets if isinstance(row, dict)
    }
    descriptor_mappings = sections["media_provenance"]["asset_mappings"]
    if not isinstance(descriptor_mappings, list) or len(descriptor_mappings) != len(cue_ids):
        _fail(
            "each cue requires one normalized media mapping",
            code="cue_media_mapping_incomplete",
            section="media_provenance",
            field_path="$.media_provenance.asset_mappings",
            consumer_effect="pipeline could build a cue without provenance",
        )
    mapping_by_cue = {
        str(row.get("cue_id")): row
        for row in descriptor_mappings
        if isinstance(row, dict)
    }
    for cue in cue_rows:
        cue_id = str(cue["cue_id"])
        mapping = mapping_by_cue.get(cue_id)
        asset_id = str(cue.get("visual_id"))
        provenance_row = provenance_by_id.get(asset_id)
        if (
            mapping is None
            or provenance_row is None
            or mapping.get("asset_id") != asset_id
            or mapping.get("source_id") != cue.get("source_provenance_id")
            or mapping.get("source_id") != provenance_row.get("source_id")
            or cue_id not in provenance_row.get("cue_ids", [])
            or str(mapping.get("sha256", "")).lower()
            != str(provenance_row.get("sha256", "")).lower()
        ):
            _fail(
                f"cue media provenance is incomplete or contradictory: {cue_id}",
                code="cue_media_provenance_invalid",
                section="media_provenance",
                field_path=f"$.media_provenance.asset_mappings.{cue_id}",
                consumer_effect="cue visual identity cannot be trusted",
            )

    factual = sections["claim_support"]["factual_cue_ids"]
    nonfactual = sections["claim_support"]["nonfactual_cue_ids"]
    if (
        not isinstance(factual, list)
        or not isinstance(nonfactual, list)
        or len(factual) != len(set(factual))
        or len(nonfactual) != len(set(nonfactual))
        or set(factual) & set(nonfactual)
        or set(factual) | set(nonfactual) != set(cue_ids)
    ):
        _fail(
            "factual and nonfactual cue coverage must be complete and disjoint",
            code="claim_cue_coverage_invalid",
            section="claim_support",
            field_path="$.claim_support",
            consumer_effect="a source-backed factual cue could lack claim support",
        )
    if (
        sections["source_intake"]["source_backed"] is True
        and (not factual or int(sections["claim_support"]["unsupported_factual_units"]) != 0)
    ):
        _fail(
            "source-backed package contains unsupported or missing factual cue coverage",
            code="factual_claim_support_invalid",
            section="claim_support",
            field_path="$.claim_support.unsupported_factual_units",
            consumer_effect="unsupported factual dialogue could enter the pipeline",
        )

    if technical_receipt.get("status") != sections["render_validation"]["technical_status"]:
        _fail(
            "technical receipt status contradicts the descriptor",
            code="technical_receipt_status_mismatch",
            section="render_validation",
            field_path="$.render_validation.technical_status",
            consumer_effect="technical validity could be overstated",
        )
    for section_name in ("generated_project", "render_validation"):
        if sections[section_name]["availability_claim"] != "receipt_identity_only":
            _fail(
                "tracked descriptor may claim only receipt identity, not live availability",
                code="receipt_only_live_availability_claim",
                section=section_name,
                field_path=f"$.{section_name}.availability_claim",
                consumer_effect="a past receipt could be mistaken for a currently available file",
            )
    if sections["source_project"]["live_required_for_contract"] is not False:
        _fail(
            "live source project must not be required for tracked contract validity",
            code="live_artifact_required_for_contract",
            section="source_project",
            field_path="$.source_project.live_required_for_contract",
            consumer_effect="tracked-only validation would produce a false contract failure",
        )

    _validate_human_decision(
        repo_root,
        package=package,
        human=sections["human_decision"],
        render_validation=sections["render_validation"],
    )

    availability = [
        _availability(
            repo_root,
            section="source_project",
            path_value=sections["source_project"]["path"],
            sha_value=sections["source_project"]["sha256"],
            check_live=check_live,
        ),
        _availability(
            repo_root,
            section="generated_project",
            path_value=sections["generated_project"]["path"],
            sha_value=sections["generated_project"]["sha256"],
            check_live=check_live,
        ),
        _availability(
            repo_root,
            section="render_validation",
            path_value=sections["render_validation"]["mp4_path"],
            sha_value=sections["render_validation"]["mp4_sha256"],
            check_live=check_live,
        ),
    ]

    descriptor_repo_path = descriptor_path.relative_to(repo_root).as_posix()
    descriptor_sha = sha256_file(descriptor_path)
    normalized_identity = sha256_json(
        {
            "schema": FACTORY_PACKAGE_SCHEMA,
            "schema_version": FACTORY_PACKAGE_VERSION,
            "package": package,
            "source_intake": sections["source_intake"],
            "claim_support": sections["claim_support"],
            "canonical_content": sections["canonical_content"],
            "shape": shape,
            "media_provenance": sections["media_provenance"],
            "episode_execution": episode,
            "source_project": sections["source_project"],
            "generated_project": sections["generated_project"],
            "render_validation": sections["render_validation"],
            "identities": sections["identities"],
            "resume_identity": sections["resume_identity"],
            "human_decision": sections["human_decision"],
            "authority": sections["authority"],
            "extensions": sections["extensions"],
        }
    )
    return {
        "schema": VALIDATION_RESULT_SCHEMA,
        "status": "passed",
        "package_id": package["package_id"],
        "episode_id": package["episode_id"],
        "descriptor": {
            "path": descriptor_repo_path,
            "sha256": descriptor_sha,
            "normalized_sha256": normalized_identity,
        },
        "contract": {
            "schema": FACTORY_PACKAGE_SCHEMA,
            "version": FACTORY_PACKAGE_VERSION,
            "json_schema_sha256": sections["contract"]["schema_sha256"],
            "field_inventory_sha256": sections["contract"]["field_inventory_sha256"],
            "classification_counts": dict(sorted(classification_counts.items())),
        },
        "normalized": {
            "content_authority": package["content_authority"],
            "source_count": int(shape["source_count"]),
            "cue_count": int(shape["cue_count"]),
            "scene_count": int(shape["scene_count"]),
            "speaker_counts": shape["speaker_counts"],
            "timeline_frames": int(shape["timeline_frames"]),
            "fps": int(shape["fps"]),
            "duration_seconds": float(shape["duration_seconds"]),
            "asset_count": int(shape["asset_count"]),
            "content_identity_sha256": sections["identities"]["content_identity_sha256"],
            "episode_manifest_path": episode["manifest_path"],
            "run_id": episode["run_id"],
            "human_decision": sections["human_decision"]["state"],
            "rights_approved": sections["authority"]["rights"]["approved"],
            "production_approved": sections["authority"]["production"]["approved"],
            "publication_approved": sections["authority"]["publication"]["approved"],
            "upload_approved": sections["authority"]["upload"]["approved"],
        },
        "availability": availability,
        "v1_compatibility": {
            "adapter": "generic_descriptor_driven_read_only",
            "manifest_schema": manifest.get("schema"),
            "manifest_sha256": episode["manifest_sha256"],
            "provenance_sha256": sections["media_provenance"]["sha256"],
            "canonical_content_sha256": sections["canonical_content"]["sha256"],
            "technical_receipt_sha256": sections["render_validation"][
                "technical_receipt_sha256"
            ],
            "source_artifacts_mutated": False,
        },
        "boundaries": {
            "tracked_contract_valid_without_live_artifacts": True,
            "live_hashes_checked": check_live,
            "network_access": False,
            "yymm4_launched": False,
            "render_performed": False,
            "media_playback": False,
            "artifacts_mutated": False,
            "universal_arbitrary_topic_compatibility": False,
        },
    }


def validate_factory_contract_receipt(payload: Mapping[str, Any]) -> None:
    """Reject generalization claims outside the three observed v2 fixtures."""

    if payload.get("schema") != "nlmytgen.factory_contract_v2_validation_receipt.v1":
        _fail(
            "unsupported Factory Contract validation receipt schema",
            code="contract_receipt_schema_invalid",
            section="receipt",
            field_path="$.schema",
            consumer_effect="supervising consumers cannot interpret the evidence",
        )
    claims = payload.get("claims")
    if not isinstance(claims, Mapping):
        _fail(
            "validation receipt claims must be an object",
            code="contract_receipt_claims_invalid",
            section="receipt",
            field_path="$.claims",
            consumer_effect="supported and unsupported axes are not explicit",
        )
    if (
        claims.get("universal_arbitrary_topic_compatibility") is not False
        or claims.get("fourth_topic_validated") is not False
        or claims.get("production_ready") is not False
    ):
        _fail(
            "validation receipt overclaims an unobserved factory axis",
            code="unobserved_axis_overclaim",
            section="receipt",
            field_path="$.claims",
            consumer_effect="the fourth topic would no longer be an out-of-sample gate",
        )
