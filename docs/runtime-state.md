# Runtime State — NLMYTGen

Project-State-ID: new-banknote-stable-internal-cut-regression-integrity-green-v1
State-Revision: 2026-07-24.2
Updated: 2026-07-24 JST
Product-State: accepted-real-media-internal-cut-with-evidence-safe-regression-gate
Product-Gate: dependency-portability-and-gui-security
Recommended-Next: make-dependency-locks-portable-and-validate-electron-upgrade
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-accepted-cut-regression-integrity-v1
Handoff-PR: none
Required-Base: c77a89b8db15d5c0b286afc322dd6842a016a606
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after outcome push
Tracked-Worktree: clean required after outcome commit; preserved untracked artifacts remain

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

## Product Position

The new-banknote vertical slice now has both an accepted stable internal cut and
an evidence-safe three-mode regression gate. Accepted creative dimensions are
closed unless a later explicit successor decision reopens them. This checkpoint
does not authorize rights, production, publication, upload, release, merge, or
master integration.

## Exact Next Action

Start a separate dependency-portability and GUI-security lane. Decide how
`uv.lock` and `gui/package-lock.json` become reproducible tracked authority, then
validate the required Electron major upgrade without changing the accepted cut.
Do not rerender or reopen creative review as part of that lane.

## Evidence and Access

- Accepted-cut decision:
  `auto_video_pipeline/human_real_media_cut_acceptance_receipt.json`
- Validated media identity:
  `auto_video_pipeline/validated_real_media_run_receipt.json`
- Three-mode machine result:
  `docs/verification/REGRESSION_INTEGRITY_2026-07-24.json`
- Three-mode explanatory report:
  `docs/verification/REGRESSION_INTEGRITY_2026-07-24.md`
- Canonical runner:
  `scripts/check_regression_integrity.py`
- Focused contracts:
  `tests/test_regression_integrity_runner.py`

## Cross-Terminal Re-entry

- Fetch and fast-forward
  `origin/codex/nlmytgen-accepted-cut-regression-integrity-v1`; verify
  `HEAD...@{upstream}=0/0` and a clean tracked worktree.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Source media, `.local.ymmp`, MP4, frames, profiles, and run archives stay
  ignored. Their absence is an availability boundary, not a regression failure.
- Preserve `.playwright-mcp/`, `artifacts/`, and
  `phase-e-01-contact-acquired*.png`; they are unrelated user evidence.

## Active Boundaries

- Human creative acceptance: complete for the exact stable internal cut.
- Rerender: not required.
- Rights clearance and production asset approval: pending.
- Publication, upload, release, PR, merge, and master integration: not performed.
- Dependency portability and Electron security validation: next planned lane.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Exact results are in the two 2026-07-24 regression artifacts.
