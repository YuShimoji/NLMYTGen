from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.local_edit_slice_execution_pack import (
    BLOCKED_GATE_OPERATION_IDS,
    LOCAL_EXECUTION_OPERATION_IDS,
    REQUIRED_BOUNDARY_FLAGS,
    REQUIRED_LOCAL_EDIT_SLICE_FILES,
    build_local_edit_slice_execution_pack,
    validate_local_edit_slice_execution_pack,
)
from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_local_edit_slice_execution_builds_queue_and_preview(tmp_path) -> None:
    output_dir = tmp_path / "local_edit_slice_execution_pack"

    readback = build_local_edit_slice_execution_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_local_edit_slice_execution_pack",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_LOCAL_EDIT_SLICE_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "local_edit_slice_manifest.json")
    queue = _load(output_dir / "local_edit_slice_queue.json")
    scene_plan = _load(output_dir / "scene_edit_execution_plan.json")
    gate_readback = _load(output_dir / "operation_gate_preservation_readback.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    html = (output_dir / "local_edit_execution_preview.html").read_text(encoding="utf-8")
    markdown = (output_dir / "local_edit_execution_preview.md").read_text(encoding="utf-8")

    queued_ids = {row["operation_id"] for row in queue["queue"]}
    blocked_ids = {row["operation_id"] for row in queue["blocked_operations"]}
    assert manifest["artifact_kind"] == "episode-local-edit-slice-execution-pack"
    assert manifest["parallel_lane"] == "editing_features_local_execution"
    assert manifest["thread_id"] == "local-edit-slice-episode002"
    assert manifest["gates_closed"] is True
    assert manifest["actual_yymm4_import"] is False
    assert manifest["real_input_replacement_executed"] is False
    assert manifest["public_ready"] is False
    assert queued_ids == set(LOCAL_EXECUTION_OPERATION_IDS)
    assert set(BLOCKED_GATE_OPERATION_IDS).issubset(blocked_ids)
    assert queue["queue_operation_count"] == len(LOCAL_EXECUTION_OPERATION_IDS)
    assert scene_plan["scene_count"] >= 3
    assert len(scene_plan["scenes"]) >= 3
    assert gate_readback["status"] == "closed_gates_preserved"
    assert gate_readback["forbidden_gates_closed"] is True
    assert all(value is False for value in gate_readback["closed_gate_flags"].values())
    assert source_index["editing_operations_context_read_only"] is True
    assert 'data-local-edit-slice="true"' in html
    assert 'data-region="execution-queue"' in html
    assert 'data-region="scene-execution-plan"' in html
    assert "local edit-slice execution" in markdown
    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundary_flags"][flag] is True
    for touches in manifest["protected_context_files_touched"].values():
        assert touches == []


def test_local_edit_slice_validation_catches_missing_queue(tmp_path) -> None:
    output_dir = tmp_path / "local_edit_slice_execution_pack"
    build_local_edit_slice_execution_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_local_edit_slice_execution_pack",
    )
    (output_dir / "local_edit_slice_queue.json").unlink()

    readback = validate_local_edit_slice_execution_pack(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:local_edit_slice_queue.json" in readback["failed_checks"]


def test_cli_build_local_edit_slice_execution_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_local_edit_slice_execution_pack"

    code = main(
        [
            "build-local-edit-slice-execution-pack",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_local_edit_slice_execution_pack",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["primary_review_file"].endswith("local_edit_execution_preview.html")
    assert payload["queue_operation_count"] == len(LOCAL_EXECUTION_OPERATION_IDS)
    assert payload["scene_count"] >= 3
    assert payload["blocked_operation_count"] >= len(BLOCKED_GATE_OPERATION_IDS)
    assert payload["gates_closed"] is True
    assert payload["actual_yymm4_import"] is False
    assert payload["real_input_replacement_executed"] is False
    assert payload["public_ready"] is False
    assert payload["thread_registry_updated"] is True
    assert payload["shared_docs_touched"] is True
    assert payload["full_pytest_run"] is False


def test_local_edit_slice_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "local_edit_slice_execution_pack"
    build_local_edit_slice_execution_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_local_edit_slice_execution_pack",
    )

    readback = _load(output_dir / "validation_readback.json")
    assert readback["status"] == "passed"
    assert readback["checks"]["external_dependency_status"] == "none_found"
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["temporary_copy_absent"] is True
    assert readback["checks"]["blocked_gate_operations_not_queued"] is True

    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for marker in EXTERNAL_REF_MARKERS:
            assert marker not in text, (path.name, marker)

    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_TRUE_CLAIMS:
            assert forbidden not in text, (path.name, forbidden)
