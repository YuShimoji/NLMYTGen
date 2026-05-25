from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = REPO_ROOT / "samples" / "_probe" / "baseball" / "static"
PNG_PATH = STATIC_DIR / "baseball_pitch_event_p05.png"
MANIFEST_PATH = STATIC_DIR / "baseball_pitch_event_p05_manifest.json"
READBACK_PATH = STATIC_DIR / "baseball_pitch_event_p05_readback.json"
VISUAL_DATA_SAMPLE = (
    REPO_ROOT
    / "lanes"
    / "sports_news"
    / "examples"
    / "baseball_pitch_event_visual_data_sample.json"
)
GUI_PACKAGE = REPO_ROOT / "gui" / "package.json"


def _png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    assert data[12:16] == b"IHDR"
    return struct.unpack(">II", data[16:24])


def test_baseball_static_capture_script_is_registered() -> None:
    package = json.loads(GUI_PACKAGE.read_text(encoding="utf-8"))

    assert package["scripts"]["capture:baseball-static"] == (
        "electron capture_baseball_infographic_static.js"
    )


def test_baseball_static_png_artifact_is_1280x720() -> None:
    assert PNG_PATH.exists()
    assert PNG_PATH.stat().st_size > 100_000

    assert _png_size(PNG_PATH) == (1280, 720)


def test_baseball_static_manifest_tracks_input_hash_and_boundaries() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    readback = json.loads(READBACK_PATH.read_text(encoding="utf-8"))
    expected_input_hash = hashlib.sha256(VISUAL_DATA_SAMPLE.read_bytes()).hexdigest()
    expected_output_hash = hashlib.sha256(PNG_PATH.read_bytes()).hexdigest()

    assert manifest["schema_version"] == "baseball_static_render_manifest.v1"
    assert manifest["artifact_type"] == "baseball_static_png_export"
    assert manifest["input"]["visual_data_path"] == (
        "lanes/sports_news/examples/baseball_pitch_event_visual_data_sample.json"
    )
    assert manifest["input"]["sha256"] == expected_input_hash
    assert manifest["output"]["png_path"] == "samples/_probe/baseball/static/baseball_pitch_event_p05.png"
    assert manifest["output"]["sha256"] == expected_output_hash
    assert manifest["output"]["width"] == 1280
    assert manifest["output"]["height"] == 720
    assert manifest["variant"] == "detailed"
    assert manifest["export_settings"]["currentPitchNumber"] == 5
    assert manifest["boundaries"]["not_yymm4_proof"] is True
    assert manifest["boundaries"]["not_animation_export"] is True
    assert manifest["boundaries"]["not_creative_acceptance"] is True

    assert readback["status"] == "passed"
    assert readback["output_sha256"] == expected_output_hash
    assert readback["not_yymm4_proof"] is True
    assert readback["dom_state"]["design_canvas_visible"] is False
    assert readback["dom_state"]["tweaks_visible"] is False
