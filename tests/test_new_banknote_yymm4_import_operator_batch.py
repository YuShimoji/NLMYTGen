from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.pipeline.new_banknote_yymm4_import_operator_batch import (
    ACCEPTED_SCRIPT_COMMIT,
    APPROVED_FILES,
    COLLECT_SCRIPT_FILENAME,
    DEFAULT_PILOT_DIR,
    EXPECTED_CONTRACT_FILENAME,
    EXPECTED_APPROVED_HASHES,
    LOCAL_BATCH_STATE_FILENAME,
    LOCAL_OUTPUT_DIRNAME,
    LOCAL_PROJECT_FILENAME,
    LOCAL_RESULT_FILENAME,
    MANIFEST_FILENAME,
    OPERATOR_DIRNAME,
    PREFLIGHT_FILENAME,
    PROFILE_VERSION,
    README_FILENAME,
    RETURN_TEMPLATE_FILENAME,
    RUN_SCRIPT_FILENAME,
    SUPERVISOR_DECISION,
    SUPERVISOR_RECEIPT_FILENAME,
    collect_new_banknote_yymm4_import_result,
    main as operator_main,
    preflight_new_banknote_yymm4_operator_batch,
    render_new_banknote_yymm4_operator_artifacts,
)
from src.pipeline.ymm4_character_alias_profile import read_headerless_yymm4_csv
from src.pipeline.ymmp_patch import save_ymmp


REPO_ROOT = Path(__file__).resolve().parents[1]
_PRIVATE_PATH_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/]|\\\\[^\\\s]+[\\/]|/home/|/users/)"
)


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


@pytest.fixture
def isolated_pilot(tmp_path: Path) -> Path:
    target = tmp_path / "new_banknote_pilot"
    shutil.copytree(
        DEFAULT_PILOT_DIR,
        target,
        ignore=shutil.ignore_patterns(LOCAL_OUTPUT_DIRNAME),
    )
    return target


def _derived_rows(pilot: Path) -> list[tuple[str, str]]:
    payload = read_headerless_yymm4_csv(
        pilot / "derived_yymm4_import.csv"
    )
    return [
        (str(row["speaker"]), str(row["text"]))
        for row in payload["rows"]
    ]


def _write_import_project(
    pilot: Path,
    rows: list[tuple[str, str]],
) -> Path:
    project_path = (
        pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_PROJECT_FILENAME
    ).resolve()
    project_path.parent.mkdir(parents=True, exist_ok=True)
    frames = [index * 180 for index in range(len(rows))]
    lengths = [150 + (index % 3) * 10 for index in range(len(rows))]
    voices = [
        {
            "$type": (
                "YukkuriMovieMaker.Project.Items.VoiceItem, "
                "YukkuriMovieMaker"
            ),
            "CharacterName": character,
            "Serif": text,
            "Frame": frames[index],
            "Length": lengths[index],
            "Layer": index % 2,
            "Group": 0,
            "VoiceCache": {"must_not_leak": f"voice-{index + 1}"},
        }
        for index, (character, text) in enumerate(rows)
    ]
    project = {
        "FilePath": str(project_path),
        "SelectedTimelineIndex": 0,
        "Timelines": [
            {
                "Name": "メイン",
                "VideoInfo": {
                    "FPS": 60,
                    "Hz": 48000,
                    "Width": 1920,
                    "Height": 1080,
                },
                "Items": voices,
                "Length": frames[-1] + lengths[-1],
            }
        ],
    }
    save_ymmp(project, project_path)
    return project_path


