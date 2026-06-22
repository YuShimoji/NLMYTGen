"""Record the human/operator YMM4 manual import result readback.

This module records operator-provided evidence for the already committed tiny
CSV import check. It does not launch YMM4, create or edit projects, render,
generate TTS/audio, import real media, or approve production use.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_tiny_importable_proof import DEFAULT_TINY_IMPORT_CSV_PATH
from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    DEFAULT_MANUAL_IMPORT_CHECK_PACKET_PATH,
    DEFAULT_MANUAL_IMPORT_RESULT_TEMPLATE_PATH,
    EXPECTED_MANUAL_IMPORT_ROW_COUNT,
    read_tiny_script_import_csv,
)


MANUAL_IMPORT_RESULT_SCHEMA_VERSION = (
    "newsroom_yym4_manual_import_result_readback.v1"
)
MANUAL_IMPORT_RESULT_ID = (
    "newsroom_yym4_manual_import_result_readback_v1_2026_06_23"
)
DEFAULT_MANUAL_IMPORT_RESULT_PATH = Path(
    "samples/_probe/newsroom_handoff/yym4_manual_import_result_readback_v1.json"
)
DEFAULT_MANUAL_IMPORT_RESULT_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YYM4_MANUAL_IMPORT_RESULT_READBACK_V1_2026-06-23.md"
)


OPERATOR_MANUAL_IMPORT_RESULT_V1: dict[str, Any] = {
    "result": "pass_with_warnings",
    "target_csv": "samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv",
    "observed_line_count": 4,
    "expected_line_count": 4,
    "all_text_visible": "yes",
    "speaker_behavior": "mapped_after_manual_selection",
    "selected_speaker_or_character": "ゆっくり霊夢",
    "encoding_or_text_issues": "no",
    "header_or_column_issues": "no",
    "error_message": "none",
    "screenshot_reference": "provided_in_supervisor_thread",
    "operator_notes_freeform": (
        "YMM4 requested speaker/character selection; existing ゆっくり霊夢 was "
        "selected and import succeeded; 4 dialogue items were visible in YMM4."
    ),
    "did_not_render": "yes",
    "did_not_generate_tts": "operator_did_not_explicitly_generate_tts",
    "did_not_import_real_media": "yes",
    "did_not_commit_ymmp": "yes",
}


def build_default_newsroom_yym4_manual_import_result(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed result readback from default artifacts."""
    base = Path(root) if root is not None else Path(".")
    packet = load_json_object(base / DEFAULT_MANUAL_IMPORT_CHECK_PACKET_PATH)
    template = load_json_object(base / DEFAULT_MANUAL_IMPORT_RESULT_TEMPLATE_PATH)
    csv_readback = read_tiny_script_import_csv(base / DEFAULT_TINY_IMPORT_CSV_PATH)
    return build_newsroom_yym4_manual_import_result(
        OPERATOR_MANUAL_IMPORT_RESULT_V1,
        packet,
        template,
        csv_readback=csv_readback,
        source_packet_path=DEFAULT_MANUAL_IMPORT_CHECK_PACKET_PATH,
        source_template_path=DEFAULT_MANUAL_IMPORT_RESULT_TEMPLATE_PATH,
        source_tiny_csv_path=DEFAULT_TINY_IMPORT_CSV_PATH,
    )


