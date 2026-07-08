"""YMM4 import-ready package for episode 002."""

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

DEFAULT_OUTPUT_DIRNAME = "ymm4_import_ready_pack"
DEFAULT_ARTIFACT_ID = "nlm-e002-ymm4-import-ready-edit-package-v1-001"
SOURCE_EPISODE_ID = "yukkuri_newsroom_content_spine_002"

LOCAL_EDIT_DIRNAME = "local_edit_slice_execution_pack"
EDITING_OPERATIONS_DIRNAME = "editing_operations_readiness_pack"

REQUIRED_YMM4_IMPORT_READY_FILES = (
    "ymm4_import_ready_manifest.json",
    "edit_slice_to_ymm4_cue_map.json",
    "manual_ymm4_import_observation_sheet.md",
    "ymm4_import_ready_preview.html",
    "validation_readback.json",
    "gate_readback.json",
    "source_artifact_index.json",
    "ymmp_adapter_plan.json",
    "README_YMM4_IMPORT_READY.md",
    "limitations.md",
)

REQUIRED_CUE_FIELDS = (
    "cue_id",
    "source_scene_id",
    "approximate_timing",
    "voice_or_subtitle_action",
    "visual_action",
    "overlay_or_citation_action",
    "expected_yymm4_layer_or_track",
    "required_asset_state",
    "import_risk",
    "manual_observation_question",
)

FORBIDDEN_GATE_FLAGS = (
    "actual_ymm4_imported",
    "actual_yymm4_import",
    "rendered_video_created",
    "yymm4_rendered",
    "production_ymmp_written",
    "real_input_replaced",
    "real_input_replacement_executed",
    "rights_approved",
    "rights_accepted",
    "public_ready",
    "final_thumbnail_approval",
    "youtube_uploaded",
)


