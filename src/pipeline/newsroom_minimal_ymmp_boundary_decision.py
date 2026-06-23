"""Minimal .ymmp boundary decision for the diagnostic newsroom lane.

This module turns the bound-speaker CSV readiness readback into a narrow
decision about what may happen before any .ymmp probe. It does not create
.ymmp files, launch YMM4, render, generate TTS/audio, import real media, fetch
external sources, or approve production use.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_yym4_bound_speaker_import_readiness import (
    DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH,
)
from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    EXPECTED_MANUAL_IMPORT_ROW_COUNT,
    TARGET_SURFACE_COLUMNS,
    read_tiny_script_import_csv,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    DEFAULT_BOUND_SPEAKER_CSV_PATH,
    OBSERVED_MANUAL_CHARACTER,
)


MINIMAL_YMMP_BOUNDARY_DECISION_SCHEMA_VERSION = (
    "newsroom_minimal_ymmp_boundary_decision.v1"
)
MINIMAL_YMMP_BOUNDARY_DECISION_ID = (
    "newsroom_minimal_ymmp_boundary_decision_v1_2026_06_23"
)
DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH = Path(
    "samples/_probe/newsroom_handoff/minimal_ymmp_boundary_decision_v1.json"
)
DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_DOC_PATH = Path(
    "docs/verification/NEWSROOM_MINIMAL_YMMP_BOUNDARY_DECISION_V1_2026-06-23.md"
)

RECOMMENDED_NEXT_PATH = "prepare_manual_diagnostic_ymmp_probe_packet"
RECOMMENDED_NEXT_SLICE = "newsroom-diagnostic-ymmp-probe-packet-v1"


def build_default_newsroom_minimal_ymmp_boundary_decision(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed minimal .ymmp boundary decision."""
    base = Path(root) if root is not None else Path(".")
    readiness = load_json_object(base / DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH)
    bound_csv_readback = read_tiny_script_import_csv(
        base / DEFAULT_BOUND_SPEAKER_CSV_PATH
    )
    return build_newsroom_minimal_ymmp_boundary_decision(
        readiness,
        bound_csv_readback=bound_csv_readback,
        source_bound_speaker_readiness_path=(
            DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH
        ),
        source_bound_csv_path=DEFAULT_BOUND_SPEAKER_CSV_PATH,
    )


