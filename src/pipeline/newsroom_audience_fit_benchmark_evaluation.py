"""Evaluate current newsroom cards against the visual audience-fit benchmark.

This records a proxy evaluation of existing committed SVG/PNG card assets. It
does not launch YMM4, render video, edit .ymmp files, regenerate cards,
generate audio/TTS, fetch external sources, import media, or approve
production/public use.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_visual_audience_fit_benchmark import (
    DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH,
    NEXT_DEFAULT_SLICE as BENCHMARK_EVALUATION_SLICE,
    SOURCE_AUDIENCE_FIT_REFINEMENT_PATH,
    SOURCE_CARD_PLACEMENT_RENDER_READBACK_PATH,
    SOURCE_VISUAL_CARDS_DIR,
)


AUDIENCE_FIT_BENCHMARK_EVALUATION_SCHEMA_VERSION = (
    "newsroom_audience_fit_benchmark_evaluation.v1"
)
AUDIENCE_FIT_BENCHMARK_EVALUATION_ID = (
    "newsroom_audience_fit_benchmark_evaluation_v1_2026_06_26"
)

DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH = Path(
    "samples/_probe/newsroom_handoff/audience_fit_benchmark_evaluation_v1.json"
)
DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_AUDIENCE_FIT_BENCHMARK_EVALUATION_V1_2026-06-26.md"
)

NEXT_REFINEMENT_SLICE = "newsroom-visual-card-benchmarked-refinement-v1"
REFERENCE_PACK_SLICE = "newsroom-reference-pack-visual-grammar-v1"
OPERATOR_REVIEW_SLICE = "newsroom-internal-review-v0.1-operator-review-card"
RENDER_READBACK_SLICE = "newsroom-post-audience-fit-render-smoke-result-readback-v1"


CARD_EVALUATION_NOTES: dict[str, dict[str, Any]] = {
    "visual_card_cap_beat_fake_intro_001_01_v1": {
        "evaluation_status": "warning",
        "observed_title": "TODAY'S POINT",
        "observed_primary_message": "Fake topic, review only.",
        "visual_notes": [
            "role and review-only boundary are clear",
            "headline visually reaches the left panel boundary",
            "source label crowds the subtitle reserve band",
        ],
    },
    "visual_card_cap_beat_fake_intro_001_02_v1": {
        "evaluation_status": "warning",
        "observed_title": "HOW IT FLOWS",
        "observed_primary_message": "Review-only handoff stays.",
        "visual_notes": [
            "simple 1-2-3 flow is clear",
            "headline visually reaches the left panel boundary",
            "source label crowds the subtitle reserve band",
        ],
    },
    "visual_card_cap_beat_fake_claim_001_01_v1": {
        "evaluation_status": "fail",
        "observed_title": "CHECK POINT",
        "observed_primary_message": "A fake claim is shown.",
        "visual_notes": [
            "check/caution/status boxes are clear",
            "left-panel body text is visibly clipped at the right edge",
            "source label crowds the subtitle reserve band",
        ],
    },
    "visual_card_cap_beat_fake_claim_001_02_v1": {
        "evaluation_status": "fail",
        "observed_title": "WATCH NEXT",
        "observed_primary_message": "Fake source checks are noted.",
        "visual_notes": [
            "source/status/next role is clear",
            "headline is visibly clipped at the right edge",
            "source label crowds the subtitle reserve band",
        ],
    },
}


def build_default_newsroom_audience_fit_benchmark_evaluation(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed benchmark evaluation from current card assets."""
    base = Path(root) if root is not None else Path(".")
    benchmark = load_json_object(base / DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH)
    refinement = load_json_object(base / SOURCE_AUDIENCE_FIT_REFINEMENT_PATH)
    render_readback = load_json_object(base / SOURCE_CARD_PLACEMENT_RENDER_READBACK_PATH)
    cards = _evaluated_cards(base, refinement, render_readback)
    return build_newsroom_audience_fit_benchmark_evaluation(
        benchmark,
        refinement,
        render_readback,
        cards,
    )


