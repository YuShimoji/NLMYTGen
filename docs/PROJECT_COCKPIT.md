# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-reference-grounded-visual-proof-evidence-strengthened-human-review-ready-v1
State-Revision: 2026-07-20.2
Updated: 2026-07-20 JST
Product-State: new-banknote-reference-evidence-graded-clean-viewer-proof-ready
Product-Gate: human-reference-grounded-visual-review
Recommended-Next: review-evidence-strengthened-reference-grounded-proof
External-State: public-repo-feature-branch
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0
Tracked-Worktree: clean; unrelated untracked supervision artifact and intentional ignored evidence retained

このページはpublic repositoryで現在地を読む追跡済みMarkdownです。
短期capsuleは[runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。

## いまの一文

16件の公開existing contentを、page/frame・thumbnail・in-video frameへ証拠分類しました。
Y01–Y03は3 channelの時刻固定動画内frame、Y04–Y05はthumbnail限定です。選定方向を維持し、
clean viewerとannotationを分離しました。次はfinal宣言ではなくhuman reviewです。

## 判断に使える現在地

| 対象 | 現在状態 | 次のgateで確認すること |
| --- | --- | --- |
| Research | 16件登録、page/frame 9、thumbnail 5、動画内frame 3、Y04–Y05 thumbnail-only | 証拠精度とcorpusの十分性をhuman判断 |
| Route decision | internal heuristicでobject-focus consensusが89点、次点差6、選定維持 | 点数は品質/受容評価ではなくfinal acceptanceはfalse |
| Approval/content | 8 hashes、9 cues、2/4/3、3/6、CSV、15/20/21がsource baseとexact | visual feedbackでscriptをsilent editしない |
| Viewer frames | clean viewer 6枚は可視scene/cue/reference/evidence/review metadata 0 | flow、hierarchy、模式図riskをhuman判断 |
| Annotation / lineage | annotation 6枚と12/12 decision、単一reference最大share 0.3333 | evidence class、shared grammar、neutral glueをhuman判断 |
| Cue coverage | cue_001–cue_009をapproved subtitle付きcontact sheetで9/9表示 | omissionとscene/cue-specific revisionを確認 |
| Rights boundary | capture/thumbnailはignored localのみ、tracked proofはsource image/logo/creator art 0 | adaptationか模倣かhuman判断 |
| Motion | sequence観察0、P07はinferred ceiling、loop false、principal motion最大1 | 未観察を前提にproposalのrestraintをhuman判断 |
| Acceptance | final acceptance、Shot/Motion、Asset/Rights、YMM4、renderはfalse/untested | proof acceptance後も別gate |

Primary review surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_grounded_visual_design/reference_grounded_visual_proof.html`

## 次の入口

同HTMLのclean viewer面、`#annotation`、`#reference-lineage`、5問のreview sheetを見て、`accept`または
source/decision/scene/cue-specific revisionを返します。human accept前にShot/Motion、
Asset/Proxy/Rights、YMM4へ進みません。

## 公開・実行境界

このsliceではapproved content、旧Route A、YMM4 evidence、Operator Batch、ignored
research evidence、source branch、masterを変更していません。YMM4、video render、
production/publication、rights approval、PR、master integration、full suiteは実行していません。