def test_tracked_operator_batch_is_byte_deterministic_and_preflight_passes() -> None:
    first = render_new_banknote_yymm4_operator_artifacts(DEFAULT_PILOT_DIR)
    second = render_new_banknote_yymm4_operator_artifacts(DEFAULT_PILOT_DIR)
    assert first == second
    for relative, expected_bytes in first.items():
        assert (DEFAULT_PILOT_DIR / relative).read_bytes() == expected_bytes

    preflight = preflight_new_banknote_yymm4_operator_batch(
        DEFAULT_PILOT_DIR
    )
    assert preflight["status"] == "passed"
    assert preflight["failed_checks"] == []
    assert all(preflight["checks"].values())

    receipt = _load(DEFAULT_PILOT_DIR / SUPERVISOR_RECEIPT_FILENAME)
    assert receipt["decision"] == SUPERVISOR_DECISION
    assert receipt["accepted_script_commit"] == ACCEPTED_SCRIPT_COMMIT
    assert len(receipt["review_results"]) == 5
    assert {
        item["result"] for item in receipt["review_results"]
    } == {"pass_for_bounded_yymm4_import_observation"}
    boundary = receipt["authorization_boundary"]
    assert boundary["operator_batch_preparation"] is True
    for key in (
        "user_creative_preference_acceptance",
        "production_approval",
        "render_approval",
        "rights_approval",
        "publication_approval",
    ):
        assert boundary[key] is False

    approved_hashes = receipt["approved_artifact_hashes"]
    assert tuple(approved_hashes) == APPROVED_FILES
    assert approved_hashes == EXPECTED_APPROVED_HASHES
    for name, digest in approved_hashes.items():
        assert hashlib.sha256(
            (DEFAULT_PILOT_DIR / name).read_bytes()
        ).hexdigest() == digest

    contract = _load(
        DEFAULT_PILOT_DIR / OPERATOR_DIRNAME / EXPECTED_CONTRACT_FILENAME
    )
    assert len(contract["rows"]) == 9
    assert [row["csv_row_id"] for row in contract["rows"]] == [
        f"csv_row_{index}" for index in range(1, 10)
    ]
    assert dict(
        Counter(row["character"] for row in contract["rows"])
    ) == {"ゆっくり霊夢": 3, "ゆっくり魔理沙": 6}
    assert contract["expectations"]["ImageItem_required"] is False
    assert contract["expectations"]["independent_TextItem_required"] is False
    assert contract["expectations"]["render_required"] is False


def test_operator_surfaces_are_utf8_safe_launch_bounded_and_private() -> None:
    operator = DEFAULT_PILOT_DIR / OPERATOR_DIRNAME
    run_bytes = (operator / RUN_SCRIPT_FILENAME).read_bytes()
    collect_bytes = (operator / COLLECT_SCRIPT_FILENAME).read_bytes()
    assert all(byte < 128 for byte in run_bytes + collect_bytes)
    run_text = run_bytes.decode("ascii")
    collect_text = collect_bytes.decode("ascii")

    launch = run_text.index("Start-Process -FilePath $Ymm4")
    assert run_text.count("Start-Process -FilePath $Ymm4") == 1
    assert run_text.index("if ($CollectOnly)") < launch
    assert run_text.index("if ($PreflightOnly)") < launch
    assert run_text.index("$ExistingTargets.Count -gt 0") < launch
    assert run_text.rindex("if (Test-Ymm4Running)", 0, launch) < launch
    assert "Start-Process" not in collect_text
    assert "-Ymm4Exe" in run_text
    assert "NLMYTGEN_YMM4_EXE" in run_text
    assert "Out-String" not in run_text + collect_text
    assert "[IO.File]::ReadAllText" in run_text + collect_text
    assert "[Text.Encoding]::UTF8" in run_text + collect_text
    assert "| Out-Null" in run_text + collect_text
    assert "[scriptblock]::Create" in run_text

    manifest = _load(operator / MANIFEST_FILENAME)
    assert manifest["manual_action_count"] == 4
    assert manifest["return_item_count"] == 3
    assert manifest["modes"]["preflight_only"]["launches_yymm4"] is False
    assert manifest["modes"]["collect_only"]["launches_yymm4"] is False
    assert "日本語" not in run_text + collect_text
    assert any(
        ord(character) > 127
        for value in manifest["operator_messages"].values()
        for character in value
    )

    tracked_paths = [
        DEFAULT_PILOT_DIR / SUPERVISOR_RECEIPT_FILENAME,
        operator / README_FILENAME,
        operator / MANIFEST_FILENAME,
        operator / EXPECTED_CONTRACT_FILENAME,
        operator / PREFLIGHT_FILENAME,
        operator / RETURN_TEMPLATE_FILENAME,
        operator / RUN_SCRIPT_FILENAME,
        operator / COLLECT_SCRIPT_FILENAME,
    ]
    combined = "\n".join(
        path.read_text(encoding="utf-8") for path in tracked_paths
    )
    assert not _PRIVATE_PATH_RE.search(combined)
    assert "notebooklm.google.com" not in combined.lower()


