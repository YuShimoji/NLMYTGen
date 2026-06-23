"""Structure readback for the diagnostic newsroom .ymmp project.

This module parses the locally saved diagnostic .ymmp only far enough to record
structural evidence. It does not launch YMM4, edit or commit .ymmp, render,
generate TTS/audio, import real media, fetch external sources, or approve
production use.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_diagnostic_ymmp_manual_result import (
    DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH,
    LOCAL_DIAGNOSTIC_YMMP_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_minimal_ymmp_boundary_decision import (
    DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH,
)
from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    EXPECTED_MANUAL_IMPORT_ROW_COUNT,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    OBSERVED_MANUAL_CHARACTER,
)


DIAGNOSTIC_YMMP_STRUCTURE_READBACK_SCHEMA_VERSION = (
    "newsroom_diagnostic_ymmp_structure_readback.v1"
)
DIAGNOSTIC_YMMP_STRUCTURE_READBACK_ID = (
    "newsroom_diagnostic_ymmp_structure_readback_v1_2026_06_23"
)
DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/diagnostic_ymmp_structure_readback_v1.json"
)
DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_DOC_PATH = Path(
    "docs/verification/NEWSROOM_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_V1_2026-06-23.md"
)


def build_default_newsroom_diagnostic_ymmp_structure_readback(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed structure readback from local diagnostic .ymmp."""
    base = Path(root) if root is not None else Path(".")
    manual_result = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH
    )
    boundary_decision = load_json_object(
        base / DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH
    )
    source_ymmp_path = LOCAL_DIAGNOSTIC_YMMP_PATH
    parse = parse_diagnostic_ymmp_structure(base / source_ymmp_path)
    return build_newsroom_diagnostic_ymmp_structure_readback(
        parse,
        manual_result,
        boundary_decision,
        source_ymmp_path=source_ymmp_path,
        source_manual_result_readback_path=(
            DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH
        ),
    )


def parse_diagnostic_ymmp_structure(path: str | Path) -> dict[str, Any]:
    """Parse a diagnostic .ymmp JSON file into bounded structural facts."""
    ymmp_path = Path(path)
    if not ymmp_path.exists():
        return {
            "ymmp_found": False,
            "parse_status": "failed",
            "parse_method": "python json utf-8-sig bounded structure read",
            "warnings": ["YMMP_FILE_NOT_FOUND"],
            "raw": {},
        }

    try:
        root = json.loads(ymmp_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError, UnicodeError) as exc:
        return {
            "ymmp_found": True,
            "parse_status": "failed",
            "parse_method": "python json utf-8-sig bounded structure read",
            "warnings": [f"YMMP_PARSE_FAILED:{type(exc).__name__}"],
            "raw": {},
        }

    timelines = root.get("Timelines") if isinstance(root, dict) else None
    timeline = timelines[0] if isinstance(timelines, list) and timelines else {}
    items = timeline.get("Items") if isinstance(timeline, dict) else []
    items = [item for item in items if isinstance(item, dict)]
    video_info = timeline.get("VideoInfo") if isinstance(timeline, dict) else {}
    fps = _number(_dict(video_info).get("FPS"))
    timeline_length = _number(timeline.get("Length")) if isinstance(timeline, dict) else None
    duration_sec = (
        round(timeline_length / fps, 6)
        if timeline_length is not None and fps not in (None, 0)
        else None
    )

    warnings: list[str] = []
    if len(items) != EXPECTED_MANUAL_IMPORT_ROW_COUNT:
        warnings.append("DIALOGUE_ITEM_COUNT_DIFFERS_FROM_EXPECTED")

    return {
        "ymmp_found": True,
        "parse_status": "parsed" if not warnings else "parsed_with_warnings",
        "parse_method": "python json utf-8-sig bounded structure read",
        "warnings": warnings,
        "project": {
            "top_level_keys": sorted(root.keys()) if isinstance(root, dict) else [],
            "timeline_count": len(timelines) if isinstance(timelines, list) else 0,
            "selected_timeline_index": root.get("SelectedTimelineIndex"),
            "character_count": len(root.get("Characters", []))
            if isinstance(root, dict) and isinstance(root.get("Characters"), list)
            else 0,
            "video_info": video_info,
        },
        "timeline": {
            "name": timeline.get("Name") if isinstance(timeline, dict) else None,
            "length_frames": timeline_length,
            "fps": fps,
            "duration_sec": duration_sec,
            "max_layer": timeline.get("MaxLayer")
            if isinstance(timeline, dict)
            else None,
            "item_count": len(items),
        },
        "items": [_item_summary(index, item, fps) for index, item in enumerate(items)],
        "characters": _character_summaries(root.get("Characters", [])),
    }


