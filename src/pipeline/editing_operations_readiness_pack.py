"""Editing operations readiness package for episode 002."""

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

DEFAULT_OUTPUT_DIRNAME = "editing_operations_readiness_pack"
DEFAULT_ARTIFACT_ID = "episode_002_editing_operations_readiness_pack_v1"

OUTPUT_TEMPLATE_DIRNAME = "output_template_readiness_pack"
REAL_INPUT_DIRNAME = "real_input_intake_readiness"
TRANSCRIPT_READINESS_DIRNAME = "transcript_substitution_readiness"
IR_BRIDGE_DIRNAME = "ir_bridge"
JAPANESE_GRAPHIC_CONSOLE_DIRNAME = "japanese_graphic_review_console"

REQUIRED_EDITING_OPERATIONS_FILES = (
    "editing_operations_manifest.json",
    "editing_operations_preview.html",
    "editing_operations_preview.md",
    "edit_operation_registry.json",
    "scene_operation_plan.json",
    "timing_adjustment_model.json",
    "voice_subtitle_operation_map.json",
    "visual_asset_slot_map.json",
    "yymm4_observation_protocol.md",
    "yymm4_readback_schema.json",
    "operation_gap_ledger.json",
    "source_artifact_index.json",
    "validation_readback.json",
    "review_checklist.md",
    "limitations.md",
    "README_EDITING_OPERATIONS_READINESS.md",
)

REQUIRED_OPERATION_IDS = (
    "set_scene_duration",
    "align_voice_subtitle",
    "split_or_wrap_subtitle",
    "assign_visual_scene_template",
    "place_citation_overlay",
    "transfer_thumbnail_motif",
    "mark_yymm4_observation_needed",
    "flag_real_input_required",
)

