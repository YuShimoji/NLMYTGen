from __future__ import annotations

import csv
import hashlib
import json
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
    render.write_bytes(b"\x00\x00\x00\x18ftypisom" + b"\x00" * 64)

    success = collect_verified_local_evidence_operator_result(
        pilot_dir=pilot,
        project_path=generated["project_path"],
        render_path=render,
        not_before_utc=started,
        operator_confirmed_clean=True,
        yymm4_product_version="4.54.0.1",
        profile_observation_version="4.53.0.9",
    )
    assert success["status"] == "success"
    assert success["operator_reported"]["profile_version_match"] is False

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
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"


def test_static_readback_does_not_overclaim_actual_project(tmp_path: Path) -> None:
    pilot = tmp_path / "pilot"
    build_verified_local_evidence_input_pilot(package_dir=PACKAGE, output_dir=pilot)
    readback = json.loads(
        (pilot / STATIC_PROJECT_READBACK_FILENAME).read_text(encoding="utf-8")
    )
    assert readback["status"] == "contract_pass"
    assert readback["actual_project_present"] is False
    assert readback["actual_project_parse_performed"] is False
    assert readback["actual_render_validated"] is False
    assert validate_verified_local_evidence_input_pilot(pilot_dir=pilot)["status"] == "passed"
