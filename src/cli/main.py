"""NLMYTGen CLI -- 単一エントリポイント。

Usage:
    python -m src.cli.main build-csv <input>... [-o output.csv] [--speaker-map K1=V1,K2=V2] [--dry-run] [--stats]
    python -m src.cli.main build-cue-packet <input> [-o packet.md] [--format markdown|json] [--bundle-dir DIR]
    python -m src.cli.main build-diagram-packet <input> [-o packet.md] [--format markdown|json] [--bundle-dir DIR]
    python -m src.cli.main patch-ymmp <ymmp> <ir-json> --face-map face.json --bg-map bg.json [-o patched.ymmp]
    python -m src.cli.main patch-ymmp <ymmp> <ir-json> --skit-group-registry registry.json --skit-group-template-source templates.ymmp [--skit-group-only] [-o patched.ymmp]
    python -m src.cli.main audit-skit-group <ymmp> <ir-json> --skit-group-registry registry.json [--format text|json]
    python -m src.cli.main validate <input>
    python -m src.cli.main inspect <input> [--speaker-map K1=V1,K2=V2]
    python -m src.cli.main diagnose-script <input> [--speaker-map ...] [--format text|json] [--strict]
    python -m src.cli.main generate-map <input> [--unlabeled] [--format text|json]
    python -m src.cli.main fetch-topics <URL>... [-n 20] [--after YYYY-MM-DD] [--format text|json]
    python -m src.cli.main validate-ir <ir.json> [--palette ...] [--format text|json]
    python -m src.cli.main emit-packaging-brief-template [-o path] [--format markdown|json]
    python -m src.cli.main score-thumbnail-s8 --scores '{"single_claim":2,...}' [--payload ...] [--format text|json]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from math import ceil
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
    reflow_subtitles_measured,
    reflow_subtitles_v2,
    split_long_utterances,
)
from src.pipeline.text_measure import EastAsianWidthMeasurer, TextMeasurer, WpfTextMeasurer
from src.pipeline.validate_handoff import validate, has_errors, Severity
from src.pipeline.script_diagnostics import (
    diagnose_script,
    diagnostics_to_jsonable,
    has_error as diagnostics_has_error,
)
from src.pipeline.thumbnail_s8_score import score_thumbnail_s8


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


def _positive_percent(raw: str) -> float:
    """argparse 用: 0 より大きい倍率パーセントだけを受け付ける。"""
    try:
        value = float(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive number") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return value


def _positive_float(raw: str) -> float:
    """argparse 用: 0 より大きい数値だけを受け付ける。"""
    try:
        value = float(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive number") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return value


def _wrap_safety_value(raw: str) -> float:
    """argparse 用: wrap safety は 0 < value <= 1 の範囲に限定する。"""
    value = _positive_float(raw)
    if value > 1:
        raise argparse.ArgumentTypeError("must be less than or equal to 1")
    return value


def _effective_chars_per_line(chars_per_line: int, subtitle_font_scale: float) -> int:
    """基準 chars_per_line を字幕フォント倍率で補正する。"""
    if chars_per_line <= 0:
        return chars_per_line
    return max(1, int(chars_per_line * 100 / subtitle_font_scale))


def _animation_scalar_value(raw) -> float | None:
    """YMM4 の Animation 型から代表値を取り出す。"""
    if isinstance(raw, (int, float)):
        return float(raw)
    if not isinstance(raw, dict):
        return None
    values = raw.get("Values")
    if not isinstance(values, list) or not values:
        return None
    first_value = values[0]
    if not isinstance(first_value, dict):
        return None
    value = first_value.get("Value")
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _iter_mapping_nodes(raw):
    """YMM4 JSON 内の dict ノードを再帰走査する。"""
    if isinstance(raw, dict):
        yield raw
        for value in raw.values():
            yield from _iter_mapping_nodes(value)
    elif isinstance(raw, list):
        for value in raw:
            yield from _iter_mapping_nodes(value)


def _subtitle_font_size_entries_from_ymmp(data: dict) -> list[dict]:
    """YMM4 project 内の字幕フォントサイズ候補を抽出する。"""
    entries: list[dict] = []
    for node in _iter_mapping_nodes(data):
        if "FontSize" not in node:
            continue
        if not any(key in node for key in ("Font", "JimakuVisibility", "IsJimakuVisible")):
            continue
        font_size = _animation_scalar_value(node.get("FontSize"))
        if font_size is None or font_size <= 0:
            continue
        node_type = str(node.get("$type", ""))
        source = "voice_item" if "VoiceItem" in node_type or "Serif" in node else "character"
        entries.append(
            {
                "font_size": font_size,
                "font": node.get("Font"),
                "character": node.get("CharacterName") or node.get("Name"),
                "jimaku_visibility": node.get("JimakuVisibility"),
                "source": source,
            }
        )
    return entries


def _infer_subtitle_font_scale_from_ymmp(path: Path, base_font_size: float) -> tuple[float, float, int, dict]:
    """YMM4 project の字幕 FontSize から倍率を推定する。最大値を採用して安全側に倒す。"""
    with path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)
    entries = _subtitle_font_size_entries_from_ymmp(data)
    if not entries:
        raise ValueError(f"Subtitle FontSize not found in YMM4 project: {path}")
    selected = max(entries, key=lambda entry: entry["font_size"])
    if selected.get("font") is None:
        font_candidates = [entry for entry in entries if entry.get("font")]
        if font_candidates:
            selected = {**selected, "font": max(font_candidates, key=lambda entry: entry["font_size"]).get("font")}
    font_size = selected["font_size"]
    return font_size * 100 / base_font_size, font_size, len(entries), selected


def _resolve_subtitle_font_scale(args: argparse.Namespace) -> tuple[float, dict]:
    """明示倍率または YMM4 project から字幕フォント倍率を決める。"""
    explicit_scale = getattr(args, "subtitle_font_scale", None)
    if explicit_scale is not None:
        return explicit_scale, {"source": "manual"}

    source_ymmp = getattr(args, "subtitle_font_source_ymmp", None)
    if source_ymmp:
        base_font_size = getattr(args, "subtitle_base_font_size", 45.0)
        inferred_scale, font_size, entry_count, selected = _infer_subtitle_font_scale_from_ymmp(
            Path(source_ymmp),
            base_font_size,
        )
        return inferred_scale, {
            "source": "ymmp",
            "font_size": font_size,
            "font": selected.get("font"),
            "character": selected.get("character"),
            "base_font_size": base_font_size,
            "font_entry_count": entry_count,
            "source_ymmp": str(source_ymmp),
        }

    return 100.0, {"source": "default"}


def _default_wpf_measure_exe() -> Path:
    env_path = os.environ.get("NLMYTGEN_WPF_MEASURE_EXE")
    if env_path:
        return Path(env_path)
    return (
        Path(__file__).resolve().parents[2]
        / "tools"
        / "MeasureTextWpf"
        / "bin"
        / "Release"
        / "net8.0-windows"
        / "win-x64"
        / "publish"
        / "MeasureTextWpf.exe"
    )


def _resolve_text_measurer(
    args: argparse.Namespace,
    subtitle_font_info: dict,
) -> tuple[TextMeasurer | None, dict | None]:
    """--wrap-px 指定時の計測バックエンドを構築する。"""
    wrap_px = getattr(args, "wrap_px", None)
    if wrap_px is None:
        return None, None

    backend = getattr(args, "measure_backend", None)
    font_family = getattr(args, "font_family", None) or subtitle_font_info.get("font")
    font_size = getattr(args, "font_size", None) or subtitle_font_info.get("font_size")
    letter_spacing = float(getattr(args, "letter_spacing", 0.0) or 0.0)
    if backend is None:
        backend = "wpf" if (font_family and font_size) else "eaw"

    info = {
        "backend": backend,
        "wrap_px": wrap_px,
        "wrap_safety": getattr(args, "wrap_safety", 0.94),
        "effective_wrap_px": wrap_px * getattr(args, "wrap_safety", 0.94),
        "font_family": font_family,
        "font_size": font_size,
        "letter_spacing": letter_spacing,
    }

    if backend == "eaw":
        return EastAsianWidthMeasurer(), info

    if backend != "wpf":
        raise ValueError(f"Unsupported measure backend: {backend}")
    if not font_family:
        raise ValueError("--measure-backend wpf requires --font-family or --subtitle-font-source-ymmp with Font")
    if not font_size:
        raise ValueError("--measure-backend wpf requires --font-size or --subtitle-font-source-ymmp with FontSize")

    exe_path = Path(getattr(args, "measure_exe", None) or _default_wpf_measure_exe())
    if not exe_path.exists():
        raise FileNotFoundError(
            f"WPF measure helper not found: {exe_path}. "
            "Build it with: dotnet publish tools/MeasureTextWpf -c Release -r win-x64 --self-contained false"
        )
    info["measure_exe"] = str(exe_path)
    return WpfTextMeasurer(exe_path, font_family, float(font_size), letter_spacing), info


def _build_stats_payload(
    output,
    chars_per_line: int = 0,
    max_display_lines: int = 0,
    subtitle_font_scale: float = 100.0,
    effective_chars_per_line: int | None = None,
    subtitle_font_info: dict | None = None,
    measure_info: dict | None = None,
    measurer: TextMeasurer | None = None,
) -> dict:
    """話者統計とはみ出し候補を JSON 用 dict にまとめる（GUI / --format json 用）。"""
    speaker_counts = Counter(row.speaker for row in output.rows)
    speaker_chars = Counter()
    for row in output.rows:
        speaker_chars[row.speaker] += len(row.text.replace("\n", ""))

    speakers_out: list[dict] = []
    for speaker in sorted(speaker_counts):
        count = speaker_counts[speaker]
        chars = speaker_chars[speaker]
        avg = chars // count if count else 0
        speakers_out.append(
            {
                "speaker": speaker,
                "utterances": count,
                "total_chars": chars,
                "avg_chars": avg,
            }
        )
    total_chars = sum(speaker_chars.values())
    payload: dict = {
        "speakers": speakers_out,
        "total_utterances": len(output.rows),
        "total_chars": total_chars,
        "overflow_candidates": [],
        "overflow_params": None,
    }

    if chars_per_line > 0 and max_display_lines > 0:
        effective_cpl = (
            effective_chars_per_line
            if effective_chars_per_line is not None
            else _effective_chars_per_line(chars_per_line, subtitle_font_scale)
        )
        payload["overflow_params"] = {
            "chars_per_line": chars_per_line,
            "subtitle_font_scale": subtitle_font_scale,
            "effective_chars_per_line": effective_cpl,
            "max_display_lines": max_display_lines,
        }
        if subtitle_font_info:
            payload["overflow_params"]["subtitle_font_scale_source"] = subtitle_font_info.get("source")
            if subtitle_font_info.get("font") is not None:
                payload["overflow_params"]["subtitle_font"] = subtitle_font_info["font"]
            if subtitle_font_info.get("font_size") is not None:
                payload["overflow_params"]["subtitle_font_size"] = subtitle_font_info["font_size"]
            if subtitle_font_info.get("base_font_size") is not None:
                payload["overflow_params"]["subtitle_base_font_size"] = subtitle_font_info["base_font_size"]
            if subtitle_font_info.get("font_entry_count") is not None:
                payload["overflow_params"]["subtitle_font_entry_count"] = subtitle_font_info["font_entry_count"]
            if subtitle_font_info.get("source_ymmp") is not None:
                payload["overflow_params"]["subtitle_font_source_ymmp"] = subtitle_font_info["source_ymmp"]
        if measure_info:
            payload["overflow_params"]["measure_backend"] = measure_info.get("backend")
            payload["overflow_params"]["wrap_px"] = measure_info.get("wrap_px")
            payload["overflow_params"]["wrap_safety"] = measure_info.get("wrap_safety")
            payload["overflow_params"]["effective_wrap_px"] = measure_info.get("effective_wrap_px")
            payload["overflow_params"]["font_family"] = measure_info.get("font_family")
            payload["overflow_params"]["font_size"] = measure_info.get("font_size")
            payload["overflow_params"]["letter_spacing"] = measure_info.get("letter_spacing")
        overflow: list[dict] = []
        for i, row in enumerate(output.rows):
            w = display_width(row.text)
            measured_width = None
            if measurer is not None and measure_info:
                line_limit = float(measure_info["effective_wrap_px"])
                measured_widths = [measurer.width(chunk) for chunk in row.text.split("\n")]
                lines = sum(max(1, ceil(width / line_limit)) for width in measured_widths)
                measured_width = max(measured_widths) if measured_widths else 0.0
            else:
                lines = estimate_display_lines(row.text, effective_cpl)
            if lines > max_display_lines:
                item = {
                    "row": i + 1,
                    "speaker": row.speaker,
                    "estimated_lines": lines,
                    "display_width": w,
                }
                if measured_width is not None:
                    item["measured_width"] = round(measured_width, 2)
                overflow.append(item)
        payload["overflow_candidates"] = overflow

    return payload


def _print_stats(
    output,
    chars_per_line: int = 0,
    max_display_lines: int = 0,
    subtitle_font_scale: float = 100.0,
    effective_chars_per_line: int | None = None,
    subtitle_font_info: dict | None = None,
    measure_info: dict | None = None,
    measurer: TextMeasurer | None = None,
    file=sys.stdout,
):
    """話者ごとの発話統計を表示する。

    chars_per_line > 0 かつ max_display_lines > 0 のとき、
    推定行数が max_display_lines を超える行をはみ出し候補として警告する。
    """
    payload = _build_stats_payload(
        output,
        chars_per_line,
        max_display_lines,
        subtitle_font_scale=subtitle_font_scale,
        effective_chars_per_line=effective_chars_per_line,
        subtitle_font_info=subtitle_font_info,
        measure_info=measure_info,
        measurer=measurer,
    )

    print("--- Stats ---", file=file)
    for entry in payload["speakers"]:
        sp = entry["speaker"]
        count = entry["utterances"]
        chars = entry["total_chars"]
        avg = entry["avg_chars"]
        print(f"  {sp}: {count} utterances, {chars} chars (avg {avg})", file=file)
    print(
        f"  Total: {payload['total_utterances']} utterances, {payload['total_chars']} chars",
        file=file,
    )

    op = payload["overflow_params"]
    if op:
        cpl = op["chars_per_line"]
        effective_cpl = op["effective_chars_per_line"]
        font_scale = op["subtitle_font_scale"]
        mdl = op["max_display_lines"]
        oc = payload["overflow_candidates"]
        measure_backend = op.get("measure_backend")
        if oc:
            if measure_backend:
                header = (
                    f"--- Overflow candidates (>{mdl} lines at {op.get('effective_wrap_px'):g}px; "
                    f"backend={measure_backend}) ---"
                )
            elif effective_cpl == cpl and font_scale == 100:
                header = f"--- Overflow candidates (>{mdl} lines at {cpl} chars/line) ---"
            else:
                header = (
                    f"--- Overflow candidates (>{mdl} lines at effective {effective_cpl} chars/line; "
                    f"base={cpl}, font_scale={font_scale:g}%) ---"
                )
            print(header, file=file)
            for item in oc:
                width_note = f"display_width={item['display_width']}"
                if "measured_width" in item:
                    width_note += f", measured_width={item['measured_width']}"
                print(
                    f"  [WARN] row {item['row']}: {item['speaker']}, "
                    f"推定{item['estimated_lines']}行 ({width_note})",
                    file=file,
                )
        else:
            if measure_backend:
                fit_target = f"{op.get('effective_wrap_px'):g}px; backend={measure_backend}"
            elif effective_cpl == cpl and font_scale == 100:
                fit_target = f"{cpl} chars/line"
            else:
                fit_target = f"effective {effective_cpl} chars/line; base={cpl}, font_scale={font_scale:g}%"
            print(
                f"--- No overflow candidates (all within {mdl} lines at {fit_target}) ---",
                file=file,
            )
        if op.get("subtitle_font_scale_source") == "ymmp":
            print(
                f"Subtitle font scale inferred from YMM4: {font_scale:g}% "
                f"(font_size={op.get('subtitle_font_size')}, base={op.get('subtitle_base_font_size')})",
                file=file,
            )


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
    subtitle_font_scale, subtitle_font_info = _resolve_subtitle_font_scale(args)
    effective_chars_per_line = _effective_chars_per_line(chars_per_line, subtitle_font_scale)
    text_measurer, measure_info = _resolve_text_measurer(args, subtitle_font_info)
    balance_lines = getattr(args, "balance_lines", False)
    reflow_v2 = getattr(args, "reflow_v2", False)

    if max_lines:
        if text_measurer is not None and measure_info is not None:
            output = reflow_subtitles_measured(
                output,
                max_width=float(measure_info["effective_wrap_px"]),
                max_lines=max_lines,
                measurer=text_measurer,
            )
        elif reflow_v2:
            output = reflow_subtitles_v2(
                output,
                chars_per_line=effective_chars_per_line,
                max_lines=max_lines,
            )
        elif balance_lines:
            output = reflow_subtitles_v2(
                output,
                chars_per_line=effective_chars_per_line,
                max_lines=max_lines,
            )
        else:
            effective_max = effective_chars_per_line * max_lines
            output = split_long_utterances(output, max_length=effective_max, use_display_width=True)
    elif max_length:
        output = split_long_utterances(output, max_length=max_length, use_display_width=use_dw)

    results = validate(output)
    for r in results:
        prefix = "ERROR" if r.severity == Severity.ERROR else "WARN"
        print(f"[{prefix}] row {r.row_index}: {r.message}", file=sys.stderr)

    if json_result is not None:
        max_lines = getattr(args, "max_lines", None)
        use_dw = getattr(args, "display_width", False)
        chars_per_line = getattr(args, "chars_per_line", 40)
        stats_cpl = chars_per_line if (use_dw or max_lines) else 0
        stats_lines = max_lines if max_lines else (2 if (use_dw or max_lines) else 0)
        json_result["stats"] = _build_stats_payload(
            output,
            stats_cpl,
            stats_lines,
            subtitle_font_scale=subtitle_font_scale,
            effective_chars_per_line=effective_chars_per_line if stats_cpl > 0 else None,
            subtitle_font_info=subtitle_font_info,
            measure_info=measure_info,
            measurer=text_measurer,
        )

    if has_errors(results):
        print(f"Validation errors found. CSV not written: {input_path.name}", file=sys.stderr)
        if json_result is not None:
            json_result.update({"success": False, "error": "validation_errors"})
        return False

    if getattr(args, "stats", False) or getattr(args, "dry_run", False):
        stats_cpl = chars_per_line if (use_dw or max_lines) else 0
        stats_lines = max_lines if max_lines else (2 if (use_dw or max_lines) else 0)
        _print_stats(
            output,
            chars_per_line=stats_cpl,
            max_display_lines=stats_lines,
            subtitle_font_scale=subtitle_font_scale,
            effective_chars_per_line=effective_chars_per_line if stats_cpl > 0 else None,
            subtitle_font_info=subtitle_font_info,
            measure_info=measure_info,
            measurer=text_measurer,
        )

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
    if getattr(args, "wrap_px", None) is not None and not args.max_lines:
        raise ValueError("--wrap-px requires --max-lines")

    if len(inputs) == 1:
        input_path = inputs[0]
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.with_name(f"{input_path.stem}_ymm4.csv")
        jr: dict | None = {"input": str(input_path)} if fmt == "json" else None
        try:
            success = _build_one(input_path, output_path, args, json_result=jr)
        except (ValueError, FileNotFoundError) as exc:
            if fmt == "json":
                jr = {"input": str(input_path), "success": False, "error": str(exc)}
                print(json.dumps(jr, ensure_ascii=False))
            else:
                print(f"Error: {exc}", file=sys.stderr)
            return 1
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


def _cmd_diagnose_script(args: argparse.Namespace) -> int:
    """B-18: 台本機械診断を stdout に出す。"""
    input_path = Path(args.input)
    speaker_map = _resolve_speaker_map(args)
    unlabeled = getattr(args, "unlabeled", False)
    script = normalize(input_path, unlabeled=unlabeled)
    results = diagnose_script(
        script,
        speaker_map=speaker_map,
        expected_explainer=args.expected_explainer,
        expected_listener=args.expected_listener,
        long_run_threshold=args.long_run_threshold,
        listener_avg_ratio=args.listener_avg_ratio,
        strict=args.strict,
    )
    fmt = getattr(args, "diag_format", "text")
    meta: dict = {
        "input": str(input_path.resolve()),
        "utterance_count": len(script.utterances),
        "mapped_speaker_keys": sorted(set(speaker_map.keys())) if speaker_map else [],
    }
    if fmt == "json":
        payload = diagnostics_to_jsonable(results, meta=meta)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for d in results:
            sev = d.severity.name
            idx = "" if d.utterance_index is None else f" utt#{d.utterance_index}"
            print(f"[{sev}] {d.code}{idx}: {d.message}")
            print(f"  HINT: {d.hint}")
    return 1 if diagnostics_has_error(results) else 0


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
    p_build.add_argument("--subtitle-font-scale", type=_positive_percent, metavar="PERCENT",
                         help="Subtitle font scale percent used to narrow effective chars/line (default: 100)")
    p_build.add_argument("--subtitle-font-source-ymmp",
                         help="YMM4 project to infer subtitle font scale from FontSize when scale is omitted")
    p_build.add_argument("--subtitle-base-font-size", type=_positive_percent, default=45.0, metavar="N",
                         help="Base YMM4 subtitle FontSize treated as 100%% for --subtitle-font-source-ymmp (default: 45)")
    p_build.add_argument("--wrap-px", type=_positive_float, metavar="PX",
                         help="Measured subtitle line width in pixels/units; enables measured reflow with --max-lines")
    p_build.add_argument("--wrap-safety", type=_wrap_safety_value, default=0.94, metavar="RATIO",
                         help="Safety factor applied to --wrap-px (default: 0.94)")
    p_build.add_argument("--measure-backend", choices=["eaw", "wpf"],
                         help="Measured reflow backend for --wrap-px (default: wpf when font data exists, otherwise eaw)")
    p_build.add_argument("--font-family",
                         help="Font family for --measure-backend wpf; inferred from --subtitle-font-source-ymmp when possible")
    p_build.add_argument("--font-size", type=_positive_float, metavar="PX",
                         help="Font size for --measure-backend wpf; inferred from --subtitle-font-source-ymmp when possible")
    p_build.add_argument("--letter-spacing", type=float, default=0.0, metavar="PX",
                         help="Additional per-character spacing for measured text width (default: 0)")
    p_build.add_argument("--measure-exe",
                         help="Path to MeasureTextWpf.exe (or set NLMYTGEN_WPF_MEASURE_EXE)")
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
    p_patch.add_argument("--face-map-bundle", help="G-19: Face map bundle registry JSON (multi-body)")
    p_patch.add_argument("--bg-map", help="BG label → image/video file path mapping (JSON)")
    p_patch.add_argument("--slot-map", help="Slot label -> x/y/zoom mapping (JSON or registry)")
    p_patch.add_argument("--overlay-map", help="Overlay label -> image asset mapping (JSON or registry)")
    p_patch.add_argument("--se-map", help="SE label -> audio asset mapping (JSON or registry)")
    p_patch.add_argument(
        "--timeline-profile",
        choices=[
            "motion_only",
            "motion_bg_anim_minimal",
            "motion_bg_anim_effects",
            "production_ai_monitoring_lane",
            "group_motion_only",
        ],
        default=None,
        help="G-17: timeline_route_contract.json のプロファイル (maps と併用)",
    )
    p_patch.add_argument(
        "--motion-map",
        help="G-17: JSON motion ラベル → {video_effect: {...}} (プロファイル適用時)",
    )
    p_patch.add_argument(
        "--tachie-motion-map",
        help="Phase2: JSON motion ラベル → VideoEffects 配列（--timeline-profile 未指定時に区間分割適用）",
    )
    p_patch.add_argument(
        "--transition-map",
        help="JSON: transition ラベル → VoiceItem へマージするフィールド辞書",
    )
    p_patch.add_argument(
        "--bg-anim-map",
        help="JSON: bg_anim ラベル → {video_effect: {...}} (Layer 0 Image/Video の VideoEffects へ)",
    )
    p_patch.add_argument(
        "--group-motion-map",
        help="A案: group_motion ラベル → {x,y,zoom}（既存 GroupItem の幾何）",
    )
    p_patch.add_argument(
        "--skit-group-registry",
        help="G-24: skit_group canonical anchor / exact-fallback-manual_note registry JSON",
    )
    p_patch.add_argument(
        "--skit-group-template-source",
        help="G-24: repo-tracked ymmp template library for skit_group GroupItem placement",
    )
    p_patch.add_argument(
        "--skit-group-only",
        action="store_true",
        help="G-24: apply only skit_group GroupItem placement; skip face/bg/timeline patch paths",
    )
    p_patch.add_argument(
        "--skit-group-compact-review",
        action="store_true",
        help="G-24: place skit_group cues sequentially for compact visual review instead of production timing",
    )
    p_patch.add_argument(
        "--skit-group-review-spacing",
        type=int,
        default=240,
        help="G-24: frame spacing for --skit-group-compact-review (default: 240)",
    )
    p_patch.add_argument(
        "--timeline-contract",
        help="timeline_route_contract.json のパス (省略時は samples/timeline_route_contract.json)",
    )
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
    p_apply.add_argument("--face-map-bundle", help="G-19: Face map bundle registry JSON (multi-body)")
    p_apply.add_argument("--bg-map", help="BG label → file path mapping (JSON)")
    p_apply.add_argument("--slot-map", help="Slot label -> x/y/zoom mapping (JSON or registry)")
    p_apply.add_argument("--overlay-map", help="Overlay label -> image asset mapping (JSON or registry)")
    p_apply.add_argument("--se-map", help="SE label -> audio asset mapping (JSON or registry)")
    p_apply.add_argument(
        "--timeline-profile",
        choices=[
            "motion_only",
            "motion_bg_anim_minimal",
            "motion_bg_anim_effects",
            "production_ai_monitoring_lane",
            "group_motion_only",
        ],
        default=None,
        help="G-17: timeline_route_contract.json のプロファイル",
    )
    p_apply.add_argument(
        "--motion-map",
        help="G-17: JSON motion ラベル → {video_effect: {...}}",
    )
    p_apply.add_argument(
        "--tachie-motion-map",
        help="Phase2: JSON motion ラベル → VideoEffects 配列",
    )
    p_apply.add_argument(
        "--transition-map",
        help="JSON: transition ラベル → VoiceItem フィールド",
    )
    p_apply.add_argument(
        "--bg-anim-map",
        help="JSON: bg_anim ラベル → {video_effect: {...}}",
    )
    p_apply.add_argument(
        "--group-motion-map",
        help="A案: group_motion ラベル → {x,y,zoom}（既存 GroupItem の幾何）",
    )
    p_apply.add_argument(
        "--skit-group-registry",
        help="G-24: skit_group canonical anchor / exact-fallback-manual_note registry JSON",
    )
    p_apply.add_argument(
        "--skit-group-template-source",
        help="G-24: repo-tracked ymmp template library for skit_group GroupItem placement",
    )
    p_apply.add_argument(
        "--skit-group-only",
        action="store_true",
        help="G-24: apply only skit_group GroupItem placement; skip face/bg/timeline patch paths",
    )
    p_apply.add_argument(
        "--skit-group-compact-review",
        action="store_true",
        help="G-24: place skit_group cues sequentially for compact visual review instead of production timing",
    )
    p_apply.add_argument(
        "--skit-group-review-spacing",
        type=int,
        default=240,
        help="G-24: frame spacing for --skit-group-compact-review (default: 240)",
    )
    p_apply.add_argument(
        "--strict-skit-group-intents",
        action="store_true",
        help="Fail when motion_target layer entries use labels outside the skit_group registry",
    )
    p_apply.add_argument(
        "--timeline-contract",
        help="timeline_route_contract.json のパス",
    )
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
    p_valir.add_argument("--face-map-bundle", help="G-19: Face map bundle registry JSON (multi-body)")
    p_valir.add_argument("--palette", help="Palette ymmp (alternative to --face-map)")
    p_valir.add_argument("--slot-map", help="Slot label -> x/y/zoom mapping (JSON or registry)")
    p_valir.add_argument("--overlay-map", help="Overlay label -> image asset mapping (JSON or registry)")
    p_valir.add_argument("--se-map", help="SE label -> audio asset mapping (JSON or registry)")
    p_valir.add_argument(
        "--motion-map",
        help="G-17: motion 台帳 JSON のラベル（MOTION_MAP_UNKNOWN_LABEL 用）",
    )
    p_valir.add_argument(
        "--tachie-motion-map",
        help="Phase2: VideoEffects 配列台帳 JSON のラベル（MOTION_MAP_UNKNOWN_LABEL 用）",
    )
    p_valir.add_argument(
        "--group-motion-map",
        help="A案: group_motion 台帳 JSON のラベル（GROUP_MOTION_UNKNOWN_LABEL 用）",
    )
    p_valir.add_argument(
        "--skit-group-registry",
        help="G-24: skit_group intent vocabulary registry JSON",
    )
    p_valir.add_argument(
        "--strict-skit-group-intents",
        action="store_true",
        help="Fail when motion_target layer entries use labels outside the skit_group registry",
    )
    p_valir.add_argument("--prompt-doc",
                         help="Prompt markdown for face contract drift check"
                              " (default: docs/S6-production-memo-prompt.md)")
    p_valir.add_argument("--format", choices=["text", "json"], default="text",
                         help="text: human report to stdout; json: machine summary on stdout, meta on stderr")

    # audit-skit-group
    p_skit_audit = subparsers.add_parser(
        "audit-skit-group",
        help="G-24: preflight audit for canonical skit_group anchor and template resolution",
    )
    p_skit_audit.add_argument("ymmp", help="Input ymmp file path")
    p_skit_audit.add_argument("ir_json", help="Production IR JSON file path")
    p_skit_audit.add_argument(
        "--skit-group-registry",
        required=True,
        help="skit_group registry JSON with canonical_groups/templates/intent_fallbacks",
    )
    p_skit_audit.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

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

    # score-thumbnail-s8 (Lane E probe)
    p_score_thumb = subparsers.add_parser(
        "score-thumbnail-s8",
        help="Lane E probe: score S-8 thumbnail quality from manual category scores",
    )
    p_score_thumb.add_argument(
        "--scores",
        required=True,
        help=(
            "Category scores JSON: "
            "{\"single_claim\": 0-3, \"specificity\": 0-3, "
            "\"title_alignment\": 0-3, \"mobile_readability\": 0-3}"
        ),
    )
    p_score_thumb.add_argument(
        "--payload",
        help="Optional metadata JSON: {\"run_id\":\"...\",\"video_slug\":\"...\",\"output_file\":\"...\"}",
    )
    p_score_thumb.add_argument(
        "--payload-file",
        help="Optional metadata JSON file path (same schema as --payload)",
    )
    p_score_thumb.add_argument("--format", choices=["json", "text"], default="text")

    # emit-packaging-brief-template (H-01)
    p_emit_brief = subparsers.add_parser(
        "emit-packaging-brief-template",
        help="H-01: Write empty Packaging Orchestrator brief (Markdown or JSON skeleton)",
    )
    p_emit_brief.add_argument(
        "-o", "--output",
        help="Output file path (default: stdout)",
    )
    p_emit_brief.add_argument(
        "--format", choices=["markdown", "json"], default="markdown",
        help="markdown (default) or minimal JSON skeleton",
    )

    # diagnose-script (B-18)
    p_diag_script = subparsers.add_parser(
        "diagnose-script",
        help="B-18: Mechanical script quality diagnostics before yukkuri refinement",
    )
    p_diag_script.add_argument("input", help="Input file path (.txt or .csv)")
    _add_speaker_map_args(p_diag_script)
    _add_unlabeled_arg(p_diag_script)
    p_diag_script.add_argument(
        "--expected-explainer",
        default="まりさ",
        help="Expected mapped name for explainer/host-like role (default: まりさ)",
    )
    p_diag_script.add_argument(
        "--expected-listener",
        default="れいむ",
        help="Expected mapped name for listener/guest-like role (default: れいむ)",
    )
    p_diag_script.add_argument(
        "--long-run-threshold",
        type=int,
        default=6,
        metavar="N",
        help="Warn when same speaker has N+ consecutive utterances (default: 6)",
    )
    p_diag_script.add_argument(
        "--listener-avg-ratio",
        type=float,
        default=1.25,
        metavar="R",
        help="guest avg / host avg >= R triggers LISTENER_LONG_AVG_DOMINANCE (default: 1.25)",
    )
    p_diag_script.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        dest="diag_format",
        help="Output format (default: text)",
    )
    p_diag_script.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any ERROR diagnostic (e.g. unmapped speaker with incomplete map)",
    )

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
        elif args.command == "audit-skit-group":
            return _cmd_audit_skit_group(args)
        elif args.command == "score-evidence":
            return _cmd_score_evidence(args)
        elif args.command == "score-visual-density":
            return _cmd_score_visual_density(args)
        elif args.command == "score-thumbnail-s8":
            return _cmd_score_thumbnail_s8(args)
        elif args.command == "emit-packaging-brief-template":
            return _cmd_emit_packaging_brief_template(args)
        elif args.command == "diagnose-script":
            return _cmd_diagnose_script(args)
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

    skit_group_only = bool(getattr(args, "skit_group_only", False))
    if skit_group_only and (
        not getattr(args, "skit_group_registry", None)
        or not getattr(args, "skit_group_template_source", None)
    ):
        print(
            "Error: --skit-group-only requires --skit-group-registry "
            "and --skit-group-template-source",
            file=sys.stderr,
        )
        return 1

    ymmp_data = load_ymmp(args.ymmp)
    ir_data = load_ir(args.ir_json)

    skit_audit_result = None
    skit_group_registry_data = None
    skit_group_template_source_data = None
    if getattr(args, "skit_group_template_source", None):
        if not getattr(args, "skit_group_registry", None):
            print(
                "Error: --skit-group-template-source requires --skit-group-registry",
                file=sys.stderr,
            )
            return 1
        skit_group_registry_data, skit_labels = _load_skit_group_registry_contract(
            args.skit_group_registry,
        )
        skit_group_template_source_data = load_ymmp(args.skit_group_template_source)
        print(
            f"skit_group_template_source: {args.skit_group_template_source} "
            f"({len(skit_labels)} registry labels)"
        )
    elif getattr(args, "skit_group_registry", None):
        skit_audit_result = _run_skit_group_audit(
            ymmp_data,
            ir_data,
            args.skit_group_registry,
        )
        _print_skit_group_audit(skit_audit_result)
        if skit_audit_result.status == "error":
            print("\nSkit group preflight FAILED. Patch aborted.", file=sys.stderr)
            return 1

    face_map: dict[str, dict[str, str]] = {}
    face_map_bundle: dict[str, dict] | None = None
    char_default_bodies: dict[str, str] | None = None
    if getattr(args, "face_map_bundle", None):
        if args.face_map:
            print("Error: --face-map and --face-map-bundle are mutually exclusive",
                  file=sys.stderr)
            return 1
        face_map_bundle, char_default_bodies = _load_face_map_bundle(args.face_map_bundle)
        print(f"face_map_bundle: {args.face_map_bundle} ({len(face_map_bundle)} bodies)")
    elif args.face_map:
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

    motion_map: dict[str, dict] = {}
    if getattr(args, "motion_map", None):
        motion_map = _load_adapter_motion_map(args.motion_map)
        print(f"motion_map (G-17): {args.motion_map} ({len(motion_map)} labels)")
    tachie_motion_effects_map = None
    if getattr(args, "tachie_motion_map", None):
        tachie_motion_effects_map = _load_tachie_motion_effects_map(
            args.tachie_motion_map,
        )
        print(
            f"tachie_motion_map: {args.tachie_motion_map} "
            f"({len(tachie_motion_effects_map)} labels)",
        )
    transition_map: dict[str, dict] = {}
    if getattr(args, "transition_map", None):
        with open(args.transition_map, "r", encoding="utf-8") as f:
            transition_map = json.load(f)
        print(f"transition_map: {args.transition_map} ({len(transition_map)} labels)")
    bg_anim_map: dict[str, dict] = {}
    if getattr(args, "bg_anim_map", None):
        with open(args.bg_anim_map, "r", encoding="utf-8") as f:
            bg_anim_map = json.load(f)
        print(f"bg_anim_map: {args.bg_anim_map} ({len(bg_anim_map)} labels)")
    group_motion_map: dict[str, dict] = {}
    if getattr(args, "group_motion_map", None):
        group_motion_map = _load_group_motion_map(args.group_motion_map)
        print(
            f"group_motion_map: {args.group_motion_map} "
            f"({len(group_motion_map)} labels)"
        )

    result = patch_ymmp(
        ymmp_data,
        ir_data,
        face_map,
        bg_map,
        slot_map=slot_map,
        char_default_slots=char_default_slots,
        overlay_map=overlay_map,
        se_map=se_map,
        timeline_profile=getattr(args, "timeline_profile", None),
        motion_map=motion_map or None,
        transition_map=transition_map or None,
        bg_anim_map=bg_anim_map or None,
        group_motion_map=group_motion_map or None,
        timeline_contract_path=getattr(args, "timeline_contract", None),
        tachie_motion_effects_map=tachie_motion_effects_map,
        face_map_bundle=face_map_bundle,
        char_default_bodies=char_default_bodies,
        skit_group_registry=skit_group_registry_data,
        skit_group_template_source=skit_group_template_source_data,
        skit_group_only=skit_group_only,
        skit_group_compact_review=getattr(args, "skit_group_compact_review", False),
        skit_group_review_spacing=getattr(args, "skit_group_review_spacing", 240),
    )

    print(f"Face changes: {result.face_changes}")
    print(f"Slot changes: {result.slot_changes}")
    print(f"Overlay changes: {result.overlay_changes}")
    print(f"SE insertions: {result.se_plans}")
    if result.motion_changes or result.transition_changes or result.bg_anim_changes:
        print(
            f"Timeline adapter: motion={result.motion_changes}, "
            f"transition={result.transition_changes}, bg_anim={result.bg_anim_changes}"
        )
    print(f"BG removed: {result.bg_changes}, BG added: {result.bg_additions}")
    print(f"BG anim writes: {result.bg_anim_changes}")
    print(f"Transition VoiceItem writes: {result.transition_changes}")
    print(f"VideoEffects writes (motion): {result.motion_changes}")
    print(f"GroupItem geometry writes: {result.group_motion_changes}")
    print(
        "Skit group placements: "
        f"{result.skit_group_placements} "
        f"(GroupItems inserted: {result.skit_group_item_insertions})"
    )
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


def _load_face_map_bundle(
    bundle_path: str | Path,
) -> tuple[dict[str, dict], dict[str, str]]:
    """face_map バンドルレジストリ JSON を読み、body_id → face_map を返す (G-19).

    Returns
    -------
    (body_face_maps, char_default_bodies)
        body_face_maps: { body_id: { char_name: { label: { parts } } } }
        char_default_bodies: { char_name: default_body_id }
    """
    bundle_path = Path(bundle_path)
    with open(bundle_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    bodies_section = raw.get("bodies")
    if not isinstance(bodies_section, dict):
        raise ValueError("face_map_bundle must have a 'bodies' object")

    body_face_maps: dict[str, dict] = {}
    base_dir = bundle_path.parent
    for body_id, spec in bodies_section.items():
        if not isinstance(spec, dict):
            raise ValueError(f"bodies['{body_id}'] must be an object")
        face_map_rel = spec.get("face_map")
        if not isinstance(face_map_rel, str):
            raise ValueError(f"bodies['{body_id}'].face_map must be a string path")
        face_map_path = base_dir / face_map_rel
        if not face_map_path.exists():
            raise FileNotFoundError(
                f"Face map file not found: {face_map_path} "
                f"(referenced by bodies['{body_id}'])"
            )
        with open(face_map_path, "r", encoding="utf-8") as fm:
            body_face_maps[body_id] = json.load(fm)

    char_default_bodies: dict[str, str] = {}
    characters = raw.get("characters")
    if isinstance(characters, dict):
        for char, spec in characters.items():
            if not isinstance(spec, dict):
                continue
            default_body = spec.get("default_body")
            if isinstance(default_body, str) and default_body:
                char_default_bodies[str(char)] = default_body

    return body_face_maps, char_default_bodies


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


def _load_tachie_motion_effects_map(path: str | Path) -> dict[str, list[dict]]:
    """Phase2: motion ラベル → TachieItem.VideoEffects 配列を読む."""
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, dict):
        raise ValueError("motion_map JSON must be an object")

    motions_raw = raw.get("motions") if isinstance(raw.get("motions"), dict) else raw
    if not isinstance(motions_raw, dict):
        raise ValueError(
            "motion_map JSON must define a top-level object or 'motions'"
        )

    motion_map: dict[str, object] = {}
    for label, value in motions_raw.items():
        if isinstance(value, dict) and value.get("schema") == "base_prop_oneshot":
            # v3 one-shot schema: { "schema": "base_prop_oneshot",
            #   "delta_keyframes": { "X": {"Values":[...], "AnimationType":...}, ... } }
            deltas = value.get("delta_keyframes")
            if not isinstance(deltas, dict) or not deltas:
                raise ValueError(
                    f"motion_map entry '{label}' (base_prop_oneshot) "
                    "must have non-empty 'delta_keyframes' dict"
                )
            for prop_name, prop_def in deltas.items():
                if not isinstance(prop_def, dict):
                    raise ValueError(
                        f"motion_map '{label}'.delta_keyframes['{prop_name}'] "
                        "must be an object"
                    )
                if not isinstance(prop_def.get("Values"), list):
                    raise ValueError(
                        f"motion_map '{label}'.delta_keyframes['{prop_name}']"
                        ".Values must be a list"
                    )
            motion_map[str(label)] = dict(value)
            continue
        if not isinstance(value, list):
            raise ValueError(
                f"motion_map entry '{label}' must be a list of effect objects"
                " or a base_prop_oneshot dict"
            )
        parsed: list[dict] = []
        for i, item in enumerate(value):
            if not isinstance(item, dict):
                raise ValueError(
                    f"motion_map entry '{label}'[{i}] must be an object"
                )
            parsed.append(dict(item))
        motion_map[str(label)] = parsed
    return motion_map


def _load_adapter_motion_map(path: str | Path) -> dict[str, dict]:
    """G-17: motion ラベル → { video_effect: {...} } を読む."""
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        raise ValueError("motion_map JSON must be an object")
    out: dict[str, dict] = {}
    for k, v in raw.items():
        if not isinstance(v, dict):
            raise ValueError(f"motion_map entry '{k}' must be an object")
        out[str(k)] = dict(v)
    return out


def _load_group_motion_map(path: str | Path) -> dict[str, dict]:
    """A案: group_motion ラベル → GroupItem.X/Y/Zoom の辞書を読む."""
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        raise ValueError("group_motion_map JSON must be an object")

    motions_raw = raw.get("group_motions") if isinstance(raw.get("group_motions"), dict) else raw
    if not isinstance(motions_raw, dict):
        raise ValueError(
            "group_motion_map JSON must define a top-level object or 'group_motions'"
        )

    _VALID_MODES = {"absolute", "relative"}
    out: dict[str, dict] = {}
    for label, spec in motions_raw.items():
        if not isinstance(spec, dict):
            raise ValueError(f"group_motion_map entry '{label}' must be an object")
        mode = spec.get("mode", "absolute")
        if mode not in _VALID_MODES:
            raise ValueError(
                f"group_motion_map entry '{label}' has invalid mode '{mode}'"
                f" (must be one of {sorted(_VALID_MODES)})"
            )
        out[str(label)] = dict(spec)
    return out


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
        "SLOT_CHARACTER_DRIFT:",
        "SLOT_DEFAULT_DRIFT:",
        "SLOT_REGISTRY_MISS:",
        "SLOT_NO_TACHIE_ITEM:",
        "SLOT_VALUE_INVALID:",
        "MOTION_MAP_MISS:",
        "MOTION_NO_TACHIE_ITEM:",
        "GROUP_MOTION_NO_GROUP_ITEM:",
        "GROUP_MOTION_TARGET_MISS:",
        "GROUP_MOTION_TARGET_AMBIGUOUS:",
        "SKIT_TEMPLATE_SOURCE_MISSING:",
        "SKIT_TEMPLATE_SOURCE_FORBIDDEN_ITEM:",
        "SKIT_TEMPLATE_SOURCE_ASSET_MISSING:",
        "SKIT_PLACEMENT_NO_VOICE_TIMING:",
        "SKIT_PLACEMENT_GROUP_AMBIGUOUS:",
        "SKIT_PLACEMENT_REGISTRY_INVALID:",
        "SKIT_TEMPLATE_ANALYSIS_INSUFFICIENT:",
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


def _ir_validate_json_summary(vr, ir_data: dict) -> dict:
    """validate-ir --format json 用の機械可読サマリ（詳細は従来どおり text モード）。"""
    face_top = sorted(vr.face_distribution.items(), key=lambda x: -x[1])[:5]
    return {
        "command": "validate-ir",
        "success": not vr.has_errors,
        "error_count": len(vr.errors),
        "warning_count": len(vr.warnings),
        "info_count": len(vr.info),
        "utterance_count": len(ir_data.get("utterances", [])),
        "preview_errors": vr.errors[:8],
        "preview_warnings": vr.warnings[:8],
        "face_distribution_top": [{"label": k, "count": v} for k, v in face_top],
        "used_skit_group_motion_labels": vr.used_skit_group_motion_labels,
    }


def _apply_production_summary(result) -> dict:
    """apply-production JSON に付与する変更件数・警告プレビュー。"""
    fatal = _fatal_face_patch_warnings(result.warnings)
    return {
        "warning_count": len(result.warnings),
        "fatal_warning_count": len(fatal),
        "preview_warnings": result.warnings[:8],
        "face_changes": result.face_changes,
        "slot_changes": result.slot_changes,
        "overlay_changes": result.overlay_changes,
        "se_plans": result.se_plans,
        "tachie_syncs": result.tachie_syncs,
        "bg_removed": result.bg_changes,
        "bg_added": result.bg_additions,
        "bg_anim_changes": result.bg_anim_changes,
        "transition_changes": result.transition_changes,
        "motion_changes": result.motion_changes,
        "group_motion_changes": result.group_motion_changes,
        "skit_group_placements": result.skit_group_placements,
        "skit_group_item_insertions": result.skit_group_item_insertions,
    }


def _skit_audit_json_summary(audit_result) -> dict:
    return audit_result.to_dict()


def _print_skit_group_audit(audit_result, *, file=sys.stdout) -> None:
    from src.pipeline.skit_group_audit import render_skit_group_audit_text

    print(render_skit_group_audit_text(audit_result), file=file)


def _run_skit_group_audit(ymmp_data: dict, ir_data: dict, registry_path: str):
    from src.pipeline.skit_group_audit import audit_skit_group, load_skit_group_registry

    registry_data = load_skit_group_registry(registry_path)
    return audit_skit_group(ymmp_data, ir_data, registry_data)


def _load_skit_group_registry_contract(registry_path: str) -> tuple[dict, set[str]]:
    from src.pipeline.skit_group_audit import load_skit_group_registry

    registry_data = load_skit_group_registry(registry_path)
    templates = registry_data.get("templates", {})
    if not isinstance(templates, dict):
        return registry_data, set()
    labels = {
        raw.get("intent")
        for raw in templates.values()
        if isinstance(raw, dict) and isinstance(raw.get("intent"), str)
    }
    fallbacks = registry_data.get("intent_fallbacks", {})
    if isinstance(fallbacks, dict):
        labels.update(key for key in fallbacks if isinstance(key, str))
    labels.discard(None)
    return registry_data, {str(label) for label in labels}


def _cmd_audit_skit_group(args: argparse.Namespace) -> int:
    from src.pipeline.ymmp_patch import load_ir, load_ymmp

    ymmp_data = load_ymmp(args.ymmp)
    ir_data = load_ir(args.ir_json)
    audit_result = _run_skit_group_audit(
        ymmp_data,
        ir_data,
        args.skit_group_registry,
    )

    if args.format == "json":
        print(json.dumps(_skit_audit_json_summary(audit_result), ensure_ascii=False))
    else:
        _print_skit_group_audit(audit_result)

    return 1 if audit_result.status == "error" else 0


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
    known_motion_labels = None
    known_group_motion_labels = None
    known_skit_group_motion_labels = None
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
    known_motion_keys: set[str] = set()
    if getattr(args, "motion_map", None):
        known_motion_keys.update(
            _load_adapter_motion_map(args.motion_map).keys(),
        )
    if getattr(args, "tachie_motion_map", None):
        known_motion_keys.update(
            _load_tachie_motion_effects_map(args.tachie_motion_map).keys(),
        )
    if known_motion_keys:
        known_motion_labels = known_motion_keys
    if getattr(args, "group_motion_map", None):
        known_group_motion_labels = set(
            _load_group_motion_map(args.group_motion_map).keys()
        )
    if getattr(args, "skit_group_registry", None):
        _, known_skit_group_motion_labels = _load_skit_group_registry_contract(
            args.skit_group_registry
        )
    elif getattr(args, "strict_skit_group_intents", False):
        print(
            "Error: --strict-skit-group-intents requires --skit-group-registry",
            file=sys.stderr,
        )
        return 1

    # G-19: face_map_bundle → known_body_ids
    known_body_ids: set[str] | None = None
    if getattr(args, "face_map_bundle", None):
        bundle_maps, _ = _load_face_map_bundle(args.face_map_bundle)
        known_body_ids = set(bundle_maps.keys())

    fmt = getattr(args, "format", "text")
    meta_stream = sys.stderr if fmt == "json" else sys.stdout

    if prompt_doc_path and prompt_face_labels:
        print(
            f"prompt face contract: {prompt_doc_path}"
            f" ({len(prompt_face_labels)} labels)",
            file=meta_stream,
        )
    if known_slots is not None:
        print(f"slot contract: {len(known_slots)} labels", file=meta_stream)
    if known_overlays is not None:
        print(f"overlay contract: {len(known_overlays)} labels", file=meta_stream)
    if known_se is not None:
        print(f"se contract: {len(known_se)} labels", file=meta_stream)
    if known_motion_labels is not None:
        print(
            f"motion contract: {len(known_motion_labels)} labels",
            file=meta_stream,
        )
    if known_group_motion_labels is not None:
        print(
            f"group motion contract: {len(known_group_motion_labels)} labels",
            file=meta_stream,
        )
    if known_skit_group_motion_labels is not None:
        print(
            f"skit_group intent contract: {len(known_skit_group_motion_labels)} labels",
            file=meta_stream,
        )
    if known_body_ids is not None:
        print(
            f"body_id contract: {len(known_body_ids)} bodies",
            file=meta_stream,
        )

    vr = validate_ir(
        ir_data,
        known_labels,
        char_face_map=char_face,
        known_slot_labels=known_slots,
        known_overlay_labels=known_overlays,
        known_se_labels=known_se,
        known_motion_labels=known_motion_labels,
        known_group_motion_labels=known_group_motion_labels,
        known_skit_group_motion_labels=known_skit_group_motion_labels,
        strict_skit_group_intents=getattr(args, "strict_skit_group_intents", False),
        char_default_slots=char_default_slots,
        prompt_face_labels=prompt_face_labels,
        known_body_ids=known_body_ids,
    )

    if fmt == "json":
        print(json.dumps(_ir_validate_json_summary(vr, ir_data), ensure_ascii=False))
        return 1 if vr.has_errors else 0

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

    skit_group_only = bool(getattr(args, "skit_group_only", False))
    if getattr(args, "strict_skit_group_intents", False) and not getattr(args, "skit_group_registry", None):
        print(
            "Error: --strict-skit-group-intents requires --skit-group-registry",
            file=sys.stderr,
        )
        return 1
    if skit_group_only:
        if (
            not getattr(args, "skit_group_registry", None)
            or not getattr(args, "skit_group_template_source", None)
        ):
            print(
                "Error: --skit-group-only requires --skit-group-registry "
                "and --skit-group-template-source",
                file=sys.stderr,
            )
            return 1
        if getattr(args, "csv", None):
            print(
                "Error: --skit-group-only uses existing IR index anchors; "
                "do not pass --csv",
                file=sys.stderr,
            )
            return 1

        skit_group_registry_data, skit_labels = _load_skit_group_registry_contract(
            args.skit_group_registry,
        )
        skit_group_template_source_data = load_ymmp(args.skit_group_template_source)
        ir_data = load_ir(args.ir_json)
        fmt = getattr(args, "format", "text")
        if getattr(args, "strict_skit_group_intents", False):
            from src.pipeline.ir_validate import validate_ir
            vr = validate_ir(
                ir_data,
                known_skit_group_motion_labels=skit_labels,
                strict_skit_group_intents=True,
            )
            if vr.has_errors:
                if fmt == "json":
                    print(json.dumps({
                        "success": False,
                        "error": "validation_failed",
                        "validation": _ir_validate_json_summary(vr, ir_data),
                    }, ensure_ascii=False))
                else:
                    _print_validation(vr)
                    print(
                        f"\nValidation FAILED ({len(vr.errors)} errors). Patch aborted.",
                        file=sys.stderr,
                )
                return 1
        ymmp_data = load_ymmp(args.production_ymmp)
        if fmt != "json":
            print(
                f"skit_group_registry: {args.skit_group_registry} "
                f"({len(skit_labels)} labels)"
            )
            print(f"skit_group_template_source: {args.skit_group_template_source}")

        result = patch_ymmp(
            ymmp_data,
            ir_data,
            {},
            {},
            skit_group_registry=skit_group_registry_data,
            skit_group_template_source=skit_group_template_source_data,
            skit_group_only=True,
            skit_group_compact_review=getattr(args, "skit_group_compact_review", False),
            skit_group_review_spacing=getattr(args, "skit_group_review_spacing", 240),
        )

        if fmt != "json":
            print(
                "Skit group placements: "
                f"{result.skit_group_placements} "
                f"(GroupItems inserted: {result.skit_group_item_insertions})"
            )
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
            else:
                print(json.dumps({
                    "success": False,
                    "error": "fatal_warnings",
                    "fatal_warnings": fatal_warnings,
                    "skit_group_placements": result.skit_group_placements,
                    "skit_group_item_insertions": result.skit_group_item_insertions,
                    "warnings": result.warnings,
                    "summary": _apply_production_summary(result),
                }, ensure_ascii=False))
            return 1

        if args.dry_run:
            if fmt == "json":
                print(json.dumps({
                    "success": True,
                    "dry_run": True,
                    "skit_group_placements": result.skit_group_placements,
                    "skit_group_item_insertions": result.skit_group_item_insertions,
                    "warnings": result.warnings,
                    "summary": _apply_production_summary(result),
                }, ensure_ascii=False))
            else:
                print("(dry-run: no file written)")
            return 0

        out_path = args.output
        if not out_path:
            stem = Path(args.production_ymmp).stem
            out_path = str(Path(args.production_ymmp).parent / f"{stem}_patched.ymmp")
        save_ymmp(ymmp_data, out_path)
        if fmt == "json":
            print(json.dumps({
                "success": True,
                "output": out_path,
                "skit_group_placements": result.skit_group_placements,
                "skit_group_item_insertions": result.skit_group_item_insertions,
                "warnings": result.warnings,
                "summary": _apply_production_summary(result),
            }, ensure_ascii=False))
        else:
            print(f"Written: {out_path}")
        return 0

    # --- G-19: face_map_bundle の解決 ---
    face_map_bundle: dict[str, dict] | None = None
    char_default_bodies: dict[str, str] | None = None
    if getattr(args, "face_map_bundle", None):
        if args.face_map:
            print("Error: --face-map and --face-map-bundle are mutually exclusive",
                  file=sys.stderr)
            return 1
        face_map_bundle, char_default_bodies = _load_face_map_bundle(args.face_map_bundle)
        print(f"face_map_bundle: {args.face_map_bundle} ({len(face_map_bundle)} bodies)")

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

    motion_map: dict[str, dict] = {}
    if getattr(args, "motion_map", None):
        motion_map = _load_adapter_motion_map(args.motion_map)
        print(f"motion_map (G-17): {args.motion_map} ({len(motion_map)} labels)")
    tachie_motion_effects_map = None
    if getattr(args, "tachie_motion_map", None):
        tachie_motion_effects_map = _load_tachie_motion_effects_map(
            args.tachie_motion_map,
        )
        print(
            f"tachie_motion_map: {args.tachie_motion_map} "
            f"({len(tachie_motion_effects_map)} labels)",
        )
    transition_map: dict[str, dict] = {}
    if getattr(args, "transition_map", None):
        with open(args.transition_map, "r", encoding="utf-8") as f:
            transition_map = json.load(f)
        print(f"transition_map: {args.transition_map} ({len(transition_map)} labels)")
    bg_anim_map: dict[str, dict] = {}
    if getattr(args, "bg_anim_map", None):
        with open(args.bg_anim_map, "r", encoding="utf-8") as f:
            bg_anim_map = json.load(f)
        print(f"bg_anim_map: {args.bg_anim_map} ({len(bg_anim_map)} labels)")
    group_motion_map: dict[str, dict] = {}
    if getattr(args, "group_motion_map", None):
        group_motion_map = _load_group_motion_map(args.group_motion_map)
        print(
            f"group_motion_map: {args.group_motion_map} "
            f"({len(group_motion_map)} labels)"
        )
    skit_group_registry_data = None
    skit_group_template_source_data = None
    known_skit_group_motion_labels = None
    if getattr(args, "skit_group_registry", None):
        skit_group_registry_data, known_skit_group_motion_labels = (
            _load_skit_group_registry_contract(args.skit_group_registry)
        )
        print(
            f"skit_group_registry: {args.skit_group_registry} "
            f"({len(known_skit_group_motion_labels)} labels)"
        )
    if getattr(args, "skit_group_template_source", None):
        if skit_group_registry_data is None:
            print(
                "Error: --skit-group-template-source requires --skit-group-registry",
                file=sys.stderr,
            )
            return 1
        skit_group_template_source_data = load_ymmp(args.skit_group_template_source)
        print(f"skit_group_template_source: {args.skit_group_template_source}")

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
    known_motion_keys: set[str] = set()
    if motion_map:
        known_motion_keys.update(motion_map.keys())
    if tachie_motion_effects_map:
        known_motion_keys.update(tachie_motion_effects_map.keys())
    known_motion_labels = known_motion_keys or None
    known_group_motion_labels = set(group_motion_map) if group_motion_map else None
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
        known_motion_labels=known_motion_labels,
        known_group_motion_labels=known_group_motion_labels,
        known_skit_group_motion_labels=known_skit_group_motion_labels,
        strict_skit_group_intents=getattr(args, "strict_skit_group_intents", False),
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
    fmt = getattr(args, "format", "text")

    skit_audit_result = None
    if getattr(args, "skit_group_registry", None) and skit_group_template_source_data is None:
        skit_audit_result = _run_skit_group_audit(
            ymmp_data,
            ir_data,
            args.skit_group_registry,
        )
        if fmt == "json":
            if skit_audit_result.status == "error":
                print(json.dumps({
                    "success": False,
                    "error": "skit_group_preflight_failed",
                    "skit_audit": _skit_audit_json_summary(skit_audit_result),
                }, ensure_ascii=False))
                return 1
        else:
            _print_skit_group_audit(skit_audit_result)
            if skit_audit_result.status == "error":
                print("\nSkit group preflight FAILED. Patch aborted.", file=sys.stderr)
                return 1

    result = patch_ymmp(
        ymmp_data,
        ir_data,
        face_map,
        bg_map,
        slot_map=slot_map,
        char_default_slots=char_default_slots or None,
        overlay_map=overlay_map,
        se_map=se_map,
        timeline_profile=getattr(args, "timeline_profile", None),
        motion_map=motion_map or None,
        transition_map=transition_map or None,
        bg_anim_map=bg_anim_map or None,
        group_motion_map=group_motion_map or None,
        timeline_contract_path=getattr(args, "timeline_contract", None),
        tachie_motion_effects_map=tachie_motion_effects_map,
        face_map_bundle=face_map_bundle,
        char_default_bodies=char_default_bodies,
        skit_group_registry=skit_group_registry_data,
        skit_group_template_source=skit_group_template_source_data,
        skit_group_compact_review=getattr(args, "skit_group_compact_review", False),
        skit_group_review_spacing=getattr(args, "skit_group_review_spacing", 240),
    )

    if fmt != "json":
        print(f"\nFace changes: {result.face_changes}")
        print(f"Slot changes: {result.slot_changes}")
        print(f"Overlay changes: {result.overlay_changes}")
        print(f"SE insertions: {result.se_plans}")
        if result.motion_changes or result.transition_changes or result.bg_anim_changes:
            print(
                f"Timeline adapter: motion={result.motion_changes}, "
                f"transition={result.transition_changes}, bg_anim={result.bg_anim_changes}"
            )
        if result.group_motion_changes:
            print(f"Group motion writes: {result.group_motion_changes}")
        if result.tachie_syncs:
            print(f"Idle face inserts: {result.tachie_syncs}")
        print(f"BG removed: {result.bg_changes}, BG added: {result.bg_additions}")
        print(f"BG anim writes: {result.bg_anim_changes}")
        print(f"Transition VoiceItem writes: {result.transition_changes}")
        print(f"VideoEffects writes (motion): {result.motion_changes}")
        print(f"GroupItem geometry writes: {result.group_motion_changes}")
        print(
            "Skit group placements: "
            f"{result.skit_group_placements} "
            f"(GroupItems inserted: {result.skit_group_item_insertions})"
        )
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
                "skit_group_placements": result.skit_group_placements,
                "skit_group_item_insertions": result.skit_group_item_insertions,
                "warnings": result.warnings,
                "summary": _apply_production_summary(result),
            }, ensure_ascii=False))
        return 1

    if args.dry_run:
        if fmt == "json":
            payload = {
                "success": True, "dry_run": True,
                "face_changes": result.face_changes,
                "slot_changes": result.slot_changes,
                "overlay_changes": result.overlay_changes,
                "se_plans": result.se_plans,
                "tachie_syncs": result.tachie_syncs,
                "bg_changes": result.bg_changes,
                "bg_additions": result.bg_additions,
                "bg_anim_changes": result.bg_anim_changes,
                "transition_changes": result.transition_changes,
                "motion_changes": result.motion_changes,
                "group_motion_changes": result.group_motion_changes,
                "skit_group_placements": result.skit_group_placements,
                "skit_group_item_insertions": result.skit_group_item_insertions,
                "warnings": result.warnings,
                "summary": _apply_production_summary(result),
            }
            if skit_audit_result is not None:
                payload["skit_audit"] = _skit_audit_json_summary(skit_audit_result)
            print(json.dumps(payload, ensure_ascii=False))
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
        payload = {
            "success": True,
            "output": out_path,
            "face_changes": result.face_changes,
            "slot_changes": result.slot_changes,
            "overlay_changes": result.overlay_changes,
            "se_plans": result.se_plans,
            "tachie_syncs": result.tachie_syncs,
            "bg_changes": result.bg_changes,
            "bg_additions": result.bg_additions,
            "bg_anim_changes": result.bg_anim_changes,
            "transition_changes": result.transition_changes,
            "motion_changes": result.motion_changes,
            "group_motion_changes": result.group_motion_changes,
            "skit_group_placements": result.skit_group_placements,
            "skit_group_item_insertions": result.skit_group_item_insertions,
            "warnings": result.warnings,
            "summary": _apply_production_summary(result),
        }
        if skit_audit_result is not None:
            payload["skit_audit"] = _skit_audit_json_summary(skit_audit_result)
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(f"Written: {out_path}")
    return 0


def _cmd_emit_packaging_brief_template(args: argparse.Namespace) -> int:
    """H-01 空テンプレを stdout または -o に書き出す。"""
    from src.pipeline.packaging_brief_template import emit_json_text, emit_markdown

    fmt = getattr(args, "format", "markdown")
    if fmt not in {"markdown", "json"}:
        raise ValueError(f"unsupported H-01 template format: {fmt}")

    # Guard: schema drift やテンプレ欠落はここで失敗させる。
    text = emit_json_text() if fmt == "json" else emit_markdown()
    out = getattr(args, "output", None)
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(text, encoding="utf-8")
        print(f"Written: {out}")
    else:
        sys.stdout.write(text)
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


def _cmd_score_thumbnail_s8(args: argparse.Namespace) -> int:
    """Lane E: S-8 thumbnail quality score."""
    payload: dict = {}
    if getattr(args, "payload", None):
        payload = json.loads(args.payload)
    if getattr(args, "payload_file", None):
        payload = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))

    category_scores = json.loads(args.scores)
    result = score_thumbnail_s8(payload, category_scores)

    fmt = getattr(args, "format", "text")
    if fmt == "json":
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"Thumbnail S-8 Score: {result.total_score}/100 ({result.band})")
        print("\nCategory scores:")
        for key, score in result.category_scores.items():
            print(f"  {key}: {score}/3")
        if result.warnings:
            print("\nWarnings:")
            for warning in result.warnings:
                print(f"  {warning}")
        if result.recommended_repairs:
            print("\nRecommended repairs:")
            for repair in result.recommended_repairs:
                print(f"  - {repair}")

    # PASS 条件: pass band かつ warning なし
    return 0 if (result.band == "pass" and not result.warnings) else 1


def cli_entry() -> None:
    """pyproject.toml scripts エントリポイント."""
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main())
