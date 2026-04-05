"""NLMYTGen CLI -- 単一エントリポイント。

Usage:
    python -m src.cli.main build-csv <input>... [-o output.csv] [--speaker-map K1=V1,K2=V2] [--dry-run] [--stats]
    python -m src.cli.main build-cue-packet <input> [-o packet.md] [--format markdown|json] [--bundle-dir DIR]
    python -m src.cli.main build-diagram-packet <input> [-o packet.md] [--format markdown|json] [--bundle-dir DIR]
    python -m src.cli.main patch-ymmp <ymmp> <ir-json> --face-map face.json --bg-map bg.json [-o patched.ymmp]
    python -m src.cli.main validate <input>
    python -m src.cli.main inspect <input> [--speaker-map K1=V1,K2=V2]
    python -m src.cli.main generate-map <input> [--unlabeled] [--format text|json]
    python -m src.cli.main fetch-topics <URL>... [-n 20] [--after YYYY-MM-DD] [--format text|json]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from src.pipeline.normalize import normalize, analyze_speaker_roles
from src.pipeline.cue_packet import build_cue_packet_payload, render_cue_packet_markdown
from src.pipeline.cue_proof import render_cue_workflow_proof
from src.pipeline.diagram_brief import build_diagram_brief_payload, render_diagram_brief_markdown
from src.pipeline.diagram_proof import render_diagram_workflow_proof
from src.pipeline.diagram_rerun import (
    render_diagram_baseline_notes_template,
    render_diagram_quickstart,
    render_diagram_rerun_diff_template,
    render_diagram_rerun_prompt,
)
from src.pipeline.assemble_csv import (
    assemble,
    balance_subtitle_lines,
    display_width,
    estimate_display_lines,
    find_unmapped_speakers,
    reflow_subtitles,
    reflow_subtitles_v2,
    split_long_utterances,
)
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


def _print_stats(output, chars_per_line: int = 0, max_display_lines: int = 0, file=sys.stdout):
    """話者ごとの発話統計を表示する。

    chars_per_line > 0 かつ max_display_lines > 0 のとき、
    推定行数が max_display_lines を超える行をはみ出し候補として警告する。
    """
    speaker_counts = Counter(row.speaker for row in output.rows)
    speaker_chars = Counter()
    for row in output.rows:
        speaker_chars[row.speaker] += len(row.text.replace("\n", ""))

    print("--- Stats ---", file=file)
    for speaker in sorted(speaker_counts):
        count = speaker_counts[speaker]
        chars = speaker_chars[speaker]
        avg = chars // count if count else 0
        print(f"  {speaker}: {count} utterances, {chars} chars (avg {avg})", file=file)
    total_chars = sum(speaker_chars.values())
    print(f"  Total: {len(output.rows)} utterances, {total_chars} chars", file=file)

    if chars_per_line > 0 and max_display_lines > 0:
        overflow = []
        for i, row in enumerate(output.rows):
            w = display_width(row.text)
            lines = estimate_display_lines(row.text, chars_per_line)
            if lines > max_display_lines:
                overflow.append((i + 1, row.speaker, lines, w))
        if overflow:
            print(f"--- Overflow candidates (>{max_display_lines} lines at {chars_per_line} chars/line) ---", file=file)
            for row_num, speaker, lines, w in overflow:
                print(f"  [WARN] row {row_num}: {speaker}, 推定{lines}行 (display_width={w})", file=file)
        else:
            print(f"--- No overflow candidates (all within {max_display_lines} lines at {chars_per_line} chars/line) ---", file=file)


def _build_one(
    input_path: Path,
    output_path: Path,
    args: argparse.Namespace,
    *,
    json_result: dict | None = None,
) -> bool:
    """単一ファイルの build-csv 処理。成功なら True を返す。

    json_result が渡された場合、結果データをそこに書き込む。
    """
    speaker_map = _resolve_speaker_map(args)
    unlabeled = getattr(args, "unlabeled", False)
    script = normalize(input_path, unlabeled=unlabeled)

    if speaker_map:
        unmapped = find_unmapped_speakers(script, speaker_map)
        for name in sorted(unmapped):
            print(f"[WARN] unmapped speaker: {name}", file=sys.stderr)

    merge = getattr(args, "merge_consecutive", False)
    output = assemble(script, speaker_map=speaker_map, merge_consecutive=merge)

    max_lines = getattr(args, "max_lines", None)
    max_length = getattr(args, "max_length", None)
    use_dw = getattr(args, "display_width", False)
    chars_per_line = getattr(args, "chars_per_line", 40)
    balance_lines = getattr(args, "balance_lines", False)
    reflow_v2 = getattr(args, "reflow_v2", False)

    if max_lines:
        if reflow_v2:
            output = reflow_subtitles_v2(
                output,
                chars_per_line=chars_per_line,
                max_lines=max_lines,
            )
        elif balance_lines:
            output = reflow_subtitles_v2(
                output,
                chars_per_line=chars_per_line,
                max_lines=max_lines,
            )
        else:
            effective_max = chars_per_line * max_lines
            output = split_long_utterances(output, max_length=effective_max, use_display_width=True)
    elif max_length:
        output = split_long_utterances(output, max_length=max_length, use_display_width=use_dw)

    results = validate(output)
    for r in results:
        prefix = "ERROR" if r.severity == Severity.ERROR else "WARN"
        print(f"[{prefix}] row {r.row_index}: {r.message}", file=sys.stderr)

    if has_errors(results):
        print(f"Validation errors found. CSV not written: {input_path.name}", file=sys.stderr)
        if json_result is not None:
            json_result.update({"success": False, "error": "validation_errors"})
        return False

    if getattr(args, "stats", False) or getattr(args, "dry_run", False):
        stats_cpl = chars_per_line if (use_dw or max_lines) else 0
        stats_lines = max_lines if max_lines else (2 if (use_dw or max_lines) else 0)
        _print_stats(output, chars_per_line=stats_cpl, max_display_lines=stats_lines)

    if getattr(args, "dry_run", False):
        print("--- Preview (first 5 rows) ---")
        for row in output.rows[:5]:
            print(f"  {row.speaker},{row.text}")
        if len(output.rows) > 5:
            print(f"  ... ({len(output.rows) - 5} more rows)")
        print("(dry-run: CSV not written)")
        if json_result is not None:
            json_result.update({
                "success": True, "dry_run": True,
                "rows": len(output.rows),
                "speakers": dict(Counter(r.speaker for r in output.rows)),
            })
        return True

    output.write(output_path)
    print(f"Written: {output_path} ({len(output.rows)} rows)")

    if json_result is not None:
        json_result.update({
            "success": True,
            "output": str(output_path),
            "rows": len(output.rows),
            "speakers": dict(Counter(r.speaker for r in output.rows)),
        })
    return True


def _cmd_build_csv(args: argparse.Namespace) -> int:
    """build-csv: 入力ファイル → YMM4 CSV 生成。複数ファイル対応。"""
    inputs = [Path(p) for p in args.input]
    fmt = getattr(args, "format", "text")

    if getattr(args, "balance_lines", False) and not args.max_lines:
        raise ValueError("--balance-lines requires --max-lines")

    if len(inputs) == 1:
        input_path = inputs[0]
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.with_name(f"{input_path.stem}_ymm4.csv")
        jr: dict | None = {"input": str(input_path)} if fmt == "json" else None
        success = _build_one(input_path, output_path, args, json_result=jr)
        if fmt == "json":
            print(json.dumps(jr, ensure_ascii=False))
        return 0 if success else 1

    # 複数ファイル
    if args.output:
        print("[WARN] -o is ignored with multiple inputs (each file gets {stem}_ymm4.csv)", file=sys.stderr)

    ok, fail = 0, 0
    results_list = []
    for input_path in inputs:
        output_path = input_path.with_name(f"{input_path.stem}_ymm4.csv")
        if fmt != "json":
            print(f"--- {input_path.name} ---")
        try:
            success = _build_one(input_path, output_path, args)
            if success:
                ok += 1
            else:
                fail += 1
            if fmt == "json":
                results_list.append({
                    "input": str(input_path),
                    "output": str(output_path),
                    "success": success,
                })
        except (ValueError, FileNotFoundError) as e:
            if fmt != "json":
                print(f"Error: {e}", file=sys.stderr)
            fail += 1
            if fmt == "json":
                results_list.append({
                    "input": str(input_path),
                    "output": None,
                    "success": False,
                    "error": str(e),
                })

    if fmt == "json":
        print(json.dumps({"batch": results_list, "ok": ok, "fail": fail}, ensure_ascii=False))
    else:
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

    # ロール推定（--unlabeled 時に特に有用）
    if unlabeled:
        roles = analyze_speaker_roles(script)
        print("Speaker role analysis:")
        role_labels = {"host": "host (introduces topics, longer explanations)",
                       "guest": "guest (questions, short responses, reactions)",
                       "unknown": "unknown"}
        for sp in input_speakers:
            r = roles[sp]
            role_desc = role_labels.get(r["role"], r["role"])
            print(f"  {sp}: {role_desc}")
            print(f"    {r['utterances']} utterances, avg {r['avg_length']:.0f} chars")
            print(f"    short responses: {r['short_responses']}, questions: {r['questions']}, topic intros: {r['topic_intros']}")

        # speaker-map の推奨順序を提示
        host_sp = next((sp for sp in input_speakers if roles[sp]["role"] == "host"), None)
        guest_sp = next((sp for sp in input_speakers if roles[sp]["role"] == "guest"), None)
        if host_sp and guest_sp and not speaker_map:
            print(f"\nRecommended --speaker-map (host={host_sp}, guest={guest_sp}):")
            print(f"  To map host to character A and guest to character B:")
            print(f"  --speaker-map \"{host_sp}=<charA>,{guest_sp}=<charB>\"")

    output = assemble(script, speaker_map=speaker_map)
    _print_stats(output)

    return 0


def _cmd_fetch_topics(args: argparse.Namespace) -> int:
    """fetch-topics: RSS/Atom フィードからトピック候補を取得する。"""
    from datetime import date
    from src.feed.fetch import fetch_feed

    after_date: str | None = None
    if getattr(args, "after", None):
        try:
            date.fromisoformat(args.after)
            after_date = args.after
        except ValueError:
            print(f"Error: invalid date format: {args.after} (expected YYYY-MM-DD)", file=sys.stderr)
            return 1

    all_entries = []
    for url in args.urls:
        try:
            entries = fetch_feed(url, timeout=args.timeout)
        except (ValueError, OSError) as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)
            continue
        all_entries.extend(entries)

    if after_date:
        all_entries = [e for e in all_entries if e.published and e.published >= after_date]

    all_entries = all_entries[:args.limit]

    if not all_entries:
        print("No entries found.", file=sys.stderr)
        return 0

    fmt = getattr(args, "format", "text")
    output_lines: list[str] = []

    if fmt == "json":
        data = [
            {"title": e.title, "published": e.published, "source": e.source_url}
            for e in all_entries
        ]
        output_lines.append(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        seen_sources: set[str | None] = set()
        for entry in all_entries:
            if entry.source_url not in seen_sources:
                seen_sources.add(entry.source_url)
                today = date.today().isoformat()
                output_lines.append(f"# Source: {entry.source_url} ({today})")
            output_lines.append(entry.title)

    text = "\n".join(output_lines) + "\n"

    if getattr(args, "output", None):
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"Written: {out_path} ({len(all_entries)} entries)")
    else:
        sys.stdout.write(text)

    return 0


def _cmd_generate_map(args: argparse.Namespace) -> int:
    """generate-map: 入力ファイルから話者マッピングテンプレートを生成する。"""
    input_path = Path(args.input)
    unlabeled = getattr(args, "unlabeled", False)
    script = normalize(input_path, unlabeled=unlabeled)

    speakers = sorted(set(u.speaker for u in script.utterances))
    fmt = getattr(args, "format", "text")

    # ロール推定（--unlabeled 時）
    roles = analyze_speaker_roles(script) if unlabeled else {}

    if fmt == "json":
        data = {s: s for s in speakers}
        if roles:
            data["_roles"] = {s: roles[s]["role"] for s in speakers}
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("# Speaker map template")
        print(f"# Generated from: {input_path.name}")
        print(f"# Edit the values (right side of =) to YMM4 character names")
        if roles:
            for s in speakers:
                role = roles[s]["role"]
                hint = "host: longer explanations, topic intros" if role == "host" else "guest: short responses, questions"
                print(f"# {s} = {hint}")
        for s in speakers:
            print(f"{s}={s}")

    return 0


def _cmd_build_cue_packet(args: argparse.Namespace) -> int:
    """build-cue-packet: 外部 LLM/Automation 用の cue memo packet を生成する。"""
    input_path = Path(args.input)
    script = normalize(input_path, unlabeled=getattr(args, "unlabeled", False))
    speaker_map = _resolve_speaker_map(args)

    payload = build_cue_packet_payload(
        script,
        source_name=input_path.name,
        speaker_map=speaker_map,
    )

    fmt = getattr(args, "format", "markdown")
    bundle_dir_raw = getattr(args, "bundle_dir", None)

    if bundle_dir_raw:
        bundle_dir = Path(bundle_dir_raw)
        bundle_dir.mkdir(parents=True, exist_ok=True)
        stem = input_path.stem
        md_path = bundle_dir / f"{stem}_cue_packet.md"
        json_path = bundle_dir / f"{stem}_cue_packet.json"
        proof_path = bundle_dir / f"{stem}_cue_workflow_proof.md"

        packet_markdown = render_cue_packet_markdown(payload)
        packet_json = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        packet_command = f"python -m src.cli.main build-cue-packet {input_path}"
        proof_text = render_cue_workflow_proof(
            source_name=input_path.name,
            packet_markdown_name=md_path.name,
            packet_json_name=json_path.name,
            packet_command=packet_command,
            payload=payload,
        )

        md_path.write_text(packet_markdown, encoding="utf-8")
        json_path.write_text(packet_json, encoding="utf-8")
        if not proof_path.exists():
            proof_path.write_text(proof_text, encoding="utf-8")
        print(f"Written bundle: {md_path}, {json_path}, {proof_path}")
        return 0

    if fmt == "json":
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    else:
        text = render_cue_packet_markdown(payload)

    if getattr(args, "output", None):
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"Written: {out_path}")
    else:
        sys.stdout.write(text)

    return 0


def _cmd_build_diagram_packet(args: argparse.Namespace) -> int:
    """build-diagram-packet: 外部 LLM/Automation 用の diagram brief packet を生成する。"""
    input_path = Path(args.input)
    script = normalize(input_path, unlabeled=getattr(args, "unlabeled", False))
    speaker_map = _resolve_speaker_map(args)

    payload = build_diagram_brief_payload(
        script,
        source_name=input_path.name,
        speaker_map=speaker_map,
    )

    fmt = getattr(args, "format", "markdown")
    bundle_dir_raw = getattr(args, "bundle_dir", None)

    if bundle_dir_raw:
        bundle_dir = Path(bundle_dir_raw)
        bundle_dir.mkdir(parents=True, exist_ok=True)
        stem = input_path.stem
        md_path = bundle_dir / f"{stem}_diagram_packet.md"
        json_path = bundle_dir / f"{stem}_diagram_packet.json"
        proof_path = bundle_dir / f"{stem}_diagram_workflow_proof.md"
        rerun_prompt_path = bundle_dir / f"{stem}_diagram_rerun_prompt.txt"
        rerun_diff_path = bundle_dir / f"{stem}_diagram_rerun_diff_template.md"
        quickstart_path = bundle_dir / f"{stem}_diagram_quickstart.md"
        baseline_notes_path = bundle_dir / f"{stem}_diagram_baseline_notes.md"

        packet_markdown = render_diagram_brief_markdown(payload)
        packet_json = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        packet_command = f"python -m src.cli.main build-diagram-packet {input_path}"
        proof_text = render_diagram_workflow_proof(
            source_name=input_path.name,
            packet_markdown_name=md_path.name,
            packet_json_name=json_path.name,
            packet_command=packet_command,
            payload=payload,
        )
        rerun_prompt_text = render_diagram_rerun_prompt()
        rerun_diff_text = render_diagram_rerun_diff_template()
        baseline_notes_text = render_diagram_baseline_notes_template(
            target_diagram_count=payload["response_preferences"]["target_diagram_count"],
            section_seeds=payload["context"].get("section_seeds"),
        )
        quickstart_text = render_diagram_quickstart(
            packet_name=md_path.name,
            rerun_prompt_name=rerun_prompt_path.name,
            diff_template_name=rerun_diff_path.name,
            proof_log_name=proof_path.name,
            baseline_notes_name=baseline_notes_path.name if baseline_notes_path.exists() else None,
        )

        md_path.write_text(packet_markdown, encoding="utf-8")
        json_path.write_text(packet_json, encoding="utf-8")
        if not proof_path.exists():
            proof_path.write_text(proof_text, encoding="utf-8")
        if not baseline_notes_path.exists():
            baseline_notes_path.write_text(baseline_notes_text, encoding="utf-8")
        rerun_prompt_path.write_text(rerun_prompt_text, encoding="utf-8")
        rerun_diff_path.write_text(rerun_diff_text, encoding="utf-8")
        quickstart_path.write_text(quickstart_text, encoding="utf-8")
        print(
            "Written bundle: "
            f"{md_path}, {json_path}, {proof_path}, {rerun_prompt_path}, "
            f"{rerun_diff_path}, {quickstart_path}, {baseline_notes_path}"
        )
        return 0

    if fmt == "json":
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    else:
        text = render_diagram_brief_markdown(payload)

    if getattr(args, "output", None):
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"Written: {out_path}")
    else:
        sys.stdout.write(text)

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
    p_build.add_argument("--max-length", type=int, metavar="N",
                         help="Split utterances longer than N chars at sentence boundaries")
    p_build.add_argument("--display-width", action="store_true",
                         help="Use display width (fullwidth=2, halfwidth=1) for --max-length")
    p_build.add_argument("--max-lines", type=int, metavar="N",
                         help="Split to fit within N display lines (uses --chars-per-line)")
    p_build.add_argument("--chars-per-line", type=int, default=40, metavar="N",
                         help="Display width per line for --max-lines (default: 40)")
    p_build.add_argument("--balance-lines", action="store_true",
                         help="Insert a natural line break for 2-line subtitles (requires --max-lines)")
    p_build.add_argument("--reflow-v2", action="store_true",
                         help="Use v2 reflow algorithm (balanced page+line splitting, requires --max-lines)")
    p_build.add_argument("--dry-run", action="store_true", help="Preview without writing")
    p_build.add_argument("--stats", action="store_true", help="Show speaker statistics")
    p_build.add_argument("--format", choices=["text", "json"], default="text",
                         help="Output format for results (default: text)")

    # validate
    p_validate = subparsers.add_parser("validate", help="Validate input file")
    p_validate.add_argument("input", help="Input file path (.txt or .csv)")
    _add_unlabeled_arg(p_validate)

    # build-cue-packet
    p_cue = subparsers.add_parser(
        "build-cue-packet",
        help="Build a text-only cue packet for external LLM/Automation",
    )
    p_cue.add_argument("input", help="Input file path (.txt or .csv)")
    p_cue.add_argument("-o", "--output", help="Output packet path (default: stdout)")
    p_cue.add_argument("--format", choices=["markdown", "json"], default="markdown",
                       help="Packet format (default: markdown)")
    p_cue.add_argument("--bundle-dir",
                       help="Write packet markdown/json plus a workflow-proof template into DIR")
    _add_speaker_map_args(p_cue)
    _add_unlabeled_arg(p_cue)

    # build-diagram-packet
    p_diagram = subparsers.add_parser(
        "build-diagram-packet",
        help="Build a text-only diagram brief packet for external LLM/Automation",
    )
    p_diagram.add_argument("input", help="Input file path (.txt or .csv)")
    p_diagram.add_argument("-o", "--output", help="Output packet path (default: stdout)")
    p_diagram.add_argument("--format", choices=["markdown", "json"], default="markdown",
                           help="Packet format (default: markdown)")
    p_diagram.add_argument("--bundle-dir",
                           help="Write packet markdown/json plus a workflow-proof template into DIR")
    _add_speaker_map_args(p_diagram)
    _add_unlabeled_arg(p_diagram)

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Inspect input and preview mapping")
    p_inspect.add_argument("input", help="Input file path (.txt or .csv)")
    _add_speaker_map_args(p_inspect)
    _add_unlabeled_arg(p_inspect)

    # fetch-topics
    p_fetch = subparsers.add_parser("fetch-topics", help="Fetch topic candidates from RSS/Atom feeds")
    p_fetch.add_argument("urls", nargs="+", metavar="URL", help="RSS/Atom feed URL(s)")
    p_fetch.add_argument("-o", "--output", help="Output file path (default: stdout)")
    p_fetch.add_argument("-n", "--limit", type=int, default=20, help="Max entries to show (default: 20)")
    p_fetch.add_argument("--after", metavar="YYYY-MM-DD", help="Only entries published after this date")
    p_fetch.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")
    p_fetch.add_argument("--timeout", type=int, default=10, help="HTTP timeout in seconds (default: 10)")

    # generate-map
    p_genmap = subparsers.add_parser("generate-map", help="Generate speaker map template from input")
    p_genmap.add_argument("input", help="Input file path (.txt or .csv)")
    _add_unlabeled_arg(p_genmap)
    p_genmap.add_argument("--format", choices=["text", "json"], default="text",
                          help="Output format (default: text)")

    # extract-template
    p_extract = subparsers.add_parser(
        "extract-template",
        help="Extract face_map / bg_map from an existing ymmp",
    )
    p_extract.add_argument("ymmp", help="Input ymmp file path")
    p_extract.add_argument("-o", "--output-dir",
                           help="Output directory for face_map.json and bg_map.json")
    p_extract.add_argument("--format", choices=["json", "summary"], default="summary",
                           help="Output format (default: summary to stdout)")
    p_extract.add_argument("--labeled", action="store_true",
                           help="Use Remark field as IR label (character-scoped output)")

    # measure-timeline-routes
    p_measure = subparsers.add_parser(
        "measure-timeline-routes",
        help="Inspect motion / transition / bg_anim candidate routes in a ymmp",
    )
    p_measure.add_argument("ymmp", help="Input ymmp file path")
    p_measure.add_argument("-o", "--output", help="Output report path")
    p_measure.add_argument("--expect",
                           help="Expected route contract JSON (category -> [routes])")
    p_measure.add_argument("--profile",
                           help="Contract profile name inside --expect JSON")
    p_measure.add_argument("--format", choices=["text", "json"], default="text",
                           help="Output format (default: text)")

    # patch-ymmp
    p_patch = subparsers.add_parser(
        "patch-ymmp",
        help="Apply production IR to an existing ymmp (face + bg + slot patch)",
    )
    p_patch.add_argument("ymmp", help="Input ymmp file path")
    p_patch.add_argument("ir_json", help="Production IR JSON file path")
    p_patch.add_argument("--face-map", help="Face label → parts file path mapping (JSON)")
    p_patch.add_argument("--bg-map", help="BG label → image/video file path mapping (JSON)")
    p_patch.add_argument("--slot-map", help="Slot label -> x/y/zoom mapping (JSON or registry)")
    p_patch.add_argument("--overlay-map", help="Overlay label -> image asset mapping (JSON or registry)")
    p_patch.add_argument("--se-map", help="SE label -> audio asset mapping (JSON or registry)")
    p_patch.add_argument("-o", "--output", help="Output ymmp path (default: <input>_patched.ymmp)")
    p_patch.add_argument("--dry-run", action="store_true", help="Preview changes without writing")

    # apply-production
    p_apply = subparsers.add_parser(
        "apply-production",
        help="One-command S-6 pipeline: extract maps + patch ymmp",
    )
    p_apply.add_argument("production_ymmp", help="Production ymmp (CSV imported)")
    p_apply.add_argument("ir_json", help="Production IR JSON")
    p_apply.add_argument("--palette", help="Palette ymmp for face_map extraction")
    p_apply.add_argument("--face-map", help="Pre-built face_map.json (skip extraction)")
    p_apply.add_argument("--bg-map", help="BG label → file path mapping (JSON)")
    p_apply.add_argument("--slot-map", help="Slot label -> x/y/zoom mapping (JSON or registry)")
    p_apply.add_argument("--overlay-map", help="Overlay label -> image asset mapping (JSON or registry)")
    p_apply.add_argument("--se-map", help="SE label -> audio asset mapping (JSON or registry)")
    p_apply.add_argument("--refresh-maps", action="store_true",
                         help="Force re-extract face_map from palette even if file exists")
    p_apply.add_argument("--csv", help="CSV file for auto row_start/row_end annotation")
    p_apply.add_argument("--prompt-doc",
                         help="Prompt markdown for face contract drift check"
                              " (default: docs/S6-production-memo-prompt.md)")
    p_apply.add_argument("-o", "--output", help="Output ymmp path")
    p_apply.add_argument("--dry-run", action="store_true", help="Preview without writing")
    p_apply.add_argument("--format", choices=["text", "json"], default="text",
                         help="Output format for results (default: text)")

    # annotate-row-range
    p_annot = subparsers.add_parser(
        "annotate-row-range",
        help="Auto-annotate IR with row_start/row_end from CSV alignment",
    )
    p_annot.add_argument("ir_json", help="Production IR JSON")
    p_annot.add_argument("csv", help="YMM4 CSV file (build-csv output)")
    p_annot.add_argument("-o", "--output", help="Output IR JSON path")
    p_annot.add_argument("--force", action="store_true",
                         help="Overwrite existing row_start/row_end")
    p_annot.add_argument("--keep-existing", action="store_true",
                         help="Skip utterances with existing row_start/row_end")
    p_annot.add_argument("--dry-run", action="store_true",
                         help="Preview without writing")

    # validate-ir
    p_valir = subparsers.add_parser(
        "validate-ir",
        help="Check IR quality before apply-production (face distribution, unknown labels, etc.)",
    )
    p_valir.add_argument("ir_json", help="Production IR JSON")
    p_valir.add_argument("--face-map", help="face_map.json for unknown label check")
    p_valir.add_argument("--palette", help="Palette ymmp (alternative to --face-map)")
    p_valir.add_argument("--slot-map", help="Slot label -> x/y/zoom mapping (JSON or registry)")
    p_valir.add_argument("--overlay-map", help="Overlay label -> image asset mapping (JSON or registry)")
    p_valir.add_argument("--se-map", help="SE label -> audio asset mapping (JSON or registry)")
    p_valir.add_argument("--prompt-doc",
                         help="Prompt markdown for face contract drift check"
                              " (default: docs/S6-production-memo-prompt.md)")

    # score-evidence (H-04)
    p_score_ev = subparsers.add_parser(
        "score-evidence",
        help="H-04: Score evidence richness from brief + category scores",
    )
    p_score_ev.add_argument("brief", help="H-01 Packaging brief (JSON or Markdown)")
    p_score_ev.add_argument("--scores", required=True,
                            help="Category scores JSON: {\"number\": 3, \"anecdote\": 1, ...}")
    p_score_ev.add_argument("--format", choices=["json", "text"], default="text")

    # score-visual-density (H-03)
    p_score_vd = subparsers.add_parser(
        "score-visual-density",
        help="H-03: Score visual density from brief + category scores",
    )
    p_score_vd.add_argument("brief", help="H-01 Packaging brief (JSON or Markdown)")
    p_score_vd.add_argument("--scores", required=True,
                            help="Category scores JSON: {\"scene_variety\": 2, ...}")
    p_score_vd.add_argument("--format", choices=["json", "text"], default="text")

    args = parser.parse_args(argv)

    try:
        if args.command == "build-csv":
            return _cmd_build_csv(args)
        elif args.command == "validate":
            return _cmd_validate(args)
        elif args.command == "build-cue-packet":
            return _cmd_build_cue_packet(args)
        elif args.command == "build-diagram-packet":
            return _cmd_build_diagram_packet(args)
        elif args.command == "inspect":
            return _cmd_inspect(args)
        elif args.command == "generate-map":
            return _cmd_generate_map(args)
        elif args.command == "fetch-topics":
            return _cmd_fetch_topics(args)
        elif args.command == "extract-template":
            return _cmd_extract_template(args)
        elif args.command == "measure-timeline-routes":
            return _cmd_measure_timeline_routes(args)
        elif args.command == "patch-ymmp":
            return _cmd_patch_ymmp(args)
        elif args.command == "apply-production":
            return _cmd_apply_production(args)
        elif args.command == "annotate-row-range":
            return _cmd_annotate_row_range(args)
        elif args.command == "validate-ir":
            return _cmd_validate_ir(args)
        elif args.command == "score-evidence":
            return _cmd_score_evidence(args)
        elif args.command == "score-visual-density":
            return _cmd_score_visual_density(args)
        else:
            parser.print_help()
            return 1
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _cmd_extract_template(args: argparse.Namespace) -> int:
    from src.pipeline.ymmp_patch import load_ymmp
    from src.pipeline.ymmp_extract import (
        extract_template,
        extract_template_labeled,
        generate_face_map,
        generate_face_map_labeled,
        generate_bg_map,
        generate_bg_map_labeled,
    )

    ymmp_data = load_ymmp(args.ymmp)

    if args.labeled:
        return _cmd_extract_template_labeled(
            args, ymmp_data,
            extract_template_labeled,
            generate_face_map_labeled,
            generate_bg_map_labeled,
        )

    result = extract_template(ymmp_data)

    face_map = generate_face_map(result.face_patterns)
    bg_map = generate_bg_map(result.bg_paths)

    if args.format == "summary" and not args.output_dir:
        print(f"Characters: {result.characters}")
        print(f"VoiceItems: {result.voice_item_count}")
        print(f"BG items: {result.bg_item_count}")
        print(f"\n--- Face patterns ({len(face_map)} unique) ---")
        for label, parts in face_map.items():
            print(f"  {label}:")
            for k, v in parts.items():
                print(f"    {k}: {Path(v).name}")
        print(f"\n--- BG paths ({len(bg_map)} unique) ---")
        for label, path in bg_map.items():
            print(f"  {label}: {Path(path).name}")
        print("\nTo export JSON files, add -o <output_dir>")
        return 0

    out_dir = Path(args.output_dir) if args.output_dir else Path(".")
    out_dir.mkdir(parents=True, exist_ok=True)

    face_path = out_dir / "face_map.json"
    with open(face_path, "w", encoding="utf-8") as f:
        json.dump(face_map, f, ensure_ascii=False, indent=2)
    print(f"face_map: {face_path} ({len(face_map)} patterns)")

    bg_path = out_dir / "bg_map.json"
    with open(bg_path, "w", encoding="utf-8") as f:
        json.dump(bg_map, f, ensure_ascii=False, indent=2)
    print(f"bg_map: {bg_path} ({len(bg_map)} paths)")

    print(f"\nNext step: rename JSON keys to IR labels (serious, smile, studio_blue, etc.)")
    return 0


def _cmd_measure_timeline_routes(args: argparse.Namespace) -> int:
    """Read-only ymmp inspection for motion / transition / bg_anim routes."""
    from src.pipeline.ymmp_patch import load_ymmp
    from src.pipeline.ymmp_measure import (
        measure_timeline_routes,
        render_timeline_measurement_text,
        validate_timeline_route_contract,
    )

    ymmp_data = load_ymmp(args.ymmp)
    measurement = measure_timeline_routes(ymmp_data)
    validation = None
    if getattr(args, "expect", None):
        with open(args.expect, "r", encoding="utf-8") as f:
            contract = json.load(f)
        validation = validate_timeline_route_contract(
            measurement,
            contract,
            profile=getattr(args, "profile", None),
        )

    if args.format == "json":
        payload = measurement.to_dict()
        if validation is not None:
            payload["validation"] = {
                "errors": validation.errors,
                "warnings": validation.warnings,
                "missing_routes": validation.missing_routes,
            }
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    else:
        text = render_timeline_measurement_text(measurement)
        if validation is not None:
            lines = [text.rstrip(), "", "--- Contract Check ---"]
            for msg in validation.errors:
                lines.append(f"  ERROR: {msg}")
            for msg in validation.warnings:
                lines.append(f"  WARNING: {msg}")
            text = "\n".join(lines) + "\n"

    if getattr(args, "output", None):
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"Written: {out_path}")
    else:
        sys.stdout.write(text)

    if validation is not None and validation.has_errors:
        return 1
    return 0


def _cmd_extract_template_labeled(
    args: argparse.Namespace,
    ymmp_data: dict,
    extract_fn,
    gen_face_fn,
    gen_bg_fn,
) -> int:
    """--labeled モードの extract-template."""
    result = extract_fn(ymmp_data)

    # Conflict (同キャラ・同ラベル・異パーツ) はエラー
    errors = [c for c in result.conflicts if c.startswith("Conflict:")]
    warnings = [c for c in result.conflicts if c.startswith("Warning:")]

    for w in warnings:
        print(f"  {w}", file=sys.stderr)

    if errors:
        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
        return 1

    face_map = gen_face_fn(result)
    bg_map = gen_bg_fn(result)

    total_faces = sum(len(labels) for labels in face_map.values())

    if args.format == "summary" and not args.output_dir:
        print(f"Characters: {result.characters}")
        print(f"\n--- Face patterns (character-scoped, {total_faces} total) ---")
        for char, labels in face_map.items():
            print(f"  {char}:")
            for label, parts in labels.items():
                parts_str = ", ".join(
                    f"{k}={Path(v).name}" for k, v in parts.items()
                )
                print(f"    {label}: {parts_str}")
        print(f"\n--- BG labels ({len(bg_map)}) ---")
        for label, path in bg_map.items():
            print(f"  {label}: {Path(path).name}")
        if total_faces == 0 and len(bg_map) == 0:
            print("\n0 patterns extracted. Set Remark on VoiceItem/ImageItem in YMM4.")
        return 0

    out_dir = Path(args.output_dir) if args.output_dir else Path(".")
    out_dir.mkdir(parents=True, exist_ok=True)

    face_path = out_dir / "face_map.json"
    with open(face_path, "w", encoding="utf-8") as f:
        json.dump(face_map, f, ensure_ascii=False, indent=2)
    print(f"face_map: {face_path} (character-scoped, {total_faces} patterns)")

    bg_path = out_dir / "bg_map.json"
    with open(bg_path, "w", encoding="utf-8") as f:
        json.dump(bg_map, f, ensure_ascii=False, indent=2)
    print(f"bg_map: {bg_path} ({len(bg_map)} labels)")

    return 0


def _cmd_patch_ymmp(args: argparse.Namespace) -> int:
    from src.pipeline.ymmp_patch import load_ymmp, load_ir, save_ymmp, patch_ymmp

    ymmp_data = load_ymmp(args.ymmp)
    ir_data = load_ir(args.ir_json)

    face_map: dict[str, dict[str, str]] = {}
    if args.face_map:
        with open(args.face_map, "r", encoding="utf-8") as f:
            face_map = json.load(f)

    bg_map: dict[str, str] = {}
    if args.bg_map:
        with open(args.bg_map, "r", encoding="utf-8") as f:
            bg_map = json.load(f)

    slot_map: dict[str, dict | None] = {}
    char_default_slots: dict[str, str] = {}
    if args.slot_map:
        slot_map, char_default_slots = _load_slot_contract(args.slot_map)
        print(f"slot_map: {args.slot_map} ({len(slot_map)} labels)")

    overlay_map: dict[str, dict] = {}
    if args.overlay_map:
        overlay_map = _load_labeled_asset_map(args.overlay_map, "overlays")
        print(f"overlay_map: {args.overlay_map} ({len(overlay_map)} labels)")

    se_map: dict[str, dict] = {}
    if args.se_map:
        se_map = _load_labeled_asset_map(args.se_map, "se")
        print(f"se_map: {args.se_map} ({len(se_map)} labels)")

    result = patch_ymmp(
        ymmp_data,
        ir_data,
        face_map,
        bg_map,
        slot_map=slot_map,
        char_default_slots=char_default_slots,
        overlay_map=overlay_map,
        se_map=se_map,
    )

    print(f"Face changes: {result.face_changes}")
    print(f"Slot changes: {result.slot_changes}")
    print(f"Overlay changes: {result.overlay_changes}")
    print(f"SE plans: {result.se_plans}")
    print(f"BG removed: {result.bg_changes}, BG added: {result.bg_additions}")
    if result.warnings:
        for w in result.warnings:
            print(f"  Warning: {w}", file=sys.stderr)

    fatal_warnings = _fatal_face_patch_warnings(result.warnings or [])
    if fatal_warnings:
        print(
            f"\nPatch FAILED ({len(fatal_warnings)} blocking issues)."
            " Partial output was not accepted.",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print("(dry-run: no file written)")
        return 0

    out_path = args.output
    if not out_path:
        stem = Path(args.ymmp).stem
        out_path = str(Path(args.ymmp).parent / f"{stem}_patched.ymmp")
    save_ymmp(ymmp_data, out_path)
    print(f"Written: {out_path}")
    return 0


def _get_known_face_labels(face_map: dict) -> set[str]:
    """face_map から既知の face ラベルを抽出する."""
    labels: set[str] = set()
    for key, value in face_map.items():
        if isinstance(value, dict):
            if all(isinstance(v, str) for v in value.values()):
                labels.add(key)  # flat map
            else:
                labels.update(value.keys())  # char-scoped map
    return labels


def _get_char_face_map(face_map: dict) -> dict[str, set[str]] | None:
    """face_map からキャラ別の face ラベル集合を抽出する.

    character-scoped map の場合のみ有効。flat map の場合は None を返す。
    """
    char_map: dict[str, set[str]] = {}
    for key, value in face_map.items():
        if isinstance(value, dict):
            if all(isinstance(v, str) for v in value.values()):
                return None  # flat map -- キャラ別チェック不可
            else:
                char_map[key] = set(value.keys())
    return char_map if char_map else None


def _load_slot_contract(
    path: str | Path,
) -> tuple[dict[str, dict | None], dict[str, str]]:
    """slot_map または registry 互換 JSON から slot 契約を読む."""
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, dict):
        raise ValueError("slot_map JSON must be an object")

    slot_map_raw = raw.get("slots") if isinstance(raw.get("slots"), dict) else raw
    if not isinstance(slot_map_raw, dict):
        raise ValueError("slot_map JSON must define a top-level object or 'slots'")

    slot_map: dict[str, dict | None] = {}
    for label, value in slot_map_raw.items():
        if value is None or isinstance(value, dict):
            slot_map[str(label)] = value
        else:
            raise ValueError(
                f"slot_map entry '{label}' must be an object or null"
            )

    char_default_slots: dict[str, str] = {}
    characters = raw.get("characters")
    if isinstance(characters, dict):
        for char, spec in characters.items():
            if not isinstance(spec, dict):
                continue
            default_slot = spec.get("default_slot")
            if isinstance(default_slot, str) and default_slot:
                char_default_slots[str(char)] = default_slot

    return slot_map, char_default_slots


def _load_labeled_asset_map(
    path: str | Path,
    section_name: str,
) -> dict[str, dict]:
    """Load overlay/se registry entries from either sectioned or flat JSON."""
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, dict):
        raise ValueError(f"{section_name} JSON must be an object")

    asset_raw = raw.get(section_name) if isinstance(raw.get(section_name), dict) else raw
    if not isinstance(asset_raw, dict):
        raise ValueError(
            f"{section_name} JSON must define a top-level object or '{section_name}'"
        )

    asset_map: dict[str, dict] = {}
    for label, value in asset_raw.items():
        if isinstance(value, str):
            asset_map[str(label)] = {"path": value}
            continue
        if isinstance(value, dict):
            asset_map[str(label)] = dict(value)
            continue
        raise ValueError(
            f"{section_name} entry '{label}' must be a string path or object"
        )
    return asset_map


def _default_prompt_doc_path() -> Path:
    """repo-local の既定 prompt doc パスを返す."""
    return Path(__file__).resolve().parents[2] / "docs" / "S6-production-memo-prompt.md"


def _load_prompt_face_contract(prompt_doc: str | None) -> tuple[set[str] | None, Path | None]:
    """prompt doc から face 契約ラベルを読み込む."""
    from src.pipeline.ir_validate import load_prompt_face_labels

    path = Path(prompt_doc) if prompt_doc else _default_prompt_doc_path()
    if not path.exists():
        return None, None

    labels = load_prompt_face_labels(path)
    if not labels:
        return None, path
    return labels, path


def _fatal_face_patch_warnings(warnings: list[str]) -> list[str]:
    """partial patch を許容しない face failure class を抽出する."""
    fatal_prefixes = (
        "FACE_MAP_MISS:",
        "IDLE_FACE_MAP_MISS:",
        "VOICE_NO_TACHIE_FACE:",
        "ROW_RANGE_MISSING:",
        "ROW_RANGE_INVALID:",
        "OVERLAY_MAP_MISS:",
        "OVERLAY_NO_TIMING_ANCHOR:",
        "OVERLAY_SPEC_INVALID:",
        "SE_MAP_MISS:",
        "SE_NO_TIMING_ANCHOR:",
        "SE_SPEC_INVALID:",
        "SE_WRITE_ROUTE_UNSUPPORTED:",
        "SLOT_CHARACTER_DRIFT:",
        "SLOT_DEFAULT_DRIFT:",
        "SLOT_REGISTRY_MISS:",
        "SLOT_NO_TACHIE_ITEM:",
        "SLOT_VALUE_INVALID:",
    )
    return [
        warning
        for warning in warnings
        if warning.startswith(fatal_prefixes)
    ]


def _print_validation(vr) -> None:
    """IRValidationResult を表示する."""
    from src.pipeline.ir_validate import IRValidationResult
    # face distribution
    if vr.face_distribution:
        total = sum(vr.face_distribution.values())
        print(f"\n--- Face Distribution ({total} utterances) ---")
        for label, count in sorted(
            vr.face_distribution.items(), key=lambda x: -x[1]
        ):
            pct = count * 100 // total
            bar = "#" * (pct // 5)
            print(f"  {label:12s} {count:3d} ({pct:2d}%) {bar}")

    if vr.prompt_face_labels or vr.palette_face_labels:
        print("\n--- Face Contract ---")
        if vr.prompt_face_labels:
            print(f"  prompt : {', '.join(vr.prompt_face_labels)}")
        if vr.palette_face_labels:
            print(f"  palette: {', '.join(vr.palette_face_labels)}")
        if vr.used_face_labels:
            print(f"  used   : {', '.join(vr.used_face_labels)}")
        if vr.used_idle_face_labels:
            print(f"  idle   : {', '.join(vr.used_idle_face_labels)}")

    if vr.slot_distribution:
        total_slots = sum(vr.slot_distribution.values())
        print(f"\n--- Slot Distribution ({total_slots} utterances) ---")
        for label, count in sorted(
            vr.slot_distribution.items(), key=lambda x: (-x[1], x[0])
        ):
            print(f"  {label:12s} {count:3d}")
        for char, labels in sorted(vr.character_slot_usage.items()):
            print(f"  {char}: {', '.join(labels)}")

    if vr.overlay_distribution:
        total_overlay = sum(vr.overlay_distribution.values())
        print(f"\n--- Overlay Distribution ({total_overlay} utterances) ---")
        for label, count in sorted(
            vr.overlay_distribution.items(), key=lambda x: (-x[1], x[0])
        ):
            print(f"  {label:12s} {count:3d}")

    if vr.se_distribution:
        total_se = sum(vr.se_distribution.values())
        print(f"\n--- SE Distribution ({total_se} utterances) ---")
        for label, count in sorted(
            vr.se_distribution.items(), key=lambda x: (-x[1], x[0])
        ):
            print(f"  {label:12s} {count:3d}")

    if vr.active_face_gaps or vr.latent_face_gaps:
        print("\n--- Palette Gap Report ---")
        for char, labels in sorted(vr.active_face_gaps.items()):
            print(f"  active {char}: {', '.join(labels)}")
        for char, labels in sorted(vr.latent_face_gaps.items()):
            print(f"  latent {char}: {', '.join(labels)}")

    for msg in vr.errors:
        print(f"  ERROR: {msg}", file=sys.stderr)
    for msg in vr.warnings:
        print(f"  WARNING: {msg}", file=sys.stderr)
    for msg in vr.info:
        print(f"  INFO: {msg}")


def _cmd_validate_ir(args: argparse.Namespace) -> int:
    """IR 品質 gate."""
    from src.pipeline.ymmp_patch import load_ir, load_ymmp
    from src.pipeline.ir_validate import validate_ir

    ir_data = load_ir(args.ir_json)

    known_labels = None
    char_face = None
    known_slots = None
    known_overlays = None
    known_se = None
    char_default_slots = None
    prompt_face_labels, prompt_doc_path = _load_prompt_face_contract(
        getattr(args, "prompt_doc", None)
    )
    if args.face_map:
        with open(args.face_map, "r", encoding="utf-8") as f:
            face_map = json.load(f)
        known_labels = _get_known_face_labels(face_map)
        char_face = _get_char_face_map(face_map)
    elif args.palette:
        from src.pipeline.ymmp_extract import (
            extract_template_labeled,
            generate_face_map_labeled,
        )
        palette_data = load_ymmp(args.palette)
        result = extract_template_labeled(palette_data)
        face_map = generate_face_map_labeled(result)
        known_labels = _get_known_face_labels(face_map)
        char_face = _get_char_face_map(face_map)
    if args.slot_map:
        slot_map, char_default_slots = _load_slot_contract(args.slot_map)
        known_slots = set(slot_map)
    if args.overlay_map:
        overlay_map = _load_labeled_asset_map(args.overlay_map, "overlays")
        known_overlays = set(overlay_map)
    if args.se_map:
        se_map = _load_labeled_asset_map(args.se_map, "se")
        known_se = set(se_map)

    if prompt_doc_path and prompt_face_labels:
        print(
            f"prompt face contract: {prompt_doc_path}"
            f" ({len(prompt_face_labels)} labels)"
        )
    if known_slots is not None:
        print(f"slot contract: {len(known_slots)} labels")
    if known_overlays is not None:
        print(f"overlay contract: {len(known_overlays)} labels")
    if known_se is not None:
        print(f"se contract: {len(known_se)} labels")

    vr = validate_ir(
        ir_data,
        known_labels,
        char_face_map=char_face,
        known_slot_labels=known_slots,
        known_overlay_labels=known_overlays,
        known_se_labels=known_se,
        char_default_slots=char_default_slots,
        prompt_face_labels=prompt_face_labels,
    )
    _print_validation(vr)

    if vr.has_errors:
        print(f"\nValidation FAILED ({len(vr.errors)} errors)")
        return 1
    elif vr.warnings:
        print(f"\nValidation PASSED with {len(vr.warnings)} warnings")
        return 0
    else:
        print("\nValidation PASSED")
        return 0


def _load_csv_rows(csv_path: str) -> list[list[str]]:
    """CSV を読み込んで [speaker, text] のリストを返す."""
    import csv as csv_mod
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        return list(csv_mod.reader(f))


def _cmd_annotate_row_range(args: argparse.Namespace) -> int:
    """IR に row_start/row_end を自動付与する."""
    from src.pipeline.ymmp_patch import load_ir
    from src.pipeline.row_range import annotate_row_range

    ir_data = load_ir(args.ir_json)
    csv_rows = _load_csv_rows(args.csv)

    result = annotate_row_range(
        ir_data, csv_rows,
        force=args.force,
        keep_existing=args.keep_existing,
    )

    utts = ir_data.get("utterances", [])
    print(f"Matched: {result.matched}/{len(utts)}")
    if result.unmatched_utterances:
        print(f"Unmatched: {result.unmatched_utterances}")
    if result.uncovered_rows:
        print(f"Uncovered rows: {len(result.uncovered_rows)}")
    if result.warnings:
        for w in result.warnings:
            print(f"  Warning: {w}", file=sys.stderr)

    # 既存 range error の場合は書き込まず終了
    if not result.matched and result.warnings:
        has_existing_error = any("existing row_start" in w for w in result.warnings)
        if has_existing_error:
            return 1

    if args.dry_run:
        # dry-run: 各 utterance の range を表示
        for u in utts:
            rs = u.get("row_start", "-")
            re_ = u.get("row_end", "-")
            print(f"  IR[{u.get('index', '?'):2}] rows {rs}-{re_}")
        print("(dry-run: no file written)")
        return 0

    out_path = args.output
    if not out_path:
        stem = Path(args.ir_json).stem
        out_path = str(Path(args.ir_json).parent / f"{stem}_annotated.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(ir_data, f, ensure_ascii=False, indent=2)
    print(f"Written: {out_path}")
    return 0



def _cmd_apply_production(args: argparse.Namespace) -> int:
    """S-6 ワンコマンド: extract-template → patch-ymmp をまとめて実行."""
    from src.pipeline.ymmp_patch import load_ymmp, load_ir, save_ymmp, patch_ymmp
    from src.pipeline.ymmp_extract import (
        extract_template_labeled,
        generate_face_map_labeled,
        generate_bg_map_labeled,
    )

    # --- face_map の解決 ---
    face_map: dict = {}
    if args.face_map and not args.refresh_maps:
        # 既存 face_map を使用
        with open(args.face_map, "r", encoding="utf-8") as f:
            face_map = json.load(f)
        print(f"face_map: {args.face_map} (loaded)")
    elif args.palette:
        # palette から抽出
        palette_data = load_ymmp(args.palette)
        extract_result = extract_template_labeled(palette_data)

        errors = [c for c in extract_result.conflicts if c.startswith("Conflict:")]
        warnings = [c for c in extract_result.conflicts if c.startswith("Warning:")]
        for w in warnings:
            print(f"  {w}", file=sys.stderr)
        if errors:
            for e in errors:
                print(f"  ERROR: {e}", file=sys.stderr)
            return 1

        face_map = generate_face_map_labeled(extract_result)
        total_faces = sum(len(v) for v in face_map.values())
        print(f"face_map: extracted from {args.palette} ({total_faces} patterns)")

        # face_map.json を palette と同じディレクトリに保存
        face_map_path = Path(args.palette).parent / "face_map.json"
        with open(face_map_path, "w", encoding="utf-8") as f:
            json.dump(face_map, f, ensure_ascii=False, indent=2)
        print(f"  saved: {face_map_path}")

        # bg_map も抽出して保存 (ラベル付き bg があれば)
        bg_map_labeled = generate_bg_map_labeled(extract_result)
        if bg_map_labeled:
            bg_map_path = Path(args.palette).parent / "bg_map.json"
            with open(bg_map_path, "w", encoding="utf-8") as f:
                json.dump(bg_map_labeled, f, ensure_ascii=False, indent=2)
            print(f"  bg_map: {bg_map_path} ({len(bg_map_labeled)} labels)")
    else:
        print("Warning: no --palette or --face-map specified. "
              "Face changes will be skipped.", file=sys.stderr)

    # --- bg_map の解決 ---
    bg_map: dict[str, str] = {}
    if args.bg_map:
        with open(args.bg_map, "r", encoding="utf-8") as f:
            bg_map = json.load(f)

    slot_map: dict[str, dict | None] = {}
    char_default_slots: dict[str, str] = {}
    if args.slot_map:
        slot_map, char_default_slots = _load_slot_contract(args.slot_map)
        print(f"slot_map: {args.slot_map} ({len(slot_map)} labels)")

    overlay_map: dict[str, dict] = {}
    if args.overlay_map:
        overlay_map = _load_labeled_asset_map(args.overlay_map, "overlays")
        print(f"overlay_map: {args.overlay_map} ({len(overlay_map)} labels)")

    se_map: dict[str, dict] = {}
    if args.se_map:
        se_map = _load_labeled_asset_map(args.se_map, "se")
        print(f"se_map: {args.se_map} ({len(se_map)} labels)")

    # --- row-range annotation (--csv) ---
    ir_data = load_ir(args.ir_json)

    if getattr(args, "csv", None):
        from src.pipeline.row_range import annotate_row_range
        csv_rows = _load_csv_rows(args.csv)
        annot = annotate_row_range(ir_data, csv_rows, force=True)
        print(f"row-range: {annot.matched}/{len(ir_data.get('utterances', []))} matched")
        if annot.unmatched_utterances:
            for idx in annot.unmatched_utterances:
                print(f"  Warning: utterance {idx} unmatched", file=sys.stderr)
        if annot.uncovered_rows:
            print(f"  Warning: {len(annot.uncovered_rows)} CSV rows uncovered",
                  file=sys.stderr)
        if annot.unmatched_utterances or annot.uncovered_rows:
            print("\nRow-range annotation FAILED", file=sys.stderr)
            return 1

    # --- quality gate (pre-patch) ---
    from src.pipeline.ir_validate import validate_ir
    known_labels = _get_known_face_labels(face_map) if face_map else None
    char_face = _get_char_face_map(face_map) if face_map else None
    known_slots = set(slot_map) if slot_map else None
    known_overlays = set(overlay_map) if overlay_map else None
    known_se = set(se_map) if se_map else None
    prompt_face_labels, prompt_doc_path = _load_prompt_face_contract(
        getattr(args, "prompt_doc", None)
    )
    if prompt_doc_path and prompt_face_labels:
        print(
            f"prompt face contract: {prompt_doc_path}"
            f" ({len(prompt_face_labels)} labels)"
        )

    vr = validate_ir(
        ir_data,
        known_labels,
        char_face_map=char_face,
        known_slot_labels=known_slots,
        known_overlay_labels=known_overlays,
        known_se_labels=known_se,
        char_default_slots=char_default_slots or None,
        prompt_face_labels=prompt_face_labels,
    )
    _print_validation(vr)
    if vr.has_errors:
        print(f"\nValidation FAILED ({len(vr.errors)} errors). Patch aborted.",
              file=sys.stderr)
        return 1

    # --- patch ---
    ymmp_data = load_ymmp(args.production_ymmp)

    result = patch_ymmp(
        ymmp_data,
        ir_data,
        face_map,
        bg_map,
        slot_map=slot_map,
        char_default_slots=char_default_slots or None,
        overlay_map=overlay_map,
        se_map=se_map,
    )

    fmt = getattr(args, "format", "text")

    if fmt != "json":
        print(f"\nFace changes: {result.face_changes}")
        print(f"Slot changes: {result.slot_changes}")
        print(f"Overlay changes: {result.overlay_changes}")
        print(f"SE plans: {result.se_plans}")
        if result.tachie_syncs:
            print(f"Idle face inserts: {result.tachie_syncs}")
        print(f"BG removed: {result.bg_changes}, BG added: {result.bg_additions}")
    for warning in result.warnings:
        print(f"  WARNING: {warning}", file=sys.stderr)

    fatal_warnings = _fatal_face_patch_warnings(result.warnings)
    if fatal_warnings:
        if fmt != "json":
            print(
                f"\nPatch FAILED ({len(fatal_warnings)} blocking issues)."
                " Partial output was not accepted.",
                file=sys.stderr,
            )
        if fmt == "json":
            print(json.dumps({
                "success": False,
                "error": "fatal_warnings",
                "fatal_warnings": fatal_warnings,
                "face_changes": result.face_changes,
                "slot_changes": result.slot_changes,
                "warnings": result.warnings,
            }, ensure_ascii=False))
        return 1

    if args.dry_run:
        if fmt == "json":
            print(json.dumps({
                "success": True, "dry_run": True,
                "face_changes": result.face_changes,
                "slot_changes": result.slot_changes,
                "overlay_changes": result.overlay_changes,
                "se_plans": result.se_plans,
                "tachie_syncs": result.tachie_syncs,
                "bg_changes": result.bg_changes,
                "bg_additions": result.bg_additions,
                "warnings": result.warnings,
            }, ensure_ascii=False))
        else:
            print("(dry-run: no file written)")
        return 0

    out_path = args.output
    if not out_path:
        stem = Path(args.production_ymmp).stem
        out_path = str(
            Path(args.production_ymmp).parent / f"{stem}_patched.ymmp"
        )
    save_ymmp(ymmp_data, out_path)
    if fmt == "json":
        print(json.dumps({
            "success": True,
            "output": out_path,
            "face_changes": result.face_changes,
            "slot_changes": result.slot_changes,
            "overlay_changes": result.overlay_changes,
            "se_plans": result.se_plans,
            "tachie_syncs": result.tachie_syncs,
            "bg_changes": result.bg_changes,
            "bg_additions": result.bg_additions,
            "warnings": result.warnings,
        }, ensure_ascii=False))
    else:
        print(f"Written: {out_path}")
    return 0


def _cmd_score_evidence(args: argparse.Namespace) -> int:
    """H-04: Evidence richness score."""
    from src.pipeline.evidence_score import score_evidence, load_brief

    brief = load_brief(args.brief)
    cat_scores = json.loads(args.scores)
    result = score_evidence(brief, cat_scores)

    fmt = getattr(args, "format", "text")
    if fmt == "json":
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"Evidence Richness Score: {result.total_score}/100 ({result.band})")
        print(f"\nCategory scores:")
        for cat, score in result.category_scores.items():
            print(f"  {cat}: {score}/3")
        if result.warnings:
            print(f"\nWarnings:")
            for w in result.warnings:
                print(f"  {w}")
        if result.recommended_repairs:
            print(f"\nRecommended repairs:")
            for r in result.recommended_repairs:
                print(f"  - {r}")
        if result.best_supports:
            print(f"\nBest supports: {', '.join(result.best_supports)}")
    return 0


def _cmd_score_visual_density(args: argparse.Namespace) -> int:
    """H-03: Visual density score."""
    from src.pipeline.visual_density_score import score_visual_density
    from src.pipeline.evidence_score import load_brief

    brief = load_brief(args.brief)
    cat_scores = json.loads(args.scores)
    result = score_visual_density(brief, cat_scores)

    fmt = getattr(args, "format", "text")
    if fmt == "json":
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"Visual Density Score: {result.total_score}/100 ({result.band})")
        print(f"\nCategory scores:")
        for cat, score in result.category_scores.items():
            print(f"  {cat}: {score}/3")
        if result.warnings:
            print(f"\nWarnings:")
            for w in result.warnings:
                print(f"  {w}")
        if result.recommended_repairs:
            print(f"\nRecommended repairs:")
            for r in result.recommended_repairs:
                print(f"  - {r}")
    return 0


def cli_entry() -> None:
    """pyproject.toml scripts エントリポイント."""
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main())
