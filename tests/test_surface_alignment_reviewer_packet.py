from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.surface_alignment_reviewer_packet import (
    REPAIR_CLASSIFICATIONS,
    REQUIRED_BOUNDARY_FLAGS,
    REQUIRED_REVIEWER_PACKET_FILES,
    build_surface_alignment_reviewer_packet,
    validate_surface_alignment_reviewer_packet,
)
from src.pipeline.surface_alignment_pack import SURFACE_STATUS_CATEGORIES


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


def test_surface_alignment_reviewer_packet_builds_repaired_review_entrypoint(tmp_path) -> None:
    output_dir = tmp_path / "surface_alignment_review_packet"

    readback = build_surface_alignment_reviewer_packet(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_surface_alignment_reviewer_packet",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_REVIEWER_PACKET_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "reviewer_packet_manifest.json")
    summary = _load(output_dir / "alignment_repair_summary.json")
    ledger = _load(output_dir / "remaining_mismatch_ledger.json")
    next_action = _load(output_dir / "next_action_readback.json")
    boundary = _load(output_dir / "boundary_status_readback.json")
    crosswalk = _load(output_dir / "source_artifact_crosswalk_readback.json")
    story = (output_dir / "aligned_review_story.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "surface-alignment-reviewer-packet"
    assert summary["status"] == "reviewer_packet_ready_local_offline"
    assert summary["repair_mode"] == "packet_level_readback_repair_no_underlying_surface_rewrite"
    assert summary["reviewer_packet_status"] == "ready"
    assert summary["surface_statuses"]["gui_panel_status"] == "ready"
    assert summary["surface_statuses"]["import_preview_status"] == "ready"
    assert summary["surface_statuses"]["thumbnail_proof_status"] == "ready"
    assert summary["boundary_consistency_status"] == "accepted_nonblocking"
    assert summary["next_action_consistency_status"] == "packet_resolved"
    assert summary["source_crosswalk_status"] == "aligned"

    assert set(SURFACE_STATUS_CATEGORIES).issubset(set(summary["status_categories"]))
    assert set(REPAIR_CLASSIFICATIONS).issubset(set(summary["repair_classifications"]))
    assert ledger["prior_mismatch_count"] == 8
    assert ledger["still_open_mismatch_count"] == 0
    assert ledger["blocking_for_reviewer_packet"] is False
    assert ledger["underlying_surfaces_rewritten"] is False
    repair_classes = {row["repair_classification"] for row in ledger["rows"]}
    assert "resolved" in repair_classes
    assert "accepted_nonblocking" in repair_classes
    assert repair_classes <= set(REPAIR_CLASSIFICATIONS)
    assert not {"boundary_mismatch", "missing_reference", "unknown"} & repair_classes

    assert next_action["status"] == "packet_resolved"
    option_ids = {option["option_id"] for option in next_action["advisory_next_options"]}
    assert "real_input_replacement" in option_ids
    assert "actual_yymm4_import_observation_no_render" in option_ids
    assert "yymm4_render" in " ".join(next_action["not_performed"])

    assert boundary["status"] == "closed_gates_confirmed"
    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert boundary["boundary_flags"][flag] is True
    assert boundary["closed_gate_status"]["yymm4_import_status"] == "no_yymm4_import"
    assert boundary["closed_gate_status"]["thumbnail_approval_status"] == "thumbnail_context_only"

    assert crosswalk["overall_status"] == "aligned"
    assert crosswalk["missing_reference_count"] == 0
    source_ids = {row["artifact_id"] for row in crosswalk["source_artifact_rows"]}
    assert "gui_panel_data" in source_ids
    assert "import_readiness_summary" in source_ids
    assert "thumbnail_variants" in source_ids
    assert "validation_ledger" in source_ids

    for status in SURFACE_STATUS_CATEGORIES:
        assert status in story
    for marker in (
        "remaining_mismatch_ledger.json",
        "next_action_readback.json",
        "boundary_status_readback.json",
        "source_artifact_crosswalk_readback.json",
        "thumbnail_context_only",
        "validation_noise_nonblocking",
        "not_production_ready",
        "no_yymm4_import",
    ):
        assert marker in story


def test_surface_alignment_reviewer_packet_validation_catches_missing_story(tmp_path) -> None:
    output_dir = tmp_path / "surface_alignment_review_packet"
    build_surface_alignment_reviewer_packet(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_surface_alignment_reviewer_packet",
    )
    (output_dir / "aligned_review_story.md").unlink()

    readback = validate_surface_alignment_reviewer_packet(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:aligned_review_story.md" in readback["failed_checks"]


def test_cli_build_surface_reviewer_packet_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_surface_alignment_review_packet"

    code = main(
        [
            "build-surface-reviewer-packet",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_surface_alignment_reviewer_packet",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["reviewer_packet_status"] == "ready"
    assert payload["boundary_consistency_status"] == "accepted_nonblocking"
    assert payload["next_action_consistency_status"] == "packet_resolved"
    assert payload["source_crosswalk_status"] == "aligned"
    assert payload["prior_mismatch_count"] == 8
    assert payload["still_open_mismatch_count"] == 0
    assert payload["primary_machine_readable"].endswith("validation_readback.json")
    assert payload["primary_human_review"].endswith("aligned_review_story.md")
    assert (output_dir / "validation_readback.json").exists()
    assert (output_dir / "aligned_review_story.md").exists()


def test_generated_surface_reviewer_packet_has_no_completion_or_external_media_claims(tmp_path) -> None:
    output_dir = tmp_path / "surface_alignment_review_packet"
    build_surface_alignment_reviewer_packet(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_surface_alignment_reviewer_packet",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
            for marker in EXTERNAL_MEDIA_MARKERS:
                assert marker not in lowered, (path.name, marker)
