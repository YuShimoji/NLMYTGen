"""G-16: motion → TachieItem.VideoEffects patch."""

import copy

from src.pipeline.ir_validate import validate_ir
from src.pipeline.ymmp_patch import (
    MOTION_ALLOWED,
    PatchResult,
    _apply_motion_to_tachie_items,
    _parse_motion_target_layer,
    patch_ymmp,
)


def test_motion_allowed_matches_spec_section_36():
    assert MOTION_ALLOWED == frozenset({
        "none",
        "pop_in",
        "slide_in",
        "shake_small",
        "shake_big",
        "bounce",
        "fade_in",
        "fade_out",
    })


def test_validate_ir_rejects_unknown_motion_label():
    ir = {
        "ir_version": "1.0",
        "video_id": "x",
        "macro": {
            "sections": [{"section_id": "S1", "start_index": 1, "default_bg": "b"}],
        },
        "utterances": [
            {
                "index": 1,
                "speaker": "a",
                "text": "t",
                "section_id": "S1",
                "face": "f",
                "motion": "invalid_motion_xyz",
            },
        ],
    }
    vr = validate_ir(ir, known_face_labels={"f"})
    assert vr.has_errors
    assert any("MOTION_UNKNOWN_LABEL" in e for e in vr.errors)


def test_validate_ir_motion_map_unknown_label():
    ir = {
        "ir_version": "1.0",
        "video_id": "x",
        "macro": {
            "sections": [{"section_id": "S1", "start_index": 1, "default_bg": "b"}],
        },
        "utterances": [
            {
                "index": 1,
                "speaker": "a",
                "text": "t",
                "section_id": "S1",
                "face": "f",
                "motion": "bounce",
            },
        ],
    }
    vr = validate_ir(
        ir,
        known_face_labels={"f"},
        known_motion_labels={"pop_in"},
    )
    assert vr.has_errors
    assert any("MOTION_MAP_UNKNOWN_LABEL" in e for e in vr.errors)


def test_validate_ir_group_motion_map_unknown_label():
    ir = {
        "ir_version": "1.0",
        "video_id": "x",
        "macro": {
            "sections": [{"section_id": "S1", "start_index": 1, "default_bg": "b"}],
        },
        "utterances": [
            {
                "index": 1,
                "speaker": "a",
                "text": "t",
                "section_id": "S1",
                "face": "f",
                "group_target": "main_group",
                "group_motion": "slide_left",
            },
        ],
    }
    vr = validate_ir(
        ir,
        known_face_labels={"f"},
        known_group_motion_labels={"zoom_in"},
    )
    assert vr.has_errors
    assert any("GROUP_MOTION_UNKNOWN_LABEL" in e for e in vr.errors)


def _ir_one_utt_group(*, group_target, group_motion: str = "slide_left") -> dict:
    return {
        "ir_version": "1.0",
        "video_id": "x",
        "macro": {
            "sections": [{"section_id": "S1", "start_index": 1, "end_index": 1, "default_bg": "b"}],
        },
        "utterances": [
            {
                "index": 1,
                "speaker": "a",
                "text": "t",
                "section_id": "S1",
                "face": "f",
                "group_target": group_target,
                "group_motion": group_motion,
            },
        ],
    }


def test_validate_ir_group_target_empty_string():
    vr = validate_ir(_ir_one_utt_group(group_target=""), known_face_labels={"f"})
    assert vr.has_errors
    assert any(e.startswith("GROUP_TARGET_EMPTY:") for e in vr.errors)


def test_validate_ir_group_target_whitespace_only():
    vr = validate_ir(_ir_one_utt_group(group_target="   "), known_face_labels={"f"})
    assert vr.has_errors
    assert any(e.startswith("GROUP_TARGET_EMPTY:") for e in vr.errors)


def test_validate_ir_group_target_surrounding_whitespace():
    vr = validate_ir(_ir_one_utt_group(group_target=" main "), known_face_labels={"f"})
    assert vr.has_errors
    assert any(
        e.startswith("GROUP_TARGET_SURROUNDING_WHITESPACE:") for e in vr.errors
    )


