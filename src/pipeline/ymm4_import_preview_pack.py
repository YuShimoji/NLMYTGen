"""Local/offline YMM4 import preview package for content-spine pilots.

This package aggregates the current draft CSV, cue packet, Writer IR, transcript
readiness, and dashboard panel state. It never launches YMM4, imports into a
project, renders video, or claims production/public readiness.
"""

from __future__ import annotations

import csv
import html
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

from src.pipeline.dashboard_readiness_ingest import STATUS_CATEGORIES

DEFAULT_OUTPUT_DIRNAME = "ymm4_import_preview_pack"
DEFAULT_ARTIFACT_ID = "ymm4_import_preview_pack_001"

PREVIEW_CSV_FILENAME = "draft_yymm4_import_preview.csv"

REQUIRED_IMPORT_PREVIEW_FILES = (
    "import_preview_manifest.json",
    "yymm4_csv_inventory.json",
    "cue_packet_inventory.json",
    "writer_ir_inventory.json",
    "import_readiness_summary.json",
    "import_preview_checklist.md",
    "import_preview_panel.md",
    "import_preview_panel.html",
    "source_artifact_index.json",
    "validation_readback.json",
    "limitations.md",
    PREVIEW_CSV_FILENAME,
)

REQUIRED_HTML_MARKERS = (
    'data-import-preview-pack="true"',
    'data-section="readiness-grid"',
    'data-section="csv-contract"',
    'data-section="source-artifact-index"',
    'data-section="boundary-status"',
    'data-status="ready"',
    'data-status="partial"',
    'data-status="sample_fixture_not_real"',
    'data-status="draft_offline"',
    'data-status="blocked_by_real_input"',
    'data-status="blocked_by_true_gate"',
    'data-status="deferred"',
    'data-status="missing"',
    'data-status="unknown"',
)


def build_ymm4_import_preview_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a static local/offline YMM4 import preview package."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)

    repo_root = _find_repo_root(source_root)
    snapshot = _load_snapshot(source_root)
    copied_csv_path = output_root / PREVIEW_CSV_FILENAME
    if snapshot["files"]["draft_csv"].exists():
        shutil.copyfile(snapshot["files"]["draft_csv"], copied_csv_path)

    csv_inventory = _csv_inventory(
        csv_path=snapshot["files"]["draft_csv"],
        copied_csv_path=copied_csv_path,
        repo_root=repo_root,
    )
    cue_inventory = _cue_packet_inventory(snapshot, repo_root)
    writer_ir_inventory = _writer_ir_inventory(snapshot, repo_root)
    readiness_rows = _readiness_rows(
        snapshot=snapshot,
        csv_inventory=csv_inventory,
        cue_inventory=cue_inventory,
        writer_ir_inventory=writer_ir_inventory,
        repo_root=repo_root,
    )
    readiness_summary = _readiness_summary_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        snapshot=snapshot,
        csv_inventory=csv_inventory,
        cue_inventory=cue_inventory,
        writer_ir_inventory=writer_ir_inventory,
        rows=readiness_rows,
    )
    manifest = _manifest_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        snapshot=snapshot,
        readiness_summary=readiness_summary,
        csv_inventory=csv_inventory,
    )
    panel_data = {
        "schema_version": "ymm4_import_preview_panel_data.v1",
        "artifact_id": artifact_id,
        "selected_candidate_id": readiness_summary.get("selected_candidate_id"),
        "status_categories": list(STATUS_CATEGORIES),
        "readiness_rows": readiness_rows,
        "boundary_status": readiness_summary["boundary_status"],
        "status_groups": readiness_summary["status_groups"],
        "csv_inventory": csv_inventory,
        "cue_packet_inventory": cue_inventory,
        "writer_ir_inventory": writer_ir_inventory,
        "next_action": readiness_summary["next_safe_local_action"],
    }

    _write_json(output_root / "import_preview_manifest.json", manifest)
    _write_json(output_root / "yymm4_csv_inventory.json", csv_inventory)
    _write_json(output_root / "cue_packet_inventory.json", cue_inventory)
    _write_json(output_root / "writer_ir_inventory.json", writer_ir_inventory)
    _write_json(output_root / "import_readiness_summary.json", readiness_summary)
    _write_text(output_root / "import_preview_checklist.md", _render_checklist(readiness_summary, readiness_rows))
    _write_text(output_root / "import_preview_panel.md", _render_markdown_panel(panel_data))
    _write_text(output_root / "import_preview_panel.html", _render_html_panel(panel_data))
    _write_text(output_root / "limitations.md", _render_limitations(readiness_summary))
    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(snapshot, output_root, repo_root))

    readback = validate_ymm4_import_preview_pack(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(snapshot, output_root, repo_root))
    final_readback = validate_ymm4_import_preview_pack(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(snapshot, output_root, repo_root))
    return final_readback


