from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping

import pytest

from src.cli import main as cli
from src.pipeline.factory_queue import (
    evaluate_factory_queue,
    sha256_file,
    sha256_json,
)
from src.pipeline.factory_queue_executor import (
    AUTHORITY_SET_SCHEMA,
    CHANGE_SET_SCHEMA,
    JOURNAL_SCHEMA,
    FactoryQueueExecutorError,
    execute_factory_queue,
)


ROOT = Path(__file__).resolve().parents[1]
QUEUE_V3 = Path(
    "production_pilots/factory_queues/four_package_lifecycle_queue_v3.json"
)
ZERO_CHANGE_SET = Path(
    "production_pilots/factory_queues/four_package_zero_change_set_v1.json"
)
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


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _hex(seed: int) -> str:
    return hashlib.sha256(f"synthetic-{seed}".encode()).hexdigest()


def _contract() -> dict[str, Any]:
    return {
        "schema": "nlmytgen.factory_queue.execution_contract.v1",
        "change_set_schema_path": CHANGE_SET_SCHEMA_PATH.as_posix(),
        "change_set_schema_sha256": sha256_file(ROOT / CHANGE_SET_SCHEMA_PATH),
        "authority_schema_path": AUTHORITY_SCHEMA_PATH.as_posix(),
        "authority_schema_sha256": sha256_file(ROOT / AUTHORITY_SCHEMA_PATH),
        "journal_schema_path": JOURNAL_SCHEMA_PATH.as_posix(),
        "journal_schema_sha256": sha256_file(ROOT / JOURNAL_SCHEMA_PATH),
    }


