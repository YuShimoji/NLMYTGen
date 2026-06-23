"""Speaker binding policy for the diagnostic newsroom YMM4 import.

This module uses the observed manual import result to define a bounded speaker
binding policy and an optional next-check CSV candidate. It does not launch
YMM4, create or edit projects, render, generate TTS/audio, import real media,
fetch external sources, or approve production use.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_tiny_importable_proof import DEFAULT_TINY_IMPORT_CSV_PATH
from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    EXPECTED_MANUAL_IMPORT_ROW_COUNT,
    TARGET_SURFACE_COLUMNS,
    read_tiny_script_import_csv,
)
from src.pipeline.newsroom_yym4_manual_import_result import (
    DEFAULT_MANUAL_IMPORT_RESULT_PATH,
)


SPEAKER_BINDING_POLICY_SCHEMA_VERSION = "newsroom_yym4_speaker_binding_policy.v1"
SPEAKER_BINDING_POLICY_ID = (
    "newsroom_yym4_speaker_binding_policy_v1_2026_06_23"
)
DEFAULT_SPEAKER_BINDING_POLICY_PATH = Path(
    "samples/_probe/newsroom_handoff/yym4_speaker_binding_policy_v1.json"
)
DEFAULT_BOUND_SPEAKER_CSV_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "tiny_script_import_candidate_yukkuri_reimu_v1.csv"
)
DEFAULT_SPEAKER_BINDING_POLICY_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YYM4_SPEAKER_BINDING_POLICY_V1_2026-06-23.md"
)

SOURCE_PLACEHOLDER_SPEAKER = "synthetic_newsroom_placeholder"
OBSERVED_MANUAL_CHARACTER = "ゆっくり霊夢"
POLICY_STATUS_VALUES: tuple[str, ...] = (
    "proposed",
    "diagnostic_candidate",
    "accepted_for_next_manual_check",
    "blocked",
)
BINDING_MODES: tuple[str, ...] = (
    "keep_placeholder_and_require_manual_selection",
    "emit_existing_yym4_character_name",
    "maintain_metadata_mapping_only",
)


def build_default_newsroom_yym4_speaker_binding_policy(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed speaker binding policy from default artifacts."""
    base = Path(root) if root is not None else Path(".")
    manual_result = load_json_object(base / DEFAULT_MANUAL_IMPORT_RESULT_PATH)
    source_csv_readback = read_tiny_script_import_csv(
        base / DEFAULT_TINY_IMPORT_CSV_PATH
    )
    return build_newsroom_yym4_speaker_binding_policy(
        manual_result,
        source_csv_readback=source_csv_readback,
        source_manual_result_path=DEFAULT_MANUAL_IMPORT_RESULT_PATH,
        source_tiny_csv_path=DEFAULT_TINY_IMPORT_CSV_PATH,
        bound_csv_candidate_path=DEFAULT_BOUND_SPEAKER_CSV_PATH,
    )


