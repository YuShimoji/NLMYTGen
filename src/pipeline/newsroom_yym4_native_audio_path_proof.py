"""YMM4 native audio path proof for the diagnostic newsroom lane.

This module proves only the next diagnostic responsibility choice. It does not
launch YMM4, render, generate TTS/audio, import real media, fetch external
sources, edit or commit .ymmp/media files, or approve production use.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_audio_tts_boundary import (
    DEFAULT_AUDIO_TTS_BOUNDARY_PATH,
    DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH,
)
from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
    DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object


YYM4_NATIVE_AUDIO_PATH_PROOF_SCHEMA_VERSION = (
    "newsroom_yym4_native_audio_path_proof.v1"
)
YYM4_NATIVE_AUDIO_PATH_PROOF_ID = (
    "newsroom_yym4_native_audio_path_proof_v1_2026_06_24"
)
DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH = Path(
    "samples/_probe/newsroom_handoff/yym4_native_audio_path_proof_v1.json"
)
DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YYM4_NATIVE_AUDIO_PATH_PROOF_V1_2026-06-24.md"
)

RECOMMENDED_DEFAULT = (
    "continue_with_YMM4_native_voice_audio_path_for_diagnostic_flow"
)
NEXT_RECOMMENDED_SLICE = "newsroom-ymmp-timing-patch-strategy-v1"
AUDIO_OBSERVATION_SLICE = "newsroom-tiny-render-audio-observation-card-v1"
FIELD_AUDIT_SLICE = "newsroom-yym4-native-audio-field-audit-v1"


def build_default_newsroom_yym4_native_audio_path_proof(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed native audio path proof from source readbacks."""
    base = Path(root) if root is not None else Path(".")
    audio_boundary = load_json_object(base / DEFAULT_AUDIO_TTS_BOUNDARY_PATH)
    render_result = load_json_object(
        base / DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    structure_readback = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
    )
    return build_newsroom_yym4_native_audio_path_proof(
        audio_boundary,
        render_result,
        structure_readback,
        source_audio_tts_boundary_path=DEFAULT_AUDIO_TTS_BOUNDARY_PATH,
        source_tiny_render_result_path=(
            DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        source_ymmp_structure_readback_path=(
            DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
        ),
    )


def build_newsroom_yym4_native_audio_path_proof(
    audio_boundary: dict[str, Any],
    render_result: dict[str, Any],
    structure_readback: dict[str, Any],
    *,
    source_audio_tts_boundary_path: str | Path,
    source_tiny_render_result_path: str | Path,
    source_ymmp_structure_readback_path: str | Path,
) -> dict[str, Any]:
    """Build a diagnostic-only YMM4 native voice/audio path proof."""
    source_validation = _source_validation(
        audio_boundary,
        render_result,
        structure_readback,
    )
    native_evidence = _native_audio_evidence(structure_readback)
    proof_status = (
        "passed_with_unknowns"
        if not source_validation["errors"] and native_evidence["native_audio_path_candidate"]
        else "blocked"
    )
    not_accepted = _not_accepted_scope()

    return {
        "artifact_id": YYM4_NATIVE_AUDIO_PATH_PROOF_ID,
        "proof_id": YYM4_NATIVE_AUDIO_PATH_PROOF_ID,
        "schema_version": YYM4_NATIVE_AUDIO_PATH_PROOF_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "proof_status": proof_status,
        "identity": {
            "proof_id": YYM4_NATIVE_AUDIO_PATH_PROOF_ID,
            "source_audio_tts_boundary_path": _path_text(
                source_audio_tts_boundary_path
            ),
            "source_audio_tts_boundary_id": audio_boundary.get("boundary_id"),
            "source_tiny_render_result_path": _path_text(
                source_tiny_render_result_path
            ),
            "source_tiny_render_result_id": render_result.get("result_id"),
            "source_ymmp_structure_readback_path": _path_text(
                source_ymmp_structure_readback_path
            ),
            "source_ymmp_structure_readback_id": structure_readback.get(
                "readback_id"
            ),
            "production_status": "diagnostic_only",
            "proof_status": proof_status,
        },
        "source_validation": source_validation,
        "known_render_state": _known_render_state(render_result),
        "native_audio_evidence_from_ymmp": native_evidence,
        "audio_tts_knowns_and_unknowns": _audio_tts_knowns_and_unknowns(
            audio_boundary,
            native_evidence,
        ),
        "responsibility_split": _responsibility_split(),
        "recommended_default": {
            "choice": RECOMMENDED_DEFAULT,
            "reasoning": [
                "The tiny render smoke already passed at diagnostic scope.",
                "The parsed .ymmp has YMM4 voice fields, VoiceCache, voice lengths, and AquesTalk as the native engine hint.",
                "External TTS would introduce a second audio/timing responsibility before the native path is exhausted.",
                "The neutral 68 second timing patch can be planned next without claiming audio quality or production readiness.",
            ],
            "do_now": [
                "treat the YMM4 native voice/audio path as the diagnostic default",
                "carry audio presence in the rendered file as unknown",
                "keep external TTS closed for this lane",
                "move next to timing patch strategy if no separate audio-presence decision is requested",
            ],
            "defer": [
                "audio presence acceptance",
                "audio quality acceptance",
                "TTS readiness",
                "external TTS generation",
                "production render or public video readiness",
            ],
        },
        "next_path": {
            "recommended_next_slice": NEXT_RECOMMENDED_SLICE,
            "reason": (
                "Native YMM4 voice fields are sufficient to keep the native path "
                "as the diagnostic default; the remaining unknown is audible "
                "presence/quality, not field sufficiency."
            ),
            "if_audio_presence_becomes_the_next_bottleneck": (
                AUDIO_OBSERVATION_SLICE
            ),
            "if_native_fields_drift_or_are_later_missing": FIELD_AUDIT_SLICE,
            "do_not_recommend": "production_render_immediately",
        },
        "boundaries": _boundaries(),
        "review_memory": {
            "review_source": "audio_tts_boundary_plus_structure_readback",
            "checked": True,
            "prior_evidence_reused": [
                "newsroom-audio-tts-boundary-v1",
                "tiny render smoke result readback",
                "diagnostic .ymmp structure readback",
                "YMM4 timing gap strategy",
            ],
            "next_nonredundant_axis": [
                NEXT_RECOMMENDED_SLICE,
                AUDIO_OBSERVATION_SLICE,
                FIELD_AUDIT_SLICE,
            ],
            "not_accepted_scope": not_accepted,
            "repeated_general_review_allowed": False,
            "user_side_work_re_requested": False,
            "input_mode": "freeform",
        },
        "human_burden_hygiene": {
            "user_input": "freeform",
            "template_required": False,
            "schema_owner": "Agent",
            "user_side_work_this_slice": "none",
            "operator_observation_card": "not_needed_this_slice",
            "future_observation_max_required_points": 3,
            "screenshot_optional": True,
            "negative_confirmations_required_from_user": False,
            "fixed_form_result_template": False,
        },
        "not_accepted_scope": not_accepted,
        "timing_interaction": {
            "first_render_smoke_used_natural_duration": True,
            "first_smoke_duration_sec": _dict(
                render_result.get("normalized_result")
            ).get("output_duration_observed_sec"),
            "prior_ymmp_natural_duration_sec": _dict(
                structure_readback.get("timing_structure")
            ).get("observed_project_duration_sec"),
            "neutral_68_sec_timing_patch_applied": False,
            "neutral_68_sec_timing_patch_remains_deferred_until_next_slice": True,
            "audio_quality_or_presence_not_required_for_this_proof": True,
        },
        "downstream_next_use": {
            "use_this_proof_to": [
                "keep YMM4 native voice/audio as the default diagnostic path",
                "avoid introducing external TTS before native fields are exhausted",
                "separate field sufficiency from audible output acceptance",
                "open the timing patch strategy without production render claims",
            ],
            "do_not_use_this_proof_to": [
                "claim audio is present in the render",
                "claim audio quality acceptance",
                "claim TTS readiness",
                "generate or import audio",
                "stage or commit .ymmp, mp4, wav, mp3, or media output",
                "claim production or public video readiness",
            ],
        },
    }


def render_newsroom_yym4_native_audio_path_proof_markdown(
    proof: dict[str, Any],
) -> str:
    """Render a human-readable YMM4 native audio path proof."""
    identity = _dict(proof.get("identity"))
    validation = _dict(proof.get("source_validation"))
    render_state = _dict(proof.get("known_render_state"))
    native = _dict(proof.get("native_audio_evidence_from_ymmp"))
    knowns = _dict(proof.get("audio_tts_knowns_and_unknowns"))
    recommended = _dict(proof.get("recommended_default"))
    next_path = _dict(proof.get("next_path"))
    boundaries = _dict(proof.get("boundaries"))
    hygiene = _dict(proof.get("human_burden_hygiene"))
    timing = _dict(proof.get("timing_interaction"))

    lines = [
        "# Newsroom YMM4 Native Audio Path Proof v1",
        "",
        f"artifact_id: {proof.get('artifact_id')}",
        f"proof_id: {proof.get('proof_id')}",
        f"schema_version: {proof.get('schema_version')}",
        f"review_status: {proof.get('review_status')}",
        f"production_status: {proof.get('production_status')}",
        f"proof_status: {proof.get('proof_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        (
            "- source_audio_tts_boundary_path: "
            f"{identity.get('source_audio_tts_boundary_path')}"
        ),
        (
            "- source_audio_tts_boundary_id: "
            f"{identity.get('source_audio_tts_boundary_id')}"
        ),
        (
            "- source_tiny_render_result_path: "
            f"{identity.get('source_tiny_render_result_path')}"
        ),
        (
            "- source_tiny_render_result_id: "
            f"{identity.get('source_tiny_render_result_id')}"
        ),
        (
            "- source_ymmp_structure_readback_path: "
            f"{identity.get('source_ymmp_structure_readback_path')}"
        ),
        (
            "- source_ymmp_structure_readback_id: "
            f"{identity.get('source_ymmp_structure_readback_id')}"
        ),
        "",
        "## Source Validation",
        "",
        f"- status: {validation.get('status')}",
        f"- errors: {_display(validation.get('errors'))}",
        f"- canonical_speaker_value: {validation.get('canonical_speaker_value')}",
        (
            "- canonical_speaker_unicode_escape: "
            f"{validation.get('canonical_speaker_unicode_escape')}"
        ),
        "",
        "## Known Render State",
        "",
    ]
    for key, value in render_state.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Native Audio Evidence From .ymmp", ""])
    for key, value in native.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Known / Unknown Audio State", ""])
    for key, value in knowns.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Responsibility Split",
            "",
            "| path | role | benefits | risks | enables | defers |",
            "|---|---|---|---|---|---|",
        ]
    )
    for item in proof.get("responsibility_split", []):
        lines.append(
            "| "
            f"{item.get('path_id')} | "
            f"{item.get('role')} | "
            f"{'; '.join(item.get('benefits', []))} | "
            f"{'; '.join(item.get('risks', []))} | "
            f"{'; '.join(item.get('what_it_enables', []))} | "
            f"{'; '.join(item.get('what_it_defers', []))} |"
        )

    lines.extend(
        [
            "",
            "## Recommended Default",
            "",
            f"- choice: {recommended.get('choice')}",
            "- reasoning:",
        ]
    )
    for item in recommended.get("reasoning", []):
        lines.append(f"  - {item}")
    lines.append("- do_now:")
    for item in recommended.get("do_now", []):
        lines.append(f"  - {item}")
    lines.append("- defer:")
    for item in recommended.get("defer", []):
        lines.append(f"  - {item}")

    lines.extend(["", "## Next Path", ""])
    for key, value in next_path.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Timing Interaction", ""])
    for key, value in timing.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Boundaries", ""])
    for key, value in boundaries.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Human Burden Hygiene", ""])
    for key, value in hygiene.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This proof accepts the YMM4 native voice/audio path as the next "
            "diagnostic default with unknowns preserved. It does not prove "
            "audio presence, audio quality, TTS readiness, production render "
            "readiness, public video readiness, or production approval.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    audio_boundary: dict[str, Any],
    render_result: dict[str, Any],
    structure_readback: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    boundary_knowns = _dict(audio_boundary.get("audio_tts_knowns_and_unknowns"))
    normalized = _dict(render_result.get("normalized_result"))
    parse_status = _dict(structure_readback.get("parse_status"))
    dialogue = _dict(structure_readback.get("dialogue_structure"))
    audio = _dict(structure_readback.get("audio_tts_structure"))
    fields = audio.get("voice_audio_related_fields_present", [])

    if audio_boundary.get("production_status") != "diagnostic_only":
        errors.append("AUDIO_BOUNDARY_NOT_DIAGNOSTIC_ONLY")
    if audio_boundary.get("boundary_status") != "accepted_for_next_audio_observation":
        errors.append("AUDIO_BOUNDARY_NOT_ACCEPTED")
    if render_result.get("production_status") != "diagnostic_only":
        errors.append("RENDER_RESULT_NOT_DIAGNOSTIC_ONLY")
    if normalized.get("result") != "pass":
        errors.append("TINY_RENDER_RESULT_NOT_PASS")
    if normalized.get("output_video_observed") is not True:
        errors.append("OUTPUT_VIDEO_NOT_OBSERVED")
    if normalized.get("four_dialogue_lines_visible") is not True:
        errors.append("FOUR_DIALOGUE_LINES_NOT_VISIBLE")
    if normalized.get("neutral_68_sec_timing_patch_applied") is not False:
        errors.append("TIMING_PATCH_ALREADY_APPLIED")
    if parse_status.get("parse_status") != "parsed":
        errors.append("YMMP_STRUCTURE_NOT_PARSED")
    if dialogue.get("canonical_speaker_value") != CANONICAL_UI_OBSERVED_SPEAKER:
        errors.append("CANONICAL_SPEAKER_MISMATCH")
    if not fields:
        errors.append("VOICE_AUDIO_FIELDS_MISSING")
    if audio.get("voice_cache_item_count") != 4:
        errors.append("VOICE_CACHE_ITEM_COUNT_NOT_4")
    if "AquesTalk" not in audio.get("character_voice_apis", []):
        errors.append("AQUESTALK_ENGINE_HINT_MISSING")
    if boundary_knowns.get("audio_presence_in_render") != "unknown":
        errors.append("AUDIO_PRESENCE_STATE_NOT_UNKNOWN")
    if boundary_knowns.get("audio_quality_accepted") is not False:
        errors.append("AUDIO_QUALITY_ALREADY_ACCEPTED")
    if boundary_knowns.get("TTS_ready") is not False:
        errors.append("TTS_READY_NOT_FALSE")

    return {
        "status": "passed" if not errors else "blocked",
        "audio_boundary_id": audio_boundary.get("boundary_id"),
        "tiny_render_result_id": render_result.get("result_id"),
        "ymmp_structure_readback_id": structure_readback.get("readback_id"),
        "canonical_speaker_value": dialogue.get("canonical_speaker_value"),
        "canonical_speaker_unicode_escape": dialogue.get(
            "canonical_speaker_unicode_escape"
        ),
        "voice_audio_related_fields_present": fields,
        "voice_cache_item_count": audio.get("voice_cache_item_count"),
        "native_voice_engine_hint": _native_voice_engine_hint(audio),
        "errors": errors,
    }