def test_validate_ir_group_target_newline_rejected():
    vr = validate_ir(_ir_one_utt_group(group_target="a\nb"), known_face_labels={"f"})
    assert vr.has_errors
    assert any(e.startswith("GROUP_TARGET_NEWLINE:") for e in vr.errors)


def test_apply_motion_sets_tachie_video_effects():
    bounce_fx = [
        {
            "$type": "YukkuriMovieMaker.Plugin.Effects.BounceEffect, YukkuriMovieMaker.Plugin.Effects",
            "Name": "Bounce",
        },
    ]
    ymmp = {
        "Timelines": [{
            "ID": 0,
            "Items": [
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Serif": "x",
                    "Frame": 0,
                    "Length": 50,
                    "Layer": 1,
                    "TachieFaceParameter": {
                        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter",
                        "Eyebrow": "e.png",
                        "Eye": "i.png",
                        "Mouth": "m.png",
                        "Hair": "",
                        "Body": "",
                        "Complexion": "",
                    },
                },
                {
                    "$type": "YukkuriMovieMaker.Project.Items.TachieItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Layer": 2,
                    "TachieItemParameter": {
                        "X": 0.0,
                        "Y": 0.0,
                        "Zoom": 100.0,
                    },
                },
            ],
            "LayerSettings": [],
        }],
        "Characters": [{"Name": "a"}],
    }
    ir = {
        "ir_version": "1.0",
        "video_id": "t",
        "macro": {"sections": []},
        "utterances": [
            {
                "index": 1,
                "speaker": "a",
                "text": "x",
                "section_id": "S1",
                "face": "n",
                "motion": "bounce",
            },
        ],
    }
    res = patch_ymmp(
        ymmp,
        ir,
        {"n": {"Eye": "i.png", "Mouth": "m.png", "Eyebrow": "e.png"}},
        {},
        tachie_motion_effects_map={"bounce": copy.deepcopy(bounce_fx)},
    )
    assert res.motion_changes >= 1
    items = ymmp["Timelines"][0]["Items"]
    tachie = [i for i in items if "TachieItem" in i.get("$type", "")]
    assert len(tachie) == 1
    assert tachie[0]["VideoEffects"] == bounce_fx


def test_apply_motion_none_clears_video_effects():
    ymmp = {
        "Timelines": [{
            "ID": 0,
            "Items": [
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Serif": "x",
                    "Frame": 0,
                    "Length": 50,
                    "Layer": 1,
                    "TachieFaceParameter": {
                        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter",
                        "Eyebrow": "e.png",
                        "Eye": "i.png",
                        "Mouth": "m.png",
                        "Hair": "",
                        "Body": "",
                        "Complexion": "",
                    },
                },
                {
                    "$type": "YukkuriMovieMaker.Project.Items.TachieItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Layer": 2,
                    "VideoEffects": [
                        {
                            "$type": "YukkuriMovieMaker.Plugin.Effects.BounceEffect, YukkuriMovieMaker.Plugin.Effects",
                            "Name": "Bounce",
                        },
                    ],
                    "TachieItemParameter": {
                        "X": 0.0,
                        "Y": 0.0,
                        "Zoom": 100.0,
                    },
                },
            ],
            "LayerSettings": [],
        }],
        "Characters": [{"Name": "a"}],
    }
    ir = {
        "ir_version": "1.0",
        "video_id": "t",
        "macro": {"sections": []},
        "utterances": [
            {
                "index": 1,
                "speaker": "a",
                "text": "x",
                "section_id": "S1",
                "face": "n",
                "motion": "none",
            },
        ],
    }
    res = patch_ymmp(
        ymmp,
        ir,
        {"n": {"Eye": "i.png", "Mouth": "m.png", "Eyebrow": "e.png"}},
        {},
        tachie_motion_effects_map=None,
    )
    assert res.motion_changes >= 1
    items = ymmp["Timelines"][0]["Items"]
    tachie = [i for i in items if "TachieItem" in i.get("$type", "")]
    assert tachie[0]["VideoEffects"] == []


