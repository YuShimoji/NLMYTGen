import json
import re
from pathlib import Path

from src.pipeline.newsroom_post_benchmarked_visual_observation_density_gate import (
    ALTERNATIVE_NEXT_AXIS,
    DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_DOC_PATH,
    DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH,
    FOLLOW_ON_REFINEMENT_SLICE,
    NORMALIZED_NEXT_AXIS,
    POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_ID,
    POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_SCHEMA_VERSION,
    RECOMMENDED_NEXT_AXIS,
    build_default_newsroom_post_benchmarked_visual_observation_density_gate,
    render_newsroom_post_benchmarked_visual_observation_density_gate_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH
GATE_DOC_PATH = (
    ROOT / DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_DOC_PATH
)


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_density_gate_json_matches_builder_and_identity() -> None:
    gate = _json(GATE_PATH)

    assert gate == (
        build_default_newsroom_post_benchmarked_visual_observation_density_gate(
            root=ROOT
        )
    )
    assert gate["readback_id"] == POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_ID
    assert gate["schema_version"] == (
        POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_SCHEMA_VERSION
    )
    assert gate["observation_status"] == "visual_density_issue_confirmed"
    assert gate["mechanics_status"] == "pass"
    assert gate["production_status"] == "diagnostic_only"
    assert gate["visual_work_class"] == "audience_fit"
    assert gate["observation_source"] == "user_freeform_with_screenshot_support"
    assert gate["audience_acceptance_claimed"] is False
    assert gate["production_visual_quality_accepted"] is False
    assert gate["public_video_ready"] is False
    assert gate["source_validation"]["status"] == "passed"
    assert gate["source_validation"]["errors"] == []


def test_mechanics_preservation_and_visual_findings_are_normalized() -> None:
    gate = _json(GATE_PATH)
    mechanics = gate["mechanics_preservation"]
    findings = gate["visual_findings"]

    assert gate["card_assets_visible"] is True
    assert gate["native_audio_present"] is True
    assert gate["dialogue_item_count_preserved"] is True
    assert mechanics["card_assets_visible"] is True
    assert mechanics["native_audio_present"] is True
    assert mechanics["dialogue_items_preserved"] is True
    assert mechanics["timing_or_duration_regression_reported"] is False
    assert mechanics["render_or_preview_context"] == "user_observed_YMM4_surface"
    assert mechanics["production_ready"] is False
    assert gate["screenshot_support"]["count"] == 4

    assert gate["rendered_line_count_mismatch_warning"] is True
    assert gate["text_fit_tight_warning"] is True
    assert gate["source_or_small_text_tightness_warning"] is True
    assert gate["manual_edit_quality_minor_issue"] is True
    assert gate["format_attention_over_content"] is True
    assert gate["bbc_like_surface_signal"] is True
    assert gate["information_density_high"] is True
    assert gate["cognitive_load_high"] is True
    assert findings["not_a_local_clipping_only_issue"] is True


def test_benchmark_impact_and_next_axis_preserve_gate_boundary() -> None:
    gate = _json(GATE_PATH)
    impact = gate["benchmark_impact"]
    decision = gate["decision"]

    assert impact["readability_at_a_glance"]["result"] == "warning"
    assert impact["text_clipping_or_wrapping"]["result"] == "improved_but_tight"
    assert impact["no_reliance_on_tiny_metadata"]["result"] == "warning"
    assert impact["pacing_density_for_68_sec_video"]["result"] == "fail"
    assert impact["familiar_explainer_visual_grammar"]["result"] == "mixed"
    assert impact["one_dominant_message_per_card"]["result"] == "warning"
    assert impact["actual_audience_acceptance"]["result"] == "unknown"

    assert gate["recommended_next_axis"] == NORMALIZED_NEXT_AXIS
    assert decision["recommended_next_axis"] == RECOMMENDED_NEXT_AXIS
    assert decision["alternative_next_axis"] == ALTERNATIVE_NEXT_AXIS
    assert decision["follow_on_refinement_slice"] == FOLLOW_ON_REFINEMENT_SLICE
    assert decision["redesign_now"] is False
    assert decision["render_now"] is False


def test_matrices_and_next_slices_match_prompt_gate_totals() -> None:
    gate = _json(GATE_PATH)
    next_slices = {row["slice"]: row for row in gate["recommended_next_slices"]}

    assert gate["recommended_next_slice"]["slice"] == RECOMMENDED_NEXT_AXIS
    assert next_slices[RECOMMENDED_NEXT_AXIS]["timing"] == "default_next"
    assert (
        next_slices[ALTERNATIVE_NEXT_AXIS]["timing"]
        == "if_existing_benchmark_density_criteria_are_insufficient"
    )
    assert next_slices[FOLLOW_ON_REFINEMENT_SLICE]["timing"] == (
        "after_density_spec_or_sufficient_existing_criteria"
    )
    assert len(gate["goal_stack"]) == 4
    assert len(gate["completion_matrix"]) == 6
    assert len(gate["artifact_readiness"]) == 6
    assert len(gate["visual_gate"]) == 8
    assert len(gate["render_gate_hygiene"]) == 6
    assert len(gate["human_burden_hygiene"]) == 7
    assert len(gate["review_non_redundancy"]) == 6
    assert len(gate["inertia_check"]) == 5
    assert gate["not_accepted_scope"]["actual_audience_acceptance"] is False
    assert gate["boundaries"]["YMM4_launched_by_agent"] is False
    assert gate["boundaries"]["svg_png_cards_regenerated"] is False


def test_doc_matches_renderer_and_avoids_url_or_acceptance_claims() -> None:
    gate = _json(GATE_PATH)
    doc_text = GATE_DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == (
        render_newsroom_post_benchmarked_visual_observation_density_gate_markdown(
            gate
        )
    )
    assert "actual_audience_acceptance: True" not in doc_text
    assert "audience_acceptance_claimed: True" not in doc_text
    assert "production_approval: True" not in doc_text
    assert "public_video_ready: True" not in doc_text
    assert "render_now: True" not in doc_text
    assert "redesign_now: True" not in doc_text
    assert _real_url_pattern().search(doc_text) is None
