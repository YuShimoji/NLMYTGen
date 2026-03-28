"""話者割当の精度評価スクリプト。

gold set（正解ラベル付きデータ）に対して、
各割当手法の line accuracy を計測する。

Usage:
    python -X utf8 tools/evaluate_diarization.py tools/gold_set_template.json

gold_set_template.json の speaker 欄を A/B で埋めてから実行すること。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# --- 定数 ---
SHORT_THRESHOLD = 3
TERMINAL_PUNCT = frozenset("。！？!?")

AIZUCHI_STARTS = {
    "ええ", "はい", "そうですね", "なるほど", "その通りです",
    "まさに", "分かりました", "うわあ", "いや",
}

QUESTION_ENDINGS = re.compile(
    r'(ですか[?？]?|でしょうか[?？]?|ですよね[?？]?|んですか[?？]?|ませんか[?？]?|[?？])$'
)


# --- ユーティリティ ---
def load_transcript(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines() if line.strip()]


def merge_short_lines(lines: list[str]) -> list[str]:
    merged: list[str] = []
    for line in lines:
        if merged and len(line) <= SHORT_THRESHOLD and line[-1] not in TERMINAL_PUNCT:
            merged[-1] = f"{merged[-1]}{line}"
        else:
            merged.append(line)
    return merged


# --- 割当手法 ---
def alternating(lines: list[str]) -> list[str]:
    """行交互（現行）。"""
    return ["A" if i % 2 == 0 else "B" for i in range(len(lines))]


def rule_v1_aizuchi_length(lines: list[str]) -> list[str]:
    """ルールベース v1: 文分断検出。

    前の行が句読点で終わらず、次の行が相槌でも質問でもない長文なら
    同一話者の連続発話と判定する。
    """
    if not lines:
        return []

    result = ["A"]
    for i in range(1, len(lines)):
        prev = lines[i - 1]
        curr = lines[i]
        prev_speaker = result[i - 1]
        next_speaker = "B" if prev_speaker == "A" else "A"

        starts_aizuchi = any(curr.startswith(p) for p in AIZUCHI_STARTS)

        # 文分断: 前行が未完結 + 次行が新発話の兆候なし
        if (len(prev) > 20
            and not prev.endswith(("。", "？", "?", "！", "!", "」"))
            and not starts_aizuchi
            and not QUESTION_ENDINGS.search(curr)
            and len(curr) > 20):
            next_speaker = prev_speaker

        result.append(next_speaker)
    return result


def rule_v2_resync(lines: list[str]) -> list[str]:
    """ルールベース v2: 文分断検出 + 再同期。

    v1 の問題（1箇所のずれが全行に波及する）を緩和する。
    文分断を検出した後、次に明確な話者交代の兆候が出たら交互に戻す。
    """
    if not lines:
        return []

    result = ["A"]
    shifted = False  # 交互からずれているか

    for i in range(1, len(lines)):
        prev = lines[i - 1]
        curr = lines[i]
        prev_speaker = result[i - 1]

        starts_aizuchi = any(curr.startswith(p) for p in AIZUCHI_STARTS)
        is_question = bool(QUESTION_ENDINGS.search(curr))
        is_short = len(curr) <= 10

        # デフォルト: 交互
        next_speaker = "B" if prev_speaker == "A" else "A"

        # 文分断検出: 同一話者の連続
        if (len(prev) > 20
            and not prev.endswith(("。", "？", "?", "！", "!", "」"))
            and not starts_aizuchi
            and not is_question
            and len(curr) > 20):
            next_speaker = prev_speaker
            shifted = True
        # 再同期: 明確な話者交代の兆候
        elif shifted and (is_short or starts_aizuchi or is_question):
            # 交代が明確 → 交互に戻す
            next_speaker = "B" if prev_speaker == "A" else "A"
            shifted = False

        result.append(next_speaker)
    return result


# 登録された全手法
METHODS = {
    "alternating": alternating,
    "rule_v1": rule_v1_aizuchi_length,
    "rule_v2_resync": rule_v2_resync,
}


# --- 評価 ---
def evaluate(gold: dict, transcript_path: Path):
    raw_lines = load_transcript(transcript_path)
    merged = merge_short_lines(raw_lines)

    # gold set から評価対象行を抽出
    gold_entries = [
        e for e in gold["lines"]
        if e.get("speaker") in ("A", "B")
    ]

    if not gold_entries:
        print("ERROR: gold set に有効なラベル (speaker: A/B) がありません。")
        print("gold_set_template.json の speaker 欄を A or B で埋めてください。")
        return

    # 結合後の行番号マッピング（元の行番号 → 結合後のインデックス）
    # 結合で消えた行は直前の行に吸収されている
    orig_to_merged = {}
    merged_idx = 0
    orig_idx = 0
    raw_i = 0
    temp_merged: list[str] = []
    for line in raw_lines:
        if temp_merged and len(line) <= SHORT_THRESHOLD and line[-1] not in TERMINAL_PUNCT:
            # この行は前の行に結合された
            orig_to_merged[raw_i + 1] = len(temp_merged) - 1  # 0-indexed
            temp_merged[-1] = f"{temp_merged[-1]}{line}"
        else:
            orig_to_merged[raw_i + 1] = len(temp_merged)  # 0-indexed
            temp_merged.append(line)
        raw_i += 1

    # 各手法の割当を生成
    method_results = {name: fn(merged) for name, fn in METHODS.items()}

    # 評価
    print(f"=== 話者割当 精度評価 ===")
    print(f"入力: {transcript_path.name}")
    print(f"全行数（結合後）: {len(merged)}")
    print(f"gold set ラベル数: {len(gold_entries)}")
    print()

    for method_name, assignments in method_results.items():
        correct = 0
        wrong = 0
        skipped = 0
        errors = []

        for entry in gold_entries:
            line_num = entry["line"]
            gold_speaker = entry["speaker"]

            if line_num not in orig_to_merged:
                skipped += 1
                continue

            merged_idx = orig_to_merged[line_num]
            if merged_idx >= len(assignments):
                skipped += 1
                continue

            predicted = assignments[merged_idx]
            if predicted == gold_speaker:
                correct += 1
            else:
                wrong += 1
                errors.append({
                    "line": line_num,
                    "gold": gold_speaker,
                    "predicted": predicted,
                    "text_preview": entry.get("text_preview", merged[merged_idx][:50]),
                    "confidence": entry.get("confidence", ""),
                })

        total = correct + wrong
        accuracy = correct / total * 100 if total > 0 else 0

        print(f"--- {method_name} ---")
        print(f"  正解: {correct} / {total} ({accuracy:.1f}%)")
        if skipped:
            print(f"  スキップ: {skipped} (結合で消えた行等)")

        if errors:
            print(f"  誤り ({len(errors)} 件):")
            for e in errors:
                conf = f" [{e['confidence']}]" if e["confidence"] else ""
                print(f"    L{e['line']:3d}: gold={e['gold']} pred={e['predicted']}{conf} | {e['text_preview']}")
        print()

    # --- ラベル反転検出 ---
    def _flip(s: str) -> str:
        return "B" if s == "A" else "A"

    def _score(assignments, entries, flip_gold=False):
        c, t = 0, 0
        for e in entries:
            ln = e["line"]
            gs = _flip(e["speaker"]) if flip_gold else e["speaker"]
            if ln not in orig_to_merged:
                continue
            mi = orig_to_merged[ln]
            if mi >= len(assignments):
                continue
            t += 1
            if assignments[mi] == gs:
                c += 1
        return c, t

    # 手法間の比較サマリー (両方向)
    print("=== 手法比較サマリー ===")
    print(f"{'手法':<20} {'直接':>10} {'反転':>10} {'best':>10}")
    print("-" * 54)
    best_scores = {}
    for method_name, assignments in method_results.items():
        c_d, t_d = _score(assignments, gold_entries, flip_gold=False)
        c_i, t_i = _score(assignments, gold_entries, flip_gold=True)
        acc_d = c_d / t_d * 100 if t_d else 0
        acc_i = c_i / t_i * 100 if t_i else 0
        best = max(acc_d, acc_i)
        orient = "direct" if acc_d >= acc_i else "inverted"
        best_scores[method_name] = (best, orient, max(c_d, c_i), t_d)
        print(f"{method_name:<20} {acc_d:>9.1f}% {acc_i:>9.1f}% {best:>9.1f}%")

    # 位相シフト分析
    print()
    print("=== 位相シフト分析 (alternating) ===")
    alt_assign = method_results["alternating"]
    prev_match = None
    shift_points = []
    for entry in sorted(gold_entries, key=lambda e: e["line"]):
        ln = entry["line"]
        gs = entry["speaker"]
        if ln not in orig_to_merged:
            continue
        mi = orig_to_merged[ln]
        if mi >= len(alt_assign):
            continue
        pred = alt_assign[mi]
        matches_direct = (pred == gs)
        if prev_match is not None and matches_direct != prev_match:
            shift_points.append(ln)
        prev_match = matches_direct

    if shift_points:
        print(f"  位相シフト検出: {len(shift_points)} 箇所")
        for sp in shift_points:
            print(f"    L{sp} 付近で direct/inverted が切り替わる")
    else:
        print("  位相シフトなし（全行が同一方向）")

    # 区間別精度
    print()
    print("=== 区間別精度 (alternating, best orientation per section) ===")
    sections = [
        ("L001-020", [e for e in gold_entries if 1 <= e["line"] <= 20]),
        ("L033-046", [e for e in gold_entries if 33 <= e["line"] <= 46]),
        ("L053-060", [e for e in gold_entries if 53 <= e["line"] <= 60]),
        ("L074-080", [e for e in gold_entries if 74 <= e["line"] <= 80]),
        ("L104-113", [e for e in gold_entries if 104 <= e["line"] <= 113]),
        ("L136-142", [e for e in gold_entries if 136 <= e["line"] <= 142]),
    ]
    for sec_name, sec_entries in sections:
        if not sec_entries:
            continue
        c_d, t_d = _score(alt_assign, sec_entries, flip_gold=False)
        c_i, t_i = _score(alt_assign, sec_entries, flip_gold=True)
        acc_d = c_d / t_d * 100 if t_d else 0
        acc_i = c_i / t_i * 100 if t_i else 0
        best = max(acc_d, acc_i)
        orient = "direct" if acc_d >= acc_i else "inverted"
        print(f"  {sec_name}: {best:5.1f}% ({orient}, {max(c_d,c_i)}/{t_d})")

    # 連続同一話者の検出
    print()
    print("=== 連続同一話者 (gold set 内) ===")
    sorted_entries = sorted(
        [e for e in gold_entries if e["line"] in orig_to_merged],
        key=lambda e: e["line"]
    )
    consecutive_runs = []
    for i in range(1, len(sorted_entries)):
        prev_e = sorted_entries[i - 1]
        curr_e = sorted_entries[i]
        # 連続する行番号 (gap=1) で同一話者
        if curr_e["line"] == prev_e["line"] + 1 and curr_e["speaker"] == prev_e["speaker"]:
            if consecutive_runs and consecutive_runs[-1][-1] == prev_e:
                consecutive_runs[-1].append(curr_e)
            else:
                consecutive_runs.append([prev_e, curr_e])
    if consecutive_runs:
        for run in consecutive_runs:
            lines = [e["line"] for e in run]
            speaker = run[0]["speaker"]
            print(f"  L{lines[0]}-L{lines[-1]}: speaker {speaker} が {len(run)} 行連続")
    else:
        print("  なし")

    # Go/No-Go 判定
    print()
    print("=== Gemini PoC 進行判定 ===")
    alt_best, alt_orient, alt_best_correct, alt_total = best_scores["alternating"]
    print(f"行交互 best accuracy: {alt_best:.1f}% ({alt_orient})")

    # 位相シフトを考慮した「パターン正答率」
    # 各区間の best を合算
    pattern_correct = 0
    pattern_total = 0
    for _, sec_entries in sections:
        c_d, t_d = _score(alt_assign, sec_entries, flip_gold=False)
        c_i, t_i = _score(alt_assign, sec_entries, flip_gold=True)
        pattern_correct += max(c_d, c_i)
        pattern_total += t_d
    pattern_acc = pattern_correct / pattern_total * 100 if pattern_total else 0
    print(f"行交互 パターン正答率 (区間別best合算): {pattern_acc:.1f}% ({pattern_correct}/{pattern_total})")
    print()

    threshold = 15.0
    print(f"判定基準:")
    if pattern_acc >= 95:
        print(f"  -> パターン正答率 {pattern_acc:.1f}% >= 95%")
        print(f"  -> 行交互のパターン自体は高精度。問題は位相シフトとラベル反転。")
        print(f"  -> LLM の価値: 位相シフト検出 + 連続同一話者の検出に限定される")
    elif pattern_acc >= 85:
        print(f"  -> パターン正答率 {pattern_acc:.1f}% >= 85%: LLM 導入の費用対効果は低い")
    elif pattern_acc >= 50:
        print(f"  -> パターン正答率 {pattern_acc:.1f}%: LLM 改善の余地あり (Go 候補)")
    else:
        print(f"  -> パターン正答率 {pattern_acc:.1f}% < 50%: S-2 品質改善が先")

    if shift_points:
        print(f"  -> 位相シフト {len(shift_points)} 箇所: ルールベースで検出・修正可能か要検討")
    if consecutive_runs:
        total_consec = sum(len(r) - 1 for r in consecutive_runs)
        print(f"  -> 連続同一話者 {total_consec} 箇所: 行交互では原理的に検出不能")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        gold_path = Path("tools/gold_set_template.json")
    else:
        gold_path = Path(sys.argv[1])

    if not gold_path.exists():
        print(f"Gold set not found: {gold_path}", file=sys.stderr)
        sys.exit(1)

    gold = json.loads(gold_path.read_text(encoding="utf-8"))

    # transcript パスを gold set から取得
    source = gold.get("_source", "")
    if source:
        transcript_path = Path(source)
    else:
        transcript_path = Path("samples/2026 Global Crisis Oil Markets, Air Security, and Conflict.txt")

    if not transcript_path.exists():
        print(f"Transcript not found: {transcript_path}", file=sys.stderr)
        sys.exit(1)

    evaluate(gold, transcript_path)