def test_apply_motion_helper_no_tachie_warns():
    from src.pipeline.ymmp_patch import PatchResult

    items: list[dict] = []
    resolved = [
        {
            "index": 1,
            "speaker": "ghost",
            "motion": "bounce",
        },
    ]
    result = PatchResult()
    voice_items = [{
        "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
        "CharacterName": "ghost",
        "Frame": 0,
        "Length": 30,
    }]
    _apply_motion_to_tachie_items(
        items,
        voice_items,
        resolved,
        {"bounce": [{"$type": "X", "Name": "Bounce"}]},
        result,
        use_row_range=False,
    )
    assert any(w.startswith("MOTION_NO_TACHIE_ITEM:") for w in (result.warnings or []))


def test_phase2_motion_splits_tachie_by_utterance_timing():
    ymmp = {
        "Timelines": [{
            "ID": 0,
            "Items": [
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Serif": "u1",
                    "Frame": 0,
                    "Length": 30,
                    "Layer": 1,
                    "TachieFaceParameter": {
                        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter",
                        "Eyebrow": "e.png",
                        "Eye": "i.png",
                        "Mouth": "m.png",
                        "Hair": "",
                        "Body": "",
                        "Complexion": "",
                    },
                },
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Serif": "u2",
                    "Frame": 30,
                    "Length": 30,
                    "Layer": 1,
                    "TachieFaceParameter": {
                        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter",
                        "Eyebrow": "e.png",
                        "Eye": "i.png",
                        "Mouth": "m.png",
                        "Hair": "",
                        "Body": "",
                        "Complexion": "",
                    },
                },
                {
                    "$type": "YukkuriMovieMaker.Project.Items.TachieItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Frame": 0,
                    "Length": 60,
                    "Layer": 2,
                    "TachieItemParameter": {"X": 0.0, "Y": 0.0, "Zoom": 100.0},
                },
            ],
            "LayerSettings": [],
        }],
        "Characters": [{"Name": "a"}],
    }
    ir = {
        "ir_version": "1.0",
        "video_id": "t",
        "macro": {"sections": []},
        "utterances": [
            {"index": 1, "speaker": "a", "text": "u1", "section_id": "S1", "face": "n", "motion": "bounce"},
            {"index": 2, "speaker": "a", "text": "u2", "section_id": "S1", "face": "n", "motion": "none"},
        ],
    }
    bounce_fx = [{
        "$type": "YukkuriMovieMaker.Plugin.Effects.BounceEffect, YukkuriMovieMaker.Plugin.Effects",
        "Name": "Bounce",
    }]
    patch_ymmp(
        ymmp,
        ir,
        {"n": {"Eye": "i.png", "Mouth": "m.png", "Eyebrow": "e.png"}},
        {},
        tachie_motion_effects_map={"bounce": bounce_fx},
    )
    tachie_items = [
        i for i in ymmp["Timelines"][0]["Items"]
        if "TachieItem" in i.get("$type", "")
    ]
    assert len(tachie_items) == 2
    assert tachie_items[0]["Frame"] == 0
    assert tachie_items[0]["Length"] == 30
    assert tachie_items[0]["VideoEffects"] == bounce_fx
    assert tachie_items[1]["Frame"] == 30
    assert tachie_items[1]["Length"] == 30
    assert tachie_items[1]["VideoEffects"] == []


