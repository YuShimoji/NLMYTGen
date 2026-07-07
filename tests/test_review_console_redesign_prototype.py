from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.review_console_redesign_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
    PRIMARY_RECOMMENDATION_NO_REAL_INPUT,
    REQUIRED_LAYOUT_REGIONS,
    REQUIRED_REVIEW_CONSOLE_FILES,
    build_review_console_redesign_prototype,
    validate_review_console_redesign_prototype,
)
from src.pipeline.split_view_decision_evidence_prototype import REQUIRED_BOUNDARY_FLAGS


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_review_console_redesign_builds_compact_console_package(tmp_path) -> None:
    output_dir = tmp_path / "review_console_redesign_prototype"

    readback = build_review_console_redesign_prototype(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_review_console_redesign",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_REVIEW_CONSOLE_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "review_console_manifest.json")
    audit = _load(output_dir / "screen_audit.json")
    state = _load(output_dir / "console_state.json")
    inspector = _load(output_dir / "inspector_readback.json")
    drawer = _load(output_dir / "evidence_drawer_index.json")
    metrics = _load(output_dir / "layout_metrics.json")
    html = (output_dir / "review_console.html").read_text(encoding="utf-8")
    self_review = (output_dir / "visual_self_review.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-review-console-redesign-prototype"
    assert manifest["status"] == "review_console_ready_local_offline"
    assert audit["primary_decision"] == state["primary_decision"]
    assert audit["primary_artifact"] == state["primary_artifact"]
    assert "raw artifact paths" in audit["noise"]
    assert state["primary_recommendation"] == PRIMARY_RECOMMENDATION_NO_REAL_INPUT
    assert state["fallback_hold_status"] == "safe_fallback_not_progress"
    assert state["hold_is_not_progress"] is True
    assert inspector["primary_recommendation"] == PRIMARY_RECOMMENDATION_NO_REAL_INPUT
    assert inspector["hold_is_not_progress"] is True
    assert len(
        [
            row
            for row in inspector["operational_controls"]
            if row["recommended_for_current_state"] is True
        ]
    ) == 1
    assert drawer["evidence_visible_outside_drawer"] is True
    assert drawer["drawer_only_evidence"] is False
    assert drawer["source_records_secondary"] is True
    assert drawer["detail_drawer_role"] == "secondary_raw_records_and_source_paths"
    assert metrics["initial_visible_text_reduction_passed"] is True
    assert metrics["initial_visible_text_reduction_percent"] >= 50
    assert metrics["same_shape_card_grid_primary"] is False
    assert metrics["gate_text_bounded"] is True
    assert metrics["source_records_secondary"] is True
    assert 'data-review-console="true"' in html
    assert 'data-initial-visible-copy="true"' in html
    assert 'data-evidence-visible-outside-drawer="true"' in html
    assert 'data-same-shape-grid-primary="false"' in html
    assert "class=\"card" not in html.lower()
    assert "card-grid" not in html.lower()
    for region in REQUIRED_LAYOUT_REGIONS:
        assert f'data-region="{region}"' in html
    assert "color-scheme: dark light" in html
    assert "prefers-color-scheme" in html
    assert "Review console Visual Self-Review".lower() in self_review.lower()

    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundary_flags"][flag] is True


def test_review_console_validation_catches_missing_html(tmp_path) -> None:
    output_dir = tmp_path / "review_console_redesign_prototype"
    build_review_console_redesign_prototype(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_review_console_redesign",
    )
    (output_dir / "review_console.html").unlink()

    readback = validate_review_console_redesign_prototype(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:review_console.html" in readback["failed_checks"]


def test_cli_build_review_console_redesign_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_review_console_redesign"

    code = main(
        [
            "build-review-console-redesign-prototype",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_review_console_redesign",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["primary_review_file"].endswith("review_console.html")
    assert payload["primary_recommendation"] == PRIMARY_RECOMMENDATION_NO_REAL_INPUT
    assert payload["same_shape_card_grid_primary"] is False
    assert payload["evidence_visible_outside_drawer"] is True
    assert payload["detail_drawer_role"] == "secondary_raw_records_and_source_paths"
    assert payload["gate_text_bounded"] is True
    assert payload["source_records_secondary"] is True
    assert payload["internal_artifact_ids_in_primary_copy"] == []
    assert "reduction" in payload["initial_visible_text_reduction"]
    assert payload["launcher_or_open_command"]


def test_review_console_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "review_console_redesign_prototype"
    build_review_console_redesign_prototype(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_review_console_redesign",
    )

    readback = _load(output_dir / "validation_readback.json")
    assert readback["status"] == "passed"
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
