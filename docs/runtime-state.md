# Runtime State — NLMYTGen

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

## Current Slice

- `DEPENDENCY_LOCKS_LOCAL_ONLY` is resolved. Existing `uv.lock` and
  `gui/package-lock.json` are tracked, reviewable dependency authority and are
  no longer ignored.
- The Python lock SHA-256 remains
  `40e64f793775f0b0181f5ba8972c17842717dbe14bc8c0a6c0cabd14442435d0`.
  The npm lock SHA-256 remains
  `81b060f37fd2c7c4151fcf6fc402b554476d4ea6785022c8eef01aaaa9ff4a73`.
- `pyproject.toml` and `gui/package.json` remain byte-exact to required base
  `c9c5f4b`. Their SHA-256 values are respectively
  `7b9ce97035187e00e396c50aa5d79862fce06c0404cc272435f93136b1efd51d`
  and
  `a180ad8bbbba3a28e72576181259510bb42e119dd920f8995056936ffab251a2`.
- The Python lock resolves only public PyPI sources. The npm lock resolves only
  public `registry.npmjs.org` HTTPS sources. Neither lock contains credential,
  private registry, host path, local wheel, or file dependency references.
- Electron remains exactly 35.7.5 under the unchanged `^35.0.0` manifest range.
  The known direct high-severity audit finding remains unresolved; tracking the
  lock does not fix or waive it.
- README setup now uses `uv sync --extra dev --locked` and
  `npm --prefix gui ci`, followed by dependency and Electron readback.
- A tracked-only candidate workspace completed isolated Python locked sync,
  Python import smoke, npm clean install, npm dependency readback, and Electron
  35.7.5 readback. Both lock hashes were byte-exact after setup.
- The exact outcome commit is revalidated in a short-path tracked-only checkout
  after commit and before push. No source `.venv`, `node_modules`, media,
  browser profile, YMM4 project, or private run output is copied into it.
- Seven focused dependency-authority tests cover Git tracking/ignore state,
  manifest identity, public dependency sources, Electron pin, locked setup
  documentation, and accepted-cut authority identity.
- Canonical Regression Integrity is the post-commit tracked-set gate. It must
  retain 0 failures / 0 errors, a valid declared-locator skip contract, Git
  status/diff/cached-diff integrity, and temporary workspace cleanup.
- No Electron upgrade, dependency upgrade, YMM4, render, window, playback,
  public-media access, rights action, publication, PR, or master mutation
  occurred in this slice.

## Product Position

The accepted real-media internal cut and evidence-safe Regression Integrity gate
remain unchanged. Clean Git checkouts now carry the exact Python and npm
dependency graphs needed for cross-terminal code development. This portability
checkpoint does not make private media portable and does not resolve Electron
security support.

## Exact Next Action

Start a separate isolated Electron major compatibility mission from this remote
branch tip. Evaluate Electron 43.2.0 first, with explicit startup, IPC, file
dialog, Python bridge, capture-script, audio-safety, and rollback gates. Keep the
current 35.7.5 lock as the rollback baseline. Do not combine the evaluation with
accepted-cut, media, rights, production, publication, PR, or master changes.

## Evidence and Access

- Dependency authority focused contract:
  `tests/test_dependency_lock_authority.py`
- Dependency authority verification:
  `docs/verification/DEPENDENCY_LOCK_AUTHORITY_2026-07-25.md`
- Canonical regression runner:
  `scripts/check_regression_integrity.py`
- Accepted-cut decision:
  `auto_video_pipeline/human_real_media_cut_acceptance_receipt.json`
- Prior three-mode result:
  `docs/verification/REGRESSION_INTEGRITY_2026-07-24.json`

## Cross-Terminal Re-entry

- Fetch and track
  `origin/codex/nlmytgen-portable-dependency-lock-authority-v1`; require
  `HEAD...@{upstream}=0/0` and a clean tracked worktree.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Run `uv sync --extra dev --locked`, then `npm --prefix gui ci`.
- Confirm `npm --prefix gui ls --depth=0` and Electron 35.7.5 before changing
  dependency authority.
- Source media, `.local.ymmp`, MP4, frames, browser profiles, and run archives
  remain ignored/private and are not restored by dependency setup.

## Active Boundaries

- Human creative acceptance remains complete for the exact stable internal cut.
- Accepted speech, wording/order, cue/subtitle timing, line breaks, and
  real-media visual treatment remain closed.
- Electron 35.7.5 remains the verified rollback baseline, not a supported or
  security-cleared final target.
- Rights clearance, production, publication, upload, release, PR, merge, and
  master integration remain unperformed.
- The next owner is the isolated Electron compatibility mission; it may change
  dependency versions only under its own approval and rollback contract.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Exact setup commands and evidence are in the 2026-07-25
dependency authority report.
