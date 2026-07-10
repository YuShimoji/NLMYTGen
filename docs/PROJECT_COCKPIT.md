# NLMYTGen Project Cockpit

Project-State-ID: episode-002-ymm4-speaker-alias-ready-for-reobservation-v1
State-Revision: 2026-07-11.1
Updated: 2026-07-11 JST
Product-State: episode-002-ymm4-speaker-alias-ready-for-reobservation
Product-Gate: bounded-yymm4-alias-reobservation
Recommended-Next: reobserve-derived-yymm4-csv
External-State: public-repo-feature-branch

このページはpublic repositoryで現在地を読むための追跡済みMarkdownです。
内部capsuleは[runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。これらは状態の保存・案内面であり、
開発セッションのPromptやWorker実行権限を定義しません。

## いまの一文

Episode 002は、canonical speakerを保つ明示的YMM4 character profileと9行の
derived import CSV、CSV/diagnostic-project責務分離まで実装・検証済みです。
再観測時にYMM4が既存のunsaved `無題*` projectを復元したため、その状態を破棄せず
停止しました。現在のgateはderived CSVの一回限りのbounded re-observationです。

## 現在の状態

| 対象 | 現在地 | 次に進む条件 | まだ保証しないこと |
| --- | --- | --- | --- |
| speaker identity | canonical `れいむ` / `まりさ`を維持し、profileで`ゆっくり霊夢` / `ゆっくり魔理沙`へstrictに射影 | 未定義speakerを追加する場合はprofileを明示更新 | 全YMM4環境のuniversal default |
| derived CSV | 9行、text/order不変、speaker列だけ変換。canonical SHA不変 | cleanなYMM4 projectへ一度だけimport | automatic bindingのGUI pass |
| CSV contract | `VoiceItem + linked_subtitle`だけがCSV gate | mapping dialogなし・9/9 items・正しいcharacter・text/order・timing orderを観測 | ImageItem/独立TextItemをCSVが生成すること |
| diagnostic project | `not_authorized / not_attempted` | supervisorが別sliceとして明示認可 | `.ymmp`生成・patch・保存 |
| GUI再観測 | 既存unsaved `無題*`を保全して停止。derived import未実施 | userが既存projectをsave elsewhereまたはdiscardする判断 | existing unsaved stateの無断破棄 |
| 実素材置換 | intake契約はあるが検証済み候補ゼロ | source / transcript / provenance / stable identity / cue alignmentを受領 | sample inputをreal inputと扱うこと |

## 次に選べる入口

| 入口 | 解くbottleneck | 選ぶと可能になること |
| --- | --- | --- |
| **Reobserve（推奨）** | YMM4に復元された既存unsaved projectがclean importを阻む | 既存stateの扱いを決めた後、derived CSVのCSV gateだけを観測できる |
| **Advance** | sample fixtureから先へ進めない | 検証済み実素材receiptを作り、置換へ進める |
| **Integrate** | feature/default branchの関係が未判断 | 最新diffを監査し、安全な統合方針を選べる |

Reobserveの実行対象は
`production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/derived_yymm4_import.csv`
です。先に、現在開いているYMM4のunsaved `無題*` projectを保存するか破棄するかを
決める必要があります。成功してもdiagnostic `.ymmp`を自動開始しません。

## 証拠境界

- canonical CSV SHA-256:
  `6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C`
- derived CSV SHA-256:
  `5452DE96DC6EF012400A132BA5BAE80B8553C1B1CDD27860D36674C25AF391BC`
- immutable prior receipt SHA-256:
  `DC756D9C4EE9ABDFDDFB284B2B8EC70B227DDEB5E365C1BBB8EE8438D8C9A5B5`
- current GUI blocker: existing unsaved project preserved; no derived import,
  save, render, export, or project discard occurred.

## 公開境界

このページにはprivate URL、token、raw source、article body、権利未確認素材、
ローカルuser-home絶対pathを載せません。render、production `.ymmp`、real-input
replacement、rights approval、final thumbnail、upload、default-branch integrationは
対応する証拠が揃うまで未完了です。
