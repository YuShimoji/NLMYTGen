"""Local/offline YMM4 import preview pack for episode packages."""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

from src.pipeline.dashboard_readiness_ingest import STATUS_CATEGORIES

DEFAULT_OUTPUT_DIRNAME = "ymm4_import_preview_pack"
DEFAULT_ARTIFACT_ID = "episode_002_yymm4_import_preview_pack_v1"
VALIDATION_LEDGER_PATH = Path("samples/_probe/newsroom_handoff/validation_drift_velocity_recovery_v1.json")

IMPORT_PREVIEW_STATUS_CATEGORIES = tuple(
    dict.fromkeys((*STATUS_CATEGORIES, "dry_run", "validation_noise_nonblocking"))
)

REQUIRED_IMPORT_PREVIEW_FILES = (
    "import_preview_manifest.json",
    "yymm4_csv_inventory.json",
    "cue_packet_inventory.json",
    "writer_ir_inventory.json",
    "import_readiness_summary.json",
    "import_preview_checklist.md",
    "import_preview_panel.md",
    "source_artifact_index.json",
    "draft_yymm4_preview.csv",
    "limitations.md",
    "validation_readback.json",
)

REQUIRED_BOUNDARY_FLAGS = (
    "dry_run",
    "sample_fixture_not_real",
    "no_real_transcript",
    "rights_boundary",
    "public_upload_closed",
    "yymm4_render_closed",
    "no_yymm4_import",
    "not_imported_to_yymm4",
    "no_production_ymmp",
)

FORBIDDEN_TRUE_CLAIMS = (
    '"youtube_uploaded": true',
    '"production_ready": true',
    '"render_completion": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"actual_yymm4_import": true',
    '"yymm4_rendered": true',
)


