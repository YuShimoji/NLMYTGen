"""Revalidate existing new-banknote YMM4 evidence without mutating it.

The source project, operator result, batch state, and optional observation are
read-only inputs.  This module never launches YMM4, rewrites local evidence,
renders media, or persists machine-specific paths in tracked output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from src.pipeline.new_banknote_yymm4_import_operator_batch import (
    APPROVAL_RECEIPT_FILENAME,
    DEFAULT_PILOT_DIR,
    EXPECTED_DERIVED_COUNTS,
    LOCAL_BATCH_STATE_FILENAME,
    LOCAL_OBSERVATION_FILENAME,
    LOCAL_OUTPUT_DIRNAME,
    LOCAL_PROJECT_FILENAME,
    LOCAL_RESULT_FILENAME,
    PROFILE_VERSION,
    _item_int,
    _load_contract_inputs,
    _same_path,
    _timeline_from_project,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


SUCCESSOR_STATE_ID = (
    "new-banknote-current-lineage-yymm4-evidence-revalidated-v1"
)
REVALIDATION_MODE = "read_only_non_overwriting"

README_FILENAME = "README_EXISTING_YMM4_EVIDENCE_REVALIDATION.md"
RECEIPT_FILENAME = "existing_yymm4_evidence_revalidation_receipt.json"
READBACK_FILENAME = "existing_yymm4_evidence_revalidation_readback.json"
TRACEABILITY_FILENAME = (
    "existing_yymm4_evidence_current_lineage_traceability.json"
)
LIMITATIONS_FILENAME = "existing_yymm4_evidence_limitations.md"

ARTIFACT_FILENAMES = (
    README_FILENAME,
    RECEIPT_FILENAME,
    READBACK_FILENAME,
    TRACEABILITY_FILENAME,
    LIMITATIONS_FILENAME,
)

EXPECTED_STAGE_ORDER = [f"T{index:02d}" for index in range(8)]
EXPECTED_APPROVED_CONTRACT = {
    "cue_count": 9,
    "unique_adopted_claim_count": 15,
    "factual_support_unit_count": 20,
    "claim_edge_count": 21,
    "unsupported_spoken_claim_count": 0,
}

_PRIVATE_PATH_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/]|\\\\[^\\\s]+[\\/]|/home/|/users/)"
)
_UUID_RE = re.compile(
    r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
    r"[0-9a-f]{4}-[0-9a-f]{12}\b"
)
_PROHIBITED_BODY_KEYS = (
    '"raw_text"',
    '"source_body"',
    '"transcript_body"',
)


def _json_bytes(payload: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("JSON_OBJECT_REQUIRED")
    return payload


def _parse_datetime(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def _snapshot(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {
            "exists": False,
            "size_bytes": None,
            "mtime_ns": None,
            "sha256": None,
        }
    stat = path.stat()
    return {
        "exists": True,
        "size_bytes": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "sha256": _sha256(path),
    }


def _snapshot_evidence(paths: Mapping[str, Path]) -> dict[str, dict[str, Any]]:
    return {role: _snapshot(path) for role, path in paths.items()}


def _public_evidence_identity(
    role: str,
    name: str,
    before: Mapping[str, Any],
    after: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "role": role,
        "name": name,
        "present": bool(before.get("exists")),
        "size_bytes": before.get("size_bytes"),
        "sha256": before.get("sha256"),
        "before_after_equal": dict(before) == dict(after),
    }


def _is_within(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
    except ValueError:
        return False
    return True


def _safe_code(exc: BaseException) -> str:
    message = str(exc).splitlines()[0] if str(exc) else type(exc).__name__
    return message.split(":", 1)[0]


def _project_readback(
    project: dict[str, Any],
    expected_rows: list[tuple[str, str]],
) -> dict[str, Any]:
    timeline = _timeline_from_project(project)
    items = _get_timeline_items(project) if timeline else []
    stored_voices = [item for item in items if _item_type(item) == "VoiceItem"]
    ordered_voices = sorted(
        stored_voices,
        key=lambda item: (
            _item_int(item, "Frame", -1),
            stored_voices.index(item),
        ),
    )
    actual_rows = [
        (
            str(item.get("CharacterName") or ""),
            str(item.get("Serif") or ""),
        )
        for item in ordered_voices
    ]
    frames = [_item_int(item, "Frame", -1) for item in ordered_voices]
    lengths = [_item_int(item, "Length", 0) for item in ordered_voices]

    expected_texts = [text for _, text in expected_rows]
    actual_texts = [text for _, text in actual_rows]
    expected_counter = Counter(expected_texts)
    actual_counter = Counter(actual_texts)
    missing_count = sum((expected_counter - actual_counter).values())
    duplicate_count = sum((actual_counter - expected_counter).values())
    reordered = (
        len(actual_texts) == len(expected_texts)
        and actual_counter == expected_counter
        and actual_texts != expected_texts
    )

    video_info = (
        timeline.get("VideoInfo")
        if isinstance(timeline.get("VideoInfo"), dict)
        else {}
    )
    fps_raw = video_info.get("FPS") if video_info else None
    try:
        fps_number = float(fps_raw) if fps_raw is not None else None
    except (TypeError, ValueError):
        fps_number = None
    fps: int | float | None
    if fps_number is not None and fps_number.is_integer():
        fps = int(fps_number)
    else:
        fps = fps_number

    timing_rows = [
        {
            "csv_row_id": f"csv_row_{index}",
            "cue_id": f"cue_{index:03d}",
            "frame": _item_int(item, "Frame", 0),
            "length_frames": _item_int(item, "Length", 0),
            "end_frame": (
                _item_int(item, "Frame", 0)
                + _item_int(item, "Length", 0)
            ),
        }
        for index, item in enumerate(ordered_voices, start=1)
    ]
    item_end = max((row["end_frame"] for row in timing_rows), default=0)
    timeline_frames = _item_int(timeline, "Length", 0) if timeline else 0
    timeline_frames = max(timeline_frames, item_end)
    duration_seconds = (
        round(timeline_frames / fps_number, 6)
        if fps_number is not None and fps_number > 0
        else None
    )

    cue_bindings = []
    for index, expected in enumerate(expected_rows, start=1):
        actual = actual_rows[index - 1] if index <= len(actual_rows) else ("", "")
        cue_bindings.append(
            {
                "cue_id": f"cue_{index:03d}",
                "sequence": index,
                "expected_character": expected[0],
                "actual_character": actual[0],
                "approved_text_sha256": _text_sha256(expected[1]),
                "project_text_sha256": (
                    _text_sha256(actual[1]) if actual[1] else None
                ),
                "character_and_text_exact": actual == expected,
            }
        )

    checks = {
        "one_selected_timeline": bool(timeline),
        "VoiceItem_count_9": len(ordered_voices) == 9,
        "character_counts_3_6": dict(
            Counter(character for character, _ in actual_rows)
        )
        == EXPECTED_DERIVED_COUNTS,
        "exact_text_order": actual_texts == expected_texts,
        "exact_character_text_order": actual_rows == expected_rows,
        "missing_count_zero": missing_count == 0,
        "duplicate_count_zero": duplicate_count == 0,
        "reordered_false": reordered is False,
        "voice_frames_strictly_increasing": (
            len(frames) == 9
            and frames[0] >= 0
            and all(left < right for left, right in zip(frames, frames[1:]))
        ),
        "voice_lengths_positive": (
            len(lengths) == 9 and all(length > 0 for length in lengths)
        ),
        "VoiceItem_only_timeline": len(items) == len(stored_voices),
        "fps_present_and_positive": fps_number is not None and fps_number > 0,
    }
    return {
        "checks": checks,
        "actual_rows": actual_rows,
        "VoiceItem_count": len(ordered_voices),
        "character_counts": dict(
            Counter(character for character, _ in actual_rows)
        ),
        "missing_count": missing_count,
        "duplicate_count": duplicate_count,
        "reordered": reordered,
        "fps": fps,
        "timeline_frames": timeline_frames,
        "duration_seconds": duration_seconds,
        "voice_timing_summary": timing_rows,
        "cue_bindings": cue_bindings,
    }


def _existing_note(
    result: Mapping[str, Any],
    observation: Mapping[str, Any] | None,
) -> tuple[str | None, str]:
    values: list[tuple[str, str]] = []
    if observation is not None:
        for key in (
            "pronunciation_or_clipping_notes",
            "pronunciation_notes",
        ):
            if key in observation and isinstance(observation[key], str):
                values.append(("operator_observation_file", observation[key]))
                break
    operator = result.get("operator_observation")
    if isinstance(operator, dict):
        value = operator.get("pronunciation_or_clipping_notes")
        if isinstance(value, str):
            values.append(("operator_result", value))

    nonempty = [(source, value) for source, value in values if value.strip()]
    if len({value for _, value in nonempty}) > 1:
        raise ValueError("PRONUNCIATION_NOTE_CONFLICT")
    if nonempty:
        source, value = nonempty[0]
        return value, source
    return None, "not_recorded"


def _result_alignment_checks(
    result: Mapping[str, Any],
    readback: Mapping[str, Any],
    project_sha256: str,
    project_size: int,
) -> dict[str, bool]:
    identity = result.get("project_identity")
    verified = result.get("independently_verified")
    checks = result.get("checks")
    operator = result.get("operator_observation")
    if not isinstance(identity, dict):
        identity = {}
    if not isinstance(verified, dict):
        verified = {}
    if not isinstance(checks, dict):
        checks = {}
    if not isinstance(operator, dict):
        operator = {}
    return {
        "predecessor_result_status_success": result.get("status") == "success",
        "predecessor_failed_checks_empty": result.get("failed_checks") == [],
        "predecessor_checks_all_true": bool(checks)
        and all(value is True for value in checks.values()),
        "result_project_sha256_matches": identity.get("sha256") == project_sha256,
        "result_project_size_matches": identity.get("size_bytes") == project_size,
        "result_recorded_exact_target": identity.get("exact_target_matches") is True,
        "result_recorded_embedded_path_match": (
            identity.get("embedded_file_path_matches") is True
        ),
        "result_mapping_confirmation_observed": (
            operator.get(
                "no_mapping_error_update_or_character_mismatch_confirmed"
            )
            is True
        ),
        "result_VoiceItem_count_matches": (
            verified.get("VoiceItem_count") == readback.get("VoiceItem_count")
        ),
        "result_character_counts_match": (
            verified.get("character_counts") == readback.get("character_counts")
        ),
        "result_text_order_matches": (
            verified.get("exact_text_order")
            == readback.get("checks", {}).get("exact_text_order")
            == True
        ),
        "result_character_text_order_matches": (
            verified.get("exact_character_text_order")
            == readback.get("checks", {}).get("exact_character_text_order")
            == True
        ),
        "result_missing_count_matches": (
            verified.get("missing_count") == readback.get("missing_count") == 0
        ),
        "result_duplicate_count_matches": (
            verified.get("duplicate_count")
            == readback.get("duplicate_count")
            == 0
        ),
        "result_reordered_matches": (
            verified.get("reordered") == readback.get("reordered") is False
        ),
        "result_fps_matches": verified.get("fps") == readback.get("fps"),
        "result_timeline_frames_match": (
            verified.get("timeline_frames") == readback.get("timeline_frames")
        ),
        "result_duration_matches": (
            verified.get("duration_seconds")
            == readback.get("duration_seconds")
        ),
        "result_voice_timing_matches": (
            verified.get("voice_timing_summary")
            == readback.get("voice_timing_summary")
        ),
    }


def _tracked_output_is_private(payload: bytes) -> bool:
    text = payload.decode("utf-8", errors="replace")
    return bool(
        _PRIVATE_PATH_RE.search(text)
        or _UUID_RE.search(text)
        or "notebooklm.google.com" in text.lower()
        or any(token in text for token in _PROHIBITED_BODY_KEYS)
    )


def inspect_existing_yymm4_evidence(
    *,
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
    project_path: str | Path,
    result_path: str | Path,
    batch_state_path: str | Path,
    observation_path: str | Path | None = None,
) -> dict[str, Any]:
    """Read and validate existing evidence without writing any file."""
    pilot = Path(pilot_dir).resolve()
    project_source = Path(project_path).resolve()
    result_source = Path(result_path).resolve()
    batch_source = Path(batch_state_path).resolve()
    observation_source = (
        Path(observation_path).resolve() if observation_path is not None else None
    )
    evidence_paths = {
        "project": project_source,
        "result": result_source,
        "batch_state": batch_source,
    }
    if observation_source is not None:
        evidence_paths["observation"] = observation_source

    before = _snapshot_evidence(evidence_paths)
    checks: dict[str, bool] = {
        "required_project_present": before["project"]["exists"],
        "required_result_present": before["result"]["exists"],
        "required_batch_state_present": before["batch_state"]["exists"],
    }
    failed: list[str] = []
    warnings: list[str] = []
    inputs: dict[str, Any] | None = None
    result: dict[str, Any] | None = None
    batch: dict[str, Any] | None = None
    observation: dict[str, Any] | None = None
    project: dict[str, Any] | None = None
    readback: dict[str, Any] | None = None
    ledger: dict[str, Any] | None = None
    lineage_readback: dict[str, Any] | None = None
    cue_matrix: dict[str, Any] | None = None
    note: str | None = None
    note_source = "not_recorded"

    if all(checks.values()):
        try:
            inputs = _load_contract_inputs(pilot)
            ledger = _read_json(pilot / "content_transformation_ledger.json")
            lineage_readback = _read_json(pilot / "content_lineage_readback.json")
            cue_matrix = _read_json(pilot / "cue_lineage_matrix.json")
            checks["current_approval_and_lineage_lock_valid"] = True
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            checks["current_approval_and_lineage_lock_valid"] = False
            failed.append(f"current_contract_invalid:{_safe_code(exc)}")

    if checks.get("current_approval_and_lineage_lock_valid"):
        try:
            result = _read_json(result_source)
            batch = _read_json(batch_source)
            if observation_source is not None:
                observation = _read_json(observation_source)
            project = load_ymmp(project_source)
            readback = _project_readback(project, list(inputs["derived_rows"]))
            note, note_source = _existing_note(result, observation)
            checks["existing_evidence_parse_pass"] = True
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            checks["existing_evidence_parse_pass"] = False
            failed.append(f"existing_evidence_parse_failed:{_safe_code(exc)}")

    after = _snapshot_evidence(evidence_paths)
    checks["source_evidence_before_after_equal"] = before == after

    for name, passed in list(checks.items()):
        if passed is not True and name not in failed:
            failed.append(name)

    if (
        inputs is not None
        and result is not None
        and batch is not None
        and project is not None
        and readback is not None
        and ledger is not None
        and lineage_readback is not None
        and cue_matrix is not None
    ):
        approval = inputs["approval_receipt"]
        approval_scope = approval.get("approval_scope")
        approval_contract = approval.get("approved_contract")
        if not isinstance(approval_scope, dict):
            approval_scope = {}
        if not isinstance(approval_contract, dict):
            approval_contract = {}
        stage_order = ledger.get("stage_order")
        result_operator = result.get("operator_observation")
        result_identity = result.get("project_identity")
        if not isinstance(result_operator, dict):
            result_operator = {}
        if not isinstance(result_identity, dict):
            result_identity = {}

        current_checks = {
            "approval_receipt_valid": (
                approval.get("status") == "valid"
                and approval.get("receipt_id")
                == "new-banknote-script-option-a-approval-v1"
            ),
            "approval_contract_exact": approval_contract
            == EXPECTED_APPROVED_CONTRACT,
            "scene_allocation_2_4_3": approval_scope.get("scene_allocation")
            == {"S1": 2, "S2": 4, "S3": 3},
            "canonical_speaker_counts_3_6": approval_scope.get(
                "canonical_speaker_counts"
            )
            == {"れいむ": 3, "まりさ": 6},
            "lineage_readback_passed": (
                lineage_readback.get("status") == "passed"
                and all(
                    value is True
                    for value in dict(
                        lineage_readback.get("checks") or {}
                    ).values()
                )
            ),
            "stage_coverage_T00_T07": stage_order == EXPECTED_STAGE_ORDER,
            "cue_matrix_9_15_20_21": (
                cue_matrix.get("cue_coverage") == "9/9"
                and cue_matrix.get("unique_adopted_claim_count") == 15
                and cue_matrix.get("factual_support_unit_count") == 20
                and cue_matrix.get("claim_edge_count") == 21
            ),
            "token_level_attribution_not_claimed": (
                cue_matrix.get("token_level_attribution_claimed") is False
            ),
        }
        checks.update(current_checks)
        checks.update(readback["checks"])

        embedded = str(project.get("FilePath") or "").strip()
        result_expected = str(result_identity.get("expected_repo_relative_path") or "")
        expected_role_suffix = (
            f"{LOCAL_OUTPUT_DIRNAME}/{LOCAL_PROJECT_FILENAME}"
        )
        binding_checks = {
            "project_embedded_path_matches_source": bool(embedded)
            and _same_path(Path(embedded), project_source),
            "result_expected_role_matches": result_expected.replace(
                "\\", "/"
            ).endswith(expected_role_suffix),
            "batch_project_target_matches_source": bool(
                batch.get("target_project")
            )
            and _same_path(Path(str(batch["target_project"])), project_source),
            "batch_result_target_matches_source": bool(batch.get("target_result"))
            and _same_path(Path(str(batch["target_result"])), result_source),
        }
        checks.update(binding_checks)

        result_checks = _result_alignment_checks(
            result,
            readback,
            str(before["project"]["sha256"]),
            int(before["project"]["size_bytes"]),
        )
        checks.update(result_checks)

        batch_started = _parse_datetime(batch.get("batch_not_before_utc"))
        result_started = _parse_datetime(result.get("batch_not_before_utc"))
        result_collected = _parse_datetime(result.get("collected_at_utc"))
        project_modified = datetime.fromtimestamp(
            int(before["project"]["mtime_ns"]) / 1_000_000_000,
            timezone.utc,
        )
        temporal_checks = {
            "batch_id_matches": batch.get("batch_id")
            == "new-banknote-yymm4-import-observation-v1",
            "batch_start_matches_result": (
                batch_started is not None
                and result_started is not None
                and batch_started == result_started
            ),
            "project_not_older_than_batch": (
                batch_started is not None and project_modified >= batch_started
            ),
            "result_collected_after_project": (
                result_collected is not None
                and result_collected >= project_modified
            ),
            "batch_and_result_yymm4_version_match": (
                batch.get("yymm4_product_version")
                == result_operator.get("yymm4_product_version")
            ),
            "batch_and_result_profile_version_match": (
                batch.get("profile_observation_version")
                == result_operator.get("profile_observation_version")
                == PROFILE_VERSION
            ),
        }
        checks.update(temporal_checks)

        yymm4_version = str(batch.get("yymm4_product_version") or "")
        profile_version = str(batch.get("profile_observation_version") or "")
        profile_match = yymm4_version.startswith(profile_version)
        if not profile_match:
            warnings.append("YMM4_PROFILE_VERSION_MISMATCH_WARNING_ONLY")

        if note is not None:
            note_bytes = _json_bytes({"note": note})
            checks["pronunciation_note_sanitized"] = not _tracked_output_is_private(
                note_bytes
            )
            pronunciation_status = "observed_note_present"
            clipping_status = "observed_note_present"
            pronunciation_grade = "observed"
        else:
            checks["pronunciation_note_sanitized"] = True
            pronunciation_status = "unknown"
            clipping_status = "unknown"
            pronunciation_grade = "unknown"

        for name, passed in checks.items():
            if passed is not True and name not in failed:
                failed.append(name)

        evidence_identities = {
            role: _public_evidence_identity(
                role,
                evidence_paths[role].name,
                before[role],
                after[role],
            )
            for role in evidence_paths
        }
        receipt = {
            "schema_version": (
                "new_banknote_yymm4_existing_evidence_revalidation.receipt.v1"
            ),
            "status": "accepted" if not failed else "failed",
            "revalidation_mode": REVALIDATION_MODE,
            "successor_state_id": SUCCESSOR_STATE_ID,
            "current_approval": {
                "receipt_id": approval.get("receipt_id"),
                "receipt_sha256": inputs["lineage_hashes"][
                    APPROVAL_RECEIPT_FILENAME
                ],
                "status": approval.get("status"),
                "approved_commit": approval.get("approved_commit"),
                "approved_file_hashes": inputs["approved_hashes"],
                "approved_content_modified": False,
            },
            "current_lineage": {
                "status": "passed",
                "artifact_hashes": inputs["lineage_hashes"],
                "stage_coverage": EXPECTED_STAGE_ORDER,
                "cue_count": 9,
                "scene_allocation": {"S1": 2, "S2": 4, "S3": 3},
                "canonical_speaker_counts": {"れいむ": 3, "まりさ": 6},
                "adopted_claim_count": 15,
                "factual_support_unit_count": 20,
                "claim_edge_count": 21,
                "unsupported_spoken_claim_count": 0,
            },
            "local_evidence": evidence_identities,
            "project_result_binding": binding_checks | result_checks,
            "structural_readback": {
                "VoiceItem_count": readback["VoiceItem_count"],
                "character_counts": readback["character_counts"],
                "exact_text_order": readback["checks"]["exact_text_order"],
                "exact_character_text_order": readback["checks"][
                    "exact_character_text_order"
                ],
                "missing_count": readback["missing_count"],
                "duplicate_count": readback["duplicate_count"],
                "reordered": readback["reordered"],
                "fps": readback["fps"],
                "timeline_frames": readback["timeline_frames"],
                "duration_seconds": readback["duration_seconds"],
                "voice_timing_summary": readback["voice_timing_summary"],
            },
            "version_readback": {
                "yymm4_product_version": yymm4_version,
                "profile_observation_version": profile_version,
                "profile_version_match": profile_match,
                "mismatch_policy": "warning_only",
            },
            "pronunciation_and_clipping": {
                "pronunciation_status": pronunciation_status,
                "clipping_status": clipping_status,
                "rhythm_status": "unknown",
                "existing_note_present": note is not None,
                "existing_note": note,
                "note_source": note_source,
                "evidence_grade": pronunciation_grade,
                "acceptance_claimed": False,
            },
            "before_after_immutability": {
                "status": "passed" if before == after else "failed",
                "all_source_evidence_unchanged": before == after,
                "compared_fields": ["exists", "size_bytes", "mtime_ns", "sha256"],
            },
            "predecessor_evidence_identity": {
                "operator_result_schema": result.get("schema_version"),
                "operator_result_status": result.get("status"),
                "operator_result_sha256": before["result"]["sha256"],
                "project_sha256": before["project"]["sha256"],
                "batch_state_sha256": before["batch_state"]["sha256"],
                "collected_at_utc": result.get("collected_at_utc"),
            },
            "execution_boundary": {
                "yymm4_launched": False,
                "yymm4_rerun": False,
                "computer_use_invoked": False,
                "render_or_media_generated": False,
                "source_evidence_written": False,
            },
            "evidence_boundary": {
                "current_lineage_compatibility_verified": not failed,
                "internal_import_observation_only": True,
                "pronunciation_or_clipping_acceptance": False,
                "production_project": False,
                "rights_or_publication_approval": False,
                "private_path_tracked": False,
                "local_binary_tracked": False,
            },
            "checks": checks,
            "failed_checks": failed,
            "warnings": warnings,
        }
        return {
            "status": "passed" if not failed else "failed",
            "checks": checks,
            "failed_checks": failed,
            "warnings": warnings,
            "receipt": receipt,
            "cue_bindings": readback["cue_bindings"],
        }

    return {
        "status": "failed",
        "checks": checks,
        "failed_checks": list(dict.fromkeys(failed)),
        "warnings": warnings,
        "receipt": None,
        "cue_bindings": [],
    }


def _readme(receipt: Mapping[str, Any]) -> str:
    structural = receipt["structural_readback"]
    version = receipt["version_readback"]
    pronunciation = receipt["pronunciation_and_clipping"]
    return f"""# Existing YMM4 Evidence Revalidation

