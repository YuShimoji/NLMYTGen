"""Readback for the diagnostic bound-speaker YMM4 CSV import.

This module records a user/operator observation for the already committed
bound-speaker CSV candidate. It does not launch YMM4, create or edit projects,
render, generate TTS/audio, import real media, fetch external sources, or
approve production use.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_neutral_timeline_import_proof import (
    DEFAULT_NEUTRAL_TIMELINE_PATH,
)
from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    EXPECTED_MANUAL_IMPORT_ROW_COUNT,
    TARGET_SURFACE_COLUMNS,
    read_tiny_script_import_csv,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    DEFAULT_BOUND_SPEAKER_CSV_PATH,
    DEFAULT_SPEAKER_BINDING_POLICY_PATH,
    OBSERVED_MANUAL_CHARACTER,
)


BOUND_SPEAKER_IMPORT_READINESS_SCHEMA_VERSION = (
    "newsroom_yym4_bound_speaker_import_readiness.v1"
)
BOUND_SPEAKER_IMPORT_READINESS_ID = (
    "newsroom_yym4_bound_speaker_import_readiness_v1_2026_06_23"
)
DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH = Path(
    "samples/_probe/newsroom_handoff/yym4_bound_speaker_import_readiness_v1.json"
)
DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_YYM4_BOUND_SPEAKER_IMPORT_READINESS_V1_2026-06-23.md"
)

OBSERVED_YYM4_VERSION = "v4.53.0.6"
OBSERVED_YYM4_TIMELINE_APPROX_SEC = 8.48
MANUAL_OBSERVATION_SOURCE = "user_freeform_and_supervisor_screenshot"


def build_default_newsroom_yym4_bound_speaker_import_readiness(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed bound-speaker import readiness readback."""
    base = Path(root) if root is not None else Path(".")
    policy = load_json_object(base / DEFAULT_SPEAKER_BINDING_POLICY_PATH)
    neutral_timeline = load_json_object(base / DEFAULT_NEUTRAL_TIMELINE_PATH)
    bound_csv_readback = read_tiny_script_import_csv(
        base / DEFAULT_BOUND_SPEAKER_CSV_PATH
    )
    return build_newsroom_yym4_bound_speaker_import_readiness(
        policy,
        neutral_timeline,
        bound_csv_readback=bound_csv_readback,
        source_policy_path=DEFAULT_SPEAKER_BINDING_POLICY_PATH,
        source_bound_csv_path=DEFAULT_BOUND_SPEAKER_CSV_PATH,
        source_neutral_timeline_path=DEFAULT_NEUTRAL_TIMELINE_PATH,
    )


