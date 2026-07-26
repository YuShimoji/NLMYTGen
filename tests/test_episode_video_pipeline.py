from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import pytest

from src.pipeline import episode_video
from src.pipeline.episode_video import (
    EpisodeVideoError,
    IMAGE_ITEM_TYPE,
    MANIFEST_SCHEMA,
    VOICE_ITEM_TYPE,
    build_pipeline_paths,
    build_content_identity,
    build_render_driver_command,
    build_yymm4_project,
    load_episode_manifest,
    normalize_review_mp4,
    preflight_episode,
    run_episode_video,
    validate_run_id,
)


LENGTHS = [391, 705, 338, 384, 407, 610, 427, 733, 420]
SPEAKERS = [
    "ゆっくり霊夢",
    "ゆっくり魔理沙",
    "ゆっくり魔理沙",
    "ゆっくり魔理沙",
    "ゆっくり霊夢",
    "ゆっくり魔理沙",
    "ゆっくり魔理沙",
    "ゆっくり霊夢",
    "ゆっくり魔理沙",
]
SCENES = ["S1", "S1", "S2", "S2", "S2", "S2", "S3", "S3", "S3"]
ROOT = Path(__file__).resolve().parents[1]
PILOT_PIPELINE = ROOT / (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001/auto_video_pipeline"
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _synthetic_episode(tmp_path: Path) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "inputs").mkdir()
    (repo / "visuals").mkdir()
    (repo / "inputs" / "source-package.json").write_text("{}\n", encoding="utf-8")
    (repo / "inputs" / "approval.json").write_text("{}\n", encoding="utf-8")
    texts = [f"approved line {index}" for index in range(1, 10)]

    with (repo / "inputs" / "derived.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(zip(SPEAKERS, texts, strict=True))

    frame = 0
    voices = []
    cue_mapping = []
    for index, (length, speaker, scene, text) in enumerate(
        zip(LENGTHS, SPEAKERS, SCENES, texts, strict=True), start=1
    ):
        cue_id = f"cue_{index:03d}"
        visual_id = f"visual_{index:03d}"
        voices.append(
            {
                "$type": VOICE_ITEM_TYPE,
                "CharacterName": speaker,
                "Serif": text,
                "Frame": frame,
                "Length": length,
                "SyntheticSentinel": {"index": index},
            }
        )
        frame += length
        cue_mapping.append(
            {
                "cue_id": cue_id,
                "scene_id": scene,
                "speaker": speaker,
                "visual_id": visual_id,
            }
        )
        (repo / "visuals" / f"{visual_id}.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" '
            f'data-cue-id="{cue_id}" data-scene-id="{scene}" '
            f'data-approved-text="{text}"><rect width="1920" height="1080"/></svg>\n',
            encoding="utf-8",
        )

    assert frame == 4415
    source_project = repo / "inputs" / "source.local.ymmp"
    _write_json(
        source_project,
        {
            "SelectedTimelineIndex": 0,
            "ToolStates": {"synthetic": True},
            "LayoutXml": "<synthetic/>",
            "Timelines": [
                {
                    "Name": "main",
                    "VideoInfo": {"FPS": 60, "Width": 1920, "Height": 1080, "Hz": 48000},
                    "Items": voices,
                    "Length": 4415,
                    "MaxLayer": 1,
                }
            ],
        },
    )

    locked = repo / "inputs" / "locked.json"
    locked.write_text('{"locked":true}\n', encoding="utf-8")
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "episode_id": "synthetic_episode",
        "source_package": "inputs/source-package.json",
        "approved_script": "inputs/approval.json",
        "derived_csv": "inputs/derived.csv",
        "cue_mapping": cue_mapping,
        "visual_source_path": "visuals",
        "yymm4": {
            "source_project_path": "inputs/source.local.ymmp",
            "source_project_sha256": _sha(source_project),
            "fps": 60,
            "timeline_frames": 4415,
        },
        "output": {
            "run_root_path": "runs",
            "run_id": "synthetic-v1",
            "project_filename": "generated.local.ymmp",
            "mp4_filename": "review.mp4",
        },
        "render_settings": {
            "fps": 60,
            "video_bitrate_kbps": 10000,
            "video_maxrate_kbps": 12000,
            "video_bufsize_kbps": 20000,
            "audio_bitrate_kbps": 192,
            "timeout_seconds": 1200,
        },
        "boundaries": {
            "internal_review_only": True,
            "rights_approved": False,
            "production": False,
            "publication": False,
            "external_upload": False,
        },
        "content_locks": [{"path": "inputs/locked.json", "sha256": _sha(locked)}],
    }
    manifest_path = repo / "episode.json"
    _write_json(manifest_path, manifest)
    return repo, manifest_path


