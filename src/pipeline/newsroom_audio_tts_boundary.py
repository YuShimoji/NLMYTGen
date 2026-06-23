"""Audio/TTS boundary for the diagnostic newsroom YMM4 lane.

This module defines responsibility boundaries after a diagnostic tiny render
smoke has passed. It does not launch YMM4, render, generate TTS/audio, patch
or commit .ymmp, import real media, fetch external sources, or approve
production use.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
    DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_yym4_timing_gap_strategy import (
    DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH,
)


AUDIO_TTS_BOUNDARY_SCHEMA_VERSION = "newsroom_audio_tts_boundary.v1"
AUDIO_TTS_BOUNDARY_ID = "newsroom_audio_tts_boundary_v1_2026_06_23"
DEFAULT_AUDIO_TTS_BOUNDARY_PATH = Path(
    "samples/_probe/newsroom_handoff/audio_tts_boundary_v1.json"
)
DEFAULT_AUDIO_TTS_BOUNDARY_DOC_PATH = Path(
    "docs/verification/NEWSROOM_AUDIO_TTS_BOUNDARY_V1_2026-06-23.md"
)
DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/tiny_render_smoke_result_readback_v1.json"
)

RECOMMENDED_DEFAULT = "keep_yym4_native_voice_audio_path_for_next_diagnostic"
TINY_AUDIO_OBSERVATION_SLICE = "newsroom-tiny-render-audio-observation-card-v1"
YYM4_NATIVE_AUDIO_PATH_PROOF_SLICE = "newsroom-yym4-native-audio-path-proof-v1"
TIMING_PATCH_STRATEGY_SLICE = "newsroom-ymmp-timing-patch-strategy-v1"


def build_default_newsroom_audio_tts_boundary(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed audio/TTS boundary from source readbacks."""
    base = Path(root) if root is not None else Path(".")
    render_result = load_json_object(
        base / DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    structure_readback = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
    )
    timing_strategy = load_json_object(base / DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH)
    return build_newsroom_audio_tts_boundary(
        render_result,
        structure_readback,
        timing_strategy,
        source_render_smoke_result_path=(
            DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        source_ymmp_structure_readback_path=(
            DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
        ),
        source_timing_strategy_path=DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH,
    )


def build_newsroom_audio_tts_boundary(
    render_result: dict[str, Any],
    structure_readback: dict[str, Any],
    timing_strategy: dict[str, Any],
    *,
    source_render_smoke_result_path: str | Path,
    source_ymmp_structure_readback_path: str | Path,
    source_timing_strategy_path: str | Path,
) -> dict[str, Any]:
    """Build a diagnostic-only audio/TTS responsibility boundary."""
    source_validation = _source_validation(
        render_result,
        structure_readback,
        timing_strategy,
    )
    known_render_result = _known_render_result(render_result)
    audio_knowns = _audio_tts_knowns_and_unknowns(structure_readback)
    responsibilities = _responsibility_split()
    timing_interaction = _timing_interaction(render_result, timing_strategy)
    not_accepted_scope = _not_accepted_scope()
    operator_card = _operator_observation_card()
    boundary_status = (
        "accepted_for_next_audio_observation"
        if not source_validation["errors"]
        else "blocked"
    )

    return {
        "artifact_id": AUDIO_TTS_BOUNDARY_ID,
        "boundary_id": AUDIO_TTS_BOUNDARY_ID,
        "schema_version": AUDIO_TTS_BOUNDARY_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "boundary_status": boundary_status,
        "identity": {
            "boundary_id": AUDIO_TTS_BOUNDARY_ID,
            "source_render_smoke_result_path": _path_text(
                source_render_smoke_result_path
            ),
            "source_render_smoke_result_id": render_result.get("result_id"),
            "source_ymmp_structure_readback_path": _path_text(
                source_ymmp_structure_readback_path
            ),
            "source_ymmp_structure_readback_id": structure_readback.get(
                "readback_id"
            ),
            "source_timing_strategy_path": _path_text(source_timing_strategy_path),
            "source_timing_strategy_id": timing_strategy.get("strategy_id"),
            "production_status": "diagnostic_only",
            "boundary_status": boundary_status,
        },
        "source_validation": source_validation,
        "known_render_result": known_render_result,
        "audio_tts_knowns_and_unknowns": audio_knowns,
        "responsibility_split": responsibilities,
        "recommended_default": {
            "choice": RECOMMENDED_DEFAULT,
            "reasoning": [
                "The current .ymmp already records YMM4 voice fields and VoiceCache.",
                "The tiny render smoke proves diagnostic render viability, not audio quality.",
                "External TTS would add a second timing and integration variable too early.",
                "Audio/TTS choice should be understood before neutral 68 second timing patch work.",
            ],
            "do_now": [
                "keep YMM4 native voice/audio path as the next diagnostic path",
                "record audio presence in render as unknown until a small observation is needed",
                "keep external TTS closed",
            ],
            "defer": [
                "external TTS generation",
                "audio quality acceptance",
                "production voice readiness",
                "neutral 68 second timing patch",
            ],
        },
        "operator_observation_card_if_needed": operator_card,
        "timing_interaction": timing_interaction,
        "next_recommended_slices": {
            "if_audio_presence_is_sufficient_from_existing_evidence": (
                TIMING_PATCH_STRATEGY_SLICE
            ),
            "if_audio_presence_is_unknown_and_needed": (
                TINY_AUDIO_OBSERVATION_SLICE
            ),
            "if_audio_path_should_be_defined_first": (
                YYM4_NATIVE_AUDIO_PATH_PROOF_SLICE
            ),
            "do_not_recommend": "production_render_immediately",
        },
        "boundary_status_detail": _boundary_status_detail(),
        "review_memory": {
            "review_source": "tiny_render_smoke_result_readback",
            "checked": True,
            "prior_user_review_count": {
                "manual_import_behavior": 1,
                "bound_speaker_behavior": 1,
                "diagnostic_ymmp_manual_observation": 1,
                "ymmp_structure_readback": 1,
                "timing_gap_strategy": 1,
                "tiny_render_smoke_boundary": 1,
                "tiny_render_smoke_result": 1,
                "audio_tts_boundary": 0,
            },
            "prior_evidence_reused": [
                "tiny render smoke result readback",
                "diagnostic .ymmp structure readback",
                "YMM4 timing gap strategy",
            ],
            "next_nonredundant_axis": [
                TINY_AUDIO_OBSERVATION_SLICE,
                YYM4_NATIVE_AUDIO_PATH_PROOF_SLICE,
                TIMING_PATCH_STRATEGY_SLICE,
            ],
            "not_accepted_scope": not_accepted_scope,
            "repeated_general_review_allowed": False,
            "user_side_work_re_requested": False,
            "input_mode": "freeform",
        },
        "human_burden_hygiene": {
            "user_input": "freeform",
            "template_required": False,
            "schema_owner": "Agent",
            "user_side_work_this_slice": "none",
            "future_observation_max_required_points": len(operator_card["look_for"]),
            "screenshot_optional": True,
            "negative_confirmations_required_from_user": False,
            "fixed_form_result_template": False,
        },
        "not_accepted_scope": not_accepted_scope,
        "downstream_next_use": {
            "use_this_boundary_to": [
                "keep render success separate from audio quality acceptance",
                "choose a minimal YMM4 native audio observation if audio evidence becomes necessary",
                "avoid introducing external TTS before native YMM4 audio behavior is understood",
                "defer neutral timing patch until audio/TTS boundary is stable",
            ],
            "do_not_use_this_boundary_to": [
                "claim audio quality acceptance",
                "claim TTS readiness",
                "generate or import audio",
                "claim production render or public video readiness",
                "commit .ymmp, mp4, wav, mp3, or media output",
            ],
        },
    }


def render_newsroom_audio_tts_boundary_markdown(boundary: dict[str, Any]) -> str:
    """Render a human-readable audio/TTS boundary readback."""
    identity = _dict(boundary.get("identity"))
    validation = _dict(boundary.get("source_validation"))
    render_result = _dict(boundary.get("known_render_result"))
    knowns = _dict(boundary.get("audio_tts_knowns_and_unknowns"))
    recommended = _dict(boundary.get("recommended_default"))
    card = _dict(boundary.get("operator_observation_card_if_needed"))
    timing = _dict(boundary.get("timing_interaction"))
    next_slices = _dict(boundary.get("next_recommended_slices"))
    status = _dict(boundary.get("boundary_status_detail"))
    hygiene = _dict(boundary.get("human_burden_hygiene"))
    review = _dict(boundary.get("review_memory"))

    lines = [
        "# Newsroom Audio / TTS Boundary v1",
        "",
        f"artifact_id: {boundary.get('artifact_id')}",
        f"boundary_id: {boundary.get('boundary_id')}",
        f"schema_version: {boundary.get('schema_version')}",
        f"review_status: {boundary.get('review_status')}",
        f"production_status: {boundary.get('production_status')}",
        f"boundary_status: {boundary.get('boundary_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        (
            "- source_render_smoke_result_path: "
            f"{identity.get('source_render_smoke_result_path')}"
        ),
        (
            "- source_render_smoke_result_id: "
            f"{identity.get('source_render_smoke_result_id')}"
        ),
        (
            "- source_ymmp_structure_readback_path: "
            f"{identity.get('source_ymmp_structure_readback_path')}"
        ),
        (
            "- source_ymmp_structure_readback_id: "
            f"{identity.get('source_ymmp_structure_readback_id')}"
        ),
        f"- source_timing_strategy_path: {identity.get('source_timing_strategy_path')}",
        f"- source_timing_strategy_id: {identity.get('source_timing_strategy_id')}",
        "",
        "## Source Validation",
        "",
        f"- status: {validation.get('status')}",
        f"- errors: {_display(validation.get('errors'))}",
        f"- canonical_speaker_value: {validation.get('canonical_speaker_value')}",
        "",
        "## Known Render Result",
        "",
    ]
    for key, value in render_result.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Known / Unknown Audio State", ""])
    for key, value in knowns.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Responsibility Split",
            "",
            "| path | role | enables | defers | main risk |",
            "|---|---|---|---|---|",
        ]
    )
    for item in boundary.get("responsibility_split", []):
        lines.append(
            "| "
            f"{item.get('path_id')} | "
            f"{item.get('role')} | "
            f"{'; '.join(item.get('what_it_enables', []))} | "
            f"{'; '.join(item.get('what_it_defers', []))} | "
            f"{'; '.join(item.get('risks', []))} |"
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

    lines.extend(
        [
            "",
            "## Operator Observation Card If Needed",
            "",
            f"- status: {card.get('status')}",
            f"- target: {card.get('target')}",
            f"- why: {card.get('why')}",
            f"- action: {card.get('action')}",
            f"- answer_style: {card.get('answer_style')}",
            "- look_for:",
        ]
    )
    for item in card.get("look_for", []):
        lines.append(f"  - {item}")
    lines.append("- not_needed:")
    for item in card.get("not_needed", []):
        lines.append(f"  - {item}")

    lines.extend(["", "## Timing Interaction", ""])
    for key, value in timing.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Next Recommended Slices", ""])
    for key, value in next_slices.items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Boundary Status", ""])
    for key, value in status.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Human Burden Hygiene", ""])
    for key, value in hygiene.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Review Memory",
            "",
            (
                "- prior_user_review_count: "
                f"{_display(review.get('prior_user_review_count'))}"
            ),
            (
                "- next_nonredundant_axis: "
                f"{_display(review.get('next_nonredundant_axis'))}"
            ),
            (
                "- repeated_general_review_allowed: "
                f"{_display(review.get('repeated_general_review_allowed'))}"
            ),
            "",
            "## Boundary Note",
            "",
            "This boundary defines audio/TTS responsibility only. It does not "
            "launch YMM4, render, generate audio/TTS, import real media, patch "
            "or commit `.ymmp`, approve production, prepare public video, or "
            "change dashboard/governance/freshness work.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    render_result: dict[str, Any],
    structure_readback: dict[str, Any],
    timing_strategy: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    normalized = _dict(render_result.get("normalized_result"))
    audio = _dict(structure_readback.get("audio_tts_structure"))
    dialogue = _dict(structure_readback.get("dialogue_structure"))
    timing = _dict(timing_strategy.get("timing_facts"))

    if render_result.get("production_status") != "diagnostic_only":
        errors.append("RENDER_RESULT_NOT_DIAGNOSTIC_ONLY")
    if normalized.get("result") != "pass":
        errors.append("RENDER_RESULT_NOT_PASS")
    if normalized.get("render_completed") is not True:
        errors.append("RENDER_NOT_COMPLETED")
    if normalized.get("TTS_quality_acceptance") is not False:
        errors.append("TTS_QUALITY_ALREADY_ACCEPTED")
    if dialogue.get("canonical_speaker_value") != CANONICAL_UI_OBSERVED_SPEAKER:
        errors.append("CANONICAL_SPEAKER_MISMATCH")
    if audio.get("voice_cache_item_count") != 4:
        errors.append("VOICE_CACHE_ITEM_COUNT_NOT_4")
    if audio.get("TTS_generated_by_agent") is not False:
        errors.append("TTS_GENERATED_BY_AGENT_NOT_FALSE")
    if audio.get("explicit_operator_TTS_generation") is not False:
        errors.append("EXPLICIT_OPERATOR_TTS_GENERATION_NOT_FALSE")
    if timing.get("timing_patch_applied") is not False:
        errors.append("TIMING_PATCH_ALREADY_APPLIED")

    return {
        "status": "passed" if not errors else "blocked",
        "render_result_id": render_result.get("result_id"),
        "structure_readback_id": structure_readback.get("readback_id"),
        "timing_strategy_id": timing_strategy.get("strategy_id"),
        "canonical_speaker_value": dialogue.get("canonical_speaker_value"),
        "canonical_speaker_unicode_escape": dialogue.get(
            "canonical_speaker_unicode_escape"
        ),
        "voice_cache_item_count": audio.get("voice_cache_item_count"),
        "voice_audio_related_fields_present": audio.get(
            "voice_audio_related_fields_present", []
        ),
        "errors": errors,
    }


def _known_render_result(render_result: dict[str, Any]) -> dict[str, Any]:
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
        "render_output_path_if_known": normalized.get("output_path"),
        "render_output_committed": normalized.get("render_output_committed"),
        "render_output_staged": normalized.get("render_output_staged"),
    }


