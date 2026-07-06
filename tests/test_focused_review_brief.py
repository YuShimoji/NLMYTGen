from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.focused_review_brief import (
    REQUIRED_BOUNDARY_FLAGS,
    REQUIRED_FOCUSED_REVIEW_FILES,
    build_focused_review_brief,
    validate_focused_review_brief,
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


def test_focused_review_brief_builds_dark_decision_first_package(tmp_path) -> None:
    output_dir = tmp_path / "focused_review_brief"

    readback = build_focused_review_brief(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_focused_review_brief",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_FOCUSED_REVIEW_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "focused_review_manifest.json")
    summary = _load(output_dir / "review_summary.json")
    decision_card = _load(output_dir / "review_decision_card.json")
    source_index = _load(output_dir / "detail_source_index.json")
    html = (output_dir / "focused_review_brief.html").read_text(encoding="utf-8")
    markdown = (output_dir / "focused_review_brief.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-focused-review-brief"
    assert summary["status"] == "focused_review_brief_ready_local_offline"
    assert summary["source_artifact_id"] == "episode_002_surface_alignment_repair_and_reviewer_packet_v1"
    assert summary["current_state"]["legacy_story_role"] == "source_record"
    assert summary["current_state"]["still_open_mismatch_count"] == 0
    assert len(summary["top_summary_lines"]) == 3
    assert all(len(line) <= 160 for line in summary["top_summary_lines"])
    assert len(summary["evidence_cards"]) == 3
    assert len(decision_card["primary_questions"]) == 1
    assert decision_card["decision_card_count"] == 1
    assert len(decision_card["next_action_cards"]) == 3
    assert {card["option_id"] for card in decision_card["next_action_cards"]} == {
        "real_input_replacement",
        "actual_yymm4_import_observation_no_render",
        "hold_review_later",
    }

    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert summary["boundary_flags"][flag] is True
        assert flag in html
    assert "color-scheme: dark light" in html
    assert "prefers-color-scheme" in html
    assert 'data-section="decision-card"' in html
    assert 'data-section="three-line-summary"' in html
    assert 'data-section="next-action-cards"' in html
    assert 'data-section="evidence-cards"' in html
    assert 'data-section="gate-strip"' in html
    assert "<details" in html
    assert "remaining_mismatch_ledger.json" in html
    assert "Repair Ledger" not in html
    assert "# Episode 002 Focused Review Brief" in markdown
    assert "## Details" not in markdown
    assert len(markdown.splitlines()) <= 80
    assert source_index["legacy_story_role"] == "source_record"
    assert source_index["primary_review_surface"].endswith("focused_review_brief.html")


def test_focused_review_brief_validation_catches_missing_html(tmp_path) -> None:
    output_dir = tmp_path / "focused_review_brief"
    build_focused_review_brief(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_focused_review_brief",
    )
    (output_dir / "focused_review_brief.html").unlink()

    readback = validate_focused_review_brief(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:focused_review_brief.html" in readback["failed_checks"]


def test_cli_build_focused_review_brief_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_focused_review_brief"

    code = main(
        [
            "build-focused-review-brief",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_focused_review_brief",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["primary_question"]
    assert payload["top_summary_length"] == 3
    assert payload["decision_cards"] == 3
    assert payload["evidence_cards"] == 3
    assert payload["external_dependency_status"] == "absent"
    assert payload["white_background_status"] == "absent"
    assert payload["primary_human_review"].endswith("focused_review_brief.html")
    assert payload["markdown_fallback"].endswith("focused_review_brief.md")
    assert (output_dir / "validation_readback.json").exists()
    assert (output_dir / "focused_review_brief.html").exists()


def test_generated_focused_review_brief_has_no_external_refs_or_false_claims(tmp_path) -> None:
    output_dir = tmp_path / "focused_review_brief"
    build_focused_review_brief(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_focused_review_brief",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
            for marker in EXTERNAL_REF_MARKERS:
                assert marker not in lowered, (path.name, marker)
            assert "#fff" not in lowered
            assert "#ffffff" not in lowered
            assert "background: white" not in lowered
