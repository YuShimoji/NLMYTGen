"""IR utterance と CSV 行の対応付け (row_start / row_end 自動生成).

Greedy Forward Match で IR の意味単位を CSV 行範囲にマッピングする。
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field


@dataclass
class AnnotateResult:
    """annotate_row_range の結果."""

    matched: int = 0
    unmatched_utterances: list[int] = field(default_factory=list)
    uncovered_rows: list[int] = field(default_factory=list)
    overlap_detected: bool = False
    warnings: list[str] = field(default_factory=list)


def _norm_strict(s: str) -> str:
    """NFKC 正規化 + 全空白除去."""
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))


_PUNCT_RE = re.compile(r"[、。，．,.!?！？…・\-ー～〜「」『』（）()\[\]【】]")


def _norm_loose(s: str) -> str:
    """strict + 句読点・記号除去."""
    return _PUNCT_RE.sub("", _norm_strict(s))


def _match_level(ir_norm: str, concat_norm: str, level: str) -> bool:
    """指定レベルで一致するか判定する."""
    if level == "strict":
        return ir_norm == concat_norm
    if level == "loose":
        return ir_norm == concat_norm
    if not concat_norm or not ir_norm:
        return False
    # partial-forward: concat が ir に含まれる (CSV が IR の部分)
    if len(concat_norm) >= len(ir_norm) * 0.8 and concat_norm in ir_norm:
        return True
    # partial-reverse: ir が concat に含まれる (IR が CSV の部分)
    # IR が短すぎる場合の誤マッチ防止: IR が 10 文字以上 かつ concat の 80% 以上
    if (
        len(ir_norm) >= 10
        and len(ir_norm) >= len(concat_norm) * 0.8
        and ir_norm in concat_norm
    ):
        return True
    return False


def annotate_row_range(
    ir_data: dict,
    csv_rows: list[list[str]],
    *,
    force: bool = False,
    keep_existing: bool = False,
) -> AnnotateResult:
    """IR utterances に row_start/row_end を自動付与する.

    Parameters
    ----------
    ir_data : dict
        load_ir() 後の IR データ (in-place で変更される)
    csv_rows : list[list[str]]
        CSV の各行 [speaker, text]
    force : bool
        既存 row_start/row_end を上書きする
    keep_existing : bool
        既存 row_start/row_end をスキップする

    Returns
    -------
    AnnotateResult
    """
    result = AnnotateResult()
    utterances = ir_data.get("utterances", [])

    # 既存 range チェック
    if not force and not keep_existing:
        existing = [
            u for u in utterances
            if u.get("row_start") is not None or u.get("row_end") is not None
        ]
        if existing:
            for u in existing:
                result.warnings.append(
                    f"utterance index={u.get('index', '?')} has existing"
                    f" row_start/row_end. Use --force to overwrite"
                    f" or --keep-existing to skip."
                )
            return result

    # CSV テキストの正規化 (事前計算)
    csv_texts_strict = [_norm_strict(r[1]) if len(r) >= 2 else "" for r in csv_rows]
    csv_texts_loose = [_norm_loose(r[1]) if len(r) >= 2 else "" for r in csv_rows]
    csv_speakers = [r[0].strip() if r else "" for r in csv_rows]

    csv_pos = 0
    covered_rows: set[int] = set()

    for utt in utterances:
        utt_idx = utt.get("index", 0)

        # keep_existing: 既存があればスキップ
        if keep_existing and utt.get("row_start") is not None:
            # 既存 range をカバー済みとして記録
            rs = utt["row_start"]
            re_ = utt.get("row_end", rs)
            for r in range(rs, re_ + 1):
                covered_rows.add(r)
            csv_pos = max(csv_pos, re_)
            result.matched += 1
            continue

        ir_text = utt.get("text", "")
        if not ir_text:
            result.unmatched_utterances.append(utt_idx)
            result.warnings.append(
                f"utterance index={utt_idx} has empty text"
            )
            continue

        ir_strict = _norm_strict(ir_text)
        ir_loose = _norm_loose(ir_text)
        ir_speaker = utt.get("speaker", "")

        found = False
        best_partial_end = -1
        # 探索上限: IR テキスト長の 2 倍の行数、または残り行数
        max_rows = min(len(csv_rows), csv_pos + max(len(ir_strict) // 5, 10))

        for end in range(csv_pos, max_rows):
            concat_strict = "".join(csv_texts_strict[csv_pos : end + 1])
            concat_loose = "".join(csv_texts_loose[csv_pos : end + 1])

            # strict / loose 完全一致 → 即採用
            if (
                _match_level(ir_strict, concat_strict, "strict")
                or _match_level(ir_loose, concat_loose, "loose")
            ):
                best_partial_end = -1  # 完全一致なので partial 不要
                found = True
                row_start = csv_pos + 1
                row_end = end + 1
                break

            # partial: 最長一致を記録 (即採用しない)
            if _match_level(ir_loose, concat_loose, "partial"):
                best_partial_end = end

            # concat が ir より長くなったら打ち切り
            if len(concat_strict) > len(ir_strict) * 1.5:
                break

        # strict/loose が見つからなければ partial の最長を採用
        if not found and best_partial_end >= 0:
            found = True
            row_start = csv_pos + 1
            row_end = best_partial_end + 1

        if found:
            utt["row_start"] = row_start
            utt["row_end"] = row_end

            for r in range(row_start, row_end + 1):
                covered_rows.add(r)

            csv_speaker = csv_speakers[csv_pos] if csv_pos < len(csv_speakers) else ""
            if ir_speaker and csv_speaker and ir_speaker != csv_speaker:
                result.warnings.append(
                    f"utterance index={utt_idx} speaker mismatch:"
                    f" IR='{ir_speaker}' CSV='{csv_speaker}'"
                )

            csv_pos = row_end
            result.matched += 1

        if not found:
            result.unmatched_utterances.append(utt_idx)
            result.warnings.append(
                f"utterance index={utt_idx} could not be matched"
                f" to CSV rows (from row {csv_pos + 1})"
            )
            # cascade failure 防止: 1 行進めて後続のマッチを試行可能にする
            if csv_pos < len(csv_rows):
                csv_pos += 1

    # uncovered rows
    for i in range(1, len(csv_rows) + 1):
        if i not in covered_rows:
            result.uncovered_rows.append(i)

    return result
