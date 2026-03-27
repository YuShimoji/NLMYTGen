"""出力データ契約: YMM4 台本読込用 CSV。

YMM4 の「ツール → 台本読み込み」機能が直接読み込める 2列 CSV を定義する。
フォーマット: ヘッダーなし、UTF-8 (BOM 付き)、カンマ区切り。
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class YMM4CsvRow:
    """YMM4 台本の 1行。"""

    speaker: str
    text: str


@dataclass(frozen=True)
class YMM4CsvOutput:
    """YMM4 台本読込 CSV 全体。"""

    rows: tuple[YMM4CsvRow, ...]

    def write(self, path: Path) -> Path:
        """CSV ファイルを書き出す。UTF-8 BOM 付き, ヘッダーなし。"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            for row in self.rows:
                writer.writerow([row.speaker, row.text])
        return path
