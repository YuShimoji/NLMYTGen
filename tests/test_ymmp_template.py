"""extract-template --labeled + character-scoped face_map + adapter 互換テスト."""

from __future__ import annotations

import copy

import pytest

from src.pipeline.ymmp_extract import (
    ExtractResult,
    FacePattern,
    extract_template_labeled,
    generate_face_map_labeled,
    generate_bg_map_labeled,
)
from src.pipeline.ymmp_patch import _resolve_face_parts, patch_ymmp


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_voice_item(
    char: str,
    remark: str,
    eb: str = "eb_a.png",
    ey: str = "ey_a.png",
    mo: str = "mo_a.png",
    *,
    frame: int = 0,
    has_face_param: bool = True,
) -> dict:
    item = {
        "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
        "CharacterName": char,
        "Remark": remark,
        "Serif": "test",
        "Frame": frame,
        "Length": 100,
        "Layer": 1,
        "Group": 0,
        "IsLocked": False,
        "IsHidden": False,
    }
    if has_face_param:
        item["TachieFaceParameter"] = {
            "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
            "Eyebrow": eb,
            "Eye": ey,
            "Mouth": mo,
            "Hair": "",
            "Body": "",
            "Complexion": "",
        }
    return item


def _make_tachie_item(
    char: str,
    remark: str,
    eb: str = "eb_a.png",
    ey: str = "ey_a.png",
    mo: str = "mo_a.png",
    *,
    frame: int = 0,
) -> dict:
    return {
        "$type": "YukkuriMovieMaker.Project.Items.TachieItem, YukkuriMovieMaker",
        "CharacterName": char,
        "Remark": remark,
        "Frame": frame,
        "Length": 100,
        "Layer": 0,
        "Group": 0,
        "IsLocked": False,
        "IsHidden": False,
        "TachieItemParameter": {
            "Eyebrow": eb,
            "Eye": ey,
            "Mouth": mo,
            "Hair": "",
            "Body": "",
            "X": 0.0,
            "Y": 540.0,
            "Zoom": 100.0,
        },
    }


def _make_tachie_face_item(
    char: str,
    remark: str,
    eb: str = "eb_a.png",
    ey: str = "ey_a.png",
    mo: str = "mo_a.png",
    *,
    frame: int = 0,
) -> dict:
    """TachieFaceItem (表情アイテム) — YMM4 で表情変更に使うアイテム."""
    return {
        "$type": "YukkuriMovieMaker.Project.Items.TachieFaceItem, YukkuriMovieMaker",
        "CharacterName": char,
        "Remark": remark,
        "Frame": frame,
        "Length": 100,
        "Layer": 0,
        "Group": 0,
        "IsLocked": False,
        "IsHidden": False,
        "TachieFaceParameter": {
            "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
            "Eyebrow": eb,
            "Eye": ey,
            "Mouth": mo,
            "Hair": "",
            "Body": "",
            "Complexion": "",
        },
    }


def _make_image_item(
    remark: str,
    filepath: str,
    *,
    frame: int = 0,
    layer: int = 0,
) -> dict:
    return {
        "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
        "Remark": remark,
        "FilePath": filepath,
        "Frame": frame,
        "Length": 100,
        "Layer": layer,
        "Group": 0,
        "IsLocked": False,
        "IsHidden": False,
    }


def _wrap_ymmp(items: list[dict], characters: list[str] | None = None) -> dict:
    chars = [{"Name": c} for c in (characters or [])]
    return {
        "Timelines": [{
            "ID": 0,
            "Items": items,
            "LayerSettings": [],
        }],
        "Characters": chars,
    }


# ---------------------------------------------------------------------------
# extract_template_labeled
# ---------------------------------------------------------------------------

