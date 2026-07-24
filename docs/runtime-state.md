# Runtime State — NLMYTGen

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

## Current Slice

- The accepted real-media review carrier is now the stable internal cut.
  `human_real_media_cut_acceptance_receipt.json` binds run
  `new_banknote_real_media_review_v1` to MP4 SHA-256
  `423553e0aff40619ffb0fd88bcc80344417788aa6128f0a8778aefbdd19ca476`
  and generated-project SHA-256
  `244c05ae6fe6179e9dace4b569cd5f3f9f496cfe70d46ac16ac459e787712611`.
- Speech, wording/order, cue timing, subtitle timing, subtitle line breaks, and
  real-media visual treatment are accepted. Status is `stable_internal_cut`;
  rerender is not required.
- The predecessor visual-rejection receipt remains unchanged and is referenced
  only as the decision for the rejected proxy artifact.
- Rights clearance, production, publication, upload, release, PR merge, and
  master integration remain false. The MP4 and generated project remain ignored
  same-machine evidence and are not remotely portable.
- The canonical Regression Integrity selection remains 16 modules / 170 tests.
  Independent clean-room passed 161 with 9 declared-locator skips;
  evidence-rich same-machine passed 166 with 4 declared-locator skips;
  tracked-only linked worktree passed 161 with 9 declared-locator skips.
  Every mode had 0 failures / 0 errors.
- In every mode, `git status --porcelain`, `git diff --no-ext-diff`, and
  `git diff --cached --no-ext-diff` were byte-exact before/after. JUnit and
  project-owned temporary workspaces were removed after successful inspection.
- Regression fixtures materialize only committed Git-object subtrees. Ignored
  media, browser profiles, local outputs, and unrelated evidence are never
  recursively copied into a temporary workspace.
- Local/private evidence tests require exact repo-relative locators. Missing
  locators produce documented `requires_local_evidence` skips; historical
  receipts alone never count as live availability.
- Repo-relative ignore probes work when `.git` is a directory or a linked-
  worktree file. No Thank-terminal path is encoded in the contract.
- No YMM4, render, media playback, system-volume, dependency-upgrade, or
  creative-mutation path was executed in this slice.
- A fresh receiving-terminal audit moved from the obsolete end-to-end handoff
  branch to this canonical successor at remote parity `0/0`. Its canonical
  selection passed 165 with 5 declared-locator skips, 0 failures, and 0 errors;
  workspace status/diff/cached diff remained unchanged.
- The current Thank-terminal refresh fetched three newer handoff commits and
  fast-forwarded `e574614` to `739c5a4` without merge, rebase, or history
  rewrite. The branch was 40 commits ahead of and 0 behind `origin/master`;
  master remained an ancestor.
- The current canonical selection passed 166 with 4 declared-locator skips,
  0 failures, and 0 errors in 95.459 seconds. The skip contract was valid,
  status/diff/cached diff remained unchanged, and the temporary workspace was
  removed.
- Python locked sync, Electron locked install, tracked JavaScript syntax,
  project-state sync, the focused runner contracts, and the .NET 10 Release
  build pass on the current terminal. The installed baseline is Python 3.13.3 /
  uv 0.10.7, Node 24.13.0 / npm 11.6.2 / Electron 35.7.5, .NET SDK 10.0.204,
  and ffmpeg/ffprobe 8.0.1.
- The accepted MP4, generated/source YMM4 projects, and all nine real-media
  files are present on the current terminal and match their tracked SHA-256
  authority. YMM4 4.54.0.1 is discoverable at a bounded candidate path. Silent
  real-media `--dry-run` preflight passed 18 protected inputs, 9 cues, 2/4/3
  scenes, 3/6 speakers, 4415 frames, and 9/9 provenance coverage. No window,
  playback, render, remux, or media validation stage was run.
- `uv.lock` and `gui/package-lock.json` remain ignored local authority. Locked
  sync/install succeeded, but a clean Git checkout still cannot reproduce them.
  `npm audit` reports one direct high-severity Electron aggregate; the offered
  fix is Electron 43.2.0 and is a semver-major change.
- Dependency Lock Authority attempt 1 stopped during preflight without mutation:
  its launch prompt required exact base `0b29c5a`, while the canonical remote had
  already advanced to `3869588` through the receiving-terminal supervisor
  handoff. No mission branch, lock edit, install, render, window, playback,
  commit, or push was created by that attempt.

## Product Position

The new-banknote vertical slice now has both an accepted stable internal cut and
an evidence-safe three-mode regression gate. Accepted creative dimensions are
closed unless a later explicit successor decision reopens them. This checkpoint
does not authorize rights, production, publication, upload, release, merge, or
master integration.

## Exact Next Action

Restart Dependency Lock Authority from the current remote branch tip, not the
stale `0b29c5a` launch base. Make `uv.lock` and `gui/package-lock.json`
reproducible tracked authority without changing either manifest or Electron
35.7.5. Electron major compatibility remains the separate successor mission.
Do not open windows, play media, rerender, or reopen creative review.

## Evidence and Access

- Accepted-cut decision:
  `auto_video_pipeline/human_real_media_cut_acceptance_receipt.json`
- Validated media identity:
  `auto_video_pipeline/validated_real_media_run_receipt.json`
- Three-mode machine result:
  `docs/verification/REGRESSION_INTEGRITY_2026-07-24.json`
- Three-mode explanatory report:
  `docs/verification/REGRESSION_INTEGRITY_2026-07-24.md`
- Receiving-terminal development and supervisor roadmap:
  `docs/verification/REMOTE_SYNC_DEVELOPMENT_READINESS_SUPERVISOR_ROADMAP_2026-07-24.md`
- Canonical runner:
  `scripts/check_regression_integrity.py`
- Focused contracts:
  `tests/test_regression_integrity_runner.py`

## Cross-Terminal Re-entry

- Fetch and fast-forward
  `origin/codex/nlmytgen-accepted-cut-regression-integrity-v1`; verify
  `HEAD...@{upstream}=0/0` and a clean tracked worktree.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Resolve a fresh exact launch base from the fetched remote tip. Do not reuse
  Dependency Lock Authority attempt 1's stale `0b29c5a` base.
- Source media, `.local.ymmp`, MP4, frames, profiles, and run archives stay
  ignored. Their absence is an availability boundary, not a regression failure.
- Preserve `.venv/`, `gui/node_modules/`, and any ignored/private evidence found
  on the receiving terminal. Do not assume private media is remotely portable.

## Active Boundaries

- Human creative acceptance: complete for the exact stable internal cut.
- Rerender: not required.
- Rights clearance and production asset approval: pending.
- Publication, upload, release, PR, merge, and master integration: not performed.
- Dependency portability and Electron security validation: next planned lane.
- The current Thank terminal is code-development and private-artifact preflight
  ready. The accepted carrier and YMM4 runtime are locally available, but
  rerender remains unnecessary and was not authorized by this readiness slice.
- Other receiving terminals may still lack private artifacts or YMM4. Treat that
  as terminal availability, not as loss of the tracked acceptance decision.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Exact regression results are in the two 2026-07-24 regression
artifacts. The current-terminal toolchain, private-artifact availability, and
far-goal proposal are in the 2026-07-24 supervisor roadmap.