def _real_media_episode(tmp_path: Path) -> tuple[Path, Path]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    repo, manifest_path = _synthetic_episode(tmp_path)
    media = repo / "media"
    media.mkdir()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sources = []
    assets = []
    for index, cue in enumerate(manifest["cue_mapping"], start=1):
        source_id = f"official-source-{index:03d}"
        asset_id = f"real-media-{index:03d}"
        asset = media / f"{asset_id}.png"
        asset.write_bytes(f"real-media-{index}".encode())
        cue.update(
            {
                "visual_id": asset_id,
                "asset_type": "image",
                "local_asset_path": f"media/{asset.name}",
                "source_provenance_id": source_id,
                "fit_mode": "contain",
                "internal_review_only": True,
                "subtitle_lines": [f"approved line {index}"],
                "speaker_label": (
                    "れいむ" if cue["speaker"] == "ゆっくり霊夢" else "まりさ"
                ),
            }
        )
        sources.append(
            {
                "source_id": source_id,
                "exact_title": f"Official source {index}",
                "publisher": "Synthetic official publisher",
                "canonical_url": f"https://example.invalid/source/{index}",
            }
        )
        assets.append(
            {
                "asset_id": asset_id,
                "source_id": source_id,
                "local_asset_path": f"media/{asset.name}",
                "sha256": _sha(asset),
                "media_type": "image",
                "crop_or_segment": "full frame",
                "cue_ids": [cue["cue_id"]],
                "usage_classification": "official_reuse_candidate",
                "rights_state": "unresolved; internal review only",
                "production_allowed": False,
                "publication_allowed": False,
            }
        )
    provenance = repo / "inputs" / "real-media-provenance.json"
    _write_json(
        provenance,
        {
            "schema": "nlmytgen.real_media_provenance.v1",
            "sources": sources,
            "assets": assets,
        },
    )
    manifest["provenance_manifest_path"] = "inputs/real-media-provenance.json"
    _write_json(manifest_path, manifest)
    return repo, manifest_path


def _install_fake_runtime(monkeypatch: pytest.MonkeyPatch) -> dict[str, int]:
    calls = {"render": 0}

    def fake_materialize(
        timings: list[episode_video.CueTiming],
        paths: episode_video.PipelinePaths,
        *,
        resume: bool,
        repo_root: Path,
    ) -> tuple[dict[str, Path], dict[str, object]]:
        outputs: dict[str, Path] = {}
        records = []
        paths.generated_assets.mkdir(parents=True, exist_ok=True)
        for timing in timings:
            output = paths.generated_assets / f"{timing.asset_id}.png"
            if not output.exists():
                output.write_bytes(f"visual:{timing.asset_id}".encode())
            outputs[timing.asset_id] = output
            records.append(
                {
                    "asset_id": timing.asset_id,
                    "asset_type": timing.asset_type,
                    "source_path": episode_video._repo_relative(repo_root, timing.visual_source),
                    "source_sha256": _sha(timing.visual_source),
                    "png_sha256": _sha(output),
                    "fit_mode": timing.fit_mode,
                    "crop": list(timing.crop) if timing.crop else None,
                    "source_provenance_id": timing.source_provenance_id,
                    "materialization_process": {
                        "status": "passed",
                        "engine": "fixture",
                        "cleanup_verified": True,
                    },
                }
            )
        receipt: dict[str, object] = {
            "status": "passed",
            "unique_visual_count": len(outputs),
            "records": records,
        }
        content = episode_video.canonical_json_bytes(receipt)
        if paths.real_media_asset_manifest.exists() and resume:
            assert paths.real_media_asset_manifest.read_bytes() == content
        else:
            paths.real_media_asset_manifest.write_bytes(content)
        return outputs, receipt

    def fake_cue_readback(
        timings: list[episode_video.CueTiming],
        _visuals: dict[str, Path],
        _paths: episode_video.PipelinePaths,
    ) -> dict[str, object]:
        return {
            "schema": episode_video.VISUAL_READBACK_SCHEMA,
            "status": "passed",
            "records": [
                {
                    "cue_id": timing.cue_id,
                    "path": f"<run-dir>/generated_assets/{timing.asset_id}.png",
                    "sha256": hashlib.sha256(timing.asset_id.encode()).hexdigest(),
                }
                for timing in timings
            ],
        }

    def fake_render(
        _repo_root: Path,
        _manifest: dict[str, object],
        paths: episode_video.PipelinePaths,
        *,
        resume: bool,
    ) -> dict[str, object]:
        if paths.yymm4_render.exists() and resume:
            return {
                "status": "reused",
                "render_sha256": _sha(paths.yymm4_render),
                "project_owned_process_cleanup": True,
                "yymm4_launched": False,
                "timings": {"automation_total_seconds": 0.0, "cleanup_seconds": 0.0},
            }
        calls["render"] += 1
        paths.yymm4_render.write_bytes(b"fixture-render")
        return {
            "status": "passed",
            "render_sha256": _sha(paths.yymm4_render),
            "project_owned_process_cleanup": True,
            "yymm4_launched": True,
            "timings": {"automation_total_seconds": 0.01, "cleanup_seconds": 0.001},
        }

    def fake_normalize(
        source: Path,
        output: Path,
        _settings: dict[str, object],
        *,
        resume: bool,
    ) -> dict[str, object]:
        if output.exists() and resume:
            return {"status": "reused", "sha256": _sha(output)}
        output.write_bytes(source.read_bytes())
        return {"status": "passed", "output_sha256": _sha(output)}

    def fake_validate(
        mp4: Path,
        timings: list[episode_video.CueTiming],
        paths: episode_video.PipelinePaths,
        _settings: dict[str, object],
        project_hash: str,
    ) -> dict[str, object]:
        result: dict[str, object] = {
            "schema": episode_video.MEDIA_VALIDATION_SCHEMA,
            "status": "passed",
            "cue_count": len(timings),
            "project_sha256": project_hash,
            "mp4_sha256": _sha(mp4),
        }
        paths.media_validation.write_bytes(episode_video.canonical_json_bytes(result))
        return result

    monkeypatch.setattr(episode_video, "materialize_visuals", fake_materialize)
    monkeypatch.setattr(episode_video, "build_cue_visual_readback", fake_cue_readback)
    monkeypatch.setattr(episode_video, "execute_yymm4_render", fake_render)
    monkeypatch.setattr(episode_video, "normalize_review_mp4", fake_normalize)
    monkeypatch.setattr(episode_video, "validate_media", fake_validate)
    return calls


