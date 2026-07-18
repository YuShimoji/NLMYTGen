# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-successor-selectively-integrated-visual-selection-ready-v1
State-Revision: 2026-07-19.3
Updated: 2026-07-19 JST
Product-State: new-banknote-lineage-yymm4-provenance-visual-proposals-unified
Product-Gate: human-visual-direction-selection
Recommended-Next: select-new-banknote-visual-direction-from-unified-surface
External-State: public-repo-feature-branch
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0
Tracked-Worktree: clean; intentional ignored evidence retained

このページはpublic repositoryで現在地を読む追跡済みMarkdownです。
短期capsuleは[runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。

## いまの一文

exact auditの27/2/8/14 partitionでnew-banknote successorを選択統合し、
primary approval・T00–T07・current YMM4 revalidationを正本のまま、candidate
D00–D10・historical observation・A/B/C proposalだけを一つのreview surfaceへ
接続しました。次はbranch reconciliationではなくhuman visual selectionです。

## 判断に使える現在地

| 対象 | 現在状態 | 次のgateで確認すること |
| --- | --- | --- |
| Approval | option A receipt、8 hashes、9 cues、2/4/3、3/6、CSV、15/20/21がprimary byte-exact | visual選択でscript/contentを変えない |
| Lineage / provenance | T00–T07がcurrent、D00–D10はsecondary deep audit | 来歴を見ながらscene/cueごとのvisual妥当性を判断 |
| YMM4 evidence | primary revalidationがcurrent、candidate observationはhistorical。9 VoiceItems、60 fps、4415 frames、73.583333秒で整合 | audio品質は別gateのまま維持 |
| Operator Batch | primary five-action familyがcurrent、candidate four-action familyはexcluded | visual選択では実行しない |
| Visual | A/B/C proposal integrated、Route A `recommended_not_selected`、selectionなし | A/B/Cまたはscene/cue-specific revisionを返す |
| Portability | same-machine local evidence不在は`not_reperformed_or_not_present` | tracked packageをportableにreviewできること |
| Privacy / rights | private path、local binary、raw/source bodyなし。rights未解決 | misleading-diagram riskとrights burdenをhuman判断 |

Primary integrated surface:
`docs/verification/NEW_BANKNOTE_SUCCESSOR_SELECTIVE_INTEGRATION.md`

Human review surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/visual_scene_decision/visual_direction_board.html`

## 次の入口

A/B/C choiceまたはscene/cue-specific revision、S1/S2/S3 flow、
diagram-misleading risk、motion restraintの4点をhuman reviewerが返します。
このdecision前にShot Layout、Motion Beat、asset work、diagnostic YMM4へ進みません。

## 公開・実行境界

このsliceではnormal merge/rebase/cherry-pick、approved content変更、YMM4、render/media、
production/publication、rights action、PR、master integrationを行っていません。
Route Aのrecommendationはselection、approval、implementationを意味しません。
