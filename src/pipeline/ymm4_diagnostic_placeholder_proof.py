"""Build an Episode 002 diagnostic-only YMM4 placeholder proof.

The source project must be a clean YMM4 CSV import containing the expected
nine VoiceItems.  The builder preserves those VoiceItem objects and appends
one neutral ImageItem plus one independent TextItem for each of S1/S2/S3.
The generated project is intentionally local-only because current YMM4
examples require absolute asset paths.
"""

from __future__ import annotations

import binascii
import copy
import csv
import hashlib
import json
import re
import struct
import zlib
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from src.pipeline.ymmp_openability import normalize_ymmp_openability
from src.pipeline.ymm4_observation_readback_pack import (
    load_ymm4_observation_receipt,
)
from src.pipeline.ymmp_patch import (
    _build_overlay_item,
    _get_timeline_items,
    _item_type,
    load_ymmp,
    save_ymmp,
)


EPISODE_ID = "yukkuri_newsroom_content_spine_002"
ARTIFACT_ID = "episode_002_ymm4_diagnostic_placeholder_proof_v1"
MANIFEST_SCHEMA_VERSION = "ymm4_diagnostic_project_manifest.v1"
READBACK_SCHEMA_VERSION = "ymm4_diagnostic_project_readback.v1"
GUI_RECEIPT_SCHEMA_VERSION = "ymm4_diagnostic_project_gui_receipt.v1"
CSV_RECEIPT_SCHEMA_VERSION = "ymm4_gui_observation_receipt.v2"

DEFAULT_OUTPUT_DIRNAME = "ymm4_diagnostic_placeholder_proof"
PROJECT_FILENAME = "episode_002_diagnostic_placeholder.local.ymmp"
MANIFEST_FILENAME = "diagnostic_project_manifest.json"
READBACK_FILENAME = "diagnostic_project_readback.json"
RECEIPT_FILENAME = "diagnostic_project_receipt.json"
README_FILENAME = "README_DIAGNOSTIC_PLACEHOLDER_PROOF.md"
ASSET_PATH = Path("assets/diagnostic_placeholder.png")

DERIVED_CSV = Path("ymm4_import_ready_pack/derived_yymm4_import.csv")
CANONICAL_CSV = Path(
    "transcript_substitution_readiness/regenerated_draft_yymm4.csv"
)
CUE_MAP = Path("ymm4_import_ready_pack/edit_slice_to_ymm4_cue_map.json")
PROFILE = Path(
    "ymm4_character_alias_profiles/ymm4_4_53_0_9_yukkuri_characters_v1.json"
)

SCENE_ROWS = (("S1", 0, 2), ("S2", 2, 4), ("S3", 4, 9))
EXPECTED_CHARACTER_COUNTS = {"ゆっくり霊夢": 3, "ゆっくり魔理沙": 6}
LABEL_TEMPLATE = "{scene_id} | DIAGNOSTIC | NOT FINAL | SAMPLE / PLACEHOLDER"
REMARK_PREFIX = "episode002:diagnostic_placeholder:"
PNG_WIDTH = 1920
PNG_HEIGHT = 1080


def build_ymm4_diagnostic_placeholder_proof(
    *,
    package_dir: str | Path,
    source_ymmp: str | Path,
    csv_gate_receipt: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = ARTIFACT_ID,
) -> dict[str, Any]:
    """Build the local project plus sanitized, tracked proof artifacts."""
    package = Path(package_dir)
    source = Path(source_ymmp)
    receipt_path = Path(csv_gate_receipt)
    output = Path(output_dir) if output_dir is not None else package / DEFAULT_OUTPUT_DIRNAME
    output.mkdir(parents=True, exist_ok=True)
    ignore_path = output / ".gitignore"
    if not ignore_path.exists():
        _write_text(ignore_path, "*.local.ymmp\n")
    asset_path = output / ASSET_PATH
    project_path = output / PROJECT_FILENAME
    if source.resolve() == project_path.resolve():
        raise ValueError("SOURCE_PROJECT_MUST_DIFFER_FROM_DIAGNOSTIC_TARGET")

    existing_receipt_path = output / RECEIPT_FILENAME
    if existing_receipt_path.exists():
        existing_receipt = _load_json(existing_receipt_path)
        if existing_receipt.get("status") in {"passed", "blocked"}:
            existing_manifest = _load_json(output / MANIFEST_FILENAME)
            if existing_manifest.get("artifact_id") != artifact_id:
                raise ValueError("EXISTING_DIAGNOSTIC_PROOF_ARTIFACT_ID_MISMATCH")
            validation = validate_ymm4_diagnostic_placeholder_proof(
                proof_dir=output,
                package_dir=package,
                source_ymmp=source,
                csv_gate_receipt=receipt_path,
            )
            if validation["status"] != "passed":
                raise ValueError(
                    "PASSED_DIAGNOSTIC_GUI_RECEIPT_PRECHECK_FAILED: "
                    + ", ".join(validation["errors"])
                )
            return {
                "status": (
                    "diagnostic_placeholder_proof_observed"
                    if existing_receipt.get("status") == "passed"
                    else "diagnostic_placeholder_proof_gui_blocked"
                ),
                "output_dir": str(output),
                "project_path": str(project_path),
                "project_commit_disposition": "local_only_not_committed",
                "manifest": _load_json(output / MANIFEST_FILENAME),
                "readback": _load_json(output / READBACK_FILENAME),
                "validation": validation,
            }

    inputs = _load_and_validate_inputs(package, source, receipt_path)
    source_project = inputs["source_project"]
    source_voice_items = inputs["voice_items"]
    source_voice_digests = [_json_sha256(item) for item in source_voice_items]
    scene_specs = _derive_scene_specs(source_voice_items)

    _write_neutral_png(asset_path)
    patched = copy.deepcopy(source_project)
    patched.pop("Tools", None)
    patched.pop("ToolStates", None)
    timeline = _first_timeline(patched)
    items = _get_timeline_items(patched)
    base_max_layer = max(
        [int(timeline.get("MaxLayer", 0) or 0)]
        + [int(item.get("Layer", 0) or 0) for item in items]
    )
    image_layer = base_max_layer + 1
    text_layer = base_max_layer + 2
    absolute_asset_path = str(asset_path.resolve())
    for scene in scene_specs:
        items.append(
            _make_image_item(
                scene,
                asset_path=absolute_asset_path,
                layer=image_layer,
            )
        )
        items.append(_make_text_item(scene, layer=text_layer))
    timeline["MaxLayer"] = text_layer
    patched["FilePath"] = str(project_path.resolve())
    normalize_ymmp_openability(patched)
    save_ymmp(patched, project_path)

    readback = _build_readback(
        artifact_id=artifact_id,
        project_path=project_path,
        source_voice_digests=source_voice_digests,
        source_timeline_length=int(_first_timeline(source_project).get("Length", 0) or 0),
        expected_rows=inputs["derived_rows"],
        scene_specs=scene_specs,
        asset_path=asset_path,
    )
    if readback["status"] != "structural_pass":
        raise ValueError(
            "DIAGNOSTIC_PROJECT_READBACK_FAILED: "
            + ", ".join(readback["failed_checks"])
        )

    source_records = _source_records(package, source, receipt_path)
    manifest = _build_manifest(
        artifact_id=artifact_id,
        project_path=project_path,
        asset_path=asset_path,
        scene_specs=scene_specs,
        readback=readback,
        source_records=source_records,
        source_environment=inputs["source_environment"],
    )
    _write_json(output / MANIFEST_FILENAME, manifest)
    _write_json(output / READBACK_FILENAME, readback)
    _write_text(output / README_FILENAME, _render_readme(manifest))
    _write_or_preserve_gui_receipt(
        output / RECEIPT_FILENAME,
        manifest=manifest,
        readback=readback,
    )
    validation = validate_ymm4_diagnostic_placeholder_proof(
        proof_dir=output,
        package_dir=package,
        source_ymmp=source,
        csv_gate_receipt=receipt_path,
    )
    if validation["status"] != "passed":
        raise ValueError(
            "DIAGNOSTIC_PROOF_VALIDATION_FAILED: " + ", ".join(validation["errors"])
        )
    return {
        "status": "diagnostic_placeholder_proof_ready",
        "output_dir": str(output),
        "project_path": str(project_path),
        "project_commit_disposition": "local_only_not_committed",
        "manifest": manifest,
        "readback": readback,
        "validation": validation,
    }


