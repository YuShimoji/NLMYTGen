"""Output/video layer proof package for episode 002."""

from __future__ import annotations

import csv
import html
import json
import re
from pathlib import Path
from typing import Any

from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
    TEMPORARY_COPY_MARKERS,
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

DEFAULT_OUTPUT_DIRNAME = "output_video_layer_proof"
DEFAULT_ARTIFACT_ID = "episode_002_output_video_layer_proof_v1"

IR_BRIDGE_DIRNAME = "ir_bridge"
TRANSCRIPT_READINESS_DIRNAME = "transcript_substitution_readiness"
IMPORT_PREVIEW_DIRNAME = "ymm4_import_preview_pack"
THUMBNAIL_PROOF_DIRNAME = "thumbnail_visual_proof_pack"
JAPANESE_GRAPHIC_CONSOLE_DIRNAME = "japanese_graphic_review_console"

REQUIRED_OUTPUT_VIDEO_FILES = (
    "output_video_proof_manifest.json",
    "episode_002_storyboard_preview.html",
    "episode_002_storyboard_preview.md",
    "scene_timeline.json",
    "draft_yukkuri_narration_outline.md",
    "yymm4_handoff_readiness.json",
    "output_gap_ledger.json",
    "missing_editing_features.md",
    "source_artifact_index.json",
    "validation_readback.json",
    "review_checklist.md",
    "limitations.md",
    "README_OUTPUT_VIDEO_LAYER_PROOF.md",
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
    "blocked_by_yymm4_gate",
    "blocked_by_public_rights_gate",
)

PROTECTED_GUI_LANE_DIRS = (
    "production_pilots/yukkuri_newsroom_content_spine_002/japanese_graphic_review_console",
    "production_pilots/yukkuri_newsroom_content_spine_002/primary_artifact_review_console",
    "production_pilots/yukkuri_newsroom_content_spine_002/review_console_redesign_prototype",
)


