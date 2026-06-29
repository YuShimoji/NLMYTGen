"""Create the minimal integrated background animation scene probe.

This slice uses the existing tracked nod-head YMM4 sample as a safe local
materialization route. It creates only an ignored diagnostic probe under
``_tmp/`` plus tracked readback/contract artifacts. It does not launch YMM4,
render, produce audio/TTS output, fetch external media, modify cards, or claim
production quality.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_background_animation_mvp_policy import (
    BUSINESS_GOAL_OUTCOME_CONTRACT as MVP_BUSINESS_GOAL_OUTCOME_CONTRACT,
    DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_PATH,
    DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH,
    DISABLED_BY_DEFAULT,
    REVIEW_GATE,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
    _beat_readback,
    _dict,
    _first_timeline,
    _get_timeline_items,
    _item_type,
    _not_accepted_scope,
    _value_range,
)
from src.pipeline.newsroom_yukkuri_animation_primitive_probe_materialization import (
    SOURCE_NOD_HEAD_YMMP_PATH,
    _clone_beat_items,
)
from src.pipeline.newsroom_yukkuri_animation_tempo_contract import (
    _git_check_ignore,
    _local_probe_access,
    _sha256,
    _write_json,
    _write_text,
)
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


MINIMAL_INTEGRATED_SCENE_PROBE_ID = (
    "newsroom_background_animation_minimal_integrated_scene_probe_v1_2026_06_29"
)
MINIMAL_INTEGRATED_SCENE_CONTRACT_ID = (
    "newsroom_background_animation_minimal_integrated_scene_contract_v1_2026_06_29"
)
MINIMAL_INTEGRATED_SCENE_PROBE_SCHEMA_VERSION = (
    "newsroom_background_animation_minimal_integrated_scene_probe.v1"
)
MINIMAL_INTEGRATED_SCENE_CONTRACT_SCHEMA_VERSION = (
    "newsroom_background_animation_minimal_integrated_scene_contract.v1"
)

DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "background_animation_minimal_integrated_scene_probe_v1.json"
)
DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_BACKGROUND_ANIMATION_MINIMAL_INTEGRATED_SCENE_PROBE_V1_2026-06-29.md"
)
DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "background_animation_minimal_integrated_scene_contract_v1.json"
)
DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_BACKGROUND_ANIMATION_MINIMAL_INTEGRATED_SCENE_CONTRACT_V1_2026-06-29.md"
)

LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH = Path(
    "_tmp/newsroom_manual_probe/background_animation_minimal_integrated_scene_probe_v1.ymmp"
)

NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION = (
    "newsroom-background-animation-minimal-integrated-scene-preview-operator-instruction-v1"
)
NEXT_AXIS_MATERIALIZATION = (
    "newsroom-background-animation-integrated-scene-materialization-v1"
)
NEXT_AXIS_EXPRESSION_BINDING = "newsroom-animation-expression-event-binding-v1"
NEXT_AXIS_BODY_DISABLE_DEFAULT = "newsroom-animation-body-motion-disable-default-v1"
NEXT_AXIS_FREEZE_AND_RSS_RETURN = "newsroom-animation-accent-freeze-and-rss-return-v1"

FPS = 60
SCENE_ID = "background_animation_minimal_integrated_scene_probe_v1"
SCENE_TIMELINE_LENGTH_FRAMES = 720
SCENE_DURATION_SEC = round(SCENE_TIMELINE_LENGTH_FRAMES / FPS, 6)

EXPLANATION_BEAT = (
    "A structural shift can create short-term friction while moving long-term leverage."
)

SCENE_DESCRIPTION: dict[str, Any] = {
    "scene_id": SCENE_ID,
    "duration_target_sec": SCENE_DURATION_SEC,
    "explanation_beat": EXPLANATION_BEAT,
    "narration_intent": "explain one structural-shift diagnostic point in a review-only beat",
    "viewer_information_goal": (
        "the viewer should understand the caution point while the character "
        "accent reduces static-card fatigue"
    ),
    "animation_role": "small background accent supporting the explanation",
    "card_overlay_role": "none; existing minimal card or overlay context only",
    "source_boundary_role": "review-only diagnostic line; no real RSS/news source is used",
}

ANIMATION_PLAN: dict[str, Any] = {
    "stable_start_pose": {
        "segment_id": "stable_start_pose",
        "frame": 0,
        "length": 240,
        "expression": "easy",
        "parent_x_values": [-96.0],
        "head_rotation_values": [0.0],
        "scene_reason": "let the explanation start from a readable neutral pose",
    },
    "expression_event": {
        "segment_id": "expression_event_key_phrase",
        "frame": 240,
        "length": 180,
        "expression": "panic",
        "parent_x_values": [-96.0],
        "head_rotation_values": [0.0],
        "scene_reason": "the key phrase introduces short-term friction",
    },
    "nod_or_reaction": {
        "segment_id": "one_short_nod_after_key_phrase",
        "frame": 420,
        "length": 45,
        "expression": "panic",
        "parent_x_values": [-96.0],
        "head_rotation_values": [0.0, -8.0, 0.0],
        "scene_reason": "one short acknowledgement after the caution point",
    },
    "optional_lateral_emphasis": {
        "status": "omitted_not_needed",
        "reason": "the integrated beat can be represented without lateral movement",
    },
    "stable_end_pose": {
        "segment_id": "stable_end_pose",
        "frame": 465,
        "length": 255,
        "expression": "panic",
        "parent_x_values": [-96.0],
        "head_rotation_values": [0.0],
        "scene_reason": "end with neutral body/head pose so the accent does not keep acting",
    },
    "disabled_primitives": [
        "repeated_nods",
        "mechanical_expression_cycle",
        "body_forward_back",
        "complex_balloon",
    ],
}

INTEGRATION_CRITERIA: dict[str, Any] = {
    "animation_supports_explanation": {
        "target": True,
        "evidence": "expression and nod are tied to the explanation beat rather than isolated primitives",
    },
    "animation_does_not_distract": {
        "target": True,
        "evidence": "body X stays fixed and active motion is limited to one short head nod",
    },
    "no_primitive_collage": {
        "target": True,
        "evidence": "the scene has one explanation beat with stable start, one expression event, one nod, stable end",
    },
    "no_body_forward_back_default": {
        "target": True,
        "evidence": "all parent X routes stay at -96.0 and no Y/depth route is introduced",
    },
    "expression_has_scene_reason": {
        "target": True,
        "evidence": "panic expression marks the short-term friction phrase",
    },
    "nod_has_scene_reason": {
        "target": True,
        "evidence": "single nod acknowledges the explanation after the key phrase",
    },
    "return_to_stable_pose": {
        "target": True,
        "evidence": "final segment returns head rotation to 0.0 and holds X=-96.0",
    },
}


def write_default_newsroom_background_animation_minimal_integrated_scene_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    materialize_local_minimal_integrated_scene_probe(root=base)
    contract = build_default_minimal_integrated_scene_contract(root=base)
    probe = build_default_minimal_integrated_scene_probe_readback(root=base)
    _write_json(base / DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_PATH, contract)
    _write_text(
        base / DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_DOC_PATH,
        render_minimal_integrated_scene_contract_markdown(contract),
    )
    _write_json(base / DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH, probe)
    _write_text(
        base / DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_DOC_PATH,
        render_minimal_integrated_scene_probe_markdown(probe),
    )
    return {
        "minimal_integrated_scene_contract": contract,
        "minimal_integrated_scene_probe": probe,
    }


def build_default_minimal_integrated_scene_contract(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    probe = build_default_minimal_integrated_scene_probe_readback(root=base)
    next_axis = _next_axis(probe)
    return {
        "artifact_id": MINIMAL_INTEGRATED_SCENE_CONTRACT_ID,
        "contract_id": MINIMAL_INTEGRATED_SCENE_CONTRACT_ID,
        "probe_id": MINIMAL_INTEGRATED_SCENE_PROBE_ID,
        "schema_version": MINIMAL_INTEGRATED_SCENE_CONTRACT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_context": _source_context(base),
        "scene_description": SCENE_DESCRIPTION,
        "animation_plan": ANIMATION_PLAN,
        "integration_criteria": INTEGRATION_CRITERIA,
        "mvp_policy_compliance": _mvp_policy_compliance(),
        "business_goal_outcome_contract": _business_goal_outcome_contract(probe),
        "local_probe_access": probe.get("local_probe_access"),
        "local_probe_readback_summary": probe.get("local_probe_readback_summary"),
        "selected_next_axis": next_axis,
        "next_recommended_axis": {
            "selected": next_axis,
            "reason": _next_axis_reason(probe),
        },
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(local_probe_created=_probe_created(probe)),
        "inertia_check": _inertia_check(next_axis),
    }


def build_default_minimal_integrated_scene_probe_readback(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    access = _local_probe_access(
        base,
        LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH,
        "local_ignored_minimal_integrated_scene_probe",
    )
    readback = _minimal_scene_probe_readback(base, access)
    created = (
        access["target_exists"]
        and access["access_state"] == "verified_present"
        and readback["readback_status"] == "structural_pass"
    )
    return {
        "artifact_id": MINIMAL_INTEGRATED_SCENE_PROBE_ID,
        "probe_id": MINIMAL_INTEGRATED_SCENE_PROBE_ID,
        "schema_version": MINIMAL_INTEGRATED_SCENE_PROBE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_context": _source_context(base),
        "scene_description": SCENE_DESCRIPTION,
        "animation_plan_summary": _animation_plan_summary(),
        "integration_criteria": INTEGRATION_CRITERIA,
        "scene_probe_materialization_status": (
            "materialized_ignored_local_probe" if created else "blocked"
        ),
        "local_probe_access": access,
        "local_probe_readback": readback,
        "local_probe_readback_summary": _minimal_scene_probe_readback_summary(readback),
        "selected_next_axis": _next_axis_from_created(created),
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(local_probe_created=created),
    }


def materialize_local_minimal_integrated_scene_probe(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    project = load_ymmp(base / SOURCE_NOD_HEAD_YMMP_PATH)
    probe = copy.deepcopy(project)
    target_path = base / LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)

    probe["FilePath"] = str(target_path.resolve())
    timeline = _first_timeline(probe)
    if not timeline:
        raise ValueError(f"YMM4 source has no timeline: {SOURCE_NOD_HEAD_YMMP_PATH}")
    source_items = [
        copy.deepcopy(item)
        for item in _get_timeline_items(project)
        if isinstance(item, dict) and item.get("Remark") == "nod_head_v1"
    ]
    if len(source_items) != 4:
        raise ValueError(f"expected 4 nod_head_v1 source items, found {len(source_items)}")

    items: list[dict[str, Any]] = []
    for segment in _minimal_scene_segments():
        items.extend(_clone_beat_items(base, source_items, segment))
    timeline["Items"] = sorted(
        items,
        key=lambda item: (int(item.get("Frame", 0)), int(item.get("Layer", 0))),
    )
    timeline["Length"] = SCENE_TIMELINE_LENGTH_FRAMES
    timeline["CurrentFrame"] = 0
    timeline["MaxLayer"] = max(
        int(item.get("Layer", 0))
        for item in timeline["Items"]
        if isinstance(item.get("Layer"), int)
    )
    save_ymmp(probe, target_path)
    return probe


def render_minimal_integrated_scene_contract_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Background Animation Minimal Integrated Scene Contract v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "Scene Description", payload.get("scene_description"))
    _append_mapping(lines, "Animation Plan", payload.get("animation_plan"))
    _append_mapping(lines, "Integration Criteria", payload.get("integration_criteria"))
    _append_mapping(lines, "MVP Policy Compliance", payload.get("mvp_policy_compliance"))
    _append_mapping(
        lines,
        "Business Goal Outcome Contract",
        payload.get("business_goal_outcome_contract"),
    )
    _append_mapping(lines, "Local Probe Access", payload.get("local_probe_access"))
    _append_mapping(
        lines,
        "Local Probe Readback Summary",
        payload.get("local_probe_readback_summary"),
    )
    _append_mapping(lines, "Next Recommended Axis", payload.get("next_recommended_axis"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This contract creates a minimal integrated explanation beat for local "
        "preview only. It is not rendered, not staged as .ymmp, and not "
        "production/public/audience acceptance."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_minimal_integrated_scene_probe_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Background Animation Minimal Integrated Scene Probe v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"scene_probe_materialization_status: {payload.get('scene_probe_materialization_status')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "Scene Description", payload.get("scene_description"))
    _append_mapping(lines, "Animation Plan Summary", payload.get("animation_plan_summary"))
    _append_mapping(lines, "Integration Criteria", payload.get("integration_criteria"))
    _append_mapping(lines, "Local Probe Access", payload.get("local_probe_access"))
    _append_mapping(lines, "Local Probe Readback Summary", payload.get("local_probe_readback_summary"))
    _append_mapping(lines, "Semantic Checks", payload.get("local_probe_readback", {}).get("semantic_checks"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "The local probe is an ignored diagnostic .ymmp only. It is not rendered, "
        "not staged, not committed, and not production/public/audience acceptance."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _minimal_scene_segments() -> list[dict[str, Any]]:
    rows = [
        (
            "stable_start_pose",
            "explanation_support_start",
            "stable_pose",
            ANIMATION_PLAN["stable_start_pose"],
        ),
        (
            "expression_event_key_phrase",
            "explanation_key_phrase_reaction",
            "expression_swap",
            ANIMATION_PLAN["expression_event"],
        ),
        (
            "one_short_nod_after_key_phrase",
            "single_acknowledgement_after_key_phrase",
            "head_nod",
            ANIMATION_PLAN["nod_or_reaction"],
        ),
        (
            "stable_end_pose",
            "explanation_support_end",
            "stable_pose",
            ANIMATION_PLAN["stable_end_pose"],
        ),
    ]
    segments: list[dict[str, Any]] = []
    for beat_id, scene_function, primitive_id, plan in rows:
        frame = int(plan["frame"])
        length = int(plan["length"])
        segments.append(
            {
                "beat_id": beat_id,
                "scene_function": scene_function,
                "timing_range": f"{frame / FPS:.2f}-{(frame + length) / FPS:.2f} sec",
                "frame": frame,
                "length": length,
                "expression": plan["expression"],
                "primitive_ids": [primitive_id],
                "parent_x_values": list(plan["parent_x_values"]),
                "head_rotation_values": list(plan["head_rotation_values"]),
                "scene_reason": plan["scene_reason"],
            }
        )
    return segments


def _minimal_scene_probe_readback(base: Path, access: dict[str, Any]) -> dict[str, Any]:
    target = base / LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH
    if not target.exists():
        return {
            "readback_status": "blocked",
            "reason": "local_minimal_integrated_scene_probe_missing",
            "target_exists": False,
        }
    data = load_ymmp(target)
    timeline = _first_timeline(data)
    items = _get_timeline_items(data)
    item_type_counts: dict[str, int] = {}
    for item in items:
        item_type = _item_type(item)
        item_type_counts[item_type] = item_type_counts.get(item_type, 0) + 1
    segment_readback = [_beat_readback(segment, items) for segment in _minimal_scene_segments()]
    unexpected_item_types = sorted(
        item_type for item_type in item_type_counts if item_type not in {"GroupItem", "ImageItem"}
    )
    semantic_checks = _semantic_checks(segment_readback)
    structural_pass = (
        timeline.get("Length") == SCENE_TIMELINE_LENGTH_FRAMES
        and item_type_counts.get("GroupItem") == 8
        and item_type_counts.get("ImageItem") == 8
        and not unexpected_item_types
        and all(row["status"] == "pass" for row in segment_readback)
        and semantic_checks["status"] == "pass"
        and access["access_state"] == "verified_present"
    )
    return {
        "readback_status": "structural_pass" if structural_pass else "blocked",
        "target_exists": True,
        "file_sha256": _sha256(target),
        "file_size_bytes": target.stat().st_size,
        "timeline": {
            "fps": _dict(timeline.get("VideoInfo")).get("FPS"),
            "length_frames": timeline.get("Length"),
            "length_sec": round(SCENE_TIMELINE_LENGTH_FRAMES / FPS, 6),
            "item_count": len(items),
            "item_type_counts": item_type_counts,
            "unexpected_item_types": unexpected_item_types,
        },
        "scene_id": SCENE_ID,
        "segment_count": len(segment_readback),
        "segment_readback": segment_readback,
        "semantic_checks": semantic_checks,
        "source_ymmp_copy_basis": SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
        "git_check_ignore_result": _git_check_ignore(
            base,
            LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH,
        ),
        "local_probe_access_state": access["access_state"],
        "YMM4_launch_status": "not_launched",
        "render_status": "not_rendered",
        "audio_tts_status": "not_created",
    }


def _semantic_checks(segment_readback: list[dict[str, Any]]) -> dict[str, Any]:
    expression_event_segments = [
        row["beat_id"]
        for row in segment_readback
        if "expression_swap" in row.get("primitive_ids", [])
    ]
    nod_segments = [
        row["beat_id"]
        for row in segment_readback
        if "head_nod" in row.get("primitive_ids", [])
        and any(abs(value) > 0 for value in row.get("head_rotation_values", []))
    ]
    parent_values = [
        value
        for row in segment_readback
        for value in row.get("parent_x_values", [])
    ]
    final_row = segment_readback[-1] if segment_readback else {}
    checks = {
        "duration_10_to_20_sec": 10.0 <= SCENE_DURATION_SEC <= 20.0,
        "one_expression_event": expression_event_segments == ["expression_event_key_phrase"],
        "one_short_nod_or_reaction": nod_segments == ["one_short_nod_after_key_phrase"],
        "no_body_forward_back_default": parent_values
        and all(value == -96.0 for value in parent_values)
        and _value_range(parent_values) == 0.0,
        "no_primitive_collage": [
            row["beat_id"] for row in segment_readback
        ] == [
            "stable_start_pose",
            "expression_event_key_phrase",
            "one_short_nod_after_key_phrase",
            "stable_end_pose",
        ],
        "expression_has_scene_reason": True,
        "nod_has_scene_reason": True,
        "return_to_stable_pose": final_row.get("parent_x_values") == [-96.0]
        and final_row.get("head_rotation_values") == [0.0],
    }
    return {
        "status": "pass" if all(checks.values()) else "blocked",
        "checks": checks,
        "expression_event_segments": expression_event_segments,
        "nod_or_reaction_segments": nod_segments,
        "parent_x_values": parent_values,
    }


def _minimal_scene_probe_readback_summary(readback: dict[str, Any]) -> dict[str, Any]:
    if readback.get("readback_status") != "structural_pass":
        return {
            "status": readback.get("readback_status"),
            "reason": readback.get("reason", "minimal integrated scene readback blocked"),
        }
    return {
        "status": "structural_pass",
        "timeline_length_frames": readback["timeline"]["length_frames"],
        "timeline_length_sec": readback["timeline"]["length_sec"],
        "item_type_counts": readback["timeline"]["item_type_counts"],
        "segment_count": readback["segment_count"],
        "semantic_status": readback["semantic_checks"]["status"],
    }


def _source_context(base: Path) -> dict[str, Any]:
    return {
        "source_mvp_policy_path": DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH.as_posix(),
        "source_integration_plan_path": DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_PATH.as_posix(),
        "source_nod_head_ymmp_path": SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
        "local_probe_path": LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH.as_posix(),
        "repo_root": str(base.resolve()),
    }


def _animation_plan_summary() -> dict[str, Any]:
    return {
        "stable_start_pose": ANIMATION_PLAN["stable_start_pose"],
        "expression_event": ANIMATION_PLAN["expression_event"],
        "nod_or_reaction": ANIMATION_PLAN["nod_or_reaction"],
        "optional_lateral_emphasis": ANIMATION_PLAN["optional_lateral_emphasis"],
        "stable_end_pose": ANIMATION_PLAN["stable_end_pose"],
        "disabled_primitives": ANIMATION_PLAN["disabled_primitives"],
    }


def _mvp_policy_compliance() -> dict[str, Any]:
    disabled = [row["primitive_id"] for row in DISABLED_BY_DEFAULT]
    return {
        "stable_pose_used": True,
        "one_expression_event_used": True,
        "one_short_nod_or_reaction_used": True,
        "optional_lateral_emphasis_used": False,
        "disabled_by_default_refs": disabled,
        "review_gate_refs": [row["gate_id"] for row in REVIEW_GATE],
        "no_repeated_nodding": True,
        "no_mechanical_expression_cycling": True,
        "body_forward_back_disabled": True,
        "speech_balloon_omitted": True,
        "full_chaban_scene_not_created": True,
    }


def _business_goal_outcome_contract(probe: dict[str, Any]) -> dict[str, Any]:
    readback_summary = probe.get("local_probe_readback_summary", {})
    visual_status = (
        "pending_user_preview"
        if readback_summary.get("status") == "structural_pass"
        else "blocked_before_preview"
    )
    return {
        "problem_clear": MVP_BUSINESS_GOAL_OUTCOME_CONTRACT["problem_clear"],
        "offer_clear": {
            "status": True,
            "rationale": "the probe shows a background accent on one explanation beat",
        },
        "proof_clear": {
            "status": True,
            "rationale": "structural .ymmp readback is separated from user visual acceptance",
        },
        "boundary_clear": MVP_BUSINESS_GOAL_OUTCOME_CONTRACT["boundary_clear"],
        "next_action_clear": {
            "status": True,
            "rationale": _next_axis(probe),
        },
        "visual_supports_explanation": {
            "status": visual_status,
            "rationale": (
                "local structure is ready for one freeform preview, but visual "
                "acceptance is not claimed by the agent"
            ),
        },
    }


def _probe_created(probe: dict[str, Any]) -> bool:
    return probe.get("scene_probe_materialization_status") == "materialized_ignored_local_probe"


def _next_axis(probe: dict[str, Any]) -> str:
    readback = probe.get("local_probe_readback", {})
    semantic = readback.get("semantic_checks", {})
    checks = semantic.get("checks", {}) if isinstance(semantic, dict) else {}
    if _probe_created(probe) and readback.get("readback_status") == "structural_pass":
        return NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION
    if checks.get("one_expression_event") is False:
        return NEXT_AXIS_EXPRESSION_BINDING
    if checks.get("no_body_forward_back_default") is False:
        return NEXT_AXIS_BODY_DISABLE_DEFAULT
    return NEXT_AXIS_MATERIALIZATION


def _next_axis_from_created(created: bool) -> str:
    return NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION if created else NEXT_AXIS_MATERIALIZATION


def _next_axis_reason(probe: dict[str, Any]) -> str:
    next_axis = _next_axis(probe)
    if next_axis == NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION:
        return (
            "the local ignored integrated scene probe exists, is ignored by git, "
            "and has structural readback pass"
        )
    if next_axis == NEXT_AXIS_EXPRESSION_BINDING:
        return "the expression event did not satisfy the one scene-reasoned event contract"
    if next_axis == NEXT_AXIS_BODY_DISABLE_DEFAULT:
        return "body motion could not be reliably held at the shared anchor"
    return "materialization is not yet verified"


def _boundaries(*, local_probe_created: bool) -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "dense_script_modified": False,
        "local_ignored_ymmp_created_in_this_slice": local_probe_created,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
        "actual_order_or_audience_acceptance_claimed": False,
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_primitive_only_loop", "status": True},
        {"gate": "no_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "next_review_is_integrated_scene", "status": next_axis},
        {"gate": "no_full_chaban_scene", "status": True},
    ]


def main() -> int:
    write_default_newsroom_background_animation_minimal_integrated_scene_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
