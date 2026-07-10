from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.cli.main import main
from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
)
from src.pipeline.ymm4_observation_readback_pack import (
    DEFAULT_ARTIFACT_ID,
    OBSERVATION_RECEIPT_SCHEMA_VERSION,
    REQUIRED_YMM4_OBSERVATION_FILES,
    _detect_yymm4,
    build_ymm4_observation_readback_pack,
    validate_ymm4_observation_readback_pack,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _actual_observation_receipt() -> dict:
    return {
        "schema_version": OBSERVATION_RECEIPT_SCHEMA_VERSION,
        "episode_id": "yukkuri_newsroom_content_spine_002",
        "observed_at": "2026-07-10_JST",
        "status": "partial",
        "result": "pass_with_warnings",
        "actual_ymm4_import_attempted": True,
        "actual_ymm4_imported": True,
        "source_csv": "production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv",
        "source_csv_sha256": "6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C",
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
    assert observation["placeholder_boundary_observed"] == "not_observed"
    assert observation["screenshot_or_visual_evidence_paths"] == []
    assert observation["rendered_video_created"] is False
    assert observation["ymmp_file_created"] is False
    assert observation["production_ymmp_written"] is False
    assert observation["real_input_replaced"] is False
    assert observation["rights_approved"] is False
    assert observation["public_ready"] is False
    assert observation["next_gate"] == "manual_ymm4_import_observation_return"
    assert all(value is False for value in observation["closed_gate_flags"].values())
    assert source_index["ymm4_import_ready_pack_read_only"] is True
    assert source_index["real_input_prep_pack_read_only"] is True
    assert '<html lang="ja"' in html
    assert 'data-ymm4-observation-readback="true"' in html
    assert 'data-region="pipeline-runway"' in html
    assert 'data-region="observation-matrix"' in html
    assert 'data-region="closed-gates"' in html
    assert "実観測は未実行" in html
    assert "card-grid" not in html
    assert "operatorが返す観測5点" in manual
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
        json.dumps(_actual_observation_receipt(), ensure_ascii=False, indent=2),
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
    assert readback["observation_mode"] == "actual_ymm4_gui_observation"
    assert readback["actual_ymm4_import_attempted"] is True
    assert readback["actual_ymm4_imported"] is True
    assert readback["cue_count_observed"] == 9
    assert readback["scene_order_observed"] == ["S1", "S2", "S3"]
    assert readback["cue_order_observed"] == [f"csv_row_{index}" for index in range(1, 10)]
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
    assert "bounded CSV import" in limitations


def test_ymm4_observation_readback_rejects_missing_explicit_receipt(tmp_path) -> None:
    with pytest.raises(FileNotFoundError, match="observation receipt not found"):
        build_ymm4_observation_readback_pack(
            package_dir=SOURCE_PACKAGE,
            output_dir=tmp_path / "output",
            artifact_id=DEFAULT_ARTIFACT_ID,
            observation_receipt=tmp_path / "missing.json",
        )


def test_ymm4_observation_readback_rejects_mismatched_source_hash(tmp_path) -> None:
    receipt = _actual_observation_receipt()
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
    receipt = _actual_observation_receipt()
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
    receipt = _actual_observation_receipt()
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
    assert payload["placeholder_boundary_observed"] == "not_observed"
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
        json.dumps(_actual_observation_receipt(), ensure_ascii=False, indent=2),
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
    assert payload["status"] == "partial"
    assert payload["observation_mode"] == "actual_ymm4_gui_observation"
    assert payload["cue_count_observed"] == 9


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
