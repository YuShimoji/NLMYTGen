"""Prepare and validate the generic static Image/Text/subtitle YMM4 probe.

This module deliberately stops at H0 preparation.  It never launches YMM4 and
never renders media.  Runtime observations belong to the user-operated batch.
"""

from __future__ import annotations

import argparse
import binascii
import copy
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import struct
from typing import Any
import zlib

from src.pipeline.ymmp_openability import normalize_ymmp_openability
from src.pipeline.ymmp_patch import (
    _build_overlay_item,
    _get_timeline_items,
    _item_type,
    load_ymmp,
    save_ymmp,
)


PROBE_ID = "generic_static_image_text_subtitle_safe_area_v1"
REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_REL = Path("samples/visual_composition_lab/runtime_probe")
CARRIER_REL = Path("samples/Test_Template_00.ymmp")
PROJECT_REL = Path("local_outputs/generic_static_layout_probe.local.ymmp")
ASSET_REL = Path("local_outputs/assets/generic_probe_image.png")
RESULT_REL = Path("local_outputs/operator_result.json")
BATCH_STATE_REL = Path("local_outputs/operator_batch.local.json")
READBACK_NAME = "static_layout_probe_materialization_readback.json"
PREFLIGHT_REL = Path("operator_batch/preflight_readback.json")

EXPECTED_CARRIER_SHA256 = "9f89a982caba90cc4c241acaaa5c4df50d92c4a38d09270a04aeb3df4e09a524"
PNG_WIDTH = 640
PNG_HEIGHT = 360
LABEL = "PROBE LABEL"

IMAGE_BBOX = {"x_min": 160, "y_min": 180, "x_max": 800, "y_max": 540}
TEXT_BBOX = {"x_min": 1040, "y_min": 220, "x_max": 1450, "y_max": 300}
SUBTITLE_BBOX = {"x_min": 96, "y_min": 842, "x_max": 1824, "y_max": 1026}

OBSERVATION_KEYS = (
    "subtitle_readability_nonoverlap",
    "image_visibility_crop_anchor",
    "text_visibility_wrapping_anchor",
)
OBSERVATION_VALUES = {"pass", "fail", "uncertain"}


class ProbeError(ValueError):
    """Fail-closed preparation or collection error."""


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return _sha256_bytes(payload)


