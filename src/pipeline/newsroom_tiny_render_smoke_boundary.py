"""Tiny render smoke boundary for the diagnostic newsroom YMM4 lane.

This module prepares a future manual operator packet for one tiny diagnostic
render smoke. It records boundary and observation policy only: it does not
launch YMM4, render, patch or commit .ymmp, generate TTS/audio, import real
media, fetch external sources, or approve production use.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_diagnostic_ymmp_manual_result import (
    DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH,
)
from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
    DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_yym4_timing_gap_strategy import (
    DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH,
    RECOMMENDED_DEFAULT,
)


TINY_RENDER_SMOKE_BOUNDARY_SCHEMA_VERSION = (
    "newsroom_tiny_render_smoke_boundary.v1"
)
TINY_RENDER_SMOKE_BOUNDARY_ID = (
    "newsroom_tiny_render_smoke_boundary_v1_2026_06_23"
)
DEFAULT_TINY_RENDER_SMOKE_BOUNDARY_PATH = Path(
    "samples/_probe/newsroom_handoff/tiny_render_smoke_boundary_v1.json"
)
DEFAULT_TINY_RENDER_SMOKE_BOUNDARY_DOC_PATH = Path(
    "docs/verification/NEWSROOM_TINY_RENDER_SMOKE_BOUNDARY_V1_2026-06-23.md"
)

SMOKE_SUCCESS_READBACK_SLICE = "newsroom-tiny-render-smoke-result-readback-v1"
SMOKE_FAILURE_CLASSIFICATION_SLICE = (
    "newsroom-yym4-render-failure-classification-v1"
)
SMOKE_OPERATOR_POLISH_SLICE = (
    "newsroom-yym4-render-operator-instruction-polish-v1"
)
TIMING_PATCH_STRATEGY_SLICE = "newsroom-ymmp-timing-patch-strategy-v1"
ANSWER_HINT = (
    "render\u3067\u304d\u307e\u3057\u305f\u30024\u884c\u304c"
    "\u51fa\u3066\u3001\u5c3a\u306f\u77ed\u3044\u307e\u307e"
    "\u3067\u3059\u3002"
)


def build_default_newsroom_tiny_render_smoke_boundary(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed tiny render smoke boundary from source readbacks."""
    base = Path(root) if root is not None else Path(".")
    timing_strategy = load_json_object(base / DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH)
    structure_readback = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
    )
    manual_result = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH
    )
    source_ymmp_path = _dict(structure_readback.get("identity")).get(
        "source_ymmp_path"
    )
    source_ymmp_exists = (
        (base / source_ymmp_path).exists()
        if isinstance(source_ymmp_path, str)
        else False
    )
    return build_newsroom_tiny_render_smoke_boundary(
        timing_strategy,
        structure_readback,
        manual_result,
        source_timing_strategy_path=DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH,
        source_ymmp_structure_readback_path=(
            DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
        ),
        source_manual_result_readback_path=(
            DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH
        ),
        source_ymmp_exists=source_ymmp_exists,
    )


