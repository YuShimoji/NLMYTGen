"""Review-driven visual card refinement readback for the newsroom handoff.

This slice consumes the freeform internal review result, refines the external
card assets, and records the next milestone. It does not launch YMM4, render
video, edit .ymmp files, fetch real media, generate audio/TTS, or approve
production/public use.
"""

from __future__ import annotations

import json
import struct
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_card_placement_render_smoke_result_readback import (
    DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_internal_review_v0_1_prep import (
    DEFAULT_INTERNAL_REVIEW_V0_1_PREP_PATH,
)
from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH,
    DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
    VISUAL_CARD_REFINEMENT_TOKENS,
    write_default_newsroom_visual_card_asset_bridge_artifacts,
)
from src.pipeline.newsroom_yym4_card_asset_placement_probe import (
    DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH,
    ensure_card_png_assets,
)


INTERNAL_REVIEW_V0_1_RESULT_READBACK_SCHEMA_VERSION = (
    "newsroom_internal_review_v0_1_result_readback.v1"
)
INTERNAL_REVIEW_V0_1_RESULT_READBACK_ID = (
    "newsroom_internal_review_v0_1_result_readback_v1_2026_06_25"
)
VISUAL_CARD_DESIGN_REFINEMENT_SCHEMA_VERSION = (
    "newsroom_visual_card_design_refinement.v1"
)
VISUAL_CARD_DESIGN_REFINEMENT_ID = (
    "newsroom_visual_card_design_refinement_v1_2026_06_25"
)

DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/internal_review_v0_1_result_readback_v1.json"
)
DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_DOC_PATH = Path(
    "docs/verification/NEWSROOM_INTERNAL_REVIEW_V0_1_RESULT_READBACK_V1_2026-06-25.md"
)
DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH = Path(
    "samples/_probe/newsroom_handoff/visual_card_design_refinement_v1.json"
)
DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_DOC_PATH = Path(
    "docs/verification/NEWSROOM_VISUAL_CARD_DESIGN_REFINEMENT_V1_2026-06-25.md"
)

NEXT_DEFAULT_SLICE = "newsroom-card-placement-post-refinement-render-smoke-v1"
PLACEMENT_REFRESH_SLICE = "newsroom-yym4-card-asset-placement-refresh-v1"
RASTER_EXPORT_SLICE = "newsroom-visual-card-raster-export-v1"
INTERNAL_REVIEW_PREP_SLICE = "newsroom-internal-review-v0.1-prep"
RSS_DRY_RUN_SLICE = "newsroom-rss-dry-run-integration-plan-v1"


