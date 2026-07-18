from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import src.pipeline.new_banknote_yymm4_existing_evidence_revalidation as revalidation
from src.pipeline.new_banknote_yymm4_existing_evidence_revalidation import (
    ARTIFACT_FILENAMES,
    LIMITATIONS_FILENAME,
    README_FILENAME,
    READBACK_FILENAME,
    RECEIPT_FILENAME,
    SUCCESSOR_STATE_ID,
    TRACEABILITY_FILENAME,
    build_existing_yymm4_evidence_revalidation,
    inspect_existing_yymm4_evidence,
    main as revalidation_main,
    render_existing_yymm4_evidence_revalidation_artifacts,
)
from src.pipeline.new_banknote_yymm4_import_operator_batch import (
    DEFAULT_PILOT_DIR,
    LOCAL_BATCH_STATE_FILENAME,
    LOCAL_OUTPUT_DIRNAME,
    LOCAL_PROJECT_FILENAME,
    LOCAL_RESULT_FILENAME,
    PROFILE_VERSION,
    _load_contract_inputs,
    collect_new_banknote_yymm4_import_result,
)
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


REPO_ROOT = Path(__file__).resolve().parents[1]
_PRIVATE_PATH_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/]|\\\\[^\\\s]+[\\/]|/home/|/users/)"
)


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _snapshot(paths: list[Path]) -> dict[str, tuple[int, int, str]]:
    return {
        path.name: (path.stat().st_size, path.stat().st_mtime_ns, _sha256(path))
        for path in paths
    }


@pytest.fixture
def isolated_pilot(tmp_path: Path) -> Path:
    target = tmp_path / "new_banknote_pilot"
    shutil.copytree(
        DEFAULT_PILOT_DIR,
        target,
        ignore=shutil.ignore_patterns(LOCAL_OUTPUT_DIRNAME),
    )
    return target


def _write_project(pilot: Path, rows: list[tuple[str, str]]) -> Path:
    project_path = pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_PROJECT_FILENAME
    project_path.parent.mkdir(parents=True, exist_ok=True)
    frames = [0, 391, 1096, 1434, 1818, 2225, 2835, 3262, 3995]
    lengths = [391, 705, 338, 384, 407, 610, 427, 733, 420]
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
            "VoiceCache": {"private_fixture_field": f"voice-{index + 1}"},
        }
        for index, (character, text) in enumerate(rows)
    ]
    project = {
        "FilePath": str(project_path.resolve()),
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
                "Length": 4415,
            }
        ],
    }
    save_ymmp(project, project_path)
    return project_path