def build_gui_observation_receipt(
    *,
    proof_dir: str | Path,
    observed_at: str,
    yymm4_version: str,
    observations: dict[str, Any],
    safety: dict[str, Any],
    application_close_state: str,
    screenshot: str | None = None,
) -> dict[str, Any]:
    """Bind caller-supplied GUI observations to the generated proof hashes."""
    root = Path(proof_dir)
    manifest = _load_json(root / MANIFEST_FILENAME)
    readback = _load_json(root / READBACK_FILENAME)
    project = root / PROJECT_FILENAME
    if readback.get("status") != "structural_pass":
        raise ValueError("GUI_RECEIPT_REQUIRES_STRUCTURAL_READBACK_PASS")
    if _sha256(project) != readback.get("project_sha256"):
        raise ValueError("GUI_RECEIPT_PROJECT_HASH_MISMATCH")
    receipt = {
        "schema_version": GUI_RECEIPT_SCHEMA_VERSION,
        "artifact_id": f"{manifest.get('artifact_id')}_gui_observation",
        "episode_id": EPISODE_ID,
        "status": "passed",
        "result": "passed",
        "observed_at": observed_at,
        "observed_by_environment": {
            "application": "YukkuriMovieMaker",
            "yymm4_version": yymm4_version,
            "observation_mode": "actual_gui_reopen",
        },
        "application_close_state": application_close_state,
        "project": {
            "repo_relative_local_path": PROJECT_FILENAME,
            "sha256": readback["project_sha256"],
            "commit_disposition": "local_only_not_committed_absolute_asset_reference",
        },
        "evidence_hashes": _receipt_evidence_hashes(root, manifest),
        "observations": copy.deepcopy(observations),
        "screenshot": _screenshot_record(root, screenshot),
        "safety": copy.deepcopy(safety),
        "next_gate": "supervisor_next_slice_decision",
    }
    validate_gui_observation_receipt(receipt, proof_dir=root)
    return receipt


def build_blocked_gui_observation_receipt(
    *,
    proof_dir: str | Path,
    observed_at: str,
    yymm4_version: str,
    blocker: dict[str, Any],
    safety: dict[str, Any],
    application_close_state: str,
    screenshot: str | None = None,
) -> dict[str, Any]:
    """Bind an evidence-backed GUI-open blocker to the generated proof."""
    root = Path(proof_dir)
    manifest = _load_json(root / MANIFEST_FILENAME)
    readback = _load_json(root / READBACK_FILENAME)
    project = root / PROJECT_FILENAME
    if readback.get("status") != "structural_pass":
        raise ValueError("GUI_RECEIPT_REQUIRES_STRUCTURAL_READBACK_PASS")
    if _sha256(project) != readback.get("project_sha256"):
        raise ValueError("GUI_RECEIPT_PROJECT_HASH_MISMATCH")
    receipt = {
        "schema_version": GUI_RECEIPT_SCHEMA_VERSION,
        "artifact_id": f"{manifest.get('artifact_id')}_gui_observation",
        "episode_id": EPISODE_ID,
        "status": "blocked",
        "result": "blocked",
        "observed_at": observed_at,
        "observed_by_environment": {
            "application": "YukkuriMovieMaker",
            "yymm4_version": yymm4_version,
            "observation_mode": "actual_gui_reopen_attempt",
        },
        "application_close_state": application_close_state,
        "project": {
            "repo_relative_local_path": PROJECT_FILENAME,
            "sha256": readback["project_sha256"],
            "commit_disposition": "local_only_not_committed_absolute_asset_reference",
        },
        "evidence_hashes": _receipt_evidence_hashes(root, manifest),
        "observations": {},
        "blocker": copy.deepcopy(blocker),
        "screenshot": _screenshot_record(root, screenshot),
        "safety": copy.deepcopy(safety),
        "next_gate": "bounded_diagnostic_project_observation",
    }
    validate_gui_observation_receipt(receipt, proof_dir=root)
    return receipt


