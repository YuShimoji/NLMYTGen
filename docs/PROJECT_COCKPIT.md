# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-route-a-dual-surface-visual-proof-human-review-ready-v1
State-Revision: 2026-07-19.5
Updated: 2026-07-19 JST
Product-State: new-banknote-route-a-viewer-and-annotation-proof-ready
Product-Gate: human-route-a-visual-proof-review
Recommended-Next: review-clean-route-a-viewer-frames
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

Route Aをconcrete proof生成の方向として維持し、approved contentを変えずに、六つのclean
viewer frameと六つのannotation frameを分離しました。9 cue contact sheetの完全ラベル、
semantic wrapping、non-looping motion storyboardも揃い、次はfinal宣言ではなくhuman reviewです。

## 判断に使える現在地

| 対象 | 現在状態 | 次のgateで確認すること |
| --- | --- | --- |
| Route decision | Route A selected for concrete proof only | final acceptanceとimplementationはfalseのまま |
| Approval/content | 8 hashes、9 cues、2/4/3、3/6、CSV、15/20/21がsource baseとexact | visual feedbackでscriptをsilent editしない |
| Viewer frames | S1、S2 four techniques、S3の六つをclean 1920×1080 SVG化 | flow、hierarchy、abstract geometryをhuman判断 |
| Annotation frames | 同じ六画面にcue/motion/source/safe-area evidenceを保持 | overlayは動画graphicではなく監査面として参照 |
| Cue coverage | cue_001–cue_009をapproved subtitle付きcontact sheetで9/9表示 | omissionとscene/cue-specific revisionを確認 |
| Subtitle | semantic segment連結がapproved textとexact、orphan/既知語分割なし | 1920×1080での実読性をhuman判断 |
| Diagram | 全full-frameに模式・非縮尺・非配置 disclaimer | real-note/official-procedureに見えないかhuman判断 |
| Motion | start/emphasis/settled、loop false、principal motion最大1 | restraintとcue主旨への干渉をhuman判断 |
| Assets/rights | original abstract SVG only、external resource 0 | production asset/rightsはH2で別契約 |

Primary review surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/route_a_visual_proof/route_a_visual_proof.html`

## 次の入口

同HTMLの既定viewer面とreview sheetを見て、四問に対する`accept`またはscene/cue-specific revisionを返します。
A/B/Cは選び直しません。human accept前にShot/Motion、Asset/Proxy/Rights、YMM4へ進みません。

## 公開・実行境界

このsliceではapproved content、original proposal、YMM4 evidence、Operator Batch、ignored
evidence、source branch、masterを変更していません。YMM4、render、production/publication、
rights approval、PR、master integration、full suiteは実行していません。
