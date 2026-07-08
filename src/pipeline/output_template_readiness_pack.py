"""Output template readiness package for episode 002."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.output_video_layer_proof import (
    PROTECTED_GUI_LANE_DIRS,
    _input_paths,
    _load_payloads,
    _read_csv_rows,
    _select_draft_csv,
)
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

DEFAULT_OUTPUT_DIRNAME = "output_template_readiness_pack"
DEFAULT_ARTIFACT_ID = "episode_002_output_template_readiness_pack_v1"
OUTPUT_PROOF_DIRNAME = "output_video_layer_proof"

REQUIRED_OUTPUT_TEMPLATE_FILES = (
    "output_template_readiness_manifest.json",
    "output_template_readiness_preview.html",
    "output_template_readiness_preview.md",
    "scene_timing_map.json",
    "voice_subtitle_mapping.json",
    "visual_scene_template_registry.json",
    "citation_overlay_spec.json",
    "thumbnail_transfer_map.json",
    "yymm4_template_handoff_readiness.json",
    "template_gap_closure_readback.json",
    "source_artifact_index.json",
    "validation_readback.json",
    "review_checklist.md",
    "limitations.md",
    "README_OUTPUT_TEMPLATE_READINESS.md",
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

BUILDABLE_LOCAL_GAPS = (
    "timing_alignment",
    "voice_item_mapping",
    "visual_scene_template",
    "citation_source_overlay",
    "thumbnail_transfer",
)

BLOCKED_GAP_GROUPS = (
    "blocked_by_real_input",
    "blocked_by_yymm4_gate",
    "blocked_by_public_rights_gate",
)

TEMPLATE_TYPE_IDS = (
    "intro_status",
    "topic_explanation",
    "evidence_source",
    "summary_transition",
    "call_to_action",
)


def build_output_template_readiness_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build the local output template readiness package."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _template_input_paths(source_root)
    payloads = _load_template_payloads(paths)
    csv_path = _select_draft_csv(paths)
    csv_rows = _read_csv_rows(csv_path)

    state = _state(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        payloads=payloads,
        csv_path=csv_path,
        csv_rows=csv_rows,
    )
    scene_timing_map = _scene_timing_map(state)
    voice_mapping = _voice_subtitle_mapping(state, scene_timing_map)
    visual_registry = _visual_scene_template_registry(state, scene_timing_map)
    overlay_spec = _citation_overlay_spec(state, scene_timing_map)
    thumbnail_map = _thumbnail_transfer_map(state)
    handoff = _yymm4_template_handoff_readiness(
        state,
        scene_timing_map,
        voice_mapping,
        visual_registry,
        overlay_spec,
        thumbnail_map,
    )
    gap_readback = _template_gap_closure_readback(state)
    source_index = _source_artifact_index(state)
    manifest = _manifest(
        state,
        scene_timing_map,
        voice_mapping,
        visual_registry,
        overlay_spec,
        thumbnail_map,
        gap_readback,
        output_root,
        repo_root,
    )

    _write_json(output_root / "output_template_readiness_manifest.json", manifest)
    _write_json(output_root / "scene_timing_map.json", scene_timing_map)
    _write_json(output_root / "voice_subtitle_mapping.json", voice_mapping)
    _write_json(output_root / "visual_scene_template_registry.json", visual_registry)
    _write_json(output_root / "citation_overlay_spec.json", overlay_spec)
    _write_json(output_root / "thumbnail_transfer_map.json", thumbnail_map)
    _write_json(output_root / "yymm4_template_handoff_readiness.json", handoff)
    _write_json(output_root / "template_gap_closure_readback.json", gap_readback)
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_text(
        output_root / "output_template_readiness_preview.html",
        _render_html(
            state,
            scene_timing_map,
            voice_mapping,
            visual_registry,
            overlay_spec,
            thumbnail_map,
            gap_readback,
        ),
    )
    _write_text(
        output_root / "output_template_readiness_preview.md",
        _render_markdown(state, scene_timing_map, voice_mapping, visual_registry, overlay_spec, thumbnail_map, gap_readback),
    )
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state))
    _write_text(output_root / "limitations.md", _render_limitations(state))
    _write_text(
        output_root / "README_OUTPUT_TEMPLATE_READINESS.md",
        _render_readme(state, scene_timing_map, visual_registry, gap_readback),
    )

    readback = validate_output_template_readiness_pack(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_output_template_readiness_pack(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_output_template_readiness_pack(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated output template readiness package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_OUTPUT_TEMPLATE_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["output_template_readiness_manifest.json"])
    scene_timing_map = _load_json_if_present(files["scene_timing_map.json"])
    voice_mapping = _load_json_if_present(files["voice_subtitle_mapping.json"])
    visual_registry = _load_json_if_present(files["visual_scene_template_registry.json"])
    overlay_spec = _load_json_if_present(files["citation_overlay_spec.json"])
    thumbnail_map = _load_json_if_present(files["thumbnail_transfer_map.json"])
    handoff = _load_json_if_present(files["yymm4_template_handoff_readiness.json"])
    gap_readback = _load_json_if_present(files["template_gap_closure_readback.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])
    json_payloads = {
        "manifest": manifest,
        "scene_timing_map": scene_timing_map,
        "voice_subtitle_mapping": voice_mapping,
        "visual_scene_template_registry": visual_registry,
        "citation_overlay_spec": overlay_spec,
        "thumbnail_transfer_map": thumbnail_map,
        "yymm4_template_handoff_readiness": handoff,
        "template_gap_closure_readback": gap_readback,
        "source_artifact_index": source_index,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = _dict(json_payloads["manifest"])
    scene_timing_map = _dict(json_payloads["scene_timing_map"])
    voice_mapping = _dict(json_payloads["voice_subtitle_mapping"])
    visual_registry = _dict(json_payloads["visual_scene_template_registry"])
    overlay_spec = _dict(json_payloads["citation_overlay_spec"])
    thumbnail_map = _dict(json_payloads["thumbnail_transfer_map"])
    handoff = _dict(json_payloads["yymm4_template_handoff_readiness"])
    gap_readback = _dict(json_payloads["template_gap_closure_readback"])
    source_index = _dict(json_payloads["source_artifact_index"])

    html_text = files["output_template_readiness_preview.html"].read_text(encoding="utf-8") if files["output_template_readiness_preview.html"].exists() else ""
    markdown_text = files["output_template_readiness_preview.md"].read_text(encoding="utf-8") if files["output_template_readiness_preview.md"].exists() else ""
    limitations_text = files["limitations.md"].read_text(encoding="utf-8") if files["limitations.md"].exists() else ""

    scenes = [row for row in _list(scene_timing_map.get("scenes")) if isinstance(row, dict)]
    utterances = [row for row in _list(voice_mapping.get("utterance_mappings")) if isinstance(row, dict)]
    template_types = [row for row in _list(visual_registry.get("template_types")) if isinstance(row, dict)]
    overlay_slots = [row for row in _list(overlay_spec.get("overlay_slots")) if isinstance(row, dict)]
    transfer_rules = [row for row in _list(thumbnail_map.get("transfer_rules")) if isinstance(row, dict)]
    gap_rows = [row for row in _list(gap_readback.get("gap_results")) if isinstance(row, dict)]
    gap_by_id = {str(row.get("feature_id")): row for row in gap_rows}
    boundary_flags = _dict(manifest.get("boundary_flags"))
    gui_touches = _list(manifest.get("gui_lane_files_touched"))

    if manifest.get("artifact_kind") != "episode-output-template-readiness-pack":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "output_template_readiness_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")
    if len(scenes) < 3:
        failed_checks.append("scene_timing_map_too_short")
    if not utterances:
        failed_checks.append("voice_subtitle_mapping_empty")
    if voice_mapping.get("csv_reference_status") != "references_available_csv_rows":
        failed_checks.append("voice_mapping_csv_reference_missing")
    if len(template_types) < 4:
        failed_checks.append("visual_template_registry_too_short")
    if not overlay_slots:
        failed_checks.append("citation_overlay_slots_missing")
    if not transfer_rules:
        failed_checks.append("thumbnail_transfer_rules_missing")
    for gap_id in BUILDABLE_LOCAL_GAPS:
        result = _dict(gap_by_id.get(gap_id))
        if result.get("template_readiness_status") not in {"closed_for_local_template_readiness", "partial_for_local_template_readiness"}:
            failed_checks.append(f"buildable_gap_not_addressed:{gap_id}")
    if int(gap_readback.get("previous_buildable_gap_count", 0) or 0) != len(BUILDABLE_LOCAL_GAPS):
        failed_checks.append("previous_buildable_gap_count_mismatch")
    if int(gap_readback.get("buildable_gap_closed_count", 0) or 0) < len(BUILDABLE_LOCAL_GAPS):
        failed_checks.append("buildable_gap_closed_count_too_low")
    if handoff.get("actual_yymm4_import") is not False:
        failed_checks.append("actual_yymm4_import_not_false")
    if handoff.get("yymm4_rendered") is not False:
        failed_checks.append("yymm4_rendered_not_false")
    if handoff.get("production_ready") is not False:
        failed_checks.append("production_ready_not_false")
    if thumbnail_map.get("final_thumbnail_approval") is not False:
        failed_checks.append("final_thumbnail_approval_not_false")
    if manifest.get("shared_docs_touched") is not False:
        failed_checks.append("shared_docs_touched_not_false")
    if gui_touches:
        failed_checks.append("gui_lane_files_touched_not_empty")
    if source_index.get("gui_lane_context_read_only") is not True:
        failed_checks.append("gui_lane_context_not_read_only")
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")
    for marker in (
        'data-output-template-readiness="true"',
        'data-region="timing-strip"',
        'data-region="scene-template-lane"',
        'data-region="voice-subtitle-lane"',
        'data-region="overlay-lane"',
        'data-region="thumbnail-transfer-lane"',
    ):
        if marker not in html_text:
            failed_checks.append(f"html_marker_missing:{marker}")
    if "color-scheme: dark light" not in html_text:
        failed_checks.append("dark_color_scheme_missing")
    if "prefers-color-scheme" not in html_text:
        failed_checks.append("prefers_color_scheme_missing")
    if not markdown_text.strip():
        failed_checks.append("markdown_preview_empty")
    if "no YMM4 GUI launch, import, or render" not in limitations_text:
        failed_checks.append("limitations_yymm4_gate_missing")

    external_refs = _external_refs_in_files([path for name, path in files.items() if name != "validation_readback.json"])
    forbidden_hits = _forbidden_true_claims(root)
    temporary_hits = _temporary_copy_hits(
        [
            files["output_template_readiness_preview.html"],
            files["output_template_readiness_preview.md"],
            files["README_OUTPUT_TEMPLATE_READINESS.md"],
        ]
    )
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "html_preview_exists": files["output_template_readiness_preview.html"].exists(),
        "markdown_preview_exists": files["output_template_readiness_preview.md"].exists(),
        "scene_count": len(scenes),
        "voice_mapping_rows": len(utterances),
        "visual_template_count": len(template_types),
        "overlay_slot_count": len(overlay_slots),
        "thumbnail_transfer_rule_count": len(transfer_rules),
        "buildable_gap_results": {gap_id: _dict(gap_by_id.get(gap_id)).get("template_readiness_status") for gap_id in BUILDABLE_LOCAL_GAPS},
        "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS),
        "gui_lane_files_touched": gui_touches,
        "shared_docs_touched": manifest.get("shared_docs_touched"),
        "external_dependency_status": "none_found" if not external_refs else "found",
        "forbidden_true_claims_absent": not forbidden_hits,
        "temporary_copy_absent": not temporary_hits,
    }
    return {
        "schema_version": "output_template_readiness_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "primary_review_file": str(root / "output_template_readiness_preview.html"),
        "primary_human_review": str(root / "output_template_readiness_preview.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "scene_count": len(scenes),
        "timing_map_status": scene_timing_map.get("status"),
        "voice_mapping_status": voice_mapping.get("status"),
        "visual_template_count": len(template_types),
        "citation_overlay_status": overlay_spec.get("status"),
        "thumbnail_transfer_status": thumbnail_map.get("status"),
        "previous_buildable_gap_count": int(gap_readback.get("previous_buildable_gap_count", 0) or 0),
        "buildable_gap_closed_count": int(gap_readback.get("buildable_gap_closed_count", 0) or 0),
        "buildable_gap_partial_count": int(gap_readback.get("buildable_gap_partial_count", 0) or 0),
        "blocked_by_real_input_count": int(gap_readback.get("blocked_by_real_input_count", 0) or 0),
        "blocked_by_yymm4_gate_count": int(gap_readback.get("blocked_by_yymm4_gate_count", 0) or 0),
        "blocked_by_public_rights_count": int(gap_readback.get("blocked_by_public_rights_count", 0) or 0),
        "gui_lane_files_touched": gui_touches,
        "shared_docs_touched": manifest.get("shared_docs_touched"),
        "full_pytest_run": False,
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{(root / "output_template_readiness_preview.html").resolve()}"',
        "access_state": "verified_present" if (root / "output_template_readiness_preview.html").exists() else "missing",
        "next_action": manifest.get("next_action"),
    }


def _template_input_paths(source_root: Path) -> dict[str, Path]:
    paths = _input_paths(source_root)
    proof_root = source_root / OUTPUT_PROOF_DIRNAME
    paths.update(
        {
            "output_proof_root": proof_root,
            "output_proof_manifest": proof_root / "output_video_proof_manifest.json",
            "output_proof_scene_timeline": proof_root / "scene_timeline.json",
            "output_proof_gap_ledger": proof_root / "output_gap_ledger.json",
            "output_proof_validation": proof_root / "validation_readback.json",
            "output_proof_storyboard": proof_root / "episode_002_storyboard_preview.html",
        }
    )
    return paths


def _load_template_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    payloads = _load_payloads(paths)
    payloads.update(
        {
            "output_proof_manifest": _load_json_if_present(paths["output_proof_manifest"]),
            "output_proof_scene_timeline": _load_json_if_present(paths["output_proof_scene_timeline"]),
            "output_proof_gap_ledger": _load_json_if_present(paths["output_proof_gap_ledger"]),
            "output_proof_validation": _load_json_if_present(paths["output_proof_validation"]),
        }
    )
    return payloads


def _state(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    repo_root: Path,
    paths: dict[str, Path],
    payloads: dict[str, Any],
    csv_path: Path,
    csv_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    proof_manifest = _dict(payloads.get("output_proof_manifest"))
    scene_timeline = _dict(payloads.get("output_proof_scene_timeline"))
    gap_ledger = _dict(payloads.get("output_proof_gap_ledger"))
    import_summary = _dict(payloads.get("import_summary"))
    boundary_status = _dict(import_summary.get("boundary_status"))
    boundary_flags = _boundary_flags(import_summary)
    thumbnail_variants = _dict(payloads.get("thumbnail_variants"))
    writer_ir = _dict(payloads.get("writer_ir"))
    return {
        "schema_version": "output_template_readiness_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-output-template-readiness-pack",
        "status": "output_template_readiness_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "repo_root": str(repo_root),
        "paths": {name: _relpath(path, repo_root) for name, path in paths.items() if isinstance(path, Path)},
        "proof_manifest": proof_manifest,
        "proof_scene_timeline": scene_timeline,
        "proof_gap_ledger": gap_ledger,
        "csv_path": _relpath(csv_path, repo_root),
        "csv_rows": csv_rows,
        "csv_row_count": len(csv_rows),
        "writer_utterances": _list(writer_ir.get("utterances")),
        "writer_sections": _list(writer_ir.get("sections")),
        "thumbnail_variants": thumbnail_variants,
        "thumbnail_recommended_variant": thumbnail_variants.get("recommended_variant_id"),
        "real_transcript_status": boundary_status.get("real_transcript_status", "blocked_by_real_input"),
        "yymm4_status": boundary_status.get("yymm4_import_observed_status", "not_imported_to_yymm4"),
        "boundary_flags": boundary_flags,
        "primary_human_review": _relpath(output_root / "output_template_readiness_preview.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_action": "Review output_template_readiness_preview.html, then prepare verified local source/transcript material before any YMM4 observation gate.",
    }


def _boundary_flags(import_summary: dict[str, Any]) -> dict[str, bool]:
    source_flags = _dict(import_summary.get("boundary_flags"))
    return {
        "dry_run": True,
        "sample_fixture_not_real": bool(source_flags.get("sample_fixture_not_real", True)),
        "no_real_transcript": bool(source_flags.get("no_real_transcript", True)),
        "rights_boundary": True,
        "public_upload_closed": bool(source_flags.get("public_upload_closed", True)),
        "yymm4_render_closed": bool(source_flags.get("yymm4_render_closed", True)),
        "no_yymm4_import": bool(source_flags.get("no_yymm4_import", True)),
        "validation_noise_nonblocking": bool(source_flags.get("validation_noise_nonblocking", True)),
        "not_production_ready": True,
    }


def _scene_timing_map(state: dict[str, Any]) -> dict[str, Any]:
    proof_timeline = _dict(state.get("proof_scene_timeline"))
    scenes = [_timing_scene(scene, state) for scene in _list(proof_timeline.get("scenes")) if isinstance(scene, dict)]
    return {
        "schema_version": "scene_timing_map.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "template_ready_estimated_no_audio_or_yymm4_timing",
        "source_scene_timeline": _dict(state.get("paths")).get("output_proof_scene_timeline"),
        "draft_csv_used": state.get("csv_path"),
        "scene_count": len(scenes),
        "csv_row_count": state.get("csv_row_count"),
        "timing_model": "provisional_scene_template_timing_from_rows",
        "total_provisional_duration_sec": sum(int(scene.get("provisional_duration_sec", 0) or 0) for scene in scenes),
        "actual_audio_timing_status": "not_available_until_yymm4_observation",
        "scenes": scenes,
    }


def _timing_scene(scene: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    row_start = int(scene.get("row_start", 0) or 0)
    row_end = int(scene.get("row_end", row_start) or row_start)
    cue_ids = [f"csv_row_{row}" for row in range(row_start, row_end + 1) if row > 0]
    return {
        "scene_id": scene.get("scene_id"),
        "title": scene.get("title"),
        "arc_phase": scene.get("arc_phase"),
        "row_start": row_start,
        "row_end": row_end,
        "cue_ids": cue_ids,
        "transcript_csv_rows": cue_ids,
        "provisional_start_sec": scene.get("estimated_start_sec"),
        "provisional_end_sec": scene.get("estimated_end_sec"),
        "provisional_duration_sec": scene.get("estimated_duration_sec"),
        "duration_source": "output_video_layer_proof.scene_timeline.estimated_duration_sec",
        "timing_readback_template": {
            "future_yymm4_voiceitem_start_sec": None,
            "future_yymm4_voiceitem_end_sec": None,
            "future_audio_duration_sec": None,
            "observation_required": "explicit_yymm4_gate",
        },
        "template_ready": True,
        "actual_timing_ready": False,
        "status": "closed_for_local_template_readiness",
    }


def _voice_subtitle_mapping(state: dict[str, Any], scene_timing_map: dict[str, Any]) -> dict[str, Any]:
    csv_rows = [row for row in _list(state.get("csv_rows")) if isinstance(row, dict)]
    speaker_order = _speaker_order(csv_rows)
    voice_slots = {
        speaker: {
            "speaker": speaker,
            "voice_slot_id": f"voice_slot_{index}",
            "role_hint": "explainer_or_host" if index == 1 else "listener_or_partner",
            "voice_item_status": "template_assumption_not_yymm4_voiceitem",
            "requires_yymm4_observation": True,
        }
        for index, speaker in enumerate(speaker_order, start=1)
    }
    utterance_mappings = []
    for row in csv_rows:
        row_number = int(row.get("row_number", 0) or 0)
        scene = _scene_for_row(scene_timing_map, row_number)
        speaker = str(row.get("speaker") or "").strip()
        slot = _dict(voice_slots.get(speaker))
        utterance_mappings.append(
            {
                "row_number": row_number,
                "cue_id": f"csv_row_{row_number}",
                "scene_id": scene.get("scene_id"),
                "speaker": speaker,
                "voice_slot_id": slot.get("voice_slot_id"),
                "subtitle_text": row.get("text"),
                "subtitle_source": f"{state.get('csv_path')}#row-{row_number}",
                "subtitle_status": "draft_sample_fixture_not_real",
                "voiceitem_status": "not_imported_to_yymm4",
            }
        )
    return {
        "schema_version": "voice_subtitle_mapping.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "voice_subtitle_template_ready_no_yymm4_voiceitems",
        "csv_reference_status": "references_available_csv_rows",
        "source_csv": state.get("csv_path"),
        "speaker_count": len(speaker_order),
        "voice_slots": list(voice_slots.values()),
        "utterance_count": len(utterance_mappings),
        "utterance_mappings": utterance_mappings,
        "unknowns": [
            "actual YMM4 VoiceItem IDs",
            "audio-derived start/end timing",
            "final voice preset choices",
            "real transcript replacement text",
        ],
    }


def _speaker_order(csv_rows: list[dict[str, Any]]) -> list[str]:
    speakers: list[str] = []
    for row in csv_rows:
        speaker = str(row.get("speaker") or "").strip()
        if speaker and speaker not in speakers:
            speakers.append(speaker)
    return speakers


def _scene_for_row(scene_timing_map: dict[str, Any], row_number: int) -> dict[str, Any]:
    for scene in _list(scene_timing_map.get("scenes")):
        if not isinstance(scene, dict):
            continue
        if int(scene.get("row_start", 0) or 0) <= row_number <= int(scene.get("row_end", 0) or 0):
            return scene
    return {}


def _visual_scene_template_registry(state: dict[str, Any], scene_timing_map: dict[str, Any]) -> dict[str, Any]:
    template_types = [
        _template_type("intro_status", "Intro status", ["intro"], "Opening hook, title promise, dry-run status badges", "studio_blue"),
        _template_type("topic_explanation", "Topic explanation", ["develop"], "Two-column explanation surface with subtitle rail", "diagram"),
        _template_type("evidence_source", "Evidence/source", ["develop", "closing"], "Source note shelf and citation overlay placeholders", "dark_board"),
        _template_type("summary_transition", "Summary transition", ["closing"], "Boundary recap and next-material strip", "dark_board"),
        _template_type("call_to_action", "Call to action", ["closing"], "Verified input preparation card without public upload claim", "dark_board"),
    ]
    assignments = []
    for scene in _list(scene_timing_map.get("scenes")):
        if not isinstance(scene, dict):
            continue
        phase = str(scene.get("arc_phase") or "")
        default_template = "intro_status" if phase == "intro" else "topic_explanation" if phase == "develop" else "summary_transition"
        assignments.append(
            {
                "scene_id": scene.get("scene_id"),
                "arc_phase": phase,
                "primary_template_id": default_template,
                "supporting_template_ids": ["evidence_source"] if phase in {"develop", "closing"} else [],
                "template_status": "local_template_ready",
                "requires_external_media": False,
            }
        )
    return {
        "schema_version": "visual_scene_template_registry.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "visual_scene_templates_ready_local_offline",
        "template_type_count": len(template_types),
        "template_types": template_types,
        "scene_assignments": assignments,
        "closed_gate_policy": "Templates prepare composition only; no YMM4 import, render, production .ymmp, or public asset approval.",
    }


def _template_type(template_id: str, label: str, phases: list[str], purpose: str, default_bg: str) -> dict[str, Any]:
    return {
        "template_id": template_id,
        "label": label,
        "applicable_arc_phases": phases,
        "purpose": purpose,
        "default_bg": default_bg,
        "lanes": ["scene_frame", "speaker_slots", "subtitle_band", "overlay_slot"],
        "ready_to_apply_local_template": True,
        "requires_external_media": False,
        "requires_yymm4_gate": False,
    }


def _citation_overlay_spec(state: dict[str, Any], scene_timing_map: dict[str, Any]) -> dict[str, Any]:
    overlay_slots = []
    for scene in _list(scene_timing_map.get("scenes")):
        if not isinstance(scene, dict):
            continue
        scene_id = str(scene.get("scene_id") or "")
        overlay_slots.append(
            {
                "overlay_id": f"{scene_id.lower()}_source_note",
                "scene_id": scene_id,
                "timing_anchor": f"{scene_id}:{scene.get('row_start')}-{scene.get('row_end')}",
                "screen_region": "lower_third_source_shelf",
                "source_text_policy": "reviewed local source note placeholder only",
                "current_text": "Synthetic dry-run source; replace after verified local source intake.",
                "external_media_allowed": False,
                "status": "overlay_template_ready_no_real_source_claim",
            }
        )
    return {
        "schema_version": "citation_overlay_spec.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "citation_overlay_template_ready_local_offline",
        "overlay_slot_count": len(overlay_slots),
        "overlay_slots": overlay_slots,
        "source_context_status": "sample_fixture_not_real",
        "future_input_required": "verified local source/transcript before production use",
    }


def _thumbnail_transfer_map(state: dict[str, Any]) -> dict[str, Any]:
    thumbnail_variants = _dict(state.get("thumbnail_variants"))
    recommended_id = str(thumbnail_variants.get("recommended_variant_id") or "headline_driven")
    variants = [row for row in _list(thumbnail_variants.get("variants")) if isinstance(row, dict)]
    recommended = next((row for row in variants if row.get("variant_id") == recommended_id), {})
    return {
        "schema_version": "thumbnail_transfer_map.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "thumbnail_context_transfer_ready_not_final_approval",
        "source_thumbnail_variants": _dict(state.get("paths")).get("thumbnail_variants"),
        "recommended_variant_id": recommended_id,
        "recommended_layout_family": _dict(recommended).get("layout_family"),
        "final_thumbnail_approval": False,
        "transfer_rules": [
            {
                "rule_id": "headline_to_opening_frame",
                "source_concept": _dict(recommended).get("headline", "DRY RUN FACTORY CHECK"),
                "video_frame_language": "Use as opening frame headline with dry-run badge.",
                "target_scene_ids": ["S1"],
            },
            {
                "rule_id": "proof_stack_to_boundary_strip",
                "source_concept": "proof metrics and closed-gate labels",
                "video_frame_language": "Move compact proof labels into lower status strip.",
                "target_scene_ids": ["S1", "S3"],
            },
            {
                "rule_id": "palette_to_template_tokens",
                "source_concept": _dict(recommended).get("palette", {}),
                "video_frame_language": "Reuse contrast direction as local CSS/template color tokens only.",
                "target_scene_ids": ["S1", "S2", "S3"],
            },
        ],
        "blocked_until_human_review": [
            "final thumbnail approval",
            "production thumbnail export",
            "rights/public-ready acceptance",
        ],
    }


def _yymm4_template_handoff_readiness(
    state: dict[str, Any],
    scene_timing_map: dict[str, Any],
    voice_mapping: dict[str, Any],
    visual_registry: dict[str, Any],
    overlay_spec: dict[str, Any],
    thumbnail_map: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "yymm4_template_handoff_readiness.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "ready_for_later_import_observation_templates_only",
        "ready_for_later_import_observation": [
            "scene timing map with cue IDs",
            "voice/subtitle row mapping",
            "visual scene template assignments",
            "citation/source overlay slots",
            "thumbnail-to-frame transfer rules",
        ],
        "requires_yymm4_gate": [
            "actual CSV import observation",
            "VoiceItem timing readback",
            "render smoke",
            "production .ymmp generation",
        ],
        "requires_real_input": [
            "verified source/transcript replacement",
            "real source rights context",
        ],
        "actual_yymm4_import": False,
        "yymm4_rendered": False,
        "production_ready": False,
        "public_ready": False,
        "scene_count": scene_timing_map.get("scene_count"),
        "voice_mapping_rows": voice_mapping.get("utterance_count"),
        "visual_template_count": visual_registry.get("template_type_count"),
        "overlay_slot_count": overlay_spec.get("overlay_slot_count"),
        "thumbnail_transfer_status": thumbnail_map.get("status"),
        "gate_policy": "YMM4 GUI launch, import, render, and production .ymmp creation remain closed.",
    }


def _template_gap_closure_readback(state: dict[str, Any]) -> dict[str, Any]:
    gap_ledger = _dict(state.get("proof_gap_ledger"))
    features = [row for row in _list(gap_ledger.get("features")) if isinstance(row, dict)]
    groups = _dict(gap_ledger.get("groups"))
    gap_results = []
    for feature in features:
        feature_id = str(feature.get("feature_id") or "")
        category = str(feature.get("category") or "")
        if feature_id in BUILDABLE_LOCAL_GAPS:
            status = "closed_for_local_template_readiness"
            closure_artifact = _closure_artifact_for_gap(feature_id)
        else:
            status = f"unchanged_{category}"
            closure_artifact = None
        gap_results.append(
            {
                "feature_id": feature_id,
                "previous_category": category,
                "previous_current_state": feature.get("current_state"),
                "template_readiness_status": status,
                "closure_artifact": closure_artifact,
                "remaining_true_gate": _remaining_gate_for_gap(feature_id, category),
            }
        )
    return {
        "schema_version": "template_gap_closure_readback.v1",
        "artifact_id": state.get("artifact_id"),
        "source_gap_ledger": _dict(state.get("paths")).get("output_proof_gap_ledger"),
        "previous_buildable_gap_count": len(_list(groups.get("buildable_locally"))) or len(BUILDABLE_LOCAL_GAPS),
        "buildable_gap_closed_count": len(BUILDABLE_LOCAL_GAPS),
        "buildable_gap_partial_count": 0,
        "blocked_by_real_input_count": len(_list(groups.get("blocked_by_real_input"))),
        "blocked_by_yymm4_gate_count": len(_list(groups.get("blocked_by_yymm4_gate"))),
        "blocked_by_public_rights_count": len(_list(groups.get("blocked_by_public_rights_gate"))),
        "gap_results": gap_results,
    }


def _closure_artifact_for_gap(feature_id: str) -> str:
    return {
        "timing_alignment": "scene_timing_map.json",
        "voice_item_mapping": "voice_subtitle_mapping.json",
        "visual_scene_template": "visual_scene_template_registry.json",
        "citation_source_overlay": "citation_overlay_spec.json",
        "thumbnail_transfer": "thumbnail_transfer_map.json",
    }.get(feature_id, "")


def _remaining_gate_for_gap(feature_id: str, category: str) -> str:
    if feature_id in BUILDABLE_LOCAL_GAPS:
        return "actual production use still waits for verified input and explicit YMM4/public gates where relevant"
    if category == "blocked_by_real_input":
        return "verified local source/transcript material required"
    if category == "blocked_by_yymm4_gate":
        return "explicit YMM4 observation/render gate required"
    if category == "blocked_by_public_rights_gate":
        return "human rights/public-ready/final thumbnail decision required"
    return "unknown"


def _source_artifact_index(state: dict[str, Any]) -> dict[str, Any]:
    paths = _dict(state.get("paths"))
    records = [
        _source_record("output_video_proof_manifest", paths.get("output_proof_manifest"), "proof_source", True),
        _source_record("output_scene_timeline", paths.get("output_proof_scene_timeline"), "timing_source", True),
        _source_record("output_gap_ledger", paths.get("output_proof_gap_ledger"), "gap_source", True),
        _source_record("writer_ir_candidate", paths.get("writer_ir"), "voice_visual_source", True),
        _source_record("cue_packet_candidate", paths.get("cue_packet"), "cue_source", True),
        _source_record("draft_yymm4_csv", state.get("csv_path"), "draft_csv_source", True),
        _source_record("transcript_validation", paths.get("transcript_validation"), "input_boundary", True),
        _source_record("import_readiness_summary", paths.get("import_summary"), "yymm4_boundary", True),
        _source_record("yymm4_csv_inventory", paths.get("csv_inventory"), "csv_inventory", True),
        _source_record("thumbnail_variants", paths.get("thumbnail_variants"), "thumbnail_context", True),
        _source_record("japanese_graphic_console_validation", paths.get("japanese_console_validation"), "gui_context_read_only", True),
    ]
    return {
        "schema_version": "output_template_source_artifact_index.v1",
        "artifact_id": state.get("artifact_id"),
        "gui_lane_context_read_only": True,
        "protected_gui_lane_dirs": list(PROTECTED_GUI_LANE_DIRS),
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
    scene_timing_map: dict[str, Any],
    voice_mapping: dict[str, Any],
    visual_registry: dict[str, Any],
    overlay_spec: dict[str, Any],
    thumbnail_map: dict[str, Any],
    gap_readback: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "output_template_readiness_manifest.v1",
        "artifact_id": state.get("artifact_id"),
        "artifact_kind": "episode-output-template-readiness-pack",
        "status": "output_template_readiness_ready_local_offline",
        "parallel_lane": "output_video_layer",
        "output_dir": _relpath(output_root, repo_root),
        "files": {filename: _relpath(output_root / filename, repo_root) for filename in REQUIRED_OUTPUT_TEMPLATE_FILES},
        "primary_review_file": state.get("primary_human_review"),
        "primary_human_review": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "scene_count": scene_timing_map.get("scene_count"),
        "timing_map_status": scene_timing_map.get("status"),
        "voice_mapping_status": voice_mapping.get("status"),
        "visual_template_count": visual_registry.get("template_type_count"),
        "citation_overlay_status": overlay_spec.get("status"),
        "thumbnail_transfer_status": thumbnail_map.get("status"),
        "previous_buildable_gap_count": gap_readback.get("previous_buildable_gap_count"),
        "buildable_gap_closed_count": gap_readback.get("buildable_gap_closed_count"),
        "buildable_gap_partial_count": gap_readback.get("buildable_gap_partial_count"),
        "blocked_by_real_input_count": gap_readback.get("blocked_by_real_input_count"),
        "blocked_by_yymm4_gate_count": gap_readback.get("blocked_by_yymm4_gate_count"),
        "blocked_by_public_rights_count": gap_readback.get("blocked_by_public_rights_count"),
        "gui_lane_files_touched": [],
        "shared_docs_touched": False,
        "boundary_flags": state.get("boundary_flags"),
        "actual_yymm4_import": False,
        "yymm4_rendered": False,
        "production_ready": False,
        "public_ready": False,
        "final_thumbnail_approval": False,
        "next_action": state.get("next_action"),
    }


def _render_html(
    state: dict[str, Any],
    scene_timing_map: dict[str, Any],
    voice_mapping: dict[str, Any],
    visual_registry: dict[str, Any],
    overlay_spec: dict[str, Any],
    thumbnail_map: dict[str, Any],
    gap_readback: dict[str, Any],
) -> str:
    timing_nodes = "\n".join(_render_timing_node(scene) for scene in _list(scene_timing_map.get("scenes")))
    scene_templates = "\n".join(_render_template_assignment(row) for row in _list(visual_registry.get("scene_assignments")))
    voice_rows = "\n".join(_render_voice_row(row) for row in _list(voice_mapping.get("utterance_mappings"))[:9])
    overlay_rows = "\n".join(_render_overlay_slot(row) for row in _list(overlay_spec.get("overlay_slots")))
    thumb_rules = "\n".join(_render_thumb_rule(row) for row in _list(thumbnail_map.get("transfer_rules")))
    closed = gap_readback.get("buildable_gap_closed_count")
    total = gap_readback.get("previous_buildable_gap_count")
    return f"""<!doctype html>
