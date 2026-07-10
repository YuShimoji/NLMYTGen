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
CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION = "ymm4_gui_observation_receipt.v2"
OBSERVATION_BLOCKER_SCHEMA_VERSION = "ymm4_gui_observation_blocker.v1"
EXPECTED_SCENE_ORDER = ("S1", "S2", "S3")
EXPECTED_CUE_ORDER = tuple(f"csv_row_{index}" for index in range(1, 10))
LEGACY_FIVE_POINT_OBSERVATION_KEYS = (
    "cue_order",
    "voice_items",
    "subtitle_text",
    "timing_order",
    "placeholder_boundary",
)
CSV_GATE_FIVE_POINT_OBSERVATION_KEYS = (
    "cue_order",
    "voice_items",
    "subtitle_text",
    "timing_order",
    "csv_responsibility_boundary",
)

YMM4_IMPORT_READY_DIRNAME = "ymm4_import_ready_pack"
REAL_INPUT_PREP_DIRNAME = "real_input_replacement_readiness_pack"
ALIAS_COVERAGE_FILENAME = "yymm4_character_alias_coverage_readback.json"
ORIGINAL_OBSERVATION_RECEIPT_FILENAME = "ymm4_observation_receipt_2026-07-10.json"

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
    "diagnostic_ymmp_project_attempted",
)


