# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-silent-execution-guarded-reference-proof-human-review-ready-v1
State-Revision: 2026-07-20.3
Updated: 2026-07-20 JST
Product-State: new-banknote-reference-proof-ready-with-silent-development-runtime
Product-Gate: human-reference-grounded-visual-review
Recommended-Next: review-evidence-strengthened-reference-grounded-proof
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

証拠強化済みreference-grounded visual proofを変更せず、project-owned browser/mediaを
多層で静音化・封じ込めるdevelopment runtimeを追加しました。過去の大音量音声は
browser public-playerが`probable`な先行仮説ですが、発音元PIDは未検証です。次のproduct gateは
引き続きhuman visual reviewであり、final acceptanceは未付与です。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 / 次の確認 |
| --- | --- | --- |
| Incident attribution | C1 browser mediaが時系列上probable | historical PID/session不在。VOICEVOX/SofTalk/YMM4原因を主張しない |
| Default policy | `NLMYTGEN_AUDIO_POLICY=silent`のみ | audible opt-inなし。別契約なしに再生しない |
| Browser guard | isolated profile、headless、mute、autoplay抑止、DOM guard、Job Object | public playerは別途許可後もこのwrapper必須 |
| Windows session | built-in Core Audio、owned PIDだけmute | endpoint/master volumeとpre-existing sessionを変更しない |
| Local smoke | zero-amplitude PCM、DOM全条件、COM 3 checks、owned tree 10→0 | microphone-measured silenceは主張しない |
| Approval/content | 8 hashes、9 cues、CSV、claims/lineage exact | visual feedbackでsilent editしない |
| Reference proof | evidence-strengthened clean viewer + annotation | human acceptanceはpending |
| Production | YMM4、render、rights、publication、masterは未実施 | human visual gate前に進めない |

Primary review surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_grounded_visual_design/reference_grounded_visual_proof.html`

## 次の入口

上記HTML、`#annotation`、`#reference-lineage`、5問のreview sheetを人間が確認し、
`accept`またはsource/decision/scene/cue-specific revisionを返します。proof自体に外部assetや
media playbackはありません。human accept前にShot/Motion、Asset/Proxy/Rights、YMM4へ進みません。

## 公開・実行境界

このsliceではpublic player、音声生成、可聴テスト、YMM4、video render、dependency install、
production/publication、PR、master integration、full suiteを実行していません。既存browser/process、
Core Audio session、Windows master volume、approved content、visual proof、既存ignored evidenceは変更していません。
新しいsanitized audio diagnosticsだけをnarrow ignored pathへ残しています。
