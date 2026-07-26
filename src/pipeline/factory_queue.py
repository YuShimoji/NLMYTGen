"""Bounded, deterministic planning for mixed Factory Contract v2 packages."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

from src.pipeline.factory_contract_v2_1 import (
    FactoryContractError,
    build_pre_render_stage_plan,
    validate_factory_package_lifecycle,
)


FACTORY_QUEUE_SCHEMA = "nlmytgen.factory_queue.v1"
FACTORY_QUEUE_VERSION = "1.0"
FACTORY_QUEUE_RESULT_SCHEMA = "nlmytgen.factory_queue_evaluation.v1"
FACTORY_QUEUE_SAFE_STAGE_SCHEMA = "nlmytgen.factory_queue_safe_stage_result.v1"
FACTORY_QUEUE_HARD_MAXIMUM = 32

TECHNICAL_DECISIONS = (
    "verified_noop",
    "recorded_complete_no_live_file",
    "source_project_generation_required",
    "render_required",
    "human_review_required",
    "blocked_contract",
    "blocked_identity_drift",
    "blocked_corrupt_output",
    "blocked_authority",
)

RUN_LOCAL_FIELDS = frozenset(
    {
        "run_id",
        "timestamp",
        "pid",
        "elapsed_time",
        "local_directory",
        "machine_path",
    }
)

_TOP_LEVEL_FIELDS = frozenset(
    {
        "schema",
        "schema_version",
        "contract",
        "queue",
        "evaluation_policy",
        "execution_authority_policy",
        "receipt_policy",
    }
)
_CONTRACT_FIELDS = frozenset({"schema", "schema_path", "schema_sha256"})
_QUEUE_FIELDS = frozenset(
    {"schema", "queue_id", "maximum_queue_size", "packages"}
)
_ENTRY_FIELDS = frozenset(
    {
        "order",
        "priority",
        "descriptor_path",
        "expected_package_id",
        "expected_content_identity_sha256",
        "expected_render_settings_sha256",
        "expected_completed_output_sha256",
        "immutable_artifact_reference",
    }
)
_EVALUATION_FIELDS = frozenset(
    {
        "schema",
        "ordering",
        "duplicate_package_id",
        "duplicate_content_identity",
        "target_collision",
        "render_on_change",
        "run_local_fields_excluded",
    }
)
_EXECUTION_FIELDS = frozenset(
    {
        "schema",
        "plan_only_default",
        "safe_stages_only",
        "source_project_generation_authorized",
        "render_authorized",
        "human_review_authorized",
        "private_artifact_copy_authorized",
    }
)
_RECEIPT_FIELDS = frozenset(
    {
        "schema",
        "output_mode",
        "deterministic_fields_only",
        "include_usernames",
        "include_drive_letters",
        "include_private_absolute_paths",
        "include_credentials",
        "include_process_command_lines",
        "include_private_media",
    }
)

_IDENTITY_DRIFT_CODES = frozenset(
    {
        "bound_authority_hash_mismatch",
        "content_identity_mismatch",
        "content_identity_polluted",
        "protected_input_hash_mismatch",
        "render_settings_hash_mismatch",
        "render_settings_identity_mismatch",
    }
)


class FactoryQueueError(ValueError):
    """A sanitized, consumer-aware queue contract failure."""

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
            "schema": FACTORY_QUEUE_RESULT_SCHEMA,
            "status": "failed",
            "error_code": self.code,
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


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _fail(
    message: str,
    *,
    code: str,
    field_path: str,
    consumer_effect: str,
) -> None:
    raise FactoryQueueError(
        message,
        code=code,
        field_path=field_path,
        consumer_effect=consumer_effect,
    )


def _require_mapping(
    value: Any,
    *,
    field_path: str,
    required: frozenset[str],
    allowed: frozenset[str],
) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail(
            "queue section must be an object",
            code="queue_section_type_invalid",
            field_path=field_path,
            consumer_effect="queue policy cannot be evaluated deterministically",
        )
    keys = frozenset(str(key) for key in value)
    missing = sorted(required - keys)
    unknown = sorted(keys - allowed)
    if missing or unknown:
        _fail(
            "queue section fields do not match the versioned schema",
            code="queue_section_fields_invalid",
            field_path=field_path,
            consumer_effect=(
                "missing or unknown fields would make queue behavior ambiguous"
            ),
        )
    return value


def _load_json(path: Path, *, field_path: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FactoryQueueError(
            "queue JSON is unavailable or malformed",
            code="queue_json_unreadable",
            field_path=field_path,
            consumer_effect="queue evaluation cannot start",
        ) from exc
    if not isinstance(value, dict):
        _fail(
            "queue JSON root must be an object",
            code="queue_root_type_invalid",
            field_path=field_path,
            consumer_effect="queue evaluation cannot select a versioned contract",
        )
    return value


def _repo_locator(
    repo_root: Path,
    value: Any,
    *,
    field_path: str,
    require_file: bool = True,
) -> tuple[str, Path]:
    if not isinstance(value, str) or not value:
        _fail(
            "queue locator must be a non-empty repository-relative string",
            code="queue_locator_invalid",
            field_path=field_path,
            consumer_effect="queue input cannot be resolved safely",
        )
    if "\\" in value or ":" in value:
        _fail(
            "queue locator must use a repository-relative POSIX path",
            code="queue_locator_private_or_absolute",
            field_path=field_path,
            consumer_effect="private or machine-local paths cannot enter a queue receipt",
        )
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        _fail(
            "queue locator escapes the repository boundary",
            code="queue_locator_escape",
            field_path=field_path,
            consumer_effect="queue input cannot be resolved safely",
        )
    root = repo_root.resolve()
    resolved = (root / Path(*pure.parts)).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        _fail(
            "queue locator escapes the repository boundary",
            code="queue_locator_escape",
            field_path=field_path,
            consumer_effect="queue input cannot be resolved safely",
        )
    if require_file and not resolved.is_file():
        _fail(
            "queue locator does not identify a tracked input file",
            code="queue_locator_unavailable",
            field_path=field_path,
            consumer_effect="queue input cannot be validated",
        )
    return pure.as_posix(), resolved


def _require_exact(value: Any, expected: Any, *, field_path: str) -> None:
    if value != expected:
        _fail(
            "queue policy differs from the supported v1 contract",
            code="queue_policy_invalid",
            field_path=field_path,
            consumer_effect="queue behavior would no longer be bounded or deterministic",
        )


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def _validate_queue_descriptor(
    *,
    repo_root: Path,
    queue_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    root = repo_root.resolve()
    relative_queue, resolved_queue = _repo_locator(
        root,
        queue_path.as_posix(),
        field_path="$.queue_descriptor",
    )
    payload = _load_json(resolved_queue, field_path="$")
    _require_mapping(
        payload,
        field_path="$",
        required=_TOP_LEVEL_FIELDS,
        allowed=_TOP_LEVEL_FIELDS,
    )
    _require_exact(payload["schema"], FACTORY_QUEUE_SCHEMA, field_path="$.schema")
    _require_exact(
        payload["schema_version"],
        FACTORY_QUEUE_VERSION,
        field_path="$.schema_version",
    )

    contract = _require_mapping(
        payload["contract"],
        field_path="$.contract",
        required=_CONTRACT_FIELDS,
        allowed=_CONTRACT_FIELDS,
    )
    _require_exact(
        contract["schema"],
        "nlmytgen.factory_queue.contract.v1",
        field_path="$.contract.schema",
    )
    schema_relative, schema_path = _repo_locator(
        root,
        contract["schema_path"],
        field_path="$.contract.schema_path",
    )
    if schema_relative != "schemas/factory_queue_v1/factory_queue_v1.schema.json":
        _fail(
            "queue schema locator is not the v1 authority",
            code="queue_schema_locator_invalid",
            field_path="$.contract.schema_path",
            consumer_effect="queue fields cannot be interpreted against one authority",
        )
    schema_sha = sha256_file(schema_path)
    if contract["schema_sha256"] != schema_sha:
        _fail(
            "queue schema identity does not match the bound authority",
            code="queue_schema_hash_mismatch",
            field_path="$.contract.schema_sha256",
            consumer_effect="queue contract drift must fail before package evaluation",
        )
    schema_payload = _load_json(schema_path, field_path="$.contract.schema_path")
    if schema_payload.get("$id") != FACTORY_QUEUE_SCHEMA:
        _fail(
            "queue schema authority declares an unsupported identity",
            code="queue_schema_identity_invalid",
            field_path="$.contract.schema_path",
            consumer_effect="queue contract version cannot be established",
        )

    queue = _require_mapping(
        payload["queue"],
        field_path="$.queue",
        required=_QUEUE_FIELDS,
        allowed=_QUEUE_FIELDS,
    )
    _require_exact(
        queue["schema"],
        "nlmytgen.factory_queue.entries.v1",
        field_path="$.queue.schema",
    )
    queue_id = queue["queue_id"]
    if (
        not isinstance(queue_id, str)
        or not queue_id
        or len(queue_id) > 96
        or not all(char.islower() or char.isdigit() or char in "_-" for char in queue_id)
    ):
        _fail(
            "queue ID is invalid",
            code="queue_id_invalid",
            field_path="$.queue.queue_id",
            consumer_effect="queue receipt identity would be unstable",
        )
    maximum = queue["maximum_queue_size"]
    if (
        isinstance(maximum, bool)
        or not isinstance(maximum, int)
        or not 1 <= maximum <= FACTORY_QUEUE_HARD_MAXIMUM
    ):
        _fail(
            "maximum queue size must be a finite integer within the hard cap",
            code="queue_maximum_invalid",
            field_path="$.queue.maximum_queue_size",
            consumer_effect="queue intake would be unbounded",
        )
    packages = queue["packages"]
    if not isinstance(packages, list) or not packages:
        _fail(
            "queue packages must be a non-empty list",
            code="queue_packages_invalid",
            field_path="$.queue.packages",
            consumer_effect="queue evaluation has no bounded inputs",
        )
    if len(packages) > maximum or len(packages) > FACTORY_QUEUE_HARD_MAXIMUM:
        _fail(
            "queue package count exceeds the declared or hard maximum",
            code="queue_maximum_exceeded",
            field_path="$.queue.packages",
            consumer_effect="queue intake must stop before package validation",
        )

    normalized_entries: list[dict[str, Any]] = []
    orders: list[int] = []
    descriptor_locators: set[str] = set()
    for index, raw_entry in enumerate(packages):
        field_path = f"$.queue.packages[{index}]"
        entry = _require_mapping(
            raw_entry,
            field_path=field_path,
            required=frozenset(
                {
                    "order",
                    "descriptor_path",
                    "expected_package_id",
                    "expected_content_identity_sha256",
                    "expected_render_settings_sha256",
                    "expected_completed_output_sha256",
                }
            ),
            allowed=_ENTRY_FIELDS,
        )
        order = entry["order"]
        priority = entry.get("priority", 0)
        if (
            isinstance(order, bool)
            or not isinstance(order, int)
            or not 1 <= order <= FACTORY_QUEUE_HARD_MAXIMUM
        ):
            _fail(
                "queue entry order is invalid",
                code="queue_order_invalid",
                field_path=f"{field_path}.order",
                consumer_effect="queue ordering would not be stable",
            )
        if (
            isinstance(priority, bool)
            or not isinstance(priority, int)
            or not 0 <= priority <= 100
        ):
            _fail(
                "queue priority must be an integer from 0 through 100",
                code="queue_priority_invalid",
                field_path=f"{field_path}.priority",
                consumer_effect="queue ordering would not be bounded",
            )
        locator, descriptor_path = _repo_locator(
            root,
            entry["descriptor_path"],
            field_path=f"{field_path}.descriptor_path",
        )
        if locator in descriptor_locators:
            _fail(
                "the same descriptor locator appears more than once",
                code="queue_descriptor_duplicate",
                field_path=f"{field_path}.descriptor_path",
                consumer_effect="one package could be evaluated or scheduled twice",
            )
        descriptor_locators.add(locator)
        expected_package_id = entry["expected_package_id"]
        if (
            not isinstance(expected_package_id, str)
            or not expected_package_id
            or len(expected_package_id) > 128
            or not all(
                char.islower() or char.isdigit() or char in "_-"
                for char in expected_package_id
            )
        ):
            _fail(
                "expected package ID is invalid",
                code="queue_expected_package_id_invalid",
                field_path=f"{field_path}.expected_package_id",
                consumer_effect="queue identity baseline cannot be established",
            )
        for identity_field in (
            "expected_content_identity_sha256",
            "expected_render_settings_sha256",
        ):
            if not _is_sha256(entry[identity_field]):
                _fail(
                    "expected semantic identity is invalid",
                    code="queue_expected_identity_invalid",
                    field_path=f"{field_path}.{identity_field}",
                    consumer_effect="render-on-change comparison cannot be performed",
                )
        expected_output = entry["expected_completed_output_sha256"]
        if expected_output is not None and not _is_sha256(expected_output):
            _fail(
                "expected completed output identity is invalid",
                code="queue_expected_output_identity_invalid",
                field_path=f"{field_path}.expected_completed_output_sha256",
                consumer_effect="completed output drift cannot be detected",
            )
        immutable_reference = entry.get("immutable_artifact_reference")
        if immutable_reference is not None and (
            not isinstance(immutable_reference, str)
            or not immutable_reference
            or len(immutable_reference) > 128
            or not all(
                char.islower() or char.isdigit() or char in "_.-"
                for char in immutable_reference
            )
        ):
            _fail(
                "immutable artifact reference is invalid",
                code="queue_immutable_reference_invalid",
                field_path=f"{field_path}.immutable_artifact_reference",
                consumer_effect="duplicate content identity cannot be adjudicated",
            )
        orders.append(order)
        normalized_entries.append(
            {
                "declared_index": index,
                "order": order,
                "priority": priority,
                "descriptor_path": locator,
                "resolved_descriptor_path": descriptor_path,
                "expected_package_id": expected_package_id,
                "expected_content_identity_sha256": entry[
                    "expected_content_identity_sha256"
                ],
                "expected_render_settings_sha256": entry[
                    "expected_render_settings_sha256"
                ],
                "expected_completed_output_sha256": expected_output,
                "immutable_artifact_reference": immutable_reference,
            }
        )
    if sorted(orders) != list(range(1, len(packages) + 1)):
        _fail(
            "queue order values must be unique and contiguous from one",
            code="queue_order_unstable",
            field_path="$.queue.packages[*].order",
            consumer_effect="equivalent queue inputs could produce different plans",
        )

    evaluation = _require_mapping(
        payload["evaluation_policy"],
        field_path="$.evaluation_policy",
        required=_EVALUATION_FIELDS,
        allowed=_EVALUATION_FIELDS,
    )
    expected_evaluation = {
        "schema": "nlmytgen.factory_queue.evaluation_policy.v1",
        "ordering": "priority_descending_then_order_ascending",
        "duplicate_package_id": "reject",
        "duplicate_content_identity": (
            "reject_unless_same_immutable_artifact_reference"
        ),
        "target_collision": "reject",
        "render_on_change": "plan_only_never_overwrite_completed_artifact",
    }
    for key, expected in expected_evaluation.items():
        _require_exact(
            evaluation[key],
            expected,
            field_path=f"$.evaluation_policy.{key}",
        )
    exclusions = evaluation["run_local_fields_excluded"]
    if (
        not isinstance(exclusions, list)
        or len(exclusions) != len(RUN_LOCAL_FIELDS)
        or set(exclusions) != RUN_LOCAL_FIELDS
    ):
        _fail(
            "run-local exclusion set must be exact",
            code="queue_run_local_policy_invalid",
            field_path="$.evaluation_policy.run_local_fields_excluded",
            consumer_effect="run-local metadata could trigger a false semantic change",
        )

    execution = _require_mapping(
        payload["execution_authority_policy"],
        field_path="$.execution_authority_policy",
        required=_EXECUTION_FIELDS,
        allowed=_EXECUTION_FIELDS,
    )
    expected_execution = {
        "schema": "nlmytgen.factory_queue.execution_authority.v1",
        "plan_only_default": True,
        "safe_stages_only": True,
        "source_project_generation_authorized": False,
        "render_authorized": False,
        "human_review_authorized": False,
        "private_artifact_copy_authorized": False,
    }
    for key, expected in expected_execution.items():
        _require_exact(
            execution[key],
            expected,
            field_path=f"$.execution_authority_policy.{key}",
        )

    receipt = _require_mapping(
        payload["receipt_policy"],
        field_path="$.receipt_policy",
        required=_RECEIPT_FIELDS,
        allowed=_RECEIPT_FIELDS,
    )
    expected_receipt = {
        "schema": "nlmytgen.factory_queue.receipt_policy.v1",
        "output_mode": "sanitized_stdout",
        "deterministic_fields_only": True,
        "include_usernames": False,
        "include_drive_letters": False,
        "include_private_absolute_paths": False,
        "include_credentials": False,
        "include_process_command_lines": False,
        "include_private_media": False,
    }
    for key, expected in expected_receipt.items():
        _require_exact(
            receipt[key],
            expected,
            field_path=f"$.receipt_policy.{key}",
        )

    normalized_entries.sort(key=lambda row: (-row["priority"], row["order"]))
    normalized = {
        "queue_id": queue_id,
        "maximum_queue_size": maximum,
        "packages": normalized_entries,
        "execution_authority_policy": dict(execution),
        "receipt_policy": dict(receipt),
    }
    identity = {
        "path": relative_queue,
        "sha256": sha256_file(resolved_queue),
        "schema_path": schema_relative,
        "schema_sha256": schema_sha,
    }
    return normalized, identity


def decide_render_on_change(
    *,
    lifecycle: str,
    live_output_status: str,
    semantic_identity_match: bool,
    render_settings_match: bool,
    output_corrupt: bool,
    source_project_available: bool,
    run_local_only_change: bool = False,
) -> tuple[str, list[str]]:
    """Return one technical decision without performing any side effect."""

    reasons: list[str] = []
    if run_local_only_change:
        reasons.append("run_local_change_ignored")
    if not semantic_identity_match or not render_settings_match:
        return "blocked_identity_drift", [
            *reasons,
            "semantic_or_render_settings_identity_changed",
        ]
    if output_corrupt:
        return "blocked_corrupt_output", [
            *reasons,
            "completed_output_hash_or_structure_invalid",
        ]
    if lifecycle in {"human_accepted", "rendered"}:
        if live_output_status == "live_file_hash_exact":
            return "verified_noop", [*reasons, "completed_output_live_exact"]
        if live_output_status in {
            "receipt_only_no_live_file",
            "not_checked",
        }:
            return "recorded_complete_no_live_file", [
                *reasons,
                (
                    "completed_identity_recorded_live_file_absent"
                    if live_output_status == "receipt_only_no_live_file"
                    else "completed_identity_recorded_live_file_not_checked"
                ),
            ]
        return "blocked_corrupt_output", [
            *reasons,
            "completed_output_availability_contradiction",
        ]
    if lifecycle == "source_project_ready":
        if live_output_status == "live_file_hash_exact":
            return "verified_noop", [
                *reasons,
                "completed_output_live_exact",
            ]
        return "render_required", [
            *reasons,
            (
                "source_project_live_exact_no_valid_render"
                if source_project_available
                else "source_project_identity_recorded_live_file_unavailable"
            ),
        ]
    if lifecycle == "package_prepared":
        return "source_project_generation_required", [
            *reasons,
            "source_project_planned_not_generated",
        ]
    return "blocked_contract", [*reasons, "unsupported_lifecycle"]


def _raw_package_id(payload: Mapping[str, Any]) -> str | None:
    package = payload.get("package")
    if isinstance(package, Mapping):
        value = package.get("package_id")
        if isinstance(value, str):
            return value
    return None


def _raw_lifecycle(payload: Mapping[str, Any]) -> str | None:
    lifecycle = payload.get("lifecycle")
    if isinstance(lifecycle, Mapping) and isinstance(lifecycle.get("state"), str):
        return str(lifecycle["state"])
    if payload.get("schema") == "nlmytgen.factory_package.v2":
        human = payload.get("human_decision")
        if isinstance(human, Mapping):
            return (
                "human_accepted"
                if human.get("state") == "accepted_exact_artifact"
                else "rendered"
            )
    return None


def _raw_content_identity(payload: Mapping[str, Any]) -> str | None:
    identities = payload.get("identities")
    if isinstance(identities, Mapping):
        value = identities.get("content_identity_sha256")
        if isinstance(value, str):
            return value
    return None


def _render_settings_identity(payload: Mapping[str, Any]) -> str | None:
    episode = payload.get("episode_execution")
    if isinstance(episode, Mapping):
        value = episode.get("render_settings_sha256")
        if isinstance(value, str):
            return value
    return None


def _completed_output_identity(payload: Mapping[str, Any]) -> str | None:
    render = payload.get("render_validation")
    if isinstance(render, Mapping):
        value = render.get("mp4_sha256")
        if isinstance(value, str):
            return value
    return None


def _target_identity(payload: Mapping[str, Any]) -> tuple[str, str] | None:
    episode = payload.get("episode_execution")
    if not isinstance(episode, Mapping):
        return None
    run_id = episode.get("run_id", episode.get("planned_run_id"))
    mp4 = episode.get("mp4_filename")
    if isinstance(run_id, str) and isinstance(mp4, str):
        return run_id, mp4
    return None


def _availability_status(
    availability: Sequence[Mapping[str, Any]],
    artifact_class: str,
) -> str | None:
    for row in availability:
        if row.get("artifact_class") == artifact_class:
            value = row.get("status")
            return str(value) if value is not None else None
    return None


def _live_availability_summary(
    *,
    lifecycle: str,
    availability: Sequence[Mapping[str, Any]],
    check_live: bool,
) -> str:
    if not check_live:
        return "not_checked"
    if lifecycle in {"human_accepted", "rendered"}:
        status = _availability_status(availability, "render_validation")
        return (
            "live_exact"
            if status == "live_file_hash_exact"
            else "recorded_only"
        )
    if lifecycle == "source_project_ready":
        status = _availability_status(availability, "source_project")
        return (
            "source_project_live_exact"
            if status == "live_file_hash_exact"
            else "source_project_recorded_only"
        )
    media = [
        row
        for row in availability
        if str(row.get("artifact_class", "")).startswith("media_asset:")
    ]
    if media and all(row.get("status") == "live_file_hash_exact" for row in media):
        return "prepared_inputs_live_exact"
    return "prepared_inputs_recorded_only"


def _external_authority(
    validation: Mapping[str, Any],
    execution_policy: Mapping[str, Any],
) -> dict[str, Any]:
    normalized = validation["normalized"]
    lifecycle = validation["normalized_lifecycle"]
    return {
        "human_accepted": bool(lifecycle.get("human_accepted")),
        "rights_approved": bool(normalized.get("rights_approved", False)),
        "production_approved": bool(
            normalized.get("production_approved", False)
        ),
        "publication_approved": bool(
            normalized.get("publication_approved", False)
        ),
        "upload_approved": bool(normalized.get("upload_approved", False)),
        "release_approved": bool(normalized.get("release_approved", False)),
        "source_project_generation_authorized": bool(
            execution_policy["source_project_generation_authorized"]
        ),
        "render_authorized": bool(execution_policy["render_authorized"]),
        "human_review_authorized": bool(
            execution_policy["human_review_authorized"]
        ),
    }


def _package_error_row(
    *,
    entry: Mapping[str, Any],
    payload: Mapping[str, Any],
    error: FactoryContractError,
    decision: str,
) -> dict[str, Any]:
    return {
        "order": entry["order"],
        "priority": entry["priority"],
        "descriptor_path": entry["descriptor_path"],
        "descriptor_sha256": sha256_file(entry["resolved_descriptor_path"]),
        "package_id": _raw_package_id(payload),
        "input_schema": payload.get("schema"),
        "normalized_lifecycle": _raw_lifecycle(payload),
        "contract_valid": False,
        "content_identity_sha256": _raw_content_identity(payload),
        "render_settings_identity_sha256": _render_settings_identity(payload),
        "live_availability": "not_evaluated",
        "recorded_identity_available": bool(_raw_content_identity(payload)),
        "semantic_drift_state": (
            "detected" if decision == "blocked_identity_drift" else "not_evaluated"
        ),
        "technical_next_stage": None,
        "technical_decision": decision,
        "external_authority": None,
        "execution_eligible": False,
        "execution_gate_decision": "not_applicable",
        "reason_codes": [error.code],
        "contract_error": {
            "error_code": error.code,
            "section": error.section,
            "field_path": error.field_path,
            "consumer_effect": error.consumer_effect,
        },
        "target_identity_sha256": None,
    }


def _classify_contract_error(error: FactoryContractError) -> str:
    if error.code in _IDENTITY_DRIFT_CODES:
        return "blocked_identity_drift"
    if error.code == "live_artifact_hash_mismatch":
        if error.field_path.startswith(
            ("$.render_validation", "$.generated_project")
        ):
            return "blocked_corrupt_output"
        return "blocked_identity_drift"
    return "blocked_contract"


def evaluate_factory_queue(
    *,
    repo_root: Path,
    queue_path: Path,
    check_live: bool = False,
) -> dict[str, Any]:
    """Evaluate a bounded queue without writes, launches, or execution authority."""

    root = repo_root.resolve()
    normalized_queue, queue_identity = _validate_queue_descriptor(
        repo_root=root,
        queue_path=queue_path,
    )
    execution_policy = normalized_queue["execution_authority_policy"]
    rows: list[dict[str, Any]] = []
    package_ids: dict[str, int] = {}
    content_identities: dict[str, list[tuple[int, str | None]]] = {}
    targets: dict[tuple[str, str], int] = {}

    for entry in normalized_queue["packages"]:
        payload = _load_json(
            entry["resolved_descriptor_path"],
            field_path=f"$.queue.packages[{entry['declared_index']}].descriptor_path",
        )
        try:
            baseline = validate_factory_package_lifecycle(
                repo_root=root,
                descriptor_path=entry["resolved_descriptor_path"],
                check_live=False,
            )
        except FactoryContractError as exc:
            rows.append(
                _package_error_row(
                    entry=entry,
                    payload=payload,
                    error=exc,
                    decision=_classify_contract_error(exc),
                )
            )
            continue

        validation = baseline
        live_error: FactoryContractError | None = None
        if check_live:
            try:
                validation = validate_factory_package_lifecycle(
                    repo_root=root,
                    descriptor_path=entry["resolved_descriptor_path"],
                    check_live=True,
                )
            except FactoryContractError as exc:
                live_error = exc

        package_id = str(baseline["package_id"])
        content_identity = str(
            baseline["normalized"]["content_identity_sha256"]
        )
        if package_id in package_ids:
            _fail(
                "queue contains a duplicate package ID",
                code="queue_duplicate_package_id",
                field_path=f"$.queue.packages[{entry['declared_index']}]",
                consumer_effect="one logical package could receive multiple stage decisions",
            )
        package_ids[package_id] = entry["order"]
        content_identities.setdefault(content_identity, []).append(
            (entry["order"], entry["immutable_artifact_reference"])
        )
        target = _target_identity(payload)
        if target is not None:
            if target in targets:
                _fail(
                    "queue contains an output target collision",
                    code="queue_target_collision",
                    field_path=f"$.queue.packages[{entry['declared_index']}]",
                    consumer_effect="two packages could address the same run-local output",
                )
            targets[target] = entry["order"]

        lifecycle = str(baseline["normalized_lifecycle"]["state"])
        availability = list(validation["availability"])
        package_identity_match = package_id == entry["expected_package_id"]
        semantic_match = (
            content_identity == entry["expected_content_identity_sha256"]
        )
        render_settings_match = (
            _render_settings_identity(payload)
            == entry["expected_render_settings_sha256"]
        )
        completed_output_match = (
            _completed_output_identity(payload)
            == entry["expected_completed_output_sha256"]
        )
        output_corrupt = False
        live_error_decision: str | None = None
        if live_error is not None:
            live_error_decision = _classify_contract_error(live_error)
            semantic_match = (
                semantic_match
                and live_error_decision != "blocked_identity_drift"
            )
            output_corrupt = live_error_decision == "blocked_corrupt_output"

        render_status = (
            _availability_status(availability, "render_validation")
            if check_live
            else "not_checked"
        ) or "unavailable"
        source_status = _availability_status(availability, "source_project")
        source_available = source_status == "live_file_hash_exact"
        decision, reasons = decide_render_on_change(
            lifecycle=lifecycle,
            live_output_status=render_status,
            semantic_identity_match=semantic_match,
            render_settings_match=render_settings_match,
            output_corrupt=output_corrupt,
            source_project_available=source_available,
        )
        if not package_identity_match:
            decision = "blocked_contract"
            reasons = ["expected_package_id_mismatch"]
        elif not completed_output_match:
            decision = "blocked_identity_drift"
            reasons = ["expected_completed_output_identity_changed"]
        if live_error_decision is not None:
            decision = live_error_decision
            reasons = [live_error.code]

        technical_next_stage = {
            "source_project_generation_required": "source_project_generation",
            "render_required": "render",
            "human_review_required": "human_review",
        }.get(decision)
        action_authorized = {
            "source_project_generation_required": bool(
                execution_policy["source_project_generation_authorized"]
            ),
            "render_required": bool(execution_policy["render_authorized"]),
            "human_review_required": bool(
                execution_policy["human_review_authorized"]
            ),
        }.get(decision, False)
        action_decision = decision in {
            "source_project_generation_required",
            "render_required",
            "human_review_required",
        }
        execution_gate = (
            "eligible"
            if action_decision and action_authorized
            else "blocked_authority"
            if action_decision
            else "not_applicable"
        )
        if action_decision and not action_authorized:
            reasons = [*reasons, "execution_authority_absent"]

        recorded = {
            "content_identity": True,
            "render_settings_identity": bool(_render_settings_identity(payload)),
            "source_project_identity": bool(
                isinstance(payload.get("source_project"), Mapping)
                and payload["source_project"].get("sha256")
            ),
            "completed_output_identity": bool(
                isinstance(payload.get("render_validation"), Mapping)
                and payload["render_validation"].get("mp4_sha256")
            ),
            "human_decision_identity": bool(
                isinstance(payload.get("human_decision"), Mapping)
                and payload["human_decision"].get("receipt_sha256")
            ),
        }
        row = {
            "order": entry["order"],
            "priority": entry["priority"],
            "descriptor_path": entry["descriptor_path"],
            "descriptor_sha256": baseline["descriptor"]["sha256"],
            "package_id": package_id,
            "input_schema": baseline["input_schema"],
            "normalized_lifecycle": lifecycle,
            "contract_valid": live_error is None
            or live_error_decision
            in {"blocked_identity_drift", "blocked_corrupt_output"},
            "content_identity_sha256": content_identity,
            "render_settings_identity_sha256": _render_settings_identity(payload),
            "live_availability": _live_availability_summary(
                lifecycle=lifecycle,
                availability=availability,
                check_live=check_live,
            ),
            "availability": [
                {
                    "artifact_class": str(item["artifact_class"]),
                    "status": str(item["status"]),
                }
                for item in availability
            ],
            "recorded_identity_availability": recorded,
            "semantic_drift_state": (
                "detected"
                if decision == "blocked_identity_drift"
                else "unchanged"
            ),
            "technical_next_stage": technical_next_stage,
            "technical_decision": decision,
            "external_authority": _external_authority(
                baseline,
                execution_policy,
            ),
            "execution_eligible": bool(action_decision and action_authorized),
            "execution_gate_decision": execution_gate,
            "reason_codes": reasons,
            "contract_error": (
                {
                    "error_code": live_error.code,
                    "section": live_error.section,
                    "field_path": live_error.field_path,
                    "consumer_effect": live_error.consumer_effect,
                }
                if live_error is not None
                else None
            ),
            "target_identity_sha256": (
                sha256_json({"run_id": target[0], "mp4_filename": target[1]})
                if target is not None
                else None
            ),
        }
        rows.append(row)

    for identity, references in content_identities.items():
        if len(references) < 2:
            continue
        groups = {reference for _, reference in references}
        if None in groups or len(groups) != 1:
            _fail(
                "queue contains a duplicate content identity",
                code="queue_duplicate_content_identity",
                field_path="$.queue.packages[*]",
                consumer_effect=(
                    "the same semantic content could be scheduled more than once"
                ),
            )

    blocked_decisions = {
        "blocked_contract",
        "blocked_identity_drift",
        "blocked_corrupt_output",
    }
    counts = {
        "total_packages": len(rows),
        "verified_noop": sum(
            row["technical_decision"] == "verified_noop" for row in rows
        ),
        "recorded_complete_no_live_file": sum(
            row["technical_decision"] == "recorded_complete_no_live_file"
            for row in rows
        ),
        "source_project_candidates": sum(
            row["technical_decision"] == "source_project_generation_required"
            for row in rows
        ),
        "render_candidates": sum(
            row["technical_decision"] == "render_required" for row in rows
        ),
        "human_review_candidates": sum(
            row["technical_decision"] == "human_review_required"
            for row in rows
        ),
        "blocked_packages": sum(
            row["technical_decision"] in blocked_decisions for row in rows
        ),
        "invalid_packages": sum(
            row["technical_decision"] == "blocked_contract" for row in rows
        ),
        "scheduled_for_render": sum(
            row["technical_decision"] == "render_required"
            and row["execution_eligible"]
            for row in rows
        ),
        "execution_set_size": sum(
            bool(row["execution_eligible"]) for row in rows
        ),
    }
    result: dict[str, Any] = {
        "schema": FACTORY_QUEUE_RESULT_SCHEMA,
        "schema_version": FACTORY_QUEUE_VERSION,
        "status": "failed" if counts["blocked_packages"] else "passed",
        "queue_id": normalized_queue["queue_id"],
        "queue_descriptor": queue_identity,
        "bounds": {
            "hard_maximum": FACTORY_QUEUE_HARD_MAXIMUM,
            "declared_maximum": normalized_queue["maximum_queue_size"],
            "observed_count": len(rows),
            "ordering": "priority_descending_then_order_ascending",
            "stable": True,
        },
        "evaluation": {
            "mode": "live_hash_check" if check_live else "recorded_identity_only",
            "check_live": check_live,
            "side_effect_free": True,
            "run_local_fields_excluded": sorted(RUN_LOCAL_FIELDS),
            "technical_and_execution_authority_separate": True,
        },
        "packages": rows,
        "counts": counts,
        "execution_set": [
            {
                "package_id": row["package_id"],
                "technical_next_stage": row["technical_next_stage"],
            }
            for row in rows
            if row["execution_eligible"]
        ],
        "boundaries": {
            "source_project_generated": False,
            "yymm4_launched": False,
            "electron_launched": False,
            "render_driver_launched": False,
            "ffmpeg_encode_performed": False,
            "media_playback": False,
            "system_volume_operation": False,
            "product_artifacts_written": False,
            "private_artifacts_copied": False,
            "human_or_rights_authority_granted": False,
        },
    }
    result["evaluation_sha256"] = sha256_json(result)
    return result


def execute_safe_queue_stages(
    *,
    repo_root: Path,
    evaluation: Mapping[str, Any],
) -> dict[str, Any]:
    """Run validation-only dry-runs and return a sanitized deterministic receipt."""

    if evaluation.get("status") != "passed":
        _fail(
            "safe stages require a queue with no contract or identity failures",
            code="queue_safe_stage_blocked",
            field_path="$.status",
            consumer_effect="safe-stage execution cannot bypass a blocked package",
        )
    root = repo_root.resolve()
    from src.pipeline.episode_video import EpisodeVideoError, run_episode_video

    results: list[dict[str, Any]] = []
    for index, row in enumerate(evaluation["packages"]):
        descriptor_relative, descriptor_path = _repo_locator(
            root,
            row["descriptor_path"],
            field_path=f"$.packages[{index}].descriptor_path",
        )
        validation = validate_factory_package_lifecycle(
            repo_root=root,
            descriptor_path=descriptor_path,
            check_live=True,
        )
        lifecycle = validation["normalized_lifecycle"]["state"]
        if lifecycle in {"package_prepared", "source_project_ready"}:
            plan = build_pre_render_stage_plan(
                repo_root=root,
                descriptor_path=descriptor_path,
                validation_result=validation,
            )
            results.append(
                {
                    "package_id": row["package_id"],
                    "descriptor_path": descriptor_relative,
                    "mode": "pre_render_stage_plan",
                    "status": plan["status"],
                    "content_identity_sha256": plan[
                        "content_identity_sha256"
                    ],
                    "content_identity_exact": (
                        plan["content_identity_sha256"]
                        == row["content_identity_sha256"]
                    ),
                    "completed_video_dry_run": False,
                    "successful_stop_before": plan["stop"]["before_stage"],
                    "launch_counts": dict(plan["launch_counts"]),
                    "writes": dict(plan["writes"]),
                }
            )
            continue
        manifest_path = root / Path(
            *PurePosixPath(
                validation["normalized"]["episode_manifest_path"]
            ).parts
        )
        try:
            plan = run_episode_video(
                repo_root=root,
                manifest_path=manifest_path,
                render=False,
                dry_run=True,
                resume=False,
                force=False,
                run_id_override=None,
            )
        except EpisodeVideoError as exc:
            raise FactoryQueueError(
                "existing package dry-run failed",
                code="queue_safe_stage_package_dry_run_failed",
                field_path=f"$.packages[{index}]",
                consumer_effect=(
                    "queue validation cannot assert a write-free package plan"
                ),
            ) from exc
        identity_exact = (
            plan.get("content_identity_sha256")
            == row["content_identity_sha256"]
        )
        if not identity_exact:
            _fail(
                "existing package dry-run changed semantic identity",
                code="queue_safe_stage_identity_mismatch",
                field_path=f"$.packages[{index}].content_identity_sha256",
                consumer_effect="completed package cannot remain a no-op",
            )
        results.append(
            {
                "package_id": row["package_id"],
                "descriptor_path": descriptor_relative,
                "mode": "existing_episode_pipeline_dry_run",
                "status": str(plan["status"]),
                "content_identity_sha256": str(
                    plan["content_identity_sha256"]
                ),
                "content_identity_exact": True,
                "completed_video_dry_run": True,
                "render_requested": bool(plan["render_requested"]),
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
            }
        )

    safe_result: dict[str, Any] = {
        "schema": FACTORY_QUEUE_SAFE_STAGE_SCHEMA,
        "status": "passed",
        "queue_id": evaluation["queue_id"],
        "queue_evaluation_sha256": evaluation["evaluation_sha256"],
        "package_results": results,
        "counts": {
            "packages_validated": len(results),
            "existing_pipeline_dry_runs": sum(
                row["mode"] == "existing_episode_pipeline_dry_run"
                for row in results
            ),
            "pre_render_stage_plans": sum(
                row["mode"] == "pre_render_stage_plan" for row in results
            ),
            "identity_exact": sum(
                bool(row["content_identity_exact"]) for row in results
            ),
            "product_writes": 0,
            "process_launches": 0,
        },
        "boundaries": {
            "validation_only": True,
            "sanitized": True,
            "deterministic_fields_only": True,
            "source_project_generated": False,
            "yymm4_launched": False,
            "electron_launched": False,
            "render_driver_launched": False,
            "ffmpeg_encode_performed": False,
            "media_playback": False,
            "system_volume_operation": False,
            "product_artifacts_written": False,
            "private_artifacts_copied": False,
        },
    }
    safe_result["safe_stage_sha256"] = sha256_json(safe_result)
    return safe_result


__all__ = [
    "FACTORY_QUEUE_HARD_MAXIMUM",
    "FACTORY_QUEUE_RESULT_SCHEMA",
    "FACTORY_QUEUE_SCHEMA",
    "FACTORY_QUEUE_SAFE_STAGE_SCHEMA",
    "FACTORY_QUEUE_VERSION",
    "FactoryQueueError",
    "TECHNICAL_DECISIONS",
    "decide_render_on_change",
    "evaluate_factory_queue",
    "execute_safe_queue_stages",
]