def _execution_policy() -> dict[str, Any]:
    return {
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


def _receipt_policy() -> dict[str, Any]:
    return {
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


def _constraints() -> dict[str, Any]:
    return {
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


def _authority_record(
    fixture: Mapping[str, Any],
    entry: Mapping[str, Any],
    *,
    authority_id: str | None = None,
    replaces_authority_id: str | None = None,
) -> dict[str, Any]:
    return {
        "schema": "nlmytgen.factory_queue.execution_authority.v1",
        "authority_id": authority_id or entry["authority_id"],
        "replaces_authority_id": replaces_authority_id,
        "queue": {
            "path": fixture["queue_path"].as_posix(),
            "sha256": sha256_file(ROOT / fixture["queue_path"]),
        },
        "change_set": {
            "change_set_id": fixture["change_set"]["change_set_id"],
            "sha256": sha256_file(ROOT / fixture["change_set_path"]),
        },
        "package": {
            "package_id": entry["package_id"],
            "descriptor_path": entry["descriptor_path"],
            "descriptor_sha256": entry["descriptor_sha256"],
        },
        "from_lifecycle": entry["expected_current_lifecycle"],
        "to_lifecycle": entry["requested_target_lifecycle"],
        "operation": entry["operation"],
        "maximum_use_count": 1,
        "status": "available",
        "constraints": _constraints(),
    }


@contextmanager
def _synthetic_fixture(
    *,
    mutating_count: int = 1,
    include_noop: bool = True,
) -> Iterator[dict[str, Any]]:
    with tempfile.TemporaryDirectory(
        prefix=".factory-executor-test-",
        dir=ROOT,
    ) as temp:
        temp_root = Path(temp)
        rows: list[dict[str, Any]] = []
        queue_entries: list[dict[str, Any]] = []
        change_entries: list[dict[str, Any]] = []
        for index in range(1, mutating_count + 1):
            package_id = f"synthetic_package_{index:03d}"
            descriptor = temp_root / f"descriptor-{index}.json"
            _write_json(descriptor, {"package_id": package_id, "fixture": True})
            descriptor_path = _relative(descriptor)
            content = _hex(100 + index)
            render = _hex(200 + index)
            target = _hex(300 + index)
            descriptor_hash = sha256_file(descriptor)
            queue_entries.append(
                {
                    "order": index,
                    "descriptor_path": descriptor_path,
                    "expected_package_id": package_id,
                    "expected_content_identity_sha256": content,
                    "expected_render_settings_sha256": render,
                    "expected_completed_output_sha256": None,
                }
            )
            rows.append(
                {
                    "order": index,
                    "priority": 50,
                    "descriptor_path": descriptor_path,
                    "descriptor_sha256": descriptor_hash,
                    "package_id": package_id,
                    "content_identity_sha256": content,
                    "render_settings_identity_sha256": render,
                    "target_identity_sha256": target,
                    "normalized_lifecycle": "package_prepared",
                    "technical_decision": "source_project_generation_required",
                }
            )
            change_entries.append(
                {
                    "order": index,
                    "package_id": package_id,
                    "descriptor_path": descriptor_path,
                    "descriptor_sha256": descriptor_hash,
                    "expected_content_identity_sha256": content,
                    "expected_render_settings_identity_sha256": render,
                    "expected_completed_output_sha256": None,
                    "expected_target_identity_sha256": target,
                    "expected_current_lifecycle": "package_prepared",
                    "requested_target_lifecycle": "source_project_ready",
                    "operation": "source_project_generation",
                    "authority_id": f"synthetic_authority_{index:03d}",
                }
            )
        if include_noop:
            order = mutating_count + 1
            package_id = "synthetic_completed_001"
            descriptor = temp_root / "descriptor-noop.json"
            _write_json(descriptor, {"package_id": package_id, "fixture": True})
            descriptor_path = _relative(descriptor)
            descriptor_hash = sha256_file(descriptor)
            queue_entries.append(
                {
                    "order": order,
                    "descriptor_path": descriptor_path,
                    "expected_package_id": package_id,
                    "expected_content_identity_sha256": _hex(401),
                    "expected_render_settings_sha256": _hex(402),
                    "expected_completed_output_sha256": _hex(403),
                }
            )
            rows.append(
                {
                    "order": order,
                    "priority": 50,
                    "descriptor_path": descriptor_path,
                    "descriptor_sha256": descriptor_hash,
                    "package_id": package_id,
                    "content_identity_sha256": _hex(401),
                    "render_settings_identity_sha256": _hex(402),
                    "target_identity_sha256": _hex(404),
                    "normalized_lifecycle": "rendered",
                    "technical_decision": "verified_noop",
                }
            )
        queue_path_abs = temp_root / "queue.json"
        _write_json(queue_path_abs, {"queue": {"packages": queue_entries}})
        queue_path = queue_path_abs.relative_to(ROOT)
        change_set = {
            "schema": CHANGE_SET_SCHEMA,
            "schema_version": "1.0",
            "contract": _contract(),
            "change_set_id": "synthetic_change_set_v1",
            "queue": {
                "path": queue_path.as_posix(),
                "sha256": sha256_file(queue_path_abs),
            },
            "maximum_mutating_entries": mutating_count,
            "execution_policy": _execution_policy(),
            "entries": change_entries,
            "receipt_policy": _receipt_policy(),
        }
        change_set_abs = temp_root / "change-set.json"
        _write_json(change_set_abs, change_set)
        change_set_path = change_set_abs.relative_to(ROOT)
        fixture: dict[str, Any] = {
            "root": temp_root,
            "queue_path": queue_path,
            "queue_rows": rows,
            "queue_entries": queue_entries,
            "change_set": change_set,
            "change_set_path": change_set_path,
            "change_entries": change_entries,
        }
        authority_payload = {
            "schema": AUTHORITY_SET_SCHEMA,
            "schema_version": "1.0",
            "authorities": [
                _authority_record(fixture, entry) for entry in change_entries
            ],
        }
        authority_abs = temp_root / "authorities.json"
        _write_json(authority_abs, authority_payload)
        fixture["authority_payload"] = authority_payload
        fixture["authority_path"] = authority_abs.relative_to(ROOT)

        def evaluator(
            *,
            repo_root: Path,
            queue_path: Path,
            check_live: bool,
        ) -> dict[str, Any]:
            assert repo_root == ROOT
            assert queue_path == fixture["queue_path"]
            assert check_live is True
            result = {
                "schema": "nlmytgen.factory_queue_evaluation.v1",
                "schema_version": "1.0",
                "status": "passed",
                "queue_descriptor": {
                    "path": fixture["queue_path"].as_posix(),
                    "sha256": sha256_file(ROOT / fixture["queue_path"]),
                },
                "packages": copy.deepcopy(fixture["queue_rows"]),
            }
            result["evaluation_sha256"] = sha256_json(result)
            return result

        fixture["evaluator"] = evaluator
        yield fixture


def _execute_synthetic(
    fixture: Mapping[str, Any],
    backend: Callable[..., Mapping[str, Any]],
    *,
    authority_path: Path | None = None,
    resume_journal_path: Path | None = None,
) -> dict[str, Any]:
    return execute_factory_queue(
        repo_root=ROOT,
        queue_path=fixture["queue_path"],
        change_set_path=fixture["change_set_path"],
        authority_path=authority_path or fixture["authority_path"],
        execute=True,
        resume_journal_path=resume_journal_path,
        queue_evaluator=fixture["evaluator"],
        advancement_backend=backend,
    )


def test_versioned_schemas_and_zero_change_set_bind_exact_hashes() -> None:
    change_schema = json.loads(
        (ROOT / CHANGE_SET_SCHEMA_PATH).read_text(encoding="utf-8")
    )
    authority_schema = json.loads(
        (ROOT / AUTHORITY_SCHEMA_PATH).read_text(encoding="utf-8")
    )
    journal_schema = json.loads(
        (ROOT / JOURNAL_SCHEMA_PATH).read_text(encoding="utf-8")
    )
    zero = json.loads((ROOT / ZERO_CHANGE_SET).read_text(encoding="utf-8"))
    assert change_schema["$id"] == CHANGE_SET_SCHEMA
    assert authority_schema["$id"] == AUTHORITY_SET_SCHEMA
    assert journal_schema["$id"] == JOURNAL_SCHEMA
    assert zero["maximum_mutating_entries"] == 0
    assert zero["entries"] == []
    assert zero["queue"]["sha256"] == sha256_file(ROOT / QUEUE_V3)
    assert zero["contract"]["change_set_schema_sha256"] == sha256_file(
        ROOT / CHANGE_SET_SCHEMA_PATH
    )
    assert zero["contract"]["authority_schema_sha256"] == sha256_file(
        ROOT / AUTHORITY_SCHEMA_PATH
    )
    assert zero["contract"]["journal_schema_sha256"] == sha256_file(
        ROOT / JOURNAL_SCHEMA_PATH
    )


def test_real_zero_change_plan_is_deterministic_and_plan_only() -> None:
    first = execute_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE_V3,
        change_set_path=ZERO_CHANGE_SET,
    )
    second = execute_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE_V3,
        change_set_path=ZERO_CHANGE_SET,
    )
    assert first == second
    assert first["status"] == "planned"
    assert first["journal"]["counts"]["verified_noop"] == 4
    assert first["journal"]["counts"]["authority_consumptions"] == 0
    assert first["journal"]["boundaries"]["backend_dispatch_count"] == 0


def test_real_zero_change_execute_dispatches_no_backend() -> None:
    def forbidden_backend(**_: Any) -> Mapping[str, Any]:
        raise AssertionError("real zero change set reached a backend")

    first = execute_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE_V3,
        change_set_path=ZERO_CHANGE_SET,
        execute=True,
        advancement_backend=forbidden_backend,
    )
    second = execute_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE_V3,
        change_set_path=ZERO_CHANGE_SET,
        execute=True,
        advancement_backend=forbidden_backend,
    )
    assert first == second
    assert first["status"] == "succeeded"
    assert first["journal"]["counts"]["verified_noop"] == 4
    assert set(
        value
        for key, value in first["journal"]["boundaries"].items()
        if key.endswith("_count")
    ) == {0}


