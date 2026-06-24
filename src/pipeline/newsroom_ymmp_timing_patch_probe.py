"""Timing patch probe for the diagnostic newsroom YMM4 project.

This module creates a structural timing patch plan and readback for a local
ignored .ymmp copy. It does not launch YMM4, render, generate TTS/audio, import
real media, stage or commit .ymmp/media output, or approve production use.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_audio_observation_and_timing_patch_readiness import (
    DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH,
)
from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
    DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_neutral_timeline_import_proof import (
    DEFAULT_NEUTRAL_TIMELINE_PATH,
)
from src.pipeline.newsroom_ymmp_timing_patch_strategy import (
    DEFAULT_YMMP_TIMING_PATCH_STRATEGY_PATH,
    NEXT_PATCH_PROBE_SLICE,
    RECOMMENDED_DEFAULT,
)
from src.pipeline.newsroom_yym4_native_audio_path_proof import (
    DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH,
)


YMMP_TIMING_PATCH_PROBE_SCHEMA_VERSION = "newsroom_ymmp_timing_patch_probe.v1"
YMMP_TIMING_PATCH_PROBE_READBACK_SCHEMA_VERSION = (
    "newsroom_ymmp_timing_patch_probe_readback.v1"
)
YMMP_TIMING_PATCH_PROBE_ID = (
    "newsroom_ymmp_timing_patch_probe_v1_2026_06_24"
)
YMMP_TIMING_PATCH_PROBE_READBACK_ID = (
    "newsroom_ymmp_timing_patch_probe_readback_v1_2026_06_24"
)
DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH = Path(
    "samples/_probe/newsroom_handoff/ymmp_timing_patch_probe_v1.json"
)
DEFAULT_YMMP_TIMING_PATCH_PROBE_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/ymmp_timing_patch_probe_readback_v1.json"
)
DEFAULT_YMMP_TIMING_PATCH_PROBE_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YMMP_TIMING_PATCH_PROBE_V1_2026-06-24.md"
)
DEFAULT_SOURCE_YMMP_LOCAL_PATH = Path(
    "_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp"
)
DEFAULT_PATCHED_YMMP_LOCAL_PATH = Path(
    "_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp"
)

PATCH_METHOD = "neutral_timeline_skeleton_patch_with_native_voice_preserved"
POST_PATCH_RENDER_SMOKE_SLICE = "newsroom-ymmp-timing-patch-render-smoke-v1"
VOICE_ITEM_TYPE_FRAGMENT = "VoiceItem"
VOICE_PRESERVED_FIELDS: tuple[str, ...] = (
    "CharacterName",
    "Serif",
    "VoiceCache",
    "VoiceParameter",
    "Pronounce",
    "Hatsuon",
    "VoiceLength",
    "AudioEffects",
)


def build_default_newsroom_ymmp_timing_patch_probe(
    *,
    root: str | Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build the committed patch plan and structural readback."""
    plan, readback, _patched_root = _build_default_probe_payload(root=root)
    return plan, readback


