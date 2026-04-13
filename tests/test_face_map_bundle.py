"""G-19: face_map bundle (multi-body) tests."""
import json
import pytest
from pathlib import Path

from src.pipeline.ymmp_patch import (
    _select_face_map_for_body,
    _resolve_carry_forward,
    patch_ymmp,
    PatchResult,
)
from src.cli.main import _load_face_map_bundle


# --- Fixtures ---

FACE_MAP_BODY_A = {
    "ゆっくり魔理沙黄縁": {
        "neutral": {"Eyebrow": "bodyA/marisa/eyebrow.png", "Body": "bodyA/marisa/body.png"},
        "smile": {"Eyebrow": "bodyA/marisa/eyebrow_smile.png", "Body": "bodyA/marisa/body.png"},
    }
}

FACE_MAP_BODY_B = {
    "ゆっくり魔理沙黄縁": {
        "neutral": {"Eyebrow": "bodyB/marisa/eyebrow.png", "Body": "bodyB/marisa/body.png"},
        "smile": {"Eyebrow": "bodyB/marisa/eyebrow_smile.png", "Body": "bodyB/marisa/body.png"},
    }
}

FACE_MAP_FLAT = {
    "neutral": {"Eyebrow": "flat/eyebrow.png", "Body": "flat/body.png"},
}


# --- _select_face_map_for_body tests ---

class TestSelectFaceMapForBody:
    def test_no_bundle_returns_flat(self):
        result = _select_face_map_for_body(None, FACE_MAP_FLAT, "bodyA", None, None)
        assert result is FACE_MAP_FLAT

    def test_explicit_body_id(self):
        bundle = {"bodyA": FACE_MAP_BODY_A, "bodyB": FACE_MAP_BODY_B}
        result = _select_face_map_for_body(bundle, FACE_MAP_FLAT, "bodyB", None, None)
        assert result is FACE_MAP_BODY_B

    def test_character_default_body(self):
        bundle = {"bodyA": FACE_MAP_BODY_A, "bodyB": FACE_MAP_BODY_B}
        char_defaults = {"ゆっくり魔理沙黄縁": "bodyA"}
        result = _select_face_map_for_body(
            bundle, FACE_MAP_FLAT, None, char_defaults, "ゆっくり魔理沙黄縁"
        )
        assert result is FACE_MAP_BODY_A

    def test_default_key_fallback(self):
        bundle = {"default": FACE_MAP_BODY_A, "bodyB": FACE_MAP_BODY_B}
        result = _select_face_map_for_body(bundle, FACE_MAP_FLAT, None, None, None)
        assert result is FACE_MAP_BODY_A

    def test_all_miss_returns_flat(self):
        bundle = {"bodyX": FACE_MAP_BODY_A}
        result = _select_face_map_for_body(bundle, FACE_MAP_FLAT, "unknown", None, None)
        assert result is FACE_MAP_FLAT

    def test_body_id_priority_over_char_default(self):
        bundle = {"bodyA": FACE_MAP_BODY_A, "bodyB": FACE_MAP_BODY_B}
        char_defaults = {"ゆっくり魔理沙黄縁": "bodyA"}
        result = _select_face_map_for_body(
            bundle, FACE_MAP_FLAT, "bodyB", char_defaults, "ゆっくり魔理沙黄縁"
        )
        assert result is FACE_MAP_BODY_B


# --- carry-forward tests ---

class TestBodyIdCarryForward:
    def test_body_id_carries_forward(self):
        ir_data = {
            "utterances": [
                {"index": 1, "speaker": "まりさ", "text": "a", "section_id": "S1", "body_id": "haitatsuin"},
                {"index": 2, "speaker": "まりさ", "text": "b", "section_id": "S1"},
                {"index": 3, "speaker": "まりさ", "text": "c", "section_id": "S1", "body_id": "default"},
            ],
            "macro": {"sections": [{"section_id": "S1", "topic": "t"}]},
        }
        resolved = _resolve_carry_forward(ir_data)
        assert resolved[0]["body_id"] == "haitatsuin"
        assert resolved[1]["body_id"] == "haitatsuin"  # carried forward
        assert resolved[2]["body_id"] == "default"

    def test_body_id_section_reset(self):
        ir_data = {
            "utterances": [
                {"index": 1, "speaker": "まりさ", "text": "a", "section_id": "S1", "body_id": "haitatsuin"},
                {"index": 2, "speaker": "まりさ", "text": "b", "section_id": "S2"},
            ],
            "macro": {"sections": [
                {"section_id": "S1", "topic": "t1"},
                {"section_id": "S2", "topic": "t2", "default_body_id": "default"},
            ]},
        }
        resolved = _resolve_carry_forward(ir_data)
        assert resolved[0]["body_id"] == "haitatsuin"
        assert resolved[1]["body_id"] == "default"  # reset to section default


