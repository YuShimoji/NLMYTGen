"""ymmp からテンプレート資産 (face_map / bg_map) を自動抽出する.

既存の完成品 ymmp を読み込み、使われている表情パーツと背景の
ユニークな組み合わせを抽出して、face_map / bg_map の雛形を生成する。

Usage (via CLI):
    python -m src.cli.main extract-template project.ymmp -o template_dir/
"""

from __future__ import annotations

import json
import os
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path

from src.pipeline.ymmp_patch import _get_timeline_items, _item_type


@dataclass
class FacePattern:
    """ユニークな表情パーツの組み合わせ."""

    eyebrow: str = ""
    eye: str = ""
    mouth: str = ""
    hair: str = ""
    body: str = ""
    complexion: str = ""

    @property
    def key(self) -> tuple[str, ...]:
        return (self.eyebrow, self.eye, self.mouth, self.hair, self.body)

    @property
    def short_label(self) -> str:
        """ファイル名からパーツ番号を抽出して簡潔なラベルを生成."""
        parts = []
        for name, path in [
            ("eb", self.eyebrow),
            ("ey", self.eye),
            ("mo", self.mouth),
        ]:
            if path:
                basename = os.path.splitext(os.path.basename(path))[0]
                parts.append(f"{name}{basename}")
        return "_".join(parts) if parts else "unknown"

    def to_dict(self) -> dict[str, str]:
        result: dict[str, str] = {}
        if self.eyebrow:
            result["Eyebrow"] = self.eyebrow
        if self.eye:
            result["Eye"] = self.eye
        if self.mouth:
            result["Mouth"] = self.mouth
        if self.hair:
            result["Hair"] = self.hair
        if self.body:
            result["Body"] = self.body
        if self.complexion:
            result["Complexion"] = self.complexion
        return result


@dataclass
class ExtractResult:
    """抽出結果."""

    face_patterns: list[FacePattern] = field(default_factory=list)
    bg_paths: list[str] = field(default_factory=list)
    characters: list[str] = field(default_factory=list)
    voice_item_count: int = 0
    bg_item_count: int = 0


def extract_template(ymmp_data: dict) -> ExtractResult:
    """ymmp から表情パーツと背景のユニークパターンを抽出する."""
    items = _get_timeline_items(ymmp_data)
    result = ExtractResult()

    # Characters
    chars = ymmp_data.get("Characters", [])
    result.characters = [c.get("Name", "?") for c in chars]

    # face パターン収集 (VoiceItem + TachieItem)
    seen_faces: dict[tuple, FacePattern] = OrderedDict()

    for item in items:
        itype = _item_type(item)

        if itype == "VoiceItem":
            result.voice_item_count += 1
            fp = item.get("TachieFaceParameter")
            if fp:
                pattern = FacePattern(
                    eyebrow=fp.get("Eyebrow", ""),
                    eye=fp.get("Eye", ""),
                    mouth=fp.get("Mouth", ""),
                    hair=fp.get("Hair", ""),
                    body=fp.get("Body", ""),
                    complexion=fp.get("Complexion") or "",
                )
                if pattern.key not in seen_faces:
                    seen_faces[pattern.key] = pattern

        elif itype == "TachieItem":
            param = item.get("TachieItemParameter", {})
            if param:
                pattern = FacePattern(
                    eyebrow=param.get("Eyebrow", ""),
                    eye=param.get("Eye", ""),
                    mouth=param.get("Mouth", ""),
                    hair=param.get("Hair", ""),
                    body=param.get("Body", ""),
                    complexion=param.get("Complexion") or "",
                )
                if pattern.key not in seen_faces:
                    seen_faces[pattern.key] = pattern

        elif itype in ("ImageItem", "VideoItem"):
            fp = item.get("FilePath", "")
            if fp and item.get("Layer", -1) == 0:
                result.bg_item_count += 1
                if fp not in result.bg_paths:
                    result.bg_paths.append(fp)

    result.face_patterns = list(seen_faces.values())
    return result


def generate_face_map(patterns: list[FacePattern]) -> dict[str, dict[str, str]]:
    """抽出した face パターンから face_map の雛形を生成.

    キーは自動生成ラベル (face_01, face_02, ...)。
    ユーザーが後から IR ラベル (serious, smile 等) にリネームする。
    """
    face_map: dict[str, dict[str, str]] = {}
    for i, pattern in enumerate(patterns, 1):
        label = f"face_{i:02d}_{pattern.short_label}"
        face_map[label] = pattern.to_dict()
    return face_map


def generate_bg_map(bg_paths: list[str]) -> dict[str, str]:
    """抽出した背景パスから bg_map の雛形を生成.

    キーは自動生成ラベル (bg_01, bg_02, ...)。
    ユーザーが後から IR ラベル (studio_blue, dark_board 等) にリネームする。
    """
    bg_map: dict[str, str] = {}
    for i, path in enumerate(bg_paths, 1):
        basename = os.path.splitext(os.path.basename(path))[0]
        # 長いハッシュ名は短縮
        if len(basename) > 20:
            basename = basename[:15]
        label = f"bg_{i:02d}_{basename}"
        bg_map[label] = path
    return bg_map