def build_ymm4_observation_readback_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
    observation_receipt: str | Path | None = None,
    observation_blocker: str | Path | None = None,
) -> dict[str, Any]:
    """Build an observation-only YMM4 readback package."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)
    receipt_path = Path(observation_receipt) if observation_receipt is not None else None
    receipt = _load_observation_receipt(receipt_path) if receipt_path is not None else None
    blocker_path = Path(observation_blocker) if observation_blocker is not None else None
    if receipt_path is not None and blocker_path is not None:
        raise ValueError("Use either an observation receipt or an observation blocker, not both")
    blocker_receipt = _load_observation_blocker(blocker_path) if blocker_path is not None else None

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
        observation_blocker_path=blocker_path,
        observation_blocker=blocker_receipt,
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

    if readback.get("schema_version") != "ymm4_observation_readback.v2":
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
        if readback.get("next_gate") != "bounded_yymm4_alias_reobservation":
            failed_checks.append("operator_instruction_next_gate_invalid")
        if not _dict(readback.get("prior_observation_evidence")):
            failed_checks.append("operator_instruction_prior_evidence_missing")
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
            "responsibility_boundary_observed",
        ):
            if readback.get(field) in {None, "", "not_observed"}:
                failed_checks.append(f"actual_observation_field_missing:{field}")
        observations = _dict(readback.get("five_point_observations"))
        receipt_schema = str(readback.get("receipt_schema_version") or "")
        expected_keys = (
            CSV_GATE_FIVE_POINT_OBSERVATION_KEYS
            if receipt_schema == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION
            else LEGACY_FIVE_POINT_OBSERVATION_KEYS
        )
        for key in expected_keys:
            if not _dict(observations.get(key)).get("status"):
                failed_checks.append(f"actual_observation_check_missing:{key}")
        passed_five_points = _five_point_observations_pass(observations, receipt_schema=receipt_schema)
        if receipt_schema == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION:
            if readback.get("status") == "passed":
                if readback.get("observation_result") != "passed":
                    failed_checks.append("csv_gate_observation_passed_result_invalid")
                if not passed_five_points or _list(readback.get("import_errors")):
                    failed_checks.append("csv_gate_observation_passed_without_five_point_pass")
                if readback.get("next_gate") != "supervisor_next_slice_decision":
                    failed_checks.append("csv_gate_observation_passed_next_gate_invalid")
            elif passed_five_points:
                failed_checks.append("csv_gate_observation_partial_without_gap")
            elif readback.get("observation_result") != "pass_with_warnings":
                failed_checks.append("csv_gate_observation_partial_result_invalid")
            elif readback.get("next_gate") != "bounded_yymm4_alias_reobservation":
                failed_checks.append("csv_gate_observation_partial_next_gate_invalid")
        else:
            if readback.get("status") == "passed":
                if readback.get("observation_result") != "passed" or not passed_five_points:
                    failed_checks.append("legacy_observation_passed_without_five_point_pass")
                if readback.get("next_gate") != "render_proof_after_observation":
                    failed_checks.append("legacy_observation_passed_next_gate_invalid")
            elif passed_five_points:
                failed_checks.append("legacy_observation_partial_without_gap")
            elif readback.get("observation_result") != "pass_with_warnings":
                failed_checks.append("legacy_observation_partial_result_invalid")
            elif readback.get("next_gate") != "adapter_correction_after_observation":
                failed_checks.append("legacy_observation_partial_next_gate_invalid")
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
        if readback.get("next_gate") == "bounded_yymm4_alias_reobservation" and readback.get("status") == "passed":
            failed_checks.append("actual_observation_passed_gate_not_advanced")
    for flag in CLOSED_GATE_FLAGS:
        if readback.get(flag) is not False:
            failed_checks.append(f"gate_not_false:{flag}")
        if closed_gates.get(flag) is not False:
            failed_checks.append(f"closed_gate_not_false:{flag}")
    if readback.get("cue_count_expected") != 9:
        failed_checks.append("cue_count_expected_mismatch")
    if readback.get("scene_count_expected") != 3:
        failed_checks.append("scene_count_expected_mismatch")
    if readback.get("next_gate") not in {
        "bounded_yymm4_alias_reobservation",
        "supervisor_next_slice_decision",
        "adapter_correction_after_observation",
        "render_proof_after_observation",
    }:
        failed_checks.append("next_gate_invalid")
    csv_gate = _dict(readback.get("csv_import_gate"))
    diagnostic_gate = _dict(readback.get("diagnostic_project_gate"))
    if csv_gate.get("expected_item_families") != ["VoiceItem", "linked_subtitle"]:
        failed_checks.append("csv_import_gate_contract_mismatch")
    if diagnostic_gate.get("authorization_status") != "not_authorized":
        failed_checks.append("diagnostic_project_authorization_not_closed")
    if diagnostic_gate.get("execution_status") != "not_attempted":
        failed_checks.append("diagnostic_project_execution_not_closed")
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
    schema_version = str(payload.get("schema_version") or "")
    if schema_version not in {
        OBSERVATION_RECEIPT_SCHEMA_VERSION,
        CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION,
    }:
        raise ValueError("YMM4 observation receipt schema mismatch")
    if payload.get("episode_id") != EPISODE_ID:
        raise ValueError(f"YMM4 observation receipt episode must be {EPISODE_ID}")
    if payload.get("status") not in {"passed", "partial"}:
        raise ValueError("YMM4 observation receipt status must be passed or partial")
    observations = _dict(payload.get("five_point_observations"))
    expected_keys = (
        CSV_GATE_FIVE_POINT_OBSERVATION_KEYS
        if schema_version == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION
        else LEGACY_FIVE_POINT_OBSERVATION_KEYS
    )
    missing = [key for key in expected_keys if not _dict(observations.get(key)).get("status")]
    if missing:
        raise ValueError(f"YMM4 observation receipt is missing five-point checks: {', '.join(missing)}")
    passed_five_points = _five_point_observations_pass(
        observations,
        receipt_schema=schema_version,
    )
    if schema_version == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION:
        if payload.get("observation_contract") != "ymm4_csv_import_gate.v1":
            raise ValueError("YMM4 CSV-gate receipt observation_contract is invalid")
        for field in (
            "canonical_source_csv",
            "canonical_source_csv_sha256",
            "selected_yymm4_character_profile",
            "profile_id",
            "prior_receipt_reference",
        ):
            if not payload.get(field):
                raise ValueError(f"YMM4 CSV-gate receipt is missing required field: {field}")
        if payload.get("status") == "passed":
            if payload.get("result") != "passed":
                raise ValueError("A passed YMM4 CSV-gate receipt must use result=passed")
            if not passed_five_points or _list(payload.get("import_errors")):
                raise ValueError("A passed YMM4 CSV-gate receipt requires all five checks to pass")
            if payload.get("next_gate") != "supervisor_next_slice_decision":
                raise ValueError("A passed YMM4 CSV-gate receipt must advance to supervisor decision")
        elif passed_five_points:
            raise ValueError("A partial YMM4 CSV-gate receipt must retain an observed gap")
        elif payload.get("result") != "pass_with_warnings":
            raise ValueError("A partial YMM4 CSV-gate receipt must use result=pass_with_warnings")
        elif payload.get("next_gate") != "bounded_yymm4_alias_reobservation":
            raise ValueError("A partial YMM4 CSV-gate receipt must retain the re-observation gate")
    else:
        if payload.get("next_gate") not in {
            "adapter_correction_after_observation",
            "render_proof_after_observation",
        }:
            raise ValueError("YMM4 observation receipt next_gate is invalid")
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


def _load_observation_blocker(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"YMM4 observation blocker not found: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"YMM4 observation blocker is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("YMM4 observation blocker must be a JSON object")
    if payload.get("schema_version") != OBSERVATION_BLOCKER_SCHEMA_VERSION:
        raise ValueError("YMM4 observation blocker schema mismatch")
    if payload.get("episode_id") != EPISODE_ID:
        raise ValueError(f"YMM4 observation blocker episode must be {EPISODE_ID}")
    if payload.get("status") != "blocked":
        raise ValueError("YMM4 observation blocker status must be blocked")
    if payload.get("blocker_id") != "existing_unsaved_project_requires_discard_authorization":
        raise ValueError("YMM4 observation blocker id is invalid")
    if payload.get("next_gate") != "bounded_yymm4_alias_reobservation":
        raise ValueError("YMM4 observation blocker next_gate is invalid")
    actions = _dict(payload.get("actions"))
    for field in (
        "existing_project_discarded",
        "new_project_created",
        "derived_csv_import_attempted",
        "render_or_export_performed",
        "ymmp_saved_or_written",
    ):
        if actions.get(field) is not False:
            raise ValueError(f"YMM4 observation blocker action must be false: {field}")
    if actions.get("application_left_open_to_preserve_unsaved_state") is not True:
        raise ValueError("YMM4 observation blocker must preserve the existing unsaved state")
    for field in (
        "blocked_at",
        "source_csv",
        "source_csv_sha256",
        "observed_by_environment",
        "operator_action",
    ):
        if not payload.get(field):
            raise ValueError(f"YMM4 observation blocker is missing required field: {field}")
    return payload


def _five_point_observations_pass(
    observations: dict[str, Any],
    *,
    receipt_schema: str,
) -> bool:
    cue = _dict(observations.get("cue_order"))
    voice = _dict(observations.get("voice_items"))
    subtitle = _dict(observations.get("subtitle_text"))
    timing = _dict(observations.get("timing_order"))
    if receipt_schema == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION:
        boundary = _dict(observations.get("csv_responsibility_boundary"))
        statuses_pass = all(
            _dict(observations.get(key)).get("status") == "passed"
            for key in CSV_GATE_FIVE_POINT_OBSERVATION_KEYS
        )
        return bool(
            statuses_pass
            and cue.get("scene_order") == list(EXPECTED_SCENE_ORDER)
            and cue.get("cue_order") == list(EXPECTED_CUE_ORDER)
            and voice.get("count") == len(EXPECTED_CUE_ORDER)
            and not _list(voice.get("missing_cue_ids"))
            and not _list(voice.get("duplicate_cue_ids"))
            and voice.get("reordered") is False
            and subtitle.get("mapping_dialog_present") is False
            and subtitle.get("automatic_speaker_binding_observed") is True
            and subtitle.get("all_text_matched") is True
            and subtitle.get("speaker_cue_match") is True
            and not _list(subtitle.get("incorrect_character_cue_ids"))
            and subtitle.get("character_counts")
            == {"ゆっくり霊夢": 3, "ゆっくり魔理沙": 6}
            and timing.get("order_preserved") is True
            and boundary.get("csv_import_expected_item_families")
            == ["VoiceItem", "linked_subtitle"]
            and boundary.get("diagnostic_project_gate") == "not_authorized"
            and boundary.get("diagnostic_project_status") == "not_attempted"
            and boundary.get("diagnostic_item_absence_is_csv_failure") is False
            and boundary.get("misleading_final_or_public_ready_claim_present") is False
        )

    placeholder = _dict(observations.get("placeholder_boundary"))
    statuses_pass = all(
        _dict(observations.get(key)).get("status") == "passed"
        for key in LEGACY_FIVE_POINT_OBSERVATION_KEYS
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
        "ymm4_alias_coverage": import_root / ALIAS_COVERAGE_FILENAME,
        "ymm4_derived_csv": import_root / "derived_yymm4_import.csv",
        "real_input_prep_root": real_input_root,
        "real_input_prep_validation": real_input_root / "validation_readback.json",
        "real_input_prep_contract": real_input_root / "real_input_replacement_contract.md",
        "ir_bridge_csv": source_root / "ir_bridge" / "draft_yymm4.csv",
        "regenerated_csv": source_root / "transcript_substitution_readiness" / "regenerated_draft_yymm4.csv",
        "preview_csv": source_root / "ymm4_import_preview_pack" / "draft_yymm4_preview.csv",
        "original_observation_receipt": source_root / ORIGINAL_OBSERVATION_RECEIPT_FILENAME,
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "ymm4_import_ready_validation": _load_json_if_present(paths["ymm4_import_ready_validation"]),
        "ymm4_import_ready_manifest": _load_json_if_present(paths["ymm4_import_ready_manifest"]),
        "ymm4_cue_map": _load_json_if_present(paths["ymm4_cue_map"]),
        "ymm4_alias_coverage": _load_json_if_present(paths["ymm4_alias_coverage"]),
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
    observation_blocker_path: Path | None,
    observation_blocker: dict[str, Any] | None,
) -> dict[str, Any]:
    cue_map = _dict(payloads.get("ymm4_cue_map"))
    import_validation = _dict(payloads.get("ymm4_import_ready_validation"))
    import_manifest = _dict(payloads.get("ymm4_import_ready_manifest"))
    alias_coverage = _dict(payloads.get("ymm4_alias_coverage"))
    real_input_validation = _dict(payloads.get("real_input_prep_validation"))
    detected = _detect_yymm4()
    if observation_receipt:
        detected.update(_dict(observation_receipt.get("observed_by_environment")))
    elif observation_blocker:
        detected = _dict(observation_blocker.get("observed_by_environment"))
    canonical_import_csv = str(
        import_manifest.get("canonical_source_csv")
        or _relpath(paths["regenerated_csv"], repo_root)
    )
    derived_import_csv = str(
        import_manifest.get("primary_import_csv")
        or _relpath(paths["ymm4_derived_csv"], repo_root)
    )
    receipt_schema = str(_dict(observation_receipt).get("schema_version") or "")
    primary_import_csv = (
        canonical_import_csv
        if receipt_schema == OBSERVATION_RECEIPT_SCHEMA_VERSION
        else derived_import_csv
    )
    csv_candidates = _csv_candidates(
        paths,
        import_manifest,
        repo_root,
        primary_import_csv=primary_import_csv,
    )
    source_path = repo_root / primary_import_csv
    if not source_path.exists():
        raise FileNotFoundError(f"YMM4 observation source CSV not found: {source_path}")
    verified_source_csv_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest().upper()
    if observation_receipt:
        receipt_source_csv = str(observation_receipt.get("source_csv") or "")
        if receipt_source_csv != primary_import_csv:
            raise ValueError(
                "YMM4 observation receipt source_csv must match the primary import CSV"
            )
        receipt_sha256 = str(observation_receipt.get("source_csv_sha256") or "").upper()
        if receipt_sha256 != verified_source_csv_sha256:
            raise ValueError("YMM4 observation receipt source_csv_sha256 does not match the source CSV")
        if receipt_schema == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION:
            canonical_hash = str(_dict(alias_coverage.get("canonical_csv")).get("sha256") or "")
            profile_id = str(_dict(alias_coverage.get("profile")).get("profile_id") or "")
            selected_profile = str(import_manifest.get("selected_yymm4_character_profile") or "")
            if observation_receipt.get("canonical_source_csv") != canonical_import_csv:
                raise ValueError("YMM4 CSV-gate receipt canonical_source_csv mismatch")
            if str(observation_receipt.get("canonical_source_csv_sha256") or "").upper() != canonical_hash:
                raise ValueError("YMM4 CSV-gate receipt canonical source SHA-256 mismatch")
            if observation_receipt.get("selected_yymm4_character_profile") != selected_profile:
                raise ValueError("YMM4 CSV-gate receipt selected profile path mismatch")
            if observation_receipt.get("profile_id") != profile_id:
                raise ValueError("YMM4 CSV-gate receipt profile_id mismatch")
            if observation_receipt.get("prior_receipt_reference") != _relpath(
                paths["original_observation_receipt"], repo_root
            ):
                raise ValueError("YMM4 CSV-gate receipt prior receipt reference mismatch")
    elif observation_blocker:
        if observation_blocker.get("source_csv") != primary_import_csv:
            raise ValueError("YMM4 observation blocker source_csv must match the derived import CSV")
        if str(observation_blocker.get("source_csv_sha256") or "").upper() != verified_source_csv_sha256:
            raise ValueError("YMM4 observation blocker source CSV SHA-256 mismatch")

    original_receipt_sha256 = hashlib.sha256(
        paths["original_observation_receipt"].read_bytes()
    ).hexdigest().upper()
    return {
        "schema_version": "ymm4_observation_state.v2",
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
        "canonical_import_csv": canonical_import_csv,
        "derived_import_csv": derived_import_csv,
        "selected_yymm4_character_profile": import_manifest.get("selected_yymm4_character_profile"),
        "profile_id": _dict(alias_coverage.get("profile")).get("profile_id"),
        "alias_coverage_reference": import_manifest.get("alias_coverage_readback"),
        "verified_source_csv_sha256": verified_source_csv_sha256,
        "canonical_source_csv_sha256": _dict(alias_coverage.get("canonical_csv")).get("sha256"),
        "prior_observation_evidence": {
            "receipt": _relpath(paths["original_observation_receipt"], repo_root),
            "receipt_sha256": original_receipt_sha256,
            "schema_version": OBSERVATION_RECEIPT_SCHEMA_VERSION,
            "status": "partial",
            "interpretation": "historical_result_under_legacy_placeholder_contract",
        },
        "yymm4_environment": detected,
        "observation_receipt": observation_receipt,
        "observation_receipt_path": (
            _relpath(observation_receipt_path, repo_root) if observation_receipt_path is not None else ""
        ),
        "observation_blocker": observation_blocker,
        "observation_blocker_path": (
            _relpath(observation_blocker_path, repo_root) if observation_blocker_path is not None else ""
        ),
        "blocker": (
            {
                "blocker_id": "none",
                "status": "resolved_by_actual_gui_observation",
                "reason": "The bounded YMM4 GUI import observation was completed.",
                "operator_action": "none",
            }
            if observation_receipt
            else {
                "blocker_id": observation_blocker.get("blocker_id"),
                "status": "blocked_for_actual_observation",
                "reason": observation_blocker.get("reason"),
                "operator_action": observation_blocker.get("operator_action"),
            }
            if observation_blocker
            else _observation_blocker(detected)
        ),
        "next_gate": (
            observation_receipt.get("next_gate")
            if observation_receipt
            else "bounded_yymm4_alias_reobservation"
        ),
    }


def _observation_readback(state: dict[str, Any], output_root: Path, repo_root: Path) -> dict[str, Any]:
    closed_gates = {flag: False for flag in CLOSED_GATE_FLAGS}
    blocker = _dict(state.get("blocker"))
    receipt = _dict(state.get("observation_receipt"))
    blocker_receipt = _dict(state.get("observation_blocker"))
    receipt_schema = str(receipt.get("schema_version") or "")
    common = {
        "schema_version": "ymm4_observation_readback.v2",
        "artifact_id": DEFAULT_ARTIFACT_ID,
        "episode_id": EPISODE_ID,
        "observation_contract": (
            "legacy_five_point_observation.v1"
            if receipt_schema == OBSERVATION_RECEIPT_SCHEMA_VERSION
            else "ymm4_csv_import_gate.v1"
        ),
        "receipt_schema_version": receipt_schema or None,
        "source_import_ready_pack_reference": state.get("source_import_ready_pack_reference"),
        "source_real_input_prep_reference": state.get("source_real_input_prep_reference"),
        "cue_count_expected": state.get("cue_count_expected"),
        "scene_count_expected": state.get("scene_count_expected"),
        "expected_import_path": state.get("primary_import_csv"),
        "canonical_source_csv": state.get("canonical_import_csv"),
        "canonical_source_csv_sha256": state.get("canonical_source_csv_sha256"),
        "derived_import_csv": state.get("derived_import_csv"),
        "selected_yymm4_character_profile": state.get("selected_yymm4_character_profile"),
        "profile_id": state.get("profile_id"),
        "alias_coverage_reference": state.get("alias_coverage_reference"),
        "prior_observation_evidence": state.get("prior_observation_evidence"),
        "importable_csv_candidates": state.get("csv_candidates"),
        "csv_import_gate": {
            "contract": "ymm4_csv_import_gate.v1",
            "expected_item_families": ["VoiceItem", "linked_subtitle"],
            "status": "not_observed" if not receipt else receipt.get("status"),
        },
        "diagnostic_project_gate": {
            "expected_item_families": ["ImageItem", "independent_TextItem_placeholders"],
            "authorization_status": "not_authorized",
            "execution_status": "not_attempted",
            "absence_during_csv_import_is_failure": False,
        },
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
        "diagnostic_ymmp_project_attempted": False,
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
                "observed_at": blocker_receipt.get("blocked_at") or "not_observed_2026-07-11_JST",
                "observed_by_environment": state.get("yymm4_environment"),
                "cue_count_observed": 0,
                "scene_order_observed": [],
                "cue_order_observed": [],
                "voice_item_observed": "not_observed",
                "subtitle_item_observed": "not_observed",
                "timing_order_observed": "not_observed",
                "responsibility_boundary_observed": "not_observed",
                "five_point_observations": {},
                "timeline_observation": {},
                "speaker_mapping": [],
                "import_errors": [],
                "deviations": [
                    {
                        "deviation_id": blocker_receipt.get("blocker_id")
                        or "bounded_alias_reobservation_not_performed",
                        "severity": "blocking_for_observation_pass",
                        "detail": blocker.get("reason"),
                    }
                ],
                "blocker": blocker,
                "observation_blocker_receipt": state.get("observation_blocker_path") or None,
                "safety": _dict(blocker_receipt.get("actions")),
                "screenshot_or_visual_evidence_paths": [],
            }
        )
        return common

    observations = _dict(receipt.get("five_point_observations"))
    cue_observation = _dict(observations.get("cue_order"))
    voice_observation = _dict(observations.get("voice_items"))
    subtitle_observation = _dict(observations.get("subtitle_text"))
    timing_observation = _dict(observations.get("timing_order"))
    responsibility_observation = _dict(
        observations.get("csv_responsibility_boundary")
        if receipt_schema == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION
        else observations.get("placeholder_boundary")
    )
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
    legacy_placeholder_lanes_present = (
        responsibility_observation.get("imageitem_placeholder_lanes_present") is True
        and responsibility_observation.get("textitem_placeholder_lanes_present") is True
    )
    common.update(
        {
            "status": receipt.get("status"),
            "receipt_schema_version": receipt_schema,
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
                "linked_subtitle_texts_match_with_automatic_character_binding"
                if receipt_schema == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION
                and subtitle_status == "passed"
                else "linked_subtitle_texts_match_after_manual_character_mapping"
                if subtitle_status == "passed_with_manual_mapping"
                else f"linked_subtitle_text_status_{subtitle_status}"
            ),
            "timing_order_observed": (
                f"order_preserved_actual_voice_duration_{duration_seconds}_seconds"
                if timing_order_preserved
                else f"order_not_preserved_actual_voice_duration_{duration_seconds}_seconds"
            ),
            "responsibility_boundary_observed": (
                "csv_voiceitem_linked_subtitle_only_diagnostic_project_not_authorized_not_attempted"
                if receipt_schema == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION
                else "legacy_imageitem_textitem_placeholder_lanes_present"
                if legacy_placeholder_lanes_present
                else "legacy_imageitem_textitem_placeholder_lanes_absent"
            ),
            "five_point_observations": observations,
            "timeline_observation": timing_observation,
            "speaker_mapping": subtitle_observation.get("speaker_mapping", []),
            "character_counts": subtitle_observation.get("character_counts", {}),
            "mapping_dialog_present": subtitle_observation.get("mapping_dialog_present"),
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
        _source_record("ymm4_alias_coverage", paths.get("ymm4_alias_coverage"), "alias_derivation_readback", True),
        _source_record("ymm4_derived_csv", paths.get("ymm4_derived_csv"), "primary_derived_import_csv", True),
        _source_record("canonical_csv", paths.get("regenerated_csv"), "canonical_speaker_identity_read_only", True),
        _source_record("prior_gui_observation_receipt", paths.get("original_observation_receipt"), "immutable_legacy_partial_evidence", True),
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
    if state.get("observation_blocker_path"):
        records.append(
            _source_record(
                "actual_gui_observation_blocker",
                state.get("observation_blocker_path"),
                "existing_unsaved_project_preserved_blocker",
                True,
            )
        )
    return {
        "schema_version": "ymm4_observation_source_artifact_index.v2",
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
    boundary_observation = _dict(
        observations.get("csv_responsibility_boundary")
        or observations.get("placeholder_boundary")
    )
    if is_actual:
        voice_count = voice_observation.get("count")
        subtitle_status = subtitle_observation.get("status")
        timing_status = timing_observation.get("status")
        boundary_status = boundary_observation.get("status")
        deviation_ids = ", ".join(
            str(_dict(item).get("deviation_id")) for item in _list(readback.get("deviations"))
        )
        runway_steps = [
            ("準備済み", "import-ready pack", "3 scenes / 9 cues の観測対象を使用。"),
            ("実観測", "actual YMM4 GUI", f"{voice_count} VoiceItemsの順序とlinked subtitle textを確認。"),
            ("今回の判定", str(readback.get("status")), f"subtitle={subtitle_status}; timing={timing_status}; responsibility={boundary_status}."),
            ("次判断", str(readback.get("next_gate")), "観測証拠に限定して次gateへ進む。"),
        ]
        hero_copy = (
            f"実YMM4 GUIでbounded importを観測済み。VoiceItems={voice_count}; "
            f"subtitle={subtitle_status}; timing={timing_status}; responsibility={boundary_status}."
        )
        result_label = "observation result"
        result_copy = f"{readback.get('observation_result')} / {readback.get('status')}"
        result_class = "ok" if readback.get("status") == "passed" else "hold"
        unresolved_copy = f"recorded deviations: {deviation_ids or 'none'}。render/exportやproduction approvalは未実施。"
        next_copy = "五点観測の証拠とrecorded deviationsに限定して次gateへ進む。"
    else:
        runway_steps = [
            ("準備済み", "import-ready pack", "3 scenes / 9 cues の観測対象は定義済み。"),
            ("今回の判定", "operator_instruction_only", "derived CSVは生成・検証済みだが、bounded GUI re-observationは未実行。"),
            ("返却待ち", "bounded re-observation", "derived CSVだけをimportし、CSV責務の5点を確認する。"),
            ("次判断", str(readback.get("next_gate")), "CSV gate結果だけを返し、diagnostic projectは自動開始しない。"),
        ]
        hero_copy = "実観測は未実行。explicit profileとderived CSVは準備済みで、現在はbounded alias re-observationのoperator instructionとして保持する。"
        result_label = "blocker"
        result_copy = _dict(readback.get("blocker")).get("reason")
        result_class = "hold"
        unresolved_copy = "mapping dialog、9 VoiceItems、character binding、text/order、timing order、CSV responsibility boundaryは未観測。"
        next_copy = "bounded CSV gateの結果を返した後、supervisorがdiagnostic `.ymmp` proofまたはreal inputを選ぶ。"
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
            ("responsibility_boundary_observed", readback.get("responsibility_boundary_observed")),
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
        <p>Derived CSV: <code>{_escape(readback.get("expected_import_path"))}</code></p>
        <p>Canonical source: <code>{_escape(readback.get("canonical_source_csv"))}</code></p>
        <p>Character profile: <code>{_escape(readback.get("selected_yymm4_character_profile"))}</code></p>
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
        if readback.get("receipt_schema_version") == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION:
            boundary = _dict(observations.get("csv_responsibility_boundary"))
            return f"""# Episode 002 YMM4 CSV import gate readback

