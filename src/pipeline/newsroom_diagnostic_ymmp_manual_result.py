"""Diagnostic .ymmp manual probe result readback for newsroom handoff."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_diagnostic_ymmp_probe_packet import (
    DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_minimal_ymmp_boundary_decision import (
    DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH,
)
from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    EXPECTED_MANUAL_IMPORT_ROW_COUNT,
    read_tiny_script_import_csv,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    DEFAULT_BOUND_SPEAKER_CSV_PATH,
    OBSERVED_MANUAL_CHARACTER,
)


DIAGNOSTIC_YMMP_MANUAL_RESULT_SCHEMA_VERSION = (
    "newsroom_diagnostic_ymmp_manual_result_readback.v1"
)
DIAGNOSTIC_YMMP_MANUAL_RESULT_ID = (
    "newsroom_diagnostic_ymmp_manual_result_readback_v1_2026_06_23"
)
DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH = Path(
    "samples/_probe/newsroom_handoff/diagnostic_ymmp_manual_result_readback_v1.json"
)
DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_DOC_PATH = Path(
    "docs/verification/NEWSROOM_DIAGNOSTIC_YMMP_MANUAL_RESULT_READBACK_V1_2026-06-23.md"
)
LOCAL_DIAGNOSTIC_YMMP_PATH = Path(
    "_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp"
)


OPERATOR_DIAGNOSTIC_YMMP_MANUAL_RESULT_V1: dict[str, Any] = {
    "result": "pass",
    "observation_source": "user_freeform_and_supervisor_screenshot",
    "diagnostic_ymmp_saved_or_save_attempt_observed": True,
    "local_ymmp_path": str(LOCAL_DIAGNOSTIC_YMMP_PATH).replace("\\", "/"),
    "local_ymmp_path_status": "discoverable_local_file_at_readback_time",
    "ymmp_committed": False,
    "observed_line_count": 4,
    "all_text_visible": True,
    "speaker_preserved": True,
    "speaker_value_ui_observed": OBSERVED_MANUAL_CHARACTER,
    "raw_speaker_value_if_detected": "unknown",
    "encoding_note": (
        "Use the UI-observed speaker value as canonical; terminal mojibake or "
        "raw parse ambiguity is not treated as the accepted speaker value."
    ),
    "timing_observation": "short_natural_duration",
    "render_created": False,
    "explicit_tts_generation_by_operator": False,
    "real_media_imported": False,
    "production_approval": False,
    "screenshot_reference": "provided_in_supervisor_thread",
}


def build_default_newsroom_diagnostic_ymmp_manual_result(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed diagnostic .ymmp manual result readback."""
    base = Path(root) if root is not None else Path(".")
    probe_packet = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_PATH
    )
    boundary_decision = load_json_object(
        base / DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH
    )
    bound_csv_readback = read_tiny_script_import_csv(
        base / DEFAULT_BOUND_SPEAKER_CSV_PATH
    )
    local_ymmp_exists = (base / LOCAL_DIAGNOSTIC_YMMP_PATH).exists()
    return build_newsroom_diagnostic_ymmp_manual_result(
        OPERATOR_DIAGNOSTIC_YMMP_MANUAL_RESULT_V1,
        probe_packet,
        boundary_decision,
        bound_csv_readback=bound_csv_readback,
        local_ymmp_exists=local_ymmp_exists,
        source_probe_packet_path=DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_PATH,
        source_boundary_decision_path=DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH,
        source_bound_csv_path=DEFAULT_BOUND_SPEAKER_CSV_PATH,
    )


