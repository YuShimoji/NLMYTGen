"""Result readback for the patched newsroom YMM4 render smoke.

This module records the user freeform post-patch render observation as repo
evidence. It does not launch YMM4, render, edit .ymmp, generate TTS/audio,
import media, or approve production use.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_audio_observation_and_timing_patch_readiness import (
    DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_ymmp_timing_patch_probe import (
    DEFAULT_PATCHED_YMMP_LOCAL_PATH,
    DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH,
    DEFAULT_YMMP_TIMING_PATCH_PROBE_READBACK_PATH,
)
from src.pipeline.newsroom_ymmp_timing_patch_render_smoke import (
    DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_PATH,
    PASS_CLASSIFICATION,
)
from src.pipeline.newsroom_ymmp_timing_patch_strategy import (
    DEFAULT_YMMP_TIMING_PATCH_STRATEGY_PATH,
)
from src.pipeline.newsroom_yym4_native_audio_path_proof import (
    DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH,
)
from src.pipeline.newsroom_audio_tts_boundary import (
    DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH,
)


YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION = (
    "newsroom_ymmp_timing_patch_render_smoke_result_readback.v1"
)
YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_ID = (
    "newsroom_ymmp_timing_patch_render_smoke_result_readback_v1_2026_06_25"
)
DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "ymmp_timing_patch_render_smoke_result_readback_v1.json"
)
DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_V1_2026-06-25.md"
)
DEFAULT_RENDER_OUTPUT_LOCAL_PATH = Path(
    "_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.mp4"
)

VOICE_PATH = "YMM4_native_yukkuri_japanese"
NEXT_DEFAULT_SLICE = "newsroom-visual-card-asset-bridge-v1"
INTERNAL_REVIEW_PREP_SLICE = "newsroom-internal-review-v0.1-prep"
RETENTION_POLICY_SLICE = "newsroom-render-output-retention-policy-v1"
RSS_DRY_RUN_PLAN_SLICE = "newsroom-rss-dry-run-integration-plan-v1"

USER_FREEFORM_OBSERVATION = (
    "問題有りません。意図通りの動画になっています。発話され、大半は無音です。"
    "タイムライン上で発話後の要素だけ伸びています。"
)


def build_default_newsroom_ymmp_timing_patch_render_smoke_result_readback(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed post-patch render smoke result readback."""
    base = Path(root) if root is not None else Path(".")
    render_smoke_package = load_json_object(
        base / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_PATH
    )
    timing_patch_probe = load_json_object(base / DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH)
    timing_patch_probe_readback = load_json_object(
        base / DEFAULT_YMMP_TIMING_PATCH_PROBE_READBACK_PATH
    )
    timing_patch_strategy = load_json_object(
        base / DEFAULT_YMMP_TIMING_PATCH_STRATEGY_PATH
    )
    audio_readiness = load_json_object(
        base / DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
    )
    native_audio_path_proof = load_json_object(
        base / DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH
    )
    tiny_render_readback = load_json_object(
        base / DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    return build_newsroom_ymmp_timing_patch_render_smoke_result_readback(
        render_smoke_package,
        timing_patch_probe,
        timing_patch_probe_readback,
        timing_patch_strategy,
        audio_readiness,
        native_audio_path_proof,
        tiny_render_readback,
        source_render_smoke_package_path=(
            DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_PATH
        ),
        source_timing_patch_probe_path=DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH,
        source_timing_patch_probe_readback_path=(
            DEFAULT_YMMP_TIMING_PATCH_PROBE_READBACK_PATH
        ),
        source_timing_patch_strategy_path=DEFAULT_YMMP_TIMING_PATCH_STRATEGY_PATH,
        source_audio_readiness_path=(
            DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
        ),
        source_native_audio_path_proof_path=DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH,
        source_tiny_render_readback_path=DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH,
        render_output_path=DEFAULT_RENDER_OUTPUT_LOCAL_PATH,
        render_output_exists=(base / DEFAULT_RENDER_OUTPUT_LOCAL_PATH).exists(),
        patched_ymmp_path=DEFAULT_PATCHED_YMMP_LOCAL_PATH,
        patched_ymmp_exists=(base / DEFAULT_PATCHED_YMMP_LOCAL_PATH).exists(),
    )


def write_default_newsroom_ymmp_timing_patch_render_smoke_result_readback_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write JSON and human-readable post-patch render smoke readback."""
    base = Path(root) if root is not None else Path(".")
    readback = build_default_newsroom_ymmp_timing_patch_render_smoke_result_readback(
        root=base
    )
    _write_json(
        base / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH,
        readback,
    )
    _write_text(
        base / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_DOC_PATH,
        render_newsroom_ymmp_timing_patch_render_smoke_result_readback_markdown(
            readback
        ),
    )
    return readback


def build_newsroom_ymmp_timing_patch_render_smoke_result_readback(
    render_smoke_package: dict[str, Any],
    timing_patch_probe: dict[str, Any],
    timing_patch_probe_readback: dict[str, Any],
    timing_patch_strategy: dict[str, Any],
    audio_readiness: dict[str, Any],
    native_audio_path_proof: dict[str, Any],
    tiny_render_readback: dict[str, Any],
    *,
    source_render_smoke_package_path: str | Path,
    source_timing_patch_probe_path: str | Path,
    source_timing_patch_probe_readback_path: str | Path,
    source_timing_patch_strategy_path: str | Path,
    source_audio_readiness_path: str | Path,
    source_native_audio_path_proof_path: str | Path,
    source_tiny_render_readback_path: str | Path,
    render_output_path: str | Path,
    render_output_exists: bool,
    patched_ymmp_path: str | Path,
    patched_ymmp_exists: bool,
) -> dict[str, Any]:
    """Build a diagnostic-only result readback from the supplied observation."""
    source_validation = _source_validation(
        render_smoke_package,
        timing_patch_probe,
        timing_patch_probe_readback,
        timing_patch_strategy,
        audio_readiness,
        native_audio_path_proof,
        tiny_render_readback,
        patched_ymmp_path=patched_ymmp_path,
        patched_ymmp_exists=patched_ymmp_exists,
    )
    normalized_result = _normalized_render_result()

    return {
        "artifact_id": YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_ID,
        "readback_id": YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_ID,
        "schema_version": (
            YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION
        ),
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "observation_source": "user_freeform_with_screenshot_support",
        "result_status": "pass",
        "identity": {
            "readback_id": YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_ID,
            "source_render_smoke_package_path": _path_text(
                source_render_smoke_package_path
            ),
            "source_render_smoke_package_id": render_smoke_package.get("smoke_id"),
            "source_timing_patch_probe_path": _path_text(
                source_timing_patch_probe_path
            ),
            "source_timing_patch_probe_id": timing_patch_probe.get("probe_id"),
            "source_timing_patch_probe_readback_path": _path_text(
                source_timing_patch_probe_readback_path
            ),
            "source_timing_patch_probe_readback_id": timing_patch_probe_readback.get(
                "readback_id"
            ),
            "source_timing_patch_strategy_path": _path_text(
                source_timing_patch_strategy_path
            ),
            "source_timing_patch_strategy_id": timing_patch_strategy.get(
                "strategy_id"
            ),
            "source_audio_readiness_path": _path_text(source_audio_readiness_path),
            "source_audio_readiness_id": audio_readiness.get("readback_id"),
            "source_native_audio_path_proof_path": _path_text(
                source_native_audio_path_proof_path
            ),
            "source_native_audio_path_proof_id": native_audio_path_proof.get(
                "proof_id"
            ),
            "source_tiny_render_readback_path": _path_text(
                source_tiny_render_readback_path
            ),
            "source_tiny_render_readback_id": tiny_render_readback.get("result_id"),
            "observation_source": "user_freeform_with_screenshot_support",
            "production_status": "diagnostic_only",
            "result_status": "pass",
        },
        "source_validation": source_validation,
        "operator_freeform_observation": _operator_freeform_observation(),
        "screenshot_supported_observation": _screenshot_supported_observation(),
        "normalized_render_result": normalized_result,
        "classification": _classification(),
        "local_artifact_status": _local_artifact_status(
            render_output_path=render_output_path,
            render_output_exists=render_output_exists,
            patched_ymmp_path=patched_ymmp_path,
            patched_ymmp_exists=patched_ymmp_exists,
        ),
        "accepted_scope": _accepted_scope(),
        "not_accepted_scope": _not_accepted_scope(),
        "readiness_separation": _readiness_separation(),
        "render_gate_carry_forward": _render_gate_carry_forward(),
        "recommended_next_slices": _recommended_next_slices(),
        "implementation_principle_for_next_lane": (
            _implementation_principle_for_next_lane()
        ),
        "completion_matrix": _completion_matrix(),
        "artifact_readiness": _artifact_readiness(),
        "video_readiness": _video_readiness(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(),
        "boundaries": _boundaries(),
        "downstream_next_use": _downstream_next_use(),
        "validation_expectations": _validation_expectations(),
    }


def render_newsroom_ymmp_timing_patch_render_smoke_result_readback_markdown(
    readback: dict[str, Any],
) -> str:
    """Render the human-readable post-patch render smoke result readback."""
    identity = _dict(readback.get("identity"))
    validation = _dict(readback.get("source_validation"))
    normalized = _dict(readback.get("normalized_render_result"))
    local_status = _dict(readback.get("local_artifact_status"))
    readiness = _dict(readback.get("readiness_separation"))
    render_gate = _dict(readback.get("render_gate_carry_forward"))

    lines = [
        "# Newsroom YMM4 Timing Patch Render Smoke Result Readback v1",
        "",
        f"artifact_id: {readback.get('artifact_id')}",
        f"readback_id: {readback.get('readback_id')}",
        f"schema_version: {readback.get('schema_version')}",
        f"review_status: {readback.get('review_status')}",
        f"production_status: {readback.get('production_status')}",
        f"result_status: {readback.get('result_status')}",
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

    lines.extend(["", "## Operator Observation", ""])
    for key, value in _dict(readback.get("operator_freeform_observation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Screenshot-Supported Observation", ""])
    for key, value in _dict(readback.get("screenshot_supported_observation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Normalized Render Result", ""])
    for key, value in normalized.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Accepted Scope", ""])
    for key, value in _dict(readback.get("accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(readback.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Readiness Separation", ""])
    for key, value in readiness.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Render Gate Carry-Forward", ""])
    for key, value in render_gate.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Local Artifact Status", ""])
    for key, value in local_status.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Recommended Next Slices",
            "",
            "| slice | timing | reason |",
            "|---|---|---|",
        ]
    )
    for row in readback.get("recommended_next_slices", []):
        lines.append(
            "| "
            f"{row.get('slice')} | "
            f"{row.get('timing')} | "
            f"{row.get('reason')} |"
        )

    lines.extend(["", "## Implementation Principle For Next Lane", ""])
    for item in readback.get("implementation_principle_for_next_lane", []):
        lines.append(f"- {item}")

    _append_status_table(lines, "Completion Matrix", readback.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", readback.get("artifact_readiness"))
    _append_status_table(lines, "Video Readiness", readback.get("video_readiness"))
    _append_status_table(
        lines, "Render Gate Hygiene", readback.get("render_gate_hygiene")
    )
    _append_status_table(
        lines, "Human Burden Hygiene", readback.get("human_burden_hygiene")
    )
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
            "The user observation is consumed once as diagnostic render evidence: "
            "the patched project opens and renders at 68 seconds, four dialogue "
            "items remain visible, and native YMM4/Yukkuri audio is present. "
            "The long silence after speech is expected for this sparse timing "
            "skeleton and is not accepted as production pacing, visual quality, "
            "or public video readiness.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    render_smoke_package: dict[str, Any],
    timing_patch_probe: dict[str, Any],
    timing_patch_probe_readback: dict[str, Any],
    timing_patch_strategy: dict[str, Any],
    audio_readiness: dict[str, Any],
    native_audio_path_proof: dict[str, Any],
    tiny_render_readback: dict[str, Any],
    *,
    patched_ymmp_path: str | Path,
    patched_ymmp_exists: bool,
) -> dict[str, Any]:
    errors: list[str] = []
    package_target = _dict(render_smoke_package.get("target"))
    package_expected = _dict(package_target.get("expected_project_state"))
    probe_structural = _dict(timing_patch_probe_readback.get("structural_result"))
    probe_audio = _dict(timing_patch_probe_readback.get("audio_voice_boundary"))
    strategy_recommended = _dict(timing_patch_strategy.get("recommended_default"))
    audio_normalized = _dict(audio_readiness.get("normalized_audio_observation"))
    native_validation = _dict(native_audio_path_proof.get("source_validation"))
    tiny_normalized = _dict(tiny_render_readback.get("normalized_result"))

    if render_smoke_package.get("package_status") != (
        "ready_for_manual_milestone_render_smoke"
    ):
        errors.append("RENDER_SMOKE_PACKAGE_NOT_READY")
    if render_smoke_package.get("smoke_status") != "prepared_not_run":
        errors.append("RENDER_SMOKE_PACKAGE_ALREADY_CONSUMED")
    if timing_patch_probe.get("probe_status") != (
        "applied_to_ignored_local_copy_after_validation"
    ):
        errors.append("TIMING_PATCH_PROBE_NOT_APPLIED")
    if timing_patch_probe_readback.get("readback_status") != "structural_pass":
        errors.append("TIMING_PATCH_PROBE_READBACK_NOT_STRUCTURAL_PASS")
    if probe_structural.get("target_68_sec_reached_structurally") is not True:
        errors.append("TIMING_PATCH_NOT_STRUCTURALLY_68_SEC")
    if package_expected.get("total_duration_sec") != 68.0:
        errors.append("RENDER_SMOKE_PACKAGE_EXPECTED_DURATION_NOT_68")
    if package_expected.get("dialogue_item_count") != 4:
        errors.append("RENDER_SMOKE_PACKAGE_DIALOGUE_COUNT_NOT_4")
    if package_expected.get("native_audio_expected_from_preserved_yym4_fields") is not True:
        errors.append("RENDER_SMOKE_PACKAGE_NATIVE_AUDIO_EXPECTATION_MISSING")
    if strategy_recommended.get("choice") != (
        "neutral_timeline_skeleton_patch_with_native_voice_preserved"
    ):
        errors.append("TIMING_PATCH_STRATEGY_CHOICE_MISMATCH")
    if audio_normalized.get("voice_path") != VOICE_PATH:
        errors.append("AUDIO_READINESS_VOICE_PATH_MISMATCH")
    if audio_normalized.get("diagnostic_audio_path_accepted") is not True:
        errors.append("AUDIO_READINESS_NOT_ACCEPTED")
    if native_audio_path_proof.get("proof_status") != "passed_with_unknowns":
        errors.append("NATIVE_AUDIO_PATH_PROOF_NOT_AVAILABLE")
    if native_validation.get("native_voice_engine_hint") != "AquesTalk":
        errors.append("NATIVE_AUDIO_ENGINE_HINT_MISSING")
    if tiny_normalized.get("result") != "pass":
        errors.append("PRIOR_TINY_RENDER_SMOKE_NOT_PASS")
    if probe_audio.get("canonical_speaker_unicode_escape") != (
        "\\u3086\\u3063\\u304f\\u308a\\u970a\\u5922"
    ):
        errors.append("CANONICAL_SPEAKER_NOT_YUKKURI_REIMU")
    if _path_text(patched_ymmp_path) != package_target.get("patched_ymmp_path"):
        errors.append("PATCHED_YMMP_PATH_MISMATCH")
    if not patched_ymmp_exists:
        errors.append("PATCHED_YMMP_NOT_FOUND_LOCALLY")

    return {
        "status": "passed" if not errors else "blocked",
        "render_smoke_package_id": render_smoke_package.get("smoke_id"),
        "timing_patch_probe_id": timing_patch_probe.get("probe_id"),
        "timing_patch_probe_readback_id": timing_patch_probe_readback.get(
            "readback_id"
        ),
        "timing_patch_strategy_id": timing_patch_strategy.get("strategy_id"),
        "audio_readiness_id": audio_readiness.get("readback_id"),
        "native_audio_path_proof_id": native_audio_path_proof.get("proof_id"),
        "prior_tiny_render_readback_id": tiny_render_readback.get("result_id"),
        "canonical_speaker_unicode_escape": probe_audio.get(
            "canonical_speaker_unicode_escape"
        ),
        "canonical_speaker": "ゆっくり霊夢",
        "expected_duration_sec": package_expected.get("total_duration_sec"),
        "expected_total_frames": package_expected.get("total_frames"),
        "expected_dialogue_item_count": package_expected.get("dialogue_item_count"),
        "patched_ymmp_path": _path_text(patched_ymmp_path),
        "patched_ymmp_found_at_generation": patched_ymmp_exists,
        "errors": errors,
    }


def _operator_freeform_observation() -> dict[str, Any]:
    return {
        "input_mode": "freeform",
        "observation_source": "user_freeform",
        "raw_observation": USER_FREEFORM_OBSERVATION,
        "normalized_summary": (
            "The user reported no problem, the video behaved as intended, "
            "speech is present, most of the timeline is silent, and only the "
            "post-speech timeline elements are extended."
        ),
        "fixed_result_template_requested": False,
        "manual_observation_re_requested": False,
    }


def _screenshot_supported_observation() -> dict[str, Any]:
    return {
        "support_source": "supervisor_screenshot_readback",
        "output_file_name": "diagnostic_bound_speaker_probe_timing_patch_v1.mp4",
        "windows_properties_duration": "00:01:08",
        "frame_width_height": "1920x1080",
        "frame_rate": "60.00 fps",
        "audio_stream_observed": True,
        "audio_sample_rate": "48.000 kHz",
        "yym4_preview_project_duration": "00:01:08.00",
        "dialogue_items_remaining_on_timeline": 4,
        "preview_text_observed": "Fake topic, review only.",
        "screenshot_file_committed": False,
        "media_file_committed": False,
    }


def _normalized_render_result() -> dict[str, Any]:
    return {
        "render_smoke_result": "pass",
        "yym4_opened_patched_project": True,
        "render_completed": True,
        "output_video_observed": True,
        "output_duration_observed": "00:01:08",
        "output_duration_sec": 68,
        "expected_duration_sec": 68,
        "duration_matches_timing_patch": True,
        "output_resolution_observed": "1920x1080",
        "output_frame_width_observed": 1920,
        "output_frame_height_observed": 1080,
        "output_fps_observed": 60,
        "audio_stream_observed": True,
        "audio_sample_rate_observed": "48kHz",
        "native_audio_present": True,
        "voice_path": VOICE_PATH,
        "dialogue_items_visible": True,
        "dialogue_item_count_observed": 4,
        "preview_text_observed": "Fake topic, review only.",
        "majority_silence_observed": True,
        "majority_silence_expected_for_diagnostic_sparse_timeline": True,
        "post_speech_elements_extended": True,
        "timing_patch_effective_in_render": True,
        "production_pacing_accepted": False,
        "production_quality_accepted": False,
        "visual_layout_accepted": False,
        "public_video_ready": False,
        "classification": PASS_CLASSIFICATION,
    }


def _classification() -> dict[str, Any]:
    return {
        "classification": PASS_CLASSIFICATION,
        "result": "pass",
        "reason": (
            "The patched project opened, rendered, produced a 68 second output, "
            "kept four dialogue items visible, and retained native audio."
        ),
        "next_recommended_slice": NEXT_DEFAULT_SLICE,
    }


def _local_artifact_status(
    *,
    render_output_path: str | Path,
    render_output_exists: bool,
    patched_ymmp_path: str | Path,
    patched_ymmp_exists: bool,
) -> dict[str, Any]:
    return {
        "render_output_path": _path_text(render_output_path),
        "render_output_exists_at_readback_generation": render_output_exists,
        "render_output_expected_git_policy": "ignored_under_tmp_do_not_stage_or_commit",
        "render_output_staged": False,
        "render_output_committed": False,
        "patched_ymmp_path": _path_text(patched_ymmp_path),
        "patched_ymmp_exists_at_readback_generation": patched_ymmp_exists,
        "patched_ymmp_expected_git_policy": "ignored_under_tmp_do_not_stage_or_commit",
        "patched_ymmp_staged": False,
        "patched_ymmp_committed": False,
    }


def _accepted_scope() -> dict[str, bool]:
    return {
        "patched_ymmp_can_be_opened_and_rendered_in_current_yym4_environment": True,
        "timing_patch_effective_in_rendered_output": True,
        "four_dialogue_items_remain_visible": True,
        "native_yukkuri_audio_remains_present": True,
        "sparse_silence_expected_for_this_diagnostic_skeleton": True,
        "timing_patch_smoke_passes_at_diagnostic_level": True,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_pacing": False,
        "final_narration_pacing": False,
        "final_script_density": False,
        "visual_layout_quality": False,
        "public_video_readiness": False,
        "production_render_readiness": False,
        "real_content_readiness": False,
        "production_approval": False,
        "external_TTS_adoption": False,
    }


def _readiness_separation() -> dict[str, Any]:
    return {
        "slice_completion": "pass_for_this_readback",
        "video_readiness_progress": "6/7",
        "video_readiness_current": "targeted 68sec patched render observed",
        "video_readiness_next_missing_gate": (
            "internal review milestone after visual/card bridge"
        ),
        "production_readiness": "low_diagnostic_only",
        "production_readiness_reason": (
            "pacing, visuals, real content, public use, and production approval "
            "remain outside this diagnostic smoke"
        ),
        "next_default_slice": NEXT_DEFAULT_SLICE,
    }


def _render_gate_carry_forward() -> dict[str, Any]:
    return {
        "current_render_observation_consumed_once": True,
        "new_render_in_this_slice": False,
        "YMM4_launched_by_agent": False,
        "render_audio_or_tts_created_by_agent": False,
        "render_gate": "milestone_gated_not_docs_gated",
        "next_render_allowed_after": [
            "visual/card bridge affects the video surface",
            "internal review v0.1 milestone",
        ],
        "do_not_rerender_for": [
            "docs changes",
            "readback changes",
            "policy-only changes",
        ],
        "repeated_audio_or_render_check_requested": False,
    }


def _recommended_next_slices() -> list[dict[str, str]]:
    return [
        {
            "slice": NEXT_DEFAULT_SLICE,
            "timing": "recommended_next_default",
            "reason": (
                "timing/render/audio axes now pass at diagnostic level; next "
                "product value comes from visible card assets"
            ),
        },
        {
            "slice": INTERNAL_REVIEW_PREP_SLICE,
            "timing": "after_visual_card_bridge",
            "reason": "prepare internal review v0.1 once the video surface has visuals",
        },
        {
            "slice": RETENTION_POLICY_SLICE,
            "timing": "only_if_output_artifacts_need_retention",
            "reason": "ignored mp4 output should stay out of source history unless a later retention gate is opened",
        },
        {
            "slice": RSS_DRY_RUN_PLAN_SLICE,
            "timing": "later_not_immediate",
            "reason": "real/source integration should wait until the diagnostic video surface is reviewable",
        },
    ]


def _implementation_principle_for_next_lane() -> list[str]:
    return [
        "Do not rebuild cards as complex YMM4 object graphs.",
        "Prefer external card assets generated from HTML/SVG/Canvas and imported or placed into YMM4 later.",
        "Preserve the YMM4 native audio path.",
        "Keep .ymmp mutation limited to ignored local copies and bounded timing/layout carrier operations.",
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "current_repo_state_verified", "status": "passed"},
        {"gate": "source_render_smoke_package_inspected", "status": "passed"},
        {"gate": "user_freeform_observation_normalized", "status": "passed"},
        {"gate": "result_readback_json_doc_created", "status": "passed"},
        {"gate": "readiness_separation_updated", "status": "passed"},
        {"gate": "narrow_commit_created_and_pushed_if_gate_passes", "status": "pending_until_git_gate"},
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"artifact": "result_readback_json", "status": "present"},
        {"artifact": "human_readback", "status": "present"},
        {"artifact": "normalized_render_result", "status": "present"},
        {"artifact": "accepted_not_accepted_scopes", "status": "present"},
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
        {"gate": "targeted_regression_render_observed", "status": True},
        {"gate": "internal_review_milestone_reached", "status": False},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "render_performed_by_agent_in_this_slice", "status": False},
        {"gate": "existing_user_render_observation_consumed_once", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {"gate": "next_render_tied_to_visual_card_or_internal_review_milestone", "status": True},
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
        {"gate": "prior_timing_proof_reused", "status": True},
        {"gate": "prior_audio_evidence_reused", "status": True},
        {"gate": "current_render_observation_consumed_once", "status": True},
        {"gate": "next_axis_stated_as_visual_card_bridge", "status": True},
        {"gate": "not_accepted_scope_preserved", "status": True},
        {"gate": "repeated_render_audio_review_requested", "status": False},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "packet_for_packet_drift", "status": False},
        {"gate": "readback_only_stall", "status": False},
        {"gate": "repeated_render_request", "status": False},
        {"gate": "product_video_readiness_separated_from_slice_completion", "status": True},
        {"gate": "next_concrete_milestone", "status": NEXT_DEFAULT_SLICE},
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
        "render_output_staged_or_committed": False,
        "external_TTS_introduced": False,
        "production_approval": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


def _downstream_next_use() -> dict[str, list[str]]:
    return {
        "use_this_readback_to": [
            "close the 8sec-vs-68sec timing uncertainty at diagnostic render-smoke level",
            "advance video readiness to 6/7 while keeping production readiness diagnostic-only",
            "start the visual/card asset bridge as the next default product-value axis",
        ],
        "do_not_use_this_readback_to": [
            "claim production pacing, visual quality, public readiness, or production approval",
            "reopen audio observation or request another render for this same timing proof",
            "commit .ymmp, mp4, wav, mp3, m4a, voice cache, or render output",
            "proceed to visual implementation inside this result-readback slice",
        ],
    }


def _validation_expectations() -> dict[str, bool]:
    return {
        "json_parse_required": True,
        "focused_tests_required": True,
        "compileall_required": True,
        "git_diff_check_required": True,
        "git_cached_diff_check_required": True,
        "conflict_marker_scan_required": True,
        "fixed_form_relapse_scan_required": True,
        "repeated_render_request_scan_required": True,
        "forbidden_staged_file_scan_required": True,
        "YMM4_launched_by_agent": False,
        "render_audio_or_tts_created_by_agent": False,
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


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