def _known_render_state(render_result: dict[str, Any]) -> dict[str, Any]:
    normalized = _dict(render_result.get("normalized_result"))
    return {
        "tiny_render_smoke_result": normalized.get("result"),
        "output_video_observed": normalized.get("output_video_observed"),
        "approximate_duration_sec": normalized.get("output_duration_observed_sec"),
        "four_dialogue_lines_visible": normalized.get("four_dialogue_lines_visible"),
        "timing_mode": "YMM4 natural duration",
        "neutral_68_sec_timing_patch_applied": normalized.get(
            "neutral_68_sec_timing_patch_applied"
        ),
    }


def _native_audio_evidence(structure_readback: dict[str, Any]) -> dict[str, Any]:
    audio = _dict(structure_readback.get("audio_tts_structure"))
    fields = audio.get("voice_audio_related_fields_present", [])
    dialogue = _dict(structure_readback.get("dialogue_structure"))
    voice_fields_present = bool(fields) and audio.get("voice_item_count") == 4
    voice_cache_present = audio.get("voice_cache_item_count") == 4
    voice_length_present = "VoiceLength" in fields
    pronounce_or_hatsuon_present = "Pronounce" in fields or "Hatsuon" in fields
    native_audio_path_candidate = all(
        [
            voice_fields_present,
            voice_cache_present,
            voice_length_present,
            pronounce_or_hatsuon_present,
            "AquesTalk" in audio.get("character_voice_apis", []),
        ]
    )

    return {
        "voice_fields_present": voice_fields_present,
        "voice_cache_present": voice_cache_present,
        "voice_length_fields_present": voice_length_present,
        "pronounce_or_hatsuon_fields_present": pronounce_or_hatsuon_present,
        "native_voice_engine_hint": _native_voice_engine_hint(audio),
        "voice_item_count": audio.get("voice_item_count"),
        "voice_cache_item_count": audio.get("voice_cache_item_count"),
        "voice_audio_related_fields_present": fields,
        "speaker_binding_status": (
            f"{CANONICAL_UI_OBSERVED_SPEAKER} accepted for diagnostic import"
        ),
        "speaker_unicode_escape": dialogue.get(
            "canonical_speaker_unicode_escape",
            CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
        ),
        "native_audio_path_candidate": native_audio_path_candidate,
    }