def test_phase2_motion_respects_row_range_anchor():
    ymmp = {
        "Timelines": [{
            "ID": 0,
            "Items": [
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Serif": "r1",
                    "Frame": 0,
                    "Length": 20,
                    "Layer": 1,
                    "TachieFaceParameter": {
                        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter",
                        "Eyebrow": "e.png",
                        "Eye": "i.png",
                        "Mouth": "m.png",
                        "Hair": "",
                        "Body": "",
                        "Complexion": "",
                    },
                },
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Serif": "r2",
                    "Frame": 20,
                    "Length": 20,
                    "Layer": 1,
                    "TachieFaceParameter": {
                        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter",
                        "Eyebrow": "e.png",
                        "Eye": "i.png",
                        "Mouth": "m.png",
                        "Hair": "",
                        "Body": "",
                        "Complexion": "",
                    },
                },
                {
                    "$type": "YukkuriMovieMaker.Project.Items.TachieItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Frame": 0,
                    "Length": 40,
                    "Layer": 2,
                    "TachieItemParameter": {"X": 0.0, "Y": 0.0, "Zoom": 100.0},
                },
            ],
            "LayerSettings": [],
        }],
        "Characters": [{"Name": "a"}],
    }
    ir = {
        "ir_version": "1.0",
        "video_id": "t",
        "macro": {"sections": []},
        "utterances": [
            {
                "index": 1,
                "row_start": 1,
                "row_end": 2,
                "speaker": "a",
                "text": "x",
                "section_id": "S1",
                "face": "n",
                "motion": "bounce",
            },
        ],
    }
    bounce_fx = [{
        "$type": "YukkuriMovieMaker.Plugin.Effects.BounceEffect, YukkuriMovieMaker.Plugin.Effects",
        "Name": "Bounce",
    }]
    patch_ymmp(
        ymmp,
        ir,
        {"n": {"Eye": "i.png", "Mouth": "m.png", "Eyebrow": "e.png"}},
        {},
        tachie_motion_effects_map={"bounce": bounce_fx},
    )
    tachie_items = [
        i for i in ymmp["Timelines"][0]["Items"]
        if "TachieItem" in i.get("$type", "")
    ]
    assert len(tachie_items) == 1
    assert tachie_items[0]["Frame"] == 0
    assert tachie_items[0]["Length"] == 40
    assert tachie_items[0]["VideoEffects"] == bounce_fx


# --- G-20 Slice 2: relative mode ---


def _make_group_motion_ymmp(*, group_x=100.0, group_y=200.0, group_zoom=100.0):
    """GroupItem を 1 件持つ最小 ymmp."""
    return {
        "Timelines": [{
            "ID": 0,
            "Items": [
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Serif": "hello",
                    "Frame": 0,
                    "Length": 50,
                    "Layer": 1,
                    "TachieFaceParameter": {
                        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter",
                        "Eyebrow": "e.png", "Eye": "i.png", "Mouth": "m.png",
                        "Hair": "", "Body": "", "Complexion": "",
                    },
                },
                {
                    "$type": "YukkuriMovieMaker.Project.Items.GroupItem, YukkuriMovieMaker",
                    "Remark": "main",
                    "X": group_x,
                    "Y": group_y,
                    "Zoom": group_zoom,
                    "Layer": 2,
                },
            ],
            "LayerSettings": [],
        }],
        "Characters": [{"Name": "a"}],
    }


def _group_motion_ir(*, group_target="main", group_motion="slide_left"):
    return {
        "ir_version": "1.0",
        "video_id": "t",
        "macro": {"sections": [{"section_id": "S1", "start_index": 1, "end_index": 1, "default_bg": "b"}]},
        "utterances": [
            {
                "index": 1, "speaker": "a", "text": "hello", "section_id": "S1",
                "face": "n", "group_target": group_target, "group_motion": group_motion,
            },
        ],
    }


def test_group_motion_absolute_mode_unchanged():
    """absolute (既定) は従来と同じ絶対値書き込み."""
    ymmp = _make_group_motion_ymmp(group_x=100.0, group_y=200.0, group_zoom=100.0)
    ir = _group_motion_ir()
    gm_map = {"slide_left": {"x": -320, "y": 540, "zoom": 100}}
    res = patch_ymmp(ymmp, ir, {"n": {"Eye": "i.png", "Mouth": "m.png", "Eyebrow": "e.png"}}, {},
                     group_motion_map=gm_map)
    gi = [i for i in ymmp["Timelines"][0]["Items"] if "GroupItem" in i.get("$type", "")][0]
    assert gi["X"] == -320.0
    assert gi["Y"] == 540.0
    assert gi["Zoom"] == 100.0
    assert res.group_motion_changes >= 1


def test_group_motion_absolute_mode_explicit():
    """mode: absolute を明示しても同じ挙動."""
    ymmp = _make_group_motion_ymmp(group_x=50.0)
    ir = _group_motion_ir()
    gm_map = {"slide_left": {"mode": "absolute", "x": -320, "y": 540, "zoom": 100}}
    patch_ymmp(ymmp, ir, {"n": {"Eye": "i.png", "Mouth": "m.png", "Eyebrow": "e.png"}}, {},
               group_motion_map=gm_map)
    gi = [i for i in ymmp["Timelines"][0]["Items"] if "GroupItem" in i.get("$type", "")][0]
    assert gi["X"] == -320.0