def _audio_tts_knowns_and_unknowns(
    structure_readback: dict[str, Any],
) -> dict[str, Any]:
    audio = _dict(structure_readback.get("audio_tts_structure"))
    fields = audio.get("voice_audio_related_fields_present", [])
    voice_fields_present = bool(fields) and audio.get("voice_cache_item_count") == 4
    return {
        "VoiceCache_or_voice_fields_present_in_ymmp": voice_fields_present,
        "voice_audio_related_fields_present": fields,
        "voice_item_count": audio.get("voice_item_count"),
        "voice_cache_item_count": audio.get("voice_cache_item_count"),
        "character_voice_apis": audio.get("character_voice_apis", []),
        "TTS_generated_by_agent": False,
        "explicit_operator_TTS_generation": False,
        "audio_presence_in_render": "unknown",
        "audio_quality_accepted": False,
        "TTS_ready": False,
        "voice_binding_ready": "partial",
        "speaker_binding_status": (
            f"{CANONICAL_UI_OBSERVED_SPEAKER} accepted for diagnostic import"
        ),
        "speaker_unicode_escape": CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
        "known_unknown_note": (
            "Render success and VoiceCache presence do not establish audio "
            "presence or audio quality in the output."
        ),
    }


def _responsibility_split() -> list[dict[str, Any]]:
    return [
        {
            "path_id": "yym4_native_voice_audio_path",
            "role": "recommended_next_diagnostic_path",
            "benefits": [
                "uses the saved .ymmp voice fields and VoiceCache",
                "keeps speaker binding and timing in one YMM4-native surface",
            ],
            "risks": [
                "audio presence in the current render is not yet observed",
                "VoiceCache presence can be overread as audio quality",
            ],
            "what_it_enables": [
                "small audio presence observation",
                "native voice path proof",
            ],
            "what_it_defers": [
                "external TTS integration",
                "production voice readiness",
            ],
        },
        {
            "path_id": "external_tts_path",
            "role": "closed_for_now",
            "benefits": [
                "could provide explicit audio generation control later",
                "could decouple voice from YMM4 internals later",
            ],
            "risks": [
                "adds timing drift before the native path is understood",
                "adds credential/tooling and file-retention questions",
            ],
            "what_it_enables": [
                "future external narration experiments",
                "future voice replacement design",
            ],
            "what_it_defers": [
                "current diagnostic render follow-through",
                "neutral timing patch strategy",
            ],
        },
        {
            "path_id": "metadata_only_voice_profile_path",
            "role": "planning_only",
            "benefits": [
                "records intended speaker/profile without generating audio",
                "keeps schemas stable for future normalization",
            ],
            "risks": [
                "does not prove audible output",
                "can be mistaken for voice readiness",
            ],
            "what_it_enables": [
                "voice profile bookkeeping",
                "future path comparison",
            ],
            "what_it_defers": [
                "audio presence proof",
                "TTS quality acceptance",
            ],
        },
        {
            "path_id": "no_audio_diagnostic_render_path",
            "role": "fallback_if_audio_remains_unneeded",
            "benefits": [
                "keeps render/timing diagnostics isolated from audio",
                "allows visual/tool-chain checks without narration claims",
            ],
            "risks": [
                "not representative of a public video",
                "cannot validate voice timing or speaker quality",
            ],
            "what_it_enables": [
                "continued non-audio diagnostic render checks",
                "retention-policy decisions for silent outputs",
            ],
            "what_it_defers": [
                "voice readiness",
                "production render readiness",
            ],
        },
    ]


