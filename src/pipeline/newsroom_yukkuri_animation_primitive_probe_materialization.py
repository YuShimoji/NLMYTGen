"""Materialize the first newsroom yukkuri animation primitive probe.

This slice creates an ignored local YMM4 probe by copying tracked
repo-local proof/template material and changing only bounded timing,
asset-path, and transform fields. It does not launch YMM4, render,
create audio/TTS, fetch external media, or claim production quality.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_yukkuri_animation_primitive_proof import (
    DEFAULT_PROOF_DOC_PATH,
    DEFAULT_PROOF_PATH,
    DEFAULT_SCENE_BEAT_DOC_PATH,
    DEFAULT_SCENE_BEAT_PATH,
    LOCAL_IGNORED_PROBE_PATH,
    NEXT_AXIS_RENDER_SMOKE,
    SELECTED_PRIMITIVES,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp, save_ymmp


MATERIALIZATION_ID = (
    "newsroom_yukkuri_animation_primitive_probe_materialization_v1_2026_06_28"
)
MATERIALIZATION_SCHEMA_VERSION = (
    "newsroom_yukkuri_animation_primitive_probe_materialization.v1"
)

DEFAULT_MATERIALIZATION_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "yukkuri_animation_primitive_probe_materialization_v1.json"
)
DEFAULT_MATERIALIZATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_YUKKURI_ANIMATION_PRIMITIVE_PROBE_MATERIALIZATION_V1_2026-06-28.md"
)

SOURCE_NOD_HEAD_YMMP_PATH = Path("samples/nod_head.ymmp")
BODY_SOURCE_PATH = Path(
    "samples/characterAnimSample/"
    "Gemini_Generated_Image_kfezhpkfezhpkfez-removebg-preview.png"
)
EXPRESSION_PATHS = {
    "easy": Path("samples/characterAnimSample/reimu_easy.png"),
    "anger": Path("samples/characterAnimSample/reimu_anger.png"),
    "panic": Path("samples/characterAnimSample/reimu_panic.png"),
}

FPS = 60
BEAT_LENGTH_FRAMES = 720
TIMELINE_LENGTH_FRAMES = BEAT_LENGTH_FRAMES * 5
PROVEN_PRIMITIVES = [
    "head_nod",
    "expression_swap",
    "character_entrance_exit",
    "small_position_move",
]
OMITTED_PRIMITIVES = {
    "speech_balloon": (
        "omitted from the local .ymmp because the previous proof classified it "
        "as partial: ShapeItem/TextItem routes exist, but no dedicated balloon "
        "template or visual pass exists yet"
    )
}

BEAT_PLAN: list[dict[str, Any]] = [
    {
        "beat_id": "probe_beat_01_enter_question",
        "frame": 0,
        "length": BEAT_LENGTH_FRAMES,
        "timing_range": "0-12 sec",
        "scene_function": "viewer_question_reaction",
        "expression": "panic",
        "primitive_ids": ["character_entrance_exit", "expression_swap"],
        "parent_x_values": [-520.0, -120.0, -80.0],
        "head_rotation_values": [0.0],
        "motion_label": "enter_from_left",
    },
    {
        "beat_id": "probe_beat_02_nod_response",
        "frame": BEAT_LENGTH_FRAMES,
        "length": BEAT_LENGTH_FRAMES,
        "timing_range": "12-24 sec",
        "scene_function": "explanation_response",
        "expression": "easy",
        "primitive_ids": ["head_nod", "small_position_move"],
        "parent_x_values": [-80.0, -48.0, -80.0],
        "head_rotation_values": [0.0, -8.0, 0.0],
        "motion_label": "small_nudge_right",
    },
    {
        "beat_id": "probe_beat_03_emphasis_nudge",
        "frame": BEAT_LENGTH_FRAMES * 2,
        "length": BEAT_LENGTH_FRAMES,
        "timing_range": "24-36 sec",
        "scene_function": "proof_emphasis",
        "expression": "anger",
        "primitive_ids": ["expression_swap", "small_position_move"],
        "parent_x_values": [-80.0, -116.0, -80.0],
        "head_rotation_values": [0.0],
        "motion_label": "small_nudge_left",
    },
    {
        "beat_id": "probe_beat_04_boundary_warning",
        "frame": BEAT_LENGTH_FRAMES * 3,
        "length": BEAT_LENGTH_FRAMES,
        "timing_range": "36-48 sec",
        "scene_function": "boundary_warning",
        "expression": "panic",
        "primitive_ids": ["expression_swap", "small_position_move"],
        "parent_x_values": [-80.0, -60.0, -80.0],
        "head_rotation_values": [0.0],
        "motion_label": "small_nudge_center",
    },
    {
        "beat_id": "probe_beat_05_exit_close",
        "frame": BEAT_LENGTH_FRAMES * 4,
        "length": BEAT_LENGTH_FRAMES,
        "timing_range": "48-60 sec",
        "scene_function": "next_action_close",
        "expression": "easy",
        "primitive_ids": ["character_entrance_exit", "head_nod"],
        "parent_x_values": [-80.0, -120.0, -520.0],
        "head_rotation_values": [0.0, -6.0, 0.0],
        "motion_label": "exit_left",
    },
]


def write_default_newsroom_yukkuri_animation_primitive_probe_materialization_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write tracked readback artifacts and the ignored local probe .ymmp."""
    base = Path(root) if root is not None else Path(".")
    materialize_local_primitive_probe_ymmp(root=base)
    payload = build_default_newsroom_yukkuri_animation_primitive_probe_materialization(
        root=base
    )
    _write_json(base / DEFAULT_MATERIALIZATION_PATH, payload)
    _write_text(
        base / DEFAULT_MATERIALIZATION_DOC_PATH,
        render_newsroom_yukkuri_animation_primitive_probe_materialization_markdown(
            payload
        ),
    )
    return payload


