"""YMM4 observation readback package for episode 002."""

from __future__ import annotations

import hashlib
import json
import os
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

DEFAULT_OUTPUT_DIRNAME = "ymm4_observation_readback_pack"
DEFAULT_ARTIFACT_ID = "episode_002_ymm4_observation_readback_pack_v1"
EPISODE_ID = "yukkuri_newsroom_content_spine_002"
OBSERVATION_RECEIPT_SCHEMA_VERSION = "ymm4_gui_observation_receipt.v1"
EXPECTED_SCENE_ORDER = ("S1", "S2", "S3")
EXPECTED_CUE_ORDER = tuple(f"csv_row_{index}" for index in range(1, 10))
FIVE_POINT_OBSERVATION_KEYS = (
    "cue_order",
    "voice_items",
    "subtitle_text",
    "timing_order",
    "placeholder_boundary",
)

YMM4_IMPORT_READY_DIRNAME = "ymm4_import_ready_pack"
REAL_INPUT_PREP_DIRNAME = "real_input_replacement_readiness_pack"

REQUIRED_YMM4_OBSERVATION_FILES = (
    "observation_readback.json",
    "observation_preview.html",
    "manual_ymm4_observation_readback.md",
    "source_artifact_index.json",
    "README_YMM4_OBSERVATION_READBACK.md",
    "limitations.md",
)

CLOSED_GATE_FLAGS = (
    "rendered_video_created",
    "ymmp_file_created",
    "production_ymmp_written",
    "real_input_replaced",
    "rights_approved",
    "public_ready",
    "final_thumbnail_approval",
    "youtube_uploaded",
    "live_fetch_performed",
    "external_media_downloaded",
)


