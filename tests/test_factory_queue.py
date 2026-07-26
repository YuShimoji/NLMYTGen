from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator

import pytest

from src.cli import main as cli
from src.pipeline import factory_queue
from src.pipeline.factory_contract_v2_1 import FactoryContractError
from src.pipeline.factory_queue import (
    FACTORY_QUEUE_HARD_MAXIMUM,
    TECHNICAL_DECISIONS,
    FactoryQueueError,
    decide_render_on_change,
    evaluate_factory_queue,
    execute_safe_queue_stages,
)


ROOT = Path(__file__).resolve().parents[1]
QUEUE = Path(
    "production_pilots/factory_queues/four_package_lifecycle_queue_v1.json"
)
QUEUE_SCHEMA = Path(
    "schemas/factory_queue_v1/factory_queue_v1.schema.json"
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


@contextmanager
def _mutated_queue(
    mutate: Callable[[dict[str, Any], Path], None],
) -> Iterator[Path]:
    payload = copy.deepcopy(_load(QUEUE))
    with tempfile.TemporaryDirectory(prefix=".factory-queue-test-", dir=ROOT) as temp:
        temp_root = Path(temp)
        mutate(payload, temp_root)
        path = temp_root / "queue.json"
        _write_json(path, payload)
        yield path.relative_to(ROOT)


def _copy_descriptor(
    temp_root: Path,
    source: str,
    *,
    name: str,
    mutate: Callable[[dict[str, Any]], None] | None = None,
) -> str:
    payload = json.loads((ROOT / source).read_text(encoding="utf-8"))
    if mutate is not None:
        mutate(payload)
    target = temp_root / name
    _write_json(target, payload)
    return target.relative_to(ROOT).as_posix()


def test_queue_schema_and_descriptor_are_versioned_and_bounded() -> None:
    schema = _load(QUEUE_SCHEMA)
    descriptor = _load(QUEUE)
    assert schema["$id"] == "nlmytgen.factory_queue.v1"
    assert schema["properties"]["queue"]["properties"][
        "maximum_queue_size"
    ]["maximum"] == FACTORY_QUEUE_HARD_MAXIMUM
    assert descriptor["contract"]["schema_sha256"] == _sha(ROOT / QUEUE_SCHEMA)
    assert descriptor["queue"]["maximum_queue_size"] == 4
    assert len(descriptor["queue"]["packages"]) == 4
    assert [row["order"] for row in descriptor["queue"]["packages"]] == [
        1,
        2,
        3,
        4,
    ]
    assert set(descriptor["evaluation_policy"]["run_local_fields_excluded"]) == {
        "run_id",
        "timestamp",
        "pid",
        "elapsed_time",
        "local_directory",
        "machine_path",
    }


def test_live_four_package_queue_has_one_prepared_candidate_and_no_render() -> None:
    result = evaluate_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE,
        check_live=True,
    )
    assert result["status"] == "passed"
    assert [
        (
            row["package_id"],
            row["normalized_lifecycle"],
            row["technical_decision"],
        )
        for row in result["packages"]
    ] == [
        (
            "new_banknote_security_notebooklm_001",
            "human_accepted",
            "verified_noop",
        ),
        (
            "real_estate_reins_transparency_001",
            "rendered",
            "verified_noop",
        ),
        (
            "ai_monitoring_labor_001",
            "rendered",
            "verified_noop",
        ),
        (
            "food_expiry_labels_001",
            "package_prepared",
            "source_project_generation_required",
        ),
    ]
    assert result["counts"] == {
        "total_packages": 4,
        "verified_noop": 3,
        "recorded_complete_no_live_file": 0,
        "source_project_candidates": 1,
        "render_candidates": 0,
        "human_review_candidates": 0,
        "blocked_packages": 0,
        "invalid_packages": 0,
        "scheduled_for_render": 0,
        "execution_set_size": 0,
    }
    assert result["execution_set"] == []


def test_queue_evaluation_is_deterministic_twice() -> None:
    first = evaluate_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE,
        check_live=True,
    )
    second = evaluate_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE,
        check_live=True,
    )
    assert first == second
    assert first["evaluation_sha256"] == (
        "52149bc8f1f3793586bc1d59dd31839d3dabb79266b7f7023339b9582a826229"
    )


