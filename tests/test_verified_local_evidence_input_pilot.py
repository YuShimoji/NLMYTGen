from __future__ import annotations

import codecs
import csv
import hashlib
import json
import struct
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.cli.main import main as cli_main
from src.pipeline.verified_local_evidence_input_pilot import (
    DERIVED_CSV_FILENAME,
    INPUT_READBACK_FILENAME,
    LOCAL_ACTUAL_READBACK_FILENAME,
    LOCAL_PROJECT_FILENAME,
    LOCAL_RENDER_FILENAME,
    OPERATOR_DIRNAME,
    OPERATOR_SCRIPT_FILENAME,
    PROJECT_MANIFEST_FILENAME,
    PROJECT_RECEIPT_FILENAME,
    STATIC_PROJECT_READBACK_FILENAME,
    build_verified_local_evidence_input_pilot,
    collect_verified_local_evidence_operator_result,
    generate_verified_local_evidence_project,
    validate_verified_local_evidence_input_pilot,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp, save_ymmp


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = REPO_ROOT / "production_pilots/yukkuri_newsroom_content_spine_002"


def _rows(path: Path) -> list[tuple[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [(row[0], row[1]) for row in csv.reader(handle) if row]


def _write_import_base(
    path: Path, rows: list[tuple[str, str]]
) -> list[dict]:
    frames = [index * 180 for index in range(9)]
    lengths = [150 + (index % 3) * 10 for index in range(9)]
    voices = [
        {
            "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
            "CharacterName": character,
            "Serif": text,
            "Frame": frames[index],
            "Length": lengths[index],
            "Layer": index % 2,
            "Group": 0,
            "IsLocked": False,
            "IsHidden": False,
            "VoiceCache": {"test_marker": f"voice-{index + 1}"},
        }
        for index, (character, text) in enumerate(rows)
    ]
    project = {
        "FilePath": str(path.resolve()),
        "SelectedTimelineIndex": 0,
        "Timelines": [
            {
                "ID": "verified-local-evidence-test",
                "Name": "メイン",
                "VideoInfo": {
                    "FPS": 60,
                    "Hz": 48000,
                    "Width": 1920,
                    "Height": 1080,
                },
                "VerticalLine": {"IsEnabled": False, "StartFrame": 0},
                "Items": voices,
                "LayerSettings": {"Items": []},
                "CurrentFrame": 0,
                "Length": frames[-1] + lengths[-1],
                "MaxLayer": 1,
            }
        ],
        "Characters": [],
        "LayoutXml": "<LayoutRoot><LayoutAnchorableFloatingWindow /></LayoutRoot>",
        "CollapsedGroups": ["detached-timeline-test-state"],
    }
    save_ymmp(project, path)
    return voices


def _file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


def _box(box_type: bytes, payload: bytes = b"") -> bytes:
    return struct.pack(">I4s", 8 + len(payload), box_type) + payload


def _minimal_structural_mp4(*, ftyp_after_first_32_bytes: bool = False) -> bytes:
    prefix = _box(b"free", b"x" * 40) if ftyp_after_first_32_bytes else b""
    ftyp = _box(b"ftyp", b"isom" + struct.pack(">I", 512) + b"isomiso2mp41")
    mvhd = _box(
        b"mvhd",
        b"\x00\x00\x00\x00"
        + struct.pack(">IIII", 0, 0, 1000, 1000)
        + b"\x00" * 80,
    )
    return prefix + ftyp + _box(b"moov", mvhd) + _box(b"mdat", b"\x00")


def test_builds_complete_deterministic_operator_ready_pilot(tmp_path: Path) -> None:
    first = tmp_path / "pilot-a"
    second = tmp_path / "pilot-b"

    result = build_verified_local_evidence_input_pilot(
        package_dir=PACKAGE,
        output_dir=first,
    )
    build_verified_local_evidence_input_pilot(
        package_dir=PACKAGE,
        output_dir=second,
    )

    assert result["status"] == "operator_batch_ready"
    assert result["cue_count"] == 9
    assert result["manual_action_count"] == 5
    assert _file_hashes(first) == _file_hashes(second)
    readback = json.loads((first / INPUT_READBACK_FILENAME).read_text(encoding="utf-8"))
    assert readback["status"] == "passed"
    assert readback["failed_checks"] == []
    assert all(readback["checks"].values())
    manifest = json.loads((first / PROJECT_MANIFEST_FILENAME).read_text(encoding="utf-8"))
    assert manifest["status"] == "ready_for_operator_generation"
    assert manifest["prior_local_base_assessment"]["reusable_for_current_script"] is False
    assert (first / OPERATOR_DIRNAME / OPERATOR_SCRIPT_FILENAME).exists()


def test_claim_script_and_csv_contract_is_exact(tmp_path: Path) -> None:
    pilot = tmp_path / "pilot"
    build_verified_local_evidence_input_pilot(package_dir=PACKAGE, output_dir=pilot)

    ledger = json.loads((pilot / "source_claim_ledger.json").read_text(encoding="utf-8"))
    script = json.loads((pilot / "canonical_script.json").read_text(encoding="utf-8"))
    canonical = _rows(pilot / "canonical_yymm4.csv")
    derived = _rows(pilot / DERIVED_CSV_FILENAME)

    assert ledger["claim_count"] == 9
    assert ledger["unsupported_claim_count"] == 0
    assert all(claim["unsupported_claim"] is False for claim in ledger["claims"])
    assert [cue["scene_id"] for cue in script["cues"]] == [
        "S1",
        "S1",
        "S2",
        "S2",
        "S3",
        "S3",
        "S3",
        "S3",
        "S3",
    ]
    assert [speaker for speaker, _ in canonical].count("れいむ") == 3
    assert [speaker for speaker, _ in derived].count("ゆっくり霊夢") == 3
    assert [text for _, text in canonical] == [text for _, text in derived]
    assert "DRY RUN" not in "\n".join(text for _, text in canonical).upper()


def test_generator_preserves_voiceitems_and_adds_three_scene_boundaries(
    tmp_path: Path,
) -> None:
    pilot = tmp_path / "pilot"
    build_verified_local_evidence_input_pilot(package_dir=PACKAGE, output_dir=pilot)
    source = tmp_path / "new-import-base.local.ymmp"
    expected_rows = _rows(pilot / DERIVED_CSV_FILENAME)
    original_voices = _write_import_base(source, expected_rows)

    result = generate_verified_local_evidence_project(
        pilot_dir=pilot,
        source_ymmp=source,
    )

    assert result["status"] == "local_internal_review_project_ready"
    project_path = pilot / "local_outputs" / LOCAL_PROJECT_FILENAME
    project = load_ymmp(project_path)
    assert "LayoutXml" not in project
    assert "CollapsedGroups" not in project
    items = _get_timeline_items(project)
    voices = [item for item in items if _item_type(item) == "VoiceItem"]
    images = [item for item in items if _item_type(item) == "ImageItem"]
    texts = [item for item in items if _item_type(item) == "TextItem"]
    assert voices == original_voices
    assert len(images) == 3
    assert len(texts) == 3
    assert all("INTERNAL REVIEW" in item["Text"] for item in texts)
    assert all("NOT FINAL" in item["Text"] for item in texts)
    assert all("LOCAL EVIDENCE PILOT" in item["Text"] for item in texts)
    actual = json.loads(
        (project_path.parent / LOCAL_ACTUAL_READBACK_FILENAME).read_text(encoding="utf-8")
    )
    assert actual["status"] == "structural_pass"
    assert all(actual["checks"].values())
    assert str(tmp_path) not in json.dumps(actual, ensure_ascii=False)

    second_project = tmp_path / "second" / LOCAL_PROJECT_FILENAME
    second = generate_verified_local_evidence_project(
        pilot_dir=pilot,
        source_ymmp=source,
        output_ymmp=second_project,
    )
    assert second["readback"]["normalized_project_sha256"] == actual[
        "normalized_project_sha256"
    ]


def test_generator_rejects_old_or_mismatched_voice_text(tmp_path: Path) -> None:
    pilot = tmp_path / "pilot"
    build_verified_local_evidence_input_pilot(package_dir=PACKAGE, output_dir=pilot)
    rows = _rows(pilot / DERIVED_CSV_FILENAME)
    rows[0] = (rows[0][0], "旧DRY RUN台本")
    source = tmp_path / "old-import-base.local.ymmp"
    _write_import_base(source, rows)

    with pytest.raises(
        ValueError, match="OPERATOR_IMPORT_BASE_TEXT_OR_CHARACTER_ORDER_MISMATCH"
    ):
        generate_verified_local_evidence_project(
            pilot_dir=pilot,
            source_ymmp=source,
        )


def test_collector_requires_fresh_outputs_and_explicit_clean_confirmation(
    tmp_path: Path,
) -> None:
    pilot = tmp_path / "pilot"
    build_verified_local_evidence_input_pilot(package_dir=PACKAGE, output_dir=pilot)
    source = tmp_path / "new-import-base.local.ymmp"
    _write_import_base(source, _rows(pilot / DERIVED_CSV_FILENAME))
    started = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
    generated = generate_verified_local_evidence_project(
        pilot_dir=pilot,
        source_ymmp=source,
    )
    render = pilot / "local_outputs" / LOCAL_RENDER_FILENAME
    render.write_bytes(_minimal_structural_mp4(ftyp_after_first_32_bytes=True))
    project_hash_before = hashlib.sha256(
        Path(generated["project_path"]).read_bytes()
    ).hexdigest()
    render_hash_before = hashlib.sha256(render.read_bytes()).hexdigest()

    success = collect_verified_local_evidence_operator_result(
        pilot_dir=pilot,
        project_path=generated["project_path"],
        render_path=render,
        not_before_utc=started,
        operator_confirmed_clean=True,
        yymm4_product_version="4.54.0.1",
        profile_observation_version="4.53.0.9",
        operator_output_setting_note="動画出力でMPEGへ変更",
    )
    assert success["status"] == "success"
    assert success["operator_reported"]["profile_version_match"] is False
    assert success["operator_reported"]["output_setting_note"] == (
        "動画出力でMPEGへ変更"
    )
    assert (
        success["independently_verified"]["render_iso_bmff_structure_pass"] is True
    )
    assert success["independently_verified"]["render_top_level_box_types"] == [
        "free",
        "ftyp",
        "moov",
        "mdat",
    ]
    assert (
        hashlib.sha256(Path(generated["project_path"]).read_bytes()).hexdigest()
        == project_hash_before
    )
    assert hashlib.sha256(render.read_bytes()).hexdigest() == render_hash_before

    result_path = pilot / "local_outputs" / "operator_result.json"
    assert "動画出力でMPEGへ変更" in result_path.read_text(encoding="utf-8")
    result_bytes = result_path.read_bytes()
    preserved = collect_verified_local_evidence_operator_result(
        pilot_dir=pilot,
        project_path=generated["project_path"],
        render_path=render,
        output_path=result_path,
        not_before_utc=started,
        operator_confirmed_clean=True,
        yymm4_product_version="4.54.0.1",
        profile_observation_version="4.53.0.9",
        preserve_existing_success=True,
    )
    assert preserved["status"] == "success"
    assert preserved["operator_result_preserved_byte_for_byte"] is True
    assert result_path.read_bytes() == result_bytes

    stale = collect_verified_local_evidence_operator_result(
        pilot_dir=pilot,
        project_path=generated["project_path"],
        render_path=render,
        output_path=pilot / "local_outputs" / "operator_result.stale.json",
        not_before_utc=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        operator_confirmed_clean=False,
        yymm4_product_version="4.54.0.1",
        profile_observation_version="4.53.0.9",
    )
    assert stale["status"] == "failure"
    assert "operator_clean_confirmation_missing" in stale["failed_checks"]
    assert "local_project_predates_batch" in stale["failed_checks"]
    assert "render_predates_batch" in stale["failed_checks"]


def test_collector_reports_yymm4_project_json_misnamed_as_mp4(tmp_path: Path) -> None:
    pilot = tmp_path / "pilot"
    build_verified_local_evidence_input_pilot(package_dir=PACKAGE, output_dir=pilot)
    source = tmp_path / "new-import-base.local.ymmp"
    _write_import_base(source, _rows(pilot / DERIVED_CSV_FILENAME))
    generated = generate_verified_local_evidence_project(
        pilot_dir=pilot,
        source_ymmp=source,
    )
    render = pilot / "local_outputs" / LOCAL_RENDER_FILENAME
    masquerading_project = {
        "FilePath": str(render),
        "SelectedTimelineIndex": 0,
        "Timelines": [{"Name": "メイン", "Items": []}],
    }
    render.write_bytes(
        codecs.BOM_UTF8
        + json.dumps(masquerading_project, ensure_ascii=False).encode("utf-8")
    )
    render_hash_before = hashlib.sha256(render.read_bytes()).hexdigest()

    result = collect_verified_local_evidence_operator_result(
        pilot_dir=pilot,
        project_path=generated["project_path"],
        render_path=render,
        not_before_utc=(datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(),
        operator_confirmed_clean=True,
        yymm4_product_version="4.54.0.1",
        profile_observation_version="4.53.0.9",
    )

    assert result["status"] == "failure"
    assert "render_is_yymm4_project_json_not_mp4" in result["failed_checks"]
    assert result["independently_verified"]["render_is_yymm4_project_json"] is True
    assert hashlib.sha256(render.read_bytes()).hexdigest() == render_hash_before


def test_cli_build_and_validate(tmp_path: Path, capsys) -> None:
    pilot = tmp_path / "pilot"
    code = cli_main(
        [
            "build-verified-local-evidence-pilot",
            "--package",
            str(PACKAGE),
            "--output",
            str(pilot),
            "--format",
            "json",
        ]
    )
    assert code == 0
    assert json.loads(capsys.readouterr().out)["status"] == "operator_batch_ready"

    code = cli_main(
        [
            "validate-verified-local-evidence-pilot",
            "--pilot",
            str(pilot),
            "--package",
            str(PACKAGE),
            "--format",
            "json",
            "--result-json",
            str(tmp_path / "日本語-validation-result.json"),
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    explicit_result = tmp_path / "日本語-validation-result.json"
    assert json.loads(explicit_result.read_text(encoding="utf-8"))["status"] == (
        "passed"
    )
    assert explicit_result.read_bytes().startswith(b"{")

    source = tmp_path / "日本語-import-base.local.ymmp"
    _write_import_base(source, _rows(pilot / DERIVED_CSV_FILENAME))
    generation_result = tmp_path / "日本語-generation-result.json"
    code = cli_main(
        [
            "generate-verified-local-evidence-project",
            "--pilot",
            str(pilot),
            "--source-ymmp",
            str(source),
            "--result-json",
            str(generation_result),
            "--format",
            "json",
        ]
    )
    assert code == 0
    assert json.loads(capsys.readouterr().out)["status"] == (
        "local_internal_review_project_ready"
    )
    assert json.loads(generation_result.read_text(encoding="utf-8"))["status"] == (
        "local_internal_review_project_ready"
    )


def test_operator_scripts_use_utf8_files_and_collect_only_precedes_yymm4(
    tmp_path: Path,
) -> None:
    pilot = tmp_path / "pilot"
    build_verified_local_evidence_input_pilot(package_dir=PACKAGE, output_dir=pilot)
    operator_script = (
        pilot / OPERATOR_DIRNAME / OPERATOR_SCRIPT_FILENAME
    ).read_text(encoding="utf-8")
    collector_script = (
        pilot / OPERATOR_DIRNAME / "collect_operator_result.ps1"
    ).read_text(encoding="utf-8")
    readme = (pilot / OPERATOR_DIRNAME / "README_OPERATOR_BATCH.md").read_text(
        encoding="utf-8"
    )

    assert "$env:PYTHONUTF8 = \"1\"" in operator_script
    assert "$env:PYTHONIOENCODING = \"utf-8\"" in operator_script
    assert "--result-json $ValidationResultFile" in operator_script
    assert "--result-json $GenerationResultFile" in operator_script
    assert "Get-Content -LiteralPath $Path -Raw -Encoding UTF8" in operator_script
    assert "Out-String" not in operator_script
    assert "Out-String" not in collector_script
    assert (
        "Get-Content -LiteralPath $OutputPath -Raw -Encoding UTF8"
        in collector_script
    )
    assert "[switch]$CollectOnly" in operator_script
    collect_branch = operator_script.index("if ($CollectOnly)")
    resolve_call = operator_script.index("$Ymm4 = Resolve-Ymm4Exe")
    launch_call = operator_script.index("Start-Process -FilePath $Ymm4")
    generate_call = operator_script.index("generate-verified-local-evidence-project")
    assert collect_branch < resolve_call < launch_call < generate_call
    assert "Project Save As -> `.local.ymmp`" in readme
    assert "Video Output/Export -> `.mp4`" in readme
    assert "Project Save Asを使ってはいけません" in readme


def test_static_readback_does_not_overclaim_actual_project(tmp_path: Path) -> None:
    pilot = tmp_path / "pilot"
    build_verified_local_evidence_input_pilot(package_dir=PACKAGE, output_dir=pilot)
    readback = json.loads(
        (pilot / STATIC_PROJECT_READBACK_FILENAME).read_text(encoding="utf-8")
    )
    assert readback["status"] == "contract_pass"
    assert readback["contract_stage"] == "pre_operator_contract_snapshot"
    assert readback["current_authority_when_render_exists"] == "render_receipt.json"
    assert readback["actual_project_present"] is False
    assert readback["actual_project_parse_performed"] is False
    assert readback["actual_render_validated"] is False
    receipt = json.loads(
        (pilot / PROJECT_RECEIPT_FILENAME).read_text(encoding="utf-8")
    )
    assert receipt["superseded_by_render_receipt_when_present"] == (
        "render_receipt.json"
    )
    assert validate_verified_local_evidence_input_pilot(pilot_dir=pilot)["status"] == "passed"
