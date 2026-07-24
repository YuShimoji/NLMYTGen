# Electron 43 Compatibility Decision — 2026-07-25 JST

Classification: `upgrade_candidate_ready`

Source:
`codex/nlmytgen-portable-dependency-lock-authority-v1` at
`2e11987ff0732d21df4a5da83d1ea557614991ac`

Outcome: resolve the exact commit from the tip of
`origin/codex/nlmytgen-electron-43-compatibility-v1`.

## Decision

Electron 43.2.0 is an upgrade-ready NLMYTGen GUI candidate. This decision is
based on the actual application window, renderer, production preload and IPC,
deterministic file-dialog paths, actual Python bridge, representative capture,
sanitized npm audit delta, clean-checkout candidate reproduction, and separate
35.7.5 rollback reproduction.

This is a compatibility and dependency-audit decision. It does not claim that
the application is universally secure, and it does not approve production,
rights, YMM4, render, publication, or the accepted cut again.

## Dependency identities and delta

| Item | Baseline | Candidate |
| --- | --- | --- |
| manifest range | `^35.0.0` | `^43.2.0` |
| exact Electron | 35.7.5 | 43.2.0 |
| `gui/package.json` SHA-256 | `a180ad8bbbba3a28e72576181259510bb42e119dd920f8995056936ffab251a2` | `740e289b228550183d8fe3adda5a68aba8caafbcf0e2d80d0d787d182a7af6b2` |
| `gui/package-lock.json` SHA-256 | `81b060f37fd2c7c4151fcf6fc402b554476d4ea6785022c8eef01aaaa9ff4a73` | `095706aba72687058863d8bca16c5a9a9f7d4e45cde3397dda3197a528d0f047` |
| lock package entries | 70 | 13 |
| `uv.lock` SHA-256 | `40e64f793775f0b0181f5ba8972c17842717dbe14bc8c0a6c0cabd14442435d0` | unchanged |

Electron is the only direct dependency and the only direct dependency changed.
The lock graph changes are Electron 43's public transitive graph: newer
`@electron/get`, `@electron-internal/extract-zip`, `@types/node`, `env-paths`,
`semver`, `undici`, and `undici-types`, with the older Electron 35 download and
proxy stack removed. No unrelated direct dependency was upgraded. The lock uses
public `registry.npmjs.org` HTTPS entries and contains no credential, private
registry, file/link/workspace dependency, localhost, drive-qualified path, or
machine-local reference.

## Security delta

The baseline `npm audit --json` returned exit 1 with:

- direct Electron aggregate: high, dev-only;
- 17 advisory entries;
- 0 low, 0 moderate, 0 critical;
- affected aggregate range `<=39.8.4`;
- fix available: Electron 43.2.0, semver-major.

The candidate audit returned exit 0 with 0 findings at all severities across
13 dependency entries. The motivating direct high Electron finding is absent
and no equal-or-higher direct finding was introduced. This supports the ready
classification. The claim is bounded to the npm audit result for this exact
lock; it is not a blanket security certification.

## Actual application compatibility

`npm --prefix gui run smoke:electron-compatibility` launches the actual
NLMYTGen `main.js`, actual `index.html` / `renderer.js`, and production
`preload.js` under Electron 43.2.0. The test-only entry point:

- creates a project-owned profile below ignored `_tmp/`;
- creates the real 900×700 application window with `show:false` and offscreen
  rendering;
- forces `NLMYTGEN_AUDIO_POLICY=silent`, Chromium mute-audio, and background
  networking disabled;
- waits for complete renderer load and two animation frames;
- captures console, preload, load, render-process-gone, window error, and
  unhandled-rejection observations;
- writes a machine-readable ignored receipt and actual-window PNG;
- closes automatically with a 15-second integration timeout.

Observed:

- Electron 43.2.0 / Chromium 150.0.7871.129 / Node 24.18.0;
- renderer `readyState=complete`, title `NLMYTGen`, 74 buttons;
- 25 production preload bridge keys present;
- no console error, security warning, preload error, load failure, renderer
  crash, or unhandled renderer error;
- `contextIsolation=true`, `sandbox=true`, `nodeIntegration=false`;
- the window closed and the project Electron process count returned to zero.

No Electron compatibility repair to product behavior or API names was needed.
The only product-file integration changes are the test-mode hook in `main.js`
and the test-only preload listener. Production-visible startup, window, bridge
names, dialog calls, and security settings remain unchanged.

## IPC, dialogs, and Python bridge

The smoke inventories all current preload methods and requires representative
read, dialog, persistence, and Python methods. It passes:

- renderer→main invoke through `select-file`, `save-ir-paste`, and
  `diagnose-script`;
- main→renderer delivery through a test-only one-shot preload bridge;
- open request shape with `openFile` and `txt` filter, returning the exact
  deterministic fixture path;
- save request shape with JSON filter, normalized absolute ignored output path,
  and byte-exact content readback;
- actual configured `uv run python -m src.cli.main diagnose-script ...`;
- UTF-8 output, stderr empty, exit code 0, parseable JSON, and 3 utterances.

No native dialog, focus, mouse, keyboard, clipboard, global shortcut, YMM4,
media generator, or public network was used.

## Representative capture

`capture_pipeline_smoke_fixtures.js` now accepts optional ignored output and
profile roots while retaining its previous tracked default. Under Electron 43,
the representative smoke produced and parsed:

- one manifest with three topics;
- 3 PNG captures;
- 3 HTML proofs;
- 25 JSON artifacts.

The output was created below `_tmp/electron43_capture_20260725`; all
BrowserWindows were hidden/offscreen. The accepted
`samples/_probe/pipeline_smoke` tracked tree had zero diff. Temporary outputs
and profiles were removed after inspection, and no project Electron process
remained.

## Clean-checkout candidate and rollback

The staged candidate tree was materialized at a short Windows path without
source `node_modules`, source browser profile, private media, YMM4 project, or
ignored evidence. It passed:

```powershell
npm --prefix gui ci
npm --prefix gui ls --depth=0
npm --prefix gui run smoke:electron-compatibility
npm --prefix gui run capture:pipeline-smoke
```

Electron read back exactly 43.2.0, candidate package-lock SHA-256 remained
byte-exact, and the isolated capture manifest parsed with three topics.

A separate worktree at the exact source commit passed `npm --prefix gui ci`,
Electron 35.7.5 readback, and the existing hidden
`gui/review_console_dom_smoke.js` startup/readback. Its package-lock SHA-256
remained exactly
`81b060f37fd2c7c4151fcf6fc402b554476d4ea6785022c8eef01aaaa9ff4a73`.
Abandoning the candidate therefore requires no source-branch mutation.

## Validation and preservation

Focused validation covers the exact version/lock, rollback and Python-lock
identities, harness security contract, public source rules, capture output
override, and sanitized receipt. All candidate GUI/capture JavaScript files
pass `node --check`. Project-state sync and `git diff --check` pass.

After the outcome commit, canonical Regression Integrity is run exactly once.
The required result is 0 failures / 0 errors with a valid declared-locator skip
contract and unchanged Git three-surface state.

Preserved without staging, deletion, or modification:

- `.playwright-mcp/`, `artifacts/`, and
  `phase-e-01-contact-acquired*.png`;
- accepted MP4, generated project, receipts, script, audio, media, timing,
  subtitles, YMM4 projects, browser profiles, run archives, and `.venv/`;
- source branch, master, PRs, tags, releases, rights, and publication state.