def build_newsroom_yym4_speaker_binding_policy(
    manual_result: dict[str, Any],
    *,
    source_csv_readback: dict[str, Any],
    source_manual_result_path: str | Path,
    source_tiny_csv_path: str | Path,
    bound_csv_candidate_path: str | Path,
    source_commit_or_status: str = "worktree_verified_before_generation",
) -> dict[str, Any]:
    """Build a diagnostic speaker binding policy and bound CSV candidate."""
    observation = _dict(manual_result.get("observation"))
    review_memory = _dict(manual_result.get("review_memory"))
    source_rows = _list(source_csv_readback.get("rows"))
    candidate_rows = _bound_candidate_rows(source_rows)
    source_validation = _source_validation(
        manual_result,
        source_csv_readback,
        observation=observation,
    )
    candidate_validation = _candidate_validation(source_rows, candidate_rows)
    safety_boundary = _safety_boundary()
    policy_status = (
        "diagnostic_candidate"
        if not source_validation["errors"] and not candidate_validation["errors"]
        else "blocked"
    )

    return {
        "artifact_id": SPEAKER_BINDING_POLICY_ID,
        "policy_id": SPEAKER_BINDING_POLICY_ID,
        "schema_version": SPEAKER_BINDING_POLICY_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "policy_status": policy_status,
        "identity": {
            "policy_id": SPEAKER_BINDING_POLICY_ID,
            "source_manual_result_path": _path_text(source_manual_result_path),
            "source_manual_result_id": manual_result.get("result_id"),
            "source_tiny_csv_path": _path_text(source_tiny_csv_path),
            "source_commit_or_status": source_commit_or_status,
            "production_status": "diagnostic_only",
            "policy_status": policy_status,
            "allowed_policy_status_values": list(POLICY_STATUS_VALUES),
        },
        "review_memory": {
            "review_source": "manual_import_result_readback",
            "prior_user_review_count": review_memory.get(
                "prior_user_review_count",
                1,
            ),
            "accepted_scope": {
                "tiny_speaker_text_csv_accepted_by_YMM4_manual_import": True,
                "four_dialogue_rows_visible": True,
                "all_text_visible": True,
                "manual_speaker_binding_observed": True,
            },
            "not_accepted_scope": _not_accepted_scope(),
            "next_nonredundant_axis": [
                "speaker_binding_policy",
                "placeholder_to_yym4_character_mapping",
                "bound_speaker_csv_candidate",
            ],
            "repeated_general_review_allowed": False,
        },
        "observed_binding": {
            "source_placeholder_speaker": SOURCE_PLACEHOLDER_SPEAKER,
            "observed_manual_character": OBSERVED_MANUAL_CHARACTER,
            "observed_behavior": "manual_selection_required",
            "source_manual_result_behavior": observation.get("speaker_behavior"),
            "import_result": manual_result.get("result"),
            "automatic_binding_observed": False,
            "manual_selection_succeeded": True,
            "observed_line_count": observation.get("observed_line_count"),
            "expected_line_count": observation.get("expected_line_count"),
            "all_text_visible": observation.get("all_text_visible"),
            "primary_warning_id": "manual_speaker_binding_required",
        },
        "binding_proposal": {
            "allowed_modes": list(BINDING_MODES),
            "proposed_binding_mode": "emit_existing_yym4_character_name",
            "recommended_default": {
                "mode": "emit_existing_yym4_character_name",
                "reason": (
                    "The manual result showed that selecting the existing YMM4 "
                    "character resolved the placeholder safely while all four "
                    "diagnostic texts stayed visible. Emitting that existing "
                    "character name in a separate candidate CSV reduces the "
                    "next manual import friction without claiming automatic "
                    "binding, TTS readiness, .ymmp readiness, or production "
                    "approval."
                ),
            },
            "candidate_speaker_name": OBSERVED_MANUAL_CHARACTER,
            "fallback_behavior": "manual selection remains allowed",
            "automatic_binding_claimed": False,
            "metadata_mapping_still_recorded": True,
        },
        "placeholder_to_yym4_character_mapping": {
            "source_placeholder_speaker": SOURCE_PLACEHOLDER_SPEAKER,
            "candidate_speaker_name": OBSERVED_MANUAL_CHARACTER,
            "mapping_basis": "operator_observed_manual_selection",
            "mapping_status": "candidate_not_YMM4_verified_as_automatic_binding",
            "applies_to_rows": [row["csv_row_number"] for row in candidate_rows],
        },
        "optional_bound_csv_candidate": {
            "created": True,
            "path": _path_text(bound_csv_candidate_path),
            "source_tiny_csv_path": _path_text(source_tiny_csv_path),
            "status": [
                "not_YMM4_verified",
                "intended_for_next_manual_check",
            ],
            "derivation": {
                "source_row_count": len(source_rows),
                "candidate_row_count": len(candidate_rows),
                "text_preserved_exactly": candidate_validation[
                    "all_text_preserved_exactly"
                ],
                "changed_columns": ["speaker"],
                "unchanged_columns": ["text"],
                "source_placeholder_speaker": SOURCE_PLACEHOLDER_SPEAKER,
                "candidate_speaker_name": OBSERVED_MANUAL_CHARACTER,
            },
            "csv_contract": {
                "encoding": "utf-8-sig",
                "preserve_utf8_bom": True,
                "has_header": False,
                "columns": list(TARGET_SURFACE_COLUMNS),
                "timing_columns_in_csv": False,
                "media_paths_in_csv": False,
                "production_ready_flags_in_csv": False,
            },
            "rows": candidate_rows,
            "validation": candidate_validation,
        },
        "source_validation": source_validation,
        "safety_boundary": safety_boundary,
        "boundary_assertions": {
            **safety_boundary,
            "diagnostic_only": True,
            "source_tiny_csv_replaced": False,
            "bound_csv_is_new_artifact": True,
            "automatic_speaker_binding_claimed": False,
            "YMM4_approval": False,
            "external_fetch_performed": False,
            "real_newsroom_ingest_performed": False,
            "dashboard_governance_freshness_changed": False,
        },
        "next_actions": {
            "recommended_next_slice": (
                "newsroom-yym4-bound-speaker-manual-check-packet-v1"
            ),
            "if_bound_csv_candidate_is_used": (
                "Create a new manual check packet for the bound-speaker CSV "
                "and verify whether YMM4 accepts the explicit existing "
                "character name without asking the operator to bind it again."
            ),
            "fallback_next_slice": (
                "newsroom-yym4-import-readiness-after-manual-result-v1"
            ),
            "do_not_recommend_immediate": [
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
            "axis_if_needed": "speaker_binding_policy",
            "reason": (
                "The prior manual result is already recorded; this slice only "
                "turns that result into a bounded policy and new candidate CSV. "
                "No repeated timing, caption, copy, neutral timeline, CSV, "
                "script, tiny import, or generic manual result review is needed."
            ),
        },
    }


def render_bound_speaker_csv_output(policy: dict[str, Any]) -> list[list[str]]:
    """Return the bound speaker CSV rows as two-column values."""
    candidate = _dict(policy.get("optional_bound_csv_candidate"))
    return [
        [str(row.get("bound_speaker") or ""), str(row.get("text") or "")]
        for row in _list(candidate.get("rows"))
    ]


def write_bound_speaker_csv(policy: dict[str, Any], path: str | Path) -> Path:
    """Write the bound speaker CSV candidate with UTF-8 BOM and no header."""
    csv_path = Path(path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerows(render_bound_speaker_csv_output(policy))
    return csv_path


def render_newsroom_yym4_speaker_binding_policy_markdown(
    policy: dict[str, Any],
) -> str:
    """Render a human-readable speaker binding policy readback."""
    identity = _dict(policy.get("identity"))
    observed = _dict(policy.get("observed_binding"))
    proposal = _dict(policy.get("binding_proposal"))
    recommended = _dict(proposal.get("recommended_default"))
    candidate = _dict(policy.get("optional_bound_csv_candidate"))
    candidate_validation = _dict(candidate.get("validation"))
    safety = _dict(policy.get("safety_boundary"))
    review_memory = _dict(policy.get("review_memory"))
    next_actions = _dict(policy.get("next_actions"))

    lines = [
        "# Newsroom YMM4 Speaker Binding Policy v1",
        "",
        f"artifact_id: {policy.get('artifact_id')}",
        f"policy_id: {policy.get('policy_id')}",
        f"schema_version: {policy.get('schema_version')}",
        f"review_status: {policy.get('review_status')}",
        f"production_status: {policy.get('production_status')}",
        f"policy_status: {policy.get('policy_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        f"- source_manual_result_path: {identity.get('source_manual_result_path')}",
        f"- source_manual_result_id: {identity.get('source_manual_result_id')}",
        f"- source_tiny_csv_path: {identity.get('source_tiny_csv_path')}",
        f"- source_commit_or_status: {identity.get('source_commit_or_status')}",
        "",
        "## Observed Binding",
        "",
        (
            "- source_placeholder_speaker: "
            f"{observed.get('source_placeholder_speaker')}"
        ),
        f"- observed_manual_character: {observed.get('observed_manual_character')}",
        f"- observed_behavior: {observed.get('observed_behavior')}",
        f"- import_result: {observed.get('import_result')}",
        (
            "- automatic_binding_observed: "
            f"{str(observed.get('automatic_binding_observed')).lower()}"
        ),
        f"- observed_line_count: {observed.get('observed_line_count')}",
        f"- all_text_visible: {str(observed.get('all_text_visible')).lower()}",
        "",
        "## Binding Proposal",
        "",
        f"- proposed_binding_mode: {proposal.get('proposed_binding_mode')}",
        f"- recommended_default: {recommended.get('mode')}",
        f"- candidate_speaker_name: {proposal.get('candidate_speaker_name')}",
        f"- fallback_behavior: {proposal.get('fallback_behavior')}",
        (
            "- automatic_binding_claimed: "
            f"{str(proposal.get('automatic_binding_claimed')).lower()}"
        ),
        f"- reason: {recommended.get('reason')}",
        "",
        "## Bound CSV Candidate",
        "",
        f"- created: {str(candidate.get('created')).lower()}",
        f"- path: {candidate.get('path')}",
        f"- status: {', '.join(candidate.get('status', []))}",
        f"- encoding: {candidate.get('csv_contract', {}).get('encoding')}",
        (
            "- preserve_utf8_bom: "
            f"{str(candidate.get('csv_contract', {}).get('preserve_utf8_bom')).lower()}"
        ),
        f"- has_header: {str(candidate.get('csv_contract', {}).get('has_header')).lower()}",
        (
            "- timing_columns_in_csv: "
            f"{str(candidate.get('csv_contract', {}).get('timing_columns_in_csv')).lower()}"
        ),
        (
            "- production_ready_flags_in_csv: "
            f"{str(candidate.get('csv_contract', {}).get('production_ready_flags_in_csv')).lower()}"
        ),
        "",
        "| csv_row | source speaker | bound speaker | text |",
        "|---|---|---|---|",
    ]
    for row in _list(candidate.get("rows")):
        lines.append(
            f"| {row['csv_row_number']} | {row['source_speaker']} | "
            f"{row['bound_speaker']} | {row['text']} |"
        )

    lines.extend(
        [
            "",
            "## Candidate Validation",
            "",
            f"- row_count: {candidate_validation.get('row_count')}",
            f"- expected_row_count: {candidate_validation.get('expected_row_count')}",
            (
                "- all_text_preserved_exactly: "
                f"{str(candidate_validation.get('all_text_preserved_exactly')).lower()}"
            ),
            (
                "- only_speaker_column_changed: "
                f"{str(candidate_validation.get('only_speaker_column_changed')).lower()}"
            ),
            (
                "- no_timing_columns: "
                f"{str(candidate_validation.get('no_timing_columns')).lower()}"
            ),
            (
                "- no_media_paths: "
                f"{str(candidate_validation.get('no_media_paths')).lower()}"
            ),
            "",
            "## Review Memory",
            "",
            f"- prior_user_review_count: {review_memory.get('prior_user_review_count')}",
            "- repeated_general_review_allowed: false",
            "- next_nonredundant_axis:",
        ]
    )
    for axis in review_memory.get("next_nonredundant_axis", []):
        lines.append(f"  - {axis}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(review_memory.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(["", "## Safety Boundary", ""])
    for key, value in safety.items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(
        [
            "",
            "## Next Use",
            "",
            f"- recommended_next_slice: {next_actions.get('recommended_next_slice')}",
            f"- fallback_next_slice: {next_actions.get('fallback_next_slice')}",
            f"- if_bound_csv_candidate_is_used: {next_actions.get('if_bound_csv_candidate_is_used')}",
            "- do_not_recommend_immediate:",
        ]
    )
    for item in next_actions.get("do_not_recommend_immediate", []):
        lines.append(f"  - {item}")

    lines.extend(
        [
            "",
            "## Review Card",
            "",
            "Review Card: none. The prior manual import result is already "
            "recorded, and this policy only defines the speaker-binding axis "
            "and a separate bound CSV candidate.",
            "",
            "## Boundary",
            "",
            "This policy is diagnostic-only. It does not prove automatic speaker "
            "binding, TTS readiness, `.ymmp` readiness, render readiness, "
            "production readiness, YMM4 approval, or public video readiness.",
            "",
        ]
    )
    return "\n".join(lines)


def _bound_candidate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_row in source_rows:
        rows.append(
            {
                "csv_row_number": source_row.get("row_number"),
                "source_speaker": source_row.get("speaker"),
                "bound_speaker": OBSERVED_MANUAL_CHARACTER,
                "text": source_row.get("text"),
                "source_column_count": source_row.get("column_count"),
                "candidate_column_count": 2,
                "speaker_changed": source_row.get("speaker")
                != OBSERVED_MANUAL_CHARACTER,
                "text_preserved": True,
            }
        )
    return rows


def _source_validation(
    manual_result: dict[str, Any],
    source_csv_readback: dict[str, Any],
    *,
    observation: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if manual_result.get("result") != "pass_with_warnings":
        errors.append("MANUAL_RESULT_NOT_PASS_WITH_WARNINGS")
    if observation.get("selected_speaker_or_character") != OBSERVED_MANUAL_CHARACTER:
        errors.append("OBSERVED_MANUAL_CHARACTER_MISMATCH")
    if observation.get("speaker_behavior") != "mapped_after_manual_selection":
        errors.append("SPEAKER_BEHAVIOR_NOT_MANUAL_SELECTION")
    if observation.get("all_text_visible") is not True:
        errors.append("ALL_TEXT_VISIBLE_NOT_TRUE")
    if observation.get("observed_line_count") != EXPECTED_MANUAL_IMPORT_ROW_COUNT:
        errors.append("OBSERVED_ROW_COUNT_NOT_4")
    if source_csv_readback.get("row_count") != EXPECTED_MANUAL_IMPORT_ROW_COUNT:
        errors.append("SOURCE_CSV_ROW_COUNT_NOT_4")
    if source_csv_readback.get("bom_verified") is not True:
        errors.append("SOURCE_CSV_BOM_NOT_VERIFIED")
    if source_csv_readback.get("has_header") is not False:
        errors.append("SOURCE_CSV_HEADER_PRESENT")
    if source_csv_readback.get("all_rows_two_columns") is not True:
        errors.append("SOURCE_CSV_NOT_TWO_COLUMN")

    rows = _list(source_csv_readback.get("rows"))
    placeholder_rows = [
        row
        for row in rows
        if row.get("speaker") == SOURCE_PLACEHOLDER_SPEAKER
    ]
    if len(placeholder_rows) != len(rows):
        errors.append("SOURCE_PLACEHOLDER_NOT_USED_FOR_ALL_ROWS")

    return {
        "manual_result": manual_result.get("result"),
        "manual_check_status": manual_result.get("manual_check_status"),
        "selected_speaker_or_character": observation.get(
            "selected_speaker_or_character"
        ),
        "speaker_behavior": observation.get("speaker_behavior"),
        "automatic_binding_observed": False,
        "source_csv_bom_verified": source_csv_readback.get("bom_verified"),
        "source_csv_has_header": source_csv_readback.get("has_header"),
        "source_csv_all_rows_two_columns": source_csv_readback.get(
            "all_rows_two_columns"
        ),
        "source_csv_row_count": source_csv_readback.get("row_count"),
        "source_placeholder_rows": len(placeholder_rows),
        "errors": errors,
    }


def _candidate_validation(
    source_rows: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    errors: list[str] = []
    if len(candidate_rows) != EXPECTED_MANUAL_IMPORT_ROW_COUNT:
        errors.append(f"CANDIDATE_ROW_COUNT_EXPECTED_4_ACTUAL_{len(candidate_rows)}")
    if len(candidate_rows) != len(source_rows):
        errors.append("CANDIDATE_SOURCE_ROW_COUNT_MISMATCH")

    row_checks: list[dict[str, Any]] = []
    for source_row, candidate_row in zip(source_rows, candidate_rows, strict=False):
        row_errors: list[str] = []
        source_text = str(source_row.get("text") or "")
        candidate_text = str(candidate_row.get("text") or "")
        source_speaker = str(source_row.get("speaker") or "")
        bound_speaker = str(candidate_row.get("bound_speaker") or "")
        if candidate_text != source_text:
            row_errors.append("text_changed")
        if source_speaker != SOURCE_PLACEHOLDER_SPEAKER:
            row_errors.append("source_speaker_not_placeholder")
        if bound_speaker != OBSERVED_MANUAL_CHARACTER:
            row_errors.append("bound_speaker_not_observed_character")
        if _has_real_url(candidate_text) or _has_real_url(bound_speaker):
            row_errors.append("real_url_detected")
        if _has_media_path(candidate_text) or _has_media_path(bound_speaker):
            row_errors.append("media_path_detected")
        errors.extend(
            f"CSV_ROW_{candidate_row.get('csv_row_number')}:{error}"
            for error in row_errors
        )
        row_checks.append(
            {
                "csv_row_number": candidate_row.get("csv_row_number"),
                "text_preserved": candidate_text == source_text,
                "source_speaker_was_placeholder": (
                    source_speaker == SOURCE_PLACEHOLDER_SPEAKER
                ),
                "bound_speaker_is_observed_character": (
                    bound_speaker == OBSERVED_MANUAL_CHARACTER
                ),
                "no_real_urls": not (
                    _has_real_url(candidate_text) or _has_real_url(bound_speaker)
                ),
                "no_media_paths": not (
                    _has_media_path(candidate_text) or _has_media_path(bound_speaker)
                ),
                "status": "passed" if not row_errors else "failed",
                "errors": row_errors,
            }
        )

    return {
        "row_count": len(candidate_rows),
        "expected_row_count": EXPECTED_MANUAL_IMPORT_ROW_COUNT,
        "all_text_preserved_exactly": all(
            check["text_preserved"] for check in row_checks
        ),
        "only_speaker_column_changed": all(
            check["source_speaker_was_placeholder"]
            and check["bound_speaker_is_observed_character"]
            and check["text_preserved"]
            for check in row_checks
        ),
        "candidate_speaker_name": OBSERVED_MANUAL_CHARACTER,
        "no_timing_columns": True,
        "no_media_paths": all(check["no_media_paths"] for check in row_checks),
        "no_real_urls": all(check["no_real_urls"] for check in row_checks),
        "no_production_ready_flags": True,
        "automatic_binding_verified_by_YMM4": False,
        "rows": row_checks,
        "errors": errors,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "automatic_speaker_binding": False,
        "TTS_ready_script": False,
        "ymmp": False,
        "render": False,
        "production_readiness": False,
        "public_video": False,
        "YMM4_approval": False,
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


def _has_real_url(text: str) -> bool:
    lowered = text.lower()
    return (
        ("http" + "://") in lowered
        or ("https" + "://") in lowered
        or (("w" * 3) + ".") in lowered
    )


def _has_media_path(text: str) -> bool:
    lowered = text.lower()
    media_suffixes = (
        ".mp4",
        ".mov",
        ".wav",
        ".mp3",
        ".m4a",
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".gif",
    )
    return any(suffix in lowered for suffix in media_suffixes)


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None
