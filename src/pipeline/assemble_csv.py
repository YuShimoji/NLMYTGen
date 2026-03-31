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


# ========================================================================
# B-15: トップダウン改行アルゴリズム
# ========================================================================

def _is_katakana(ch: str) -> bool:
    return "\u30A0" <= ch <= "\u30FF"


def _is_hiragana(ch: str) -> bool:
    return "\u3040" <= ch <= "\u309F"


def _is_cjk_ideograph(ch: str) -> bool:
    cp = ord(ch)
    return 0x4E00 <= cp <= 0x9FFF


_BRACKET_PAIRS = {"「": "」", "『": "』", "（": "）", "(": ")", "【": "】"}
_CLOSE_BRACKETS = set(_BRACKET_PAIRS.values())
_OPEN_BRACKETS = set(_BRACKET_PAIRS.keys())
_POST_BRACKET_PARTICLES = frozenset("とをがはにでもやのへ")


def _find_bracket_ranges(text: str) -> list[tuple[int, int]]:
    """括弧ペアの開始・終了インデックスを返す（ネスト非対応、最外のみ）。"""
    ranges: list[tuple[int, int]] = []
    stack: list[tuple[str, int]] = []
    for i, ch in enumerate(text):
        if ch in _OPEN_BRACKETS:
            stack.append((ch, i))
        elif ch in _CLOSE_BRACKETS and stack:
            _, start = stack.pop()
            ranges.append((start, i))
    return ranges


def _in_bracket(pos: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start < pos < end for start, end in ranges)


def _is_katakana_run(text: str, pos: int) -> bool:
    """pos が連続カタカナ（含む長音符・中黒）の途中かどうか。"""
    if pos <= 0 or pos >= len(text):
        return False
    before = text[pos - 1]
    after = text[pos]
    def is_kata_like(c: str) -> bool:
        return _is_katakana(c) or c in ("ー", "・")
    return is_kata_like(before) and is_kata_like(after)


def _is_kanji_run(text: str, pos: int) -> bool:
    """pos が連続漢字の途中かどうか。"""
    if pos <= 0 or pos >= len(text):
        return False
    return _is_cjk_ideograph(text[pos - 1]) and _is_cjk_ideograph(text[pos])


def _is_digit_run(text: str, pos: int) -> bool:
    """pos が連続数字（含む隣接記号 .,/%）の途中かどうか。"""
    if pos <= 0 or pos >= len(text):
        return False
    digit_adjacent = frozenset(".,/%")
    before = text[pos - 1]
    after = text[pos]
    # 数字同士
    if before.isdigit() and after.isdigit():
        return True
    # 数字+記号 or 記号+数字
    if before.isdigit() and after in digit_adjacent:
        return True
    if before in digit_adjacent and after.isdigit():
        return True
    return False


# 大区切り候補
_MAJOR_BREAK_AFTER: dict[str, int] = {
    "。": 0, "！": 0, "？": 0, "!": 0, "?": 0,
    "、": 1, ",": 1, "，": 1,
    ";": 2, ":": 2, "：": 2, "；": 2,
}

# 接続句（直前で分割）
_MAJOR_BREAK_BEFORE = (
    "しかし", "しかしながら", "ですが", "でも",
    "なので", "ため", "一方で", "ということ",
)

# 小区切り: マーカー句
_MINOR_MARKER_AFTER = (
    "という", "として", "により", "による",
    "について", "に対して", "していたら", "したら", "すると",
)


