"""入力正規化: NotebookLM transcript → StructuredScript。

.csv と .txt の自動判定を行い、話者名+テキストのペアを抽出する。
"""

from __future__ import annotations

import csv
import io
import re
from pathlib import Path

from src.contracts.notebooklm_input import load_transcript
from src.contracts.structured_script import StructuredScript, Utterance

# タイムスタンプ付き: [00:00] Speaker: text
_TIMESTAMPED_RE = re.compile(
    r"^\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s*([^:：]+?)\s*[:：]\s*(.+)$"
)

# シンプル: Speaker: text  or  Speaker：text
_SIMPLE_COLON_RE = re.compile(r"^([^:：]+?)\s*[:：]\s*(.+)$")


def normalize(path: Path) -> StructuredScript:
    """入力ファイルをパースして StructuredScript を返す。

    .csv → CSV モード (2列: speaker, text)
    .txt → テキストモード (話者タグ付き対話)
    """
    transcript = load_transcript(path)

    if path.suffix.lower() == ".csv":
        return _parse_csv(transcript.text)
    else:
        return _parse_text(transcript.text)


def _parse_csv(text: str) -> StructuredScript:
    """2列 CSV (speaker, text) をパースする。"""
    utterances: list[Utterance] = []
    reader = csv.reader(io.StringIO(text))

    for row in reader:
        if len(row) < 2:
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
            # 話者名が長すぎる場合はパース失敗とみなす (非対話行)
            if len(speaker) <= 30 and content:
                utterances.append(Utterance(speaker=speaker, text=content))
                continue

    if not utterances:
        raise ValueError("No valid utterances found in text input")
    return StructuredScript(utterances=tuple(utterances))
