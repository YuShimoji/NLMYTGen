# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-content-lineage-sealed-yymm4-batch-ready-v1
State-Revision: 2026-07-17.1
Updated: 2026-07-17 JST
Product-State: new-banknote-human-approved-script-lineage-sealed-operator-batch-ready
Product-Gate: manual-yymm4-import-observation
Recommended-Next: run-one-new-banknote-yymm4-operator-batch
External-State: public-repo-feature-branch
Handoff-Commit: 5d46a7389334626eb713ea5f9681288ac9b25b63
Remote-Parity: 0/0
Tracked-Worktree: clean; intentional ignored evidence retained

このページは public repository で現在地を読むための追跡済み Markdown です。
短期 capsule は [runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task 経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipeline は
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd) にあります。

## いまの一文

人が option A で承認した新紙幣9-cue scriptを commitと8 file hashesで固定し、
提出 transcript から official evidence、supported rewrite、editorial convergence、
approval、YMM4 projectionまでをT00–T07の一つのlineage packageへ統合しました。
次はユーザー自身による一度だけのYMM4 import観測です。

## 判断に使える現在地

| 対象 | 現在状態 | 次の gate で確認すること |
| --- | --- | --- |
| Approval | `b05eb386…`、9 cues、2/4/3、Reimu/Marisa 3/6、8 hashesをreceiptで固定 | hash、text/order、speaker/scene、claim/evidence、CSV driftがあれば自動停止 |
| Submitted content | 326 lines→182 claims。raw claim fingerprintでfinal cueへの影響を追跡 | transcriptはoriginでありfactual authorityではない。token-level authorshipは不明 |
| Evidence | 19 verified-primaryのうち15 claimsを採用、20 units・21 edges、used sourcesはV02/V06/V07/V13 | unsupported policy/cashless/quantitative framingは不採用のまま |
| Editorial origin | factual paraphraseとWorker connective/voice/structureをcue単位で分離 | connective/voiceはsource quotationとして扱わない |
| Operator batch | 5 actions、return最大3、実行前/収集前の二重lock、collectorが9/3/6/text/order/timingを検証 | mapping/update/wrong characterで停止し、発音・clippingをcue番号で記録 |
| Privacy | raw/source/local bodiesとprivate pathをtracked artifactへ含めない | ignored salvage evidenceをbatch recoveryで移動・削除しない |
| Runtime | headless preflight passed、YMM4 process増加0、Computer Use 0 | actual import、pronunciation/rhythm、renderは未実施 |

Primary surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_CONTENT_LINEAGE.md`

## 次の入口

repository rootから次を一度だけ実行します。

`powershell -NoProfile -ExecutionPolicy Bypass -File ".\production_pilots\yukkuri_newsroom_content_spine_002\external_editorial_input\new_banknote_security_notebooklm_001\yymm4_operator_batch\run_new_banknote_yymm4_batch.ps1"`

YMM4に未保存の無関係な作業がないことを確認し、新規空projectへ表示済みCSVを
importしてexact local pathへ保存します。9 cuesを一度previewし、発音または明らかな
clippingをcue番号でメモして、renderせず閉じた後にterminalで`COLLECT`とメモを
入力します。

## 公開・実行境界

このsliceではapproved contentを変更せず、NotebookLM、web fetch、Computer Use、
YMM4 launch/inspection、render、production、public/rights action、master integrationを
行っていません。Human approvalはbounded import observationだけを許可し、production
やpublicationの承認ではありません。