def build_newsroom_minimal_ymmp_boundary_decision(
    readiness: dict[str, Any],
    *,
    bound_csv_readback: dict[str, Any],
    source_bound_speaker_readiness_path: str | Path,
    source_bound_csv_path: str | Path,
    source_commit_or_status: str = "worktree_verified_before_generation",
) -> dict[str, Any]:
    """Build a diagnostic-only .ymmp boundary decision from readiness evidence."""
    timing_gap = _dict(readiness.get("timing_gap"))
    normalized = _dict(readiness.get("normalized_result"))
    review_memory = _dict(readiness.get("review_memory"))
    accepted_inputs = _accepted_inputs(readiness, bound_csv_readback)
    source_validation = _source_validation(readiness, bound_csv_readback)
    ymmp_boundary = _ymmp_boundary()
    timing_gap_policy = _timing_gap_policy(timing_gap)
    evidence_policy = _evidence_policy()
    operator_card = _operator_observation_card()
    not_accepted_scope = _not_accepted_scope()

    decision_status = (
        "approved_for_next_probe_packet"
        if not source_validation["errors"]
        else "blocked"
    )

    return {
        "artifact_id": MINIMAL_YMMP_BOUNDARY_DECISION_ID,
        "decision_id": MINIMAL_YMMP_BOUNDARY_DECISION_ID,
        "schema_version": MINIMAL_YMMP_BOUNDARY_DECISION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "decision_status": decision_status,
        "identity": {
            "decision_id": MINIMAL_YMMP_BOUNDARY_DECISION_ID,
            "source_bound_speaker_readiness_path": _path_text(
                source_bound_speaker_readiness_path
            ),
            "source_bound_speaker_readiness_id": readiness.get("readback_id"),
            "source_bound_csv_path": _path_text(source_bound_csv_path),
            "source_commit_or_status": source_commit_or_status,
            "production_status": "diagnostic_only",
            "decision_status": decision_status,
        },
        "review_memory": {
            "source_review_memory": review_memory.get("prior_user_review_count"),
            "prior_user_review_count": {
                "manual_import_behavior": 1,
                "bound_speaker_behavior": 1,
                "minimal_ymmp_boundary": 0,
            },
            "accepted_scope": _dict(review_memory.get("accepted_scope")),
            "not_accepted_scope": not_accepted_scope,
            "next_nonredundant_axis": [
                "minimal_ymmp_boundary_decision",
                "diagnostic_ymmp_probe_packet",
                "timing_gap_after_csv_import",
            ],
            "repeated_general_review_allowed": False,
            "input_mode": "freeform",
        },
        "source_validation": source_validation,
        "accepted_inputs": accepted_inputs,
        "ymmp_boundary": ymmp_boundary,
        "recommended_next_path": {
            "choice": RECOMMENDED_NEXT_PATH,
            "next_recommended_slice": RECOMMENDED_NEXT_SLICE,
            "reason": (
                "Bound speaker CSV import is accepted in the current diagnostic "
                "environment, but the CSV path does not carry the 68 second "
                "neutral timing plan. The narrow next move is to prepare, not "
                "execute, a manual diagnostic .ymmp probe packet that keeps "
                "render, TTS, real media, and production closed."
            ),
            "alternatives_considered": [
                {
                    "path": "timing_gap_strategy_first",
                    "reason_not_default": (
                        "Useful soon, but the permission boundary for any "
                        "saved project should be fixed before strategy work "
                        "can name concrete evidence."
                    ),
                },
                {
                    "path": "TTS_boundary_first",
                    "reason_not_default": (
                        "Premature because the current bottleneck is import/"
                        ".ymmp/timing, not narration or audio generation."
                    ),
                },
                {
                    "path": "defer_ymmp",
                    "reason_not_default": (
                        "Too conservative now that speaker import works and "
                        "the next probe can remain manual and diagnostic."
                    ),
                },
            ],
        },
        "timing_gap_policy": timing_gap_policy,
        "evidence_policy": evidence_policy,
        "operator_observation_card": operator_card,
        "human_burden_hygiene": {
            "user_input": "freeform",
            "template_required": False,
            "schema_owner": "Agent",
            "max_required_points": len(operator_card["look_for"]),
            "screenshot_optional": True,
            "negative_confirmations_required_from_user": False,
            "fixed_form_result_template": False,
        },
        "not_accepted_scope": not_accepted_scope,
        "next_recommended_slice": RECOMMENDED_NEXT_SLICE,
        "downstream_next_use": {
            "use_this_decision_to": (
                "Write the next diagnostic .ymmp probe packet with a compact "
                "freeform observation card and no production, render, TTS, or "
                "real-media route."
            ),
            "do_not_use_this_decision_to": [
                "create .ymmp in this slice",
                "claim render readiness",
                "claim TTS readiness",
                "claim production readiness",
                "publish or prepare a public video",
            ],
        },
        "review_card": {
            "status": "none",
            "axis_if_needed": "minimal_ymmp_boundary_decision",
            "reason": (
                "This slice is an agent-owned boundary decision based on the "
                "already recorded freeform YMM4 observation. It does not ask "
                "for repeated prior review or a fixed result template."
            ),
        },
        "boundary_assertions": {
            **ymmp_boundary,
            "diagnostic_only": True,
            "decision_only_no_probe_execution": True,
            "YMM4_launched_by_agent": False,
            "external_fetch_performed": False,
            "real_newsroom_ingest_performed": False,
            "dashboard_governance_freshness_changed": False,
        },
    }


