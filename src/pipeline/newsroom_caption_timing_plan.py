"""Diagnostic caption and timing plan for newsroom episode capsules.

This module consumes the already diagnostic-only episode production capsule and
builds a planning artifact. It does not fetch sources, create media, generate
TTS, write YMM4 projects, render output, or approve production use.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_episode_production_capsule import (
    DEFAULT_CAPSULE_PATH,
    load_json_object,
)


PLAN_SCHEMA_VERSION = "newsroom_caption_timing_plan.v1"
PLAN_ARTIFACT_ID = "newsroom_caption_timing_plan_v1_2026_06_22"
DEFAULT_PLAN_PATH = Path(
    "samples/_probe/newsroom_handoff/episode_caption_timing_plan_v1.json"
)
DEFAULT_PLAN_DOC_PATH = Path(
    "docs/verification/NEWSROOM_CAPTION_TIMING_PLAN_V1_2026-06-22.md"
)

CAPTION_NEXT_ALLOWED_STEPS: tuple[str, ...] = (
    "Review Console timing panel or preview extension",
    "YMM4 transfer candidate proof only after blockers are resolved",
    "caption copy refinement",
    "synthetic voice placeholder planning without TTS generation",
)


def build_default_newsroom_caption_timing_plan(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed caption/timing plan from the default capsule."""
    base = Path(root) if root is not None else Path(".")
    capsule = load_json_object(base / DEFAULT_CAPSULE_PATH)
    return build_newsroom_caption_timing_plan(capsule, capsule_path=DEFAULT_CAPSULE_PATH)