def test_recorded_only_private_absence_remains_non_mutating() -> None:
    def tracked_only_evaluator(
        *,
        repo_root: Path,
        queue_path: Path,
        check_live: bool,
    ) -> dict[str, Any]:
        assert check_live is True
        return evaluate_factory_queue(
            repo_root=repo_root,
            queue_path=queue_path,
            check_live=False,
        )

    result = execute_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE_V3,
        change_set_path=ZERO_CHANGE_SET,
        execute=True,
        queue_evaluator=tracked_only_evaluator,
    )
    assert result["status"] == "succeeded"
    assert [row["technical_decision"] for row in result["journal"]["entries"]] == [
        "recorded_complete_no_live_file",
    ] * 4
    assert result["journal"]["boundaries"]["backend_dispatch_count"] == 0
    assert result["journal"]["boundaries"]["private_artifact_copy_count"] == 0


def test_public_cli_defaults_to_plan_only_and_zero_exit(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = cli.main(
        [
            "execute-factory-queue",
            "--queue",
            QUEUE_V3.as_posix(),
            "--change-set",
            ZERO_CHANGE_SET.as_posix(),
            "--format",
            "json",
        ]
    )
    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["status"] == "planned"
    assert payload["journal"]["execution_mode"] == "plan_only"


def test_one_exact_authorized_entry_dispatches_once_and_noop_never_dispatches() -> None:
    with _synthetic_fixture() as fixture:
        calls: list[str] = []

        def backend(**kwargs: Any) -> Mapping[str, Any]:
            calls.append(kwargs["package_id"])
            return {
                "status": "promoted",
                "boundaries": {"product_write_count": 0},
            }

        result = _execute_synthetic(fixture, backend)
        consumed_status = json.loads(
            (ROOT / fixture["authority_path"]).read_text(encoding="utf-8")
        )["authorities"][0]["status"]
    assert calls == ["synthetic_package_001"]
    assert consumed_status == "consumed"
    assert result["status"] == "succeeded"
    assert result["journal"]["counts"]["succeeded"] == 1
    assert result["journal"]["counts"]["verified_noop"] == 1
    assert result["journal"]["counts"]["authority_consumptions"] == 1
    states = [
        event["state"] for event in result["journal"]["entries"][0]["events"]
    ]
    assert states == ["planned", "authority_validated", "started", "succeeded"]


def test_plan_only_never_consumes_authority_or_dispatches() -> None:
    with _synthetic_fixture() as fixture:
        calls = 0

        def backend(**_: Any) -> Mapping[str, Any]:
            nonlocal calls
            calls += 1
            return {"status": "promoted"}

        result = execute_factory_queue(
            repo_root=ROOT,
            queue_path=fixture["queue_path"],
            change_set_path=fixture["change_set_path"],
            authority_path=fixture["authority_path"],
            queue_evaluator=fixture["evaluator"],
            advancement_backend=backend,
        )
        available_status = json.loads(
            (ROOT / fixture["authority_path"]).read_text(encoding="utf-8")
        )["authorities"][0]["status"]
    assert calls == 0
    assert available_status == "available"
    assert result["status"] == "planned"
    assert result["journal"]["entries"][0]["current_state"] == "planned"
    assert result["journal"]["counts"]["authority_consumptions"] == 0


def test_consumed_authority_cannot_be_reused_without_prior_journal() -> None:
    with _synthetic_fixture(include_noop=False) as fixture:
        calls = 0

        def backend(**_: Any) -> Mapping[str, Any]:
            nonlocal calls
            calls += 1
            return {"status": "promoted"}

        first = _execute_synthetic(fixture, backend)
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, backend)
    assert first["status"] == "succeeded"
    assert observed.value.code == "authority_status_mismatch"
    assert calls == 1


