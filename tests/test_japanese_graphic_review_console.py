from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.japanese_graphic_review_console import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
    GRAPHICAL_ELEMENTS,
    PRIMARY_RECOMMENDATION_NO_REAL_INPUT,
    REQUIRED_JAPANESE_GRAPHIC_FILES,
    REQUIRED_LAYOUT_REGIONS,
    build_japanese_graphic_review_console,
    validate_japanese_graphic_review_console,
)
from src.pipeline.split_view_decision_evidence_prototype import REQUIRED_BOUNDARY_FLAGS


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _lane_map(tmp_path: Path) -> Path:
    path = tmp_path / "PROJECT_LANES.md"
    path.write_text(
        "\n".join(
            [
                "# Project Lanes",
                "",
                "- Output / Video Layer",
                "- Input / API Hub",
                "- GUI / IA / i18n",
                "- Integrity / Triage",
                "- Editing / YMM4 Feature Design",
                "- Deep Research",
                "",
                "After the Japanese graphical console is reviewable, return to the product lane unless the user rejects the UI direction.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path


def test_japanese_graphic_review_console_builds_japanese_graphic_package(tmp_path) -> None:
    output_dir = tmp_path / "japanese_graphic_review_console"

    readback = build_japanese_graphic_review_console(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        lane_map_path=_lane_map(tmp_path),
        artifact_id="test_japanese_graphic_review_console",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_JAPANESE_GRAPHIC_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "japanese_graphic_console_manifest.json")
    audit = _load(output_dir / "screen_audit.json")
    graphic = _load(output_dir / "graphic_surface_readback.json")
    japanese_copy = _load(output_dir / "japanese_copy_readback.json")
    inspector = _load(output_dir / "inspector_readback.json")
    drawer = _load(output_dir / "evidence_drawer_index.json")
    metrics = _load(output_dir / "layout_metrics.json")
    html = (output_dir / "japanese_graphic_review_console.html").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-japanese-graphic-review-console"
    assert manifest["status"] == "japanese_graphic_console_ready_local_offline"
    assert manifest["project_lanes_recorded"] is True
    assert manifest["stop_rule_recorded"] is True
    assert audit["primary_decision"] == manifest["primary_decision"]
    assert audit["primary_artifact"] == manifest["primary_artifact"]
    assert "English-first primary labels" in audit["noise"]
    assert graphic["primary_artifact_dominant"] is True
    assert graphic["center_not_text_cards"] is True
    assert graphic["main_surface_type"] == "japanese_graphical_flow_spine"
    assert set(GRAPHICAL_ELEMENTS).issubset(set(graphic["graphical_elements"]))
    assert japanese_copy["primary_ui_language"] == "ja"
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
    assert metrics["main_surface_type"] == "japanese_graphical_flow_spine"
    assert metrics["primary_ui_language"] == "ja"
    assert metrics["same_shape_card_grid_primary"] is False
    assert metrics["explanatory_cards_in_main_surface"] == 0
    assert metrics["evidence_front_stage_card_row"] is False
    assert metrics["free_text_role"] == "secondary_handoff_note"
    assert metrics["gate_text_bounded"] is True
    assert '<html lang="ja"' in html
    assert 'data-japanese-graphic-console="true"' in html
    assert 'data-primary-ui-language="ja"' in html
    assert 'data-main-surface-type="japanese-graphic-flow-spine"' in html
    assert 'data-free-text-role="secondary_handoff_note"' in html
    assert 'data-evidence-front-stage-row="false"' in html
    assert "Primary Decision" not in html
    assert "Evidence Drawer" not in html
    assert "Main Review Surface" not in html
    assert "class=\"card" not in html.lower()
    for region in REQUIRED_LAYOUT_REGIONS:
        assert f'data-region="{region}"' in html

    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert manifest["boundary_flags"][flag] is True


def test_japanese_graphic_validation_catches_missing_html(tmp_path) -> None:
    output_dir = tmp_path / "japanese_graphic_review_console"
    build_japanese_graphic_review_console(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        lane_map_path=_lane_map(tmp_path),
        artifact_id="test_japanese_graphic_review_console",
    )
    (output_dir / "japanese_graphic_review_console.html").unlink()

    readback = validate_japanese_graphic_review_console(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:japanese_graphic_review_console.html" in readback["failed_checks"]


def test_cli_build_japanese_graphic_review_console_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_japanese_graphic_review_console"

    code = main(
        [
            "build-japanese-graphic-review-console",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--lane-map-path",
            str(_lane_map(tmp_path)),
            "--artifact-id",
            "test_cli_japanese_graphic_review_console",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["primary_review_file"].endswith("japanese_graphic_review_console.html")
    assert payload["primary_recommendation"] == PRIMARY_RECOMMENDATION_NO_REAL_INPUT
    assert payload["main_surface_type"] == "japanese_graphical_flow_spine"
    assert set(GRAPHICAL_ELEMENTS).issubset(set(payload["graphical_elements"]))
    assert payload["primary_ui_language"] == "ja"
    assert payload["english_primary_headings"] == []
    assert payload["free_text_role"] == "secondary_handoff_note"
    assert payload["same_shape_card_grid_primary"] is False
    assert payload["explanatory_cards_in_main_surface"] == 0
    assert payload["evidence_front_stage_card_row"] is False
    assert payload["evidence_visible_outside_drawer"] is True
    assert payload["project_lanes_recorded"] is True
    assert payload["stop_rule_recorded"] is True
    assert payload["source_records_secondary"] is True
    assert payload["internal_artifact_ids_in_primary_copy"] == []
    assert payload["launcher_or_open_command"]


def test_japanese_graphic_console_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "japanese_graphic_review_console"
    build_japanese_graphic_review_console(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        lane_map_path=_lane_map(tmp_path),
        artifact_id="test_japanese_graphic_review_console",
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
