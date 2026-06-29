"""Record the v4 tempo sweep observation and scene-beat tempo policy.

This slice exits the primitive-only fast/slow loop by selecting the default
tempo band from the user's v4 sweep observation. It keeps scene choreography
artifacts diagnostic-only and routes the next proof to scene-beat integration.
It does not launch YMM4, render, create audio/TTS, fetch external media, or
claim production quality.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    DEFAULT_MOTION_CONTRACT_PATH,
    _append_mapping,
    _append_rows,
    _beat_readback,
    _dict,
    _first_timeline,
    _get_timeline_items,
    _item_type,
    _not_accepted_scope,
    _route_values,
    _value_range,
)
from src.pipeline.newsroom_yukkuri_animation_primitive_probe_materialization import (
    SOURCE_NOD_HEAD_YMMP_PATH,
    _clone_beat_items,
)
from src.pipeline.newsroom_yukkuri_animation_tempo_sweep import (
    DEFAULT_TEMPO_SWEEP_CONTRACT_PATH,
    LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH,
    _git_check_ignore,
    _local_probe_access,
    _sha256,
    _write_json,
    _write_text,
)
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


V4_SWEEP_OBSERVATION_ID = (
    "newsroom_yukkuri_animation_v4_tempo_sweep_observation_v1_2026_06_29"
)
SCENE_CHOREOGRAPHY_CONTRACT_ID = (
    "newsroom_yukkuri_animation_scene_choreography_contract_v1_2026_06_29"
)
SCENE_CHOREOGRAPHY_PROBE_ID = (
    "newsroom_yukkuri_animation_scene_choreography_probe_v1_2026_06_29"
)
V4_SWEEP_OBSERVATION_SCHEMA_VERSION = (
    "newsroom_yukkuri_animation_v4_tempo_sweep_observation.v1"
)
SCENE_CHOREOGRAPHY_CONTRACT_SCHEMA_VERSION = (
    "newsroom_yukkuri_animation_scene_choreography_contract.v1"
)
SCENE_CHOREOGRAPHY_PROBE_SCHEMA_VERSION = (
    "newsroom_yukkuri_animation_scene_choreography_probe.v1"
)

DEFAULT_V4_SWEEP_OBSERVATION_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "yukkuri_animation_v4_tempo_sweep_observation_v1.json"
)
DEFAULT_V4_SWEEP_OBSERVATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_YUKKURI_ANIMATION_V4_TEMPO_SWEEP_OBSERVATION_V1_2026-06-29.md"
)
DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "yukkuri_animation_scene_choreography_contract_v1.json"
)
DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_YUKKURI_ANIMATION_SCENE_CHOREOGRAPHY_CONTRACT_V1_2026-06-29.md"
)
DEFAULT_SCENE_CHOREOGRAPHY_PROBE_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "yukkuri_animation_scene_choreography_probe_v1.json"
)

LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH = Path(
    "_tmp/newsroom_manual_probe/yukkuri_animation_scene_choreography_probe_v1.ymmp"
)

NEXT_AXIS_SCENE_PREVIEW = (
    "newsroom-yukkuri-animation-scene-beat-integration-v1"
)
FALLBACK_AXIS_SCENE_IMPLEMENTATION = (
    "newsroom-yukkuri-animation-scene-beat-integration-prep-v1"
)
EXPRESSION_BINDING_AXIS = (
    "newsroom-yukkuri-animation-expression-event-binding-v1"
)
BODY_FACING_FIX_AXIS = (
    "newsroom-yukkuri-animation-body-motion-role-and-facing-fix-v1"
)
TIMING_STRUCTURE_AUDIT_AXIS = (
    "newsroom-yukkuri-animation-timing-structure-audit-v1"
)

FPS = 60
SCENE_ID = "yukkuri_scene_choreography_probe_v1"
SCENE_TIMELINE_LENGTH_FRAMES = 1080

NORMALIZED_V4_SWEEP_OBSERVATION: dict[str, Any] = {
    "source_observation_role": "user_opened_local_v4_tempo_sweep_preview",
    "source_v4_probe_path": LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH.as_posix(),
    "yym4_opened": True,
    "v4_preview_observed": True,
    "default_tempo_band": "0.75s",
    "default_frame_span_at_60fps": 45,
    "scene_dependency": True,
    "one_second_status": "acceptable_variant_for_slower_explanatory_or_readability_heavy_moments",
    "half_second_status": "acceptable_variant_for_quick_reaction_punch_or_small_emphasis",
    "one_point_five_second_status": "not_selected_as_default_upper_comparison_or_special_slow_case_only",
    "tempo_loop_exit": True,
    "primitive_only_loop_exit": True,
    "next_axis": NEXT_AXIS_SCENE_PREVIEW,
    "render_export_checked": False,
    "render_export_required_now": False,
    "production_public_render_approval_given": False,
}

V4_USER_OBSERVATION_NOTES = [
    "0.75s looks the most natural.",
    "However, the best duration depends on the scene.",
    "1.0s is also within acceptable range.",
    "0.5s is also within acceptable range.",
    "No production/public/render approval was given.",
]

TEMPO_DEFAULT_POLICY: dict[str, Any] = {
    "policy_id": "newsroom_yukkuri_animation_v4_tempo_default_policy_v1_2026_06_29",
    "status": "active_for_scene_beat_integration",
    "scene_dependency": True,
    "default_tempo_band": "0.75s",
    "default_frame_span_at_60fps": 45,
    "default_use_case": "default light reenactment beat",
    "use_case_policy": [
        {
            "use_case": "default light reenactment beat",
            "tempo": "0.75s",
            "frames_at_60fps": 45,
            "note": "user-selected most natural",
        },
        {
            "use_case": "quick reaction / punch / short emphasis",
            "tempo": "0.5s",
            "frames_at_60fps": 30,
            "note": "acceptable but use selectively",
        },
        {
            "use_case": "explanatory / readable / calmer beat",
            "tempo": "1.0s",
            "frames_at_60fps": 60,
            "note": "acceptable, useful when readability matters",
        },
        {
            "use_case": "slow upper comparison",
            "tempo": "1.5s",
            "frames_at_60fps": 90,
            "note": "not default; contrast or special slow scene only",
        },
    ],
    "next_axis": NEXT_AXIS_SCENE_PREVIEW,
    "source_user_observation": V4_USER_OBSERVATION_NOTES,
}

PROVISIONAL_TEMPO_POLICY: dict[str, Any] = {
    "default_reaction_motion": "45 frames / 0.75s",
    "quick_reaction_or_punch": "30 frames / 0.5s",
    "readability_heavy_or_calm_explanation": "60 frames / 1.0s",
    "slow_upper_comparison": "90 frames / 1.5s",
    "scene_dependency": True,
    "status": "superseded_by_tempo_default_policy",
}

CHOREOGRAPHY_RULES = [
    "every motion must have a scene function",
    "do not cycle expressions mechanically",
    "expression changes must be tied to a beat reason",
    "do not repeat nodding unless the scene calls for repeated acknowledgement",
    "do not use body forward/back movement unless it expresses a clear action",
    "use 0.75s / 45 frames as the default light reenactment beat",
    "use 0.5s / 30 frames only for quick reaction, punch, or short emphasis",
    "use 1.0s / 60 frames for slower explanatory or readability-heavy moments",
    "keep 1.5s / 90 frames as a slow comparison or special-case upper bound",
    "prefer short active motion plus readable hold",
    "preserve anchor continuity",
    "avoid floaty drifting",
    "avoid cheap-looking tilt loops by limiting nod count and using neutral return",
    "treat cards and overlays as optional support, not the animation target",
]

SCENE_BEAT_INTEGRATION_RISKS = [
    {
        "risk_id": "primitive_only_tempo_loop",
        "status": "exited",
        "mitigation": "use the tempo policy inside an actual scene/beat structure",
    },
    {
        "risk_id": "scene_dependent_timing",
        "status": "active",
        "mitigation": "select 0.5s, 0.75s, or 1.0s by beat function instead of forcing one global value",
    },
    {
        "risk_id": "slow_upper_bound_overuse",
        "status": "guarded",
        "mitigation": "do not use 1.5s as default; reserve it for contrast or a specific slow scene",
    },
]

SCENE_BEAT_MAPPING: list[dict[str, Any]] = [
    {
        "scene_id": SCENE_ID,
        "scene_function": "establish_readable_listening_state",
        "beat_id": "beat_a_neutral_listening_pose",
        "viewer_information_goal": "show the character is present and listening before the reaction starts",
        "character_state_before": "neutral stable pose at shared anchor",
        "motion_reason": "no movement; this beat prevents immediate primitive playback",
        "primitive_used": ["stable_hold"],
        "expression": "easy",
        "expression_reason": "calm listening state before the question cue",
        "facing_policy": "neutral front-facing proxy; no facing flip is claimed",
        "anchor_policy": "hold X=-96 throughout the beat",
        "frame": 0,
        "length": 180,
        "active_motion_span": 0,
        "hold_span": 180,
        "parent_x_values": [-96.0],
        "head_rotation_values": [0.0],
        "transition_policy": "hard scene start into stable pose",
        "forbidden_motion": ["nod_loop", "body_forward_back", "expression_cycle"],
        "fallback_if_primitive_unavailable": "static easy expression at X=-96",
    },
    {
        "scene_id": SCENE_ID,
        "scene_function": "question_reaction_cue",
        "beat_id": "beat_b_question_reaction_cue",
        "viewer_information_goal": "mark that a question or concern has appeared",
        "character_state_before": "neutral listening pose",
        "motion_reason": "expression change carries the reaction; body stays anchored",
        "primitive_used": ["expression_swap"],
        "expression": "panic",
        "expression_reason": "concerned reaction to the question cue",
        "facing_policy": "keep facing stable; do not imply walking backward",
        "anchor_policy": "hold X=-96 throughout the beat",
        "frame": 180,
        "length": 180,
        "active_motion_span": 0,
        "hold_span": 180,
        "parent_x_values": [-96.0],
        "head_rotation_values": [0.0],
        "transition_policy": "instant expression swap at beat boundary followed by readable hold",
        "forbidden_motion": ["extra_nod", "body_forward_back", "expression_cycle"],
        "fallback_if_primitive_unavailable": "hold neutral expression and mark expression binding unresolved",
    },
    {
        "scene_id": SCENE_ID,
        "scene_function": "single_acknowledgement",
        "beat_id": "beat_c_one_short_ack_nod",
        "viewer_information_goal": "show a single acknowledgement before explanation continues",
        "character_state_before": "question reaction pose",
        "motion_reason": "one nod acknowledges the question; it is not repeated",
        "primitive_used": ["head_nod"],
        "expression": "easy",
        "expression_reason": "return to explanation-ready confidence after the question cue",
        "facing_policy": "head tilt only; no body direction change",
        "anchor_policy": "hold X=-96 while the nod returns to neutral",
        "frame": 360,
        "length": 180,
        "active_motion_span": 45,
        "hold_span": 135,
        "parent_x_values": [-96.0],
        "head_rotation_values": [0.0, -8.0, 0.0],
        "transition_policy": "45-frame active nod followed by neutral hold",
        "forbidden_motion": ["second_nod", "body_forward_back", "expression_cycle"],
        "fallback_if_primitive_unavailable": "skip nod and rely on the expression return to easy",
    },
    {
        "scene_id": SCENE_ID,
        "scene_function": "risk_emphasis_expression",
        "beat_id": "beat_d_reasoned_expression_shift",
        "viewer_information_goal": "mark the moment where the explanation turns to risk or caution",
        "character_state_before": "explanation-ready pose",
        "motion_reason": "expression change carries emphasis; no extra body motion is needed",
        "primitive_used": ["expression_swap"],
        "expression": "anger",
        "expression_reason": "risk/caution emphasis rather than mechanical sequence",
        "facing_policy": "keep facing stable",
        "anchor_policy": "hold X=-96 throughout the beat",
        "frame": 540,
        "length": 180,
        "active_motion_span": 0,
        "hold_span": 180,
        "parent_x_values": [-96.0],
        "head_rotation_values": [0.0],
        "transition_policy": "instant expression swap at beat boundary followed by readable hold",
        "forbidden_motion": ["nod_loop", "body_forward_back", "random_expression_swap"],
        "fallback_if_primitive_unavailable": "hold easy expression and mark caution expression unresolved",
    },
    {
        "scene_id": SCENE_ID,
        "scene_function": "intentional_small_emphasis_move",
        "beat_id": "beat_e_one_small_intentional_nudge",
        "viewer_information_goal": "show one small emphasis move tied to the caution point",
        "character_state_before": "risk emphasis pose",
        "motion_reason": "small nudge underlines emphasis, then returns to the shared anchor",
        "primitive_used": ["small_position_move"],
        "expression": "anger",
        "expression_reason": "same caution expression holds while the body makes one intentional nudge",
        "facing_policy": "lateral nudge only; no forward/back or facing claim",
        "anchor_policy": "start and end at X=-96",
        "frame": 720,
        "length": 180,
        "active_motion_span": 60,
        "hold_span": 120,
        "parent_x_values": [-96.0, -108.0, -96.0],
        "head_rotation_values": [0.0],
        "transition_policy": "60-frame nudge followed by anchor hold",
        "forbidden_motion": ["body_forward_back", "long_drift", "second_nudge"],
        "fallback_if_primitive_unavailable": "drop the nudge and keep the caution expression",
    },
    {
        "scene_id": SCENE_ID,
        "scene_function": "return_to_stable_explanation_pose",
        "beat_id": "beat_f_stable_explanation_pose",
        "viewer_information_goal": "settle the scene back into a stable explanation pose",
        "character_state_before": "post-emphasis anchored pose",
        "motion_reason": "no movement; the beat closes the mini-scene cleanly",
        "primitive_used": ["expression_swap", "stable_hold"],
        "expression": "easy",
        "expression_reason": "return from caution to explanation-ready tone",
        "facing_policy": "neutral front-facing proxy; no facing flip is claimed",
        "anchor_policy": "hold X=-96 throughout the beat",
        "frame": 900,
        "length": 180,
        "active_motion_span": 0,
        "hold_span": 180,
        "parent_x_values": [-96.0],
        "head_rotation_values": [0.0],
        "transition_policy": "instant expression return followed by readable hold",
        "forbidden_motion": ["closing_nod_loop", "body_forward_back", "extra_expression_cycle"],
        "fallback_if_primitive_unavailable": "hold previous expression and mark close expression unresolved",
    },
]


def write_default_newsroom_yukkuri_animation_scene_choreography_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    materialize_local_scene_choreography_probe(root=base)
    observation = build_default_v4_sweep_observation(root=base)
    contract = build_default_scene_choreography_contract(root=base)
    probe = build_default_scene_choreography_probe_readback(root=base)
    _write_json(base / DEFAULT_V4_SWEEP_OBSERVATION_PATH, observation)
    _write_text(
        base / DEFAULT_V4_SWEEP_OBSERVATION_DOC_PATH,
        render_v4_sweep_observation_markdown(observation),
    )
    _write_json(base / DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_PATH, contract)
    _write_text(
        base / DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_DOC_PATH,
        render_scene_choreography_contract_markdown(contract),
    )
    _write_json(base / DEFAULT_SCENE_CHOREOGRAPHY_PROBE_PATH, probe)
    return {
        "observation": observation,
        "scene_choreography_contract": contract,
        "scene_choreography_probe": probe,
    }


def build_default_v4_sweep_observation(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    v4_access = _local_probe_access(base, LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH, "local_ignored_v4_tempo_sweep_probe")
    return {
        "artifact_id": V4_SWEEP_OBSERVATION_ID,
        "observation_id": V4_SWEEP_OBSERVATION_ID,
        "schema_version": V4_SWEEP_OBSERVATION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_v4_probe_path": LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH.as_posix(),
        "source_v4_probe_access": v4_access,
        "source_tempo_sweep_contract_path": DEFAULT_TEMPO_SWEEP_CONTRACT_PATH.as_posix(),
        "user_observation_notes": V4_USER_OBSERVATION_NOTES,
        "normalized_user_observation": NORMALIZED_V4_SWEEP_OBSERVATION,
        "tempo_default_policy": TEMPO_DEFAULT_POLICY,
        "tempo_only_loop_exit": {
            "exit": True,
            "reason": (
                "The v4 sweep has selected a default timing policy: 0.75s / "
                "45 frames is the most natural default, while 0.5s and 1.0s "
                "remain acceptable by scene. The next bottleneck is applying "
                "that policy inside scene beats, not another primitive-only "
                "fast/slow loop."
            ),
            "next_axis": NEXT_AXIS_SCENE_PREVIEW,
        },
        "primitive_feasibility_judgment": {
            "status": "not_reopened",
            "reason": "this readback records tempo selection only; production animation quality remains unapproved",
        },
        "motion_coherence_warning": {
            "status": "deferred_to_scene_beat_integration",
            "issues": [
                "duration choice depends on scene function",
                "primitive timing should be evaluated inside a scene-beat structure",
            ],
        },
        "render_export_checked": False,
        "render_export_required_now": False,
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(scene_probe_created=False),
    }


def build_default_scene_choreography_contract(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    probe_payload = build_default_scene_choreography_probe_readback(root=base)
    scene_created = probe_payload["scene_probe_materialization_status"] == "materialized_ignored_local_probe"
    next_axis = _next_axis(scene_created=scene_created, probe_payload=probe_payload)
    return {
        "artifact_id": SCENE_CHOREOGRAPHY_CONTRACT_ID,
        "scene_choreography_contract_id": SCENE_CHOREOGRAPHY_CONTRACT_ID,
        "schema_version": SCENE_CHOREOGRAPHY_CONTRACT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_context": {
            "source_v4_probe_path": LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH.as_posix(),
            "source_v4_observation_path": DEFAULT_V4_SWEEP_OBSERVATION_PATH.as_posix(),
            "source_tempo_sweep_contract_path": DEFAULT_TEMPO_SWEEP_CONTRACT_PATH.as_posix(),
            "source_motion_contract_path": DEFAULT_MOTION_CONTRACT_PATH.as_posix(),
            "source_nod_head_ymmp_path": SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
        },
        "tempo_default_policy": TEMPO_DEFAULT_POLICY,
        "provisional_tempo_policy": PROVISIONAL_TEMPO_POLICY,
        "choreography_rules": CHOREOGRAPHY_RULES,
        "scene_beat_integration_risks": SCENE_BEAT_INTEGRATION_RISKS,
        "scene_beat_mapping": _scene_beat_contract_rows(),
        "v1_scene_probe_plan": _scene_probe_plan(),
        "scene_probe_materialization_status": probe_payload["scene_probe_materialization_status"],
        "scene_probe_access": probe_payload["scene_probe_access"],
        "scene_probe_readback_summary": probe_payload["scene_probe_readback_summary"],
        "selected_next_axis": next_axis,
        "next_recommended_axis": {
            "selected": next_axis,
            "reason": _next_axis_reason(scene_created=scene_created, probe_payload=probe_payload),
            "prerequisites": [
                "keep scene choreography .ymmp ignored and unstaged",
                "use scene-beat integration before any render request",
                "do not claim production/public acceptance",
            ],
        },
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(scene_probe_created=scene_created),
        "inertia_check": _inertia_check(next_axis),
    }


def build_default_scene_choreography_probe_readback(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    access = _local_probe_access(
        base,
        LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH,
        "local_ignored_scene_choreography_probe",
    )
    readback = _scene_probe_readback(base, access)
    created = (
        access["target_exists"]
        and access["access_state"] == "verified_present"
        and readback["readback_status"] == "structural_pass"
    )
    return {
        "artifact_id": SCENE_CHOREOGRAPHY_PROBE_ID,
        "scene_choreography_probe_id": SCENE_CHOREOGRAPHY_PROBE_ID,
        "schema_version": SCENE_CHOREOGRAPHY_PROBE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_context": {
            "source_v4_probe_path": LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH.as_posix(),
            "source_scene_choreography_contract_path": DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_PATH.as_posix(),
            "source_nod_head_ymmp_path": SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
        },
        "scene_probe_materialization_status": (
            "materialized_ignored_local_probe" if created else "blocked"
        ),
        "scene_probe_access": access,
        "scene_probe_plan": _scene_probe_plan(),
        "scene_probe_readback": readback,
        "scene_probe_readback_summary": _scene_probe_readback_summary(readback),
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(scene_probe_created=created),
    }


def materialize_local_scene_choreography_probe(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    project = load_ymmp(base / SOURCE_NOD_HEAD_YMMP_PATH)
    probe = copy.deepcopy(project)
    target_path = base / LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH
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
    for segment in _scene_segment_plan():
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


def render_v4_sweep_observation_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Yukkuri Animation V4 Tempo Sweep Observation v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        "",
    ]
    _append_mapping(lines, "Source V4 Probe Access", payload.get("source_v4_probe_access"))
    _append_mapping(lines, "Normalized User Observation", payload.get("normalized_user_observation"))
    _append_mapping(lines, "Tempo Default Policy", payload.get("tempo_default_policy"))
    _append_mapping(lines, "Tempo Only Loop Exit", payload.get("tempo_only_loop_exit"))
    _append_mapping(lines, "Primitive Feasibility Judgment", payload.get("primitive_feasibility_judgment"))
    _append_mapping(lines, "Motion Coherence Warning", payload.get("motion_coherence_warning"))
    _append_mapping(
        lines,
        "Render Deferral",
        {
            "render_export_checked": payload.get("render_export_checked"),
            "render_export_required_now": payload.get("render_export_required_now"),
        },
    )
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This readback normalizes a user-side v4 preview observation only. It "
        "does not render, launch YMM4 from the agent, stage media, or accept "
        "production/public quality."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_scene_choreography_contract_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Yukkuri Animation Scene Choreography Contract v1",
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
    _append_mapping(lines, "Tempo Default Policy", payload.get("tempo_default_policy"))
    _append_mapping(lines, "Provisional Tempo Policy", payload.get("provisional_tempo_policy"))
    _append_mapping(lines, "Choreography Rules", payload.get("choreography_rules"))
    _append_rows(
        lines,
        "Scene Beat Integration Risks",
        ["risk_id", "status", "mitigation"],
        payload.get("scene_beat_integration_risks"),
    )
    _append_rows(
        lines,
        "Scene Beat Mapping",
        [
            "beat_id",
            "scene_function",
            "viewer_information_goal",
            "motion_reason",
            "primitive_used",
            "expression_reason",
            "active_motion_span",
            "hold_span",
            "forbidden_motion",
        ],
        payload.get("scene_beat_mapping"),
    )
    _append_mapping(lines, "V1 Scene Probe Plan", payload.get("v1_scene_probe_plan"))
    _append_mapping(lines, "Scene Probe Access", payload.get("scene_probe_access"))
    _append_mapping(lines, "Scene Probe Readback Summary", payload.get("scene_probe_readback_summary"))
    _append_mapping(lines, "Next Recommended Axis", payload.get("next_recommended_axis"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "The scene choreography probe is an ignored local diagnostic artifact. "
        "It is not rendered, not staged, not committed, and not production/public acceptance."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _scene_segment_plan() -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    for beat in SCENE_BEAT_MAPPING:
        active_span = int(beat["active_motion_span"])
        hold_span = int(beat["hold_span"])
        frame = int(beat["frame"])
        if active_span > 0:
            segments.append(
                _segment_from_beat(
                    beat,
                    segment_kind="active",
                    segment_frame=frame,
                    segment_length=active_span,
                    parent_x_values=list(beat["parent_x_values"]),
                    head_rotation_values=list(beat["head_rotation_values"]),
                    primitive_ids=list(beat["primitive_used"]),
                )
            )
            if hold_span > 0:
                segments.append(
                    _segment_from_beat(
                        beat,
                        segment_kind="hold",
                        segment_frame=frame + active_span,
                        segment_length=hold_span,
                        parent_x_values=[float(beat["parent_x_values"][-1])],
                        head_rotation_values=[0.0],
                        primitive_ids=["stable_hold"],
                    )
                )
        else:
            segments.append(
                _segment_from_beat(
                    beat,
                    segment_kind="hold",
                    segment_frame=frame,
                    segment_length=hold_span,
                    parent_x_values=list(beat["parent_x_values"]),
                    head_rotation_values=list(beat["head_rotation_values"]),
                    primitive_ids=list(beat["primitive_used"]),
                )
            )
    return segments


def _segment_from_beat(
    beat: dict[str, Any],
    *,
    segment_kind: str,
    segment_frame: int,
    segment_length: int,
    parent_x_values: list[float],
    head_rotation_values: list[float],
    primitive_ids: list[str],
) -> dict[str, Any]:
    beat_id = str(beat["beat_id"])
    segment_id = f"{beat_id}_{segment_kind}"
    return {
        **beat,
        "beat_id": segment_id,
        "source_scene_beat_id": beat_id,
        "segment_kind": segment_kind,
        "frame": segment_frame,
        "length": segment_length,
        "timing_range": f"{segment_frame / FPS:.2f}-{(segment_frame + segment_length) / FPS:.2f} sec",
        "primitive_ids": primitive_ids,
        "parent_x_values": parent_x_values,
        "head_rotation_values": head_rotation_values,
    }


def _scene_probe_readback(base: Path, access: dict[str, Any]) -> dict[str, Any]:
    target = base / LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH
    if not target.exists():
        return {
            "readback_status": "blocked",
            "reason": "local_scene_probe_missing",
            "target_exists": False,
        }
    data = load_ymmp(target)
    timeline = _first_timeline(data)
    items = _get_timeline_items(data)
    item_type_counts: dict[str, int] = {}
    for item in items:
        item_type_counts[_item_type(item)] = item_type_counts.get(_item_type(item), 0) + 1
    segment_readback = [_beat_readback(segment, items) for segment in _scene_segment_plan()]
    beat_readback = _scene_beat_readback(segment_readback)
    unexpected_item_types = sorted(
        item_type for item_type in item_type_counts if item_type not in {"GroupItem", "ImageItem"}
    )
    structural_pass = (
        timeline.get("Length") == SCENE_TIMELINE_LENGTH_FRAMES
        and item_type_counts.get("GroupItem") == 16
        and item_type_counts.get("ImageItem") == 16
        and not unexpected_item_types
        and all(row["status"] == "pass" for row in segment_readback)
        and all(row["status"] == "pass" for row in beat_readback)
        and _semantic_checks(beat_readback)["status"] == "pass"
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
        "scene_beat_readback": beat_readback,
        "semantic_checks": _semantic_checks(beat_readback),
        "source_ymmp_copy_basis": SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
        "git_check_ignore_result": _git_check_ignore(base, LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH),
        "local_probe_access_state": access["access_state"],
        "YMM4_launch_status": "not_launched",
        "render_status": "not_rendered",
        "audio_tts_status": "not_created",
    }


def _scene_beat_readback(segment_readback: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_segment = {row["beat_id"]: row for row in segment_readback}
    rows: list[dict[str, Any]] = []
    for beat in SCENE_BEAT_MAPPING:
        segments = [
            segment
            for segment in _scene_segment_plan()
            if segment["source_scene_beat_id"] == beat["beat_id"]
        ]
        reads = [by_segment[segment["beat_id"]] for segment in segments]
        parent_values = [
            value
            for row in reads
            for value in row.get("parent_x_values", [])
        ]
        head_values = [
            value
            for row in reads
            for value in row.get("head_rotation_values", [])
        ]
        expression_paths = sorted(
            {
                row.get("face_file_path")
                for row in reads
                if isinstance(row.get("face_file_path"), str)
            }
        )
        status = "pass" if all(row["status"] == "pass" for row in reads) else "blocked"
        rows.append(
            {
                "scene_id": SCENE_ID,
                "beat_id": beat["beat_id"],
                "scene_function": beat["scene_function"],
                "frame": beat["frame"],
                "length": beat["length"],
                "timing_range": f"{beat['frame'] / FPS:.2f}-{(beat['frame'] + beat['length']) / FPS:.2f} sec",
                "active_motion_span": beat["active_motion_span"],
                "hold_span": beat["hold_span"],
                "primitive_used": beat["primitive_used"],
                "expression": beat["expression"],
                "expression_reason": beat["expression_reason"],
                "motion_reason": beat["motion_reason"],
                "segment_count": len(reads),
                "parent_x_values": parent_values,
                "head_rotation_values": head_values,
                "face_file_paths": expression_paths,
                "anchor_continuity": "pass" if parent_values and parent_values[0] == -96.0 and parent_values[-1] == -96.0 else "blocked",
                "status": status,
            }
        )
    return rows


def _semantic_checks(beat_readback: list[dict[str, Any]]) -> dict[str, Any]:
    nod_beats = [
        row["beat_id"]
        for row in beat_readback
        if "head_nod" in row.get("primitive_used", [])
        and any(abs(value) > 0 for value in row.get("head_rotation_values", []))
    ]
    moving_beats = [
        row["beat_id"]
        for row in beat_readback
        if _value_range(row.get("parent_x_values", [])) > 0
    ]
    expression_change_beats = [
        row["beat_id"]
        for row in beat_readback
        if "expression_swap" in row.get("primitive_used", [])
    ]
    checks = {
        "one_meaningful_nod": nod_beats == ["beat_c_one_short_ack_nod"],
        "one_small_intentional_move": moving_beats == ["beat_e_one_small_intentional_nudge"],
        "mechanical_expression_cycle_avoided": expression_change_beats == [
            "beat_b_question_reaction_cue",
            "beat_d_reasoned_expression_shift",
            "beat_f_stable_explanation_pose",
        ],
        "all_beat_boundaries_anchor_x_minus_96": all(
            row.get("anchor_continuity") == "pass" for row in beat_readback
        ),
        "active_motion_shorter_than_hold_when_motion_exists": all(
            int(row["active_motion_span"]) == 0
            or int(row["active_motion_span"]) < int(row["hold_span"])
            for row in beat_readback
        ),
    }
    return {
        "status": "pass" if all(checks.values()) else "blocked",
        "checks": checks,
        "nod_beats": nod_beats,
        "moving_beats": moving_beats,
        "expression_change_beats": expression_change_beats,
    }


def _scene_probe_readback_summary(readback: dict[str, Any]) -> dict[str, Any]:
    if readback.get("readback_status") != "structural_pass":
        return {
            "status": readback.get("readback_status"),
            "reason": readback.get("reason", "scene probe readback blocked"),
        }
    return {
        "status": "structural_pass",
        "timeline_length_frames": readback["timeline"]["length_frames"],
        "timeline_length_sec": readback["timeline"]["length_sec"],
        "item_type_counts": readback["timeline"]["item_type_counts"],
        "segment_count": readback["segment_count"],
        "semantic_status": readback["semantic_checks"]["status"],
    }


def _scene_beat_contract_rows() -> list[dict[str, Any]]:
    required_keys = [
        "scene_id",
        "scene_function",
        "beat_id",
        "viewer_information_goal",
        "character_state_before",
        "motion_reason",
        "primitive_used",
        "expression_reason",
        "facing_policy",
        "anchor_policy",
        "active_motion_span",
        "hold_span",
        "transition_policy",
        "forbidden_motion",
        "fallback_if_primitive_unavailable",
    ]
    return [
        {key: beat[key] for key in required_keys}
        for beat in SCENE_BEAT_MAPPING
    ]


def _scene_probe_plan() -> dict[str, Any]:
    return {
        "scene_id": SCENE_ID,
        "duration_frames": SCENE_TIMELINE_LENGTH_FRAMES,
        "duration_sec_at_60fps": round(SCENE_TIMELINE_LENGTH_FRAMES / FPS, 6),
        "beat_count": len(SCENE_BEAT_MAPPING),
        "structure": [
            "Beat A: neutral listening pose",
            "Beat B: question/reaction cue",
            "Beat C: one short nod or acknowledgement",
            "Beat D: expression changes for reason",
            "Beat E: one small intentional nudge",
            "Beat F: return to stable explanation pose",
        ],
        "demonstrates": [
            "one meaningful nod",
            "one reasoned expression change sequence",
            "one small intentional move",
            "0.75s default active timing in a scene-beat structure",
            "stable anchor continuity",
            "no mechanical expression cycling",
            "no meaningless forward/back drift",
            "no production claim",
        ],
        "local_probe_path": LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH.as_posix(),
    }


def _next_axis(*, scene_created: bool, probe_payload: dict[str, Any]) -> str:
    if not scene_created:
        return FALLBACK_AXIS_SCENE_IMPLEMENTATION
    checks = probe_payload.get("scene_probe_readback", {}).get("semantic_checks", {}).get("checks", {})
    if checks.get("mechanical_expression_cycle_avoided") is False:
        return EXPRESSION_BINDING_AXIS
    if checks.get("one_small_intentional_move") is False:
        return BODY_FACING_FIX_AXIS
    if probe_payload.get("scene_probe_readback", {}).get("timeline", {}).get("length_frames") != SCENE_TIMELINE_LENGTH_FRAMES:
        return TIMING_STRUCTURE_AUDIT_AXIS
    return NEXT_AXIS_SCENE_PREVIEW


def _next_axis_reason(*, scene_created: bool, probe_payload: dict[str, Any]) -> str:
    if scene_created:
        return (
            "the v4 sweep selected 0.75s / 45 frames as the default tempo; "
            "the next proof should apply 0.5s, 0.75s, and 1.0s by scene-beat "
            "function instead of running another primitive-only tempo sweep"
        )
    return probe_payload.get("scene_probe_readback_summary", {}).get("reason", "scene probe materialization blocked")


def _boundaries(*, scene_probe_created: bool) -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "dense_script_modified": False,
        "local_ignored_scene_probe_created": scene_probe_created,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "tempo_only_loop_exited", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "default_tempo_policy_selected", "status": "0.75s / 45 frames"},
        {"gate": "scene_dependent_variants_preserved", "status": "0.5s and 1.0s"},
        {"gate": "scene_beat_integration_replaces_primitive_loop", "status": True},
        {"gate": "next_concrete_animation_milestone_named", "status": next_axis},
    ]


def main() -> int:
    write_default_newsroom_yukkuri_animation_scene_choreography_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
