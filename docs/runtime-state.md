# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-runtime-doctor-private-ingest-ready-v1
State-Revision: 2026-07-25.3
Updated: 2026-07-25 JST
Product-State: electron-43-portable-runtime-with-consumer-profile-doctor-and-private-ingest-contract
Product-Gate: named-private-artifact-delivery-or-standard-production-loop-gui
Recommended-Next: use-runtime-doctor-to-select-private-artifact-delivery-or-gui-production-loop
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-runtime-doctor-private-ingest-v1
Handoff-PR: none
Required-Base: 21194b60f6824eaedaddacf05bb920e1a324936a
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required and verified after handoff push on 2026-07-25 JST
Tracked-Worktree: tracked state clean after handoff; pre-existing ignored/private state preserved

## Current Slice

- `doctor-runtime` schema `nlmytgen.runtime_doctor_result.v1` now classifies
  `code`, `review`, `render`, and `regenerate` independently. `all` reports
  unavailable private profiles without failing; `--require-profile` makes only
  the named consumer readiness decisive.
- The Thank terminal has exact Electron 43.2.0, hidden/silent compatibility
  smoke, YMM4 4.54.0.1 discovery without launch, ffmpeg/ffprobe, .NET, source
  project, generated project, accepted MP4, and all nine real-media assets.
  After the outcome commit its four profiles are ready.
- A tracked-only short-path checkout restored Python/npm dependencies from the
  exact locks. `code` is ready; all 12 private artifacts are
  `receipt_only_no_live_file`, so review/render/regenerate are unavailable
  availability results rather than code regressions.
- The accepted new-banknote contract binds 12 artifact IDs and hashes:
  source project, generated project, accepted MP4, and nine real-media assets.
  Its default is validation-only with copy/apply/overwrite false.
- An empty staging root reports all 12 artifacts receipt-only and
  `ingest_ready=false`. A synthetic MP4 at the declared fixture locator reports
  `present_hash_mismatch`; requiring review returns nonzero. Neither path copies
  or overwrites data.
- Historical receipts establish accepted identity and lineage only. Live
  readiness requires the declared file, exact hash, and profile-specific
  capability evidence.
- Electron 43.2.0 remains the current feature-branch runtime. Electron 35.7.5
  at `2e11987ff0732d21df4a5da83d1ea557614991ac` remains the exact rollback
  checkpoint; both npm lock identities and `uv.lock` are unchanged.
- Focused doctor/Electron/dependency tests, project-state sync, JSON/Markdown
  parse, Git integrity, and the one post-commit canonical Regression Integrity
  run are the closeout gates.

## Product Position

The accepted real-media internal cut and canonical Regression Integrity remain
unchanged. Electron 43 code runtime portability is observable from one command,
and the same command distinguishes live private availability from historical
acceptance. Private bytes remain outside Git and outside automatic transfer.

## Exact Next Action

Run the doctor on the named destination terminal. If a review/render consumer
is selected, obtain a named recipient and separate transfer authority, then
validate the delivered staging root without applying it. If private delivery is
not selected, open the standard production-loop GUI as a separate feature slice.

## Evidence and Access

- Runtime doctor decision:
  `docs/verification/RUNTIME_DOCTOR_PRIVATE_INGEST_2026-07-25.md`
- Sanitized doctor receipt:
  `docs/verification/RUNTIME_DOCTOR_PRIVATE_INGEST_2026-07-25.json`
- Private artifact contract:
  `auto_video_pipeline/new_banknote_private_artifact_ingest_contract.json`
- Focused tests:
  `tests/test_runtime_doctor_private_ingest.py`
- Canonical regression runner:
  `scripts/check_regression_integrity.py`
- Accepted-cut decision:
  `auto_video_pipeline/human_real_media_cut_acceptance_receipt.json`

## Cross-Terminal Re-entry

- Fetch and track
  `origin/codex/nlmytgen-runtime-doctor-private-ingest-v1`; require
  `HEAD...@{upstream}=0/0` and a clean tracked worktree.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Run `uv sync --extra dev --locked`, `npm --prefix gui ci`, then
  `npm --prefix gui ls --depth=0`; require Electron 43.2.0.
- Run
  `uv run python -m src.cli.main doctor-runtime --profile all --deep --format json`.
  Require `code` for development; require other profiles only for the selected
  consumer.
- For an authorized incoming directory, add `--artifact-root <staging-root>`.
  The result is a validation plan and does not transfer or apply bytes.

## Active Boundaries

- Human creative acceptance remains complete for the exact stable internal cut.
- Accepted speech, wording/order, cue/subtitle timing, line breaks, and
  real-media visual treatment remain closed.
- The contract validates exact identities but grants no transfer, rights,
  production, publication, upload, or release authority.
- YMM4 discovery is read-only. YMM4 launch, render, playback, system-volume
  change, rights action, production, publication, PR, merge, and master
  integration remain unperformed.
- Actual cross-terminal transport still requires a named recipient and separate
  transfer authority.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Exact evidence is in the 2026-07-25 runtime-doctor report.