def test_recorded_only_evaluation_never_schedules_completed_packages() -> None:
    result = evaluate_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE,
        check_live=False,
    )
    assert [row["technical_decision"] for row in result["packages"][:3]] == [
        "recorded_complete_no_live_file",
        "recorded_complete_no_live_file",
        "recorded_complete_no_live_file",
    ]
    assert result["counts"]["render_candidates"] == 0
    assert result["counts"]["scheduled_for_render"] == 0


@pytest.mark.parametrize(
    ("lifecycle", "live_status", "source_available", "expected"),
    [
        ("human_accepted", "live_file_hash_exact", True, "verified_noop"),
        (
            "human_accepted",
            "receipt_only_no_live_file",
            False,
            "recorded_complete_no_live_file",
        ),
        ("rendered", "live_file_hash_exact", True, "verified_noop"),
        (
            "rendered",
            "receipt_only_no_live_file",
            False,
            "recorded_complete_no_live_file",
        ),
        ("source_project_ready", "unavailable", True, "render_required"),
        (
            "package_prepared",
            "not_applicable_before_rendered",
            False,
            "source_project_generation_required",
        ),
    ],
)
def test_render_on_change_lifecycle_rules(
    lifecycle: str,
    live_status: str,
    source_available: bool,
    expected: str,
) -> None:
    decision, _ = decide_render_on_change(
        lifecycle=lifecycle,
        live_output_status=live_status,
        semantic_identity_match=True,
        render_settings_match=True,
        output_corrupt=False,
        source_project_available=source_available,
    )
    assert decision == expected


def test_render_on_change_ignores_run_local_only_difference() -> None:
    decision, reasons = decide_render_on_change(
        lifecycle="human_accepted",
        live_output_status="live_file_hash_exact",
        semantic_identity_match=True,
        render_settings_match=True,
        output_corrupt=False,
        source_project_available=True,
        run_local_only_change=True,
    )
    assert decision == "verified_noop"
    assert "run_local_change_ignored" in reasons


def test_render_on_change_blocks_semantic_drift_and_corrupt_output() -> None:
    drift, _ = decide_render_on_change(
        lifecycle="human_accepted",
        live_output_status="live_file_hash_exact",
        semantic_identity_match=False,
        render_settings_match=True,
        output_corrupt=False,
        source_project_available=True,
    )
    corrupt, _ = decide_render_on_change(
        lifecycle="rendered",
        live_output_status="unavailable",
        semantic_identity_match=True,
        render_settings_match=True,
        output_corrupt=True,
        source_project_available=True,
    )
    assert drift == "blocked_identity_drift"
    assert corrupt == "blocked_corrupt_output"


def test_queue_maximum_exceeded_fails_before_package_evaluation() -> None:
    def mutate(payload: dict[str, Any], _: Path) -> None:
        fifth = copy.deepcopy(payload["queue"]["packages"][-1])
        fifth["order"] = 5
        payload["queue"]["packages"].append(fifth)

    with _mutated_queue(mutate) as queue:
        with pytest.raises(FactoryQueueError) as observed:
            evaluate_factory_queue(repo_root=ROOT, queue_path=queue)
    assert observed.value.code == "queue_maximum_exceeded"


def test_unstable_or_duplicate_order_fails_closed() -> None:
    def mutate(payload: dict[str, Any], _: Path) -> None:
        payload["queue"]["packages"][3]["order"] = 2

    with _mutated_queue(mutate) as queue:
        with pytest.raises(FactoryQueueError) as observed:
            evaluate_factory_queue(repo_root=ROOT, queue_path=queue)
    assert observed.value.code == "queue_order_unstable"


def test_private_absolute_descriptor_path_is_rejected() -> None:
    def mutate(payload: dict[str, Any], _: Path) -> None:
        payload["queue"]["packages"][0]["descriptor_path"] = (
            "C:/private/factory_package.json"
        )

    with _mutated_queue(mutate) as queue:
        with pytest.raises(FactoryQueueError) as observed:
            evaluate_factory_queue(repo_root=ROOT, queue_path=queue)
    assert observed.value.code == "queue_locator_private_or_absolute"
    assert "C:/" not in str(observed.value)


