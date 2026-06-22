"""Manual YMM4 import check packet for the tiny newsroom CSV.

This module defines a diagnostic-only handoff packet for a human/operator to
manually check the already committed tiny CSV in YMM4. It does not launch YMM4,
create projects, render, generate TTS/audio, import real media, fetch external
sources, or approve production use.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_tiny_importable_proof import (
    DEFAULT_TINY_IMPORT_CSV_PATH,
    DEFAULT_TINY_IMPORTABLE_PROOF_PATH,
    TINY_IMPORTABLE_PROOF_ID,
)


MANUAL_IMPORT_CHECK_PACKET_SCHEMA_VERSION = (
    "newsroom_yym4_manual_import_check_packet.v1"
)
MANUAL_IMPORT_RESULT_TEMPLATE_SCHEMA_VERSION = (
    "newsroom_yym4_manual_import_result_template.v1"
)
MANUAL_IMPORT_CHECK_PACKET_ID = (
    "newsroom_yym4_manual_import_check_packet_v1_2026_06_22"
)
MANUAL_IMPORT_RESULT_TEMPLATE_ID = (
    "newsroom_yym4_manual_import_result_template_v1_2026_06_22"
)
DEFAULT_MANUAL_IMPORT_CHECK_PACKET_PATH = Path(
    "samples/_probe/newsroom_handoff/yym4_manual_import_check_packet_v1.json"
)
DEFAULT_MANUAL_IMPORT_RESULT_TEMPLATE_PATH = Path(
    "samples/_probe/newsroom_handoff/yym4_manual_import_result_template_v1.json"
)
DEFAULT_MANUAL_IMPORT_CHECK_PACKET_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YYM4_MANUAL_IMPORT_CHECK_PACKET_V1_2026-06-22.md"
)

EXPECTED_MANUAL_IMPORT_ROW_COUNT = 4
TARGET_SURFACE_COLUMNS: tuple[str, ...] = ("speaker", "text")
ALLOWED_MANUAL_IMPORT_RESULTS: tuple[str, ...] = (
    "pass",
    "pass_with_warnings",
    "fail",
    "blocked_by_operator_uncertainty",
)
FAILURE_CATEGORIES: tuple[str, ...] = (
    "encoding_error",
    "header_or_column_mismatch",
    "speaker_binding_error",
    "text_import_error",
    "row_count_mismatch",
    "unsupported_csv_shape",
    "operator_menu_unknown",
    "unexpected_YMM4_behavior",
)
REQUIRED_EVIDENCE_FIELDS: tuple[str, ...] = (
    "screenshot_path_placeholder",
    "observed_line_count",
    "observed_speaker_behavior",
    "observed_text_behavior",
    "error_message",
    "operator_notes_freeform",
    "result",
)


def build_default_newsroom_yym4_manual_import_check_packet(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed manual import check packet from default artifacts."""
    base = Path(root) if root is not None else Path(".")
    tiny_proof = load_json_object(base / DEFAULT_TINY_IMPORTABLE_PROOF_PATH)
    csv_readback = read_tiny_script_import_csv(base / DEFAULT_TINY_IMPORT_CSV_PATH)
    return build_newsroom_yym4_manual_import_check_packet(
        tiny_proof,
        csv_readback=csv_readback,
        source_tiny_csv_path=DEFAULT_TINY_IMPORT_CSV_PATH,
        source_tiny_proof_path=DEFAULT_TINY_IMPORTABLE_PROOF_PATH,
        result_template_path=DEFAULT_MANUAL_IMPORT_RESULT_TEMPLATE_PATH,
    )


