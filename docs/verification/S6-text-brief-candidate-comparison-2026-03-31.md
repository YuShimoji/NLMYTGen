# S-6 Text Brief Candidate Comparison

## Scope

- date: 2026-03-31
- purpose: S-6 の残 bottleneck に対して、次に proposal 化するならどの narrow text-only candidate が自然かを比較する
- mode: feasibility only
- owner: `assistant`

## Context

- B-15 Phase 1 により、section 分けと演出方針メモの初動はかなり軽くなった
- それでも S-6 では、素材選定・図作成・フリー素材探索・動画素材の尺つなぎが重い
- ただし、素材そのものの取得自動化は D-02 quarantined の論点と混ざりやすいため、次候補は text-only に寄せたほうが安全

## Candidate Comparison

| candidate | solves | likely output | overlap risk | evaluation ease | feasibility now |
|---|---|---|---|---|---|
| asset brief | 各 section で何を見せるべきかの具体化 | 必須モチーフ、優先順位、避けたい表現、静止画で良い区間 | B-15 cue memo と近い | high | high |
| diagram brief | 図作成前の設計コスト削減 | 図の目的、見出し、ラベル案、比較軸、誤読防止メモ | cue memo と重なりにくい | medium-high | medium-high |
| search query brief | フリー素材探索の初動短縮 | 検索語、除外語、採用基準、代替案 | asset brief と部分重複 | medium | medium |
| pacing brief | 動画素材の尺つなぎ計画 | 区間尺、差し替え候補、静止画許容区間、図へ逃がす区間 | 実編集に寄りすぎやすい | medium | medium-low |

## Recommended Order

1. `diagram brief`
2. `asset brief`
3. `search query brief`
4. `pacing brief`

## Why Diagram Brief Comes First

| point | rationale |
|---|---|
| pain fit | ユーザー観測では、図作成が特に重く、テンプレート化余地もありそう |
| overlap control | cue memo の「方向性」とは役割が分かれやすい |
| boundary fit | 図版そのものを作らず、図の text brief に限定しやすい |
| manual value | 人間は brief をもとに図を作るだけでも着手しやすくなる |

## Why Asset Brief Is Still Strong

- cue memo の `primary_background` より一段具体的に、「何が必須で何が不要か」を出せれば素材選定の迷いは減る
- 一方で、B-15 と近すぎると「同じことを粒度違いで二重にやる」リスクがある
- そのため、proposal 化するなら cue memo との差分を明確にする必要がある

## Candidate Boundaries

### diagram brief

- 許可:
  - 図の目的
  - 図に入れるべき項目
  - 比較軸やラベル案
  - 誤解を避けるための注意
- 禁止:
  - 画像生成
  - レイアウト自動化
  - 図版ファイルの生成

### asset brief

- 許可:
  - 主背景候補の優先順位
  - 補助素材の役割
  - 避けたい誤読や演出ノイズ
  - 静止画 / 図 / 動画の向き不向き
- 禁止:
  - 素材ダウンロード
  - 権利確認の自動化
  - YMM4 への配置

## Suggested Acceptance Shape

| candidate | minimal acceptance |
|---|---|
| diagram brief | 1 transcript で 1 つ以上の図区間を brief 化でき、人間が図の着手に使える |
| asset brief | 1 transcript で section ごとの素材選定メモが具体化し、候補迷いが減る |

## Do Not Merge Yet

- `diagram brief` と `asset brief` を最初から同一 feature にまとめない
- 自動取得や検索 API 連携を前提にしない
- B-15 Phase 2 rewrite と抱き合わせにしない

## Recommended Next Step

もし新しい narrow feature を 1 つだけ proposal 化するなら、最初の候補は `diagram brief` が自然。

理由は次の 3 点。

1. S-6 の重さの中でも図作成は独立した pain として見えやすい
2. B-15 cue memo との差分が説明しやすい
3. text-only boundary を守ったまま value path を検証しやすい
