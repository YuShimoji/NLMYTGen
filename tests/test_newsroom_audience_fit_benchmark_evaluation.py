import json
import re
from pathlib import Path

from src.pipeline.newsroom_audience_fit_benchmark_evaluation import (
    AUDIENCE_FIT_BENCHMARK_EVALUATION_ID,
    AUDIENCE_FIT_BENCHMARK_EVALUATION_SCHEMA_VERSION,
    DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_DOC_PATH,
    DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH,
    NEXT_REFINEMENT_SLICE,
    build_default_newsroom_audience_fit_benchmark_evaluation,
    render_newsroom_audience_fit_benchmark_evaluation_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
EVALUATION_PATH = ROOT / DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH
DOC_PATH = ROOT / DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_DOC_PATH


def _evaluation() -> dict:
    return json.loads(EVALUATION_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_evaluation_json_matches_builder_output_and_identity() -> None:
    evaluation = _evaluation()

    assert evaluation == build_default_newsroom_audience_fit_benchmark_evaluation(
        root=ROOT
    )
    assert evaluation["artifact_id"] == AUDIENCE_FIT_BENCHMARK_EVALUATION_ID
    assert evaluation["evaluation_id"] == AUDIENCE_FIT_BENCHMARK_EVALUATION_ID
    assert evaluation["schema_version"] == (
        AUDIENCE_FIT_BENCHMARK_EVALUATION_SCHEMA_VERSION
    )
    assert evaluation["benchmark_status"] == "applied"
    assert evaluation["evaluation_status"] == "material_proxy_failures_found"
    assert evaluation["production_status"] == "diagnostic_only"
    assert evaluation["visual_work_class"] == "audience_fit"
    assert evaluation["audience_acceptance_claimed"] is False


def test_source_validation_and_card_inventory_cover_current_four_cards() -> None:
    evaluation = _evaluation()
    validation = evaluation["source_validation"]
    cards = evaluation["evaluated_card_inventory"]

    assert validation == {
        "status": "passed",
        "errors": [],
        "source_benchmark_status": "draft_proxy_benchmark_defined",
        "source_refinement_status": "assets_regenerated",
        "source_render_readback_status": "pass",
        "card_count": 4,
    }
    assert [card["card_id"] for card in cards] == [
        "visual_card_cap_beat_fake_intro_001_01_v1",
        "visual_card_cap_beat_fake_intro_001_02_v1",
        "visual_card_cap_beat_fake_claim_001_01_v1",
        "visual_card_cap_beat_fake_claim_001_02_v1",
    ]
    assert [card["evaluation_status"] for card in cards] == [
        "warning",
        "warning",
        "fail",
        "fail",
    ]
    assert all(card["svg_exists"] is True for card in cards)
    assert all(card["png_exists"] is True for card in cards)
    assert all(card["png_size"] == {"width": 1920, "height": 1080} for card in cards)
    assert all(card["min_font_size"] >= 34 for card in cards)
    assert all(card["review_only_visible"] is True for card in cards)
    assert all(card["diagnostic_visible"] is True for card in cards)
    assert all(card["subtitle_area_visible"] is True for card in cards)
    assert all(card["real_url_or_www_in_svg_text"] is False for card in cards)


def test_proxy_metric_results_select_benchmarked_refinement() -> None:
    evaluation = _evaluation()
    metrics = evaluation["proxy_metric_evaluation"]
    results = {row["metric_id"]: row for row in metrics}

    assert [row["metric_id"] for row in metrics] == [
        "readability_at_a_glance",
        "text_clipping_or_wrapping",
        "minimum_meaningful_font_size",
        "one_dominant_message_per_card",
        "familiar_explainer_visual_grammar",
        "no_reliance_on_tiny_metadata",
        "card_role_variation",
        "pacing_density_for_68_sec_video",
        "diagnostic_boundary_visibility",
        "no_real_brand_url_public_claim",
    ]
    assert results["text_clipping_or_wrapping"]["result"] == "fail"
    assert results["text_clipping_or_wrapping"]["affected_cards"] == [
        "visual_card_cap_beat_fake_intro_001_01_v1",
        "visual_card_cap_beat_fake_intro_001_02_v1",
        "visual_card_cap_beat_fake_claim_001_01_v1",
        "visual_card_cap_beat_fake_claim_001_02_v1",
    ]
    assert results["minimum_meaningful_font_size"]["result"] == "pass"
    assert results["one_dominant_message_per_card"]["result"] == "pass"
    assert results["familiar_explainer_visual_grammar"]["result"] == "warning"
    assert results["no_reliance_on_tiny_metadata"]["result"] == "warning"
    assert results["diagnostic_boundary_visibility"]["result"] == "pass"
    assert results["no_real_brand_url_public_claim"]["result"] == "pass"


def test_summary_unknowns_and_not_accepted_scope_preserve_boundaries() -> None:
    evaluation = _evaluation()
    summary = evaluation["evaluation_summary"]

    assert summary == {
        "benchmark_status": "applied",
        "card_count_evaluated": 4,
        "pass_count": 5,
        "warning_count": 4,
        "fail_count": 1,
        "unknown_count": 0,
        "next_iteration_allowed": True,
        "benchmark_failures_justifying_iteration": ["text_clipping_or_wrapping"],
        "benchmark_warnings_to_consider": [
            "readability_at_a_glance",
            "familiar_explainer_visual_grammar",
            "no_reliance_on_tiny_metadata",
            "pacing_density_for_68_sec_video",
        ],
    }
    assert evaluation["unknowns_preserved"] == [
        "actual target viewer preference",
        "CTR / retention",
        "target viewer comprehension outside this project",
        "production visual quality",
        "real newsroom visual acceptance",
    ]
    assert all(value is False for value in evaluation["not_accepted_scope"].values())
    assert all(value is False for value in evaluation["boundaries"].values())


def test_recommendation_and_downstream_use_are_benchmark_linked() -> None:
    evaluation = _evaluation()
    recommendation = evaluation["recommendation"]
    downstream = evaluation["downstream_next_use"]

    assert recommendation["selected_next_slice"] == NEXT_REFINEMENT_SLICE
    assert "text clipping/wrapping" in recommendation["reason"]
    assert [row["slice"] for row in recommendation["not_selected"]] == [
        "newsroom-reference-pack-visual-grammar-v1",
        "newsroom-internal-review-v0.1-operator-review-card",
        "newsroom-post-audience-fit-render-smoke-result-readback-v1",
    ]
    assert downstream["default_slice"] == NEXT_REFINEMENT_SLICE
    assert downstream["allowed_change_axis"] == [
        "left-panel text wrapping/fit",
        "bottom source/subtitle reserve separation",
    ]
    assert "YMM4 render" in downstream["disallowed_change_axis"]
    assert "audience acceptance claim" in downstream["disallowed_change_axis"]


def test_review_protocol_render_gate_and_hygiene_are_bounded() -> None:
    evaluation = _evaluation()
    review = evaluation["review_protocol_carry_forward"]
    render_gate = evaluation["render_gate_carry_forward"]

    assert review["future_user_review"] == "freeform"
    assert len(review["look_for"]) == 3
    assert review["fixed_pass_fail_labels_required"] is False
    assert review["one_user_review_is_market_proof"] is False
    assert render_gate["render_performed_in_this_slice"] is False
    assert render_gate["render_used_for_vague_visual_guessing"] is False
    assert render_gate["render_for_docs_evaluation_only_change"] is False
    assert render_gate["repeated_render_loop_avoided"] is True
    assert {"item": "template_required", "status": False} in evaluation[
        "human_burden_hygiene"
    ]
    assert {"item": "card_redesign_in_this_slice", "status": False} in evaluation[
        "inertia_check"
    ]


def test_evaluation_doc_matches_renderer_and_has_no_real_url() -> None:
    evaluation = _evaluation()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_audience_fit_benchmark_evaluation_markdown(
        evaluation
    )
    assert "material text-fit failures" in doc_text
    assert NEXT_REFINEMENT_SLICE in doc_text
    assert "actual audience acceptance" in doc_text or "actual_audience_acceptance" in doc_text
    assert _real_url_pattern().search(doc_text) is None
