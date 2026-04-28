"""字幕折り返し用の文字列幅計測器。"""

from __future__ import annotations

import json
import subprocess
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Protocol


class TextMeasurer(Protocol):
    """字幕レイアウト用の文字列幅計測インターフェース。"""

    def width(self, text: str) -> float:
        """文字列の横幅を返す。"""
        ...

    def widths(self, texts: list[str]) -> list[float]:
        """複数文字列の横幅をまとめて返す。"""
        ...


class EastAsianWidthMeasurer:
    """従来の全角=2 / 半角=1 近似計測。"""

    def width(self, text: str) -> float:
        total = 0.0
        for character in text:
            if character in ("\n", "\r"):
                continue
            total += 2.0 if unicodedata.east_asian_width(character) in ("F", "W", "A") else 1.0
        return total

    def widths(self, texts: list[str]) -> list[float]:
        return [self.width(text) for text in texts]


class WpfTextMeasurer:
    """Windows WPF の FormattedText による文字列幅計測。"""

    def __init__(
        self,
        exe_path: str | Path,
        font_family: str,
        font_size: float,
        letter_spacing: float = 0.0,
    ) -> None:
        self.exe_path = str(exe_path)
        self.font_family = font_family
        self.font_size = float(font_size)
        self.letter_spacing = float(letter_spacing)

    @lru_cache(maxsize=8192)
    def width(self, text: str) -> float:
        return self.widths([text])[0]

    def widths(self, texts: list[str]) -> list[float]:
        if not texts:
            return []
        payload = {
            "FontFamily": self.font_family,
            "FontSize": self.font_size,
            "LetterSpacing": self.letter_spacing,
            "Texts": texts,
        }
        result = subprocess.run(
            [self.exe_path],
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=True,
        )
        data = json.loads(result.stdout)
        widths = data.get("Widths")
        if not isinstance(widths, list) or len(widths) != len(texts):
            raise ValueError("Invalid WPF measurement response")
        return [float(width) for width in widths]