def build_newsroom_tiny_render_smoke_boundary(
    timing_strategy: dict[str, Any],
    structure_readback: dict[str, Any],
    manual_result: dict[str, Any],
    *,
    source_timing_strategy_path: str | Path,
    source_ymmp_structure_readback_path: str | Path,
    source_manual_result_readback_path: str | Path,
    source_ymmp_exists: bool,
) -> dict[str, Any]:
    """Build a diagnostic-only future manual render smoke boundary."""
    source_validation = _source_validation(
        timing_strategy,
        structure_readback,
        manual_result,
    )
    target = _target(structure_readback, source_ymmp_exists=source_ymmp_exists)
    allowed = _allowed_future_manual_action()
    forbidden = _forbidden_actions()
    operator_card = _operator_observation_card(target)
    timing_policy = _timing_policy(timing_strategy)
    not_accepted_scope = _not_accepted_scope()
    boundary_assertions = _boundary_assertions()
    render_smoke_status = (
        "ready_for_future_manual_smoke"
        if not source_validation["errors"]
        else "blocked"
    )

    return {
        "artifact_id": TINY_RENDER_SMOKE_BOUNDARY_ID,
        "boundary_id": TINY_RENDER_SMOKE_BOUNDARY_ID,
        "schema_version": TINY_RENDER_SMOKE_BOUNDARY_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "render_smoke_status": "not_run",
        "boundary_status": render_smoke_status,
        "identity": {
            "boundary_id": TINY_RENDER_SMOKE_BOUNDARY_ID,
            "source_timing_strategy_path": _path_text(
                source_timing_strategy_path
            ),
            "source_timing_strategy_id": timing_strategy.get("strategy_id"),
            "source_ymmp_structure_readback_path": _path_text(
                source_ymmp_structure_readback_path
            ),
            "source_ymmp_structure_readback_id": structure_readback.get(
                "readback_id"
            ),
            "source_manual_result_readback_path": _path_text(
                source_manual_result_readback_path
            ),
            "source_manual_result_id": manual_result.get("result_id"),
            "production_status": "diagnostic_only",
            "render_smoke_status": "not_run",
        },
        "source_validation": source_validation,
        "target": target,
        "allowed_future_manual_action": allowed,
        "forbidden_actions": forbidden,
        "operator_observation_card": operator_card,
        "agent_normalization_plan": _agent_normalization_plan(),
        "timing_policy": timing_policy,
        "next_recommended_slices": {
            "if_manual_render_succeeds": SMOKE_SUCCESS_READBACK_SLICE,
            "if_render_fails": SMOKE_FAILURE_CLASSIFICATION_SLICE,
            "if_operator_is_uncertain": SMOKE_OPERATOR_POLISH_SLICE,
            "next_timing_axis_after_smoke": TIMING_PATCH_STRATEGY_SLICE,
        },
        "review_memory": {
            "review_source": "newsroom_yym4_timing_gap_strategy_v1",
            "prior_user_review_count": {
                "manual_import_behavior": 1,
                "bound_speaker_behavior": 1,
                "diagnostic_ymmp_manual_observation": 1,
                "ymmp_structure_readback": 1,
                "timing_gap_strategy": 1,
                "tiny_render_smoke_boundary": 0,
            },
            "prior_evidence_reused": [
                "diagnostic .ymmp save observation",
                "diagnostic .ymmp structure readback",
                "timing gap strategy accepted for first tiny render smoke",
            ],
            "next_nonredundant_axis": [
                SMOKE_SUCCESS_READBACK_SLICE,
                SMOKE_FAILURE_CLASSIFICATION_SLICE,
                TIMING_PATCH_STRATEGY_SLICE,
            ],
            "not_accepted_scope": not_accepted_scope,
            "repeated_general_review_allowed": False,
            "input_mode": "freeform",
        },
        "human_burden_hygiene": {
            "user_input": "freeform",
            "template_required": False,
            "schema_owner": "Agent",
            "max_required_points": len(operator_card["look_for"]),
            "screenshot_optional": True,
            "negative_confirmations_required_from_user": False,
            "fixed_form_result_template": False,
            "user_side_work_this_agent_slice": "none",
        },
        "not_accepted_scope": not_accepted_scope,
        "downstream_next_use": {
            "use_this_boundary_to": [
                "guide a future manual tiny diagnostic render smoke",
                "normalize a later freeform render result readback",
                "keep timing patch strategy separate until after smoke evidence",
            ],
            "do_not_use_this_boundary_to": [
                "launch YMM4 from the agent",
                "create render output in this slice",
                "commit .ymmp or render output",
                "claim production, TTS, visual layout, or public video readiness",
            ],
        },
        "boundary_assertions": boundary_assertions,
    }


