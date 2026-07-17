# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-content-lineage-sealed-existing-yymm4-evidence-reconciliation-ready-v1
State-Revision: 2026-07-17.2
Updated: 2026-07-17 JST
Product-State: new-banknote-lineage-sealed-existing-import-evidence-readback-ready
Product-Gate: current-lineage-compatible-yymm4-evidence-reconciliation
Recommended-Next: build-non-overwriting-existing-yymm4-evidence-revalidation
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
同端末に既存YMM4 import成功証跡があるため、次は再実行ではなくcurrent lineageとの
非破壊再照合です。

## 判断に使える現在地

| 対象 | 現在状態 | 次の gate で確認すること |
| --- | --- | --- |
| Approval | `b05eb386…`、9 cues、2/4/3、Reimu/Marisa 3/6、8 hashesをreceiptで固定 | hash、text/order、speaker/scene、claim/evidence、CSV driftがあれば自動停止 |
| Submitted content | 326 lines→182 claims。raw claim fingerprintでfinal cueへの影響を追跡 | transcriptはoriginでありfactual authorityではない。token-level authorshipは不明 |
| Evidence | 19 verified-primaryのうち15 claimsを採用、20 units・21 edges、used sourcesはV02/V06/V07/V13 | unsupported policy/cashless/quantitative framingは不採用のまま |
| Editorial origin | factual paraphraseとWorker connective/voice/structureをcue単位で分離 | connective/voiceはsource quotationとして扱わない |
| Operator evidence | ignored project/result/stateあり。旧resultは9/3/6、exact text/order、4415 frames、73.583333秒 | 再実行せずcurrent lineage lockで非破壊再照合。発音/clippingはunknown維持 |
| Privacy | raw/source/local bodiesとprivate pathをtracked artifactへ含めない | ignored salvage evidenceをbatch recoveryで移動・削除しない |
| Runtime | focused 25 + regression 17、validator/headless preflight passed | tracked successor receipt、branch integration audit、pronunciation/rhythm、renderは未完了 |

Primary surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_CONTENT_LINEAGE.md`

## 次の入口

既存ignored project/result/batch stateを削除・移動・上書きせず、current approvalと
lineage lockを検査して既存project/resultをparseするread-only revalidation pathを作ります。
sanitized successor receiptが通った後にだけ、分岐したvisual/provenance branchとの
integration auditへ進みます。監修用の詳細は
[`REMOTE_SYNC_DEVELOPMENT_READINESS_SUPERVISOR_ROADMAP_2026-07-17.md`](verification/REMOTE_SYNC_DEVELOPMENT_READINESS_SUPERVISOR_ROADMAP_2026-07-17.md)
を参照してください。

## 公開・実行境界

このsliceではapproved contentを変更せず、NotebookLM、web fetch、Computer Use、
YMM4 launch/inspection、render、production、public/rights action、master integrationを
行っていません。Human approvalはbounded import observationだけを許可し、production
やpublicationの承認ではありません。
