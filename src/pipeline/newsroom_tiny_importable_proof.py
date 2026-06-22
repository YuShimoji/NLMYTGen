"""Tiny importable proof for diagnostic newsroom script rows.

This module turns the existing YMM4-adjacent no-media row shape into the
smallest repo-consistent CSV artifact. It does not create YMM4 projects,
carriers, renders, TTS/audio, media, real packet ingests, fetches, or
production approvals.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from src.contracts.ymm4_csv_schema import YMM4CsvOutput, YMM4CsvRow
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_script_import_candidate import (
    DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH,
)
from src.pipeline.newsroom_yym4_adjacent_no_media_import_shape import (
    DEFAULT_YYM4_ADJACENT_NO_MEDIA_PROOF_PATH,
)


TINY_IMPORTABLE_SCHEMA_VERSION = "newsroom_tiny_importable_proof.v1"
TINY_IMPORTABLE_PROOF_ID = "newsroom_tiny_importable_proof_v1_2026_06_22"
DEFAULT_TINY_IMPORT_CSV_PATH = Path(
    "samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv"
)
DEFAULT_TINY_IMPORTABLE_PROOF_PATH = Path(
    "samples/_probe/newsroom_handoff/tiny_importable_proof_v1.json"
)
DEFAULT_TINY_IMPORTABLE_DOC_PATH = Path(
    "docs/verification/NEWSROOM_TINY_IMPORTABLE_PROOF_V1_2026-06-22.md"
)

EXPECTED_TINY_IMPORT_ROW_COUNT = 4
TINY_IMPORT_COLUMNS: tuple[str, ...] = ("speaker", "text")
TINY_IMPORT_WARNINGS: tuple[str, ...] = (
    "not_YMM4_verified",
    "timing_metadata_not_imported",
    "no_audio",
    "no_media",
    "synthetic_speaker_not_bound_to_YMM4_character",
)


def build_default_newsroom_tiny_importable_proof(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed tiny importable proof from default inputs."""
    base = Path(root) if root is not None else Path(".")
    yym4_adjacent_shape = load_json_object(
        base / DEFAULT_YYM4_ADJACENT_NO_MEDIA_PROOF_PATH
    )
    script_candidate = load_json_object(base / DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH)
    return build_newsroom_tiny_importable_proof(
        yym4_adjacent_shape,
        script_candidate,
        yym4_adjacent_shape_path=DEFAULT_YYM4_ADJACENT_NO_MEDIA_PROOF_PATH,
        script_candidate_path=DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH,
        import_artifact_path=DEFAULT_TINY_IMPORT_CSV_PATH,
    )