def build_newsroom_diagnostic_ymmp_structure_readback(
    parse: dict[str, Any],
    manual_result: dict[str, Any],
    boundary_decision: dict[str, Any],
    *,
    source_ymmp_path: str | Path,
    source_manual_result_readback_path: str | Path,
) -> dict[str, Any]:
    """Build the diagnostic .ymmp structure readback artifact."""
    dialogue = _dialogue_structure(parse)
    timing = _timing_structure(parse, boundary_decision)
    audio = _audio_tts_structure(parse)
    boundary = _boundary()
    accepted_scope = _accepted_scope()
    not_accepted_scope = _not_accepted_scope()

    return {
        "artifact_id": DIAGNOSTIC_YMMP_STRUCTURE_READBACK_ID,
        "readback_id": DIAGNOSTIC_YMMP_STRUCTURE_READBACK_ID,
        "schema_version": DIAGNOSTIC_YMMP_STRUCTURE_READBACK_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "ymmp_committed": False,
        "identity": {
            "readback_id": DIAGNOSTIC_YMMP_STRUCTURE_READBACK_ID,
            "source_ymmp_path": _path_text(source_ymmp_path),
            "source_manual_result_readback_path": _path_text(
                source_manual_result_readback_path
            ),
            "source_manual_result_id": manual_result.get("result_id"),
            "production_status": "diagnostic_only",
            "ymmp_committed": False,
        },
        "parse_status": {
            "ymmp_found": parse.get("ymmp_found"),
            "parse_status": parse.get("parse_status"),
            "parse_method": parse.get("parse_method"),
            "warnings": parse.get("warnings", []),
        },
        "project_structure": parse.get("project", {}),
        "dialogue_structure": dialogue,
        "timing_structure": timing,
        "audio_tts_structure": audio,
        "accepted_scope": accepted_scope,
        "not_accepted_scope": not_accepted_scope,
        "boundary": boundary,
        "review_memory": {
            "review_source": "diagnostic_ymmp_manual_result_readback",
            "prior_user_review_count": {
                "manual_import_behavior": 1,
                "bound_speaker_behavior": 1,
                "diagnostic_ymmp_manual_observation": 1,
                "ymmp_structure_readback": 0,
            },
            "accepted_scope": accepted_scope,
            "not_accepted_scope": not_accepted_scope,
            "next_nonredundant_axis": [
                "newsroom-yym4-timing-gap-strategy-v1",
                "newsroom-audio-tts-boundary-v1",
                "newsroom-tiny-render-smoke-boundary-v1",
            ],
            "repeated_general_review_allowed": False,
            "input_mode": "freeform",
        },
        "human_burden_hygiene": {
            "user_input": "freeform",
            "template_required": False,
            "schema_owner": "Agent",
            "max_required_points": 0,
            "screenshot_optional": True,
            "negative_confirmations_required_from_user": False,
            "fixed_form_result_template": False,
            "user_side_work_this_slice": "none",
        },
        "downstream_next_use": {
            "use_this_readback_to": [
                "compare natural YMM4 project duration with neutral timeline timing",
                "decide whether voice cache presence changes the audio/TTS boundary",
                "decide the smallest safe render-smoke boundary without production approval",
            ],
            "do_not_use_this_readback_to": [
                "commit .ymmp files",
                "claim production .ymmp readiness",
                "claim render readiness",
                "claim TTS readiness",
                "claim timing patch strategy completion",
                "publish or prepare a public video",
            ],
        },
        "next_recommended_axes": [
            "newsroom-yym4-timing-gap-strategy-v1",
            "newsroom-audio-tts-boundary-v1",
            "newsroom-tiny-render-smoke-boundary-v1",
        ],
        "review_debt": {
            "generic_review_card_emitted": False,
            "reason": (
                "This is an agent-owned structure readback from a local "
                "diagnostic .ymmp. No manual observation is re-requested."
            ),
        },
    }


