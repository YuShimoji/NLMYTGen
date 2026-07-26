"""Lifecycle-aware Factory Package v2.1 validation and v2.0 normalization.

Factory Package v2.1 represents packages before rendering without fabricating
source-project, generated-project, MP4, technical-render, or human-decision
evidence. Existing v2.0 descriptors remain byte-exact and are normalized
read-only into the lifecycle model.
"""

from __future__ import annotations

import copy
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from src.pipeline.factory_contract_v2 import (
    FACTORY_PACKAGE_SCHEMA as FACTORY_PACKAGE_V2_SCHEMA,
    FactoryContractError,
    _fail,
    _load_json,
    _resolve_repo_path,
    _validate_authority_clocks,
    _validate_content_identity,
    _validate_extensions,
    _validate_safe_tracked_payload,
    _validate_sha,
    _verify_bound_file,
    canonical_json_bytes,
    sha256_file,
    sha256_json,
    validate_factory_package as validate_factory_package_v2,
)


FACTORY_PACKAGE_SCHEMA = "nlmytgen.factory_package.v2.1"
FACTORY_PACKAGE_VERSION = "2.1"
VALIDATION_RESULT_SCHEMA = "nlmytgen.factory_package_lifecycle_validation.v2.1"
FIELD_INVENTORY_SCHEMA = "nlmytgen.factory_contract_field_inventory.v2.1"
PRE_RENDER_MANIFEST_SCHEMA = "nlmytgen.episode_manifest.pre_render.v2.1"
STAGE_PLAN_SCHEMA = "nlmytgen.factory_pre_render_stage_plan.v1"

LIFECYCLE_ORDER = (
    "package_prepared",
    "source_project_ready",
    "rendered",
    "human_accepted",
)
LIFECYCLE_RANK = {state: index for index, state in enumerate(LIFECYCLE_ORDER)}
LIFECYCLE_FLAGS = {
    "package_prepared": {
        "contract_valid": True,
        "tracked_package_ready": True,
        "source_project_ready": False,
        "render_ready": False,
        "human_accepted": False,
    },
    "source_project_ready": {
        "contract_valid": True,
        "tracked_package_ready": True,
        "source_project_ready": True,
        "render_ready": False,
        "human_accepted": False,
    },
    "rendered": {
        "contract_valid": True,
        "tracked_package_ready": True,
        "source_project_ready": True,
        "render_ready": True,
        "human_accepted": False,
    },
    "human_accepted": {
        "contract_valid": True,
        "tracked_package_ready": True,
        "source_project_ready": True,
        "render_ready": True,
        "human_accepted": True,
    },
}

