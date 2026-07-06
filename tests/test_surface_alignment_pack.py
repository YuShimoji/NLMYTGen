from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.surface_alignment_pack import (
    MISMATCH_CATEGORIES,
    REQUIRED_SURFACE_ALIGNMENT_FILES,
    SURFACE_STATUS_CATEGORIES,
    build_surface_alignment_pack,
    validate_surface_alignment_pack,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"

FORBIDDEN_COMPLETION_CLAIMS = (
    '"render_completion": true',
    '"production_ready": true',
    '"production_thumbnail_ready": true',
    '"public_ready": true',
    '"rights_accepted": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"video_generation": true',
    '"thumbnail_image_generated": true',
    '"youtube_uploaded": true',
    '"actual_yymm4_import": true',
    '"yymm4_rendered": true',
)

EXTERNAL_MEDIA_MARKERS = (
    "data:image",
    "src=\"http://",
    "src=\"https://",
    "src='http://",
    "src='https://",
    "href=\"http://",
    "href=\"https://",
    "href='http://",
    "href='https://",
    "<image href=\"http",
    "<image href='http",
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_surface_alignment_pack_builds_cross_surface_review_package(tmp_path) -> None:
    output_dir = tmp_path / "surface_alignment_pack"

    readback = build_surface_alignment_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_surface_alignment_pack",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_SURFACE_ALIGNMENT_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "surface_alignment_manifest.json")
    summary = _load(output_dir / "surface_alignment_summary.json")
    matrix = _load(output_dir / "surface_status_matrix.json")
    crosswalk = _load(output_dir / "source_artifact_crosswalk.json")
    boundary = _load(output_dir / "boundary_consistency_report.json")
    next_action = _load(output_dir / "next_action_consistency_report.json")
    story = (output_dir / "review_story.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "surface-alignment-pack"
    assert summary["status"] == "alignment_ready_local_offline"
    assert summary["boundary_flags"]["dry_run"] is True
    assert summary["boundary_flags"]["sample_fixture_not_real"] is True
    assert summary["boundary_flags"]["no_real_transcript"] is True
    assert summary["boundary_flags"]["rights_boundary"] is True
    assert summary["boundary_flags"]["public_upload_closed"] is True
    assert summary["boundary_flags"]["yymm4_render_closed"] is True
    assert summary["boundary_flags"]["no_yymm4_import"] is True
    assert summary["boundary_flags"]["thumbnail_context_only"] is True
    assert summary["boundary_flags"]["validation_noise_nonblocking"] is True
    assert summary["surface_alignment_results"]["gui_panel_status"] == "ready"
    assert summary["surface_alignment_results"]["import_preview_status"] == "ready"
    assert summary["surface_alignment_results"]["thumbnail_proof_status"] == "ready"
    assert summary["surface_alignment_results"]["boundary_consistency_status"] == "minor_label_drift"
    assert summary["surface_alignment_results"]["next_action_consistency_status"] == "stale_next_action"

    assert set(SURFACE_STATUS_CATEGORIES).issubset(set(matrix["status_categories"]))
    assert set(MISMATCH_CATEGORIES).issubset(set(matrix["mismatch_categories"]))
    assert len(matrix["rows"]) >= 10
    classifications = {row["classification"] for row in matrix["rows"]}
    assert "aligned" in classifications
    assert "minor_label_drift" in classifications
    assert "stale_next_action" in classifications

    crosswalk_ids = {row["artifact_id"] for row in crosswalk["crosswalk_rows"]}
    assert crosswalk["overall_status"] == "aligned"
    assert "gui_panel_data" in crosswalk_ids
    assert "import_readiness_summary" in crosswalk_ids
    assert "thumbnail_variants" in crosswalk_ids
    assert "validation_ledger" in crosswalk_ids
    assert crosswalk["missing_reference_count"] == 0

    boundary_ids = {row["boundary_id"] for row in boundary["boundary_rows"]}
    assert boundary["overall_status"] == "minor_label_drift"
    assert "dry_run" in boundary_ids
    assert "thumbnail_context_only" in boundary_ids
    assert "validation_noise_nonblocking" in boundary_ids
    assert all(row["classification"] in MISMATCH_CATEGORIES for row in boundary["boundary_rows"])

    assert next_action["overall_status"] == "stale_next_action"
    assert any(row["classification"] == "stale_next_action" for row in next_action["next_action_rows"])

    for status in SURFACE_STATUS_CATEGORIES:
        assert status in story
    for marker in (
        "source_artifact_crosswalk.json",
        "boundary_consistency_report.json",
        "next_action_consistency_report.json",
        "thumbnail_context_only",
        "blocked_by_true_gate",
    ):
        assert marker in story


def test_surface_alignment_validation_catches_missing_review_story(tmp_path) -> None:
    output_dir = tmp_path / "surface_alignment_pack"
    build_surface_alignment_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_surface_alignment_pack",
    )
    (output_dir / "review_story.md").unlink()

    readback = validate_surface_alignment_pack(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:review_story.md" in readback["failed_checks"]


def test_cli_build_surface_alignment_pack_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_surface_alignment_pack"

    code = main([
        "build-surface-alignment-pack",
        "--package",
        str(SOURCE_PACKAGE),
        "--output",
        str(output_dir),
        "--artifact-id",
        "test_cli_surface_alignment_pack",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["gui_panel_status"] == "ready"
    assert payload["import_preview_status"] == "ready"
    assert payload["thumbnail_proof_status"] == "ready"
    assert payload["source_crosswalk_status"] == "aligned"
    assert payload["boundary_consistency_status"] == "minor_label_drift"
    assert payload["next_action_consistency_status"] == "stale_next_action"
    assert payload["primary_machine_readable"].endswith("surface_alignment_summary.json")
    assert payload["primary_human_review"].endswith("review_story.md")
    assert (output_dir / "surface_alignment_summary.json").exists()
    assert (output_dir / "review_story.md").exists()


def test_generated_surface_alignment_pack_has_no_completion_or_external_media_claims(tmp_path) -> None:
    output_dir = tmp_path / "surface_alignment_pack"
    build_surface_alignment_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_surface_alignment_pack",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
            for marker in EXTERNAL_MEDIA_MARKERS:
                assert marker not in lowered, (path.name, marker)
