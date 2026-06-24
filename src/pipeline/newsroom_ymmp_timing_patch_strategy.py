"""YMM4 timing patch strategy for the diagnostic newsroom lane.

This module records how the diagnostic 8 second YMM4 natural timeline should
move toward the neutral 68 second timeline in the next probe. It does not patch
.ymmp, launch YMM4, render, generate TTS/audio, import real media, fetch
external sources, or approve production use.
"""

from __future__ import annotations

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
from src.pipeline.newsroom_yym4_native_audio_path_proof import (
    DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH,
)
from src.pipeline.newsroom_yym4_timing_gap_strategy import (
    DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH,
)
from src.pipeline.newsroom_audio_tts_boundary import (
    DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH,
)


YMMP_TIMING_PATCH_STRATEGY_SCHEMA_VERSION = (
    "newsroom_ymmp_timing_patch_strategy.v1"
)
YMMP_TIMING_PATCH_STRATEGY_ID = (
    "newsroom_ymmp_timing_patch_strategy_v1_2026_06_24"
)
DEFAULT_YMMP_TIMING_PATCH_STRATEGY_PATH = Path(
    "samples/_probe/newsroom_handoff/ymmp_timing_patch_strategy_v1.json"
)
DEFAULT_YMMP_TIMING_PATCH_STRATEGY_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YMMP_TIMING_PATCH_STRATEGY_V1_2026-06-24.md"
)

RECOMMENDED_DEFAULT = "neutral_timeline_skeleton_patch_with_native_voice_preserved"
NEXT_PATCH_PROBE_SLICE = "newsroom-ymmp-timing-patch-probe-v1"
POST_PATCH_RENDER_SMOKE = "milestone-gated-post-patch-render-smoke"
VISUAL_LAYOUT_BRIDGE_SLICE = "newsroom-visual-layout-bridge-v1"
OPTIONAL_RETENTION_SLICE = "newsroom-render-output-retention-policy-v1"