def test_known_backend_failure_stops_later_entries() -> None:
    with _synthetic_fixture(mutating_count=2, include_noop=False) as fixture:
        calls: list[str] = []

        def backend(**kwargs: Any) -> Mapping[str, Any]:
            calls.append(kwargs["package_id"])
            return {
                "status": "failed",
                "effect_performed": False,
                "error_code": "synthetic_pre_effect_failure",
            }

        result = _execute_synthetic(fixture, backend)
    assert calls == ["synthetic_package_001"]
    assert result["status"] == "failed"
    assert [entry["current_state"] for entry in result["journal"]["entries"]] == [
        "failed",
        "skipped_after_failure",
    ]


def test_resume_preserves_history_skips_success_and_continues_safe_entries() -> None:
    with _synthetic_fixture(mutating_count=2, include_noop=False) as fixture:
        first_calls: list[str] = []

        def fail_second(**kwargs: Any) -> Mapping[str, Any]:
            first_calls.append(kwargs["package_id"])
            if kwargs["package_id"] == "synthetic_package_002":
                return {
                    "status": "failed",
                    "effect_performed": False,
                    "error_code": "synthetic_second_failure",
                }
            return {"status": "promoted"}

        first = _execute_synthetic(fixture, fail_second)
        first_entry_history = copy.deepcopy(
            first["journal"]["entries"][0]["events"]
        )
        second_entry_history = copy.deepcopy(
            first["journal"]["entries"][1]["events"]
        )
        journal_abs = fixture["root"] / "journal.json"
        _write_json(journal_abs, first["journal"])
        replacement = _authority_record(
            fixture,
            fixture["change_entries"][1],
            authority_id="synthetic_authority_002_retry",
            replaces_authority_id="synthetic_authority_002",
        )
        authorities = copy.deepcopy(fixture["authority_payload"])
        authorities["authorities"].append(replacement)
        authority_abs = fixture["root"] / "resume-authorities.json"
        _write_json(authority_abs, authorities)
        resume_calls: list[str] = []

        def succeed(**kwargs: Any) -> Mapping[str, Any]:
            resume_calls.append(kwargs["package_id"])
            return {"status": "promoted"}

        resumed = _execute_synthetic(
            fixture,
            succeed,
            authority_path=authority_abs.relative_to(ROOT),
            resume_journal_path=journal_abs.relative_to(ROOT),
        )
        resumed_first = resumed["journal"]["entries"][0]["events"]
        resumed_second = resumed["journal"]["entries"][1]["events"]
    assert first_calls == ["synthetic_package_001", "synthetic_package_002"]
    assert resume_calls == ["synthetic_package_002"]
    assert resumed["status"] == "succeeded"
    assert resumed_first == first_entry_history
    assert resumed_second[: len(second_entry_history)] == second_entry_history
    assert resumed_second[-1]["authority_id"] == (
        "synthetic_authority_002_retry"
    )


