"""Render smoke observation package for the patched newsroom YMM4 project.

This module prepares the milestone-gated manual render smoke packet and the
future result-readback builder. It does not launch YMM4, render, modify .ymmp,
generate TTS/audio, import media, or approve production use.
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
    PATCH_METHOD,
    POST_PATCH_RENDER_SMOKE_SLICE,
    YMMP_TIMING_PATCH_PROBE_ID,
    YMMP_TIMING_PATCH_PROBE_READBACK_ID,
)
from src.pipeline.newsroom_yym4_native_audio_path_proof import (
    DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH,
)


YMMP_TIMING_PATCH_RENDER_SMOKE_SCHEMA_VERSION = (
    "newsroom_ymmp_timing_patch_render_smoke.v1"
)
YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION = (
    "newsroom_ymmp_timing_patch_render_smoke_result_readback.v1"
)
YMMP_TIMING_PATCH_RENDER_SMOKE_ID = (
    "newsroom_ymmp_timing_patch_render_smoke_v1_2026_06_25"
)
YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_BUILDER_ID = (
    "newsroom_ymmp_timing_patch_render_smoke_result_readback_builder_v1"
)
DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_PATH = Path(
    "samples/_probe/newsroom_handoff/ymmp_timing_patch_render_smoke_v1.json"
)
DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YMMP_TIMING_PATCH_RENDER_SMOKE_V1_2026-06-25.md"
)

NEXT_RESULT_READBACK_SLICE = (
    "newsroom-ymmp-timing-patch-render-smoke-result-readback-v1"
)
RENDER_FAILURE_CLASSIFICATION_SLICE = (
    "newsroom-ymmp-timing-patch-render-failure-classification-v1"
)
OPERATOR_UNCERTAINTY_SLICE = (
    "newsroom-ymmp-timing-patch-render-smoke-operator-uncertainty-v1"
)

EXPECTED_DURATION_SEC = 68
EXPECTED_DURATION_TOLERANCE_SEC = 2
EXPECTED_DIALOGUE_ITEM_COUNT = 4

PASS_CLASSIFICATION = "post_patch_render_smoke_pass"
OPEN_FAILURE_CLASSIFICATION = "patched_project_open_failure"
RENDER_FAILURE_CLASSIFICATION = "patched_render_execution_failure"
DURATION_FAILURE_CLASSIFICATION = "patched_duration_mismatch"
DIALOGUE_FAILURE_CLASSIFICATION = "dialogue_preservation_regression"
NATIVE_AUDIO_FAILURE_CLASSIFICATION = "native_audio_preservation_regression"
OPERATOR_UNCERTAIN_CLASSIFICATION = "operator_observation_uncertain"

OBSERVATION_TARGETS: tuple[str, ...] = (
    "patched project opens successfully",
    "render completes",
    "output duration is approximately 68 seconds",
    "four dialogue items remain present",
    "native YMM4/Yukkuri audio remains present",
)
NORMALIZATION_FIELD_NAMES: tuple[str, ...] = (
    "patched_project_opened",
    "render_completed",
    "output_duration_observed_sec",
    "duration_approximately_68_sec",
    "dialogue_items_preserved",
    "dialogue_item_count_observed",
    "native_audio_present",
    "operator_notes",
    "error_message",
    "confidence",
    "unknowns",
    "classification",
    "result",
)


def build_default_newsroom_ymmp_timing_patch_render_smoke(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed render smoke observation package."""
    base = Path(root) if root is not None else Path(".")
    probe = load_json_object(base / DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH)
    probe_readback = load_json_object(
        base / DEFAULT_YMMP_TIMING_PATCH_PROBE_READBACK_PATH
    )
    native_audio_path_proof = load_json_object(
        base / DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH
    )
    audio_observation = load_json_object(
        base / DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
    )
    patched_ymmp_exists = (base / DEFAULT_PATCHED_YMMP_LOCAL_PATH).exists()
    return build_newsroom_ymmp_timing_patch_render_smoke(
        probe,
        probe_readback,
        native_audio_path_proof,
        audio_observation,
        source_probe_path=DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH,
        source_probe_readback_path=DEFAULT_YMMP_TIMING_PATCH_PROBE_READBACK_PATH,
        source_native_audio_path_proof_path=DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH,
        source_audio_observation_path=(
            DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
        ),
        patched_ymmp_path=DEFAULT_PATCHED_YMMP_LOCAL_PATH,
        patched_ymmp_exists=patched_ymmp_exists,
    )


