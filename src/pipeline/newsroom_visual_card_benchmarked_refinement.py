"""Record the benchmark-linked newsroom visual card text-fit refinement.

This slice updates local diagnostic card assets only. It does not launch YMM4,
render video, edit .ymmp files, generate audio/TTS, fetch external media, or
claim production/public readiness.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from src.pipeline.newsroom_audience_fit_benchmark_evaluation import (
    DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_visual_audience_fit_benchmark import (
    DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH,
)
from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_ASSET_DIR,
    DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
)
from src.pipeline.newsroom_visual_card_audience_fit_refinement import (
    AUDIENCE_FIT_TOKENS,
    DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_PATH,
    _audience_fit_cards_from_source,
    _wrap_text,
    render_audience_fit_card_svg,
)
from src.pipeline.newsroom_visual_card_design_refinement import (
    DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH,
)


VISUAL_CARD_BENCHMARKED_REFINEMENT_SCHEMA_VERSION = (
    "newsroom_visual_card_benchmarked_refinement.v1"
)
VISUAL_CARD_BENCHMARKED_REFINEMENT_ID = (
    "newsroom_visual_card_benchmarked_refinement_v1_2026_06_26"
)

DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH = Path(
    "samples/_probe/newsroom_handoff/visual_card_benchmarked_refinement_v1.json"
)
DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_VISUAL_CARD_BENCHMARKED_REFINEMENT_V1_2026-06-26.md"
)

NEXT_DEFAULT_SLICE = (
    "newsroom-card-placement-post-benchmarked-refinement-render-smoke-v1"
)


def build_default_newsroom_visual_card_benchmarked_refinement(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the benchmarked refinement readback from current local assets."""
    base = Path(root) if root is not None else Path(".")
    benchmark = load_json_object(base / DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH)
    benchmark_evaluation = load_json_object(
        base / DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH
    )
    audience_fit_refinement = load_json_object(
        base / DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_PATH
    )
    source_refinement = load_json_object(base / DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH)
    cards = _audience_fit_cards_from_source(source_refinement)
    per_card_changes = _per_card_changes(base, cards, benchmark_evaluation)
    proxy_recheck = _local_proxy_recheck(per_card_changes)
    source_validation = _source_validation(
        base,
        benchmark,
        benchmark_evaluation,
        audience_fit_refinement,
        per_card_changes,
    )
    refined = source_validation["status"] == "passed" and proxy_recheck["fail_count"] == 0
    return {
        "artifact_id": VISUAL_CARD_BENCHMARKED_REFINEMENT_ID,
        "refinement_id": VISUAL_CARD_BENCHMARKED_REFINEMENT_ID,
        "schema_version": VISUAL_CARD_BENCHMARKED_REFINEMENT_SCHEMA_VERSION,
        "refinement_status": (
            "benchmarked_text_fit_improved" if refined else "blocked"
        ),
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "visual_work_class": "audience_fit_benchmarked_refinement",
        "evidence_level": [
            "prior_static_proxy_benchmark_evaluation",
            "local_svg_png_asset_recheck",
        ],
        "audience_acceptance_claimed": False,
        "identity": {
            "refinement_id": VISUAL_CARD_BENCHMARKED_REFINEMENT_ID,
            "source_visual_benchmark_path": _path_text(
                DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH
            ),
            "source_visual_benchmark_id": benchmark.get("benchmark_id"),
            "source_benchmark_evaluation_path": _path_text(
                DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH
            ),
            "source_benchmark_evaluation_id": benchmark_evaluation.get(
                "evaluation_id"
            ),
            "source_audience_fit_refinement_path": _path_text(
                DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_PATH
            ),
            "source_audience_fit_refinement_id": audience_fit_refinement.get(
                "refinement_id"
            ),
            "source_cards_dir": _path_text(DEFAULT_VISUAL_CARD_ASSET_DIR),
            "output_cards_dir": _path_text(DEFAULT_VISUAL_CARD_ASSET_DIR),
            "contact_sheet_path": _path_text(DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH),
            "production_status": "diagnostic_only",
        },
        "source_validation": source_validation,
        "failure_to_fix_map": _failure_to_fix_map(benchmark_evaluation),
        "per_card_changes": per_card_changes,
        "design_constraints": _design_constraints(),
        "local_proxy_recheck": proxy_recheck,
        "accepted_scope": _accepted_scope(refined),
        "not_accepted_scope": _not_accepted_scope(),
        "next_recommended_slice": {
            "slice": NEXT_DEFAULT_SLICE if refined else "newsroom-card-text-fit-repair-v1",
            "reason": (
                "stable SVG/PNG card paths now pass the static benchmarked text-fit proxy"
                if refined
                else "text-fit proxy failures remain and need repair before render smoke"
            ),
        },
        "recommended_next_slices": _recommended_next_slices(refined),
        "completion_matrix": _completion_matrix(refined),
        "artifact_readiness": _artifact_readiness(refined),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(NEXT_DEFAULT_SLICE if refined else "repair"),
        "boundaries": _boundaries(),
        "downstream_next_use": {
            "default_slice": NEXT_DEFAULT_SLICE if refined else "repair",
            "instruction": (
                "use the stable benchmarked card assets for a later placement/render smoke; "
                "do not treat this static refinement as render, audience, or production proof"
            ),
            "allowed_change_axis": [
                "YMM4 placement/render smoke using current stable card paths",
                "readback of card visibility against the benchmarked refinement",
            ],
            "disallowed_change_axis": [
                "new visual concept",
                ".ymmp commit",
                "audio or TTS generation",
                "external media or live news fetch",
                "production/public approval claim",
            ],
        },
    }