def render_newsroom_diagnostic_ymmp_structure_readback_markdown(
    readback: dict[str, Any],
) -> str:
    """Render a human-readable diagnostic .ymmp structure readback."""
    identity = _dict(readback.get("identity"))
    parse_status = _dict(readback.get("parse_status"))
    dialogue = _dict(readback.get("dialogue_structure"))
    timing = _dict(readback.get("timing_structure"))
    audio = _dict(readback.get("audio_tts_structure"))
    hygiene = _dict(readback.get("human_burden_hygiene"))

    lines = [
        "# Newsroom Diagnostic .ymmp Structure Readback v1",
        "",
        f"artifact_id: {readback.get('artifact_id')}",
        f"readback_id: {readback.get('readback_id')}",
        f"schema_version: {readback.get('schema_version')}",
        f"review_status: {readback.get('review_status')}",
        f"production_status: {readback.get('production_status')}",
        f"ymmp_committed: {_display(readback.get('ymmp_committed'))}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        f"- source_ymmp_path: {identity.get('source_ymmp_path')}",
        (
            "- source_manual_result_readback_path: "
            f"{identity.get('source_manual_result_readback_path')}"
        ),
        "",
        "## Parse Status",
        "",
    ]
    for key, value in parse_status.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Dialogue Structure",
            "",
            f"- dialogue_item_count: {dialogue.get('dialogue_item_count')}",
            (
                "- expected_dialogue_item_count: "
                f"{dialogue.get('expected_dialogue_item_count')}"
            ),
            f"- canonical_speaker_value: {dialogue.get('canonical_speaker_value')}",
            f"- raw_speaker_values: {_display(dialogue.get('raw_speaker_values'))}",
            f"- item_type_names: {_display(dialogue.get('item_type_names'))}",
            "- items:",
        ]
    )
    for item in dialogue.get("items", []):
        lines.append(
            "  - "
            f"index={item.get('index')} frame={item.get('frame')} "
            f"length={item.get('length_frames')} "
            f"text={item.get('text')!r}"
        )

    lines.extend(["", "## Timing Structure", ""])
    for key, value in timing.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Audio / TTS Structure", ""])
    for key, value in audio.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(readback.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Boundary", ""])
    for key, value in _dict(readback.get("boundary")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Human Burden Hygiene", ""])
    for key, value in hygiene.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Next Recommended Axes", ""])
    for axis in readback.get("next_recommended_axes", []):
        lines.append(f"- {axis}")

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This readback parses a local diagnostic `.ymmp` for structure only. "
            "It does not stage or commit `.ymmp`, launch YMM4, render, generate "
            "TTS/audio, import real media, approve production, or prepare a "
            "public video.",
            "",
        ]
    )
    return "\n".join(lines)


def _item_summary(index: int, item: dict[str, Any], fps: float | None) -> dict[str, Any]:
    frame = _number(item.get("Frame"))
    length = _number(item.get("Length"))
    return {
        "index": index,
        "type_name": item.get("$type"),
        "frame": frame,
        "start_sec": round(frame / fps, 6) if frame is not None and fps else None,
        "length_frames": length,
        "duration_sec": round(length / fps, 6) if length is not None and fps else None,
        "layer": item.get("Layer"),
        "character_name_raw": item.get("CharacterName"),
        "text": item.get("Serif"),
        "pronounce_present": isinstance(item.get("Pronounce"), dict),
        "hatsuon_present": bool(item.get("Hatsuon")),
        "voice_length": item.get("VoiceLength"),
        "voice_cache_present": bool(item.get("VoiceCache")),
        "voice_cache_char_count": len(item.get("VoiceCache") or ""),
        "audio_effect_count": len(item.get("AudioEffects") or []),
        "voice_fade_in": item.get("VoiceFadeIn"),
        "voice_fade_out": item.get("VoiceFadeOut"),
        "additional_time": item.get("AdditionalTime"),
        "playback_rate": item.get("PlaybackRate"),
    }


def _character_summaries(characters: Any) -> list[dict[str, Any]]:
    if not isinstance(characters, list):
        return []
    rows = []
    for character in characters:
        if not isinstance(character, dict):
            continue
        rows.append(
            {
                "name_raw": character.get("Name"),
                "group_name_raw": character.get("GroupName"),
                "voice_api": _dict(character.get("Voice")).get("API"),
                "voice_arg": _dict(character.get("Voice")).get("Arg"),
                "additional_time": character.get("AdditionalTime"),
                "voice_fade_in": character.get("VoiceFadeIn"),
                "voice_fade_out": character.get("VoiceFadeOut"),
                "audio_effect_count": len(character.get("AudioEffects") or []),
            }
        )
    return rows


