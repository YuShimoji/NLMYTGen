# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-end-to-end-internal-review-video-ready-v1
State-Revision: 2026-07-22.2
Updated: 2026-07-22 JST
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

このページはpublic repositoryで現在地だけを読む追跡済みMarkdownです。短期正本は
[runtime-state.md](runtime-state.md)、開発時の静音契約は
[DEVELOPMENT_AUDIO_SAFETY.md](DEVELOPMENT_AUDIO_SAFETY.md)、判断履歴は
[project-context.md](project-context.md)にあります。

## いまの一文

承認済み新紙幣pilotを、manifestから実YMM4 project、実YMM4 render、検証済み内部レビュー
MP4まで一コマンドで到達できる状態にしました。次はローカルMP4の人間レビューです。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 / 次の確認 |
| --- | --- | --- |
| Pipeline | manifest → PNG → YMMP → YMM4 render → MP4 validation | implementation commit `e7ee831` |
| Content | 18 locked inputs、9 cues、2/4/3 scenes、3/6 speakers exact | 9 VoiceItems object-identical |
| Generated project | 1920×1080 / 60 fps / 4415 frames | SHA-256 `f0361f4704adda2d87c342a9d281170ab3250fa9d9ea622a52bb3c8850019853` |
| Review MP4 | H.264/AAC / 73.583008 sec / 93,375,804 bytes | SHA-256 `f2444f9657a569e9a374582765c41a28e414040a018f029b0180f256657421f7` |
| Validation | full decode、12 unique frames、9 cue visual inspection | focused 46 passed。独立clean-room回帰は157 passed / 9 skips、same-machine/worktree caveatあり |
| Silent policy | `NLMYTGEN_AUDIO_POLICY=silent` | speaker/preview playbackなし、owned process cleanup済み |
| Rights | tracked proxy geometryのみ | production asset/rights未確定 |
| Downstream | human creative review、rights、production、publication false | machine proofだけでgateを開かない |

Primary review surface（ignored local artifact）:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_runs/new_banknote_internal_review_v1/internal_review.mp4`

## 次の入口

別端末では`origin/codex/nlmytgen-regression-integrity-v1`をfetchし、同branchへ
fast-forward限定で同期します。`AGENTS.md` → `docs/REPO_LOCAL_RULES.md` →
`docs/runtime-state.md`を読み、必要時だけ`docs/project-context.md`最上部を参照します。

MP4が同端末にある場合は再生成せず、発音、リズム、cue切替、字幕の読み心地、proxy構成を
確認し、`accept` / `repair` / `reject`をcue id付きで返します。MP4やsource `.local.ymmp`は
public Gitへ載せないsame-machine evidenceなので、別マシンで必要ならmanifest記載のexact path/hashを
満たすsource projectとYMM4/Chrome/ffmpeg/uv/.NET環境を用意し、先に`--dry-run`を通します。

## 公開・実行境界

このsliceは内部レビュー用proxy evidenceです。draft PR #2は回帰支援差分のreview-onlyで、
公開upload、publication、rights承認、production、merge、master integrationは実施していません。
tracked manifest/code/tests/sanitized receiptだけがGitで
可搬です。ignored MP4/YMMP/frames/force-run archive、pre-existing untracked artifacts、
Windows master volume、approved content、過去proof packageはpublic remoteへ送りません。
