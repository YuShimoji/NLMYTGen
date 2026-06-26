import json
import re
from pathlib import Path

from src.pipeline.newsroom_visual_audience_fit_benchmark import (
    DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_DOC_PATH,
    DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH,
    NEXT_DEFAULT_SLICE,
    VISUAL_AUDIENCE_FIT_BENCHMARK_ID,
    VISUAL_AUDIENCE_FIT_BENCHMARK_SCHEMA_VERSION,
    build_default_newsroom_visual_audience_fit_benchmark,
    render_newsroom_visual_audience_fit_benchmark_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_PATH = ROOT / DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH
DOC_PATH = ROOT / DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_DOC_PATH


def _benchmark() -> dict:
    return json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_benchmark_json_matches_builder_output_and_identity() -> None:
    benchmark = _benchmark()

    assert benchmark == build_default_newsroom_visual_audience_fit_benchmark(root=ROOT)
    assert benchmark["artifact_id"] == VISUAL_AUDIENCE_FIT_BENCHMARK_ID
    assert benchmark["benchmark_id"] == VISUAL_AUDIENCE_FIT_BENCHMARK_ID
    assert benchmark["schema_version"] == VISUAL_AUDIENCE_FIT_BENCHMARK_SCHEMA_VERSION
    assert benchmark["benchmark_status"] == "draft_proxy_benchmark_defined"
    assert benchmark["visual_work_class"] == "audience_fit"
    assert benchmark["production_status"] == "diagnostic_only"
    assert benchmark["diagnostic_only"] is True
    assert benchmark["identity"]["current_cards_status"] == (
        "improved_but_not_audience_fit_accepted"
    )


def test_source_validation_uses_current_audience_fit_evidence_without_new_media() -> None:
    validation = _benchmark()["source_validation"]
    boundaries = _benchmark()["boundaries"]

    assert validation == {
        "status": "passed",
        "errors": [],
        "source_audience_fit_refinement_status": "assets_regenerated",
        "source_audience_fit_review_status": "ready_for_supervisor_review",
        "source_internal_review_prep_status": "ready_for_supervisor_review",
        "source_card_render_result_status": "pass",
        "post_refinement_render_package_status": (
            "ready_for_manual_milestone_render_smoke"
        ),
        "current_card_asset_count": 8,
    }
    assert boundaries == {
        "YMM4_launched_by_agent": False,
        "video_render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "ymmp_edited_by_agent": False,
        "cards_regenerated_in_this_slice": False,
        "external_fetch_performed": False,
        "real_media_imported": False,
        "production_visual_quality_accepted": False,
        "actual_audience_acceptance_claimed": False,
        "public_video_ready": False,
    }


def test_target_audience_job_and_evidence_level_preserve_unknowns() -> None:
    benchmark = _benchmark()
    target = benchmark["target_audience_assumption"]
    job = benchmark["visual_job_to_be_done"]
    evidence = benchmark["evidence_level"]

    assert target["assumed_audience"] == [
        "general YouTube viewers for explanatory/newsroom-style content",
        "non-expert",
        "low patience",
        "expects familiar visual grammar",
    ]
    assert target["device_screen_assumption"] == (
        "1080p baseline, readable after video compression"
    )
    assert job["dominant_message"] == "one clear point per card"
    assert "audience acceptance proof" in job["non_goals"]
    assert evidence["current_level"] == "L1_user_freeform_direction"
    assert evidence["evidence_not_yet"] == [
        "L2_reference_pack",
        "L3_proxy_metric_pass",
        "L4_target_viewer_feedback",
        "L5_actual_analytics",
    ]
    assert "actual target viewer preference" in evidence["unknowns"]
    assert "production visual quality" in evidence["unknowns"]


def test_proxy_metrics_and_acceptance_criteria_cover_required_benchmark_axes() -> None:
    benchmark = _benchmark()
    metric_ids = [row["metric_id"] for row in benchmark["proxy_metrics"]]
    criteria = benchmark["acceptance_criteria"]

    assert metric_ids == [
        "readability_at_a_glance",
        "text_clipping_wrapping",
        "minimum_meaningful_font_size",
        "one_dominant_message_per_card",
        "familiar_explainer_tv_youtube_grammar",
        "no_tiny_metadata_dependency",
        "card_to_card_role_variation",
        "pacing_density_68_sec",
        "diagnostic_boundary_visibility",
        "no_real_brand_url_public_claim",
    ]
    assert len(metric_ids) >= 10
    assert "no clipped meaningful text" in criteria["must"]
    assert "no tiny metadata carrying essential meaning" in criteria["must"]
    assert "card role understood within about 3 seconds" in criteria["must"]
    assert "familiar large-block layout" in criteria["should"]
    assert "claim actual audience acceptance" in criteria["must_not"]
    assert "use real brand, URL, or news screenshot" in criteria["must_not"]


def test_reference_abstraction_is_deferred_and_not_market_proof() -> None:
    reference = _benchmark()["reference_benchmark_abstraction"]

    assert reference["reference_pack_status"] == "needed_or_deferred"
    assert reference["candidate_reference_types"] == [
        "Japanese explainer video card",
        "TV info-board style",
        "YouTube news commentary simple panel",
        "educational slide-like callout",
    ]
    assert reference["hypotheses_not_market_proof"] is True
    assert "do not copy reference images" in reference["no_copy_policy"]


def test_review_protocol_and_gate_allow_only_benchmark_linked_next_work() -> None:
    benchmark = _benchmark()
    protocol = benchmark["review_protocol"]
    gate = benchmark["visual_benchmark_gate"]

    assert protocol["look_for"] == [
        "Can the card role be understood within a few seconds?",
        "Is any meaningful text too small or clipped?",
        "Does the visual feel familiar enough for an explanatory YouTube video?",
    ]
    assert len(protocol["look_for"]) == 3
    assert protocol["answer_style"] == "freeform"
    assert protocol["form_required"] is False
    assert protocol["template_required"] is False
    assert gate["status"] == "draft"
    assert gate["benchmark_status"] == "defined_not_applied"
    assert gate["proxy_metrics"]["metric_count"] == 10
    assert gate["proxy_metrics"]["current_cards_evaluated"] is False
    assert gate["next_iteration_allowed"] is True
    assert gate["next_iteration_allowed_scope"] == NEXT_DEFAULT_SLICE
    assert gate["visual_refinement_allowed_before_evaluation"] is False
    assert gate["missing_benchmark_components"] == []


def test_next_slice_render_gate_and_human_burden_are_bounded() -> None:
    benchmark = _benchmark()

    assert benchmark["recommended_next_slice"]["slice"] == NEXT_DEFAULT_SLICE
    assert [row["slice"] for row in benchmark["alternative_next_slices"]] == [
        "newsroom-visual-card-benchmarked-refinement-v1",
        "newsroom-reference-pack-visual-grammar-v1",
        "newsroom-internal-review-v0.1-operator-review-card",
    ]
    assert benchmark["downstream_next_use"] == {
        "default_slice": NEXT_DEFAULT_SLICE,
        "instruction": (
            "score the current cards against the proxy metrics before any further "
            "visual redesign"
        ),
        "evaluation_subject": "current four diagnostic SVG/PNG cards",
        "refinement_gate": (
            "only concrete benchmark failures may drive a later benchmarked refinement"
        ),
    }
    assert all(row["status"] is True for row in benchmark["render_gate_hygiene"])
    assert {"item": "template_required", "status": False} in benchmark[
        "human_burden_hygiene"
    ]
    assert {"item": "fixed_form_relapse", "status": False} in benchmark[
        "human_burden_hygiene"
    ]
    assert {"item": "ad_hoc_visual_iteration_stopped", "status": True} in benchmark[
        "inertia_check"
    ]


def test_benchmark_doc_matches_renderer_and_has_no_real_url() -> None:
    benchmark = _benchmark()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_visual_audience_fit_benchmark_markdown(
        benchmark
    )
    assert "Visual Benchmark Gate" in doc_text
    assert "newsroom-audience-fit-benchmark-evaluation-v1" in doc_text
    assert "production approval" in doc_text
    assert _real_url_pattern().search(doc_text) is None
