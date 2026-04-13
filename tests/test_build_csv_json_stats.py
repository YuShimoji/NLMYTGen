"""build-csv --format json が stats ペイロードを含むこと（GUI 表示用）。"""

import json

from src.cli.main import main


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
    assert st["overflow_params"]["max_display_lines"] == 2
    assert isinstance(st["overflow_candidates"], list)
