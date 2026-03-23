"""NLMYTGen CLI -- 単一エントリポイント。

Usage:
    python -m src.cli.main build-csv <input> [-o output.csv] [--speaker-map K1=V1,K2=V2]
    python -m src.cli.main validate <input>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.pipeline.normalize import normalize
from src.pipeline.assemble_csv import assemble
from src.pipeline.validate_handoff import validate, has_errors, Severity


def _parse_speaker_map(raw: str) -> dict[str, str]:
    """'Host1=れいむ,Host2=まりさ' 形式の文字列を辞書に変換する。"""
    result: dict[str, str] = {}
    for pair in raw.split(","):
        pair = pair.strip()
        if "=" not in pair:
            continue
        key, value = pair.split("=", 1)
        key, value = key.strip(), value.strip()
        if key and value:
            result[key] = value
    return result


def _cmd_build_csv(args: argparse.Namespace) -> int:
    """build-csv: 入力ファイル → YMM4 CSV 生成。"""
    input_path = Path(args.input)

    # 出力パス決定
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_name(f"{input_path.stem}_ymm4.csv")

    # 話者マッピング
    speaker_map = _parse_speaker_map(args.speaker_map) if args.speaker_map else None

    # パイプライン実行
    script = normalize(input_path)
    output = assemble(script, speaker_map=speaker_map)

    # バリデーション
    results = validate(output, speaker_map=speaker_map)
    for r in results:
        prefix = "ERROR" if r.severity == Severity.ERROR else "WARN"
        print(f"[{prefix}] row {r.row_index}: {r.message}", file=sys.stderr)

    if has_errors(results):
        print("Validation errors found. CSV not written.", file=sys.stderr)
        return 1

    # 書き出し
    output.write(output_path)
    print(f"Written: {output_path} ({len(output.rows)} rows)")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    """validate: 入力ファイルの構文チェックのみ。"""
    input_path = Path(args.input)

    script = normalize(input_path)
    print(f"OK: {len(script.utterances)} utterances parsed")

    speakers = sorted(set(u.speaker for u in script.utterances))
    print(f"Speakers: {', '.join(speakers)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="nlmytgen",
        description="NotebookLM transcript to YMM4 CSV pipeline",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # build-csv
    p_build = subparsers.add_parser("build-csv", help="Build YMM4 CSV from input")
    p_build.add_argument("input", help="Input file path (.txt or .csv)")
    p_build.add_argument("-o", "--output", help="Output CSV path")
    p_build.add_argument(
        "--speaker-map",
        help="Speaker name mapping (e.g., Host1=れいむ,Host2=まりさ)",
    )

    # validate
    p_validate = subparsers.add_parser("validate", help="Validate input file")
    p_validate.add_argument("input", help="Input file path (.txt or .csv)")

    args = parser.parse_args(argv)

    try:
        if args.command == "build-csv":
            return _cmd_build_csv(args)
        elif args.command == "validate":
            return _cmd_validate(args)
        else:
            parser.print_help()
            return 1
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
