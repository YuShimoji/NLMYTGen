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
_LINE_BREAK_AFTER = {
    "。": 0,
    "！": 0,
    "？": 0,
    "!": 0,
    "?": 0,
    "、": 1,
    ",": 1,
    "，": 1,
    "」": 2,
    "』": 2,
    "）": 2,
    ")": 2,
    "】": 2,
}
_CLAUSE_BREAK_AFTER = {
    "、": 0,
    ",": 0,
    "，": 0,
    ";": 1,
    ":": 1,
    "：": 1,
    "；": 1,
}
_CLAUSE_BREAK_BEFORE = (
    "しかし",
    "しかしながら",
    "ですが",
    "でも",
    "なので",
    "ため",
    "一方で",
    "ということ",
)
_AGGRESSIVE_BREAK_AFTER = {
    "」": 1,
    "』": 1,
    "）": 1,
    ")": 1,
    "】": 1,
    "は": 5,
    "が": 5,
    "を": 5,
    "に": 5,
    "へ": 5,
    "と": 5,
    "で": 5,
    "も": 5,
    "や": 5,
    "の": 5,
}
_AGGRESSIVE_BREAK_AFTER_MARKERS = (
    "という",
    "として",
    "により",
    "による",
    "について",
    "に対して",
    "していたら",
    "したら",
    "すると",
)


def display_width(text: str) -> int:
    """全角=2, 半角=1 の簡易表示幅を返す。

    East Asian Ambiguous ('A') を全角扱いする。
    YMM4 は Windows 日本語フォント環境で動作するため、
    Ambiguous 文字は全角幅で描画される。
    """
    w = 0
    for ch in text:
        if ch in ("\n", "\r"):
            continue
        w += 2 if unicodedata.east_asian_width(ch) in ("F", "W", "A") else 1
    return w


def estimate_display_lines(text: str, chars_per_line: int) -> int:
    """明示改行を尊重した推定表示行数を返す。"""
    if chars_per_line <= 0:
        return 0

    lines = 0
    for chunk in text.split("\n"):
        width = display_width(chunk)
        lines += max(1, -(-width // chars_per_line))
    return lines


def _find_clause_breaks(text: str) -> list[tuple[int, int]]:
    """一文の中で使える節分割候補を返す。"""
    candidates: dict[int, int] = {}

    for idx, ch in enumerate(text, start=1):
        penalty = _CLAUSE_BREAK_AFTER.get(ch)
        if penalty is not None:
            candidates[idx] = min(candidates.get(idx, penalty), penalty)

    for marker in _CLAUSE_BREAK_BEFORE:
        start = 0
        while True:
            idx = text.find(marker, start)
            if idx <= 0:
                break
            candidates[idx] = min(candidates.get(idx, 2), 2)
            start = idx + len(marker)

    return sorted(candidates.items())


def _find_aggressive_breaks(text: str) -> list[tuple[int, int]]:
    """通常候補が尽きた長文向けの、より強い分割候補を返す。"""
    candidates: dict[int, int] = {}

    for idx, ch in enumerate(text, start=1):
        penalty = _AGGRESSIVE_BREAK_AFTER.get(ch)
        if penalty is not None:
            candidates[idx] = min(candidates.get(idx, penalty), penalty)

    for marker in _AGGRESSIVE_BREAK_AFTER_MARKERS:
        start = 0
        while True:
            idx = text.find(marker, start)
            if idx < 0:
                break
            split_at = idx + len(marker)
            candidates[split_at] = min(candidates.get(split_at, 2), 2)
            start = idx + len(marker)

    return sorted(candidates.items())


def _split_single_long_sentence(
    text: str,
    *,
    max_length: int,
    measure,
) -> list[str]:
    """文末がない長文に対する節分割 fallback。"""
    if measure(text) <= max_length:
        return [text]

    remaining = text
    chunks: list[str] = []
    min_chunk = max(6, max_length // 4)

    while measure(remaining) > max_length:
        best: tuple[int, int] | None = None

        candidates = _find_clause_breaks(remaining)
        if not candidates:
            candidates = _find_aggressive_breaks(remaining)

        for split_at, penalty in candidates:
            left = remaining[:split_at]
            right = remaining[split_at:]
            if not right.strip():
                continue

            left_width = measure(left)
            right_width = measure(right)
            if left_width > max_length or left_width < min_chunk:
                continue

            short_tail_penalty = 50 if right_width < min_chunk else 0
            score = (max_length - left_width) + penalty * 3 + short_tail_penalty
            if best is None or score < best[0]:
                best = (score, split_at)

        if best is None:
            return [text]

        split_at = best[1]
        chunks.append(remaining[:split_at])
        remaining = remaining[split_at:]

    if remaining:
        chunks.append(remaining)
    return chunks


def _balance_two_lines(
    text: str,
    *,
    chars_per_line: int,
    measure,
) -> str:
    """2行字幕向けに、自然な候補位置へ改行を挿入する。"""
    if "\n" in text:
        return text

    total_width = measure(text)
    if total_width <= chars_per_line or total_width > chars_per_line * 2:
        return text

    min_width = max(4, chars_per_line // 5)
    best: tuple[int, int] | None = None

    for idx, ch in enumerate(text, start=1):
        penalty = _LINE_BREAK_AFTER.get(ch)
        if penalty is None:
            continue

        left = text[:idx]
        right = text[idx:]
        if not right.strip():
            continue

        left_width = measure(left)
        right_width = measure(right)
        if left_width > chars_per_line or right_width > chars_per_line:
            continue

        if min(left_width, right_width) < min_width:
            continue

        score = abs(left_width - right_width) + penalty * 4
        if best is None or score < best[0]:
            best = (score, idx)

    if best is None:
        return text

    split_at = best[1]
    return f"{text[:split_at]}\n{text[split_at:]}"


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
            for chunk in _split_single_long_sentence(
                row.text,
                max_length=max_length,
                measure=_measure,
            ):
                rows.append(YMM4CsvRow(speaker=row.speaker, text=chunk))
            continue

        expanded_sentences: list[str] = []
        for sentence in sentences:
            if _measure(sentence) > max_length:
                expanded_sentences.extend(
                    _split_single_long_sentence(
                        sentence,
                        max_length=max_length,
                        measure=_measure,
                    )
                )
            else:
                expanded_sentences.append(sentence)

        # 文を max_length 以内にグループ化
        buf = ""
        for sentence in expanded_sentences:
            if buf and _measure(buf) + _measure(sentence) > max_length:
                rows.append(YMM4CsvRow(speaker=row.speaker, text=buf))
                buf = sentence
            else:
                buf += sentence
        if buf:
            rows.append(YMM4CsvRow(speaker=row.speaker, text=buf))

    return YMM4CsvOutput(rows=tuple(rows))


def balance_subtitle_lines(
    output: YMM4CsvOutput,
    *,
    chars_per_line: int,
    max_lines: int = 2,
    use_display_width: bool = True,
) -> YMM4CsvOutput:
    """2行字幕向けに、見た目のバランスが良い改行を挿入する。"""
    if max_lines != 2 or chars_per_line <= 0:
        return output

    measure = display_width if use_display_width else len
    rows = [
        YMM4CsvRow(
            speaker=row.speaker,
            text=_balance_two_lines(
                row.text,
                chars_per_line=chars_per_line,
                measure=measure,
            ),
        )
        for row in output.rows
    ]
    return YMM4CsvOutput(rows=tuple(rows))