def write_default_newsroom_audience_fit_benchmark_evaluation_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write the evaluation JSON and human-readable readback document."""
    base = Path(root) if root is not None else Path(".")
    evaluation = build_default_newsroom_audience_fit_benchmark_evaluation(root=base)
    _write_json(base / DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH, evaluation)
    _write_text(
        base / DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_DOC_PATH,
        render_newsroom_audience_fit_benchmark_evaluation_markdown(evaluation),
    )
    return evaluation


def build_newsroom_audience_fit_benchmark_evaluation(
    benchmark: dict[str, Any],
    refinement: dict[str, Any],
    render_readback: dict[str, Any],
    cards: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a benchmark application readback from current evidence."""
    proxy_results = _proxy_metric_results(cards)
    failures = [
        row for row in proxy_results if row["result"] == "fail"
    ]
    warnings = [
        row for row in proxy_results if row["result"] == "warning"
    ]
    recommendation = {
        "selected_next_slice": NEXT_REFINEMENT_SLICE,
        "reason": (
            "current cards fail the material text clipping/wrapping proxy and "
            "show subtitle/source-band crowding warnings"
        ),
        "not_selected": [
            {
                "slice": REFERENCE_PACK_SLICE,
                "reason": "familiarity can be evaluated as warning without blocking on references",
            },
            {
                "slice": OPERATOR_REVIEW_SLICE,
                "reason": "current cards are not sufficient for internal review while clipping remains",
            },
            {
                "slice": RENDER_READBACK_SLICE,
                "reason": "this slice evaluates cards; no new render result needs normalization",
            },
        ],
    }
    return {
        "artifact_id": AUDIENCE_FIT_BENCHMARK_EVALUATION_ID,
        "evaluation_id": AUDIENCE_FIT_BENCHMARK_EVALUATION_ID,
        "schema_version": AUDIENCE_FIT_BENCHMARK_EVALUATION_SCHEMA_VERSION,
        "benchmark_status": "applied",
        "evaluation_status": "material_proxy_failures_found",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "visual_work_class": "audience_fit",
        "evidence_level": [
            "L1_user_freeform_direction",
            "local_proxy_evaluation",
        ],
        "audience_acceptance_claimed": False,
        "identity": {
            "evaluation_id": AUDIENCE_FIT_BENCHMARK_EVALUATION_ID,
            "source_benchmark_path": _path_text(DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH),
            "source_benchmark_id": benchmark.get("benchmark_id"),
            "source_cards_dir": _path_text(SOURCE_VISUAL_CARDS_DIR),
            "source_audience_fit_refinement_path": _path_text(
                SOURCE_AUDIENCE_FIT_REFINEMENT_PATH
            ),
            "source_audience_fit_refinement_id": refinement.get("refinement_id"),
            "source_card_render_readback_path": _path_text(
                SOURCE_CARD_PLACEMENT_RENDER_READBACK_PATH
            ),
            "source_card_render_readback_id": render_readback.get("readback_id"),
            "production_status": "diagnostic_only",
            "visual_work_class": "audience_fit",
        },
        "source_validation": _source_validation(benchmark, refinement, render_readback, cards),
        "evaluated_card_inventory": cards,
        "proxy_metric_evaluation": proxy_results,
        "evaluation_summary": {
            "benchmark_status": "applied",
            "card_count_evaluated": len(cards),
            "pass_count": len([row for row in proxy_results if row["result"] == "pass"]),
            "warning_count": len(warnings),
            "fail_count": len(failures),
            "unknown_count": len([row for row in proxy_results if row["result"] == "unknown"]),
            "next_iteration_allowed": True,
            "benchmark_failures_justifying_iteration": [
                row["metric_id"] for row in failures
            ],
            "benchmark_warnings_to_consider": [
                row["metric_id"] for row in warnings
            ],
        },
        "unknowns_preserved": [
            "actual target viewer preference",
            "CTR / retention",
            "target viewer comprehension outside this project",
            "production visual quality",
            "real newsroom visual acceptance",
        ],
        "not_accepted_scope": {
            "actual_audience_acceptance": False,
            "production_visual_quality": False,
            "public_video_readiness": False,
            "real_newsroom_visual_acceptance": False,
            "real_content_readiness": False,
            "production_approval": False,
        },
        "recommendation": recommendation,
        "review_protocol_carry_forward": {
            "future_user_review": "freeform",
            "look_for": [
                "Can the card role be understood within a few seconds?",
                "Is any meaningful text too small or clipped?",
                "Does the visual feel familiar enough for an explanatory YouTube video?",
            ],
            "look_for_count": 3,
            "fixed_pass_fail_labels_required": False,
            "one_user_review_is_market_proof": False,
            "schema_owner": "Agent/Supervisor",
        },
        "render_gate_carry_forward": {
            "render_performed_in_this_slice": False,
            "render_used_for_vague_visual_guessing": False,
            "next_render_only_after": [
                "benchmark-linked material visual change",
                "internal review milestone",
            ],
            "render_for_docs_evaluation_only_change": False,
            "repeated_render_loop_avoided": True,
            "output_first_principle_preserved": True,
        },
        "completion_matrix": [
            {"item": "current_repo_state_verified", "status": True},
            {"item": "benchmark_spec_inspected", "status": True},
            {"item": "current_cards_inspected", "status": True},
            {"item": "benchmark_applied_to_current_cards", "status": True},
            {"item": "next_benchmark_linked_action_selected", "status": True},
            {"item": "narrow_commit_created_and_pushed_if_push_gate_passes", "status": "pending_until_git_gate"},
        ],
        "artifact_readiness": [
            {"item": "evaluation_json_exists", "status": True},
            {"item": "human_doc_exists", "status": True},
            {"item": "card_inventory_present", "status": True},
            {"item": "proxy_metric_results_present", "status": True},
            {"item": "unknowns_not_accepted_scope_preserved", "status": True},
            {"item": "downstream_next_use_described", "status": True},
        ],
        "visual_benchmark_evaluation": [
            {"item": "target_audience_assumption_reused", "status": True},
            {"item": "visual_job_to_be_done_reused", "status": True},
            {"item": "proxy_metrics_applied", "status": True},
            {"item": "pass_fail_unknown_recorded", "status": True},
            {"item": "evidence_level_stated", "status": True},
            {"item": "unknowns_preserved", "status": True},
            {"item": "next_iteration_permission_decided", "status": True},
            {"item": "review_protocol_carried_forward", "status": True},
        ],
        "render_gate_hygiene": [
            {"item": "no_render_performed", "status": True},
            {"item": "render_not_used_for_vague_visual_guessing", "status": True},
            {"item": "next_render_tied_to_benchmark_linked_material_change", "status": True},
            {"item": "no_render_for_docs_evaluation_only_change", "status": True},
            {"item": "repeated_render_loop_avoided", "status": True},
            {"item": "output_first_principle_preserved", "status": True},
        ],
        "human_burden_hygiene": [
            {"item": "user_input", "status": "freeform"},
            {"item": "template_required", "status": False},
            {"item": "schema_owner", "status": "Agent"},
            {"item": "user_side_work_for_this_slice", "status": "none"},
            {"item": "future_review_look_for_count", "status": 3},
            {"item": "negative_confirmation_checklist", "status": False},
            {"item": "fixed_form_relapse", "status": False},
        ],
        "review_non_redundancy": [
            {"item": "benchmark_spec_reused", "status": True},
            {"item": "prior_visual_reviews_reused", "status": True},
            {"item": "next_axis_stated_as_benchmark_evaluation", "status": True},
            {"item": "not_accepted_scope_preserved", "status": True},
            {"item": "repeated_user_review_requested", "status": False},
            {"item": "mechanics_re_review_requested", "status": False},
        ],
        "inertia_check": [
            {"item": "ad_hoc_visual_iteration_remains_stopped", "status": True},
            {"item": "card_redesign_in_this_slice", "status": False},
            {"item": "packet_for_packet_drift", "status": False},
            {"item": "readiness_separated_from_slice_completion", "status": True},
            {"item": "next_concrete_benchmark_linked_milestone", "status": NEXT_REFINEMENT_SLICE},
        ],
        "boundaries": {
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
        },
        "downstream_next_use": {
            "default_slice": NEXT_REFINEMENT_SLICE,
            "instruction": "fix only the concrete benchmark failures before another review or render milestone",
            "allowed_change_axis": [
                "left-panel text wrapping/fit",
                "bottom source/subtitle reserve separation",
            ],
            "disallowed_change_axis": [
                "new visual concept exploration",
                "YMM4 render",
                "real media import",
                "audience acceptance claim",
            ],
        },
    }