def test_group_motion_relative_mode_adds_to_current():
    """mode: relative は現在値に加算する."""
    ymmp = _make_group_motion_ymmp(group_x=100.0, group_y=200.0, group_zoom=100.0)
    ir = _group_motion_ir()
    gm_map = {"slide_left": {"mode": "relative", "x": -50, "y": 30, "zoom": 10}}
    res = patch_ymmp(ymmp, ir, {"n": {"Eye": "i.png", "Mouth": "m.png", "Eyebrow": "e.png"}}, {},
                     group_motion_map=gm_map)
    gi = [i for i in ymmp["Timelines"][0]["Items"] if "GroupItem" in i.get("$type", "")][0]
    assert gi["X"] == 50.0    # 100 + (-50)
    assert gi["Y"] == 230.0   # 200 + 30
    assert gi["Zoom"] == 110.0  # 100 + 10
    assert res.group_motion_changes >= 1


def test_group_motion_relative_mode_with_keyframe_dict():
    """keyframe 形式 (Values[0].Value) でも relative が効く."""
    ymmp = _make_group_motion_ymmp()
    gi = [i for i in ymmp["Timelines"][0]["Items"] if "GroupItem" in i.get("$type", "")][0]
    gi["X"] = {"Values": [{"Value": 200.0}]}
    ir = _group_motion_ir()
    gm_map = {"slide_left": {"mode": "relative", "x": -80}}
    patch_ymmp(ymmp, ir, {"n": {"Eye": "i.png", "Mouth": "m.png", "Eyebrow": "e.png"}}, {},
               group_motion_map=gm_map)
    assert gi["X"]["Values"][0]["Value"] == 120.0  # 200 + (-80)


def test_group_motion_relative_partial_axes():
    """relative で一部の軸だけ指定した場合、指定外の軸は変わらない."""
    ymmp = _make_group_motion_ymmp(group_x=100.0, group_y=200.0, group_zoom=80.0)
    ir = _group_motion_ir()
    gm_map = {"slide_left": {"mode": "relative", "x": 10}}
    patch_ymmp(ymmp, ir, {"n": {"Eye": "i.png", "Mouth": "m.png", "Eyebrow": "e.png"}}, {},
               group_motion_map=gm_map)
    gi = [i for i in ymmp["Timelines"][0]["Items"] if "GroupItem" in i.get("$type", "")][0]
    assert gi["X"] == 110.0
    assert gi["Y"] == 200.0   # 変更なし
    assert gi["Zoom"] == 80.0  # 変更なし


def test_load_group_motion_map_rejects_invalid_mode():
    """不正な mode はロード時にエラー."""
    import json
    import tempfile
    from src.cli.main import _load_group_motion_map

    data = {"group_motions": {"bad": {"mode": "incremental", "x": 10}}}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        f.flush()
        import pytest
        with pytest.raises(ValueError, match="invalid mode"):
            _load_group_motion_map(f.name)


# ---------------------------------------------------------------------------
# motion_target: ImageItem / GroupItem への VideoEffects 適用
# ---------------------------------------------------------------------------

_BOUNCE_FX = [{"$type": "YukkuriMovieMaker.Plugin.Effects.BounceEffect, YukkuriMovieMaker.Plugin.Effects", "Name": "Bounce"}]
_FACE_MAP = {"n": {"Eye": "i.png", "Mouth": "m.png", "Eyebrow": "e.png"}}
_MOTION_MAP = {"bounce": _BOUNCE_FX}


