"""Audio observation and timing patch readiness for the newsroom lane.

This module records a user freeform audio observation as repo readback and
separates the next timing patch axis. It does not launch YMM4, render, generate
TTS/audio, import real media, edit .ymmp files, or approve production use.
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
from src.pipeline.newsroom_yym4_native_audio_path_proof import (
    DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH,
)
from src.pipeline.newsroom_yym4_timing_gap_strategy import (
    DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH,
)


AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_SCHEMA_VERSION = (
    "newsroom_audio_observation_and_timing_patch_readiness.v1"
)
AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_ID = (
    "newsroom_audio_observation_and_timing_patch_readiness_v1_2026_06_24"
)
DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "audio_observation_and_timing_patch_readiness_v1.json"
)
DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_V1_2026-06-24.md"
)

VOICE_PATH = "YMM4_native_yukkuri_japanese"
ENGLISH_WORD_HANDLING = "katakana_loanword_style"
OBSERVED_SOURCE_WORD = "Fake"
OBSERVED_READING = "フェイク"
OBSERVED_READING_UNICODE_ESCAPE = "\\u30d5\\u30a7\\u30a4\\u30af"
NEXT_RECOMMENDED_SLICE = "newsroom-ymmp-timing-patch-strategy-v1"
TIMING_PATCH_PROBE_SLICE = "newsroom-ymmp-timing-patch-probe-v1"
MILESTONE_RENDER_AFTER_TIMING_PATCH = (
    "milestone-gated-render-smoke-after-timing-patch"
)
OPTIONAL_RETENTION_SLICE = "newsroom-render-output-retention-policy-v1"


def build_default_newsroom_audio_observation_and_timing_patch_readiness(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed readback from source artifacts."""
    base = Path(root) if root is not None else Path(".")
    native_audio_path_proof = load_json_object(
        base / DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH
    )
    tiny_render_result = load_json_object(
        base / DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    audio_tts_boundary = load_json_object(base / DEFAULT_AUDIO_TTS_BOUNDARY_PATH)
    timing_strategy = load_json_object(base / DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH)
    structure_readback = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
    )
    return build_newsroom_audio_observation_and_timing_patch_readiness(
        native_audio_path_proof,
        tiny_render_result,
        audio_tts_boundary,
        timing_strategy,
        structure_readback,
        source_native_audio_path_proof_path=(
            DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH
        ),
        source_tiny_render_result_path=(
            DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        source_audio_tts_boundary_path=DEFAULT_AUDIO_TTS_BOUNDARY_PATH,
        source_timing_strategy_path=DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH,
        source_structure_readback_path=DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH,
    )


def build_newsroom_audio_observation_and_timing_patch_readiness(
    native_audio_path_proof: dict[str, Any],
    tiny_render_result: dict[str, Any],
    audio_tts_boundary: dict[str, Any],
    timing_strategy: dict[str, Any],
    structure_readback: dict[str, Any],
    *,
    source_native_audio_path_proof_path: str | Path,
    source_tiny_render_result_path: str | Path,
    source_audio_tts_boundary_path: str | Path,
    source_timing_strategy_path: str | Path,
    source_structure_readback_path: str | Path,
) -> dict[str, Any]:
    """Build a diagnostic audio observation and timing readiness readback."""
    source_validation = _source_validation(
        native_audio_path_proof,
        tiny_render_result,
        audio_tts_boundary,
        timing_strategy,
        structure_readback,
    )
    timing_readiness = _timing_readiness(tiny_render_result, timing_strategy)
    accepted_scope = _accepted_scope()
    not_accepted_scope = _not_accepted_scope()

    return {
        "artifact_id": AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_ID,
        "readback_id": AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_ID,
        "schema_version": (
            AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_SCHEMA_VERSION
        ),
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "observation_source": "user_freeform",
        "readiness_status": (
            "accepted_for_timing_patch_strategy"
            if not source_validation["errors"]
            else "blocked"
        ),
        "identity": {
            "readback_id": AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_ID,
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
            "source_audio_tts_boundary_path": _path_text(
                source_audio_tts_boundary_path
            ),
            "source_audio_tts_boundary_id": audio_tts_boundary.get("boundary_id"),
            "source_timing_strategy_path": _path_text(source_timing_strategy_path),
            "source_timing_strategy_id": timing_strategy.get("strategy_id"),
            "source_structure_readback_path": _path_text(
                source_structure_readback_path
            ),
            "source_structure_readback_id": structure_readback.get("readback_id"),
            "production_status": "diagnostic_only",
            "observation_source": "user_freeform",
        },
        "source_validation": source_validation,
        "normalized_audio_observation": _normalized_audio_observation(),
        "accepted_scope": accepted_scope,
        "not_accepted_scope": not_accepted_scope,
        "timing_readiness": timing_readiness,
        "render_gate_policy": _render_gate_policy(),
        "progress_strip": {
            "lane": "VIDEO v0.1 READINESS",
            "progress_completed": 5,
            "progress_total": 7,
            "current": "tiny render + native audio diagnostic pass",
            "next": NEXT_RECOMMENDED_SLICE,
            "main_blocker": "8 sec natural duration vs 68 sec neutral timeline",
            "user_work": "none",
        },
        "recommended_next_slices": [
            NEXT_RECOMMENDED_SLICE,
            TIMING_PATCH_PROBE_SLICE,
            MILESTONE_RENDER_AFTER_TIMING_PATCH,
            OPTIONAL_RETENTION_SLICE,
        ],
        "recommended_next_slice_notes": {
            NEXT_RECOMMENDED_SLICE: (
                "Separate the neutral 68 second timing patch strategy from "
                "audio acceptance now that native audio is diagnostic-acceptable."
            ),
            TIMING_PATCH_PROBE_SLICE: (
                "Apply or simulate the selected timing patch boundary after the "
                "strategy is recorded, without mixing it into this readback."
            ),
            MILESTONE_RENDER_AFTER_TIMING_PATCH: (
                "Render only after the timing patch or another output-affecting "
                "milestone changes what the video would contain."
            ),
            OPTIONAL_RETENTION_SLICE: (
                "Use only if the local diagnostic output file needs explicit "
                "retention policy later."
            ),
        },
        "completion_matrix": _completion_matrix(),
        "artifact_readiness": _artifact_readiness(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(),
        "boundaries": _boundaries(),
        "downstream_next_use": {
            "use_this_readback_to": [
                "treat the tiny render audio as present and diagnostic-acceptable",
                "keep YMM4 native yukkuri audio as the current diagnostic path",
                "move to a timing patch strategy without adding external TTS",
                "preserve production readiness as a separate later decision",
            ],
            "do_not_use_this_readback_to": [
                "claim production narration quality",
                "claim public video readiness",
                "claim neutral 68 second timing proof",
                "launch YMM4 or create a new render",
                "generate, import, stage, or commit audio/media output",
            ],
        },
        "validation_expectations": {
            "json_parse_required": True,
            "focused_tests_required_if_builder_added": True,
            "compileall_required_if_python_module_added": True,
            "git_diff_check_required": True,
            "conflict_marker_scan_required": True,
            "fixed_form_relapse_scan_required": True,
            "forbidden_staged_file_scan_required": True,
            "YMM4_launched_by_agent": False,
            "render_audio_or_tts_created_by_agent": False,
        },
    }


def render_newsroom_audio_observation_and_timing_patch_readiness_markdown(
    readback: dict[str, Any],
) -> str:
    """Render the human-readable audio observation readiness document."""
    identity = _dict(readback.get("identity"))
    validation = _dict(readback.get("source_validation"))
    observation = _dict(readback.get("normalized_audio_observation"))
    timing = _dict(readback.get("timing_readiness"))
    render_gate = _dict(readback.get("render_gate_policy"))
    progress = _dict(readback.get("progress_strip"))

    lines = [
        "# Newsroom Audio Observation And Timing Patch Readiness v1",
        "",
        f"artifact_id: {readback.get('artifact_id')}",
        f"readback_id: {readback.get('readback_id')}",
        f"schema_version: {readback.get('schema_version')}",
        f"review_status: {readback.get('review_status')}",
        f"production_status: {readback.get('production_status')}",
        f"readiness_status: {readback.get('readiness_status')}",
        f"observation_source: {readback.get('observation_source')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
    ]
    for key, value in identity.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Source Validation", ""])
    for key, value in validation.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Normalized Audio Observation", ""])
    for key, value in observation.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Accepted Scope", ""])
    for key, value in _dict(readback.get("accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(readback.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Timing Readiness", ""])
    for key, value in timing.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Render Gate Policy", ""])
    for key, value in render_gate.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Progress Strip", ""])
    for key, value in progress.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Recommended Next Slices",
            "",
            "| slice | why it is next |",
            "|---|---|",
        ]
    )
    notes = _dict(readback.get("recommended_next_slice_notes"))
    for item in readback.get("recommended_next_slices", []):
        lines.append(f"| {item} | {notes.get(item)} |")

    _append_status_table(lines, "Completion Matrix", readback.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", readback.get("artifact_readiness"))
    _append_status_table(
        lines,
        "Human Burden Hygiene",
        readback.get("human_burden_hygiene"),
    )
    _append_status_table(lines, "Render Gate Hygiene", readback.get("render_gate_hygiene"))
    _append_status_table(
        lines,
        "Review Non-Redundancy",
        readback.get("review_non_redundancy"),
    )
    _append_status_table(lines, "Inertia Check", readback.get("inertia_check"))

    lines.extend(["", "## Boundaries", ""])
    for key, value in _dict(readback.get("boundaries")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "The user freeform audio observation is consumed once as diagnostic "
            "evidence: audio is present, the YMM4 native yukkuri Japanese path "
            "is acceptable for the diagnostic flow, and the next nonredundant "
            "axis is the neutral timing patch strategy. This does not accept "
            "production narration quality, public video readiness, visual "
            "layout readiness, real content readiness, or production approval.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    native_audio_path_proof: dict[str, Any],
    tiny_render_result: dict[str, Any],
    audio_tts_boundary: dict[str, Any],
    timing_strategy: dict[str, Any],
    structure_readback: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    proof_validation = _dict(native_audio_path_proof.get("source_validation"))
    normalized = _dict(tiny_render_result.get("normalized_result"))
    timing_facts = _dict(timing_strategy.get("timing_facts"))
    timing_gap_status = _timing_gap_status(timing_strategy)
    structure_dialogue = _dict(structure_readback.get("dialogue_structure"))

    if native_audio_path_proof.get("production_status") != "diagnostic_only":
        errors.append("NATIVE_AUDIO_PROOF_NOT_DIAGNOSTIC_ONLY")
    if native_audio_path_proof.get("proof_status") != "passed_with_unknowns":
        errors.append("NATIVE_AUDIO_PROOF_NOT_PASSED_WITH_UNKNOWNS")
    if proof_validation.get("canonical_speaker_value") != CANONICAL_UI_OBSERVED_SPEAKER:
        errors.append("NATIVE_AUDIO_PROOF_SPEAKER_MISMATCH")
    if tiny_render_result.get("production_status") != "diagnostic_only":
        errors.append("TINY_RENDER_RESULT_NOT_DIAGNOSTIC_ONLY")
    if normalized.get("result") != "pass":
        errors.append("TINY_RENDER_RESULT_NOT_PASS")
    if normalized.get("output_duration_observed_sec") != 8:
        errors.append("TINY_RENDER_DURATION_NOT_APPROX_8")
    if audio_tts_boundary.get("boundary_status") != "accepted_for_next_audio_observation":
        errors.append("AUDIO_TTS_BOUNDARY_NOT_ACCEPTED")
    if timing_strategy.get("strategy_status") != "accepted_for_next_tiny_render_smoke":
        errors.append("TIMING_STRATEGY_NOT_ACCEPTED")
    if timing_facts.get("neutral_timeline_total_sec") != 68:
        errors.append("NEUTRAL_TIMELINE_TOTAL_NOT_68")
    if timing_gap_status != "unresolved":
        errors.append("TIMING_GAP_NOT_UNRESOLVED")
    if structure_dialogue.get("canonical_speaker_value") != CANONICAL_UI_OBSERVED_SPEAKER:
        errors.append("STRUCTURE_SPEAKER_MISMATCH")

    return {
        "status": "passed" if not errors else "blocked",
        "native_audio_path_proof_id": native_audio_path_proof.get("proof_id"),
        "tiny_render_result_id": tiny_render_result.get("result_id"),
        "audio_tts_boundary_id": audio_tts_boundary.get("boundary_id"),
        "timing_strategy_id": timing_strategy.get("strategy_id"),
        "structure_readback_id": structure_readback.get("readback_id"),
        "canonical_speaker": structure_dialogue.get("canonical_speaker_value"),
        "canonical_speaker_unicode_escape": structure_dialogue.get(
            "canonical_speaker_unicode_escape",
            CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
        ),
        "native_audio_path_prior_status": native_audio_path_proof.get(
            "proof_status"
        ),
        "tiny_render_result": normalized.get("result"),
        "tiny_render_duration_sec": normalized.get("output_duration_observed_sec"),
        "timing_gap_status": timing_gap_status,
        "errors": errors,
    }


def _normalized_audio_observation() -> dict[str, Any]:
    return {
        "audio_presence_in_render": True,
        "voice_path": VOICE_PATH,
        "canonical_speaker": CANONICAL_UI_OBSERVED_SPEAKER,
        "canonical_speaker_unicode_escape": CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
        "english_word_handling": ENGLISH_WORD_HANDLING,
        "observed_example": {
            "source_text": OBSERVED_SOURCE_WORD,
            "observed_reading": OBSERVED_READING,
            "observed_reading_unicode_escape": OBSERVED_READING_UNICODE_ESCAPE,
            "normalization": f"{OBSERVED_SOURCE_WORD} -> {OBSERVED_READING}",
        },
        "spelling_read_issue": False,
        "diagnostic_audio_path_accepted": True,
        "audio_quality_accepted_for_diagnostic_flow": True,
        "audio_quality_accepted_for_production": False,
        "TTS_ready_for_production": False,
        "external_TTS_introduced": False,
        "production_ready": False,
    }


def _accepted_scope() -> dict[str, bool]:
    return {
        "tiny_render_includes_audible_native_yym4_yukkuri_voice": True,
        "audio_sufficient_to_continue_diagnostic_flow": True,
        "english_loanword_handling_acceptable_for_diagnostic_flow": True,
        "external_TTS_unnecessary_for_now": True,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_narration_quality": False,
        "final_subtitle_narration_script": False,
        "public_video_readiness": False,
        "neutral_68_sec_timing_proof": False,
        "visual_layout_readiness": False,
        "real_content_readiness": False,
        "production_approval": False,
    }


def _timing_readiness(
    tiny_render_result: dict[str, Any],
    timing_strategy: dict[str, Any],
) -> dict[str, Any]:
    normalized = _dict(tiny_render_result.get("normalized_result"))
    timing_facts = _dict(timing_strategy.get("timing_facts"))
    return {
        "tiny_render_duration_sec": normalized.get("output_duration_observed_sec"),
        "tiny_render_duration_qualifier": normalized.get(
            "output_duration_observed_qualifier",
            "approx",
        ),
        "first_smoke_timing_mode": "YMM4 natural duration",
        "neutral_timeline_total_sec": timing_facts.get("neutral_timeline_total_sec"),
        "ymmp_natural_duration_sec": timing_facts.get("ymmp_total_duration_sec"),
        "timing_gap_status": _timing_gap_status(timing_strategy),
        "neutral_68_sec_timing_patch_applied": False,
        "recommended_next_axis": NEXT_RECOMMENDED_SLICE,
        "reason": [
            "render path works",
            "native audio path is diagnostic-acceptable",
            "external TTS remains closed",
            "timing patch can now be handled as a separate axis",
        ],
    }


def _render_gate_policy() -> dict[str, Any]:
    return {
        "new_render_in_this_slice": False,
        "render_gate": "milestone_gated_not_change_gated",
        "future_render_condition": (
            "only after timing patch or another output-affecting milestone"
        ),
        "do_not_rerender_for": [
            "docs changes",
            "readback changes",
            "policy changes",
        ],
    }


def _timing_gap_status(timing_strategy: dict[str, Any]) -> Any:
    timing_facts = _dict(timing_strategy.get("timing_facts"))
    source_validation = _dict(timing_strategy.get("source_validation"))
    return (
        timing_facts.get("timing_gap_status")
        or timing_facts.get("source_timing_gap_status")
        or source_validation.get("timing_gap_status")
    )


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "permission_preflight", "status": "passed"},
        {"gate": "current_state_verified", "status": "passed"},
        {"gate": "native_audio_proof_inspected", "status": "passed"},
        {"gate": "user_freeform_audio_observation_normalized", "status": "passed"},
        {"gate": "timing_patch_readiness_recorded", "status": "passed"},
        {"gate": "narrow_commit_and_push_if_gate_passes", "status": "pending_until_git_gate"},
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"artifact": "readback_json", "status": "present"},
        {"artifact": "human_readback", "status": "present"},
        {"artifact": "normalized_audio_observation", "status": "present"},
        {"artifact": "accepted_and_not_accepted_scopes", "status": "present"},
        {"artifact": "timing_readiness", "status": "present"},
        {"artifact": "downstream_next_use", "status": "present"},
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


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "render_performed_in_this_slice", "status": False},
        {"gate": "existing_render_observation_reused", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {"gate": "next_render_tied_to_output_milestone", "status": True},
        {"gate": "no_render_for_docs_readback_changes", "status": True},
        {"gate": "output_retention_deferred_unless_needed", "status": True},
    ]


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"gate": "prior_render_evidence_reused", "status": True},
        {"gate": "prior_audio_tts_boundary_reused", "status": True},
        {"gate": "user_audio_observation_consumed_once", "status": True},
        {"gate": "next_axis_stated", "status": NEXT_RECOMMENDED_SLICE},
        {"gate": "not_accepted_scope_preserved", "status": True},
        {"gate": "repeated_audio_check_requested", "status": False},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "repeated_render_request", "status": False},
        {"gate": "repeated_audio_observation_request", "status": False},
        {"gate": "packet_for_packet_drift", "status": False},
        {"gate": "video_readiness_separated_from_slice_completion", "status": True},
        {"gate": "next_concrete_milestone", "status": NEXT_RECOMMENDED_SLICE},
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


def _append_status_table(
    lines: list[str],
    title: str,
    rows: Any,
) -> None:
    lines.extend(["", f"## {title}", "", "| item | status |", "|---|---|"])
    for row in rows if isinstance(rows, list) else []:
        key = row.get("gate") or row.get("artifact") or "item"
        lines.append(f"| {key} | {_display(row.get('status'))} |")


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
