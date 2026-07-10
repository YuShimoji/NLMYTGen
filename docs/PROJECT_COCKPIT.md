# NLMYTGen Project Cockpit

Project-State-ID: supervisor-only-control-boundary-restored-v1
State-Revision: 2026-07-10.5
Updated: 2026-07-10 JST
Product-State: episode-002-ymm4-observation-completed-with-adapter-gap
Product-Gate: evidence-backed-adapter-correction
Recommended-Next: correct-speaker-mapping-and-placeholder-lane-gap
External-State: public-repo-feature-branch

このページは、public repository で現在地を読むための追跡済み Markdown です。
内部 capsule は [runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、タスク経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipeline は
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd) にあります。これらは状態の保存・案内面であり、
開発セッションの Prompt や Worker 実行権限を定義しません。

別端末からはfeature branchをfast-forwardで取得した後、通常の3文書と
`project-context.md`最上部の「現在の別端末再開ハンドオフ」を読めば、
現在地・未実施事項・再開条件へ戻れます。

## いまの一文

Episode 002 の9行CSVはYMM4 `4.53.0.9`で実importされ、9 VoiceItems、順序、
字幕本文、timing orderを確認しました。結果はpartialで、話者の手動mappingと
ImageItem/TextItem placeholder lane欠落が次のadapter修正対象です。保存・render・
実素材置換は行っていません。

## 現在の状態

| 対象 | 現在地 | 次に進む条件 | まだ保証しないこと |
| --- | --- | --- | --- |
| Episode 002 観測 | 9/9 VoiceItemsを順序どおり実観測。字幕は手動話者mapping後に一致。実durationは2790 frames / 46.50秒 | speaker aliasとplaceholder laneを証拠範囲で補正 | render / production `.ymmp` / public-ready |
| 実素材置換 | intake 契約はあるが検証済み候補はゼロ | source / transcript / provenance / stable identity / cue alignment を受領 | sample input を real input と扱うこと |
| feature branch | control-boundary correctionを実装 | default branch との差分を再計算し、integration を判断 | default branch に統合済みという主張 |
| 公開面 | public repo のこの Markdown で現在地を参照可能 | Pages が必要な場合だけ別途 publication を選ぶ | Pages / Wiki の自動公開 |

## 今回の境界修正

| 除去したもの | 残したもの | 意味 |
| --- | --- | --- |
| repo 内 Supervisor Prompt 正本と汎用 Worker authority | Web supervisor から渡す self-contained prompt | セッション指示と repository state を混同しない |
| 応答品質・YMM4・scene bible・asset matrix の Stop lint | 明示されていない cross-repo 参照だけを止める guardrail | 内容や報告形式が隠れた hard gate にならない |
| state checker の自動 Stop hook / retry logic | 明示実行できる state alignment CLI | 状態検査を保ちつつ応答停止ループを作らない |
| repo 内の汎用監修 workflow | product artifact 用の review cycle / Direction Check | 見た目の方向確認を Worker governance から分離する |

## 次に選べる入口

| 入口 | 解く bottleneck | 選ぶと可能になること |
| --- | --- | --- |
| **Correct（推奨）** | 話者aliasが自動bindingされず、ImageItem/TextItem placeholder laneがない | 二つの実測gapだけを修正し、bounded observationを再実行できる |
| **Advance** | sample fixture から先へ進めない | 検証済み実素材 receipt を作り、置換へ進める |
| **Integrate** | feature/default branch の関係が未判断 | 最新 diff を監査し、安全な統合方針を選べる |

Explore は将来の visible product review debt に降格し、Excise は現在の入口にしません。
default branch への integration と GitHub Pages の publication は別の選択です。
public repo の安定した Markdown URL を使うだけなら Pages は不要です。

推奨既定は **Correct** です。五点観測で確認されたspeaker mappingとplaceholder laneの
二点だけを対象にし、renderや実素材へscopeを広げません。

## 公開境界

このページには private URL、token、raw source、article body、権利未確認素材、
ローカル絶対パスを載せません。actual importはこのbounded diagnostic runだけで確認済みです。
render、production `.ymmp`、real-input replacement、rights approval、upload completion は
証拠が揃うまで未完了として扱います。
