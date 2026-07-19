# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-reference-grounded-visual-proof-human-review-ready-v1
State-Revision: 2026-07-20.1
Updated: 2026-07-20 JST
Product-State: new-banknote-existing-content-researched-visual-grammar-implemented
Product-Gate: human-reference-grounded-visual-review
Recommended-Next: review-reference-grounded-visual-proof-and-lineage
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

16件の公開existing contentを先に調査し、14件の実視覚面から横断文法を抽出しました。
旧Route AをAI-originalな探索履歴へ降格し、approved contentを変えずに、外部asset 0の
reference-grounded proofを再設計しました。次はfinal宣言ではなくhuman reviewです。

## 判断に使える現在地

| 対象 | 現在状態 | 次のgateで確認すること |
| --- | --- | --- |
| Research | 16件登録、14件usable、official/journalism/Yukkuriが4/5/5 | corpusの十分性と偏りをhuman判断 |
| Route decision | documentary object-focus consensusが92点、次点差6 | final acceptanceはfalseのまま |
| Approval/content | 8 hashes、9 cues、2/4/3、3/6、CSV、15/20/21がsource baseとexact | visual feedbackでscriptをsilent editしない |
| Viewer frames | S1、S2 four techniques、S3の六つをoriginal neutral 1920×1080 SVG化 | flow、hierarchy、模式図riskをhuman判断 |
| Lineage | 12/12 decision、単一reference最大share 0.3333 | shared grammarとneutral glueをhuman判断 |
| Cue coverage | cue_001–cue_009をapproved subtitle付きcontact sheetで9/9表示 | omissionとscene/cue-specific revisionを確認 |
| Rights boundary | capture/thumbnailはignored localのみ、tracked proofはsource image/logo/creator art 0 | adaptationか模倣かhuman判断 |
| Motion | start/emphasis/settled、loop false、principal motion最大1 | restraintとcue主旨への干渉をhuman判断 |
| Acceptance | final acceptance、Shot/Motion、Asset/Rights、YMM4、renderはfalse/untested | proof acceptance後も別gate |

Primary review surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_grounded_visual_design/reference_grounded_visual_proof.html`

## 次の入口

同HTMLのviewer面、`#reference-lineage`、5問のreview sheetを見て、`accept`または
source/decision/scene/cue-specific revisionを返します。human accept前にShot/Motion、
Asset/Proxy/Rights、YMM4へ進みません。

## 公開・実行境界

このsliceではapproved content、旧Route A、YMM4 evidence、Operator Batch、ignored
research evidence、source branch、masterを変更していません。YMM4、video render、
production/publication、rights approval、PR、master integration、full suiteは実行していません。
