from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.yymm4_import_preview_pack import (
    IMPORT_PREVIEW_STATUS_CATEGORIES,
    REQUIRED_IMPORT_PREVIEW_FILES,
    build_yymm4_import_preview_pack,
    validate_yymm4_import_preview_pack,
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
    '"actual_yymm4_import": true',
    '"yymm4_rendered": true',
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_yymm4_import_preview_pack_builds_local_package(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_preview_pack"

    readback = build_yymm4_import_preview_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_yymm4_import_preview_pack",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_IMPORT_PREVIEW_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "import_preview_manifest.json")
    csv_inventory = _load(output_dir / "yymm4_csv_inventory.json")
    cue_inventory = _load(output_dir / "cue_packet_inventory.json")
    writer_inventory = _load(output_dir / "writer_ir_inventory.json")
    summary = _load(output_dir / "import_readiness_summary.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    panel = (output_dir / "import_preview_panel.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "yymm4-import-preview-pack"
    assert csv_inventory["row_count"] == 9
    assert csv_inventory["header_mode"] == "headerless"
    assert csv_inventory["missing_required_fields"] == []
    assert csv_inventory["not_imported_to_yymm4"] is True
    assert (output_dir / "draft_yymm4_preview.csv").read_text(encoding="utf-8")
    assert cue_inventory["transcript_rows"] == 9
    assert cue_inventory["section_count"] == 3
    assert writer_inventory["utterance_count"] == 9
    assert writer_inventory["section_count"] == 3
    assert writer_inventory["validate_ir_ready"] is False
    assert summary["boundary_flags"]["dry_run"] is True
    assert summary["boundary_flags"]["sample_fixture_not_real"] is True
    assert summary["boundary_flags"]["no_real_transcript"] is True
    assert summary["boundary_flags"]["no_yymm4_import"] is True
    assert summary["boundary_flags"]["not_imported_to_yymm4"] is True
    assert summary["boundary_flags"]["no_production_ymmp"] is True
    assert summary["boundary_status"]["transcript_status"] == "sample_fixture_not_real"
    assert summary["boundary_status"]["real_transcript_status"] == "blocked_by_real_input"
    assert summary["boundary_status"]["yymm4_import_status"] == "blocked_by_true_gate"
    assert summary["boundary_status"]["yymm4_import_observed_status"] == "not_imported_to_yymm4"
    assert summary["validation_noise"]["status"] == "validation_noise_nonblocking"
    assert summary["validation_noise"]["blocking_for_this_slice"] is False
    assert len(source_index["source_artifacts"]) >= 8
    assert "source_artifact_index.json" in panel
    assert "draft_yymm4_preview.csv" in panel
    assert "not_imported_to_yymm4" in panel
    for state in IMPORT_PREVIEW_STATUS_CATEGORIES:
        assert state in panel


def test_yymm4_import_preview_validation_catches_missing_panel(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_preview_pack"
    build_yymm4_import_preview_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_yymm4_import_preview_pack",
    )
    (output_dir / "import_preview_panel.md").unlink()

    readback = validate_yymm4_import_preview_pack(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:import_preview_panel.md" in readback["failed_checks"]


def test_cli_build_yymm4_import_preview_pack_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_yymm4_import_preview_pack"

    code = main([
        "build-yymm4-import-preview-pack",
        "--package",
        str(SOURCE_PACKAGE),
        "--output",
        str(output_dir),
        "--artifact-id",
        "test_cli_yymm4_import_preview_pack",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["csv_row_count"] == 9
    assert payload["csv_header_mode"] == "headerless"
    assert payload["transcript_status"] == "sample_fixture_not_real"
    assert payload["yymm4_import_status"] == "blocked_by_true_gate"
    assert payload["validation_noise_status"] == "validation_noise_nonblocking"
    assert payload["primary_human_review"].endswith("import_preview_panel.md")
    assert payload["preview_csv"].endswith("draft_yymm4_preview.csv")
    assert (output_dir / "import_readiness_summary.json").exists()
    assert (output_dir / "draft_yymm4_preview.csv").exists()


def test_generated_yymm4_import_preview_pack_does_not_claim_forbidden_completion(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_preview_pack"
    build_yymm4_import_preview_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_yymm4_import_preview_pack",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