状態: `{readback.get("status")}` / `actual_ymm4_gui_observation` / `ymm4_csv_import_gate.v1`

明示選択したcharacter profileから生成したderived CSVだけをYMM4 `{env.get("yymm4_version")}`へ読み込み、保存せず終了した。

import済みderived CSV:
`{readback.get("expected_import_path")}`

canonical source（不変）:
`{readback.get("canonical_source_csv")}`

## CSV gate 実観測結果5点

1. **{cue.get("status")}** — scene order: {' -> '.join(str(item) for item in _list(cue.get("scene_order")))}; cue order: {' -> '.join(str(item) for item in _list(cue.get("cue_order")))}。
2. **{voice.get("status")}** — VoiceItemは{voice.get("count")}件。missing={_list(voice.get("missing_cue_ids"))}; duplicate={_list(voice.get("duplicate_cue_ids"))}; reordered={voice.get("reordered")}。
3. **{subtitle.get("status")}** — mapping_dialog_present={subtitle.get("mapping_dialog_present")}; automatic_binding={subtitle.get("automatic_speaker_binding_observed")}; character_counts={subtitle.get("character_counts")}; text/cue match={subtitle.get("speaker_cue_match")}。
4. **{timing.get("status")}** — order_preserved={timing.get("order_preserved")}; duration varianceはinformational。{timing.get("frame_rate")}fps・{timing.get("total_frames")} frames・{timing.get("duration_seconds")}秒。
5. **{boundary.get("status")}** — CSV expected={boundary.get("csv_import_expected_item_families")}; diagnostic project={boundary.get("diagnostic_project_gate")}/{boundary.get("diagnostic_project_status")}; diagnostic item absence is CSV failure={boundary.get("diagnostic_item_absence_is_csv_failure")}。