def build_newsroom_diagnostic_ymmp_manual_result(
    operator_result: dict[str, Any],
    probe_packet: dict[str, Any],
    boundary_decision: dict[str, Any],
    *,
    bound_csv_readback: dict[str, Any],
    local_ymmp_exists: bool,
    source_probe_packet_path: str | Path,
    source_boundary_decision_path: str | Path,
    source_bound_csv_path: str | Path,
) -> dict[str, Any]:
    """Normalize the freeform manual .ymmp probe observation."""
    accepted_scope = _accepted_scope()
    not_accepted_scope = _not_accepted_scope()
    timing_gap = _timing_gap_carry_forward(boundary_decision)
    normalized = _normalized_result(operator_result)

    return {
        "artifact_id": DIAGNOSTIC_YMMP_MANUAL_RESULT_ID,
        "result_id": DIAGNOSTIC_YMMP_MANUAL_RESULT_ID,
        "schema_version": DIAGNOSTIC_YMMP_MANUAL_RESULT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "manual_probe_status": "observed",
        "result": "pass",
        "identity": {
            "result_id": DIAGNOSTIC_YMMP_MANUAL_RESULT_ID,
            "source_probe_packet_path": _path_text(source_probe_packet_path),
            "source_probe_packet_id": probe_packet.get("packet_id"),
            "source_boundary_decision_path": _path_text(
                source_boundary_decision_path
            ),
            "source_boundary_decision_id": boundary_decision.get("decision_id"),
            "source_bound_csv_path": _path_text(source_bound_csv_path),
            "production_status": "diagnostic_only",
            "manual_probe_status": "observed",
            "observation_source": operator_result["observation_source"],
        },
        "source_validation": _source_validation(
            probe_packet,
            boundary_decision,
            bound_csv_readback,
        ),
        "operator_freeform_observation": {
            "input_mode": "freeform",
            "observation_source": operator_result["observation_source"],
            "screenshot_reference": operator_result["screenshot_reference"],
            "summary": (
                "The manual diagnostic save/result was observed: four rows, "
                "visible text, and the UI-observed speaker remained; duration "
                "stayed short and no render or TTS was reported."
            ),
        },
        "normalized_result": normalized,
        "local_ymmp_discovery": {
            "local_ymmp_path": normalized["local_ymmp_path"],
            "path_status": operator_result["local_ymmp_path_status"],
            "exists_at_readback_time": local_ymmp_exists,
            "path_source": "reported_path_and_workspace_probe",
            "file_inspected": False,
            "ymmp_structure_parsed": False,
            "ymmp_committed": False,
            "commit_policy": "do_not_stage_or_commit_in_this_slice",
        },
        "accepted_scope": accepted_scope,
        "not_accepted_scope": not_accepted_scope,
        "timing_gap_carry_forward": timing_gap,
        "review_memory": {
            "review_source": "diagnostic_ymmp_manual_observation",
            "prior_user_review_count": {
                "manual_import_behavior": 1,
                "bound_speaker_behavior": 1,
                "diagnostic_ymmp_manual_observation": 1,
            },
            "accepted_scope": accepted_scope,
            "not_accepted_scope": not_accepted_scope,
            "next_nonredundant_axis": [
                "ymmp_structure_readback",
                "timing_gap_strategy",
                "audio_tts_boundary",
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
        "next_recommended_slices": [
            "newsroom-ymmp-structure-readback-v1",
            "newsroom-yym4-timing-gap-strategy-v1",
            "newsroom-audio-tts-boundary-v1",
        ],
        "downstream_next_use": {
            "use_this_readback_to": [
                "plan a non-committed diagnostic .ymmp structure readback",
                "carry short natural duration into timing-gap strategy",
                "keep audio/TTS readiness separate from save/readback evidence",
            ],
            "do_not_use_this_readback_to": [
                "commit .ymmp files",
                "claim .ymmp structure acceptance",
                "claim production readiness",
                "claim render readiness",
                "claim TTS readiness",
                "claim timing strategy resolution",
                "prepare or publish a public video",
            ],
        },
        "review_debt": {
            "generic_review_card_emitted": False,
            "reason": (
                "The manual observation is already supplied; this slice does "
                "not request repeated general review or a fixed result template."
            ),
        },
        "boundary_assertions": {
            "diagnostic_only": True,
            "manual_probe_status": "observed",
            "agent_launched_yym4": False,
            "agent_created_or_edited_ymmp": False,
            "ymmp_committed": False,
            "ymmp_structure_parsed": False,
            "render_created": False,
            "TTS_generated": False,
            "real_media_imported": False,
            "production_approval": False,
            "public_video_ready": False,
            "external_fetch_performed": False,
            "real_newsroom_ingest_performed": False,
            "dashboard_governance_freshness_changed": False,
        },
    }


def render_newsroom_diagnostic_ymmp_manual_result_markdown(
    readback: dict[str, Any],
) -> str:
    """Render a human-readable diagnostic .ymmp manual result readback."""
    identity = _dict(readback.get("identity"))
    result = _dict(readback.get("normalized_result"))
    discovery = _dict(readback.get("local_ymmp_discovery"))
    timing = _dict(readback.get("timing_gap_carry_forward"))
    hygiene = _dict(readback.get("human_burden_hygiene"))
    review = _dict(readback.get("review_memory"))

    lines = [
        "# Newsroom Diagnostic .ymmp Manual Result Readback v1",
        "",
        f"artifact_id: {readback.get('artifact_id')}",
        f"result_id: {readback.get('result_id')}",
        f"schema_version: {readback.get('schema_version')}",
        f"review_status: {readback.get('review_status')}",
        f"production_status: {readback.get('production_status')}",
        f"manual_probe_status: {readback.get('manual_probe_status')}",
        f"result: {readback.get('result')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        f"- source_probe_packet_path: {identity.get('source_probe_packet_path')}",
        f"- source_boundary_decision_path: {identity.get('source_boundary_decision_path')}",
        f"- source_bound_csv_path: {identity.get('source_bound_csv_path')}",
        f"- observation_source: {identity.get('observation_source')}",
        "",
        "## Normalized Result",
        "",
    ]
    for key, value in result.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Local .ymmp Discovery", ""])
    for key, value in discovery.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Accepted Scope", ""])
    for key, value in _dict(readback.get("accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(readback.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Timing Gap Carry-forward", ""])
    for key, value in timing.items():
        if isinstance(value, list):
            lines.append(f"- {key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Human Burden Hygiene", ""])
    for key, value in hygiene.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Review Debt",
            "",
            "- generic_review_card_emitted: false",
            f"- repeated_general_review_allowed: {_display(review.get('repeated_general_review_allowed'))}",
            f"- prior_user_review_count: {review.get('prior_user_review_count')}",
            "- next_nonredundant_axis:",
        ]
    )
    for axis in review.get("next_nonredundant_axis", []):
        lines.append(f"  - {axis}")

    lines.extend(["", "## Next Recommended Slices", ""])
    for next_slice in readback.get("next_recommended_slices", []):
        lines.append(f"- {next_slice}")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This readback records a diagnostic manual observation only. It does "
            "not commit or parse `.ymmp`, prove production readiness, prove "
            "render readiness, prove TTS readiness, resolve timing strategy, "
            "or prepare a public video.",
            "",
        ]
    )
    return "\n".join(lines)


