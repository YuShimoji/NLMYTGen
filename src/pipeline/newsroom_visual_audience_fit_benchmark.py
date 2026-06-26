"""Visual audience-fit benchmark spec for the newsroom diagnostic cards.

This slice defines a proxy benchmark before further audience-facing visual
refinement. It does not launch YMM4, render video, edit .ymmp files, regenerate
cards, generate audio/TTS, fetch external sources, import media, or approve
production/public use.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_episode_production_capsule import load_json_object


VISUAL_AUDIENCE_FIT_BENCHMARK_SCHEMA_VERSION = (
    "newsroom_visual_audience_fit_benchmark.v1"
)
VISUAL_AUDIENCE_FIT_BENCHMARK_ID = (
    "newsroom_visual_audience_fit_benchmark_v1_2026_06_26"
)

DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH = Path(
    "samples/_probe/newsroom_handoff/visual_audience_fit_benchmark_v1.json"
)
DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_DOC_PATH = Path(
    "docs/verification/NEWSROOM_VISUAL_AUDIENCE_FIT_BENCHMARK_V1_2026-06-26.md"
)

SOURCE_AUDIENCE_FIT_REFINEMENT_PATH = Path(
    "samples/_probe/newsroom_handoff/visual_card_audience_fit_refinement_v1.json"
)
SOURCE_AUDIENCE_FIT_REVIEW_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "visual_card_audience_fit_review_readback_v1.json"
)
SOURCE_VISUAL_CARD_DESIGN_REFINEMENT_PATH = Path(
    "samples/_probe/newsroom_handoff/visual_card_design_refinement_v1.json"
)
SOURCE_INTERNAL_REVIEW_PREP_PATH = Path(
    "samples/_probe/newsroom_handoff/internal_review_v0_1_prep_v1.json"
)
SOURCE_CARD_PLACEMENT_RENDER_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "card_placement_render_smoke_result_readback_v1.json"
)
SOURCE_POST_REFINEMENT_RENDER_PACKAGE_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "card_placement_post_refinement_render_smoke_v1.json"
)
SOURCE_VISUAL_CARDS_DIR = Path(
    "samples/_probe/newsroom_handoff/visual_cards_v1"
)

NEXT_DEFAULT_SLICE = "newsroom-audience-fit-benchmark-evaluation-v1"
BENCHMARKED_REFINEMENT_SLICE = "newsroom-visual-card-benchmarked-refinement-v1"
REFERENCE_PACK_SLICE = "newsroom-reference-pack-visual-grammar-v1"
OPERATOR_REVIEW_SLICE = "newsroom-internal-review-v0.1-operator-review-card"


PROXY_METRICS: tuple[dict[str, Any], ...] = (
    {
        "metric_id": "readability_at_a_glance",
        "pass": "card role and dominant message are understandable in about 3 seconds",
        "fail": "viewer must pause, inspect tiny text, or infer from metadata",
        "unknown": "no benchmark evaluation has been run against current cards yet",
    },
    {
        "metric_id": "text_clipping_wrapping",
        "pass": "no meaningful text is clipped and wrapping preserves readable phrases",
        "fail": "meaningful label, headline, or body text is clipped or awkwardly wrapped",
        "unknown": "render compression and final placement are not benchmarked here",
    },
    {
        "metric_id": "minimum_meaningful_font_size",
        "pass": "essential meaning uses the current 34px or larger card text floor",
        "fail": "essential meaning depends on text below the 34px floor or footer microcopy",
        "unknown": "apparent size after video compression still needs evaluation",
    },
    {
        "metric_id": "one_dominant_message_per_card",
        "pass": "each card has one primary point before secondary labels",
        "fail": "multiple equal-weight messages compete for attention",
        "unknown": "viewer comprehension outside the project is not measured",
    },
    {
        "metric_id": "familiar_explainer_tv_youtube_grammar",
        "pass": "layout resembles large-block explainer, TV info-board, or simple YouTube panel grammar",
        "fail": "layout reads mainly as SaaS dashboard, audit UI, or dense internal tool",
        "unknown": "reference pack is needed before calling this market-proven",
    },
    {
        "metric_id": "no_tiny_metadata_dependency",
        "pass": "small metadata is decorative or diagnostic, not required for core meaning",
        "fail": "role, claim, fake boundary, or next action depends on tiny metadata",
        "unknown": "requires card-by-card benchmark evaluation",
    },
    {
        "metric_id": "card_to_card_role_variation",
        "pass": "cards have visibly different roles, motifs, and reading order",
        "fail": "cards feel like repeated panels with swapped text",
        "unknown": "variation has not yet been judged against this benchmark",
    },
    {
        "metric_id": "pacing_density_68_sec",
        "pass": "density can be understood during normal 68 sec playback",
        "fail": "viewer must frame-step or pause because density exceeds pacing",
        "unknown": "current benchmark is not a new render or playback review",
    },
    {
        "metric_id": "diagnostic_boundary_visibility",
        "pass": "fake/review-only boundary is visible without reading tiny footnotes",
        "fail": "card could be mistaken for real news, source proof, or public claim",
        "unknown": "needs evaluation on current cards and any future render surface",
    },
    {
        "metric_id": "no_real_brand_url_public_claim",
        "pass": "no real brand, URL, real screenshot, or public-readiness claim is present",
        "fail": "real external identity or production/public claim appears",
        "unknown": "none for the current committed card assets; recheck future edits",
    },
)


def build_default_newsroom_visual_audience_fit_benchmark(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed visual audience-fit benchmark from current evidence."""
    base = Path(root) if root is not None else Path(".")
    sources = {
        "audience_fit_refinement": load_json_object(
            base / SOURCE_AUDIENCE_FIT_REFINEMENT_PATH
        ),
        "audience_fit_review_readback": load_json_object(
            base / SOURCE_AUDIENCE_FIT_REVIEW_READBACK_PATH
        ),
        "visual_card_design_refinement": load_json_object(
            base / SOURCE_VISUAL_CARD_DESIGN_REFINEMENT_PATH
        ),
        "internal_review_prep": load_json_object(
            base / SOURCE_INTERNAL_REVIEW_PREP_PATH
        ),
        "card_placement_render_readback": load_json_object(
            base / SOURCE_CARD_PLACEMENT_RENDER_READBACK_PATH
        ),
        "post_refinement_render_package": load_json_object(
            base / SOURCE_POST_REFINEMENT_RENDER_PACKAGE_PATH
        ),
    }
    return build_newsroom_visual_audience_fit_benchmark(
        sources,
        card_asset_count=_card_asset_count(base / SOURCE_VISUAL_CARDS_DIR),
    )


