from __future__ import annotations

import hashlib
import json
import struct
import subprocess
from pathlib import Path

import pytest

from src.pipeline import media_validation
from src.pipeline.media_validation import (
    decode_with_ffmpeg,
    inspect_iso_bmff,
    probe_with_ffprobe,
)


def _box(
    box_type: bytes,
    payload: bytes = b"",
    *,
    extended: bool = False,
    to_eof: bool = False,
) -> bytes:
    assert len(box_type) == 4
    if to_eof:
        return struct.pack(">I4s", 0, box_type) + payload
    if extended:
        return struct.pack(">I4sQ", 1, box_type, 16 + len(payload)) + payload
    return struct.pack(">I4s", 8 + len(payload), box_type) + payload


def _mvhd(*, timescale: int = 1000, duration: int = 59383) -> bytes:
    payload = b"\x00\x00\x00\x00" + struct.pack(">IIII", 0, 0, timescale, duration)
    return _box(b"mvhd", payload)


def _valid_bmff(*, delayed_ftyp: bool = True) -> bytes:
    free = _box(b"free", b"\x00" * 64) if delayed_ftyp else b""
    ftyp_payload = b"isom" + struct.pack(">I", 512) + b"isomiso2avc1mp41"
    ftyp = _box(b"ftyp", ftyp_payload, extended=True)
    moov = _box(b"moov", _mvhd())
    mdat = _box(b"mdat", b"\x00\x01\x02\x03", to_eof=True)
    return free + ftyp + moov + mdat


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_inspect_streams_boxes_and_finds_ftyp_after_first_32_bytes(
    tmp_path: Path,
) -> None:
    media = tmp_path / "delayed-ftyp.mp4"
    media.write_bytes(_valid_bmff(delayed_ftyp=True))

    result = inspect_iso_bmff(media)

    assert result["status"] == "passed"
    assert result["error_code"] is None
    assert result["failed_checks"] == []
    assert result["is_yymm4_project_json"] is False
    assert result["file_size_bytes"] == media.stat().st_size
    assert result["sha256"] == _sha256(media)
    assert result["top_level_box_types"] == ["free", "ftyp", "moov", "mdat"]
    ftyp_box = result["top_level_boxes"][1]
    assert ftyp_box["offset"] > 32
    assert ftyp_box["header_size"] == 16
    assert result["top_level_boxes"][-1]["size"] == 12
    assert result["ftyp"] == {
        "major_brand": "isom",
        "minor_version": 512,
        "compatible_brands": ["isom", "iso2", "avc1", "mp41"],
    }
    assert result["mvhd"] == {
        "timescale": 1000,
        "duration_units": 59383,
        "duration_seconds": pytest.approx(59.383),
    }
    assert all(result["checks"].values())


def test_inspect_rejects_utf8_bom_yymm4_project_json(tmp_path: Path) -> None:
    media = tmp_path / "project-misnamed-as-video.mp4"
    project = {
        "FilePath": str(media),
        "SelectedTimelineIndex": 0,
        "Timelines": [{"Name": "メイン", "Items": []}],
    }
    media.write_bytes(
        b" \r\n\xef\xbb\xbf\t"
        + json.dumps(project, ensure_ascii=False).encode("utf-8")
    )

    result = inspect_iso_bmff(media)

    assert result["status"] == "failed"
    assert result["error_code"] == "render_is_yymm4_project_json_not_mp4"
    assert result["failed_checks"] == ["not_yymm4_project_json"]
    assert result["is_yymm4_project_json"] is True
    assert result["top_level_boxes"] == []
    assert result["ftyp"] is None


def test_inspect_rejects_box_that_exceeds_file_bounds(tmp_path: Path) -> None:
    media = tmp_path / "truncated.mp4"
    media.write_bytes(struct.pack(">I4s", 128, b"free") + b"short")

    result = inspect_iso_bmff(media)

    assert result["status"] == "failed"
    assert result["error_code"] == "malformed_iso_bmff_bounds"
    assert result["failed_checks"] == ["top_level_boxes_well_formed"]


def test_inspect_requires_ftyp_moov_and_mdat(tmp_path: Path) -> None:
    media = tmp_path / "missing-mdat.mp4"
    ftyp_payload = b"isom" + struct.pack(">I", 0) + b"isom"
    media.write_bytes(_box(b"ftyp", ftyp_payload) + _box(b"moov", _mvhd()))

    result = inspect_iso_bmff(media)

    assert result["status"] == "failed"
    assert result["error_code"] == "required_iso_bmff_boxes_missing"
    assert result["failed_checks"] == ["mdat_present"]