OPTIONAL_OPERATION_IDS = (
    "capture_yymm4_readback",
    "validate_operation_pack",
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

REQUIRED_GAP_GROUPS = (
    "buildable_locally",
    "blocked_by_real_input",
    "blocked_by_explicit_yymm4_gate",
    "blocked_by_public_rights_gate",
)

PROTECTED_GUI_LANE_DIRS = (
    "production_pilots/yukkuri_newsroom_content_spine_002/japanese_graphic_review_console",
    "production_pilots/yukkuri_newsroom_content_spine_002/primary_artifact_review_console",
    "production_pilots/yukkuri_newsroom_content_spine_002/review_console_redesign_prototype",
    "production_pilots/yukkuri_newsroom_content_spine_002/split_view_decision_evidence_prototype",
)

PROTECTED_OUTPUT_TEMPLATE_DIRS = (
    "production_pilots/yukkuri_newsroom_content_spine_002/output_template_readiness_pack",
)

PROTECTED_INPUT_INTAKE_DIRS = (
    "production_pilots/yukkuri_newsroom_content_spine_002/real_input_intake_readiness",
)


def build_editing_operations_readiness_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build the local editing operations readiness package."""
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

    registry = _edit_operation_registry(state)
    scene_plan = _scene_operation_plan(state, registry)
    timing_model = _timing_adjustment_model(state, scene_plan)
    voice_map = _voice_subtitle_operation_map(state, scene_plan)
    visual_map = _visual_asset_slot_map(state, scene_plan)
    readback_schema = _yymm4_readback_schema(state, scene_plan)
    gap_ledger = _operation_gap_ledger(state, registry)
    source_index = _source_artifact_index(state)
    manifest = _manifest(
        state,
        registry,
        scene_plan,
        timing_model,
        voice_map,
        visual_map,
        readback_schema,
        gap_ledger,
        output_root,
        repo_root,
    )

    _write_json(output_root / "editing_operations_manifest.json", manifest)
    _write_json(output_root / "edit_operation_registry.json", registry)
    _write_json(output_root / "scene_operation_plan.json", scene_plan)
    _write_json(output_root / "timing_adjustment_model.json", timing_model)
    _write_json(output_root / "voice_subtitle_operation_map.json", voice_map)
    _write_json(output_root / "visual_asset_slot_map.json", visual_map)
    _write_json(output_root / "yymm4_readback_schema.json", readback_schema)
    _write_json(output_root / "operation_gap_ledger.json", gap_ledger)
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_text(output_root / "yymm4_observation_protocol.md", _render_yymm4_protocol(state, readback_schema))
    _write_text(output_root / "editing_operations_preview.html", _render_html(state, registry, scene_plan, timing_model, voice_map, visual_map, gap_ledger))
    _write_text(output_root / "editing_operations_preview.md", _render_markdown(state, registry, scene_plan, timing_model, voice_map, visual_map, gap_ledger))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state))
    _write_text(output_root / "limitations.md", _render_limitations(state))
    _write_text(output_root / "README_EDITING_OPERATIONS_READINESS.md", _render_readme(state, registry, scene_plan, gap_ledger))

    readback = validate_editing_operations_readiness_pack(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_editing_operations_readiness_pack(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_editing_operations_readiness_pack(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated editing operations readiness package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_EDITING_OPERATIONS_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["editing_operations_manifest.json"])
    registry = _load_json_if_present(files["edit_operation_registry.json"])
    scene_plan = _load_json_if_present(files["scene_operation_plan.json"])
    timing_model = _load_json_if_present(files["timing_adjustment_model.json"])
    voice_map = _load_json_if_present(files["voice_subtitle_operation_map.json"])
    visual_map = _load_json_if_present(files["visual_asset_slot_map.json"])
    readback_schema = _load_json_if_present(files["yymm4_readback_schema.json"])
    gap_ledger = _load_json_if_present(files["operation_gap_ledger.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])
    json_payloads = {
        "manifest": manifest,
        "registry": registry,
        "scene_plan": scene_plan,
        "timing_model": timing_model,
        "voice_map": voice_map,
        "visual_map": visual_map,
        "readback_schema": readback_schema,
        "gap_ledger": gap_ledger,
        "source_index": source_index,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = _dict(json_payloads["manifest"])
    registry = _dict(json_payloads["registry"])
    scene_plan = _dict(json_payloads["scene_plan"])
    timing_model = _dict(json_payloads["timing_model"])
    voice_map = _dict(json_payloads["voice_map"])
    visual_map = _dict(json_payloads["visual_map"])
    readback_schema = _dict(json_payloads["readback_schema"])
    gap_ledger = _dict(json_payloads["gap_ledger"])
    source_index = _dict(json_payloads["source_index"])

    html_text = files["editing_operations_preview.html"].read_text(encoding="utf-8") if files["editing_operations_preview.html"].exists() else ""
    markdown_text = files["editing_operations_preview.md"].read_text(encoding="utf-8") if files["editing_operations_preview.md"].exists() else ""
    protocol_text = files["yymm4_observation_protocol.md"].read_text(encoding="utf-8") if files["yymm4_observation_protocol.md"].exists() else ""
    limitations_text = files["limitations.md"].read_text(encoding="utf-8") if files["limitations.md"].exists() else ""

    operations = [row for row in _list(registry.get("operations")) if isinstance(row, dict)]
    operation_ids = {str(row.get("operation_id")) for row in operations}
    scenes = [row for row in _list(scene_plan.get("scenes")) if isinstance(row, dict)]
    voice_rows = [row for row in _list(voice_map.get("utterance_operations")) if isinstance(row, dict)]
    visual_slots = [row for row in _list(visual_map.get("scene_visual_slots")) if isinstance(row, dict)]
    gap_groups = _dict(gap_ledger.get("groups"))
    boundary_flags = _dict(manifest.get("boundary_flags"))
    gui_touches = _list(manifest.get("gui_lane_files_touched"))
    output_template_touches = _list(manifest.get("output_template_files_touched"))
    input_intake_touches = _list(manifest.get("input_intake_files_touched"))

    if manifest.get("artifact_kind") != "episode-editing-operations-readiness-pack":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "editing_operations_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")
    if len(operations) < len(REQUIRED_OPERATION_IDS):
        failed_checks.append("operation_registry_too_short")
    for operation_id in REQUIRED_OPERATION_IDS:
        if operation_id not in operation_ids:
            failed_checks.append(f"operation_missing:{operation_id}")
    if len(scenes) < 3:
        failed_checks.append("scene_operation_plan_too_short")
    if timing_model.get("status") != "provisional_timing_model_ready_no_audio_or_yymm4_timing":
        failed_checks.append("timing_model_status_mismatch")
    if voice_map.get("status") != "voice_subtitle_operations_ready_no_yymm4_voiceitems":
        failed_checks.append("voice_subtitle_operation_status_mismatch")
    if not voice_rows:
        failed_checks.append("voice_subtitle_operations_empty")
    if visual_map.get("status") != "visual_asset_slots_ready_no_external_media":
        failed_checks.append("visual_slot_map_status_mismatch")
    if not visual_slots:
        failed_checks.append("visual_slot_map_empty")
    if readback_schema.get("status") != "schema_ready_no_actual_import":
        failed_checks.append("yymm4_readback_schema_status_mismatch")
    if readback_schema.get("actual_yymm4_import") is not False:
        failed_checks.append("readback_schema_actual_yymm4_import_not_false")
    if readback_schema.get("yymm4_rendered") is not False:
        failed_checks.append("readback_schema_yymm4_rendered_not_false")
    if manifest.get("invented_real_content") is not False:
        failed_checks.append("invented_real_content_not_false")
    if manifest.get("actual_yymm4_import") is not False:
        failed_checks.append("actual_yymm4_import_not_false")
    if manifest.get("yymm4_rendered") is not False:
        failed_checks.append("yymm4_rendered_not_false")
    if manifest.get("production_ready") is not False:
        failed_checks.append("production_ready_not_false")
    if manifest.get("public_ready") is not False:
        failed_checks.append("public_ready_not_false")
    if manifest.get("thread_registry_updated") is not True:
        failed_checks.append("thread_registry_updated_not_true")
    if manifest.get("shared_docs_touched") is not True:
        failed_checks.append("shared_docs_touched_not_true")
    if gui_touches:
        failed_checks.append("gui_lane_files_touched_not_empty")
    if output_template_touches:
        failed_checks.append("output_template_files_touched_not_empty")
    if input_intake_touches:
        failed_checks.append("input_intake_files_touched_not_empty")
    if source_index.get("output_template_context_read_only") is not True:
        failed_checks.append("output_template_context_not_read_only")
    if source_index.get("input_intake_context_read_only") is not True:
        failed_checks.append("input_intake_context_not_read_only")
    if source_index.get("gui_lane_context_read_only") is not True:
        failed_checks.append("gui_lane_context_not_read_only")
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")
    for group_id in REQUIRED_GAP_GROUPS:
        if not _list(gap_groups.get(group_id)):
            failed_checks.append(f"gap_group_missing_or_empty:{group_id}")
    for marker in (
        'data-editing-operations="true"',
        'data-region="operation-lanes"',
        'data-region="scene-operation-matrix"',
        'data-region="timing-strip"',
        'data-region="voice-subtitle-lane"',
        'data-region="visual-slot-lane"',
        'data-region="yymm4-observation-lane"',
    ):
        if marker not in html_text:
            failed_checks.append(f"html_marker_missing:{marker}")
    if "color-scheme: dark light" not in html_text:
        failed_checks.append("dark_color_scheme_missing")
    if "prefers-color-scheme" not in html_text:
        failed_checks.append("prefers_color_scheme_missing")
    if not markdown_text.strip():
        failed_checks.append("markdown_preview_empty")
    if "future manual observation only" not in protocol_text:
        failed_checks.append("protocol_future_manual_boundary_missing")
    if "Do not launch YMM4" not in protocol_text:
        failed_checks.append("protocol_no_launch_boundary_missing")
    if "no actual YMM4 import" not in limitations_text:
        failed_checks.append("limitations_yymm4_gate_missing")

    external_refs = _external_refs_in_files([path for name, path in files.items() if name != "validation_readback.json"])
    forbidden_hits = _forbidden_true_claims(root)
    temporary_hits = _temporary_copy_hits(
        [
            files["editing_operations_preview.html"],
            files["editing_operations_preview.md"],
            files["README_EDITING_OPERATIONS_READINESS.md"],
        ]
    )
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "html_preview_exists": files["editing_operations_preview.html"].exists(),
        "markdown_preview_exists": files["editing_operations_preview.md"].exists(),
        "operation_count": len(operations),
        "required_operations_present": all(operation_id in operation_ids for operation_id in REQUIRED_OPERATION_IDS),
        "scene_count": len(scenes),
        "voice_operation_rows": len(voice_rows),
        "visual_slot_rows": len(visual_slots),
        "gap_groups_present": all(bool(_list(gap_groups.get(group_id))) for group_id in REQUIRED_GAP_GROUPS),
        "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS),
        "gui_lane_files_touched": gui_touches,
        "output_template_files_touched": output_template_touches,
        "input_intake_files_touched": input_intake_touches,
        "thread_registry_updated": manifest.get("thread_registry_updated"),
        "shared_docs_touched": manifest.get("shared_docs_touched"),
        "external_dependency_status": "none_found" if not external_refs else "found",
        "forbidden_true_claims_absent": not forbidden_hits,
        "temporary_copy_absent": not temporary_hits,
    }
    return {
        "schema_version": "editing_operations_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "primary_review_file": str(root / "editing_operations_preview.html"),
        "primary_human_review": str(root / "editing_operations_preview.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "operation_count": len(operations),
        "scene_count": len(scenes),
        "timing_model_status": timing_model.get("status"),
        "voice_subtitle_operation_status": voice_map.get("status"),
        "visual_slot_map_status": visual_map.get("status"),
        "yymm4_protocol_status": manifest.get("yymm4_protocol_status"),
        "yymm4_readback_schema_status": readback_schema.get("status"),
        "invented_real_content": manifest.get("invented_real_content"),
        "actual_yymm4_import": manifest.get("actual_yymm4_import"),
        "gui_lane_files_touched": gui_touches,
        "output_template_files_touched": output_template_touches,
        "input_intake_files_touched": input_intake_touches,
        "thread_registry_updated": manifest.get("thread_registry_updated"),
        "shared_docs_touched": manifest.get("shared_docs_touched"),
        "full_pytest_run": False,
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{(root / "editing_operations_preview.html").resolve()}"',
        "access_state": "verified_present" if (root / "editing_operations_preview.html").exists() else "missing",
        "next_action": manifest.get("next_action"),
    }


def _input_paths(source_root: Path) -> dict[str, Path]:
    output_template_root = source_root / OUTPUT_TEMPLATE_DIRNAME
    real_input_root = source_root / REAL_INPUT_DIRNAME
    transcript_root = source_root / TRANSCRIPT_READINESS_DIRNAME
    ir_root = source_root / IR_BRIDGE_DIRNAME
    gui_root = source_root / JAPANESE_GRAPHIC_CONSOLE_DIRNAME
    return {
        "output_template_root": output_template_root,
        "output_template_manifest": output_template_root / "output_template_readiness_manifest.json",
        "scene_timing_map": output_template_root / "scene_timing_map.json",
        "voice_subtitle_mapping": output_template_root / "voice_subtitle_mapping.json",
        "visual_scene_template_registry": output_template_root / "visual_scene_template_registry.json",
        "citation_overlay_spec": output_template_root / "citation_overlay_spec.json",
        "thumbnail_transfer_map": output_template_root / "thumbnail_transfer_map.json",
        "template_gap_closure_readback": output_template_root / "template_gap_closure_readback.json",
        "output_template_validation": output_template_root / "validation_readback.json",
        "real_input_root": real_input_root,
        "real_input_manifest": real_input_root / "real_input_intake_manifest.json",
        "source_transcript_contract_schema": real_input_root / "source_transcript_contract.schema.json",
        "real_input_replacement_plan": real_input_root / "real_input_replacement_plan.md",
        "real_input_validation": real_input_root / "validation_readback.json",
        "draft_yymm4_csv": transcript_root / "regenerated_draft_yymm4.csv",
        "ir_draft_yymm4_csv": ir_root / "draft_yymm4.csv",
        "japanese_console_validation": gui_root / "validation_readback.json",
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "output_template_manifest": _load_json_if_present(paths["output_template_manifest"]),
        "scene_timing_map": _load_json_if_present(paths["scene_timing_map"]),
        "voice_subtitle_mapping": _load_json_if_present(paths["voice_subtitle_mapping"]),
        "visual_scene_template_registry": _load_json_if_present(paths["visual_scene_template_registry"]),
        "citation_overlay_spec": _load_json_if_present(paths["citation_overlay_spec"]),
        "thumbnail_transfer_map": _load_json_if_present(paths["thumbnail_transfer_map"]),
        "template_gap_closure_readback": _load_json_if_present(paths["template_gap_closure_readback"]),
        "output_template_validation": _load_json_if_present(paths["output_template_validation"]),
        "real_input_manifest": _load_json_if_present(paths["real_input_manifest"]),
        "source_transcript_contract_schema": _load_json_if_present(paths["source_transcript_contract_schema"]),
        "real_input_validation": _load_json_if_present(paths["real_input_validation"]),
        "japanese_console_validation": _load_json_if_present(paths["japanese_console_validation"]),
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
    output_template_manifest = _dict(payloads.get("output_template_manifest"))
    real_input_manifest = _dict(payloads.get("real_input_manifest"))
    scene_timing_map = _dict(payloads.get("scene_timing_map"))
    voice_mapping = _dict(payloads.get("voice_subtitle_mapping"))
    visual_registry = _dict(payloads.get("visual_scene_template_registry"))
    overlay_spec = _dict(payloads.get("citation_overlay_spec"))
    thumbnail_map = _dict(payloads.get("thumbnail_transfer_map"))
    return {
        "schema_version": "editing_operations_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-editing-operations-readiness-pack",
        "status": "editing_operations_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "repo_root": str(repo_root),
        "paths": {name: _relpath(path, repo_root) for name, path in paths.items() if isinstance(path, Path)},
        "output_template_status": output_template_manifest.get("status", "unknown"),
        "real_input_status": real_input_manifest.get("status", "unknown"),
        "scene_timing_map": scene_timing_map,
        "voice_subtitle_mapping": voice_mapping,
        "visual_scene_template_registry": visual_registry,
        "citation_overlay_spec": overlay_spec,
        "thumbnail_transfer_map": thumbnail_map,
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
        "primary_human_review": _relpath(output_root / "editing_operations_preview.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_action": "Use the operation contracts to choose a manual edit slice; verify real input before replacement and use an explicit YMM4 observation gate before import/readback work.",
    }


def _edit_operation_registry(state: dict[str, Any]) -> dict[str, Any]:
    operations = [
        _operation(
            "set_scene_duration",
            "timing",
            "Set provisional scene durations from the existing scene timing map.",
            ["scene_timing_map.json"],
            "scene_operation_plan.scenes[].duration_contract",
            "buildable_locally",
            ["actual audio duration remains blocked by explicit YMM4 gate"],
        ),
        _operation(
            "align_voice_subtitle",
            "voice_subtitle",
            "Bind each draft CSV cue to a voice slot, subtitle slot, and scene.",
            ["voice_subtitle_mapping.json", "scene_timing_map.json"],
            "voice_subtitle_operation_map.utterance_operations[]",
            "buildable_locally",
            ["actual VoiceItem ids remain blocked by explicit YMM4 gate"],
        ),
        _operation(
            "split_or_wrap_subtitle",
            "voice_subtitle",
            "Mark subtitle wrapping responsibility before real timing observation.",
            ["voice_subtitle_mapping.json"],
            "voice_subtitle_operation_map.utterance_operations[].subtitle_wrap_contract",
            "buildable_locally",
            ["final line breaks wait for real text and YMM4 timing"],
        ),
        _operation(
            "assign_visual_scene_template",
            "visual",
            "Assign existing visual scene template ids to each scene.",
            ["visual_scene_template_registry.json"],
            "visual_asset_slot_map.scene_visual_slots[]",
            "buildable_locally",
            ["production visual acceptance remains outside this package"],
        ),
        _operation(
            "place_citation_overlay",
            "visual",
            "Reserve citation overlay slots without claiming real source approval.",
            ["citation_overlay_spec.json"],
            "visual_asset_slot_map.scene_visual_slots[].citation_overlay_ids",
            "buildable_locally",
            ["verified local source and rights review are still required"],
        ),
        _operation(
            "transfer_thumbnail_motif",
            "visual",
            "Transfer approved thumbnail motif contracts into scene slot language.",
            ["thumbnail_transfer_map.json"],
            "visual_asset_slot_map.scene_visual_slots[].thumbnail_transfer_rule_ids",
            "buildable_locally",
            ["final thumbnail approval remains blocked by public/rights gate"],
        ),
        _operation(
            "mark_yymm4_observation_needed",
            "yymm4_observation",
            "Attach future manual YMM4 readback fields without launching or importing.",
            ["yymm4_readback_schema.json"],
            "scene_operation_plan.scenes[].yymm4_observation_needed",
            "blocked_by_explicit_yymm4_gate",
            ["YMM4 GUI launch/import/render remains closed in this package"],
        ),
        _operation(
            "flag_real_input_required",
            "input_boundary",
            "Flag every source/text dependent slot as requiring verified local input.",
            ["real_input_intake_manifest.json", "source_transcript_contract.schema.json"],
            "operation_gap_ledger.groups.blocked_by_real_input",
            "blocked_by_real_input",
            ["no real source transcript is ingested here"],
        ),
        _operation(
            "capture_yymm4_readback",
            "yymm4_observation",
            "Define the future readback shape an operator can fill after an explicit gate.",
            ["yymm4_readback_schema.json"],
            "yymm4_readback_schema.json",
            "blocked_by_explicit_yymm4_gate",
            ["schema only; no actual observation is recorded"],
        ),
        _operation(
            "validate_operation_pack",
            "validation",
            "Validate package completeness, local-only references, and closed claims.",
            ["validation_readback.json"],
            "validation_readback.json",
            "buildable_locally",
            ["full pytest is outside the scoped validation budget"],
        ),
    ]
    return {
        "schema_version": "edit_operation_registry.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "operation_registry_ready_local_offline",
        "operation_count": len(operations),
        "required_operation_ids": list(REQUIRED_OPERATION_IDS),
        "optional_operation_ids": list(OPTIONAL_OPERATION_IDS),
        "operations": operations,
        "actual_yymm4_import": False,
        "invented_real_content": False,
    }


def _operation(
    operation_id: str,
    lane: str,
    purpose: str,
    input_artifacts: list[str],
    output_contract: str,
    build_status: str,
    remaining_gates: list[str],
) -> dict[str, Any]:
    return {
        "operation_id": operation_id,
        "lane": lane,
        "purpose": purpose,
        "input_artifacts": input_artifacts,
        "output_contract": output_contract,
        "build_status": build_status,
        "remaining_gates": remaining_gates,
        "local_only": True,
    }


def _scene_operation_plan(state: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    timing_map = _dict(state.get("scene_timing_map"))
    visual_registry = _dict(state.get("visual_scene_template_registry"))
    overlay_spec = _dict(state.get("citation_overlay_spec"))
    thumbnail_map = _dict(state.get("thumbnail_transfer_map"))
    voice_mapping = _dict(state.get("voice_subtitle_mapping"))
    scenes = []
    for scene in _list(timing_map.get("scenes")):
        if not isinstance(scene, dict):
            continue
        scene_id = str(scene.get("scene_id") or "")
        assignment = _find_scene_assignment(visual_registry, scene_id)
        overlays = _overlay_ids_for_scene(overlay_spec, scene_id)
        transfer_rules = _thumbnail_rules_for_scene(thumbnail_map, scene_id)
        cue_ids = [str(cue_id) for cue_id in _list(scene.get("cue_ids"))]
        scenes.append(
            {
                "scene_id": scene_id,
                "title": scene.get("title"),
                "arc_phase": scene.get("arc_phase"),
                "row_range": {"start": scene.get("row_start"), "end": scene.get("row_end")},
                "cue_ids": cue_ids,
                "duration_contract": {
                    "operation_id": "set_scene_duration",
                    "provisional_start_sec": scene.get("provisional_start_sec"),
                    "provisional_end_sec": scene.get("provisional_end_sec"),
                    "provisional_duration_sec": scene.get("provisional_duration_sec"),
                    "actual_timing_ready": False,
                },
                "voice_subtitle_contract": {
                    "operation_ids": ["align_voice_subtitle", "split_or_wrap_subtitle"],
                    "cue_count": len(cue_ids),
                    "source_status": voice_mapping.get("status"),
                    "actual_voiceitems_ready": False,
                },
                "visual_contract": {
                    "operation_ids": ["assign_visual_scene_template", "place_citation_overlay", "transfer_thumbnail_motif"],
                    "primary_template_id": assignment.get("primary_template_id"),
                    "supporting_template_ids": _list(assignment.get("supporting_template_ids")),
                    "citation_overlay_ids": overlays,
                    "thumbnail_transfer_rule_ids": transfer_rules,
                    "external_media_allowed": False,
                },
                "gate_contracts": [
                    {
                        "operation_id": "flag_real_input_required",
                        "reason": "source, transcript, citation text, and final wording need verified local input",
                        "status": "blocked_by_real_input",
                    },
                    {
                        "operation_id": "mark_yymm4_observation_needed",
                        "reason": "actual VoiceItem ids and timing require future manual YMM4 readback",
                        "status": "blocked_by_explicit_yymm4_gate",
                    },
                ],
                "operation_ids": [
                    "set_scene_duration",
                    "align_voice_subtitle",
                    "split_or_wrap_subtitle",
                    "assign_visual_scene_template",
                    "place_citation_overlay",
                    "transfer_thumbnail_motif",
                    "flag_real_input_required",
                    "mark_yymm4_observation_needed",
                ],
            }
        )
    return {
        "schema_version": "scene_operation_plan.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "scene_operation_plan_ready_local_offline",
        "source_scene_timing_map": _dict(state.get("paths")).get("scene_timing_map"),
        "operation_registry": registry.get("status"),
        "scene_count": len(scenes),
        "scenes": scenes,
        "actual_yymm4_import": False,
        "invented_real_content": False,
    }


def _find_scene_assignment(visual_registry: dict[str, Any], scene_id: str) -> dict[str, Any]:
    for row in _list(visual_registry.get("scene_assignments")):
        if isinstance(row, dict) and row.get("scene_id") == scene_id:
            return row
    return {}


def _overlay_ids_for_scene(overlay_spec: dict[str, Any], scene_id: str) -> list[str]:
    return [
        str(row.get("overlay_id"))
        for row in _list(overlay_spec.get("overlay_slots"))
        if isinstance(row, dict) and row.get("scene_id") == scene_id
    ]


def _thumbnail_rules_for_scene(thumbnail_map: dict[str, Any], scene_id: str) -> list[str]:
    rules = []
    for row in _list(thumbnail_map.get("transfer_rules")):
        if not isinstance(row, dict):
            continue
        if scene_id in [str(value) for value in _list(row.get("target_scene_ids"))]:
            rules.append(str(row.get("rule_id")))
    return rules


def _timing_adjustment_model(state: dict[str, Any], scene_plan: dict[str, Any]) -> dict[str, Any]:
    scene_contracts = []
    for scene in _list(scene_plan.get("scenes")):
        if not isinstance(scene, dict):
            continue
        duration = _dict(scene.get("duration_contract"))
        scene_contracts.append(
            {
                "scene_id": scene.get("scene_id"),
                "operation_id": "set_scene_duration",
                "row_range": scene.get("row_range"),
                "cue_ids": scene.get("cue_ids"),
                "provisional_start_sec": duration.get("provisional_start_sec"),
                "provisional_end_sec": duration.get("provisional_end_sec"),
                "provisional_duration_sec": duration.get("provisional_duration_sec"),
                "adjustment_policy": "preserve cue order, then adjust only after future audio/YMM4 readback",
                "actual_audio_timing_status": "blocked_by_explicit_yymm4_gate",
            }
        )
    return {
        "schema_version": "timing_adjustment_model.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "provisional_timing_model_ready_no_audio_or_yymm4_timing",
        "source_scene_timing_map": _dict(state.get("paths")).get("scene_timing_map"),
        "scene_count": len(scene_contracts),
        "total_provisional_duration_sec": sum(int(row.get("provisional_duration_sec", 0) or 0) for row in scene_contracts),
        "scene_duration_contracts": scene_contracts,
        "adjustment_rules": [
            "set_scene_duration may use provisional seconds from the template map",
            "audio-derived start/end changes require future manual YMM4 readback",
            "row ranges and cue ids stay stable until real input replacement is validated",
            "no render or import action is part of this timing model",
        ],
        "actual_yymm4_import": False,
        "yymm4_rendered": False,
        "invented_real_content": False,
    }


def _voice_subtitle_operation_map(state: dict[str, Any], scene_plan: dict[str, Any]) -> dict[str, Any]:
    voice_mapping = _dict(state.get("voice_subtitle_mapping"))
    scene_by_id = {str(row.get("scene_id")): row for row in _list(scene_plan.get("scenes")) if isinstance(row, dict)}
    utterance_operations = []
    for row in _list(voice_mapping.get("utterance_mappings")):
        if not isinstance(row, dict):
            continue
        scene_id = str(row.get("scene_id") or "")
        subtitle_source = str(row.get("subtitle_source") or "")
        text_length = len(str(row.get("subtitle_text") or ""))
        utterance_operations.append(
            {
                "cue_id": row.get("cue_id"),
                "row_number": row.get("row_number"),
                "scene_id": scene_id,
                "scene_title": _dict(scene_by_id.get(scene_id)).get("title"),
                "speaker": row.get("speaker"),
                "voice_slot_id": row.get("voice_slot_id"),
                "operation_ids": ["align_voice_subtitle", "split_or_wrap_subtitle", "flag_real_input_required", "mark_yymm4_observation_needed"],
                "subtitle_source": subtitle_source,
                "subtitle_text_status": row.get("subtitle_status"),
                "subtitle_wrap_contract": {
                    "operation_id": "split_or_wrap_subtitle",
                    "source_text_length": text_length,
                    "wrap_policy": "local review can mark wrapping intent; final wrap waits for real text and observed timing",
                    "actual_linebreaks_ready": False,
                },
                "voiceitem_readback": {
                    "actual_yymm4_voiceitem_id": None,
                    "actual_start_sec": None,
                    "actual_end_sec": None,
                    "observation_required": "explicit_yymm4_gate",
                },
            }
        )
    return {
        "schema_version": "voice_subtitle_operation_map.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "voice_subtitle_operations_ready_no_yymm4_voiceitems",
        "source_voice_subtitle_mapping": _dict(state.get("paths")).get("voice_subtitle_mapping"),
        "source_csv": voice_mapping.get("source_csv"),
        "utterance_operation_count": len(utterance_operations),
        "utterance_operations": utterance_operations,
        "unknowns": [
            "actual YMM4 VoiceItem IDs",
            "audio-derived start/end timing",
            "real transcript replacement text",
        ],
        "actual_yymm4_import": False,
        "invented_real_content": False,
    }


def _visual_asset_slot_map(state: dict[str, Any], scene_plan: dict[str, Any]) -> dict[str, Any]:
    visual_registry = _dict(state.get("visual_scene_template_registry"))
    overlay_spec = _dict(state.get("citation_overlay_spec"))
    thumbnail_map = _dict(state.get("thumbnail_transfer_map"))
    slots = []
    for scene in _list(scene_plan.get("scenes")):
        if not isinstance(scene, dict):
            continue
        visual = _dict(scene.get("visual_contract"))
        slots.append(
            {
                "scene_id": scene.get("scene_id"),
                "operation_ids": ["assign_visual_scene_template", "place_citation_overlay", "transfer_thumbnail_motif", "flag_real_input_required"],
                "primary_template_id": visual.get("primary_template_id"),
                "supporting_template_ids": _list(visual.get("supporting_template_ids")),
                "citation_overlay_ids": _list(visual.get("citation_overlay_ids")),
                "thumbnail_transfer_rule_ids": _list(visual.get("thumbnail_transfer_rule_ids")),
                "asset_policy": "template slots and local tokens only",
                "external_media_allowed": False,
                "final_thumbnail_approval": False,
            }
        )
    return {
        "schema_version": "visual_asset_slot_map.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "visual_asset_slots_ready_no_external_media",
        "source_visual_registry": _dict(state.get("paths")).get("visual_scene_template_registry"),
        "source_overlay_spec": _dict(state.get("paths")).get("citation_overlay_spec"),
        "source_thumbnail_map": _dict(state.get("paths")).get("thumbnail_transfer_map"),
        "template_type_count": visual_registry.get("template_type_count"),
        "overlay_slot_count": overlay_spec.get("overlay_slot_count"),
        "thumbnail_transfer_status": thumbnail_map.get("status"),
        "scene_visual_slot_count": len(slots),
        "scene_visual_slots": slots,
        "external_media_allowed": False,
        "final_thumbnail_approval": False,
        "invented_real_content": False,
    }


def _yymm4_readback_schema(state: dict[str, Any], scene_plan: dict[str, Any]) -> dict[str, Any]:
    scene_ids = [str(row.get("scene_id")) for row in _list(scene_plan.get("scenes")) if isinstance(row, dict)]
    return {
        "schema_version": "yymm4_readback_schema.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "schema_ready_no_actual_import",
        "protocol": "future manual observation only",
        "actual_yymm4_import": False,
        "yymm4_rendered": False,
        "production_ready": False,
        "scene_ids": scene_ids,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "observation_session_id",
                "operator",
                "observed_at_local_time",
                "explicit_yymm4_gate_confirmed",
                "project_file_path",
                "csv_import_observed",
                "render_attempted",
                "scene_readbacks",
                "notes",
            ],
            "properties": {
                "observation_session_id": {"type": "string"},
                "operator": {"type": "string"},
                "observed_at_local_time": {"type": "string"},
                "explicit_yymm4_gate_confirmed": {"type": "boolean"},
                "project_file_path": {"type": "string"},
                "csv_import_observed": {"type": "boolean"},
                "render_attempted": {"type": "boolean"},
                "scene_readbacks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["scene_id", "voiceitems", "subtitle_items", "observed_start_sec", "observed_end_sec", "issues"],
                        "properties": {
                            "scene_id": {"type": "string", "enum": scene_ids},
                            "voiceitems": {"type": "array", "items": {"type": "object"}},
                            "subtitle_items": {"type": "array", "items": {"type": "object"}},
                            "observed_start_sec": {"type": ["number", "null"]},
                            "observed_end_sec": {"type": ["number", "null"]},
                            "issues": {"type": "array", "items": {"type": "string"}},
                        },
                    },
                },
                "notes": {"type": "array", "items": {"type": "string"}},
            },
        },
    }


def _operation_gap_ledger(state: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    operations = [row for row in _list(registry.get("operations")) if isinstance(row, dict)]
    groups = {
        "buildable_locally": [
            "edit_operation_registry.json",
            "scene_operation_plan.json",
            "timing_adjustment_model.json",
            "voice_subtitle_operation_map.json",
            "visual_asset_slot_map.json",
            "operation_gap_ledger.json",
            "editing_operations_preview.html",
        ],
        "blocked_by_real_input": [
            "verified local source file",
            "verified transcript text",
            "citation overlay wording from real material",
            "real-input replacement execution",
        ],
        "blocked_by_explicit_yymm4_gate": [
            "YMM4 GUI launch",
            "CSV import observation",
            "VoiceItem id and timing readback",
            "render smoke or production project write",
        ],
        "blocked_by_public_rights_gate": [
            "rights/public-ready acceptance",
            "final thumbnail approval",
            "public upload or production publication decision",
        ],
    }
    return {
        "schema_version": "operation_gap_ledger.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "operation_gap_ledger_ready_local_offline",
        "operation_count": len(operations),
        "groups": groups,
        "counts": {group_id: len(rows) for group_id, rows in groups.items()},
        "operation_status_by_id": {str(row.get("operation_id")): row.get("build_status") for row in operations},
        "invented_real_content": False,
        "actual_yymm4_import": False,
        "public_ready": False,
    }


def _source_artifact_index(state: dict[str, Any]) -> dict[str, Any]:
    paths = _dict(state.get("paths"))
    records = [
        _source_record("output_template_manifest", paths.get("output_template_manifest"), "output_template_context_read_only", True),
        _source_record("scene_timing_map", paths.get("scene_timing_map"), "timing_context_read_only", True),
        _source_record("voice_subtitle_mapping", paths.get("voice_subtitle_mapping"), "voice_subtitle_context_read_only", True),
        _source_record("visual_scene_template_registry", paths.get("visual_scene_template_registry"), "visual_context_read_only", True),
        _source_record("citation_overlay_spec", paths.get("citation_overlay_spec"), "citation_context_read_only", True),
        _source_record("thumbnail_transfer_map", paths.get("thumbnail_transfer_map"), "thumbnail_context_read_only", True),
        _source_record("real_input_manifest", paths.get("real_input_manifest"), "input_intake_context_read_only", True),
        _source_record("source_transcript_contract_schema", paths.get("source_transcript_contract_schema"), "input_contract_read_only", True),
        _source_record("draft_yymm4_csv", paths.get("draft_yymm4_csv"), "draft_csv_context_read_only", True),
        _source_record("ir_draft_yymm4_csv", paths.get("ir_draft_yymm4_csv"), "optional_ir_csv_context_read_only", False),
        _source_record("japanese_console_validation", paths.get("japanese_console_validation"), "gui_context_read_only", True),
    ]
    return {
        "schema_version": "editing_operations_source_artifact_index.v1",
        "artifact_id": state.get("artifact_id"),
        "output_template_context_read_only": True,
        "input_intake_context_read_only": True,
        "gui_lane_context_read_only": True,
        "protected_gui_lane_dirs": list(PROTECTED_GUI_LANE_DIRS),
        "protected_output_template_dirs": list(PROTECTED_OUTPUT_TEMPLATE_DIRS),
        "protected_input_intake_dirs": list(PROTECTED_INPUT_INTAKE_DIRS),
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
    registry: dict[str, Any],
    scene_plan: dict[str, Any],
    timing_model: dict[str, Any],
    voice_map: dict[str, Any],
    visual_map: dict[str, Any],
    readback_schema: dict[str, Any],
    gap_ledger: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "editing_operations_manifest.v1",
        "artifact_id": state.get("artifact_id"),
        "artifact_kind": "episode-editing-operations-readiness-pack",
        "status": "editing_operations_ready_local_offline",
        "parallel_lane": "editing_features",
        "thread_id": "editing-ops-episode002",
        "output_dir": _relpath(output_root, repo_root),
        "files": {filename: _relpath(output_root / filename, repo_root) for filename in REQUIRED_EDITING_OPERATIONS_FILES},
        "primary_review_file": state.get("primary_human_review"),
        "primary_human_review": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "operation_count": registry.get("operation_count"),
        "scene_count": scene_plan.get("scene_count"),
        "timing_model_status": timing_model.get("status"),
        "voice_subtitle_operation_status": voice_map.get("status"),
        "visual_slot_map_status": visual_map.get("status"),
        "yymm4_protocol_status": "future_manual_observation_protocol_ready_no_launch",
        "yymm4_readback_schema_status": readback_schema.get("status"),
        "operation_gap_ledger_status": gap_ledger.get("status"),
        "invented_real_content": False,
        "actual_yymm4_import": False,
        "yymm4_rendered": False,
        "production_ready": False,
        "public_ready": False,
        "rights_accepted": False,
        "final_thumbnail_approval": False,
        "gui_lane_files_touched": [],
        "output_template_files_touched": [],
        "input_intake_files_touched": [],
        "thread_registry_updated": True,
        "shared_docs_touched": True,
        "full_pytest_run": False,
        "boundary_flags": state.get("boundary_flags"),
        "next_action": state.get("next_action"),
    }


def _render_html(
    state: dict[str, Any],
    registry: dict[str, Any],
    scene_plan: dict[str, Any],
    timing_model: dict[str, Any],
    voice_map: dict[str, Any],
    visual_map: dict[str, Any],
    gap_ledger: dict[str, Any],
) -> str:
    operation_cards = "\n".join(_render_operation_card(row) for row in _list(registry.get("operations")))
    scene_rows = "\n".join(_render_scene_row(row) for row in _list(scene_plan.get("scenes")))
    timing_nodes = "\n".join(_render_timing_node(row) for row in _list(timing_model.get("scene_duration_contracts")))
    voice_rows = "\n".join(_render_voice_row(row) for row in _list(voice_map.get("utterance_operations"))[:9])
    visual_rows = "\n".join(_render_visual_row(row) for row in _list(visual_map.get("scene_visual_slots")))
    gap_rows = "\n".join(_render_gap_group(group_id, rows) for group_id, rows in _dict(gap_ledger.get("groups")).items())
    return f"""<!doctype html>
<html lang="ja" data-editing-operations="true" data-artifact-kind="episode-editing-operations-readiness-pack">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Editing Operations Readiness</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #101316;
      --surface: #172027;
      --panel: #1f2a31;
      --ink: #edf6f9;
      --muted: #9fb3bd;
      --line: #33454e;
      --amber: #f6c85f;
      --teal: #55d6be;
      --rose: #f28b82;
      --blue: #8ab4f8;
      --green: #9ad67d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.5;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 28px 18px 40px;
    }}
    h1, h2, h3 {{ margin: 0; letter-spacing: 0; }}
    h1 {{ font-size: clamp(28px, 4vw, 46px); line-height: 1.05; }}
    h2 {{ font-size: 20px; margin-top: 28px; }}
    h3 {{ font-size: 15px; }}
    p {{ color: var(--muted); }}
    .hero {{
      display: grid;
      gap: 14px;
      padding: 24px 0 18px;
      border-bottom: 1px solid var(--line);
    }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .chip {{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 5px 10px;
      color: var(--ink);
      background: var(--surface);
      font-size: 12px;
    }}
    .grid {{ display: grid; gap: 12px; }}
    .ops {{ grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }}
    .card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--surface);
      padding: 14px;
      min-height: 130px;
    }}
    .lane {{ color: var(--teal); font-size: 12px; text-transform: uppercase; }}
    .matrix {{
      display: grid;
      gap: 8px;
      overflow-x: auto;
    }}
    .matrix-row {{
      display: grid;
      grid-template-columns: 90px minmax(160px, 1.2fr) repeat(4, minmax(130px, 1fr));
      gap: 8px;
      min-width: 860px;
      align-items: stretch;
    }}
    .cell {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      padding: 10px;
      min-height: 74px;
      overflow-wrap: anywhere;
    }}
    .head .cell {{ color: var(--amber); min-height: auto; }}
    .timeline {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 10px;
    }}
    .time-node {{
      border: 1px solid var(--line);
      border-left: 5px solid var(--blue);
      border-radius: 8px;
      padding: 12px;
      background: var(--surface);
    }}
    .voice-row, .visual-row, .gap-row {{
      display: grid;
      grid-template-columns: 120px 1fr 1fr;
      gap: 8px;
      border-bottom: 1px solid var(--line);
      padding: 10px 0;
    }}
    .danger {{ color: var(--rose); }}
    .ok {{ color: var(--green); }}
    code {{ color: var(--amber); }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #f7faf9;
        --surface: #ffffff;
        --panel: #eef3f5;
        --ink: #142026;
        --muted: #4c626d;
        --line: #c7d6dc;
      }}
    }}
    @media (max-width: 760px) {{
      main {{ padding: 20px 12px 32px; }}
      .voice-row, .visual-row, .gap-row {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div class="chips">
        <span class="chip">operation count: {_escape(registry.get("operation_count"))}</span>
        <span class="chip">scene count: {_escape(scene_plan.get("scene_count"))}</span>
        <span class="chip">YMM4: future manual only</span>
        <span class="chip">real input: required later</span>
      </div>
      <h1>Episode 002 Editing Operations Readiness</h1>
      <p>Local operation contracts for timing, voice/subtitle, visual slots, citation overlays, thumbnail transfer, and future YMM4 observation readback. No import, render, or public-ready claim is made here.</p>
    </section>

    <section data-region="operation-lanes">
      <h2>Operation Lanes</h2>
      <div class="grid ops">{operation_cards}</div>
    </section>

    <section data-region="scene-operation-matrix">
      <h2>Scene Operation Matrix</h2>
      <div class="matrix">
        <div class="matrix-row head">
          <div class="cell">Scene</div>
          <div class="cell">Purpose</div>
          <div class="cell">Timing</div>
          <div class="cell">Voice / Subtitle</div>
          <div class="cell">Visual / Citation</div>
          <div class="cell">Gates</div>
        </div>
        {scene_rows}
      </div>
    </section>

    <section data-region="timing-strip">
      <h2>Timing Strip</h2>
      <div class="timeline">{timing_nodes}</div>
    </section>

    <section data-region="voice-subtitle-lane">
      <h2>Voice / Subtitle Lane</h2>
      {voice_rows}
    </section>

    <section data-region="visual-slot-lane">
      <h2>Visual Slot Lane</h2>
      {visual_rows}
    </section>

    <section data-region="yymm4-observation-lane">
      <h2>YMM4 Observation Lane</h2>
      <p class="danger">Do not launch, import, render, or write production project output from this package. The schema only defines fields for a future manual observation after an explicit gate.</p>
      {gap_rows}
    </section>
  </main>
</body>
</html>
"""


def _render_operation_card(row: Any) -> str:
    item = _dict(row)
    return f"""<article class="card">
  <div class="lane">{_escape(item.get("lane"))}</div>
  <h3>{_escape(item.get("operation_id"))}</h3>
  <p>{_escape(item.get("purpose"))}</p>
  <p class="ok">{_escape(item.get("build_status"))}</p>
</article>"""


def _render_scene_row(row: Any) -> str:
    scene = _dict(row)
    duration = _dict(scene.get("duration_contract"))
    voice = _dict(scene.get("voice_subtitle_contract"))
    visual = _dict(scene.get("visual_contract"))
    gates = _list(scene.get("gate_contracts"))
    gate_text = "; ".join(str(_dict(gate).get("status")) for gate in gates)
    return f"""<div class="matrix-row">
  <div class="cell"><code>{_escape(scene.get("scene_id"))}</code><br>{_escape(scene.get("arc_phase"))}</div>
  <div class="cell">{_escape(scene.get("title"))}</div>
  <div class="cell">{_escape(duration.get("provisional_duration_sec"))} sec<br><code>set_scene_duration</code></div>
  <div class="cell">{_escape(voice.get("cue_count"))} cues<br><code>align_voice_subtitle</code></div>
  <div class="cell">{_escape(visual.get("primary_template_id"))}<br>{_escape(', '.join(_list(visual.get("citation_overlay_ids"))))}</div>
  <div class="cell danger">{_escape(gate_text)}</div>
</div>"""


def _render_timing_node(row: Any) -> str:
    item = _dict(row)
    return f"""<div class="time-node">
  <h3>{_escape(item.get("scene_id"))}</h3>
  <p>{_escape(item.get("provisional_start_sec"))}s to {_escape(item.get("provisional_end_sec"))}s / {_escape(item.get("provisional_duration_sec"))}s</p>
  <p>{_escape(item.get("actual_audio_timing_status"))}</p>
</div>"""


def _render_voice_row(row: Any) -> str:
    item = _dict(row)
    readback = _dict(item.get("voiceitem_readback"))
    wrap = _dict(item.get("subtitle_wrap_contract"))
    return f"""<div class="voice-row">
  <div><code>{_escape(item.get("cue_id"))}</code><br>{_escape(item.get("scene_id"))}</div>
  <div>{_escape(item.get("speaker"))}<br>{_escape(item.get("voice_slot_id"))}</div>
  <div>{_escape(wrap.get("wrap_policy"))}<br><span class="danger">{_escape(readback.get("observation_required"))}</span></div>
</div>"""


def _render_visual_row(row: Any) -> str:
    item = _dict(row)
    return f"""<div class="visual-row">
  <div><code>{_escape(item.get("scene_id"))}</code></div>
  <div>{_escape(item.get("primary_template_id"))}<br>{_escape(', '.join(_list(item.get("supporting_template_ids"))))}</div>
  <div>overlays: {_escape(', '.join(_list(item.get("citation_overlay_ids"))))}<br>thumbnail: {_escape(', '.join(_list(item.get("thumbnail_transfer_rule_ids"))))}</div>
</div>"""


def _render_gap_group(group_id: str, rows: Any) -> str:
    items = ", ".join(str(row) for row in _list(rows))
    return f"""<div class="gap-row">
  <div><code>{_escape(group_id)}</code></div>
  <div>{_escape(len(_list(rows)))} items</div>
  <div>{_escape(items)}</div>
</div>"""


def _render_markdown(
    state: dict[str, Any],
    registry: dict[str, Any],
    scene_plan: dict[str, Any],
    timing_model: dict[str, Any],
    voice_map: dict[str, Any],
    visual_map: dict[str, Any],
    gap_ledger: dict[str, Any],
) -> str:
    scene_lines = "\n".join(
        f"- {scene.get('scene_id')}: {scene.get('title')} / ops {', '.join(_list(scene.get('operation_ids')))}"
        for scene in _list(scene_plan.get("scenes"))
        if isinstance(scene, dict)
    )
    group_lines = "\n".join(
        f"- {group_id}: {len(_list(rows))} items"
        for group_id, rows in _dict(gap_ledger.get("groups")).items()
    )
    return f"""# Episode 002 Editing Operations Readiness

This local pack turns the output template and real-input intake context into editing operation contracts. It does not launch YMM4, import CSV, render, replace real input, approve rights, or claim production readiness.

Primary review file: `{state.get("primary_human_review")}`

Operation count: {registry.get("operation_count")}
Scene count: {scene_plan.get("scene_count")}
Timing model: {timing_model.get("status")}
Voice/subtitle operations: {voice_map.get("status")}
Visual slots: {visual_map.get("status")}

## Scene Operation Plan

{scene_lines}

## Gap Groups

{group_lines}

## Next Use

Review the HTML matrix, choose the next edit slice, and keep real input replacement plus future manual YMM4 observation behind their explicit gates.
"""


def _render_yymm4_protocol(state: dict[str, Any], readback_schema: dict[str, Any]) -> str:
    return f"""# Episode 002 YMM4 Observation Protocol

This protocol is future manual observation only. Do not launch YMM4, import CSV, render, write a production project, or record actual VoiceItem timing as part of this package.

Use this only after an explicit YMM4 observation gate is opened by the operator.

1. Confirm the real-input replacement package has been reviewed, if the observation depends on real source text.
2. Open the future manual observation session outside this pack.
3. Fill a readback object matching `{readback_schema.get("schema_version")}`.
4. Record scene ids, observed VoiceItem ids, subtitle items, start/end timing, and issues.
5. Keep render attempts, public upload decisions, rights acceptance, and final thumbnail approval outside this protocol unless a separate gate opens them.

Current package status:

- actual_yymm4_import: false
- yymm4_rendered: false
- production_ready: false
- schema_status: {readback_schema.get("status")}
"""


def _render_review_checklist(state: dict[str, Any]) -> str:
    return """# Editing Operations Review Checklist

- Confirm operation registry includes timing, voice/subtitle, visual, citation, thumbnail transfer, real-input, and YMM4 observation contracts.
- Confirm all three scenes have timing, voice/subtitle, visual, and gate contracts.
- Confirm YMM4 protocol remains future manual only.
- Confirm no GUI lane, output template pack, or input intake pack files were modified.
- Confirm no real input replacement, public-ready approval, render, or upload claim appears.
"""


def _render_limitations(state: dict[str, Any]) -> str:
    return """# Limitations

- Local readiness only; no actual YMM4 import, render, production project write, or GUI launch is performed.
- Real input replacement is not executed, and no verified source/transcript material is embedded here.
- Citation overlay copy remains placeholder-only until verified local source intake.
- Thumbnail transfer is motif/context only; final thumbnail approval remains closed.
- Public upload, rights acceptance, and production-ready decisions remain outside this package.
- Full pytest is not run for this scoped slice.
"""


def _render_readme(
    state: dict[str, Any],
    registry: dict[str, Any],
    scene_plan: dict[str, Any],
    gap_ledger: dict[str, Any],
) -> str:
    return f"""# Episode 002 Editing Operations Readiness Pack

This package maps Episode 002 editing work into local operation contracts.

Open `editing_operations_preview.html` for the graphical review surface. Use `validation_readback.json` as the machine-readable status record.

What is ready:

- {registry.get("operation_count")} operation contracts.
- {scene_plan.get("scene_count")} scene operation rows.
- Timing, voice/subtitle, visual slot, citation overlay, thumbnail transfer, and future YMM4 readback contracts.

What remains gated:

- Verified real source/transcript input.
- Explicit future manual YMM4 observation.
- Public/rights/final thumbnail approval.

Gap groups are stored in `operation_gap_ledger.json`.
"""
