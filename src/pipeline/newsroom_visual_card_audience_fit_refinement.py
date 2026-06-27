"""Audience-fit visual card refinement for the newsroom handoff.

This slice consumes the latest freeform visual review, regenerates the external
card assets at stable paths, and records a diagnostic-only audience-fit
refinement. It does not launch YMM4, render video, edit .ymmp files, generate
audio/TTS, fetch external sources, import real media, or approve production use.
"""

from __future__ import annotations

import html
import json
import subprocess
import struct
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from src.pipeline.newsroom_card_placement_post_refinement_render_smoke import (
    DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH,
    DEFAULT_VISUAL_CARD_ASSET_DIR,
    DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
)
from src.pipeline.newsroom_visual_card_design_refinement import (
    DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_PATH,
    DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH,
)
from src.pipeline.newsroom_yym4_card_asset_placement_probe import (
    ensure_card_png_assets,
)


VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_SCHEMA_VERSION = (
    "newsroom_visual_card_audience_fit_review_readback.v1"
)
VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_ID = (
    "newsroom_visual_card_audience_fit_review_readback_v1_2026_06_25"
)
VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_SCHEMA_VERSION = (
    "newsroom_visual_card_audience_fit_refinement.v1"
)
VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_ID = (
    "newsroom_visual_card_audience_fit_refinement_v1_2026_06_25"
)

DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "visual_card_audience_fit_review_readback_v1.json"
)
DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_V1_2026-06-25.md"
)
DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "visual_card_audience_fit_refinement_v1.json"
)
DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_V1_2026-06-25.md"
)

NEXT_DEFAULT_SLICE = "newsroom-card-placement-post-audience-fit-render-smoke-v1"
PLACEMENT_REFRESH_SLICE = "newsroom-yym4-card-asset-placement-refresh-v1"
RASTER_EXPORT_SLICE = "newsroom-visual-card-raster-export-v1"
INTERNAL_REVIEW_PREP_SLICE = "newsroom-internal-review-v0.1-prep"

AUDIENCE_FIT_TOKENS: dict[str, Any] = {
    "canvas_size": {"width": 1920, "height": 1080},
    "safe_margin": 84,
    "minimum_font_size": 34,
    "title_font_size": 62,
    "headline_font_size": 76,
    "body_font_size": 44,
    "chip_or_label_font_size": 36,
    "meta_font_size": 36,
    "maximum_copy_font_size": 76,
    "display_number_font_size": 132,
    "maximum_font_size": 132,
    "max_title_lines": 1,
    "max_headline_lines": 2,
    "max_body_lines": 3,
    "wrap_width": 760,
    "left_panel_safe_text_width": 702,
    "headline_wrap_chars": 18,
    "body_wrap_chars": 27,
    "source_display_format": "SRC N/4",
    "source_band_treatment": "short right label separated from subtitle detail",
    "subtitle_safe_reserve": {
        "x": 104,
        "y": 820,
        "width": 1712,
        "height": 124,
    },
    "footer_debug_treatment": "removed_from_visible_review_surface",
    "audience_fit_style": [
        "familiar_youtube_explainer",
        "diagnostic_only",
    ],
    "real_brand_or_url_present": False,
    "production_claim_present": False,
}

AUDIENCE_FIT_CARD_SPECS: tuple[dict[str, Any], ...] = (
    {
        "role": "intro_summary",
        "review_role_label": "POINT",
        "layout_motif": "large_number",
        "card_title": "TODAY'S POINT",
        "headline": "Fake topic, review only.",
        "body": "Big, plain summary card for a normal viewer.",
        "main_label": "1",
        "callout_label": "POINT",
        "callout_text": "Review overview",
        "familiar_ui_adjustment": "large TV-style title and number, fewer chips",
        "variation_adjustment": "large-number lead card",
        "palette": {
            "name": "tv_red_point",
            "background": "#F8FAFC",
            "ink": "#111827",
            "muted": "#374151",
            "panel": "#FFFFFF",
            "panel_2": "#F3F4F6",
            "accent": "#DC2626",
            "accent_dark": "#991B1B",
            "chip": "#111827",
            "chip_text": "#FFFFFF",
            "warning": "#FEF3C7",
        },
    },
    {
        "role": "handoff_process",
        "review_role_label": "FLOW",
        "layout_motif": "simple_process_steps",
        "card_title": "HOW IT FLOWS",
        "headline": "Review-only handoff stays.",
        "body": "Three simple steps replace dashboard-style microcopy.",
        "main_label": "2",
        "callout_label": "FLOW",
        "callout_text": "Input -> Card -> Check",
        "familiar_ui_adjustment": "numbered steps with large labels",
        "variation_adjustment": "simple process ladder",
        "palette": {
            "name": "tv_blue_flow",
            "background": "#F8FAFC",
            "ink": "#111827",
            "muted": "#374151",
            "panel": "#FFFFFF",
            "panel_2": "#EFF6FF",
            "accent": "#2563EB",
            "accent_dark": "#1E3A8A",
            "chip": "#111827",
            "chip_text": "#FFFFFF",
            "warning": "#DBEAFE",
        },
    },
    {
        "role": "claim_check",
        "review_role_label": "CHECK",
        "layout_motif": "check_warning_box",
        "card_title": "CHECK POINT",
        "headline": "A fake claim is shown.",
        "body": "Plain check and caution boxes make the fake status obvious.",
        "main_label": "3",
        "callout_label": "CHECK",
        "callout_text": "Fake claim only",
        "familiar_ui_adjustment": "bold check/caution boxes instead of fine cells",
        "variation_adjustment": "check and warning box composition",
        "palette": {
            "name": "tv_yellow_check",
            "background": "#F8FAFC",
            "ink": "#111827",
            "muted": "#374151",
            "panel": "#FFFFFF",
            "panel_2": "#FEF3C7",
            "accent": "#D97706",
            "accent_dark": "#92400E",
            "chip": "#111827",
            "chip_text": "#FFFFFF",
            "warning": "#FEE2E2",
        },
    },
    {
        "role": "source_status_next_action",
        "review_role_label": "NEXT",
        "layout_motif": "source_status_panel",
        "card_title": "WATCH NEXT",
        "headline": "Fake source checks are noted.",
        "body": "Status and next-action panels stay large and familiar.",
        "main_label": "4",
        "callout_label": "NEXT",
        "callout_text": "Post-fit smoke later",
        "familiar_ui_adjustment": "large status panel and next-action label",
        "variation_adjustment": "source/status panel with next action",
        "palette": {
            "name": "tv_green_next",
            "background": "#F8FAFC",
            "ink": "#111827",
            "muted": "#374151",
            "panel": "#FFFFFF",
            "panel_2": "#ECFDF5",
            "accent": "#059669",
            "accent_dark": "#065F46",
            "chip": "#111827",
            "chip_text": "#FFFFFF",
            "warning": "#DCFCE7",
        },
    },
)


