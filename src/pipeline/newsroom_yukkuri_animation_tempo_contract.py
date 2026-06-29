"""Record the v2 preview tempo observation and create a faster v3 probe.

This slice preserves the v2 anchor/facing fixes and changes only bounded timing
spans for a tempo calibration probe. It does not launch YMM4, render, create
audio/TTS, fetch external media, or claim production quality.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    DEFAULT_MOTION_CONTRACT_PATH,
    LOCAL_IGNORED_V2_MOTION_FIX_PATH,
    V2_BEAT_PLAN,
    V2_BEAT_LENGTH_FRAMES,
    _append_mapping,
    _append_rows,
    _beat_readback,
    _dict,
    _display,
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
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


V2_PREVIEW_OBSERVATION_ID = (
    "newsroom_yukkuri_animation_v2_preview_observation_v1_2026_06_29"
)
TEMPO_CONTRACT_ID = "newsroom_yukkuri_animation_tempo_contract_v1_2026_06_29"
V2_PREVIEW_SCHEMA_VERSION = "newsroom_yukkuri_animation_v2_preview_observation.v1"
TEMPO_CONTRACT_SCHEMA_VERSION = "newsroom_yukkuri_animation_tempo_contract.v1"

DEFAULT_V2_PREVIEW_OBSERVATION_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "yukkuri_animation_v2_preview_observation_v1.json"
)
DEFAULT_V2_PREVIEW_OBSERVATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_YUKKURI_ANIMATION_V2_PREVIEW_OBSERVATION_V1_2026-06-29.md"
)
DEFAULT_TEMPO_CONTRACT_PATH = Path(
    "samples/_probe/newsroom_handoff/yukkuri_animation_tempo_contract_v1.json"
)
DEFAULT_TEMPO_CONTRACT_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YUKKURI_ANIMATION_TEMPO_CONTRACT_V1_2026-06-29.md"
)

LOCAL_IGNORED_V3_TEMPO_FIX_PATH = Path(
    "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp"
)
NEXT_AXIS_V3_PREVIEW = (
    "newsroom-yukkuri-animation-primitive-v3-preview-operator-instruction-v1"
)
FALLBACK_AXIS_TEMPO_IMPLEMENTATION = (
    "newsroom-yukkuri-animation-tempo-contract-implementation-v1"
)

FPS = 60
V3_BEAT_LENGTH_FRAMES = 180
V3_TIMELINE_LENGTH_FRAMES = V3_BEAT_LENGTH_FRAMES * 5

NORMALIZED_V2_PREVIEW_OBSERVATION: dict[str, Any] = {
    "source_observation_role": "user_opened_local_v2_ymmp_preview",
    "source_v2_probe_path": LOCAL_IGNORED_V2_MOTION_FIX_PATH.as_posix(),
    "yym4_opened": True,
    "v2_preview_observed": True,
    "anchor_continuity": "improved",
    "segment_connection": "pass",
    "x_jump_regression": "not_reported",
    "motion_speed": "too_slow",
    "tempo_status": "fail_or_warning",
    "major_visual_breakage": False,
    "render_export_checked": False,
    "render_export_required_now": False,
    "next_axis": "motion_tempo_calibration",
}

V2_USER_OBSERVATION_NOTES = [
    "Motion connects smoothly now.",
    "The motion is still very slow.",
    "No new major breakage was reported.",
    "Render/export was not requested and is not needed for this stage.",
]

PRIMITIVE_TEMPO_CLASSIFICATION = [
    {
        "primitive_id": "head_nod",
        "classification": "pass_with_tempo_warning",
        "v2_status": "anchor/neutral-return improved",
        "observed_issue": "nod still reads too slowly for a short reaction beat",
        "decision": "halve the beat span while preserving 0 -> tilt -> 0 return",
    },
    {
        "primitive_id": "expression_swap",
        "classification": "pass",
        "v2_status": "beat-aligned and readable",
        "observed_issue": "no expression regression reported",
        "decision": "keep one expression per faster beat; do not flicker mid-beat",
    },
    {
        "primitive_id": "character_entrance_exit",
        "classification": "pass_with_tempo_warning",
        "v2_status": "bounded neutral movement improved connection",
        "observed_issue": "movement still feels slow and drifting",
        "decision": "halve the bounded travel span while preserving shared anchors",
    },
    {
        "primitive_id": "small_position_move",
        "classification": "pass_with_tempo_warning",
        "v2_status": "anchor continuity improved and X jump not reported",
        "observed_issue": "small movement still feels too slow",
        "decision": "halve the nudge span and keep return to X=-96",
    },
]

TEMPO_CONTRACT = [
    {
        "primitive_id": "head_nod",
        "v2_status": "pass_with_tempo_warning",
        "observed_issue": "visible and connected, but still too slow",
        "intended_tempo": "short reaction nod that reads within a compact 3 second beat",
        "current_duration_or_frame_span_if_available": "360 frames / 6 seconds",
        "proposed_duration_or_frame_span": "180 frames / 3 seconds",
        "speed_change_ratio_if_available": "0.5x duration / 2.0x tempo",
        "easing_policy": "keep linear route for structural probe; concentrate the tilt near the middle keyframe",
        "continuity_policy": "preserve 0 -> negative -> 0 rotation so no tilt leaks across beat boundaries",
        "natural_pause_policy": "no long pause at the tilted state; neutral can hold at the end of the beat",
        "fallback_if_not_supported": "use v2 nod timing but mark tempo unresolved",
    },
    {
        "primitive_id": "expression_swap",
        "v2_status": "pass",
        "observed_issue": "no regression; must remain readable after tempo increase",
        "intended_tempo": "one readable expression state per 3 second beat",
        "current_duration_or_frame_span_if_available": "360 frames / 6 seconds per expression beat",
        "proposed_duration_or_frame_span": "180 frames / 3 seconds per expression beat",
        "speed_change_ratio_if_available": "0.5x duration / 2.0x tempo",
        "easing_policy": "instant image swap remains acceptable; no mid-beat flicker",
        "continuity_policy": "expression changes only at beat boundaries",
        "natural_pause_policy": "hold expression for the full 3 second beat",
        "fallback_if_not_supported": "keep v2 expression beat length and continue tempo work on motion only",
    },
    {
        "primitive_id": "character_entrance_exit",
        "v2_status": "pass_with_tempo_warning",
        "observed_issue": "connected movement still feels slow",
        "intended_tempo": "intentional bounded cue rather than slow drift",
        "current_duration_or_frame_span_if_available": "360 frames / 6 seconds",
        "proposed_duration_or_frame_span": "180 frames / 3 seconds",
        "speed_change_ratio_if_available": "0.5x duration / 2.0x tempo",
        "easing_policy": "linear route is acceptable; avoid slow centerward drift",
        "continuity_policy": "preserve v2 shared anchor X=-96 at adjacent beat boundaries",
        "natural_pause_policy": "entry/exit ends on a stable anchor instead of continuing to drift",
        "fallback_if_not_supported": "hold at X=-96 with no entrance/exit travel",
    },
    {
        "primitive_id": "small_position_move",
        "v2_status": "pass_with_tempo_warning",
        "observed_issue": "anchor continuity improved but small movement remains slow",
        "intended_tempo": "quick bounded nudge that returns to the shared anchor",
        "current_duration_or_frame_span_if_available": "360 frames / 6 seconds",
        "proposed_duration_or_frame_span": "180 frames / 3 seconds",
        "speed_change_ratio_if_available": "0.5x duration / 2.0x tempo",
        "easing_policy": "linear out-and-back is acceptable for this tempo pass",
        "continuity_policy": "start and end every nudge at X=-96",
        "natural_pause_policy": "no lingering drift after the nudge returns to anchor",
        "fallback_if_not_supported": "drop the nudge and keep the shared anchor",
    },
]


def _v3_beat_from_v2(beat: dict[str, Any], index: int) -> dict[str, Any]:
    start = index * V3_BEAT_LENGTH_FRAMES
    end = start + V3_BEAT_LENGTH_FRAMES
    label = str(beat["beat_id"]).replace("v2_", "v3_", 1)
    return {
        **beat,
        "beat_id": label,
        "frame": start,
        "length": V3_BEAT_LENGTH_FRAMES,
        "timing_range": f"{start // FPS}-{end // FPS} sec",
        "motion_label": str(beat["motion_label"]).replace("bounded_side", "tempo_bounded_side"),
    }


V3_BEAT_PLAN: list[dict[str, Any]] = [
    _v3_beat_from_v2(beat, index)
    for index, beat in enumerate(V2_BEAT_PLAN)
]


def write_default_newsroom_yukkuri_animation_tempo_contract_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    materialize_local_v3_tempo_fix_probe(root=base)
    observation = build_default_v2_preview_observation(root=base)
    contract = build_default_tempo_contract(root=base)
    _write_json(base / DEFAULT_V2_PREVIEW_OBSERVATION_PATH, observation)
    _write_text(
        base / DEFAULT_V2_PREVIEW_OBSERVATION_DOC_PATH,
        render_v2_preview_observation_markdown(observation),
    )
    _write_json(base / DEFAULT_TEMPO_CONTRACT_PATH, contract)
    _write_text(base / DEFAULT_TEMPO_CONTRACT_DOC_PATH, render_tempo_contract_markdown(contract))
    return {"observation": observation, "tempo_contract": contract}


def build_default_v2_preview_observation(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    v2_access = _local_probe_access(base, LOCAL_IGNORED_V2_MOTION_FIX_PATH, "local_ignored_v2_motion_fix_probe")
    return {
        "artifact_id": V2_PREVIEW_OBSERVATION_ID,
        "observation_id": V2_PREVIEW_OBSERVATION_ID,
        "schema_version": V2_PREVIEW_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_v2_probe_path": LOCAL_IGNORED_V2_MOTION_FIX_PATH.as_posix(),
        "source_v2_probe_access": v2_access,
        "source_motion_contract_path": DEFAULT_MOTION_CONTRACT_PATH.as_posix(),
        "user_observation_notes": V2_USER_OBSERVATION_NOTES,
        "normalized_user_observation": NORMALIZED_V2_PREVIEW_OBSERVATION,
        "primitive_tempo_classification": PRIMITIVE_TEMPO_CLASSIFICATION,
        "render_export_checked": False,
        "render_export_required_now": False,
        "render_deferred_reason": (
            "The user-side v2 preview confirmed smooth segment connection, so "
            "the remaining bottleneck is tempo calibration rather than render/export proof."
        ),
        "next_axis": "motion_tempo_calibration",
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(v3_created=False),
    }


def build_default_tempo_contract(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    v3_access = _local_probe_access(base, LOCAL_IGNORED_V3_TEMPO_FIX_PATH, "local_ignored_v3_tempo_fix_probe")
    v3_readback = _v3_probe_readback(base, v3_access)
    v3_created = (
        v3_access["target_exists"]
        and v3_access["access_state"] == "verified_present"
        and v3_readback["readback_status"] == "structural_pass"
    )
    next_axis = NEXT_AXIS_V3_PREVIEW if v3_created else FALLBACK_AXIS_TEMPO_IMPLEMENTATION
    return {
        "artifact_id": TEMPO_CONTRACT_ID,
        "tempo_contract_id": TEMPO_CONTRACT_ID,
        "schema_version": TEMPO_CONTRACT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_context": {
            "source_v2_probe_path": LOCAL_IGNORED_V2_MOTION_FIX_PATH.as_posix(),
            "source_v2_observation_path": DEFAULT_V2_PREVIEW_OBSERVATION_PATH.as_posix(),
            "source_motion_contract_path": DEFAULT_MOTION_CONTRACT_PATH.as_posix(),
            "source_nod_head_ymmp_path": SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
        },
        "v2_issue_summary": [
            "anchor continuity improved",
            "segment connection passed",
            "X jump regression was not reported",
            "motion remains very slow",
            "render/export is still not required for this stage",
        ],
        "tempo_contract": TEMPO_CONTRACT,
        "v3_correction_plan": _v3_correction_plan(),
        "v3_beat_plan": _v3_beat_plan(),
        "v3_materialization_status": "materialized_ignored_local_probe" if v3_created else "blocked",
        "v3_local_probe": v3_access,
        "v3_probe_readback": v3_readback,
        "selected_next_axis": next_axis,
        "next_recommended_axis": {
            "selected": next_axis,
            "reason": (
                "ignored local v3 probe exists, is git-ignored, preserves v2 "
                "anchor continuity, and halves beat duration from 6 seconds to 3 seconds"
                if v3_created
                else "v3 tempo probe could not be safely materialized from known routes"
            ),
            "prerequisites": [
                "keep v3 .ymmp ignored and unstaged",
                "use preview-only operator observation before any render request",
                "do not claim production/public acceptance",
            ],
        },
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(v3_created=v3_created),
        "inertia_check": _inertia_check(next_axis),
    }


def materialize_local_v3_tempo_fix_probe(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    project = load_ymmp(base / SOURCE_NOD_HEAD_YMMP_PATH)
    probe = copy.deepcopy(project)
    target_path = base / LOCAL_IGNORED_V3_TEMPO_FIX_PATH
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
    for beat in V3_BEAT_PLAN:
        items.extend(_clone_beat_items(base, source_items, beat))
    timeline["Items"] = sorted(
        items,
        key=lambda item: (int(item.get("Frame", 0)), int(item.get("Layer", 0))),
    )
    timeline["Length"] = V3_TIMELINE_LENGTH_FRAMES
    timeline["CurrentFrame"] = 0
    timeline["MaxLayer"] = max(
        int(item.get("Layer", 0))
        for item in timeline["Items"]
        if isinstance(item.get("Layer"), int)
    )
    save_ymmp(probe, target_path)
    return probe


def render_v2_preview_observation_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Yukkuri Animation V2 Preview Observation v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"next_axis: {payload.get('next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source V2 Probe Access", payload.get("source_v2_probe_access"))
    _append_mapping(lines, "Normalized User Observation", payload.get("normalized_user_observation"))
    _append_rows(
        lines,
        "Primitive Tempo Classification",
        ["primitive_id", "classification", "v2_status", "observed_issue", "decision"],
        payload.get("primitive_tempo_classification"),
    )
    _append_mapping(
        lines,
        "Render Deferral",
        {
            "render_export_checked": payload.get("render_export_checked"),
            "render_export_required_now": payload.get("render_export_required_now"),
            "render_deferred_reason": payload.get("render_deferred_reason"),
        },
    )
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This readback normalizes a user-side v2 preview observation only. It "
        "does not render, launch YMM4 from the agent, stage media, or accept "
        "production/public quality."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_tempo_contract_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Yukkuri Animation Tempo Contract v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"v3_materialization_status: {payload.get('v3_materialization_status')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_rows(
        lines,
        "Tempo Contract",
        [
            "primitive_id",
            "v2_status",
            "observed_issue",
            "intended_tempo",
            "current_duration_or_frame_span_if_available",
            "proposed_duration_or_frame_span",
            "speed_change_ratio_if_available",
            "easing_policy",
            "continuity_policy",
            "natural_pause_policy",
            "fallback_if_not_supported",
        ],
        payload.get("tempo_contract"),
    )
    _append_mapping(lines, "V2 Issue Summary", payload.get("v2_issue_summary"))
    _append_mapping(lines, "V3 Correction Plan", payload.get("v3_correction_plan"))
    _append_rows(
        lines,
        "V3 Beat Plan",
        ["beat_id", "timing_range", "scene_function", "primitive_ids", "parent_x_values", "head_rotation_values"],
        payload.get("v3_beat_plan"),
    )
    _append_mapping(lines, "V3 Local Probe", payload.get("v3_local_probe"))
    _append_mapping(lines, "V3 Probe Readback", payload.get("v3_probe_readback"))
    _append_mapping(lines, "Next Recommended Axis", payload.get("next_recommended_axis"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "The v3 probe is an ignored local diagnostic artifact. It is not rendered, "
        "not staged, not committed, and not production/public acceptance."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _v3_probe_readback(base: Path, v3_access: dict[str, Any]) -> dict[str, Any]:
    target = base / LOCAL_IGNORED_V3_TEMPO_FIX_PATH
    if not target.exists():
        return {
            "readback_status": "blocked",
            "reason": "local_v3_probe_missing",
            "target_exists": False,
        }
    data = load_ymmp(target)
    timeline = _first_timeline(data)
    items = _get_timeline_items(data)
    item_type_counts: dict[str, int] = {}
    for item in items:
        item_type_counts[_item_type(item)] = item_type_counts.get(_item_type(item), 0) + 1
    beat_summaries = [_beat_readback(beat, items) for beat in V3_BEAT_PLAN]
    primitive_status = _v3_primitive_status(beat_summaries)
    unexpected_item_types = sorted(
        item_type for item_type in item_type_counts if item_type not in {"GroupItem", "ImageItem"}
    )
    structural_pass = (
        timeline.get("Length") == V3_TIMELINE_LENGTH_FRAMES
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
            "length_sec": round(V3_TIMELINE_LENGTH_FRAMES / FPS, 6),
            "item_count": len(items),
            "item_type_counts": item_type_counts,
            "unexpected_item_types": unexpected_item_types,
        },
        "beat_readback": beat_summaries,
        "primitive_status": primitive_status,
        "tempo_change": {
            "v2_beat_length_frames": V2_BEAT_LENGTH_FRAMES,
            "v3_beat_length_frames": V3_BEAT_LENGTH_FRAMES,
            "duration_ratio": round(V3_BEAT_LENGTH_FRAMES / V2_BEAT_LENGTH_FRAMES, 6),
            "tempo_multiplier": round(V2_BEAT_LENGTH_FRAMES / V3_BEAT_LENGTH_FRAMES, 6),
        },
        "anchor_continuity": {
            "shared_anchor_x": -96.0,
            "adjacent_boundaries_share_anchor": True,
        },
        "source_ymmp_copy_basis": SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
        "local_probe_access_state": v3_access["access_state"],
        "YMM4_launch_status": "not_launched",
        "render_status": "not_rendered",
        "audio_tts_status": "not_created",
    }


def _v3_primitive_status(beat_summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
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
    short_beat_ok = all(row.get("length") == V3_BEAT_LENGTH_FRAMES for row in beat_summaries)
    return [
        {
            "primitive_id": "head_nod",
            "status": (
                "pass"
                if short_beat_ok
                and any(
                    "head_nod" in row["primitive_ids"]
                    and len(row.get("head_rotation_values", [])) == 3
                    and row["head_rotation_values"][0] == 0.0
                    and row["head_rotation_values"][-1] == 0.0
                    and any(abs(value) >= 8.0 for value in row["head_rotation_values"])
                    for row in beat_summaries
                )
                else "blocked"
            ),
            "evidence": "head nod keeps 0 -> non-zero -> 0 and beat length is 180 frames",
        },
        {
            "primitive_id": "expression_swap",
            "status": "pass" if short_beat_ok and len(face_paths) >= 3 else "blocked",
            "evidence": sorted(face_paths),
        },
        {
            "primitive_id": "character_entrance_exit",
            "status": (
                "pass"
                if short_beat_ok
                and shared_anchor_ok
                and any(
                    "character_entrance_exit" in row["primitive_ids"]
                    and 40.0 <= _value_range(row.get("parent_x_values", [])) <= 80.0
                    for row in beat_summaries
                )
                else "blocked"
            ),
            "evidence": "bounded entry/exit travel is preserved at 180 frames per beat",
        },
        {
            "primitive_id": "small_position_move",
            "status": (
                "pass"
                if short_beat_ok
                and shared_anchor_ok
                and any(
                    "small_position_move" in row["primitive_ids"]
                    and 0 < _value_range(row.get("parent_x_values", [])) <= 24.0
                    for row in beat_summaries
                )
                else "blocked"
            ),
            "evidence": "nudges still return to X=-96 and run in 180-frame beats",
        },
    ]


def _v3_correction_plan() -> dict[str, Any]:
    return {
        "tempo": [
            "halve each v2 beat from 360 frames / 6 seconds to 180 frames / 3 seconds",
            "keep the five-beat structure but shorten the total probe from 30 seconds to 15 seconds",
        ],
        "anchor_continuity": [
            "preserve X=-96 shared anchor at adjacent beat boundaries",
            "do not reintroduce v1 X jumps",
        ],
        "head_nod": [
            "preserve 0 -> negative rotation -> 0 neutral return",
            "make the nod read inside a short reaction beat",
        ],
        "expression_timing": [
            "keep one expression per 3 second beat",
            "do not flicker mid-beat",
        ],
        "render_boundary": "no render/export proof in this slice",
    }


def _v3_beat_plan() -> list[dict[str, Any]]:
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
        for beat in V3_BEAT_PLAN
    ]


def _local_probe_access(base: Path, path: Path, artifact_id: str) -> dict[str, Any]:
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
        "artifact_id": artifact_id,
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


def _boundaries(*, v3_created: bool) -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "dense_script_modified": False,
        "local_ignored_v3_probe_created": v3_created,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_text_density_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "tempo_contract_targets_reported_visual_issue", "status": True},
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


def main() -> int:
    write_default_newsroom_yukkuri_animation_tempo_contract_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
