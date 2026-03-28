"""NLMYTGen CLI -- 単一エントリポイント。

Usage:
    python -m src.cli.main build-csv <input>... [-o output.csv] [--speaker-map K1=V1,K2=V2] [--dry-run] [--stats]
    python -m src.cli.main validate <input>
    python -m src.cli.main inspect <input> [--speaker-map K1=V1,K2=V2]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from src.pipeline.normalize import normalize
from src.pipeline.assemble_csv import assemble, find_unmapped_speakers
from src.pipeline.validate_handoff import validate, has_errors, Severity


def _parse_kv_pairs(lines: list[str]) -> dict[str, str]:
    """key=value ペアのリストを辞書に変換する。# コメントと空行をスキップ。"""
    result: dict[str, str] = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if key and value:
            result[key] = value
    return result


def _parse_speaker_map(raw: str) -> dict[str, str]:
    """'Host1=れいむ,Host2=まりさ' 形式の文字列を辞書に変換する。"""
    return _parse_kv_pairs(raw.split(","))


def _load_speaker_map_file(path: Path) -> dict[str, str]:
    """話者マッピングファイルを読み込む。JSON または key=value 形式。"""
    text = path.read_text(encoding="utf-8")

    if path.suffix.lower() == ".json":
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError(f"Speaker map JSON must be an object: {path}")
        return {str(k): str(v) for k, v in data.items()}

    return _parse_kv_pairs(text.splitlines())


def _resolve_speaker_map(args: argparse.Namespace) -> dict[str, str] | None:
    """--speaker-map と --speaker-map-file を統合する。"""
    result: dict[str, str] = {}

    if getattr(args, "speaker_map_file", None):
        result.update(_load_speaker_map_file(Path(args.speaker_map_file)))

    if getattr(args, "speaker_map", None):
        result.update(_parse_speaker_map(args.speaker_map))

    return result or None


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


def _build_one(input_path: Path, output_path: Path, args: argparse.Namespace) -> bool:
    """単一ファイルの build-csv 処理。成功なら True を返す。"""
    speaker_map = _resolve_speaker_map(args)
    unlabeled = getattr(args, "unlabeled", False)
    script = normalize(input_path, unlabeled=unlabeled)

    if speaker_map:
        unmapped = find_unmapped_speakers(script, speaker_map)
        for name in sorted(unmapped):
            print(f"[WARN] unmapped speaker: {name}", file=sys.stderr)

    merge = getattr(args, "merge_consecutive", False)
    output = assemble(script, speaker_map=speaker_map, merge_consecutive=merge)

    results = validate(output)
    for r in results:
        prefix = "ERROR" if r.severity == Severity.ERROR else "WARN"
        print(f"[{prefix}] row {r.row_index}: {r.message}", file=sys.stderr)

    if has_errors(results):
        print(f"Validation errors found. CSV not written: {input_path.name}", file=sys.stderr)
        return False

    if getattr(args, "stats", False) or getattr(args, "dry_run", False):
        _print_stats(output)

    if getattr(args, "dry_run", False):
        print("--- Preview (first 5 rows) ---")
        for row in output.rows[:5]:
            print(f"  {row.speaker},{row.text}")
        if len(output.rows) > 5:
            print(f"  ... ({len(output.rows) - 5} more rows)")
        print("(dry-run: CSV not written)")
        return True

    output.write(output_path)
    print(f"Written: {output_path} ({len(output.rows)} rows)")
    return True


def _cmd_build_csv(args: argparse.Namespace) -> int:
    """build-csv: 入力ファイル → YMM4 CSV 生成。複数ファイル対応。"""
    inputs = [Path(p) for p in args.input]

    if len(inputs) == 1:
        input_path = inputs[0]
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.with_name(f"{input_path.stem}_ymm4.csv")
        return 0 if _build_one(input_path, output_path, args) else 1

    # 複数ファイル
    if args.output:
        print("[WARN] -o is ignored with multiple inputs (each file gets {stem}_ymm4.csv)", file=sys.stderr)

    ok, fail = 0, 0
    for input_path in inputs:
        output_path = input_path.with_name(f"{input_path.stem}_ymm4.csv")
        print(f"--- {input_path.name} ---")
        try:
            if _build_one(input_path, output_path, args):
                ok += 1
            else:
                fail += 1
        except (ValueError, FileNotFoundError) as e:
            print(f"Error: {e}", file=sys.stderr)
            fail += 1

    print(f"\n=== Batch: {ok} succeeded, {fail} failed (of {len(inputs)} files) ===")
    return 1 if fail > 0 else 0


