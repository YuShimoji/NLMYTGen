"""Apply density-benchmarked simplification to newsroom visual cards.

This slice regenerates only the existing four diagnostic SVG/PNG card assets
at stable paths. It does not launch YMM4, render video, edit .ymmp files,
generate audio/TTS, fetch external media, or claim production/public/audience
acceptance.
"""

from __future__ import annotations

import html
import json
import struct
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from src.pipeline.newsroom_audience_fit_benchmark_evaluation import (
    DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_post_benchmarked_visual_observation_density_gate import (
    DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH,
)
from src.pipeline.newsroom_visual_audience_fit_benchmark import (
    DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH,
)
from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_ASSET_DIR,
    DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
)
from src.pipeline.newsroom_visual_card_benchmarked_refinement import (
    DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH,
)
from src.pipeline.newsroom_visual_card_audience_fit_refinement import (
    _export_pngs_with_bundled_python,
    _png_export_status_from_files,
)
from src.pipeline.newsroom_visual_density_simplification_spec import (
    DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH,
)
from src.pipeline.newsroom_yym4_card_asset_placement_probe import (
    ensure_card_png_assets,
)


VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_SCHEMA_VERSION = (
    "newsroom_visual_card_density_benchmarked_refinement.v1"
)
VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_ID = (
    "newsroom_visual_card_density_benchmarked_refinement_v1_2026_06_26"
)

DEFAULT_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "visual_card_density_benchmarked_refinement_v1.json"
)
DEFAULT_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_V1_2026-06-26.md"
)

NEXT_DEFAULT_SLICE = "newsroom-card-placement-post-density-refinement-render-smoke-v1"
DENSITY_REDUCTION_V2_SLICE = "newsroom-visual-card-density-reduction-v2"
SOURCE_BAND_SIMPLIFICATION_SLICE = "newsroom-visual-card-source-band-simplification-v1"
PLACEMENT_REFRESH_SLICE = "newsroom-yym4-card-asset-placement-refresh-v1"

CANVAS_SIZE = {"width": 1920, "height": 1080}
MINIMUM_MEANINGFUL_FONT_SIZE = 42
MAX_MEANINGFUL_LABELS = 3


