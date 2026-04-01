# Asset Brief Proposal Draft (2026-03-31)

## Why This Exists

B-15 は S-6 の方針メモ化を短縮し、B-16 は図作成前の planning を短縮した。
それでも残っている大きい pain は、各 section で「何を見せるべきか」を決める素材選定前の迷いである。

ここで欲しいのは素材の自動取得ではなく、人間が素材選定に入る前に参照する text-only の asset brief である。

## Problem Statement

- B-15 cue memo は方向性の整理には効くが、素材選定直前の判断材料としてはまだ粗い
- search query brief を先に立てると、「何を見せるか」が曖昧なまま検索語だけが増えるリスクがある
- したがって次は、section ごとに「主背景 / 補助素材 / 図へ逃がすべきか / 動画が必要か」を決めやすくする narrow support が自然

## Value Path

| 観点 | 狙い |
|---|---|
| どこに効くか | S-6 の素材選定前メモ |
| 何を減らすか | 何を見せるべきか、どの素材種別を優先すべきかの迷い |
| 手作業は何が残るか | 実素材探索、採否判断、YMM4 への配置、演出判断 |
| なぜ今やるか | B-16 rerun が positive なら、次の bottleneck は図以外の素材選定前整理に寄るため |

## Difference From B-15

| item | B-15 cue memo | asset brief draft |
|---|---|---|
| 主目的 | section の演出方向を決めやすくする | 素材選定前に「何を見せるか」を具体化する |
| 出力中心 | primary background / supporting visual / emotion / transition | 必須モチーフ / 素材種別優先順位 / 図や動画に逃がすべきか / 避けたい誤読 |
| 使う場所 | S-6 全体の初動 | 素材探しに入る直前 |
| 残る作業 | 素材選定、配置、採否判断 | 同左 |

## Recommended Scope

- transcript または cue memo を入力に取り、section ごとの素材選定前メモを返す
- 出力は text artifact のみ
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

## Boundaries

### 許可

- 素材種別の優先順位
- 何が必須モチーフか
- どの区間は図へ逃がすべきか
- どの区間は動画でなく静止画でもよいか

### 禁止

- 素材ダウンロード
- 実検索
- 権利確認の自動化
- YMM4 配置指定

## Acceptance

| ID | 条件 |
|---|---|
| AC-1 | 出力は text artifact のみ |
| AC-2 | B-15 cue memo との差分が説明できる |
| AC-3 | section ごとに「何を見せるか」の迷いが減る |
| AC-4 | 図 / 動画 / 静止画の向き不向きが、素材選定前に判断しやすくなる |
| AC-5 | D-02 や検索自動化へ滑らない |

## Risks

| risk | note |
|---|---|
| B-15 と重複する | 背景候補の言い換えに見えると価値が薄い |
| 抽象論になる | 何を見せるべきかが具体化しなければ意味がない |
| search query brief のほうが直接的な場合がある | 素材探索が主 pain なら順番が逆転する |

## Recommendation

次の `proposed` 候補としては、現時点では `search query brief` より `asset brief` の方が自然。

理由は次の 3 点。

1. 「何を探すか」より前に「何を見せるか」を決める工程が重い
2. text-only boundary を保ちやすい
3. B-16 で図作成を切り出した後の残 bottleneck に直接つながる
