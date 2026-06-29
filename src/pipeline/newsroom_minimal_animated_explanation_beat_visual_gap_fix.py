"""Record the v1 visual integration gap and build a v2 visible-text probe.

The previous mainline proof correctly froze the animation accent, but the local
YMM4 scene materialized only character animation. This slice records that
actual-vs-claim gap and adds one plain TextItem to a v2 ignored local probe.
It does not tune animation, render, launch YMM4, generate audio/TTS, fetch real
news, or redesign cards.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_minimal_animated_explanation_beat import (
    DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_PATH,
    DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH,
    LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH,
    materialize_local_minimal_animated_explanation_beat_probe,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
    _dict,
    _first_timeline,
    _get_timeline_items,
    _item_type,
    _not_accepted_scope,
)
from src.pipeline.newsroom_yukkuri_animation_tempo_contract import (
    _git_check_ignore,
    _local_probe_access,
    _sha256,
    _write_json,
    _write_text,
)
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


PREVIEW_GAP_ID = "newsroom_minimal_animated_explanation_beat_preview_gap_v1_2026_06_29"
VISUAL_GAP_FIX_ID = (
    "newsroom_minimal_animated_explanation_beat_visual_integration_gap_fix_v1_2026_06_29"
)
PREVIEW_GAP_SCHEMA_VERSION = (
    "newsroom_minimal_animated_explanation_beat_preview_gap.v1"
)
VISUAL_GAP_FIX_SCHEMA_VERSION = (
    "newsroom_minimal_animated_explanation_beat_visual_integration_gap_fix.v1"
)

DEFAULT_PREVIEW_GAP_PATH = Path(
    "samples/_probe/newsroom_handoff/minimal_animated_explanation_beat_preview_gap_v1.json"
)
DEFAULT_PREVIEW_GAP_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_PREVIEW_GAP_V1_2026-06-29.md"
)
DEFAULT_VISUAL_GAP_FIX_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "minimal_animated_explanation_beat_visual_integration_gap_fix_v1.json"
)
DEFAULT_VISUAL_GAP_FIX_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_VISUAL_INTEGRATION_GAP_FIX_V1_2026-06-29.md"
)

LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH = Path(
    "_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v2_visible_integration.ymmp"
)

NEXT_AXIS_V2_PREVIEW_OPERATOR_INSTRUCTION = (
    "newsroom-minimal-animated-explanation-beat-v2-preview-operator-instruction-v1"
)
NEXT_AXIS_TEXTITEM_ROUTE_AUDIT = "newsroom-yymp-textitem-overlay-route-audit-v1"
NEXT_AXIS_MINIMAL_OVERLAY_VISIBILITY_FIX = "newsroom-minimal-overlay-visibility-fix-v1"
NEXT_AXIS_CLOSE_AND_RSS_RETURN = (
    "newsroom-animation-accent-policy-closed-return-to-rss-dry-run-v1"
)

VISIBLE_DIAGNOSTIC_TEXT = (
    "説明beat: 台本・字幕・最小アニメを同じ場面で確認"
)
VISIBLE_TEXT_REMARK = "minimal_animated_explanation_beat_v2_visible_text_overlay"

NORMALIZED_USER_OBSERVATION: dict[str, Any] = {
    "source_observation_role": "user_opened_minimal_animated_explanation_beat_v1_probe",
    "source_probe_path": LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH.as_posix(),
    "yym4_opened": True,
    "minimal_integrated_scene_preview_observed": True,
    "character_animation_visible": True,
    "nod_visible": True,
    "card_or_overlay_visible": False,
    "subtitle_or_explanation_text_visible": "unknown_or_absent",
    "integrated_explanation_beat_status": "fail_or_unproven",
    "animation_accent_status": "pass",
    "mainline_integration_gap": True,
    "next_axis": "visual_integration_gap_audit_and_v2_materialization",
}


def write_default_newsroom_minimal_animated_explanation_beat_visual_gap_fix_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    materialize_local_v2_visible_integration_probe(root=base)
    preview_gap = build_default_preview_gap(root=base)
    visual_fix = build_default_visual_gap_fix(root=base)
    _write_json(base / DEFAULT_PREVIEW_GAP_PATH, preview_gap)
    _write_text(
        base / DEFAULT_PREVIEW_GAP_DOC_PATH,
        render_preview_gap_markdown(preview_gap),
    )
    _write_json(base / DEFAULT_VISUAL_GAP_FIX_PATH, visual_fix)
    _write_text(
        base / DEFAULT_VISUAL_GAP_FIX_DOC_PATH,
        render_visual_gap_fix_markdown(visual_fix),
    )
    return {
        "preview_gap": preview_gap,
        "visual_gap_fix": visual_fix,
    }


def build_default_preview_gap(*, root: str | Path | None = None) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    v1_readback = _probe_structure_readback(
        base,
        LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH,
    )
    contract_claim = _previous_contract_claim(base)
    return {
        "artifact_id": PREVIEW_GAP_ID,
        "gap_id": PREVIEW_GAP_ID,
        "schema_version": PREVIEW_GAP_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_context": _source_context(base),
        "source_v1_probe_path": LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH.as_posix(),
        "user_observation": NORMALIZED_USER_OBSERVATION,
        "actual_v1_readback": v1_readback,
        "contract_claim_from_previous_slice": contract_claim,
        "actual_YMM4_visible_gap": {
            "status": "confirmed_gap",
            "card_or_overlay_visible": False,
            "visible_TextItem_subtitle_card_or_overlay_exists": False,
            "animation_accent_visible": True,
            "integrated_explanation_beat_status": "fail_or_unproven",
            "reason": "v1 .ymmp contains GroupItem/ImageItem animation only and no TextItem or ShapeItem overlay item",
        },
        "root_cause_classification": _root_cause(v1_readback, contract_claim),
        "v2_correction_plan": _v2_correction_plan(),
        "v2_materialization_status": _v2_materialization_status(base),
        "business_goal_outcome_contract": _business_goal_outcome_contract(
            v2_materialized=_v2_materialized(base)
        ),
        "not_accepted_scope": _not_accepted_scope_with_gap_boundaries(),
        "boundaries": _boundaries(local_v2_created=_v2_materialized(base)),
    }


def build_default_visual_gap_fix(*, root: str | Path | None = None) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    v1_readback = _probe_structure_readback(
        base,
        LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH,
    )
    v2_access = _local_probe_access(
        base,
        LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH,
        "local_ignored_minimal_animated_explanation_beat_v2_visible_integration_probe",
    )
    v2_readback = _probe_structure_readback(base, LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH)
    v2_materialized = (
        v2_access["target_exists"]
        and v2_access["access_state"] == "verified_present"
        and v2_readback["readback_status"] == "structural_pass"
        and v2_readback["visible_text_or_overlay_item_count"] >= 1
    )
    next_axis = (
        NEXT_AXIS_V2_PREVIEW_OPERATOR_INSTRUCTION
        if v2_materialized
        else NEXT_AXIS_TEXTITEM_ROUTE_AUDIT
    )
    return {
        "artifact_id": VISUAL_GAP_FIX_ID,
        "fix_id": VISUAL_GAP_FIX_ID,
        "schema_version": VISUAL_GAP_FIX_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_context": _source_context(base),
        "source_v1_probe_path": LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH.as_posix(),
        "user_observation": NORMALIZED_USER_OBSERVATION,
        "actual_v1_readback": v1_readback,
        "root_cause_classification": _root_cause(v1_readback, _previous_contract_claim(base)),
        "v2_correction_plan": _v2_correction_plan(),
        "v2_visible_integration_probe": {
            "artifact_id": "local_ignored_minimal_animated_explanation_beat_v2_visible_integration_probe",
            "repo_relative_path": LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH.as_posix(),
            "folder_full_path_current_host": v2_access.get("folder_full_path_current_host"),
            "file_full_path_current_host": v2_access.get("file_full_path_current_host"),
            "launcher_or_open_command": v2_access.get("launcher_or_open_command"),
            "target_exists": v2_access.get("target_exists"),
            "access_state": v2_access.get("access_state"),
            "access_evidence_level": v2_access.get("access_evidence_level"),
            "artifact_scope": v2_access.get("artifact_scope"),
            "evidence_source": v2_access.get("evidence_source"),
            "git_check_ignore_result": v2_access.get("git_check_ignore_result"),
            "size": v2_access.get("size"),
            "visible_text_or_overlay_item_count": v2_readback.get(
                "visible_text_or_overlay_item_count", 0
            ),
            "animation_item_count": v2_readback.get("animation_item_count", 0),
            "materialization_status": (
                "materialized_ignored_local_probe" if v2_materialized else "blocked"
            ),
        },
        "v2_readback": v2_readback,
        "business_goal_outcome_contract": _business_goal_outcome_contract(
            v2_materialized=v2_materialized
        ),
        "selected_next_axis": next_axis,
        "next_recommended_axis": {
            "selected": next_axis,
            "reason": _next_axis_reason(v2_materialized, v2_readback),
            "if_v1_already_had_visible_items": NEXT_AXIS_MINIMAL_OVERLAY_VISIBILITY_FIX,
            "if_materialization_not_worth_more_work": NEXT_AXIS_CLOSE_AND_RSS_RETURN,
        },
        "not_accepted_scope": _not_accepted_scope_with_gap_boundaries(),
        "boundaries": _boundaries(local_v2_created=v2_materialized),
        "inertia_check": _inertia_check(next_axis),
    }


def materialize_local_v2_visible_integration_probe(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    v1_path = base / LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH
    if not v1_path.exists():
        materialize_local_minimal_animated_explanation_beat_probe(root=base)
    v1_readback = _probe_structure_readback(
        base,
        LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH,
    )
    if v1_readback.get("readback_status") != "structural_pass":
        raise ValueError("source v1 probe is not structurally readable")

    target = base / LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    probe = copy.deepcopy(load_ymmp(v1_path))
    probe["FilePath"] = str(target.resolve())
    timeline = _first_timeline(probe)
    if not timeline:
        raise ValueError("v1 probe has no timeline")
    items = _get_timeline_items(probe)
    items[:] = [
        item
        for item in items
        if not (
            isinstance(item, dict)
            and item.get("Remark") == VISIBLE_TEXT_REMARK
        )
    ]
    items.append(_make_visible_text_item())
    timeline["Items"] = sorted(
        items,
        key=lambda item: (int(item.get("Frame", 0)), int(item.get("Layer", 0))),
    )
    timeline["Length"] = max(int(timeline.get("Length", 0)), 720)
    save_ymmp(probe, target)
    return probe


def render_preview_gap_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Minimal Animated Explanation Beat Preview Gap v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "User Observation", payload.get("user_observation"))
    _append_mapping(lines, "Actual V1 Readback", payload.get("actual_v1_readback"))
    _append_mapping(
        lines,
        "Contract Claim From Previous Slice",
        payload.get("contract_claim_from_previous_slice"),
    )
    _append_mapping(lines, "Actual YMM4 Visible Gap", payload.get("actual_YMM4_visible_gap"))
    _append_mapping(lines, "Root Cause Classification", payload.get("root_cause_classification"))
    _append_mapping(lines, "V2 Correction Plan", payload.get("v2_correction_plan"))
    _append_mapping(lines, "V2 Materialization Status", payload.get("v2_materialization_status"))
    _append_mapping(lines, "Business Goal Outcome Contract", payload.get("business_goal_outcome_contract"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This artifact records an actual-vs-claim gap. It does not tune "
        "animation, render media, launch YMM4, generate audio/TTS, fetch news, "
        "or approve production/public use."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_visual_gap_fix_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Minimal Animated Explanation Beat Visual Integration Gap Fix v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "User Observation", payload.get("user_observation"))
    _append_mapping(lines, "Actual V1 Readback", payload.get("actual_v1_readback"))
    _append_mapping(lines, "Root Cause Classification", payload.get("root_cause_classification"))
    _append_mapping(lines, "V2 Correction Plan", payload.get("v2_correction_plan"))
    _append_mapping(lines, "V2 Visible Integration Probe", payload.get("v2_visible_integration_probe"))
    _append_mapping(lines, "V2 Readback", payload.get("v2_readback"))
    _append_mapping(lines, "Business Goal Outcome Contract", payload.get("business_goal_outcome_contract"))
    _append_mapping(lines, "Next Recommended Axis", payload.get("next_recommended_axis"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "V2 is an ignored local diagnostic .ymmp with one plain TextItem. It is "
        "not a card redesign, not a render proof, and not production/public "
        "acceptance."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _probe_structure_readback(base: Path, relative_path: Path) -> dict[str, Any]:
    target = base / relative_path
    if not target.exists():
        return {
            "readback_status": "blocked",
            "target_exists": False,
            "reason": "probe_missing",
            "item_type_counts": {},
            "visible_text_or_overlay_item_count": 0,
            "animation_item_count": 0,
        }
    data = load_ymmp(target)
    timeline = _first_timeline(data)
    items = _get_timeline_items(data)
    item_type_counts: dict[str, int] = {}
    for item in items:
        item_type = _item_type(item)
        item_type_counts[item_type] = item_type_counts.get(item_type, 0) + 1
    text_items = [item for item in items if _item_type(item) == "TextItem"]
    shape_items = [item for item in items if _item_type(item) == "ShapeItem"]
    visible_text_items = [item for item in text_items if _is_visible_item(item) and item.get("Text")]
    visible_shape_items = [item for item in shape_items if _is_visible_item(item)]
    animation_item_count = item_type_counts.get("GroupItem", 0) + item_type_counts.get("ImageItem", 0)
    unexpected_item_types = sorted(
        item_type
        for item_type in item_type_counts
        if item_type not in {"GroupItem", "ImageItem", "TextItem", "ShapeItem"}
    )
    structural_pass = bool(timeline) and not unexpected_item_types
    return {
        "readback_status": "structural_pass" if structural_pass else "blocked",
        "target_exists": True,
        "repo_relative_path": relative_path.as_posix(),
        "file_sha256": _sha256(target),
        "file_size_bytes": target.stat().st_size,
        "timeline": {
            "fps": _dict(timeline.get("VideoInfo")).get("FPS") if timeline else None,
            "length_frames": timeline.get("Length") if timeline else None,
            "item_count": len(items),
            "item_type_counts": item_type_counts,
            "unexpected_item_types": unexpected_item_types,
        },
        "actual_item_type_counts": item_type_counts,
        "TextItem_count": len(text_items),
        "ShapeItem_count": len(shape_items),
        "visible_text_item_count": len(visible_text_items),
        "visible_shape_item_count": len(visible_shape_items),
        "visible_text_or_overlay_item_count": len(visible_text_items) + len(visible_shape_items),
        "visible_TextItem_subtitle_card_or_overlay_exists": bool(visible_text_items or visible_shape_items),
        "visible_texts": [item.get("Text") for item in visible_text_items],
        "animation_item_count": animation_item_count,
        "git_check_ignore_result": _git_check_ignore(base, relative_path),
        "YMM4_launch_status": "not_launched",
        "render_status": "not_rendered",
        "audio_tts_status": "not_created",
    }


def _make_visible_text_item() -> dict[str, Any]:
    return {
        "$type": "YukkuriMovieMaker.Project.Items.TextItem, YukkuriMovieMaker",
        "Text": VISIBLE_DIAGNOSTIC_TEXT,
        "Font": "Yu Gothic UI",
        "FontSize": _animation(34),
        "FontColor": "#FFFF66FF",
        "Style": "Normal",
        "X": _animation(-760),
        "Y": _animation(-420),
        "Z": _animation(0),
        "Opacity": _animation(100),
        "Zoom": _animation(100),
        "Rotation": _animation(0),
        "FadeIn": 0,
        "FadeOut": 0,
        "Blend": "Normal",
        "IsAlwaysOnTop": True,
        "IsZOrderEnabled": False,
        "VideoEffects": [],
        "Group": 0,
        "Frame": 0,
        "Layer": 1,
        "KeyFrames": {"Frames": [], "Count": 0},
        "Length": 720,
        "PlaybackRate": 100,
        "ContentOffset": "00:00:00",
        "Remark": VISIBLE_TEXT_REMARK,
        "IsLocked": False,
        "IsHidden": False,
    }


def _animation(value: Any) -> dict[str, Any]:
    return {
        "Values": [{"Value": value}],
        "Span": 0,
        "AnimationType": "なし",
        "Bezier": {
            "Points": [
                {
                    "Point": {"X": 0, "Y": 0},
                    "ControlPoint1": {"X": -0.3, "Y": -0.3},
                    "ControlPoint2": {"X": 0.3, "Y": 0.3},
                },
                {
                    "Point": {"X": 1, "Y": 1},
                    "ControlPoint1": {"X": -0.3, "Y": -0.3},
                    "ControlPoint2": {"X": 0.3, "Y": 0.3},
                },
            ],
            "IsQuadratic": False,
        },
    }


def _is_visible_item(item: dict[str, Any]) -> bool:
    return (
        not item.get("IsHidden", False)
        and int(item.get("Length", 0) or 0) > 0
        and _first_value(item.get("Opacity"), 100) > 0
    )


def _first_value(animated: Any, default: Any = None) -> Any:
    if isinstance(animated, dict):
        values = animated.get("Values")
        if isinstance(values, list) and values:
            return values[0].get("Value", default)
    return default


def _previous_contract_claim(base: Path) -> dict[str, Any]:
    path = base / DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_PATH
    if not path.exists():
        return {"status": "missing_previous_contract"}
    payload = json.loads(path.read_text(encoding="utf-8"))
    beat = dict(payload.get("explanation_beat", {}))
    route = dict(payload.get("mainline_route", {}))
    return {
        "contract_path": DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_PATH.as_posix(),
        "card_overlay_role_claim": beat.get("card_overlay_role"),
        "subtitle_role_claim": beat.get("subtitle_role"),
        "integration_acceptance_claim": payload.get("integration_acceptance"),
        "local_probe_readback_item_type_counts": route.get("local_probe_readback", {})
        .get("timeline", {})
        .get("item_type_counts"),
        "claim_gap": (
            "previous contract described overlay/readback semantics but the materialized "
            "YMM4 v1 probe did not include visible TextItem/ShapeItem overlay items"
        ),
    }


def _root_cause(v1_readback: dict[str, Any], contract_claim: dict[str, Any]) -> dict[str, Any]:
    text_or_overlay_exists = v1_readback.get("visible_TextItem_subtitle_card_or_overlay_exists")
    claim_text = " ".join(
        str(contract_claim.get(key, ""))
        for key in ("card_overlay_role_claim", "subtitle_role_claim")
    )
    contributing = []
    if "readback-only" in claim_text:
        contributing.append("overlay_role_readback_only")
    return {
        "primary": "contract_only_not_materialized"
        if not text_or_overlay_exists
        else "item_present_but_not_visible",
        "contributing": contributing,
        "ruled_out": [
            "item_hidden_or_zero_duration",
            "unknown",
        ]
        if not text_or_overlay_exists
        else ["unknown"],
        "rationale": (
            "The v1 .ymmp has no visible TextItem/ShapeItem/subtitle/card item, "
            "so the integration claim was recorded in JSON/docs but not "
            "materialized into the YMM4-visible scene."
        ),
    }


def _v2_correction_plan() -> dict[str, Any]:
    return {
        "status": "safe_to_materialize_plain_text_overlay",
        "approach": "copy v1 animation items unchanged and add one full-duration TextItem",
        "diagnostic_text": VISIBLE_DIAGNOSTIC_TEXT,
        "visible_item_semantics": "plain TextItem overlay, not a designed card",
        "animation_changes": "none",
        "card_design_changes": "none",
        "render_required": False,
        "YMM4_launch_required_by_agent": False,
    }


def _v2_materialization_status(base: Path) -> dict[str, Any]:
    access = _local_probe_access(
        base,
        LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH,
        "local_ignored_minimal_animated_explanation_beat_v2_visible_integration_probe",
    )
    readback = _probe_structure_readback(base, LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH)
    return {
        "status": "materialized_ignored_local_probe"
        if access.get("target_exists") and readback.get("visible_text_or_overlay_item_count", 0) >= 1
        else "blocked",
        "repo_relative_path": LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH.as_posix(),
        "access_state": access.get("access_state"),
        "visible_text_or_overlay_item_count": readback.get("visible_text_or_overlay_item_count", 0),
        "animation_item_count": readback.get("animation_item_count", 0),
    }


def _v2_materialized(base: Path) -> bool:
    status = _v2_materialization_status(base)
    return (
        status.get("status") == "materialized_ignored_local_probe"
        and status.get("access_state") == "verified_present"
    )


def _source_context(base: Path) -> dict[str, Any]:
    return {
        "source_mainline_proof_path": DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH.as_posix(),
        "source_contract_path": DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_PATH.as_posix(),
        "source_v1_probe_path": LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH.as_posix(),
        "v2_probe_path": LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH.as_posix(),
        "repo_root": str(base.resolve()),
    }


def _business_goal_outcome_contract(*, v2_materialized: bool) -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": True,
            "rationale": "the report explicitly acknowledges the v1 YMM4-visible integration gap",
        },
        "offer_clear": {
            "status": v2_materialized,
            "rationale": "v2 adds one visible plain TextItem while keeping the animation accent unchanged",
        },
        "proof_clear": {
            "status": True,
            "rationale": "animation accent pass is separated from integrated explanation proof failure",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "the fix avoids animation tuning, card polish, render, audio/TTS, and production claims",
        },
        "next_action_clear": {
            "status": True,
            "rationale": NEXT_AXIS_V2_PREVIEW_OPERATOR_INSTRUCTION
            if v2_materialized
            else NEXT_AXIS_TEXTITEM_ROUTE_AUDIT,
        },
        "visual_supports_explanation": {
            "status": "ready_for_one_preview" if v2_materialized else "blocked",
            "rationale": "the visible TextItem is present to support the explanation beat, pending user preview",
        },
    }


def _next_axis_reason(v2_materialized: bool, v2_readback: dict[str, Any]) -> str:
    if v2_materialized:
        return (
            "v2 local ignored probe exists, is ignored by git, and contains one "
            "visible TextItem plus the unchanged 16 animation items"
        )
    if v2_readback.get("visible_text_or_overlay_item_count", 0) == 0:
        return "TextItem/overlay generation did not produce a visible item"
    return "v2 materialization did not pass structural readback"


def _not_accepted_scope_with_gap_boundaries() -> dict[str, bool]:
    scope = _not_accepted_scope()
    scope.update(
        {
            "production_animation_quality": False,
            "render_export_proof": False,
            "public_readiness": False,
            "real_RSS_news_integration": False,
            "speech_balloon_visual_acceptance": False,
            "full_chaban_scene": False,
            "audience_order_acceptance": False,
            "animation_only_probe_loop": False,
            "tempo_only_probe_loop": False,
            "card_redesign_or_density_work": False,
            "polished_visual_card": False,
        }
    )
    return scope


def _boundaries(*, local_v2_created: bool) -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "real_RSS_news_fetch_performed": False,
        "card_assets_modified": False,
        "card_redesign_performed": False,
        "dense_script_modified": False,
        "animation_tuned": False,
        "local_ignored_ymmp_created_in_this_slice": local_v2_created,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
        "actual_order_or_audience_acceptance_claimed": False,
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_animation_only_probe", "status": True},
        {"gate": "no_animation_tuning", "status": True},
        {"gate": "no_primitive_loop", "status": True},
        {"gate": "no_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "next_axis_is_visible_integration_preview", "status": next_axis},
    ]


def main() -> int:
    write_default_newsroom_minimal_animated_explanation_beat_visual_gap_fix_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