def render_newsroom_minimal_ymmp_boundary_decision_markdown(
    decision: dict[str, Any],
) -> str:
    """Render a human-readable minimal .ymmp boundary decision."""
    identity = _dict(decision.get("identity"))
    accepted = _dict(decision.get("accepted_inputs"))
    ymmp = _dict(decision.get("ymmp_boundary"))
    next_path = _dict(decision.get("recommended_next_path"))
    timing = _dict(decision.get("timing_gap_policy"))
    evidence = _dict(decision.get("evidence_policy"))
    hygiene = _dict(decision.get("human_burden_hygiene"))
    not_accepted = _dict(decision.get("not_accepted_scope"))
    operator_card = _dict(decision.get("operator_observation_card"))

    lines = [
        "# Newsroom Minimal .ymmp Boundary Decision v1",
        "",
        f"artifact_id: {decision.get('artifact_id')}",
        f"decision_id: {decision.get('decision_id')}",
        f"schema_version: {decision.get('schema_version')}",
        f"review_status: {decision.get('review_status')}",
        f"production_status: {decision.get('production_status')}",
        f"decision_status: {decision.get('decision_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        (
            "- source_bound_speaker_readiness_path: "
            f"{identity.get('source_bound_speaker_readiness_path')}"
        ),
        (
            "- source_bound_speaker_readiness_id: "
            f"{identity.get('source_bound_speaker_readiness_id')}"
        ),
        f"- source_bound_csv_path: {identity.get('source_bound_csv_path')}",
        f"- source_commit_or_status: {identity.get('source_commit_or_status')}",
        "",
        "## Accepted Inputs",
        "",
        (
            "- bound_CSV_accepted_in_current_environment: "
            f"{str(accepted.get('bound_CSV_accepted_in_current_environment')).lower()}"
        ),
        f"- speaker_value: {accepted.get('speaker_value')}",
        f"- row_count: {accepted.get('row_count')}",
        f"- text_visible: {str(accepted.get('text_visible')).lower()}",
        (
            "- speaker_prompt_shown: "
            f"{str(accepted.get('speaker_prompt_shown')).lower()}"
        ),
        f"- accepted_for: {accepted.get('accepted_for')}",
        "",
        "## .ymmp Boundary",
        "",
        f"- current_ymmp_status: {ymmp.get('current_ymmp_status')}",
        (
            "- agent_may_create_ymmp_now: "
            f"{str(ymmp.get('agent_may_create_ymmp_now')).lower()}"
        ),
        (
            "- user_manual_ymmp_probe_may_be_prepared_next: "
            f"{str(ymmp.get('user_manual_ymmp_probe_may_be_prepared_next')).lower()}"
        ),
        f"- production_ymmp_allowed: {str(ymmp.get('production_ymmp_allowed')).lower()}",
        f"- render_allowed: {str(ymmp.get('render_allowed')).lower()}",
        (
            "- TTS_generation_allowed: "
            f"{str(ymmp.get('TTS_generation_allowed')).lower()}"
        ),
        f"- real_media_allowed: {str(ymmp.get('real_media_allowed')).lower()}",
        "",
        "## Recommended Next Path",
        "",
        f"- choice: {next_path.get('choice')}",
        f"- next_recommended_slice: {next_path.get('next_recommended_slice')}",
        f"- reason: {next_path.get('reason')}",
        "",
        "## Timing Gap Policy",
        "",
        f"- neutral_timeline_total_sec: {timing.get('neutral_timeline_total_sec')}",
        (
            "- observed_yym4_import_approx_sec: "
            f"{timing.get('observed_yym4_import_approx_sec')}"
        ),
        (
            "- timing_imported_by_csv: "
            f"{str(timing.get('timing_imported_by_csv')).lower()}"
        ),
        f"- recommended_default: {timing.get('recommended_default')}",
        f"- reason: {timing.get('reason')}",
        "- options:",
    ]
    for option in timing.get("options", []):
        lines.append(f"  - {option}")

    lines.extend(
        [
            "",
            "## Evidence Policy",
            "",
            f"- input_mode: {evidence.get('input_mode')}",
            f"- template_required: {str(evidence.get('template_required')).lower()}",
            f"- schema_owner: {evidence.get('schema_owner')}",
            (
                "- screenshot_optional: "
                f"{str(evidence.get('screenshot_optional')).lower()}"
            ),
            "- sufficient_freeform_evidence:",
        ]
    )
    for item in evidence.get("sufficient_freeform_evidence", []):
        lines.append(f"  - {item}")

    lines.extend(["", "## Operator Observation Card", ""])
    for key in ("status", "target", "why", "action", "answer_style"):
        lines.append(f"- {key}: {operator_card.get(key)}")
    lines.append("- look_for:")
    for item in operator_card.get("look_for", []):
        lines.append(f"  - {item}")
    lines.append("- not_needed:")
    for item in operator_card.get("not_needed", []):
        lines.append(f"  - {item}")

    lines.extend(["", "## Human Burden Hygiene", ""])
    for key, value in hygiene.items():
        lines.append(f"- {key}: {str(value).lower() if isinstance(value, bool) else value}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in not_accepted.items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(
        [
            "",
            "## Review Card",
            "",
            "Review Card: none. This is an agent-owned boundary decision and "
            "does not ask for repeated prior review or a fixed result template.",
            "",
            "## Boundary",
            "",
            "This decision does not create `.ymmp`, launch YMM4, render, "
            "generate TTS/audio, import real media, fetch external sources, "
            "approve production, or prepare a public video.",
            "",
        ]
    )
    return "\n".join(lines)


