# B-16 Proposal: Diagram Brief Packet for S-6

## Why This Exists

B-15 Phase 1 により、S-6 の section 分けや背景方向の初動はかなり短縮できた。
一方で、図作成については次の pain が独立して残っている。

- どの区間で図を使うべきかの見極め
- 図に何を書くべきかの整理
- ラベルや比較軸の設計
- 図を作り始めるまでの白紙時間

ここで欲しいのは図版の生成ではなく、図作成前に人間が参照する text-only の brief である。

## Value Path

| 観点 | 狙い |
|---|---|
| どこに効くか | S-6 の図作成前メモ |
| 何を減らすか | 図の目的整理、構成メモ、ラベル設計の初動時間 |
| 手作業は何が残るか | 図版作成、レイアウト、素材選定、最終採否判断 |
| なぜ今やるか | B-15 と役割が分かれやすく、図作成は独立した bottleneck として観測されているため |

## Difference From B-15

| item | B-15 cue memo | B-16 diagram brief |
|---|---|---|
| 主目的 | section ごとの演出方針を決めやすくする | 図区間で「何を図にするか」を決めやすくする |
| 粒度 | section 全体 | 図に向く局所論点 |
| 出力 | 背景・感情・転換・operator note | 図の目的・比較軸・ラベル案・誤読防止メモ |
| 使う場所 | S-6 の全体方針決め | S-6 で図を作る直前 |
| やらないこと | YMM4 direct edit、画像生成 | 同左 |

## Recommended Scope

- transcript または cue memo を入力に取り、図に向く区間だけを text brief 化する
- 出力は Markdown / JSON / plain text のみ
- 返す内容は、図の目的、入れる項目、比較軸、ラベル案、誤読防止メモ
- 図版そのものは作らない

## Proposal Scope

### やる

- 図作成 bottleneck を text-only brief として切り出す
- B-15 cue memo との差分を明文化する
- output contract と proof 条件を先に定義する
- 画像生成や自動取得に滑らない narrow candidate として扱う

### やらない

- 画像生成
- 図版ファイル生成
- レイアウト自動化
- 素材ダウンロード
- YMM4 への配置
- D-02 の取得自動化との統合

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

## Workflow Insertion

| step | actor | owner artifact | note |
|---|---|---|---|
| S-6a pre-figure | tool | text brief | transcript または cue memo を受ける |
| S-6a | user | figure draft / visual notes | brief を見ながら図を起こす |
| S-6 | user | YMM4 project | 図版を含む演出判断を行う |

## Acceptance

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
| 汎化しすぎる | 抽象論だけだと着手コストは下がらない |
| 視覚生成へ滑る | 「図」から画像生成へ拡張しやすい |
| proof が曖昧 | 図作成時間のどこが減ったのかを記録しづらい |

## Recommendation

1. `B-16` を `proposed` として FEATURE_REGISTRY に登録する
2. 最初は text-only brief に限定し、画像や取得機能に広げない
3. B-15 と混ぜず、独立した narrow candidate として proof 条件を持たせる
4. 実装判断は approval 後に行う

## Minimal Ask

次に必要な判断は 1 点でよい。

- `B-16 Diagram Brief Packet` を次 frontier 候補として approved に進めるか
