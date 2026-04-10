# H-01 レーンD C-08 入力記録（2026-04-09）

目的: C-08 実行時に `brief -> script` の順を固定し、コピー案の drift を抑制する。

## 入力順（固定）
1. `samples/packaging_brief_ai_monitoring.md` の全文を貼る
2. `samples/AI監視が追い詰める生身の労働.txt` の全文を貼る

## 使用プロンプト正本
- `docs/S8-thumbnail-copy-prompt.md`
  - H-01 連携節
  - プロンプト本体（Specificity Ledger / Brief Compliance Check 含む）

## 先頭入力ブロック（参照）
```text
[Packaging Orchestrator brief]
<samples/packaging_brief_ai_monitoring.md の全文>

[Transcript]
<samples/AI監視が追い詰める生身の労働.txt の全文>
```

## 判定
- brief が台本より先に与えられている: yes
- banned_copy_patterns を先頭制約として扱う前提が成立: yes
