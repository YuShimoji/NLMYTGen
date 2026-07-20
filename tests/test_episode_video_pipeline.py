from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from src.pipeline import episode_video
from src.pipeline.episode_video import (
    EpisodeVideoError,
    IMAGE_ITEM_TYPE,
    MANIFEST_SCHEMA,
    VOICE_ITEM_TYPE,
    build_pipeline_paths,
    build_render_driver_command,
    build_yymm4_project,
    load_episode_manifest,
    normalize_review_mp4,
    preflight_episode,
    run_episode_video,
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
