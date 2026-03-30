"""CSV 組立: StructuredScript → YMM4CsvOutput。

話者マッピングの適用とテキスト内の話者プレフィックス除去を行う。
"""

from __future__ import annotations

import re
import unicodedata

from src.contracts.structured_script import StructuredScript
from src.contracts.ymm4_csv_schema import YMM4CsvOutput, YMM4CsvRow

# テキスト先頭の汎用話者プレフィックスを除去する正規表現。
_GENERIC_PREFIX_RE = re.compile(
    r"^(Host\d*|Speaker\d*|ナレーター\d*|進行役\d*|解説者\d*)\s*[:：]\s*",
    re.IGNORECASE,
)


def _strip_speaker_prefix(text: str, speaker: str = "") -> str:
    """テキスト先頭の話者プレフィックスを除去する。

    speaker が指定された場合、その話者名がテキスト先頭にあれば除去する。
    """
    # 動的: 話者名がテキスト先頭にある場合
    if speaker:
        for sep in (":", "："):
            prefix = f"{speaker}{sep}"
            if text.startswith(prefix):
                return text[len(prefix):].strip()
            prefix_sp = f"{speaker} {sep}"
            if text.startswith(prefix_sp):
                return text[len(prefix_sp):].strip()

    # 静的: 汎用パターン
    return _GENERIC_PREFIX_RE.sub("", text).strip()


def find_unmapped_speakers(
    script: StructuredScript,
    speaker_map: dict[str, str],
) -> set[str]:
    """speaker_map に含まれない話者名を返す。assembly 前に呼ぶこと。"""
    return {u.speaker for u in script.utterances} - set(speaker_map.keys())


def assemble(
    script: StructuredScript,
    speaker_map: dict[str, str] | None = None,
    merge_consecutive: bool = False,
) -> YMM4CsvOutput:
    """StructuredScript を YMM4CsvOutput に変換する。

    Args:
        script: 構造化済み台本
        speaker_map: 話者名マッピング (例: {"Host1": "れいむ", "Host2": "まりさ"})
        merge_consecutive: True なら同一話者の連続発話を結合する
    """
    rows: list[YMM4CsvRow] = []
    effective_map = speaker_map or {}

    for utt in script.utterances:
        speaker = effective_map.get(utt.speaker, utt.speaker)
        text = _strip_speaker_prefix(utt.text, speaker=utt.speaker)

        if merge_consecutive and rows and rows[-1].speaker == speaker:
            prev = rows[-1].text
            # 前のテキストが句読点等で終わっていなければ句点を補う
            sep = "" if prev.endswith(("。", "、", ".", ",", "!", "?", "！", "？", "\n")) else "。"
            merged_text = f"{prev}{sep}{text}"
            rows[-1] = YMM4CsvRow(speaker=speaker, text=merged_text)
        else:
            rows.append(YMM4CsvRow(speaker=speaker, text=text))

    return YMM4CsvOutput(rows=tuple(rows))


# 文末区切り文字
_SENTENCE_ENDS = re.compile(r"(?<=[。！？!?])")


def display_width(text: str) -> int:
    """全角=2, 半角=1 の簡易表示幅を返す。

    East Asian Ambiguous ('A') を全角扱いする。
    YMM4 は Windows 日本語フォント環境で動作するため、
    Ambiguous 文字は全角幅で描画される。
    """
    w = 0
    for ch in text:
        w += 2 if unicodedata.east_asian_width(ch) in ("F", "W", "A") else 1
    return w


def split_long_utterances(
    output: YMM4CsvOutput,
    max_length: int,
    *,
    use_display_width: bool = False,
) -> YMM4CsvOutput:
    """長い発話を句点で分割する。

    max_length を超える発話を文末（。！？!?）で分割し、
    同じ話者の複数行に展開する。
    単一文が max_length を超える場合はそのまま保持する。

    Args:
        output: 分割対象の CSV 出力
        max_length: 分割閾値 (文字数または表示幅)
        use_display_width: True なら全角=2, 半角=1 の表示幅で判定
    """
    _measure = display_width if use_display_width else len
    rows: list[YMM4CsvRow] = []

    for row in output.rows:
        if _measure(row.text) <= max_length:
            rows.append(row)
            continue

        # 文末で分割
        sentences = [s for s in _SENTENCE_ENDS.split(row.text) if s]
        if len(sentences) <= 1:
            rows.append(row)
            continue

        # 文を max_length 以内にグループ化
        buf = ""
        for sentence in sentences:
            if buf and _measure(buf) + _measure(sentence) > max_length:
                rows.append(YMM4CsvRow(speaker=row.speaker, text=buf))
                buf = sentence
            else:
                buf += sentence
        if buf:
            rows.append(YMM4CsvRow(speaker=row.speaker, text=buf))

    return YMM4CsvOutput(rows=tuple(rows))