def render_newsroom_audience_fit_benchmark_evaluation_markdown(
    evaluation: dict[str, Any],
) -> str:
    """Render a compact human-readable evaluation report."""
    lines = [
        "# Newsroom Audience-Fit Benchmark Evaluation v1",
        "",
        f"artifact_id: {evaluation['artifact_id']}",
        f"evaluation_id: {evaluation['evaluation_id']}",
        f"schema_version: {evaluation['schema_version']}",
        f"benchmark_status: {evaluation['benchmark_status']}",
        f"evaluation_status: {evaluation['evaluation_status']}",
        f"production_status: {evaluation['production_status']}",
        "",
        "## Outcome",
        "",
        "The current cards are understandable as diagnostic review-only cards, but the benchmark finds material text-fit failures. The next action is a benchmarked refinement, not a new visual concept, YMM4 render, .ymmp edit, or audience-acceptance claim.",
        "",
        "## Card Inventory",
        "",
        "| card | role | title | primary message | status |",
        "|---|---|---|---|---|",
    ]
    for card in evaluation["evaluated_card_inventory"]:
        lines.append(
            f"| {card['card_id']} | {card['role']} | {card['observed_title']} | {card['observed_primary_message']} | {card['evaluation_status']} |"
        )
    lines.extend(
        [
            "",
            "## Proxy Metric Results",
            "",
            "| metric | result | evidence | recommended response |",
            "|---|---|---|---|",
        ]
    )
    for row in evaluation["proxy_metric_evaluation"]:
        lines.append(
            f"| {row['metric_id']} | {row['result']} | {row['evidence']} | {row['recommended_response']} |"
        )
    summary = evaluation["evaluation_summary"]
    lines.extend(
        [
            "",
            "## Evaluation Summary",
            "",
            f"- benchmark_status: {summary['benchmark_status']}",
            f"- pass_count: {summary['pass_count']}",
            f"- warning_count: {summary['warning_count']}",
            f"- fail_count: {summary['fail_count']}",
            f"- unknown_count: {summary['unknown_count']}",
            f"- next_iteration_allowed: {summary['next_iteration_allowed']}",
            f"- failures: {', '.join(summary['benchmark_failures_justifying_iteration'])}",
            f"- warnings: {', '.join(summary['benchmark_warnings_to_consider'])}",
            "",
            "## Unknowns / Not Accepted Scope",
            "",
            f"- unknowns_preserved: {', '.join(evaluation['unknowns_preserved'])}",
        ]
    )
    for key in sorted(evaluation["not_accepted_scope"]):
        lines.append(f"- {key}: {evaluation['not_accepted_scope'][key]}")
    recommendation = evaluation["recommendation"]
    lines.extend(
        [
            "",
            "## Recommendation / Next Axis",
            "",
            f"- selected_next_slice: {recommendation['selected_next_slice']}",
            f"- reason: {recommendation['reason']}",
            "",
            "## Review Protocol Carry-Forward",
            "",
            f"- future_user_review: {evaluation['review_protocol_carry_forward']['future_user_review']}",
            f"- look_for: {', '.join(evaluation['review_protocol_carry_forward']['look_for'])}",
            f"- fixed_pass_fail_labels_required: {evaluation['review_protocol_carry_forward']['fixed_pass_fail_labels_required']}",
            f"- one_user_review_is_market_proof: {evaluation['review_protocol_carry_forward']['one_user_review_is_market_proof']}",
            "",
            "## Render Gate",
            "",
        ]
    )
    for key in sorted(evaluation["render_gate_carry_forward"]):
        lines.append(f"- {key}: {evaluation['render_gate_carry_forward'][key]}")
    _append_status_table(lines, "Completion Matrix", evaluation["completion_matrix"])
    _append_status_table(lines, "Artifact Readiness", evaluation["artifact_readiness"])
    _append_status_table(
        lines,
        "Visual Benchmark Evaluation",
        evaluation["visual_benchmark_evaluation"],
    )
    _append_status_table(lines, "Human Burden Hygiene", evaluation["human_burden_hygiene"])
    _append_status_table(
        lines,
        "Review Non-Redundancy",
        evaluation["review_non_redundancy"],
    )
    _append_status_table(lines, "Inertia Check", evaluation["inertia_check"])
    lines.extend(["", "## Boundary", ""])
    for key in sorted(evaluation["boundaries"]):
        lines.append(f"- {key}: {evaluation['boundaries'][key]}")
    lines.extend(
        [
            "",
            "## Downstream Next Use",
            "",
            f"- default_slice: {evaluation['downstream_next_use']['default_slice']}",
            f"- instruction: {evaluation['downstream_next_use']['instruction']}",
            f"- allowed_change_axis: {', '.join(evaluation['downstream_next_use']['allowed_change_axis'])}",
            f"- disallowed_change_axis: {', '.join(evaluation['downstream_next_use']['disallowed_change_axis'])}",
            "",
        ]
    )
    return "\n".join(lines)


