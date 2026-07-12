"""Headless, non-mutating validation helpers for local review media.

The helpers in this module deliberately return sanitized machine data.  They
never expose the selected executable path or the media path, and they never
write beside the source file.  ISO BMFF inspection is implemented with
streaming seeks so a large ``mdat`` payload is not loaded into memory.
"""

from __future__ import annotations

import hashlib
import json
import locale
import re
import shutil
import struct
import subprocess
import time
from pathlib import Path
from typing import Any, BinaryIO


YMM4_PROJECT_JSON_ERROR = "render_is_yymm4_project_json_not_mp4"


class _BoxParseError(ValueError):
    """Internal structured ISO BMFF parse failure."""

    def __init__(self, message: str, *, error_code: str = "malformed_iso_bmff_bounds") -> None:
        super().__init__(message)
        self.error_code = error_code


def inspect_iso_bmff(path: str | Path) -> dict[str, Any]:
    """Inspect a local ISO BMFF file without loading media payloads.

    A successful result requires well-bounded top-level ``ftyp``, ``moov``,
    and ``mdat`` boxes.  The function also recognizes a common operator error:
    a UTF-8 YMM4 project JSON saved under a video-output filename.
    """

    media_path = Path(path)
    result = _inspection_result()
    try:
        file_size = media_path.stat().st_size
        sha256 = _sha256(media_path)
    except OSError:
        result["error_code"] = "media_file_unreadable"
        result["failed_checks"] = ["source_readable"]
        return result

    result["file_size_bytes"] = file_size
    result["sha256"] = sha256
    result["checks"]["source_readable"] = True

    if _is_yymm4_project_json(media_path):
        result["error_code"] = YMM4_PROJECT_JSON_ERROR
        result["failed_checks"] = ["not_yymm4_project_json"]
        result["is_yymm4_project_json"] = True
        return result

    result["checks"]["not_yymm4_project_json"] = True
    try:
        with media_path.open("rb") as handle:
            boxes = _parse_box_range(handle, start=0, end=file_size)
    except (OSError, _BoxParseError) as exc:
        result["error_code"] = getattr(exc, "error_code", "media_file_unreadable")
        result["failed_checks"] = ["top_level_boxes_well_formed"]
        return result

    result["top_level_boxes"] = boxes
    box_types = [box["type"] for box in boxes]
    result["top_level_box_types"] = box_types
    result["checks"]["top_level_boxes_well_formed"] = True
    for box_type in ("ftyp", "moov", "mdat"):
        result["checks"][f"{box_type}_present"] = box_type in box_types

    missing = [
        f"{box_type}_present"
        for box_type in ("ftyp", "moov", "mdat")
        if box_type not in box_types
    ]
    if missing:
        result["error_code"] = "required_iso_bmff_boxes_missing"
        result["failed_checks"] = missing
        return result

    first_ftyp = next(box for box in boxes if box["type"] == "ftyp")
    try:
        with media_path.open("rb") as handle:
            result["ftyp"] = _read_ftyp(handle, first_ftyp)
    except (OSError, _BoxParseError):
        result["error_code"] = "invalid_ftyp_box"
        result["failed_checks"] = ["ftyp_valid"]
        return result
    result["checks"]["ftyp_valid"] = True

    first_moov = next(box for box in boxes if box["type"] == "moov")
    try:
        with media_path.open("rb") as handle:
            result["mvhd"] = _read_mvhd_from_moov(handle, first_moov)
    except (OSError, _BoxParseError):
        result["error_code"] = "invalid_mvhd_box"
        result["failed_checks"] = ["mvhd_valid_when_present"]
        return result
    result["checks"]["mvhd_valid_when_present"] = True

    result["status"] = "passed"
    result["error_code"] = None
    result["failed_checks"] = []
    return result


