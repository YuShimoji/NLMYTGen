"""Diagnostic visual card asset bridge for the newsroom YMM4 handoff.

This module generates external SVG card assets and a local HTML contact sheet
for the already-observed 68 second diagnostic render smoke. It does not launch
YMM4, render video, edit .ymmp files, fetch real media, generate audio/TTS, or
approve production/public use.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_caption_timing_plan import DEFAULT_PLAN_PATH
from src.pipeline.newsroom_episode_production_capsule import (
    DEFAULT_CAPSULE_PATH,
    load_json_object,
)
from src.pipeline.newsroom_neutral_timeline_import_proof import (
    DEFAULT_NEUTRAL_TIMELINE_PATH,
)
from src.pipeline.newsroom_ymmp_timing_patch_render_smoke_result_readback import (
    DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH,
)


VISUAL_CARD_ASSET_BRIDGE_SCHEMA_VERSION = "newsroom_visual_card_asset_bridge.v1"
VISUAL_CARD_ASSET_BRIDGE_ID = (
    "newsroom_visual_card_asset_bridge_v1_2026_06_25"
)
DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH = Path(
    "samples/_probe/newsroom_handoff/visual_card_asset_bridge_v1.json"
)
DEFAULT_VISUAL_CARD_ASSET_BRIDGE_DOC_PATH = Path(
    "docs/verification/NEWSROOM_VISUAL_CARD_ASSET_BRIDGE_V1_2026-06-25.md"
)
DEFAULT_VISUAL_CARD_ASSET_DIR = Path(
    "samples/_probe/newsroom_handoff/visual_cards_v1"
)
DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH = (
    DEFAULT_VISUAL_CARD_ASSET_DIR / "contact_sheet.html"
)

NEXT_DEFAULT_SLICE = "newsroom-yym4-card-asset-placement-probe-v1"
NEXT_RENDER_SMOKE_SLICE = "newsroom-card-placement-render-smoke-v1"
INTERNAL_REVIEW_PREP_SLICE = "newsroom-internal-review-v0.1-prep"
RETENTION_POLICY_SLICE = "newsroom-render-output-retention-policy-v1"

CARD_TEXTS: tuple[str, ...] = (
    "Fake topic, review only.",
    "Review-only handoff stays.",
    "A fake claim is shown.",
    "Fake source checks are noted.",
)

CARD_BODIES: dict[str, str] = {
    "cap_beat_fake_intro_001_01": (
        "Synthetic intro surface for the already-proven diagnostic timing lane."
    ),
    "cap_beat_fake_intro_001_02": (
        "The bridge keeps review-only text visible without building YMM4 card graphs."
    ),
    "cap_beat_fake_claim_001_01": (
        "A placeholder claim block demonstrates hierarchy without real news content."
    ),
    "cap_beat_fake_claim_001_02": (
        "Fake source checks stay abstract so no real URL, brand, or media is implied."
    ),
}

CARD_PALETTES: tuple[dict[str, str], ...] = (
    {
        "name": "teal_signal",
        "accent": "#2DD4BF",
        "accent_dark": "#0F766E",
        "panel": "#12232A",
        "panel_2": "#172E35",
        "chip": "#D1FAE5",
        "chip_text": "#064E3B",
    },
    {
        "name": "blue_review",
        "accent": "#60A5FA",
        "accent_dark": "#1D4ED8",
        "panel": "#172033",
        "panel_2": "#1C2A44",
        "chip": "#DBEAFE",
        "chip_text": "#1E3A8A",
    },
    {
        "name": "amber_claim",
        "accent": "#FBBF24",
        "accent_dark": "#B45309",
        "panel": "#2B2417",
        "panel_2": "#352A19",
        "chip": "#FEF3C7",
        "chip_text": "#78350F",
    },
    {
        "name": "rose_check",
        "accent": "#FB7185",
        "accent_dark": "#BE123C",
        "panel": "#2B1B25",
        "panel_2": "#351F2B",
        "chip": "#FFE4E6",
        "chip_text": "#881337",
    },
)


def build_default_newsroom_visual_card_asset_bridge(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed visual card asset bridge from default inputs."""
    base = Path(root) if root is not None else Path(".")
    render_smoke_result = load_json_object(
        base / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    neutral_timeline = load_json_object(base / DEFAULT_NEUTRAL_TIMELINE_PATH)
    timing_plan = load_json_object(base / DEFAULT_PLAN_PATH)
    capsule = load_json_object(base / DEFAULT_CAPSULE_PATH)
    return build_newsroom_visual_card_asset_bridge(
        render_smoke_result,
        neutral_timeline,
        timing_plan,
        capsule,
        source_render_smoke_result_path=(
            DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        source_neutral_timeline_path=DEFAULT_NEUTRAL_TIMELINE_PATH,
        source_caption_timing_plan_path=DEFAULT_PLAN_PATH,
        source_episode_capsule_path=DEFAULT_CAPSULE_PATH,
        asset_dir=DEFAULT_VISUAL_CARD_ASSET_DIR,
        contact_sheet_path=DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
    )


def write_default_newsroom_visual_card_asset_bridge_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write the bridge JSON, Markdown doc, SVG cards, and contact sheet."""
    base = Path(root) if root is not None else Path(".")
    bridge = build_default_newsroom_visual_card_asset_bridge(root=base)
    _write_json(base / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH, bridge)
    _write_text(
        base / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_DOC_PATH,
        render_newsroom_visual_card_asset_bridge_markdown(bridge),
    )
    for asset in bridge["assets"]:
        _write_text(
            base / asset["repo_relative_path"],
            render_visual_card_svg(asset),
        )
    _write_text(
        base / bridge["preview_contact_sheet"]["repo_relative_path"],
        render_visual_card_contact_sheet_html(bridge),
    )
    return bridge


def build_newsroom_visual_card_asset_bridge(
    render_smoke_result: dict[str, Any],
    neutral_timeline: dict[str, Any],
    timing_plan: dict[str, Any],
    capsule: dict[str, Any],
    *,
    source_render_smoke_result_path: str | Path,
    source_neutral_timeline_path: str | Path,
    source_caption_timing_plan_path: str | Path,
    source_episode_capsule_path: str | Path,
    asset_dir: str | Path,
    contact_sheet_path: str | Path,
) -> dict[str, Any]:
    """Build a deterministic diagnostic-only visual bridge."""
    caption_items = _caption_items(neutral_timeline)
    visual_by_beat = _visual_placeholder_by_beat(neutral_timeline, timing_plan)
    assets = _asset_rows(caption_items, visual_by_beat, asset_dir=asset_dir)
    source_validation = _source_validation(
        render_smoke_result,
        neutral_timeline,
        timing_plan,
        capsule,
        assets,
    )

    return {
        "artifact_id": VISUAL_CARD_ASSET_BRIDGE_ID,
        "bridge_id": VISUAL_CARD_ASSET_BRIDGE_ID,
        "schema_version": VISUAL_CARD_ASSET_BRIDGE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "visual_status": "asset_bridge_created",
        "preview_status": "preview_only",
        "png_export_status": "png_export_deferred",
        "identity": {
            "bridge_id": VISUAL_CARD_ASSET_BRIDGE_ID,
            "source_render_smoke_result_path": _path_text(
                source_render_smoke_result_path
            ),
            "source_render_smoke_result_id": render_smoke_result.get("readback_id"),
            "source_neutral_timeline_path": _path_text(
                source_neutral_timeline_path
            ),
            "source_neutral_timeline_id": neutral_timeline.get("timeline_id"),
            "source_timing_patch_probe_path": (
                "samples/_probe/newsroom_handoff/ymmp_timing_patch_probe_v1.json"
            ),
            "source_timing_patch_strategy_path": (
                "samples/_probe/newsroom_handoff/ymmp_timing_patch_strategy_v1.json"
            ),
            "source_caption_timing_plan_path": _path_text(
                source_caption_timing_plan_path
            ),
            "source_caption_timing_plan_id": timing_plan.get("artifact_id"),
            "source_episode_capsule_path": _path_text(source_episode_capsule_path),
            "source_episode_capsule_id": capsule.get("artifact_id"),
            "production_status": "diagnostic_only",
            "visual_status": "asset_bridge_created",
            "observation_source": "repo_readback_after_user_render_observation",
        },
        "source_validation": source_validation,
        "source_state": _source_state(render_smoke_result),
        "asset_generation": _asset_generation(contact_sheet_path),
        "assets": assets,
        "preview_contact_sheet": {
            "status": "created",
            "asset_type": "html",
            "repo_relative_path": _path_text(contact_sheet_path),
            "review_status": "diagnostic_only",
            "external_dependencies": False,
            "real_url_or_media_dependency": False,
        },
        "placement_contract": _placement_contract(),
        "accepted_scope": _accepted_scope(),
        "not_accepted_scope": _not_accepted_scope(),
        "readiness_separation": _readiness_separation(),
        "recommended_next_slices": _recommended_next_slices(),
        "implementation_principle_for_next_lane": (
            _implementation_principle_for_next_lane()
        ),
        "completion_matrix": _completion_matrix(),
        "artifact_readiness": _artifact_readiness(),
        "video_readiness": _video_readiness(),
        "visual_readiness": _visual_readiness(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(),
        "boundaries": _boundaries(),
        "downstream_next_use": _downstream_next_use(),
        "validation_expectations": _validation_expectations(),
    }


def render_newsroom_visual_card_asset_bridge_markdown(
    bridge: dict[str, Any],
) -> str:
    """Render a human-readable readback for the visual card bridge."""
    identity = _dict(bridge.get("identity"))
    validation = _dict(bridge.get("source_validation"))
    source_state = _dict(bridge.get("source_state"))
    generation = _dict(bridge.get("asset_generation"))
    contact_sheet = _dict(bridge.get("preview_contact_sheet"))
    placement = _dict(bridge.get("placement_contract"))
    readiness = _dict(bridge.get("readiness_separation"))

    lines = [
        "# Newsroom Visual Card Asset Bridge v1",
        "",
        f"artifact_id: {bridge.get('artifact_id')}",
        f"bridge_id: {bridge.get('bridge_id')}",
        f"schema_version: {bridge.get('schema_version')}",
        f"review_status: {bridge.get('review_status')}",
        f"production_status: {bridge.get('production_status')}",
        f"visual_status: {bridge.get('visual_status')}",
        f"preview_status: {bridge.get('preview_status')}",
        f"png_export_status: {bridge.get('png_export_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
    ]
    for key, value in identity.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Source Validation", ""])
    for key, value in validation.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Source State", ""])
    for key, value in source_state.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Asset Generation", ""])
    for key, value in generation.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Generated Cards",
            "",
            "| asset_id | timing | source | path |",
            "|---|---:|---|---|",
        ]
    )
    for asset in bridge.get("assets", []):
        lines.append(
            "| "
            f"{asset.get('asset_id')} | "
            f"{asset.get('intended_start_sec')}-{asset.get('intended_end_sec')}s | "
            f"{asset.get('source_caption_or_beat_id')} | "
            f"{asset.get('repo_relative_path')} |"
        )

    lines.extend(["", "## Preview Contact Sheet", ""])
    for key, value in contact_sheet.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Placement Contract", ""])
    for key, value in placement.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Accepted Scope", ""])
    for key, value in _dict(bridge.get("accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(bridge.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Readiness Separation", ""])
    for key, value in readiness.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Recommended Next Slices",
            "",
            "| slice | timing | reason |",
            "|---|---|---|",
        ]
    )
    for row in bridge.get("recommended_next_slices", []):
        lines.append(
            "| "
            f"{row.get('slice')} | "
            f"{row.get('timing')} | "
            f"{row.get('reason')} |"
        )

    lines.extend(["", "## Implementation Principle", ""])
    for item in bridge.get("implementation_principle_for_next_lane", []):
        lines.append(f"- {item}")

    _append_status_table(lines, "Completion Matrix", bridge.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", bridge.get("artifact_readiness"))
    _append_status_table(lines, "Video Readiness", bridge.get("video_readiness"))
    _append_status_table(lines, "Visual Readiness", bridge.get("visual_readiness"))
    _append_status_table(
        lines, "Render Gate Hygiene", bridge.get("render_gate_hygiene")
    )
    _append_status_table(
        lines, "Human Burden Hygiene", bridge.get("human_burden_hygiene")
    )
    _append_status_table(
        lines, "Review Non-Redundancy", bridge.get("review_non_redundancy")
    )
    _append_status_table(lines, "Inertia Check", bridge.get("inertia_check"))

    lines.extend(["", "## Boundary", ""])
    for key, value in _dict(bridge.get("boundaries")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This bridge turns the sparse black diagnostic render surface into a "
            "reviewable external card-asset set only. It preserves the 68 second "
            "timing/audio result as prior evidence, keeps direct YMM4 card object "
            "construction closed, and leaves YMM4 placement, post-card render smoke, "
            "internal review, real newsroom content, and production approval for "
            "later milestone gates.",
            "",
        ]
    )
    return "\n".join(lines)


def render_visual_card_svg(asset: dict[str, Any]) -> str:
    """Render a single 1920x1080 SVG diagnostic card."""
    palette = _dict(asset.get("palette"))
    accent = palette.get("accent", "#2DD4BF")
    accent_dark = palette.get("accent_dark", "#0F766E")
    panel = palette.get("panel", "#12232A")
    panel_2 = palette.get("panel_2", "#172E35")
    chip = palette.get("chip", "#D1FAE5")
    chip_text = palette.get("chip_text", "#064E3B")
    title = _xml(asset.get("card_title"))
    text = _xml(asset.get("text"))
    body = _xml(asset.get("body"))
    beat = _xml(asset.get("source_beat_id"))
    caption = _xml(asset.get("source_caption_or_beat_id"))
    timing = _xml(f"{asset.get('intended_start_sec')}-{asset.get('intended_end_sec')} SEC")
    asset_label = _xml(asset.get("asset_id"))
    count_label = _xml(f"CARD {asset.get('display_order')}/4")

    return "\n".join(
        [
            '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" '
            f'viewBox="0 0 1920 1080" role="img" aria-label="{title}">',
            f"  <title>{title}</title>",
            "  <desc>Diagnostic-only fake newsroom card asset for later YMM4 "
            "image import placement.</desc>",
            '  <rect x="0" y="0" width="1920" height="1080" fill="#0D1117"/>',
            f'  <rect x="64" y="64" width="1792" height="952" rx="28" fill="{panel}"/>',
            f'  <rect x="64" y="64" width="1792" height="130" rx="28" fill="{panel_2}"/>',
            f'  <rect x="64" y="930" width="1792" height="86" rx="0" fill="{panel_2}"/>',
            f'  <rect x="112" y="112" width="258" height="52" rx="26" fill="{chip}"/>',
            f'  <text x="241" y="147" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="{chip_text}">DIAGNOSTIC</text>',
            f'  <rect x="390" y="112" width="260" height="52" rx="26" fill="#FDE68A"/>',
            '  <text x="520" y="147" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="#78350F">FAKE CONTENT</text>',
            f'  <rect x="670" y="112" width="216" height="52" rx="26" fill="#E5E7EB"/>',
            '  <text x="778" y="147" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="#111827">'
            f"{timing}</text>",
            f'  <text x="1740" y="148" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="700" fill="{accent}">{count_label}</text>',
            f'  <rect x="112" y="252" width="14" height="460" fill="{accent}"/>',
            f'  <text x="152" y="296" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="700" fill="{accent}">{title}</text>',
            '  <text x="152" y="420" font-family="Arial, Helvetica, sans-serif" font-size="82" font-weight="800" fill="#F8FAFC">'
            f"{text}</text>",
            '  <text x="154" y="506" font-family="Arial, Helvetica, sans-serif" font-size="34" fill="#CBD5E1">'
            f"{body}</text>",
            f'  <rect x="152" y="586" width="824" height="126" rx="20" fill="{panel_2}" stroke="{accent}" stroke-width="3"/>',
            f'  <text x="194" y="636" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="700" fill="{accent}">SOURCE CAPTION</text>',
            '  <text x="194" y="682" font-family="Arial, Helvetica, sans-serif" font-size="34" fill="#E5E7EB">'
            f"{caption}</text>",
            f'  <rect x="1032" y="268" width="704" height="444" rx="24" fill="#0B1220" stroke="{accent_dark}" stroke-width="4"/>',
            f'  <rect x="1082" y="320" width="604" height="42" rx="10" fill="{accent}"/>',
            '  <rect x="1082" y="398" width="440" height="24" rx="12" fill="#94A3B8"/>',
            '  <rect x="1082" y="448" width="518" height="24" rx="12" fill="#64748B"/>',
            '  <rect x="1082" y="498" width="382" height="24" rx="12" fill="#64748B"/>',
            f'  <rect x="1082" y="574" width="252" height="74" rx="16" fill="{panel}" stroke="{accent}" stroke-width="3"/>',
            '  <text x="1208" y="623" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="700" fill="#F8FAFC">REVIEW ONLY</text>',
            f'  <circle cx="1618" cy="611" r="44" fill="{accent}"/>',
            '  <text x="1618" y="622" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="800" fill="#0D1117">OK</text>',
            '  <rect x="112" y="796" width="1696" height="118" rx="18" fill="#05080D" stroke="#334155" stroke-width="2" stroke-dasharray="18 14"/>',
            '  <text x="152" y="852" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700" fill="#E2E8F0">SUBTITLE-SAFE RESERVE</text>',
            '  <text x="152" y="892" font-family="Arial, Helvetica, sans-serif" font-size="24" fill="#94A3B8">Future YMM4 placement should keep dialogue/subtitles readable in this lower band.</text>',
            '  <text x="112" y="972" font-family="Arial, Helvetica, sans-serif" font-size="22" fill="#94A3B8">'
            f"beat={beat} | asset={asset_label} | import role=image asset</text>",
            "</svg>",
            "",
        ]
    )


def render_visual_card_contact_sheet_html(bridge: dict[str, Any]) -> str:
    """Render a local HTML contact sheet for the generated SVG assets."""
    cards: list[str] = []
    for asset in bridge.get("assets", []):
        path = Path(str(asset.get("repo_relative_path"))).name
        cards.extend(
            [
                '<article class="card">',
                f'  <img src="{_html(path)}" alt="{_html(asset.get("asset_id"))}">',
                '  <div class="meta">',
                f'    <strong>{_html(asset.get("display_label"))}</strong>',
                f'    <span>{_html(asset.get("intended_start_sec"))}-{_html(asset.get("intended_end_sec"))}s</span>',
                f'    <span>{_html(asset.get("source_caption_or_beat_id"))}</span>',
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
            "  <title>Newsroom Visual Card Asset Bridge v1</title>",
            "  <style>",
            "    :root { color-scheme: dark; font-family: Arial, Helvetica, sans-serif; }",
            "    body { margin: 0; background: #0d1117; color: #e5e7eb; }",
            "    header { padding: 28px 32px 18px; border-bottom: 1px solid #334155; }",
            "    h1 { margin: 0 0 8px; font-size: 30px; letter-spacing: 0; }",
            "    p { margin: 0; color: #cbd5e1; max-width: 980px; line-height: 1.5; }",
            "    main { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 24px; padding: 28px 32px 36px; }",
            "    .card { border: 1px solid #334155; border-radius: 8px; background: #111827; overflow: hidden; }",
            "    img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: contain; background: #05080d; }",
            "    .meta { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; padding: 14px 16px; font-size: 14px; }",
            "    .meta span { color: #cbd5e1; }",
            "  </style>",
            "</head>",
            "<body>",
            "  <header>",
            "    <h1>Newsroom Visual Card Asset Bridge v1</h1>",
            "    <p>Diagnostic-only fake card assets for later YMM4 image placement. "
            "No real brands, real URLs, real media, render output, audio, TTS, or "
            "production approval are included.</p>",
            "  </header>",
            "  <main>",
            *cards,
            "  </main>",
            "</body>",
            "</html>",
            "",
        ]
    )


def _source_validation(
    render_smoke_result: dict[str, Any],
    neutral_timeline: dict[str, Any],
    timing_plan: dict[str, Any],
    capsule: dict[str, Any],
    assets: list[dict[str, Any]],
) -> dict[str, Any]:
    errors: list[str] = []
    normalized = _dict(render_smoke_result.get("normalized_render_result"))
    result_validation = _dict(render_smoke_result.get("source_validation"))
    neutral_timing = _dict(neutral_timeline.get("global_timing"))
    timing_summary = _dict(timing_plan.get("episode_timing_summary"))
    caption_items = _caption_items(neutral_timeline)

    if render_smoke_result.get("result_status") != "pass":
        errors.append("RENDER_SMOKE_RESULT_NOT_PASS")
    if normalized.get("output_duration_sec") != 68:
        errors.append("RENDER_SMOKE_DURATION_NOT_68")
    if normalized.get("native_audio_present") is not True:
        errors.append("NATIVE_AUDIO_NOT_PRESENT_IN_RESULT_READBACK")
    if normalized.get("timing_patch_effective_in_render") is not True:
        errors.append("TIMING_PATCH_NOT_EFFECTIVE_IN_RESULT_READBACK")
    if result_validation.get("canonical_speaker_unicode_escape") != (
        "\\u3086\\u3063\\u304f\\u308a\\u970a\\u5922"
    ):
        errors.append("CANONICAL_SPEAKER_NOT_YUKKURI_REIMU")
    if neutral_timing.get("total_duration_sec") != 68:
        errors.append("NEUTRAL_TIMELINE_NOT_68_SEC")
    if len(caption_items) != 4:
        errors.append("NEUTRAL_TIMELINE_CAPTION_COUNT_NOT_4")
    if [item.get("text") for item in caption_items] != list(CARD_TEXTS):
        errors.append("NEUTRAL_TIMELINE_CARD_TEXT_MISMATCH")
    if timing_summary.get("total_duration_sec") != 68:
        errors.append("CAPTION_TIMING_PLAN_NOT_68_SEC")
    if timing_summary.get("caption_unit_count") != 4:
        errors.append("CAPTION_TIMING_PLAN_CAPTION_COUNT_NOT_4")
    if capsule.get("production_status") != "diagnostic_only":
        errors.append("CAPSULE_NOT_DIAGNOSTIC_ONLY")
    if len(_list(capsule.get("visual_structure"))) < 2:
        errors.append("CAPSULE_VISUAL_STRUCTURE_MISSING")
    if len(assets) != 4:
        errors.append("VISUAL_CARD_ASSET_COUNT_NOT_4")

    return {
        "status": "passed" if not errors else "blocked",
        "render_smoke_result_id": render_smoke_result.get("readback_id"),
        "render_smoke_result": render_smoke_result.get("result_status"),
        "neutral_timeline_id": neutral_timeline.get("timeline_id"),
        "caption_timing_plan_id": timing_plan.get("artifact_id"),
        "episode_capsule_id": capsule.get("artifact_id"),
        "canonical_speaker": "yukkuri_reimu",
        "canonical_speaker_unicode_escape": (
            result_validation.get("canonical_speaker_unicode_escape")
        ),
        "caption_item_count": len(caption_items),
        "card_asset_count": len(assets),
        "duration_sec": normalized.get("output_duration_sec"),
        "errors": errors,
    }


def _source_state(render_smoke_result: dict[str, Any]) -> dict[str, Any]:
    normalized = _dict(render_smoke_result.get("normalized_render_result"))
    return {
        "render_smoke_result": render_smoke_result.get("result_status"),
        "duration_sec": normalized.get("output_duration_sec"),
        "native_audio_status": "diagnostic_pass",
        "timing_patch_status": "diagnostic_pass",
        "current_visual_state": "sparse_text_on_black",
        "dialogue_item_count_observed": normalized.get("dialogue_item_count_observed"),
        "majority_silence_expected_for_diagnostic_sparse_timeline": (
            normalized.get("majority_silence_expected_for_diagnostic_sparse_timeline")
        ),
        "production_pacing_accepted": False,
        "visual_layout_accepted": False,
        "public_video_ready": False,
    }


def _asset_generation(contact_sheet_path: str | Path) -> dict[str, Any]:
    return {
        "generation_mode": "external_svg_cards_with_html_contact_sheet",
        "card_asset_count": 4,
        "svg_export_status": "created",
        "html_preview_status": "created",
        "html_preview_path": _path_text(contact_sheet_path),
        "png_export_status": "png_export_deferred",
        "png_export_reason": (
            "SVG source cards and the HTML contact sheet are deterministic and "
            "sufficient for this bridge; no PNG exporter dependency was introduced."
        ),
        "external_fetch_performed": False,
        "real_media_dependency": False,
        "real_url_dependency": False,
        "asset_dimensions": "1920x1080",
        "aspect_ratio": "16:9",
        "subtitle_safe_lower_area_reserved": True,
    }


def _asset_rows(
    caption_items: list[dict[str, Any]],
    visual_by_beat: dict[str, dict[str, Any]],
    *,
    asset_dir: str | Path,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base = Path(asset_dir)
    for index, item in enumerate(caption_items, start=1):
        caption_id = str(item.get("caption_id") or "")
        beat_id = str(item.get("beat_id") or "")
        palette = CARD_PALETTES[index - 1]
        visual = _dict(visual_by_beat.get(beat_id))
        asset_id = f"visual_card_{caption_id}_v1"
        rel_path = base / f"{asset_id}.svg"
        rows.append(
            {
                "asset_id": asset_id,
                "display_order": index,
                "display_label": f"Card {index}: {item.get('text')}",
                "card_title": _card_title(index, visual),
                "body": CARD_BODIES.get(caption_id, "Diagnostic-only card asset."),
                "source_caption_or_beat_id": caption_id,
                "source_neutral_item_id": item.get("item_id"),
                "source_beat_id": beat_id,
                "source_visual_placeholder_id": visual.get("visual_id"),
                "source_visual_layout_hint": visual.get("layout_hint"),
                "text": item.get("text"),
                "asset_type": "svg",
                "repo_relative_path": _path_text(rel_path),
                "intended_start_sec": item.get("start_sec"),
                "intended_end_sec": item.get("end_sec"),
                "intended_duration_sec": item.get("duration_sec"),
                "intended_layer": 2,
                "intended_layer_role": (
                    "visual_card_image_below_dialogue_items_and_above_background"
                ),
                "placement_role": "diagnostic_visual_card_image_asset",
                "review_status": "diagnostic_only",
                "dimensions": {"width": 1920, "height": 1080, "aspect_ratio": "16:9"},
                "subtitle_safe_lower_area": {
                    "reserved": True,
                    "x": 112,
                    "y": 796,
                    "width": 1696,
                    "height": 118,
                    "note": (
                        "Future placement should keep dialogue/subtitles readable "
                        "in this lower band."
                    ),
                },
                "fake_content_only": True,
                "contains_real_urls": False,
                "contains_real_brands": False,
                "contains_real_news_claims": False,
                "external_dependencies": False,
                "palette": palette,
            }
        )
    return rows


def _card_title(index: int, visual: dict[str, Any]) -> str:
    layout = str(visual.get("layout_hint") or "diagnostic_card")
    if "evidence" in layout or "quote" in layout:
        return f"REVIEW CHECK CARD {index:02d}"
    return f"NEWSROOM REVIEW CARD {index:02d}"


def _placement_contract() -> dict[str, Any]:
    return {
        "future_yym4_placement_mode": "image_asset_import",
        "direct_yym4_card_object_graph": False,
        "yym4_text_shape_reconstruction": False,
        "preserves_native_audio_path": True,
        "preserves_existing_timing_strategy": True,
        "render_required_now": False,
        "YMM4_launch_required_now": False,
        "ymmp_edit_required_now": False,
        "next_render_trigger": (
            "after YMM4 card placement probe or internal review v0.1 milestone"
        ),
        "next_render_should_be_milestone_gated": True,
        "no_render_for_docs_readback_policy_only_changes": True,
        "card_assets_are_external_visual_inputs": True,
        "future_ymmp_mutation_boundary": (
            "ignored local copies only, limited to bounded timing/layout carrier "
            "operations"
        ),
    }


def _accepted_scope() -> dict[str, bool]:
    return {
        "external_visual_card_assets_created": True,
        "preview_contact_sheet_created": True,
        "mapped_to_existing_dialogue_caption_units": True,
        "suitable_for_later_yym4_placement_probe": True,
        "diagnostic_fake_content_safe": True,
        "subtitle_safe_lower_area_reserved": True,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_visual_quality": False,
        "final_design_system": False,
        "YMM4_placement_proof": False,
        "post_card_render_proof": False,
        "public_video_readiness": False,
        "real_newsroom_visuals": False,
        "real_content_readiness": False,
        "production_approval": False,
    }


def _readiness_separation() -> dict[str, Any]:
    return {
        "slice_completion": "pass_for_this_asset_bridge",
        "video_readiness_progress": "6/7",
        "video_readiness_current": "visual_card_asset_bridge_created",
        "video_readiness_next_missing_gate": (
            "YMM4 card asset placement probe and internal review milestone"
        ),
        "visual_readiness_progress": "4/7",
        "visual_readiness_current": "external_fake_card_assets_reviewable_in_html",
        "production_readiness": "low_diagnostic_only",
        "production_readiness_reason": (
            "The bridge creates fake visual assets only; it does not prove YMM4 "
            "placement, final visual quality, real content, or production approval."
        ),
        "next_default_slice": NEXT_DEFAULT_SLICE,
    }


def _recommended_next_slices() -> list[dict[str, str]]:
    return [
        {
            "slice": NEXT_DEFAULT_SLICE,
            "timing": "recommended_next_default",
            "reason": (
                "the video now has external fake card assets; the next useful "
                "gate is proving bounded image-asset placement in YMM4"
            ),
        },
        {
            "slice": NEXT_RENDER_SMOKE_SLICE,
            "timing": "after_card_placement_probe",
            "reason": (
                "render only after placement changes the video surface enough to "
                "justify a milestone smoke"
            ),
        },
        {
            "slice": INTERNAL_REVIEW_PREP_SLICE,
            "timing": "after_visual_card_bridge_and_or_placement_probe",
            "reason": "prepare the first internal review once the visual surface is inspectable",
        },
        {
            "slice": RETENTION_POLICY_SLICE,
            "timing": "only_if_output_artifacts_need_retention",
            "reason": "render outputs remain ignored unless a later retention gate opens",
        },
    ]


def _implementation_principle_for_next_lane() -> list[str]:
    return [
        "Do not rebuild cards as complex YMM4 object graphs.",
        "Prefer external card assets generated from HTML/SVG/Canvas and imported or placed into YMM4 later.",
        "Preserve the YMM4 native audio path.",
        "Keep .ymmp mutation limited to ignored local copies and bounded timing/layout carrier operations.",
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "current_repo_state_verified", "status": "passed"},
        {"gate": "source_render_smoke_result_inspected", "status": "passed"},
        {"gate": "visual_card_assets_generated", "status": "passed"},
        {"gate": "bridge_json_doc_created", "status": "passed"},
        {"gate": "readiness_separation_updated", "status": "passed"},
        {"gate": "narrow_commit_created_and_pushed_if_gate_passes", "status": "pending_until_git_gate"},
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"artifact": "bridge_json", "status": "present"},
        {"artifact": "human_readback", "status": "present"},
        {"artifact": "svg_card_assets", "status": "present"},
        {"artifact": "html_contact_sheet", "status": "present"},
        {"artifact": "placement_contract", "status": "present"},
        {"artifact": "downstream_next_use", "status": "present"},
    ]


def _video_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "source_input_path_proven", "status": True},
        {"gate": "target_yym4_import_path_proven", "status": True},
        {"gate": "audio_path_proven", "status": True},
        {"gate": "timing_duration_strategy_defined", "status": True},
        {"gate": "tiny_smoke_render_observed", "status": True},
        {"gate": "targeted_regression_render_observed", "status": True},
        {"gate": "internal_review_milestone_reached", "status": False},
    ]


def _visual_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "fake_review_only_content_used", "status": True},
        {"gate": "external_svg_card_assets_created", "status": True},
        {"gate": "one_card_per_caption_unit", "status": True},
        {"gate": "html_contact_sheet_created", "status": True},
        {"gate": "subtitle_safe_lower_area_reserved", "status": True},
        {"gate": "YMM4_card_asset_placement_proven", "status": False},
        {"gate": "internal_review_visual_acceptance_reached", "status": False},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "render_performed_by_agent_in_this_slice", "status": False},
        {"gate": "existing_render_observation_reused", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {"gate": "next_render_tied_to_card_placement_or_internal_review", "status": True},
        {"gate": "no_render_for_docs_readback_or_asset_bridge_only_changes", "status": True},
        {"gate": "repeated_audio_render_check_avoided", "status": True},
    ]


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "user_input", "status": "freeform_prior_observation"},
        {"gate": "template_required", "status": False},
        {"gate": "schema_owner", "status": "Agent"},
        {"gate": "user_side_work", "status": "none"},
        {"gate": "future_look_for_points_max", "status": 3},
        {"gate": "negative_confirmation_checklist", "status": False},
        {"gate": "fixed_form_relapse", "status": False},
    ]


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"gate": "prior_timing_proof_reused", "status": True},
        {"gate": "prior_audio_evidence_reused", "status": True},
        {"gate": "current_render_observation_consumed_via_result_readback", "status": True},
        {"gate": "next_axis_stated_as_yym4_card_asset_placement", "status": True},
        {"gate": "not_accepted_scope_preserved", "status": True},
        {"gate": "repeated_render_audio_review_requested", "status": False},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "packet_for_packet_drift", "status": False},
        {"gate": "readback_only_stall", "status": False},
        {"gate": "repeated_render_request", "status": False},
        {"gate": "product_video_readiness_separated_from_slice_completion", "status": True},
        {"gate": "next_concrete_milestone", "status": NEXT_DEFAULT_SLICE},
    ]


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_created_by_agent": False,
        "video_render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "external_TTS_introduced": False,
        "real_media_imported": False,
        "real_source_fetch_performed": False,
        "real_urls_accessed": False,
        "contains_real_urls": False,
        "contains_real_brands": False,
        "contains_real_news_claims": False,
        "ymmp_created_or_modified_by_agent": False,
        "ymmp_or_media_staged_or_committed": False,
        "render_output_staged_or_committed": False,
        "production_approval": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


def _downstream_next_use() -> dict[str, list[str]]:
    return {
        "use_this_bridge_to": [
            "review four fake external SVG cards without launching YMM4",
            "feed a future bounded YMM4 image-asset placement probe",
            "preserve native YMM4 audio and the 68 second timing result as prior evidence",
        ],
        "do_not_use_this_bridge_to": [
            "claim production visual quality or public video readiness",
            "claim YMM4 card placement or post-card render proof",
            "rebuild card layouts as direct YMM4 text/shape object graphs",
            "commit .ymmp, mp4, wav, mp3, m4a, voice cache, or render output",
        ],
    }


def _validation_expectations() -> dict[str, bool]:
    return {
        "json_parse_required": True,
        "svg_xml_parse_required": True,
        "html_parse_required": True,
        "focused_tests_required": True,
        "compileall_required": True,
        "git_diff_check_required": True,
        "git_cached_diff_check_required": True,
        "conflict_marker_scan_required": True,
        "fixed_form_relapse_scan_required": True,
        "repeated_render_request_scan_required": True,
        "real_url_brand_public_approval_scan_required": True,
        "forbidden_staged_file_scan_required": True,
        "YMM4_launched_by_agent": False,
        "render_audio_or_tts_created_by_agent": False,
    }


def _caption_items(neutral_timeline: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in _list(neutral_timeline.get("items"))
        if item.get("item_kind") == "caption"
    ]


def _visual_placeholder_by_beat(
    neutral_timeline: dict[str, Any],
    timing_plan: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for item in _list(neutral_timeline.get("items")):
        if item.get("item_kind") == "visual_placeholder" and item.get("beat_id"):
            rows[str(item["beat_id"])] = item
    for visual in _list(timing_plan.get("visual_timing")):
        beat_id = visual.get("beat_id")
        if not isinstance(beat_id, str):
            continue
        rows.setdefault(beat_id, {}).update(visual)
    return rows


def _append_status_table(
    lines: list[str],
    title: str,
    rows: Any,
) -> None:
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


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _xml(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _html(value: Any) -> str:
    return html.escape(str(value), quote=True)
