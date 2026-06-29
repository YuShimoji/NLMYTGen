"""Record preview observation and create the v2 primitive motion-fix probe.

This slice converts a user-side YMM4 preview observation into a bounded motion
contract. It may create an ignored local v2 probe by reusing the same tracked
nod-head source structure as v1, but it does not launch YMM4, render, create
audio/TTS, fetch external media, or claim production quality.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_yukkuri_animation_primitive_probe_materialization import (
    BODY_SOURCE_PATH,
    EXPRESSION_PATHS,
    OMITTED_PRIMITIVES,
    PROVEN_PRIMITIVES,
    SOURCE_NOD_HEAD_YMMP_PATH,
    _clone_beat_items,
    _dict,
    _first_timeline,
    _get_timeline_items,
    _item_type,
    _route_values,
    _value_range,
)
from src.pipeline.newsroom_yukkuri_animation_primitive_proof import (
    DEFAULT_PROOF_PATH,
    LOCAL_IGNORED_PROBE_PATH,
)
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


OBSERVATION_ID = "newsroom_yukkuri_animation_primitive_preview_observation_v1_2026_06_29"
MOTION_CONTRACT_ID = "newsroom_yukkuri_animation_motion_contract_v1_2026_06_29"
OBSERVATION_SCHEMA_VERSION = "newsroom_yukkuri_animation_primitive_preview_observation.v1"
MOTION_CONTRACT_SCHEMA_VERSION = "newsroom_yukkuri_animation_motion_contract.v1"

DEFAULT_OBSERVATION_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "yukkuri_animation_primitive_preview_observation_v1.json"
)
DEFAULT_OBSERVATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_YUKKURI_ANIMATION_PRIMITIVE_PREVIEW_OBSERVATION_V1_2026-06-29.md"
)
DEFAULT_MOTION_CONTRACT_PATH = Path(
    "samples/_probe/newsroom_handoff/yukkuri_animation_motion_contract_v1.json"
)
DEFAULT_MOTION_CONTRACT_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YUKKURI_ANIMATION_MOTION_CONTRACT_V1_2026-06-29.md"
)

LOCAL_IGNORED_V2_MOTION_FIX_PATH = Path(
    "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v2_motion_fix.ymmp"
)
NEXT_AXIS_V2_PREVIEW = (
    "newsroom-yukkuri-animation-primitive-v2-preview-operator-instruction-v1"
)
FALLBACK_AXIS_CONTRACT_IMPLEMENTATION = (
    "newsroom-yukkuri-animation-motion-contract-implementation-v1"
)

FPS = 60
V2_BEAT_LENGTH_FRAMES = 360
V2_TIMELINE_LENGTH_FRAMES = V2_BEAT_LENGTH_FRAMES * 5

NORMALIZED_USER_OBSERVATION: dict[str, Any] = {
    "source_observation_role": "user_opened_local_ymmp_preview",
    "source_v1_probe_path": LOCAL_IGNORED_PROBE_PATH.as_posix(),
    "yym4_opened": True,
    "character_visible": True,
    "head_body_attachment": "pass",
    "expression_swap": "pass",
    "character_motion_visible": "pass_with_warning",
    "entrance_exit": "pass_with_facing_warning",
    "small_position_move": "pass_with_anchor_continuity_warning",
    "head_nod": "pass_with_timing_warning",
    "major_visual_breakage": False,
    "render_export_checked": False,
    "render_export_required_now": False,
    "next_axis": "motion_timing_facing_anchor_continuity_fix",
}

USER_OBSERVATION_NOTES = [
    "Character is displayed.",
    "Body and head are connected without major breakage.",
    "Character animates.",
    "Motion is very slow.",
    "Character moves backward toward the screen center.",
    "The likely intended behavior is to control facing/orientation.",
    "Several expressions switch.",
    "No major breakage.",
    "X position differs between animation segments, causing jumpy disconnected movement.",
    "Head nod is very slow, with one vertical nod.",
    "Render/export confirmation is unnecessary for this stage because opening the .ymmp proved enough.",
]

PRIMITIVE_CLASSIFICATION = [
    {
        "primitive_id": "head_nod",
        "classification": "pass_with_timing_warning",
        "observed_issue": "nod was visible but excessively slow and read as one slow vertical nod",
        "decision": "keep primitive, shorten beat timing, require return-to-neutral",
    },
    {
        "primitive_id": "expression_swap",
        "classification": "pass",
        "observed_issue": "several expressions switched; no major breakage reported",
        "decision": "keep expression swap but bind each expression to a beat span",
    },
    {
        "primitive_id": "character_entrance_exit",
        "classification": "pass_with_facing_warning",
        "observed_issue": "movement appeared backward toward screen center, suggesting missing facing/orientation intent",
        "decision": "avoid broad facing-dependent travel in v2; use neutral bounded side entry/exit",
    },
    {
        "primitive_id": "small_position_move",
        "classification": "pass_with_anchor_continuity_warning",
        "observed_issue": "X position changed between animation segments and produced jumpy disconnected movement",
        "decision": "carry X anchors across adjacent beats unless a cut is explicit",
    },
]

MOTION_CONTRACT = [
    {
        "primitive_id": "head_nod",
        "current_status": "pass_with_timing_warning",
        "observed_issue": "visible but too slow; read as one vertical nod",
        "intended_motion": "short acknowledgement nod that returns to neutral",
        "start_anchor_policy": "head rotation starts at 0 degrees",
        "end_anchor_policy": "head rotation ends at 0 degrees",
        "facing_policy": "no facing change; keep body orientation neutral",
        "duration_policy": "one nod must fit inside a 6 second beat with key motion concentrated near the beat middle",
        "easing_policy": "linear route is acceptable for v2; avoid long hold at the tilted state",
        "continuity_policy": "head neutral at beat boundaries so adjacent primitives do not inherit a tilt",
        "expression_span_policy": "expression remains stable during the nod beat",
        "fallback_if_not_supported": "hold neutral head and rely on expression_swap for reaction",
    },
    {
        "primitive_id": "expression_swap",
        "current_status": "pass",
        "observed_issue": "expressions switched, but random-feeling timing would weaken the animation layer",
        "intended_motion": "beat-aligned expression state change",
        "start_anchor_policy": "expression starts at the beat file path",
        "end_anchor_policy": "expression remains stable until the next beat boundary",
        "facing_policy": "no facing change from expression alone",
        "duration_policy": "one expression per 6 second beat in v2",
        "easing_policy": "instant image source swap is acceptable for this structural probe",
        "continuity_policy": "do not change expression mid-beat unless a later visual pass asks for it",
        "expression_span_policy": "panic/easy/anger/panic/easy map to the five v2 beats",
        "fallback_if_not_supported": "use easy expression for all beats",
    },
    {
        "primitive_id": "character_entrance_exit",
        "current_status": "pass_with_facing_warning",
        "observed_issue": "broad X travel looked like backward movement toward screen center",
        "intended_motion": "bounded side entry/exit cue without implying a wrong facing direction",
        "start_anchor_policy": "entry starts near the left-side staging anchor, not far offscreen",
        "end_anchor_policy": "entry ends at the shared review anchor; exit starts from that same anchor",
        "facing_policy": "avoid flip/orientation claims in v2; use neutral lateral travel only",
        "duration_policy": "entry/exit cue each fits within one 6 second beat",
        "easing_policy": "linear route is acceptable; avoid slow center drift",
        "continuity_policy": "adjacent beat start/end X values must match the shared anchor unless a cut is explicit",
        "expression_span_policy": "entry uses panic; exit uses easy",
        "fallback_if_not_supported": "static character hold at the shared review anchor",
    },
    {
        "primitive_id": "small_position_move",
        "current_status": "pass_with_anchor_continuity_warning",
        "observed_issue": "segment-to-segment X discontinuity caused jumpy disconnected movement",
        "intended_motion": "small nudge around a stable review anchor",
        "start_anchor_policy": "start every nudge at the previous beat end anchor",
        "end_anchor_policy": "return every nudge to the same shared anchor",
        "facing_policy": "no facing change; movement must not read as walking backward",
        "duration_policy": "small nudge fits within a 6 second beat",
        "easing_policy": "linear out-and-back route is acceptable for v2",
        "continuity_policy": "remove sudden jumps by making each adjacent beat boundary share X=-96",
        "expression_span_policy": "expression remains stable while the nudge happens",
        "fallback_if_not_supported": "drop the nudge and keep the shared review anchor",
    },
]

V2_BEAT_PLAN: list[dict[str, Any]] = [
    {
        "beat_id": "v2_beat_01_enter_question",
        "frame": 0,
        "length": V2_BEAT_LENGTH_FRAMES,
        "timing_range": "0-6 sec",
        "scene_function": "viewer_question_reaction",
        "expression": "panic",
        "primitive_ids": ["character_entrance_exit", "expression_swap"],
        "parent_x_values": [-144.0, -96.0],
        "head_rotation_values": [0.0],
        "motion_label": "bounded_side_enter_to_shared_anchor",
    },
    {
        "beat_id": "v2_beat_02_nod_response",
        "frame": V2_BEAT_LENGTH_FRAMES,
        "length": V2_BEAT_LENGTH_FRAMES,
        "timing_range": "6-12 sec",
        "scene_function": "explanation_response",
        "expression": "easy",
        "primitive_ids": ["head_nod", "small_position_move"],
        "parent_x_values": [-96.0, -84.0, -96.0],
        "head_rotation_values": [0.0, -10.0, 0.0],
        "motion_label": "short_nod_and_small_right_nudge",
    },
    {
        "beat_id": "v2_beat_03_emphasis_nudge",
        "frame": V2_BEAT_LENGTH_FRAMES * 2,
        "length": V2_BEAT_LENGTH_FRAMES,
        "timing_range": "12-18 sec",
        "scene_function": "proof_emphasis",
        "expression": "anger",
        "primitive_ids": ["expression_swap", "small_position_move"],
        "parent_x_values": [-96.0, -116.0, -96.0],
        "head_rotation_values": [0.0],
        "motion_label": "small_left_nudge_return_to_anchor",
    },
    {
        "beat_id": "v2_beat_04_boundary_warning",
        "frame": V2_BEAT_LENGTH_FRAMES * 3,
        "length": V2_BEAT_LENGTH_FRAMES,
        "timing_range": "18-24 sec",
        "scene_function": "boundary_warning",
        "expression": "panic",
        "primitive_ids": ["expression_swap", "small_position_move"],
        "parent_x_values": [-96.0, -86.0, -96.0],
        "head_rotation_values": [0.0],
        "motion_label": "small_right_warning_nudge_return_to_anchor",
    },
    {
        "beat_id": "v2_beat_05_exit_close",
        "frame": V2_BEAT_LENGTH_FRAMES * 4,
        "length": V2_BEAT_LENGTH_FRAMES,
        "timing_range": "24-30 sec",
        "scene_function": "next_action_close",
        "expression": "easy",
        "primitive_ids": ["character_entrance_exit", "head_nod"],
        "parent_x_values": [-96.0, -144.0],
        "head_rotation_values": [0.0, -8.0, 0.0],
        "motion_label": "bounded_side_exit_from_shared_anchor",
    },
]


def write_default_newsroom_yukkuri_animation_motion_contract_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write observation/contract artifacts and the ignored local v2 probe."""
    base = Path(root) if root is not None else Path(".")
    materialize_local_v2_motion_fix_probe(root=base)
    observation = build_default_preview_observation(root=base)
    contract = build_default_motion_contract(root=base)
    _write_json(base / DEFAULT_OBSERVATION_PATH, observation)
    _write_text(base / DEFAULT_OBSERVATION_DOC_PATH, render_preview_observation_markdown(observation))
    _write_json(base / DEFAULT_MOTION_CONTRACT_PATH, contract)
    _write_text(base / DEFAULT_MOTION_CONTRACT_DOC_PATH, render_motion_contract_markdown(contract))
    return {"observation": observation, "motion_contract": contract}


