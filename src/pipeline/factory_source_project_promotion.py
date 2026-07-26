"""Bounded queue-driven Factory Package source-project promotion.

This module intentionally supports one exact package, lifecycle edge, and
supervisor authority.  It materializes an ignored YMM4 source project while
keeping the package-prepared descriptor and queue-v1 descriptor immutable.
"""

from __future__ import annotations

import copy
import csv
import json
import os
import re
import shutil
import subprocess
import uuid
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Mapping

from src.pipeline.episode_video import resolve_yymm4_executable
from src.pipeline.factory_contract_v2_1 import validate_factory_package_lifecycle
from src.pipeline.factory_queue import (
    canonical_json_bytes,
    evaluate_factory_queue,
    sha256_file,
    sha256_json,
)
from src.pipeline.runtime_doctor import _file_product_version


PROMOTION_RESULT_SCHEMA = "nlmytgen.factory_source_project_promotion.v1"
READBACK_SCHEMA = "nlmytgen.factory_source_project_readback.v1"
RECEIPT_SCHEMA = "nlmytgen.factory_source_project_promotion_receipt.v1"
AUTHORITY_ID = "supervisor-food-expiry-source-project-materialization-2026-07-26"
PACKAGE_ID = "food_expiry_labels_001"
TARGET_LIFECYCLE = "source_project_ready"

PACKAGE_ROOT = Path("production_pilots/factory_canaries/food_expiry_labels_001")
PREDECESSOR_DESCRIPTOR = PACKAGE_ROOT / "factory_package_v2_1.json"
PREDECESSOR_DESCRIPTOR_SHA256 = (
    "18e078f6f6c5b6e17808ec9378d8476a9cd8ce426cd1281563c833ae21acf329"
)
PREDECESSOR_QUEUE = Path(
    "production_pilots/factory_queues/four_package_lifecycle_queue_v1.json"
)
PREDECESSOR_QUEUE_SHA256 = (
    "2cfbdab4bf3bfb765afa8909b54212311155ba85c3838078a1e0aac77a11375f"
)
CONTENT_IDENTITY_SHA256 = (
    "27165fad6fadaee2e5c247a86758a505c7f5f5797eb7b386d174585622a585c6"
)
CANONICAL_CSV_SHA256 = (
    "00ade6df462c9cefb8cc1960d385def18a053793561d96a1da38eb9d9c41b855"
)
DERIVED_CSV_SHA256 = (
    "b4b4bb7ae998fa3c850a030df2ba719cde8ba1bd8c82c1215b40a7d5a9ee2256"
)
EXPECTED_SPEAKER = "ゆっくり霊夢赤縁"

SOURCE_PROJECT = (
    PACKAGE_ROOT / "local_outputs/food_expiry_labels_source.local.ymmp"
)
SOURCE_PROJECT_READBACK = PACKAGE_ROOT / "source_project_readback.json"
PROMOTION_RECEIPT = PACKAGE_ROOT / "source_project_promotion_receipt.json"
SUCCESSOR_DESCRIPTOR = PACKAGE_ROOT / "factory_package_v2_1_source_project_ready.json"
SUCCESSOR_QUEUE = Path(
    "production_pilots/factory_queues/four_package_lifecycle_queue_v2.json"
)
FAILURE_RECEIPT = PACKAGE_ROOT / "local_outputs/source_project_promotion_failure.local.json"

TEMPLATE_PROJECT = Path(
    "production_pilots/factory_canaries/real_estate_reins_transparency_001/"
    "auto_video_runs/source_projects/real_estate_reins_source.local.ymmp"
)
TEMPLATE_PROJECT_SHA256 = (
    "ed2773ce87a41936dd82d16d666d253f8bdba8763fc11bfa829d4818cb1b3ec9"
)

_WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")
_VOICE_TYPE = "YukkuriMovieMaker.Project.Items.VoiceItem"


class FactorySourceProjectPromotionError(RuntimeError):
    """Fail-closed bounded promotion error."""

    def __init__(self, message: str, *, code: str, stage: str) -> None:
        super().__init__(message)
        self.code = code
        self.stage = stage

    def as_payload(self) -> dict[str, Any]:
        return {
            "schema": PROMOTION_RESULT_SCHEMA,
            "schema_version": "1.0",
            "status": "failed",
            "error": {
                "code": self.code,
                "stage": self.stage,
                "message": str(self),
            },
            "boundaries": _boundaries(),
        }


Builder = Callable[[Path, Path, Path], Mapping[str, Any]]


def _fail(message: str, *, code: str, stage: str) -> None:
    raise FactorySourceProjectPromotionError(message, code=code, stage=stage)


def _boundaries(**overrides: Any) -> dict[str, Any]:
    result = {
        "yymm4_launch_count": 0,
        "source_project_builder_launch_count": 0,
        "render_driver_launched": False,
        "render_performed": False,
        "ffmpeg_encode_performed": False,
        "mp4_generated": False,
        "media_playback": False,
        "speaker_playback": False,
        "system_volume_operation": False,
        "manual_interaction": False,
        "computer_use": False,
        "input_injection": False,
        "human_decision_created": False,
        "rights_or_public_authority_changed": False,
    }
    result.update(overrides)
    return result


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail(
            f"JSON could not be read: {path.name}",
            code="json_read_failed",
            stage="preflight",
        )
    if not isinstance(value, dict):
        _fail(
            f"JSON root must be an object: {path.name}",
            code="json_root_invalid",
            stage="preflight",
        )
    return value


