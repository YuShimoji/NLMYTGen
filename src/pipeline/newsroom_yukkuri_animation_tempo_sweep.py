"""Record the v3 preview observation and create a tempo sweep probe.

This slice replaces one-speed-at-a-time tempo tuning with a single local
ignored YMM4 probe that compares several short timing bands. It does not
launch YMM4, render, create audio/TTS, fetch external media, or claim
production quality.
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
    _value_range,
)
from src.pipeline.newsroom_yukkuri_animation_primitive_probe_materialization import (
    SOURCE_NOD_HEAD_YMMP_PATH,
    _clone_beat_items,
)
from src.pipeline.newsroom_yukkuri_animation_tempo_contract import (
    DEFAULT_TEMPO_CONTRACT_PATH,
    LOCAL_IGNORED_V3_TEMPO_FIX_PATH,
    V3_BEAT_PLAN,
    V3_TIMELINE_LENGTH_FRAMES,
    _git_check_ignore,
    _local_probe_access,
    _sha256,
    _write_json,
    _write_text,
    materialize_local_v3_tempo_fix_probe,
)
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


V3_PREVIEW_OBSERVATION_ID = (
    "newsroom_yukkuri_animation_v3_preview_observation_v1_2026_06_29"
)
TEMPO_SWEEP_CONTRACT_ID = (
    "newsroom_yukkuri_animation_tempo_sweep_contract_v1_2026_06_29"
)
V3_PREVIEW_SCHEMA_VERSION = "newsroom_yukkuri_animation_v3_preview_observation.v1"
TEMPO_SWEEP_SCHEMA_VERSION = "newsroom_yukkuri_animation_tempo_sweep_contract.v1"

DEFAULT_V3_PREVIEW_OBSERVATION_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "yukkuri_animation_v3_preview_observation_v1.json"
)
DEFAULT_V3_PREVIEW_OBSERVATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_YUKKURI_ANIMATION_V3_PREVIEW_OBSERVATION_V1_2026-06-29.md"
)
DEFAULT_TEMPO_SWEEP_CONTRACT_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "yukkuri_animation_tempo_sweep_contract_v1.json"
)
DEFAULT_TEMPO_SWEEP_CONTRACT_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_YUKKURI_ANIMATION_TEMPO_SWEEP_CONTRACT_V1_2026-06-29.md"
)

LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH = Path(
    "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp"
)
NEXT_AXIS_V4_SWEEP_PREVIEW = (
    "newsroom-yukkuri-animation-tempo-sweep-preview-operator-instruction-v1"
)
FALLBACK_AXIS_SWEEP_IMPLEMENTATION = (
    "newsroom-yukkuri-animation-tempo-sweep-implementation-v1"
)
TIMING_STRUCTURE_AUDIT_AXIS = (
    "newsroom-yukkuri-animation-timing-structure-audit-v1"
)
ANCHOR_TEMPO_JOINT_FIX_AXIS = (
    "newsroom-yukkuri-animation-anchor-tempo-joint-fix-v1"
)

FPS = 60
PRIMITIVES_INCLUDED = [
    "head_nod",
    "small_position_move",
    "character_entrance_exit",
    "expression_swap",
]

NORMALIZED_V3_PREVIEW_OBSERVATION: dict[str, Any] = {
    "source_observation_role": "user_opened_local_v3_ymmp_preview",
    "source_v3_probe_path": LOCAL_IGNORED_V3_TEMPO_FIX_PATH.as_posix(),
    "yym4_opened": True,
    "v3_preview_observed": True,
    "motion_speed": "still_too_slow",
    "floatiness": "high",
    "v3_tempo_improved_but_insufficient": True,
    "single_value_iteration_risk": True,
    "recommended_method": "tempo_sweep",
    "render_export_checked": False,
    "render_export_required_now": False,
    "next_axis": "tempo_sweep_calibration",
}

V3_USER_OBSERVATION_NOTES = [
    "The v3 probe is shorter, around 10 seconds by user perception.",
    "The movement still feels floaty and slow.",
    "The user suggested starting around 1 second and fine-tuning from there.",
    "Continuing one fast/slow value at a time would be inefficient.",
]

TEMPO_SWEEP_BANDS: list[dict[str, Any]] = [
    {
        "band_id": "tempo_band_030f_0_5s",
        "frame_span": 30,
        "seconds_at_60fps": 0.5,
        "expected_feel": "very snappy lower bound; likely useful for reaction-only motion",
        "primitives_included": PRIMITIVES_INCLUDED,
        "continuity_policy": "carry forward v2/v3 X=-96 shared anchor at adjacent beat boundaries",
        "anchor_policy": "do not reintroduce X jump; each nudge starts and ends on the shared anchor",
        "notes": "Fastest comparison band; expression readability may need a longer hold in scene integration.",
    },
    {
        "band_id": "tempo_band_045f_0_75s",
        "frame_span": 45,
        "seconds_at_60fps": 0.75,
        "expected_feel": "quick but still readable; candidate if 1.0 second remains floaty",
        "primitives_included": PRIMITIVES_INCLUDED,
        "continuity_policy": "carry forward v2/v3 X=-96 shared anchor at adjacent beat boundaries",
        "anchor_policy": "keep bounded entry/exit and return-to-anchor nudges",
        "notes": "Middle-fast comparison band for lightweight reenactment beats.",
    },
    {
        "band_id": "tempo_band_060f_1_0s",
        "frame_span": 60,
        "seconds_at_60fps": 1.0,
        "expected_feel": "primary default candidate based on the user suggestion to start around 1 second",
        "primitives_included": PRIMITIVES_INCLUDED,
        "continuity_policy": "carry forward v2/v3 X=-96 shared anchor at adjacent beat boundaries",
        "anchor_policy": "keep head nod as a short reaction and movement as bounded cue",
        "notes": "Expected default candidate unless preview shows it is still slow or too abrupt.",
    },
    {
        "band_id": "tempo_band_090f_1_5s",
        "frame_span": 90,
        "seconds_at_60fps": 1.5,
        "expected_feel": "upper comparison band; should reveal whether longer movement still reads floaty",
        "primitives_included": PRIMITIVES_INCLUDED,
        "continuity_policy": "carry forward v2/v3 X=-96 shared anchor at adjacent beat boundaries",
        "anchor_policy": "bounded movement only; no slow centerward drift",
        "notes": "Kept as a contrast band rather than a likely default after the v3 observation.",
    },
]


def _v4_beat_from_v3(
    *,
    band: dict[str, Any],
    base_beat: dict[str, Any],
    section_index: int,
    beat_index: int,
    frame: int,
) -> dict[str, Any]:
    span = int(band["frame_span"])
    suffix = str(base_beat["beat_id"]).replace("v3_beat_", "", 1)
    return {
        **base_beat,
        "beat_id": f"v4_{band['band_id']}_beat_{beat_index + 1:02d}_{suffix}",
        "source_v3_beat_id": base_beat["beat_id"],
        "band_id": band["band_id"],
        "section_index": section_index,
        "frame": frame,
        "length": span,
        "timing_range": f"{frame / FPS:.2f}-{(frame + span) / FPS:.2f} sec",
        "motion_label": f"tempo_sweep_{band['frame_span']}f_{base_beat['motion_label']}",
    }


def _build_v4_beat_plan() -> list[dict[str, Any]]:
    beats: list[dict[str, Any]] = []
    frame = 0
    for section_index, band in enumerate(TEMPO_SWEEP_BANDS, start=1):
        for beat_index, base_beat in enumerate(V3_BEAT_PLAN):
            beat = _v4_beat_from_v3(
                band=band,
                base_beat=base_beat,
                section_index=section_index,
                beat_index=beat_index,
                frame=frame,
            )
            beats.append(beat)
            frame += int(band["frame_span"])
    return beats


V4_BEAT_PLAN: list[dict[str, Any]] = _build_v4_beat_plan()
V4_TIMELINE_LENGTH_FRAMES = sum(int(row["frame_span"]) * len(V3_BEAT_PLAN) for row in TEMPO_SWEEP_BANDS)


def write_default_newsroom_yukkuri_animation_tempo_sweep_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    materialize_local_v3_tempo_fix_probe(root=base)
    materialize_local_v4_tempo_sweep_probe(root=base)
    observation = build_default_v3_preview_observation(root=base)
    contract = build_default_tempo_sweep_contract(root=base)
    _write_json(base / DEFAULT_V3_PREVIEW_OBSERVATION_PATH, observation)
    _write_text(
        base / DEFAULT_V3_PREVIEW_OBSERVATION_DOC_PATH,
        render_v3_preview_observation_markdown(observation),
    )
    _write_json(base / DEFAULT_TEMPO_SWEEP_CONTRACT_PATH, contract)
    _write_text(
        base / DEFAULT_TEMPO_SWEEP_CONTRACT_DOC_PATH,
        render_tempo_sweep_contract_markdown(contract),
    )
    return {"observation": observation, "tempo_sweep_contract": contract}


def build_default_v3_preview_observation(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    v3_access = _local_probe_access(base, LOCAL_IGNORED_V3_TEMPO_FIX_PATH, "local_ignored_v3_tempo_fix_probe")
    return {
        "artifact_id": V3_PREVIEW_OBSERVATION_ID,
        "observation_id": V3_PREVIEW_OBSERVATION_ID,
        "schema_version": V3_PREVIEW_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_v3_probe_path": LOCAL_IGNORED_V3_TEMPO_FIX_PATH.as_posix(),
        "source_v3_probe_access": v3_access,
        "source_tempo_contract_path": DEFAULT_TEMPO_CONTRACT_PATH.as_posix(),
        "user_observation_notes": V3_USER_OBSERVATION_NOTES,
        "normalized_user_observation": NORMALIZED_V3_PREVIEW_OBSERVATION,
        "current_issue": {
            "motion_speed": "still_too_slow",
            "floatiness": "high",
            "v3_tempo_improved_but_insufficient": True,
            "next_axis": "tempo_sweep_calibration",
        },
        "single_value_iteration_risk": {
            "risk": True,
            "reason": (
                "The user already distinguished shorter from usable. More one-value "
                "speed changes would keep asking the operator for fast/slow feedback "
                "instead of choosing a default band."
            ),
            "replacement_method": "compare 0.5, 0.75, 1.0, and 1.5 second bands in one ignored local probe",
        },
        "render_export_checked": False,
        "render_export_required_now": False,
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(v4_created=False),
    }


def build_default_tempo_sweep_contract(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    v3_access = _local_probe_access(base, LOCAL_IGNORED_V3_TEMPO_FIX_PATH, "local_ignored_v3_tempo_fix_probe")
    v4_access = _local_probe_access(base, LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH, "local_ignored_v4_tempo_sweep_probe")
    v4_readback = _v4_probe_readback(base, v4_access)
    v4_created = (
        v4_access["target_exists"]
        and v4_access["access_state"] == "verified_present"
        and v4_readback["readback_status"] == "structural_pass"
    )
    next_axis = _next_axis(v4_created=v4_created, v4_readback=v4_readback)
    return {
        "artifact_id": TEMPO_SWEEP_CONTRACT_ID,
        "tempo_sweep_contract_id": TEMPO_SWEEP_CONTRACT_ID,
        "schema_version": TEMPO_SWEEP_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_context": {
            "source_v3_probe_path": LOCAL_IGNORED_V3_TEMPO_FIX_PATH.as_posix(),
            "source_v3_observation_path": DEFAULT_V3_PREVIEW_OBSERVATION_PATH.as_posix(),
            "source_tempo_contract_path": DEFAULT_TEMPO_CONTRACT_PATH.as_posix(),
            "source_motion_contract_path": DEFAULT_MOTION_CONTRACT_PATH.as_posix(),
            "source_nod_head_ymmp_path": SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
            "v3_materialization_basis": "existing tracked v3 tempo contract materializer",
        },
        "source_v3_probe_access": v3_access,
        "v3_issue_summary": [
            "v3 is shorter than v2",
            "v3 is still floaty and too slow",
            "user suggested starting around 1 second",
            "single-value fast/slow loops are inefficient",
            "render/export remains unnecessary for this stage",
        ],
        "speed_bands": TEMPO_SWEEP_BANDS,
        "primitive_coverage_per_band": _primitive_coverage_per_band(),
        "anchor_continuity_carry_forward": {
            "source_policy": "v2/v3 shared anchor",
            "shared_anchor_x": -96.0,
            "no_x_jump_regression": True,
            "entry_exit_policy": "bounded side travel only",
            "small_move_policy": "start and end at X=-96",
            "head_nod_policy": "0 -> negative -> 0 neutral return",
        },
        "expected_default_candidate": {
            "band_id": "tempo_band_060f_1_0s",
            "frame_span": 60,
            "seconds_at_60fps": 1.0,
            "reason": "The user suggested starting around 1 second; 0.75 and 0.5 seconds are comparison lower bounds.",
        },
        "review_instruction_for_next_preview": [
            "Open the v4 tempo sweep probe only; do not render.",
            "Review bands in the encoded order: 0.5 sec, 0.75 sec, 1.0 sec, 1.5 sec.",
            "Choose the default tempo band, or report that all bands are still too slow/too abrupt.",
            "After a usable band is chosen, stop the primitive tempo-only loop and move to scene-beat integration.",
        ],
        "exit_criterion": {
            "choose_default_tempo_band": True,
            "stop_primitive_tempo_only_loop": True,
            "move_to_scene_beat_integration_after_usable_band": True,
        },
        "v4_materialization_status": "materialized_ignored_local_probe" if v4_created else "blocked",
        "v4_local_probe": v4_access,
        "v4_probe_readback": v4_readback,
        "selected_next_axis": next_axis,
        "next_recommended_axis": {
            "selected": next_axis,
            "reason": _next_axis_reason(v4_created=v4_created, v4_readback=v4_readback),
            "prerequisites": [
                "keep v4 .ymmp ignored and unstaged",
                "use preview-only operator observation before any render request",
                "do not claim production/public acceptance",
            ],
        },
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(v4_created=v4_created),
        "inertia_check": _inertia_check(next_axis),
    }


def materialize_local_v4_tempo_sweep_probe(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    project = load_ymmp(base / SOURCE_NOD_HEAD_YMMP_PATH)
    probe = copy.deepcopy(project)
    target_path = base / LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH
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
    for beat in V4_BEAT_PLAN:
        items.extend(_clone_beat_items(base, source_items, beat))
    timeline["Items"] = sorted(
        items,
        key=lambda item: (int(item.get("Frame", 0)), int(item.get("Layer", 0))),
    )
    timeline["Length"] = V4_TIMELINE_LENGTH_FRAMES
    timeline["CurrentFrame"] = 0
    timeline["MaxLayer"] = max(
        int(item.get("Layer", 0))
        for item in timeline["Items"]
        if isinstance(item.get("Layer"), int)
    )
    save_ymmp(probe, target_path)
    return probe


def render_v3_preview_observation_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Yukkuri Animation V3 Preview Observation v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        "",
    ]
    _append_mapping(lines, "Source V3 Probe Access", payload.get("source_v3_probe_access"))
    _append_mapping(lines, "Normalized User Observation", payload.get("normalized_user_observation"))
    _append_mapping(lines, "Current Issue", payload.get("current_issue"))
    _append_mapping(lines, "Single Value Iteration Risk", payload.get("single_value_iteration_risk"))
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
        "This readback normalizes a user-side v3 preview observation only. It "
        "does not render, launch YMM4 from the agent, stage media, or accept "
        "production/public quality."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_tempo_sweep_contract_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Yukkuri Animation Tempo Sweep Contract v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"v4_materialization_status: {payload.get('v4_materialization_status')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "Source V3 Probe Access", payload.get("source_v3_probe_access"))
    _append_mapping(lines, "V3 Issue Summary", payload.get("v3_issue_summary"))
    _append_rows(
        lines,
        "Tempo Bands",
        [
            "band_id",
            "frame_span",
            "seconds_at_60fps",
            "expected_feel",
            "primitives_included",
            "continuity_policy",
            "anchor_policy",
            "notes",
        ],
        payload.get("speed_bands"),
    )
    _append_rows(
        lines,
        "Primitive Coverage Per Band",
        ["band_id", "frame_span", "primitive_ids", "beat_count", "section_timing_range"],
        payload.get("primitive_coverage_per_band"),
    )
    _append_mapping(
        lines,
        "Anchor Continuity Carry Forward",
        payload.get("anchor_continuity_carry_forward"),
    )
    _append_mapping(lines, "Expected Default Candidate", payload.get("expected_default_candidate"))
    _append_mapping(lines, "Review Instruction For Next Preview", payload.get("review_instruction_for_next_preview"))
    _append_mapping(lines, "Exit Criterion", payload.get("exit_criterion"))
    _append_mapping(lines, "V4 Local Probe", payload.get("v4_local_probe"))
    _append_mapping(lines, "V4 Probe Readback", payload.get("v4_probe_readback"))
    _append_mapping(lines, "Next Recommended Axis", payload.get("next_recommended_axis"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "The v4 probe is an ignored local diagnostic artifact. It is not rendered, "
        "not staged, not committed, and not production/public acceptance."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _v4_probe_readback(base: Path, v4_access: dict[str, Any]) -> dict[str, Any]:
    target = base / LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH
    if not target.exists():
        return {
            "readback_status": "blocked",
            "reason": "local_v4_probe_missing",
            "target_exists": False,
        }
    data = load_ymmp(target)
    timeline = _first_timeline(data)
    items = _get_timeline_items(data)
    item_type_counts: dict[str, int] = {}
    for item in items:
        item_type_counts[_item_type(item)] = item_type_counts.get(_item_type(item), 0) + 1
    beat_summaries = [_beat_readback(beat, items) for beat in V4_BEAT_PLAN]
    band_readback = _band_readback(beat_summaries)
    unexpected_item_types = sorted(
        item_type for item_type in item_type_counts if item_type not in {"GroupItem", "ImageItem"}
    )
    structural_pass = (
        timeline.get("Length") == V4_TIMELINE_LENGTH_FRAMES
        and item_type_counts.get("GroupItem") == 40
        and item_type_counts.get("ImageItem") == 40
        and not unexpected_item_types
        and all(row["status"] == "pass" for row in beat_summaries)
        and all(row["status"] == "pass" for row in band_readback)
    )
    return {
        "readback_status": "structural_pass" if structural_pass else "blocked",
        "target_exists": True,
        "file_sha256": _sha256(target),
        "file_size_bytes": target.stat().st_size,
        "timeline": {
            "fps": _dict(timeline.get("VideoInfo")).get("FPS"),
            "length_frames": timeline.get("Length"),
            "length_sec": round(V4_TIMELINE_LENGTH_FRAMES / FPS, 6),
            "item_count": len(items),
            "item_type_counts": item_type_counts,
            "unexpected_item_types": unexpected_item_types,
        },
        "speed_band_order": [band["band_id"] for band in TEMPO_SWEEP_BANDS],
        "band_readback": band_readback,
        "tempo_sweep_summary": {
            "band_count": len(TEMPO_SWEEP_BANDS),
            "beat_count_per_band": len(V3_BEAT_PLAN),
            "total_beat_count": len(V4_BEAT_PLAN),
            "frame_spans": [band["frame_span"] for band in TEMPO_SWEEP_BANDS],
            "seconds_at_60fps": [band["seconds_at_60fps"] for band in TEMPO_SWEEP_BANDS],
            "expected_default_candidate": "tempo_band_060f_1_0s",
        },
        "source_ymmp_copy_basis": SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
        "git_check_ignore_result": _git_check_ignore(base, LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH),
        "local_probe_access_state": v4_access["access_state"],
        "YMM4_launch_status": "not_launched",
        "render_status": "not_rendered",
        "audio_tts_status": "not_created",
    }


def _band_readback(beat_summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_id = {beat["beat_id"]: beat for beat in V4_BEAT_PLAN}
    for band in TEMPO_SWEEP_BANDS:
        band_id = str(band["band_id"])
        span = int(band["frame_span"])
        band_beats = [
            row for row in beat_summaries
            if by_id.get(str(row["beat_id"]), {}).get("band_id") == band_id
        ]
        primitive_ids = sorted(
            {
                primitive_id
                for row in band_beats
                for primitive_id in row.get("primitive_ids", [])
            }
        )
        starts = [row["parent_x_values"][0] for row in band_beats if row.get("parent_x_values")]
        ends = [row["parent_x_values"][-1] for row in band_beats if row.get("parent_x_values")]
        shared_anchor_ok = (
            len(starts) == 5
            and starts[1:] == [-96.0, -96.0, -96.0, -96.0]
            and ends[:4] == [-96.0, -96.0, -96.0, -96.0]
        )
        lengths_ok = all(row.get("length") == span for row in band_beats)
        primitives_ok = sorted(PRIMITIVES_INCLUDED) == primitive_ids
        nod_ok = any(
            "head_nod" in row.get("primitive_ids", [])
            and len(row.get("head_rotation_values", [])) == 3
            and row["head_rotation_values"][0] == 0.0
            and row["head_rotation_values"][-1] == 0.0
            and any(abs(value) >= 8.0 for value in row["head_rotation_values"])
            for row in band_beats
        )
        nudge_ok = any(
            "small_position_move" in row.get("primitive_ids", [])
            and 0 < _value_range(row.get("parent_x_values", [])) <= 24.0
            for row in band_beats
        )
        status = "pass" if lengths_ok and primitives_ok and shared_anchor_ok and nod_ok and nudge_ok else "blocked"
        if band_beats:
            start = int(band_beats[0]["frame"])
            end = int(band_beats[-1]["frame"]) + int(band_beats[-1]["length"])
            timing_range = f"{start / FPS:.2f}-{end / FPS:.2f} sec"
        else:
            start = None
            end = None
            timing_range = "missing"
        rows.append(
            {
                "band_id": band_id,
                "frame_span": span,
                "seconds_at_60fps": band["seconds_at_60fps"],
                "section_start_frame": start,
                "section_end_frame": end,
                "section_timing_range": timing_range,
                "beat_count": len(band_beats),
                "primitive_ids": primitive_ids,
                "anchor_continuity": "pass" if shared_anchor_ok else "blocked",
                "status": status,
            }
        )
    return rows


def _primitive_coverage_per_band() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for band in TEMPO_SWEEP_BANDS:
        beats = [beat for beat in V4_BEAT_PLAN if beat["band_id"] == band["band_id"]]
        rows.append(
            {
                "band_id": band["band_id"],
                "frame_span": band["frame_span"],
                "primitive_ids": sorted(PRIMITIVES_INCLUDED),
                "beat_count": len(beats),
                "section_timing_range": (
                    f"{beats[0]['frame'] / FPS:.2f}-"
                    f"{(beats[-1]['frame'] + beats[-1]['length']) / FPS:.2f} sec"
                    if beats
                    else "missing"
                ),
            }
        )
    return rows


def _next_axis(*, v4_created: bool, v4_readback: dict[str, Any]) -> str:
    if not v4_created:
        return FALLBACK_AXIS_SWEEP_IMPLEMENTATION
    blocked_bands = [
        row for row in v4_readback.get("band_readback", [])
        if row.get("status") != "pass"
    ]
    if blocked_bands:
        return ANCHOR_TEMPO_JOINT_FIX_AXIS
    if v4_readback.get("timeline", {}).get("length_frames") != V4_TIMELINE_LENGTH_FRAMES:
        return TIMING_STRUCTURE_AUDIT_AXIS
    return NEXT_AXIS_V4_SWEEP_PREVIEW


def _next_axis_reason(*, v4_created: bool, v4_readback: dict[str, Any]) -> str:
    if v4_created:
        return (
            "ignored local v4 tempo sweep probe exists, is git-ignored, "
            "covers all requested bands, and preserves the v2/v3 anchor rules"
        )
    return f"v4 tempo sweep probe could not be safely materialized: {v4_readback.get('reason', 'readback blocked')}"


def _boundaries(*, v4_created: bool) -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "dense_script_modified": False,
        "local_ignored_v4_probe_created": v4_created,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_text_density_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "tempo_sweep_replaces_single_value_loop", "status": True},
        {"gate": "next_concrete_animation_milestone_named", "status": next_axis},
    ]


def main() -> int:
    write_default_newsroom_yukkuri_animation_tempo_sweep_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