def test_collect_only_powershell_fixture_validates_9_3_6_and_timing(
    isolated_pilot: Path,
) -> None:
    rows = _derived_rows(isolated_pilot)
    project = _write_import_project(isolated_pilot, rows)
    local = isolated_pilot / LOCAL_OUTPUT_DIRNAME
    result_path = local / LOCAL_RESULT_FILENAME
    batch_state = local / LOCAL_BATCH_STATE_FILENAME
    started = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
    batch_state.write_text(
        json.dumps(
            {
                "schema_version": (
                    "new_banknote_yymm4_import_operator_batch.local.v1"
                ),
                "batch_not_before_utc": started,
                "yymm4_product_version": "4.54.0.1+fixture",
                "profile_observation_version": PROFILE_VERSION,
                "target_project": str(project),
                "target_result": str(result_path),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    collector = (
        DEFAULT_PILOT_DIR / OPERATOR_DIRNAME / COLLECT_SCRIPT_FILENAME
    )
    completed = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(collector),
            "-PythonExe",
            sys.executable,
            "-PilotDir",
            str(isolated_pilot),
            "-ProjectPath",
            str(project),
            "-OutputPath",
            str(result_path),
            "-BatchStatePath",
            str(batch_state),
            "-OperatorConfirmedNoMappingError",
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.splitlines() == [
        "1. result: success",
        f"2. operator_result.json: {result_path}",
    ]
    result = _load(result_path)
    assert result["status"] == "success"
    assert result["failed_checks"] == []
    verified = result["independently_verified"]
    assert verified["VoiceItem_count"] == 9
    assert verified["character_counts"] == {
        "ゆっくり霊夢": 3,
        "ゆっくり魔理沙": 6,
    }
    assert verified["exact_text_order"] is True
    assert verified["exact_character_text_order"] is True
    assert verified["missing_count"] == 0
    assert verified["duplicate_count"] == 0
    assert verified["reordered"] is False
    assert verified["fps"] == 60
    assert verified["timeline_frames"] > 0
    assert verified["duration_seconds"] > 0
    assert verified["voice_timing_summary"][0]["frame"] == 0
    assert "VoiceCache" not in result_path.read_text(encoding="utf-8")


def test_collector_fails_on_character_text_and_order_drift(
    isolated_pilot: Path,
) -> None:
    rows = _derived_rows(isolated_pilot)
    rows[1] = rows[0]
    rows[2], rows[3] = rows[3], rows[2]
    project = _write_import_project(isolated_pilot, rows)
    output = (
        isolated_pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_RESULT_FILENAME
    )
    result = collect_new_banknote_yymm4_import_result(
        pilot_dir=isolated_pilot,
        project_path=project,
        output_path=output,
        not_before_utc=(
            datetime.now(timezone.utc) - timedelta(seconds=1)
        ).isoformat(),
        operator_confirmed_no_mapping_error=True,
        yymm4_product_version="4.54.0.1+fixture",
    )
    assert result["status"] == "failure"
    verified = result["independently_verified"]
    assert verified["VoiceItem_count"] == 9
    assert verified["missing_count"] == 1
    assert verified["duplicate_count"] == 1
    assert verified["exact_text_order"] is False
    assert verified["exact_character_text_order"] is False
    assert "character_counts_3_6" in result["failed_checks"]


def test_collector_requires_fresh_exact_target_and_mapping_confirmation(
    isolated_pilot: Path,
) -> None:
    project = _write_import_project(isolated_pilot, _derived_rows(isolated_pilot))
    stale_time = datetime.now(timezone.utc) - timedelta(days=1)
    os.utime(project, (stale_time.timestamp(), stale_time.timestamp()))
    output = (
        isolated_pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_RESULT_FILENAME
    )
    result = collect_new_banknote_yymm4_import_result(
        pilot_dir=isolated_pilot,
        project_path=project,
        output_path=output,
        not_before_utc=datetime.now(timezone.utc).isoformat(),
        operator_confirmed_no_mapping_error=False,
        yymm4_product_version="4.53.0.9",
    )
    assert result["status"] == "failure"
    assert "local_project_fresh" in result["failed_checks"]
    assert (
        "operator_confirmed_no_mapping_error_update_or_character_mismatch"
        in result["failed_checks"]
    )
    assert (
        result["operator_observation"]["mapping_dialog_or_error_observed"]
        is None
    )


def test_wrong_character_fails_without_inventing_missing_or_duplicate_cues(
    isolated_pilot: Path,
) -> None:
    rows = _derived_rows(isolated_pilot)
    rows[0] = ("ゆっくり魔理沙", rows[0][1])
    project = _write_import_project(isolated_pilot, rows)
    output = (
        isolated_pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_RESULT_FILENAME
    )
    result = collect_new_banknote_yymm4_import_result(
        pilot_dir=isolated_pilot,
        project_path=project,
        output_path=output,
        not_before_utc=(
            datetime.now(timezone.utc) - timedelta(seconds=1)
        ).isoformat(),
        operator_confirmed_no_mapping_error=True,
        yymm4_product_version="4.54.0.1+fixture",
    )
    verified = result["independently_verified"]
    assert result["status"] == "failure"
    assert verified["exact_text_order"] is True
    assert verified["exact_character_text_order"] is False
    assert verified["missing_count"] == 0
    assert verified["duplicate_count"] == 0
    assert "character_counts_3_6" in result["failed_checks"]


def test_existing_operator_result_is_preserved_byte_for_byte(
    isolated_pilot: Path,
) -> None:
    project = _write_import_project(isolated_pilot, _derived_rows(isolated_pilot))
    output = (
        isolated_pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_RESULT_FILENAME
    )
    original = b'{"status":"existing-evidence"}\n'
    output.write_bytes(original)
    with pytest.raises(ValueError, match="EXISTING_OPERATOR_RESULT_PRESERVED"):
        collect_new_banknote_yymm4_import_result(
            pilot_dir=isolated_pilot,
            project_path=project,
            output_path=output,
            not_before_utc=(
                datetime.now(timezone.utc) - timedelta(seconds=1)
            ).isoformat(),
            operator_confirmed_no_mapping_error=True,
            yymm4_product_version="4.53.0.9",
        )
    assert output.read_bytes() == original


def test_collector_rejects_nonlocal_result_target(
    isolated_pilot: Path,
    tmp_path: Path,
) -> None:
    project = _write_import_project(isolated_pilot, _derived_rows(isolated_pilot))
    unsafe_output = tmp_path / "operator_result.json"
    with pytest.raises(
        ValueError,
        match="OPERATOR_RESULT_TARGET_MUST_BE_EXACT_LOCAL_PATH",
    ):
        collect_new_banknote_yymm4_import_result(
            pilot_dir=isolated_pilot,
            project_path=project,
            output_path=unsafe_output,
            not_before_utc=(
                datetime.now(timezone.utc) - timedelta(seconds=1)
            ).isoformat(),
            operator_confirmed_no_mapping_error=True,
            yymm4_product_version="4.53.0.9",
        )
    assert not unsafe_output.exists()


def test_local_operator_targets_are_ignored_and_untracked() -> None:
    for name in (
        LOCAL_PROJECT_FILENAME,
        LOCAL_RESULT_FILENAME,
        LOCAL_BATCH_STATE_FILENAME,
    ):
        candidate = DEFAULT_PILOT_DIR / LOCAL_OUTPUT_DIRNAME / name
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", str(candidate)],
            cwd=REPO_ROOT,
            check=False,
        )
        assert ignored.returncode == 0, name
    tracked = subprocess.run(
        [
            "git",
            "ls-files",
            str(DEFAULT_PILOT_DIR / LOCAL_OUTPUT_DIRNAME),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert tracked.returncode == 0
    assert not tracked.stdout.strip()


def test_cli_preflight_writes_explicit_utf8_json(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result_json = tmp_path / "日本語-preflight.json"
    code = operator_main(
        [
            "preflight",
            "--pilot",
            str(DEFAULT_PILOT_DIR),
            "--result-json",
            str(result_json),
        ]
    )
    assert code == 0
    capsys.readouterr()
    assert result_json.read_bytes().startswith(b"{")
    assert not result_json.read_bytes().startswith(b"\xef\xbb\xbf")
    assert _load(result_json)["status"] == "passed"