def test_probe_with_ffprobe_returns_sanitized_selected_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    media = tmp_path / "レビュー.mp4"
    media.write_bytes(_valid_bmff())
    executable = tmp_path / "private-bin" / "ffprobe.exe"
    payload = {
        "streams": [
            {
                "index": 0,
                "codec_type": "video",
                "codec_name": "h264",
                "profile": "Main",
                "codec_tag_string": "avc1",
                "width": 1920,
                "height": 1080,
                "pix_fmt": "yuv420p",
                "avg_frame_rate": "60/1",
                "duration": "59.383000",
                "bit_rate": "240000480",
                "nb_frames": "3563",
                "tags": {"encoder": "h264_nvenc"},
            },
            {
                "index": 1,
                "codec_type": "audio",
                "codec_name": "aac",
                "profile": "LC",
                "sample_rate": "48000",
                "channels": 2,
                "channel_layout": "stereo",
                "bit_rate": "171024",
            },
        ],
        "format": {
            "filename": str(media),
            "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
            "format_long_name": "QuickTime / MOV",
            "duration": "59.383008",
            "size": "1782869795",
            "bit_rate": "240185851",
            "probe_score": 100,
            "tags": {
                "major_brand": "isom",
                "minor_version": "512",
                "compatible_brands": "isomiso2avc1mp41",
            },
        },
    }

    def fake_run(command: list[str], **_: object) -> subprocess.CompletedProcess[bytes]:
        if "-version" in command:
            return subprocess.CompletedProcess(
                command,
                0,
                stdout=b"ffprobe version 8.0.1-test Copyright\n",
                stderr=b"",
            )
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            stderr=f"{media}: 日本語の確認".encode("utf-8"),
        )

    monkeypatch.setattr(media_validation.subprocess, "run", fake_run)

    result = probe_with_ffprobe(media, executable=executable)

    assert result["status"] == "passed"
    assert result["tool"] == {"name": "ffprobe", "version": "8.0.1-test"}
    assert result["format"]["compatible_brands"] == ["isom", "iso2", "avc1", "mp41"]
    assert result["streams"][0]["fps"] == 60.0
    assert result["streams"][1]["sample_rate_hz"] == 48000
    assert result["stderr_summary"] == "<LOCAL_PATH>: 日本語の確認"
    serialized = json.dumps(result, ensure_ascii=False)
    assert str(tmp_path) not in serialized
    assert str(executable) not in serialized


def test_decode_with_ffmpeg_is_full_file_by_default_and_preserves_source_hash(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    media = tmp_path / "source.mp4"
    media.write_bytes(_valid_bmff())
    executable = tmp_path / "bin" / "ffmpeg.exe"
    commands: list[list[str]] = []

    def fake_run(command: list[str], **_: object) -> subprocess.CompletedProcess[bytes]:
        commands.append(command)
        if "-version" in command:
            return subprocess.CompletedProcess(
                command,
                0,
                stdout=b"ffmpeg version 8.0.1-test Copyright\n",
                stderr=b"",
            )
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=b"",
            stderr="デコード確認".encode("utf-8"),
        )

    monkeypatch.setattr(media_validation.subprocess, "run", fake_run)
    before = _sha256(media)

    result = decode_with_ffmpeg(media, executable=executable)

    assert result["status"] == "passed"
    assert result["error_code"] is None
    assert result["scope"] == "full_file"
    assert result["requested_seconds"] is None
    assert result["source_sha256_before"] == before
    assert result["source_sha256_after"] == before
    assert result["source_unchanged"] is True
    assert _sha256(media) == before
    assert result["stderr_summary"] == "デコード確認"
    decode_command = commands[-1]
    assert "-t" not in decode_command
    assert decode_command[-7:] == [
        "-map",
        "0:v?",
        "-map",
        "0:a?",
        "-f",
        "null",
        "-",
    ]


def test_decode_with_ffmpeg_supports_bounded_smoke_seconds(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    media = tmp_path / "source.mp4"
    media.write_bytes(_valid_bmff())
    commands: list[list[str]] = []

    def fake_run(command: list[str], **_: object) -> subprocess.CompletedProcess[bytes]:
        commands.append(command)
        output = b"ffmpeg version 8.0-test\n" if "-version" in command else b""
        return subprocess.CompletedProcess(command, 0, stdout=output, stderr=b"")

    monkeypatch.setattr(media_validation.subprocess, "run", fake_run)

    result = decode_with_ffmpeg(media, executable="ffmpeg", seconds=5)

    assert result["status"] == "passed"
    assert result["scope"] == "first_n_seconds"
    assert result["requested_seconds"] == 5.0
    assert commands[-1][commands[-1].index("-t") + 1] == "5"
