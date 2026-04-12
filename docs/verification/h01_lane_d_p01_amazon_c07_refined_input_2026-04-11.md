# H-01 レーンD C-07 入力記録（P01 Amazon · refined 経路 · 2026-04-11）

目的: レーンAで **C-09 相当の refined 台本**が正になる案件で、`brief -> refined script` の順を固定する。

対象案件: `video_id` = `p0_phase1_amazon`（[P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) の `lane_a_amazon_2026-04-10_b` と整合）

## 前提（B-3）

- Custom GPT の Instructions に設定する v4 プロンプト本体が、[S6-production-memo-prompt.md](../S6-production-memo-prompt.md) フェンス内全文と一致していること（不一致なら先にレーン B で同期）。

## 入力順（固定）

1. `samples/packaging_brief_p0_amazon.md` の全文を貼る
2. `samples/amazon_panopticon_lane_a_refined.txt` の全文を貼る（生 ASR ではなく **レーンA確定稿**）

## 使用プロンプト正本

- `docs/S6-production-memo-prompt.md`
  - H-01 連携節
  - v4 プロンプト本体（フェンス内）

## 先頭入力ブロック（参照）

```text
[Packaging Orchestrator brief]
<samples/packaging_brief_p0_amazon.md の全文>

[Transcript]
<samples/amazon_panopticon_lane_a_refined.txt の全文>
```

## 判定（手順充足 · repo 記録）

- brief が台本より先に与えられる運用が本文で固定されている: **yes**
- required_evidence を上位制約として扱う前提が成立: **yes**（brief 内で明示）
- refined でも opening に吸入器逸話・71.4% 等が残り `alignment_check` と矛盾しない: **yes**（冒頭照合は [H01-packaging-orchestrator-workflow-proof.md](H01-packaging-orchestrator-workflow-proof.md) Lane D P01 Amazon の refined 節を参照）

## メモ

- 生台本のみを渡す記録は [h01_lane_d_p01_amazon_c07_input_2026-04-10.md](h01_lane_d_p01_amazon_c07_input_2026-04-10.md)。**本番で refined が先に確定している場合は本ファイルの順を正とする。**
- 実際の Custom GPT セッション URL や生成ログはオペレータ環境に残す。