def _accepted_inputs(
    readiness: dict[str, Any],
    bound_csv_readback: dict[str, Any],
) -> dict[str, Any]:
    surface = _dict(readiness.get("accepted_import_surface"))
    result = _dict(readiness.get("normalized_result"))
    return {
        "bound_CSV_accepted_in_current_environment": readiness.get("result")
        == "pass",
        "speaker_value": surface.get("speaker_value") or OBSERVED_MANUAL_CHARACTER,
        "row_count": bound_csv_readback.get("row_count"),
        "text_visible": result.get("all_text_visible") is True,
        "speaker_prompt_shown": result.get("speaker_selection_prompt_shown")
        is True,
        "speaker_prompt_not_shown": result.get("speaker_selection_prompt_shown")
        is False,
        "csv_encoding": surface.get("encoding"),
        "csv_header": surface.get("header"),
        "csv_columns": surface.get("columns") or list(TARGET_SURFACE_COLUMNS),
        "accepted_for": surface.get("accepted_for"),
    }


def _ymmp_boundary() -> dict[str, Any]:
    return {
        "current_ymmp_status": "not_created",
        "agent_may_create_ymmp_now": False,
        "user_manual_ymmp_probe_may_be_prepared_next": True,
        "production_ymmp_allowed": False,
        "render_allowed": False,
        "TTS_generation_allowed": False,
        "real_media_allowed": False,
        "real_newsroom_ingest_allowed": False,
        "external_fetch_allowed": False,
        "public_video_allowed": False,
    }


def _timing_gap_policy(timing_gap: dict[str, Any]) -> dict[str, Any]:
    return {
        "neutral_timeline_total_sec": timing_gap.get(
            "prior_neutral_timeline_total_sec"
        ),
        "observed_yym4_import_approx_sec": timing_gap.get(
            "observed_yym4_timeline_approx_sec"
        ),
        "timing_imported_by_csv": False,
        "options": [
            "accept YMM4 natural duration for first diagnostic .ymmp",
            "patch timing after import",
            "keep timing metadata external until render path",
        ],
        "recommended_default": (
            "accept YMM4 natural duration for first diagnostic .ymmp"
        ),
        "reason": (
            "The next probe should isolate the save/readback boundary first. "
            "Using YMM4 natural dialogue duration avoids mixing manual timing "
            "adjustment with the first diagnostic .ymmp evidence."
        ),
    }


def _evidence_policy() -> dict[str, Any]:
    return {
        "input_mode": "freeform",
        "template_required": False,
        "schema_owner": "Agent",
        "screenshot_optional": True,
        "negative_confirmations_required_from_user": False,
        "sufficient_freeform_evidence": [
            "whether a diagnostic .ymmp was saved",
            "whether 4 imported dialogue rows still exist",
            "whether timing stayed short or was manually adjusted",
        ],
        "not_sufficient_for": [
            "production readiness",
            "render readiness",
            "TTS readiness",
            "public video readiness",
        ],
    }