def write_default_newsroom_ymmp_timing_patch_render_smoke_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write the JSON and human-readable render smoke observation artifacts."""
    base = Path(root) if root is not None else Path(".")
    package = build_default_newsroom_ymmp_timing_patch_render_smoke(root=base)
    _write_json(base / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_PATH, package)
    _write_text(
        base / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_DOC_PATH,
        render_newsroom_ymmp_timing_patch_render_smoke_markdown(package),
    )
    return package


def build_newsroom_ymmp_timing_patch_render_smoke(
    probe: dict[str, Any],
    probe_readback: dict[str, Any],
    native_audio_path_proof: dict[str, Any],
    audio_observation: dict[str, Any],
    *,
    source_probe_path: str | Path,
    source_probe_readback_path: str | Path,
    source_native_audio_path_proof_path: str | Path,
    source_audio_observation_path: str | Path,
    patched_ymmp_path: str | Path,
    patched_ymmp_exists: bool,
) -> dict[str, Any]:
    """Build the diagnostic-only manual render smoke package."""
    source_validation = _source_validation(
        probe,
        probe_readback,
        native_audio_path_proof,
        audio_observation,
        patched_ymmp_path=patched_ymmp_path,
        patched_ymmp_exists=patched_ymmp_exists,
    )
    package_status = (
        "ready_for_manual_milestone_render_smoke"
        if not source_validation["errors"]
        else "blocked"
    )

    return {
        "artifact_id": YMMP_TIMING_PATCH_RENDER_SMOKE_ID,
        "smoke_id": YMMP_TIMING_PATCH_RENDER_SMOKE_ID,
        "schema_version": YMMP_TIMING_PATCH_RENDER_SMOKE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "smoke_status": "prepared_not_run",
        "package_status": package_status,
        "identity": {
            "smoke_id": YMMP_TIMING_PATCH_RENDER_SMOKE_ID,
            "source_probe_path": _path_text(source_probe_path),
            "source_probe_id": probe.get("probe_id"),
            "source_probe_readback_path": _path_text(source_probe_readback_path),
            "source_probe_readback_id": probe_readback.get("readback_id"),
            "source_native_audio_path_proof_path": _path_text(
                source_native_audio_path_proof_path
            ),
            "source_native_audio_path_proof_id": native_audio_path_proof.get(
                "proof_id"
            ),
            "source_audio_observation_path": _path_text(
                source_audio_observation_path
            ),
            "source_audio_observation_id": audio_observation.get("readback_id"),
            "patched_ymmp_path": _path_text(patched_ymmp_path),
            "production_status": "diagnostic_only",
            "render_smoke_status": "not_run",
        },
        "source_validation": source_validation,
        "target": _target(probe_readback, patched_ymmp_path, patched_ymmp_exists),
        "milestone_render_gate": _milestone_render_gate(),
        "operator_observation_card": _operator_observation_card(patched_ymmp_path),
        "result_normalization_schema": _result_normalization_schema(),
        "success_failure_classification_matrix": _classification_matrix(),
        "render_readback_builder": _render_readback_builder_contract(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
        "downstream_next_use": _downstream_next_use(),
        "validation_expectations": _validation_expectations(),
    }


def normalize_render_smoke_observation(
    observation: dict[str, Any],
) -> dict[str, Any]:
    """Normalize an agent-read operator observation into the result schema."""
    normalized = {
        "patched_project_opened": _bool_or_unknown(
            observation.get("patched_project_opened")
        ),
        "render_completed": _bool_or_unknown(observation.get("render_completed")),
        "output_duration_observed_sec": _number(
            observation.get("output_duration_observed_sec")
        ),
        "duration_approximately_68_sec": _bool_or_unknown(
            observation.get("duration_approximately_68_sec")
        ),
        "dialogue_items_preserved": _bool_or_unknown(
            observation.get("dialogue_items_preserved")
        ),
        "dialogue_item_count_observed": _intish(
            observation.get("dialogue_item_count_observed")
        ),
        "native_audio_present": _bool_or_unknown(
            observation.get("native_audio_present")
        ),
        "operator_notes": observation.get("operator_notes"),
        "error_message": observation.get("error_message"),
        "confidence": observation.get("confidence", "operator_freeform"),
        "unknowns": observation.get("unknowns", []),
    }

    if normalized["duration_approximately_68_sec"] == "unknown":
        duration = normalized["output_duration_observed_sec"]
        if duration is not None:
            normalized["duration_approximately_68_sec"] = _duration_is_approx_68(
                duration
            )

    dialogue_count = normalized["dialogue_item_count_observed"]
    if dialogue_count is not None and dialogue_count != EXPECTED_DIALOGUE_ITEM_COUNT:
        normalized["dialogue_items_preserved"] = False

    classification = classify_render_smoke_observation(normalized)
    normalized["classification"] = classification["classification"]
    normalized["result"] = classification["result"]
    return normalized


def classify_render_smoke_observation(
    observation: dict[str, Any],
) -> dict[str, Any]:
    """Classify the normalized render smoke observation by the first blocker."""
    opened = _bool_or_unknown(observation.get("patched_project_opened"))
    render_completed = _bool_or_unknown(observation.get("render_completed"))
    duration_ok = _bool_or_unknown(observation.get("duration_approximately_68_sec"))
    dialogue_ok = _bool_or_unknown(observation.get("dialogue_items_preserved"))
    native_audio_ok = _bool_or_unknown(observation.get("native_audio_present"))

    if duration_ok == "unknown":
        duration = _number(observation.get("output_duration_observed_sec"))
        if duration is not None:
            duration_ok = _duration_is_approx_68(duration)

    dialogue_count = _intish(observation.get("dialogue_item_count_observed"))
    if dialogue_count is not None and dialogue_count != EXPECTED_DIALOGUE_ITEM_COUNT:
        dialogue_ok = False

    if opened is False:
        return _classification_result(
            OPEN_FAILURE_CLASSIFICATION,
            "fail",
            "YMM4 did not open the patched diagnostic project.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if opened != True:
        return _uncertain_result("patched project open status was not clear")
    if render_completed is False:
        return _classification_result(
            RENDER_FAILURE_CLASSIFICATION,
            "fail",
            "YMM4 opened the project but render did not complete.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if render_completed != True:
        return _uncertain_result("render completion status was not clear")
    if duration_ok is False:
        return _classification_result(
            DURATION_FAILURE_CLASSIFICATION,
            "fail",
            "Rendered output duration was not approximately 68 seconds.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if duration_ok != True:
        return _uncertain_result("output duration was not clear")
    if dialogue_ok is False:
        return _classification_result(
            DIALOGUE_FAILURE_CLASSIFICATION,
            "fail",
            "Dialogue items were missing or altered after render.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if dialogue_ok != True:
        return _uncertain_result("dialogue preservation was not clear")
    if native_audio_ok is False:
        return _classification_result(
            NATIVE_AUDIO_FAILURE_CLASSIFICATION,
            "fail",
            "Native YMM4/Yukkuri audio was not present after render.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if native_audio_ok != True:
        return _uncertain_result("native audio presence was not clear")
    return _classification_result(
        PASS_CLASSIFICATION,
        "pass",
        "Patched project opened, rendered, stayed about 68 sec, and preserved dialogue plus native audio.",
        NEXT_RESULT_READBACK_SLICE,
    )


def build_newsroom_ymmp_timing_patch_render_smoke_result_readback(
    package: dict[str, Any],
    observation: dict[str, Any],
    *,
    source_package_path: str | Path,
    readback_id: str = "newsroom_ymmp_timing_patch_render_smoke_result_readback_v1",
    observation_source: str = "future_user_freeform",
) -> dict[str, Any]:
    """Build a future result readback from a normalized operator observation."""
    normalized = normalize_render_smoke_observation(observation)
    classification = classify_render_smoke_observation(normalized)
    return {
        "artifact_id": readback_id,
        "readback_id": readback_id,
        "schema_version": YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "observation_source": observation_source,
        "identity": {
            "readback_id": readback_id,
            "source_smoke_package_path": _path_text(source_package_path),
            "source_smoke_package_id": package.get("smoke_id"),
            "target_patched_ymmp_path": _dict(package.get("target")).get(
                "patched_ymmp_path"
            ),
            "production_status": "diagnostic_only",
        },
        "source_validation": _result_builder_source_validation(package),
        "normalized_result": normalized,
        "classification": classification,
        "accepted_scope": _accepted_scope_from_classification(classification),
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
        "next_recommended_slice": classification["next_recommended_slice"],
    }


def render_newsroom_ymmp_timing_patch_render_smoke_markdown(
    package: dict[str, Any],
) -> str:
    """Render a human-readable patched render smoke observation packet."""
    identity = _dict(package.get("identity"))
    validation = _dict(package.get("source_validation"))
    target = _dict(package.get("target"))
    expected = _dict(target.get("expected_project_state"))
    gate = _dict(package.get("milestone_render_gate"))
    card = _dict(package.get("operator_observation_card"))
    schema = _dict(package.get("result_normalization_schema"))
    builder = _dict(package.get("render_readback_builder"))

    lines = [
        "# Newsroom YMM4 Timing Patch Render Smoke v1",
        "",
        f"artifact_id: {package.get('artifact_id')}",
        f"smoke_id: {package.get('smoke_id')}",
        f"schema_version: {package.get('schema_version')}",
        f"review_status: {package.get('review_status')}",
        f"production_status: {package.get('production_status')}",
        f"smoke_status: {package.get('smoke_status')}",
        f"package_status: {package.get('package_status')}",
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

    lines.extend(["", "## Target", ""])
    lines.append(f"- patched_ymmp_path: {target.get('patched_ymmp_path')}")
    lines.append(
        f"- patched_ymmp_path_status: {target.get('patched_ymmp_path_status')}"
    )
    lines.append(f"- git_tracking_policy: {target.get('git_tracking_policy')}")
    lines.append(f"- expected_duration_sec: {expected.get('total_duration_sec')}")
    lines.append(f"- expected_total_frames: {expected.get('total_frames')}")
    lines.append(
        f"- expected_dialogue_item_count: {expected.get('dialogue_item_count')}"
    )
    lines.append(f"- expected_item_frames: {_display(expected.get('item_frames'))}")
    lines.append(
        f"- expected_item_lengths: {_display(expected.get('item_lengths'))}"
    )

    lines.extend(["", "## Milestone Render Gate", ""])
    for key, value in gate.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Operator Observation Card",
            "",
            f"- status: {card.get('status')}",
            f"- target: {card.get('target')}",
            f"- patched_ymmp_path: {card.get('patched_ymmp_path')}",
            f"- why: {card.get('why')}",
            f"- action: {card.get('action')}",
            f"- answer_style: {card.get('answer_style')}",
            f"- answer_hint: {card.get('answer_hint')}",
            "- look_for:",
        ]
    )
    for item in card.get("look_for", []):
        lines.append(f"  - {item}")
    lines.append("- not_needed:")
    for item in card.get("not_needed", []):
        lines.append(f"  - {item}")

    lines.extend(
        [
            "",
            "## Result Normalization Schema",
            "",
            f"- schema_owner: {schema.get('schema_owner')}",
            f"- user_must_fill_schema: {_display(schema.get('user_must_fill_schema'))}",
            f"- duration_tolerance_sec: {schema.get('duration_tolerance_sec')}",
            "",
            "| field | type | normalization |",
            "|---|---|---|",
        ]
    )
    for row in schema.get("fields", []):
        lines.append(
            "| "
            f"{row.get('field')} | "
            f"{row.get('type')} | "
            f"{row.get('normalization')} |"
        )

    lines.extend(
        [
            "",
            "## Success / Failure Classification Matrix",
            "",
            "| classification | trigger | result | next slice |",
            "|---|---|---|---|",
        ]
    )
    for row in package.get("success_failure_classification_matrix", []):
        lines.append(
            "| "
            f"{row.get('classification')} | "
            f"{row.get('trigger')} | "
            f"{row.get('result')} | "
            f"{row.get('next_recommended_slice')} |"
        )

    lines.extend(["", "## Render Readback Builder", ""])
    for key, value in builder.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Boundaries", ""])
    for key, value in _dict(package.get("boundaries")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This packet prepares the next manual milestone render smoke only. "
            "The agent did not launch YMM4, render, modify the patched `.ymmp`, "
            "generate or replace audio, stage media, or change the timing "
            "strategy. A later freeform observation should be normalized by the "
            "builder in this module before any production-readiness claim.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    probe: dict[str, Any],
    probe_readback: dict[str, Any],
    native_audio_path_proof: dict[str, Any],
    audio_observation: dict[str, Any],
    *,
    patched_ymmp_path: str | Path,
    patched_ymmp_exists: bool,
) -> dict[str, Any]:
    errors: list[str] = []
    structural = _dict(probe_readback.get("structural_result"))
    timing = _dict(probe_readback.get("before_after_timing"))
    preservation = _dict(probe_readback.get("field_preservation_readback"))
    audio_voice = _dict(probe_readback.get("audio_voice_boundary"))
    render_gate = _dict(probe_readback.get("render_gate"))
    audio_normalized = _dict(audio_observation.get("normalized_audio_observation"))

    if probe.get("probe_id") != YMMP_TIMING_PATCH_PROBE_ID:
        errors.append("SOURCE_PROBE_ID_MISMATCH")
    if probe_readback.get("readback_id") != YMMP_TIMING_PATCH_PROBE_READBACK_ID:
        errors.append("SOURCE_PROBE_READBACK_ID_MISMATCH")
    if probe_readback.get("readback_status") != "structural_pass":
        errors.append("TIMING_PATCH_READBACK_NOT_STRUCTURAL_PASS")
    if structural.get("target_68_sec_reached_structurally") is not True:
        errors.append("TARGET_68_SEC_NOT_STRUCTURALLY_REACHED")
    if structural.get("patched_total_frames") != 4080:
        errors.append("PATCHED_TOTAL_FRAMES_NOT_4080")
    if timing.get("patched_total_sec") != 68.0:
        errors.append("PATCHED_TOTAL_SEC_NOT_68")
    if timing.get("patched_item_end_frames") != [720, 1440, 2760, 4080]:
        errors.append("PATCHED_DIALOGUE_END_FRAMES_MISMATCH")
    if preservation.get("all_required_fields_preserved") is not True:
        errors.append("VOICE_FIELDS_NOT_PRESERVED")
    if audio_voice.get("native_voice_path_preserved") is not True:
        errors.append("NATIVE_VOICE_PATH_NOT_PRESERVED")
    if native_audio_path_proof.get("proof_status") != "passed_with_unknowns":
        errors.append("NATIVE_AUDIO_PATH_PROOF_NOT_AVAILABLE")
    if audio_normalized.get("diagnostic_audio_path_accepted") is not True:
        errors.append("DIAGNOSTIC_AUDIO_PATH_NOT_ACCEPTED")
    if render_gate.get("next_recommended_slice") != POST_PATCH_RENDER_SMOKE_SLICE:
        errors.append("RENDER_GATE_NEXT_SLICE_MISMATCH")
    if render_gate.get("render_performed_in_this_slice") is not False:
        errors.append("RENDER_ALREADY_PERFORMED_IN_PATCH_PROBE")
    if _path_text(patched_ymmp_path) != _dict(probe_readback.get("identity")).get(
        "patched_ymmp_path"
    ):
        errors.append("PATCHED_YMMP_TARGET_PATH_MISMATCH")
    if not patched_ymmp_exists:
        errors.append("PATCHED_YMMP_TARGET_NOT_FOUND")

    return {
        "status": "passed" if not errors else "blocked",
        "probe_id": probe.get("probe_id"),
        "probe_readback_id": probe_readback.get("readback_id"),
        "patch_method": PATCH_METHOD,
        "patched_ymmp_path": _path_text(patched_ymmp_path),
        "patched_ymmp_found_at_generation": patched_ymmp_exists,
        "patched_total_sec": timing.get("patched_total_sec"),
        "patched_total_frames": structural.get("patched_total_frames"),
        "patched_dialogue_item_count": structural.get("patched_voice_item_count"),
        "native_voice_path_preserved": audio_voice.get("native_voice_path_preserved"),
        "external_TTS_introduced": audio_voice.get("external_TTS_introduced"),
        "render_already_performed": render_gate.get("render_performed_in_this_slice"),
        "errors": errors,
    }


def _target(
    probe_readback: dict[str, Any],
    patched_ymmp_path: str | Path,
    patched_ymmp_exists: bool,
) -> dict[str, Any]:
    timing = _dict(probe_readback.get("before_after_timing"))
    structural = _dict(probe_readback.get("structural_result"))
    patched_items = timing.get("patched_item_timings", [])
    return {
        "patched_ymmp_path": _path_text(patched_ymmp_path),
        "patched_ymmp_path_status": (
            "discoverable_local_file_at_generation_time"
            if patched_ymmp_exists
            else "recorded_but_not_found_at_generation_time"
        ),
        "git_tracking_policy": "ignored_under_tmp_do_not_stage_or_commit",
        "ymmp_file_newly_modified_in_this_slice": False,
        "expected_project_state": {
            "fps": timing.get("fps"),
            "total_frames": structural.get("patched_total_frames"),
            "total_duration_sec": structural.get("patched_total_sec"),
            "dialogue_item_count": structural.get("patched_voice_item_count"),
            "item_frames": structural.get("patched_frames"),
            "item_lengths": structural.get("patched_lengths"),
            "item_end_frames": structural.get("patched_end_frames"),
            "text_summaries": [
                row.get("text") for row in patched_items if isinstance(row, dict)
            ],
            "native_audio_expected_from_preserved_yym4_fields": True,
        },
        "render_objective": {
            "confirm_patched_project_opens": True,
            "confirm_render_completes": True,
            "confirm_output_duration_about_68_sec": True,
            "confirm_dialogue_items_preserved": True,
            "confirm_native_audio_present": True,
            "production": False,
            "public_video": False,
        },
    }


def _milestone_render_gate() -> dict[str, Any]:
    return {
        "gate_type": "milestone_gated_verification",
        "milestone": POST_PATCH_RENDER_SMOKE_SLICE,
        "render_performed_in_this_slice": False,
        "YMM4_launched_by_agent": False,
        "manual_render_allowed_next": True,
        "manual_render_count": 1,
        "render_reason": "structural timing patch reached 68 sec and needs real YMM4 open/render confirmation",
        "timing_strategy_change_allowed": False,
        "external_TTS_allowed": False,
        "render_output_commit_allowed": False,
        "ymmp_commit_allowed": False,
    }


def _operator_observation_card(patched_ymmp_path: str | Path) -> dict[str, Any]:
    return {
        "status": "required_next_milestone",
        "target": "patched diagnostic .ymmp render smoke",
        "patched_ymmp_path": _path_text(patched_ymmp_path),
        "why": "Confirm YMM4 accepts the 68 sec structural patch on the real open/render surface.",
        "action": "Open the patched diagnostic .ymmp in YMM4 and render once without changing timing, voice, or media.",
        "look_for": list(OBSERVATION_TARGETS),
        "answer_style": "freeform",
        "answer_hint": "opened and rendered; about 68 sec; four dialogue items and native voice remained",
        "not_needed": [
            "fixed form",
            "detailed sound quality review",
            "production quality judgement",
            "screenshots unless useful",
            "committing .ymmp or media output",
        ],
    }


def _result_normalization_schema() -> dict[str, Any]:
    return {
        "schema_id": YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_BUILDER_ID,
        "schema_version": YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION,
        "schema_owner": "Agent",
        "user_must_fill_schema": False,
        "normalization_source": "future freeform operator observation",
        "duration_tolerance_sec": EXPECTED_DURATION_TOLERANCE_SEC,
        "fields": [
            {
                "field": "patched_project_opened",
                "type": "boolean_or_unknown",
                "normalization": "true only when the patched .ymmp opens in YMM4",
            },
            {
                "field": "render_completed",
                "type": "boolean_or_unknown",
                "normalization": "true only when YMM4 export finishes",
            },
            {
                "field": "output_duration_observed_sec",
                "type": "number_or_null",
                "normalization": "observed media duration in seconds when known",
            },
            {
                "field": "duration_approximately_68_sec",
                "type": "boolean_or_unknown",
                "normalization": "true when duration is within the configured 68 sec tolerance",
            },
            {
                "field": "dialogue_items_preserved",
                "type": "boolean_or_unknown",
                "normalization": "true when the four expected dialogue items remain present",
            },
            {
                "field": "dialogue_item_count_observed",
                "type": "integer_or_null",
                "normalization": "observed dialogue item count if the operator reports it",
            },
            {
                "field": "native_audio_present",
                "type": "boolean_or_unknown",
                "normalization": "true when native YMM4/Yukkuri audio is still audible",
            },
            {
                "field": "operator_notes",
                "type": "string_or_null",
                "normalization": "freeform notes retained without making the user fill a form",
            },
            {
                "field": "error_message",
                "type": "string_or_null",
                "normalization": "YMM4 or export error text when reported",
            },
            {
                "field": "confidence",
                "type": "string",
                "normalization": "agent confidence in the normalized observation",
            },
            {
                "field": "unknowns",
                "type": "array",
                "normalization": "required targets the observation did not settle",
            },
            {
                "field": "classification",
                "type": "enum",
                "normalization": "classification from the success/failure matrix",
            },
            {
                "field": "result",
                "type": "enum",
                "normalization": "pass, fail, or blocked_by_operator_uncertainty",
            },
        ],
    }


def _classification_matrix() -> list[dict[str, Any]]:
    return [
        {
            "classification": PASS_CLASSIFICATION,
            "trigger": "all five observation targets are true",
            "result": "pass",
            "next_recommended_slice": NEXT_RESULT_READBACK_SLICE,
        },
        {
            "classification": OPEN_FAILURE_CLASSIFICATION,
            "trigger": "patched project does not open",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": RENDER_FAILURE_CLASSIFICATION,
            "trigger": "project opens but render does not complete",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": DURATION_FAILURE_CLASSIFICATION,
            "trigger": "render completes but output is not approximately 68 sec",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": DIALOGUE_FAILURE_CLASSIFICATION,
            "trigger": "render completes but dialogue items are missing or altered",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": NATIVE_AUDIO_FAILURE_CLASSIFICATION,
            "trigger": "render completes and dialogue remains, but native audio is absent",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": OPERATOR_UNCERTAIN_CLASSIFICATION,
            "trigger": "one or more required observation targets remain unknown",
            "result": "blocked_by_operator_uncertainty",
            "next_recommended_slice": OPERATOR_UNCERTAINTY_SLICE,
        },
    ]


def _render_readback_builder_contract() -> dict[str, Any]:
    return {
        "builder_id": YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_BUILDER_ID,
        "module": "src.pipeline.newsroom_ymmp_timing_patch_render_smoke",
        "function": "build_newsroom_ymmp_timing_patch_render_smoke_result_readback",
        "input_package": _path_text(DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_PATH),
        "input_observation": "future freeform operator observation normalized by Agent",
        "output_schema_version": YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION,
        "writes_artifact_in_this_slice": False,
        "requires_committed_media": False,
        "requires_committed_ymmp": False,
        "classification_function": "classify_render_smoke_observation",
    }


def _human_burden_hygiene() -> dict[str, Any]:
    return {
        "user_input": "freeform",
        "template_required": False,
        "schema_owner": "Agent",
        "required_observation_target_count": len(OBSERVATION_TARGETS),
        "observation_targets_are_minimal": True,
        "screenshot_optional": True,
        "negative_confirmations_required_from_user": False,
        "fixed_form_result_template": False,
        "user_side_work_this_agent_slice": "none",
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
        "render_smoke_result": False,
        "neutral_68_sec_video_acceptance": False,
    }


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "external_TTS_introduced": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "ymmp_created_or_modified_by_agent": False,
        "ymmp_or_media_staged_or_committed": False,
        "render_output_staged_or_committed": False,
        "timing_strategy_changed": False,
        "production_approval": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


def _downstream_next_use() -> dict[str, list[str]]:
    return {
        "use_this_package_to": [
            "guide exactly one manual render smoke of the patched diagnostic .ymmp",
            "normalize the later freeform observation into a repo readback",
            "classify open, render, duration, dialogue, or native-audio failure",
        ],
        "do_not_use_this_package_to": [
            "change timing strategy",
            "launch YMM4 or render from the agent",
            "commit .ymmp, media, render output, or voice cache",
            "claim production or public video readiness",
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
        "forbidden_media_staging_scan_required": True,
        "YMM4_launched_by_agent": False,
        "render_created_by_agent": False,
    }


def _result_builder_source_validation(package: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if package.get("smoke_id") != YMMP_TIMING_PATCH_RENDER_SMOKE_ID:
        errors.append("SOURCE_PACKAGE_ID_MISMATCH")
    if package.get("package_status") != "ready_for_manual_milestone_render_smoke":
        errors.append("SOURCE_PACKAGE_NOT_READY")
    if package.get("smoke_status") != "prepared_not_run":
        errors.append("SOURCE_PACKAGE_SMOKE_STATUS_NOT_PREPARED")
    return {
        "status": "passed" if not errors else "blocked",
        "source_package_id": package.get("smoke_id"),
        "source_package_status": package.get("package_status"),
        "errors": errors,
    }


def _accepted_scope_from_classification(
    classification: dict[str, Any],
) -> dict[str, bool]:
    passed = classification.get("classification") == PASS_CLASSIFICATION
    return {
        "patched_project_opened": passed,
        "render_completed": passed,
        "diagnostic_output_about_68_sec": passed,
        "dialogue_items_preserved": passed,
        "native_audio_present": passed,
        "production_ready": False,
        "public_video_ready": False,
    }


def _classification_result(
    classification: str,
    result: str,
    reason: str,
    next_slice: str,
) -> dict[str, Any]:
    return {
        "classification": classification,
        "result": result,
        "reason": reason,
        "next_recommended_slice": next_slice,
    }


def _uncertain_result(reason: str) -> dict[str, Any]:
    return _classification_result(
        OPERATOR_UNCERTAIN_CLASSIFICATION,
        "blocked_by_operator_uncertainty",
        reason,
        OPERATOR_UNCERTAINTY_SLICE,
    )


def _duration_is_approx_68(duration_sec: float) -> bool:
    return abs(duration_sec - EXPECTED_DURATION_SEC) <= EXPECTED_DURATION_TOLERANCE_SEC


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


def _bool_or_unknown(value: Any) -> bool | str:
    if isinstance(value, bool):
        return value
    return "unknown"


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _intish(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