def probe_with_ffprobe(
    path: str | Path,
    executable: str | Path | None = None,
) -> dict[str, Any]:
    """Return selected ffprobe metadata without leaking local paths."""

    media_path = Path(path)
    tool = {"name": "ffprobe", "version": None}
    result: dict[str, Any] = {
        "status": "failed",
        "error_code": None,
        "tool": tool,
        "format": None,
        "streams": [],
        "stream_count": 0,
        "stderr_summary": "",
    }
    if not media_path.is_file():
        result["error_code"] = "media_file_unreadable"
        return result

    resolved = _resolve_executable(executable, "ffprobe")
    if resolved is None:
        result["error_code"] = "ffprobe_not_available"
        return result

    tool["version"] = _tool_version(resolved, "ffprobe")
    command = [
        resolved,
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        "-show_chapters",
        "-show_programs",
        "--",
        str(media_path),
    ]
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        result["error_code"] = (
            "ffprobe_timeout" if isinstance(exc, subprocess.TimeoutExpired) else "ffprobe_failed"
        )
        result["stderr_summary"] = _sanitize_output(
            _exception_output(exc), media_path=media_path, executable=resolved
        )
        return result

    stderr = _decode_bytes(completed.stderr)
    result["stderr_summary"] = _sanitize_output(
        stderr, media_path=media_path, executable=resolved
    )
    if completed.returncode != 0:
        result["error_code"] = "ffprobe_failed"
        return result

    try:
        payload = json.loads(_decode_bytes(completed.stdout))
    except (UnicodeError, json.JSONDecodeError, TypeError):
        result["error_code"] = "ffprobe_invalid_json"
        return result
    if not isinstance(payload, dict):
        result["error_code"] = "ffprobe_invalid_json"
        return result

    format_payload = payload.get("format")
    format_payload = format_payload if isinstance(format_payload, dict) else {}
    tags = format_payload.get("tags")
    tags = tags if isinstance(tags, dict) else {}
    result["format"] = {
        "format_name": _string_or_none(format_payload.get("format_name")),
        "format_long_name": _string_or_none(format_payload.get("format_long_name")),
        "duration_seconds": _float_or_none(format_payload.get("duration")),
        "size_bytes": _int_or_none(format_payload.get("size")),
        "bit_rate_bps": _int_or_none(format_payload.get("bit_rate")),
        "probe_score": _int_or_none(format_payload.get("probe_score")),
        "major_brand": _string_or_none(tags.get("major_brand")),
        "minor_version": _int_or_none(tags.get("minor_version")),
        "compatible_brands": _split_brands(tags.get("compatible_brands")),
    }

    raw_streams = payload.get("streams")
    if not isinstance(raw_streams, list):
        raw_streams = []
    result["streams"] = [
        _selected_stream(stream)
        for stream in raw_streams
        if isinstance(stream, dict)
    ]
    result["stream_count"] = len(result["streams"])
    result["status"] = "passed"
    return result