def _operator_observation_card() -> dict[str, Any]:
    return {
        "status": "for_next_probe_packet_only",
        "target": "manual diagnostic .ymmp probe after a future packet is written",
        "why": (
            "Confirm only the save/readback and timing-boundary behavior for a "
            "diagnostic project, without render, TTS, real media, or production."
        ),
        "action": (
            "If a later packet authorizes it, save a diagnostic project from the "
            "bound CSV import and answer in freeform."
        ),
        "look_for": [
            ".ymmp saved or not saved",
            "4 dialogue rows still present",
            "timing stayed short or was adjusted",
        ],
        "answer_style": "freeform",
        "not_needed": [
            "fixed result form",
            "render confirmation",
            "TTS/audio confirmation",
            "production approval",
        ],
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_readiness": False,
        "render_readiness": False,
        "TTS_readiness": False,
        "public_video_readiness": False,
        "visual_layout_import": False,
        "portability_across_all_YMM4_installations": False,
        "timing_import_from_neutral_timeline_metadata": False,
    }


def _source_validation(
    readiness: dict[str, Any],
    bound_csv_readback: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if readiness.get("result") != "pass":
        errors.append("BOUND_SPEAKER_READINESS_NOT_PASS")
    if bound_csv_readback.get("bom_verified") is not True:
        errors.append("BOUND_CSV_BOM_NOT_VERIFIED")
    if bound_csv_readback.get("has_header") is not False:
        errors.append("BOUND_CSV_HEADER_PRESENT")
    if bound_csv_readback.get("all_rows_two_columns") is not True:
        errors.append("BOUND_CSV_NOT_TWO_COLUMN")
    if bound_csv_readback.get("row_count") != EXPECTED_MANUAL_IMPORT_ROW_COUNT:
        errors.append("BOUND_CSV_ROW_COUNT_NOT_4")

    normalized = _dict(readiness.get("normalized_result"))
    timing_gap = _dict(readiness.get("timing_gap"))
    if normalized.get("speaker_selection_prompt_shown") is not False:
        errors.append("SPEAKER_PROMPT_NOT_FALSE")
    if normalized.get("all_text_visible") is not True:
        errors.append("ALL_TEXT_VISIBLE_NOT_TRUE")
    if timing_gap.get("timing_imported_from_csv") is not False:
        errors.append("TIMING_IMPORTED_FROM_CSV_NOT_FALSE")

    rows = _list(bound_csv_readback.get("rows"))
    row_checks: list[dict[str, Any]] = []
    for row in rows:
        row_errors: list[str] = []
        if row.get("speaker") != OBSERVED_MANUAL_CHARACTER:
            row_errors.append("speaker_mismatch")
        if not row.get("text"):
            row_errors.append("text_empty")
        errors.extend(
            f"CSV_ROW_{row.get('row_number')}:{error}" for error in row_errors
        )
        row_checks.append(
            {
                "row_number": row.get("row_number"),
                "speaker_matches_bound_value": (
                    row.get("speaker") == OBSERVED_MANUAL_CHARACTER
                ),
                "text_non_empty": bool(row.get("text")),
                "status": "passed" if not row_errors else "failed",
                "errors": row_errors,
            }
        )

    return {
        "source_readiness_id": readiness.get("readback_id"),
        "source_readiness_result": readiness.get("result"),
        "bound_csv_bom_verified": bound_csv_readback.get("bom_verified"),
        "bound_csv_has_header": bound_csv_readback.get("has_header"),
        "bound_csv_all_rows_two_columns": bound_csv_readback.get(
            "all_rows_two_columns"
        ),
        "bound_csv_row_count": bound_csv_readback.get("row_count"),
        "all_rows_use_bound_speaker": all(
            check["speaker_matches_bound_value"] for check in row_checks
        ),
        "all_rows_have_text": all(check["text_non_empty"] for check in row_checks),
        "speaker_prompt_shown": normalized.get("speaker_selection_prompt_shown"),
        "timing_imported_from_csv": timing_gap.get("timing_imported_from_csv"),
        "rows": row_checks,
        "errors": errors,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None