def validate_ymm4_import_preview_pack(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate a generated YMM4 import preview package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_IMPORT_PREVIEW_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["import_preview_manifest.json"])
    csv_inventory = _load_json_if_present(files["yymm4_csv_inventory.json"])
    cue_inventory = _load_json_if_present(files["cue_packet_inventory.json"])
    writer_inventory = _load_json_if_present(files["writer_ir_inventory.json"])
    summary = _load_json_if_present(files["import_readiness_summary.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])

    json_payloads = {
        "import_preview_manifest": manifest,
        "yymm4_csv_inventory": csv_inventory,
        "cue_packet_inventory": cue_inventory,
        "writer_ir_inventory": writer_inventory,
        "import_readiness_summary": summary,
        "source_artifact_index": source_index,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["import_preview_manifest"]
    csv_inventory = json_payloads["yymm4_csv_inventory"]
    cue_inventory = json_payloads["cue_packet_inventory"]
    writer_inventory = json_payloads["writer_ir_inventory"]
    summary = json_payloads["import_readiness_summary"]
    source_index = json_payloads["source_artifact_index"]

    if manifest.get("artifact_kind") != "ymm4-import-preview-pack":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if csv_inventory.get("row_count", 0) <= 0:
        failed_checks.append("csv_row_count_empty")
    if csv_inventory.get("column_count_ok") is not True:
        failed_checks.append("csv_column_count_not_ok")
    if csv_inventory.get("copied_csv_exists") is not True or not files[PREVIEW_CSV_FILENAME].exists():
        failed_checks.append("copied_csv_missing")
    if csv_inventory.get("csv_contract", {}).get("header_mode") != "headerless_yymm4_csv":
        failed_checks.append("csv_header_mode_unexpected")
    if cue_inventory.get("transcript_row_count") != csv_inventory.get("row_count"):
        failed_checks.append("cue_csv_row_count_mismatch")
    if writer_inventory.get("utterance_count") != csv_inventory.get("row_count"):
        failed_checks.append("writer_ir_csv_row_count_mismatch")

    boundary_status = summary.get("boundary_status", {})
    if boundary_status.get("transcript_status") != "sample_fixture_not_real":
        failed_checks.append("sample_fixture_status_not_preserved")
    if boundary_status.get("public_upload_status") != "blocked_by_true_gate":
        failed_checks.append("public_upload_gate_not_closed")
    if boundary_status.get("ymm4_render_status") != "blocked_by_true_gate":
        failed_checks.append("ymm4_render_gate_not_closed")
    if boundary_status.get("ymm4_gui_status") != "blocked_by_true_gate":
        failed_checks.append("ymm4_gui_gate_not_closed")
    if boundary_status.get("production_status") != "blocked_by_true_gate":
        failed_checks.append("production_gate_not_closed")

    rows = summary.get("readiness_rows", [])
    row_states = {row.get("state") for row in rows if isinstance(row, dict)}
    missing_states = [state for state in STATUS_CATEGORIES if state not in row_states]
    failed_checks.extend(f"missing_visible_state:{state}" for state in missing_states)

    html_text = files["import_preview_panel.html"].read_text(encoding="utf-8") if files["import_preview_panel.html"].exists() else ""
    markdown_text = files["import_preview_panel.md"].read_text(encoding="utf-8") if files["import_preview_panel.md"].exists() else ""
    missing_markers = [marker for marker in REQUIRED_HTML_MARKERS if marker not in html_text]
    failed_checks.extend(f"missing_html_marker:{marker}" for marker in missing_markers)
    for state in STATUS_CATEGORIES:
        if state not in html_text or state not in markdown_text:
            failed_checks.append(f"panel_state_text_missing:{state}")
    if "source_artifact_index" not in html_text:
        failed_checks.append("html_source_artifact_index_missing")
    if not source_index.get("source_inputs"):
        failed_checks.append("source_artifact_index_empty")

    return {
        "schema_version": "ymm4_import_preview_pack_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
            "csv_rows_present": csv_inventory.get("row_count", 0) > 0,
            "csv_column_count_ok": csv_inventory.get("column_count_ok") is True,
            "sample_fixture_preserved": boundary_status.get("transcript_status") == "sample_fixture_not_real",
            "required_status_categories_visible": not missing_states,
            "html_markers_present": not missing_markers,
            "public_upload_gate_closed": boundary_status.get("public_upload_status") == "blocked_by_true_gate",
            "ymm4_gui_gate_closed": boundary_status.get("ymm4_gui_status") == "blocked_by_true_gate",
            "ymm4_render_gate_closed": boundary_status.get("ymm4_render_status") == "blocked_by_true_gate",
            "source_artifact_index_present": bool(source_index.get("source_inputs")),
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "source_package_dir": manifest.get("source_package_dir"),
        "selected_candidate_id": summary.get("selected_candidate_id"),
        "transcript_status": boundary_status.get("transcript_status"),
        "draft_csv_rows": csv_inventory.get("row_count"),
        "copied_csv_path": csv_inventory.get("copied_csv_path"),
        "primary_machine_readable": str(root / "import_readiness_summary.json"),
        "primary_human_review": str(root / "import_preview_panel.md"),
        "primary_human_review_html": str(root / "import_preview_panel.html"),
        "next_action": summary.get("next_safe_local_action"),
    }


def _load_snapshot(source_root: Path) -> dict[str, Any]:
    transcript_root = source_root / "transcript_substitution_readiness"
    dashboard_root = source_root / "dashboard_readiness_ingest"
    gui_root = source_root / "gui_dashboard_panel"
    files = {
        "transcript_manifest": transcript_root / "substitution_manifest.json",
        "transcript_probe": transcript_root / "transcript_source_probe.json",
        "transcript_readback": transcript_root / "validation_readback.json",
        "cue_packet_readiness": transcript_root / "cue_packet_readiness.json",
        "writer_ir": transcript_root / "regenerated_writer_ir_candidate.json",
        "cue_packet": transcript_root / "regenerated_cue_packet_candidate.json",
        "draft_csv": transcript_root / "regenerated_draft_yymm4.csv",
        "episode_bridge": transcript_root / "regenerated_episode_bridge.json",
        "dashboard_summary": dashboard_root / "readiness_summary.json",
        "dashboard_source_index": dashboard_root / "source_artifact_index.json",
        "dashboard_readback": dashboard_root / "validation_readback.json",
        "gui_adapter": gui_root / "gui_dashboard_adapter.json",
        "gui_panel_html": gui_root / "dashboard_panel_preview.html",
        "gui_readback": gui_root / "validation_readback.json",
    }
    payloads = {
        name: _load_json_if_present(path)
        for name, path in files.items()
        if path.suffix.lower() == ".json"
    }
    return {
        "source_root": source_root,
        "transcript_root": transcript_root,
        "dashboard_root": dashboard_root,
        "gui_root": gui_root,
        "files": files,
        "payloads": payloads,
    }


def _csv_inventory(*, csv_path: Path, copied_csv_path: Path, repo_root: Path) -> dict[str, Any]:
    rows = _read_csv_rows(csv_path)
    first_row = rows[0] if rows else []
    header_present = [cell.strip().lower() for cell in first_row[:2]] == ["speaker", "text"]
    data_rows = rows[1:] if header_present else rows
    non_empty_rows = [row for row in data_rows if any(cell.strip() for cell in row)]
    column_counts = Counter(len(row) for row in non_empty_rows)
    speaker_counts = Counter(row[0].strip() for row in non_empty_rows if row)
    malformed_rows = [
        {"row_number": index + (2 if header_present else 1), "column_count": len(row)}
        for index, row in enumerate(non_empty_rows)
        if len(row) != 2
    ]
    blank_speaker_rows = [
        index + (2 if header_present else 1)
        for index, row in enumerate(non_empty_rows)
        if len(row) < 1 or not row[0].strip()
    ]
    blank_text_rows = [
        index + (2 if header_present else 1)
        for index, row in enumerate(non_empty_rows)
        if len(row) < 2 or not row[1].strip()
    ]
    required_headers = ["speaker", "text"]
    missing_headers = [] if header_present else required_headers
    return {
        "schema_version": "yymm4_csv_inventory.v1",
        "source_csv_path": _relpath(csv_path, repo_root),
        "source_csv_exists": csv_path.exists(),
        "copied_csv_path": _relpath(copied_csv_path, repo_root),
        "copied_csv_exists": copied_csv_path.exists(),
        "row_count": len(non_empty_rows),
        "raw_row_count": len(rows),
        "header_present": header_present,
        "csv_contract": {
            "format": "YMM4 script import CSV",
            "encoding": "utf-8",
            "column_count": 2,
            "required_columns": ["speaker", "text"],
            "required_headers": required_headers,
            "headers_required_for_yymm4_import": False,
            "header_mode": "headerless_yymm4_csv",
            "missing_headers": missing_headers,
            "missing_headers_block_import": False,
        },
        "column_count_ok": bool(non_empty_rows) and not malformed_rows,
        "malformed_rows": malformed_rows,
        "blank_speaker_rows": blank_speaker_rows,
        "blank_text_rows": blank_text_rows,
        "speaker_counts": dict(sorted(speaker_counts.items())),
        "column_count_distribution": {str(key): value for key, value in sorted(column_counts.items())},
        "sample_rows": [
            {
                "speaker": row[0] if len(row) > 0 else "",
                "text": row[1] if len(row) > 1 else "",
            }
            for row in non_empty_rows[:3]
        ],
        "state": "draft_offline" if non_empty_rows else "missing",
        "status_note": "headerless two-column draft CSV; no YMM4 import or VoiceItem timing proof has been run",
    }


def _cue_packet_inventory(snapshot: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    cue = _payload(snapshot, "cue_packet")
    readiness = _payload(snapshot, "cue_packet_readiness")
    transcript_rows = cue.get("transcript", [])
    sections = cue.get("context", {}).get("sections", [])
    return {
        "schema_version": "cue_packet_inventory.v1",
        "cue_packet_path": _relpath(snapshot["files"]["cue_packet"], repo_root),
        "cue_packet_exists": snapshot["files"]["cue_packet"].exists(),
        "cue_packet_readiness_path": _relpath(snapshot["files"]["cue_packet_readiness"], repo_root),
        "cue_packet_readiness_exists": snapshot["files"]["cue_packet_readiness"].exists(),
        "packet_version": cue.get("packet_version"),
        "phase": cue.get("phase") or readiness.get("phase"),
        "objective": cue.get("objective"),
        "section_count": len(sections) if isinstance(sections, list) else 0,
        "transcript_row_count": len(transcript_rows) if isinstance(transcript_rows, list) else readiness.get("transcript_rows", 0),
        "constraints_count": len(cue.get("constraints", [])) if isinstance(cue.get("constraints"), list) else 0,
        "external_llm_called": readiness.get("external_llm_called", False),
        "ready_for_human_review": readiness.get("ready_for_human_review"),
        "not_ready_for_production": readiness.get("not_ready_for_production", True),
        "remaining_gaps": readiness.get("remaining_gaps", []),
        "state": "draft_offline" if snapshot["files"]["cue_packet"].exists() else "missing",
        "status_note": "cue packet candidate only; not sent to an external LLM and not production accepted",
    }


def _writer_ir_inventory(snapshot: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    writer_ir = _payload(snapshot, "writer_ir")
    utterances = writer_ir.get("utterances", [])
    sections = writer_ir.get("sections", [])
    has_row_ranges = any(
        isinstance(item, dict) and ("row_start" in item or "row_end" in item)
        for item in utterances
    )
    return {
        "schema_version": "writer_ir_inventory.v1",
        "writer_ir_path": _relpath(snapshot["files"]["writer_ir"], repo_root),
        "writer_ir_exists": snapshot["files"]["writer_ir"].exists(),
        "source_schema_version": writer_ir.get("schema_version"),
        "video_id": writer_ir.get("video_id"),
        "compatibility_status": writer_ir.get("compatibility_status"),
        "not_validate_ir_ready_reason": writer_ir.get("not_validate_ir_ready_reason"),
        "section_count": len(sections) if isinstance(sections, list) else 0,
        "utterance_count": len(utterances) if isinstance(utterances, list) else 0,
        "row_ranges_present": has_row_ranges,
        "production_maps_present": False,
        "transcript_status": writer_ir.get("transcript_substitution", {}).get("transcript_status"),
        "timing_status": writer_ir.get("transcript_substitution", {}).get("timing_status"),
        "audio_status": writer_ir.get("transcript_substitution", {}).get("audio_status"),
        "state": "draft_offline" if snapshot["files"]["writer_ir"].exists() else "missing",
        "status_note": "Writer IR candidate only; validate-ir/apply-production prerequisites remain missing",
    }


def _readiness_rows(
    *,
    snapshot: dict[str, Any],
    csv_inventory: dict[str, Any],
    cue_inventory: dict[str, Any],
    writer_ir_inventory: dict[str, Any],
    repo_root: Path,
) -> list[dict[str, Any]]:
    probe = _payload(snapshot, "transcript_probe")
    dashboard_summary = _payload(snapshot, "dashboard_summary")
    boundary = dashboard_summary.get("boundary_status", {})
    real_transcript_found = probe.get("access_reality", {}).get("real_transcript_found_for_current_package") is True
    return [
        _row(
            "draft_yymm4_csv",
            "Draft YMM4 CSV copy",
            "draft_offline" if csv_inventory.get("row_count", 0) > 0 else "missing",
            snapshot["files"]["draft_csv"],
            "copied into the preview package; no YMM4 import has been run",
            repo_root,
            review_ready=csv_inventory.get("row_count", 0) > 0,
        ),
        _row(
            "csv_row_contract",
            "CSV two-column row contract",
            "ready" if csv_inventory.get("column_count_ok") else "partial",
            snapshot["files"]["draft_csv"],
            f"{csv_inventory.get('row_count', 0)} data rows; column_count_ok={csv_inventory.get('column_count_ok')}",
            repo_root,
            review_ready=csv_inventory.get("column_count_ok") is True,
        ),
        _row(
            "csv_header_contract",
            "CSV header contract",
            "partial",
            snapshot["files"]["draft_csv"],
            "YMM4 import CSV is headerless; speaker/text headers are documented but absent by design",
            repo_root,
            review_ready=True,
        ),
        _row(
            "cue_packet",
            "Cue packet candidate",
            cue_inventory.get("state", "unknown"),
            snapshot["files"]["cue_packet"],
            "candidate only; external LLM and production operator steps were not run",
            repo_root,
            review_ready=snapshot["files"]["cue_packet"].exists(),
        ),
        _row(
            "writer_ir",
            "Writer IR candidate",
            writer_ir_inventory.get("state", "unknown"),
            snapshot["files"]["writer_ir"],
            "candidate only; row ranges, timing, maps, and validate/apply remain gated",
            repo_root,
            review_ready=snapshot["files"]["writer_ir"].exists(),
        ),
        _row(
            "transcript_source",
            "Transcript source reality",
            "sample_fixture_not_real" if probe.get("sample_fixture_used") is True else "draft_offline",
            snapshot["files"]["transcript_probe"],
            "sample fixture is not a real NotebookLM/human-reviewed transcript",
            repo_root,
            review_ready=snapshot["files"]["transcript_probe"].exists(),
        ),
        _row(
            "real_transcript_input",
            "Real transcript input",
            "ready" if real_transcript_found else "blocked_by_real_input",
            Path(probe.get("real_input_dropzone") or snapshot["transcript_root"] / "real_input"),
            "supply a verified local transcript before production import review",
            repo_root,
            review_ready=False,
        ),
        _row(
            "dashboard_readiness_ingest",
            "Dashboard readiness ingest",
            "ready" if snapshot["files"]["dashboard_summary"].exists() else "missing",
            snapshot["files"]["dashboard_summary"],
            "read-only status ingest is available to cross-check import state",
            repo_root,
            review_ready=snapshot["files"]["dashboard_summary"].exists(),
        ),
        _row(
            "gui_dashboard_panel",
            "GUI dashboard panel",
            "ready" if snapshot["files"]["gui_adapter"].exists() else "missing",
            snapshot["files"]["gui_adapter"],
            "static read-only panel exists; no GUI runtime or YMM4 launch implied",
            repo_root,
            review_ready=snapshot["files"]["gui_adapter"].exists(),
        ),
        _row(
            "timing_audio_status",
            "Timing and audio status",
            "unknown",
            snapshot["files"]["transcript_probe"],
            f"timing={boundary.get('timing_status', 'unknown')}; audio={boundary.get('audio_status', 'unknown')}",
            repo_root,
            review_ready=False,
        ),
        _row(
            "source_rights_status",
            "Source rights/public use",
            "blocked_by_true_gate",
            snapshot["files"]["transcript_probe"],
            str(boundary.get("rights_status", "sample_only_no_publication")),
            repo_root,
            review_ready=False,
        ),
        _row(
            "production_status",
            "Production status",
            "blocked_by_true_gate",
            snapshot["files"]["transcript_probe"],
            "blocked until real transcript, timing, source review, and human acceptance exist",
            repo_root,
            review_ready=False,
        ),
        _row(
            "public_upload_status",
            "Public upload status",
            "blocked_by_true_gate",
            snapshot["files"]["dashboard_summary"],
            "no YouTube upload, scheduling, visibility, or public-ready claim",
            repo_root,
            review_ready=False,
        ),
        _row(
            "ymm4_gui_import_status",
            "YMM4 GUI import status",
            "deferred",
            snapshot["source_root"] / "manual_yymm4_import",
            "YMM4 was not launched; import is a future manual/verified gate",
            repo_root,
            review_ready=False,
        ),
        _row(
            "ymm4_render_status",
            "YMM4 render status",
            "blocked_by_true_gate",
            snapshot["source_root"] / "render",
            "no render or video output was generated",
            repo_root,
            review_ready=False,
        ),
        _row(
            "production_ymmp",
            "Production .ymmp",
            "missing",
            snapshot["source_root"] / "production.ymmp",
            "not created in this slice; zero-generation remains out of scope",
            repo_root,
            review_ready=False,
        ),
    ]


def _readiness_summary_payload(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    snapshot: dict[str, Any],
    csv_inventory: dict[str, Any],
    cue_inventory: dict[str, Any],
    writer_ir_inventory: dict[str, Any],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    probe = _payload(snapshot, "transcript_probe")
    dashboard_summary = _payload(snapshot, "dashboard_summary")
    gui_adapter = _payload(snapshot, "gui_adapter")
    boundary = dashboard_summary.get("boundary_status", {})
    status_groups = {category: [] for category in STATUS_CATEGORIES}
    for row in rows:
        status_groups[row["state"]].append(row["capability_id"])

    return {
        "schema_version": "ymm4_import_readiness_summary.v1",
        "artifact_id": artifact_id,
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": _first_nonempty(
            gui_adapter.get("selected_candidate_id"),
            dashboard_summary.get("selected_candidate_id"),
            probe.get("selected_candidate_id"),
            writer_ir_inventory.get("video_id"),
        ),
        "status_groups": {key: value for key, value in status_groups.items() if value},
        "readiness_rows": rows,
        "csv_summary": {
            "row_count": csv_inventory.get("row_count"),
            "column_count_ok": csv_inventory.get("column_count_ok"),
            "header_present": csv_inventory.get("header_present"),
            "required_headers": csv_inventory.get("csv_contract", {}).get("required_headers"),
            "missing_headers": csv_inventory.get("csv_contract", {}).get("missing_headers"),
            "missing_headers_block_import": csv_inventory.get("csv_contract", {}).get("missing_headers_block_import"),
        },
        "cue_summary": {
            "section_count": cue_inventory.get("section_count"),
            "transcript_row_count": cue_inventory.get("transcript_row_count"),
            "external_llm_called": cue_inventory.get("external_llm_called"),
            "state": cue_inventory.get("state"),
        },
        "writer_ir_summary": {
            "section_count": writer_ir_inventory.get("section_count"),
            "utterance_count": writer_ir_inventory.get("utterance_count"),
            "compatibility_status": writer_ir_inventory.get("compatibility_status"),
            "row_ranges_present": writer_ir_inventory.get("row_ranges_present"),
            "state": writer_ir_inventory.get("state"),
        },
        "input_reality": {
            "sample_fixture_used": probe.get("sample_fixture_used"),
            "real_transcript_found_for_current_package": probe.get("access_reality", {}).get(
                "real_transcript_found_for_current_package"
            ),
            "selected_transcript_path": probe.get("selected_transcript_path"),
            "source_mode": probe.get("source_mode"),
        },
        "boundary_status": {
            "source_status": boundary.get("source_status", "unknown"),
            "transcript_status": probe.get("transcript_status", boundary.get("transcript_status", "unknown")),
            "timing_status": probe.get("timing_status", boundary.get("timing_status", "unknown")),
            "audio_status": probe.get("audio_status", boundary.get("audio_status", "unknown")),
            "rights_status": boundary.get("rights_status", "sample_only_no_publication"),
            "production_status": "blocked_by_true_gate",
            "public_upload_status": "blocked_by_true_gate",
            "ymm4_gui_status": "blocked_by_true_gate",
            "ymm4_import_status": "deferred",
            "ymm4_render_status": "blocked_by_true_gate",
        },
        "closed_gates": [
            "YouTube upload/publication/visibility change",
            "OAuth/API keys/payment",
            "rights/legal/public-ready acceptance",
            "live scraping/media download",
            "YMM4 GUI launch/import/render",
            "production .ymmp generation",
            "cross-repo or destructive git",
        ],
        "next_safe_local_action": (
            "Open import_preview_panel.md or import_preview_panel.html for offline review; "
            "then provide a verified real transcript via transcript_substitution_readiness/real_input/ "
            "or rerun build-transcript-substitution with --transcript before any actual YMM4 import."
        ),
    }


def _manifest_payload(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    snapshot: dict[str, Any],
    readiness_summary: dict[str, Any],
    csv_inventory: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "ymm4_import_preview_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "ymm4-import-preview-pack",
        "status": "generated",
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": readiness_summary.get("selected_candidate_id"),
        "files": {name: str(output_root / name) for name in REQUIRED_IMPORT_PREVIEW_FILES},
        "source_inputs": {
            key: str(path)
            for key, path in snapshot["files"].items()
        },
        "preview_csv": {
            "source_csv_path": csv_inventory.get("source_csv_path"),
            "copied_csv_path": csv_inventory.get("copied_csv_path"),
            "row_count": csv_inventory.get("row_count"),
            "state": "draft_offline",
        },
        "boundaries": {
            "local_offline_review_only": True,
            "sample_fixture_not_real_visible": readiness_summary["boundary_status"].get("transcript_status")
            == "sample_fixture_not_real",
            "draft_offline_only": True,
            "no_live_fetch": True,
            "no_media_download": True,
            "no_youtube_publication": True,
            "no_oauth_or_paid_api": True,
            "no_rights_or_legal_acceptance": True,
            "no_yymm4_gui_launch_or_import_or_render": True,
            "no_production_ymmp_generation": True,
            "no_audio_generation": True,
        },
    }


def _source_artifact_index(snapshot: dict[str, Any], output_root: Path, repo_root: Path) -> dict[str, Any]:
    source_inputs = []
    for key, path in snapshot["files"].items():
        payload = _payload(snapshot, key)
        source_inputs.append({
            "id": key,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": "ready" if path.exists() else "missing",
            "schema_version": payload.get("schema_version"),
        })
    generated_outputs = []
    for name in REQUIRED_IMPORT_PREVIEW_FILES:
        path = output_root / name
        generated_outputs.append({
            "id": name,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": "ready" if path.exists() else "missing",
        })
    return {
        "schema_version": "ymm4_import_preview_source_artifact_index.v1",
        "source_inputs": source_inputs,
        "generated_outputs": generated_outputs,
        "artifact_counts": {
            "source_total": len(source_inputs),
            "source_present": sum(1 for item in source_inputs if item["exists"]),
            "generated_total": len(generated_outputs),
            "generated_present": sum(1 for item in generated_outputs if item["exists"]),
        },
    }


def _render_markdown_panel(panel_data: dict[str, Any]) -> str:
    csv_inventory = panel_data["csv_inventory"]
    lines = [
        "# YMM4 Import Preview Pack",
        "",
        f"- artifact_id: {panel_data['artifact_id']}",
        f"- selected_candidate_id: {panel_data.get('selected_candidate_id')}",
        f"- transcript_status: {panel_data['boundary_status'].get('transcript_status')}",
        f"- csv_rows: {csv_inventory.get('row_count')}",
        f"- copied_csv: `{csv_inventory.get('copied_csv_path')}`",
        "",
        "## Status Palette",
        "",
        ", ".join(panel_data["status_categories"]),
        "",
        "## Readiness Grid",
        "",
        "| capability | state | review_ready | path | note |",
        "|---|---|---:|---|---|",
    ]
    for row in panel_data["readiness_rows"]:
        lines.append(
            f"| {row['capability_id']} | {row['state']} | {str(row['review_ready']).lower()} | "
            f"`{row['repo_relative_path']}` | {row['note']} |"
        )
    lines.extend([
        "",
        "## CSV Contract",
        "",
        f"- header_mode: {csv_inventory['csv_contract']['header_mode']}",
        f"- required_headers: {', '.join(csv_inventory['csv_contract']['required_headers'])}",
        f"- missing_headers: {', '.join(csv_inventory['csv_contract']['missing_headers'])}",
        f"- missing_headers_block_import: {str(csv_inventory['csv_contract']['missing_headers_block_import']).lower()}",
        f"- column_count_ok: {str(csv_inventory['column_count_ok']).lower()}",
        "",
        "## Boundary Status",
        "",
        "| boundary | status |",
        "|---|---|",
    ])
    for key, value in panel_data["boundary_status"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend([
        "",
        "## Next Safe Local Action",
        "",
        panel_data["next_action"],
        "",
    ])
    return "\n".join(lines)


def _render_html_panel(panel_data: dict[str, Any]) -> str:
    title = "YMM4 Import Preview Pack"
    rows = panel_data["readiness_rows"]
    boundary = panel_data["boundary_status"]
    csv_inventory = panel_data["csv_inventory"]
    cards = "\n".join(_status_card(row) for row in rows)
    boundary_rows = "\n".join(
        f"<tr><th>{_esc(key)}</th><td><span class=\"status-pill\" data-status=\"{_esc(_boundary_state(value))}\">{_esc(value)}</span></td></tr>"
        for key, value in boundary.items()
    )
    palette = "\n".join(
        f"<span class=\"status-pill\" data-status=\"{_esc(state)}\">{_esc(state)}</span>"
        for state in STATUS_CATEGORIES
    )
    source_index_label = "source_artifact_index"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #f7f7f4;
      --surface: #ffffff;
      --ink: #16202a;
      --muted: #667085;
      --line: #d7ded8;
      --ready: #0f766e;
      --draft: #8a6116;
      --sample: #a14f16;
      --input: #b42318;
      --gate: #7f1d1d;
      --deferred: #475569;
      --missing: #6b7280;
      --unknown: #4b5563;
      --accent: #2563eb;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; min-height: 100%; background: var(--bg); color: var(--ink); font-family: "Segoe UI", "Noto Sans", Arial, sans-serif; }}
    body {{ padding: 24px; }}
    .shell {{ max-width: 1320px; margin: 0 auto; }}
    header {{ display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 16px; align-items: end; margin-bottom: 18px; }}
    h1 {{ margin: 0; font-size: 28px; line-height: 1.15; letter-spacing: 0; }}
    h2 {{ margin: 0 0 12px; font-size: 16px; line-height: 1.25; letter-spacing: 0; }}
    p {{ margin: 0; color: var(--muted); line-height: 1.5; }}
    code {{ font-family: Consolas, "SFMono-Regular", monospace; font-size: 12px; overflow-wrap: anywhere; }}
    .topline {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }}
    .summary-strip {{ display: grid; grid-template-columns: repeat(4, minmax(140px, 1fr)); gap: 10px; margin-bottom: 18px; }}
    .metric, .panel, .card {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; }}
    .metric {{ padding: 14px; min-height: 78px; }}
    .metric b {{ display: block; font-size: 20px; margin-top: 6px; }}
    .layout {{ display: grid; grid-template-columns: minmax(0, 1.45fr) minmax(320px, 0.85fr); gap: 16px; }}
    .panel {{ padding: 16px; margin-bottom: 16px; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }}
    .card {{ padding: 12px; display: grid; gap: 8px; min-height: 135px; }}
    .card-head {{ display: flex; justify-content: space-between; gap: 8px; align-items: flex-start; }}
    .card-title {{ font-size: 14px; font-weight: 700; line-height: 1.25; }}
    .note {{ font-size: 12px; color: var(--muted); line-height: 1.4; }}
    .status-pill {{ display: inline-flex; align-items: center; min-height: 24px; padding: 3px 8px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid currentColor; background: #fff; }}
    [data-status="ready"] {{ color: var(--ready); }}
    [data-status="draft_offline"] {{ color: var(--draft); }}
    [data-status="sample_fixture_not_real"] {{ color: var(--sample); }}
    [data-status="blocked_by_real_input"] {{ color: var(--input); }}
    [data-status="blocked_by_true_gate"] {{ color: var(--gate); }}
    [data-status="deferred"] {{ color: var(--deferred); }}
    [data-status="missing"] {{ color: var(--missing); }}
    [data-status="partial"], [data-status="unknown"] {{ color: var(--unknown); }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ text-align: left; padding: 9px 8px; border-top: 1px solid var(--line); vertical-align: top; }}
    th {{ width: 200px; color: var(--muted); font-weight: 700; }}
    .next {{ border-left: 4px solid var(--accent); padding-left: 12px; }}
    @media (max-width: 980px) {{
      body {{ padding: 14px; }}
      header, .layout {{ grid-template-columns: 1fr; }}
      .summary-strip, .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 640px) {{
      .summary-strip, .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="shell" data-import-preview-pack="true">
    <header>
      <div>
        <h1>{title}</h1>
        <p>Local/offline handoff preview for { _esc(panel_data.get("selected_candidate_id", "unknown")) }.</p>
        <div class="topline">{palette}</div>
      </div>
      <span class="status-pill" data-status="sample_fixture_not_real">{_esc(boundary.get("transcript_status", "unknown"))}</span>
    </header>

    <section class="summary-strip" aria-label="import preview summary">
      <div class="metric"><p>CSV rows</p><b>{_esc(csv_inventory.get("row_count", 0))}</b></div>
      <div class="metric"><p>CSV columns</p><b>{_esc(str(csv_inventory.get("column_count_ok")).lower())}</b></div>
      <div class="metric"><p>Transcript</p><b>{_esc(boundary.get("transcript_status", "unknown"))}</b></div>
      <div class="metric"><p>YMM4 GUI</p><b>{_esc(boundary.get("ymm4_gui_status", "unknown"))}</b></div>
    </section>

    <section class="layout">
      <div>
        <section class="panel" data-section="readiness-grid">
          <h2>Readiness Grid</h2>
          <div class="grid">{cards}</div>
        </section>

        <section class="panel" data-section="source-artifact-index">
          <h2>Source Artifact Index</h2>
          <p>{source_index_label}: see <code>source_artifact_index.json</code> for source inputs and generated files.</p>
        </section>
      </div>

      <aside>
        <section class="panel" data-section="csv-contract">
          <h2>CSV Contract</h2>
          <table aria-label="csv contract">
            <tbody>
              <tr><th>source_csv</th><td><code>{_esc(csv_inventory.get("source_csv_path", ""))}</code></td></tr>
              <tr><th>copied_csv</th><td><code>{_esc(csv_inventory.get("copied_csv_path", ""))}</code></td></tr>
              <tr><th>header_mode</th><td>{_esc(csv_inventory["csv_contract"]["header_mode"])}</td></tr>
              <tr><th>required_headers</th><td>{_esc(", ".join(csv_inventory["csv_contract"]["required_headers"]))}</td></tr>
              <tr><th>missing_headers</th><td>{_esc(", ".join(csv_inventory["csv_contract"]["missing_headers"]))}</td></tr>
              <tr><th>missing_headers_block_import</th><td>{_esc(str(csv_inventory["csv_contract"]["missing_headers_block_import"]).lower())}</td></tr>
            </tbody>
          </table>
        </section>

        <section class="panel" data-section="boundary-status">
          <h2>Boundaries</h2>
          <table aria-label="boundary status"><tbody>{boundary_rows}</tbody></table>
        </section>

        <section class="panel next" data-section="next-action">
          <h2>Next Safe Local Action</h2>
          <p>{_esc(panel_data.get("next_action", ""))}</p>
        </section>
      </aside>
    </section>
  </main>
</body>
</html>
"""


def _status_card(row: dict[str, Any]) -> str:
    state = str(row.get("state", "unknown"))
    return (
        f'<article class="card" data-capability="{_esc(row.get("capability_id", "unknown"))}" data-status="{_esc(state)}">'
        '<div class="card-head">'
        f'<div class="card-title">{_esc(row.get("label", row.get("capability_id", "unknown")))}</div>'
        f'<span class="status-pill" data-status="{_esc(state)}">{_esc(state)}</span>'
        "</div>"
        f'<div class="note">{_esc(row.get("note", ""))}</div>'
        f'<code>{_esc(row.get("repo_relative_path", ""))}</code>'
        "</article>"
    )


def _render_checklist(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    reviewable = [row for row in rows if row.get("review_ready") is True]
    lines = [
        "# YMM4 Import Preview Checklist",
        "",
        "## Check Now",
        "",
        "- Confirm the copied CSV is the intended draft import handoff file.",
        "- Confirm `sample_fixture_not_real` is visible before any real transcript rerun.",
        "- Confirm headerless CSV state is understood: headers are documented, not present in the import CSV.",
        "- Confirm cue packet and Writer IR are candidates only.",
        "- Confirm YMM4 GUI, import, render, production `.ymmp`, rights, public upload, OAuth, and payment gates remain closed.",
        "",
        "## Reviewable Artifacts",
        "",
    ]
    for row in reviewable:
        lines.append(f"- {row['capability_id']}: `{row['repo_relative_path']}`")
    lines.extend([
        "",
        "## Next Move",
        "",
        summary["next_safe_local_action"],
        "",
    ])
    return "\n".join(lines)


def _render_limitations(summary: dict[str, Any]) -> str:
    lines = [
        "# YMM4 Import Preview Limitations",
        "",
        "This is a local/offline import preview package. It aggregates current draft artifacts for review only.",
        "",
        "Not performed:",
        "",
    ]
    for gate in summary.get("closed_gates", []):
        lines.append(f"- {gate}")
    lines.extend([
        "- real transcript rerun",
        "- YMM4 VoiceItem timing readback",
        "- source, rights, legal, public-ready, or production acceptance",
        "",
        f"Current transcript_status: `{summary['boundary_status'].get('transcript_status')}`",
        "",
    ])
    return "\n".join(lines)


def _row(
    capability_id: str,
    label: str,
    state: str,
    path: Path,
    note: str,
    repo_root: Path,
    *,
    review_ready: bool,
) -> dict[str, Any]:
    return {
        "capability_id": capability_id,
        "label": label,
        "state": state if state in STATUS_CATEGORIES else "unknown",
        "review_ready": review_ready,
        "repo_relative_path": _relpath(path, repo_root),
        "exists": path.exists(),
        "note": note,
    }


def _read_csv_rows(path: Path) -> list[list[str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [row for row in csv.reader(handle)]


def _payload(snapshot: dict[str, Any], key: str) -> dict[str, Any]:
    payload = snapshot.get("payloads", {}).get(key)
    return payload if isinstance(payload, dict) else {}


def _load_json_if_present(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _find_repo_root(path: Path) -> Path:
    resolved = path.resolve()
    for candidate in (resolved, *resolved.parents):
        if (candidate / "pyproject.toml").exists() or (candidate / "AGENTS.md").exists():
            return candidate
    return Path.cwd()


def _relpath(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def _first_nonempty(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", []):
            return value
    return None


def _boundary_state(value: Any) -> str:
    text = str(value)
    if text in STATUS_CATEGORIES:
        return text
    if "blocked" in text:
        return "blocked_by_true_gate"
    if "sample" in text:
        return "sample_fixture_not_real"
    if "draft" in text or "offline" in text:
        return "draft_offline"
    if "deferred" in text:
        return "deferred"
    if "missing" in text:
        return "missing"
    if "unknown" in text:
        return "unknown"
    return "ready"


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