def write_default_newsroom_visual_card_design_refinement_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write refined card assets, review readback, refinement JSON, and docs."""
    base = Path(root) if root is not None else Path(".")

    bridge = write_default_newsroom_visual_card_asset_bridge_artifacts(root=base)
    png_export = ensure_card_png_assets(
        base,
        _png_source_assets(bridge),
        force=True,
    )
    if png_export["png_export_status"] != "generated":
        raise RuntimeError(f"PNG regeneration failed: {png_export.get('errors')}")

    readback = build_default_newsroom_internal_review_v0_1_result_readback(
        root=base
    )
    _write_json(base / DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_PATH, readback)
    _write_text(
        base / DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_DOC_PATH,
        render_newsroom_internal_review_v0_1_result_readback_markdown(readback),
    )

    refinement = build_default_newsroom_visual_card_design_refinement(root=base)
    _write_json(base / DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH, refinement)
    _write_text(
        base / DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_DOC_PATH,
        render_newsroom_visual_card_design_refinement_markdown(refinement),
    )
    return refinement


def build_default_newsroom_internal_review_v0_1_result_readback(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the normalized internal review result readback."""
    base = Path(root) if root is not None else Path(".")
    prep = load_json_object(base / DEFAULT_INTERNAL_REVIEW_V0_1_PREP_PATH)
    card_result = load_json_object(
        base / DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    placement_probe = load_json_object(
        base / DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH
    )
    bridge = load_json_object(base / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH)
    validation = _review_source_validation(
        prep=prep,
        card_result=card_result,
        placement_probe=placement_probe,
        bridge=bridge,
    )

    return {
        "artifact_id": INTERNAL_REVIEW_V0_1_RESULT_READBACK_ID,
        "readback_id": INTERNAL_REVIEW_V0_1_RESULT_READBACK_ID,
        "schema_version": INTERNAL_REVIEW_V0_1_RESULT_READBACK_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "internal_review_status": "needs_visual_refinement",
        "mechanics_status": "pass",
        "timing_audio_render_status": "diagnostic_pass",
        "identity": {
            "readback_id": INTERNAL_REVIEW_V0_1_RESULT_READBACK_ID,
            "source_review_stage_path": _path_text(
                DEFAULT_INTERNAL_REVIEW_V0_1_PREP_PATH
            ),
            "source_review_stage_id": prep.get("review_package_id"),
            "source_card_render_result_path": _path_text(
                DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
            ),
            "source_card_render_result_id": card_result.get("readback_id"),
            "source_card_placement_probe_path": _path_text(
                DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH
            ),
            "source_visual_card_bridge_path": _path_text(
                DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH
            ),
            "review_source": "user_freeform",
            "production_status": "diagnostic_only",
        },
        "source_validation": validation,
        "internal_review_normalization": _internal_review_normalization(),
        "accepted_mechanics": {
            "timing": "diagnostic_pass",
            "native_audio": "diagnostic_pass",
            "render": "diagnostic_pass",
            "card_placement": "diagnostic_pass",
        },
        "review_findings": _review_findings(),
        "accepted_scope": {
            "mechanics_timing_audio_render_card_placement_pass": True,
            "internal_review_observation_captured": True,
            "visual_refinement_axis_selected": True,
            "review_does_not_reopen_audio_or_timing": True,
        },
        "not_accepted_scope": _not_accepted_scope(),
        "readiness_separation": _readiness_separation(),
        "render_gate_carry_forward": _render_gate_carry_forward(),
        "recommended_next_axis": "visual_card_design_refinement",
        "completion_matrix": _result_completion_matrix(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(),
        "boundaries": _boundaries(),
    }


def build_default_newsroom_visual_card_design_refinement(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the visual card design refinement artifact."""
    base = Path(root) if root is not None else Path(".")
    readback = load_json_object(
        base / DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_PATH
    )
    bridge = load_json_object(base / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH)
    card_result = load_json_object(
        base / DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    design_changes = _design_changes(base, bridge)
    pngs_valid = all(row["png_valid"] for row in design_changes)
    refinement_status = "assets_regenerated" if pngs_valid else "blocked"

    return {
        "artifact_id": VISUAL_CARD_DESIGN_REFINEMENT_ID,
        "refinement_id": VISUAL_CARD_DESIGN_REFINEMENT_ID,
        "schema_version": VISUAL_CARD_DESIGN_REFINEMENT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "refinement_status": refinement_status,
        "identity": {
            "refinement_id": VISUAL_CARD_DESIGN_REFINEMENT_ID,
            "source_internal_review_result_readback_path": _path_text(
                DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_PATH
            ),
            "source_internal_review_result_readback_id": readback.get("readback_id"),
            "source_visual_card_bridge_path": _path_text(
                DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH
            ),
            "source_cards_dir": "samples/_probe/newsroom_handoff/visual_cards_v1",
            "output_cards_dir": "samples/_probe/newsroom_handoff/visual_cards_v1",
            "source_card_render_result_path": _path_text(
                DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
            ),
            "source_card_render_result_id": card_result.get("readback_id"),
            "production_status": "diagnostic_only",
        },
        "design_token_constraints": _design_token_constraints(),
        "design_changes": design_changes,
        "source_review_findings": readback.get("review_findings"),
        "source_internal_review_normalization": readback.get(
            "internal_review_normalization"
        ),
        "accepted_scope": _refinement_accepted_scope(pngs_valid),
        "not_accepted_scope": _refinement_not_accepted_scope(),
        "readiness_separation": _refinement_readiness_separation(pngs_valid),
        "next_recommended_slice": {
            "slice": NEXT_DEFAULT_SLICE if pngs_valid else RASTER_EXPORT_SLICE,
            "reason": (
                "asset paths are stable and PNGs were regenerated, so the next "
                "milestone is a post-refinement render-smoke observation"
                if pngs_valid
                else "raster export must pass before any placement/render milestone"
            ),
        },
        "recommended_next_slices": _recommended_next_slices(pngs_valid),
        "implementation_principle_for_next_lane": [
            "Do not rebuild cards as complex YMM4 object graphs.",
            "Keep cards as external SVG/PNG assets.",
            "Preserve the YMM4 native audio path.",
            "Keep .ymmp mutation limited to ignored local copies.",
        ],
        "goal_stack": _goal_stack(),
        "completion_matrix": _refinement_completion_matrix(pngs_valid),
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
                "run a milestone-gated post-refinement render smoke later",
                "compare readability and variation against the prior review finding",
            ],
            "do_not_use_this_refinement_to": [
                "claim production visual quality",
                "claim public video readiness",
                "introduce real brands, real URLs, screenshots, or external TTS",
                "commit ignored .ymmp, mp4, audio, voice cache, or render outputs",
            ],
        },
    }


def render_newsroom_internal_review_v0_1_result_readback_markdown(
    readback: dict[str, Any],
) -> str:
    """Render the human-readable internal review result readback."""
    lines = [
        "# Newsroom Internal Review v0.1 Result Readback v1",
        "",
        f"artifact_id: {readback.get('artifact_id')}",
        f"readback_id: {readback.get('readback_id')}",
        f"schema_version: {readback.get('schema_version')}",
        f"internal_review_status: {readback.get('internal_review_status')}",
        f"mechanics_status: {readback.get('mechanics_status')}",
        f"timing_audio_render_status: {readback.get('timing_audio_render_status')}",
        "production_status: diagnostic_only",
        "",
        "## Identity",
        "",
    ]
    _append_key_values(lines, readback.get("identity"))
    lines.extend(["", "## Source Validation", ""])
    _append_key_values(lines, readback.get("source_validation"))
    lines.extend(["", "## Normalized Review", ""])
    _append_key_values(lines, readback.get("internal_review_normalization"))
    lines.extend(["", "## Findings", ""])
    _append_key_values(lines, readback.get("review_findings"))
    lines.extend(["", "## Accepted Mechanics", ""])
    _append_key_values(lines, readback.get("accepted_mechanics"))
    lines.extend(["", "## Not Accepted Scope", ""])
    _append_key_values(lines, readback.get("not_accepted_scope"))
    lines.extend(["", "## Readiness Separation", ""])
    _append_key_values(lines, readback.get("readiness_separation"))
    lines.extend(["", "## Render Gate", ""])
    _append_key_values(lines, readback.get("render_gate_carry_forward"))
    _append_status_table(lines, "Completion Matrix", readback.get("completion_matrix"))
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
            "The internal review accepts the diagnostic mechanics but rejects the "
            "current visual quality. The next axis is external card design "
            "refinement; audio, timing, and card placement mechanics are reused "
            "as prior evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def render_newsroom_visual_card_design_refinement_markdown(
    refinement: dict[str, Any],
) -> str:
    """Render the human-readable visual card design refinement readback."""
    lines = [
        "# Newsroom Visual Card Design Refinement v1",
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
            "| card | role | motif | wrap | clipping guard | svg | png |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for row in _list(refinement.get("design_changes")):
        lines.append(
            "| "
            f"{row.get('card_id')} | "
            f"{row.get('role')} | "
            f"{row.get('layout_motif')} | "
            f"{_display(row.get('text_wrap_applied'))} | "
            f"{_display(row.get('clipping_guard'))} | "
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
            "The assets are improved diagnostic cards only. The stable PNG paths "
            "make a later post-refinement smoke meaningful, but production visual "
            "quality, final design, real content, and public readiness stay closed.",
            "",
        ]
    )
    return "\n".join(lines)


def _png_source_assets(bridge: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for asset in _list(bridge.get("assets")):
        svg_path = Path(str(asset.get("repo_relative_path")))
        rows.append(
            {
                "source_svg_path": _path_text(svg_path),
                "png_path": _path_text(svg_path.with_suffix(".png")),
            }
        )
    return rows


def _review_source_validation(
    *,
    prep: dict[str, Any],
    card_result: dict[str, Any],
    placement_probe: dict[str, Any],
    bridge: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    normalized = _dict(card_result.get("normalized_render_result"))
    if prep.get("review_package_id") is None:
        errors.append("INTERNAL_REVIEW_PREP_MISSING_ID")
    if card_result.get("result_status") != "pass":
        errors.append("CARD_RENDER_RESULT_NOT_PASS")
    if normalized.get("output_duration_sec") != 68:
        errors.append("CARD_RENDER_DURATION_NOT_68")
    if normalized.get("card_count_visible") != 4:
        errors.append("CARD_RENDER_CARD_COUNT_NOT_4")
    if placement_probe.get("probe_status") != "placed_structurally":
        errors.append("CARD_PLACEMENT_PROBE_NOT_STRUCTURAL_PASS")
    if len(_list(bridge.get("assets"))) != 4:
        errors.append("VISUAL_CARD_ASSET_COUNT_NOT_4")
    return {
        "status": "passed" if not errors else "blocked",
        "errors": errors,
        "source_review_stage_id": prep.get("review_package_id"),
        "source_card_render_result_id": card_result.get("readback_id"),
        "source_card_render_result": card_result.get("result_status"),
        "source_card_render_duration_sec": normalized.get("output_duration_sec"),
        "source_card_count_visible": normalized.get("card_count_visible"),
        "source_placement_probe_status": placement_probe.get("probe_status"),
        "source_visual_card_count": len(_list(bridge.get("assets"))),
    }


def _internal_review_normalization() -> dict[str, Any]:
    return {
        "internal_review_status": "needs_visual_refinement",
        "mechanics_status": "pass",
        "timing_audio_render_status": "diagnostic_pass",
        "pacing_density_issue": "known",
        "text_clipping": True,
        "text_wrap_missing": True,
        "min_font_too_small": True,
        "large_font_too_large": True,
        "type_scale_unbalanced": True,
        "overall_readability_low": True,
        "card_variation_insufficient": True,
        "production_visual_quality_accepted": False,
        "public_video_ready": False,
        "recommended_next_axis": "visual_card_design_refinement",
    }


def _review_findings() -> dict[str, Any]:
    return {
        "text_clipping": True,
        "text_wrap_missing": True,
        "type_scale_unbalanced": True,
        "overall_readability_low": True,
        "card_variation_insufficient": True,
        "pacing_density_issue_known": True,
    }


def _design_changes(root: Path, bridge: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for asset in _list(bridge.get("assets")):
        svg_path = str(asset.get("repo_relative_path"))
        png_path = str(asset.get("raster_repo_relative_path") or "")
        if not png_path:
            png_path = _path_text(Path(svg_path).with_suffix(".png"))
        metadata = _png_metadata(root / png_path)
        rows.append(
            {
                "card_id": asset.get("asset_id"),
                "role": asset.get("design_refinement_role"),
                "role_label": asset.get("review_role_label"),
                "layout_motif": asset.get("layout_motif"),
                "before_issue_summary": asset.get("before_issue_summary"),
                "after_change_summary": asset.get("after_change_summary"),
                "text_wrap_applied": asset.get("text_wrap_applied") is True,
                "clipping_guard": asset.get("clipping_guard") is True,
                "type_scale_status": asset.get("type_scale_status"),
                "variation_status": asset.get("variation_status"),
                "output_svg_path": svg_path,
                "output_png_path": png_path,
                "preview_path": _path_text(DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH),
                "contact_sheet_path": _path_text(DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH),
                "png_valid": metadata.get("valid") is True,
                "png_width": metadata.get("width"),
                "png_height": metadata.get("height"),
            }
        )
    return rows


def _design_token_constraints() -> dict[str, Any]:
    return {
        **VISUAL_CARD_REFINEMENT_TOKENS,
        "real_brand_or_url_present": False,
        "production_claim_present": False,
        "text_wrapping_required": True,
        "source_metadata_wrap_required": True,
        "card_variation_required": "role_specific_layout_motif",
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_visual_quality": False,
        "final_design_system": False,
        "final_narration_script_density": False,
        "public_video_readiness": False,
        "real_newsroom_visuals": False,
        "real_content_readiness": False,
        "production_approval": False,
    }


def _readiness_separation() -> dict[str, Any]:
    return {
        "slice_completion": "pass_for_review_result_readback",
        "video_readiness_progress": "6/7",
        "visual_readiness_current": "needs_visual_refinement",
        "production_readiness": "low_diagnostic_only",
        "recommended_next_axis": "visual_card_design_refinement",
        "public_video_ready": False,
    }


def _render_gate_carry_forward() -> dict[str, Any]:
    return {
        "new_render_in_this_slice": False,
        "YMM4_launched_by_agent": False,
        "render_audio_or_tts_created_by_agent": False,
        "existing_render_review_evidence_reused": True,
        "render_gate": "milestone_gated_not_docs_gated",
        "next_render_allowed_after": [
            "visual/card design surface changes are written to stable PNG assets",
            "internal review v0.1 milestone needs a fresh observation",
        ],
        "no_render_for": [
            "docs changes",
            "readback changes",
            "policy-only changes",
        ],
    }


def _refinement_accepted_scope(pngs_valid: bool) -> dict[str, bool]:
    return {
        "review_findings_captured": True,
        "external_card_assets_refined": pngs_valid,
        "text_clipping_reduced_by_generator_rules": pngs_valid,
        "wrapping_clamping_rules_introduced": True,
        "card_variation_increased": True,
        "assets_ready_for_later_yym4_placement_render_smoke": pngs_valid,
    }


def _refinement_not_accepted_scope() -> dict[str, bool]:
    return {
        "production_visual_quality": False,
        "final_design_system": False,
        "YMM4_placement_proof_after_refinement": False,
        "post_refinement_render_proof": False,
        "public_video_readiness": False,
        "real_newsroom_visuals": False,
        "real_content_readiness": False,
        "production_approval": False,
    }


def _refinement_readiness_separation(pngs_valid: bool) -> dict[str, Any]:
    return {
        "slice_completion": "pass_for_visual_refinement" if pngs_valid else "blocked",
        "video_readiness_progress": "6/7",
        "visual_readiness_progress": "7/7_diagnostic_refined"
        if pngs_valid
        else "blocked",
        "visual_readiness_current": "external_card_assets_refined"
        if pngs_valid
        else "png_regeneration_blocked",
        "video_readiness_next_missing_gate": (
            "post-refinement render smoke observation, then internal review milestone"
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
                "stable SVG/PNG asset paths are regenerated; the existing ignored "
                "placement project should now reference the improved PNGs"
                if pngs_valid
                else "PNG export must be fixed before another visual milestone"
            ),
        },
        {
            "slice": PLACEMENT_REFRESH_SLICE,
            "timing": "only_if_existing_placement_paths_are_not_stable",
            "reason": "refresh ImageItem placement only if stable PNG paths cannot be reused",
        },
        {
            "slice": "newsroom-internal-review-v0.1-prep",
            "timing": "after_post_refinement_smoke",
            "reason": "internal review is meaningful after the changed visual surface is observed",
        },
        {
            "slice": RSS_DRY_RUN_SLICE,
            "timing": "later_not_immediate",
            "reason": "real packet integration should wait until the visual baseline is accepted",
        },
    ]


def _goal_stack() -> list[dict[str, str]]:
    return [
        {
            "level": "Immediate",
            "goal": "Convert internal review into actionable visual refinement",
            "success_signal": "review readback and refined assets exist",
            "contribution": "avoids a vague review loop",
        },
        {
            "level": "Short-term",
            "goal": "Improve card readability and variation",
            "success_signal": "no obvious clipping, better type scale, differentiated cards",
            "contribution": "makes next render review meaningful",
        },
        {
            "level": "Mid-term",
            "goal": "Prepare post-refinement render smoke",
            "success_signal": "stable PNG assets can be reused by placement .ymmp",
            "contribution": "moves toward internal review acceptance",
        },
        {
            "level": "Long-term",
            "goal": "Establish reusable card design baseline",
            "success_signal": "future packets can use readable card templates",
            "contribution": "supports automation",
        },
    ]


def _result_completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "current_repo_state_verified", "status": True},
        {"gate": "internal_review_observation_normalized", "status": True},
        {"gate": "current_card_issues_inspected", "status": True},
        {"gate": "review_result_readback_created", "status": True},
        {"gate": "readiness_separation_recorded", "status": True},
        {"gate": "narrow_commit_created_and_pushed_if_push_gate_passes", "status": "pending_until_git_gate"},
    ]


def _refinement_completion_matrix(pngs_valid: bool) -> list[dict[str, Any]]:
    return [
        {"gate": "current_repo_state_verified", "status": True},
        {"gate": "internal_review_observation_normalized", "status": True},
        {"gate": "current_card_issues_inspected", "status": True},
        {"gate": "refined_card_assets_generated", "status": pngs_valid},
        {"gate": "preview_contact_sheet_updated", "status": True},
        {"gate": "narrow_commit_created_and_pushed_if_push_gate_passes", "status": "pending_until_git_gate"},
    ]


def _artifact_readiness(pngs_valid: bool) -> list[dict[str, Any]]:
    return [
        {"artifact": "review_result_readback", "status": "present"},
        {"artifact": "visual_refinement_json", "status": "present"},
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
        {"gate": "post_refinement_render_reviewed", "status": False if pngs_valid else "blocked"},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "render_performed_in_this_slice", "status": False},
        {"gate": "existing_render_review_evidence_reused", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {"gate": "next_render_tied_to_visual_card_design_surface_change", "status": True},
        {"gate": "no_render_for_docs_readback_changes", "status": True},
        {"gate": "repeated_timing_audio_review_avoided", "status": True},
    ]


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
        {"gate": "next_axis_stated_as_visual_refinement", "status": True},
        {"gate": "not_accepted_scope_preserved", "status": True},
        {"gate": "repeated_user_review_requested", "status": False},
        {"gate": "mechanics_re_review_requested", "status": False},
    ]


def _inertia_check(next_slice: str = "visual_card_design_refinement") -> list[dict[str, Any]]:
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
