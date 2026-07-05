"""Reusable local/offline episode factory template registry.

This registry distills the current yukkuri newsroom pilot into reusable
machine-readable templates and a deterministic seed sample. It does not fetch
live sources, rerun a real transcript, launch YMM4, render, publish, or claim
rights/public readiness.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.pipeline.content_planning_spine import BLOCKED_PUBLIC_ACTIONS
from src.pipeline.dashboard_readiness_ingest import STATUS_CATEGORIES

DEFAULT_OUTPUT_DIRNAME = "episode_factory_template_registry"
DEFAULT_ARTIFACT_ID = "episode_factory_template_registry_001"

REQUIRED_EPISODE_FACTORY_TEMPLATE_REGISTRY_FILES = (
    "template_registry_manifest.json",
    "episode_factory_templates.json",
    "yukkuri_newsroom_template.json",
    "content_spine_template.json",
    "transcript_input_template.json",
    "writer_ir_template.json",
    "yymm4_import_template.json",
    "thumbnail_proof_template.json",
    "dashboard_status_template.json",
    "next_episode_seed_sample.json",
    "init_readiness_summary.json",
    "source_artifact_index.json",
    "template_usage.md",
    "review_checklist.md",
    "limitations.md",
    "validation_readback.json",
)

REQUIRED_TEMPLATE_IDS = (
    "yukkuri_newsroom_template",
    "content_spine_template",
    "transcript_input_template",
    "writer_ir_template",
    "yymm4_import_template",
    "thumbnail_proof_template",
    "dashboard_status_template",
)

JSON_REGISTRY_FILES = tuple(
    name
    for name in REQUIRED_EPISODE_FACTORY_TEMPLATE_REGISTRY_FILES
    if name.endswith(".json") and name != "validation_readback.json"
)

EXTERNAL_REFERENCE_PATTERNS = (
    re.compile(r"\b(src|href)\s*=\s*['\"]https?://", re.IGNORECASE),
    re.compile(r"url\(\s*['\"]?https?://", re.IGNORECASE),
    re.compile(r"<image\b", re.IGNORECASE),
    re.compile(r"<img\b", re.IGNORECASE),
)

FORBIDDEN_COMPLETION_CLAIMS = (
    '"production_ready": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"youtube_uploaded": true',
    '"external_media_download_required": true',
    '"media_download_required": true',
    '"oauth_required": true',
    '"payment_required": true',
    '"yymm4_gui_launched": true',
    '"yymm4_import_completed": true',
    '"yymm4_render_completed": true',
)

CLOSED_GATES = (
    "YouTube upload/publication/visibility change",
    "OAuth/API keys/payment",
    "rights/legal/public-ready acceptance",
    "live scraping/media download",
    "external image/media download or embedded copyrighted media",
    "YMM4 GUI launch/import/render",
    "production .ymmp generation",
    "cross-repo or destructive git",
)

BOUNDARY_STATUS = {
    "source_status": "offline_fixture_not_live",
    "template_status": "draft_offline",
    "transcript_status": "sample_fixture_not_real",
    "real_transcript_status": "blocked_by_real_input",
    "rights_boundary": "sample_only_no_publication",
    "rights_gate": "blocked_by_true_gate",
    "public_upload_status": "public_upload_closed",
    "public_upload_gate": "blocked_by_true_gate",
    "external_media_status": "blocked_by_true_gate",
    "yymm4_gui_status": "blocked_by_true_gate",
    "yymm4_import_status": "deferred",
    "yymm4_render_status": "yymm4_render_closed",
    "yymm4_render_gate": "blocked_by_true_gate",
    "production_status": "blocked_by_true_gate",
}


def build_episode_factory_template_registry(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build the reusable template registry and next episode seed sample."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)

    repo_root = _find_repo_root(source_root)
    snapshot = _load_snapshot(source_root)
    selected_candidate = _selected_candidate(snapshot)

    yukkuri_template = _yukkuri_newsroom_template(selected_candidate)
    content_template = _content_spine_template(snapshot, selected_candidate)
    transcript_template = _transcript_input_template(snapshot)
    writer_template = _writer_ir_template(snapshot, selected_candidate)
    yymm4_template = _yymm4_import_template(snapshot)
    thumbnail_template = _thumbnail_proof_template(snapshot, selected_candidate)
    dashboard_template = _dashboard_status_template(snapshot)

    template_payloads = {
        "yukkuri_newsroom_template": yukkuri_template,
        "content_spine_template": content_template,
        "transcript_input_template": transcript_template,
        "writer_ir_template": writer_template,
        "yymm4_import_template": yymm4_template,
        "thumbnail_proof_template": thumbnail_template,
        "dashboard_status_template": dashboard_template,
    }
    template_index = _episode_factory_templates(template_payloads, selected_candidate)
    seed_sample = _next_episode_seed_sample(
        artifact_id=artifact_id,
        output_root=output_root,
        selected_candidate=selected_candidate,
        template_index=template_index,
    )
    readiness_summary = _init_readiness_summary(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        snapshot=snapshot,
        selected_candidate=selected_candidate,
        template_index=template_index,
        seed_sample=seed_sample,
    )
    manifest = _manifest_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        selected_candidate=selected_candidate,
        template_index=template_index,
        readiness_summary=readiness_summary,
        snapshot=snapshot,
    )
    source_index = _source_artifact_index(snapshot, output_root, repo_root)

    _write_json(output_root / "template_registry_manifest.json", manifest)
    _write_json(output_root / "episode_factory_templates.json", template_index)
    _write_json(output_root / "yukkuri_newsroom_template.json", yukkuri_template)
    _write_json(output_root / "content_spine_template.json", content_template)
    _write_json(output_root / "transcript_input_template.json", transcript_template)
    _write_json(output_root / "writer_ir_template.json", writer_template)
    _write_json(output_root / "yymm4_import_template.json", yymm4_template)
    _write_json(output_root / "thumbnail_proof_template.json", thumbnail_template)
    _write_json(output_root / "dashboard_status_template.json", dashboard_template)
    _write_json(output_root / "next_episode_seed_sample.json", seed_sample)
    _write_json(output_root / "init_readiness_summary.json", readiness_summary)
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_text(output_root / "template_usage.md", _render_template_usage(readiness_summary))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(readiness_summary))
    _write_text(output_root / "limitations.md", _render_limitations(readiness_summary))

    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(snapshot, output_root, repo_root))
    readback = validate_episode_factory_template_registry(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(snapshot, output_root, repo_root))
    final_readback = validate_episode_factory_template_registry(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(snapshot, output_root, repo_root))
    return final_readback


def validate_episode_factory_template_registry(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate registry files, template keys, seed sample, and closed gates."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_EPISODE_FACTORY_TEMPLATE_REGISTRY_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    json_payloads = {
        name.removesuffix(".json"): _load_json_if_present(files[name])
        for name in JSON_REGISTRY_FILES
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["template_registry_manifest"]
    template_index = json_payloads["episode_factory_templates"]
    seed_sample = json_payloads["next_episode_seed_sample"]
    readiness_summary = json_payloads["init_readiness_summary"]
    source_index = json_payloads["source_artifact_index"]

    if manifest.get("artifact_kind") != "episode-factory-template-registry":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("boundary_status", {}).get("transcript_status") != "sample_fixture_not_real":
        failed_checks.append("sample_fixture_status_not_preserved")
    if manifest.get("boundary_status", {}).get("template_status") != "draft_offline":
        failed_checks.append("draft_offline_status_not_preserved")
    if manifest.get("boundary_status", {}).get("rights_boundary") != "sample_only_no_publication":
        failed_checks.append("rights_boundary_not_preserved")
    if manifest.get("boundary_status", {}).get("public_upload_status") != "public_upload_closed":
        failed_checks.append("public_upload_closed_not_preserved")
    if manifest.get("boundary_status", {}).get("yymm4_render_status") != "yymm4_render_closed":
        failed_checks.append("yymm4_render_closed_not_preserved")

    template_ids = {
        item.get("template_id")
        for item in template_index.get("templates", [])
        if isinstance(item, dict)
    }
    missing_templates = [template_id for template_id in REQUIRED_TEMPLATE_IDS if template_id not in template_ids]
    failed_checks.extend(f"missing_template:{template_id}" for template_id in missing_templates)

    for template_id, payload in json_payloads.items():
        if not template_id.endswith("_template"):
            continue
        if not payload.get("required_fields_for_real_episode"):
            failed_checks.append(f"template_missing_required_fields:{template_id}")
        if not payload.get("carried_from_template"):
            failed_checks.append(f"template_missing_carried_fields:{template_id}")

    required_inputs = seed_sample.get("required_inputs", {})
    if seed_sample.get("status") != "draft_offline_seed_sample":
        failed_checks.append("seed_sample_status_unexpected")
    if not seed_sample.get("episode_id"):
        failed_checks.append("seed_episode_id_missing")
    for key in ("topic_or_source_packet", "real_transcript", "rights_review", "human_episode_decision"):
        if key not in required_inputs:
            failed_checks.append(f"seed_required_input_missing:{key}")
    if seed_sample.get("boundary_status", {}).get("public_upload_status") != "public_upload_closed":
        failed_checks.append("seed_public_upload_closed_not_preserved")
    if readiness_summary.get("deterministic_generation_path") is not True:
        failed_checks.append("deterministic_generation_path_missing")
    if source_index.get("artifact_counts", {}).get("source_present", 0) < 8:
        failed_checks.append("source_artifact_index_too_sparse")

    combined_text = _combined_text(files.values())
    external_reference_hits = _external_reference_hits(combined_text)
    failed_checks.extend(f"external_reference:{hit}" for hit in external_reference_hits)
    forbidden_hits = [claim for claim in FORBIDDEN_COMPLETION_CLAIMS if claim in combined_text]
    failed_checks.extend(f"forbidden_completion_claim:{claim}" for claim in forbidden_hits)

    return {
        "schema_version": "episode_factory_template_registry_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
            "required_templates_present": not missing_templates,
            "seed_sample_present": bool(seed_sample.get("episode_id")),
            "required_seed_inputs_present": all(
                key in required_inputs
                for key in ("topic_or_source_packet", "real_transcript", "rights_review", "human_episode_decision")
            ),
            "sample_fixture_preserved": manifest.get("boundary_status", {}).get("transcript_status")
            == "sample_fixture_not_real",
            "draft_offline_preserved": manifest.get("boundary_status", {}).get("template_status")
            == "draft_offline",
            "rights_boundary_preserved": manifest.get("boundary_status", {}).get("rights_boundary")
            == "sample_only_no_publication",
            "public_upload_closed": manifest.get("boundary_status", {}).get("public_upload_status")
            == "public_upload_closed",
            "yymm4_render_closed": manifest.get("boundary_status", {}).get("yymm4_render_status")
            == "yymm4_render_closed",
            "no_external_references": not external_reference_hits,
            "no_forbidden_completion_claims": not forbidden_hits,
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "source_package_dir": manifest.get("source_package_dir"),
        "selected_candidate_id": manifest.get("selected_candidate_id"),
        "template_count": len(template_ids),
        "seed_sample_path": str(root / "next_episode_seed_sample.json"),
        "primary_machine_readable": str(root / "template_registry_manifest.json"),
        "primary_human_review": str(root / "template_usage.md"),
        "next_action": readiness_summary.get("next_safe_local_action"),
    }


def _load_snapshot(source_root: Path) -> dict[str, Any]:
    ir_root = source_root / "ir_bridge"
    transcript_root = source_root / "transcript_substitution_readiness"
    dashboard_root = source_root / "dashboard_readiness_ingest"
    gui_root = source_root / "gui_dashboard_panel"
    import_root = source_root / "ymm4_import_preview_pack"
    thumbnail_root = source_root / "thumbnail_visual_proof_pack"
    files = {
        "content_manifest": source_root / "MANIFEST.json",
        "topic_candidates": source_root / "topic_candidates.json",
        "content_readback": source_root / "content_spine_readback.json",
        "dashboard_status": source_root / "dashboard_status.json",
        "ir_manifest": ir_root / "bridge_manifest.json",
        "ir_episode_bridge": ir_root / "episode_bridge.json",
        "ir_writer_ir": ir_root / "writer_ir_candidate.json",
        "ir_cue_packet": ir_root / "cue_packet_candidate.json",
        "ir_draft_csv": ir_root / "draft_yymm4.csv",
        "ir_readback": ir_root / "validation_readback.json",
        "transcript_manifest": transcript_root / "substitution_manifest.json",
        "transcript_contract": transcript_root / "transcript_input_contract.json",
        "transcript_probe": transcript_root / "transcript_source_probe.json",
        "transcript_episode_bridge": transcript_root / "regenerated_episode_bridge.json",
        "transcript_writer_ir": transcript_root / "regenerated_writer_ir_candidate.json",
        "transcript_cue_packet": transcript_root / "regenerated_cue_packet_candidate.json",
        "transcript_draft_csv": transcript_root / "regenerated_draft_yymm4.csv",
        "transcript_readback": transcript_root / "validation_readback.json",
        "dashboard_summary": dashboard_root / "readiness_summary.json",
        "dashboard_pipeline": dashboard_root / "pipeline_status.json",
        "dashboard_readback": dashboard_root / "validation_readback.json",
        "gui_adapter": gui_root / "gui_dashboard_adapter.json",
        "gui_readback": gui_root / "validation_readback.json",
        "import_manifest": import_root / "import_preview_manifest.json",
        "import_csv_inventory": import_root / "yymm4_csv_inventory.json",
        "import_summary": import_root / "import_readiness_summary.json",
        "import_readback": import_root / "validation_readback.json",
        "thumbnail_manifest": thumbnail_root / "thumbnail_proof_manifest.json",
        "thumbnail_title_candidates": thumbnail_root / "title_text_candidates.json",
        "thumbnail_concepts": thumbnail_root / "thumbnail_concepts.json",
        "thumbnail_constraints": thumbnail_root / "visual_constraints.json",
        "thumbnail_readback": thumbnail_root / "validation_readback.json",
    }
    payloads = {
        name: _load_json_if_present(path)
        for name, path in files.items()
        if path.suffix.lower() == ".json"
    }
    return {
        "source_root": source_root,
        "files": files,
        "payloads": payloads,
    }


def _selected_candidate(snapshot: dict[str, Any]) -> dict[str, Any]:
    manifest = _payload(snapshot, "content_manifest")
    selected_id = manifest.get("selected_candidate_id")
    candidates = _payload(snapshot, "topic_candidates").get("candidates", [])
    if isinstance(candidates, list):
        for candidate in candidates:
            if isinstance(candidate, dict) and candidate.get("candidate_id") == selected_id:
                return candidate
        if candidates and isinstance(candidates[0], dict):
            return candidates[0]
    return {
        "candidate_id": selected_id or "unknown",
        "title": manifest.get("selected_title") or "unknown",
        "source_boundary": {},
        "yukkuri_profile": {},
        "thumbnail_profile": {},
        "channel_angle": "",
        "score_rationale": "",
    }


def _yukkuri_newsroom_template(candidate: dict[str, Any]) -> dict[str, Any]:
    profile = candidate.get("yukkuri_profile", {})
    return {
        "schema_version": "yukkuri_newsroom_template.v1",
        "template_id": "yukkuri_newsroom_template",
        "purpose": "Initialize local/offline yukkuri newsroom explainer episodes from a reusable template.",
        "template_status": "draft_offline",
        "episode_route": [
            "content_spine_template",
            "transcript_input_template",
            "writer_ir_template",
            "yymm4_import_template",
            "dashboard_status_template",
            "thumbnail_proof_template",
        ],
        "required_fields_for_real_episode": [
            "episode_id",
            "topic_or_source_packet",
            "source_boundary",
            "title",
            "yukkuri_profile.beat_outline",
            "human_episode_decision",
            "rights_review_status",
            "real_transcript_or_script_input",
        ],
        "carried_from_template": {
            "explainer_role": profile.get("explainer_role", "まりさ"),
            "listener_role": profile.get("listener_role", "れいむ"),
            "tone_family": profile.get("recommended_tone", "yukkuri newsroom explainer"),
            "default_section_count": 3,
            "status_policy": BOUNDARY_STATUS,
        },
        "closed_gates": list(CLOSED_GATES),
    }


def _content_spine_template(snapshot: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    manifest = _payload(snapshot, "content_manifest")
    boundary = candidate.get("source_boundary", {})
    return {
        "schema_version": "content_spine_template.v1",
        "template_id": "content_spine_template",
        "source_schema_reference": manifest.get("schema_version"),
        "required_fields_for_real_episode": [
            "candidate_id",
            "title",
            "candidate_score_or_selection_reason",
            "source_boundary.source_name",
            "source_boundary.freshness_status",
            "source_boundary.rights_status",
            "source_boundary.excluded_claims",
            "yukkuri_profile.hook",
            "yukkuri_profile.beat_outline",
            "thumbnail_profile.title_hook",
        ],
        "carried_from_template": {
            "selection_policy": _payload(snapshot, "topic_candidates").get("selection_policy"),
            "source_boundary_shape": {
                key: boundary.get(key)
                for key in (
                    "source_name",
                    "source_url_or_placeholder",
                    "published_at_or_placeholder",
                    "freshness_status",
                    "rights_status",
                    "attribution_note",
                    "production_status",
                )
            },
            "public_actions_blocked": list(BLOCKED_PUBLIC_ACTIONS),
        },
        "field_contract": {
            "candidate_score": "optional ranking aid; not a production approval",
            "source_boundary": "required before any downstream public or rights claim",
            "thumbnail_profile": "draft planning input only",
        },
        "default_boundary_status": BOUNDARY_STATUS,
    }


def _transcript_input_template(snapshot: dict[str, Any]) -> dict[str, Any]:
    contract = _payload(snapshot, "transcript_contract")
    probe = _payload(snapshot, "transcript_probe")
    return {
        "schema_version": "transcript_input_template.v1",
        "template_id": "transcript_input_template",
        "source_schema_reference": contract.get("schema_version"),
        "required_fields_for_real_episode": [
            "transcript_path_or_dropzone_file",
            "transcript_status",
            "source_mode",
            "speaker_mapping",
            "rights_status",
            "timing_status",
            "audio_status",
        ],
        "carried_from_template": {
            "accepted_inputs": contract.get("accepted_inputs", []),
            "required_boundary_fields": contract.get("required_boundary_fields", []),
            "parser": contract.get("normalization_readback", {}).get("parser"),
            "current_dropzone_shape": "real_input/*.txt or real_input/*.csv",
            "sample_fixture_status": probe.get("transcript_status", "sample_fixture_not_real"),
        },
        "real_episode_requirements": {
            "sample_fixture_is_never_real": True,
            "real_transcript_required_before_production": True,
            "notebooklm_api_used": False,
            "live_fetch_used": False,
        },
        "default_boundary_status": BOUNDARY_STATUS,
    }


def _writer_ir_template(snapshot: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    writer_ir = _payload(snapshot, "transcript_writer_ir") or _payload(snapshot, "ir_writer_ir")
    sections = writer_ir.get("sections", [])
    utterances = writer_ir.get("utterances", [])
    return {
        "schema_version": "writer_ir_template.v1",
        "template_id": "writer_ir_template",
        "source_schema_reference": writer_ir.get("schema_version"),
        "production_ir_spec_reference": writer_ir.get("production_ir_spec_reference", "docs/PRODUCTION_IR_SPEC.md"),
        "required_fields_for_real_episode": [
            "video_id",
            "sections[].section_id",
            "sections[].arc_phase",
            "utterances[].index",
            "utterances[].speaker",
            "utterances[].text",
            "utterances[].section_id",
            "utterances[].row_start",
            "utterances[].row_end",
            "source_boundary",
        ],
        "carried_from_template": {
            "section_pattern": [
                {
                    "section_id": section.get("section_id"),
                    "arc_phase": section.get("arc_phase"),
                    "default_bg": section.get("default_bg"),
                    "default_face": section.get("default_face"),
                }
                for section in sections
                if isinstance(section, dict)
            ],
            "utterance_shape": sorted({key for item in utterances if isinstance(item, dict) for key in item.keys()}),
            "tone": writer_ir.get("tone") or candidate.get("yukkuri_profile", {}).get("recommended_tone"),
            "compatibility_status": "draft_template_not_validate_ir_ready",
        },
        "gates_before_validate_ir": [
            "human-reviewed transcript/script",
            "row_start/row_end annotation from YMM4 CSV import or accepted timing route",
            "production maps when face/bg/slot/overlay/se/motion are used",
            "human source/rights/publication review",
        ],
        "default_boundary_status": BOUNDARY_STATUS,
    }


def _yymm4_import_template(snapshot: dict[str, Any]) -> dict[str, Any]:
    inventory = _payload(snapshot, "import_csv_inventory")
    summary = _payload(snapshot, "import_summary")
    return {
        "schema_version": "yymm4_import_template.v1",
        "template_id": "yymm4_import_template",
        "source_schema_reference": inventory.get("schema_version"),
        "required_fields_for_real_episode": [
            "draft_yymm4_csv_path",
            "csv_contract.required_columns",
            "csv_contract.header_mode",
            "speaker_names",
            "row_count",
            "yymm4_gui_import_review_status",
            "voiceitem_timing_readback",
        ],
        "carried_from_template": {
            "csv_contract": inventory.get("csv_contract", {}),
            "speaker_count_shape": sorted(inventory.get("speaker_counts", {}).keys()),
            "headerless_import_csv": inventory.get("header_present") is False,
            "current_preview_row_count": inventory.get("row_count"),
            "status_categories": list(STATUS_CATEGORIES),
        },
        "current_boundary_status": summary.get("boundary_status", BOUNDARY_STATUS),
        "not_claimed": [
            "YMM4 GUI launch",
            "YMM4 import",
            "VoiceItem timing readback",
            "YMM4 render",
            "production .ymmp",
        ],
    }


def _thumbnail_proof_template(snapshot: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    title_candidates = _payload(snapshot, "thumbnail_title_candidates")
    concepts = _payload(snapshot, "thumbnail_concepts")
    constraints = _payload(snapshot, "thumbnail_constraints")
    thumbnail_profile = candidate.get("thumbnail_profile", {})
    return {
        "schema_version": "thumbnail_proof_template.v1",
        "template_id": "thumbnail_proof_template",
        "required_fields_for_real_episode": [
            "title_hook",
            "short_text_candidates",
            "visual_motif",
            "forbidden_avoid_claims",
            "source_rights_caution",
            "thumbnail_direction_decision",
        ],
        "carried_from_template": {
            "text_candidate_shape": sorted(title_candidates.keys()),
            "concept_shape": sorted(concepts.keys()),
            "layout_constraints": constraints.get("layout_constraints", {}),
            "proof_status": "static_proof_only_not_final_thumbnail",
            "no_external_media": constraints.get("rights_boundaries", {}).get("no_external_media", True),
            "current_motif": thumbnail_profile.get("visual_motif"),
        },
        "rights_boundaries": constraints.get("rights_boundaries", {}),
        "not_claimed": [
            "final thumbnail image",
            "external image/media download",
            "image generation API",
            "logos, player photos, broadcast stills, or public-ready artwork",
        ],
        "default_boundary_status": BOUNDARY_STATUS,
    }


def _dashboard_status_template(snapshot: dict[str, Any]) -> dict[str, Any]:
    summary = _payload(snapshot, "dashboard_summary")
    pipeline = _payload(snapshot, "dashboard_pipeline")
    return {
        "schema_version": "dashboard_status_template.v1",
        "template_id": "dashboard_status_template",
        "source_schema_reference": summary.get("schema_version"),
        "required_fields_for_real_episode": [
            "capability_rows",
            "status_groups",
            "boundary_status",
            "input_reality",
            "next_action",
            "source_artifact_index",
        ],
        "carried_from_template": {
            "status_categories": list(STATUS_CATEGORIES),
            "route_nodes": [item.get("node") for item in pipeline.get("route", []) if isinstance(item, dict)],
            "capability_ids": [
                item.get("capability_id")
                for item in summary.get("capability_rows", [])
                if isinstance(item, dict)
            ],
            "bar_mode": "hypothesis",
        },
        "default_boundary_status": BOUNDARY_STATUS,
        "dashboard_is_read_only": True,
    }


def _episode_factory_templates(
    template_payloads: dict[str, dict[str, Any]],
    candidate: dict[str, Any],
) -> dict[str, Any]:
    templates = []
    for template_id in REQUIRED_TEMPLATE_IDS:
        payload = template_payloads[template_id]
        templates.append({
            "template_id": template_id,
            "file": f"{template_id}.json",
            "schema_version": payload.get("schema_version"),
            "required_field_count": len(payload.get("required_fields_for_real_episode", [])),
            "carried_field_groups": sorted(payload.get("carried_from_template", {}).keys()),
        })
    return {
        "schema_version": "episode_factory_templates.v1",
        "registry_status": "draft_offline",
        "selected_source_candidate_id": candidate.get("candidate_id"),
        "templates": templates,
        "init_flow": [
            "load template_registry_manifest.json",
            "copy next_episode_seed_sample.json to a new local run record",
            "replace required_inputs.topic_or_source_packet with a real local source packet or reviewed topic capsule",
            "run build-content-spine or an equivalent approved local source-pack adapter",
            "rerun downstream packages only after real transcript/source gates are satisfied",
        ],
        "required_real_inputs": [
            "topic_or_source_packet",
            "real_transcript_or_script",
            "rights_review_status",
            "human_episode_decision",
            "YMM4 import/timing readback before production claims",
        ],
        "carry_forward_allowed": [
            "yukkuri role names",
            "three-section explainer route",
            "CSV contract shape",
            "dashboard status categories",
            "thumbnail proof safety constraints",
        ],
        "boundary_status": BOUNDARY_STATUS,
        "closed_gates": list(CLOSED_GATES),
    }


def _next_episode_seed_sample(
    *,
    artifact_id: str,
    output_root: Path,
    selected_candidate: dict[str, Any],
    template_index: dict[str, Any],
) -> dict[str, Any]:
    profile = selected_candidate.get("yukkuri_profile", {})
    thumbnail = selected_candidate.get("thumbnail_profile", {})
    return {
        "schema_version": "next_episode_seed_sample.v1",
        "seed_id": "next_yukkuri_newsroom_episode_seed_sample_001",
        "episode_id": "yukkuri_newsroom_episode_002_seed_sample",
        "status": "draft_offline_seed_sample",
        "derived_from_registry_artifact_id": artifact_id,
        "template_registry_dir": str(output_root),
        "source_template_files": [item["file"] for item in template_index.get("templates", [])],
        "required_inputs": {
            "topic_or_source_packet": {
                "state": "required_for_real_episode",
                "value": None,
                "accepted_shape": "local reviewed topic/source packet with source_boundary",
            },
            "real_transcript": {
                "state": "required_before_production",
                "value": None,
                "accepted_shape": ".txt or .csv transcript through transcript_input_template",
            },
            "rights_review": {
                "state": "required_before_public_use",
                "value": None,
                "accepted_shape": "human review result; no legal/public-ready claim is inferred",
            },
            "human_episode_decision": {
                "state": "required_before_yymm4_import",
                "value": None,
                "accepted_shape": "accept/revise/hold decision on the next episode capsule",
            },
        },
        "carried_defaults": {
            "explainer_role": profile.get("explainer_role", "まりさ"),
            "listener_role": profile.get("listener_role", "れいむ"),
            "section_count": 3,
            "csv_header_mode": "headerless_yymm4_csv",
            "thumbnail_text_constraints": {
                "max_primary_tokens": 4,
                "max_short_text_candidates_on_canvas": 1,
            },
            "thumbnail_safety": {
                "no_external_media": True,
                "no_logos_or_player_photos": True,
                "source_rights_caution": thumbnail.get("source_rights_caution"),
            },
        },
        "initialized_output_plan": [
            "content_spine_package",
            "transcript_substitution_readiness",
            "dashboard_readiness_ingest",
            "gui_dashboard_panel",
            "ymm4_import_preview_pack",
            "thumbnail_visual_proof_pack",
        ],
        "boundary_status": BOUNDARY_STATUS,
        "closed_gates": list(CLOSED_GATES),
        "not_created_by_seed_sample": [
            "real transcript",
            "YMM4 project",
            "production .ymmp",
            "rendered video",
            "final thumbnail image",
            "public upload or visibility change",
        ],
    }


def _init_readiness_summary(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    snapshot: dict[str, Any],
    selected_candidate: dict[str, Any],
    template_index: dict[str, Any],
    seed_sample: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "episode_factory_init_readiness_summary.v1",
        "artifact_id": artifact_id,
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": selected_candidate.get("candidate_id"),
        "deterministic_generation_path": True,
        "seed_sample_path": str(output_root / "next_episode_seed_sample.json"),
        "template_count": len(template_index.get("templates", [])),
        "source_artifact_count": len(snapshot.get("files", {})),
        "required_for_real_second_episode": list(seed_sample.get("required_inputs", {}).keys()),
        "carry_forward_from_current_pilot": template_index.get("carry_forward_allowed", []),
        "boundary_status": BOUNDARY_STATUS,
        "closed_gates": list(CLOSED_GATES),
        "init_status": {
            "can_generate_registry_offline": True,
            "can_create_seed_sample_without_external_input": True,
            "can_claim_production_readiness": False,
            "can_launch_yymm4": False,
            "can_publish": False,
        },
        "next_safe_local_action": (
            "Review template_usage.md and next_episode_seed_sample.json; then provide a real local "
            "topic/source packet and transcript before any YMM4 import, render, rights, or public work."
        ),
    }


def _manifest_payload(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    selected_candidate: dict[str, Any],
    template_index: dict[str, Any],
    readiness_summary: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "episode_factory_template_registry_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-factory-template-registry",
        "status": "generated",
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": selected_candidate.get("candidate_id"),
        "files": {name: str(output_root / name) for name in REQUIRED_EPISODE_FACTORY_TEMPLATE_REGISTRY_FILES},
        "source_inputs": {key: str(path) for key, path in snapshot.get("files", {}).items()},
        "template_files": [item["file"] for item in template_index.get("templates", [])],
        "seed_sample_path": readiness_summary.get("seed_sample_path"),
        "boundary_status": BOUNDARY_STATUS,
        "boundaries": {
            "local_offline_review_only": True,
            "template_registry_only": True,
            "seed_sample_only": True,
            "sample_fixture_not_real_preserved": True,
            "draft_offline_only": True,
            "no_live_fetch": True,
            "no_external_media_download": True,
            "no_embedded_external_images": True,
            "no_youtube_publication": True,
            "no_oauth_or_paid_api": True,
            "no_rights_or_legal_acceptance": True,
            "no_yymm4_gui_launch_or_import_or_render": True,
            "no_production_ymmp_generation": True,
            "no_audio_generation": True,
        },
        "next_safe_local_action": readiness_summary.get("next_safe_local_action"),
    }


def _source_artifact_index(snapshot: dict[str, Any], output_root: Path, repo_root: Path) -> dict[str, Any]:
    source_inputs = []
    for key, path in snapshot.get("files", {}).items():
        payload = _payload(snapshot, key)
        source_inputs.append({
            "id": key,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": "ready" if path.exists() else "missing",
            "schema_version": payload.get("schema_version"),
        })
    generated_outputs = []
    for name in REQUIRED_EPISODE_FACTORY_TEMPLATE_REGISTRY_FILES:
        path = output_root / name
        generated_outputs.append({
            "id": name,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": "ready" if path.exists() else "missing",
        })
    return {
        "schema_version": "episode_factory_source_artifact_index.v1",
        "source_inputs": source_inputs,
        "generated_outputs": generated_outputs,
        "artifact_counts": {
            "source_total": len(source_inputs),
            "source_present": sum(1 for item in source_inputs if item["exists"]),
            "generated_total": len(generated_outputs),
            "generated_present": sum(1 for item in generated_outputs if item["exists"]),
        },
    }


def _render_template_usage(summary: dict[str, Any]) -> str:
    return "\n".join([
        "# Episode Factory Template Registry Usage",
        "",
        f"- artifact_id: {summary['artifact_id']}",
        f"- selected_candidate_id: {summary.get('selected_candidate_id')}",
        f"- seed_sample: `next_episode_seed_sample.json`",
        f"- deterministic_generation_path: {str(summary.get('deterministic_generation_path')).lower()}",
        "",
        "## Regenerate",
        "",
        "```bash",
        "python -m src.cli.main build-episode-factory-template-registry --package production_pilots/yukkuri_newsroom_content_spine_001",
        "```",
        "",
        "## Use For Next Episode",
        "",
        "1. Open `next_episode_seed_sample.json`.",
        "2. Replace required inputs with a reviewed local topic/source packet and real transcript path.",
        "3. Keep `sample_fixture_not_real`, `draft_offline`, `rights_boundary`, `public_upload_closed`, and `yymm4_render_closed` visible until real gates are satisfied.",
        "4. Rerun downstream packages only after the relevant local inputs exist.",
        "",
        "## Closed Gates",
        "",
        *[f"- {gate}" for gate in summary.get("closed_gates", [])],
        "",
        "## Next Safe Local Action",
        "",
        summary["next_safe_local_action"],
        "",
    ])


def _render_review_checklist(summary: dict[str, Any]) -> str:
    return "\n".join([
        "# Episode Factory Template Registry Review Checklist",
        "",
        "- Confirm `template_registry_manifest.json` lists every generated template file.",
        "- Confirm `episode_factory_templates.json` separates required real episode fields from carry-forward defaults.",
        "- Confirm `next_episode_seed_sample.json` has required input placeholders, not fake real inputs.",
        "- Confirm sample fixture, draft/offline, rights boundary, public upload, and YMM4 render gates remain closed.",
        "- Confirm no external media, scraping, OAuth, payment, YMM4 GUI/import/render, production `.ymmp`, or publication action is implied.",
        "",
        "## Next Safe Local Action",
        "",
        summary["next_safe_local_action"],
        "",
    ])


def _render_limitations(summary: dict[str, Any]) -> str:
    lines = [
        "# Episode Factory Template Registry Limitations",
        "",
        "This package is a local/offline template registry and seed sample only.",
        "",
        "Not performed:",
        "",
    ]
    for gate in summary.get("closed_gates", []):
        lines.append(f"- {gate}")
    lines.extend([
        "- real transcript rerun",
        "- final transcript, timing, source, rights, legal, or public-ready acceptance",
        "- actual second episode initialization from a real source packet",
        "",
        "The seed sample exists to make the next local episode easier to initialize. It is not production material.",
        "",
    ])
    return "\n".join(lines)


def _payload(snapshot: dict[str, Any], key: str) -> dict[str, Any]:
    payload = snapshot.get("payloads", {}).get(key)
    return payload if isinstance(payload, dict) else {}


def _combined_text(paths: Any) -> str:
    chunks = []
    for path in paths:
        if Path(path).is_file():
            chunks.append(Path(path).read_text(encoding="utf-8"))
    return "\n".join(chunks)


def _external_reference_hits(text: str) -> list[str]:
    hits = []
    for pattern in EXTERNAL_REFERENCE_PATTERNS:
        match = pattern.search(text)
        if match:
            hits.append(match.group(0))
    return hits


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
