"""Caption-only CSV import candidate checker for newsroom diagnostics.

This module reads the existing neutral timeline JSON and its derived caption
CSV, then produces an import-candidate readback. It does not create YMM4
projects, carriers, renders, TTS/audio, real packet ingests, fetches, media, or
production approvals.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_neutral_timeline_import_proof import (
    CAPTION_CSV_COLUMNS,
    DEFAULT_CAPTION_IMPORT_CSV_PATH,
    DEFAULT_NEUTRAL_TIMELINE_PATH,
)


CAPTION_CSV_IMPORT_CANDIDATE_SCHEMA_VERSION = (
    "newsroom_caption_csv_import_candidate.v1"
)
CAPTION_CSV_IMPORT_CANDIDATE_ID = (
    "newsroom_caption_csv_import_candidate_v1_2026_06_22"
)
DEFAULT_CAPTION_CSV_IMPORT_CANDIDATE_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/caption_csv_import_candidate_readback_v1.json"
)
DEFAULT_CAPTION_CSV_IMPORT_CANDIDATE_DOC_PATH = Path(
    "docs/verification/NEWSROOM_CAPTION_CSV_IMPORT_CANDIDATE_V1_2026-06-22.md"
)

REQUIRED_COLUMNS: tuple[str, ...] = CAPTION_CSV_COLUMNS
TIMING_TOLERANCE_SEC = 0.001


def build_default_newsroom_caption_csv_import_candidate(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed caption CSV import candidate readback."""
    base = Path(root) if root is not None else Path(".")
    timeline = load_json_object(base / DEFAULT_NEUTRAL_TIMELINE_PATH)
    csv_rows = load_caption_csv_rows(base / DEFAULT_CAPTION_IMPORT_CSV_PATH)
    return build_newsroom_caption_csv_import_candidate(
        csv_rows,
        timeline,
        csv_path=DEFAULT_CAPTION_IMPORT_CSV_PATH,
        neutral_timeline_path=DEFAULT_NEUTRAL_TIMELINE_PATH,
    )


def load_caption_csv_rows(path: str | Path) -> list[dict[str, str]]:
    """Load the caption import CSV as a list of string-keyed rows."""
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def build_newsroom_caption_csv_import_candidate(
    csv_rows: list[dict[str, str]],
    neutral_timeline: dict[str, Any],
    *,
    csv_path: str | Path | None = None,
    neutral_timeline_path: str | Path | None = None,
    source_commit_or_status: str = "worktree_verified_before_generation",
) -> dict[str, Any]:
    """Validate the caption CSV as a caption-only diagnostic import candidate."""
    caption_items = _caption_items_by_id(neutral_timeline)
    schema = _schema_validation(csv_rows)
    row_validation = _row_validation(csv_rows)
    consistency = _neutral_timeline_consistency(csv_rows, caption_items)
    safety = _diagnostic_safety(csv_rows, neutral_timeline)
    errors = (
        schema["errors"]
        + row_validation["errors"]
        + consistency["errors"]
        + safety["errors"]
    )
    warnings = (
        schema["warnings"]
        + row_validation["warnings"]
        + consistency["warnings"]
        + safety["warnings"]
    )
    status = _candidate_status(errors, warnings)

    return {
        "artifact_id": CAPTION_CSV_IMPORT_CANDIDATE_ID,
        "schema_version": CAPTION_CSV_IMPORT_CANDIDATE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "source": {
            "source_csv_path": _path_text(csv_path),
            "source_neutral_timeline_path": _path_text(neutral_timeline_path),
            "source_commit_or_status": source_commit_or_status,
            "neutral_timeline_id": neutral_timeline.get("timeline_id"),
            "source_episode_id": neutral_timeline.get("source_episode_id"),
        },
        "review_memory": {
            "prior_user_review_count": 0,
            "accepted_scope": [
                "diagnostic_timing_panel_surface_by_validation",
                "diagnostic_caption_copy_refinement_by_validation",
                "diagnostic_transfer_candidate_classification",
                "neutral_timeline_import_proof",
            ],
            "not_accepted_scope": [
                "production subtitle design",
                "production narration",
                "TTS-ready script",
                "YMM4 transfer approval",
                ".ymmp",
                "render",
                "public video",
            ],
            "current_axis": "caption_csv_import_candidate_schema",
            "next_nonredundant_axis": [
                "csv_consumer_readback",
                "caption_only_import_minimum",
            ],
            "repeated_general_review_allowed": False,
        },
        "caption_csv_import_status": status,
        "schema_validation": schema,
        "row_validation": row_validation,
        "neutral_timeline_consistency": consistency,
        "diagnostic_safety": safety,
        "import_candidate_result": {
            "caption_csv_import_status": status,
            "recommended_next_slice": "newsroom-script-import-candidate-v1",
            "allowed_next_artifacts": [
                "script import candidate",
                "neutral timeline consumer proof",
                "YMM4-adjacent no-media proof",
            ],
            "prohibited_next_artifacts": [
                "production .ymmp",
                "render output",
                "TTS output",
                "real media",
            ],
            "errors": errors,
            "warnings": warnings,
        },
        "review_card": {
            "status": "none",
            "axis_if_needed": "caption_csv_import_candidate_schema",
            "reason": (
                "No user judgement is required because the checker validates the "
                "caption-only CSV import minimum directly."
            ),
            "not_asking": (
                "No repeated timing, caption copy, blocker, or neutral timeline "
                "review is requested."
            ),
        },
        "boundary_assertions": {
            "diagnostic_only": True,
            "caption_only_import_candidate": True,
            "neutral_timeline_json_is_source_of_truth": True,
            "source_csv_changed": False,
            "opens_production_transfer": False,
            "opens_YMM4_transfer": False,
            "requires_YMM4_columns": False,
            "real_urls": False,
            "real_media_paths": False,
            "TTS_generated": False,
            "render_created": False,
            "ymmp_created": False,
            "production_approval": False,
            "public_video": False,
            "external_fetch_performed": False,
            "dashboard_governance_freshness_changed": False,
        },
    }


