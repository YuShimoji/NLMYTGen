import json
import re
from pathlib import Path

from src.pipeline.newsroom_post_density_refinement_render_smoke_result_readback import (
    DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_DOC_PATH,
    DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_PATH,
    NEXT_DEFAULT_SLICE,
    POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_ID,
    POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION,
    build_default_newsroom_post_density_refinement_render_smoke_result_readback,
    render_newsroom_post_density_refinement_render_smoke_result_readback_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
READBACK_PATH = (
    ROOT / DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
)
DOC_PATH = (
    ROOT / DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_DOC_PATH
)


def _readback() -> dict:
    return json.loads(READBACK_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_readback_matches_builder_output_and_identity() -> None:
    readback = _readback()

    assert readback == (
        build_default_newsroom_post_density_refinement_render_smoke_result_readback(
            root=ROOT
        )
    )
    assert readback["artifact_id"] == (
        POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_ID
    )
    assert readback["readback_id"] == (
        POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_ID
    )
    assert readback["schema_version"] == (
        POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION
    )
    assert readback["review_status"] == "ready_for_supervisor_review"
    assert readback["production_status"] == "diagnostic_only"
    assert readback["visual_work_class"] == "audience_fit"
    assert readback["observation_source"] == (
        "user_freeform_with_screenshot_support"
    )
    assert readback["result_status"] == "pass"
    assert readback["actual_audience_acceptance_claimed"] is False


def test_source_validation_reuses_density_refinement_without_regenerating_cards() -> None:
    validation = _readback()["source_validation"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["source_density_refinement_status"] == (
        "density_benchmark_materially_improved"
    )
    assert validation["source_density_proxy_status"] == "materially_improved"
    assert validation["source_density_proxy_fail_count"] == 0
    assert validation["source_png_export_status"] == "generated"
    assert validation["source_density_gate_status"] == (
        "visual_density_issue_confirmed"
    )
    assert validation["source_card_count"] == 4
    assert validation["card_assets_exist"] is True
    assert validation["svg_png_cards_regenerated_in_this_slice"] is False


def test_normalized_render_observation_records_post_density_pass() -> None:
    observation = _readback()["normalized_render_observation"]

    assert observation == {
        "render_smoke_result": "pass",
        "yym4_opened_card_placement_project": True,
        "render_completed": True,
        "output_duration_observed": "approximately_68_sec",
        "duration_matches_timing_patch": True,
        "card_assets_visible": True,
        "card_count_visible": 4,
        "density_refinement_visible": True,
        "information_density_reduced": True,
        "dialogue_items_preserved": True,
        "rendered_line_count_mismatch_warning": "possible_due_to_wrapping",
        "native_audio_present": True,
        "visual_card_integrity": "pass",
        "timing_preservation_regression_reported": False,
        "audio_regression_reported": False,
        "production_visual_quality_accepted": False,
        "actual_audience_acceptance_claimed": False,
        "public_video_ready": False,
    }


def test_card_observations_cover_four_density_simplified_cards() -> None:
    rows = _readback()["screenshot_supported_card_observations"]

    assert len(rows) == 4
    assert [row["card_index"] for row in rows] == [1, 2, 3, 4]
    assert all(row["visible_status"] is True for row in rows)
    assert all(row["density_simplification_visible"] is True for row in rows)
    assert all(row["dominant_message_visible"] is True for row in rows)
    assert all(row["clutter_reduced"] is True for row in rows)
    assert all(
        row["notes"]
        == [
            "diagnostic/review-only card",
            "no audience acceptance claim",
        ]
        for row in rows
    )


def test_scope_readiness_render_gate_and_next_axis_are_separated() -> None:
    readback = _readback()
    accepted = readback["accepted_scope"]
    not_accepted = readback["not_accepted_scope"]
    readiness = readback["readiness_separation"]
    gate = readback["render_gate_carry_forward"]

    assert accepted["post_density_refinement_cards_render_visibly_in_yym4_surface"]
    assert accepted["duration_remains_approximately_68_sec"]
    assert accepted["four_card_assets_remain_visible"]
    assert accepted["dialogue_and_native_audio_are_preserved"]
    assert accepted["information_density_materially_improved_at_diagnostic_level"]
    assert accepted["ready_to_return_to_internal_review_v0_1_reevaluation"]
    assert not_accepted == {
        "actual_youtube_audience_acceptance": False,
        "ctr_retention_prediction": False,
        "production_visual_quality": False,
        "final_design_system": False,
        "final_narration_script_density": False,
        "public_video_readiness": False,
        "real_newsroom_visual_acceptance": False,
        "production_approval": False,
    }
    assert readiness["slice_completion"] == "pass_for_this_readback"
    assert readiness["video_readiness_progress"] == "6/7"
    assert readiness["visual_density_readiness"] == "diagnostic_pass"
    assert readiness["production_readiness"] == "low_diagnostic_only"
    assert readiness["recommended_next_axis"] == NEXT_DEFAULT_SLICE
    assert gate["current_user_render_observation_consumed_once"] is True
    assert gate["new_render_in_this_slice"] is False
    assert gate["YMM4_launched_by_agent"] is False
    assert gate["card_assets_regenerated_in_this_slice"] is False


def test_matrices_match_contract_counts_and_next_default() -> None:
    readback = _readback()

    assert [row["slice"] for row in readback["recommended_next_slices"]] == [
        NEXT_DEFAULT_SLICE,
        "newsroom-visual-density-reduction-v2",
        "newsroom-rss-dry-run-integration-plan-v1",
        "newsroom-render-output-retention-policy-v1",
    ]
    assert readback["recommended_next_slices"][0]["timing"] == (
        "recommended_next_default"
    )
    assert len(readback["completion_matrix"]) == 6
    assert len(readback["artifact_readiness"]) == 6
    assert len(readback["visual_density_gate"]) == 8
    assert len(readback["render_gate_hygiene"]) == 6
    assert len(readback["human_burden_hygiene"]) == 7
    assert len(readback["review_non_redundancy"]) == 6
    assert len(readback["inertia_check"]) == 5
    assert readback["inertia_check"][-1] == {
        "gate": "next_concrete_review_milestone",
        "status": NEXT_DEFAULT_SLICE,
    }


def test_doc_matches_renderer_and_avoids_real_url_or_positive_claims() -> None:
    readback = _readback()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == (
        render_newsroom_post_density_refinement_render_smoke_result_readback_markdown(
            readback
        )
    )
    combined = (
        READBACK_PATH.read_text(encoding="utf-8") + "\n" + doc_text
    ).replace("http://www.w3.org/2000/svg", "")
    assert not _real_url_pattern().search(combined)
    assert "actual_audience_acceptance_claimed: true" not in combined
    assert '"actual_audience_acceptance_claimed": true' not in combined
    assert "production_approval: true" not in combined
    assert '"production_approval": true' not in combined
    assert "public_video_ready: true" not in combined
    assert '"public_video_ready": true' not in combined
    assert " ".join(["fixed", "form", "required"]) not in combined.lower()
    assert " ".join(["render", "again"]) not in combined.lower()