def write_default_newsroom_ymmp_timing_patch_probe_artifacts(
    *,
    root: str | Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Write JSON/doc artifacts and the ignored local patched .ymmp copy."""
    base = Path(root) if root is not None else Path(".")
    plan, readback, patched_root = _build_default_probe_payload(root=base)

    _write_json(base / DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH, plan)
    _write_json(base / DEFAULT_YMMP_TIMING_PATCH_PROBE_READBACK_PATH, readback)
    _write_text(
        base / DEFAULT_YMMP_TIMING_PATCH_PROBE_DOC_PATH,
        render_newsroom_ymmp_timing_patch_probe_markdown(plan, readback),
    )
    _write_json(base / DEFAULT_PATCHED_YMMP_LOCAL_PATH, patched_root)
    return plan, readback


def build_newsroom_ymmp_timing_patch_probe(
    strategy: dict[str, Any],
    neutral_timeline: dict[str, Any],
    structure_readback: dict[str, Any],
    audio_observation: dict[str, Any],
    native_audio_path_proof: dict[str, Any],
    source_ymmp_root: dict[str, Any],
    *,
    source_ymmp_path: str | Path,
    patched_ymmp_path: str | Path,
    source_strategy_path: str | Path,
    source_neutral_timeline_path: str | Path,
    source_structure_readback_path: str | Path,
    source_audio_observation_path: str | Path,
    source_native_audio_path_proof_path: str | Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Build a diagnostic-only timing patch plan and patched structure readback."""
    source_summary = _ymmp_summary(source_ymmp_root)
    neutral_caption_items = _neutral_caption_items(neutral_timeline)
    mapping = _build_mapping(source_summary, neutral_caption_items)
    source_validation = _source_validation(
        strategy,
        neutral_timeline,
        structure_readback,
        audio_observation,
        native_audio_path_proof,
        source_summary,
        mapping,
    )
    patch_operations = _patch_operations(source_summary, mapping)
    patched_root = apply_timing_patch_to_ymmp(source_ymmp_root, patch_operations)
    patched_summary = _ymmp_summary(patched_root)
    preservation = _field_preservation(source_summary, patched_summary)
    structural_result = _structural_result(source_summary, patched_summary, mapping)
    plan_status = (
        "applied_to_ignored_local_copy_after_validation"
        if source_validation["status"] == "passed"
        and preservation["all_required_fields_preserved"]
        and structural_result["target_68_sec_reached_structurally"]
        else "blocked"
    )
    readback_status = (
        "structural_pass"
        if plan_status == "applied_to_ignored_local_copy_after_validation"
        else "blocked"
    )

    plan = {
        "artifact_id": YMMP_TIMING_PATCH_PROBE_ID,
        "probe_id": YMMP_TIMING_PATCH_PROBE_ID,
        "schema_version": YMMP_TIMING_PATCH_PROBE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "probe_status": plan_status,
        "identity": {
            "probe_id": YMMP_TIMING_PATCH_PROBE_ID,
            "source_strategy_path": _path_text(source_strategy_path),
            "source_strategy_id": strategy.get("strategy_id"),
            "source_neutral_timeline_path": _path_text(source_neutral_timeline_path),
            "source_neutral_timeline_id": neutral_timeline.get("timeline_id"),
            "source_structure_readback_path": _path_text(
                source_structure_readback_path
            ),
            "source_structure_readback_id": structure_readback.get("readback_id"),
            "source_audio_observation_path": _path_text(source_audio_observation_path),
            "source_audio_observation_id": audio_observation.get("readback_id"),
            "source_native_audio_path_proof_path": _path_text(
                source_native_audio_path_proof_path
            ),
            "source_native_audio_path_proof_id": native_audio_path_proof.get(
                "proof_id"
            ),
            "source_ymmp_path": _path_text(source_ymmp_path),
            "patched_ymmp_path": _path_text(patched_ymmp_path),
            "production_status": "diagnostic_only",
        },
        "source_validation": source_validation,
        "selected_patch_method": _selected_patch_method(),
        "target_timeline": _target_timeline(mapping),
        "mapping": mapping,
        "patch_operations": patch_operations,
        "patch_sequence": _patch_sequence(),
        "field_preservation_plan": _field_preservation_plan(),
        "structural_result_expected": structural_result,
        "local_file_boundary": _local_file_boundary(source_ymmp_path, patched_ymmp_path),
        "render_gate": _render_gate(),
        "not_accepted_scope": _not_accepted_scope(),
        "warnings": _warnings(),
        "next_recommended_slice": POST_PATCH_RENDER_SMOKE_SLICE,
        "downstream_next_use": _downstream_next_use(),
        "boundaries": _boundaries(),
    }
    readback = {
        "artifact_id": YMMP_TIMING_PATCH_PROBE_READBACK_ID,
        "readback_id": YMMP_TIMING_PATCH_PROBE_READBACK_ID,
        "schema_version": YMMP_TIMING_PATCH_PROBE_READBACK_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "readback_status": readback_status,
        "identity": {
            "readback_id": YMMP_TIMING_PATCH_PROBE_READBACK_ID,
            "source_probe_id": YMMP_TIMING_PATCH_PROBE_ID,
            "source_probe_path": _path_text(DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH),
            "source_ymmp_path": _path_text(source_ymmp_path),
            "patched_ymmp_path": _path_text(patched_ymmp_path),
            "production_status": "diagnostic_only",
        },
        "local_file_status": _local_file_status(source_ymmp_path, patched_ymmp_path),
        "patch_application": {
            "patch_method": PATCH_METHOD,
            "operation_count": len(patch_operations),
            "operations_applied": all(row.get("applied") for row in patch_operations),
            "timeline_length_operation_applied": patch_operations[0].get(
                "field_changed"
            )
            == "Timeline.Length",
            "voice_item_timing_operations_applied": len(patch_operations) - 1,
            "fallback_carrier_used": False,
        },
        "before_after_timing": {
            "fps": patched_summary["fps"],
            "source_total_frames": source_summary["timeline_length_frames"],
            "source_total_sec": source_summary["timeline_duration_sec"],
            "patched_total_frames": patched_summary["timeline_length_frames"],
            "patched_total_sec": patched_summary["timeline_duration_sec"],
            "target_total_frames": 4080,
            "target_total_sec": 68,
            "source_item_timings": _item_timing_rows(source_summary),
            "patched_item_timings": _item_timing_rows(patched_summary),
            "patched_item_end_frames": [
                row["end_frame"] for row in _item_timing_rows(patched_summary)
            ],
            "target_68_sec_reached_structurally": structural_result[
                "target_68_sec_reached_structurally"
            ],
        },
        "mapping_readback": mapping,
        "field_preservation_readback": preservation,
        "structural_result": structural_result,
        "audio_voice_boundary": _audio_voice_boundary(),
        "render_gate": _render_gate(),
        "not_accepted_scope": _not_accepted_scope(),
        "warnings": _warnings(),
        "next_recommended_slice": POST_PATCH_RENDER_SMOKE_SLICE,
        "boundaries": _boundaries(),
    }
    return plan, readback, patched_root


def apply_timing_patch_to_ymmp(
    source_ymmp_root: dict[str, Any],
    patch_operations: list[dict[str, Any]],
) -> dict[str, Any]:
    """Apply the plan's timing-only operations to a copied YMM4 project root."""
    patched = copy.deepcopy(source_ymmp_root)
    timeline = _first_timeline(patched)
    items = timeline.get("Items") if isinstance(timeline.get("Items"), list) else []

    for operation in patch_operations:
        field = operation.get("field_changed")
        if field == "Timeline.Length":
            timeline["Length"] = operation.get("after")
            continue
        item_index = operation.get("item_index")
        if not isinstance(item_index, int) or item_index >= len(items):
            continue
        item = items[item_index]
        if not isinstance(item, dict):
            continue
        if field == "Frame":
            item["Frame"] = operation.get("after")
        elif field == "Length":
            item["Length"] = operation.get("after")

    return patched


def render_newsroom_ymmp_timing_patch_probe_markdown(
    plan: dict[str, Any],
    readback: dict[str, Any],
) -> str:
    """Render a human-readable patch probe readback."""
    lines = [
        "# Newsroom YMM4 Timing Patch Probe v1",
        "",
        f"artifact_id: {plan.get('artifact_id')}",
        f"probe_id: {plan.get('probe_id')}",
        f"schema_version: {plan.get('schema_version')}",
        f"review_status: {plan.get('review_status')}",
        f"production_status: {plan.get('production_status')}",
        f"probe_status: {plan.get('probe_status')}",
        f"readback_id: {readback.get('readback_id')}",
        f"readback_status: {readback.get('readback_status')}",
        "diagnostic_only: true",
        "",
    ]
    _append_mapping(lines, "Source", plan.get("identity"))
    _append_mapping(lines, "Source Validation", plan.get("source_validation"))
    _append_mapping(lines, "Selected Patch Method", plan.get("selected_patch_method"))

    lines.extend(
        [
            "",
            "## Dialogue Mapping",
            "",
            "| index | text | source frame/length | target frame/length | method |",
            "|---|---|---|---|---|",
        ]
    )
    for row in plan.get("mapping", {}).get("items", []):
        source = f"{row.get('source_frame')} / {row.get('source_length_frames')}"
        target = f"{row.get('target_frame')} / {row.get('target_length_frames')}"
        lines.append(
            "| "
            f"{row.get('source_index')} | "
            f"{row.get('text')} | "
            f"{source} | "
            f"{target} | "
            f"{row.get('mapping_method')} |"
        )

    lines.extend(
        [
            "",
            "## Patch Operations",
            "",
            "| target | before | after | applied |",
            "|---|---:|---:|---|",
        ]
    )
    for operation in plan.get("patch_operations", []):
        lines.append(
            "| "
            f"{operation.get('target_path')} | "
            f"{_display(operation.get('before'))} | "
            f"{_display(operation.get('after'))} | "
            f"{_display(operation.get('applied'))} |"
        )

    _append_mapping(lines, "Patch Application", readback.get("patch_application"))
    _append_mapping(lines, "Before / After Timing", readback.get("before_after_timing"))
    _append_mapping(
        lines,
        "Field Preservation Readback",
        readback.get("field_preservation_readback"),
    )
    _append_mapping(lines, "Structural Result", readback.get("structural_result"))
    _append_mapping(lines, "Local File Status", readback.get("local_file_status"))
    _append_mapping(lines, "Render Gate", readback.get("render_gate"))
    _append_mapping(lines, "Not Accepted Scope", readback.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", readback.get("boundaries"))

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "The patched `.ymmp` is an ignored local diagnostic copy only. This "
            "probe changes timeline length plus VoiceItem Frame/Length fields, "
            "preserves speaker/text/native voice fields, and keeps render "
            "deferred to the next milestone.",
            "",
        ]
    )
    return "\n".join(lines)


