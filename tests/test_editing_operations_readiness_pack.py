from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.editing_operations_readiness_pack import (
    REQUIRED_BOUNDARY_FLAGS,
    REQUIRED_EDITING_OPERATIONS_FILES,
    REQUIRED_GAP_GROUPS,
    REQUIRED_OPERATION_IDS,
    build_editing_operations_readiness_pack,
    validate_editing_operations_readiness_pack,
)
from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_editing_operations_readiness_pack_builds_contracts_and_preview(tmp_path) -> None:
    output_dir = tmp_path / "editing_operations_readiness_pack"

    readback = build_editing_operations_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_editing_operations_readiness_pack",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_EDITING_OPERATIONS_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "editing_operations_manifest.json")
    registry = _load(output_dir / "edit_operation_registry.json")
    scene_plan = _load(output_dir / "scene_operation_plan.json")
    timing_model = _load(output_dir / "timing_adjustment_model.json")
    voice_map = _load(output_dir / "voice_subtitle_operation_map.json")
    visual_map = _load(output_dir / "visual_asset_slot_map.json")
    readback_schema = _load(output_dir / "yymm4_readback_schema.json")
    gap_ledger = _load(output_dir / "operation_gap_ledger.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    html = (output_dir / "editing_operations_preview.html").read_text(encoding="utf-8")
    protocol = (output_dir / "yymm4_observation_protocol.md").read_text(encoding="utf-8")

    operation_ids = {row["operation_id"] for row in registry["operations"]}
    assert manifest["artifact_kind"] == "episode-editing-operations-readiness-pack"
    assert manifest["parallel_lane"] == "editing_features"
    assert manifest["thread_id"] == "editing-ops-episode002"
    assert registry["operation_count"] >= len(REQUIRED_OPERATION_IDS)
    assert operation_ids >= set(REQUIRED_OPERATION_IDS)
    assert scene_plan["scene_count"] >= 3
    assert len(scene_plan["scenes"]) >= 3
    assert timing_model["status"] == "provisional_timing_model_ready_no_audio_or_yymm4_timing"
    assert timing_model["scene_count"] >= 3
    assert voice_map["status"] == "voice_subtitle_operations_ready_no_yymm4_voiceitems"
    assert voice_map["utterance_operation_count"] >= 3
    assert visual_map["status"] == "visual_asset_slots_ready_no_external_media"
    assert visual_map["scene_visual_slot_count"] >= 3
    assert readback_schema["status"] == "schema_ready_no_actual_import"
    assert readback_schema["actual_yymm4_import"] is False
    assert readback_schema["yymm4_rendered"] is False
    assert gap_ledger["counts"]["buildable_locally"] >= 3
    for group_id in REQUIRED_GAP_GROUPS:
        assert gap_ledger["groups"][group_id], group_id
    assert manifest["invented_real_content"] is False
    assert manifest["actual_yymm4_import"] is False
    assert manifest["yymm4_rendered"] is False
    assert manifest["production_ready"] is False
    assert manifest["public_ready"] is False
    assert manifest["gui_lane_files_touched"] == []
    assert manifest["output_template_files_touched"] == []
    assert manifest["input_intake_files_touched"] == []
    assert manifest["thread_registry_updated"] is True
    assert manifest["shared_docs_touched"] is True
    assert source_index["output_template_context_read_only"] is True
    assert source_index["input_intake_context_read_only"] is True
    assert source_index["gui_lane_context_read_only"] is True
    assert 'data-editing-operations="true"' in html
    assert 'data-region="operation-lanes"' in html
    assert 'data-region="scene-operation-matrix"' in html
    assert 'data-region="timing-strip"' in html
    assert 'data-region="voice-subtitle-lane"' in html
    assert 'data-region="visual-slot-lane"' in html
    assert 'data-region="yymm4-observation-lane"' in html
    assert "future manual observation only" in protocol
    assert "Do not launch YMM4" in protocol
    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundary_flags"][flag] is True


def test_editing_operations_validation_catches_missing_readback_schema(tmp_path) -> None:
    output_dir = tmp_path / "editing_operations_readiness_pack"
    build_editing_operations_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_editing_operations_readiness_pack",
    )
    (output_dir / "yymm4_readback_schema.json").unlink()

    readback = validate_editing_operations_readiness_pack(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:yymm4_readback_schema.json" in readback["failed_checks"]


def test_cli_build_editing_operations_readiness_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_editing_operations_readiness_pack"

    code = main(
        [
            "build-editing-operations-readiness-pack",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_editing_operations_readiness_pack",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["primary_review_file"].endswith("editing_operations_preview.html")
    assert payload["operation_count"] >= len(REQUIRED_OPERATION_IDS)
    assert payload["scene_count"] >= 3
    assert payload["timing_model_status"] == "provisional_timing_model_ready_no_audio_or_yymm4_timing"
    assert payload["voice_subtitle_operation_status"] == "voice_subtitle_operations_ready_no_yymm4_voiceitems"
    assert payload["visual_slot_map_status"] == "visual_asset_slots_ready_no_external_media"
    assert payload["yymm4_protocol_status"] == "future_manual_observation_protocol_ready_no_launch"
    assert payload["yymm4_readback_schema_status"] == "schema_ready_no_actual_import"
    assert payload["invented_real_content"] is False
    assert payload["actual_yymm4_import"] is False
    assert payload["gui_lane_files_touched"] == []
    assert payload["output_template_files_touched"] == []
    assert payload["input_intake_files_touched"] == []
    assert payload["thread_registry_updated"] is True
    assert payload["shared_docs_touched"] is True
    assert payload["full_pytest_run"] is False
    assert payload["launcher_or_open_command"]


def test_editing_operations_readiness_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "editing_operations_readiness_pack"
    build_editing_operations_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_editing_operations_readiness_pack",
    )

    readback = _load(output_dir / "validation_readback.json")
    assert readback["status"] == "passed"
    assert readback["checks"]["external_dependency_status"] == "none_found"
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["temporary_copy_absent"] is True
    assert readback["checks"]["gui_lane_files_touched"] == []
    assert readback["checks"]["output_template_files_touched"] == []
    assert readback["checks"]["input_intake_files_touched"] == []

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