def _make_layer_motion_ymmp(*, target_layer=5, item_type="ImageItem",
                            frame=0, length=60):
    """VoiceItem + 指定レイヤーの ImageItem/GroupItem を含む最小 YMMP."""
    full_type = f"YukkuriMovieMaker.Project.Items.{item_type}, YukkuriMovieMaker"
    return {
        "Timelines": [{
            "ID": 0,
            "Items": [
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Serif": "x",
                    "Frame": 0,
                    "Length": 30,
                    "Layer": 1,
                    "TachieFaceParameter": {
                        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter",
                        "Eyebrow": "e.png", "Eye": "i.png", "Mouth": "m.png",
                        "Hair": "", "Body": "", "Complexion": "",
                    },
                },
                {
                    "$type": full_type,
                    "Layer": target_layer,
                    "Frame": frame,
                    "Length": length,
                    "VideoEffects": [],
                    "Remark": "",
                    "FilePath": "dummy.png" if item_type == "ImageItem" else "",
                },
            ],
            "LayerSettings": [],
        }],
        "Characters": [{"Name": "a"}],
    }


def _layer_motion_ir(*, motion_target="layer:5", motion="bounce"):
    """motion_target 付きの最小 IR."""
    utt = {
        "index": 1, "speaker": "a", "text": "x", "section_id": "S1",
        "face": "n", "motion": motion, "motion_target": motion_target,
    }
    return {
        "ir_version": "1.0", "video_id": "t",
        "macro": {"sections": []},
        "utterances": [utt],
    }


def test_parse_motion_target_layer_formats():
    assert _parse_motion_target_layer("layer:10") == 10
    assert _parse_motion_target_layer({"layer": 5}) == 5
    assert _parse_motion_target_layer({"layer": "7"}) == 7
    assert _parse_motion_target_layer("layer:") is None
    assert _parse_motion_target_layer("layer:abc") is None
    assert _parse_motion_target_layer({"X": 1}) is None
    assert _parse_motion_target_layer("speaker") is None
    assert _parse_motion_target_layer(42) is None
    assert _parse_motion_target_layer(None) is None


def test_motion_target_layer_applies_to_image_item():
    """単一 ImageItem に VideoEffects が書き込まれる (主 happy path)."""
    ymmp = _make_layer_motion_ymmp()
    ir = _layer_motion_ir()
    res = patch_ymmp(ymmp, ir, _FACE_MAP, {},
                     tachie_motion_effects_map=_MOTION_MAP)
    items = ymmp["Timelines"][0]["Items"]
    images = [i for i in items if "ImageItem" in i.get("$type", "")]
    assert len(images) >= 1
    assert any(i.get("VideoEffects") == _BOUNCE_FX for i in images)
    assert res.motion_changes >= 1


def test_motion_target_splits_image_item_by_timing():
    """2 utterance で 1 ImageItem が分��される."""
    ymmp = {
        "Timelines": [{
            "ID": 0,
            "Items": [
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a", "Serif": "x",
                    "Frame": 0, "Length": 30, "Layer": 1,
                    "TachieFaceParameter": {
                        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter",
                        "Eyebrow": "e.png", "Eye": "i.png", "Mouth": "m.png",
                        "Hair": "", "Body": "", "Complexion": "",
                    },
                },
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a", "Serif": "y",
                    "Frame": 30, "Length": 30, "Layer": 1,
                    "TachieFaceParameter": {
                        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter",
                        "Eyebrow": "e.png", "Eye": "i.png", "Mouth": "m.png",
                        "Hair": "", "Body": "", "Complexion": "",
                    },
                },
                {
                    "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
                    "Layer": 5, "Frame": 0, "Length": 60,
                    "VideoEffects": [], "Remark": "", "FilePath": "dummy.png",
                },
            ],
            "LayerSettings": [],
        }],
        "Characters": [{"Name": "a"}],
    }
    ir = {
        "ir_version": "1.0", "video_id": "t",
        "macro": {"sections": []},
        "utterances": [
            {"index": 1, "speaker": "a", "text": "x", "section_id": "S1",
             "face": "n", "motion": "bounce", "motion_target": "layer:5"},
            {"index": 2, "speaker": "a", "text": "y", "section_id": "S1",
             "face": "n", "motion": "none", "motion_target": "layer:5"},
        ],
    }
    res = patch_ymmp(ymmp, ir, _FACE_MAP, {},
                     tachie_motion_effects_map=_MOTION_MAP)
    items = ymmp["Timelines"][0]["Items"]
    images = [i for i in items if "ImageItem" in i.get("$type", "")]
    assert len(images) == 2
    bounce_seg = [i for i in images if i.get("VideoEffects") == _BOUNCE_FX]
    none_seg = [i for i in images if i.get("VideoEffects") == []]
    assert len(bounce_seg) == 1
    assert len(none_seg) == 1
    assert bounce_seg[0]["Frame"] == 0
    assert bounce_seg[0]["Length"] == 30
    assert none_seg[0]["Frame"] == 30
    assert res.motion_changes >= 2


