import json
import re
from pathlib import Path

from src.pipeline.newsroom_visual_density_simplification_spec import (
    DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_DOC_PATH,
    DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH,
    INFORMATION_DENSITY_BENCHMARK_SLICE,
    NEXT_DEFAULT_SLICE,
    SOURCE_BAND_SIMPLIFICATION_SLICE,
    VISUAL_DENSITY_SIMPLIFICATION_SPEC_ID,
    VISUAL_DENSITY_SIMPLIFICATION_SPEC_SCHEMA_VERSION,
    build_default_newsroom_visual_density_simplification_spec,
    render_newsroom_visual_density_simplification_spec_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH
SPEC_DOC_PATH = ROOT / DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_DOC_PATH


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_density_spec_json_matches_builder_and_identity() -> None:
    spec = _json(SPEC_PATH)

    assert spec == build_default_newsroom_visual_density_simplification_spec(
        root=ROOT
    )
    assert spec["spec_id"] == VISUAL_DENSITY_SIMPLIFICATION_SPEC_ID
    assert spec["schema_version"] == VISUAL_DENSITY_SIMPLIFICATION_SPEC_SCHEMA_VERSION
    assert spec["spec_status"] == "defined"
    assert spec["production_status"] == "diagnostic_only"
    assert spec["visual_work_class"] == "audience_fit"
    assert spec["actual_audience_acceptance_claimed"] is False
    assert spec["source_validation"]["status"] == "passed"
    assert spec["source_validation"]["errors"] == []
    assert spec["identity"]["source_density_gate_path"].endswith(
        "post_benchmarked_visual_observation_density_gate_v1.json"
    )


def test_problem_statement_density_budget_and_hard_constraints() -> None:
    spec = _json(SPEC_PATH)
    problem = spec["problem_statement"]
    budget = spec["density_budget"]
    constraints = spec["hard_constraints"]

    assert problem["mechanics_status_pass"] is True
    assert problem["visual_density_issue"] is True
    assert problem["cognitive_load_high"] is True
    assert problem["format_attention_over_content"] is True
    assert problem["text_fit_tight_warning"] is True
    assert problem["pacing_density_issue_for_68_sec_video"] is True
    assert problem["production_quality_accepted"] is False
    assert problem["public_video_ready"] is False

    assert budget["dominant_message_per_card"] == "exactly_one"
    assert budget["headline_budget"] == "maximum_1_headline"
    assert budget["primary_sentence_budget"] == "maximum_1_primary_sentence"
    assert budget["supporting_note_or_diagram_budget"] == "maximum_1"
    assert budget["meaningful_label_budget"] == "maximum_2_to_3_labels"
    assert budget["essential_meaning_in_tiny_metadata"] is False
    assert budget["debug_or_source_text_policy"] == (
        "shorten_demote_or_hide_from_main_viewing_path"
    )
    assert budget["subtitle_reserve_policy"] == "simple_and_non_competing"
    assert budget["minimum_meaningful_font_size_policy"] == "preserve_or_increase"

    assert constraints["do_not_reduce_minimum_meaningful_font_size"] is True
    assert constraints["do_not_solve_density_by_shrinking_text"] is True
    assert constraints["do_not_add_more_boxes_to_explain_existing_boxes"] is True
    assert constraints["do_not_introduce_real_brands_urls_or_real_news_visuals"] is True
    assert constraints["do_not_convert_cards_into_complex_yym4_object_graphs"] is True
    assert constraints["do_not_claim_production_visual_quality"] is True
    assert constraints["do_not_claim_audience_acceptance"] is True


def test_simplification_operations_and_card_diagnosis_are_bounded() -> None:
    spec = _json(SPEC_PATH)
    operations = {row["operation"] for row in spec["simplification_operations"]}
    diagnosis = {
        row["display_order"]: row
        for row in spec["card_specific_preliminary_diagnosis"]
    }

    assert operations == {
        "remove_nonessential_microcopy",
        "merge_repeated_labels",
        "demote_diagnostic_source_metadata",
        "replace_small_text_with_visual_markers",
        "increase_whitespace_around_essential_text",
        "split_overloaded_roles_only_if_necessary",
        "preserve_fake_review_boundary_with_fewer_labels",
        "preserve_card_role_variation",
    }
    assert len(diagnosis) == 4
    assert diagnosis[1]["essential_message_to_preserve"] == (
        "fake topic is review-only and the card is a plain point summary"
    )
    assert "secondary POINT mini panel" in diagnosis[1][
        "elements_that_can_be_removed_or_demoted"
    ]
    assert "three-step flow" in diagnosis[2]["elements_that_must_stay"]
    assert "RESULT box" in diagnosis[3]["elements_that_can_be_removed_or_demoted"]
    assert "source-check awareness" in diagnosis[4]["elements_that_must_stay"]
    assert all(row["implemented_in_this_slice"] is False for row in diagnosis.values())
    assert all(row["current_png_path"].endswith(".png") for row in diagnosis.values())


def test_evaluation_criteria_next_slices_and_matrices_match_prompt() -> None:
    spec = _json(SPEC_PATH)
    criteria = {
        row["criterion"]: row["target"]
        for row in spec["evaluation_criteria_for_next_refinement"]
    }
    next_slices = {row["slice"]: row for row in spec["recommended_next_slices"]}

    assert "dominant_message_visible_within_3_seconds" in criteria
    assert "no_more_than_one_primary_reading_path" in criteria
    assert "meaningful_text_fits_without_crowding" in criteria
    assert "source_subtitle_debug_area_does_not_compete" in criteria
    assert "surface_feels_simpler_than_previous_density_gate" in criteria

    assert spec["next_slice_recommendation"]["default_slice"] == NEXT_DEFAULT_SLICE
    assert next_slices[NEXT_DEFAULT_SLICE]["timing"] == "default_next"
    assert next_slices[INFORMATION_DENSITY_BENCHMARK_SLICE]["timing"] == (
        "only_if_current_spec_cannot_define_adequate_criteria"
    )
    assert next_slices[SOURCE_BAND_SIMPLIFICATION_SLICE]["timing"] == (
        "if_source_subtitle_band_is_dominant_actionable_issue"
    )
    assert len(spec["goal_stack"]) == 4
    assert len(spec["completion_matrix"]) == 6
    assert len(spec["artifact_readiness"]) == 6
    assert len(spec["visual_gate"]) == 8
    assert len(spec["render_gate_hygiene"]) == 6
    assert len(spec["human_burden_hygiene"]) == 7
    assert len(spec["review_non_redundancy"]) == 6
    assert len(spec["inertia_check"]) == 5


def test_doc_matches_renderer_and_preserves_unknown_not_accepted_scope() -> None:
    spec = _json(SPEC_PATH)
    doc_text = SPEC_DOC_PATH.read_text(encoding="utf-8")
    not_accepted = spec["not_accepted_scope"]

    assert doc_text == render_newsroom_visual_density_simplification_spec_markdown(
        spec
    )
    assert not_accepted["actual_target_audience_acceptance"] == "unknown"
    assert not_accepted["ctr_retention_prediction"] == "unknown"
    assert not_accepted["production_visual_quality"] is False
    assert not_accepted["final_design_system"] is False
    assert not_accepted["real_newsroom_visual_acceptance"] is False
    assert not_accepted["public_readiness"] is False
    assert not_accepted["production_approval"] is False
    assert spec["boundaries"]["card_redesign_performed"] is False
    assert spec["boundaries"]["svg_png_cards_regenerated"] is False
    assert "actual_audience_acceptance_claimed: True" not in doc_text
    assert "production_approval: True" not in doc_text
    assert "public_video_ready: True" not in doc_text
    assert _real_url_pattern().search(doc_text) is None
