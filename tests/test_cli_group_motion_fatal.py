"""GroupMotion failure classes should be fatal in CLI commands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.cli.main import (
    _cmd_apply_production,
    _cmd_patch_ymmp,
    _fatal_face_patch_warnings,
)


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _minimal_ymmp(group_items: list[dict]) -> dict:
    return {
        "Timelines": [{
            "ID": 0,
            "Items": [
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "marisa",
                    "Serif": "t1",
                    "Frame": 0,
                    "Length": 30,
                    "Layer": 1,
                },
                *group_items,
            ],
            "LayerSettings": [],
        }],
        "Characters": [{"Name": "marisa"}],
    }


def _minimal_ir(*, group_target, group_motion: str = "slide_left") -> dict:
    utt: dict = {
        "index": 1,
        "speaker": "marisa",
        "text": "t1",
        "section_id": "S1",
        "group_motion": group_motion,
    }
    if group_target is not None:
        utt["group_target"] = group_target
    return {
        "ir_version": "1.0",
        "video_id": "g20_cli_test",
        "macro": {
            "sections": [{
                "section_id": "S1",
                "start_index": 1,
                "end_index": 1,
                "default_bg": "bg1",
            }],
        },
        "utterances": [utt],
    }


def _group_motion_map() -> dict:
    return {"group_motions": {"slide_left": {"x": -320, "y": 540, "zoom": 100}}}


def test_fatal_warning_helper_includes_group_motion_failures():
    warnings = [
        "GROUP_MOTION_NO_GROUP_ITEM: x",
        "GROUP_MOTION_TARGET_MISS: y",
        "GROUP_MOTION_TARGET_AMBIGUOUS: z",
    ]
    fatal = _fatal_face_patch_warnings(warnings)
    assert len(fatal) == 3


def test_cmd_patch_ymmp_target_miss_is_fatal_in_dry_run(tmp_path: Path):
    ymmp_path = tmp_path / "in.ymmp"
    ir_path = tmp_path / "ir.json"
    gm_path = tmp_path / "group_motion_map.json"

    ymmp = _minimal_ymmp([
        {
            "$type": "YukkuriMovieMaker.Project.Items.GroupItem, YukkuriMovieMaker",
            "Remark": "existing_group",
            "Frame": 0,
            "Length": 100,
            "Layer": 4,
            "GroupRange": 2,
            "X": {"Values": [{"Value": 0.0}]},
            "Y": {"Values": [{"Value": 0.0}]},
            "Zoom": {"Values": [{"Value": 100.0}]},
        }
    ])
    _write_json(ymmp_path, ymmp)
    _write_json(ir_path, _minimal_ir(group_target="missing_group"))
    _write_json(gm_path, _group_motion_map())

    args = argparse.Namespace(
        ymmp=str(ymmp_path),
        ir_json=str(ir_path),
        face_map=None,
        face_map_bundle=None,
        bg_map=None,
        slot_map=None,
        overlay_map=None,
        se_map=None,
        timeline_profile=None,
        motion_map=None,
        tachie_motion_map=None,
        transition_map=None,
        bg_anim_map=None,
        group_motion_map=str(gm_path),
        timeline_contract=None,
        output=None,
        dry_run=True,
    )
    rc = _cmd_patch_ymmp(args)
    assert rc == 1


def test_cmd_apply_production_ambiguous_target_is_fatal_in_dry_run(tmp_path: Path):
    ymmp_path = tmp_path / "production.ymmp"
    ir_path = tmp_path / "ir.json"
    gm_path = tmp_path / "group_motion_map.json"

    ymmp = _minimal_ymmp([
        {
            "$type": "YukkuriMovieMaker.Project.Items.GroupItem, YukkuriMovieMaker",
            "Remark": "group_a",
            "Frame": 0,
            "Length": 100,
            "Layer": 4,
            "GroupRange": 2,
            "X": {"Values": [{"Value": 0.0}]},
            "Y": {"Values": [{"Value": 0.0}]},
            "Zoom": {"Values": [{"Value": 100.0}]},
        },
        {
            "$type": "YukkuriMovieMaker.Project.Items.GroupItem, YukkuriMovieMaker",
            "Remark": "group_b",
            "Frame": 0,
            "Length": 100,
            "Layer": 6,
            "GroupRange": 2,
            "X": {"Values": [{"Value": 0.0}]},
            "Y": {"Values": [{"Value": 0.0}]},
            "Zoom": {"Values": [{"Value": 100.0}]},
        },
    ])
    _write_json(ymmp_path, ymmp)
    _write_json(ir_path, _minimal_ir(group_target=None))
    _write_json(gm_path, _group_motion_map())

    args = argparse.Namespace(
        production_ymmp=str(ymmp_path),
        ir_json=str(ir_path),
        palette=None,
        face_map=None,
        refresh_maps=False,
        face_map_bundle=None,
        bg_map=None,
        slot_map=None,
        overlay_map=None,
        se_map=None,
        timeline_profile=None,
        motion_map=None,
        tachie_motion_map=None,
        transition_map=None,
        bg_anim_map=None,
        group_motion_map=str(gm_path),
        timeline_contract=None,
        csv=None,
        prompt_doc=None,
        output=None,
        dry_run=True,
        format="text",
    )
    rc = _cmd_apply_production(args)
    assert rc == 1