def test_motion_target_no_item_on_layer_warns():
    """対象レイヤーにアイテムなし → 警告."""
    ymmp = _make_layer_motion_ymmp(target_layer=99)
    ir = _layer_motion_ir(motion_target="layer:5", motion="bounce")
    res = patch_ymmp(ymmp, ir, _FACE_MAP, {},
                     tachie_motion_effects_map=_MOTION_MAP)
    assert any(w.startswith("MOTION_TARGET_NO_ITEM:") for w in (res.warnings or []))


def test_motion_target_speaker_uses_tachie_path():
    """motion_target='speaker' → layer-items 経路ではなく TachieItem 経路を使用."""
    ymmp = {
        "Timelines": [{
            "ID": 0,
            "Items": [
                {
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a", "Serif": "x",
                    "Frame": 0, "Length": 30, "Layer": 1,
                    "TachieFaceParameter": {
                        "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter",
                        "Eyebrow": "e.png", "Eye": "i.png", "Mouth": "m.png",
                        "Hair": "", "Body": "", "Complexion": "",
                    },
                },
                {
                    "$type": "YukkuriMovieMaker.Project.Items.TachieItem, YukkuriMovieMaker",
                    "CharacterName": "a", "Layer": 2, "Frame": 0, "Length": 60,
                    "VideoEffects": [],
                    "TachieItemParameter": {"X": 0.0, "Y": 0.0, "Zoom": 100.0},
                },
            ],
            "LayerSettings": [],
        }],
        "Characters": [{"Name": "a"}],
    }
    ir = _layer_motion_ir(motion_target="speaker", motion="bounce")
    res = patch_ymmp(ymmp, ir, _FACE_MAP, {},
                     tachie_motion_effects_map=_MOTION_MAP)
    items = ymmp["Timelines"][0]["Items"]
    tachie = [i for i in items if "TachieItem" in i.get("$type", "")]
    assert any(t.get("VideoEffects") == _BOUNCE_FX for t in tachie)
    assert res.motion_changes >= 1


def test_motion_target_none_clears_effects():
    """motion='none' + motion_target → VideoEffects は空."""
    ymmp = _make_layer_motion_ymmp()
    ir = _layer_motion_ir(motion="none")
    res = patch_ymmp(ymmp, ir, _FACE_MAP, {},
                     tachie_motion_effects_map=_MOTION_MAP)
    items = ymmp["Timelines"][0]["Items"]
    images = [i for i in items if "ImageItem" in i.get("$type", "")]
    for img in images:
        assert img.get("VideoEffects", []) == []


def test_validate_ir_motion_target_invalid_string():
    """IR validation: 不正文字列 → MOTION_TARGET_INVALID."""
    ir = {
        "ir_version": "1.0", "video_id": "t",
        "macro": {"sections": []},
        "utterances": [
            {"index": 1, "speaker": "a", "text": "x", "section_id": "S1",
             "face": "n", "motion_target": "invalid_format"},
        ],
    }
    vr = validate_ir(ir)
    assert vr.has_errors
    assert any("MOTION_TARGET_INVALID" in e for e in vr.errors)


def test_validate_ir_motion_target_dict_missing_layer():
    """IR validation: layer キーなし dict → MOTION_TARGET_INVALID."""
    ir = {
        "ir_version": "1.0", "video_id": "t",
        "macro": {"sections": []},
        "utterances": [
            {"index": 1, "speaker": "a", "text": "x", "section_id": "S1",
             "face": "n", "motion_target": {"X": 1}},
        ],
    }
    vr = validate_ir(ir)
    assert vr.has_errors
    assert any("MOTION_TARGET_INVALID" in e for e in vr.errors)
