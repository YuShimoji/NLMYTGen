"""Ingest immutable YMM4 import evidence and build a visual decision packet.

This module is intentionally headless.  It reads the ignored operator result
and imported project without mutating either one, promotes only sanitized
facts, and renders a deterministic three-route review packet.  It never
launches YMM4, creates a visual project, downloads assets, or renders media.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import posixpath
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from src.pipeline.new_banknote_yymm4_import_operator_batch import (
    APPROVED_FILES,
    EXPECTED_APPROVED_HASHES,
    EXPECTED_DERIVED_COUNTS,
    LOCAL_BATCH_STATE_FILENAME,
    LOCAL_OUTPUT_DIRNAME,
    LOCAL_PROJECT_FILENAME,
    LOCAL_RESULT_FILENAME,
    PILOT_RELATIVE,
    _get_timeline_items,
    _item_int,
    _item_type,
    _same_path,
    _timeline_from_project,
)
from src.pipeline.ymmp_patch import load_ymmp


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PILOT_DIR = REPO_ROOT / PILOT_RELATIVE

TARGET_STATE_ID = "new-banknote-yymm4-import-observed-visual-decision-ready-v1"
PRODUCT_STATE = "new-banknote-yymm4-import-observed-visual-direction-review-ready"
PRODUCT_GATE = "human-visual-direction-selection"
RECOMMENDED_NEXT = "select-new-banknote-visual-direction"

IMPORT_README_FILENAME = "README_YMM4_IMPORT_OBSERVATION.md"
IMPORT_RECEIPT_FILENAME = "yymm4_import_observation_receipt.json"
IMPORT_READBACK_FILENAME = "yymm4_import_observation_readback.json"
IMPORT_TRACEABILITY_FILENAME = (
    "yymm4_import_source_to_project_traceability.json"
)
IMPORT_LIMITATIONS_FILENAME = "yymm4_import_observation_limitations.md"

VISUAL_DIRNAME = "visual_scene_decision"
VISUAL_README_FILENAME = "README_VISUAL_SCENE_DECISION.md"
VISUAL_OPTIONS_FILENAME = "visual_direction_options.json"
RECOMMENDED_DIRECTION_FILENAME = "recommended_visual_direction.json"
SCRIPT_BEAT_FILENAME = "script_beat_ir.json"
SCENE_PLAN_FILENAME = "scene_layout_plan.json"
MOTION_PLAN_FILENAME = "motion_beat_plan.json"
ASSET_MATRIX_FILENAME = "asset_rights_matrix.json"
YMM4_CONTRACT_FILENAME = "yymm4_visual_project_contract.json"
VISUAL_REVIEW_FILENAME = "visual_review_sheet.md"
HTML_BOARD_FILENAME = "visual_direction_board.html"
HTML_READBACK_FILENAME = "visual_direction_board_readback.json"
VISUAL_LIMITATIONS_FILENAME = "limitations.md"

REQUIRED_RESULT_CHECKS = {
    "exact_local_project_target",
    "operator_confirmed_no_mapping_error_update_or_character_mismatch",
    "local_project_exists",
    "local_project_fresh",
    "project_parse_pass",
    "one_selected_timeline",
    "embedded_project_target_matches",
    "VoiceItem_count_9",
    "character_counts_3_6",
    "exact_text_order",
    "exact_character_text_order",
    "missing_count_zero",
    "duplicate_count_zero",
    "reordered_false",
    "voice_frames_strictly_increasing",
    "voice_lengths_positive",
    "VoiceItem_only_timeline",
}
ALLOWED_ADDITIONAL_RESULT_CHECKS = {
    "approval_and_content_lineage_lock_valid",
    "pronunciation_or_clipping_notes_valid",
    "explicit_observation_json_when_cli_used",
}

ALLOWED_SOURCE_IDS = {"V02", "V06", "V07", "V13"}
EXCLUDED_VISUAL_CLAIM_IDS = {"claim_158"}
EXPECTED_ROUTE_IDS = [
    "route_A_security_inspection_lab",
    "route_B_everyday_verification",
    "route_C_design_evolution",
]

_PRIVATE_OR_EXTERNAL_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/]|\\\\[^\\\s]+[\\/]|/home/|/users/|"
    r"https?://|file://|www\.)"
)


def _json_bytes(payload: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False)
        + "\n"
    ).encode("utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"EXPECTED_JSON_OBJECT:{path.name}")
    return payload


def _write_bytes(path: Path, data: bytes) -> bool:
    if path.is_file() and path.read_bytes() == data:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return True


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _mtime_utc(path: Path) -> str:
    return datetime.fromtimestamp(
        path.stat().st_mtime, timezone.utc
    ).isoformat()


def _parse_utc(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _fingerprint(path: Path) -> dict[str, Any]:
    return {
        "sha256": _sha256(path),
        "size_bytes": path.stat().st_size,
        "modified_at_utc": _mtime_utc(path),
    }


def _csv_rows(path: Path) -> list[tuple[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [tuple(row) for row in csv.reader(handle)]
    if any(len(row) != 2 for row in rows):
        raise ValueError("DERIVED_CSV_MUST_BE_HEADERLESS_TWO_COLUMN")
    return [(str(character), str(text)) for character, text in rows]


def _compact_row_hash(rows: Sequence[tuple[str, str]]) -> str:
    payload = json.dumps(
        [list(row) for row in rows],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _actual_approved_hashes(pilot: Path) -> dict[str, str]:
    return {name: _sha256(pilot / name) for name in APPROVED_FILES}


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ValueError(code)


def _cue_boundaries() -> dict[str, str]:
    return {
        "cue_001": (
            "2024年発行だけを扱う。発行目的、経済効果、政策意図は示さない。"
        ),
        "cue_002": (
            "複数技術とユニバーサルデザインの採用意図まで。効果、優位性、"
            "新規性の実証は主張しない。"
        ),
        "cue_003": (
            "透過光で細かな模様が見えることだけを抽象化する。実券の肖像、"
            "位置、寸法、製法を再現しない。"
        ),
        "cue_004": (
            "角度で三次元の肖像が回転して見える現象を非肖像シルエットで示す。"
            "実際の形状、位置、箔模様は示さない。"
        ),
        "cue_005": (
            "額面数字などの盛り上がりと触感だけを概念化する。版、工程、"
            "インキ高さなど再現可能な製造情報を示さない。"
        ),
        "cue_006": (
            "NIPPONGINKOを単一の模式ラベルとして示す。実寸、密度、位置、"
            "周辺模様は再現せず、複写は困難という範囲に留める。"
        ),
        "cue_007": (
            "11本の斜線と券種別の位置差を模式図で示す。座標、角度、太さ、"
            "性能評価は示さない。"
        ),
        "cue_008": (
            "E券より大きい額面数字、F券内の一万円券と千円券のホログラム差、"
            "千円券中央の橙色グラデーションだけを縮尺外の抽象図で示す。"
        ),
        "cue_009": (
            "透かす・触る・傾ける・ルーペで見るを確認行動として示す。"
            "真贋保証や完全な判定手順とは扱わない。"
        ),
    }


def audit_new_banknote_yymm4_import_observation(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
    *,
    user_reported_terminal_status: str = "success",
) -> dict[str, Any]:
    """Read and verify existing local evidence without changing its bytes."""
    pilot = Path(pilot_dir).resolve()
    result_path = pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_RESULT_FILENAME
    project_path = pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_PROJECT_FILENAME
    batch_path = pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_BATCH_STATE_FILENAME
    paths = [result_path, project_path, batch_path]
    for path in paths:
        _require(path.is_file(), f"MISSING_LOCAL_EVIDENCE:{path.name}")

    before = {path.name: _fingerprint(path) for path in paths}
    result = _read_json(result_path)
    batch = _read_json(batch_path)

    _require(
        result.get("schema_version")
        == "new_banknote_yymm4_import_observation.operator_result.v1",
        "UNEXPECTED_OPERATOR_RESULT_SCHEMA",
    )
    _require(result.get("status") == "success", "OPERATOR_RESULT_NOT_SUCCESS")
    _require(result.get("failed_checks") == [], "OPERATOR_RESULT_HAS_FAILURES")
    result_checks = result.get("checks")
    _require(isinstance(result_checks, dict), "RESULT_CHECKS_MISSING")
    result_check_names = set(result_checks)
    _require(
        REQUIRED_RESULT_CHECKS <= result_check_names
        and result_check_names
        <= REQUIRED_RESULT_CHECKS | ALLOWED_ADDITIONAL_RESULT_CHECKS,
        "RESULT_CHECK_SET_DRIFT",
    )
    _require(all(value is True for value in result_checks.values()), "RESULT_CHECK_FAILED")

    observation = result.get("operator_observation")
    _require(isinstance(observation, dict), "OPERATOR_OBSERVATION_MISSING")
    _require(
        observation.get(
            "no_mapping_error_update_or_character_mismatch_confirmed"
        )
        is True,
        "OPERATOR_CONFIRMATION_MISSING",
    )
    _require(
        observation.get("mapping_dialog_or_error_observed") is False,
        "OPERATOR_REPORTED_MAPPING_OR_ERROR",
    )

    expected_project_relative = (
        f"{PILOT_RELATIVE.as_posix()}/{LOCAL_OUTPUT_DIRNAME}/"
        f"{LOCAL_PROJECT_FILENAME}"
    )
    expected_result_relative = (
        f"{PILOT_RELATIVE.as_posix()}/{LOCAL_OUTPUT_DIRNAME}/"
        f"{LOCAL_RESULT_FILENAME}"
    )
    expected_batch_relative = (
        f"{PILOT_RELATIVE.as_posix()}/{LOCAL_OUTPUT_DIRNAME}/"
        f"{LOCAL_BATCH_STATE_FILENAME}"
    )
    project_identity = result.get("project_identity")
    _require(isinstance(project_identity, dict), "PROJECT_IDENTITY_MISSING")
    _require(
        project_identity.get("expected_repo_relative_path")
        == expected_project_relative,
        "RESULT_EXPECTED_PROJECT_IDENTITY_DRIFT",
    )
    _require(
        _same_path(Path(str(project_identity.get("actual_path"))), project_path),
        "RESULT_ACTUAL_PROJECT_TARGET_DRIFT",
    )
    _require(project_identity.get("exact_target_matches") is True, "RESULT_TARGET_MISMATCH")
    _require(
        project_identity.get("embedded_file_path_matches") is True,
        "RESULT_EMBEDDED_TARGET_MISMATCH",
    )

    _require(
        batch.get("schema_version")
        == "new_banknote_yymm4_import_operator_batch.local.v1",
        "UNEXPECTED_BATCH_STATE_SCHEMA",
    )
    _require(
        _same_path(Path(str(batch.get("target_project"))), project_path),
        "BATCH_PROJECT_TARGET_DRIFT",
    )
    _require(
        _same_path(Path(str(batch.get("target_result"))), result_path),
        "BATCH_RESULT_TARGET_DRIFT",
    )
    _require(
        batch.get("yymm4_product_version")
        == observation.get("yymm4_product_version"),
        "YMM4_VERSION_EVIDENCE_DRIFT",
    )
    threshold = _parse_utc(str(result.get("batch_not_before_utc")))
    _require(
        _parse_utc(str(batch.get("batch_not_before_utc"))) == threshold,
        "BATCH_THRESHOLD_DRIFT",
    )

    actual_approved_hashes = _actual_approved_hashes(pilot)
    _require(
        actual_approved_hashes == EXPECTED_APPROVED_HASHES,
        "APPROVED_SCRIPT_IDENTITY_DRIFT",
    )

    derived_rows = _csv_rows(pilot / "derived_yymm4_import.csv")
    _require(len(derived_rows) == 9, "DERIVED_CSV_ROW_COUNT_DRIFT")
    _require(
        dict(Counter(character for character, _ in derived_rows))
        == EXPECTED_DERIVED_COUNTS,
        "DERIVED_CSV_CHARACTER_COUNT_DRIFT",
    )

    project = load_ymmp(project_path)
    _require(isinstance(project, dict), "PROJECT_PARSE_FAILED")
    _require(
        bool(project.get("FilePath"))
        and _same_path(Path(str(project.get("FilePath"))), project_path),
        "PROJECT_EMBEDDED_TARGET_DRIFT",
    )
    timeline = _timeline_from_project(project)
    _require(bool(timeline), "PROJECT_TIMELINE_INVALID")
    items = _get_timeline_items(project)
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
    _require(len(items) == len(ordered_voices), "UNEXPECTED_NON_VOICE_ITEM")
    _require(len(ordered_voices) == 9, "VOICEITEM_COUNT_DRIFT")
    _require(
        dict(Counter(character for character, _ in actual_rows))
        == EXPECTED_DERIVED_COUNTS,
        "PROJECT_CHARACTER_COUNT_DRIFT",
    )
    _require(actual_rows == derived_rows, "PROJECT_TEXT_OR_ORDER_DRIFT")
    _require(
        frames[0] >= 0
        and all(left < right for left, right in zip(frames, frames[1:])),
        "PROJECT_FRAME_ORDER_DRIFT",
    )
    _require(all(length > 0 for length in lengths), "PROJECT_VOICE_LENGTH_INVALID")

    expected_texts = [text for _, text in derived_rows]
    actual_texts = [text for _, text in actual_rows]
    missing_count = sum(
        (Counter(expected_texts) - Counter(actual_texts)).values()
    )
    duplicate_count = sum(
        (Counter(actual_texts) - Counter(expected_texts)).values()
    )
    _require(missing_count == 0, "PROJECT_MISSING_TEXT")
    _require(duplicate_count == 0, "PROJECT_DUPLICATE_TEXT")

    project_fingerprint = before[LOCAL_PROJECT_FILENAME]
    _require(
        project_identity.get("sha256") == project_fingerprint["sha256"],
        "RESULT_PROJECT_HASH_DRIFT",
    )
    _require(
        project_identity.get("size_bytes")
        == project_fingerprint["size_bytes"],
        "RESULT_PROJECT_SIZE_DRIFT",
    )
    _require(
        _parse_utc(str(project_identity.get("modified_at_utc")))
        == _parse_utc(project_fingerprint["modified_at_utc"]),
        "RESULT_PROJECT_MTIME_DRIFT",
    )
    project_modified = _parse_utc(project_fingerprint["modified_at_utc"])
    result_modified = _parse_utc(before[LOCAL_RESULT_FILENAME]["modified_at_utc"])
    _require(project_modified >= threshold, "PROJECT_NOT_FRESH")
    _require(result_modified >= project_modified, "RESULT_PREDATES_PROJECT")

    video_info = (
        timeline.get("VideoInfo")
        if isinstance(timeline.get("VideoInfo"), dict)
        else {}
    )
    fps_raw = video_info.get("FPS")
    fps = float(fps_raw)
    _require(fps > 0, "PROJECT_FPS_INVALID")
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
    timeline_frames = max(_item_int(timeline, "Length", 0), item_end)
    duration_seconds = round(timeline_frames / fps, 6)
    verified = result.get("independently_verified")
    _require(isinstance(verified, dict), "RESULT_VERIFICATION_MISSING")
    _require(
        verified.get("VoiceItem_count") == 9
        and verified.get("character_counts") == EXPECTED_DERIVED_COUNTS
        and verified.get("exact_text_order") is True
        and verified.get("exact_character_text_order") is True
        and verified.get("missing_count") == 0
        and verified.get("duplicate_count") == 0
        and verified.get("reordered") is False,
        "RESULT_SUMMARY_DRIFT",
    )
    _require(
        float(verified.get("fps")) == fps
        and verified.get("timeline_frames") == timeline_frames
        and float(verified.get("duration_seconds")) == duration_seconds
        and verified.get("voice_timing_summary") == timing_rows,
        "RESULT_TIMING_DRIFT",
    )

    canonical = _read_json(pilot / "canonical_script.json")
    traceability = _read_json(pilot / "cue_source_traceability.json")
    cues = canonical.get("cues")
    trace_cues = traceability.get("cues")
    _require(isinstance(cues, list) and len(cues) == 9, "CANONICAL_CUE_DRIFT")
    _require(
        isinstance(trace_cues, list) and len(trace_cues) == 9,
        "TRACEABILITY_CUE_DRIFT",
    )
    trace_by_id = {
        str(item.get("cue_id")): item
        for item in trace_cues
        if isinstance(item, dict)
    }
    boundaries = _cue_boundaries()
    cue_evidence: list[dict[str, Any]] = []
    for index, cue in enumerate(cues, start=1):
        cue_id = str(cue.get("cue_id"))
        trace = trace_by_id.get(cue_id)
        _require(isinstance(trace, dict), f"MISSING_CUE_TRACE:{cue_id}")
        claim_ids = [str(value) for value in cue.get("adopted_claim_ids", [])]
        source_ids = [str(value) for value in trace.get("supporting_source_ids", [])]
        _require(
            claim_ids == [str(value) for value in trace.get("adopted_claim_ids", [])],
            f"CLAIM_TRACE_DRIFT:{cue_id}",
        )
        _require(set(source_ids) <= ALLOWED_SOURCE_IDS, f"SOURCE_NOT_ALLOWLISTED:{cue_id}")
        _require(
            not (set(claim_ids) & EXCLUDED_VISUAL_CLAIM_IDS),
            f"EXCLUDED_CLAIM_IN_VISUAL_SPINE:{cue_id}",
        )
        cue_evidence.append(
            {
                "sequence": index,
                "cue_id": cue_id,
                "csv_row_id": f"csv_row_{index}",
                "scene_id": str(cue.get("scene_id")),
                "speaker": str(cue.get("speaker")),
                "text": str(cue.get("text")),
                "claim_ids": claim_ids,
                "source_ids": source_ids,
                "source_backed_factual_boundary": boundaries[cue_id],
                "timing": timing_rows[index - 1],
            }
        )

    after = {path.name: _fingerprint(path) for path in paths}
    _require(before == after, "LOCAL_EVIDENCE_CHANGED_DURING_AUDIT")

    snapshot = {
        "schema_version": (
            "new_banknote_yymm4_import_observation.evidence_snapshot.v1"
        ),
        "status": "verified_import_observation",
        "user_reported_terminal_result": {
            "status": user_reported_terminal_status,
            "evidence_grade": "observed",
        },
        "operator_result": {
            "repo_relative_path": expected_result_relative,
            "basename": LOCAL_RESULT_FILENAME,
            **before[LOCAL_RESULT_FILENAME],
            "status": "success",
            "failed_checks": [],
            "verified_check_count": len(REQUIRED_RESULT_CHECKS),
        },
        "operator_batch_state": {
            "repo_relative_path": expected_batch_relative,
            "basename": LOCAL_BATCH_STATE_FILENAME,
            **before[LOCAL_BATCH_STATE_FILENAME],
            "batch_not_before_utc": threshold.isoformat(),
        },
        "project_identity": {
            "repo_relative_path": expected_project_relative,
            "basename": LOCAL_PROJECT_FILENAME,
            **project_fingerprint,
            "exact_target_matches": True,
            "embedded_file_path_matches": True,
            "parse_error_code": None,
        },
        "operator_observation": {
            "no_mapping_error_update_or_character_mismatch_confirmed": True,
            "mapping_dialog_or_error_observed": False,
            "evidence_grade": "observed",
            "yymm4_product_version": observation.get("yymm4_product_version"),
            "profile_observation_version": observation.get(
                "profile_observation_version"
            ),
            "profile_version_match": observation.get("profile_version_match"),
            "version_difference_policy": "warning_only",
        },
        "project_verification": {
            "evidence_grade": "verified",
            "VoiceItem_count": 9,
            "character_counts": EXPECTED_DERIVED_COUNTS,
            "expected_and_actual_row_sha256": _compact_row_hash(actual_rows),
            "exact_text_order": True,
            "exact_character_text_order": True,
            "missing_count": missing_count,
            "duplicate_count": duplicate_count,
            "reordered": False,
            "fps": fps_raw,
            "timeline_frames": timeline_frames,
            "duration_seconds": duration_seconds,
            "timing_source": "actual_saved_voiceitem_frames_and_fps",
            "voice_timing_summary": timing_rows,
            "ImageItem_required_for_import_gate": False,
            "independent_TextItem_required_for_import_gate": False,
            "render_required_for_import_gate": False,
        },
        "approved_script_identity": {
            "accepted_batch_commit": (
                "d47794f47d7ffa1ffdbdffe506562fc7ddd2cb77"
            ),
            "artifact_hashes": actual_approved_hashes,
            "cue_count": 9,
            "scene_allocation": {"S1": 2, "S2": 4, "S3": 3},
            "unsupported_spoken_claim_count": 0,
        },
        "source_anchor_allowlist": sorted(ALLOWED_SOURCE_IDS),
        "cue_evidence": cue_evidence,
        "evidence_grades": {
            "verified": [
                "local_json_schema_and_hash",
                "project_parse_and_structure",
                "script_csv_hashes",
                "timing_summary",
            ],
            "observed": [
                "user_terminal_success",
                "no_mapping_error_update_or_character_mismatch",
            ],
            "inferred": [
                "creative_suitability",
                "future_yymm4_implementation_weight",
            ],
            "unverified": [
                "audio_rhythm_and_pronunciation",
                "subtitle_readability",
                "visual_effectiveness",
                "production_render_and_rights",
            ],
            "unknown": [],
        },
        "gate_boundary": {
            "csv_import_gate": "passed",
            "audio_editorial_gate": "open",
            "visual_direction_gate": "open",
            "render_gate": "open",
            "production_project": False,
            "rights_or_publication_approval": False,
        },
        "local_evidence_byte_preserved": True,
    }
    _require(
        user_reported_terminal_status == "success",
        "USER_TERMINAL_RESULT_NOT_SUCCESS",
    )
    return snapshot


def _route_options() -> list[dict[str, Any]]:
    common_typography = {
        "stack": "Japanese system UI sans-serif",
        "headline_role": "scene question or inspection action",
        "body_role": "one source-backed explanation at a time",
        "metadata_role": "cue/source IDs remain machine metadata only",
    }
    return [
        {
            "route_id": EXPECTED_ROUTE_IDS[0],
            "route_label": "Route A",
            "name": "Security Inspection Lab",
            "status": "RECOMMENDED",
            "recommended": True,
            "concept": (
                "抽象的な検査台の上で、技術の層と四つの確認動作を順に解く。"
                "Labは説明上の舞台比喩であり、実在施設や公式手順ではない。"
            ),
            "scene_purposes": {
                "S1": "問いを起点に、複数の技術と見分けやすさを俯瞰する。",
                "S2": "透過・傾き・触感・ルーペの四技術を一つずつ説明する。",
                "S3": "券種識別の工夫と四つの確認動作をまとめる。",
            },
            "layout_system": (
                "中央の抽象券シルエット、左の行動ラベル、右の根拠付き説明。"
                "字幕用下端リザーブを常時確保する。"
            ),
            "typography_role": common_typography,
            "color_role_proposal": {
                "proposal_only": True,
                "paper_field": "off-white",
                "primary_ink": "ink blue",
                "security_layer": "security green",
                "attention_accent": "restrained orange",
                "factual_color_exception": (
                    "橙色が事実を表すのはcue_008の千円券中央グラデーションだけ"
                ),
            },
            "motion_vocabulary": [
                "light_sweep",
                "restrained_tilt_parallax",
                "tactile_pulse",
                "loupe_zoom",
                "short_label_transition",
            ],
            "required_asset_families": [
                "original_abstract_note_silhouette",
                "css_security_layer_callouts",
                "generic_non_likeness_portrait",
                "schematic_loupe_and_action_icons",
            ],
            "rights_risk": "low_but_not_cleared",
            "factual_or_misleading_risk": (
                "抽象図を実券の位置・形状・検査手順と誤認させる可能性。"
                "全図を模式・縮尺外として扱う。"
            ),
            "ymm4_implementation_weight": "low_to_medium",
            "validation_evidence": (
                "S1/S2/S3の流れと各模式図が、9 cueの説明を誤解なく支えるかを"
                "human reviewで確認する。"
            ),
            "why_it_may_be_rejected": (
                "検査台の比喩が硬すぎる、または技術説明が日常文脈から離れて"
                "見える場合。"
            ),
        },
        {
            "route_id": EXPECTED_ROUTE_IDS[1],
            "route_label": "Route B",
            "name": "Everyday Verification",
            "status": "OPTION",
            "recommended": False,
            "concept": (
                "会計・ATM・手元確認を抽象的な日常背景として使い、"
                "四つの確認動作へ接続する。文脈は演出上の推定で事実根拠ではない。"
            ),
            "scene_purposes": {
                "S1": "新しいお札に気づく日常の入口を作る。",
                "S2": "日常背景を弱め、四技術の模式説明へ切り替える。",
                "S3": "手元確認と見分けやすさの工夫を整理する。",
            },
            "layout_system": (
                "左に抽象的な場所シルエット、中央に手元の模式図、"
                "右に確認動作。人物・店舗固有表現は使わない。"
            ),
            "typography_role": common_typography,
            "color_role_proposal": {
                "proposal_only": True,
                "environment": "neutral gray-blue",
                "note_focus": "off-white and ink blue",
                "action_accent": "security green",
            },
            "motion_vocabulary": [
                "context_fade",
                "hand_position_hint",
                "action_highlight",
                "restrained_focus_shift",
            ],
            "required_asset_families": [
                "original_generic_checkout_geometry",
                "original_generic_atm_geometry",
                "abstract_hand_pose",
                "schematic_action_icons",
            ],
            "rights_risk": "medium_not_cleared",
            "factual_or_misleading_risk": (
                "日常背景を政策、決済手段の比較、普及効果の根拠と誤認させる"
                "可能性。背景は非事実の文脈として明記する。"
            ),
            "ymm4_implementation_weight": "medium",
            "validation_evidence": (
                "日常文脈が説明を助け、技術事実や社会的意味を追加していないかを"
                "human reviewで確認する。"
            ),
            "why_it_may_be_rejected": (
                "人物・手・場所のrights-safe asset負担が増え、文脈が根拠以上の"
                "意味を帯びる場合。"
            ),
        },
        {
            "route_id": EXPECTED_ROUTE_IDS[2],
            "route_label": "Route C",
            "name": "Design Evolution",
            "status": "OPTION",
            "recommended": False,
            "concept": (
                "識別しやすさに関わるデザイン変更を抽象比較する。"
                "改善効果や政策進化ではなく、採用された差異だけを扱う。"
            ),
            "scene_purposes": {
                "S1": "2024年発行と複数技術の採用を現在側の俯瞰として示す。",
                "S2": "四技術を機能別の模式レイヤーとして並べる。",
                "S3": "額面数字、識別マーク、券種内の配置差を限定比較する。",
            },
            "layout_system": (
                "左右比較はcue_008で根拠のある額面数字だけに限定し、"
                "その他はF券内の抽象配置図として分離する。"
            ),
            "typography_role": common_typography,
            "color_role_proposal": {
                "proposal_only": True,
                "prior_series_placeholder": "neutral gray",
                "current_series_placeholder": "ink blue",
                "difference_marker": "restrained orange",
            },
            "motion_vocabulary": [
                "split_reveal",
                "difference_marker",
                "layer_step",
                "restrained_position_shift",
            ],
            "required_asset_families": [
                "original_generic_series_silhouettes",
                "schematic_numeral_scale_comparison",
                "abstract_position_diagrams",
                "difference_labels",
            ],
            "rights_risk": "medium_not_cleared",
            "factual_or_misleading_risk": (
                "比較範囲を越えた全体進化、改善効果、正確な券面差と受け取られる"
                "可能性。比較対象を明示して縮尺外とする。"
            ),
            "ymm4_implementation_weight": "medium_to_high",
            "validation_evidence": (
                "E券対F券の比較が額面数字だけに限定され、F券内差との混同が"
                "ないかをhuman reviewで確認する。"
            ),
            "why_it_may_be_rejected": (
                "比較精度と情報密度が高く、説明より券面再現に見える場合。"
            ),
        },
    ]


def _cue_visual_specs() -> dict[str, dict[str, str]]:
    return {
        "cue_001": {
            "screen_objective": "新しいお札の変化を問う導入を作る。",
            "foreground": "角丸の抽象券シルエットと大きな疑問符。",
            "background": "off-whiteの検査台グリッド。",
            "text_overlay": "2024年 新しいお札",
            "animation_primitive": "outline_reveal",
            "placeholder_asset": "abstract_note_question_placeholder",
            "ymm4_item_family_expectation": "ShapeItem + TextItem",
        },
        "cue_002": {
            "screen_objective": "複数の偽造防止技術と見分けやすさを俯瞰する。",
            "foreground": "抽象券の上に四つの色分けされた技術レイヤー。",
            "background": "中央照明のある検査台。",
            "text_overlay": "複数技術 + ユニバーサルデザイン",
            "animation_primitive": "layer_callout_reveal",
            "placeholder_asset": "security_layer_callout_placeholder",
            "ymm4_item_family_expectation": "ShapeItem group + TextItem",
        },
        "cue_003": {
            "screen_objective": "高精細すき入れを透過光の現象として示す。",
            "foreground": "非肖像の細線パターンが光で浮かぶ抽象パネル。",
            "background": "暗い青からoff-whiteへのバックライト。",
            "text_overlay": "透かす｜高精細すき入れ",
            "animation_primitive": "light_sweep",
            "placeholder_asset": "abstract_backlight_pattern_placeholder",
            "ymm4_item_family_expectation": "ShapeItem + masked gradient",
        },
        "cue_004": {
            "screen_objective": "3Dホログラムの見え方を傾きで説明する。",
            "foreground": "人物に似せない楕円シルエットと傾き矢印。",
            "background": "低彩度の角度ガイド。",
            "text_overlay": "傾ける｜3Dホログラム",
            "animation_primitive": "restrained_tilt_parallax",
            "placeholder_asset": "generic_portrait_parallax_placeholder",
            "ymm4_item_family_expectation": "ShapeItem layers + TextItem",
        },
        "cue_005": {
            "screen_objective": "深凹版印刷の盛り上がりと触感を概念化する。",
            "foreground": "三本の抽象インキ稜線と指示波形。",
            "background": "off-whiteの断面風パネル。",
            "text_overlay": "触る｜深凹版印刷",
            "animation_primitive": "tactile_pulse",
            "placeholder_asset": "raised_ink_ridge_placeholder",
            "ymm4_item_family_expectation": "ShapeItem group + TextItem",
        },
        "cue_006": {
            "screen_objective": "マイクロ文字をルーペ確認の模式図で示す。",
            "foreground": "ルーペ円内に単一のNIPPONGINKO模式ラベル。",
            "background": "実券模様を持たない点描グリッド。",
            "text_overlay": "ルーペで見る｜マイクロ文字",
            "animation_primitive": "loupe_zoom",
            "placeholder_asset": "schematic_loupe_label_placeholder",
            "ymm4_item_family_expectation": "ShapeItem + TextItem",
        },
        "cue_007": {
            "screen_objective": "識別マークの統一数と位置差を模式化する。",
            "foreground": "11本の同一斜線と三つの概念位置カード。",
            "background": "縮尺外と明記した抽象券枠。",
            "text_overlay": "識別マーク｜11本・位置が異なる",
            "animation_primitive": "position_marker_step",
            "placeholder_asset": "identification_mark_diagram_placeholder",
            "ymm4_item_family_expectation": "ShapeItem group + TextItem",
        },
        "cue_008": {
            "screen_objective": "額面数字と券種内の配置差を限定比較する。",
            "foreground": "大きさの異なる抽象数字と二つのF券位置カード。",
            "background": "比較範囲を分けた二段グリッド。",
            "text_overlay": "大きい額面数字｜券種ごとの違い",
            "animation_primitive": "bounded_difference_reveal",
            "placeholder_asset": "denomination_difference_placeholder",
            "ymm4_item_family_expectation": "ShapeItem + TextItem group",
        },
        "cue_009": {
            "screen_objective": "四つの確認動作を一列で記憶しやすくまとめる。",
            "foreground": "光・指・傾き・ルーペの四つの抽象アイコン。",
            "background": "off-whiteの最終チェックライン。",
            "text_overlay": "透かす / 触る / 傾ける / ルーペで見る",
            "animation_primitive": "four_action_sequence",
            "placeholder_asset": "four_action_icon_placeholder",
            "ymm4_item_family_expectation": "ShapeItem icons + TextItem",
        },
    }


def _script_beats(snapshot: Mapping[str, Any]) -> list[dict[str, Any]]:
    specs = _cue_visual_specs()
    beats: list[dict[str, Any]] = []
    for cue in snapshot["cue_evidence"]:
        spec = specs[str(cue["cue_id"])]
        timing = dict(cue["timing"])
        beats.append(
            {
                "sequence": cue["sequence"],
                "cue_id": cue["cue_id"],
                "csv_row_id": cue["csv_row_id"],
                "scene_id": cue["scene_id"],
                "speaker": cue["speaker"],
                "text": cue["text"],
                "claim_ids": cue["claim_ids"],
                "source_ids": cue["source_ids"],
                "screen_objective": spec["screen_objective"],
                "foreground": spec["foreground"],
                "background": spec["background"],
                "text_overlay": spec["text_overlay"],
                "source_backed_factual_boundary": cue[
                    "source_backed_factual_boundary"
                ],
                "animation": {
                    "primitive": spec["animation_primitive"],
                    "start": "voice_start",
                    "end": "voice_end",
                    "start_frame": timing["frame"],
                    "end_frame": timing["end_frame"],
                },
                "expected_duration_relation_to_actual_voiceitem_timing": {
                    "basis": "actual_import_voiceitem",
                    "length_frames": timing["length_frames"],
                    "policy": (
                        "visual beat fits inside the observed voice interval; "
                        "future implementation may not alter VoiceItem timing"
                    ),
                },
                "placeholder_asset": spec["placeholder_asset"],
                "future_rights_decision": (
                    "review original abstract asset after route selection; "
                    "rights not cleared in this slice"
                ),
                "ymm4_item_family_expectation": spec[
                    "ymm4_item_family_expectation"
                ],
                "implementation_status": "not_started",
            }
        )
    return beats


def _scene_layout_plan(beats: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    scene_meta = {
        "S1": {
            "title": "Question and Overview",
            "purpose": "問いから複数の技術レイヤーへ導く。",
            "layout": "center-focal abstract note with side callouts",
        },
        "S2": {
            "title": "Four Security Techniques",
            "purpose": "透過・傾き・触感・ルーペを順に深掘りする。",
            "layout": "single inspection stage with one technique at a time",
        },
        "S3": {
            "title": "Identification and Four Actions",
            "purpose": "識別の工夫を整理し、四動作で締める。",
            "layout": "bounded comparison followed by four-action ribbon",
        },
    }
    scenes: list[dict[str, Any]] = []
    for scene_id in ("S1", "S2", "S3"):
        scenes.append(
            {
                "scene_id": scene_id,
                **scene_meta[scene_id],
                "subtitle_safe_reserve": "bottom_22_percent",
                "reading_order": "headline -> diagram -> one explanation label",
                "cue_plans": [
                    dict(beat) for beat in beats if beat["scene_id"] == scene_id
                ],
            }
        )
    return {
        "schema_version": "new_banknote.visual_scene_layout_plan.v1",
        "status": "review_candidate_not_selected",
        "route_id": EXPECTED_ROUTE_IDS[0],
        "depiction_policy": "original_abstract_schematic_only",
        "canvas_assumption": "16:9 internal review composition",
        "palette_roles_are_proposals": True,
        "scenes": scenes,
        "cue_coverage": [beat["cue_id"] for beat in beats],
        "implementation_authorized": False,
    }


def _motion_plan(beats: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "new_banknote.visual_motion_beat_plan.v1",
        "status": "proposed_not_implemented",
        "route_id": EXPECTED_ROUTE_IDS[0],
        "motion_policy": {
            "restrained": True,
            "production_keyframes_authorized": False,
            "voice_timing_mutation_authorized": False,
            "allowed_semantics": [
                "enter",
                "reveal",
                "emphasize",
                "move",
                "dim",
            ],
        },
        "beats": [
            {
                "cue_id": beat["cue_id"],
                "scene_id": beat["scene_id"],
                "primitive": beat["animation"]["primitive"],
                "start_frame_reference": beat["animation"]["start_frame"],
                "end_frame_reference": beat["animation"]["end_frame"],
                "timing_basis": "observed VoiceItem interval",
                "future_tuning": "human-selected route diagnostic project only",
            }
            for beat in beats
        ],
    }


def _asset_rights_matrix() -> dict[str, Any]:
    assets = [
        ("abstract_note_silhouette", "CSS geometry", "S1/S2/S3"),
        ("security_layer_callouts", "CSS geometry and labels", "S1"),
        ("backlight_pattern", "original abstract line pattern", "S2"),
        ("generic_portrait_silhouette", "non-likeness CSS geometry", "S2"),
        ("raised_ink_ridges", "original abstract CSS geometry", "S2"),
        ("loupe_and_schematic_label", "CSS geometry and one text label", "S2"),
        ("identification_mark_diagram", "schematic CSS geometry", "S3"),
        ("denomination_difference_diagram", "schematic CSS geometry", "S3"),
        ("four_action_icons", "original symbolic CSS geometry", "S3"),
    ]
    return {
        "schema_version": "new_banknote.visual_asset_rights_matrix.v1",
        "status": "planning_only",
        "default_representation": "original_abstract_schematic",
        "official_image_reuse": False,
        "external_asset_fetch": False,
        "rights_cleared": False,
        "prohibited_representation_elements": [
            "recognizable_portrait",
            "serial_or_seal",
            "full_note_layout",
            "real_security_pattern_texture",
            "repeatable_exact_placement_or_detail",
        ],
        "assets": [
            {
                "asset_id": asset_id,
                "representation": representation,
                "scene_use": scene_use,
                "source": "future_original_internal_asset",
                "rights_risk": "low_but_not_cleared",
                "current_file": None,
                "created_in_this_slice": False,
                "future_decision": "review after Route A is selected",
            }
            for asset_id, representation, scene_use in assets
        ],
    }


def _ymm4_visual_project_contract() -> dict[str, Any]:
    return {
        "schema_version": "new_banknote.yymm4_visual_project_contract.v1",
        "status": "not_authorized",
        "implementation_status": "not_started",
        "selected_route": None,
        "recommended_route": EXPECTED_ROUTE_IDS[0],
        "authorization": {
            "human_route_selection_required": True,
            "diagnostic_project_authorized": False,
            "production_project_authorized": False,
            "render_authorized": False,
            "asset_creation_authorized": False,
        },
        "future_base_project": {
            "repo_relative_identity": (
                f"{PILOT_RELATIVE.as_posix()}/{LOCAL_OUTPUT_DIRNAME}/"
                f"{LOCAL_PROJECT_FILENAME}"
            ),
            "tracked": False,
            "cross_machine_portability_verified": False,
            "existing_voiceitems_must_be_preserved": True,
            "project_zero_generation": False,
        },
        "future_item_family_expectations": {
            "VoiceItem": "preserve all 9 imported items byte-semantically",
            "ShapeItem": "preferred for original schematic geometry",
            "TextItem": "short explanation labels only",
            "ImageItem": "only for later reviewed original assets if required",
            "render_or_media": "outside this contract",
        },
        "future_acceptance": [
            "human selected route or cue-specific revision",
            "9 VoiceItems remain 3/6 with exact text/order",
            "planned scene items resolve without external assets",
            "diagnostic project parses headlessly",
        ],
    }


def _review_questions() -> list[str]:
    return [
        "A / B / C のどれを次の方向として選びますか。",
        "S1 / S2 / S3 のscene spineは台本の説明順に合っていますか。",
        "実際のお札について誤解を招きそうな模式図はありますか。",
        "一般向け解説としてmotionは十分に抑制されていますか。",
    ]


def _import_readme(snapshot: Mapping[str, Any]) -> str:
    verified = snapshot["project_verification"]
    project = snapshot["project_identity"]
    result = snapshot["operator_result"]
    return f"""# 新紙幣 YMM4 import observation

