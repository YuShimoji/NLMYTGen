"""NotebookLM 入力パース契約テスト。"""

import pytest

from src.pipeline.normalize import normalize


def test_parse_csv_two_column(tmp_path):
    """2列 CSV を正しくパースする。"""
    csv_file = tmp_path / "input.csv"
    csv_file.write_text("Host1,こんにちは\nHost2,よろしく\n", encoding="utf-8")

    script = normalize(csv_file)
    assert len(script.utterances) == 2
    assert script.utterances[0].speaker == "Host1"
    assert script.utterances[0].text == "こんにちは"
    assert script.utterances[1].speaker == "Host2"


def test_parse_text_with_timestamps(tmp_path):
    """タイムスタンプ付きテキストを正しくパースする。"""
    txt_file = tmp_path / "input.txt"
    txt_file.write_text(
        "[00:00] Host1: こんにちは、解説します\n"
        "[00:10] Host2: よろしくお願いします\n",
        encoding="utf-8",
    )

    script = normalize(txt_file)
    assert len(script.utterances) == 2
    assert script.utterances[0].speaker == "Host1"
    assert script.utterances[0].text == "こんにちは、解説します"


def test_parse_text_simple_colon(tmp_path):
    """シンプルコロン形式を正しくパースする。"""
    txt_file = tmp_path / "input.txt"
    txt_file.write_text(
        "ナレーター1: こんにちは、今日のテーマです\n"
        "ナレーター2：よろしくお願いします\n",
        encoding="utf-8",
    )

    script = normalize(txt_file)
    assert len(script.utterances) == 2
    assert script.utterances[0].speaker == "ナレーター1"
    assert script.utterances[1].speaker == "ナレーター2"


def test_empty_input_raises(tmp_path):
    """空入力は ValueError。"""
    txt_file = tmp_path / "input.txt"
    txt_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        normalize(txt_file)
