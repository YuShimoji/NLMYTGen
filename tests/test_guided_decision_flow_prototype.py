from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.guided_decision_flow_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
    REQUIRED_BOUNDARY_FLAGS,
    REQUIRED_GUIDED_DECISION_FILES,
    build_guided_decision_flow_prototype,
    validate_guided_decision_flow_prototype,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_guided_decision_flow_builds_one_recommendation_from_user_situation(tmp_path) -> None:
    output_dir = tmp_path / "guided_decision_flow_prototype"

    readback = build_guided_decision_flow_prototype(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_guided_decision_flow",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_GUIDED_DECISION_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "guided_flow_manifest.json")
    state = _load(output_dir / "flow_state.json")
    outcomes = _load(output_dir / "decision_outcomes.json")
    recommendation = _load(output_dir / "recommendation_engine_readback.json")
    evidence = _load(output_dir / "evidence_drawer_index.json")
    html = (output_dir / "guided_decision_flow.html").read_text(encoding="utf-8")
    markdown = (output_dir / "guided_decision_flow.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-guided-decision-flow-prototype"
    assert manifest["status"] == "guided_decision_flow_prototype_ready_local_offline"
    assert manifest["selected_candidate"] == "candidate_b_guided_decision_flow"
    assert state["primary_user_question"] == "What situation are you in right now?"
    assert state["real_input_available"] is False
    assert state["explicit_yymm4_observation_selected"] is False
    assert state["default_recommendation"] == "hold_review_later"
    assert outcomes["recommended_outcome_ids"] == ["hold_review_later"]
    assert recommendation["exactly_one_recommendation"] is True
    assert recommendation["default_recommendation"] == "hold_review_later"
    assert evidence["source_record_policy"] == "secondary_records_only"
    assert all(row["display_zone"] == "evidence_drawer" for row in evidence["source_records"])
    assert all(row["role"] == "secondary_source_record" for row in evidence["source_records"])
    assert "What situation are you in right now?" in html
    assert "Hold and review later" in html
    assert "Source records stay secondary" in markdown
    assert "data-secondary-records" in html
    assert "color-scheme: dark light" in html
    assert "prefers-color-scheme" in html

    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundary_flags"][flag] is True
        assert flag in html


def test_guided_decision_flow_validation_catches_missing_html(tmp_path) -> None:
    output_dir = tmp_path / "guided_decision_flow_prototype"
    build_guided_decision_flow_prototype(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_guided_decision_flow",
    )
    (output_dir / "guided_decision_flow.html").unlink()

    readback = validate_guided_decision_flow_prototype(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:guided_decision_flow.html" in readback["failed_checks"]


def test_cli_build_guided_decision_flow_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_guided_decision_flow"

    code = main(
        [
            "build-guided-decision-flow-prototype",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_guided_decision_flow",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["default_recommendation"] == "hold_review_later"
    assert payload["exactly_one_recommendation"] is True
    assert payload["source_records_secondary"] is True
    assert payload["checks"]["internal_artifact_ids_in_primary_copy"] == []
    assert payload["checks"]["external_dependency_status"] == "none_found"
    assert payload["primary_human_review"].endswith("guided_decision_flow.html")
    assert payload["recommendation_engine_readback"].endswith("recommendation_engine_readback.json")
    assert payload["launcher_command"]


def test_generated_guided_decision_flow_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "guided_decision_flow_prototype"
    build_guided_decision_flow_prototype(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_guided_decision_flow",
    )

    readback = _load(output_dir / "validation_readback.json")
    assert readback["checks"]["internal_artifact_ids_in_primary_copy"] == []
    assert readback["checks"]["source_records_secondary"] is True
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["temporary_copy_absent"] is True
    assert readback["gate_integrity_status"] == "closed_preserved"

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