def _make_evidence(
    pilot: Path,
    *,
    note: str | None = None,
) -> tuple[Path, Path, Path]:
    inputs = _load_contract_inputs(pilot)
    project = _write_project(pilot, list(inputs["derived_rows"]))
    result = pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_RESULT_FILENAME
    batch = pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_BATCH_STATE_FILENAME
    started = (datetime.now(timezone.utc) - timedelta(seconds=5)).isoformat()
    collected = collect_new_banknote_yymm4_import_result(
        pilot_dir=pilot,
        project_path=project,
        output_path=result,
        not_before_utc=started,
        operator_confirmed_no_mapping_error=True,
        pronunciation_notes=note or "",
        yymm4_product_version="4.54.0.1+fixture",
    )
    assert collected["status"] == "success"
    if note is None:
        payload = _load(result)
        payload["operator_observation"].pop(
            "pronunciation_or_clipping_notes", None
        )
        result.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    batch.write_text(
        json.dumps(
            {
                "schema_version": (
                    "new_banknote_yymm4_import_operator_batch.local.v1"
                ),
                "batch_id": "new-banknote-yymm4-import-observation-v1",
                "batch_not_before_utc": started,
                "yymm4_exe": "X:/private/YukkuriMovieMaker.exe",
                "yymm4_product_version": "4.54.0.1+fixture",
                "profile_observation_version": PROFILE_VERSION,
                "target_project": str(project.resolve()),
                "target_result": str(result.resolve()),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return project, result, batch


def test_current_lock_and_existing_evidence_pass_without_source_mutation(
    isolated_pilot: Path,
) -> None:
    project, result, batch = _make_evidence(isolated_pilot)
    sources = [project, result, batch]
    before = _snapshot(sources)

    outcome = inspect_existing_yymm4_evidence(
        pilot_dir=isolated_pilot,
        project_path=project,
        result_path=result,
        batch_state_path=batch,
    )

    assert outcome["status"] == "passed"
    assert outcome["failed_checks"] == []
    assert all(outcome["checks"].values())
    receipt = outcome["receipt"]
    assert receipt["successor_state_id"] == SUCCESSOR_STATE_ID
    assert receipt["current_approval"]["status"] == "valid"
    assert receipt["current_lineage"]["stage_coverage"] == [
        f"T{index:02d}" for index in range(8)
    ]
    assert receipt["structural_readback"]["VoiceItem_count"] == 9
    assert receipt["structural_readback"]["character_counts"] == {
        "ゆっくり霊夢": 3,
        "ゆっくり魔理沙": 6,
    }
    assert receipt["structural_readback"]["exact_character_text_order"] is True
    assert receipt["structural_readback"]["missing_count"] == 0
    assert receipt["structural_readback"]["duplicate_count"] == 0
    assert receipt["structural_readback"]["reordered"] is False
    assert receipt["structural_readback"]["fps"] == 60
    assert receipt["structural_readback"]["timeline_frames"] == 4415
    assert receipt["structural_readback"]["duration_seconds"] == 73.583333
    assert receipt["before_after_immutability"][
        "all_source_evidence_unchanged"
    ] is True
    assert receipt["pronunciation_and_clipping"] == {
        "pronunciation_status": "unknown",
        "clipping_status": "unknown",
        "rhythm_status": "unknown",
        "existing_note_present": False,
        "existing_note": None,
        "note_source": "not_recorded",
        "evidence_grade": "unknown",
        "acceptance_claimed": False,
    }
    assert _snapshot(sources) == before


def test_deterministic_sanitized_artifacts_and_cli(
    isolated_pilot: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    project, result, batch = _make_evidence(isolated_pilot)
    first = render_existing_yymm4_evidence_revalidation_artifacts(
        pilot_dir=isolated_pilot,
        project_path=project,
        result_path=result,
        batch_state_path=batch,
    )
    second = render_existing_yymm4_evidence_revalidation_artifacts(
        pilot_dir=isolated_pilot,
        project_path=project,
        result_path=result,
        batch_state_path=batch,
    )
    assert first == second
    assert tuple(first) == ARTIFACT_FILENAMES

    combined = b"\n".join(first.values()).decode("utf-8")
    assert not _PRIVATE_PATH_RE.search(combined)
    assert str(tmp_path) not in combined
    assert "notebooklm.google.com" not in combined.lower()
    assert '"raw_text"' not in combined
    assert '"source_body"' not in combined
    assert '"transcript_body"' not in combined
    assert "VoiceCache" not in combined

    output = tmp_path / "tracked_output"
    code = revalidation_main(
        [
            "--pilot",
            str(isolated_pilot),
            "--project",
            str(project),
            "--result",
            str(result),
            "--batch-state",
            str(batch),
            "--output-dir",
            str(output),
        ]
    )
    assert code == 0
    public = json.loads(capsys.readouterr().out)
    assert public["status"] == "passed"
    assert public["yymm4_launched"] is False
    assert sorted(path.name for path in output.iterdir()) == sorted(
        ARTIFACT_FILENAMES
    )
    assert _load(output / RECEIPT_FILENAME)["status"] == "accepted"
    assert _load(output / READBACK_FILENAME)["status"] == "passed"
    assert _load(output / TRACEABILITY_FILENAME)["status"] == "passed"
    assert "YMM4は再実行していません" in (
        output / README_FILENAME
    ).read_text(encoding="utf-8")
    assert "pronunciation / rhythm / clipping" in (
        output / LIMITATIONS_FILENAME
    ).read_text(encoding="utf-8")


def test_result_project_hash_mismatch_is_rejected(isolated_pilot: Path) -> None:
    project, result, batch = _make_evidence(isolated_pilot)
    payload = _load(result)
    payload["project_identity"]["sha256"] = "0" * 64
    result.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    outcome = inspect_existing_yymm4_evidence(
        pilot_dir=isolated_pilot,
        project_path=project,
        result_path=result,
        batch_state_path=batch,
    )
    assert outcome["status"] == "failed"
    assert outcome["checks"]["result_project_sha256_matches"] is False
    assert "result_project_sha256_matches" in outcome["failed_checks"]


def test_approved_csv_drift_is_rejected_before_evidence_acceptance(
    isolated_pilot: Path,
) -> None:
    project, result, batch = _make_evidence(isolated_pilot)
    derived = isolated_pilot / "derived_yymm4_import.csv"
    derived.write_text(
        derived.read_text(encoding="utf-8") + "ゆっくり霊夢,drift\n",
        encoding="utf-8",
    )
    outcome = inspect_existing_yymm4_evidence(
        pilot_dir=isolated_pilot,
        project_path=project,
        result_path=result,
        batch_state_path=batch,
    )
    assert outcome["status"] == "failed"
    assert outcome["checks"]["current_approval_and_lineage_lock_valid"] is False
    assert any(
        item.startswith("current_contract_invalid")
        for item in outcome["failed_checks"]
    )


def test_project_cue_speaker_and_order_drift_is_rejected(
    isolated_pilot: Path,
) -> None:
    project, result, batch = _make_evidence(isolated_pilot)
    payload = load_ymmp(project)
    items = payload["Timelines"][0]["Items"]
    items[0]["CharacterName"] = "ゆっくり魔理沙"
    items[1]["Serif"], items[2]["Serif"] = items[2]["Serif"], items[1]["Serif"]
    save_ymmp(payload, project)
    outcome = inspect_existing_yymm4_evidence(
        pilot_dir=isolated_pilot,
        project_path=project,
        result_path=result,
        batch_state_path=batch,
    )
    assert outcome["status"] == "failed"
    assert outcome["checks"]["character_counts_3_6"] is False
    assert outcome["checks"]["exact_text_order"] is False
    assert outcome["checks"]["exact_character_text_order"] is False


def test_evidence_mutation_during_read_is_rejected(
    isolated_pilot: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project, result, batch = _make_evidence(isolated_pilot)
    original = revalidation.load_ymmp

    def mutating_load(path: Path) -> dict:
        loaded = original(path)
        stat = Path(path).stat()
        os.utime(
            path,
            ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000),
        )
        return loaded

    monkeypatch.setattr(revalidation, "load_ymmp", mutating_load)
    outcome = inspect_existing_yymm4_evidence(
        pilot_dir=isolated_pilot,
        project_path=project,
        result_path=result,
        batch_state_path=batch,
    )
    assert outcome["status"] == "failed"
    assert outcome["checks"]["source_evidence_before_after_equal"] is False


def test_existing_note_is_observed_not_verified(isolated_pilot: Path) -> None:
    project, result, batch = _make_evidence(
        isolated_pilot,
        note="cue_006: pronunciation needs human review",
    )
    outcome = inspect_existing_yymm4_evidence(
        pilot_dir=isolated_pilot,
        project_path=project,
        result_path=result,
        batch_state_path=batch,
    )
    assert outcome["status"] == "passed"
    audio = outcome["receipt"]["pronunciation_and_clipping"]
    assert audio["pronunciation_status"] == "observed_note_present"
    assert audio["clipping_status"] == "observed_note_present"
    assert audio["evidence_grade"] == "observed"
    assert audio["acceptance_claimed"] is False


def test_version_mismatch_is_warning_only_and_no_launch_path_exists(
    isolated_pilot: Path,
) -> None:
    project, result, batch = _make_evidence(isolated_pilot)
    outcome = inspect_existing_yymm4_evidence(
        pilot_dir=isolated_pilot,
        project_path=project,
        result_path=result,
        batch_state_path=batch,
    )
    assert outcome["status"] == "passed"
    assert outcome["warnings"] == [
        "YMM4_PROFILE_VERSION_MISMATCH_WARNING_ONLY"
    ]
    receipt = outcome["receipt"]
    assert receipt["version_readback"]["profile_version_match"] is False
    assert receipt["version_readback"]["mismatch_policy"] == "warning_only"
    assert receipt["execution_boundary"]["yymm4_launched"] is False
    assert receipt["execution_boundary"]["computer_use_invoked"] is False
    assert receipt["execution_boundary"]["render_or_media_generated"] is False
    source = Path(revalidation.__file__).read_text(encoding="utf-8")
    assert "subprocess" not in source
    assert "Start-Process" not in source
    assert "YukkuriMovieMaker.exe" not in source


def test_output_cannot_overlap_ignored_evidence_directory(
    isolated_pilot: Path,
) -> None:
    project, result, batch = _make_evidence(isolated_pilot)
    outcome = build_existing_yymm4_evidence_revalidation(
        pilot_dir=isolated_pilot,
        project_path=project,
        result_path=result,
        batch_state_path=batch,
        output_dir=project.parent,
    )
    assert outcome == {
        "status": "failed",
        "failed_checks": ["OUTPUT_DIRECTORY_OVERLAPS_SOURCE_EVIDENCE"],
        "written_files": [],
    }


def test_local_operator_evidence_remains_ignored_and_untracked() -> None:
    local = DEFAULT_PILOT_DIR / LOCAL_OUTPUT_DIRNAME
    for name in (
        LOCAL_PROJECT_FILENAME,
        LOCAL_RESULT_FILENAME,
        LOCAL_BATCH_STATE_FILENAME,
    ):
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", str(local / name)],
            cwd=REPO_ROOT,
            check=False,
        )
        assert ignored.returncode == 0, name
    tracked = subprocess.run(
        ["git", "ls-files", str(local)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert tracked.returncode == 0
    assert not tracked.stdout.strip()