def build_newsroom_yym4_manual_import_result(
    operator_result: dict[str, Any],
    packet: dict[str, Any],
    result_template: dict[str, Any],
    *,
    csv_readback: dict[str, Any],
    source_packet_path: str | Path,
    source_template_path: str | Path,
    source_tiny_csv_path: str | Path,
) -> dict[str, Any]:
    """Build a diagnostic result readback from human/operator observations."""
    observation = _normalized_observation(operator_result)
    accepted_scope = _accepted_scope()
    not_accepted_scope = _not_accepted_scope()
    safety = _safety_boundary(operator_result)
    warning_classification = _warning_classification()
    result = str(operator_result.get("result"))
    source_packet_path_text = _path_text(source_packet_path)
    target_csv_path_text = _path_text(source_tiny_csv_path)

    return {
        "artifact_id": MANUAL_IMPORT_RESULT_ID,
        "result_id": MANUAL_IMPORT_RESULT_ID,
        "schema_version": MANUAL_IMPORT_RESULT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "manual_check_status": "observed",
        "result": result,
        "source_packet_path": source_packet_path_text,
        "target_csv_path": target_csv_path_text,
        "source": {
            "source_packet_path": source_packet_path_text,
            "source_template_path": _path_text(source_template_path),
            "target_csv_path": target_csv_path_text,
            "packet_id": packet.get("packet_id"),
            "template_id": result_template.get("template_id"),
            "manual_check_status_before_result": packet.get("manual_check_status"),
        },
        "review_memory": {
            "review_source": "user_freeform_manual_import_result",
            "prior_user_review_count": 1,
            "accepted_scope": accepted_scope,
            "not_accepted_scope": not_accepted_scope,
            "next_nonredundant_axis": [
                "speaker_binding_policy",
                "YMM4_import_readiness_after_manual_result",
                "minimal_ymmp_boundary_decision",
            ],
            "repeated_general_review_allowed": False,
        },
        "operator_result": {
            **operator_result,
            "normalized_result": result,
            "screenshot_path_or_none": "provided_in_supervisor_thread",
        },
        "observation": observation,
        "safety": safety,
        "warning_classification": warning_classification,
        "accepted_scope": accepted_scope,
        "not_accepted_scope": not_accepted_scope,
        "recommended_next_slices": [
            "newsroom-speaker-binding-policy-v1",
            "newsroom-yym4-import-readiness-after-manual-result-v1",
            "newsroom-minimal-ymmp-boundary-decision-v1",
        ],
        "result_classification": {
            "result": result,
            "line_count_matches": observation["observed_line_count"]
            == observation["expected_line_count"]
            == EXPECTED_MANUAL_IMPORT_ROW_COUNT,
            "text_import_passed": _passed_text_import(observation),
            "speaker_required_manual_selection": (
                observation["speaker_behavior"] == "mapped_after_manual_selection"
            ),
            "selected_speaker_or_character": observation[
                "selected_speaker_or_character"
            ],
            "primary_warning_id": "manual_speaker_binding_required",
            "warnings": [warning["warning_id"] for warning in warning_classification],
            "blocking_failures": [],
            "classification_summary": (
                "Tiny speaker,text CSV import was observed in YMM4 with all four "
                "rows visible, but speaker binding required manual selection. "
                "This is not production, render, TTS, .ymmp, or public-video "
                "approval."
            ),
        },
        "target_csv_readback": {
            "path": target_csv_path_text,
            "bom_verified": csv_readback.get("bom_verified"),
            "row_count": csv_readback.get("row_count"),
            "all_rows_two_columns": csv_readback.get("all_rows_two_columns"),
            "has_header": csv_readback.get("has_header"),
            "rows": csv_readback.get("rows"),
        },
        "readiness_delta": {
            "manual_check_before": packet.get("manual_check_status"),
            "manual_check_after": "observed_pass_with_warnings",
            "tiny_csv_text_import_observed": True,
            "speaker_mapping_observed_after_manual_selection": True,
            "automatic_speaker_binding_observed": False,
            "timing_import_observed": False,
            "explicit_tts_generation_by_operator": False,
            "render_observed": False,
            "real_media_import_observed": False,
            "ymmp_committed": False,
            "transfer_status": "blocked",
            "production_status": "diagnostic_only",
            "public_video_ready": False,
        },
        "next_actions_by_classification": {
            "recommended_next": (
                "Use this readback to decide speaker-binding policy or a bounded "
                "YMM4 import-readiness follow-up. Do not re-request general "
                "timing/caption/copy/tiny-proof review."
            ),
            "allowed": [
                "speaker-binding policy slice",
                "YMM4 import-readiness after manual result slice",
                "minimal .ymmp boundary decision slice",
            ],
            "prohibited": [
                ".ymmp generation",
                "render generation",
                "TTS/audio generation",
                "real media import",
                "production approval",
                "publishing",
            ],
        },
        "review_card": {
            "status": "warnings_only",
            "fixed_phrase_required": False,
            "warnings": warning_classification,
            "review_debt": [
                "Speaker/character binding is manual, not automatic.",
                "The operator did not explicitly perform a separate TTS generation.",
            ],
        },
        "safety_boundary": {
            **safety,
            "agent_launched_yym4": False,
            "agent_created_or_edited_ymmp": False,
            "agent_rendered_media": False,
            "agent_generated_tts": False,
            "dashboard_governance_freshness_changed": False,
            "external_fetch_performed": False,
        },
        "boundary_assertions": {
            **safety,
            "agent_launched_yym4": False,
            "agent_created_or_edited_ymmp": False,
            "agent_rendered_media": False,
            "agent_generated_tts": False,
            "dashboard_governance_freshness_changed": False,
            "external_fetch_performed": False,
        },
    }


