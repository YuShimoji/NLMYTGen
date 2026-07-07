from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.output_video_layer_proof import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
    REQUIRED_BOUNDARY_FLAGS,
    REQUIRED_GAP_GROUPS,
    REQUIRED_OUTPUT_VIDEO_FILES,
    build_output_video_layer_proof,
    validate_output_video_layer_proof,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_output_video_layer_proof_builds_storyboard_package(tmp_path) -> None:
    output_dir = tmp_path / "output_video_layer_proof"

    readback = build_output_video_layer_proof(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_output_video_layer_proof",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_OUTPUT_VIDEO_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "output_video_proof_manifest.json")
    scene_timeline = _load(output_dir / "scene_timeline.json")
    handoff = _load(output_dir / "yymm4_handoff_readiness.json")
    gap_ledger = _load(output_dir / "output_gap_ledger.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    html = (output_dir / "episode_002_storyboard_preview.html").read_text(encoding="utf-8")
    missing_features = (output_dir / "missing_editing_features.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-output-video-layer-proof"
    assert manifest["parallel_lane"] == "output_video_layer"
    assert manifest["shared_docs_touched"] is False
    assert manifest["gui_lane_files_touched"] == []
    assert scene_timeline["scene_count"] >= 3
    assert len(scene_timeline["scenes"]) >= 3
    assert scene_timeline["timeline_source"] == "writer_ir_sections_plus_regenerated_draft_yymm4_csv"
    assert scene_timeline["draft_csv_used"].endswith("transcript_substitution_readiness/regenerated_draft_yymm4.csv")
    assert handoff["actual_yymm4_import"] is False
    assert handoff["yymm4_rendered"] is False
    assert handoff["production_ready"] is False
    assert gap_ledger["missing_feature_count"] >= 8
    for group in REQUIRED_GAP_GROUPS:
        assert gap_ledger["groups"][group], group
        assert f"## {group}" in missing_features
    assert source_index["gui_lane_context_read_only"] is True
    assert 'data-output-video-proof="true"' in html
    assert 'data-region="storyboard-timeline"' in html
    assert 'data-region="gap-ledger"' in html
    assert "color-scheme: dark light" in html
    assert "YMM4 import, render, or public gate is crossed" in html
    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundary_flags"][flag] is True


def test_output_video_layer_validation_catches_missing_html(tmp_path) -> None:
    output_dir = tmp_path / "output_video_layer_proof"
    build_output_video_layer_proof(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_output_video_layer_proof",
    )
    (output_dir / "episode_002_storyboard_preview.html").unlink()

    readback = validate_output_video_layer_proof(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:episode_002_storyboard_preview.html" in readback["failed_checks"]


def test_cli_build_output_video_layer_proof_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_output_video_layer_proof"

    code = main(
        [
            "build-output-video-layer-proof",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_output_video_layer_proof",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["primary_review_file"].endswith("episode_002_storyboard_preview.html")
    assert payload["scene_count"] >= 3
    assert payload["timeline_source"] == "writer_ir_sections_plus_regenerated_draft_yymm4_csv"
    assert payload["draft_csv_used"].endswith("transcript_substitution_readiness/regenerated_draft_yymm4.csv")
    assert payload["missing_feature_count"] >= 8
    assert payload["buildable_local_count"] >= 4
    assert payload["blocked_by_real_input_count"] >= 1
    assert payload["blocked_by_yymm4_gate_count"] >= 1
    assert payload["blocked_by_public_rights_count"] >= 1
    assert payload["gui_lane_files_touched"] == []
    assert payload["shared_docs_touched"] is False
    assert payload["full_pytest_run"] is False
    assert payload["launcher_or_open_command"]


def test_output_video_layer_proof_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "output_video_layer_proof"
    build_output_video_layer_proof(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_output_video_layer_proof",
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
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_TRUE_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
