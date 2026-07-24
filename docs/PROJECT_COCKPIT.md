# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-stable-internal-cut-regression-integrity-green-v1
State-Revision: 2026-07-24.5
Updated: 2026-07-24 JST
Product-State: accepted-real-media-internal-cut-with-evidence-safe-regression-gate
Product-Gate: dependency-portability-and-gui-security
Recommended-Next: restart-dependency-lock-authority-from-current-remote-tip
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-accepted-cut-regression-integrity-v1
Handoff-PR: none
Required-Base: c77a89b8db15d5c0b286afc322dd6842a016a606
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 verified after handoff push on 2026-07-24 JST
Tracked-Worktree: tracked state clean; local ignored development environments preserved

短期正本は [runtime-state.md](runtime-state.md)、判断履歴は
[project-context.md](project-context.md)、三モードの機械可読結果は
[REGRESSION_INTEGRITY_2026-07-24.json](verification/REGRESSION_INTEGRITY_2026-07-24.json)
です。

## いまの一文

新紙幣pilotは、exact hashで受理されたstable internal cutと、private evidenceを
tempへ複製しない三モードgreenのcanonical Regression Integrity gateを持つ。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Accepted MP4 | SHA-256 `423553...a476`、`stable_internal_cut` | ignored local、再render不要 |
| Generated project | SHA-256 `244c05...2611` | ignored local、byte変更なし |
| Closed dimensions | speech / wording-order / cue timing / subtitle timing-line breaks / real-media visual | successor decisionなしに再開しない |
| Clean-room | 161 pass / 9 declared-locator skip | failure 0 / error 0 |
| Same-machine | 166 pass / 4 declared-locator skip | 存在するprivate evidence 5件を実行 |
| Linked worktree | 161 pass / 9 declared-locator skip | `.git` file、absolute-path依存なし |
| Workspace integrity | status / diff / cached diff全mode不変 | temp回収済み |
| Copy boundary | Git-object tracked subtreeのみ | media/profile/local outputs 0 copy |
| Rights | 全素材未clearance | production/publication/upload false |

Accepted carrier:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_runs/new_banknote_real_media_review_v1/internal_review_real_media.mp4`

Acceptance receipt:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_pipeline/human_real_media_cut_acceptance_receipt.json`

## 次の入口

`origin/codex/nlmytgen-accepted-cut-regression-integrity-v1`へfast-forward限定で
同期し、`AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → `docs/runtime-state.md`を読む。
Dependency Lock Authority attempt 1はlaunch base `0b29c5a`と、すでに
`3869588`へ進んでいたcanonical remoteの不一致により、preflightで無変更停止した。
次laneはfetch後のcurrent remote tipを新しいexact baseとしてdependency lock authorityを
再開する。Electron major compatibilityは後続へ分離し、accepted MP4の再render、
creative再判断、rights判断を混ぜない。

2026-07-24 Thank端末では`e574614`から`739c5a4`へ3 commitをfast-forwardし、
canonical selectionは`166 passed / 4 declared-locator skips / 0 failed / 0 errors`。
9/9 real-media、source/generated project、accepted MP4はtracked hashと一致し、
YMM4 4.54.0.1を検出、silent `--dry-run` preflightもpassした。再render、window、
playbackは実行していない。依存lockはlocked installに使えるがignoredのため、
clean checkoutのportable authorityにはまだなっていない。

## 公開・実行境界

human creative acceptanceはexact internal cutに限って完了した。rights、
production、publication、upload、release、PR、merge、master integrationは未実施。
YMM4、render、音声再生、system volume、dependency upgradeは今回動かしていない。
