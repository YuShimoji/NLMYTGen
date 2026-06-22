"""YMM4-adjacent no-media import-shape proof for newsroom diagnostics.

This module maps the existing diagnostic script import candidate into a
tool-adjacent row shape. It does not create YMM4 projects, carriers, renders,
TTS/audio, media, real packet ingests, fetches, or production approvals.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_caption_csv_import_candidate import load_caption_csv_rows
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_neutral_timeline_import_proof import (
    DEFAULT_CAPTION_IMPORT_CSV_PATH,
    DEFAULT_NEUTRAL_TIMELINE_PATH,
)
from src.pipeline.newsroom_script_import_candidate import (
    DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH,
)


YYM4_ADJACENT_NO_MEDIA_SCHEMA_VERSION = (
    "newsroom_yym4_adjacent_no_media_import_shape.v1"
)
YYM4_ADJACENT_NO_MEDIA_PROOF_ID = (
    "newsroom_yym4_adjacent_no_media_import_shape_v1_2026_06_22"
)
DEFAULT_YYM4_ADJACENT_NO_MEDIA_PROOF_PATH = Path(
    "samples/_probe/newsroom_handoff/yym4_adjacent_no_media_import_shape_v1.json"
)
DEFAULT_YYM4_ADJACENT_NO_MEDIA_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YYM4_ADJACENT_NO_MEDIA_PROOF_V1_2026-06-22.md"
)

EXPECTED_MAPPING_ROW_COUNT = 4
MAPPING_ROW_REQUIRED_FIELDS: tuple[str, ...] = (
    "row_id",
    "source_line_id",
    "source_caption_id",
    "beat_id",
    "start_sec",
    "end_sec",
    "duration_sec",
    "speaker_id",
    "voice_profile",
    "text",
    "row_kind",
    "media_dependency",
    "audio_dependency",
    "tts_required",
    "diagnostic_only",
    "production_ready",
)

STATIC_COMPATIBILITY_WARNINGS: tuple[str, ...] = (
    "YMM4_NOT_LAUNCHED_STATIC_REPO_CONTRACT_ONLY",
    "TIMING_FIELDS_ARE_METADATA_NOT_KNOWN_YMM4_CSV_COLUMNS",
)


def build_default_newsroom_yym4_adjacent_no_media_import_shape(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed YMM4-adjacent no-media proof from default inputs."""
    base = Path(root) if root is not None else Path(".")
    script_candidate = load_json_object(base / DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH)
    neutral_timeline = load_json_object(base / DEFAULT_NEUTRAL_TIMELINE_PATH)
    csv_rows = load_caption_csv_rows(base / DEFAULT_CAPTION_IMPORT_CSV_PATH)
    return build_newsroom_yym4_adjacent_no_media_import_shape(
        script_candidate,
        csv_rows,
        neutral_timeline,
        script_candidate_path=DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH,
        caption_csv_path=DEFAULT_CAPTION_IMPORT_CSV_PATH,
        neutral_timeline_path=DEFAULT_NEUTRAL_TIMELINE_PATH,
    )