def _dialogue_structure(parse: dict[str, Any]) -> dict[str, Any]:
    items = parse.get("items", [])
    raw_speakers = sorted(
        {
            item.get("character_name_raw")
            for item in items
            if isinstance(item, dict) and item.get("character_name_raw")
        }
    )
    item_types = sorted(
        {
            item.get("type_name")
            for item in items
            if isinstance(item, dict) and item.get("type_name")
        }
    )
    return {
        "dialogue_item_count": len(items),
        "expected_dialogue_item_count": EXPECTED_MANUAL_IMPORT_ROW_COUNT,
        "item_type_names": item_types,
        "text_fields": ["Serif"],
        "speaker_character_fields": ["CharacterName"],
        "text_summaries": [item.get("text") for item in items],
        "canonical_speaker_value": OBSERVED_MANUAL_CHARACTER,
        "raw_speaker_values": raw_speakers,
        "encoding_note": (
            "Raw .ymmp speaker strings may display differently in terminals; "
            "the UI-observed speaker value remains canonical."
        ),
        "items": items,
    }


def _timing_structure(
    parse: dict[str, Any],
    boundary_decision: dict[str, Any],
) -> dict[str, Any]:
    timeline = _dict(parse.get("timeline"))
    timing = _dict(boundary_decision.get("timing_gap_policy"))
    return {
        "observed_project_duration_sec": timeline.get("duration_sec"),
        "observed_project_duration_frames": timeline.get("length_frames"),
        "fps": timeline.get("fps"),
        "item_start_duration_fields": ["Frame", "Length", "VoiceLength"],
        "item_timings": [
            {
                "index": item.get("index"),
                "frame": item.get("frame"),
                "length_frames": item.get("length_frames"),
                "start_sec": item.get("start_sec"),
                "duration_sec": item.get("duration_sec"),
                "voice_length": item.get("voice_length"),
            }
            for item in parse.get("items", [])
            if isinstance(item, dict)
        ],
        "timing_gap_status": "unresolved",
        "neutral_timeline_total_sec": timing.get("neutral_timeline_total_sec"),
        "prior_observed_yym4_import_approx_sec": timing.get(
            "observed_yym4_import_approx_sec"
        ),
        "ymmp_natural_duration_observed": (
            "short_natural_duration"
            if timeline.get("duration_sec") is not None
            else "unknown"
        ),
        "timing_patch_applied": False,
    }


def _audio_tts_structure(parse: dict[str, Any]) -> dict[str, Any]:
    items = [item for item in parse.get("items", []) if isinstance(item, dict)]
    characters = [
        item for item in parse.get("characters", []) if isinstance(item, dict)
    ]
    return {
        "voice_audio_related_fields_present": [
            "VoiceLength",
            "VoiceCache",
            "VoiceParameter",
            "Pronounce",
            "Hatsuon",
            "AudioEffects",
        ],
        "voice_item_count": len(items),
        "voice_cache_item_count": sum(
            1 for item in items if item.get("voice_cache_present")
        ),
        "audio_effect_total_count": sum(
            int(item.get("audio_effect_count") or 0) for item in items
        ),
        "character_voice_apis": sorted(
            {
                character.get("voice_api")
                for character in characters
                if character.get("voice_api")
            }
        ),
        "TTS_generated_by_agent": False,
        "explicit_operator_TTS_generation": False,
        "TTS_ready": False,
        "audio_boundary_note": (
            "Voice cache/voice fields are present in the saved diagnostic "
            ".ymmp, but this does not establish TTS readiness."
        ),
    }


def _accepted_scope() -> dict[str, bool]:
    return {
        "ymmp_structure_parsed_for_diagnostic_readback": True,
        "dialogue_rows_found": True,
        "speaker_raw_fields_recorded": True,
        "short_natural_timing_fields_recorded": True,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_ymmp_ready": False,
        "render_readiness": False,
        "TTS_readiness": False,
        "timing_patch_strategy": False,
        "public_video_readiness": False,
    }


def _boundary() -> dict[str, bool]:
    return {
        "render_created": False,
        "real_media_imported": False,
        "production_approval": False,
        "public_video_ready": False,
        "ymmp_staged_or_committed": False,
        "agent_launched_yym4": False,
        "agent_created_or_edited_ymmp": False,
        "TTS_generated_by_agent": False,
        "external_fetch_performed": False,
    }


def _number(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
