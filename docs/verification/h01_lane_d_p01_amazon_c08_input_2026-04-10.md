# H-01 レーンD C-08 入力記録（P01 Amazon · 2026-04-10）

目的: C-08 実行時に `brief -> script` の順を固定し、コピー案の drift を抑制する。

対象案件: `video_id` = `p0_phase1_amazon`

## 前提（B-3 / B-5）

- C-07 と同様、演出メモ用 GPT の v4 は [S6-production-memo-prompt.md](../S6-production-memo-prompt.md) と一致。
- サムネコピー用プロンプトは [S8-thumbnail-copy-prompt.md](../S8-thumbnail-copy-prompt.md) 正本と一致（[OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) B-5）。

## 入力順（固定）

1. `samples/packaging_brief_p0_amazon.md` の全文を貼る
2. `samples/The Amazon Panopticon Surveillance and the Modern Worker.txt` の全文を貼る

## 使用プロンプト正本

- `docs/S8-thumbnail-copy-prompt.md`
  - H-01 連携節
  - プロンプト本体（Specificity Ledger / Brief Compliance Check 含む）

## 先頭入力ブロック（参照）

```text
[Packaging Orchestrator brief]
<samples/packaging_brief_p0_amazon.md の全文>

[Transcript]
<samples/The Amazon Panopticon Surveillance and the Modern Worker.txt の全文>
```

## 判定（手順充足 · repo 記録）

- brief が台本より先に与えられる運用が本文で固定されている: **yes**
- banned_copy_patterns を先頭制約として扱う前提が成立: **yes**

## メモ

- **C-09 後に refined 台本が正のとき**は [h01_lane_d_p01_amazon_c08_refined_input_2026-04-11.md](h01_lane_d_p01_amazon_c08_refined_input_2026-04-11.md) を参照。
- 採用したコピー案の保存先はオペレータ任意。lexical チェックは `banned_copy_patterns` との突合を推奨。