def validate_gui_observation_receipt(
    receipt: dict[str, Any],
    *,
    proof_dir: str | Path,
) -> None:
    """Validate the narrow diagnostic GUI evidence contract."""
    root = Path(proof_dir)
    if receipt.get("schema_version") != GUI_RECEIPT_SCHEMA_VERSION:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_SCHEMA_MISMATCH")
    if receipt.get("episode_id") != EPISODE_ID:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_EPISODE_MISMATCH")
    if receipt.get("status") not in {"ready_for_gui_observation", "passed", "blocked"}:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_STATUS_INVALID")
    base_keys = {
        "schema_version",
        "artifact_id",
        "episode_id",
        "status",
        "result",
        "observed_at",
        "application_close_state",
        "project",
        "evidence_hashes",
        "observations",
        "screenshot",
        "safety",
        "next_gate",
    }
    expected_keys = set(base_keys)
    if receipt.get("status") in {"passed", "blocked"}:
        expected_keys.add("observed_by_environment")
    if receipt.get("status") == "blocked":
        expected_keys.add("blocker")
    if set(receipt) != expected_keys:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_FIELD_SET_MISMATCH")
    manifest = _load_json(root / MANIFEST_FILENAME)
    readback = _load_json(root / READBACK_FILENAME)
    if manifest.get("status") != "generated_structural_pass" or manifest.get(
        "diagnostic_only"
    ) is not True:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_MANIFEST_NOT_STRUCTURAL_PASS")
    checks = _dict(readback.get("checks"))
    if (
        readback.get("status") != "structural_pass"
        or readback.get("failed_checks") != []
        or not checks
        or any(value is not True for value in checks.values())
    ):
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_READBACK_NOT_STRUCTURAL_PASS")
    expected_project = {
        "repo_relative_local_path": PROJECT_FILENAME,
        "sha256": readback.get("project_sha256"),
        "commit_disposition": "local_only_not_committed_absolute_asset_reference",
    }
    if receipt.get("artifact_id") != f"{manifest.get('artifact_id')}_gui_observation":
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_ARTIFACT_ID_MISMATCH")
    if _dict(receipt.get("project")) != expected_project:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_PROJECT_BINDING_MISMATCH")
    if _dict(receipt.get("evidence_hashes")) != _receipt_evidence_hashes(root, manifest):
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_EVIDENCE_HASH_MISMATCH")
    if _dict(receipt.get("evidence_hashes")).get("project_sha256") != _dict(
        receipt.get("project")
    ).get("sha256"):
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_PROJECT_EVIDENCE_MISMATCH")
    if _dict(receipt.get("safety")) != _expected_diagnostic_safety():
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_SAFETY_MISMATCH")
    _validate_screenshot_record(root, _dict(receipt.get("screenshot")))
    if _text_has_absolute_or_uri(json.dumps(receipt, ensure_ascii=False)):
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_PRIVATE_PATH_OR_URI_PRESENT")
    if receipt.get("status") == "ready_for_gui_observation":
        if receipt.get("result") != "not_observed":
            raise ValueError("PENDING_DIAGNOSTIC_GUI_RECEIPT_RESULT_INVALID")
        if receipt.get("observed_at") is not None:
            raise ValueError("PENDING_DIAGNOSTIC_GUI_RECEIPT_TIMESTAMP_INVALID")
        if receipt.get("application_close_state") != "not_observed":
            raise ValueError("PENDING_DIAGNOSTIC_GUI_RECEIPT_APPLICATION_STATE_INVALID")
        if _dict(receipt.get("observations")):
            raise ValueError("PENDING_DIAGNOSTIC_GUI_RECEIPT_OBSERVATIONS_MUST_BE_EMPTY")
        if receipt.get("next_gate") != "bounded_diagnostic_project_observation":
            raise ValueError("PENDING_DIAGNOSTIC_GUI_RECEIPT_NEXT_GATE_INVALID")
        return
    _validate_observed_environment(receipt)
    if _dict(receipt.get("observed_by_environment")).get(
        "yymm4_version"
    ) != _dict(manifest.get("source_environment")).get("yymm4_version"):
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_YMM4_VERSION_MISMATCH")
    _validate_iso_timestamp(str(receipt.get("observed_at") or ""))
    if receipt.get("status") == "blocked":
        if receipt.get("result") != "blocked":
            raise ValueError("BLOCKED_DIAGNOSTIC_GUI_RECEIPT_RESULT_INVALID")
        if _dict(receipt.get("observations")):
            raise ValueError("BLOCKED_DIAGNOSTIC_GUI_RECEIPT_OBSERVATIONS_MUST_BE_EMPTY")
        blocker = _dict(receipt.get("blocker"))
        if set(blocker) != {"blocker_id", "detail"} or not blocker.get(
            "blocker_id"
        ) or not blocker.get("detail"):
            raise ValueError("BLOCKED_DIAGNOSTIC_GUI_RECEIPT_BLOCKER_MISSING")
        if receipt.get("application_close_state") not in {
            "left_open_after_observation_blocker",
            "closed_after_observation_blocker",
        }:
            raise ValueError("BLOCKED_DIAGNOSTIC_GUI_RECEIPT_APPLICATION_STATE_INVALID")
        if receipt.get("next_gate") != "bounded_diagnostic_project_observation":
            raise ValueError("BLOCKED_DIAGNOSTIC_GUI_RECEIPT_NEXT_GATE_INVALID")
        return
    if receipt.get("result") != "passed":
        raise ValueError("PASSED_DIAGNOSTIC_GUI_RECEIPT_RESULT_INVALID")
    if receipt.get("application_close_state") not in {
        "left_open_with_saved_diagnostic_project",
        "closed_after_observation_without_changes",
    }:
        raise ValueError("PASSED_DIAGNOSTIC_GUI_RECEIPT_APPLICATION_STATE_INVALID")
    observations = _dict(receipt.get("observations"))
    expected = {
        "opened_without_error": True,
        "unexpected_dialog_present": False,
        "VoiceItems": 9,
        "character_counts": EXPECTED_CHARACTER_COUNTS,
        "linked_subtitles_preserved": True,
        "ImageItems": 3,
        "independent_TextItems": 3,
        "placeholder_is_explicitly_non_final": True,
        "render_or_export_performed": False,
        "scene_labels_readable": [
            LABEL_TEMPLATE.format(scene_id=scene_id)
            for scene_id, _, _ in SCENE_ROWS
        ],
    }
    if observations != expected:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_OBSERVATION_MISMATCH")
    if receipt.get("next_gate") != "supervisor_next_slice_decision":
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_NEXT_GATE_INVALID")


def write_gui_observation_receipt(receipt: dict[str, Any], proof_dir: str | Path) -> Path:
    validate_gui_observation_receipt(receipt, proof_dir=proof_dir)
    path = Path(proof_dir) / RECEIPT_FILENAME
    _write_json(path, receipt)
    return path


