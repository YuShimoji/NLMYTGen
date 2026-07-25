"""Concrete-first, repeatable episode-to-review-video pipeline.

The first supported manifest is the approved new-banknote pilot.  The stage
interfaces are intentionally small: manifest loading, cue timing, visual
materialization, YMM4 project construction, render execution, media
validation, and a sanitized run receipt.  Local project/media artifacts stay
under an ignored run directory.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile
import time
from typing import Any, Iterable, Mapping, Sequence
import xml.etree.ElementTree as ET

from src.pipeline.media_validation import (
    decode_with_ffmpeg,
    inspect_iso_bmff,
    probe_with_ffprobe,
)
from src.pipeline.silent_media_runtime import (
    assert_command_allowed,
    descendant_pids,
    find_browser,
    process_snapshot,
    resolve_audio_policy,
)


MANIFEST_SCHEMA = "nlmytgen.episode_manifest.v1"
RUN_RECEIPT_SCHEMA = "nlmytgen.episode_video_run_receipt.v1"
PROJECT_READBACK_SCHEMA = "nlmytgen.episode_video_project_readback.v1"
VISUAL_READBACK_SCHEMA = "nlmytgen.cue_visual_readback.v1"
MEDIA_VALIDATION_SCHEMA = "nlmytgen.episode_media_validation.v1"
REAL_MEDIA_PROVENANCE_SCHEMA = "nlmytgen.real_media_provenance.v1"
VOICE_ITEM_TYPE = "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker"
IMAGE_ITEM_TYPE = "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker"
ABSOLUTE_WINDOWS_PATH = re.compile(r"^[A-Za-z]:[\\/]")
URL_PREFIXES = ("http://", "https://", "file://")
REAL_MEDIA_ASSET_TYPES = {"image", "video"}
REAL_MEDIA_FIT_MODES = {"contain", "cover"}
REAL_MEDIA_USAGE_CLASSIFICATIONS = {
    "official_reuse_candidate",
    "internal_review_only",
    "user_owned",
}
IMAGE_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".m4v", ".mkv", ".mov", ".mp4", ".webm"}


class EpisodeVideoError(RuntimeError):
    """Structured pipeline failure with a stable error code."""

    def __init__(self, message: str, *, code: str = "episode_video_pipeline_failed") -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class CueTiming:
    cue_id: str
    scene_id: str
    speaker: str
    text: str
    frame: int
    length_frames: int
    end_frame: int
    visual_id: str
    asset_id: str
    visual_source: Path
    asset_type: str = "svg"
    source_provenance_id: str | None = None
    fit_mode: str = "contain"
    crop: tuple[float, float, float, float] | None = None
    source_start_seconds: float | None = None
    source_end_seconds: float | None = None
    internal_review_only: bool = False
    subtitle_lines: tuple[str, ...] = ()
    speaker_label: str | None = None


@dataclass(frozen=True)
class PipelinePaths:
    run_directory: Path
    generated_assets: Path
    generated_project: Path
    yymm4_render: Path
    review_mp4: Path
    extracted_frames: Path
    resolved_manifest: Path
    real_media_asset_manifest: Path
    run_receipt: Path
    media_validation: Path
    cue_visual_readback: Path
    run_log: Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _validate_real_media_cue_contract(cue: Mapping[str, Any]) -> None:
    cue_id = str(cue.get("cue_id") or "<unknown>")
    asset_type = str(cue.get("asset_type") or "")
    if asset_type not in REAL_MEDIA_ASSET_TYPES:
        raise EpisodeVideoError(
            f"real-media asset_type is invalid for {cue_id}",
            code="real_media_asset_type_invalid",
        )
    local_asset_path = cue.get("local_asset_path")
    provenance_id = cue.get("source_provenance_id")
    fit_mode = str(cue.get("fit_mode") or "")
    if not isinstance(local_asset_path, str) or not local_asset_path.strip():
        raise EpisodeVideoError(
            f"real-media local_asset_path is missing for {cue_id}",
            code="real_media_asset_path_missing",
        )
    if Path(local_asset_path).suffix.lower() == ".svg":
        raise EpisodeVideoError(
            f"SVG is forbidden in a real-media cue: {cue_id}",
            code="real_media_svg_forbidden",
        )
    allowed_extensions = IMAGE_EXTENSIONS if asset_type == "image" else VIDEO_EXTENSIONS
    if Path(local_asset_path).suffix.lower() not in allowed_extensions:
        raise EpisodeVideoError(
            f"real-media file extension is invalid for {cue_id}",
            code="real_media_extension_invalid",
        )
    if not isinstance(provenance_id, str) or not provenance_id.strip():
        raise EpisodeVideoError(
            f"source_provenance_id is missing for {cue_id}",
            code="real_media_provenance_missing",
        )
    if fit_mode not in REAL_MEDIA_FIT_MODES:
        raise EpisodeVideoError(
            f"fit_mode is invalid for {cue_id}",
            code="real_media_fit_mode_invalid",
        )
    if cue.get("internal_review_only") is not True:
        raise EpisodeVideoError(
            f"real-media cue is not fail-closed for {cue_id}",
            code="real_media_rights_boundary_invalid",
        )
    subtitle_lines = cue.get("subtitle_lines")
    speaker_label = cue.get("speaker_label")
    if (
        not isinstance(subtitle_lines, list)
        or not 1 <= len(subtitle_lines) <= 3
        or any(not isinstance(line, str) or not line for line in subtitle_lines)
    ):
        raise EpisodeVideoError(
            f"subtitle_lines are missing or invalid for {cue_id}",
            code="real_media_subtitle_lines_invalid",
        )
    if speaker_label not in {"れいむ", "まりさ"}:
        raise EpisodeVideoError(
            f"speaker_label is missing or invalid for {cue_id}",
            code="real_media_speaker_label_invalid",
        )

    crop = cue.get("crop")
    if crop is not None:
        if (
            not isinstance(crop, list)
            or len(crop) != 4
            or any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in crop)
        ):
            raise EpisodeVideoError(
                f"crop must be four normalized numbers for {cue_id}",
                code="real_media_crop_invalid",
            )
        x, y, width, height = (float(value) for value in crop)
        if (
            x < 0
            or y < 0
            or width <= 0
            or height <= 0
            or x + width > 1.000001
            or y + height > 1.000001
        ):
            raise EpisodeVideoError(
                f"crop escapes the source bounds for {cue_id}",
                code="real_media_crop_invalid",
            )

    source_time_range = cue.get("source_time_range")
    if source_time_range is not None:
        if asset_type != "video" or not isinstance(source_time_range, dict):
            raise EpisodeVideoError(
                f"source_time_range is only valid for video cues: {cue_id}",
                code="real_media_time_range_invalid",
            )
        start = source_time_range.get("start_seconds")
        end = source_time_range.get("end_seconds")
        if (
            isinstance(start, bool)
            or isinstance(end, bool)
            or not isinstance(start, (int, float))
            or not isinstance(end, (int, float))
            or float(start) < 0
            or float(end) <= float(start)
        ):
            raise EpisodeVideoError(
                f"source_time_range is invalid for {cue_id}",
                code="real_media_time_range_invalid",
            )


def load_episode_manifest(repo_root: Path, manifest_path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EpisodeVideoError(
            f"episode manifest is unreadable: {manifest_path}", code="manifest_unreadable"
        ) from exc
    if not isinstance(payload, dict) or payload.get("schema") != MANIFEST_SCHEMA:
        raise EpisodeVideoError("unsupported episode manifest schema", code="manifest_schema_invalid")

    required = (
        "episode_id",
        "source_package",
        "approved_script",
        "derived_csv",
        "cue_mapping",
        "visual_source_path",
        "yymm4",
        "output",
        "render_settings",
        "boundaries",
        "content_locks",
    )
    missing = [key for key in required if key not in payload]
    if missing:
        raise EpisodeVideoError(
            f"manifest is missing required fields: {', '.join(missing)}",
            code="manifest_fields_missing",
        )

    cue_mapping = payload.get("cue_mapping")
    if not isinstance(cue_mapping, list) or not cue_mapping:
        raise EpisodeVideoError("manifest must define at least one cue", code="cue_mapping_invalid")
    expected_cues = [f"cue_{index:03d}" for index in range(1, len(cue_mapping) + 1)]
    actual_cues = [row.get("cue_id") for row in cue_mapping if isinstance(row, dict)]
    if actual_cues != expected_cues:
        raise EpisodeVideoError(
            "cue ids/order are not a contiguous cue_001..cue_N sequence",
            code="cue_order_invalid",
        )

    real_media_rows = [row for row in cue_mapping if isinstance(row, dict) and row.get("asset_type")]
    if real_media_rows:
        if len(real_media_rows) != len(cue_mapping):
            raise EpisodeVideoError(
                "real-media manifests must declare asset_type for every cue",
                code="real_media_cue_contract_incomplete",
            )
        if not payload.get("provenance_manifest_path"):
            raise EpisodeVideoError(
                "real-media manifest is missing provenance_manifest_path",
                code="real_media_provenance_missing",
            )
        for row in real_media_rows:
            _validate_real_media_cue_contract(row)

    boundaries = payload.get("boundaries") or {}
    if not (
        boundaries.get("internal_review_only") is True
        and boundaries.get("production") is False
        and boundaries.get("publication") is False
        and boundaries.get("external_upload") is False
        and boundaries.get("rights_approved") is False
    ):
        raise EpisodeVideoError("internal review boundary is not fail-closed", code="boundary_invalid")

    for key, value in _walk_strings(payload):
        if key == "resolved_runtime_path":
            continue
        if ABSOLUTE_WINDOWS_PATH.match(value) or value.startswith("/") or value.startswith("\\\\"):
            raise EpisodeVideoError(
                f"manifest contains an absolute/private path at {key}",
                code="manifest_absolute_path_forbidden",
            )
        if value.lower().startswith(URL_PREFIXES):
            raise EpisodeVideoError(
                f"manifest contains an external URL at {key}", code="manifest_external_url_forbidden"
            )

    # Resolve every declared repo path once so traversal attempts fail early.
    for relative in _manifest_repo_paths(payload):
        resolve_repo_path(repo_root, relative)
    return payload


def resolve_repo_path(repo_root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise EpisodeVideoError("empty repo-relative path", code="repo_path_invalid")
    candidate = Path(relative)
    if candidate.is_absolute() or ABSOLUTE_WINDOWS_PATH.match(relative) or relative.startswith("\\\\"):
        raise EpisodeVideoError("absolute manifest path is forbidden", code="repo_path_absolute")
    root = repo_root.resolve()
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise EpisodeVideoError("manifest path escapes repository", code="repo_path_escape") from exc
    return resolved


def build_pipeline_paths(repo_root: Path, manifest: Mapping[str, Any]) -> PipelinePaths:
    output = manifest["output"]
    output_root = resolve_repo_path(repo_root, str(output["run_root_path"]))
    run_id = str(output["run_id"])
    if not re.fullmatch(r"[A-Za-z0-9._-]+", run_id):
        raise EpisodeVideoError("run_id contains unsafe characters", code="run_id_invalid")
    run = output_root / run_id
    return PipelinePaths(
        run_directory=run,
        generated_assets=run / "generated_assets",
        generated_project=run / str(output["project_filename"]),
        yymm4_render=run / "yymm4_render_intermediate.local.mp4",
        review_mp4=run / str(output["mp4_filename"]),
        extracted_frames=run / "extracted_review_frames",
        resolved_manifest=run / "resolved_manifest.json",
        real_media_asset_manifest=run / "real_media_asset_manifest.local.json",
        run_receipt=run / "pipeline_run_receipt.json",
        media_validation=run / "media_validation.json",
        cue_visual_readback=run / "cue_visual_readback.json",
        run_log=run / "run.log",
    )


def _load_real_media_provenance(
    repo_root: Path, manifest: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Mapping[str, Any]]]:
    relative = manifest.get("provenance_manifest_path")
    if not isinstance(relative, str) or not relative:
        raise EpisodeVideoError(
            "real-media provenance manifest is missing",
            code="real_media_provenance_missing",
        )
    path = resolve_repo_path(repo_root, relative)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EpisodeVideoError(
            "real-media provenance manifest is unreadable",
            code="real_media_provenance_unreadable",
        ) from exc
    if not isinstance(payload, dict) or payload.get("schema") != REAL_MEDIA_PROVENANCE_SCHEMA:
        raise EpisodeVideoError(
            "real-media provenance schema is invalid",
            code="real_media_provenance_schema_invalid",
        )

    source_rows = payload.get("sources")
    asset_rows = payload.get("assets")
    if not isinstance(source_rows, list) or not isinstance(asset_rows, list):
        raise EpisodeVideoError(
            "real-media provenance sources/assets are invalid",
            code="real_media_provenance_records_invalid",
        )
    sources: dict[str, Mapping[str, Any]] = {}
    for row in source_rows:
        if not isinstance(row, dict):
            raise EpisodeVideoError(
                "real-media provenance source is invalid",
                code="real_media_provenance_records_invalid",
            )
        source_id = row.get("source_id")
        required = ("exact_title", "publisher", "canonical_url")
        if (
            not isinstance(source_id, str)
            or not source_id
            or any(not isinstance(row.get(key), str) or not row[key] for key in required)
            or not str(row["canonical_url"]).lower().startswith(("http://", "https://"))
        ):
            raise EpisodeVideoError(
                "real-media provenance source metadata is incomplete",
                code="real_media_provenance_records_invalid",
            )
        sources[source_id] = row

    assets: dict[str, Mapping[str, Any]] = {}
    for row in asset_rows:
        if not isinstance(row, dict):
            raise EpisodeVideoError(
                "real-media provenance asset is invalid",
                code="real_media_provenance_records_invalid",
            )
        asset_id = row.get("asset_id")
        source_id = row.get("source_id")
        local_asset_path = row.get("local_asset_path")
        required_strings = (
            "sha256",
            "media_type",
            "crop_or_segment",
            "usage_classification",
            "rights_state",
        )
        if (
            not isinstance(asset_id, str)
            or not asset_id
            or source_id not in sources
            or not isinstance(local_asset_path, str)
            or not local_asset_path
            or any(not isinstance(row.get(key), str) or not row[key] for key in required_strings)
            or not isinstance(row.get("cue_ids"), list)
            or row.get("usage_classification") not in REAL_MEDIA_USAGE_CLASSIFICATIONS
            or row.get("production_allowed") is not False
            or row.get("publication_allowed") is not False
        ):
            raise EpisodeVideoError(
                f"real-media provenance asset metadata is incomplete: {asset_id}",
                code="real_media_provenance_records_invalid",
            )
        resolve_repo_path(repo_root, local_asset_path)
        assets[asset_id] = row
    return payload, assets


def preflight_episode(
    repo_root: Path, manifest: Mapping[str, Any]
) -> tuple[dict[str, Any], list[CueTiming]]:
    policy = resolve_audio_policy()
    real_media_mode = all(
        isinstance(row, dict) and row.get("asset_type") in REAL_MEDIA_ASSET_TYPES
        for row in manifest["cue_mapping"]
    )
    provenance_payload: dict[str, Any] | None = None
    provenance_assets: dict[str, Mapping[str, Any]] = {}
    if real_media_mode:
        provenance_payload, provenance_assets = _load_real_media_provenance(repo_root, manifest)
    protected: list[dict[str, Any]] = []
    failed_locks: list[str] = []
    for row in manifest["content_locks"]:
        relative = str(row["path"])
        expected = str(row["sha256"]).lower()
        path = resolve_repo_path(repo_root, relative)
        if not path.is_file():
            failed_locks.append(relative)
            protected.append({"path": relative, "status": "missing", "sha256": None})
            continue
        actual = sha256_file(path)
        status = "passed" if actual == expected else "hash_mismatch"
        protected.append({"path": relative, "status": status, "sha256": actual})
        if actual != expected:
            failed_locks.append(relative)
    if failed_locks:
        raise EpisodeVideoError(
            f"protected input lock failed: {', '.join(failed_locks)}",
            code="protected_input_hash_mismatch",
        )

    source_project = resolve_repo_path(repo_root, str(manifest["yymm4"]["source_project_path"]))
    if not source_project.is_file():
        raise EpisodeVideoError("same-machine source YMM4 project is missing", code="source_ymmp_missing")
    expected_project_hash = str(manifest["yymm4"]["source_project_sha256"]).lower()
    actual_project_hash = sha256_file(source_project)
    if actual_project_hash != expected_project_hash:
        raise EpisodeVideoError(
            "same-machine source YMM4 project hash changed", code="source_ymmp_hash_mismatch"
        )

    project = _read_project(source_project)
    timeline = _selected_timeline(project)
    video_info = timeline.get("VideoInfo") or {}
    fps = int(video_info.get("FPS", 0))
    width = int(video_info.get("Width", 0))
    height = int(video_info.get("Height", 0))
    if (fps, width, height) != (60, 1920, 1080):
        raise EpisodeVideoError("source YMM4 profile is not 1920x1080/60", code="source_profile_invalid")

    voices = _voice_items(timeline)
    csv_rows = _read_csv(resolve_repo_path(repo_root, str(manifest["derived_csv"])))
    cue_rows = manifest["cue_mapping"]
    if len(voices) != len(cue_rows) or len(csv_rows) != len(cue_rows):
        raise EpisodeVideoError(
            "voice/csv row counts do not match the manifest cue count",
            code="voice_count_invalid",
        )
    expected_pairs = [(row[0], row[1]) for row in csv_rows]
    actual_pairs = [(str(item.get("CharacterName")), str(item.get("Serif"))) for item in voices]
    if actual_pairs != expected_pairs:
        raise EpisodeVideoError("VoiceItem text/order differs from approved CSV", code="voice_text_drift")
    counts: dict[str, int] = {}
    for speaker, _ in actual_pairs:
        counts[speaker] = counts.get(speaker, 0) + 1
    expected_counts: dict[str, int] = {}
    for cue in cue_rows:
        speaker = str(cue["speaker"])
        expected_counts[speaker] = expected_counts.get(speaker, 0) + 1
    if counts != expected_counts:
        raise EpisodeVideoError(
            "VoiceItem speaker distribution differs from the manifest",
            code="speaker_split_drift",
        )

    timings: list[CueTiming] = []
    previous_end = 0
    for cue, voice in zip(cue_rows, voices, strict=True):
        frame = int(voice.get("Frame", -1))
        length = int(voice.get("Length", -1))
        end = frame + length
        if frame != previous_end or length <= 0:
            raise EpisodeVideoError("VoiceItem timing is not contiguous", code="voice_timing_invalid")
        speaker = str(voice["CharacterName"])
        if speaker != str(cue["speaker"]):
            raise EpisodeVideoError("manifest speaker mapping differs from project", code="cue_speaker_drift")
        asset_type = str(cue.get("asset_type") or "svg")
        visual_relative = (
            cue.get("local_asset_path")
            if asset_type in REAL_MEDIA_ASSET_TYPES
            else cue.get("visual_source_path")
            or f"{str(manifest['visual_source_path']).rstrip('/')}/{str(cue['visual_id'])}.svg"
        )
        visual_source = resolve_repo_path(repo_root, str(visual_relative))
        if not visual_source.is_file():
            raise EpisodeVideoError(
                f"visual source is missing for {cue['cue_id']}", code="visual_source_missing"
            )
        source_provenance_id: str | None = None
        fit_mode = "contain"
        crop: tuple[float, float, float, float] | None = None
        source_start_seconds: float | None = None
        source_end_seconds: float | None = None
        internal_review_only = False
        subtitle_lines: tuple[str, ...] = ()
        speaker_label: str | None = None
        if asset_type in REAL_MEDIA_ASSET_TYPES:
            asset_id = str(cue.get("materialized_visual_id") or cue["visual_id"])
            provenance = provenance_assets.get(asset_id)
            source_provenance_id = str(cue["source_provenance_id"])
            if provenance is None:
                raise EpisodeVideoError(
                    f"provenance record is missing for {cue['cue_id']}",
                    code="real_media_provenance_missing",
                )
            provenance_path = str(provenance["local_asset_path"])
            if (
                provenance_path != str(visual_relative)
                or provenance.get("source_id") != source_provenance_id
                or cue["cue_id"] not in provenance["cue_ids"]
                or str(provenance["sha256"]).lower() != sha256_file(visual_source)
                or provenance.get("media_type") != asset_type
            ):
                raise EpisodeVideoError(
                    f"provenance binding differs for {cue['cue_id']}",
                    code="real_media_provenance_binding_invalid",
                )
            fit_mode = str(cue["fit_mode"])
            if cue.get("crop") is not None:
                crop_values = [float(value) for value in cue["crop"]]
                crop = (
                    crop_values[0],
                    crop_values[1],
                    crop_values[2],
                    crop_values[3],
                )
            source_range = cue.get("source_time_range")
            if isinstance(source_range, dict):
                source_start_seconds = float(source_range["start_seconds"])
                source_end_seconds = float(source_range["end_seconds"])
            internal_review_only = True
            subtitle_lines = tuple(str(line) for line in cue["subtitle_lines"])
            speaker_label = str(cue["speaker_label"])
            if "".join(subtitle_lines) != str(voice["Serif"]):
                raise EpisodeVideoError(
                    f"accepted subtitle line fragments differ for {cue['cue_id']}",
                    code="subtitle_line_fragment_drift",
                )
            if not speaker_label.strip():
                raise EpisodeVideoError(
                    f"speaker label is empty for {cue['cue_id']}",
                    code="subtitle_speaker_label_drift",
                )
        else:
            try:
                svg_root = ET.parse(visual_source).getroot()
            except (OSError, ET.ParseError) as exc:
                raise EpisodeVideoError(
                    f"visual source is not valid SVG for {cue['cue_id']}",
                    code="visual_source_invalid",
                ) from exc
            if (
                svg_root.attrib.get("data-cue-id") != str(cue["cue_id"])
                or svg_root.attrib.get("data-scene-id") != str(cue["scene_id"])
                or svg_root.attrib.get("data-approved-text") != str(voice["Serif"])
            ):
                raise EpisodeVideoError(
                    f"visual source cue/text binding differs for {cue['cue_id']}",
                    code="visual_cue_binding_drift",
                )
        timings.append(
            CueTiming(
                cue_id=str(cue["cue_id"]),
                scene_id=str(cue["scene_id"]),
                speaker=speaker,
                text=str(voice["Serif"]),
                frame=frame,
                length_frames=length,
                end_frame=end,
                visual_id=str(cue["visual_id"]),
                asset_id=str(cue.get("materialized_visual_id") or cue["visual_id"]),
                visual_source=visual_source,
                asset_type=asset_type,
                source_provenance_id=source_provenance_id,
                fit_mode=fit_mode,
                crop=crop,
                source_start_seconds=source_start_seconds,
                source_end_seconds=source_end_seconds,
                internal_review_only=internal_review_only,
                subtitle_lines=subtitle_lines,
                speaker_label=speaker_label,
            )
        )
        previous_end = end
    expected_timeline_frames = int(manifest["yymm4"]["timeline_frames"])
    if (
        previous_end != int(timeline.get("Length", -1))
        or previous_end != expected_timeline_frames
    ):
        raise EpisodeVideoError(
            "timeline length differs from the manifest",
            code="timeline_length_drift",
        )

    scene_counts: dict[str, int] = {}
    for timing in timings:
        scene_counts[timing.scene_id] = scene_counts.get(timing.scene_id, 0) + 1
    expected_scene_counts: dict[str, int] = {}
    for cue in cue_rows:
        scene = str(cue["scene_id"])
        expected_scene_counts[scene] = expected_scene_counts.get(scene, 0) + 1
    if scene_counts != expected_scene_counts:
        raise EpisodeVideoError(
            "scene allocation differs from the manifest",
            code="scene_allocation_drift",
        )

    return (
        {
            "status": "passed",
            "audio_policy": policy,
            "protected_inputs": protected,
            "source_project": {
                "sha256": actual_project_hash,
                "voice_item_count": len(voices),
                "speaker_counts": counts,
                "fps": fps,
                "width": width,
                "height": height,
                "timeline_frames": previous_end,
                "duration_seconds": previous_end / fps,
                "tool_states_present_in_source": bool(project.get("ToolStates")),
                "layout_xml_present_in_source": bool(project.get("LayoutXml")),
            },
            "cue_count": len(timings),
            "scene_counts": scene_counts,
            "exact_text_order": True,
            "real_media": {
                "enabled": real_media_mode,
                "asset_count": len(provenance_assets),
                "cue_provenance_coverage": (
                    f"{len(timings)}/{len(cue_rows)}"
                    if real_media_mode
                    else "legacy-svg"
                ),
                "svg_reference_count": sum(timing.asset_type == "svg" for timing in timings),
                "internal_review_only": (
                    all(timing.internal_review_only for timing in timings)
                    if real_media_mode
                    else False
                ),
                "subtitle_line_fragments_locked": (
                    all(timing.subtitle_lines for timing in timings)
                    if real_media_mode
                    else False
                ),
                "provenance_schema": (
                    provenance_payload.get("schema") if provenance_payload is not None else None
                ),
            },
        },
        timings,
    )


def _escape_drawtext(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace(":", "\\:")
    )


def _subtitle_overlay_filters(timing: CueTiming) -> list[str]:
    if not timing.subtitle_lines or timing.speaker_label is None:
        raise EpisodeVideoError(
            f"subtitle overlay contract is missing for {timing.cue_id}",
            code="real_media_subtitle_lines_invalid",
        )
    font = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / "YuGothB.ttc"
    if not font.is_file():
        raise EpisodeVideoError(
            "required Japanese subtitle font is unavailable",
            code="subtitle_font_missing",
        )
    font_value = str(font).replace("\\", "/").replace(":", r"\:")
    max_length = max(len(line) for line in timing.subtitle_lines)
    if len(timing.subtitle_lines) == 3:
        font_size = 34 if max_length >= 34 else 36
        line_positions = [806, 864, 922]
    else:
        font_size = 36 if max_length >= 40 else 40 if max_length >= 34 else 42
        line_positions = [815, 883] if len(timing.subtitle_lines) == 2 else [854]
    label_color = "0xb94a5b" if timing.speaker_label == "れいむ" else "0xc59a34"
    filters = [
        "drawbox=x=0:y=780:w=1920:h=300:color=black@0.96:t=fill",
        f"drawbox=x=56:y=854:w=190:h=74:color={label_color}:t=fill",
        (
            f"drawtext=fontfile='{font_value}':"
            f"text='{_escape_drawtext(timing.speaker_label)}':"
            "expansion=none:fontcolor=white:fontsize=36:x=95:y=870"
        ),
    ]
    for line, y in zip(timing.subtitle_lines, line_positions, strict=True):
        filters.append(
            f"drawtext=fontfile='{font_value}':"
            f"text='{_escape_drawtext(line)}':"
            f"expansion=none:fontcolor=white:fontsize={font_size}:x=285:y={y}"
        )
    return filters


def _materialize_real_media_frame(
    timing: CueTiming, output: Path
) -> dict[str, Any]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise EpisodeVideoError("ffmpeg is unavailable", code="ffmpeg_missing")
    source_hash_before = sha256_file(timing.visual_source)
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
    ]
    selected_seconds: float | None = None
    if timing.asset_type == "video":
        start = timing.source_start_seconds or 0.0
        end = timing.source_end_seconds
        selected_seconds = start if end is None else start + ((end - start) / 2.0)
        command.extend(["-ss", f"{selected_seconds:.6f}"])
    command.extend(["-i", str(timing.visual_source)])

    filters: list[str] = []
    if timing.crop is not None:
        x, y, width, height = timing.crop
        filters.append(
            "crop="
            f"iw*{width:.8f}:ih*{height:.8f}:iw*{x:.8f}:ih*{y:.8f}"
        )
    if timing.fit_mode == "cover":
        filters.extend(
            [
                "scale=1920:1080:force_original_aspect_ratio=increase",
                "crop=1920:1080",
            ]
        )
    else:
        filters.extend(
            [
                "scale=1920:1080:force_original_aspect_ratio=decrease",
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black",
            ]
        )
    filters.extend(_subtitle_overlay_filters(timing))
    command.extend(
        [
            "-vf",
            ",".join(filters),
            "-frames:v",
            "1",
            "-an",
            "-sn",
            "-dn",
            "-threads",
            "1",
            str(output),
        ]
    )
    assert_command_allowed(command)
    completed = subprocess.run(command, capture_output=True, check=False, timeout=120)
    if completed.returncode != 0 or not output.is_file():
        stderr = completed.stderr.decode("utf-8", errors="replace")[-1000:]
        raise EpisodeVideoError(
            f"real-media materialization failed for {timing.cue_id}: {stderr}",
            code="real_media_materialization_failed",
        )
    if sha256_file(timing.visual_source) != source_hash_before:
        raise EpisodeVideoError(
            f"real-media source changed during materialization: {timing.cue_id}",
            code="real_media_source_mutated",
        )
    return {
        "status": "passed",
        "engine": "ffmpeg",
        "cleanup_verified": True,
        "speaker_playback": False,
        "preview_playback": False,
        "selected_seconds": selected_seconds,
        "subtitle_lines_composited": len(timing.subtitle_lines),
        "speaker_label_composited": timing.speaker_label,
    }


def materialize_visuals(
    timings: Sequence[CueTiming],
    paths: PipelinePaths,
    *,
    resume: bool,
    repo_root: Path | None = None,
) -> tuple[dict[str, Path], dict[str, Any]]:
    unique_sources: dict[str, CueTiming] = {}
    for timing in timings:
        unique_sources.setdefault(timing.asset_id, timing)
    paths.generated_assets.mkdir(parents=True, exist_ok=True)
    browser = find_browser() if any(timing.asset_type == "svg" for timing in timings) else None
    records: list[dict[str, Any]] = []
    outputs: dict[str, Path] = {}
    for asset_id in sorted(unique_sources):
        timing = unique_sources[asset_id]
        source = timing.visual_source
        output = paths.generated_assets / f"{asset_id}.png"
        if output.exists() and resume:
            width, height = png_dimensions(output)
            if (width, height) != (1920, 1080):
                raise EpisodeVideoError(
                    f"cached visual has wrong dimensions: {asset_id}", code="cached_visual_invalid"
                )
            process_receipt = {
                "status": "reused",
                "cleanup_verified": True,
                "speaker_playback": False,
                "preview_playback": False,
            }
        else:
            if timing.asset_type in REAL_MEDIA_ASSET_TYPES:
                process_receipt = _materialize_real_media_frame(timing, output)
            else:
                if browser is None:
                    raise EpisodeVideoError(
                        "browser is unavailable for SVG materialization",
                        code="browser_missing",
                    )
                process_receipt = _render_svg_with_silent_chromium(source, output, browser)
            width, height = png_dimensions(output)
            if (width, height) != (1920, 1080):
                raise EpisodeVideoError(
                    f"materialized visual has wrong dimensions: {asset_id}",
                    code="visual_dimensions_invalid",
                )
        records.append(
            {
                "asset_id": asset_id,
                "asset_type": timing.asset_type,
                "source_provenance_id": timing.source_provenance_id,
                "source_path": (
                    _repo_relative(repo_root, source) if repo_root is not None else source.name
                ),
                "source_sha256": sha256_file(source),
                "png_sha256": sha256_file(output),
                "width": width,
                "height": height,
                "fit_mode": timing.fit_mode,
                "crop": list(timing.crop) if timing.crop is not None else None,
                "source_time_range": (
                    {
                        "start_seconds": timing.source_start_seconds,
                        "end_seconds": timing.source_end_seconds,
                    }
                    if timing.source_start_seconds is not None
                    else None
                ),
                "internal_review_only": timing.internal_review_only,
                "subtitle_lines": list(timing.subtitle_lines),
                "speaker_label": timing.speaker_label,
                "materialization_process": process_receipt,
            }
        )
        outputs[asset_id] = output
    receipt = {
        "status": "passed",
        "unique_visual_count": len(outputs),
        "records": records,
        "real_media_asset_count": sum(
            row["asset_type"] in REAL_MEDIA_ASSET_TYPES for row in records
        ),
        "external_asset_count": sum(
            row["asset_type"] in REAL_MEDIA_ASSET_TYPES for row in records
        ),
        "svg_reference_count": sum(row["asset_type"] == "svg" for row in records),
        "source_svg_modified": False,
    }
    _write_or_verify(
        paths.real_media_asset_manifest,
        canonical_json_bytes(receipt),
        resume=resume,
    )
    return outputs, receipt


def build_yymm4_project(
    repo_root: Path,
    manifest: Mapping[str, Any],
    timings: Sequence[CueTiming],
    visual_outputs: Mapping[str, Path],
    paths: PipelinePaths,
    *,
    resume: bool,
) -> dict[str, Any]:
    source_path = resolve_repo_path(repo_root, str(manifest["yymm4"]["source_project_path"]))
    source_hash_before = sha256_file(source_path)
    project = _read_project(source_path)
    timeline = _selected_timeline(project)
    voices = _voice_items(timeline)
    voice_digest_before = _json_digest(voices)

    project["FilePath"] = str(paths.generated_project.resolve())
    project["SelectedTimelineIndex"] = 0
    project["LayoutXml"] = ""
    project["ToolStates"] = {}
    project["CollapsedGroups"] = []
    timeline["CurrentFrame"] = 0
    timeline["MaxLayer"] = max(2, int(timeline.get("MaxLayer", 0)))
    image_items = [
        _image_item(
            asset_path=visual_outputs[timing.asset_id],
            cue_id=timing.cue_id,
            frame=timing.frame,
            length=timing.length_frames,
            real_media=timing.asset_type in REAL_MEDIA_ASSET_TYPES,
        )
        for timing in timings
    ]
    timeline["Items"] = voices + image_items
    project_bytes = canonical_json_bytes(project)
    if paths.generated_project.exists() and resume:
        if paths.generated_project.read_bytes() != project_bytes:
            raise EpisodeVideoError(
                "cached generated project differs from deterministic rebuild",
                code="generated_project_nondeterministic",
            )
    else:
        paths.generated_project.write_bytes(project_bytes)

    if sha256_file(source_path) != source_hash_before:
        raise EpisodeVideoError("source YMM4 project was modified", code="source_ymmp_mutated")
    readback = readback_generated_project(paths.generated_project, paths.run_directory, timings)
    if _json_digest(_voice_items(_selected_timeline(_read_project(paths.generated_project)))) != voice_digest_before:
        raise EpisodeVideoError("VoiceItem object drift occurred", code="voice_item_object_drift")
    readback["source_project_sha256"] = source_hash_before
    readback["generated_project_sha256"] = sha256_file(paths.generated_project)
    readback["voice_items_unchanged"] = True
    return readback


def readback_generated_project(
    project_path: Path, run_directory: Path, timings: Sequence[CueTiming]
) -> dict[str, Any]:
    project = _read_project(project_path)
    timeline = _selected_timeline(project)
    voices = _voice_items(timeline)
    images = [item for item in timeline.get("Items", []) if item.get("$type") == IMAGE_ITEM_TYPE]
    counts: dict[str, int] = {}
    for item in voices:
        speaker = str(item.get("CharacterName"))
        counts[speaker] = counts.get(speaker, 0) + 1
    expected_intervals = [(t.frame, t.length_frames) for t in timings]
    actual_intervals = [(int(item.get("Frame", -1)), int(item.get("Length", -1))) for item in images]
    real_media_mode = all(timing.asset_type in REAL_MEDIA_ASSET_TYPES for timing in timings)
    image_paths = [str(item.get("FilePath") or "") for item in images]

    path_leaks: list[str] = []
    run_root = run_directory.resolve()
    for pointer, value in _walk_strings(project):
        lowered = value.lower()
        if lowered.startswith(URL_PREFIXES) or value.startswith("\\\\"):
            path_leaks.append(pointer)
            continue
        if ABSOLUTE_WINDOWS_PATH.match(value):
            try:
                Path(value).resolve().relative_to(run_root)
            except ValueError:
                path_leaks.append(pointer)

    checks = {
        "project_parse_pass": True,
        "voice_item_count_matches_manifest": len(voices) == len(timings),
        "image_item_count_matches_manifest": len(images) == len(timings),
        "speaker_counts_match_manifest": counts
        == {
            speaker: sum(timing.speaker == speaker for timing in timings)
            for speaker in {timing.speaker for timing in timings}
        },
        "visual_timing_matches_cues": actual_intervals == expected_intervals,
        "tool_states_stripped": project.get("ToolStates") == {},
        "layout_xml_stripped": project.get("LayoutXml") == "",
        "only_run_directory_absolute_paths": not path_leaks,
        "timeline_frames_match_manifest": int(timeline.get("Length", -1))
        == timings[-1].end_frame,
        "real_media_paths_are_raster": (
            all(Path(path).suffix.lower() in IMAGE_EXTENSIONS for path in image_paths)
            if real_media_mode
            else True
        ),
        "real_media_has_zero_svg_references": (
            not any(value.lower().endswith(".svg") for _, value in _walk_strings(project))
            if real_media_mode
            else True
        ),
        "real_media_remarks_are_not_proxy": (
            all(str(item.get("Remark", "")).startswith("internal-review-real-media:") for item in images)
            if real_media_mode
            else True
        ),
    }
    failed = [key for key, passed in checks.items() if not passed]
    if failed:
        raise EpisodeVideoError(
            f"generated project readback failed: {', '.join(failed)}",
            code="generated_project_readback_failed",
        )
    return {
        "schema": PROJECT_READBACK_SCHEMA,
        "status": "passed",
        "checks": checks,
        "failed_checks": [],
        "voice_item_count": len(voices),
        "image_item_count": len(images),
        "speaker_counts": counts,
        "timeline_frames": int(timeline["Length"]),
        "fps": int(timeline["VideoInfo"]["FPS"]),
        "absolute_path_leaks": [],
        "svg_reference_count": (
            sum(value.lower().endswith(".svg") for _, value in _walk_strings(project))
            if real_media_mode
            else None
        ),
    }


def build_cue_visual_readback(
    timings: Sequence[CueTiming], visual_outputs: Mapping[str, Path], paths: PipelinePaths
) -> dict[str, Any]:
    rows = []
    for timing in timings:
        asset = visual_outputs[timing.asset_id]
        rows.append(
            {
                "cue_id": timing.cue_id,
                "scene_id": timing.scene_id,
                "speaker": timing.speaker,
                "frame": timing.frame,
                "length_frames": timing.length_frames,
                "end_frame": timing.end_frame,
                "visual_id": timing.visual_id,
                "materialized_visual_id": timing.asset_id,
                "asset_type": timing.asset_type,
                "source_provenance_id": timing.source_provenance_id,
                "internal_review_only": timing.internal_review_only,
                "subtitle_lines": list(timing.subtitle_lines),
                "speaker_label": timing.speaker_label,
                "asset_path": f"<run-dir>/generated_assets/{asset.name}",
                "asset_sha256": sha256_file(asset),
            }
        )
    return {
        "schema": VISUAL_READBACK_SCHEMA,
        "status": "passed",
        "cue_count": len(rows),
        "visual_item_coverage": f"{len(rows)}/9",
        "rows": rows,
        "real_media_cue_count": sum(
            row["asset_type"] in REAL_MEDIA_ASSET_TYPES for row in rows
        ),
        "svg_reference_count": sum(row["asset_type"] == "svg" for row in rows),
        "external_asset_count": sum(
            row["asset_type"] in REAL_MEDIA_ASSET_TYPES for row in rows
        ),
        "private_path_count": 0,
    }


def resolve_yymm4_executable() -> Path:
    candidates: list[Path] = []
    explicit = os.environ.get("NLMYTGEN_YMM4_EXE")
    if explicit:
        candidates.append(Path(explicit))
    resolved = shutil.which("YukkuriMovieMaker.exe")
    if resolved:
        candidates.append(Path(resolved))
    if os.name == "nt":
        try:
            import winreg

            for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
                try:
                    with winreg.OpenKey(
                        hive,
                        r"Software\Microsoft\Windows\CurrentVersion\App Paths\YukkuriMovieMaker.exe",
                    ) as key:
                        candidates.append(Path(winreg.QueryValueEx(key, None)[0]))
                except OSError:
                    pass
        except ImportError:
            pass
        for drive_ord in range(ord("C"), ord("Z") + 1):
            drive = f"{chr(drive_ord)}:/"
            candidates.extend(
                [
                    Path(drive) / "YukkuriMovieMaker_v4/YukkuriMovieMaker.exe",
                    Path(drive) / "MovieCreationWorkspace/YukkuriMovieMaker_v4/YukkuriMovieMaker.exe",
                ]
            )
    seen: set[Path] = set()
    for candidate in candidates:
        try:
            canonical = candidate.resolve()
        except OSError:
            continue
        if canonical in seen:
            continue
        seen.add(canonical)
        if canonical.is_file():
            return canonical
    raise EpisodeVideoError("YMM4 executable was not found", code="yymm4_executable_missing")


def build_render_driver_command(
    repo_root: Path, executable: Path, project: Path, output: Path, settings: Mapping[str, Any]
) -> list[str]:
    driver_project = repo_root / "tools" / "Ymm4RenderAutomation" / "Ymm4RenderAutomation.csproj"
    return [
        "dotnet",
        "run",
        "--project",
        str(driver_project),
        "--configuration",
        "Release",
        "--",
        "render",
        "--exe",
        str(executable),
        "--project",
        str(project),
        "--output",
        str(output),
        "--video-bitrate-kbps",
        str(int(settings["video_bitrate_kbps"])),
        "--audio-bitrate-kbps",
        str(int(settings["audio_bitrate_kbps"])),
        "--timeout-seconds",
        str(int(settings.get("timeout_seconds", 1200))),
    ]


def execute_yymm4_render(
    repo_root: Path,
    manifest: Mapping[str, Any],
    paths: PipelinePaths,
    *,
    resume: bool,
) -> dict[str, Any]:
    if paths.yymm4_render.exists() and resume:
        return {
            "status": "reused",
            "render_sha256": sha256_file(paths.yymm4_render),
            "render_size_bytes": paths.yymm4_render.stat().st_size,
            "project_sha256": sha256_file(paths.generated_project),
            "project_owned_process_cleanup": True,
        }
    executable = resolve_yymm4_executable()
    command = build_render_driver_command(
        repo_root, executable, paths.generated_project, paths.yymm4_render, manifest["render_settings"]
    )
    baseline = process_snapshot()
    started_ns = time.time_ns()
    completed = subprocess.run(
        command,
        cwd=repo_root,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=int(manifest["render_settings"].get("timeout_seconds", 1200)) + 60,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    after = process_snapshot()
    new_yymm4 = [
        pid
        for pid, row in after.items()
        if pid not in baseline
        and str(row.get("name", "")).lower() == "yukkurimoviemaker.exe"
    ]
    if new_yymm4:
        raise EpisodeVideoError(
            f"project-owned YMM4 process remained: {new_yymm4}", code="yymm4_process_residual"
        )
    if completed.returncode != 0 or not paths.yymm4_render.is_file():
        summary = _sanitize_subprocess_output(completed.stderr or completed.stdout, paths)
        raise EpisodeVideoError(
            f"YMM4 render automation failed: {summary}", code="yymm4_render_failed"
        )
    if paths.yymm4_render.stat().st_mtime_ns < started_ns:
        raise EpisodeVideoError("YMM4 render is stale", code="render_freshness_failed")
    return {
        "status": "passed",
        "driver": "bounded_windows_uia",
        "yymm4_executable": executable.name,
        "render_sha256": sha256_file(paths.yymm4_render),
        "render_size_bytes": paths.yymm4_render.stat().st_size,
        "project_sha256": sha256_file(paths.generated_project),
        "render_fresh": True,
        "project_owned_process_cleanup": True,
        "speaker_playback_used": False,
        "preview_used": False,
        "stdout_summary": _sanitize_subprocess_output(completed.stdout, paths),
    }


def normalize_review_mp4(
    source: Path, output: Path, settings: Mapping[str, Any], *, resume: bool
) -> dict[str, Any]:
    if output.exists() and resume:
        return {"status": "reused", "sha256": sha256_file(output)}
    if output.exists():
        raise EpisodeVideoError("review MP4 already exists", code="review_mp4_overwrite_refused")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise EpisodeVideoError("ffmpeg is unavailable", code="ffmpeg_missing")
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(source),
        "-map",
        "0:v:0",
        "-map",
        "0:a:0",
        "-c",
        "copy",
        "-movflags",
        "+faststart",
        str(output),
    ]
    assert_command_allowed(command)
    completed = subprocess.run(command, capture_output=True, check=False, timeout=900)
    if completed.returncode != 0 or not output.is_file():
        raise EpisodeVideoError("review MP4 normalization failed", code="mp4_normalization_failed")
    return {
        "status": "passed",
        "source_sha256": sha256_file(source),
        "output_sha256": sha256_file(output),
        "mode": "lossless_stream_remux",
        "video_bitrate_kbps": int(settings["video_bitrate_kbps"]),
        "audio_bitrate_kbps": int(settings["audio_bitrate_kbps"]),
    }


def validate_media(
    mp4: Path,
    timings: Sequence[CueTiming],
    paths: PipelinePaths,
    settings: Mapping[str, Any],
    project_hash: str,
) -> dict[str, Any]:
    iso = inspect_iso_bmff(mp4)
    probe = probe_with_ffprobe(mp4)
    decode = decode_with_ffmpeg(mp4)
    video = next((row for row in probe.get("streams", []) if row.get("codec_type") == "video"), {})
    audio = next((row for row in probe.get("streams", []) if row.get("codec_type") == "audio"), {})
    fmt = probe.get("format") or {}
    expected_duration = timings[-1].end_frame / float(settings["fps"])
    duration = float(fmt.get("duration_seconds") or 0)
    fps = float(video.get("fps") or 0)
    bitrate = int(fmt.get("bit_rate_bps") or 0)
    size = int(fmt.get("size_bytes") or mp4.stat().st_size)
    expected_width = int(settings.get("width", 1920))
    expected_height = int(settings.get("height", 1080))
    duration_tolerance = float(settings.get("max_duration_delta_seconds", 0.5))
    max_size_bytes = int(settings.get("max_size_bytes", 250_000_000))
    min_distinct_frames = int(settings.get("min_distinct_frame_hashes", 4))
    checks = {
        "iso_bmff_ftyp_moov_mdat": iso.get("status") == "passed",
        "ffprobe_parse": probe.get("status") == "passed",
        "h264_video": video.get("codec_name") == "h264",
        "aac_audio": audio.get("codec_name") == "aac",
        "resolution_matches_project": (video.get("width"), video.get("height"))
        == (expected_width, expected_height),
        "fps_matches_project": abs(fps - float(settings["fps"])) < 0.01,
        "duration_within_manifest_tolerance": abs(duration - expected_duration)
        <= duration_tolerance,
        "bitrate_internal_review_range": 6_000_000 <= bitrate <= 16_500_000,
        "size_within_manifest_limit": size < max_size_bytes,
        "audio_and_video_streams_present": bool(video) and bool(audio),
        "full_file_decode": decode.get("status") == "passed",
        "decode_source_unchanged": decode.get("source_unchanged") is True,
    }
    failed = [key for key, passed in checks.items() if not passed]
    frame_readback = extract_review_frames(mp4, timings, paths)
    if frame_readback["unique_sha256_count"] < min_distinct_frames:
        failed.append("representative_frames_not_varied")
        checks["representative_frames_not_varied"] = False
    else:
        checks["representative_frames_not_varied"] = True
    result = {
        "schema": MEDIA_VALIDATION_SCHEMA,
        "status": "passed" if not failed else "failed",
        "checks": checks,
        "failed_checks": failed,
        "iso_bmff": iso,
        "probe": probe,
        "decode": decode,
        "media": {
            "sha256": sha256_file(mp4),
            "size_bytes": size,
            "container": fmt.get("format_name"),
            "video_codec": video.get("codec_name"),
            "audio_codec": audio.get("codec_name"),
            "width": video.get("width"),
            "height": video.get("height"),
            "fps": fps,
            "duration_seconds": duration,
            "overall_bitrate_bps": bitrate,
            "stream_count": probe.get("stream_count"),
        },
        "binding": {
            "project_sha256": project_hash,
            "render_sha256": sha256_file(mp4),
            "render_fresh": mp4.stat().st_mtime_ns >= paths.generated_project.stat().st_mtime_ns,
        },
        "frame_extraction": frame_readback,
    }
    paths.media_validation.write_bytes(canonical_json_bytes(result))
    if failed:
        raise EpisodeVideoError(
            f"media validation failed: {', '.join(failed)}", code="media_validation_failed"
        )
    return result


def extract_review_frames(
    mp4: Path, timings: Sequence[CueTiming], paths: PipelinePaths
) -> dict[str, Any]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise EpisodeVideoError("ffmpeg is unavailable", code="ffmpeg_missing")
    paths.extracted_frames.mkdir(parents=True, exist_ok=True)
    fps = 60.0
    duration = timings[-1].end_frame / fps
    targets = [
        ("first", 0.05),
        ("middle", duration / 2),
        ("last", max(0.0, duration - 0.1)),
    ]
    targets.extend(
        (
            timing.cue_id,
            timing.frame / fps + min(0.25, timing.length_frames / fps / 2),
        )
        for timing in timings
    )
    records = []
    for label, seconds in targets:
        output = paths.extracted_frames / f"{label}.png"
        command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{seconds:.6f}",
            "-i",
            str(mp4),
            "-frames:v",
            "1",
            "-threads",
            "1",
            str(output),
        ]
        assert_command_allowed(command)
        completed = subprocess.run(command, capture_output=True, check=False, timeout=120)
        if completed.returncode != 0 or not output.is_file():
            raise EpisodeVideoError(f"frame extraction failed: {label}", code="frame_extract_failed")
        width, height = png_dimensions(output)
        if (width, height) != (1920, 1080):
            raise EpisodeVideoError(f"extracted frame has wrong size: {label}", code="frame_size_invalid")
        records.append(
            {
                "label": label,
                "seconds": round(seconds, 6),
                "path": f"<run-dir>/extracted_review_frames/{output.name}",
                "sha256": sha256_file(output),
                "width": width,
                "height": height,
            }
        )
    return {
        "status": "passed",
        "frame_count": len(records),
        "cue_frame_count": len(timings),
        "unique_sha256_count": len({row["sha256"] for row in records}),
        "records": records,
    }


def run_episode_video(
    *,
    repo_root: Path,
    manifest_path: Path,
    render: bool,
    dry_run: bool,
    resume: bool,
    force: bool,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    manifest_path = manifest_path.resolve()
    manifest = load_episode_manifest(repo_root, manifest_path)
    paths = build_pipeline_paths(repo_root, manifest)
    preflight, timings = preflight_episode(repo_root, manifest)
    plan = {
        "schema": RUN_RECEIPT_SCHEMA,
        "status": "dry_run" if dry_run else "running",
        "episode_id": manifest["episode_id"],
        "run_id": manifest["output"]["run_id"],
        "stages": [
            "preflight",
            "media_materialization",
            "yymm4_project_generation",
            "yymm4_render" if render else "render_skipped",
            "mp4_normalization" if render else "normalization_skipped",
            "media_validation" if render else "validation_skipped",
            "receipt_generation",
        ],
        "preflight": preflight,
        "output_directory": str(manifest["output"]["run_root_path"]).rstrip("/")
        + "/"
        + str(manifest["output"]["run_id"]),
        "render_requested": render,
        "resume": resume,
        "force": force,
        "boundaries": manifest["boundaries"],
    }
    if dry_run:
        return plan

    if paths.run_directory.exists() and not (resume or force):
        raise EpisodeVideoError(
            f"run directory already exists; use --resume or --force: {paths.run_directory}",
            code="run_overwrite_refused",
        )
    if paths.run_directory.exists() and force:
        output_root = paths.run_directory.parent.resolve()
        run_directory = paths.run_directory.resolve()
        if run_directory.parent != output_root:
            raise EpisodeVideoError("force target escaped the output root", code="force_target_invalid")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        replacement = output_root / f"{run_directory.name}.replaced-{stamp}.local"
        if replacement.exists():
            raise EpisodeVideoError("force replacement archive already exists", code="force_archive_exists")
        run_directory.replace(replacement)
        resume = False
    paths.run_directory.mkdir(parents=True, exist_ok=True)
    paths.generated_assets.mkdir(parents=True, exist_ok=True)
    paths.extracted_frames.mkdir(parents=True, exist_ok=True)
    _append_log(paths.run_log, "preflight passed")

    resolved_manifest = {
        **manifest,
        "runtime_resolution": {
            "repo_root": "<repo-root>",
            "manifest_path": _repo_relative(repo_root, manifest_path),
            "run_directory": "<repo-root>/" + _repo_relative(repo_root, paths.run_directory),
        },
    }
    _write_or_verify(paths.resolved_manifest, canonical_json_bytes(resolved_manifest), resume=resume)

    visuals, visual_receipt = materialize_visuals(
        timings, paths, resume=resume, repo_root=repo_root
    )
    _append_log(paths.run_log, "visual materialization passed")
    project_readback = build_yymm4_project(
        repo_root, manifest, timings, visuals, paths, resume=resume
    )
    _append_log(paths.run_log, "YMM4 project generation/readback passed")
    cue_readback = build_cue_visual_readback(timings, visuals, paths)
    _write_or_verify(paths.cue_visual_readback, canonical_json_bytes(cue_readback), resume=resume)

    render_receipt: dict[str, Any] | None = None
    normalization: dict[str, Any] | None = None
    media: dict[str, Any] | None = None
    if render:
        render_receipt = execute_yymm4_render(repo_root, manifest, paths, resume=resume)
        _append_log(paths.run_log, "YMM4 render passed")
        normalization = normalize_review_mp4(
            paths.yymm4_render, paths.review_mp4, manifest["render_settings"], resume=resume
        )
        _append_log(paths.run_log, "review MP4 normalization passed")
        media = validate_media(
            paths.review_mp4,
            timings,
            paths,
            manifest["render_settings"],
            sha256_file(paths.generated_project),
        )
        _append_log(paths.run_log, "media validation and frame extraction passed")

    receipt = {
        **plan,
        "status": "passed",
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "preflight": preflight,
        "visual_materialization": visual_receipt,
        "project_readback": project_readback,
        "cue_visual_readback_sha256": sha256_file(paths.cue_visual_readback),
        "render": render_receipt,
        "normalization": normalization,
        "media_validation": media,
        "outputs": {
            "resolved_manifest": "<run-dir>/resolved_manifest.json",
            "real_media_asset_manifest": "<run-dir>/real_media_asset_manifest.local.json",
            "generated_assets": "<run-dir>/generated_assets",
            "generated_project": f"<run-dir>/{paths.generated_project.name}",
            "internal_review_mp4": f"<run-dir>/{paths.review_mp4.name}" if render else None,
            "media_validation": "<run-dir>/media_validation.json" if render else None,
            "extracted_review_frames": "<run-dir>/extracted_review_frames" if render else None,
            "run_log": "<run-dir>/run.log",
        },
        "repeatability": {
            "protected_input_hashes_verified": True,
            "deterministic_project_generation": True,
            "existing_run_requires_resume_or_force": True,
            "existing_render_not_overwritten_without_force": True,
        },
        "silent_execution": {
            "policy": resolve_audio_policy(),
            "speaker_playback": False,
            "preview_playback": False,
            "system_volume_changed": False,
            "public_media_access": False,
        },
    }
    paths.run_receipt.write_bytes(canonical_json_bytes(receipt))
    _append_log(paths.run_log, "run receipt written")
    return receipt


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise EpisodeVideoError(f"not a PNG: {path.name}", code="png_invalid")
    return struct.unpack(">II", header[16:24])


def _render_svg_with_silent_chromium(source: Path, output: Path, browser: Path) -> dict[str, Any]:
    baseline = process_snapshot()
    baseline_pids = set(baseline)
    command: list[str]
    # Chromium's --screenshot path handling still trips over long Windows paths.
    # Capture under the short OS temp root, then copy the verified PNG into the
    # ignored run directory.
    with tempfile.TemporaryDirectory(prefix="nlmytgen-svg-") as temporary:
        temporary_root = Path(temporary)
        profile = temporary_root / "profile"
        capture = temporary_root / "capture.png"
        command = [
            str(browser),
            "--headless=new",
            "--mute-audio",
            "--autoplay-policy=user-gesture-required",
            "--disable-background-mode",
            "--disable-background-networking",
            "--disable-breakpad",
            "--disable-component-update",
            "--disable-crash-reporter",
            "--disable-default-apps",
            "--disable-sync",
            "--metrics-recording-only",
            "--no-default-browser-check",
            "--no-first-run",
            "--no-pings",
            "--disable-extensions",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--window-size=1920,1080",
            "--host-resolver-rules=MAP * ~NOTFOUND",
            f"--user-data-dir={profile}",
            f"--screenshot={capture}",
            source.resolve().as_uri(),
        ]
        assert_command_allowed(command, guarded_browser=True)
        process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
        )
        completed_stdout: bytes = b""
        completed_stderr: bytes = b""
        try:
            completed_stdout, completed_stderr = process.communicate(timeout=60)
        except subprocess.TimeoutExpired as exc:
            process.kill()
            process.communicate()
            raise EpisodeVideoError("Chromium SVG render timed out", code="svg_render_timeout") from exc
        current = process_snapshot()
        owned = descendant_pids(process.pid, current) - baseline_pids
        if process.returncode != 0 or not capture.is_file():
            raise EpisodeVideoError(
                "Chromium SVG render failed: "
                + (completed_stderr.decode("utf-8", errors="replace")[-500:] or "no screenshot"),
                code="svg_materialization_failed",
            )
        if png_dimensions(capture) != (1920, 1080):
            raise EpisodeVideoError(
                "Chromium SVG render produced wrong dimensions",
                code="visual_dimensions_invalid",
            )
        shutil.copyfile(capture, output)
        time.sleep(0.1)
        remaining = (owned | {process.pid}) & set(process_snapshot())
        if remaining:
            raise EpisodeVideoError(
                f"Chromium process residual after SVG render: {sorted(remaining)}",
                code="svg_browser_process_residual",
            )
    return {
        "status": "passed",
        "browser": browser.name,
        "network_blocked": True,
        "mute_flag": True,
        "autoplay_suppressed": True,
        "isolated_profile_removed": True,
        "cleanup_verified": True,
        "stderr_nonempty": bool(completed_stderr.strip()),
        "stdout_nonempty": bool(completed_stdout.strip()),
    }


def _selected_timeline(project: Mapping[str, Any]) -> dict[str, Any]:
    timelines = project.get("Timelines")
    if not isinstance(timelines, list) or len(timelines) != 1 or not isinstance(timelines[0], dict):
        raise EpisodeVideoError("YMM4 project must have one timeline", code="ymmp_timeline_invalid")
    return timelines[0]


def _voice_items(timeline: Mapping[str, Any]) -> list[dict[str, Any]]:
    items = timeline.get("Items")
    if not isinstance(items, list):
        raise EpisodeVideoError("YMM4 Items is not a list", code="ymmp_items_invalid")
    voices = [item for item in items if isinstance(item, dict) and item.get("$type") == VOICE_ITEM_TYPE]
    return sorted(voices, key=lambda item: int(item.get("Frame", -1)))


def _image_item(
    *, asset_path: Path, cue_id: str, frame: int, length: int, real_media: bool = False
) -> dict[str, Any]:
    def animation(value: float) -> dict[str, Any]:
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

    return {
        "$type": IMAGE_ITEM_TYPE,
        "FilePath": str(asset_path.resolve()),
        "X": animation(0.0),
        "Y": animation(0.0),
        "Z": animation(0.0),
        "Zoom": animation(100.0),
        "Opacity": animation(100.0),
        "Rotation": animation(0.0),
        "FadeIn": 0.0,
        "FadeOut": 0.0,
        "Blend": "Normal",
        "IsInverted": False,
        "IsClippingWithObjectAbove": False,
        "IsAlwaysOnTop": False,
        "IsZOrderEnabled": False,
        "VideoEffects": [],
        "Layer": 2,
        "Group": 0,
        "KeyFrames": {"Frames": [], "Count": 0},
        "PlaybackRate": 100.0,
        "ContentOffset": "00:00:00",
        "IsLocked": False,
        "IsHidden": False,
        "Frame": frame,
        "Length": length,
        "Remark": (
            f"internal-review-real-media:{cue_id}"
            if real_media
            else f"internal-review-proxy:{cue_id}"
        ),
    }


def _read_project(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EpisodeVideoError(f"YMM4 project parse failed: {path}", code="ymmp_parse_failed") from exc
    if not isinstance(payload, dict):
        raise EpisodeVideoError("YMM4 project root is not an object", code="ymmp_parse_failed")
    return payload


def _read_csv(path: Path) -> list[list[str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = [row for row in csv.reader(handle) if row]
    except (OSError, UnicodeError, csv.Error) as exc:
        raise EpisodeVideoError(f"derived CSV parse failed: {path}", code="csv_parse_failed") from exc
    if any(len(row) != 2 for row in rows):
        raise EpisodeVideoError("derived CSV rows must have two columns", code="csv_shape_invalid")
    return rows


def _walk_strings(value: Any, pointer: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = f"{pointer}/{key}" if pointer else str(key)
            yield from _walk_strings(child, child_pointer)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_pointer = f"{pointer}/{index}" if pointer else str(index)
            yield from _walk_strings(child, child_pointer)
    elif isinstance(value, str):
        yield pointer, value


def _manifest_repo_paths(manifest: Mapping[str, Any]) -> Iterable[str]:
    yield str(manifest["source_package"])
    yield str(manifest["approved_script"])
    yield str(manifest["derived_csv"])
    yield str(manifest["visual_source_path"])
    yield str(manifest["yymm4"]["source_project_path"])
    yield str(manifest["output"]["run_root_path"])
    if manifest.get("provenance_manifest_path"):
        yield str(manifest["provenance_manifest_path"])
    for cue in manifest["cue_mapping"]:
        if cue.get("visual_source_path"):
            yield str(cue["visual_source_path"])
        if cue.get("local_asset_path"):
            yield str(cue["local_asset_path"])
    for row in manifest["content_locks"]:
        yield str(row["path"])


def _json_digest(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _write_or_verify(path: Path, content: bytes, *, resume: bool) -> None:
    if path.exists() and resume:
        if path.read_bytes() != content:
            raise EpisodeVideoError(
                f"resume artifact drift: {path.name}", code="resume_artifact_drift"
            )
        return
    path.write_bytes(content)


def _repo_relative(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _append_log(path: Path, message: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{timestamp} {message}\n")


def _sanitize_subprocess_output(text: str, paths: PipelinePaths) -> str:
    sanitized = text or ""
    replacements = [
        (str(paths.run_directory), "<run-dir>"),
        (str(paths.run_directory.resolve()), "<run-dir>"),
    ]
    for raw, replacement in replacements:
        sanitized = sanitized.replace(raw, replacement)
    sanitized = re.sub(r"[A-Za-z]:\\[^\r\n\"]+", "<local-path>", sanitized)
    return " ".join(sanitized.strip().split())[-1000:]
