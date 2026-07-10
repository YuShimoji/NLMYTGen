# Turn-Based Development Map

> **Historical snapshot (2026-06-17):** このページの G-28 / common-foundation
> ターンは current plan ではありません。現在地と次の分岐は
> [PROJECT_COCKPIT.md](PROJECT_COCKPIT.md)、内部詳細は
> [runtime-state.md](runtime-state.md) を使ってください。この turn map は更新せず、
> 当時の判断経路として保持します。

## 2026-06-17 時点の見え方

既存 docs は日付、feature ID、slice、decision gate で進捗を保存しています。これは履歴証跡としては強い一方で、「次の 1-4 ターンで何をするか」を一目で見るには重いです。

当時は、ローカル閲覧で次の turn 区切りを使っていました。

| Turn | 入口 | 減らす摩擦 | 次に可能になること |
| --- | --- | --- | --- |
| T+0 | [runtime-state.md](runtime-state.md) の先頭、[Project Overview](project-overview.md)、[Visual Proof Index](visual-proof-index.md) | いま何を見るべきかを決める | G-28 prototype / object catalog / chat-first digest のどれをレビュー入口にするか決められる |
| T+1 | G-28 の HTML prototype と verification docs | 画面・object slot・弱点をチャットで読める状態にする | `accept_with_caveats / revise_once / reject / hold` の判断を返せる |
| T+2 | [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) の G-28 行と [REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md](REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md) | proposed / approved / diagnostic の境界を確認する | 次の修正が docs/prototype か、YMM4 transfer planning かを切り分けられる |
| T+3 | [TASK_DEVELOPMENT_CYCLE_SPEC.md](TASK_DEVELOPMENT_CYCLE_SPEC.md) と関連 verification | review surface / machine proof / human signal / close gate を揃える | 次の artifact が proof、readback、review packet、または hold record のどれかを決められる |

## 2026-06-17 のレーン別ターン読み

| レーン | T+0 で見る場所 | T+1 の判断 | T+2 以降の注意 |
| --- | --- | --- | --- |
| G-28 reference-driven screen carrier | `samples/_probe/g28/reference_layout_prototypes/index.html` と [Visual Proof Index](visual-proof-index.md) | prototype をレビューできるか、object catalog を先に見るか | production / render / YMM4 transfer は別 gate。受け入れ前に飛ばない。 |
| G-27 retained evidence | [G27_REVIEW_CONSOLE_SPEC.md](G27_REVIEW_CONSOLE_SPEC.md) と `samples/_probe/g24/` | 診断証跡として読むか、再利用 lesson として読むか | active production blocker として引き戻さない。G-28 への学びとして扱う。 |
| Common foundation / runner | [AGENT_ORCHESTRATION.md](AGENT_ORCHESTRATION.md) と runner verification docs | preview-only か real-runner かを混同しない | real runner は別途明示承認が必要。 |
| Baseball / sports_news | [BASEBALL_NEWS_PIPELINE_SPEC.md](BASEBALL_NEWS_PIPELINE_SPEC.md) と `lanes/sports_news/` | 本流ではなく sidequest として起動するか | 最初の review surface は screen plan。PNG/export を先に最終 proof にしない。 |

## 当時この turn map に残っていた未解決事項

| 未解決 | 今の扱い | 次に整えるなら |
| --- | --- | --- |
| 正本 runtime 自体が turn ベースではなかった | このページだけが当時の turn 見取り図だった | 現在は `PROJECT_COCKPIT.md` の decision paths を使う |
| スクリーンショットの採否が一箇所に閉じていない | [Visual Proof Index](visual-proof-index.md) で入口を集約 | proof ごとの `accepted / diagnostic / superseded` を別表化する |
| feature status と visual proof の対応が完全には結線されていない | FEATURE_REGISTRY と proof docs を併読 | feature ID ごとの proof index を生成する |
