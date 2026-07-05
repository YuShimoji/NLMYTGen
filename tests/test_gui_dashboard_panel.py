from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.gui_dashboard_panel import (
    REQUIRED_GUI_PANEL_FILES,
    build_gui_dashboard_panel_package,
    validate_gui_dashboard_panel_package,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_001"

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


def test_gui_dashboard_panel_builds_static_preview_package(tmp_path) -> None:
    output_dir = tmp_path / "gui_dashboard_panel"

    readback = build_gui_dashboard_panel_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_gui_panel",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_GUI_PANEL_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "panel_manifest.json")
    adapter = _load(output_dir / "gui_dashboard_adapter.json")
    panel_data = _load(output_dir / "panel_data.json")
    static_readback = _load(output_dir / "dom_or_static_readback.json")
    html = (output_dir / "dashboard_panel_preview.html").read_text(encoding="utf-8")

    rows = {row["capability_id"]: row for row in panel_data["capability_rows"]}

    assert manifest["artifact_kind"] == "gui-dashboard-panel-ingest"
    assert adapter["source_kind"] == "dashboard_readiness_ingest"
    assert panel_data["boundary_status"]["transcript_status"] == "sample_fixture_not_real"
    assert rows["transcript_substitution"]["state"] == "sample_fixture_not_real"
    assert rows["real_transcript_input"]["state"] == "blocked_by_real_input"
    assert rows["draft_yymm4_csv"]["state"] == "draft_offline"
    assert rows["yymm4_import_preview"]["state"] == "deferred"
    assert static_readback["checks"]["html_references_expected_status_categories"] is True
    assert static_readback["checks"]["html_references_source_artifact_index"] is True
    assert 'data-dashboard-panel="true"' in html
    assert 'data-section="source-artifact-index"' in html
    assert "source_artifact_index" in html
    assert "sample_fixture_not_real" in html
    for state in (
        "ready",
        "partial",
        "sample_fixture_not_real",
        "draft_offline",
        "blocked_by_real_input",
        "blocked_by_true_gate",
        "deferred",
        "missing",
        "unknown",
    ):
        assert f'data-status="{state}"' in html


def test_gui_dashboard_panel_validation_catches_missing_html(tmp_path) -> None:
    output_dir = tmp_path / "gui_dashboard_panel"
    build_gui_dashboard_panel_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_gui_panel",
    )
    (output_dir / "dashboard_panel_preview.html").unlink()

    readback = validate_gui_dashboard_panel_package(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:dashboard_panel_preview.html" in readback["failed_checks"]


def test_cli_build_gui_dashboard_panel_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_gui_dashboard_panel"

    code = main([
        "build-gui-dashboard-panel",
        "--package",
        str(SOURCE_PACKAGE),
        "--output",
        str(output_dir),
        "--artifact-id",
        "test_cli_gui_panel",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["transcript_status"] == "sample_fixture_not_real"
    assert payload["primary_human_review"].endswith("dashboard_panel_preview.html")
    assert (output_dir / "gui_dashboard_adapter.json").exists()
    assert (output_dir / "dashboard_panel_preview.html").exists()


def test_generated_gui_dashboard_panel_text_does_not_claim_forbidden_completion(tmp_path) -> None:
    output_dir = tmp_path / "gui_dashboard_panel"
    build_gui_dashboard_panel_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_gui_panel",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
