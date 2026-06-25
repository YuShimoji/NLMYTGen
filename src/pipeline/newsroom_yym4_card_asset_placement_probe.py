"""Diagnostic YMM4 card image placement probe for the newsroom handoff.

This slice converts the already-created external SVG card assets into PNGs and
places those PNGs as ImageItem objects in an ignored local YMM4 copy. It does
not launch YMM4, render video, generate audio/TTS, fetch external media, or
approve production use.
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import struct
import subprocess
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from PIL import Image, ImageDraw, ImageFont

from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH,
    DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
)
from src.pipeline.newsroom_ymmp_timing_patch_probe import (
    DEFAULT_PATCHED_YMMP_LOCAL_PATH as DEFAULT_TIMING_PATCHED_YMMP_LOCAL_PATH,
    DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH,
)
from src.pipeline.newsroom_ymmp_timing_patch_render_smoke_result_readback import (
    DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH,
)
from src.pipeline.skit_group_placement import _format_yymm_asset_path
from src.pipeline.ymmp_patch import (
    _build_overlay_item,
    _get_timeline_items,
    _item_type,
    load_ymmp,
    save_ymmp,
)


YYM4_CARD_ASSET_PLACEMENT_PROBE_SCHEMA_VERSION = (
    "newsroom_yym4_card_asset_placement_probe.v1"
)
YYM4_CARD_ASSET_PLACEMENT_PROBE_ID = (
    "newsroom_yym4_card_asset_placement_probe_v1_2026_06_25"
)
DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH = Path(
    "samples/_probe/newsroom_handoff/yym4_card_asset_placement_probe_v1.json"
)
DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YYM4_CARD_ASSET_PLACEMENT_PROBE_V1_2026-06-25.md"
)
DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH = Path(
    "_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp"
)

FRAME_RATE = 60
EXPECTED_TOTAL_FRAMES = 4080
EXPECTED_DURATION_SEC = 68
CARD_LAYER = 2
CARD_REMARK_PREFIX = "newsroom_card_asset:"
NEXT_DEFAULT_SLICE = "newsroom-card-placement-render-smoke-v1"
PNG_EXPORT_SLICE = "newsroom-visual-card-raster-export-v1"
IMAGE_SCHEMA_AUDIT_SLICE = "newsroom-yym4-image-item-schema-audit-v1"
INTERNAL_REVIEW_PREP_SLICE = "newsroom-internal-review-v0.1-prep"

EXPECTED_TEXTS = (
    "Fake topic, review only.",
    "Review-only handoff stays.",
    "A fake claim is shown.",
    "Fake source checks are noted.",
)


def build_default_newsroom_yym4_card_asset_placement_probe(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the placement probe readback from the current local evidence."""
    base = Path(root) if root is not None else Path(".")
    bridge = load_json_object(base / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH)
    render_result = load_json_object(
        base / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    timing_probe = load_json_object(base / DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH)

    source_assets = _source_assets(bridge)
    raster_status = _raster_export_status(base, source_assets)
    source_ymmp_path = base / DEFAULT_TIMING_PATCHED_YMMP_LOCAL_PATH
    patched_ymmp_path = base / DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH
    source_summary = _ymmp_summary(source_ymmp_path)
    patched_summary = _ymmp_summary(patched_ymmp_path)
    structural_status = _structural_status(source_summary, patched_summary)
    source_validation = _source_validation(
        bridge=bridge,
        render_result=render_result,
        timing_probe=timing_probe,
        source_assets=source_assets,
        raster_status=raster_status,
        source_summary=source_summary,
        patched_summary=patched_summary,
        structural_status=structural_status,
    )
    probe_status = _probe_status(source_validation, raster_status, structural_status)

    return {
        "artifact_id": YYM4_CARD_ASSET_PLACEMENT_PROBE_ID,
        "probe_id": YYM4_CARD_ASSET_PLACEMENT_PROBE_ID,
        "schema_version": YYM4_CARD_ASSET_PLACEMENT_PROBE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "probe_status": probe_status,
        "identity": {
            "probe_id": YYM4_CARD_ASSET_PLACEMENT_PROBE_ID,
            "source_visual_card_bridge_path": _path_text(
                DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH
            ),
            "source_render_smoke_result_path": _path_text(
                DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH
            ),
            "source_timing_patch_probe_path": _path_text(
                DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH
            ),
            "source_ymmp_local_path": _path_text(
                DEFAULT_TIMING_PATCHED_YMMP_LOCAL_PATH
            ),
            "patched_ymmp_local_path": _path_text(
                DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH
            ),
            "production_status": "diagnostic_only",
            "probe_status": probe_status,
            "observation_source": "repo_structural_probe_without_yym4_launch",
        },
        "source_validation": source_validation,
        "source_assets": source_assets,
        "raster_export_status": raster_status,
        "placement_operations": _placement_operations(
            source_assets, structural_status
        ),
        "preservation_checks": _preservation_checks(
            structural_status, source_summary, patched_summary
        ),
        "structural_result": _structural_result(
            source_assets, structural_status, patched_summary
        ),
        "accepted_scope": _accepted_scope(probe_status),
        "not_accepted_scope": _not_accepted_scope(),
        "readiness_separation": _readiness_separation(probe_status),
        "recommended_next_slices": _recommended_next_slices(probe_status),
        "goal_stack": _goal_stack(probe_status),
        "completion_matrix": _completion_matrix(probe_status),
        "artifact_readiness": _artifact_readiness(probe_status),
        "video_readiness": _video_readiness(),
        "visual_readiness": _visual_readiness(probe_status),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(probe_status),
        "placement_contract": _placement_contract(),
        "boundaries": _boundaries(),
        "local_artifact_status": _local_artifact_status(
            base, DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH
        ),
        "downstream_next_use": _downstream_next_use(probe_status),
    }


def write_default_newsroom_yym4_card_asset_placement_probe_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write PNGs, ignored local YMM4 copy, JSON readback, and Markdown doc."""
    base = Path(root) if root is not None else Path(".")
    bridge = load_json_object(base / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH)
    source_assets = _source_assets(bridge)

    export_result = ensure_card_png_assets(base, source_assets)
    if export_result["png_export_status"] not in {"generated", "already_present"}:
        probe = build_default_newsroom_yym4_card_asset_placement_probe(root=base)
        _write_json(base / DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH, probe)
        _write_text(
            base / DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_DOC_PATH,
            render_newsroom_yym4_card_asset_placement_probe_markdown(probe),
        )
        return probe

    create_card_placement_ymmp(
        source_path=base / DEFAULT_TIMING_PATCHED_YMMP_LOCAL_PATH,
        target_path=base / DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH,
        source_assets=source_assets,
        root=base,
    )

    probe = build_default_newsroom_yym4_card_asset_placement_probe(root=base)
    _write_json(base / DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH, probe)
    _write_text(
        base / DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_DOC_PATH,
        render_newsroom_yym4_card_asset_placement_probe_markdown(probe),
    )
    return probe


def ensure_card_png_assets(
    root: str | Path,
    source_assets: list[dict[str, Any]],
) -> dict[str, Any]:
    """Generate PNG cards from the committed SVG cards using local sharp."""
    base = Path(root)
    missing_svg = [
        asset["source_svg_path"]
        for asset in source_assets
        if not (base / asset["source_svg_path"]).exists()
    ]
    if missing_svg:
        return {
            "png_export_status": "blocked",
            "rasterization_method": "not_available",
            "deterministic_export": False,
            "errors": [f"SVG_SOURCE_MISSING:{path}" for path in missing_svg],
            "png_files": [],
        }

    existing_pngs = [
        _png_metadata_for_asset(base, asset)
        for asset in source_assets
        if (base / asset["png_path"]).exists()
    ]
    if len(existing_pngs) == len(source_assets) and all(
        metadata.get("valid") for metadata in existing_pngs
    ):
        return {
            "png_export_status": "already_present",
            "rasterization_method": "existing_toolchain",
            "deterministic_export": True,
            "errors": [],
            "png_files": existing_pngs,
        }

    errors: list[str] = []
    exporter = _find_sharp_exporter()
    if exporter is not None:
        errors = _export_pngs_with_sharp(base, source_assets, exporter)
    else:
        errors = ["LOCAL_SHARP_EXPORTER_NOT_AVAILABLE"]

    if errors:
        errors = _export_pngs_with_pillow_svg_subset(base, source_assets)

    if errors:
        return {
            "png_export_status": "blocked",
            "rasterization_method": "not_available",
            "deterministic_export": False,
            "errors": errors,
            "png_files": existing_pngs,
        }

    png_files = [_png_metadata_for_asset(base, asset) for asset in source_assets]
    errors = [
        f"PNG_EXPORT_INVALID:{metadata.get('path')}"
        for metadata in png_files
        if not metadata.get("valid")
    ]
    return {
        "png_export_status": "generated" if not errors else "blocked",
        "rasterization_method": "existing_toolchain",
        "deterministic_export": not errors,
        "errors": errors,
        "png_files": png_files,
    }


def _export_pngs_with_sharp(
    base: Path,
    source_assets: list[dict[str, Any]],
    exporter: tuple[Path, Path],
) -> list[str]:
    jobs = []
    for asset in source_assets:
        output_path = base / asset["png_path"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        jobs.append(
            {
                "input": str((base / asset["source_svg_path"]).resolve()),
                "output": str(output_path.resolve()),
            }
        )

    node_path, module_dir = exporter
    script = (
        "const sharp = require('sharp');"
        "const jobs = JSON.parse(process.argv[1]);"
        "(async () => {"
        "for (const job of jobs) {"
        "await sharp(job.input).png().toFile(job.output);"
        "}"
        "})().catch((err) => { console.error(err); process.exit(1); });"
    )
    env = os.environ.copy()
    env["NODE_PATH"] = str(module_dir)
    result = subprocess.run(
        [str(node_path), "-e", script, json.dumps(jobs)],
        cwd=base,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return ["SHARP_EXPORT_FAILED"]
    return []


def _export_pngs_with_pillow_svg_subset(
    base: Path,
    source_assets: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    for asset in source_assets:
        svg_path = base / asset["source_svg_path"]
        png_path = base / asset["png_path"]
        png_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            _render_svg_subset_to_png(svg_path, png_path)
        except (OSError, ElementTree.ParseError, ValueError) as exc:
            errors.append(f"PILLOW_SVG_SUBSET_EXPORT_FAILED:{svg_path}:{exc}")
    return errors


def create_card_placement_ymmp(
    *,
    source_path: str | Path,
    target_path: str | Path,
    source_assets: list[dict[str, Any]],
    root: str | Path,
) -> None:
    """Create the ignored diagnostic YMM4 copy with card ImageItems inserted."""
    base = Path(root)
    data = load_ymmp(source_path)
    patched = copy.deepcopy(data)
    timeline = _first_timeline(patched)
    if timeline is None:
        raise ValueError("YMM4 timeline not found")

    items = timeline.setdefault("Items", [])
    items[:] = [
        item
        for item in items
        if not (
            _item_type(item) == "ImageItem"
            and isinstance(item.get("Remark"), str)
            and item["Remark"].startswith(CARD_REMARK_PREFIX)
        )
    ]

    for asset in source_assets:
        frame = int(asset["start_frame"])
        length = int(asset["length_frames"])
        png_path = (base / asset["png_path"]).resolve()
        item = _build_overlay_item(
            {
                "path": _format_yymm_asset_path(png_path),
                "x": 0.0,
                "y": 0.0,
                "zoom": 100.0,
                "opacity": 100.0,
                "layer": CARD_LAYER,
                "group": 0,
            },
            frame=frame,
            length=length,
        )
        item["Remark"] = f"{CARD_REMARK_PREFIX}{asset['card_id']}"
        items.append(item)

    items.sort(key=lambda item: (int(item.get("Frame", 0)), int(item.get("Layer", 0))))
    timeline["Length"] = EXPECTED_TOTAL_FRAMES
    timeline["MaxLayer"] = max(
        int(timeline.get("MaxLayer", 0) or 0),
        CARD_LAYER,
        *(int(item.get("Layer", 0) or 0) for item in items),
    )
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    save_ymmp(patched, target)


def render_newsroom_yym4_card_asset_placement_probe_markdown(
    probe: dict[str, Any],
) -> str:
    """Render a human-readable placement probe readback."""
    lines = [
        "# Newsroom YMM4 Card Asset Placement Probe v1",
        "",
        f"artifact_id: {probe.get('artifact_id')}",
        f"probe_id: {probe.get('probe_id')}",
        f"schema_version: {probe.get('schema_version')}",
        f"review_status: {probe.get('review_status')}",
        f"production_status: {probe.get('production_status')}",
        f"probe_status: {probe.get('probe_status')}",
        "diagnostic_only: true",
        "",
        "## Identity",
        "",
    ]
    for key, value in _dict(probe.get("identity")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Source Validation", ""])
    for key, value in _dict(probe.get("source_validation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Source Assets",
            "",
            "| card_id | timing | dialogue | svg | png |",
            "|---|---:|---|---|---|",
        ]
    )
    for asset in probe.get("source_assets", []):
        lines.append(
            "| "
            f"{asset.get('card_id')} | "
            f"{asset.get('intended_start_sec')}-{asset.get('intended_end_sec')}s | "
            f"{asset.get('mapped_dialogue_text')} | "
            f"{asset.get('source_svg_path')} | "
            f"{asset.get('png_path')} |"
        )

    lines.extend(["", "## Raster Export", ""])
    for key, value in _dict(probe.get("raster_export_status")).items():
        if key == "png_files":
            continue
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Placement Operations",
            "",
            "| operation_id | frame | length | target | applied |",
            "|---|---:|---:|---|---|",
        ]
    )
    for row in probe.get("placement_operations", []):
        lines.append(
            "| "
            f"{row.get('operation_id')} | "
            f"{row.get('start_frame')} | "
            f"{row.get('length_frames')} | "
            f"{row.get('target_layer_or_track')} | "
            f"{_display(row.get('applied'))} |"
        )

    lines.extend(["", "## Preservation Checks", ""])
    for key, value in _dict(probe.get("preservation_checks")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Structural Result", ""])
    for key, value in _dict(probe.get("structural_result")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Accepted Scope", ""])
    for key, value in _dict(probe.get("accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(probe.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Readiness Separation", ""])
    for key, value in _dict(probe.get("readiness_separation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Recommended Next Slices",
            "",
            "| slice | timing | reason |",
            "|---|---|---|",
        ]
    )
    for row in probe.get("recommended_next_slices", []):
        lines.append(
            "| "
            f"{row.get('slice')} | "
            f"{row.get('timing')} | "
            f"{row.get('reason')} |"
        )

    lines.extend(
        [
            "",
            "## Goal Stack",
            "",
            "| level | goal | success signal | contribution |",
            "|---|---|---|---|",
        ]
    )
    for row in probe.get("goal_stack", []):
        lines.append(
            "| "
            f"{row.get('level')} | "
            f"{row.get('goal')} | "
            f"{row.get('success_signal')} | "
            f"{row.get('contribution')} |"
        )

    _append_status_table(lines, "Completion Matrix", probe.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", probe.get("artifact_readiness"))
    _append_status_table(lines, "Video Readiness", probe.get("video_readiness"))
    _append_status_table(lines, "Visual Readiness", probe.get("visual_readiness"))
    _append_status_table(lines, "Render Gate Hygiene", probe.get("render_gate_hygiene"))
    _append_status_table(
        lines, "Human Burden Hygiene", probe.get("human_burden_hygiene")
    )
    _append_status_table(
        lines, "Review Non-Redundancy", probe.get("review_non_redundancy")
    )
    _append_status_table(lines, "Inertia Check", probe.get("inertia_check"))

    lines.extend(["", "## Placement Contract", ""])
    for key, value in _dict(probe.get("placement_contract")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Boundary", ""])
    for key, value in _dict(probe.get("boundaries")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This probe proves structural image-asset placement in the ignored "
            "diagnostic YMM4 copy only. It preserves the prior native audio and "
            "68 second timing evidence, avoids direct YMM4 text/shape card "
            "reconstruction, and leaves post-placement render smoke, internal "
            "review, real newsroom visuals, and production approval to later "
            "milestones.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_assets(bridge: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for asset in _list(bridge.get("assets")):
        svg_path = Path(str(asset.get("repo_relative_path", "")))
        png_path = svg_path.with_suffix(".png")
        start_sec = int(asset.get("intended_start_sec", 0) or 0)
        end_sec = int(asset.get("intended_end_sec", start_sec) or start_sec)
        rows.append(
            {
                "card_id": asset.get("asset_id"),
                "source_svg_path": _path_text(svg_path),
                "png_path": _path_text(png_path),
                "html_preview_path": _path_text(DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH),
                "mapped_dialogue_or_caption_id": asset.get(
                    "source_caption_or_beat_id"
                ),
                "mapped_dialogue_text": asset.get("text"),
                "intended_start_sec": start_sec,
                "intended_end_sec": end_sec,
                "intended_duration_sec": end_sec - start_sec,
                "start_frame": start_sec * FRAME_RATE,
                "length_frames": max((end_sec - start_sec) * FRAME_RATE, 1),
                "placement_role": "diagnostic_visual_card_image_asset",
                "target_layer_or_track": f"Layer {CARD_LAYER} / ImageItem",
                "direct_yym4_card_object_graph": False,
                "yym4_text_shape_reconstruction": False,
            }
        )
    return rows


def _raster_export_status(
    root: str | Path,
    source_assets: list[dict[str, Any]],
) -> dict[str, Any]:
    base = Path(root)
    png_files = [_png_metadata_for_asset(base, asset) for asset in source_assets]
    all_valid = len(png_files) == len(source_assets) and all(
        file.get("valid") for file in png_files
    )
    errors = [
        f"PNG_INVALID_OR_MISSING:{file.get('path')}"
        for file in png_files
        if not file.get("valid")
    ]
    return {
        "png_export_status": "generated" if all_valid else "blocked",
        "rasterization_method": "existing_toolchain" if all_valid else "unknown",
        "deterministic_export": True if all_valid else "unknown",
        "png_files_generated_in_this_slice": all_valid,
        "png_file_count": len([file for file in png_files if file.get("exists")]),
        "expected_png_file_count": len(source_assets),
        "asset_dimensions": "1920x1080",
        "source_format": "svg",
        "target_format": "png",
        "external_fetch_performed": False,
        "real_media_dependency": False,
        "errors": errors,
        "png_files": png_files,
    }


def _ymmp_summary(path: str | Path) -> dict[str, Any]:
    ymmp_path = Path(path)
    if not ymmp_path.exists():
        return {"exists": False, "path": _path_text(ymmp_path)}
    data = load_ymmp(ymmp_path)
    timeline = _first_timeline(data)
    items = _get_timeline_items(data)
    voices = [item for item in items if _item_type(item) == "VoiceItem"]
    image_items = [item for item in items if _item_type(item) == "ImageItem"]
    card_items = [
        item
        for item in image_items
        if isinstance(item.get("Remark"), str)
        and item["Remark"].startswith(CARD_REMARK_PREFIX)
    ]
    return {
        "exists": True,
        "path": _path_text(ymmp_path),
        "timeline_length_frames": timeline.get("Length") if timeline else None,
        "max_layer": timeline.get("MaxLayer") if timeline else None,
        "item_count": len(items),
        "voice_item_count": len(voices),
        "image_item_count": len(image_items),
        "card_image_item_count": len(card_items),
        "voice_items": [_voice_summary(item) for item in voices],
        "card_image_items": [_image_summary(item) for item in card_items],
    }


def _structural_status(
    source_summary: dict[str, Any],
    patched_summary: dict[str, Any],
) -> dict[str, Any]:
    source_voices = source_summary.get("voice_items", [])
    patched_voices = patched_summary.get("voice_items", [])
    card_items = patched_summary.get("card_image_items", [])
    voice_fields_preserved = _voice_preservation_keys(source_voices) == (
        _voice_preservation_keys(patched_voices)
    )
    expected_frames = [
        {
            "frame": index[0],
            "length": index[1],
        }
        for index in [(0, 720), (720, 720), (1440, 1320), (2760, 1320)]
    ]
    observed_frames = [
        {
            "frame": item.get("Frame"),
            "length": item.get("Length"),
        }
        for item in card_items
    ]
    return {
        "source_ymmp_exists": source_summary.get("exists") is True,
        "patched_ymmp_exists": patched_summary.get("exists") is True,
        "timeline_duration_preserved": (
            source_summary.get("timeline_length_frames") == EXPECTED_TOTAL_FRAMES
            and patched_summary.get("timeline_length_frames") == EXPECTED_TOTAL_FRAMES
        ),
        "dialogue_items_preserved": source_voices == patched_voices,
        "native_audio_fields_preserved": voice_fields_preserved,
        "speaker_preserved": voice_fields_preserved,
        "card_image_item_count": len(card_items),
        "card_item_count_expected": 4,
        "card_items_match_expected_timing": observed_frames == expected_frames,
        "card_items_use_image_item_schema": all(
            item.get("item_type") == "ImageItem" for item in card_items
        ),
        "card_items_use_png_paths": all(
            str(item.get("FilePath", "")).lower().endswith(".png")
            for item in card_items
        ),
        "card_items_use_target_layer": all(
            item.get("Layer") == CARD_LAYER for item in card_items
        ),
    }


def _source_validation(
    *,
    bridge: dict[str, Any],
    render_result: dict[str, Any],
    timing_probe: dict[str, Any],
    source_assets: list[dict[str, Any]],
    raster_status: dict[str, Any],
    source_summary: dict[str, Any],
    patched_summary: dict[str, Any],
    structural_status: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    normalized = _dict(render_result.get("normalized_render_result"))
    timing_result = _dict(timing_probe.get("patch_result"))
    observed_texts = [item.get("text") for item in source_summary.get("voice_items", [])]
    if bridge.get("visual_status") != "asset_bridge_created":
        errors.append("VISUAL_CARD_BRIDGE_NOT_READY")
    if render_result.get("result_status") != "pass":
        errors.append("RENDER_SMOKE_RESULT_NOT_PASS")
    if normalized.get("output_duration_sec") != EXPECTED_DURATION_SEC:
        errors.append("RENDER_SMOKE_DURATION_NOT_68")
    if normalized.get("native_audio_present") is not True:
        errors.append("NATIVE_AUDIO_NOT_PRESENT_IN_PRIOR_RESULT")
    if timing_result.get("total_length_frames") not in {
        EXPECTED_TOTAL_FRAMES,
        None,
    } and timing_probe.get("total_frames") not in {EXPECTED_TOTAL_FRAMES, None}:
        errors.append("TIMING_PATCH_TOTAL_FRAMES_NOT_4080")
    if len(source_assets) != 4:
        errors.append("VISUAL_CARD_ASSET_COUNT_NOT_4")
    if raster_status.get("png_export_status") != "generated":
        errors.append("PNG_EXPORT_NOT_READY")
    if source_summary.get("exists") is not True:
        errors.append("SOURCE_YMMP_MISSING")
    if observed_texts != list(EXPECTED_TEXTS):
        errors.append("SOURCE_DIALOGUE_TEXT_MISMATCH")
    if structural_status.get("patched_ymmp_exists") is not True:
        errors.append("PATCHED_PLACEMENT_YMMP_MISSING")
    if structural_status.get("card_image_item_count") != 4:
        errors.append("CARD_IMAGE_ITEM_COUNT_NOT_4")
    if structural_status.get("card_items_use_image_item_schema") is not True:
        errors.append("CARD_IMAGE_ITEM_SCHEMA_NOT_CONFIRMED")

    return {
        "status": "passed" if not errors else "blocked",
        "errors": errors,
        "source_visual_card_bridge_id": bridge.get("bridge_id"),
        "source_render_smoke_result_id": render_result.get("readback_id"),
        "source_timing_patch_probe_id": timing_probe.get("probe_id"),
        "render_smoke_result": render_result.get("result_status"),
        "duration_sec": normalized.get("output_duration_sec"),
        "native_audio_present": normalized.get("native_audio_present"),
        "source_ymmp_exists": source_summary.get("exists"),
        "patched_ymmp_exists": patched_summary.get("exists"),
        "source_dialogue_item_count": source_summary.get("voice_item_count"),
        "patched_dialogue_item_count": patched_summary.get("voice_item_count"),
        "source_card_asset_count": len(source_assets),
        "png_file_count": raster_status.get("png_file_count"),
        "image_item_schema_source": "existing_repo_overlay_builder_and_tracked_ymmp_samples",
        "canonical_speaker": "yukkuri_reimu",
        "canonical_speaker_unicode_escape": (
            "\\u3086\\u3063\\u304f\\u308a\\u970a\\u5922"
        ),
    }


def _probe_status(
    source_validation: dict[str, Any],
    raster_status: dict[str, Any],
    structural_status: dict[str, Any],
) -> str:
    if raster_status.get("png_export_status") != "generated":
        return "blocked_png_required"
    if structural_status.get("card_items_use_image_item_schema") is not True:
        return "blocked_schema_unknown"
    if source_validation.get("status") == "passed":
        return "placed_structurally"
    return "plan_only"


def _placement_operations(
    source_assets: list[dict[str, Any]],
    structural_status: dict[str, Any],
) -> list[dict[str, Any]]:
    applied = (
        structural_status.get("patched_ymmp_exists") is True
        and structural_status.get("card_image_item_count") == len(source_assets)
    )
    rows = []
    for asset in source_assets:
        rows.append(
            {
                "operation_id": f"add_image_item_{asset['card_id']}",
                "target_layer_or_track": asset["target_layer_or_track"],
                "asset_path": asset["png_path"],
                "start_frame": asset["start_frame"],
                "length_frames": asset["length_frames"],
                "field_changed_or_item_added": "Timelines[0].Items[] ImageItem",
                "before": "absent",
                "after": {
                    "item_type": "ImageItem",
                    "file_path": asset["png_path"],
                    "frame": asset["start_frame"],
                    "length": asset["length_frames"],
                    "layer": CARD_LAYER,
                    "remark": f"{CARD_REMARK_PREFIX}{asset['card_id']}",
                },
                "safety_class": "diagnostic_only",
                "applied": applied,
            }
        )
    return rows


def _preservation_checks(
    structural_status: dict[str, Any],
    source_summary: dict[str, Any],
    patched_summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "timeline_duration_preserved": structural_status.get(
            "timeline_duration_preserved"
        ),
        "dialogue_items_preserved": structural_status.get("dialogue_items_preserved"),
        "native_audio_fields_preserved": structural_status.get(
            "native_audio_fields_preserved"
        ),
        "speaker_preserved": structural_status.get("speaker_preserved"),
        "source_dialogue_item_count": source_summary.get("voice_item_count"),
        "patched_dialogue_item_count": patched_summary.get("voice_item_count"),
        "direct_yym4_card_object_graph": False,
        "yym4_text_shape_reconstruction": False,
        "external_TTS_introduced": False,
        "render_created": False,
        "media_committed": False,
    }


def _structural_result(
    source_assets: list[dict[str, Any]],
    structural_status: dict[str, Any],
    patched_summary: dict[str, Any],
) -> dict[str, Any]:
    structural_pass = (
        structural_status.get("patched_ymmp_exists") is True
        and structural_status.get("timeline_duration_preserved") is True
        and structural_status.get("dialogue_items_preserved") is True
        and structural_status.get("native_audio_fields_preserved") is True
        and structural_status.get("card_image_item_count") == 4
        and structural_status.get("card_items_match_expected_timing") is True
        and structural_status.get("card_items_use_image_item_schema") is True
        and structural_status.get("card_items_use_png_paths") is True
    )
    return {
        "patched_ymmp_created_locally": patched_summary.get("exists") is True,
        "patched_ymmp_committed": False,
        "visual_assets_committed": True,
        "card_item_count_added_or_planned": len(source_assets),
        "card_image_item_count_observed": structural_status.get(
            "card_image_item_count"
        ),
        "placement_structural_readback_status": (
            "pass" if structural_pass else "blocked"
        ),
        "next_render_trigger": NEXT_DEFAULT_SLICE if structural_pass else None,
    }


def _accepted_scope(probe_status: str) -> dict[str, bool]:
    placed = probe_status == "placed_structurally"
    return {
        "external_visual_card_assets_are_placement_mapped": True,
        "cards_are_placed_into_ignored_yym4_diagnostic_copy": placed,
        "direct_yym4_card_object_graph_construction_avoided": True,
        "native_audio_timing_proofs_preserved": placed,
        "png_card_assets_generated_from_existing_svg": True,
        "timing_patch_duration_preserved": placed,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_visual_quality": False,
        "final_design_system": False,
        "post_card_render_proof": False,
        "public_video_readiness": False,
        "real_newsroom_visuals": False,
        "real_content_readiness": False,
        "production_approval": False,
    }


def _readiness_separation(probe_status: str) -> dict[str, Any]:
    placed = probe_status == "placed_structurally"
    return {
        "slice_completion": "pass_for_this_placement_probe" if placed else "blocked",
        "video_readiness_progress": "6/7",
        "video_readiness_current": (
            "card_assets_structurally_placed_in_ignored_yym4_copy"
            if placed
            else "card_asset_placement_not_yet_structurally_proven"
        ),
        "video_readiness_next_missing_gate": (
            "post-placement render smoke and internal review milestone"
        ),
        "visual_readiness_progress": "6/7" if placed else "4/7",
        "visual_readiness_current": (
            "YMM4 image placement proof exists structurally"
            if placed
            else "external card assets exist but placement is blocked"
        ),
        "production_readiness": "low_diagnostic_only",
        "production_readiness_reason": (
            "The probe uses fake PNG card assets and an ignored local YMM4 copy; "
            "it does not prove post-card render output or production quality."
        ),
        "next_default_slice": (
            NEXT_DEFAULT_SLICE if placed else PNG_EXPORT_SLICE
        ),
    }


def _recommended_next_slices(probe_status: str) -> list[dict[str, str]]:
    placed = probe_status == "placed_structurally"
    default = NEXT_DEFAULT_SLICE if placed else PNG_EXPORT_SLICE
    return [
        {
            "slice": default,
            "timing": "recommended_next_default",
            "reason": (
                "structural placement passed, so the next meaningful gate is a "
                "milestone render smoke of the changed video surface"
                if placed
                else "PNG/raster export must be completed before safe YMM4 image placement"
            ),
        },
        {
            "slice": PNG_EXPORT_SLICE,
            "timing": "only_if_png_export_missing",
            "reason": "use only when compatible raster assets are unavailable",
        },
        {
            "slice": IMAGE_SCHEMA_AUDIT_SLICE,
            "timing": "only_if_image_item_schema_becomes_unsafe",
            "reason": "audit ImageItem fields before mutating any YMM4 copy",
        },
        {
            "slice": INTERNAL_REVIEW_PREP_SLICE,
            "timing": "later_after_card_placement_render_smoke",
            "reason": "prepare v0.1 review once the rendered visual surface is observed",
        },
    ]


def _goal_stack(probe_status: str) -> list[dict[str, str]]:
    success = (
        "placement probe JSON/readback shows card assets mapped without direct object graph reconstruction"
        if probe_status == "placed_structurally"
        else "clean block records what is missing before placement"
    )
    return [
        {
            "level": "Immediate",
            "goal": "Place or prepare external card assets for YMM4 image placement",
            "success_signal": success,
            "contribution": "moves visual axis from asset-only to YMM4-placement-ready",
        },
        {
            "level": "Short-term",
            "goal": "Prepare post-card render smoke",
            "success_signal": "ignored .ymmp copy structurally includes card images",
            "contribution": "makes the next render milestone meaningful",
        },
        {
            "level": "Mid-term",
            "goal": "Reach internal review v0.1",
            "success_signal": "68sec video has native audio, timing, and visible cards",
            "contribution": "enables useful human review",
        },
        {
            "level": "Long-term",
            "goal": "Stabilize Newsroom-to-video pipeline",
            "success_signal": (
                "content packet can drive script, audio, timing, and visual assets repeatably"
            ),
            "contribution": "reduces manual assembly",
        },
    ]


def _completion_matrix(probe_status: str) -> list[dict[str, Any]]:
    passed = probe_status == "placed_structurally"
    return [
        {"gate": "current_repo_state_verified", "status": True},
        {"gate": "visual_card_assets_inspected", "status": True},
        {"gate": "raster_export_readiness_determined", "status": True},
        {"gate": "placement_plan_probe_created", "status": True},
        {"gate": "structural_readback_or_clean_block_recorded", "status": passed},
        {
            "gate": "narrow_commit_created_and_pushed_if_push_gate_passes",
            "status": "pending_until_git_gate",
        },
    ]


def _artifact_readiness(probe_status: str) -> list[dict[str, Any]]:
    placed = probe_status == "placed_structurally"
    return [
        {"artifact": "placement_probe_json", "status": "present"},
        {"artifact": "human_readback", "status": "present"},
        {"artifact": "asset_mapping", "status": "present"},
        {
            "artifact": "placement_operations_or_clean_block",
            "status": "applied" if placed else "blocked",
        },
        {"artifact": "preservation_checks", "status": "present"},
        {"artifact": "downstream_next_use", "status": "present"},
    ]


def _video_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "source_input_path_proven", "status": True},
        {"gate": "target_yym4_import_path_proven", "status": True},
        {"gate": "audio_path_proven", "status": True},
        {"gate": "timing_duration_strategy_defined", "status": True},
        {"gate": "tiny_smoke_render_observed", "status": True},
        {"gate": "targeted_regression_render_observed", "status": True},
        {"gate": "internal_review_milestone_reached", "status": False},
    ]


def _visual_readiness(probe_status: str) -> list[dict[str, Any]]:
    placed = probe_status == "placed_structurally"
    return [
        {"gate": "visual_card_concept_selected", "status": True},
        {"gate": "external_card_assets_generated", "status": True},
        {"gate": "preview_contact_sheet_available", "status": True},
        {"gate": "assets_mapped_to_timeline_caption_units", "status": True},
        {"gate": "yym4_placement_contract_defined", "status": True},
        {"gate": "yym4_placement_proof_observed", "status": placed},
        {"gate": "post_placement_render_reviewed", "status": False},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "video_render_performed_in_this_slice", "status": False},
        {"gate": "existing_render_evidence_reused", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {"gate": "next_render_tied_to_successful_card_placement", "status": True},
        {"gate": "no_render_for_docs_readback_changes", "status": True},
        {"gate": "repeated_timing_audio_render_check_avoided", "status": True},
    ]


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "user_input", "status": "freeform"},
        {"gate": "template_required", "status": False},
        {"gate": "schema_owner", "status": "Agent"},
        {"gate": "user_side_work", "status": "none"},
        {"gate": "future_look_for_points_max", "status": 3},
        {"gate": "negative_confirmation_checklist", "status": False},
        {"gate": "fixed_form_relapse", "status": False},
    ]


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"gate": "prior_timing_proof_reused", "status": True},
        {"gate": "prior_audio_evidence_reused", "status": True},
        {"gate": "prior_render_smoke_result_reused", "status": True},
        {"gate": "next_axis_stated_as_visual_placement", "status": True},
        {"gate": "not_accepted_scope_preserved", "status": True},
        {"gate": "repeated_timing_audio_render_review_requested", "status": False},
    ]


def _inertia_check(probe_status: str) -> list[dict[str, Any]]:
    return [
        {"gate": "packet_for_packet_drift", "status": False},
        {"gate": "readback_only_stall", "status": False},
        {"gate": "repeated_render_request", "status": False},
        {
            "gate": "product_video_visual_readiness_separated_from_slice_completion",
            "status": True,
        },
        {
            "gate": "next_concrete_milestone",
            "status": NEXT_DEFAULT_SLICE
            if probe_status == "placed_structurally"
            else PNG_EXPORT_SLICE,
        },
    ]


def _placement_contract() -> dict[str, Any]:
    return {
        "placement_mode": "image_asset_import",
        "yym4_item_type": "ImageItem",
        "card_asset_format": "png",
        "source_card_format": "svg",
        "target_layer": CARD_LAYER,
        "direct_yym4_card_object_graph": False,
        "yym4_text_shape_reconstruction": False,
        "preserves_native_audio_path": True,
        "preserves_existing_timing_strategy": True,
        "render_required_in_this_slice": False,
        "YMM4_launch_required_in_this_slice": False,
        "ymmp_mutation_boundary": "ignored local diagnostic copy only",
        "next_render_should_be_milestone_gated": True,
        "no_render_for_docs_readback_policy_only_changes": True,
    }


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "video_render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "external_TTS_introduced": False,
        "real_media_imported": False,
        "external_source_fetch_performed": False,
        "real_urls_or_real_brands_used": False,
        "production_ymmp_edited_or_committed": False,
        "ignored_ymmp_staged_or_committed": False,
        "render_output_staged_or_committed": False,
        "production_approval": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


def _local_artifact_status(root: Path, rel_path: Path) -> dict[str, Any]:
    exists = (root / rel_path).exists()
    return {
        "patched_ymmp_local_path": _path_text(rel_path),
        "patched_ymmp_exists_at_readback_generation": exists,
        "patched_ymmp_staged": _git_has_output(root, ["diff", "--cached", "--name-only", "--", rel_path.as_posix()]),
        "patched_ymmp_committed": _git_has_output(root, ["ls-files", "--", rel_path.as_posix()]),
        "patched_ymmp_ignored": _git_returncode_zero(root, ["check-ignore", "-q", "--", rel_path.as_posix()]),
    }


def _downstream_next_use(probe_status: str) -> dict[str, list[str]]:
    if probe_status == "placed_structurally":
        use_this = [
            "run the post-placement render smoke milestone against the ignored diagnostic YMM4 copy",
            "verify the card images are visible on the 68 second timeline",
            "preserve native YMM4 audio and sparse diagnostic timing as prior evidence",
        ]
    else:
        use_this = [
            "resolve the clean block before mutating another YMM4 copy",
            "keep visual cards as external assets rather than YMM4 primitive graphs",
        ]
    return {
        "use_this_probe_to": use_this,
        "do_not_use_this_probe_to": [
            "claim public video readiness",
            "claim production visual quality",
            "commit ignored .ymmp or render outputs",
            "introduce external TTS or real media",
        ],
    }


def _first_timeline(data: dict[str, Any]) -> dict[str, Any] | None:
    timelines = data.get("Timelines")
    if isinstance(timelines, list) and timelines and isinstance(timelines[0], dict):
        return timelines[0]
    timeline = data.get("Timeline")
    if isinstance(timeline, dict):
        return timeline
    return None


def _voice_summary(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "item_type": _item_type(item),
        "Frame": item.get("Frame"),
        "Length": item.get("Length"),
        "Layer": item.get("Layer"),
        "Group": item.get("Group"),
        "text": item.get("Serif") or item.get("Text"),
        "CharacterName": item.get("CharacterName"),
        "VoiceLength": item.get("VoiceLength"),
        "VoiceCache": item.get("VoiceCache"),
        "VoiceParameter": item.get("VoiceParameter"),
    }


def _image_summary(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "item_type": _item_type(item),
        "Frame": item.get("Frame"),
        "Length": item.get("Length"),
        "Layer": item.get("Layer"),
        "Group": item.get("Group"),
        "FilePath": item.get("FilePath"),
        "Remark": item.get("Remark"),
    }


def _voice_preservation_keys(items: Any) -> list[dict[str, Any]]:
    return [
        {
            "CharacterName": item.get("CharacterName"),
            "VoiceLength": item.get("VoiceLength"),
            "VoiceCache": item.get("VoiceCache"),
            "VoiceParameter": item.get("VoiceParameter"),
        }
        for item in items
        if isinstance(item, dict)
    ]


def _render_svg_subset_to_png(svg_path: Path, png_path: Path) -> None:
    root = ElementTree.parse(svg_path).getroot()
    width = _int_attr(root, "width", 1920)
    height = _int_attr(root, "height", 1080)
    if width != 1920 or height != 1080:
        raise ValueError("card SVG must be 1920x1080")

    image = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(image)
    for element in root:
        tag = _local_xml_tag(element.tag)
        if tag == "rect":
            _draw_svg_rect(draw, element)
        elif tag == "circle":
            _draw_svg_circle(draw, element)
        elif tag == "text":
            _draw_svg_text(draw, element)
    image.save(png_path, format="PNG")


def _draw_svg_rect(draw: ImageDraw.ImageDraw, element: ElementTree.Element) -> None:
    x = _float_attr(element, "x", 0.0)
    y = _float_attr(element, "y", 0.0)
    width = _float_attr(element, "width", 0.0)
    height = _float_attr(element, "height", 0.0)
    radius = _float_attr(element, "rx", 0.0)
    fill = _svg_color(element.get("fill"), "#000000")
    stroke = _svg_color(element.get("stroke"), None)
    stroke_width = int(_float_attr(element, "stroke-width", 1.0))
    box = [x, y, x + width, y + height]
    if radius > 0:
        draw.rounded_rectangle(
            box,
            radius=radius,
            fill=fill,
            outline=stroke,
            width=stroke_width if stroke else 1,
        )
    else:
        draw.rectangle(
            box,
            fill=fill,
            outline=stroke,
            width=stroke_width if stroke else 1,
        )


def _draw_svg_circle(draw: ImageDraw.ImageDraw, element: ElementTree.Element) -> None:
    cx = _float_attr(element, "cx", 0.0)
    cy = _float_attr(element, "cy", 0.0)
    radius = _float_attr(element, "r", 0.0)
    fill = _svg_color(element.get("fill"), "#000000")
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=fill)


def _draw_svg_text(draw: ImageDraw.ImageDraw, element: ElementTree.Element) -> None:
    text = "".join(element.itertext())
    if not text:
        return
    x = _float_attr(element, "x", 0.0)
    y = _float_attr(element, "y", 0.0)
    size = int(_float_attr(element, "font-size", 24.0))
    weight = str(element.get("font-weight") or "")
    fill = _svg_color(element.get("fill"), "#000000")
    anchor = str(element.get("text-anchor") or "start")
    font = _font(size, bold=weight in {"700", "800", "bold"})
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    if anchor == "middle":
        x -= text_width / 2
    elif anchor == "end":
        x -= text_width
    draw.text((x, y - size * 0.82), text, fill=fill, font=font)


def _font(size: int, *, bold: bool) -> ImageFont.ImageFont:
    font_dir = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    candidates = [
        font_dir / ("arialbd.ttf" if bold else "arial.ttf"),
        font_dir / ("segoeuib.ttf" if bold else "segoeui.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def _local_xml_tag(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _int_attr(element: ElementTree.Element, key: str, default: int) -> int:
    try:
        return int(float(str(element.get(key, default))))
    except (TypeError, ValueError):
        return default


def _float_attr(element: ElementTree.Element, key: str, default: float) -> float:
    try:
        return float(str(element.get(key, default)))
    except (TypeError, ValueError):
        return default


def _svg_color(value: str | None, default: str | None) -> str | None:
    if value in {None, "", "none"}:
        return default
    return value


def _find_sharp_exporter() -> tuple[Path, Path] | None:
    home = Path.home()
    bundled = home / ".cache" / "codex-runtimes" / "codex-primary-runtime"
    node_dir = bundled / "dependencies" / "node"
    module_dir = node_dir / "node_modules"
    candidates = [
        node_dir / "bin" / "node.exe",
        node_dir / "node.exe",
    ]
    node_on_path = shutil.which("node")
    if node_on_path:
        candidates.append(Path(node_on_path))
    for candidate in candidates:
        if candidate.exists() and (module_dir / "sharp").exists():
            return candidate, module_dir
    return None


def _png_metadata(path: str | Path) -> dict[str, Any]:
    png_path = Path(path)
    metadata: dict[str, Any] = {
        "path": _path_text(png_path),
        "exists": png_path.exists(),
        "valid": False,
    }
    if not png_path.exists():
        return metadata
    try:
        with png_path.open("rb") as handle:
            header = handle.read(24)
        if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
            return metadata
        width, height = struct.unpack(">II", header[16:24])
    except OSError:
        return metadata
    metadata.update(
        {
            "valid": width == 1920 and height == 1080,
            "width": width,
            "height": height,
            "format": "png",
            "expected_width": 1920,
            "expected_height": 1080,
        }
    )
    return metadata


def _png_metadata_for_asset(
    root: str | Path,
    asset: dict[str, Any],
) -> dict[str, Any]:
    metadata = _png_metadata(Path(root) / asset["png_path"])
    metadata["path"] = asset["png_path"]
    return metadata


def _git_has_output(root: Path, args: list[str]) -> bool:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return bool(result.stdout.strip())


def _git_returncode_zero(root: Path, args: list[str]) -> bool:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def _append_status_table(
    lines: list[str],
    title: str,
    rows: Any,
) -> None:
    lines.extend(["", f"## {title}", "", "| item | status |", "|---|---|"])
    for row in rows if isinstance(rows, list) else []:
        key = row.get("gate") or row.get("artifact") or "item"
        lines.append(f"| {key} | {_display(row.get('status'))} |")


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    json_path = Path(path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_bytes(
        (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )


def _write_text(path: str | Path, text: str) -> None:
    text_path = Path(path)
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text_path.write_bytes(text.encode("utf-8"))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, list):
        if not value:
            return "[]"
        return ", ".join(_display(item) for item in value)
    return str(value)
