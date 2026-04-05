"""annotate_row_range: IR utterance と CSV 行の自動対応付けテスト."""

from __future__ import annotations

import copy

import pytest

from src.pipeline.row_range import annotate_row_range, _norm_strict, _norm_loose


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_ir(utterances: list[dict]) -> dict:
    return {
        "ir_version": "1.0",
        "video_id": "test",
        "macro": {"sections": [{"section_id": "S1", "start_index": 1,
                                 "end_index": len(utterances)}]},
        "utterances": utterances,
    }


def _utt(index: int, text: str, speaker: str = "sp") -> dict:
    return {"index": index, "speaker": speaker, "text": text, "section_id": "S1"}


# ---------------------------------------------------------------------------
# 正規化
# ---------------------------------------------------------------------------

class TestNormalization:
    def test_strict_removes_whitespace(self):
        assert _norm_strict("hello  world") == "helloworld"
        assert _norm_strict("hello\nworld") == "helloworld"

    def test_strict_nfkc(self):
        # 全角英数 → 半角
        assert _norm_strict("ＡＢＣ１２３") == "ABC123"

    def test_loose_removes_punctuation(self):
        assert _norm_loose("こんにちは、世界。") == "こんにちは世界"
        assert _norm_loose("Hello! World?") == "HelloWorld"
        assert _norm_loose("「括弧」テスト") == "括弧テスト"


# ---------------------------------------------------------------------------
# 基本マッチ
# ---------------------------------------------------------------------------

class TestBasicAnnotation:
    def test_basic_3utt_6rows(self):
        """3 utterance が 6 CSV 行にマッチ (1:2 ずつ)."""
        ir = _make_ir([
            _utt(1, "あいうえお かきくけこ"),
            _utt(2, "さしすせそ たちつてと"),
            _utt(3, "なにぬねの はひふへほ"),
        ])
        csv_rows = [
            ["sp", "あいうえお"],
            ["sp", "かきくけこ"],
            ["sp", "さしすせそ"],
            ["sp", "たちつてと"],
            ["sp", "なにぬねの"],
            ["sp", "はひふへほ"],
        ]
        result = annotate_row_range(ir, csv_rows)
        assert result.matched == 3
        assert ir["utterances"][0]["row_start"] == 1
        assert ir["utterances"][0]["row_end"] == 2
        assert ir["utterances"][1]["row_start"] == 3
        assert ir["utterances"][1]["row_end"] == 4
        assert ir["utterances"][2]["row_start"] == 5
        assert ir["utterances"][2]["row_end"] == 6

    def test_multi_row_span(self):
        """1 utterance が 3 行にまたがる."""
        ir = _make_ir([
            _utt(1, "あいうえおかきくけこさしすせそ"),
        ])
        csv_rows = [
            ["sp", "あいうえお"],
            ["sp", "かきくけこ"],
            ["sp", "さしすせそ"],
        ]
        result = annotate_row_range(ir, csv_rows)
        assert result.matched == 1
        assert ir["utterances"][0]["row_start"] == 1
        assert ir["utterances"][0]["row_end"] == 3

    def test_single_row_per_utterance(self):
        """1:1 対応."""
        ir = _make_ir([_utt(1, "テスト"), _utt(2, "確認")])
        csv_rows = [["sp", "テスト"], ["sp", "確認"]]
        result = annotate_row_range(ir, csv_rows)
        assert result.matched == 2
        assert ir["utterances"][0]["row_start"] == 1
        assert ir["utterances"][0]["row_end"] == 1


# ---------------------------------------------------------------------------
# 正規化差の吸収
# ---------------------------------------------------------------------------

class TestNormalizationMatching:
    def test_whitespace_newline_diff(self):
        """改行・空白差を strict で吸収."""
        ir = _make_ir([_utt(1, "あいう えお")])
        csv_rows = [["sp", "あいう\nえお"]]
        result = annotate_row_range(ir, csv_rows)
        assert result.matched == 1

    def test_punctuation_diff(self):
        """句読点差を loose で吸収."""
        ir = _make_ir([_utt(1, "こんにちは、世界。")])
        csv_rows = [["sp", "こんにちは世界"]]
        result = annotate_row_range(ir, csv_rows)
        assert result.matched == 1

    def test_fullwidth_halfwidth(self):
        """全角半角差を NFKC で吸収."""
        ir = _make_ir([_utt(1, "ＡＩ監視が追い詰める")])
        csv_rows = [["sp", "AI監視が追い詰める"]]
        result = annotate_row_range(ir, csv_rows)
        assert result.matched == 1