def _cmd_validate(args: argparse.Namespace) -> int:
    """validate: 入力ファイルのパース + 出力検証。"""
    input_path = Path(args.input)
    unlabeled = getattr(args, "unlabeled", False)

    script = normalize(input_path, unlabeled=unlabeled)
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
    speaker_map = _resolve_speaker_map(args)
    unlabeled = getattr(args, "unlabeled", False)

    script = normalize(input_path, unlabeled=unlabeled)

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


def _cmd_generate_map(args: argparse.Namespace) -> int:
    """generate-map: 入力ファイルから話者マッピングテンプレートを生成する。"""
    input_path = Path(args.input)
    unlabeled = getattr(args, "unlabeled", False)
    script = normalize(input_path, unlabeled=unlabeled)

    speakers = sorted(set(u.speaker for u in script.utterances))
    fmt = getattr(args, "format", "text")

    if fmt == "json":
        data = {s: s for s in speakers}
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("# Speaker map template")
        print(f"# Generated from: {input_path.name}")
        print(f"# Edit the values (right side of =) to YMM4 character names")
        for s in speakers:
            print(f"{s}={s}")

    return 0


def _add_speaker_map_args(parser: argparse.ArgumentParser) -> None:
    """--speaker-map / --speaker-map-file 引数を追加する。"""
    parser.add_argument(
        "--speaker-map",
        help="Speaker name mapping (e.g., Host1=れいむ,Host2=まりさ)",
    )
    parser.add_argument(
        "--speaker-map-file",
        help="Speaker map file (.json or key=value text)",
    )


def _add_unlabeled_arg(parser: argparse.ArgumentParser) -> None:
    """--unlabeled 引数を追加する。"""
    parser.add_argument(
        "--unlabeled", action="store_true",
        help="Treat input as unlabeled text (alternating Speaker_A/Speaker_B)",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="nlmytgen",
        description="NotebookLM transcript to YMM4 CSV pipeline",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # build-csv
    p_build = subparsers.add_parser("build-csv", help="Build YMM4 CSV from input")
    p_build.add_argument("input", nargs="+", help="Input file path(s) (.txt or .csv)")
    p_build.add_argument("-o", "--output", help="Output CSV path")
    _add_speaker_map_args(p_build)
    _add_unlabeled_arg(p_build)
    p_build.add_argument("--merge-consecutive", action="store_true",
                         help="Merge consecutive utterances from the same speaker")
    p_build.add_argument("--dry-run", action="store_true", help="Preview without writing")
    p_build.add_argument("--stats", action="store_true", help="Show speaker statistics")

    # validate
    p_validate = subparsers.add_parser("validate", help="Validate input file")
    p_validate.add_argument("input", help="Input file path (.txt or .csv)")
    _add_unlabeled_arg(p_validate)

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Inspect input and preview mapping")
    p_inspect.add_argument("input", help="Input file path (.txt or .csv)")
    _add_speaker_map_args(p_inspect)
    _add_unlabeled_arg(p_inspect)

    # generate-map
    p_genmap = subparsers.add_parser("generate-map", help="Generate speaker map template from input")
    p_genmap.add_argument("input", help="Input file path (.txt or .csv)")
    _add_unlabeled_arg(p_genmap)
    p_genmap.add_argument("--format", choices=["text", "json"], default="text",
                          help="Output format (default: text)")

    args = parser.parse_args(argv)

    try:
        if args.command == "build-csv":
            return _cmd_build_csv(args)
        elif args.command == "validate":
            return _cmd_validate(args)
        elif args.command == "inspect":
            return _cmd_inspect(args)
        elif args.command == "generate-map":
            return _cmd_generate_map(args)
        else:
            parser.print_help()
            return 1
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
