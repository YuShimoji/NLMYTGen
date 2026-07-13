# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-source-backed-script-editorially-refined-v1
State-Revision: 2026-07-13.5
Updated: 2026-07-13 JST
Product-State: new-banknote-authoritative-script-human-review-ready
Product-Gate: human-script-review-and-yymm4-batch-decision
Recommended-Next: review-refined-nine-cue-script
External-State: public-repo-feature-branch

このページは public repository で現在地を読むための追跡済み Markdown です。
短期 capsule は [runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task 経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipeline は
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd) にあります。

## いまの一文

公式資料で採用 claim を絞り込んだ9 cue から、未説明のシリーズ記号、cue 8の
過密、曖昧な確認方法、語尾の反復を取り除きました。同じ本文順を保持する
canonical / YMM4-character-derived CSV も同期済みです。次の gate は人による
script 判断であり、YMM4 実行や production 承認ではありません。

## レビュー判断に使える現在地

| 対象 | 現在状態 | 判断に残る境界 |
| --- | --- | --- |
| official sources | 13 captures。S10/S11 は exact title、S04 は現行 exact document | S04 の generation-time byte version は不明。S05 の exact 572KB document は未解決で、別登録の official equivalent を使用 |
| claims | 182/182 adjudicated、`verified_primary` 19 | unsupported policy-intent、cashless-causation、位置を特定できない quantitative claim は canonical script に不採用 |
| script | 9 cues、scene 2/4/3、canonical speaker 3/6、20意味単位・21 claim edge、traceability 9/9 | human editorial acceptance は未実施。spoken text の unsupported claim は0 |
| editorial revision | cue 1→2を質問/回答化、cue 8を3事実化、cue 9をルーペへ具体化 | cue 8から外した数字`1`のclaimはverifiedのまま非採用traceへ保持 |
| CSV | canonical / derived の2列・9行 pair、本文と順序は一致 | YMM4 import・render は未実施 |
| privacy | title、receipt、hash、短い support location のみ tracked | raw transcript、source body、NotebookLM link / UUID、private path は tracked されない |

Primary surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_CANONICAL_SCRIPT_REVIEW.md`

## 次の入口

primary surface と `operator_review_sheet.md` を使い、改訂後の公式情報の分かりやすさ、
cashless-policy の誤解が残らないこと、Reimu / Marisa の自然さ、2/4/3 の流れ、
用語の正確さを確認します。承認された場合だけ、bounded YMM4 operator batch を
次の slice として選べます。

## 公開・実行境界

No NotebookLM access, Audio Overview regeneration, YMM4 launch, Computer Use,
render, human editorial acceptance, production, rights approval, upload,
publication, or master integration occurred in this slice.
