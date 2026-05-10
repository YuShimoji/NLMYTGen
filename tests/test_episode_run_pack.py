from __future__ import annotations

import json

import pytest

from src.cli.main import main
from src.pipeline.episode_run_pack import (
    EPISODE_RUN_DIRS,
    build_episode_run_handoff,
    init_episode_run_pack,
)


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
    assert manifest["standard_inputs"]["required_files"] == [
        "csv/<episode_id>.txt",
        "ir/<episode_id>_production_ir.json",
    ]
    assert manifest["standard_inputs"]["generated_later_files"] == [
        "ymmp/<episode_id>_base.ymmp",
    ]
    contracts = manifest["standard_inputs"]["required_file_contracts"]
    assert contracts[0]["id"] == "source_script"
    assert contracts[1]["id"] == "production_ir"
    assert contracts[2]["id"] == "base_ymmp"
    assert "new_script_policy" in contracts[0]
    assert "why_required" in contracts[0]
    assert "accepted_format" in contracts[0]
    assert "same_episode_binding" in contracts[0]
    assert "Build CSV" in contracts[2]["creation_route"]
    assert "maps/bg_map.json" in manifest["standard_inputs"]["conditional_files"]
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
    assert "Current blocker" in readme
    assert "Required operator action" in readme
    assert "After a return" in readme
    assert "assistant status" not in readme
    assert "user action" not in readme
    assert "assistant next" not in readme
    assert "episode-run-handoff" in readme
    assert "Initial input packet" in readme
    assert "csv/pilot_001.txt" in readme
    assert "ir/pilot_001_production_ir.json" in readme
    assert "ymmp/pilot_001_base.ymmp" in readme
    assert "Validate IR" in readme
    assert "pilot_001_dry_run.json" in readme
    assert "pilot_001_patched.ymmp" in readme


def test_episode_run_handoff_explains_missing_required_inputs(tmp_path) -> None:
    init_episode_run_pack(episode_id="pilot_handoff", root=tmp_path)

    handoff = build_episode_run_handoff(episode_id="pilot_handoff", root=tmp_path)

    assert handoff["phase"] == "initial_inputs"
    assert handoff["assistant_status"] == "blocked_on_initial_user_inputs"
    assert handoff["missing_required"] == [
        "source_script",
        "production_ir",
    ]
    assert handoff["pending_generated"] == ["base_ymmp"]
    inputs = {item["id"]: item for item in handoff["required_inputs"]}
    assert inputs["source_script"]["state"] == "missing"
    assert inputs["source_script"]["path"].endswith("pilot_handoff.txt")
    assert "Completed dialogue script" in inputs["source_script"]["what_it_is"]
    assert "既存完成台本があれば新規作成不要" in inputs["source_script"]["new_script_policy"]
    assert "row-range" in inputs["source_script"]["why_required"]
    assert "UTF-8 .txt" in inputs["source_script"]["accepted_format"]
    assert "another episode" in inputs["source_script"]["same_episode_binding"]
    assert "S-6" in inputs["production_ir"]["how_to_create"]
    assert inputs["base_ymmp"]["state"] == "generated_later"
    assert inputs["base_ymmp"]["required_phase"] == "after_build_csv"
    assert "Build CSV後に生成" in inputs["base_ymmp"]["how_to_create"]
    assert "YMM4" in inputs["base_ymmp"]["how_to_create"]
    assert "hand-edit" in handoff["do_not"][3]


def test_episode_run_handoff_phase_progresses_after_initial_inputs(tmp_path) -> None:
    init_episode_run_pack(episode_id="pilot_phase", root=tmp_path)
    run_dir = tmp_path / "pilot_phase"
    (run_dir / "csv" / "pilot_phase.txt").write_text(
        "れいむ：こんにちは\nまりさ：解説するぜ\n",
        encoding="utf-8",
    )
    (run_dir / "ir" / "pilot_phase_production_ir.json").write_text(
        "{}\n",
        encoding="utf-8",
    )

    handoff = build_episode_run_handoff(episode_id="pilot_phase", root=tmp_path)

    assert handoff["missing_required"] == []
    assert handoff["phase"] == "build_csv"
    assert handoff["assistant_status"] == "ready_for_build_csv"

    (run_dir / "csv" / "pilot_phase.csv").write_text(
        "Speaker,Text\nれいむ,こんにちは\n",
        encoding="utf-8",
    )
    handoff = build_episode_run_handoff(episode_id="pilot_phase", root=tmp_path)

    assert handoff["phase"] == "ymm4_base_save"
    assert handoff["assistant_status"] == "waiting_for_ymm4_base_generation"
    assert handoff["pending_generated"] == ["base_ymmp"]


def test_cli_episode_run_handoff_json_stdout(tmp_path, capsys) -> None:
    main([
        "init-episode-run",
        "--episode-id",
        "pilot_cli_handoff",
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()

    code = main([
        "episode-run-handoff",
        "--episode-id",
        "pilot_cli_handoff",
        "--root",
        str(tmp_path),
        "--format",
        "json",
    ])

    assert code == 0
    result = json.loads(capsys.readouterr().out)
    assert result["episode_id"] == "pilot_cli_handoff"
    assert result["assistant_status"] == "blocked_on_initial_user_inputs"
    assert result["ng_returns"]["dry_run_ng"].endswith("pilot_cli_handoff_dry_run.json")


def test_cli_episode_run_handoff_text_mentions_script_policy_and_base_generation(
    tmp_path,
    capsys,
) -> None:
    main([
        "init-episode-run",
        "--episode-id",
        "pilot_cli_text",
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()

    code = main([
        "episode-run-handoff",
        "--episode-id",
        "pilot_cli_text",
        "--root",
        str(tmp_path),
        "--format",
        "text",
    ])

    assert code == 0
    text = capsys.readouterr().out
    assert "Current blocker:" in text
    assert "After a return:" in text
    assert "Assistant status:" not in text
    assert "Assistant next:" not in text
    assert "既存完成台本があれば新規作成不要" in text
    assert "base .ymmp はBuild CSV後に生成" in text


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