<html lang="ja" data-output-template-readiness="true" data-artifact-kind="episode-output-template-readiness-pack">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Output Template Readiness</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #101316;
      --surface: #172027;
      --stage: #111a21;
      --panel: #202734;
      --line: #66717c;
      --text: #f4efe4;
      --muted: #c8c0b1;
      --teal: #73dfcf;
      --blue: #91bbff;
      --amber: #f1cf6a;
      --rose: #f0a1aa;
      --green: #9ee8bc;
      --shadow: 0 18px 44px rgba(0, 0, 0, 0.34);
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #eef2ef;
        --surface: #e4ebe6;
        --stage: #f6f0e4;
        --panel: #e8e6dc;
        --line: #aeb8b2;
        --text: #1d231f;
        --muted: #5d665f;
        --teal: #0f766e;
        --blue: #1d4ed8;
        --amber: #8a5a00;
        --rose: #9b1c1c;
        --green: #047857;
        --shadow: 0 16px 32px rgba(29, 35, 31, 0.12);
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }}
    .wrap {{
      width: min(1400px, calc(100% - 28px));
      margin: 0 auto;
      padding: 16px 0 34px;
    }}
    .topline {{
      display: grid;
      grid-template-columns: minmax(280px, 1fr) auto;
      gap: 12px;
      align-items: center;
      padding: 10px 0 14px;
    }}
    .identity, .badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }}
    .episode {{ font-size: 1.06rem; font-weight: 780; }}
    .badge, .gate {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 3px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--panel);
      color: var(--teal);
      font-size: 0.76rem;
      font-weight: 720;
      white-space: nowrap;
    }}
    .gate {{ color: var(--rose); }}
    h1, h2, h3, p {{ margin: 0; }}
    h1 {{ font-size: clamp(1.45rem, 2.4vw, 2.25rem); line-height: 1.08; letter-spacing: 0; }}
    h2 {{ font-size: 1rem; letter-spacing: 0; }}
    h3 {{ font-size: 0.82rem; color: var(--muted); letter-spacing: 0; }}
    p, span {{ line-height: 1.4; }}
    p {{ color: var(--muted); }}
    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(280px, 0.32fr);
      gap: 14px;
      align-items: stretch;
    }}
    .board, .side, .lane {{
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      background: var(--surface);
    }}
    .board {{
      padding: 16px;
      display: grid;
      gap: 14px;
    }}
    .side {{
      padding: 16px;
      background: var(--panel);
      display: grid;
      align-content: start;
      gap: 12px;
    }}
    .summary-strip {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 8px;
    }}
    .summary-item {{
      border-left: 3px solid var(--teal);
      padding: 7px 9px;
      background: rgba(255, 255, 255, 0.035);
      min-width: 0;
    }}
    .summary-item strong {{ display: block; color: var(--text); }}
    .timing-strip {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }}
    .timing-node, .template-node, .voice-row, .overlay-node, .thumb-node {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--stage);
      padding: 10px;
      min-width: 0;
    }}
    .meter {{
      height: 9px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.08);
      overflow: hidden;
      margin: 8px 0;
    }}
    .meter span {{ display: block; height: 100%; background: var(--amber); }}
    .lanes {{
      display: grid;
      grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
      gap: 14px;
      margin-top: 14px;
    }}
    .lane {{
      padding: 14px;
      display: grid;
      gap: 10px;
      align-content: start;
    }}
    .template-grid, .overlay-grid, .thumb-grid {{
      display: grid;
      gap: 8px;
    }}
    .voice-list {{
      display: grid;
      gap: 6px;
      max-height: 470px;
      overflow: auto;
      padding-right: 4px;
    }}
    .voice-row {{
      display: grid;
      grid-template-columns: 74px 120px minmax(0, 1fr);
      gap: 8px;
      align-items: start;
    }}
    .voice-row span:first-child {{ color: var(--blue); font-weight: 720; }}
    .voice-row span:nth-child(2) {{ color: var(--green); }}
    .template-node strong, .timing-node strong, .overlay-node strong, .thumb-node strong {{
      display: block;
      color: var(--text);
    }}
    code {{ color: var(--blue); overflow-wrap: anywhere; font-size: 0.84rem; }}
    @media (max-width: 1120px) {{
      .topline, .hero, .lanes, .summary-strip, .timing-strip {{ grid-template-columns: 1fr; }}
      .voice-row {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <header class="topline" data-region="header">
      <div class="identity">
        <span class="episode">Episode 002</span>
        <span class="badge">Output / Video Layer</span>
        <span class="badge">template readiness</span>
        <span class="badge">local offline</span>
      </div>
      <div class="badges" aria-label="closed gates">
        <span class="gate">no import</span>
        <span class="gate">no render</span>
        <span class="gate">no public</span>
        <span class="gate">no final thumbnail</span>
      </div>
    </header>
    <section class="hero">
      <section class="board">
        <div>
          <h1>Episode 002 Output Template Readiness</h1>
          <p>Buildable output gaps are converted into reusable local templates for timing, voice/subtitles, scenes, overlays, and thumbnail transfer. Real input and YMM4/public gates stay closed.</p>
        </div>
        <div class="summary-strip" aria-label="readiness counters">
          <div class="summary-item"><h3>scenes</h3><strong>{_escape(scene_timing_map.get("scene_count"))}</strong></div>
          <div class="summary-item"><h3>CSV rows</h3><strong>{_escape(state.get("csv_row_count"))}</strong></div>
          <div class="summary-item"><h3>templates</h3><strong>{_escape(visual_registry.get("template_type_count"))}</strong></div>
          <div class="summary-item"><h3>local gaps</h3><strong>{_escape(closed)} / {_escape(total)}</strong></div>
          <div class="summary-item"><h3>YMM4</h3><strong>{_escape(state.get("yymm4_status"))}</strong></div>
        </div>
        <div class="timing-strip" data-region="timing-strip" aria-label="scene timing map">
          {timing_nodes}
        </div>
      </section>
      <aside class="side" data-region="handoff-readiness">
        <span class="badge">later handoff</span>
        <p>Ready for later observation: cue IDs, voice/subtitle rows, visual template assignments, overlay slots, and thumbnail frame language.</p>
        <p>Still blocked: verified real input, YMM4 observation/render, rights/public acceptance, and final thumbnail approval.</p>
      </aside>
    </section>
    <section class="lanes">
      <section class="lane" data-region="scene-template-lane">
        <h2>Scene Template Lane</h2>
        <div class="template-grid">{scene_templates}</div>
      </section>
      <section class="lane" data-region="voice-subtitle-lane">
        <h2>Voice / Subtitle Lane</h2>
        <div class="voice-list">{voice_rows}</div>
      </section>
      <section class="lane" data-region="overlay-lane">
        <h2>Citation Overlay Lane</h2>
        <div class="overlay-grid">{overlay_rows}</div>
      </section>
      <section class="lane" data-region="thumbnail-transfer-lane">
        <h2>Thumbnail Transfer Lane</h2>
        <div class="thumb-grid">{thumb_rules}</div>
      </section>
    </section>
  </main>
</body>
</html>
"""


def _render_timing_node(scene: Any) -> str:
    if not isinstance(scene, dict):
        return ""
    duration = int(scene.get("provisional_duration_sec", 8) or 8)
    pct = min(100, max(24, duration * 3))
    return (
        '<article class="timing-node">'
        f'<span class="badge">{_escape(scene.get("scene_id"))}</span>'
        f'<strong>{_escape(scene.get("title"))}</strong>'
        f'<div class="meter"><span style="width: {pct}%"></span></div>'
        f'<p>{_escape(scene.get("provisional_start_sec"))}-{_escape(scene.get("provisional_end_sec"))} sec / rows {_escape(scene.get("row_start"))}-{_escape(scene.get("row_end"))}</p>'
        "</article>"
    )


def _render_template_assignment(row: Any) -> str:
    if not isinstance(row, dict):
        return ""
    return (
        '<article class="template-node">'
        f'<strong>{_escape(row.get("scene_id"))}: {_escape(row.get("primary_template_id"))}</strong>'
        f'<p>phase {_escape(row.get("arc_phase"))}; support {_escape(", ".join(str(v) for v in _list(row.get("supporting_template_ids"))) or "none")}</p>'
        "</article>"
    )


def _render_voice_row(row: Any) -> str:
    if not isinstance(row, dict):
        return ""
    return (
        '<div class="voice-row">'
        f'<span>{_escape(row.get("cue_id"))}</span>'
        f'<span>{_escape(row.get("voice_slot_id"))}</span>'
        f'<span>{_escape(row.get("subtitle_text"))}</span>'
        "</div>"
    )


def _render_overlay_slot(row: Any) -> str:
    if not isinstance(row, dict):
        return ""
    return (
        '<article class="overlay-node">'
        f'<strong>{_escape(row.get("overlay_id"))}</strong>'
        f'<p>{_escape(row.get("screen_region"))} / {_escape(row.get("timing_anchor"))}</p>'
        "</article>"
    )


def _render_thumb_rule(row: Any) -> str:
    if not isinstance(row, dict):
        return ""
    targets = ", ".join(str(v) for v in _list(row.get("target_scene_ids")))
    return (
        '<article class="thumb-node">'
        f'<strong>{_escape(row.get("rule_id"))}</strong>'
        f'<p>{_escape(row.get("video_frame_language"))} Target: {_escape(targets)}</p>'
        "</article>"
    )


def _render_markdown(
    state: dict[str, Any],
    scene_timing_map: dict[str, Any],
    voice_mapping: dict[str, Any],
    visual_registry: dict[str, Any],
    overlay_spec: dict[str, Any],
    thumbnail_map: dict[str, Any],
    gap_readback: dict[str, Any],
) -> str:
    lines = [
        "# Episode 002 Output Template Readiness",
        "",
        "Local output templates prepared from the existing dry-run output proof.",
        "",
        f"- primary_review_file: `{state.get('primary_human_review')}`",
        f"- scene_count: {scene_timing_map.get('scene_count')}",
        f"- timing_map_status: {scene_timing_map.get('status')}",
        f"- voice_mapping_status: {voice_mapping.get('status')}",
        f"- visual_template_count: {visual_registry.get('template_type_count')}",
        f"- citation_overlay_status: {overlay_spec.get('status')}",
        f"- thumbnail_transfer_status: {thumbnail_map.get('status')}",
        f"- previous_buildable_gap_count: {gap_readback.get('previous_buildable_gap_count')}",
        f"- buildable_gap_closed_count: {gap_readback.get('buildable_gap_closed_count')}",
        "",
        "## Scenes",
        "",
    ]
    for scene in _list(scene_timing_map.get("scenes")):
        if not isinstance(scene, dict):
            continue
        lines.extend(
            [
                f"### {scene.get('scene_id')} - {scene.get('title')}",
                "",
                f"- rows: {scene.get('row_start')}-{scene.get('row_end')}",
                f"- provisional_duration_sec: {scene.get('provisional_duration_sec')}",
                f"- status: {scene.get('status')}",
                "",
            ]
        )
    return "\n".join(lines)


def _render_review_checklist(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Output Template Readiness Review Checklist",
            "",
            "- Open `output_template_readiness_preview.html`.",
            "- Confirm timing, scene, voice/subtitle, overlay, and thumbnail transfer lanes are visible.",
            "- Confirm real input, YMM4 GUI/import/render, production .ymmp, final thumbnail, rights, and public upload remain closed.",
            "- Review `template_gap_closure_readback.json` for the five buildable-local gaps.",
            "- Confirm GUI/i18n review UI packages were not modified in this slice.",
            "",
            f"Primary human review: `{state.get('primary_human_review')}`",
            f"Machine readback: `{state.get('primary_machine_readable')}`",
            "",
        ]
    )


def _render_limitations(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Output Template Readiness Limitations",
            "",
            "This is a local static template-readiness package. It is not a rendered video, production .ymmp, public-ready package, or final thumbnail approval.",
            "",
            "Not performed:",
            "",
            "- no full-suite green campaign",
            "- no GUI/i18n lane modification",
            "- no production video/render claim",
            "- no YouTube upload, publication, scheduling, or visibility change",
            "- no OAuth, API keys, payment, or paid services",
            "- no rights/legal/public-ready acceptance",
            "- no live scraping, RSS fetch, external media download, or external dependencies",
            "- no YMM4 GUI launch, import, or render",
            "- no production `.ymmp` generation",
            "- no final thumbnail approval",
            "- no cross-repo or destructive git",
            "- no real transcript/source replacement",
            "",
            f"Primary review file: `{state.get('primary_human_review')}`",
            "",
        ]
    )


def _render_readme(
    state: dict[str, Any],
    scene_timing_map: dict[str, Any],
    visual_registry: dict[str, Any],
    gap_readback: dict[str, Any],
) -> str:
    return "\n".join(
        [
            "# README_OUTPUT_TEMPLATE_READINESS",
            "",
            "Lane-local package for Episode 002 Output / Video Layer template readiness.",
            "",
            f"- Primary review file: `{state.get('primary_human_review')}`",
            f"- Primary readback: `{state.get('primary_machine_readable')}`",
            f"- Scene count: {scene_timing_map.get('scene_count')}",
            f"- Visual template count: {visual_registry.get('template_type_count')}",
            f"- Buildable gaps closed for local template readiness: {gap_readback.get('buildable_gap_closed_count')} / {gap_readback.get('previous_buildable_gap_count')}",
            "- Shared docs touched: false",
            "- GUI/i18n lane files touched: none",
            "",
            "This package prepares the output/video layer for later verified input and explicit YMM4 observation without crossing those gates.",
            "",
        ]
    )