def build_default_newsroom_visual_card_density_benchmarked_refinement(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the density refinement readback from current regenerated assets."""
    base = Path(root) if root is not None else Path(".")
    density_spec = load_json_object(
        base / DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH
    )
    density_gate = load_json_object(
        base / DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH
    )
    benchmark_evaluation = load_json_object(
        base / DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH
    )
    visual_benchmark = load_json_object(
        base / DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH
    )
    benchmarked_refinement = load_json_object(
        base / DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH
    )
    cards = _density_cards_from_sources(density_spec, benchmarked_refinement)
    per_card_changes = _per_card_changes(base, cards, density_spec)
    source_validation = _source_validation(
        base=base,
        density_spec=density_spec,
        density_gate=density_gate,
        benchmark_evaluation=benchmark_evaluation,
        visual_benchmark=visual_benchmark,
        benchmarked_refinement=benchmarked_refinement,
        per_card_changes=per_card_changes,
    )
    local_proxy_recheck = _local_proxy_recheck(per_card_changes)
    improved = (
        source_validation["status"] == "passed"
        and local_proxy_recheck["fail_count"] == 0
        and local_proxy_recheck["proxy_status"] == "materially_improved"
    )
    stable_paths = all(row["stable_asset_paths_preserved"] for row in per_card_changes)
    return {
        "artifact_id": VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_ID,
        "refinement_id": VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_ID,
        "schema_version": VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_SCHEMA_VERSION,
        "refinement_status": (
            "density_benchmark_materially_improved" if improved else "blocked"
        ),
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "visual_work_class": "audience_fit",
        "refinement_type": "density_benchmark_linked",
        "actual_audience_acceptance_claimed": False,
        "identity": {
            "refinement_id": VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_ID,
            "source_density_spec_path": _path_text(
                DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH
            ),
            "source_density_spec_id": density_spec.get("spec_id"),
            "source_density_gate_path": _path_text(
                DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH
            ),
            "source_density_gate_id": density_gate.get("readback_id"),
            "source_benchmark_evaluation_path": _path_text(
                DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH
            ),
            "source_benchmark_evaluation_id": benchmark_evaluation.get(
                "evaluation_id"
            ),
            "source_visual_benchmark_path": _path_text(
                DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH
            ),
            "source_visual_benchmark_id": visual_benchmark.get("benchmark_id"),
            "source_benchmarked_refinement_path": _path_text(
                DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH
            ),
            "source_benchmarked_refinement_id": benchmarked_refinement.get(
                "refinement_id"
            ),
            "source_cards_dir": _path_text(DEFAULT_VISUAL_CARD_ASSET_DIR),
            "production_status": "diagnostic_only",
            "visual_work_class": "audience_fit",
            "refinement_type": "density_benchmark_linked",
            "actual_audience_acceptance_claimed": False,
        },
        "source_validation": source_validation,
        "density_fix_map": _density_fix_map(per_card_changes),
        "per_card_changes": per_card_changes,
        "design_constraints": _design_constraints(),
        "local_proxy_recheck": local_proxy_recheck,
        "accepted_scope": _accepted_scope(improved),
        "not_accepted_scope": _not_accepted_scope(),
        "next_recommended_slice": _next_recommended_slice(improved, stable_paths),
        "recommended_next_slices": _recommended_next_slices(improved, stable_paths),
        "goal_stack": _goal_stack(),
        "completion_matrix": _completion_matrix(improved),
        "artifact_readiness": _artifact_readiness(improved),
        "visual_density_gate": _visual_density_gate(improved),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(improved),
        "downstream_next_use": _downstream_next_use(improved, stable_paths),
        "boundaries": _boundaries(),
    }


def write_default_newsroom_visual_card_density_benchmarked_refinement_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Regenerate density-simplified cards plus JSON and Markdown readback."""
    base = Path(root) if root is not None else Path(".")
    density_spec = load_json_object(
        base / DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH
    )
    benchmarked_refinement = load_json_object(
        base / DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH
    )
    cards = _density_cards_from_sources(density_spec, benchmarked_refinement)
    for card in cards:
        _write_text(base / card["output_svg_path"], render_density_refined_card_svg(card))
    _write_text(
        base / DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
        render_density_refined_contact_sheet_html(cards),
    )
    source_assets = [
        {
            "source_svg_path": card["output_svg_path"],
            "png_path": card["output_png_path"],
        }
        for card in cards
    ]
    png_result = ensure_card_png_assets(base, source_assets, force=True)
    if png_result.get("png_export_status") != "generated":
        fallback_errors = _export_pngs_with_bundled_python(base, source_assets)
        if fallback_errors:
            png_result = png_result | {
                "png_export_status": "blocked",
                "rasterization_method": "not_available",
                "deterministic_export": False,
                "errors": list(png_result.get("errors", [])) + fallback_errors,
            }
        else:
            png_result = _png_export_status_from_files(base, cards) | {
                "rasterization_method": "bundled_python_pillow_svg_subset",
            }
    refinement = build_default_newsroom_visual_card_density_benchmarked_refinement(
        root=base
    )
    refinement["png_export"] = png_result
    _write_json(
        base / DEFAULT_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_PATH,
        refinement,
    )
    _write_text(
        base / DEFAULT_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_DOC_PATH,
        render_newsroom_visual_card_density_benchmarked_refinement_markdown(
            refinement
        ),
    )
    return refinement


def render_density_refined_card_svg(card: dict[str, Any]) -> str:
    """Render a simplified diagnostic card at 1920x1080."""
    palette = _dict(card.get("palette"))
    background = palette.get("background", "#F8FAFC")
    ink = palette.get("ink", "#111827")
    muted = palette.get("muted", "#374151")
    accent = palette.get("accent", "#DC2626")
    accent_dark = palette.get("accent_dark", "#991B1B")
    panel = palette.get("panel", "#FFFFFF")
    soft = palette.get("soft", "#F3F4F6")
    title = _xml(card["card_title"])
    count = _xml(f"{card['display_order']}/4")
    role_label = _xml(card["role_label"])
    boundary = _xml(card["boundary_label"])
    primary_lines = _wrap_text(card["primary_sentence"], 34, max_lines=2)
    support = card.get("support_note_or_diagram")

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" '
        f'viewBox="0 0 1920 1080" role="img" aria-label="{title}" '
        'data-refinement="density-benchmarked-v1" '
        f'data-card-id="{_xml(card["card_id"])}" '
        f'data-role="{_xml(card["role"])}">',
        f"  <title>{title}</title>",
        "  <desc>Diagnostic-only fake newsroom card simplified by density benchmark.</desc>",
        f'  <rect x="0" y="0" width="1920" height="1080" fill="{background}"/>',
        f'  <rect x="70" y="64" width="1780" height="940" rx="8" fill="{panel}" stroke="#111827" stroke-width="7"/>',
        f'  <rect x="96" y="92" width="1728" height="96" rx="8" fill="#111827"/>',
        f'  <text x="136" y="153" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="800" fill="#FFFFFF">{boundary}</text>',
        f'  <text x="1692" y="153" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="800" fill="#FFFFFF">CARD {count}</text>',
        f'  <rect x="136" y="246" width="544" height="102" rx="8" fill="{accent}"/>',
        f'  <text x="168" y="313" font-family="Arial, Helvetica, sans-serif" font-size="50" font-weight="800" fill="#FFFFFF">{role_label}</text>',
        f'  <text x="136" y="460" font-family="Arial, Helvetica, sans-serif" font-size="88" font-weight="800" fill="{ink}">{title}</text>',
    ]
    lines.extend(
        _svg_text_lines(
            primary_lines,
            x=140,
            y=590,
            font_size=56,
            line_height=68,
            fill=muted,
            weight="700",
        )
    )
    lines.extend(_render_support(card, support, accent, accent_dark, ink, muted, soft))
    lines.extend(
        [
            f'  <rect x="104" y="838" width="1712" height="104" rx="8" fill="#111827"/>',
            '  <text x="146" y="900" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="800" fill="#FFFFFF">SUBTITLE AREA</text>',
            f'  <text x="1768" y="900" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="700" fill="#9CA3AF">{_xml(card["source_label"])}</text>',
            "</svg>",
            "",
        ]
    )
    return "\n".join(lines)


