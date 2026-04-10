# H-01 レーンD C-07 入力記録（2026-04-09）

目的: C-07 実行時に `brief -> script` の順を固定し、上位制約の適用漏れを防ぐ。

## 入力順（固定）
1. `samples/packaging_brief_ai_monitoring.md` の全文を貼る
2. `samples/AI監視が追い詰める生身の労働.txt` の全文を貼る

## 使用プロンプト正本
- `docs/S6-production-memo-prompt.md`
  - H-01 連携節
  - v4 プロンプト本体（フェンス内）

## 先頭入力ブロック（参照）
```text
[Packaging Orchestrator brief]
<samples/packaging_brief_ai_monitoring.md の全文>

[Transcript]
<samples/AI監視が追い詰める生身の労働.txt の全文>
```

## 判定
- brief が台本より先に与えられている: yes
- required_evidence を上位制約として扱う前提が成立: yes
