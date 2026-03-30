"""split_long_utterances の分割ロジックテスト。

B-04 品質改善: 表示幅ベースの分割をテストする。
"""

import pytest

from src.contracts.ymm4_csv_schema import YMM4CsvOutput, YMM4CsvRow
from src.pipeline.assemble_csv import (
    balance_subtitle_lines,
    display_width,
    estimate_display_lines,
    split_long_utterances,
)


class TestDisplayWidth:
    """display_width() のテスト。"""

    def test_fullwidth_only(self):
        """全角文字のみ: 文字数の2倍。"""
        assert display_width("あいうえお") == 10

    def test_halfwidth_only(self):
        """半角英数のみ: 文字数と同じ。"""
        assert display_width("hello") == 5

    def test_mixed(self):
        """全角半角混合。"""
        # "AIの" = A(1) + I(1) + の(2) = 4
        assert display_width("AIの") == 4

    def test_empty(self):
        assert display_width("") == 0

    def test_east_asian_ambiguous(self):
        """East Asian Ambiguous は全角扱い。"""
        # ～ (U+FF5E) は Fullwidth, ~ (U+301C) は Wide
        # ① (U+2460) は Ambiguous → 全角扱い
        assert display_width("①") == 2

    def test_fullwidth_punctuation(self):
        """全角句読点は幅2。"""
        assert display_width("。") == 2
        assert display_width("、") == 2


class TestSplitBackwardCompatibility:
    """display_width=False (デフォルト) で従来と同一動作。"""

    def _make_output(self, *texts: str, speaker: str = "れいむ") -> YMM4CsvOutput:
        return YMM4CsvOutput(rows=tuple(YMM4CsvRow(speaker=speaker, text=t) for t in texts))

    def test_short_text_not_split(self):
        output = self._make_output("短いテキスト。")
        result = split_long_utterances(output, max_length=80)
        assert len(result.rows) == 1

    def test_long_text_split_at_sentence_end(self):
        text = "最初の文です。二番目の文です。三番目の文です。"
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=20)
        assert len(result.rows) >= 2
        # 再結合すると元のテキストになる
        assert "".join(r.text for r in result.rows) == text

    def test_long_single_sentence_inside_multi_sentence_row_is_expanded(self):
        """複数文の先頭にある長文も、文ごとの fallback で再分割する。"""
        text = (
            "私たちが普段「アルゴリズムによる最適化」と聞くと、効率的でクリーンな魔法を想像しがちですが、"
            "もしその計算式に「人間の身体的限界」という変数が最初から欠落していたらどうなるか。"
            "今回の探求では、その裏側に切り込んでいきます。"
        )
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=80, use_display_width=True)
        assert len(result.rows) >= 3
        assert "".join(r.text for r in result.rows) == text

    def test_single_sentence_preserved_without_clause_break(self):
        """節分割候補のない長文はそのまま保持。"""
        text = "a" * 200
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=80)
        assert len(result.rows) == 1
        assert result.rows[0].text == text

    def test_single_sentence_split_at_clause_break(self):
        """句点がなくても読点で節分割する。"""
        text = "前半の説明が長く続き、後半の説明もまだ続いています"
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=28, use_display_width=True)
        assert len(result.rows) == 2
        assert "".join(r.text for r in result.rows) == text

    def test_speaker_preserved(self):
        output = self._make_output("長い文です。もう一つの文です。", speaker="まりさ")
        result = split_long_utterances(output, max_length=10)
        for row in result.rows:
            assert row.speaker == "まりさ"


