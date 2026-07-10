from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from src.cli.main import main
from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
)
from src.pipeline.ymm4_observation_readback_pack import (
    CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION,
    DEFAULT_ARTIFACT_ID,
    OBSERVATION_RECEIPT_SCHEMA_VERSION,
    REQUIRED_YMM4_OBSERVATION_FILES,
    _detect_yymm4,
    build_ymm4_observation_readback_pack,
    validate_ymm4_observation_readback_pack,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"
BLOCKER_RECEIPT = SOURCE_PACKAGE / "ymm4_alias_reobservation_blocker_2026-07-11.json"
LEGACY_RECEIPT_PATH = SOURCE_PACKAGE / "ymm4_observation_receipt_2026-07-10.json"
LEGACY_RECEIPT_SHA256 = "DC756D9C4EE9ABDFDDFB284B2B8EC70B227DDEB5E365C1BBB8EE8438D8C9A5B5"
CANONICAL_CSV = (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "transcript_substitution_readiness/regenerated_draft_yymm4.csv"
)
CANONICAL_CSV_SHA256 = "6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C"
DERIVED_CSV = (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "ymm4_import_ready_pack/derived_yymm4_import.csv"
)
DERIVED_CSV_SHA256 = "5452DE96DC6EF012400A132BA5BAE80B8553C1B1CDD27860D36674C25AF391BC"
CHARACTER_PROFILE = (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "ymm4_character_alias_profiles/ymm4_4_53_0_9_yukkuri_characters_v1.json"
)
CHARACTER_PROFILE_ID = "ymm4_4_53_0_9_yukkuri_characters_ja_v1"
LEGACY_RECEIPT_REFERENCE = (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "ymm4_observation_receipt_2026-07-10.json"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _legacy_actual_observation_receipt() -> dict:
    return {
        "schema_version": OBSERVATION_RECEIPT_SCHEMA_VERSION,
        "episode_id": "yukkuri_newsroom_content_spine_002",
        "observed_at": "2026-07-10_JST",
        "status": "partial",
        "result": "pass_with_warnings",
        "actual_ymm4_import_attempted": True,
        "actual_ymm4_imported": True,
        "source_csv": CANONICAL_CSV,
        "source_csv_sha256": CANONICAL_CSV_SHA256,
        "observed_by_environment": {
            "terminal_or_device": "thank",
            "yymm4_version": "4.53.0.9",
            "yymm4_executable_path": r"D:\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe",
            "launch_attempted": True,
            "gui_observation_channel_available": True,
        },
        "five_point_observations": {
            "cue_order": {
                "status": "passed",
                "scene_order": ["S1", "S2", "S3"],
                "cue_order": [f"csv_row_{index}" for index in range(1, 10)],
            },
            "voice_items": {
                "status": "passed",
                "count": 9,
                "missing_cue_ids": [],
                "duplicate_cue_ids": [],
                "reordered": False,
            },
            "subtitle_text": {
                "status": "passed_with_manual_mapping",
                "speaker_mapping": [
                    {"source_speaker": "れいむ", "selected_character": "ゆっくり霊夢"},
                    {"source_speaker": "まりさ", "selected_character": "ゆっくり魔理沙"},
                ],
            },
            "timing_order": {
                "status": "passed_with_variance",
                "order_preserved": True,
                "frame_rate": 60,
                "total_frames": 2790,
                "duration_seconds": 46.5,
            },
            "placeholder_boundary": {
                "status": "not_met",
                "imageitem_placeholder_lanes_present": False,
                "textitem_placeholder_lanes_present": False,
            },
        },
        "import_errors": [],
        "deviations": [
            {
                "deviation_id": "manual_speaker_mapping_required",
                "severity": "adapter_correction_recommended",
            },
            {
                "deviation_id": "imageitem_textitem_placeholder_lanes_absent",
                "severity": "adapter_correction_required",
            },
        ],
        "safety": {
            "application_closed_without_saving": True,
            "render_or_export_performed": False,
            "ymmp_saved_or_written": False,
            "real_input_replaced": False,
            "rights_or_public_approval_performed": False,
            "upload_performed": False,
        },
        "screenshot_or_visual_evidence_paths": [],
        "next_gate": "adapter_correction_after_observation",
        "artifact_id": "receipt_must_not_override_output_identity",
        "public_ready": True,
    }


def _csv_gate_observation_receipt() -> dict:
    return {
        "schema_version": CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION,
        "observation_contract": "ymm4_csv_import_gate.v1",
        "episode_id": "yukkuri_newsroom_content_spine_002",
        "observed_at": "2026-07-11_JST",
        "status": "passed",
        "result": "passed",
        "actual_ymm4_import_attempted": True,
        "actual_ymm4_imported": True,
        "source_csv": DERIVED_CSV,
        "source_csv_sha256": DERIVED_CSV_SHA256,
        "canonical_source_csv": CANONICAL_CSV,
        "canonical_source_csv_sha256": CANONICAL_CSV_SHA256,
        "selected_yymm4_character_profile": CHARACTER_PROFILE,
        "profile_id": CHARACTER_PROFILE_ID,
        "prior_receipt_reference": LEGACY_RECEIPT_REFERENCE,
        "observed_by_environment": {
            "terminal_or_device": "thank",
            "yymm4_version": "4.53.0.9",
            "yymm4_executable_path": r"D:\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe",
            "launch_attempted": True,
            "gui_observation_channel_available": True,
        },
        "five_point_observations": {
            "cue_order": {
                "status": "passed",
                "scene_order": ["S1", "S2", "S3"],
                "cue_order": [f"csv_row_{index}" for index in range(1, 10)],
            },
            "voice_items": {
                "status": "passed",
                "count": 9,
                "missing_cue_ids": [],
                "duplicate_cue_ids": [],
                "reordered": False,
            },
            "subtitle_text": {
                "status": "passed",
                "mapping_dialog_present": False,
                "automatic_speaker_binding_observed": True,
                "all_text_matched": True,
                "speaker_cue_match": True,
                "incorrect_character_cue_ids": [],
                "character_counts": {
                    "ゆっくり霊夢": 3,
                    "ゆっくり魔理沙": 6,
                },
                "speaker_mapping": [
                    {
                        "canonical_speaker": "れいむ",
                        "selected_character": "ゆっくり霊夢",
                        "mapping_mode": "derived_csv_automatic_binding",
                    },
                    {
                        "canonical_speaker": "まりさ",
                        "selected_character": "ゆっくり魔理沙",
                        "mapping_mode": "derived_csv_automatic_binding",
                    },
                ],
            },
            "timing_order": {
                "status": "passed",
                "order_preserved": True,
                "provisional_exact_durations_preserved": False,
                "duration_variance_status": "informational",
                "frame_rate": 60,
                "total_frames": 2790,
                "duration_seconds": 46.5,
            },
            "csv_responsibility_boundary": {
                "status": "passed",
                "csv_import_expected_item_families": [
                    "VoiceItem",
                    "linked_subtitle",
                ],
                "diagnostic_project_expected_item_families": [
                    "ImageItem",
                    "independent_TextItem_placeholders",
                ],
                "diagnostic_project_gate": "not_authorized",
                "diagnostic_project_status": "not_attempted",
                "diagnostic_items_present_during_csv_import": False,
                "diagnostic_item_absence_is_csv_failure": False,
                "misleading_final_or_public_ready_claim_present": False,
            },
        },
        "import_errors": [],
        "deviations": [
            {
                "deviation_id": "provisional_timing_recomputed_by_yymm4",
                "severity": "informational",
            }
        ],
        "safety": {
            "application_closed_without_saving": True,
            "render_or_export_performed": False,
            "ymmp_saved_or_written": False,
            "real_input_replaced": False,
            "rights_or_public_approval_performed": False,
            "upload_performed": False,
        },
        "screenshot_or_visual_evidence_paths": [],
        "next_gate": "supervisor_next_slice_decision",
    }


def test_ymm4_observation_readback_builds_operator_instruction_package(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_observation_readback_pack"

    readback = build_ymm4_observation_readback_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )

    assert readback["validation_status"] == "passed"
    assert readback["status"] == "blocked"
    for filename in REQUIRED_YMM4_OBSERVATION_FILES:
        assert (output_dir / filename).exists(), filename

    observation = _load(output_dir / "observation_readback.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    html = (output_dir / "observation_preview.html").read_text(encoding="utf-8")
    manual = (output_dir / "manual_ymm4_observation_readback.md").read_text(encoding="utf-8")

    assert observation["artifact_id"] == DEFAULT_ARTIFACT_ID
    assert observation["episode_id"] == "yukkuri_newsroom_content_spine_002"
    assert observation["source_import_ready_pack_reference"].endswith("ymm4_import_ready_pack")
    assert observation["source_real_input_prep_reference"].endswith("real_input_replacement_readiness_pack")
    assert observation["observation_mode"] == "operator_instruction_only"
    assert observation["actual_ymm4_import_attempted"] is False
    assert observation["actual_ymm4_imported"] is False
    assert observation["cue_count_expected"] == 9
    assert observation["scene_count_expected"] == 3
    assert observation["cue_count_observed"] == 0
    assert observation["voice_item_observed"] == "not_observed"
    assert observation["subtitle_item_observed"] == "not_observed"
    assert observation["timing_order_observed"] == "not_observed"
    assert observation["responsibility_boundary_observed"] == "not_observed"
    assert observation["observation_contract"] == "ymm4_csv_import_gate.v1"
    assert observation["receipt_schema_version"] is None
    assert observation["expected_import_path"] == DERIVED_CSV
    assert observation["derived_import_csv"] == DERIVED_CSV
    assert observation["canonical_source_csv"] == CANONICAL_CSV
    assert observation["selected_yymm4_character_profile"] == CHARACTER_PROFILE
    assert observation["csv_import_gate"] == {
        "contract": "ymm4_csv_import_gate.v1",
        "expected_item_families": ["VoiceItem", "linked_subtitle"],
        "status": "not_observed",
    }
    assert observation["diagnostic_project_gate"] == {
        "expected_item_families": [
            "ImageItem",
            "independent_TextItem_placeholders",
        ],
        "authorization_status": "not_authorized",
        "execution_status": "not_attempted",
        "absence_during_csv_import_is_failure": False,
    }
    assert observation["screenshot_or_visual_evidence_paths"] == []
    assert observation["rendered_video_created"] is False
    assert observation["ymmp_file_created"] is False
    assert observation["production_ymmp_written"] is False
    assert observation["real_input_replaced"] is False
    assert observation["rights_approved"] is False
    assert observation["public_ready"] is False
    assert observation["next_gate"] == "bounded_yymm4_alias_reobservation"
    assert all(value is False for value in observation["closed_gate_flags"].values())
    assert source_index["ymm4_import_ready_pack_read_only"] is True
    assert source_index["real_input_prep_pack_read_only"] is True
    records = {record["record_id"]: record for record in source_index["records"]}
    assert records["ymm4_derived_csv"]["repo_relative_path"] == DERIVED_CSV
    assert records["canonical_csv"]["repo_relative_path"] == CANONICAL_CSV
    assert records["prior_gui_observation_receipt"]["repo_relative_path"] == (
        LEGACY_RECEIPT_REFERENCE
    )
    assert '<html lang="ja"' in html
    assert 'data-ymm4-observation-readback="true"' in html
    assert 'data-region="pipeline-runway"' in html
    assert 'data-region="observation-matrix"' in html
    assert 'data-region="closed-gates"' in html
    assert "実観測は未実行" in html
    assert "card-grid" not in html
    assert "operatorが返す観測5点" in manual
    assert "mapping dialogが出ず" in manual
    assert "not_authorized/not_attempted" in manual
    assert "Do not render/export" in manual
    assert manual.count("\n1.") == 1
    assert manual.count("\n5.") == 1


def test_ymm4_observation_validation_catches_missing_manual_sheet(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_observation_readback_pack"
    build_ymm4_observation_readback_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )
    (output_dir / "manual_ymm4_observation_readback.md").unlink()

    readback = validate_ymm4_observation_readback_pack(output_dir)

    assert readback["validation_status"] == "failed"
    assert "missing_file:manual_ymm4_observation_readback.md" in readback["failed_checks"]


def test_ymm4_observation_validation_rejects_unhandled_blocked_mode(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_observation_readback_pack"
    build_ymm4_observation_readback_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )
    observation_path = output_dir / "observation_readback.json"
    observation = _load(observation_path)
    observation["observation_mode"] = "blocked"
    observation_path.write_text(
        json.dumps(observation, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    readback = validate_ymm4_observation_readback_pack(output_dir)

    assert readback["validation_status"] == "failed"
    assert "observation_mode_invalid" in readback["failed_checks"]


def test_ymm4_observation_readback_accepts_actual_gui_receipt_safely(tmp_path) -> None:
    output_dir = tmp_path / "actual_ymm4_observation_readback_pack"
    receipt_path = tmp_path / "actual_ymm4_observation_receipt.json"
    receipt_path.write_text(
        json.dumps(_legacy_actual_observation_receipt(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    readback = build_ymm4_observation_readback_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
        observation_receipt=receipt_path,
    )

    assert readback["validation_status"] == "passed"
    assert readback["status"] == "partial"
    assert readback["artifact_id"] == DEFAULT_ARTIFACT_ID
    assert readback["receipt_schema_version"] == OBSERVATION_RECEIPT_SCHEMA_VERSION
    assert readback["observation_contract"] == "legacy_five_point_observation.v1"
    assert readback["observation_mode"] == "actual_ymm4_gui_observation"
    assert readback["actual_ymm4_import_attempted"] is True
    assert readback["actual_ymm4_imported"] is True
    assert readback["cue_count_observed"] == 9
    assert readback["scene_order_observed"] == ["S1", "S2", "S3"]
    assert readback["cue_order_observed"] == [f"csv_row_{index}" for index in range(1, 10)]
    assert readback["expected_import_path"] == CANONICAL_CSV
    assert readback["receipt_source_csv"] == CANONICAL_CSV
    assert readback["responsibility_boundary_observed"] == (
        "legacy_imageitem_textitem_placeholder_lanes_absent"
    )
    assert readback["next_gate"] == "adapter_correction_after_observation"
    assert readback["public_ready"] is False
    assert all(value is False for value in readback["closed_gate_flags"].values())

    source_index = _load(output_dir / "source_artifact_index.json")
    records = {record["record_id"]: record for record in source_index["records"]}
    assert "actual_gui_observation_receipt" in records
    html = (output_dir / "observation_preview.html").read_text(encoding="utf-8")
    manual = (output_dir / "manual_ymm4_observation_readback.md").read_text(encoding="utf-8")
    limitations = (output_dir / "limitations.md").read_text(encoding="utf-8")
    assert "実YMM4 GUIでbounded importを観測済み" in html
    assert "実観測は未実行" not in html
    assert "実観測結果5点" in manual
    assert "ImageItem/TextItem placeholder scene laneはない" in manual
    assert "immutable historical v1 evidence" in limitations


def test_original_v1_receipt_remains_byte_immutable_and_historical(tmp_path) -> None:
    before = LEGACY_RECEIPT_PATH.read_bytes()
    assert hashlib.sha256(before).hexdigest().upper() == LEGACY_RECEIPT_SHA256

    readback = build_ymm4_observation_readback_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=tmp_path / "legacy_receipt_readback",
        artifact_id=DEFAULT_ARTIFACT_ID,
        observation_receipt=LEGACY_RECEIPT_PATH,
    )

    after = LEGACY_RECEIPT_PATH.read_bytes()
    assert after == before
    assert hashlib.sha256(after).hexdigest().upper() == LEGACY_RECEIPT_SHA256
    assert readback["validation_status"] == "passed"
    assert readback["status"] == "partial"
    assert readback["receipt_schema_version"] == OBSERVATION_RECEIPT_SCHEMA_VERSION
    assert readback["observation_contract"] == "legacy_five_point_observation.v1"
    assert readback["prior_observation_evidence"] == {
        "receipt": LEGACY_RECEIPT_REFERENCE,
        "receipt_sha256": LEGACY_RECEIPT_SHA256,
        "schema_version": OBSERVATION_RECEIPT_SCHEMA_VERSION,
        "status": "partial",
        "interpretation": "historical_result_under_legacy_placeholder_contract",
    }


def test_ymm4_observation_readback_accepts_passed_csv_gate_without_diagnostic_items(
    tmp_path,
) -> None:
    output_dir = tmp_path / "csv_gate_observation_readback_pack"
    receipt_path = tmp_path / "csv_gate_observation_receipt.json"
    receipt_path.write_text(
        json.dumps(_csv_gate_observation_receipt(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    readback = build_ymm4_observation_readback_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
        observation_receipt=receipt_path,
    )

    assert readback["validation_status"] == "passed"
    assert readback["status"] == "passed"
    assert readback["observation_result"] == "passed"
    assert readback["receipt_schema_version"] == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION
    assert readback["observation_contract"] == "ymm4_csv_import_gate.v1"
    assert readback["observation_mode"] == "actual_ymm4_gui_observation"
    assert readback["expected_import_path"] == DERIVED_CSV
    assert readback["receipt_source_csv"] == DERIVED_CSV
    assert readback["source_csv_sha256"] == DERIVED_CSV_SHA256
    assert readback["canonical_source_csv"] == CANONICAL_CSV
    assert readback["canonical_source_csv_sha256"] == CANONICAL_CSV_SHA256
    assert readback["selected_yymm4_character_profile"] == CHARACTER_PROFILE
    assert readback["profile_id"] == CHARACTER_PROFILE_ID
    assert readback["cue_count_observed"] == 9
    assert readback["scene_order_observed"] == ["S1", "S2", "S3"]
    assert readback["cue_order_observed"] == [
        f"csv_row_{index}" for index in range(1, 10)
    ]
    assert readback["mapping_dialog_present"] is False
    assert readback["character_counts"] == {
        "ゆっくり霊夢": 3,
        "ゆっくり魔理沙": 6,
    }
    assert readback["subtitle_item_observed"] == (
        "linked_subtitle_texts_match_with_automatic_character_binding"
    )
    assert readback["timing_order_observed"] == (
        "order_preserved_actual_voice_duration_46.5_seconds"
    )
    assert readback["responsibility_boundary_observed"] == (
        "csv_voiceitem_linked_subtitle_only_diagnostic_project_not_authorized_not_attempted"
    )
    assert readback["csv_import_gate"] == {
        "contract": "ymm4_csv_import_gate.v1",
        "expected_item_families": ["VoiceItem", "linked_subtitle"],
        "status": "passed",
    }
    assert readback["diagnostic_project_gate"] == {
        "expected_item_families": [
            "ImageItem",
            "independent_TextItem_placeholders",
        ],
        "authorization_status": "not_authorized",
        "execution_status": "not_attempted",
        "absence_during_csv_import_is_failure": False,
    }
    assert readback["diagnostic_ymmp_project_attempted"] is False
    assert readback["next_gate"] == "supervisor_next_slice_decision"
    assert all(value is False for value in readback["closed_gate_flags"].values())

    observations = readback["five_point_observations"]
    assert observations["voice_items"]["count"] == 9
    assert observations["subtitle_text"]["mapping_dialog_present"] is False
    assert observations["subtitle_text"]["automatic_speaker_binding_observed"] is True
    assert observations["subtitle_text"]["all_text_matched"] is True
    assert observations["subtitle_text"]["speaker_cue_match"] is True
    assert observations["subtitle_text"]["incorrect_character_cue_ids"] == []
    assert observations["timing_order"]["order_preserved"] is True
    boundary = observations["csv_responsibility_boundary"]
    assert boundary["diagnostic_project_gate"] == "not_authorized"
    assert boundary["diagnostic_project_status"] == "not_attempted"
    assert boundary["diagnostic_items_present_during_csv_import"] is False
    assert boundary["diagnostic_item_absence_is_csv_failure"] is False

    source_index = _load(output_dir / "source_artifact_index.json")
    records = {record["record_id"]: record for record in source_index["records"]}
    assert records["ymm4_derived_csv"]["repo_relative_path"] == DERIVED_CSV
    assert records["canonical_csv"]["repo_relative_path"] == CANONICAL_CSV
    assert records["prior_gui_observation_receipt"]["role"] == (
        "immutable_legacy_partial_evidence"
    )
    assert "actual_gui_observation_receipt" in records

    manual = (output_dir / "manual_ymm4_observation_readback.md").read_text(
        encoding="utf-8"
    )
    limitations = (output_dir / "limitations.md").read_text(encoding="utf-8")
    assert "CSV gate 実観測結果5点" in manual
    assert "mapping_dialog_present=False" in manual
    assert "diagnostic project=not_authorized/not_attempted" in manual
    assert "supervisor_next_slice_decision" in manual
    assert "ImageItem or independent TextItem absence is not a CSV failure" in limitations


@pytest.mark.parametrize(
    "gap",
    [
        "mapping_dialog",
        "voice_count",
        "character_counts",
        "text_match",
        "cue_order",
        "timing_order",
        "diagnostic_gate",
        "diagnostic_status",
        "next_gate",
    ],
)
def test_ymm4_observation_readback_rejects_false_csv_gate_pass(tmp_path, gap) -> None:
    receipt = _csv_gate_observation_receipt()
    observations = receipt["five_point_observations"]
    if gap == "mapping_dialog":
        observations["subtitle_text"]["mapping_dialog_present"] = True
    elif gap == "voice_count":
        observations["voice_items"]["count"] = 8
    elif gap == "character_counts":
        observations["subtitle_text"]["character_counts"] = {
            "ゆっくり霊夢": 9,
            "ゆっくり魔理沙": 0,
        }
    elif gap == "text_match":
        observations["subtitle_text"]["all_text_matched"] = False
    elif gap == "cue_order":
        observations["cue_order"]["cue_order"] = list(
            reversed(observations["cue_order"]["cue_order"])
        )
    elif gap == "timing_order":
        observations["timing_order"]["order_preserved"] = False
    elif gap == "diagnostic_gate":
        observations["csv_responsibility_boundary"]["diagnostic_project_gate"] = (
            "authorized"
        )
    elif gap == "diagnostic_status":
        observations["csv_responsibility_boundary"]["diagnostic_project_status"] = (
            "attempted"
        )
    elif gap == "next_gate":
        receipt["next_gate"] = "render_proof_after_observation"

    receipt_path = tmp_path / f"false_csv_gate_{gap}.json"
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="requires all five checks to pass|must advance to supervisor decision",
    ):
        build_ymm4_observation_readback_pack(
            package_dir=SOURCE_PACKAGE,
            output_dir=tmp_path / f"false_csv_gate_{gap}",
            artifact_id=DEFAULT_ARTIFACT_ID,
            observation_receipt=receipt_path,
        )


def test_ymm4_observation_readback_rejects_missing_explicit_receipt(tmp_path) -> None:
    with pytest.raises(FileNotFoundError, match="observation receipt not found"):
        build_ymm4_observation_readback_pack(
            package_dir=SOURCE_PACKAGE,
            output_dir=tmp_path / "output",
            artifact_id=DEFAULT_ARTIFACT_ID,
            observation_receipt=tmp_path / "missing.json",
        )


def test_ymm4_observation_readback_records_existing_unsaved_project_blocker(tmp_path) -> None:
    output_dir = tmp_path / "blocked_ymm4_observation_readback_pack"

    readback = build_ymm4_observation_readback_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
        observation_blocker=BLOCKER_RECEIPT,
    )

    assert readback["validation_status"] == "passed"
    assert readback["status"] == "blocked"
    assert readback["expected_import_path"].endswith("derived_yymm4_import.csv")
    assert readback["blocker"]["blocker_id"] == (
        "existing_unsaved_project_requires_discard_authorization"
    )
    assert readback["observed_by_environment"]["gui_observation_channel_available"] is True
    assert readback["actual_ymm4_import_attempted"] is False
    assert readback["safety"]["existing_project_discarded"] is False
    assert readback["safety"]["application_left_open_to_preserve_unsaved_state"] is True
    records = {
        record["record_id"]
        for record in _load(output_dir / "source_artifact_index.json")["records"]
    }
    assert "actual_gui_observation_blocker" in records


def test_ymm4_observation_readback_rejects_mismatched_source_hash(tmp_path) -> None:
    receipt = _legacy_actual_observation_receipt()
    receipt["source_csv_sha256"] = "0" * 64
    receipt_path = tmp_path / "mismatched_source_receipt.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="source_csv_sha256 does not match"):
        build_ymm4_observation_readback_pack(
            package_dir=SOURCE_PACKAGE,
            output_dir=tmp_path / "output",
            artifact_id=DEFAULT_ARTIFACT_ID,
            observation_receipt=receipt_path,
        )


def test_ymm4_observation_readback_rejects_open_safety_gate(tmp_path) -> None:
    receipt = _legacy_actual_observation_receipt()
    receipt["safety"]["render_or_export_performed"] = True
    receipt_path = tmp_path / "unsafe_receipt.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="safety field must be false"):
        build_ymm4_observation_readback_pack(
            package_dir=SOURCE_PACKAGE,
            output_dir=tmp_path / "output",
            artifact_id=DEFAULT_ARTIFACT_ID,
            observation_receipt=receipt_path,
        )


def test_ymm4_observation_readback_rejects_pass_claim_with_observed_gap(tmp_path) -> None:
    receipt = _legacy_actual_observation_receipt()
    receipt["status"] = "passed"
    receipt["result"] = "passed"
    receipt["next_gate"] = "render_proof_after_observation"
    receipt_path = tmp_path / "false_pass_receipt.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="requires all five checks to pass"):
        build_ymm4_observation_readback_pack(
            package_dir=SOURCE_PACKAGE,
            output_dir=tmp_path / "output",
            artifact_id=DEFAULT_ARTIFACT_ID,
            observation_receipt=receipt_path,
        )


def test_cli_build_ymm4_observation_readback_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_ymm4_observation_readback_pack"

    code = main(
        [
            "build-ymm4-observation-readback-pack",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            DEFAULT_ARTIFACT_ID,
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["validation_status"] == "passed"
    assert payload["status"] == "blocked"
    assert payload["primary_review_file"].endswith("observation_preview.html")
    assert payload["observation_mode"] == "operator_instruction_only"
    assert payload["actual_ymm4_import_attempted"] is False
    assert payload["actual_ymm4_imported"] is False
    assert payload["cue_count_expected"] == 9
    assert payload["cue_count_observed"] == 0
    assert payload["voice_item_observed"] == "not_observed"
    assert payload["subtitle_item_observed"] == "not_observed"
    assert payload["timing_order_observed"] == "not_observed"
    assert payload["responsibility_boundary_observed"] == "not_observed"
    assert payload["observation_contract"] == "ymm4_csv_import_gate.v1"
    assert payload["expected_import_path"] == DERIVED_CSV
    assert payload["canonical_source_csv"] == CANONICAL_CSV
    assert payload["next_gate"] == "bounded_yymm4_alias_reobservation"
    assert payload["csv_import_gate"]["expected_item_families"] == [
        "VoiceItem",
        "linked_subtitle",
    ]
    assert payload["diagnostic_project_gate"]["authorization_status"] == (
        "not_authorized"
    )
    assert payload["diagnostic_project_gate"]["execution_status"] == "not_attempted"
    assert payload["rendered_video_created"] is False
    assert payload["ymmp_file_created"] is False
    assert payload["production_ymmp_written"] is False
    assert payload["real_input_replaced"] is False
    assert payload["rights_approved"] is False
    assert payload["public_ready"] is False


def test_cli_build_ymm4_observation_readback_with_actual_receipt(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_actual_ymm4_observation_readback_pack"
    receipt_path = tmp_path / "actual_ymm4_observation_receipt.json"
    receipt_path.write_text(
        json.dumps(_csv_gate_observation_receipt(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    code = main(
        [
            "build-ymm4-observation-readback-pack",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            DEFAULT_ARTIFACT_ID,
            "--observation-receipt",
            str(receipt_path),
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["validation_status"] == "passed"
    assert payload["status"] == "passed"
    assert payload["observation_mode"] == "actual_ymm4_gui_observation"
    assert payload["receipt_schema_version"] == CSV_GATE_OBSERVATION_RECEIPT_SCHEMA_VERSION
    assert payload["cue_count_observed"] == 9
    assert payload["mapping_dialog_present"] is False
    assert payload["character_counts"] == {
        "ゆっくり霊夢": 3,
        "ゆっくり魔理沙": 6,
    }
    assert payload["responsibility_boundary_observed"] == (
        "csv_voiceitem_linked_subtitle_only_diagnostic_project_not_authorized_not_attempted"
    )
    assert payload["next_gate"] == "supervisor_next_slice_decision"


def test_detect_yymm4_uses_environment_override_and_current_home(tmp_path, monkeypatch) -> None:
    executable = tmp_path / "YukkuriMovieMaker.exe"
    executable.touch()
    monkeypatch.setenv("NLMYTGEN_YMM4_EXE", str(executable))

    detected = _detect_yymm4()

    assert detected["terminal_or_device"] == Path.home().name
    assert detected["yymm4_executable_detected"] is True
    assert detected["yymm4_executable_path"] == str(executable)
    assert detected["environment_override_used"] is True


def test_ymm4_observation_readback_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_observation_readback_pack"
    build_ymm4_observation_readback_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )

    readback = _load(output_dir / "observation_readback.json")
    assert readback["validation_status"] == "passed"
    assert readback["checks"]["external_dependency_status"] == "none_found"
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["temporary_copy_absent"] is True

    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for marker in EXTERNAL_REF_MARKERS:
            assert marker not in text, (path.name, marker)

    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_TRUE_CLAIMS:
            assert forbidden not in text, (path.name, forbidden)