def test_synthetic_preflight_and_project_readback_preserve_voice_items(tmp_path: Path) -> None:
    repo, manifest_path = _synthetic_episode(tmp_path)
    manifest = load_episode_manifest(repo, manifest_path)

    preflight, timings = preflight_episode(repo, manifest)

    assert preflight["status"] == "passed"
    assert preflight["cue_count"] == 9
    assert preflight["scene_counts"] == {"S1": 2, "S2": 4, "S3": 3}
    assert timings[-1].end_frame == 4415

    paths = build_pipeline_paths(repo, manifest)
    paths.generated_assets.mkdir(parents=True)
    visual_outputs = {}
    for timing in timings:
        image = paths.generated_assets / f"{timing.visual_id}.png"
        image.write_bytes(b"synthetic-png")
        visual_outputs[timing.visual_id] = image

    readback = build_yymm4_project(
        repo, manifest, timings, visual_outputs, paths, resume=False
    )
    generated_once = paths.generated_project.read_bytes()
    repeated = build_yymm4_project(
        repo, manifest, timings, visual_outputs, paths, resume=True
    )

    assert readback["status"] == repeated["status"] == "passed"
    assert readback["voice_items_unchanged"] is True
    assert paths.generated_project.read_bytes() == generated_once
    project = json.loads(generated_once)
    images = [
        item
        for item in project["Timelines"][0]["Items"]
        if item.get("$type") == IMAGE_ITEM_TYPE
    ]
    assert len(images) == 9
    assert [(item["Frame"], item["Length"]) for item in images] == [
        (timing.frame, timing.length_frames) for timing in timings
    ]
    assert all(item["VideoEffects"] == [] for item in images)
    assert all(item["KeyFrames"] == {"Frames": [], "Count": 0} for item in images)
    assert all(item["Zoom"]["AnimationType"] == "なし" for item in images)


