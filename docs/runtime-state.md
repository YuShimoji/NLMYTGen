# Runtime State — NLMYTGen

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

## Current Slice

- `uv.lock` and `gui/package-lock.json` are now tracked dependency authority.
  Their SHA-256 values remain
  `40e64f793775f0b0181f5ba8972c17842717dbe14bc8c0a6c0cabd14442435d0`
  and
  `81b060f37fd2c7c4151fcf6fc402b554476d4ea6785022c8eef01aaaa9ff4a73`.
- `pyproject.toml` and `gui/package.json` are byte-unchanged from required base
  `c9c5f4b`. The GUI root range remains `electron: ^35.0.0`, and the tracked npm
  lock resolves Electron 35.7.5.
- `.gitignore` no longer excludes either lock. README now defines locked install,
  manifest-plus-lock review ownership, and non-mutating drift checks.
- `start-gui.bat` uses `uv sync --locked`. When GUI dependencies are absent it
  runs `npm ci` and launches only `node_modules\.bin\electron.cmd`; the unlocked
  `npx --yes electron` fallback is removed.
- This worktree began without `.venv/` or `gui/node_modules/`. Python 3.11.0 /
  uv 0.10.0 completed `uv sync --extra dev --locked`; Node 22.19.0 /
  npm 10.9.3 completed `npm ci`; local Electron read back as 35.7.5.
- `uv lock --check`, repeated locked sync, `npm ci --dry-run`, exact package-tree
  readback, lock hash readback, launcher contract inspection, whitespace check,
  and project-state synchronization passed without lock drift.
- Live `npm audit` still reports one direct high-severity Electron aggregate
  with 17 advisory paths. Its offered fix is Electron 43.2.0 and is a semver-major
  change, so no audit fix, manifest edit, or dependency upgrade was performed.
- The accepted stable internal cut, its content/timing/visual decision, canonical
  Regression Integrity results, private artifact boundaries, and all receipts
  remain unchanged. No YMM4, GUI window, playback, render, media operation,
  rights decision, publication, PR, merge, or master integration occurred.

## Product Position

The new-banknote vertical slice now has an accepted stable internal cut, an
evidence-safe three-mode regression gate, and Git-portable Python / Electron
dependency authority. A fresh checkout can install the reviewed dependency set
without reopening creative review. This checkpoint does not authorize Electron
major migration, rights, production, publication, upload, release, merge, or
master integration.

## Exact Next Action

Audit Electron 43.2.0 compatibility in an isolated successor before changing
either manifest or lock. Define startup, IPC, file-dialog, Python bridge,
capture-script, audio-safety, and rollback checks against the tracked 35.7.5
baseline; implement the major only after that separate approval. Do not reopen
accepted creative dimensions, rights, production, or publication.

## Evidence and Access

- Accepted-cut decision:
  `auto_video_pipeline/human_real_media_cut_acceptance_receipt.json`
- Validated media identity:
  `auto_video_pipeline/validated_real_media_run_receipt.json`
- Three-mode machine result:
  `docs/verification/REGRESSION_INTEGRITY_2026-07-24.json`
- Three-mode explanatory report:
  `docs/verification/REGRESSION_INTEGRITY_2026-07-24.md`
- Dependency lock authority report:
  `docs/verification/DEPENDENCY_LOCK_AUTHORITY_2026-07-28.md`
- Receiving-terminal development and supervisor roadmap:
  `docs/verification/REMOTE_SYNC_DEVELOPMENT_READINESS_SUPERVISOR_ROADMAP_2026-07-24.md`
- Canonical runner:
  `scripts/check_regression_integrity.py`
- Focused contracts:
  `tests/test_regression_integrity_runner.py`

## Cross-Terminal Re-entry

- Fetch and fast-forward
  `origin/codex/nlmytgen-dependency-lock-authority-v1`; verify
  `HEAD...@{upstream}=0/0` and a clean tracked worktree.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Run `uv sync --extra dev --locked`, then `npm ci --no-audit --no-fund` in
  `gui/`. A lock drift or Electron version other than 35.7.5 is a setup failure.
- Source media, `.local.ymmp`, MP4, frames, profiles, and run archives stay
  ignored. Their absence is an availability boundary, not a regression failure.
- Preserve `.venv/`, `gui/node_modules/`, and any ignored/private evidence found
  on the receiving terminal. Do not assume private media is remotely portable.

## Active Boundaries

- Human creative acceptance: complete for the exact stable internal cut.
- Rerender: not required.
- Rights clearance and production asset approval: pending.
- Publication, upload, release, PR, merge, and master integration: not performed.
- Dependency portability: complete for the current manifests and locks.
- Electron 35.7.5 security remediation: pending isolated major-compatibility
  decision; live audit remains one direct high-severity aggregate.
- Other receiving terminals may still lack private artifacts or YMM4. Treat that
  as terminal availability, not as loss of the tracked acceptance decision.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Exact regression results are in the two 2026-07-24 regression
artifacts. Lock authority details are in the 2026-07-28 dependency report;
private-artifact availability and the farther roadmap remain in the 2026-07-24
supervisor roadmap.
