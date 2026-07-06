from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.dashboard_readiness_ingest import (
    REQUIRED_DASHBOARD_INGEST_FILES,
    build_dashboard_readiness_ingest_package,
    validate_dashboard_readiness_ingest_package,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"

FORBIDDEN_COMPLETION_CLAIMS = (
    '"render_completion": true',
    '"production_ready": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"video_generation": true',
    '"thumbnail_image_generated": true',
    '"youtube_uploaded": true',
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_dashboard_readiness_ingest_builds_status_package(tmp_path) -> None:
    output_dir = tmp_path / "dashboard_readiness_ingest"

    readback = build_dashboard_readiness_ingest_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_dashboard_ingest",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_DASHBOARD_INGEST_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "dashboard_manifest.json")
    summary = _load(output_dir / "readiness_summary.json")
    pipeline = _load(output_dir / "pipeline_status.json")
    grid = _load(output_dir / "capability_glyph_grid.json")
    panel = _load(output_dir / "symbolic_visual_panel.json")
    source_index = _load(output_dir / "source_artifact_index.json")

    rows = {row["capability_id"]: row for row in grid["rows"]}
    artifact_ids = {artifact["id"] for artifact in source_index["artifacts"]}

    assert manifest["artifact_kind"] == "dashboard-readiness-ingest"
    assert summary["boundary_status"]["transcript_status"] == "sample_fixture_not_real"
    assert summary["boundary_status"]["yymm4_import_status"] == "blocked_by_true_gate"
    assert summary["input_reality"]["sample_fixture_used"] is True
    assert summary["boundary_flags"]["dry_run"] is True
    assert summary["boundary_flags"]["no_real_transcript"] is True
    assert summary["boundary_flags"]["no_yymm4_import"] is True
    assert summary["seed_origin"]["manual_copy_of_original_pilot"] is False
    assert summary["seed_origin"]["required_real_inputs_present"] is True
    assert manifest["boundaries"]["no_external_image_or_media_download"] is True
    assert manifest["boundaries"]["no_yymm4_import"] is True
    assert "real_transcript_input" in summary["needs_real_transcript_input"]
    assert rows["content_spine_002"]["state"] == "draft_offline"
    assert rows["ir_bridge_002"]["state"] == "draft_offline"
    assert rows["transcript_substitution_002"]["state"] == "sample_fixture_not_real"
    assert rows["dashboard_ingest"]["state"] == "ready"
    assert rows["yymm4_import_preview"]["state"] == "deferred"
    assert panel["bar_mode"] == "hypothesis"
    assert {node["node"] for node in pipeline["route"]} >= {
        "content_spine_002",
        "ir_bridge_002",
        "transcript_substitution_002",
    }
    assert {
        "content_manifest",
        "content_source_seed_reference",
        "transcript_probe",
        "transcript_readback",
    }.issubset(artifact_ids)
    assert readback["primary_machine_readable"].endswith("readiness_summary.json")
    assert readback["primary_human_review"].endswith("dashboard_preview.md")
    assert "build-transcript-substitution" not in readback["next_action"]


def test_dashboard_readiness_validation_catches_missing_preview(tmp_path) -> None:
    output_dir = tmp_path / "dashboard_readiness_ingest"
    build_dashboard_readiness_ingest_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_dashboard_ingest",
    )
    (output_dir / "dashboard_preview.md").unlink()

    readback = validate_dashboard_readiness_ingest_package(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:dashboard_preview.md" in readback["failed_checks"]


def test_cli_build_dashboard_readiness_ingest_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_dashboard_readiness_ingest"

    code = main([
        "build-dashboard-readiness-ingest",
        "--package",
        str(SOURCE_PACKAGE),
        "--output",
        str(output_dir),
        "--artifact-id",
        "test_cli_dashboard_ingest",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["transcript_status"] == "sample_fixture_not_real"
    assert (output_dir / "readiness_summary.json").exists()
    assert (output_dir / "dashboard_preview.md").exists()


def test_generated_dashboard_ingest_text_does_not_claim_forbidden_completion(tmp_path) -> None:
    output_dir = tmp_path / "dashboard_readiness_ingest"
    build_dashboard_readiness_ingest_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_dashboard_ingest",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
