"""G-15: transition → VoiceItem Voice/Jimaku フェード patch."""

from src.pipeline.ymmp_patch import (
    G15_JIMAKU_FADE_IN_SEC,
    G15_VOICE_FADE_IN_SEC,
    TRANSITION_ALLOWED,
    _apply_transition_voice_items,
    patch_ymmp,
)
from src.pipeline.ir_validate import validate_ir


def test_transition_allowed_none_fade_only():
    assert TRANSITION_ALLOWED == frozenset({"none", "fade"})


def test_validate_ir_rejects_slide_transition():
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
                "transition": "slide_left",
            },
        ],
    }
    vr = validate_ir(ir, known_face_labels={"f"})
    assert vr.has_errors
    assert any("TRANSITION_UNKNOWN_LABEL" in e for e in vr.errors)


def test_patch_positional_fade_sets_voice_jimaku_fades():
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
                "transition": "fade",
            },
        ],
    }
    face_map = {"n": {"Eyebrow": "e.png", "Eye": "i.png", "Mouth": "m.png"}}
    res = patch_ymmp(ymmp, ir, face_map, {})
    assert res.transition_changes >= 1
    vi = ymmp["Timelines"][0]["Items"][0]
    assert vi["VoiceFadeIn"] == G15_VOICE_FADE_IN_SEC
    assert vi["JimakuFadeIn"] == G15_JIMAKU_FADE_IN_SEC


def test_apply_transition_none_zeros_fades():
    from src.pipeline.ymmp_patch import PatchResult, _apply_transition_voice_items

    voice_items = [
        {
            "CharacterName": "a",
            "VoiceFadeIn": 0.9,
            "VoiceFadeOut": 0.8,
            "JimakuFadeIn": 0.7,
            "JimakuFadeOut": 0.6,
        }
    ]
    resolved = [
        {
            "index": 1,
            "transition": "none",
        }
    ]
    r = PatchResult()
    _apply_transition_voice_items(
        voice_items, resolved, r, use_row_range=False
    )
    assert voice_items[0]["VoiceFadeIn"] == 0.0
    assert voice_items[0]["JimakuFadeOut"] == 0.0