class TestExtractTemplateLabeled:
    def test_single_char_single_label(self):
        ymmp = _wrap_ymmp([
            _make_voice_item("marisa", "serious", "eb01.png", "ey01.png", "mo01.png"),
        ])
        result = extract_template_labeled(ymmp)
        assert not result.conflicts
        assert "marisa" in result.labeled_faces
        assert "serious" in result.labeled_faces["marisa"]
        pat = result.labeled_faces["marisa"]["serious"]
        assert pat.eyebrow == "eb01.png"

    def test_multi_char_same_label(self):
        ymmp = _wrap_ymmp([
            _make_voice_item("marisa", "serious", "eb01.png", "ey01.png", "mo01.png"),
            _make_voice_item("reimu", "serious", "eb02.png", "ey02.png", "mo02.png"),
        ])
        result = extract_template_labeled(ymmp)
        assert not [c for c in result.conflicts if c.startswith("Conflict:")]
        assert result.labeled_faces["marisa"]["serious"].eyebrow == "eb01.png"
        assert result.labeled_faces["reimu"]["serious"].eyebrow == "eb02.png"

    def test_same_char_same_label_same_parts_idempotent(self):
        ymmp = _wrap_ymmp([
            _make_voice_item("marisa", "serious", "eb01.png", "ey01.png", "mo01.png"),
            _make_voice_item("marisa", "serious", "eb01.png", "ey01.png", "mo01.png"),
        ])
        result = extract_template_labeled(ymmp)
        assert not [c for c in result.conflicts if c.startswith("Conflict:")]
        assert len(result.labeled_faces["marisa"]) == 1

    def test_same_char_same_label_different_parts_conflict(self):
        ymmp = _wrap_ymmp([
            _make_voice_item("marisa", "serious", "eb01.png", "ey01.png", "mo01.png"),
            _make_voice_item("marisa", "serious", "eb99.png", "ey99.png", "mo99.png"),
        ])
        result = extract_template_labeled(ymmp)
        errors = [c for c in result.conflicts if c.startswith("Conflict:")]
        assert len(errors) == 1
        assert "marisa.serious" in errors[0]

    def test_empty_remark_skipped(self):
        ymmp = _wrap_ymmp([
            _make_voice_item("marisa", "", "eb01.png", "ey01.png", "mo01.png"),
            _make_voice_item("marisa", "   ", "eb02.png", "ey02.png", "mo02.png"),
        ])
        result = extract_template_labeled(ymmp)
        assert len(result.labeled_faces) == 0

    def test_remark_whitespace_stripped(self):
        ymmp = _wrap_ymmp([
            _make_voice_item("marisa", "  serious  ", "eb01.png", "ey01.png", "mo01.png"),
        ])
        result = extract_template_labeled(ymmp)
        assert "serious" in result.labeled_faces["marisa"]

    def test_no_character_name_warning(self):
        ymmp = _wrap_ymmp([
            _make_voice_item("", "serious", "eb01.png", "ey01.png", "mo01.png"),
        ])
        result = extract_template_labeled(ymmp)
        warnings = [c for c in result.conflicts if "CharacterName is empty" in c]
        assert len(warnings) == 1
        assert len(result.labeled_faces) == 0

    def test_no_face_parameter_warning(self):
        ymmp = _wrap_ymmp([
            _make_voice_item("marisa", "serious", has_face_param=False),
        ])
        result = extract_template_labeled(ymmp)
        warnings = [c for c in result.conflicts if "no face parameter" in c]
        assert len(warnings) == 1

    def test_tachie_item_extraction(self):
        ymmp = _wrap_ymmp([
            _make_tachie_item("marisa", "smile", "eb03.png", "ey03.png", "mo03.png"),
        ])
        result = extract_template_labeled(ymmp)
        assert not [c for c in result.conflicts if c.startswith("Conflict:")]
        assert result.labeled_faces["marisa"]["smile"].eyebrow == "eb03.png"

    def test_tachie_face_item_extraction(self):
        """TachieFaceItem (表情アイテム) からの抽出。palette ymmp の主要パス。"""
        ymmp = _wrap_ymmp([
            _make_tachie_face_item("marisa", "serious", "eb01.png", "ey01.png", "mo01.png"),
            _make_tachie_face_item("marisa", "smile", "eb02.png", "ey02.png", "mo02.png"),
            _make_tachie_face_item("reimu", "serious", "eb03.png", "ey03.png", "mo03.png"),
        ])
        result = extract_template_labeled(ymmp)
        assert not [c for c in result.conflicts if c.startswith("Conflict:")]
        assert result.labeled_faces["marisa"]["serious"].eyebrow == "eb01.png"
        assert result.labeled_faces["marisa"]["smile"].eyebrow == "eb02.png"
        assert result.labeled_faces["reimu"]["serious"].eyebrow == "eb03.png"

    def test_bg_from_remark(self):
        ymmp = _wrap_ymmp([
            _make_image_item("studio_blue", "C:/bg/studio.png"),
        ])
        result = extract_template_labeled(ymmp)
        assert result.labeled_bgs["studio_blue"] == "C:/bg/studio.png"

    def test_bg_conflict(self):
        ymmp = _wrap_ymmp([
            _make_image_item("studio_blue", "C:/bg/studio1.png", frame=0),
            _make_image_item("studio_blue", "C:/bg/studio2.png", frame=100),
        ])
        result = extract_template_labeled(ymmp)
        errors = [c for c in result.conflicts if c.startswith("Conflict:")]
        assert len(errors) == 1

    def test_bg_same_label_same_path_idempotent(self):
        ymmp = _wrap_ymmp([
            _make_image_item("studio_blue", "C:/bg/studio.png", frame=0),
            _make_image_item("studio_blue", "C:/bg/studio.png", frame=100),
        ])
        result = extract_template_labeled(ymmp)
        assert not [c for c in result.conflicts if c.startswith("Conflict:")]
        assert len(result.labeled_bgs) == 1

    def test_empty_palette(self):
        ymmp = _wrap_ymmp([])
        result = extract_template_labeled(ymmp)
        assert len(result.labeled_faces) == 0
        assert len(result.labeled_bgs) == 0
        assert len(result.conflicts) == 0


class TestGenerateMaps:
    def test_generate_face_map_labeled(self):
        result = ExtractResult()
        result.labeled_faces = {
            "marisa": {
                "serious": FacePattern(eyebrow="eb01.png", eye="ey01.png", mouth="mo01.png"),
            },
            "reimu": {
                "smile": FacePattern(eyebrow="eb02.png", eye="ey02.png", mouth="mo02.png"),
            },
        }
        face_map = generate_face_map_labeled(result)
        assert face_map["marisa"]["serious"]["Eyebrow"] == "eb01.png"
        assert face_map["reimu"]["smile"]["Eyebrow"] == "eb02.png"

    def test_generate_bg_map_labeled(self):
        result = ExtractResult()
        result.labeled_bgs = {"studio_blue": "C:/bg/s.png"}
        bg_map = generate_bg_map_labeled(result)
        assert bg_map == {"studio_blue": "C:/bg/s.png"}


# ---------------------------------------------------------------------------
# _resolve_face_parts: flat vs character-scoped
# ---------------------------------------------------------------------------

class TestResolveFaceParts:
    def test_flat_map_no_character(self):
        flat = {"serious": {"Eyebrow": "a.png", "Eye": "b.png"}}
        result = _resolve_face_parts("serious", flat)
        assert result == {"Eyebrow": "a.png", "Eye": "b.png"}

    def test_flat_map_with_character_fallback(self):
        flat = {"serious": {"Eyebrow": "a.png", "Eye": "b.png"}}
        result = _resolve_face_parts("serious", flat, "marisa")
        assert result == {"Eyebrow": "a.png", "Eye": "b.png"}

    def test_char_scoped_map(self):
        scoped = {
            "marisa": {"serious": {"Eyebrow": "m_a.png"}},
            "reimu": {"serious": {"Eyebrow": "r_a.png"}},
        }
        assert _resolve_face_parts("serious", scoped, "marisa") == {"Eyebrow": "m_a.png"}
        assert _resolve_face_parts("serious", scoped, "reimu") == {"Eyebrow": "r_a.png"}

    def test_char_scoped_unknown_char(self):
        scoped = {"marisa": {"serious": {"Eyebrow": "a.png"}}}
        result = _resolve_face_parts("serious", scoped, "unknown")
        assert result is None

    def test_char_scoped_unknown_label(self):
        scoped = {"marisa": {"serious": {"Eyebrow": "a.png"}}}
        result = _resolve_face_parts("smile", scoped, "marisa")
        assert result is None

    def test_none_label(self):
        flat = {"serious": {"Eyebrow": "a.png"}}
        # face_label is a string, not None, in normal flow
        # but test robustness
        result = _resolve_face_parts("nonexistent", flat)
        assert result is None


