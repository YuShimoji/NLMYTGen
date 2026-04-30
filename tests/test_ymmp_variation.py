"""YMM4 property-based variation probe tests."""

from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.ymmp_openability import normalize_ymmp_openability
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp
from src.pipeline.ymmp_variation import (
    extract_source_clips,
    probe_ymmp_variations,
)


ROOT = Path(__file__).resolve().parents[1]


def _anim(*values: float) -> dict:
    return {
        "Values": [{"Value": value} for value in values],
        "Span": 0.0,
        "AnimationType": "none",
    }


def _group_item(
    *,
    remark: str = "manual_clip",
    frame: int = 10,
    layer: int = 9,
    length: int = 40,
    with_rotation: bool = False,
    with_flip: bool = False,
    with_effects: bool = False,
) -> dict:
    item = {
        "$type": "YukkuriMovieMaker.Project.Items.GroupItem, YukkuriMovieMaker",
        "Remark": remark,
        "Frame": frame,
        "Layer": layer,
        "Length": length,
        "GroupRange": 2,
        "X": _anim(100.0),
        "Y": _anim(200.0),
        "Zoom": _anim(100.0),
    }
    if with_rotation:
        item["Rotation"] = _anim(0.0)
    if with_flip:
        item["IsFlipped"] = False
    if with_effects:
        item["VideoEffects"] = [
            {
                "$type": "YukkuriMovieMaker.Plugin.Effects.ShakeEffect, YukkuriMovieMaker.Plugin.Effects",
                "Name": "Shake",
                "Strength": {"Values": [{"Value": 12.0}]},
            }
        ]
    return item


def _image_item(*, frame: int = 10, layer: int = 10, remark: str = "") -> dict:
    return {
        "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
        "Remark": remark,
        "Frame": frame,
        "Layer": layer,
        "Length": 40,
        "FilePath": "body.png",
        "X": _anim(0.0),
        "Y": _anim(0.0),
        "Zoom": _anim(100.0),
    }


def _text_item(*, frame: int = 10, layer: int = 11, remark: str = "") -> dict:
    return {
        "$type": "YukkuriMovieMaker.Project.Items.TextItem, YukkuriMovieMaker",
        "Remark": remark,
        "Frame": frame,
        "Layer": layer,
        "Length": 40,
        "Text": "caption",
    }


def _ymmp(items: list[dict]) -> dict:
    return {
        "FilePath": "",
        "SelectedTimelineIndex": 0,
        "Timelines": [{
            "ID": "main",
            "Name": "main",
            "VideoInfo": {},
            "VerticalLine": {},
            "Items": items,
            "LayerSettings": {"Items": []},
            "CurrentFrame": 0,
            "Length": 1000,
            "MaxLayer": 20,
        }],
        "Characters": [],
        "CollapsedGroups": [],
        "LayoutXml": "",
        "ToolStates": {},
    }


def test_openability_guard_keeps_layer_settings_object() -> None:
    layer_settings = [{"Layer": 9, "IsHidden": False}]
    data = _ymmp([_group_item(), _image_item()])
    data["Timelines"][0]["LayerSettings"] = {"Items": layer_settings}

    result = normalize_ymmp_openability(data)

    assert result["normalized_layer_settings"] == 0
    assert data["Timelines"][0]["LayerSettings"] == {"Items": layer_settings}


def test_openability_guard_wraps_legacy_layer_settings_array() -> None:
    layer_settings = [{"Layer": 9, "IsHidden": False}]
    data = _ymmp([_group_item(), _image_item()])
    data["Timelines"][0]["LayerSettings"] = layer_settings

    result = normalize_ymmp_openability(data)

    assert result["normalized_layer_settings"] == 1
    assert data["Timelines"][0]["LayerSettings"] == {"Items": layer_settings}


def test_openability_guard_defaults_missing_layer_settings_to_object() -> None:
    data = _ymmp([_group_item(), _image_item()])
    del data["Timelines"][0]["LayerSettings"]

    result = normalize_ymmp_openability(data)

    assert result["defaulted_layer_settings"] == 1
    assert data["Timelines"][0]["LayerSettings"] == {"Items": []}


def test_openability_guard_rejects_invalid_layer_settings() -> None:
    data = _ymmp([_group_item(), _image_item()])
    data["Timelines"][0]["LayerSettings"] = {"Items": "not-array"}

    try:
        normalize_ymmp_openability(data)
    except ValueError as exc:
        assert str(exc).startswith("YMM4_LAYER_SETTINGS_INVALID")
    else:
        raise AssertionError("expected invalid LayerSettings to fail")