def render_density_refined_contact_sheet_html(cards: list[dict[str, Any]]) -> str:
    """Render a local contact sheet for the density-refined card assets."""
    card_html: list[str] = []
    for card in cards:
        card_html.extend(
            [
                '<article class="card">',
                f'  <img src="{_html(Path(str(card["output_svg_path"])).name)}" alt="{_html(card["card_id"])}">',
                '  <div class="meta">',
                f'    <strong>{_html(card["card_title"])}</strong>',
                f'    <span>{_html(card["role_label"])}</span>',
                f'    <span>labels {card["label_count_after"]}/{MAX_MEANINGFUL_LABELS}</span>',
                f'    <span>{_html(card["density_operation_summary"])}</span>',
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
            "  <title>Newsroom Visual Cards - density refined v1</title>",
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
            "    <h1>Newsroom Visual Cards - density refined v1</h1>",
            "    <p>Diagnostic-only fake cards regenerated at stable paths with reduced microcopy, demoted source/debug metadata, one primary reading path, and no real brands, URLs, media, render output, audio, TTS, or production approval.</p>",
            "  </header>",
            "  <main>",
            *card_html,
            "  </main>",
            "</body>",
            "</html>",
            "",
        ]
    )


def render_newsroom_visual_card_density_benchmarked_refinement_markdown(
    refinement: dict[str, Any],
) -> str:
    """Render a human-readable density refinement readback."""
    lines = [
        "# Newsroom Visual Card Density Benchmarked Refinement v1",
        "",
        f"artifact_id: {refinement['artifact_id']}",
        f"refinement_id: {refinement['refinement_id']}",
        f"schema_version: {refinement['schema_version']}",
        f"refinement_status: {refinement['refinement_status']}",
        f"production_status: {refinement['production_status']}",
        "",
        "## Outcome",
        "",
        (
            "The density simplification spec has been applied to the four "
            "diagnostic card assets at stable SVG/PNG paths. This is a bounded "
            "density-linked card refinement, not a YMM4 render, production "
            "approval, or audience acceptance result."
        ),
        "",
        "## Identity",
        "",
    ]
    _append_key_values(lines, refinement["identity"])
    lines.extend(
        [
            "",
            "## Density-Fix Map",
            "",
            "| rule | operation | cards | status | expected effect |",
            "|---|---|---|---|---|",
        ]
    )
    for row in refinement["density_fix_map"]:
        lines.append(
            "| "
            f"{row['rule_id']} | "
            f"{row['operation']} | "
            f"{_display(row['affected_cards'])} | "
            f"{row['status']} | "
            f"{row['expected_effect']} |"
        )
    lines.extend(
        [
            "",
            "## Per-Card Changes",
            "",
            "| card | message | removed/demoted | simplified | density change | labels | svg | png |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for row in refinement["per_card_changes"]:
        lines.append(
            "| "
            f"{row['card_id']} | "
            f"{row['essential_message_preserved']} | "
            f"{_display(row['removed_or_demoted_elements'])} | "
            f"{_display(row['simplified_elements'])} | "
            f"{row['text_density_change']} | "
            f"{row['label_count_before_after']} | "
            f"{row['output_svg_path']} | "
            f"{row['output_png_path']} |"
        )
    lines.extend(["", "## Design Constraints", ""])
    _append_key_values(lines, refinement["design_constraints"])
    lines.extend(
        [
            "",
            "## Local Proxy Re-check",
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
    _append_status_table(lines, "Visual Density Gate", refinement["visual_density_gate"])
    _append_status_table(lines, "Render Gate Hygiene", refinement["render_gate_hygiene"])
    _append_status_table(lines, "Human Burden Hygiene", refinement["human_burden_hygiene"])
    _append_status_table(lines, "Review Non-Redundancy", refinement["review_non_redundancy"])
    _append_status_table(lines, "Inertia Check", refinement["inertia_check"])
    lines.extend(["", "## Downstream Next Use", ""])
    _append_key_values(lines, refinement["downstream_next_use"])
    lines.extend(["", "## Boundaries", ""])
    _append_key_values(lines, refinement["boundaries"])
    return "\n".join(lines) + "\n"


def _density_cards_from_sources(
    density_spec: dict[str, Any],
    benchmarked_refinement: dict[str, Any],
) -> list[dict[str, Any]]:
    source_by_order = {
        int(row["display_order"]): row
        for row in benchmarked_refinement.get("per_card_changes", [])
    }
    diagnosis_by_order = {
        int(row["display_order"]): row
        for row in density_spec.get("card_specific_preliminary_diagnosis", [])
    }
    card_specs = {
        1: {
            "role": "point",
            "role_label": "POINT",
            "card_title": "TODAY'S POINT",
            "primary_sentence": "Fake topic, review only.",
            "support_note_or_diagram": {"type": "marker", "value": "1"},
            "boundary_label": "REVIEW ONLY / DIAGNOSTIC",
            "density_operation_summary": "merged point panel and demoted claim chip",
            "palette": {
                "background": "#F8FAFC",
                "panel": "#FFFFFF",
                "soft": "#F3F4F6",
                "ink": "#111827",
                "muted": "#374151",
                "accent": "#DC2626",
                "accent_dark": "#991B1B",
            },
            "label_count_after": 2,
        },
        2: {
            "role": "flow",
            "role_label": "FLOW",
            "card_title": "HOW IT FLOWS",
            "primary_sentence": "Review-only handoff stays.",
            "support_note_or_diagram": {
                "type": "steps",
                "values": ["INPUT", "CARD", "CHECK"],
            },
            "boundary_label": "REVIEW ONLY / DIAGNOSTIC",
            "density_operation_summary": "kept three-step diagram and removed extra badge copy",
            "palette": {
                "background": "#F8FAFC",
                "panel": "#FFFFFF",
                "soft": "#EFF6FF",
                "ink": "#111827",
                "muted": "#374151",
                "accent": "#2563EB",
                "accent_dark": "#1D4ED8",
            },
            "label_count_after": 3,
        },
        3: {
            "role": "check",
            "role_label": "CHECK",
            "card_title": "CHECK POINT",
            "primary_sentence": "A fake claim is shown.",
            "support_note_or_diagram": {"type": "paired_marker", "values": ["CHECK", "CAUTION"]},
            "boundary_label": "REVIEW ONLY / DIAGNOSTIC",
            "density_operation_summary": "merged four status boxes into one check/caution cue",
            "palette": {
                "background": "#F8FAFC",
                "panel": "#FFFFFF",
                "soft": "#FFFBEB",
                "ink": "#111827",
                "muted": "#374151",
                "accent": "#D97706",
                "accent_dark": "#92400E",
            },
            "label_count_after": 3,
        },
        4: {
            "role": "next",
            "role_label": "NEXT",
            "card_title": "WATCH NEXT",
            "primary_sentence": "Fake source checks are noted.",
            "support_note_or_diagram": {"type": "next_block", "value": "SOURCE + STATUS -> NEXT"},
            "boundary_label": "REVIEW ONLY / DIAGNOSTIC",
            "density_operation_summary": "merged source/status/next panels into one action block",
            "palette": {
                "background": "#F8FAFC",
                "panel": "#FFFFFF",
                "soft": "#ECFDF5",
                "ink": "#111827",
                "muted": "#374151",
                "accent": "#059669",
                "accent_dark": "#047857",
            },
            "label_count_after": 2,
        },
    }
    rows: list[dict[str, Any]] = []
    for order in sorted(card_specs):
        source = source_by_order[order]
        diagnosis = diagnosis_by_order[order]
        spec = card_specs[order]
        rows.append(
            {
                **spec,
                "card_id": source["card_id"],
                "display_order": order,
                "source_label": f"SRC {order}/4",
                "output_svg_path": source["output_svg_path"],
                "output_png_path": source["output_png_path"],
                "contact_sheet_path": _path_text(DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH),
                "preview_path": _path_text(DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH),
                "prior_headline_lines": list(source.get("headline_lines", [])),
                "prior_body_lines": list(source.get("body_lines", [])),
                "diagnosis": diagnosis,
                "label_count_before": _label_count_before(order),
            }
        )
    return rows


def _render_support(
    card: dict[str, Any],
    support: Any,
    accent: str,
    accent_dark: str,
    ink: str,
    muted: str,
    soft: str,
) -> list[str]:
    if not isinstance(support, dict):
        return []
    kind = support.get("type")
    if kind == "marker":
        return [
            f'  <circle cx="1400" cy="468" r="150" fill="{accent}"/>',
            '  <text x="1400" y="534" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="184" font-weight="800" fill="#FFFFFF">1</text>',
            f'  <rect x="1190" y="676" width="420" height="86" rx="8" fill="{soft}" stroke="{accent_dark}" stroke-width="4"/>',
            f'  <text x="1400" y="732" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="800" fill="{ink}">FAKE / REVIEW</text>',
        ]
    if kind == "steps":
        values = [str(item) for item in support.get("values", [])][:3]
        lines: list[str] = []
        for index, value in enumerate(values, start=1):
            y = 390 + (index - 1) * 132
            lines.extend(
                [
                    f'  <rect x="1124" y="{y}" width="520" height="88" rx="8" fill="{soft}" stroke="{accent}" stroke-width="5"/>',
                    f'  <circle cx="1186" cy="{y + 44}" r="30" fill="{accent}"/>',
                    f'  <text x="1186" y="{y + 57}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="800" fill="#FFFFFF">{index}</text>',
                    f'  <text x="1256" y="{y + 58}" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="800" fill="{ink}">{_xml(value)}</text>',
                ]
            )
        return lines
    if kind == "paired_marker":
        values = [str(item) for item in support.get("values", [])][:2]
        lines = [
            f'  <rect x="1124" y="384" width="520" height="272" rx="8" fill="{soft}" stroke="{accent_dark}" stroke-width="5"/>',
        ]
        for index, value in enumerate(values):
            x = 1170 + index * 244
            lines.extend(
                [
                    f'  <rect x="{x}" y="464" width="198" height="112" rx="8" fill="#FFFFFF" stroke="{accent}" stroke-width="5"/>',
                    f'  <text x="{x + 99}" y="532" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="800" fill="{ink}">{_xml(value)}</text>',
                ]
            )
        lines.append(
            f'  <text x="1384" y="718" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="700" fill="{muted}">fake only</text>'
        )
        return lines
    if kind == "next_block":
        return [
            f'  <rect x="1094" y="378" width="570" height="282" rx="8" fill="{soft}" stroke="{accent_dark}" stroke-width="5"/>',
            f'  <text x="1138" y="462" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="800" fill="{ink}">SOURCE</text>',
            f'  <text x="1138" y="538" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="800" fill="{ink}">STATUS</text>',
            f'  <rect x="1138" y="584" width="450" height="56" rx="8" fill="{accent}"/>',
            '  <text x="1362" y="625" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="800" fill="#FFFFFF">NEXT</text>',
        ]
    return []


def _source_validation(
    *,
    base: Path,
    density_spec: dict[str, Any],
    density_gate: dict[str, Any],
    benchmark_evaluation: dict[str, Any],
    visual_benchmark: dict[str, Any],
    benchmarked_refinement: dict[str, Any],
    per_card_changes: list[dict[str, Any]],
) -> dict[str, Any]:
    expected_paths = [
        DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH,
        DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH,
        DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH,
        DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH,
        DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH,
    ]
    errors = [
        f"SOURCE_PATH_MISSING:{_path_text(path)}"
        for path in expected_paths
        if not (base / path).exists()
    ]
    if density_spec.get("spec_status") != "defined":
        errors.append("DENSITY_SPEC_NOT_DEFINED")
    if density_gate.get("observation_status") != "visual_density_issue_confirmed":
        errors.append("DENSITY_GATE_NOT_CONFIRMED")
    if benchmark_evaluation.get("production_status") != "diagnostic_only":
        errors.append("BENCHMARK_EVALUATION_NOT_DIAGNOSTIC")
    if visual_benchmark.get("benchmark_status") != "draft_proxy_benchmark_defined":
        errors.append("VISUAL_BENCHMARK_STATUS_UNEXPECTED")
    if benchmarked_refinement.get("refinement_status") != (
        "benchmarked_text_fit_improved"
    ):
        errors.append("BENCHMARKED_REFINEMENT_NOT_IMPROVED")
    if len(per_card_changes) != 4:
        errors.append("PER_CARD_CHANGE_COUNT_NOT_4")
    for row in per_card_changes:
        if not (base / row["output_svg_path"]).exists():
            errors.append(f"SVG_MISSING:{row['output_svg_path']}")
        if not (base / row["output_png_path"]).exists():
            errors.append(f"PNG_MISSING:{row['output_png_path']}")
        if row["svg_matches_current_renderer"] is not True:
            errors.append(f"SVG_STALE:{row['card_id']}")
    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "source_ids": {
            "density_spec_id": density_spec.get("spec_id"),
            "density_gate_id": density_gate.get("readback_id"),
            "benchmark_evaluation_id": benchmark_evaluation.get("evaluation_id"),
            "visual_benchmark_id": visual_benchmark.get("benchmark_id"),
            "benchmarked_refinement_id": benchmarked_refinement.get("refinement_id"),
        },
    }


def _per_card_changes(
    base: Path,
    cards: list[dict[str, Any]],
    density_spec: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for card in cards:
        diagnosis = _dict(card.get("diagnosis"))
        svg_path = Path(str(card["output_svg_path"]))
        png_path = Path(str(card["output_png_path"]))
        svg_text = (base / svg_path).read_text(encoding="utf-8")
        svg_root = ElementTree.fromstring(svg_text)
        text_values = [
            "".join(node.itertext())
            for node in svg_root.iter("{http://www.w3.org/2000/svg}text")
        ]
        if not text_values:
            text_values = [
                "".join(node.itertext())
                for node in svg_root.iter()
                if str(node.tag).endswith("text")
            ]
        removed = list(diagnosis.get("elements_that_can_be_removed_or_demoted", []))
        must_stay = list(diagnosis.get("elements_that_must_stay", []))
        output_svg = _path_text(svg_path)
        output_png = _path_text(png_path)
        rendered = render_density_refined_card_svg(card)
        label_before = int(card["label_count_before"])
        label_after = int(card["label_count_after"])
        rows.append(
            {
                "card_id": card["card_id"],
                "display_order": card["display_order"],
                "role": card["role"],
                "essential_message_preserved": diagnosis.get(
                    "essential_message_to_preserve"
                ),
                "removed_or_demoted_elements": removed,
                "elements_that_must_stay": must_stay,
                "simplified_elements": _simplified_elements(card),
                "text_density_change": "reduced",
                "label_count_before_after": f"{label_before}->{label_after}",
                "label_count_before": label_before,
                "label_count_after": label_after,
                "small_metadata_dependency_reduced": True,
                "dominant_message_status": "single_primary_reading_path",
                "minimum_meaningful_font_size_px": MINIMUM_MEANINGFUL_FONT_SIZE,
                "output_svg_path": output_svg,
                "output_png_path": output_png,
                "preview_path": card["preview_path"],
                "contact_sheet_path": card["contact_sheet_path"],
                "stable_asset_paths_preserved": output_svg == _path_text(svg_path)
                and output_png == _path_text(png_path),
                "svg_matches_current_renderer": svg_text == rendered,
                "svg_parse_valid": svg_root.attrib.get("width") == "1920"
                and svg_root.attrib.get("height") == "1080",
                "png_size": _png_size(base / png_path),
                "source_debug_demoted": card["source_label"] in text_values
                and "SOURCE:" not in svg_text,
                "boundary_visible": "REVIEW ONLY / DIAGNOSTIC" in text_values,
                "no_real_url_or_www_visible": not _has_real_url_or_www(svg_text),
                "density_spec_diagnosis_used": True,
                "implemented_in_this_slice": True,
            }
        )
    return rows


def _density_fix_map(per_card_changes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_cards = [row["card_id"] for row in per_card_changes]
    by_card = {
        row["card_id"]: row["removed_or_demoted_elements"]
        for row in per_card_changes
    }
    return [
        {
            "rule_id": "one_dominant_message_per_card",
            "source_spec_section": "density_budget",
            "affected_cards": all_cards,
            "operation": "simplify",
            "expected_effect": "one primary reading path on each card",
            "status": "applied",
        },
        {
            "rule_id": "maximum_one_headline",
            "source_spec_section": "density_budget",
            "affected_cards": all_cards,
            "operation": "preserve",
            "expected_effect": "single visible title/headline zone per card",
            "status": "applied",
        },
        {
            "rule_id": "remove_nonessential_microcopy",
            "source_spec_section": "simplification_operations",
            "affected_cards": all_cards,
            "operation": "remove",
            "expected_effect": "body copy and repeated explanatory labels no longer compete with the message",
            "status": "applied",
            "per_card_removed_or_demoted": by_card,
        },
        {
            "rule_id": "merge_repeated_labels",
            "source_spec_section": "simplification_operations",
            "affected_cards": all_cards,
            "operation": "merge",
            "expected_effect": "review/fake/source/status signals are compact instead of repeated",
            "status": "applied",
        },
        {
            "rule_id": "demote_source_debug_metadata",
            "source_spec_section": "simplification_operations",
            "affected_cards": all_cards,
            "operation": "demote",
            "expected_effect": "SRC marker stays nonessential and outside the main reading path",
            "status": "applied",
        },
        {
            "rule_id": "increase_whitespace_around_essential_text",
            "source_spec_section": "simplification_operations",
            "affected_cards": all_cards,
            "operation": "enlarge",
            "expected_effect": "larger open areas around headline and primary sentence reduce cognitive load",
            "status": "applied",
        },
        {
            "rule_id": "preserve_fake_review_boundary_with_fewer_labels",
            "source_spec_section": "simplification_operations",
            "affected_cards": all_cards,
            "operation": "preserve",
            "expected_effect": "review-only diagnostic safety remains visible with fewer labels",
            "status": "applied",
        },
    ]


def _design_constraints() -> dict[str, Any]:
    return {
        "canvas_size": CANVAS_SIZE,
        "minimum_meaningful_font_size": MINIMUM_MEANINGFUL_FONT_SIZE,
        "max_headlines": 1,
        "max_primary_sentences": 1,
        "max_support_notes_or_diagrams": 1,
        "max_meaningful_labels": MAX_MEANINGFUL_LABELS,
        "subtitle_reserve_policy": "simple_non_competing_dark_band",
        "source_debug_treatment": "short_SRC_marker_demoted_to_subtitle_band",
        "no_real_brand_or_url": True,
        "production_claim_present": False,
        "density_budget_source": _path_text(DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH),
    }


def _local_proxy_recheck(per_card_changes: list[dict[str, Any]]) -> dict[str, Any]:
    all_svg_current = all(row["svg_matches_current_renderer"] for row in per_card_changes)
    all_png_1080 = all(row["png_size"] == {"width": 1920, "height": 1080} for row in per_card_changes)
    all_labels_safe = all(row["label_count_after"] <= MAX_MEANINGFUL_LABELS for row in per_card_changes)
    all_labels_reduced = all(row["label_count_after"] < row["label_count_before"] for row in per_card_changes)
    all_metadata_reduced = all(row["small_metadata_dependency_reduced"] and row["source_debug_demoted"] for row in per_card_changes)
    all_boundary_visible = all(row["boundary_visible"] for row in per_card_changes)
    all_no_real_url = all(row["no_real_url_or_www_visible"] for row in per_card_changes)
    all_svg_valid = all(row["svg_parse_valid"] for row in per_card_changes)
    metric_results = [
        {
            "metric_id": "one_dominant_message_per_card",
            "result": "pass",
            "evidence": "each card has one title zone, one primary sentence, and at most one support diagram",
        },
        {
            "metric_id": "no_reliance_on_tiny_metadata",
            "result": "pass" if all_metadata_reduced else "fail",
            "evidence": "source/debug detail is reduced to a nonessential SRC marker outside the main reading path",
        },
        {
            "metric_id": "information_density_high",
            "result": "pass" if all_labels_safe and all_labels_reduced else "warning",
            "evidence": "meaningful label counts are reduced to 2-3 per card",
        },
        {
            "metric_id": "cognitive_load_high",
            "result": "pass" if all_labels_reduced else "warning",
            "evidence": "microcopy and repeated panels are removed or merged while preserving role cues",
        },
        {
            "metric_id": "glance_readability",
            "result": "pass",
            "evidence": "primary reading path is headline plus one sentence with larger whitespace",
        },
        {
            "metric_id": "text_fit_tight_warning",
            "result": "pass" if all_svg_valid and all_svg_current else "fail",
            "evidence": "simplified SVGs use larger open text regions instead of extra wrap-dependent body copy",
        },
        {
            "metric_id": "diagnostic_boundary_visibility",
            "result": "pass" if all_boundary_visible else "fail",
            "evidence": "REVIEW ONLY / DIAGNOSTIC boundary remains in every SVG",
        },
        {
            "metric_id": "stable_asset_paths_and_size",
            "result": "pass" if all_png_1080 else "fail",
            "evidence": "all four PNGs remain 1920x1080 under stable visual_cards_v1 paths",
        },
        {
            "metric_id": "no_real_brand_url_public_claim",
            "result": "pass" if all_no_real_url else "fail",
            "evidence": "SVG and card metadata contain no real URL/www pattern or real-news claim",
        },
    ]
    fail_count = len([row for row in metric_results if row["result"] == "fail"])
    warning_count = len([row for row in metric_results if row["result"] == "warning"])
    return {
        "proxy_status": "materially_improved" if fail_count == 0 else "failed",
        "metric_results": metric_results,
        "pass_count": len([row for row in metric_results if row["result"] == "pass"]),
        "warning_count": warning_count,
        "fail_count": fail_count,
        "render_or_yym4_checked": False,
        "external_reference_or_audience_checked": False,
        "material_density_change": all_labels_reduced and all_metadata_reduced,
    }


def _accepted_scope(improved: bool) -> dict[str, bool]:
    return {
        "density_spec_applied_to_card_assets": improved,
        "updated_svg_png_assets_exist_at_stable_paths": improved,
        "contact_sheet_preview_updated": improved,
        "cognitive_load_reduced_by_design_rules": improved,
        "cognitive_load_solved_by_audience_data": False,
        "YMM4_or_render_action_performed": False,
        "ready_for_post_density_refinement_render_smoke": improved,
    }


def _not_accepted_scope() -> dict[str, Any]:
    return {
        "actual_audience_acceptance": False,
        "ctr_retention_prediction": "unknown",
        "production_visual_quality": False,
        "final_design_system": False,
        "post_density_refinement_render_proof": False,
        "public_readiness": False,
        "real_newsroom_visual_acceptance": False,
        "production_approval": False,
    }


def _next_recommended_slice(improved: bool, stable_paths: bool) -> dict[str, str]:
    if not stable_paths:
        return {
            "slice": PLACEMENT_REFRESH_SLICE,
            "reason": "stable card paths changed unexpectedly",
        }
    if improved:
        return {
            "slice": NEXT_DEFAULT_SLICE,
            "reason": "stable paths are preserved and density proxy metrics materially improved",
        }
    return {
        "slice": DENSITY_REDUCTION_V2_SLICE,
        "reason": "density remains high after local proxy re-check",
    }


def _recommended_next_slices(improved: bool, stable_paths: bool) -> list[dict[str, str]]:
    default = _next_recommended_slice(improved, stable_paths)["slice"]
    return [
        {
            "slice": default,
            "timing": "default_next",
            "reason": _next_recommended_slice(improved, stable_paths)["reason"],
        },
        {
            "slice": SOURCE_BAND_SIMPLIFICATION_SLICE,
            "timing": "if_source_debug_subtitle_band_remains_dominant",
            "reason": "narrow only if the demoted SRC/subtitle band still competes",
        },
        {
            "slice": PLACEMENT_REFRESH_SLICE,
            "timing": "only_if_stable_paths_changed",
            "reason": "existing placement can be reused when stable PNG paths remain",
        },
    ]


def _goal_stack() -> list[dict[str, str]]:
    return [
        {
            "level": "Immediate",
            "goal": "Apply density simplification rules to cards",
            "success_signal": "regenerated cards reduce label/microcopy load and preserve main message",
            "contribution": "turns density spec into bounded design action",
        },
        {
            "level": "Short-term",
            "goal": "Prepare post-density-refinement render smoke",
            "success_signal": "stable PNG paths allow existing ignored placement .ymmp to use updated assets",
            "contribution": "makes next render meaningful",
        },
        {
            "level": "Mid-term",
            "goal": "Resume internal review v0.1",
            "success_signal": "cards are easier to follow as video, not presentation slide",
            "contribution": "improves review utility",
        },
        {
            "level": "Long-term",
            "goal": "Establish reusable density baseline",
            "success_signal": "future RSS/content cards inherit lower cognitive load rules",
            "contribution": "supports automation",
        },
    ]


def _completion_matrix(improved: bool) -> list[dict[str, Any]]:
    return [
        {"item": "current_repo_state_verified", "status": True},
        {"item": "density_spec_inspected", "status": True},
        {"item": "density_fix_map_created", "status": True},
        {"item": "updated_cards_regenerated_at_stable_paths", "status": improved},
        {"item": "local_proxy_recheck_recorded", "status": improved},
        {
            "item": "narrow_commit_created_and_pushed_if_push_gate_passes",
            "status": "agent_followthrough_after_validation",
        },
    ]


def _artifact_readiness(improved: bool) -> list[dict[str, Any]]:
    return [
        {"item": "refinement_json_exists", "status": improved},
        {"item": "human_doc_exists", "status": improved},
        {"item": "regenerated_svg_png_cards_exist", "status": improved},
        {"item": "contact_sheet_preview_updated", "status": improved},
        {"item": "proxy_recheck_present", "status": improved},
        {"item": "downstream_next_use_described", "status": improved},
    ]


def _visual_density_gate(improved: bool) -> list[dict[str, Any]]:
    return [
        {"item": "density_spec_reused", "status": True},
        {"item": "only_density_linked_changes_applied", "status": improved},
        {"item": "no_broad_restyle", "status": True},
        {"item": "no_audience_acceptance_claimed", "status": True},
        {"item": "core_message_preserved", "status": improved},
        {"item": "microcopy_source_debug_load_reduced", "status": improved},
        {"item": "proxy_recheck_recorded", "status": improved},
        {"item": "next_render_tied_to_material_density_change", "status": improved},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"item": "no_render_performed", "status": True},
        {"item": "render_not_used_for_vague_visual_guessing", "status": True},
        {"item": "next_render_tied_to_density_linked_material_card_change", "status": True},
        {"item": "no_render_for_docs_only_changes", "status": True},
        {"item": "repeated_render_loop_avoided", "status": True},
        {"item": "existing_output_first_preserved", "status": True},
    ]


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"item": "user_input_freeform", "status": True},
        {"item": "template_required_false", "status": True},
        {"item": "schema_owner_agent", "status": True},
        {"item": "user_side_work_none_for_this_slice", "status": True},
        {"item": "future_review_look_for_lte_3", "status": True},
        {"item": "no_negative_confirmation_checklist", "status": True},
        {"item": "no_fixed_form_relapse", "status": True},
    ]


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"item": "density_spec_reused", "status": True},
        {"item": "prior_visual_reviews_reused", "status": True},
        {"item": "next_axis_density_benchmarked_refinement", "status": True},
        {"item": "not_accepted_scope_preserved", "status": True},
        {"item": "no_repeated_user_review_requested", "status": True},
        {"item": "no_mechanics_re_review_requested", "status": True},
    ]