def _repo_path(repo_root: Path, locator: Path | str, *, field: str) -> Path:
    text = Path(locator).as_posix()
    if (
        not text
        or Path(text).is_absolute()
        or _WINDOWS_ABSOLUTE.match(text)
        or "\\" in text
        or ".." in Path(text).parts
    ):
        _fail(
            f"{field} must be a repository-relative forward-slash locator",
            code="private_or_unsafe_locator",
            stage="preflight",
        )
    root = repo_root.resolve()
    resolved = (root / text).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        _fail(
            f"{field} escapes the repository",
            code="locator_outside_repository",
            stage="preflight",
        )
    return resolved


def _validate_output_locator(repo_root: Path, locator: Path) -> Path:
    output = _repo_path(repo_root, locator, field="source_project.path")
    approved_root = (repo_root.resolve() / PACKAGE_ROOT / "local_outputs").resolve()
    try:
        output.relative_to(approved_root)
    except ValueError:
        _fail(
            "source project is outside the approved package-local output root",
            code="source_project_outside_package_root",
            stage="preflight",
        )
    return output


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(payload))


def _write_or_verify_json(path: Path, payload: Mapping[str, Any]) -> None:
    expected = canonical_json_bytes(payload)
    if path.exists():
        if path.read_bytes() != expected:
            _fail(
                f"existing tracked artifact differs: {path.name}",
                code="tracked_artifact_collision",
                stage="persist",
            )
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(expected)


