from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.ymm4_import_preview_pack import (
    REQUIRED_IMPORT_PREVIEW_FILES,
    build_ymm4_import_preview_pack,
    validate_ymm4_import_preview_pack,
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
    '"no_yymm4_gui_launch_or_import_or_render": false',
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_yymm4_import_preview_pack_builds_from_current_pilot_artifacts(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_preview_pack"

    readback = build_ymm4_import_preview_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_import_preview",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_IMPORT_PREVIEW_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "import_preview_manifest.json")
    csv_inventory = _load(output_dir / "yymm4_csv_inventory.json")
    cue_inventory = _load(output_dir / "cue_packet_inventory.json")
    writer_inventory = _load(output_dir / "writer_ir_inventory.json")
    summary = _load(output_dir / "import_readiness_summary.json")
    html = (output_dir / "import_preview_panel.html").read_text(encoding="utf-8")
    markdown = (output_dir / "import_preview_panel.md").read_text(encoding="utf-8")

    rows = {row["capability_id"]: row for row in summary["readiness_rows"]}
    row_states = {row["state"] for row in summary["readiness_rows"]}

    assert manifest["artifact_kind"] == "ymm4-import-preview-pack"
    assert manifest["boundaries"]["no_yymm4_gui_launch_or_import_or_render"] is True
    assert csv_inventory["row_count"] == 10
    assert csv_inventory["column_count_ok"] is True
    assert csv_inventory["header_present"] is False
    assert csv_inventory["csv_contract"]["required_headers"] == ["speaker", "text"]
    assert csv_inventory["csv_contract"]["missing_headers"] == ["speaker", "text"]
    assert csv_inventory["csv_contract"]["missing_headers_block_import"] is False
    assert (output_dir / "draft_yymm4_import_preview.csv").exists()
    assert cue_inventory["transcript_row_count"] == csv_inventory["row_count"]
    assert cue_inventory["external_llm_called"] is False
    assert writer_inventory["utterance_count"] == csv_inventory["row_count"]
    assert writer_inventory["row_ranges_present"] is False
    assert summary["boundary_status"]["transcript_status"] == "sample_fixture_not_real"
    assert summary["boundary_status"]["ymm4_gui_status"] == "blocked_by_true_gate"
    assert summary["boundary_status"]["ymm4_render_status"] == "blocked_by_true_gate"
    assert rows["transcript_source"]["state"] == "sample_fixture_not_real"
    assert rows["real_transcript_input"]["state"] == "blocked_by_real_input"
    assert rows["draft_yymm4_csv"]["state"] == "draft_offline"
    assert rows["csv_header_contract"]["state"] == "partial"
    assert rows["production_ymmp"]["state"] == "missing"
    assert {
        "ready",
        "partial",
        "sample_fixture_not_real",
        "draft_offline",
        "blocked_by_real_input",
        "blocked_by_true_gate",
        "deferred",
        "missing",
        "unknown",
    }.issubset(row_states)
    assert 'data-import-preview-pack="true"' in html
    assert 'data-section="csv-contract"' in html
    assert "source_artifact_index" in html
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
        assert state in markdown


def test_yymm4_import_preview_validation_catches_missing_copied_csv(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_preview_pack"
    build_ymm4_import_preview_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_import_preview",
    )
    (output_dir / "draft_yymm4_import_preview.csv").unlink()

    readback = validate_ymm4_import_preview_pack(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:draft_yymm4_import_preview.csv" in readback["failed_checks"]
    assert "copied_csv_missing" in readback["failed_checks"]


def test_cli_build_yymm4_import_preview_pack_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_ymm4_import_preview_pack"

    code = main([
        "build-yymm4-import-preview-pack",
        "--package",
        str(SOURCE_PACKAGE),
        "--output",
        str(output_dir),
        "--artifact-id",
        "test_cli_import_preview",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["transcript_status"] == "sample_fixture_not_real"
    assert payload["draft_csv_rows"] == 10
    assert payload["primary_machine_readable"].endswith("import_readiness_summary.json")
    assert (output_dir / "import_preview_panel.md").exists()
    assert (output_dir / "import_preview_panel.html").exists()


def test_generated_yymm4_import_preview_text_does_not_claim_forbidden_completion(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_preview_pack"
    build_ymm4_import_preview_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_import_preview",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
