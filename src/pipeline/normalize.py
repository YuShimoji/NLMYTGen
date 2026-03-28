"""入力正規化: NotebookLM transcript → StructuredScript。

.csv と .txt の自動判定を行い、話者名+テキストのペアを抽出する。
"""

from __future__ import annotations

import csv
import io
import re
import warnings
from pathlib import Path

from src.contracts.notebooklm_input import load_transcript
from src.contracts.structured_script import StructuredScript, Utterance

_SUPPORTED_EXTENSIONS = {".csv", ".txt"}

# 話者名の最大長。コロン前の文字列がこれより長い場合は話者タグではなく通常テキストとみなす。
_MAX_SPEAKER_NAME_LEN = 30

# タイムスタンプ付き: [00:00] Speaker: text
_TIMESTAMPED_RE = re.compile(
    r"^\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s*([^:：]+?)\s*[:：]\s*(.+)$"
)

# シンプル: Speaker: text  or  Speaker：text
_SIMPLE_COLON_RE = re.compile(r"^([^:：]+?)\s*[:：]\s*(.+)$")


def normalize(path: Path, *, unlabeled: bool = False) -> StructuredScript:
    """入力ファイルをパースして StructuredScript を返す。

    .csv → CSV モード (2列: speaker, text)
    .txt → テキストモード (話者タグ付き対話)
    unlabeled=True → ラベルなしモード (行交互で Speaker_A/Speaker_B を割当)
    """
    transcript = load_transcript(path)
    suffix = path.suffix.lower()

    if suffix not in _SUPPORTED_EXTENSIONS:
        warnings.warn(
            f"Unsupported extension '{suffix}', treating as text: {path.name}",
            stacklevel=2,
        )

    if suffix == ".csv" and not unlabeled:
        return _parse_csv(transcript.text)
    elif unlabeled:
        return _parse_text_unlabeled(transcript.text)
    else:
        return _parse_text(transcript.text)


_HEADER_WORDS = {"speaker", "text", "name", "character", "dialogue", "line", "話者", "テキスト", "セリフ"}


def _looks_like_header(row: list[str]) -> bool:
    """CSV の 1行目がヘッダー行かどうかを推定する。"""
    return any(cell.strip().lower() in _HEADER_WORDS for cell in row[:2])


def _parse_csv(text: str) -> StructuredScript:
    """2列 CSV (speaker, text) をパースする。ヘッダー行は自動スキップ。"""
    utterances: list[Utterance] = []
    reader = csv.reader(io.StringIO(text))

    for i, row in enumerate(reader):
        if len(row) < 2:
            continue
        if i == 0 and _looks_like_header(row):
            continue
        speaker = row[0].strip()
        content = row[1].strip()
        if not speaker or not content:
            continue
        utterances.append(Utterance(speaker=speaker, text=content))

    if not utterances:
        raise ValueError("No valid utterances found in CSV input")
    return StructuredScript(utterances=tuple(utterances))


def _parse_text(text: str) -> StructuredScript:
    """話者タグ付きテキストをパースする。"""
    utterances: list[Utterance] = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # タイムスタンプ付きを先に試す
        m = _TIMESTAMPED_RE.match(line)
        if m:
            utterances.append(Utterance(speaker=m.group(1).strip(), text=m.group(2).strip()))
            continue

        # シンプルコロン形式
        m = _SIMPLE_COLON_RE.match(line)
        if m:
            speaker = m.group(1).strip()
            content = m.group(2).strip()
            if len(speaker) <= _MAX_SPEAKER_NAME_LEN and content:
                utterances.append(Utterance(speaker=speaker, text=content))
                continue

    if not utterances:
        raise ValueError("No valid utterances found in text input")
    return StructuredScript(utterances=tuple(utterances))


# ラベルなしモード: 短い行を前行に結合する閾値 (音声認識の分断アーティファクト緩和)
_SHORT_LINE_THRESHOLD = 3

# 句読点で終わる短行は完全な発話（相槌等）とみなし結合しない
_TERMINAL_PUNCTUATION = frozenset("。！？!?")


def _parse_text_unlabeled(text: str) -> StructuredScript:
    """ラベルなしテキストを行交互で 2 話者に割り当てる。

    短い行 (≤ _SHORT_LINE_THRESHOLD 文字) のうち、句読点で終わらないものは
    前の行に結合し、音声認識の分断アーティファクトを緩和する。
    句読点で終わる短行（"はい。" 等）は完全な発話として保持する。
    """
    # 非空行を収集
    raw_lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not raw_lines:
        raise ValueError("No valid utterances found in text input (unlabeled)")

    # 短い行を前行に結合（句読点で終わる完全な発話は保持）
    merged: list[str] = []
    for line in raw_lines:
        if merged and len(line) <= _SHORT_LINE_THRESHOLD and line[-1] not in _TERMINAL_PUNCTUATION:
            merged[-1] = f"{merged[-1]}{line}"
        else:
            merged.append(line)

    if not merged:
        raise ValueError("No valid utterances found in text input (unlabeled)")

    speakers = ("Speaker_A", "Speaker_B")
    utterances = [
        Utterance(speaker=speakers[i % 2], text=line)
        for i, line in enumerate(merged)
    ]
    return StructuredScript(utterances=tuple(utterances))