def render_newsroom_yym4_manual_import_result_markdown(
    result: dict[str, Any],
) -> str:
    """Render a human-readable manual import result readback."""
    observation = _dict(result.get("observation"))
    source = _dict(result.get("source"))
    classification = _dict(result.get("result_classification"))
    safety = _dict(result.get("safety"))
    review_memory = _dict(result.get("review_memory"))

    lines = [
        "# Newsroom YMM4 Manual Import Result Readback v1",
        "",
        f"artifact_id: {result.get('artifact_id')}",
        f"schema_version: {result.get('schema_version')}",
        f"review_status: {result.get('review_status')}",
        f"manual_check_status: {result.get('manual_check_status')}",
        f"result: {result.get('result')}",
        "diagnostic_only: true",
        "production_status: diagnostic_only",
        "",
        "## Source",
        "",
        f"- source_packet_path: {source.get('source_packet_path')}",
        f"- source_template_path: {source.get('source_template_path')}",
        f"- target_csv_path: {source.get('target_csv_path')}",
        f"- packet_id: {source.get('packet_id')}",
        "",
        "## Manual Observation",
        "",
        f"- observed_line_count: {observation.get('observed_line_count')}",
        f"- expected_line_count: {observation.get('expected_line_count')}",
        f"- all_text_visible: {str(observation.get('all_text_visible')).lower()}",
        f"- speaker_behavior: {observation.get('speaker_behavior')}",
        (
            "- selected_speaker_or_character: "
            f"{observation.get('selected_speaker_or_character')}"
        ),
        (
            "- encoding_or_text_issues: "
            f"{str(observation.get('encoding_or_text_issues')).lower()}"
        ),
        (
            "- header_or_column_issues: "
            f"{str(observation.get('header_or_column_issues')).lower()}"
        ),
        (
            "- error_message: "
            f"{observation.get('error_message') if observation.get('error_message') is not None else 'null'}"
        ),
        f"- screenshot_reference: {observation.get('screenshot_reference')}",
        "",
        "## Warning Classification",
        "",
    ]
    for warning in result.get("warning_classification", []):
        lines.extend(
            [
                f"- warning_id: {warning.get('warning_id')}",
                f"  severity: {warning.get('severity')}",
                f"  meaning: {warning.get('meaning')}",
                f"  next_axis: {warning.get('next_axis')}",
            ]
        )

    lines.extend(
        [
            "",
            "## Classification",
            "",
            f"- result: {classification.get('result')}",
            (
                "- line_count_matches: "
                f"{str(classification.get('line_count_matches')).lower()}"
            ),
            (
                "- text_import_passed: "
                f"{str(classification.get('text_import_passed')).lower()}"
            ),
            (
                "- speaker_required_manual_selection: "
                f"{str(classification.get('speaker_required_manual_selection')).lower()}"
            ),
            f"- transfer_status: {result.get('readiness_delta', {}).get('transfer_status')}",
            f"- public_video_ready: {str(result.get('readiness_delta', {}).get('public_video_ready')).lower()}",
            "",
            "## Accepted Scope",
            "",
        ]
    )
    for key, value in result.get("accepted_scope", {}).items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in result.get("not_accepted_scope", {}).items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(["", "## Safety Boundary", ""])
    for key, value in safety.items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(
        [
            "",
            "## Review Memory",
            "",
            f"- prior_user_review_count: {review_memory.get('prior_user_review_count')}",
            (
                "- repeated_general_review_allowed: "
                f"{str(review_memory.get('repeated_general_review_allowed')).lower()}"
            ),
            "- next_nonredundant_axis:",
        ]
    )
    for axis in review_memory.get("next_nonredundant_axis", []):
        lines.append(f"  - {axis}")

    lines.extend(
        [
            "",
            "## Recommended Next Slices",
            "",
        ]
    )
    for next_slice in result.get("recommended_next_slices", []):
        lines.append(f"- {next_slice}")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This readback records a human/operator observation only. It does not "
            "prove production readiness, automatic speaker binding, TTS readiness, "
            ".ymmp readiness, render readiness, YMM4 transfer approval, or public "
            "video readiness.",
            "",
        ]
    )
    return "\n".join(lines)