def test_unknown_queue_version_is_rejected() -> None:
    def mutate(payload: dict[str, Any], _: Path) -> None:
        payload["schema_version"] = "2.0"

    with _mutated_queue(mutate) as queue:
        with pytest.raises(FactoryQueueError) as observed:
            evaluate_factory_queue(repo_root=ROOT, queue_path=queue)
    assert observed.value.code == "queue_policy_invalid"


def test_duplicate_package_id_is_rejected() -> None:
    def mutate(payload: dict[str, Any], temp_root: Path) -> None:
        first = payload["queue"]["packages"][0]
        copied = copy.deepcopy(first)
        copied["order"] = 4
        copied["descriptor_path"] = _copy_descriptor(
            temp_root,
            first["descriptor_path"],
            name="duplicate-package.json",
        )
        payload["queue"]["packages"][3] = copied

    with _mutated_queue(mutate) as queue:
        with pytest.raises(FactoryQueueError) as observed:
            evaluate_factory_queue(repo_root=ROOT, queue_path=queue)
    assert observed.value.code == "queue_duplicate_package_id"


def test_duplicate_content_identity_is_rejected() -> None:
    shared_identity = (
        "50772aa09294d634044c1598d9fc9c2f3366b79bbf953147830ff44c9aee4cf0"
    )

    def mutate(payload: dict[str, Any], temp_root: Path) -> None:
        second = payload["queue"]["packages"][1]

        def change_descriptor(descriptor: dict[str, Any]) -> None:
            descriptor["identities"]["content_identity_sha256"] = shared_identity

        second["descriptor_path"] = _copy_descriptor(
            temp_root,
            second["descriptor_path"],
            name="duplicate-content.json",
            mutate=change_descriptor,
        )
        second["expected_content_identity_sha256"] = shared_identity

    with _mutated_queue(mutate) as queue:
        with pytest.raises(FactoryQueueError) as observed:
            evaluate_factory_queue(repo_root=ROOT, queue_path=queue)
    assert observed.value.code == "queue_duplicate_content_identity"


def test_duplicate_content_identity_can_name_one_immutable_reference() -> None:
    shared_identity = (
        "50772aa09294d634044c1598d9fc9c2f3366b79bbf953147830ff44c9aee4cf0"
    )

    def mutate(payload: dict[str, Any], temp_root: Path) -> None:
        first = payload["queue"]["packages"][0]
        second = payload["queue"]["packages"][1]
        first["immutable_artifact_reference"] = "shared-immutable-proof"
        second["immutable_artifact_reference"] = "shared-immutable-proof"

        def change_descriptor(descriptor: dict[str, Any]) -> None:
            descriptor["identities"]["content_identity_sha256"] = shared_identity

        second["descriptor_path"] = _copy_descriptor(
            temp_root,
            second["descriptor_path"],
            name="allowed-shared-content.json",
            mutate=change_descriptor,
        )
        second["expected_content_identity_sha256"] = shared_identity

    with _mutated_queue(mutate) as queue:
        result = evaluate_factory_queue(
            repo_root=ROOT,
            queue_path=queue,
            check_live=False,
        )
    assert result["status"] == "passed"
    assert result["counts"]["render_candidates"] == 0


def test_target_collision_is_rejected_even_for_one_immutable_reference() -> None:
    def mutate(payload: dict[str, Any], temp_root: Path) -> None:
        first = payload["queue"]["packages"][0]
        copied = copy.deepcopy(first)
        first["immutable_artifact_reference"] = "same-immutable-output"
        copied["immutable_artifact_reference"] = "same-immutable-output"
        copied["order"] = 4
        copied["expected_package_id"] = "new_banknote_immutable_copy"

        def change_package_id(descriptor: dict[str, Any]) -> None:
            descriptor["package"]["package_id"] = (
                "new_banknote_immutable_copy"
            )

        copied["descriptor_path"] = _copy_descriptor(
            temp_root,
            first["descriptor_path"],
            name="target-collision.json",
            mutate=change_package_id,
        )
        payload["queue"]["packages"][3] = copied

    with _mutated_queue(mutate) as queue:
        with pytest.raises(FactoryQueueError) as observed:
            evaluate_factory_queue(repo_root=ROOT, queue_path=queue)
    assert observed.value.code == "queue_target_collision"


