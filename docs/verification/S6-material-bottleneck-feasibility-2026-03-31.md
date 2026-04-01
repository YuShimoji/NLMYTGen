# S-6 Material Bottleneck Feasibility

## Scope

- date: 2026-03-31
- purpose: B-15 Phase 1 が「方針メモ化」を短縮した後、S-6 に残る bottleneck を repo 境界ごとに分解する
- mode: feasibility only
- owner: `assistant`

## What B-15 Solved

- cue memo により、section 分け・背景の方向性・演出トーンの初期判断は大きく短縮できた
- 初回観測では、S-6 の方針メモ化は 30〜60 分想定から 5 分まで短縮した
- rerun では `primary_background` / `supporting_visual` / `sound_cue_optional` へ圧縮でき、response density も改善した

## What Still Hurts In S-6

| area | pain summary | why B-15 does not fully solve it |
|---|---|---|
| 素材選定 | cue は出ても、実際に何を採用するかで時間がかかる | cue memo は判断軸を出すが、候補の質と入手性までは埋めない |
| 図作成 | どんな図を作るか、何を書くかの設計に時間がかかる | cue memo はテーマを示すが、図の文言や構成までは粗い |
| フリー素材探索 | いらすとや等で欲しい絵柄・構図を探すのが遅い | cue memo は検索語や妥当性基準を持っていない |
| 動画素材の尺つなぎ | 20 秒級の動画を複数つないで持たせるのが重い | cue memo は尺配分や差し替え候補の整理まではしていない |

## Boundary Breakdown

| subtask | repo で支援しやすい部分 | repo で支援しにくい部分 | boundary fit |
|---|---|---|---|
| 素材選定 | section ごとの必須モチーフ、避けたい表現、主背景 / 補助素材の優先順位を text で出す | 実素材そのものの審美判断、最終採用判断 | high |
| 図作成 | 図の目的、入れるラベル、比較軸、避ける誤読を text brief として出す | 図版そのものの作成、レイアウト、視覚バランス | high |
| フリー素材探索 | 検索クエリ候補、検索時の除外語、採用チェック観点を text で出す | サイト横断取得、自動ダウンロード、権利確認の最終責任 | medium |
| 動画素材の尺つなぎ | 区間ごとの尺感、差し替えタイミング、静止画で埋めてもよい区間の印を出す | 実際の動画編集、視覚テンポ調整、レンダリング判断 | medium |

## Candidate Shapes

| candidate shape | value path | risk | feasibility now |
|---|---|---|---|
| section asset brief packet | 各 section で「何を見せるか」「何を優先するか」をさらに具体化できる | cue memo と重複しやすい。粒度を誤ると冗長 | high |
| diagram brief scaffold | 図作成の着手コストを下げやすい | 汎化しすぎると役に立たない | medium-high |
| asset search query packet | フリー素材探索の初動を速くできる | 検索先・権利・品質差の扱いが難しい | medium |
| automated asset acquisition | 実素材探索を直接短縮できる可能性はある | D-02 quarantine と権利 / 取得元 / 受け取り境界が未整理 | low |

## Recommended Direction

1. 次に proposal 化を検討するなら、`automated acquisition` ではなく `text-only asset brief` 系に寄せる
2. 最初の焦点は「素材そのものを取る」ことではなく、「素材選定・図作成の前に必要な判断材料を詰める」ことに置く
3. D-02 は引き続き quarantine のまま扱い、通常候補に戻さない
4. GUI や SDK 導入より先に、text artifact だけでどこまで S-6 の残時間を削れるかを見る

## Suggested Narrow Problem Statement

- cue memo は「各 section の方向性」は十分に短縮できた
- 次の未解決 pain は、「その方向性を実素材・図・尺配分へ落とす前段メモ」がまだ重いこと
- したがって、次に考えるなら「section ごとの asset / diagram brief を text で出す narrow feature」が最も自然

## Do Not Do Yet

- D-02 の quarantine を崩して取得自動化へ進まない
- YMM4 / `.ymmp` / 動画編集へ責務を広げない
- B-15 Phase 2 constrained rewrite と同時に走らせない
- SDK 導入や provider 内蔵を前提にしない

## Minimal Ask Before New Feature Proposal

次に必要なのは実装ではなく、1 点の設計判断である。

- 新規候補を立てる場合、対象を `asset / diagram brief` のような text-only 補助に限定してよいか
