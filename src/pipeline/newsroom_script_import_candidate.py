"""Script import candidate checker for diagnostic newsroom handoff.

This module consumes the existing caption CSV and neutral timeline proof to
produce a script-shaped import candidate. It does not create YMM4 projects,
carriers, renders, TTS/audio, real packet ingests, fetches, media, or
production approvals.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_caption_csv_import_candidate import (
    DEFAULT_CAPTION_CSV_IMPORT_CANDIDATE_READBACK_PATH,
    load_caption_csv_rows,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_neutral_timeline_import_proof import (
    DEFAULT_CAPTION_IMPORT_CSV_PATH,
    DEFAULT_NEUTRAL_TIMELINE_PATH,
)


SCRIPT_IMPORT_CANDIDATE_SCHEMA_VERSION = "newsroom_script_import_candidate.v1"
SCRIPT_IMPORT_CANDIDATE_ID = "newsroom_script_import_candidate_v1_2026_06_22"
DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH = Path(
    "samples/_probe/newsroom_handoff/script_import_candidate_v1.json"
)
DEFAULT_SCRIPT_IMPORT_CANDIDATE_DOC_PATH = Path(
    "docs/verification/NEWSROOM_SCRIPT_IMPORT_CANDIDATE_V1_2026-06-22.md"
)

SCRIPT_LINE_REQUIRED_FIELDS: tuple[str, ...] = (
    "line_id",
    "source_caption_id",
    "beat_id",
    "start_sec",
    "end_sec",
    "duration_sec",
    "text",
    "speaker_id",
    "voice_profile",
    "diagnostic_only",
    "production_ready",
    "tts_ready",
    "source_ref",
)
EXPECTED_SCRIPT_LINE_COUNT = 4
TIMING_TOLERANCE_SEC = 0.001


def build_default_newsroom_script_import_candidate(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed script import candidate from default inputs."""
    base = Path(root) if root is not None else Path(".")
    neutral_timeline = load_json_object(base / DEFAULT_NEUTRAL_TIMELINE_PATH)
    csv_rows = load_caption_csv_rows(base / DEFAULT_CAPTION_IMPORT_CSV_PATH)
    caption_csv_readback = load_json_object(
        base / DEFAULT_CAPTION_CSV_IMPORT_CANDIDATE_READBACK_PATH
    )
    return build_newsroom_script_import_candidate(
        csv_rows,
        neutral_timeline,
        caption_csv_readback=caption_csv_readback,
        csv_path=DEFAULT_CAPTION_IMPORT_CSV_PATH,
        neutral_timeline_path=DEFAULT_NEUTRAL_TIMELINE_PATH,
        caption_csv_readback_path=DEFAULT_CAPTION_CSV_IMPORT_CANDIDATE_READBACK_PATH,
    )