> **INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION**

ユーザー操作で保存されたlocal YMM4 projectをheadlessに再解析し、CSV import
gateの構造的成功を確認したsanitized review surfaceです。local project、result、
batch stateはignoredのままbyte-preservedで、ここにはrepo-relative identity、
basename、hash、size、mtime、検証値だけを記録します。

## 結果

- operator result: `{result['status']}` / failed checks `0`
- project: `{project['basename']}`
- VoiceItems: `{verified['VoiceItem_count']}`
- characters: ゆっくり霊夢 `{verified['character_counts']['ゆっくり霊夢']}` / ゆっくり魔理沙 `{verified['character_counts']['ゆっくり魔理沙']}`
- text/order: exact / missing `{verified['missing_count']}` / duplicate `{verified['duplicate_count']}`
- timing: `{verified['fps']} fps` / `{verified['timeline_frames']} frames` / `{verified['duration_seconds']} seconds`
- project SHA-256: `{project['sha256']}`
- result SHA-256: `{result['sha256']}`

## Evidence boundary

CSV import gateはpassedです。mapping/error/update/character mismatchがなかったことは
operator observationであり、project構造・本文・順序・timingはmachine verifiedです。
音声のリズム・発音、字幕の読みやすさ、visual effectiveness、render、production、
rights、publicationは未検証です。import gateではImageItem、独立TextItem、renderを
要求していません。