def test_extract_source_clips_groups_children_by_remark_layer_and_time() -> None:
    data = _ymmp([
        _group_item(remark="manual_clip"),
        _image_item(),
        _text_item(),
        _image_item(remark="foreign_clip"),
        _image_item(frame=200, layer=10, remark="other_clip"),
    ])

    clips = extract_source_clips(data)

    assert len(clips) == 3
    assert clips[0].source_remark == "manual_clip"
    assert clips[0].anchor_type == "group"
    assert [clip_item.item_index for clip_item in clips[0].items] == [0, 1, 2]
    assert clips[1].source_remark == "foreign_clip"
    assert clips[1].anchor_type == "standalone"
    assert clips[2].source_remark == "other_clip"
    assert clips[2].anchor_type == "standalone"


def test_probe_reports_routes_effect_fingerprint_and_flip_missing() -> None:
    data = _ymmp([
        _group_item(with_rotation=True, with_effects=True),
        _image_item(),
        _text_item(),
    ])

    result = probe_ymmp_variations(data)

    assert result["success"] is True
    clip = result["source_clips"][0]
    assert clip["source_remark"] == "manual_clip"
    assert clip["patchable_property_routes"]["x"][0]["route"] == "GroupItem.X.Values[].Value"
    assert clip["patchable_property_routes"]["rotation"][0]["route"] == (
        "GroupItem.Rotation.Values[].Value"
    )
    assert clip["video_effects"]["stack_count"] == 1
    assert clip["video_effects"]["stacks"][0]["effect_types"] == ["ShakeEffect"]
    assert isinstance(clip["video_effects"]["fingerprint"], str)
    variant_ids = {
        candidate["variant_id"]
        for candidate in clip["variation_candidates"]
    }
    assert {
        "nudge_left",
        "nudge_right",
        "nudge_up",
        "nudge_down",
        "scale_up",
        "scale_down",
        "rotate_small",
        "effect_reuse",
    }.issubset(variant_ids)
    assert "flip" not in variant_ids
    assert {"variant_id": "flip", "reason": "FLIP_ROUTE_MISSING"} in clip[
        "unsupported_variants"
    ]
    assert result["warnings"] == ["FLIP_ROUTE_MISSING: manual_clip"]


def test_probe_generates_flip_candidate_only_when_route_exists() -> None:
    data = _ymmp([_group_item(with_flip=True), _image_item()])

    result = probe_ymmp_variations(data)

    clip = result["source_clips"][0]
    flip_candidate = [
        candidate
        for candidate in clip["variation_candidates"]
        if candidate["variant_id"] == "flip"
    ][0]
    assert flip_candidate["operation"] == "toggle_bool"
    assert flip_candidate["target_routes"][0]["route"] == "GroupItem.IsFlipped"
    assert result["warnings"] == []


def test_probe_review_appends_variation_clips_without_mutating_source() -> None:
    data = _ymmp([_group_item(with_flip=True), _image_item()])

    result = probe_ymmp_variations(data, create_review=True, review_spacing=30)

    items = data["Timelines"][0]["Items"]
    assert result["review_clip_insertions"] == result["candidate_count"]
    assert len(items) == 2 + (result["candidate_count"] * 2)
    assert items[0]["Remark"] == "manual_clip"
    left_group = [
        item
        for item in items
        if item.get("Remark") == "variation:manual_clip:nudge_left"
        and item["$type"].split(",")[0].endswith("GroupItem")
    ][0]
    assert left_group["Frame"] > 50
    assert left_group["X"]["Values"][0]["Value"] == 60.0
    flip_group = [
        item
        for item in items
        if item.get("Remark") == "variation:manual_clip:flip"
        and item["$type"].split(",")[0].endswith("GroupItem")
    ][0]
    assert flip_group["IsFlipped"] is True


def test_probe_does_not_silently_generate_missing_transform_routes() -> None:
    data = _ymmp([_text_item(remark="caption_only")])

    result = probe_ymmp_variations(data)

    clip = result["source_clips"][0]
    assert clip["variation_candidates"] == []
    assert {"variant_id": "nudge_or_scale", "reason": "TRANSFORM_ROUTE_MISSING"} in clip[
        "unsupported_variants"
    ]
    assert {"variant_id": "flip", "reason": "FLIP_ROUTE_MISSING"} in clip[
        "unsupported_variants"
    ]


