"""Local/offline episode factory seed instantiation dry-run.

This module initializes a second yukkuri newsroom episode seed from the
existing episode factory template registry. It creates reviewable dry-run
artifacts only; it does not fetch sources, run transcript generation, launch
YMM4, render, publish, or claim rights/public readiness.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.pipeline.episode_factory_template_registry import (
    BOUNDARY_STATUS as REGISTRY_BOUNDARY_STATUS,
    CLOSED_GATES,
    REQUIRED_EPISODE_FACTORY_TEMPLATE_REGISTRY_FILES,
    REQUIRED_TEMPLATE_IDS,
)

DEFAULT_OUTPUT_DIRNAME = "factory_seed_dry_run_002"
DEFAULT_ARTIFACT_ID = "factory_seed_instantiation_dry_run_002"
DEFAULT_EPISODE_ID = "yukkuri_newsroom_episode_002_dry_run_seed"

REQUIRED_FACTORY_SEED_INSTANTIATION_FILES = (
    "seed_instantiation_manifest.json",
    "episode_seed.json",
    "dry_run_topic_source_packet.json",
    "required_real_inputs.json",
    "carried_template_defaults.json",
    "planned_pipeline_steps.json",
    "boundary_status.json",
    "init_readiness_summary.json",
    "source_artifact_index.json",
    "content_spine_input_candidate.json",
    "review_checklist.md",
    "limitations.md",
    "validation_readback.json",
)

JSON_FACTORY_SEED_FILES = tuple(
    name
    for name in REQUIRED_FACTORY_SEED_INSTANTIATION_FILES
    if name.endswith(".json") and name != "validation_readback.json"
)

EXTERNAL_REFERENCE_PATTERNS = (
    re.compile(r"\b(src|href)\s*=\s*['\"]https?://", re.IGNORECASE),
    re.compile(r"url\(\s*['\"]?https?://", re.IGNORECASE),
    re.compile(r"\bhttps?://", re.IGNORECASE),
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
    '"public_upload_open": true',
)


def instantiate_episode_factory_seed(
    *,
    registry_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
    episode_id: str = DEFAULT_EPISODE_ID,
) -> dict[str, Any]:
    """Instantiate a local/offline dry-run seed from the template registry."""
    registry_root = Path(registry_dir)
    if not registry_root.exists():
        raise FileNotFoundError(registry_root)
    output_root = Path(output_dir) if output_dir else registry_root.parent / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)

    repo_root = _find_repo_root(registry_root)
    registry = _load_registry_payloads(registry_root)
    registry_manifest = registry["template_registry_manifest"]
    template_index = registry["episode_factory_templates"]
    seed_sample = registry["next_episode_seed_sample"]
    readiness = registry["init_readiness_summary"]

    boundary_status = _boundary_status()
    dry_run_packet = _dry_run_topic_source_packet(
        artifact_id=artifact_id,
        episode_id=episode_id,
        seed_sample=seed_sample,
        registry_manifest=registry_manifest,
        boundary_status=boundary_status,
    )
    required_real_inputs = _required_real_inputs(
        seed_sample=seed_sample,
        boundary_status=boundary_status,
    )
    carried_defaults = _carried_template_defaults(
        seed_sample=seed_sample,
        template_index=template_index,
        registry=registry,
        boundary_status=boundary_status,
    )
    planned_steps = _planned_pipeline_steps(
        registry_manifest=registry_manifest,
        output_root=output_root,
        boundary_status=boundary_status,
    )
    content_spine_candidate = _content_spine_input_candidate(
        dry_run_packet=dry_run_packet,
        carried_defaults=carried_defaults,
        boundary_status=boundary_status,
    )
    episode_seed = _episode_seed(
        artifact_id=artifact_id,
        episode_id=episode_id,
        output_root=output_root,
        registry_root=registry_root,
        registry_manifest=registry_manifest,
        seed_sample=seed_sample,
        dry_run_packet=dry_run_packet,
        required_real_inputs=required_real_inputs,
        carried_defaults=carried_defaults,
        planned_steps=planned_steps,
        boundary_status=boundary_status,
    )
    init_summary = _init_readiness_summary(
        artifact_id=artifact_id,
        episode_id=episode_id,
        registry_root=registry_root,
        output_root=output_root,
        registry_manifest=registry_manifest,
        registry_readiness=readiness,
        required_real_inputs=required_real_inputs,
        boundary_status=boundary_status,
    )
    manifest = _manifest_payload(
        artifact_id=artifact_id,
        episode_id=episode_id,
        registry_root=registry_root,
        output_root=output_root,
        registry_manifest=registry_manifest,
        boundary_status=boundary_status,
        init_summary=init_summary,
    )

    _write_json(output_root / "seed_instantiation_manifest.json", manifest)
    _write_json(output_root / "episode_seed.json", episode_seed)
    _write_json(output_root / "dry_run_topic_source_packet.json", dry_run_packet)
    _write_json(output_root / "required_real_inputs.json", required_real_inputs)
    _write_json(output_root / "carried_template_defaults.json", carried_defaults)
    _write_json(output_root / "planned_pipeline_steps.json", planned_steps)
    _write_json(output_root / "boundary_status.json", boundary_status)
    _write_json(output_root / "init_readiness_summary.json", init_summary)
    _write_json(output_root / "content_spine_input_candidate.json", content_spine_candidate)
    _write_text(output_root / "review_checklist.md", _render_review_checklist(init_summary))
    _write_text(output_root / "limitations.md", _render_limitations(init_summary))

    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(registry_root, output_root, repo_root))
    readback = validate_factory_seed_instantiation(output_root, registry_dir=registry_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(registry_root, output_root, repo_root))
    final_readback = validate_factory_seed_instantiation(output_root, registry_dir=registry_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_factory_seed_instantiation(
    output_dir: str | Path,
    *,
    registry_dir: str | Path | None = None,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate dry-run seed files, source separation, and closed boundaries."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_FACTORY_SEED_INSTANTIATION_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    json_payloads = {
        name.removesuffix(".json"): _load_json_if_present(files[name])
        for name in JSON_FACTORY_SEED_FILES
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["seed_instantiation_manifest"]
    episode_seed = json_payloads["episode_seed"]
    dry_run_packet = json_payloads["dry_run_topic_source_packet"]
    required_real_inputs = json_payloads["required_real_inputs"]
    carried_defaults = json_payloads["carried_template_defaults"]
    planned_steps = json_payloads["planned_pipeline_steps"]
    boundary_status = json_payloads["boundary_status"]
    init_summary = json_payloads["init_readiness_summary"]
    source_index = json_payloads["source_artifact_index"]
    content_spine_candidate = json_payloads["content_spine_input_candidate"]

    if manifest.get("artifact_kind") != "factory-seed-instantiation-dry-run":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "dry_run_seed_instantiated":
        failed_checks.append("manifest_status_unexpected")
    if episode_seed.get("status") != "dry_run":
        failed_checks.append("episode_seed_status_unexpected")
    if episode_seed.get("source_reality") != "sample_fixture_not_real":
        failed_checks.append("episode_seed_source_reality_unexpected")
    if dry_run_packet.get("status") != "dry_run":
        failed_checks.append("dry_run_packet_status_unexpected")
    if dry_run_packet.get("source_boundary", {}).get("freshness_status") != "offline_fixture_not_live":
        failed_checks.append("dry_run_source_not_offline_fixture")
    if dry_run_packet.get("source_boundary", {}).get("rights_status") != "sample_only_no_publication":
        failed_checks.append("dry_run_rights_boundary_missing")

    _check_boundary_flags(boundary_status, failed_checks)
    _check_boundary_flags(manifest.get("boundary_status", {}), failed_checks, prefix="manifest_")
    _check_boundary_flags(episode_seed.get("boundary_status", {}), failed_checks, prefix="seed_")

    real_inputs = required_real_inputs.get("required_real_inputs", {})
    for key in ("topic_or_source_packet", "real_transcript", "rights_review", "human_episode_decision"):
        if key not in real_inputs:
            failed_checks.append(f"required_real_input_missing:{key}")
        elif real_inputs.get(key, {}).get("value") is not None:
            failed_checks.append(f"required_real_input_has_dry_run_value:{key}")

    if not episode_seed.get("synthetic_dry_run_placeholders"):
        failed_checks.append("synthetic_placeholders_missing")
    if not episode_seed.get("inherited_defaults"):
        failed_checks.append("inherited_defaults_missing")
    if not carried_defaults.get("carried_template_defaults"):
        failed_checks.append("carried_template_defaults_missing")
    if carried_defaults.get("state") != "inherited_defaults_only":
        failed_checks.append("carried_defaults_state_unexpected")
    if planned_steps.get("execution_policy") != "plan_only_no_downstream_execution":
        failed_checks.append("planned_steps_execution_policy_unexpected")
    if any(step.get("execution_status") == "executed_downstream" for step in planned_steps.get("steps", [])):
        failed_checks.append("downstream_step_executed")
    if init_summary.get("deterministic_seed_instantiation_path") is not True:
        failed_checks.append("deterministic_seed_instantiation_missing")
    if init_summary.get("init_status", {}).get("can_initialize_seed_from_registry_offline") is not True:
        failed_checks.append("offline_seed_init_not_confirmed")
    if init_summary.get("init_status", {}).get("can_run_downstream_pipeline_now") is not False:
        failed_checks.append("downstream_pipeline_not_closed")

    if content_spine_candidate.get("schema_version") != "content_spine_source_manifest.v1":
        failed_checks.append("content_spine_candidate_schema_unexpected")
    candidates = content_spine_candidate.get("candidates", [])
    if not candidates:
        failed_checks.append("content_spine_candidate_empty")
    elif candidates[0].get("freshness_status") != "offline_fixture_not_live":
        failed_checks.append("content_spine_candidate_not_offline_fixture")

    if source_index.get("artifact_counts", {}).get("source_present", 0) < 3:
        failed_checks.append("source_artifact_index_too_sparse")
    if source_index.get("artifact_counts", {}).get("generated_present", 0) < len(REQUIRED_FACTORY_SEED_INSTANTIATION_FILES) - 1:
        failed_checks.append("generated_artifact_index_too_sparse")

    if registry_dir is not None:
        missing_registry_files = [
            name
            for name in REQUIRED_EPISODE_FACTORY_TEMPLATE_REGISTRY_FILES
            if not (Path(registry_dir) / name).exists()
        ]
        failed_checks.extend(f"registry_missing_file:{name}" for name in missing_registry_files)

    combined_text = _combined_text(files.values())
    external_reference_hits = _external_reference_hits(combined_text)
    forbidden_hits = [claim for claim in FORBIDDEN_COMPLETION_CLAIMS if claim in combined_text]
    failed_checks.extend(f"external_reference:{hit}" for hit in external_reference_hits)
    failed_checks.extend(f"forbidden_completion_claim:{claim}" for claim in forbidden_hits)

    return {
        "schema_version": "factory_seed_instantiation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(
                path.exists()
                for name, path in files.items()
                if require_readback or name != "validation_readback.json"
            ),
            "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
            "registry_input_files_present": not any(item.startswith("registry_missing_file:") for item in failed_checks),
            "required_real_inputs_separated": all(
                key in real_inputs and real_inputs[key].get("value") is None
                for key in ("topic_or_source_packet", "real_transcript", "rights_review", "human_episode_decision")
            ),
            "carried_defaults_separated": carried_defaults.get("state") == "inherited_defaults_only",
            "synthetic_placeholders_marked": bool(episode_seed.get("synthetic_dry_run_placeholders")),
            "dry_run_marked": boundary_status.get("dry_run") is True,
            "sample_fixture_not_real_marked": boundary_status.get("sample_fixture_not_real") is True,
            "rights_boundary_preserved": boundary_status.get("rights_boundary") == "sample_only_no_publication",
            "public_upload_closed": boundary_status.get("public_upload_closed") is True,
            "yymm4_render_closed": boundary_status.get("yymm4_render_closed") is True,
            "no_external_references": not external_reference_hits,
            "no_forbidden_completion_claims": not forbidden_hits,
            "content_spine_candidate_present": bool(candidates),
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "episode_id": manifest.get("episode_id"),
        "source_registry_dir": manifest.get("source_registry_dir"),
        "primary_machine_readable": str(root / "seed_instantiation_manifest.json"),
        "episode_seed_path": str(root / "episode_seed.json"),
        "topic_source_packet_path": str(root / "dry_run_topic_source_packet.json"),
        "content_spine_input_candidate_path": str(root / "content_spine_input_candidate.json"),
        "primary_human_review": str(root / "review_checklist.md"),
        "next_action": init_summary.get("next_safe_local_action"),
    }


def _load_registry_payloads(registry_root: Path) -> dict[str, dict[str, Any]]:
    required = (
        "template_registry_manifest.json",
        "episode_factory_templates.json",
        "next_episode_seed_sample.json",
        "init_readiness_summary.json",
    )
    payloads: dict[str, dict[str, Any]] = {}
    for filename in required:
        path = registry_root / filename
        if not path.exists():
            raise FileNotFoundError(path)
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(payload, dict):
            raise ValueError(f"registry file must contain a JSON object: {path}")
        payloads[filename.removesuffix(".json")] = payload
    for template_id in REQUIRED_TEMPLATE_IDS:
        path = registry_root / f"{template_id}.json"
        payload = _load_json_if_present(path)
        if isinstance(payload, dict):
            payloads[template_id] = payload
    return payloads


def _boundary_status() -> dict[str, Any]:
    return {
        **REGISTRY_BOUNDARY_STATUS,
        "dry_run": True,
        "sample_fixture_not_real": True,
        "rights_boundary": "sample_only_no_publication",
        "public_upload_closed": True,
        "yymm4_render_closed": True,
        "factory_seed_status": "instantiated_from_template_registry",
        "source_packet_status": "synthetic_local_dry_run",
        "content_spine_candidate_status": "derived_candidate_only_not_executed",
        "real_source_status": "required_before_real_episode",
        "real_transcript_status": "required_before_production",
        "external_network_status": "closed",
        "oauth_status": "closed",
        "payment_status": "closed",
        "public_upload_status": "public_upload_closed",
        "yymm4_render_status": "yymm4_render_closed",
        "production_status": "blocked_by_true_gate",
    }


def _dry_run_topic_source_packet(
    *,
    artifact_id: str,
    episode_id: str,
    seed_sample: dict[str, Any],
    registry_manifest: dict[str, Any],
    boundary_status: dict[str, Any],
) -> dict[str, Any]:
    carried = seed_sample.get("carried_defaults", {})
    return {
        "schema_version": "factory_seed_dry_run_topic_source_packet.v1",
        "packet_id": "dry_run_topic_source_packet_002",
        "artifact_id": artifact_id,
        "episode_id": episode_id,
        "status": "dry_run",
        "source_reality": "sample_fixture_not_real",
        "registry_source": {
            "registry_artifact_id": registry_manifest.get("artifact_id"),
            "registry_status": registry_manifest.get("status"),
            "source_candidate_id": registry_manifest.get("selected_candidate_id"),
        },
        "topic_capsule": {
            "candidate_id": "factory_seed_dry_run_002",
            "title": "Factory seed dry-run placeholder for a second yukkuri newsroom episode",
            "candidate_score": 1,
            "score_rationale": "Synthetic local seed used only to prove registry initialization; not a real news topic.",
            "channel_angle": "dry-run factory proof, not publishable editorial material",
        },
        "source_boundary": {
            "source_name": "Synthetic Yukkuri Newsroom Factory Seed Dry-Run",
            "source_url_or_placeholder": "offline://factory_seed_dry_run/yukkuri_newsroom_episode_002",
            "published_at_or_placeholder": "dry_run_placeholder_date_required",
            "freshness_status": "offline_fixture_not_live",
            "rights_status": "sample_only_no_publication",
            "attribution_note": "Synthetic/local dry-run packet; no public source or rights claim.",
            "excluded_claims": [
                "No claim that this is a real source packet.",
                "No claim that the topic is current news.",
                "No publication readiness or rights clearance.",
                "No external media, scraping, OAuth, payment, YMM4 import, render, or upload.",
            ],
            "production_status": "dry_run_only_not_production",
            "external_media_required": False,
            "network_required": False,
        },
        "yukkuri_profile": {
            "explainer_role": carried.get("explainer_role"),
            "listener_role": carried.get("listener_role"),
            "hook": "Dry-run only: confirm the factory can open a second episode seed.",
            "why_it_matters": "The registry should initialize a new package without copying the original pilot by hand.",
            "beat_outline": [
                "Load the template registry.",
                "Separate inherited defaults from real required inputs.",
                "Mark the source packet as synthetic dry-run material.",
                "Stop before transcript, YMM4, rights, render, or publication work.",
            ],
            "recommended_tone": carried.get("tone_family", "fact-first yukkuri explainer"),
            "glossary_terms": ["factory seed", "template registry", "dry-run boundary"],
            "likely_audience": "internal reviewers",
            "channel_fit": "not a public episode; local factory proof only",
        },
        "thumbnail_profile": {
            "title_hook": "DRY RUN",
            "short_text_candidates": ["DRY RUN", "SEED ONLY"],
            "visual_motif": "Original abstract seed card and closed-gate labels.",
            "forbidden_avoid_claims": [
                "Do not use public news imagery.",
                "Do not imply final thumbnail readiness.",
                "Do not use logos, player photos, broadcast stills, or external media.",
            ],
            "source_rights_caution": "Use only original local placeholders until a real source packet is reviewed.",
            "designer_note": "This is a boundary marker, not a production thumbnail direction.",
        },
        "boundary_status": boundary_status,
    }


def _required_real_inputs(*, seed_sample: dict[str, Any], boundary_status: dict[str, Any]) -> dict[str, Any]:
    seed_required = seed_sample.get("required_inputs", {})
    return {
        "schema_version": "factory_seed_required_real_inputs.v1",
        "state": "required_real_inputs_only",
        "note": "Values are intentionally null in this dry-run. Synthetic placeholders live in dry_run_topic_source_packet.json.",
        "required_real_inputs": {
            "topic_or_source_packet": {
                "state": seed_required.get("topic_or_source_packet", {}).get("state", "required_for_real_episode"),
                "value": None,
                "accepted_shape": "reviewed local topic/source packet with source_boundary and rights notes",
                "blocks": ["content_spine_real_run", "editorial_claims", "public_use"],
            },
            "real_transcript": {
                "state": seed_required.get("real_transcript", {}).get("state", "required_before_production"),
                "value": None,
                "accepted_shape": "human-reviewed transcript/script input routed through transcript_input_template",
                "blocks": ["writer_ir_claim", "csv_timing_claim", "production_readiness"],
            },
            "rights_review": {
                "state": seed_required.get("rights_review", {}).get("state", "required_before_public_use"),
                "value": None,
                "accepted_shape": "human rights/public-use review record",
                "blocks": ["thumbnail_public_use", "publication", "legal_or_rights_acceptance"],
            },
            "human_episode_decision": {
                "state": seed_required.get("human_episode_decision", {}).get("state", "required_before_yymm4_import"),
                "value": None,
                "accepted_shape": "accept/revise/hold decision on the real episode capsule",
                "blocks": ["YMM4 import", "YMM4 render", "production .ymmp"],
            },
        },
        "closed_until_real_inputs_exist": [
            "downstream content-spine real run",
            "real transcript substitution",
            "YMM4 GUI/import/render",
            "production .ymmp",
            "public upload",
        ],
        "boundary_status": boundary_status,
    }


def _carried_template_defaults(
    *,
    seed_sample: dict[str, Any],
    template_index: dict[str, Any],
    registry: dict[str, dict[str, Any]],
    boundary_status: dict[str, Any],
) -> dict[str, Any]:
    template_summaries = []
    for template in template_index.get("templates", []):
        if not isinstance(template, dict):
            continue
        template_id = template.get("template_id")
        payload = registry.get(str(template_id), {})
        template_summaries.append({
            "template_id": template_id,
            "file": template.get("file"),
            "required_field_count": template.get("required_field_count"),
            "carried_field_groups": template.get("carried_field_groups", []),
            "carried_from_template": payload.get("carried_from_template", {}),
        })
    return {
        "schema_version": "factory_seed_carried_template_defaults.v1",
        "state": "inherited_defaults_only",
        "derived_from_seed_sample_id": seed_sample.get("seed_id"),
        "carried_template_defaults": seed_sample.get("carried_defaults", {}),
        "carry_forward_allowed": template_index.get("carry_forward_allowed", []),
        "source_template_files": seed_sample.get("source_template_files", []),
        "template_summaries": template_summaries,
        "not_real_inputs": [
            "topic_or_source_packet",
            "real_transcript",
            "rights_review",
            "human_episode_decision",
            "YMM4 import/timing readback",
        ],
        "boundary_status": boundary_status,
    }


def _planned_pipeline_steps(
    *,
    registry_manifest: dict[str, Any],
    output_root: Path,
    boundary_status: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "factory_seed_planned_pipeline_steps.v1",
        "execution_policy": "plan_only_no_downstream_execution",
        "source_registry_artifact_id": registry_manifest.get("artifact_id"),
        "steps": [
            {
                "step_id": "load_registry",
                "target_artifact": "episode_factory_template_registry",
                "execution_status": "completed_local_read",
                "requires_real_input": False,
                "output": "seed_instantiation_manifest.json",
            },
            {
                "step_id": "instantiate_dry_run_seed",
                "target_artifact": "episode_seed",
                "execution_status": "completed_local_dry_run",
                "requires_real_input": False,
                "output": "episode_seed.json",
            },
            {
                "step_id": "derive_content_spine_input_candidate",
                "target_artifact": "content_spine_source_manifest",
                "execution_status": "completed_candidate_only_not_executed",
                "requires_real_input": False,
                "output": "content_spine_input_candidate.json",
            },
            {
                "step_id": "real_content_spine_run",
                "target_artifact": "content_spine_package",
                "execution_status": "deferred",
                "requires_real_input": True,
                "blocked_by": "real topic/source packet",
            },
            {
                "step_id": "real_transcript_substitution",
                "target_artifact": "transcript_substitution_readiness",
                "execution_status": "deferred",
                "requires_real_input": True,
                "blocked_by": "real transcript/script input",
            },
            {
                "step_id": "dashboard_and_preview_refresh",
                "target_artifact": "dashboard/gui/import/thumbnail review packs",
                "execution_status": "deferred",
                "requires_real_input": True,
                "blocked_by": "real source/transcript gates and human episode decision",
            },
            {
                "step_id": "yymm4_publication_or_production_work",
                "target_artifact": "YMM4/import/render/publication",
                "execution_status": "closed",
                "requires_real_input": True,
                "blocked_by": "true YMM4, rights, production, and public gates",
            },
        ],
        "regeneration_command": (
            "python -m src.cli.main instantiate-episode-factory-seed "
            "--registry production_pilots/yukkuri_newsroom_content_spine_001/episode_factory_template_registry"
        ),
        "output_dir": str(output_root),
        "boundary_status": boundary_status,
    }


def _content_spine_input_candidate(
    *,
    dry_run_packet: dict[str, Any],
    carried_defaults: dict[str, Any],
    boundary_status: dict[str, Any],
) -> dict[str, Any]:
    topic = dry_run_packet["topic_capsule"]
    source_boundary = dry_run_packet["source_boundary"]
    yukkuri_profile = dry_run_packet["yukkuri_profile"]
    thumbnail_profile = dry_run_packet["thumbnail_profile"]
    carried = carried_defaults.get("carried_template_defaults", {})
    return {
        "schema_version": "content_spine_source_manifest.v1",
        "source_manifest_id": "factory_seed_dry_run_content_spine_candidate_002",
        "source_type": "offline_synthetic_fixture",
        "fixture_note": "Dry-run candidate only; proves seed initialization and is not a real episode input.",
        "boundary_status": boundary_status,
        "candidates": [
            {
                "candidate_id": topic["candidate_id"],
                "title": topic["title"],
                "candidate_score": topic["candidate_score"],
                "score_rationale": topic["score_rationale"],
                "channel_angle": topic["channel_angle"],
                "source_name": source_boundary["source_name"],
                "source_url_or_placeholder": source_boundary["source_url_or_placeholder"],
                "published_at_or_placeholder": source_boundary["published_at_or_placeholder"],
                "freshness_status": source_boundary["freshness_status"],
                "rights_status": source_boundary["rights_status"],
                "attribution_note": source_boundary["attribution_note"],
                "excluded_claims": source_boundary["excluded_claims"],
                "production_status": source_boundary["production_status"],
                "explainer_role": yukkuri_profile.get("explainer_role"),
                "listener_role": yukkuri_profile.get("listener_role"),
                "hook": yukkuri_profile["hook"],
                "why_it_matters": yukkuri_profile["why_it_matters"],
                "beat_outline": yukkuri_profile["beat_outline"],
                "recommended_tone": yukkuri_profile["recommended_tone"],
                "glossary_terms": yukkuri_profile["glossary_terms"],
                "likely_audience": yukkuri_profile["likely_audience"],
                "channel_fit": yukkuri_profile["channel_fit"],
                "title_hook": thumbnail_profile["title_hook"],
                "short_text_candidates": thumbnail_profile["short_text_candidates"],
                "visual_motif": thumbnail_profile["visual_motif"],
                "forbidden_avoid_claims": thumbnail_profile["forbidden_avoid_claims"],
                "source_rights_caution": thumbnail_profile["source_rights_caution"],
                "designer_note": thumbnail_profile["designer_note"],
                "csv_header_mode": carried.get("csv_header_mode"),
                "section_count": carried.get("section_count"),
            }
        ],
    }


def _episode_seed(
    *,
    artifact_id: str,
    episode_id: str,
    output_root: Path,
    registry_root: Path,
    registry_manifest: dict[str, Any],
    seed_sample: dict[str, Any],
    dry_run_packet: dict[str, Any],
    required_real_inputs: dict[str, Any],
    carried_defaults: dict[str, Any],
    planned_steps: dict[str, Any],
    boundary_status: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "factory_seed_episode_seed.v1",
        "seed_id": f"{episode_id}_record",
        "episode_id": episode_id,
        "artifact_id": artifact_id,
        "status": "dry_run",
        "source_reality": "sample_fixture_not_real",
        "derived_from_registry_artifact_id": registry_manifest.get("artifact_id"),
        "derived_from_seed_sample_id": seed_sample.get("seed_id"),
        "template_registry_dir": str(registry_root),
        "output_dir": str(output_root),
        "source_template_files": seed_sample.get("source_template_files", []),
        "inherited_defaults": carried_defaults.get("carried_template_defaults", {}),
        "synthetic_dry_run_placeholders": {
            "topic_source_packet": "dry_run_topic_source_packet.json",
            "candidate_id": dry_run_packet.get("topic_capsule", {}).get("candidate_id"),
            "source_url_or_placeholder": dry_run_packet.get("source_boundary", {}).get("source_url_or_placeholder"),
            "placeholder_status": "sample_fixture_not_real",
        },
        "required_real_inputs": {
            key: {
                "state": value.get("state"),
                "value": value.get("value"),
                "accepted_shape": value.get("accepted_shape"),
            }
            for key, value in required_real_inputs.get("required_real_inputs", {}).items()
            if isinstance(value, dict)
        },
        "planned_pipeline_steps_path": "planned_pipeline_steps.json",
        "planned_pipeline_step_ids": [
            item.get("step_id")
            for item in planned_steps.get("steps", [])
            if isinstance(item, dict)
        ],
        "content_spine_input_candidate_path": "content_spine_input_candidate.json",
        "boundary_status": boundary_status,
        "closed_gates": list(CLOSED_GATES),
        "not_created_by_seed_instantiation": [
            "real topic/source packet",
            "real transcript",
            "YMM4 GUI import",
            "YMM4 render",
            "production .ymmp",
            "rendered video",
            "final thumbnail image",
            "public upload or visibility change",
        ],
    }


def _init_readiness_summary(
    *,
    artifact_id: str,
    episode_id: str,
    registry_root: Path,
    output_root: Path,
    registry_manifest: dict[str, Any],
    registry_readiness: dict[str, Any],
    required_real_inputs: dict[str, Any],
    boundary_status: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "factory_seed_init_readiness_summary.v1",
        "artifact_id": artifact_id,
        "episode_id": episode_id,
        "source_registry_dir": str(registry_root),
        "output_dir": str(output_root),
        "derived_from_registry_artifact_id": registry_manifest.get("artifact_id"),
        "registry_deterministic_generation_path": registry_readiness.get("deterministic_generation_path"),
        "deterministic_seed_instantiation_path": True,
        "required_for_real_episode": list(required_real_inputs.get("required_real_inputs", {}).keys()),
        "boundary_status": boundary_status,
        "closed_gates": list(CLOSED_GATES),
        "init_status": {
            "can_initialize_seed_from_registry_offline": True,
            "used_manual_copy_of_original_pilot": False,
            "can_use_synthetic_packet_for_dry_run": True,
            "can_run_downstream_pipeline_now": False,
            "can_claim_real_source_readiness": False,
            "can_claim_production_readiness": False,
            "can_launch_yymm4": False,
            "can_publish": False,
        },
        "next_safe_local_action": (
            "Review episode_seed.json and required_real_inputs.json; replace the dry-run source packet "
            "with a real reviewed local topic/source packet before any downstream content-spine, transcript, "
            "YMM4, rights, render, production, or public work."
        ),
    }


def _manifest_payload(
    *,
    artifact_id: str,
    episode_id: str,
    registry_root: Path,
    output_root: Path,
    registry_manifest: dict[str, Any],
    boundary_status: dict[str, Any],
    init_summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "factory_seed_instantiation_manifest.v1",
        "artifact_id": artifact_id,
        "episode_id": episode_id,
        "artifact_kind": "factory-seed-instantiation-dry-run",
        "status": "dry_run_seed_instantiated",
        "source_registry_dir": str(registry_root),
        "derived_from_registry_artifact_id": registry_manifest.get("artifact_id"),
        "output_dir": str(output_root),
        "files": {name: str(output_root / name) for name in REQUIRED_FACTORY_SEED_INSTANTIATION_FILES},
        "boundaries": {
            "local_offline_review_only": True,
            "dry_run": True,
            "sample_fixture_not_real": True,
            "no_manual_copy_of_original_pilot": True,
            "no_live_fetch": True,
            "no_external_media_download": True,
            "no_embedded_external_images": True,
            "no_youtube_publication": True,
            "no_oauth_or_paid_api": True,
            "no_rights_or_legal_acceptance": True,
            "no_yymm4_gui_launch_or_import_or_render": True,
            "no_production_ymmp_generation": True,
            "no_audio_generation": True,
            "public_upload_closed": True,
            "yymm4_render_closed": True,
        },
        "boundary_status": boundary_status,
        "next_safe_local_action": init_summary.get("next_safe_local_action"),
    }


def _source_artifact_index(registry_root: Path, output_root: Path, repo_root: Path) -> dict[str, Any]:
    source_inputs = []
    for name in REQUIRED_EPISODE_FACTORY_TEMPLATE_REGISTRY_FILES:
        path = registry_root / name
        payload = _load_json_if_present(path) if path.suffix.lower() == ".json" else {}
        source_inputs.append({
            "id": name,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": "ready" if path.exists() else "missing",
            "schema_version": payload.get("schema_version") if isinstance(payload, dict) else None,
        })
    generated_outputs = []
    for name in REQUIRED_FACTORY_SEED_INSTANTIATION_FILES:
        path = output_root / name
        generated_outputs.append({
            "id": name,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": "ready" if path.exists() else "missing",
        })
    return {
        "schema_version": "factory_seed_source_artifact_index.v1",
        "source_registry_dir": str(registry_root),
        "generated_output_dir": str(output_root),
        "source_inputs": source_inputs,
        "generated_outputs": generated_outputs,
        "artifact_counts": {
            "source_total": len(source_inputs),
            "source_present": sum(1 for item in source_inputs if item["exists"]),
            "generated_total": len(generated_outputs),
            "generated_present": sum(1 for item in generated_outputs if item["exists"]),
        },
    }


def _render_review_checklist(summary: dict[str, Any]) -> str:
    return "\n".join([
        "# Factory Seed Instantiation Dry-Run Review Checklist",
        "",
        "- Confirm `seed_instantiation_manifest.json` points to the existing template registry.",
        "- Confirm `episode_seed.json` separates inherited defaults, synthetic dry-run placeholders, and required real inputs.",
        "- Confirm `dry_run_topic_source_packet.json` is marked `dry_run` and `sample_fixture_not_real`.",
        "- Confirm `required_real_inputs.json` has null values for real topic/source, transcript, rights, and human decision fields.",
        "- Confirm `content_spine_input_candidate.json` is a candidate only and was not run downstream.",
        "- Confirm rights, public upload, YMM4 render, production `.ymmp`, OAuth/payment/API, external media, and publication gates remain closed.",
        "",
        "## Next Safe Local Action",
        "",
        summary["next_safe_local_action"],
        "",
    ])


def _render_limitations(summary: dict[str, Any]) -> str:
    lines = [
        "# Factory Seed Instantiation Dry-Run Limitations",
        "",
        "This package proves local seed initialization from the template registry only.",
        "",
        "Not performed:",
        "",
    ]
    for gate in summary.get("closed_gates", []):
        lines.append(f"- {gate}")
    lines.extend([
        "- real topic/source packet intake",
        "- real transcript or script generation",
        "- downstream content-spine package execution",
        "- final transcript, timing, source, rights, legal, or public-ready acceptance",
        "",
        "The dry-run packet is synthetic fixture material and must not be treated as production content.",
        "",
    ])
    return "\n".join(lines)


def _check_boundary_flags(boundary_status: dict[str, Any], failed_checks: list[str], *, prefix: str = "") -> None:
    if boundary_status.get("dry_run") is not True:
        failed_checks.append(f"{prefix}dry_run_not_marked")
    if boundary_status.get("sample_fixture_not_real") is not True:
        failed_checks.append(f"{prefix}sample_fixture_not_real_not_marked")
    if boundary_status.get("rights_boundary") != "sample_only_no_publication":
        failed_checks.append(f"{prefix}rights_boundary_not_preserved")
    if boundary_status.get("public_upload_closed") is not True:
        failed_checks.append(f"{prefix}public_upload_closed_not_marked")
    if boundary_status.get("yymm4_render_closed") is not True:
        failed_checks.append(f"{prefix}yymm4_render_closed_not_marked")
    if boundary_status.get("public_upload_status") != "public_upload_closed":
        failed_checks.append(f"{prefix}public_upload_status_not_closed")
    if boundary_status.get("yymm4_render_status") != "yymm4_render_closed":
        failed_checks.append(f"{prefix}yymm4_render_status_not_closed")


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