def build_newsroom_caption_timing_plan(
    capsule: dict[str, Any],
    *,
    capsule_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build a deterministic, diagnostic caption/timing plan."""
    beat_windows = _beat_windows(capsule)
    caption_units = _caption_units(capsule, beat_windows)
    visual_timing = _visual_timing(capsule, beat_windows)
    transfer = _dict(capsule.get("transfer_status"))
    audio = _dict(capsule.get("audio_voice_status"))
    timing = _dict(capsule.get("timing_approximation"))

    total_duration = int(timing.get("total_duration_seconds") or _covered_range(beat_windows))
    return {
        "artifact_id": PLAN_ARTIFACT_ID,
        "schema_version": PLAN_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_timing_plan_only",
        "source": {
            "capsule_path": _path_text(capsule_path),
            "capsule_artifact_id": capsule.get("artifact_id"),
            "capsule_schema_version": capsule.get("schema_version"),
            "episode_id": _dict(capsule.get("episode")).get("episode_id"),
            "source": "episode production capsule",
        },
        "episode_timing_summary": {
            "total_duration_sec": total_duration,
            "covered_range_sec": _covered_range(beat_windows),
            "beat_count": len(beat_windows),
            "caption_unit_count": len(caption_units),
            "visual_count": len(visual_timing),
            "timing_confidence": "low_provisional_from_capsule",
            "timing_basis": (
                "Capsule rough durations and narration placeholders only; no audio timing."
            ),
            "provisional_timing": True,
            "notes": [
                "Timing is a planning layer, not narration timing or YMM4 timing.",
                "Caption text is placeholder copy and should be refined before transfer review.",
                "Caption reserve is semantic only; geometry remains downstream/YMM4 blocked.",
            ],
        },
        "beat_timing": [
            {
                "beat_id": row["beat_id"],
                "start_sec": row["start_sec"],
                "end_sec": row["end_sec"],
                "duration_sec": row["duration_sec"],
                "narration_placeholder": row["narration_placeholder"],
                "caption_units": [
                    unit["caption_id"]
                    for unit in caption_units
                    if unit["beat_id"] == row["beat_id"]
                ],
                "visual_refs": row["visual_refs"],
                "source_refs": row["source_refs"],
                "blocker_refs": _blocker_refs(transfer),
            }
            for row in beat_windows
        ],
        "caption_units": caption_units,
        "visual_timing": visual_timing,
        "audio_readiness": {
            "voice_status": audio.get("audio_readiness") or "not_started",
            "voice_source": audio.get("voice_source") or "absent_synthetic_placeholder",
            "TTS_generated": False,
            "audio_timing_confidence": "low_no_audio",
            "blockers": [
                "audio voice, TTS, and narration timing are not started",
                "caption timing is placeholder-only until narration is approved",
            ],
        },
        "transfer_status": {
            "transfer_status": "blocked",
            "YMM4_candidate": False,
            "unlock_requirements": transfer.get("unlock_requirements", []),
            "prohibited_next_actions": capsule.get("prohibited_steps", []),
            "blocker_count": transfer.get("blocker_count"),
            "unlock_requirement_count": transfer.get("unlock_requirement_count"),
        },
        "next_allowed_steps": list(CAPTION_NEXT_ALLOWED_STEPS),
        "remaining_gaps_before_importable_proof": capsule.get(
            "remaining_gaps_before_importable_proof",
            [],
        ),
        "boundary_assertions": {
            "diagnostic_only": True,
            "public_video": False,
            "usable_public_video": False,
            "real_source_fetch_performed": False,
            "real_urls_accessed": False,
            "contains_real_urls": False,
            "contains_media": False,
            "external_media_downloaded": False,
            "tts_generated": False,
            "ymmp_generated": False,
            "ymm4_carrier_generated": False,
            "render_generated": False,
            "production_approval": False,
            "publishing_ready": False,
        },
    }


def render_newsroom_caption_timing_plan_markdown(plan: dict[str, Any]) -> str:
    """Render a human-readable readback for the caption/timing plan."""
    source = _dict(plan.get("source"))
    summary = _dict(plan.get("episode_timing_summary"))
    audio = _dict(plan.get("audio_readiness"))
    transfer = _dict(plan.get("transfer_status"))

    lines = [
        "# Newsroom Caption / Timing Plan v1",
        "",
        f"artifact_id: {plan.get('artifact_id')}",
        f"schema_version: {plan.get('schema_version')}",
        f"review_status: {plan.get('review_status')}",
        f"production_status: {plan.get('production_status')}",
        "diagnostic_only: true",
        "",
        "## Purpose",
        "",
        "This plan refines the diagnostic episode capsule into a caption and timing "
        "planning layer. It keeps transfer blocked and does not create audio, media, "
        "YMM4 projects, renders, or production-ready video output.",
        "",
        "## Episode Timing Summary",
        "",
        f"- episode_id: {source.get('episode_id')}",
        f"- total_duration_sec: {summary.get('total_duration_sec')}",
        f"- covered_range_sec: {summary.get('covered_range_sec')}",
        f"- beat_count: {summary.get('beat_count')}",
        f"- caption_unit_count: {summary.get('caption_unit_count')}",
        f"- visual_count: {summary.get('visual_count')}",
        f"- timing_confidence: {summary.get('timing_confidence')}",
        "",
        "## Video Readiness Matrix",
        "",
        "| area | status | note |",
        "|---|---|---|",
        "| timing | provisional | capsule rough durations only |",
        "| captions | placeholder_plan | copy and reading speed need review |",
        "| visuals | mapped_to_beats | schematic VisualIR / G-28 references only |",
        (
            "| audio | "
            f"{audio.get('voice_status')} | no TTS or audio timing exists |"
        ),
        (
            "| transfer | "
            f"{transfer.get('transfer_status')} | YMM4_candidate=false |"
        ),
        "",
        "## Beat Timing",
        "",
    ]
    for beat in plan.get("beat_timing", []):
        lines.append(
            f"- {beat['beat_id']}: {beat['start_sec']}-{beat['end_sec']}s "
            f"({beat['duration_sec']}s)"
        )
        lines.append(f"  captions: {', '.join(beat.get('caption_units', [])) or 'none'}")
        lines.append(f"  visuals: {', '.join(beat.get('visual_refs', [])) or 'none'}")
        lines.append(f"  sources: {', '.join(beat.get('source_refs', [])) or 'none'}")

    lines.extend(["", "## Caption Units", ""])
    for unit in plan.get("caption_units", []):
        lines.append(
            f"- {unit['caption_id']}: {unit['start_sec']}-{unit['end_sec']}s "
            f"beat={unit['beat_id']} max_chars={unit['max_chars_target']} "
            f"lines={unit['line_count_target']}"
        )
        lines.append(f"  placeholder: {unit['text_placeholder']}")
        lines.append(f"  reserve: {unit['caption_reserve_status']}")

    lines.extend(["", "## Visual Timing", ""])
    for visual in plan.get("visual_timing", []):
        lines.append(
            f"- {visual['visual_id']}: {visual['start_sec']}-{visual['end_sec']}s "
            f"beat={visual['beat_id']} slot={visual['g28_slot']}"
        )
        lines.append(
            f"  layout={visual['layout_hint']}; caption risk={visual['caption_interference_risk']}"
        )
        lines.append(f"  review_surface_ref: {visual['review_surface_ref']}")

    lines.extend([
        "",
        "## Transfer And Boundary",
        "",
        f"transfer_status: {transfer.get('transfer_status')}",
        f"YMM4_candidate: {str(transfer.get('YMM4_candidate')).lower()}",
        f"TTS_generated: {str(audio.get('TTS_generated')).lower()}",
        "",
        "Prohibited next actions:",
    ])
    for action in transfer.get("prohibited_next_actions", []):
        lines.append(f"- {action}")

    lines.extend(["", "Next allowed steps:"])
    for step in plan.get("next_allowed_steps", []):
        lines.append(f"- {step}")

    lines.extend([
        "",
        "## Remaining Gaps",
        "",
    ])
    for gap in plan.get("remaining_gaps_before_importable_proof", []):
        lines.append(f"- {gap}")

    lines.extend([
        "",
        "## Boundary",
        "",
        "This readback is diagnostic-only. It is a timing/caption planning layer, "
        "not public video, not an importable proof, and not a production approval.",
        "",
    ])
    return "\n".join(lines)


def _beat_windows(capsule: dict[str, Any]) -> list[dict[str, Any]]:
    cursor = 0
    rows: list[dict[str, Any]] = []
    for beat in _list(capsule.get("script_structure")):
        duration = int(beat.get("rough_duration_seconds") or 0)
        start = cursor
        end = start + duration
        rows.append({
            "beat_id": beat.get("beat_id"),
            "start_sec": start,
            "end_sec": end,
            "duration_sec": duration,
            "narration_placeholder": beat.get("expected_narration_placeholder"),
            "visual_refs": _string_list(beat.get("visual_refs")),
            "source_refs": _string_list(beat.get("source_note_refs")),
        })
        cursor = end
    return rows


def _caption_units(
    capsule: dict[str, Any],
    beat_windows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    caption_status_by_beat = _caption_reserve_by_beat(capsule)
    units: list[dict[str, Any]] = []
    for beat in beat_windows:
        chunks = _caption_chunks(str(beat.get("narration_placeholder") or ""))
        split_count = max(1, len(chunks))
        unit_duration = beat["duration_sec"] / split_count if split_count else beat["duration_sec"]
        for index, chunk in enumerate(chunks, start=1):
            start = beat["start_sec"] + math.floor(unit_duration * (index - 1))
            end = beat["end_sec"] if index == split_count else beat["start_sec"] + math.floor(unit_duration * index)
            units.append({
                "caption_id": f"cap_{beat['beat_id']}_{index:02d}",
                "beat_id": beat["beat_id"],
                "text_placeholder": chunk,
                "start_sec": start,
                "end_sec": end,
                "max_chars_target": 34,
                "line_count_target": 2,
                "reading_speed_note": "placeholder_copy_only_not_final_narration",
                "caption_reserve_status": caption_status_by_beat.get(
                    beat["beat_id"],
                    "unknown_semantic_reserve",
                ),
            })
    return units


def _caption_chunks(text: str) -> list[str]:
    stripped = text.strip().rstrip(".")
    if not stripped:
        return ["Placeholder narration copy not yet written."]
    for separator in [" with ", " and "]:
        if separator in stripped:
            parts = [part.strip() for part in stripped.split(separator, 1)]
            return [
                _sentence(parts[0]),
                _sentence(_sentence_start(parts[1])),
            ]
    return [_sentence(stripped)]


def _visual_timing(
    capsule: dict[str, Any],
    beat_windows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    window_by_beat = {row["beat_id"]: row for row in beat_windows}
    result: list[dict[str, Any]] = []
    for visual in _list(capsule.get("visual_structure")):
        beat_id = visual.get("beat_id")
        window = window_by_beat.get(beat_id, {})
        slot_refs = _list(visual.get("g28_slot_refs"))
        selected_slot = (
            slot_refs[0].get("object_catalog_slot")
            if slot_refs
            else "missing_g28_slot"
        )
        result.append({
            "visual_id": visual.get("visual_id"),
            "beat_id": beat_id,
            "start_sec": window.get("start_sec", 0),
            "end_sec": window.get("end_sec", 0),
            "g28_slot": selected_slot,
            "layout_hint": visual.get("layout_candidate") or visual.get("visualir_concept"),
            "caption_interference_risk": _caption_interference_risk(visual),
            "review_surface_ref": _review_surface_ref(visual),
        })
    return result


def _caption_reserve_by_beat(capsule: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for visual in _list(capsule.get("visual_structure")):
        beat_id = visual.get("beat_id")
        if not isinstance(beat_id, str):
            continue
        reserve_status = _dict(visual.get("caption_reserve")).get("status")
        result[beat_id] = (
            "present_semantic_only"
            if reserve_status == "present"
            else "missing_or_unverified"
        )
    return result


def _caption_interference_risk(visual: dict[str, Any]) -> str:
    unhinted = set(_string_list(visual.get("unhinted_content_slots")))
    if "caption_reserve" in unhinted:
        return "medium_unhinted_caption_reserve"
    if _dict(visual.get("caption_reserve")).get("status") == "present":
        return "low_semantic_reserve_present"
    return "unknown_caption_reserve"


def _review_surface_ref(visual: dict[str, Any]) -> str:
    for ref in _list(visual.get("review_surface_refs")):
        if ref.get("kind") == "reference_layout" and ref.get("path"):
            return str(ref["path"])
    refs = _list(visual.get("review_surface_refs"))
    return str(refs[0].get("path")) if refs and refs[0].get("path") else "missing"


def _blocker_refs(transfer: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for category, blockers in _dict(transfer.get("blockers")).items():
        for blocker in _list(blockers):
            code = blocker.get("code")
            if code:
                refs.append(f"{category}:{code}")
    return refs


def _covered_range(beat_windows: list[dict[str, Any]]) -> int:
    if not beat_windows:
        return 0
    return int(max(row["end_sec"] for row in beat_windows) - min(row["start_sec"] for row in beat_windows))


def _sentence(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        return "Placeholder narration copy not yet written."
    return stripped if stripped.endswith(".") else f"{stripped}."


def _sentence_start(value: str) -> str:
    stripped = value.strip()
    return f"{stripped[:1].upper()}{stripped[1:]}" if stripped else stripped


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None
