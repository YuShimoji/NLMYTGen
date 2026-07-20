from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess

import pytest

from src.pipeline import silent_media_runtime as runtime


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
INCIDENT_RECEIPT = ROOT / "docs/verification/development_audio_incident_receipt.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_silent_policy_is_the_default_and_no_allow_value_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(runtime.AUDIO_POLICY_ENV, raising=False)
    assert runtime.resolve_audio_policy() == "silent"
    monkeypatch.setenv(runtime.AUDIO_POLICY_ENV, "allow")
    with pytest.raises(runtime.SilentPolicyError, match="only 'silent'"):
        runtime.resolve_audio_policy()


@pytest.mark.parametrize(
    "command",
    [
        ["VOICEVOX.exe"],
        ["SofTalkW.exe"],
        ["YukkuriMovieMaker.exe"],
        ["ffplay.exe", "preview.wav"],
        ["mpv.exe", "preview.wav"],
        ["vlc.exe", "preview.wav"],
        ["wmplayer.exe", "preview.wav"],
        ["python.exe", "-c", "import winsound; winsound.PlaySound('x', 0)"],
        ["python.exe", "-c", "import playsound"],
        ["pwsh.exe", "-Command", "Add-Type -AssemblyName System.Speech; $s.Speak('x')"],
    ],
)
def test_audible_frontends_and_playback_paths_are_denied(command: list[str]) -> None:
    with pytest.raises(runtime.SilentPolicyError):
        runtime.assert_command_allowed(command)


def test_synthesis_is_distinct_from_playback() -> None:
    assert runtime.assert_command_allowed(["voicevox_engine.exe", "--host", "127.0.0.1"]) == (
        "synthesis_engine_only"
    )
    assert runtime.assert_command_allowed(["ffprobe.exe", "-show_streams", "fixture.wav"]) == (
        "static_media_metadata"
    )
    assert runtime.assert_command_allowed(["ffmpeg.exe", "-i", "input.wav", "output.wav"]) == (
        "media_file_generation_or_null_decode"
    )


def test_browser_requires_guard_and_launch_has_all_silent_flags(tmp_path: Path) -> None:
    browser = tmp_path / "chrome.exe"
    profile = tmp_path / "isolated-profile"
    with pytest.raises(runtime.SilentPolicyError, match="silent inspection wrapper"):
        runtime.assert_command_allowed([str(browser), "about:blank"])
    command = runtime.build_browser_command(browser, profile)
    assert "--mute-audio" in command
    assert "--autoplay-policy=user-gesture-required" in command
    assert "--headless=new" in command
    assert "--disable-background-mode" in command
    assert "--disable-background-networking" in command
    assert "--disable-crash-reporter" in command
    assert "--remote-debugging-address=127.0.0.1" in command
    assert f"--user-data-dir={profile}" in command
    assert all("allow-audio" not in value for value in command)


def test_dom_guard_precedes_navigation_contract_and_covers_new_media() -> None:
    source = runtime.DOM_MEDIA_GUARD_SCRIPT
    assert "HTMLMediaElement.prototype.play" in source
    assert "node.muted = true" in source
    assert "node.volume = 0" in source
    assert "node.autoplay = false" in source
    assert "node.removeAttribute('autoplay')" in source
    assert "node.pause()" in source
    assert "MutationObserver" in source
    assert "observer.observe(document" in source
    assert "Page.addScriptToEvaluateOnNewDocument" in Path(runtime.__file__).read_text(
        encoding="utf-8"
    )


def test_process_ancestry_and_preexisting_exclusion() -> None:
    snapshot = {
        10: {"parent_pid": 1},
        11: {"parent_pid": 10},
        12: {"parent_pid": 11},
        20: {"parent_pid": 1},
    }
    assert runtime.descendant_pids(10, snapshot) == {10, 11, 12}
    baseline = {11, 20}
    assert runtime.descendant_pids(10, snapshot) - baseline == {10, 12}


def test_runtime_result_instrumentation_names_required_process_and_session_fields() -> None:
    source = Path(runtime.__file__).read_text(encoding="utf-8")
    for field in (
        '"pid"',
        '"parent_pid"',
        '"executable"',
        '"command_line_sanitized"',
        '"start_time"',
        '"project_owned"',
        '"sessions"',
    ):
        assert field in source