def test_real_media_manifest_parses_images_and_video_with_provenance(tmp_path: Path) -> None:
    repo, manifest_path = _real_media_episode(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    video = repo / "media" / "real-media-009.mp4"
    (repo / "media" / "real-media-009.png").replace(video)
    manifest["cue_mapping"][-1].update(
        {
            "asset_type": "video",
            "local_asset_path": "media/real-media-009.mp4",
            "source_time_range": {"start_seconds": 1.0, "end_seconds": 2.0},
        }
    )
    provenance_path = repo / manifest["provenance_manifest_path"]
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance["assets"][-1].update(
        {
            "local_asset_path": "media/real-media-009.mp4",
            "sha256": _sha(video),
            "media_type": "video",
            "crop_or_segment": "1.0-2.0 seconds",
        }
    )
    _write_json(provenance_path, provenance)
    _write_json(manifest_path, manifest)

    loaded = load_episode_manifest(repo, manifest_path)
    preflight, timings = preflight_episode(repo, loaded)

    assert preflight["real_media"]["cue_provenance_coverage"] == "9/9"
    assert preflight["real_media"]["svg_reference_count"] == 0
    assert timings[-1].asset_type == "video"
    assert timings[-1].source_start_seconds == 1.0
    assert timings[-1].source_end_seconds == 2.0
    assert all(timing.internal_review_only for timing in timings)


def test_real_media_manifest_rejects_missing_provenance_svg_and_open_rights(
    tmp_path: Path,
) -> None:
    repo, manifest_path = _real_media_episode(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    del manifest["cue_mapping"][0]["source_provenance_id"]
    _write_json(manifest_path, manifest)
    with pytest.raises(EpisodeVideoError) as missing:
        load_episode_manifest(repo, manifest_path)
    assert missing.value.code == "real_media_provenance_missing"

    repo, manifest_path = _real_media_episode(tmp_path / "svg")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["cue_mapping"][0]["local_asset_path"] = "media/forbidden.svg"
    _write_json(manifest_path, manifest)
    with pytest.raises(EpisodeVideoError) as svg:
        load_episode_manifest(repo, manifest_path)
    assert svg.value.code == "real_media_svg_forbidden"

    repo, manifest_path = _real_media_episode(tmp_path / "rights")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    provenance_path = repo / manifest["provenance_manifest_path"]
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance["assets"][0]["production_allowed"] = True
    _write_json(provenance_path, provenance)
    loaded = load_episode_manifest(repo, manifest_path)
    with pytest.raises(EpisodeVideoError) as rights:
        preflight_episode(repo, loaded)
    assert rights.value.code == "real_media_provenance_records_invalid"


def test_real_media_project_preserves_voice_timing_line_breaks_and_uses_run_pngs(
    tmp_path: Path,
) -> None:
    repo, manifest_path = _real_media_episode(tmp_path)
    project_path = repo / "inputs" / "source.local.ymmp"
    project = json.loads(project_path.read_text(encoding="utf-8"))
    project["Timelines"][0]["Items"][0]["Serif"] = "approved line 1\nlocked fragment"
    _write_json(project_path, project)
    with (repo / "inputs" / "derived.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(
            zip(
                SPEAKERS,
                ["approved line 1\nlocked fragment"]
                + [f"approved line {index}" for index in range(2, 10)],
                strict=True,
            )
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["yymm4"]["source_project_sha256"] = _sha(project_path)
    manifest["cue_mapping"][0]["subtitle_lines"] = [
        "approved line 1",
        "\nlocked fragment",
    ]
    _write_json(manifest_path, manifest)
    loaded = load_episode_manifest(repo, manifest_path)
    _, timings = preflight_episode(repo, loaded)
    paths = build_pipeline_paths(repo, loaded)
    paths.generated_assets.mkdir(parents=True)
    visual_outputs = {}
    for timing in timings:
        output = paths.generated_assets / f"{timing.asset_id}.png"
        output.write_bytes(b"normalized")
        visual_outputs[timing.asset_id] = output

    readback = build_yymm4_project(
        repo, loaded, timings, visual_outputs, paths, resume=False
    )
    generated = json.loads(paths.generated_project.read_text(encoding="utf-8"))
    voices = [
        item
        for item in generated["Timelines"][0]["Items"]
        if item.get("$type") == VOICE_ITEM_TYPE
    ]
    images = [
        item
        for item in generated["Timelines"][0]["Items"]
        if item.get("$type") == IMAGE_ITEM_TYPE
    ]

    assert readback["voice_items_unchanged"] is True
    assert voices[0]["Serif"] == "approved line 1\nlocked fragment"
    assert [(row["Frame"], row["Length"]) for row in voices] == [
        (timing.frame, timing.length_frames) for timing in timings
    ]
    assert len(images) == 9
    assert all(Path(row["FilePath"]).parent == paths.generated_assets.resolve() for row in images)
    assert all(Path(row["FilePath"]).suffix.lower() == ".png" for row in images)
    assert all(row["Remark"].startswith("internal-review-real-media:") for row in images)
    assert ".svg" not in paths.generated_project.read_text(encoding="utf-8").lower()

    with (repo / "inputs" / "derived.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(
            zip(
                SPEAKERS,
                ["approved line 1 locked fragment"]
                + [f"approved line {index}" for index in range(2, 10)],
                strict=True,
            )
        )
    with pytest.raises(EpisodeVideoError) as line_break:
        preflight_episode(repo, loaded)
    assert line_break.value.code == "voice_text_drift"


def test_preflight_rejects_visual_with_wrong_approved_text(tmp_path: Path) -> None:
    repo, manifest_path = _synthetic_episode(tmp_path)
    visual = repo / "visuals" / "visual_004.svg"
    visual.write_text(visual.read_text(encoding="utf-8").replace("approved line 4", "wrong"), encoding="utf-8")
    manifest = load_episode_manifest(repo, manifest_path)

    with pytest.raises(EpisodeVideoError) as caught:
        preflight_episode(repo, manifest)

    assert caught.value.code == "visual_cue_binding_drift"


def test_preflight_rejects_protected_input_hash_drift(tmp_path: Path) -> None:
    repo, manifest_path = _synthetic_episode(tmp_path)
    (repo / "inputs" / "locked.json").write_text('{"locked":false}\n', encoding="utf-8")
    manifest = load_episode_manifest(repo, manifest_path)

    with pytest.raises(EpisodeVideoError) as caught:
        preflight_episode(repo, manifest)

    assert caught.value.code == "protected_input_hash_mismatch"


def test_manifest_rejects_absolute_private_path(tmp_path: Path) -> None:
    repo, manifest_path = _synthetic_episode(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source_package"] = r"C:\private\source-package.json"
    _write_json(manifest_path, manifest)

    with pytest.raises(EpisodeVideoError) as caught:
        load_episode_manifest(repo, manifest_path)

    assert caught.value.code == "manifest_absolute_path_forbidden"


def test_dry_run_is_write_free_and_existing_run_is_protected(tmp_path: Path) -> None:
    repo, manifest_path = _synthetic_episode(tmp_path)
    manifest = load_episode_manifest(repo, manifest_path)
    paths = build_pipeline_paths(repo, manifest)

    plan = run_episode_video(
        repo_root=repo,
        manifest_path=manifest_path,
        render=False,
        dry_run=True,
        resume=False,
        force=False,
    )

    assert plan["status"] == "dry_run"
    assert plan["preflight"]["status"] == "passed"
    assert not paths.run_directory.exists()

    paths.run_directory.mkdir(parents=True)
    with pytest.raises(EpisodeVideoError) as caught:
        run_episode_video(
            repo_root=repo,
            manifest_path=manifest_path,
            render=False,
            dry_run=False,
            resume=False,
            force=False,
        )
    assert caught.value.code == "run_overwrite_refused"


def test_run_id_override_is_safe_bounded_and_content_neutral(tmp_path: Path) -> None:
    repo, manifest_path = _real_media_episode(tmp_path)
    manifest = load_episode_manifest(repo, manifest_path)
    _, timings = preflight_episode(repo, manifest)
    default_identity = build_content_identity(repo, manifest, timings)

    overridden = json.loads(json.dumps(manifest))
    overridden["output"]["run_id"] = validate_run_id("repeatability-01")
    _, overridden_timings = preflight_episode(repo, overridden)
    overridden_identity = build_content_identity(repo, overridden, overridden_timings)

    assert default_identity["sha256"] == overridden_identity["sha256"]
    assert "output.run_id" in default_identity["excluded_volatile_fields"]
    for value in ("", "..", "../escape", r"C:\escape", r"\\server\share", "CON", "LPT1.txt"):
        with pytest.raises(EpisodeVideoError) as caught:
            validate_run_id(value)
        assert caught.value.code == "run_id_invalid"

    plan = run_episode_video(
        repo_root=repo,
        manifest_path=manifest_path,
        render=False,
        dry_run=True,
        resume=False,
        force=False,
        run_id_override="repeatability-01",
    )
    assert plan["run_id"] == "repeatability-01"
    assert plan["content_identity_sha256"] == default_identity["sha256"]
    assert plan["render_timeout_contract"] == {
        "schema": "nlmytgen.render_timeout_contract.v1",
        "authority": "manifest.render_settings.timeout_seconds",
        "render_timeout_seconds": 1200,
        "cleanup_grace_seconds": 60,
        "pipeline_timeout_seconds": 1260,
        "observer_grace_seconds": 30,
        "observer_timeout_seconds": 1290,
    }
    assert not (repo / "runs" / "repeatability-01").exists()


def test_completed_resume_is_noop_and_semantic_drift_stays_fail_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, manifest_path = _real_media_episode(tmp_path)
    calls = _install_fake_runtime(monkeypatch)
    run_id = "repeatability-03"
    first = run_episode_video(
        repo_root=repo,
        manifest_path=manifest_path,
        render=True,
        dry_run=False,
        resume=False,
        force=False,
        run_id_override=run_id,
    )
    run_dir = repo / "runs" / run_id
    before = {
        path.relative_to(run_dir).as_posix(): (_sha(path), path.stat().st_mtime_ns)
        for path in run_dir.rglob("*")
        if path.is_file()
    }

    resumed = run_episode_video(
        repo_root=repo,
        manifest_path=manifest_path,
        render=True,
        dry_run=False,
        resume=True,
        force=False,
        run_id_override=run_id,
    )
    after = {
        path.relative_to(run_dir).as_posix(): (_sha(path), path.stat().st_mtime_ns)
        for path in run_dir.rglob("*")
        if path.is_file()
    }

    assert first["status"] == resumed["status"] == "passed"
    assert resumed["resume_observation"]["status"] == "verified_noop"
    assert resumed["resume_observation"]["outputs_rewritten"] is False
    assert resumed["resume_observation"]["yymm4_launched"] is False
    assert calls["render"] == 1
    assert after == before

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["render_settings"]["video_bitrate_kbps"] += 1
    _write_json(manifest_path, manifest)
    with pytest.raises(EpisodeVideoError) as drift:
        run_episode_video(
            repo_root=repo,
            manifest_path=manifest_path,
            render=True,
            dry_run=False,
            resume=True,
            force=False,
            run_id_override=run_id,
        )
    assert drift.value.code == "resume_artifact_drift"


def test_incomplete_render_stage_can_resume_and_corrupt_completed_output_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, manifest_path = _real_media_episode(tmp_path)
    calls = _install_fake_runtime(monkeypatch)
    run_id = "repeatability-incomplete"
    incomplete = run_episode_video(
        repo_root=repo,
        manifest_path=manifest_path,
        render=False,
        dry_run=False,
        resume=False,
        force=False,
        run_id_override=run_id,
    )
    completed = run_episode_video(
        repo_root=repo,
        manifest_path=manifest_path,
        render=True,
        dry_run=False,
        resume=True,
        force=False,
        run_id_override=run_id,
    )

    assert incomplete["render_requested"] is False
    assert completed["render_requested"] is True
    assert completed["status"] == "passed"
    assert calls["render"] == 1

    mp4 = repo / "runs" / run_id / "review.mp4"
    mp4.write_bytes(b"corrupt")
    with pytest.raises(EpisodeVideoError) as corrupt:
        run_episode_video(
            repo_root=repo,
            manifest_path=manifest_path,
            render=True,
            dry_run=False,
            resume=True,
            force=False,
            run_id_override=run_id,
        )
    assert corrupt.value.code == "resume_artifact_drift"


def test_normalized_project_identity_ignores_only_run_local_paths(tmp_path: Path) -> None:
    repo, manifest_path = _real_media_episode(tmp_path)
    manifest = load_episode_manifest(repo, manifest_path)
    _, timings = preflight_episode(repo, manifest)
    identities = []
    raw_hashes = []
    for run_id in ("repeatability-a", "repeatability-b"):
        candidate = json.loads(json.dumps(manifest))
        candidate["output"]["run_id"] = run_id
        paths = build_pipeline_paths(repo, candidate)
        paths.generated_assets.mkdir(parents=True)
        visuals = {}
        for timing in timings:
            output = paths.generated_assets / f"{timing.asset_id}.png"
            output.write_bytes(timing.asset_id.encode())
            visuals[timing.asset_id] = output
        readback = build_yymm4_project(
            repo,
            candidate,
            timings,
            visuals,
            paths,
            resume=False,
        )
        raw_hashes.append(readback["generated_project_sha256"])
        identities.append(
            readback["normalized_project_structural_identity"]["sha256"]
        )

    assert len(set(raw_hashes)) == 2
    assert len(set(identities)) == 1


def test_tracked_manifest_keeps_required_base_mapping_and_receipt_is_sanitized() -> None:
    manifest_path = PILOT_PIPELINE / "new_banknote_episode_manifest.json"
    receipt_path = PILOT_PIPELINE / "validated_run_receipt.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = [
        "reconstructed_S1_overview",
        "reconstructed_S1_overview",
        "reconstructed_cue_003_watermark",
        "reconstructed_cue_004_hologram",
        "reconstructed_cue_005_intaglio",
        "reconstructed_cue_006_microtext",
        "reconstructed_S3_summary",
        "reconstructed_S3_summary",
        "reconstructed_S3_summary",
    ]

    assert [row["visual_id"] for row in manifest["cue_mapping"]] == expected
    assert [
        row.get("materialized_visual_id") for row in manifest["cue_mapping"]
    ] == [
        None,
        "proxy_cue_002_overview",
        None,
        None,
        None,
        None,
        "proxy_cue_007_identification",
        "proxy_cue_008_denomination",
        None,
    ]
    tracked_text = manifest_path.read_text(encoding="utf-8") + receipt_path.read_text(
        encoding="utf-8"
    )
    assert "C:\\Users\\" not in tracked_text
    assert "D:\\" not in tracked_text
    assert "http://" not in tracked_text and "https://" not in tracked_text


def test_tracked_real_media_contract_and_validated_receipt_are_sanitized() -> None:
    manifest_path = PILOT_PIPELINE / "new_banknote_real_media_episode_manifest.json"
    provenance_path = PILOT_PIPELINE / "new_banknote_real_media_provenance.json"
    receipt_path = PILOT_PIPELINE / "validated_real_media_run_receipt.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    source_ids = {row["source_id"] for row in provenance["sources"]}

    assert len(manifest["cue_mapping"]) == 9
    assert all(row["asset_type"] in {"image", "video"} for row in manifest["cue_mapping"])
    assert all(row["source_provenance_id"] in source_ids for row in manifest["cue_mapping"])
    assert all(row["internal_review_only"] is True for row in manifest["cue_mapping"])
    assert all(1 <= len(row["subtitle_lines"]) <= 3 for row in manifest["cue_mapping"])
    assert ".svg" not in manifest_path.read_text(encoding="utf-8").lower()
    assert receipt["status"] == "passed"
    assert receipt["protected_identity"]["voice_items_unchanged"] is True
    assert receipt["protected_identity"]["subtitle_line_fragments_unchanged"] is True
    assert receipt["real_media"]["cue_coverage"] == "9/9"
    assert receipt["real_media"]["svg_reference_count_manifest"] == 0
    assert receipt["cue_frame_inspection"]["cue_count"] == 9
    assert receipt["silent_execution"]["speaker_playback_used"] is False
    assert receipt["silent_execution"]["preview_playback_used"] is False
    tracked_receipt = receipt_path.read_text(encoding="utf-8")
    assert "C:\\Users\\" not in tracked_receipt
    assert "D:\\" not in tracked_receipt
    assert "http://" not in tracked_receipt and "https://" not in tracked_receipt


def test_render_driver_command_is_bounded_and_carries_requested_rates(tmp_path: Path) -> None:
    command = build_render_driver_command(
        tmp_path,
        tmp_path / "YukkuriMovieMaker.exe",
        tmp_path / "generated.local.ymmp",
        tmp_path / "render.local.mp4",
        {"video_bitrate_kbps": 10000, "audio_bitrate_kbps": 192, "timeout_seconds": 321},
    )

    assert command[:2] == ["dotnet", "run"]
    assert command[-6:] == [
        "--video-bitrate-kbps",
        "10000",
        "--audio-bitrate-kbps",
        "192",
        "--timeout-seconds",
        "321",
    ]
    assert command[command.index("--output") + 1].endswith("render.local.mp4")


def test_render_timeout_closes_owned_process_job(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = {
        "output": {
            "run_root_path": "runs",
            "run_id": "timeout_case",
            "project_filename": "generated.local.ymmp",
            "mp4_filename": "review.mp4",
        },
        "render_settings": {
            "video_bitrate_kbps": 10000,
            "audio_bitrate_kbps": 192,
            "timeout_seconds": 1,
        },
    }
    paths = build_pipeline_paths(tmp_path, manifest)
    paths.run_directory.mkdir(parents=True)
    paths.generated_project.write_text("{}\n", encoding="utf-8")
    executable = tmp_path / "YukkuriMovieMaker.exe"
    executable.write_bytes(b"test")
    closed: list[bool] = []

    class FakeProcess:
        pid = 12345
        returncode: int | None = None

        def communicate(self, timeout: int | None = None) -> tuple[str, str]:
            if timeout == 61:
                raise subprocess.TimeoutExpired(cmd="dotnet", timeout=timeout)
            self.returncode = -9
            return "", ""

        def poll(self) -> int | None:
            return self.returncode

        def kill(self) -> None:
            self.returncode = -9

    class FakeJob:
        def __init__(self, process: FakeProcess) -> None:
            self.process = process

        def close(self) -> None:
            closed.append(True)
            self.process.returncode = -9

    monkeypatch.setattr(episode_video, "resolve_yymm4_executable", lambda: executable)
    monkeypatch.setattr(episode_video.subprocess, "Popen", lambda *_, **__: FakeProcess())
    monkeypatch.setattr(episode_video, "OwnedProcessJob", FakeJob)
    monkeypatch.setattr(episode_video, "process_snapshot", lambda: {})
    monkeypatch.setattr(episode_video.time, "sleep", lambda _: None)

    with pytest.raises(EpisodeVideoError) as exc_info:
        episode_video.execute_yymm4_render(
            tmp_path,
            manifest,
            paths,
            resume=False,
        )

    assert exc_info.value.code == "yymm4_render_timeout"
    assert exc_info.value.details["cleanup_verified"] is True
    assert exc_info.value.details["residual_count"] == 0
    assert closed


def test_render_failure_persists_sanitized_stage_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, manifest_path = _real_media_episode(tmp_path)
    _install_fake_runtime(monkeypatch)

    def fail_render(*_args: object, **_kwargs: object) -> dict[str, object]:
        raise EpisodeVideoError(
            r"render failed at C:\Users\private-owner\project",
            code="yymm4_render_timeout",
            details={
                "failed_stage": "yymm4_render",
                "driver_stage": "wait_render_file",
                "job_object_assigned": True,
                "cleanup_verified": True,
                "residual_count": 0,
                "cleanup_seconds": 0.02,
            },
        )

    monkeypatch.setattr(episode_video, "execute_yymm4_render", fail_render)
    with pytest.raises(EpisodeVideoError) as caught:
        run_episode_video(
            repo_root=repo,
            manifest_path=manifest_path,
            render=True,
            dry_run=False,
            resume=False,
            force=False,
            run_id_override="timeout-receipt",
        )

    receipt_path = repo / "runs" / "timeout-receipt" / "pipeline_failure_receipt.json"
    receipt_text = receipt_path.read_text(encoding="utf-8")
    receipt = json.loads(receipt_text)
    assert caught.value.details["failure_receipt"] == receipt_path.name
    assert receipt["status"] == "failed"
    assert receipt["failed_stage"] == "yymm4_render"
    assert receipt["failure_details"]["driver_stage"] == "wait_render_file"
    assert receipt["failure_details"]["cleanup_verified"] is True
    assert receipt["failure_details"]["residual_count"] == 0
    assert "private-owner" not in receipt_text
    assert "C:\\Users" not in receipt_text


@pytest.mark.skipif(os.name != "nt", reason="Windows Job Object containment proof")
def test_job_object_timeout_kills_real_child_grandchild_and_preserves_unrelated(
    tmp_path: Path,
) -> None:
    helper = tmp_path / "owned_tree_helper.py"
    helper.write_text(
        "\n".join(
            [
                "import os",
                "from pathlib import Path",
                "import subprocess",
                "import sys",
                "import time",
                "mode = sys.argv[1]",
                "root = Path(sys.argv[2])",
                "(root / f'{mode}.pid').write_text(str(os.getpid()), encoding='ascii')",
                "if mode == 'root':",
                "    while not (root / 'go').exists():",
                "        time.sleep(0.02)",
                "    subprocess.Popen([sys.executable, __file__, 'child', str(root)])",
                "elif mode == 'child':",
                "    subprocess.Popen([sys.executable, __file__, 'grandchild', str(root)])",
                "time.sleep(30)",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    unrelated = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    root = subprocess.Popen(
        [sys.executable, str(helper), "root", str(tmp_path)],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    job = episode_video.OwnedProcessJob(root)
    try:
        (tmp_path / "go").write_text("go\n", encoding="ascii")
        deadline = time.monotonic() + 5
        pid_paths = [
            tmp_path / "root.pid",
            tmp_path / "child.pid",
            tmp_path / "grandchild.pid",
        ]
        while not all(path.exists() for path in pid_paths) and time.monotonic() < deadline:
            time.sleep(0.02)
        assert all(path.exists() for path in pid_paths)
        owned_pids = {int(path.read_text(encoding="ascii")) for path in pid_paths}

        with pytest.raises(subprocess.TimeoutExpired):
            root.communicate(timeout=0.1)
        job.close()
        root.wait(timeout=5)

        deadline = time.monotonic() + 5
        residual = owned_pids
        while residual and time.monotonic() < deadline:
            snapshot = episode_video.process_snapshot()
            residual = {pid for pid in owned_pids if pid in snapshot}
            if residual:
                time.sleep(0.05)
        assert residual == set()
        assert unrelated.poll() is None
    finally:
        job.close()
        if root.poll() is None:
            root.kill()
            root.wait(timeout=5)
        if unrelated.poll() is None:
            unrelated.kill()
            unrelated.wait(timeout=5)


def test_review_normalization_is_lossless_faststart_remux(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source.mp4"
    output = tmp_path / "review.mp4"
    source.write_bytes(b"synthetic-media")
    captured: list[str] = []

    def fake_run(command: list[str], **_: object) -> subprocess.CompletedProcess[bytes]:
        captured.extend(command)
        Path(command[-1]).write_bytes(source.read_bytes())
        return subprocess.CompletedProcess(command, 0, b"", b"")

    monkeypatch.setattr(episode_video.shutil, "which", lambda _: "ffmpeg")
    monkeypatch.setattr(episode_video, "assert_command_allowed", lambda *_, **__: None)
    monkeypatch.setattr(episode_video.subprocess, "run", fake_run)

    result = normalize_review_mp4(
        source,
        output,
        {
            "video_bitrate_kbps": 10000,
            "video_maxrate_kbps": 12000,
            "video_bufsize_kbps": 20000,
            "audio_bitrate_kbps": 192,
        },
        resume=False,
    )

    assert result["status"] == "passed"
    assert result["mode"] == "lossless_stream_remux"
    assert captured[captured.index("-c") + 1] == "copy"
    assert captured[captured.index("-movflags") + 1] == "+faststart"
    assert "libx264" not in captured
    assert output.read_bytes() == source.read_bytes()


def test_distinct_crops_reusing_one_asset_materialize_per_cue(
    tmp_path: Path, monkeypatch
) -> None:
    source = tmp_path / "source.png"
    source.write_bytes(b"source")
    run = tmp_path / "run"
    paths = episode_video.PipelinePaths(
        run_directory=run,
        generated_assets=run / "generated_assets",
        generated_project=run / "generated_project.local.ymmp",
        yymm4_render=run / "render.local.mp4",
        review_mp4=run / "review.mp4",
        extracted_frames=run / "frames",
        resolved_manifest=run / "resolved_manifest.json",
        real_media_asset_manifest=run / "real_media_asset_manifest.local.json",
        run_receipt=run / "pipeline_run_receipt.json",
        media_validation=run / "media_validation.json",
        cue_visual_readback=run / "cue_visual_readback.json",
        run_log=run / "run.log",
    )
    timings = [
        episode_video.CueTiming(
            cue_id=f"cue_{index:03d}",
            scene_id="S1",
            speaker="reimu",
            text=f"text-{index}",
            frame=(index - 1) * 60,
            length_frames=60,
            end_frame=index * 60,
            visual_id="shared",
            asset_id="shared",
            visual_source=source,
            asset_type="image",
            source_provenance_id="source",
            fit_mode="cover",
            crop=crop,
            internal_review_only=True,
            subtitle_lines=(f"subtitle-{index}",),
        )
        for index, crop in enumerate(
            ((0.0, 0.0, 0.5, 0.5), (0.5, 0.5, 0.5, 0.5)),
            start=1,
        )
    ]

    def materialize(timing, output):
        output.write_bytes(timing.cue_id.encode("utf-8"))
        return {
            "status": "passed",
            "cleanup_verified": True,
            "speaker_playback": False,
            "preview_playback": False,
        }

    monkeypatch.setattr(episode_video, "_materialize_real_media_frame", materialize)
    monkeypatch.setattr(episode_video, "png_dimensions", lambda path: (1920, 1080))
    outputs, receipt = episode_video.materialize_visuals(
        timings,
        paths,
        resume=False,
        repo_root=tmp_path,
    )
    assert outputs["cue_001"] != outputs["cue_002"]
    assert outputs["cue_001"].name == "shared__cue_001.png"
    assert outputs["cue_002"].name == "shared__cue_002.png"
    assert receipt["unique_visual_count"] == 2
    assert [row["crop"] for row in receipt["records"]] == [
        [0.0, 0.0, 0.5, 0.5],
        [0.5, 0.5, 0.5, 0.5],
    ]


def test_review_frame_extraction_uses_accurate_output_seek(
    tmp_path: Path, monkeypatch
) -> None:
    mp4 = tmp_path / "review.mp4"
    mp4.write_bytes(b"mp4")
    run = tmp_path / "run"
    paths = episode_video.PipelinePaths(
        run_directory=run,
        generated_assets=run / "generated_assets",
        generated_project=run / "generated_project.local.ymmp",
        yymm4_render=run / "render.local.mp4",
        review_mp4=mp4,
        extracted_frames=run / "frames",
        resolved_manifest=run / "resolved_manifest.json",
        real_media_asset_manifest=run / "real_media_asset_manifest.local.json",
        run_receipt=run / "pipeline_run_receipt.json",
        media_validation=run / "media_validation.json",
        cue_visual_readback=run / "cue_visual_readback.json",
        run_log=run / "run.log",
    )
    timing = episode_video.CueTiming(
        cue_id="cue_001",
        scene_id="S1",
        speaker="reimu",
        text="text",
        frame=60,
        length_frames=120,
        end_frame=180,
        visual_id="visual",
        asset_id="visual",
        visual_source=tmp_path / "source.png",
    )
    commands: list[list[str]] = []

    def run(command, **kwargs):
        commands.append(command)
        Path(command[-1]).write_bytes(str(command).encode("utf-8"))
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(episode_video.shutil, "which", lambda name: "ffmpeg")
    monkeypatch.setattr(episode_video.subprocess, "run", run)
    monkeypatch.setattr(episode_video, "png_dimensions", lambda path: (1920, 1080))
    receipt = episode_video.extract_review_frames(mp4, [timing], paths)
    assert receipt["cue_frame_count"] == 1
    assert commands
    assert all(command.index("-i") < command.index("-ss") for command in commands)
    cue = [row for row in receipt["records"] if row["label"] == "cue_001"][0]
    assert cue["seconds"] == 2.0