def _operator_observation_card() -> dict[str, Any]:
    return {
        "status": "proposed_if_needed",
        "target": "tiny render audio presence observation",
        "why": (
            "Audio presence in the render is unknown; use only if audio becomes "
            "the next bottleneck."
        ),
        "action": (
            "Play the existing diagnostic tiny render and answer in freeform."
        ),
        "look_for": [
            "whether any audio is present",
            "whether the voice sounds like the expected YMM4 speaker",
            "whether there is obvious silence, cutoff, or mismatch",
        ],
        "answer_style": "freeform",
        "not_needed": [
            "fixed form",
            "production quality review",
            "timing patch",
            "new render",
            "external TTS",
        ],
    }


def _timing_interaction(
    render_result: dict[str, Any],
    timing_strategy: dict[str, Any],
) -> dict[str, Any]:
    normalized = _dict(render_result.get("normalized_result"))
    timing = _dict(timing_strategy.get("timing_facts"))
    return {
        "first_render_smoke_used_natural_duration": True,
        "first_smoke_duration_sec": normalized.get("output_duration_observed_sec"),
        "first_smoke_duration_qualifier": normalized.get(
            "output_duration_observed_qualifier"
        ),
        "prior_ymmp_natural_duration_sec": timing.get("ymmp_total_duration_sec"),
        "neutral_68_sec_timing_patch_remains_deferred": True,
        "audio_tts_choice_may_affect_timing_duration": True,
        "do_not_patch_timing_before_audio_tts_boundary_understood": True,
        "timing_patch_applied": False,
    }


def _boundary_status_detail() -> dict[str, bool]:
    return {
        "render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "real_media_imported": False,
        "production_approval": False,
        "public_video_ready": False,
        "output_retention_required_now": False,
        "dashboard_governance_freshness_changed": False,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_render_readiness": False,
        "public_video_readiness": False,
        "neutral_68_sec_timing_proof": False,
        "visual_layout_readiness": False,
        "TTS_audio_quality_acceptance": False,
        "TTS_readiness": False,
        "real_content_readiness": False,
        "production_approval": False,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