def test_zero_amplitude_fixture_is_inherently_inaudible(tmp_path: Path) -> None:
    receipt = runtime.create_zero_amplitude_fixture(tmp_path)
    assert receipt["waveform"] == "zero_amplitude"
    assert receipt["pcm_all_zero"] is True
    assert receipt["frame_count"] == 8000
    assert (tmp_path / "zero_amplitude.wav").read_bytes().startswith(b"RIFF")
    html = (tmp_path / "silent_media_fixture.html").read_text(encoding="utf-8")
    assert "autoplay" in html
    assert "zero_amplitude.wav" in html


def test_command_line_diagnostics_are_sanitized() -> None:
    raw = '"C:\\Users\\private\\Chrome\\chrome.exe" --user-data-dir=C:\\Users\\private\\profile'
    sanitized = runtime._sanitize_command_line(raw, [])
    assert "C:\\" not in sanitized
    assert "private" not in sanitized
    assert "<local-path>" in sanitized


def test_audio_session_helper_has_pid_guard_and_no_master_volume_call() -> None:
    source = (ROOT / "scripts/inspect_project_audio_sessions.ps1").read_text(encoding="utf-8")
    assert "owned.Contains((int)pid)" in source
    assert "volume.SetMute(true" in source
    # The vtable declaration is required; it must never be invoked.
    assert source.count("SetMasterVolume(") == 1
    assert "master_volume_operation = $false" in source
    assert "unowned_session_mutation = $false" in source


def test_incident_receipt_is_deterministic_and_private_path_free(tmp_path: Path) -> None:
    receipt = json.loads(INCIDENT_RECEIPT.read_text(encoding="utf-8"))
    assert receipt["root_cause"] == {
        "strongest_class": "C1_BROWSER_MEDIA_PLAYBACK",
        "confidence": "probable",
        "evidence_grade": "probable_from_operation_timeline",
        "exact_historical_emitter": "unknown",
        "overclaim_prevented": True,
    }
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    runtime._write_json(first, receipt)
    runtime._write_json(second, receipt)
    assert first.read_bytes() == second.read_bytes()
    tracked_evidence = INCIDENT_RECEIPT.read_text(encoding="utf-8") + (
        ROOT / "docs/verification/DEVELOPMENT_AUDIO_INCIDENT_2026-07-20.md"
    ).read_text(encoding="utf-8")
    assert "C:\\Users\\" not in tracked_evidence


def test_no_audio_fixture_is_tracked_in_guard_write_set() -> None:
    tracked = subprocess.check_output(
        ["git", "ls-files", "--", "artifacts/audio_diagnostics"], cwd=ROOT, text=True
    ).splitlines()
    assert tracked == []


def test_protected_approval_and_visual_artifacts_are_unchanged() -> None:
    approval = json.loads((PILOT / "human_script_approval_receipt.json").read_text(encoding="utf-8"))
    assert len(approval["approved_file_hashes"]) == 8
    for relative, expected in approval["approved_file_hashes"].items():
        assert _sha256(PILOT / relative) == expected

    supersession = json.loads(
        (PILOT / "reference_grounded_visual_design/ai_original_visual_supersession_receipt.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(supersession["protected_artifact_sha256"]) == 23
    for relative, expected in supersession["protected_artifact_sha256"].items():
        assert _sha256(ROOT / relative) == expected

    assert _sha256(
        PILOT / "reference_grounded_visual_design/reference_grounded_visual_proof_manifest.json"
    ) == "502809c0a183c398ed1eed2d8ce69c5471d6f189b68100a5557cf010af89022a"


@pytest.mark.skipif(os.name != "nt", reason="Core Audio helper is Windows-only")
def test_core_audio_inspection_is_supported_without_mutation() -> None:
    helper = ROOT / "scripts/inspect_project_audio_sessions.ps1"
    result = runtime.inspect_audio_sessions(helper, [], mode="inspect")
    assert result["supported"] is True
    assert result["owned_session_count"] == 0
    assert result["unowned_session_mutation"] is False
    assert result["master_volume_operation"] is False
