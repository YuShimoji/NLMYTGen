from __future__ import annotations

import csv
import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
)
from src.pipeline.ymm4_import_ready_pack import (
    ALIAS_COVERAGE_FILENAME,
    DEFAULT_ARTIFACT_ID,
    DERIVED_IMPORT_CSV_FILENAME,
    ORIGINAL_CANONICAL_CSV_SHA256,
    REQUIRED_CUE_FIELDS,
    REQUIRED_YMM4_IMPORT_READY_FILES,
    build_ymm4_import_ready_pack,
    validate_ymm4_import_ready_pack,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"
PROFILE_PATH = (
    SOURCE_PACKAGE
    / "ymm4_character_alias_profiles"
    / "ymm4_4_53_0_9_yukkuri_characters_v1.json"
)
CANONICAL_CSV = (
    SOURCE_PACKAGE
    / "transcript_substitution_readiness"
    / "regenerated_draft_yymm4.csv"
)
EXPECTED_CANONICAL_SPEAKERS = [
    "れいむ",
    "まりさ",
    "まりさ",
    "まりさ",
    "れいむ",
    "まりさ",
    "まりさ",
    "れいむ",
    "まりさ",
]
EXPECTED_YMM4_CHARACTERS = [
    "ゆっくり霊夢" if speaker == "れいむ" else "ゆっくり魔理沙"
    for speaker in EXPECTED_CANONICAL_SPEAKERS
]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _csv_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _build(output_dir: Path) -> dict:
    return build_ymm4_import_ready_pack(
        package_dir=SOURCE_PACKAGE,
        yymm4_character_profile=PROFILE_PATH,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )


def test_ymm4_import_ready_pack_builds_manifest_cue_map_and_preview(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_ready_pack"

    readback = _build(output_dir)

    assert readback["status"] == "passed"
    for filename in REQUIRED_YMM4_IMPORT_READY_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "ymm4_import_ready_manifest.json")
    cue_map = _load(output_dir / "edit_slice_to_ymm4_cue_map.json")
    gate_readback = _load(output_dir / "gate_readback.json")
    adapter_plan = _load(output_dir / "ymmp_adapter_plan.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    alias_coverage = _load(output_dir / ALIAS_COVERAGE_FILENAME)
    canonical_rows = _csv_rows(CANONICAL_CSV)
    derived_rows = _csv_rows(output_dir / DERIVED_IMPORT_CSV_FILENAME)
    html = (output_dir / "ymm4_import_ready_preview.html").read_text(encoding="utf-8")
    sheet = (output_dir / "manual_ymm4_import_observation_sheet.md").read_text(encoding="utf-8")

    assert manifest["schema_version"] == "ymm4_import_ready_manifest.v2"
    assert manifest["artifact_id"] == DEFAULT_ARTIFACT_ID
    assert manifest["source_episode_id"] == "yukkuri_newsroom_content_spine_002"
    assert manifest["queue_count"] == 7
    assert manifest["scene_count"] == 3
    assert manifest["cue_count"] == 9
    assert manifest["expected_voice_subtitle_links"]["count"] == 9
    assert len(manifest["visual_scene_links"]) == 3
    assert len(manifest["citation_overlay_links"]) == 3
    assert manifest["thumbnail_motif_status"] == "placeholder_context_transferred_not_final_approval"
    assert manifest["ymm4_import_state"] == "ready_for_bounded_alias_reobservation"
    assert manifest["canonical_source_csv"].endswith(
        "transcript_substitution_readiness/regenerated_draft_yymm4.csv"
    )
    assert manifest["primary_import_csv"].endswith(DERIVED_IMPORT_CSV_FILENAME)
    assert manifest["selected_yymm4_character_profile"].endswith(PROFILE_PATH.name)
    assert manifest["alias_coverage_readback"].endswith(ALIAS_COVERAGE_FILENAME)
    derivation = manifest["character_alias_derivation"]
    assert derivation["profile_id"] == "ymm4_4_53_0_9_yukkuri_characters_ja_v1"
    assert derivation["strict_coverage"] is True
    assert derivation["canonical_csv_sha256"] == ORIGINAL_CANONICAL_CSV_SHA256
    assert derivation["row_count"] == 9
    assert derivation["derived_csv_sha256"] == alias_coverage["derived_csv"]["sha256"]
    assert manifest["actual_ymm4_imported"] is False
    assert manifest["rendered_video_created"] is False
    assert manifest["real_input_replaced"] is False
    assert manifest["rights_approved"] is False
    assert manifest["public_ready"] is False
    assert manifest["gates_closed"] is True

    assert alias_coverage["status"] == "passed"
    assert alias_coverage["profile"]["profile_id"] == derivation["profile_id"]
    assert alias_coverage["profile"]["repo_relative_path"].endswith(PROFILE_PATH.name)
    assert alias_coverage["canonical_csv"]["sha256"] == ORIGINAL_CANONICAL_CSV_SHA256
    assert alias_coverage["canonical_csv"]["row_count"] == 9
    assert alias_coverage["derived_csv"]["row_count"] == 9
    assert alias_coverage["checks"]["canonical_source_unchanged"] is True
    assert alias_coverage["checks"]["strict_coverage_satisfied"] is True
    assert alias_coverage["checks"]["text_and_order_preserved"] is True
    assert alias_coverage["checks"]["speaker_projection_matches_profile"] is True

    assert len(canonical_rows) == len(derived_rows) == 9
    assert [row[0] for row in canonical_rows] == EXPECTED_CANONICAL_SPEAKERS
    assert [row[0] for row in derived_rows] == EXPECTED_YMM4_CHARACTERS
    assert [row[1] for row in derived_rows] == [row[1] for row in canonical_rows]

    assert cue_map["schema_version"] == "edit_slice_to_ymm4_cue_map.v2"
    assert cue_map["cue_count"] == 9
    assert cue_map["scene_count"] == 3
    assert cue_map["canonical_csv"] == manifest["canonical_source_csv"]
    assert cue_map["derived_import_csv"] == manifest["primary_import_csv"]
    assert cue_map["selected_yymm4_character_profile"] == manifest["selected_yymm4_character_profile"]
    responsibility = cue_map["responsibility_contract"]
    assert responsibility == {
        "schema_version": "ymm4_import_responsibility_contract.v1",
        "csv_import_expected_item_families": ["VoiceItem", "linked_subtitle"],
        "diagnostic_project_expected_item_families": [
            "ImageItem",
            "independent_TextItem_placeholders",
        ],
        "diagnostic_project_gate": "not_authorized",
        "diagnostic_project_status": "not_attempted",
    }
    assert len(cue_map["cues"]) == 9
    assert [cue["row_number"] for cue in cue_map["cues"]] == list(range(1, 10))
    assert [cue["canonical_speaker"] for cue in cue_map["cues"]] == EXPECTED_CANONICAL_SPEAKERS
    assert [cue["yymm4_character"] for cue in cue_map["cues"]] == EXPECTED_YMM4_CHARACTERS
    for cue in cue_map["cues"]:
        for field in REQUIRED_CUE_FIELDS:
            assert field in cue
        assert "expected_yymm4_layer_or_track" not in cue
        assert cue["speaker"] == cue["canonical_speaker"]
        assert cue["csv_import_expected_item_families"] == ["VoiceItem", "linked_subtitle"]
        assert cue["diagnostic_project_expected_item_families"] == [
            "ImageItem",
            "independent_TextItem_placeholders",
        ]
        assert cue["diagnostic_project_gate"] == "not_authorized"
        assert cue["voice_or_subtitle_action"]["canonical_subtitle_source"].endswith(
            f"regenerated_draft_yymm4.csv#row-{cue['row_number']}"
        )
        assert cue["voice_or_subtitle_action"]["csv_import_source"].endswith(
            f"{DERIVED_IMPORT_CSV_FILENAME}#row-{cue['row_number']}"
        )
        assert cue["required_asset_state"] in {"placeholder", "diagnostic", "real_required_later"}

    assert gate_readback["schema_version"] == "ymm4_import_ready_gate_readback.v2"
    assert gate_readback["status"] == "ymm4_import_gates_closed"
    assert gate_readback["gates_closed"] is True
    assert all(value is False for value in gate_readback["closed_gate_flags"].values())
    assert gate_readback["closed_gate_flags"]["diagnostic_ymmp_project_attempted"] is False

    assert adapter_plan["schema_version"] == "ymmp_adapter_plan.v2"
    assert adapter_plan["status"] == "adapter_plan_ready_no_ymmp_write"
    assert "expected_item_families" not in adapter_plan
    assert adapter_plan["csv_import_contract"] == {
        "expected_item_families": ["VoiceItem", "linked_subtitle"],
        "source_csv": manifest["primary_import_csv"],
        "selected_yymm4_character_profile": manifest["selected_yymm4_character_profile"],
    }
    assert adapter_plan["diagnostic_project_contract"] == {
        "expected_item_families": ["ImageItem", "independent_TextItem_placeholders"],
        "gate": "not_authorized",
        "status": "not_attempted",
        "separate_authorization_required": True,
    }
    assert adapter_plan["ymmp_file_created"] is False
    assert source_index["local_edit_pack_read_only"] is True
    source_records = {record["record_id"]: record for record in source_index["records"]}
    assert source_records["canonical_csv"]["role"] == "canonical_speaker_identity_read_only"
    assert source_records["yymm4_character_profile"]["repo_relative_path"].endswith(PROFILE_PATH.name)
    assert source_records["original_observation_receipt"]["role"] == "immutable_prior_observation_evidence"
    assert '<html lang="ja"' in html
    assert 'data-ymm4-import-ready="true"' in html
    assert 'data-region="cue-map"' in html
    assert "YMM4インポート準備レビュー" in html
    assert "cueマップ" in html
    assert "gate確認" in html
    assert "未実行" in html
    assert "import risk" in html
    assert "れいむ → ゆっくり霊夢" in html
    assert "まりさ → ゆっくり魔理沙" in html
    assert "card-grid" not in html
    assert "Episode 002限定" in sheet
    assert "目的: YMM4観測前の確認チェック" in sheet
    assert "範囲: derived CSV" in sheet
    assert "対象外:" in sheet
    assert "YMM4 observation readback" in sheet
    assert "mapping dialog" in sheet
    assert "not_authorized/not_attempted" in sheet
    assert "窶" not in html
    assert "窶" not in sheet
    assert sheet.count("\n1.") == 1
    assert sheet.count("\n5.") == 1


def test_ymm4_import_ready_validation_catches_missing_cue_map(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_ready_pack"
    _build(output_dir)
    (output_dir / "edit_slice_to_ymm4_cue_map.json").unlink()

    readback = validate_ymm4_import_ready_pack(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:edit_slice_to_ymm4_cue_map.json" in readback["failed_checks"]


def test_cli_build_ymm4_import_ready_pack_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_ymm4_import_ready_pack"

    code = main(
        [
            "build-ymm4-import-ready-pack",
            "--package",
            str(SOURCE_PACKAGE),
            "--ymm4-character-profile",
            str(PROFILE_PATH),
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
    assert payload["status"] == "passed"
    assert payload["primary_review_file"].endswith("ymm4_import_ready_preview.html")
    assert payload["queue_count"] == 7
    assert payload["scene_count"] == 3
    assert payload["cue_count"] == 9
    assert payload["ymm4_import_state"] == "ready_for_bounded_alias_reobservation"
    assert payload["primary_import_csv"].endswith(DERIVED_IMPORT_CSV_FILENAME)
    assert payload["selected_yymm4_character_profile"].endswith(PROFILE_PATH.name)
    assert payload["actual_ymm4_imported"] is False
    assert payload["rendered_video_created"] is False
    assert payload["real_input_replaced"] is False
    assert payload["rights_approved"] is False
    assert payload["public_ready"] is False
    assert payload["gates_closed"] is True
    assert payload["full_pytest_run"] is False


def test_ymm4_import_ready_pack_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_ready_pack"
    _build(output_dir)

    readback = _load(output_dir / "validation_readback.json")
    assert readback["status"] == "passed"
    assert readback["checks"]["external_dependency_status"] == "none_found"
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["temporary_copy_absent"] is True
    assert readback["checks"]["ymmp_file_created"] is False

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


def test_ymm4_import_ready_validation_rejects_derived_text_and_hash_corruption(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_ready_pack"
    _build(output_dir)
    derived_path = output_dir / DERIVED_IMPORT_CSV_FILENAME
    rows = _csv_rows(derived_path)
    rows[0][1] = "corrupted subtitle text"
    with derived_path.open("w", encoding="utf-8", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerows(rows)

    readback = validate_ymm4_import_ready_pack(output_dir)

    assert readback["status"] == "failed"
    assert "derived_csv_sha256_mismatch" in readback["failed_checks"]
    assert "derived_csv_actual_text_order_mismatch" in readback["failed_checks"]
    assert "derived_csv_actual_crosswalk_mismatch" in readback["failed_checks"]


def test_ymm4_import_ready_derived_artifacts_regenerate_byte_deterministically(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_ready_pack"
    _build(output_dir)
    derived_before = (output_dir / DERIVED_IMPORT_CSV_FILENAME).read_bytes()
    coverage_before = (output_dir / ALIAS_COVERAGE_FILENAME).read_bytes()

    _build(output_dir)

    assert (output_dir / DERIVED_IMPORT_CSV_FILENAME).read_bytes() == derived_before
    assert (output_dir / ALIAS_COVERAGE_FILENAME).read_bytes() == coverage_before