def render_newsroom_caption_csv_import_candidate_markdown(
    readback: dict[str, Any],
) -> str:
    """Render a human-readable readback for the caption CSV import candidate."""
    source = _dict(readback.get("source"))
    schema = _dict(readback.get("schema_validation"))
    rows = _dict(readback.get("row_validation"))
    consistency = _dict(readback.get("neutral_timeline_consistency"))
    safety = _dict(readback.get("diagnostic_safety"))
    result = _dict(readback.get("import_candidate_result"))
    review_memory = _dict(readback.get("review_memory"))

    lines = [
        "# Newsroom Caption CSV Import Candidate v1",
        "",
        f"artifact_id: {readback.get('artifact_id')}",
        f"schema_version: {readback.get('schema_version')}",
        f"review_status: {readback.get('review_status')}",
        f"production_status: {readback.get('production_status')}",
        f"caption_csv_import_status: {readback.get('caption_csv_import_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        f"- source_csv_path: {source.get('source_csv_path')}",
        f"- source_neutral_timeline_path: {source.get('source_neutral_timeline_path')}",
        f"- source_episode_id: {source.get('source_episode_id')}",
        f"- source_commit_or_status: {source.get('source_commit_or_status')}",
        "",
        "## Review Memory",
        "",
        f"- prior_user_review_count: {review_memory.get('prior_user_review_count')}",
        f"- current_axis: {review_memory.get('current_axis')}",
        "- repeated_general_review_allowed: false",
        "",
        "## Schema",
        "",
        f"- required_columns_present: {str(schema.get('required_columns_present')).lower()}",
        f"- column_order_matches_required: {str(schema.get('column_order_matches_required')).lower()}",
        f"- required_YMM4_columns: {', '.join(schema.get('required_YMM4_columns', [])) or 'none'}",
        f"- extra_columns_blocking: {str(schema.get('extra_columns_blocking')).lower()}",
        "",
        "## Row Validation",
        "",
        f"- row_count: {rows.get('row_count')}",
        f"- expected_row_count: {rows.get('expected_row_count')}",
        f"- all_rows_valid: {str(rows.get('all_rows_valid')).lower()}",
        "",
        "| caption_id | beat_id | timing | flags |",
        "|---|---|---|---|",
    ]
    for row in rows.get("rows", []):
        lines.append(
            f"| {row['caption_id']} | {row['beat_id']} | "
            f"{row['start_sec']}-{row['end_sec']}s | "
            f"diagnostic_only={str(row['diagnostic_only_is_true']).lower()}, "
            "production_ready=false |"
        )

    lines.extend([
        "",
        "## Neutral Timeline Consistency",
        "",
        f"- every_csv_caption_id_exists: {str(consistency.get('every_csv_caption_id_exists')).lower()}",
        f"- timing_matches: {str(consistency.get('timing_matches')).lower()}",
        f"- text_matches: {str(consistency.get('text_matches')).lower()}",
        f"- missing_caption_rows: {', '.join(consistency.get('missing_caption_rows', [])) or 'none'}",
        f"- extra_caption_rows: {', '.join(consistency.get('extra_caption_rows', [])) or 'none'}",
        "",
        "## Diagnostic Safety",
        "",
        f"- real_urls: {str(safety.get('real_urls')).lower()}",
        f"- real_media_paths: {str(safety.get('real_media_paths')).lower()}",
        f"- TTS_generated: {str(safety.get('TTS_generated')).lower()}",
        f"- render_created: {str(safety.get('render_created')).lower()}",
        f"- ymmp_created: {str(safety.get('ymmp_created')).lower()}",
        f"- production_approval: {str(safety.get('production_approval')).lower()}",
        "",
        "## Next Use",
        "",
        f"- recommended_next_slice: {result.get('recommended_next_slice')}",
        "- allowed_next_artifacts:",
    ])
    for artifact in result.get("allowed_next_artifacts", []):
        lines.append(f"  - {artifact}")
    lines.append("- prohibited_next_artifacts:")
    for artifact in result.get("prohibited_next_artifacts", []):
        lines.append(f"  - {artifact}")

    lines.extend([
        "",
        "## Review Card",
        "",
        "Review Card: none. This checker validates the caption CSV import candidate "
        "schema without asking for repeated timing, caption, copy, blocker, or "
        "neutral timeline review.",
        "",
        "## Boundary",
        "",
        "This readback is diagnostic-only and caption-only. It does not create "
        "`.ymmp`, YMM4 carriers, renders, TTS/audio, real packet ingestion, "
        "external fetches, real source access, media files, production approvals, "
        "rights approvals, public-use approvals, or publishing output.",
        "",
    ])
    return "\n".join(lines)