# ---------------------------------------------------------------------------
# patch_ymmp: adapter 互換テスト
# ---------------------------------------------------------------------------

class TestPatchYmmpAdapter:
    def _make_production_ymmp(self):
        """2 キャラ、各 1 VoiceItem のミニマル ymmp."""
        return _wrap_ymmp([
            _make_voice_item("marisa", "", "default.png", "default.png", "default.png", frame=0),
            _make_voice_item("reimu", "", "default.png", "default.png", "default.png", frame=100),
        ])

    def _make_ir(self, faces: list[str]):
        return {
            "ir_version": "1.0",
            "video_id": "test",
            "macro": {
                "sections": [{
                    "section_id": "S1",
                    "start_index": 1,
                    "end_index": len(faces),
                    "default_bg": "bg1",
                    "default_face": "serious",
                }],
            },
            "utterances": [
                {"index": i + 1, "speaker": "sp", "text": "t", "section_id": "S1", "face": f}
                for i, f in enumerate(faces)
            ],
        }

    def test_flat_map_preserved(self):
        """既存のフラット face_map で patch_ymmp が動作する。"""
        ymmp = self._make_production_ymmp()
        ir = self._make_ir(["smile", "smile"])
        flat_map = {"smile": {"Eyebrow": "smile_eb.png", "Eye": "smile_ey.png", "Mouth": "smile_mo.png"}}

        result = patch_ymmp(ymmp, ir, flat_map, {})
        assert result.face_changes > 0
        # 両キャラとも同じ flat map で解決される
        items = ymmp["Timelines"][0]["Items"]
        vis = [i for i in items if "VoiceItem" in i.get("$type", "")]
        for vi in vis:
            assert vi["TachieFaceParameter"]["Eyebrow"] == "smile_eb.png"

    def test_char_scoped_map_different_parts(self):
        """character-scoped map でキャラごとに異なるパーツが適用される。"""
        ymmp = self._make_production_ymmp()
        ir = self._make_ir(["serious", "serious"])
        scoped_map = {
            "marisa": {"serious": {"Eyebrow": "m_eb.png", "Eye": "m_ey.png", "Mouth": "m_mo.png"}},
            "reimu": {"serious": {"Eyebrow": "r_eb.png", "Eye": "r_ey.png", "Mouth": "r_mo.png"}},
        }

        result = patch_ymmp(ymmp, ir, scoped_map, {})
        assert result.face_changes > 0

        items = ymmp["Timelines"][0]["Items"]
        vis = sorted(
            [i for i in items if "VoiceItem" in i.get("$type", "")],
            key=lambda x: x.get("Frame", 0),
        )
        assert vis[0]["TachieFaceParameter"]["Eyebrow"] == "m_eb.png"
        assert vis[1]["TachieFaceParameter"]["Eyebrow"] == "r_eb.png"

    def test_char_scoped_missing_char_warns(self):
        """character-scoped map にないキャラは warning。"""
        ymmp = self._make_production_ymmp()
        ir = self._make_ir(["serious", "serious"])
        scoped_map = {
            "marisa": {"serious": {"Eyebrow": "m_eb.png", "Eye": "m_ey.png", "Mouth": "m_mo.png"}},
            # reimu は map に無い
        }

        result = patch_ymmp(ymmp, ir, scoped_map, {})
        warnings = [w for w in result.warnings if "not found in face_map" in w]
        assert len(warnings) == 1  # reimu の serious


