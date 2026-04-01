# B-17 Proposal: Asset Brief Packet for S-6

## Why This Exists

B-15 は S-6 の方針メモ化を短縮し、B-16 は図作成前の planning を短縮した。
その後も残る主 pain は、各 section で「何を見せるべきか」を素材選定前に具体化する工程である。

ここで欲しいのは素材の自動取得ではなく、人間が素材選定に入る前に参照する text-only の asset brief である。

## Value Path

| 観点 | 狙い |
|---|---|
| どこに効くか | S-6 の素材選定前メモ |
| 何を減らすか | section ごとの主背景・補助素材・図/動画/静止画の向き不向きに迷う時間 |
| 手作業は何が残るか | 実素材探索、採否判断、YMM4 への配置、演出判断 |
| なぜ今やるか | B-16 rerun で図対象の絞り込みは概ね収束し、次の bottleneck が図以外の素材選定前整理へ移ったため |

## Difference From Existing Features

| item | B-15 cue memo | B-16 diagram brief | B-17 asset brief |
|---|---|---|---|
| 主目的 | section の演出方向を決めやすくする | 図区間で何を図にするか決めやすくする | 素材選定前に何を見せるか具体化する |
| 出力中心 | background / supporting visual / emotion / transition | goal / must_include / label / avoid_misread | 必須モチーフ / 素材種別優先順位 / 図や動画へ逃がすべき条件 |
| 使う場所 | S-6 全体の初動 | 図作成直前 | 素材探しに入る直前 |
| やらないこと | direct edit / image generation | 同左 | 同左 + 検索実行 / ダウンロード |

## Recommended Scope

- transcript または cue memo を入力に取り、section ごとの素材選定前メモを返す
- 出力は Markdown / JSON / plain text のみ
- 返す内容は、主背景の意図、補助素材の役割、図 / 動画 / 静止画の向き不向き、避けたい誤読やノイズ

## Output Contract Draft

### top-level

- `summary`
- `section_asset_briefs[]`
- `global_notes`
- `operator_todos`

### section_asset_briefs[]

- `section_id`
- `goal`
- `core_visual_message`
- `primary_asset_type`
- `secondary_asset_type`
- `must_show`
- `avoid_visual_noise`
- `prefer_diagram_over_asset_when`
- `prefer_video_over_still_when`
- `operator_note`

## Workflow Insertion

| step | actor | owner artifact | note |
|---|---|---|---|
| S-6 pre-asset-selection | tool | text brief | transcript または cue memo を受ける |
| S-6 | user | asset notes / selected materials | brief を見ながら素材候補を集める |
| S-6 | user | YMM4 project | 実際の配置と演出判断を行う |

## Acceptance

| ID | 条件 |
|---|---|
| AC-1 | 出力は text artifact のみで、素材取得や検索実行をしない |
| AC-2 | B-15 cue memo との差分が説明できる |
| AC-3 | section ごとに「何を見せるか」の迷いが減る |
| AC-4 | 図 / 動画 / 静止画の向き不向きが素材選定前に判断しやすくなる |
| AC-5 | D-02 や検索自動化へ滑らない |

## Risks

| risk | note |
|---|---|
| B-15 と重複する | 単なる背景候補の言い換えに見えると価値が薄い |
| 抽象論になる | 何を見せるべきかが具体化しなければ意味がない |
| search query brief の方が先かもしれない | 実際の pain が検索初動に偏ると順番が逆転する |

## Recommendation

1. `B-17` を `proposed` として FEATURE_REGISTRY に登録する
2. 最初は text-only brief に限定し、検索実行や取得機能へ広げない
3. B-15 / B-16 と混ぜず、独立した narrow candidate として proof 条件を持たせる
4. 実装判断は approval 後に行う

## Minimal Ask

次に必要な判断は 1 点でよい。

- `B-17 Asset Brief Packet` を次の `approved` 候補として進めるか
