# Runtime State — NLMYTGen

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

## Current Slice

- Electron 43.2.0 is the exact locked GUI runtime under manifest range
  `^43.2.0`. The candidate npm lock SHA-256 is
  `095706aba72687058863d8bca16c5a9a9f7d4e45cde3397dda3197a528d0f047`.
- Source commit `2e11987ff0732d21df4a5da83d1ea557614991ac` remains the immutable
  rollback checkpoint. Its Electron version is 35.7.5 and npm lock SHA-256 is
  `81b060f37fd2c7c4151fcf6fc402b554476d4ea6785022c8eef01aaaa9ff4a73`.
- `uv.lock` and the Python dependency graph are unchanged at SHA-256
  `40e64f793775f0b0181f5ba8972c17842717dbe14bc8c0a6c0cabd14442435d0`.
- The baseline audit had one direct, dev-only high Electron aggregate with 17
  advisory entries and proposed Electron 43.2.0 as a semver-major fix. The
  candidate audit reports zero findings at every severity. This proves removal
  of the motivating npm audit finding; it is not a blanket security claim.
- The actual NLMYTGen `main.js` window, actual renderer, and production preload
  run hidden/offscreen with an isolated project profile. Renderer load,
  25 bridge keys, renderer→main invoke, main→renderer delivery, deterministic
  open/save dialog paths, and the actual `uv run python -m src.cli.main`
  bridge pass without console, security, preload, load, crash, or unhandled
  rejection observations.
- The smoke retains `contextIsolation=true`, `sandbox=true`, and
  `nodeIntegration=false`. It forces the development audio policy to silent,
  adds Chromium mute/background-network switches, displays no window, and
  leaves no project Electron process running.
- The representative pipeline-smoke capture accepts an environment-selected
  ignored output root while retaining its prior default. Electron 43 produced
  one parseable manifest, 3 PNG, 3 HTML, and 25 JSON outputs for three topics;
  accepted tracked pipeline-smoke artifacts remained byte-unchanged.
- Candidate and rollback clean-checkout proofs use separate short Windows
  worktrees. Candidate `npm ci`, Electron 43 readback, compatibility smoke,
  dependency readback, lock identity, and capture pass. Rollback `npm ci`,
  Electron 35.7.5 readback, existing hidden DOM smoke, and source lock identity
  pass.
- Focused contract tests, GUI JavaScript syntax, project-state sync,
  `git diff --check`, Git three-surface integrity, and one post-commit canonical
  Regression Integrity run are the closeout gates.

## Product Position

The accepted real-media internal cut and canonical Regression Integrity remain
unchanged. A portable Electron 43 upgrade candidate now exists for GUI code
development, with the exact 35.7.5 source checkpoint retained as rollback.
Private media and YMM4 projects remain outside Git and outside this decision.

## Exact Next Action

Build one read-only runtime doctor that checks locked Python/npm recovery,
Electron GUI capability, required private artifact locators, and consumer-safe
ingest readiness without copying private artifacts. Then define one
cross-terminal private-artifact ingest contract that reports availability and
lineage while leaving YMM4, render, rights, and publication as separate gates.

## Evidence and Access

- Compatibility decision:
  `docs/verification/ELECTRON_43_COMPATIBILITY_2026-07-25.md`
- Sanitized receipt:
  `docs/verification/ELECTRON_43_COMPATIBILITY_2026-07-25.json`
- Focused contract:
  `tests/test_electron_43_compatibility_contract.py`
- Canonical regression runner:
  `scripts/check_regression_integrity.py`
- Accepted-cut decision:
  `auto_video_pipeline/human_real_media_cut_acceptance_receipt.json`

## Cross-Terminal Re-entry

- Fetch and track
  `origin/codex/nlmytgen-electron-43-compatibility-v1`; require
  `HEAD...@{upstream}=0/0` and a clean tracked worktree.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Run `uv sync --extra dev --locked`, `npm --prefix gui ci`, then
  `npm --prefix gui ls --depth=0`; require Electron 43.2.0.
- Run `npm --prefix gui run smoke:electron-compatibility` with no visible
  window. The receipt is written only under ignored `_tmp/`.
- Source media, `.local.ymmp`, MP4, frames, browser profiles, and run archives
  remain ignored/private and are not restored by dependency setup.

## Active Boundaries

- Human creative acceptance remains complete for the exact stable internal cut.
- Accepted speech, wording/order, cue/subtitle timing, line breaks, and
  real-media visual treatment remain closed.
- Electron 43 is an upgrade-ready candidate based on the recorded runtime and
  audit gates, not a universal security guarantee.
- Rights clearance, production, YMM4, render, publication, upload, release, PR,
  merge, and master integration remain unperformed.
- The next owner is the runtime-doctor/private-ingest slice. It must preserve
  35.7.5 rollback identity and must not treat private artifact absence as a code
  regression.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Exact evidence is in the 2026-07-25 compatibility report.
