"""Diagnostic .ymmp probe packet for the newsroom bound-speaker CSV.

This module prepares instructions and evidence boundaries for a later manual
YMM4 probe. It does not launch YMM4, create .ymmp files, render, generate
TTS/audio, import real media, fetch external sources, or approve production use.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_minimal_ymmp_boundary_decision import (
    DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH,
)
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


DIAGNOSTIC_YMMP_PROBE_PACKET_SCHEMA_VERSION = (
    "newsroom_diagnostic_ymmp_probe_packet.v1"
)
DIAGNOSTIC_YMMP_PROBE_PACKET_ID = (
    "newsroom_diagnostic_ymmp_probe_packet_v1_2026_06_23"
)
DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_PATH = Path(
    "samples/_probe/newsroom_handoff/diagnostic_ymmp_probe_packet_v1.json"
)
DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_DOC_PATH = Path(
    "docs/verification/NEWSROOM_DIAGNOSTIC_YMMP_PROBE_PACKET_V1_2026-06-23.md"
)

RECOMMENDED_MANUAL_SAVE_PATH = Path(
    "_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp"
)


def build_default_newsroom_diagnostic_ymmp_probe_packet(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed diagnostic .ymmp probe packet."""
    base = Path(root) if root is not None else Path(".")
    boundary_decision = load_json_object(
        base / DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH
    )
    readiness = load_json_object(base / DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH)
    bound_csv_readback = read_tiny_script_import_csv(
        base / DEFAULT_BOUND_SPEAKER_CSV_PATH
    )
    return build_newsroom_diagnostic_ymmp_probe_packet(
        boundary_decision,
        readiness,
        bound_csv_readback=bound_csv_readback,
        source_boundary_decision_path=DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH,
        source_bound_speaker_readiness_path=(
            DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH
        ),
        source_bound_csv_path=DEFAULT_BOUND_SPEAKER_CSV_PATH,
    )


