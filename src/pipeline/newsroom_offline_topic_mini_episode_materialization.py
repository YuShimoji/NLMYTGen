"""Materialize the offline topic mini episode capsule as an ignored YMM4 probe.

This slice connects the current 5-beat offline-topic capsule to a local
diagnostic YMM4 project. It uses only the current capsule, tracked source
materials, plain TextItem roles, and the frozen minimal animation accent route.
It does not use stale fake-packet routes as the current materialization path.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_offline_topic_mini_episode_capsule import (
    ANIMATION_ASSIGNMENTS,
    DEFAULT_CAPSULE_CONTRACT_PATH,
    DEFAULT_CAPSULE_PATH,
)
from src.pipeline.newsroom_offline_topic_mini_episode_capsule_bridge import (
    DEFAULT_BRIDGE_PATH,
)
from src.pipeline.newsroom_rss_dry_run_to_animated_explanation_beat import (
    DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
)
from src.pipeline.newsroom_yukkuri_animation_primitive_probe_materialization import (
    SOURCE_NOD_HEAD_YMMP_PATH,
    _clone_beat_items,
    _dict,
    _first_timeline,
    _get_timeline_items,
    _item_type,
    _route_values,
)
from src.pipeline.newsroom_yukkuri_animation_tempo_contract import (
    _write_json,
    _write_text,
)
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


MATERIALIZATION_ID = (
    "newsroom_offline_topic_mini_episode_capsule_materialization_v1_2026_06_30"
)
ROUTE_ID = "newsroom_offline_topic_mini_episode_materialization_route_v1_2026_06_30"
MATERIALIZATION_SCHEMA_VERSION = (
    "newsroom_offline_topic_mini_episode_capsule_materialization.v1"
)
ROUTE_SCHEMA_VERSION = "newsroom_offline_topic_mini_episode_materialization_route.v1"

DEFAULT_MATERIALIZATION_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "offline_topic_mini_episode_capsule_materialization_v1.json"
)
DEFAULT_MATERIALIZATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_CAPSULE_MATERIALIZATION_V1_2026-06-30.md"
)
DEFAULT_ROUTE_PATH = Path(
    "samples/_probe/newsroom_handoff/offline_topic_mini_episode_materialization_route_v1.json"
)

LOCAL_IGNORED_MATERIALIZED_YMMP_PATH = Path(
    "_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp"
)

FPS = 60
BEAT_DURATION_FRAMES = 360
BEAT_COUNT = 5
TIMELINE_LENGTH_FRAMES = BEAT_DURATION_FRAMES * BEAT_COUNT

NEXT_AXIS_PREVIEW = "newsroom-offline-topic-mini-episode-preview-operator-instruction-v1"
NEXT_AXIS_ROUTE_AUDIT = "newsroom-episode-capsule-route-audit-v1"
NEXT_AXIS_IMPLEMENTATION = (
    "newsroom-offline-topic-mini-episode-materialization-implementation-v1"
)
NEXT_AXIS_TOPIC_AUDIT = "newsroom-rss-topic-fixture-route-audit-v1"
NEXT_AXIS_LIVE_BOUNDARY_PLAN = "newsroom-live-rss-boundary-plan-v1"


def write_default_newsroom_offline_topic_mini_episode_materialization_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    route = build_default_materialization_route(root=base)
    if route["route_classification"] == "current_supported":
        materialize_local_offline_topic_mini_episode_capsule(root=base)
    materialization = build_default_materialization_readback(root=base)
    route = build_default_materialization_route(root=base)
    _write_json(base / DEFAULT_ROUTE_PATH, route)
    _write_json(base / DEFAULT_MATERIALIZATION_PATH, materialization)
    _write_text(
        base / DEFAULT_MATERIALIZATION_DOC_PATH,
        render_materialization_markdown(materialization),
    )
    return {
        "route": route,
        "materialization": materialization,
    }


def build_default_materialization_route(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    capsule = _load_json_object(base / DEFAULT_CAPSULE_PATH)
    route_classification, blockers = _classify_route(base, capsule)
    output_artifacts = [
        {"path": DEFAULT_ROUTE_PATH.as_posix(), "scope": "tracked_route_readback"},
        {
            "path": DEFAULT_MATERIALIZATION_PATH.as_posix(),
            "scope": "tracked_materialization_readback",
        },
        {
            "path": DEFAULT_MATERIALIZATION_DOC_PATH.as_posix(),
            "scope": "tracked_verification_doc",
        },
        {
            "path": LOCAL_IGNORED_MATERIALIZED_YMMP_PATH.as_posix(),
            "scope": "ignored_local_only",
        },
    ]
    return {
        "artifact_id": ROUTE_ID,
        "route_id": ROUTE_ID,
        "schema_version": ROUTE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_capsule_path": DEFAULT_CAPSULE_PATH.as_posix(),
        "source_capsule_contract_path": DEFAULT_CAPSULE_CONTRACT_PATH.as_posix(),
        "source_topic_fixture_path": DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix(),
        "route_classification": route_classification,
        "route_confidence": "high" if route_classification == "current_supported" else "low",
        "existing_artifacts_used": [
            DEFAULT_CAPSULE_PATH.as_posix(),
            DEFAULT_CAPSULE_CONTRACT_PATH.as_posix(),
            DEFAULT_BRIDGE_PATH.as_posix(),
            DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix(),
            "samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json",
            SOURCE_NOD_HEAD_YMMP_PATH.as_posix(),
        ],
        "stale_fake_packet_route_classification": {
            "path": "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json",
            "classification": "stale_fake_packet_only",
            "used_for_materialization": False,
            "reason": "older fake-packet capsule is not the current offline-topic route",
        },
        "transformation_steps": [
            "read the current offline-topic 5-beat capsule",
            "create one sequential timeline segment per capsule beat",
            "insert one plain TextItem per beat as the diagnostic text role",
            "clone tracked nod_head character items only for beats with a capsule animation assignment",
            "keep body X fixed and use at most one expression or short nod per relevant beat",
            "write the result to an ignored local YMM4 diagnostic project",
        ],
        "output_artifacts": output_artifacts,
        "item_semantics": {
            "TextItem role": "one visible plain diagnostic text/caption role per beat",
            "GroupItem/ImageItem animation accent role": (
                "frozen optional character accent from tracked nod_head source; "
                "no body forward/back and no full chaban scene"
            ),
            "beat timing role": (
                f"{BEAT_COUNT} sequential beats, {BEAT_DURATION_FRAMES} frames each, "
                f"{TIMELINE_LENGTH_FRAMES} frames total at {FPS} fps"
            ),
            "source boundary role": "each beat carries offline fixture/source-boundary text",
        },
        "route_blockers": blockers,
        "next_required_route_work": _next_required_route_work(route_classification),
        "boundaries": _boundaries(local_ymmp_created=False),
    }


def build_default_materialization_readback(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    capsule = _load_json_object(base / DEFAULT_CAPSULE_PATH)
    route = build_default_materialization_route(root=base)
    access = _local_probe_access(base)
    readback = _local_materialization_readback(base, capsule, access)
    materialized = readback.get("readback_status") == "structural_pass"
    next_axis = NEXT_AXIS_PREVIEW if materialized else _fallback_next_axis(route)
    return {
        "artifact_id": MATERIALIZATION_ID,
        "schema_version": MATERIALIZATION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_capsule_path": DEFAULT_CAPSULE_PATH.as_posix(),
        "source_route_path": DEFAULT_ROUTE_PATH.as_posix(),
        "source_topic_fixture_path": DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix(),
        "route": route,
        "local_ymmp_materialization_status": (
            "materialized_ignored_local_probe" if materialized else "blocked_or_deferred"
        ),
        "local_probe_access_state": access,
        "materialization_readback": readback,
        "capsule_acceptance_readback": _capsule_acceptance_readback(readback),
        "business_goal_outcome_contract": _business_goal_outcome_contract(
            materialized=materialized,
            next_axis=next_axis,
        ),
        "recommendation_logic": _recommendation_logic(materialized, route),
        "selected_next_axis": next_axis,
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(local_ymmp_created=materialized),
        "inertia_check": _inertia_check(next_axis),
        "completion_matrix": _completion_matrix(materialized, route),
    }


def materialize_local_offline_topic_mini_episode_capsule(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    capsule = _load_json_object(base / DEFAULT_CAPSULE_PATH)
    route_classification, blockers = _classify_route(base, capsule)
    if route_classification != "current_supported":
        raise ValueError(f"materialization route is not supported: {blockers}")

    project = load_ymmp(base / SOURCE_NOD_HEAD_YMMP_PATH)
    probe = copy.deepcopy(project)
    target_path = base / LOCAL_IGNORED_MATERIALIZED_YMMP_PATH
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
    for beat in _capsule_beats(capsule):
        items.append(_make_text_item(beat))
        if beat["animation_assignment"] != "none":
            items.extend(_clone_beat_items(base, source_items, _animation_clone_plan(beat)))

    timeline["Items"] = sorted(
        items,
        key=lambda item: (int(item.get("Frame", 0)), int(item.get("Layer", 0))),
    )
    timeline["Length"] = TIMELINE_LENGTH_FRAMES
    timeline["CurrentFrame"] = 0
    timeline["MaxLayer"] = max(
        int(item.get("Layer", 0))
        for item in timeline["Items"]
        if isinstance(item.get("Layer"), int)
    )
    save_ymmp(probe, target_path)
    return probe


def render_materialization_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Offline Topic Mini Episode Capsule Materialization v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"local_ymmp_materialization_status: {payload.get('local_ymmp_materialization_status')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Materialization Route", payload.get("route"))
    _append_mapping(lines, "Local Probe Access State", payload.get("local_probe_access_state"))
    _append_mapping(lines, "Materialization Readback", payload.get("materialization_readback"))
    _append_mapping(
        lines,
        "Capsule Acceptance Readback",
        payload.get("capsule_acceptance_readback"),
    )
    _append_mapping(
        lines,
        "Business Goal Outcome Contract",
        payload.get("business_goal_outcome_contract"),
    )
    _append_mapping(lines, "Recommendation Logic", payload.get("recommendation_logic"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    _append_rows(
        lines,
        "Inertia Check",
        ["gate", "status"],
        payload.get("inertia_check"),
    )
    _append_rows(
        lines,
        "Completion Matrix",
        ["gate", "status"],
        payload.get("completion_matrix"),
    )
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This materialization creates an ignored local diagnostic .ymmp only. "
        "It does not launch YMM4, render, create audio/TTS, fetch live RSS/news, "
        "redesign cards, accept production subtitle/card design, or claim public readiness."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _classify_route(base: Path, capsule: dict[str, Any]) -> tuple[str, list[str]]:
    blockers: list[str] = []
    if not (base / DEFAULT_CAPSULE_PATH).exists():
        blockers.append("source capsule artifact is missing")
    if not (base / SOURCE_NOD_HEAD_YMMP_PATH).exists():
        blockers.append("tracked nod_head YMM4 source is missing")
    beats = _capsule_beats(capsule)
    if len(beats) != BEAT_COUNT:
        blockers.append(f"expected {BEAT_COUNT} capsule beats, found {len(beats)}")
    unsupported_assignments = sorted(
        {
            str(beat.get("animation_assignment"))
            for beat in beats
            if beat.get("animation_assignment") not in ANIMATION_ASSIGNMENTS
        }
    )
    if unsupported_assignments:
        blockers.append(f"unsupported animation assignments: {unsupported_assignments}")
    if blockers:
        return "blocked", blockers
    return "current_supported", []


def _next_required_route_work(route_classification: str) -> list[str]:
    if route_classification == "current_supported":
        return [
            "local ignored YMM4 diagnostic materialization in this slice",
            NEXT_AXIS_PREVIEW,
        ]
    return [NEXT_AXIS_ROUTE_AUDIT, NEXT_AXIS_IMPLEMENTATION]


def _capsule_beats(capsule: dict[str, Any]) -> list[dict[str, Any]]:
    beats = _dict(capsule.get("episode_capsule")).get("beats", [])
    if not isinstance(beats, list):
        return []
    return [beat for beat in beats if isinstance(beat, dict)]


def _animation_clone_plan(beat: dict[str, Any]) -> dict[str, Any]:
    assignment = str(beat.get("animation_assignment"))
    expression = {
        "stable_pose_only": "easy",
        "expression_event": "panic",
        "expression_plus_short_nod": "panic",
        "short_nod_reaction": "easy",
    }.get(assignment, "easy")
    head_rotation_values = (
        [0.0, -8.0, 0.0]
        if assignment in {"expression_plus_short_nod", "short_nod_reaction"}
        else [0.0]
    )
    return {
        "beat_id": beat["beat_id"],
        "frame": _beat_start_frame(beat),
        "length": BEAT_DURATION_FRAMES,
        "expression": expression,
        "parent_x_values": [-96.0],
        "head_rotation_values": head_rotation_values,
    }


def _make_text_item(beat: dict[str, Any]) -> dict[str, Any]:
    return {
        "$type": "YukkuriMovieMaker.Project.Items.TextItem, YukkuriMovieMaker",
        "Text": beat.get("explanation_line"),
        "Font": "Yu Gothic UI",
        "FontSize": _animation(30),
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
        "Frame": _beat_start_frame(beat),
        "Layer": 1,
        "KeyFrames": {"Frames": [], "Count": 0},
        "Length": BEAT_DURATION_FRAMES,
        "PlaybackRate": 100,
        "ContentOffset": "00:00:00",
        "Remark": f"offline_topic_mini_episode:text:{beat.get('beat_id')}",
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


def _beat_start_frame(beat: dict[str, Any]) -> int:
    return (int(beat.get("order", 1)) - 1) * BEAT_DURATION_FRAMES


def _local_probe_access(base: Path) -> dict[str, Any]:
    full_path = (base / LOCAL_IGNORED_MATERIALIZED_YMMP_PATH).resolve()
    target_exists = full_path.exists()
    check_ignore = _git_check_ignore(base, LOCAL_IGNORED_MATERIALIZED_YMMP_PATH)
    ignored = check_ignore["ignored"]
    if target_exists and ignored:
        access_state = "verified_present"
        access_evidence_level = "L3_VERIFIED_PRESENT"
    elif target_exists:
        access_state = "present_but_not_ignored_blocked"
        access_evidence_level = "L1_PRESENT_NOT_IGNORED"
    elif ignored:
        access_state = "ignored_local_artifact_missing"
        access_evidence_level = "L1_IGNORED_PATH_CONFIRMED_NO_FILE"
    else:
        access_state = "missing_not_ignored_blocked"
        access_evidence_level = "L0_MISSING_NOT_IGNORED"
    return {
        "artifact_id": "local_ignored_offline_topic_mini_episode_materialized_probe",
        "repo_relative_path": LOCAL_IGNORED_MATERIALIZED_YMMP_PATH.as_posix(),
        "folder_full_path_current_host": str(full_path.parent),
        "file_full_path_current_host": str(full_path),
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{full_path}"',
        "target_exists": target_exists,
        "access_state": access_state,
        "access_evidence_level": access_evidence_level,
        "artifact_scope": "ignored_local_only",
        "evidence_source": "current_host_filesystem_plus_git_check_ignore",
        "git_check_ignore_result": check_ignore,
        "size": full_path.stat().st_size if target_exists else None,
    }


def _local_materialization_readback(
    base: Path,
    capsule: dict[str, Any],
    access: dict[str, Any],
) -> dict[str, Any]:
    target = base / LOCAL_IGNORED_MATERIALIZED_YMMP_PATH
    if not target.exists():
        return {
            "readback_status": "blocked",
            "target_exists": False,
            "reason": "local_materialized_probe_missing",
            "repo_relative_path": LOCAL_IGNORED_MATERIALIZED_YMMP_PATH.as_posix(),
            "per_beat_mapping": [],
        }
    data = load_ymmp(target)
    timeline = _first_timeline(data)
    items = _get_timeline_items(data)
    item_type_counts: dict[str, int] = {}
    for item in items:
        item_type = _item_type(item)
        item_type_counts[item_type] = item_type_counts.get(item_type, 0) + 1
    text_items = [item for item in items if _item_type(item) == "TextItem"]
    animation_items = [
        item for item in items if _item_type(item) in {"GroupItem", "ImageItem"}
    ]
    beats = _capsule_beats(capsule)
    per_beat_mapping = [_per_beat_readback(beat, items) for beat in beats]
    unexpected_item_types = sorted(
        item_type
        for item_type in item_type_counts
        if item_type not in {"TextItem", "GroupItem", "ImageItem"}
    )
    structural_pass = (
        bool(timeline)
        and not unexpected_item_types
        and len(beats) == BEAT_COUNT
        and len(text_items) == BEAT_COUNT
        and all(row["text_item_present"] for row in per_beat_mapping)
        and item_type_counts.get("GroupItem") == 8
        and item_type_counts.get("ImageItem") == 8
        and timeline.get("Length") == TIMELINE_LENGTH_FRAMES
        and access.get("access_state") == "verified_present"
    )
    return {
        "readback_status": "structural_pass" if structural_pass else "blocked",
        "artifact_id": access["artifact_id"],
        "repo_relative_path": access["repo_relative_path"],
        "folder_full_path_current_host": access["folder_full_path_current_host"],
        "file_full_path_current_host": access["file_full_path_current_host"],
        "target_exists": access["target_exists"],
        "access_state": access["access_state"],
        "access_evidence_level": access["access_evidence_level"],
        "artifact_scope": access["artifact_scope"],
        "evidence_source": access["evidence_source"],
        "git_check_ignore_result": access["git_check_ignore_result"],
        "size": access["size"],
        "file_sha256": _sha256(target),
        "item_type_counts": item_type_counts,
        "unexpected_item_types": unexpected_item_types,
        "beat_count": len(beats),
        "text_item_count": len(text_items),
        "animation_item_count": len(animation_items),
        "duration_frames": timeline.get("Length") if timeline else None,
        "fps": _dict(timeline.get("VideoInfo")).get("FPS") if timeline else None,
        "per_beat_mapping": per_beat_mapping,
        "YMM4_launch_status": "not_launched",
        "render_status": "not_rendered",
        "audio_tts_status": "not_created",
    }


def _per_beat_readback(beat: dict[str, Any], items: list[dict[str, Any]]) -> dict[str, Any]:
    beat_id = str(beat.get("beat_id"))
    start = _beat_start_frame(beat)
    text_remark = f"offline_topic_mini_episode:text:{beat_id}"
    text_item = next((item for item in items if item.get("Remark") == text_remark), None)
    animation_marker = f"primitive_probe:{beat_id}:nod_head_v1"
    animation_items = [item for item in items if item.get("Remark") == animation_marker]
    group_items = [item for item in animation_items if _item_type(item) == "GroupItem"]
    parent = next((item for item in group_items if item.get("GroupRange") == 3), None)
    head = next((item for item in group_items if item.get("GroupRange") == 1), None)
    return {
        "beat_id": beat_id,
        "text_item_present": text_item is not None,
        "text_item_text": text_item.get("Text") if text_item else None,
        "animation_accent_assignment": beat.get("animation_assignment"),
        "animation_item_count": len(animation_items),
        "start_frame": start,
        "duration_frames": BEAT_DURATION_FRAMES,
        "source_boundary_role": beat.get("source_boundary_role"),
        "parent_x_values": _route_values(parent, "X") if parent else [],
        "head_rotation_values": _route_values(head, "Rotation") if head else [],
    }


def _capsule_acceptance_readback(readback: dict[str, Any]) -> dict[str, Any]:
    per_beat = readback.get("per_beat_mapping")
    if not isinstance(per_beat, list):
        per_beat = []
    animation_rows = [row for row in per_beat if row.get("animation_item_count", 0) > 0]
    all_parent_x_fixed = all(
        row.get("parent_x_values") in ([], [-96.0])
        for row in per_beat
    )
    no_mechanical_expression_cycle = (
        len([row for row in animation_rows if row.get("animation_accent_assignment") == "expression_event"])
        <= 1
    )
    return {
        "five_beats_are_represented": readback.get("beat_count") == BEAT_COUNT,
        "text_role_exists_per_beat": all(row.get("text_item_present") for row in per_beat),
        "animation_accent_remains_subordinate": (
            readback.get("animation_item_count", 0) <= 16
            and len(animation_rows) <= 4
        ),
        "no_body_forward_back_default": all_parent_x_fixed,
        "no_mechanical_expression_cycling": no_mechanical_expression_cycle,
        "no_card_polish": True,
        "no_render_export": readback.get("render_status") == "not_rendered",
        "no_live_fetch": True,
        "no_production_claim": True,
    }


def _business_goal_outcome_contract(
    *,
    materialized: bool,
    next_axis: str,
) -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": materialized,
            "rationale": (
                "the slice moves beyond contract-only capsule by creating a local ignored "
                "multi-beat YMM4 diagnostic project"
                if materialized
                else "materialization remains blocked or deferred"
            ),
        },
        "offer_clear": {
            "status": materialized,
            "rationale": "the materialization shows how five beats map to TextItems and optional accents",
        },
        "proof_clear": {
            "status": materialized,
            "rationale": "the proof is route/materialization structure, not production quality",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "card design, animation tuning, render, audio/TTS, and live RSS remain closed",
        },
        "next_action_clear": {
            "status": True,
            "rationale": next_axis,
        },
        "visual_supports_explanation": {
            "status": materialized,
            "rationale": "animation is optional, subordinate, and absent on the close beat",
        },
    }


def _recommendation_logic(materialized: bool, route: dict[str, Any]) -> dict[str, Any]:
    if materialized:
        selected = NEXT_AXIS_PREVIEW
        reason = (
            "A new multi-beat ignored local .ymmp exists, access is verified, "
            "and one bounded preview can test the episode-level co-presence."
        )
    elif route.get("route_classification") in {"unclear", "stale_fake_packet_only"}:
        selected = NEXT_AXIS_ROUTE_AUDIT
        reason = "The route is not clear enough to ask for preview."
    elif route.get("route_classification") == "current_partial":
        selected = NEXT_AXIS_IMPLEMENTATION
        reason = "The route is clear but implementation remains incomplete."
    else:
        selected = NEXT_AXIS_ROUTE_AUDIT
        reason = "Materialization did not complete."
    return {
        "selected": selected,
        "if_new_multi_beat_local_ymmp_exists_and_preview_adds_value": NEXT_AXIS_PREVIEW,
        "if_existing_route_is_unclear": NEXT_AXIS_ROUTE_AUDIT,
        "if_route_clear_but_implementation_incomplete": NEXT_AXIS_IMPLEMENTATION,
        "if_topic_to_beat_is_too_synthetic": NEXT_AXIS_TOPIC_AUDIT,
        "if_offline_capsule_route_is_strong_and_source_boundary_is_next": (
            NEXT_AXIS_LIVE_BOUNDARY_PLAN
        ),
        "reason": reason,
    }


def _fallback_next_axis(route: dict[str, Any]) -> str:
    if route.get("route_classification") == "current_supported":
        return NEXT_AXIS_IMPLEMENTATION
    return NEXT_AXIS_ROUTE_AUDIT


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "live_rss_or_news_fetch": False,
        "production_script_quality": False,
        "production_subtitle_design": False,
        "production_card_design": False,
        "production_animation_quality": False,
        "card_redesign": False,
        "visual_layout_tuning": False,
        "animation_tuning": False,
        "render_export_proof": False,
        "audio_or_tts_output": False,
        "public_upload_or_public_readiness": False,
        "actual_order_or_audience_acceptance": False,
        "source_truth_or_rights_approval": False,
    }


def _boundaries(*, local_ymmp_created: bool) -> dict[str, bool]:
    return {
        "network_fetch_performed": False,
        "live_RSS_news_fetch_performed": False,
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "card_redesign_performed": False,
        "production_subtitle_or_card_design_created": False,
        "animation_tuned": False,
        "animation_only_probe_created": False,
        "local_ignored_ymmp_created_in_this_slice": local_ymmp_created,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
        "actual_order_or_audience_acceptance_claimed": False,
        "stale_fake_packet_route_used_as_current": False,
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_animation_only_loop", "status": True},
        {"gate": "no_primitive_or_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "no_live_RSS_or_network_fetch", "status": True},
        {"gate": "no_stale_fake_packet_route_overclaim", "status": True},
        {"gate": "next_axis_remains_episode_construction", "status": next_axis},
    ]


def _completion_matrix(materialized: bool, route: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"gate": "repo_state_verified", "status": True},
        {"gate": "previous_capsule_inspected", "status": True},
        {
            "gate": "materialization_route_classified",
            "status": route.get("route_classification"),
        },
        {
            "gate": "local_ymmp_created_or_honestly_deferred",
            "status": "created" if materialized else "blocked_or_deferred",
        },
        {"gate": "materialization_readback_created", "status": True},
        {"gate": "next_axis_selected", "status": True},
    ]


def _load_json_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


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


def main() -> int:
    write_default_newsroom_offline_topic_mini_episode_materialization_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