## Next review

Route A / B / C と推奨S1/S2/S3 spineは
`visual_scene_decision/README_VISUAL_SCENE_DECISION.md`から確認します。推奨は選択済みを
意味せず、visual YMM4 projectの作成はまだ許可されていません。
"""


def _import_receipt(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "new_banknote.yymm4_import_observation_receipt.v1",
        "status": "passed",
        "decision": "csv_import_gate_passed_visual_review_ready",
        "target_state_id": TARGET_STATE_ID,
        "operator_result": snapshot["operator_result"],
        "project_identity": snapshot["project_identity"],
        "operator_observation": snapshot["operator_observation"],
        "verified_import_contract": snapshot["project_verification"],
        "approved_script_identity": snapshot["approved_script_identity"],
        "evidence_grades": snapshot["evidence_grades"],
        "gate_boundary": snapshot["gate_boundary"],
        "local_evidence_disposition": {
            "project_tracked": False,
            "operator_result_tracked": False,
            "batch_state_tracked": False,
            "local_bytes_preserved": True,
            "absolute_runtime_paths_promoted": False,
        },
    }


def _import_traceability(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": (
            "new_banknote.yymm4_import_source_to_project_traceability.v1"
        ),
        "status": "passed",
        "source_registry": "authoritative_source_registry.json",
        "claim_adjudication": "claim_adjudication.json",
        "cue_traceability": "cue_source_traceability.json",
        "project_identity": {
            "repo_relative_path": snapshot["project_identity"][
                "repo_relative_path"
            ],
            "sha256": snapshot["project_identity"]["sha256"],
        },
        "expected_and_actual_row_sha256": snapshot["project_verification"][
            "expected_and_actual_row_sha256"
        ],
        "rows": [
            {
                "csv_row_id": cue["csv_row_id"],
                "cue_id": cue["cue_id"],
                "scene_id": cue["scene_id"],
                "claim_ids": cue["claim_ids"],
                "source_ids": cue["source_ids"],
                "project_character": (
                    "ゆっくり霊夢"
                    if cue["speaker"] == "れいむ"
                    else "ゆっくり魔理沙"
                ),
                "text_sha256": hashlib.sha256(
                    str(cue["text"]).encode("utf-8")
                ).hexdigest(),
                "timing": cue["timing"],
                "exact_project_match": True,
            }
            for cue in snapshot["cue_evidence"]
        ],
        "unsupported_spoken_claim_count": 0,
        "source_bodies_copied": False,
        "absolute_paths_copied": False,
    }


def _import_limitations() -> str:
    return """# YMM4 import observation limitations

