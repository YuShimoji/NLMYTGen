# NLMYTGen Project Cockpit

Project-State-ID: generic-visual-static-layout-observation-passed-v1
State-Revision: 2026-07-15.1
Updated: 2026-07-15 JST
Product-State: generic-static-layout-bounded-runtime-observation-passed
Product-Gate: new-banknote-visual-direction-selection
Recommended-Next: review-new-banknote-route-a-b-c-on-provenance-branch
External-State: public-repo-feature-branch

このページはpublic repositoryで現在地を読むためのtracked summaryです。短期capsuleは
[runtime-state.md](runtime-state.md)、履歴は[project-context.md](project-context.md)、
task経路は[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。

## いまの一文

80 relevant paths / 38 capabilitiesのenvelopeに、exact same-machine static compositeの
operator-observed passをsanitized evidenceとして追加しました。字幕、Image、短いTextの
3点はpassですが、global capability rowとC0-C5 totalsは変更せず、1件のbounded C3
combinationだけを記録しています。次は別のauthoritative provenance branchで行う
new-banknote A/B/C人間選択です。

## 判断に使える現在地

| 対象 | 現在状態 | 残る境界 |
| --- | --- | --- |
| path inventory | 80 classified / unclassified 0 | 新規2 pathはsanitized receipt/readback |
| capability classes | proven 15 / conditional 14 / unsupported 5 / unknown 4 | row変更なし |
| evidence ladder | C0-C5 = 5/3/14/14/2/0 | exact combination C3をglobal totalsへ加算しない |
| local project | Voice 1 + Image 1 + Text 1 / 109 frames / identity match | same-machine exact artifactのみ |
| operator result | non-fixture / status pass / three pass answers | operator-observed、Worker GUI観測なし |
| subtitle | readable and non-overlapping = pass | 他profile/layoutは未確認 |
| Image | visible / crop / anchor = pass | 他サイズ・asset・anchorは未確認 |
| Text | visible / no clipping or unwanted wrap = pass | longer/style/font変更は未確認 |
| execution | no save / no screenshot evidence / no render | motion/effect/C4/C5なし |
| next gate | new-banknote A/B/C human selection | generic branchの旧boardを権威にしない |

Primary result surface:
`samples/visual_composition_lab/runtime_probe/README_STATIC_LAYOUT_PROBE_RESULT.md`

Capability authority:
`docs/visual_system/README_GENERIC_VISUAL_CAPABILITIES.md`

## 次の入口

このgeneric branchでYMM4 probeを再実行しません。authoritative new-banknote provenance
branchを別レーンとしてlive re-anchorし、provenance surfaceと最新visual boardから
A/B/C、S1/S2/S3 flow、misleading-diagram risk、motion restraintを人間が判断します。

## 公開・実行境界

Worker Computer Use 0、Worker YMM4 launch 0。Ignored local evidenceはbyte不変・untracked。
No render/media、dependency install、route selection、selected-route project、branch
integration、master mutation、production、rights/publication/upload。Exact composite passは
別layoutやgeneric visual system全体のproofではありません。