def _load_and_validate_inputs(
    package: Path,
    source: Path,
    receipt_path: Path,
) -> dict[str, Any]:
    required = [package / DERIVED_CSV, package / CANONICAL_CSV, package / CUE_MAP, package / PROFILE]
    missing = [str(path) for path in [source, receipt_path, *required] if not path.exists()]
    if missing:
        raise FileNotFoundError("DIAGNOSTIC_PROOF_INPUT_MISSING: " + ", ".join(missing))
    receipt = load_ymm4_observation_receipt(receipt_path)
    if receipt.get("schema_version") != CSV_RECEIPT_SCHEMA_VERSION:
        raise ValueError("CSV_GATE_RECEIPT_MUST_BE_V2")
    safety = _dict(receipt.get("safety"))
    if not (
        safety.get("application_closed_without_saving") is False
        and safety.get("application_left_open_for_authorized_diagnostic_project") is True
        and safety.get("ymmp_saved_or_written") is False
    ):
        raise ValueError("CSV_GATE_RECEIPT_MUST_RECORD_AUTHORIZED_CONTINUATION_CHECKPOINT")
    derived_rows = _load_csv_rows(package / DERIVED_CSV)
    canonical_rows = _load_csv_rows(package / CANONICAL_CSV)
    if len(derived_rows) != 9 or len(canonical_rows) != 9:
        raise ValueError("EPISODE_002_CSV_MUST_HAVE_9_ROWS")
    if [text for _, text in derived_rows] != [text for _, text in canonical_rows]:
        raise ValueError("CANONICAL_AND_DERIVED_TEXT_ORDER_MISMATCH")
    if str(receipt.get("source_csv_sha256") or "").upper() != _sha256(package / DERIVED_CSV):
        raise ValueError("CSV_GATE_RECEIPT_DERIVED_HASH_MISMATCH")
    if str(receipt.get("canonical_source_csv_sha256") or "").upper() != _sha256(package / CANONICAL_CSV):
        raise ValueError("CSV_GATE_RECEIPT_CANONICAL_HASH_MISMATCH")
    package_prefix = f"production_pilots/{package.name}/"
    profile = _load_json(package / PROFILE)
    expected_receipt_fields = {
        "episode_id": EPISODE_ID,
        "observation_contract": "ymm4_csv_import_gate.v1",
        "source_csv": package_prefix + DERIVED_CSV.as_posix(),
        "canonical_source_csv": package_prefix + CANONICAL_CSV.as_posix(),
        "selected_yymm4_character_profile": package_prefix + PROFILE.as_posix(),
        "prior_receipt_reference": package_prefix + "ymm4_observation_receipt_2026-07-10.json",
        "profile_id": profile.get("profile_id"),
        "next_gate": "supervisor_next_slice_decision",
    }
    mismatches = [
        field
        for field, expected in expected_receipt_fields.items()
        if receipt.get(field) != expected
    ]
    if mismatches:
        raise ValueError("CSV_GATE_RECEIPT_IDENTITY_MISMATCH:" + ",".join(mismatches))
    receipt_version = str(
        _dict(receipt.get("observed_by_environment")).get("yymm4_version") or ""
    )
    profile_version = str(
        _dict(profile.get("observed_environment")).get("yymm4_version") or ""
    )
    if not receipt_version or receipt_version != profile_version:
        raise ValueError("CSV_GATE_RECEIPT_PROFILE_YMM4_VERSION_MISMATCH")

    source_project = load_ymmp(source)
    timelines = source_project.get("Timelines")
    if (
        not isinstance(timelines, list)
        or len(timelines) != 1
        or source_project.get("SelectedTimelineIndex") != 0
    ):
        raise ValueError("SOURCE_PROJECT_MUST_HAVE_ONE_SELECTED_TIMELINE")
    items = _get_timeline_items(source_project)
    voice_items = _ordered_voice_items(items)
    if len(voice_items) != 9:
        raise ValueError(f"SOURCE_PROJECT_VOICEITEM_COUNT_MISMATCH:{len(voice_items)}")
    if any(_item_type(item) != "VoiceItem" for item in items):
        raise ValueError("SOURCE_PROJECT_MUST_BE_CLEAN_VOICEITEM_ONLY_IMPORT")
    actual_rows = [(str(item.get("CharacterName") or ""), str(item.get("Serif") or "")) for item in voice_items]
    if actual_rows != derived_rows:
        raise ValueError("SOURCE_PROJECT_VOICEITEM_TEXT_OR_CHARACTER_ORDER_MISMATCH")
    if dict(Counter(character for character, _ in actual_rows)) != EXPECTED_CHARACTER_COUNTS:
        raise ValueError("SOURCE_PROJECT_CHARACTER_COUNTS_MISMATCH")
    if any(int(item.get("Length", 0) or 0) <= 0 for item in voice_items):
        raise ValueError("SOURCE_PROJECT_VOICEITEM_LENGTH_INVALID")
    frames = [int(item.get("Frame", 0) or 0) for item in voice_items]
    if any(frame < 0 for frame in frames) or any(
        left >= right for left, right in zip(frames, frames[1:])
    ):
        raise ValueError("SOURCE_PROJECT_VOICEITEM_TIMING_ORDER_MISMATCH")
    timeline = timelines[0]
    timing = _dict(_dict(receipt.get("five_point_observations")).get("timing_order"))
    fps = _dict(timeline.get("VideoInfo")).get("FPS")
    timeline_length = timeline.get("Length")
    receipt_fps = timing.get("frame_rate")
    receipt_frames = timing.get("total_frames")
    receipt_duration = timing.get("duration_seconds")
    last_voice_end = max(
        int(item.get("Frame", 0) or 0) + int(item.get("Length", 0) or 0)
        for item in voice_items
    )
    try:
        timing_matches = (
            float(fps) == float(receipt_fps)
            and int(timeline_length) == int(receipt_frames)
            and last_voice_end == int(timeline_length)
            and abs(float(timeline_length) / float(fps) - float(receipt_duration))
            <= 1e-9
        )
    except (TypeError, ValueError, ZeroDivisionError):
        timing_matches = False
    if not timing_matches:
        raise ValueError("SOURCE_PROJECT_TIMING_RECEIPT_MISMATCH")
    return {
        "source_project": source_project,
        "voice_items": voice_items,
        "derived_rows": derived_rows,
        "receipt": receipt,
        "source_environment": {
            "yymm4_version": receipt_version,
            "profile_id": str(profile.get("profile_id") or ""),
        },
    }