def _write_bytes_if_changed(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == payload:
        return
    path.write_bytes(payload)


def _write_json_if_changed(path: Path, value: Any) -> None:
    _write_bytes_if_changed(path, _json_bytes(value))


def _selected_timeline(project: dict[str, Any]) -> dict[str, Any]:
    timelines = project.get("Timelines")
    selected = project.get("SelectedTimelineIndex")
    if not isinstance(timelines, list) or len(timelines) != 1 or selected != 0:
        raise ProbeError("CARRIER_TIMELINE_CONTRACT_FAILED")
    timeline = timelines[0]
    if not isinstance(timeline, dict):
        raise ProbeError("CARRIER_TIMELINE_INVALID")
    return timeline


def _static_animation(value: int | float) -> dict[str, Any]:
    return {
        "Values": [{"Value": value}],
        "Span": 0.0,
        "AnimationType": "なし",
        "Bezier": {
            "Points": [
                {
                    "Point": {"X": 0.0, "Y": 0.0},
                    "ControlPoint1": {"X": -0.3, "Y": -0.3},
                    "ControlPoint2": {"X": 0.3, "Y": 0.3},
                },
                {
                    "Point": {"X": 1.0, "Y": 1.0},
                    "ControlPoint1": {"X": -0.3, "Y": -0.3},
                    "ControlPoint2": {"X": 0.3, "Y": 0.3},
                },
            ],
            "IsQuadratic": False,
        },
    }


def _build_image_item(*, asset_path: Path, frame: int, length: int, layer: int) -> dict[str, Any]:
    item = _build_overlay_item(
        {
            "path": str(asset_path.resolve()),
            "x": -480,
            "y": -180,
            "zoom": 100,
            "opacity": 100,
            "layer": layer,
            "group": 0,
        },
        frame=frame,
        length=length,
    )
    item.update(
        {
            "Z": _static_animation(0),
            "Rotation": _static_animation(0),
            "FadeIn": 0.0,
            "FadeOut": 0.0,
            "Blend": "Normal",
            "IsInverted": False,
            "IsClippingWithObjectAbove": False,
            "IsAlwaysOnTop": False,
            "IsZOrderEnabled": False,
            "VideoEffects": [],
            "KeyFrames": {"Frames": [], "Count": 0},
            "PlaybackRate": 100.0,
            "ContentOffset": "00:00:00",
            "Remark": "generic-static-layout-probe:image",
        }
    )
    return item


def _build_text_item(*, frame: int, length: int, layer: int) -> dict[str, Any]:
    return {
        "$type": "YukkuriMovieMaker.Project.Items.TextItem, YukkuriMovieMaker",
        "Text": LABEL,
        "Font": "Yu Gothic UI",
        "FontSize": _static_animation(34),
        "LineHeight2": _static_animation(100),
        "LetterSpacing2": _static_animation(0),
        "WordWrap": "NoWrap",
        "MaxWidth": _static_animation(410),
        "FontColor": "#FFFFFFFF",
        "Style": "Border",
        "StyleColor": "#FF20242A",
        "Bold": True,
        "Italic": False,
        "Underline": False,
        "Strikethrough": False,
        "X": _static_animation(80),
        "Y": _static_animation(-320),
        "Z": _static_animation(0),
        "Opacity": _static_animation(100),
        "Zoom": _static_animation(100),
        "Rotation": _static_animation(0),
        "FadeIn": 0.0,
        "FadeOut": 0.0,
        "Blend": "Normal",
        "IsInverted": False,
        "IsClippingWithObjectAbove": False,
        "IsAlwaysOnTop": False,
        "IsZOrderEnabled": False,
        "VideoEffects": [],
        "Group": 0,
        "Frame": frame,
        "Layer": layer,
        "KeyFrames": {"Frames": [], "Count": 0},
        "Length": length,
        "PlaybackRate": 100.0,
        "ContentOffset": "00:00:00",
        "Remark": "generic-static-layout-probe:text",
        "IsLocked": False,
        "IsHidden": False,
    }


def _png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)


def _neutral_png_bytes() -> bytes:
    """Return a deterministic opaque RGB abstract geometry image."""
    rows = bytearray()
    for y in range(PNG_HEIGHT):
        rows.append(0)
        for x in range(PNG_WIDTH):
            if x < 24 or x >= PNG_WIDTH - 24 or y < 24 or y >= PNG_HEIGHT - 24:
                rgb = (32, 38, 46)
            elif (x // 80 + y // 60) % 2 == 0:
                rgb = (74, 132, 156)
            else:
                rgb = (186, 148, 72)
            rows.extend(rgb)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", struct.pack(">IIBBBBB", PNG_WIDTH, PNG_HEIGHT, 8, 2, 0, 0, 0))
        + _png_chunk(b"IDAT", zlib.compress(bytes(rows), level=9))
        + _png_chunk(b"IEND", b"")
    )


def _animation_is_static(value: Any, expected: int | float | None = None) -> bool:
    if not isinstance(value, dict):
        return False
    values = value.get("Values")
    if not isinstance(values, list) or len(values) != 1 or not isinstance(values[0], dict):
        return False
    if float(value.get("Span", -1)) != 0.0 or value.get("AnimationType") != "なし":
        return False
    if expected is not None and float(values[0].get("Value")) != float(expected):
        return False
    return True


