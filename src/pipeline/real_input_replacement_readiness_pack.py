"""Real input replacement readiness package for episode 002."""

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

DEFAULT_OUTPUT_DIRNAME = "real_input_replacement_readiness_pack"
DEFAULT_ARTIFACT_ID = "episode_002_verified_real_input_replacement_readiness_pack_v1"
EPISODE_ID = "yukkuri_newsroom_content_spine_002"

YMM4_IMPORT_READY_DIRNAME = "ymm4_import_ready_pack"
REAL_INPUT_INTAKE_DIRNAME = "real_input_intake_readiness"
LOCAL_EDIT_DIRNAME = "local_edit_slice_execution_pack"

REQUIRED_REAL_INPUT_REPLACEMENT_FILES = (
    "real_input_replacement_manifest.json",
    "replacement_input_requirements.json",
    "source_artifact_index.json",
    "real_input_replacement_preview.html",
    "real_input_replacement_contract.md",
    "validation_readback.json",
    "input_dropzone/README.md",
    "README_REAL_INPUT_REPLACEMENT_READINESS.md",
    "limitations.md",
)

REQUIRED_INPUT_IDS = (
    "local_source_audio_video_or_document_path",
    "local_transcript_or_generation_receipt_path",
    "source_provenance_and_rights_note",
    "stable_file_identity",
    "episode_002_cue_map_alignment",
)

CLOSED_GATE_FLAGS = (
    "actual_real_input_replaced",
    "real_input_replaced",
    "live_fetch_performed",
    "external_media_downloaded",
    "actual_ymm4_imported",
    "actual_yymm4_import",
    "rendered_video_created",
    "yymm4_rendered",
    "ymmp_file_created",
    "production_ymmp_written",
    "rights_approved",
    "rights_accepted",
    "public_ready",
    "final_thumbnail_approval",
    "youtube_uploaded",
)


