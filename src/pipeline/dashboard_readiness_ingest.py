"""Read-only dashboard readiness ingest for content-spine pilot packages.

The ingest aggregates existing local artifacts into machine-readable status
JSON and a Markdown preview. It does not fetch sources, launch YMM4, render,
approve rights, or make public/production claims.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIRNAME = "dashboard_readiness_ingest"
DEFAULT_ARTIFACT_ID = "content_spine_dashboard_readiness_ingest_v1"

BLOCKED_PUBLIC_ACTIONS = (
    "YouTube upload/publication/visibility change",
    "OAuth/API keys/payment",
    "rights/legal/public-ready acceptance",
    "live scraping/media download",
    "external image/media download or embedded copyrighted media",
    "YMM4 GUI launch/import/render",
    "cross-repo or destructive git",
)

STATUS_CATEGORIES = (
    "ready",
    "partial",
    "sample_fixture_not_real",
    "draft_offline",
    "blocked_by_real_input",
    "blocked_by_true_gate",
    "deferred",
    "missing",
    "unknown",
)

REQUIRED_DASHBOARD_INGEST_FILES = (
    "dashboard_manifest.json",
    "pipeline_status.json",
    "readiness_summary.json",
    "symbolic_visual_panel.json",
    "capability_glyph_grid.json",
    "dashboard_preview.md",
    "source_artifact_index.json",
    "review_checklist.md",
    "limitations.md",
    "validation_readback.json",
)

REQUIRED_CAPABILITY_IDS = (
    "content_spine_002",
    "ir_bridge_002",
    "transcript_substitution_002",
    "writer_ir",
    "cue_packet",
    "draft_yymm4_csv",
    "real_transcript_input",
    "dashboard_ingest",
    "project_cockpit",
    "project_pipeline_mermaid",
    "yymm4_import_preview",
    "thumbnail_visual_proof",
)


def build_dashboard_readiness_ingest_package(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a read-only dashboard/status ingest package."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)

    repo_root = _find_repo_root(source_root)
    snapshot = _load_snapshot(source_root, repo_root)
    capability_rows = _capability_rows(snapshot, output_root, repo_root)
    source_index = _source_artifact_index(snapshot, repo_root)
    readiness_summary = _readiness_summary_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        snapshot=snapshot,
        capability_rows=capability_rows,
    )
    pipeline_status = _pipeline_status_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        snapshot=snapshot,
        capability_rows=capability_rows,
    )
    symbolic_visual_panel = _symbolic_visual_panel(capability_rows)
    capability_glyph_grid = _capability_glyph_grid(capability_rows)
    manifest = _dashboard_manifest_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        capability_rows=capability_rows,
        readiness_summary=readiness_summary,
    )

    _write_json(output_root / "dashboard_manifest.json", manifest)
    _write_json(output_root / "pipeline_status.json", pipeline_status)
    _write_json(output_root / "readiness_summary.json", readiness_summary)
    _write_json(output_root / "symbolic_visual_panel.json", symbolic_visual_panel)
    _write_json(output_root / "capability_glyph_grid.json", capability_glyph_grid)
    _write_text(output_root / "dashboard_preview.md", _render_dashboard_preview(readiness_summary, capability_rows))
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_text(output_root / "review_checklist.md", _render_review_checklist(readiness_summary, capability_rows))
    _write_text(output_root / "limitations.md", _render_limitations(readiness_summary))

    readback = validate_dashboard_readiness_ingest_package(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_dashboard_readiness_ingest_package(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_dashboard_readiness_ingest_package(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate generated dashboard readiness ingest files and boundaries."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_DASHBOARD_INGEST_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["dashboard_manifest.json"])
    pipeline = _load_json_if_present(files["pipeline_status.json"])
    summary = _load_json_if_present(files["readiness_summary.json"])
    panel = _load_json_if_present(files["symbolic_visual_panel.json"])
    glyph_grid = _load_json_if_present(files["capability_glyph_grid.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])

    json_payloads = {
        "dashboard_manifest": manifest,
        "pipeline_status": pipeline,
        "readiness_summary": summary,
        "symbolic_visual_panel": panel,
        "capability_glyph_grid": glyph_grid,
        "source_artifact_index": source_index,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["dashboard_manifest"]
    pipeline = json_payloads["pipeline_status"]
    summary = json_payloads["readiness_summary"]
    panel = json_payloads["symbolic_visual_panel"]
    glyph_grid = json_payloads["capability_glyph_grid"]
    source_index = json_payloads["source_artifact_index"]

    rows = glyph_grid.get("rows", [])
    capability_ids = {row.get("capability_id") for row in rows if isinstance(row, dict)}
    missing_capabilities = [capability for capability in REQUIRED_CAPABILITY_IDS if capability not in capability_ids]
    failed_checks.extend(f"missing_capability:{capability}" for capability in missing_capabilities)

    invalid_states = [
        row.get("state")
        for row in rows
        if isinstance(row, dict) and row.get("state") not in STATUS_CATEGORIES
    ]
    if invalid_states:
        failed_checks.append("invalid_status_category")

    boundary_status = summary.get("boundary_status", {})
    input_reality = summary.get("input_reality", {})
    transcript_state = _row_state(rows, "transcript_substitution_002")
    if input_reality.get("sample_fixture_used") is True:
        if boundary_status.get("transcript_status") != "sample_fixture_not_real":
            failed_checks.append("sample_fixture_transcript_status_missing")
        if transcript_state != "sample_fixture_not_real":
            failed_checks.append("sample_fixture_capability_state_missing")

    if boundary_status.get("public_upload_status") != "blocked_by_true_gate":
        failed_checks.append("public_upload_gate_not_closed")
    if boundary_status.get("ymm4_render_status") != "blocked_by_true_gate":
        failed_checks.append("ymm4_render_gate_not_closed")
    if boundary_status.get("yymm4_import_status") != "blocked_by_true_gate":
        failed_checks.append("ymm4_import_gate_not_closed")
    if boundary_status.get("audio_status") not in {"no_audio_generated_or_imported", "blocked_by_true_gate", "unknown"}:
        failed_checks.append("audio_boundary_unexpected")
    if panel.get("bar_mode") != "hypothesis":
        failed_checks.append("symbolic_bar_mode_missing")
    if manifest.get("artifact_kind") != "dashboard-readiness-ingest":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if not source_index.get("artifacts"):
        failed_checks.append("source_artifact_index_empty")

    return {
        "schema_version": "dashboard_readiness_ingest_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
            "required_capabilities_present": not missing_capabilities,
            "status_categories_valid": not invalid_states,
            "sample_fixture_reported_accurately": not any(
                item in failed_checks
                for item in (
                    "sample_fixture_transcript_status_missing",
                    "sample_fixture_capability_state_missing",
                )
            ),
            "public_upload_gate_closed": boundary_status.get("public_upload_status") == "blocked_by_true_gate",
            "ymm4_render_gate_closed": boundary_status.get("ymm4_render_status") == "blocked_by_true_gate",
            "ymm4_import_gate_closed": boundary_status.get("yymm4_import_status") == "blocked_by_true_gate",
            "symbolic_bar_mode_hypothesis": panel.get("bar_mode") == "hypothesis",
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "source_package_dir": manifest.get("source_package_dir"),
        "selected_candidate_id": summary.get("selected_candidate_id") or pipeline.get("selected_candidate_id"),
        "transcript_status": boundary_status.get("transcript_status"),
        "sample_fixture_used": input_reality.get("sample_fixture_used"),
        "capability_count": len(rows) if isinstance(rows, list) else 0,
        "primary_machine_readable": str(root / "readiness_summary.json"),
        "primary_human_review": str(root / "dashboard_preview.md"),
        "next_action": summary.get("next_action"),
    }


def _load_snapshot(source_root: Path, repo_root: Path) -> dict[str, Any]:
    ir_root = source_root / "ir_bridge"
    transcript_root = source_root / "transcript_substitution_readiness"
    cockpit_path = repo_root / "docs" / "PROJECT_COCKPIT.md"
    pipeline_path = repo_root / "docs" / "PROJECT_PIPELINE.mmd"
    files = {
        "content_manifest": source_root / "MANIFEST.json",
        "content_dry_run_manifest": source_root / "content_spine_dry_run_manifest.json",
        "content_dashboard": source_root / "dashboard_status.json",
        "content_readback": source_root / "content_spine_readback.json",
        "content_source_seed_reference": source_root / "source_seed_reference.json",
        "content_source_artifact_index": source_root / "source_artifact_index.json",
        "ir_manifest": ir_root / "bridge_manifest.json",
        "ir_episode_bridge": ir_root / "episode_bridge.json",
        "ir_writer_ir": ir_root / "writer_ir_candidate.json",
        "ir_cue_packet": ir_root / "cue_packet_candidate.json",
        "ir_draft_csv": ir_root / "draft_yymm4.csv",
        "ir_readback": ir_root / "validation_readback.json",
        "transcript_manifest": transcript_root / "substitution_manifest.json",
        "transcript_probe": transcript_root / "transcript_source_probe.json",
        "transcript_episode_bridge": transcript_root / "regenerated_episode_bridge.json",
        "transcript_writer_ir": transcript_root / "regenerated_writer_ir_candidate.json",
        "transcript_cue_packet": transcript_root / "regenerated_cue_packet_candidate.json",
        "transcript_draft_csv": transcript_root / "regenerated_draft_yymm4.csv",
        "transcript_readback": transcript_root / "validation_readback.json",
        "project_cockpit": cockpit_path,
        "project_pipeline": pipeline_path,
    }
    payloads = {
        name: _load_json_if_present(path)
        for name, path in files.items()
        if path.suffix.lower() == ".json"
    }
    return {
        "source_root": source_root,
        "repo_root": repo_root,
        "ir_root": ir_root,
        "transcript_root": transcript_root,
        "files": files,
        "payloads": payloads,
    }


def _capability_rows(snapshot: dict[str, Any], output_root: Path, repo_root: Path) -> list[dict[str, Any]]:
    files = snapshot["files"]
    payloads = snapshot["payloads"]
    content_manifest = _payload(payloads, "content_manifest")
    content_dashboard = _payload(payloads, "content_dashboard")
    content_readback = _payload(payloads, "content_readback")
    ir_manifest = _payload(payloads, "ir_manifest")
    ir_readback = _payload(payloads, "ir_readback")
    transcript_manifest = _payload(payloads, "transcript_manifest")
    transcript_probe = _payload(payloads, "transcript_probe")
    transcript_readback = _payload(payloads, "transcript_readback")

    sample_fixture_used = transcript_probe.get("sample_fixture_used") is True
    real_transcript_found = transcript_probe.get("access_reality", {}).get("real_transcript_found_for_current_package") is True

    return [
        _row(
            "content_spine_002",
            "Content spine package",
            "draft_offline" if content_readback.get("status") == "passed" else _missing_or_partial(files["content_manifest"]),
            files["content_manifest"],
            "offline content/package is reviewable; source remains local fixture",
            repo_root,
            review_ready=content_readback.get("status") == "passed",
            source_schema=content_manifest.get("schema_version"),
        ),
        _row(
            "ir_bridge_002",
            "IR/CSV bridge",
            "draft_offline" if ir_readback.get("status") == "passed" else _missing_or_partial(files["ir_manifest"]),
            files["ir_manifest"],
            "draft Writer IR, cue packet, and CSV bridge exist; not production timing",
            repo_root,
            review_ready=ir_readback.get("status") == "passed",
            source_schema=ir_manifest.get("schema_version"),
        ),
        _row(
            "transcript_substitution_002",
            "Transcript substitution readiness",
            "sample_fixture_not_real" if sample_fixture_used else (
                "draft_offline" if transcript_readback.get("status") == "passed" else _missing_or_partial(files["transcript_manifest"])
            ),
            files["transcript_manifest"],
            "sample fixture is used until a real transcript is supplied" if sample_fixture_used else "local transcript input has not been independently accepted",
            repo_root,
            review_ready=transcript_readback.get("status") == "passed",
            source_schema=transcript_manifest.get("schema_version"),
        ),
        _row(
            "writer_ir",
            "Regenerated Writer IR candidate",
            "draft_offline" if files["transcript_writer_ir"].exists() else "missing",
            files["transcript_writer_ir"],
            "candidate only; validate-ir/apply-production inputs are not accepted",
            repo_root,
            review_ready=files["transcript_writer_ir"].exists(),
        ),
        _row(
            "cue_packet",
            "Regenerated cue packet candidate",
            "draft_offline" if files["transcript_cue_packet"].exists() else "missing",
            files["transcript_cue_packet"],
            "candidate not sent to external LLM or production operator",
            repo_root,
            review_ready=files["transcript_cue_packet"].exists(),
        ),
        _row(
            "draft_yymm4_csv",
            "Regenerated draft YMM4 CSV",
            "draft_offline" if files["transcript_draft_csv"].exists() else "missing",
            files["transcript_draft_csv"],
            "CSV preview only; no YMM4 import, VoiceItem timing, or render proof",
            repo_root,
            review_ready=files["transcript_draft_csv"].exists(),
        ),
        _row(
            "real_transcript_input",
            "Real transcript input",
            "ready" if real_transcript_found else "blocked_by_real_input",
            Path(transcript_probe.get("real_input_dropzone") or snapshot["transcript_root"] / "real_input"),
            "drop a real NotebookLM/human-reviewed transcript here for a future replacement slice",
            repo_root,
            review_ready=False,
        ),
        _row(
            "dashboard_ingest",
            "Dashboard readiness ingest",
            "ready",
            output_root,
            "read-only status package generated for local review and later GUI adapter work",
            repo_root,
            review_ready=True,
            source_schema="dashboard_readiness_ingest_manifest.v1",
        ),
        _row(
            "project_cockpit",
            "Project Cockpit",
            "ready" if files["project_cockpit"].exists() else "missing",
            files["project_cockpit"],
            "navigation doc; not a production gate",
            repo_root,
            review_ready=files["project_cockpit"].exists(),
        ),
        _row(
            "project_pipeline_mermaid",
            "Project Pipeline Mermaid",
            "ready" if files["project_pipeline"].exists() else "missing",
            files["project_pipeline"],
            "navigation diagram; dashboard node should be visible",
            repo_root,
            review_ready=files["project_pipeline"].exists(),
        ),
        _row(
            "yymm4_import_preview",
            "YMM4 import preview",
            "deferred",
            snapshot["source_root"] / "yymm4_import_preview",
            "future slice; no YMM4 GUI/import/render in this ingest",
            repo_root,
            review_ready=False,
        ),
        _row(
            "thumbnail_visual_proof",
            "Thumbnail visual proof",
            "deferred",
            snapshot["source_root"] / "thumbnail_visual_proof",
            "future slice; no thumbnail image generation or public-ready proof",
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
    capability_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    payloads = snapshot["payloads"]
    content_dashboard = _payload(payloads, "content_dashboard")
    content_dry_run_manifest = _payload(payloads, "content_dry_run_manifest")
    content_source_seed_reference = _payload(payloads, "content_source_seed_reference")
    ir_episode_bridge = _payload(payloads, "ir_episode_bridge")
    transcript_probe = _payload(payloads, "transcript_probe")
    transcript_episode_bridge = _payload(payloads, "transcript_episode_bridge")
    transcript_boundary = transcript_episode_bridge.get("transcript_substitution", {}).get("transcript_boundary", {})
    source_boundary = transcript_episode_bridge.get("source_boundary") or ir_episode_bridge.get("source_boundary", {})
    readiness = transcript_episode_bridge.get("readiness", {})

    status_groups = {category: [] for category in STATUS_CATEGORIES}
    for row in capability_rows:
        status_groups[row["state"]].append(row["capability_id"])

    return {
        "schema_version": "dashboard_readiness_summary.v1",
        "artifact_id": artifact_id,
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": _first_nonempty(
            transcript_episode_bridge.get("selected_candidate_id"),
            ir_episode_bridge.get("selected_candidate_id"),
            content_dashboard.get("selected_candidate_id"),
        ),
        "status_groups": {key: value for key, value in status_groups.items() if value},
        "ready_for_review": [
            row["capability_id"]
            for row in capability_rows
            if row.get("review_ready") is True
        ],
        "needs_real_transcript_input": [
            row["capability_id"]
            for row in capability_rows
            if row["state"] == "blocked_by_real_input"
        ],
        "blocked_by_true_gate": [
            "rights_status",
            "public_upload_status",
            "yymm4_import_status",
            "yymm4_render_status",
            "production_status",
        ],
        "boundary_flags": {
            "dry_run": True,
            "sample_fixture_not_real": transcript_probe.get("sample_fixture_used") is True,
            "no_real_transcript": transcript_probe.get("access_reality", {}).get(
                "real_transcript_found_for_current_package"
            ) is not True,
            "rights_boundary": True,
            "public_upload_closed": True,
            "yymm4_render_closed": True,
            "no_yymm4_import": True,
        },
        "seed_origin": {
            "content_spine_artifact_id": _first_nonempty(
                content_dry_run_manifest.get("artifact_id"),
                content_source_seed_reference.get("artifact_id"),
            ),
            "source_seed_package_dir": content_source_seed_reference.get("source_seed_package_dir"),
            "source_seed_package_present": _repo_path_exists(
                content_source_seed_reference.get("source_seed_package_dir"),
                snapshot["repo_root"],
            ),
            "derived_from_seed_instantiation_artifact_id": content_source_seed_reference.get(
                "derived_from_seed_instantiation_artifact_id"
            ),
            "manual_copy_of_original_pilot": content_source_seed_reference.get("manual_copy_of_original_pilot"),
            "inherited_template_defaults_present": bool(content_source_seed_reference.get("inherited_template_defaults")),
            "required_real_inputs_present": bool(content_source_seed_reference.get("required_real_inputs")),
        },
        "input_reality": {
            "source_fixture_status": source_boundary.get("freshness_status", "unknown"),
            "source_rights_status": source_boundary.get("rights_status", "unknown"),
            "sample_fixture_used": transcript_probe.get("sample_fixture_used"),
            "real_transcript_found_for_current_package": transcript_probe.get("access_reality", {}).get(
                "real_transcript_found_for_current_package"
            ),
            "selected_transcript_path": transcript_probe.get("selected_transcript_path"),
        },
        "boundary_status": {
            "source_status": source_boundary.get("freshness_status", "unknown"),
            "transcript_status": transcript_probe.get("transcript_status", "unknown"),
            "timing_status": transcript_probe.get("timing_status") or readiness.get("timing_status", "unknown"),
            "audio_status": transcript_probe.get("audio_status") or readiness.get("audio_status", "unknown"),
            "rights_status": transcript_boundary.get("rights_status")
            or source_boundary.get("rights_status", "unknown"),
            "production_status": readiness.get("production_status", "unknown"),
            "public_upload_status": "blocked_by_true_gate",
            "yymm4_import_status": "blocked_by_true_gate",
            "ymm4_render_status": "blocked_by_true_gate",
        },
        "capability_rows": capability_rows,
        "next_action": (
            "Review dashboard_preview.md and readiness_summary.json, then supply a verified local real "
            "transcript in the real_input drop-zone for a future replacement slice before YMM4 import preview work."
        ),
    }


def _pipeline_status_payload(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    snapshot: dict[str, Any],
    capability_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    payloads = snapshot["payloads"]
    transcript_probe = _payload(payloads, "transcript_probe")
    transcript_episode_bridge = _payload(payloads, "transcript_episode_bridge")
    return {
        "schema_version": "dashboard_pipeline_status.v1",
        "artifact_id": artifact_id,
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": transcript_episode_bridge.get("selected_candidate_id"),
        "route": [
            {"node": "offline_topic_candidates", "state": "draft_offline"},
            {"node": "content_spine_002", "state": _state_for(capability_rows, "content_spine_002")},
            {"node": "ir_bridge_002", "state": _state_for(capability_rows, "ir_bridge_002")},
            {"node": "transcript_substitution_002", "state": _state_for(capability_rows, "transcript_substitution_002")},
            {"node": "dashboard_readiness_ingest", "state": "ready"},
            {"node": "real_transcript_rerun", "state": _state_for(capability_rows, "real_transcript_input")},
            {"node": "yymm4_import_preview", "state": "deferred"},
            {"node": "thumbnail_visual_proof", "state": "deferred"},
        ],
        "transcript_probe": {
            "source_mode": transcript_probe.get("source_mode"),
            "transcript_status": transcript_probe.get("transcript_status"),
            "sample_fixture_used": transcript_probe.get("sample_fixture_used"),
        },
        "closed_gates": list(BLOCKED_PUBLIC_ACTIONS),
        "roadmap_delta": {
            "previous_t_plus_1": "transcript_substitution_readiness",
            "completed_current": "dashboard_readiness_ingest",
            "new_t_plus_1_proposal": "real_transcript_rerun",
            "reordered_or_deferred": [
                "YMM4 import preview remains after real transcript review",
                "thumbnail visual proof remains after source/rights and visual direction review",
            ],
            "reason": "dashboard ingest makes current pilot state readable before crossing real-input and YMM4 gates",
        },
    }


def _symbolic_visual_panel(capability_rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "symbolic_visual_panel.v1",
        "bar_mode": "hypothesis",
        "measured_progress": False,
        "bars": [
            _bar("content_spine_002", "Content spine 002", _state_for(capability_rows, "content_spine_002"), 5),
            _bar("ir_bridge_002", "IR/CSV bridge 002", _state_for(capability_rows, "ir_bridge_002"), 5),
            _bar(
                "transcript_substitution_002",
                "Transcript substitution 002",
                _state_for(capability_rows, "transcript_substitution_002"),
                4,
            ),
            _bar("dashboard_ingest", "Dashboard ingest", "ready", 6),
            _bar("real_transcript_input", "Real transcript", _state_for(capability_rows, "real_transcript_input"), 1),
            _bar("yymm4_import_preview", "YMM4 import preview", "deferred", 0),
            _bar("thumbnail_visual_proof", "Thumbnail proof", "deferred", 0),
        ],
        "legend": {
            "[#######]": "complete is not claimed; full bars are not used in this ingest",
            "ready": "present and locally reviewable",
            "draft_offline": "present but sample/draft/offline",
            "sample_fixture_not_real": "sample substitute, not real transcript input",
            "blocked_by_real_input": "waiting for real transcript/material input",
            "deferred": "future slice, intentionally not run here",
        },
    }


def _capability_glyph_grid(capability_rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "capability_glyph_grid.v1",
        "legend": {
            "[OK]": "ready",
            "[DRAFT]": "draft_offline",
            "[SAMPLE]": "sample_fixture_not_real",
            "[INPUT]": "blocked_by_real_input",
            "[GATE]": "blocked_by_true_gate",
            "[WAIT]": "deferred",
            "[MISS]": "missing",
            "[PART]": "partial",
            "[UNK]": "unknown",
        },
        "rows": [
            {
                "glyph": _glyph(row["state"]),
                **row,
            }
            for row in capability_rows
        ],
    }


def _source_artifact_index(snapshot: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    artifacts = []
    payloads = snapshot["payloads"]
    for key, path in snapshot["files"].items():
        state = "ready" if path.exists() else "missing"
        schema = None
        if key in payloads and isinstance(payloads[key], dict):
            schema = payloads[key].get("schema_version")
        artifacts.append({
            "id": key,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": state,
            "schema_version": schema,
        })
    return {
        "schema_version": "dashboard_source_artifact_index.v1",
        "artifacts": artifacts,
        "artifact_counts": {
            "total": len(artifacts),
            "present": sum(1 for artifact in artifacts if artifact["exists"]),
            "missing": sum(1 for artifact in artifacts if not artifact["exists"]),
        },
    }


def _dashboard_manifest_payload(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    capability_rows: list[dict[str, Any]],
    readiness_summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "dashboard_readiness_ingest_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "dashboard-readiness-ingest",
        "status": "generated",
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": readiness_summary.get("selected_candidate_id"),
        "files": {name: str(output_root / name) for name in REQUIRED_DASHBOARD_INGEST_FILES},
        "capability_ids": [row["capability_id"] for row in capability_rows],
        "readiness_counts": {
            category: sum(1 for row in capability_rows if row["state"] == category)
            for category in STATUS_CATEGORIES
        },
        "boundaries": {
            "read_only_ingest": True,
            "local_offline_review_only": True,
            "no_live_fetch": True,
            "no_media_download": True,
            "no_external_image_or_media_download": True,
            "no_youtube_publication": True,
            "no_oauth_or_paid_api": True,
            "no_rights_or_legal_acceptance": True,
            "no_ymm4_gui_launch_import_or_render": True,
            "no_yymm4_import": True,
            "no_production_ymmp_generation": True,
            "no_audio_generation": True,
            "dry_run": True,
            "sample_fixture_not_real": readiness_summary.get("input_reality", {}).get("sample_fixture_used") is True,
            "no_real_transcript": readiness_summary.get("input_reality", {}).get(
                "real_transcript_found_for_current_package"
            ) is not True,
            "public_upload_closed": True,
            "yymm4_render_closed": True,
        },
    }


def _render_dashboard_preview(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Dashboard Readiness Ingest Preview",
        "",
        f"- artifact_id: {summary['artifact_id']}",
        f"- selected_candidate_id: {summary.get('selected_candidate_id')}",
        f"- transcript_status: {summary['boundary_status']['transcript_status']}",
        f"- next_action: {summary['next_action']}",
        "",
        "## Capability Grid",
        "",
        "| capability | state | review_ready | path | note |",
        "|---|---|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['capability_id']} | {row['state']} | {str(row['review_ready']).lower()} | "
            f"`{row['repo_relative_path']}` | {row['note']} |"
        )

    lines.extend([
        "",
        "## Boundary Status",
        "",
        "| boundary | status |",
        "|---|---|",
    ])
    for key, value in summary["boundary_status"].items():
        lines.append(f"| {key} | {value} |")

    lines.extend([
        "",
        "## Ready For Review",
        "",
    ])
    for capability in summary["ready_for_review"]:
        lines.append(f"- {capability}")
    lines.extend([
        "",
        "## Needs Real Input",
        "",
    ])
    for capability in summary["needs_real_transcript_input"]:
        lines.append(f"- {capability}")
    lines.append("")
    return "\n".join(lines)


def _render_review_checklist(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    reviewable = [row for row in rows if row.get("review_ready") is True]
    lines = [
        "# Dashboard Readiness Review Checklist",
        "",
        "## Check Now",
        "",
        "- Confirm the dashboard preview matches the current pilot package.",
        "- Confirm sample_fixture_not_real is visible before any transcript rerun.",
        "- Confirm draft_yymm4_csv is treated as a preview, not YMM4 import proof.",
        "- Confirm no rights, legal, public-ready, render, upload, or payment gate is crossed.",
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
        summary["next_action"],
        "",
    ])
    return "\n".join(lines)


def _render_limitations(summary: dict[str, Any]) -> str:
    lines = [
        "# Dashboard Readiness Ingest Limitations",
        "",
        "This package is a read-only local status ingest. It summarizes existing artifacts and gate state.",
        "",
        "Not performed:",
        "",
    ]
    for item in BLOCKED_PUBLIC_ACTIONS:
        lines.append(f"- {item}")
    lines.extend([
        "- production .ymmp generation",
        "- YMM4 CSV import or VoiceItem timing readback",
        "- final transcript, rights, legal, or public-ready acceptance",
        "- thumbnail image generation or visual proof",
        "",
        f"Current transcript_status: `{summary['boundary_status']['transcript_status']}`",
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
    source_schema: str | None = None,
) -> dict[str, Any]:
    return {
        "capability_id": capability_id,
        "label": label,
        "state": state if state in STATUS_CATEGORIES else "unknown",
        "review_ready": review_ready,
        "repo_relative_path": _relpath(path, repo_root),
        "exists": path.exists(),
        "source_schema": source_schema,
        "note": note,
    }


def _bar(capability_id: str, label: str, state: str, filled: int) -> dict[str, Any]:
    max_units = 7
    clamped = max(0, min(max_units, filled))
    return {
        "capability_id": capability_id,
        "label": label,
        "state": state,
        "done_units": clamped,
        "total_units": max_units,
        "bar": "[" + ("#" * clamped) + ("-" * (max_units - clamped)) + "]",
    }


def _glyph(state: str) -> str:
    return {
        "ready": "[OK]",
        "draft_offline": "[DRAFT]",
        "sample_fixture_not_real": "[SAMPLE]",
        "blocked_by_real_input": "[INPUT]",
        "blocked_by_true_gate": "[GATE]",
        "deferred": "[WAIT]",
        "missing": "[MISS]",
        "partial": "[PART]",
        "unknown": "[UNK]",
    }.get(state, "[UNK]")


def _missing_or_partial(path: Path) -> str:
    return "partial" if path.exists() else "missing"


def _payload(payloads: dict[str, Any], key: str) -> dict[str, Any]:
    payload = payloads.get(key)
    return payload if isinstance(payload, dict) else {}


def _state_for(rows: list[dict[str, Any]], capability_id: str) -> str:
    return _row_state(rows, capability_id) or "unknown"


def _row_state(rows: list[Any], capability_id: str) -> str | None:
    for row in rows:
        if isinstance(row, dict) and row.get("capability_id") == capability_id:
            state = row.get("state")
            return str(state) if state is not None else None
    return None


def _first_nonempty(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", []):
            return value
    return None


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


def _repo_path_exists(raw_path: Any, repo_root: Path) -> bool:
    if not raw_path:
        return False
    candidate = Path(str(raw_path))
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    return candidate.exists()


def _load_json_if_present(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