def decode_with_ffmpeg(
    path: str | Path,
    executable: str | Path | None = None,
    seconds: float | None = None,
) -> dict[str, Any]:
    """Decode all audio/video streams to FFmpeg's null muxer.

    ``seconds=None`` decodes the complete file.  Source hashes are calculated
    before and after the subprocess so the non-mutation guarantee is explicit.
    """

    media_path = Path(path)
    tool = {"name": "ffmpeg", "version": None}
    result: dict[str, Any] = {
        "status": "failed",
        "error_code": None,
        "tool": tool,
        "scope": "full_file" if seconds is None else "first_n_seconds",
        "requested_seconds": None if seconds is None else float(seconds),
        "exit_code": None,
        "elapsed_seconds": None,
        "stderr_summary": "",
        "source_sha256_before": None,
        "source_sha256_after": None,
        "source_unchanged": False,
    }
    if not media_path.is_file():
        result["error_code"] = "media_file_unreadable"
        return result
    if seconds is not None and (not isinstance(seconds, (int, float)) or seconds <= 0):
        result["error_code"] = "invalid_decode_duration"
        return result

    before = _sha256(media_path)
    result["source_sha256_before"] = before
    resolved = _resolve_executable(executable, "ffmpeg")
    if resolved is None:
        result["error_code"] = "ffmpeg_not_available"
        result["source_sha256_after"] = _sha256(media_path)
        result["source_unchanged"] = before == result["source_sha256_after"]
        return result

    tool["version"] = _tool_version(resolved, "ffmpeg")
    command = [
        resolved,
        "-hide_banner",
        "-v",
        "error",
        "-xerror",
        "-i",
        str(media_path),
    ]
    if seconds is not None:
        command.extend(["-t", format(float(seconds), ".12g")])
    command.extend(["-map", "0:v?", "-map", "0:a?", "-f", "null", "-"])

    started = time.monotonic()
    completed: subprocess.CompletedProcess[bytes] | None = None
    caught: OSError | subprocess.TimeoutExpired | None = None
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=900,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        caught = exc
    result["elapsed_seconds"] = round(time.monotonic() - started, 3)

    try:
        after = _sha256(media_path)
    except OSError:
        after = None
    result["source_sha256_after"] = after
    result["source_unchanged"] = before == after
    if not result["source_unchanged"]:
        result["error_code"] = "source_mutated_during_decode"
        return result

    if caught is not None:
        result["error_code"] = (
            "ffmpeg_decode_timeout"
            if isinstance(caught, subprocess.TimeoutExpired)
            else "ffmpeg_decode_failed"
        )
        result["stderr_summary"] = _sanitize_output(
            _exception_output(caught), media_path=media_path, executable=resolved
        )
        return result

    assert completed is not None
    result["exit_code"] = completed.returncode
    result["stderr_summary"] = _sanitize_output(
        _decode_bytes(completed.stderr), media_path=media_path, executable=resolved
    )
    if completed.returncode != 0:
        result["error_code"] = "ffmpeg_decode_failed"
        return result

    result["status"] = "passed"
    return result


def _inspection_result() -> dict[str, Any]:
    return {
        "status": "failed",
        "error_code": None,
        "failed_checks": [],
        "is_yymm4_project_json": False,
        "file_size_bytes": None,
        "sha256": None,
        "top_level_boxes": [],
        "top_level_box_types": [],
        "ftyp": None,
        "mvhd": None,
        "checks": {
            "source_readable": False,
            "not_yymm4_project_json": False,
            "top_level_boxes_well_formed": False,
            "ftyp_present": False,
            "moov_present": False,
            "mdat_present": False,
            "ftyp_valid": False,
            "mvhd_valid_when_present": False,
        },
    }


def _parse_box_range(
    handle: BinaryIO,
    *,
    start: int,
    end: int,
) -> list[dict[str, int | str]]:
    boxes: list[dict[str, int | str]] = []
    offset = start
    while offset < end:
        remaining = end - offset
        if remaining < 8:
            raise _BoxParseError(f"trailing {remaining} bytes at offset {offset}")
        handle.seek(offset)
        header = handle.read(8)
        if len(header) != 8:
            raise _BoxParseError(f"short box header at offset {offset}")
        size32, type_bytes = struct.unpack(">I4s", header)
        box_type = type_bytes.decode("latin-1")
        header_size = 8
        if size32 == 1:
            extended = handle.read(8)
            if len(extended) != 8:
                raise _BoxParseError(f"short extended header at offset {offset}")
            size = struct.unpack(">Q", extended)[0]
            header_size = 16
        elif size32 == 0:
            size = remaining
        else:
            size = size32
        if size < header_size:
            raise _BoxParseError(
                f"box {box_type!r} at {offset} has size {size} below header {header_size}"
            )
        box_end = offset + size
        if box_end > end:
            raise _BoxParseError(
                f"box {box_type!r} at {offset} ends at {box_end}, beyond {end}"
            )
        boxes.append(
            {
                "type": box_type,
                "offset": offset,
                "size": size,
                "header_size": header_size,
            }
        )
        offset = box_end
    return boxes


