"""G-16: motion → TachieItem.VideoEffects patch."""

import copy

from src.pipeline.ir_validate import validate_ir
from src.pipeline.ymmp_patch import (
    MOTION_ALLOWED,
    _apply_motion_to_tachie_items,
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
        motion_map={"bounce": copy.deepcopy(bounce_fx)},
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
        motion_map=None,
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
        motion_map={"bounce": bounce_fx},
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
        motion_map={"bounce": bounce_fx},
    )
    tachie_items = [
        i for i in ymmp["Timelines"][0]["Items"]
        if "TachieItem" in i.get("$type", "")
    ]
    assert len(tachie_items) == 1
    assert tachie_items[0]["Frame"] == 0
    assert tachie_items[0]["Length"] == 40
    assert tachie_items[0]["VideoEffects"] == bounce_fx
