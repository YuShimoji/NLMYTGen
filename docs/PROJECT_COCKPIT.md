# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-end-to-end-internal-review-video-ready-v1
State-Revision: 2026-07-23.2
Updated: 2026-07-23 JST
Product-State: new-banknote-one-command-internal-review-video-ready
Product-Gate: human-internal-review
Recommended-Next: restore-local-review-carrier
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-regression-integrity-v1
Handoff-PR: https://github.com/YuShimoji/NLMYTGen/pull/2
Pipeline-Implementation-Commit: e7ee831abe5fb4e51d39b1e4a7beda186ba2a8fa
Regression-Integrity-Implementation-Commit: f34f79f93fcc2db1cbc779e960bf1ed318f38048
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 after handoff push
Tracked-Worktree: clean after handoff commit; pre-existing untracked artifacts retained
Handoff-Anchor: 2f558499efc66810314d823627bce23ea6400883
Handoff-Verified: 2026-07-23 JST

このページはpublic repositoryで現在地だけを読む追跡済みMarkdownです。短期正本は
[runtime-state.md](runtime-state.md)、開発時の静音契約は
[DEVELOPMENT_AUDIO_SAFETY.md](DEVELOPMENT_AUDIO_SAFETY.md)、判断履歴は
[project-context.md](project-context.md)にあります。

## いまの一文

承認済み新紙幣pilotは、過去のsame-machine evidenceでmanifestから実YMM4 render、検証済み
内部レビューMP4まで一コマンド到達済みです。現在端末ではprivate carrierが欠けているため、
次はexact MP4またはsource projectを復元し、人間レビューへ再接続します。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 / 次の確認 |
| --- | --- | --- |
| Pipeline | manifest → PNG → YMMP → YMM4 render → MP4 validation | implementation commit `e7ee831` |
| Content | 18 locked inputs、9 cues、2/4/3 scenes、3/6 speakers exact | 9 VoiceItems object-identical |
| Generated project | historical receiptは1920×1080 / 60 fps / 4415 frames | current端末では不在。期待SHA-256 `f0361f...9853` |
| Review MP4 | historical receiptはH.264/AAC / 73.583008 sec | current端末では不在。期待SHA-256 `f2444f...21f7` |
| Validation | focused 46、state sync、.NET 10 driver build | current端末でpass。独立clean-room回帰は157 passed / 9 skips、same-machine/worktree caveatあり |
| Silent policy | `NLMYTGEN_AUDIO_POLICY=silent` | speaker/preview playbackなし、owned process cleanup済み |
| Rights | tracked proxy geometryのみ | production asset/rights未確定 |
| Downstream | human creative review、rights、production、publication false | machine proofだけでgateを開かない |

Primary review surface（ignored local artifact、現在端末では復元待ち）:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_runs/new_banknote_internal_review_v1/internal_review.mp4`

## 次の入口

別端末では`origin/codex/nlmytgen-regression-integrity-v1`をfetchし、同branchへ
fast-forward限定で同期します。`AGENTS.md` → `docs/REPO_LOCAL_RULES.md` →
`docs/runtime-state.md`を読み、必要時だけ`docs/project-context.md`最上部を参照します。
handoff commitは固定文字列ではなくremote branch tipから解決し、`HEAD...@{u}=0/0`を
確認してください。今回のsync anchorは`2f55849`で、この時点では
`origin/master`に29 ahead / 0 behindでした。

現在端末の全4 worktreeにはMP4とsource `.local.ymmp`がありません。既存MP4が別の許可済み端末に
残っていれば再生成せずexpected path/hashへ復元し、発音、リズム、cue切替、字幕の読み心地、proxy構成を
`accept` / `repair` / `reject`へ決定します。MP4が失われていればmanifestのexact source path/hash、
YMM4 discovery、silent `--dry-run`を満たしてから承認済み再renderへ進みます。詳細と長期goalは
`docs/verification/REMOTE_SYNC_DEVELOPMENT_READINESS_SUPERVISOR_ROADMAP_2026-07-23.md`を参照します。

## 公開・実行境界

このsliceは内部レビュー用proxy evidenceです。draft PR #2は回帰支援差分のreview-onlyで、
公開upload、publication、rights承認、production、merge、master integrationは実施していません。
tracked manifest/code/tests/sanitized receiptだけがGitで
可搬です。ignored MP4/YMMP/frames/force-run archive、pre-existing untracked artifacts、
Windows master volume、approved content、過去proof packageはpublic remoteへ送りません。
