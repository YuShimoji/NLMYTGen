"""NLMYTGen CLI -- 単一エントリポイント。

Usage:
    python -m src.cli.main build-csv <input> [-o output.csv] [--speaker-map K1=V1,K2=V2] [--dry-run] [--stats]
    python -m src.cli.main validate <input>
    python -m src.cli.main inspect <input> [--speaker-map K1=V1,K2=V2]
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from src.pipeline.normalize import normalize
from src.pipeline.assemble_csv import assemble, find_unmapped_speakers
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


def _print_stats(output, file=sys.stdout):
    """話者ごとの発話統計を表示する。"""
    speaker_counts = Counter(row.speaker for row in output.rows)
    speaker_chars = Counter()
    for row in output.rows:
        speaker_chars[row.speaker] += len(row.text)

    print("--- Stats ---", file=file)
    for speaker in sorted(speaker_counts):
        count = speaker_counts[speaker]
        chars = speaker_chars[speaker]
        avg = chars // count if count else 0
        print(f"  {speaker}: {count} utterances, {chars} chars (avg {avg})", file=file)
    total_chars = sum(speaker_chars.values())
    print(f"  Total: {len(output.rows)} utterances, {total_chars} chars", file=file)


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

    # 未マッピング話者の警告 (assembly 前に実施)
    if speaker_map:
        unmapped = find_unmapped_speakers(script, speaker_map)
        for name in sorted(unmapped):
            print(f"[WARN] unmapped speaker: {name}", file=sys.stderr)

    output = assemble(script, speaker_map=speaker_map)

    # バリデーション
    results = validate(output)
    for r in results:
        prefix = "ERROR" if r.severity == Severity.ERROR else "WARN"
        print(f"[{prefix}] row {r.row_index}: {r.message}", file=sys.stderr)

    if has_errors(results):
        print("Validation errors found. CSV not written.", file=sys.stderr)
        return 1

    # 統計表示
    if getattr(args, "stats", False) or getattr(args, "dry_run", False):
        _print_stats(output)

    # dry-run: プレビューのみ
    if getattr(args, "dry_run", False):
        print("--- Preview (first 5 rows) ---")
        for row in output.rows[:5]:
            print(f"  {row.speaker},{row.text}")
        if len(output.rows) > 5:
            print(f"  ... ({len(output.rows) - 5} more rows)")
        print("(dry-run: CSV not written)")
        return 0

    # 書き出し
    output.write(output_path)
    print(f"Written: {output_path} ({len(output.rows)} rows)")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    """validate: 入力ファイルのパース + 出力検証。"""
    input_path = Path(args.input)

    script = normalize(input_path)
    print(f"OK: {len(script.utterances)} utterances parsed")

    speakers = sorted(set(u.speaker for u in script.utterances))
    print(f"Speakers: {', '.join(speakers)}")

    # handoff validation も実行
    output = assemble(script)
    results = validate(output)
    for r in results:
        prefix = "ERROR" if r.severity == Severity.ERROR else "WARN"
        print(f"[{prefix}] row {r.row_index}: {r.message}", file=sys.stderr)

    if has_errors(results):
        return 1
    return 0


def _cmd_inspect(args: argparse.Namespace) -> int:
    """inspect: 入力の詳細分析。マッピング結果のプレビュー。"""
    input_path = Path(args.input)
    speaker_map = _parse_speaker_map(args.speaker_map) if args.speaker_map else None

    script = normalize(input_path)

    print(f"Input: {input_path}")
    print(f"Utterances: {len(script.utterances)}")

    # 入力側の話者一覧
    input_speakers = sorted(set(u.speaker for u in script.utterances))
    print(f"Input speakers: {', '.join(input_speakers)}")

    if speaker_map:
        unmapped = find_unmapped_speakers(script, speaker_map)
        print("Speaker mapping:")
        for k, v in speaker_map.items():
            status = "(used)" if k in {u.speaker for u in script.utterances} else "(unused)"
            print(f"  {k} -> {v} {status}")
        if unmapped:
            print(f"Unmapped: {', '.join(sorted(unmapped))}")

    output = assemble(script, speaker_map=speaker_map)
    _print_stats(output)

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
    p_build.add_argument("--dry-run", action="store_true", help="Preview without writing")
    p_build.add_argument("--stats", action="store_true", help="Show speaker statistics")

    # validate
    p_validate = subparsers.add_parser("validate", help="Validate input file")
    p_validate.add_argument("input", help="Input file path (.txt or .csv)")

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Inspect input and preview mapping")
    p_inspect.add_argument("input", help="Input file path (.txt or .csv)")
    p_inspect.add_argument(
        "--speaker-map",
        help="Speaker name mapping (e.g., Host1=れいむ,Host2=まりさ)",
    )

    args = parser.parse_args(argv)

    try:
        if args.command == "build-csv":
            return _cmd_build_csv(args)
        elif args.command == "validate":
            return _cmd_validate(args)
        elif args.command == "inspect":
            return _cmd_inspect(args)
        else:
            parser.print_help()
            return 1
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
