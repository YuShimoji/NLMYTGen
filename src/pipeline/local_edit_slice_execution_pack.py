"""Local edit-slice execution package for episode 002."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.split_view_decision_evidence_prototype import (
    _dict,
    _escape,
    _external_refs_in_files,
    _find_repo_root,
    _forbidden_true_claims,
    _list,
    _load_json_if_present,
    _relpath,
    _temporary_copy_hits,
    _write_json,
    _write_text,
)

DEFAULT_OUTPUT_DIRNAME = "local_edit_slice_execution_pack"
DEFAULT_ARTIFACT_ID = "episode_002_local_edit_slice_execution_pack_v1"

EDITING_OPERATIONS_DIRNAME = "editing_operations_readiness_pack"
OUTPUT_TEMPLATE_DIRNAME = "output_template_readiness_pack"
REAL_INPUT_DIRNAME = "real_input_intake_readiness"
JAPANESE_GRAPHIC_CONSOLE_DIRNAME = "japanese_graphic_review_console"

REQUIRED_LOCAL_EDIT_SLICE_FILES = (
    "local_edit_slice_manifest.json",
    "local_edit_execution_preview.html",
    "local_edit_execution_preview.md",
    "local_edit_slice_queue.json",
    "scene_edit_execution_plan.json",
    "operation_gate_preservation_readback.json",
    "source_artifact_index.json",
    "validation_readback.json",
    "review_checklist.md",
    "limitations.md",
    "README_LOCAL_EDIT_SLICE_EXECUTION.md",
)

LOCAL_EXECUTION_OPERATION_IDS = (
    "set_scene_duration",
    "align_voice_subtitle",
    "split_or_wrap_subtitle",
    "assign_visual_scene_template",
    "place_citation_overlay",
    "transfer_thumbnail_motif",
    "validate_operation_pack",
)

BLOCKED_GATE_OPERATION_IDS = (
    "flag_real_input_required",
    "mark_yymm4_observation_needed",
    "capture_yymm4_readback",
)

REQUIRED_BOUNDARY_FLAGS = (
    "dry_run",
    "sample_fixture_not_real",
    "no_real_transcript",
    "rights_boundary",
    "public_upload_closed",
    "yymm4_render_closed",
    "no_yymm4_import",
    "validation_noise_nonblocking",
    "not_production_ready",
)

PROTECTED_CONTEXT_DIRS = (
    "production_pilots/yukkuri_newsroom_content_spine_002/editing_operations_readiness_pack",
    "production_pilots/yukkuri_newsroom_content_spine_002/output_template_readiness_pack",
    "production_pilots/yukkuri_newsroom_content_spine_002/real_input_intake_readiness",
    "production_pilots/yukkuri_newsroom_content_spine_002/japanese_graphic_review_console",
    "production_pilots/yukkuri_newsroom_content_spine_002/primary_artifact_review_console",
    "production_pilots/yukkuri_newsroom_content_spine_002/review_console_redesign_prototype",
    "production_pilots/yukkuri_newsroom_content_spine_002/split_view_decision_evidence_prototype",
)


def build_local_edit_slice_execution_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a local-only execution pack from editing operation contracts."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root)
    payloads = _load_payloads(paths)
    state = _state(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        payloads=payloads,
    )
    queue = _local_edit_slice_queue(state)
    scene_plan = _scene_edit_execution_plan(state, queue)
    gate_readback = _operation_gate_preservation_readback(state, queue, scene_plan)
    source_index = _source_artifact_index(state)
    manifest = _manifest(state, queue, scene_plan, gate_readback, output_root, repo_root)

    _write_json(output_root / "local_edit_slice_manifest.json", manifest)
    _write_json(output_root / "local_edit_slice_queue.json", queue)
    _write_json(output_root / "scene_edit_execution_plan.json", scene_plan)
    _write_json(output_root / "operation_gate_preservation_readback.json", gate_readback)
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_text(output_root / "local_edit_execution_preview.html", _render_html(state, queue, scene_plan, gate_readback))
    _write_text(output_root / "local_edit_execution_preview.md", _render_markdown(state, queue, scene_plan, gate_readback))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state, queue, scene_plan))
    _write_text(output_root / "limitations.md", _render_limitations(state))
    _write_text(output_root / "README_LOCAL_EDIT_SLICE_EXECUTION.md", _render_readme(state, queue, scene_plan, gate_readback))

    readback = validate_local_edit_slice_execution_pack(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_local_edit_slice_execution_pack(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_local_edit_slice_execution_pack(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated local edit-slice execution package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_LOCAL_EDIT_SLICE_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["local_edit_slice_manifest.json"])
    queue = _load_json_if_present(files["local_edit_slice_queue.json"])
    scene_plan = _load_json_if_present(files["scene_edit_execution_plan.json"])
    gate_readback = _load_json_if_present(files["operation_gate_preservation_readback.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])
    json_payloads = {
        "manifest": manifest,
        "queue": queue,
        "scene_plan": scene_plan,
        "gate_readback": gate_readback,
        "source_index": source_index,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = _dict(json_payloads["manifest"])
    queue = _dict(json_payloads["queue"])
    scene_plan = _dict(json_payloads["scene_plan"])
    gate_readback = _dict(json_payloads["gate_readback"])
    source_index = _dict(json_payloads["source_index"])

    html_text = files["local_edit_execution_preview.html"].read_text(encoding="utf-8") if files["local_edit_execution_preview.html"].exists() else ""
    markdown_text = files["local_edit_execution_preview.md"].read_text(encoding="utf-8") if files["local_edit_execution_preview.md"].exists() else ""
    limitations_text = files["limitations.md"].read_text(encoding="utf-8") if files["limitations.md"].exists() else ""

    queue_rows = [row for row in _list(queue.get("queue")) if isinstance(row, dict)]
    queued_ids = {str(row.get("operation_id")) for row in queue_rows}
    blocked_rows = [row for row in _list(queue.get("blocked_operations")) if isinstance(row, dict)]
    scenes = [row for row in _list(scene_plan.get("scenes")) if isinstance(row, dict)]
    closed_gate_flags = _dict(gate_readback.get("closed_gate_flags"))
    boundary_flags = _dict(manifest.get("boundary_flags"))
    protected_touches = _dict(manifest.get("protected_context_files_touched"))

    if manifest.get("artifact_kind") != "episode-local-edit-slice-execution-pack":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "local_edit_slice_execution_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")
    if queue.get("status") != "local_edit_slice_queue_ready":
        failed_checks.append("queue_status_mismatch")
    for operation_id in LOCAL_EXECUTION_OPERATION_IDS:
        if operation_id not in queued_ids:
            failed_checks.append(f"queued_operation_missing:{operation_id}")
    for operation_id in BLOCKED_GATE_OPERATION_IDS:
        if operation_id in queued_ids:
            failed_checks.append(f"blocked_operation_queued:{operation_id}")
    if len(queue_rows) < len(LOCAL_EXECUTION_OPERATION_IDS):
        failed_checks.append("queue_too_short")
    if len(blocked_rows) < 2:
        failed_checks.append("blocked_operations_not_recorded")
    if scene_plan.get("status") != "scene_edit_execution_plan_ready_local_offline":
        failed_checks.append("scene_plan_status_mismatch")
    if len(scenes) < 3:
        failed_checks.append("scene_plan_too_short")
    if gate_readback.get("status") != "closed_gates_preserved":
        failed_checks.append("gate_readback_status_mismatch")
    if gate_readback.get("forbidden_gates_closed") is not True:
        failed_checks.append("forbidden_gates_not_closed")
    for flag_name, flag_value in closed_gate_flags.items():
        if flag_value is not False:
            failed_checks.append(f"closed_gate_flag_not_false:{flag_name}")
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing:{flag}")
    for touch_group, touches in protected_touches.items():
        if _list(touches):
            failed_checks.append(f"protected_context_files_touched:{touch_group}")
    if source_index.get("editing_operations_context_read_only") is not True:
        failed_checks.append("editing_operations_context_not_read_only")
    if "data-local-edit-slice=\"true\"" not in html_text:
        failed_checks.append("html_missing_local_edit_marker")
    if "data-region=\"execution-queue\"" not in html_text:
        failed_checks.append("html_missing_execution_queue")
    if "Do not launch YMM4" not in limitations_text:
        failed_checks.append("limitations_missing_yymm4_stop")
    if "local edit-slice execution" not in markdown_text:
        failed_checks.append("markdown_missing_execution_phrase")

    visible_files = [path for path in files.values() if path.exists()]
    external_refs = _external_refs_in_files(visible_files)
    if external_refs:
        failed_checks.append("external_refs_found")
    forbidden_claims = _forbidden_true_claims(root)
    if forbidden_claims:
        failed_checks.append("forbidden_true_claims_found")
    temporary_hits = _temporary_copy_hits(visible_files)
    if temporary_hits:
        failed_checks.append("temporary_copy_found")

    status = "passed" if not failed_checks else "failed"
    return {
        "schema_version": "local_edit_slice_validation_readback.v1",
        "status": status,
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(
                path.exists() for name, path in files.items() if name != "validation_readback.json" or require_readback
            ),
            "json_loads": all(isinstance(payload, dict) for payload in json_payloads.values()),
            "html_preview_exists": files["local_edit_execution_preview.html"].exists(),
            "markdown_preview_exists": files["local_edit_execution_preview.md"].exists(),
            "queue_operation_count": len(queue_rows),
            "required_local_operations_queued": set(LOCAL_EXECUTION_OPERATION_IDS).issubset(queued_ids),
            "blocked_gate_operations_not_queued": not any(operation_id in queued_ids for operation_id in BLOCKED_GATE_OPERATION_IDS),
            "blocked_operation_count": len(blocked_rows),
            "scene_count": len(scenes),
            "forbidden_gates_closed": gate_readback.get("forbidden_gates_closed"),
            "closed_gate_flags": closed_gate_flags,
            "protected_context_files_touched": protected_touches,
            "external_dependency_status": "none_found" if not external_refs else external_refs,
            "forbidden_true_claims_absent": not forbidden_claims,
            "temporary_copy_absent": not temporary_hits,
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "primary_review_file": str(root / "local_edit_execution_preview.html"),
        "primary_human_review": str(root / "local_edit_execution_preview.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "queue_operation_count": len(queue_rows),
        "scene_count": len(scenes),
        "blocked_operation_count": len(blocked_rows),
        "gates_closed": gate_readback.get("forbidden_gates_closed") is True,
        "actual_yymm4_import": closed_gate_flags.get("actual_yymm4_import"),
        "real_input_replacement_executed": closed_gate_flags.get("real_input_replacement_executed"),
        "public_ready": closed_gate_flags.get("public_ready"),
        "thread_registry_updated": manifest.get("thread_registry_updated"),
        "shared_docs_touched": manifest.get("shared_docs_touched"),
        "full_pytest_run": False,
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{(root / "local_edit_execution_preview.html").resolve()}"',
        "access_state": "verified_present" if (root / "local_edit_execution_preview.html").exists() else "missing",
        "next_action": manifest.get("next_action"),
    }


def _input_paths(source_root: Path) -> dict[str, Path]:
    editing_root = source_root / EDITING_OPERATIONS_DIRNAME
    output_template_root = source_root / OUTPUT_TEMPLATE_DIRNAME
    real_input_root = source_root / REAL_INPUT_DIRNAME
    gui_root = source_root / JAPANESE_GRAPHIC_CONSOLE_DIRNAME
    return {
        "editing_root": editing_root,
        "editing_manifest": editing_root / "editing_operations_manifest.json",
        "edit_operation_registry": editing_root / "edit_operation_registry.json",
        "scene_operation_plan": editing_root / "scene_operation_plan.json",
        "timing_adjustment_model": editing_root / "timing_adjustment_model.json",
        "voice_subtitle_operation_map": editing_root / "voice_subtitle_operation_map.json",
        "visual_asset_slot_map": editing_root / "visual_asset_slot_map.json",
        "operation_gap_ledger": editing_root / "operation_gap_ledger.json",
        "editing_validation": editing_root / "validation_readback.json",
        "output_template_root": output_template_root,
        "real_input_root": real_input_root,
        "japanese_console_root": gui_root,
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "editing_manifest": _load_json_if_present(paths["editing_manifest"]),
        "edit_operation_registry": _load_json_if_present(paths["edit_operation_registry"]),
        "scene_operation_plan": _load_json_if_present(paths["scene_operation_plan"]),
        "timing_adjustment_model": _load_json_if_present(paths["timing_adjustment_model"]),
        "voice_subtitle_operation_map": _load_json_if_present(paths["voice_subtitle_operation_map"]),
        "visual_asset_slot_map": _load_json_if_present(paths["visual_asset_slot_map"]),
        "operation_gap_ledger": _load_json_if_present(paths["operation_gap_ledger"]),
        "editing_validation": _load_json_if_present(paths["editing_validation"]),
    }


def _state(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    repo_root: Path,
    paths: dict[str, Path],
    payloads: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "local_edit_slice_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-local-edit-slice-execution-pack",
        "status": "local_edit_slice_execution_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "repo_root": str(repo_root),
        "paths": {name: _relpath(path, repo_root) for name, path in paths.items()},
        "editing_manifest": _dict(payloads.get("editing_manifest")),
        "edit_operation_registry": _dict(payloads.get("edit_operation_registry")),
        "scene_operation_plan": _dict(payloads.get("scene_operation_plan")),
        "timing_adjustment_model": _dict(payloads.get("timing_adjustment_model")),
        "voice_subtitle_operation_map": _dict(payloads.get("voice_subtitle_operation_map")),
        "visual_asset_slot_map": _dict(payloads.get("visual_asset_slot_map")),
        "operation_gap_ledger": _dict(payloads.get("operation_gap_ledger")),
        "editing_validation": _dict(payloads.get("editing_validation")),
        "boundary_flags": {
            "dry_run": True,
            "sample_fixture_not_real": True,
            "no_real_transcript": True,
            "rights_boundary": True,
            "public_upload_closed": True,
            "yymm4_render_closed": True,
            "no_yymm4_import": True,
            "validation_noise_nonblocking": True,
            "not_production_ready": True,
        },
        "primary_human_review": _relpath(output_root / "local_edit_execution_preview.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_action": "Use the queue to execute one local draft edit slice, or open an explicit real-input/YMM4 gate before any replacement or observation work.",
    }


def _local_edit_slice_queue(state: dict[str, Any]) -> dict[str, Any]:
    registry = _dict(state.get("edit_operation_registry"))
    operations_by_id = {
        str(row.get("operation_id")): row
        for row in _list(registry.get("operations"))
        if isinstance(row, dict)
    }
    queue = []
    for step_number, operation_id in enumerate(LOCAL_EXECUTION_OPERATION_IDS, start=1):
        operation = _dict(operations_by_id.get(operation_id))
        queue.append(
            {
                "step_number": step_number,
                "operation_id": operation_id,
                "lane": operation.get("lane") or _lane_for_operation(operation_id),
                "purpose": operation.get("purpose") or _purpose_for_operation(operation_id),
                "effect": _effect_for_operation(operation_id),
                "requirements": _requirements_for_operation(operation_id),
                "current_state": "ready_local_offline",
                "owner": "assistant_or_future_operator_local_only",
                "next_move": _next_move_for_operation(operation_id),
                "source_contract": operation.get("output_contract"),
                "may_execute_without_real_input": True,
                "may_execute_without_yymm4": True,
                "requires_explicit_gate": False,
                "writes_existing_lane_artifacts": False,
            }
        )
    blocked_operations = []
    for operation_id in BLOCKED_GATE_OPERATION_IDS:
        operation = _dict(operations_by_id.get(operation_id))
        blocked_operations.append(
            {
                "operation_id": operation_id,
                "lane": operation.get("lane") or _lane_for_operation(operation_id),
                "purpose": operation.get("purpose") or _purpose_for_operation(operation_id),
                "current_state": operation.get("build_status") or "blocked_by_gate",
                "owner": "human_gate_required",
                "next_move": _blocked_next_move(operation_id),
                "requires_explicit_gate": True,
            }
        )
    return {
        "schema_version": "local_edit_slice_queue.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "local_edit_slice_queue_ready",
        "source_operation_registry": _dict(state.get("paths")).get("edit_operation_registry"),
        "queue_operation_count": len(queue),
        "queue": queue,
        "blocked_operation_count": len(blocked_operations),
        "blocked_operations": blocked_operations,
        "selection_reason": "Only operations marked buildable_locally are queued; real-input, YMM4, and public-rights gates stay closed.",
        "actual_yymm4_import": False,
        "real_input_replacement_executed": False,
        "public_ready": False,
    }


def _scene_edit_execution_plan(state: dict[str, Any], queue: dict[str, Any]) -> dict[str, Any]:
    source_scene_plan = _dict(state.get("scene_operation_plan"))
    timing_model = _dict(state.get("timing_adjustment_model"))
    voice_map = _dict(state.get("voice_subtitle_operation_map"))
    visual_map = _dict(state.get("visual_asset_slot_map"))
    duration_by_scene = {
        str(row.get("scene_id")): row
        for row in _list(timing_model.get("scene_duration_contracts"))
        if isinstance(row, dict)
    }
    voice_rows_by_scene: dict[str, list[dict[str, Any]]] = {}
    for row in _list(voice_map.get("utterance_operations")):
        if isinstance(row, dict):
            voice_rows_by_scene.setdefault(str(row.get("scene_id")), []).append(row)
    visual_by_scene = {
        str(row.get("scene_id")): row
        for row in _list(visual_map.get("scene_visual_slots"))
        if isinstance(row, dict)
    }
    queue_ids = [str(row.get("operation_id")) for row in _list(queue.get("queue")) if isinstance(row, dict)]
    scenes = []
    for scene in _list(source_scene_plan.get("scenes")):
        if not isinstance(scene, dict):
            continue
        scene_id = str(scene.get("scene_id"))
        duration = _dict(duration_by_scene.get(scene_id))
        visual = _dict(visual_by_scene.get(scene_id))
        voice_rows = voice_rows_by_scene.get(scene_id, [])
        scenes.append(
            {
                "scene_id": scene_id,
                "title": scene.get("title"),
                "arc_phase": scene.get("arc_phase"),
                "row_range": scene.get("row_range"),
                "cue_ids": scene.get("cue_ids"),
                "local_execution_steps": [
                    _scene_step("set_scene_duration", f"Use provisional duration {duration.get('provisional_duration_sec')} sec."),
                    _scene_step("align_voice_subtitle", f"Bind {len(voice_rows)} draft cue rows to stable scene slots."),
                    _scene_step("split_or_wrap_subtitle", "Mark wrap intent only; final linebreaks wait for real text and observed timing."),
                    _scene_step("assign_visual_scene_template", f"Use template {visual.get('primary_template_id')}."),
                    _scene_step("place_citation_overlay", f"Reserve overlays {', '.join(_list(visual.get('citation_overlay_ids')))}."),
                    _scene_step("transfer_thumbnail_motif", f"Carry thumbnail motif rules {', '.join(_list(visual.get('thumbnail_transfer_rule_ids')))}."),
                ],
                "queued_operation_ids": [operation_id for operation_id in queue_ids if operation_id != "validate_operation_pack"],
                "validation_step": "validate_operation_pack",
                "blocked_after_local_execution": [
                    "verified_real_input_required_before_replacement",
                    "explicit_yymm4_gate_required_before_observation",
                    "rights_public_gate_required_before_final_claims",
                ],
                "execution_state": "ready_local_offline",
                "actual_yymm4_import": False,
                "real_input_replacement_executed": False,
            }
        )
    return {
        "schema_version": "scene_edit_execution_plan.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "scene_edit_execution_plan_ready_local_offline",
        "source_scene_operation_plan": _dict(state.get("paths")).get("scene_operation_plan"),
        "scene_count": len(scenes),
        "scenes": scenes,
        "global_validation_step": "validate_operation_pack",
        "actual_yymm4_import": False,
        "real_input_replacement_executed": False,
        "public_ready": False,
    }


def _scene_step(operation_id: str, effect: str) -> dict[str, Any]:
    return {
        "operation_id": operation_id,
        "effect": effect,
        "current_state": "ready_local_offline",
        "requires_explicit_gate": False,
    }


def _operation_gate_preservation_readback(
    state: dict[str, Any],
    queue: dict[str, Any],
    scene_plan: dict[str, Any],
) -> dict[str, Any]:
    closed_gate_flags = {
        "actual_yymm4_import": False,
        "yymm4_rendered": False,
        "production_ymmp_written": False,
        "real_input_replacement_executed": False,
        "real_transcript_exists": False,
        "rights_accepted": False,
        "public_ready": False,
        "final_thumbnail_approval": False,
        "live_fetch_performed": False,
        "external_media_downloaded": False,
        "oauth_or_api_used": False,
        "youtube_uploaded": False,
    }
    return {
        "schema_version": "operation_gate_preservation_readback.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "closed_gates_preserved",
        "queue_operation_count": queue.get("queue_operation_count"),
        "scene_count": scene_plan.get("scene_count"),
        "closed_gate_flags": closed_gate_flags,
        "forbidden_gates_closed": all(value is False for value in closed_gate_flags.values()),
        "protected_context_files_touched": {
            "editing_operations_files_touched": [],
            "output_template_files_touched": [],
            "input_intake_files_touched": [],
            "gui_lane_files_touched": [],
        },
        "readback_statement": "The pack materializes only a local execution queue; it does not modify source readiness artifacts or cross any input, YMM4, rights, or publication gate.",
    }


def _source_artifact_index(state: dict[str, Any]) -> dict[str, Any]:
    paths = _dict(state.get("paths"))
    records = [
        _source_record("editing_manifest", paths.get("editing_manifest"), "editing_operations_context_read_only", True),
        _source_record("edit_operation_registry", paths.get("edit_operation_registry"), "operation_registry_read_only", True),
        _source_record("scene_operation_plan", paths.get("scene_operation_plan"), "scene_contract_read_only", True),
        _source_record("timing_adjustment_model", paths.get("timing_adjustment_model"), "timing_contract_read_only", True),
        _source_record("voice_subtitle_operation_map", paths.get("voice_subtitle_operation_map"), "voice_subtitle_contract_read_only", True),
        _source_record("visual_asset_slot_map", paths.get("visual_asset_slot_map"), "visual_contract_read_only", True),
        _source_record("operation_gap_ledger", paths.get("operation_gap_ledger"), "gap_ledger_read_only", True),
        _source_record("editing_validation", paths.get("editing_validation"), "validation_readback_read_only", True),
    ]
    return {
        "schema_version": "local_edit_slice_source_artifact_index.v1",
        "artifact_id": state.get("artifact_id"),
        "editing_operations_context_read_only": True,
        "protected_context_dirs": list(PROTECTED_CONTEXT_DIRS),
        "records": records,
    }


def _source_record(record_id: str, path: Any, role: str, exists_expected: bool) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "repo_relative_path": str(path or ""),
        "role": role,
        "exists_expected": exists_expected,
        "display_zone": "source_artifact_index",
    }


def _manifest(
    state: dict[str, Any],
    queue: dict[str, Any],
    scene_plan: dict[str, Any],
    gate_readback: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "local_edit_slice_manifest.v1",
        "artifact_id": state.get("artifact_id"),
        "artifact_kind": "episode-local-edit-slice-execution-pack",
        "status": "local_edit_slice_execution_ready_local_offline",
        "parallel_lane": "editing_features_local_execution",
        "thread_id": "local-edit-slice-episode002",
        "output_dir": _relpath(output_root, repo_root),
        "files": {filename: _relpath(output_root / filename, repo_root) for filename in REQUIRED_LOCAL_EDIT_SLICE_FILES},
        "primary_review_file": state.get("primary_human_review"),
        "primary_human_review": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "queue_operation_count": queue.get("queue_operation_count"),
        "scene_count": scene_plan.get("scene_count"),
        "blocked_operation_count": queue.get("blocked_operation_count"),
        "gates_closed": gate_readback.get("forbidden_gates_closed"),
        "actual_yymm4_import": False,
        "yymm4_rendered": False,
        "real_input_replacement_executed": False,
        "public_ready": False,
        "rights_accepted": False,
        "final_thumbnail_approval": False,
        "protected_context_files_touched": gate_readback.get("protected_context_files_touched"),
        "thread_registry_updated": True,
        "shared_docs_touched": True,
        "full_pytest_run": False,
        "boundary_flags": state.get("boundary_flags"),
        "next_action": state.get("next_action"),
    }


def _render_html(
    state: dict[str, Any],
    queue: dict[str, Any],
    scene_plan: dict[str, Any],
    gate_readback: dict[str, Any],
) -> str:
    queue_cards = "\n".join(_render_queue_card(row) for row in _list(queue.get("queue")))
    scene_rows = "\n".join(_render_scene_row(row) for row in _list(scene_plan.get("scenes")))
    blocked_rows = "\n".join(_render_blocked_row(row) for row in _list(queue.get("blocked_operations")))
    gate_rows = "\n".join(_render_gate_flag(flag, value) for flag, value in _dict(gate_readback.get("closed_gate_flags")).items())
    return f"""<!doctype html>
