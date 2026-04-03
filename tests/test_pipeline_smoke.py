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


def test_analyze_speaker_roles_host_guest():
    """ロール推定: 長文話者=host、短応答話者=guest。"""
    from src.pipeline.normalize import analyze_speaker_roles
    from src.contracts.structured_script import StructuredScript, Utterance

    script = StructuredScript(utterances=(
        Utterance(speaker="Speaker_A", text="というわけで今回はAI技術の最新動向について詳しく解説していきます。"),
        Utterance(speaker="Speaker_B", text="はい。"),
        Utterance(speaker="Speaker_A", text="まずディープラーニングの進化ですが、トランスフォーマーモデルが登場してから劇的に変わりました。"),
        Utterance(speaker="Speaker_B", text="なるほど、具体的にはどういう変化ですか?"),
        Utterance(speaker="Speaker_A", text="自然言語処理の精度が飛躍的に向上し、以前は不可能だったタスクが実現できるようになったんです。"),
        Utterance(speaker="Speaker_B", text="ええ。"),
    ))

    roles = analyze_speaker_roles(script)
    assert roles["Speaker_A"]["role"] == "host"
    assert roles["Speaker_B"]["role"] == "guest"
    assert roles["Speaker_A"]["avg_length"] > roles["Speaker_B"]["avg_length"]


def test_load_ir_single_object(tmp_path):
    """load_ir: 単一 JSON オブジェクトを読み込む。"""
    from src.pipeline.ymmp_patch import load_ir

    ir_file = tmp_path / "ir.json"
    ir_file.write_text(
        '{"ir_version": "1.0", "macro": {"sections": []}, "utterances": []}',
        encoding="utf-8",
    )
    data = load_ir(ir_file)
    assert data["ir_version"] == "1.0"
    assert "macro" in data
    assert "utterances" in data


def test_load_ir_multi_object(tmp_path):
    """load_ir: 2つの JSON オブジェクト連結形式を読み込む。"""
    from src.pipeline.ymmp_patch import load_ir

    ir_file = tmp_path / "ir.json"
    ir_file.write_text(
        '{"ir_version": "1.0", "macro": {"sections": []}}\n'
        '{"utterances": [{"index": 1, "speaker": "A", "text": "hello"}]}',
        encoding="utf-8",
    )
    data = load_ir(ir_file)
    assert data["ir_version"] == "1.0"
    assert "macro" in data
    assert len(data["utterances"]) == 1
    assert data["utterances"][0]["speaker"] == "A"


def _project_root():
    """プロジェクトルートを返す。"""
    from pathlib import Path
    return Path(__file__).resolve().parent.parent