def _audio_tts_knowns_and_unknowns(
    audio_boundary: dict[str, Any],
    native_evidence: dict[str, Any],
) -> dict[str, Any]:
    boundary_knowns = _dict(audio_boundary.get("audio_tts_knowns_and_unknowns"))
    return {
        "audio_presence_in_render": boundary_knowns.get(
            "audio_presence_in_render",
            "unknown",
        ),
        "audio_quality_accepted": False,
        "TTS_ready": False,
        "TTS_generated_by_agent": False,
        "explicit_operator_TTS_generation": False,
        "external_TTS_introduced": False,
        "native_audio_path_candidate": native_evidence.get(
            "native_audio_path_candidate"
        ),
        "confidence": "medium",
        "confidence_reason": [
            "YMM4 voice fields and VoiceCache are present for all four diagnostic VoiceItem rows.",
            "The diagnostic tiny render smoke passed, so the project can render at tool-chain smoke scope.",
            "Audible presence and voice quality remain unknown because no audio observation was accepted.",
        ],
        "known_unknown_note": (
            "This proof supports the native path as a diagnostic default, not "
            "audio presence, TTS readiness, or audio quality acceptance."
        ),
    }


def _responsibility_split() -> list[dict[str, Any]]:
    return [
        {
            "path_id": "YMM4_native_voice_audio_path",
            "role": "recommended_diagnostic_default",
            "benefits": [
                "uses the voice fields and VoiceCache already saved in .ymmp",
                "keeps speaker binding, timing fields, and audio responsibility in one YMM4-native surface",
            ],
            "risks": [
                "audio presence in the rendered mp4 is still unknown",
                "VoiceCache can be overread as audio quality acceptance",
            ],
            "what_it_enables": [
                NEXT_RECOMMENDED_SLICE,
                "optional compact audio observation only if audio becomes the bottleneck",
            ],
            "what_it_defers": [
                "external TTS integration",
                "audio quality acceptance",
                "production voice readiness",
            ],
        },
        {
            "path_id": "external_TTS_path",
            "role": "closed_for_now",
            "benefits": [
                "could provide explicit audio generation control later",
                "could support future non-YMM4 voice replacement experiments",
            ],
            "risks": [
                "adds credential, retention, and timing boundaries too early",
                "can obscure whether YMM4 native audio already works",
            ],
            "what_it_enables": [
                "future external narration experiments after native path evidence is exhausted",
            ],
            "what_it_defers": [
                "current diagnostic follow-through",
                NEXT_RECOMMENDED_SLICE,
            ],
        },
        {
            "path_id": "metadata_only_voice_profile_path",
            "role": "planning_only",
            "benefits": [
                "records intended voice identity without generating audio",
                "keeps future normalization schemas stable",
            ],
            "risks": [
                "does not prove audible output",
                "can be mistaken for TTS readiness",
            ],
            "what_it_enables": [
                "future voice-profile bookkeeping",
            ],
            "what_it_defers": [
                "audio presence proof",
                "TTS quality acceptance",
            ],
        },
        {
            "path_id": "no_audio_diagnostic_path",
            "role": "fallback_only",
            "benefits": [
                "keeps visual/render diagnostics isolated if audio is irrelevant",
                "avoids new audio generation or media retention",
            ],
            "risks": [
                "does not represent a public video",
                "cannot validate speaker timing or audio quality",
            ],
            "what_it_enables": [
                "silent tool-chain diagnostics if explicitly chosen",
            ],
            "what_it_defers": [
                "voice readiness",
                "production render readiness",
            ],
        },
    ]


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "ymmp_created_or_modified_by_agent": False,
        "ymmp_or_media_staged_or_committed": False,
        "production_approval": False,
        "public_video_ready": False,
        "render_output_retention_required_now": False,
        "dashboard_governance_freshness_changed": False,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_render_readiness": False,
        "public_video_readiness": False,
        "neutral_68_sec_timing_proof": False,
        "timing_patch_readiness": False,
        "visual_layout_readiness": False,
        "TTS_audio_quality_acceptance": False,
        "TTS_readiness": False,
        "real_content_readiness": False,
        "external_TTS_adoption": False,
        "production_approval": False,
    }


def _native_voice_engine_hint(audio: dict[str, Any]) -> str:
    apis = audio.get("character_voice_apis", [])
    if "AquesTalk" in apis:
        return "AquesTalk"
    if apis:
        return "other"
    return "unknown"


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