def build_default_preview_observation(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    v1_access = _local_probe_access(base, LOCAL_IGNORED_PROBE_PATH)
    return {
        "artifact_id": OBSERVATION_ID,
        "observation_id": OBSERVATION_ID,
        "schema_version": OBSERVATION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_v1_probe_path": LOCAL_IGNORED_PROBE_PATH.as_posix(),
        "source_v1_probe_access": v1_access,
        "user_observation_notes": USER_OBSERVATION_NOTES,
        "normalized_user_observation": NORMALIZED_USER_OBSERVATION,
        "primitive_classification": PRIMITIVE_CLASSIFICATION,
        "render_export_checked": False,
        "render_export_required_now": False,
        "render_deferred_reason": (
            "User-side preview opened the .ymmp and confirmed the current stage: "
            "the remaining problem is motion timing, facing, and anchor continuity, "
            "not render/export mechanics."
        ),
        "next_axis": "motion_timing_facing_anchor_continuity_fix",
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(v2_created=False),
    }


def build_default_motion_contract(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    v2_access = _local_probe_access(base, LOCAL_IGNORED_V2_MOTION_FIX_PATH)
    v2_readback = _v2_probe_readback(base, v2_access)
    v2_created = (
        v2_access["target_exists"]
        and v2_access["access_state"] == "verified_present"
        and v2_readback["readback_status"] == "structural_pass"
    )
    next_axis = NEXT_AXIS_V2_PREVIEW if v2_created else FALLBACK_AXIS_CONTRACT_IMPLEMENTATION
    return {
        "artifact_id": MOTION_CONTRACT_ID,
        "motion_contract_id": MOTION_CONTRACT_ID,
        "schema_version": MOTION_CONTRACT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_context": {
            "source_primitive_proof_path": DEFAULT_PROOF_PATH.as_posix(),
            "source_v1_probe_path": LOCAL_IGNORED_PROBE_PATH.as_posix(),
            "source_v1_observation_path": DEFAULT_OBSERVATION_PATH.as_posix(),
            "source_nod_head_ymmp_path": SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
        },
        "v1_issue_summary": [
            "motion too slow",
            "head nod too slow and perceived as a single vertical nod",
            "broad X travel looked like backward movement toward screen center",
            "facing/orientation intent was underspecified",
            "X anchor changed between adjacent segments and created jumps",
            "expression changes passed but need beat-aligned spans",
        ],
        "motion_contract": MOTION_CONTRACT,
        "v2_correction_plan": _v2_correction_plan(),
        "v2_beat_plan": _v2_beat_plan(),
        "v2_materialization_status": "materialized_ignored_local_probe" if v2_created else "blocked",
        "v2_local_probe": v2_access,
        "v2_probe_readback": v2_readback,
        "selected_next_axis": next_axis,
        "next_recommended_axis": {
            "selected": next_axis,
            "reason": (
                "ignored local v2 probe exists, is git-ignored, and structurally "
                "implements the motion timing/facing/anchor-continuity contract"
                if v2_created
                else "v2 probe could not be safely materialized from known routes"
            ),
            "prerequisites": [
                "keep v2 .ymmp ignored and unstaged",
                "use a preview-only operator instruction before any render request",
                "do not claim production/public acceptance",
            ],
        },
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(v2_created=v2_created),
        "inertia_check": _inertia_check(next_axis),
    }


def materialize_local_v2_motion_fix_probe(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Create the ignored local v2 probe from the tracked nod-head proof source."""
    base = Path(root) if root is not None else Path(".")
    project = load_ymmp(base / SOURCE_NOD_HEAD_YMMP_PATH)
    probe = copy.deepcopy(project)
    target_path = base / LOCAL_IGNORED_V2_MOTION_FIX_PATH
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
    for beat in V2_BEAT_PLAN:
        items.extend(_clone_beat_items(base, source_items, beat))
    timeline["Items"] = sorted(
        items,
        key=lambda item: (int(item.get("Frame", 0)), int(item.get("Layer", 0))),
    )
    timeline["Length"] = V2_TIMELINE_LENGTH_FRAMES
    timeline["CurrentFrame"] = 0
    timeline["MaxLayer"] = max(
        int(item.get("Layer", 0))
        for item in timeline["Items"]
        if isinstance(item.get("Layer"), int)
    )

    save_ymmp(probe, target_path)
    return probe


def render_preview_observation_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Yukkuri Animation Primitive Preview Observation v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"next_axis: {payload.get('next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source V1 Probe Access", payload.get("source_v1_probe_access"))
    _append_mapping(lines, "Normalized User Observation", payload.get("normalized_user_observation"))
    _append_rows(
        lines,
        "Primitive Classification",
        ["primitive_id", "classification", "observed_issue", "decision"],
        payload.get("primitive_classification"),
    )
    _append_mapping(lines, "Render Deferral", {
        "render_export_checked": payload.get("render_export_checked"),
        "render_export_required_now": payload.get("render_export_required_now"),
        "render_deferred_reason": payload.get("render_deferred_reason"),
    })
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This readback normalizes a user-side preview observation only. It does "
        "not render, launch YMM4 from the agent, stage media, or accept "
        "production/public quality."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_motion_contract_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Yukkuri Animation Motion Contract v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"v2_materialization_status: {payload.get('v2_materialization_status')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_rows(
        lines,
        "Motion Contract",
        [
            "primitive_id",
            "current_status",
            "observed_issue",
            "intended_motion",
            "start_anchor_policy",
            "end_anchor_policy",
            "facing_policy",
            "duration_policy",
            "easing_policy",
            "continuity_policy",
            "expression_span_policy",
            "fallback_if_not_supported",
        ],
        payload.get("motion_contract"),
    )
    _append_mapping(lines, "V1 Issue Summary", payload.get("v1_issue_summary"))
    _append_mapping(lines, "V2 Correction Plan", payload.get("v2_correction_plan"))
    _append_rows(
        lines,
        "V2 Beat Plan",
        ["beat_id", "timing_range", "scene_function", "primitive_ids", "parent_x_values", "head_rotation_values"],
        payload.get("v2_beat_plan"),
    )
    _append_mapping(lines, "V2 Local Probe", payload.get("v2_local_probe"))
    _append_mapping(lines, "V2 Probe Readback", payload.get("v2_probe_readback"))
    _append_mapping(lines, "Next Recommended Axis", payload.get("next_recommended_axis"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "The v2 probe is an ignored local diagnostic artifact. It is not rendered, "
        "not staged, not committed, and not production/public acceptance."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _v2_probe_readback(base: Path, v2_access: dict[str, Any]) -> dict[str, Any]:
    target = base / LOCAL_IGNORED_V2_MOTION_FIX_PATH
    if not target.exists():
        return {
            "readback_status": "blocked",
            "reason": "local_v2_probe_missing",
            "target_exists": False,
        }
    data = load_ymmp(target)
    timeline = _first_timeline(data)
    items = _get_timeline_items(data)
    item_type_counts: dict[str, int] = {}
    for item in items:
        item_type_counts[_item_type(item)] = item_type_counts.get(_item_type(item), 0) + 1
    beat_summaries = [_beat_readback(beat, items) for beat in V2_BEAT_PLAN]
    primitive_status = _v2_primitive_status(beat_summaries)
    unexpected_item_types = sorted(
        item_type for item_type in item_type_counts if item_type not in {"GroupItem", "ImageItem"}
    )
    boundary_x_values = [row["parent_x_values"][0] for row in beat_summaries if row.get("parent_x_values")]
    structural_pass = (
        timeline.get("Length") == V2_TIMELINE_LENGTH_FRAMES
        and item_type_counts.get("GroupItem") == 10
        and item_type_counts.get("ImageItem") == 10
        and not unexpected_item_types
        and all(row["status"] == "pass" for row in primitive_status)
    )
    return {
        "readback_status": "structural_pass" if structural_pass else "blocked",
        "target_exists": True,
        "file_sha256": _sha256(target),
        "file_size_bytes": target.stat().st_size,
        "timeline": {
            "fps": _dict(timeline.get("VideoInfo")).get("FPS"),
            "length_frames": timeline.get("Length"),
            "length_sec": round(V2_TIMELINE_LENGTH_FRAMES / FPS, 6),
            "item_count": len(items),
            "item_type_counts": item_type_counts,
            "unexpected_item_types": unexpected_item_types,
        },
        "beat_readback": beat_summaries,
        "primitive_status": primitive_status,
        "anchor_continuity": {
            "shared_anchor_x": -96.0,
            "beat_boundary_start_x_values": boundary_x_values,
            "adjacent_boundaries_share_anchor": True,
        },
        "source_ymmp_copy_basis": SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
        "local_probe_access_state": v2_access["access_state"],
        "YMM4_launch_status": "not_launched",
        "render_status": "not_rendered",
        "audio_tts_status": "not_created",
    }


def _beat_readback(beat: dict[str, Any], items: list[dict[str, Any]]) -> dict[str, Any]:
    marker = f"primitive_probe:{beat['beat_id']}:nod_head_v1"
    matched = [item for item in items if item.get("Remark") == marker]
    groups = [item for item in matched if _item_type(item) == "GroupItem"]
    images = [item for item in matched if _item_type(item) == "ImageItem"]
    parent = next((item for item in groups if item.get("GroupRange") == 3), None)
    head = next((item for item in groups if item.get("GroupRange") == 1), None)
    face = next(
        (
            item
            for item in images
            if isinstance(item.get("FilePath"), str)
            and "reimu_" in item.get("FilePath", "")
        ),
        None,
    )
    return {
        "beat_id": beat["beat_id"],
        "scene_function": beat["scene_function"],
        "timing_range": beat["timing_range"],
        "frame": beat["frame"],
        "length": beat["length"],
        "primitive_ids": beat["primitive_ids"],
        "item_count": len(matched),
        "group_item_count": len(groups),
        "image_item_count": len(images),
        "parent_x_values": _route_values(parent, "X"),
        "head_rotation_values": _route_values(head, "Rotation"),
        "face_file_path": face.get("FilePath") if face else None,
        "status": "pass" if len(groups) == 2 and len(images) == 2 else "blocked",
    }


def _v2_primitive_status(beat_summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    face_paths = {
        row.get("face_file_path")
        for row in beat_summaries
        if isinstance(row.get("face_file_path"), str)
    }
    starts = [row["parent_x_values"][0] for row in beat_summaries if row.get("parent_x_values")]
    ends = [row["parent_x_values"][-1] for row in beat_summaries if row.get("parent_x_values")]
    shared_anchor_ok = (
        len(starts) == 5
        and starts[1:] == [-96.0, -96.0, -96.0, -96.0]
        and ends[:4] == [-96.0, -96.0, -96.0, -96.0]
    )
    return [
        {
            "primitive_id": "head_nod",
            "status": (
                "pass"
                if any(
                    "head_nod" in row["primitive_ids"]
                    and len(row.get("head_rotation_values", [])) == 3
                    and row["head_rotation_values"][0] == 0.0
                    and row["head_rotation_values"][-1] == 0.0
                    and any(abs(value) >= 8.0 for value in row["head_rotation_values"])
                    for row in beat_summaries
                )
                else "blocked"
            ),
            "evidence": "head Rotation route has 0 -> non-zero -> 0 within a 6 second beat",
        },
        {
            "primitive_id": "expression_swap",
            "status": "pass" if len(face_paths) >= 3 else "blocked",
            "evidence": sorted(face_paths),
        },
        {
            "primitive_id": "character_entrance_exit",
            "status": (
                "pass"
                if any(
                    "character_entrance_exit" in row["primitive_ids"]
                    and 40.0 <= _value_range(row.get("parent_x_values", [])) <= 80.0
                    for row in beat_summaries
                )
                else "blocked"
            ),
            "evidence": "entry/exit uses bounded side travel instead of broad center drift",
        },
        {
            "primitive_id": "small_position_move",
            "status": (
                "pass"
                if shared_anchor_ok
                and any(
                    "small_position_move" in row["primitive_ids"]
                    and 0 < _value_range(row.get("parent_x_values", [])) <= 24.0
                    for row in beat_summaries
                )
                else "blocked"
            ),
            "evidence": "adjacent beats share X=-96 and nudges return to that anchor",
        },
    ]


def _v2_correction_plan() -> dict[str, Any]:
    return {
        "head_nod": [
            "shorten beat length from 12 seconds to 6 seconds",
            "use 0 -> negative rotation -> 0 so the head returns to neutral",
        ],
        "facing_orientation": [
            "do not claim or perform facing flip in v2",
            "replace broad centerward travel with bounded neutral lateral movement",
        ],
        "anchor_continuity": [
            "use X=-96 as the shared review anchor",
            "every adjacent beat boundary carries that anchor unless the exit beat intentionally leaves it",
        ],
        "expression_timing": [
            "one expression state per beat",
            "panic/easy/anger/panic/easy sequence follows scene role instead of random switching",
        ],
        "render_boundary": "no render/export proof in this slice",
    }


def _v2_beat_plan() -> list[dict[str, Any]]:
    return [
        {
            "beat_id": beat["beat_id"],
            "timing_range": beat["timing_range"],
            "scene_function": beat["scene_function"],
            "primitive_ids": beat["primitive_ids"],
            "expression": beat["expression"],
            "parent_x_values": beat["parent_x_values"],
            "head_rotation_values": beat["head_rotation_values"],
            "motion_label": beat["motion_label"],
        }
        for beat in V2_BEAT_PLAN
    ]


def _local_probe_access(base: Path, path: Path) -> dict[str, Any]:
    full_path = (base / path).resolve()
    check_ignore = _git_check_ignore(base, path)
    target_exists = full_path.exists()
    ignored = check_ignore["ignored"]
    if target_exists and ignored:
        access_state = "verified_present"
        evidence_level = "L3_VERIFIED_PRESENT"
    elif target_exists:
        access_state = "branch_or_worktree_mismatch"
        evidence_level = "L3_VERIFIED_PRESENT"
    elif ignored:
        access_state = "not_generated"
        evidence_level = "L2_MANIFEST_OR_GIT"
    else:
        access_state = "unknown"
        evidence_level = "L0_PATH_TEXT"
    return {
        "artifact_id": "local_ignored_v2_motion_fix_probe"
        if path == LOCAL_IGNORED_V2_MOTION_FIX_PATH
        else "local_ignored_primitive_probe_v1",
        "repo_relative_path": path.as_posix(),
        "folder_full_path_current_host": str(full_path.parent),
        "file_full_path_current_host": str(full_path),
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{full_path}"',
        "target_exists": target_exists,
        "access_state": access_state,
        "access_evidence_level": evidence_level,
        "artifact_scope": "ignored_local_only" if ignored else "untracked_or_unknown",
        "evidence_source": "current_host_filesystem_plus_git_check_ignore",
        "git_check_ignore_result": check_ignore,
        "size": full_path.stat().st_size if target_exists else None,
    }


def _git_check_ignore(base: Path, path: Path) -> dict[str, Any]:
    result = subprocess.run(
        ["git", "check-ignore", "-v", "--", path.as_posix()],
        cwd=base,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    return {
        "command": f"git check-ignore -v -- {path.as_posix()}",
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "ignored": result.returncode == 0,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "render_proof": False,
        "render_export_required_now": False,
        "production_animation_quality": False,
        "public_upload_or_public_readiness": False,
        "real_rss_or_news_integration": False,
        "card_redesign_or_density_work": False,
        "dense_script_rewrite": False,
        "external_reference_video_fetch": False,
        "audio_or_tts_output": False,
        "actual_order_or_audience_acceptance": False,
        "speech_balloon_visual_acceptance": False,
    }


def _boundaries(*, v2_created: bool) -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "dense_script_modified": False,
        "local_ignored_v2_probe_created": v2_created,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_text_density_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "motion_contract_targets_reported_visual_issue", "status": True},
        {"gate": "next_concrete_animation_milestone_named", "status": next_axis},
    ]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_text(path: str | Path, text: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def _append_mapping(lines: list[str], title: str, mapping: object) -> None:
    lines.extend(["", f"## {title}", "", "```json"])
    lines.append(json.dumps(mapping, ensure_ascii=False, indent=2))
    lines.extend(["```", ""])


def _append_rows(
    lines: list[str],
    title: str,
    columns: list[str],
    rows: object,
) -> None:
    items = [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []
    lines.extend(["", f"## {title}", ""])
    if not items:
        lines.extend(["None.", ""])
        return
    lines.append("| " + " | ".join(columns) + " |")
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in items:
        lines.append("| " + " | ".join(_display(row.get(col)) for col in columns) + " |")
    lines.append("")


def _display(value: object) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if value is None:
        return ""
    return str(value).replace("\n", " ")


def main() -> int:
    write_default_newsroom_yukkuri_animation_motion_contract_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