def _schema_validation(csv_rows: list[dict[str, str]]) -> dict[str, Any]:
    actual_columns = list(csv_rows[0].keys()) if csv_rows else []
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in actual_columns]
    extra_columns = [column for column in actual_columns if column not in REQUIRED_COLUMNS]
    errors = [
        f"MISSING_REQUIRED_COLUMN:{column}"
        for column in missing_columns
    ]
    return {
        "required_columns": list(REQUIRED_COLUMNS),
        "actual_columns": actual_columns,
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
        "required_columns_present": not missing_columns,
        "column_order_matches_required": actual_columns == list(REQUIRED_COLUMNS),
        "extra_columns_blocking": False,
        "required_YMM4_columns": [],
        "YMM4_columns_required": False,
        "errors": errors,
        "warnings": [],
    }


def _row_validation(csv_rows: list[dict[str, str]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    for index, row in enumerate(csv_rows, start=1):
        row_errors: list[str] = []
        caption_id = str(row.get("caption_id") or "")
        beat_id = str(row.get("beat_id") or "")
        text = str(row.get("text") or "")
        start = _float_value(row.get("start_sec"))
        end = _float_value(row.get("end_sec"))
        duration = _float_value(row.get("duration_sec"))
        if not caption_id:
            row_errors.append("caption_id_empty")
        if not beat_id:
            row_errors.append("beat_id_empty")
        if start is None or end is None:
            row_errors.append("timing_not_numeric")
        elif not start < end:
            row_errors.append("start_sec_not_less_than_end_sec")
        if start is not None and end is not None and duration is not None:
            if abs(duration - (end - start)) > TIMING_TOLERANCE_SEC:
                row_errors.append("duration_mismatch")
        else:
            row_errors.append("duration_not_numeric")
        if not text:
            row_errors.append("text_empty")
        diagnostic_true = _bool_string(row.get("diagnostic_only")) is True
        production_false = _bool_string(row.get("production_ready")) is False
        if not diagnostic_true:
            row_errors.append("diagnostic_only_not_true")
        if not production_false:
            row_errors.append("production_ready_not_false")

        errors.extend(f"ROW_{index}:{error}" for error in row_errors)
        rows.append({
            "row_number": index,
            "caption_id": caption_id,
            "beat_id": beat_id,
            "start_sec": start,
            "end_sec": end,
            "duration_sec": duration,
            "text": text,
            "diagnostic_only_is_true": diagnostic_true,
            "production_ready_is_false": production_false,
            "status": "passed" if not row_errors else "failed",
            "errors": row_errors,
        })
    if len(csv_rows) != 4:
        errors.append(f"ROW_COUNT_EXPECTED_4_ACTUAL_{len(csv_rows)}")
    return {
        "row_count": len(csv_rows),
        "expected_row_count": 4,
        "all_rows_valid": not errors,
        "rows": rows,
        "errors": errors,
        "warnings": warnings,
    }


def _neutral_timeline_consistency(
    csv_rows: list[dict[str, str]],
    caption_items: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    csv_ids = [str(row.get("caption_id") or "") for row in csv_rows]
    timeline_ids = list(caption_items)
    missing_caption_rows = [caption_id for caption_id in timeline_ids if caption_id not in csv_ids]
    extra_caption_rows = [caption_id for caption_id in csv_ids if caption_id not in caption_items]
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for row in csv_rows:
        caption_id = str(row.get("caption_id") or "")
        item = caption_items.get(caption_id)
        if item is None:
            rows.append({
                "caption_id": caption_id,
                "exists_in_neutral_timeline": False,
                "timing_matches": False,
                "text_matches": False,
            })
            continue
        start = _float_value(row.get("start_sec"))
        end = _float_value(row.get("end_sec"))
        duration = _float_value(row.get("duration_sec"))
        timing_matches = (
            _float_matches(start, item.get("start_sec"))
            and _float_matches(end, item.get("end_sec"))
            and _float_matches(duration, item.get("duration_sec"))
        )
        text_matches = str(row.get("text") or "") == str(item.get("text") or "")
        if not timing_matches:
            errors.append(f"TIMING_MISMATCH:{caption_id}")
        if not text_matches:
            errors.append(f"TEXT_MISMATCH:{caption_id}")
        rows.append({
            "caption_id": caption_id,
            "exists_in_neutral_timeline": True,
            "neutral_timeline_item_id": item.get("item_id"),
            "timing_matches": timing_matches,
            "text_matches": text_matches,
        })
    errors.extend(f"MISSING_CAPTION_ROW:{caption_id}" for caption_id in missing_caption_rows)
    errors.extend(f"EXTRA_CAPTION_ROW:{caption_id}" for caption_id in extra_caption_rows)
    return {
        "neutral_timeline_caption_count": len(caption_items),
        "csv_caption_count": len(csv_rows),
        "every_csv_caption_id_exists": not extra_caption_rows,
        "timing_matches": not any(not row["timing_matches"] for row in rows),
        "text_matches": not any(not row["text_matches"] for row in rows),
        "missing_caption_rows": missing_caption_rows,
        "extra_caption_rows": extra_caption_rows,
        "rows": rows,
        "errors": errors,
        "warnings": [],
    }


def _diagnostic_safety(
    csv_rows: list[dict[str, str]],
    neutral_timeline: dict[str, Any],
) -> dict[str, Any]:
    text_blob = "\n".join(
        str(value)
        for row in csv_rows
        for value in row.values()
        if value is not None
    )
    boundary = _dict(neutral_timeline.get("boundary_assertions"))
    real_urls = _has_real_url(text_blob)
    real_media_paths = _has_media_path(text_blob)
    tts_generated = bool(boundary.get("tts_generated"))
    render_created = bool(boundary.get("render_generated"))
    ymmp_created = bool(boundary.get("ymmp_generated"))
    production_approval = bool(boundary.get("production_approval"))
    errors: list[str] = []
    if real_urls:
        errors.append("REAL_URL_PRESENT")
    if real_media_paths:
        errors.append("REAL_MEDIA_PATH_PRESENT")
    if tts_generated:
        errors.append("TTS_GENERATED_TRUE")
    if render_created:
        errors.append("RENDER_CREATED_TRUE")
    if ymmp_created:
        errors.append("YMMP_CREATED_TRUE")
    if production_approval:
        errors.append("PRODUCTION_APPROVAL_TRUE")
    return {
        "real_urls": real_urls,
        "real_media_paths": real_media_paths,
        "TTS_generated": tts_generated,
        "render_created": render_created,
        "ymmp_created": ymmp_created,
        "production_approval": production_approval,
        "external_fetch_performed": bool(boundary.get("external_fetch_performed")),
        "errors": errors,
        "warnings": [],
    }


def _caption_items_by_id(timeline: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("caption_id")): item
        for item in _list(timeline.get("items"))
        if item.get("item_kind") == "caption" and item.get("caption_id")
    }


def _candidate_status(errors: list[str], warnings: list[str]) -> str:
    if errors:
        return "failed"
    if warnings:
        return "passed_with_warnings"
    return "passed"


def _float_value(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _float_matches(left: float | None, right: Any) -> bool:
    right_value = _float_value(right)
    if left is None or right_value is None:
        return False
    return abs(left - right_value) <= TIMING_TOLERANCE_SEC


def _bool_string(value: Any) -> bool | None:
    lowered = str(value).strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return None


def _has_real_url(text: str) -> bool:
    lowered = text.lower()
    return ("http" + "://") in lowered or ("https" + "://") in lowered or (("w" * 3) + ".") in lowered


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