> **INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION**

- Structural success verifies one saved local project, 9 VoiceItems, character 3/6,
  exact text/order, zero missing/duplicate, and actual timing metadata.
- The operator-confirmed absence of mapping/error/update/character mismatch is observed
  evidence. It is not an independent GUI observation by Codex.
- Audio rhythm, pronunciation, terminology comfort, linked subtitle readability, and
  creative quality remain human-review gates.
- No visual route, asset, YMM4 visual project, render, production use, rights use, or
  publication is approved.
- The ignored project contains machine-local identity. Cross-machine portability is
  not established.
- The import gate did not require ImageItem, independent TextItem, render, or media.
"""


def _visual_readme(
    routes: Sequence[Mapping[str, Any]],
    snapshot: Mapping[str, Any],
) -> str:
    timing = snapshot["project_verification"]
    return f"""# 新紙幣 visual / scene decision

> **INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION**

machine-verified import timing（{timing['fps']} fps / {timing['timeline_frames']} frames /
{timing['duration_seconds']} seconds）を参照し、同じ9 cueを三つのvisual routeとして
比較するreview packetです。ここではrouteを実装せず、Route Aを推奨として明示します。

## Editorial provenance

事実部分はclaimとofficial sourceに接続し、会話構造・接続・圧縮はeditorial synthesisとして
区別しています。current execution contractで現在の9 cueを継続するbounded approvalを
記録していますが、独立した同時点receiptや将来のsilent edit権限ではありません。
以前のuser-submitted scriptの取り込みは利用可能なrepo証拠から未証明です。
詳細は[Editorial Provenance](../editorial_provenance/README_EDITORIAL_PROVENANCE.md)で確認できます。