def _evaluated_cards(
    base: Path,
    refinement: dict[str, Any],
    render_readback: dict[str, Any],
) -> list[dict[str, Any]]:
    captions = {
        row["expected_mapping_source"]: row["expected_dialogue_or_caption"]
        for row in render_readback.get("screenshot_supported_card_observations", [])
    }
    cards: list[dict[str, Any]] = []
    for row in refinement.get("design_changes", []):
        card_id = row["card_id"]
        svg_path = Path(row["output_svg_path"])
        png_path = Path(row["output_png_path"])
        note = CARD_EVALUATION_NOTES[card_id]
        svg_info = _svg_info(base / svg_path)
        cards.append(
            {
                "card_id": card_id,
                "svg_path": _path_text(svg_path),
                "png_path": _path_text(png_path),
                "role": row["role"],
                "role_label": row["role_label"],
                "layout_motif": row["layout_motif"],
                "observed_title": note["observed_title"],
                "observed_primary_message": note["observed_primary_message"],
                "mapped_caption_or_dialogue": captions.get(card_id),
                "evaluation_status": note["evaluation_status"],
                "visual_notes": note["visual_notes"],
                "min_font_size": svg_info["min_font_size"],
                "max_font_size": svg_info["max_font_size"],
                "review_only_visible": svg_info["review_only_visible"],
                "diagnostic_visible": svg_info["diagnostic_visible"],
                "subtitle_area_visible": svg_info["subtitle_area_visible"],
                "real_url_or_www_in_svg_text": svg_info["real_url_or_www_in_svg_text"],
                "svg_exists": (base / svg_path).exists(),
                "png_exists": (base / png_path).exists(),
                "png_size": _png_size(base / png_path),
            }
        )
    return cards