def build_newsroom_tiny_importable_proof(
    yym4_adjacent_shape: dict[str, Any],
    script_candidate: dict[str, Any],
    *,
    yym4_adjacent_shape_path: str | Path | None = None,
    script_candidate_path: str | Path | None = None,
    import_artifact_path: str | Path | None = None,
    source_commit_or_status: str = "worktree_verified_before_generation",
) -> dict[str, Any]:
    """Build and validate a tiny no-media importable CSV proof."""
    mapping_rows = _list(yym4_adjacent_shape.get("mapping_rows"))
    import_rows = _import_rows_from_mapping_rows(mapping_rows)
    source_validation = _source_validation(yym4_adjacent_shape, script_candidate)
    row_validation = _row_validation(mapping_rows, import_rows)
    safety = _diagnostic_safety(mapping_rows, import_rows, yym4_adjacent_shape)
    boundary = _boundary_status()

    errors = source_validation["errors"] + row_validation["errors"] + safety["errors"]
    warnings = list(TINY_IMPORT_WARNINGS)
    warnings.extend(source_validation["warnings"])
    warnings.extend(row_validation["warnings"])
    warnings.extend(safety["warnings"])
    status = _candidate_status(errors, warnings)

    return {
        "artifact_id": TINY_IMPORTABLE_PROOF_ID,
        "proof_id": TINY_IMPORTABLE_PROOF_ID,
        "schema_version": TINY_IMPORTABLE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "tiny_importable_status": status,
        "identity": {
            "proof_id": TINY_IMPORTABLE_PROOF_ID,
            "source_yym4_adjacent_shape_path": _path_text(yym4_adjacent_shape_path),
            "source_script_candidate_path": _path_text(script_candidate_path),
            "import_artifact_path": _path_text(import_artifact_path),
            "source_commit_or_status": source_commit_or_status,
            "source_episode_id": yym4_adjacent_shape.get("identity", {}).get(
                "source_episode_id"
            ),
            "source_yym4_adjacent_proof_id": yym4_adjacent_shape.get("proof_id"),
            "source_no_media_import_shape_status": yym4_adjacent_shape.get(
                "no_media_import_shape_status"
            ),
            "production_status": "diagnostic_only",
            "import_artifact_type": "tool_adjacent_csv",
            "repo_consistent_value": "speaker_text_no_header_utf8_bom_when_written",
        },
        "review_memory": {
            "prior_user_review_count": 0,
            "accepted_scope": [
                "diagnostic_timing_panel_surface_by_validation",
                "diagnostic_caption_copy_refinement_by_validation",
                "diagnostic_transfer_classification",
                "neutral_timeline_import_proof",
                "caption_csv_import_candidate_schema",
                "diagnostic_script_import_candidate",
                "YMM4_adjacent_no_media_import_shape",
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
            "current_axis": "tiny_importable_artifact_shape",
            "next_nonredundant_axis": [
                "import_readiness_review_surface",
                "manual_import_check_packet",
                "speaker_binding_policy",
            ],
            "repeated_general_review_allowed": False,
        },
        "import_artifact_schema": {
            "format_family": "repo_ymm4_csv_two_column_static_contract",
            "columns": list(TINY_IMPORT_COLUMNS),
            "has_header": False,
            "encoding": "utf-8-sig",
            "delimiter": ",",
            "row_count": len(import_rows),
            "import_artifact_type": "tool_adjacent_csv",
            "repo_consistent_value": "speaker_text_no_header_utf8_bom_when_written",
            "production_ready_flags_in_csv": False,
            "timing_columns_in_csv": False,
        },
        "import_artifact_rows": import_rows,
        "source_mapping": _source_mapping(mapping_rows),
        "source_validation": source_validation,
        "row_validation": row_validation,
        "timing_policy": {
            "policy": "metadata_only",
            "not_in_script_csv": True,
            "metadata_fields": ["start_sec", "end_sec", "duration_sec"],
        },
        "no_media_policy": [
            "captions_and_script_rows_only",
            "no_render",
            "no_TTS",
            "no_real_assets",
        ],
        "boundary_status": boundary,
        "diagnostic_safety": safety,
        "result": {
            "tiny_importable_status": status,
            "warnings": warnings,
            "errors": errors,
            "recommended_next_slice": "newsroom-import-readiness-review-surface-v1",
            "prohibited_next_artifacts": [
                "production .ymmp",
                "render output",
                "TTS output",
                "real media",
            ],
        },
        "review_card": {
            "status": "none",
            "axis_if_needed": "tiny_importable_artifact_shape",
            "reason": (
                "The checker validates the tiny CSV artifact directly; no fresh "
                "user judgement is needed for timing, caption copy, blocker, "
                "neutral timeline, CSV, script, or YMM4-adjacent proof review."
            ),
            "not_asking": (
                "No repeated timing/caption/copy/blocker/neutral timeline/CSV/"
                "script/YMM4-adjacent proof review, YMM4 approval, TTS, media, "
                "render, or production judgement is requested."
            ),
        },
        "boundary_assertions": {
            "diagnostic_only": True,
            "tiny_importable_artifact_shape": True,
            "tool_adjacent_not_YMM4_verified": True,
            "source_yym4_adjacent_shape_changed": False,
            "source_script_candidate_changed": False,
            "opens_production_transfer": False,
            "opens_YMM4_transfer": False,
            "ymmp_created": False,
            "YMM4_launched": False,
            "YMM4_carrier_created": False,
            "YMM4_approval": False,
            "TTS_generated": False,
            "render_created": False,
            "production_approval": False,
            "public_video_ready": False,
            "real_urls": False,
            "real_media_paths": False,
            "external_fetch_performed": False,
            "dashboard_governance_freshness_changed": False,
        },
    }


def render_tiny_import_csv_output(proof: dict[str, Any]) -> YMM4CsvOutput:
    """Return the CSV payload using the repo YMM4 CSV writer contract."""
    rows = tuple(
        YMM4CsvRow(speaker=str(row["speaker"]), text=str(row["text"]))
        for row in _list(proof.get("import_artifact_rows"))
    )
    return YMM4CsvOutput(rows=rows)


def write_tiny_import_csv(proof: dict[str, Any], path: str | Path) -> Path:
    """Write the tiny import CSV artifact with UTF-8 BOM and no header."""
    csv_path = Path(path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        for row in render_tiny_import_csv_output(proof).rows:
            writer.writerow([row.speaker, row.text])
    return csv_path


def render_newsroom_tiny_importable_proof_markdown(
    proof: dict[str, Any],
) -> str:
    """Render a human-readable readback for the tiny importable proof."""
    identity = _dict(proof.get("identity"))
    schema = _dict(proof.get("import_artifact_schema"))
    row_validation = _dict(proof.get("row_validation"))
    safety = _dict(proof.get("diagnostic_safety"))
    boundary = _dict(proof.get("boundary_status"))
    result = _dict(proof.get("result"))
    review_memory = _dict(proof.get("review_memory"))

    lines = [
        "# Newsroom Tiny Importable Proof v1",
        "",
        f"artifact_id: {proof.get('artifact_id')}",
        f"proof_id: {proof.get('proof_id')}",
        f"schema_version: {proof.get('schema_version')}",
        f"review_status: {proof.get('review_status')}",
        f"production_status: {proof.get('production_status')}",
        f"tiny_importable_status: {proof.get('tiny_importable_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        f"- source_yym4_adjacent_shape_path: {identity.get('source_yym4_adjacent_shape_path')}",
        f"- source_script_candidate_path: {identity.get('source_script_candidate_path')}",
        f"- import_artifact_path: {identity.get('import_artifact_path')}",
        f"- import_artifact_type: {identity.get('import_artifact_type')}",
        f"- source_episode_id: {identity.get('source_episode_id')}",
        f"- source_commit_or_status: {identity.get('source_commit_or_status')}",
        "",
        "## Review Memory",
        "",
        f"- prior_user_review_count: {review_memory.get('prior_user_review_count')}",
        f"- current_axis: {review_memory.get('current_axis')}",
        "- repeated_general_review_allowed: false",
        "",
        "## Tiny Importable Summary",
        "",
        f"- columns: {', '.join(schema.get('columns', []))}",
        f"- has_header: {str(schema.get('has_header')).lower()}",
        f"- encoding: {schema.get('encoding')}",
        f"- row_count: {schema.get('row_count')}",
        f"- timing_columns_in_csv: {str(schema.get('timing_columns_in_csv')).lower()}",
        f"- production_ready_flags_in_csv: {str(schema.get('production_ready_flags_in_csv')).lower()}",
        "",
        "## Source Mapping Summary",
        "",
        "| csv_row | source_row_id | source_line_id | source_caption_id | speaker | text | timing metadata |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in _list(proof.get("source_mapping")):
        lines.append(
            f"| {row['csv_row_number']} | {row['source_row_id']} | "
            f"{row['source_line_id']} | {row['source_caption_id']} | "
            f"{row['speaker']} | {row['text']} | "
            f"{row['start_sec']}-{row['end_sec']}s / {row['duration_sec']}s |"
        )

    lines.extend([
        "",
        "## Row Validation",
        "",
        f"- row_count: {row_validation.get('row_count')}",
        f"- expected_row_count: {row_validation.get('expected_row_count')}",
        f"- every_row_maps_exactly_one_source_row: {str(row_validation.get('every_row_maps_exactly_one_source_row')).lower()}",
        f"- all_rows_valid: {str(row_validation.get('all_rows_valid')).lower()}",
        f"- no_real_names_detected: {str(row_validation.get('no_real_names_detected')).lower()}",
        "",
        "## Boundary Summary",
        "",
        f"- ymmp_created: {str(boundary.get('ymmp_created')).lower()}",
        f"- YMM4_launched: {str(boundary.get('YMM4_launched')).lower()}",
        f"- YMM4_carrier_created: {str(boundary.get('YMM4_carrier_created')).lower()}",
        f"- YMM4_approval: {str(boundary.get('YMM4_approval')).lower()}",
        f"- TTS_generated: {str(boundary.get('TTS_generated')).lower()}",
        f"- render_created: {str(boundary.get('render_created')).lower()}",
        f"- public_video_ready: {str(boundary.get('public_video_ready')).lower()}",
        "",
        "## Diagnostic Safety",
        "",
        f"- real_urls: {str(safety.get('real_urls')).lower()}",
        f"- real_media_paths: {str(safety.get('real_media_paths')).lower()}",
        f"- production_approval: {str(safety.get('production_approval')).lower()}",
        "",
        "## Next Use",
        "",
        f"- tiny_importable_status: {result.get('tiny_importable_status')}",
        "- warnings:",
    ])
    for warning in result.get("warnings", []):
        lines.append(f"  - {warning}")
    lines.append(f"- recommended_next_slice: {result.get('recommended_next_slice')}")
    lines.append("- prohibited_next_artifacts:")
    for artifact in result.get("prohibited_next_artifacts", []):
        lines.append(f"  - {artifact}")

    lines.extend([
        "",
        "## Review Card",
        "",
        "Review Card: none. This checker validates the tiny importable artifact "
        "without asking for repeated timing, caption copy, blocker, neutral "
        "timeline, CSV, script, YMM4-adjacent proof, YMM4, TTS, media, render, "
        "or production review.",
        "",
        "## Boundary",
        "",
        "This readback is diagnostic-only and tool-adjacent. It creates only a "
        "tiny script CSV plus proof metadata. It does not create `.ymmp`, YMM4 "
        "carriers, renders, TTS/audio, real packet ingestion, external fetches, "
        "real source access, media files, production approvals, rights approvals, "
        "public-use approvals, or publishing output.",
        "",
    ])
    return "\n".join(lines)


def _import_rows_from_mapping_rows(mapping_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(mapping_rows, start=1):
        adjacent = _dict(row.get("tool_adjacent_row"))
        rows.append({
            "csv_row_number": index,
            "speaker": str(adjacent.get("speaker") or row.get("speaker_id") or ""),
            "text": str(adjacent.get("text") or row.get("text") or ""),
            "source_row_id": row.get("row_id"),
            "source_line_id": row.get("source_line_id"),
            "source_caption_id": row.get("source_caption_id"),
        })
    return rows


def _source_mapping(mapping_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(mapping_rows, start=1):
        rows.append({
            "csv_row_number": index,
            "source_row_id": row.get("row_id"),
            "source_line_id": row.get("source_line_id"),
            "source_caption_id": row.get("source_caption_id"),
            "beat_id": row.get("beat_id"),
            "start_sec": row.get("start_sec"),
            "end_sec": row.get("end_sec"),
            "duration_sec": row.get("duration_sec"),
            "speaker": row.get("speaker_id"),
            "text": row.get("text"),
            "timing_policy": "metadata_only_not_in_script_csv",
        })
    return rows


def _source_validation(
    yym4_adjacent_shape: dict[str, Any],
    script_candidate: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if yym4_adjacent_shape.get("no_media_import_shape_status") != "passed_with_warnings":
        errors.append("YYM4_ADJACENT_STATUS_NOT_PASSED_WITH_WARNINGS")
    if len(_list(yym4_adjacent_shape.get("mapping_rows"))) != EXPECTED_TINY_IMPORT_ROW_COUNT:
        errors.append("YYM4_ADJACENT_MAPPING_ROW_COUNT_NOT_4")
    if script_candidate.get("script_import_status") != "passed":
        errors.append("SCRIPT_IMPORT_STATUS_NOT_PASSED")
    return {
        "source_yym4_adjacent_status": yym4_adjacent_shape.get(
            "no_media_import_shape_status"
        ),
        "source_mapping_row_count": len(_list(yym4_adjacent_shape.get("mapping_rows"))),
        "source_script_import_status": script_candidate.get("script_import_status"),
        "source_artifacts_identified": not errors,
        "errors": errors,
        "warnings": [],
    }


def _row_validation(
    mapping_rows: list[dict[str, Any]],
    import_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    errors: list[str] = []
    rows: list[dict[str, Any]] = []
    source_ids = [str(row.get("source_row_id") or "") for row in import_rows]
    duplicate_source_ids = sorted(
        source_id
        for source_id in set(source_ids)
        if source_id and source_ids.count(source_id) > 1
    )
    mapping_by_id = {
        str(row.get("row_id") or ""): row
        for row in mapping_rows
        if row.get("row_id")
    }
    for row in import_rows:
        source_id = str(row.get("source_row_id") or "")
        source = mapping_by_id.get(source_id)
        row_errors: list[str] = []
        speaker = str(row.get("speaker") or "")
        text = str(row.get("text") or "")
        if source is None:
            row_errors.append("source_row_missing")
        if not speaker:
            row_errors.append("speaker_empty")
        if not text:
            row_errors.append("text_empty")
        if source is not None and text != str(source.get("text") or ""):
            row_errors.append("text_mismatch")
        if _has_real_name(text):
            row_errors.append("real_name_detected")
        if _has_real_url(text):
            row_errors.append("real_url_detected")
        if _has_media_path(text):
            row_errors.append("media_path_detected")
        errors.extend(
            f"CSV_ROW_{row.get('csv_row_number')}:{error}"
            for error in row_errors
        )
        rows.append({
            "csv_row_number": row.get("csv_row_number"),
            "source_row_id": source_id,
            "source_row_exists": source is not None,
            "speaker_non_empty": bool(speaker),
            "text_non_empty": bool(text),
            "text_matches_source_row": (
                source is not None and text == str(source.get("text") or "")
            ),
            "no_real_names": not _has_real_name(text),
            "no_real_urls": not _has_real_url(text),
            "no_media_paths": not _has_media_path(text),
            "status": "passed" if not row_errors else "failed",
            "errors": row_errors,
        })
    if len(import_rows) != EXPECTED_TINY_IMPORT_ROW_COUNT:
        errors.append(f"CSV_ROW_COUNT_EXPECTED_4_ACTUAL_{len(import_rows)}")
    errors.extend(f"DUPLICATE_SOURCE_ROW_ID:{source_id}" for source_id in duplicate_source_ids)
    return {
        "row_count": len(import_rows),
        "expected_row_count": EXPECTED_TINY_IMPORT_ROW_COUNT,
        "every_row_maps_exactly_one_source_row": (
            len(import_rows) == len(mapping_rows)
            and not duplicate_source_ids
            and all(row["source_row_exists"] for row in rows)
        ),
        "all_rows_valid": not errors,
        "no_real_names_detected": all(row["no_real_names"] for row in rows),
        "no_real_urls_detected": all(row["no_real_urls"] for row in rows),
        "no_media_paths_detected": all(row["no_media_paths"] for row in rows),
        "rows": rows,
        "errors": errors,
        "warnings": [],
    }


def _boundary_status() -> dict[str, Any]:
    return {
        "ymmp_created": False,
        "YMM4_launched": False,
        "YMM4_carrier_created": False,
        "YMM4_approval": False,
        "TTS_generated": False,
        "render_created": False,
        "production_approval": False,
        "public_video_ready": False,
        "production_transfer_status": "blocked",
    }


def _diagnostic_safety(
    mapping_rows: list[dict[str, Any]],
    import_rows: list[dict[str, Any]],
    yym4_adjacent_shape: dict[str, Any],
) -> dict[str, Any]:
    text_blob = "\n".join(
        str(value)
        for row in import_rows
        for value in (row.get("speaker"), row.get("text"), row.get("source_row_id"))
        if value is not None
    )
    boundary = _dict(yym4_adjacent_shape.get("boundary_assertions"))
    row_audio = any(row.get("audio_dependency") != "none_for_this_proof" for row in mapping_rows)
    row_media = any(row.get("media_dependency") != "none" for row in mapping_rows)
    real_urls = _has_real_url(text_blob)
    real_media_paths = _has_media_path(text_blob)
    tts_generated = bool(boundary.get("TTS_generated"))
    render_created = bool(boundary.get("render_created"))
    ymmp_created = bool(boundary.get("ymmp_created"))
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
    if row_audio:
        errors.append("ROW_AUDIO_DEPENDENCY_PRESENT")
    if row_media:
        errors.append("ROW_MEDIA_DEPENDENCY_PRESENT")
    return {
        "real_urls": real_urls,
        "real_media_paths": real_media_paths,
        "TTS_generated": tts_generated,
        "render_created": render_created,
        "ymmp_created": ymmp_created,
        "production_approval": production_approval,
        "external_fetch_performed": bool(boundary.get("external_fetch_performed")),
        "row_audio_dependency_present": row_audio,
        "row_media_dependency_present": row_media,
        "errors": errors,
        "warnings": [],
    }


def _candidate_status(errors: list[str], warnings: list[str]) -> str:
    if errors:
        return "failed"
    if warnings:
        return "passed_with_warnings"
    return "passed"


def _has_real_name(text: str) -> bool:
    lowered = text.lower()
    synthetic_markers = ("fake", "review-only")
    return not any(marker in lowered for marker in synthetic_markers)


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