def build_real_input_replacement_readiness_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build the verified local input replacement readiness package."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "input_dropzone").mkdir(parents=True, exist_ok=True)
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
    requirements = _replacement_input_requirements(state)
    source_index = _source_artifact_index(state)
    manifest = _manifest(state, requirements, output_root, repo_root)

    _write_json(output_root / "real_input_replacement_manifest.json", manifest)
    _write_json(output_root / "replacement_input_requirements.json", requirements)
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_text(output_root / "real_input_replacement_preview.html", _render_html(state, manifest, requirements))
    _write_text(output_root / "real_input_replacement_contract.md", _render_contract(state, requirements))
    _write_text(output_root / "input_dropzone" / "README.md", _render_dropzone_readme(state))
    _write_text(output_root / "README_REAL_INPUT_REPLACEMENT_READINESS.md", _render_readme(state, manifest, requirements))
    _write_text(output_root / "limitations.md", _render_limitations())

    readback = validate_real_input_replacement_readiness_pack(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_real_input_replacement_readiness_pack(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_real_input_replacement_readiness_pack(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate a generated real-input replacement readiness package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_REAL_INPUT_REPLACEMENT_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["real_input_replacement_manifest.json"])
    requirements = _load_json_if_present(files["replacement_input_requirements.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])
    json_payloads = {
        "manifest": manifest,
        "requirements": requirements,
        "source_index": source_index,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = _dict(json_payloads["manifest"])
    requirements = _dict(json_payloads["requirements"])
    source_index = _dict(json_payloads["source_index"])
    html_text = files["real_input_replacement_preview.html"].read_text(encoding="utf-8") if files["real_input_replacement_preview.html"].exists() else ""
    contract_text = files["real_input_replacement_contract.md"].read_text(encoding="utf-8") if files["real_input_replacement_contract.md"].exists() else ""
    dropzone_text = files["input_dropzone/README.md"].read_text(encoding="utf-8") if files["input_dropzone/README.md"].exists() else ""
    limitations_text = files["limitations.md"].read_text(encoding="utf-8") if files["limitations.md"].exists() else ""

    required_inputs = [row for row in _list(requirements.get("required_local_inputs")) if isinstance(row, dict)]
    required_ids = {str(row.get("input_id")) for row in required_inputs}
    candidate_count = _candidate_input_count(root)
    closed_gate_flags = _dict(manifest.get("closed_gate_flags"))
    operator_check_count = _numbered_check_count(contract_text)

    if manifest.get("artifact_kind") != "episode-real-input-replacement-readiness-pack":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("episode_id") != EPISODE_ID:
        failed_checks.append("manifest_episode_id_mismatch")
    if manifest.get("package_type") != "real_input_replacement_readiness":
        failed_checks.append("manifest_package_type_mismatch")
    if manifest.get("status") != "ready_for_verified_local_input_not_replaced":
        failed_checks.append("manifest_status_mismatch")
    if manifest.get("source_episode_pack_reference") != "production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack":
        failed_checks.append("source_episode_pack_reference_mismatch")
    if manifest.get("placeholder_state") != "sample_diagnostic_only_no_verified_local_input":
        failed_checks.append("placeholder_state_mismatch")
    if manifest.get("required_local_input_count") != len(REQUIRED_INPUT_IDS):
        failed_checks.append("required_local_input_count_mismatch")
    if manifest.get("candidate_input_count") != candidate_count:
        failed_checks.append("candidate_input_count_mismatch")
    if candidate_count != 0:
        failed_checks.append("candidate_input_files_present_in_placeholder_dropzone")
    for input_id in REQUIRED_INPUT_IDS:
        if input_id not in required_ids:
            failed_checks.append(f"required_input_missing:{input_id}")
    for flag in CLOSED_GATE_FLAGS:
        if manifest.get(flag) is not False:
            failed_checks.append(f"manifest_gate_not_false:{flag}")
        if closed_gate_flags.get(flag) is not False:
            failed_checks.append(f"closed_gate_not_false:{flag}")
    if manifest.get("next_gate") != "provide_verified_local_source_and_transcript":
        failed_checks.append("next_gate_mismatch")
    if source_index.get("ymm4_import_ready_pack_read_only") is not True:
        failed_checks.append("ymm4_import_ready_pack_not_read_only")
    if source_index.get("real_input_intake_pack_read_only") is not True:
        failed_checks.append("real_input_intake_pack_not_read_only")
    if 'data-real-input-replacement-readiness="true"' not in html_text:
        failed_checks.append("html_marker_missing")
    for marker in (
        'data-region="pipeline-runway"',
        'data-region="input-matrix"',
        'data-region="material-boundary"',
        'data-region="closed-gates"',
        'data-region="next-artifact"',
    ):
        if marker not in html_text:
            failed_checks.append(f"html_region_missing:{marker}")
    if '<html lang="ja"' not in html_text:
        failed_checks.append("html_not_japanese_lang")
    if "実入力置換準備" not in html_text or "未実行" not in html_text:
        failed_checks.append("html_japanese_operator_copy_missing")
    if "card-grid" in html_text or 'data-region="card-grid"' in html_text:
        failed_checks.append("html_card_grid_marker_found")
    if operator_check_count > 5:
        failed_checks.append("operator_contract_too_many_checks")
    if operator_check_count < 1:
        failed_checks.append("operator_contract_checks_missing")
    if "source audio/video/document path" not in contract_text:
        failed_checks.append("contract_source_path_requirement_missing")
    if "transcript path" not in contract_text:
        failed_checks.append("contract_transcript_requirement_missing")
    if "hash" not in contract_text.lower() and "stable identity" not in contract_text.lower():
        failed_checks.append("contract_stable_identity_missing")
    if "Episode 002 cue map" not in contract_text:
        failed_checks.append("contract_cue_map_requirement_missing")
    if "placeholder folder only" not in dropzone_text:
        failed_checks.append("dropzone_placeholder_boundary_missing")
    if "Do not place media files in this commit" not in dropzone_text:
        failed_checks.append("dropzone_media_boundary_missing")
    if "Do not launch YMM4" not in limitations_text:
        failed_checks.append("limitations_yymm4_stop_missing")

    visible_files = [path for name, path in files.items() if path.exists() and name != "validation_readback.json"]
    external_refs = _external_refs_in_files(visible_files)
    forbidden_claims = _forbidden_true_claims(root)
    temporary_hits = _temporary_copy_hits(visible_files)
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_claims)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    status = "passed" if not failed_checks else "failed"
    checks = {
        "all_required_files_present": all(
            path.exists() for name, path in files.items() if name != "validation_readback.json" or require_readback
        ),
        "json_loads": all(isinstance(payload, dict) for payload in json_payloads.values()),
        "html_preview_exists": files["real_input_replacement_preview.html"].exists(),
        "operator_contract_exists": files["real_input_replacement_contract.md"].exists(),
        "input_dropzone_readme_exists": files["input_dropzone/README.md"].exists(),
        "japanese_first_surface": '<html lang="ja"' in html_text and "実入力置換準備" in html_text,
        "primary_card_grid_absent": "card-grid" not in html_text,
        "required_local_input_count": len(required_inputs),
        "candidate_input_count": candidate_count,
        "closed_gate_flags": closed_gate_flags,
        "external_dependency_status": "none_found" if not external_refs else external_refs,
        "forbidden_true_claims_absent": not forbidden_claims,
        "temporary_copy_absent": not temporary_hits,
    }
    return {
        "schema_version": "real_input_replacement_validation_readback.v1",
        "status": status,
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "episode_id": manifest.get("episode_id"),
        "package_type": manifest.get("package_type"),
        "source_episode_pack_reference": manifest.get("source_episode_pack_reference"),
        "placeholder_state": manifest.get("placeholder_state"),
        "required_local_input_count": manifest.get("required_local_input_count"),
        "candidate_input_count": candidate_count,
        "actual_real_input_replaced": manifest.get("actual_real_input_replaced"),
        "live_fetch_performed": manifest.get("live_fetch_performed"),
        "external_media_downloaded": manifest.get("external_media_downloaded"),
        "actual_ymm4_imported": manifest.get("actual_ymm4_imported"),
        "rendered_video_created": manifest.get("rendered_video_created"),
        "ymmp_file_created": manifest.get("ymmp_file_created"),
        "rights_approved": manifest.get("rights_approved"),
        "public_ready": manifest.get("public_ready"),
        "next_gate": manifest.get("next_gate"),
        "primary_review_file": str(root / "real_input_replacement_preview.html"),
        "primary_human_review": str(root / "real_input_replacement_preview.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "full_pytest_run": False,
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{(root / "real_input_replacement_preview.html").resolve()}"',
        "access_state": "verified_present" if (root / "real_input_replacement_preview.html").exists() else "missing",
    }


def _input_paths(source_root: Path) -> dict[str, Path]:
    ymm4_root = source_root / YMM4_IMPORT_READY_DIRNAME
    intake_root = source_root / REAL_INPUT_INTAKE_DIRNAME
    local_edit_root = source_root / LOCAL_EDIT_DIRNAME
    return {
        "ymm4_root": ymm4_root,
        "ymm4_validation": ymm4_root / "validation_readback.json",
        "ymm4_cue_map": ymm4_root / "edit_slice_to_ymm4_cue_map.json",
        "ymm4_manifest": ymm4_root / "ymm4_import_ready_manifest.json",
        "intake_root": intake_root,
        "intake_manifest": intake_root / "real_input_intake_manifest.json",
        "intake_contract_schema": intake_root / "source_transcript_contract.schema.json",
        "intake_validation": intake_root / "validation_readback.json",
        "local_edit_root": local_edit_root,
        "local_edit_validation": local_edit_root / "validation_readback.json",
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "ymm4_validation": _load_json_if_present(paths["ymm4_validation"]),
        "ymm4_cue_map": _load_json_if_present(paths["ymm4_cue_map"]),
        "ymm4_manifest": _load_json_if_present(paths["ymm4_manifest"]),
        "intake_manifest": _load_json_if_present(paths["intake_manifest"]),
        "intake_contract_schema": _load_json_if_present(paths["intake_contract_schema"]),
        "intake_validation": _load_json_if_present(paths["intake_validation"]),
        "local_edit_validation": _load_json_if_present(paths["local_edit_validation"]),
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
    cue_map = _dict(payloads.get("ymm4_cue_map"))
    intake_manifest = _dict(payloads.get("intake_manifest"))
    ymm4_validation = _dict(payloads.get("ymm4_validation"))
    return {
        "schema_version": "real_input_replacement_readiness_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-real-input-replacement-readiness-pack",
        "episode_id": EPISODE_ID,
        "package_type": "real_input_replacement_readiness",
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "paths": {name: _relpath(path, repo_root) for name, path in paths.items()},
        "cue_count": cue_map.get("cue_count") or 0,
        "scene_count": cue_map.get("scene_count") or 0,
        "queue_count": _dict(payloads.get("ymm4_manifest")).get("queue_count"),
        "intake_contract_status": intake_manifest.get("input_contract_status") or "unknown",
        "source_pack_status": ymm4_validation.get("status") or "unknown",
        "source_episode_pack_reference": _relpath(paths["ymm4_root"], repo_root),
        "source_episode_pack_validation": _relpath(paths["ymm4_validation"], repo_root),
        "source_cue_map_reference": _relpath(paths["ymm4_cue_map"], repo_root),
        "placeholder_state": "sample_diagnostic_only_no_verified_local_input",
        "primary_human_review": _relpath(output_root / "real_input_replacement_preview.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_gate": "provide_verified_local_source_and_transcript",
        "next_artifact_expected": "validated_local_input_receipt_for_episode_002",
    }


def _replacement_input_requirements(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "real_input_replacement_requirements.v1",
        "artifact_id": state.get("artifact_id"),
        "episode_id": EPISODE_ID,
        "status": "requirements_ready_no_candidate_input",
        "placeholder_state": state.get("placeholder_state"),
        "required_local_inputs": [
            {
                "input_id": "local_source_audio_video_or_document_path",
                "label_ja": "元資料ファイル",
                "required": True,
                "expected_value": "source audio/video/document path",
                "accepted_material_types": ["local audio", "local video", "local document", "local notes"],
                "forbidden_material_types": ["live URL only", "worker-downloaded media", "untracked external asset"],
                "stable_identity_expectation": "path plus hash, file size, or timestamp note",
                "episode_002_relation": "source for S1-S3 narrative and citation placeholders",
            },
            {
                "input_id": "local_transcript_or_generation_receipt_path",
                "label_ja": "文字起こし",
                "required": True,
                "expected_value": "transcript path or transcript generation receipt",
                "accepted_material_types": ["speaker-labeled text", "plain transcript", "CSV transcript", "JSON segments", "local generation receipt"],
                "forbidden_material_types": ["unverified generated text", "remote-only transcript"],
                "stable_identity_expectation": "path plus generation date or hash when available",
                "episode_002_relation": "maps to csv_row_1 through csv_row_9 before replacement",
            },
            {
                "input_id": "source_provenance_and_rights_note",
                "label_ja": "由来と権利メモ",
                "required": True,
                "expected_value": "source provenance/rights note",
                "accepted_material_types": ["local review note", "operator provenance memo"],
                "forbidden_material_types": ["public-ready approval", "legal acceptance claim"],
                "stable_identity_expectation": "reviewer name/date or equivalent local receipt",
                "episode_002_relation": "keeps citation/thumbnail/public gates separated from replacement",
            },
            {
                "input_id": "stable_file_identity",
                "label_ja": "安定識別子",
                "required": True,
                "expected_value": "file hash or stable identity expectation",
                "accepted_material_types": ["sha256", "file size plus modified time", "local export receipt"],
                "forbidden_material_types": ["only a title", "only a URL"],
                "stable_identity_expectation": "enough to detect file drift before rerun",
                "episode_002_relation": "prevents sample/real boundary drift during replacement",
            },
            {
                "input_id": "episode_002_cue_map_alignment",
                "label_ja": "cue対応",
                "required": True,
                "expected_value": "expected relation to Episode 002 cue map",
                "accepted_material_types": ["S1-S3 mapping note", "csv_row_1-9 mapping note", "explicit no-timestamp explanation"],
                "forbidden_material_types": ["replacement text with no cue relation"],
                "stable_identity_expectation": "alignment note references source cue map revision",
                "episode_002_relation": f"{state.get('scene_count')} scenes / {state.get('cue_count')} cues must remain traceable",
            },
        ],
        "allowed_material_summary_ja": "ローカルに存在し、由来と照合方法を書ける source/transcript/receipt だけ。",
        "forbidden_material_summary_ja": "live fetch、scraping、外部media download、OAuth/API/payment、public-ready承認、YMM4実行結果は対象外。",
        "transcript_alignment_requirements": {
            "cue_map_reference": state.get("source_cue_map_reference"),
            "scene_count": state.get("scene_count"),
            "cue_count": state.get("cue_count"),
            "minimum_alignment": "S1-S3 and csv_row_1-9 relation must be declared before replacement",
        },
    }


def _source_artifact_index(state: dict[str, Any]) -> dict[str, Any]:
    paths = _dict(state.get("paths"))
    records = [
        _source_record("ymm4_import_ready_validation", paths.get("ymm4_validation"), "source_episode_pack_reference", True),
        _source_record("ymm4_import_ready_cue_map", paths.get("ymm4_cue_map"), "episode_002_cue_map", True),
        _source_record("ymm4_import_ready_manifest", paths.get("ymm4_manifest"), "source_pack_manifest", True),
        _source_record("real_input_intake_manifest", paths.get("intake_manifest"), "prior_input_contract", True),
        _source_record("source_transcript_contract_schema", paths.get("intake_contract_schema"), "prior_input_contract", True),
        _source_record("real_input_intake_validation", paths.get("intake_validation"), "prior_input_readback", True),
        _source_record("local_edit_validation", paths.get("local_edit_validation"), "local_edit_context", True),
    ]
    return {
        "schema_version": "real_input_replacement_source_artifact_index.v1",
        "artifact_id": state.get("artifact_id"),
        "ymm4_import_ready_pack_read_only": True,
        "real_input_intake_pack_read_only": True,
        "local_edit_pack_read_only": True,
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
    requirements: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    required_inputs = _list(requirements.get("required_local_inputs"))
    closed_gate_flags = {flag: False for flag in CLOSED_GATE_FLAGS}
    return {
        "schema_version": "real_input_replacement_manifest.v1",
        "artifact_id": state.get("artifact_id"),
        "artifact_kind": "episode-real-input-replacement-readiness-pack",
        "episode_id": EPISODE_ID,
        "package_type": "real_input_replacement_readiness",
        "status": "ready_for_verified_local_input_not_replaced",
        "lane_id": "INPUT_API_HUB/VERIFIED_REAL_INPUT_PREP",
        "output_dir": _relpath(output_root, repo_root),
        "files": {filename: _relpath(output_root / filename, repo_root) for filename in REQUIRED_REAL_INPUT_REPLACEMENT_FILES},
        "source_episode_pack_reference": state.get("source_episode_pack_reference"),
        "source_episode_pack_validation": state.get("source_episode_pack_validation"),
        "source_cue_map_reference": state.get("source_cue_map_reference"),
        "placeholder_state": state.get("placeholder_state"),
        "required_local_input_count": len(required_inputs),
        "candidate_input_count": _candidate_input_count(output_root),
        "scene_count": state.get("scene_count"),
        "cue_count": state.get("cue_count"),
        "queue_count": state.get("queue_count"),
        "closed_gate_flags": closed_gate_flags,
        "actual_real_input_replaced": False,
        "real_input_replaced": False,
        "live_fetch_performed": False,
        "external_media_downloaded": False,
        "actual_ymm4_imported": False,
        "actual_yymm4_import": False,
        "rendered_video_created": False,
        "yymm4_rendered": False,
        "ymmp_file_created": False,
        "production_ymmp_written": False,
        "rights_approved": False,
        "rights_accepted": False,
        "public_ready": False,
        "final_thumbnail_approval": False,
        "youtube_uploaded": False,
        "gates_closed": True,
        "primary_review_file": state.get("primary_human_review"),
        "primary_human_review": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "next_gate": state.get("next_gate"),
        "next_artifact_expected": state.get("next_artifact_expected"),
        "full_pytest_run": False,
    }


def _render_html(state: dict[str, Any], manifest: dict[str, Any], requirements: dict[str, Any]) -> str:
    runway_steps = [
        ("現在", "sample/diagnosticのみ", "既存packはcue順とplaceholder境界を読めるが、実入力はまだない。"),
        ("入力待ち", "verified local input", "source path、transcript/receipt、provenance/rights note、stable identity、cue対応を揃える。"),
        ("検証", "local-only receipt", "ファイル存在、hash/size/date、Episode 002 cue map対応を確認する。"),
        ("次artifact", "validated local input receipt", "実入力置換を走らせる前のreadbackを作る。"),
    ]
    runway = "\n".join(_render_runway_step(index, *step) for index, step in enumerate(runway_steps, start=1))
    requirement_rows = "\n".join(_render_requirement_row(row) for row in _list(requirements.get("required_local_inputs")))
    gate_rows = "\n".join(_render_gate_row(flag, value) for flag, value in _dict(manifest.get("closed_gate_flags")).items())
    return f"""<!doctype html>
<html lang="ja" data-real-input-replacement-readiness="true" data-artifact-kind="episode-real-input-replacement-readiness-pack">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 実入力置換準備</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #101412;
      --surface: #18211e;
      --panel: #202a26;
      --ink: #f1f7f3;
      --muted: #aebdb4;
      --line: #36473f;
      --accent: #7ad8bf;
      --warn: #f2cf7a;
      --stop: #efa5a5;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; background: var(--bg); color: var(--ink); line-height: 1.5; }}
    main {{ max-width: 1240px; margin: 0 auto; padding: 28px 18px 44px; }}
    h1, h2 {{ margin: 0; letter-spacing: 0; }}
    h1 {{ font-size: clamp(28px, 4vw, 42px); line-height: 1.08; }}
    h2 {{ font-size: 20px; margin: 30px 0 12px; }}
    p {{ color: var(--muted); margin: 0; }}
    code {{ color: var(--warn); }}
    .hero {{ display: grid; gap: 14px; padding-bottom: 18px; border-bottom: 1px solid var(--line); }}
    .metrics {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .metric {{ border: 1px solid var(--line); border-radius: 999px; padding: 5px 10px; background: var(--surface); font-size: 12px; }}
    .runway {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; }}
    .step {{ border-top: 4px solid var(--accent); background: var(--surface); padding: 10px; min-height: 118px; }}
    .step strong {{ display: block; color: var(--warn); margin-bottom: 6px; }}
    .matrix {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
    th, td {{ border: 1px solid var(--line); padding: 9px; vertical-align: top; overflow-wrap: anywhere; }}
    th {{ color: var(--warn); background: var(--panel); text-align: left; }}
    td {{ background: var(--surface); }}
    .ok {{ color: var(--accent); }}
    .hold {{ color: var(--stop); }}
    .band {{ border: 1px solid var(--line); background: var(--surface); padding: 12px; }}
    @media (prefers-color-scheme: light) {{
      :root {{ --bg: #f6faf7; --surface: #ffffff; --panel: #edf5f0; --ink: #15211b; --muted: #516258; --line: #c7d8cf; }}
    }}
    @media (max-width: 860px) {{
      main {{ padding: 20px 12px 34px; }}
      .runway {{ grid-template-columns: 1fr; }}
      .matrix {{ display: block; overflow-x: auto; white-space: normal; }}
      th, td {{ min-width: 180px; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div class="metrics">
        <span class="metric">placeholder: {_escape(manifest.get("placeholder_state"))}</span>
        <span class="metric">required input: {_escape(manifest.get("required_local_input_count"))}</span>
        <span class="metric">candidate input: {_escape(manifest.get("candidate_input_count"))}</span>
        <span class="metric">next gate: {_escape(manifest.get("next_gate"))}</span>
      </div>
      <h1>Episode 002 実入力置換準備</h1>
      <p>このpackageは、sample/diagnosticのEpisode 002を実入力で置換する前に、どのローカルsource/transcript/receiptが必要かをoperatorが確認するための準備面です。置換、YMM4 import、render、`.ymmp`作成、rights/public承認はすべて未実行です。</p>
    </section>

    <section data-region="pipeline-runway">
      <h2>pipeline runway</h2>
      <div class="runway">{runway}</div>
    </section>

    <section data-region="input-matrix">
      <h2>必要なverified local input</h2>
      <table class="matrix">
        <thead><tr><th>入力</th><th>必要な証跡</th><th>許可される材料</th><th>禁止される材料</th><th>Episode 002 cue mapとの関係</th></tr></thead>
        <tbody>{requirement_rows}</tbody>
      </table>
    </section>

    <section data-region="material-boundary">
      <h2>material boundary</h2>
      <div class="band">
        <p><strong class="ok">allowed:</strong> {_escape(requirements.get("allowed_material_summary_ja"))}</p>
        <p><strong class="hold">forbidden:</strong> {_escape(requirements.get("forbidden_material_summary_ja"))}</p>
      </div>
    </section>

    <section data-region="closed-gates">
      <h2>閉じたgate / 未実行</h2>
      <table class="matrix">
        <thead><tr><th>gate key</th><th>値</th><th>意味</th></tr></thead>
        <tbody>{gate_rows}</tbody>
      </table>
    </section>

    <section data-region="next-artifact">
      <h2>次に期待するartifact</h2>
      <div class="band">
        <p><code>{_escape(manifest.get("next_artifact_expected"))}</code> を、実ファイル提供後に別artifactとして作る。そこまで real input replacement は走らせない。</p>
      </div>
    </section>
  </main>
</body>
</html>
"""


def _render_runway_step(index: int, label: str, status: str, note: str) -> str:
    return f"""<div class="step">
  <strong>{index}. {_escape(label)}</strong>
  <code>{_escape(status)}</code>
  <p>{_escape(note)}</p>
</div>"""


def _render_requirement_row(row: Any) -> str:
    item = _dict(row)
    return f"""<tr>
  <td>{_escape(item.get("label_ja"))}<br><code>{_escape(item.get("input_id"))}</code></td>
  <td>{_escape(item.get("expected_value"))}<br>{_escape(item.get("stable_identity_expectation"))}</td>
  <td>{_escape(", ".join(_list(item.get("accepted_material_types"))))}</td>
  <td><span class="hold">{_escape(", ".join(_list(item.get("forbidden_material_types"))))}</span></td>
  <td>{_escape(item.get("episode_002_relation"))}</td>
</tr>"""


def _render_gate_row(flag: str, value: Any) -> str:
    return f"""<tr>
  <td><code>{_escape(flag)}</code></td>
  <td><code>{_escape(value)}</code></td>
  <td><span class="ok">false = 未実行 / このpackageでは閉じたまま</span></td>
</tr>"""


def _render_contract(state: dict[str, Any], requirements: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| {item.get('label_ja')} | `{item.get('input_id')}` | {item.get('expected_value')} | {item.get('episode_002_relation')} |"
        for item in _list(requirements.get("required_local_inputs"))
        if isinstance(item, dict)
    )
    return f"""# Episode 002 実入力置換前 operator contract

このcontractは、sample/diagnosticのEpisode 002を実入力へ置換する前に必要なローカル材料だけを定義する。ここでは置換を実行しない。YMM4 import、render/export、production `.ymmp` write、rights/public approval、YouTube uploadも実行しない。

参照元: `{state.get("source_episode_pack_reference")}`
cue map: `{state.get("source_cue_map_reference")}`

| 入力 | stable key | 必要な内容 | Episode 002 cue mapとの関係 |
| --- | --- | --- | --- |
{rows}

## 5つの確認

1. source audio/video/document path と transcript path または transcript generation receipt path が、ローカルで開ける場所として示されている。
2. provenance/rights note はreview用メモであり、public-ready approvalやlegal acceptanceを主張していない。
3. hash、file size、modified time、export receiptなど、stable identityとして再確認できる情報がある。
4. Episode 002 cue map のS1-S3またはcsv_row_1-9へ、どの範囲が対応するかが書かれている。
5. live fetch、scraping、external media download、YMM4 import/render、`.ymmp` writeはこの段階で行っていない。

次に作るべきものは `{state.get("next_artifact_expected")}`。実ファイルが入るまでは real input replacement は未実行のままにする。
"""


def _render_dropzone_readme(state: dict[str, Any]) -> str:
    return f"""# input_dropzone

This is a placeholder folder only for the Episode 002 real-input replacement readiness contract.

Do not place media files in this commit. Future local files may be reviewed here only after the user provides verified material and asks for the next gate.

Expected future layout:

- `source/` for the verified local source audio/video/document path.
- `transcript/` for the transcript path or transcript generation receipt.
- `receipt/` for provenance, rights note, hash, file size, or stable identity notes.

Current state: no candidate input files are tracked. The next gate remains `{state.get("next_gate")}`.
"""


def _render_readme(state: dict[str, Any], manifest: dict[str, Any], requirements: dict[str, Any]) -> str:
    return f"""# Episode 002 実入力置換準備pack

Primary review: `real_input_replacement_preview.html`
Operator contract: `real_input_replacement_contract.md`
Machine readback: `validation_readback.json`

このpackは、実入力置換の前に必要なローカルsource/transcript/receiptを明確にする。現在のcandidate inputは `{manifest.get("candidate_input_count")}` 件で、置換は未実行。

- required local input count: `{manifest.get("required_local_input_count")}`
- source episode pack: `{manifest.get("source_episode_pack_reference")}`
- cue map: `{state.get("source_cue_map_reference")}`
- next gate: `{manifest.get("next_gate")}`

Allowed material: {requirements.get("allowed_material_summary_ja")}

Forbidden material: {requirements.get("forbidden_material_summary_ja")}
"""


def _render_limitations() -> str:
    return """# Limitations

Do not launch YMM4 from this package.
Do not render/export video.
Do not write a production `.ymmp` file.
Do not perform real input replacement from this package.
Do not approve rights, public readiness, final thumbnail, or YouTube upload.
Do not live fetch, scrape, download external media, use OAuth/API keys, or perform payment work.
"""


def _candidate_input_count(root: Path) -> int:
    dropzone = root / "input_dropzone"
    if not dropzone.exists():
        return 0
    return sum(1 for path in dropzone.rglob("*") if path.is_file() and path.name.lower() != "readme.md")


def _numbered_check_count(text: str) -> int:
    prefixes = tuple(f"{index}." for index in range(1, 10))
    return sum(1 for line in text.splitlines() if line.strip().startswith(prefixes))