# ---------------------------------------------------------------------------
# カバレッジ
# ---------------------------------------------------------------------------

class TestCoverage:
    def test_all_rows_covered(self):
        ir = _make_ir([_utt(1, "あいう"), _utt(2, "えお")])
        csv_rows = [["sp", "あいう"], ["sp", "えお"]]
        result = annotate_row_range(ir, csv_rows)
        assert result.uncovered_rows == []

    def test_uncovered_trailing_rows(self):
        """IR より CSV が長い場合、末尾が uncovered."""
        ir = _make_ir([_utt(1, "あいう")])
        csv_rows = [["sp", "あいう"], ["sp", "余分な行"]]
        result = annotate_row_range(ir, csv_rows)
        assert result.uncovered_rows == [2]


# ---------------------------------------------------------------------------
# エラー / Warning
# ---------------------------------------------------------------------------

class TestErrorsAndWarnings:
    def test_unmatch_warning(self):
        """テキスト不一致で unmatched."""
        ir = _make_ir([_utt(1, "完全に異なるテキスト")])
        csv_rows = [["sp", "別の内容です"]]
        result = annotate_row_range(ir, csv_rows)
        assert 1 in result.unmatched_utterances
        assert len(result.warnings) > 0

    def test_speaker_mismatch_warning(self):
        """speaker 不一致で warning."""
        ir = _make_ir([_utt(1, "テスト", speaker="まりさ")])
        csv_rows = [["れいむ", "テスト"]]
        result = annotate_row_range(ir, csv_rows)
        assert result.matched == 1
        warnings = [w for w in result.warnings if "speaker mismatch" in w]
        assert len(warnings) == 1

    def test_short_repeated_text(self):
        """短い相槌が繰り返しても正しく前方進行する."""
        ir = _make_ir([
            _utt(1, "はい。"),
            _utt(2, "そうですね。"),
            _utt(3, "はい。"),
        ])
        csv_rows = [
            ["sp", "はい。"],
            ["sp", "そうですね。"],
            ["sp", "はい。"],
        ]
        result = annotate_row_range(ir, csv_rows)
        assert result.matched == 3
        assert ir["utterances"][0]["row_end"] == 1
        assert ir["utterances"][1]["row_end"] == 2
        assert ir["utterances"][2]["row_end"] == 3

    def test_no_cascade_failure(self):
        """1 件失敗後に後続が連鎖崩壊しない."""
        ir = _make_ir([
            _utt(1, "完全に異なる"),
            _utt(2, "マッチする文"),
        ])
        csv_rows = [
            ["sp", "ここは違う"],
            ["sp", "マッチする文"],
        ]
        result = annotate_row_range(ir, csv_rows)
        # utt 1 は unmatched だが utt 2 は matched
        assert 1 in result.unmatched_utterances
        assert result.matched >= 1


# ---------------------------------------------------------------------------
# 既存 range の扱い
# ---------------------------------------------------------------------------

class TestExistingRange:
    def test_existing_range_error_default(self):
        """既存 row_start/row_end がデフォルトで error."""
        ir = _make_ir([_utt(1, "テスト")])
        ir["utterances"][0]["row_start"] = 1
        ir["utterances"][0]["row_end"] = 1
        csv_rows = [["sp", "テスト"]]
        result = annotate_row_range(ir, csv_rows)
        assert result.matched == 0
        assert any("existing row_start" in w for w in result.warnings)

    def test_force_overwrite(self):
        """--force で上書き."""
        ir = _make_ir([_utt(1, "テスト")])
        ir["utterances"][0]["row_start"] = 99
        ir["utterances"][0]["row_end"] = 99
        csv_rows = [["sp", "テスト"]]
        result = annotate_row_range(ir, csv_rows, force=True)
        assert result.matched == 1
        assert ir["utterances"][0]["row_start"] == 1
        assert ir["utterances"][0]["row_end"] == 1

    def test_keep_existing(self):
        """--keep-existing でスキップ."""
        ir = _make_ir([
            _utt(1, "テスト"),
            _utt(2, "確認"),
        ])
        ir["utterances"][0]["row_start"] = 1
        ir["utterances"][0]["row_end"] = 1
        csv_rows = [["sp", "テスト"], ["sp", "確認"]]
        result = annotate_row_range(ir, csv_rows, keep_existing=True)
        assert result.matched == 2
        assert ir["utterances"][0]["row_start"] == 1  # preserved
        assert ir["utterances"][1]["row_start"] == 2  # newly matched
