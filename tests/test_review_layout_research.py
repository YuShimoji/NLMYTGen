from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.review_layout_research import (
    REQUIRED_BOUNDARY_FLAGS,
    REQUIRED_LAYOUT_RESEARCH_FILES,
    build_review_layout_research,
    validate_review_layout_research,
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


def test_review_layout_research_builds_packet_with_single_recommendation(tmp_path) -> None:
    output_dir = tmp_path / "review_layout_research"

    readback = build_review_layout_research(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_review_layout_research",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_LAYOUT_RESEARCH_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "layout_research_manifest.json")
    principles = _load(output_dir / "layout_principles.json")
    matrix = _load(output_dir / "layout_decision_matrix.json")
    report = (output_dir / "layout_research_report.md").read_text(encoding="utf-8")
    diagnosis = (output_dir / "current_ui_diagnosis.md").read_text(encoding="utf-8")
    recommendation = (output_dir / "final_layout_recommendation.md").read_text(encoding="utf-8")
    wireframe_html = (output_dir / "candidate_wireframes.html").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-review-layout-research"
    assert manifest["status"] == "layout_research_ready_local_offline"
    assert manifest["evaluated_prototype"]["verdict"] == "weak_pass_evaluated_prototype"
    assert manifest["selected_candidate"] == "candidate_b_guided_decision_flow"
    assert matrix["selected_candidate_ids"] == ["candidate_b_guided_decision_flow"]
    assert matrix["winning_candidate"] == "candidate_b_guided_decision_flow"
    assert len(matrix["pattern_benchmark"]) >= 6
    assert len(matrix["candidate_wireframes"]) == 3
    assert len(principles["principles"]) >= 6
    assert "Selected candidate: `candidate_b_guided_decision_flow`" in report
    assert "weak_pass_evaluated_prototype" in diagnosis
    assert "selected_candidate: candidate_b_guided_decision_flow" in recommendation
    assert "## Test Anti-Goals" in recommendation
    assert 'data-selected-candidate="candidate_b_guided_decision_flow"' in wireframe_html
    assert "color-scheme: dark light" in wireframe_html
    assert "prefers-color-scheme" in wireframe_html

    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundary_flags"][flag] is True
        assert flag in wireframe_html


def test_review_layout_research_validation_catches_missing_wireframe(tmp_path) -> None:
    output_dir = tmp_path / "review_layout_research"
    build_review_layout_research(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_review_layout_research",
    )
    (output_dir / "candidate_wireframes.html").unlink()

    readback = validate_review_layout_research(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:candidate_wireframes.html" in readback["failed_checks"]


def test_cli_build_review_layout_research_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_review_layout_research"

    code = main(
        [
            "build-review-layout-research",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_review_layout_research",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["selected_candidate"] == "candidate_b_guided_decision_flow"
    assert payload["checks"]["selected_candidate_exactly_one"] is True
    assert payload["checks"]["wireframes_have_no_external_dependencies"] is True
    assert payload["checks"]["forbidden_true_claims_absent"] is True
    assert payload["primary_human_review"].endswith("layout_research_report.md")
    assert payload["candidate_wireframes"].endswith("candidate_wireframes.html")
    assert payload["launcher_command"]


def test_generated_layout_research_wireframes_are_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "review_layout_research"
    build_review_layout_research(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_review_layout_research",
    )

    for path in (output_dir / "candidate_wireframes.html", output_dir / "candidate_wireframes.md"):
        text = path.read_text(encoding="utf-8").lower()
        for marker in EXTERNAL_REF_MARKERS:
            assert marker not in text, (path.name, marker)

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
