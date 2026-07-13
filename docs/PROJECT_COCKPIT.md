# NLMYTGen Project Cockpit

Project-State-ID: generic-visual-static-layout-probe-ready-v1
State-Revision: 2026-07-14.3
Updated: 2026-07-14 JST
Product-State: generic-visual-static-layout-yymm4-probe-ready
Product-Gate: manual-generic-static-layout-observation
Recommended-Next: run-generic-static-layout-yymm4-probe
External-State: public-repo-feature-branch

このページはpublic repositoryで現在地を読むためのtracked summaryです。短期capsuleは
[runtime-state.md](runtime-state.md)、履歴は[project-context.md](project-context.md)、
task経路は[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。

## いまの一文

78 relevant paths / 38 capabilitiesのaccepted envelopeを変更せず、リンク字幕safe areaを
主対象に、静止ImageItem 1件と短いTextItem 1件だけを置くtopic-neutral H0 probeと
Japanese-first Operator Batchを準備しました。次のgateはuser-operated目視3点であり、
runtime acceptance、C3、render、Route A、productionの承認ではありません。

## 判断に使える現在地

| 対象 | 現在状態 | 残る境界 |
| --- | --- | --- |
| path inventory | 78 classified / unclassified 0 | pipeline表記も78へseal済み |
| capability classes | proven 15 / conditional 14 / unsupported 5 / unknown 4 | record変更なし |
| evidence ladder | C0-C5 = 5/3/14/14/2/0 | H0準備からC3へ昇格しない |
| carrier | neutral tracked sample / source hash不変 / VoiceItem 1 | source visual/GUI stateは非継承 |
| local project | Voice 1 + Image 1 + Text 1 / 109 frames / parse pass | actual visibilityは未観測 |
| layout | upper-left Image / upper-right Text / bottom subtitle reserve | crop/anchor/wrap/readabilityはH1 |
| Operator Batch | 3 actions / 3 questions / return最大3 / safe modes launch 0 | normal modeはuserだけが実行 |
| validation | exact non-overlapping commands and counts tracked | full pytest・GUI・mediaなし |
| minimum stack | C3 narration/timing/no-transition + optional C2 image/text | subtitle gateはmanual observation待ち |

Primary probe surface:
`samples/visual_composition_lab/runtime_probe/README_STATIC_LAYOUT_PROBE.md`

Capability authority:
`docs/visual_system/README_GENERIC_VISUAL_CAPABILITIES.md`

## 次の入口

repo rootからtracked README記載のbatch commandを1回実行し、字幕non-overlap、Image
crop/anchor、Text wrap/anchorの3点だけを確認します。projectはsave/renderせず閉じ、
terminalで3回答をcollectionします。

## 公開・実行境界

WorkerはComputer UseもYMM4も実行していません。ignored project/PNGとsafe-mode fixture
evidenceだけがlocalにあります。No screenshot, render/media, external asset, topic branch,
capability regrade, C3/C4/C5, rights/publication, Route A implementation or master integration.
