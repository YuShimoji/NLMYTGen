"""edit_hints モジュールのテスト。"""

from src.contracts.ymm4_csv_schema import YMM4CsvOutput, YMM4CsvRow
from src.pipeline.edit_hints import generate_edit_hints, _estimate_duration, _detect_expression


def _make_output(rows: list[tuple[str, str]]) -> YMM4CsvOutput:
    return YMM4CsvOutput(rows=tuple(YMM4CsvRow(speaker=s, text=t) for s, t in rows))


class TestEstimateDuration:
    def test_basic(self):
        # 10文字 / 5文字/秒 = 2.0秒
        assert _estimate_duration("あいうえおかきくけこ") == 2.0

    def test_empty(self):
        assert _estimate_duration("") == 0.0


class TestDetectExpression:
    def test_question(self):
        assert _detect_expression("本当ですか？") == "question"

    def test_excited(self):
        assert _detect_expression("すごい！") == "excited"

    def test_laugh(self):
        assert _detect_expression("ふふ、面白いですね") == "laugh"

    def test_surprise(self):
        assert _detect_expression("え！まさか") == "surprise"

    def test_neutral(self):
        assert _detect_expression("そうですね、確かに。") == "neutral"


class TestGenerateEditHints:
    def test_basic_structure(self):
        output = _make_output([
            ("れいむ", "こんにちは、今日はAI技術について解説します。"),
            ("まりさ", "よろしくお願いします。"),
            ("れいむ", "さて、まずはディープラーニングの基本から見ていきましょう。"),
            ("まりさ", "なるほど、面白いですね！"),
        ])
        hints = generate_edit_hints(output, source_file="test.txt")

        assert hints.total_utterances == 4
        assert hints.total_chars > 0
        assert hints.estimated_total_duration_sec > 0
        assert len(hints.rows) == 4
        assert len(hints.speaker_stats) == 2
        assert "れいむ" in hints.speaker_stats
        assert "まりさ" in hints.speaker_stats

    def test_segment_detection(self):
        output = _make_output([
            ("れいむ", "今回のテーマはAI監視です。"),
            ("まりさ", "面白そうですね。"),
            ("れいむ", "ところで、最近の動向を見てみましょう。"),
            ("まりさ", "はい、お願いします。"),
        ])
        hints = generate_edit_hints(output)

        # row 0 と row 2 ("ところで") がセグメント開始
        assert hints.rows[0].is_segment_start is True
        assert hints.rows[1].is_segment_start is False
        assert hints.rows[2].is_segment_start is True
        assert len(hints.segments) == 2
        # topic_preview
        assert "今回のテーマ" in hints.segments[0].topic_preview
        assert "ところで" in hints.segments[1].topic_preview

    def test_expression_hints_in_rows(self):
        output = _make_output([
            ("れいむ", "どうしてそうなるんですか？"),
            ("まりさ", "すごいですね！"),
            ("れいむ", "普通のことです。"),
        ])
        hints = generate_edit_hints(output)

        assert hints.rows[0].expression_hint == "question"
        assert hints.rows[1].expression_hint == "excited"
        assert hints.rows[2].expression_hint == "neutral"

    def test_to_dict(self):
        output = _make_output([
            ("れいむ", "テストです。"),
        ])
        hints = generate_edit_hints(output, source_file="test.txt")
        d = hints.to_dict()

        assert d["source"] == "test.txt"
        assert "generated" in d
        assert d["summary"]["total_utterances"] == 1
        assert len(d["rows"]) == 1
        assert len(d["segments"]) == 1
        assert d["rows"][0]["speaker"] == "れいむ"

    def test_speaker_stats(self):
        output = _make_output([
            ("れいむ", "あいうえお"),  # 5文字
            ("まりさ", "かきくけこさしすせそ"),  # 10文字
            ("れいむ", "たちつてと"),  # 5文字
        ])
        hints = generate_edit_hints(output)

        assert hints.speaker_stats["れいむ"]["utterances"] == 2
        assert hints.speaker_stats["れいむ"]["total_chars"] == 10
        assert hints.speaker_stats["まりさ"]["utterances"] == 1
        assert hints.speaker_stats["まりさ"]["total_chars"] == 10