def build_ymm4_import_ready_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build an import-ready package for future manual YMM4 observation."""
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
    cue_map = _cue_map(state)
    gate_readback = _gate_readback(state, cue_map)
    adapter_plan = _ymmp_adapter_plan(state, cue_map)
    source_index = _source_artifact_index(state)
    manifest = _manifest(state, cue_map, gate_readback, adapter_plan, output_root, repo_root)

    _write_json(output_root / "ymm4_import_ready_manifest.json", manifest)
    _write_json(output_root / "edit_slice_to_ymm4_cue_map.json", cue_map)
    _write_json(output_root / "gate_readback.json", gate_readback)
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_json(output_root / "ymmp_adapter_plan.json", adapter_plan)
    _write_text(output_root / "manual_ymm4_import_observation_sheet.md", _render_observation_sheet(state, cue_map, gate_readback))
    _write_text(output_root / "ymm4_import_ready_preview.html", _render_html(state, manifest, cue_map, gate_readback))
    _write_text(output_root / "README_YMM4_IMPORT_READY.md", _render_readme(state, manifest, cue_map, gate_readback))
    _write_text(output_root / "limitations.md", _render_limitations())

    readback = validate_ymm4_import_ready_pack(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_ymm4_import_ready_pack(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_ymm4_import_ready_pack(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate a generated YMM4 import-ready package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_YMM4_IMPORT_READY_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["ymm4_import_ready_manifest.json"])
    cue_map = _load_json_if_present(files["edit_slice_to_ymm4_cue_map.json"])
    gate_readback = _load_json_if_present(files["gate_readback.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])
    adapter_plan = _load_json_if_present(files["ymmp_adapter_plan.json"])
    json_payloads = {
        "manifest": manifest,
        "cue_map": cue_map,
        "gate_readback": gate_readback,
        "source_index": source_index,
        "adapter_plan": adapter_plan,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = _dict(json_payloads["manifest"])
    cue_map = _dict(json_payloads["cue_map"])
    gate_readback = _dict(json_payloads["gate_readback"])
    source_index = _dict(json_payloads["source_index"])
    adapter_plan = _dict(json_payloads["adapter_plan"])

    html_text = files["ymm4_import_ready_preview.html"].read_text(encoding="utf-8") if files["ymm4_import_ready_preview.html"].exists() else ""
    sheet_text = files["manual_ymm4_import_observation_sheet.md"].read_text(encoding="utf-8") if files["manual_ymm4_import_observation_sheet.md"].exists() else ""
    limitations_text = files["limitations.md"].read_text(encoding="utf-8") if files["limitations.md"].exists() else ""

    cues = [row for row in _list(cue_map.get("cues")) if isinstance(row, dict)]
    scenes = [row for row in _list(cue_map.get("scene_summaries")) if isinstance(row, dict)]
    gate_flags = _dict(gate_readback.get("closed_gate_flags"))
    observation_checks = [line for line in sheet_text.splitlines() if line.strip().startswith(tuple(f"{idx}." for idx in range(1, 10)))]

    if manifest.get("artifact_id") != DEFAULT_ARTIFACT_ID:
        failed_checks.append("manifest_artifact_id_mismatch")
    if manifest.get("artifact_kind") != "episode-ymm4-import-ready-edit-package":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("source_episode_id") != SOURCE_EPISODE_ID:
        failed_checks.append("manifest_source_episode_id_mismatch")
    if manifest.get("ymm4_import_state") != "ready_for_manual_import_observation":
        failed_checks.append("manifest_import_state_mismatch")
    for flag in (
        "actual_ymm4_imported",
        "rendered_video_created",
        "real_input_replaced",
        "rights_approved",
        "public_ready",
    ):
        if manifest.get(flag) is not False:
            failed_checks.append(f"manifest_gate_not_false:{flag}")
    if manifest.get("gates_closed") is not True:
        failed_checks.append("manifest_gates_not_closed")
    if manifest.get("cue_count") != len(cues):
        failed_checks.append("manifest_cue_count_mismatch")
    if manifest.get("scene_count") != len(scenes):
        failed_checks.append("manifest_scene_count_mismatch")
    if len(cues) < 1:
        failed_checks.append("cue_map_empty")
    for cue in cues:
        for field in REQUIRED_CUE_FIELDS:
            if field not in cue:
                failed_checks.append(f"cue_field_missing:{field}")
        if cue.get("required_asset_state") not in {"placeholder", "diagnostic", "real_required_later"}:
            failed_checks.append(f"cue_asset_state_invalid:{cue.get('cue_id')}")
    if gate_readback.get("status") != "ymm4_import_gates_closed":
        failed_checks.append("gate_readback_status_mismatch")
    if gate_readback.get("gates_closed") is not True:
        failed_checks.append("gate_readback_gates_not_closed")
    for flag_name in FORBIDDEN_GATE_FLAGS:
        if gate_flags.get(flag_name) is not False:
            failed_checks.append(f"gate_flag_not_false:{flag_name}")
    if adapter_plan.get("status") != "adapter_plan_ready_no_ymmp_write":
        failed_checks.append("adapter_plan_status_mismatch")
    if adapter_plan.get("ymmp_file_created") is not False:
        failed_checks.append("adapter_plan_created_ymmp")
    if source_index.get("local_edit_pack_read_only") is not True:
        failed_checks.append("local_edit_pack_not_read_only")
    if "data-ymm4-import-ready=\"true\"" not in html_text:
        failed_checks.append("html_missing_import_ready_marker")
    if "data-region=\"cue-map\"" not in html_text:
        failed_checks.append("html_missing_cue_map")
    if "card-grid" in html_text or "data-region=\"card-grid\"" in html_text:
        failed_checks.append("html_card_grid_marker_found")
    if len(observation_checks) > 5:
        failed_checks.append("observation_sheet_too_many_checks")
    if "Do not launch YMM4" not in limitations_text:
        failed_checks.append("limitations_missing_yymm4_stop")

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
        "schema_version": "ymm4_import_ready_validation_readback.v1",
        "status": status,
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(
                path.exists() for name, path in files.items() if name != "validation_readback.json" or require_readback
            ),
            "json_loads": all(isinstance(payload, dict) for payload in json_payloads.values()),
            "html_preview_exists": files["ymm4_import_ready_preview.html"].exists(),
            "manual_observation_sheet_exists": files["manual_ymm4_import_observation_sheet.md"].exists(),
            "cue_count": len(cues),
            "scene_count": len(scenes),
            "observation_check_count": len(observation_checks),
            "gates_closed": gate_readback.get("gates_closed"),
            "closed_gate_flags": gate_flags,
            "ymmp_file_created": adapter_plan.get("ymmp_file_created"),
            "local_edit_pack_read_only": source_index.get("local_edit_pack_read_only"),
            "external_dependency_status": "none_found" if not external_refs else external_refs,
            "forbidden_true_claims_absent": not forbidden_claims,
            "temporary_copy_absent": not temporary_hits,
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "primary_review_file": str(root / "ymm4_import_ready_preview.html"),
        "primary_human_review": str(root / "ymm4_import_ready_preview.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "queue_count": manifest.get("queue_count"),
        "scene_count": len(scenes),
        "cue_count": len(cues),
        "ymm4_import_state": manifest.get("ymm4_import_state"),
        "actual_ymm4_imported": manifest.get("actual_ymm4_imported"),
        "rendered_video_created": manifest.get("rendered_video_created"),
        "real_input_replaced": manifest.get("real_input_replaced"),
        "rights_approved": manifest.get("rights_approved"),
        "public_ready": manifest.get("public_ready"),
        "gates_closed": manifest.get("gates_closed"),
        "full_pytest_run": False,
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{(root / "ymm4_import_ready_preview.html").resolve()}"',
        "access_state": "verified_present" if (root / "ymm4_import_ready_preview.html").exists() else "missing",
        "next_action": manifest.get("next_action"),
    }


def _input_paths(source_root: Path) -> dict[str, Path]:
    local_root = source_root / LOCAL_EDIT_DIRNAME
    editing_root = source_root / EDITING_OPERATIONS_DIRNAME
    return {
        "local_edit_root": local_root,
        "local_edit_manifest": local_root / "local_edit_slice_manifest.json",
        "local_edit_queue": local_root / "local_edit_slice_queue.json",
        "local_scene_plan": local_root / "scene_edit_execution_plan.json",
        "local_gate_readback": local_root / "operation_gate_preservation_readback.json",
        "local_validation": local_root / "validation_readback.json",
        "editing_root": editing_root,
        "voice_subtitle_operation_map": editing_root / "voice_subtitle_operation_map.json",
        "visual_asset_slot_map": editing_root / "visual_asset_slot_map.json",
        "timing_adjustment_model": editing_root / "timing_adjustment_model.json",
        "operation_gap_ledger": editing_root / "operation_gap_ledger.json",
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "local_edit_manifest": _load_json_if_present(paths["local_edit_manifest"]),
        "local_edit_queue": _load_json_if_present(paths["local_edit_queue"]),
        "local_scene_plan": _load_json_if_present(paths["local_scene_plan"]),
        "local_gate_readback": _load_json_if_present(paths["local_gate_readback"]),
        "local_validation": _load_json_if_present(paths["local_validation"]),
        "voice_subtitle_operation_map": _load_json_if_present(paths["voice_subtitle_operation_map"]),
        "visual_asset_slot_map": _load_json_if_present(paths["visual_asset_slot_map"]),
        "timing_adjustment_model": _load_json_if_present(paths["timing_adjustment_model"]),
        "operation_gap_ledger": _load_json_if_present(paths["operation_gap_ledger"]),
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
        "schema_version": "ymm4_import_ready_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-ymm4-import-ready-edit-package",
        "source_episode_id": SOURCE_EPISODE_ID,
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "repo_root": str(repo_root),
        "paths": {name: _relpath(path, repo_root) for name, path in paths.items()},
        "local_edit_manifest": _dict(payloads.get("local_edit_manifest")),
        "local_edit_queue": _dict(payloads.get("local_edit_queue")),
        "local_scene_plan": _dict(payloads.get("local_scene_plan")),
        "local_gate_readback": _dict(payloads.get("local_gate_readback")),
        "local_validation": _dict(payloads.get("local_validation")),
        "voice_subtitle_operation_map": _dict(payloads.get("voice_subtitle_operation_map")),
        "visual_asset_slot_map": _dict(payloads.get("visual_asset_slot_map")),
        "timing_adjustment_model": _dict(payloads.get("timing_adjustment_model")),
        "operation_gap_ledger": _dict(payloads.get("operation_gap_ledger")),
        "primary_human_review": _relpath(output_root / "ymm4_import_ready_preview.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_action": "Use the preview and observation sheet for a future explicit YMM4 import observation; do not import, render, replace real input, or publish from this package.",
    }


def _cue_map(state: dict[str, Any]) -> dict[str, Any]:
    voice_map = _dict(state.get("voice_subtitle_operation_map"))
    visual_map = _dict(state.get("visual_asset_slot_map"))
    timing_model = _dict(state.get("timing_adjustment_model"))
    local_queue = _dict(state.get("local_edit_queue"))

    visual_by_scene = {
        str(row.get("scene_id")): row
        for row in _list(visual_map.get("scene_visual_slots"))
        if isinstance(row, dict)
    }
    duration_by_scene = {
        str(row.get("scene_id")): row
        for row in _list(timing_model.get("scene_duration_contracts"))
        if isinstance(row, dict)
    }
    voice_rows_by_scene: dict[str, list[dict[str, Any]]] = {}
    for row in _list(voice_map.get("utterance_operations")):
        if isinstance(row, dict):
            voice_rows_by_scene.setdefault(str(row.get("scene_id")), []).append(row)

    cues = []
    for scene_id, rows in voice_rows_by_scene.items():
        duration = _dict(duration_by_scene.get(scene_id))
        visual = _dict(visual_by_scene.get(scene_id))
        row_count = max(len(rows), 1)
        scene_start = float(duration.get("provisional_start_sec") or 0)
        scene_end = float(duration.get("provisional_end_sec") or scene_start)
        scene_duration = max(scene_end - scene_start, 0.0)
        cue_duration = scene_duration / row_count if row_count else 0.0
        for index, row in enumerate(rows):
            approx_start = scene_start + cue_duration * index
            approx_end = scene_start + cue_duration * (index + 1)
            cue_id = str(row.get("cue_id") or f"{scene_id}_cue_{index + 1}")
            overlays = _list(visual.get("citation_overlay_ids"))
            thumbnail_rules = _list(visual.get("thumbnail_transfer_rule_ids"))
            cues.append(
                {
                    "cue_id": cue_id,
                    "source_scene_id": scene_id,
                    "local_edit_item_id": f"{scene_id}:{cue_id}",
                    "row_number": row.get("row_number"),
                    "speaker": row.get("speaker"),
                    "approximate_timing": {
                        "timing_source": "provisional_even_split_from_scene_duration",
                        "scene_start_sec": scene_start,
                        "scene_end_sec": scene_end,
                        "cue_index_in_scene": index + 1,
                        "cue_count_in_scene": row_count,
                        "approximate_start_sec": round(approx_start, 3),
                        "approximate_end_sec": round(approx_end, 3),
                    },
                    "voice_or_subtitle_action": {
                        "expected_voice_slot_id": row.get("voice_slot_id"),
                        "expected_subtitle_source": row.get("subtitle_source"),
                        "subtitle_text_status": row.get("subtitle_text_status"),
                        "action": "observe YMM4 CSV-imported VoiceItem and linked subtitle readability",
                    },
                    "visual_action": {
                        "primary_template_id": visual.get("primary_template_id"),
                        "supporting_template_ids": _list(visual.get("supporting_template_ids")),
                        "action": "confirm the placeholder scene template instruction is understandable before any final asset work",
                    },
                    "overlay_or_citation_action": {
                        "citation_overlay_ids": overlays,
                        "thumbnail_transfer_rule_ids": thumbnail_rules,
                        "action": "keep citation and thumbnail motifs as placeholders until verified source and approval gates open",
                    },
                    "expected_yymm4_layer_or_track": "VoiceItem/subtitle import lane plus ImageItem/TextItem placeholder scene lanes",
                    "required_asset_state": "real_required_later" if overlays else "placeholder",
                    "import_risk": _import_risk(row, visual),
                    "manual_observation_question": _manual_question(row, visual),
                }
            )

    scene_summaries = []
    for scene_id, rows in voice_rows_by_scene.items():
        visual = _dict(visual_by_scene.get(scene_id))
        duration = _dict(duration_by_scene.get(scene_id))
        scene_summaries.append(
            {
                "scene_id": scene_id,
                "cue_count": len(rows),
                "provisional_start_sec": duration.get("provisional_start_sec"),
                "provisional_end_sec": duration.get("provisional_end_sec"),
                "primary_template_id": visual.get("primary_template_id"),
                "citation_overlay_ids": _list(visual.get("citation_overlay_ids")),
                "thumbnail_transfer_rule_ids": _list(visual.get("thumbnail_transfer_rule_ids")),
                "asset_state": "placeholder_and_real_required_later",
            }
        )

    return {
        "schema_version": "edit_slice_to_ymm4_cue_map.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "cue_map_ready_for_manual_ymm4_observation",
        "input_local_edit_execution_pack": _dict(state.get("paths")).get("local_edit_root"),
        "source_voice_subtitle_map": _dict(state.get("paths")).get("voice_subtitle_operation_map"),
        "source_visual_slot_map": _dict(state.get("paths")).get("visual_asset_slot_map"),
        "queue_operation_count": local_queue.get("queue_operation_count"),
        "scene_count": len(scene_summaries),
        "cue_count": len(cues),
        "scene_summaries": scene_summaries,
        "cues": cues,
        "actual_ymm4_imported": False,
        "rendered_video_created": False,
        "real_input_replaced": False,
        "public_ready": False,
    }


def _import_risk(row: dict[str, Any], visual: dict[str, Any]) -> str:
    risks = []
    if _dict(row.get("voiceitem_readback")).get("observation_required"):
        risks.append("voiceitem_timing_unobserved")
    if row.get("subtitle_text_status") == "draft_sample_fixture_not_real":
        risks.append("sample_fixture_text")
    if _list(visual.get("citation_overlay_ids")):
        risks.append("citation_wording_requires_verified_source")
    return ", ".join(risks) if risks else "low_placeholder_risk"


def _manual_question(row: dict[str, Any], visual: dict[str, Any]) -> str:
    return (
        f"After explicit import observation, does {row.get('cue_id')} keep readable voice/subtitle order "
        f"and make the {visual.get('primary_template_id')} placeholder intent understandable without implying final assets?"
    )


def _gate_readback(state: dict[str, Any], cue_map: dict[str, Any]) -> dict[str, Any]:
    closed_gate_flags = {
        "actual_ymm4_imported": False,
        "actual_yymm4_import": False,
        "rendered_video_created": False,
        "yymm4_rendered": False,
        "production_ymmp_written": False,
        "real_input_replaced": False,
        "real_input_replacement_executed": False,
        "rights_approved": False,
        "rights_accepted": False,
        "public_ready": False,
        "final_thumbnail_approval": False,
        "youtube_uploaded": False,
    }
    return {
        "schema_version": "ymm4_import_ready_gate_readback.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "ymm4_import_gates_closed",
        "cue_count": cue_map.get("cue_count"),
        "scene_count": cue_map.get("scene_count"),
        "gates_closed": all(value is False for value in closed_gate_flags.values()),
        "closed_gate_flags": closed_gate_flags,
        "non_gate_work_completed": [
            "manifest",
            "cue_map",
            "manual_observation_sheet",
            "html_preview",
            "adapter_plan_no_ymmp_write",
        ],
    }


def _ymmp_adapter_plan(state: dict[str, Any], cue_map: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "ymmp_adapter_plan.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "adapter_plan_ready_no_ymmp_write",
        "purpose": "Describe future adapter inputs without generating or patching a YMM4 project.",
        "source_cue_map": "edit_slice_to_ymm4_cue_map.json",
        "cue_count": cue_map.get("cue_count"),
        "expected_item_families": ["VoiceItem", "subtitle/TextItem", "ImageItem", "TextItem"],
        "csv_import_is_manual_future_gate": True,
        "ymmp_file_created": False,
        "production_ymmp_written": False,
        "actual_ymm4_imported": False,
        "rendered_video_created": False,
    }


def _source_artifact_index(state: dict[str, Any]) -> dict[str, Any]:
    paths = _dict(state.get("paths"))
    records = [
        _source_record("local_edit_manifest", paths.get("local_edit_manifest"), "local_edit_pack_read_only", True),
        _source_record("local_edit_queue", paths.get("local_edit_queue"), "queue_read_only", True),
        _source_record("local_scene_plan", paths.get("local_scene_plan"), "scene_execution_read_only", True),
        _source_record("local_gate_readback", paths.get("local_gate_readback"), "gate_readback_read_only", True),
        _source_record("voice_subtitle_operation_map", paths.get("voice_subtitle_operation_map"), "voice_subtitle_read_only", True),
        _source_record("visual_asset_slot_map", paths.get("visual_asset_slot_map"), "visual_slot_read_only", True),
        _source_record("timing_adjustment_model", paths.get("timing_adjustment_model"), "timing_read_only", True),
    ]
    return {
        "schema_version": "ymm4_import_ready_source_artifact_index.v1",
        "artifact_id": state.get("artifact_id"),
        "local_edit_pack_read_only": True,
        "editing_operations_pack_read_only": True,
        "records": records,
    }


def _source_record(record_id: str, path: Any, role: str, exists_expected: bool) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "repo_relative_path": str(path or ""),
        "role": role,
        "exists_expected": exists_expected,
    }


def _manifest(
    state: dict[str, Any],
    cue_map: dict[str, Any],
    gate_readback: dict[str, Any],
    adapter_plan: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    cue_count = int(cue_map.get("cue_count") or 0)
    scenes = _list(cue_map.get("scene_summaries"))
    return {
        "schema_version": "ymm4_import_ready_manifest.v1",
        "artifact_id": DEFAULT_ARTIFACT_ID,
        "artifact_kind": "episode-ymm4-import-ready-edit-package",
        "source_episode_id": SOURCE_EPISODE_ID,
        "input_local_edit_execution_pack": _dict(state.get("paths")).get("local_edit_root"),
        "output_dir": _relpath(output_root, repo_root),
        "files": {filename: _relpath(output_root / filename, repo_root) for filename in REQUIRED_YMM4_IMPORT_READY_FILES},
        "queue_count": _dict(state.get("local_edit_queue")).get("queue_operation_count"),
        "scene_count": len(scenes),
        "cue_count": cue_count,
        "expected_voice_subtitle_links": {
            "count": cue_count,
            "source": _dict(state.get("paths")).get("voice_subtitle_operation_map"),
            "status": "ready_for_manual_import_observation",
        },
        "visual_scene_links": [
            {
                "scene_id": scene.get("scene_id"),
                "primary_template_id": scene.get("primary_template_id"),
                "asset_state": scene.get("asset_state"),
            }
            for scene in scenes
            if isinstance(scene, dict)
        ],
        "citation_overlay_links": [
            {
                "scene_id": scene.get("scene_id"),
                "citation_overlay_ids": scene.get("citation_overlay_ids"),
            }
            for scene in scenes
            if isinstance(scene, dict)
        ],
        "thumbnail_motif_status": "placeholder_context_transferred_not_final_approval",
        "ymm4_import_state": "ready_for_manual_import_observation",
        "actual_ymm4_imported": False,
        "rendered_video_created": False,
        "real_input_replaced": False,
        "rights_approved": False,
        "public_ready": False,
        "gates_closed": gate_readback.get("gates_closed"),
        "adapter_plan_status": adapter_plan.get("status"),
        "ymmp_file_created": adapter_plan.get("ymmp_file_created"),
        "primary_review_file": state.get("primary_human_review"),
        "primary_human_review": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "full_pytest_run": False,
        "next_action": state.get("next_action"),
    }


def _render_html(
    state: dict[str, Any],
    manifest: dict[str, Any],
    cue_map: dict[str, Any],
    gate_readback: dict[str, Any],
) -> str:
    cue_rows = "\n".join(_render_cue_row(row) for row in _list(cue_map.get("cues")))
    scene_rows = "\n".join(_render_scene_row(row) for row in _list(cue_map.get("scene_summaries")))
    gate_rows = "\n".join(_render_gate_row(flag, value) for flag, value in _dict(gate_readback.get("closed_gate_flags")).items())
    return f"""<!doctype html>