> **READ-ONLY REVALIDATION — INTERNAL IMPORT OBSERVATION — NON-PRODUCTION**

このpackageは、既存のignored YMM4 project、operator result、batch stateを
削除・移動・上書きせず、現在のhuman approvalとT00–T07 content lineageへ
再接続したsanitized successor evidenceです。YMM4は再実行していません。

## 結論

- status: `{receipt['status']}`
- mode: `{REVALIDATION_MODE}`
- VoiceItems: `{structural['VoiceItem_count']}`
- ゆっくり霊夢 / ゆっくり魔理沙: `3 / 6`
- exact text / order: `{str(structural['exact_character_text_order']).lower()}`
- missing / duplicate / reordered: `{structural['missing_count']} / {structural['duplicate_count']} / {str(structural['reordered']).lower()}`
- fps / frames / duration: `{structural['fps']} / {structural['timeline_frames']} / {structural['duration_seconds']}`
- source evidence before/after: `unchanged`

既存resultとcurrent parserのproject readbackは、project hash、9 VoiceItems、3/6、
本文、順序、timingで一致しました。approved script、CSV、claim/source、lineageは
変更していません。

## 音声品質の境界

pronunciationは`{pronunciation['pronunciation_status']}`、clippingは
`{pronunciation['clipping_status']}`、rhythmは`{pronunciation['rhythm_status']}`です。
構造的なimport成功から音声品質を推定せず、acceptanceは主張しません。