次gate: `{readback.get("next_gate")}`

Do not render/export. Do not save or write production `.ymmp`. Do not start the diagnostic project. Do not replace real input. Do not approve rights/public/final thumbnail. Do not upload.
"""
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

importするderived CSV:
`{readback.get("expected_import_path")}`

canonical source（上書き禁止）:
`{readback.get("canonical_source_csv")}`

selected character profile:
`{readback.get("selected_yymm4_character_profile")}`

blocker:
{blocker.get("reason")}

## operatorが返す観測5点

1. CSV import後、cue順がS1 -> S2 -> S3、csv_row_1 -> csv_row_9として読めるか。
2. VoiceItemが9 cue分に見えるか、欠落・重複・順序入れ替わりがあるか。
3. mapping dialogが出ず、れいむ行=ゆっくり霊夢、まりさ行=ゆっくり魔理沙として自動bindingされるか。linked subtitle textがspeaker/cueに一致するか。
4. timing orderは仮timingの流れを崩していないか。duration再計算はinformationalとして記録する。
5. CSV責務がVoiceItem + linked subtitleに限定され、ImageItem/独立TextItemのdiagnostic projectがnot_authorized/not_attemptedのままか。

Do not render/export. Do not save or write production `.ymmp`. Do not start the diagnostic project. Do not replace real input. Do not approve rights/public/final thumbnail. Do not upload.
"""


