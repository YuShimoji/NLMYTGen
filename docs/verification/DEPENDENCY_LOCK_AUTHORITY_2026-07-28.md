# Dependency Lock Authority 完了記録（2026-07-28 JST）

Scope: NLMYTGen

Required base:
`c9c5f4bd50b86edd72cd3dc92254dc7ea02bee7e`

Branch:
`codex/nlmytgen-dependency-lock-authority-v1`

## この slice で閉じた摩擦

Python と Electron の lock は別 worktree の locked install には使えていたが、
`.gitignore` 対象だったため、Git checkout だけでは依存集合を取得できなかった。
この slice は既存 lock の byte identityを保ったまま両 lock を追跡正本へ昇格し、
導入・起動導線を lock fail-closed に揃えた。

| 対象 | required base | この slice | workflow への効果 |
| --- | --- | --- | --- |
| `uv.lock` | ignored local authority | SHA-256 `40e64f793775f0b0181f5ba8972c17842717dbe14bc8c0a6c0cabd14442435d0` のまま追跡 | fresh checkout が Python dependency set を取得できる |
| `gui/package-lock.json` | ignored local authority | SHA-256 `81b060f37fd2c7c4151fcf6fc402b554476d4ea6785022c8eef01aaaa9ff4a73` のまま追跡 | `npm ci` が Electron 35.7.5 を再現できる |
| `.gitignore` | 両 lock を除外 | lock 2行だけを除去 | lock の欠落が Git status で見える |
| 開発手順 | unlocked install を案内 | locked install、更新owner、drift check を明記 | manifest と lock の同時reviewが標準になる |
| `start-gui.bat` | `uv sync` と unlocked `npx` fallback | `uv sync --locked`、未導入時 `npm ci`、local Electron 起動 | 起動時に別Electronを暗黙解決しない |

`pyproject.toml` の SHA-256
`7b9ce97035187e00e396c50aa5d79862fce06c0404cc272435f93136b1efd51d` と
`gui/package.json` の SHA-256
`a180ad8bbbba3a28e72576181259510bb42e119dd920f8995056936ffab251a2`
は required base から変えていない。GUI manifest の
`electron: ^35.0.0` と npm lock の exact 35.7.5 も不変である。

## 再現性の実測

この worktree は検証開始時に `.venv/` と `gui/node_modules/` の両方が存在しなかった。
その状態から次を実行した。依存環境は ignored のままであり、追跡対象へ追加していない。

| 検証 | 実測 | 判定 |
| --- | --- | --- |
| Python locked install | Python 3.11.0 / uv 0.10.0、7 packages resolved、6 installed | pass |
| Python drift check | `uv lock --check`、再度の `uv sync --extra dev --locked` | pass、lock hash不変 |
| Python tool readback | pytest 8.4.2 | lock と一致 |
| GUI locked install | Node 22.19.0 / npm 10.9.3、`npm ci` で70 packages | pass |
| GUI tree readback | direct dependency `electron@35.7.5` | pass |
| Electron binary readback | local `node_modules\.bin\electron.cmd --version` → `v35.7.5` | pass |
| npm drift check | `npm ci --dry-run --ignore-scripts --no-audit --no-fund` | `up to date` |
| launcher contract | locked uv、npm ci、local Electronを静的readback | pass |
| whitespace / state sync | `git diff --check`、project-state checker | pass |

lock materialization前後で両 manifest と両 lock の SHA-256 を再取得し、上記4値が
変わらないことを確認した。`npm ci --dry-run` と Electron version readbackも、
package manifest と lock の組合せが現行 contract を満たすことを確認している。

## セキュリティ境界と変えていない判断

live `npm audit --json` は Electron を direct high 1 packageとして集約し、
17 advisory pathを報告した。offered fix は Electron 43.2.0 で
`isSemVerMajor: true` である。この slice では `npm audit fix --force`、
manifest変更、transitive refresh、Electron major更新を行っていない。

accepted stable internal cut の speech、wording/order、cue timing、subtitle timing、
line breaks、real-media visual treatment、receipt、media hashは変更していない。
YMM4、GUI window、動画・音声再生、render、remux、media validationも実行していない。
rights、production、publication、upload、release、PR、merge、master integrationは
引き続き未承認・未実施である。

## 次の一意な判断

dependency portability は現行 manifest / lock について完了した。次の既定入口は、
tracked 35.7.5 baselineをrollback点として Electron 43.2.0 の互換性監査を
isolated successorで行うことである。startup、IPC、file dialog、Python bridge、
capture scripts、development audio safetyを変更前後で比較し、重大非互換時だけ
41 / 42系の最新minor比較へ分岐する。major変更そのものはこの完了記録に含めない。

根拠:
`docs/runtime-state.md` の Product Gate +
`docs/verification/REMOTE_SYNC_DEVELOPMENT_READINESS_SUPERVISOR_ROADMAP_2026-07-24.md`
の段階1 / 2分離。