def build_ymm4_observation_readback_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
    observation_receipt: str | Path | None = None,
) -> dict[str, Any]:
    """Build an observation-only YMM4 readback package."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)
    receipt_path = Path(observation_receipt) if observation_receipt is not None else None
    receipt = _load_observation_receipt(receipt_path) if receipt_path is not None else None

    paths = _input_paths(source_root)
    payloads = _load_payloads(paths)
    state = _state(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        payloads=payloads,
        observation_receipt_path=receipt_path,
        observation_receipt=receipt,
    )
    readback = _observation_readback(state, output_root, repo_root)
    source_index = _source_artifact_index(state)

    _write_json(output_root / "observation_readback.json", readback)
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_text(output_root / "observation_preview.html", _render_html(state, readback))
    _write_text(output_root / "manual_ymm4_observation_readback.md", _render_manual_readback(state, readback))
    _write_text(output_root / "README_YMM4_OBSERVATION_READBACK.md", _render_readme(state, readback))
    _write_text(output_root / "limitations.md", _render_limitations(readback))

    return validate_ymm4_observation_readback_pack(output_root)


def validate_ymm4_observation_readback_pack(output_dir: str | Path) -> dict[str, Any]:
    """Validate the YMM4 observation readback package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_YMM4_OBSERVATION_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    readback = _load_json_if_present(files["observation_readback.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])
    if not isinstance(readback, dict):
        failed_checks.append("observation_readback_json_invalid")
        readback = {}
    if not isinstance(source_index, dict):
        failed_checks.append("source_index_json_invalid")
        source_index = {}

    readback = _dict(readback)
    source_index = _dict(source_index)
    html_text = files["observation_preview.html"].read_text(encoding="utf-8") if files["observation_preview.html"].exists() else ""
    manual_text = files["manual_ymm4_observation_readback.md"].read_text(encoding="utf-8") if files["manual_ymm4_observation_readback.md"].exists() else ""
    limitations_text = files["limitations.md"].read_text(encoding="utf-8") if files["limitations.md"].exists() else ""
    closed_gates = _dict(readback.get("closed_gate_flags"))
    manual_check_count = _numbered_check_count(manual_text)

    if readback.get("schema_version") != "ymm4_observation_readback.v1":
        failed_checks.append("readback_schema_version_mismatch")
    if readback.get("status") not in {"passed", "blocked", "partial"}:
        failed_checks.append("readback_status_invalid")
    if readback.get("status") == "passed" and readback.get("actual_ymm4_imported") is not True:
        failed_checks.append("passed_without_actual_import")
    if readback.get("artifact_id") != DEFAULT_ARTIFACT_ID:
        failed_checks.append("artifact_id_mismatch")
    if readback.get("episode_id") != EPISODE_ID:
        failed_checks.append("episode_id_mismatch")
    if readback.get("observation_mode") not in {"actual_ymm4_gui_observation", "operator_instruction_only"}:
        failed_checks.append("observation_mode_invalid")
    if readback.get("observation_mode") == "operator_instruction_only":
        if readback.get("status") != "blocked":
            failed_checks.append("operator_instruction_status_not_blocked")
        if readback.get("actual_ymm4_import_attempted") is not False:
            failed_checks.append("operator_instruction_attempted_import")
        if readback.get("actual_ymm4_imported") is not False:
            failed_checks.append("operator_instruction_imported_true")
        if readback.get("cue_count_observed") != 0:
            failed_checks.append("operator_instruction_observed_cues_not_zero")
        if readback.get("next_gate") != "manual_ymm4_import_observation_return":
            failed_checks.append("operator_instruction_next_gate_invalid")
    if readback.get("observation_mode") == "actual_ymm4_gui_observation":
        source_records = [_dict(record) for record in _list(source_index.get("records"))]
        receipt_recorded = any(record.get("record_id") == "actual_gui_observation_receipt" for record in source_records)
        if not receipt_recorded:
            failed_checks.append("actual_observation_receipt_not_indexed")
        if readback.get("actual_ymm4_import_attempted") is not True:
            failed_checks.append("actual_observation_import_not_attempted")
        if readback.get("actual_ymm4_imported") is not True:
            failed_checks.append("actual_observation_import_not_completed")
        if readback.get("status") not in {"passed", "partial"}:
            failed_checks.append("actual_observation_status_invalid")
        if readback.get("cue_count_observed") != readback.get("cue_count_expected"):
            failed_checks.append("actual_observation_cue_count_mismatch")
        if readback.get("receipt_source_csv") != readback.get("expected_import_path"):
            failed_checks.append("actual_observation_source_csv_mismatch")
        if len(str(readback.get("source_csv_sha256") or "")) != 64:
            failed_checks.append("actual_observation_source_sha256_missing")
        if readback.get("scene_order_observed") != list(EXPECTED_SCENE_ORDER):
            failed_checks.append("actual_observation_scene_order_mismatch")
        if readback.get("cue_order_observed") != list(EXPECTED_CUE_ORDER):
            failed_checks.append("actual_observation_cue_order_mismatch")
        if not readback.get("observed_at") or str(readback.get("observed_at")).startswith("not_observed"):
            failed_checks.append("actual_observation_timestamp_missing")
        for field in (
            "voice_item_observed",
            "subtitle_item_observed",
            "timing_order_observed",
            "placeholder_boundary_observed",
        ):
            if readback.get(field) in {None, "", "not_observed"}:
                failed_checks.append(f"actual_observation_field_missing:{field}")
        observations = _dict(readback.get("five_point_observations"))
        for key in FIVE_POINT_OBSERVATION_KEYS:
            if not _dict(observations.get(key)).get("status"):
                failed_checks.append(f"actual_observation_check_missing:{key}")
        passed_five_points = _five_point_observations_pass(observations)
        if readback.get("status") == "passed":
            if readback.get("observation_result") != "passed":
                failed_checks.append("actual_observation_passed_result_invalid")
            if not passed_five_points or _list(readback.get("import_errors")):
                failed_checks.append("actual_observation_passed_without_five_point_pass")
            if readback.get("next_gate") != "render_proof_after_observation":
                failed_checks.append("actual_observation_passed_next_gate_invalid")
        elif passed_five_points:
            failed_checks.append("actual_observation_partial_without_gap")
        elif readback.get("observation_result") != "pass_with_warnings":
            failed_checks.append("actual_observation_partial_result_invalid")
        elif readback.get("next_gate") != "adapter_correction_after_observation":
            failed_checks.append("actual_observation_partial_next_gate_invalid")
        safety = _dict(readback.get("safety"))
        if safety.get("application_closed_without_saving") is not True:
            failed_checks.append("actual_observation_not_closed_without_saving")
        for field in (
            "render_or_export_performed",
            "ymmp_saved_or_written",
            "real_input_replaced",
            "rights_or_public_approval_performed",
            "upload_performed",
        ):
            if safety.get(field) is not False:
                failed_checks.append(f"actual_observation_safety_not_false:{field}")
        if readback.get("next_gate") == "manual_ymm4_import_observation_return":
            failed_checks.append("actual_observation_manual_gate_not_advanced")
    for flag in CLOSED_GATE_FLAGS:
        if readback.get(flag) is not False:
            failed_checks.append(f"gate_not_false:{flag}")
        if closed_gates.get(flag) is not False:
            failed_checks.append(f"closed_gate_not_false:{flag}")
    if readback.get("cue_count_expected") != 9:
        failed_checks.append("cue_count_expected_mismatch")
    if readback.get("scene_count_expected") != 3:
        failed_checks.append("scene_count_expected_mismatch")
    if readback.get("next_gate") not in {"manual_ymm4_import_observation_return", "adapter_correction_after_observation", "render_proof_after_observation"}:
        failed_checks.append("next_gate_invalid")
    if source_index.get("ymm4_import_ready_pack_read_only") is not True:
        failed_checks.append("ymm4_import_ready_pack_not_read_only")
    if source_index.get("real_input_prep_pack_read_only") is not True:
        failed_checks.append("real_input_prep_pack_not_read_only")
    if '<html lang="ja"' not in html_text:
        failed_checks.append("html_not_japanese_lang")
    for marker in (
        'data-ymm4-observation-readback="true"',
        'data-region="pipeline-runway"',
        'data-region="observation-matrix"',
        'data-region="closed-gates"',
        'data-region="next-decision"',
    ):
        if marker not in html_text:
            failed_checks.append(f"html_marker_missing:{marker}")
    if "card-grid" in html_text or 'data-region="card-grid"' in html_text:
        failed_checks.append("html_card_grid_marker_found")
    if "実観測は未実行" not in html_text and readback.get("observation_mode") == "operator_instruction_only":
        failed_checks.append("html_blocked_copy_missing")
    if manual_check_count > 5:
        failed_checks.append("manual_checks_too_many")
    if manual_check_count < 1:
        failed_checks.append("manual_checks_missing")
    if "Do not render/export" not in manual_text:
        failed_checks.append("manual_missing_render_stop")
    if "Do not launch render/export" not in limitations_text:
        failed_checks.append("limitations_render_stop_missing")

    visible_files = [path for path in files.values() if path.exists()]
    external_refs = _external_refs_in_files(visible_files)
    forbidden_claims = _forbidden_true_claims(root)
    temporary_hits = _temporary_copy_hits(visible_files)
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_claims)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    validation_status = "passed" if not failed_checks else "failed"
    readback["validation_status"] = validation_status
    readback["failed_checks"] = failed_checks
    readback["checks"] = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": isinstance(readback, dict) and isinstance(source_index, dict),
        "html_preview_exists": files["observation_preview.html"].exists(),
        "manual_readback_exists": files["manual_ymm4_observation_readback.md"].exists(),
        "japanese_first_surface": '<html lang="ja"' in html_text,
        "primary_card_grid_absent": "card-grid" not in html_text,
        "operator_instruction_check_count": manual_check_count,
        "closed_gate_flags": closed_gates,
        "external_dependency_status": "none_found" if not external_refs else external_refs,
        "forbidden_true_claims_absent": not forbidden_claims,
        "temporary_copy_absent": not temporary_hits,
    }
    readback["primary_review_file"] = str(root / "observation_preview.html")
    readback["primary_human_review"] = str(root / "observation_preview.html")
    readback["primary_machine_readable"] = str(root / "observation_readback.json")
    readback["launcher_or_open_command"] = f'Invoke-Item -LiteralPath "{(root / "observation_preview.html").resolve()}"'
    readback["access_state"] = "verified_present" if (root / "observation_preview.html").exists() else "missing"
    _write_json(root / "observation_readback.json", readback)
    return readback


