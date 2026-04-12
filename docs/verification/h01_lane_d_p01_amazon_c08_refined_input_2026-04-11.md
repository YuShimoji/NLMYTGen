# H-01 レーンD C-08 入力記録（P01 Amazon · refined 経路 · 2026-04-11）

目的: C-08 実行時に `brief -> refined script` の順を固定し、サムネコピー案が **確定台本**と突合できるようにする。

対象案件: `video_id` = `p0_phase1_amazon`

## 前提（B-3 / B-5）

- C-07 と同様、演出メモ用 GPT の v4 は [S6-production-memo-prompt.md](../S6-production-memo-prompt.md) と一致。
- サムネコピー用プロンプトは [S8-thumbnail-copy-prompt.md](../S8-thumbnail-copy-prompt.md) 正本と一致（[OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) B-5）。

## 入力順（固定）

1. `samples/packaging_brief_p0_amazon.md` の全文を貼る
2. `samples/amazon_panopticon_lane_a_refined.txt` の全文を貼る

## 使用プロンプト正本

- `docs/S8-thumbnail-copy-prompt.md`
  - H-01 連携節
  - プロンプト本体（Specificity Ledger / Brief Compliance Check 含む）

## 先頭入力ブロック（参照）

```text
[Packaging Orchestrator brief]
<samples/packaging_brief_p0_amazon.md の全文>

[Transcript]
<samples/amazon_panopticon_lane_a_refined.txt の全文>
```

## 判定（手順充足 · repo 記録）

- brief が台本より先に与えられる運用が本文で固定されている: **yes**
- banned_copy_patterns を先頭制約として扱う前提が成立: **yes**
- `preferred_specifics`（71.4%, 19億ドル, 9%, 1.61倍）が refined 本文でも参照可能: **yes**（数値・構成は生稿と同系）

## メモ

- 生台本のみを渡す記録は [h01_lane_d_p01_amazon_c08_input_2026-04-10.md](h01_lane_d_p01_amazon_c08_input_2026-04-10.md)。**採用コピー案の最終確定は人（[B11-manual-checkpoints.md](../B11-manual-checkpoints.md)）。**
- 採用したコピー案の保存先はオペレータ任意。lexical チェックは `banned_copy_patterns` との突合を推奨。