def _bbox_disjoint(left: dict[str, int], right: dict[str, int]) -> bool:
    return (
        left["x_max"] <= right["x_min"]
        or right["x_max"] <= left["x_min"]
        or left["y_max"] <= right["y_min"]
        or right["y_max"] <= left["y_min"]
    )


def _absolute_path_strings(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for child in value.values():
            found.extend(_absolute_path_strings(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_absolute_path_strings(child))
    elif isinstance(value, str) and (
        re.match(r"^[A-Za-z]:[\\/]", value) is not None or value.startswith("\\\\")
    ):
        found.append(value)
    return found


def _carrier_snapshot(carrier_path: Path) -> dict[str, Any]:
    payload = carrier_path.read_bytes()
    source_hash = _sha256_bytes(payload)
    if source_hash != EXPECTED_CARRIER_SHA256:
        raise ProbeError("CARRIER_HASH_MISMATCH")
    project = load_ymmp(carrier_path)
    timeline = _selected_timeline(project)
    items = _get_timeline_items(project)
    voices = [item for item in items if _item_type(item) == "VoiceItem"]
    if not voices:
        raise ProbeError("CARRIER_HAS_NO_VOICEITEM")
    for voice in voices:
        if int(voice.get("Length", 0)) <= 0:
            raise ProbeError("CARRIER_VOICE_TIMING_INVALID")
        if voice.get("JimakuVisibility") != "UseCharacterSetting":
            raise ProbeError("CARRIER_LINKED_SUBTITLE_POLICY_INVALID")
        serif = voice.get("Serif")
        if not isinstance(serif, str) or not serif.strip() or "\ufffd" in serif:
            raise ProbeError("CARRIER_SUBTITLE_TEXT_INVALID")
    characters = project.get("Characters")
    if not isinstance(characters, list) or not characters:
        raise ProbeError("CARRIER_CHARACTERS_INVALID")
    character_by_name = {
        character.get("Name"): character
        for character in characters
        if isinstance(character, dict)
    }
    if not all(
        character_by_name.get(voice.get("CharacterName"), {}).get("IsJimakuVisible") is True
        for voice in voices
    ):
        raise ProbeError("CARRIER_LINKED_SUBTITLE_NOT_VISIBLE")
    video_info = timeline.get("VideoInfo")
    if not isinstance(video_info, dict):
        raise ProbeError("CARRIER_VIDEO_INFO_INVALID")
    linked_characters = [character_by_name[voice.get("CharacterName")] for voice in voices]
    if not all(
        _animation_is_static(character.get("X"))
        and _animation_is_static(character.get("Y"))
        and _animation_is_static(character.get("FontSize"))
        and _animation_is_static(character.get("MaxWidth"))
        and float(character.get("JimakuFadeIn", -1)) == 0.0
        and float(character.get("JimakuFadeOut", -1)) == 0.0
        and character.get("JimakuVideoEffects") == []
        for character in linked_characters
    ):
        raise ProbeError("CARRIER_LINKED_SUBTITLE_NOT_STATIC")
    linked_character = linked_characters[0]
    subtitle_profile = {
        "stored_x": float(linked_character["X"]["Values"][0]["Value"]),
        "stored_y": float(linked_character["Y"]["Values"][0]["Value"]),
        "font_size": float(linked_character["FontSize"]["Values"][0]["Value"]),
        "max_width": float(linked_character["MaxWidth"]["Values"][0]["Value"]),
        "word_wrap": str(linked_character.get("WordWrap")),
        "base_point": str(linked_character.get("BasePoint")),
        "fade_in": float(linked_character.get("JimakuFadeIn", 0)),
        "fade_out": float(linked_character.get("JimakuFadeOut", 0)),
        "video_effect_count": len(linked_character.get("JimakuVideoEffects", [])),
    }
    return {
        "payload": payload,
        "hash": source_hash,
        "project": project,
        "timeline": timeline,
        "voices": voices,
        "voice_digests": [_canonical_digest(voice) for voice in voices],
        "character_digests": [_canonical_digest(character) for character in characters],
        "width": int(video_info.get("Width", 0)),
        "height": int(video_info.get("Height", 0)),
        "fps": float(video_info.get("FPS", 0)),
        "source_item_count": len(items),
        "subtitle_profile": subtitle_profile,
    }


def _normalized_project_digest(project: dict[str, Any]) -> str:
    normalized = copy.deepcopy(project)
    normalized["FilePath"] = "<IGNORED_LOCAL_PROJECT>"
    for item in _get_timeline_items(normalized):
        if _item_type(item) == "ImageItem":
            item["FilePath"] = "<IGNORED_LOCAL_ASSET>"
    return _canonical_digest(normalized)


def _inspect_materialized(
    *,
    project_path: Path,
    asset_path: Path,
    carrier_path: Path,
) -> dict[str, Any]:
    carrier = _carrier_snapshot(carrier_path)
    project = load_ymmp(project_path)
    normalize_ymmp_openability(project)
    timeline = _selected_timeline(project)
    items = _get_timeline_items(project)
    type_counts = Counter(_item_type(item) for item in items)
    voices = [item for item in items if _item_type(item) == "VoiceItem"]
    images = [item for item in items if _item_type(item) == "ImageItem"]
    texts = [item for item in items if _item_type(item) == "TextItem"]
    allowed = {"VoiceItem", "ImageItem", "TextItem"}

    start = min(int(voice.get("Frame", 0)) for voice in carrier["voices"])
    end = max(int(voice.get("Frame", 0)) + int(voice.get("Length", 0)) for voice in carrier["voices"])
    span = end - start
    expected_image_layer = max(int(voice.get("Layer", 0)) for voice in carrier["voices"]) + 1
    expected_text_layer = expected_image_layer + 1

    checks = {
        "one_selected_timeline": project.get("SelectedTimelineIndex") == 0 and len(project.get("Timelines", [])) == 1,
        "voice_count_preserved": len(voices) == len(carrier["voices"]),
        "voice_objects_unchanged": [_canonical_digest(voice) for voice in voices] == carrier["voice_digests"],
        "voice_order_unchanged": [_canonical_digest(voice) for voice in voices] == carrier["voice_digests"],
        "character_objects_unchanged": [_canonical_digest(character) for character in project.get("Characters", [])] == carrier["character_digests"],
        "linked_subtitle_transport_preserved": all(voice.get("JimakuVisibility") == "UseCharacterSetting" for voice in voices),
        "linked_subtitle_settings_static": carrier["subtitle_profile"]["fade_in"] == 0.0
        and carrier["subtitle_profile"]["fade_out"] == 0.0
        and carrier["subtitle_profile"]["video_effect_count"] == 0,
        "linked_subtitle_reserve_contains_baseline": SUBTITLE_BBOX["y_min"]
        <= (carrier["height"] / 2 + carrier["subtitle_profile"]["stored_y"])
        <= SUBTITLE_BBOX["y_max"],
        "exactly_one_imageitem": len(images) == 1,
        "exactly_one_independent_textitem": len(texts) == 1 and "CharacterName" not in texts[0] if texts else False,
        "item_families_exact": set(type_counts) == allowed,
        "timing_matches_voice_span": all(
            int(item.get("Frame", -1)) == start and int(item.get("Length", -1)) == span
            for item in images + texts
        ),
        "layers_distinct_above_voice": (
            len(images) == 1
            and len(texts) == 1
            and int(images[0].get("Layer", -1)) == expected_image_layer
            and int(texts[0].get("Layer", -1)) == expected_text_layer
        ),
        "max_layer_matches": int(timeline.get("MaxLayer", -1)) == expected_text_layer,
        "asset_path_matches": len(images) == 1 and Path(str(images[0].get("FilePath", ""))).resolve() == asset_path.resolve(),
        "project_path_matches": Path(str(project.get("FilePath", ""))).resolve() == project_path.resolve(),
        "allowed_absolute_paths_only": set(_absolute_path_strings(project))
        == {str(project_path.resolve()), str(asset_path.resolve())},
        "zone_contract_nonoverlap": (
            _bbox_disjoint(IMAGE_BBOX, TEXT_BBOX)
            and _bbox_disjoint(IMAGE_BBOX, SUBTITLE_BBOX)
            and _bbox_disjoint(TEXT_BBOX, SUBTITLE_BBOX)
        ),
        "no_render_output": not any(
            path.suffix.lower() in {".mp4", ".mov", ".avi", ".webm"}
            for path in project_path.parent.rglob("*")
            if path.is_file()
        ),
    }
    if images and texts:
        static_items = images + texts
        checks["static_positions_only"] = all(
            _animation_is_static(item.get(axis)) for item in static_items for axis in ("X", "Y")
        )
        checks["default_serializer_transform_fields_only"] = all(
            _animation_is_static(item.get("Opacity"), 100)
            and _animation_is_static(item.get("Zoom"), 100)
            and _animation_is_static(item.get("Rotation"), 0)
            for item in static_items
        )
        checks["no_fade_effect_or_keyframes"] = all(
            float(item.get("FadeIn", 0)) == 0.0
            and float(item.get("FadeOut", 0)) == 0.0
            and item.get("VideoEffects", []) == []
            and item.get("KeyFrames", {}).get("Frames", []) == []
            and int(item.get("KeyFrames", {}).get("Count", 0)) == 0
            for item in static_items
        )
        checks["no_transition_or_shape_fields"] = all(
            "transition" not in json.dumps(item, ensure_ascii=False).lower()
            and "shapeitem" not in json.dumps(item, ensure_ascii=False).lower()
            for item in static_items
        )
    else:
        checks["static_positions_only"] = False
        checks["default_serializer_transform_fields_only"] = False
        checks["no_fade_effect_or_keyframes"] = False
        checks["no_transition_or_shape_fields"] = False

    png_header = asset_path.read_bytes()[:26] if asset_path.exists() else b""
    checks["deterministic_opaque_rgb_asset"] = (
        len(png_header) >= 26
        and png_header[:8] == b"\x89PNG\r\n\x1a\n"
        and struct.unpack(">II", png_header[16:24]) == (PNG_WIDTH, PNG_HEIGHT)
        and png_header[25] == 2
    )
    checks["source_bytes_unchanged"] = _sha256_file(carrier_path) == carrier["hash"]
    if not all(checks.values()):
        failed = ",".join(key for key, passed in checks.items() if not passed)
        raise ProbeError(f"MATERIALIZATION_CHECK_FAILED:{failed}")

    return {
        "schema_version": 1,
        "probe_id": PROBE_ID,
        "evidence_grade": "verified_structure_C2_only",
        "carrier": {
            "sha256": carrier["hash"],
            "byte_count": len(carrier["payload"]),
            "source_item_count": carrier["source_item_count"],
            "voiceitem_count": len(carrier["voices"]),
            "timeline_count": 1,
            "width": carrier["width"],
            "height": carrier["height"],
            "fps": carrier["fps"],
            "limitation": "neutral_sample_voice_subtitle_transport_only",
            "linked_subtitle_profile": carrier["subtitle_profile"],
        },
        "materialized": {
            "project_path_policy": "ignored_repo_relative_target",
            "asset_path_policy": "ignored_repo_relative_target",
            "frame": start,
            "length_frames": span,
            "item_type_counts": dict(sorted(type_counts.items())),
            "image_layer": expected_image_layer,
            "text_layer": expected_text_layer,
            "normalized_project_sha256": _normalized_project_digest(project),
            "asset_sha256": _sha256_file(asset_path),
            "asset": {"format": "png", "width": PNG_WIDTH, "height": PNG_HEIGHT, "color_mode": "opaque_rgb"},
        },
        "layout_contract": {
            "coordinate_system": "top_left_canvas_pixels_1920x1080",
            "image_bbox": IMAGE_BBOX,
            "text_bbox_conservative": TEXT_BBOX,
            "linked_subtitle_reserve": SUBTITLE_BBOX,
        },
        "checks": checks,
        "observation_status": {
            "subtitle_readability_nonoverlap": "unverified_H1",
            "image_visibility_crop_anchor": "unverified_H1",
            "text_visibility_wrapping_anchor": "unverified_H1",
        },
        "runtime_capability_proven": False,
        "capability_regraded": False,
    }


def materialize_probe(
    *,
    repo_root: Path = REPO_ROOT,
    carrier_path: Path | None = None,
    package_dir: Path | None = None,
) -> dict[str, Any]:
    package = (package_dir or repo_root / PACKAGE_REL).resolve()
    carrier_file = (carrier_path or repo_root / CARRIER_REL).resolve()
    project_path = package / PROJECT_REL
    asset_path = package / ASSET_REL
    if carrier_file == project_path.resolve():
        raise ProbeError("CARRIER_AND_OUTPUT_MUST_DIFFER")

    carrier = _carrier_snapshot(carrier_file)
    source_before = carrier["payload"]
    source_project = carrier["project"]
    source_timeline = carrier["timeline"]
    voices = copy.deepcopy(carrier["voices"])
    start = min(int(voice.get("Frame", 0)) for voice in voices)
    end = max(int(voice.get("Frame", 0)) + int(voice.get("Length", 0)) for voice in voices)
    span = end - start
    image_layer = max(int(voice.get("Layer", 0)) for voice in voices) + 1
    text_layer = image_layer + 1

    _write_bytes_if_changed(asset_path, _neutral_png_bytes())
    timeline = {
        key: copy.deepcopy(source_timeline[key])
        for key in ("ID", "Name", "VideoInfo", "VerticalLine", "LayerSettings")
        if key in source_timeline
    }
    timeline.update(
        {
            "Items": voices
            + [
                _build_image_item(asset_path=asset_path, frame=start, length=span, layer=image_layer),
                _build_text_item(frame=start, length=span, layer=text_layer),
            ],
            "CurrentFrame": start,
            "Length": max(end, 1),
            "MaxLayer": text_layer,
        }
    )
    project = {
        "FilePath": str(project_path.resolve()),
        "SelectedTimelineIndex": 0,
        "Timelines": [timeline],
        "Characters": copy.deepcopy(source_project.get("Characters", [])),
        "CollapsedGroups": [],
        "LayoutXml": "",
        "ToolStates": {},
    }
    normalize_ymmp_openability(project)
    project_path.parent.mkdir(parents=True, exist_ok=True)
    existing = project_path.read_bytes() if project_path.exists() else None
    save_ymmp(project, project_path)
    if existing is not None and existing == project_path.read_bytes():
        pass
    if carrier_file.read_bytes() != source_before:
        raise ProbeError("SOURCE_CARRIER_WAS_MODIFIED")

    readback = _inspect_materialized(
        project_path=project_path,
        asset_path=asset_path,
        carrier_path=carrier_file,
    )
    _write_json_if_changed(package / READBACK_NAME, readback)
    return readback


def preflight_probe(
    *,
    repo_root: Path = REPO_ROOT,
    carrier_path: Path | None = None,
    package_dir: Path | None = None,
) -> dict[str, Any]:
    package = (package_dir or repo_root / PACKAGE_REL).resolve()
    carrier_file = (carrier_path or repo_root / CARRIER_REL).resolve()
    readback = _inspect_materialized(
        project_path=package / PROJECT_REL,
        asset_path=package / ASSET_REL,
        carrier_path=carrier_file,
    )
    expected = json.loads((package / READBACK_NAME).read_text(encoding="utf-8"))
    if expected != readback:
        raise ProbeError("TRACKED_MATERIALIZATION_READBACK_MISMATCH")
    receipt = {
        "schema_version": 1,
        "probe_id": PROBE_ID,
        "result": "pass",
        "launch_count": 0,
        "mode": "structural_preflight_only",
        "project_parse": "pass",
        "normalized_project_sha256": readback["materialized"]["normalized_project_sha256"],
        "asset_sha256": readback["materialized"]["asset_sha256"],
        "source_carrier_sha256": readback["carrier"]["sha256"],
        "checks": readback["checks"],
        "runtime_observation": "not_performed",
        "runtime_capability_proven": False,
    }
    _write_json_if_changed(package / PREFLIGHT_REL, receipt)
    return receipt


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _require_ignored_local_target(path: Path, package: Path, *, suffix: str) -> Path:
    resolved = path.resolve()
    local_root = (package / "local_outputs").resolve()
    try:
        resolved.relative_to(local_root)
    except ValueError as exc:
        raise ProbeError("OUTPUT_MUST_BE_UNDER_IGNORED_LOCAL_OUTPUTS") from exc
    if resolved.suffix.lower() != suffix:
        raise ProbeError("OUTPUT_SUFFIX_INVALID")
    return resolved


def start_operator_batch(
    *,
    state_path: Path,
    repo_root: Path = REPO_ROOT,
    package_dir: Path | None = None,
) -> dict[str, Any]:
    package = (package_dir or repo_root / PACKAGE_REL).resolve()
    state_path = _require_ignored_local_target(state_path, package, suffix=".json")
    project_path = package / PROJECT_REL
    result_path = package / RESULT_REL
    if state_path.exists():
        raise ProbeError("BATCH_STATE_ALREADY_EXISTS_ARCHIVE_FIRST")
    if result_path.exists():
        raise ProbeError("OPERATOR_RESULT_ALREADY_EXISTS_ARCHIVE_FIRST")
    preflight_probe(repo_root=repo_root, package_dir=package)
    stat = project_path.stat()
    state = {
        "schema_version": 1,
        "probe_id": PROBE_ID,
        "started_at": _utc_now(),
        "project_path": str(project_path.resolve()),
        "project_sha256": _sha256_file(project_path),
        "project_size": stat.st_size,
        "project_mtime_ns": stat.st_mtime_ns,
        "result_path": str(result_path.resolve()),
        "expected_observation_keys": list(OBSERVATION_KEYS),
        "no_save_required": True,
        "render_required": False,
    }
    _write_json_if_changed(state_path, state)
    return state


def _read_observations(path: Path) -> dict[str, str]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value.get("collector_validation_fixture"), dict):
        value = value["collector_validation_fixture"]
    observations = value.get("observations") if isinstance(value, dict) else None
    if not isinstance(observations, dict) or set(observations) != set(OBSERVATION_KEYS):
        raise ProbeError("OBSERVATION_KEYS_INVALID")
    normalized = {key: str(observations[key]).lower() for key in OBSERVATION_KEYS}
    if any(answer not in OBSERVATION_VALUES for answer in normalized.values()):
        raise ProbeError("OBSERVATION_VALUE_INVALID")
    return normalized


def collect_operator_result(
    *,
    state_path: Path,
    observations_path: Path,
    output_path: Path,
    fixture_mode: bool = False,
    repo_root: Path = REPO_ROOT,
    package_dir: Path | None = None,
) -> dict[str, Any]:
    package = (package_dir or repo_root / PACKAGE_REL).resolve()
    state_path = _require_ignored_local_target(state_path, package, suffix=".json")
    output_path = _require_ignored_local_target(output_path, package, suffix=".json")
    project_path = package / PROJECT_REL
    if output_path.exists():
        raise ProbeError("OPERATOR_RESULT_ALREADY_EXISTS_ARCHIVE_FIRST")
    if fixture_mode:
        stat = project_path.stat()
        state = {
            "probe_id": PROBE_ID,
            "project_path": str(project_path.resolve()),
            "project_sha256": _sha256_file(project_path),
            "project_size": stat.st_size,
            "project_mtime_ns": stat.st_mtime_ns,
        }
    else:
        if not state_path.exists():
            raise ProbeError("BATCH_STATE_MISSING")
        state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("probe_id") != PROBE_ID or Path(str(state.get("project_path", ""))).resolve() != project_path.resolve():
        raise ProbeError("BATCH_STATE_PROJECT_MISMATCH")
    stat = project_path.stat()
    if (
        _sha256_file(project_path) != state.get("project_sha256")
        or stat.st_size != int(state.get("project_size", -1))
        or stat.st_mtime_ns != int(state.get("project_mtime_ns", -1))
    ):
        raise ProbeError("PREPARED_PROJECT_CHANGED_DURING_BATCH")

    preflight = preflight_probe(repo_root=repo_root, package_dir=package)
    observations = _read_observations(observations_path)
    if fixture_mode:
        status = "fixture_validation_pass"
        observation_grade = "synthetic_validation_only_not_observed"
    elif all(answer == "pass" for answer in observations.values()):
        status = "pass"
        observation_grade = "observed_by_operator"
    elif any(answer == "fail" for answer in observations.values()):
        status = "fail"
        observation_grade = "observed_by_operator"
    else:
        status = "uncertain"
        observation_grade = "observed_by_operator"
    result = {
        "schema_version": 1,
        "probe_id": PROBE_ID,
        "status": status,
        "collected_at": _utc_now(),
        "fixture_mode": fixture_mode,
        "structural_facts": {
            "evidence_grade": "verified",
            "project_hash_unchanged_during_batch": True,
            "exactly_one_imageitem": preflight["checks"]["exactly_one_imageitem"],
            "exactly_one_independent_textitem": preflight["checks"]["exactly_one_independent_textitem"],
            "voice_objects_unchanged": preflight["checks"]["voice_objects_unchanged"],
            "excluded_behavior_absent": (
                preflight["checks"]["static_positions_only"]
                and preflight["checks"]["default_serializer_transform_fields_only"]
                and preflight["checks"]["no_fade_effect_or_keyframes"]
                and preflight["checks"]["no_render_output"]
            ),
        },
        "operator_observations": {
            "evidence_grade": observation_grade,
            "values": observations,
        },
        "capability_regraded": False,
        "render_performed": False,
    }
    _write_json_if_changed(output_path, result)
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("materialize", "preflight"):
        child = subparsers.add_parser(command)
        child.add_argument("--repo-root", type=Path, default=REPO_ROOT)
        child.add_argument("--carrier", type=Path)
        child.add_argument("--package", type=Path)
    start = subparsers.add_parser("batch-start")
    start.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    start.add_argument("--package", type=Path)
    start.add_argument("--state", type=Path, required=True)
    collect = subparsers.add_parser("collect")
    collect.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    collect.add_argument("--package", type=Path)
    collect.add_argument("--state", type=Path, required=True)
    collect.add_argument("--observations", type=Path, required=True)
    collect.add_argument("--output", type=Path, required=True)
    collect.add_argument("--fixture-mode", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "materialize":
        materialize_probe(repo_root=args.repo_root, carrier_path=args.carrier, package_dir=args.package)
    elif args.command == "preflight":
        preflight_probe(repo_root=args.repo_root, carrier_path=args.carrier, package_dir=args.package)
    elif args.command == "batch-start":
        start_operator_batch(state_path=args.state, repo_root=args.repo_root, package_dir=args.package)
    elif args.command == "collect":
        collect_operator_result(
            state_path=args.state,
            observations_path=args.observations,
            output_path=args.output,
            fixture_mode=args.fixture_mode,
            repo_root=args.repo_root,
            package_dir=args.package,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