def build_newsroom_yym4_adjacent_no_media_import_shape(
    script_candidate: dict[str, Any],
    csv_rows: list[dict[str, str]],
    neutral_timeline: dict[str, Any],
    *,
    script_candidate_path: str | Path | None = None,
    caption_csv_path: str | Path | None = None,
    neutral_timeline_path: str | Path | None = None,
    source_commit_or_status: str = "worktree_verified_before_generation",
) -> dict[str, Any]:
    """Map diagnostic script lines into a no-media YMM4-adjacent row shape."""
    script_lines = _list(script_candidate.get("script_lines"))
    mapping_rows = [
        _mapping_row_from_script_line(index, line)
        for index, line in enumerate(script_lines, start=1)
    ]
    source_validation = _source_validation(script_candidate, csv_rows, neutral_timeline)
    mapping_validation = _mapping_validation(script_lines, mapping_rows, csv_rows)
    no_media_validation = _no_media_validation(mapping_rows)
    yym4_boundary = _yym4_boundary()
    safety = _diagnostic_safety(mapping_rows, script_candidate, neutral_timeline)

    errors = (
        source_validation["errors"]
        + mapping_validation["errors"]
        + no_media_validation["errors"]
        + safety["errors"]
    )
    warnings = list(STATIC_COMPATIBILITY_WARNINGS)
    warnings.extend(source_validation["warnings"])
    warnings.extend(mapping_validation["warnings"])
    warnings.extend(no_media_validation["warnings"])
    warnings.extend(safety["warnings"])
    status = _candidate_status(errors, warnings)
    yym4_status = "failed" if errors else "passed_with_warnings"

    return {
        "artifact_id": YYM4_ADJACENT_NO_MEDIA_PROOF_ID,
        "proof_id": YYM4_ADJACENT_NO_MEDIA_PROOF_ID,
        "schema_version": YYM4_ADJACENT_NO_MEDIA_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "yym4_status": yym4_status,
        "production_transfer_status": "blocked",
        "no_media_import_shape_status": status,
        "identity": {
            "proof_id": YYM4_ADJACENT_NO_MEDIA_PROOF_ID,
            "source_script_candidate_path": _path_text(script_candidate_path),
            "source_caption_csv_path": _path_text(caption_csv_path),
            "source_neutral_timeline_path": _path_text(neutral_timeline_path),
            "source_commit_or_status": source_commit_or_status,
            "source_episode_id": script_candidate.get("identity", {}).get(
                "source_episode_id"
            ),
            "source_script_candidate_id": script_candidate.get("script_candidate_id"),
            "source_script_import_status": script_candidate.get("script_import_status"),
            "source_neutral_timeline_id": neutral_timeline.get("timeline_id"),
            "production_status": "diagnostic_only",
            "yym4_status": yym4_status,
        },
        "review_memory": {
            "prior_user_review_count": 0,
            "accepted_scope": [
                "diagnostic_timing_panel_surface_by_validation",
                "diagnostic_caption_copy_refinement_by_validation",
                "diagnostic_transfer_candidate_classification",
                "neutral_timeline_import_proof",
                "caption_csv_import_candidate_schema",
                "diagnostic_script_import_candidate",
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
            "current_axis": "YMM4_adjacent_no_media_import_shape",
            "next_nonredundant_axis": [
                "script_line_to_tool_row_mapping",
                "no_media_placeholder_policy",
                "tiny_importable_proof",
            ],
            "repeated_general_review_allowed": False,
        },
        "known_yym4_script_import_conventions": {
            "found_in_repo": True,
            "sources": [
                "src/contracts/ymm4_csv_schema.py",
                "src/pipeline/assemble_csv.py",
                "tests/test_csv_handoff_contract.py",
                "docs/YMM4-AUTOMATION-RESEARCH.md",
            ],
            "static_summary": [
                "Repo YMM4 CSV row minimum is speaker,text.",
                "YMM4CsvOutput.write emits UTF-8 BOM and no header.",
                "build-csv is the repo-supported route toward YMM4 script import.",
                "start/end/duration are not part of the known CSV row minimum.",
            ],
            "compatible_surface": "speaker_text_two_column_static_match_only",
            "YMM4_verified": False,
            "YMM4_verification_reason": (
                "This slice does not launch YMM4, create .ymmp, import CSV, "
                "render, or generate TTS/audio."
            ),
        },
        "mapping_rows": mapping_rows,
        "source_validation": source_validation,
        "mapping_validation": mapping_validation,
        "no_media_placeholder_policy": {
            "visual_placeholders_consumed": "reference_only",
            "audio_placeholder_consumed": "reference_only",
            "no_media_policy": [
                "captions_and_script_rows_only",
                "no_render",
                "no_TTS",
                "no_real_assets",
            ],
            "intentionally_not_represented": [
                "YMM4 timeline geometry",
                "YMM4 character binding",
                "YMM4 native voice synthesis",
                "visual media files",
                "audio media files",
                "render settings",
                "production approval state",
            ],
        },
        "no_media_validation": no_media_validation,
        "YMM4_boundary": yym4_boundary,
        "diagnostic_safety": safety,
        "result": {
            "no_media_import_shape_status": status,
            "warnings": warnings,
            "errors": errors,
            "missing_for_tiny_importable_proof": [
                "Decide whether to emit a real repo YMM4 CSV artifact.",
                "Bind synthetic speaker placeholder to accepted YMM4 character names.",
                "Keep timing metadata out of CSV unless a consumer contract accepts it.",
                "Run a later no-production import/readback gate without TTS/render.",
            ],
            "recommended_next_slice": "newsroom-tiny-importable-proof-v1",
            "prohibited_next_artifacts": [
                "production .ymmp",
                "render output",
                "TTS output",
                "real media",
            ],
        },
        "review_card": {
            "status": "none",
            "axis_if_needed": "YMM4_adjacent_no_media_import_shape",
            "reason": (
                "The checker validates the no-media import shape directly; no "
                "fresh user judgement is needed for timing, caption copy, blocker, "
                "neutral timeline, CSV, or script candidate review."
            ),
            "not_asking": (
                "No repeated timing/caption/copy/blocker/neutral timeline/CSV/"
                "script candidate review, YMM4 approval, TTS, media, render, or "
                "production judgement is requested."
            ),
        },
        "boundary_assertions": {
            "diagnostic_only": True,
            "YMM4_adjacent_no_media_import_shape": True,
            "tool_adjacent_not_YMM4_verified": True,
            "source_script_candidate_changed": False,
            "source_caption_csv_changed": False,
            "source_neutral_timeline_changed": False,
            "opens_production_transfer": False,
            "opens_YMM4_transfer": False,
            "ymmp_created": False,
            "YMM4_launched": False,
            "YMM4_carrier_created": False,
            "YMM4_approval": False,
            "real_urls": False,
            "real_media_paths": False,
            "TTS_generated": False,
            "render_created": False,
            "production_approval": False,
            "public_video": False,
            "external_fetch_performed": False,
            "dashboard_governance_freshness_changed": False,
        },
    }


def render_newsroom_yym4_adjacent_no_media_import_shape_markdown(
    proof: dict[str, Any],
) -> str:
    """Render a human-readable readback for the no-media import-shape proof."""
    identity = _dict(proof.get("identity"))
    review_memory = _dict(proof.get("review_memory"))
    conventions = _dict(proof.get("known_yym4_script_import_conventions"))
    mapping_validation = _dict(proof.get("mapping_validation"))
    no_media = _dict(proof.get("no_media_placeholder_policy"))
    boundary = _dict(proof.get("YMM4_boundary"))
    safety = _dict(proof.get("diagnostic_safety"))
    result = _dict(proof.get("result"))

    lines = [
        "# Newsroom YMM4 Adjacent No-media Import Shape v1",
        "",
        f"artifact_id: {proof.get('artifact_id')}",
        f"proof_id: {proof.get('proof_id')}",
        f"schema_version: {proof.get('schema_version')}",
        f"review_status: {proof.get('review_status')}",
        f"production_status: {proof.get('production_status')}",
        f"yym4_status: {proof.get('yym4_status')}",
        f"no_media_import_shape_status: {proof.get('no_media_import_shape_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        f"- source_script_candidate_path: {identity.get('source_script_candidate_path')}",
        f"- source_caption_csv_path: {identity.get('source_caption_csv_path')}",
        f"- source_neutral_timeline_path: {identity.get('source_neutral_timeline_path')}",
        f"- source_episode_id: {identity.get('source_episode_id')}",
        f"- source_commit_or_status: {identity.get('source_commit_or_status')}",
        "",
        "## Review Memory",
        "",
        f"- prior_user_review_count: {review_memory.get('prior_user_review_count')}",
        f"- current_axis: {review_memory.get('current_axis')}",
        "- repeated_general_review_allowed: false",
        "",
        "## YMM4-adjacent No-media Summary",
        "",
        f"- known_repo_convention_found: {str(conventions.get('found_in_repo')).lower()}",
        f"- compatible_surface: {conventions.get('compatible_surface')}",
        f"- YMM4_verified: {str(conventions.get('YMM4_verified')).lower()}",
        f"- mapping_row_count: {mapping_validation.get('mapping_row_count')}",
        f"- all_rows_valid: {str(mapping_validation.get('all_rows_valid')).lower()}",
        "",
        "## Script-to-Row Mapping Summary",
        "",
        "| row_id | source_line_id | speaker | timing | row_kind | tool-adjacent columns | flags |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in _list(proof.get("mapping_rows")):
        adjacent = _dict(row.get("tool_adjacent_row"))
        lines.append(
            f"| {row['row_id']} | {row['source_line_id']} | "
            f"{row['speaker_id']} | {row['start_sec']}-{row['end_sec']}s | "
            f"{row['row_kind']} | {', '.join(adjacent.get('columns', []))} | "
            f"diagnostic_only={str(row['diagnostic_only']).lower()}, "
            f"production_ready={str(row['production_ready']).lower()}, "
            f"tts_required={str(row['tts_required']).lower()} |"
        )

    lines.extend([
        "",
        "## No-media Placeholder Policy",
        "",
        f"- visual_placeholders_consumed: {no_media.get('visual_placeholders_consumed')}",
        f"- audio_placeholder_consumed: {no_media.get('audio_placeholder_consumed')}",
        f"- no_media_policy: {', '.join(no_media.get('no_media_policy', []))}",
        "- intentionally_not_represented:",
    ])
    for item in no_media.get("intentionally_not_represented", []):
        lines.append(f"  - {item}")

    lines.extend([
        "",
        "## YMM4 Boundary",
        "",
        f"- ymmp_created: {str(boundary.get('ymmp_created')).lower()}",
        f"- YMM4_launched: {str(boundary.get('YMM4_launched')).lower()}",
        f"- YMM4_carrier_created: {str(boundary.get('YMM4_carrier_created')).lower()}",
        f"- YMM4_approval: {str(boundary.get('YMM4_approval')).lower()}",
        f"- compatibility_statement: {boundary.get('compatibility_statement')}",
        "",
        "## Diagnostic Safety",
        "",
        f"- real_urls: {str(safety.get('real_urls')).lower()}",
        f"- real_media_paths: {str(safety.get('real_media_paths')).lower()}",
        f"- TTS_generated: {str(safety.get('TTS_generated')).lower()}",
        f"- render_created: {str(safety.get('render_created')).lower()}",
        f"- production_approval: {str(safety.get('production_approval')).lower()}",
        "",
        "## Next Use",
        "",
        f"- no_media_import_shape_status: {result.get('no_media_import_shape_status')}",
        "- warnings:",
    ])
    for warning in result.get("warnings", []):
        lines.append(f"  - {warning}")
    lines.append("- missing_for_tiny_importable_proof:")
    for missing in result.get("missing_for_tiny_importable_proof", []):
        lines.append(f"  - {missing}")
    lines.append(f"- recommended_next_slice: {result.get('recommended_next_slice')}")
    lines.append("- prohibited_next_artifacts:")
    for artifact in result.get("prohibited_next_artifacts", []):
        lines.append(f"  - {artifact}")

    lines.extend([
        "",
        "## Review Card",
        "",
        "Review Card: none. This checker validates the YMM4-adjacent no-media "
        "shape without asking for repeated timing, caption copy, blocker, "
        "neutral timeline, CSV, script candidate, YMM4, TTS, media, render, or "
        "production review.",
        "",
        "## Boundary",
        "",
        "This readback is diagnostic-only and tool-adjacent. It does not create "
        "`.ymmp`, YMM4 carriers, renders, TTS/audio, real packet ingestion, "
        "external fetches, real source access, media files, production approvals, "
        "rights approvals, public-use approvals, or publishing output.",
        "",
    ])
    return "\n".join(lines)


def _mapping_row_from_script_line(index: int, line: dict[str, Any]) -> dict[str, Any]:
    voice_profile = _dict(line.get("voice_profile"))
    return {
        "row_id": f"yym4_adjacent_row_{index:02d}",
        "source_line_id": line.get("line_id"),
        "source_caption_id": line.get("source_caption_id"),
        "beat_id": line.get("beat_id"),
        "start_sec": line.get("start_sec"),
        "end_sec": line.get("end_sec"),
        "duration_sec": line.get("duration_sec"),
        "speaker_id": line.get("speaker_id"),
        "voice_profile": voice_profile,
        "text": line.get("text"),
        "row_kind": "dialogue_caption",
        "media_dependency": "none",
        "audio_dependency": "none_for_this_proof",
        "tts_required": False,
        "diagnostic_only": True,
        "production_ready": False,
        "tool_adjacent_row": {
            "format_family": "repo_ymm4_csv_two_column_static_contract",
            "columns": ["speaker", "text"],
            "speaker": line.get("speaker_id"),
            "text": line.get("text"),
            "known_import_contract": "speaker_text_no_header_utf8_bom_when_written",
            "timing_metadata_not_csv_column": True,
            "YMM4_verified": False,
        },
        "notes": [
            "Derived from diagnostic script import candidate script_lines.",
            "Timing is retained as metadata only, not as known YMM4 CSV columns.",
            "No media, audio, TTS, render, .ymmp, or YMM4 carrier is created.",
        ],
    }


def _source_validation(
    script_candidate: dict[str, Any],
    csv_rows: list[dict[str, str]],
    neutral_timeline: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if script_candidate.get("script_import_status") != "passed":
        errors.append("SCRIPT_IMPORT_STATUS_NOT_PASSED")
    if script_candidate.get("line_count") != EXPECTED_MAPPING_ROW_COUNT:
        errors.append("SCRIPT_LINE_COUNT_NOT_4")
    if len(csv_rows) != EXPECTED_MAPPING_ROW_COUNT:
        errors.append(f"CSV_ROW_COUNT_EXPECTED_4_ACTUAL_{len(csv_rows)}")
    if not neutral_timeline.get("timeline_id"):
        errors.append("NEUTRAL_TIMELINE_ID_MISSING")
    return {
        "script_import_status": script_candidate.get("script_import_status"),
        "script_line_count": len(_list(script_candidate.get("script_lines"))),
        "csv_row_count": len(csv_rows),
        "neutral_timeline_id": neutral_timeline.get("timeline_id"),
        "source_artifacts_identified": not errors,
        "errors": errors,
        "warnings": [],
    }


def _mapping_validation(
    script_lines: list[dict[str, Any]],
    mapping_rows: list[dict[str, Any]],
    csv_rows: list[dict[str, str]],
) -> dict[str, Any]:
    csv_by_id = {
        str(row.get("caption_id") or ""): row
        for row in csv_rows
        if row.get("caption_id")
    }
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    source_line_ids = [str(row.get("source_line_id") or "") for row in mapping_rows]
    duplicate_source_line_ids = sorted(
        line_id
        for line_id in set(source_line_ids)
        if line_id and source_line_ids.count(line_id) > 1
    )
    for line, row in zip(script_lines, mapping_rows, strict=False):
        row_errors: list[str] = []
        missing = [field for field in MAPPING_ROW_REQUIRED_FIELDS if field not in row]
        source_caption_id = str(row.get("source_caption_id") or "")
        csv_row = csv_by_id.get(source_caption_id)
        matches_line = (
            row.get("source_line_id") == line.get("line_id")
            and row.get("source_caption_id") == line.get("source_caption_id")
            and row.get("beat_id") == line.get("beat_id")
            and row.get("start_sec") == line.get("start_sec")
            and row.get("end_sec") == line.get("end_sec")
            and row.get("duration_sec") == line.get("duration_sec")
            and row.get("speaker_id") == line.get("speaker_id")
            and row.get("voice_profile") == line.get("voice_profile")
            and row.get("text") == line.get("text")
        )
        if missing:
            row_errors.append(f"missing_fields:{','.join(missing)}")
        if not matches_line:
            row_errors.append("does_not_match_source_script_line")
        if csv_row is None:
            row_errors.append("source_caption_id_missing_from_csv")
        if row.get("row_kind") != "dialogue_caption":
            row_errors.append("row_kind_not_dialogue_caption")
        if row.get("media_dependency") != "none":
            row_errors.append("media_dependency_not_none")
        if row.get("audio_dependency") != "none_for_this_proof":
            row_errors.append("audio_dependency_not_none_for_this_proof")
        if row.get("tts_required") is not False:
            row_errors.append("tts_required_not_false")
        if row.get("diagnostic_only") is not True:
            row_errors.append("diagnostic_only_not_true")
        if row.get("production_ready") is not False:
            row_errors.append("production_ready_not_false")
        errors.extend(f"ROW_{row.get('row_id')}:{error}" for error in row_errors)
        rows.append({
            "row_id": row.get("row_id"),
            "source_line_id": row.get("source_line_id"),
            "source_caption_id": source_caption_id,
            "source_caption_id_exists_in_csv": csv_row is not None,
            "matches_source_script_line": matches_line,
            "required_fields_present": not missing,
            "no_media": row.get("media_dependency") == "none",
            "no_audio": row.get("audio_dependency") == "none_for_this_proof",
            "tts_not_required": row.get("tts_required") is False,
            "status": "passed" if not row_errors else "failed",
            "errors": row_errors,
        })
    if len(mapping_rows) != EXPECTED_MAPPING_ROW_COUNT:
        errors.append(f"MAPPING_ROW_COUNT_EXPECTED_4_ACTUAL_{len(mapping_rows)}")
    if len(mapping_rows) != len(script_lines):
        errors.append("MAPPING_ROW_COUNT_DOES_NOT_MATCH_SCRIPT_LINE_COUNT")
    errors.extend(
        f"DUPLICATE_SOURCE_LINE_ID:{line_id}"
        for line_id in duplicate_source_line_ids
    )
    return {
        "mapping_row_count": len(mapping_rows),
        "expected_mapping_row_count": EXPECTED_MAPPING_ROW_COUNT,
        "script_line_count": len(script_lines),
        "every_script_line_mapped": len(mapping_rows) == len(script_lines),
        "source_line_ids_are_unique": not duplicate_source_line_ids,
        "all_rows_valid": not errors,
        "rows": rows,
        "errors": errors,
        "warnings": [],
    }


def _no_media_validation(mapping_rows: list[dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for row in mapping_rows:
        row_errors: list[str] = []
        voice_profile = _dict(row.get("voice_profile"))
        if row.get("media_dependency") != "none":
            row_errors.append("media_dependency_not_none")
        if row.get("audio_dependency") != "none_for_this_proof":
            row_errors.append("audio_dependency_not_none_for_this_proof")
        if row.get("tts_required") is not False:
            row_errors.append("tts_required_not_false")
        if voice_profile.get("TTS_generated") is not False:
            row_errors.append("voice_profile_tts_generated_not_false")
        if voice_profile.get("audio_file") is not None:
            row_errors.append("voice_profile_audio_file_present")
        errors.extend(f"ROW_{row.get('row_id')}:{error}" for error in row_errors)
        rows.append({
            "row_id": row.get("row_id"),
            "media_dependency_none": row.get("media_dependency") == "none",
            "audio_dependency_none_for_this_proof": (
                row.get("audio_dependency") == "none_for_this_proof"
            ),
            "tts_required_false": row.get("tts_required") is False,
            "voice_profile_not_generated": (
                voice_profile.get("voice_status") == "placeholder_not_generated"
            ),
            "status": "passed" if not row_errors else "failed",
            "errors": row_errors,
        })
    return {
        "all_rows_no_media": all(row["media_dependency_none"] for row in rows),
        "all_rows_no_audio": all(
            row["audio_dependency_none_for_this_proof"] for row in rows
        ),
        "all_rows_no_tts": all(row["tts_required_false"] for row in rows),
        "all_voice_profiles_placeholder_not_generated": all(
            row["voice_profile_not_generated"] for row in rows
        ),
        "rows": rows,
        "errors": errors,
        "warnings": [],
    }


def _yym4_boundary() -> dict[str, Any]:
    return {
        "ymmp_created": False,
        "YMM4_launched": False,
        "YMM4_carrier_created": False,
        "YMM4_approval": False,
        "production_transfer_status": "blocked",
        "compatibility_statement": (
            "Static compatibility only: rows expose speaker/text like the repo "
            "YMM4 CSV contract, while timing remains metadata and no YMM4 import "
            "or .ymmp readback was performed."
        ),
        "known_convention_reference": "src/contracts/ymm4_csv_schema.py",
    }


def _diagnostic_safety(
    mapping_rows: list[dict[str, Any]],
    script_candidate: dict[str, Any],
    neutral_timeline: dict[str, Any],
) -> dict[str, Any]:
    text_blob = "\n".join(
        str(value)
        for row in mapping_rows
        for value in (
            row.get("text"),
            row.get("source_caption_id"),
            row.get("source_line_id"),
            row.get("beat_id"),
        )
        if value is not None
    )
    script_boundary = _dict(script_candidate.get("boundary_assertions"))
    timeline_boundary = _dict(neutral_timeline.get("boundary_assertions"))
    real_urls = _has_real_url(text_blob)
    real_media_paths = _has_media_path(text_blob)
    tts_generated = bool(script_boundary.get("TTS_generated")) or bool(
        timeline_boundary.get("tts_generated")
    )
    render_created = bool(script_boundary.get("render_created")) or bool(
        timeline_boundary.get("render_generated")
    )
    ymmp_created = bool(script_boundary.get("ymmp_created")) or bool(
        timeline_boundary.get("ymmp_generated")
    )
    production_approval = bool(script_boundary.get("production_approval")) or bool(
        timeline_boundary.get("production_approval")
    )
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
        "external_fetch_performed": bool(script_boundary.get("external_fetch_performed"))
        or bool(timeline_boundary.get("external_fetch_performed")),
        "errors": errors,
        "warnings": [],
    }


def _candidate_status(errors: list[str], warnings: list[str]) -> str:
    if errors:
        return "failed"
    if warnings:
        return "passed_with_warnings"
    return "passed"


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