def test_cli_probe_ymmp_variations_json_on_repo_template(capsys) -> None:
    sample_path = ROOT / "samples" / "templates" / "skit_group" / "delivery_v1_templates.ymmp"

    code = main(["probe-ymmp-variations", str(sample_path), "--format", "json"])

    assert code == 0
    result = json.loads(capsys.readouterr().out)
    assert result["success"] is True
    assert result["source_clip_count"] >= 5
    assert result["candidate_count"] > 0
    assert any(
        clip["source_remark"] == "delivery_nod_v1"
        for clip in result["source_clips"]
    )


def test_cli_probe_ymmp_variations_writes_review_copy(tmp_path, capsys) -> None:
    source_path = tmp_path / "source.ymmp"
    output_path = tmp_path / "review.ymmp"
    save_ymmp(_ymmp([_group_item(with_flip=True), _image_item()]), source_path)

    code = main([
        "probe-ymmp-variations",
        str(source_path),
        "-o",
        str(output_path),
        "--format",
        "json",
    ])

    assert code == 0
    result = json.loads(capsys.readouterr().out)
    assert result["output"] == str(output_path)
    patched = load_ymmp(output_path)
    remarks = [
        item.get("Remark")
        for item in patched["Timelines"][0]["Items"]
        if isinstance(item.get("Remark"), str)
    ]
    assert "manual_clip" in remarks
    assert "variation:manual_clip:nudge_left" in remarks


def test_cli_probe_ymmp_variations_uses_review_seed_canvas(tmp_path, capsys) -> None:
    source_path = tmp_path / "source.ymmp"
    seed_path = tmp_path / "seed.ymmp"
    output_path = tmp_path / "review.ymmp"
    source = _ymmp([_group_item(), _image_item()])
    save_ymmp(source, source_path)
    seed = _ymmp([_text_item(remark="seed_canvas", frame=0, layer=1)])
    save_ymmp(seed, seed_path)

    code = main([
        "probe-ymmp-variations",
        str(source_path),
        "-o",
        str(output_path),
        "--review-seed",
        str(seed_path),
        "--format",
        "json",
    ])

    assert code == 0
    result = json.loads(capsys.readouterr().out)
    assert result["review_seed"] == str(seed_path)
    patched = load_ymmp(output_path)
    remarks = [
        item.get("Remark")
        for item in patched["Timelines"][0]["Items"]
        if isinstance(item.get("Remark"), str)
    ]
    assert "seed_canvas" in remarks
    assert "manual_clip" not in remarks
    assert "variation:manual_clip:nudge_left" in remarks


def test_cli_probe_ymmp_variations_wraps_array_layer_settings(tmp_path, capsys) -> None:
    source_path = tmp_path / "source.ymmp"
    seed_path = tmp_path / "seed_array.ymmp"
    output_path = tmp_path / "review.ymmp"
    source = _ymmp([_group_item(), _image_item()])
    save_ymmp(source, source_path)
    seed = _ymmp([_text_item(remark="seed_canvas", frame=0, layer=1)])
    seed["Timelines"][0]["LayerSettings"] = [{"Layer": 9}]
    save_ymmp(seed, seed_path)

    code = main([
        "probe-ymmp-variations",
        str(source_path),
        "-o",
        str(output_path),
        "--review-seed",
        str(seed_path),
        "--format",
        "json",
    ])

    assert code == 0
    result = json.loads(capsys.readouterr().out)
    assert result["openability"]["normalized_layer_settings"] == 1
    patched = load_ymmp(output_path)
    assert patched["Timelines"][0]["LayerSettings"] == {"Items": [{"Layer": 9}]}


def test_cli_probe_ymmp_variations_rejects_stub_review_without_seed(tmp_path, capsys) -> None:
    source_path = tmp_path / "source_stub.ymmp"
    output_path = tmp_path / "review.ymmp"
    source = {
        "SelectedTimelineIndex": 0,
        "Timelines": [{"Items": [_group_item(), _image_item()], "LayerSettings": []}],
        "Characters": [],
    }
    save_ymmp(source, source_path)

    code = main([
        "probe-ymmp-variations",
        str(source_path),
        "-o",
        str(output_path),
        "--format",
        "json",
    ])

    assert code == 1
    assert "YMM4_REVIEW_SEED_REQUIRED" in capsys.readouterr().err