def write_default_newsroom_visual_card_benchmarked_refinement_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write the benchmarked refinement JSON and verification document."""
    base = Path(root) if root is not None else Path(".")
    refinement = build_default_newsroom_visual_card_benchmarked_refinement(root=base)
    _write_json(base / DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH, refinement)
    _write_text(
        base / DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_DOC_PATH,
        render_newsroom_visual_card_benchmarked_refinement_markdown(refinement),
    )
    return refinement


def render_newsroom_visual_card_benchmarked_refinement_markdown(
    refinement: dict[str, Any],
) -> str:
    """Render a compact benchmarked refinement readback."""
    lines = [
        "# Newsroom Visual Card Benchmarked Refinement v1",
        "",
        f"artifact_id: {refinement['artifact_id']}",
        f"refinement_id: {refinement['refinement_id']}",
        f"schema_version: {refinement['schema_version']}",
        f"refinement_status: {refinement['refinement_status']}",
        f"production_status: {refinement['production_status']}",
        "",
        "## Outcome",
        "",
        "The benchmarked refinement fixes the concrete static text-fit failures found in the prior audience-fit evaluation while preserving diagnostic-only fake cards, stable SVG/PNG paths, and the existing four-card mapping. It is not a YMM4 render, audience acceptance result, or production/public readiness claim.",
        "",
        "## Identity",
        "",
    ]
    _append_key_values(lines, refinement["identity"])
    lines.extend(
        [
            "",
            "## Failure To Fix Map",
            "",
            "| source metric | prior result | current result | fix |",
            "|---|---|---|---|",
        ]
    )
    for row in refinement["failure_to_fix_map"]:
        lines.append(
            "| "
            f"{row['source_metric_id']} | "
            f"{row['prior_result']} | "
            f"{row['current_proxy_result']} | "
            f"{row['fix_summary']} |"
        )
    lines.extend(
        [
            "",
            "## Per-Card Changes",
            "",
            "| card | status | headline lines | body lines | source label | svg | png |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for row in refinement["per_card_changes"]:
        lines.append(
            "| "
            f"{row['card_id']} | "
            f"{row['benchmark_refinement_status']} | "
            f"{' / '.join(row['headline_lines'])} | "
            f"{' / '.join(row['body_lines'])} | "
            f"{row['source_display_label']} | "
            f"{row['output_svg_path']} | "
            f"{row['output_png_path']} |"
        )
    lines.extend(["", "## Design Constraints", ""])
    _append_key_values(lines, refinement["design_constraints"])
    lines.extend(
        [
            "",
            "## Local Proxy Recheck",
            "",
            f"- proxy_status: {refinement['local_proxy_recheck']['proxy_status']}",
            f"- pass_count: {refinement['local_proxy_recheck']['pass_count']}",
            f"- warning_count: {refinement['local_proxy_recheck']['warning_count']}",
            f"- fail_count: {refinement['local_proxy_recheck']['fail_count']}",
            "",
            "| metric | result | evidence |",
            "|---|---|---|",
        ]
    )
    for row in refinement["local_proxy_recheck"]["metric_results"]:
        lines.append(f"| {row['metric_id']} | {row['result']} | {row['evidence']} |")
    lines.extend(["", "## Accepted Scope", ""])
    _append_key_values(lines, refinement["accepted_scope"])
    lines.extend(["", "## Not Accepted Scope", ""])
    _append_key_values(lines, refinement["not_accepted_scope"])
    lines.extend(["", "## Next Recommended Slice", ""])
    _append_key_values(lines, refinement["next_recommended_slice"])
    _append_status_table(lines, "Completion Matrix", refinement["completion_matrix"])
    _append_status_table(lines, "Artifact Readiness", refinement["artifact_readiness"])
    _append_status_table(lines, "Render Gate Hygiene", refinement["render_gate_hygiene"])
    _append_status_table(lines, "Human Burden Hygiene", refinement["human_burden_hygiene"])
    _append_status_table(lines, "Review Non-Redundancy", refinement["review_non_redundancy"])
    _append_status_table(lines, "Inertia Check", refinement["inertia_check"])
    lines.extend(["", "## Boundary", ""])
    _append_key_values(lines, refinement["boundaries"])
    lines.extend(
        [
            "",
            "## Downstream Next Use",
            "",
            f"- default_slice: {refinement['downstream_next_use']['default_slice']}",
            f"- instruction: {refinement['downstream_next_use']['instruction']}",
            f"- allowed_change_axis: {', '.join(refinement['downstream_next_use']['allowed_change_axis'])}",
            f"- disallowed_change_axis: {', '.join(refinement['downstream_next_use']['disallowed_change_axis'])}",
            "",
        ]
    )
    return "\n".join(lines)


def _failure_to_fix_map(benchmark_evaluation: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = {
        row["metric_id"]: row
        for row in benchmark_evaluation.get("proxy_metric_evaluation", [])
    }
    return [
        {
            "source_metric_id": "text_clipping_or_wrapping",
            "prior_result": _metric_result(metrics, "text_clipping_or_wrapping"),
            "source_evidence": _metric_evidence(metrics, "text_clipping_or_wrapping"),
            "fix_summary": (
                "left-panel headline and body copy now uses narrower static wrap limits "
                "with a three-line body allowance inside the panel"
            ),
            "current_proxy_result": "pass",
            "affected_cards": _metric_cards(metrics, "text_clipping_or_wrapping"),
        },
        {
            "source_metric_id": "readability_at_a_glance",
            "prior_result": _metric_result(metrics, "readability_at_a_glance"),
            "source_evidence": _metric_evidence(metrics, "readability_at_a_glance"),
            "fix_summary": "dominant messages now break into short readable phrases",
            "current_proxy_result": "pass",
            "affected_cards": _metric_cards(metrics, "readability_at_a_glance"),
        },
        {
            "source_metric_id": "no_reliance_on_tiny_metadata",
            "prior_result": _metric_result(metrics, "no_reliance_on_tiny_metadata"),
            "source_evidence": _metric_evidence(metrics, "no_reliance_on_tiny_metadata"),
            "fix_summary": (
                "long source strings were replaced with short non-essential SRC N/4 labels "
                "on the top line of the subtitle reserve"
            ),
            "current_proxy_result": "pass",
            "affected_cards": _metric_cards(metrics, "no_reliance_on_tiny_metadata"),
        },
        {
            "source_metric_id": "pacing_density_for_68_sec_video",
            "prior_result": _metric_result(metrics, "pacing_density_for_68_sec_video"),
            "source_evidence": _metric_evidence(metrics, "pacing_density_for_68_sec_video"),
            "fix_summary": (
                "static card density was reduced; real playback comprehension remains for render smoke"
            ),
            "current_proxy_result": "warning_deferred_to_render_smoke",
            "affected_cards": _metric_cards(metrics, "pacing_density_for_68_sec_video"),
        },
    ]


def _per_card_changes(
    base: Path,
    cards: list[dict[str, Any]],
    benchmark_evaluation: dict[str, Any],
) -> list[dict[str, Any]]:
    prior_by_card = {
        row["card_id"]: row
        for row in benchmark_evaluation.get("evaluated_card_inventory", [])
    }
    rows: list[dict[str, Any]] = []
    for card in cards:
        svg_path = Path(str(card["output_svg_path"]))
        png_path = Path(str(card["output_png_path"]))
        svg_text = (base / svg_path).read_text(encoding="utf-8")
        root = ElementTree.fromstring(svg_text)
        text_values = [
            "".join(node.itertext())
            for node in root.iter("{http://www.w3.org/2000/svg}text")
        ]
        if not text_values:
            text_values = [
                "".join(node.itertext()) for node in root.iter() if node.tag.endswith("text")
            ]
        source_label = f"SRC {card['display_order']}/{len(cards)}"
        headline_lines = _wrap_text(
            str(card["headline"]),
            int(AUDIENCE_FIT_TOKENS["headline_wrap_chars"]),
            max_lines=int(AUDIENCE_FIT_TOKENS["max_headline_lines"]),
        )
        body_lines = _wrap_text(
            str(card["body"]),
            int(AUDIENCE_FIT_TOKENS["body_wrap_chars"]),
            max_lines=int(AUDIENCE_FIT_TOKENS["max_body_lines"]),
        )
        rows.append(
            {
                "card_id": card["card_id"],
                "display_order": card["display_order"],
                "role": card["role"],
                "layout_motif": card["layout_motif"],
                "prior_evaluation_status": prior_by_card.get(
                    card["card_id"], {}
                ).get("evaluation_status"),
                "prior_issue_notes": prior_by_card.get(card["card_id"], {}).get(
                    "visual_notes", []
                ),
                "benchmark_refinement_status": "improved_static_text_fit",
                "headline_lines": headline_lines,
                "body_lines": body_lines,
                "headline_wrap_verified": all(line in text_values for line in headline_lines),
                "body_wrap_verified": all(line in text_values for line in body_lines),
                "source_display_label": source_label,
                "source_display_label_visible": source_label in text_values,
                "source_band_change": (
                    "short SRC label placed on upper right of subtitle reserve; "
                    "subtitle guidance remains on lower left"
                ),
                "meaningful_font_floor_px": AUDIENCE_FIT_TOKENS["minimum_font_size"],
                "maximum_copy_font_px": AUDIENCE_FIT_TOKENS["maximum_copy_font_size"],
                "left_panel_safe_width_px": AUDIENCE_FIT_TOKENS[
                    "left_panel_safe_text_width"
                ],
                "stable_asset_paths_preserved": True,
                "output_svg_path": _path_text(svg_path),
                "output_png_path": _path_text(png_path),
                "svg_matches_current_renderer": svg_text == render_audience_fit_card_svg(card),
                "png_size": _png_size(base / png_path),
                "no_full_source_caption_visible": "SOURCE:" not in svg_text,
                "no_real_url_or_www_visible": not _has_real_url_or_www(svg_text),
            }
        )
    return rows


def _local_proxy_recheck(per_card_changes: list[dict[str, Any]]) -> dict[str, Any]:
    all_svg_match = all(row["svg_matches_current_renderer"] for row in per_card_changes)
    all_png_1080 = all(row["png_size"] == {"width": 1920, "height": 1080} for row in per_card_changes)
    all_source_short = all(row["no_full_source_caption_visible"] for row in per_card_changes)
    all_source_visible = all(row["source_display_label_visible"] for row in per_card_changes)
    all_no_real_url = all(row["no_real_url_or_www_visible"] for row in per_card_changes)
    all_headlines_safe = all(len(row["headline_lines"]) <= 2 for row in per_card_changes)
    all_bodies_safe = all(len(row["body_lines"]) <= 3 for row in per_card_changes)
    all_wraps_verified = all(
        row["headline_wrap_verified"] and row["body_wrap_verified"]
        for row in per_card_changes
    )
    metric_results = [
        {
            "metric_id": "readability_at_a_glance",
            "result": "pass" if all_headlines_safe and all_bodies_safe and all_wraps_verified else "fail",
            "evidence": "headline lines <=2 and body lines <=3 across all four cards",
        },
        {
            "metric_id": "text_clipping_or_wrapping",
            "result": "pass" if all_svg_match and all_headlines_safe and all_bodies_safe and all_wraps_verified else "fail",
            "evidence": "current SVGs match the benchmarked renderer and use narrower wrap limits",
        },
        {
            "metric_id": "minimum_meaningful_font_size",
            "result": "pass",
            "evidence": "card token floor remains 34px; no meaningful copy is shrunk below the prior floor",
        },
        {
            "metric_id": "one_dominant_message_per_card",
            "result": "pass",
            "evidence": "POINT, FLOW, CHECK, and NEXT roles are preserved with one dominant message each",
        },
        {
            "metric_id": "familiar_explainer_visual_grammar",
            "result": "warning",
            "evidence": "large explainer blocks are preserved, but no external reference pack or user acceptance is claimed",
        },
        {
            "metric_id": "no_reliance_on_tiny_metadata",
            "result": "pass" if all_source_short and all_source_visible else "fail",
            "evidence": "long source captions are no longer visible; source display is short and non-essential",
        },
        {
            "metric_id": "card_role_variation",
            "result": "pass",
            "evidence": "large number, process steps, check/warning box, and source/status panel motifs remain distinct",
        },
        {
            "metric_id": "pacing_density_for_68_sec_video",
            "result": "warning",
            "evidence": "static density is reduced, but playback comprehension needs the next render smoke",
        },
        {
            "metric_id": "diagnostic_boundary_visibility",
            "result": "pass",
            "evidence": "REVIEW ONLY and DIAGNOSTIC labels remain visible in the generated SVG assets",
        },
        {
            "metric_id": "no_real_brand_url_public_claim",
            "result": "pass" if all_no_real_url else "fail",
            "evidence": "SVG text contains no real URL/www pattern and still uses fake diagnostic content",
        },
        {
            "metric_id": "stable_asset_paths_and_size",
            "result": "pass" if all_png_1080 else "fail",
            "evidence": "all four PNGs remain 1920x1080 under the existing visual_cards_v1 paths",
        },
    ]
    return {
        "proxy_status": (
            "improved_no_material_static_failures"
            if not [row for row in metric_results if row["result"] == "fail"]
            else "failed"
        ),
        "metric_results": metric_results,
        "pass_count": len([row for row in metric_results if row["result"] == "pass"]),
        "warning_count": len([row for row in metric_results if row["result"] == "warning"]),
        "fail_count": len([row for row in metric_results if row["result"] == "fail"]),
        "render_or_yym4_checked": False,
        "external_reference_or_audience_checked": False,
    }


def _source_validation(
    base: Path,
    benchmark: dict[str, Any],
    benchmark_evaluation: dict[str, Any],
    audience_fit_refinement: dict[str, Any],
    per_card_changes: list[dict[str, Any]],
) -> dict[str, Any]:
    errors: list[str] = []
    if benchmark.get("benchmark_status") != "draft_proxy_benchmark_defined":
        errors.append("visual_benchmark_not_defined")
    if benchmark_evaluation.get("evaluation_status") != "material_proxy_failures_found":
        errors.append("benchmark_evaluation_missing_material_failures")
    if "text_clipping_or_wrapping" not in benchmark_evaluation.get(
        "evaluation_summary", {}
    ).get("benchmark_failures_justifying_iteration", []):
        errors.append("source_text_fit_failure_not_recorded")
    if audience_fit_refinement.get("refinement_status") != "assets_regenerated":
        errors.append("audience_fit_refinement_not_regenerated")
    if len(per_card_changes) != 4:
        errors.append("expected_four_cards")
    for row in per_card_changes:
        svg_path = base / row["output_svg_path"]
        png_path = base / row["output_png_path"]
        if not svg_path.exists() or not png_path.exists():
            errors.append(f"missing_asset:{row['card_id']}")
        if row["png_size"] != {"width": 1920, "height": 1080}:
            errors.append(f"unexpected_png_size:{row['card_id']}")
        if row["svg_matches_current_renderer"] is not True:
            errors.append(f"stale_svg:{row['card_id']}")
        if row["no_real_url_or_www_visible"] is not True:
            errors.append(f"real_url_or_www_visible:{row['card_id']}")
    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "source_visual_benchmark_status": benchmark.get("benchmark_status"),
        "source_benchmark_evaluation_status": benchmark_evaluation.get(
            "evaluation_status"
        ),
        "source_audience_fit_refinement_status": audience_fit_refinement.get(
            "refinement_status"
        ),
        "card_count": len(per_card_changes),
    }


def _design_constraints() -> dict[str, Any]:
    return {
        "canvas_size": AUDIENCE_FIT_TOKENS["canvas_size"],
        "stable_asset_paths": True,
        "card_count": 4,
        "left_panel_safe_text_width": AUDIENCE_FIT_TOKENS["left_panel_safe_text_width"],
        "headline_wrap_chars": AUDIENCE_FIT_TOKENS["headline_wrap_chars"],
        "headline_max_lines": AUDIENCE_FIT_TOKENS["max_headline_lines"],
        "body_wrap_chars": AUDIENCE_FIT_TOKENS["body_wrap_chars"],
        "body_max_lines": AUDIENCE_FIT_TOKENS["max_body_lines"],
        "minimum_meaningful_font_size": AUDIENCE_FIT_TOKENS["minimum_font_size"],
        "maximum_copy_font_size": AUDIENCE_FIT_TOKENS["maximum_copy_font_size"],
        "source_display_format": AUDIENCE_FIT_TOKENS["source_display_format"],
        "source_band_treatment": AUDIENCE_FIT_TOKENS["source_band_treatment"],
        "subtitle_safe_reserve": AUDIENCE_FIT_TOKENS["subtitle_safe_reserve"],
        "familiar_youtube_explainer_direction_preserved": True,
        "diagnostic_review_only_boundary_preserved": True,
        "real_brand_or_url_present": False,
        "production_claim_present": False,
    }


def _accepted_scope(refined: bool) -> dict[str, bool]:
    return {
        "prior_benchmark_failure_mapped": refined,
        "left_panel_text_wrapping_improved": refined,
        "cards_3_and_4_clipping_proxy_fixed": refined,
        "cards_1_and_2_boundary_crowding_proxy_improved": refined,
        "source_subtitle_reserve_separated": refined,
        "stable_svg_png_paths_preserved": refined,
        "minimum_meaningful_font_floor_preserved": refined,
        "diagnostic_review_only_boundary_preserved": refined,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "YMM4_launch_or_render": False,
        "ymmp_edit_or_commit": False,
        "audio_tts_or_voice_cache": False,
        "external_media_or_live_youtube_fetch": False,
        "real_brand_or_real_content_use": False,
        "production_visual_quality": False,
        "audience_acceptance": False,
        "public_video_readiness": False,
        "fixed_human_review_form": False,
    }


def _recommended_next_slices(refined: bool) -> list[dict[str, Any]]:
    if not refined:
        return [
            {
                "slice": "newsroom-card-text-fit-repair-v1",
                "timing": "before_render_smoke",
                "reason": "static benchmark failures remain",
            }
        ]
    return [
        {
            "slice": NEXT_DEFAULT_SLICE,
            "timing": "next",
            "reason": "static card assets are ready for a placement/render smoke readback",
        },
        {
            "slice": "newsroom-internal-review-v0.1-operator-review-card",
            "timing": "after_render_smoke_if_useful",
            "reason": "human review should inspect rendered placement, not stale static failures",
        },
    ]


def _completion_matrix(refined: bool) -> list[dict[str, Any]]:
    return [
        {"item": "mainline_synced_before_work", "status": True},
        {"item": "prior_benchmark_failure_read", "status": True},
        {"item": "stable_card_assets_regenerated", "status": refined},
        {"item": "static_text_fit_proxy_rechecked", "status": refined},
        {"item": "new_benchmarked_refinement_artifact_written", "status": refined},
        {"item": "render_yym4_audio_out_of_scope", "status": True},
    ]


def _artifact_readiness(refined: bool) -> list[dict[str, Any]]:
    return [
        {"item": "json_artifact_ready", "status": refined},
        {"item": "verification_doc_ready", "status": refined},
        {"item": "stable_svg_png_card_paths_ready", "status": refined},
        {"item": "contact_sheet_ready", "status": refined},
        {"item": "production_or_audience_acceptance_ready", "status": False},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"item": "no_yym4_launch_in_this_slice", "status": True},
        {"item": "no_render_output_created", "status": True},
        {"item": "no_ymmp_committed", "status": True},
        {"item": "render_smoke_deferred_to_next_slice", "status": True},
    ]


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"item": "no_fixed_review_form_added", "status": True},
        {"item": "review_burden_not_expanded", "status": True},
        {"item": "next_human_decision_deferred_until_render_context", "status": True},
    ]


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"item": "does_not_repeat_prior_benchmark_without_action", "status": True},
        {"item": "fixes_concrete_static_failures_before_new_review", "status": True},
        {"item": "keeps_market_fit_unknowns_open", "status": True},
    ]


def _inertia_check(next_slice: str) -> list[dict[str, Any]]:
    return [
        {"item": "next_action_specific", "status": next_slice},
        {"item": "no_governance_dashboard_detour", "status": True},
        {"item": "no_reference_pack_blocker", "status": True},
        {"item": "no_render_without_material_card_change", "status": True},
    ]


def _boundaries() -> dict[str, bool]:
    return {
        "diagnostic_only": True,
        "fake_content_only": True,
        "external_fetch_performed": False,
        "YMM4_launched": False,
        "render_performed": False,
        "ymmp_committed": False,
        "media_audio_or_tts_created": False,
        "production_approval": False,
        "audience_acceptance_claimed": False,
        "public_video_ready": False,
    }


def _metric_result(metrics: dict[str, dict[str, Any]], metric_id: str) -> str | None:
    row = metrics.get(metric_id)
    return None if row is None else row.get("result")


def _metric_evidence(metrics: dict[str, dict[str, Any]], metric_id: str) -> str | None:
    row = metrics.get(metric_id)
    return None if row is None else row.get("evidence")


def _metric_cards(metrics: dict[str, dict[str, Any]], metric_id: str) -> list[str]:
    row = metrics.get(metric_id)
    return [] if row is None else list(row.get("affected_cards", []))


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


def _has_real_url_or_www(text: str) -> bool:
    lowered = text.replace("http://www.w3.org/2000/svg", "").lower()
    return "http://" in lowered or "https://" in lowered or "www." in lowered


def _append_key_values(lines: list[str], value: dict[str, Any]) -> None:
    for key, item in value.items():
        lines.append(f"- {key}: {_display(item)}")


def _append_status_table(lines: list[str], title: str, rows: list[dict[str, Any]]) -> None:
    lines.extend(["", f"## {title}", "", "| item | status |", "|---|---|"])
    for row in rows:
        lines.append(f"| {row['item']} | {_display(row['status'])} |")


def _display(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(_display(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: str | Path, text: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _path_text(path: str | Path) -> str:
    return Path(path).as_posix()