def test_queue_sha_mismatch_fails_before_dispatch() -> None:
    with _synthetic_fixture() as fixture:
        fixture["change_set"]["queue"]["sha256"] = "0" * 64
        _write_json(ROOT / fixture["change_set_path"], fixture["change_set"])
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "execution_bound_file_hash_mismatch"


def test_descriptor_sha_mismatch_fails_before_dispatch() -> None:
    with _synthetic_fixture() as fixture:
        fixture["change_set"]["entries"][0]["descriptor_sha256"] = "0" * 64
        _write_json(ROOT / fixture["change_set_path"], fixture["change_set"])
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "change_set_descriptor_hash_mismatch"


def test_content_identity_mismatch_fails_before_dispatch() -> None:
    with _synthetic_fixture() as fixture:
        fixture["queue_rows"][0]["content_identity_sha256"] = "0" * 64
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "change_set_content_identity_mismatch"


def test_render_settings_identity_mismatch_fails_before_dispatch() -> None:
    with _synthetic_fixture() as fixture:
        fixture["queue_rows"][0]["render_settings_identity_sha256"] = "0" * 64
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "change_set_render_settings_mismatch"


def test_lifecycle_edge_mismatch_is_rejected() -> None:
    with _synthetic_fixture() as fixture:
        fixture["change_set"]["entries"][0][
            "requested_target_lifecycle"
        ] = "rendered"
        _write_json(ROOT / fixture["change_set_path"], fixture["change_set"])
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "change_set_lifecycle_edge_mismatch"


def test_package_not_present_in_queue_is_rejected() -> None:
    with _synthetic_fixture() as fixture:
        fixture["change_set"]["entries"][0]["package_id"] = (
            "synthetic_absent_001"
        )
        _write_json(ROOT / fixture["change_set_path"], fixture["change_set"])
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "change_set_package_not_in_queue"


def test_duplicate_package_entry_is_rejected() -> None:
    with _synthetic_fixture(mutating_count=2) as fixture:
        fixture["change_set"]["entries"][1]["package_id"] = fixture[
            "change_set"
        ]["entries"][0]["package_id"]
        _write_json(ROOT / fixture["change_set_path"], fixture["change_set"])
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "change_set_duplicate_package"