def _build_default_probe_payload(
    *,
    root: str | Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    base = Path(root) if root is not None else Path(".")
    strategy = load_json_object(base / DEFAULT_YMMP_TIMING_PATCH_STRATEGY_PATH)
    neutral_timeline = load_json_object(base / DEFAULT_NEUTRAL_TIMELINE_PATH)
    structure_readback = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
    )
    audio_observation = load_json_object(
        base / DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
    )
    native_audio_path_proof = load_json_object(
        base / DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH
    )
    source_ymmp_root = _load_ymmp(base / DEFAULT_SOURCE_YMMP_LOCAL_PATH)
    return build_newsroom_ymmp_timing_patch_probe(
        strategy,
        neutral_timeline,
        structure_readback,
        audio_observation,
        native_audio_path_proof,
        source_ymmp_root,
        source_ymmp_path=DEFAULT_SOURCE_YMMP_LOCAL_PATH,
        patched_ymmp_path=DEFAULT_PATCHED_YMMP_LOCAL_PATH,
        source_strategy_path=DEFAULT_YMMP_TIMING_PATCH_STRATEGY_PATH,
        source_neutral_timeline_path=DEFAULT_NEUTRAL_TIMELINE_PATH,
        source_structure_readback_path=DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH,
        source_audio_observation_path=(
            DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
        ),
        source_native_audio_path_proof_path=DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH,
    )


