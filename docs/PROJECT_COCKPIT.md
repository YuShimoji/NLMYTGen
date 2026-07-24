# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-portable-dependency-lock-authority-ready-v1
State-Revision: 2026-07-25.1
Updated: 2026-07-25 JST
Product-State: accepted-cut-regression-green-with-portable-python-and-npm-locks
Product-Gate: electron-major-compatibility-evaluation
Recommended-Next: evaluate-electron-43-upgrade-in-isolated-branch
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-portable-dependency-lock-authority-v1
Handoff-PR: none
Required-Base: c9c5f4bd50b86edd72cd3dc92254dc7ea02bee7e
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 verified after handoff push on 2026-07-25 JST
Tracked-Worktree: tracked state clean; pre-existing ignored/private state preserved

短期正本は [runtime-state.md](runtime-state.md)、判断履歴は
[project-context.md](project-context.md)、lock authorityの検証詳細は
[DEPENDENCY_LOCK_AUTHORITY_2026-07-25.md](verification/DEPENDENCY_LOCK_AUTHORITY_2026-07-25.md)
です。

## いまの一文

accepted stable internal cutとcanonical Regression Integrityを維持したまま、
Python / npmのexact dependency graphをclean Git checkoutへ運べる状態になった。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| `uv.lock` | tracked、SHA-256 `40e64f...35d0` | PyPI public sourceのみ |
| `gui/package-lock.json` | tracked、SHA-256 `81b060...4a73` | npm public HTTPS sourceのみ |
| Python manifest | required baseとbyte-exact | dependency range変更なし |
| GUI manifest | required baseとbyte-exact | Electron range `^35.0.0`不変 |
| Electron | exact 35.7.5 | high audit findingは未解決 |
| Tracked-only setup | locked Python + npm clean install pass | private media / YMM4はコピーしない |
| Focused contract | 7 tests pass | generic doctorへ拡張しない |
| Accepted cut | exact receipt / manifest hashes不変 | 再render不要 |

## 次の入口

`origin/codex/nlmytgen-portable-dependency-lock-authority-v1`へ同期し、
`uv sync --extra dev --locked`と`npm --prefix gui ci`で依存を復元する。
次laneはElectron 43.2.0のisolated compatibility evaluationである。
startup、IPC、file dialog、Python bridge、capture scripts、audio safety、rollbackを
明示的に検証し、35.7.5をrollback baselineとして保持する。

## 公開・実行境界

dependency lockをGit authorityへ昇格しただけで、Electron security findingは解消していない。
YMM4、render、window、音声・動画再生、rights、production、publication、upload、release、
PR、merge、master integrationは未実施。private mediaはGit経由でportableにならない。
