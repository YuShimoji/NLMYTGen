from __future__ import annotations

import json

import pytest

from src.cli.main import main
from src.pipeline.episode_run_pack import EPISODE_RUN_DIRS, init_episode_run_pack


def test_init_episode_run_pack_creates_expected_layout(tmp_path) -> None:
    result = init_episode_run_pack(episode_id="pilot_001", root=tmp_path)
    run_dir = tmp_path / "pilot_001"

    assert result["success"] is True
    for dirname in EPISODE_RUN_DIRS:
        assert (run_dir / dirname).is_dir()

    assert (run_dir / "README.md").is_file()
    assert (run_dir / "review" / "gaps.md").is_file()
    assert (run_dir / "review" / "ymm4_acceptance.md").is_file()
    assert (run_dir / "manifest" / "session_manifest.command.txt").is_file()

    manifest = json.loads(
        (run_dir / "manifest" / "episode_pack_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["episode_id"] == "pilot_001"
    assert manifest["standard_inputs"]["production_ir"] == [
        "face",
        "idle_face",
        "bg",
        "skit_group",
    ]
    assert manifest["motion_candidates"]["full_body_baseline"] == "nod_clear_v2"
    assert manifest["motion_candidates"]["head_only_candidate"] == "nod_head_v1"
    assert "GUI Validate IR" in manifest["gui_policy"]["primary_route"]
    assert manifest["expected_paths"]["csv"].endswith("pilot_001.csv")
    assert manifest["expected_paths"]["validate_result"].endswith("pilot_001_validate.json")
    assert manifest["expected_paths"]["dry_run_result"].endswith("pilot_001_dry_run.json")
    assert manifest["expected_paths"]["apply_result"].endswith("pilot_001_apply.json")
    assert manifest["expected_paths"]["patched_ymmp"].endswith("pilot_001_patched.ymmp")

    readme = (run_dir / "README.md").read_text(encoding="utf-8")
    assert "Episode Pack Root" in readme
    assert "assistant status" in readme
    assert "user action" in readme
    assert "assistant next" in readme
    assert "Validate IR" in readme
    assert "pilot_001_dry_run.json" in readme
    assert "pilot_001_patched.ymmp" in readme


def test_init_episode_run_pack_does_not_overwrite_without_force(tmp_path) -> None:
    run_dir = tmp_path / "pilot"
    gaps = run_dir / "review" / "gaps.md"
    gaps.parent.mkdir(parents=True)
    gaps.write_text("custom gaps\n", encoding="utf-8")

    result = init_episode_run_pack(episode_id="pilot", root=tmp_path)

    assert gaps.read_text(encoding="utf-8") == "custom gaps\n"
    assert str(gaps) in result["skipped_files"]


def test_init_episode_run_pack_force_overwrites_starter_files(tmp_path) -> None:
    run_dir = tmp_path / "pilot"
    gaps = run_dir / "review" / "gaps.md"
    gaps.parent.mkdir(parents=True)
    gaps.write_text("custom gaps\n", encoding="utf-8")

    result = init_episode_run_pack(episode_id="pilot", root=tmp_path, force=True)

    assert "custom gaps" not in gaps.read_text(encoding="utf-8")
    assert str(gaps) in result["created_files"]


def test_init_episode_run_pack_rejects_path_like_ids(tmp_path) -> None:
    with pytest.raises(ValueError, match="EPISODE_RUN_ID_INVALID"):
        init_episode_run_pack(episode_id="../escape", root=tmp_path)


def test_cli_init_episode_run_json_stdout(tmp_path, capsys) -> None:
    code = main([
        "init-episode-run",
        "--episode-id",
        "pilot_cli",
        "--root",
        str(tmp_path),
        "--format",
        "json",
    ])

    assert code == 0
    result = json.loads(capsys.readouterr().out)
    assert result["episode_id"] == "pilot_cli"
    assert (tmp_path / "pilot_cli" / "manifest" / "episode_pack_manifest.json").is_file()
