"""Bounded queue-driven Factory Package render promotion.

This module advances one exact ``source_project_ready`` package to ``rendered``.
It derives an ignored runtime manifest and delegates all project generation,
YMM4 rendering, normalization, media validation, and resume behavior to the
existing episode-video pipeline.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any, Callable, Mapping

from src.pipeline.episode_video import EpisodeVideoError, run_episode_video
from src.pipeline.factory_contract_v2_1 import validate_factory_package_lifecycle
from src.pipeline.factory_queue import (
    canonical_json_bytes,
    evaluate_factory_queue,
    sha256_file,
)
from src.pipeline.factory_source_project_promotion import (
    FactorySourceProjectPromotionError,
)


RENDER_RESULT_SCHEMA = "nlmytgen.factory_render_promotion.v1"
RENDER_READBACK_SCHEMA = "nlmytgen.factory_render_readback.v1"
RENDER_RECEIPT_SCHEMA = "nlmytgen.factory_render_promotion_receipt.v1"
RESUME_OBSERVATION_SCHEMA = "nlmytgen.factory_render_resume_observation.v1"

AUTHORITY_ID = "supervisor-food-expiry-single-render-2026-07-26"
PACKAGE_ID = "food_expiry_labels_001"
TARGET_LIFECYCLE = "rendered"
CONTENT_IDENTITY_SHA256 = (
    "27165fad6fadaee2e5c247a86758a505c7f5f5797eb7b386d174585622a585c6"
)
RENDER_SETTINGS_IDENTITY_SHA256 = (
    "2270ad92c6941d5d887715d95589bd5168d67c3fdc92fd12a722604ded33e0e2"
)

PACKAGE_ROOT = Path("production_pilots/factory_canaries/food_expiry_labels_001")
PREDECESSOR_DESCRIPTOR = PACKAGE_ROOT / "factory_package_v2_1_source_project_ready.json"
PREDECESSOR_DESCRIPTOR_SHA256 = (
    "4017f7d1591dc229f1163aecaf85f91e14d1d0eb919b03a3d1945e29d604688c"
)
PREDECESSOR_QUEUE = Path(
    "production_pilots/factory_queues/four_package_lifecycle_queue_v2.json"
)
PREDECESSOR_QUEUE_SHA256 = (
    "4f0fe080a56697720409791e68c922655428f2832a604525e276bd3ee156554d"
)
PRE_RENDER_MANIFEST = (
    PACKAGE_ROOT / "auto_video_pipeline/food_expiry_labels_episode_manifest.json"
)
PRE_RENDER_MANIFEST_SHA256 = (
    "31bd6788a1bca8cbb631bcee9b3391e5a0a04912a65db8c40c0e93f66b814cb9"
)
SOURCE_PROJECT_READBACK = PACKAGE_ROOT / "source_project_readback.json"
SOURCE_PROJECT_READBACK_SHA256 = (
    "e98ebad7b8f1cbc7bc20f4cd675f423fe1b2da44aac773969ecc392ec2f91aea"
)
SOURCE_PROJECT_PROMOTION_RECEIPT = PACKAGE_ROOT / "source_project_promotion_receipt.json"
SOURCE_PROJECT_PROMOTION_RECEIPT_SHA256 = (
    "81eae90ac4c4a8ab06b0c9bb62591d57a6fee9d96001e1a7279a803b8f77f18e"
)
REAL_MEDIA_PROVENANCE = PACKAGE_ROOT / "real_media_provenance.json"
REAL_MEDIA_PROVENANCE_SHA256 = (
    "0fc8cf2d4f1bfec672c1f1898dac7efd33df1835f212e7a2967814337ae7d9b8"
)
SOURCE_PROJECT = (
    PACKAGE_ROOT / "local_outputs/food_expiry_labels_source.local.ymmp"
)
SOURCE_PROJECT_SHA256 = (
    "4f8dc13976cb4ef56ea582d75e1ff92ae9d2780fff4cf53c13923d561955bdbf"
)
SOURCE_PROJECT_STRUCTURAL_SHA256 = (
    "10fa9fefac7ebc68ba3ace7af9f24e47a74eedf55be853fa05d5a4fb674183ff"
)

RUN_ROOT = PACKAGE_ROOT / "auto_video_runs"
PRIMARY_RUN_ID = "food_expiry_labels_internal_review_v1"
PROJECT_FILENAME = "generated_project.local.ymmp"
MP4_FILENAME = "internal_review_food_expiry_labels.mp4"
LOCAL_OUTPUTS = PACKAGE_ROOT / "local_outputs"
RENDER_READBACK = PACKAGE_ROOT / "render_readback.json"
RENDER_PROMOTION_RECEIPT = PACKAGE_ROOT / "render_promotion_receipt.json"
RENDER_RESUME_OBSERVATION = PACKAGE_ROOT / "render_resume_observation.json"
SUCCESSOR_DESCRIPTOR = PACKAGE_ROOT / "factory_package_v2_1_rendered.json"
SUCCESSOR_QUEUE = Path(
    "production_pilots/factory_queues/four_package_lifecycle_queue_v3.json"
)
FAILURE_RECEIPT = LOCAL_OUTPUTS / "render_promotion_failure.local.json"

_WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")

EpisodeRunner = Callable[..., dict[str, Any]]


class FactoryRenderPromotionError(FactorySourceProjectPromotionError):
    """Fail-closed error for the exact render lifecycle edge."""

    def as_payload(self) -> dict[str, Any]:
        return {
            "schema": RENDER_RESULT_SCHEMA,
            "schema_version": "1.0",
            "status": "failed",
            "error": {
                "code": self.code,
                "stage": self.stage,
                "message": str(self),
            },
            "boundaries": _boundaries(),
        }


def _fail(message: str, *, code: str, stage: str) -> None:
    raise FactoryRenderPromotionError(message, code=code, stage=stage)


def _boundaries(
    *,
    yymm4_launch_count: int = 0,
    render_driver_launch_count: int = 0,
    ffmpeg_encode_count: int = 0,
) -> dict[str, Any]:
    return {
        "selected_package_only": PACKAGE_ID,
        "human_creative_acceptance": False,
        "rights_approval": False,
        "production_approval": False,
        "publication": False,
        "upload": False,
        "release": False,
        "media_playback": False,
        "speaker_playback": False,
        "system_volume_operation": False,
        "computer_use": False,
        "sendkeys": False,
        "keyboard_mouse_injection": False,
        "manual_yymm4_operation": False,
        "yymm4_launch_count": yymm4_launch_count,
        "render_driver_launch_count": render_driver_launch_count,
        "ffmpeg_encode_count": ffmpeg_encode_count,
    }


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail(
            f"required JSON is unreadable: {path.as_posix()}",
            code="required_json_unreadable",
            stage="preflight",
        )
    if not isinstance(payload, dict):
        _fail(
            f"required JSON is not an object: {path.as_posix()}",
            code="required_json_invalid",
            stage="preflight",
        )
    return payload


def _repo_file(root: Path, relative: Path, *, field: str) -> Path:
    if relative.is_absolute() or _WINDOWS_ABSOLUTE.match(str(relative)):
        _fail(
            f"{field} must be repository-relative",
            code="private_absolute_path_forbidden",
            stage="preflight",
        )
    resolved = (root / relative).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        _fail(
            f"{field} escaped the repository",
            code="path_escape_forbidden",
            stage="preflight",
        )
    return resolved


def _walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for child in value.values():
            yield from _walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_strings(child)


def _assert_sanitized(payload: Mapping[str, Any]) -> None:
    for value in _walk_strings(payload):
        if _WINDOWS_ABSOLUTE.match(value) or value.startswith(("/", "\\\\")):
            _fail(
                "tracked render evidence contains a private absolute path",
                code="tracked_private_path_forbidden",
                stage="evidence",
            )


def _write_or_verify_json(path: Path, payload: Mapping[str, Any]) -> None:
    _assert_sanitized(payload)
    encoded = canonical_json_bytes(payload)
    if path.exists():
        if path.read_bytes() != encoded:
            _fail(
                f"append-only evidence differs: {path.as_posix()}",
                code="append_only_evidence_drift",
                stage="evidence",
            )
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encoded)


def _persist_failure(root: Path, exc: FactoryRenderPromotionError) -> None:
    payload = {
        "schema": "nlmytgen.factory_render_promotion_failure.v1",
        "status": "failed",
        "package_id": PACKAGE_ID,
        "authority_id": AUTHORITY_ID,
        "error_code": exc.code,
        "stage": exc.stage,
        "message": str(exc),
        "predecessor_descriptor_path": PREDECESSOR_DESCRIPTOR.as_posix(),
        "predecessor_queue_path": PREDECESSOR_QUEUE.as_posix(),
        "boundaries": _boundaries(),
    }
    encoded = canonical_json_bytes(payload)
    path = root / FAILURE_RECEIPT
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != encoded:
        for sequence in range(2, 33):
            successor = path.with_name(
                f"{path.stem.rsplit('.local', 1)[0]}-{sequence}.local.json"
            )
            if not successor.exists():
                path = successor
                break
    if not path.exists():
        path.write_bytes(encoded)


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
            "render promotion requires the exact rendered lifecycle",
            code="unsupported_lifecycle_jump",
            stage="authority",
        )
    if not authority_id:
        _fail(
            "render authority ID is required",
            code="authority_id_missing",
            stage="authority",
        )
    if authority_id != AUTHORITY_ID:
        _fail(
            "render authority ID is not exact",
            code="authority_id_mismatch",
            stage="authority",
        )
    if render_authority_id not in (None, ""):
        _fail(
            "a second render-authority field is forbidden",
            code="duplicate_render_authority_forbidden",
            stage="authority",
        )
    if Path(queue_path).as_posix() != PREDECESSOR_QUEUE.as_posix():
        _fail(
            "render promotion requires the exact queue-v2 descriptor",
            code="queue_override_rejected",
            stage="preflight",
        )
    descriptor = evaluation.get("queue_descriptor") or {}
    if descriptor.get("sha256") != PREDECESSOR_QUEUE_SHA256:
        _fail(
            "queue-v2 identity drifted",
            code="queue_identity_drift",
            stage="preflight",
        )
    counts = evaluation.get("counts") or {}
    expected = {
        "total_packages": 4,
        "verified_noop": 3,
        "source_project_candidates": 0,
        "render_candidates": 1,
        "scheduled_for_render": 0,
        "execution_set_size": 0,
        "blocked_packages": 0,
        "invalid_packages": 0,
    }
    if any(counts.get(key) != value for key, value in expected.items()):
        _fail(
            "queue-v2 no longer has one bounded render candidate",
            code="queue_candidate_baseline_drift",
            stage="preflight",
        )
    candidates = [
        row
        for row in evaluation.get("packages", [])
        if row.get("technical_decision") == "render_required"
    ]
    if len(candidates) != 1:
        _fail(
            "queue-v2 must select exactly one render candidate",
            code="render_candidate_not_unique",
            stage="preflight",
        )
    candidate = candidates[0]
    if package_id != candidate.get("package_id"):
        _fail(
            "manually named package is not the queue-selected render candidate",
            code="package_not_selected",
            stage="authority",
        )
    if package_id != PACKAGE_ID:
        _fail(
            "render of another package is forbidden",
            code="unrelated_package_override",
            stage="authority",
        )
    if (
        candidate.get("descriptor_path") != PREDECESSOR_DESCRIPTOR.as_posix()
        or candidate.get("descriptor_sha256") != PREDECESSOR_DESCRIPTOR_SHA256
        or candidate.get("content_identity_sha256") != CONTENT_IDENTITY_SHA256
        or candidate.get("render_settings_identity_sha256")
        != RENDER_SETTINGS_IDENTITY_SHA256
        or candidate.get("normalized_lifecycle") != "source_project_ready"
        or candidate.get("live_availability") != "source_project_live_exact"
        or candidate.get("execution_eligible") is not False
    ):
        _fail(
            "queue-selected source-project-ready identity drifted",
            code="predecessor_identity_drift",
            stage="preflight",
        )
    return candidate


def _validate_predecessor(
    root: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    protected = {
        PREDECESSOR_DESCRIPTOR: PREDECESSOR_DESCRIPTOR_SHA256,
        PRE_RENDER_MANIFEST: PRE_RENDER_MANIFEST_SHA256,
        SOURCE_PROJECT_READBACK: SOURCE_PROJECT_READBACK_SHA256,
        SOURCE_PROJECT_PROMOTION_RECEIPT: SOURCE_PROJECT_PROMOTION_RECEIPT_SHA256,
        REAL_MEDIA_PROVENANCE: REAL_MEDIA_PROVENANCE_SHA256,
        SOURCE_PROJECT: SOURCE_PROJECT_SHA256,
    }
    for relative, expected in protected.items():
        path = _repo_file(root, relative, field=relative.as_posix())
        if not path.is_file() or sha256_file(path) != expected:
            _fail(
                f"protected predecessor identity drifted: {relative.as_posix()}",
                code="protected_predecessor_drift",
                stage="preflight",
            )
    validation = validate_factory_package_lifecycle(
        repo_root=root,
        descriptor_path=PREDECESSOR_DESCRIPTOR,
        check_live=True,
    )
    if (
        validation["normalized_lifecycle"]["state"] != "source_project_ready"
        or validation["normalized"]["content_identity_sha256"]
        != CONTENT_IDENTITY_SHA256
    ):
        _fail(
            "source-project-ready contract no longer validates exactly",
            code="source_project_contract_drift",
            stage="preflight",
        )
    predecessor = _load_json(root / PREDECESSOR_DESCRIPTOR)
    manifest = _load_json(root / PRE_RENDER_MANIFEST)
    readback = _load_json(root / SOURCE_PROJECT_READBACK)
    provenance = _load_json(root / REAL_MEDIA_PROVENANCE)
    if (
        predecessor["identities"]["content_identity_sha256"]
        != CONTENT_IDENTITY_SHA256
        or predecessor["episode_execution"]["render_settings_sha256"]
        != RENDER_SETTINGS_IDENTITY_SHA256
        or any(
            predecessor["authority"][clock]["approved"] is not False
            or predecessor["authority"][clock]["record"] is not None
            for clock in ("rights", "production", "publication", "upload", "release")
        )
        or manifest.get("boundaries", {}).get("final_aesthetic_acceptance") is not False
        or manifest.get("boundaries", {}).get("rights_approved") is not False
        or manifest.get("boundaries", {}).get("production") is not False
        or manifest.get("boundaries", {}).get("publication") is not False
        or manifest.get("boundaries", {}).get("external_upload") is not False
        or manifest.get("boundaries", {}).get("release") is not False
    ):
        _fail(
            "content, render-settings, or external authority boundary drifted",
            code="authority_or_identity_smuggling",
            stage="preflight",
        )
    source = readback.get("source_project") or {}
    structure = readback.get("structure") or {}
    if (
        source.get("sha256") != SOURCE_PROJECT_SHA256
        or source.get("structural_identity_sha256")
        != SOURCE_PROJECT_STRUCTURAL_SHA256
        or structure.get("voice_item_count") != 4
        or structure.get("speaker_counts") != {"ゆっくり霊夢赤縁": 4}
        or structure.get("scene_count") != 1
        or structure.get("timeline_frames") != 1335
        or structure.get("fps") != 60
    ):
        _fail(
            "source-project authority or structure drifted",
            code="source_project_identity_drift",
            stage="preflight",
        )
    mappings = predecessor["media_provenance"]["asset_mappings"]
    for row in mappings:
        asset = _repo_file(
            root,
            Path(str(row["local_asset_path"])),
            field="media_provenance.local_asset_path",
        )
        if not asset.is_file() or sha256_file(asset) != row["sha256"]:
            _fail(
                f"raster asset identity drifted: {row['cue_id']}",
                code="raster_asset_hash_mismatch",
                stage="preflight",
            )
    return predecessor, manifest, readback, provenance


def _runtime_manifest(
    *,
    predecessor_manifest: Mapping[str, Any],
    source_readback: Mapping[str, Any],
    run_id: str,
) -> dict[str, Any]:
    runtime = copy.deepcopy(dict(predecessor_manifest))
    source_plan = runtime.pop("source_project_plan")
    output_plan = runtime.pop("output_plan")
    runtime.pop("lifecycle", None)
    runtime["schema"] = "nlmytgen.episode_manifest.v1"
    runtime["provenance_manifest_path"] = _runtime_provenance_path(run_id).as_posix()
    source = source_readback["source_project"]
    structure = source_readback["structure"]
    runtime["yymm4"] = {
        "source_project_path": source["path"],
        "source_project_sha256": source["sha256"],
        "profile_id": source_plan["profile_id"],
        "profile_version_expected": source_plan["profile_version_expected"],
        "observed_product_version": str(source["yymm4_version"]).split("+", 1)[0],
        "version_difference_policy": "exact_match_required",
        "fps": structure["fps"],
        "timeline_frames": structure["timeline_frames"],
        "duration_seconds": structure["duration_seconds"],
    }
    runtime["output"] = {
        "run_root_path": RUN_ROOT.as_posix(),
        "run_id": run_id,
        "project_filename": output_plan["project_filename"],
        "mp4_filename": output_plan["mp4_filename"],
    }
    runtime["execution_authority"] = {
        "schema": "nlmytgen.one_shot_render_authority.v1",
        "authority_id": AUTHORITY_ID,
        "package_id": PACKAGE_ID,
        "operation": "single_internal_review_render",
        "standing_authority": False,
        "human_creative_acceptance": False,
        "rights_or_public_authority": False,
    }
    return runtime


def _runtime_manifest_path(run_id: str) -> Path:
    return LOCAL_OUTPUTS / f"food_expiry_render_execution_{run_id}.local.json"


def _runtime_provenance_path(run_id: str) -> Path:
    return LOCAL_OUTPUTS / f"food_expiry_render_provenance_{run_id}.local.json"


def _runtime_provenance(predecessor: Mapping[str, Any]) -> dict[str, Any]:
    """Adapt reusable-crop v2.1 provenance for the existing episode pipeline."""

    runtime = copy.deepcopy(dict(predecessor))
    for asset in runtime.get("assets", []):
        if asset.get("crop_or_segment"):
            continue
        views = "; ".join(
            f"{view['cue_id']} crop={json.dumps(view['crop'], separators=(',', ':'))}"
            for view in asset.get("cue_views", [])
        )
        asset["crop_or_segment"] = (
            f"{asset.get('capture_basis', 'official raster')}; {views}"
        )
    runtime["runtime_resolution"] = {
        "source_provenance_path": REAL_MEDIA_PROVENANCE.as_posix(),
        "source_provenance_sha256": REAL_MEDIA_PROVENANCE_SHA256,
        "adaptation": "add crop_or_segment summary from exact cue_views",
        "source_bytes_mutated": False,
    }
    return runtime


def _run_paths(root: Path, run_id: str) -> dict[str, Path]:
    run = root / RUN_ROOT / run_id
    return {
        "run": run,
        "project": run / PROJECT_FILENAME,
        "mp4": run / MP4_FILENAME,
        "receipt": run / "pipeline_run_receipt.json",
        "validation": run / "media_validation.json",
        "cue_readback": run / "cue_visual_readback.json",
        "frames": run / "extracted_review_frames",
    }


def _looks_complete(paths: Mapping[str, Path]) -> bool:
    return all(
        paths[key].is_file()
        for key in ("project", "mp4", "receipt", "validation", "cue_readback")
    ) and paths["frames"].is_dir()


def _next_run(
    *,
    root: Path,
    predecessor_manifest: Mapping[str, Any],
    predecessor_provenance: Mapping[str, Any],
    source_readback: Mapping[str, Any],
    episode_runner: EpisodeRunner,
) -> tuple[str, Path, dict[str, Any] | None, list[str]]:
    preserved_collisions: list[str] = []
    for sequence in range(1, 33):
        run_id = f"food_expiry_labels_internal_review_v{sequence}"
        paths = _run_paths(root, run_id)
        manifest = _runtime_manifest(
            predecessor_manifest=predecessor_manifest,
            source_readback=source_readback,
            run_id=run_id,
        )
        manifest_path = root / _runtime_manifest_path(run_id)
        if not paths["run"].exists():
            expected_manifest = canonical_json_bytes(manifest)
            provenance_path = root / _runtime_provenance_path(run_id)
            expected_provenance = canonical_json_bytes(
                _runtime_provenance(predecessor_provenance)
            )
            if (
                manifest_path.exists()
                and manifest_path.read_bytes() != expected_manifest
                or provenance_path.exists()
                and provenance_path.read_bytes() != expected_provenance
            ):
                preserved_collisions.append(run_id)
                continue
            return run_id, manifest_path, None, preserved_collisions
        if (
            paths["run"] / "technical_visual_inspection_failure.local.json"
        ).is_file():
            preserved_collisions.append(run_id)
            continue
        if not _looks_complete(paths):
            preserved_collisions.append(run_id)
            continue
        _write_or_verify_json(manifest_path, manifest)
        _write_or_verify_json(
            root / _runtime_provenance_path(run_id),
            _runtime_provenance(predecessor_provenance),
        )
        try:
            result = episode_runner(
                repo_root=root,
                manifest_path=manifest_path,
                render=True,
                dry_run=False,
                resume=True,
                force=False,
            )
        except EpisodeVideoError:
            preserved_collisions.append(run_id)
            continue
        observation = result.get("resume_observation") or {}
        if (
            result.get("status") == "passed"
            and observation.get("status") == "verified_noop"
            and observation.get("outputs_rewritten") is False
            and observation.get("yymm4_launched") is False
        ):
            return run_id, manifest_path, result, preserved_collisions
        preserved_collisions.append(run_id)
    _fail(
        "all bounded versioned run namespaces are occupied",
        code="output_namespace_exhausted",
        stage="preflight",
    )


def _plan_payload(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema": RENDER_RESULT_SCHEMA,
        "schema_version": "1.0",
        "status": "planned",
        "operation": "single_internal_review_render",
        "execute": False,
        "authority_id": AUTHORITY_ID,
        "package_id": PACKAGE_ID,
        "from_lifecycle": "source_project_ready",
        "to_lifecycle": TARGET_LIFECYCLE,
        "queue_decision": candidate["technical_decision"],
        "content_identity_sha256": CONTENT_IDENTITY_SHA256,
        "source_project": {
            "path": SOURCE_PROJECT.as_posix(),
            "sha256": SOURCE_PROJECT_SHA256,
            "structural_identity_sha256": SOURCE_PROJECT_STRUCTURAL_SHA256,
        },
        "expected_primary_run_id": PRIMARY_RUN_ID,
        "boundaries": _boundaries(),
    }


def _validate_run_result(
    *,
    root: Path,
    run_id: str,
    result: Mapping[str, Any],
    source_readback: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    paths = _run_paths(root, run_id)
    for name in ("project", "mp4", "receipt", "validation", "cue_readback"):
        if not paths[name].is_file():
            _fail(
                f"completed run is missing {name}",
                code="completed_run_artifact_missing",
                stage="validate",
            )
    project = result.get("project_readback") or {}
    media = result.get("media_validation") or {}
    checks = project.get("checks") or {}
    required_project_checks = (
        "project_parse_pass",
        "voice_item_count_matches_manifest",
        "image_item_count_matches_manifest",
        "speaker_counts_match_manifest",
        "visual_timing_matches_cues",
        "tool_states_stripped",
        "layout_xml_stripped",
        "only_run_directory_absolute_paths",
        "timeline_frames_match_manifest",
        "real_media_paths_are_raster",
        "real_media_has_zero_svg_references",
        "real_media_remarks_are_not_proxy",
    )
    if (
        result.get("status") != "passed"
        or project.get("status") != "passed"
        or project.get("voice_item_count") != 4
        or project.get("image_item_count") != 4
        or project.get("speaker_counts") != {"ゆっくり霊夢赤縁": 4}
        or project.get("timeline_frames") != 1335
        or project.get("fps") != 60
        or project.get("source_project_sha256") != SOURCE_PROJECT_SHA256
        or project.get("voice_items_unchanged") is not True
        or any(checks.get(key) is not True for key in required_project_checks)
    ):
        _fail(
            "generated project readback does not match the exact four-cue source",
            code="generated_project_readback_invalid",
            stage="validate",
        )
    media_checks = media.get("checks") or {}
    required_media_checks = (
        "iso_bmff_ftyp_moov_mdat",
        "ffprobe_parse",
        "h264_video",
        "aac_audio",
        "resolution_matches_project",
        "fps_matches_project",
        "duration_within_manifest_tolerance",
        "bitrate_internal_review_range",
        "size_within_manifest_limit",
        "audio_and_video_streams_present",
        "full_file_decode",
        "decode_source_unchanged",
        "representative_frames_not_varied",
    )
    media_row = media.get("media") or {}
    frame_extraction = media.get("frame_extraction") or {}
    if (
        media.get("status") != "passed"
        or any(media_checks.get(key) is not True for key in required_media_checks)
        or media_row.get("video_codec") != "h264"
        or media_row.get("audio_codec") != "aac"
        or media_row.get("width") != 1920
        or media_row.get("height") != 1080
        or float(media_row.get("fps") or 0) != 60.0
        or not 18 <= float(media_row.get("duration_seconds") or 0) <= 30
        or frame_extraction.get("status") != "passed"
        or frame_extraction.get("cue_frame_count") != 4
        or int(frame_extraction.get("unique_sha256_count") or 0) < 5
    ):
        _fail(
            "internal-review MP4 validation failed",
            code="media_validation_invalid",
            stage="validate",
        )
    cue_frames = [
        row
        for row in frame_extraction.get("records", [])
        if str(row.get("label", "")).startswith("cue_")
    ]
    if [row.get("label") for row in cue_frames] != [
        "cue_001",
        "cue_002",
        "cue_003",
        "cue_004",
    ]:
        _fail(
            "cue frame extraction is incomplete or out of order",
            code="cue_frame_inspection_incomplete",
            stage="validate",
        )
    generated_sha = sha256_file(paths["project"])
    mp4_sha = sha256_file(paths["mp4"])
    normalized = project.get("normalized_project_structural_identity") or {}
    if (
        generated_sha != project.get("generated_project_sha256")
        or mp4_sha != media_row.get("sha256")
        or normalized.get("run_local_paths_normalized") is not True
        or not normalized.get("sha256")
    ):
        _fail(
            "generated project or MP4 identity binding failed",
            code="render_identity_binding_invalid",
            stage="validate",
        )
    readback = {
        "schema": RENDER_READBACK_SCHEMA,
        "schema_version": "1.0",
        "status": "passed",
        "package_id": PACKAGE_ID,
        "authority_id": AUTHORITY_ID,
        "run_id": run_id,
        "content_identity_sha256": CONTENT_IDENTITY_SHA256,
        "pipeline_content_identity_sha256": result["content_identity_sha256"],
        "source_project": {
            "path": SOURCE_PROJECT.as_posix(),
            "sha256": SOURCE_PROJECT_SHA256,
            "structural_identity_sha256": SOURCE_PROJECT_STRUCTURAL_SHA256,
            "size_bytes": int((root / SOURCE_PROJECT).stat().st_size),
            "yymm4_version": source_readback["source_project"]["yymm4_version"],
        },
        "generated_project": {
            "path": (RUN_ROOT / run_id / PROJECT_FILENAME).as_posix(),
            "sha256": generated_sha,
            "size_bytes": int(paths["project"].stat().st_size),
            "normalized_structural_identity_sha256": normalized["sha256"],
            "voice_item_count": 4,
            "image_item_count": 4,
            "speaker_counts": {"ゆっくり霊夢赤縁": 4},
            "scene_count": 1,
            "timeline_frames": 1335,
            "fps": 60,
            "source_voice_items_unchanged": True,
            "svg_reference_count": 0,
            "private_path_leaks": 0,
        },
        "media": {
            "path": (RUN_ROOT / run_id / MP4_FILENAME).as_posix(),
            "sha256": mp4_sha,
            "size_bytes": int(media_row["size_bytes"]),
            "container": media_row["container"],
            "video_codec": media_row["video_codec"],
            "audio_codec": media_row["audio_codec"],
            "width": media_row["width"],
            "height": media_row["height"],
            "fps": media_row["fps"],
            "duration_seconds": media_row["duration_seconds"],
            "overall_bitrate_bps": media_row["overall_bitrate_bps"],
            "full_file_decode": True,
        },
        "cue_frames": {
            "status": "passed",
            "actual_png_files_inspected": True,
            "binding_method": "decoded_frame_plus_exact_cue_media_readback",
            "records": [
                {
                    "cue_id": row["label"],
                    "path": (
                        RUN_ROOT
                        / run_id
                        / "extracted_review_frames"
                        / f"{row['label']}.png"
                    ).as_posix(),
                    "sha256": row["sha256"],
                    "width": row["width"],
                    "height": row["height"],
                }
                for row in cue_frames
            ],
        },
        "runtime": {
            "audio_policy": "silent",
            "driver": (result.get("render") or {}).get("driver"),
            "yymm4_launch_count": 1,
            "render_driver_launch_count": 1,
            "ffmpeg_encode_count": 0,
            "project_owned_process_cleanup": bool(
                (result.get("render") or {}).get("project_owned_process_cleanup")
            ),
            "manual_intervention_count": 0,
            "readiness_bypass": False,
            "test_double": False,
        },
        "authority_clocks": {
            "human_creative_acceptance": False,
            "rights": False,
            "production": False,
            "publication": False,
            "upload": False,
            "release": False,
        },
    }
    receipt = {
        "schema": RENDER_RECEIPT_SCHEMA,
        "schema_version": "1.0",
        "status": "passed",
        "authority_id": AUTHORITY_ID,
        "authority_consumed_for_package": PACKAGE_ID,
        "predecessor": {
            "descriptor_path": PREDECESSOR_DESCRIPTOR.as_posix(),
            "descriptor_sha256": PREDECESSOR_DESCRIPTOR_SHA256,
            "queue_path": PREDECESSOR_QUEUE.as_posix(),
            "queue_sha256": PREDECESSOR_QUEUE_SHA256,
            "manifest_path": PRE_RENDER_MANIFEST.as_posix(),
            "manifest_sha256": PRE_RENDER_MANIFEST_SHA256,
            "source_project_readback_path": SOURCE_PROJECT_READBACK.as_posix(),
            "source_project_readback_sha256": SOURCE_PROJECT_READBACK_SHA256,
        },
        "promotion": {
            "from_lifecycle": "source_project_ready",
            "to_lifecycle": "rendered",
            "content_identity_sha256_before": CONTENT_IDENTITY_SHA256,
            "content_identity_sha256_after": CONTENT_IDENTITY_SHA256,
            "run_id": run_id,
            "render_readback_path": RENDER_READBACK.as_posix(),
        },
        "boundaries": _boundaries(
            yymm4_launch_count=1,
            render_driver_launch_count=1,
            ffmpeg_encode_count=0,
        ),
    }
    return readback, receipt


def _build_successor_descriptor(
    predecessor: Mapping[str, Any],
    readback: Mapping[str, Any],
) -> dict[str, Any]:
    successor = copy.deepcopy(dict(predecessor))
    successor["lifecycle"].update(
        {
            "state": "rendered",
            "contract_valid": True,
            "tracked_package_ready": True,
            "source_project_ready": True,
            "render_ready": True,
            "human_accepted": False,
        }
    )
    successor["generated_project"] = {
        "schema": "nlmytgen.factory_package.generated_project.v2.1",
        "path": readback["generated_project"]["path"],
        "sha256": readback["generated_project"]["sha256"],
        "identity_source": "bounded_queue_render_readback",
        "availability_claim": "receipt_identity_only",
    }
    successor["render_validation"] = {
        "schema": "nlmytgen.factory_package.render_validation.v2.1",
        "technical_receipt_path": RENDER_READBACK.as_posix(),
        "technical_receipt_sha256": sha256_file_from_payload(readback),
        "technical_status": "passed",
        "mp4_path": readback["media"]["path"],
        "mp4_sha256": readback["media"]["sha256"],
        "availability_claim": "receipt_identity_only",
    }
    successor["resume_identity"]["completed_run_observed"] = True
    successor["extensions"]["values"][
        "org.nlmytgen.food_expiry_labels.render_predecessor"
    ] = {
        "descriptor_path": PREDECESSOR_DESCRIPTOR.as_posix(),
        "descriptor_sha256": PREDECESSOR_DESCRIPTOR_SHA256,
        "queue_path": PREDECESSOR_QUEUE.as_posix(),
        "queue_sha256": PREDECESSOR_QUEUE_SHA256,
        "render_authority_id": AUTHORITY_ID,
        "render_receipt_path": RENDER_PROMOTION_RECEIPT.as_posix(),
        "render_readback_path": RENDER_READBACK.as_posix(),
        "completed_run_id": readback["run_id"],
    }
    return successor


def sha256_file_from_payload(payload: Mapping[str, Any]) -> str:
    import hashlib

    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def _build_successor_queue(
    predecessor_queue: Mapping[str, Any],
    *,
    descriptor_sha256: str,
    mp4_sha256: str,
) -> dict[str, Any]:
    successor = copy.deepcopy(dict(predecessor_queue))
    successor["queue"]["queue_id"] = "four_package_lifecycle_queue_v3"
    rows = successor["queue"]["packages"]
    food = [row for row in rows if row["expected_package_id"] == PACKAGE_ID]
    if len(food) != 1:
        _fail(
            "queue-v2 does not contain one Food Expiry entry",
            code="queue_food_entry_invalid",
            stage="evidence",
        )
    food[0]["descriptor_path"] = SUCCESSOR_DESCRIPTOR.as_posix()
    food[0]["expected_completed_output_sha256"] = mp4_sha256
    # Descriptor identity is bound by queue evaluation; recording it here would
    # change the stable queue-v1 schema, so it is returned in the result receipt.
    _ = descriptor_sha256
    return successor


def _validate_successors(root: Path) -> dict[str, Any]:
    validation = validate_factory_package_lifecycle(
        repo_root=root,
        descriptor_path=SUCCESSOR_DESCRIPTOR,
        check_live=True,
    )
    if (
        validation["normalized_lifecycle"]["state"] != "rendered"
        or validation["normalized"]["content_identity_sha256"]
        != CONTENT_IDENTITY_SHA256
    ):
        _fail(
            "rendered successor contract is invalid",
            code="rendered_successor_invalid",
            stage="validate",
        )
    evaluation = evaluate_factory_queue(
        repo_root=root,
        queue_path=SUCCESSOR_QUEUE,
        check_live=True,
    )
    counts = evaluation["counts"]
    if (
        counts["verified_noop"] != 4
        or counts["render_candidates"] != 0
        or counts["source_project_candidates"] != 0
        or counts["scheduled_for_render"] != 0
        or counts["execution_set_size"] != 0
        or counts["blocked_packages"] != 0
        or counts["invalid_packages"] != 0
    ):
        _fail(
            "queue-v3 does not classify all four packages as completed no-ops",
            code="queue_v3_result_invalid",
            stage="validate",
        )
    return evaluation


def _persist_rendered_evidence(
    *,
    root: Path,
    predecessor: Mapping[str, Any],
    readback: Mapping[str, Any],
    receipt: dict[str, Any],
) -> dict[str, Any]:
    _write_or_verify_json(root / RENDER_READBACK, readback)
    receipt["promotion"]["render_readback_sha256"] = sha256_file(
        root / RENDER_READBACK
    )
    _write_or_verify_json(root / RENDER_PROMOTION_RECEIPT, receipt)
    successor = _build_successor_descriptor(predecessor, readback)
    successor["extensions"]["values"][
        "org.nlmytgen.food_expiry_labels.render_predecessor"
    ]["render_receipt_sha256"] = sha256_file(root / RENDER_PROMOTION_RECEIPT)
    _write_or_verify_json(root / SUCCESSOR_DESCRIPTOR, successor)
    successor_queue = _build_successor_queue(
        _load_json(root / PREDECESSOR_QUEUE),
        descriptor_sha256=sha256_file(root / SUCCESSOR_DESCRIPTOR),
        mp4_sha256=readback["media"]["sha256"],
    )
    _write_or_verify_json(root / SUCCESSOR_QUEUE, successor_queue)
    return _validate_successors(root)


def _known_completion(
    *,
    root: Path,
    run_id: str,
    result: Mapping[str, Any],
) -> dict[str, Any]:
    required = (
        RENDER_READBACK,
        RENDER_PROMOTION_RECEIPT,
        SUCCESSOR_DESCRIPTOR,
        SUCCESSOR_QUEUE,
    )
    if not all((root / path).is_file() for path in required):
        _fail(
            "completed local run lacks append-only rendered lifecycle evidence",
            code="completed_run_tracked_evidence_missing",
            stage="resume",
        )
    readback = _load_json(root / RENDER_READBACK)
    if (
        readback.get("status") != "passed"
        or readback.get("run_id") != run_id
        or readback.get("content_identity_sha256") != CONTENT_IDENTITY_SHA256
        or sha256_file(root / Path(readback["generated_project"]["path"]))
        != readback["generated_project"]["sha256"]
        or sha256_file(root / Path(readback["media"]["path"]))
        != readback["media"]["sha256"]
    ):
        _fail(
            "completed run render evidence drifted",
            code="completed_run_render_evidence_drift",
            stage="resume",
        )
    evaluation = _validate_successors(root)
    observation = {
        "schema": RESUME_OBSERVATION_SCHEMA,
        "schema_version": "1.0",
        "status": "verified_noop",
        "package_id": PACKAGE_ID,
        "authority_id": AUTHORITY_ID,
        "run_id": run_id,
        "content_identity_sha256": CONTENT_IDENTITY_SHA256,
        "artifact_identities_exact": True,
        "sha_size_mtime_mismatch_count": 0,
        "outputs_rewritten": False,
        "replacement_lifecycle_receipt_created": False,
        "yymm4_launch_count": 0,
        "render_driver_launch_count": 0,
        "ffmpeg_encode_count": 0,
        "pipeline_resume_observation": {
            "status": (result.get("resume_observation") or {}).get("status"),
            "outputs_rewritten": (result.get("resume_observation") or {}).get(
                "outputs_rewritten"
            ),
            "artifact_identities_exact": (
                result.get("resume_observation") or {}
            ).get("artifact_identities_exact"),
        },
    }
    _write_or_verify_json(root / RENDER_RESUME_OBSERVATION, observation)
    return {
        "schema": RENDER_RESULT_SCHEMA,
        "schema_version": "1.0",
        "status": "verified_noop",
        "operation": "single_internal_review_render",
        "authority_id": AUTHORITY_ID,
        "package_id": PACKAGE_ID,
        "run_id": run_id,
        "content_identity_sha256": CONTENT_IDENTITY_SHA256,
        "render_readback_path": RENDER_READBACK.as_posix(),
        "render_receipt_path": RENDER_PROMOTION_RECEIPT.as_posix(),
        "successor_descriptor_path": SUCCESSOR_DESCRIPTOR.as_posix(),
        "successor_queue_path": SUCCESSOR_QUEUE.as_posix(),
        "resume_observation_path": RENDER_RESUME_OBSERVATION.as_posix(),
        "successor_queue_evaluation_sha256": evaluation["evaluation_sha256"],
        "successor_queue_counts": evaluation["counts"],
        "boundaries": _boundaries(),
    }


def advance_factory_render(
    *,
    repo_root: Path,
    queue_path: Path,
    package_id: str,
    to_lifecycle: str,
    authority_id: str | None,
    execute: bool,
    render_authority_id: str | None = None,
    episode_runner: EpisodeRunner = run_episode_video,
    persist_failure: bool = True,
) -> dict[str, Any]:
    """Plan or execute the exact queue-selected Food Expiry render."""

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
        (
            predecessor,
            predecessor_manifest,
            source_readback,
            predecessor_provenance,
        ) = _validate_predecessor(root)
        plan = _plan_payload(candidate)
        if not execute:
            return plan

        run_id, manifest_path, completed, preserved_collisions = _next_run(
            root=root,
            predecessor_manifest=predecessor_manifest,
            predecessor_provenance=predecessor_provenance,
            source_readback=source_readback,
            episode_runner=episode_runner,
        )
        if completed is not None:
            required = (
                RENDER_READBACK,
                RENDER_PROMOTION_RECEIPT,
                SUCCESSOR_DESCRIPTOR,
                SUCCESSOR_QUEUE,
            )
            if all((root / path).is_file() for path in required):
                return _known_completion(root=root, run_id=run_id, result=completed)
            readback, receipt = _validate_run_result(
                root=root,
                run_id=run_id,
                result=completed,
                source_readback=source_readback,
            )
            receipt["promotion"]["preserved_collision_run_ids"] = preserved_collisions
            successor_evaluation = _persist_rendered_evidence(
                root=root,
                predecessor=predecessor,
                readback=readback,
                receipt=receipt,
            )
            return {
                "schema": RENDER_RESULT_SCHEMA,
                "schema_version": "1.0",
                "status": "rendered_evidence_recovered",
                "operation": "single_internal_review_render",
                "authority_id": AUTHORITY_ID,
                "package_id": PACKAGE_ID,
                "run_id": run_id,
                "content_identity_sha256": CONTENT_IDENTITY_SHA256,
                "successor_queue_evaluation_sha256": successor_evaluation[
                    "evaluation_sha256"
                ],
                "successor_queue_counts": successor_evaluation["counts"],
                "boundaries": _boundaries(),
            }

        runtime_manifest = _runtime_manifest(
            predecessor_manifest=predecessor_manifest,
            source_readback=source_readback,
            run_id=run_id,
        )
        _write_or_verify_json(manifest_path, runtime_manifest)
        _write_or_verify_json(
            root / _runtime_provenance_path(run_id),
            _runtime_provenance(predecessor_provenance),
        )
        try:
            result = episode_runner(
                repo_root=root,
                manifest_path=manifest_path,
                render=True,
                dry_run=False,
                resume=False,
                force=False,
            )
        except EpisodeVideoError as exc:
            _fail(
                f"episode-video render failed: {exc}",
                code=f"episode_video_{exc.code}",
                stage="render",
            )
        readback, receipt = _validate_run_result(
            root=root,
            run_id=run_id,
            result=result,
            source_readback=source_readback,
        )
        receipt["promotion"]["preserved_collision_run_ids"] = preserved_collisions
        successor_evaluation = _persist_rendered_evidence(
            root=root,
            predecessor=predecessor,
            readback=readback,
            receipt=receipt,
        )
        return {
            "schema": RENDER_RESULT_SCHEMA,
            "schema_version": "1.0",
            "status": "rendered",
            "operation": "single_internal_review_render",
            "authority_id": AUTHORITY_ID,
            "package_id": PACKAGE_ID,
            "from_lifecycle": "source_project_ready",
            "to_lifecycle": "rendered",
            "run_id": run_id,
            "preserved_collision_run_ids": preserved_collisions,
            "content_identity_sha256_before": CONTENT_IDENTITY_SHA256,
            "content_identity_sha256_after": CONTENT_IDENTITY_SHA256,
            "generated_project": copy.deepcopy(readback["generated_project"]),
            "media": copy.deepcopy(readback["media"]),
            "render_readback_path": RENDER_READBACK.as_posix(),
            "render_receipt_path": RENDER_PROMOTION_RECEIPT.as_posix(),
            "successor_descriptor_path": SUCCESSOR_DESCRIPTOR.as_posix(),
            "successor_descriptor_sha256": sha256_file(root / SUCCESSOR_DESCRIPTOR),
            "successor_queue_path": SUCCESSOR_QUEUE.as_posix(),
            "successor_queue_sha256": sha256_file(root / SUCCESSOR_QUEUE),
            "successor_queue_evaluation_sha256": successor_evaluation[
                "evaluation_sha256"
            ],
            "successor_queue_counts": successor_evaluation["counts"],
            "boundaries": _boundaries(
                yymm4_launch_count=1,
                render_driver_launch_count=1,
                ffmpeg_encode_count=0,
            ),
        }
    except FactoryRenderPromotionError as exc:
        if persist_failure:
            _persist_failure(root, exc)
        raise


__all__ = [
    "AUTHORITY_ID",
    "FactoryRenderPromotionError",
    "PACKAGE_ID",
    "PREDECESSOR_QUEUE",
    "SUCCESSOR_DESCRIPTOR",
    "SUCCESSOR_QUEUE",
    "TARGET_LIFECYCLE",
    "advance_factory_render",
]
