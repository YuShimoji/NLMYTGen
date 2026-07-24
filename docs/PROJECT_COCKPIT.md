# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-electron-43-upgrade-candidate-ready-v1
State-Revision: 2026-07-25.2
Updated: 2026-07-25 JST
Product-State: portable-locks-with-validated-electron-43-runtime-candidate
Product-Gate: runtime-doctor-and-cross-terminal-artifact-ingest
Recommended-Next: build-one-command-runtime-doctor-and-private-artifact-ingest-contract
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-electron-43-compatibility-v1
Handoff-PR: none
Required-Base: 2e11987ff0732d21df4a5da83d1ea557614991ac
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required and verified after handoff push on 2026-07-25 JST
Tracked-Worktree: tracked state clean after handoff; pre-existing ignored/private state preserved

短期正本は [runtime-state.md](runtime-state.md)、判断履歴は
[project-context.md](project-context.md)、Electron判断の詳細は
[ELECTRON_43_COMPATIBILITY_2026-07-25.md](verification/ELECTRON_43_COMPATIBILITY_2026-07-25.md)
です。

## いまの一文

accepted stable internal cutとcanonical Regression Integrityを維持したまま、
Electron 43.2.0をportable GUI upgrade candidateとして実アプリ経路で検証した。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Electron candidate | exact 43.2.0、manifest `^43.2.0` | 35.7.5 source commitへrollback可 |
| npm audit | high 1 / 17 advisory → finding 0 | blanket security保証ではない |
| Actual GUI | hidden real main/renderer/preload pass | UI redesign・人間reviewなし |
| IPC / dialog | 25 bridge keys、双方向、open/save pass | test mode外の製品動作不変 |
| Python bridge | actual `uv run ... diagnose-script` pass | YMM4・media未実行 |
| Capture | ignored rootへ3 topics / 3 PNG pass | accepted artifacts差分なし |
| Security settings | isolation/sandbox維持、node integration無効 | 弱化なし |
| Dependency authority | candidate lockとrollback lockを固定 | `uv.lock`不変 |
| Accepted cut | exact receipt / manifest hashes不変 | 再render不要 |

## 次の入口

`origin/codex/nlmytgen-electron-43-compatibility-v1`へ同期し、locked setupと
hidden compatibility smokeを再実行する。次laneはone-command runtime doctorと
cross-terminal private-artifact ingest contractである。private artifactの存在、
lineage、consumer readinessをread-onlyに診断し、private data自体は複製しない。

## 公開・実行境界

Electron 43 candidateは実GUIとnpm auditの限定証拠に基づく。YMM4、render、
音声・動画再生、rights、production、publication、upload、release、PR、merge、
master integrationは未実施。private mediaはGit経由でportableにならない。
