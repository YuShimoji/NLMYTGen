from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GUI_PACKAGE = REPO_ROOT / "gui" / "package.json"
SCRIPT_PATH = REPO_ROOT / "gui" / "capture_baseball_infographic_frames.js"
PLAN_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "animation"
    / "baseball_pitch_event_p05_animation_export_plan.json"
)
MANIFEST_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "animation"
    / "baseball_pitch_event_p05_animation_manifest.json"
)
READBACK_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "animation"
    / "baseball_pitch_event_p05_animation_readback.json"
)
HANDOFF_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "animation"
    / "baseball_pitch_event_p05_animation_handoff.md"
)
FRAME_DIR = (
    REPO_ROOT / "samples" / "_probe" / "baseball" / "animation" / "frames" / "baseball_pitch_event_p05"
)
VISUAL_DATA_SAMPLE = (
    REPO_ROOT
    / "lanes"
    / "sports_news"
    / "examples"
    / "baseball_pitch_event_visual_data_sample.json"
)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    assert data[12:16] == b"IHDR"
    return struct.unpack(">II", data[16:24])


def _frame_path(index: int) -> Path:
    return FRAME_DIR / f"baseball_pitch_event_p05_f{index:03d}.png"


def test_baseball_frame_capture_script_is_registered() -> None:
    package = _load_json(GUI_PACKAGE)

    assert SCRIPT_PATH.exists()
    assert package["scripts"]["capture:baseball-frames"] == (
        "electron capture_baseball_infographic_frames.js"
    )


def test_baseball_frame_sequence_outputs_are_1280x720_pngs() -> None:
    for index in range(5):
        frame_path = _frame_path(index)
        assert frame_path.exists()
        assert frame_path.stat().st_size > 100_000
        assert _png_size(frame_path) == (1280, 720)


def test_baseball_frame_sequence_manifest_tracks_hashes_and_boundaries() -> None:
    manifest = _load_json(MANIFEST_PATH)
    readback = _load_json(READBACK_PATH)

    assert manifest["schema_version"] == "baseball_frame_sequence_manifest.v1"
    assert manifest["artifact_type"] == "baseball_frame_sequence_export"
    assert manifest["input"]["visual_data_path"] == (
        "lanes/sports_news/examples/baseball_pitch_event_visual_data_sample.json"
    )
    assert manifest["input"]["visual_data_sha256"] == _sha256(VISUAL_DATA_SAMPLE)
    assert manifest["input"]["plan_sha256"] == _sha256(PLAN_PATH)
    assert manifest["output"]["frame_dir"] == (
        "samples/_probe/baseball/animation/frames/baseball_pitch_event_p05"
    )
    assert manifest["output"]["frame_pattern"] == "baseball_pitch_event_p05_f%03d.png"
    assert manifest["output"]["frame_count"] == 5
    assert manifest["output"]["width"] == 1280
    assert manifest["output"]["height"] == 720
    assert manifest["output"]["fps"] == 30
    assert manifest["output"]["duration_ms"] == 1200

    assert len(manifest["frames"]) == 5
    assert manifest["frames"][0]["label"] == "previous_pitch_context"
    assert manifest["frames"][0]["pitch_index"] == 0
    assert manifest["frames"][-1]["label"] == "current_pitch_lock"
    assert manifest["frames"][-1]["pitch_index"] == 1
    for frame in manifest["frames"]:
        frame_path = REPO_ROOT / frame["path"]
        assert frame["sha256"] == _sha256(frame_path)
        assert frame["width"] == 1280
        assert frame["height"] == 720

    assert manifest["boundaries"]["not_yymm4_placement"] is True
    assert manifest["boundaries"]["not_clip_export"] is True
    assert manifest["boundaries"]["not_creative_acceptance"] is True
    assert manifest["boundaries"]["not_publish_gate"] is True

    assert readback["status"] == "passed"
    assert readback["checks"]["frame_count_matches_plan"] is True
    assert readback["checks"]["all_frames_exist"] is True
    assert readback["checks"]["all_frames_1280x720"] is True
    assert readback["checks"]["hashes_match_manifest"] is True
    assert readback["checks"]["no_design_canvas_or_tweaks"] is True
    assert readback["checks"]["no_clip_export"] is True
    assert readback["checks"]["not_yymm4_placement"] is True
    assert readback["checks"]["not_creative_acceptance"] is True
    assert readback["failed_checks"] == []
    assert readback["unique_frame_hash_count"] >= 2


def test_baseball_frame_sequence_handoff_keeps_manual_gate_clear() -> None:
    handoff = HANDOFF_PATH.read_text(encoding="utf-8")

    assert "not a video clip" in handoff
    assert "not a YMM4 placement proof" in handoff
    assert "not creative acceptance" in handoff
    assert "Verify BN-05 manual preview" in handoff
