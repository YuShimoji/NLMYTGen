"""話者割当の精度分析ツール。

既存の行交互割当と、ルールベースの改善案を比較する。
ground truth（音声確認）がないため、「疑わしい箇所」の特定に留める。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# 相槌・短応答パターン（聞き手の発話を示唆）
AIZUCHI_STARTS = {
    "ええ", "はい", "そうですね", "なるほど", "その通りです",
    "まさに", "分かりました", "うわあ", "いや",
}

# 質問終端パターン
QUESTION_ENDINGS = re.compile(r'(ですか[?？]?|でしょうか[?？]?|ですよね[?？]?|んですか[?？]?|ませんか[?？]?|[?？])$')

# 確認・合意パターン（話題を受ける側）
AGREEMENT_PATTERNS = {"その通りです", "まさにその通りです", "完璧な指摘です", "非常に鋭い"}

# 話題転換パターン（進行役の行動）
TRANSITION_PATTERNS = {"というわけで", "ではここから", "そこで最後に"}

# 結合閾値
SHORT_THRESHOLD = 3
TERMINAL_PUNCT = frozenset("。！？!?")


def load_transcript(path: Path) -> list[str]:
    """テキストファイルを行リストとして読み込む。"""
    text = path.read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines() if line.strip()]


def merge_short_lines(lines: list[str]) -> list[str]:
    """短行結合（現行の normalize.py と同じロジック）。"""
    merged: list[str] = []
    for line in lines:
        if merged and len(line) <= SHORT_THRESHOLD and line[-1] not in TERMINAL_PUNCT:
            merged[-1] = f"{merged[-1]}{line}"
        else:
            merged.append(line)
    return merged


def classify_line(line: str) -> dict:
    """各行の特徴を分類する。"""
    features = {
        "length": len(line),
        "is_short": len(line) <= 10,
        "is_very_short": len(line) <= 5,
        "starts_with_aizuchi": False,
        "is_question": bool(QUESTION_ENDINGS.search(line)),
        "is_agreement": False,
        "is_transition": False,
    }

    for pattern in AIZUCHI_STARTS:
        if line.startswith(pattern):
            features["starts_with_aizuchi"] = True
            break

    for pattern in AGREEMENT_PATTERNS:
        if pattern in line:
            features["is_agreement"] = True
            break

    for pattern in TRANSITION_PATTERNS:
        if line.startswith(pattern):
            features["is_transition"] = True
            break

    return features


def alternating_assignment(lines: list[str]) -> list[str]:
    """行交互割当（現行方式）。"""
    speakers = ("A", "B")
    return [speakers[i % 2] for i in range(len(lines))]


def rule_based_assignment(lines: list[str]) -> list[str]:
    """ルールベース割当（PoC）。

    方針:
    - 基本は行交互
    - ただし「前の行と同じ話者が続けて話している」と判断できる場合は
      交互を崩して同じ話者に割り当てる
    """
    if not lines:
        return []

    assignments = ["A"]  # 最初の行はA
    features = [classify_line(line) for line in lines]

    for i in range(1, len(lines)):
        prev_speaker = assignments[i - 1]
        prev_feat = features[i - 1]
        curr_feat = features[i]

        # デフォルト: 交互
        next_speaker = "B" if prev_speaker == "A" else "A"

        # ルール1: 前の行が非常に短い反応（≤5文字）で、
        #          現在の行が長い説明（≥30文字）なら、
        #          前の行と現在の行は別話者（交互のまま）
        # → デフォルト動作なので何もしない

        # ルール2: 前の行が長い説明で途中で切れている感じ
        #          (句読点で終わらず、次の行が前の行の続きっぽい)
        if (prev_feat["length"] > 20 and
            not lines[i-1].endswith(("。", "？", "?", "！", "!")) and
            not curr_feat["is_question"] and
            not curr_feat["starts_with_aizuchi"] and
            curr_feat["length"] > 20):
            # 前の行の続きかもしれない → 同じ話者
            next_speaker = prev_speaker

        # ルール3: 前の行が質問で終わっていて、
        #          現在の行がそれに答えている場合は交互（別話者）
        # → デフォルト動作なので何もしない

        # ルール4: 現在の行が「はい。」「ええ。」のみ（超短応答）で
        #          前の行が質問だった場合 → 交互のまま
        # → デフォルト動作

        # ルール5: 連続する短い反応（両方≤10文字）は同じ話者の可能性
        if (prev_feat["is_very_short"] and
            curr_feat["is_very_short"] and
            not curr_feat["starts_with_aizuchi"]):
            next_speaker = prev_speaker

        assignments.append(next_speaker)

    return assignments


def analyze(transcript_path: Path):
    """分析を実行して結果を表示する。"""
    raw_lines = load_transcript(transcript_path)
    merged = merge_short_lines(raw_lines)

    print(f"=== 話者割当分析 ===")
    print(f"入力ファイル: {transcript_path.name}")
    print(f"元の行数: {len(raw_lines)}")
    print(f"結合後の行数: {len(merged)}")
    print()

    # 特徴分析
    features = [classify_line(line) for line in merged]

    # 統計
    lengths = [f["length"] for f in features]
    short_count = sum(1 for f in features if f["is_short"])
    very_short_count = sum(1 for f in features if f["is_very_short"])
    aizuchi_count = sum(1 for f in features if f["starts_with_aizuchi"])
    question_count = sum(1 for f in features if f["is_question"])

    print(f"--- 行の特徴統計 ---")
    print(f"  平均文字数: {sum(lengths)/len(lengths):.1f}")
    print(f"  最短: {min(lengths)} / 最長: {max(lengths)}")
    print(f"  短い行 (10文字以下): {short_count} ({short_count*100/len(merged):.1f}%)")
    print(f"  非常に短い行 (5文字以下): {very_short_count} ({very_short_count*100/len(merged):.1f}%)")
    print(f"  相槌で始まる行: {aizuchi_count} ({aizuchi_count*100/len(merged):.1f}%)")
    print(f"  質問で終わる行: {question_count} ({question_count*100/len(merged):.1f}%)")
    print()

    # 割当の比較
    alt = alternating_assignment(merged)
    rule = rule_based_assignment(merged)

    diff_count = sum(1 for a, r in zip(alt, rule) if a != r)
    print(f"--- 割当比較 ---")
    print(f"  行交互とルールベースの差分: {diff_count} 行 ({diff_count*100/len(merged):.1f}%)")
    print()

    if diff_count > 0:
        print(f"--- 差分の詳細 ---")
        for i, (a, r) in enumerate(zip(alt, rule)):
            if a != r:
                line = merged[i]
                preview = line[:60] + ("..." if len(line) > 60 else "")
                print(f"  L{i+1:3d}: 交互={a} → ルール={r} | {len(line):3d}文字 | {preview}")
        print()

    # 疑わしい箇所の特定
    print(f"--- 疑わしい箇所（行交互の弱点候補）---")
    suspicious = []
    for i in range(1, len(merged)):
        prev = merged[i - 1]
        curr = merged[i]
        prev_f = features[i - 1]
        curr_f = features[i]

        reasons = []

        # 疑い1: 前の行が文中で切れている + 次の行が続きっぽい
        if (not prev.endswith(("。", "？", "?", "！", "!", "」")) and
            not curr_f["starts_with_aizuchi"] and
            not curr_f["is_question"] and
            prev_f["length"] > 15 and curr_f["length"] > 15):
            reasons.append("文が途中で切れて次行に続いている可能性")

        # 疑い2: 同一の発話スタイルが連続（両方相槌 or 両方長い説明）
        if (prev_f["starts_with_aizuchi"] and curr_f["starts_with_aizuchi"] and
            prev_f["length"] > 20 and curr_f["length"] > 20):
            reasons.append("両方とも相槌+長文で同一話者の連続発話の可能性")

        # 疑い3: "はい。" → 長い説明（同一話者が「はい。」で始めて説明を続けるパターン）
        if (prev_f["is_very_short"] and prev.startswith(("はい", "ええ")) and
            curr_f["length"] > 30 and not curr_f["starts_with_aizuchi"]):
            # これは交互が正しいパターンも多い。
            # ただし prev が独立した発話で curr が質問への回答なら交互が正しい。
            # prev が「話の繋ぎ」で curr が同じ人の本論なら同一話者。
            # 判別が難しいケース。
            reasons.append("短い相槌→長い説明: 別話者の応答か同一話者の前置きか不明")

        if reasons:
            suspicious.append((i, reasons))

    if suspicious:
        for idx, reasons in suspicious:
            prev_preview = merged[idx - 1][:40]
            curr_preview = merged[idx][:40]
            print(f"  L{idx:3d}-{idx+1:3d}:")
            print(f"    前: [{alt[idx-1]}] {prev_preview}...")
            print(f"    次: [{alt[idx]}] {curr_preview}...")
            for r in reasons:
                print(f"    → {r}")
            print()
    else:
        print("  なし")

    # A/B の文字数・行数統計（行交互版）
    print(f"--- 話者バランス（行交互版）---")
    for speaker in ("A", "B"):
        lines_s = [merged[i] for i in range(len(merged)) if alt[i] == speaker]
        chars = sum(len(l) for l in lines_s)
        avg = chars // len(lines_s) if lines_s else 0
        print(f"  Speaker_{speaker}: {len(lines_s)} 行, {chars} 文字 (平均 {avg} 文字/行)")

    print()
    print(f"--- 話者バランス（ルールベース版）---")
    for speaker in ("A", "B"):
        lines_s = [merged[i] for i in range(len(merged)) if rule[i] == speaker]
        chars = sum(len(l) for l in lines_s)
        avg = chars // len(lines_s) if lines_s else 0
        print(f"  Speaker_{speaker}: {len(lines_s)} 行, {chars} 文字 (平均 {avg} 文字/行)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        path = Path("samples/2026 Global Crisis Oil Markets, Air Security, and Conflict.txt")
    else:
        path = Path(sys.argv[1])

    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    analyze(path)
