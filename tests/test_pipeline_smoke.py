"""パイプラインスモークテスト。"""

import subprocess
import sys

from src.pipeline.normalize import normalize
from src.pipeline.assemble_csv import assemble


def test_csv_to_csv_roundtrip(tmp_path):
    """CSV 入力 → speaker_map 付き CSV 出力。"""
    input_csv = tmp_path / "in.csv"
    input_csv.write_text(
        "Host1,こんにちは世界のみなさん\nHost2,よろしくお願いします\n",
        encoding="utf-8",
    )

    script = normalize(input_csv)
    output = assemble(script, speaker_map={"Host1": "れいむ", "Host2": "まりさ"})

    out_path = tmp_path / "out.csv"
    output.write(out_path)

    lines = out_path.read_text(encoding="utf-8-sig").strip().splitlines()
    assert lines[0].startswith("れいむ,")
    assert lines[1].startswith("まりさ,")


def test_text_to_csv(tmp_path):
    """テキスト入力 → CSV 出力。"""
    input_txt = tmp_path / "in.txt"
    input_txt.write_text(
        "[00:00] Host1: 今日のテーマはAI技術です\n"
        "[00:10] Host2: 楽しみにしています\n",
        encoding="utf-8",
    )

    script = normalize(input_txt)
    output = assemble(script)

    assert len(output.rows) == 2
    assert output.rows[0].speaker == "Host1"
    assert output.rows[0].text == "今日のテーマはAI技術です"


def test_cli_build_csv(tmp_path):
    """CLI build-csv がファイルを生成する。"""
    input_csv = tmp_path / "in.csv"
    input_csv.write_text(
        "Host1,こんにちは世界のみなさん\nHost2,よろしくお願いします\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "out.csv"

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "build-csv", str(input_csv), "-o", str(out_csv)],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert out_csv.exists()
    content = out_csv.read_text(encoding="utf-8")
    assert "Host1" in content


def test_cli_validate(tmp_path):
    """CLI validate が正常終了する。"""
    input_csv = tmp_path / "in.csv"
    input_csv.write_text(
        "Host1,こんにちは世界のみなさん\nHost2,よろしくお願いします\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "src.cli.main", "validate", str(input_csv)],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "2 utterances" in result.stdout


def _project_root():
    """プロジェクトルートを返す。"""
    from pathlib import Path
    return Path(__file__).resolve().parent.parent