## Recommendation

**Route A — Security Inspection Lab — RECOMMENDED**

source-backedな四技術と「透かす / 触る / 傾ける / ルーペで見る」を直接対応させ、
外部画像なしの抽象図で構成でき、rights burdenと誤解リスクを最も制御しやすいためです。
推奨はhuman selectionではありません。

## Three routes

- Route A: Security Inspection Lab — low to medium — recommended
- Route B: Everyday Verification — medium — contextual asset and implication risk
- Route C: Design Evolution — medium to high — comparison accuracy and density risk

## Review path

1. `visual_direction_board.html`でRoute AのS1/S2/S3 spineとB/C比較を確認する。
2. `visual_review_sheet.md`の4問にA/B/Cまたはcue/scene修正で答える。
3. human selection後の別sliceでのみdiagnostic YMM4 projectを検討する。

全routeはoriginal abstract schematicだけを前提とし、実券の肖像、通し番号、印章、
券面全体、実security pattern、再現可能な正確配置を扱いません。paletteは提案であり、
rights cleared、production ready、render approvedを意味しません。
"""


def _visual_review_sheet() -> str:
    questions = _review_questions()
    return """# Visual direction review sheet

> **INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION**

JSONやsecondary artifactを全件確認する必要はありません。HTML boardを見て、次の4問だけ
返してください。修正が必要ならscene IDまたはcue IDを添えてください。