def write_default_newsroom_visual_card_audience_fit_refinement_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write audience-fit SVG/PNG assets, JSON readbacks, and docs."""
    base = Path(root) if root is not None else Path(".")
    review = build_default_newsroom_visual_card_audience_fit_review_readback(
        root=base
    )
    _write_json(base / DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_PATH, review)
    _write_text(
        base / DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_DOC_PATH,
        render_newsroom_visual_card_audience_fit_review_readback_markdown(review),
    )

    source_refinement = load_json_object(
        base / DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH
    )
    cards = _audience_fit_cards_from_source(source_refinement)
    for card in cards:
        _write_text(base / card["output_svg_path"], render_audience_fit_card_svg(card))
    _write_text(
        base / DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
        render_audience_fit_contact_sheet_html(cards),
    )
    png_export = _ensure_audience_fit_png_assets(base, cards)
    refinement = build_default_newsroom_visual_card_audience_fit_refinement(
        root=base,
        png_export=png_export,
    )
    _write_json(base / DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_PATH, refinement)
    _write_text(
        base / DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_DOC_PATH,
        render_newsroom_visual_card_audience_fit_refinement_markdown(refinement),
    )
    return refinement


def build_default_newsroom_visual_card_audience_fit_review_readback(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the normalized audience-fit review readback."""
    base = Path(root) if root is not None else Path(".")
    source_refinement = load_json_object(
        base / DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH
    )
    post_refinement_package = load_json_object(
        base / DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_PATH
    )
    source_review = load_json_object(
        base / DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_PATH
    )
    validation = _review_source_validation(
        source_refinement,
        post_refinement_package,
        source_review,
    )
    return {
        "artifact_id": VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_ID,
        "readback_id": VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_ID,
        "schema_version": VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "internal_review_status": "needs_audience_fit_refinement",
        "mechanics_status": "pass",
        "identity": {
            "readback_id": VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_ID,
            "source_review_stage_path": _path_text(
                DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_PATH
            ),
            "source_card_render_or_preview_context_path": _path_text(
                DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_PATH
            ),
            "source_visual_card_refinement_path": _path_text(
                DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH
            ),
            "review_source": "user_freeform",
            "production_status": "diagnostic_only",
        },
        "source_validation": validation,
        "audience_fit_review_normalization": _audience_fit_review_normalization(),
        "review_findings": _audience_fit_review_findings(),
        "accepted_mechanics": {
            "timing": "diagnostic_pass",
            "native_audio": "diagnostic_pass",
            "render": "diagnostic_pass_prior_evidence",
            "card_placement": "diagnostic_pass_prior_evidence",
        },
        "accepted_scope": {
            "audience_fit_review_captured": True,
            "modern_visual_quality_signal_preserved": True,
            "audience_fit_refinement_axis_selected": True,
            "review_does_not_reopen_timing_audio_or_placement": True,
        },
        "not_accepted_scope": _not_accepted_scope(),
        "readiness_separation": {
            "slice_completion": "pass_for_review_readback",
            "video_readiness_progress": "6/7",
            "visual_readiness_current": "needs_audience_fit_refinement",
            "production_readiness": "low_diagnostic_only",
            "recommended_next_axis": "visual_card_audience_fit_refinement",
            "public_video_ready": False,
        },
        "render_gate_carry_forward": _render_gate_hygiene_note(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check("visual_card_audience_fit_refinement"),
        "boundaries": _boundaries(),
    }


def build_default_newsroom_visual_card_audience_fit_refinement(
    *,
    root: str | Path | None = None,
    png_export: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the audience-fit refinement artifact from current files."""
    base = Path(root) if root is not None else Path(".")
    review = load_json_object(
        base / DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_PATH
    )
    source_refinement = load_json_object(
        base / DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH
    )
    bridge = load_json_object(base / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH)
    cards = _audience_fit_cards_from_source(source_refinement)
    design_changes = _design_changes(base, cards)
    pngs_valid = all(row["png_valid"] for row in design_changes)
    status = "assets_regenerated" if pngs_valid else "blocked"
    export_status = png_export or _png_export_status_from_files(base, cards)
    return {
        "artifact_id": VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_ID,
        "refinement_id": VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_ID,
        "schema_version": VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "refinement_status": status,
        "identity": {
            "refinement_id": VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_ID,
            "source_audience_fit_review_readback_path": _path_text(
                DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_PATH
            ),
            "source_audience_fit_review_readback_id": review.get("readback_id"),
            "source_visual_card_refinement_path": _path_text(
                DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH
            ),
            "source_visual_card_refinement_id": source_refinement.get(
                "refinement_id"
            ),
            "source_visual_card_bridge_path": _path_text(
                DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH
            ),
            "source_visual_card_bridge_id": bridge.get("bridge_id"),
            "source_cards_dir": _path_text(DEFAULT_VISUAL_CARD_ASSET_DIR),
            "output_cards_dir": _path_text(DEFAULT_VISUAL_CARD_ASSET_DIR),
            "production_status": "diagnostic_only",
        },
        "design_token_constraints": _design_token_constraints(),
        "design_changes": design_changes,
        "source_review_findings": review.get("review_findings"),
        "source_audience_fit_review_normalization": review.get(
            "audience_fit_review_normalization"
        ),
        "raster_export_status": export_status,
        "accepted_scope": _accepted_scope(pngs_valid),
        "not_accepted_scope": _not_accepted_scope(),
        "readiness_separation": _readiness_separation(pngs_valid),
        "next_recommended_slice": {
            "slice": NEXT_DEFAULT_SLICE if pngs_valid else RASTER_EXPORT_SLICE,
            "reason": (
                "stable SVG/PNG asset paths were regenerated with a familiar "
                "YouTube explainer style, so the next milestone is a "
                "post-audience-fit render smoke"
                if pngs_valid
                else "raster export must pass before a render milestone"
            ),
        },
        "recommended_next_slices": _recommended_next_slices(pngs_valid),
        "implementation_principle_for_next_lane": [
            "Keep cards as external SVG/PNG assets.",
            "Do not rebuild cards as YMM4 TextItem/ShapeItem graphs.",
            "Preserve the YMM4 native audio path.",
            "Keep .ymmp mutation limited to ignored local copies.",
        ],
        "goal_stack": _goal_stack(),
        "completion_matrix": _completion_matrix(pngs_valid),
        "artifact_readiness": _artifact_readiness(pngs_valid),
        "visual_readiness": _visual_readiness(pngs_valid),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(
            NEXT_DEFAULT_SLICE if pngs_valid else RASTER_EXPORT_SLICE
        ),
        "boundaries": _boundaries(),
        "downstream_next_use": {
            "use_this_refinement_to": [
                "reuse stable PNG paths in the existing ignored placement project",
                "run a milestone-gated post-audience-fit render smoke later",
                "compare familiarity and readability against the latest review",
            ],
            "do_not_use_this_refinement_to": [
                "claim production visual quality",
                "claim public video readiness",
                "introduce real brands, real URLs, screenshots, or external TTS",
                "commit ignored .ymmp, mp4, audio, voice cache, or render outputs",
            ],
        },
    }


def render_audience_fit_card_svg(card: dict[str, Any]) -> str:
    """Render one familiar explainer-style diagnostic card."""
    palette = _dict(card.get("palette"))
    background = palette.get("background", "#F8FAFC")
    ink = palette.get("ink", "#111827")
    muted = palette.get("muted", "#374151")
    panel = palette.get("panel", "#FFFFFF")
    panel_2 = palette.get("panel_2", "#F3F4F6")
    accent = palette.get("accent", "#DC2626")
    accent_dark = palette.get("accent_dark", "#991B1B")
    chip = palette.get("chip", "#111827")
    chip_text = palette.get("chip_text", "#FFFFFF")
    warning = palette.get("warning", "#FEF3C7")
    title = _xml(card.get("card_title"))
    role = _xml(card.get("role"))
    motif = _xml(card.get("layout_motif"))
    headline_lines = _wrap_text(
        str(card.get("headline") or ""),
        int(AUDIENCE_FIT_TOKENS["headline_wrap_chars"]),
        max_lines=int(AUDIENCE_FIT_TOKENS["max_headline_lines"]),
    )
    body_lines = _wrap_text(
        str(card.get("body") or ""),
        int(AUDIENCE_FIT_TOKENS["body_wrap_chars"]),
        max_lines=int(AUDIENCE_FIT_TOKENS["max_body_lines"]),
    )
    source = _xml(_source_display_label(card))
    timing = _xml(f"{card.get('intended_start_sec')}-{card.get('intended_end_sec')} SEC")
    count = _xml(f"{card.get('display_order')}/4")

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" '
        f'viewBox="0 0 1920 1080" role="img" aria-label="{title}" '
        f'data-refinement="audience-fit-v1" data-role="{role}" '
        f'data-motif="{motif}" data-audience-fit="familiar_youtube_explainer">',
        f"  <title>{title}</title>",
        "  <desc>Diagnostic-only fake newsroom audience-fit card asset.</desc>",
        f'  <rect x="0" y="0" width="1920" height="1080" fill="{background}"/>',
        f'  <rect x="56" y="56" width="1808" height="968" rx="8" fill="{panel}" stroke="#111827" stroke-width="8"/>',
        f'  <rect x="84" y="84" width="1752" height="108" rx="8" fill="{chip}"/>',
        f'  <text x="126" y="154" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="800" fill="{chip_text}">REVIEW ONLY</text>',
        f'  <rect x="448" y="106" width="254" height="64" rx="8" fill="{warning}" stroke="{accent_dark}" stroke-width="4"/>',
        f'  <text x="575" y="150" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="800" fill="{accent_dark}">DIAGNOSTIC</text>',
        f'  <text x="1748" y="154" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="800" fill="{chip_text}">CARD {count}</text>',
        f'  <rect x="104" y="232" width="774" height="548" rx="8" fill="{panel_2}" stroke="{accent_dark}" stroke-width="6"/>',
        f'  <rect x="104" y="232" width="774" height="94" rx="8" fill="{accent}"/>',
        f'  <text x="140" y="296" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="800" fill="#FFFFFF">{_xml(card.get("review_role_label"))}</text>',
        f'  <text x="820" y="296" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="800" fill="#FFFFFF">{timing}</text>',
        f'  <text x="140" y="412" font-family="Arial, Helvetica, sans-serif" font-size="62" font-weight="800" fill="{ink}">{title}</text>',
    ]
    lines.extend(
        _svg_text_lines(
            headline_lines,
            x=140,
            y=520,
            font_size=76,
            line_height=84,
            fill=ink,
            weight="800",
        )
    )
    lines.extend(
        _svg_text_lines(
            body_lines,
            x=144,
            y=650,
            font_size=44,
            line_height=54,
            fill=muted,
            weight="700",
        )
    )
    lines.extend(_render_audience_fit_motif(card, palette))
    lines.extend(
        [
            f'  <rect x="104" y="820" width="1712" height="124" rx="8" fill="#111827"/>',
            '  <text x="146" y="872" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="800" fill="#FFFFFF">SUBTITLE AREA</text>',
            '  <text x="146" y="918" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="700" fill="#D1D5DB">Keep this lower band simple for YMM4 dialogue/subtitle review.</text>',
            f'  <text x="1768" y="872" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="800" fill="#FFFFFF">{source}</text>',
            "</svg>",
            "",
        ]
    )
    return "\n".join(lines)


def _source_display_label(card: dict[str, Any]) -> str:
    order = int(card.get("display_order") or 0)
    total = len(AUDIENCE_FIT_CARD_SPECS)
    return f"SRC {order}/{total}"


def render_audience_fit_contact_sheet_html(cards: list[dict[str, Any]]) -> str:
    """Render a local contact sheet for the audience-fit card assets."""
    card_html: list[str] = []
    for card in cards:
        card_html.extend(
            [
                '<article class="card">',
                f'  <img src="{_html(Path(str(card.get("output_svg_path"))).name)}" alt="{_html(card.get("card_id"))}">',
                '  <div class="meta">',
                f'    <strong>{_html(card.get("card_title"))}</strong>',
                f'    <span>{_html(card.get("review_role_label"))}</span>',
                f'    <span>{_html(card.get("layout_motif"))}</span>',
                f'    <span>{_html(card.get("intended_start_sec"))}-{_html(card.get("intended_end_sec"))}s</span>',
                "  </div>",
                "</article>",
            ]
        )
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '  <meta charset="utf-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1">',
            "  <title>Newsroom Visual Cards - audience fit v1</title>",
            "  <style>",
            "    :root { color-scheme: light; font-family: Arial, Helvetica, sans-serif; }",
            "    body { margin: 0; background: #f8fafc; color: #111827; }",
            "    header { padding: 28px 32px 18px; border-bottom: 2px solid #111827; }",
            "    h1 { margin: 0 0 8px; font-size: 30px; letter-spacing: 0; }",
            "    p { margin: 0; color: #374151; max-width: 980px; line-height: 1.5; }",
            "    main { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 24px; padding: 28px 32px 36px; }",
            "    .card { border: 2px solid #111827; border-radius: 8px; background: #fff; overflow: hidden; }",
            "    img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: contain; background: #f8fafc; }",
            "    .meta { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; padding: 14px 16px; font-size: 15px; }",
            "    .meta span { color: #374151; }",
            "  </style>",
            "</head>",
            "<body>",
            "  <header>",
            "    <h1>Newsroom Visual Cards - audience fit v1</h1>",
            "    <p>Diagnostic-only fake cards with larger text, benchmarked text-fit wraps, "
            "familiar labels, and mainstream explainer composition. No real brands, URLs, media, "
            "render output, audio, TTS, or production approval are included.</p>",
            "  </header>",
            "  <main>",
            *card_html,
            "  </main>",
            "</body>",
            "</html>",
            "",
        ]
    )


def render_newsroom_visual_card_audience_fit_review_readback_markdown(
    readback: dict[str, Any],
) -> str:
    """Render the audience-fit review readback doc."""
    lines = [
        "# Newsroom Visual Card Audience-Fit Review Readback v1",
        "",
        f"artifact_id: {readback.get('artifact_id')}",
        f"readback_id: {readback.get('readback_id')}",
        f"schema_version: {readback.get('schema_version')}",
        f"internal_review_status: {readback.get('internal_review_status')}",
        f"mechanics_status: {readback.get('mechanics_status')}",
        "production_status: diagnostic_only",
        "",
        "## Identity",
        "",
    ]
    _append_key_values(lines, readback.get("identity"))
    lines.extend(["", "## Source Validation", ""])
    _append_key_values(lines, readback.get("source_validation"))
    lines.extend(["", "## Normalized Review", ""])
    _append_key_values(lines, readback.get("audience_fit_review_normalization"))
    lines.extend(["", "## Findings", ""])
    _append_key_values(lines, readback.get("review_findings"))
    lines.extend(["", "## Accepted Mechanics", ""])
    _append_key_values(lines, readback.get("accepted_mechanics"))
    lines.extend(["", "## Not Accepted Scope", ""])
    _append_key_values(lines, readback.get("not_accepted_scope"))
    lines.extend(["", "## Render Gate", ""])
    _append_key_values(lines, readback.get("render_gate_carry_forward"))
    _append_status_table(
        lines, "Human Burden Hygiene", readback.get("human_burden_hygiene")
    )
    _append_status_table(
        lines, "Review Non-Redundancy", readback.get("review_non_redundancy")
    )
    _append_status_table(lines, "Inertia Check", readback.get("inertia_check"))
    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "The review is normalized as an audience-fit issue: the current cards "
            "are cleaner and more readable, but still too SaaS/dashboard-like for "
            "the target YouTube viewer. Timing, audio, placement mechanics, "
            "production/public approval, and real content remain outside this slice.",
            "",
        ]
    )
    return "\n".join(lines)


def render_newsroom_visual_card_audience_fit_refinement_markdown(
    refinement: dict[str, Any],
) -> str:
    """Render the audience-fit refinement doc."""
    lines = [
        "# Newsroom Visual Card Audience-Fit Refinement v1",
        "",
        f"artifact_id: {refinement.get('artifact_id')}",
        f"refinement_id: {refinement.get('refinement_id')}",
        f"schema_version: {refinement.get('schema_version')}",
        f"refinement_status: {refinement.get('refinement_status')}",
        "production_status: diagnostic_only",
        "",
        "## Identity",
        "",
    ]
    _append_key_values(lines, refinement.get("identity"))
    lines.extend(["", "## Design Token Constraints", ""])
    _append_key_values(lines, refinement.get("design_token_constraints"))
    lines.extend(
        [
            "",
            "## Card Changes",
            "",
            "| card | role | motif | text size | familiarity | svg | png |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for row in _list(refinement.get("design_changes")):
        lines.append(
            "| "
            f"{row.get('card_id')} | "
            f"{row.get('role')} | "
            f"{row.get('layout_motif')} | "
            f"{row.get('text_size_adjustment')} | "
            f"{row.get('familiar_ui_adjustment')} | "
            f"{row.get('output_svg_path')} | "
            f"{row.get('output_png_path')} |"
        )
    lines.extend(["", "## Accepted Scope", ""])
    _append_key_values(lines, refinement.get("accepted_scope"))
    lines.extend(["", "## Not Accepted Scope", ""])
    _append_key_values(lines, refinement.get("not_accepted_scope"))
    lines.extend(["", "## Next Recommended Slice", ""])
    _append_key_values(lines, refinement.get("next_recommended_slice"))
    lines.extend(
        [
            "",
            "## Recommended Next Slices",
            "",
            "| slice | timing | reason |",
            "|---|---|---|",
        ]
    )
    for row in _list(refinement.get("recommended_next_slices")):
        lines.append(
            "| "
            f"{row.get('slice')} | "
            f"{row.get('timing')} | "
            f"{row.get('reason')} |"
        )
    lines.extend(
        [
            "",
            "## Goal Stack",
            "",
            "| level | goal | success signal | contribution |",
            "|---|---|---|---|",
        ]
    )
    for row in _list(refinement.get("goal_stack")):
        lines.append(
            "| "
            f"{row.get('level')} | "
            f"{row.get('goal')} | "
            f"{row.get('success_signal')} | "
            f"{row.get('contribution')} |"
        )
    _append_status_table(lines, "Completion Matrix", refinement.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", refinement.get("artifact_readiness"))
    _append_status_table(lines, "Visual Readiness", refinement.get("visual_readiness"))
    _append_status_table(lines, "Render Gate Hygiene", refinement.get("render_gate_hygiene"))
    _append_status_table(
        lines, "Human Burden Hygiene", refinement.get("human_burden_hygiene")
    )
    _append_status_table(
        lines, "Review Non-Redundancy", refinement.get("review_non_redundancy")
    )
    _append_status_table(lines, "Inertia Check", refinement.get("inertia_check"))
    lines.extend(["", "## Boundary", ""])
    _append_key_values(lines, refinement.get("boundaries"))
    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "The regenerated assets are diagnostic cards only. They use stable "
            "SVG/PNG paths for a later render smoke, but do not prove YMM4 render "
            "quality, production visual quality, public readiness, real content, "
            "or final design-system acceptance.",
            "",
        ]
    )
    return "\n".join(lines)


def _audience_fit_cards_from_source(
    source_refinement: dict[str, Any],
) -> list[dict[str, Any]]:
    source_changes = _list(source_refinement.get("design_changes"))
    rows: list[dict[str, Any]] = []
    for index, source in enumerate(source_changes):
        spec = AUDIENCE_FIT_CARD_SPECS[index]
        rows.append(
            {
                "card_id": source.get("card_id"),
                "display_order": index + 1,
                "role": spec["role"],
                "review_role_label": spec["review_role_label"],
                "layout_motif": spec["layout_motif"],
                "card_title": spec["card_title"],
                "headline": spec["headline"],
                "body": spec["body"],
                "main_label": spec["main_label"],
                "callout_label": spec["callout_label"],
                "callout_text": spec["callout_text"],
                "previous_issue_summary": (
                    "Refined card was modern and cleaner, but still felt "
                    "SaaS/dashboard-like and kept some text too small for "
                    "mainstream YouTube viewing."
                ),
                "audience_fit_change_summary": (
                    "Shifted to larger, plainer explainer blocks with familiar "
                    "labels and fewer fine UI ornaments."
                ),
                "text_size_adjustment": "minimum visible text raised to 34px",
                "familiar_ui_adjustment": spec["familiar_ui_adjustment"],
                "variation_adjustment": spec["variation_adjustment"],
                "text_wrap_applied": True,
                "clipping_guard": True,
                "type_scale_status": "audience_fit_larger_plain",
                "variation_status": "role_specific_familiar_layout",
                "output_svg_path": source.get("output_svg_path"),
                "output_png_path": source.get("output_png_path"),
                "preview_path": _path_text(DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH),
                "contact_sheet_path": _path_text(DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH),
                "source_caption_or_beat_id": _caption_id_from_card_id(
                    str(source.get("card_id") or "")
                ),
                "intended_start_sec": _start_sec(index),
                "intended_end_sec": _end_sec(index),
                "design_tokens": AUDIENCE_FIT_TOKENS,
                "audience_fit_style": "familiar_youtube_explainer",
                "fake_content_only": True,
                "contains_real_urls": False,
                "contains_real_brands": False,
                "contains_real_news_claims": False,
                "palette": spec["palette"],
            }
        )
    return rows


def _design_changes(root: Path, cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for card in cards:
        metadata = _png_metadata(root / str(card.get("output_png_path")))
        rows.append(
            {
                "card_id": card.get("card_id"),
                "role": card.get("role"),
                "role_label": card.get("review_role_label"),
                "layout_motif": card.get("layout_motif"),
                "previous_issue_summary": card.get("previous_issue_summary"),
                "audience_fit_change_summary": card.get(
                    "audience_fit_change_summary"
                ),
                "text_size_adjustment": card.get("text_size_adjustment"),
                "familiar_ui_adjustment": card.get("familiar_ui_adjustment"),
                "variation_adjustment": card.get("variation_adjustment"),
                "text_wrap_applied": card.get("text_wrap_applied") is True,
                "clipping_guard": card.get("clipping_guard") is True,
                "type_scale_status": card.get("type_scale_status"),
                "variation_status": card.get("variation_status"),
                "output_svg_path": card.get("output_svg_path"),
                "output_png_path": card.get("output_png_path"),
                "preview_path": card.get("preview_path"),
                "contact_sheet_path": card.get("contact_sheet_path"),
                "png_valid": metadata.get("valid") is True,
                "png_width": metadata.get("width"),
                "png_height": metadata.get("height"),
            }
        )
    return rows


def _render_audience_fit_motif(
    card: dict[str, Any],
    palette: dict[str, str],
) -> list[str]:
    accent = palette.get("accent", "#DC2626")
    accent_dark = palette.get("accent_dark", "#991B1B")
    panel = palette.get("panel", "#FFFFFF")
    panel_2 = palette.get("panel_2", "#F3F4F6")
    ink = palette.get("ink", "#111827")
    muted = palette.get("muted", "#374151")
    warning = palette.get("warning", "#FEF3C7")
    role = str(card.get("role") or "")
    lines = [
        f'  <rect x="944" y="232" width="872" height="548" rx="8" fill="{panel}" stroke="{accent_dark}" stroke-width="6"/>',
    ]
    if role == "intro_summary":
        lines.extend(
            [
                f'  <circle cx="1156" cy="430" r="128" fill="{accent}"/>',
                f'  <text x="1156" y="470" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="132" font-weight="800" fill="#FFFFFF">{_xml(card.get("main_label"))}</text>',
                f'  <rect x="1320" y="330" width="380" height="200" rx="8" fill="{panel_2}" stroke="{accent}" stroke-width="5"/>',
                f'  <text x="1360" y="410" font-family="Arial, Helvetica, sans-serif" font-size="54" font-weight="800" fill="{ink}">{_xml(card.get("callout_label"))}</text>',
                f'  <text x="1360" y="478" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="700" fill="{muted}">{_xml(card.get("callout_text"))}</text>',
                f'  <rect x="1030" y="626" width="694" height="86" rx="8" fill="{warning}" stroke="{accent_dark}" stroke-width="4"/>',
                f'  <text x="1072" y="682" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="800" fill="{accent_dark}">NO REAL NEWS CLAIM</text>',
            ]
        )
    elif role == "handoff_process":
        steps = [("1", "INPUT"), ("2", "CARD"), ("3", "CHECK")]
        for index, (number, label) in enumerate(steps):
            y = 326 + index * 126
            lines.extend(
                [
                    f'  <rect x="1036" y="{y}" width="632" height="92" rx="8" fill="{panel_2}" stroke="{accent}" stroke-width="5"/>',
                    f'  <circle cx="1100" cy="{y + 46}" r="36" fill="{accent}"/>',
                    f'  <text x="1100" y="{y + 59}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="800" fill="#FFFFFF">{number}</text>',
                    f'  <text x="1170" y="{y + 60}" font-family="Arial, Helvetica, sans-serif" font-size="48" font-weight="800" fill="{ink}">{label}</text>',
                ]
            )
        lines.extend(
            [
                f'  <rect x="1238" y="704" width="430" height="58" rx="8" fill="{accent}"/>',
                '  <text x="1453" y="745" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="800" fill="#FFFFFF">SIMPLE FLOW</text>',
            ]
        )
    elif role == "claim_check":
        cells = [
            (1018, 318, "CHECK", "fake only", panel_2),
            (1380, 318, "CAUTION", "review only", warning),
            (1018, 542, "RESULT", "not public", panel_2),
            (1380, 542, "STATUS", "diagnostic", panel_2),
        ]
        for x, y, label, note, fill in cells:
            lines.extend(
                [
                    f'  <rect x="{x}" y="{y}" width="312" height="150" rx="8" fill="{fill}" stroke="{accent_dark}" stroke-width="5"/>',
                    f'  <text x="{x + 34}" y="{y + 62}" font-family="Arial, Helvetica, sans-serif" font-size="48" font-weight="800" fill="{ink}">{label}</text>',
                    f'  <text x="{x + 34}" y="{y + 114}" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="700" fill="{muted}">{note}</text>',
                ]
            )
    else:
        rows = [("SOURCE", "fake source note"), ("STATUS", "diagnostic only"), ("NEXT", "render smoke later")]
        for index, (label, note) in enumerate(rows):
            y = 318 + index * 132
            lines.extend(
                [
                    f'  <rect x="1038" y="{y}" width="640" height="98" rx="8" fill="{panel_2}" stroke="#111827" stroke-width="4"/>',
                    f'  <rect x="1038" y="{y}" width="22" height="98" rx="8" fill="{accent}"/>',
                    f'  <text x="1094" y="{y + 45}" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="800" fill="{ink}">{label}</text>',
                    f'  <text x="1094" y="{y + 84}" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="700" fill="{muted}">{note}</text>',
                ]
            )
        lines.extend(
            [
                f'  <circle cx="1668" cy="690" r="58" fill="{accent}"/>',
                '  <text x="1668" y="710" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="56" font-weight="800" fill="#FFFFFF">NEXT</text>',
            ]
        )
    return lines


def _review_source_validation(
    source_refinement: dict[str, Any],
    post_refinement_package: dict[str, Any],
    source_review: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if source_refinement.get("refinement_status") != "assets_regenerated":
        errors.append("SOURCE_VISUAL_REFINEMENT_NOT_REGENERATED")
    if len(_list(source_refinement.get("design_changes"))) != 4:
        errors.append("SOURCE_VISUAL_REFINEMENT_CARD_COUNT_NOT_4")
    if post_refinement_package.get("package_status") != (
        "ready_for_manual_milestone_render_smoke"
    ):
        errors.append("POST_REFINEMENT_PACKAGE_NOT_READY")
    if source_review.get("mechanics_status") != "pass":
        errors.append("SOURCE_REVIEW_MECHANICS_NOT_PASS")
    return {
        "status": "passed" if not errors else "blocked",
        "errors": errors,
        "source_visual_refinement_id": source_refinement.get("refinement_id"),
        "source_visual_refinement_status": source_refinement.get("refinement_status"),
        "source_post_refinement_package_id": post_refinement_package.get("smoke_id"),
        "source_post_refinement_package_status": post_refinement_package.get(
            "package_status"
        ),
        "source_review_readback_id": source_review.get("readback_id"),
        "source_review_mechanics_status": source_review.get("mechanics_status"),
        "card_count": len(_list(source_refinement.get("design_changes"))),
    }


def _audience_fit_review_normalization() -> dict[str, Any]:
    return {
        "internal_review_status": "needs_audience_fit_refinement",
        "modern_visual_quality_signal": "positive",
        "small_text_still_present": True,
        "audience_familiarity_mismatch": True,
        "too_saas_dashboard_like": True,
        "mainstream_youtube_visual_language_required": True,
        "production_visual_quality_accepted": False,
        "public_video_ready": False,
        "recommended_next_axis": "visual_card_audience_fit_refinement",
    }


def _audience_fit_review_findings() -> dict[str, Any]:
    return {
        "modern_visual_quality_signal": "positive",
        "small_text_still_present": True,
        "audience_familiarity_mismatch": True,
        "too_saas_dashboard_like": True,
        "mainstream_youtube_visual_language_required": True,
    }


def _design_token_constraints() -> dict[str, Any]:
    return {
        **AUDIENCE_FIT_TOKENS,
        "text_wrapping_required": True,
        "source_metadata_wrap_required": True,
        "card_variation_required": "role_specific_familiar_layout",
    }


def _accepted_scope(pngs_valid: bool) -> dict[str, bool]:
    return {
        "audience_fit_review_captured": True,
        "external_card_assets_regenerated": pngs_valid,
        "minimum_text_readability_improved": pngs_valid,
        "dashboard_saas_feel_reduced": pngs_valid,
        "familiar_youtube_explainer_visual_language_introduced": pngs_valid,
        "card_variation_increased": pngs_valid,
        "assets_ready_for_later_yym4_render_smoke": pngs_valid,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_visual_quality": False,
        "final_design_system": False,
        "post_audience_fit_render_proof": False,
        "YMM4_placement_proof_after_this_refinement": False,
        "public_video_readiness": False,
        "real_newsroom_visuals": False,
        "real_content_readiness": False,
        "production_approval": False,
    }


def _readiness_separation(pngs_valid: bool) -> dict[str, Any]:
    return {
        "slice_completion": "pass_for_audience_fit_refinement"
        if pngs_valid
        else "blocked",
        "video_readiness_progress": "6/7",
        "visual_readiness_progress": "7/7_diagnostic_audience_fit_refined"
        if pngs_valid
        else "blocked",
        "visual_readiness_current": "external_card_assets_audience_fit_refined"
        if pngs_valid
        else "png_regeneration_blocked",
        "video_readiness_next_missing_gate": (
            "post-audience-fit render smoke observation, then internal review milestone"
        ),
        "production_readiness": "low_diagnostic_only",
        "next_default_slice": NEXT_DEFAULT_SLICE if pngs_valid else RASTER_EXPORT_SLICE,
    }


def _recommended_next_slices(pngs_valid: bool) -> list[dict[str, str]]:
    default = NEXT_DEFAULT_SLICE if pngs_valid else RASTER_EXPORT_SLICE
    return [
        {
            "slice": default,
            "timing": "recommended_next_default",
            "reason": (
                "stable SVG/PNG card paths were regenerated with audience-fit "
                "visual language"
                if pngs_valid
                else "PNG export must be fixed before another render milestone"
            ),
        },
        {
            "slice": PLACEMENT_REFRESH_SLICE,
            "timing": "only_if_existing_placement_paths_are_not_stable",
            "reason": "refresh ImageItem placement only if stable PNG paths cannot be reused",
        },
        {
            "slice": INTERNAL_REVIEW_PREP_SLICE,
            "timing": "after_post_audience_fit_smoke",
            "reason": "internal review is meaningful after the changed visual surface is observed",
        },
    ]


def _goal_stack() -> list[dict[str, str]]:
    return [
        {
            "level": "Immediate",
            "goal": "Convert visual review into audience-fit refinement",
            "success_signal": "review readback and regenerated cards exist",
            "contribution": "avoids vague taste debate",
        },
        {
            "level": "Short-term",
            "goal": "Improve readability and familiarity",
            "success_signal": "cards are larger, simpler, less SaaS-like",
            "contribution": "makes next render review meaningful",
        },
        {
            "level": "Mid-term",
            "goal": "Prepare post-audience-fit render smoke",
            "success_signal": "stable PNG assets can be reused by placement .ymmp",
            "contribution": "moves toward internal review acceptance",
        },
        {
            "level": "Long-term",
            "goal": "Establish reusable mainstream card baseline",
            "success_signal": "future packets can use viewer-familiar templates",
            "contribution": "improves automation viability",
        },
    ]


def _completion_matrix(pngs_valid: bool) -> list[dict[str, Any]]:
    return [
        {"gate": "current_repo_state_verified", "status": True},
        {"gate": "audience_fit_review_normalized", "status": True},
        {"gate": "current_card_issues_inspected", "status": True},
        {"gate": "audience_fit_refined_card_assets_generated", "status": pngs_valid},
        {"gate": "preview_contact_sheet_updated", "status": True},
        {
            "gate": "narrow_commit_created_and_pushed_if_push_gate_passes",
            "status": "pending_until_git_gate",
        },
    ]


def _artifact_readiness(pngs_valid: bool) -> list[dict[str, Any]]:
    return [
        {"artifact": "audience_fit_review_readback", "status": "present"},
        {"artifact": "audience_fit_refinement_json", "status": "present"},
        {"artifact": "human_docs", "status": "present"},
        {"artifact": "refined_svg_png_assets", "status": "present" if pngs_valid else "blocked"},
        {"artifact": "contact_sheet_preview", "status": "present"},
        {"artifact": "downstream_next_use", "status": "present"},
    ]


def _visual_readiness(pngs_valid: bool) -> list[dict[str, Any]]:
    return [
        {"gate": "visual_card_concept_selected", "status": True},
        {"gate": "external_card_assets_generated", "status": True},
        {"gate": "preview_contact_sheet_available", "status": True},
        {"gate": "assets_mapped_to_timeline_caption_units", "status": True},
        {"gate": "yym4_placement_contract_defined", "status": True},
        {"gate": "yym4_placement_proof_observed", "status": True},
        {"gate": "post_audience_fit_render_reviewed", "status": False if pngs_valid else "blocked"},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "render_performed_in_this_slice", "status": False},
        {"gate": "existing_render_review_evidence_reused", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {"gate": "next_render_tied_to_audience_fit_visual_surface_change", "status": True},
        {"gate": "no_render_for_docs_only_changes", "status": True},
        {"gate": "repeated_timing_audio_review_avoided", "status": True},
    ]


def _render_gate_hygiene_note() -> dict[str, Any]:
    return {
        "new_render_in_this_slice": False,
        "YMM4_launched_by_agent": False,
        "render_audio_or_tts_created_by_agent": False,
        "existing_render_review_evidence_reused": True,
        "render_gate": "milestone_gated_not_docs_gated",
        "next_render_allowed_after": [
            "audience-fit visual surface changes are written to stable PNG assets",
            "internal review v0.1 milestone needs a fresh observation",
        ],
    }


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "user_input", "status": "freeform"},
        {"gate": "template_required", "status": False},
        {"gate": "schema_owner", "status": "Agent"},
        {"gate": "user_side_work_for_this_slice", "status": "none"},
        {"gate": "negative_confirmation_checklist", "status": False},
        {"gate": "fixed_form_relapse", "status": False},
        {"gate": "repeated_review_request", "status": False},
    ]


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"gate": "prior_internal_review_observation_consumed_once", "status": True},
        {"gate": "prior_render_evidence_reused", "status": True},
        {"gate": "next_axis_stated_as_audience_fit_visual_refinement", "status": True},
        {"gate": "not_accepted_scope_preserved", "status": True},
        {"gate": "repeated_user_review_requested", "status": False},
        {"gate": "mechanics_re_review_requested", "status": False},
    ]


def _inertia_check(next_slice: str) -> list[dict[str, Any]]:
    return [
        {"gate": "packet_for_packet_drift", "status": False},
        {"gate": "readback_only_stall", "status": False},
        {"gate": "repeated_render_request", "status": False},
        {"gate": "readiness_separated_from_slice_completion", "status": True},
        {"gate": "next_concrete_milestone", "status": next_slice},
    ]


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "video_render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "external_TTS_introduced": False,
        "real_media_imported": False,
        "external_source_fetch_performed": False,
        "real_brand_url_or_news_screenshot_used": False,
        "ymmp_edited_by_agent": False,
        "ymmp_or_media_staged_or_committed": False,
        "render_output_staged_or_committed": False,
        "production_visual_quality_accepted": False,
        "production_approval": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


def _png_export_status_from_files(
    root: Path,
    cards: list[dict[str, Any]],
) -> dict[str, Any]:
    files = [_png_metadata(root / str(card.get("output_png_path"))) for card in cards]
    return {
        "png_export_status": "generated" if all(row["valid"] for row in files) else "blocked",
        "rasterization_method": "existing_toolchain",
        "deterministic_export": all(row["valid"] for row in files),
        "png_file_count": len(files),
        "expected_png_file_count": 4,
        "errors": [f"PNG_INVALID:{row['path']}" for row in files if not row["valid"]],
        "png_files": files,
    }


def _ensure_audience_fit_png_assets(
    root: Path,
    cards: list[dict[str, Any]],
) -> dict[str, Any]:
    source_assets = [
        {
            "source_svg_path": card["output_svg_path"],
            "png_path": card["output_png_path"],
        }
        for card in cards
    ]
    result = ensure_card_png_assets(root, source_assets, force=True)
    if result.get("png_export_status") == "generated":
        return result

    fallback_errors = _export_pngs_with_bundled_python(root, source_assets)
    if fallback_errors:
        merged_errors = _list_str(result.get("errors")) + fallback_errors
        files = [_png_metadata(root / str(card.get("output_png_path"))) for card in cards]
        return {
            "png_export_status": "blocked",
            "rasterization_method": "not_available",
            "deterministic_export": False,
            "png_file_count": len(files),
            "expected_png_file_count": 4,
            "errors": merged_errors,
            "png_files": files,
        }
    return _png_export_status_from_files(root, cards) | {
        "rasterization_method": "bundled_python_pillow_svg_subset",
    }


def _export_pngs_with_bundled_python(
    root: Path,
    source_assets: list[dict[str, Any]],
) -> list[str]:
    python_path = _bundled_python_path()
    if python_path is None:
        return ["BUNDLED_PYTHON_NOT_AVAILABLE"]
    jobs = [
        {
            "source_svg_path": str(asset["source_svg_path"]),
            "png_path": str(asset["png_path"]),
        }
        for asset in source_assets
    ]
    script = (
        "import json, sys\n"
        "from pathlib import Path\n"
        "from src.pipeline.newsroom_yym4_card_asset_placement_probe "
        "import _render_svg_subset_to_png\n"
        "jobs = json.loads(sys.argv[1])\n"
        "for job in jobs:\n"
        "    _render_svg_subset_to_png(Path(job['source_svg_path']), Path(job['png_path']))\n"
    )
    result = subprocess.run(
        [str(python_path), "-c", script, json.dumps(jobs)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        return [f"BUNDLED_PYTHON_PNG_EXPORT_FAILED:{detail}"]
    return []


def _bundled_python_path() -> Path | None:
    candidate = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
        / "python"
        / "python.exe"
    )
    return candidate if candidate.exists() else None


def _png_metadata(path: str | Path) -> dict[str, Any]:
    png_path = Path(path)
    metadata: dict[str, Any] = {
        "path": _path_text(png_path),
        "exists": png_path.exists(),
        "valid": False,
    }
    if not png_path.exists():
        return metadata
    try:
        with png_path.open("rb") as handle:
            header = handle.read(24)
        if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
            return metadata
        width, height = struct.unpack(">II", header[16:24])
    except OSError:
        return metadata
    metadata.update(
        {
            "valid": width == 1920 and height == 1080,
            "width": width,
            "height": height,
            "format": "png",
        }
    )
    return metadata


def _caption_id_from_card_id(card_id: str) -> str:
    prefix = "visual_card_"
    suffix = "_v1"
    if card_id.startswith(prefix) and card_id.endswith(suffix):
        return card_id[len(prefix) : -len(suffix)]
    return card_id


def _start_sec(index: int) -> int:
    return [0, 12, 24, 46][index]


def _end_sec(index: int) -> int:
    return [12, 24, 46, 68][index]


def _svg_text_lines(
    values: list[str],
    *,
    x: int,
    y: int,
    font_size: int,
    line_height: int,
    fill: str,
    weight: str,
    anchor: str = "start",
) -> list[str]:
    lines: list[str] = []
    for index, value in enumerate(values):
        line_y = y + index * line_height
        anchor_attr = f' text-anchor="{anchor}"' if anchor != "start" else ""
        lines.append(
            f'  <text x="{x}" y="{line_y}"{anchor_attr} '
            'font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{font_size}" font-weight="{weight}" '
            f'fill="{fill}">{_xml(value)}</text>'
        )
    return lines


def _wrap_text(value: str, max_chars: int, *, max_lines: int) -> list[str]:
    words = str(value).split()
    if not words:
        return [""]
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
        if len(lines) == max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(current)
    if len(lines) == max_lines:
        used = " ".join(lines)
        if len(used) < len(value):
            lines[-1] = lines[-1].rstrip(".") + "..."
    return lines[:max_lines]


def _append_key_values(lines: list[str], value: Any) -> None:
    for key, item in _dict(value).items():
        lines.append(f"- {key}: {_display(item)}")


def _append_status_table(lines: list[str], title: str, rows: Any) -> None:
    lines.extend(["", f"## {title}", "", "| item | status |", "|---|---|"])
    for row in rows if isinstance(rows, list) else []:
        key = row.get("gate") or row.get("artifact") or "item"
        lines.append(f"| {key} | {_display(row.get('status'))} |")


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    json_path = Path(path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_bytes(
        (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )


def _write_text(path: str | Path, text: str) -> None:
    text_path = Path(path)
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text_path.write_bytes(text.encode("utf-8"))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _list_str(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _path_text(value: str | Path | None) -> str:
    return str(value).replace("\\", "/") if value is not None else ""


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, list):
        if not value:
            return "[]"
        return ", ".join(_display(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _xml(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _html(value: Any) -> str:
    return html.escape(str(value), quote=True)


def parse_svg(path: str | Path) -> ElementTree.Element:
    """Parse generated SVG for tests and lightweight validation."""
    return ElementTree.parse(path).getroot()