def _render_readme(state: dict[str, Any], readback: dict[str, Any]) -> str:
    if readback.get("observation_mode") == "actual_ymm4_gui_observation":
        if readback.get("receipt_schema_version") == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION:
            state_copy = (
                f"The bounded derived-CSV gate was observed with "
                f"`cue_count_observed={readback.get('cue_count_observed')}` and "
                f"`status={readback.get('status')}`. VoiceItem, automatic character binding, "
                "linked subtitle, timing order, and the CSV responsibility boundary are recorded; "
                "the diagnostic project remained not_authorized/not_attempted."
            )
        else:
            state_copy = (
                f"The historical v1 bounded import was observed with "
                f"`cue_count_observed={readback.get('cue_count_observed')}` and "
                f"`status={readback.get('status')}` under its legacy placeholder contract."
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
- canonical source CSV: `{readback.get("canonical_source_csv")}`
- derived import CSV: `{readback.get("derived_import_csv")}`
- selected character profile: `{readback.get("selected_yymm4_character_profile")}`
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
        if readback.get("receipt_schema_version") == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION:
            observation_copy = (
                "Actual observed means only the bounded derived-CSV import and five CSV-gate "
                "checks occurred. ImageItem or independent TextItem absence is not a CSV failure; "
                "the diagnostic project remains not_authorized/not_attempted. It does not prove "
                f"render, production `.ymmp`, real-input, rights, thumbnail, upload, or public "
                f"readiness. Observation status is `{readback.get('status')}`; recorded deviations: "
                f"{deviation_ids or 'none'}."
            )
        else:
            observation_copy = (
                "This is immutable historical v1 evidence interpreted under its legacy placeholder "
                f"contract. Observation status is `{readback.get('status')}`; recorded deviations: "
                f"{deviation_ids or 'none'}."
            )
    else:
        observation_copy = (
            "Actual observed means actual GUI/manual observation occurred. This package is "
            "blocked/operator-instruction-only until that evidence is returned."
        )
    return f"""# Limitations

Do not launch render/export from this package.
Do not write or save a production `.ymmp` file.
Do not create or start the diagnostic `.ymmp` project without separate authorization.
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
            "The explicit alias profile and derived CSV are ready, but the bounded "
            "YMM4 alias re-observation has not been completed in this artifact."
        )
    else:
        reason = "YMM4 executable was not detected in the checked local paths."
    return {
        "blocker_id": "bounded_yymm4_alias_reobservation_required",
        "status": "blocked_for_actual_observation",
        "reason": reason,
        "operator_action": "Open YMM4, import only the derived CSV, record mapping-dialog/VoiceItem/character/text-order/timing/CSV-boundary results, then close without saving.",
    }


def _csv_candidates(
    paths: dict[str, Path],
    manifest: dict[str, Any],
    repo_root: Path,
    *,
    primary_import_csv: str,
) -> list[dict[str, Any]]:
    candidates: list[Path] = [repo_root / primary_import_csv]
    canonical = str(manifest.get("canonical_source_csv") or "")
    derived = str(manifest.get("primary_import_csv") or "")
    for reference in (derived, canonical):
        if reference:
            candidates.append(repo_root / reference)
    for key in ("ir_bridge_csv", "preview_csv"):
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
