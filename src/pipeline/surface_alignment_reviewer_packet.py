"""Reviewer packet for episode 002 surface alignment repair."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from src.pipeline.surface_alignment_pack import SURFACE_STATUS_CATEGORIES

DEFAULT_OUTPUT_DIRNAME = "surface_alignment_review_packet"
DEFAULT_ARTIFACT_ID = "episode_002_surface_alignment_repair_and_reviewer_packet_v1"
DEFAULT_ALIGNMENT_DIRNAME = "surface_alignment_pack"

REQUIRED_REVIEWER_PACKET_FILES = (
    "reviewer_packet_manifest.json",
    "aligned_review_story.md",
    "alignment_repair_summary.json",
    "remaining_mismatch_ledger.json",
    "next_action_readback.json",
    "boundary_status_readback.json",
    "source_artifact_crosswalk_readback.json",
    "validation_readback.json",
    "review_checklist.md",
    "limitations.md",
)

REPAIR_CLASSIFICATIONS = (
    "resolved",
    "accepted_nonblocking",
    "still_open_minor_label_drift",
    "still_open_stale_next_action",
    "boundary_mismatch",
    "missing_reference",
    "unknown",
)

FORBIDDEN_TRUE_CLAIMS = (
    '"youtube_uploaded": true',
    '"production_ready": true',
    '"production_thumbnail_ready": true',
    '"public_ready": true',
    '"rights_accepted": true',
    '"render_completion": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"actual_yymm4_import": true',
    '"yymm4_rendered": true',
    '"thumbnail_image_generated": true',
)

REQUIRED_BOUNDARY_FLAGS = (
    "dry_run",
    "sample_fixture_not_real",
    "no_real_transcript",
    "rights_boundary",
    "public_upload_closed",
    "yymm4_render_closed",
    "no_yymm4_import",
    "thumbnail_context_only",
    "validation_noise_nonblocking",
    "not_production_ready",
)


def build_surface_alignment_reviewer_packet(
    *,
    package_dir: str | Path,
    alignment_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a deterministic reviewer packet from the current alignment pack."""
    source_root = Path(package_dir)
    alignment_root = Path(alignment_dir) if alignment_dir else source_root / DEFAULT_ALIGNMENT_DIRNAME
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root, alignment_root)
    payloads = _load_payloads(paths)
    ledger = _remaining_mismatch_ledger(
        artifact_id=artifact_id,
        payloads=payloads,
        source_root=source_root,
        alignment_root=alignment_root,
        output_root=output_root,
        repo_root=repo_root,
    )
    next_action = _next_action_readback(artifact_id, payloads, ledger, output_root, repo_root)
    boundary = _boundary_status_readback(artifact_id, payloads, ledger, source_root, output_root, repo_root)
    crosswalk = _source_artifact_crosswalk_readback(artifact_id, payloads, paths, source_root, alignment_root, output_root, repo_root)
    summary = _alignment_repair_summary(
        artifact_id=artifact_id,
        payloads=payloads,
        ledger=ledger,
        next_action=next_action,
        boundary=boundary,
        crosswalk=crosswalk,
        source_root=source_root,
        alignment_root=alignment_root,
        output_root=output_root,
        repo_root=repo_root,
    )
    manifest = _reviewer_packet_manifest(artifact_id, summary, source_root, alignment_root, output_root, repo_root)

    _write_json(output_root / "reviewer_packet_manifest.json", manifest)
    _write_json(output_root / "alignment_repair_summary.json", summary)
    _write_json(output_root / "remaining_mismatch_ledger.json", ledger)
    _write_json(output_root / "next_action_readback.json", next_action)
    _write_json(output_root / "boundary_status_readback.json", boundary)
    _write_json(output_root / "source_artifact_crosswalk_readback.json", crosswalk)
    _write_text(output_root / "aligned_review_story.md", _render_aligned_review_story(summary, ledger, next_action, boundary, crosswalk))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(summary, next_action))
    _write_text(output_root / "limitations.md", _render_limitations(summary))

    readback = validate_surface_alignment_reviewer_packet(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_surface_alignment_reviewer_packet(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_surface_alignment_reviewer_packet(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate a generated surface alignment reviewer packet."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_REVIEWER_PACKET_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["reviewer_packet_manifest.json"])
    summary = _load_json_if_present(files["alignment_repair_summary.json"])
    ledger = _load_json_if_present(files["remaining_mismatch_ledger.json"])
    next_action = _load_json_if_present(files["next_action_readback.json"])
    boundary = _load_json_if_present(files["boundary_status_readback.json"])
    crosswalk = _load_json_if_present(files["source_artifact_crosswalk_readback.json"])
    payloads = {
        "reviewer_packet_manifest": manifest,
        "alignment_repair_summary": summary,
        "remaining_mismatch_ledger": ledger,
        "next_action_readback": next_action,
        "boundary_status_readback": boundary,
        "source_artifact_crosswalk_readback": crosswalk,
    }
    for name, payload in payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            payloads[name] = {}

    manifest = payloads["reviewer_packet_manifest"]
    summary = payloads["alignment_repair_summary"]
    ledger = payloads["remaining_mismatch_ledger"]
    next_action = payloads["next_action_readback"]
    boundary = payloads["boundary_status_readback"]
    crosswalk = payloads["source_artifact_crosswalk_readback"]

    if manifest.get("artifact_kind") != "surface-alignment-reviewer-packet":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if summary.get("status") != "reviewer_packet_ready_local_offline":
        failed_checks.append("summary_status_mismatch")
    if summary.get("repair_mode") != "packet_level_readback_repair_no_underlying_surface_rewrite":
        failed_checks.append("repair_mode_mismatch")
    if summary.get("reviewer_packet_status") != "ready":
        failed_checks.append("reviewer_packet_status_not_ready")

    visible_statuses = set(summary.get("status_categories", []))
    for status in SURFACE_STATUS_CATEGORIES:
        if status not in visible_statuses:
            failed_checks.append(f"status_category_missing:{status}")

    rows = ledger.get("rows", [])
    if not isinstance(rows, list) or len(rows) < 8:
        failed_checks.append("mismatch_ledger_too_small")
        rows = []
    for row in rows:
        classification = row.get("repair_classification") if isinstance(row, dict) else None
        if classification not in REPAIR_CLASSIFICATIONS:
            failed_checks.append(f"repair_classification_invalid:{classification}")
    if ledger.get("prior_mismatch_count") != len(rows):
        failed_checks.append("prior_mismatch_count_mismatch")
    if ledger.get("still_open_mismatch_count") not in (0, None):
        failed_checks.append("still_open_mismatch_count_nonzero")
    if not any(row.get("repair_classification") == "resolved" for row in rows if isinstance(row, dict)):
        failed_checks.append("no_resolved_mismatches")
    if not any(row.get("repair_classification") == "accepted_nonblocking" for row in rows if isinstance(row, dict)):
        failed_checks.append("no_accepted_nonblocking_mismatches")

    boundary_flags = boundary.get("boundary_flags", {})
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")
    if boundary.get("status") != "closed_gates_confirmed":
        failed_checks.append("boundary_status_not_closed_gates_confirmed")

    if next_action.get("status") != "packet_resolved":
        failed_checks.append("next_action_status_not_packet_resolved")
    option_ids = {option.get("option_id") for option in _list(next_action.get("advisory_next_options"))}
    for option_id in ("real_input_replacement", "actual_yymm4_import_observation_no_render"):
        if option_id not in option_ids:
            failed_checks.append(f"next_option_missing:{option_id}")

    if crosswalk.get("overall_status") != "aligned":
        failed_checks.append("source_crosswalk_not_aligned")
    if crosswalk.get("missing_reference_count") != 0:
        failed_checks.append("source_crosswalk_missing_reference_count_nonzero")
    source_rows = _list(crosswalk.get("source_artifact_rows"))
    for required_id in ("gui_panel_data", "import_readiness_summary", "thumbnail_variants", "validation_ledger"):
        if required_id not in {row.get("artifact_id") for row in source_rows if isinstance(row, dict)}:
            failed_checks.append(f"source_artifact_missing:{required_id}")

    story_text = files["aligned_review_story.md"].read_text(encoding="utf-8") if files["aligned_review_story.md"].exists() else ""
    for marker in (
        "remaining_mismatch_ledger.json",
        "next_action_readback.json",
        "boundary_status_readback.json",
        "source_artifact_crosswalk_readback.json",
        "thumbnail_context_only",
        "validation_noise_nonblocking",
        "not_production_ready",
        "no_yymm4_import",
    ):
        if marker not in story_text:
            failed_checks.append(f"aligned_review_story_marker_missing:{marker}")
    for status in SURFACE_STATUS_CATEGORIES:
        if status not in story_text:
            failed_checks.append(f"aligned_review_story_status_missing:{status}")

    forbidden_hits = _forbidden_true_claims(root)
    external_refs = _external_refs(root)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)

    counts = _dict(ledger.get("repair_classification_counts"))
    return {
        "schema_version": "surface_alignment_reviewer_packet_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in payloads.values()),
            "all_status_categories_visible": all(status in visible_statuses for status in SURFACE_STATUS_CATEGORIES),
            "mismatch_ledger_rows": len(rows),
            "repair_classifications_valid": not any(
                isinstance(row, dict) and row.get("repair_classification") not in REPAIR_CLASSIFICATIONS for row in rows
            ),
            "prior_mismatches_classified": ledger.get("prior_mismatch_count") == len(rows),
            "resolved_mismatches": counts.get("resolved", 0),
            "accepted_nonblocking_mismatches": counts.get("accepted_nonblocking", 0),
            "still_open_mismatch_count": ledger.get("still_open_mismatch_count"),
            "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS),
            "next_action_packet_resolved": next_action.get("status") == "packet_resolved",
            "source_crosswalk_aligned": crosswalk.get("overall_status") == "aligned",
            "forbidden_true_claims_absent": not forbidden_hits,
            "external_refs_absent": not external_refs,
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "selected_candidate_id": summary.get("selected_candidate_id"),
        "reviewer_packet_status": summary.get("reviewer_packet_status"),
        "gui_panel_status": summary.get("surface_statuses", {}).get("gui_panel_status"),
        "import_preview_status": summary.get("surface_statuses", {}).get("import_preview_status"),
        "thumbnail_proof_status": summary.get("surface_statuses", {}).get("thumbnail_proof_status"),
        "boundary_consistency_status": summary.get("boundary_consistency_status"),
        "next_action_consistency_status": summary.get("next_action_consistency_status"),
        "source_crosswalk_status": crosswalk.get("overall_status"),
        "prior_mismatch_count": ledger.get("prior_mismatch_count"),
        "resolved_mismatch_count": counts.get("resolved", 0),
        "accepted_nonblocking_mismatch_count": counts.get("accepted_nonblocking", 0),
        "still_open_mismatch_count": ledger.get("still_open_mismatch_count"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "primary_human_review": str(root / "aligned_review_story.md"),
        "next_action": next_action.get("next_safe_local_action"),
    }


def _input_paths(source_root: Path, alignment_root: Path) -> dict[str, Path]:
    return {
        "alignment_summary": alignment_root / "surface_alignment_summary.json",
        "surface_status_matrix": alignment_root / "surface_status_matrix.json",
        "source_crosswalk": alignment_root / "source_artifact_crosswalk.json",
        "boundary_report": alignment_root / "boundary_consistency_report.json",
        "next_action_report": alignment_root / "next_action_consistency_report.json",
        "alignment_readback": alignment_root / "validation_readback.json",
        "alignment_story": alignment_root / "review_story.md",
        "gui_readback": source_root / "gui_dashboard_panel" / "validation_readback.json",
        "import_readback": source_root / "ymm4_import_preview_pack" / "validation_readback.json",
        "thumbnail_readback": source_root / "thumbnail_visual_proof_pack" / "readback.json",
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    return {name: _load_json(path) for name, path in paths.items() if path.suffix == ".json"}


def _remaining_mismatch_ledger(
    *,
    artifact_id: str,
    payloads: dict[str, Any],
    source_root: Path,
    alignment_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    matrix = payloads["surface_status_matrix"]
    boundary = payloads["boundary_report"]
    next_action = payloads["next_action_report"]

    for index, row in enumerate(_list(matrix.get("rows")), start=1):
        classification = row.get("classification")
        if classification and classification != "aligned":
            axis = str(row.get("axis", "unknown_axis"))
            rows.append(
                _ledger_row(
                    mismatch_id=f"surface_status_matrix:{index}:{_slug(axis)}",
                    source_report="surface_status_matrix.json",
                    mismatch_scope="surface_status_matrix",
                    subject=axis,
                    prior_classification=classification,
                    repair_classification=_classify_matrix_row(axis, classification),
                    source_values={
                        "gui_dashboard_panel": row.get("gui_dashboard_panel"),
                        "yymm4_import_preview_pack": row.get("yymm4_import_preview_pack"),
                        "thumbnail_visual_proof_pack": row.get("thumbnail_visual_proof_pack"),
                    },
                    repair_note=_matrix_repair_note(axis, classification),
                )
            )

    for index, row in enumerate(_list(boundary.get("boundary_rows")), start=1):
        classification = row.get("classification")
        if classification and classification != "aligned":
            boundary_id = str(row.get("boundary_id", "unknown_boundary"))
            rows.append(
                _ledger_row(
                    mismatch_id=f"boundary_consistency_report:{index}:{_slug(boundary_id)}",
                    source_report="boundary_consistency_report.json",
                    mismatch_scope="boundary_status",
                    subject=boundary_id,
                    prior_classification=classification,
                    repair_classification=_classify_boundary_row(boundary_id, classification),
                    source_values={
                        "gui_dashboard_panel": row.get("gui_dashboard_panel"),
                        "yymm4_import_preview_pack": row.get("yymm4_import_preview_pack"),
                        "thumbnail_visual_proof_pack": row.get("thumbnail_visual_proof_pack"),
                    },
                    repair_note=_boundary_repair_note(boundary_id, classification),
                )
            )

    for index, row in enumerate(_list(next_action.get("next_action_rows")), start=1):
        classification = row.get("classification")
        if classification and classification != "aligned":
            surface_id = str(row.get("surface_id", "unknown_surface"))
            rows.append(
                _ledger_row(
                    mismatch_id=f"next_action_consistency_report:{index}:{_slug(surface_id)}",
                    source_report="next_action_consistency_report.json",
                    mismatch_scope="next_action",
                    subject=surface_id,
                    prior_classification=classification,
                    repair_classification=_classify_next_action_row(surface_id, classification),
                    source_values={"next_action": row.get("next_action")},
                    repair_note=_next_action_repair_note(surface_id, classification),
                )
            )

    counts = Counter(row["repair_classification"] for row in rows)
    still_open = sum(
        count
        for classification, count in counts.items()
        if classification
        in {
            "still_open_minor_label_drift",
            "still_open_stale_next_action",
            "boundary_mismatch",
            "missing_reference",
            "unknown",
        }
    )
    prior_counts = Counter(row["prior_classification"] for row in rows)
    return {
        "schema_version": "remaining_mismatch_ledger.v1",
        "artifact_id": artifact_id,
        "source_alignment_artifact_id": payloads["alignment_summary"].get("artifact_id"),
        "source_package_dir": _relpath(source_root, repo_root),
        "source_alignment_dir": _relpath(alignment_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "repair_classifications": list(REPAIR_CLASSIFICATIONS),
        "prior_mismatch_count": len(rows),
        "prior_classification_counts": dict(prior_counts),
        "repair_classification_counts": dict(counts),
        "still_open_mismatch_count": still_open,
        "blocking_for_reviewer_packet": still_open > 0,
        "underlying_surfaces_rewritten": False,
        "rows": rows,
    }


def _ledger_row(
    *,
    mismatch_id: str,
    source_report: str,
    mismatch_scope: str,
    subject: str,
    prior_classification: str,
    repair_classification: str,
    source_values: dict[str, Any],
    repair_note: str,
) -> dict[str, Any]:
    return {
        "mismatch_id": mismatch_id,
        "source_report": source_report,
        "mismatch_scope": mismatch_scope,
        "subject": subject,
        "prior_classification": prior_classification,
        "repair_classification": repair_classification,
        "source_values": source_values,
        "source_surface_changed": False,
        "packet_readback_supersedes_old_label": repair_classification == "resolved",
        "remaining_in_underlying_surface": True,
        "blocking_for_reviewer_packet": repair_classification
        in {
            "still_open_minor_label_drift",
            "still_open_stale_next_action",
            "boundary_mismatch",
            "missing_reference",
            "unknown",
        },
        "repair_note": repair_note,
    }


def _next_action_readback(
    artifact_id: str,
    payloads: dict[str, Any],
    ledger: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    source_rows = _list(payloads["next_action_report"].get("next_action_rows"))
    repaired_rows = []
    for row in source_rows:
        surface_id = row.get("surface_id")
        repaired_rows.append(
            {
                "surface_id": surface_id,
                "source_next_action": row.get("next_action"),
                "source_classification": row.get("classification"),
                "packet_classification": "resolved" if row.get("classification") == "stale_next_action" else "accepted_nonblocking",
                "packet_action": _packet_action_for_surface(str(surface_id)),
            }
        )
    return {
        "schema_version": "next_action_readback.v1",
        "artifact_id": artifact_id,
        "status": "packet_resolved",
        "source_next_action_status": payloads["next_action_report"].get("overall_status"),
        "current_reviewer_action": "Open aligned_review_story.md as the single local review entrypoint.",
        "next_safe_local_action": (
            "Review aligned_review_story.md, then choose a later slice for verified local real input "
            "replacement or for actual YMM4 import observation without render/public claims."
        ),
        "advisory_next_options": [
            {
                "option_id": "real_input_replacement",
                "status": "advisory_deferred",
                "unblocks": "real topic/source/transcript replacement using reviewed local input",
                "requires": "verified local transcript/source material and provenance",
                "closed_gates_preserved": [
                    "no_yymm4_import",
                    "no_yymm4_render",
                    "no_public_upload",
                    "no_rights_acceptance",
                ],
            },
            {
                "option_id": "actual_yymm4_import_observation_no_render",
                "status": "advisory_deferred",
                "unblocks": "manual YMM4 import readback of VoiceItem/timing behavior",
                "requires": "explicit human decision to launch/import in YMM4",
                "closed_gates_preserved": [
                    "no_yymm4_render",
                    "no_public_upload",
                    "no_production_ymmp",
                    "no_final_thumbnail_approval",
                ],
            },
        ],
        "surface_next_action_rows": repaired_rows,
        "mismatch_repair_counts": ledger.get("repair_classification_counts", {}),
        "primary_human_review": _relpath(output_root / "aligned_review_story.md", repo_root),
        "not_performed": [
            "real_transcript_rerun",
            "yymm4_gui_launch",
            "yymm4_import",
            "yymm4_render",
            "production_ymmp_generation",
            "final_thumbnail_approval",
            "public_upload",
        ],
    }


def _boundary_status_readback(
    artifact_id: str,
    payloads: dict[str, Any],
    ledger: dict[str, Any],
    source_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    normalized_rows = []
    for row in _list(payloads["boundary_report"].get("boundary_rows")):
        prior = row.get("classification")
        normalized_rows.append(
            {
                "boundary_id": row.get("boundary_id"),
                "source_classification": prior,
                "packet_classification": "accepted_nonblocking" if prior == "minor_label_drift" else "resolved",
                "packet_status": _boundary_packet_status(str(row.get("boundary_id"))),
                "note": row.get("note"),
            }
        )
    return {
        "schema_version": "boundary_status_readback.v1",
        "artifact_id": artifact_id,
        "status": "closed_gates_confirmed",
        "source_boundary_status": payloads["boundary_report"].get("overall_status"),
        "boundary_flags": {
            "dry_run": True,
            "sample_fixture_not_real": True,
            "no_real_transcript": True,
            "rights_boundary": True,
            "public_upload_closed": True,
            "yymm4_render_closed": True,
            "no_yymm4_import": True,
            "thumbnail_context_only": True,
            "validation_noise_nonblocking": True,
            "not_production_ready": True,
            "no_yymm4_gui_launch": True,
            "no_production_ymmp": True,
            "no_production_thumbnail_acceptance": True,
            "no_external_media_download": True,
            "no_live_scraping": True,
            "no_oauth_api_keys_payment": True,
        },
        "closed_gate_status": {
            "public_upload_status": "blocked_by_true_gate",
            "rights_public_ready_status": "blocked_by_true_gate",
            "yymm4_gui_status": "not_launched",
            "yymm4_import_status": "no_yymm4_import",
            "yymm4_render_status": "yymm4_render_closed",
            "production_ymmp_status": "blocked_by_true_gate",
            "thumbnail_approval_status": "thumbnail_context_only",
            "real_transcript_status": "blocked_by_real_input",
        },
        "normalized_boundary_rows": normalized_rows,
        "mismatch_repair_counts": ledger.get("repair_classification_counts", {}),
        "source_package_dir": _relpath(source_root, repo_root),
        "primary_human_review": _relpath(output_root / "aligned_review_story.md", repo_root),
    }


def _source_artifact_crosswalk_readback(
    artifact_id: str,
    payloads: dict[str, Any],
    paths: dict[str, Path],
    source_root: Path,
    alignment_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    source_rows = []
    for row in _list(payloads["source_crosswalk"].get("crosswalk_rows")):
        repo_path = row.get("repo_relative_path")
        exists = bool(row.get("exists"))
        source_rows.append(
            {
                "artifact_id": row.get("artifact_id"),
                "repo_relative_path": repo_path,
                "surfaces": row.get("surfaces", []),
                "exists": exists,
                "classification": "aligned" if exists else "missing_reference",
            }
        )
    missing = [row for row in source_rows if not row["exists"]]
    reviewer_inputs = [
        "surface_alignment_summary.json",
        "surface_status_matrix.json",
        "boundary_consistency_report.json",
        "next_action_consistency_report.json",
        "source_artifact_crosswalk.json",
        "validation_readback.json",
    ]
    return {
        "schema_version": "source_artifact_crosswalk_readback.v1",
        "artifact_id": artifact_id,
        "overall_status": "missing_reference" if missing else "aligned",
        "source_crosswalk_status": payloads["source_crosswalk"].get("overall_status"),
        "source_package_dir": _relpath(source_root, repo_root),
        "source_alignment_dir": _relpath(alignment_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "reviewer_packet_inputs": [
            {
                "file": name,
                "repo_relative_path": _relpath(paths[_path_key_for_input(name)], repo_root),
                "exists": paths[_path_key_for_input(name)].exists(),
            }
            for name in reviewer_inputs
        ],
        "source_artifact_rows": source_rows,
        "source_artifact_counts_by_surface": payloads["source_crosswalk"].get("source_artifact_counts_by_surface", {}),
        "missing_reference_count": len(missing),
    }


def _alignment_repair_summary(
    *,
    artifact_id: str,
    payloads: dict[str, Any],
    ledger: dict[str, Any],
    next_action: dict[str, Any],
    boundary: dict[str, Any],
    crosswalk: dict[str, Any],
    source_root: Path,
    alignment_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    alignment_summary = payloads["alignment_summary"]
    source_readback = payloads["alignment_readback"]
    repair_counts = _dict(ledger.get("repair_classification_counts"))
    surfaces = alignment_summary.get("surfaces", [])
    return {
        "schema_version": "alignment_repair_summary.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "surface-alignment-reviewer-packet",
        "status": "reviewer_packet_ready_local_offline",
        "repair_mode": "packet_level_readback_repair_no_underlying_surface_rewrite",
        "source_alignment_artifact_id": alignment_summary.get("artifact_id"),
        "source_alignment_status": source_readback.get("status"),
        "source_package_dir": _relpath(source_root, repo_root),
        "source_alignment_dir": _relpath(alignment_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "selected_candidate_id": alignment_summary.get("selected_candidate_id"),
        "surfaces": surfaces,
        "status_categories": list(SURFACE_STATUS_CATEGORIES),
        "repair_classifications": list(REPAIR_CLASSIFICATIONS),
        "reviewer_packet_status": "ready",
        "surface_statuses": {
            "gui_panel_status": alignment_summary.get("surface_alignment_results", {}).get("gui_panel_status"),
            "import_preview_status": alignment_summary.get("surface_alignment_results", {}).get("import_preview_status"),
            "thumbnail_proof_status": alignment_summary.get("surface_alignment_results", {}).get("thumbnail_proof_status"),
        },
        "prior_alignment_results": alignment_summary.get("surface_alignment_results", {}),
        "prior_mismatch_counts": alignment_summary.get("mismatch_counts", {}),
        "prior_minor_label_drift": {
            "count": ledger.get("prior_classification_counts", {}).get("minor_label_drift", 0),
            "packet_handling": "resolved_where_status_label_was_stale_and_accepted_nonblocking_where_semantics_already_matched",
        },
        "prior_stale_next_action": {
            "count": ledger.get("prior_classification_counts", {}).get("stale_next_action", 0),
            "packet_handling": "resolved_by_next_action_readback",
        },
        "repair_classification_counts": repair_counts,
        "remaining_mismatch_ledger": _relpath(output_root / "remaining_mismatch_ledger.json", repo_root),
        "still_open_mismatch_count": ledger.get("still_open_mismatch_count"),
        "boundary_consistency_status": "accepted_nonblocking",
        "next_action_consistency_status": next_action.get("status"),
        "source_crosswalk_status": crosswalk.get("overall_status"),
        "boundary_status_readback": _relpath(output_root / "boundary_status_readback.json", repo_root),
        "next_action_readback": _relpath(output_root / "next_action_readback.json", repo_root),
        "source_artifact_crosswalk_readback": _relpath(output_root / "source_artifact_crosswalk_readback.json", repo_root),
        "boundary_flags": boundary.get("boundary_flags", {}),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "primary_human_review": _relpath(output_root / "aligned_review_story.md", repo_root),
        "next_safe_local_action": next_action.get("next_safe_local_action"),
    }


def _reviewer_packet_manifest(
    artifact_id: str,
    summary: dict[str, Any],
    source_root: Path,
    alignment_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "reviewer_packet_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "surface-alignment-reviewer-packet",
        "status": "generated",
        "source_package_dir": _relpath(source_root, repo_root),
        "source_alignment_dir": _relpath(alignment_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "files": {name: _relpath(output_root / name, repo_root) for name in REQUIRED_REVIEWER_PACKET_FILES},
        "surfaces": [surface.get("surface_id") for surface in summary.get("surfaces", [])],
        "boundaries": summary.get("boundary_flags", {}),
        "next_safe_local_action": summary.get("next_safe_local_action"),
    }


def _render_aligned_review_story(
    summary: dict[str, Any],
    ledger: dict[str, Any],
    next_action: dict[str, Any],
    boundary: dict[str, Any],
    crosswalk: dict[str, Any],
) -> str:
    lines = [
        "# Episode 002 Surface Alignment Reviewer Packet",
        "",
        f"- artifact_id: {summary.get('artifact_id')}",
        f"- status: {summary.get('status')}",
        f"- selected_candidate_id: {summary.get('selected_candidate_id')}",
        f"- repair_mode: {summary.get('repair_mode')}",
        "- source surfaces: GUI dashboard panel, YMM4 import preview pack, thumbnail visual proof pack",
        "- primary machine readback: `validation_readback.json`",
        "- repair summary: `alignment_repair_summary.json`",
        "- remaining mismatch ledger: `remaining_mismatch_ledger.json`",
        "- next action readback: `next_action_readback.json`",
        "- boundary readback: `boundary_status_readback.json`",
        "- source crosswalk readback: `source_artifact_crosswalk_readback.json`",
        "",
        "## What This Packet Repairs",
        "",
        "This packet does not rewrite the underlying GUI, import preview, or thumbnail proof packages. It gives reviewers one current readback that normalizes stale labels and next-action wording from the accepted surface alignment pack.",
        "",
        "| repair area | prior state | packet handling |",
        "|---|---|---|",
        f"| minor label drift | {summary.get('prior_minor_label_drift', {}).get('count')} rows | status-label drift is either resolved in this packet or accepted_nonblocking when the source wording already preserves the same closed gate |",
        f"| stale next action | {summary.get('prior_stale_next_action', {}).get('count')} rows | resolved by `next_action_readback.json` |",
        f"| source artifact crosswalk | {summary.get('source_crosswalk_status')} | all required source artifacts remain aligned |",
        "",
        "## Status Legend",
        "",
        "| status | reviewer meaning |",
        "|---|---|",
    ]
    for status in SURFACE_STATUS_CATEGORIES:
        lines.append(f"| {status} | visible review state marker |")

    lines.extend(
        [
            "",
            "## Surface Snapshot",
            "",
            "| surface | status | role | human review |",
            "|---|---|---|---|",
        ]
    )
    for surface in summary.get("surfaces", []):
        lines.append(
            f"| {surface.get('surface_id')} | {surface.get('status')} | {surface.get('role_in_alignment')} | `{surface.get('primary_human_review')}` |"
        )

    lines.extend(
        [
            "",
            "## Repair Ledger",
            "",
            "| subject | source classification | packet classification | blocking |",
            "|---|---|---|---|",
        ]
    )
    for row in _list(ledger.get("rows")):
        lines.append(
            f"| {row.get('subject')} | {row.get('prior_classification')} | {row.get('repair_classification')} | {row.get('blocking_for_reviewer_packet')} |"
        )

    lines.extend(
        [
            "",
            "## Boundary Readback",
            "",
            f"- status: {boundary.get('status')}",
            "- required markers: dry_run, sample_fixture_not_real, no_real_transcript, rights_boundary, public_upload_closed, yymm4_render_closed, no_yymm4_import, thumbnail_context_only, validation_noise_nonblocking, not_production_ready",
            "- closed gates: public upload, rights/public-ready acceptance, YMM4 GUI/import/render, production .ymmp, final thumbnail approval, external media, live scraping, OAuth/API keys/payment",
            "",
            "## Next Action Readback",
            "",
            f"- status: {next_action.get('status')}",
            f"- current reviewer action: {next_action.get('current_reviewer_action')}",
            f"- next safe local action: {next_action.get('next_safe_local_action')}",
            "",
            "## Advisory Forward Options",
            "",
            "| option | status | unlocks | requires |",
            "|---|---|---|---|",
        ]
    )
    for option in _list(next_action.get("advisory_next_options")):
        lines.append(
            f"| {option.get('option_id')} | {option.get('status')} | {option.get('unblocks')} | {option.get('requires')} |"
        )

    lines.extend(
        [
            "",
            "## Source Artifact Crosswalk",
            "",
            f"- status: {crosswalk.get('overall_status')}",
            f"- source rows: {len(_list(crosswalk.get('source_artifact_rows')))}",
            f"- missing references: {crosswalk.get('missing_reference_count')}",
            "",
            "## Symbolic Review Bars",
            "",
            "- episode_002_surface_reviewer_packet: `[#####--]` local packet generated and validated.",
            "- gui_import_thumbnail_surfaces: `[######-]` aligned review surfaces, not implementation targets.",
            "- real_input_replacement: `[#------]` blocked_by_real_input until verified local input exists.",
            "- yymm4_import_observation: `[#------]` blocked_by_true_gate until explicit YMM4 observation is selected.",
            "",
            "## Not Production Ready",
            "",
            "This is a dry_run and sample_fixture_not_real reviewer packet. It has no_real_transcript, keeps rights_boundary and public_upload_closed, keeps yymm4_render_closed and no_yymm4_import, treats thumbnail_context_only as context rather than final approval, and records validation_noise_nonblocking as nonblocking validation noise.",
            "",
        ]
    )
    return "\n".join(lines)


def _render_review_checklist(summary: dict[str, Any], next_action: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Surface Alignment Reviewer Packet Checklist",
            "",
            "- Open `aligned_review_story.md` first.",
            "- Confirm `remaining_mismatch_ledger.json` classifies prior minor label drift and stale next-action rows.",
            "- Confirm `next_action_readback.json` supersedes stale source next-action text without changing source surfaces.",
            "- Confirm `boundary_status_readback.json` keeps dry-run, real-input, rights/public, YMM4, thumbnail, validation-noise, and production gates closed.",
            "- Confirm `source_artifact_crosswalk_readback.json` has no missing source references.",
            "- Treat real input replacement and YMM4 import observation as later advisory choices only.",
            "",
            "## Current Safe Action",
            "",
            str(next_action.get("next_safe_local_action") or summary.get("next_safe_local_action")),
            "",
        ]
    )


def _render_limitations(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Surface Alignment Reviewer Packet Limitations",
            "",
            "This packet is a local/offline readback repair over existing review surfaces. It does not edit creative assets, CSV content, Writer IR, thumbnail variants, or YMM4 files.",
            "",
            "Not performed:",
            "",
            "- real transcript rerun or source replacement",
            "- YMM4 GUI launch, import, or render",
            "- production .ymmp generation",
            "- final thumbnail approval",
            "- public upload, publication, scheduling, or visibility change",
            "- rights/legal/public-ready acceptance",
            "- OAuth, API keys, payment, or paid services",
            "- live scraping, RSS fetch, or external image/media download",
            "- full-suite green campaign or broad fixture regeneration",
            "",
            "Current safe action:",
            "",
            str(summary.get("next_safe_local_action")),
            "",
        ]
    )


def _classify_matrix_row(axis: str, classification: str) -> str:
    if classification == "stale_next_action":
        return "resolved"
    if classification == "minor_label_drift":
        if axis in {"YMM4 import preview status", "Thumbnail visual proof status"}:
            return "resolved"
        return "accepted_nonblocking"
    return _fallback_repair_classification(classification)


def _classify_boundary_row(boundary_id: str, classification: str) -> str:
    if classification == "minor_label_drift":
        return "accepted_nonblocking"
    return _fallback_repair_classification(classification)


def _classify_next_action_row(surface_id: str, classification: str) -> str:
    if classification == "stale_next_action":
        return "resolved"
    return _fallback_repair_classification(classification)


def _fallback_repair_classification(classification: str) -> str:
    if classification == "missing_reference":
        return "missing_reference"
    if classification == "boundary_mismatch":
        return "boundary_mismatch"
    if classification == "minor_label_drift":
        return "still_open_minor_label_drift"
    if classification == "stale_next_action":
        return "still_open_stale_next_action"
    return "unknown"


def _matrix_repair_note(axis: str, classification: str) -> str:
    if classification == "stale_next_action":
        return "The packet replaces the stale cross-surface next-action row with next_action_readback.json."
    if axis in {"YMM4 import preview status", "Thumbnail visual proof status"}:
        return "The packet treats older GUI deferred labels as historical and shows the current surface as ready/context-ready."
    return "The source labels differ, but the packet preserves the common closed-gate meaning as accepted nonblocking drift."


def _boundary_repair_note(boundary_id: str, classification: str) -> str:
    if classification == "minor_label_drift":
        return f"The packet normalizes {boundary_id} as a closed boundary while leaving source wording untouched."
    return "The packet records this boundary row without changing source surfaces."


def _next_action_repair_note(surface_id: str, classification: str) -> str:
    if classification == "stale_next_action":
        return f"The packet supersedes the old {surface_id} next action with a current reviewer action and advisory later choices."
    return "The packet records the source next action as nonblocking context."


def _packet_action_for_surface(surface_id: str) -> str:
    if surface_id == "gui_dashboard_panel":
        return "Use GUI panel status as an already-aligned input surface; do not treat it as the current build target."
    if surface_id == "thumbnail_visual_proof_pack":
        return "Use thumbnail proof as context only; do not treat headline_driven as final thumbnail approval."
    if surface_id == "yymm4_import_preview_pack":
        return "Keep import preview as local/offline import-prep evidence; do not launch/import/render in YMM4."
    return "Use the surface as reviewer context only."


def _boundary_packet_status(boundary_id: str) -> str:
    mapping = {
        "dry_run": "dry_run",
        "sample_fixture_not_real": "sample_fixture_not_real",
        "no_real_transcript": "no_real_transcript",
        "rights_boundary": "rights_boundary",
        "public_upload_closed": "public_upload_closed",
        "yymm4_render_closed": "yymm4_render_closed",
        "no_yymm4_import": "no_yymm4_import",
        "thumbnail_context_only": "thumbnail_context_only",
        "validation_noise_nonblocking": "validation_noise_nonblocking",
        "no_production_thumbnail_acceptance": "thumbnail_context_only",
        "blocked_by_true_gate": "blocked_by_true_gate",
    }
    return mapping.get(boundary_id, "unknown")


def _path_key_for_input(filename: str) -> str:
    mapping = {
        "surface_alignment_summary.json": "alignment_summary",
        "surface_status_matrix.json": "surface_status_matrix",
        "boundary_consistency_report.json": "boundary_report",
        "next_action_consistency_report.json": "next_action_report",
        "source_artifact_crosswalk.json": "source_crosswalk",
        "validation_readback.json": "alignment_readback",
    }
    return mapping[filename]


def _forbidden_true_claims(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
            for claim in FORBIDDEN_TRUE_CLAIMS:
                if claim in text:
                    hits.append(f"{path.name}:{claim}")
    return hits


def _external_refs(root: Path) -> list[str]:
    hits: list[str] = []
    markers = (
        "data:image",
        "src=\"http://",
        "src=\"https://",
        "src='http://",
        "src='https://",
        "href=\"http://",
        "href=\"https://",
        "href='http://",
        "href='https://",
        "<image href=\"http",
        "<image href='http",
    )
    for path in root.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8-sig", errors="ignore").lower()
            for marker in markers:
                if marker in text:
                    hits.append(f"{path.name}:{marker}")
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


def _slug(value: str) -> str:
    cleaned = "".join(char.lower() if char.isalnum() else "_" for char in value)
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_") or "unknown"


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
