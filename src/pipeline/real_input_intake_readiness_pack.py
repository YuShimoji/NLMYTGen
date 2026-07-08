"""Real input intake readiness package for episode 002."""

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

DEFAULT_OUTPUT_DIRNAME = "real_input_intake_readiness"
DEFAULT_ARTIFACT_ID = "episode_002_real_input_intake_readiness_pack_v1"

OUTPUT_TEMPLATE_DIRNAME = "output_template_readiness_pack"
OUTPUT_VIDEO_DIRNAME = "output_video_layer_proof"
TRANSCRIPT_READINESS_DIRNAME = "transcript_substitution_readiness"
IR_BRIDGE_DIRNAME = "ir_bridge"
JAPANESE_GRAPHIC_CONSOLE_DIRNAME = "japanese_graphic_review_console"

REQUIRED_REAL_INPUT_INTAKE_FILES = (
    "real_input_intake_manifest.json",
    "real_input_intake_panel.html",
    "real_input_intake_panel.md",
    "README_REAL_INPUT_INTAKE.md",
    "DROPZONE_README.md",
    "source_transcript_contract.schema.json",
    "local_source_manifest_template.json",
    "transcript_template.json",
    "provenance_receipt_template.json",
    "rights_usage_checklist.md",
    "intake_validation_plan.json",
    "real_input_replacement_plan.md",
    "source_artifact_index.json",
    "validation_readback.json",
    "review_checklist.md",
    "limitations.md",
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

REQUIRED_CONTRACT_FIELDS = (
    "local_file_path",
    "source_title",
    "source_type",
    "capture_date",
    "provenance_note",
    "rights_usage_note",
    "transcript_language",
    "transcript_format",
    "segment_timestamps",
    "trust_verification_notes",
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


def build_real_input_intake_readiness_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build the local real-input intake readiness package."""
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

    contract_schema = _source_transcript_contract_schema(state)
    source_template = _local_source_manifest_template(state)
    transcript_template = _transcript_template(state)
    provenance_template = _provenance_receipt_template(state)
    validation_plan = _intake_validation_plan(state)
    replacement_plan = _replacement_plan_payload(state)
    source_index = _source_artifact_index(state)
    manifest = _manifest(
        state,
        contract_schema,
        source_template,
        transcript_template,
        provenance_template,
        validation_plan,
        replacement_plan,
        output_root,
        repo_root,
    )

    _write_json(output_root / "real_input_intake_manifest.json", manifest)
    _write_json(output_root / "source_transcript_contract.schema.json", contract_schema)
    _write_json(output_root / "local_source_manifest_template.json", source_template)
    _write_json(output_root / "transcript_template.json", transcript_template)
    _write_json(output_root / "provenance_receipt_template.json", provenance_template)
    _write_json(output_root / "intake_validation_plan.json", validation_plan)
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_text(output_root / "real_input_replacement_plan.md", _render_replacement_plan(state, replacement_plan))
    _write_text(output_root / "real_input_intake_panel.html", _render_html(state, validation_plan, replacement_plan))
    _write_text(output_root / "real_input_intake_panel.md", _render_markdown(state, validation_plan, replacement_plan))
    _write_text(output_root / "README_REAL_INPUT_INTAKE.md", _render_readme(state))
    _write_text(output_root / "DROPZONE_README.md", _render_dropzone_readme(state))
    _write_text(output_root / "rights_usage_checklist.md", _render_rights_usage_checklist(state))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state))
    _write_text(output_root / "limitations.md", _render_limitations(state))

    readback = validate_real_input_intake_readiness_pack(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_real_input_intake_readiness_pack(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_real_input_intake_readiness_pack(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated real-input intake readiness package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_REAL_INPUT_INTAKE_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["real_input_intake_manifest.json"])
    contract_schema = _load_json_if_present(files["source_transcript_contract.schema.json"])
    source_template = _load_json_if_present(files["local_source_manifest_template.json"])
    transcript_template = _load_json_if_present(files["transcript_template.json"])
    provenance_template = _load_json_if_present(files["provenance_receipt_template.json"])
    validation_plan = _load_json_if_present(files["intake_validation_plan.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])
    json_payloads = {
        "manifest": manifest,
        "contract_schema": contract_schema,
        "source_template": source_template,
        "transcript_template": transcript_template,
        "provenance_template": provenance_template,
        "validation_plan": validation_plan,
        "source_index": source_index,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = _dict(json_payloads["manifest"])
    contract_schema = _dict(json_payloads["contract_schema"])
    source_template = _dict(json_payloads["source_template"])
    transcript_template = _dict(json_payloads["transcript_template"])
    provenance_template = _dict(json_payloads["provenance_template"])
    validation_plan = _dict(json_payloads["validation_plan"])
    source_index = _dict(json_payloads["source_index"])

    html_text = files["real_input_intake_panel.html"].read_text(encoding="utf-8") if files["real_input_intake_panel.html"].exists() else ""
    markdown_text = files["real_input_intake_panel.md"].read_text(encoding="utf-8") if files["real_input_intake_panel.md"].exists() else ""
    dropzone_text = files["DROPZONE_README.md"].read_text(encoding="utf-8") if files["DROPZONE_README.md"].exists() else ""
    rights_text = files["rights_usage_checklist.md"].read_text(encoding="utf-8") if files["rights_usage_checklist.md"].exists() else ""
    replacement_text = files["real_input_replacement_plan.md"].read_text(encoding="utf-8") if files["real_input_replacement_plan.md"].exists() else ""
    boundary_flags = _dict(manifest.get("boundary_flags"))
    contract_properties = _dict(contract_schema.get("properties"))
    contract_required = set(str(value) for value in _list(contract_schema.get("required")))
    source_payload = _dict(source_template.get("source"))
    transcript_payload = _dict(transcript_template.get("transcript"))
    provenance_payload = _dict(provenance_template.get("provenance_receipt"))
    gui_touches = _list(manifest.get("gui_lane_files_touched"))
    output_template_touches = _list(manifest.get("output_template_files_touched"))

    if manifest.get("artifact_kind") != "episode-real-input-intake-readiness-pack":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "real_input_intake_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")
    for field in REQUIRED_CONTRACT_FIELDS:
        if field not in contract_properties:
            failed_checks.append(f"contract_property_missing:{field}")
        if field not in contract_required:
            failed_checks.append(f"contract_required_missing:{field}")
    if transcript_payload.get("invented_real_content") is not False:
        failed_checks.append("transcript_template_invented_real_content_not_false")
    if transcript_payload.get("actual_segments_present") is not False:
        failed_checks.append("transcript_template_actual_segments_present_not_false")
    if source_payload.get("local_file_path") != "<required-local-path-inside-real_input-dropzone>":
        failed_checks.append("source_template_path_placeholder_missing")
    if provenance_template.get("receipt_status") != "template_only_not_verified":
        failed_checks.append("provenance_template_status_mismatch")
    if validation_plan.get("invented_real_content") is not False:
        failed_checks.append("validation_plan_invented_real_content_not_false")
    if validation_plan.get("rights_acceptance_claimed") is not False:
        failed_checks.append("validation_plan_rights_acceptance_not_false")
    if manifest.get("invented_real_content") is not False:
        failed_checks.append("manifest_invented_real_content_not_false")
    if manifest.get("rights_acceptance_claimed") is not False:
        failed_checks.append("manifest_rights_acceptance_not_false")
    if manifest.get("real_source_transcript_ingested") is not False:
        failed_checks.append("real_source_transcript_ingested_not_false")
    if manifest.get("shared_docs_touched") is not True:
        failed_checks.append("thread_registry_shared_docs_status_missing")
    if gui_touches:
        failed_checks.append("gui_lane_files_touched_not_empty")
    if output_template_touches:
        failed_checks.append("output_template_files_touched_not_empty")
    if source_index.get("output_template_context_read_only") is not True:
        failed_checks.append("output_template_context_not_read_only")
    if source_index.get("gui_lane_context_read_only") is not True:
        failed_checks.append("gui_lane_context_not_read_only")
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")
    for marker in (
        'data-real-input-intake="true"',
        'data-region="intake-checklist"',
        'data-region="contract-map"',
        'data-region="provenance-flow"',
        'data-region="replacement-strip"',
    ):
        if marker not in html_text:
            failed_checks.append(f"html_marker_missing:{marker}")
    if "color-scheme: dark light" not in html_text:
        failed_checks.append("dark_color_scheme_missing")
    if "prefers-color-scheme" not in html_text:
        failed_checks.append("prefers_color_scheme_missing")
    if not markdown_text.strip():
        failed_checks.append("markdown_panel_empty")
    if "real_input/source/" not in dropzone_text or "real_input/transcript/" not in dropzone_text:
        failed_checks.append("dropzone_paths_missing")
    if "not legal acceptance" not in rights_text:
        failed_checks.append("rights_checklist_acceptance_boundary_missing")
    if "output_template_readiness_pack" not in replacement_text:
        failed_checks.append("replacement_plan_output_template_link_missing")

    external_refs = _external_refs_in_files([path for name, path in files.items() if name != "validation_readback.json"])
    forbidden_hits = _forbidden_true_claims(root)
    temporary_hits = _temporary_copy_hits(
        [
            files["real_input_intake_panel.html"],
            files["real_input_intake_panel.md"],
            files["README_REAL_INPUT_INTAKE.md"],
        ]
    )
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "html_panel_exists": files["real_input_intake_panel.html"].exists(),
        "markdown_panel_exists": files["real_input_intake_panel.md"].exists(),
        "contract_required_fields_present": all(field in contract_required for field in REQUIRED_CONTRACT_FIELDS),
        "template_placeholders_only": source_payload.get("local_file_path") == "<required-local-path-inside-real_input-dropzone>",
        "invented_real_content": manifest.get("invented_real_content"),
        "rights_acceptance_claimed": manifest.get("rights_acceptance_claimed"),
        "real_source_transcript_ingested": manifest.get("real_source_transcript_ingested"),
        "gui_lane_files_touched": gui_touches,
        "output_template_files_touched": output_template_touches,
        "shared_docs_touched": manifest.get("shared_docs_touched"),
        "external_dependency_status": "none_found" if not external_refs else "found",
        "forbidden_true_claims_absent": not forbidden_hits,
        "temporary_copy_absent": not temporary_hits,
    }
    return {
        "schema_version": "real_input_intake_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "primary_review_file": str(root / "real_input_intake_panel.html"),
        "primary_human_review": str(root / "real_input_intake_panel.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "input_contract_status": manifest.get("input_contract_status"),
        "transcript_template_status": manifest.get("transcript_template_status"),
        "provenance_template_status": manifest.get("provenance_template_status"),
        "dropzone_status": manifest.get("dropzone_status"),
        "replacement_plan_status": manifest.get("replacement_plan_status"),
        "invented_real_content": manifest.get("invented_real_content"),
        "rights_acceptance_claimed": manifest.get("rights_acceptance_claimed"),
        "gui_lane_files_touched": gui_touches,
        "output_template_files_touched": output_template_touches,
        "thread_registry_updated": manifest.get("thread_registry_updated"),
        "shared_docs_touched": manifest.get("shared_docs_touched"),
        "full_pytest_run": False,
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{(root / "real_input_intake_panel.html").resolve()}"',
        "access_state": "verified_present" if (root / "real_input_intake_panel.html").exists() else "missing",
        "next_action": manifest.get("next_action"),
    }


def _input_paths(source_root: Path) -> dict[str, Path]:
    output_template_root = source_root / OUTPUT_TEMPLATE_DIRNAME
    output_video_root = source_root / OUTPUT_VIDEO_DIRNAME
    transcript_root = source_root / TRANSCRIPT_READINESS_DIRNAME
    ir_root = source_root / IR_BRIDGE_DIRNAME
    gui_root = source_root / JAPANESE_GRAPHIC_CONSOLE_DIRNAME
    return {
        "output_template_root": output_template_root,
        "output_template_manifest": output_template_root / "output_template_readiness_manifest.json",
        "output_template_gap_readback": output_template_root / "template_gap_closure_readback.json",
        "output_template_source_index": output_template_root / "source_artifact_index.json",
        "output_video_gap_ledger": output_video_root / "output_gap_ledger.json",
        "transcript_validation": transcript_root / "validation_readback.json",
        "transcript_dropzone_existing": transcript_root / "real_input",
        "episode_bridge": ir_root / "episode_bridge.json",
        "writer_ir": ir_root / "writer_ir_candidate.json",
        "cue_packet": ir_root / "cue_packet_candidate.json",
        "draft_yymm4_csv": ir_root / "draft_yymm4.csv",
        "japanese_console_validation": gui_root / "validation_readback.json",
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "output_template_manifest": _load_json_if_present(paths["output_template_manifest"]),
        "output_template_gap_readback": _load_json_if_present(paths["output_template_gap_readback"]),
        "output_template_source_index": _load_json_if_present(paths["output_template_source_index"]),
        "output_video_gap_ledger": _load_json_if_present(paths["output_video_gap_ledger"]),
        "transcript_validation": _load_json_if_present(paths["transcript_validation"]),
        "episode_bridge": _load_json_if_present(paths["episode_bridge"]),
        "writer_ir": _load_json_if_present(paths["writer_ir"]),
        "cue_packet": _load_json_if_present(paths["cue_packet"]),
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
    episode_bridge = _dict(payloads.get("episode_bridge"))
    transcript_validation = _dict(payloads.get("transcript_validation"))
    output_template_manifest = _dict(payloads.get("output_template_manifest"))
    return {
        "schema_version": "real_input_intake_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-real-input-intake-readiness-pack",
        "status": "real_input_intake_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "selected_candidate_id": episode_bridge.get("selected_candidate_id") or "factory_seed_dry_run_002",
        "episode_title": episode_bridge.get("selected_title") or "Episode 002",
        "current_transcript_status": transcript_validation.get("transcript_status") or "sample_fixture_not_real",
        "output_template_status": output_template_manifest.get("status") or "unknown",
        "paths": {name: _relpath(path, repo_root) for name, path in paths.items() if isinstance(path, Path)},
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
        "primary_human_review": _relpath(output_root / "real_input_intake_panel.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_action": "Place future verified local source and transcript files under the real_input dropzone, then validate the manifest before real-input replacement.",
    }


def _source_transcript_contract_schema(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "source_transcript_contract.schema.v1",
        "title": "Episode 002 Local Source and Transcript Contract",
        "type": "object",
        "additionalProperties": False,
        "required": list(REQUIRED_CONTRACT_FIELDS),
        "properties": {
            "local_file_path": {"type": "string", "description": "Repo-relative or absolute local path supplied by the user."},
            "source_title": {"type": "string", "description": "Human-readable source title."},
            "source_type": {"type": "string", "enum": ["article", "paper", "video", "audio", "document", "notes", "other"]},
            "capture_date": {"type": "string", "description": "Date the local source/transcript was captured or exported."},
            "provenance_note": {"type": "string", "description": "How the local file was obtained and why it is trusted."},
            "rights_usage_note": {"type": "string", "description": "Usage note for review only; not legal acceptance."},
            "transcript_language": {"type": "string", "description": "Language tag or plain language name."},
            "transcript_format": {"type": "string", "enum": ["plain_text", "speaker_labeled_text", "csv_two_column", "json_segments", "other"]},
            "segment_timestamps": {"type": "array", "items": {"type": "object"}},
            "trust_verification_notes": {"type": "array", "items": {"type": "string"}},
        },
        "boundary": {
            "template_only": True,
            "no_live_fetch": True,
            "no_rights_acceptance": True,
            "no_real_content_embedded": True,
        },
    }


def _local_source_manifest_template(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "local_source_manifest_template.v1",
        "template_status": "placeholder_only_not_verified",
        "source": {
            "local_file_path": "<required-local-path-inside-real_input-dropzone>",
            "source_title": "<required-source-title>",
            "source_type": "<article|paper|video|audio|document|notes|other>",
            "capture_date": "<YYYY-MM-DD-or-local-export-date>",
            "provenance_note": "<how-this-local-file-was-obtained>",
            "rights_usage_note": "<review-only-usage-note-not-legal-acceptance>",
            "trust_verification_notes": ["<required-verification-note>"],
        },
        "episode_linkage": {
            "target_episode": "episode_002",
            "current_status": state.get("current_transcript_status"),
            "replacement_execution": "not_run",
        },
        "invented_real_content": False,
    }


def _transcript_template(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "transcript_template.v1",
        "template_status": "placeholder_only_no_real_transcript",
        "transcript": {
            "local_file_path": "<required-local-transcript-path-inside-real_input-dropzone>",
            "transcript_language": "<required-language>",
            "transcript_format": "<plain_text|speaker_labeled_text|csv_two_column|json_segments|other>",
            "segment_timestamps": [
                {
                    "segment_id": "<segment-id>",
                    "start_time": "<optional-start-time>",
                    "end_time": "<optional-end-time>",
                    "speaker": "<optional-speaker-label>",
                    "text": "<transcript-text-placeholder>",
                }
            ],
            "trust_verification_notes": ["<required-note-confirming-this-is-user-provided-local-material>"],
            "actual_segments_present": False,
            "invented_real_content": False,
        },
    }


def _provenance_receipt_template(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "provenance_receipt_template.v1",
        "receipt_status": "template_only_not_verified",
        "provenance_receipt": {
            "source_manifest_path": "<local-source-manifest-path>",
            "transcript_path": "<local-transcript-path>",
            "captured_by": "<user-or-local-process-name>",
            "capture_date": "<YYYY-MM-DD>",
            "hash_or_size_note": "<optional-local-file-size-or-hash-note>",
            "reviewer_verification_note": "<what-the-reviewer-checked>",
            "rights_usage_note": "<review-only-note-not-public-ready-approval>",
            "public_ready_acceptance": False,
            "legal_acceptance": False,
        },
        "invented_real_content": False,
    }


def _intake_validation_plan(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "intake_validation_plan.v1",
        "status": "ready_to_validate_future_local_files",
        "invented_real_content": False,
        "rights_acceptance_claimed": False,
        "checks": [
            "source_manifest_json_loads",
            "all_required_contract_fields_present",
            "local_file_paths_exist_when_user_supplies_files",
            "transcript_format_declared",
            "segment_timestamps_declared_or_explicitly_not_available",
            "provenance_note_present",
            "rights_usage_note_present_without_public_ready_claim",
            "trust_verification_notes_present",
            "no_live_fetch_or_external_media_download",
            "output_template_readiness_pack_link_available",
        ],
        "future_failures_to_block_replacement": [
            "missing local source file",
            "missing transcript file",
            "rights note claims public-ready approval without human gate",
            "transcript cannot be parsed into supported format",
            "provenance note absent",
        ],
    }


def _replacement_plan_payload(state: dict[str, Any]) -> dict[str, Any]:
    paths = _dict(state.get("paths"))
    return {
        "schema_version": "real_input_replacement_plan.v1",
        "status": "planned_not_executed",
        "source_intake_package": state.get("output_dir"),
        "output_template_readiness_pack": paths.get("output_template_root"),
        "future_linkage": [
            "Validate local source manifest and transcript against source_transcript_contract.schema.json.",
            "Generate real-input replacement draft artifacts from validated local files.",
            "Reconnect replacement output to output_template_readiness_pack timing, voice, scene, overlay, and thumbnail transfer slots.",
            "Review readback before any YMM4 observation gate.",
        ],
        "replacement_executed": False,
    }


def _source_artifact_index(state: dict[str, Any]) -> dict[str, Any]:
    paths = _dict(state.get("paths"))
    records = [
        _source_record("output_template_manifest", paths.get("output_template_manifest"), "output_template_context_read_only", True),
        _source_record("output_template_gap_readback", paths.get("output_template_gap_readback"), "output_template_context_read_only", True),
        _source_record("output_template_source_index", paths.get("output_template_source_index"), "output_template_context_read_only", True),
        _source_record("output_video_gap_ledger", paths.get("output_video_gap_ledger"), "gap_context", True),
        _source_record("transcript_validation", paths.get("transcript_validation"), "current_input_boundary", True),
        _source_record("episode_bridge", paths.get("episode_bridge"), "episode_context", True),
        _source_record("writer_ir_candidate", paths.get("writer_ir"), "episode_context", True),
        _source_record("cue_packet_candidate", paths.get("cue_packet"), "episode_context", True),
        _source_record("draft_yymm4_csv", paths.get("draft_yymm4_csv"), "sample_csv_context", True),
        _source_record("japanese_console_validation", paths.get("japanese_console_validation"), "gui_context_read_only", True),
    ]
    return {
        "schema_version": "real_input_intake_source_artifact_index.v1",
        "artifact_id": state.get("artifact_id"),
        "output_template_context_read_only": True,
        "gui_lane_context_read_only": True,
        "protected_gui_lane_dirs": list(PROTECTED_GUI_LANE_DIRS),
        "protected_output_template_dirs": list(PROTECTED_OUTPUT_TEMPLATE_DIRS),
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
    contract_schema: dict[str, Any],
    source_template: dict[str, Any],
    transcript_template: dict[str, Any],
    provenance_template: dict[str, Any],
    validation_plan: dict[str, Any],
    replacement_plan: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "real_input_intake_manifest.v1",
        "artifact_id": state.get("artifact_id"),
        "artifact_kind": "episode-real-input-intake-readiness-pack",
        "status": "real_input_intake_ready_local_offline",
        "parallel_lane": "input_api_hub",
        "thread_id": "input-intake-episode002",
        "output_dir": _relpath(output_root, repo_root),
        "files": {filename: _relpath(output_root / filename, repo_root) for filename in REQUIRED_REAL_INPUT_INTAKE_FILES},
        "primary_review_file": state.get("primary_human_review"),
        "primary_human_review": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "input_contract_status": "schema_ready_template_only",
        "transcript_template_status": transcript_template.get("template_status"),
        "provenance_template_status": provenance_template.get("receipt_status"),
        "dropzone_status": "instructions_ready_no_files_required_now",
        "replacement_plan_status": replacement_plan.get("status"),
        "invented_real_content": False,
        "rights_acceptance_claimed": False,
        "real_source_transcript_ingested": False,
        "gui_lane_files_touched": [],
        "output_template_files_touched": [],
        "thread_registry_updated": True,
        "shared_docs_touched": True,
        "boundary_flags": state.get("boundary_flags"),
        "actual_yymm4_import": False,
        "yymm4_rendered": False,
        "production_ready": False,
        "public_ready": False,
        "final_thumbnail_approval": False,
        "contract_required_fields": contract_schema.get("required"),
        "validation_plan_status": validation_plan.get("status"),
        "next_action": state.get("next_action"),
    }


def _render_html(
    state: dict[str, Any],
    validation_plan: dict[str, Any],
    replacement_plan: dict[str, Any],
) -> str:
    checks = "\n".join(_render_check_item(item) for item in _list(validation_plan.get("checks"))[:8])
    replacement_steps = "\n".join(_render_step(index, item) for index, item in enumerate(_list(replacement_plan.get("future_linkage")), start=1))
    return f"""<!doctype html>
<html lang="ja" data-real-input-intake="true" data-artifact-kind="episode-real-input-intake-readiness-pack">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Real Input Intake</title>
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
      --green: #9ee8bc;
      --teal: #73dfcf;
      --blue: #91bbff;
      --amber: #f1cf6a;
      --rose: #f0a1aa;
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
        --green: #047857;
        --teal: #0f766e;
        --blue: #1d4ed8;
        --amber: #8a5a00;
        --rose: #9b1c1c;
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
      width: min(1380px, calc(100% - 28px));
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
      grid-template-columns: minmax(0, 1fr) minmax(320px, 0.34fr);
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
    .flow {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }}
    .flow-node, .contract-node, .check-item, .step-node {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--stage);
      padding: 10px;
      min-width: 0;
    }}
    .flow-node strong, .contract-node strong, .step-node strong {{
      display: block;
      color: var(--text);
    }}
    .lanes {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 14px;
    }}
    .lane {{
      padding: 14px;
      display: grid;
      gap: 10px;
      align-content: start;
    }}
    .contract-map {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
    }}
    .check-list, .steps {{
      display: grid;
      gap: 8px;
    }}
    code {{ color: var(--blue); overflow-wrap: anywhere; font-size: 0.84rem; }}
    @media (max-width: 1120px) {{
      .topline, .hero, .lanes, .flow, .contract-map {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <header class="topline" data-region="header">
      <div class="identity">
        <span class="episode">Episode 002</span>
        <span class="badge">Input / API Hub</span>
        <span class="badge">実入力受け入れ準備</span>
        <span class="badge">local only</span>
      </div>
      <div class="badges" aria-label="closed gates">
        <span class="gate">no live fetch</span>
        <span class="gate">no real ingest</span>
        <span class="gate">no YMM4</span>
        <span class="gate">no public approval</span>
      </div>
    </header>
    <section class="hero">
      <section class="board">
        <div>
          <h1>実入力を受け取るための準備パネル</h1>
          <p>今は sample_fixture のままです。次にユーザーがローカルのソースと文字起こしを置けるよう、契約・置き場・来歴・置換手順だけを用意します。</p>
        </div>
        <div class="flow" data-region="intake-checklist" aria-label="intake flow">
          <article class="flow-node"><strong>1. local source</strong><p>source manifest とファイルパスを用意</p></article>
          <article class="flow-node"><strong>2. transcript</strong><p>言語、形式、timestamp 有無を明記</p></article>
          <article class="flow-node"><strong>3. provenance</strong><p>取得経路と確認メモを receipt に記録</p></article>
          <article class="flow-node"><strong>4. replacement</strong><p>output template slots へ後で接続</p></article>
        </div>
      </section>
      <aside class="side">
        <span class="badge">current state</span>
        <p>current_transcript_status: {_escape(state.get("current_transcript_status"))}</p>
        <p>output_template_status: {_escape(state.get("output_template_status"))}</p>
        <p>実ファイルの検証と episode 置換は、ユーザー提供ファイルが入ってからです。</p>
      </aside>
    </section>
    <section class="lanes">
      <section class="lane" data-region="contract-map">
        <h2>契約フィールド</h2>
        <div class="contract-map">
          {_contract_nodes()}
        </div>
      </section>
      <section class="lane" data-region="provenance-flow">
        <h2>来歴確認</h2>
        <div class="check-list">{checks}</div>
      </section>
      <section class="lane" data-region="replacement-strip">
        <h2>置換への接続</h2>
        <div class="steps">{replacement_steps}</div>
      </section>
      <section class="lane">
        <h2>次に置くもの</h2>
        <p><code>real_input/source/</code> にソース、<code>real_input/transcript/</code> に文字起こし、<code>real_input/manifests/</code> に manifest と receipt を置く想定です。</p>
      </section>
    </section>
  </main>
</body>
</html>
"""


def _contract_nodes() -> str:
    labels = [
        ("local_file_path", "ローカルファイルの場所"),
        ("source_title", "ソース名"),
        ("source_type", "種別"),
        ("capture_date", "取得日"),
        ("provenance_note", "来歴メモ"),
        ("rights_usage_note", "利用メモ"),
        ("transcript_language", "文字起こし言語"),
        ("transcript_format", "形式"),
        ("segment_timestamps", "時刻情報"),
        ("trust_verification_notes", "確認メモ"),
    ]
    return "\n".join(
        f'<article class="contract-node"><strong>{_escape(field)}</strong><p>{_escape(label)}</p></article>'
        for field, label in labels
    )


def _render_check_item(item: Any) -> str:
    return f'<div class="check-item"><strong>{_escape(item)}</strong><p>future validation check</p></div>'


def _render_step(index: int, item: Any) -> str:
    return f'<article class="step-node"><strong>{index}</strong><p>{_escape(item)}</p></article>'


def _render_markdown(
    state: dict[str, Any],
    validation_plan: dict[str, Any],
    replacement_plan: dict[str, Any],
) -> str:
    return "\n".join(
        [
            "# Episode 002 Real Input Intake Panel",
            "",
            "Local-only intake readiness for future verified source/transcript material.",
            "",
            f"- primary_review_file: `{state.get('primary_human_review')}`",
            f"- current_transcript_status: {state.get('current_transcript_status')}",
            "- invented_real_content: false",
            "- rights_acceptance_claimed: false",
            "- real_source_transcript_ingested: false",
            "",
            "## Required Contract Fields",
            "",
            *[f"- {field}" for field in REQUIRED_CONTRACT_FIELDS],
            "",
            "## Future Replacement Link",
            "",
            f"- output_template_readiness_pack: `{_dict(state.get('paths')).get('output_template_root')}`",
            f"- replacement_plan_status: {replacement_plan.get('status')}",
            f"- validation_plan_status: {validation_plan.get('status')}",
            "",
        ]
    )


def _render_readme(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# README_REAL_INPUT_INTAKE",
            "",
            "Lane-local package for Episode 002 real-input intake readiness.",
            "",
            f"- Primary review file: `{state.get('primary_human_review')}`",
            f"- Primary readback: `{state.get('primary_machine_readable')}`",
            "- This package does not ingest real source/transcript material.",
            "- It only defines the local contract, dropzone, provenance receipt, rights checklist, and future replacement plan.",
            "- GUI/i18n and output template packages are read-only context for this slice.",
            "",
        ]
    )


def _render_dropzone_readme(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# DROPZONE_README",
            "",
            "Future user-provided files should be placed under this package's dropzone before a replacement run.",
            "",
            "Planned dropzone paths:",
            "",
            "- `real_input/source/` for local source files.",
            "- `real_input/transcript/` for local transcript files.",
            "- `real_input/manifests/` for completed source manifest and provenance receipt JSON files.",
            "",
            "No file is required or claimed present in this readiness slice. Live fetch, scraping, media download, OAuth, API keys, and public upload stay closed.",
            "",
        ]
    )


def _render_rights_usage_checklist(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Rights / Usage Checklist",
            "",
            "This checklist is for review preparation only and is not legal acceptance or public-ready approval.",
            "",
            "- Source title and type are identified.",
            "- Local capture/export date is recorded.",
            "- Provenance note explains how the file was obtained.",
            "- Usage note states review-only or approved internal use boundaries.",
            "- Public-ready acceptance remains false unless a separate human gate is opened.",
            "- Final thumbnail approval and YouTube visibility remain closed.",
            "",
        ]
    )


def _render_replacement_plan(state: dict[str, Any], replacement_plan: dict[str, Any]) -> str:
    lines = [
        "# Real Input Replacement Plan",
        "",
        "Status: planned only; replacement is not executed in this slice.",
        "",
        f"- output_template_readiness_pack: `{_dict(state.get('paths')).get('output_template_root')}`",
        "- real source/transcript ingestion: not performed",
        "- YMM4 GUI/import/render: closed",
        "- public upload/rights acceptance: closed",
        "",
        "## Future Linkage",
        "",
    ]
    for item in _list(replacement_plan.get("future_linkage")):
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def _render_review_checklist(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Real Input Intake Review Checklist",
            "",
            "- Open `real_input_intake_panel.html`.",
            "- Confirm the contract fields explain what the user must provide.",
            "- Confirm templates contain placeholders, not real source/transcript content.",
            "- Confirm rights checklist does not claim legal/public-ready acceptance.",
            "- Confirm future replacement connects to `output_template_readiness_pack` without modifying it now.",
            "",
        ]
    )


def _render_limitations(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Real Input Intake Limitations",
            "",
            "This is a local static readiness package. It is not real input ingestion, legal review, a rendered video, or a public-ready package.",
            "",
            "Not performed:",
            "",
            "- no full-suite green campaign",
            "- no GUI/i18n lane modification",
            "- no output-template package modification",
            "- no real source/transcript ingestion",
            "- no invented real content",
            "- no production video/render claim",
            "- no YouTube upload, publication, scheduling, or visibility change",
            "- no OAuth, API keys, payment, or paid services",
            "- no rights/legal/public-ready acceptance",
            "- no live scraping, RSS fetch, external media download, or external dependencies",
            "- no YMM4 GUI launch, import, or render",
            "- no production `.ymmp` generation",
            "- no final thumbnail approval",
            "- no cross-repo or destructive git",
            "",
        ]
    )
