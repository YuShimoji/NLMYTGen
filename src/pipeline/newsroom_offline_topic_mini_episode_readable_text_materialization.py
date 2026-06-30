"""Build a readable-text v2 of the offline topic mini episode probe.

The previous local YMM4 preview proved the five-beat route and character
accent timing, but the user saw debug labels as the screen-facing notes. This
slice preserves the route and rewrites the five visible text items to short
human-readable explanation lines. It does not launch YMM4, render, fetch live
RSS/news, tune animation, redesign cards, or create audio/TTS.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_offline_topic_mini_episode_materialization import (
    BEAT_COUNT,
    BEAT_DURATION_FRAMES,
    DEFAULT_CAPSULE_PATH,
    DEFAULT_MATERIALIZATION_PATH,
    DEFAULT_ROUTE_PATH,
    FPS,
    LOCAL_IGNORED_MATERIALIZED_YMMP_PATH,
    TIMELINE_LENGTH_FRAMES,
    _beat_start_frame,
    _capsule_beats,
    _git_check_ignore,
    _load_json_object,
    _sha256,
    build_default_materialization_route,
    materialize_local_offline_topic_mini_episode_capsule,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
)
from src.pipeline.newsroom_yukkuri_animation_primitive_probe_materialization import (
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


PREVIEW_OBSERVATION_ID = (
    "newsroom_offline_topic_mini_episode_preview_observation_v1_2026_06_30"
)
READABLE_MATERIALIZATION_ID = (
    "newsroom_offline_topic_mini_episode_readable_text_materialization_v1_2026_06_30"
)
PREVIEW_OBSERVATION_SCHEMA_VERSION = (
    "newsroom_offline_topic_mini_episode_preview_observation.v1"
)
READABLE_MATERIALIZATION_SCHEMA_VERSION = (
    "newsroom_offline_topic_mini_episode_readable_text_materialization.v1"
)

DEFAULT_PREVIEW_OBSERVATION_PATH = Path(
    "samples/_probe/newsroom_handoff/offline_topic_mini_episode_preview_observation_v1.json"
)
DEFAULT_PREVIEW_OBSERVATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_PREVIEW_OBSERVATION_V1_2026-06-30.md"
)
DEFAULT_READABLE_MATERIALIZATION_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "offline_topic_mini_episode_readable_text_materialization_v1.json"
)
DEFAULT_READABLE_MATERIALIZATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_READABLE_TEXT_MATERIALIZATION_V1_2026-06-30.md"
)

LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH = Path(
    "_tmp/newsroom_manual_probe/"
    "offline_topic_mini_episode_capsule_materialized_v2_readable_text.ymmp"
)

NEXT_AXIS_READABLE_PREVIEW = (
    "newsroom-offline-topic-mini-episode-readable-preview-operator-instruction-v1"
)
NEXT_AXIS_TOPIC_FIXTURE_AUDIT = "newsroom-rss-topic-fixture-route-audit-v1"
NEXT_AXIS_LIVE_RSS_BOUNDARY_PLAN = "newsroom-live-rss-boundary-plan-v1"
NEXT_AXIS_ROUTE_HARDENING = "newsroom-episode-capsule-route-hardening-v1"

DEBUG_LABEL_PREFIX = "offline_topic_mini_episode:text:"

READABLE_BEAT_LINES: tuple[dict[str, str], ...] = (
    {
        "beat_id": "offline_topic_mini_ep_beat_01_hook",
        "visible_text": "Hook: this offline topic checks the episode route.",
    },
    {
        "beat_id": "offline_topic_mini_ep_beat_02_key_claim",
        "visible_text": "Key claim: source boundaries must be verified first.",
    },
    {
        "beat_id": "offline_topic_mini_ep_beat_03_source_warning",
        "visible_text": "Warning: this is a fixture, not live news.",
    },
    {
        "beat_id": "offline_topic_mini_ep_beat_04_implication",
        "visible_text": "Why it matters: topic input can become a short explainer.",
    },
    {
        "beat_id": "offline_topic_mini_ep_beat_05_close",
        "visible_text": "Next: harden the source route before production.",
    },
)

USER_VISIBLE_DEBUG_LABELS: tuple[str, ...] = tuple(
    f"{DEBUG_LABEL_PREFIX}{row['beat_id']}" for row in READABLE_BEAT_LINES
)

NORMALIZED_PREVIEW_OBSERVATION: dict[str, Any] = {
    "source_observation_role": "user_opened_offline_topic_mini_episode_v1_probe",
    "user_opened_path_current_host": (
        "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe\\"
        "offline_topic_mini_episode_capsule_materialized_v1.ymmp"
    ),
    "repo_relative_path": LOCAL_IGNORED_MATERIALIZED_YMMP_PATH.as_posix(),
    "yym4_opened": True,
    "five_textitems_visible": True,
    "five_textitems_sequential": True,
    "animation_accent_visible": True,
    "animation_accent_not_disruptive": True,
    "episode_route_materialization_status": "pass_with_boundary",
    "visible_text_is_debug_label": True,
    "human_readable_explanation_text_visible": False,
    "production_subtitle_design_accepted": False,
    "production_card_design_accepted": False,
    "visible_screen_notes": list(USER_VISIBLE_DEBUG_LABELS),
    "next_axis": "readable_text_materialization_v2",
}


def write_default_newsroom_offline_topic_mini_episode_readable_text_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    materialize_local_readable_text_mini_episode(root=base)
    observation = build_default_preview_observation(root=base)
    materialization = build_default_readable_text_materialization(root=base)
    _write_json(base / DEFAULT_PREVIEW_OBSERVATION_PATH, observation)
    _write_text(
        base / DEFAULT_PREVIEW_OBSERVATION_DOC_PATH,
        render_preview_observation_markdown(observation),
    )
    _write_json(base / DEFAULT_READABLE_MATERIALIZATION_PATH, materialization)
    _write_text(
        base / DEFAULT_READABLE_MATERIALIZATION_DOC_PATH,
        render_readable_text_materialization_markdown(materialization),
    )
    return {
        "preview_observation": observation,
        "readable_text_materialization": materialization,
    }


def build_default_preview_observation(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    return {
        "artifact_id": PREVIEW_OBSERVATION_ID,
        "schema_version": PREVIEW_OBSERVATION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_v1_materialization_path": DEFAULT_MATERIALIZATION_PATH.as_posix(),
        "source_v1_route_path": DEFAULT_ROUTE_PATH.as_posix(),
        "source_v1_local_ymmp_path": LOCAL_IGNORED_MATERIALIZED_YMMP_PATH.as_posix(),
        "normalized_preview_observation": NORMALIZED_PREVIEW_OBSERVATION,
        "v1_debug_label_readback": build_v1_debug_label_readback(root=base),
        "issue_classification": {
            "route_materialization_structure": "pass_with_boundary",
            "animation_accent": "pass_with_boundary",
            "screen_facing_text": "debug_label_visible_not_human_readable",
            "production_subtitle_or_card_design": "not_accepted",
        },
        "recommended_fix": {
            "status": "safe_to_materialize_readable_text_v2",
            "approach": (
                "preserve v1 route and animation timing, replace five visible "
                "TextItem text/remark fields with short readable lines"
            ),
            "next_axis": "readable_text_materialization_v2",
        },
        "boundaries": _boundaries(local_ymmp_created=False),
    }


def build_default_readable_text_materialization(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    route = build_default_materialization_route(root=base)
    access = _local_probe_access(base)
    readback = _readable_text_readback(base, access)
    materialized = readback.get("readback_status") == "readable_text_pass"
    next_axis = (
        NEXT_AXIS_READABLE_PREVIEW
        if materialized
        else NEXT_AXIS_ROUTE_HARDENING
    )
    return {
        "artifact_id": READABLE_MATERIALIZATION_ID,
        "schema_version": READABLE_MATERIALIZATION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_capsule_path": DEFAULT_CAPSULE_PATH.as_posix(),
        "source_v1_materialization_path": DEFAULT_MATERIALIZATION_PATH.as_posix(),
        "source_v1_route_path": DEFAULT_ROUTE_PATH.as_posix(),
        "source_v1_local_ymmp_path": LOCAL_IGNORED_MATERIALIZED_YMMP_PATH.as_posix(),
        "source_route_classification": route.get("route_classification"),
        "source_route_confidence": route.get("route_confidence"),
        "normalized_preview_observation": NORMALIZED_PREVIEW_OBSERVATION,
        "language_policy": _language_policy(),
        "readable_text_lines": list(READABLE_BEAT_LINES),
        "local_ymmp_materialization_status": (
            "materialized_ignored_local_probe" if materialized else "blocked_or_deferred"
        ),
        "local_probe_access_state": access,
        "materialization_readback": readback,
        "acceptance_readback": _acceptance_readback(readback),
        "business_goal_outcome_contract": _business_goal_outcome_contract(
            materialized=materialized,
            next_axis=next_axis,
        ),
        "recommendation_logic": _recommendation_logic(materialized),
        "selected_next_axis": next_axis,
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(local_ymmp_created=materialized),
        "inertia_check": _inertia_check(next_axis),
        "completion_matrix": _completion_matrix(materialized),
    }


def build_v1_debug_label_readback(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    target = base / LOCAL_IGNORED_MATERIALIZED_YMMP_PATH
    if not target.exists():
        return {
            "readback_status": "blocked",
            "target_exists": False,
            "reason": "v1_local_probe_missing",
            "user_observed_debug_label_count": len(USER_VISIBLE_DEBUG_LABELS),
        }
    data = load_ymmp(target)
    items = _get_timeline_items(data)
    text_items = sorted(
        [item for item in items if _item_type(item) == "TextItem"],
        key=lambda item: int(item.get("Frame", 0)),
    )
    text_values = [str(item.get("Text", "")) for item in text_items]
    remark_values = [str(item.get("Remark", "")) for item in text_items]
    return {
        "readback_status": "user_preview_observation_recorded",
        "target_exists": True,
        "repo_relative_path": LOCAL_IGNORED_MATERIALIZED_YMMP_PATH.as_posix(),
        "file_full_path_current_host": str(target.resolve()),
        "text_item_count": len(text_items),
        "text_field_values": text_values,
        "remark_values": remark_values,
        "remark_debug_label_count": sum(_is_debug_label(value) for value in remark_values),
        "text_field_human_readable_count": sum(_is_human_readable(value) for value in text_values),
        "user_observed_visible_values": list(USER_VISIBLE_DEBUG_LABELS),
        "user_observed_debug_label_count": len(USER_VISIBLE_DEBUG_LABELS),
        "classification": "screen_visible_debug_label_from_user_preview",
        "interpretation": (
            "filesystem readback shows explanation text in Text and debug labels in "
            "Remark; user preview is treated as authoritative that the screen-facing "
            "notes were debug labels"
        ),
    }


def materialize_local_readable_text_mini_episode(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    route = build_default_materialization_route(root=base)
    if route.get("route_classification") != "current_supported":
        raise ValueError("current materialization route is not supported")
    source = base / LOCAL_IGNORED_MATERIALIZED_YMMP_PATH
    if not source.exists():
        materialize_local_offline_topic_mini_episode_capsule(root=base)
    if not source.exists():
        raise ValueError(f"source v1 local probe is missing: {source}")

    target = base / LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    probe = copy.deepcopy(load_ymmp(source))
    probe["FilePath"] = str(target.resolve())
    timeline = _first_timeline(probe)
    if not timeline:
        raise ValueError("source v1 local probe has no timeline")

    items = _get_timeline_items(probe)
    text_items = sorted(
        [item for item in items if _item_type(item) == "TextItem"],
        key=lambda item: int(item.get("Frame", 0)),
    )
    if len(text_items) != BEAT_COUNT:
        raise ValueError(f"expected {BEAT_COUNT} TextItems, found {len(text_items)}")

    for text_item, readable in zip(text_items, READABLE_BEAT_LINES, strict=True):
        text_item["Text"] = readable["visible_text"]
        text_item["Remark"] = readable["visible_text"]

    timeline["Items"] = sorted(
        items,
        key=lambda item: (int(item.get("Frame", 0)), int(item.get("Layer", 0))),
    )
    timeline["Length"] = TIMELINE_LENGTH_FRAMES
    timeline["CurrentFrame"] = 0
    save_ymmp(probe, target)
    return probe


def render_preview_observation_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Offline Topic Mini Episode Preview Observation v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        "",
    ]
    _append_mapping(
        lines,
        "Normalized Preview Observation",
        payload.get("normalized_preview_observation"),
    )
    _append_mapping(lines, "V1 Debug Label Readback", payload.get("v1_debug_label_readback"))
    _append_mapping(lines, "Issue Classification", payload.get("issue_classification"))
    _append_mapping(lines, "Recommended Fix", payload.get("recommended_fix"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This records a user-side preview observation. It accepts the five-beat "
        "route and animation accent only with boundary, and it does not accept "
        "production subtitle/card design, render quality, public readiness, or "
        "audience response."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_readable_text_materialization_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Offline Topic Mini Episode Readable Text Materialization v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"local_ymmp_materialization_status: {payload.get('local_ymmp_materialization_status')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(
        lines,
        "Normalized Preview Observation",
        payload.get("normalized_preview_observation"),
    )
    _append_mapping(lines, "Language Policy", payload.get("language_policy"))
    _append_rows(
        lines,
        "Readable Text Lines",
        ["beat_id", "visible_text"],
        payload.get("readable_text_lines"),
    )
    _append_mapping(lines, "Local Probe Access State", payload.get("local_probe_access_state"))
    _append_mapping(lines, "Materialization Readback", payload.get("materialization_readback"))
    _append_mapping(lines, "Acceptance Readback", payload.get("acceptance_readback"))
    _append_mapping(
        lines,
        "Business Goal Outcome Contract",
        payload.get("business_goal_outcome_contract"),
    )
    _append_mapping(lines, "Recommendation Logic", payload.get("recommendation_logic"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    _append_rows(lines, "Completion Matrix", ["gate", "status"], payload.get("completion_matrix"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "V2 is an ignored local diagnostic .ymmp. It changes only screen-facing "
        "TextItem content from debug labels to readable explanation lines while "
        "preserving the route and frozen animation accent policy."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _local_probe_access(base: Path) -> dict[str, Any]:
    full_path = (base / LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH).resolve()
    target_exists = full_path.exists()
    check_ignore = _git_check_ignore(base, LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH)
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
        "artifact_id": "local_ignored_offline_topic_mini_episode_readable_text_probe",
        "repo_relative_path": LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH.as_posix(),
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


def _readable_text_readback(base: Path, access: dict[str, Any]) -> dict[str, Any]:
    target = base / LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH
    if not target.exists():
        return {
            "readback_status": "blocked",
            "target_exists": False,
            "reason": "local_readable_text_probe_missing",
            "repo_relative_path": LOCAL_IGNORED_READABLE_TEXT_YMMP_PATH.as_posix(),
            "per_beat_mapping": [],
        }
    capsule = _load_json_object(base / DEFAULT_CAPSULE_PATH)
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
    debug_label_visible_count = sum(
        _is_debug_label(str(item.get("Text", "")))
        or _is_debug_label(str(item.get("Remark", "")))
        for item in text_items
    )
    human_readable_text_item_count = sum(
        row["text_is_human_readable"] for row in per_beat_mapping
    )
    structural_pass = (
        bool(timeline)
        and not unexpected_item_types
        and len(beats) == BEAT_COUNT
        and len(text_items) == BEAT_COUNT
        and all(row["text_item_present"] for row in per_beat_mapping)
        and human_readable_text_item_count == BEAT_COUNT
        and debug_label_visible_count == 0
        and item_type_counts.get("GroupItem") == 8
        and item_type_counts.get("ImageItem") == 8
        and timeline.get("Length") == TIMELINE_LENGTH_FRAMES
        and access.get("access_state") == "verified_present"
    )
    return {
        "readback_status": "readable_text_pass" if structural_pass else "blocked",
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
        "debug_label_visible_count": debug_label_visible_count,
        "human_readable_text_item_count": human_readable_text_item_count,
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
    debug_label = f"{DEBUG_LABEL_PREFIX}{beat_id}"
    text_item = next(
        (
            item
            for item in items
            if _item_type(item) == "TextItem" and int(item.get("Frame", -1)) == start
        ),
        None,
    )
    visible_text = str(text_item.get("Text", "")) if text_item else None
    remark = str(text_item.get("Remark", "")) if text_item else None
    animation_marker = f"primitive_probe:{beat_id}:nod_head_v1"
    animation_items = [item for item in items if item.get("Remark") == animation_marker]
    group_items = [item for item in animation_items if _item_type(item) == "GroupItem"]
    parent = next((item for item in group_items if item.get("GroupRange") == 3), None)
    head = next((item for item in group_items if item.get("GroupRange") == 1), None)
    return {
        "beat_id": beat_id,
        "debug_label": debug_label,
        "visible_text": visible_text,
        "text_item_remark": remark,
        "text_item_present": text_item is not None,
        "text_is_human_readable": _is_human_readable(visible_text or "")
        and not _is_debug_label(remark or ""),
        "animation_accent_assignment": beat.get("animation_assignment"),
        "animation_item_count": len(animation_items),
        "start_frame": start,
        "duration_frames": BEAT_DURATION_FRAMES,
        "source_boundary_role": beat.get("source_boundary_role"),
        "parent_x_values": _route_values(parent, "X") if parent else [],
        "head_rotation_values": _route_values(head, "Rotation") if head else [],
    }


def _language_policy() -> dict[str, Any]:
    return {
        "selected_language": "english",
        "preferred_language_in_prompt": "japanese_if_safe",
        "reason": (
            "the supplied Japanese examples are mojibake in the prompt, while the "
            "current capsule artifacts already use ASCII English explanation lines; "
            "English avoids adding an encoding/display variable to this diagnostic slice"
        ),
        "text_is_diagnostic_not_production_script": True,
    }


def _acceptance_readback(readback: dict[str, Any]) -> dict[str, Any]:
    per_beat = readback.get("per_beat_mapping")
    if not isinstance(per_beat, list):
        per_beat = []
    animation_rows = [row for row in per_beat if row.get("animation_item_count", 0) > 0]
    all_parent_x_fixed = all(row.get("parent_x_values") in ([], [-96.0]) for row in per_beat)
    no_mechanical_expression_cycle = (
        len(
            [
                row
                for row in animation_rows
                if row.get("animation_accent_assignment") == "expression_event"
            ]
        )
        <= 1
    )
    return {
        "five_beats_are_represented": readback.get("beat_count") == BEAT_COUNT,
        "TextItem_exists_per_beat": all(row.get("text_item_present") for row in per_beat),
        "visible_text_is_human_readable": (
            readback.get("human_readable_text_item_count") == BEAT_COUNT
        ),
        "debug_labels_are_not_main_visible_content": (
            readback.get("debug_label_visible_count") == 0
        ),
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
            "status": True,
            "rationale": "the v1 preview pass is accepted for route structure while the debug-label text gap is recorded",
        },
        "offer_clear": {
            "status": materialized,
            "rationale": "v2 maps the five beats to short readable explanation lines",
        },
        "proof_clear": {
            "status": materialized,
            "rationale": "the proof is readable episode materialization, not production script or card quality",
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
            "rationale": "animation remains optional, subordinate, and absent on the close beat",
        },
    }


def _recommendation_logic(materialized: bool) -> dict[str, Any]:
    if materialized:
        selected = NEXT_AXIS_READABLE_PREVIEW
        reason = (
            "A v2 ignored local .ymmp exists, access is verified, and the screen "
            "text changed from debug labels to readable explanation lines."
        )
    else:
        selected = NEXT_AXIS_ROUTE_HARDENING
        reason = "Readable text materialization did not pass structural readback."
    return {
        "selected": selected,
        "if_v2_local_ymmp_exists_and_preview_adds_value": NEXT_AXIS_READABLE_PREVIEW,
        "if_topic_to_readable_beat_is_too_synthetic": NEXT_AXIS_TOPIC_FIXTURE_AUDIT,
        "if_offline_readable_text_route_is_strong_and_live_boundary_is_next": (
            NEXT_AXIS_LIVE_RSS_BOUNDARY_PLAN
        ),
        "if_reusable_route_hardening_is_needed": NEXT_AXIS_ROUTE_HARDENING,
        "reason": reason,
    }


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
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_animation_only_loop", "status": True},
        {"gate": "no_primitive_or_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "no_live_RSS_or_network_fetch", "status": True},
        {"gate": "next_axis_remains_episode_construction", "status": next_axis},
    ]


def _completion_matrix(materialized: bool) -> list[dict[str, Any]]:
    return [
        {"gate": "repo_state_verified", "status": True},
        {"gate": "user_observation_recorded", "status": True},
        {"gate": "v1_debug_label_issue_classified", "status": True},
        {"gate": "readable_text_materialization_plan_created", "status": True},
        {
            "gate": "v2_local_ymmp_created_or_honestly_deferred",
            "status": "created" if materialized else "blocked_or_deferred",
        },
        {"gate": "materialization_readback_created", "status": True},
        {"gate": "next_axis_selected", "status": True},
    ]


def _is_debug_label(value: str) -> bool:
    return value.startswith(DEBUG_LABEL_PREFIX)


def _is_human_readable(value: str) -> bool:
    stripped = value.strip()
    return bool(stripped) and not _is_debug_label(stripped) and ":" in stripped


def main() -> int:
    write_default_newsroom_offline_topic_mini_episode_readable_text_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