def _derive_scene_specs(voice_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for index, (scene_id, start_index, end_index) in enumerate(SCENE_ROWS):
        start_frame = int(voice_items[start_index].get("Frame", 0) or 0)
        if index + 1 < len(SCENE_ROWS):
            next_start_index = SCENE_ROWS[index + 1][1]
            end_frame = int(voice_items[next_start_index].get("Frame", 0) or 0)
        else:
            last = voice_items[end_index - 1]
            end_frame = int(last.get("Frame", 0) or 0) + int(last.get("Length", 0) or 0)
        if end_frame <= start_frame:
            raise ValueError(f"SCENE_BOUNDARY_INVALID:{scene_id}")
        specs.append(
            {
                "scene_id": scene_id,
                "cue_ids": [f"csv_row_{row}" for row in range(start_index + 1, end_index + 1)],
                "start_frame": start_frame,
                "end_frame": end_frame,
                "length_frames": end_frame - start_frame,
                "timing_source": "actual_voiceitem_frames_and_next_scene_cue_boundary",
                "label": LABEL_TEMPLATE.format(scene_id=scene_id),
                "image_remark": f"{REMARK_PREFIX}{scene_id}:image",
                "text_remark": f"{REMARK_PREFIX}{scene_id}:text",
            }
        )
    return specs


def _make_image_item(scene: dict[str, Any], *, asset_path: str, layer: int) -> dict[str, Any]:
    item = _build_overlay_item(
        {
            "path": asset_path,
            "x": 0,
            "y": 0,
            "zoom": 100,
            "opacity": 100,
            "layer": layer,
            "group": 0,
        },
        frame=scene["start_frame"],
        length=scene["length_frames"],
    )
    item["Remark"] = scene["image_remark"]
    return item


def _make_text_item(scene: dict[str, Any], *, layer: int) -> dict[str, Any]:
    return {
        "$type": "YukkuriMovieMaker.Project.Items.TextItem, YukkuriMovieMaker",
        "Text": scene["label"],
        "Font": "Yu Gothic UI",
        "FontSize": _animation(34),
        "FontColor": "#FFFF66FF",
        "Style": "Normal",
        "X": _animation(-760),
        "Y": _animation(-420),
        "Z": _animation(0),
        "Opacity": _animation(100),
        "Zoom": _animation(100),
        "Rotation": _animation(0),
        "FadeIn": 0,
        "FadeOut": 0,
        "Blend": "Normal",
        "IsAlwaysOnTop": True,
        "IsZOrderEnabled": False,
        "VideoEffects": [],
        "Group": 0,
        "Frame": scene["start_frame"],
        "Layer": layer,
        "KeyFrames": {"Frames": [], "Count": 0},
        "Length": scene["length_frames"],
        "PlaybackRate": 100,
        "ContentOffset": "00:00:00",
        "Remark": scene["text_remark"],
        "IsLocked": False,
        "IsHidden": False,
    }


def _animation(value: Any) -> dict[str, Any]:
    return {
        "Values": [{"Value": value}],
        "Span": 0,
        "AnimationType": "なし",
        "Bezier": {
            "Points": [
                {
                    "Point": {"X": 0, "Y": 0},
                    "ControlPoint1": {"X": -0.3, "Y": -0.3},
                    "ControlPoint2": {"X": 0.3, "Y": 0.3},
                },
                {
                    "Point": {"X": 1, "Y": 1},
                    "ControlPoint1": {"X": -0.3, "Y": -0.3},
                    "ControlPoint2": {"X": 0.3, "Y": 0.3},
                },
            ],
            "IsQuadratic": False,
        },
    }


def _build_readback(
    *,
    artifact_id: str,
    project_path: Path,
    source_voice_digests: list[str],
    source_timeline_length: int,
    expected_rows: list[tuple[str, str]],
    scene_specs: list[dict[str, Any]],
    asset_path: Path,
) -> dict[str, Any]:
    project = load_ymmp(project_path)
    timeline = _first_timeline(project)
    items = _get_timeline_items(project)
    voice_items = _ordered_voice_items(items)
    image_items = [item for item in items if _item_type(item) == "ImageItem"]
    text_items = [item for item in items if _item_type(item) == "TextItem"]
    type_counts = dict(Counter(_item_type(item) for item in items))
    voice_digests = [_json_sha256(item) for item in voice_items]
    actual_rows = [(str(item.get("CharacterName") or ""), str(item.get("Serif") or "")) for item in voice_items]
    scene_readback = []
    for scene in scene_specs:
        image = [item for item in image_items if item.get("Remark") == scene["image_remark"]]
        text = [item for item in text_items if item.get("Remark") == scene["text_remark"]]
        scene_readback.append(
            {
                **scene,
                "ImageItem_count": len(image),
                "TextItem_count": len(text),
                "image_asset_matches": len(image) == 1
                and str(image[0].get("FilePath") or "").casefold()
                == str(asset_path.resolve()).casefold(),
                "image_timing_matches": _timing_matches(image, scene),
                "text_timing_matches": _timing_matches(text, scene),
                "text_matches": len(text) == 1 and text[0].get("Text") == scene["label"],
            }
        )
    frames = [int(item.get("Frame", 0) or 0) for item in voice_items]
    project_path_audit = _audit_project_paths(
        project,
        allowed_local_paths={str(project_path.resolve()), str(asset_path.resolve())},
    )
    checks = {
        "project_parse_pass": bool(timeline),
        "one_selected_timeline": (
            len(project.get("Timelines", [])) == 1
            and project.get("SelectedTimelineIndex") == 0
        ),
        "VoiceItem_count_9": len(voice_items) == 9,
        "VoiceItem_objects_unchanged": voice_digests == source_voice_digests,
        "VoiceItem_text_character_order_matches_derived_csv": actual_rows == expected_rows,
        "VoiceItem_frames_strictly_increasing": bool(frames)
        and all(left < right for left, right in zip(frames, frames[1:])),
        "character_counts_3_6": dict(Counter(row[0] for row in actual_rows)) == EXPECTED_CHARACTER_COUNTS,
        "ImageItem_count_3": len(image_items) == 3,
        "independent_TextItem_count_3": len(text_items) == 3,
        "item_type_families_exact": set(type_counts)
        == {"VoiceItem", "ImageItem", "TextItem"},
        "scene_placeholder_coverage": all(
            row["ImageItem_count"] == 1
            and row["TextItem_count"] == 1
            and row["image_asset_matches"]
            and row["image_timing_matches"]
            and row["text_timing_matches"]
            and row["text_matches"]
            for row in scene_readback
        ),
        "timeline_length_unchanged": int(timeline.get("Length", 0) or 0)
        == source_timeline_length,
        "timeline_contains_last_scene": int(timeline.get("Length", 0) or 0)
        >= scene_specs[-1]["end_frame"],
        "placeholder_asset_is_valid_png": _png_metadata(asset_path)["valid"],
        "only_expected_local_absolute_references": not project_path_audit[
            "unexpected_local_reference_present"
        ],
        "no_external_or_file_uri_reference": not project_path_audit[
            "external_or_file_uri_reference_present"
        ],
        "no_unc_reference": not project_path_audit["unc_reference_present"],
        "diagnostic_boundary_explicit": all(
            all(token in row["label"] for token in ("DIAGNOSTIC", "NOT FINAL", "SAMPLE", "PLACEHOLDER"))
            for row in scene_readback
        ),
    }
    payload = {
        "schema_version": READBACK_SCHEMA_VERSION,
        "artifact_id": f"{artifact_id}_readback",
        "episode_id": EPISODE_ID,
        "status": "pending_validation",
        "diagnostic_only": True,
        "project_repo_relative_local_path": PROJECT_FILENAME,
        "project_sha256": _sha256(project_path),
        "normalized_project_sha256": _normalized_project_sha256(project),
        "asset": {
            "repo_relative_path": ASSET_PATH.as_posix(),
            "sha256": _sha256(asset_path),
            **_png_metadata(asset_path),
            "external_source": False,
        },
        "timeline": {
            "fps": _dict(timeline.get("VideoInfo")).get("FPS"),
            "length_frames": timeline.get("Length"),
            "item_count": len(items),
            "item_type_counts": type_counts,
        },
        "VoiceItems": [
            {
                "cue_id": f"csv_row_{index}",
                "scene_id": _scene_for_row(index),
                "character": item.get("CharacterName"),
                "text": item.get("Serif"),
                "frame": item.get("Frame"),
                "length": item.get("Length"),
                "canonical_json_sha256": voice_digests[index - 1],
            }
            for index, item in enumerate(voice_items, start=1)
        ],
        "scenes": scene_readback,
        "path_audit": {
            "project_contains_absolute_local_asset_reference": project_path_audit[
                "allowed_asset_reference_count"
            ]
            == 3,
            **project_path_audit,
            "private_path_values_exposed_in_readback": False,
            "commit_disposition": "local_only_not_committed_absolute_asset_reference",
        },
        "checks": checks,
        "failed_checks": [],
        "render_or_export_performed": False,
        "production_ymmp_written": False,
        "real_input_replaced": False,
        "public_ready": False,
        "final_thumbnail_approval": False,
        "upload_performed": False,
    }
    metadata_probe = copy.deepcopy(payload)
    metadata_probe["path_audit"].pop("private_path_values_exposed_in_readback", None)
    metadata_is_clean = not _text_has_absolute_or_uri(
        json.dumps(metadata_probe, ensure_ascii=False)
    )
    payload["path_audit"]["private_path_values_exposed_in_readback"] = (
        not metadata_is_clean
    )
    payload["checks"]["committed_metadata_has_no_private_path_values"] = (
        metadata_is_clean
    )
    failed_checks = [
        key for key, value in payload["checks"].items() if value is not True
    ]
    payload["failed_checks"] = failed_checks
    payload["status"] = "structural_pass" if not failed_checks else "blocked"
    return payload


def _build_manifest(
    *,
    artifact_id: str,
    project_path: Path,
    asset_path: Path,
    scene_specs: list[dict[str, Any]],
    readback: dict[str, Any],
    source_records: list[dict[str, Any]],
    source_environment: dict[str, str],
) -> dict[str, Any]:
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "artifact_id": artifact_id,
        "episode_id": EPISODE_ID,
        "status": "generated_structural_pass",
        "diagnostic_only": True,
        "generator": {
            "module": "src.pipeline.ymm4_diagnostic_placeholder_proof",
            "command": (
                "uv run python -m src.cli.main build-ymm4-diagnostic-placeholder-proof "
                "--package production_pilots/yukkuri_newsroom_content_spine_002 "
                "--source-ymmp <local-import-base.ymmp> "
                "--csv-gate-receipt <csv-gate-receipt-v2.json>"
            ),
            "determinism_contract": "same inputs and output path yield identical project and metadata bytes",
        },
        "source_records": source_records,
        "source_environment": copy.deepcopy(source_environment),
        "project": {
            "repo_relative_local_path": PROJECT_FILENAME,
            "sha256": _sha256(project_path),
            "normalized_sha256": readback["normalized_project_sha256"],
            "commit_disposition": "local_only_not_committed_absolute_asset_reference",
            "portable_relative_imageitem_path_proven": False,
        },
        "assets": [
            {
                "repo_relative_path": ASSET_PATH.as_posix(),
                "sha256": _sha256(asset_path),
                "width": PNG_WIDTH,
                "height": PNG_HEIGHT,
                "external_source": False,
                "generation": "deterministic_python_standard_library_rgba_png",
            }
        ],
        "scenes": scene_specs,
        "expected_counts": {
            "VoiceItem": 9,
            "ImageItem": 3,
            "independent_TextItem": 3,
            "characters": EXPECTED_CHARACTER_COUNTS,
        },
        "evidence_boundary": {
            "csv_gate_receipt_is_separate": True,
            "machine_readback_is_not_gui_observation": True,
            "diagnostic_project_receipt_records_gui_observation": True,
            "render_or_export_performed": False,
            "production_ymmp_written": False,
            "real_input_replaced": False,
            "rights_public_or_upload_approved": False,
            "final_thumbnail_approved": False,
        },
    }