""" + "\n".join(
        f"{index}. {question}" for index, question in enumerate(questions, 1)
    ) + "\n"


def _visual_limitations() -> str:
    return """# Visual decision limitations

> **INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION**

- Route A is recommended, not selected or approved.
- Routes B and C contain inferred creative context; they add no factual claims.
- All diagrams are original abstract schematic proposals and not to scale.
- No official image, portrait likeness, serial, seal, full-note layout, real security
  texture, exact placement, external asset, font, script, or URL is used.
- Color roles are proposals. Orange is factual only for the cue-008 ¥1,000 central
  gradient statement.
- Actual visual effectiveness, subtitle readability, motion comfort, audio quality,
  asset rights, YMM4 feasibility, render, production, and publication remain open.
- No image asset or YMM4 visual project was created in this slice.
"""


def _render_html(
    routes: Sequence[Mapping[str, Any]],
    scene_plan: Mapping[str, Any],
    snapshot: Mapping[str, Any],
) -> str:
    route_a = routes[0]
    scene_cards: list[str] = []
    for scene in scene_plan["scenes"]:
        cue_chips = "".join(
            (
                '<li><span class="cue-id">'
                + html.escape(str(cue["cue_id"]))
                + "</span><strong>"
                + html.escape(str(cue["text_overlay"]))
                + "</strong><small>"
                + html.escape(str(cue["screen_objective"]))
                + "</small></li>"
            )
            for cue in scene["cue_plans"]
        )
        scene_cards.append(
            '<section class="scene-card">'
            f'<div class="scene-kicker">{html.escape(str(scene["scene_id"]))}</div>'
            f'<h3>{html.escape(str(scene["title"]))}</h3>'
            f'<p>{html.escape(str(scene["purpose"]))}</p>'
            '<div class="note-geometry" aria-hidden="true">'
            '<span class="note-core"></span><span class="note-mark m1"></span>'
            '<span class="note-mark m2"></span><span class="note-mark m3"></span>'
            "</div>"
            f'<ul class="cue-list">{cue_chips}</ul>'
            "</section>"
        )
    comparison_rows = "".join(
        (
            '<article class="compare-row">'
            f'<div><span class="route-label">{html.escape(str(route["route_label"]))}</span>'
            f'<h3>{html.escape(str(route["name"]))}</h3></div>'
            f'<p>{html.escape(str(route["concept"]))}</p>'
            f'<div class="weight">{html.escape(str(route["ymm4_implementation_weight"]))}</div>'
            "</article>"
        )
        for route in routes[1:]
    )
    timing = snapshot["project_verification"]
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>New Banknote Visual Direction Board</title>
<style>
:root {{ --paper:#f4f0e6; --ink:#17324d; --green:#2f6f5d; --orange:#d77836; --line:#c8c2b5; --muted:#68737c; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:#e8e4db; color:#152433; font-family:"Yu Gothic UI","Meiryo",sans-serif; }}
.shell {{ max-width:1440px; margin:0 auto; padding:28px; }}
.banner {{ background:#172a3a; color:white; padding:12px 18px; letter-spacing:.08em; font-weight:800; border-radius:12px; }}
.hero {{ display:grid; grid-template-columns:1.4fr .6fr; gap:24px; margin:24px 0; }}
.hero h1 {{ font-size:clamp(30px,4vw,58px); line-height:1.05; margin:10px 0; color:var(--ink); }}
.eyebrow,.route-label,.scene-kicker {{ color:var(--green); font-weight:900; letter-spacing:.1em; text-transform:uppercase; }}
.status {{ border:2px solid var(--orange); background:var(--paper); padding:18px; border-radius:16px; }}
.status strong {{ display:block; color:var(--orange); font-size:22px; }}
.meta {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:14px; }}
.meta span {{ background:white; border:1px solid var(--line); border-radius:999px; padding:7px 11px; }}
.spine {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }}
.scene-card {{ background:var(--paper); border:1px solid var(--line); border-top:8px solid var(--green); border-radius:18px; padding:20px; min-height:520px; }}
.scene-card h3 {{ font-size:24px; color:var(--ink); margin:8px 0; }}
.note-geometry {{ height:130px; margin:18px 0; border:3px solid var(--ink); border-radius:14px; position:relative; background:linear-gradient(110deg,#f7f3e9,#e6efe8); overflow:hidden; }}
.note-core {{ position:absolute; width:64px; height:64px; border:2px solid var(--green); border-radius:50%; left:50%; top:50%; transform:translate(-50%,-50%); }}
.note-mark {{ position:absolute; width:34px; height:8px; background:var(--orange); border-radius:8px; }}
.m1 {{ left:12%; top:25%; }} .m2 {{ right:12%; top:55%; }} .m3 {{ left:18%; bottom:18%; background:var(--green); }}
.cue-list {{ list-style:none; padding:0; margin:0; display:grid; gap:10px; }}
.cue-list li {{ display:grid; grid-template-columns:auto 1fr; gap:4px 10px; background:white; border:1px solid var(--line); border-radius:12px; padding:10px; }}
.cue-id {{ grid-row:1 / span 2; color:var(--orange); font-weight:800; }}
.cue-list small {{ color:var(--muted); }}
.alternatives {{ margin-top:28px; }}
.compare-row {{ display:grid; grid-template-columns:240px 1fr 130px; gap:18px; align-items:center; background:white; border-left:7px solid var(--ink); padding:16px 20px; margin:10px 0; border-radius:12px; }}
.compare-row h3 {{ margin:3px 0; }} .compare-row p {{ margin:0; color:#394957; }}
.weight {{ text-align:center; border:1px solid var(--line); border-radius:999px; padding:8px; font-weight:800; }}
.footer {{ margin-top:26px; padding:20px; border:2px dashed var(--orange); background:var(--paper); border-radius:14px; }}
.links {{ display:flex; flex-wrap:wrap; gap:12px; margin-top:12px; }}
.links a {{ color:var(--ink); background:white; border:1px solid var(--line); padding:9px 12px; border-radius:9px; font-weight:700; }}
@media (max-width:900px) {{ .hero,.spine,.compare-row {{ grid-template-columns:1fr; }} .scene-card {{ min-height:auto; }} }}
</style>
</head>
<body>
<main class="shell">
  <div class="banner">INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION</div>
  <section class="hero">
    <div>
      <div class="eyebrow">Visual direction decision</div>
      <h1>新紙幣を、抽象図でどう説明するか</h1>
      <p>三つのrouteを比較し、source-backedなS1/S2/S3 spineを選ぶための静的boardです。</p>
      <div class="meta"><span>9 cues</span><span>{timing['fps']} fps</span><span>{timing['timeline_frames']} frames</span><span>{timing['duration_seconds']} sec</span></div>
    </div>
    <aside class="status"><strong>Route A — RECOMMENDED</strong><h2>{html.escape(str(route_a['name']))}</h2><p>推奨は選択・承認・実装を意味しません。</p></aside>
  </section>
  <section>
    <div class="eyebrow">Primary scene spine</div>
    <h2>Route A / S1 → S2 → S3</h2>
    <div class="spine">{''.join(scene_cards)}</div>
  </section>
  <section class="alternatives">
    <div class="eyebrow">Compact comparison</div>
    <h2>Routes B and C</h2>
    {comparison_rows}
  </section>
  <section class="footer">
    <p><strong>Editorial provenance:</strong> source-derived facts、editorial synthesis、current execution contractのbounded approval（独立receiptなし）、prior-user-scriptの未証明範囲を分離して記録しています。</p>
    <strong>Abstract schematic only.</strong> 実券の肖像・通し番号・印章・券面全体・実security pattern・正確配置を使いません。
    <div class="links"><a href="visual_review_sheet.md">4-question review sheet</a><a href="recommended_visual_direction.json">Recommended direction</a><a href="../README_YMM4_IMPORT_OBSERVATION.md">Import evidence</a><a href="../editorial_provenance/README_EDITORIAL_PROVENANCE.md">Editorial provenance</a></div>
  </section>
</main>
</body>
</html>
"""