def build_output_video_layer_proof(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build the local output/video layer proof package."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root)
    payloads = _load_payloads(paths)
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
    scene_timeline = _scene_timeline(state)
    gap_ledger = _output_gap_ledger(state)
    handoff = _yymm4_handoff_readiness(state, scene_timeline, gap_ledger)
    source_index = _source_artifact_index(state)
    manifest = _manifest(state, scene_timeline, gap_ledger, output_root, repo_root)

    _write_json(output_root / "output_video_proof_manifest.json", manifest)
    _write_json(output_root / "scene_timeline.json", scene_timeline)
    _write_json(output_root / "yymm4_handoff_readiness.json", handoff)
    _write_json(output_root / "output_gap_ledger.json", gap_ledger)
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_text(output_root / "episode_002_storyboard_preview.html", _render_html(state, scene_timeline, gap_ledger, handoff))
    _write_text(output_root / "episode_002_storyboard_preview.md", _render_storyboard_markdown(state, scene_timeline, gap_ledger))
    _write_text(output_root / "draft_yukkuri_narration_outline.md", _render_narration_outline(state, scene_timeline))
    _write_text(output_root / "missing_editing_features.md", _render_missing_features(gap_ledger))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state))
    _write_text(output_root / "limitations.md", _render_limitations(state))
    _write_text(output_root / "README_OUTPUT_VIDEO_LAYER_PROOF.md", _render_readme(state, scene_timeline, gap_ledger))

    readback = validate_output_video_layer_proof(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_output_video_layer_proof(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_output_video_layer_proof(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated output/video layer proof package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_OUTPUT_VIDEO_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["output_video_proof_manifest.json"])
    scene_timeline = _load_json_if_present(files["scene_timeline.json"])
    handoff = _load_json_if_present(files["yymm4_handoff_readiness.json"])
    gap_ledger = _load_json_if_present(files["output_gap_ledger.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])
    json_payloads = {
        "output_video_proof_manifest": manifest,
        "scene_timeline": scene_timeline,
        "yymm4_handoff_readiness": handoff,
        "output_gap_ledger": gap_ledger,
        "source_artifact_index": source_index,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = _dict(json_payloads["output_video_proof_manifest"])
    scene_timeline = _dict(json_payloads["scene_timeline"])
    handoff = _dict(json_payloads["yymm4_handoff_readiness"])
    gap_ledger = _dict(json_payloads["output_gap_ledger"])
    source_index = _dict(json_payloads["source_artifact_index"])
    html_text = files["episode_002_storyboard_preview.html"].read_text(encoding="utf-8") if files["episode_002_storyboard_preview.html"].exists() else ""
    markdown_text = files["episode_002_storyboard_preview.md"].read_text(encoding="utf-8") if files["episode_002_storyboard_preview.md"].exists() else ""
    missing_features_text = files["missing_editing_features.md"].read_text(encoding="utf-8") if files["missing_editing_features.md"].exists() else ""

    scenes = [row for row in _list(scene_timeline.get("scenes")) if isinstance(row, dict)]
    features = [row for row in _list(gap_ledger.get("features")) if isinstance(row, dict)]
    groups = _dict(gap_ledger.get("groups"))
    group_counts = _dict(gap_ledger.get("group_counts"))
    boundary_flags = _dict(manifest.get("boundary_flags"))
    gui_touches = _list(manifest.get("gui_lane_files_touched"))

    if manifest.get("artifact_kind") != "episode-output-video-layer-proof":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "output_video_layer_proof_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")
    if len(scenes) < 3:
        failed_checks.append("scene_timeline_too_short")
    if not features:
        failed_checks.append("output_gap_ledger_empty")
    for group in REQUIRED_GAP_GROUPS:
        if not _list(groups.get(group)):
            failed_checks.append(f"missing_feature_group_empty:{group}")
        if f"## {group}" not in missing_features_text:
            failed_checks.append(f"missing_features_markdown_group_absent:{group}")

    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")

    if not files["episode_002_storyboard_preview.html"].exists():
        failed_checks.append("storyboard_html_missing")
    if not markdown_text.strip():
        failed_checks.append("storyboard_markdown_empty")
    if 'data-output-video-proof="true"' not in html_text:
        failed_checks.append("output_video_proof_marker_missing")
    if 'data-region="storyboard-timeline"' not in html_text:
        failed_checks.append("storyboard_timeline_region_missing")
    if 'data-region="gap-ledger"' not in html_text:
        failed_checks.append("gap_ledger_region_missing")
    if "color-scheme: dark light" not in html_text:
        failed_checks.append("dark_color_scheme_missing")
    if "prefers-color-scheme" not in html_text:
        failed_checks.append("prefers_color_scheme_missing")
    if "#ffffff" in html_text.lower() or "#fff" in html_text.lower():
        failed_checks.append("pure_white_background_marker_present")
    if handoff.get("actual_yymm4_import") is not False:
        failed_checks.append("actual_yymm4_import_not_false")
    if handoff.get("yymm4_rendered") is not False:
        failed_checks.append("yymm4_rendered_not_false")
    if handoff.get("production_ready") is not False:
        failed_checks.append("production_ready_not_false")
    if manifest.get("shared_docs_touched") is not False:
        failed_checks.append("shared_docs_touched_not_false")
    if gui_touches:
        failed_checks.append("gui_lane_files_touched_not_empty")
    if source_index.get("gui_lane_context_read_only") is not True:
        failed_checks.append("gui_lane_context_not_read_only")

    external_refs = _external_refs_in_files([path for name, path in files.items() if name != "validation_readback.json"])
    forbidden_hits = _forbidden_true_claims(root)
    temporary_hits = _temporary_copy_hits(
        [
            files["episode_002_storyboard_preview.html"],
            files["episode_002_storyboard_preview.md"],
            files["draft_yukkuri_narration_outline.md"],
            files["missing_editing_features.md"],
            files["README_OUTPUT_VIDEO_LAYER_PROOF.md"],
        ]
    )
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "storyboard_html_exists": files["episode_002_storyboard_preview.html"].exists(),
        "storyboard_markdown_exists": files["episode_002_storyboard_preview.md"].exists(),
        "scene_count": len(scenes),
        "gap_ledger_feature_count": len(features),
        "missing_feature_groups": {group: len(_list(groups.get(group))) for group in REQUIRED_GAP_GROUPS},
        "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS),
        "gui_lane_files_touched": gui_touches,
        "shared_docs_touched": manifest.get("shared_docs_touched"),
        "external_dependency_status": "none_found" if not external_refs else "found",
        "forbidden_true_claims_absent": not forbidden_hits,
        "temporary_copy_absent": not temporary_hits,
    }
    return {
        "schema_version": "output_video_layer_proof_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "primary_review_file": str(root / "episode_002_storyboard_preview.html"),
        "primary_human_review": str(root / "episode_002_storyboard_preview.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "scene_count": len(scenes),
        "timeline_source": scene_timeline.get("timeline_source"),
        "draft_csv_used": scene_timeline.get("draft_csv_used"),
        "real_transcript_status": manifest.get("real_transcript_status"),
        "yymm4_status": handoff.get("yymm4_status"),
        "missing_feature_count": len(features),
        "buildable_local_count": int(group_counts.get("buildable_locally", 0) or 0),
        "blocked_by_real_input_count": int(group_counts.get("blocked_by_real_input", 0) or 0),
        "blocked_by_yymm4_gate_count": int(group_counts.get("blocked_by_yymm4_gate", 0) or 0),
        "blocked_by_public_rights_count": int(group_counts.get("blocked_by_public_rights_gate", 0) or 0),
        "gui_lane_files_touched": gui_touches,
        "shared_docs_touched": manifest.get("shared_docs_touched"),
        "full_pytest_run": False,
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{(root / "episode_002_storyboard_preview.html").resolve()}"',
        "access_state": "verified_present" if (root / "episode_002_storyboard_preview.html").exists() else "missing",
        "next_action": manifest.get("next_action"),
    }


def _input_paths(source_root: Path) -> dict[str, Path]:
    ir_root = source_root / IR_BRIDGE_DIRNAME
    transcript_root = source_root / TRANSCRIPT_READINESS_DIRNAME
    import_root = source_root / IMPORT_PREVIEW_DIRNAME
    thumbnail_root = source_root / THUMBNAIL_PROOF_DIRNAME
    gui_root = source_root / JAPANESE_GRAPHIC_CONSOLE_DIRNAME
    return {
        "ir_root": ir_root,
        "episode_bridge": ir_root / "episode_bridge.json",
        "writer_ir": ir_root / "writer_ir_candidate.json",
        "cue_packet": ir_root / "cue_packet_candidate.json",
        "ir_draft_csv": ir_root / "draft_yymm4.csv",
        "ir_validation": ir_root / "validation_readback.json",
        "transcript_root": transcript_root,
        "transcript_validation": transcript_root / "validation_readback.json",
        "transcript_csv": transcript_root / "regenerated_draft_yymm4.csv",
        "real_input_dir": transcript_root / "real_input",
        "import_root": import_root,
        "import_summary": import_root / "import_readiness_summary.json",
        "csv_inventory": import_root / "yymm4_csv_inventory.json",
        "import_panel": import_root / "import_preview_panel.md",
        "thumbnail_root": thumbnail_root,
        "thumbnail_variants": thumbnail_root / "thumbnail_variants.json",
        "thumbnail_html": thumbnail_root / "thumbnail_visual_proof.html",
        "japanese_console_validation": gui_root / "validation_readback.json",
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "episode_bridge": _load_json_if_present(paths["episode_bridge"]),
        "writer_ir": _load_json_if_present(paths["writer_ir"]),
        "cue_packet": _load_json_if_present(paths["cue_packet"]),
        "ir_validation": _load_json_if_present(paths["ir_validation"]),
        "transcript_validation": _load_json_if_present(paths["transcript_validation"]),
        "import_summary": _load_json_if_present(paths["import_summary"]),
        "csv_inventory": _load_json_if_present(paths["csv_inventory"]),
        "thumbnail_variants": _load_json_if_present(paths["thumbnail_variants"]),
        "japanese_console_validation": _load_json_if_present(paths["japanese_console_validation"]),
    }


def _select_draft_csv(paths: dict[str, Path]) -> Path:
    if paths["transcript_csv"].exists():
        return paths["transcript_csv"]
    return paths["ir_draft_csv"]


def _read_csv_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for index, row in enumerate(csv.reader(handle), start=1):
            if not row:
                continue
            speaker = row[0] if len(row) > 0 else ""
            text = row[1] if len(row) > 1 else ""
            rows.append({"row_number": index, "speaker": speaker, "text": text})
    return rows


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
    episode_bridge = _dict(payloads.get("episode_bridge"))
    writer_ir = _dict(payloads.get("writer_ir"))
    import_summary = _dict(payloads.get("import_summary"))
    csv_inventory = _dict(payloads.get("csv_inventory"))
    thumbnail_variants = _dict(payloads.get("thumbnail_variants"))
    boundary_status = _dict(import_summary.get("boundary_status"))
    return {
        "schema_version": "output_video_layer_proof_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-output-video-layer-proof",
        "status": "output_video_layer_proof_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "episode_title": episode_bridge.get("selected_title")
        or "Factory seed dry-run placeholder for a second yukkuri newsroom episode",
        "selected_candidate_id": episode_bridge.get("selected_candidate_id") or "factory_seed_dry_run_002",
        "csv_path": _relpath(csv_path, repo_root),
        "csv_rows": csv_rows,
        "csv_row_count": len(csv_rows) or int(csv_inventory.get("row_count", 0) or 0),
        "sections": _list(writer_ir.get("sections")) or _list(episode_bridge.get("sections")),
        "utterances": _list(writer_ir.get("utterances")) or _list(episode_bridge.get("draft_dialogue")),
        "thumbnail_recommended_variant": thumbnail_variants.get("recommended_variant_id"),
        "thumbnail_variant_count": thumbnail_variants.get("variant_count"),
        "real_transcript_status": boundary_status.get("real_transcript_status", "blocked_by_real_input"),
        "yymm4_status": boundary_status.get("yymm4_import_observed_status", "not_imported_to_yymm4"),
        "boundary_flags": _boundary_flags(import_summary),
        "paths": {name: _relpath(path, repo_root) for name, path in paths.items() if isinstance(path, Path)},
        "primary_human_review": _relpath(output_root / "episode_002_storyboard_preview.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_action": "Review episode_002_storyboard_preview.html and output_gap_ledger.json; this proof keeps real input, YMM4 import/render, and public gates closed.",
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


def _scene_timeline(state: dict[str, Any]) -> dict[str, Any]:
    scenes = _scenes_from_sections(state)
    return {
        "schema_version": "episode_002_scene_timeline.v1",
        "artifact_id": state.get("artifact_id"),
        "timeline_source": "writer_ir_sections_plus_regenerated_draft_yymm4_csv",
        "draft_csv_used": state.get("csv_path"),
        "scene_count": len(scenes),
        "csv_row_count": state.get("csv_row_count"),
        "timing_model": "rough_estimate_only_not_yymm4_timing",
        "total_estimated_duration_sec": sum(int(scene.get("estimated_duration_sec", 0) or 0) for scene in scenes),
        "real_transcript_status": state.get("real_transcript_status"),
        "yymm4_status": state.get("yymm4_status"),
        "scenes": scenes,
    }


def _scenes_from_sections(state: dict[str, Any]) -> list[dict[str, Any]]:
    sections = [row for row in _list(state.get("sections")) if isinstance(row, dict)]
    utterances = [row for row in _list(state.get("utterances")) if isinstance(row, dict)]
    csv_rows = [row for row in _list(state.get("csv_rows")) if isinstance(row, dict)]
    if not sections:
        sections = _fallback_sections(csv_rows)
    scenes: list[dict[str, Any]] = []
    cursor = 0
    for index, section in enumerate(sections, start=1):
        start_index = int(section.get("start_index", index) or index)
        end_index = int(section.get("end_index", start_index) or start_index)
        section_utterances = [
            row for row in utterances if start_index <= int(row.get("index", 0) or 0) <= end_index
        ]
        if not section_utterances:
            section_utterances = [
                row for row in csv_rows if start_index <= int(row.get("row_number", 0) or 0) <= end_index
            ]
        row_count = max(1, len(section_utterances))
        duration = max(8, row_count * 4)
        scene_id = str(section.get("section_id") or f"S{index}")
        preview_lines = [
            str(row.get("text", "")).strip()
            for row in section_utterances[:2]
            if str(row.get("text", "")).strip()
        ]
        scenes.append(
            {
                "scene_id": scene_id,
                "beat_index": index,
                "title": section.get("topic") or f"Scene {index}",
                "arc_phase": section.get("arc_phase") or "proof",
                "row_start": start_index,
                "row_end": end_index,
                "utterance_count": row_count,
                "speakers": sorted(
                    {
                        str(row.get("speaker") or row.get("mapped_speaker") or "").strip()
                        for row in section_utterances
                        if str(row.get("speaker") or row.get("mapped_speaker") or "").strip()
                    }
                ),
                "default_bg": section.get("default_bg"),
                "default_face": section.get("default_face"),
                "bgm": section.get("bgm"),
                "narration_preview": preview_lines,
                "visual_intent": _visual_intent_for_phase(str(section.get("arc_phase") or "")),
                "estimated_start_sec": cursor,
                "estimated_end_sec": cursor + duration,
                "estimated_duration_sec": duration,
                "timing_status": "estimated_only_no_audio_or_yymm4_timing",
                "output_readiness": "storyboard_ready_local_offline",
                "missing_for_real_video": [
                    "real source/transcript",
                    "YMM4 timing observation",
                    "visual scene template",
                ],
            }
        )
        cursor += duration
    return scenes


def _fallback_sections(csv_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    total = max(3, len(csv_rows))
    return [
        {"section_id": "S1", "topic": "Opening", "start_index": 1, "end_index": max(1, total // 3), "arc_phase": "intro"},
        {
            "section_id": "S2",
            "topic": "Main explanation",
            "start_index": max(2, total // 3 + 1),
            "end_index": max(2, total * 2 // 3),
            "arc_phase": "develop",
        },
        {
            "section_id": "S3",
            "topic": "Boundary and next work",
            "start_index": max(3, total * 2 // 3 + 1),
            "end_index": total,
            "arc_phase": "closing",
        },
    ]


def _visual_intent_for_phase(phase: str) -> str:
    if phase == "intro":
        return "topic hook, title proof, speaker setup"
    if phase == "develop":
        return "diagram view, template registry, inherited defaults split"
    if phase == "closing":
        return "readiness strip, closed gates, next material requirement"
    return "storyboard placeholder for local proof"


def _output_gap_ledger(state: dict[str, Any]) -> dict[str, Any]:
    features = [
        _feature("timing_alignment", "buildable_locally", "Scene durations are rough estimates.", "Create timing readback from narration rows and future audio/YMM4 observation."),
        _feature("voice_item_mapping", "buildable_locally", "Speaker rows exist but no VoiceItem mapping proof exists.", "Map speakers to YMM4 voice item assumptions without importing."),
        _feature("visual_scene_template", "buildable_locally", "Sections have default bg/face labels only.", "Create a local scene-template proof for intro/develop/closing beats."),
        _feature("citation_source_overlay", "buildable_locally", "No source/citation overlay contract exists for a real episode.", "Define overlay slots that can accept reviewed source notes later."),
        _feature("thumbnail_transfer", "buildable_locally", "Thumbnail proof exists as context only.", "Record how selected thumbnail direction would transfer into a video package."),
        _feature("verified_source_transcript_intake", "blocked_by_real_input", "Current transcript is sample_fixture_not_real.", "Provide reviewed local source/transcript material."),
        _feature("real_source_rights_context", "blocked_by_real_input", "Source is offline fixture, not live reviewed material.", "Attach source context and rights status before production use."),
        _feature("yymm4_import_observation", "blocked_by_yymm4_gate", "Draft CSV has not been imported to YMM4.", "Explicit human gate required for import observation without render."),
        _feature("voiceitem_timing_readback", "blocked_by_yymm4_gate", "No VoiceItem timing exists.", "Read timing only after explicit YMM4 observation."),
        _feature("render_smoke", "blocked_by_yymm4_gate", "No render was performed.", "Render smoke remains closed until explicit YMM4/render gate."),
        _feature("public_rights_acceptance", "blocked_by_public_rights_gate", "No rights/legal/public-ready acceptance exists.", "Human rights/public review required."),
        _feature("youtube_visibility_package", "blocked_by_public_rights_gate", "No upload/visibility action is allowed.", "Public metadata and upload remain closed."),
        _feature("final_thumbnail_approval", "blocked_by_public_rights_gate", "Thumbnail proof is contextual only.", "Human final thumbnail approval required."),
    ]
    groups: dict[str, list[str]] = {group: [] for group in REQUIRED_GAP_GROUPS}
    for feature in features:
        groups.setdefault(str(feature["category"]), []).append(str(feature["feature_id"]))
    return {
        "schema_version": "output_gap_ledger.v1",
        "artifact_id": state.get("artifact_id"),
        "purpose": "Identify what is still needed to turn Episode 002 into a real yukkuri video.",
        "features": features,
        "groups": groups,
        "group_counts": {group: len(rows) for group, rows in groups.items()},
        "missing_feature_count": len(features),
    }


def _feature(feature_id: str, category: str, current_state: str, next_needed: str) -> dict[str, str]:
    return {
        "feature_id": feature_id,
        "category": category,
        "current_state": current_state,
        "needed_for_video": next_needed,
    }


def _yymm4_handoff_readiness(
    state: dict[str, Any],
    scene_timeline: dict[str, Any],
    gap_ledger: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "yymm4_handoff_readiness.v1",
        "artifact_id": state.get("artifact_id"),
        "status": "local_preview_only_not_yymm4_import_ready",
        "draft_csv_used": state.get("csv_path"),
        "draft_csv_rows": state.get("csv_row_count"),
        "scene_count": scene_timeline.get("scene_count"),
        "available_now": [
            "draft YMM4 CSV preview",
            "writer IR candidate",
            "cue packet candidate",
            "thumbnail proof context",
            "storyboard/timeline preview",
        ],
        "missing_before_real_video": [
            "verified source/transcript",
            "timing alignment",
            "voice item mapping",
            "visual scene template",
            "citation/source overlay",
            "YMM4 import observation",
            "render smoke",
            "public/rights acceptance",
        ],
        "gap_group_counts": gap_ledger.get("group_counts"),
        "actual_yymm4_import": False,
        "yymm4_rendered": False,
        "production_ready": False,
        "public_ready": False,
        "yymm4_status": state.get("yymm4_status"),
        "real_transcript_status": state.get("real_transcript_status"),
        "gate_policy": "YMM4 GUI/import/render remain closed until an explicit human gate.",
    }


def _source_artifact_index(state: dict[str, Any]) -> dict[str, Any]:
    paths = _dict(state.get("paths"))
    records = [
        _source_record("episode_bridge", paths.get("episode_bridge"), "story_source", True),
        _source_record("writer_ir_candidate", paths.get("writer_ir"), "story_source", True),
        _source_record("cue_packet_candidate", paths.get("cue_packet"), "story_source", True),
        _source_record("draft_yymm4_csv", state.get("csv_path"), "draft_csv_source", True),
        _source_record("transcript_validation", paths.get("transcript_validation"), "input_boundary", True),
        _source_record("import_readiness_summary", paths.get("import_summary"), "handoff_boundary", True),
        _source_record("yymm4_csv_inventory", paths.get("csv_inventory"), "handoff_boundary", True),
        _source_record("thumbnail_variants", paths.get("thumbnail_variants"), "thumbnail_context", True),
        _source_record("japanese_graphic_console_validation", paths.get("japanese_console_validation"), "gui_context_read_only", True),
    ]
    return {
        "schema_version": "output_video_source_artifact_index.v1",
        "artifact_id": state.get("artifact_id"),
        "gui_lane_context_read_only": True,
        "protected_gui_lane_dirs": list(PROTECTED_GUI_LANE_DIRS),
        "records": records,
    }


def _source_record(record_id: str, path: Any, role: str, exists_expected: bool) -> dict[str, Any]:
    text = str(path or "")
    return {
        "record_id": record_id,
        "repo_relative_path": text,
        "role": role,
        "exists_expected": exists_expected,
        "display_zone": "source_artifact_index",
    }


def _manifest(
    state: dict[str, Any],
    scene_timeline: dict[str, Any],
    gap_ledger: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    group_counts = _dict(gap_ledger.get("group_counts"))
    return {
        "schema_version": "output_video_proof_manifest.v1",
        "artifact_id": state.get("artifact_id"),
        "artifact_kind": "episode-output-video-layer-proof",
        "status": "output_video_layer_proof_ready_local_offline",
        "parallel_lane": "output_video_layer",
        "output_dir": _relpath(output_root, repo_root),
        "files": {
            filename: _relpath(output_root / filename, repo_root)
            for filename in REQUIRED_OUTPUT_VIDEO_FILES
        },
        "primary_review_file": state.get("primary_human_review"),
        "primary_human_review": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "scene_count": scene_timeline.get("scene_count"),
        "timeline_source": scene_timeline.get("timeline_source"),
        "draft_csv_used": scene_timeline.get("draft_csv_used"),
        "real_transcript_status": state.get("real_transcript_status"),
        "yymm4_status": state.get("yymm4_status"),
        "missing_feature_count": gap_ledger.get("missing_feature_count"),
        "buildable_local_count": group_counts.get("buildable_locally", 0),
        "blocked_by_real_input_count": group_counts.get("blocked_by_real_input", 0),
        "blocked_by_yymm4_gate_count": group_counts.get("blocked_by_yymm4_gate", 0),
        "blocked_by_public_rights_count": group_counts.get("blocked_by_public_rights_gate", 0),
        "gui_lane_files_touched": [],
        "shared_docs_touched": False,
        "boundary_flags": state.get("boundary_flags"),
        "production_video_rendered": False,
        "production_ready": False,
        "next_action": state.get("next_action"),
    }


def _render_html(
    state: dict[str, Any],
    scene_timeline: dict[str, Any],
    gap_ledger: dict[str, Any],
    handoff: dict[str, Any],
) -> str:
    scenes = "\n".join(_render_scene(scene) for scene in _list(scene_timeline.get("scenes")))
    groups = _dict(gap_ledger.get("groups"))
    group_columns = "\n".join(_render_gap_group(group, _list(groups.get(group))) for group in REQUIRED_GAP_GROUPS)
    total_sec = scene_timeline.get("total_estimated_duration_sec")
    return f"""<!doctype html>
<html lang="ja" data-output-video-proof="true" data-artifact-kind="episode-output-video-layer-proof">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Output Video Layer Proof</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #0c1116;
      --surface: #182129;
      --stage: #101820;
      --panel: #141b22;
      --line: #50606d;
      --text: #f3efe7;
      --muted: #c2baad;
      --accent: #73dfcf;
      --action: #9fc5ff;
      --warn: #f1cf6a;
      --closed: #ef9f9f;
      --ok: #9ee8bc;
      --shadow: 0 18px 44px rgba(0, 0, 0, 0.34);
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #eef2ef;
        --surface: #e2e9e5;
        --stage: #f7f2e8;
        --panel: #efede5;
        --line: #aeb9b3;
        --text: #1d231f;
        --muted: #5d665f;
        --accent: #0f766e;
        --action: #1d4ed8;
        --warn: #8a5a00;
        --closed: #9b1c1c;
        --ok: #047857;
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
    button {{ font: inherit; }}
    .wrap {{
      width: min(1360px, calc(100% - 28px));
      margin: 0 auto;
      padding: 16px 0 32px;
    }}
    .topline {{
      display: grid;
      grid-template-columns: minmax(280px, 1fr) auto;
      gap: 12px;
      align-items: center;
      padding: 10px 0 14px;
    }}
    .identity, .nav, .badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }}
    .nav {{ justify-content: flex-end; }}
    .episode {{ font-size: 1.08rem; font-weight: 760; }}
    .badge, .gate {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 3px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--panel);
      color: var(--accent);
      font-size: 0.76rem;
      font-weight: 720;
      white-space: nowrap;
    }}
    .gate {{ color: var(--closed); }}
    .nav button {{
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--surface);
      color: var(--text);
      padding: 7px 10px;
      cursor: pointer;
    }}
    .layout {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(320px, 0.34fr);
      gap: 14px;
      align-items: stretch;
    }}
    .storyboard, .side, .gap-ledger, .handoff {{
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      background: var(--surface);
    }}
    .storyboard {{
      min-height: 640px;
      padding: 16px;
      display: grid;
      grid-template-rows: auto auto 1fr;
      gap: 14px;
    }}
    .side {{
      padding: 16px;
      display: grid;
      gap: 13px;
      align-content: start;
      background: var(--panel);
    }}
    h1, h2, h3, p {{ margin: 0; }}
    h1 {{ font-size: clamp(1.45rem, 2.3vw, 2.2rem); line-height: 1.08; letter-spacing: 0; }}
    h2 {{ font-size: 1rem; letter-spacing: 0; }}
    h3 {{ font-size: 0.82rem; color: var(--muted); letter-spacing: 0; }}
    p, li, span {{ line-height: 1.4; }}
    p, li {{ color: var(--muted); }}
    .summary-strip {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 8px;
    }}
    .summary-item {{
      border-left: 3px solid var(--accent);
      padding: 7px 9px;
      background: rgba(255, 255, 255, 0.035);
      min-width: 0;
    }}
    .summary-item strong {{ display: block; color: var(--text); }}
    .scene-rail {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }}
    .scene-panel {{
      min-width: 0;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--stage);
      padding: 12px;
      display: grid;
      grid-template-rows: auto auto 1fr auto;
      gap: 10px;
    }}
    .scene-panel strong {{ color: var(--text); }}
    .phase-bar {{
      height: 8px;
      border-radius: 999px;
      background: var(--line);
      overflow: hidden;
    }}
    .phase-bar span {{
      display: block;
      height: 100%;
      background: var(--accent);
    }}
    .rows {{
      display: grid;
      gap: 5px;
      min-height: 80px;
    }}
    .dialogue-row {{
      border-left: 3px solid var(--action);
      padding: 6px 7px;
      background: rgba(255, 255, 255, 0.035);
      color: var(--muted);
      font-size: 0.84rem;
    }}
    .timeline {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 8px;
    }}
    .timeline-node {{
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 8px;
      background: rgba(255, 255, 255, 0.035);
      min-width: 0;
    }}
    .timeline-node strong {{ color: var(--text); display: block; }}
    .table {{
      display: grid;
      gap: 6px;
    }}
    .table-row {{
      display: grid;
      grid-template-columns: 112px 1fr;
      gap: 8px;
      padding: 7px 0;
      border-bottom: 1px solid var(--line);
    }}
    .table-row span:first-child {{ color: var(--muted); }}
    .table-row span:last-child {{ color: var(--text); }}
    .gap-ledger, .handoff {{
      margin-top: 14px;
      padding: 14px;
    }}
    .gap-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-top: 10px;
    }}
    .gap-group {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.035);
      padding: 10px;
      min-width: 0;
    }}
    .gap-group ul {{ margin: 8px 0 0; padding-left: 18px; }}
    code {{ color: var(--action); overflow-wrap: anywhere; font-size: 0.84rem; }}
    @media (max-width: 1100px) {{
      .topline, .layout {{ grid-template-columns: 1fr; }}
      .nav {{ justify-content: flex-start; }}
      .summary-strip, .scene-rail, .timeline, .gap-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <header class="topline" data-region="header">
      <div class="identity">
        <span class="episode">Episode 002</span>
        <span class="badge">Output / Video Layer</span>
        <span class="badge">local proof</span>
        <span class="badge">sample fixture</span>
      </div>
      <nav class="nav" data-region="navigation" aria-label="proof navigation">
        <button type="button" data-jump="storyboard">storyboard</button>
        <button type="button" data-jump="gaps">gaps</button>
        <button type="button" data-jump="handoff">handoff</button>
      </nav>
    </header>
    <section class="layout">
      <section class="storyboard" id="storyboard" data-region="storyboard-timeline">
        <div>
          <h1>{_escape(state.get("episode_title"))}</h1>
          <p>Existing dry-run IR/CSV artifacts are assembled into a local storyboard and timeline preview. No YMM4 import, render, or public gate is crossed.</p>
        </div>
        <div class="summary-strip" aria-label="proof summary">
          <div class="summary-item"><h3>scenes</h3><strong>{_escape(scene_timeline.get("scene_count"))}</strong></div>
          <div class="summary-item"><h3>CSV rows</h3><strong>{_escape(state.get("csv_row_count"))}</strong></div>
          <div class="summary-item"><h3>estimated time</h3><strong>{_escape(total_sec)} sec</strong></div>
          <div class="summary-item"><h3>real input</h3><strong>{_escape(state.get("real_transcript_status"))}</strong></div>
        </div>
        <div class="scene-rail" aria-label="storyboard scenes">
          {scenes}
        </div>
      </section>
      <aside class="side" data-region="readiness-panel">
        <span class="badge">readiness</span>
        <div class="table" aria-label="readiness table">
          <div class="table-row"><span>timeline</span><span>{_escape(scene_timeline.get("timeline_source"))}</span></div>
          <div class="table-row"><span>draft CSV</span><span>{_escape(state.get("csv_path"))}</span></div>
          <div class="table-row"><span>YMM4</span><span>{_escape(handoff.get("yymm4_status"))}</span></div>
          <div class="table-row"><span>thumbnail</span><span>{_escape(state.get("thumbnail_recommended_variant"))}</span></div>
        </div>
        <div class="badges" aria-label="closed gates">
          <span class="gate">no import</span>
          <span class="gate">no render</span>
          <span class="gate">no public</span>
          <span class="gate">no rights approval</span>
        </div>
      </aside>
    </section>
    <section class="gap-ledger" id="gaps" data-region="gap-ledger">
      <h2>Missing output/editing features</h2>
      <p>The ledger is secondary to the storyboard preview; it names the concrete work still needed for a real yukkuri video.</p>
      <div class="gap-grid">
        {group_columns}
      </div>
    </section>
    <section class="handoff" id="handoff" data-region="handoff-readiness">
      <h2>YMM4 handoff readiness</h2>
      <div class="timeline" aria-label="handoff ladder">
        <div class="timeline-node"><h3>now</h3><strong>storyboard proof</strong><span>local preview only</span></div>
        <div class="timeline-node"><h3>input</h3><strong>real source needed</strong><span>blocked by real input</span></div>
        <div class="timeline-node"><h3>timing</h3><strong>voice mapping</strong><span>buildable locally</span></div>
        <div class="timeline-node"><h3>gate</h3><strong>YMM4 observation</strong><span>explicit choice only</span></div>
        <div class="timeline-node"><h3>public</h3><strong>closed</strong><span>rights and upload blocked</span></div>
      </div>
    </section>
  </main>
  <script>
    for (const button of document.querySelectorAll('[data-jump]')) {{
      button.addEventListener('click', () => {{
        const target = document.getElementById(button.dataset.jump);
        if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }});
    }}
  </script>
</body>
</html>
"""


def _render_scene(scene: Any) -> str:
    if not isinstance(scene, dict):
        return ""
    preview = "\n".join(
        f'<div class="dialogue-row">{_escape(line)}</div>'
        for line in _list(scene.get("narration_preview"))
    )
    pct = min(100, max(20, int(scene.get("estimated_duration_sec", 8) or 8) * 3))
    return (
        '<article class="scene-panel">'
        f'<span class="badge">{_escape(scene.get("scene_id"))}</span>'
        f'<div><h2>{_escape(scene.get("title"))}</h2><p>{_escape(scene.get("visual_intent"))}</p></div>'
        f'<div class="rows">{preview}</div>'
        f'<div><div class="phase-bar"><span style="width: {pct}%"></span></div>'
        f'<p>{_escape(scene.get("estimated_start_sec"))}-{_escape(scene.get("estimated_end_sec"))} sec / rows {_escape(scene.get("row_start"))}-{_escape(scene.get("row_end"))}</p></div>'
        "</article>"
    )


def _render_gap_group(group: str, feature_ids: list[Any]) -> str:
    items = "\n".join(f"<li>{_escape(feature_id)}</li>" for feature_id in feature_ids)
    return (
        '<section class="gap-group">'
        f"<h3>{_escape(group)}</h3>"
        f"<ul>{items}</ul>"
        "</section>"
    )


def _render_storyboard_markdown(
    state: dict[str, Any],
    scene_timeline: dict[str, Any],
    gap_ledger: dict[str, Any],
) -> str:
    lines = [
        "# Episode 002 Output / Video Layer Proof",
        "",
        "Local storyboard/timeline preview assembled from existing dry-run Episode 002 artifacts.",
        "",
        f"- primary_review_file: `{state.get('primary_human_review')}`",
        f"- scene_count: {scene_timeline.get('scene_count')}",
        f"- timeline_source: {scene_timeline.get('timeline_source')}",
        f"- draft_csv_used: `{scene_timeline.get('draft_csv_used')}`",
        f"- real_transcript_status: {state.get('real_transcript_status')}",
        f"- yymm4_status: {state.get('yymm4_status')}",
        f"- missing_feature_count: {gap_ledger.get('missing_feature_count')}",
        "",
        "## Scenes",
        "",
    ]
    for scene in _list(scene_timeline.get("scenes")):
        if not isinstance(scene, dict):
            continue
        lines.extend(
            [
                f"### {scene.get('scene_id')} - {scene.get('title')}",
                "",
                f"- rows: {scene.get('row_start')}-{scene.get('row_end')}",
                f"- estimate: {scene.get('estimated_duration_sec')} sec",
                f"- visual intent: {scene.get('visual_intent')}",
                f"- timing status: {scene.get('timing_status')}",
                "",
            ]
        )
    return "\n".join(lines)


def _render_narration_outline(state: dict[str, Any], scene_timeline: dict[str, Any]) -> str:
    lines = [
        "# Draft Yukkuri Narration Outline",
        "",
        "Boundary: sample_fixture_not_real and no_real_transcript remain true.",
        "",
    ]
    for scene in _list(scene_timeline.get("scenes")):
        if not isinstance(scene, dict):
            continue
        lines.extend([f"## {scene.get('scene_id')} - {scene.get('title')}", ""])
        for line in _list(scene.get("narration_preview")):
            lines.append(f"- {line}")
        lines.append("")
    return "\n".join(lines)


def _render_missing_features(gap_ledger: dict[str, Any]) -> str:
    groups = _dict(gap_ledger.get("groups"))
    features_by_id = {
        str(row.get("feature_id")): row
        for row in _list(gap_ledger.get("features"))
        if isinstance(row, dict)
    }
    lines = ["# Missing Editing / Output Features", ""]
    for group in REQUIRED_GAP_GROUPS:
        lines.extend([f"## {group}", ""])
        for feature_id in _list(groups.get(group)):
            feature = _dict(features_by_id.get(str(feature_id)))
            lines.append(f"- {feature_id}: {feature.get('current_state')} Needed: {feature.get('needed_for_video')}")
        lines.append("")
    return "\n".join(lines)


def _render_review_checklist(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Output Video Layer Proof Review Checklist",
            "",
            "- Open `episode_002_storyboard_preview.html`.",
            "- Confirm the primary artifact is the storyboard/timeline preview.",
            "- Confirm real input, YMM4 import/render, and public gates remain closed.",
            "- Review `output_gap_ledger.json` and `missing_editing_features.md` for concrete output/editing gaps.",
            "- Confirm GUI/i18n artifacts were not modified in this branch.",
            "",
            f"Primary human review: `{state.get('primary_human_review')}`",
            f"Machine readback: `{state.get('primary_machine_readable')}`",
            "",
        ]
    )


def _render_limitations(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Output Video Layer Proof Limitations",
            "",
            "This is a local static proof package. It is not a rendered video, production .ymmp, or public-ready package.",
            "",
            "Not performed:",
            "",
            "- full-suite green campaign",
            "- GUI/i18n lane modification",
            "- production video/render claim",
            "- YouTube upload, publication, scheduling, or visibility change",
            "- OAuth, API keys, payment, or paid services",
            "- rights/legal/public-ready acceptance",
            "- live scraping, RSS fetch, external media download, or external dependencies",
            "- YMM4 GUI launch, import, render, or production `.ymmp` generation",
            "- final thumbnail approval",
            "- cross-repo or destructive git",
            "- real transcript/source replacement",
            "",
            f"Primary review file: `{state.get('primary_human_review')}`",
            "",
        ]
    )


def _render_readme(
    state: dict[str, Any],
    scene_timeline: dict[str, Any],
    gap_ledger: dict[str, Any],
) -> str:
    return "\n".join(
        [
            "# README_OUTPUT_VIDEO_LAYER_PROOF",
            "",
            "Lane-local package for Episode 002 Output / Video Layer proof.",
            "",
            f"- Primary review file: `{state.get('primary_human_review')}`",
            f"- Primary readback: `{state.get('primary_machine_readable')}`",
            f"- Scene count: {scene_timeline.get('scene_count')}",
            f"- Missing feature count: {gap_ledger.get('missing_feature_count')}",
            "- Shared docs touched: false",
            "- GUI/i18n lane files touched: none",
            "",
            "Use this package to see what is still needed to turn the dry-run Episode 002 artifacts into a real yukkuri video.",
            "",
        ]
    )
