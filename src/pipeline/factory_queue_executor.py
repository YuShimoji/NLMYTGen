"""Bounded, serial execution of exact Factory Queue change sets."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping

from src.pipeline.factory_queue import (
    canonical_json_bytes,
    evaluate_factory_queue,
    sha256_file,
    sha256_json,
)
from src.pipeline.factory_source_project_promotion import advance_factory_package


CHANGE_SET_SCHEMA = "nlmytgen.factory_queue.change_set.v1"
AUTHORITY_SET_SCHEMA = "nlmytgen.factory_queue.execution_authority_set.v1"
AUTHORITY_RECORD_SCHEMA = "nlmytgen.factory_queue.execution_authority.v1"
JOURNAL_SCHEMA = "nlmytgen.factory_queue.execution_journal.v1"
EXECUTION_RESULT_SCHEMA = "nlmytgen.factory_queue.execution_result.v1"
EXECUTOR_SCHEMA = "nlmytgen.factory_queue.executor.v1"
SCHEMA_VERSION = "1.0"
HARD_MAXIMUM_MUTATING_ENTRIES = 32

CHANGE_SET_SCHEMA_PATH = Path(
    "schemas/factory_queue_execution_v1/factory_queue_change_set_v1.schema.json"
)
AUTHORITY_SCHEMA_PATH = Path(
    "schemas/factory_queue_execution_v1/"
    "factory_queue_execution_authority_v1.schema.json"
)
JOURNAL_SCHEMA_PATH = Path(
    "schemas/factory_queue_execution_v1/"
    "factory_queue_execution_journal_v1.schema.json"
)

NOOP_DECISIONS = frozenset(
    {"verified_noop", "recorded_complete_no_live_file"}
)
OPERATION_DECISIONS = {
    "source_project_generation": "source_project_generation_required",
    "render": "render_required",
}
OPERATION_EDGES = {
    "source_project_generation": ("package_prepared", "source_project_ready"),
    "render": ("source_project_ready", "rendered"),
}
JOURNAL_STATES = frozenset(
    {
        "not_selected",
        "verified_noop",
        "planned",
        "authority_validated",
        "started",
        "succeeded",
        "failed",
        "effect_unknown",
        "skipped_after_failure",
    }
)

_STABLE_ID = re.compile(r"^[a-z0-9]+(?:[a-z0-9_.-]*[a-z0-9])?$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")

_CHANGE_SET_FIELDS = frozenset(
    {
        "schema",
        "schema_version",
        "contract",
        "change_set_id",
        "queue",
        "maximum_mutating_entries",
        "execution_policy",
        "entries",
        "receipt_policy",
    }
)
_CONTRACT_FIELDS = frozenset(
    {
        "schema",
        "change_set_schema_path",
        "change_set_schema_sha256",
        "authority_schema_path",
        "authority_schema_sha256",
        "journal_schema_path",
        "journal_schema_sha256",
    }
)
_BOUND_FILE_FIELDS = frozenset({"path", "sha256"})
_EXECUTION_POLICY_FIELDS = frozenset(
    {
        "schema",
        "ordering",
        "serial",
        "plan_only_default",
        "noop_elision",
        "stop_on_first_mutating_failure",
        "drift_policy",
        "unknown_effect_policy",
    }
)
_ENTRY_FIELDS = frozenset(
    {
        "order",
        "package_id",
        "descriptor_path",
        "descriptor_sha256",
        "expected_content_identity_sha256",
        "expected_render_settings_identity_sha256",
        "expected_completed_output_sha256",
        "expected_target_identity_sha256",
        "expected_current_lifecycle",
        "requested_target_lifecycle",
        "operation",
        "authority_id",
        "immutable_artifact_reference",
    }
)
_RECEIPT_POLICY_FIELDS = frozenset(
    {
        "schema",
        "deterministic",
        "append_only_journal",
        "include_usernames",
        "include_drive_letters",
        "include_private_absolute_paths",
        "include_credentials",
        "include_private_media",
        "include_process_command_lines",
    }
)
_AUTHORITY_SET_FIELDS = frozenset(
    {"schema", "schema_version", "authorities"}
)
_AUTHORITY_FIELDS = frozenset(
    {
        "schema",
        "authority_id",
        "replaces_authority_id",
        "queue",
        "change_set",
        "package",
        "from_lifecycle",
        "to_lifecycle",
        "operation",
        "maximum_use_count",
        "status",
        "constraints",
    }
)
_AUTHORITY_CHANGE_SET_FIELDS = frozenset({"change_set_id", "sha256"})
_AUTHORITY_PACKAGE_FIELDS = frozenset(
    {"package_id", "descriptor_path", "descriptor_sha256"}
)
_AUTHORITY_CONSTRAINT_FIELDS = frozenset(
    {
        "serial_only",
        "exact_identity_recheck",
        "private_artifact_copy",
        "human_acceptance",
        "rights",
        "production",
        "publication",
        "upload",
        "release",
    }
)
_JOURNAL_FIELDS = frozenset(
    {
        "schema",
        "schema_version",
        "plan_identity_sha256",
        "queue",
        "change_set",
        "execution_mode",
        "status",
        "entries",
        "counts",
        "boundaries",
    }
)
_JOURNAL_CHANGE_SET_FIELDS = frozenset(
    {"change_set_id", "path", "sha256"}
)
_JOURNAL_ENTRY_FIELDS = frozenset(
    {
        "order",
        "package_id",
        "descriptor_path",
        "descriptor_sha256",
        "technical_decision",
        "requested_operation",
        "from_lifecycle",
        "to_lifecycle",
        "events",
        "current_state",
    }
)
_EVENT_FIELDS = frozenset(
    {
        "sequence",
        "state",
        "authority_id",
        "authority_status",
        "backend_result_identity_sha256",
        "failure_code",
        "consumer_effect",
    }
)
_COUNT_FIELDS = frozenset(
    {
        "packages_validated",
        "verified_noop",
        "not_selected",
        "planned",
        "succeeded",
        "failed",
        "effect_unknown",
        "skipped_after_failure",
        "authority_consumptions",
    }
)
_BOUNDARY_FIELDS = frozenset(
    {
        "serial_execution",
        "append_only_journal",
        "noop_backend_dispatch_count",
        "backend_dispatch_count",
        "source_project_generation_count",
        "render_count",
        "yymm4_launch_count",
        "electron_launch_count",
        "render_driver_launch_count",
        "ffmpeg_encode_count",
        "playback_count",
        "system_volume_operation_count",
        "private_artifact_copy_count",
        "product_write_count",
        "human_or_rights_action_count",
        "public_action_count",
    }
)


class FactoryQueueExecutorError(RuntimeError):
    """Sanitized executor contract or safety failure."""

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
            "schema": EXECUTION_RESULT_SCHEMA,
            "schema_version": SCHEMA_VERSION,
            "status": "failed",
            "error_code": self.code,
            "field_path": self.field_path,
            "consumer_effect": self.consumer_effect,
            "message": str(self),
            "boundaries": _empty_boundaries(),
        }


QueueEvaluator = Callable[..., dict[str, Any]]
AdvancementBackend = Callable[..., Mapping[str, Any]]


def _fail(
    message: str,
    *,
    code: str,
    field_path: str,
    consumer_effect: str,
) -> None:
    raise FactoryQueueExecutorError(
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
            "executor contract section must be an object",
            code="execution_section_type_invalid",
            field_path=field_path,
            consumer_effect="the bounded execution contract cannot be interpreted",
        )
    keys = frozenset(str(key) for key in value)
    if required - keys or keys - allowed:
        _fail(
            "executor contract fields do not match the versioned schema",
            code="execution_section_fields_invalid",
            field_path=field_path,
            consumer_effect="missing or unknown fields would make execution ambiguous",
        )
    return value


def _require_exact(
    value: Any,
    expected: Any,
    *,
    field_path: str,
    code: str = "execution_policy_invalid",
) -> None:
    if value != expected:
        _fail(
            "executor value differs from the exact v1 contract",
            code=code,
            field_path=field_path,
            consumer_effect="execution must stop before any backend effect",
        )


def _require_sha256(value: Any, *, field_path: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        _fail(
            "executor identity must be a lowercase SHA-256",
            code="execution_identity_invalid",
            field_path=field_path,
            consumer_effect="the exact execution identity cannot be established",
        )
    return value


def _require_stable_id(value: Any, *, field_path: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) > 128
        or _STABLE_ID.fullmatch(value) is None
    ):
        _fail(
            "executor identifier is not stable or sanitized",
            code="execution_identifier_invalid",
            field_path=field_path,
            consumer_effect="the execution record cannot be bound deterministically",
        )
    return value


def _load_json(path: Path, *, field_path: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FactoryQueueExecutorError(
            "executor JSON is unavailable or malformed",
            code="execution_json_unreadable",
            field_path=field_path,
            consumer_effect="bounded execution cannot start",
        ) from exc
    if not isinstance(value, dict):
        _fail(
            "executor JSON root must be an object",
            code="execution_root_type_invalid",
            field_path=field_path,
            consumer_effect="bounded execution cannot select a versioned contract",
        )
    return value


def _repo_locator(
    repo_root: Path,
    value: Any,
    *,
    field_path: str,
) -> tuple[str, Path]:
    if not isinstance(value, str) or not value:
        _fail(
            "executor locator must be a non-empty repository-relative string",
            code="execution_locator_invalid",
            field_path=field_path,
            consumer_effect="the bound input cannot be resolved safely",
        )
    if "\\" in value or ":" in value:
        _fail(
            "executor locator must use a repository-relative POSIX path",
            code="execution_locator_private_or_absolute",
            field_path=field_path,
            consumer_effect="private or machine-local paths cannot enter a journal",
        )
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        _fail(
            "executor locator escapes the repository boundary",
            code="execution_locator_escape",
            field_path=field_path,
            consumer_effect="the bound input cannot be resolved safely",
        )
    root = repo_root.resolve()
    resolved = (root / Path(*pure.parts)).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        _fail(
            "executor locator escapes the repository boundary",
            code="execution_locator_escape",
            field_path=field_path,
            consumer_effect="the bound input cannot be resolved safely",
        )
    if not resolved.is_file():
        _fail(
            "executor locator does not identify an input file",
            code="execution_locator_unavailable",
            field_path=field_path,
            consumer_effect="the bound input cannot be rehashed",
        )
    return pure.as_posix(), resolved


def _validate_bound_file(
    repo_root: Path,
    value: Any,
    *,
    field_path: str,
) -> dict[str, Any]:
    bound = _require_mapping(
        value,
        field_path=field_path,
        required=_BOUND_FILE_FIELDS,
        allowed=_BOUND_FILE_FIELDS,
    )
    locator, resolved = _repo_locator(
        repo_root,
        bound["path"],
        field_path=f"{field_path}.path",
    )
    expected = _require_sha256(
        bound["sha256"],
        field_path=f"{field_path}.sha256",
    )
    if sha256_file(resolved) != expected:
        _fail(
            "bound file bytes changed",
            code="execution_bound_file_hash_mismatch",
            field_path=f"{field_path}.sha256",
            consumer_effect="identity drift must stop before an effect",
        )
    return {"path": locator, "sha256": expected, "resolved_path": resolved}


def _validate_schema_contract(
    repo_root: Path,
    contract: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    expected = {
        "change_set": (
            CHANGE_SET_SCHEMA_PATH,
            CHANGE_SET_SCHEMA,
        ),
        "authority": (
            AUTHORITY_SCHEMA_PATH,
            AUTHORITY_SET_SCHEMA,
        ),
        "journal": (
            JOURNAL_SCHEMA_PATH,
            JOURNAL_SCHEMA,
        ),
    }
    result: dict[str, dict[str, Any]] = {}
    for name, (expected_path, expected_id) in expected.items():
        path_field = f"{name}_schema_path"
        hash_field = f"{name}_schema_sha256"
        locator, resolved = _repo_locator(
            repo_root,
            contract[path_field],
            field_path=f"$.contract.{path_field}",
        )
        if locator != expected_path.as_posix():
            _fail(
                "executor schema locator is not the v1 authority",
                code="execution_schema_locator_invalid",
                field_path=f"$.contract.{path_field}",
                consumer_effect="the execution contract version is not exact",
            )
        expected_hash = _require_sha256(
            contract[hash_field],
            field_path=f"$.contract.{hash_field}",
        )
        actual_hash = sha256_file(resolved)
        if actual_hash != expected_hash:
            _fail(
                "executor schema identity changed",
                code="execution_schema_hash_mismatch",
                field_path=f"$.contract.{hash_field}",
                consumer_effect="schema drift must stop before planning",
            )
        schema = _load_json(
            resolved,
            field_path=f"$.contract.{path_field}",
        )
        if schema.get("$id") != expected_id:
            _fail(
                "executor schema declares an unsupported identity",
                code="execution_schema_identity_invalid",
                field_path=f"$.contract.{path_field}",
                consumer_effect="the execution contract version is not exact",
            )
        result[name] = {"path": locator, "sha256": actual_hash}
    return result


def _validate_change_set(
    *,
    repo_root: Path,
    change_set_path: Path,
) -> dict[str, Any]:
    root = repo_root.resolve()
    relative_path, resolved_path = _repo_locator(
        root,
        change_set_path.as_posix(),
        field_path="$.change_set",
    )
    payload = _load_json(resolved_path, field_path="$")
    _require_mapping(
        payload,
        field_path="$",
        required=_CHANGE_SET_FIELDS,
        allowed=_CHANGE_SET_FIELDS,
    )
    _require_exact(payload["schema"], CHANGE_SET_SCHEMA, field_path="$.schema")
    _require_exact(
        payload["schema_version"],
        SCHEMA_VERSION,
        field_path="$.schema_version",
    )
    change_set_id = _require_stable_id(
        payload["change_set_id"],
        field_path="$.change_set_id",
    )

    contract = _require_mapping(
        payload["contract"],
        field_path="$.contract",
        required=_CONTRACT_FIELDS,
        allowed=_CONTRACT_FIELDS,
    )
    _require_exact(
        contract["schema"],
        "nlmytgen.factory_queue.execution_contract.v1",
        field_path="$.contract.schema",
    )
    schemas = _validate_schema_contract(root, contract)
    queue = _validate_bound_file(root, payload["queue"], field_path="$.queue")

    maximum = payload["maximum_mutating_entries"]
    if (
        isinstance(maximum, bool)
        or not isinstance(maximum, int)
        or not 0 <= maximum <= HARD_MAXIMUM_MUTATING_ENTRIES
    ):
        _fail(
            "change-set maximum must be a finite integer within the hard cap",
            code="change_set_maximum_invalid",
            field_path="$.maximum_mutating_entries",
            consumer_effect="the mutating batch would not be bounded",
        )

    policy = _require_mapping(
        payload["execution_policy"],
        field_path="$.execution_policy",
        required=_EXECUTION_POLICY_FIELDS,
        allowed=_EXECUTION_POLICY_FIELDS,
    )
    expected_policy = {
        "schema": "nlmytgen.factory_queue.change_set_execution_policy.v1",
        "ordering": "queue_order",
        "serial": True,
        "plan_only_default": True,
        "noop_elision": True,
        "stop_on_first_mutating_failure": True,
        "drift_policy": (
            "recheck_queue_descriptor_content_render_and_output_"
            "before_every_effect"
        ),
        "unknown_effect_policy": (
            "read_only_reconciliation_required_before_retry"
        ),
    }
    for key, expected in expected_policy.items():
        _require_exact(
            policy[key],
            expected,
            field_path=f"$.execution_policy.{key}",
        )

    entries = payload["entries"]
    if not isinstance(entries, list):
        _fail(
            "change-set entries must be an array",
            code="change_set_entries_invalid",
            field_path="$.entries",
            consumer_effect="the mutating package set is ambiguous",
        )
    if len(entries) > maximum or len(entries) > HARD_MAXIMUM_MUTATING_ENTRIES:
        _fail(
            "change-set entry count exceeds its finite maximum",
            code="change_set_maximum_exceeded",
            field_path="$.entries",
            consumer_effect="the executor must not broaden the authorized batch",
        )

    normalized_entries: list[dict[str, Any]] = []
    package_ids: set[str] = set()
    descriptor_paths: set[str] = set()
    authority_ids: set[str] = set()
    target_identities: set[str] = set()
    observed_orders: list[int] = []
    for index, raw_entry in enumerate(entries):
        field_path = f"$.entries[{index}]"
        entry = _require_mapping(
            raw_entry,
            field_path=field_path,
            required=_ENTRY_FIELDS - {"immutable_artifact_reference"},
            allowed=_ENTRY_FIELDS,
        )
        order = entry["order"]
        if (
            isinstance(order, bool)
            or not isinstance(order, int)
            or not 1 <= order <= HARD_MAXIMUM_MUTATING_ENTRIES
        ):
            _fail(
                "change-set order is outside the bounded queue range",
                code="change_set_order_invalid",
                field_path=f"{field_path}.order",
                consumer_effect="serial execution order cannot be established",
            )
        package_id = _require_stable_id(
            entry["package_id"],
            field_path=f"{field_path}.package_id",
        )
        descriptor_locator, descriptor_path = _repo_locator(
            root,
            entry["descriptor_path"],
            field_path=f"{field_path}.descriptor_path",
        )
        descriptor_sha = _require_sha256(
            entry["descriptor_sha256"],
            field_path=f"{field_path}.descriptor_sha256",
        )
        if sha256_file(descriptor_path) != descriptor_sha:
            _fail(
                "change-set descriptor bytes changed",
                code="change_set_descriptor_hash_mismatch",
                field_path=f"{field_path}.descriptor_sha256",
                consumer_effect="descriptor drift must stop before planning",
            )
        content_identity = _require_sha256(
            entry["expected_content_identity_sha256"],
            field_path=f"{field_path}.expected_content_identity_sha256",
        )
        render_identity = _require_sha256(
            entry["expected_render_settings_identity_sha256"],
            field_path=(
                f"{field_path}.expected_render_settings_identity_sha256"
            ),
        )
        completed_output = entry["expected_completed_output_sha256"]
        if completed_output is not None:
            completed_output = _require_sha256(
                completed_output,
                field_path=f"{field_path}.expected_completed_output_sha256",
            )
        target_identity = entry["expected_target_identity_sha256"]
        if target_identity is not None:
            target_identity = _require_sha256(
                target_identity,
                field_path=f"{field_path}.expected_target_identity_sha256",
            )
        operation = entry["operation"]
        if operation not in OPERATION_EDGES:
            _fail(
                "change-set operation is not supported by v1",
                code="change_set_operation_unsupported",
                field_path=f"{field_path}.operation",
                consumer_effect="arbitrary or external effects are forbidden",
            )
        expected_edge = OPERATION_EDGES[operation]
        actual_edge = (
            entry["expected_current_lifecycle"],
            entry["requested_target_lifecycle"],
        )
        if actual_edge != expected_edge:
            _fail(
                "change-set lifecycle edge does not match its operation",
                code="change_set_lifecycle_edge_mismatch",
                field_path=field_path,
                consumer_effect="the backend operation must remain exact",
            )
        authority_id = _require_stable_id(
            entry["authority_id"],
            field_path=f"{field_path}.authority_id",
        )
        immutable_reference = entry.get("immutable_artifact_reference")
        if immutable_reference is not None:
            immutable_reference = _require_stable_id(
                immutable_reference,
                field_path=f"{field_path}.immutable_artifact_reference",
            )
        if package_id in package_ids:
            _fail(
                "change-set contains a duplicate package",
                code="change_set_duplicate_package",
                field_path=field_path,
                consumer_effect="one package could be dispatched twice",
            )
        if descriptor_locator in descriptor_paths:
            _fail(
                "change-set contains a duplicate descriptor",
                code="change_set_duplicate_descriptor",
                field_path=field_path,
                consumer_effect="one package could be dispatched twice",
            )
        if authority_id in authority_ids:
            _fail(
                "change-set reuses one authority ID",
                code="change_set_duplicate_authority",
                field_path=f"{field_path}.authority_id",
                consumer_effect="one-shot authority cannot cover two effects",
            )
        if target_identity is not None and target_identity in target_identities:
            _fail(
                "change-set contains an output target collision",
                code="change_set_target_collision",
                field_path=f"{field_path}.expected_target_identity_sha256",
                consumer_effect="two effects cannot address one output target",
            )
        package_ids.add(package_id)
        descriptor_paths.add(descriptor_locator)
        authority_ids.add(authority_id)
        if target_identity is not None:
            target_identities.add(target_identity)
        observed_orders.append(order)
        normalized_entries.append(
            {
                "order": order,
                "package_id": package_id,
                "descriptor_path": descriptor_locator,
                "resolved_descriptor_path": descriptor_path,
                "descriptor_sha256": descriptor_sha,
                "expected_content_identity_sha256": content_identity,
                "expected_render_settings_identity_sha256": render_identity,
                "expected_completed_output_sha256": completed_output,
                "expected_target_identity_sha256": target_identity,
                "expected_current_lifecycle": actual_edge[0],
                "requested_target_lifecycle": actual_edge[1],
                "operation": operation,
                "authority_id": authority_id,
                "immutable_artifact_reference": immutable_reference,
            }
        )
    if observed_orders != sorted(observed_orders) or len(set(observed_orders)) != len(
        observed_orders
    ):
        _fail(
            "change-set entries are not in one stable explicit order",
            code="change_set_order_unstable",
            field_path="$.entries[*].order",
            consumer_effect="serial execution could vary between runs",
        )

    receipt = _require_mapping(
        payload["receipt_policy"],
        field_path="$.receipt_policy",
        required=_RECEIPT_POLICY_FIELDS,
        allowed=_RECEIPT_POLICY_FIELDS,
    )
    expected_receipt = {
        "schema": "nlmytgen.factory_queue.execution_receipt_policy.v1",
        "deterministic": True,
        "append_only_journal": True,
        "include_usernames": False,
        "include_drive_letters": False,
        "include_private_absolute_paths": False,
        "include_credentials": False,
        "include_private_media": False,
        "include_process_command_lines": False,
    }
    for key, expected in expected_receipt.items():
        _require_exact(
            receipt[key],
            expected,
            field_path=f"$.receipt_policy.{key}",
        )

    return {
        "change_set_id": change_set_id,
        "path": relative_path,
        "sha256": sha256_file(resolved_path),
        "queue": queue,
        "maximum_mutating_entries": maximum,
        "entries": normalized_entries,
        "schemas": schemas,
        "receipt_policy": dict(receipt),
    }


def _queue_expected_entries(queue_path: Path) -> dict[str, dict[str, Any]]:
    payload = _load_json(queue_path, field_path="$.queue")
    try:
        entries = payload["queue"]["packages"]
    except (KeyError, TypeError) as exc:
        raise FactoryQueueExecutorError(
            "queue package bindings are unavailable",
            code="execution_queue_shape_invalid",
            field_path="$.queue.packages",
            consumer_effect="change-set bindings cannot be compared",
        ) from exc
    if not isinstance(entries, list):
        _fail(
            "queue package bindings must be an array",
            code="execution_queue_shape_invalid",
            field_path="$.queue.packages",
            consumer_effect="change-set bindings cannot be compared",
        )
    result: dict[str, dict[str, Any]] = {}
    for raw in entries:
        if not isinstance(raw, Mapping):
            _fail(
                "queue package binding is malformed",
                code="execution_queue_shape_invalid",
                field_path="$.queue.packages[*]",
                consumer_effect="change-set bindings cannot be compared",
            )
        package_id = raw.get("expected_package_id")
        if isinstance(package_id, str):
            result[package_id] = dict(raw)
    return result


def _build_plan(
    *,
    repo_root: Path,
    queue_path: Path,
    change_set_path: Path,
    queue_evaluator: QueueEvaluator,
) -> dict[str, Any]:
    root = repo_root.resolve()
    change_set = _validate_change_set(
        repo_root=root,
        change_set_path=change_set_path,
    )
    queue_locator, resolved_queue = _repo_locator(
        root,
        queue_path.as_posix(),
        field_path="$.queue_argument",
    )
    if (
        queue_locator != change_set["queue"]["path"]
        or sha256_file(resolved_queue) != change_set["queue"]["sha256"]
    ):
        _fail(
            "queue argument does not match the exact change-set binding",
            code="change_set_queue_identity_mismatch",
            field_path="$.queue",
            consumer_effect="the change set cannot move to another queue",
        )
    evaluation = queue_evaluator(
        repo_root=root,
        queue_path=queue_path,
        check_live=True,
    )
    if evaluation.get("status") != "passed":
        _fail(
            "queue evaluation is blocked or invalid",
            code="execution_queue_evaluation_failed",
            field_path="$.queue",
            consumer_effect="no backend effect is allowed from a blocked plan",
        )
    queue_identity = evaluation.get("queue_descriptor")
    if not isinstance(queue_identity, Mapping):
        _fail(
            "queue evaluation omitted its identity",
            code="execution_queue_identity_missing",
            field_path="$.queue",
            consumer_effect="the plan cannot bind an exact queue",
        )
    if (
        queue_identity.get("path") != queue_locator
        or queue_identity.get("sha256") != change_set["queue"]["sha256"]
    ):
        _fail(
            "queue evaluation identity differs from the change set",
            code="execution_queue_identity_mismatch",
            field_path="$.queue",
            consumer_effect="queue drift must stop before planning",
        )

    rows = evaluation.get("packages")
    if not isinstance(rows, list):
        _fail(
            "queue evaluation package rows are unavailable",
            code="execution_queue_rows_invalid",
            field_path="$.queue.packages",
            consumer_effect="the ordered package plan cannot be built",
        )
    row_by_id = {
        row.get("package_id"): row
        for row in rows
        if isinstance(row, Mapping) and isinstance(row.get("package_id"), str)
    }
    queue_entries = _queue_expected_entries(resolved_queue)
    selected_by_id = {
        entry["package_id"]: entry for entry in change_set["entries"]
    }

    for index, entry in enumerate(change_set["entries"]):
        field_path = f"$.entries[{index}]"
        row = row_by_id.get(entry["package_id"])
        queue_entry = queue_entries.get(entry["package_id"])
        if row is None or queue_entry is None:
            _fail(
                "change-set package is not present in the queue",
                code="change_set_package_not_in_queue",
                field_path=f"{field_path}.package_id",
                consumer_effect="the executor cannot broaden the queue",
            )
        comparisons = (
            (
                row.get("order"),
                entry["order"],
                "order",
                "change_set_queue_order_mismatch",
            ),
            (
                row.get("descriptor_path"),
                entry["descriptor_path"],
                "descriptor_path",
                "change_set_descriptor_path_mismatch",
            ),
            (
                row.get("descriptor_sha256"),
                entry["descriptor_sha256"],
                "descriptor_sha256",
                "change_set_descriptor_hash_mismatch",
            ),
            (
                row.get("content_identity_sha256"),
                entry["expected_content_identity_sha256"],
                "expected_content_identity_sha256",
                "change_set_content_identity_mismatch",
            ),
            (
                row.get("render_settings_identity_sha256"),
                entry["expected_render_settings_identity_sha256"],
                "expected_render_settings_identity_sha256",
                "change_set_render_settings_mismatch",
            ),
            (
                queue_entry.get("expected_completed_output_sha256"),
                entry["expected_completed_output_sha256"],
                "expected_completed_output_sha256",
                "change_set_output_identity_mismatch",
            ),
            (
                row.get("target_identity_sha256"),
                entry["expected_target_identity_sha256"],
                "expected_target_identity_sha256",
                "change_set_target_identity_mismatch",
            ),
            (
                row.get("normalized_lifecycle"),
                entry["expected_current_lifecycle"],
                "expected_current_lifecycle",
                "change_set_lifecycle_edge_mismatch",
            ),
            (
                row.get("technical_decision"),
                OPERATION_DECISIONS[entry["operation"]],
                "operation",
                "change_set_noop_or_decision_mismatch",
            ),
        )
        for actual, expected, field, code in comparisons:
            if actual != expected:
                _fail(
                    "change-set entry no longer matches its queue decision",
                    code=code,
                    field_path=f"{field_path}.{field}",
                    consumer_effect="drift or no-op selection must stop before dispatch",
                )

    plan_packages: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        package_id = str(row["package_id"])
        selected = selected_by_id.get(package_id)
        decision = str(row["technical_decision"])
        if decision in NOOP_DECISIONS:
            state = "verified_noop"
        elif selected is not None:
            state = "planned"
        else:
            state = "not_selected"
        plan_packages.append(
            {
                "order": int(row["order"]),
                "package_id": package_id,
                "descriptor_path": str(row["descriptor_path"]),
                "descriptor_sha256": str(row["descriptor_sha256"]),
                "content_identity_sha256": row.get("content_identity_sha256"),
                "render_settings_identity_sha256": row.get(
                    "render_settings_identity_sha256"
                ),
                "target_identity_sha256": row.get("target_identity_sha256"),
                "normalized_lifecycle": row.get("normalized_lifecycle"),
                "technical_decision": decision,
                "initial_state": state,
                "requested_operation": (
                    selected["operation"] if selected is not None else None
                ),
                "requested_target_lifecycle": (
                    selected["requested_target_lifecycle"]
                    if selected is not None
                    else None
                ),
                "authority_id": (
                    selected["authority_id"] if selected is not None else None
                ),
            }
        )
    plan_packages.sort(key=lambda row: row["order"])
    identity_payload = {
        "executor": {
            "schema": EXECUTOR_SCHEMA,
            "schema_version": SCHEMA_VERSION,
        },
        "queue_sha256": change_set["queue"]["sha256"],
        "change_set_sha256": change_set["sha256"],
        "packages": [
            {
                "order": row["order"],
                "package_id": row["package_id"],
                "descriptor_sha256": row["descriptor_sha256"],
                "content_identity_sha256": row["content_identity_sha256"],
                "render_settings_identity_sha256": row[
                    "render_settings_identity_sha256"
                ],
                "target_identity_sha256": row["target_identity_sha256"],
                "normalized_lifecycle": row["normalized_lifecycle"],
                "requested_operation": row["requested_operation"],
                "requested_target_lifecycle": row[
                    "requested_target_lifecycle"
                ],
                "authority_id": row["authority_id"],
            }
            for row in plan_packages
        ],
    }
    return {
        "schema": EXECUTOR_SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "plan_identity_sha256": sha256_json(identity_payload),
        "queue": {
            "path": queue_locator,
            "sha256": change_set["queue"]["sha256"],
        },
        "change_set": {
            "change_set_id": change_set["change_set_id"],
            "path": change_set["path"],
            "sha256": change_set["sha256"],
            "maximum_mutating_entries": change_set[
                "maximum_mutating_entries"
            ],
        },
        "packages": plan_packages,
        "mutating_entry_count": len(change_set["entries"]),
        "change_set_entries": change_set["entries"],
        "queue_evaluation_sha256": evaluation.get("evaluation_sha256"),
    }


def _event(
    *,
    sequence: int,
    state: str,
    authority_id: str | None,
    authority_status: str | None,
    backend_result_identity_sha256: str | None,
    failure_code: str | None,
    consumer_effect: str,
) -> dict[str, Any]:
    return {
        "sequence": sequence,
        "state": state,
        "authority_id": authority_id,
        "authority_status": authority_status,
        "backend_result_identity_sha256": backend_result_identity_sha256,
        "failure_code": failure_code,
        "consumer_effect": consumer_effect,
    }


def _append_event(
    entry: dict[str, Any],
    *,
    state: str,
    authority_id: str | None = None,
    authority_status: str | None = None,
    backend_result_identity_sha256: str | None = None,
    failure_code: str | None = None,
    consumer_effect: str,
) -> None:
    entry["events"].append(
        _event(
            sequence=len(entry["events"]) + 1,
            state=state,
            authority_id=authority_id,
            authority_status=authority_status,
            backend_result_identity_sha256=backend_result_identity_sha256,
            failure_code=failure_code,
            consumer_effect=consumer_effect,
        )
    )
    entry["current_state"] = state


def _empty_boundaries() -> dict[str, Any]:
    return {
        "serial_execution": True,
        "append_only_journal": True,
        "noop_backend_dispatch_count": 0,
        "backend_dispatch_count": 0,
        "source_project_generation_count": 0,
        "render_count": 0,
        "yymm4_launch_count": 0,
        "electron_launch_count": 0,
        "render_driver_launch_count": 0,
        "ffmpeg_encode_count": 0,
        "playback_count": 0,
        "system_volume_operation_count": 0,
        "private_artifact_copy_count": 0,
        "product_write_count": 0,
        "human_or_rights_action_count": 0,
        "public_action_count": 0,
    }


def _new_journal(plan: Mapping[str, Any], *, execute: bool) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for row in plan["packages"]:
        state = row["initial_state"]
        if state == "verified_noop":
            consumer_effect = (
                "completed package validated and excluded from backend dispatch"
            )
            authority_status = "not_required"
        elif state == "planned":
            consumer_effect = "exact mutating entry planned without authority use"
            authority_status = "not_consumed"
        else:
            consumer_effect = "package is outside the exact change set"
            authority_status = "not_required"
        entries.append(
            {
                "order": row["order"],
                "package_id": row["package_id"],
                "descriptor_path": row["descriptor_path"],
                "descriptor_sha256": row["descriptor_sha256"],
                "technical_decision": row["technical_decision"],
                "requested_operation": row["requested_operation"],
                "from_lifecycle": (
                    row["normalized_lifecycle"]
                    if row["requested_operation"] is not None
                    else None
                ),
                "to_lifecycle": row["requested_target_lifecycle"],
                "events": [
                    _event(
                        sequence=1,
                        state=state,
                        authority_id=row["authority_id"],
                        authority_status=authority_status,
                        backend_result_identity_sha256=None,
                        failure_code=None,
                        consumer_effect=consumer_effect,
                    )
                ],
                "current_state": state,
            }
        )
    return {
        "schema": JOURNAL_SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "plan_identity_sha256": plan["plan_identity_sha256"],
        "queue": copy.deepcopy(plan["queue"]),
        "change_set": {
            "change_set_id": plan["change_set"]["change_set_id"],
            "path": plan["change_set"]["path"],
            "sha256": plan["change_set"]["sha256"],
        },
        "execution_mode": "execute" if execute else "plan_only",
        "status": "planned",
        "entries": entries,
        "counts": {},
        "boundaries": _empty_boundaries(),
    }


def _validate_resume_journal(
    *,
    repo_root: Path,
    journal_path: Path,
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    root = repo_root.resolve()
    _, resolved = _repo_locator(
        root,
        journal_path.as_posix(),
        field_path="$.resume_journal",
    )
    payload = _load_json(resolved, field_path="$.resume_journal")
    _require_mapping(
        payload,
        field_path="$.resume_journal",
        required=_JOURNAL_FIELDS,
        allowed=_JOURNAL_FIELDS,
    )
    _require_exact(
        payload["schema"],
        JOURNAL_SCHEMA,
        field_path="$.resume_journal.schema",
        code="journal_schema_mismatch",
    )
    _require_exact(
        payload["schema_version"],
        SCHEMA_VERSION,
        field_path="$.resume_journal.schema_version",
        code="journal_schema_mismatch",
    )
    if payload["status"] not in {
        "planned",
        "succeeded",
        "failed",
        "effect_unknown",
    }:
        _fail(
            "resume journal status is unknown",
            code="journal_state_invalid",
            field_path="$.resume_journal.status",
            consumer_effect="the last safe execution state is unknown",
        )
    if payload["execution_mode"] != "execute":
        _fail(
            "plan-only journal cannot be resumed as an execution",
            code="journal_mode_mismatch",
            field_path="$.resume_journal.execution_mode",
            consumer_effect="authority must not be consumed from a planning receipt",
        )
    comparisons = (
        (
            payload["plan_identity_sha256"],
            plan["plan_identity_sha256"],
            "plan_identity_sha256",
        ),
        (payload["queue"], plan["queue"], "queue"),
        (
            payload["change_set"],
            {
                "change_set_id": plan["change_set"]["change_set_id"],
                "path": plan["change_set"]["path"],
                "sha256": plan["change_set"]["sha256"],
            },
            "change_set",
        ),
    )
    for actual, expected, field in comparisons:
        if actual != expected:
            _fail(
                "resume journal does not match the current exact plan",
                code="journal_plan_mismatch",
                field_path=f"$.resume_journal.{field}",
                consumer_effect="completed effects cannot be mapped to a drifted plan",
            )
    entries = payload["entries"]
    if not isinstance(entries, list) or len(entries) != len(plan["packages"]):
        _fail(
            "resume journal package set differs from the plan",
            code="journal_package_set_mismatch",
            field_path="$.resume_journal.entries",
            consumer_effect="resume cannot skip or repeat packages safely",
        )
    for index, (entry, row) in enumerate(zip(entries, plan["packages"])):
        field_path = f"$.resume_journal.entries[{index}]"
        mapped = _require_mapping(
            entry,
            field_path=field_path,
            required=_JOURNAL_ENTRY_FIELDS,
            allowed=_JOURNAL_ENTRY_FIELDS,
        )
        expected_identity = {
            "order": row["order"],
            "package_id": row["package_id"],
            "descriptor_path": row["descriptor_path"],
            "descriptor_sha256": row["descriptor_sha256"],
            "technical_decision": row["technical_decision"],
            "requested_operation": row["requested_operation"],
            "from_lifecycle": (
                row["normalized_lifecycle"]
                if row["requested_operation"] is not None
                else None
            ),
            "to_lifecycle": row["requested_target_lifecycle"],
        }
        for key, expected in expected_identity.items():
            if mapped[key] != expected:
                _fail(
                    "resume journal package identity differs from the plan",
                    code="journal_package_identity_mismatch",
                    field_path=f"{field_path}.{key}",
                    consumer_effect="resume cannot skip or repeat packages safely",
                )
        events = mapped["events"]
        if not isinstance(events, list) or not events:
            _fail(
                "resume journal entry has no append-only history",
                code="journal_events_invalid",
                field_path=f"{field_path}.events",
                consumer_effect="the last safe package state is unknown",
            )
        for event_index, raw_event in enumerate(events):
            event_path = f"{field_path}.events[{event_index}]"
            event = _require_mapping(
                raw_event,
                field_path=event_path,
                required=_EVENT_FIELDS,
                allowed=_EVENT_FIELDS,
            )
            if event["sequence"] != event_index + 1:
                _fail(
                    "resume journal sequence is not append-only",
                    code="journal_sequence_invalid",
                    field_path=f"{event_path}.sequence",
                    consumer_effect="prior execution history may have been rewritten",
                )
            if event["state"] not in JOURNAL_STATES:
                _fail(
                    "resume journal contains an unknown state",
                    code="journal_state_invalid",
                    field_path=f"{event_path}.state",
                    consumer_effect="the last safe package state is unknown",
                )
            if (
                isinstance(event["sequence"], bool)
                or not isinstance(event["sequence"], int)
                or event["sequence"] < 1
            ):
                _fail(
                    "resume journal sequence is invalid",
                    code="journal_sequence_invalid",
                    field_path=f"{event_path}.sequence",
                    consumer_effect="prior execution history may have been rewritten",
                )
            authority_id = event["authority_id"]
            if authority_id is not None:
                _require_stable_id(
                    authority_id,
                    field_path=f"{event_path}.authority_id",
                )
            if event["authority_status"] not in {
                None,
                "not_required",
                "not_consumed",
                "validated",
                "consumed",
            }:
                _fail(
                    "resume journal authority status is invalid",
                    code="journal_authority_status_invalid",
                    field_path=f"{event_path}.authority_status",
                    consumer_effect="one-shot authority history is not trustworthy",
                )
            backend_identity = event["backend_result_identity_sha256"]
            if backend_identity is not None:
                _require_sha256(
                    backend_identity,
                    field_path=(
                        f"{event_path}.backend_result_identity_sha256"
                    ),
                )
            failure_code = event["failure_code"]
            if failure_code is not None:
                _require_stable_id(
                    failure_code,
                    field_path=f"{event_path}.failure_code",
                )
            consumer_effect = event["consumer_effect"]
            if (
                not isinstance(consumer_effect, str)
                or not consumer_effect
                or len(consumer_effect) > 256
                or "\\" in consumer_effect
                or re.search(r"[A-Za-z]:[/\\]", consumer_effect)
            ):
                _fail(
                    "resume journal consumer effect is not sanitized",
                    code="journal_consumer_effect_invalid",
                    field_path=f"{event_path}.consumer_effect",
                    consumer_effect="private or machine-local text cannot be replayed",
                )
        if mapped["current_state"] != events[-1]["state"]:
            _fail(
                "resume journal current state is not its last event",
                code="journal_state_invalid",
                field_path=f"{field_path}.current_state",
                consumer_effect="prior execution history may have been rewritten",
            )
    counts = _require_mapping(
        payload["counts"],
        field_path="$.resume_journal.counts",
        required=_COUNT_FIELDS,
        allowed=_COUNT_FIELDS,
    )
    for key, value in counts.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            _fail(
                "resume journal count is invalid",
                code="journal_counts_invalid",
                field_path=f"$.resume_journal.counts.{key}",
                consumer_effect="aggregate execution history is not trustworthy",
            )
    boundaries = _require_mapping(
        payload["boundaries"],
        field_path="$.resume_journal.boundaries",
        required=_BOUNDARY_FIELDS,
        allowed=_BOUNDARY_FIELDS,
    )
    for key, value in boundaries.items():
        if key in {"serial_execution", "append_only_journal"}:
            if value is not True:
                _fail(
                    "resume journal lost its serial append-only boundary",
                    code="journal_boundaries_invalid",
                    field_path=f"$.resume_journal.boundaries.{key}",
                    consumer_effect="resume cannot broaden the executor contract",
                )
        elif isinstance(value, bool) or not isinstance(value, int) or value < 0:
            _fail(
                "resume journal boundary count is invalid",
                code="journal_boundaries_invalid",
                field_path=f"$.resume_journal.boundaries.{key}",
                consumer_effect="effect history is not trustworthy",
            )
    derived = copy.deepcopy(payload)
    _refresh_summaries(derived)
    if derived["counts"] != payload["counts"] or derived["status"] != payload["status"]:
        _fail(
            "resume journal summaries do not match append-only events",
            code="journal_summary_mismatch",
            field_path="$.resume_journal",
            consumer_effect="resume cannot rely on rewritten aggregate state",
        )
    if (
        payload["boundaries"]["backend_dispatch_count"]
        != payload["counts"]["authority_consumptions"]
    ):
        _fail(
            "resume journal dispatch count differs from authority consumption",
            code="journal_summary_mismatch",
            field_path="$.resume_journal.boundaries.backend_dispatch_count",
            consumer_effect="one-shot authority use cannot be counted safely",
        )
    return copy.deepcopy(payload)


def _load_authorities(
    *,
    repo_root: Path,
    authority_path: Path | None,
) -> list[dict[str, Any]]:
    if authority_path is None:
        return []
    root = repo_root.resolve()
    _, resolved = _repo_locator(
        root,
        authority_path.as_posix(),
        field_path="$.authority_file",
    )
    payload = _load_json(resolved, field_path="$.authority_file")
    _require_mapping(
        payload,
        field_path="$.authority_file",
        required=_AUTHORITY_SET_FIELDS,
        allowed=_AUTHORITY_SET_FIELDS,
    )
    _require_exact(
        payload["schema"],
        AUTHORITY_SET_SCHEMA,
        field_path="$.authority_file.schema",
        code="authority_schema_mismatch",
    )
    _require_exact(
        payload["schema_version"],
        SCHEMA_VERSION,
        field_path="$.authority_file.schema_version",
        code="authority_schema_mismatch",
    )
    records = payload["authorities"]
    if (
        not isinstance(records, list)
        or not records
        or len(records) > HARD_MAXIMUM_MUTATING_ENTRIES
    ):
        _fail(
            "authority set must contain a bounded non-empty record list",
            code="authority_set_invalid",
            field_path="$.authority_file.authorities",
            consumer_effect="one-shot authorities cannot be selected",
        )
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw_record in enumerate(records):
        field_path = f"$.authority_file.authorities[{index}]"
        record = _require_mapping(
            raw_record,
            field_path=field_path,
            required=_AUTHORITY_FIELDS,
            allowed=_AUTHORITY_FIELDS,
        )
        _require_exact(
            record["schema"],
            AUTHORITY_RECORD_SCHEMA,
            field_path=f"{field_path}.schema",
            code="authority_schema_mismatch",
        )
        authority_id = _require_stable_id(
            record["authority_id"],
            field_path=f"{field_path}.authority_id",
        )
        if authority_id in seen:
            _fail(
                "authority set contains a duplicate authority ID",
                code="authority_duplicate",
                field_path=f"{field_path}.authority_id",
                consumer_effect="one-shot use cannot be counted deterministically",
            )
        seen.add(authority_id)
        replacement = record["replaces_authority_id"]
        if replacement is not None:
            replacement = _require_stable_id(
                replacement,
                field_path=f"{field_path}.replaces_authority_id",
            )
        queue = _require_mapping(
            record["queue"],
            field_path=f"{field_path}.queue",
            required=_BOUND_FILE_FIELDS,
            allowed=_BOUND_FILE_FIELDS,
        )
        _repo_locator(
            root,
            queue["path"],
            field_path=f"{field_path}.queue.path",
        )
        _require_sha256(
            queue["sha256"],
            field_path=f"{field_path}.queue.sha256",
        )
        change_set = _require_mapping(
            record["change_set"],
            field_path=f"{field_path}.change_set",
            required=_AUTHORITY_CHANGE_SET_FIELDS,
            allowed=_AUTHORITY_CHANGE_SET_FIELDS,
        )
        _require_stable_id(
            change_set["change_set_id"],
            field_path=f"{field_path}.change_set.change_set_id",
        )
        _require_sha256(
            change_set["sha256"],
            field_path=f"{field_path}.change_set.sha256",
        )
        package = _require_mapping(
            record["package"],
            field_path=f"{field_path}.package",
            required=_AUTHORITY_PACKAGE_FIELDS,
            allowed=_AUTHORITY_PACKAGE_FIELDS,
        )
        _require_stable_id(
            package["package_id"],
            field_path=f"{field_path}.package.package_id",
        )
        _repo_locator(
            root,
            package["descriptor_path"],
            field_path=f"{field_path}.package.descriptor_path",
        )
        _require_sha256(
            package["descriptor_sha256"],
            field_path=f"{field_path}.package.descriptor_sha256",
        )
        constraints = _require_mapping(
            record["constraints"],
            field_path=f"{field_path}.constraints",
            required=_AUTHORITY_CONSTRAINT_FIELDS,
            allowed=_AUTHORITY_CONSTRAINT_FIELDS,
        )
        expected_constraints = {
            "serial_only": True,
            "exact_identity_recheck": True,
            "private_artifact_copy": False,
            "human_acceptance": False,
            "rights": False,
            "production": False,
            "publication": False,
            "upload": False,
            "release": False,
        }
        if dict(constraints) != expected_constraints:
            _fail(
                "authority constraints exceed the technical executor boundary",
                code="authority_constraints_invalid",
                field_path=f"{field_path}.constraints",
                consumer_effect="external or private effects remain forbidden",
            )
        result.append(
            {
                **dict(record),
                "authority_id": authority_id,
                "replaces_authority_id": replacement,
            }
        )
    return result


def _used_authority_ids(journal: Mapping[str, Any]) -> set[str]:
    return {
        str(event["authority_id"])
        for entry in journal["entries"]
        for event in entry["events"]
        if event["state"] == "started" and event["authority_id"] is not None
    }


def _last_consumed_authority(entry: Mapping[str, Any]) -> str | None:
    consumed = [
        event["authority_id"]
        for event in entry["events"]
        if event["state"] == "started" and event["authority_id"] is not None
    ]
    return str(consumed[-1]) if consumed else None


def _select_authority(
    *,
    authorities: list[dict[str, Any]],
    plan: Mapping[str, Any],
    change_entry: Mapping[str, Any],
    journal_entry: Mapping[str, Any],
    used_authorities: set[str],
) -> dict[str, Any]:
    previous = (
        _last_consumed_authority(journal_entry)
        if journal_entry["current_state"] == "failed"
        else None
    )
    if previous is None:
        candidates = [
            record
            for record in authorities
            if record["authority_id"] == change_entry["authority_id"]
            and record["replaces_authority_id"] is None
        ]
    else:
        candidates = [
            record
            for record in authorities
            if record["replaces_authority_id"] == previous
            and record["authority_id"] != previous
        ]
    if len(candidates) != 1:
        _fail(
            "one exact available authority record is required",
            code=(
                "resume_new_authority_required"
                if previous is not None
                else "authority_missing_or_ambiguous"
            ),
            field_path="$.authority_file",
            consumer_effect="the backend remains undispatched",
        )
    record = candidates[0]
    if record["authority_id"] in used_authorities:
        _fail(
            "authority was already consumed by this journal",
            code="authority_already_consumed",
            field_path="$.authority_file.authority_id",
            consumer_effect="one-shot authority cannot be reused",
        )
    expected = {
        "queue": plan["queue"],
        "change_set": {
            "change_set_id": plan["change_set"]["change_set_id"],
            "sha256": plan["change_set"]["sha256"],
        },
        "package": {
            "package_id": change_entry["package_id"],
            "descriptor_path": change_entry["descriptor_path"],
            "descriptor_sha256": change_entry["descriptor_sha256"],
        },
        "from_lifecycle": change_entry["expected_current_lifecycle"],
        "to_lifecycle": change_entry["requested_target_lifecycle"],
        "operation": change_entry["operation"],
        "maximum_use_count": 1,
        "status": "available",
    }
    for key, value in expected.items():
        if record[key] != value:
            _fail(
                "authority does not match the exact package effect",
                code=f"authority_{key}_mismatch",
                field_path=f"$.authority_file.{key}",
                consumer_effect="the backend remains undispatched",
            )
    return record


def _consume_authority_file(
    *,
    repo_root: Path,
    authority_path: Path | None,
    expected_record: Mapping[str, Any],
) -> None:
    if authority_path is None:
        _fail(
            "mutating execution requires a writable one-shot authority file",
            code="authority_file_missing",
            field_path="$.authority_file",
            consumer_effect="the backend remains undispatched",
        )
    root = repo_root.resolve()
    _, resolved = _repo_locator(
        root,
        authority_path.as_posix(),
        field_path="$.authority_file",
    )
    payload = _load_json(resolved, field_path="$.authority_file")
    records = payload.get("authorities")
    if not isinstance(records, list):
        _fail(
            "authority set changed before consumption",
            code="authority_consumption_drift",
            field_path="$.authority_file.authorities",
            consumer_effect="the backend remains undispatched",
        )
    matching = [
        record
        for record in records
        if isinstance(record, Mapping)
        and record.get("authority_id") == expected_record["authority_id"]
    ]
    if len(matching) != 1 or dict(matching[0]) != dict(expected_record):
        _fail(
            "authority record changed before consumption",
            code="authority_consumption_drift",
            field_path="$.authority_file.authorities",
            consumer_effect="the backend remains undispatched",
        )
    if matching[0].get("status") != "available":
        _fail(
            "authority is no longer available",
            code="authority_already_consumed",
            field_path="$.authority_file.status",
            consumer_effect="one-shot authority cannot be reused",
        )
    matching[0]["status"] = "consumed"
    temporary = resolved.with_name(f".{resolved.name}.consume.tmp")
    if temporary.exists():
        _fail(
            "authority consumption temporary file already exists",
            code="authority_consumption_collision",
            field_path="$.authority_file",
            consumer_effect="the backend remains undispatched",
        )
    try:
        with temporary.open("xb") as handle:
            handle.write(canonical_json_bytes(payload))
            handle.flush()
        temporary.replace(resolved)
    except OSError as exc:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise FactoryQueueExecutorError(
            "authority consumption could not be persisted",
            code="authority_consumption_write_failed",
            field_path="$.authority_file",
            consumer_effect="the backend remains undispatched",
        ) from exc


def _default_advancement_backend(
    *,
    repo_root: Path,
    queue_path: Path,
    package_id: str,
    to_lifecycle: str,
    authority_id: str,
    execute: bool,
) -> Mapping[str, Any]:
    return advance_factory_package(
        repo_root=repo_root,
        queue_path=queue_path,
        package_id=package_id,
        to_lifecycle=to_lifecycle,
        authority_id=authority_id,
        execute=execute,
        persist_failure=True,
    )


def _safe_failure_code(value: Any, *, fallback: str) -> str:
    if isinstance(value, str) and _STABLE_ID.fullmatch(value):
        return value
    return fallback


def _apply_backend_boundaries(
    journal: dict[str, Any],
    *,
    change_entry: Mapping[str, Any],
    backend_result: Mapping[str, Any],
    succeeded: bool,
) -> None:
    boundaries = journal["boundaries"]
    raw = backend_result.get("boundaries")
    backend_boundaries = raw if isinstance(raw, Mapping) else {}
    if succeeded:
        if change_entry["operation"] == "source_project_generation":
            boundaries["source_project_generation_count"] += 1
        elif change_entry["operation"] == "render":
            boundaries["render_count"] += 1
    integer_sources = {
        "yymm4_launch_count": ("yymm4_launch_count",),
        "electron_launch_count": ("electron_launch_count",),
        "render_driver_launch_count": ("render_driver_launch_count",),
        "ffmpeg_encode_count": ("ffmpeg_encode_count",),
        "playback_count": ("playback_count", "preview_playback_count"),
        "system_volume_operation_count": ("system_volume_operation_count",),
        "private_artifact_copy_count": ("private_artifact_copy_count",),
        "product_write_count": ("product_write_count",),
        "human_or_rights_action_count": (
            "human_or_rights_action_count",
        ),
        "public_action_count": ("public_action_count",),
    }
    for target, candidates in integer_sources.items():
        for candidate in candidates:
            value = backend_boundaries.get(candidate)
            if isinstance(value, int) and not isinstance(value, bool):
                boundaries[target] += max(0, value)
                break
    boolean_sources = {
        "electron_launch_count": "electron_launched",
        "render_driver_launch_count": "render_driver_launched",
        "ffmpeg_encode_count": "ffmpeg_encode_performed",
        "playback_count": "media_playback",
        "system_volume_operation_count": "system_volume_operation",
        "private_artifact_copy_count": "private_artifacts_copied",
        "product_write_count": "product_artifacts_written",
        "human_or_rights_action_count": "human_or_rights_authority_granted",
    }
    for target, source in boolean_sources.items():
        if backend_boundaries.get(source) is True:
            boundaries[target] += 1


def _refresh_summaries(journal: dict[str, Any]) -> None:
    states = [entry["current_state"] for entry in journal["entries"]]
    journal["counts"] = {
        "packages_validated": len(states),
        "verified_noop": states.count("verified_noop"),
        "not_selected": states.count("not_selected"),
        "planned": states.count("planned"),
        "succeeded": states.count("succeeded"),
        "failed": states.count("failed"),
        "effect_unknown": states.count("effect_unknown"),
        "skipped_after_failure": states.count("skipped_after_failure"),
        "authority_consumptions": sum(
            event["state"] == "started"
            for entry in journal["entries"]
            for event in entry["events"]
        ),
    }
    journal["boundaries"]["backend_dispatch_count"] = journal["counts"][
        "authority_consumptions"
    ]
    if journal["execution_mode"] == "plan_only":
        journal["status"] = "planned"
    elif journal["counts"]["effect_unknown"]:
        journal["status"] = "effect_unknown"
    elif journal["counts"]["failed"]:
        journal["status"] = "failed"
    elif journal["counts"]["skipped_after_failure"]:
        journal["status"] = "failed"
    elif journal["counts"]["planned"]:
        journal["status"] = "failed"
    else:
        journal["status"] = "succeeded"


def _execution_result(
    *,
    plan: Mapping[str, Any],
    journal: dict[str, Any],
) -> dict[str, Any]:
    _refresh_summaries(journal)
    journal_identity = sha256_json(journal)
    receipt = {
        "schema": "nlmytgen.factory_queue.execution_receipt.v1",
        "schema_version": SCHEMA_VERSION,
        "status": journal["status"],
        "plan_identity_sha256": plan["plan_identity_sha256"],
        "journal_sha256": journal_identity,
        "queue_evaluation_sha256": plan["queue_evaluation_sha256"],
        "counts": copy.deepcopy(journal["counts"]),
        "boundaries": copy.deepcopy(journal["boundaries"]),
    }
    result = {
        "schema": EXECUTION_RESULT_SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "status": journal["status"],
        "plan": {
            "schema": plan["schema"],
            "schema_version": plan["schema_version"],
            "plan_identity_sha256": plan["plan_identity_sha256"],
            "queue": copy.deepcopy(plan["queue"]),
            "change_set": copy.deepcopy(plan["change_set"]),
            "package_count": len(plan["packages"]),
            "mutating_entry_count": plan["mutating_entry_count"],
        },
        "journal": journal,
        "execution_receipt": receipt,
    }
    result["execution_receipt_sha256"] = sha256_json(receipt)
    return result


def execute_factory_queue(
    *,
    repo_root: Path,
    queue_path: Path,
    change_set_path: Path,
    authority_path: Path | None = None,
    execute: bool = False,
    resume_journal_path: Path | None = None,
    queue_evaluator: QueueEvaluator = evaluate_factory_queue,
    advancement_backend: AdvancementBackend = _default_advancement_backend,
) -> dict[str, Any]:
    """Plan or execute one exact, bounded, serial queue change set."""

    root = repo_root.resolve()
    plan = _build_plan(
        repo_root=root,
        queue_path=queue_path,
        change_set_path=change_set_path,
        queue_evaluator=queue_evaluator,
    )
    if resume_journal_path is not None and not execute:
        _fail(
            "resume journal requires explicit execute mode",
            code="journal_resume_requires_execute",
            field_path="$.resume_journal",
            consumer_effect="planning never consumes or resumes authority",
        )
    journal = (
        _validate_resume_journal(
            repo_root=root,
            journal_path=resume_journal_path,
            plan=plan,
        )
        if resume_journal_path is not None
        else _new_journal(plan, execute=execute)
    )
    if not execute:
        return _execution_result(plan=plan, journal=journal)

    if any(
        entry["current_state"] == "effect_unknown"
        for entry in journal["entries"]
    ):
        _fail(
            "effect-unknown journal requires read-only reconciliation",
            code="effect_unknown_retry_forbidden",
            field_path="$.resume_journal.entries",
            consumer_effect="no backend is automatically retried",
        )

    change_entries = {
        entry["package_id"]: entry for entry in plan["change_set_entries"]
    }
    authorities = _load_authorities(
        repo_root=root,
        authority_path=authority_path,
    )
    failure_index: int | None = None
    for index, journal_entry in enumerate(journal["entries"]):
        state = journal_entry["current_state"]
        if state in {"verified_noop", "not_selected", "succeeded"}:
            continue
        change_entry = change_entries.get(journal_entry["package_id"])
        if change_entry is None:
            continue
        if state == "effect_unknown":
            _fail(
                "effect-unknown entry cannot be automatically retried",
                code="effect_unknown_retry_forbidden",
                field_path=f"$.resume_journal.entries[{index}]",
                consumer_effect="read-only reconciliation is required",
            )

        refreshed = _build_plan(
            repo_root=root,
            queue_path=queue_path,
            change_set_path=change_set_path,
            queue_evaluator=queue_evaluator,
        )
        if refreshed["plan_identity_sha256"] != plan["plan_identity_sha256"]:
            _fail(
                "queue or package identity changed before backend dispatch",
                code="execution_pre_effect_plan_drift",
                field_path=f"$.entries[{index}]",
                consumer_effect="the authority remains unused",
            )
        authorities = _load_authorities(
            repo_root=root,
            authority_path=authority_path,
        )
        authority = _select_authority(
            authorities=authorities,
            plan=plan,
            change_entry=change_entry,
            journal_entry=journal_entry,
            used_authorities=_used_authority_ids(journal),
        )
        _append_event(
            journal_entry,
            state="authority_validated",
            authority_id=authority["authority_id"],
            authority_status="validated",
            consumer_effect="exact one-shot authority validated before effect",
        )
        _consume_authority_file(
            repo_root=root,
            authority_path=authority_path,
            expected_record=authority,
        )
        _append_event(
            journal_entry,
            state="started",
            authority_id=authority["authority_id"],
            authority_status="consumed",
            consumer_effect="authority consumed immediately before backend dispatch",
        )
        try:
            backend_result = advancement_backend(
                repo_root=root,
                queue_path=queue_path,
                package_id=change_entry["package_id"],
                to_lifecycle=change_entry["requested_target_lifecycle"],
                authority_id=authority["authority_id"],
                execute=True,
            )
        except Exception:
            _append_event(
                journal_entry,
                state="effect_unknown",
                authority_id=authority["authority_id"],
                authority_status="consumed",
                failure_code="backend_effect_unknown",
                consumer_effect=(
                    "backend result is unknown and automatic retry is forbidden"
                ),
            )
            failure_index = index
            break
        if not isinstance(backend_result, Mapping):
            _append_event(
                journal_entry,
                state="effect_unknown",
                authority_id=authority["authority_id"],
                authority_status="consumed",
                failure_code="backend_result_invalid",
                consumer_effect=(
                    "backend result is unknown and automatic retry is forbidden"
                ),
            )
            failure_index = index
            break
        backend_identity = sha256_json(backend_result)
        backend_status = backend_result.get("status")
        if backend_status == "effect_unknown":
            _append_event(
                journal_entry,
                state="effect_unknown",
                authority_id=authority["authority_id"],
                authority_status="consumed",
                backend_result_identity_sha256=backend_identity,
                failure_code=_safe_failure_code(
                    backend_result.get("error_code"),
                    fallback="backend_effect_unknown",
                ),
                consumer_effect=(
                    "backend result is unknown and automatic retry is forbidden"
                ),
            )
            _apply_backend_boundaries(
                journal,
                change_entry=change_entry,
                backend_result=backend_result,
                succeeded=False,
            )
            failure_index = index
            break
        if (
            backend_status in {"failed", "error"}
            and backend_result.get("effect_performed") is False
        ):
            _append_event(
                journal_entry,
                state="failed",
                authority_id=authority["authority_id"],
                authority_status="consumed",
                backend_result_identity_sha256=backend_identity,
                failure_code=_safe_failure_code(
                    backend_result.get("error_code"),
                    fallback="backend_failed_before_effect",
                ),
                consumer_effect=(
                    "known non-effect failure stopped all later mutating entries"
                ),
            )
            _apply_backend_boundaries(
                journal,
                change_entry=change_entry,
                backend_result=backend_result,
                succeeded=False,
            )
            failure_index = index
            break
        _append_event(
            journal_entry,
            state="succeeded",
            authority_id=authority["authority_id"],
            authority_status="consumed",
            backend_result_identity_sha256=backend_identity,
            consumer_effect="exact backend effect completed once",
        )
        _apply_backend_boundaries(
            journal,
            change_entry=change_entry,
            backend_result=backend_result,
            succeeded=True,
        )

    if failure_index is not None:
        for later in journal["entries"][failure_index + 1 :]:
            if later["requested_operation"] is None:
                continue
            if later["current_state"] in {
                "planned",
                "authority_validated",
                "started",
            }:
                _append_event(
                    later,
                    state="skipped_after_failure",
                    authority_id=later["events"][-1]["authority_id"],
                    authority_status="not_consumed",
                    failure_code="earlier_mutating_entry_failed",
                    consumer_effect=(
                        "serial stop prevented every later backend dispatch"
                    ),
                )
    return _execution_result(plan=plan, journal=journal)


__all__ = [
    "AUTHORITY_RECORD_SCHEMA",
    "AUTHORITY_SET_SCHEMA",
    "CHANGE_SET_SCHEMA",
    "EXECUTION_RESULT_SCHEMA",
    "FactoryQueueExecutorError",
    "JOURNAL_SCHEMA",
    "execute_factory_queue",
]
