# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-notebooklm-source-set-frozen-v1
State-Revision: 2026-07-13.3
Updated: 2026-07-13 JST
Product-State: new-banknote-notebooklm-generation-source-set-frozen
Product-Gate: authoritative-source-resolution-and-claim-verification
Recommended-Next: resolve-official-source-urls-and-map-claims
External-State: public-repo-feature-branch

このページはpublic repositoryで現在地を読むための追跡済みMarkdownです。
内部capsuleは[runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。

## いまの一文

外部提供された11件のtitleをS01-S11として凍結し、生成時候補10件と生成後派生1件を
分離しました。既存claim 182件はtitle-level source familyへ全件整列済みですが、
source content未確認のためverified claimは0のままです。

## Source-set freeze結果

| 対象 | 現在状態 | 判断境界 |
| --- | --- | --- |
| title snapshot | 11/11 exact title、stable ID、deterministic fingerprint | URL・stable identifier・source contentは未解決 |
| chronology | generation-time 10、post-generation derived 1 | S07はstyle/dialogue provenanceのみ、factual authorityなし |
| authority | official候補はS04/S05/S10/S11 | title-level provisionalで、content verificationではない |
| non-independent | S03はsynthesisまたはuser note候補 | 独立した事実根拠にしない |
| claims | fingerprint照合182/182、5 lexical topic familyへ整列 | 本文はtrackedせず、verified claimは0、quantitativeはexact location必須 |
| privacy | raw/full textはignored、trackedはtitle・hash・分類・短いlabel | NotebookLM link / UUID / private pathなし |

Primary surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_SOURCE_RECONCILIATION.md`

## 次の入口

まずS04/S05/S10/S11のofficial URLまたはstable document identifier、publisher/date、
content identityを解決し、claimのexact page / field / date / unitへ接続します。その後、
S01/S02/S06/S08をcontextとして解決します。title一覧の再提示やAudio Overview再生成は不要です。

## 残存debt

- generation-time 10件のURL / stable identifierとsource contentは未解決。
- lexical topic labelはroutingであり、exact source supportや真偽を確定しない。
- S02/S08のpublisherとS03のorigin typeは未解決。
- timestamp / original audio durationはなく位置はline基準で、speaker identityとhuman editorial valueも未判定。
- YMM4 portability、full-suite drift、receipt test-path typoは別slice。

## 公開・実行境界

No NotebookLM access、external fetch、final script、Reimu/Marisa casting、CSV、YMM4、
Computer Use、dependency install、production、rights/legal、upload/publicationを維持しています。