def _normalized_result(operator_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "result": "pass",
        "diagnostic_ymmp_saved_or_save_attempt_observed": True,
        "local_ymmp_path": operator_result["local_ymmp_path"],
        "ymmp_committed": False,
        "observed_line_count": operator_result["observed_line_count"],
        "all_text_visible": True,
        "speaker_preserved": True,
        "speaker_value_ui_observed": operator_result["speaker_value_ui_observed"],
        "raw_speaker_value_if_detected": operator_result[
            "raw_speaker_value_if_detected"
        ],
        "encoding_note": operator_result["encoding_note"],
        "timing_observation": "short_natural_duration",
        "render_created": False,
        "explicit_tts_generation_by_operator": False,
        "real_media_imported": False,
        "production_approval": False,
    }


def _source_validation(
    probe_packet: dict[str, Any],
    boundary_decision: dict[str, Any],
    csv_readback: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if probe_packet.get("manual_probe_status") != "not_run":
        errors.append("PROBE_PACKET_MANUAL_STATUS_NOT_NOT_RUN")
    if boundary_decision.get("decision_status") != "approved_for_next_probe_packet":
        errors.append("BOUNDARY_DECISION_NOT_APPROVED_FOR_NEXT_PROBE_PACKET")
    if csv_readback.get("row_count") != EXPECTED_MANUAL_IMPORT_ROW_COUNT:
        errors.append("BOUND_CSV_ROW_COUNT_NOT_4")
    if csv_readback.get("bom_verified") is not True:
        errors.append("BOUND_CSV_BOM_NOT_VERIFIED")
    if csv_readback.get("has_header") is not False:
        errors.append("BOUND_CSV_HEADER_PRESENT")
    if csv_readback.get("all_rows_two_columns") is not True:
        errors.append("BOUND_CSV_NOT_TWO_COLUMN")

    rows = _list(csv_readback.get("rows"))
    row_checks = [
        {
            "row_number": row.get("row_number"),
            "speaker_matches_bound_value": (
                row.get("speaker") == OBSERVED_MANUAL_CHARACTER
            ),
            "text_non_empty": bool(row.get("text")),
        }
        for row in rows
    ]
    for row in row_checks:
        if not row["speaker_matches_bound_value"]:
            errors.append(f"CSV_ROW_{row.get('row_number')}:speaker_mismatch")
        if not row["text_non_empty"]:
            errors.append(f"CSV_ROW_{row.get('row_number')}:text_empty")

    return {
        "source_probe_packet_id": probe_packet.get("packet_id"),
        "source_probe_packet_manual_probe_status": probe_packet.get(
            "manual_probe_status"
        ),
        "source_boundary_decision_id": boundary_decision.get("decision_id"),
        "source_boundary_decision_status": boundary_decision.get(
            "decision_status"
        ),
        "bound_csv_bom_verified": csv_readback.get("bom_verified"),
        "bound_csv_has_header": csv_readback.get("has_header"),
        "bound_csv_all_rows_two_columns": csv_readback.get("all_rows_two_columns"),
        "bound_csv_row_count": csv_readback.get("row_count"),
        "all_rows_use_bound_speaker": all(
            row["speaker_matches_bound_value"] for row in row_checks
        ),
        "all_rows_have_text": all(row["text_non_empty"] for row in row_checks),
        "errors": errors,
    }


def _accepted_scope() -> dict[str, bool]:
    return {
        "diagnostic_ymmp_probe_observed": True,
        "dialogue_rows_preserved": True,
        "speaker_binding_preserved": True,
        "short_natural_duration_observed": True,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_ymmp_ready": False,
        "ymmp_structure_parsed": False,
        "timing_patch_ready": False,
        "TTS_ready": False,
        "render_ready": False,
        "public_video_ready": False,
    }


def _timing_gap_carry_forward(boundary_decision: dict[str, Any]) -> dict[str, Any]:
    timing = _dict(boundary_decision.get("timing_gap_policy"))
    return {
        "neutral_timeline_total_sec": timing.get("neutral_timeline_total_sec"),
        "observed_yym4_duration": "short_natural_duration",
        "prior_observed_yym4_import_approx_sec": timing.get(
            "observed_yym4_import_approx_sec"
        ),
        "timing_gap_status": "unresolved",
        "timing_patch_ready": False,
        "recommended_next_axis": [
            "ymmp_structure_readback",
            "timing_gap_strategy",
        ],
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None