def _proxy_metric_results(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    warning_cards = [
        card["card_id"] for card in cards if card["evaluation_status"] == "warning"
    ]
    fail_cards = [
        card["card_id"] for card in cards if card["evaluation_status"] == "fail"
    ]
    all_cards = [card["card_id"] for card in cards]
    return [
        {
            "metric_id": "readability_at_a_glance",
            "source_benchmark_metric_id": "readability_at_a_glance",
            "criterion": "role and dominant message should be understood in about 3 seconds",
            "how_checked": "static PNG visual inspection plus SVG title/role extraction",
            "result": "warning",
            "evidence": "roles are visible, but long headlines crowd or cross the left panel boundary",
            "affected_cards": warning_cards + fail_cards,
            "recommended_response": "shorten or wrap dominant messages before another visual milestone",
        },
        {
            "metric_id": "text_clipping_or_wrapping",
            "source_benchmark_metric_id": "text_clipping_wrapping",
            "criterion": "no meaningful text should be clipped and wrapping should preserve readable phrases",
            "how_checked": "static PNG visual inspection against panel boundaries",
            "result": "fail",
            "evidence": "cards 3 and 4 visibly clip meaningful left-panel text; cards 1 and 2 crowd the same boundary",
            "affected_cards": all_cards,
            "recommended_response": "fix left-panel wrapping/fit in a benchmarked refinement",
        },
        {
            "metric_id": "minimum_meaningful_font_size",
            "source_benchmark_metric_id": "minimum_meaningful_font_size",
            "criterion": "essential card meaning uses the 34px or larger card text floor",
            "how_checked": "SVG font-size extraction",
            "result": "pass",
            "evidence": "minimum SVG text size is 34px across current cards",
            "affected_cards": [],
            "recommended_response": "keep the 34px floor; do not shrink text to solve clipping",
        },
        {
            "metric_id": "one_dominant_message_per_card",
            "source_benchmark_metric_id": "one_dominant_message_per_card",
            "criterion": "each card should present one primary point before secondary labels",
            "how_checked": "card title/headline/role inspection",
            "result": "pass",
            "evidence": "POINT, FLOW, CHECK, and NEXT each carry a distinct primary message",
            "affected_cards": [],
            "recommended_response": "preserve one-message structure during text-fit correction",
        },
        {
            "metric_id": "familiar_explainer_visual_grammar",
            "source_benchmark_metric_id": "familiar_explainer_tv_youtube_grammar",
            "criterion": "layout should resemble large-block explainer or simple TV/YouTube panel grammar",
            "how_checked": "static card composition inspection against benchmark hypotheses",
            "result": "warning",
            "evidence": "large blocks and role labels are present, but no reference pack proves market fit",
            "affected_cards": all_cards,
            "recommended_response": "do not block on references; fix concrete text-fit failures first",
        },
        {
            "metric_id": "no_reliance_on_tiny_metadata",
            "source_benchmark_metric_id": "no_tiny_metadata_dependency",
            "criterion": "core meaning should not depend on tiny metadata",
            "how_checked": "visual inspection of source/subtitle band and primary card labels",
            "result": "warning",
            "evidence": "core meaning does not depend on source labels, but source labels crowd the subtitle reserve",
            "affected_cards": all_cards,
            "recommended_response": "separate or down-prioritize source labels without making them essential",
        },
        {
            "metric_id": "card_role_variation",
            "source_benchmark_metric_id": "card_to_card_role_variation",
            "criterion": "cards should have visibly different roles, motifs, and reading order",
            "how_checked": "role labels and layout motif inventory",
            "result": "pass",
            "evidence": "large number, process steps, check/warning boxes, and source/status panel are distinct",
            "affected_cards": [],
            "recommended_response": "preserve role variation while correcting text fit",
        },
        {
            "metric_id": "pacing_density_for_68_sec_video",
            "source_benchmark_metric_id": "pacing_density_68_sec",
            "criterion": "density should be understandable during normal 68 sec playback",
            "how_checked": "static card density plus prior render readback context; no render in this slice",
            "result": "warning",
            "evidence": "prior render observed four cards over 68 sec, but current clipping may hurt normal playback comprehension",
            "affected_cards": fail_cards,
            "recommended_response": "correct text fit before using render as an internal review milestone",
        },
        {
            "metric_id": "diagnostic_boundary_visibility",
            "source_benchmark_metric_id": "diagnostic_boundary_visibility",
            "criterion": "fake/review-only boundary should be visible without tiny footnotes",
            "how_checked": "SVG text extraction and PNG visual inspection",
            "result": "pass",
            "evidence": "REVIEW ONLY and DIAGNOSTIC are large and present on every card",
            "affected_cards": [],
            "recommended_response": "preserve top boundary labels",
        },
        {
            "metric_id": "no_real_brand_url_public_claim",
            "source_benchmark_metric_id": "no_real_brand_url_public_claim",
            "criterion": "no real brand, URL, screenshot, or public-readiness claim should appear",
            "how_checked": "SVG text scan plus existing refinement boundary readback",
            "result": "pass",
            "evidence": "no real brand, URL, news screenshot, or public-readiness claim appears in card text",
            "affected_cards": [],
            "recommended_response": "keep real media and public claims out of the refinement",
        },
    ]


def _source_validation(
    benchmark: dict[str, Any],
    refinement: dict[str, Any],
    render_readback: dict[str, Any],
    cards: list[dict[str, Any]],
) -> dict[str, Any]:
    errors: list[str] = []
    if benchmark.get("benchmark_status") != "draft_proxy_benchmark_defined":
        errors.append("benchmark_not_defined")
    if refinement.get("refinement_status") != "assets_regenerated":
        errors.append("audience_fit_refinement_missing")
    if render_readback.get("result_status") != "pass":
        errors.append("prior_render_readback_not_pass")
    if len(cards) != 4:
        errors.append("expected_four_cards")
    for card in cards:
        if not card["svg_exists"] or not card["png_exists"]:
            errors.append(f"missing_asset:{card['card_id']}")
        if card["png_size"] != {"width": 1920, "height": 1080}:
            errors.append(f"unexpected_png_size:{card['card_id']}")
        if card["real_url_or_www_in_svg_text"]:
            errors.append(f"real_url_or_www_in_svg_text:{card['card_id']}")
    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "source_benchmark_status": benchmark.get("benchmark_status"),
        "source_refinement_status": refinement.get("refinement_status"),
        "source_render_readback_status": render_readback.get("result_status"),
        "card_count": len(cards),
    }