class TestSplitDisplayWidth:
    """use_display_width=True のテスト。"""

    def _make_output(self, *texts: str, speaker: str = "れいむ") -> YMM4CsvOutput:
        return YMM4CsvOutput(rows=tuple(YMM4CsvRow(speaker=speaker, text=t) for t in texts))

    def test_fullwidth_triggers_split(self):
        """全角80文字 = display_width 160。max_length=120 で分割される。"""
        text = "あ" * 40 + "。" + "い" * 40 + "。"
        output = self._make_output(text)
        # len(text) = 82, but display_width = 164
        result = split_long_utterances(output, max_length=120, use_display_width=True)
        assert len(result.rows) == 2

    def test_fullwidth_no_split_with_len(self):
        """同じテキストが use_display_width=False だと分割されない。"""
        text = "あ" * 40 + "。" + "い" * 40 + "。"
        output = self._make_output(text)
        # len(text) = 82 <= 120
        result = split_long_utterances(output, max_length=120, use_display_width=False)
        assert len(result.rows) == 1

    def test_halfwidth_within_display_limit(self):
        """半角多めで文字数は超過するが表示幅は閾値内 → 分割されない。"""
        text = "a" * 50 + "." + "b" * 50 + "."
        output = self._make_output(text)
        # len = 102, display_width = 102 (all halfwidth)
        result = split_long_utterances(output, max_length=120, use_display_width=True)
        assert len(result.rows) == 1

    def test_reconstruct_original(self):
        """分割後に再結合すると元のテキストになる。"""
        text = "最初の説明文です。次に重要なポイントを述べます。最後にまとめです。"
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=30, use_display_width=True)
        assert "".join(r.text for r in result.rows) == text

    def test_single_sentence_no_split_point(self):
        """文末も節分割候補もない長文は display_width モードでもそのまま保持。"""
        text = "あ" * 100  # no sentence end
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=80, use_display_width=True)
        assert len(result.rows) == 1

    def test_single_sentence_split_before_connector(self):
        """接続句の直前でも節分割できる。"""
        text = "最初に状況を説明しますしかしここから結論に入ります"
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=28, use_display_width=True)
        assert len(result.rows) == 2
        assert result.rows[0].text.endswith("します")
        assert result.rows[1].text.startswith("しかし")
        assert "".join(r.text for r in result.rows) == text

    def test_single_sentence_split_after_quote_phrase(self):
        """通常候補が尽きた残り長文でも、引用句+機能語で節分割できる。"""
        text = "もしその計算式に「人間の身体的限界」という変数が最初から欠落していたらどうなるか。"
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=28, use_display_width=True)
        assert len(result.rows) >= 2
        assert "".join(r.text for r in result.rows) == text


class TestBalanceSubtitleLines:
    """balance_subtitle_lines() のテスト。"""

    def _make_output(self, *texts: str, speaker: str = "れいむ") -> YMM4CsvOutput:
        return YMM4CsvOutput(rows=tuple(YMM4CsvRow(speaker=speaker, text=t) for t in texts))

    def test_inserts_balanced_newline_after_comma(self):
        output = self._make_output("AAAAAA、BBBBBB")
        result = balance_subtitle_lines(output, chars_per_line=8, max_lines=2, use_display_width=True)
        assert result.rows[0].text == "AAAAAA、\nBBBBBB"
        assert estimate_display_lines(result.rows[0].text, 8) == 2

    def test_preserves_text_without_candidate(self):
        text = "ABCDEFGHIJKLMN"
        output = self._make_output(text)
        result = balance_subtitle_lines(output, chars_per_line=8, max_lines=2, use_display_width=True)
        assert result.rows[0].text == text

    def test_no_change_when_already_within_one_line(self):
        text = "短い文。"
        output = self._make_output(text)
        result = balance_subtitle_lines(output, chars_per_line=20, max_lines=2, use_display_width=True)
        assert result.rows[0].text == text

    def test_only_applies_to_two_line_mode(self):
        text = "AAAAAA、BBBBBB"
        output = self._make_output(text)
        result = balance_subtitle_lines(output, chars_per_line=8, max_lines=3, use_display_width=True)
        assert result.rows[0].text == text

    def test_avoids_one_character_second_line(self):
        text = "ABCDEFG、HI"
        output = self._make_output(text)
        result = balance_subtitle_lines(output, chars_per_line=8, max_lines=2, use_display_width=True)
        assert result.rows[0].text == text