def test_unknown_package_schema_becomes_blocked_contract() -> None:
    def mutate(payload: dict[str, Any], temp_root: Path) -> None:
        fourth = payload["queue"]["packages"][3]

        def change_schema(descriptor: dict[str, Any]) -> None:
            descriptor["schema"] = "nlmytgen.factory_package.v99"

        fourth["descriptor_path"] = _copy_descriptor(
            temp_root,
            fourth["descriptor_path"],
            name="unknown-package-schema.json",
            mutate=change_schema,
        )

    with _mutated_queue(mutate) as queue:
        result = evaluate_factory_queue(repo_root=ROOT, queue_path=queue)
    assert result["status"] == "failed"
    assert result["packages"][3]["technical_decision"] == "blocked_contract"
    assert result["packages"][3]["reason_codes"] == [
        "factory_package_schema_invalid"
    ]


def test_contradictory_lifecycle_evidence_becomes_blocked_contract() -> None:
    def mutate(payload: dict[str, Any], temp_root: Path) -> None:
        fourth = payload["queue"]["packages"][3]

        def contradict(descriptor: dict[str, Any]) -> None:
            descriptor["lifecycle"]["render_ready"] = True

        fourth["descriptor_path"] = _copy_descriptor(
            temp_root,
            fourth["descriptor_path"],
            name="contradictory-lifecycle.json",
            mutate=contradict,
        )

    with _mutated_queue(mutate) as queue:
        result = evaluate_factory_queue(repo_root=ROOT, queue_path=queue)
    assert result["status"] == "failed"
    assert result["packages"][3]["technical_decision"] == "blocked_contract"
    assert result["packages"][3]["reason_codes"] == [
        "lifecycle_flags_contradiction"
    ]


def test_accepted_artifact_semantic_drift_fails_closed() -> None:
    def mutate(payload: dict[str, Any], temp_root: Path) -> None:
        first = payload["queue"]["packages"][0]

        def drift(descriptor: dict[str, Any]) -> None:
            descriptor["identities"]["content_identity_sha256"] = "0" * 64

        first["descriptor_path"] = _copy_descriptor(
            temp_root,
            first["descriptor_path"],
            name="accepted-semantic-drift.json",
            mutate=drift,
        )

    with _mutated_queue(mutate) as queue:
        result = evaluate_factory_queue(repo_root=ROOT, queue_path=queue)
    row = result["packages"][0]
    assert result["status"] == "failed"
    assert row["normalized_lifecycle"] == "human_accepted"
    assert row["technical_decision"] == "blocked_identity_drift"
    assert row["execution_eligible"] is False


def test_rendered_output_hash_mismatch_is_blocked_corrupt_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_validate = factory_queue.validate_factory_package_lifecycle

    def validate_with_corrupt_reins(
        *,
        repo_root: Path,
        descriptor_path: Path,
        check_live: bool = False,
        require_lifecycle: str | None = None,
    ) -> dict[str, Any]:
        if check_live and "real_estate_reins_transparency_001" in str(
            descriptor_path
        ):
            raise FactoryContractError(
                "synthetic output mismatch",
                code="live_artifact_hash_mismatch",
                section="render_validation",
                field_path="$.render_validation.mp4_path",
                consumer_effect="completed output cannot be trusted",
            )
        return real_validate(
            repo_root=repo_root,
            descriptor_path=descriptor_path,
            check_live=check_live,
            require_lifecycle=require_lifecycle,
        )

    monkeypatch.setattr(
        factory_queue,
        "validate_factory_package_lifecycle",
        validate_with_corrupt_reins,
    )
    result = evaluate_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE,
        check_live=True,
    )
    assert result["status"] == "failed"
    assert result["packages"][1]["technical_decision"] == (
        "blocked_corrupt_output"
    )
    assert result["counts"]["render_candidates"] == 0