def _normalized_observation(operator_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "observed_line_count": operator_result.get("observed_line_count"),
        "expected_line_count": operator_result.get("expected_line_count"),
        "all_text_visible": operator_result.get("all_text_visible") == "yes",
        "speaker_behavior": operator_result.get("speaker_behavior"),
        "selected_speaker_or_character": operator_result.get(
            "selected_speaker_or_character"
        ),
        "encoding_or_text_issues": operator_result.get("encoding_or_text_issues")
        != "no",
        "header_or_column_issues": operator_result.get("header_or_column_issues")
        != "no",
        "error_message": None
        if operator_result.get("error_message") == "none"
        else operator_result.get("error_message"),
        "screenshot_reference": operator_result.get("screenshot_reference"),
        "operator_notes_freeform": operator_result.get("operator_notes_freeform"),
    }


def _safety_boundary(operator_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "render_created": False,
        "explicit_tts_generation_by_operator": False,
        "did_not_generate_tts_interpretation": operator_result.get(
            "did_not_generate_tts"
        ),
        "real_media_imported": False,
        "ymmp_committed": False,
        "production_approval": False,
        "public_video_ready": False,
    }


def _warning_classification() -> list[dict[str, str]]:
    return [
        {
            "warning_id": "manual_speaker_binding_required",
            "severity": "medium",
            "meaning": (
                "YMM4 accepted rows/text but required manual binding to an "
                "existing character."
            ),
            "next_axis": "speaker_binding_policy",
        },
        {
            "warning_id": "operator_tts_generation_not_explicitly_confirmed",
            "severity": "low",
            "meaning": (
                "The operator did not explicitly perform a separate TTS "
                "generation; no TTS readiness is implied."
            ),
            "next_axis": "YMM4_import_readiness_after_manual_result",
        },
    ]


def _accepted_scope() -> dict[str, bool]:
    return {
        "tiny_csv_shape_observed_in_YMM4": True,
        "row_text_import_observed": True,
        "manual_speaker_binding_observed": True,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "automatic_speaker_binding": False,
        "TTS_ready": False,
        "render_ready": False,
        "production_ready": False,
        "YMM4_project_ready": False,
        "production_subtitle_design": False,
        "production_narration": False,
        "public_video": False,
    }


def _passed_text_import(observation: dict[str, Any]) -> bool:
    return (
        observation.get("observed_line_count") == EXPECTED_MANUAL_IMPORT_ROW_COUNT
        and observation.get("expected_line_count") == EXPECTED_MANUAL_IMPORT_ROW_COUNT
        and observation.get("all_text_visible") is True
        and observation.get("encoding_or_text_issues") is False
        and observation.get("header_or_column_issues") is False
        and observation.get("error_message") is None
    )


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None