def build_newsroom_diagnostic_ymmp_probe_packet(
    boundary_decision: dict[str, Any],
    readiness: dict[str, Any],
    *,
    bound_csv_readback: dict[str, Any],
    source_boundary_decision_path: str | Path,
    source_bound_speaker_readiness_path: str | Path,
    source_bound_csv_path: str | Path,
    source_commit_or_status: str = "worktree_verified_before_generation",
) -> dict[str, Any]:
    """Build a manual diagnostic .ymmp probe packet from boundary evidence."""
    source_validation = _source_validation(
        boundary_decision,
        readiness,
        bound_csv_readback,
    )
    target = _target(source_bound_csv_path, bound_csv_readback)
    observation_card = _operator_observation_card()
    timing_policy = _timing_policy(boundary_decision)
    forbidden = _forbidden_actions()
    allowed = _allowed_future_manual_action()
    normalization = _agent_normalization_plan()

    return {
        "artifact_id": DIAGNOSTIC_YMMP_PROBE_PACKET_ID,
        "packet_id": DIAGNOSTIC_YMMP_PROBE_PACKET_ID,
        "schema_version": DIAGNOSTIC_YMMP_PROBE_PACKET_SCHEMA_VERSION,
        "review_status": "ready_for_future_manual_probe",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "manual_probe_status": "not_run",
        "identity": {
            "packet_id": DIAGNOSTIC_YMMP_PROBE_PACKET_ID,
            "source_boundary_decision_path": _path_text(
                source_boundary_decision_path
            ),
            "source_boundary_decision_id": boundary_decision.get("decision_id"),
            "source_bound_speaker_readiness_path": _path_text(
                source_bound_speaker_readiness_path
            ),
            "source_bound_speaker_readiness_id": readiness.get("readback_id"),
            "source_bound_csv_path": _path_text(source_bound_csv_path),
            "source_commit_or_status": source_commit_or_status,
            "production_status": "diagnostic_only",
            "manual_probe_status": "not_run",
        },
        "review_memory": {
            "source_boundary_review_count": _dict(
                boundary_decision.get("review_memory")
            ).get("prior_user_review_count"),
            "source_readiness_review_count": _dict(
                readiness.get("review_memory")
            ).get("prior_user_review_count"),
            "prior_user_review_count": {
                "manual_import_behavior": 1,
                "bound_speaker_behavior": 1,
                "minimal_ymmp_boundary": 0,
                "diagnostic_ymmp_probe_packet": 0,
            },
            "accepted_scope": {
                "bound_speaker_csv_import_current_environment": True,
                "four_dialogue_rows_visible": True,
                "all_text_visible": True,
                "speaker_prompt_not_shown": True,
                "minimal_ymmp_boundary_decision_ready": True,
            },
            "not_accepted_scope": _not_accepted_scope(),
            "next_nonredundant_axis": [
                "diagnostic_ymmp_manual_result_readback",
                "ymmp_save_readback_boundary",
                "timing_gap_after_csv_import",
            ],
            "repeated_general_review_allowed": False,
            "input_mode": "freeform",
        },
        "source_validation": source_validation,
        "target": target,
        "expected_starting_point": {
            "import_bound_speaker_csv": True,
            "confirm_4_rows_and_speaker": True,
            "save_minimal_diagnostic_ymmp_only_if_operator_comfortable": True,
            "do_not_render": True,
            "do_not_generate_TTS": True,
            "do_not_import_real_media": True,
            "timing_patch_in_this_probe": False,
        },
        "allowed_future_manual_action": allowed,
        "forbidden_actions": forbidden,
        "operator_observation_card": observation_card,
        "agent_normalization_plan": normalization,
        "timing_policy": timing_policy,
        "human_burden_hygiene": {
            "user_input": "freeform",
            "template_required": False,
            "schema_owner": "Agent",
            "max_required_points": len(observation_card["look_for"]),
            "screenshot_optional": True,
            "negative_confirmations_required_from_user": False,
            "fixed_form_result_template": False,
        },
        "not_accepted_scope": _not_accepted_scope(),
        "next_recommended_slices": [
            "newsroom-diagnostic-ymmp-manual-result-readback-v1",
            "newsroom-yym4-timing-gap-strategy-v1",
            "newsroom-ymmp-structure-readback-v1",
        ],
        "downstream_next_use": {
            "if_manual_probe_runs_later": (
                "Normalize the user's freeform observation into a diagnostic "
                ".ymmp manual result readback."
            ),
            "if_manual_probe_does_not_run": (
                "Keep this packet as the prepared boundary and continue with a "
                "timing-gap strategy that does not require .ymmp evidence."
            ),
            "do_not_use_this_packet_to": [
                "create .ymmp in this agent slice",
                "claim production readiness",
                "claim render readiness",
                "claim TTS readiness",
                "publish or prepare a public video",
            ],
        },
        "review_card": {
            "status": "none",
            "axis_if_needed": "diagnostic_ymmp_probe_packet",
            "reason": (
                "This slice prepares the manual probe packet only. It does not "
                "ask the user to do the probe inside this agent turn, and it "
                "does not request repeated prior-artifact review."
            ),
        },
        "boundary_assertions": {
            "diagnostic_only": True,
            "manual_probe_status": "not_run",
            "agent_launched_yym4": False,
            "agent_created_or_edited_ymmp": False,
            "ymmp_created": False,
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


def render_newsroom_diagnostic_ymmp_probe_packet_markdown(
    packet: dict[str, Any],
) -> str:
    """Render a human-readable diagnostic .ymmp probe packet."""
    identity = _dict(packet.get("identity"))
    target = _dict(packet.get("target"))
    allowed = _dict(packet.get("allowed_future_manual_action"))
    forbidden = _dict(packet.get("forbidden_actions"))
    card = _dict(packet.get("operator_observation_card"))
    normalization = _dict(packet.get("agent_normalization_plan"))
    timing = _dict(packet.get("timing_policy"))
    hygiene = _dict(packet.get("human_burden_hygiene"))

    lines = [
        "# Newsroom Diagnostic .ymmp Probe Packet v1",
        "",
        f"artifact_id: {packet.get('artifact_id')}",
        f"packet_id: {packet.get('packet_id')}",
        f"schema_version: {packet.get('schema_version')}",
        f"review_status: {packet.get('review_status')}",
        f"production_status: {packet.get('production_status')}",
        f"manual_probe_status: {packet.get('manual_probe_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        (
            "- source_boundary_decision_path: "
            f"{identity.get('source_boundary_decision_path')}"
        ),
        (
            "- source_boundary_decision_id: "
            f"{identity.get('source_boundary_decision_id')}"
        ),
        (
            "- source_bound_speaker_readiness_path: "
            f"{identity.get('source_bound_speaker_readiness_path')}"
        ),
        f"- source_bound_csv_path: {identity.get('source_bound_csv_path')}",
        "",
        "## Target",
        "",
        f"- target_csv: {target.get('target_csv')}",
        f"- intended_YMM4_environment: {target.get('intended_YMM4_environment')}",
        f"- expected_row_count: {target.get('expected_row_count')}",
        f"- speaker_value: {target.get('speaker_value')}",
        f"- encoding: {target.get('encoding')}",
        f"- header: {str(target.get('header')).lower()}",
        f"- columns: {', '.join(target.get('columns', []))}",
        "",
        "## Expected Starting Point",
        "",
    ]
    for key, value in packet.get("expected_starting_point", {}).items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(["", "## Allowed Future Manual Action", ""])
    for key, value in allowed.items():
        if isinstance(value, bool):
            value = str(value).lower()
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Forbidden Actions", ""])
    for key, value in forbidden.items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(
        [
            "",
            "## Operator Observation Card",
            "",
            f"- status: {card.get('status')}",
            f"- target: {card.get('target')}",
            f"- why: {card.get('why')}",
            f"- action: {card.get('action')}",
            "- look_for:",
        ]
    )
    for item in card.get("look_for", []):
        lines.append(f"  - {item}")
    lines.extend(
        [
            f"- answer_style: {card.get('answer_style')}",
            f"- answer_hint: {card.get('answer_hint')}",
            "- not_needed:",
        ]
    )
    for item in card.get("not_needed", []):
        lines.append(f"  - {item}")

    lines.extend(
        [
            "",
            "## Agent Normalization Plan",
            "",
            f"- schema_owner: {normalization.get('schema_owner')}",
            (
                "- exposed_as_user_form: "
                f"{str(normalization.get('exposed_as_user_form')).lower()}"
            ),
            "- fields:",
        ]
    )
    for field in normalization.get("fields", []):
        lines.append(f"  - {field}")

    lines.extend(
        [
            "",
            "## Timing Policy",
            "",
            f"- neutral_timeline_total_sec: {timing.get('neutral_timeline_total_sec')}",
            (
                "- observed_yym4_import_approx_sec: "
                f"{timing.get('observed_yym4_import_approx_sec')}"
            ),
            f"- first_probe_expected_timing: {timing.get('first_probe_expected_timing')}",
            (
                "- timing_patch_in_this_probe: "
                f"{str(timing.get('timing_patch_in_this_probe')).lower()}"
            ),
            "- next_timing_axis:",
        ]
    )
    for axis in timing.get("next_timing_axis", []):
        lines.append(f"  - {axis}")

    lines.extend(["", "## Human Burden Hygiene", ""])
    for key, value in hygiene.items():
        if isinstance(value, bool):
            value = str(value).lower()
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(packet.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(["", "## Next Recommended Slices", ""])
    for next_slice in packet.get("next_recommended_slices", []):
        lines.append(f"- {next_slice}")

    lines.extend(
        [
            "",
            "## Review Card",
            "",
            "Review Card: none. This packet prepares a later manual diagnostic "
            "probe and does not ask for repeated prior-artifact review.",
            "",
            "## Boundary",
            "",
            "This packet does not create `.ymmp`, launch YMM4, render, generate "
            "TTS/audio, import real media, fetch external sources, approve "
            "production, or prepare a public video.",
            "",
        ]
    )
    return "\n".join(lines)


def _target(source_bound_csv_path: str | Path, csv_readback: dict[str, Any]) -> dict[str, Any]:
    return {
        "target_csv": _path_text(source_bound_csv_path),
        "intended_YMM4_environment": "manual/operator-run only",
        "expected_row_count": EXPECTED_MANUAL_IMPORT_ROW_COUNT,
        "observed_row_count_before_probe": csv_readback.get("row_count"),
        "speaker_value": OBSERVED_MANUAL_CHARACTER,
        "encoding": "UTF-8 BOM",
        "bom_verified": csv_readback.get("bom_verified"),
        "header": False,
        "has_header": csv_readback.get("has_header"),
        "columns": list(TARGET_SURFACE_COLUMNS),
        "all_rows_two_columns": csv_readback.get("all_rows_two_columns"),
        "rows": csv_readback.get("rows"),
    }


def _allowed_future_manual_action() -> dict[str, Any]:
    return {
        "manual_YMM4_launch_by_user_operator": True,
        "manual_diagnostic_ymmp_save": True,
        "manual_diagnostic_ymmp_save_scope": "diagnostic observation only",
        "recommended_save_location": _path_text(RECOMMENDED_MANUAL_SAVE_PATH),
        "recommended_save_location_created_by_agent": False,
        "committing_ymmp_allowed_now": False,
        "committing_ymmp_condition": (
            "not allowed unless a later explicit result-readback slice approves it"
        ),
    }


def _forbidden_actions() -> dict[str, bool]:
    return {
        "Agent_YMM4_launch": False,
        "Agent_ymmp_creation": False,
        "render": False,
        "TTS_generation": False,
        "real_media_import": False,
        "production_approval": False,
        "public_video_claim": False,
        "external_fetch": False,
        "real_newsroom_ingest": False,
    }


def _operator_observation_card() -> dict[str, Any]:
    return {
        "status": "required_later",
        "target": "diagnostic .ymmp probe from bound speaker CSV",
        "why": (
            "Confirm whether YMM4 can save the imported 4-line script as a "
            "project without render, TTS, real media, or production flow."
        ),
        "action": (
            "Manually import the bound CSV in YMM4 and, only if comfortable, "
            "save a diagnostic .ymmp outside production flow."
        ),
        "look_for": [
            "4 dialogue rows remain after save/reopen or save observation",
            f"speaker remains {OBSERVED_MANUAL_CHARACTER}",
            "timing stays natural short duration or changes unexpectedly",
        ],
        "answer_style": "freeform",
        "answer_hint": (
            "One sentence is enough, for example: saved; 4 rows and speaker "
            "remained; timing stayed short."
        ),
        "not_needed": [
            "render",
            "TTS",
            "real media",
            "production approval",
            "fixed form",
            "screenshot unless useful",
        ],
    }


def _agent_normalization_plan() -> dict[str, Any]:
    return {
        "schema_owner": "Agent",
        "exposed_as_user_form": False,
        "fields": [
            "result",
            "ymmp_saved",
            "row_count_observed",
            "speaker_preserved",
            "timing_observation",
            "render_created",
            "TTS_generated",
            "media_imported",
            "confidence",
            "unknowns",
        ],
        "normalization_note": (
            "The agent may infer these fields later from freeform user text; "
            "the user is not asked to fill this schema."
        ),
    }


def _timing_policy(boundary_decision: dict[str, Any]) -> dict[str, Any]:
    source_timing = _dict(boundary_decision.get("timing_gap_policy"))
    return {
        "neutral_timeline_total_sec": source_timing.get(
            "neutral_timeline_total_sec"
        ),
        "observed_yym4_import_approx_sec": source_timing.get(
            "observed_yym4_import_approx_sec"
        ),
        "first_probe_expected_timing": "YMM4 natural duration",
        "timing_patch_in_this_probe": False,
        "reason": (
            "The first diagnostic .ymmp probe observes save/readback behavior. "
            "Timing patch strategy waits until project structure is known."
        ),
        "next_timing_axis": [
            "timing_gap_strategy",
            "optional ymmp_patch_strategy after project structure is known",
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
        "committed_ymmp_artifact": False,
    }


def _source_validation(
    boundary_decision: dict[str, Any],
    readiness: dict[str, Any],
    csv_readback: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    boundary = _dict(boundary_decision.get("ymmp_boundary"))
    if boundary_decision.get("decision_status") != "approved_for_next_probe_packet":
        errors.append("BOUNDARY_DECISION_NOT_APPROVED_FOR_NEXT_PROBE_PACKET")
    if boundary.get("agent_may_create_ymmp_now") is not False:
        errors.append("AGENT_MAY_CREATE_YMMP_NOW_NOT_FALSE")
    if boundary.get("user_manual_ymmp_probe_may_be_prepared_next") is not True:
        errors.append("USER_MANUAL_PROBE_NOT_ALLOWED_NEXT")
    if readiness.get("result") != "pass":
        errors.append("BOUND_SPEAKER_READINESS_NOT_PASS")
    if csv_readback.get("bom_verified") is not True:
        errors.append("BOUND_CSV_BOM_NOT_VERIFIED")
    if csv_readback.get("has_header") is not False:
        errors.append("BOUND_CSV_HEADER_PRESENT")
    if csv_readback.get("all_rows_two_columns") is not True:
        errors.append("BOUND_CSV_NOT_TWO_COLUMN")
    if csv_readback.get("row_count") != EXPECTED_MANUAL_IMPORT_ROW_COUNT:
        errors.append("BOUND_CSV_ROW_COUNT_NOT_4")

    rows = _list(csv_readback.get("rows"))
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
        "source_boundary_decision_id": boundary_decision.get("decision_id"),
        "source_boundary_decision_status": boundary_decision.get(
            "decision_status"
        ),
        "source_readiness_id": readiness.get("readback_id"),
        "source_readiness_result": readiness.get("result"),
        "bound_csv_bom_verified": csv_readback.get("bom_verified"),
        "bound_csv_has_header": csv_readback.get("has_header"),
        "bound_csv_all_rows_two_columns": csv_readback.get("all_rows_two_columns"),
        "bound_csv_row_count": csv_readback.get("row_count"),
        "all_rows_use_bound_speaker": all(
            check["speaker_matches_bound_value"] for check in row_checks
        ),
        "all_rows_have_text": all(check["text_non_empty"] for check in row_checks),
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
