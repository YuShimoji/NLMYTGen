from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.review_layout_second_pass import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
    REQUIRED_BOUNDARY_FLAGS,
    REQUIRED_CANDIDATES,
    REQUIRED_LAYOUT_SECOND_PASS_FILES,
    SELECTED_CANDIDATE,
    build_review_layout_second_pass,
    validate_review_layout_second_pass,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_review_layout_second_pass_builds_split_view_benchmark(tmp_path) -> None:
    output_dir = tmp_path / "review_layout_second_pass"

    readback = build_review_layout_second_pass(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_layout_second_pass",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_LAYOUT_SECOND_PASS_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "layout_second_pass_manifest.json")
    matrix = _load(output_dir / "layout_candidate_matrix.json")
    html = (output_dir / "candidate_wireframes_second_pass.html").read_text(encoding="utf-8")
    recommendation = (output_dir / "final_layout_recommendation.md").read_text(encoding="utf-8")
    evidence = (output_dir / "evidence_handling_report.md").read_text(encoding="utf-8")
    card_bloat = (output_dir / "card_bloat_risk_report.md").read_text(encoding="utf-8")
    split_benchmark = (output_dir / "split_view_benchmark.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-review-layout-second-pass"
    assert manifest["status"] == "layout_second_pass_ready_local_offline"
    assert manifest["evaluated_guided_flow"]["verdict"] == "weak_pass_evaluated_prototype"
    assert manifest["selected_candidate"] == SELECTED_CANDIDATE
    assert matrix["selected_candidate_ids"] == [SELECTED_CANDIDATE]
    assert matrix["winning_candidate"] == SELECTED_CANDIDATE
    assert len(matrix["candidates"]) >= 6
    candidate_ids = {row["candidate_id"] for row in matrix["candidates"]}
    assert set(REQUIRED_CANDIDATES).issubset(candidate_ids)
    assert 'data-selected-candidate="candidate_a_split_view_decision_evidence_pane"' in html
    assert "data-left-pane" in html
    assert "data-right-pane" in html
    assert "Evidence preview pane" in html
    assert "Gate context" in html
    assert "Active path spine" in html
    assert "Selected node detail" in html
    assert "Current card/drawer pattern" in html
    assert "color-scheme: dark light" in html
    assert "prefers-color-scheme" in html
    assert "selected_candidate: candidate_a_split_view_decision_evidence_pane" in recommendation
    assert "user-situation-first" in recommendation
    assert "visible active path" in recommendation
    assert "evidence is available without becoming a junk drawer" in recommendation
    assert "not a generic drawer" in evidence
    assert "card-bloat risk: high" in card_bloat
    assert "split view: decision rail + evidence/preview pane" in split_benchmark

    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundary_flags"][flag] is True
        assert flag in html


def test_review_layout_second_pass_validation_catches_missing_wireframe(tmp_path) -> None:
    output_dir = tmp_path / "review_layout_second_pass"
    build_review_layout_second_pass(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_layout_second_pass",
    )
    (output_dir / "candidate_wireframes_second_pass.html").unlink()

    readback = validate_review_layout_second_pass(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:candidate_wireframes_second_pass.html" in readback["failed_checks"]


def test_cli_build_review_layout_second_pass_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_review_layout_second_pass"

    code = main(
        [
            "build-review-layout-second-pass",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_layout_second_pass",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["selected_candidate"] == SELECTED_CANDIDATE
    assert payload["checks"]["candidate_count"] >= 6
    assert payload["checks"]["selected_candidate_exactly_one"] is True
    assert payload["checks"]["split_view_candidate_present"] is True
    assert payload["checks"]["split_view_panes_present"] is True
    assert payload["checks"]["evidence_not_generic_drawer"] is True
    assert payload["checks"]["card_bloat_risk_classified"] is True
    assert payload["checks"]["wireframes_have_no_external_dependencies"] is True
    assert payload["primary_human_review"].endswith("split_view_benchmark.md")
    assert payload["candidate_wireframes"].endswith("candidate_wireframes_second_pass.html")
    assert payload["launcher_command"]


def test_generated_review_layout_second_pass_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "review_layout_second_pass"
    build_review_layout_second_pass(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_layout_second_pass",
    )

    readback = _load(output_dir / "validation_readback.json")
    assert readback["checks"]["wireframes_have_no_external_dependencies"] is True
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["boundary_flags_present"] is True
    assert readback["checks"]["test_strategy_present"] is True

    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for marker in EXTERNAL_REF_MARKERS:
            assert marker not in text, (path.name, marker)

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_TRUE_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
