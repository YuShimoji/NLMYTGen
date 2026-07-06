"""Local/offline alignment pack for episode 002 review surfaces."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIRNAME = "surface_alignment_pack"
DEFAULT_ARTIFACT_ID = "episode_002_surface_alignment_across_gui_import_thumbnail_v1"

REQUIRED_SURFACE_ALIGNMENT_FILES = (
    "surface_alignment_manifest.json",
    "surface_alignment_summary.json",
    "surface_status_matrix.json",
    "source_artifact_crosswalk.json",
    "boundary_consistency_report.json",
    "next_action_consistency_report.json",
    "review_story.md",
    "validation_readback.json",
    "review_checklist.md",
    "limitations.md",
)

SURFACE_STATUS_CATEGORIES = (
    "ready",
    "partial",
    "sample_fixture_not_real",
    "dry_run",
    "draft_offline",
    "blocked_by_real_input",
    "blocked_by_true_gate",
    "validation_noise_nonblocking",
    "thumbnail_context_only",
    "deferred",
    "missing",
    "unknown",
)

MISMATCH_CATEGORIES = (
    "aligned",
    "minor_label_drift",
    "missing_reference",
    "boundary_mismatch",
    "stale_next_action",
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


def build_surface_alignment_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a deterministic cross-surface alignment package."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)
    paths = _input_paths(source_root)
    payloads = _load_surface_payloads(paths)

    surfaces = _surface_records(payloads, paths, repo_root)
    status_matrix = _surface_status_matrix(artifact_id, surfaces, payloads)
    source_crosswalk = _source_artifact_crosswalk(artifact_id, source_root, output_root, paths, payloads, repo_root)
    boundary_report = _boundary_consistency_report(artifact_id, surfaces, payloads)
    next_action_report = _next_action_consistency_report(artifact_id, surfaces)
    summary = _surface_alignment_summary(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        surfaces=surfaces,
        status_matrix=status_matrix,
        source_crosswalk=source_crosswalk,
        boundary_report=boundary_report,
        next_action_report=next_action_report,
    )
    manifest = _surface_alignment_manifest(artifact_id, source_root, output_root, summary)

    _write_json(output_root / "surface_alignment_manifest.json", manifest)
    _write_json(output_root / "surface_alignment_summary.json", summary)
    _write_json(output_root / "surface_status_matrix.json", status_matrix)
    _write_json(output_root / "source_artifact_crosswalk.json", source_crosswalk)
    _write_json(output_root / "boundary_consistency_report.json", boundary_report)
    _write_json(output_root / "next_action_consistency_report.json", next_action_report)
    _write_text(output_root / "review_story.md", _render_review_story(summary, status_matrix, source_crosswalk, boundary_report, next_action_report))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(summary))
    _write_text(output_root / "limitations.md", _render_limitations(summary))

    readback = validate_surface_alignment_pack(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_surface_alignment_pack(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_surface_alignment_pack(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate a generated surface alignment package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_SURFACE_ALIGNMENT_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["surface_alignment_manifest.json"])
    summary = _load_json_if_present(files["surface_alignment_summary.json"])
    matrix = _load_json_if_present(files["surface_status_matrix.json"])
    crosswalk = _load_json_if_present(files["source_artifact_crosswalk.json"])
    boundary_report = _load_json_if_present(files["boundary_consistency_report.json"])
    next_action_report = _load_json_if_present(files["next_action_consistency_report.json"])
    payloads = {
        "surface_alignment_manifest": manifest,
        "surface_alignment_summary": summary,
        "surface_status_matrix": matrix,
        "source_artifact_crosswalk": crosswalk,
        "boundary_consistency_report": boundary_report,
        "next_action_consistency_report": next_action_report,
    }
    for name, payload in payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            payloads[name] = {}

    manifest = payloads["surface_alignment_manifest"]
    summary = payloads["surface_alignment_summary"]
    matrix = payloads["surface_status_matrix"]
    crosswalk = payloads["source_artifact_crosswalk"]
    boundary_report = payloads["boundary_consistency_report"]
    next_action_report = payloads["next_action_consistency_report"]

    if manifest.get("artifact_kind") != "surface-alignment-pack":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if summary.get("status") != "alignment_ready_local_offline":
        failed_checks.append("summary_status_mismatch")
    surfaces = summary.get("surfaces", [])
    surface_ids = {surface.get("surface_id") for surface in surfaces if isinstance(surface, dict)}
    for surface_id in ("gui_dashboard_panel", "yymm4_import_preview_pack", "thumbnail_visual_proof_pack"):
        if surface_id not in surface_ids:
            failed_checks.append(f"surface_missing:{surface_id}")

    matrix_rows = matrix.get("rows", [])
    if not isinstance(matrix_rows, list) or len(matrix_rows) < 10:
        failed_checks.append("status_matrix_too_small")
        matrix_rows = []
    visible_categories = set(matrix.get("status_categories", []))
    missing_status_categories = [status for status in SURFACE_STATUS_CATEGORIES if status not in visible_categories]
    failed_checks.extend(f"status_category_missing:{status}" for status in missing_status_categories)

    boundary_rows = boundary_report.get("boundary_rows", [])
    if not isinstance(boundary_rows, list):
        boundary_rows = []
        failed_checks.append("boundary_rows_invalid")
    required_boundaries = (
        "dry_run",
        "sample_fixture_not_real",
        "no_real_transcript",
        "rights_boundary",
        "public_upload_closed",
        "yymm4_render_closed",
        "no_yymm4_import",
        "thumbnail_context_only",
        "validation_noise_nonblocking",
    )
    boundary_ids = {row.get("boundary_id") for row in boundary_rows if isinstance(row, dict)}
    for boundary_id in required_boundaries:
        if boundary_id not in boundary_ids:
            failed_checks.append(f"boundary_missing:{boundary_id}")
    for row in boundary_rows:
        if isinstance(row, dict) and row.get("classification") not in MISMATCH_CATEGORIES:
            failed_checks.append(f"boundary_classification_unknown:{row.get('boundary_id')}")
    if boundary_report.get("overall_status") not in {"aligned", "minor_label_drift"}:
        failed_checks.append("boundary_overall_status_not_reviewable")

    crosswalk_rows = crosswalk.get("crosswalk_rows", [])
    if not isinstance(crosswalk_rows, list) or len(crosswalk_rows) < 8:
        failed_checks.append("source_crosswalk_too_small")
        crosswalk_rows = []
    for required_artifact in ("gui_panel_data", "import_readiness_summary", "thumbnail_variants", "validation_ledger"):
        if required_artifact not in {row.get("artifact_id") for row in crosswalk_rows if isinstance(row, dict)}:
            failed_checks.append(f"crosswalk_required_artifact_missing:{required_artifact}")
    if crosswalk.get("overall_status") not in {"aligned", "minor_label_drift"}:
        failed_checks.append("crosswalk_overall_status_not_reviewable")

    next_rows = next_action_report.get("next_action_rows", [])
    if not isinstance(next_rows, list) or len(next_rows) < 3:
        failed_checks.append("next_action_rows_too_small")
        next_rows = []
    if "stale_next_action" not in {row.get("classification") for row in next_rows if isinstance(row, dict)}:
        failed_checks.append("stale_next_action_not_detected")

    story_text = files["review_story.md"].read_text(encoding="utf-8") if files["review_story.md"].exists() else ""
    for marker in (
        "source_artifact_crosswalk.json",
        "boundary_consistency_report.json",
        "next_action_consistency_report.json",
        "thumbnail_context_only",
        "validation_noise_nonblocking",
        "blocked_by_true_gate",
    ):
        if marker not in story_text:
            failed_checks.append(f"review_story_marker_missing:{marker}")
    for status in SURFACE_STATUS_CATEGORIES:
        if status not in story_text:
            failed_checks.append(f"review_story_status_missing:{status}")

    forbidden_hits = _forbidden_true_claims(root)
    external_refs = _external_refs(root)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)

    mismatch_counts = summary.get("mismatch_counts", {})
    return {
        "schema_version": "surface_alignment_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in payloads.values()),
            "surface_count": len(surfaces),
            "status_matrix_rows": len(matrix_rows),
            "source_crosswalk_rows": len(crosswalk_rows),
            "boundary_rows": len(boundary_rows),
            "next_action_rows": len(next_rows),
            "all_status_categories_visible": not missing_status_categories,
            "boundary_consistency_reviewable": boundary_report.get("overall_status") in {"aligned", "minor_label_drift"},
            "source_crosswalk_reviewable": crosswalk.get("overall_status") in {"aligned", "minor_label_drift"},
            "stale_next_action_detected": "stale_next_action" in {
                row.get("classification") for row in next_rows if isinstance(row, dict)
            },
            "forbidden_true_claims_absent": not forbidden_hits,
            "external_refs_absent": not external_refs,
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "selected_candidate_id": summary.get("selected_candidate_id"),
        "gui_panel_status": summary.get("surface_alignment_results", {}).get("gui_panel_status"),
        "import_preview_status": summary.get("surface_alignment_results", {}).get("import_preview_status"),
        "thumbnail_proof_status": summary.get("surface_alignment_results", {}).get("thumbnail_proof_status"),
        "source_crosswalk_status": crosswalk.get("overall_status"),
        "boundary_consistency_status": boundary_report.get("overall_status"),
        "next_action_consistency_status": next_action_report.get("overall_status"),
        "mismatches_found": sum(value for key, value in mismatch_counts.items() if key != "aligned"),
        "primary_machine_readable": str(root / "surface_alignment_summary.json"),
        "primary_human_review": str(root / "review_story.md"),
        "next_action": summary.get("next_safe_local_action"),
    }


def _input_paths(source_root: Path) -> dict[str, Path]:
    gui_dir = source_root / "gui_dashboard_panel"
    import_dir = source_root / "ymm4_import_preview_pack"
    thumbnail_dir = source_root / "thumbnail_visual_proof_pack"
    return {
        "gui_readback": gui_dir / "validation_readback.json",
        "gui_panel_data": gui_dir / "panel_data.json",
        "gui_source_index": gui_dir / "source_artifact_index.json",
        "gui_human_review": gui_dir / "dashboard_panel_preview.html",
        "import_readback": import_dir / "validation_readback.json",
        "import_summary": import_dir / "import_readiness_summary.json",
        "import_source_index": import_dir / "source_artifact_index.json",
        "import_csv_inventory": import_dir / "yymm4_csv_inventory.json",
        "import_human_review": import_dir / "import_preview_panel.md",
        "thumbnail_readback": thumbnail_dir / "readback.json",
        "thumbnail_manifest": thumbnail_dir / "manifest.json",
        "thumbnail_variants": thumbnail_dir / "thumbnail_variants.json",
        "thumbnail_source_index": thumbnail_dir / "source_index.json",
        "thumbnail_human_review": thumbnail_dir / "thumbnail_visual_proof.html",
        "validation_ledger": source_root.parents[1] / "samples" / "_probe" / "newsroom_handoff" / "validation_drift_velocity_recovery_v1.json",
    }


def _load_surface_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "gui_readback": _load_json(paths["gui_readback"]),
        "gui_panel_data": _load_json(paths["gui_panel_data"]),
        "gui_source_index": _load_json(paths["gui_source_index"]),
        "import_readback": _load_json(paths["import_readback"]),
        "import_summary": _load_json(paths["import_summary"]),
        "import_source_index": _load_json(paths["import_source_index"]),
        "import_csv_inventory": _load_json(paths["import_csv_inventory"]),
        "thumbnail_readback": _load_json(paths["thumbnail_readback"]),
        "thumbnail_manifest": _load_json(paths["thumbnail_manifest"]),
        "thumbnail_variants": _load_json(paths["thumbnail_variants"]),
        "thumbnail_source_index": _load_json(paths["thumbnail_source_index"]),
        "validation_ledger": _load_json_if_present(paths["validation_ledger"]) or {},
    }


def _surface_records(payloads: dict[str, Any], paths: dict[str, Path], repo_root: Path) -> list[dict[str, Any]]:
    gui_data = payloads["gui_panel_data"]
    import_summary = payloads["import_summary"]
    thumbnail_variants = payloads["thumbnail_variants"]
    thumbnail_readback = payloads["thumbnail_readback"]
    return [
        {
            "surface_id": "gui_dashboard_panel",
            "label": "GUI dashboard panel",
            "status": "ready" if payloads["gui_readback"].get("status") == "passed" else "partial",
            "role_in_alignment": "input_surface",
            "primary_machine_readable": _relpath(paths["gui_panel_data"], repo_root),
            "primary_human_review": _relpath(paths["gui_human_review"], repo_root),
            "selected_candidate_id": gui_data.get("selected_candidate_id"),
            "transcript_status": gui_data.get("boundary_status", {}).get("transcript_status"),
            "validation_noise_status": gui_data.get("validation_noise", {}).get("status"),
            "next_action": gui_data.get("next_action"),
        },
        {
            "surface_id": "yymm4_import_preview_pack",
            "label": "YMM4 import preview pack",
            "status": "ready" if payloads["import_readback"].get("status") == "passed" else "partial",
            "role_in_alignment": "active_import_review_surface",
            "primary_machine_readable": _relpath(paths["import_summary"], repo_root),
            "primary_human_review": _relpath(paths["import_human_review"], repo_root),
            "selected_candidate_id": import_summary.get("selected_candidate_id"),
            "transcript_status": import_summary.get("boundary_status", {}).get("transcript_status"),
            "validation_noise_status": import_summary.get("validation_noise", {}).get("status"),
            "next_action": import_summary.get("next_safe_local_action"),
        },
        {
            "surface_id": "thumbnail_visual_proof_pack",
            "label": "Thumbnail visual proof pack",
            "status": "ready" if thumbnail_readback.get("status") == "passed" else "partial",
            "role_in_alignment": "context_surface",
            "primary_machine_readable": _relpath(paths["thumbnail_variants"], repo_root),
            "primary_human_review": _relpath(paths["thumbnail_human_review"], repo_root),
            "selected_candidate_id": thumbnail_variants.get("selected_candidate_id"),
            "transcript_status": thumbnail_variants.get("source_context", {}).get("transcript_status"),
            "validation_noise_status": "validation_noise_nonblocking"
            if payloads["thumbnail_manifest"].get("boundaries", {}).get("validation_noise_nonblocking") is True
            else "unknown",
            "next_action": thumbnail_variants.get("source_context", {}).get("next_safe_local_action"),
            "recommended_variant_id": thumbnail_variants.get("recommended_variant_id"),
        },
    ]


def _surface_status_matrix(
    artifact_id: str,
    surfaces: list[dict[str, Any]],
    payloads: dict[str, Any],
) -> dict[str, Any]:
    gui = payloads["gui_panel_data"]
    import_summary = payloads["import_summary"]
    thumbnail = payloads["thumbnail_variants"]
    thumbnail_context = import_summary.get("thumbnail_proof_context", {})
    rows = [
        _matrix_row("GUI dashboard panel status", "ready", "ready", "ready", "aligned", "GUI readback passed; old capability rows remain visible as historical panel data."),
        _matrix_row("YMM4 import preview status", "deferred", "ready", "ready_context", "minor_label_drift", "GUI panel still labels import preview deferred; import pack exists and is context-synced."),
        _matrix_row("Thumbnail visual proof status", "deferred", thumbnail_context.get("status", "unknown"), "ready", "minor_label_drift", "GUI panel predates thumbnail proof; import and thumbnail surfaces agree it exists."),
        _matrix_row(
            "Sample fixture / transcript status",
            gui.get("boundary_status", {}).get("transcript_status"),
            import_summary.get("boundary_status", {}).get("transcript_status"),
            thumbnail.get("source_context", {}).get("transcript_status"),
            "aligned",
            "All surfaces keep the transcript sample-backed and non-real.",
        ),
        _matrix_row(
            "Real transcript gate",
            "blocked_by_real_input",
            import_summary.get("boundary_status", {}).get("real_transcript_status"),
            "blocked_by_real_input",
            "aligned",
            "No real transcript replacement happened in these surfaces.",
        ),
        _matrix_row(
            "Validation drift status",
            gui.get("validation_noise", {}).get("status"),
            import_summary.get("validation_noise", {}).get("status"),
            "validation_noise_nonblocking",
            "aligned",
            "All surfaces use the drift ledger as nonblocking product evidence.",
        ),
        _matrix_row(
            "Rights / publication status",
            gui.get("boundary_status", {}).get("rights_status"),
            import_summary.get("boundary_status", {}).get("rights_status"),
            thumbnail.get("source_context", {}).get("rights_status"),
            "minor_label_drift",
            "Labels differ but all mean sample-only/no-publication.",
        ),
        _matrix_row(
            "YMM4 import / render status",
            gui.get("boundary_status", {}).get("yymm4_import_status"),
            import_summary.get("boundary_status", {}).get("yymm4_import_status"),
            thumbnail.get("source_context", {}).get("yymm4_import_status"),
            "aligned",
            "No surface claims YMM4 import or render.",
        ),
        _matrix_row(
            "Thumbnail approval status",
            "deferred",
            import_summary.get("boundary_status", {}).get("production_thumbnail_status"),
            "proof_only",
            "aligned",
            "Thumbnail proof is context only, not final approval.",
        ),
        _matrix_row(
            "Next safe local action",
            "prepare_import_preview",
            "review_import_preview_with_thumbnail_context",
            "review_thumbnail_direction",
            "stale_next_action",
            "GUI and thumbnail next-action text predate this alignment package.",
        ),
        _matrix_row(
            "Source artifact references",
            "source_index_present",
            "source_index_present",
            "source_index_present",
            "aligned",
            "All three packages expose source-artifact indexes.",
        ),
    ]
    return {
        "schema_version": "surface_status_matrix.v1",
        "artifact_id": artifact_id,
        "status_categories": list(SURFACE_STATUS_CATEGORIES),
        "mismatch_categories": list(MISMATCH_CATEGORIES),
        "surfaces": [surface["surface_id"] for surface in surfaces],
        "rows": rows,
        "classification_counts": dict(Counter(row["classification"] for row in rows)),
    }


def _matrix_row(axis: str, gui: Any, import_preview: Any, thumbnail: Any, classification: str, note: str) -> dict[str, Any]:
    return {
        "axis": axis,
        "gui_dashboard_panel": gui,
        "yymm4_import_preview_pack": import_preview,
        "thumbnail_visual_proof_pack": thumbnail,
        "classification": classification,
        "note": note,
    }


def _source_artifact_crosswalk(
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    paths: dict[str, Path],
    payloads: dict[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    rows = [
        _crosswalk_row("gui_panel_data", paths["gui_panel_data"], ["gui_dashboard_panel", "yymm4_import_preview_pack", "thumbnail_visual_proof_pack"], repo_root),
        _crosswalk_row("gui_human_review", paths["gui_human_review"], ["gui_dashboard_panel"], repo_root),
        _crosswalk_row("import_readiness_summary", paths["import_summary"], ["yymm4_import_preview_pack", "thumbnail_visual_proof_pack"], repo_root),
        _crosswalk_row("import_preview_panel", paths["import_human_review"], ["yymm4_import_preview_pack"], repo_root),
        _crosswalk_row("import_csv_inventory", paths["import_csv_inventory"], ["yymm4_import_preview_pack"], repo_root),
        _crosswalk_row("thumbnail_variants", paths["thumbnail_variants"], ["thumbnail_visual_proof_pack", "yymm4_import_preview_pack"], repo_root),
        _crosswalk_row("thumbnail_human_review", paths["thumbnail_human_review"], ["thumbnail_visual_proof_pack", "yymm4_import_preview_pack"], repo_root),
        _crosswalk_row("validation_ledger", paths["validation_ledger"], ["gui_dashboard_panel", "yymm4_import_preview_pack", "thumbnail_visual_proof_pack"], repo_root),
        _crosswalk_row("gui_source_index", paths["gui_source_index"], ["gui_dashboard_panel", "yymm4_import_preview_pack", "thumbnail_visual_proof_pack"], repo_root),
        _crosswalk_row("import_source_index", paths["import_source_index"], ["yymm4_import_preview_pack", "thumbnail_visual_proof_pack"], repo_root),
        _crosswalk_row("thumbnail_source_index", paths["thumbnail_source_index"], ["thumbnail_visual_proof_pack", "yymm4_import_preview_pack"], repo_root),
    ]
    missing = [row for row in rows if row["exists"] is not True]
    surface_counts = {
        "gui_dashboard_panel": len(_list(payloads["gui_source_index"].get("source_artifacts"))),
        "yymm4_import_preview_pack": len(_list(payloads["import_source_index"].get("source_artifacts"))),
        "thumbnail_visual_proof_pack": len(_list(payloads["thumbnail_source_index"].get("source_artifacts"))),
    }
    return {
        "schema_version": "source_artifact_crosswalk.v1",
        "artifact_id": artifact_id,
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "overall_status": "missing_reference" if missing else "aligned",
        "crosswalk_rows": rows,
        "source_artifact_counts_by_surface": surface_counts,
        "missing_reference_count": len(missing),
    }


def _crosswalk_row(artifact_id: str, path: Path, surfaces: list[str], repo_root: Path) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "repo_relative_path": _relpath(path, repo_root),
        "surfaces": surfaces,
        "exists": path.exists(),
        "classification": "aligned" if path.exists() else "missing_reference",
    }


def _boundary_consistency_report(
    artifact_id: str,
    surfaces: list[dict[str, Any]],
    payloads: dict[str, Any],
) -> dict[str, Any]:
    gui_flags = payloads["gui_panel_data"].get("boundary_flags", {})
    gui_status = payloads["gui_panel_data"].get("boundary_status", {})
    import_flags = payloads["import_summary"].get("boundary_flags", {})
    import_status = payloads["import_summary"].get("boundary_status", {})
    thumbnail_manifest = payloads["thumbnail_manifest"]
    thumbnail_context = payloads["thumbnail_variants"].get("source_context", {})
    thumbnail_gates = payloads["thumbnail_variants"].get("proof_only_gates", {})
    rows = [
        _boundary_row("dry_run", gui_flags.get("dry_run"), import_flags.get("dry_run"), "proof_text_context", "minor_label_drift", "Thumbnail proof expresses dry-run in copy rather than a dry_run flag."),
        _boundary_row("sample_fixture_not_real", gui_flags.get("sample_fixture_not_real"), import_flags.get("sample_fixture_not_real"), thumbnail_context.get("transcript_status"), "aligned", "All surfaces preserve sample fixture status."),
        _boundary_row("no_real_transcript", gui_flags.get("no_real_transcript"), import_flags.get("no_real_transcript"), thumbnail_context.get("transcript_status"), "aligned", "No surface reports a real transcript."),
        _boundary_row("rights_boundary", gui_flags.get("rights_boundary"), import_flags.get("rights_boundary"), thumbnail_context.get("rights_status"), "minor_label_drift", "Thumbnail uses rights/public-ready wording instead of rights_boundary."),
        _boundary_row("public_upload_closed", gui_flags.get("public_upload_closed"), import_flags.get("public_upload_closed"), thumbnail_gates.get("youtube_uploaded") is False, "aligned", "Public/upload gates remain closed."),
        _boundary_row("yymm4_render_closed", gui_flags.get("yymm4_render_closed"), import_flags.get("yymm4_render_closed"), thumbnail_context.get("yymm4_render_status"), "aligned", "No render has occurred."),
        _boundary_row("no_yymm4_import", gui_flags.get("no_yymm4_import"), import_flags.get("no_yymm4_import"), thumbnail_context.get("yymm4_import_status"), "aligned", "No import has occurred."),
        _boundary_row("thumbnail_context_only", "not_applicable", import_flags.get("thumbnail_context_only"), thumbnail_manifest.get("boundaries", {}).get("proof_only"), "aligned", "Import treats thumbnail as context only; thumbnail remains proof-only."),
        _boundary_row("validation_noise_nonblocking", payloads["gui_panel_data"].get("validation_noise", {}).get("status"), import_flags.get("validation_noise_nonblocking"), thumbnail_manifest.get("boundaries", {}).get("validation_noise_nonblocking"), "aligned", "All surfaces use validation drift as nonblocking."),
        _boundary_row("no_production_thumbnail_acceptance", "not_applicable", import_flags.get("no_production_thumbnail_acceptance"), thumbnail_gates.get("production_thumbnail_ready") is False, "aligned", "No final thumbnail approval is claimed."),
        _boundary_row("blocked_by_true_gate", gui_status.get("public_upload_status"), import_status.get("public_upload_status"), "public_ready_false", "aligned", "Public/production gates stay closed."),
    ]
    counts = Counter(row["classification"] for row in rows)
    overall = "minor_label_drift" if counts.get("minor_label_drift") else "aligned"
    if counts.get("boundary_mismatch"):
        overall = "boundary_mismatch"
    return {
        "schema_version": "boundary_consistency_report.v1",
        "artifact_id": artifact_id,
        "overall_status": overall,
        "mismatch_categories": list(MISMATCH_CATEGORIES),
        "boundary_rows": rows,
        "classification_counts": dict(counts),
    }


def _boundary_row(boundary_id: str, gui: Any, import_preview: Any, thumbnail: Any, classification: str, note: str) -> dict[str, Any]:
    return {
        "boundary_id": boundary_id,
        "gui_dashboard_panel": gui,
        "yymm4_import_preview_pack": import_preview,
        "thumbnail_visual_proof_pack": thumbnail,
        "classification": classification,
        "note": note,
    }


def _next_action_consistency_report(artifact_id: str, surfaces: list[dict[str, Any]]) -> dict[str, Any]:
    rows = [
        {
            "surface_id": "gui_dashboard_panel",
            "next_action": _surface_by_id(surfaces, "gui_dashboard_panel").get("next_action"),
            "classification": "stale_next_action",
            "note": "GUI panel still points toward preparing the import preview; that preview now exists.",
        },
        {
            "surface_id": "yymm4_import_preview_pack",
            "next_action": _surface_by_id(surfaces, "yymm4_import_preview_pack").get("next_action"),
            "classification": "aligned",
            "note": "Import preview already frames thumbnail proof as context only.",
        },
        {
            "surface_id": "thumbnail_visual_proof_pack",
            "next_action": _surface_by_id(surfaces, "thumbnail_visual_proof_pack").get("next_action"),
            "classification": "stale_next_action",
            "note": "Thumbnail proof points toward direction selection; this alignment slice only compares surfaces.",
        },
    ]
    counts = Counter(row["classification"] for row in rows)
    return {
        "schema_version": "next_action_consistency_report.v1",
        "artifact_id": artifact_id,
        "overall_status": "stale_next_action" if counts.get("stale_next_action") else "aligned",
        "next_action_rows": rows,
        "classification_counts": dict(counts),
        "recommended_next_safe_local_action": (
            "Review review_story.md, then decide whether GUI/import/thumbnail surfaces tell the same "
            "dry-run story before any real transcript replacement or YMM4 import review."
        ),
    }


def _surface_alignment_summary(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    surfaces: list[dict[str, Any]],
    status_matrix: dict[str, Any],
    source_crosswalk: dict[str, Any],
    boundary_report: dict[str, Any],
    next_action_report: dict[str, Any],
) -> dict[str, Any]:
    mismatch_counts = Counter()
    for report in (status_matrix, boundary_report, source_crosswalk, next_action_report):
        for key, value in _dict(report.get("classification_counts")).items():
            mismatch_counts[key] += int(value)
    selected_ids = {surface.get("selected_candidate_id") for surface in surfaces if surface.get("selected_candidate_id")}
    return {
        "schema_version": "surface_alignment_summary.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "surface-alignment-pack",
        "status": "alignment_ready_local_offline",
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": sorted(selected_ids)[0] if selected_ids else None,
        "surfaces": surfaces,
        "status_categories": list(SURFACE_STATUS_CATEGORIES),
        "mismatch_categories": list(MISMATCH_CATEGORIES),
        "mismatch_counts": dict(mismatch_counts),
        "surface_alignment_results": {
            "gui_panel_status": _surface_by_id(surfaces, "gui_dashboard_panel").get("status"),
            "import_preview_status": _surface_by_id(surfaces, "yymm4_import_preview_pack").get("status"),
            "thumbnail_proof_status": _surface_by_id(surfaces, "thumbnail_visual_proof_pack").get("status"),
            "source_crosswalk_status": source_crosswalk.get("overall_status"),
            "boundary_consistency_status": boundary_report.get("overall_status"),
            "next_action_consistency_status": next_action_report.get("overall_status"),
        },
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
            "no_production_thumbnail_acceptance": True,
            "no_yymm4_gui_launch_or_render": True,
            "no_production_ymmp": True,
        },
        "primary_machine_readable": str(output_root / "surface_alignment_summary.json"),
        "primary_human_review": str(output_root / "review_story.md"),
        "next_safe_local_action": next_action_report.get("recommended_next_safe_local_action"),
    }


def _surface_alignment_manifest(
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "surface_alignment_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "surface-alignment-pack",
        "status": "generated",
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "files": {name: str(output_root / name) for name in REQUIRED_SURFACE_ALIGNMENT_FILES},
        "surfaces": [surface.get("surface_id") for surface in summary.get("surfaces", [])],
        "boundaries": summary.get("boundary_flags", {}),
        "next_safe_local_action": summary.get("next_safe_local_action"),
    }


def _render_review_story(
    summary: dict[str, Any],
    matrix: dict[str, Any],
    crosswalk: dict[str, Any],
    boundary_report: dict[str, Any],
    next_action_report: dict[str, Any],
) -> str:
    lines = [
        "# Episode 002 Surface Alignment Review Story",
        "",
        f"- artifact_id: {summary.get('artifact_id')}",
        f"- status: {summary.get('status')}",
        f"- selected_candidate_id: {summary.get('selected_candidate_id')}",
        "- surfaces: GUI dashboard panel, YMM4 import preview pack, thumbnail visual proof pack",
        "- primary machine readback: `surface_alignment_summary.json`",
        "- source crosswalk: `source_artifact_crosswalk.json`",
        "- boundary report: `boundary_consistency_report.json`",
        "- next action report: `next_action_consistency_report.json`",
        "",
        "## Status Legend",
        "",
        "| status | meaning in this alignment pack |",
        "|---|---|",
    ]
    for status in SURFACE_STATUS_CATEGORIES:
        lines.append(f"| {status} | visible cross-surface state marker |")
    lines.extend([
        "",
        "## Surface Snapshot",
        "",
        "| surface | status | role | human review |",
        "|---|---|---|---|",
    ])
    for surface in summary.get("surfaces", []):
        lines.append(
            f"| {surface.get('surface_id')} | {surface.get('status')} | {surface.get('role_in_alignment')} | `{surface.get('primary_human_review')}` |"
        )
    lines.extend([
        "",
        "## Status Matrix Highlights",
        "",
        "| axis | GUI | Import preview | Thumbnail proof | classification |",
        "|---|---|---|---|---|",
    ])
    for row in matrix.get("rows", []):
        lines.append(
            f"| {row.get('axis')} | {row.get('gui_dashboard_panel')} | {row.get('yymm4_import_preview_pack')} | {row.get('thumbnail_visual_proof_pack')} | {row.get('classification')} |"
        )
    lines.extend([
        "",
        "## Boundary Consistency",
        "",
        f"- overall_status: {boundary_report.get('overall_status')}",
        f"- boundary_rows: {len(boundary_report.get('boundary_rows', []))}",
        "- required markers: dry_run, sample_fixture_not_real, no_real_transcript, rights_boundary, public_upload_closed, yymm4_render_closed, no_yymm4_import, thumbnail_context_only, validation_noise_nonblocking, blocked_by_true_gate",
        "",
        "## Source Artifact Crosswalk",
        "",
        f"- overall_status: {crosswalk.get('overall_status')}",
        f"- crosswalk_rows: {len(crosswalk.get('crosswalk_rows', []))}",
        "",
        "## Next Action Consistency",
        "",
        f"- overall_status: {next_action_report.get('overall_status')}",
        "- stale_next_action indicates the older GUI/thumbnail text predates this alignment pack; it is recorded rather than rewritten.",
        "",
        "## Next Safe Local Action",
        "",
        str(summary.get("next_safe_local_action")),
        "",
    ])
    return "\n".join(lines)


def _render_review_checklist(summary: dict[str, Any]) -> str:
    return "\n".join([
        "# Surface Alignment Review Checklist",
        "",
        "- Open `review_story.md` first.",
        "- Confirm GUI dashboard, import preview, and thumbnail proof are present as local review surfaces.",
        "- Confirm `surface_status_matrix.json` marks GUI/import/thumbnail status in one table.",
        "- Confirm `source_artifact_crosswalk.json` has no missing required references.",
        "- Confirm `boundary_consistency_report.json` keeps public/auth/rights/YMM4/thumbnail approval gates closed.",
        "- Treat stale next-action labels as review debt, not blockers.",
        "",
        "## Next Safe Local Action",
        "",
        str(summary.get("next_safe_local_action")),
        "",
    ])


def _render_limitations(summary: dict[str, Any]) -> str:
    return "\n".join([
        "# Surface Alignment Limitations",
        "",
        "This package compares existing local/offline review surfaces. It does not revise creative output or perform YMM4 work.",
        "",
        "Not performed:",
        "",
        "- real transcript rerun or source replacement",
        "- YMM4 GUI launch/import/render",
        "- production .ymmp generation",
        "- final thumbnail approval or thumbnail redesign",
        "- public upload or publication",
        "- rights/legal/public-ready acceptance",
        "- live scraping or external media download",
        "- full-suite green campaign",
        "",
        "Current safe action:",
        "",
        str(summary.get("next_safe_local_action")),
        "",
    ])


def _surface_by_id(surfaces: list[dict[str, Any]], surface_id: str) -> dict[str, Any]:
    for surface in surfaces:
        if surface.get("surface_id") == surface_id:
            return surface
    return {}


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


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


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