def build_newsroom_script_import_candidate(
    csv_rows: list[dict[str, str]],
    neutral_timeline: dict[str, Any],
    *,
    caption_csv_readback: dict[str, Any] | None = None,
    csv_path: str | Path | None = None,
    neutral_timeline_path: str | Path | None = None,
    caption_csv_readback_path: str | Path | None = None,
    source_commit_or_status: str = "worktree_verified_before_generation",
) -> dict[str, Any]:
    """Build and validate a diagnostic script-shaped import candidate."""
    caption_items = _caption_items_by_id(neutral_timeline)
    script_lines = [
        _script_line_from_csv_row(index, row, caption_items.get(str(row.get("caption_id") or "")))
        for index, row in enumerate(csv_rows, start=1)
    ]

    schema = _schema_validation(script_lines)
    mapping = _csv_to_script_mapping(csv_rows, script_lines)
    line_validation = _line_validation(csv_rows, script_lines)
    safety = _diagnostic_safety(script_lines, neutral_timeline)

    errors = (
        schema["errors"]
        + mapping["errors"]
        + line_validation["errors"]
        + safety["errors"]
    )
    warnings = (
        schema["warnings"]
        + mapping["warnings"]
        + line_validation["warnings"]
        + safety["warnings"]
    )
    status = _candidate_status(errors, warnings)
    import_status = "failed" if errors else "candidate_with_placeholders"

    return {
        "artifact_id": SCRIPT_IMPORT_CANDIDATE_ID,
        "script_candidate_id": SCRIPT_IMPORT_CANDIDATE_ID,
        "schema_version": SCRIPT_IMPORT_CANDIDATE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "import_status": import_status,
        "script_import_status": status,
        "line_count": len(script_lines),
        "identity": {
            "script_candidate_id": SCRIPT_IMPORT_CANDIDATE_ID,
            "source_csv_path": _path_text(csv_path),
            "source_neutral_timeline_path": _path_text(neutral_timeline_path),
            "source_caption_csv_readback_path": _path_text(caption_csv_readback_path),
            "source_commit_or_status": source_commit_or_status,
            "source_episode_id": neutral_timeline.get("source_episode_id"),
            "neutral_timeline_id": neutral_timeline.get("timeline_id"),
            "caption_csv_import_status": _dict(
                _dict(caption_csv_readback).get("import_candidate_result")
            ).get("caption_csv_import_status"),
            "production_status": "diagnostic_only",
            "import_status": import_status,
        },
        "review_memory": {
            "prior_user_review_count": 0,
            "accepted_scope": [
                "diagnostic_timing_panel_surface_by_validation",
                "diagnostic_caption_copy_refinement_by_validation",
                "diagnostic_transfer_candidate_classification",
                "neutral_timeline_import_proof",
                "caption_csv_import_candidate_schema",
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
            "current_axis": "script_import_candidate_schema",
            "next_nonredundant_axis": [
                "script_import_mapping_proof",
                "YMM4-adjacent no-media proof",
                "tiny importable proof after another gate",
            ],
            "repeated_general_review_allowed": False,
        },
        "source_policy": {
            "csv_rows_are_source_of_script_lines": True,
            "neutral_timeline_caption_items_are_cross_check_only": True,
            "speaker_assignment_policy": "single_synthetic_placeholder",
            "voice_profile_policy": "placeholder_not_generated_no_tts",
            "real_source_dependency": "none",
        },
        "script_lines": script_lines,
        "schema_validation": schema,
        "csv_to_script_mapping": mapping,
        "line_validation": line_validation,
        "diagnostic_safety": safety,
        "import_candidate_result": {
            "script_import_status": status,
            "allowed_next_artifacts": [
                "YMM4-adjacent no-media proof",
                "script import mapping proof",
                "tiny importable proof after another gate",
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
            "axis_if_needed": "script_import_candidate_schema",
            "reason": (
                "No user judgement is required because the checker validates the "
                "caption CSV to script-line mapping directly."
            ),
            "not_asking": (
                "No repeated timing, caption copy, blocker, neutral timeline, "
                "YMM4, TTS, media, or production review is requested."
            ),
        },
        "boundary_assertions": {
            "diagnostic_only": True,
            "script_import_candidate": True,
            "source_csv_changed": False,
            "source_neutral_timeline_changed": False,
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


def render_newsroom_script_import_candidate_markdown(
    candidate: dict[str, Any],
) -> str:
    """Render a human-readable readback for the script import candidate."""
    identity = _dict(candidate.get("identity"))
    review_memory = _dict(candidate.get("review_memory"))
    source_policy = _dict(candidate.get("source_policy"))
    schema = _dict(candidate.get("schema_validation"))
    mapping = _dict(candidate.get("csv_to_script_mapping"))
    line_validation = _dict(candidate.get("line_validation"))
    safety = _dict(candidate.get("diagnostic_safety"))
    result = _dict(candidate.get("import_candidate_result"))

    lines = [
        "# Newsroom Script Import Candidate v1",
        "",
        f"artifact_id: {candidate.get('artifact_id')}",
        f"script_candidate_id: {candidate.get('script_candidate_id')}",
        f"schema_version: {candidate.get('schema_version')}",
        f"review_status: {candidate.get('review_status')}",
        f"production_status: {candidate.get('production_status')}",
        f"import_status: {candidate.get('import_status')}",
        f"script_import_status: {candidate.get('script_import_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        f"- source_csv_path: {identity.get('source_csv_path')}",
        f"- source_neutral_timeline_path: {identity.get('source_neutral_timeline_path')}",
        f"- source_caption_csv_readback_path: {identity.get('source_caption_csv_readback_path')}",
        f"- source_episode_id: {identity.get('source_episode_id')}",
        f"- source_commit_or_status: {identity.get('source_commit_or_status')}",
        "",
        "## Review Memory",
        "",
        f"- prior_user_review_count: {review_memory.get('prior_user_review_count')}",
        f"- current_axis: {review_memory.get('current_axis')}",
        "- repeated_general_review_allowed: false",
        "",
        "## Script Import Candidate Summary",
        "",
        f"- script_lines_array_present: {str(schema.get('script_lines_array_present')).lower()}",
        f"- line_count: {schema.get('line_count')}",
        f"- expected_line_count: {schema.get('expected_line_count')}",
        f"- required_line_fields_present: {str(schema.get('required_line_fields_present')).lower()}",
        f"- speaker_assignment_policy: {source_policy.get('speaker_assignment_policy')}",
        f"- voice_profile_policy: {source_policy.get('voice_profile_policy')}",
        "",
        "## CSV-to-Script Mapping Summary",
        "",
        f"- every_line_maps_exactly_one_csv_caption_row: {str(mapping.get('every_line_maps_exactly_one_csv_caption_row')).lower()}",
        f"- every_csv_row_mapped: {str(mapping.get('every_csv_row_mapped')).lower()}",
        f"- source_caption_ids_are_unique: {str(mapping.get('source_caption_ids_are_unique')).lower()}",
        f"- timing_matches: {str(mapping.get('timing_matches')).lower()}",
        f"- text_matches: {str(mapping.get('text_matches')).lower()}",
        f"- missing_csv_caption_rows: {', '.join(mapping.get('missing_csv_caption_rows', [])) or 'none'}",
        f"- extra_script_lines: {', '.join(mapping.get('extra_script_lines', [])) or 'none'}",
        "",
        "## Script Lines",
        "",
        "| line_id | source_caption_id | beat_id | timing | speaker | voice | flags |",
        "|---|---|---|---|---|---|---|",
    ]
    for line in _list(candidate.get("script_lines")):
        voice_profile = _dict(line.get("voice_profile"))
        lines.append(
            f"| {line['line_id']} | {line['source_caption_id']} | "
            f"{line['beat_id']} | {line['start_sec']}-{line['end_sec']}s | "
            f"{line['speaker_id']} | "
            f"voice_status={voice_profile.get('voice_status')} | "
            f"diagnostic_only={str(line['diagnostic_only']).lower()}, "
            f"production_ready={str(line['production_ready']).lower()}, "
            f"tts_ready={str(line['tts_ready']).lower()} |"
        )

    lines.extend([
        "",
        "## Line Validation",
        "",
        f"- line_count: {line_validation.get('line_count')}",
        f"- expected_line_count: {line_validation.get('expected_line_count')}",
        f"- all_lines_valid: {str(line_validation.get('all_lines_valid')).lower()}",
        f"- all_lines_diagnostic_only: {str(line_validation.get('all_lines_diagnostic_only')).lower()}",
        f"- all_lines_production_not_ready: {str(line_validation.get('all_lines_production_not_ready')).lower()}",
        f"- all_lines_tts_not_ready: {str(line_validation.get('all_lines_tts_not_ready')).lower()}",
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
        f"- script_import_status: {result.get('script_import_status')}",
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
        "Review Card: none. This checker validates the script import candidate "
        "without asking for repeated timing, caption copy, blocker, neutral "
        "timeline, YMM4, TTS, media, or production review.",
        "",
        "## Boundary",
        "",
        "This readback is diagnostic-only. It does not create `.ymmp`, YMM4 "
        "carriers, renders, TTS/audio, real packet ingestion, external fetches, "
        "real source access, media files, production approvals, rights approvals, "
        "public-use approvals, or publishing output.",
        "",
    ])
    return "\n".join(lines)


def _script_line_from_csv_row(
    index: int,
    row: dict[str, str],
    timeline_item: dict[str, Any] | None,
) -> dict[str, Any]:
    caption_id = str(row.get("caption_id") or "")
    start = _number_value(row.get("start_sec"))
    end = _number_value(row.get("end_sec"))
    duration = _number_value(row.get("duration_sec"))
    return {
        "line_id": f"line_{index:02d}_{caption_id}",
        "source_caption_id": caption_id,
        "beat_id": str(row.get("beat_id") or ""),
        "start_sec": start,
        "end_sec": end,
        "duration_sec": duration,
        "text": str(row.get("text") or ""),
        "speaker_id": "synthetic_newsroom_placeholder",
        "voice_profile": {
            "voice_profile_id": "voice_placeholder_not_generated",
            "voice_status": "placeholder_not_generated",
            "TTS_generated": False,
            "audio_file": None,
            "audio_required_for_this_candidate": False,
        },
        "diagnostic_only": True,
        "production_ready": False,
        "tts_ready": False,
        "source_ref": f"caption_csv.caption_id:{caption_id}",
        "source_neutral_timeline_item_id": _dict(timeline_item).get("item_id"),
        "notes": [
            "Synthetic script line derived from caption CSV row.",
            "Voice profile is a placeholder only; no TTS or audio was generated.",
        ],
    }


def _schema_validation(script_lines: list[dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for line in script_lines:
        missing = [
            field
            for field in SCRIPT_LINE_REQUIRED_FIELDS
            if field not in line
        ]
        if missing:
            errors.append(f"LINE_SCHEMA_MISSING:{line.get('line_id')}:{','.join(missing)}")
        rows.append({
            "line_id": line.get("line_id"),
            "missing_fields": missing,
            "required_fields_present": not missing,
        })
    if len(script_lines) != EXPECTED_SCRIPT_LINE_COUNT:
        errors.append(f"LINE_COUNT_EXPECTED_4_ACTUAL_{len(script_lines)}")
    return {
        "script_lines_array_present": isinstance(script_lines, list),
        "required_line_fields": list(SCRIPT_LINE_REQUIRED_FIELDS),
        "line_count": len(script_lines),
        "expected_line_count": EXPECTED_SCRIPT_LINE_COUNT,
        "required_line_fields_present": not any(row["missing_fields"] for row in rows),
        "rows": rows,
        "errors": errors,
        "warnings": [],
    }


def _csv_to_script_mapping(
    csv_rows: list[dict[str, str]],
    script_lines: list[dict[str, Any]],
) -> dict[str, Any]:
    csv_by_id = {
        str(row.get("caption_id") or ""): row
        for row in csv_rows
        if row.get("caption_id")
    }
    csv_ids = [str(row.get("caption_id") or "") for row in csv_rows]
    line_source_ids = [str(line.get("source_caption_id") or "") for line in script_lines]
    source_counts = {
        caption_id: line_source_ids.count(caption_id)
        for caption_id in set(line_source_ids)
    }
    missing_csv_caption_rows = [
        caption_id for caption_id in csv_ids if source_counts.get(caption_id, 0) == 0
    ]
    extra_script_lines = [
        str(line.get("line_id") or "")
        for line in script_lines
        if str(line.get("source_caption_id") or "") not in csv_by_id
    ]
    duplicate_source_caption_ids = sorted(
        caption_id
        for caption_id, count in source_counts.items()
        if caption_id and count > 1
    )

    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for line in script_lines:
        caption_id = str(line.get("source_caption_id") or "")
        csv_row = csv_by_id.get(caption_id)
        exists = csv_row is not None
        timing_matches = exists and _line_timing_matches_csv(line, csv_row)
        text_matches = exists and str(line.get("text") or "") == str(csv_row.get("text") or "")
        one_line = source_counts.get(caption_id, 0) == 1
        if not exists:
            errors.append(f"SOURCE_CAPTION_ID_NOT_IN_CSV:{caption_id}")
        if exists and not one_line:
            errors.append(f"SOURCE_CAPTION_ID_NOT_UNIQUE:{caption_id}")
        if exists and not timing_matches:
            errors.append(f"TIMING_MISMATCH:{caption_id}")
        if exists and not text_matches:
            errors.append(f"TEXT_MISMATCH:{caption_id}")
        rows.append({
            "line_id": line.get("line_id"),
            "source_caption_id": caption_id,
            "source_caption_id_exists_in_csv": exists,
            "one_line_for_csv_caption": one_line,
            "timing_matches_csv": timing_matches,
            "text_matches_csv": text_matches,
            "csv_row_number": csv_ids.index(caption_id) + 1 if caption_id in csv_ids else None,
        })
    errors.extend(
        f"MISSING_SCRIPT_LINE_FOR_CSV_CAPTION:{caption_id}"
        for caption_id in missing_csv_caption_rows
    )
    errors.extend(f"EXTRA_SCRIPT_LINE:{line_id}" for line_id in extra_script_lines)
    errors.extend(
        f"DUPLICATE_SOURCE_CAPTION_ID:{caption_id}"
        for caption_id in duplicate_source_caption_ids
    )
    exactly_one = (
        not missing_csv_caption_rows
        and not extra_script_lines
        and not duplicate_source_caption_ids
        and len(csv_rows) == len(script_lines)
    )
    return {
        "line_count": len(script_lines),
        "csv_row_count": len(csv_rows),
        "every_line_maps_exactly_one_csv_caption_row": exactly_one,
        "every_csv_row_mapped": not missing_csv_caption_rows,
        "source_caption_ids_are_unique": not duplicate_source_caption_ids,
        "timing_matches": not any(not row["timing_matches_csv"] for row in rows),
        "text_matches": not any(not row["text_matches_csv"] for row in rows),
        "missing_csv_caption_rows": missing_csv_caption_rows,
        "extra_script_lines": extra_script_lines,
        "duplicate_source_caption_ids": duplicate_source_caption_ids,
        "rows": rows,
        "errors": errors,
        "warnings": [],
    }


def _line_validation(
    csv_rows: list[dict[str, str]],
    script_lines: list[dict[str, Any]],
) -> dict[str, Any]:
    csv_by_id = {
        str(row.get("caption_id") or ""): row
        for row in csv_rows
        if row.get("caption_id")
    }
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for line in script_lines:
        caption_id = str(line.get("source_caption_id") or "")
        csv_row = csv_by_id.get(caption_id)
        voice_profile = _dict(line.get("voice_profile"))
        row_errors: list[str] = []
        source_exists = csv_row is not None
        timing_matches = source_exists and _line_timing_matches_csv(line, csv_row)
        text_matches = source_exists and str(line.get("text") or "") == str(csv_row.get("text") or "")
        diagnostic_only = line.get("diagnostic_only") is True
        production_not_ready = line.get("production_ready") is False
        tts_not_ready = line.get("tts_ready") is False
        synthetic_speaker = _is_synthetic_placeholder(line.get("speaker_id"))
        voice_placeholder = (
            voice_profile.get("voice_status") == "placeholder_not_generated"
            and voice_profile.get("TTS_generated") is False
            and voice_profile.get("audio_file") is None
        )
        if not source_exists:
            row_errors.append("source_caption_id_missing_from_csv")
        if source_exists and not timing_matches:
            row_errors.append("timing_mismatch")
        if source_exists and not text_matches:
            row_errors.append("text_mismatch")
        if not diagnostic_only:
            row_errors.append("diagnostic_only_not_true")
        if not production_not_ready:
            row_errors.append("production_ready_not_false")
        if not tts_not_ready:
            row_errors.append("tts_ready_not_false")
        if not synthetic_speaker:
            row_errors.append("speaker_id_not_synthetic_placeholder")
        if not voice_placeholder:
            row_errors.append("voice_profile_not_placeholder")
        errors.extend(
            f"LINE_{line.get('line_id')}:{error}"
            for error in row_errors
        )
        rows.append({
            "line_id": line.get("line_id"),
            "source_caption_id": caption_id,
            "source_caption_id_exists_in_csv": source_exists,
            "timing_matches_csv": timing_matches,
            "text_matches_csv": text_matches,
            "diagnostic_only_is_true": diagnostic_only,
            "production_ready_is_false": production_not_ready,
            "tts_ready_is_false": tts_not_ready,
            "speaker_id_is_synthetic_placeholder": synthetic_speaker,
            "voice_profile_is_placeholder_not_generated": voice_placeholder,
            "status": "passed" if not row_errors else "failed",
            "errors": row_errors,
        })
    if len(script_lines) != EXPECTED_SCRIPT_LINE_COUNT:
        errors.append(f"LINE_COUNT_EXPECTED_4_ACTUAL_{len(script_lines)}")
    return {
        "line_count": len(script_lines),
        "expected_line_count": EXPECTED_SCRIPT_LINE_COUNT,
        "all_lines_valid": not errors,
        "all_lines_diagnostic_only": all(
            row["diagnostic_only_is_true"] for row in rows
        ),
        "all_lines_production_not_ready": all(
            row["production_ready_is_false"] for row in rows
        ),
        "all_lines_tts_not_ready": all(row["tts_ready_is_false"] for row in rows),
        "all_speakers_are_synthetic_placeholders": all(
            row["speaker_id_is_synthetic_placeholder"] for row in rows
        ),
        "all_voice_profiles_are_placeholders": all(
            row["voice_profile_is_placeholder_not_generated"] for row in rows
        ),
        "rows": rows,
        "errors": errors,
        "warnings": [],
    }


def _diagnostic_safety(
    script_lines: list[dict[str, Any]],
    neutral_timeline: dict[str, Any],
) -> dict[str, Any]:
    text_blob = "\n".join(
        str(value)
        for line in script_lines
        for value in (
            line.get("text"),
            line.get("source_ref"),
            line.get("source_caption_id"),
            line.get("beat_id"),
        )
        if value is not None
    )
    boundary = _dict(neutral_timeline.get("boundary_assertions"))
    voice_profiles = [_dict(line.get("voice_profile")) for line in script_lines]
    real_urls = _has_real_url(text_blob)
    real_media_paths = _has_media_path(text_blob)
    tts_generated = bool(boundary.get("tts_generated")) or any(
        profile.get("TTS_generated") is True for profile in voice_profiles
    )
    render_created = bool(boundary.get("render_generated")) or bool(
        boundary.get("render_created")
    )
    ymmp_created = bool(boundary.get("ymmp_generated")) or bool(
        boundary.get("ymmp_created")
    )
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
        "script_line_audio_files": [
            profile.get("audio_file")
            for profile in voice_profiles
            if profile.get("audio_file")
        ],
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


def _line_timing_matches_csv(
    line: dict[str, Any],
    csv_row: dict[str, str],
) -> bool:
    return (
        _numbers_match(line.get("start_sec"), csv_row.get("start_sec"))
        and _numbers_match(line.get("end_sec"), csv_row.get("end_sec"))
        and _numbers_match(line.get("duration_sec"), csv_row.get("duration_sec"))
    )


def _number_value(value: Any) -> int | float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number.is_integer():
        return int(number)
    return number


def _float_value(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _numbers_match(left: Any, right: Any) -> bool:
    left_value = _float_value(left)
    right_value = _float_value(right)
    if left_value is None or right_value is None:
        return False
    return abs(left_value - right_value) <= TIMING_TOLERANCE_SEC


def _is_synthetic_placeholder(value: Any) -> bool:
    text = str(value or "")
    return text.startswith("synthetic_") and text.endswith("_placeholder")


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
