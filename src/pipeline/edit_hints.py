"""YMM4 編集支援メタデータ生成。

build-csv --emit-meta で生成されるサイドカー JSON の中身を組み立てる。
YMM4 の CSV フォーマットには影響しない。
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.contracts.ymm4_csv_schema import YMM4CsvOutput

# 日本語 TTS の平均読み上げ速度 (文字/秒)。YMM4 デフォルト付近の推定値。
_CHARS_PER_SEC = 5.0

# セグメント区切り検出: 話題導入パターン
_TOPIC_INTRO_RE = re.compile(
    r"^(というわけで|ではここから|そこで|今回の|さて|では早速|"
    r"ところで|次に|続いて|それでは|最後に|まず|ここで|"
    r"じゃあ|えっと|そうそう|ちなみに|実は)"
)

# 表情ヒント用パターン
_QUESTION_RE = re.compile(r"[?？]")
_EXCLAIM_RE = re.compile(r"[!！]")
_LAUGH_RE = re.compile(r"(笑|ふふ|はは|あはは|わはは|ぷぷ)")
_SURPRISE_RE = re.compile(r"(え[!！ぇ]|うわ|おお|まさか|嘘|驚)")


def _estimate_duration(text: str) -> float:
    """発話テキストから推定読み上げ時間 (秒) を返す。"""
    return round(len(text) / _CHARS_PER_SEC, 1)


def _detect_expression(text: str) -> str:
    """テキストから表情ヒントを推定する。

    Returns: "question" | "excited" | "laugh" | "surprise" | "neutral"
    """
    if _LAUGH_RE.search(text):
        return "laugh"
    if _SURPRISE_RE.search(text):
        return "surprise"
    if _QUESTION_RE.search(text):
        return "question"
    if _EXCLAIM_RE.search(text):
        return "excited"
    return "neutral"


@dataclass
class RowHint:
    """1行分の編集ヒント。"""
    index: int
    speaker: str
    char_count: int
    estimated_duration_sec: float
    expression_hint: str
    is_segment_start: bool


@dataclass
class SegmentInfo:
    """セグメント (話題区切り) 情報。"""
    segment_id: int
    start_row: int
    end_row: int
    utterance_count: int
    estimated_duration_sec: float
    topic_preview: str  # セグメント冒頭のテキスト抜粋


@dataclass
class EditHints:
    """編集支援メタデータ全体。"""
    source_file: str
    generated_at: str
    total_utterances: int
    total_chars: int
    estimated_total_duration_sec: float
    speaker_stats: dict[str, dict]
    segments: list[SegmentInfo]
    rows: list[RowHint]

    def to_dict(self) -> dict:
        """JSON シリアライズ用の dict を返す。"""
        return {
            "source": self.source_file,
            "generated": self.generated_at,
            "summary": {
                "total_utterances": self.total_utterances,
                "total_chars": self.total_chars,
                "estimated_total_duration_sec": self.estimated_total_duration_sec,
                "speakers": self.speaker_stats,
            },
            "segments": [
                {
                    "segment_id": s.segment_id,
                    "start_row": s.start_row,
                    "end_row": s.end_row,
                    "utterance_count": s.utterance_count,
                    "estimated_duration_sec": s.estimated_duration_sec,
                    "topic_preview": s.topic_preview,
                }
                for s in self.segments
            ],
            "rows": [
                {
                    "index": r.index,
                    "speaker": r.speaker,
                    "char_count": r.char_count,
                    "estimated_duration_sec": r.estimated_duration_sec,
                    "expression_hint": r.expression_hint,
                    "is_segment_start": r.is_segment_start,
                }
                for r in self.rows
            ],
        }


def generate_edit_hints(
    output: YMM4CsvOutput,
    source_file: str = "",
) -> EditHints:
    """YMM4CsvOutput から編集支援メタデータを生成する。"""
    row_hints: list[RowHint] = []
    segment_starts: list[int] = [0]  # 最初の行は常にセグメント開始

    for i, row in enumerate(output.rows):
        duration = _estimate_duration(row.text)
        expression = _detect_expression(row.text)

        # セグメント区切り検出: 話題導入パターン + 先行行と話者が異なる
        is_seg_start = i == 0
        if i > 0 and _TOPIC_INTRO_RE.match(row.text):
            is_seg_start = True
            segment_starts.append(i)

        row_hints.append(RowHint(
            index=i,
            speaker=row.speaker,
            char_count=len(row.text),
            estimated_duration_sec=duration,
            expression_hint=expression,
            is_segment_start=is_seg_start,
        ))

    # セグメント情報を組み立て
    segments: list[SegmentInfo] = []
    for seg_idx, start in enumerate(segment_starts):
        end = segment_starts[seg_idx + 1] - 1 if seg_idx + 1 < len(segment_starts) else len(output.rows) - 1
        seg_rows = row_hints[start:end + 1]
        # トピックプレビュー: セグメント冒頭テキストの先頭40文字
        preview_text = output.rows[start].text
        topic_preview = preview_text[:40] + ("..." if len(preview_text) > 40 else "")
        segments.append(SegmentInfo(
            segment_id=seg_idx,
            start_row=start,
            end_row=end,
            utterance_count=len(seg_rows),
            estimated_duration_sec=round(sum(r.estimated_duration_sec for r in seg_rows), 1),
            topic_preview=topic_preview,
        ))

    # 話者統計
    speaker_counts = Counter(row.speaker for row in output.rows)
    speaker_chars = Counter()
    for row in output.rows:
        speaker_chars[row.speaker] += len(row.text)
    speaker_stats = {
        speaker: {
            "utterances": speaker_counts[speaker],
            "total_chars": speaker_chars[speaker],
            "estimated_duration_sec": round(speaker_chars[speaker] / _CHARS_PER_SEC, 1),
        }
        for speaker in sorted(speaker_counts)
    }

    total_chars = sum(len(row.text) for row in output.rows)

    return EditHints(
        source_file=source_file,
        generated_at=datetime.now(timezone.utc).isoformat(),
        total_utterances=len(output.rows),
        total_chars=total_chars,
        estimated_total_duration_sec=round(total_chars / _CHARS_PER_SEC, 1),
        speaker_stats=speaker_stats,
        segments=segments,
        rows=row_hints,
    )
