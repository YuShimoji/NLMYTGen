"""Build a content spine dry-run package from a factory seed package.

This is the first downstream planning step after seed instantiation. It
consumes the second episode dry-run seed package and reuses the existing
content spine builder with the seed's content_spine_input_candidate.json.
No live fetch, transcript generation, YMM4 action, render, external media, or
publication work is performed.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.pipeline.content_planning_spine import (
    REQUIRED_PACKAGE_FILES as CONTENT_SPINE_PACKAGE_FILES,
    build_content_spine_package,
)

DEFAULT_OUTPUT_DIRNAME = "yukkuri_newsroom_content_spine_002"
DEFAULT_ARTIFACT_ID = "yukkuri_newsroom_content_spine_002_dry_run"

SOURCE_SEED_FILES = (
    "seed_instantiation_manifest.json",
    "episode_seed.json",
    "dry_run_topic_source_packet.json",
    "required_real_inputs.json",
    "carried_template_defaults.json",
    "planned_pipeline_steps.json",
    "boundary_status.json",
    "init_readiness_summary.json",
    "content_spine_input_candidate.json",
    "validation_readback.json",
)

SEED_TO_CONTENT_SPINE_FILES = (
    "content_spine_dry_run_manifest.json",
    "source_seed_reference.json",
    "source_artifact_index.json",
    "validation_readback.json",
)

REQUIRED_FACTORY_SEED_CONTENT_SPINE_FILES = (
    *CONTENT_SPINE_PACKAGE_FILES,
    *SEED_TO_CONTENT_SPINE_FILES,
)

JSON_SEED_TO_CONTENT_SPINE_FILES = tuple(
    name
    for name in REQUIRED_FACTORY_SEED_CONTENT_SPINE_FILES
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


def build_content_spine_from_factory_seed(
    *,
    seed_package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a second content spine dry-run package from a seed package."""
    seed_root = Path(seed_package_dir)
    if not seed_root.exists():
        raise FileNotFoundError(seed_root)
    output_root = Path(output_dir) if output_dir else _default_output_dir(seed_root)
    output_root.mkdir(parents=True, exist_ok=True)

    repo_root = _find_repo_root(seed_root)
    seed = _load_seed_payloads(seed_root)
    content_spine_source = seed_root / "content_spine_input_candidate.json"

    content_readback = build_content_spine_package(
        source_path=content_spine_source,
        output_dir=output_root,
        artifact_id=artifact_id,
    )
    _normalize_text_files(output_root, CONTENT_SPINE_PACKAGE_FILES)

    boundary_status = _boundary_status(seed)
    source_seed_reference = _source_seed_reference(
        seed_root=seed_root,
        output_root=output_root,
        artifact_id=artifact_id,
        seed=seed,
        content_readback=content_readback,
        boundary_status=boundary_status,
    )
    manifest = _manifest_payload(
        seed_root=seed_root,
        output_root=output_root,
        artifact_id=artifact_id,
        seed=seed,
        content_readback=content_readback,
        boundary_status=boundary_status,
    )

    _write_json(output_root / "content_spine_dry_run_manifest.json", manifest)
    _write_json(output_root / "source_seed_reference.json", source_seed_reference)
    _append_seed_review_sections(output_root, source_seed_reference)
    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(seed_root, output_root, repo_root))

    readback = validate_factory_seed_content_spine(output_root, seed_package_dir=seed_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(seed_root, output_root, repo_root))
    final_readback = validate_factory_seed_content_spine(output_root, seed_package_dir=seed_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_factory_seed_content_spine(
    output_dir: str | Path,
    *,
    seed_package_dir: str | Path | None = None,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate seed-origin readback, content spine output, and closed gates."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_FACTORY_SEED_CONTENT_SPINE_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    json_payloads = {
        name.removesuffix(".json"): _load_json_if_present(files[name])
        for name in JSON_SEED_TO_CONTENT_SPINE_FILES
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["content_spine_dry_run_manifest"]
    source_seed = json_payloads["source_seed_reference"]
    topic_candidates = json_payloads["topic_candidates"]
    dashboard = json_payloads["dashboard_status"]
    content_readback = json_payloads["content_spine_readback"]
    source_index = json_payloads["source_artifact_index"]

    if manifest.get("artifact_kind") != "factory-seed-to-content-spine-dry-run":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "generated":
        failed_checks.append("manifest_status_unexpected")
    if manifest.get("content_spine_readback", {}).get("status") != "passed":
        failed_checks.append("content_spine_readback_not_passed")
    if content_readback.get("status") != "passed":
        failed_checks.append("standard_content_spine_readback_not_passed")

    _check_boundary_flags(manifest.get("boundary_status", {}), failed_checks, prefix="manifest_")
    _check_boundary_flags(source_seed.get("boundary_status", {}), failed_checks, prefix="seed_reference_")

    real_inputs = source_seed.get("required_real_inputs", {})
    for key in ("topic_or_source_packet", "real_transcript", "rights_review", "human_episode_decision"):
        if key not in real_inputs:
            failed_checks.append(f"required_real_input_missing:{key}")
        elif real_inputs.get(key, {}).get("value") is not None:
            failed_checks.append(f"required_real_input_has_value:{key}")

    if not source_seed.get("inherited_template_defaults"):
        failed_checks.append("inherited_template_defaults_missing")
    if not source_seed.get("dry_run_placeholders"):
        failed_checks.append("dry_run_placeholders_missing")
    if source_seed.get("manual_copy_of_original_pilot") is not False:
        failed_checks.append("manual_copy_boundary_missing")

    candidates = topic_candidates.get("candidates", [])
    if not candidates:
        failed_checks.append("topic_candidates_empty")
    else:
        selected = candidates[0]
        boundary = selected.get("source_boundary", {})
        if boundary.get("freshness_status") != "offline_fixture_not_live":
            failed_checks.append("candidate_not_offline_fixture")
        if boundary.get("rights_status") != "sample_only_no_publication":
            failed_checks.append("candidate_rights_boundary_missing")
        if boundary.get("production_status") != "dry_run_only_not_production":
            failed_checks.append("candidate_production_status_unexpected")

    readiness = dashboard.get("readiness", {})
    if readiness.get("episode_package_status") != "local_reviewable":
        failed_checks.append("content_spine_not_local_reviewable")
    if readiness.get("ymm4_readiness") != "planning_ready_csv_ir_not_generated":
        failed_checks.append("ymm4_not_closed_at_content_spine")

    if source_index.get("artifact_counts", {}).get("source_present", 0) < 5:
        failed_checks.append("source_artifact_index_too_sparse")
    if source_index.get("artifact_counts", {}).get("generated_present", 0) < len(REQUIRED_FACTORY_SEED_CONTENT_SPINE_FILES) - 1:
        failed_checks.append("generated_artifact_index_too_sparse")

    if seed_package_dir is not None:
        missing_seed_files = [
            name
            for name in SOURCE_SEED_FILES
            if not (Path(seed_package_dir) / name).exists()
        ]
        failed_checks.extend(f"seed_missing_file:{name}" for name in missing_seed_files)

    combined_text = _combined_text(files.values())
    external_reference_hits = _external_reference_hits(combined_text)
    forbidden_hits = [claim for claim in FORBIDDEN_COMPLETION_CLAIMS if claim in combined_text]
    failed_checks.extend(f"external_reference:{hit}" for hit in external_reference_hits)
    failed_checks.extend(f"forbidden_completion_claim:{claim}" for claim in forbidden_hits)

    return {
        "schema_version": "factory_seed_content_spine_readback.v1",
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
            "seed_input_files_present": not any(item.startswith("seed_missing_file:") for item in failed_checks),
            "standard_content_spine_readback_passed": content_readback.get("status") == "passed",
            "required_real_inputs_separated": all(
                key in real_inputs and real_inputs[key].get("value") is None
                for key in ("topic_or_source_packet", "real_transcript", "rights_review", "human_episode_decision")
            ),
            "inherited_defaults_separated": bool(source_seed.get("inherited_template_defaults")),
            "dry_run_placeholders_marked": bool(source_seed.get("dry_run_placeholders")),
            "dry_run_marked": manifest.get("boundary_status", {}).get("dry_run") is True,
            "sample_fixture_not_real_marked": manifest.get("boundary_status", {}).get("sample_fixture_not_real") is True,
            "no_real_transcript_marked": manifest.get("boundary_status", {}).get("no_real_transcript") is True,
            "rights_boundary_preserved": manifest.get("boundary_status", {}).get("rights_boundary")
            == "sample_only_no_publication",
            "public_upload_closed": manifest.get("boundary_status", {}).get("public_upload_closed") is True,
            "yymm4_render_closed": manifest.get("boundary_status", {}).get("yymm4_render_closed") is True,
            "no_external_references": not external_reference_hits,
            "no_forbidden_completion_claims": not forbidden_hits,
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "source_seed_package_dir": manifest.get("source_seed_package_dir"),
        "selected_candidate_id": manifest.get("selected_candidate_id"),
        "primary_machine_readable": str(root / "content_spine_dry_run_manifest.json"),
        "standard_content_spine_manifest": str(root / "MANIFEST.json"),
        "source_seed_reference_path": str(root / "source_seed_reference.json"),
        "primary_human_review": str(root / "episode_candidate_001.md"),
        "review_checklist": str(root / "review_checklist.md"),
        "next_action": manifest.get("next_safe_local_action"),
    }


def _load_seed_payloads(seed_root: Path) -> dict[str, dict[str, Any]]:
    payloads: dict[str, dict[str, Any]] = {}
    for filename in SOURCE_SEED_FILES:
        path = seed_root / filename
        if not path.exists():
            raise FileNotFoundError(path)
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(payload, dict):
            raise ValueError(f"seed file must contain a JSON object: {path}")
        payloads[filename.removesuffix(".json")] = payload
    return payloads


def _default_output_dir(seed_root: Path) -> Path:
    production_root = seed_root.parent.parent
    return production_root / DEFAULT_OUTPUT_DIRNAME


def _boundary_status(seed: dict[str, dict[str, Any]]) -> dict[str, Any]:
    source_boundary = seed["boundary_status"]
    return {
        **source_boundary,
        "dry_run": True,
        "sample_fixture_not_real": True,
        "rights_boundary": "sample_only_no_publication",
        "public_upload_closed": True,
        "yymm4_render_closed": True,
        "no_real_transcript": True,
        "seed_to_content_spine_status": "generated_from_factory_seed",
        "content_spine_generation_status": "local_offline_dry_run",
        "real_transcript_status": "not_run_required_before_production",
        "public_upload_status": "public_upload_closed",
        "yymm4_render_status": "yymm4_render_closed",
        "yymm4_import_status": "not_run",
        "external_network_status": "closed",
        "oauth_status": "closed",
        "payment_status": "closed",
        "production_status": "blocked_by_true_gate",
    }


def _source_seed_reference(
    *,
    seed_root: Path,
    output_root: Path,
    artifact_id: str,
    seed: dict[str, dict[str, Any]],
    content_readback: dict[str, Any],
    boundary_status: dict[str, Any],
) -> dict[str, Any]:
    episode_seed = seed["episode_seed"]
    required_inputs = seed["required_real_inputs"].get("required_real_inputs", {})
    carried_defaults = seed["carried_template_defaults"].get("carried_template_defaults", {})
    dry_run_packet = seed["dry_run_topic_source_packet"]
    source_candidate = seed["content_spine_input_candidate"].get("candidates", [{}])[0]
    return {
        "schema_version": "factory_seed_content_spine_source_reference.v1",
        "artifact_id": artifact_id,
        "source_seed_package_dir": str(seed_root),
        "content_spine_output_dir": str(output_root),
        "derived_from_seed_instantiation_artifact_id": seed["seed_instantiation_manifest"].get("artifact_id"),
        "derived_from_episode_seed_id": episode_seed.get("seed_id"),
        "derived_from_registry_artifact_id": episode_seed.get("derived_from_registry_artifact_id"),
        "manual_copy_of_original_pilot": False,
        "content_spine_source_file": str(seed_root / "content_spine_input_candidate.json"),
        "source_candidate_id": source_candidate.get("candidate_id"),
        "source_candidate_title": source_candidate.get("title"),
        "inherited_template_defaults": carried_defaults,
        "dry_run_placeholders": {
            "episode_seed_placeholders": episode_seed.get("synthetic_dry_run_placeholders", {}),
            "topic_source_packet": {
                "packet_id": dry_run_packet.get("packet_id"),
                "status": dry_run_packet.get("status"),
                "source_reality": dry_run_packet.get("source_reality"),
                "source_boundary": dry_run_packet.get("source_boundary", {}),
            },
        },
        "required_real_inputs": {
            key: {
                "state": value.get("state"),
                "value": value.get("value"),
                "accepted_shape": value.get("accepted_shape"),
            }
            for key, value in required_inputs.items()
            if isinstance(value, dict)
        },
        "generated_content_spine_outputs": {
            "standard_manifest": str(output_root / "MANIFEST.json"),
            "topic_candidates": str(output_root / "topic_candidates.json"),
            "episode_candidate": str(output_root / "episode_candidate_001.md"),
            "thumbnail_brief": str(output_root / "thumbnail_brief_001.md"),
            "dashboard_status": str(output_root / "dashboard_status.json"),
            "standard_readback": str(output_root / "content_spine_readback.json"),
        },
        "content_spine_readback": {
            "status": content_readback.get("status"),
            "selected_candidate_id": content_readback.get("selected_candidate_id"),
            "next_action": content_readback.get("next_action"),
        },
        "boundary_status": boundary_status,
    }


def _manifest_payload(
    *,
    seed_root: Path,
    output_root: Path,
    artifact_id: str,
    seed: dict[str, dict[str, Any]],
    content_readback: dict[str, Any],
    boundary_status: dict[str, Any],
) -> dict[str, Any]:
    source_candidate = seed["content_spine_input_candidate"].get("candidates", [{}])[0]
    return {
        "schema_version": "factory_seed_content_spine_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "factory-seed-to-content-spine-dry-run",
        "status": "generated",
        "source_seed_package_dir": str(seed_root),
        "output_dir": str(output_root),
        "selected_candidate_id": source_candidate.get("candidate_id"),
        "selected_title": source_candidate.get("title"),
        "input_source": str(seed_root / "content_spine_input_candidate.json"),
        "files": {name: str(output_root / name) for name in REQUIRED_FACTORY_SEED_CONTENT_SPINE_FILES},
        "content_spine_readback": {
            "status": content_readback.get("status"),
            "selected_candidate_id": content_readback.get("selected_candidate_id"),
            "standard_readback": str(output_root / "content_spine_readback.json"),
        },
        "boundaries": {
            "local_offline_review_only": True,
            "dry_run": True,
            "sample_fixture_not_real": True,
            "no_manual_copy_of_original_pilot": True,
            "no_real_transcript": True,
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
        "next_safe_local_action": (
            "Review the dry-run content spine package and source_seed_reference.json; replace the seed dry-run "
            "source packet with a real reviewed local topic/source packet before real transcript, IR bridge, "
            "YMM4, rights, render, production, or public work."
        ),
    }


def _append_seed_review_sections(output_root: Path, source_seed_reference: dict[str, Any]) -> None:
    checklist_path = output_root / "review_checklist.md"
    limitations_path = output_root / "limitations.md"
    checklist = checklist_path.read_text(encoding="utf-8")
    checklist += "\n".join([
        "",
        "## Factory Seed Dry-Run Checks",
        "",
        "- Confirm this content spine was generated from `source_seed_reference.json`, not by copying the original pilot.",
        "- Confirm inherited defaults, dry-run placeholders, and required real inputs remain separated.",
        "- Confirm no real transcript, YMM4 import/render, production `.ymmp`, rights/public-ready acceptance, or upload is implied.",
        "",
    ])
    limitations = limitations_path.read_text(encoding="utf-8")
    limitations += "\n".join([
        "",
        "## Factory Seed Dry-Run Boundary",
        "",
        f"- source_seed_package_dir: {source_seed_reference['source_seed_package_dir']}",
        "- This package uses synthetic dry-run seed input only.",
        "- Required real inputs are still null in `source_seed_reference.json`.",
        "- It does not run transcript substitution, IR bridge, YMM4 import/render, production `.ymmp`, external media, or publication.",
        "",
    ])
    checklist_path.write_text(checklist, encoding="utf-8", newline="\n")
    limitations_path.write_text(limitations, encoding="utf-8", newline="\n")


def _source_artifact_index(seed_root: Path, output_root: Path, repo_root: Path) -> dict[str, Any]:
    source_inputs = []
    for name in SOURCE_SEED_FILES:
        path = seed_root / name
        payload = _load_json_if_present(path)
        source_inputs.append({
            "id": name,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": "ready" if path.exists() else "missing",
            "schema_version": payload.get("schema_version") if isinstance(payload, dict) else None,
        })
    generated_outputs = []
    for name in REQUIRED_FACTORY_SEED_CONTENT_SPINE_FILES:
        path = output_root / name
        generated_outputs.append({
            "id": name,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": "ready" if path.exists() else "missing",
        })
    return {
        "schema_version": "factory_seed_content_spine_source_artifact_index.v1",
        "source_seed_package_dir": str(seed_root),
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


def _check_boundary_flags(boundary_status: dict[str, Any], failed_checks: list[str], *, prefix: str = "") -> None:
    if boundary_status.get("dry_run") is not True:
        failed_checks.append(f"{prefix}dry_run_not_marked")
    if boundary_status.get("sample_fixture_not_real") is not True:
        failed_checks.append(f"{prefix}sample_fixture_not_real_not_marked")
    if boundary_status.get("no_real_transcript") is not True:
        failed_checks.append(f"{prefix}no_real_transcript_not_marked")
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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def _normalize_text_files(root: Path, filenames: tuple[str, ...]) -> None:
    for filename in filenames:
        path = root / filename
        if path.exists():
            path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