def _load_observation_receipt(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"YMM4 observation receipt not found: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"YMM4 observation receipt is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("YMM4 observation receipt must be a JSON object")
    if payload.get("schema_version") != OBSERVATION_RECEIPT_SCHEMA_VERSION:
        raise ValueError(
            "YMM4 observation receipt schema mismatch: "
            f"expected {OBSERVATION_RECEIPT_SCHEMA_VERSION}"
        )
    if payload.get("episode_id") != EPISODE_ID:
        raise ValueError(f"YMM4 observation receipt episode must be {EPISODE_ID}")
    if payload.get("status") not in {"passed", "partial"}:
        raise ValueError("YMM4 observation receipt status must be passed or partial")
    if payload.get("next_gate") not in {
        "adapter_correction_after_observation",
        "render_proof_after_observation",
    }:
        raise ValueError("YMM4 observation receipt next_gate is invalid")
    observations = _dict(payload.get("five_point_observations"))
    missing = [key for key in FIVE_POINT_OBSERVATION_KEYS if not _dict(observations.get(key)).get("status")]
    if missing:
        raise ValueError(f"YMM4 observation receipt is missing five-point checks: {', '.join(missing)}")
    passed_five_points = _five_point_observations_pass(observations)
    if payload.get("status") == "passed":
        if payload.get("result") != "passed":
            raise ValueError("A passed YMM4 observation receipt must use result=passed")
        if not passed_five_points or _list(payload.get("import_errors")):
            raise ValueError("A passed YMM4 observation receipt requires all five checks to pass")
        if payload.get("next_gate") != "render_proof_after_observation":
            raise ValueError("A passed YMM4 observation receipt must advance to render proof")
    elif passed_five_points:
        raise ValueError("A partial YMM4 observation receipt must retain an observed gap")
    elif payload.get("result") != "pass_with_warnings":
        raise ValueError("A partial YMM4 observation receipt must use result=pass_with_warnings")
    elif payload.get("next_gate") != "adapter_correction_after_observation":
        raise ValueError("A partial YMM4 observation receipt must advance to adapter correction")
    for field in (
        "observed_at",
        "result",
        "observed_by_environment",
        "actual_ymm4_import_attempted",
        "actual_ymm4_imported",
        "source_csv",
        "source_csv_sha256",
        "import_errors",
        "deviations",
        "safety",
    ):
        if field not in payload:
            raise ValueError(f"YMM4 observation receipt is missing required field: {field}")
    if payload.get("actual_ymm4_import_attempted") is not True:
        raise ValueError("YMM4 observation receipt must record an attempted GUI import")
    if payload.get("actual_ymm4_imported") is not True:
        raise ValueError("YMM4 observation receipt must record a completed GUI import")
    safety = _dict(payload.get("safety"))
    if safety.get("application_closed_without_saving") is not True:
        raise ValueError("YMM4 observation receipt must record closing without saving")
    for field in (
        "render_or_export_performed",
        "ymmp_saved_or_written",
        "real_input_replaced",
        "rights_or_public_approval_performed",
        "upload_performed",
    ):
        if safety.get(field) is not False:
            raise ValueError(f"YMM4 observation receipt safety field must be false: {field}")
    return payload


def _five_point_observations_pass(observations: dict[str, Any]) -> bool:
    cue = _dict(observations.get("cue_order"))
    voice = _dict(observations.get("voice_items"))
    subtitle = _dict(observations.get("subtitle_text"))
    timing = _dict(observations.get("timing_order"))
    placeholder = _dict(observations.get("placeholder_boundary"))
    statuses_pass = all(
        _dict(observations.get(key)).get("status") == "passed"
        for key in FIVE_POINT_OBSERVATION_KEYS
    )
    return bool(
        statuses_pass
        and cue.get("scene_order") == list(EXPECTED_SCENE_ORDER)
        and cue.get("cue_order") == list(EXPECTED_CUE_ORDER)
        and voice.get("count") == len(EXPECTED_CUE_ORDER)
        and not _list(voice.get("missing_cue_ids"))
        and not _list(voice.get("duplicate_cue_ids"))
        and voice.get("reordered") is False
        and subtitle.get("all_text_matched") is True
        and subtitle.get("speaker_cue_match") is True
        and timing.get("order_preserved") is True
        and placeholder.get("voiceitem_subtitle_lane_present") is True
        and placeholder.get("imageitem_placeholder_lanes_present") is True
        and placeholder.get("textitem_placeholder_lanes_present") is True
        and placeholder.get("misleading_final_or_public_ready_claim_present") is False
    )


def _input_paths(source_root: Path) -> dict[str, Path]:
    import_root = source_root / YMM4_IMPORT_READY_DIRNAME
    real_input_root = source_root / REAL_INPUT_PREP_DIRNAME
    return {
        "ymm4_import_ready_root": import_root,
        "ymm4_import_ready_validation": import_root / "validation_readback.json",
        "ymm4_import_ready_manifest": import_root / "ymm4_import_ready_manifest.json",
        "ymm4_cue_map": import_root / "edit_slice_to_ymm4_cue_map.json",
        "ymm4_manual_sheet": import_root / "manual_ymm4_import_observation_sheet.md",
        "real_input_prep_root": real_input_root,
        "real_input_prep_validation": real_input_root / "validation_readback.json",
        "real_input_prep_contract": real_input_root / "real_input_replacement_contract.md",
        "ir_bridge_csv": source_root / "ir_bridge" / "draft_yymm4.csv",
        "regenerated_csv": source_root / "transcript_substitution_readiness" / "regenerated_draft_yymm4.csv",
        "preview_csv": source_root / "ymm4_import_preview_pack" / "draft_yymm4_preview.csv",
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "ymm4_import_ready_validation": _load_json_if_present(paths["ymm4_import_ready_validation"]),
        "ymm4_import_ready_manifest": _load_json_if_present(paths["ymm4_import_ready_manifest"]),
        "ymm4_cue_map": _load_json_if_present(paths["ymm4_cue_map"]),
        "real_input_prep_validation": _load_json_if_present(paths["real_input_prep_validation"]),
    }


def _state(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    repo_root: Path,
    paths: dict[str, Path],
    payloads: dict[str, Any],
    observation_receipt_path: Path | None,
    observation_receipt: dict[str, Any] | None,
) -> dict[str, Any]:
    cue_map = _dict(payloads.get("ymm4_cue_map"))
    import_validation = _dict(payloads.get("ymm4_import_ready_validation"))
    real_input_validation = _dict(payloads.get("real_input_prep_validation"))
    detected = _detect_yymm4()
    if observation_receipt:
        detected.update(_dict(observation_receipt.get("observed_by_environment")))
    csv_candidates = _csv_candidates(paths, cue_map, repo_root)
    primary_import_csv = csv_candidates[0]["repo_relative_path"] if csv_candidates else ""
    verified_source_csv_sha256 = ""
    if observation_receipt:
        receipt_source_csv = str(observation_receipt.get("source_csv") or "")
        if receipt_source_csv != primary_import_csv:
            raise ValueError(
                "YMM4 observation receipt source_csv must match the primary import CSV"
            )
        source_path = repo_root / receipt_source_csv
        if not source_path.exists():
            raise FileNotFoundError(f"YMM4 observation source CSV not found: {source_path}")
        verified_source_csv_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest().upper()
        receipt_sha256 = str(observation_receipt.get("source_csv_sha256") or "").upper()
        if receipt_sha256 != verified_source_csv_sha256:
            raise ValueError("YMM4 observation receipt source_csv_sha256 does not match the source CSV")
    return {
        "schema_version": "ymm4_observation_state.v1",
        "artifact_id": artifact_id,
        "episode_id": EPISODE_ID,
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "paths": {name: _relpath(path, repo_root) for name, path in paths.items()},
        "source_import_ready_pack_reference": _relpath(paths["ymm4_import_ready_root"], repo_root),
        "source_real_input_prep_reference": _relpath(paths["real_input_prep_root"], repo_root),
        "cue_count_expected": cue_map.get("cue_count") or import_validation.get("cue_count") or 0,
        "scene_count_expected": cue_map.get("scene_count") or import_validation.get("scene_count") or 0,
        "queue_count": import_validation.get("queue_count"),
        "real_input_prep_status": real_input_validation.get("status"),
        "csv_candidates": csv_candidates,
        "primary_import_csv": primary_import_csv,
        "verified_source_csv_sha256": verified_source_csv_sha256,
        "yymm4_environment": detected,
        "observation_receipt": observation_receipt,
        "observation_receipt_path": (
            _relpath(observation_receipt_path, repo_root) if observation_receipt_path is not None else ""
        ),
        "blocker": (
            {
                "blocker_id": "none",
                "status": "resolved_by_actual_gui_observation",
                "reason": "The bounded YMM4 GUI import observation was completed.",
                "operator_action": "none",
            }
            if observation_receipt
            else _observation_blocker(detected)
        ),
        "next_gate": (
            observation_receipt.get("next_gate")
            if observation_receipt
            else "manual_ymm4_import_observation_return"
        ),
    }


def _observation_readback(state: dict[str, Any], output_root: Path, repo_root: Path) -> dict[str, Any]:
    closed_gates = {flag: False for flag in CLOSED_GATE_FLAGS}
    blocker = _dict(state.get("blocker"))
    receipt = _dict(state.get("observation_receipt"))
    common = {
        "schema_version": "ymm4_observation_readback.v1",
        "artifact_id": DEFAULT_ARTIFACT_ID,
        "episode_id": EPISODE_ID,
        "source_import_ready_pack_reference": state.get("source_import_ready_pack_reference"),
        "source_real_input_prep_reference": state.get("source_real_input_prep_reference"),
        "cue_count_expected": state.get("cue_count_expected"),
        "scene_count_expected": state.get("scene_count_expected"),
        "expected_import_path": state.get("primary_import_csv"),
        "importable_csv_candidates": state.get("csv_candidates"),
        "rendered_video_created": False,
        "ymmp_file_created": False,
        "production_ymmp_written": False,
        "real_input_replaced": False,
        "rights_approved": False,
        "public_ready": False,
        "final_thumbnail_approval": False,
        "youtube_uploaded": False,
        "live_fetch_performed": False,
        "external_media_downloaded": False,
        "closed_gate_flags": closed_gates,
        "next_gate": state.get("next_gate"),
        "output_dir": _relpath(output_root, repo_root),
    }
    if not receipt:
        common.update(
            {
                "status": "blocked",
                "observation_mode": "operator_instruction_only",
                "actual_ymm4_import_attempted": False,
                "actual_ymm4_imported": False,
                "observed_at": "not_observed_2026-07-09_JST",
                "observed_by_environment": state.get("yymm4_environment"),
                "cue_count_observed": 0,
                "scene_order_observed": [],
                "cue_order_observed": [],
                "voice_item_observed": "not_observed",
                "subtitle_item_observed": "not_observed",
                "timing_order_observed": "not_observed",
                "placeholder_boundary_observed": "not_observed",
                "five_point_observations": {},
                "timeline_observation": {},
                "speaker_mapping": [],
                "import_errors": [],
                "deviations": [
                    {
                        "deviation_id": "actual_gui_observation_not_performed",
                        "severity": "blocking_for_observation_pass",
                        "detail": blocker.get("reason"),
                    }
                ],
                "blocker": blocker,
                "screenshot_or_visual_evidence_paths": [],
            }
        )
        return common

    observations = _dict(receipt.get("five_point_observations"))
    cue_observation = _dict(observations.get("cue_order"))
    voice_observation = _dict(observations.get("voice_items"))
    subtitle_observation = _dict(observations.get("subtitle_text"))
    timing_observation = _dict(observations.get("timing_order"))
    placeholder_observation = _dict(observations.get("placeholder_boundary"))
    voice_count = voice_observation.get("count", 0)
    duration_seconds = timing_observation.get("duration_seconds")
    voice_items_match = (
        voice_count == state.get("cue_count_expected")
        and not _list(voice_observation.get("missing_cue_ids"))
        and not _list(voice_observation.get("duplicate_cue_ids"))
        and voice_observation.get("reordered") is False
    )
    subtitle_status = subtitle_observation.get("status")
    timing_order_preserved = timing_observation.get("order_preserved") is True
    placeholder_lanes_present = (
        placeholder_observation.get("imageitem_placeholder_lanes_present") is True
        and placeholder_observation.get("textitem_placeholder_lanes_present") is True
    )
    common.update(
        {
            "status": receipt.get("status"),
            "observation_result": receipt.get(
                "result",
                "passed" if receipt.get("status") == "passed" else "pass_with_warnings",
            ),
            "observation_mode": "actual_ymm4_gui_observation",
            "actual_ymm4_import_attempted": receipt.get("actual_ymm4_import_attempted"),
            "actual_ymm4_imported": receipt.get("actual_ymm4_imported"),
            "observed_at": receipt.get("observed_at"),
            "observed_by_environment": state.get("yymm4_environment"),
            "cue_count_observed": voice_count,
            "scene_order_observed": cue_observation.get("scene_order", []),
            "cue_order_observed": cue_observation.get("cue_order", []),
            "voice_item_observed": (
                f"{voice_count}_voiceitems_no_missing_duplicate_or_reorder"
                if voice_items_match
                else f"{voice_count}_voiceitems_with_count_or_order_deviation"
            ),
            "subtitle_item_observed": (
                "linked_subtitle_texts_match_after_manual_character_mapping"
                if subtitle_status == "passed_with_manual_mapping"
                else f"linked_subtitle_text_status_{subtitle_status}"
            ),
            "timing_order_observed": (
                f"order_preserved_actual_voice_duration_{duration_seconds}_seconds"
                if timing_order_preserved
                else f"order_not_preserved_actual_voice_duration_{duration_seconds}_seconds"
            ),
            "placeholder_boundary_observed": (
                "imageitem_textitem_placeholder_lanes_present"
                if placeholder_lanes_present
                else "imageitem_textitem_placeholder_lanes_absent"
            ),
            "five_point_observations": observations,
            "timeline_observation": timing_observation,
            "speaker_mapping": subtitle_observation.get("speaker_mapping", []),
            "import_errors": _list(receipt.get("import_errors")),
            "deviations": _list(receipt.get("deviations")),
            "blocker": blocker,
            "screenshot_or_visual_evidence_paths": _list(
                receipt.get("screenshot_or_visual_evidence_paths")
            ),
            "source_csv_sha256": state.get("verified_source_csv_sha256"),
            "receipt_source_csv": receipt.get("source_csv"),
            "safety": _dict(receipt.get("safety")),
            "next_gate": receipt.get("next_gate"),
        }
    )
    return common


def _source_artifact_index(state: dict[str, Any]) -> dict[str, Any]:
    paths = _dict(state.get("paths"))
    records = [
        _source_record("ymm4_import_ready_validation", paths.get("ymm4_import_ready_validation"), "import_ready_readback", True),
        _source_record("ymm4_import_ready_manifest", paths.get("ymm4_import_ready_manifest"), "import_ready_manifest", True),
        _source_record("ymm4_cue_map", paths.get("ymm4_cue_map"), "cue_map_expected_observation", True),
        _source_record("ymm4_manual_sheet", paths.get("ymm4_manual_sheet"), "prior_operator_sheet", True),
        _source_record("real_input_prep_validation", paths.get("real_input_prep_validation"), "real_input_gate_readback", True),
        _source_record("real_input_prep_contract", paths.get("real_input_prep_contract"), "real_input_gate_contract", True),
    ]
    if state.get("observation_receipt_path"):
        records.append(
            _source_record(
                "actual_gui_observation_receipt",
                state.get("observation_receipt_path"),
                "actual_gui_observation_receipt",
                True,
            )
        )
    return {
        "schema_version": "ymm4_observation_source_artifact_index.v1",
        "artifact_id": state.get("artifact_id"),
        "ymm4_import_ready_pack_read_only": True,
        "real_input_prep_pack_read_only": True,
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


def _render_html(state: dict[str, Any], readback: dict[str, Any]) -> str:
    is_actual = readback.get("observation_mode") == "actual_ymm4_gui_observation"
    observations = _dict(readback.get("five_point_observations"))
    voice_observation = _dict(observations.get("voice_items"))
    subtitle_observation = _dict(observations.get("subtitle_text"))
    timing_observation = _dict(observations.get("timing_order"))
    placeholder_observation = _dict(observations.get("placeholder_boundary"))
    if is_actual:
        voice_count = voice_observation.get("count")
        subtitle_status = subtitle_observation.get("status")
        timing_status = timing_observation.get("status")
        placeholder_status = placeholder_observation.get("status")
        deviation_ids = ", ".join(
            str(_dict(item).get("deviation_id")) for item in _list(readback.get("deviations"))
        )
        runway_steps = [
            ("準備済み", "import-ready pack", "3 scenes / 9 cues の観測対象を使用。"),
            ("実観測", "actual YMM4 GUI", f"{voice_count} VoiceItemsの順序とlinked subtitle textを確認。"),
            ("今回の判定", str(readback.get("status")), f"subtitle={subtitle_status}; timing={timing_status}; placeholder={placeholder_status}."),
            ("次判断", str(readback.get("next_gate")), "観測証拠に限定して次gateへ進む。"),
        ]
        hero_copy = (
            f"実YMM4 GUIでbounded importを観測済み。VoiceItems={voice_count}; "
            f"subtitle={subtitle_status}; timing={timing_status}; placeholder={placeholder_status}."
        )
        result_label = "observation result"
        result_copy = f"{readback.get('observation_result')} / {readback.get('status')}"
        result_class = "ok" if readback.get("status") == "passed" else "hold"
        unresolved_copy = f"recorded deviations: {deviation_ids or 'none'}。render/exportやproduction approvalは未実施。"
        next_copy = "五点観測の証拠とrecorded deviationsに限定して次gateへ進む。"
    else:
        runway_steps = [
            ("準備済み", "import-ready pack", "3 scenes / 9 cues の観測対象は定義済み。"),
            ("今回の判定", "operator_instruction_only", "YMM4実行ファイルは検出したが、GUI importを安全に操作・視認できる経路がない。"),
            ("返却待ち", "manual observation", "operatorがYMM4上でimport結果を確認し、5点だけ返す。"),
            ("次判断", str(readback.get("next_gate")), "観測結果によりadapter correction、real input receipt、render proof待ちを分岐する。"),
        ]
        hero_copy = "実観測は未実行。YMM4 executable は検出済みだが、GUI importをこのworkerが安全に操作・視認する経路がないため、operator instructionとして保持する。"
        result_label = "blocker"
        result_copy = _dict(readback.get("blocker")).get("reason")
        result_class = "hold"
        unresolved_copy = "VoiceItem、subtitle、timing order、placeholder boundary、visual evidence は actual GUI importが未実行のため未観測。"
        next_copy = "operatorが5点の観測結果を返した後、adapter correction / real input receipt / later render proof のどれに進むかを決める。"
    runway = "\n".join(_render_runway_step(index, *step) for index, step in enumerate(runway_steps, start=1))
    status_rows = "\n".join(
        _render_status_row(label, value)
        for label, value in (
            ("observation_mode", readback.get("observation_mode")),
            ("actual_ymm4_import_attempted", readback.get("actual_ymm4_import_attempted")),
            ("actual_ymm4_imported", readback.get("actual_ymm4_imported")),
            ("cue_count_expected", readback.get("cue_count_expected")),
            ("cue_count_observed", readback.get("cue_count_observed")),
            ("scene_order_observed", readback.get("scene_order_observed")),
            ("cue_order_observed", readback.get("cue_order_observed")),
            ("voice_item_observed", readback.get("voice_item_observed")),
            ("subtitle_item_observed", readback.get("subtitle_item_observed")),
            ("timing_order_observed", readback.get("timing_order_observed")),
            ("placeholder_boundary_observed", readback.get("placeholder_boundary_observed")),
        )
    )
    check_rows = "\n".join(
        _render_status_row(key, _dict(value).get("status"))
        for key, value in observations.items()
    )
    gate_rows = "\n".join(_render_gate_row(flag, value) for flag, value in _dict(readback.get("closed_gate_flags")).items())
    env = _dict(readback.get("observed_by_environment"))
    csv_rows = "\n".join(_render_csv_row(row) for row in _list(readback.get("importable_csv_candidates")))
    return f"""<!doctype html>
<html lang="ja" data-ymm4-observation-readback="true" data-artifact-kind="episode-ymm4-observation-readback-pack">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 YMM4観測readback</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #101413;
      --surface: #18211f;
      --panel: #202b28;
      --ink: #f0f7f4;
      --muted: #a9bbb3;
      --line: #34463f;
      --accent: #7dd7c2;
      --warn: #f1cc75;
      --stop: #f0a0a0;
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
    .band {{ border: 1px solid var(--line); background: var(--surface); padding: 12px; }}
    .ok {{ color: var(--accent); }}
    .hold {{ color: var(--stop); }}
    @media (prefers-color-scheme: light) {{
      :root {{ --bg: #f7faf8; --surface: #ffffff; --panel: #edf5f1; --ink: #17211e; --muted: #516258; --line: #c8d9d1; }}
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
        <span class="metric">status: {_escape(readback.get("status"))}</span>
        <span class="metric">mode: {_escape(readback.get("observation_mode"))}</span>
        <span class="metric">expected cues: {_escape(readback.get("cue_count_expected"))}</span>
        <span class="metric">observed cues: {_escape(readback.get("cue_count_observed"))}</span>
      </div>
      <h1>Episode 002 YMM4観測readback</h1>
      <p>{_escape(hero_copy)}</p>
    </section>

    <section data-region="pipeline-runway">
      <h2>pipeline runway</h2>
      <div class="runway">{runway}</div>
    </section>

    <section data-region="observation-matrix">
      <h2>観測matrix / result or blocker</h2>
      <table class="matrix">
        <thead><tr><th>項目</th><th>readback</th></tr></thead>
        <tbody>{status_rows}</tbody>
      </table>
    </section>

    <section data-region="five-point-observations">
      <h2>五点観測</h2>
      <table class="matrix">
        <thead><tr><th>項目</th><th>判定</th></tr></thead>
        <tbody>{check_rows or _render_status_row("actual_observation", "not_observed")}</tbody>
      </table>
    </section>

    <section data-region="expected-import-path">
      <h2>expected import path</h2>
      <div class="band">
        <p>YMM4: <code>{_escape(env.get("yymm4_executable_path"))}</code></p>
        <p>CSV: <code>{_escape(readback.get("expected_import_path"))}</code></p>
        <p>{_escape(result_label)}: <span class="{result_class}">{_escape(result_copy)}</span></p>
      </div>
      <table class="matrix">
        <thead><tr><th>candidate</th><th>exists</th><th>role</th></tr></thead>
        <tbody>{csv_rows}</tbody>
      </table>
    </section>

    <section data-region="untested">
      <h2>未検証または未解消の項目</h2>
      <div class="band">
        <p>{_escape(unresolved_copy)}</p>
      </div>
    </section>

    <section data-region="closed-gates">
      <h2>閉じたgate</h2>
      <table class="matrix">
        <thead><tr><th>gate key</th><th>値</th><th>意味</th></tr></thead>
        <tbody>{gate_rows}</tbody>
      </table>
    </section>

    <section data-region="next-decision">
      <h2>次の判断</h2>
      <div class="band">
        <p><code>{_escape(readback.get("next_gate"))}</code>: {_escape(next_copy)}</p>
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


def _render_status_row(label: str, value: Any) -> str:
    return f"""<tr>
  <td><code>{_escape(label)}</code></td>
  <td>{_escape(value)}</td>
</tr>"""


def _render_gate_row(flag: str, value: Any) -> str:
    return f"""<tr>
  <td><code>{_escape(flag)}</code></td>
  <td><code>{_escape(value)}</code></td>
  <td><span class="ok">false = 未実行 / このpackageでは閉じたまま</span></td>
</tr>"""


def _render_csv_row(row: Any) -> str:
    item = _dict(row)
    return f"""<tr>
  <td><code>{_escape(item.get("repo_relative_path"))}</code></td>
  <td>{_escape(item.get("exists"))}</td>
  <td>{_escape(item.get("role"))}</td>
</tr>"""


def _render_manual_readback(state: dict[str, Any], readback: dict[str, Any]) -> str:
    env = _dict(readback.get("observed_by_environment"))
    blocker = _dict(readback.get("blocker"))
    if readback.get("observation_mode") == "actual_ymm4_gui_observation":
        observations = _dict(readback.get("five_point_observations"))
        cue = _dict(observations.get("cue_order"))
        voice = _dict(observations.get("voice_items"))
        subtitle = _dict(observations.get("subtitle_text"))
        timing = _dict(observations.get("timing_order"))
        placeholder = _dict(observations.get("placeholder_boundary"))
        mapping_text = "; ".join(
            (
                f"{_dict(item).get('source_speaker')} -> {_dict(item).get('selected_character')}"
                + (
                    f" (initial={_dict(item).get('initial_default_character')})"
                    if _dict(item).get("initial_default_character")
                    else ""
                )
            )
            for item in _list(subtitle.get("speaker_mapping"))
        )
        sampled_text = "; ".join(
            f"{_dict(item).get('cue_id')}={_dict(item).get('start_frame')}/{_dict(item).get('length_frames')} frames"
            for item in _list(timing.get("sampled_items"))
        )
        placeholder_lanes_present = (
            placeholder.get("imageitem_placeholder_lanes_present") is True
            and placeholder.get("textitem_placeholder_lanes_present") is True
        )
        placeholder_presence = "ある" if placeholder_lanes_present else "ない"
        return f"""# Episode 002 YMM4観測readback

状態: `{readback.get("status")}` / `actual_ymm4_gui_observation`

YMM4 `{env.get("yymm4_version")}` で対象CSVを実際に読み込み、保存せずに終了した。観測結果はreceiptから再生成され、総合判定は`{readback.get("status")}`。

YMM4 executable:
`{env.get("yymm4_executable_path")}`

import済みCSV:
`{readback.get("expected_import_path")}`

## 実観測結果5点

1. **{cue.get("status")}** — scene order: {' -> '.join(str(item) for item in _list(cue.get("scene_order")))}; cue order: {' -> '.join(str(item) for item in _list(cue.get("cue_order")))}。
2. **{voice.get("status")}** — VoiceItemは{voice.get("count")}件。missing={_list(voice.get("missing_cue_ids"))}; duplicate={_list(voice.get("duplicate_cue_ids"))}; reordered={voice.get("reordered")}。
3. **{subtitle.get("status")}** — linked subtitle textのspeaker/cue match={subtitle.get("speaker_cue_match")}; mapping: {mapping_text or 'none'}。
4. **{timing.get("status")}** — order_preserved={timing.get("order_preserved")}; provisional_exact_durations_preserved={timing.get("provisional_exact_durations_preserved")}; {timing.get("frame_rate")}fps・{timing.get("total_frames")} frames・{timing.get("duration_seconds")}秒。sampled: {sampled_text or 'none'}。
5. **{placeholder.get("status")}** — VoiceItem/subtitle lane={placeholder.get("voiceitem_subtitle_lane_present")}; ImageItem/TextItem placeholder scene laneは{placeholder_presence}; misleading_final_or_public_ready_claim={placeholder.get("misleading_final_or_public_ready_claim_present")}。

次gate: `{readback.get("next_gate")}`

Do not render/export. Do not save or write production `.ymmp`. Do not replace real input. Do not approve rights/public/final thumbnail. Do not upload.
"""
    return f"""# Episode 002 YMM4観測readback

状態: `operator_instruction_only`

実観測は未実行。YMM4 executable は検出されたが、このworkerからGUI import結果を安全に操作・視認する経路がないため、観測passは付けない。

YMM4 executable:
`{env.get("yymm4_executable_path")}`

開くもの:
`{state.get("source_import_ready_pack_reference")}/ymm4_import_ready_preview.html`

import候補CSV:
`{readback.get("expected_import_path")}`

blocker:
{blocker.get("reason")}

## operatorが返す観測5点

1. CSV import後、cue順がS1 -> S2 -> S3、csv_row_1 -> csv_row_9として読めるか。
2. VoiceItemが9 cue分に見えるか、欠落・重複・順序入れ替わりがあるか。
3. subtitle/textがspeakerとcueに対応し、sample/diagnostic textであることが誤解なく見えるか。
4. timing orderは仮timingの流れを崩していないか。
5. visual/overlay/citation/thumbnail要素がplaceholder境界として読め、final素材やpublic-readyを示していないか。

Do not render/export. Do not save or write production `.ymmp`. Do not replace real input. Do not approve rights/public/final thumbnail. Do not upload.
"""


def _render_readme(state: dict[str, Any], readback: dict[str, Any]) -> str:
    if readback.get("observation_mode") == "actual_ymm4_gui_observation":
        state_copy = (
            f"Actual bounded GUI import was observed with "
            f"`cue_count_observed={readback.get('cue_count_observed')}` and "
            f"`status={readback.get('status')}`. VoiceItem, subtitle, timing, and placeholder "
            "outcomes are recorded in `observation_readback.json`; no result is inferred beyond "
            "those fields. YMM4 was closed without saving the project."
        )
    else:
        state_copy = (
            "Actual GUI import was not performed, so `status=blocked` and "
            "`observation_mode=operator_instruction_only`."
        )
    return f"""# Episode 002 YMM4観測readback pack

Primary review: `observation_preview.html`
Machine readback: `observation_readback.json`
Manual operator sheet: `manual_ymm4_observation_readback.md`

This package records the current observation-only state. {state_copy}

- source import-ready pack: `{readback.get("source_import_ready_pack_reference")}`
- source real-input prep pack: `{readback.get("source_real_input_prep_reference")}`
- expected cue count: `{readback.get("cue_count_expected")}`
- observed cue count: `{readback.get("cue_count_observed")}`
- next gate: `{readback.get("next_gate")}`

No render/export, production `.ymmp`, real input replacement, rights/public
approval, thumbnail approval, upload, live fetch, or external media download
occurred.
"""


def _render_limitations(readback: dict[str, Any]) -> str:
    if readback.get("observation_mode") == "actual_ymm4_gui_observation":
        deviation_ids = ", ".join(
            str(_dict(item).get("deviation_id")) for item in _list(readback.get("deviations"))
        )
        observation_copy = (
            "Actual observed means only the bounded CSV import and the five recorded GUI "
            "checks occurred. It does not prove render, production `.ymmp`, real-input, "
            f"rights, thumbnail, upload, or public readiness. Observation status is "
            f"`{readback.get('status')}`; recorded deviations: {deviation_ids or 'none'}."
        )
    else:
        observation_copy = (
            "Actual observed means actual GUI/manual observation occurred. This package is "
            "blocked/operator-instruction-only until that evidence is returned."
        )
    return f"""# Limitations

Do not launch render/export from this package.
Do not write or save a production `.ymmp` file.
Do not replace sample placeholders with real input.
Do not approve rights, legal status, public readiness, final thumbnail, or upload.
Do not live fetch, scrape, download external media, use OAuth/API keys, or perform payment work.

{observation_copy}
"""


def _detect_yymm4() -> dict[str, Any]:
    home = Path.home()
    shortcut = home / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "YukkuriMovieMaker.lnk"
    override = os.environ.get("NLMYTGEN_YMM4_EXE", "").strip()
    candidates = ([Path(override)] if override else []) + [
        home / "Downloads" / "YukkuriMovieMaker_v4" / "YukkuriMovieMaker.exe",
        home / "AppData" / "Local" / "YukkuriMovieMaker" / "YukkuriMovieMaker.exe",
    ]
    executable = next((path for path in candidates if path.exists()), None)
    status = "executable_detected_but_gui_observation_not_attempted" if executable else "not_detected"
    if executable is None and shortcut.exists():
        status = "start_menu_shortcut_detected_but_target_not_resolved"
    return {
        "terminal_or_device": home.name,
        "yymm4_availability_status": status,
        "yymm4_executable_detected": executable is not None,
        "yymm4_executable_path": str(executable) if executable else "",
        "environment_override_used": bool(override and executable == Path(override)),
        "start_menu_shortcut_detected": shortcut.exists(),
        "start_menu_shortcut_path": str(shortcut) if shortcut.exists() else "",
        "launch_attempted": False,
        "gui_observation_channel_available": False,
    }


def _observation_blocker(detected: dict[str, Any]) -> dict[str, Any]:
    if detected.get("yymm4_executable_detected"):
        reason = (
            "YMM4 executable was detected locally, but this worker has no safe "
            "manual/GUI visual readback channel for importing and inspecting the project."
        )
    else:
        reason = "YMM4 executable was not detected in the checked local paths."
    return {
        "blocker_id": "manual_gui_observation_required",
        "status": "blocked_for_actual_observation",
        "reason": reason,
        "operator_action": "Open YMM4 manually, import the CSV candidate, inspect cue/voice/subtitle/timing/placeholder boundaries, and return the five observations.",
    }


def _csv_candidates(paths: dict[str, Path], cue_map: dict[str, Any], repo_root: Path) -> list[dict[str, Any]]:
    candidates: list[Path] = []
    for cue in _list(cue_map.get("cues")):
        source = _dict(cue).get("voice_or_subtitle_action", {})
        expected = _dict(source).get("expected_subtitle_source")
        if isinstance(expected, str) and expected:
            candidates.append(repo_root / expected.split("#", 1)[0])
    for key in ("regenerated_csv", "ir_bridge_csv", "preview_csv"):
        candidates.append(paths[key])

    seen: set[str] = set()
    rows: list[dict[str, Any]] = []
    for path in candidates:
        resolved = path.resolve()
        marker = str(resolved).lower()
        if marker in seen:
            continue
        seen.add(marker)
        rows.append(
            {
                "repo_relative_path": _relpath(path, repo_root),
                "exists": path.exists(),
                "role": "primary_import_candidate" if not rows else "alternate_import_candidate",
            }
        )
    return rows


def _numbered_check_count(text: str) -> int:
    prefixes = tuple(f"{index}." for index in range(1, 10))
    return sum(1 for line in text.splitlines() if line.strip().startswith(prefixes))