<html lang="ja" data-ymm4-import-ready="true" data-artifact-kind="episode-ymm4-import-ready-edit-package">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 YMM4インポート準備レビュー</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #101312;
      --surface: #18201e;
      --panel: #202b28;
      --ink: #f0f7f4;
      --muted: #a8b7b1;
      --line: #34443f;
      --accent: #79d5c5;
      --warn: #f3c66d;
      --hold: #f09595;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; background: var(--bg); color: var(--ink); line-height: 1.5; }}
    main {{ max-width: 1220px; margin: 0 auto; padding: 28px 18px 44px; }}
    h1, h2 {{ margin: 0; letter-spacing: 0; }}
    h1 {{ font-size: clamp(28px, 4vw, 42px); line-height: 1.08; }}
    h2 {{ font-size: 20px; margin: 28px 0 10px; }}
    p {{ color: var(--muted); }}
    .hero {{ display: grid; gap: 14px; padding-bottom: 18px; border-bottom: 1px solid var(--line); }}
    .metrics {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .metric {{ border: 1px solid var(--line); border-radius: 999px; padding: 5px 10px; background: var(--surface); font-size: 12px; }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }}
    .summary-box {{ border: 1px solid var(--line); background: var(--surface); padding: 10px; }}
    .summary-box strong {{ display: block; color: var(--warn); margin-bottom: 4px; }}
    .matrix {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
    th, td {{ border: 1px solid var(--line); padding: 9px; vertical-align: top; overflow-wrap: anywhere; }}
    th {{ color: var(--warn); background: var(--panel); text-align: left; }}
    td {{ background: var(--surface); }}
    .ok {{ color: var(--accent); }}
    .hold {{ color: var(--hold); }}
    code {{ color: var(--warn); }}
    @media (prefers-color-scheme: light) {{
      :root {{ --bg: #f7faf8; --surface: #ffffff; --panel: #eef4f1; --ink: #17211e; --muted: #4d6259; --line: #c9d9d3; }}
    }}
    @media (max-width: 820px) {{
      main {{ padding: 20px 12px 34px; }}
      .summary-grid {{ grid-template-columns: 1fr; }}
      .matrix {{ display: block; overflow-x: auto; white-space: normal; }}
      th, td {{ min-width: 170px; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div class="metrics">
        <span class="metric">import state: {_escape(manifest.get("ymm4_import_state"))}</span>
        <span class="metric">cue数: {_escape(manifest.get("cue_count"))}</span>
        <span class="metric">scene数: {_escape(manifest.get("scene_count"))}</span>
        <span class="metric">gate: {_escape(manifest.get("gates_closed"))} / 閉鎖中</span>
      </div>
      <h1>Episode 002 YMM4インポート準備レビュー</h1>
      <div class="summary-grid" aria-label="レビュー概要">
        <p class="summary-box"><strong>このpackage</strong>既存のローカル編集queueを、YMM4で後日観測するためのcue順・仮timing・voice/subtitle・visual/overlay対応に読み替えたレビュー面です。</p>
        <p class="summary-box"><strong>次に可能になること</strong>明示的なYMM4観測gateが開いた後、CSV import前後のcue順、表示意図、placeholder境界をoperatorが確認できます。</p>
        <p class="summary-box"><strong>閉じたままのこと</strong>YMM4 import、render/export、production `.ymmp` write、real input replacement、rights/public approval、final thumbnail approval、uploadは未実行です。</p>
      </div>
    </section>

    <section data-region="scene-summary">
      <h2>scene runway / cue順</h2>
      <table class="matrix">
        <thead><tr><th>scene</th><th>仮timing</th><th>visual template</th><th>overlay / thumbnail / asset境界</th></tr></thead>
        <tbody>{scene_rows}</tbody>
      </table>
    </section>

    <section data-region="cue-map">
      <h2>cueマップ / timing・voice・subtitle</h2>
      <table class="matrix">
        <thead><tr><th>cue</th><th>仮timing</th><th>voice / subtitle</th><th>visual / overlay</th><th>placeholder境界</th><th>import risk</th><th>観測checkpoint</th></tr></thead>
        <tbody>{cue_rows}</tbody>
      </table>
    </section>

    <section data-region="gate-readback">
      <h2>gate確認 / false値の意味</h2>
      <table class="matrix">
        <thead><tr><th>gate key</th><th>値</th><th>日本語label</th><th>意味</th></tr></thead>
        <tbody>{gate_rows}</tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""


def _render_scene_row(row: Any) -> str:
    item = _dict(row)
    timing = f"{item.get('provisional_start_sec')}s to {item.get('provisional_end_sec')}s"
    return f"""<tr>
  <td><code>{_escape(item.get("scene_id"))}</code><br>cue数: {_escape(item.get("cue_count"))}</td>
  <td>{_escape(timing)}</td>
  <td>{_escape(item.get("primary_template_id"))}</td>
  <td>citation overlay: {_escape(', '.join(_list(item.get("citation_overlay_ids"))))}<br>thumbnail motif: {_escape(', '.join(_list(item.get("thumbnail_transfer_rule_ids"))))}<br>asset state: <span class="hold">{_escape(item.get("asset_state"))}</span></td>
</tr>"""


def _render_cue_row(row: Any) -> str:
    item = _dict(row)
    timing = _dict(item.get("approximate_timing"))
    voice = _dict(item.get("voice_or_subtitle_action"))
    visual = _dict(item.get("visual_action"))
    overlay = _dict(item.get("overlay_or_citation_action"))
    return f"""<tr>
  <td><code>{_escape(item.get("cue_id"))}</code><br>{_escape(item.get("source_scene_id"))}<br>{_escape(item.get("speaker"))}</td>
  <td>{_escape(timing.get("approximate_start_sec"))}s to {_escape(timing.get("approximate_end_sec"))}s<br>{_escape(timing.get("timing_source"))}</td>
  <td>{_escape(voice.get("expected_voice_slot_id"))}<br>{_escape(voice.get("subtitle_text_status"))}</td>
  <td>{_escape(visual.get("primary_template_id"))}<br>overlay: {_escape(', '.join(_list(overlay.get("citation_overlay_ids"))))}<br><span class="hold">{_escape(item.get("required_asset_state"))}</span></td>
  <td>real inputではなくplaceholder/diagnostic前提<br><code>{_escape(item.get("required_asset_state"))}</code></td>
  <td>{_escape(item.get("import_risk"))}</td>
  <td>{_escape(item.get("manual_observation_question"))}</td>
</tr>"""


def _render_gate_row(flag: str, value: Any) -> str:
    return f"""<tr>
  <td><code>{_escape(flag)}</code></td>
  <td><code>{_escape(value)}</code></td>
  <td>{_escape(_gate_label_ja(flag))}</td>
  <td><span class="ok">{_escape(_gate_value_meaning_ja(value))} / このpackageでは閉じたまま</span></td>
</tr>"""


def _gate_label_ja(flag: str) -> str:
    labels = {
        "actual_ymm4_imported": "YMM4実import",
        "actual_yymm4_import": "YMM4実import",
        "rendered_video_created": "render/export済み動画",
        "yymm4_rendered": "YMM4 render",
        "production_ymmp_written": "production .ymmp write",
        "real_input_replaced": "real input replacement",
        "real_input_replacement_executed": "real input replacement",
        "rights_approved": "rights approval",
        "rights_accepted": "rights acceptance",
        "public_ready": "public-ready判定",
        "final_thumbnail_approval": "final thumbnail approval",
        "youtube_uploaded": "YouTube upload",
    }
    return labels.get(flag, flag)


def _gate_value_meaning_ja(value: Any) -> str:
    if value is False:
        return "false = 未実行"
    if value is True:
        return "true = 実行済み"
    return f"{value} = raw readback"


def _render_observation_sheet(state: dict[str, Any], cue_map: dict[str, Any], gate_readback: dict[str, Any]) -> str:
    return f"""# Episode 002 YMM4観測前確認チェック

目的: YMM4観測前の確認チェック。Episode 002限定で、{cue_map.get("scene_count")} scenes / {cue_map.get("cue_count")} cues のimport-ready表示がoperatorに読めるかを見る。
範囲: cue順、仮timing、VoiceItem/subtitle、visual/overlay、placeholder/diagnostic境界の観測準備だけ。
対象外: render承認、production `.ymmp` write、real input replacement、rights承認、public承認、final thumbnail承認、upload。
次に残す成果物: 明示的なgateが開いた場合だけ `YMM4 observation readback` を別artifactとして作る。

1. cue順はS1 -> S2 -> S3の流れで読め、行順の入れ替わりを検出できるか。
2. VoiceItem/subtitleの対応は、speaker、cue、placeholder text statusをoperatorが追える粒度になっているか。
3. visual templateとoverlay/citationの指示は、final素材ではないplaceholderとして誤解なく読めるか。
4. real source、rights、final thumbnailの判断が、diagnostic/placeholder assetから明確に分離されているか。
5. renderより前に残るblockerが、real input、YMM4 timing/readback、rights/public approval、final thumbnail approvalのどれか一つ以上として記録できるか。
"""


def _render_readme(
    state: dict[str, Any],
    manifest: dict[str, Any],
    cue_map: dict[str, Any],
    gate_readback: dict[str, Any],
) -> str:
    return f"""# Episode 002 YMM4インポート準備レビュー

このpackageは、local edit-slice execution queueをYMM4向けの将来観測概念へ読み替えるレビュー面です。実import、render、production `.ymmp` writeは行いません。

- Artifact: `{manifest.get("artifact_id")}`
- Import state: `{manifest.get("ymm4_import_state")}`
- Cue数: {cue_map.get("cue_count")}
- Scene数: {cue_map.get("scene_count")}
- Gates closed: {gate_readback.get("gates_closed")}
- Primary review: `{state.get("primary_human_review")}`
- Machine readback: `{state.get("primary_machine_readable")}`

このpackageでは`.ymmp` fileを生成・patchしません。
"""


def _render_limitations() -> str:
    return """# 制限

- YMM4を起動しない（Do not launch YMM4）。別の明示gateなしにこのpackageからYMM4作業へ進めない。
- CSV import、render/export、production `.ymmp` writeは行わない。
- diagnostic placeholderをreal sourceやtranscript materialで置き換えない。
- rights approval、public readiness、final thumbnail approval、upload、publicationを主張しない。
- cue timingは観測計画用の仮値であり、provisional scene durationからの読み替えに限る。
"""