def test_receipt_only_completed_packages_never_become_render_candidates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_validate = factory_queue.validate_factory_package_lifecycle

    def tracked_only_validate(
        *,
        repo_root: Path,
        descriptor_path: Path,
        check_live: bool = False,
        require_lifecycle: str | None = None,
    ) -> dict[str, Any]:
        result = real_validate(
            repo_root=repo_root,
            descriptor_path=descriptor_path,
            check_live=False if check_live else check_live,
            require_lifecycle=require_lifecycle,
        )
        if check_live and result["normalized_lifecycle"]["state"] in {
            "human_accepted",
            "rendered",
        }:
            result = copy.deepcopy(result)
            for row in result["availability"]:
                row["status"] = "receipt_only_no_live_file"
                row["actual_sha256"] = None
        elif check_live:
            result = real_validate(
                repo_root=repo_root,
                descriptor_path=descriptor_path,
                check_live=True,
                require_lifecycle=require_lifecycle,
            )
        return result

    monkeypatch.setattr(
        factory_queue,
        "validate_factory_package_lifecycle",
        tracked_only_validate,
    )
    result = evaluate_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE,
        check_live=True,
    )
    assert [row["technical_decision"] for row in result["packages"][:3]] == [
        "recorded_complete_no_live_file",
        "recorded_complete_no_live_file",
        "recorded_complete_no_live_file",
    ]
    assert result["counts"]["render_candidates"] == 0
    assert result["counts"]["scheduled_for_render"] == 0


def test_prepared_action_is_represented_while_authority_remains_false() -> None:
    result = evaluate_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE,
        check_live=True,
    )
    row = result["packages"][3]
    assert row["technical_decision"] == "source_project_generation_required"
    assert row["technical_next_stage"] == "source_project_generation"
    assert row["external_authority"][
        "source_project_generation_authorized"
    ] is False
    assert row["execution_gate_decision"] == "blocked_authority"
    assert row["execution_eligible"] is False


def test_noop_packages_are_excluded_from_execution_set() -> None:
    result = evaluate_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE,
        check_live=True,
    )
    assert result["execution_set"] == []
    assert all(
        row["execution_eligible"] is False
        for row in result["packages"]
        if row["technical_decision"]
        in {"verified_noop", "recorded_complete_no_live_file"}
    )


def test_safe_stage_execution_performs_no_product_write(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    evaluation = evaluate_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE,
        check_live=True,
    )

    def forbidden_write(*_: Any, **__: Any) -> int:
        raise AssertionError("safe-stage execution attempted a product write")

    monkeypatch.setattr(Path, "write_bytes", forbidden_write)
    monkeypatch.setattr(Path, "write_text", forbidden_write)
    first = execute_safe_queue_stages(
        repo_root=ROOT,
        evaluation=evaluation,
    )
    second = execute_safe_queue_stages(
        repo_root=ROOT,
        evaluation=evaluation,
    )
    assert first == second
    assert first["counts"] == {
        "packages_validated": 4,
        "existing_pipeline_dry_runs": 3,
        "pre_render_stage_plans": 1,
        "identity_exact": 4,
        "product_writes": 0,
        "process_launches": 0,
    }
    assert set(first["boundaries"].values()) == {True, False}
    assert first["boundaries"]["validation_only"] is True
    assert first["boundaries"]["product_artifacts_written"] is False


def test_public_cli_returns_zero_for_incomplete_but_valid_queue(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = cli.main(
        [
            "evaluate-factory-queue",
            "--queue",
            QUEUE.as_posix(),
            "--check-live",
            "--format",
            "json",
        ]
    )
    result = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert result["status"] == "passed"
    assert result["counts"]["source_project_candidates"] == 1
    assert result["counts"]["render_candidates"] == 0


def test_shared_queue_engine_contains_no_known_topic_id() -> None:
    source = (ROOT / "src/pipeline/factory_queue.py").read_text(
        encoding="utf-8"
    )
    forbidden_ids = (
        "new_banknote_security_notebooklm_001",
        "real_estate_reins_transparency_001",
        "ai_monitoring_labor_001",
        "food_expiry_labels_001",
    )
    assert all(value not in source for value in forbidden_ids)


def test_supported_decisions_include_every_required_fail_closed_state() -> None:
    assert set(TECHNICAL_DECISIONS) == {
        "verified_noop",
        "recorded_complete_no_live_file",
        "source_project_generation_required",
        "render_required",
        "human_review_required",
        "blocked_contract",
        "blocked_identity_drift",
        "blocked_corrupt_output",
        "blocked_authority",
    }
