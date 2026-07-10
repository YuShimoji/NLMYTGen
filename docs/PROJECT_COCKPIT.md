# NLMYTGen Project Cockpit

Project-State-ID: workflow-velocity-and-current-state-v1
State-Revision: 2026-07-10.1
Updated: 2026-07-10 JST
Product-State: episode-002-ymm4-observation-ready
Product-Gate: five-point-ymm4-import-observation
Recommended-Next: verify-ymm4-five-observations
External-State: tracked-branch-mirror-pages-unpublished

このページは branch push 後に GitHub 上で現在地を読むための追跡済みミラーです。内部の
詳細正本は `docs/runtime-state.md`、過去の判断履歴は
`docs/project-context.md` に置きます。別管理の Wiki 本文を手動更新する運用には
せず、同じ commit でこのページと runtime capsule を同期します。

## いまの一文

Episode 002 は「YMM4 に読み込んで五つの実観測を返せる準備」まで完了し、
実 import と実素材置換はまだです。開発運用は、監修AIが成果単位の一つの
Promptを渡し、開発AIが関連修正・限定検証・現在地同期・Git follow-throughまで
止まらず閉じる方式へ切り替わりました。

## 現在の状態

| 対象 | 現在地 | 次に進む条件 | 誤って主張しないこと |
| --- | --- | --- | --- |
| 開発ワークフロー | 一括スライス契約、risk-tier、Direction Check、状態同期を導入 | 次の実タスクから運用し、摩擦を観測する | 文書化だけで製品機能が増えたとは扱わない |
| Episode 002 観測パッケージ | 日本語 preview、五点シート、readback、九 cue CSV が生成済み | 人間が YMM4 import 後の五点を返す | actual import / observed cue / render |
| 実素材置換 | intake 契約と drop-zone はあるが候補ゼロ | 検証済み source / transcript / rights note / identity / cue alignment | sample input を real input と扱うこと |
| 公開・配信 | 閉じている | rights、final creative judgement、upload authority | public-ready / upload complete |
| 外部現在地 | この Markdown は branch push 後に GitHub で閲覧可能 | stable URL が必要なら master promotion と Pages 方針を決める | Wiki / Pages が自動同期済みという主張 |

## 今回変わった判断の流れ

| 以前の摩擦 | 新しい既定 | 効果 |
| --- | --- | --- |
| 安全策があらゆる曖昧さで停止を発生 | reversible な repo-local 作業は続行し、hard stop は高影響境界だけ | 小さな確認待ちで実装が途切れない |
| 調査・実装・テスト・報告を別 Prompt に分割 | 監修AIは一つの Outcome Packet を渡す | 一つの成果物が閉じるまで開発AIが自律的に進める |
| 完成品を見てから方向修正 | visible work は低コスト2〜3案→代表面→横展開 | 大物完成後の微修正沼を減らす |
| runtime / cockpit / dashboard が別々に current を名乗る | runtime capsule とこの cockpit の shared state fields を照合 | 片面更新と古い packet ID を closeout 前に検出する |

## Creative Opportunity Radar（未承認・最大2件）

| 仮説 | 最小 preview | 利得 / コスト | 着手条件 |
| --- | --- | --- | --- |
| 次の GUI visible slice を i18n-ready visual system として設計し、機械 key と表示言語、layout density、色・書体 hierarchy、motion token を分離する | 代表 1 画面で「timeline-first / artifact-first / decision-first」の 3 方向を同じ content で比較 | 日本語修正や英語対応で layout を作り直す摩擦を減らす / 中 | 新しい GUI surface が product bottleneck になった時だけ Direction Check を起動 |
| Episode 002 の artifact chain を隣接 topic 用 episode seed に昇格し、source receipt と placeholder boundary を clone 可能にする | 実 content を増やさず、1件の clone manifest と gap report だけ作る | 次の content を既存工程へ接続しやすくする / 中 | 五点の YMM4 観測と verified real-input receipt が揃ってから value gate を再確認 |

どちらも current next action ではなく、silent implementation しない。各仮説が着手条件を
満たした時だけ、低コスト比較または value validation から始める。

## 次に選べる入口

| 入口 | 解く bottleneck | 選ぶと可能になること |
| --- | --- | --- |
| **Verify（製品の最短経路）** | YMM4 実観測がゼロ | import adapter の修正要否を証拠で判断できる |
| **Advance（実素材経路）** | sample fixture から先へ進めない | Episode 002 を実素材へ置換する receipt を作れる |
| **Explore（次の visible slice）** | layout / i18n / 色・書体・motion の方向を後決めしている | 2〜3案の低fi比較で、実装前に意図を合わせられる |
| **Publish（外部現在地）** | branch URL では安定した current URL にならない | master promotion と sanitized GitHub Pages の設計へ進める |

推奨既定は **Verify** です。観測結果が返るまで開発側で進める visible task が
選ばれた場合は、先に **Explore** を一度だけ行い、方向承認後は一括実装へ進みます。

## 主要な確認先

- 現在地の内部正本: [runtime-state.md](runtime-state.md)
- 監修AI→開発AIの反復契約: [TASK_DEVELOPMENT_CYCLE_SPEC.md](TASK_DEVELOPMENT_CYCLE_SPEC.md)
- 対話・停止・報告の失敗分類: [INTERACTION_NOTES.md](INTERACTION_NOTES.md)

YMM4 観測 preview と五点返却シートにはローカル実行 path が含まれるため、
公開向け cockpit から直接リンクしない。オペレーターは内部正本の
`Human or External Decision Points` から repo-relative artifact を開く。

## 公開境界

このページには private URL、token、raw source、article body、権利未確認素材、
ローカル絶対パスを載せません。GitHub Pages / Wiki への自動公開は未実装であり、
repository visibility と公開許可を確認してから別スライスで扱います。
