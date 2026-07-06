from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.review_cockpit_compact import (
    REQUIRED_BOUNDARY_FLAGS,
    REQUIRED_REVIEW_COCKPIT_FILES,
    TEMPORARY_NOTE_PHRASES,
    build_review_cockpit_compact,
    validate_review_cockpit_compact,
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

EXTERNAL_REF_MARKERS = (
    "http://",
    "https://",
    "src=\"",
    "src='",
    "href=\"",
    "href='",
    "@import",
    "url(",
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_review_cockpit_compact_builds_bounded_dark_package(tmp_path) -> None:
    output_dir = tmp_path / "review_cockpit_compact"

    readback = build_review_cockpit_compact(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_review_cockpit_compact",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_REVIEW_COCKPIT_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "review_cockpit_manifest.json")
    state = _load(output_dir / "cockpit_state.json")
    layout = _load(output_dir / "cockpit_layout_readback.json")
    source_index = _load(output_dir / "detail_source_index.json")
    html = (output_dir / "review_cockpit.html").read_text(encoding="utf-8")
    markdown = (output_dir / "review_cockpit.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-review-cockpit-compact"
    assert state["status"] == "review_cockpit_ready_local_offline"
    assert state["source_record_policy"] == "secondary_records_only"
    assert state["source_artifact_id"] == "episode_002_surface_alignment_repair_and_reviewer_packet_v1"
    assert state["focused_brief_artifact_id"] == "episode_002_focused_review_brief_dark_surface_v1"
    assert len(state["decision_options"]) == 3
    assert len(state["surface_statuses"]) == 3
    assert layout["primary_section_count"] == 5
    assert layout["decision_card_count"] == 1
    assert layout["next_action_option_count"] == 3
    assert layout["surface_status_count"] == 3
    assert layout["visible_card_count"] == 7
    assert layout["detail_section_count"] == 2
    assert layout["top_level_table_count"] == 0
    assert layout["temporary_note_count"] == 0
    assert layout["ledger_in_primary_body"] is False
    assert layout["source_record_display_zone"] == "secondary_details"
    assert layout["layout_bloat_status"] == "bounded"

    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert state["boundary_flags"][flag] is True
        assert flag in html
    assert "color-scheme: dark light" in html
    assert "prefers-color-scheme" in html
    assert 'data-review-cockpit="true"' in html
    assert 'data-section="header-strip"' in html
    assert 'data-section="decision-card"' in html
    assert 'data-section="next-action-row"' in html
    assert 'data-section="surface-status-row"' in html
    assert 'data-section="gate-strip"' in html
    assert "<details" in html
    assert "<table" not in html.lower()
    assert "surface_alignment_review_packet/aligned_review_story.md" in html
    assert "focused_review_brief/focused_review_brief.html" in html
    assert "# Episode 002 Review Cockpit" in markdown
    assert len(markdown.splitlines()) <= 90

    records = source_index["secondary_source_records"]
    assert {record["record_id"] for record in records} >= {
        "surface_alignment_aligned_story",
        "focused_review_html",
        "focused_review_validation",
        "reviewer_packet_validation",
    }
    assert all(record["display_zone"] == "secondary_details" for record in records)


def test_review_cockpit_validation_catches_missing_html(tmp_path) -> None:
    output_dir = tmp_path / "review_cockpit_compact"
    build_review_cockpit_compact(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_review_cockpit_compact",
    )
    (output_dir / "review_cockpit.html").unlink()

    readback = validate_review_cockpit_compact(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:review_cockpit.html" in readback["failed_checks"]


def test_cli_build_review_cockpit_compact_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_review_cockpit_compact"

    code = main(
        [
            "build-review-cockpit-compact",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_review_cockpit_compact",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["primary_decision"] == "Select the next episode 002 review path."
    assert payload["decision_options"] == 3
    assert payload["surface_status_count"] == 3
    assert payload["primary_section_count"] == 5
    assert payload["visible_card_count"] == 7
    assert payload["layout_bloat_status"] == "bounded"
    assert payload["source_record_policy"] == "secondary_records_only"
    assert payload["external_dependency_status"] == "absent"
    assert payload["white_background_status"] == "absent"
    assert payload["temporary_review_copy_status"] == "absent"
    assert payload["primary_human_review"].endswith("review_cockpit.html")
    assert payload["markdown_fallback"].endswith("review_cockpit.md")
    assert payload["launcher_command"]
    assert (output_dir / "validation_readback.json").exists()
    assert (output_dir / "review_cockpit.html").exists()


def test_generated_review_cockpit_has_no_external_refs_false_claims_or_temporary_copy(tmp_path) -> None:
    output_dir = tmp_path / "review_cockpit_compact"
    build_review_cockpit_compact(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_review_cockpit_compact",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
            for marker in EXTERNAL_REF_MARKERS:
                assert marker not in lowered, (path.name, marker)
            for phrase in TEMPORARY_NOTE_PHRASES:
                assert phrase not in lowered, (path.name, phrase)
            assert "#fff" not in lowered
            assert "#ffffff" not in lowered
            assert "background: white" not in lowered
            assert "background-color: white" not in lowered
