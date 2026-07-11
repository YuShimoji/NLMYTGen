from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import pytest

from src.cli.main import main as cli_main
from src.pipeline.ymm4_diagnostic_placeholder_proof import (
    CANONICAL_CSV,
    DERIVED_CSV,
    GUI_RECEIPT_SCHEMA_VERSION,
    MANIFEST_FILENAME,
    PROJECT_FILENAME,
    READBACK_FILENAME,
    RECEIPT_FILENAME,
    build_blocked_gui_observation_receipt,
    build_gui_observation_receipt,
    build_ymm4_diagnostic_placeholder_proof,
    validate_gui_observation_receipt,
    validate_ymm4_diagnostic_placeholder_proof,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp, save_ymmp


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = REPO_ROOT / "production_pilots/yukkuri_newsroom_content_spine_002"
FRAMES = [0, 273, 566, 771, 1100, 1341, 1647, 2076, 2317]
LENGTHS = [273, 293, 205, 329, 241, 306, 429, 241, 473]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _rows(path: Path) -> list[tuple[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [(row[0], row[1]) for row in csv.reader(handle) if row]


def _write_source_project(path: Path, *, row_count: int = 9) -> list[dict]:
    rows = _rows(PACKAGE / DERIVED_CSV)[:row_count]
    voice_items = [
        {
            "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
            "CharacterName": character,
            "Serif": text,
            "Frame": FRAMES[index],
            "Length": LENGTHS[index],
            "Layer": index % 2,
            "Group": 0,
            "IsLocked": False,
            "IsHidden": False,
        }
        for index, (character, text) in enumerate(rows)
    ]
    project = {
        "FilePath": str(path.resolve()),
        "SelectedTimelineIndex": 0,
        "Timelines": [
            {
                "ID": "episode-002-test-timeline",
                "Name": "メイン",
                "VideoInfo": {"FPS": 60, "Hz": 48000, "Width": 1920, "Height": 1080},
                "VerticalLine": {"IsEnabled": False, "StartFrame": 0},
                "Items": voice_items,
                "LayerSettings": {"Items": []},
                "CurrentFrame": 0,
                "Length": FRAMES[row_count - 1] + LENGTHS[row_count - 1],
                "MaxLayer": 1,
            }
        ],
        "Characters": [],
    }
    save_ymmp(project, path)
    return voice_items


def _write_csv_gate_receipt(path: Path) -> None:
    prefix = "production_pilots/yukkuri_newsroom_content_spine_002/"
    payload = {
        "schema_version": "ymm4_gui_observation_receipt.v2",
        "observation_contract": "ymm4_csv_import_gate.v1",
        "episode_id": "yukkuri_newsroom_content_spine_002",
        "observed_at": "2026-07-11_JST",
        "status": "passed",
        "result": "passed",
        "actual_ymm4_import_attempted": True,
        "actual_ymm4_imported": True,
        "source_csv": prefix + DERIVED_CSV.as_posix(),
        "source_csv_sha256": _sha256(PACKAGE / DERIVED_CSV),
        "canonical_source_csv": prefix + CANONICAL_CSV.as_posix(),
        "canonical_source_csv_sha256": _sha256(PACKAGE / CANONICAL_CSV),
        "selected_yymm4_character_profile": (
            prefix
            + "ymm4_character_alias_profiles/"
            "ymm4_4_53_0_9_yukkuri_characters_v1.json"
        ),
        "profile_id": "ymm4_4_53_0_9_yukkuri_characters_ja_v1",
        "prior_receipt_reference": prefix + "ymm4_observation_receipt_2026-07-10.json",
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
                "character_counts": {"ゆっくり霊夢": 3, "ゆっくり魔理沙": 6},
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
                "csv_import_expected_item_families": ["VoiceItem", "linked_subtitle"],
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
            "application_closed_without_saving": False,
            "application_left_open_for_authorized_diagnostic_project": True,
            "render_or_export_performed": False,
            "ymmp_saved_or_written": False,
            "real_input_replaced": False,
            "rights_or_public_approval_performed": False,
            "upload_performed": False,
        },
        "screenshot_or_visual_evidence_paths": [],
        "next_gate": "supervisor_next_slice_decision",
    }
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _build(tmp_path: Path, output_name: str = "proof") -> dict:
    source = tmp_path / "episode_002_imported_base.local.ymmp"
    receipt = tmp_path / "csv_gate_receipt.json"
    _write_source_project(source)
    _write_csv_gate_receipt(receipt)
    return build_ymm4_diagnostic_placeholder_proof(
        package_dir=PACKAGE,
        source_ymmp=source,
        csv_gate_receipt=receipt,
        output_dir=tmp_path / output_name,
    )


def test_builds_three_scene_diagnostic_project_without_mutating_voice_items(tmp_path: Path) -> None:
    source = tmp_path / "episode_002_imported_base.local.ymmp"
    receipt = tmp_path / "csv_gate_receipt.json"
    source_voice_items = _write_source_project(source)
    _write_csv_gate_receipt(receipt)

    result = build_ymm4_diagnostic_placeholder_proof(
        package_dir=PACKAGE,
        source_ymmp=source,
        csv_gate_receipt=receipt,
        output_dir=tmp_path / "proof",
    )

    assert result["status"] == "diagnostic_placeholder_proof_ready"
    proof = tmp_path / "proof"
    project = load_ymmp(proof / PROJECT_FILENAME)
    items = _get_timeline_items(project)
    voices = [item for item in items if _item_type(item) == "VoiceItem"]
    images = [item for item in items if _item_type(item) == "ImageItem"]
    texts = [item for item in items if _item_type(item) == "TextItem"]
    assert voices == source_voice_items
    assert len(images) == 3
    assert len(texts) == 3
    assert [item["Text"] for item in texts] == [
        "S1 | DIAGNOSTIC | NOT FINAL | SAMPLE / PLACEHOLDER",
        "S2 | DIAGNOSTIC | NOT FINAL | SAMPLE / PLACEHOLDER",
        "S3 | DIAGNOSTIC | NOT FINAL | SAMPLE / PLACEHOLDER",
    ]
    assert [(item["Frame"], item["Length"]) for item in images] == [
        (0, 566),
        (566, 534),
        (1100, 1690),
    ]

    readback = json.loads((proof / READBACK_FILENAME).read_text(encoding="utf-8"))
    assert readback["status"] == "structural_pass"
    assert readback["timeline"]["item_type_counts"] == {
        "VoiceItem": 9,
        "ImageItem": 3,
        "TextItem": 3,
    }
    assert all(readback["checks"].values())
    assert readback["path_audit"]["commit_disposition"] == (
        "local_only_not_committed_absolute_asset_reference"
    )
    assert (proof / RECEIPT_FILENAME).exists()


def test_metadata_is_sanitized_and_regeneration_is_deterministic(tmp_path: Path) -> None:
    first = _build(tmp_path, "proof_a")
    second = _build(tmp_path, "proof_b")

    assert first["readback"]["normalized_project_sha256"] == second["readback"][
        "normalized_project_sha256"
    ]
    assert first["readback"]["asset"]["sha256"] == second["readback"]["asset"][
        "sha256"
    ]
    first_project_hash = first["readback"]["project_sha256"]
    rebuilt = build_ymm4_diagnostic_placeholder_proof(
        package_dir=PACKAGE,
        source_ymmp=tmp_path / "episode_002_imported_base.local.ymmp",
        csv_gate_receipt=tmp_path / "csv_gate_receipt.json",
        output_dir=tmp_path / "proof_a",
    )
    assert rebuilt["readback"]["project_sha256"] == first_project_hash

    for filename in (MANIFEST_FILENAME, READBACK_FILENAME, RECEIPT_FILENAME):
        text = (tmp_path / "proof_a" / filename).read_text(encoding="utf-8")
        assert str(tmp_path) not in text
        assert "C:\\Users\\" not in text


def test_rejects_non_nine_voiceitem_source(tmp_path: Path) -> None:
    source = tmp_path / "short.local.ymmp"
    receipt = tmp_path / "receipt.json"
    _write_source_project(source, row_count=8)
    _write_csv_gate_receipt(receipt)

    with pytest.raises(ValueError, match="SOURCE_PROJECT_VOICEITEM_COUNT_MISMATCH"):
        build_ymm4_diagnostic_placeholder_proof(
            package_dir=PACKAGE,
            source_ymmp=source,
            csv_gate_receipt=receipt,
            output_dir=tmp_path / "proof",
        )


def test_rejects_raw_voiceitem_reorder_and_duplicate_frame(tmp_path: Path) -> None:
    receipt = tmp_path / "receipt.json"
    _write_csv_gate_receipt(receipt)

    reordered = tmp_path / "reordered.local.ymmp"
    _write_source_project(reordered)
    reordered_project = load_ymmp(reordered)
    reordered_items = _get_timeline_items(reordered_project)
    reordered_items[0], reordered_items[1] = reordered_items[1], reordered_items[0]
    save_ymmp(reordered_project, reordered)
    with pytest.raises(
        ValueError,
        match="SOURCE_PROJECT_VOICEITEM_TEXT_OR_CHARACTER_ORDER_MISMATCH",
    ):
        build_ymm4_diagnostic_placeholder_proof(
            package_dir=PACKAGE,
            source_ymmp=reordered,
            csv_gate_receipt=receipt,
            output_dir=tmp_path / "reordered_proof",
        )

    duplicate = tmp_path / "duplicate.local.ymmp"
    _write_source_project(duplicate)
    duplicate_project = load_ymmp(duplicate)
    duplicate_items = _get_timeline_items(duplicate_project)
    duplicate_items[1]["Frame"] = duplicate_items[0]["Frame"]
    save_ymmp(duplicate_project, duplicate)
    with pytest.raises(ValueError, match="SOURCE_PROJECT_VOICEITEM_TIMING_ORDER_MISMATCH"):
        build_ymm4_diagnostic_placeholder_proof(
            package_dir=PACKAGE,
            source_ymmp=duplicate,
            csv_gate_receipt=receipt,
            output_dir=tmp_path / "duplicate_proof",
        )


def test_binds_csv_receipt_timing_and_yymm4_version_to_source(tmp_path: Path) -> None:
    source = tmp_path / "timing.local.ymmp"
    receipt = tmp_path / "receipt.json"
    _write_source_project(source)
    _write_csv_gate_receipt(receipt)

    wrong_timing = load_ymmp(source)
    wrong_timing["Timelines"][0]["Length"] = 2789
    save_ymmp(wrong_timing, source)
    with pytest.raises(ValueError, match="SOURCE_PROJECT_TIMING_RECEIPT_MISMATCH"):
        build_ymm4_diagnostic_placeholder_proof(
            package_dir=PACKAGE,
            source_ymmp=source,
            csv_gate_receipt=receipt,
            output_dir=tmp_path / "timing_proof",
        )

    _write_source_project(source)
    receipt_payload = json.loads(receipt.read_text(encoding="utf-8"))
    receipt_payload["observed_by_environment"]["yymm4_version"] = "4.53.0.8"
    receipt.write_text(json.dumps(receipt_payload, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="CSV_GATE_RECEIPT_PROFILE_YMM4_VERSION_MISMATCH"):
        build_ymm4_diagnostic_placeholder_proof(
            package_dir=PACKAGE,
            source_ymmp=source,
            csv_gate_receipt=receipt,
            output_dir=tmp_path / "version_proof",
        )


def test_gui_receipt_requires_exact_diagnostic_observation(tmp_path: Path) -> None:
    _build(tmp_path)
    observations = {
        "opened_without_error": True,
        "unexpected_dialog_present": False,
        "VoiceItems": 9,
        "character_counts": {"ゆっくり霊夢": 3, "ゆっくり魔理沙": 6},
        "linked_subtitles_preserved": True,
        "ImageItems": 3,
        "independent_TextItems": 3,
        "placeholder_is_explicitly_non_final": True,
        "render_or_export_performed": False,
        "scene_labels_readable": [
            "S1 | DIAGNOSTIC | NOT FINAL | SAMPLE / PLACEHOLDER",
            "S2 | DIAGNOSTIC | NOT FINAL | SAMPLE / PLACEHOLDER",
            "S3 | DIAGNOSTIC | NOT FINAL | SAMPLE / PLACEHOLDER",
        ],
    }
    safety = {
        "diagnostic_only": True,
        "production_ymmp_written": False,
        "render_or_export_performed": False,
        "real_input_replaced": False,
        "rights_or_public_approval_performed": False,
        "final_thumbnail_approval": False,
        "public_ready": False,
        "upload_performed": False,
    }
    receipt = build_gui_observation_receipt(
        proof_dir=tmp_path / "proof",
        observed_at="2026-07-11T12:00:00+09:00",
        yymm4_version="4.53.0.9",
        observations=observations,
        safety=safety,
        application_close_state="left_open_with_saved_diagnostic_project",
        screenshot=None,
    )

    assert receipt["schema_version"] == GUI_RECEIPT_SCHEMA_VERSION
    assert receipt["status"] == "passed"
    validate_gui_observation_receipt(receipt, proof_dir=tmp_path / "proof")
    bad_count = copy.deepcopy(receipt)
    bad_count["observations"]["ImageItems"] = 2
    with pytest.raises(ValueError, match="OBSERVATION_MISMATCH"):
        validate_gui_observation_receipt(bad_count, proof_dir=tmp_path / "proof")
    unsafe = copy.deepcopy(receipt)
    unsafe["safety"]["public_ready"] = True
    with pytest.raises(ValueError, match="SAFETY_MISMATCH"):
        validate_gui_observation_receipt(unsafe, proof_dir=tmp_path / "proof")
    extra_claim = copy.deepcopy(receipt)
    extra_claim["public_ready"] = True
    with pytest.raises(ValueError, match="FIELD_SET_MISMATCH"):
        validate_gui_observation_receipt(extra_claim, proof_dir=tmp_path / "proof")
    extra_observation = copy.deepcopy(receipt)
    extra_observation["observations"]["rights_approved"] = True
    with pytest.raises(ValueError, match="OBSERVATION_MISMATCH"):
        validate_gui_observation_receipt(extra_observation, proof_dir=tmp_path / "proof")
    wrong_version = copy.deepcopy(receipt)
    wrong_version["observed_by_environment"]["yymm4_version"] = "4.53.0.8"
    with pytest.raises(ValueError, match="YMM4_VERSION_MISMATCH"):
        validate_gui_observation_receipt(wrong_version, proof_dir=tmp_path / "proof")

    blocked = build_blocked_gui_observation_receipt(
        proof_dir=tmp_path / "proof",
        observed_at="2026-07-11T12:01:00+09:00",
        yymm4_version="4.53.0.9",
        blocker={"blocker_id": "open_failed", "detail": "YMM4 parse dialog"},
        safety=safety,
        application_close_state="left_open_after_observation_blocker",
        screenshot=None,
    )
    blocked["observations"] = {"public_ready": True}
    with pytest.raises(ValueError, match="OBSERVATIONS_MUST_BE_EMPTY"):
        validate_gui_observation_receipt(blocked, proof_dir=tmp_path / "proof")

    readback_path = tmp_path / "proof" / READBACK_FILENAME
    original_readback = readback_path.read_text(encoding="utf-8")
    blocked_readback = json.loads(original_readback)
    blocked_readback["status"] = "blocked"
    readback_path.write_text(
        json.dumps(blocked_readback, ensure_ascii=False),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="READBACK_NOT_STRUCTURAL_PASS"):
        validate_gui_observation_receipt(receipt, proof_dir=tmp_path / "proof")
    readback_path.write_text(original_readback, encoding="utf-8")


def test_independent_validator_detects_tracked_artifact_tamper(tmp_path: Path) -> None:
    _build(tmp_path)
    proof = tmp_path / "proof"
    source = tmp_path / "episode_002_imported_base.local.ymmp"
    receipt = tmp_path / "csv_gate_receipt.json"

    valid = validate_ymm4_diagnostic_placeholder_proof(
        proof_dir=proof,
        package_dir=PACKAGE,
        source_ymmp=source,
        csv_gate_receipt=receipt,
    )
    assert valid == {"status": "passed", "errors": []}

    readme = proof / "README_DIAGNOSTIC_PLACEHOLDER_PROOF.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "tamper\n", encoding="utf-8")
    invalid = validate_ymm4_diagnostic_placeholder_proof(
        proof_dir=proof,
        package_dir=PACKAGE,
        source_ymmp=source,
        csv_gate_receipt=receipt,
    )
    assert invalid["status"] == "failed"
    assert "README_RECOMPUTE_MISMATCH" in invalid["errors"]


def test_cli_builds_diagnostic_placeholder_proof(tmp_path: Path, capsys) -> None:
    source = tmp_path / "episode_002_imported_base.local.ymmp"
    receipt = tmp_path / "csv_gate_receipt.json"
    output = tmp_path / "cli_proof"
    _write_source_project(source)
    _write_csv_gate_receipt(receipt)

    code = cli_main(
        [
            "build-ymm4-diagnostic-placeholder-proof",
            "--package",
            str(PACKAGE),
            "--source-ymmp",
            str(source),
            "--csv-gate-receipt",
            str(receipt),
            "--output",
            str(output),
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "diagnostic_placeholder_proof_ready"
    assert payload["readback"]["status"] == "structural_pass"
    assert (output / PROJECT_FILENAME).exists()
