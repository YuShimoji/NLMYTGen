"""G-14: bg_anim → ImageItem X/Y/Zoom 線形キーフレーム patch."""

from src.pipeline.ymmp_patch import (
    BG_ANIM_ALLOWED,
    PatchResult,
    _apply_bg_anim_to_image_item,
    _item_type,
    patch_ymmp,
)


def test_bg_anim_allowed_enum_matches_spec():
    assert "ken_burns" in BG_ANIM_ALLOWED
    assert "none" in BG_ANIM_ALLOWED


def test_apply_bg_anim_sets_linear_keyframes():
    item: dict = {
        "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
        "X": {"Values": [{"Value": 0.0}], "Span": 0.0, "AnimationType": "なし"},
    }
    r = PatchResult()
    _apply_bg_anim_to_image_item(item, "zoom_in", 120, r)
    assert r.bg_anim_changes == 1
    assert len(item["Zoom"]["Values"]) == 2
    assert item["Zoom"]["Span"] == 120.0
    assert item["X"]["Values"][0]["Value"] == 0.0


def test_patch_ymmp_applies_bg_anim_per_section():
    ymmp = {
        "Timelines": [{
            "ID": 0,
            "Items": [
                {
                    "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
                    "FilePath": "C:/bg0.png",
                    "Layer": 0,
                    "Frame": 0,
                    "Length": 500,
                    "X": {"Values": [{"Value": 0.0}], "Span": 0.0, "AnimationType": "なし"},
                    "Y": {"Values": [{"Value": 0.0}], "Span": 0.0, "AnimationType": "なし"},
                    "Zoom": {"Values": [{"Value": 100.0}], "Span": 0.0, "AnimationType": "なし"},
                },
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
                    "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
                    "CharacterName": "a",
                    "Serif": "y",
                    "Frame": 50,
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
            ],
            "LayerSettings": [],
        }],
        "Characters": [{"Name": "a"}],
    }
    ir = {
        "ir_version": "1.0",
        "video_id": "t",
        "macro": {
            "sections": [{
                "section_id": "S1",
                "start_index": 1,
                "default_bg": "bg1",
            }],
        },
        "utterances": [
            {
                "index": 1,
                "speaker": "a",
                "text": "x",
                "section_id": "S1",
                "face": "n",
                "bg_anim": "pan_left",
            },
            {
                "index": 2,
                "speaker": "a",
                "text": "y",
                "section_id": "S1",
                "face": "n",
            },
        ],
    }
    face_map = {"n": {"Eyebrow": "e.png", "Eye": "i.png", "Mouth": "m.png"}}
    bg_map = {"bg1": "D:/newbg.png"}
    res = patch_ymmp(ymmp, ir, face_map, bg_map)
    assert res.bg_additions >= 1
    assert res.bg_anim_changes == 1
    items = ymmp["Timelines"][0]["Items"]
    bg_items = [
        i for i in items
        if _item_type(i) == "ImageItem" and i.get("Layer") == 0
    ]
    assert bg_items
    last_bg = bg_items[-1]
    assert len(last_bg["X"]["Values"]) == 2


def test_validate_ir_rejects_unknown_bg_anim():
    from src.pipeline.ir_validate import validate_ir

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
                "bg_anim": "not_a_real_preset",
            },
        ],
    }
    vr = validate_ir(ir, known_face_labels={"f"})
    assert vr.has_errors
    assert any("BG_ANIM_UNKNOWN_LABEL" in e for e in vr.errors)
