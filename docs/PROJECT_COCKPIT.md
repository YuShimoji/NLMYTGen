# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-yymm4-import-observed-visual-decision-ready-v1
State-Revision: 2026-07-14.1
Updated: 2026-07-14 JST
Product-State: new-banknote-yymm4-import-observed-visual-direction-review-ready
Product-Gate: human-visual-direction-selection
Recommended-Next: select-new-banknote-visual-direction
External-State: public-repo-feature-branch

このページはpublic repositoryで現在地を読むためのtracked summaryです。短期capsuleは
[runtime-state.md](runtime-state.md)、履歴は[project-context.md](project-context.md)、
task経路は[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。

## いまの一文

承認済み9 cueを変えずにreal YMM4 importの構造成功をheadless再検証し、sanitized
receiptと、Route Aを推奨するA/B/C visual decision packetを用意しました。次のgateは
human visual-direction selectionで、visual project、render、production、rightsの承認ではありません。

## レビュー判断に使える現在地

| 対象 | 現在状態 | 判断に残る境界 |
| --- | --- | --- |
| approved script / CSV | 9 cues、scene 2/4/3、3/6、unsupported 0、六hash不変 | wording/claim再判断は閉じたまま |
| import result | success、failed checks 0、operator mapping/error confirmation | GUI事実はobserved evidence |
| local project | 9 VoiceItems、3/6、exact text/order、missing/duplicate 0 | ignored・same-machine evidence |
| actual timing | 60 fps、4415 frames、73.583333 seconds | informational、production timingではない |
| visual routes | A Security Inspection Lab推奨、B Everyday Verification、C Design Evolution | Aは未選択、全route未実装 |
| scene spine | Route AにS1/S2/S3と9/9 cue、source/claim/timing/factual boundary | human flow/misleading/motion判断が必要 |
| assets / rights | original abstract schematicのみ、external asset 0 | rights clearedではない |
| HTML review | self-contained CSS、repo-relative links、4 questions | screenshot/render/GUI proofなし |

Primary review surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/visual_scene_decision/visual_direction_board.html`

## 次の入口

HTML boardを確認し、A / B / Cの選択、またはscene/cue ID付き修正を返します。同時に
S1/S2/S3の流れ、誤解を招く模式図、motionの抑制度だけを判断します。選択後の別sliceでのみ
diagnostic YMM4 visual projectを検討します。

## 公開・実行境界

No YMM4 launch, Computer Use, image generation, external fetch, asset download,
visual project, render, production, rights approval, upload, publication, or
master integration occurred in this slice.