## Version warning

existing YMM4は`{version['yymm4_product_version']}`、profile observationは
`{version['profile_observation_version']}`です。差分はwarning debtであり、
現在のhash/text/order compatibilityを自動で失敗にはしません。

## 読む順序

1. `{RECEIPT_FILENAME}` — current lockとexisting evidenceの受入正本
2. `{READBACK_FILENAME}` — checksとmetricの短いreadback
3. `{TRACEABILITY_FILENAME}` — approval/lineage/cue接続
4. `{LIMITATIONS_FILENAME}` — 未解消境界

## 次のgate

次は分岐したnew-banknote successor branchesのintegration auditです。このpackageは
branch integration、visual route選択、render、production、rights、publication、
master integrationを承認しません。
"""


def _limitations() -> str:
    return """# Existing YMM4 Evidence Revalidation — Limitations

このpackageが受け入れるのは、既存same-machine import evidenceとcurrent
approval/content-lineage lockの互換性だけです。

| debt | state | impact | owner / revisit trigger |
| --- | --- | --- | --- |
| pronunciation / rhythm / clipping | unknown | structural import successを音声受入に拡張できない | human audio reviewer when the successor integration requires audio acceptance |
| divergent visual/provenance branch | not integrated | visual decisionへ直接進めない | future `new-banknote-successor-integration-audit-v1` |
| S04 generation-time binary / exact S05 identity | unresolved | historical provenance precisionが限定される | provenance owner when exact source identity appears |
| token-level authorship | unavailable | clause/meaning-unitを越えるauthorship比率を主張できない | only revisit with new contemporaneous evidence |