def build_default_newsroom_yukkuri_animation_primitive_probe_materialization(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the tracked readback for the current-host local probe state."""
    base = Path(root) if root is not None else Path(".")
    proof = _load_json(base / DEFAULT_PROOF_PATH)
    scene_beat_probe = _load_json(base / DEFAULT_SCENE_BEAT_PATH)
    local_probe = _local_probe_access(base)
    probe_readback = _probe_ymmp_readback(base, local_probe)
    materialized = (
        local_probe["target_exists"]
        and local_probe["access_state"] == "verified_present_ignored_local_artifact"
        and probe_readback["readback_status"] == "structural_pass"
    )
    next_axis = (
        NEXT_AXIS_RENDER_SMOKE
        if materialized
        else "newsroom-chabangeki-skit-group-template-port-plan-v1"
    )

    return {
        "artifact_id": MATERIALIZATION_ID,
        "materialization_id": MATERIALIZATION_ID,
        "schema_version": MATERIALIZATION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "materialization_status": (
            "materialized_ignored_local_probe" if materialized else "blocked"
        ),
        "source_context": {
            "source_primitive_proof_path": _path_text(DEFAULT_PROOF_PATH),
            "source_primitive_proof_id": proof.get("proof_id"),
            "source_primitive_proof_doc_path": _path_text(DEFAULT_PROOF_DOC_PATH),
            "source_scene_beat_probe_path": _path_text(DEFAULT_SCENE_BEAT_PATH),
            "source_scene_beat_probe_id": scene_beat_probe.get("scene_beat_probe_id"),
            "source_scene_beat_probe_doc_path": _path_text(DEFAULT_SCENE_BEAT_DOC_PATH),
            "source_nod_head_ymmp_path": _path_text(SOURCE_NOD_HEAD_YMMP_PATH),
            "source_context_role": "verified_repo_filesystem_not_agent_report_claim",
        },
        "selected_primitives": PROVEN_PRIMITIVES,
        "selected_subset_reason": (
            "the four pass-status primitives from the previous structural proof "
            "can be represented by cloning tracked nod_head YMM4 items and "
            "bounded transform/path edits"
        ),
        "omitted_primitives": [
            {
                "primitive_id": primitive_id,
                "reason": reason,
            }
            for primitive_id, reason in OMITTED_PRIMITIVES.items()
        ],
        "local_probe": local_probe,
        "probe_plan": _probe_plan(),
        "probe_ymmp_readback": probe_readback,
        "primitive_coverage": _primitive_coverage(probe_readback),
        "access_readiness": _access_readiness(local_probe),
        "completion_matrix": _completion_matrix(materialized, next_axis),
        "expected_next_user_action_if_verified": {
            "this_slice_user_action_required": False,
            "future_render_smoke_action": (
                "use the verified ignored local probe as the target for a later "
                "operator-instructed YMM4 open/render-smoke slice"
            ),
            "open_command_recorded_not_requested": local_probe["launcher_or_open_command"],
        },
        "next_recommended_axis": {
            "selected": next_axis,
            "reason": (
                "local ignored .ymmp exists and structural readback covers the "
                "four proven primitives"
                if materialized
                else "materialization did not reach verified ignored local state"
            ),
            "prerequisites": [
                "keep the local .ymmp ignored and unstaged",
                "create an operator instruction sheet before any render smoke",
                "keep production/public acceptance false",
            ],
        },
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(materialized),
        "inertia_check": _inertia_check(next_axis),
    }


def materialize_local_primitive_probe_ymmp(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Create the ignored local probe .ymmp from tracked source material."""
    base = Path(root) if root is not None else Path(".")
    source_path = base / SOURCE_NOD_HEAD_YMMP_PATH
    project = load_ymmp(source_path)
    probe = copy.deepcopy(project)
    target_path = base / LOCAL_IGNORED_PROBE_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)

    probe["FilePath"] = str(target_path.resolve())
    timeline = _first_timeline(probe)
    if not timeline:
        raise ValueError(f"YMM4 source has no timeline: {source_path}")
    source_items = [
        copy.deepcopy(item)
        for item in _get_timeline_items(project)
        if isinstance(item, dict) and item.get("Remark") == "nod_head_v1"
    ]
    if len(source_items) != 4:
        raise ValueError(
            f"expected 4 nod_head_v1 source items, found {len(source_items)}"
        )

    items: list[dict[str, Any]] = []
    for beat in BEAT_PLAN:
        items.extend(_clone_beat_items(base, source_items, beat))
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