def _collect_break_candidates(text: str) -> list[tuple[int, int, str]]:
    """テキスト全体の区切り候補を列挙する。

    戻り値: [(分割位置, penalty, 種別), ...]
    分割位置は「ここで切る」= text[:pos] と text[pos:] に分かれる位置。
    """
    candidates: dict[int, tuple[int, str]] = {}
    bracket_ranges = _find_bracket_ranges(text)

    def _add(pos: int, penalty: int, kind: str) -> None:
        if pos <= 0 or pos >= len(text):
            return
        if _in_bracket(pos, bracket_ranges):
            return
        if _is_katakana_run(text, pos):
            return
        if _is_kanji_run(text, pos):
            return
        if _is_digit_run(text, pos):
            return
        # 長音符の直前・直後を禁止
        if pos < len(text) and text[pos] == "ー":
            return
        if pos > 0 and text[pos - 1] == "ー":
            return
        existing = candidates.get(pos)
        if existing is None or penalty < existing[0]:
            candidates[pos] = (penalty, kind)

    # 大区切り: 文字ベース
    for idx, ch in enumerate(text):
        pos = idx + 1  # 文字の直後
        penalty = _MAJOR_BREAK_AFTER.get(ch)
        if penalty is not None:
            # 閉じ括弧+助詞セットの保護
            if ch in _CLOSE_BRACKETS:
                # 次の文字が助詞なら、助詞の後を候補にする
                if pos < len(text) and text[pos] in _POST_BRACKET_PARTICLES:
                    _add(pos + 1, 1, "major:bracket+particle")
                    continue
            _add(pos, penalty, "major")

    # 閉じ括弧単体（助詞なし）
    for idx, ch in enumerate(text):
        if ch in _CLOSE_BRACKETS:
            pos = idx + 1
            if pos < len(text) and text[pos] not in _POST_BRACKET_PARTICLES:
                _add(pos, 2, "major:bracket")

    # 大区切り: 接続句の直前
    for marker in _MAJOR_BREAK_BEFORE:
        start = 0
        while True:
            idx = text.find(marker, start)
            if idx <= 0:
                break
            _add(idx, 2, "major:connector")
            start = idx + len(marker)

    # 小区切り: マーカー句の直後
    for marker in _MINOR_MARKER_AFTER:
        start = 0
        while True:
            idx = text.find(marker, start)
            if idx < 0:
                break
            _add(idx + len(marker), 3, "minor:marker")
            start = idx + len(marker)

    # 小区切り: 文字種境界
    # 注: 漢字→ひらがな (kanji-hira) は候補にしない。
    # 「単/なる」「見間違/った」のような不自然な切断が発生するため。
    # カタカナ→ひらがな、ひらがな→カタカナも候補にしない。
    # 大区切り(句読点等)がない場所では分割せず YMM4 の自動折り返しに任せる方針。
    for idx in range(1, len(text)):
        prev_ch, curr_ch = text[idx - 1], text[idx]
        pos = idx

        # 数字→非数字 (数値の末尾)
        if prev_ch.isdigit() and not curr_ch.isdigit():
            _add(pos, 4, "minor:digit-end")

    return [(pos, pen, kind) for pos, (pen, kind) in sorted(candidates.items())]


def _width_at_positions(text: str) -> list[int]:
    """各文字位置での累積表示幅を返す。widths[i] = text[:i] の幅。"""
    widths = [0]
    for ch in text:
        w = 2 if unicodedata.east_asian_width(ch) in ("F", "W", "A") else 1
        widths.append(widths[-1] + w)
    return widths