def render_newsroom_tiny_render_smoke_boundary_markdown(
    boundary: dict[str, Any],
) -> str:
    """Render a human-readable tiny render smoke boundary/operator packet."""
    identity = _dict(boundary.get("identity"))
    validation = _dict(boundary.get("source_validation"))
    target = _dict(boundary.get("target"))
    expected = _dict(target.get("expected_project_state"))
    objective = _dict(target.get("render_objective"))
    allowed = _dict(boundary.get("allowed_future_manual_action"))
    forbidden = _dict(boundary.get("forbidden_actions"))
    card = _dict(boundary.get("operator_observation_card"))
    normalization = _dict(boundary.get("agent_normalization_plan"))
    timing = _dict(boundary.get("timing_policy"))
    hygiene = _dict(boundary.get("human_burden_hygiene"))
    next_slices = _dict(boundary.get("next_recommended_slices"))
    review = _dict(boundary.get("review_memory"))

    lines = [
        "# Newsroom Tiny Render Smoke Boundary v1",
        "",
        f"artifact_id: {boundary.get('artifact_id')}",
        f"boundary_id: {boundary.get('boundary_id')}",
        f"schema_version: {boundary.get('schema_version')}",
        f"review_status: {boundary.get('review_status')}",
        f"production_status: {boundary.get('production_status')}",
        f"render_smoke_status: {boundary.get('render_smoke_status')}",
        f"boundary_status: {boundary.get('boundary_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        f"- source_timing_strategy_path: {identity.get('source_timing_strategy_path')}",
        f"- source_timing_strategy_id: {identity.get('source_timing_strategy_id')}",
        (
            "- source_ymmp_structure_readback_path: "
            f"{identity.get('source_ymmp_structure_readback_path')}"
        ),
        (
            "- source_ymmp_structure_readback_id: "
            f"{identity.get('source_ymmp_structure_readback_id')}"
        ),
        (
            "- source_manual_result_readback_path: "
            f"{identity.get('source_manual_result_readback_path')}"
        ),
        f"- source_manual_result_id: {identity.get('source_manual_result_id')}",
        "",
        "## Source Validation",
        "",
        f"- status: {validation.get('status')}",
        f"- errors: {_display(validation.get('errors'))}",
        f"- canonical_speaker_value: {validation.get('canonical_speaker_value')}",
        (
            "- recommended_timing_default: "
            f"{validation.get('recommended_timing_default')}"
        ),
        "",
        "## Target",
        "",
        f"- diagnostic_ymmp_path: {target.get('diagnostic_ymmp_path')}",
        f"- diagnostic_ymmp_path_status: {target.get('diagnostic_ymmp_path_status')}",
        f"- git_tracking_policy: {target.get('git_tracking_policy')}",
        f"- dialogue_item_count: {expected.get('dialogue_item_count')}",
        f"- speaker: {expected.get('speaker')}",
        f"- natural_short_duration_sec: {expected.get('natural_short_duration_sec')}",
        f"- item_frames: {_display(expected.get('item_frames'))}",
        f"- item_lengths: {_display(expected.get('item_lengths'))}",
        "",
        "## Render Objective",
        "",
    ]
    for key, value in objective.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Allowed Future Manual Action", ""])
    for key, value in allowed.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Forbidden Actions", ""])
    for key, value in forbidden.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Operator Observation Card",
            "",
            f"- status: {card.get('status')}",
            f"- target: {card.get('target')}",
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
            "## Agent Normalization Plan",
            "",
            f"- schema_owner: {normalization.get('schema_owner')}",
            (
                "- exposed_to_user_as_form: "
                f"{_display(normalization.get('exposed_to_user_as_form'))}"
            ),
            "- fields:",
        ]
    )
    for item in normalization.get("fields", []):
        lines.append(f"  - {item}")

    lines.extend(["", "## Timing Policy", ""])
    for key, value in timing.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Next Recommended Slices", ""])
    for key, value in next_slices.items():
        lines.append(f"- {key}: {value}")

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
            "This packet only prepares a future manual tiny render smoke. The "
            "agent did not launch YMM4, render, patch or commit `.ymmp`, "
            "generate TTS/audio, import real media, approve production, or "
            "prepare a public video.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    timing_strategy: dict[str, Any],
    structure_readback: dict[str, Any],
    manual_result: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    timing_validation = _dict(timing_strategy.get("source_validation"))
    recommended = _dict(timing_strategy.get("recommended_default"))
    timing_facts = _dict(timing_strategy.get("timing_facts"))
    parse_status = _dict(structure_readback.get("parse_status"))
    dialogue = _dict(structure_readback.get("dialogue_structure"))
    timing_structure = _dict(structure_readback.get("timing_structure"))
    manual_normalized = _dict(manual_result.get("normalized_result"))

    if timing_strategy.get("strategy_status") != "accepted_for_next_tiny_render_smoke":
        errors.append("TIMING_STRATEGY_NOT_ACCEPTED_FOR_SMOKE")
    if recommended.get("choice") != RECOMMENDED_DEFAULT:
        errors.append("TIMING_RECOMMENDATION_NOT_HYBRID")
    if timing_validation.get("status") != "passed":
        errors.append("TIMING_STRATEGY_SOURCE_VALIDATION_NOT_PASSED")
    if timing_facts.get("timing_patch_applied") is not False:
        errors.append("TIMING_PATCH_ALREADY_APPLIED")
    if parse_status.get("parse_status") != "parsed":
        errors.append("STRUCTURE_READBACK_NOT_PARSED")
    if dialogue.get("dialogue_item_count") != 4:
        errors.append("DIALOGUE_ITEM_COUNT_NOT_4")
    if dialogue.get("canonical_speaker_value") != CANONICAL_UI_OBSERVED_SPEAKER:
        errors.append("CANONICAL_SPEAKER_MISMATCH")
    if timing_structure.get("observed_project_duration_frames") != 509:
        errors.append("YMMP_TOTAL_FRAMES_NOT_509")
    if manual_result.get("result") != "pass":
        errors.append("MANUAL_RESULT_NOT_PASS")
    if manual_normalized.get("render_created") is not False:
        errors.append("PRIOR_MANUAL_RESULT_ALREADY_RENDERED")

    return {
        "status": "passed" if not errors else "blocked",
        "timing_strategy_id": timing_strategy.get("strategy_id"),
        "structure_readback_id": structure_readback.get("readback_id"),
        "manual_result_id": manual_result.get("result_id"),
        "recommended_timing_default": recommended.get("choice"),
        "canonical_speaker_value": dialogue.get("canonical_speaker_value"),
        "canonical_speaker_unicode_escape": dialogue.get(
            "canonical_speaker_unicode_escape"
        ),
        "dialogue_item_count": dialogue.get("dialogue_item_count"),
        "ymmp_total_frames": timing_structure.get("observed_project_duration_frames"),
        "ymmp_total_duration_sec": timing_structure.get(
            "observed_project_duration_sec"
        ),
        "errors": errors,
    }