def build_newsroom_yym4_bound_speaker_import_readiness(
    policy: dict[str, Any],
    neutral_timeline: dict[str, Any],
    *,
    bound_csv_readback: dict[str, Any],
    source_policy_path: str | Path,
    source_bound_csv_path: str | Path,
    source_neutral_timeline_path: str | Path,
    source_commit_or_status: str = "worktree_verified_before_generation",
) -> dict[str, Any]:
    """Build a diagnostic readback from user/operator YMM4 observation."""
    policy_identity = _dict(policy.get("identity"))
    policy_candidate = _dict(policy.get("optional_bound_csv_candidate"))
    source_validation = _source_validation(
        policy,
        bound_csv_readback,
        policy_candidate=policy_candidate,
    )
    normalized_result = _normalized_result()
    timing_gap = _timing_gap(neutral_timeline)
    accepted_surface = _accepted_import_surface(bound_csv_readback)
    not_accepted_scope = _not_accepted_scope()
    safety = _safety_boundary()

    return {
        "artifact_id": BOUND_SPEAKER_IMPORT_READINESS_ID,
        "readback_id": BOUND_SPEAKER_IMPORT_READINESS_ID,
        "schema_version": BOUND_SPEAKER_IMPORT_READINESS_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "manual_observation_source": MANUAL_OBSERVATION_SOURCE,
        "result": normalized_result["result"],
        "identity": {
            "readback_id": BOUND_SPEAKER_IMPORT_READINESS_ID,
            "source_policy_path": _path_text(source_policy_path),
            "source_policy_id": policy.get("policy_id"),
            "source_policy_status": policy.get("policy_status"),
            "source_bound_csv_path": _path_text(source_bound_csv_path),
            "source_neutral_timeline_path": _path_text(
                source_neutral_timeline_path
            ),
            "source_neutral_timeline_id": neutral_timeline.get("timeline_id"),
            "source_commit_or_status": source_commit_or_status,
            "production_status": "diagnostic_only",
            "manual_observation_source": MANUAL_OBSERVATION_SOURCE,
            "screenshot_reference": "user_attached_supervisor_screenshot_not_committed",
        },
        "review_memory": {
            "review_source": MANUAL_OBSERVATION_SOURCE,
            "prior_user_review_count": {
                "manual_import_behavior": 1,
                "bound_speaker_behavior": 1,
            },
            "accepted_scope": {
                "tiny_speaker_text_csv_import_in_YMM4": True,
                "bound_speaker_value_recognized_in_current_environment": True,
                "four_dialogue_rows_visible": True,
                "all_text_visible": True,
                "manual_speaker_selection_needed_for_bound_csv": False,
            },
            "not_accepted_scope": not_accepted_scope,
            "next_nonredundant_axis": [
                "bound_speaker_import_readiness",
                "timing_gap_after_csv_import",
                "minimal_ymmp_boundary_decision",
            ],
            "repeated_general_review_allowed": False,
            "input_mode": "freeform",
        },
        "source_validation": source_validation,
        "normalized_result": normalized_result,
        "accepted_import_surface": accepted_surface,
        "target_csv_readback": {
            "path": _path_text(source_bound_csv_path),
            "bom_verified": bound_csv_readback.get("bom_verified"),
            "row_count": bound_csv_readback.get("row_count"),
            "all_rows_two_columns": bound_csv_readback.get(
                "all_rows_two_columns"
            ),
            "has_header": bound_csv_readback.get("has_header"),
            "rows": bound_csv_readback.get("rows"),
        },
        "policy_linkage": {
            "source_policy_id": policy.get("policy_id"),
            "policy_status_before_observation": policy.get("policy_status"),
            "candidate_status_before_observation": policy_candidate.get("status"),
            "candidate_speaker_name": _dict(
                policy.get("binding_proposal")
            ).get("candidate_speaker_name"),
            "policy_recommended_default": _dict(
                _dict(policy.get("binding_proposal")).get("recommended_default")
            ).get("mode"),
            "readiness_delta": {
                "before": "not_YMM4_verified",
                "after": (
                    "diagnostic_import_accepted_in_current_environment_"
                    "with_timing_gap"
                ),
                "speaker_selection_prompt_removed_in_current_environment": True,
                "automatic_portability_across_all_YMM4_installations": False,
            },
        },
        "timing_gap": timing_gap,
        "not_accepted_scope": not_accepted_scope,
        "safety_boundary": safety,
        "boundary_assertions": {
            **safety,
            "diagnostic_only": True,
            "YMM4_launched_by_agent": False,
            "agent_claims_only_user_observed_result": True,
            "bound_csv_source_replaced": False,
            "timing_imported_from_csv": False,
            "neutral_timeline_metadata_preserved_only_as_reference": True,
            "external_fetch_performed": False,
            "real_newsroom_ingest_performed": False,
            "dashboard_governance_freshness_changed": False,
        },
        "recommended_next_slices": [
            "newsroom-minimal-ymmp-boundary-decision-v1",
            "newsroom-yym4-timing-gap-strategy-v1",
            "newsroom-diagnostic-ymmp-probe-packet-v1",
        ],
        "next_actions": {
            "recommended_default": "newsroom-minimal-ymmp-boundary-decision-v1",
            "why": (
                "The speaker value is now diagnostically accepted in the "
                "current YMM4 environment, so the next bottleneck is whether "
                "and how to cross the `.ymmp`/timing boundary without implying "
                "render, TTS, media, or production readiness."
            ),
            "allowed": [
                "minimal .ymmp boundary decision",
                "timing gap strategy",
                "diagnostic .ymmp probe packet",
            ],
            "prohibited_immediate": [
                "production .ymmp",
                "render",
                "TTS/audio generation",
                "real media import",
                "production approval",
                "public video",
            ],
        },
        "review_card": {
            "status": "none",
            "axis_if_needed": "minimal_ymmp_boundary_decision",
            "reason": (
                "The user already provided freeform bound-speaker YMM4 "
                "observation and screenshot context. No fixed template or "
                "repeated review of prior timing/caption/copy/CSV/script/tiny "
                "proof artifacts is needed."
            ),
        },
    }


