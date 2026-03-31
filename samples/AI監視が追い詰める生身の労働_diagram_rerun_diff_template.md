# B-16 Rerun Diff Template

更新後 packet に対する rerun 結果を、baseline と比較して短く残すための雛形。

## Raw Result

- response file: `AI監視が追い詰める生身の労働_diagram_brief_rerun_received.md`
- received date: 2026-03-31

## Diff Against Baseline

| 項目 | baseline | rerun | 差分メモ |
|---|---|---|---|
| selected diagram count | 3 | 3 | 変化なし |
| selected sections | S1, S2, S3 | S1-S2, S3, S3 | 導入を単独図にせず、監視構造として S1-S2 を統合 |
| excluded sections | S4, S5 | intro-only section を除外、終盤の抽象締めも除外 | 背景で足りる区間をさらに外せている |
| goal clarity | high | high | 目的は維持。因果・構造の焦点はむしろ明瞭 |
| must_include density | 3-5 が中心 | 4 が中心 | 扱いやすい密度に収束 |
| label usefulness | medium-high | high | そのまま図ラベルにしやすい粒度へ改善 |
| avoid_misread usefulness | high | high | 構造誤読の防止として引き続き有効 |

## Quick Judgment

- better: 背景で足りる導入を外し、図化する理由がある区間だけにさらに絞られた
- unchanged: 図数は 3 のままで、goal / avoid_misread の有用性は引き続き高い
- worse: source_section が `S3` に 2 図重なるため、section 単位の参照だけだと少し粗い

## Decision Hint

- rerun で改善していれば:
  - diagram brief の対象 section 絞り込みは概ね収束
- rerun でも図にしなくてよい section を拾うなら:
  - response preference をさらに強める余地あり
- rerun が B-15 cue memo と似すぎるなら:
  - role separation を packet 文言でさらに明示する