def test_change_set_maximum_exceeded_is_rejected() -> None:
    with _synthetic_fixture(mutating_count=2) as fixture:
        fixture["change_set"]["maximum_mutating_entries"] = 1
        _write_json(ROOT / fixture["change_set_path"], fixture["change_set"])
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "change_set_maximum_exceeded"


def test_unstable_change_set_order_is_rejected() -> None:
    with _synthetic_fixture(mutating_count=2) as fixture:
        fixture["change_set"]["entries"].reverse()
        _write_json(ROOT / fixture["change_set_path"], fixture["change_set"])
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "change_set_order_unstable"


def test_private_absolute_locator_is_rejected() -> None:
    with _synthetic_fixture() as fixture:
        fixture["change_set"]["entries"][0]["descriptor_path"] = (
            "C:/private/descriptor.json"
        )
        _write_json(ROOT / fixture["change_set_path"], fixture["change_set"])
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "execution_locator_private_or_absolute"
    assert "C:/" not in str(observed.value)


def test_unsupported_operation_is_rejected() -> None:
    with _synthetic_fixture() as fixture:
        fixture["change_set"]["entries"][0]["operation"] = "arbitrary_command"
        _write_json(ROOT / fixture["change_set_path"], fixture["change_set"])
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "change_set_operation_unsupported"


def test_missing_authority_is_rejected_before_dispatch() -> None:
    with _synthetic_fixture() as fixture:
        calls = 0

        def backend(**_: Any) -> Mapping[str, Any]:
            nonlocal calls
            calls += 1
            return {"status": "promoted"}

        with pytest.raises(FactoryQueueExecutorError) as observed:
            execute_factory_queue(
                repo_root=ROOT,
                queue_path=fixture["queue_path"],
                change_set_path=fixture["change_set_path"],
                authority_path=None,
                execute=True,
                queue_evaluator=fixture["evaluator"],
                advancement_backend=backend,
            )
    assert observed.value.code == "authority_missing_or_ambiguous"
    assert calls == 0


def test_wrong_authority_package_is_rejected_before_dispatch() -> None:
    with _synthetic_fixture() as fixture:
        fixture["authority_payload"]["authorities"][0]["package"][
            "package_id"
        ] = "synthetic_wrong_001"
        _write_json(
            ROOT / fixture["authority_path"],
            fixture["authority_payload"],
        )
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "authority_package_mismatch"


def test_wrong_authority_lifecycle_edge_is_rejected_before_dispatch() -> None:
    with _synthetic_fixture() as fixture:
        fixture["authority_payload"]["authorities"][0][
            "to_lifecycle"
        ] = "rendered"
        _write_json(
            ROOT / fixture["authority_path"],
            fixture["authority_payload"],
        )
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "authority_to_lifecycle_mismatch"


def test_already_consumed_authority_is_rejected_before_dispatch() -> None:
    with _synthetic_fixture() as fixture:
        fixture["authority_payload"]["authorities"][0]["status"] = "consumed"
        _write_json(
            ROOT / fixture["authority_path"],
            fixture["authority_payload"],
        )
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "authority_status_mismatch"


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    [
        ("queue", "0" * 64, "authority_queue_mismatch"),
        ("change_set", "0" * 64, "authority_change_set_mismatch"),
        ("operation", "render", "authority_operation_mismatch"),
    ],
)
def test_authority_cannot_move_to_another_bound_effect(
    field: str,
    value: str,
    expected_code: str,
) -> None:
    with _synthetic_fixture() as fixture:
        record = fixture["authority_payload"]["authorities"][0]
        if field == "queue":
            record["queue"]["sha256"] = value
        elif field == "change_set":
            record["change_set"]["sha256"] = value
        else:
            record["operation"] = value
        _write_json(
            ROOT / fixture["authority_path"],
            fixture["authority_payload"],
        )
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == expected_code