# --- _load_face_map_bundle tests ---

class TestLoadFaceMapBundle:
    def test_resolves_relative_paths(self, tmp_path):
        body_a = {"char": {"smile": {"Eye": "a.png"}}}
        body_b = {"char": {"smile": {"Eye": "b.png"}}}
        (tmp_path / "a.json").write_text(json.dumps(body_a), encoding="utf-8")
        (tmp_path / "b.json").write_text(json.dumps(body_b), encoding="utf-8")

        registry = {
            "bodies": {
                "bodyA": {"face_map": "a.json"},
                "bodyB": {"face_map": "b.json"},
            },
            "characters": {"char": {"default_body": "bodyA"}},
        }
        reg_path = tmp_path / "registry.json"
        reg_path.write_text(json.dumps(registry), encoding="utf-8")

        body_maps, char_defaults = _load_face_map_bundle(reg_path)
        assert set(body_maps.keys()) == {"bodyA", "bodyB"}
        assert body_maps["bodyA"] == body_a
        assert body_maps["bodyB"] == body_b
        assert char_defaults == {"char": "bodyA"}

    def test_missing_file_raises(self, tmp_path):
        registry = {
            "bodies": {"bodyA": {"face_map": "nonexistent.json"}},
            "characters": {},
        }
        reg_path = tmp_path / "registry.json"
        reg_path.write_text(json.dumps(registry), encoding="utf-8")

        with pytest.raises(FileNotFoundError, match="nonexistent.json"):
            _load_face_map_bundle(reg_path)


# --- Integration: patch_ymmp with bundle ---

class TestPatchWithBundle:
    def _make_voice_item(self, char_name: str, frame: int = 0) -> dict:
        return {
            "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
            "CharacterName": char_name,
            "Frame": frame,
            "Length": 100,
            "TachieFaceParameter": {
                "Eyebrow": "default.png",
                "Eye": "default.png",
                "Mouth": "default.png",
                "Body": "default.png",
            },
        }

    def _make_ymmp(self, voice_items: list[dict]) -> dict:
        return {
            "Timeline": {
                "Items": voice_items,
            }
        }

    def test_different_bodies_applied(self):
        vi1 = self._make_voice_item("ゆっくり魔理沙黄縁", 0)
        vi2 = self._make_voice_item("ゆっくり魔理沙黄縁", 100)
        ymmp = self._make_ymmp([vi1, vi2])

        ir_data = {
            "utterances": [
                {"index": 1, "speaker": "ゆっくり魔理沙黄縁", "text": "a",
                 "section_id": "S1", "face": "neutral", "body_id": "bodyA"},
                {"index": 2, "speaker": "ゆっくり魔理沙黄縁", "text": "b",
                 "section_id": "S1", "face": "neutral", "body_id": "bodyB"},
            ],
            "macro": {"sections": [{"section_id": "S1", "topic": "t"}]},
        }

        bundle = {"bodyA": FACE_MAP_BODY_A, "bodyB": FACE_MAP_BODY_B}
        char_defaults = {"ゆっくり魔理沙黄縁": "bodyA"}

        result = patch_ymmp(
            ymmp, ir_data, {}, {},
            face_map_bundle=bundle,
            char_default_bodies=char_defaults,
        )

        assert result.face_changes >= 2  # at least 2 VoiceItems touched (count is per-part)
        # VoiceItem 1 should have bodyA paths
        assert vi1["TachieFaceParameter"]["Body"] == "bodyA/marisa/body.png"
        assert vi1["TachieFaceParameter"]["Eyebrow"] == "bodyA/marisa/eyebrow.png"
        # VoiceItem 2 should have bodyB paths
        assert vi2["TachieFaceParameter"]["Body"] == "bodyB/marisa/body.png"
        assert vi2["TachieFaceParameter"]["Eyebrow"] == "bodyB/marisa/eyebrow.png"

    def test_no_bundle_backward_compat(self):
        vi1 = self._make_voice_item("ゆっくり魔理沙黄縁", 0)
        ymmp = self._make_ymmp([vi1])

        ir_data = {
            "utterances": [
                {"index": 1, "speaker": "ゆっくり魔理沙黄縁", "text": "a",
                 "section_id": "S1", "face": "neutral"},
            ],
            "macro": {"sections": [{"section_id": "S1", "topic": "t"}]},
        }

        result = patch_ymmp(ymmp, ir_data, FACE_MAP_BODY_A, {})
        assert result.face_changes >= 1  # per-part count
        assert vi1["TachieFaceParameter"]["Body"] == "bodyA/marisa/body.png"