def _csv_rows(path: Path) -> list[tuple[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [tuple(row) for row in csv.reader(handle)]
    if not rows or any(len(row) != 2 for row in rows):
        _fail(
            f"YMM4 CSV must contain exactly two columns: {path.name}",
            code="csv_shape_invalid",
            stage="preflight",
        )
    return [(str(speaker), str(text)) for speaker, text in rows]


def _validate_request(
    *,
    evaluation: Mapping[str, Any],
    queue_path: Path,
    package_id: str,
    to_lifecycle: str,
    authority_id: str | None,
    render_authority_id: str | None,
) -> Mapping[str, Any]:
    if to_lifecycle != TARGET_LIFECYCLE:
        _fail(
            "source-only command refuses lifecycle jumps",
            code="unsupported_lifecycle_jump",
            stage="authority",
        )
    if render_authority_id:
        _fail(
            "render authority is forbidden for a source-only command",
            code="render_authority_forbidden",
            stage="authority",
        )
    if not authority_id:
        _fail(
            "source-project authority ID is required",
            code="authority_id_missing",
            stage="authority",
        )
    if authority_id != AUTHORITY_ID:
        _fail(
            "source-project authority ID is not exact",
            code="authority_id_mismatch",
            stage="authority",
        )
    if Path(queue_path).as_posix() != PREDECESSOR_QUEUE.as_posix():
        _fail(
            "this bounded promotion requires the exact predecessor queue",
            code="queue_override_rejected",
            stage="preflight",
        )
    descriptor = evaluation.get("queue_descriptor") or {}
    if descriptor.get("sha256") != PREDECESSOR_QUEUE_SHA256:
        _fail(
            "predecessor queue identity drifted",
            code="queue_identity_drift",
            stage="preflight",
        )
    counts = evaluation.get("counts") or {}
    expected_counts = {
        "total_packages": 4,
        "verified_noop": 3,
        "source_project_candidates": 1,
        "render_candidates": 0,
        "blocked_packages": 0,
        "invalid_packages": 0,
        "scheduled_for_render": 0,
        "execution_set_size": 0,
    }
    if any(counts.get(key) != value for key, value in expected_counts.items()):
        _fail(
            "bounded queue baseline no longer has exactly one source-project candidate",
            code="queue_candidate_baseline_drift",
            stage="preflight",
        )
    candidates = [
        row
        for row in evaluation.get("packages", [])
        if row.get("technical_decision") == "source_project_generation_required"
    ]
    if len(candidates) != 1:
        _fail(
            "queue must select exactly one source-project candidate",
            code="source_candidate_not_unique",
            stage="preflight",
        )
    candidate = candidates[0]
    if package_id != candidate.get("package_id"):
        _fail(
            "manually named package is not the queue-selected candidate",
            code="package_not_selected",
            stage="authority",
        )
    if package_id != PACKAGE_ID:
        _fail(
            "unrelated package override is forbidden",
            code="unrelated_package_override",
            stage="authority",
        )
    if (
        candidate.get("descriptor_path") != PREDECESSOR_DESCRIPTOR.as_posix()
        or candidate.get("descriptor_sha256") != PREDECESSOR_DESCRIPTOR_SHA256
        or candidate.get("content_identity_sha256") != CONTENT_IDENTITY_SHA256
        or candidate.get("normalized_lifecycle") != "package_prepared"
    ):
        _fail(
            "queue-selected predecessor identity drifted",
            code="predecessor_identity_drift",
            stage="preflight",
        )
    if candidate.get("execution_eligible") is not False:
        _fail(
            "baseline queue unexpectedly marked the package executable",
            code="baseline_execution_authority_drift",
            stage="preflight",
        )
    return candidate


def _validate_predecessor_inputs(
    repo_root: Path, descriptor: Mapping[str, Any]
) -> tuple[list[tuple[str, str]], list[str]]:
    if descriptor.get("lifecycle", {}).get("state") != "package_prepared":
        _fail(
            "predecessor lifecycle must remain package_prepared",
            code="predecessor_lifecycle_drift",
            stage="preflight",
        )
    if (
        descriptor.get("identities", {}).get("content_identity_sha256")
        != CONTENT_IDENTITY_SHA256
    ):
        _fail(
            "predecessor content identity drifted",
            code="content_identity_drift",
            stage="preflight",
        )
    canonical_csv = repo_root / PACKAGE_ROOT / "canonical_yymm4.csv"
    derived_csv = repo_root / PACKAGE_ROOT / "derived_yymm4_import.csv"
    if sha256_file(canonical_csv) != CANONICAL_CSV_SHA256:
        _fail(
            "canonical CSV hash mismatch",
            code="canonical_csv_hash_mismatch",
            stage="preflight",
        )
    if sha256_file(derived_csv) != DERIVED_CSV_SHA256:
        _fail(
            "derived CSV hash mismatch",
            code="derived_csv_hash_mismatch",
            stage="preflight",
        )
    canonical_rows = _csv_rows(canonical_csv)
    derived_rows = _csv_rows(derived_csv)
    if [row[1] for row in canonical_rows] != [row[1] for row in derived_rows]:
        _fail(
            "derived CSV changes canonical cue text or order",
            code="derived_csv_content_drift",
            stage="preflight",
        )
    if [row[0] for row in canonical_rows] != ["れいむ"] * 4:
        _fail(
            "canonical CSV speaker mapping changed",
            code="canonical_csv_speaker_drift",
            stage="preflight",
        )
    expected_sequence = list(descriptor["canonical_content"]["cue_sequence"])
    canonical_script = _load_json(repo_root / descriptor["canonical_content"]["path"])
    cues = canonical_script.get("cues") or []
    cue_sequence = [cue.get("cue_id") for cue in cues]
    cue_texts = [cue.get("text") for cue in cues]
    if cue_sequence != expected_sequence or cue_texts != [row[1] for row in derived_rows]:
        _fail(
            "canonical cue text or order changed",
            code="cue_text_or_order_drift",
            stage="preflight",
        )
    speakers = [row[0] for row in derived_rows]
    expected_mapping = descriptor["shape"]["speaker_mapping"]
    if (
        speakers != [EXPECTED_SPEAKER] * 4
        or list(expected_mapping.values()) != speakers
        or descriptor["shape"]["speaker_counts"] != {EXPECTED_SPEAKER: 4}
    ):
        _fail(
            "single-speaker mapping changed",
            code="speaker_mapping_drift",
            stage="preflight",
        )
    if (
        len(cues) != 4
        or descriptor["shape"]["cue_count"] != 4
        or descriptor["shape"]["scene_count"] != 1
        or set(descriptor["shape"]["scene_mapping"].values()) != {"S1"}
    ):
        _fail(
            "four-cue one-scene shape changed",
            code="package_shape_drift",
            stage="preflight",
        )
    return derived_rows, expected_sequence


def _walk_strings(node: Any) -> list[str]:
    if isinstance(node, str):
        return [node]
    if isinstance(node, Mapping):
        result: list[str] = []
        for value in node.values():
            result.extend(_walk_strings(value))
        return result
    if isinstance(node, list):
        result = []
        for value in node:
            result.extend(_walk_strings(value))
        return result
    return []


def _is_private_absolute(value: str) -> bool:
    return bool(
        _WINDOWS_ABSOLUTE.match(value)
        or value.startswith("\\\\")
        or value.startswith("/")
    )


def _sanitize_paths(node: Any) -> Any:
    if isinstance(node, dict):
        return {key: _sanitize_paths(value) for key, value in node.items()}
    if isinstance(node, list):
        return [_sanitize_paths(value) for value in node]
    if isinstance(node, str) and _is_private_absolute(node):
        trimmed = node.rstrip("\\/")
        return re.split(r"[\\/]", trimmed)[-1]
    return node


def _selected_timeline(project: Mapping[str, Any]) -> Mapping[str, Any]:
    timelines = project.get("Timelines")
    if not isinstance(timelines, list) or len(timelines) != 1:
        _fail(
            "source project must contain exactly one timeline",
            code="source_project_timeline_count_invalid",
            stage="readback",
        )
    timeline = timelines[0]
    if not isinstance(timeline, Mapping):
        _fail(
            "source project timeline is invalid",
            code="source_project_timeline_invalid",
            stage="readback",
        )
    return timeline


def _prepare_blank_project(
    *, repo_root: Path, working_project: Path, package_id: str
) -> None:
    template = repo_root / TEMPLATE_PROJECT
    if not template.is_file() or sha256_file(template) != TEMPLATE_PROJECT_SHA256:
        _fail(
            "read-only source-project template is missing or drifted",
            code="source_template_unavailable",
            stage="materialize",
        )
    project = _load_json(template)
    timeline = dict(_selected_timeline(project))
    timeline["ID"] = str(uuid.uuid5(uuid.NAMESPACE_URL, f"nlmytgen:{package_id}:source"))
    timeline["Name"] = f"{package_id} source project"
    timeline["Items"] = []
    timeline["Length"] = 1
    timeline["CurrentFrame"] = 0
    timeline["MaxLayer"] = 0
    project["FilePath"] = working_project.name
    project["SelectedTimelineIndex"] = 0
    project["Timelines"] = [timeline]
    project["Characters"] = []
    project["CollapsedGroups"] = []
    project["LayoutXml"] = ""
    project["ToolStates"] = {}
    working_project.parent.mkdir(parents=True, exist_ok=True)
    working_project.write_text(
        json.dumps(project, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
        newline="\n",
    )


def _normalize_materialized_project(project_path: Path) -> None:
    project = _load_json(project_path)
    timeline = dict(_selected_timeline(project))
    items = timeline.get("Items")
    if not isinstance(items, list):
        _fail(
            "materialized source project has no items",
            code="source_project_items_missing",
            stage="readback",
        )
    voices = [
        item
        for item in items
        if isinstance(item, dict)
        and str(item.get("$type", "")).startswith(_VOICE_TYPE)
    ]
    speakers = {str(item.get("CharacterName", "")) for item in voices}
    characters = [
        row
        for row in project.get("Characters", [])
        if isinstance(row, dict) and str(row.get("Name", "")) in speakers
    ]
    timeline["Name"] = f"{PACKAGE_ID} source project"
    timeline["Items"] = voices
    timeline["CurrentFrame"] = 0
    timeline["MaxLayer"] = max((int(row.get("Layer", 0)) for row in voices), default=0)
    project["FilePath"] = project_path.name
    project["SelectedTimelineIndex"] = 0
    project["Timelines"] = [timeline]
    project["Characters"] = characters
    project["CollapsedGroups"] = []
    project["LayoutXml"] = ""
    project["ToolStates"] = {}
    project = _sanitize_paths(project)
    project_path.write_text(
        json.dumps(project, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
        newline="\n",
    )


def _run_actual_builder(
    repo_root: Path, output_project: Path, derived_csv: Path
) -> Mapping[str, Any]:
    executable = resolve_yymm4_executable()
    version = _file_product_version(executable) or "unknown"
    working = output_project.with_name("food_expiry_labels_source.working.local.ymmp")
    if working.exists():
        attempt = 1
        while True:
            preserved = output_project.with_name(
                f"food_expiry_labels_source.failed-attempt-{attempt}.local.ymmp"
            )
            if not preserved.exists():
                os.replace(working, preserved)
                break
            attempt += 1
    prior_attempts = len(
        list(output_project.parent.glob(
            "food_expiry_labels_source.failed-attempt-*.local.ymmp"
        ))
    )
    current_attempt = prior_attempts + 1
    _prepare_blank_project(
        repo_root=repo_root,
        working_project=working,
        package_id=PACKAGE_ID,
    )
    driver_project = repo_root / "tools/Ymm4RenderAutomation/Ymm4RenderAutomation.csproj"
    command = [
        "dotnet",
        "run",
        "--project",
        str(driver_project),
        "--configuration",
        "Release",
        "--",
        "import-script",
        "--exe",
        str(executable),
        "--project",
        str(working),
        "--csv",
        str(derived_csv),
        "--timeout-seconds",
        "1200",
    ]
    environment = dict(os.environ)
    environment["NLMYTGEN_AUDIO_POLICY"] = "silent"
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=1500,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        _fail(
            f"source-project builder failed to complete: {type(exc).__name__}",
            code="source_project_builder_failed",
            stage="materialize",
        )
    diagnostic = output_project.with_name(
        f"source_project_builder_attempt_{current_attempt}.local.log"
    )
    diagnostic.write_text(
        completed.stderr,
        encoding="utf-8",
        newline="\n",
    )
    if completed.returncode != 0:
        last_error = completed.stderr.strip().splitlines()[-1:] or ["driver failed"]
        try:
            failure = json.loads(last_error[0])
        except json.JSONDecodeError:
            failure = {}
        failure_stage = str(failure.get("stage") or "unknown")
        failure_message = str(failure.get("message") or last_error[0])
        _fail(
            f"source-project builder failed at {failure_stage}: {failure_message[:200]}",
            code="source_project_builder_failed",
            stage="materialize",
        )
    try:
        driver = json.loads(completed.stdout.strip().splitlines()[-1])
    except (IndexError, json.JSONDecodeError):
        _fail(
            "source-project builder returned invalid JSON",
            code="source_project_builder_output_invalid",
            stage="materialize",
        )
    if (
        driver.get("status") != "passed"
        or driver.get("operation") != "script_row_builder"
        or driver.get("imported_rows") != 4
        or driver.get("process_cleanup") is not True
        or driver.get("preview_playback") is not False
        or driver.get("speaker_playback") is not False
    ):
        _fail(
            "source-project builder result violates the source-only contract",
            code="source_project_builder_contract_failed",
            stage="materialize",
        )
    _normalize_materialized_project(working)
    output_project.parent.mkdir(parents=True, exist_ok=True)
    os.replace(working, output_project)
    return {
        "driver": "windows_uia",
        "builder": "Ymm4RenderAutomation import-script generic arbitrary-row path",
        "yymm4_version": version,
        "imported_rows": 4,
        "process_cleanup": True,
        "preview_playback": False,
        "speaker_playback": False,
        "yymm4_launch_count": current_attempt,
        "source_project_builder_launch_count": current_attempt,
    }


def build_source_project_readback(
    *,
    repo_root: Path,
    project_locator: Path,
    predecessor: Mapping[str, Any],
    cue_sequence: list[str],
    expected_rows: list[tuple[str, str]],
    builder_result: Mapping[str, Any],
) -> dict[str, Any]:
    project_path = _repo_path(
        repo_root, project_locator, field="source_project.path"
    )
    if not project_path.is_file():
        _fail(
            "source project is absent",
            code="source_project_absent",
            stage="readback",
        )
    project = _load_json(project_path)
    timeline = _selected_timeline(project)
    items = timeline.get("Items")
    if not isinstance(items, list):
        _fail(
            "source project items are invalid",
            code="source_project_items_invalid",
            stage="readback",
        )
    voices = [
        item
        for item in items
        if isinstance(item, Mapping)
        and str(item.get("$type", "")).startswith(_VOICE_TYPE)
    ]
    other_items = len(items) - len(voices)
    observed_rows = [
        (str(item.get("CharacterName", "")), str(item.get("Serif", "")))
        for item in voices
    ]
    frames = [int(item.get("Frame", -1)) for item in voices]
    lengths = [int(item.get("Length", 0)) for item in voices]
    if len(voices) != 4 or observed_rows != expected_rows:
        _fail(
            "source project cue text, order, or speaker mapping differs",
            code="source_project_content_mismatch",
            stage="readback",
        )
    if other_items != 0:
        _fail(
            "source project contains unrelated non-voice items",
            code="source_project_unrelated_items",
            stage="readback",
        )
    if frames != [sum(lengths[:index]) for index in range(len(lengths))]:
        _fail(
            "source project voice timing is not ordered and contiguous",
            code="source_project_timing_invalid",
            stage="readback",
        )
    timeline_frames = int(timeline.get("Length", 0))
    if timeline_frames != sum(lengths) or timeline_frames <= 0:
        _fail(
            "source project timeline length is invalid",
            code="source_project_timeline_length_invalid",
            stage="readback",
        )
    fps = int(predecessor["shape"]["fps"])
    duration = round(timeline_frames / fps, 6)
    if not 18 <= duration <= 30:
        _fail(
            "source project duration is outside the 18-30 second contract",
            code="source_project_duration_out_of_range",
            stage="readback",
        )
    speakers = Counter(row[0] for row in observed_rows)
    if speakers != Counter({EXPECTED_SPEAKER: 4}):
        _fail(
            "source project is not the exact single-speaker shape",
            code="source_project_speaker_count_invalid",
            stage="readback",
        )
    strings = _walk_strings(project)
    absolute_paths = [value for value in strings if _is_private_absolute(value)]
    metadata_checks = {
        "tool_states_empty": project.get("ToolStates") in ({}, None),
        "layout_xml_empty": project.get("LayoutXml") in ("", None),
        "collapsed_groups_empty": project.get("CollapsedGroups") in ([], None),
        "private_absolute_paths_absent": not absolute_paths,
        "unrelated_non_voice_items": other_items,
        "character_count": len(project.get("Characters") or []),
        "single_character_only": [
            row.get("Name")
            for row in project.get("Characters", [])
            if isinstance(row, Mapping)
        ]
        == [EXPECTED_SPEAKER],
    }
    if not all(
        value is True
        for key, value in metadata_checks.items()
        if key
        not in {
            "unrelated_non_voice_items",
            "character_count",
        }
    ) or metadata_checks["unrelated_non_voice_items"] != 0:
        _fail(
            "source project contains stale, private, or unrelated metadata",
            code="source_project_metadata_not_clean",
            stage="readback",
        )
    structural_payload = {
        "schema": "nlmytgen.factory_source_project_structure.v1",
        "voice_items": [
            {
                "cue_id": cue_id,
                "speaker": speaker,
                "text": text,
                "frame": frame,
                "length": length,
            }
            for cue_id, (speaker, text), frame, length in zip(
                cue_sequence, observed_rows, frames, lengths, strict=True
            )
        ],
        "timeline_frames": timeline_frames,
        "fps": fps,
        "scene_count": int(predecessor["shape"]["scene_count"]),
        "metadata_checks": metadata_checks,
    }
    return {
        "schema": READBACK_SCHEMA,
        "schema_version": "1.0",
        "status": "passed",
        "package_id": PACKAGE_ID,
        "predecessor": {
            "descriptor_path": PREDECESSOR_DESCRIPTOR.as_posix(),
            "descriptor_sha256": PREDECESSOR_DESCRIPTOR_SHA256,
        },
        "content_identity_sha256": CONTENT_IDENTITY_SHA256,
        "source_project": {
            "path": project_locator.as_posix(),
            "sha256": sha256_file(project_path),
            "size_bytes": project_path.stat().st_size,
            "yymm4_version": str(builder_result.get("yymm4_version") or "unknown"),
            "structural_identity_sha256": sha256_json(structural_payload),
        },
        "structure": {
            "voice_item_count": len(voices),
            "speaker_counts": dict(sorted(speakers.items())),
            "cue_mapping": structural_payload["voice_items"],
            "scene_count": int(predecessor["shape"]["scene_count"]),
            "timeline_frames": timeline_frames,
            "duration_seconds": duration,
            "fps": fps,
            "metadata_checks": metadata_checks,
        },
        "downstream_evidence": {
            "generated_project": "absent",
            "render_validation": "absent",
            "human_decision": "absent",
        },
        "authority_clocks": {
            "rights": False,
            "production": False,
            "publication": False,
            "upload": False,
            "release": False,
        },
        "runtime": {
            "audio_policy": "silent_by_default",
            "driver": str(builder_result.get("driver") or "validation_only"),
            "process_cleanup": bool(builder_result.get("process_cleanup", True)),
            "preview_playback": False,
            "speaker_playback": False,
        },
    }


def _build_successor_descriptor(
    predecessor: Mapping[str, Any], readback: Mapping[str, Any]
) -> dict[str, Any]:
    successor = copy.deepcopy(predecessor)
    successor["lifecycle"] = {
        "schema": "nlmytgen.factory_package.lifecycle.v2.1",
        "state": "source_project_ready",
        "contract_valid": True,
        "tracked_package_ready": True,
        "source_project_ready": True,
        "render_ready": False,
        "human_accepted": False,
    }
    successor["source_project"] = {
        "schema": "nlmytgen.factory_package.source_project.v2.1",
        "state": "ready",
        "strategy": predecessor["source_project"]["strategy"],
        "path": readback["source_project"]["path"],
        "sha256": readback["source_project"]["sha256"],
        "identity_source": "promotion_receipt_and_structural_readback",
        "live_required_for_contract": False,
    }
    values = successor["extensions"]["values"]
    values["org.nlmytgen.food_expiry_labels.lifecycle_predecessor"] = {
        "descriptor_path": PREDECESSOR_DESCRIPTOR.as_posix(),
        "descriptor_sha256": PREDECESSOR_DESCRIPTOR_SHA256,
        "promotion_receipt_path": PROMOTION_RECEIPT.as_posix(),
        "source_project_readback_path": SOURCE_PROJECT_READBACK.as_posix(),
        "source_project_readback_sha256": sha256_json(readback),
    }
    if successor["identities"]["content_identity_sha256"] != CONTENT_IDENTITY_SHA256:
        _fail(
            "successor content identity changed",
            code="successor_content_identity_drift",
            stage="persist",
        )
    return successor


def _build_successor_queue(predecessor_queue: Mapping[str, Any]) -> dict[str, Any]:
    successor = copy.deepcopy(predecessor_queue)
    successor["queue"]["queue_id"] = "four_package_lifecycle_queue_v2"
    packages = successor["queue"]["packages"]
    if len(packages) != 4 or packages[-1]["expected_package_id"] != PACKAGE_ID:
        _fail(
            "predecessor queue order changed",
            code="predecessor_queue_order_drift",
            stage="persist",
        )
    packages[-1]["descriptor_path"] = SUCCESSOR_DESCRIPTOR.as_posix()
    return successor


def _receipt(
    *, readback: Mapping[str, Any], observations: list[Mapping[str, Any]]
) -> dict[str, Any]:
    return {
        "schema": RECEIPT_SCHEMA,
        "schema_version": "1.0",
        "status": "passed",
        "authority_id": AUTHORITY_ID,
        "package_id": PACKAGE_ID,
        "promotion": {
            "from_lifecycle": "package_prepared",
            "to_lifecycle": "source_project_ready",
            "predecessor_descriptor_path": PREDECESSOR_DESCRIPTOR.as_posix(),
            "predecessor_descriptor_sha256": PREDECESSOR_DESCRIPTOR_SHA256,
            "predecessor_queue_path": PREDECESSOR_QUEUE.as_posix(),
            "predecessor_queue_sha256": PREDECESSOR_QUEUE_SHA256,
            "content_identity_sha256_before": CONTENT_IDENTITY_SHA256,
            "content_identity_sha256_after": CONTENT_IDENTITY_SHA256,
        },
        "source_project": copy.deepcopy(readback["source_project"]),
        "readback": {
            "path": SOURCE_PROJECT_READBACK.as_posix(),
            "sha256": sha256_json(readback),
        },
        "observations": list(observations),
        "boundaries": _boundaries(),
    }


def _plan_payload(candidate: Mapping[str, Any], *, execute: bool) -> dict[str, Any]:
    return {
        "schema": PROMOTION_RESULT_SCHEMA,
        "schema_version": "1.0",
        "status": "planned" if not execute else "preflight_passed",
        "operation": "source_project_generation",
        "authority_id": AUTHORITY_ID,
        "package_id": PACKAGE_ID,
        "from_lifecycle": "package_prepared",
        "to_lifecycle": "source_project_ready",
        "queue_decision": candidate["technical_decision"],
        "source_project_path": SOURCE_PROJECT.as_posix(),
        "execute": execute,
        "boundaries": _boundaries(),
    }


def _validate_known_noop(
    *,
    repo_root: Path,
    predecessor: Mapping[str, Any],
    expected_rows: list[tuple[str, str]],
    cue_sequence: list[str],
) -> dict[str, Any] | None:
    project = repo_root / SOURCE_PROJECT
    tracked = [
        repo_root / SOURCE_PROJECT_READBACK,
        repo_root / PROMOTION_RECEIPT,
        repo_root / SUCCESSOR_DESCRIPTOR,
        repo_root / SUCCESSOR_QUEUE,
    ]
    if not project.exists() and not any(path.exists() for path in tracked):
        return None
    if not project.is_file() or not all(path.is_file() for path in tracked):
        _fail(
            "source-project output collides with incomplete promotion evidence",
            code="output_target_collision",
            stage="preflight",
        )
    canonical_readback = _load_json(repo_root / SOURCE_PROJECT_READBACK)
    if (
        canonical_readback.get("schema") != READBACK_SCHEMA
        or not isinstance(canonical_readback.get("source_project"), Mapping)
        or not canonical_readback["source_project"].get("yymm4_version")
    ):
        _fail(
            "existing source-project readback is invalid",
            code="existing_source_project_corrupt",
            stage="preflight",
        )
    builder_result = {
        "yymm4_version": canonical_readback["source_project"]["yymm4_version"],
        "driver": canonical_readback.get("runtime", {}).get("driver", "windows_uia"),
        "process_cleanup": canonical_readback.get("runtime", {}).get(
            "process_cleanup", True
        ),
    }
    observed = build_source_project_readback(
        repo_root=repo_root,
        project_locator=SOURCE_PROJECT,
        predecessor=predecessor,
        cue_sequence=cue_sequence,
        expected_rows=expected_rows,
        builder_result=builder_result,
    )
    if observed != canonical_readback:
        _fail(
            "existing source project or readback is corrupt",
            code="existing_source_project_corrupt",
            stage="preflight",
        )
    successor = _load_json(repo_root / SUCCESSOR_DESCRIPTOR)
    if successor != _build_successor_descriptor(predecessor, canonical_readback):
        _fail(
            "existing successor descriptor differs",
            code="existing_successor_descriptor_drift",
            stage="preflight",
        )
    queue = _load_json(repo_root / PREDECESSOR_QUEUE)
    if _load_json(repo_root / SUCCESSOR_QUEUE) != _build_successor_queue(queue):
        _fail(
            "existing successor queue differs",
            code="existing_successor_queue_drift",
            stage="preflight",
        )
    validate_factory_package_lifecycle(
        repo_root=repo_root,
        descriptor_path=SUCCESSOR_DESCRIPTOR,
        check_live=True,
        require_lifecycle="source_project_ready",
    )
    successor_evaluation = evaluate_factory_queue(
        repo_root=repo_root,
        queue_path=SUCCESSOR_QUEUE,
        check_live=True,
    )
    successor_counts = successor_evaluation["counts"]
    if (
        successor_counts["verified_noop"] != 3
        or successor_counts["source_project_candidates"] != 0
        or successor_counts["render_candidates"] != 1
        or successor_counts["scheduled_for_render"] != 0
        or successor_counts["execution_set_size"] != 0
        or successor_counts["blocked_packages"] != 0
        or successor_counts["invalid_packages"] != 0
    ):
        _fail(
            "existing successor queue no longer has the bounded render plan",
            code="existing_successor_queue_result_drift",
            stage="preflight",
        )
    receipt_path = repo_root / PROMOTION_RECEIPT
    receipt = _load_json(receipt_path)
    observations = list(receipt.get("observations") or [])
    noop_observation = {
        "sequence": 2,
        "event": "verified_noop",
        "source_project_sha256": canonical_readback["source_project"]["sha256"],
        "source_project_size_bytes": canonical_readback["source_project"]["size_bytes"],
        "source_project_rewritten": False,
        "successor_descriptor_rewritten": False,
        "yymm4_launch_count": 0,
        "source_project_builder_launch_count": 0,
    }
    appended = noop_observation not in observations
    if appended:
        observations.append(noop_observation)
        receipt = _receipt(readback=canonical_readback, observations=observations)
        _write_json(receipt_path, receipt)
    stat = project.stat()
    return {
        "schema": PROMOTION_RESULT_SCHEMA,
        "schema_version": "1.0",
        "status": "verified_noop",
        "operation": "source_project_generation",
        "authority_id": AUTHORITY_ID,
        "package_id": PACKAGE_ID,
        "to_lifecycle": TARGET_LIFECYCLE,
        "source_project": {
            "path": SOURCE_PROJECT.as_posix(),
            "sha256": canonical_readback["source_project"]["sha256"],
            "size_bytes": stat.st_size,
            "mtime_ns_before": stat.st_mtime_ns,
            "mtime_ns_after": stat.st_mtime_ns,
            "rewritten": False,
        },
        "successor_descriptor_rewritten": False,
        "receipt_observation_appended": appended,
        "successor_queue_evaluation_sha256": successor_evaluation[
            "evaluation_sha256"
        ],
        "successor_queue_counts": successor_counts,
        "boundaries": _boundaries(),
    }


def _persist_failure(repo_root: Path, exc: FactorySourceProjectPromotionError) -> None:
    try:
        _write_json(
            repo_root / FAILURE_RECEIPT,
            {
                "schema": "nlmytgen.factory_source_project_promotion_failure.v1",
                "schema_version": "1.0",
                "status": "failed",
                "package_id": PACKAGE_ID,
                "stage": exc.stage,
                "error_code": exc.code,
                "message": str(exc),
                "boundaries": _boundaries(),
            },
        )
    except OSError:
        pass


def advance_factory_package(
    *,
    repo_root: Path,
    queue_path: Path,
    package_id: str,
    to_lifecycle: str,
    authority_id: str | None,
    execute: bool,
    render_authority_id: str | None = None,
    builder: Builder | None = None,
    persist_failure: bool = True,
) -> dict[str, Any]:
    """Plan or execute one exact source-project promotion."""

    root = repo_root.resolve()
    try:
        evaluation = evaluate_factory_queue(
            repo_root=root,
            queue_path=queue_path,
            check_live=True,
        )
        candidate = _validate_request(
            evaluation=evaluation,
            queue_path=queue_path,
            package_id=package_id,
            to_lifecycle=to_lifecycle,
            authority_id=authority_id,
            render_authority_id=render_authority_id,
        )
        predecessor_path = root / PREDECESSOR_DESCRIPTOR
        if sha256_file(predecessor_path) != PREDECESSOR_DESCRIPTOR_SHA256:
            _fail(
                "predecessor descriptor bytes changed",
                code="predecessor_descriptor_drift",
                stage="preflight",
            )
        predecessor = _load_json(predecessor_path)
        validate_factory_package_lifecycle(
            repo_root=root,
            descriptor_path=PREDECESSOR_DESCRIPTOR,
            check_live=True,
        )
        expected_rows, cue_sequence = _validate_predecessor_inputs(root, predecessor)
        output = _validate_output_locator(root, SOURCE_PROJECT)
        known_noop = _validate_known_noop(
            repo_root=root,
            predecessor=predecessor,
            expected_rows=expected_rows,
            cue_sequence=cue_sequence,
        )
        if known_noop is not None:
            return known_noop
        plan = _plan_payload(candidate, execute=execute)
        if not execute:
            return plan
        builder_impl = builder or _run_actual_builder
        builder_result = builder_impl(
            root,
            output,
            root / PACKAGE_ROOT / "derived_yymm4_import.csv",
        )
        readback = build_source_project_readback(
            repo_root=root,
            project_locator=SOURCE_PROJECT,
            predecessor=predecessor,
            cue_sequence=cue_sequence,
            expected_rows=expected_rows,
            builder_result=builder_result,
        )
        successor_descriptor = _build_successor_descriptor(predecessor, readback)
        predecessor_queue = _load_json(root / PREDECESSOR_QUEUE)
        successor_queue = _build_successor_queue(predecessor_queue)
        first_observation = {
            "sequence": 1,
            "event": "materialized",
            "source_project_sha256": readback["source_project"]["sha256"],
            "source_project_size_bytes": readback["source_project"]["size_bytes"],
            "yymm4_launch_count": int(builder_result.get("yymm4_launch_count", 0)),
            "source_project_builder_launch_count": int(
                builder_result.get("source_project_builder_launch_count", 0)
            ),
            "process_cleanup": bool(builder_result.get("process_cleanup", True)),
        }
        receipt = _receipt(readback=readback, observations=[first_observation])
        _write_or_verify_json(root / SOURCE_PROJECT_READBACK, readback)
        _write_or_verify_json(root / PROMOTION_RECEIPT, receipt)
        _write_or_verify_json(root / SUCCESSOR_DESCRIPTOR, successor_descriptor)
        _write_or_verify_json(root / SUCCESSOR_QUEUE, successor_queue)
        validate_factory_package_lifecycle(
            repo_root=root,
            descriptor_path=SUCCESSOR_DESCRIPTOR,
            check_live=True,
        )
        successor_evaluation = evaluate_factory_queue(
            repo_root=root,
            queue_path=SUCCESSOR_QUEUE,
            check_live=True,
        )
        counts = successor_evaluation["counts"]
        if (
            counts["verified_noop"] != 3
            or counts["source_project_candidates"] != 0
            or counts["render_candidates"] != 1
            or counts["scheduled_for_render"] != 0
            or counts["execution_set_size"] != 0
            or counts["blocked_packages"] != 0
            or counts["invalid_packages"] != 0
        ):
            _fail(
                "successor queue does not produce the bounded render-required plan",
                code="successor_queue_result_invalid",
                stage="validate",
            )
        food = [
            row
            for row in successor_evaluation["packages"]
            if row["package_id"] == PACKAGE_ID
        ][0]
        if (
            food["technical_decision"] != "render_required"
            or food["execution_eligible"] is not False
        ):
            _fail(
                "successor package unexpectedly became executable",
                code="successor_execution_authority_invalid",
                stage="validate",
            )
        return {
            "schema": PROMOTION_RESULT_SCHEMA,
            "schema_version": "1.0",
            "status": "promoted",
            "operation": "source_project_generation",
            "authority_id": AUTHORITY_ID,
            "package_id": PACKAGE_ID,
            "from_lifecycle": "package_prepared",
            "to_lifecycle": "source_project_ready",
            "content_identity_sha256_before": CONTENT_IDENTITY_SHA256,
            "content_identity_sha256_after": successor_descriptor["identities"][
                "content_identity_sha256"
            ],
            "source_project": copy.deepcopy(readback["source_project"]),
            "readback_path": SOURCE_PROJECT_READBACK.as_posix(),
            "promotion_receipt_path": PROMOTION_RECEIPT.as_posix(),
            "successor_descriptor_path": SUCCESSOR_DESCRIPTOR.as_posix(),
            "successor_queue_path": SUCCESSOR_QUEUE.as_posix(),
            "successor_queue_evaluation_sha256": successor_evaluation[
                "evaluation_sha256"
            ],
            "successor_queue_counts": counts,
            "boundaries": _boundaries(
                yymm4_launch_count=int(
                    builder_result.get("yymm4_launch_count", 0)
                ),
                source_project_builder_launch_count=int(
                    builder_result.get("source_project_builder_launch_count", 0)
                ),
            ),
        }
    except FactorySourceProjectPromotionError as exc:
        if persist_failure:
            _persist_failure(root, exc)
        raise


__all__ = [
    "AUTHORITY_ID",
    "FactorySourceProjectPromotionError",
    "PACKAGE_ID",
    "SOURCE_PROJECT",
    "SUCCESSOR_DESCRIPTOR",
    "SUCCESSOR_QUEUE",
    "TARGET_LIFECYCLE",
    "advance_factory_package",
    "build_source_project_readback",
]
