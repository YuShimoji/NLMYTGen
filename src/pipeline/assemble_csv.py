"""CSV 組立: StructuredScript → YMM4CsvOutput。

話者マッピングの適用とテキスト内の話者プレフィックス除去を行う。
"""

from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

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

    # 大区切り: 閉じ括弧+助詞セットを最優先で保護
    for idx, ch in enumerate(text):
        if ch not in _CLOSE_BRACKETS:
            continue
        pos = idx + 1
        if pos < len(text) and text[pos] in _POST_BRACKET_PARTICLES:
            _add(pos + 1, 1, "major:bracket+particle")

    # 大区切り: 文字ベース
    for idx, ch in enumerate(text):
        pos = idx + 1  # 文字の直後
        penalty = _MAJOR_BREAK_AFTER.get(ch)
        if penalty is not None:
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
            boundary_penalty = _boundary_penalty(text, pos, page_split=True)
            score = distance_penalty + break_penalty + boundary_penalty
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
            boundary_penalty = _boundary_penalty(text, pos, page_split=True)
            score = distance_penalty + break_penalty + boundary_penalty
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


def insert_inline_breaks(
    text: str,
    *,
    chars_per_line: int,
) -> str:
    """話者行テキスト内に明示改行を挿入して、YMM4 自動折り返しを制御する。

    B-16: 1行が chars_per_line を超えないよう、区切り位置で改行を挿入する。
    大区切り (句読点等) を優先し、なければ小区切り (マーカー句等) を使う。
    どちらもなければ YMM4 自動折り返しに委ねる。
    既に改行が含まれている場合はそのまま返す。
    """
    if not text or chars_per_line <= 0 or "\n" in text:
        return text

    total_width = display_width(text)
    if total_width <= chars_per_line:
        return text

    widths = _width_at_positions(text)
    all_candidates = _collect_break_candidates(text)

    # 行内改行用の追加候補: 文字種境界 (ページ間分割では使わないが行内では許容)
    # penalty を高く (10) して大区切り/マーカー句を優先
    bracket_ranges = _find_bracket_ranges(text)
    inline_extras: list[tuple[int, int, str]] = []
    for idx in range(1, len(text)):
        pos = idx
        if _in_bracket(pos, bracket_ranges):
            continue
        if _is_katakana_run(text, pos) or _is_kanji_run(text, pos) or _is_digit_run(text, pos):
            continue
        if pos < len(text) and text[pos] == "ー":
            continue
        if pos > 0 and text[pos - 1] == "ー":
            continue

        prev_ch, curr_ch = text[idx - 1], text[idx]
        # 助詞の後 (行内では許容)
        if prev_ch in "をがはにでもやのへと":
            inline_extras.append((pos, 8, "inline:particle"))

    all_with_inline = sorted(
        all_candidates + inline_extras,
        key=lambda x: x[0],
    )
    if not all_with_inline:
        return text

    major = [(p, pen, k) for p, pen, k in all_with_inline if k.startswith("major")]
    minor = all_with_inline  # 全候補 (大+小+inline)

    min_line_width = max(4, chars_per_line // 6)

    def _best_break(candidates: list[tuple[int, int, str]], prev_pos: int, prev_w: int) -> int:
        """chars_per_line に最も近い候補を選ぶ。超過しない候補を優先。"""
        target_w = prev_w + chars_per_line
        total_w = widths[len(text)]
        best_score = float("inf")
        best_pos = -1

        for pos, penalty, _kind in candidates:
            if pos <= prev_pos:
                continue
            pos_w = widths[pos]
            line_w = pos_w - prev_w
            rest_w = total_w - pos_w

            # chars_per_line を超えない候補を優先 (超過ペナルティ)
            if line_w > chars_per_line:
                overflow_penalty = (line_w - chars_per_line) * 2
            else:
                overflow_penalty = 0

            # 短すぎる行はスキップ
            if line_w < min_line_width:
                continue
            # 残りが短すぎる行を作らない
            if 0 < rest_w < min_line_width:
                continue

            distance = abs(pos_w - target_w)
            boundary_penalty = _boundary_penalty(text, pos, page_split=False)
            score = distance + penalty * 2 + overflow_penalty + boundary_penalty
            if score < best_score:
                best_score = score
                best_pos = pos

        return best_pos

    result_parts: list[str] = []
    prev_pos = 0
    prev_width = 0

    while prev_pos < len(text):
        remaining_width = widths[len(text)] - prev_width
        if remaining_width <= chars_per_line:
            break  # 残りは1行に収まる

        # 第1優先: 大区切りで chars_per_line に近い位置を探す
        best_pos = _best_break(major, prev_pos, prev_width)

        # 大区切りが見つからない or chars_per_line を大幅超過 → 全候補で探す
        if best_pos > 0:
            line_w = widths[best_pos] - prev_width
            if line_w > chars_per_line * 1.3:
                # 大区切りが遠すぎる → 小区切りも含めて再探索
                alt_pos = _best_break(minor, prev_pos, prev_width)
                if alt_pos > 0:
                    alt_line_w = widths[alt_pos] - prev_width
                    if alt_line_w <= chars_per_line:
                        best_pos = alt_pos
        elif not best_pos or best_pos <= 0:
            # 大区切りなし → 全候補で探す
            best_pos = _best_break(minor, prev_pos, prev_width)

        if best_pos <= 0:
            break  # 候補なし、以降は YMM4 に委ねる

        result_parts.append(text[prev_pos:best_pos])
        prev_pos = best_pos
        prev_width = widths[best_pos]

    # 残りを追加
    if prev_pos < len(text):
        result_parts.append(text[prev_pos:])

    return "\n".join(result_parts)


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

    # B-16: 各話者行に行内改行を挿入
    rows = [
        YMM4CsvRow(
            speaker=r.speaker,
            text=insert_inline_breaks(r.text, chars_per_line=chars_per_line),
        )
        for r in rows
    ]

    return YMM4CsvOutput(rows=tuple(rows))


# ========================================================================
# B-17: 字幕改行アルゴリズム v2 (統合リフロー)
# ページ分割と行内改行を同時に決定する。
# ========================================================================

def _collect_break_candidates_v2(text: str) -> list[tuple[int, int, str]]:
    """ページ間+行内改行の両方に使える全区切り候補を列挙する。

    既存の _collect_break_candidates に加えて、行内改行用の文字種境界を統合。
    """
    base = _collect_break_candidates(text)

    bracket_ranges = _find_bracket_ranges(text)
    extras: list[tuple[int, int, str]] = []

    for idx in range(1, len(text)):
        pos = idx
        if _in_bracket(pos, bracket_ranges):
            continue
        if _is_katakana_run(text, pos) or _is_kanji_run(text, pos) or _is_digit_run(text, pos):
            continue
        if pos < len(text) and text[pos] == "ー":
            continue
        if pos > 0 and text[pos - 1] == "ー":
            continue

        prev_ch, curr_ch = text[idx - 1], text[idx]

        if prev_ch in "をがはにでもやのへと":
            extras.append((pos, 8, "v2:particle"))

    # 重複排除して統合 (低 penalty を優先)
    combined: dict[int, tuple[int, str]] = {}
    for pos, pen, kind in base + extras:
        existing = combined.get(pos)
        if existing is None or pen < existing[0]:
            combined[pos] = (pen, kind)

    return [(pos, pen, kind) for pos, (pen, kind) in sorted(combined.items())]


_LINE_START_FORBIDDEN = (
    "」", "』", "）", ")", "】", "、", "。", "，",
    "という", "として", "とは", "とも", "ですが", "です", "でした",
    "ます", "ません", "なく", "なく、", "ように", "ような",
)
_LINE_END_FORBIDDEN = (
    "「", "『", "（", "(", "【",
    "では", "とは", "とも", "という", "として",
)
_PROTECTED_PHRASES = (
    "という", "として", "とは", "とも",
    "について", "に対して", "により", "による", "によって",
    "ではなく", "ではなく、", "ながら",
    "ように", "ような", "めましょう",
    "ている", "ていく", "している", "していく", "にして",
)


def _boundary_penalty(text: str, pos: int, *, page_split: bool) -> float:
    """画面上のまとまりを壊す切断に追加ペナルティを与える。"""
    if pos <= 0 or pos >= len(text):
        return 0.0

    left = text[:pos]
    right = text[pos:]
    left_tail = left[-6:]
    right_head = right[:6]

    penalty = 0.0

    if right.startswith(_LINE_START_FORBIDDEN):
        penalty += 80.0
    if left.endswith(_LINE_END_FORBIDDEN):
        penalty += 80.0

    left_last = left[-1]
    right_first = right[0]

    if left_last in _OPEN_BRACKETS or right_first in _CLOSE_BRACKETS:
        penalty += 120.0

    # 活用語尾・送り仮名の分断は強く避ける。
    if _is_cjk_ideograph(left_last) and _is_hiragana(right_first):
        penalty += 140.0

    # 保護句の内部で切らない。
    for phrase in _PROTECTED_PHRASES:
        start = 0
        while True:
            idx = text.find(phrase, start)
            if idx < 0:
                break
            if idx < pos < idx + len(phrase):
                penalty += 160.0
                break
            start = idx + len(phrase)

    # 引用句+助詞/補助表現は一塊として扱う。
    if left_last in _CLOSE_BRACKETS and _is_hiragana(right_first):
        penalty += 120.0
    if any(ch in _CLOSE_BRACKETS for ch in left_tail[-3:]) and right.startswith(("と", "を", "が", "は", "に", "で", "も", "の", "へ", "や", "という")):
        penalty += 100.0

    # 助詞だけを行末に残して名詞句を次行へ送る切り方は避ける。
    if left_last in "とをがはにでものへや" and (
        _is_cjk_ideograph(right_first)
        or _is_katakana(right_first)
        or right_first in _OPEN_BRACKETS
    ):
        penalty += 55.0

    # ページ跨ぎは同一ページ内改行よりさらに重く扱う。
    if page_split:
        penalty *= 1.4

    return penalty


def _render_split_positions(text: str, split_positions: list[int]) -> list[str]:
    parts: list[str] = []
    prev = 0
    for pos in split_positions:
        parts.append(text[prev:pos])
        prev = pos
    parts.append(text[prev:])
    return [part for part in parts if part]


def _optimize_inline_break_positions(
    text: str,
    *,
    chars_per_line: int,
) -> list[int]:
    """ページ内の行分割を、完成した見え方ベースで最適化する。"""
    if not text or chars_per_line <= 0:
        return []

    total_width = display_width(text)
    if total_width <= chars_per_line:
        return []

    needed_lines = -(-total_width // chars_per_line)
    ideal_line_width = total_width / needed_lines
    min_line_width = max(6, chars_per_line // 6)

    widths = _width_at_positions(text)
    candidates = _collect_break_candidates_v2(text)
    if not candidates:
        return []

    major = [(p, pen, k) for p, pen, k in candidates if k.startswith("major")]
    beam: list[tuple[float, list[int]]] = [(0.0, [])]
    beam_width = 32

    def _expand_with(
        beam_state: list[tuple[float, list[int]]],
        cands: list[tuple[int, int, str]],
        split_idx: int,
    ) -> list[tuple[float, list[int]]]:
        next_beam: list[tuple[float, list[int]]] = []
        for cost, splits in beam_state:
            prev_pos = splits[-1] if splits else 0
            prev_w = widths[prev_pos]
            target_w = prev_w + ideal_line_width
            remaining_lines = needed_lines - split_idx - 1

            for pos, penalty, _kind in cands:
                if pos <= prev_pos:
                    continue
                pos_w = widths[pos]
                line_w = pos_w - prev_w
                rest_w = total_width - pos_w
                if line_w < min_line_width:
                    continue
                if remaining_lines > 0 and rest_w / remaining_lines < min_line_width:
                    continue

                overflow_penalty = max(0.0, line_w - chars_per_line) * 6.0
                width_penalty = abs(line_w - ideal_line_width)
                short_penalty = 0.0
                if line_w < ideal_line_width * 0.55:
                    short_penalty = (ideal_line_width * 0.55 - line_w) * 4.0

                total = (
                    cost
                    + width_penalty
                    + penalty * 3.0
                    + overflow_penalty
                    + short_penalty
                    + _boundary_penalty(text, pos, page_split=False)
                )
                next_beam.append((total, splits + [pos]))
        next_beam.sort(key=lambda x: x[0])
        return next_beam[:beam_width]

    for split_idx in range(needed_lines - 1):
        next_beam = _expand_with(beam, major, split_idx)
        if not next_beam:
            next_beam = _expand_with(beam, candidates, split_idx)
        if not next_beam:
            return []
        beam = next_beam

    best_cost = float("inf")
    best_splits: list[int] = []
    for cost, splits in beam:
        last_pos = splits[-1] if splits else 0
        last_w = total_width - widths[last_pos]
        if last_w < min_line_width:
            continue
        final_short = 0.0
        if last_w < ideal_line_width * 0.55:
            final_short = (ideal_line_width * 0.55 - last_w) * 5.0
        final_overflow = max(0.0, last_w - chars_per_line) * 6.0
        final_cost = cost + abs(last_w - ideal_line_width) + final_short + final_overflow
        if final_cost < best_cost:
            best_cost = final_cost
            best_splits = splits

    return best_splits


def _estimate_inline_layout_cost(
    text: str,
    *,
    chars_per_line: int,
) -> float:
    """ページ単位の見え方コストを見積もる。"""
    if not text:
        return 0.0

    split_positions = _optimize_inline_break_positions(text, chars_per_line=chars_per_line)
    lines = _render_split_positions(text, split_positions)
    if not lines:
        lines = [text]

    line_widths = [display_width(line) for line in lines]
    total_width = sum(line_widths)
    ideal_width = total_width / len(line_widths)

    cost = 0.0
    for width in line_widths:
        cost += abs(width - ideal_width)
        if width < max(6, chars_per_line * 0.45):
            cost += (chars_per_line * 0.45 - width) * 12.0
        if width < max(6, chars_per_line * 0.3):
            cost += (chars_per_line * 0.3 - width) * 18.0
        if width > chars_per_line:
            cost += (width - chars_per_line) * 12.0

    if len(line_widths) >= 2:
        cost += abs(line_widths[0] - line_widths[-1]) * 0.6

    return cost


def _force_page_split_overflow(
    text: str,
    *,
    page_capacity: int,
    chars_per_line: int,
) -> list[str]:
    """まだ容量超過しているページを、安全な候補で再分割する。"""
    if not text or display_width(text) <= page_capacity:
        return [text] if text else []

    widths = _width_at_positions(text)
    total_width = widths[len(text)]
    target = total_width / 2
    min_width = max(12, chars_per_line // 2)

    best_score = float("inf")
    best_pos = -1
    for pos, penalty, _kind in _collect_break_candidates_v2(text):
        left_width = widths[pos]
        right_width = total_width - left_width
        if left_width < min_width or right_width < min_width:
            continue
        score = (
            abs(left_width - target)
            + penalty * 4.0
            + _boundary_penalty(text, pos, page_split=True)
        )
        if score < best_score:
            best_score = score
            best_pos = pos

    if best_pos <= 0:
        return [text]

    left = text[:best_pos]
    right = text[best_pos:]
    result: list[str] = []
    result.extend(_force_page_split_overflow(
        left,
        page_capacity=page_capacity,
        chars_per_line=chars_per_line,
    ))
    result.extend(_force_page_split_overflow(
        right,
        page_capacity=page_capacity,
        chars_per_line=chars_per_line,
    ))
    return result


def _calc_ideal_pages(total_width: int, page_capacity: int) -> int:
    """理想的なページ数を計算する。"""
    return max(1, -(-total_width // page_capacity))


def _find_optimal_page_splits(
    text: str,
    widths: list[int],
    candidates: list[tuple[int, int, str]],
    *,
    num_pages: int,
    page_capacity: int,
    chars_per_line: int,
) -> list[int]:
    """ビーム探索でページ分割位置を最適化する。

    全ページの幅バランスに加え、ページ内の実際の見え方も加味する。
    """
    if num_pages <= 1:
        return []

    total_width = widths[len(text)]
    ideal_page_width = total_width / num_pages
    min_page_width = max(16, int(ideal_page_width * 0.3))

    BEAM_WIDTH = 50

    # 状態: (累積コスト, [分割位置リスト])
    beam: list[tuple[float, list[int]]] = [(0.0, [])]

    for split_idx in range(num_pages - 1):
        next_beam: list[tuple[float, list[int]]] = []

        for cost, splits in beam:
            prev_pos = splits[-1] if splits else 0
            prev_width = widths[prev_pos]

            for pos, penalty, _kind in candidates:
                if pos <= prev_pos:
                    continue

                pos_width = widths[pos]
                page_width = pos_width - prev_width

                if page_width < min_page_width:
                    continue

                remaining_width = total_width - pos_width
                remaining_pages = num_pages - split_idx - 1
                if remaining_pages > 0 and remaining_width / remaining_pages < min_page_width:
                    continue

                segment = text[prev_pos:pos]

                # コスト計算
                balance_cost = abs(page_width - ideal_page_width)
                break_cost = penalty * 4.0
                short_penalty = 0.0
                if page_width < ideal_page_width * 0.6:
                    short_penalty = (ideal_page_width * 0.6 - page_width) * 4.0
                overflow_penalty = 0.0
                if page_width > page_capacity:
                    overflow_penalty = (page_width - page_capacity) * 14.0
                boundary_cost = _boundary_penalty(text, pos, page_split=True)
                layout_cost = _estimate_inline_layout_cost(
                    segment,
                    chars_per_line=chars_per_line,
                )

                total_cost = (
                    cost
                    + balance_cost
                    + break_cost
                    + short_penalty
                    + overflow_penalty
                    + boundary_cost
                    + layout_cost
                )
                next_beam.append((total_cost, splits + [pos]))

        next_beam.sort(key=lambda x: x[0])
        beam = next_beam[:BEAM_WIDTH]

        if not beam:
            break

    # 最終ページの評価
    best_cost = float("inf")
    best_splits: list[int] = []

    for cost, splits in beam:
        last_pos = splits[-1] if splits else 0
        last_width = total_width - widths[last_pos]
        last_segment = text[last_pos:]

        final_balance = abs(last_width - ideal_page_width)
        final_short = 0.0
        if last_width < min_page_width:
            final_short = (min_page_width - last_width) * 3.0
        final_overflow = 0.0
        if last_width > page_capacity:
            final_overflow = (last_width - page_capacity) * 14.0

        final_layout = _estimate_inline_layout_cost(
            last_segment,
            chars_per_line=chars_per_line,
        )
        total = cost + final_balance + final_short + final_overflow + final_layout
        if total < best_cost:
            best_cost = total
            best_splits = splits

    return best_splits


def _insert_line_breaks_v2(
    text: str,
    *,
    chars_per_line: int,
) -> str:
    """ページ内テキストに行内改行を挿入する (v2)。

    全体の行数を先に計算し、理想行幅に近い候補で改行する。
    大区切り優先、なければ全候補を使う。
    """
    if not text or chars_per_line <= 0 or "\n" in text:
        return text

    split_positions = _optimize_inline_break_positions(
        text,
        chars_per_line=chars_per_line,
    )
    if not split_positions:
        return text
    return "\n".join(_render_split_positions(text, split_positions))


_STRUCTURAL_PARTICLES = frozenset("はがをにでとへものかや")
_STRUCTURAL_SENTENCE_ENDS = frozenset("。！？!?")
_STRUCTURAL_COMMAS = frozenset("、,，;；:：")


def _is_contentish(ch: str) -> bool:
    return (
        _is_cjk_ideograph(ch)
        or _is_katakana(ch)
        or ch.isdigit()
        or ch in _OPEN_BRACKETS
    )


def _advance_hiragana_run(text: str, start: int) -> int:
    pos = start
    while pos < len(text) and _is_hiragana(text[pos]):
        pos += 1
    return pos


def _collect_structural_breaks(text: str) -> list[tuple[int, int, str]]:
    """大区切り/小区切りを構造ベースで収集する。"""
    bracket_ranges = _find_bracket_ranges(text)
    candidates: dict[int, tuple[int, str]] = {}

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
        if text[pos - 1] == "ー" or text[pos] == "ー":
            return
        existing = candidates.get(pos)
        if existing is None or penalty < existing[0]:
            candidates[pos] = (penalty, kind)

    for idx, ch in enumerate(text):
        pos = idx + 1
        if ch in _STRUCTURAL_SENTENCE_ENDS:
            _add(pos, 0, "major:sentence")
            continue
        if ch in _STRUCTURAL_COMMAS:
            _add(pos, 3, "major:comma")
            continue
        if ch in _CLOSE_BRACKETS:
            if pos < len(text) and _is_hiragana(text[pos]):
                run_end = _advance_hiragana_run(text, pos)
                if run_end > pos and run_end < len(text):
                    _add(run_end, 12, "minor:close+tail")
            elif pos < len(text) and text[pos] not in _CLOSE_BRACKETS and not _is_contentish(text[pos]):
                _add(pos, 9, "minor:close")
            elif pos < len(text) and text[pos] not in _CLOSE_BRACKETS:
                _add(pos, 18, "minor:close+content")

    for pos in range(1, len(text)):
        prev_ch = text[pos - 1]
        curr_ch = text[pos]

        if prev_ch in _STRUCTURAL_PARTICLES and _is_contentish(curr_ch):
            _add(pos, 10, "minor:particle")

        if _is_hiragana(prev_ch) and _is_contentish(curr_ch):
            run_start = pos - 1
            while run_start > 0 and _is_hiragana(text[run_start - 1]):
                run_start -= 1
            if run_start > 0:
                left_anchor = text[run_start - 1]
                if _is_cjk_ideograph(left_anchor) or _is_katakana(left_anchor) or left_anchor.isdigit() or left_anchor in _CLOSE_BRACKETS:
                    run_len = pos - run_start
                    _add(pos, 12 + max(0, run_len - 3) * 2, "minor:hira-tail")

        if prev_ch.isdigit() and not curr_ch.isdigit() and not _is_cjk_ideograph(curr_ch):
            _add(pos, 11, "minor:number-end")

    return [(pos, penalty, kind) for pos, (penalty, kind) in sorted(candidates.items())]


def _structural_boundary_penalty(text: str, pos: int, *, page_split: bool) -> float:
    """個別語彙ではなく構造崩れに対して罰則を与える。"""
    if pos <= 0 or pos >= len(text):
        return 0.0

    left_last = text[pos - 1]
    right_first = text[pos]
    penalty = 0.0

    if left_last in _OPEN_BRACKETS:
        penalty += 140.0
    if left_last in _CLOSE_BRACKETS:
        penalty += 110.0
    if right_first in _CLOSE_BRACKETS or right_first in _STRUCTURAL_COMMAS:
        penalty += 240.0
    if left_last in _CLOSE_BRACKETS and _is_contentish(right_first):
        penalty += 180.0 if not page_split else 220.0
    if left_last in _CLOSE_BRACKETS and _is_hiragana(right_first):
        penalty += 90.0
        run_end = _advance_hiragana_run(text, pos)
        if run_end < len(text) and _is_contentish(text[run_end]):
            penalty += 260.0 if not page_split else 320.0
    if _is_cjk_ideograph(left_last) and _is_hiragana(right_first):
        penalty += 180.0
    if left_last in _STRUCTURAL_PARTICLES and _is_contentish(right_first):
        penalty += 45.0 if not page_split else 65.0

    run_start = pos
    while run_start > 0 and _is_hiragana(text[run_start - 1]):
        run_start -= 1
    run_len = pos - run_start
    if 0 < run_len <= 3 and _is_contentish(right_first):
        left_anchor_idx = run_start - 1
        if left_anchor_idx >= 0:
            left_anchor = text[left_anchor_idx]
            run_text = text[run_start:pos]
            is_particle_run = all(ch in _STRUCTURAL_PARTICLES for ch in run_text)
            if right_first in _OPEN_BRACKETS:
                is_particle_run = True
            if (
                not is_particle_run
                and (_is_cjk_ideograph(left_anchor) or _is_katakana(left_anchor) or left_anchor.isdigit() or left_anchor in _CLOSE_BRACKETS)
            ):
                penalty += 320.0 if not page_split else 400.0

    if page_split:
        penalty *= 1.3
    return penalty


def _line_width_cost(width: int, *, ideal: float, chars_per_line: int, is_last: bool) -> float:
    min_line = max(6, chars_per_line // 3)
    cost = abs(width - ideal)
    if width < min_line:
        cost += (min_line - width) * 10.0
    if not is_last and width < chars_per_line * 0.5:
        cost += (chars_per_line * 0.5 - width) * 9.0
    if width > chars_per_line:
        cost += (width - chars_per_line) * 18.0
    return cost


def _short_line_break_penalty(
    text: str,
    start: int,
    pos: int,
    end: int,
    *,
    line_width: int,
    tail_width: int,
    chars_per_line: int,
    max_lines: int,
) -> float:
    """読点・文頭導入句で生じるスカスカ行を抑制する。"""
    if start >= pos or pos > end:
        return 0.0

    left = text[start:pos]
    left_last = left[-1]
    penalty = 0.0
    short_threshold = max(12, int(chars_per_line * 0.55))
    very_short_threshold = max(8, int(chars_per_line * 0.35))
    remaining_lines = max(1, max_lines - 1)
    fits_without_break = (line_width + tail_width) <= chars_per_line * remaining_lines

    if line_width < short_threshold:
        penalty += (short_threshold - line_width) * 5.0

    if left_last in _STRUCTURAL_COMMAS and line_width < short_threshold:
        penalty += (short_threshold - line_width) * 14.0
        if fits_without_break:
            penalty += 80.0

    if left_last in _STRUCTURAL_SENTENCE_ENDS and line_width < very_short_threshold:
        penalty += (very_short_threshold - line_width) * 10.0
        if fits_without_break:
            penalty += 55.0

    # 「その瞬間、」「例えば、」のような短い導入句で切れた見え方を抑える。
    if line_width < short_threshold and len(left) <= 10:
        penalty += (short_threshold - line_width) * 6.0
        if fits_without_break:
            penalty += 35.0

    return penalty


def _layout_page_structural(
    text: str,
    start: int,
    end: int,
    widths: list[int],
    break_positions: list[int],
    *,
    chars_per_line: int,
    max_lines: int,
) -> tuple[float, list[int]]:
    """ページ内部を max_lines 行以内にレイアウトする。"""
    total_width = widths[end] - widths[start]
    if total_width <= chars_per_line:
        return _line_width_cost(total_width, ideal=total_width, chars_per_line=chars_per_line, is_last=True), []

    desired_lines = min(max_lines, max(1, -(-total_width // chars_per_line)))
    ideal_line_width = total_width / desired_lines
    inner_positions = [p for p in break_positions if start < p < end]

    @lru_cache(maxsize=None)
    def _dp(curr_pos: int, remaining_lines: int) -> tuple[float, tuple[int, ...]]:
        current_width = widths[end] - widths[curr_pos]
        if remaining_lines <= 1:
            return (
                _line_width_cost(
                    current_width,
                    ideal=ideal_line_width,
                    chars_per_line=chars_per_line,
                    is_last=True,
                ),
                (),
            )

        best_cost = float("inf")
        best_splits: tuple[int, ...] = ()
        for pos in inner_positions:
            if pos <= curr_pos:
                continue
            line_width = widths[pos] - widths[curr_pos]
            if line_width <= 0:
                continue
            tail_width = widths[end] - widths[pos]
            min_tail = max(6, chars_per_line // 3) * (remaining_lines - 1)
            if tail_width < min_tail:
                continue

            line_cost = _line_width_cost(
                line_width,
                ideal=ideal_line_width,
                chars_per_line=chars_per_line,
                is_last=False,
            )
            line_cost += _structural_boundary_penalty(text, pos, page_split=False)
            line_cost += _short_line_break_penalty(
                text,
                curr_pos,
                pos,
                end,
                line_width=line_width,
                tail_width=tail_width,
                chars_per_line=chars_per_line,
                max_lines=remaining_lines,
            )
            rest_cost, rest_splits = _dp(pos, remaining_lines - 1)
            total = line_cost + rest_cost
            if total < best_cost:
                best_cost = total
                best_splits = (pos,) + rest_splits

        if best_cost == float("inf"):
            return (
                _line_width_cost(
                    current_width,
                    ideal=ideal_line_width,
                    chars_per_line=chars_per_line,
                    is_last=True,
                ) + current_width,
                (),
            )
        return best_cost, best_splits

    cost, split_positions = _dp(start, desired_lines)
    return cost, list(split_positions)


def _render_lines_for_page(text: str, start: int, end: int, line_splits: list[int]) -> str:
    page_text = text[start:end]
    if not line_splits:
        return page_text
    relative = [p - start for p in line_splits]
    return "\n".join(_render_split_positions(page_text, relative))


def _reflow_utterance_structural(
    text: str,
    *,
    chars_per_line: int,
    max_lines: int,
) -> list[str]:
    if not text or chars_per_line <= 0 or max_lines <= 0:
        return [text] if text else []

    widths = _width_at_positions(text)
    total_width = widths[len(text)]
    page_capacity = chars_per_line * max_lines
    if total_width <= chars_per_line:
        return [text]

    breaks = _collect_structural_breaks(text)
    major_break_positions = [pos for pos, _pen, kind in breaks if kind.startswith("major:")]
    break_positions = [pos for pos, _pen, _kind in breaks]
    desired_pages = max(1, -(-total_width // page_capacity))
    ideal_page_width = total_width / desired_pages
    min_page_width = max(12, int(page_capacity * 0.3))

    def _solve_page_plan(page_break_positions: list[int]) -> tuple[float, tuple[tuple[int, tuple[int, ...]], ...]] | None:
        positions = [0] + page_break_positions + [len(text)]

        @lru_cache(maxsize=None)
        def _page_dp(start_idx: int) -> tuple[float, tuple[tuple[int, tuple[int, ...]], ...]] | None:
            start = positions[start_idx]
            if start == len(text):
                return 0.0, ()

            best_cost = float("inf")
            best_plan: tuple[tuple[int, tuple[int, ...]], ...] = ()
            for end_idx in range(start_idx + 1, len(positions)):
                end = positions[end_idx]
                seg_width = widths[end] - widths[start]
                if end != len(text) and seg_width < min_page_width:
                    continue
                if seg_width > page_capacity * 1.35:
                    break

                line_cost, line_splits = _layout_page_structural(
                    text,
                    start,
                    end,
                    widths,
                    break_positions,
                    chars_per_line=chars_per_line,
                    max_lines=max_lines,
                )
                page_cost = line_cost + abs(seg_width - ideal_page_width) * 0.35
                if end != len(text) and seg_width < ideal_page_width * 0.45:
                    page_cost += (ideal_page_width * 0.45 - seg_width) * 8.0
                if seg_width > page_capacity:
                    page_cost += (seg_width - page_capacity) * 22.0
                if end < len(text):
                    page_cost += _structural_boundary_penalty(text, end, page_split=True)

                rest = _page_dp(end_idx)
                if rest is None:
                    continue
                rest_cost, rest_plan = rest
                total = page_cost + rest_cost
                if total < best_cost:
                    best_cost = total
                    best_plan = ((end, tuple(line_splits)),) + rest_plan

            if best_cost == float("inf"):
                return None
            return best_cost, best_plan

        return _page_dp(0)

    major_solved = _solve_page_plan(major_break_positions) if major_break_positions else None
    all_solved = _solve_page_plan(break_positions)

    solved = major_solved
    if solved is None or (all_solved is not None and all_solved[0] < solved[0]):
        solved = all_solved
    if solved is None:
        line_cost, line_splits = _layout_page_structural(
            text,
            0,
            len(text),
            widths,
            break_positions,
            chars_per_line=chars_per_line,
            max_lines=max_lines,
        )
        plan = ((len(text), tuple(line_splits)),)
    else:
        _cost, plan = solved
    pages: list[str] = []
    prev = 0
    for end, line_splits in plan:
        pages.append(_render_lines_for_page(text, prev, end, list(line_splits)))
        prev = end
    return [page for page in pages if page]


def reflow_utterance_v2(
    text: str,
    *,
    chars_per_line: int,
    max_lines: int,
) -> list[str]:
    """v2: 大区切り→小区切りの階層でページ分割と行内改行を別々に決める。"""
    return _reflow_utterance_structural(
        text,
        chars_per_line=chars_per_line,
        max_lines=max_lines,
    )


def reflow_subtitles_v2(
    output: YMM4CsvOutput,
    *,
    chars_per_line: int,
    max_lines: int,
) -> YMM4CsvOutput:
    """v2: ページ分割+行内改行を統合的に決定する字幕リフロー。"""
    if chars_per_line <= 0 or max_lines <= 0:
        return output

    rows: list[YMM4CsvRow] = []
    for row in output.rows:
        pages = reflow_utterance_v2(
            row.text,
            chars_per_line=chars_per_line,
            max_lines=max_lines,
        )
        for page in pages:
            rows.append(YMM4CsvRow(speaker=row.speaker, text=page))

    return YMM4CsvOutput(rows=tuple(rows))