def _read_ftyp(handle: BinaryIO, box: dict[str, int | str]) -> dict[str, Any]:
    payload_size = int(box["size"]) - int(box["header_size"])
    if payload_size < 8 or (payload_size - 8) % 4 != 0:
        raise _BoxParseError("invalid ftyp payload", error_code="invalid_ftyp_box")
    handle.seek(int(box["offset"]) + int(box["header_size"]))
    fixed = handle.read(8)
    if len(fixed) != 8:
        raise _BoxParseError("short ftyp payload", error_code="invalid_ftyp_box")
    major_brand = fixed[:4].decode("latin-1")
    minor_version = struct.unpack(">I", fixed[4:])[0]
    compatible_brands = []
    for _ in range((payload_size - 8) // 4):
        brand = handle.read(4)
        if len(brand) != 4:
            raise _BoxParseError("short ftyp brand", error_code="invalid_ftyp_box")
        compatible_brands.append(brand.decode("latin-1"))
    return {
        "major_brand": major_brand,
        "minor_version": minor_version,
        "compatible_brands": compatible_brands,
    }


def _read_mvhd_from_moov(
    handle: BinaryIO,
    moov: dict[str, int | str],
) -> dict[str, int | float | None] | None:
    child_start = int(moov["offset"]) + int(moov["header_size"])
    child_end = int(moov["offset"]) + int(moov["size"])
    children = _parse_box_range(handle, start=child_start, end=child_end)
    mvhd = next((box for box in children if box["type"] == "mvhd"), None)
    if mvhd is None:
        return None
    payload_size = int(mvhd["size"]) - int(mvhd["header_size"])
    payload_start = int(mvhd["offset"]) + int(mvhd["header_size"])
    handle.seek(payload_start)
    version_and_flags = handle.read(4)
    if len(version_and_flags) != 4:
        raise _BoxParseError("short mvhd full-box header", error_code="invalid_mvhd_box")
    version = version_and_flags[0]
    if version == 0:
        if payload_size < 20:
            raise _BoxParseError("short version-0 mvhd", error_code="invalid_mvhd_box")
        fixed = handle.read(16)
        _, _, timescale, duration_units = struct.unpack(">IIII", fixed)
        unknown_duration = 0xFFFFFFFF
    elif version == 1:
        if payload_size < 32:
            raise _BoxParseError("short version-1 mvhd", error_code="invalid_mvhd_box")
        fixed = handle.read(28)
        _, _, timescale, duration_units = struct.unpack(">QQIQ", fixed)
        unknown_duration = 0xFFFFFFFFFFFFFFFF
    else:
        raise _BoxParseError(
            f"unsupported mvhd version {version}", error_code="invalid_mvhd_box"
        )
    if timescale == 0:
        raise _BoxParseError("mvhd timescale is zero", error_code="invalid_mvhd_box")
    duration_seconds = (
        None if duration_units == unknown_duration else duration_units / timescale
    )
    return {
        "timescale": timescale,
        "duration_units": duration_units,
        "duration_seconds": duration_seconds,
    }


def _is_yymm4_project_json(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            prefix = handle.read(4096)
        candidate = prefix.lstrip(b" \t\r\n")
        if candidate.startswith(b"\xef\xbb\xbf"):
            candidate = candidate[3:].lstrip(b" \t\r\n")
        if not candidate.startswith(b"{"):
            return False
        raw = path.read_bytes().lstrip(b" \t\r\n")
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:].lstrip(b" \t\r\n")
        payload = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False
    return isinstance(payload, dict) and all(
        key in payload for key in ("FilePath", "Timelines", "SelectedTimelineIndex")
    )


def _selected_stream(stream: dict[str, Any]) -> dict[str, Any]:
    tags = stream.get("tags")
    tags = tags if isinstance(tags, dict) else {}
    avg_rate = _string_or_none(stream.get("avg_frame_rate"))
    real_rate = _string_or_none(stream.get("r_frame_rate"))
    return {
        "index": _int_or_none(stream.get("index")),
        "codec_type": _string_or_none(stream.get("codec_type")),
        "codec_name": _string_or_none(stream.get("codec_name")),
        "codec_long_name": _string_or_none(stream.get("codec_long_name")),
        "profile": _string_or_none(stream.get("profile")),
        "codec_tag_string": _string_or_none(stream.get("codec_tag_string")),
        "width": _int_or_none(stream.get("width")),
        "height": _int_or_none(stream.get("height")),
        "pixel_format": _string_or_none(stream.get("pix_fmt")),
        "field_order": _string_or_none(stream.get("field_order")),
        "color_range": _string_or_none(stream.get("color_range")),
        "color_space": _string_or_none(stream.get("color_space")),
        "color_transfer": _string_or_none(stream.get("color_transfer")),
        "color_primaries": _string_or_none(stream.get("color_primaries")),
        "sample_aspect_ratio": _string_or_none(stream.get("sample_aspect_ratio")),
        "display_aspect_ratio": _string_or_none(stream.get("display_aspect_ratio")),
        "r_frame_rate": real_rate,
        "avg_frame_rate": avg_rate,
        "fps": _rate_to_float(avg_rate) or _rate_to_float(real_rate),
        "duration_seconds": _float_or_none(stream.get("duration")),
        "bit_rate_bps": _int_or_none(stream.get("bit_rate")),
        "frame_count": _int_or_none(stream.get("nb_frames")),
        "sample_rate_hz": _int_or_none(stream.get("sample_rate")),
        "channels": _int_or_none(stream.get("channels")),
        "channel_layout": _string_or_none(stream.get("channel_layout")),
        "encoder": _string_or_none(tags.get("encoder")),
    }


def _resolve_executable(executable: str | Path | None, default_name: str) -> str | None:
    if executable is not None:
        return str(executable)
    return shutil.which(default_name)


def _tool_version(executable: str, tool_name: str) -> str | None:
    try:
        completed = subprocess.run(
            [executable, "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    text = _decode_bytes(completed.stdout)
    match = re.search(
        rf"(?im)^{re.escape(tool_name)}\s+version\s+([^\s]+)",
        text,
    )
    return match.group(1) if match else None


def _sanitize_output(text: str, *, media_path: Path, executable: str) -> str:
    sanitized = text
    replacements = {
        str(media_path),
        str(media_path.resolve()),
        media_path.as_posix(),
        str(executable),
        Path(executable).as_posix(),
    }
    for value in sorted((item for item in replacements if item), key=len, reverse=True):
        sanitized = re.sub(re.escape(value), "<LOCAL_PATH>", sanitized, flags=re.IGNORECASE)
    return sanitized.strip()[-2000:]


def _exception_output(exc: BaseException) -> str:
    stderr = getattr(exc, "stderr", None)
    if stderr:
        return _decode_bytes(stderr)
    return str(exc)


def _decode_bytes(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    encodings = ["utf-8-sig", locale.getpreferredencoding(False), "cp932"]
    tried: set[str] = set()
    for encoding in encodings:
        normalized = encoding.casefold()
        if normalized in tried:
            continue
        tried.add(normalized)
        try:
            return value.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return value.decode("utf-8", errors="replace")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _string_or_none(value: Any) -> str | None:
    return str(value) if value is not None else None


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _rate_to_float(value: str | None) -> float | None:
    if not value:
        return None
    numerator, separator, denominator = value.partition("/")
    if not separator:
        return _float_or_none(value)
    try:
        denominator_value = float(denominator)
        if denominator_value == 0:
            return None
        return float(numerator) / denominator_value
    except ValueError:
        return None


def _split_brands(value: Any) -> list[str]:
    if value is None:
        return []
    text = str(value)
    if len(text) % 4 != 0:
        return [text]
    return [text[index : index + 4] for index in range(0, len(text), 4)]
