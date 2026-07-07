from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.primary_artifact_review_console import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
    PRIMARY_RECOMMENDATION_NO_REAL_INPUT,
    REQUIRED_LAYOUT_REGIONS,
    REQUIRED_PRIMARY_ARTIFACT_FILES,
    build_primary_artifact_review_console,
    validate_primary_artifact_review_console,
)
from src.pipeline.split_view_decision_evidence_prototype import REQUIRED_BOUNDARY_FLAGS


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_primary_artifact_review_console_builds_artifact_first_package(tmp_path) -> None:
    output_dir = tmp_path / "primary_artifact_review_console"

    readback = build_primary_artifact_review_console(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_primary_artifact_review_console",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_PRIMARY_ARTIFACT_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "primary_artifact_console_manifest.json")
    audit = _load(output_dir / "screen_audit.json")
    primary_artifact = _load(output_dir / "primary_artifact_readback.json")
    comparison = _load(output_dir / "visual_comparison_readback.json")
    inspector = _load(output_dir / "inspector_readback.json")
    drawer = _load(output_dir / "evidence_drawer_index.json")
    metrics = _load(output_dir / "layout_metrics.json")
    html = (output_dir / "primary_artifact_review_console.html").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-primary-artifact-review-console"
    assert manifest["status"] == "primary_artifact_console_ready_local_offline"
    assert audit["primary_decision"] == manifest["primary_decision"]
    assert audit["primary_artifact"] == manifest["primary_artifact"]
    assert "50.1% metric as the largest center object" in audit["noise"]
    assert primary_artifact["primary_artifact_dominant"] is True
    assert primary_artifact["primary_artifact_type"] == "html_rendered_visual_comparison_canvas"
    assert primary_artifact["metric_as_primary_focus"] is False
    assert comparison["html_rendered_visual_canvas"] is True
    assert comparison["before_after_representation"] == "single_visual_comparison_canvas"
    assert comparison["before_after_as_text_cards"] is False
    assert inspector["primary_recommendation"] == PRIMARY_RECOMMENDATION_NO_REAL_INPUT
    assert inspector["hold_is_not_progress"] is True
    assert len(
        [
            row
            for row in inspector["operational_controls"]
            if row["recommended_for_current_state"] is True
        ]
    ) == 1
    assert drawer["evidence_front_stage_card_row"] is False
    assert drawer["evidence_visible_outside_drawer"] is True
    assert drawer["source_records_secondary"] is True
    assert metrics["main_surface_type"] == "visual_comparison_canvas"
    assert metrics["before_after_representation"] == "single_visual_comparison_canvas"
    assert metrics["metric_as_primary_focus"] is False
    assert metrics["same_shape_card_grid_primary"] is False
    assert metrics["explanatory_cards_in_main_surface"] == 0
    assert metrics["evidence_front_stage_card_row"] is False
    assert metrics["gate_text_bounded"] is True
    assert 'data-primary-artifact-console="true"' in html
    assert 'data-primary-artifact-container="true"' in html
    assert 'data-main-surface-type="visual-comparison-canvas"' in html
    assert 'data-before-after-representation="single-visual-comparison"' in html
    assert 'data-metric-primary-focus="false"' in html
    assert 'data-evidence-front-stage-row="false"' in html
    assert "50.1%" not in html
    assert "class=\"card" not in html.lower()
    assert "evidence-chip" not in html.lower()
    for region in REQUIRED_LAYOUT_REGIONS:
        assert f'data-region="{region}"' in html

    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundary_flags"][flag] is True


def test_primary_artifact_validation_catches_missing_html(tmp_path) -> None:
    output_dir = tmp_path / "primary_artifact_review_console"
    build_primary_artifact_review_console(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_primary_artifact_review_console",
    )
    (output_dir / "primary_artifact_review_console.html").unlink()

    readback = validate_primary_artifact_review_console(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:primary_artifact_review_console.html" in readback["failed_checks"]


def test_cli_build_primary_artifact_review_console_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_primary_artifact_review_console"

    code = main(
        [
            "build-primary-artifact-review-console",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_primary_artifact_review_console",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["primary_review_file"].endswith("primary_artifact_review_console.html")
    assert payload["primary_recommendation"] == PRIMARY_RECOMMENDATION_NO_REAL_INPUT
    assert payload["main_surface_type"] == "visual_comparison_canvas"
    assert payload["before_after_representation"] == "single_visual_comparison_canvas"
    assert payload["metric_as_primary_focus"] is False
    assert payload["same_shape_card_grid_primary"] is False
    assert payload["explanatory_cards_in_main_surface"] == 0
    assert payload["evidence_front_stage_card_row"] is False
    assert payload["evidence_visible_outside_drawer"] is True
    assert payload["detail_drawer_role"] == "secondary_raw_records_source_paths_and_extended_proof"
    assert payload["source_records_secondary"] is True
    assert payload["internal_artifact_ids_in_primary_copy"] == []
    assert payload["launcher_or_open_command"]


def test_primary_artifact_console_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "primary_artifact_review_console"
    build_primary_artifact_review_console(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_primary_artifact_review_console",
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
