# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-notebooklm-transcript-salvaged-v1
State-Revision: 2026-07-13.2
Updated: 2026-07-13 JST
Product-State: new-banknote-notebooklm-raw-transcript-salvaged
Product-Gate: notebooklm-source-set-reconciliation
Recommended-Next: provide-notebooklm-source-list-export
External-State: public-repo-feature-branch

このページはpublic repositoryで現在地を読むための追跡済みMarkdownです。
内部capsuleは[runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。

## いまの一文

NotebookLM Audio Overviewのraw transcriptを改変せず、326行すべてをhash-boundで
対応付け、重複・style contamination・ASR候補・匿名turn・claim riskを分離しました。
次のgateはsource-set reconciliationです。

## Salvage結果

| 対象 | 現在状態 | 判断境界 |
| --- | --- | --- |
| raw identity | SHA-256、32,089 bytes、326 logical lines一致 | raw / manifestはignored・untracked |
| duplication | exact lineとnear-spanを別cluster化 | raw evidenceは削除しない |
| style / ASR | 10 style class、reversible ASR候補 | clean transcriptとは主張しない |
| turns | `voice_1` / `voice_2` / `ambiguous`のみ | Reimu/Marisa未割当 |
| claims | technical・quantitative・historical・policy・causal等を分離 | verified claimは0 |
| full text | line map・derivatives・turn textは`local_outputs/` | tracked packageはfingerprintと短いlabelのみ |

Primary surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_TRANSCRIPT_SALVAGE.md`

## 次の入口

NotebookLM source titles、利用可能なsource URLまたはstable identifier、意図的に除外した
sourceがあればその一覧を返します。Audio Overview再生成、speaker手分け、timestamp復元は不要です。

## 残存debt

- exact source setがないため、claim verificationとcanonical script化はblocked。
- timestamp / original audio durationはなく、位置はline基準。
- speaker identityとhuman editorial valueは未判定。
- YMM4 portability、full-suite drift、receipt test-path typoは別slice。

## 公開・実行境界

No NotebookLM access、external fetch、final script、Reimu/Marisa casting、CSV、YMM4、
Computer Use、dependency install、production、rights/legal、upload/publicationを維持しています。