def write_default_newsroom_visual_audience_fit_benchmark_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write the benchmark JSON and human-readable benchmark document."""
    base = Path(root) if root is not None else Path(".")
    benchmark = build_default_newsroom_visual_audience_fit_benchmark(root=base)
    _write_json(base / DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH, benchmark)
    _write_text(
        base / DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_DOC_PATH,
        render_newsroom_visual_audience_fit_benchmark_markdown(benchmark),
    )
    return benchmark


def build_newsroom_visual_audience_fit_benchmark(
    sources: dict[str, dict[str, Any]],
    *,
    card_asset_count: int,
) -> dict[str, Any]:
    """Build a diagnostic-only benchmark spec from existing audience-fit evidence."""
    source_validation = _source_validation(sources, card_asset_count=card_asset_count)
    proxy_metric_summary = {
        "metric_count": len(PROXY_METRICS),
        "defined": True,
        "current_cards_evaluated": False,
        "status": "defined_not_applied",
    }

    return {
        "artifact_id": VISUAL_AUDIENCE_FIT_BENCHMARK_ID,
        "benchmark_id": VISUAL_AUDIENCE_FIT_BENCHMARK_ID,
        "schema_version": VISUAL_AUDIENCE_FIT_BENCHMARK_SCHEMA_VERSION,
        "benchmark_status": "draft_proxy_benchmark_defined",
        "visual_work_class": "audience_fit",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "identity": {
            "benchmark_id": VISUAL_AUDIENCE_FIT_BENCHMARK_ID,
            "source_audience_fit_refinement_path": _path_text(
                SOURCE_AUDIENCE_FIT_REFINEMENT_PATH
            ),
            "source_audience_fit_refinement_id": sources[
                "audience_fit_refinement"
            ].get("refinement_id"),
            "source_audience_fit_review_readback_path": _path_text(
                SOURCE_AUDIENCE_FIT_REVIEW_READBACK_PATH
            ),
            "source_audience_fit_review_readback_id": sources[
                "audience_fit_review_readback"
            ].get("readback_id"),
            "source_visual_card_design_refinement_path": _path_text(
                SOURCE_VISUAL_CARD_DESIGN_REFINEMENT_PATH
            ),
            "source_internal_review_prep_path": _path_text(
                SOURCE_INTERNAL_REVIEW_PREP_PATH
            ),
            "source_card_placement_render_readback_path": _path_text(
                SOURCE_CARD_PLACEMENT_RENDER_READBACK_PATH
            ),
            "source_post_refinement_render_package_path": _path_text(
                SOURCE_POST_REFINEMENT_RENDER_PACKAGE_PATH
            ),
            "source_visual_cards_dir": _path_text(SOURCE_VISUAL_CARDS_DIR),
            "current_cards_status": "improved_but_not_audience_fit_accepted",
        },
        "source_validation": source_validation,
        "target_audience_assumption": {
            "assumed_audience": [
                "general YouTube viewers for explanatory/newsroom-style content",
                "non-expert",
                "low patience",
                "expects familiar visual grammar",
            ],
            "viewing_context": "normal video playback, likely desktop/mobile, not frame-by-frame inspection",
            "attention_level": "must understand the dominant card message quickly",
            "device_screen_assumption": "1080p baseline, readable after video compression",
        },
        "visual_job_to_be_done": {
            "helps_viewer": [
                "understand what each fake/review-only card is doing",
                "follow a simple diagnostic structure without reading tiny metadata",
            ],
            "dominant_message": "one clear point per card",
            "non_goals": [
                "final production design",
                "real news design",
                "public-ready branding",
                "audience acceptance proof",
            ],
        },
        "evidence_level": {
            "current_level": "L1_user_freeform_direction",
            "evidence": [
                "user freeform review",
                "YMM4 screenshots",
                "local diagnostic render observations",
                "current diagnostic SVG/PNG card assets",
            ],
            "evidence_not_yet": [
                "L2_reference_pack",
                "L3_proxy_metric_pass",
                "L4_target_viewer_feedback",
                "L5_actual_analytics",
            ],
            "unknowns": [
                "actual target viewer preference",
                "retention or CTR",
                "target viewer comprehension outside the project",
                "production visual quality",
            ],
        },
        "reference_benchmark_abstraction": {
            "reference_pack_status": "needed_or_deferred",
            "no_copy_policy": "do not copy reference images, logos, brands, screenshots, or current YouTube-specific material",
            "candidate_reference_types": [
                "Japanese explainer video card",
                "TV info-board style",
                "YouTube news commentary simple panel",
                "educational slide-like callout",
            ],
            "extracted_grammar_hypotheses": [
                "large headline or role label before detail",
                "one dominant visual motif per card",
                "simple block hierarchy over dense dashboard chips",
                "diagnostic/fake boundary visible without footnote reading",
            ],
            "hypotheses_not_market_proof": True,
        },
        "proxy_metrics": list(PROXY_METRICS),
        "acceptance_criteria": {
            "must": [
                "no clipped meaningful text",
                "no tiny metadata carrying essential meaning",
                "one dominant message per card",
                "card role understood within about 3 seconds",
                "diagnostic/fake boundary visible",
            ],
            "should": [
                "familiar large-block layout",
                "visible role variation",
                "simple labels",
                "limited decorative noise",
            ],
            "must_not": [
                "claim production/public readiness",
                "claim actual audience acceptance",
                "use real brand, URL, or news screenshot",
                "use render as vague visual exploration",
            ],
        },
        "next_visual_iteration_mapping": [
            {
                "future_change": "enlarge source/footer text",
                "criteria": ["readability_at_a_glance", "no_tiny_metadata_dependency"],
            },
            {
                "future_change": "simplify card role labels",
                "criteria": ["one_dominant_message_per_card"],
            },
            {
                "future_change": "differentiate card composition",
                "criteria": ["card_to_card_role_variation"],
            },
            {
                "future_change": "reduce SaaS-like chips",
                "criteria": ["familiar_explainer_tv_youtube_grammar"],
            },
            {
                "future_change": "add simple visual motif",
                "criteria": ["readability_at_a_glance", "one_dominant_message_per_card"],
            },
            {
                "future_change": "adjust pacing/density after review",
                "criteria": ["pacing_density_68_sec"],
            },
        ],
        "review_protocol": {
            "ask_user_after": [
                "benchmarked evaluation",
                "material visual change",
            ],
            "look_for": [
                "Can the card role be understood within a few seconds?",
                "Is any meaningful text too small or clipped?",
                "Does the visual feel familiar enough for an explanatory YouTube video?",
            ],
            "answer_style": "freeform",
            "schema_owner": "Agent/Supervisor",
            "form_required": False,
            "template_required": False,
        },
        "visual_benchmark_gate": {
            "status": "draft",
            "visual_work_class": "audience_fit",
            "benchmark_status": "defined_not_applied",
            "evidence_level": "L1_user_freeform_direction",
            "proxy_metrics": proxy_metric_summary,
            "unknowns": [
                "actual audience preference",
                "target viewer comprehension",
                "production visual quality",
                "retention or CTR",
            ],
            "next_iteration_allowed": True,
            "next_iteration_allowed_scope": NEXT_DEFAULT_SLICE,
            "visual_refinement_allowed_before_evaluation": False,
            "missing_benchmark_components": [],
        },
        "recommended_next_slice": {
            "slice": NEXT_DEFAULT_SLICE,
            "reason": "apply this benchmark to the current cards once before any further redesign",
        },
        "alternative_next_slices": [
            {
                "slice": BENCHMARKED_REFINEMENT_SLICE,
                "condition": "only if benchmark evaluation finds concrete failures",
            },
            {
                "slice": REFERENCE_PACK_SLICE,
                "condition": "only if the benchmark cannot be completed without reference abstraction",
            },
            {
                "slice": OPERATOR_REVIEW_SLICE,
                "condition": "only if benchmark evaluation says current cards are sufficient for diagnostic review",
            },
        ],
        "completion_matrix": [
            {"item": "current_repo_state_verified", "status": True},
            {"item": "audience_fit_incident_normalized", "status": True},
            {"item": "visual_benchmark_spec_created", "status": True},
            {"item": "proxy_metrics_and_unknowns_defined", "status": True},
            {"item": "next_benchmark_linked_slice_named", "status": True},
            {"item": "narrow_commit_created_and_pushed_if_push_gate_passes", "status": "pending_until_git_gate"},
        ],
        "artifact_readiness": [
            {"item": "benchmark_json_exists", "status": True},
            {"item": "human_doc_exists", "status": True},
            {"item": "proxy_metrics_present", "status": True},
            {"item": "unmeasurable_audience_acceptance_boundary_present", "status": True},
            {"item": "review_protocol_present", "status": True},
            {"item": "downstream_next_use_described", "status": True},
        ],
        "render_gate_hygiene": [
            {"item": "no_render_performed", "status": True},
            {"item": "render_not_used_for_vague_visual_guessing", "status": True},
            {"item": "next_render_tied_to_benchmark_linked_material_change", "status": True},
            {"item": "no_render_for_docs_benchmark_only_change", "status": True},
            {"item": "repeated_render_loop_avoided", "status": True},
            {"item": "output_first_principle_preserved", "status": True},
        ],
        "human_burden_hygiene": [
            {"item": "user_input", "status": "freeform"},
            {"item": "template_required", "status": False},
            {"item": "schema_owner", "status": "Agent/Supervisor"},
            {"item": "user_side_work_for_this_slice", "status": "none"},
            {"item": "future_review_look_for_count", "status": 3},
            {"item": "negative_confirmation_checklist", "status": False},
            {"item": "fixed_form_relapse", "status": False},
        ],
        "review_non_redundancy": [
            {"item": "latest_user_correction_consumed_once", "status": True},
            {"item": "prior_visual_reviews_reused", "status": True},
            {"item": "next_axis_stated_as_benchmark", "status": True},
            {"item": "not_accepted_scope_preserved", "status": True},
            {"item": "repeated_user_review_requested", "status": False},
            {"item": "mechanics_re_review_requested", "status": False},
        ],
        "inertia_check": [
            {"item": "ad_hoc_visual_iteration_stopped", "status": True},
            {"item": "packet_for_packet_drift", "status": False},
            {"item": "readback_only_stall", "status": False},
            {"item": "readiness_separated_from_slice_completion", "status": True},
            {"item": "next_concrete_benchmark_linked_milestone", "status": NEXT_DEFAULT_SLICE},
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
            "default_slice": NEXT_DEFAULT_SLICE,
            "instruction": "score the current cards against the proxy metrics before any further visual redesign",
            "evaluation_subject": "current four diagnostic SVG/PNG cards",
            "refinement_gate": "only concrete benchmark failures may drive a later benchmarked refinement",
        },
    }


def render_newsroom_visual_audience_fit_benchmark_markdown(
    benchmark: dict[str, Any],
) -> str:
    """Render a compact human-readable benchmark document."""
    lines = [
        "# Newsroom Visual Audience-Fit Benchmark v1",
        "",
        f"artifact_id: {benchmark['artifact_id']}",
        f"benchmark_id: {benchmark['benchmark_id']}",
        f"schema_version: {benchmark['schema_version']}",
        f"benchmark_status: {benchmark['benchmark_status']}",
        f"production_status: {benchmark['production_status']}",
        "",
        "## Purpose",
        "",
        "This benchmark prevents additional ad hoc visual tweaking. It defines proxy criteria for whether the current fake/review-only newsroom cards are understandable for a general explanatory YouTube viewer. It is not a card redesign, YMM4 render, .ymmp edit, production approval, public-readiness claim, real newsroom intake, external reference scrape, or audience acceptance proof.",
        "",
        "## Target Audience Assumption",
        "",
    ]
    target = benchmark["target_audience_assumption"]
    lines.extend(
        [
            f"- assumed_audience: {', '.join(target['assumed_audience'])}",
            f"- viewing_context: {target['viewing_context']}",
            f"- attention_level: {target['attention_level']}",
            f"- device_screen_assumption: {target['device_screen_assumption']}",
            "",
            "## Visual Job-To-Be-Done",
            "",
        ]
    )
    job = benchmark["visual_job_to_be_done"]
    lines.extend([f"- helps_viewer: {', '.join(job['helps_viewer'])}"])
    lines.extend(
        [
            f"- dominant_message: {job['dominant_message']}",
            f"- non_goals: {', '.join(job['non_goals'])}",
            "",
            "## Evidence Level",
            "",
        ]
    )
    evidence = benchmark["evidence_level"]
    lines.extend(
        [
            f"- current_level: {evidence['current_level']}",
            f"- evidence: {', '.join(evidence['evidence'])}",
            f"- evidence_not_yet: {', '.join(evidence['evidence_not_yet'])}",
            f"- unknowns: {', '.join(evidence['unknowns'])}",
            "",
            "## Reference / Benchmark Abstraction",
            "",
        ]
    )
    reference = benchmark["reference_benchmark_abstraction"]
    lines.extend(
        [
            f"- reference_pack_status: {reference['reference_pack_status']}",
            f"- no_copy_policy: {reference['no_copy_policy']}",
            f"- candidate_reference_types: {', '.join(reference['candidate_reference_types'])}",
            f"- extracted_grammar_hypotheses: {', '.join(reference['extracted_grammar_hypotheses'])}",
            f"- hypotheses_not_market_proof: {reference['hypotheses_not_market_proof']}",
            "",
            "## Proxy Metrics",
            "",
            "| metric | pass | fail | unknown |",
            "|---|---|---|---|",
        ]
    )
    for metric in benchmark["proxy_metrics"]:
        lines.append(
            "| {metric_id} | {pass_} | {fail} | {unknown} |".format(
                metric_id=metric["metric_id"],
                pass_=metric["pass"],
                fail=metric["fail"],
                unknown=metric["unknown"],
            )
        )
    lines.extend(["", "## Acceptance Criteria", ""])
    criteria = benchmark["acceptance_criteria"]
    lines.extend(
        [
            f"- must: {', '.join(criteria['must'])}",
            f"- should: {', '.join(criteria['should'])}",
            f"- must_not: {', '.join(criteria['must_not'])}",
            "",
            "## Next Visual Iteration Mapping",
            "",
            "| future change | benchmark criteria |",
            "|---|---|",
        ]
    )
    for row in benchmark["next_visual_iteration_mapping"]:
        lines.append(f"| {row['future_change']} | {', '.join(row['criteria'])} |")
    protocol = benchmark["review_protocol"]
    lines.extend(
        [
            "",
            "## Review Protocol",
            "",
            f"- ask_user_after: {', '.join(protocol['ask_user_after'])}",
            f"- look_for: {', '.join(protocol['look_for'])}",
            f"- answer_style: {protocol['answer_style']}",
            f"- schema_owner: {protocol['schema_owner']}",
            f"- form_required: {protocol['form_required']}",
            "",
            "## Visual Benchmark Gate",
            "",
        ]
    )
    gate = benchmark["visual_benchmark_gate"]
    lines.extend(
        [
            f"- status: {gate['status']}",
            f"- visual_work_class: {gate['visual_work_class']}",
            f"- benchmark_status: {gate['benchmark_status']}",
            f"- evidence_level: {gate['evidence_level']}",
            f"- proxy_metrics: {gate['proxy_metrics']['metric_count']} defined, current_cards_evaluated={gate['proxy_metrics']['current_cards_evaluated']}",
            f"- unknowns: {', '.join(gate['unknowns'])}",
            f"- next_iteration_allowed: {gate['next_iteration_allowed']}",
            f"- next_iteration_allowed_scope: {gate['next_iteration_allowed_scope']}",
            f"- visual_refinement_allowed_before_evaluation: {gate['visual_refinement_allowed_before_evaluation']}",
            "",
            "## Recommended Next Slice",
            "",
            f"- default: {benchmark['recommended_next_slice']['slice']}",
            f"- reason: {benchmark['recommended_next_slice']['reason']}",
            "",
            "## Alternative Next Slices",
            "",
            "| slice | condition |",
            "|---|---|",
        ]
    )
    for row in benchmark["alternative_next_slices"]:
        lines.append(f"| {row['slice']} | {row['condition']} |")
    _append_status_table(lines, "Completion Matrix", benchmark["completion_matrix"])
    _append_status_table(lines, "Artifact Readiness", benchmark["artifact_readiness"])
    _append_status_table(lines, "Render Gate Hygiene", benchmark["render_gate_hygiene"])
    _append_status_table(
        lines,
        "Human Burden Hygiene",
        benchmark["human_burden_hygiene"],
    )
    _append_status_table(
        lines,
        "Review Non-Redundancy",
        benchmark["review_non_redundancy"],
    )
    _append_status_table(lines, "Inertia Check", benchmark["inertia_check"])
    lines.extend(
        [
            "",
            "## Boundary",
            "",
        ]
    )
    for key in sorted(benchmark["boundaries"]):
        value = benchmark["boundaries"][key]
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Downstream Next Use",
            "",
            f"- default_slice: {benchmark['downstream_next_use']['default_slice']}",
            f"- instruction: {benchmark['downstream_next_use']['instruction']}",
            f"- evaluation_subject: {benchmark['downstream_next_use']['evaluation_subject']}",
            f"- refinement_gate: {benchmark['downstream_next_use']['refinement_gate']}",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    sources: dict[str, dict[str, Any]],
    *,
    card_asset_count: int,
) -> dict[str, Any]:
    errors: list[str] = []
    audience_refinement = sources["audience_fit_refinement"]
    audience_review = sources["audience_fit_review_readback"]
    internal_review = sources["internal_review_prep"]
    render_readback = sources["card_placement_render_readback"]
    post_refinement_package = sources["post_refinement_render_package"]

    if audience_refinement.get("refinement_status") != "assets_regenerated":
        errors.append("audience_fit_refinement_not_regenerated")
    if audience_refinement.get("production_status") != "diagnostic_only":
        errors.append("audience_fit_refinement_not_diagnostic_only")
    if audience_review.get("audience_fit_review_normalization", {}).get(
        "recommended_next_axis"
    ) != "visual_card_audience_fit_refinement":
        errors.append("audience_fit_review_axis_missing")
    if audience_review.get("audience_fit_review_normalization", {}).get(
        "production_visual_quality_accepted"
    ) is not False:
        errors.append("production_visual_quality_boundary_missing")
    if internal_review.get("benchmark_baseline", {}).get("fake_card_count") != 4:
        errors.append("internal_review_fake_card_count_not_four")
    if render_readback.get("result_status") != "pass":
        errors.append("prior_card_render_readback_not_pass")
    if post_refinement_package.get("smoke_status") != "prepared_not_run":
        errors.append("post_refinement_render_package_not_prepared_not_run")
    if card_asset_count != 8:
        errors.append("expected_four_svg_and_four_png_card_assets")

    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "source_audience_fit_refinement_status": audience_refinement.get(
            "refinement_status"
        ),
        "source_audience_fit_review_status": audience_review.get("review_status"),
        "source_internal_review_prep_status": internal_review.get("review_status"),
        "source_card_render_result_status": render_readback.get("result_status"),
        "post_refinement_render_package_status": post_refinement_package.get(
            "package_status"
        ),
        "current_card_asset_count": card_asset_count,
    }


def _card_asset_count(path: Path) -> int:
    if not path.exists():
        return 0
    return len(list(path.glob("*.svg"))) + len(list(path.glob("*.png")))


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