def _source_records(package: Path, source: Path, receipt: Path) -> list[dict[str, Any]]:
    records = [
        ("derived_csv", package / DERIVED_CSV, DERIVED_CSV.as_posix()),
        ("canonical_csv", package / CANONICAL_CSV, CANONICAL_CSV.as_posix()),
        ("cue_map", package / CUE_MAP, CUE_MAP.as_posix()),
        ("character_profile", package / PROFILE, PROFILE.as_posix()),
        ("csv_gate_receipt_v2", receipt, receipt.name),
        ("local_import_base", source, source.name),
    ]
    return [
        {"record_id": record_id, "repo_relative_or_local_name": name, "sha256": _sha256(path)}
        for record_id, path, name in records
    ]


def validate_ymm4_diagnostic_placeholder_proof(
    *,
    proof_dir: str | Path,
    package_dir: str | Path,
    source_ymmp: str | Path,
    csv_gate_receipt: str | Path,
) -> dict[str, Any]:
    """Independently recompute and validate every proof artifact."""
    root = Path(proof_dir)
    package = Path(package_dir)
    source = Path(source_ymmp)
    receipt_path = Path(csv_gate_receipt)
    required = [
        root / PROJECT_FILENAME,
        root / MANIFEST_FILENAME,
        root / READBACK_FILENAME,
        root / RECEIPT_FILENAME,
        root / README_FILENAME,
        root / ASSET_PATH,
        root / ".gitignore",
    ]
    errors = [f"MISSING:{path.name}" for path in required if not path.exists()]
    if errors:
        return {"status": "failed", "errors": errors}

    try:
        inputs = _load_and_validate_inputs(package, source, receipt_path)
        stored_manifest = _load_json(root / MANIFEST_FILENAME)
        stored_readback = _load_json(root / READBACK_FILENAME)
        stored_receipt = _load_json(root / RECEIPT_FILENAME)
        artifact_id = str(stored_manifest.get("artifact_id") or "")
        if not artifact_id:
            errors.append("MANIFEST_ARTIFACT_ID_MISSING")
        source_voice_digests = [
            _json_sha256(item) for item in inputs["voice_items"]
        ]
        scene_specs = _derive_scene_specs(inputs["voice_items"])
        expected_readback = _build_readback(
            artifact_id=artifact_id,
            project_path=root / PROJECT_FILENAME,
            source_voice_digests=source_voice_digests,
            source_timeline_length=int(
                _first_timeline(inputs["source_project"]).get("Length", 0) or 0
            ),
            expected_rows=inputs["derived_rows"],
            scene_specs=scene_specs,
            asset_path=root / ASSET_PATH,
        )
        if (
            expected_readback.get("status") != "structural_pass"
            or expected_readback.get("failed_checks") != []
            or any(
                value is not True
                for value in _dict(expected_readback.get("checks")).values()
            )
        ):
            errors.append("RECOMPUTED_READBACK_NOT_STRUCTURAL_PASS")
        if stored_readback != expected_readback:
            errors.append("READBACK_RECOMPUTE_MISMATCH")
        expected_manifest = _build_manifest(
            artifact_id=artifact_id,
            project_path=root / PROJECT_FILENAME,
            asset_path=root / ASSET_PATH,
            scene_specs=scene_specs,
            readback=expected_readback,
            source_records=_source_records(package, source, receipt_path),
            source_environment=inputs["source_environment"],
        )
        if expected_manifest.get("status") != "generated_structural_pass":
            errors.append("RECOMPUTED_MANIFEST_NOT_STRUCTURAL_PASS")
        if stored_manifest != expected_manifest:
            errors.append("MANIFEST_RECOMPUTE_MISMATCH")
        if (root / README_FILENAME).read_text(encoding="utf-8") != _render_readme(
            expected_manifest
        ):
            errors.append("README_RECOMPUTE_MISMATCH")
        if stored_readback.get("artifact_id") != f"{artifact_id}_readback":
            errors.append("READBACK_ARTIFACT_ID_MISMATCH")
        if stored_manifest.get("episode_id") != EPISODE_ID or stored_readback.get(
            "episode_id"
        ) != EPISODE_ID:
            errors.append("PROOF_EPISODE_ID_MISMATCH")
        validate_gui_observation_receipt(stored_receipt, proof_dir=root)
        ignore_lines = {
            line.strip()
            for line in (root / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        if "*.local.ymmp" not in ignore_lines or not PROJECT_FILENAME.endswith(
            ".local.ymmp"
        ):
            errors.append("LOCAL_PROJECT_IGNORE_CONTRACT_MISMATCH")
    except (FileNotFoundError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"VALIDATION_EXCEPTION:{type(exc).__name__}:{exc}")
    return {"status": "passed" if not errors else "failed", "errors": errors}


def _expected_diagnostic_safety() -> dict[str, bool]:
    return {
        "diagnostic_only": True,
        "production_ymmp_written": False,
        "render_or_export_performed": False,
        "real_input_replaced": False,
        "rights_or_public_approval_performed": False,
        "final_thumbnail_approval": False,
        "public_ready": False,
        "upload_performed": False,
    }


def _receipt_evidence_hashes(
    root: Path,
    manifest: dict[str, Any],
) -> dict[str, str]:
    csv_record = next(
        (
            record
            for record in manifest.get("source_records", [])
            if isinstance(record, dict)
            and record.get("record_id") == "csv_gate_receipt_v2"
        ),
        None,
    )
    if not isinstance(csv_record, dict) or not csv_record.get("sha256"):
        raise ValueError("DIAGNOSTIC_MANIFEST_CSV_RECEIPT_HASH_MISSING")
    return {
        "manifest_sha256": _sha256(root / MANIFEST_FILENAME),
        "readback_sha256": _sha256(root / READBACK_FILENAME),
        "project_sha256": _sha256(root / PROJECT_FILENAME),
        "asset_sha256": _sha256(root / ASSET_PATH),
        "csv_gate_receipt_sha256": str(csv_record["sha256"]).upper(),
    }


def _screenshot_record(root: Path, screenshot: str | None) -> dict[str, Any]:
    if screenshot is None:
        return {
            "status": "not_captured",
            "repo_relative_path": None,
            "sha256": None,
        }
    if _text_has_absolute_or_uri(screenshot):
        raise ValueError("DIAGNOSTIC_SCREENSHOT_PATH_MUST_BE_RELATIVE")
    relative = Path(screenshot)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("DIAGNOSTIC_SCREENSHOT_PATH_MUST_BE_RELATIVE")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("DIAGNOSTIC_SCREENSHOT_OUTSIDE_PROOF_DIR") from exc
    if not candidate.is_file():
        raise ValueError("DIAGNOSTIC_SCREENSHOT_MISSING")
    return {
        "status": "captured",
        "repo_relative_path": relative.as_posix(),
        "sha256": _sha256(candidate),
    }


def _validate_screenshot_record(root: Path, record: dict[str, Any]) -> None:
    status = record.get("status")
    if status == "not_captured":
        if record != {
            "status": "not_captured",
            "repo_relative_path": None,
            "sha256": None,
        }:
            raise ValueError("DIAGNOSTIC_SCREENSHOT_NOT_CAPTURED_RECORD_INVALID")
        return
    if status != "captured":
        raise ValueError("DIAGNOSTIC_SCREENSHOT_STATUS_INVALID")
    relative = record.get("repo_relative_path")
    if not isinstance(relative, str):
        raise ValueError("DIAGNOSTIC_SCREENSHOT_PATH_INVALID")
    expected = _screenshot_record(root, relative)
    if record != expected:
        raise ValueError("DIAGNOSTIC_SCREENSHOT_HASH_MISMATCH")


def _validate_observed_environment(receipt: dict[str, Any]) -> None:
    environment = _dict(receipt.get("observed_by_environment"))
    if set(environment) != {"application", "yymm4_version", "observation_mode"}:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_ENVIRONMENT_FIELD_SET_MISMATCH")
    expected_mode = (
        "actual_gui_reopen"
        if receipt.get("status") == "passed"
        else "actual_gui_reopen_attempt"
    )
    if environment.get("application") != "YukkuriMovieMaker":
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_APPLICATION_MISMATCH")
    version = environment.get("yymm4_version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+(?:\.\d+){3}", version):
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_VERSION_INVALID")
    if environment.get("observation_mode") != expected_mode:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_OBSERVATION_MODE_INVALID")


def _validate_iso_timestamp(value: str) -> None:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_TIMESTAMP_INVALID") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("DIAGNOSTIC_GUI_RECEIPT_TIMESTAMP_TIMEZONE_REQUIRED")


def _audit_project_paths(
    project: dict[str, Any],
    *,
    allowed_local_paths: set[str],
) -> dict[str, Any]:
    strings: list[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for nested in value.values():
                visit(nested)
        elif isinstance(value, list):
            for nested in value:
                visit(nested)
        elif isinstance(value, str):
            strings.append(value)

    visit(project)
    normalized_allowed = {
        value.replace("/", "\\").casefold() for value in allowed_local_paths
    }
    local_values = [
        value for value in strings if re.search(r"[A-Za-z]:[\\/]", value) is not None
    ]
    unc_values = [value for value in strings if "\\\\" in value]
    external_values = [
        value
        for value in strings
        if re.search(
            r"[A-Za-z][A-Za-z0-9+.-]*://",
            value,
            flags=re.IGNORECASE,
        )
    ]
    normalized_local = [value.replace("/", "\\").casefold() for value in local_values]
    allowed_flags = [value in normalized_allowed for value in normalized_local]
    allowed_asset_count = sum(
        allowed
        and not original.casefold().endswith(".ymmp")
        for original, allowed in zip(local_values, allowed_flags)
    )
    unexpected_count = sum(not allowed for allowed in allowed_flags)
    return {
        "absolute_local_reference_count": len(local_values),
        "allowed_absolute_local_reference_count": sum(allowed_flags),
        "allowed_asset_reference_count": allowed_asset_count,
        "unexpected_local_reference_count": unexpected_count,
        "unexpected_local_reference_present": unexpected_count > 0,
        "external_or_file_uri_reference_present": bool(external_values),
        "unc_reference_present": bool(unc_values),
    }


def _text_has_absolute_or_uri(text: str) -> bool:
    return re.search(
        r"(?:[A-Za-z]:[\\/]|\\\\|[A-Za-z][A-Za-z0-9+.-]*://)",
        text,
        flags=re.IGNORECASE,
    ) is not None


def _write_or_preserve_gui_receipt(
    path: Path,
    *,
    manifest: dict[str, Any],
    readback: dict[str, Any],
) -> None:
    if path.exists():
        existing = _load_json(path)
        validate_gui_observation_receipt(existing, proof_dir=path.parent)
        existing_project = _dict(existing.get("project")).get("sha256")
        if existing.get("status") in {"passed", "blocked"}:
            if existing_project != readback["project_sha256"]:
                raise ValueError("STALE_DIAGNOSTIC_GUI_RECEIPT_PROJECT_HASH")
            return
    pending = {
        "schema_version": GUI_RECEIPT_SCHEMA_VERSION,
        "artifact_id": f"{manifest.get('artifact_id')}_gui_observation",
        "episode_id": EPISODE_ID,
        "status": "ready_for_gui_observation",
        "result": "not_observed",
        "observed_at": None,
        "application_close_state": "not_observed",
        "project": {
            "repo_relative_local_path": PROJECT_FILENAME,
            "sha256": readback["project_sha256"],
            "commit_disposition": "local_only_not_committed_absolute_asset_reference",
        },
        "evidence_hashes": _receipt_evidence_hashes(path.parent, manifest),
        "observations": {},
        "screenshot": _screenshot_record(path.parent, None),
        "safety": _expected_diagnostic_safety(),
        "next_gate": "bounded_diagnostic_project_observation",
    }
    validate_gui_observation_receipt(pending, proof_dir=path.parent)
    _write_json(path, pending)


def _render_readme(manifest: dict[str, Any]) -> str:
    return f"""# Episode 002 YMM4 Diagnostic Placeholder Proof

Status: diagnostic-only; not final; not production/public-ready.

This pack separates two gates:

1. the CSV receipt proves automatic VoiceItem plus linked-subtitle import;
2. this pack proves a separate `.ymmp` route with one ImageItem and one independent TextItem for each of S1/S2/S3.

Scene spans come from actual VoiceItem frames and cue boundaries. They do not reuse provisional four-second blocks.

The local project is `{PROJECT_FILENAME}`. It is intentionally ignored and not committed because current YMM4 ImageItems use an absolute local asset path. Regenerate it with:

```powershell
{manifest['generator']['command']}
```

Tracked evidence:

- `{MANIFEST_FILENAME}`
- `{READBACK_FILENAME}`
- `{RECEIPT_FILENAME}`
- `{ASSET_PATH.as_posix()}`

No render/export, production `.ymmp`, real input, external media, rights/public approval, or upload is performed here.
"""


def _write_neutral_png(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    transparent = b"\x00\x00\x00\x00"
    band = b"\x46\x50\x5a\x78"
    border = b"\x8c\x96\xa0\x82"
    rows = bytearray()
    for y in range(PNG_HEIGHT):
        rows.append(0)
        if y < 180:
            rows.extend(band * PNG_WIDTH)
            continue
        if y >= PNG_HEIGHT - 24:
            rows.extend(border * PNG_WIDTH)
            continue
        rows.extend(border * 24)
        rows.extend(transparent * (PNG_WIDTH - 48))
        rows.extend(border * 24)
    payload = (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", struct.pack(">IIBBBBB", PNG_WIDTH, PNG_HEIGHT, 8, 6, 0, 0, 0))
        + _png_chunk(b"IDAT", zlib.compress(bytes(rows), level=9))
        + _png_chunk(b"IEND", b"")
    )
    path.write_bytes(payload)


def _png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)


def _png_metadata(path: Path) -> dict[str, Any]:
    try:
        header = path.read_bytes()[:24]
        width, height = struct.unpack(">II", header[16:24])
    except (OSError, struct.error):
        return {"valid": False, "width": None, "height": None, "format": "png"}
    return {
        "valid": header[:8] == b"\x89PNG\r\n\x1a\n" and width == PNG_WIDTH and height == PNG_HEIGHT,
        "width": width,
        "height": height,
        "format": "png",
    }


def _normalized_project_sha256(project: dict[str, Any]) -> str:
    normalized = copy.deepcopy(project)
    normalized["FilePath"] = "<LOCAL_DIAGNOSTIC_PROJECT>"
    for item in _get_timeline_items(normalized):
        if _item_type(item) == "ImageItem" and str(item.get("Remark") or "").startswith(REMARK_PREFIX):
            item["FilePath"] = "<PACK_ASSET>/diagnostic_placeholder.png"
    return _json_sha256(normalized)


def _ordered_voice_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in items if _item_type(item) == "VoiceItem"]


def _first_timeline(data: dict[str, Any]) -> dict[str, Any]:
    timelines = data.get("Timelines")
    if not isinstance(timelines, list) or not timelines or not isinstance(timelines[0], dict):
        raise ValueError("YMM4_PROJECT_TIMELINE_MISSING")
    return timelines[0]


def _timing_matches(items: list[dict[str, Any]], scene: dict[str, Any]) -> bool:
    return len(items) == 1 and int(items[0].get("Frame", -1)) == scene["start_frame"] and int(items[0].get("Length", -1)) == scene["length_frames"]


def _scene_for_row(row_number: int) -> str:
    for scene_id, start, end in SCENE_ROWS:
        if start < row_number <= end:
            return scene_id
    raise ValueError(f"ROW_OUTSIDE_SCENE_MAP:{row_number}")


def _load_csv_rows(path: Path) -> list[tuple[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.reader(handle) if row]
    if any(len(row) != 2 for row in rows):
        raise ValueError(f"YMM4_CSV_ROW_SHAPE_INVALID:{path}")
    return [(row[0], row[1]) for row in rows]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _json_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}
