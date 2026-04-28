"""build-csv --format json が stats ペイロードを含むこと（GUI 表示用）。"""

import csv
import json

from src.cli.main import main


def _font_size(value: float) -> dict:
    return {
        "Values": [{"Value": value}],
        "Span": 0.0,
        "AnimationType": "なし",
    }


def test_build_csv_json_includes_stats(tmp_path, capsys) -> None:
    txt = tmp_path / "script.txt"
    txt.write_text(
        "[00:00] Host1: 短い\n"
        "[00:01] Host2: もう一行\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "out.csv"
    code = main(
        [
            "build-csv",
            str(txt),
            "-o",
            str(out_csv),
            "--format",
            "json",
            "--max-lines",
            "2",
            "--chars-per-line",
            "20",
        ],
    )
    assert code == 0
    out = capsys.readouterr().out.strip()
    parsed = json.loads(out.split("\n")[-1])
    assert parsed.get("success") is True
    assert "stats" in parsed
    st = parsed["stats"]
    assert st["total_utterances"] == 2
    assert len(st["speakers"]) == 2
    assert st["overflow_params"] is not None
    assert st["overflow_params"]["chars_per_line"] == 20
    assert st["overflow_params"]["subtitle_font_scale"] == 100.0
    assert st["overflow_params"]["effective_chars_per_line"] == 20
    assert st["overflow_params"]["max_display_lines"] == 2
    assert isinstance(st["overflow_candidates"], list)


def test_build_csv_font_scale_narrows_effective_chars_per_line(tmp_path, capsys) -> None:
    txt = tmp_path / "script.txt"
    txt.write_text(
        "[00:00] Host1: これは字幕フォント倍率のテストです。大きい文字では早めに改行します。\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "scaled.csv"
    code = main(
        [
            "build-csv",
            str(txt),
            "-o",
            str(out_csv),
            "--format",
            "json",
            "--max-lines",
            "2",
            "--chars-per-line",
            "40",
            "--subtitle-font-scale",
            "125",
            "--reflow-v2",
        ],
    )
    assert code == 0
    out = capsys.readouterr().out.strip()
    parsed = json.loads(out.split("\n")[-1])
    op = parsed["stats"]["overflow_params"]
    assert op["chars_per_line"] == 40
    assert op["subtitle_font_scale"] == 125.0
    assert op["effective_chars_per_line"] == 32

    rows = list(csv.reader(out_csv.open(encoding="utf-8-sig", newline="")))
    assert "\n" in rows[0][1]


def test_build_csv_font_scale_default_keeps_existing_width(tmp_path, capsys) -> None:
    txt = tmp_path / "script.txt"
    txt.write_text(
        "[00:00] Host1: これは字幕フォント倍率のテストです。大きい文字では早めに改行します。\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "default.csv"
    code = main(
        [
            "build-csv",
            str(txt),
            "-o",
            str(out_csv),
            "--format",
            "json",
            "--max-lines",
            "2",
            "--chars-per-line",
            "40",
            "--reflow-v2",
        ],
    )
    assert code == 0
    capsys.readouterr()

    rows = list(csv.reader(out_csv.open(encoding="utf-8-sig", newline="")))
    assert "\n" not in rows[0][1]


def test_build_csv_font_scale_can_be_inferred_from_ymmp(tmp_path, capsys) -> None:
    txt = tmp_path / "script.txt"
    txt.write_text(
        "[00:00] Host1: これは字幕フォント倍率のテストです。大きい文字では早めに改行します。\n",
        encoding="utf-8",
    )
    ymmp = tmp_path / "template.ymmp"
    ymmp.write_text(
        json.dumps(
            {
                "Characters": [
                    {
                        "Name": "れいむ",
                        "Font": "メイリオ",
                        "FontSize": _font_size(60.0),
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8-sig",
    )
    out_csv = tmp_path / "inferred.csv"
    code = main(
        [
            "build-csv",
            str(txt),
            "-o",
            str(out_csv),
            "--format",
            "json",
            "--max-lines",
            "2",
            "--chars-per-line",
            "40",
            "--subtitle-font-source-ymmp",
            str(ymmp),
            "--subtitle-base-font-size",
            "40",
            "--reflow-v2",
        ],
    )
    assert code == 0
    out = capsys.readouterr().out.strip()
    parsed = json.loads(out.split("\n")[-1])
    op = parsed["stats"]["overflow_params"]
    assert op["subtitle_font_scale_source"] == "ymmp"
    assert op["subtitle_font_size"] == 60.0
    assert op["subtitle_base_font_size"] == 40.0
    assert op["subtitle_font_scale"] == 150.0
    assert op["effective_chars_per_line"] == 26

    rows = list(csv.reader(out_csv.open(encoding="utf-8-sig", newline="")))
    assert "\n" in rows[0][1]


def test_build_csv_wrap_px_uses_measured_reflow_stats(tmp_path, capsys) -> None:
    txt = tmp_path / "script.txt"
    txt.write_text(
        "[00:00] Host1: これは字幕実測幅のテストです。横幅指定では早めに改行します。\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "measured.csv"
    code = main(
        [
            "build-csv",
            str(txt),
            "-o",
            str(out_csv),
            "--format",
            "json",
            "--max-lines",
            "2",
            "--wrap-px",
            "32",
            "--wrap-safety",
            "1",
            "--measure-backend",
            "eaw",
            "--reflow-v2",
        ],
    )
    assert code == 0
    out = capsys.readouterr().out.strip()
    parsed = json.loads(out.split("\n")[-1])
    op = parsed["stats"]["overflow_params"]
    assert op["measure_backend"] == "eaw"
    assert op["wrap_px"] == 32.0
    assert op["wrap_safety"] == 1.0
    assert op["effective_wrap_px"] == 32.0

    rows = list(csv.reader(out_csv.open(encoding="utf-8-sig", newline="")))
    assert "\n" in rows[0][1]


def test_build_csv_wrap_px_can_use_wpf_measure_helper(tmp_path, capsys) -> None:
    helper = tmp_path / "fake_measure_wpf.py"
    helper.write_text(
        "#!/usr/bin/env python3\n"
        "import json\n"
        "import sys\n"
        "request = json.loads(sys.stdin.read())\n"
        "font_size = float(request['FontSize'])\n"
        "letter_spacing = float(request.get('LetterSpacing', 0.0))\n"
        "widths = []\n"
        "for text in request['Texts']:\n"
        "    widths.append(len(text) * font_size + max(0, len(text) - 1) * letter_spacing)\n"
        "print(json.dumps({'Widths': widths}))\n",
        encoding="utf-8",
    )
    helper.chmod(0o755)

    txt = tmp_path / "script.txt"
    txt.write_text(
        "[00:00] Host1: これはWPF計測経路のテストです。指定幅で折り返します。\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "measured_wpf.csv"
    code = main(
        [
            "build-csv",
            str(txt),
            "-o",
            str(out_csv),
            "--format",
            "json",
            "--max-lines",
            "2",
            "--wrap-px",
            "180",
            "--wrap-safety",
            "1",
            "--measure-backend",
            "wpf",
            "--measure-exe",
            str(helper),
            "--font-family",
            "FakeFont",
            "--font-size",
            "10",
            "--letter-spacing",
            "1",
            "--reflow-v2",
        ],
    )
    assert code == 0
    out = capsys.readouterr().out.strip()
    parsed = json.loads(out.split("\n")[-1])
    op = parsed["stats"]["overflow_params"]
    assert op["measure_backend"] == "wpf"
    assert op["measure_exe"] == str(helper)
    assert op["font_family"] == "FakeFont"
    assert op["font_size"] == 10.0
    assert op["letter_spacing"] == 1.0

    rows = list(csv.reader(out_csv.open(encoding="utf-8-sig", newline="")))
    assert "\n" in rows[0][1] or len(rows) > 1