def test_effect_unknown_cannot_be_automatically_retried() -> None:
    with _synthetic_fixture() as fixture:
        first = _execute_synthetic(
            fixture,
            lambda **_: {
                "status": "effect_unknown",
                "error_code": "synthetic_unknown",
            },
        )
        journal_abs = fixture["root"] / "unknown-journal.json"
        _write_json(journal_abs, first["journal"])
        calls = 0

        def backend(**_: Any) -> Mapping[str, Any]:
            nonlocal calls
            calls += 1
            return {"status": "promoted"}

        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(
                fixture,
                backend,
                resume_journal_path=journal_abs.relative_to(ROOT),
            )
    assert first["status"] == "effect_unknown"
    assert observed.value.code == "effect_unknown_retry_forbidden"
    assert calls == 0


def test_resume_journal_rejects_private_or_machine_local_text() -> None:
    with _synthetic_fixture() as fixture:
        first = _execute_synthetic(
            fixture,
            lambda **_: {
                "status": "failed",
                "effect_performed": False,
                "error_code": "synthetic_failure",
            },
        )
        journal = copy.deepcopy(first["journal"])
        journal["entries"][0]["events"][-1]["consumer_effect"] = (
            "private path C:/users/example/output"
        )
        journal_abs = fixture["root"] / "private-journal.json"
        _write_json(journal_abs, journal)
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(
                fixture,
                lambda **_: {"status": "promoted"},
                resume_journal_path=journal_abs.relative_to(ROOT),
            )
    assert observed.value.code == "journal_consumer_effect_invalid"


def test_noop_package_cannot_be_included_as_mutation() -> None:
    with _synthetic_fixture() as fixture:
        fixture["queue_rows"][0]["technical_decision"] = "verified_noop"
        fixture["queue_rows"][0]["normalized_lifecycle"] = "rendered"
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code in {
        "change_set_lifecycle_edge_mismatch",
        "change_set_noop_or_decision_mismatch",
    }


def test_change_set_output_target_collision_is_rejected() -> None:
    with _synthetic_fixture(mutating_count=2) as fixture:
        fixture["change_set"]["entries"][1][
            "expected_target_identity_sha256"
        ] = fixture["change_set"]["entries"][0][
            "expected_target_identity_sha256"
        ]
        _write_json(ROOT / fixture["change_set_path"], fixture["change_set"])
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(fixture, lambda **_: {"status": "promoted"})
    assert observed.value.code == "change_set_target_collision"


def test_resume_journal_plan_mismatch_is_rejected() -> None:
    with _synthetic_fixture() as fixture:
        first = _execute_synthetic(
            fixture,
            lambda **_: {
                "status": "failed",
                "effect_performed": False,
                "error_code": "synthetic_failure",
            },
        )
        journal = copy.deepcopy(first["journal"])
        journal["plan_identity_sha256"] = "0" * 64
        journal_abs = fixture["root"] / "drifted-journal.json"
        _write_json(journal_abs, journal)
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(
                fixture,
                lambda **_: {"status": "promoted"},
                resume_journal_path=journal_abs.relative_to(ROOT),
            )
    assert observed.value.code == "journal_plan_mismatch"


def test_resume_after_queue_drift_is_rejected() -> None:
    with _synthetic_fixture() as fixture:
        first = _execute_synthetic(
            fixture,
            lambda **_: {
                "status": "failed",
                "effect_performed": False,
                "error_code": "synthetic_failure",
            },
        )
        journal_abs = fixture["root"] / "journal.json"
        _write_json(journal_abs, first["journal"])
        _write_json(
            ROOT / fixture["queue_path"],
            {"queue": {"packages": fixture["queue_entries"]}, "drift": True},
        )
        with pytest.raises(FactoryQueueExecutorError) as observed:
            _execute_synthetic(
                fixture,
                lambda **_: {"status": "promoted"},
                resume_journal_path=journal_abs.relative_to(ROOT),
            )
    assert observed.value.code == "execution_bound_file_hash_mismatch"


def test_shared_executor_contains_no_topic_specific_branch() -> None:
    source = (ROOT / "src/pipeline/factory_queue_executor.py").read_text(
        encoding="utf-8"
    )
    forbidden_ids = (
        "new_banknote_security_notebooklm_001",
        "real_estate_reins_transparency_001",
        "ai_monitoring_labor_001",
        "food_expiry_labels_001",
    )
    assert all(package_id not in source for package_id in forbidden_ids)
