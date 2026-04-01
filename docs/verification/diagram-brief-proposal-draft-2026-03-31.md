# Diagram Brief Proposal Draft

## Scope

- date: 2026-03-31
- status: draft only
- purpose: S-6 の図作成 bottleneck を text-only 支援として切り出せるかを判断しやすくする
- owner: `assistant`

## Why This Exists

B-15 Phase 1 により、動画全体の section 分けや背景方向の初動はかなり短縮できた。
一方で、S-6 では次の pain が独立して残っている。

- 図を入れるべき区間の見極め
- 図に何を書くかの整理
- ラベルや比較軸の設計
- 図を作り始めるまでの「白紙時間」

ここで欲しいのは図版の生成ではなく、図作成前に人間が参照する text brief である。

## Difference From B-15

| item | B-15 cue memo | diagram brief draft |
|---|---|---|
| 主目的 | section ごとの演出方針を決めやすくする | 図区間で「何を図にするか」を決めやすくする |
| 粒度 | section 全体 | 図に向く局所論点 |
| 出力 | 背景・感情・転換・operator note | 図の目的・ラベル案・比較軸・誤読防止メモ |
| 使う場所 | S-6 の全体方針決め | S-6 で図を作る直前 |
| やらないこと | YMM4 direct edit、画像生成 | 同左 |

## Value Path

| 観点 | 狙い |
|---|---|
| どこに効くか | S-6 の図作成前メモ |
| 何を減らすか | 図に何を入れるか考える時間、図の構成メモ作成の手間 |
| 手作業は何が残るか | 図版作成、レイアウト、素材選定、最終判断 |
| なぜ今やるか | B-15 と役割が分かれやすく、図作成は独立した bottleneck として観測されているため |

## Minimal Scope

- transcript または cue memo を入力に取り、図に向く区間だけを text brief 化する
- 出力は Markdown / JSON / plain text のみ
- 返す内容は、図の目的、入れる項目、比較軸、ラベル案、誤読防止メモ
- 図版そのものは作らない

## Explicit Non-Goals

- 画像生成
- 図版ファイル生成
- YMM4 への配置
- 素材ダウンロード
- レイアウト自動化

## Output Contract Draft

### top-level

- `summary`: 図を使うべき区間の短い要約
- `diagram_briefs[]`: 各図区間の brief
- `global_notes`: 図を多用しすぎないための注意
- `operator_todos`: 人間が確認すべき点

### diagram_briefs[]

- `diagram_id`
- `topic`
- `source_section`
- `goal`
- `recommended_format`
- `must_include`
- `comparison_axes`
- `label_suggestions`
- `avoid_misread`
- `operator_note`

## Acceptance Draft

| ID | 条件 |
|---|---|
| AC-1 | 出力は text artifact のみで、画像や図版ファイルを生成しない |
| AC-2 | B-15 cue memo との差分が説明できる |
| AC-3 | 1 transcript で 1 つ以上の図区間を brief 化できる |
| AC-4 | operator が「図作成に着手するまでの時間が減ったか」を記録できる |
| AC-5 | D-02 の取得自動化や YMM4 direct edit に滑らない |

## Risks

| risk | note |
|---|---|
| B-15 と重複する | cue memo の粒度違いに見えると feature 分離の意味が薄い |
| 汎化しすぎる | どの動画にも当てはまる抽象論だけだと役に立たない |
| 視覚生成へ滑る | 「図を出す」話が図版生成へ拡張しやすい |
| proof が曖昧 | 図作成時間のどこが減ったのかを記録しづらい |

## Recommended Evaluation

1. cue memo だけで図を作る場合の準備時間を概算する
2. diagram brief を使った場合の着手時間を記録する
3. 役に立ったのが `goal / must_include / label_suggestions / avoid_misread` のどれかを短く残す

## Recommendation

次に 1 つだけ narrow candidate を proposal 化するなら、この draft は有力。
ただし、まだ draft 止まりに留めるのが自然で、次の判断は次の 1 点に絞れる。

- `diagram brief` を FEATURE_REGISTRY の新規 `proposed` 候補として起こすか
