# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-real-media-internal-review-video-ready-v1
State-Revision: 2026-07-24.1
Updated: 2026-07-24 JST
Product-State: real-media-internal-review-video-generated
Product-Gate: human-creative-review-and-rights-pending
Recommended-Next: review-local-real-media-mp4
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-real-media-visual-replacement-v1
Handoff-PR: none
Required-Base: 321cce8a3adc7fa85623f8b417afeb4b8557bfd5
Real-Media-Implementation-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 after handoff push
Tracked-Worktree: clean after handoff commit; pre-existing untracked artifacts retained

短期正本は [runtime-state.md](runtime-state.md)、静音契約は
[DEVELOPMENT_AUDIO_SAFETY.md](DEVELOPMENT_AUDIO_SAFETY.md)、判断履歴は
[project-context.md](project-context.md) です。

## いまの一文

新紙幣pilotは、承認済み音声・4415-frame timing・字幕改行を固定したまま、
SVG proxyを9 cueの実媒体へ置換し、検証済み内部review MP4まで実生成済みです。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Pipeline | image/video + provenance → PNG → YMMP → YMM4 render → validation | 旧SVG manifestは互換維持、新manifestはSVG 0 |
| Protected content | VoiceItems 9、霊夢3/魔理沙6、text/order/timing/line fragments exact | source project unchanged |
| Real media | 9 assets / provenance 9/9 / cue coverage 9/9 | official candidate 8、internal-only 1 |
| Generated project | SHA-256 `244c05...2611`、ImageItems 9、4415 frames | ignored local |
| Review MP4 | H.264/AAC、1920×1080、60 fps、73.583008 sec、93,375,529 bytes | SHA-256 `423553...a476` |
| Visual inspection | cue_001〜009を実画像で確認、字幕可読・clipなし | cue_005 sourceは低解像度 |
| Silent policy | speaker/preview なし、volume不変、owned cleanup pass | audible reviewは人間gate |
| Rights | 全素材未clearance | production/publication/upload false |

Primary review surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_runs/new_banknote_real_media_review_v1/internal_review_real_media.mp4`

## 次の入口

`origin/codex/nlmytgen-real-media-visual-replacement-v1`へfast-forward限定で
同期し、`AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → `docs/runtime-state.md`を
読みます。tracked authorityはcode / manifest / provenance / decision receipt /
validated receipt / tests / READMEだけです。media、YMMP、MP4、framesはignored
same-machine evidenceなので、別端末ではmanifest path/hashどおり復元します。

## 公開・実行境界

この成果は内部review cutです。creative acceptance、rights、production、
publication、upload、release、PR、merge、master integrationは未実施です。
既存untracked artifactとユーザー所有プロセスには触れていません。
