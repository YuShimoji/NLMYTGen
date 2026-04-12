# H-01 レーンD C-07 入力記録（P01 Amazon · 2026-04-10）

目的: C-07 実行時に `brief -> script` の順を固定し、上位制約の適用漏れを防ぐ。

対象案件: `video_id` = `p0_phase1_amazon`（[P03-thumbnail-one-sheet-proof.md](P03-thumbnail-one-sheet-proof.md)・[P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) と整合）

## 前提（B-3）

- Custom GPT の Instructions に設定する v4 プロンプト本体が、[S6-production-memo-prompt.md](../S6-production-memo-prompt.md) フェンス内全文と一致していること（不一致なら先にレーン B で同期）。

## 入力順（固定）

1. `samples/packaging_brief_p0_amazon.md` の全文を貼る
2. `samples/The Amazon Panopticon Surveillance and the Modern Worker.txt` の全文を貼る

## 使用プロンプト正本

- `docs/S6-production-memo-prompt.md`
  - H-01 連携節
  - v4 プロンプト本体（フェンス内）

## 先頭入力ブロック（参照）

```text
[Packaging Orchestrator brief]
<samples/packaging_brief_p0_amazon.md の全文>

[Transcript]
<samples/The Amazon Panopticon Surveillance and the Modern Worker.txt の全文>
```

## 判定（手順充足 · repo 記録）

- brief が台本より先に与えられる運用が本文で固定されている: **yes**
- required_evidence を上位制約として扱う前提が成立: **yes**（brief 内で明示）

## メモ

- **C-09 後に refined 台本が正のとき**は [h01_lane_d_p01_amazon_c07_refined_input_2026-04-11.md](h01_lane_d_p01_amazon_c07_refined_input_2026-04-11.md) を参照（貼付順は同じく brief 先）。
- 実際の Custom GPT セッション URL や生成ログはオペレータ環境に残す。本 repo では上記パスと貼付順のみを正本とする。