def _recommended_direction(
    route_a: Mapping[str, Any],
    scene_plan: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "new_banknote.recommended_visual_direction.v1",
        "status": "recommended_not_selected",
        "route": route_a,
        "recommendation_rationale": [
            "direct mapping to the four source-backed inspection actions",
            "lowest external asset and rights burden",
            "strongest S1/S2/S3 explanatory fit",
            "reusable original schematic geometry in a later YMM4 diagnostic project",
        ],
        "scene_spine_summary": [
            {
                "scene_id": scene["scene_id"],
                "title": scene["title"],
                "cue_ids": [cue["cue_id"] for cue in scene["cue_plans"]],
            }
            for scene in scene_plan["scenes"]
        ],
        "human_selection_required": True,
        "implementation_authorized": False,
    }


def _safe_relative_hrefs(board: str) -> bool:
    hrefs = re.findall(r'(?i)href\s*=\s*["\']([^"\']+)["\']', board)
    if not hrefs:
        return False
    for href in hrefs:
        if _PRIVATE_OR_EXTERNAL_RE.search(href) or href.startswith(("/", "#")):
            return False
        normalized = posixpath.normpath(f"{VISUAL_DIRNAME}/{href}")
        if normalized == ".." or normalized.startswith("../"):
            return False
    return True


def _html_has_no_dependencies(board: str) -> bool:
    lower = board.lower()
    forbidden = (
        "<script",
        "<link",
        "<img",
        "<iframe",
        "<object",
        "<embed",
        " src=",
        " srcset=",
        "@import",
        "url(",
        "data:",
        "javascript:",
    )
    return not any(token in lower for token in forbidden)