def reflow_utterance(
    text: str,
    *,
    chars_per_line: int,
    max_lines: int,
) -> list[str]:
    """話者の1発話を、画面表示に最適化された複数行に分割する。

    トップダウン方式:
    1. 総幅から必要行数を決定
    2. 理想行長を計算
    3. 各行末の理想位置近傍で最適な区切りを選択
    """
    if not text or chars_per_line <= 0 or max_lines <= 0:
        return [text] if text else []

    total_width = display_width(text)
    if total_width <= chars_per_line:
        return [text]

    # 必要行数を決定
    needed_lines = -(-total_width // chars_per_line)  # ceil division
    needed_lines = min(needed_lines, max_lines)
    if needed_lines <= 1:
        return [text]

    # 理想行幅
    ideal_width = total_width / needed_lines

    # 累積幅テーブル
    widths = _width_at_positions(text)

    # 区切り候補を列挙
    all_candidates = _collect_break_candidates(text)
    if not all_candidates:
        return [text]

    # 大区切りのみを優先的に使う。小区切りはフォールバック。
    major_candidates = [(p, pen, k) for p, pen, k in all_candidates if k.startswith("major")]

    # 探索範囲: 理想位置 ± chars_per_line/3
    search_margin = max(8, chars_per_line // 3)
    min_line_width = max(8, chars_per_line // 5)

    def _find_best_in(candidates: list[tuple[int, int, str]], prev_pos: int, abs_target: float, prev_width: int) -> int:
        best_score = float("inf")
        best_pos = -1
        total_w = widths[len(text)]

        # 第1パス: 探索範囲内
        for pos, penalty, _kind in candidates:
            if pos <= prev_pos:
                continue
            pos_width = widths[pos]
            if abs(pos_width - abs_target) > search_margin:
                continue
            line_width = pos_width - prev_width
            remaining_width = total_w - pos_width
            if line_width < min_line_width or remaining_width < min_line_width:
                continue
            distance_penalty = abs(pos_width - abs_target)
            break_penalty = penalty * 3
            score = distance_penalty + break_penalty
            if score < best_score:
                best_score = score
                best_pos = pos

        if best_pos > 0:
            return best_pos

        # 第2パス: 範囲を広げる
        for pos, penalty, _kind in candidates:
            if pos <= prev_pos:
                continue
            pos_width = widths[pos]
            line_width = pos_width - prev_width
            remaining_width = total_w - pos_width
            if line_width < min_line_width or remaining_width < min_line_width:
                continue
            distance_penalty = abs(pos_width - abs_target)
            break_penalty = penalty * 3
            score = distance_penalty + break_penalty
            if score < best_score:
                best_score = score
                best_pos = pos

        return best_pos

    # 各行末の最適な区切りを選択
    split_positions: list[int] = []
    for line_idx in range(1, needed_lines):
        prev_pos = split_positions[-1] if split_positions else 0
        prev_width = widths[prev_pos]
        abs_target = prev_width + ideal_width

        # まず大区切りで探す
        best_pos = _find_best_in(major_candidates, prev_pos, abs_target, prev_width)

        # 大区切りが見つからなければ分割しない（YMM4の自動折り返しに任せる）
        if best_pos <= 0:
            break

        split_positions.append(best_pos)

    if not split_positions:
        return [text]

    # テキストを分割
    result: list[str] = []
    prev = 0
    for pos in split_positions:
        result.append(text[prev:pos])
        prev = pos
    result.append(text[prev:])

    return [chunk for chunk in result if chunk]


def reflow_subtitles(
    output: YMM4CsvOutput,
    *,
    chars_per_line: int,
    max_lines: int,
) -> YMM4CsvOutput:
    """トップダウン方式で字幕行を最適分割する。

    split_long_utterances + balance_subtitle_lines の統合版。
    """
    if chars_per_line <= 0 or max_lines <= 0:
        return output

    _measure = display_width
    effective_max = chars_per_line * max_lines
    rows: list[YMM4CsvRow] = []

    for row in output.rows:
        if _measure(row.text) <= chars_per_line:
            rows.append(row)
            continue

        # 複数文を句点で分離してから各文を reflow
        sentences = [s for s in _SENTENCE_ENDS.split(row.text) if s]
        if len(sentences) > 1:
            expanded: list[str] = []
            for sentence in sentences:
                if _measure(sentence) > effective_max:
                    # max_lines 行に収まらない長文 → 再帰的に reflow
                    pending = [sentence]
                    while pending:
                        t = pending.pop(0)
                        if _measure(t) <= effective_max:
                            expanded.append(t)
                            continue
                        parts = reflow_utterance(t, chars_per_line=chars_per_line, max_lines=max_lines)
                        if len(parts) <= 1:
                            expanded.append(t)
                        else:
                            pending = parts + pending
                else:
                    expanded.append(sentence)

            # 文をグループ化 (max_lines 行に収まるよう)
            buf = ""
            for sentence in expanded:
                combined = buf + sentence
                if buf and _measure(combined) > effective_max:
                    rows.append(YMM4CsvRow(speaker=row.speaker, text=buf))
                    buf = sentence
                else:
                    buf = combined
            if buf:
                rows.append(YMM4CsvRow(speaker=row.speaker, text=buf))
        else:
            # 単一文 → reflow (再帰的に effective_max 以下まで分割)
            pending = [row.text]
            final_chunks: list[str] = []
            while pending:
                t = pending.pop(0)
                if _measure(t) <= effective_max:
                    final_chunks.append(t)
                    continue
                parts = reflow_utterance(t, chars_per_line=chars_per_line, max_lines=max_lines)
                if len(parts) <= 1:
                    final_chunks.append(t)  # 分割不能
                else:
                    pending = parts + pending  # 再帰的に処理
            for chunk in final_chunks:
                rows.append(YMM4CsvRow(speaker=row.speaker, text=chunk))

    return YMM4CsvOutput(rows=tuple(rows))
