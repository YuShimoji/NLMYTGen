from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.output_template_readiness_pack import (
    BUILDABLE_LOCAL_GAPS,
    REQUIRED_BOUNDARY_FLAGS,
    REQUIRED_OUTPUT_TEMPLATE_FILES,
    TEMPLATE_TYPE_IDS,
    build_output_template_readiness_pack,
    validate_output_template_readiness_pack,
)
from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_output_template_readiness_pack_builds_maps_and_preview(tmp_path) -> None:
    output_dir = tmp_path / "output_template_readiness_pack"

    readback = build_output_template_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_output_template_readiness_pack",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_OUTPUT_TEMPLATE_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "output_template_readiness_manifest.json")
    timing_map = _load(output_dir / "scene_timing_map.json")
    voice_mapping = _load(output_dir / "voice_subtitle_mapping.json")
    visual_registry = _load(output_dir / "visual_scene_template_registry.json")
    overlay_spec = _load(output_dir / "citation_overlay_spec.json")
    thumbnail_map = _load(output_dir / "thumbnail_transfer_map.json")
    handoff = _load(output_dir / "yymm4_template_handoff_readiness.json")
    gap_readback = _load(output_dir / "template_gap_closure_readback.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    html = (output_dir / "output_template_readiness_preview.html").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-output-template-readiness-pack"
    assert manifest["parallel_lane"] == "output_video_layer"
    assert manifest["shared_docs_touched"] is False
    assert manifest["gui_lane_files_touched"] == []
    assert timing_map["scene_count"] >= 3
    assert len(timing_map["scenes"]) >= 3
    assert timing_map["status"] == "template_ready_estimated_no_audio_or_yymm4_timing"
    assert voice_mapping["status"] == "voice_subtitle_template_ready_no_yymm4_voiceitems"
    assert voice_mapping["csv_reference_status"] == "references_available_csv_rows"
    assert voice_mapping["utterance_count"] >= 3
    assert visual_registry["template_type_count"] >= 4
    assert {row["template_id"] for row in visual_registry["template_types"]} >= set(TEMPLATE_TYPE_IDS[:4])
    assert overlay_spec["status"] == "citation_overlay_template_ready_local_offline"
    assert overlay_spec["overlay_slot_count"] >= 3
    assert thumbnail_map["status"] == "thumbnail_context_transfer_ready_not_final_approval"
    assert thumbnail_map["final_thumbnail_approval"] is False
    assert handoff["actual_yymm4_import"] is False
    assert handoff["yymm4_rendered"] is False
    assert handoff["production_ready"] is False
    assert gap_readback["previous_buildable_gap_count"] == len(BUILDABLE_LOCAL_GAPS)
    assert gap_readback["buildable_gap_closed_count"] == len(BUILDABLE_LOCAL_GAPS)
    assert gap_readback["buildable_gap_partial_count"] == 0
    assert source_index["gui_lane_context_read_only"] is True
    assert 'data-output-template-readiness="true"' in html
    assert 'data-region="timing-strip"' in html
    assert 'data-region="scene-template-lane"' in html
    assert 'data-region="voice-subtitle-lane"' in html
    assert 'data-region="overlay-lane"' in html
    assert 'data-region="thumbnail-transfer-lane"' in html
    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundary_flags"][flag] is True


def test_output_template_validation_catches_missing_overlay_spec(tmp_path) -> None:
    output_dir = tmp_path / "output_template_readiness_pack"
    build_output_template_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_output_template_readiness_pack",
    )
    (output_dir / "citation_overlay_spec.json").unlink()

    readback = validate_output_template_readiness_pack(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:citation_overlay_spec.json" in readback["failed_checks"]


def test_cli_build_output_template_readiness_pack_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_output_template_readiness_pack"

    code = main(
        [
            "build-output-template-readiness-pack",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_output_template_readiness_pack",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["primary_review_file"].endswith("output_template_readiness_preview.html")
    assert payload["scene_count"] >= 3
    assert payload["visual_template_count"] >= 4
    assert payload["previous_buildable_gap_count"] == len(BUILDABLE_LOCAL_GAPS)
    assert payload["buildable_gap_closed_count"] == len(BUILDABLE_LOCAL_GAPS)
    assert payload["buildable_gap_partial_count"] == 0
    assert payload["blocked_by_real_input_count"] >= 1
    assert payload["blocked_by_yymm4_gate_count"] >= 1
    assert payload["blocked_by_public_rights_count"] >= 1
    assert payload["gui_lane_files_touched"] == []
    assert payload["shared_docs_touched"] is False
    assert payload["full_pytest_run"] is False
    assert payload["launcher_or_open_command"]


def test_output_template_readiness_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "output_template_readiness_pack"
    build_output_template_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_output_template_readiness_pack",
    )

    readback = _load(output_dir / "validation_readback.json")
    assert readback["status"] == "passed"
    assert readback["checks"]["external_dependency_status"] == "none_found"
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["temporary_copy_absent"] is True
    assert readback["checks"]["gui_lane_files_touched"] == []
    assert readback["checks"]["shared_docs_touched"] is False

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
