from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.gui_dashboard_panel import (
    PANEL_STATUS_CATEGORIES,
    REQUIRED_GUI_PANEL_FILES,
    build_gui_dashboard_panel_package,
    validate_gui_dashboard_panel_package,
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
    source_index = _load(output_dir / "source_artifact_index.json")
    static_readback = _load(output_dir / "dom_or_static_readback.json")
    html = (output_dir / "dashboard_panel_preview.html").read_text(encoding="utf-8")

    rows = {row["capability_id"]: row for row in panel_data["capability_rows"]}

    assert manifest["artifact_kind"] == "gui-dashboard-panel-ingest"
    assert adapter["source_kind"] == "dashboard_readiness_ingest"
    assert panel_data["boundary_status"]["transcript_status"] == "sample_fixture_not_real"
    assert panel_data["boundary_status"]["yymm4_import_status"] == "blocked_by_true_gate"
    assert panel_data["boundary_flags"]["dry_run"] is True
    assert panel_data["boundary_flags"]["no_real_transcript"] is True
    assert panel_data["boundary_flags"]["no_yymm4_import"] is True
    assert panel_data["boundary_flags"]["public_upload_closed"] is True
    assert panel_data["validation_noise"]["status"] == "validation_noise_nonblocking"
    assert panel_data["validation_noise"]["blocking_for_this_slice"] is False
    assert rows["content_spine_002"]["state"] == "draft_offline"
    assert rows["ir_bridge_002"]["state"] == "draft_offline"
    assert rows["transcript_substitution_002"]["state"] == "sample_fixture_not_real"
    assert rows["real_transcript_input"]["state"] == "blocked_by_real_input"
    assert rows["draft_yymm4_csv"]["state"] == "draft_offline"
    assert rows["validation_noise"]["state"] == "validation_noise_nonblocking"
    assert rows["yymm4_import_preview"]["state"] == "deferred"
    assert source_index["validation_ledger"]["status"] == "validation_noise_nonblocking"
    assert source_index["panel_inputs"]["validation_ledger"].endswith("validation_drift_velocity_recovery_v1.json")
    assert static_readback["checks"]["html_references_expected_status_categories"] is True
    assert static_readback["checks"]["html_references_source_artifact_index"] is True
    assert static_readback["checks"]["html_references_validation_noise"] is True
    assert static_readback["checks"]["html_references_yymm4_import_gate"] is True
    assert static_readback["checks"]["html_references_boundary_flags"] is True
    assert 'data-dashboard-panel="true"' in html
    assert 'data-section="source-artifact-index"' in html
    assert "source_artifact_index" in html
    assert "validation_noise_nonblocking" in html
    assert "dry_run" in html
    assert "no_yymm4_import" in html
    assert "public_upload_closed" in html
    assert "sample_fixture_not_real" in html
    for state in PANEL_STATUS_CATEGORIES:
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
    assert payload["validation_noise_status"] == "validation_noise_nonblocking"
    assert payload["primary_human_review"].endswith("dashboard_panel_preview.html")
    assert payload["source_artifact_index"].endswith("source_artifact_index.json")
    assert (output_dir / "gui_dashboard_adapter.json").exists()
    assert (output_dir / "source_artifact_index.json").exists()
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