class TestTimelineInsertion:
    def _make_overlay_ymmp(self):
        return _wrap_ymmp([
            _make_voice_item("marisa", "", "default.png", "default.png", "default.png", frame=0),
            _make_voice_item("marisa", "", "default.png", "default.png", "default.png", frame=100),
        ])

    def _make_overlay_ir(self, *, overlay=None, se_label=None):
        utterance = {
            "index": 1,
            "speaker": "marisa",
            "text": "t1",
            "section_id": "S1",
            "face": "serious",
            "row_start": 1,
            "row_end": 1,
        }
        if overlay:
            utterance["overlay"] = overlay
        if se_label:
            utterance["se"] = se_label
        return {
            "ir_version": "1.0",
            "video_id": "timeline_test",
            "macro": {
                "sections": [{
                    "section_id": "S1",
                    "start_index": 1,
                    "end_index": 1,
                    "default_bg": "bg1",
                    "default_face": "serious",
                }],
            },
            "utterances": [utterance],
        }

    def test_overlay_inserts_image_item(self):
        ymmp = self._make_overlay_ymmp()
        ir = self._make_overlay_ir(overlay="arrow_red")

        result = patch_ymmp(
            ymmp,
            ir,
            {"serious": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"}},
            {},
            overlay_map={
                "arrow_red": {
                    "path": "C:/overlay/arrow_red.png",
                    "layer": 4,
                    "length": 12,
                    "x": 10,
                    "y": 20,
                    "zoom": 150,
                }
            },
        )

        assert result.overlay_changes == 1
        overlays = [
            item for item in ymmp["Timelines"][0]["Items"]
            if "ImageItem" in item.get("$type", "")
        ]
        assert len(overlays) == 1
        assert overlays[0]["FilePath"] == "C:/overlay/arrow_red.png"
        assert overlays[0]["Frame"] == 0
        assert overlays[0]["Length"] == 12
        assert overlays[0]["Layer"] == 4

    def test_overlay_missing_map_warns(self):
        ymmp = self._make_overlay_ymmp()
        ir = self._make_overlay_ir(overlay="arrow_red")

        result = patch_ymmp(
            ymmp,
            ir,
            {"serious": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"}},
            {},
        )

        warnings = [w for w in result.warnings if w.startswith("OVERLAY_MAP_MISS")]
        assert len(warnings) == 1
        assert result.overlay_changes == 0

    def test_se_inserts_audio_item(self):
        ymmp = self._make_overlay_ymmp()
        ir = self._make_overlay_ir(se_label="click")

        result = patch_ymmp(
            ymmp,
            ir,
            {"serious": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"}},
            {},
            se_map={
                "click": {
                    "path": "C:/se/click.wav",
                }
            },
        )

        assert result.se_plans == 1
        assert not any(
            w.startswith("SE_WRITE_ROUTE_UNSUPPORTED") for w in (result.warnings or [])
        )
        audios = [
            i for i in ymmp["Timelines"][0]["Items"]
            if "AudioItem" in i.get("$type", "")
        ]
        assert len(audios) == 1
        assert audios[0]["FilePath"] == "C:/se/click.wav"
        assert audios[0]["Frame"] == 0
        assert audios[0]["Length"] == 100

    def test_se_inserts_without_timeline_audio_template(self):
        """タイムラインに AudioItem が無くても骨格で挿入できる."""
        items = [
            _make_voice_item("marisa", "", "d.png", "d.png", "d.png", frame=0),
        ]
        ymmp = _wrap_ymmp(items)
        ir = {
            "ir_version": "1.0",
            "video_id": "se_only",
            "macro": {
                "sections": [{
                    "section_id": "S1",
                    "start_index": 1,
                    "end_index": 1,
                    "default_bg": "bg1",
                    "default_face": "serious",
                }],
            },
            "utterances": [{
                "index": 1,
                "speaker": "marisa",
                "text": "t",
                "section_id": "S1",
                "face": "serious",
                "se": "beep",
            }],
        }
        face_map = {"serious": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"}}
        result = patch_ymmp(
            ymmp,
            ir,
            face_map,
            {"bg1": "C:/bg.png"},
            se_map={"beep": {"path": "C:/se/beep.wav", "length": 30}},
        )
        assert result.se_plans == 1
        audios = [
            i for i in ymmp["Timelines"][0]["Items"]
            if "AudioItem" in i.get("$type", "")
        ]
        assert len(audios) == 1
        assert audios[0]["FilePath"] == "C:/se/beep.wav"
        assert audios[0]["Length"] == 30
        assert audios[0]["$type"] == (
            "YukkuriMovieMaker.Project.Items.AudioItem, YukkuriMovieMaker"
        )


# ---------------------------------------------------------------------------
# E2E: extract_template_labeled → generate → patch_ymmp
# ---------------------------------------------------------------------------

class TestSlotPatch:
    def _make_slot_ymmp(self, include_reimu_tachie: bool = True) -> dict:
        items = [
            _make_tachie_item("marisa", "", frame=0),
            _make_voice_item("marisa", "", "default.png", "default.png", "default.png", frame=0),
            _make_voice_item("reimu", "", "default.png", "default.png", "default.png", frame=100),
        ]
        if include_reimu_tachie:
            items.insert(1, _make_tachie_item("reimu", "", frame=0))
        return _wrap_ymmp(items)

    def _make_slot_ir(self, utterances: list[dict]) -> dict:
        return {
            "ir_version": "1.0",
            "video_id": "slot_test",
            "macro": {
                "sections": [{
                    "section_id": "S1",
                    "start_index": 1,
                    "end_index": len(utterances),
                    "default_bg": "bg1",
                    "default_face": "serious",
                }],
            },
            "utterances": utterances,
        }

    def _base_face_map(self) -> dict:
        return {
            "serious": {
                "Eyebrow": "serious_eb.png",
                "Eye": "serious_ey.png",
                "Mouth": "serious_mo.png",
            }
        }

    def _tachie_by_name(self, ymmp: dict) -> dict[str, dict]:
        items = ymmp["Timelines"][0]["Items"]
        return {
            item["CharacterName"]: item
            for item in items
            if "TachieItem" in item.get("$type", "")
        }

    def test_slot_patch_updates_tachie_positions(self):
        ymmp = self._make_slot_ymmp()
        ir = self._make_slot_ir([
            {"index": 1, "speaker": "marisa", "text": "t1", "section_id": "S1",
             "face": "serious", "slot": "left"},
            {"index": 2, "speaker": "reimu", "text": "t2", "section_id": "S1",
             "face": "serious", "slot": "right"},
        ])
        slot_map = {
            "left": {"x": -737, "y": 540, "zoom": 120},
            "right": {"x": 708, "y": 540, "zoom": 120},
        }

        result = patch_ymmp(ymmp, ir, self._base_face_map(), {}, slot_map=slot_map)

        tachie = self._tachie_by_name(ymmp)
        assert tachie["marisa"]["TachieItemParameter"]["X"] == -737
        assert tachie["marisa"]["TachieItemParameter"]["Y"] == 540
        assert tachie["marisa"]["TachieItemParameter"]["Zoom"] == 120
        assert tachie["reimu"]["TachieItemParameter"]["X"] == 708
        assert tachie["reimu"]["TachieItemParameter"]["Y"] == 540
        assert tachie["reimu"]["TachieItemParameter"]["Zoom"] == 120
        assert result.slot_changes >= 4
        assert not [w for w in result.warnings if w.startswith("SLOT_")]

    def test_slot_default_fallback_applies_when_ir_slot_missing(self):
        ymmp = self._make_slot_ymmp()
        ir = self._make_slot_ir([
            {"index": 1, "speaker": "marisa", "text": "t1", "section_id": "S1",
             "face": "serious"},
            {"index": 2, "speaker": "reimu", "text": "t2", "section_id": "S1",
             "face": "serious"},
        ])
        slot_map = {
            "left": {"x": -737, "y": 540, "zoom": 120},
            "right": {"x": 708, "y": 540, "zoom": 120},
        }
        defaults = {"marisa": "left", "reimu": "right"}

        result = patch_ymmp(
            ymmp,
            ir,
            self._base_face_map(),
            {},
            slot_map=slot_map,
            char_default_slots=defaults,
        )

        tachie = self._tachie_by_name(ymmp)
        assert tachie["marisa"]["TachieItemParameter"]["X"] == -737
        assert tachie["reimu"]["TachieItemParameter"]["X"] == 708
        assert result.slot_changes >= 4

    def test_slot_off_hides_tachie(self):
        ymmp = self._make_slot_ymmp(include_reimu_tachie=False)
        ir = self._make_slot_ir([
            {"index": 1, "speaker": "marisa", "text": "t1", "section_id": "S1",
             "face": "serious", "slot": "off"},
        ])

        result = patch_ymmp(
            ymmp,
            ir,
            self._base_face_map(),
            {},
            slot_map={"off": None},
        )

        tachie = self._tachie_by_name(ymmp)
        assert tachie["marisa"]["IsHidden"] is True
        assert result.slot_changes >= 1

    def test_slot_character_drift_warns_and_skips_patch(self):
        ymmp = self._make_slot_ymmp(include_reimu_tachie=False)
        ir = self._make_slot_ir([
            {"index": 1, "speaker": "marisa", "text": "t1", "section_id": "S1",
             "face": "serious", "slot": "left"},
            {"index": 2, "speaker": "marisa", "text": "t2", "section_id": "S1",
             "face": "serious", "slot": "right"},
        ])
        slot_map = {
            "left": {"x": -737, "y": 540, "zoom": 120},
            "right": {"x": 708, "y": 540, "zoom": 120},
        }

        result = patch_ymmp(ymmp, ir, self._base_face_map(), {}, slot_map=slot_map)

        tachie = self._tachie_by_name(ymmp)
        assert tachie["marisa"]["TachieItemParameter"]["X"] == 0.0
        warnings = [w for w in result.warnings if w.startswith("SLOT_CHARACTER_DRIFT")]
        assert len(warnings) == 1

    def test_slot_missing_tachie_warns(self):
        ymmp = self._make_slot_ymmp(include_reimu_tachie=False)
        ir = self._make_slot_ir([
            {"index": 1, "speaker": "marisa", "text": "t1", "section_id": "S1",
             "face": "serious", "slot": "left"},
            {"index": 2, "speaker": "reimu", "text": "t2", "section_id": "S1",
             "face": "serious", "slot": "right"},
        ])
        slot_map = {
            "left": {"x": -737, "y": 540, "zoom": 120},
            "right": {"x": 708, "y": 540, "zoom": 120},
        }

        result = patch_ymmp(ymmp, ir, self._base_face_map(), {}, slot_map=slot_map)

        warnings = [w for w in result.warnings if w.startswith("SLOT_NO_TACHIE_ITEM")]
        assert len(warnings) == 1


class TestE2ELabeledPipeline:
    def test_palette_to_patch(self):
        """palette ymmp → labeled face_map → patch_ymmp の E2E。"""
        # 1. palette ymmp: 各キャラの各表情を Remark で定義
        palette = _wrap_ymmp([
            _make_voice_item("marisa", "serious", "m_eb01.png", "m_ey01.png", "m_mo01.png"),
            _make_voice_item("marisa", "smile", "m_eb02.png", "m_ey02.png", "m_mo02.png"),
            _make_voice_item("reimu", "serious", "r_eb01.png", "r_ey01.png", "r_mo01.png"),
            _make_image_item("dark_board", "C:/bg/dark.png"),
        ])

        # 2. extract
        extract_result = extract_template_labeled(palette)
        assert not [c for c in extract_result.conflicts if c.startswith("Conflict:")]

        face_map = generate_face_map_labeled(extract_result)
        bg_map = generate_bg_map_labeled(extract_result)

        assert face_map["marisa"]["serious"]["Eyebrow"] == "m_eb01.png"
        assert face_map["marisa"]["smile"]["Eyebrow"] == "m_eb02.png"
        assert face_map["reimu"]["serious"]["Eyebrow"] == "r_eb01.png"
        assert bg_map["dark_board"] == "C:/bg/dark.png"

        # 3. production ymmp (パッチ対象)
        production = _wrap_ymmp([
            _make_voice_item("marisa", "", "default.png", "default.png", "default.png", frame=0),
            _make_voice_item("reimu", "", "default.png", "default.png", "default.png", frame=100),
        ])

        ir = {
            "ir_version": "1.0",
            "video_id": "test",
            "macro": {
                "sections": [{
                    "section_id": "S1",
                    "start_index": 1,
                    "end_index": 2,
                    "default_bg": "dark_board",
                    "default_face": "serious",
                }],
            },
            "utterances": [
                {"index": 1, "speaker": "sp1", "text": "t1", "section_id": "S1", "face": "smile"},
                {"index": 2, "speaker": "sp2", "text": "t2", "section_id": "S1", "face": "serious"},
            ],
        }

        # 4. patch
        patch_result = patch_ymmp(production, ir, face_map, bg_map)
        assert patch_result.face_changes > 0

        items = production["Timelines"][0]["Items"]
        vis = sorted(
            [i for i in items if "VoiceItem" in i.get("$type", "")],
            key=lambda x: x.get("Frame", 0),
        )
        # marisa gets smile
        assert vis[0]["TachieFaceParameter"]["Eyebrow"] == "m_eb02.png"
        # reimu gets serious
        assert vis[1]["TachieFaceParameter"]["Eyebrow"] == "r_eb01.png"


# ---------------------------------------------------------------------------
# row-range: IR utterance → 複数 VoiceItem 適用
# ---------------------------------------------------------------------------

def _make_row_range_ymmp(n_items: int = 6) -> dict:
    """n_items 個の VoiceItem を持つミニマル ymmp."""
    items = [
        _make_voice_item(
            "marisa", "", "default.png", "default.png", "default.png",
            frame=i * 100,
        )
        for i in range(n_items)
    ]
    return _wrap_ymmp(items)


def _make_row_range_ir(utterances: list[dict]) -> dict:
    return {
        "ir_version": "1.0",
        "video_id": "test_row_range",
        "macro": {
            "sections": [{
                "section_id": "S1",
                "start_index": 1,
                "end_index": len(utterances),
                "default_bg": "bg1",
                "default_face": "serious",
            }],
        },
        "utterances": utterances,
    }


class TestRowRangeFace:
    def test_basic_row_range(self):
        """1 utterance が複数 VoiceItem に適用される。"""
        ymmp = _make_row_range_ymmp(6)
        ir = _make_row_range_ir([
            {"index": 1, "speaker": "sp", "text": "t1", "section_id": "S1",
             "face": "smile", "row_start": 1, "row_end": 3},
            {"index": 2, "speaker": "sp", "text": "t2", "section_id": "S1",
             "face": "angry", "row_start": 4, "row_end": 6},
        ])
        face_map = {
            "smile": {"Eyebrow": "smile.png", "Eye": "s.png", "Mouth": "s.png"},
            "angry": {"Eyebrow": "angry.png", "Eye": "a.png", "Mouth": "a.png"},
        }

        result = patch_ymmp(ymmp, ir, face_map, {})
        vis = sorted(
            [i for i in ymmp["Timelines"][0]["Items"]
             if "VoiceItem" in i.get("$type", "")],
            key=lambda x: x.get("Frame", 0),
        )
        # VoiceItem 0-2 → smile
        for i in range(3):
            assert vis[i]["TachieFaceParameter"]["Eyebrow"] == "smile.png"
        # VoiceItem 3-5 → angry
        for i in range(3, 6):
            assert vis[i]["TachieFaceParameter"]["Eyebrow"] == "angry.png"
        assert result.face_changes > 0

    def test_row_range_with_char_scoped_map(self):
        """row-range + character-scoped face_map の組み合わせ。"""
        items = [
            _make_voice_item("marisa", "", "d.png", "d.png", "d.png", frame=0),
            _make_voice_item("marisa", "", "d.png", "d.png", "d.png", frame=100),
            _make_voice_item("reimu", "", "d.png", "d.png", "d.png", frame=200),
            _make_voice_item("reimu", "", "d.png", "d.png", "d.png", frame=300),
        ]
        ymmp = _wrap_ymmp(items)
        ir = _make_row_range_ir([
            {"index": 1, "speaker": "sp1", "text": "t1", "section_id": "S1",
             "face": "smile", "row_start": 1, "row_end": 2},
            {"index": 2, "speaker": "sp2", "text": "t2", "section_id": "S1",
             "face": "smile", "row_start": 3, "row_end": 4},
        ])
        scoped_map = {
            "marisa": {"smile": {"Eyebrow": "m_s.png", "Eye": "m.png", "Mouth": "m.png"}},
            "reimu": {"smile": {"Eyebrow": "r_s.png", "Eye": "r.png", "Mouth": "r.png"}},
        }

        patch_ymmp(ymmp, ir, scoped_map, {})
        vis = sorted(
            [i for i in ymmp["Timelines"][0]["Items"]
             if "VoiceItem" in i.get("$type", "")],
            key=lambda x: x.get("Frame", 0),
        )
        assert vis[0]["TachieFaceParameter"]["Eyebrow"] == "m_s.png"
        assert vis[1]["TachieFaceParameter"]["Eyebrow"] == "m_s.png"
        assert vis[2]["TachieFaceParameter"]["Eyebrow"] == "r_s.png"
        assert vis[3]["TachieFaceParameter"]["Eyebrow"] == "r_s.png"

    def test_row_range_exceeds_voice_items(self):
        """row_end が VoiceItem 数を超えても安全に動作する。"""
        ymmp = _make_row_range_ymmp(3)
        ir = _make_row_range_ir([
            {"index": 1, "speaker": "sp", "text": "t1", "section_id": "S1",
             "face": "smile", "row_start": 1, "row_end": 10},
        ])
        face_map = {"smile": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"}}

        result = patch_ymmp(ymmp, ir, face_map, {})
        vis = ymmp["Timelines"][0]["Items"]
        voice = [i for i in vis if "VoiceItem" in i.get("$type", "")]
        for vi in voice:
            assert vi["TachieFaceParameter"]["Eyebrow"] == "s.png"
        # 3 VoiceItem x 3 parts (Eyebrow/Eye/Mouth) = 9
        assert result.face_changes == 9

    def test_missing_row_start_warns(self):
        """row_start が一部欠落している utterance は warning。"""
        ymmp = _make_row_range_ymmp(4)
        ir = _make_row_range_ir([
            {"index": 1, "speaker": "sp", "text": "t1", "section_id": "S1",
             "face": "smile", "row_start": 1, "row_end": 2},
            {"index": 2, "speaker": "sp", "text": "t2", "section_id": "S1",
             "face": "angry", "row_start": 3},  # row_end 欠落
        ])
        face_map = {
            "smile": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"},
            "angry": {"Eyebrow": "a.png", "Eye": "a.png", "Mouth": "a.png"},
        }

        result = patch_ymmp(ymmp, ir, face_map, {})
        warnings = [w for w in result.warnings if "missing row_start/row_end" in w]
        assert len(warnings) == 1

    def test_invalid_row_range_warns(self):
        """row_start > row_end は warning。"""
        ymmp = _make_row_range_ymmp(4)
        ir = _make_row_range_ir([
            {"index": 1, "speaker": "sp", "text": "t1", "section_id": "S1",
             "face": "smile", "row_start": 3, "row_end": 1},
        ])
        face_map = {"smile": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"}}

        result = patch_ymmp(ymmp, ir, face_map, {})
        warnings = [w for w in result.warnings if "invalid row_start" in w]
        assert len(warnings) == 1
        assert result.face_changes == 0

    def test_positional_fallback_without_row_range(self):
        """row_start/row_end なしの既存 IR は位置ベースで動作する。"""
        ymmp = _make_row_range_ymmp(3)
        ir = _make_row_range_ir([
            {"index": 1, "speaker": "sp", "text": "t1", "section_id": "S1",
             "face": "smile"},
            {"index": 2, "speaker": "sp", "text": "t2", "section_id": "S1",
             "face": "angry"},
            {"index": 3, "speaker": "sp", "text": "t3", "section_id": "S1",
             "face": "smile"},
        ])
        face_map = {
            "smile": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"},
            "angry": {"Eyebrow": "a.png", "Eye": "a.png", "Mouth": "a.png"},
        }

        result = patch_ymmp(ymmp, ir, face_map, {})
        vis = sorted(
            [i for i in ymmp["Timelines"][0]["Items"]
             if "VoiceItem" in i.get("$type", "")],
            key=lambda x: x.get("Frame", 0),
        )
        assert vis[0]["TachieFaceParameter"]["Eyebrow"] == "s.png"
        assert vis[1]["TachieFaceParameter"]["Eyebrow"] == "a.png"
        assert vis[2]["TachieFaceParameter"]["Eyebrow"] == "s.png"


class TestRowRangeBg:
    def test_bg_section_uses_row_start_for_frame(self):
        """row-range モードで bg セクションの Frame が正しく計算される。"""
        ymmp = _make_row_range_ymmp(6)
        ir = {
            "ir_version": "1.0",
            "video_id": "test",
            "macro": {
                "sections": [
                    {"section_id": "S1", "start_index": 1, "end_index": 1,
                     "default_bg": "bg_a", "default_face": "serious"},
                    {"section_id": "S2", "start_index": 2, "end_index": 2,
                     "default_bg": "bg_b", "default_face": "serious"},
                ],
            },
            "utterances": [
                {"index": 1, "speaker": "sp", "text": "t1", "section_id": "S1",
                 "face": "serious", "row_start": 1, "row_end": 3},
                {"index": 2, "speaker": "sp", "text": "t2", "section_id": "S2",
                 "face": "serious", "row_start": 4, "row_end": 6},
            ],
        }
        bg_map = {"bg_a": "C:/a.png", "bg_b": "C:/b.png"}

        patch_ymmp(ymmp, ir, {}, bg_map)

        items = ymmp["Timelines"][0]["Items"]
        bgs = sorted(
            [i for i in items if "ImageItem" in i.get("$type", "")],
            key=lambda x: x.get("Frame", 0),
        )
        assert len(bgs) == 2
        # S1 starts at Frame 0 (first section)
        assert bgs[0]["Frame"] == 0
        assert bgs[0]["FilePath"] == "C:/a.png"
        # S2 starts at VoiceItem index 3 (row_start=4 → 0-based=3 → Frame=300)
        assert bgs[1]["Frame"] == 300
        assert bgs[1]["FilePath"] == "C:/b.png"

    def test_g15_micro_bg_splits_section_by_utterance(self):
        """同一セクション内で Micro bg が変わると Layer 0 を複数 ImageItem に分割する."""
        items = [
            _make_voice_item("sp", "", frame=0),
            _make_voice_item("sp", "", frame=100),
            _make_voice_item("sp", "", frame=200),
            _make_voice_item("sp", "", frame=300),
        ]
        ymmp = _wrap_ymmp(items)
        ir = {
            "ir_version": "1.0",
            "video_id": "t",
            "macro": {
                "sections": [{
                    "section_id": "S1",
                    "start_index": 1,
                    "end_index": 2,
                    "default_bg": "bg_a",
                    "default_face": "serious",
                }],
            },
            "utterances": [
                {"index": 1, "speaker": "sp", "text": "a", "section_id": "S1",
                 "face": "serious", "bg": "bg_a",
                 "row_start": 1, "row_end": 2},
                {"index": 2, "speaker": "sp", "text": "b", "section_id": "S1",
                 "face": "serious", "bg": "bg_b",
                 "row_start": 3, "row_end": 4},
            ],
        }
        bg_map = {"bg_a": "C:/a.png", "bg_b": "C:/b.png"}
        face_map = {
            "serious": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"},
        }
        patch_ymmp(ymmp, ir, face_map, bg_map)
        bgs = sorted(
            [i for i in ymmp["Timelines"][0]["Items"]
             if "ImageItem" in i.get("$type", "")],
            key=lambda x: x.get("Frame", 0),
        )
        assert len(bgs) == 2
        assert bgs[0]["Frame"] == 0
        assert bgs[0]["Length"] == 200
        assert bgs[0]["FilePath"] == "C:/a.png"
        assert bgs[1]["Frame"] == 200
        assert bgs[1]["FilePath"] == "C:/b.png"

    def test_g16_overlay_array_inserts_two_items(self):
        ymmp = _make_row_range_ymmp(2)
        ir = {
            "ir_version": "1.0",
            "video_id": "t",
            "macro": {"sections": []},
            "utterances": [
                {"index": 1, "speaker": "marisa", "text": "t", "section_id": "S1",
                 "face": "smile", "overlay": ["bubble", "box"],
                 "row_start": 1, "row_end": 2},
            ],
        }
        face_map = {
            "smile": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"},
        }
        overlay_map = {
            "bubble": {"path": "C:/b.png", "layer": 5, "anchor": "start"},
            "box": {"path": "C:/x.png", "layer": 6, "anchor": "start"},
        }
        result = patch_ymmp(ymmp, ir, face_map, {}, overlay_map=overlay_map)
        assert result.overlay_changes == 2
        layers = {
            i.get("Layer")
            for i in ymmp["Timelines"][0]["Items"]
            if "ImageItem" in i.get("$type", "") and i.get("FilePath") in
            ("C:/b.png", "C:/x.png")
        }
        assert layers == {5, 6}

    def test_g17_motion_only_writes_motion_and_transition(self):
        vi = _make_voice_item("marisa", "", frame=0)
        ti = _make_tachie_item("marisa", "")
        ti["VideoEffects"] = []
        ti["Length"] = 500
        ymmp = _wrap_ymmp([vi, ti])
        ir = {
            "ir_version": "1.0",
            "video_id": "t",
            "macro": {"sections": []},
            "utterances": [
                {"index": 1, "speaker": "marisa", "text": "t", "section_id": "S1",
                 "face": "smile", "motion": "bounce", "transition": "soft"},
            ],
        }
        face_map = {
            "smile": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"},
        }
        motion_map = {
            "bounce": {
                "video_effect": {
                    "$type": "YukkuriMovieMaker.Plugin.Effects.BounceEffect, YukkuriMovieMaker.Plugin.Effects",
                    "Name": "Bounce",
                },
            },
        }
        transition_map = {"soft": {"VoiceFadeIn": 0.3}}
        result = patch_ymmp(
            ymmp,
            ir,
            face_map,
            {},
            timeline_profile="motion_only",
            motion_map=motion_map,
            transition_map=transition_map,
        )
        assert result.motion_changes == 1
        assert result.transition_changes == 1
        assert vi["VoiceFadeIn"] == 0.3
        assert len(ti["VideoEffects"]) == 1


# ---------------------------------------------------------------------------
# idle_face: 待機中表情の TachieFaceItem 挿入
# ---------------------------------------------------------------------------

def _make_two_char_ymmp() -> dict:
    """2 キャラ交互の 4 VoiceItem ymmp."""
    items = [
        _make_voice_item("marisa", "", "d.png", "d.png", "d.png", frame=0),
        _make_voice_item("reimu", "", "d.png", "d.png", "d.png", frame=100),
        _make_voice_item("marisa", "", "d.png", "d.png", "d.png", frame=200),
        _make_voice_item("reimu", "", "d.png", "d.png", "d.png", frame=300),
    ]
    return _wrap_ymmp(items)


def _make_idle_face_ir(utterances: list[dict]) -> dict:
    return {
        "ir_version": "1.0",
        "video_id": "test_idle",
        "macro": {
            "sections": [{
                "section_id": "S1",
                "start_index": 1,
                "end_index": len(utterances),
                "default_bg": "bg1",
                "default_face": "serious",
            }],
        },
        "utterances": utterances,
    }


class TestIdleFace:
    def test_idle_face_inserts_tachie_face_items(self):
        """idle_face が TachieFaceItem として non-speaker に挿入される。"""
        ymmp = _make_two_char_ymmp()
        ir = _make_idle_face_ir([
            {"index": 1, "speaker": "marisa", "text": "t1", "section_id": "S1",
             "face": "smile", "idle_face": "serious", "row_start": 1, "row_end": 1},
            {"index": 2, "speaker": "reimu", "text": "t2", "section_id": "S1",
             "face": "thinking", "idle_face": "serious", "row_start": 2, "row_end": 2},
        ])
        scoped_map = {
            "marisa": {
                "smile": {"Eyebrow": "m_s.png", "Eye": "m.png", "Mouth": "m.png"},
                "serious": {"Eyebrow": "m_ser.png", "Eye": "m.png", "Mouth": "m.png"},
            },
            "reimu": {
                "thinking": {"Eyebrow": "r_t.png", "Eye": "r.png", "Mouth": "r.png"},
                "serious": {"Eyebrow": "r_ser.png", "Eye": "r.png", "Mouth": "r.png"},
            },
        }

        result = patch_ymmp(ymmp, ir, scoped_map, {})
        assert result.tachie_syncs == 2  # 2 utterances x 1 non-speaker each

        items = ymmp["Timelines"][0]["Items"]
        face_items = [i for i in items if "TachieFaceItem" in i.get("$type", "")]
        assert len(face_items) == 2

        # Sort by Frame
        face_items.sort(key=lambda x: x.get("Frame", 0))
        # utt 1 (marisa speaks): reimu gets idle_face=serious at Frame 0
        assert face_items[0]["CharacterName"] == "reimu"
        assert face_items[0]["Frame"] == 0
        assert face_items[0]["TachieFaceParameter"]["Eyebrow"] == "r_ser.png"
        # utt 2 (reimu speaks): marisa gets idle_face=serious at Frame 100
        assert face_items[1]["CharacterName"] == "marisa"
        assert face_items[1]["Frame"] == 100
        assert face_items[1]["TachieFaceParameter"]["Eyebrow"] == "m_ser.png"

    def test_no_idle_face_no_insertion(self):
        """idle_face がなければ TachieFaceItem は挿入されない。"""
        ymmp = _make_two_char_ymmp()
        ir = _make_idle_face_ir([
            {"index": 1, "speaker": "marisa", "text": "t1", "section_id": "S1",
             "face": "smile", "row_start": 1, "row_end": 1},
            {"index": 2, "speaker": "reimu", "text": "t2", "section_id": "S1",
             "face": "thinking", "row_start": 2, "row_end": 2},
        ])
        face_map = {
            "marisa": {"smile": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"}},
            "reimu": {"thinking": {"Eyebrow": "t.png", "Eye": "t.png", "Mouth": "t.png"}},
        }

        result = patch_ymmp(ymmp, ir, face_map, {})
        assert result.tachie_syncs == 0
        items = ymmp["Timelines"][0]["Items"]
        face_items = [i for i in items if "TachieFaceItem" in i.get("$type", "")]
        assert len(face_items) == 0

    def test_idle_face_carry_forward(self):
        """idle_face は carry-forward される。"""
        ymmp = _make_two_char_ymmp()
        ir = _make_idle_face_ir([
            {"index": 1, "speaker": "marisa", "text": "t1", "section_id": "S1",
             "face": "smile", "idle_face": "serious", "row_start": 1, "row_end": 1},
            # index 2 では idle_face 省略 → carry-forward で serious
            {"index": 2, "speaker": "reimu", "text": "t2", "section_id": "S1",
             "face": "thinking", "row_start": 2, "row_end": 2},
        ])
        scoped_map = {
            "marisa": {
                "smile": {"Eyebrow": "m_s.png", "Eye": "m.png", "Mouth": "m.png"},
                "serious": {"Eyebrow": "m_ser.png", "Eye": "m.png", "Mouth": "m.png"},
            },
            "reimu": {
                "thinking": {"Eyebrow": "r_t.png", "Eye": "r.png", "Mouth": "r.png"},
                "serious": {"Eyebrow": "r_ser.png", "Eye": "r.png", "Mouth": "r.png"},
            },
        }

        result = patch_ymmp(ymmp, ir, scoped_map, {})
        # utt 1: reimu gets idle, utt 2: marisa gets idle (carry-forward)
        assert result.tachie_syncs == 2

    def test_idle_face_positional_mode(self):
        """row_start/row_end なしの位置ベースでも idle_face が動作する。"""
        ymmp = _make_two_char_ymmp()
        ir = _make_idle_face_ir([
            {"index": 1, "speaker": "marisa", "text": "t1", "section_id": "S1",
             "face": "smile", "idle_face": "serious"},
            {"index": 2, "speaker": "reimu", "text": "t2", "section_id": "S1",
             "face": "thinking", "idle_face": "serious"},
            {"index": 3, "speaker": "marisa", "text": "t3", "section_id": "S1",
             "face": "smile"},
            {"index": 4, "speaker": "reimu", "text": "t4", "section_id": "S1",
             "face": "thinking"},
        ])
        flat_map = {
            "smile": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"},
            "thinking": {"Eyebrow": "t.png", "Eye": "t.png", "Mouth": "t.png"},
            "serious": {"Eyebrow": "ser.png", "Eye": "ser.png", "Mouth": "ser.png"},
        }

        result = patch_ymmp(ymmp, ir, flat_map, {})
        # utt 1-4 all have idle_face (carry-forward), 4 non-speaker inserts
        assert result.tachie_syncs == 4

    def test_idle_face_missing_label_warns(self):
        """idle_face のラベルが face_map にない場合は warning。"""
        ymmp = _make_two_char_ymmp()
        ir = _make_idle_face_ir([
            {"index": 1, "speaker": "marisa", "text": "t1", "section_id": "S1",
             "face": "smile", "idle_face": "nonexistent", "row_start": 1, "row_end": 1},
        ])
        face_map = {
            "marisa": {"smile": {"Eyebrow": "s.png", "Eye": "s.png", "Mouth": "s.png"}},
        }

        result = patch_ymmp(ymmp, ir, face_map, {})
        warnings = [w for w in result.warnings if "idle_face" in w]
        assert len(warnings) == 1
        assert result.tachie_syncs == 0