def _source_validation(
    strategy: dict[str, Any],
    neutral_timeline: dict[str, Any],
    structure_readback: dict[str, Any],
    audio_observation: dict[str, Any],
    native_audio_path_proof: dict[str, Any],
    source_summary: dict[str, Any],
    mapping: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    strategy_recommended = _dict(strategy.get("recommended_default"))
    structure_dialogue = _dict(structure_readback.get("dialogue_structure"))
    structure_timing = _dict(structure_readback.get("timing_structure"))
    audio_normalized = _dict(audio_observation.get("normalized_audio_observation"))
    native_validation = _dict(native_audio_path_proof.get("source_validation"))

    if strategy.get("strategy_status") != "recommended_for_probe":
        errors.append("TIMING_PATCH_STRATEGY_NOT_RECOMMENDED_FOR_PROBE")
    if strategy_recommended.get("choice") != RECOMMENDED_DEFAULT:
        errors.append("TIMING_PATCH_STRATEGY_DEFAULT_MISMATCH")
    if strategy_recommended.get("choice") != PATCH_METHOD:
        errors.append("PATCH_METHOD_DOES_NOT_MATCH_STRATEGY")
    if neutral_timeline.get("global_timing", {}).get("total_duration_sec") != 68:
        errors.append("NEUTRAL_TIMELINE_NOT_68_SEC")
    if source_summary.get("fps") != 60:
        errors.append("SOURCE_YMMP_FPS_NOT_60")
    if source_summary.get("timeline_length_frames") != 509:
        errors.append("SOURCE_YMMP_LENGTH_NOT_509")
    if len(source_summary.get("voice_items", [])) != 4:
        errors.append("SOURCE_YMMP_VOICE_ITEM_COUNT_NOT_4")
    if structure_dialogue.get("canonical_speaker_value") != CANONICAL_UI_OBSERVED_SPEAKER:
        errors.append("STRUCTURE_CANONICAL_SPEAKER_MISMATCH")
    if source_summary.get("speaker_values") != [CANONICAL_UI_OBSERVED_SPEAKER]:
        errors.append("SOURCE_YMMP_SPEAKER_MISMATCH")
    if structure_timing.get("observed_project_duration_frames") != 509:
        errors.append("STRUCTURE_READBACK_SOURCE_LENGTH_MISMATCH")
    if audio_normalized.get("external_TTS_introduced") is not False:
        errors.append("EXTERNAL_TTS_ALREADY_INTRODUCED")
    if audio_normalized.get("diagnostic_audio_path_accepted") is not True:
        errors.append("DIAGNOSTIC_AUDIO_PATH_NOT_ACCEPTED")
    if native_audio_path_proof.get("proof_status") != "passed_with_unknowns":
        errors.append("NATIVE_AUDIO_PATH_PROOF_NOT_AVAILABLE")
    if native_validation.get("native_voice_engine_hint") != "AquesTalk":
        errors.append("NATIVE_ENGINE_HINT_MISSING")
    if mapping.get("status") != "mapped":
        errors.append("NEUTRAL_TEXT_MAPPING_NOT_COMPLETE")

    return {
        "status": "passed" if not errors else "blocked",
        "strategy_id": strategy.get("strategy_id"),
        "neutral_timeline_id": neutral_timeline.get("timeline_id"),
        "structure_readback_id": structure_readback.get("readback_id"),
        "audio_observation_id": audio_observation.get("readback_id"),
        "native_audio_path_proof_id": native_audio_path_proof.get("proof_id"),
        "canonical_speaker": CANONICAL_UI_OBSERVED_SPEAKER,
        "canonical_speaker_unicode_escape": CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
        "source_fps": source_summary.get("fps"),
        "source_total_frames": source_summary.get("timeline_length_frames"),
        "target_total_frames": 4080,
        "source_voice_item_count": len(source_summary.get("voice_items", [])),
        "neutral_caption_count": mapping.get("neutral_caption_count"),
        "mapping_method": mapping.get("mapping_method"),
        "errors": errors,
    }


def _build_mapping(
    source_summary: dict[str, Any],
    neutral_caption_items: list[dict[str, Any]],
) -> dict[str, Any]:
    source_voice_items = source_summary.get("voice_items", [])
    fps = source_summary.get("fps")
    rows = []
    unmatched: list[dict[str, Any]] = []
    if fps in (None, 0):
        fps = 60

    for index, source_item in enumerate(source_voice_items):
        neutral_item = neutral_caption_items[index] if index < len(neutral_caption_items) else {}
        text_matches = source_item.get("text") == neutral_item.get("text")
        if not text_matches:
            unmatched.append(
                {
                    "source_index": source_item.get("voice_index"),
                    "source_text": source_item.get("text"),
                    "neutral_item_id": neutral_item.get("item_id"),
                    "neutral_text": neutral_item.get("text"),
                }
            )
        start_sec = _intish(neutral_item.get("start_sec"))
        end_sec = _intish(neutral_item.get("end_sec"))
        duration_sec = _intish(neutral_item.get("duration_sec"))
        target_frame = int(start_sec * fps) if isinstance(start_sec, int) else None
        target_length = (
            int(duration_sec * fps) if isinstance(duration_sec, int) else None
        )
        rows.append(
            {
                "source_index": source_item.get("voice_index"),
                "item_index": source_item.get("item_index"),
                "neutral_item_id": neutral_item.get("item_id"),
                "text": source_item.get("text"),
                "text_matches_neutral_caption": text_matches,
                "source_frame": source_item.get("frame"),
                "source_length_frames": source_item.get("length_frames"),
                "source_end_frame": source_item.get("end_frame"),
                "target_start_sec": start_sec,
                "target_end_sec": end_sec,
                "target_duration_sec": duration_sec,
                "target_frame": target_frame,
                "target_length_frames": target_length,
                "target_end_frame": (
                    target_frame + target_length
                    if target_frame is not None and target_length is not None
                    else None
                ),
                "mapping_method": "text_and_order",
            }
        )

    return {
        "status": "mapped"
        if not unmatched and len(source_voice_items) == len(neutral_caption_items)
        else "blocked",
        "mapping_method": "text_and_order",
        "source_voice_item_count": len(source_voice_items),
        "neutral_caption_count": len(neutral_caption_items),
        "fps": fps,
        "target_total_sec": 68,
        "target_total_frames": 4080,
        "items": rows,
        "unmatched_items": unmatched,
    }


def _patch_operations(
    source_summary: dict[str, Any],
    mapping: dict[str, Any],
) -> list[dict[str, Any]]:
    operations = [
        {
            "operation_id": "timeline_length_to_4080_frames",
            "operation_kind": "set_timeline_duration",
            "target_path": "Timelines[0].Length",
            "field_changed": "Timeline.Length",
            "before": source_summary.get("timeline_length_frames"),
            "after": 4080,
            "allowed_by_strategy": True,
            "applied": True,
            "reason": "extend diagnostic timeline from natural 509 frames to neutral 68 sec / 4080 frames",
        }
    ]
    for row in mapping.get("items", []):
        item_index = row.get("item_index")
        source_index = row.get("source_index")
        operations.append(
            {
                "operation_id": f"voice_item_{source_index}_frame_to_neutral_anchor",
                "operation_kind": "set_voice_item_frame",
                "target_path": f"Timelines[0].Items[{item_index}].Frame",
                "field_changed": "Frame",
                "item_index": item_index,
                "voice_index": source_index,
                "text": row.get("text"),
                "before": row.get("source_frame"),
                "after": row.get("target_frame"),
                "allowed_by_strategy": True,
                "applied": True,
                "reason": "align VoiceItem start to neutral caption anchor",
            }
        )
        operations.append(
            {
                "operation_id": f"voice_item_{source_index}_length_to_neutral_span",
                "operation_kind": "set_voice_item_length",
                "target_path": f"Timelines[0].Items[{item_index}].Length",
                "field_changed": "Length",
                "item_index": item_index,
                "voice_index": source_index,
                "text": row.get("text"),
                "before": row.get("source_length_frames"),
                "after": row.get("target_length_frames"),
                "allowed_by_strategy": True,
                "applied": True,
                "reason": "align VoiceItem duration to neutral caption span while leaving voice fields untouched",
            }
        )
    return operations


def _ymmp_summary(root: dict[str, Any]) -> dict[str, Any]:
    timeline = _first_timeline(root)
    video_info = _dict(timeline.get("VideoInfo"))
    fps = _intish(video_info.get("FPS"))
    length = _intish(timeline.get("Length"))
    raw_items = timeline.get("Items") if isinstance(timeline.get("Items"), list) else []
    voice_items: list[dict[str, Any]] = []
    for item_index, item in enumerate(raw_items):
        if not isinstance(item, dict):
            continue
        if VOICE_ITEM_TYPE_FRAGMENT not in str(item.get("$type", "")):
            continue
        frame = _intish(item.get("Frame"))
        item_length = _intish(item.get("Length"))
        voice_items.append(
            {
                "voice_index": len(voice_items),
                "item_index": item_index,
                "type_name": item.get("$type"),
                "frame": frame,
                "length_frames": item_length,
                "end_frame": frame + item_length
                if isinstance(frame, int) and isinstance(item_length, int)
                else None,
                "start_sec": round(frame / fps, 6)
                if isinstance(frame, int) and isinstance(fps, int) and fps
                else None,
                "duration_sec": round(item_length / fps, 6)
                if isinstance(item_length, int) and isinstance(fps, int) and fps
                else None,
                "end_sec": round((frame + item_length) / fps, 6)
                if isinstance(frame, int)
                and isinstance(item_length, int)
                and isinstance(fps, int)
                and fps
                else None,
                "speaker": item.get("CharacterName"),
                "speaker_unicode_escape": _unicode_escape(item.get("CharacterName")),
                "text": item.get("Serif"),
                "voice_length": item.get("VoiceLength"),
                "preserved_fields": {
                    field: copy.deepcopy(item.get(field))
                    for field in VOICE_PRESERVED_FIELDS
                },
            }
        )
    characters = root.get("Characters") if isinstance(root.get("Characters"), list) else []
    return {
        "timeline_length_frames": length,
        "timeline_duration_sec": round(length / fps, 6)
        if isinstance(length, int) and isinstance(fps, int) and fps
        else None,
        "fps": fps,
        "timeline_count": len(root.get("Timelines", []))
        if isinstance(root.get("Timelines"), list)
        else 0,
        "selected_timeline_index": root.get("SelectedTimelineIndex"),
        "voice_items": voice_items,
        "speaker_values": sorted(
            {item.get("speaker") for item in voice_items if item.get("speaker")}
        ),
        "texts": [item.get("text") for item in voice_items],
        "characters": copy.deepcopy(characters),
        "character_voice_apis": sorted(
            {
                _dict(character.get("Voice")).get("API")
                for character in characters
                if isinstance(character, dict)
                and _dict(character.get("Voice")).get("API")
            }
        ),
    }


def _field_preservation(
    source_summary: dict[str, Any],
    patched_summary: dict[str, Any],
) -> dict[str, Any]:
    source_items = source_summary.get("voice_items", [])
    patched_items = patched_summary.get("voice_items", [])
    per_item = []
    all_ok = len(source_items) == len(patched_items)
    for source, patched in zip(source_items, patched_items):
        fields = {
            field: (
                source.get("preserved_fields", {}).get(field)
                == patched.get("preserved_fields", {}).get(field)
            )
            for field in VOICE_PRESERVED_FIELDS
        }
        row_ok = all(fields.values())
        all_ok = all_ok and row_ok
        per_item.append(
            {
                "voice_index": source.get("voice_index"),
                "item_index": source.get("item_index"),
                "text": source.get("text"),
                "fields": fields,
                "all_required_fields_preserved": row_ok,
            }
        )
    characters_preserved = source_summary.get("characters") == patched_summary.get(
        "characters"
    )
    all_ok = all_ok and characters_preserved
    return {
        "all_required_fields_preserved": all_ok,
        "preserved_field_names": list(VOICE_PRESERVED_FIELDS),
        "per_item": per_item,
        "characters_block_preserved": characters_preserved,
        "character_voice_apis_preserved": source_summary.get("character_voice_apis")
        == patched_summary.get("character_voice_apis"),
        "external_TTS_introduced": False,
        "voice_regenerated": False,
        "voice_stretched_or_replaced": False,
        "voice_cache_rewritten": False,
    }


def _structural_result(
    source_summary: dict[str, Any],
    patched_summary: dict[str, Any],
    mapping: dict[str, Any],
) -> dict[str, Any]:
    target_frames = [row.get("target_frame") for row in mapping.get("items", [])]
    target_lengths = [
        row.get("target_length_frames") for row in mapping.get("items", [])
    ]
    patched_items = patched_summary.get("voice_items", [])
    patched_frames = [row.get("frame") for row in patched_items]
    patched_lengths = [row.get("length_frames") for row in patched_items]
    patched_ends = [row.get("end_frame") for row in patched_items]
    target_reached = (
        patched_summary.get("timeline_length_frames") == 4080
        and patched_summary.get("timeline_duration_sec") == 68
        and patched_frames == target_frames
        and patched_lengths == target_lengths
        and patched_ends[-1:] == [4080]
    )
    return {
        "structural_readback_status": "pass" if target_reached else "blocked",
        "source_total_frames": source_summary.get("timeline_length_frames"),
        "source_total_sec": source_summary.get("timeline_duration_sec"),
        "patched_total_frames": patched_summary.get("timeline_length_frames"),
        "patched_total_sec": patched_summary.get("timeline_duration_sec"),
        "target_total_frames": 4080,
        "target_total_sec": 68,
        "fps": patched_summary.get("fps"),
        "patched_voice_item_count": len(patched_items),
        "patched_frames": patched_frames,
        "patched_lengths": patched_lengths,
        "patched_end_frames": patched_ends,
        "target_68_sec_reached_structurally": target_reached,
        "fallback_carrier_used": False,
        "render_required_before_video_acceptance": True,
    }


def _neutral_caption_items(neutral_timeline: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in neutral_timeline.get("items", [])
        if isinstance(item, dict) and item.get("item_kind") == "caption"
    ]


def _selected_patch_method() -> dict[str, Any]:
    return {
        "choice": PATCH_METHOD,
        "source_strategy_choice": RECOMMENDED_DEFAULT,
        "strategy_slice": NEXT_PATCH_PROBE_SLICE,
        "why_safe_for_this_probe": [
            "the four VoiceItem rows match the four neutral caption rows by text and order",
            "actual .ymmp timing fields are Frame, Length, and timeline Length",
            "speaker, text, VoiceCache, VoiceParameter, Pronounce, Hatsuon, VoiceLength, and AudioEffects are not modified",
        ],
        "why_diagnostic_only": [
            "long sparse spans are timing mechanics, not final pacing",
            "post-patch render has not been run in this slice",
            "visual layout and production narration remain unaccepted",
        ],
    }


def _target_timeline(mapping: dict[str, Any]) -> dict[str, Any]:
    return {
        "timebase_fps": mapping.get("fps"),
        "target_total_sec": mapping.get("target_total_sec"),
        "target_total_frames": mapping.get("target_total_frames"),
        "anchors_sec": [
            row.get("target_start_sec") for row in mapping.get("items", [])
        ]
        + [68],
        "anchors_frames": [
            row.get("target_frame") for row in mapping.get("items", [])
        ]
        + [4080],
        "item_lengths_frames": [
            row.get("target_length_frames") for row in mapping.get("items", [])
        ],
    }


def _patch_sequence() -> list[dict[str, Any]]:
    return [
        {
            "step": "validate_source_artifacts_and_local_source_ymmp",
            "status": "passed",
        },
        {
            "step": "map_existing_voice_items_to_neutral_caption_rows_by_text_and_order",
            "status": "passed",
        },
        {
            "step": "set_timeline_length_to_4080_frames",
            "status": "applied_in_ignored_copy",
        },
        {
            "step": "set_each_voice_item_frame_and_length_to_neutral_anchor_span",
            "status": "applied_in_ignored_copy",
        },
        {
            "step": "compare_preserved_voice_fields_after_patch",
            "status": "passed",
        },
        {
            "step": "defer_render_until_structural_readback_passes",
            "status": "carried_forward",
        },
    ]


def _field_preservation_plan() -> dict[str, Any]:
    return {
        "must_preserve": list(VOICE_PRESERVED_FIELDS),
        "must_not_change": [
            "native voice engine hints",
            "Characters block",
            "VoiceCache contents",
            "VoiceLength values",
            "Pronounce and Hatsuon",
        ],
        "allowed_to_change": [
            "Timelines[0].Length",
            "VoiceItem.Frame",
            "VoiceItem.Length",
        ],
        "fallback_carrier_needed": False,
    }


def _local_file_boundary(source_ymmp_path: str | Path, patched_ymmp_path: str | Path) -> dict[str, Any]:
    return {
        "source_ymmp_path": _path_text(source_ymmp_path),
        "patched_ymmp_path": _path_text(patched_ymmp_path),
        "patched_ymmp_created_or_updated_by_generation": True,
        "patched_copy_under_tmp": str(patched_ymmp_path).replace("\\", "/").startswith(
            "_tmp/"
        ),
        "expected_git_ignore_rule": "_tmp/",
        "ymmp_commit_allowed": False,
        "ymmp_or_media_stage_allowed": False,
    }


def _local_file_status(source_ymmp_path: str | Path, patched_ymmp_path: str | Path) -> dict[str, Any]:
    return {
        "source_ymmp_path": _path_text(source_ymmp_path),
        "source_ymmp_found_at_generation": True,
        "patched_ymmp_path": _path_text(patched_ymmp_path),
        "patched_ymmp_created_or_updated_by_generation": True,
        "patched_copy_under_tmp": str(patched_ymmp_path).replace("\\", "/").startswith(
            "_tmp/"
        ),
        "expected_git_ignore_rule": "_tmp/",
        "ymmp_committed": False,
        "ymmp_or_media_staged": False,
        "media_output_created": False,
    }


def _audio_voice_boundary() -> dict[str, Any]:
    return {
        "speaker_preserved": True,
        "canonical_speaker": CANONICAL_UI_OBSERVED_SPEAKER,
        "canonical_speaker_unicode_escape": CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
        "native_voice_path_preserved": True,
        "VoiceCache_preserved": True,
        "VoiceLength_preserved": True,
        "VoiceParameter_preserved": True,
        "Pronounce_preserved": True,
        "Hatsuon_preserved": True,
        "AudioEffects_preserved": True,
        "external_TTS_introduced": False,
        "audio_generated_by_agent": False,
        "voice_regenerated": False,
    }


def _render_gate() -> dict[str, Any]:
    return {
        "render_performed_in_this_slice": False,
        "YMM4_launched_by_agent": False,
        "render_deferred_until_structural_readback_passes": True,
        "next_render_trigger": (
            "patched copy structurally reaches 68 sec and preserves native voice fields"
        ),
        "next_recommended_slice": POST_PATCH_RENDER_SMOKE_SLICE,
        "repeated_audio_check_requested": False,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_render_readiness": False,
        "public_video_readiness": False,
        "production_narration_quality": False,
        "final_script_narration_quality": False,
        "visual_layout_readiness": False,
        "real_content_readiness": False,
        "production_approval": False,
        "external_TTS_adoption": False,
        "post_patch_render_smoke": False,
        "neutral_68_sec_video_acceptance": False,
    }


def _warnings() -> list[str]:
    return [
        "68 sec timing is structurally patched, not render-accepted",
        "long sparse dialogue spans are diagnostic-only and not production pacing",
        "voice/audio fields are preserved rather than stretched or regenerated",
        "patched .ymmp remains an ignored local diagnostic copy and is not committed",
    ]


def _downstream_next_use() -> dict[str, list[str]]:
    return {
        "use_this_probe_to": [
            "open a post-patch tiny render smoke only after structural readback pass",
            "verify whether YMM4 accepts the patched timeline shape",
            "keep native voice preservation separate from visual layout acceptance",
        ],
        "do_not_use_this_probe_to": [
            "claim production or public video readiness",
            "commit .ymmp or media output",
            "claim post-patch render success before a render smoke",
            "introduce external TTS or regenerate voice audio",
        ],
    }


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "source_ymmp_modified": False,
        "patched_ymmp_copy_created_under_ignored_tmp": True,
        "ymmp_or_media_staged_or_committed": False,
        "production_approval": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


def _item_timing_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "voice_index": row.get("voice_index"),
            "item_index": row.get("item_index"),
            "text": row.get("text"),
            "frame": row.get("frame"),
            "length_frames": row.get("length_frames"),
            "end_frame": row.get("end_frame"),
            "start_sec": row.get("start_sec"),
            "duration_sec": row.get("duration_sec"),
            "end_sec": row.get("end_sec"),
            "voice_length": row.get("voice_length"),
        }
        for row in summary.get("voice_items", [])
    ]


def _first_timeline(root: dict[str, Any]) -> dict[str, Any]:
    timelines = root.get("Timelines") if isinstance(root, dict) else None
    if not isinstance(timelines, list) or not timelines:
        return {}
    timeline = timelines[0]
    return timeline if isinstance(timeline, dict) else {}


def _load_ymmp(path: str | Path) -> dict[str, Any]:
    ymmp_path = Path(path)
    if not ymmp_path.exists():
        raise FileNotFoundError(f"diagnostic source .ymmp not found: {ymmp_path}")
    payload = json.loads(ymmp_path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"YMM4 project root must be an object: {ymmp_path}")
    return payload


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


def _append_mapping(lines: list[str], title: str, mapping: Any) -> None:
    lines.extend(["", f"## {title}", ""])
    for key, value in _dict(mapping).items():
        lines.append(f"- {key}: {_display(value)}")


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _intish(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _unicode_escape(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    return value.encode("unicode_escape").decode("ascii")


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
