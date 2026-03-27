"""CSV Handoff 契約テスト。"""

from src.contracts.structured_script import Utterance, StructuredScript
from src.contracts.ymm4_csv_schema import YMM4CsvOutput, YMM4CsvRow
from src.pipeline.assemble_csv import assemble


def test_basic_two_column_output(tmp_path):
    """出力 CSV は 2列、ヘッダーなし。"""
    script = StructuredScript(
        utterances=(
            Utterance(speaker="れいむ", text="こんにちは"),
            Utterance(speaker="まりさ", text="よろしく"),
        )
    )
    output = assemble(script)
    csv_path = tmp_path / "out.csv"
    output.write(csv_path)

    lines = csv_path.read_text(encoding="utf-8-sig").strip().splitlines()
    assert len(lines) == 2
    assert lines[0] == "れいむ,こんにちは"
    assert lines[1] == "まりさ,よろしく"


def test_speaker_mapping_applied():
    """speaker_map が正しく適用される。"""
    script = StructuredScript(
        utterances=(
            Utterance(speaker="Host1", text="hello"),
            Utterance(speaker="Host2", text="world"),
        )
    )
    output = assemble(script, speaker_map={"Host1": "れいむ", "Host2": "まりさ"})
    assert output.rows[0].speaker == "れいむ"
    assert output.rows[1].speaker == "まりさ"


def test_speaker_prefix_stripped():
    """テキスト内の話者プレフィックスが除去される。"""
    script = StructuredScript(
        utterances=(
            Utterance(speaker="Host1", text="Host1: これはテストです"),
        )
    )
    output = assemble(script)
    assert output.rows[0].text == "これはテストです"


def test_utf8_with_bom(tmp_path):
    """出力は UTF-8 BOM 付き (YMM4 互換)。"""
    output = YMM4CsvOutput(
        rows=(YMM4CsvRow(speaker="れいむ", text="日本語テスト"),)
    )
    csv_path = tmp_path / "out.csv"
    output.write(csv_path)

    raw = csv_path.read_bytes()
    # BOM (EF BB BF) で始まる
    assert raw.startswith(b"\xef\xbb\xbf")
    # UTF-8 でデコード可能
    text = raw.decode("utf-8-sig")
    assert "れいむ" in text
    assert "日本語テスト" in text
