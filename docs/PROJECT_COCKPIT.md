# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-reference-layout-reconstructed-human-review-ready-v1
State-Revision: 2026-07-20.4
Updated: 2026-07-21 JST
Product-State: new-banknote-reference-traced-production-frame-proof-ready
Product-Gate: human-reference-layout-review
Recommended-Next: review-reference-reconstructed-production-frame-proof
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 after handoff push
Tracked-Worktree: clean after handoff commit; pre-existing untracked artifacts retained

このページはpublic repositoryで現在地だけを読む追跡済みMarkdownです。短期正本は
[runtime-state.md](runtime-state.md)、開発時の静音契約は
[DEVELOPMENT_AUDIO_SAFETY.md](DEVELOPMENT_AUDIO_SAFETY.md)、判断履歴は
[project-context.md](project-context.md)にあります。

## いまの一文

旧Lab proofと人間がAIテンプレ表現として却下したreference-grounded proofをbyte-exactな
履歴として保持し、先に6参照レイアウトをトレースしてから、landing pageではない
production-frame-oriented proofへ置換しました。次は人間によるreference-layout reviewです。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 / 次の確認 |
| --- | --- | --- |
| Prior Lab proof | historical AI-original / tree unchanged | current authorityではない |
| Prior reference proof | research-backed / AI-template presentation rejected / tree unchanged | rejected candidateの再reviewをしない |
| Trace basis | official 2 / journalism 2 / Yukkuri-adjacent 2 | 6実画面、6publisher、16:9 geometry |
| Shared grammar | 5 patterns threshold passed | 各3 references以上・2 cohorts以上 |
| Current proof | 6 viewer + 6 annotation + cue coverage 9/9 | human layout acceptance pending |
| Content | 8 hashes、9 cues、2/4/3 scenes、3/6 speakers exact | visual feedbackでsilent editしない |
| Rights | tracked geometry only、capturesはignored research proxy | production asset/rights未確定 |
| Silent policy | `NLMYTGEN_AUDIO_POLICY=silent`のみ | audible/public media/YMM4禁止 |
| Downstream | Shot/Motion、Asset/Rights、YMM4、render、production、publication false | human gate前に進めない |

Primary review surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_layout_reconstruction/reference_layout_proof.html`

## 次の入口

上記HTMLのlarge viewerを先に確認し、必要時だけannotation toggleと構成判断の系譜を開きます。
`reference_layout_review_sheet.md`の5問に対して、`accept`または
scene/cue/decision-specific revisionを返します。machine validationは構造と内容不変を示しますが、
最終美的判断やproduction rightsを承認しません。

## 公開・実行境界

このsliceでは既存ローカルcaptureのみを使い、public player、audio、YMM4、render、dependency
install、external communication、production/publication、PR、master integration、full suiteを
実行していません。pre-existing untracked artifacts、user process、Windows master volume、
approved content、過去2 proof packageは変更していません。