def build_default_newsroom_ymmp_timing_patch_strategy(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed strategy from source readbacks."""
    base = Path(root) if root is not None else Path(".")
    audio_observation = load_json_object(
        base / DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
    )
    native_audio_path_proof = load_json_object(
        base / DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH
    )
    tiny_render_result = load_json_object(
        base / DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    structure_readback = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
    )
    neutral_timeline = load_json_object(base / DEFAULT_NEUTRAL_TIMELINE_PATH)
    prior_timing_gap_strategy = load_json_object(
        base / DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH
    )
    return build_newsroom_ymmp_timing_patch_strategy(
        audio_observation,
        native_audio_path_proof,
        tiny_render_result,
        structure_readback,
        neutral_timeline,
        prior_timing_gap_strategy,
        source_audio_observation_readback_path=(
            DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
        ),
        source_native_audio_path_proof_path=DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH,
        source_tiny_render_result_path=(
            DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        source_ymmp_structure_readback_path=(
            DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
        ),
        source_neutral_timeline_path=DEFAULT_NEUTRAL_TIMELINE_PATH,
        source_prior_timing_gap_strategy_path=DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH,
    )


def build_newsroom_ymmp_timing_patch_strategy(
    audio_observation: dict[str, Any],
    native_audio_path_proof: dict[str, Any],
    tiny_render_result: dict[str, Any],
    structure_readback: dict[str, Any],
    neutral_timeline: dict[str, Any],
    prior_timing_gap_strategy: dict[str, Any],
    *,
    source_audio_observation_readback_path: str | Path,
    source_native_audio_path_proof_path: str | Path,
    source_tiny_render_result_path: str | Path,
    source_ymmp_structure_readback_path: str | Path,
    source_neutral_timeline_path: str | Path,
    source_prior_timing_gap_strategy_path: str | Path,
) -> dict[str, Any]:
    """Build a diagnostic-only timing patch strategy."""
    source_validation = _source_validation(
        audio_observation,
        native_audio_path_proof,
        tiny_render_result,
        structure_readback,
        neutral_timeline,
        prior_timing_gap_strategy,
    )
    status = "recommended_for_probe" if not source_validation["errors"] else "blocked"
    timing_state = _known_current_timing_state(
        audio_observation,
        tiny_render_result,
        structure_readback,
        neutral_timeline,
        prior_timing_gap_strategy,
    )
    not_accepted_scope = _not_accepted_scope()

    return {
        "artifact_id": YMMP_TIMING_PATCH_STRATEGY_ID,
        "strategy_id": YMMP_TIMING_PATCH_STRATEGY_ID,
        "schema_version": YMMP_TIMING_PATCH_STRATEGY_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "strategy_status": status,
        "identity": {
            "strategy_id": YMMP_TIMING_PATCH_STRATEGY_ID,
            "source_audio_observation_readback_path": _path_text(
                source_audio_observation_readback_path
            ),
            "source_audio_observation_readback_id": audio_observation.get(
                "readback_id"
            ),
            "source_native_audio_path_proof_path": _path_text(
                source_native_audio_path_proof_path
            ),
            "source_native_audio_path_proof_id": native_audio_path_proof.get(
                "proof_id"
            ),
            "source_tiny_render_result_path": _path_text(
                source_tiny_render_result_path
            ),
            "source_tiny_render_result_id": tiny_render_result.get("result_id"),
            "source_ymmp_structure_readback_path": _path_text(
                source_ymmp_structure_readback_path
            ),
            "source_ymmp_structure_readback_id": structure_readback.get(
                "readback_id"
            ),
            "source_neutral_timeline_path": _path_text(source_neutral_timeline_path),
            "source_neutral_timeline_id": neutral_timeline.get("timeline_id"),
            "source_prior_timing_gap_strategy_path": _path_text(
                source_prior_timing_gap_strategy_path
            ),
            "source_prior_timing_gap_strategy_id": prior_timing_gap_strategy.get(
                "strategy_id"
            ),
            "production_status": "diagnostic_only",
            "strategy_status": status,
        },
        "source_validation": source_validation,
        "known_current_timing_state": timing_state,
        "strategy_candidates": _strategy_candidates(),
        "recommended_default": _recommended_default(),
        "patch_probe_boundary": _patch_probe_boundary(),
        "render_gate_carry_forward": _render_gate_carry_forward(),
        "readiness_separation": _readiness_separation(),
        "not_accepted_scope": not_accepted_scope,
        "next_recommended_slices": [
            NEXT_PATCH_PROBE_SLICE,
            POST_PATCH_RENDER_SMOKE,
            VISUAL_LAYOUT_BRIDGE_SLICE,
            OPTIONAL_RETENTION_SLICE,
        ],
        "next_recommended_slice_notes": {
            NEXT_PATCH_PROBE_SLICE: (
                "Create a JSON patch plan first, then use an ignored local "
                ".ymmp copy only if the plan passes preservation checks."
            ),
            POST_PATCH_RENDER_SMOKE: (
                "Render only after the timing patch probe changes the timeline "
                "surface and structural readback passes."
            ),
            VISUAL_LAYOUT_BRIDGE_SLICE: (
                "Open later, after timing mechanics and post-patch smoke give a "
                "stable surface for visual layout review."
            ),
            OPTIONAL_RETENTION_SLICE: (
                "Use only if a later render output must be retained as an artifact."
            ),
        },
        "goal_stack": _goal_stack(),
        "completion_matrix": _completion_matrix(),
        "artifact_readiness": _artifact_readiness(),
        "video_readiness": _video_readiness(),
        "production_readiness": _production_readiness(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(),
        "boundaries": _boundaries(),
        "downstream_next_use": {
            "use_this_strategy_to": [
                "start the timing patch probe with field-level guardrails",
                "move from natural 8 second timing toward a 68 second structural proof",
                "preserve native YMM4 voice fields while testing timing mechanics",
                "keep render/audio/user review out of this strategy slice",
            ],
            "do_not_use_this_strategy_to": [
                "claim the 68 second timing proof is already complete",
                "commit .ymmp or media output",
                "stretch or regenerate voice audio",
                "claim production narration, visual layout, or public readiness",
            ],
        },
    }


def render_newsroom_ymmp_timing_patch_strategy_markdown(
    strategy: dict[str, Any],
) -> str:
    """Render a human-readable timing patch strategy readback."""
    lines = [
        "# Newsroom YMM4 Timing Patch Strategy v1",
        "",
        f"artifact_id: {strategy.get('artifact_id')}",
        f"strategy_id: {strategy.get('strategy_id')}",
        f"schema_version: {strategy.get('schema_version')}",
        f"review_status: {strategy.get('review_status')}",
        f"production_status: {strategy.get('production_status')}",
        f"strategy_status: {strategy.get('strategy_status')}",
        "diagnostic_only: true",
        "",
    ]
    _append_mapping(lines, "Source", strategy.get("identity"))
    _append_mapping(lines, "Source Validation", strategy.get("source_validation"))
    _append_mapping(
        lines,
        "Known Current Timing State",
        strategy.get("known_current_timing_state"),
    )

    lines.extend(
        [
            "",
            "## Strategy Candidate Comparison",
            "",
            "| candidate | suitability | benefits | risks | proves / enables | cannot prove / defers |",
            "|---|---|---|---|---|---|",
        ]
    )
    for candidate in strategy.get("strategy_candidates", []):
        proves = candidate.get("what_it_proves") or candidate.get("what_it_enables")
        cannot = candidate.get("what_it_cannot_prove") or candidate.get(
            "what_it_defers"
        )
        lines.append(
            "| "
            f"{candidate.get('candidate_id')} | "
            f"{candidate.get('suitability')} | "
            f"{'; '.join(candidate.get('benefits', []))} | "
            f"{'; '.join(candidate.get('risks', []))} | "
            f"{'; '.join(proves or [])} | "
            f"{'; '.join(cannot or [])} |"
        )

    _append_mapping(lines, "Recommended Default", strategy.get("recommended_default"))
    _append_mapping(lines, "Patch Probe Boundary", strategy.get("patch_probe_boundary"))
    _append_mapping(
        lines,
        "Render Gate Carry-Forward",
        strategy.get("render_gate_carry_forward"),
    )
    _append_mapping(
        lines,
        "Readiness Separation",
        strategy.get("readiness_separation"),
    )
    _append_mapping(lines, "Not Accepted Scope", strategy.get("not_accepted_scope"))

    lines.extend(
        [
            "",
            "## Next Recommended Slices",
            "",
            "| slice | purpose |",
            "|---|---|",
        ]
    )
    notes = _dict(strategy.get("next_recommended_slice_notes"))
    for item in strategy.get("next_recommended_slices", []):
        lines.append(f"| {item} | {notes.get(item)} |")

    _append_status_table(lines, "Goal Stack", strategy.get("goal_stack"), "level")
    _append_status_table(lines, "Completion Matrix", strategy.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", strategy.get("artifact_readiness"))
    _append_status_table(lines, "Video Readiness", strategy.get("video_readiness"))
    _append_status_table(
        lines,
        "Production Readiness",
        strategy.get("production_readiness"),
    )
    _append_status_table(
        lines,
        "Render Gate Hygiene",
        strategy.get("render_gate_hygiene"),
    )
    _append_status_table(
        lines,
        "Human Burden Hygiene",
        strategy.get("human_burden_hygiene"),
    )
    _append_status_table(
        lines,
        "Review Non-Redundancy",
        strategy.get("review_non_redundancy"),
    )
    _append_status_table(lines, "Inertia Check", strategy.get("inertia_check"))
    _append_mapping(lines, "Boundaries", strategy.get("boundaries"))

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This strategy chooses the next probe path only. It does not patch "
            "or commit `.ymmp`, launch YMM4, render, generate TTS/audio, import "
            "real media, accept production quality, or ask for another audio/render "
            "observation.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    audio_observation: dict[str, Any],
    native_audio_path_proof: dict[str, Any],
    tiny_render_result: dict[str, Any],
    structure_readback: dict[str, Any],
    neutral_timeline: dict[str, Any],
    prior_timing_gap_strategy: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    observation = _dict(audio_observation.get("normalized_audio_observation"))
    timing_readiness = _dict(audio_observation.get("timing_readiness"))
    native_validation = _dict(native_audio_path_proof.get("source_validation"))
    render_normalized = _dict(tiny_render_result.get("normalized_result"))
    structure_dialogue = _dict(structure_readback.get("dialogue_structure"))
    structure_timing = _dict(structure_readback.get("timing_structure"))
    neutral_global = _dict(neutral_timeline.get("global_timing"))
    prior_facts = _dict(prior_timing_gap_strategy.get("timing_facts"))

    if audio_observation.get("readiness_status") != "accepted_for_timing_patch_strategy":
        errors.append("AUDIO_OBSERVATION_NOT_READY_FOR_TIMING_STRATEGY")
    if observation.get("audio_presence_in_render") is not True:
        errors.append("AUDIO_PRESENCE_NOT_ACCEPTED_FOR_DIAGNOSTIC")
    if observation.get("external_TTS_introduced") is not False:
        errors.append("EXTERNAL_TTS_INTRODUCED")
    if native_audio_path_proof.get("proof_status") != "passed_with_unknowns":
        errors.append("NATIVE_AUDIO_PROOF_NOT_AVAILABLE")
    if native_validation.get("canonical_speaker_value") != CANONICAL_UI_OBSERVED_SPEAKER:
        errors.append("NATIVE_AUDIO_SPEAKER_MISMATCH")
    if render_normalized.get("result") != "pass":
        errors.append("TINY_RENDER_RESULT_NOT_PASS")
    if render_normalized.get("output_duration_observed_sec") != 8:
        errors.append("TINY_RENDER_DURATION_NOT_APPROX_8")
    if structure_dialogue.get("canonical_speaker_value") != CANONICAL_UI_OBSERVED_SPEAKER:
        errors.append("STRUCTURE_SPEAKER_MISMATCH")
    if structure_timing.get("observed_project_duration_frames") != 509:
        errors.append("NATURAL_DURATION_FRAMES_NOT_509")
    if structure_timing.get("fps") != 60:
        errors.append("YMMP_TIMEBASE_FPS_NOT_60")
    if neutral_global.get("total_duration_sec") != 68:
        errors.append("NEUTRAL_TIMELINE_TOTAL_NOT_68")
    if timing_readiness.get("timing_gap_status") != "unresolved":
        errors.append("TIMING_READINESS_GAP_NOT_UNRESOLVED")
    if prior_facts.get("source_timing_gap_status") != "unresolved":
        errors.append("PRIOR_TIMING_GAP_NOT_UNRESOLVED")

    return {
        "status": "passed" if not errors else "blocked",
        "audio_observation_readback_id": audio_observation.get("readback_id"),
        "native_audio_path_proof_id": native_audio_path_proof.get("proof_id"),
        "tiny_render_result_id": tiny_render_result.get("result_id"),
        "ymmp_structure_readback_id": structure_readback.get("readback_id"),
        "neutral_timeline_id": neutral_timeline.get("timeline_id"),
        "prior_timing_gap_strategy_id": prior_timing_gap_strategy.get("strategy_id"),
        "canonical_speaker": structure_dialogue.get("canonical_speaker_value"),
        "canonical_speaker_unicode_escape": structure_dialogue.get(
            "canonical_speaker_unicode_escape",
            CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
        ),
        "tiny_render_duration_sec": render_normalized.get(
            "output_duration_observed_sec"
        ),
        "natural_duration_frames": structure_timing.get(
            "observed_project_duration_frames"
        ),
        "neutral_timeline_total_sec": neutral_global.get("total_duration_sec"),
        "timing_gap_status": timing_readiness.get("timing_gap_status"),
        "errors": errors,
    }


def _known_current_timing_state(
    audio_observation: dict[str, Any],
    tiny_render_result: dict[str, Any],
    structure_readback: dict[str, Any],
    neutral_timeline: dict[str, Any],
    prior_timing_gap_strategy: dict[str, Any],
) -> dict[str, Any]:
    observation = _dict(audio_observation.get("normalized_audio_observation"))
    render_normalized = _dict(tiny_render_result.get("normalized_result"))
    structure_timing = _dict(structure_readback.get("timing_structure"))
    neutral_global = _dict(neutral_timeline.get("global_timing"))
    prior_facts = _dict(prior_timing_gap_strategy.get("timing_facts"))
    fps = _whole_number(structure_timing.get("fps"))
    neutral_sec = _whole_number(neutral_global.get("total_duration_sec"))
    natural_frames = _whole_number(structure_timing.get("observed_project_duration_frames"))
    return {
        "tiny_render_duration_sec": render_normalized.get(
            "output_duration_observed_sec"
        ),
        "tiny_render_duration_qualifier": render_normalized.get(
            "output_duration_observed_qualifier",
            "approx",
        ),
        "yym4_timebase_fps": fps,
        "natural_duration_frames": natural_frames,
        "natural_duration_sec": structure_timing.get("observed_project_duration_sec"),
        "neutral_timeline_total_sec": neutral_sec,
        "neutral_timeline_total_frames_at_60fps": (
            neutral_sec * 60 if isinstance(neutral_sec, int) else None
        ),
        "timing_gap_sec": prior_facts.get("timing_gap_sec"),
        "timing_gap_status": "unresolved",
        "audio_path_status": "diagnostic_pass",
        "voice_path": observation.get("voice_path"),
        "external_TTS_status": "closed",
        "canonical_speaker": observation.get("canonical_speaker"),
    }


def _strategy_candidates() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "A_keep_natural_8_sec_timing",
            "label": "Keep natural 8 sec timing",
            "benefits": [
                "preserves the tiny render project exactly as already observed",
                "avoids any timing mutation risk",
            ],
            "risks": [
                "does not move toward the neutral 68 second design",
                "can cause another readback-only stall after audio is already accepted",
            ],
            "what_it_proves": [
                "current diagnostic render/audio path remains intact",
            ],
            "what_it_cannot_prove": [
                "neutral 68 second timeline mechanics",
                "post-patch render surface",
            ],
            "suitability": "deferred_not_default_after_audio_pass",
        },
        {
            "candidate_id": "B_global_scale_current_item_frames_to_68_sec",
            "label": "Global scale current item frames to 68 sec",
            "benefits": [
                "simple mathematical bridge from 509 frames to 4080 frames",
                "can expose whether YMM4 accepts stretched item timing",
            ],
            "risks": [
                "may stretch sparse dialogue gaps in a way that looks accidental",
                "can imply voice/audio stretching even when voice should be preserved",
            ],
            "likely_artifacts": [
                "large silent gaps between short voice items",
                "rounding drift in frame positions and item lengths",
            ],
            "effect_on_voice_audio_assumptions": (
                "must preserve VoiceCache and voice fields; must not stretch, "
                "regenerate, or replace native voice audio"
            ),
            "what_it_enables": [
                "rough duration proof if only total length matters",
            ],
            "what_it_defers": [
                "neutral beat alignment",
                "creative density judgement",
            ],
            "suitability": "not_default_too_mechanical",
        },
        {
            "candidate_id": "C_align_dialogue_start_end_to_neutral_timeline",
            "label": (
                "Align dialogue start/end frames to neutral timeline while "
                "preserving native voice/audio fields"
            ),
            "benefits": [
                "connects the four dialogue rows to neutral 0-12-24-46-68 sec anchors",
                "tests timing mechanics without introducing external TTS",
            ],
            "risks": [
                "long sparse gaps are diagnostic-only and not production quality",
                "YMM4 voice item length semantics may need structural readback",
            ],
            "what_it_enables": [
                "68 second project/timeline structural proof",
                NEXT_PATCH_PROBE_SLICE,
            ],
            "what_it_defers": [
                "creative density improvement",
                "visual layout acceptance",
                "post-patch render observation",
            ],
            "suitability": "recommended_default",
        },
        {
            "candidate_id": "D_add_neutral_duration_tail_or_non_voice_carrier",
            "label": (
                "Add neutral-duration tail/holder or non-voice timing carrier "
                "while preserving current voice item timing"
            ),
            "benefits": [
                "preserves current native voice timing exactly",
                "can prove total timeline extension with minimal voice mutation",
            ],
            "risks": [
                "proves carrier duration more than dialogue alignment",
                "may hide whether neutral caption/dialogue anchors can be patched",
            ],
            "what_it_proves": [
                "a YMM4 project can be extended toward 68 seconds",
            ],
            "what_it_cannot_prove": [
                "dialogue alignment to the neutral timeline",
                "production pacing",
            ],
            "suitability": "fallback_if_voice_item_length_patch_is_unsafe",
        },
        {
            "candidate_id": "E_defer_68_sec_patch_until_script_density_increases",
            "label": "Defer 68 sec patch until script density increases",
            "benefits": [
                "avoids making a sparse diagnostic 68 second surface",
                "keeps creative density concerns visible",
            ],
            "risks": [
                "blocks the next mechanical timing proof",
                "keeps internal review video v0.1 from advancing",
            ],
            "effect_on_internal_review_timeline": (
                "slows internal review because timing mechanics remain unresolved"
            ),
            "what_it_enables": [
                "future richer script preparation",
            ],
            "what_it_defers": [
                NEXT_PATCH_PROBE_SLICE,
                "milestone-gated post-patch render smoke",
            ],
            "suitability": "not_default_creative_density_is_separate",
        },
    ]


def _recommended_default() -> dict[str, Any]:
    return {
        "choice": RECOMMENDED_DEFAULT,
        "why_this_default": [
            "audio is now diagnostic-acceptable, so timing can be handled separately",
            "the neutral timeline already defines 0-12-24-46-68 second anchors",
            "native YMM4 voice fields should be preserved rather than stretched or regenerated",
            "sparse long gaps are acceptable only as diagnostic timing mechanics",
        ],
        "meaning": [
            "move toward a 68 sec project/timeline proof",
            "preserve YMM4 native voice fields, VoiceCache, speaker, and text",
            "do not introduce external TTS",
            "do not stretch or regenerate voice audio",
            "treat long gaps or sparse content as diagnostic-only",
            "prove timing mechanics separately from creative density",
        ],
        "next_probe": NEXT_PATCH_PROBE_SLICE,
        "not_recommended": [
            "global voice/audio stretch",
            "production render immediately",
            "external TTS adoption",
            "creative/script density rewrite in this slice",
        ],
    }


def _patch_probe_boundary() -> dict[str, Any]:
    return {
        "next_slice": NEXT_PATCH_PROBE_SLICE,
        "may_create_ignored_local_patched_ymmp_copy": True,
        "ymmp_commit_allowed": False,
        "json_patch_plan_first": True,
        "probe_sequence": [
            "write a repo JSON/MD patch plan first",
            "if the plan passes, create or update an ignored local .ymmp copy only",
            "parse the patched copy and write structural readback JSON/MD",
            "keep render deferred until structural patch readback passes",
        ],
        "allowed_to_change": [
            "Frame",
            "Length",
            "timeline/project duration metadata if required",
            "non-voice timing carrier fields if a carrier fallback is selected",
            "diagnostic notes/metadata on the ignored copy only",
        ],
        "must_preserve": [
            "CharacterName/speaker",
            "Serif/text",
            "VoiceCache",
            "VoiceParameter",
            "Pronounce",
            "Hatsuon",
            "VoiceLength unless readback proves a timing-only update needs otherwise",
            "AudioEffects",
            "native voice engine hints",
        ],
        "readback_required": [
            "parse patched structure from ignored local .ymmp copy",
            "compare original and patched frame/duration fields",
            "verify speaker/text/native audio fields are preserved",
            "verify no .ymmp/media output is staged or committed",
        ],
        "render_deferred_until_structural_readback_passes": True,
    }


def _render_gate_carry_forward() -> dict[str, Any]:
    return {
        "render_gate_current": "L0 No Render",
        "next_render_trigger": (
            "after timing patch probe changes timeline surface and structural "
            "readback passes"
        ),
        "render_after_patch_expected_level": [
            "L2 Tiny Smoke Render",
            "L3 Targeted Regression Render",
        ],
        "render_performed_in_this_slice": False,
        "repeated_audio_check": False,
        "do_not_render_for": [
            "strategy docs",
            "readback JSON",
            "policy-only updates",
        ],
    }


def _readiness_separation() -> dict[str, Any]:
    return {
        "slice_completion": {
            "status": "strategy_ready_for_git_gate",
            "expected_after_commit_and_push": "6/6",
        },
        "video_readiness": {
            "status": "incomplete",
            "reason": (
                "timing strategy is defined, but timing patch probe and "
                "post-patch render remain outstanding"
            ),
        },
        "production_readiness": {
            "status": "low_not_accepted",
            "reason": (
                "production narration, visual layout, real content, public use, "
                "and production approval remain outside this diagnostic slice"
            ),
        },
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
        "neutral_68_sec_timing_proof": False,
    }


def _goal_stack() -> list[dict[str, str]]:
    return [
        {
            "level": "Immediate",
            "goal": "Define timing patch strategy",
            "success_signal": "strategy JSON/readback chooses a probe-ready path",
            "contribution": "separates timing from audio/render",
        },
        {
            "level": "Short-term",
            "goal": "Prepare safe timing patch probe",
            "success_signal": "next slice has allowed fields and preservation rules",
            "contribution": "prevents destructive .ymmp edits",
        },
        {
            "level": "Mid-term",
            "goal": "Move from 8 sec diagnostic render toward 68 sec neutral timeline",
            "success_signal": "patch probe structurally proves duration/timing change",
            "contribution": "enables milestone render only when video surface changes",
        },
        {
            "level": "Long-term",
            "goal": "Reach internal review video v0.1",
            "success_signal": "timing/audio/render axes advance without repeated loops",
            "contribution": "reduces stagnation",
        },
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "current_repo_state_verified", "status": "passed"},
        {"gate": "source_timing_audio_render_artifacts_inspected", "status": "passed"},
        {"gate": "timing_strategy_candidates_evaluated", "status": "passed"},
        {"gate": "recommended_default_selected", "status": RECOMMENDED_DEFAULT},
        {"gate": "next_patch_probe_boundary_defined", "status": "passed"},
        {"gate": "narrow_commit_and_push_if_gate_passes", "status": "pending_until_git_gate"},
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"artifact": "strategy_json", "status": "present"},
        {"artifact": "human_readback", "status": "present"},
        {"artifact": "candidate_comparison", "status": "present"},
        {"artifact": "recommended_default", "status": "present"},
        {"artifact": "render_gate_carry_forward", "status": "present"},
        {"artifact": "downstream_next_use", "status": "present"},
    ]


def _video_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "source_input_path_proven", "status": True},
        {"gate": "target_yym4_import_path_proven", "status": True},
        {"gate": "audio_path_proven", "status": True},
        {"gate": "timing_duration_strategy_defined", "status": True},
        {"gate": "tiny_smoke_render_observed", "status": True},
        {"gate": "targeted_regression_render_observed_if_required", "status": False},
        {"gate": "internal_review_milestone_reached", "status": False},
    ]


def _production_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "diagnostic_render_exists", "status": True},
        {"gate": "internal_review_accepted", "status": False},
        {"gate": "quality_thresholds_met", "status": False},
        {"gate": "rights_publication_boundary_cleared", "status": False},
        {"gate": "production_export_settings_accepted", "status": False},
        {"gate": "final_artifact_packaged", "status": False},
        {"gate": "public_prod_use_explicitly_approved", "status": False},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "render_performed_in_this_slice", "status": False},
        {"gate": "existing_render_audio_evidence_reused", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {"gate": "next_render_tied_to_timing_patch_probe_milestone", "status": True},
        {"gate": "no_render_for_docs_readback_changes", "status": True},
        {"gate": "repeated_audio_render_check_avoided", "status": True},
    ]


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "user_input", "status": "freeform"},
        {"gate": "template_required", "status": False},
        {"gate": "schema_owner", "status": "Agent"},
        {"gate": "user_side_work", "status": "none"},
        {"gate": "future_look_for_points_max", "status": 3},
        {"gate": "negative_confirmation_checklist", "status": False},
        {"gate": "fixed_form_relapse", "status": False},
    ]


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"gate": "prior_render_evidence_reused", "status": True},
        {"gate": "prior_audio_evidence_reused", "status": True},
        {"gate": "prior_timing_gap_strategy_reused", "status": True},
        {"gate": "next_axis_stated_as_timing", "status": True},
        {"gate": "not_accepted_scope_preserved", "status": True},
        {"gate": "repeated_audio_render_review_requested", "status": False},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "packet_for_packet_drift", "status": False},
        {"gate": "readback_only_stall", "status": False},
        {"gate": "repeated_render_request", "status": False},
        {"gate": "product_video_readiness_separated_from_slice_completion", "status": True},
        {"gate": "next_concrete_milestone", "status": NEXT_PATCH_PROBE_SLICE},
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
        "dashboard_governance_freshness_changed": False,
    }


def _append_mapping(
    lines: list[str],
    title: str,
    mapping: Any,
) -> None:
    lines.extend(["", f"## {title}", ""])
    for key, value in _dict(mapping).items():
        lines.append(f"- {key}: {_display(value)}")


def _append_status_table(
    lines: list[str],
    title: str,
    rows: Any,
    key_name: str = "gate",
) -> None:
    lines.extend(["", f"## {title}", "", "| item | status |", "|---|---|"])
    for row in rows if isinstance(rows, list) else []:
        key = row.get(key_name) or row.get("artifact") or row.get("goal") or "item"
        if "status" in row:
            status = row["status"]
        elif "success_signal" in row:
            status = row["success_signal"]
        else:
            status = row.get("contribution")
        lines.append(f"| {key} | {_display(status)} |")


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _number(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _whole_number(value: Any) -> int | float | None:
    number = _number(value)
    if number is None:
        return None
    return int(number) if number.is_integer() else number


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