def build_yymm4_import_preview_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a read-only import preview package without launching YMM4."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)
    paths = _input_paths(source_root)

    dashboard_summary = _load_json(paths["dashboard_summary"])
    dashboard_readback = _load_json(paths["dashboard_readback"])
    gui_panel_data = _load_json(paths["gui_panel_data"])
    gui_readback = _load_json(paths["gui_readback"])
    substitution_manifest = _load_json(paths["substitution_manifest"])
    substitution_readback = _load_json(paths["substitution_readback"])
    bridge_manifest = _load_json(paths["bridge_manifest"])
    bridge_readback = _load_json(paths["bridge_readback"])
    cue_packet = _load_json(paths["cue_packet"])
    cue_readiness = _load_json(paths["cue_readiness"])
    writer_ir = _load_json(paths["writer_ir"])
    validation_noise = _validation_noise_payload(repo_root, gui_panel_data)
    thumbnail_context = _thumbnail_proof_context(paths, repo_root)

    csv_inventory = _csv_inventory(
        csv_path=paths["draft_csv"],
        copied_csv_path=output_root / "draft_yymm4_preview.csv",
        bridge_csv_path=paths["bridge_csv"],
        repo_root=repo_root,
    )
    cue_inventory = _cue_packet_inventory(
        cue_packet=cue_packet,
        cue_readiness=cue_readiness,
        cue_path=paths["cue_packet"],
        repo_root=repo_root,
    )
    writer_inventory = _writer_ir_inventory(
        writer_ir=writer_ir,
        writer_path=paths["writer_ir"],
        repo_root=repo_root,
    )
    summary = _import_readiness_summary(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        dashboard_summary=dashboard_summary,
        gui_panel_data=gui_panel_data,
        substitution_manifest=substitution_manifest,
        bridge_manifest=bridge_manifest,
        csv_inventory=csv_inventory,
        cue_inventory=cue_inventory,
        writer_inventory=writer_inventory,
        validation_noise=validation_noise,
        thumbnail_context=thumbnail_context,
    )
    source_index = _source_artifact_index(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        validation_noise=validation_noise,
    )
    manifest = _manifest_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        summary=summary,
        source_index=source_index,
    )

    _write_json(output_root / "import_preview_manifest.json", manifest)
    _write_json(output_root / "yymm4_csv_inventory.json", csv_inventory)
    _write_json(output_root / "cue_packet_inventory.json", cue_inventory)
    _write_json(output_root / "writer_ir_inventory.json", writer_inventory)
    _write_json(output_root / "import_readiness_summary.json", summary)
    _write_text(output_root / "import_preview_checklist.md", _render_checklist(summary, csv_inventory))
    _write_text(output_root / "import_preview_panel.md", _render_panel(summary, csv_inventory, cue_inventory, writer_inventory))
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_text(output_root / "limitations.md", _render_limitations(summary))

    readback = validate_yymm4_import_preview_pack(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_yymm4_import_preview_pack(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    final_source_index = _source_artifact_index(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        validation_noise=validation_noise,
    )
    _write_json(output_root / "source_artifact_index.json", final_source_index)
    final_readback = validate_yymm4_import_preview_pack(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_yymm4_import_preview_pack(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate a generated local/offline YMM4 import preview pack."""
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
    payloads = {
        "import_preview_manifest": manifest,
        "yymm4_csv_inventory": csv_inventory,
        "cue_packet_inventory": cue_inventory,
        "writer_ir_inventory": writer_inventory,
        "import_readiness_summary": summary,
        "source_artifact_index": source_index,
    }
    for name, payload in payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            payloads[name] = {}

    manifest = payloads["import_preview_manifest"]
    csv_inventory = payloads["yymm4_csv_inventory"]
    cue_inventory = payloads["cue_packet_inventory"]
    writer_inventory = payloads["writer_ir_inventory"]
    summary = payloads["import_readiness_summary"]
    source_index = payloads["source_artifact_index"]

    if manifest.get("artifact_kind") != "yymm4-import-preview-pack":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if csv_inventory.get("row_count", 0) <= 0:
        failed_checks.append("csv_row_count_empty")
    if csv_inventory.get("header_mode") not in {"headerless", "headered"}:
        failed_checks.append("csv_header_mode_unknown")
    if csv_inventory.get("missing_required_fields"):
        failed_checks.append("csv_required_fields_missing")
    if csv_inventory.get("not_imported_to_yymm4") is not True:
        failed_checks.append("csv_import_flag_not_closed")
    if cue_inventory.get("transcript_rows", 0) <= 0:
        failed_checks.append("cue_transcript_rows_empty")
    if writer_inventory.get("utterance_count", 0) <= 0:
        failed_checks.append("writer_ir_utterances_empty")

    boundary_flags = summary.get("boundary_flags", {})
    missing_boundary_flags = [flag for flag in REQUIRED_BOUNDARY_FLAGS if boundary_flags.get(flag) is not True]
    failed_checks.extend(f"missing_boundary_flag:{flag}" for flag in missing_boundary_flags)
    boundary_status = summary.get("boundary_status", {})
    if boundary_status.get("transcript_status") != "sample_fixture_not_real":
        failed_checks.append("sample_fixture_status_not_visible")
    if boundary_status.get("real_transcript_status") != "blocked_by_real_input":
        failed_checks.append("real_transcript_gate_not_visible")
    if boundary_status.get("public_upload_status") != "blocked_by_true_gate":
        failed_checks.append("public_upload_gate_not_closed")
    if boundary_status.get("yymm4_import_status") != "blocked_by_true_gate":
        failed_checks.append("yymm4_import_gate_not_closed")
    if boundary_status.get("yymm4_render_status") != "blocked_by_true_gate":
        failed_checks.append("yymm4_render_gate_not_closed")
    if summary.get("validation_noise", {}).get("status") != "validation_noise_nonblocking":
        failed_checks.append("validation_noise_not_nonblocking")
    if summary.get("validation_noise", {}).get("blocking_for_this_slice") is not False:
        failed_checks.append("validation_noise_blocking_flag_not_false")
    thumbnail_context = summary.get("thumbnail_proof_context", {})
    if thumbnail_context.get("status") != "ready":
        failed_checks.append("thumbnail_context_not_ready")
    if thumbnail_context.get("contextual_only") is not True:
        failed_checks.append("thumbnail_context_not_contextual_only")
    if thumbnail_context.get("current_implementation_target") is not False:
        failed_checks.append("thumbnail_context_current_target_not_false")

    panel_text = files["import_preview_panel.md"].read_text(encoding="utf-8") if files["import_preview_panel.md"].exists() else ""
    missing_status_text = [state for state in IMPORT_PREVIEW_STATUS_CATEGORIES if state not in panel_text]
    failed_checks.extend(f"panel_status_missing:{state}" for state in missing_status_text)
    if "source_artifact_index.json" not in panel_text:
        failed_checks.append("panel_source_artifact_index_missing")
    if "not_imported_to_yymm4" not in panel_text:
        failed_checks.append("panel_yymm4_not_imported_missing")
    if "draft_yymm4_preview.csv" not in panel_text:
        failed_checks.append("panel_preview_csv_missing")
    if "thumbnail_visual_proof" not in panel_text or "contextual_only" not in panel_text:
        failed_checks.append("panel_thumbnail_context_missing")

    source_artifacts = source_index.get("source_artifacts", [])
    output_artifacts = source_index.get("output_artifacts", [])
    if not isinstance(source_artifacts, list) or len(source_artifacts) < 8:
        failed_checks.append("source_artifact_index_too_small")
    if not isinstance(output_artifacts, list) or len(output_artifacts) < len(REQUIRED_IMPORT_PREVIEW_FILES):
        failed_checks.append("output_artifact_index_too_small")

    forbidden_hits = _forbidden_true_claims(root)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)

    return {
        "schema_version": "yymm4_import_preview_pack_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in payloads.values()),
            "csv_inventory_valid": csv_inventory.get("row_count", 0) > 0 and not csv_inventory.get("missing_required_fields"),
            "csv_header_mode_recorded": csv_inventory.get("header_mode") in {"headerless", "headered"},
            "cue_packet_inventory_valid": cue_inventory.get("transcript_rows", 0) > 0,
            "writer_ir_inventory_valid": writer_inventory.get("utterance_count", 0) > 0,
            "boundary_flags_present": not missing_boundary_flags,
            "status_categories_visible": not missing_status_text,
            "source_artifact_index_visible": "source_artifact_index.json" in panel_text,
            "not_imported_to_yymm4": summary.get("boundary_flags", {}).get("not_imported_to_yymm4") is True,
            "validation_noise_nonblocking": summary.get("validation_noise", {}).get("status") == "validation_noise_nonblocking",
            "thumbnail_context_ready": thumbnail_context.get("status") == "ready",
            "thumbnail_context_only": thumbnail_context.get("contextual_only") is True,
            "forbidden_true_claims_absent": not forbidden_hits,
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "selected_candidate_id": summary.get("selected_candidate_id"),
        "csv_row_count": csv_inventory.get("row_count"),
        "csv_header_mode": csv_inventory.get("header_mode"),
        "transcript_status": boundary_status.get("transcript_status"),
        "yymm4_import_status": boundary_status.get("yymm4_import_status"),
        "validation_noise_status": summary.get("validation_noise", {}).get("status"),
        "thumbnail_context_status": thumbnail_context.get("status"),
        "thumbnail_recommended_variant_id": thumbnail_context.get("recommended_variant_id"),
        "thumbnail_context_primary_human_review": thumbnail_context.get("primary_human_review"),
        "primary_machine_readable": str(root / "import_readiness_summary.json"),
        "primary_human_review": str(root / "import_preview_panel.md"),
        "preview_csv": str(root / "draft_yymm4_preview.csv"),
        "next_action": summary.get("next_safe_local_action"),
    }


def _input_paths(source_root: Path) -> dict[str, Path]:
    transcript_dir = source_root / "transcript_substitution_readiness"
    bridge_dir = source_root / "ir_bridge"
    dashboard_dir = source_root / "dashboard_readiness_ingest"
    gui_dir = source_root / "gui_dashboard_panel"
    thumbnail_dir = source_root / "thumbnail_visual_proof_pack"
    return {
        "draft_csv": transcript_dir / "regenerated_draft_yymm4.csv",
        "bridge_csv": bridge_dir / "draft_yymm4.csv",
        "cue_packet": transcript_dir / "regenerated_cue_packet_candidate.json",
        "cue_readiness": transcript_dir / "cue_packet_readiness.json",
        "writer_ir": transcript_dir / "regenerated_writer_ir_candidate.json",
        "substitution_manifest": transcript_dir / "substitution_manifest.json",
        "substitution_readback": transcript_dir / "validation_readback.json",
        "bridge_manifest": bridge_dir / "bridge_manifest.json",
        "bridge_readback": bridge_dir / "validation_readback.json",
        "dashboard_summary": dashboard_dir / "readiness_summary.json",
        "dashboard_readback": dashboard_dir / "validation_readback.json",
        "gui_panel_data": gui_dir / "panel_data.json",
        "gui_readback": gui_dir / "validation_readback.json",
        "gui_source_index": gui_dir / "source_artifact_index.json",
        "dashboard_source_index": dashboard_dir / "source_artifact_index.json",
        "transcript_source_index": transcript_dir / "source_artifact_index.json",
        "bridge_source_index": bridge_dir / "source_artifact_index.json",
        "thumbnail_readback": thumbnail_dir / "readback.json",
        "thumbnail_variants": thumbnail_dir / "thumbnail_variants.json",
        "thumbnail_html": thumbnail_dir / "thumbnail_visual_proof.html",
        "thumbnail_contact_sheet": thumbnail_dir / "thumbnail_contact_sheet.svg",
        "thumbnail_source_index": thumbnail_dir / "source_index.json",
    }


def _thumbnail_proof_context(paths: dict[str, Path], repo_root: Path) -> dict[str, Any]:
    readback = _load_json_if_present(paths["thumbnail_readback"])
    variants_payload = _load_json_if_present(paths["thumbnail_variants"])
    exists = isinstance(readback, dict) and isinstance(variants_payload, dict)
    status = "ready" if exists and readback.get("status") == "passed" else "missing"
    variants = variants_payload.get("variants", []) if isinstance(variants_payload, dict) else []
    return {
        "schema_version": "thumbnail_proof_context.v1",
        "status": status,
        "contextual_only": True,
        "current_implementation_target": False,
        "not_revised_in_this_slice": True,
        "artifact_id": variants_payload.get("artifact_id") if isinstance(variants_payload, dict) else None,
        "variant_count": variants_payload.get("variant_count") if isinstance(variants_payload, dict) else 0,
        "recommended_variant_id": variants_payload.get("recommended_variant_id") if isinstance(variants_payload, dict) else None,
        "variant_ids": [
            variant.get("variant_id")
            for variant in variants
            if isinstance(variant, dict) and variant.get("variant_id")
        ],
        "primary_machine_readable": _relpath(paths["thumbnail_variants"], repo_root),
        "primary_human_review": _relpath(paths["thumbnail_html"], repo_root),
        "contact_sheet": _relpath(paths["thumbnail_contact_sheet"], repo_root),
        "readback_path": _relpath(paths["thumbnail_readback"], repo_root),
        "source_index_path": _relpath(paths["thumbnail_source_index"], repo_root),
        "exists": {
            "readback": paths["thumbnail_readback"].exists(),
            "variants": paths["thumbnail_variants"].exists(),
            "html": paths["thumbnail_html"].exists(),
            "contact_sheet": paths["thumbnail_contact_sheet"].exists(),
            "source_index": paths["thumbnail_source_index"].exists(),
        },
        "proof_boundaries": {
            "proof_only": True,
            "not_production_thumbnail": True,
            "no_external_media_download": True,
            "no_public_ready_acceptance": True,
        },
    }


def _csv_inventory(*, csv_path: Path, copied_csv_path: Path, bridge_csv_path: Path, repo_root: Path) -> dict[str, Any]:
    text = csv_path.read_text(encoding="utf-8-sig")
    copied_csv_path.write_text(text, encoding="utf-8", newline="")
    rows = _csv_rows(text)
    non_empty_rows = [row for row in rows if any(cell.strip() for cell in row)]
    header_mode = _header_mode(non_empty_rows)
    data_rows = non_empty_rows[1:] if header_mode == "headered" else non_empty_rows
    max_columns = max((len(row) for row in non_empty_rows), default=0)
    missing_fields: list[str] = []
    if header_mode == "headered":
        headers = [cell.strip().lower() for cell in non_empty_rows[0]]
        for field in ("speaker", "text"):
            if field not in headers:
                missing_fields.append(field)
    elif max_columns < 2:
        missing_fields.extend(["speaker", "text"])
    malformed_row_numbers = [
        index + (2 if header_mode == "headered" else 1)
        for index, row in enumerate(data_rows)
        if len(row) < 2
    ]
    speakers = sorted({row[0] for row in data_rows if len(row) >= 1 and row[0]})
    bridge_text = bridge_csv_path.read_text(encoding="utf-8-sig") if bridge_csv_path.exists() else ""
    return {
        "schema_version": "yymm4_csv_inventory.v1",
        "source_csv_path": _relpath(csv_path, repo_root),
        "bridge_csv_path": _relpath(bridge_csv_path, repo_root),
        "copied_preview_csv_path": _relpath(copied_csv_path, repo_root),
        "selected_source": "transcript_substitution_readiness.regenerated_draft_yymm4.csv",
        "row_count": len(data_rows),
        "raw_row_count": len(non_empty_rows),
        "header_mode": header_mode,
        "detected_column_count": max_columns,
        "required_fields": ["speaker", "text"],
        "inferred_fields": ["speaker", "text"] if header_mode == "headerless" and max_columns >= 2 else [],
        "missing_required_fields": missing_fields,
        "malformed_row_numbers": malformed_row_numbers,
        "speaker_count": len(speakers),
        "speakers": speakers,
        "bridge_csv_matches_selected": bridge_text == text,
        "dry_run": True,
        "sample_fixture_not_real": True,
        "not_imported_to_yymm4": True,
        "draft_csv_status": "draft_preview_only_no_yymm4_import",
    }


def _cue_packet_inventory(
    *,
    cue_packet: dict[str, Any],
    cue_readiness: dict[str, Any],
    cue_path: Path,
    repo_root: Path,
) -> dict[str, Any]:
    sections = cue_packet.get("context", {}).get("sections", [])
    transcript = cue_packet.get("transcript", [])
    constraints = cue_packet.get("constraints", [])
    return {
        "schema_version": "cue_packet_inventory.v1",
        "source_path": _relpath(cue_path, repo_root),
        "packet_version": cue_packet.get("packet_version"),
        "phase": cue_packet.get("phase"),
        "status": cue_readiness.get("status", "draft_offline"),
        "section_count": len(sections) if isinstance(sections, list) else 0,
        "transcript_rows": len(transcript) if isinstance(transcript, list) else 0,
        "constraints_count": len(constraints) if isinstance(constraints, list) else 0,
        "ready_for_human_review": cue_readiness.get("ready_for_human_review") is True,
        "not_ready_for_production": cue_readiness.get("not_ready_for_production") is True,
        "remaining_gaps": cue_readiness.get("remaining_gaps", []),
        "cue_or_beat_availability": "ready_for_local_review" if transcript else "missing",
        "not_sent_to_external_llm": cue_readiness.get("external_llm_called") is False,
    }


def _writer_ir_inventory(*, writer_ir: dict[str, Any], writer_path: Path, repo_root: Path) -> dict[str, Any]:
    sections = writer_ir.get("sections", [])
    utterances = writer_ir.get("utterances", [])
    compatibility_status = writer_ir.get("compatibility_status", "unknown")
    return {
        "schema_version": "writer_ir_inventory.v1",
        "source_path": _relpath(writer_path, repo_root),
        "source_schema_version": writer_ir.get("schema_version"),
        "video_id": writer_ir.get("video_id"),
        "compatibility_status": compatibility_status,
        "validate_ir_ready": compatibility_status == "validate_ir_ready",
        "not_validate_ir_ready_reason": writer_ir.get("not_validate_ir_ready_reason"),
        "section_count": len(sections) if isinstance(sections, list) else 0,
        "utterance_count": len(utterances) if isinstance(utterances, list) else 0,
        "visual_arc_count": len(writer_ir.get("visual_arc", [])) if isinstance(writer_ir.get("visual_arc"), list) else 0,
        "writer_ir_availability": "draft_offline" if utterances else "missing",
        "boundary_status": writer_ir.get("boundary_status", {}),
        "production_boundary": writer_ir.get("production_boundary", {}),
    }


def _import_readiness_summary(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    dashboard_summary: dict[str, Any],
    gui_panel_data: dict[str, Any],
    substitution_manifest: dict[str, Any],
    bridge_manifest: dict[str, Any],
    csv_inventory: dict[str, Any],
    cue_inventory: dict[str, Any],
    writer_inventory: dict[str, Any],
    validation_noise: dict[str, Any],
    thumbnail_context: dict[str, Any],
) -> dict[str, Any]:
    dashboard_flags = dashboard_summary.get("boundary_flags", {})
    boundary_flags = {
        "dry_run": True,
        "sample_fixture_not_real": True,
        "no_real_transcript": True,
        "rights_boundary": True,
        "public_upload_closed": True,
        "yymm4_render_closed": True,
        "no_yymm4_import": True,
        "not_imported_to_yymm4": True,
        "no_yymm4_gui_launch": True,
        "no_yymm4_render": True,
        "no_production_ymmp": True,
        "no_external_media_download": True,
        "no_production_thumbnail_acceptance": True,
        "thumbnail_context_only": thumbnail_context.get("contextual_only") is True,
        "validation_noise_nonblocking": validation_noise.get("status") == "validation_noise_nonblocking",
        "dashboard_flags_confirmed": all(dashboard_flags.get(flag) is True for flag in dashboard_flags),
    }
    boundary_status = {
        "source_status": dashboard_summary.get("boundary_status", {}).get("source_status", "offline_fixture_not_live"),
        "transcript_status": substitution_manifest.get("transcript_status", "sample_fixture_not_real"),
        "real_transcript_status": "blocked_by_real_input",
        "timing_status": substitution_manifest.get("timing_status", "no_audio_or_yymm4_timing"),
        "audio_status": substitution_manifest.get("audio_status", "no_audio_generated_or_imported"),
        "rights_status": dashboard_summary.get("boundary_status", {}).get("rights_status", "sample_only_no_publication"),
        "rights_gate": "blocked_by_true_gate",
        "production_status": "blocked_by_true_gate",
        "public_upload_status": "blocked_by_true_gate",
        "yymm4_gui_status": "blocked_by_true_gate",
        "yymm4_import_status": "blocked_by_true_gate",
        "yymm4_import_observed_status": "not_imported_to_yymm4",
        "bridge_yymm4_import_status": bridge_manifest.get("readiness", {}).get("yymm4_import_status", "not_run"),
        "yymm4_render_status": "blocked_by_true_gate",
        "thumbnail_proof_status": thumbnail_context.get("status", "unknown"),
        "thumbnail_context_status": "contextual_existing_not_current_target",
        "production_thumbnail_status": "blocked_by_true_gate",
    }
    return {
        "schema_version": "yymm4_import_readiness_summary.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "yymm4-import-preview-pack",
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": dashboard_summary.get("selected_candidate_id"),
        "status": "preview_ready_local_offline",
        "status_categories": list(IMPORT_PREVIEW_STATUS_CATEGORIES),
        "status_groups": {
            "ready": [
                "yymm4_csv_inventory",
                "cue_packet_inventory",
                "writer_ir_inventory",
                "dashboard_readiness_ingest",
                "gui_dashboard_panel",
                "thumbnail_visual_proof_context",
                "source_artifact_index",
            ],
            "sample_fixture_not_real": ["transcript_substitution_002"],
            "dry_run": ["import_preview_pack", "draft_yymm4_preview_csv"],
            "draft_offline": ["writer_ir_candidate", "cue_packet_candidate", "draft_yymm4_csv"],
            "blocked_by_real_input": ["real_transcript_input"],
            "blocked_by_true_gate": [
                "rights_gate",
                "public_upload_status",
                "yymm4_gui_status",
                "yymm4_import_status",
                "yymm4_render_status",
                "production_status",
            ],
            "validation_noise_nonblocking": ["validation_noise"],
            "deferred": ["production_thumbnail_acceptance", "actual_yymm4_import_review"],
            "missing": [],
            "unknown": [],
            "partial": [],
        },
        "csv": {
            "row_count": csv_inventory.get("row_count"),
            "header_mode": csv_inventory.get("header_mode"),
            "missing_required_fields": csv_inventory.get("missing_required_fields", []),
            "copied_preview_csv_path": csv_inventory.get("copied_preview_csv_path"),
        },
        "cue_packet": {
            "transcript_rows": cue_inventory.get("transcript_rows"),
            "section_count": cue_inventory.get("section_count"),
            "cue_or_beat_availability": cue_inventory.get("cue_or_beat_availability"),
        },
        "writer_ir": {
            "utterance_count": writer_inventory.get("utterance_count"),
            "section_count": writer_inventory.get("section_count"),
            "compatibility_status": writer_inventory.get("compatibility_status"),
            "validate_ir_ready": writer_inventory.get("validate_ir_ready"),
        },
        "boundary_flags": boundary_flags,
        "boundary_status": boundary_status,
        "validation_noise": validation_noise,
        "thumbnail_proof_context": thumbnail_context,
        "input_reality": gui_panel_data.get("input_reality", {}),
        "dashboard_readback_status": dashboard_summary.get("artifact_id"),
        "next_safe_local_action": (
            "Review import_preview_panel.md and draft_yymm4_preview.csv locally, using the "
            "existing thumbnail proof only as context; do not launch, import, render, approve "
            "a production thumbnail, or create a production .ymmp in this preview pack."
        ),
    }


def _source_artifact_index(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    repo_root: Path,
    paths: dict[str, Path],
    validation_noise: dict[str, Any],
) -> dict[str, Any]:
    source_keys = (
        "draft_csv",
        "bridge_csv",
        "cue_packet",
        "cue_readiness",
        "writer_ir",
        "substitution_manifest",
        "substitution_readback",
        "bridge_manifest",
        "bridge_readback",
        "dashboard_summary",
        "dashboard_readback",
        "gui_panel_data",
        "gui_readback",
        "gui_source_index",
        "dashboard_source_index",
        "transcript_source_index",
        "bridge_source_index",
        "thumbnail_readback",
        "thumbnail_variants",
        "thumbnail_html",
        "thumbnail_contact_sheet",
        "thumbnail_source_index",
    )
    return {
        "schema_version": "yymm4_import_preview_source_artifact_index.v1",
        "artifact_id": artifact_id,
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "source_artifacts": [_artifact_entry(key, paths[key], repo_root) for key in source_keys],
        "output_artifacts": [_artifact_entry(name, output_root / name, repo_root) for name in REQUIRED_IMPORT_PREVIEW_FILES],
        "validation_ledger": validation_noise,
    }


def _manifest_payload(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    summary: dict[str, Any],
    source_index: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "yymm4_import_preview_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "yymm4-import-preview-pack",
        "status": "generated",
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": summary.get("selected_candidate_id"),
        "files": {name: str(output_root / name) for name in REQUIRED_IMPORT_PREVIEW_FILES},
        "source_artifact_count": len(source_index.get("source_artifacts", [])),
        "boundaries": summary.get("boundary_flags", {}),
        "next_safe_local_action": summary.get("next_safe_local_action"),
    }


def _render_panel(
    summary: dict[str, Any],
    csv_inventory: dict[str, Any],
    cue_inventory: dict[str, Any],
    writer_inventory: dict[str, Any],
) -> str:
    lines = [
        "# YMM4 Import Preview Panel",
        "",
        f"- artifact_id: {summary.get('artifact_id')}",
        f"- selected_candidate_id: {summary.get('selected_candidate_id')}",
        f"- status: {summary.get('status')}",
        f"- source_artifact_index: `source_artifact_index.json`",
        f"- preview_csv: `{csv_inventory.get('copied_preview_csv_path')}`",
        "",
        "## Status Legend",
        "",
        "| status | visible meaning |",
        "|---|---|",
    ]
    for status in IMPORT_PREVIEW_STATUS_CATEGORIES:
        lines.append(f"| {status} | import preview state marker |")
    lines.extend([
        "",
        "## CSV Inventory",
        "",
        "| item | value |",
        "|---|---|",
        f"| source_csv_path | `{csv_inventory.get('source_csv_path')}` |",
        f"| copied_preview_csv_path | `{csv_inventory.get('copied_preview_csv_path')}` |",
        f"| row_count | {csv_inventory.get('row_count')} |",
        f"| header_mode | {csv_inventory.get('header_mode')} |",
        f"| required_fields | {', '.join(csv_inventory.get('required_fields', []))} |",
        f"| missing_required_fields | {csv_inventory.get('missing_required_fields', [])} |",
        f"| not_imported_to_yymm4 | {csv_inventory.get('not_imported_to_yymm4')} |",
        "",
        "## Cue / Writer IR",
        "",
        "| surface | status | rows_or_sections |",
        "|---|---|---|",
        f"| cue_packet | {cue_inventory.get('cue_or_beat_availability')} | transcript_rows={cue_inventory.get('transcript_rows')}; sections={cue_inventory.get('section_count')} |",
        f"| writer_ir | {writer_inventory.get('writer_ir_availability')} | utterances={writer_inventory.get('utterance_count')}; sections={writer_inventory.get('section_count')} |",
        "",
        "## Boundary Status",
        "",
        "| boundary | status |",
        "|---|---|",
    ])
    for key, value in summary.get("boundary_status", {}).items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Boundary Flags", "", "| flag | value |", "|---|---|"])
    for key, value in summary.get("boundary_flags", {}).items():
        lines.append(f"| {key} | {value} |")
    thumbnail_context = summary.get("thumbnail_proof_context", {})
    lines.extend([
        "",
        "## Thumbnail Proof Context",
        "",
        "| field | value |",
        "|---|---|",
        f"| status | {thumbnail_context.get('status')} |",
        f"| contextual_only | {thumbnail_context.get('contextual_only')} |",
        f"| current_implementation_target | {thumbnail_context.get('current_implementation_target')} |",
        f"| recommended_variant_id | {thumbnail_context.get('recommended_variant_id')} |",
        f"| primary_human_review | `{thumbnail_context.get('primary_human_review')}` |",
        f"| primary_machine_readable | `{thumbnail_context.get('primary_machine_readable')}` |",
        "",
        "## Validation Drift",
        "",
        f"- status: {summary.get('validation_noise', {}).get('status')}",
        f"- ledger_path: `{summary.get('validation_noise', {}).get('ledger_path')}`",
        f"- full_pytest_policy: {summary.get('validation_noise', {}).get('full_pytest_policy')}",
        f"- recent_full_pytest_result: {summary.get('validation_noise', {}).get('recent_full_pytest_result')}",
        "",
        "## Next Safe Local Action",
        "",
        str(summary.get("next_safe_local_action")),
        "",
    ])
    return "\n".join(lines)


def _render_checklist(summary: dict[str, Any], csv_inventory: dict[str, Any]) -> str:
    return "\n".join([
        "# YMM4 Import Preview Checklist",
        "",
        "- Open `import_preview_panel.md` locally.",
        "- Confirm `draft_yymm4_preview.csv` exists and is marked dry-run/sample-backed.",
        f"- Confirm CSV row count is `{csv_inventory.get('row_count')}` and header mode is `{csv_inventory.get('header_mode')}`.",
        "- Confirm cue packet and Writer IR are inventories only, not accepted production inputs.",
        "- Confirm the existing thumbnail visual proof is context only and not a production thumbnail approval.",
        "- Confirm `not_imported_to_yymm4`, `no_yymm4_import`, and `yymm4_render_closed` remain visible.",
        "- Confirm no public upload, render, rights, legal, payment, OAuth, or external media gate is implied open.",
        "",
        "## Next Safe Local Action",
        "",
        str(summary.get("next_safe_local_action")),
        "",
    ])


def _render_limitations(summary: dict[str, Any]) -> str:
    return "\n".join([
        "# YMM4 Import Preview Limitations",
        "",
        "This package is a local/offline import preview built from tracked episode 002 artifacts.",
        "",
        "Not performed:",
        "",
        "- real transcript rerun",
        "- YMM4 GUI launch/import/render",
        "- production .ymmp generation",
        "- audio timing or VoiceItem readback",
        "- public upload or publication",
        "- rights/legal/public-ready acceptance",
        "- thumbnail proof revision or production thumbnail acceptance",
        "- live scraping or external media download",
        "- full-suite green campaign",
        "",
        "Current safe action:",
        "",
        str(summary.get("next_safe_local_action")),
        "",
    ])


def _validation_noise_payload(repo_root: Path, gui_panel_data: dict[str, Any]) -> dict[str, Any]:
    gui_noise = gui_panel_data.get("validation_noise", {})
    if isinstance(gui_noise, dict) and gui_noise.get("status") == "validation_noise_nonblocking":
        return dict(gui_noise)
    ledger_path = repo_root / VALIDATION_LEDGER_PATH
    ledger = _load_json_if_present(ledger_path)
    if not isinstance(ledger, dict):
        return {
            "status": "unknown",
            "ledger_path": _relpath(ledger_path, repo_root),
            "exists": False,
            "blocking_for_this_slice": True,
        }
    full_pytest_input = ledger.get("validation_evidence", {}).get("recent_full_pytest_input", {})
    blocking_decision = ledger.get("blocking_decision", {})
    safe_to_continue = bool(blocking_decision.get("safe_to_continue_product_work"))
    return {
        "status": "validation_noise_nonblocking" if safe_to_continue else "unknown",
        "ledger_path": _relpath(ledger_path, repo_root),
        "exists": True,
        "safe_to_continue_product_work": safe_to_continue,
        "full_pytest_policy": full_pytest_input.get("policy_decision"),
        "recent_full_pytest_result": full_pytest_input.get("result"),
        "blocking_for_this_slice": False if safe_to_continue else True,
    }


def _csv_rows(text: str) -> list[list[str]]:
    return list(csv.reader(io.StringIO(text)))


def _header_mode(rows: list[list[str]]) -> str:
    if not rows:
        return "unknown"
    first = [cell.strip().lower() for cell in rows[0]]
    if "speaker" in first and "text" in first:
        return "headered"
    return "headerless"


def _artifact_entry(artifact_id: str, path: Path, repo_root: Path) -> dict[str, Any]:
    return {
        "id": artifact_id,
        "repo_relative_path": _relpath(path, repo_root),
        "exists": path.exists(),
        "state": "ready" if path.exists() else "missing",
    }


def _forbidden_true_claims(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
            for claim in FORBIDDEN_TRUE_CLAIMS:
                if claim in text:
                    hits.append(f"{path.name}:{claim}")
    return hits


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON input must be an object: {path}")
    return data


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


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