def _target(
    structure_readback: dict[str, Any],
    *,
    source_ymmp_exists: bool,
) -> dict[str, Any]:
    identity = _dict(structure_readback.get("identity"))
    dialogue = _dict(structure_readback.get("dialogue_structure"))
    timing = _dict(structure_readback.get("timing_structure"))
    source_ymmp_path = identity.get("source_ymmp_path")
    return {
        "diagnostic_ymmp_path": source_ymmp_path,
        "diagnostic_ymmp_path_status": (
            "discoverable_local_file_at_generation_time"
            if source_ymmp_exists
            else "recorded_but_not_found_at_generation_time"
        ),
        "git_tracking_policy": "ignored_under_tmp_do_not_stage_or_commit",
        "ymmp_file_newly_parsed_in_this_slice": False,
        "expected_project_state": {
            "dialogue_item_count": dialogue.get("dialogue_item_count"),
            "speaker": dialogue.get("canonical_speaker_value"),
            "speaker_unicode_escape": dialogue.get(
                "canonical_speaker_unicode_escape"
            ),
            "text_summaries": dialogue.get("text_summaries", []),
            "fps": _whole_number(timing.get("fps")),
            "total_frames": _whole_number(
                timing.get("observed_project_duration_frames")
            ),
            "natural_short_duration_sec": timing.get("observed_project_duration_sec"),
            "item_frames": [
                _whole_number(item.get("frame"))
                for item in timing.get("item_timings", [])
                if isinstance(item, dict)
            ],
            "item_lengths": [
                _whole_number(item.get("length_frames"))
                for item in timing.get("item_timings", [])
                if isinstance(item, dict)
            ],
            "voice_cache_present_but_not_tts_readiness": True,
        },
        "render_objective": {
            "confirm_yym4_can_export_tiny_diagnostic_video": True,
            "production": False,
            "timing_patch_proof": False,
            "visual_layout_proof": False,
            "public_video": False,
        },
    }