def build_default_newsroom_yym4_manual_import_result_template(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the blank operator result template paired to the check packet."""
    packet = build_default_newsroom_yym4_manual_import_check_packet(root=root)
    return build_newsroom_yym4_manual_import_result_template(
        packet,
        source_packet_path=DEFAULT_MANUAL_IMPORT_CHECK_PACKET_PATH,
    )


def read_tiny_script_import_csv(path: str | Path) -> dict[str, Any]:
    """Read the tiny script CSV and return a bounded target-artifact readback."""
    csv_path = Path(path)
    raw = csv_path.read_bytes()
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    row_objects = [
        {
            "row_number": index,
            "speaker": row[0] if len(row) > 0 else "",
            "text": row[1] if len(row) > 1 else "",
            "column_count": len(row),
        }
        for index, row in enumerate(rows, start=1)
    ]
    return {
        "path": _path_text(csv_path),
        "bom_verified": raw.startswith(b"\xef\xbb\xbf"),
        "row_count": len(rows),
        "all_rows_two_columns": all(len(row) == 2 for row in rows),
        "has_header": bool(rows and rows[0] == list(TARGET_SURFACE_COLUMNS)),
        "rows": row_objects,
    }


def build_newsroom_yym4_manual_import_check_packet(
    tiny_proof: dict[str, Any],
    *,
    csv_readback: dict[str, Any],
    source_tiny_csv_path: str | Path,
    source_tiny_proof_path: str | Path,
    result_template_path: str | Path,
    source_commit_or_status: str = "worktree_verified_before_generation",
) -> dict[str, Any]:
    """Build the YMM4 manual import check packet from the tiny proof."""
    proof_identity = _dict(tiny_proof.get("identity"))
    proof_schema = _dict(tiny_proof.get("import_artifact_schema"))
    target = _target_artifact(source_tiny_csv_path, proof_schema, csv_readback)
    safety_boundary = _safety_boundary()

    return {
        "artifact_id": MANUAL_IMPORT_CHECK_PACKET_ID,
        "packet_id": MANUAL_IMPORT_CHECK_PACKET_ID,
        "schema_version": MANUAL_IMPORT_CHECK_PACKET_SCHEMA_VERSION,
        "review_status": "ready_for_operator_manual_check",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "manual_check_status": "not_run",
        "identity": {
            "packet_id": MANUAL_IMPORT_CHECK_PACKET_ID,
            "source_tiny_csv_path": _path_text(source_tiny_csv_path),
            "source_tiny_proof_path": _path_text(source_tiny_proof_path),
            "source_tiny_proof_id": tiny_proof.get("proof_id"),
            "source_tiny_importable_status": tiny_proof.get(
                "tiny_importable_status"
            ),
            "source_episode_id": proof_identity.get("source_episode_id"),
            "source_commit_or_status": source_commit_or_status,
            "production_status": "diagnostic_only",
            "manual_check_status": "not_run",
        },
        "review_memory": {
            "prior_user_review_count": 0,
            "accepted_scope": [
                "diagnostic_script_import_candidate",
                "YMM4_adjacent_no_media_import_shape",
                "tiny_importable_artifact_shape",
            ],
            "not_accepted_scope": [
                "production YMM4 transfer",
                "production subtitle design",
                "production narration",
                ".ymmp",
                "render",
                "TTS/audio",
                "real media",
                "public video",
            ],
            "current_axis": "YMM4_manual_import_check_packet",
            "repeated_general_review_allowed": False,
        },
        "preconditions": _preconditions(),
        "target_artifact": target,
        "manual_procedure": _manual_procedure(source_tiny_csv_path),
        "expected_successful_observation": _expected_successful_observation(target),
        "failure_categories": _failure_categories(),
        "evidence_template": _evidence_template(),
        "result_recording_contract": {
            "result_template_path": _path_text(result_template_path),
            "required_fields": list(REQUIRED_EVIDENCE_FIELDS),
            "allowed_results": list(ALLOWED_MANUAL_IMPORT_RESULTS),
            "manual_check_status_before_operator_run": "not_run",
            "accepts_only_human_operator_observation": True,
            "no_agent_claim_of_YMM4_result_without_operator_evidence": True,
        },
        "next_actions_by_result": _next_actions_by_result(),
        "safety_boundary": safety_boundary,
        "validation": {
            "target_csv_bom_verified": target["encoding_verified"] is True,
            "target_csv_has_no_header": target["has_header"] is False,
            "target_csv_row_count_matches_expected": (
                target["observed_rows_before_manual_check"]
                == target["expected_rows"]
            ),
            "target_csv_all_rows_two_columns": bool(
                csv_readback.get("all_rows_two_columns")
            ),
            "source_tiny_proof_id_matches": (
                tiny_proof.get("proof_id") == TINY_IMPORTABLE_PROOF_ID
            ),
            "source_tiny_status": tiny_proof.get("tiny_importable_status"),
            "manual_check_not_run": True,
            "review_card_required": False,
        },
        "review_card": {
            "status": "none",
            "axis_if_needed": "YMM4_manual_import_check_packet",
            "reason": (
                "This slice only defines the manual check packet and result "
                "contract; no repeated timing, caption, CSV, script, "
                "YMM4-adjacent, tiny proof, render, TTS, media, or production "
                "approval review is needed."
            ),
        },
        "boundary_assertions": {
            **safety_boundary,
            "agent_import_observation_claimed": False,
            "external_fetch_performed": False,
            "dashboard_governance_freshness_changed": False,
            "real_newsroom_ingest_performed": False,
        },
    }


def build_newsroom_yym4_manual_import_result_template(
    packet: dict[str, Any],
    *,
    source_packet_path: str | Path,
) -> dict[str, Any]:
    """Build a blank result template for the human/operator manual check."""
    identity = _dict(packet.get("identity"))
    return {
        "artifact_id": MANUAL_IMPORT_RESULT_TEMPLATE_ID,
        "template_id": MANUAL_IMPORT_RESULT_TEMPLATE_ID,
        "schema_version": MANUAL_IMPORT_RESULT_TEMPLATE_SCHEMA_VERSION,
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "manual_check_status": "not_run",
        "packet_id": packet.get("packet_id"),
        "source_packet_path": _path_text(source_packet_path),
        "source_tiny_csv_path": identity.get("source_tiny_csv_path"),
        "source_tiny_proof_path": identity.get("source_tiny_proof_path"),
        "required_fields": list(REQUIRED_EVIDENCE_FIELDS),
        "allowed_results": list(ALLOWED_MANUAL_IMPORT_RESULTS),
        "evidence_template": _evidence_template(),
        "failure_categories": list(FAILURE_CATEGORIES),
        "next_actions_by_result": _next_actions_by_result(),
        "safety_boundary": _safety_boundary(),
        "operator_fill_contract": {
            "fill_after_human_operator_manual_run_only": True,
            "leave_result_null_until_observed": True,
            "do_not_commit_experimental_ymmp_without_later_slice": True,
            "do_not_record_render_TTS_or_media_as_part_of_this_template": True,
            "record_operator_uncertainty_as_blocked_by_operator_uncertainty": True,
        },
    }


def render_newsroom_yym4_manual_import_check_packet_markdown(
    packet: dict[str, Any],
    result_template: dict[str, Any] | None = None,
) -> str:
    """Render a human-readable manual import check packet."""
    identity = _dict(packet.get("identity"))
    target = _dict(packet.get("target_artifact"))
    expected = _dict(packet.get("expected_successful_observation"))
    contract = _dict(packet.get("result_recording_contract"))
    safety = _dict(packet.get("safety_boundary"))
    template_path = contract.get("result_template_path")
    if result_template is not None:
        template_path = result_template.get("source_packet_path") and contract.get(
            "result_template_path"
        )

    lines = [
        "# Newsroom YMM4 Manual Import Check Packet v1",
        "",
        f"artifact_id: {packet.get('artifact_id')}",
        f"packet_id: {packet.get('packet_id')}",
        f"schema_version: {packet.get('schema_version')}",
        f"review_status: {packet.get('review_status')}",
        f"production_status: {packet.get('production_status')}",
        f"manual_check_status: {packet.get('manual_check_status')}",
        "diagnostic_only: true",
        "",
        "## Source and Target",
        "",
        f"- source_tiny_csv_path: {identity.get('source_tiny_csv_path')}",
        f"- source_tiny_proof_path: {identity.get('source_tiny_proof_path')}",
        f"- source_tiny_proof_id: {identity.get('source_tiny_proof_id')}",
        f"- source_tiny_importable_status: {identity.get('source_tiny_importable_status')}",
        f"- target filename: {target.get('filename')}",
        f"- target surface: {', '.join(target.get('surface', []))}",
        f"- encoding: {target.get('encoding')} (verified: {str(target.get('encoding_verified')).lower()})",
        f"- has_header: {str(target.get('has_header')).lower()}",
        f"- expected_rows: {target.get('expected_rows')}",
        f"- observed_rows_before_manual_check: {target.get('observed_rows_before_manual_check')}",
        "",
        "## Preconditions",
        "",
    ]
    for item in _list(packet.get("preconditions", {}).get("items")):
        lines.append(f"- {item['requirement']}")

    lines.extend([
        "",
        "## Manual Procedure",
        "",
    ])
    for step in _list(packet.get("manual_procedure")):
        lines.append(f"{step['step']}. {step['action']}")

    lines.extend([
        "",
        "## Expected Successful Observation",
        "",
        f"- imported_line_count: {expected.get('imported_line_count')}",
        f"- speaker_placeholder_behavior: {expected.get('speaker_placeholder_behavior')}",
        f"- text_behavior: {expected.get('text_behavior')}",
        f"- timing_import_expected: {str(expected.get('timing_import_expected')).lower()}",
        f"- audio_media_render_expected: {str(expected.get('audio_media_render_expected')).lower()}",
        "",
        "## Failure Categories",
        "",
        "| category | when to use |",
        "|---|---|",
    ])
    for category in _list(packet.get("failure_categories")):
        lines.append(f"| {category['category']} | {category['meaning']} |")

    lines.extend([
        "",
        "## Evidence Template",
        "",
    ])
    evidence = _dict(packet.get("evidence_template"))
    for field in REQUIRED_EVIDENCE_FIELDS:
        value = evidence.get(field)
        if value == "":
            value = '""'
        lines.append(f"- {field}: {value}")
    lines.append(
        f"- allowed_results: {', '.join(packet.get('result_recording_contract', {}).get('allowed_results', []))}"
    )
    lines.append(f"- result_template_path: {template_path}")

    lines.extend([
        "",
        "## Next Actions",
        "",
        "| observed result | next action |",
        "|---|---|",
    ])
    for result, action in _next_actions_by_result().items():
        lines.append(f"| {result} | {action} |")

    lines.extend([
        "",
        "## Safety Boundary",
        "",
        f"- ymmp_created_by_agent: {str(safety.get('ymmp_created_by_agent')).lower()}",
        f"- YMM4_launched_by_agent: {str(safety.get('YMM4_launched_by_agent')).lower()}",
        f"- render_created: {str(safety.get('render_created')).lower()}",
        f"- TTS_generated: {str(safety.get('TTS_generated')).lower()}",
        f"- real_media_imported: {str(safety.get('real_media_imported')).lower()}",
        f"- production_approval: {str(safety.get('production_approval')).lower()}",
        f"- public_video_ready: {str(safety.get('public_video_ready')).lower()}",
        "",
        "## Review Card",
        "",
        "Review Card: none. This packet only records the manual import-check "
        "contract and does not ask for repeated timing, caption, copy, blocker, "
        "neutral timeline, CSV, script, YMM4-adjacent, tiny proof, render, TTS, "
        "media, or production review.",
        "",
        "## Boundary",
        "",
        "This check packet is diagnostic-only. The agent did not launch YMM4, "
        "create `.ymmp`, create a carrier, render, generate TTS/audio, import "
        "real media, ingest a real newsroom packet, fetch external sources, or "
        "approve production/public video use. If YMM4 cannot show the four "
        "manual-check rows without crossing those boundaries, the operator "
        "should record `blocked_by_operator_uncertainty` instead of continuing.",
        "",
    ])
    return "\n".join(lines)


def _target_artifact(
    source_tiny_csv_path: str | Path,
    proof_schema: dict[str, Any],
    csv_readback: dict[str, Any],
) -> dict[str, Any]:
    rows = _list(csv_readback.get("rows"))
    return {
        "path": _path_text(source_tiny_csv_path),
        "filename": Path(source_tiny_csv_path).name,
        "artifact_role": "manual_import_check_target",
        "encoding": "utf-8-sig",
        "encoding_verified": (
            bool(csv_readback.get("bom_verified"))
            and proof_schema.get("encoding") == "utf-8-sig"
        ),
        "encoding_verification": {
            "bom_verified": bool(csv_readback.get("bom_verified")),
            "tiny_proof_schema_encoding": proof_schema.get("encoding"),
            "readback_encoding": "utf-8-sig",
        },
        "has_header": bool(csv_readback.get("has_header")),
        "header_expectation": "no_header",
        "surface": list(TARGET_SURFACE_COLUMNS),
        "expected_rows": EXPECTED_MANUAL_IMPORT_ROW_COUNT,
        "observed_rows_before_manual_check": csv_readback.get("row_count"),
        "all_rows_two_columns": bool(csv_readback.get("all_rows_two_columns")),
        "timing_columns_expected": False,
        "production_ready_flags_expected": False,
        "diagnostic_only": True,
        "synthetic_only": True,
        "rows": [
            {
                "row_number": row.get("row_number"),
                "speaker": row.get("speaker"),
                "text": row.get("text"),
            }
            for row in rows
        ],
    }


def _preconditions() -> dict[str, Any]:
    return {
        "items": [
            {
                "requirement": (
                    "YMM4 is opened manually by the user/operator only; the "
                    "agent does not launch or automate YMM4."
                ),
                "required": True,
            },
            {
                "requirement": (
                    "Use no production project, no render, no TTS/audio, and "
                    "no real media during this check."
                ),
                "required": True,
            },
            {
                "requirement": (
                    "Do not commit any `.ymmp` produced by manual "
                    "experimentation unless a later explicit slice requests it."
                ),
                "required": True,
            },
            {
                "requirement": (
                    "Treat the tiny CSV as synthetic diagnostic-only data, not "
                    "as production newsroom content."
                ),
                "required": True,
            },
            {
                "requirement": (
                    "If the available YMM4 flow necessarily generates voice, "
                    "audio, media, render output, or a production project, stop "
                    "and record blocked_by_operator_uncertainty."
                ),
                "required": True,
            },
        ],
        "YMM4_manual_open_only": True,
        "no_production_project": True,
        "no_render": True,
        "no_TTS": True,
        "no_real_media": True,
        "do_not_commit_experimental_ymmp": True,
        "tiny_csv_synthetic_diagnostic_only": True,
    }


def _manual_procedure(source_tiny_csv_path: str | Path) -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "action": (
                "Locate the committed target CSV: "
                f"{_path_text(source_tiny_csv_path)}."
            ),
        },
        {
            "step": 2,
            "action": "Open YMM4 manually as the user/operator, not via this agent.",
        },
        {
            "step": 3,
            "action": (
                "Use the repo-documented YMM4 script import / 台本読み込み "
                "function: ツール -> 台本読み込み. If the operator's YMM4 "
                "version differs, record operator_menu_unknown rather than "
                "inventing alternate menu names."
            ),
        },
        {
            "step": 4,
            "action": (
                "Select CSV import settings matching the repo contract when "
                "YMM4 exposes them: UTF-8 BOM / utf-8-sig, comma-delimited, "
                "headerless, two columns: speaker,text."
            ),
        },
        {
            "step": 5,
            "action": (
                "Import the CSV only far enough to observe the script rows or "
                "import preview; do not proceed into render, TTS/audio, real "
                "media, or production save flows."
            ),
        },
        {
            "step": 6,
            "action": "Observe whether exactly 4 lines/rows appear.",
        },
        {
            "step": 7,
            "action": (
                "If screenshot-only operator evidence is needed, record a "
                "placeholder path in the result template; do not save a "
                "production project."
            ),
        },
        {
            "step": 8,
            "action": "Close without render and without committing any `.ymmp`.",
        },
    ]


def _expected_successful_observation(target: dict[str, Any]) -> dict[str, Any]:
    return {
        "imported_line_count": EXPECTED_MANUAL_IMPORT_ROW_COUNT,
        "speaker_placeholder_behavior": (
            "synthetic_newsroom_placeholder appears as a speaker placeholder "
            "or is safely unmapped/manual-bindable without data loss"
        ),
        "text_behavior": "all 4 target CSV texts appear in order",
        "expected_texts": [row.get("text") for row in _list(target.get("rows"))],
        "timing_import_expected": False,
        "audio_media_render_expected": False,
        "audio_expected": False,
        "media_expected": False,
        "render_expected": False,
    }


def _failure_categories() -> list[dict[str, str]]:
    meanings = {
        "encoding_error": "CSV cannot be read as the expected UTF-8 BOM text.",
        "header_or_column_mismatch": (
            "YMM4 treats the file as having the wrong header or column count."
        ),
        "speaker_binding_error": (
            "The synthetic speaker placeholder cannot appear, stay unmapped, "
            "or be manually bound safely."
        ),
        "text_import_error": "One or more of the 4 diagnostic texts is missing or altered.",
        "row_count_mismatch": "YMM4 does not show exactly 4 lines/rows.",
        "unsupported_csv_shape": (
            "YMM4 rejects the two-column headerless speaker,text CSV shape."
        ),
        "operator_menu_unknown": (
            "The operator cannot locate the YMM4 script import / 台本読み込み function."
        ),
        "unexpected_YMM4_behavior": (
            "YMM4 behavior crosses or threatens the diagnostic boundary."
        ),
    }
    return [
        {
            "category": category,
            "meaning": meanings[category],
        }
        for category in FAILURE_CATEGORIES
    ]


def _evidence_template() -> dict[str, Any]:
    return {
        "screenshot_path_placeholder": "operator_screenshot_path_placeholder",
        "observed_line_count": None,
        "observed_speaker_behavior": None,
        "observed_text_behavior": None,
        "error_message": None,
        "operator_notes_freeform": "",
        "result": None,
        "allowed_results": list(ALLOWED_MANUAL_IMPORT_RESULTS),
    }


def _next_actions_by_result() -> dict[str, str]:
    return {
        "pass": (
            "Create a result readback and consider a tiny YMM4 import-readiness proof."
        ),
        "pass_with_warnings": (
            "Classify warnings before changing the CSV or expanding the pipeline."
        ),
        "fail": "Adjust CSV shape or encoding in a bounded follow-up slice.",
        "blocked_by_operator_uncertainty": (
            "Improve manual instructions, not the pipeline."
        ),
    }


def _safety_boundary() -> dict[str, bool]:
    return {
        "ymmp_created_by_agent": False,
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