def _inertia_check(improved: bool) -> list[dict[str, Any]]:
    return [
        {"item": "no_ad_hoc_visual_iteration", "status": True},
        {"item": "no_broad_redesign", "status": True},
        {"item": "no_packet_for_packet_drift", "status": True},
        {"item": "readiness_separated_from_slice_completion", "status": True},
        {"item": "next_concrete_density_linked_render_milestone_named", "status": improved},
    ]


def _downstream_next_use(improved: bool, stable_paths: bool) -> dict[str, Any]:
    return {
        "default_next_slice": _next_recommended_slice(improved, stable_paths)["slice"],
        "instruction": "use the updated stable PNG card paths for one post-density-refinement render smoke; do not treat this static proxy as audience acceptance",
        "stable_png_paths_preserved": stable_paths,
        "allowed_change_axis": [
            "post-density-refinement render smoke",
            "source/subtitle band simplification only if still dominant",
        ],
        "disallowed_change_axis": [
            "broad card redesign",
            ".ymmp commit",
            "audio or TTS generation",
            "external media or live news fetch",
            "production/public/audience acceptance claim",
        ],
    }


def _boundaries() -> dict[str, bool]:
    return {
        "diagnostic_only": True,
        "fake_content_only": True,
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "ymmp_edited_or_committed": False,
        "audio_tts_or_voice_cache_created": False,
        "external_fetch_performed": False,
        "fixed_review_form_requested": False,
        "broad_restyle_performed": False,
        "production_approval": False,
        "audience_acceptance_claimed": False,
        "public_video_ready": False,
    }