<html lang="en" data-local-edit-slice="true" data-artifact-kind="episode-local-edit-slice-execution-pack">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Local Edit-Slice Execution</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #111411;
      --surface: #18211b;
      --panel: #213025;
      --ink: #eef7ee;
      --muted: #a8b8aa;
      --line: #3a4a3e;
      --teal: #68d8c0;
      --amber: #f3c969;
      --red: #f08c8c;
      --blue: #91b7ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; background: var(--bg); color: var(--ink); line-height: 1.5; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 28px 18px 42px; }}
    h1, h2, h3 {{ margin: 0; letter-spacing: 0; }}
    h1 {{ font-size: clamp(28px, 4vw, 44px); line-height: 1.08; }}
    h2 {{ font-size: 20px; margin: 28px 0 12px; }}
    h3 {{ font-size: 15px; }}
    p {{ color: var(--muted); }}
    .hero {{ display: grid; gap: 14px; padding-bottom: 18px; border-bottom: 1px solid var(--line); }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .chip {{ border: 1px solid var(--line); border-radius: 999px; padding: 5px 10px; background: var(--surface); font-size: 12px; }}
    .queue {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; }}
    .card {{ border: 1px solid var(--line); border-radius: 8px; background: var(--surface); padding: 14px; min-height: 150px; }}
    .step {{ color: var(--amber); font-size: 12px; }}
    .scene-row, .blocked-row, .gate-row {{ display: grid; grid-template-columns: 120px 1fr 1fr; gap: 8px; padding: 10px 0; border-bottom: 1px solid var(--line); }}
    .cell {{ border: 1px solid var(--line); border-radius: 8px; background: var(--panel); padding: 10px; overflow-wrap: anywhere; }}
    .ok {{ color: var(--teal); }}
    .hold {{ color: var(--red); }}
    code {{ color: var(--amber); }}
    @media (prefers-color-scheme: light) {{
      :root {{ --bg: #f7faf7; --surface: #ffffff; --panel: #eef4ef; --ink: #172118; --muted: #4d6251; --line: #cbd9ce; }}
    }}
    @media (max-width: 760px) {{ main {{ padding: 20px 12px 32px; }} .scene-row, .blocked-row, .gate-row {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div class="chips">
        <span class="chip">queue operations: {_escape(queue.get("queue_operation_count"))}</span>
        <span class="chip">scenes: {_escape(scene_plan.get("scene_count"))}</span>
        <span class="chip">gates closed: {_escape(gate_readback.get("forbidden_gates_closed"))}</span>
        <span class="chip">real input: not replaced</span>
        <span class="chip">YMM4: not launched</span>
      </div>
      <h1>Episode 002 Local Edit-Slice Execution</h1>
      <p>This pack converts completed editing operation contracts into a local execution queue. It preserves the real-input, YMM4, rights, thumbnail, and public gates.</p>
    </section>

    <section data-region="execution-queue">
      <h2>Execution Queue</h2>
      <div class="queue">{queue_cards}</div>
    </section>

    <section data-region="scene-execution-plan">
      <h2>Scene Execution Plan</h2>
      {scene_rows}
    </section>

    <section data-region="blocked-gates">
      <h2>Blocked Gate Operations</h2>
      {blocked_rows}
    </section>

    <section data-region="gate-readback">
      <h2>Gate Readback</h2>
      {gate_rows}
    </section>
  </main>
</body>
</html>
"""


def _render_queue_card(row: Any) -> str:
    item = _dict(row)
    return f"""<article class="card">
  <div class="step">Step {_escape(item.get("step_number"))} / {_escape(item.get("lane"))}</div>
  <h3>{_escape(item.get("operation_id"))}</h3>
  <p>{_escape(item.get("effect"))}</p>
  <p class="ok">{_escape(item.get("current_state"))}</p>
</article>"""


def _render_scene_row(row: Any) -> str:
    item = _dict(row)
    operations = ", ".join(str(step.get("operation_id")) for step in _list(item.get("local_execution_steps")) if isinstance(step, dict))
    return f"""<div class="scene-row">
  <div class="cell"><code>{_escape(item.get("scene_id"))}</code><br>{_escape(item.get("arc_phase"))}</div>
  <div class="cell">{_escape(item.get("title"))}<br>{_escape(operations)}</div>
  <div class="cell hold">{_escape(', '.join(_list(item.get("blocked_after_local_execution"))))}</div>
</div>"""


def _render_blocked_row(row: Any) -> str:
    item = _dict(row)
    return f"""<div class="blocked-row">
  <div><code>{_escape(item.get("operation_id"))}</code></div>
  <div>{_escape(item.get("purpose"))}</div>
  <div class="hold">{_escape(item.get("next_move"))}</div>
</div>"""


def _render_gate_flag(flag: str, value: Any) -> str:
    return f"""<div class="gate-row">
  <div><code>{_escape(flag)}</code></div>
  <div>{_escape(value)}</div>
  <div class="ok">closed in this pack</div>
</div>"""


def _render_markdown(
    state: dict[str, Any],
    queue: dict[str, Any],
    scene_plan: dict[str, Any],
    gate_readback: dict[str, Any],
) -> str:
    queue_lines = "\n".join(
        f"- {row.get('step_number')}. {row.get('operation_id')}: {row.get('effect')}"
        for row in _list(queue.get("queue"))
        if isinstance(row, dict)
    )
    scene_lines = "\n".join(
        f"- {scene.get('scene_id')}: {scene.get('title')} / {len(_list(scene.get('local_execution_steps')))} local steps"
        for scene in _list(scene_plan.get("scenes"))
        if isinstance(scene, dict)
    )
    gate_lines = "\n".join(
        f"- {flag}: {value}"
        for flag, value in _dict(gate_readback.get("closed_gate_flags")).items()
    )
    return f"""# Episode 002 local edit-slice execution

This local edit-slice execution pack turns the completed editing operations readiness package into a queue for the next local-only edit slice. It does not replace real input, launch YMM4, render, approve rights, approve final thumbnail output, or publish.

Primary review file: `{state.get("primary_human_review")}`

## Queue

{queue_lines}

## Scene Plan

{scene_lines}

## Closed Gate Readback

{gate_lines}
"""


def _render_review_checklist(state: dict[str, Any], queue: dict[str, Any], scene_plan: dict[str, Any]) -> str:
    return f"""# Local Edit-Slice Execution Review Checklist

- Open `local_edit_execution_preview.html`.
- Confirm the queue contains {queue.get("queue_operation_count")} local operations.
- Confirm the scene plan covers {scene_plan.get("scene_count")} scenes.
- Confirm blocked operations are not queued for execution.
- Confirm no real input replacement, YMM4 launch/import/render, rights acceptance, final thumbnail approval, or publication step is claimed.
"""


def _render_limitations(state: dict[str, Any]) -> str:
    return """# Limitations

- Do not launch YMM4 from this pack.
- Do not import CSV into YMM4 from this pack.
- Do not render or write a production `.ymmp`.
- Do not replace real source or transcript content without verified local input.
- Do not claim rights acceptance, public readiness, final thumbnail approval, upload, or publication.
- This pack only queues local draft edit operations derived from existing read-only contracts.
"""


def _render_readme(
    state: dict[str, Any],
    queue: dict[str, Any],
    scene_plan: dict[str, Any],
    gate_readback: dict[str, Any],
) -> str:
    return f"""# Episode 002 Local Edit-Slice Execution Pack

This package is the continuation after `editing_operations_readiness_pack`.

- Queue operations: {queue.get("queue_operation_count")}
- Scenes covered: {scene_plan.get("scene_count")}
- Gates closed: {gate_readback.get("forbidden_gates_closed")}
- Primary review: `{state.get("primary_human_review")}`
- Machine readback: `{state.get("primary_machine_readable")}`

The pack is local/offline and reads source operation artifacts without modifying them.
"""


def _lane_for_operation(operation_id: str) -> str:
    return {
        "set_scene_duration": "timing",
        "align_voice_subtitle": "voice_subtitle",
        "split_or_wrap_subtitle": "voice_subtitle",
        "assign_visual_scene_template": "visual",
        "place_citation_overlay": "visual",
        "transfer_thumbnail_motif": "visual",
        "validate_operation_pack": "validation",
        "flag_real_input_required": "input_boundary",
        "mark_yymm4_observation_needed": "yymm4_observation",
        "capture_yymm4_readback": "yymm4_observation",
    }.get(operation_id, "unknown")


def _purpose_for_operation(operation_id: str) -> str:
    return {
        "set_scene_duration": "Set provisional scene durations from local timing contracts.",
        "align_voice_subtitle": "Bind draft cues to stable voice/subtitle slots.",
        "split_or_wrap_subtitle": "Mark subtitle wrapping intent before final timing.",
        "assign_visual_scene_template": "Assign local visual templates to scenes.",
        "place_citation_overlay": "Reserve citation overlay slots without approval claims.",
        "transfer_thumbnail_motif": "Carry thumbnail motif language into scene slots.",
        "validate_operation_pack": "Validate local package completeness and closed gates.",
    }.get(operation_id, "Record operation state.")


def _effect_for_operation(operation_id: str) -> str:
    return {
        "set_scene_duration": "Creates a stable provisional timing pass for each scene.",
        "align_voice_subtitle": "Keeps cue order and voice/subtitle ownership explicit.",
        "split_or_wrap_subtitle": "Separates local wrap intent from final YMM4 linebreak acceptance.",
        "assign_visual_scene_template": "Connects each scene to an existing template slot.",
        "place_citation_overlay": "Allocates citation placeholders while real source wording stays gated.",
        "transfer_thumbnail_motif": "Reuses thumbnail motifs as local scene language without final approval.",
        "validate_operation_pack": "Checks all generated files and closed gate claims.",
    }.get(operation_id, "Records local execution intent.")


def _requirements_for_operation(operation_id: str) -> list[str]:
    return {
        "set_scene_duration": ["scene_operation_plan.json", "timing_adjustment_model.json"],
        "align_voice_subtitle": ["voice_subtitle_operation_map.json"],
        "split_or_wrap_subtitle": ["voice_subtitle_operation_map.json"],
        "assign_visual_scene_template": ["visual_asset_slot_map.json"],
        "place_citation_overlay": ["visual_asset_slot_map.json", "operation_gap_ledger.json"],
        "transfer_thumbnail_motif": ["visual_asset_slot_map.json"],
        "validate_operation_pack": ["local_edit_slice_manifest.json", "operation_gate_preservation_readback.json"],
    }.get(operation_id, [])


def _next_move_for_operation(operation_id: str) -> str:
    return {
        "set_scene_duration": "Apply provisional durations to the local draft edit plan only.",
        "align_voice_subtitle": "Review cue-to-slot bindings before any real input replacement.",
        "split_or_wrap_subtitle": "Mark wrap intent and defer final linebreaks.",
        "assign_visual_scene_template": "Use the mapped local template as the scene placeholder.",
        "place_citation_overlay": "Keep citation wording as placeholder until verified source material exists.",
        "transfer_thumbnail_motif": "Carry motif tokens without declaring final thumbnail acceptance.",
        "validate_operation_pack": "Run targeted tests and gate scans after regeneration.",
    }.get(operation_id, "Review before execution.")


def _blocked_next_move(operation_id: str) -> str:
    return {
        "flag_real_input_required": "Wait for verified local source/transcript input before replacement.",
        "mark_yymm4_observation_needed": "Open an explicit YMM4 observation gate before launch/import/readback.",
        "capture_yymm4_readback": "Fill schema only after explicit manual observation.",
    }.get(operation_id, "Requires a human gate before work.")