def render_new_banknote_import_visual_decision_artifacts(
    snapshot: Mapping[str, Any],
) -> dict[str, bytes]:
    """Render the tracked packet from an already-sanitized evidence snapshot."""
    snapshot_text = _json_bytes(snapshot).decode("utf-8")
    _require(
        _PRIVATE_OR_EXTERNAL_RE.search(snapshot_text) is None,
        "SNAPSHOT_CONTAINS_PRIVATE_OR_EXTERNAL_REFERENCE",
    )
    routes = _route_options()
    _require(
        [route["route_id"] for route in routes] == EXPECTED_ROUTE_IDS,
        "VISUAL_ROUTE_SET_DRIFT",
    )
    _require(
        sum(route["recommended"] is True for route in routes) == 1
        and routes[0]["status"] == "RECOMMENDED",
        "VISUAL_RECOMMENDATION_DRIFT",
    )
    beats = _script_beats(snapshot)
    scene_plan = _scene_layout_plan(beats)
    motion_plan = _motion_plan(beats)
    asset_matrix = _asset_rights_matrix()
    board = _render_html(routes, scene_plan, snapshot)

    options = {
        "schema_version": "new_banknote.visual_direction_options.v1",
        "status": "human_selection_required",
        "route_count": 3,
        "recommended_route_count": 1,
        "routes": routes,
        "shared_boundary": {
            "abstract_original_diagrams_only": True,
            "official_image_reuse": False,
            "external_asset_or_url": False,
            "new_factual_claims": False,
            "production_or_rights_approval": False,
        },
    }
    script_ir = {
        "schema_version": "new_banknote.source_backed_script_beat_ir.v1",
        "status": "visual_planning_only",
        "source_anchor_allowlist": snapshot["source_anchor_allowlist"],
        "cue_count": 9,
        "scene_allocation": {"S1": 2, "S2": 4, "S3": 3},
        "beats": beats,
        "voice_timing_mutation_authorized": False,
        "new_claim_generation_authorized": False,
    }

    readback = {
        "schema_version": "new_banknote.yymm4_import_observation_readback.v1",
        "status": "passed",
        "evidence_snapshot": snapshot,
        "checks": {
            "operator_result_success": True,
            "failed_checks_empty": True,
            "local_project_reparsed": True,
            "VoiceItem_count_9": True,
            "character_counts_3_6": True,
            "exact_text_and_order": True,
            "missing_and_duplicate_zero": True,
            "local_evidence_byte_preserved": True,
            "approved_script_hashes_frozen": True,
            "absolute_runtime_paths_excluded": True,
        },
        "failed_checks": [],
    }
    payloads: dict[str, bytes] = {
        IMPORT_README_FILENAME: _import_readme(snapshot).encode("utf-8"),
        IMPORT_RECEIPT_FILENAME: _json_bytes(_import_receipt(snapshot)),
        IMPORT_READBACK_FILENAME: _json_bytes(readback),
        IMPORT_TRACEABILITY_FILENAME: _json_bytes(
            _import_traceability(snapshot)
        ),
        IMPORT_LIMITATIONS_FILENAME: _import_limitations().encode("utf-8"),
        f"{VISUAL_DIRNAME}/{VISUAL_README_FILENAME}": _visual_readme(
            routes, snapshot
        ).encode("utf-8"),
        f"{VISUAL_DIRNAME}/{VISUAL_OPTIONS_FILENAME}": _json_bytes(options),
        f"{VISUAL_DIRNAME}/{RECOMMENDED_DIRECTION_FILENAME}": _json_bytes(
            _recommended_direction(routes[0], scene_plan)
        ),
        f"{VISUAL_DIRNAME}/{SCRIPT_BEAT_FILENAME}": _json_bytes(script_ir),
        f"{VISUAL_DIRNAME}/{SCENE_PLAN_FILENAME}": _json_bytes(scene_plan),
        f"{VISUAL_DIRNAME}/{MOTION_PLAN_FILENAME}": _json_bytes(motion_plan),
        f"{VISUAL_DIRNAME}/{ASSET_MATRIX_FILENAME}": _json_bytes(
            asset_matrix
        ),
        f"{VISUAL_DIRNAME}/{YMM4_CONTRACT_FILENAME}": _json_bytes(
            _ymm4_visual_project_contract()
        ),
        f"{VISUAL_DIRNAME}/{VISUAL_REVIEW_FILENAME}": (
            _visual_review_sheet().encode("utf-8")
        ),
        f"{VISUAL_DIRNAME}/{HTML_BOARD_FILENAME}": board.encode("utf-8"),
        f"{VISUAL_DIRNAME}/{VISUAL_LIMITATIONS_FILENAME}": (
            _visual_limitations().encode("utf-8")
        ),
    }

    combined = b"\n".join(payloads.values()).decode("utf-8")
    source_ids = {
        source_id
        for beat in beats
        for source_id in beat["source_ids"]
    }
    cue_ids = [beat["cue_id"] for beat in beats]
    scene_ids = [scene["scene_id"] for scene in scene_plan["scenes"]]
    board_checks = {
        "exactly_three_routes": len(routes) == 3,
        "exactly_one_recommended": (
            sum(route["recommended"] is True for route in routes) == 1
        ),
        "route_A_recommended": routes[0]["status"] == "RECOMMENDED",
        "scene_spine_S1_S2_S3": scene_ids == ["S1", "S2", "S3"],
        "cue_coverage_9_of_9": cue_ids
        == [f"cue_{index:03d}" for index in range(1, 10)],
        "source_ids_allowlisted": source_ids <= ALLOWED_SOURCE_IDS,
        "excluded_visual_claim_absent": not any(
            claim_id in combined for claim_id in EXCLUDED_VISUAL_CLAIM_IDS
        ),
        "review_question_count_at_most_4": len(_review_questions()) <= 4,
        "required_boundary_banner_present": all(
            token in board
            for token in (
                "INTERNAL REVIEW",
                "NOT FINAL",
                "NON-PUBLIC",
                "NON-PRODUCTION",
            )
        ),
        "route_and_scene_labels_present": all(
            token in board
            for token in (
                "Route A",
                "Route B",
                "Route C",
                "S1",
                "S2",
                "S3",
            )
        ),
        "html_self_contained_no_dependencies": _html_has_no_dependencies(
            board
        ),
        "html_links_are_repo_relative": _safe_relative_hrefs(board),
        "private_or_external_references_absent": (
            _PRIVATE_OR_EXTERNAL_RE.search(combined) is None
        ),
        "abstract_depiction_policy_present": (
            asset_matrix["default_representation"]
            == "original_abstract_schematic"
        ),
        "visual_project_not_authorized": (
            _ymm4_visual_project_contract()["authorization"][
                "diagnostic_project_authorized"
            ]
            is False
        ),
    }
    failed = [name for name, passed in board_checks.items() if passed is not True]
    _require(not failed, "VISUAL_BOARD_READBACK_FAILED:" + ",".join(failed))
    board_readback = {
        "schema_version": "new_banknote.visual_direction_board_readback.v1",
        "status": "passed",
        "checks": board_checks,
        "failed_checks": [],
        "artifact_hashes": {
            relative: _sha256_bytes(data)
            for relative, data in payloads.items()
            if relative.startswith(f"{VISUAL_DIRNAME}/")
        },
        "human_review_question_count": len(_review_questions()),
        "selected_route": None,
        "recommended_route": EXPECTED_ROUTE_IDS[0],
    }
    payloads[f"{VISUAL_DIRNAME}/{HTML_READBACK_FILENAME}"] = _json_bytes(
        board_readback
    )
    return payloads


def build_new_banknote_import_visual_decision_packet(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, Any]:
    """Audit immutable evidence, then write only deterministic tracked outputs."""
    pilot = Path(pilot_dir).resolve()
    local_paths = [
        pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_PROJECT_FILENAME,
        pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_RESULT_FILENAME,
        pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_BATCH_STATE_FILENAME,
    ]
    before = {path.name: _fingerprint(path) for path in local_paths}
    snapshot = audit_new_banknote_yymm4_import_observation(pilot)
    payloads = render_new_banknote_import_visual_decision_artifacts(snapshot)
    changed = [
        relative
        for relative, data in payloads.items()
        if _write_bytes(pilot / relative, data)
    ]
    after = {path.name: _fingerprint(path) for path in local_paths}
    _require(before == after, "LOCAL_EVIDENCE_CHANGED_DURING_BUILD")
    return {
        "status": "passed",
        "target_state_id": TARGET_STATE_ID,
        "artifact_count": len(payloads),
        "changed": changed,
        "local_evidence_byte_preserved": True,
        "project_verification": snapshot["project_verification"],
    }


def preflight_new_banknote_import_visual_decision_packet(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, Any]:
    """Re-audit inputs and verify tracked packet bytes without writing."""
    pilot = Path(pilot_dir).resolve()
    snapshot = audit_new_banknote_yymm4_import_observation(pilot)
    payloads = render_new_banknote_import_visual_decision_artifacts(snapshot)
    checks = {
        "local_evidence_verified": True,
        "artifact_count_17": len(payloads) == 17,
        "tracked_artifacts_present": all(
            (pilot / relative).is_file() for relative in payloads
        ),
        "tracked_artifacts_byte_deterministic": all(
            (pilot / relative).is_file()
            and (pilot / relative).read_bytes() == data
            for relative, data in payloads.items()
        ),
        "no_private_or_external_reference": all(
            _PRIVATE_OR_EXTERNAL_RE.search(data.decode("utf-8")) is None
            for data in payloads.values()
        ),
    }
    failed = [name for name, passed in checks.items() if passed is not True]
    return {
        "status": "passed" if not failed else "failed",
        "checks": checks,
        "failed_checks": failed,
        "target_state_id": TARGET_STATE_ID,
    }


def load_tracked_evidence_snapshot(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, Any]:
    readback = _read_json(Path(pilot_dir) / IMPORT_READBACK_FILENAME)
    snapshot = readback.get("evidence_snapshot")
    if not isinstance(snapshot, dict):
        raise ValueError("TRACKED_EVIDENCE_SNAPSHOT_MISSING")
    return snapshot


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build or preflight the new-banknote import visual decision packet"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "preflight"):
        child = subparsers.add_parser(name)
        child.add_argument("--pilot", default=str(DEFAULT_PILOT_DIR))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "build":
        payload = build_new_banknote_import_visual_decision_packet(args.pilot)
    else:
        payload = preflight_new_banknote_import_visual_decision_packet(
            args.pilot
        )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload.get("status") == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