def _allowed_future_manual_action() -> dict[str, Any]:
    return {
        "user_or_operator_may_open_yym4_manually_later": True,
        "user_or_operator_may_open_diagnostic_ymmp": True,
        "user_or_operator_may_perform_one_tiny_render_smoke_if_comfortable": True,
        "output_treated_as_diagnostic_only": True,
        "render_output_commit_policy": (
            "do_not_commit_render_output_until_later_result_readback_slice"
        ),
        "timing_changes_allowed_in_first_smoke": False,
        "agent_action_required_now": False,
    }


def _forbidden_actions() -> dict[str, bool]:
    return {
        "agent_yym4_launch": True,
        "agent_render": True,
        "production_render": True,
        "real_media_import": True,
        "timing_patch_during_first_smoke": True,
        "tts_configuration_changes_beyond_yym4_natural_existing_state": True,
        "public_video_claim": True,
        "commit_render_output_without_explicit_later_gate": True,
        "commit_ymmp_without_explicit_later_gate": True,
        "external_fetch": True,
        "dashboard_governance_freshness_change": True,
    }


def _operator_observation_card(target: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "required_later",
        "target": "diagnostic .ymmp tiny render smoke",
        "diagnostic_ymmp_path": target.get("diagnostic_ymmp_path"),
        "why": (
            "Confirm the saved four-line YMM4 project can render a tiny "
            "diagnostic video."
        ),
        "action": (
            "Open the diagnostic .ymmp manually and, if comfortable, export one "
            "tiny render smoke without changing timing."
        ),
        "look_for": [
            "render completes or fails",
            "output plays and contains the four dialogue lines",
            "duration remains short/natural rather than 68 sec",
        ],
        "answer_style": "freeform",
        "answer_hint": ANSWER_HINT,
        "not_needed": [
            "fixed form",
            "production quality review",
            "real media",
            "timing patch",
            "screenshot unless useful",
        ],
    }


def _agent_normalization_plan() -> dict[str, Any]:
    return {
        "schema_owner": "Agent",
        "exposed_to_user_as_form": False,
        "fields": [
            "result",
            "render_completed",
            "output_path_if_known",
            "output_duration_observed",
            "four_lines_visible_or_audible",
            "timing_observation",
            "error_message",
            "confidence",
            "unknowns",
        ],
        "user_must_fill_schema": False,
        "normalization_source": "future freeform operator observation",
    }


def _timing_policy(timing_strategy: dict[str, Any]) -> dict[str, Any]:
    facts = _dict(timing_strategy.get("timing_facts"))
    return {
        "first_smoke_timing_mode": "YMM4 natural duration",
        "natural_duration_sec": facts.get("ymmp_total_duration_sec"),
        "neutral_timeline_total_sec": facts.get("neutral_timeline_total_sec"),
        "neutral_68_sec_timing_patch": "deferred",
        "timing_patch_applied": False,
        "next_timing_axis_after_smoke": TIMING_PATCH_STRATEGY_SLICE,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_ymmp": False,
        "timing_patch": False,
        "render_readiness_beyond_smoke_boundary": False,
        "TTS_readiness": False,
        "public_video_readiness": False,
        "visual_layout_import": False,
        "production_approval": False,
    }


def _boundary_assertions() -> dict[str, bool]:
    return {
        "diagnostic_only": True,
        "agent_launched_yym4": False,
        "agent_render_created": False,
        "agent_created_or_modified_ymmp": False,
        "ymmp_staged_or_committed": False,
        "render_output_staged_or_committed": False,
        "TTS_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "production_approval": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


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