REQUIRED_TOP_LEVEL_FIELDS = {
    "schema",
    "schema_version",
    "contract",
    "lifecycle",
    "package",
    "source_intake",
    "claim_support",
    "canonical_content",
    "shape",
    "media_provenance",
    "episode_execution",
    "source_project",
    "identities",
    "resume_identity",
    "authority",
    "extensions",
}
OPTIONAL_TOP_LEVEL_FIELDS = {
    "generated_project",
    "render_validation",
    "human_decision",
}
SECTION_SCHEMAS = {
    "contract": "nlmytgen.factory_contract.v2.1",
    "lifecycle": "nlmytgen.factory_package.lifecycle.v2.1",
    "package": "nlmytgen.factory_package.package_identity.v2.1",
    "source_intake": "nlmytgen.factory_package.source_intake.v2.1",
    "claim_support": "nlmytgen.factory_package.claim_support.v2.1",
    "canonical_content": "nlmytgen.factory_package.canonical_content.v2.1",
    "shape": "nlmytgen.factory_package.shape.v2.1",
    "media_provenance": "nlmytgen.factory_package.media_provenance.v2.1",
    "episode_execution": "nlmytgen.factory_package.episode_execution.v2.1",
    "source_project": "nlmytgen.factory_package.source_project.v2.1",
    "generated_project": "nlmytgen.factory_package.generated_project.v2.1",
    "render_validation": "nlmytgen.factory_package.render_validation.v2.1",
    "identities": "nlmytgen.factory_package.identities.v2.1",
    "resume_identity": "nlmytgen.factory_package.resume_identity.v2.1",
    "human_decision": "nlmytgen.factory_package.human_decision.v2.1",
    "authority": "nlmytgen.factory_package.authority.v2.1",
    "extensions": "nlmytgen.factory_package.extensions.v2.1",
}
SECTION_FIELDS = {
    "contract": {
        "schema",
        "schema_path",
        "schema_sha256",
        "field_inventory_path",
        "field_inventory_sha256",
        "v2_0_schema_path",
        "v2_0_schema_sha256",
        "v2_0_field_inventory_path",
        "v2_0_field_inventory_sha256",
    },
    "lifecycle": {
        "schema",
        "state",
        "contract_valid",
        "tracked_package_ready",
        "source_project_ready",
        "render_ready",
        "human_accepted",
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
        "timing_basis",
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
        "planned_run_id",
        "project_filename",
        "mp4_filename",
        "render_settings_sha256",
    },
    "source_project": {
        "schema",
        "state",
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


def _descriptor_path(repo_root: Path, descriptor_path: Path) -> Path:
    root = repo_root.resolve()
    path = descriptor_path
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    if path != root and root not in path.parents:
        _fail(
            "Factory Package descriptor escaped the repository root",
            code="descriptor_path_escape",
            section="root",
            field_path="$",
            consumer_effect="validator could read an unrelated or private file",
        )
    if not path.is_file():
        _fail(
            "Factory Package descriptor is missing",
            code="authority_unreadable",
            section="root",
            field_path="$",
            consumer_effect="contract lifecycle cannot be selected",
        )
    return path


def _require_exact_section(
    value: Any,
    *,
    section: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(
            "Factory Package section must be an object",
            code="section_type_invalid",
            section=section,
            field_path=f"$.{section}",
            consumer_effect="section fields cannot be addressed deterministically",
        )
    expected = SECTION_FIELDS[section]
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        _fail(
            f"section fields differ; missing={missing}, unknown={unknown}",
            code="section_fields_invalid",
            section=section,
            field_path=f"$.{section}",
            consumer_effect="unversioned or incomplete lifecycle evidence could be accepted",
        )
    if value["schema"] != SECTION_SCHEMAS[section]:
        _fail(
            "section schema identity is invalid",
            code="section_schema_invalid",
            section=section,
            field_path=f"$.{section}.schema",
            consumer_effect="section version cannot be interpreted deterministically",
        )
    return value


def _validate_top_level(payload: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    actual = set(payload)
    allowed = REQUIRED_TOP_LEVEL_FIELDS | OPTIONAL_TOP_LEVEL_FIELDS
    missing = sorted(REQUIRED_TOP_LEVEL_FIELDS - actual)
    unknown = sorted(actual - allowed)
    if missing or unknown:
        _fail(
            f"top-level fields differ; missing={missing}, unknown={unknown}",
            code="top_level_fields_invalid",
            section="root",
            field_path="$",
            consumer_effect="unversioned or incomplete lifecycle evidence could be accepted",
        )
    if (
        payload.get("schema") != FACTORY_PACKAGE_SCHEMA
        or payload.get("schema_version") != FACTORY_PACKAGE_VERSION
    ):
        _fail(
            "Factory Package v2.1 schema identity is invalid",
            code="factory_package_schema_invalid",
            section="root",
            field_path="$.schema",
            consumer_effect="validator version cannot be selected deterministically",
        )
    sections: dict[str, dict[str, Any]] = {}
    for name in SECTION_SCHEMAS:
        if name in payload:
            sections[name] = _require_exact_section(payload[name], section=name)
    return sections


def _validate_required_lifecycle(
    actual: str,
    required: str | None,
) -> None:
    if required is None:
        return
    if required not in LIFECYCLE_RANK:
        _fail(
            "required lifecycle is not recognized",
            code="required_lifecycle_invalid",
            section="lifecycle",
            field_path="$.lifecycle.state",
            consumer_effect="caller requirement cannot be compared",
        )
    if LIFECYCLE_RANK[actual] < LIFECYCLE_RANK[required]:
        _fail(
            f"package lifecycle {actual} has not reached required state {required}",
            code="required_lifecycle_not_reached",
            section="lifecycle",
            field_path="$.lifecycle.state",
            consumer_effect=f"{required} consumer must not run on {actual} evidence",
        )


def _normalize_v2_0_result(
    *,
    payload: Mapping[str, Any],
    result: Mapping[str, Any],
    require_lifecycle: str | None,
) -> dict[str, Any]:
    normalized = copy.deepcopy(dict(result))
    human_state = str(payload["human_decision"]["state"])
    lifecycle_state = (
        "human_accepted"
        if human_state == "accepted_exact_artifact"
        else "rendered"
    )
    _validate_required_lifecycle(lifecycle_state, require_lifecycle)
    lifecycle = {
        "schema": "nlmytgen.factory_package.lifecycle.normalized.v2.1",
        "state": lifecycle_state,
        **LIFECYCLE_FLAGS[lifecycle_state],
    }
    normalized["input_schema"] = FACTORY_PACKAGE_V2_SCHEMA
    normalized["input_schema_version"] = str(payload.get("schema_version"))
    normalized["normalized_lifecycle"] = lifecycle
    normalized["normalized"]["lifecycle"] = lifecycle_state
    normalized["compatibility"] = {
        "adapter": "v2_0_to_v2_1_read_only_lifecycle_normalizer",
        "source_descriptor_mutated": False,
        "lifecycle_basis": (
            "exact_human_decision_receipt"
            if lifecycle_state == "human_accepted"
            else "generated_project_and_passed_render_validation"
        ),
    }
    normalized["required_lifecycle"] = require_lifecycle
    return normalized


def _validate_lifecycle_section(
    *,
    lifecycle: Mapping[str, Any],
) -> str:
    state = str(lifecycle["state"])
    if state not in LIFECYCLE_RANK:
        _fail(
            "lifecycle state is not recognized",
            code="lifecycle_state_invalid",
            section="lifecycle",
            field_path="$.lifecycle.state",
            consumer_effect="conditional evidence requirements cannot be selected",
        )
    expected = LIFECYCLE_FLAGS[state]
    observed = {name: lifecycle[name] for name in expected}
    if observed != expected:
        _fail(
            f"lifecycle readiness flags contradict state {state}",
            code="lifecycle_flags_contradiction",
            section="lifecycle",
            field_path="$.lifecycle",
            consumer_effect="queue or render consumers could run too early",
        )
    return state


def _validate_contract_bindings(
    *,
    repo_root: Path,
    contract: Mapping[str, Any],
) -> tuple[Path, Path]:
    schema_path = _verify_bound_file(
        repo_root,
        contract,
        section="contract",
        path_key="schema_path",
        hash_key="schema_sha256",
    )
    inventory_path = _verify_bound_file(
        repo_root,
        contract,
        section="contract",
        path_key="field_inventory_path",
        hash_key="field_inventory_sha256",
    )
    _verify_bound_file(
        repo_root,
        contract,
        section="contract",
        path_key="v2_0_schema_path",
        hash_key="v2_0_schema_sha256",
    )
    _verify_bound_file(
        repo_root,
        contract,
        section="contract",
        path_key="v2_0_field_inventory_path",
        hash_key="v2_0_field_inventory_sha256",
    )
    schema = _load_json(
        schema_path,
        section="contract",
        field_path="$.contract.schema_path",
    )
    inventory = _load_json(
        inventory_path,
        section="contract",
        field_path="$.contract.field_inventory_path",
    )
    if schema.get("$id") != FACTORY_PACKAGE_SCHEMA:
        _fail(
            "bound JSON Schema does not identify Factory Package v2.1",
            code="contract_schema_identity_invalid",
            section="contract",
            field_path="$.contract.schema_path",
            consumer_effect="schema conditionals could describe another contract",
        )
    if (
        inventory.get("schema") != FIELD_INVENTORY_SCHEMA
        or inventory.get("version") != FACTORY_PACKAGE_VERSION
        or inventory.get("inherits", {}).get("sha256")
        != contract["v2_0_field_inventory_sha256"]
    ):
        _fail(
            "v2.1 field inventory or its v2.0 inheritance binding is invalid",
            code="field_inventory_identity_invalid",
            section="contract",
            field_path="$.contract.field_inventory_path",
            consumer_effect="migration and rollback behavior cannot be audited",
        )
    return schema_path, inventory_path


def _artifact_availability(
    repo_root: Path,
    *,
    artifact_class: str,
    locator: Any,
    expected_sha256: Any,
    check_live: bool,
    contract_required: bool,
    field_path: str,
) -> dict[str, Any]:
    path = _resolve_repo_path(
        repo_root,
        locator,
        section=artifact_class,
        field_path=field_path,
    )
    expected = _validate_sha(
        expected_sha256,
        section=artifact_class,
        field_path=field_path.replace("path", "sha256"),
    )
    row = {
        "artifact_class": artifact_class,
        "locator": str(locator),
        "expected_sha256": expected,
        "contract_required": contract_required,
    }
    if not path.is_file():
        return {
            **row,
            "status": "receipt_only_no_live_file",
            "actual_sha256": None,
        }
    if not check_live:
        return {
            **row,
            "status": "live_file_present_not_hashed",
            "actual_sha256": None,
        }
    actual = sha256_file(path)
    if actual != expected:
        _fail(
            f"live artifact hash mismatch: {locator}",
            code="live_artifact_hash_mismatch",
            section=artifact_class,
            field_path=field_path.replace("path", "sha256"),
            consumer_effect="live stage planning cannot use bytes that differ from provenance",
        )
    return {
        **row,
        "status": "live_file_hash_exact",
        "actual_sha256": actual,
    }


def _read_csv_pairs(path: Path) -> list[tuple[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.reader(stream))
    except (OSError, UnicodeError, csv.Error) as exc:
        _fail(
            "derived CSV is unreadable",
            code="derived_csv_unreadable",
            section="episode_execution",
            field_path="$.episode_execution.manifest_path",
            consumer_effect="source-project plan cannot preserve approved text and speakers",
        )
        raise AssertionError("unreachable") from exc
    if any(len(row) != 2 for row in rows):
        _fail(
            "derived CSV must contain exactly speaker and text columns",
            code="derived_csv_shape_invalid",
            section="episode_execution",
            field_path="$.episode_execution.manifest_path",
            consumer_effect="source-project import row shape is ambiguous",
        )
    return [(row[0], row[1]) for row in rows]


def build_v2_1_content_identity_payload(
    *,
    manifest: Mapping[str, Any],
    shape: Mapping[str, Any],
    media_mappings: list[Mapping[str, Any]],
    source_project: Mapping[str, Any],
    render_settings_sha256: str,
) -> dict[str, Any]:
    """Return the deterministic pre-render content identity payload."""

    protected_inputs = sorted(
        (
            {"path": str(row["path"]), "sha256": str(row["sha256"])}
            for row in manifest["content_locks"]
        ),
        key=lambda row: row["path"],
    )
    cue_bindings = sorted(
        (
            {
                "cue_id": str(row["cue_id"]),
                "asset_id": str(row["asset_id"]),
                "source_id": str(row["source_id"]),
                "sha256": str(row["sha256"]),
                "crop": [float(value) for value in row["crop"]],
            }
            for row in media_mappings
        ),
        key=lambda row: row["cue_id"],
    )
    return {
        "schema": "nlmytgen.factory_content_identity.v2.1",
        "protected_inputs": protected_inputs,
        "shape": {
            "cue_count": int(shape["cue_count"]),
            "scene_count": int(shape["scene_count"]),
            "scene_mapping": dict(sorted(shape["scene_mapping"].items())),
            "speaker_mapping": dict(sorted(shape["speaker_mapping"].items())),
            "speaker_counts": dict(sorted(shape["speaker_counts"].items())),
            "timeline_frames": int(shape["timeline_frames"]),
            "fps": int(shape["fps"]),
            "duration_seconds": float(shape["duration_seconds"]),
            "timing_basis": str(shape["timing_basis"]),
            "asset_count": int(shape["asset_count"]),
            "source_count": int(shape["source_count"]),
        },
        "cue_media_bindings": cue_bindings,
        "source_project_strategy": str(source_project["strategy"]),
        "render_settings_sha256": render_settings_sha256,
    }


def _validate_authorities_and_shape(
    *,
    repo_root: Path,
    sections: Mapping[str, Mapping[str, Any]],
    check_live: bool,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    source_path = _verify_bound_file(
        repo_root,
        sections["source_intake"],
        section="source_intake",
        path_key="authority_path",
        hash_key="authority_sha256",
    )
    claims_path = _verify_bound_file(
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

    source_registry = _load_json(
        source_path,
        section="source_intake",
        field_path="$.source_intake.authority_path",
    )
    claims = _load_json(
        claims_path,
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

    package = sections["package"]
    shape = sections["shape"]
    source_intake = sections["source_intake"]
    claim_support = sections["claim_support"]
    canonical_content = sections["canonical_content"]
    media = sections["media_provenance"]
    episode = sections["episode_execution"]

    if (
        source_registry.get("schema") != "nlmytgen.source_registry.v1"
        or source_registry.get("topic") != package["title"]
        or source_registry.get("retrieval_policy", {}).get(
            "official_primary_surfaces_only"
        )
        is not True
        or source_registry.get("retrieval_policy", {}).get("login_used") is not False
        or source_registry.get("retrieval_policy", {}).get("credentials_used")
        is not False
    ):
        _fail(
            "source registry is not a bounded no-login official-source authority",
            code="source_registry_invalid",
            section="source_intake",
            field_path="$.source_intake.authority_path",
            consumer_effect="pre-render package cannot establish source intake",
        )
    sources = source_registry.get("sources")
    if (
        not isinstance(sources, list)
        or len(sources) != int(source_intake["source_count"])
        or int(shape["source_count"]) != len(sources)
        or not all(isinstance(row, dict) and row.get("primary_source") for row in sources)
    ):
        _fail(
            "source count or primary-source status differs from the descriptor",
            code="source_count_invalid",
            section="source_intake",
            field_path="$.source_intake.source_count",
            consumer_effect="claim and media source coverage is ambiguous",
        )
    source_ids = {str(row["source_id"]) for row in sources}

    cues = canonical.get("cues")
    if (
        canonical.get("schema") != "nlmytgen.canonical_script.v1"
        or canonical.get("episode_id") != package["episode_id"]
        or canonical.get("title") != package["title"]
        or not isinstance(cues, list)
    ):
        _fail(
            "canonical script identity differs from the package",
            code="canonical_content_invalid",
            section="canonical_content",
            field_path="$.canonical_content.path",
            consumer_effect="cue shape and text cannot be normalized",
        )
    cue_ids = [str(cue.get("cue_id")) for cue in cues]
    if (
        cue_ids != list(canonical_content["cue_sequence"])
        or len(cue_ids) != int(shape["cue_count"])
        or canonical.get("cue_count") != int(shape["cue_count"])
        or canonical.get("scene_count") != int(shape["scene_count"])
        or canonical.get("unsupported_spoken_factual_units") != 0
    ):
        _fail(
            "canonical cue order, counts, or factual support state differs",
            code="canonical_shape_invalid",
            section="shape",
            field_path="$.shape",
            consumer_effect="single-speaker and one-scene consumers could receive drifted input",
        )
    if len(cue_ids) != len(set(cue_ids)):
        _fail(
            "canonical cue IDs must be unique",
            code="cue_id_duplicate",
            section="canonical_content",
            field_path="$.canonical_content.cue_sequence",
            consumer_effect="claim and media bindings would be ambiguous",
        )

    factual = {
        str(cue["cue_id"])
        for cue in cues
        if cue.get("spoken_factual_unit") is True
    }
    nonfactual = set(cue_ids) - factual
    if (
        factual != set(claim_support["factual_cue_ids"])
        or nonfactual != set(claim_support["nonfactual_cue_ids"])
        or claim_support["unsupported_factual_units"] != 0
        or claims.get("checks", {}).get("unsupported_spoken_factual_units") != 0
    ):
        _fail(
            "factual and nonfactual cue partition differs from claim authority",
            code="factual_claim_partition_invalid",
            section="claim_support",
            field_path="$.claim_support",
            consumer_effect="unsupported factual units could enter the queue",
        )
    supported_claim_cues: set[str] = set()
    for claim in claims.get("claims", []):
        if not isinstance(claim, dict) or claim.get("status") != "supported":
            continue
        supported_claim_cues.update(str(value) for value in claim.get("spoken_cue_ids", []))
        support = claim.get("support")
        if not isinstance(support, list) or not support:
            _fail(
                "supported claim lacks a source edge",
                code="claim_source_support_missing",
                section="claim_support",
                field_path="$.claim_support.authority_path",
                consumer_effect="factual cue would have no reviewable primary source",
            )
        for row in support:
            if row.get("source_id") not in source_ids:
                _fail(
                    "claim references an unknown source",
                    code="claim_source_unknown",
                    section="claim_support",
                    field_path="$.claim_support.authority_path",
                    consumer_effect="source registry and claim authority disagree",
                )
    if supported_claim_cues != factual:
        _fail(
            "supported claim coverage does not equal factual cue set",
            code="unsupported_factual_unit",
            section="claim_support",
            field_path="$.claim_support.factual_cue_ids",
            consumer_effect="one or more factual cues cannot enter pre-render planning",
        )

    if (
        manifest.get("schema") != episode["manifest_schema"]
        or manifest.get("schema") != PRE_RENDER_MANIFEST_SCHEMA
        or manifest.get("episode_id") != package["episode_id"]
        or manifest.get("lifecycle") != "package_prepared"
    ):
        _fail(
            "pre-render episode manifest identity or lifecycle differs",
            code="episode_manifest_invalid",
            section="episode_execution",
            field_path="$.episode_execution.manifest_path",
            consumer_effect=(
                "stage planner could use a manifest that is not the immutable "
                "package-prepared content authority"
            ),
        )
    if (
        manifest.get("source_package") != source_intake["authority_path"]
        or manifest.get("approved_script") != canonical_content["path"]
        or manifest.get("provenance_manifest_path") != media["path"]
        or manifest.get("output_plan", {}).get("run_id") != episode["planned_run_id"]
        or manifest.get("output_plan", {}).get("project_filename")
        != episode["project_filename"]
        or manifest.get("output_plan", {}).get("mp4_filename") != episode["mp4_filename"]
    ):
        _fail(
            "manifest authority paths or planned output names differ",
            code="episode_manifest_binding_invalid",
            section="episode_execution",
            field_path="$.episode_execution.manifest_path",
            consumer_effect="protected inputs or stage plan would target different artifacts",
        )

    content_locks = manifest.get("content_locks")
    if not isinstance(content_locks, list) or not content_locks:
        _fail(
            "pre-render manifest must bind protected tracked inputs",
            code="content_locks_missing",
            section="episode_execution",
            field_path="$.episode_execution.manifest_path",
            consumer_effect="content identity cannot be recalculated",
        )
    protected_inputs: list[dict[str, Any]] = []
    seen_lock_paths: set[str] = set()
    for index, row in enumerate(content_locks):
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            _fail(
                "content lock must contain only path and sha256",
                code="content_lock_invalid",
                section="episode_execution",
                field_path=f"$.episode_execution.manifest_path.content_locks[{index}]",
                consumer_effect="protected input cannot be resolved deterministically",
            )
        lock_path = str(row["path"])
        if lock_path in seen_lock_paths:
            _fail(
                "content lock paths must be unique",
                code="content_lock_duplicate",
                section="episode_execution",
                field_path=f"$.episode_execution.manifest_path.content_locks[{index}]",
                consumer_effect="content identity would contain duplicate authority",
            )
        seen_lock_paths.add(lock_path)
        path = _resolve_repo_path(
            repo_root,
            lock_path,
            section="episode_execution",
            field_path=f"$.episode_execution.manifest_path.content_locks[{index}].path",
        )
        expected = _validate_sha(
            row["sha256"],
            section="episode_execution",
            field_path=f"$.episode_execution.manifest_path.content_locks[{index}].sha256",
        )
        if not path.is_file() or sha256_file(path) != expected:
            _fail(
                f"protected input lock failed: {lock_path}",
                code="protected_input_hash_mismatch",
                section="episode_execution",
                field_path=f"$.episode_execution.manifest_path.content_locks[{index}]",
                consumer_effect="pre-render package bytes differ from its identity",
            )
        protected_inputs.append(
            {"path": lock_path, "sha256": expected, "status": "passed"}
        )

    derived_csv_path = _resolve_repo_path(
        repo_root,
        manifest.get("derived_csv"),
        section="episode_execution",
        field_path="$.episode_execution.manifest_path.derived_csv",
    )
    if not derived_csv_path.is_file():
        _fail(
            "derived YMM4 import CSV is missing",
            code="derived_csv_missing",
            section="episode_execution",
            field_path="$.episode_execution.manifest_path.derived_csv",
            consumer_effect="source-project plan lacks import rows",
        )
    csv_pairs = _read_csv_pairs(derived_csv_path)
    manifest_cues = manifest.get("cue_mapping")
    if not isinstance(manifest_cues, list) or len(manifest_cues) != len(cues):
        _fail(
            "manifest cue mapping count differs from canonical cues",
            code="cue_mapping_count_invalid",
            section="episode_execution",
            field_path="$.episode_execution.manifest_path.cue_mapping",
            consumer_effect="media and subtitle plan is incomplete",
        )

    actual_scene_mapping: dict[str, str] = {}
    actual_speaker_mapping: dict[str, str] = {}
    canonical_text_by_cue = {str(row["cue_id"]): str(row["text"]) for row in cues}
    for cue, pair in zip(manifest_cues, csv_pairs, strict=True):
        cue_id = str(cue.get("cue_id"))
        subtitle_text = "".join(str(line) for line in cue.get("subtitle_lines", []))
        if (
            cue_id not in canonical_text_by_cue
            or pair[0] != cue.get("speaker")
            or pair[1] != canonical_text_by_cue[cue_id]
            or subtitle_text != canonical_text_by_cue[cue_id]
            or cue.get("asset_type") != "image"
            or cue.get("internal_review_only") is not True
        ):
            _fail(
                f"manifest cue text, speaker, subtitle, or media binding differs: {cue_id}",
                code="cue_manifest_binding_invalid",
                section="episode_execution",
                field_path="$.episode_execution.manifest_path.cue_mapping",
                consumer_effect="pre-render stage plan would change canonical content",
            )
        actual_scene_mapping[cue_id] = str(cue["scene_id"])
        actual_speaker_mapping[cue_id] = str(cue["speaker"])
    speaker_counts = dict(Counter(actual_speaker_mapping.values()))
    if (
        actual_scene_mapping != shape["scene_mapping"]
        or actual_speaker_mapping != shape["speaker_mapping"]
        or speaker_counts != shape["speaker_counts"]
        or len(set(actual_scene_mapping.values())) != int(shape["scene_count"])
        or sum(speaker_counts.values()) != int(shape["cue_count"])
        or any(int(value) <= 0 for value in speaker_counts.values())
    ):
        _fail(
            "scene or speaker shape differs from manifest; one-speaker shapes are valid",
            code="speaker_or_scene_shape_invalid",
            section="shape",
            field_path="$.shape",
            consumer_effect="queue planning would use a different speaker or scene allocation",
        )
    if abs(
        int(shape["timeline_frames"]) / int(shape["fps"])
        - float(shape["duration_seconds"])
    ) > 0.000001:
        _fail(
            "timeline frames, fps, and duration are inconsistent",
            code="planned_timing_invalid",
            section="shape",
            field_path="$.shape.duration_seconds",
            consumer_effect="pre-render duration plan cannot be compared",
        )

    if (
        provenance.get("schema") != "nlmytgen.real_media_provenance.v1"
        or provenance.get("episode_id") != package["episode_id"]
        or not isinstance(provenance.get("assets"), list)
    ):
        _fail(
            "real-media provenance authority is invalid",
            code="media_provenance_invalid",
            section="media_provenance",
            field_path="$.media_provenance.path",
            consumer_effect="cue media cannot be traced to official sources",
        )
    provenance_assets = {
        str(row["asset_id"]): row
        for row in provenance["assets"]
        if isinstance(row, dict) and "asset_id" in row
    }
    mappings = media["asset_mappings"]
    if not isinstance(mappings, list) or len(mappings) != len(cue_ids):
        _fail(
            "every cue requires one provenance-bound media view",
            code="cue_media_coverage_invalid",
            section="media_provenance",
            field_path="$.media_provenance.asset_mappings",
            consumer_effect="one or more cues lack pre-render visual evidence",
        )
    mapping_by_cue: dict[str, Mapping[str, Any]] = {}
    availability_by_asset: dict[str, dict[str, Any]] = {}
    for index, mapping in enumerate(mappings):
        if not isinstance(mapping, dict) or set(mapping) != {
            "cue_id",
            "asset_id",
            "source_id",
            "local_asset_path",
            "sha256",
            "crop",
        }:
            _fail(
                "media mapping fields are invalid",
                code="media_mapping_fields_invalid",
                section="media_provenance",
                field_path=f"$.media_provenance.asset_mappings[{index}]",
                consumer_effect="asset reuse and crop identity cannot be audited",
            )
        cue_id = str(mapping["cue_id"])
        asset_id = str(mapping["asset_id"])
        if cue_id in mapping_by_cue or cue_id not in cue_ids:
            _fail(
                "media mapping cue is duplicate or unknown",
                code="cue_media_binding_invalid",
                section="media_provenance",
                field_path=f"$.media_provenance.asset_mappings[{index}].cue_id",
                consumer_effect="one cue could receive multiple or no assets",
            )
        provenance_asset = provenance_assets.get(asset_id)
        manifest_cue = next(
            (row for row in manifest_cues if row.get("cue_id") == cue_id),
            None,
        )
        crop = mapping["crop"]
        crop_values = [float(value) for value in crop] if isinstance(crop, list) else []
        if (
            provenance_asset is None
            or manifest_cue is None
            or len(crop_values) != 4
            or any(value < 0 or value > 1 for value in crop_values)
            or crop_values[0] + crop_values[2] > 1
            or crop_values[1] + crop_values[3] > 1
            or mapping["source_id"] not in source_ids
            or provenance_asset.get("source_id") != mapping["source_id"]
            or provenance_asset.get("local_asset_path") != mapping["local_asset_path"]
            or provenance_asset.get("sha256") != mapping["sha256"]
            or cue_id not in provenance_asset.get("cue_ids", [])
            or manifest_cue.get("visual_id") != asset_id
            or manifest_cue.get("local_asset_path") != mapping["local_asset_path"]
            or manifest_cue.get("source_provenance_id") != mapping["source_id"]
            or [float(value) for value in manifest_cue.get("crop", [])] != crop_values
        ):
            _fail(
                f"cue media provenance binding is invalid: {cue_id}",
                code="cue_media_provenance_invalid",
                section="media_provenance",
                field_path=f"$.media_provenance.asset_mappings[{index}]",
                consumer_effect="asset reuse could lose source or crop identity",
            )
        view = next(
            (
                row
                for row in provenance_asset.get("cue_views", [])
                if row.get("cue_id") == cue_id
            ),
            None,
        )
        if view is None or [float(value) for value in view.get("crop", [])] != crop_values:
            _fail(
                f"provenance cue view is missing or drifted: {cue_id}",
                code="cue_provenance_view_missing",
                section="media_provenance",
                field_path=f"$.media_provenance.asset_mappings[{index}].crop",
                consumer_effect="materially different asset sections cannot be reproduced",
            )
        mapping_by_cue[cue_id] = mapping
        if asset_id not in availability_by_asset:
            availability_by_asset[asset_id] = _artifact_availability(
                repo_root,
                artifact_class=f"media_asset:{asset_id}",
                locator=mapping["local_asset_path"],
                expected_sha256=mapping["sha256"],
                check_live=check_live,
                contract_required=False,
                field_path=f"$.media_provenance.asset_mappings[{index}].local_asset_path",
            )
    if set(mapping_by_cue) != set(cue_ids):
        _fail(
            "cue media coverage is incomplete",
            code="cue_media_coverage_invalid",
            section="media_provenance",
            field_path="$.media_provenance.asset_mappings",
            consumer_effect="one or more cues lack provenance",
        )
    if (
        len(availability_by_asset) != int(shape["asset_count"])
        or len(provenance_assets) != int(shape["asset_count"])
    ):
        _fail(
            "asset count differs from unique provenance assets",
            code="asset_count_invalid",
            section="shape",
            field_path="$.shape.asset_count",
            consumer_effect="asset reuse versus cue count cannot be interpreted",
        )

    render_settings_sha = sha256_json(manifest.get("render_settings"))
    if render_settings_sha != episode["render_settings_sha256"]:
        _fail(
            "render settings hash differs from manifest",
            code="render_settings_hash_mismatch",
            section="episode_execution",
            field_path="$.episode_execution.render_settings_sha256",
            consumer_effect="render-on-change policy would compare the wrong settings",
        )
    identity_payload = build_v2_1_content_identity_payload(
        manifest=manifest,
        shape=shape,
        media_mappings=mappings,
        source_project=sections["source_project"],
        render_settings_sha256=render_settings_sha,
    )
    actual_content_identity = sha256_json(identity_payload)
    if actual_content_identity != sections["identities"]["content_identity_sha256"]:
        _fail(
            "pre-render content identity differs from protected authorities",
            code="content_identity_mismatch",
            section="identities",
            field_path="$.identities.content_identity_sha256",
            consumer_effect="queue deduplication and render-on-change would be nondeterministic",
        )
    authority_result = {
        "source_registry": source_registry,
        "claims": claims,
        "canonical": canonical,
        "provenance": provenance,
        "manifest": manifest,
        "content_identity_payload": identity_payload,
        "protected_inputs": protected_inputs,
    }
    return authority_result, list(availability_by_asset.values()), [
        dict(row) for row in mappings
    ]


def _validate_lifecycle_evidence(
    *,
    repo_root: Path,
    state: str,
    sections: Mapping[str, Mapping[str, Any]],
    check_live: bool,
) -> list[dict[str, Any]]:
    rank = LIFECYCLE_RANK[state]
    source_project = sections["source_project"]
    has_generated = "generated_project" in sections
    has_render = "render_validation" in sections
    has_human = "human_decision" in sections
    availability: list[dict[str, Any]] = []

    if rank == LIFECYCLE_RANK["package_prepared"]:
        if (
            source_project["state"] != "planned"
            or source_project["path"] is not None
            or source_project["sha256"] is not None
            or source_project["live_required_for_contract"] is not False
        ):
            _fail(
                "package_prepared source project must be planned with no identity",
                code="package_prepared_source_project_contradiction",
                section="source_project",
                field_path="$.source_project",
                consumer_effect="pre-render validation would fabricate source-project readiness",
            )
        if has_generated or has_render or has_human:
            _fail(
                "package_prepared must omit generated, render, and human evidence",
                code="package_prepared_advanced_evidence",
                section="lifecycle",
                field_path="$",
                consumer_effect="queue could mistake invented downstream evidence for readiness",
            )
        availability.extend(
            [
                {
                    "artifact_class": "source_project",
                    "locator": None,
                    "expected_sha256": None,
                    "contract_required": False,
                    "status": "planned_not_generated",
                    "actual_sha256": None,
                },
                {
                    "artifact_class": "generated_project",
                    "locator": None,
                    "expected_sha256": None,
                    "contract_required": False,
                    "status": "not_applicable_before_rendered",
                    "actual_sha256": None,
                },
                {
                    "artifact_class": "render_validation",
                    "locator": None,
                    "expected_sha256": None,
                    "contract_required": False,
                    "status": "not_applicable_before_rendered",
                    "actual_sha256": None,
                },
                {
                    "artifact_class": "human_decision",
                    "locator": None,
                    "expected_sha256": None,
                    "contract_required": False,
                    "status": "not_applicable_before_human_accepted",
                    "actual_sha256": None,
                },
            ]
        )
    else:
        if (
            source_project["state"] != "ready"
            or not isinstance(source_project["path"], str)
            or not isinstance(source_project["sha256"], str)
        ):
            _fail(
                "source_project_ready and later states require an exact source-project identity",
                code="source_project_identity_required",
                section="source_project",
                field_path="$.source_project",
                consumer_effect="project and render consumers cannot run",
            )
        availability.append(
            _artifact_availability(
                repo_root,
                artifact_class="source_project",
                locator=source_project["path"],
                expected_sha256=source_project["sha256"],
                check_live=check_live,
                contract_required=True,
                field_path="$.source_project.path",
            )
        )
        if rank == LIFECYCLE_RANK["source_project_ready"] and (
            has_generated or has_render or has_human
        ):
            _fail(
                "source_project_ready must omit generated, render, and human evidence",
                code="source_project_ready_advanced_evidence",
                section="lifecycle",
                field_path="$",
                consumer_effect="render or human readiness would be claimed too early",
            )

    if rank >= LIFECYCLE_RANK["rendered"]:
        if not has_generated:
            _fail(
                "rendered lifecycle requires generated-project identity",
                code="rendered_generated_project_required",
                section="generated_project",
                field_path="$.generated_project",
                consumer_effect="technical render cannot be tied to its project",
            )
        if not has_render:
            _fail(
                "rendered lifecycle requires technical receipt and MP4 identity",
                code="rendered_validation_required",
                section="render_validation",
                field_path="$.render_validation",
                consumer_effect="rendered consumer cannot establish a validated output",
            )
        generated = sections["generated_project"]
        render = sections["render_validation"]
        if render["technical_status"] != "passed":
            _fail(
                "rendered lifecycle requires passed technical validation",
                code="rendered_technical_status_invalid",
                section="render_validation",
                field_path="$.render_validation.technical_status",
                consumer_effect="failed output cannot satisfy rendered lifecycle",
            )
        _verify_bound_file(
            repo_root,
            render,
            section="render_validation",
            path_key="technical_receipt_path",
            hash_key="technical_receipt_sha256",
        )
        availability.extend(
            [
                _artifact_availability(
                    repo_root,
                    artifact_class="generated_project",
                    locator=generated["path"],
                    expected_sha256=generated["sha256"],
                    check_live=check_live,
                    contract_required=False,
                    field_path="$.generated_project.path",
                ),
                _artifact_availability(
                    repo_root,
                    artifact_class="render_validation",
                    locator=render["mp4_path"],
                    expected_sha256=render["mp4_sha256"],
                    check_live=check_live,
                    contract_required=False,
                    field_path="$.render_validation.mp4_path",
                ),
            ]
        )
    elif has_generated or has_render:
        _fail(
            "pre-render lifecycle carries rendered evidence",
            code="lifecycle_upgrade_contradiction",
            section="lifecycle",
            field_path="$",
            consumer_effect="render-on-change policy would skip required work",
        )

    if state == "human_accepted":
        if not has_human:
            _fail(
                "human_accepted lifecycle requires an exact decision receipt",
                code="human_acceptance_receipt_required",
                section="human_decision",
                field_path="$.human_decision",
                consumer_effect="human creative acceptance cannot be inferred",
            )
        human = sections["human_decision"]
        render = sections["render_validation"]
        if (
            human["state"] != "accepted_exact_artifact"
            or human["artifact_sha256"] != render["mp4_sha256"]
        ):
            _fail(
                "human decision does not bind the rendered artifact",
                code="human_acceptance_artifact_mismatch",
                section="human_decision",
                field_path="$.human_decision.artifact_sha256",
                consumer_effect="acceptance from another artifact could be inherited",
            )
        _verify_bound_file(
            repo_root,
            human,
            section="human_decision",
            path_key="receipt_path",
            hash_key="receipt_sha256",
        )
    elif has_human:
        _fail(
            "human decision evidence is forbidden before human_accepted",
            code="lifecycle_human_decision_contradiction",
            section="human_decision",
            field_path="$.human_decision",
            consumer_effect="creative acceptance would be claimed at an earlier state",
        )

    completed = sections["resume_identity"]["completed_run_observed"]
    if (
        rank < LIFECYCLE_RANK["rendered"]
        and completed is not False
        or rank >= LIFECYCLE_RANK["rendered"]
        and completed is not True
    ):
        _fail(
            "resume completed-run flag contradicts lifecycle",
            code="resume_lifecycle_contradiction",
            section="resume_identity",
            field_path="$.resume_identity.completed_run_observed",
            consumer_effect="resume consumer could treat an incomplete package as completed",
        )
    if sections["resume_identity"]["semantic_drift_fail_closed"] is not True:
        _fail(
            "semantic drift must fail closed",
            code="resume_drift_policy_invalid",
            section="resume_identity",
            field_path="$.resume_identity.semantic_drift_fail_closed",
            consumer_effect="render-on-change could reuse drifted output",
        )
    return availability


def _validate_factory_package_v2_1(
    *,
    repo_root: Path,
    descriptor_path: Path,
    payload: Mapping[str, Any],
    check_live: bool,
    require_lifecycle: str | None,
) -> dict[str, Any]:
    _validate_safe_tracked_payload(payload)
    sections = _validate_top_level(payload)
    _validate_extensions(sections["extensions"])
    _validate_content_identity(sections["identities"])
    _validate_authority_clocks(sections["authority"])
    _validate_contract_bindings(repo_root=repo_root, contract=sections["contract"])
    state = _validate_lifecycle_section(lifecycle=sections["lifecycle"])
    _validate_required_lifecycle(state, require_lifecycle)

    package = sections["package"]
    if (
        not isinstance(package["package_id"], str)
        or not package["package_id"]
        or not isinstance(package["episode_id"], str)
        or not package["episode_id"]
        or not isinstance(package["title"], str)
        or not package["title"]
    ):
        _fail(
            "package identity fields must be non-empty strings",
            code="package_identity_invalid",
            section="package",
            field_path="$.package",
            consumer_effect="queue item identity is ambiguous",
        )
    if sections["source_intake"]["source_backed"] is not True:
        _fail(
            "v2.1 package must declare source-backed intake",
            code="source_backed_required",
            section="source_intake",
            field_path="$.source_intake.source_backed",
            consumer_effect="claim and media authority would be absent",
        )
    lifecycle_availability = _validate_lifecycle_evidence(
        repo_root=repo_root,
        state=state,
        sections=sections,
        check_live=check_live,
    )
    authority_result, media_availability, media_mappings = (
        _validate_authorities_and_shape(
            repo_root=repo_root,
            sections=sections,
            check_live=check_live,
        )
    )
    descriptor_repo_path = descriptor_path.relative_to(repo_root.resolve()).as_posix()
    shape = sections["shape"]
    authority = sections["authority"]
    lifecycle = {
        "schema": "nlmytgen.factory_package.lifecycle.normalized.v2.1",
        "state": state,
        **LIFECYCLE_FLAGS[state],
    }
    return {
        "schema": VALIDATION_RESULT_SCHEMA,
        "status": "passed",
        "input_schema": FACTORY_PACKAGE_SCHEMA,
        "input_schema_version": FACTORY_PACKAGE_VERSION,
        "package_id": package["package_id"],
        "episode_id": package["episode_id"],
        "descriptor": {
            "path": descriptor_repo_path,
            "sha256": sha256_file(descriptor_path),
            "normalized_sha256": sha256_json(payload),
        },
        "contract": {
            "schema": FACTORY_PACKAGE_SCHEMA,
            "version": FACTORY_PACKAGE_VERSION,
            "json_schema_sha256": sections["contract"]["schema_sha256"],
            "field_inventory_sha256": sections["contract"][
                "field_inventory_sha256"
            ],
            "v2_0_schema_sha256": sections["contract"]["v2_0_schema_sha256"],
            "v2_0_field_inventory_sha256": sections["contract"][
                "v2_0_field_inventory_sha256"
            ],
            "conditional_requiredness": True,
        },
        "normalized_lifecycle": lifecycle,
        "normalized": {
            "lifecycle": state,
            "content_authority": package["content_authority"],
            "source_count": int(shape["source_count"]),
            "cue_count": int(shape["cue_count"]),
            "scene_count": int(shape["scene_count"]),
            "speaker_counts": dict(shape["speaker_counts"]),
            "timeline_frames": int(shape["timeline_frames"]),
            "fps": int(shape["fps"]),
            "duration_seconds": float(shape["duration_seconds"]),
            "timing_basis": shape["timing_basis"],
            "asset_count": int(shape["asset_count"]),
            "content_identity_sha256": sections["identities"][
                "content_identity_sha256"
            ],
            "episode_manifest_path": sections["episode_execution"][
                "manifest_path"
            ],
            "planned_run_id": sections["episode_execution"]["planned_run_id"],
            "human_decision": (
                sections["human_decision"]["state"]
                if "human_decision" in sections
                else "absent_before_human_accepted"
            ),
            "rights_approved": authority["rights"]["approved"],
            "production_approved": authority["production"]["approved"],
            "publication_approved": authority["publication"]["approved"],
            "upload_approved": authority["upload"]["approved"],
            "release_approved": authority["release"]["approved"],
        },
        "availability": media_availability + lifecycle_availability,
        "readiness": {
            **LIFECYCLE_FLAGS[state],
            "media_live_exact": all(
                row["status"] == "live_file_hash_exact"
                for row in media_availability
            ),
            "media_receipt_only": any(
                row["status"] == "receipt_only_no_live_file"
                for row in media_availability
            ),
        },
        "compatibility": {
            "adapter": "native_v2_1_lifecycle_validator",
            "v2_0_base_preserved": True,
            "source_descriptor_mutated": False,
        },
        "protected_inputs": authority_result["protected_inputs"],
        "media_mappings": media_mappings,
        "required_lifecycle": require_lifecycle,
        "boundaries": {
            "tracked_contract_valid_without_live_media": True,
            "live_hashes_checked": check_live,
            "network_access": False,
            "source_project_generated": False,
            "generated_project_created": False,
            "yymm4_launched": False,
            "electron_launched": False,
            "render_driver_launched": False,
            "ffmpeg_encode_performed": False,
            "media_playback": False,
            "artifacts_mutated": False,
            "universal_arbitrary_topic_compatibility": False,
        },
    }


def validate_factory_package_lifecycle(
    *,
    repo_root: Path,
    descriptor_path: Path,
    check_live: bool = False,
    require_lifecycle: str | None = None,
) -> dict[str, Any]:
    """Validate v2.0 or v2.1 and return one lifecycle-aware result."""

    root = repo_root.resolve()
    path = _descriptor_path(root, descriptor_path)
    payload = _load_json(path, section="root", field_path="$")
    schema = payload.get("schema")
    if schema == FACTORY_PACKAGE_V2_SCHEMA:
        result = validate_factory_package_v2(
            repo_root=root,
            descriptor_path=path,
            check_live=check_live,
        )
        return _normalize_v2_0_result(
            payload=payload,
            result=result,
            require_lifecycle=require_lifecycle,
        )
    if schema == FACTORY_PACKAGE_SCHEMA:
        return _validate_factory_package_v2_1(
            repo_root=root,
            descriptor_path=path,
            payload=payload,
            check_live=check_live,
            require_lifecycle=require_lifecycle,
        )
    _fail(
        "Factory Package schema is unsupported",
        code="factory_package_schema_invalid",
        section="root",
        field_path="$.schema",
        consumer_effect="validator cannot select v2.0 compatibility or v2.1 lifecycle rules",
    )
    raise AssertionError("unreachable")


def build_pre_render_stage_plan(
    *,
    repo_root: Path,
    descriptor_path: Path,
    validation_result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a write-free plan that stops before source-project generation."""

    result = (
        dict(validation_result)
        if validation_result is not None
        else validate_factory_package_lifecycle(
            repo_root=repo_root,
            descriptor_path=descriptor_path,
            check_live=True,
        )
    )
    if result.get("input_schema") != FACTORY_PACKAGE_SCHEMA:
        _fail(
            "pre-render stage planning requires a native v2.1 descriptor",
            code="pre_render_plan_schema_invalid",
            section="lifecycle",
            field_path="$.schema",
            consumer_effect="completed v2.0 packages must continue through the existing pipeline",
        )
    lifecycle = result["normalized_lifecycle"]
    if LIFECYCLE_RANK[lifecycle["state"]] >= LIFECYCLE_RANK["rendered"]:
        _fail(
            "pre-render stage plan is not used for rendered packages",
            code="pre_render_plan_lifecycle_invalid",
            section="lifecycle",
            field_path="$.lifecycle.state",
            consumer_effect="rendered packages should use the existing video dry-run",
        )
    media_rows = [
        row
        for row in result["availability"]
        if str(row["artifact_class"]).startswith("media_asset:")
    ]
    media_live_exact = all(
        row["status"] == "live_file_hash_exact" for row in media_rows
    )
    return {
        "schema": STAGE_PLAN_SCHEMA,
        "status": "pre_render_plan_complete",
        "completed_video_dry_run": False,
        "package_id": result["package_id"],
        "episode_id": result["episode_id"],
        "input_schema": result["input_schema"],
        "input_schema_version": result["input_schema_version"],
        "lifecycle": lifecycle,
        "content_identity_sha256": result["normalized"][
            "content_identity_sha256"
        ],
        "protected_inputs": {
            "count": len(result["protected_inputs"]),
            "exact": all(
                row.get("status") == "passed" for row in result["protected_inputs"]
            ),
        },
        "stages": [
            {
                "stage": "package_validation",
                "ready": True,
                "executed": True,
                "mode": "read_only",
            },
            {
                "stage": "source_project",
                "ready": lifecycle["source_project_ready"],
                "executed": False,
                "planned": True,
                "authorization": False,
            },
            {
                "stage": "media_materialization",
                "ready": False,
                "inputs_live_exact": media_live_exact,
                "executed": False,
                "authorization": False,
            },
            {
                "stage": "generated_project",
                "ready": False,
                "executed": False,
                "authorization": False,
            },
            {
                "stage": "render",
                "ready": False,
                "executed": False,
                "authorization": False,
            },
            {
                "stage": "technical_validation",
                "ready": False,
                "executed": False,
                "authorization": False,
            },
        ],
        "stop": {
            "successful": True,
            "before_stage": "source_project_generation",
            "reason": "package_prepared contract is valid; source-project and render authority are absent",
        },
        "launch_counts": {
            "yymm4": 0,
            "electron": 0,
            "render_driver": 0,
            "ffmpeg_encode": 0,
            "playback": 0,
        },
        "writes": {
            "tracked": False,
            "source_project": False,
            "generated_project": False,
            "rendered_media": False,
            "private_product_artifact": False,
        },
        "availability": result["availability"],
        "boundaries": {
            "network_access": False,
            "system_volume_operation": False,
            "human_review": False,
            "rights_approval": False,
            "production": False,
            "publication": False,
            "upload": False,
            "release": False,
        },
    }


__all__ = [
    "FACTORY_PACKAGE_SCHEMA",
    "FACTORY_PACKAGE_VERSION",
    "FactoryContractError",
    "LIFECYCLE_ORDER",
    "build_pre_render_stage_plan",
    "build_v2_1_content_identity_payload",
    "canonical_json_bytes",
    "validate_factory_package_lifecycle",
]