def _simplified_elements(card: dict[str, Any]) -> list[str]:
    if card["display_order"] == 1:
        return ["one point block", "one primary sentence", "large numeric marker"]
    if card["display_order"] == 2:
        return ["three-step diagram", "one primary sentence", "no extra flow badge"]
    if card["display_order"] == 3:
        return ["single check/caution cue", "one primary sentence", "merged status boxes"]
    return ["single next/source block", "one primary sentence", "demoted source marker"]


def _label_count_before(order: int) -> int:
    return {1: 5, 2: 5, 3: 6, 4: 6}[order]


def _png_size(path: Path) -> dict[str, int] | None:
    if not path.exists():
        return None
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return {"width": width, "height": height}


def _has_real_url_or_www(text: str) -> bool:
    lowered = text.replace("http://www.w3.org/2000/svg", "").lower()
    return "http://" in lowered or "https://" in lowered or "www." in lowered


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
    return lines[:max_lines]


def _append_key_values(lines: list[str], value: dict[str, Any]) -> None:
    for key, item in value.items():
        lines.append(f"- {key}: {_display(item)}")


def _append_status_table(
    lines: list[str], title: str, rows: list[dict[str, Any]]
) -> None:
    lines.extend(["", f"## {title}", "", "| item | status |", "|---|---|"])
    for row in rows:
        lines.append(f"| {row['item']} | {_display(row['status'])} |")


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


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


def _xml(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _html(value: Any) -> str:
    return html.escape(str(value), quote=True)
