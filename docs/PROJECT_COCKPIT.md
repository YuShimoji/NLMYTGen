# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-portable-dependency-lock-authority-v1
State-Revision: 2026-07-28.1
Updated: 2026-07-28 JST
Product-State: accepted-real-media-internal-cut-with-portable-dependency-authority
Product-Gate: gui-security-major-compatibility
Recommended-Next: audit-electron-43-2-0-compatibility-in-isolated-successor
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-dependency-lock-authority-v1
Handoff-PR: none
Required-Base: c9c5f4bd50b86edd72cd3dc92254dc7ea02bee7e
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 verified after handoff push on 2026-07-28 JST
Tracked-Worktree: tracked state clean after handoff; ignored development environments preserved

短期正本は [runtime-state.md](runtime-state.md)、判断履歴は
[project-context.md](project-context.md)、三モードの機械可読結果は
[REGRESSION_INTEGRITY_2026-07-24.json](verification/REGRESSION_INTEGRITY_2026-07-24.json)
です。

## いまの一文

新紙幣pilotは、exact hashで受理されたstable internal cut、private evidenceを
tempへ複製しない三モードgreenのRegression Integrity、Git checkoutだけで取得できる
Python / Electron dependency authorityを持つ。

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
| Python lock | tracked `uv.lock`、SHA-256 `40e64f...35d0` | manifest byte不変、locked sync pass |
| GUI lock | tracked `gui/package-lock.json`、SHA-256 `81b060...4a73` | Electron 35.7.5 exact、`npm ci` pass |
| GUI security | live audit direct high 1件 / 17 advisory path | 43.2.0は別major compatibility gate |
| Rights | 全素材未clearance | production/publication/upload false |

Accepted carrier:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_runs/new_banknote_real_media_review_v1/internal_review_real_media.mp4`

Acceptance receipt:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_pipeline/human_real_media_cut_acceptance_receipt.json`

## 次の入口

`origin/codex/nlmytgen-dependency-lock-authority-v1`へfast-forward限定で
同期し、`AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → `docs/runtime-state.md`を読む。
`uv sync --extra dev --locked`と`gui`での`npm ci --no-audit --no-fund`を使い、
Electron 35.7.5をreadbackする。次laneはこのtracked baselineをrollback点にした
Electron 43.2.0 compatibility auditである。major適用、accepted MP4の再render、
creative再判断、rights判断はこのcheckpointに含まれない。

## 公開・実行境界

human creative acceptanceはexact internal cutに限って完了した。rights、
production、publication、upload、release、PR、merge、master integrationは未実施。
YMM4、render、音声再生、system volume、dependency upgradeは今回動かしていない。
lock trackingとlocked installは完了し、Electron security remediationは未完である。
