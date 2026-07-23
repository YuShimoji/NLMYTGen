# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-end-to-end-internal-review-video-ready-v1
State-Revision: 2026-07-23.4
Updated: 2026-07-23 JST
Product-State: new-banknote-one-command-internal-review-video-ready
Product-Gate: human-internal-review
Recommended-Next: review-local-internal-review-mp4
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-regression-integrity-v1
Handoff-PR: https://github.com/YuShimoji/NLMYTGen/pull/2
Pipeline-Implementation-Commit: e7ee831abe5fb4e51d39b1e4a7beda186ba2a8fa
Regression-Integrity-Implementation-Commit: f34f79f93fcc2db1cbc779e960bf1ed318f38048
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 after handoff push
Tracked-Worktree: clean after handoff commit; pre-existing untracked artifacts retained
Handoff-Anchor: eb883979479fd9a0cdace1d82fdb1295e6c80950
Handoff-Verified: 2026-07-23 JST

このページはpublic repositoryで現在地だけを読む追跡済みMarkdownです。短期正本は
[runtime-state.md](runtime-state.md)、開発時の静音契約は
[DEVELOPMENT_AUDIO_SAFETY.md](DEVELOPMENT_AUDIO_SAFETY.md)、判断履歴は
[project-context.md](project-context.md)にあります。

## いまの一文

承認済み新紙幣pilotは、manifestから実YMM4 render、検証済み内部レビューMP4まで一コマンド
到達済みです。この受信端末にはreceiptと一致するexact carrierがあるため、次は再生成せず、
人間が通し視聴して内部review decisionを閉じます。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 / 次の確認 |
| --- | --- | --- |
| Pipeline | manifest → PNG → YMMP → YMM4 render → MP4 validation | implementation commit `e7ee831` |
| Content | 18 locked inputs、9 cues、2/4/3 scenes、3/6 speakers exact | 9 VoiceItems object-identical |
| Generated project | 1920×1080 / 60 fps / 4415 frames | current端末で存在・SHA-256 `f0361f...9853`一致 |
| Review MP4 | H.264/AAC / 73.583008 sec / 93,375,804 bytes | current端末で存在・SHA-256 `f2444f...21f7`一致 |
| Validation | focused 46、state sync、dry-run、.NET 10 driver build、full decode | current端末でpass。独立clean-room回帰は157 passed / 9 skips、same-machine/worktree caveatあり |
| Silent policy | `NLMYTGEN_AUDIO_POLICY=silent` | speaker/preview playbackなし、owned process cleanup済み |
| Rights | tracked proxy geometryのみ | production asset/rights未確定 |
| Downstream | human creative review、rights、production、publication false | machine proofだけでgateを開かない |

Primary review surface（ignored local artifact、現在端末で利用可能）:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_runs/new_banknote_internal_review_v1/internal_review.mp4`

## 次の入口

別端末では`origin/codex/nlmytgen-regression-integrity-v1`をfetchし、同branchへ
fast-forward限定で同期します。`AGENTS.md` → `docs/REPO_LOCAL_RULES.md` →
`docs/runtime-state.md`を読み、必要時だけ`docs/project-context.md`最上部を参照します。
handoff commitは固定文字列ではなくremote branch tipから解決し、`HEAD...@{u}=0/0`を
確認してください。今回の再監査anchorは`eb88397`で、FF-only pullはalready up to date、
この文書更新前には`origin/master`に31 ahead / 0 behindでした。

送信端末ではMP4とsource `.local.ymmp`が不在でしたが、この受信端末には3つのexact private artifactが
あり、hash照合、silent `--dry-run`、fresh full decodeまでpassしています。再生成せず、発音、リズム、
cue切替、字幕の読み心地、proxy構成を`accept` / `repair` / `reject`へ決定します。詳細と長期goalは
`docs/verification/REMOTE_SYNC_DEVELOPMENT_READINESS_SUPERVISOR_ROADMAP_2026-07-23.md`を参照します。

## 公開・実行境界

このsliceは内部レビュー用proxy evidenceです。draft PR #2は回帰支援差分のreview-onlyで、
公開upload、publication、rights承認、production、merge、master integrationは実施していません。
tracked manifest/code/tests/sanitized receiptだけがGitで
可搬です。ignored MP4/YMMP/frames/force-run archive、pre-existing untracked artifacts、
Windows master volume、approved content、過去proof packageはpublic remoteへ送りません。