def render_newsroom_yukkuri_animation_primitive_probe_materialization_markdown(
    payload: dict[str, Any],
) -> str:
    lines = [
        "# Newsroom Yukkuri Animation Primitive Probe Materialization v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"materialization_status: {payload.get('materialization_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"next_recommended_axis: {_dict(payload.get('next_recommended_axis')).get('selected')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "Local Probe", payload.get("local_probe"))
    _append_rows(
        lines,
        "Probe Plan",
        [
            "beat_id",
            "timing_range",
            "scene_function",
            "primitive_ids",
            "expression",
            "motion_label",
        ],
        payload.get("probe_plan"),
    )
    _append_mapping(lines, "Probe YMM4 Readback", payload.get("probe_ymmp_readback"))
    _append_mapping(lines, "Primitive Coverage", payload.get("primitive_coverage"))
    _append_rows(lines, "Access Readiness", ["gate", "status"], payload.get("access_readiness"))
    _append_rows(lines, "Completion Matrix", ["gate", "status"], payload.get("completion_matrix"))
    _append_mapping(
        lines,
        "Expected Next User Action If Verified",
        payload.get("expected_next_user_action_if_verified"),
    )
    _append_mapping(lines, "Next Recommended Axis", payload.get("next_recommended_axis"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "The local `.ymmp` is an ignored diagnostic probe only. It is not "
            "rendered, not staged, not committed, and not production/public "
            "acceptance. The speech balloon primitive remains omitted because "
            "it is still partial.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _clone_beat_items(
    base: Path,
    source_items: list[dict[str, Any]],
    beat: dict[str, Any],
) -> list[dict[str, Any]]:
    cloned = [copy.deepcopy(item) for item in source_items]
    beat_id = str(beat["beat_id"])
    frame = int(beat["frame"])
    length = int(beat["length"])
    expression = str(beat["expression"])
    face_path = str((base / EXPRESSION_PATHS[expression]).resolve())
    body_path = str((base / BODY_SOURCE_PATH).resolve())

    for item in cloned:
        item["Frame"] = frame
        item["Length"] = length
        item["Remark"] = f"primitive_probe:{beat_id}:nod_head_v1"
        item_type = _item_type(item)
        if item_type == "ImageItem":
            file_path = item.get("FilePath")
            if isinstance(file_path, str) and "removebg-preview" in file_path:
                item["FilePath"] = body_path
            else:
                item["FilePath"] = face_path
        elif item_type == "GroupItem" and item.get("GroupRange") == 3:
            _set_route_values(item, "X", beat["parent_x_values"], length)
            _set_route_values(item, "Y", [0.0], length)
            _set_route_values(item, "Rotation", [0.0], length)
        elif item_type == "GroupItem" and item.get("GroupRange") == 1:
            _set_route_values(item, "Rotation", beat["head_rotation_values"], length)
    return cloned


def _set_route_values(
    item: dict[str, Any],
    key: str,
    values: list[float],
    length: int,
) -> None:
    route = item.get(key)
    if not isinstance(route, dict):
        return
    route["Values"] = [{"Value": float(value)} for value in values]
    route["AnimationType"] = "直線移動" if len(values) > 1 else "なし"
    if len(values) > 1:
        item["KeyFrames"] = {"Frames": [max(length // 2 - 1, 1)], "Count": 1}
    else:
        item["KeyFrames"] = {"Frames": [], "Count": 0}


def _probe_ymmp_readback(
    base: Path,
    local_probe: dict[str, Any],
) -> dict[str, Any]:
    target = base / LOCAL_IGNORED_PROBE_PATH
    if not target.exists():
        return {
            "readback_status": "blocked",
            "reason": "local_probe_missing",
            "target_exists": False,
        }
    data = load_ymmp(target)
    timeline = _first_timeline(data)
    items = _get_timeline_items(data)
    item_type_counts: dict[str, int] = {}
    for item in items:
        item_type_counts[_item_type(item)] = item_type_counts.get(_item_type(item), 0) + 1

    beat_summaries = [
        _beat_readback(beat, items)
        for beat in BEAT_PLAN
    ]
    primitive_status = _primitive_status(beat_summaries)
    unexpected_item_types = sorted(
        item_type for item_type in item_type_counts if item_type not in {"GroupItem", "ImageItem"}
    )
    structural_pass = (
        timeline.get("Length") == TIMELINE_LENGTH_FRAMES
        and item_type_counts.get("GroupItem") == 10
        and item_type_counts.get("ImageItem") == 10
        and not unexpected_item_types
        and all(row["status"] == "pass" for row in primitive_status if row["primitive_id"] in PROVEN_PRIMITIVES)
    )
    return {
        "readback_status": "structural_pass" if structural_pass else "blocked",
        "target_exists": True,
        "file_sha256": _sha256(target),
        "file_size_bytes": target.stat().st_size,
        "timeline": {
            "fps": _dict(timeline.get("VideoInfo")).get("FPS"),
            "length_frames": timeline.get("Length"),
            "length_sec": round(TIMELINE_LENGTH_FRAMES / FPS, 6),
            "item_count": len(items),
            "item_type_counts": item_type_counts,
            "unexpected_item_types": unexpected_item_types,
        },
        "beat_readback": beat_summaries,
        "primitive_status": primitive_status,
        "source_ymmp_copy_basis": _path_text(SOURCE_NOD_HEAD_YMMP_PATH),
        "local_probe_access_state": local_probe["access_state"],
        "YMM4_launch_status": "not_launched",
        "render_status": "not_rendered",
        "audio_tts_status": "not_created",
    }


def _beat_readback(
    beat: dict[str, Any],
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    marker = f"primitive_probe:{beat['beat_id']}:nod_head_v1"
    matched = [
        item for item in items if item.get("Remark") == marker
    ]
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


def _primitive_status(beat_summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    face_paths = {
        row.get("face_file_path")
        for row in beat_summaries
        if isinstance(row.get("face_file_path"), str)
    }
    status = [
        {
            "primitive_id": "head_nod",
            "status": (
                "pass"
                if any(
                    "head_nod" in row["primitive_ids"]
                    and len(row.get("head_rotation_values", [])) >= 3
                    and any(abs(value) > 0 for value in row["head_rotation_values"])
                    for row in beat_summaries
                )
                else "blocked"
            ),
            "evidence": "head GroupItem Rotation route contains non-zero keyframes",
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
                    and _value_range(row.get("parent_x_values", [])) >= 400
                    for row in beat_summaries
                )
                else "blocked"
            ),
            "evidence": "parent GroupItem X route moves between off-screen and review position",
        },
        {
            "primitive_id": "small_position_move",
            "status": (
                "pass"
                if any(
                    "small_position_move" in row["primitive_ids"]
                    and 0 < _value_range(row.get("parent_x_values", [])) <= 80
                    for row in beat_summaries
                )
                else "blocked"
            ),
            "evidence": "parent GroupItem X route uses small bounded nudges",
        },
        {
            "primitive_id": "speech_balloon",
            "status": "omitted_partial",
            "evidence": OMITTED_PRIMITIVES["speech_balloon"],
        },
    ]
    return status


def _primitive_coverage(probe_readback: dict[str, Any]) -> dict[str, Any]:
    beats = probe_readback.get("beat_readback")
    if not isinstance(beats, list):
        beats = []
    coverage = {
        primitive_id: [
            beat.get("beat_id")
            for beat in beats
            if primitive_id in beat.get("primitive_ids", [])
        ]
        for primitive_id in SELECTED_PRIMITIVES
    }
    return {
        "covered_primitives": PROVEN_PRIMITIVES,
        "omitted_primitives": list(OMITTED_PRIMITIVES),
        "coverage": coverage,
        "all_proven_primitives_covered": all(coverage[pid] for pid in PROVEN_PRIMITIVES),
        "speech_balloon_intentionally_omitted": True,
    }


def _local_probe_access(base: Path) -> dict[str, Any]:
    path = LOCAL_IGNORED_PROBE_PATH
    full_path = (base / path).resolve()
    folder = full_path.parent
    target_exists = full_path.exists()
    check_ignore = _git_check_ignore(base, path)
    ignored = check_ignore["ignored"]
    if target_exists and ignored:
        access_state = "verified_present_ignored_local_artifact"
    elif target_exists:
        access_state = "present_but_not_ignored_blocked"
    elif ignored:
        access_state = "ignored_local_artifact_missing"
    else:
        access_state = "missing_not_ignored_blocked"
    return {
        "artifact_id": "local_ignored_primitive_probe",
        "repo_relative_path": _path_text(path),
        "folder_full_path_current_host": str(folder),
        "file_full_path_current_host": str(full_path),
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{full_path}"',
        "target_exists": target_exists,
        "access_state": access_state,
        "access_evidence_level": "current_host_filesystem_plus_git_ignore",
        "evidence_source": "Path.exists + git check-ignore -v",
        "git_state": "ignored" if ignored else "untracked_or_absent",
        "git_check_ignore": check_ignore,
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


def _probe_plan() -> list[dict[str, Any]]:
    return [
        {
            "beat_id": beat["beat_id"],
            "timing_range": beat["timing_range"],
            "scene_function": beat["scene_function"],
            "primitive_ids": beat["primitive_ids"],
            "expression": beat["expression"],
            "motion_label": beat["motion_label"],
        }
        for beat in BEAT_PLAN
    ]


def _access_readiness(local_probe: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"gate": "target_path_emitted", "status": bool(local_probe.get("file_full_path_current_host"))},
        {"gate": "folder_path_emitted", "status": bool(local_probe.get("folder_full_path_current_host"))},
        {"gate": "target_exists_stated", "status": local_probe.get("target_exists") is True},
        {
            "gate": "access_state_verified_present",
            "status": local_probe.get("access_state") == "verified_present_ignored_local_artifact",
        },
        {
            "gate": "access_evidence_level_stated",
            "status": local_probe.get("access_evidence_level") == "current_host_filesystem_plus_git_ignore",
        },
        {
            "gate": "git_ignore_verified",
            "status": _dict(local_probe.get("git_check_ignore")).get("ignored") is True,
        },
    ]


def _completion_matrix(materialized: bool, next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "repo_state_verified", "status": True},
        {"gate": "primitive_proof_inspected", "status": True},
        {"gate": "probe_subset_selected", "status": PROVEN_PRIMITIVES},
        {"gate": "local_ignored_probe_created_or_blocked_recorded", "status": materialized},
        {"gate": "access_state_recorded", "status": materialized},
        {"gate": "readback_json_doc_created", "status": True},
        {"gate": "next_axis_selected", "status": next_axis},
        {"gate": "commit_and_push_if_push_gate_passes", "status": "ready_for_git_followthrough"},
    ]


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_text_density_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_automation_rabbit_hole", "status": True},
        {"gate": "no_user_work_before_verified_target", "status": True},
        {"gate": "next_concrete_animation_milestone_named", "status": next_axis},
    ]


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "render_proof": False,
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


def _boundaries(local_probe_created: bool) -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "source_ymmp_modified": False,
        "local_ignored_probe_created": local_probe_created,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
    }


def _first_timeline(root: dict[str, Any]) -> dict[str, Any]:
    timelines = root.get("Timelines")
    if isinstance(timelines, list) and timelines and isinstance(timelines[0], dict):
        return timelines[0]
    timeline = root.get("Timeline")
    if isinstance(timeline, dict):
        return timeline
    return {}


def _route_values(item: dict[str, Any] | None, key: str) -> list[float]:
    if not isinstance(item, dict):
        return []
    route = item.get(key)
    if not isinstance(route, dict):
        return []
    values = route.get("Values")
    if not isinstance(values, list):
        return []
    out: list[float] = []
    for point in values:
        if isinstance(point, dict) and isinstance(point.get("Value"), (int, float)):
            out.append(float(point["Value"]))
    return out


def _value_range(values: object) -> float:
    if not isinstance(values, list) or not values:
        return 0.0
    numeric = [float(value) for value in values if isinstance(value, (int, float))]
    if not numeric:
        return 0.0
    return max(numeric) - min(numeric)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: str | Path) -> Any:
    raw = Path(path).read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp932", "shift_jis"):
        try:
            return json.loads(raw.decode(encoding))
        except UnicodeDecodeError:
            continue
    return json.loads(raw.decode("utf-8", errors="replace"))


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


def _dict(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _display(value: object) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if value is None:
        return ""
    return str(value).replace("\n", " ")


def _path_text(path: str | Path) -> str:
    return Path(path).as_posix()


def main() -> int:
    write_default_newsroom_yukkuri_animation_primitive_probe_materialization_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
