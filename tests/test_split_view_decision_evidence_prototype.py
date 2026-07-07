from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
    PRIMARY_RECOMMENDATION_NO_REAL_INPUT,
    REQUIRED_BOUNDARY_FLAGS,
    REQUIRED_SPLIT_VIEW_FILES,
    SELECTED_CANDIDATE,
    build_split_view_decision_evidence_prototype,
    validate_split_view_decision_evidence_prototype,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_split_view_decision_evidence_builds_visible_evidence_prototype(tmp_path) -> None:
    output_dir = tmp_path / "split_view_decision_evidence_prototype"

    readback = build_split_view_decision_evidence_prototype(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_split_view_decision_evidence",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_SPLIT_VIEW_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "split_view_manifest.json")
    state = _load(output_dir / "split_view_state.json")
    recommendation = _load(output_dir / "recommendation_readback.json")
    evidence = _load(output_dir / "evidence_pane_readback.json")
    source_index = _load(output_dir / "source_record_index.json")
    metrics = _load(output_dir / "layout_metrics.json")
    html = (output_dir / "split_view_decision_evidence.html").read_text(encoding="utf-8")
    markdown = (output_dir / "split_view_decision_evidence.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-split-view-decision-evidence-prototype"
    assert manifest["status"] == "split_view_prototype_ready_local_offline"
    assert manifest["selected_candidate"] == SELECTED_CANDIDATE
    assert state["real_input_available"] is False
    assert state["explicit_yymm4_observation_selected"] is False
    assert state["primary_recommendation"] == PRIMARY_RECOMMENDATION_NO_REAL_INPUT
    assert state["fallback_hold_status"] == "safe_fallback_not_progress"
    assert recommendation["exactly_one_recommendation"] is True
    assert recommendation["primary_recommendation"] == PRIMARY_RECOMMENDATION_NO_REAL_INPUT
    assert recommendation["hold_is_not_progress"] is True
    assert evidence["evidence_visible_without_drawer"] is True
    assert evidence["drawer_only_evidence"] is False
    assert len(evidence["visible_evidence_rows"]) >= 4
    assert source_index["source_records_secondary"] is True
    assert all(row["display_zone"] == "secondary_source_records" for row in source_index["source_records"])
    assert all(row["role"] == "secondary_source_record" for row in source_index["source_records"])
    assert metrics["split_view_structure_status"] == "passed_left_decision_rail_right_evidence_pane"
    assert metrics["gate_text_bounded"] is True
    assert metrics["card_grid_as_primary_structure"] is False
    assert metrics["primary_card_grid_count"] == 0
    assert metrics["internal_artifact_ids_in_left_primary_copy"] == []
    assert 'data-split-view="true"' in html
    assert 'data-left-primary-copy="true"' in html
    assert 'data-right-evidence-pane="true"' in html
    assert "Evidence preview" in html
    assert "Source readiness" in html
    assert "Recommendation rationale" in html
    assert "Bounded gate context" in html
    assert "Secondary source records" in html
    assert "Prepare verified local source or transcript material" in html
    assert "Hold remains safe fallback" in html
    assert "color-scheme: dark light" in html
    assert "prefers-color-scheme" in html
    assert "right evidence pane" in markdown.lower()

    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundary_flags"][flag] is True


def test_split_view_validation_catches_missing_html(tmp_path) -> None:
    output_dir = tmp_path / "split_view_decision_evidence_prototype"
    build_split_view_decision_evidence_prototype(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_split_view_decision_evidence",
    )
    (output_dir / "split_view_decision_evidence.html").unlink()

    readback = validate_split_view_decision_evidence_prototype(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:split_view_decision_evidence.html" in readback["failed_checks"]


def test_cli_build_split_view_decision_evidence_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_split_view_decision_evidence"

    code = main(
        [
            "build-split-view-decision-evidence-prototype",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_split_view_decision_evidence",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["selected_candidate"] == SELECTED_CANDIDATE
    assert payload["primary_recommendation"] == PRIMARY_RECOMMENDATION_NO_REAL_INPUT
    assert payload["fallback_hold_status"] == "safe_fallback_not_progress"
    assert payload["evidence_visible_without_drawer"] is True
    assert payload["source_records_secondary"] is True
    assert payload["gate_text_bounded"] is True
    assert payload["internal_artifact_ids_in_left_primary_copy"] == []
    assert payload["card_grid_as_primary_structure"] is False
    assert payload["split_view_structure_status"] == "passed_left_decision_rail_right_evidence_pane"
    assert payload["primary_human_review"].endswith("split_view_decision_evidence.html")
    assert payload["recommendation_readback"].endswith("recommendation_readback.json")
    assert payload["evidence_pane_readback"].endswith("evidence_pane_readback.json")
    assert payload["launcher_command"]


def test_generated_split_view_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "split_view_decision_evidence_prototype"
    build_split_view_decision_evidence_prototype(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_split_view_decision_evidence",
    )

    readback = _load(output_dir / "validation_readback.json")
    assert readback["checks"]["split_view_structure_present"] is True
    assert readback["checks"]["evidence_visible_without_drawer"] is True
    assert readback["checks"]["drawer_only_evidence"] is False
    assert readback["checks"]["hold_is_not_progress"] is True
    assert readback["checks"]["source_records_secondary"] is True
    assert readback["checks"]["external_dependency_status"] == "none_found"
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["temporary_copy_absent"] is True
    assert readback["checks"]["boundary_flags_present"] is True

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