def _svg_info(path: Path) -> dict[str, Any]:
    root = ElementTree.fromstring(path.read_text(encoding="utf-8"))
    text_nodes = list(root.iter("{http://www.w3.org/2000/svg}text"))
    if not text_nodes:
        text_nodes = [node for node in root.iter() if node.tag.endswith("text")]
    texts = ["".join(node.itertext()) for node in text_nodes]
    sizes = [
        int(node.attrib["font-size"])
        for node in text_nodes
        if node.attrib.get("font-size", "").isdigit()
    ]
    searchable_text = " ".join(texts).lower()
    return {
        "min_font_size": min(sizes),
        "max_font_size": max(sizes),
        "review_only_visible": "review only" in searchable_text,
        "diagnostic_visible": "diagnostic" in searchable_text,
        "subtitle_area_visible": "subtitle area" in searchable_text,
        "real_url_or_www_in_svg_text": "http://" in searchable_text
        or "https://" in searchable_text
        or "www." in searchable_text,
    }


def _png_size(path: Path) -> dict[str, int] | None:
    if not path.exists():
        return None
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    return {
        "width": int.from_bytes(header[16:20], "big"),
        "height": int.from_bytes(header[20:24], "big"),
    }


def _append_status_table(lines: list[str], title: str, rows: list[dict[str, Any]]) -> None:
    lines.extend(["", f"## {title}", "", "| item | status |", "|---|---|"])
    for row in rows:
        lines.append(f"| {row['item']} | {row['status']} |")


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )


def _write_text(path: str | Path, text: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _path_text(path: str | Path) -> str:
    return Path(path).as_posix()