def render_newsroom_yym4_bound_speaker_import_readiness_markdown(
    readback: dict[str, Any],
) -> str:
    """Render a human-readable bound-speaker import readiness readback."""
    identity = _dict(readback.get("identity"))
    result = _dict(readback.get("normalized_result"))
    surface = _dict(readback.get("accepted_import_surface"))
    timing = _dict(readback.get("timing_gap"))
    review = _dict(readback.get("review_memory"))
    safety = _dict(readback.get("safety_boundary"))
    next_actions = _dict(readback.get("next_actions"))

    lines = [
        "# Newsroom YMM4 Bound Speaker Import Readiness v1",
        "",
        f"artifact_id: {readback.get('artifact_id')}",
        f"readback_id: {readback.get('readback_id')}",
        f"schema_version: {readback.get('schema_version')}",
        f"review_status: {readback.get('review_status')}",
        f"production_status: {readback.get('production_status')}",
        f"manual_observation_source: {readback.get('manual_observation_source')}",
        f"result: {readback.get('result')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        f"- source_policy_path: {identity.get('source_policy_path')}",
        f"- source_policy_id: {identity.get('source_policy_id')}",
        f"- source_bound_csv_path: {identity.get('source_bound_csv_path')}",
        (
            "- source_neutral_timeline_path: "
            f"{identity.get('source_neutral_timeline_path')}"
        ),
        f"- screenshot_reference: {identity.get('screenshot_reference')}",
        "",
        "## Normalized Result",
        "",
        f"- result: {result.get('result')}",
        f"- YMM4_version: {result.get('YMM4_version')}",
        f"- observed_line_count: {result.get('observed_line_count')}",
        f"- expected_line_count: {result.get('expected_line_count')}",
        f"- all_text_visible: {str(result.get('all_text_visible')).lower()}",
        (
            "- speaker_selection_prompt_shown: "
            f"{str(result.get('speaker_selection_prompt_shown')).lower()}"
        ),
        f"- speaker_behavior: {result.get('speaker_behavior')}",
        (
            "- selected_speaker_or_character: "
            f"{result.get('selected_speaker_or_character')}"
        ),
        (
            "- encoding_or_text_issues: "
            f"{str(result.get('encoding_or_text_issues')).lower()}"
        ),
        (
            "- header_or_column_issues: "
            f"{str(result.get('header_or_column_issues')).lower()}"
        ),
        f"- render_created: {str(result.get('render_created')).lower()}",
        f"- ymmp_committed: {str(result.get('ymmp_committed')).lower()}",
        (
            "- production_approval: "
            f"{str(result.get('production_approval')).lower()}"
        ),
        "",
        "## Accepted Import Surface",
        "",
        f"- encoding: {surface.get('encoding')}",
        f"- header: {str(surface.get('header')).lower()}",
        f"- columns: {', '.join(surface.get('columns', []))}",
        f"- speaker_value: {surface.get('speaker_value')}",
        f"- row_count: {surface.get('row_count')}",
        f"- accepted_for: {surface.get('accepted_for')}",
        f"- environment: {surface.get('environment')}",
        "",
        "## Timing Gap",
        "",
        (
            "- prior_neutral_timeline_total_sec: "
            f"{timing.get('prior_neutral_timeline_total_sec')}"
        ),
        (
            "- observed_yym4_timeline_approx_sec: "
            f"{timing.get('observed_yym4_timeline_approx_sec')}"
        ),
        (
            "- timing_imported_from_csv: "
            f"{str(timing.get('timing_imported_from_csv')).lower()}"
        ),
        f"- meaning: {timing.get('meaning')}",
        "- next_timing_axis:",
    ]
    for axis in timing.get("next_timing_axis", []):
        lines.append(f"  - {axis}")

    lines.extend(
        [
            "",
            "## Review Memory",
            "",
            (
                "- prior_user_review_count: "
                f"{review.get('prior_user_review_count')}"
            ),
            "- repeated_general_review_allowed: false",
            "- input_mode: freeform",
            "- next_nonredundant_axis:",
        ]
    )
    for axis in review.get("next_nonredundant_axis", []):
        lines.append(f"  - {axis}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(readback.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(["", "## Safety Boundary", ""])
    for key, value in safety.items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(
        [
            "",
            "## Recommended Next Slices",
            "",
        ]
    )
    for next_slice in readback.get("recommended_next_slices", []):
        lines.append(f"- {next_slice}")

    lines.extend(
        [
            "",
            "## Minimal Boundary Decision",
            "",
            f"- recommended_default: {next_actions.get('recommended_default')}",
            f"- why: {next_actions.get('why')}",
            "- allowed:",
        ]
    )
    for item in next_actions.get("allowed", []):
        lines.append(f"  - {item}")
    lines.append("- prohibited_immediate:")
    for item in next_actions.get("prohibited_immediate", []):
        lines.append(f"  - {item}")

    lines.extend(
        [
            "",
            "## Review Card",
            "",
            "Review Card: none. The user already provided freeform observation "
            "for the bound-speaker import, so no fixed template or repeated "
            "prior-artifact review is requested.",
            "",
            "## Boundary",
            "",
            "This readback records a diagnostic user/operator YMM4 observation. "
            "It does not create `.ymmp`, render output, TTS/audio, real media, "
            "production approval, YMM4-wide portability approval, or public "
            "video readiness.",
            "",
        ]
    )
    return "\n".join(lines)


def _normalized_result() -> dict[str, Any]:
    return {
        "result": "pass",
        "YMM4_version": OBSERVED_YYM4_VERSION,
        "observed_line_count": EXPECTED_MANUAL_IMPORT_ROW_COUNT,
        "expected_line_count": EXPECTED_MANUAL_IMPORT_ROW_COUNT,
        "all_text_visible": True,
        "speaker_selection_prompt_shown": False,
        "speaker_behavior": (
            "automatically_bound_to_yukkuri_reimu_in_current_environment"
        ),
        "selected_speaker_or_character": OBSERVED_MANUAL_CHARACTER,
        "encoding_or_text_issues": False,
        "header_or_column_issues": False,
        "script_editor_rows_visible": True,
        "main_timeline_dialogue_items_visible": True,
        "preview_text_visible": True,
        "observed_yym4_timeline_approx_sec": OBSERVED_YYM4_TIMELINE_APPROX_SEC,
        "render_created": False,
        "ymmp_committed": False,
        "production_approval": False,
    }


def _accepted_import_surface(csv_readback: dict[str, Any]) -> dict[str, Any]:
    return {
        "encoding": "UTF-8 BOM",
        "header": False,
        "columns": list(TARGET_SURFACE_COLUMNS),
        "speaker_value": OBSERVED_MANUAL_CHARACTER,
        "row_count": csv_readback.get("row_count"),
        "accepted_for": "diagnostic_yym4_script_import_in_current_environment",
        "environment": f"Planner007/YMM4 {OBSERVED_YYM4_VERSION}",
        "speaker_selection_prompt_shown": False,
        "all_text_visible": True,
        "timing_columns_in_csv": False,
        "production_ready_flags_in_csv": False,
    }


def _timing_gap(neutral_timeline: dict[str, Any]) -> dict[str, Any]:
    prior_total = _dict(neutral_timeline.get("global_timing")).get(
        "total_duration_sec"
    )
    gap = None
    ratio = None
    if isinstance(prior_total, (int, float)):
        gap = round(float(prior_total) - OBSERVED_YYM4_TIMELINE_APPROX_SEC, 2)
        ratio = round(OBSERVED_YYM4_TIMELINE_APPROX_SEC / float(prior_total), 4)
    return {
        "prior_neutral_timeline_total_sec": prior_total,
        "observed_yym4_timeline_approx_sec": OBSERVED_YYM4_TIMELINE_APPROX_SEC,
        "timing_imported_from_csv": False,
        "gap_sec": gap,
        "observed_to_prior_duration_ratio": ratio,
        "meaning": (
            "The tiny speaker,text CSV path imports dialogue rows and recognized "
            "speaker values, but it does not import the neutral 68 second "
            "timeline timing plan. YMM4 appears to create its own short "
            "dialogue timeline from the imported items."
        ),
        "next_timing_axis": [
            "minimal_ymmp_boundary_decision",
            "timing_patch_strategy",
            "YMM4_natural_duration_strategy",
        ],
    }


def _source_validation(
    policy: dict[str, Any],
    csv_readback: dict[str, Any],
    *,
    policy_candidate: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    rows = _list(csv_readback.get("rows"))
    policy_rows = _list(policy_candidate.get("rows"))
    if policy.get("policy_status") != "diagnostic_candidate":
        errors.append("POLICY_STATUS_NOT_DIAGNOSTIC_CANDIDATE")
    if csv_readback.get("bom_verified") is not True:
        errors.append("BOUND_CSV_BOM_NOT_VERIFIED")
    if csv_readback.get("has_header") is not False:
        errors.append("BOUND_CSV_HEADER_PRESENT")
    if csv_readback.get("all_rows_two_columns") is not True:
        errors.append("BOUND_CSV_NOT_TWO_COLUMN")
    if csv_readback.get("row_count") != EXPECTED_MANUAL_IMPORT_ROW_COUNT:
        errors.append("BOUND_CSV_ROW_COUNT_NOT_4")
    if len(policy_rows) != EXPECTED_MANUAL_IMPORT_ROW_COUNT:
        errors.append("POLICY_CANDIDATE_ROW_COUNT_NOT_4")

    row_checks: list[dict[str, Any]] = []
    for row, policy_row in zip(rows, policy_rows, strict=False):
        row_errors: list[str] = []
        speaker = str(row.get("speaker") or "")
        text = str(row.get("text") or "")
        policy_text = str(policy_row.get("text") or "")
        if speaker != OBSERVED_MANUAL_CHARACTER:
            row_errors.append("speaker_not_bound_character")
        if text != policy_text:
            row_errors.append("text_mismatch_with_policy")
        errors.extend(
            f"CSV_ROW_{row.get('row_number')}:{error}" for error in row_errors
        )
        row_checks.append(
            {
                "row_number": row.get("row_number"),
                "speaker_is_bound_character": speaker == OBSERVED_MANUAL_CHARACTER,
                "text_matches_policy_candidate": text == policy_text,
                "status": "passed" if not row_errors else "failed",
                "errors": row_errors,
            }
        )

    return {
        "source_policy_id": policy.get("policy_id"),
        "source_policy_status": policy.get("policy_status"),
        "bound_csv_bom_verified": csv_readback.get("bom_verified"),
        "bound_csv_has_header": csv_readback.get("has_header"),
        "bound_csv_all_rows_two_columns": csv_readback.get(
            "all_rows_two_columns"
        ),
        "bound_csv_row_count": csv_readback.get("row_count"),
        "all_rows_use_bound_speaker": all(
            check["speaker_is_bound_character"] for check in row_checks
        ),
        "all_text_matches_policy_candidate": all(
            check["text_matches_policy_candidate"] for check in row_checks
        ),
        "rows": row_checks,
        "errors": errors,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "automatic_portability_across_all_YMM4_installations": False,
        "TTS_ready": False,
        "render_ready": False,
        "production_ready": False,
        "visual_layout_ready": False,
        "public_video_ready": False,
        "timing_import_from_neutral_timeline_metadata": False,
        "ymmp_ready": False,
    }


def _safety_boundary() -> dict[str, bool]:
    return {
        "ymmp_created": False,
        "YMM4_launched_by_agent": False,
        "render_created": False,
        "TTS_generated": False,
        "real_media_imported": False,
        "production_approval": False,
        "public_video_ready": False,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None