YMM4 rerun、render、production、rights、publication、master integrationは
このrevalidationに含まれません。
"""


def _render_artifacts(outcome: Mapping[str, Any]) -> dict[str, bytes]:
    receipt = outcome.get("receipt")
    if outcome.get("status") != "passed" or not isinstance(receipt, dict):
        failed = ",".join(str(item) for item in outcome.get("failed_checks", []))
        raise ValueError(f"EXISTING_EVIDENCE_REVALIDATION_FAILED:{failed}")

    receipt_bytes = _json_bytes(receipt)
    readback = {
        "schema_version": (
            "new_banknote_yymm4_existing_evidence_revalidation.readback.v1"
        ),
        "status": "passed",
        "successor_state_id": SUCCESSOR_STATE_ID,
        "receipt_sha256": _sha256_bytes(receipt_bytes),
        "checks": outcome["checks"],
        "failed_checks": [],
        "warnings": outcome["warnings"],
        "metrics": receipt["structural_readback"],
        "evidence_grades": {
            "approval_lineage_and_hashes": "verified",
            "existing_operator_confirmation": "observed",
            "current_compatibility_conclusion": "inferred_from_verified_inputs",
            "pronunciation_rhythm_clipping": receipt[
                "pronunciation_and_clipping"
            ]["evidence_grade"],
        },
    }
    traceability = {
        "schema_version": (
            "new_banknote_yymm4_existing_evidence_revalidation.traceability.v1"
        ),
        "status": "passed",
        "successor_state_id": SUCCESSOR_STATE_ID,
        "approval_receipt": {
            "receipt_id": receipt["current_approval"]["receipt_id"],
            "sha256": receipt["current_approval"]["receipt_sha256"],
            "approved_commit": receipt["current_approval"]["approved_commit"],
        },
        "lineage_artifact_hashes": receipt["current_lineage"][
            "artifact_hashes"
        ],
        "stage_coverage": receipt["current_lineage"]["stage_coverage"],
        "existing_evidence_hashes": {
            role: value["sha256"]
            for role, value in receipt["local_evidence"].items()
            if value["present"]
        },
        "cue_bindings": outcome["cue_bindings"],
        "approved_content_modified": False,
        "source_evidence_modified": False,
    }
    artifacts = {
        README_FILENAME: _readme(receipt).encode("utf-8"),
        RECEIPT_FILENAME: receipt_bytes,
        READBACK_FILENAME: _json_bytes(readback),
        TRACEABILITY_FILENAME: _json_bytes(traceability),
        LIMITATIONS_FILENAME: _limitations().encode("utf-8"),
    }
    combined = b"\n".join(artifacts.values())
    if _tracked_output_is_private(combined):
        raise ValueError("TRACKED_REVALIDATION_OUTPUT_PRIVACY_FAILURE")
    return artifacts


def render_existing_yymm4_evidence_revalidation_artifacts(
    *,
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
    project_path: str | Path,
    result_path: str | Path,
    batch_state_path: str | Path,
    observation_path: str | Path | None = None,
) -> dict[str, bytes]:
    outcome = inspect_existing_yymm4_evidence(
        pilot_dir=pilot_dir,
        project_path=project_path,
        result_path=result_path,
        batch_state_path=batch_state_path,
        observation_path=observation_path,
    )
    return _render_artifacts(outcome)


def build_existing_yymm4_evidence_revalidation(
    *,
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
    project_path: str | Path,
    result_path: str | Path,
    batch_state_path: str | Path,
    output_dir: str | Path,
    observation_path: str | Path | None = None,
) -> dict[str, Any]:
    """Write deterministic sanitized artifacts outside the evidence directory."""
    project = Path(project_path).resolve()
    result = Path(result_path).resolve()
    batch = Path(batch_state_path).resolve()
    output = Path(output_dir).resolve()
    evidence_directory = project.parent
    if result.parent != evidence_directory or batch.parent != evidence_directory:
        return {
            "status": "failed",
            "failed_checks": ["EVIDENCE_SOURCES_MUST_SHARE_DIRECTORY"],
            "written_files": [],
        }
    if _is_within(output, evidence_directory):
        return {
            "status": "failed",
            "failed_checks": ["OUTPUT_DIRECTORY_OVERLAPS_SOURCE_EVIDENCE"],
            "written_files": [],
        }

    outcome = inspect_existing_yymm4_evidence(
        pilot_dir=pilot_dir,
        project_path=project,
        result_path=result,
        batch_state_path=batch,
        observation_path=observation_path,
    )
    if outcome["status"] != "passed":
        return {
            **outcome,
            "written_files": [],
        }
    artifacts = _render_artifacts(outcome)
    output.mkdir(parents=True, exist_ok=True)
    for name, data in artifacts.items():
        (output / name).write_bytes(data)
    return {
        "status": "passed",
        "successor_state_id": SUCCESSOR_STATE_ID,
        "written_files": sorted(artifacts),
        "checks": outcome["checks"],
        "warnings": outcome["warnings"],
        "source_evidence_written": False,
        "yymm4_launched": False,
        "computer_use_invoked": False,
        "render_or_media_generated": False,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", type=Path, default=DEFAULT_PILOT_DIR)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--batch-state", type=Path, required=True)
    parser.add_argument("--observation", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    outcome = build_existing_yymm4_evidence_revalidation(
        pilot_dir=args.pilot,
        project_path=args.project,
        result_path=args.result,
        batch_state_path=args.batch_state,
        observation_path=args.observation,
        output_dir=args.output_dir,
    )
    public = {
        "status": outcome.get("status"),
        "successor_state_id": outcome.get("successor_state_id"),
        "written_files": outcome.get("written_files", []),
        "failed_checks": outcome.get("failed_checks", []),
        "warnings": outcome.get("warnings", []),
        "source_evidence_written": outcome.get("source_evidence_written", False),
        "yymm4_launched": False,
        "computer_use_invoked": False,
        "render_or_media_generated": False,
    }
    print(_json_bytes(public).decode("utf-8"), end="")
    return 0 if outcome.get("status") == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
