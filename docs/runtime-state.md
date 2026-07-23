# Runtime State — NLMYTGen

Project-State-ID: new-banknote-end-to-end-internal-review-video-ready-v1
State-Revision: 2026-07-23.3
Updated: 2026-07-23 JST
Product-State: new-banknote-one-command-internal-review-video-ready
Product-Gate: human-internal-review
Recommended-Next: review-local-internal-review-mp4
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-regression-integrity-v1
Handoff-PR: https://github.com/YuShimoji/NLMYTGen/pull/2
Pipeline-Implementation-Commit: e7ee831abe5fb4e51d39b1e4a7beda186ba2a8fa
Regression-Integrity-Implementation-Commit: f34f79f93fcc2db1cbc779e960bf1ed318f38048
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 after handoff push
Tracked-Worktree: clean after handoff commit; pre-existing untracked artifacts retained

## Current Slice

- The receiving terminal fast-forwarded the handoff worktree from `2f55849`
  to `58feb85`: upstream `0/0`, master ahead/behind `30/0`, tracked clean.
- Python 3.13.3, uv 0.10.7, Electron 35.7.5, ffmpeg/ffprobe 8.0.1,
  YMM4 4.54.0.1, and .NET SDK 10.0.204 are available here. The current
  46 focused tests, project-state sync, silent dry-run, and MP4 full decode pass;
  the render driver builds with 0 warnings / 0 errors.
  Electron has one direct high-severity audit finding whose fix is semver-major;
  both Python/npm lockfiles remain ignored debt.
- The support slice repaired the broad regression gate in its independent
  clean-room without changing the product state, approved content, receipts,
  manifests, visual artifacts, or tracked production pilots.
- `scripts/check_regression_integrity.py` fixes the canonical 16-module
  selection and fails if Git status, worktree diff, or cached diff changes.
- The independent-checkout result is 166 collected, 157 passed, 9 exact-locator
  local-evidence skips, 0 failures, and 0 errors. Consecutive runs were
  classification-equivalent and workspace-integrity clean.
- A same-machine audit with retained private evidence found that the runner is
  not yet evidence-safe: 135 passed, 11 contract failures, 16 temp-copy disk
  errors, and 4 skips. A tracked-only linked worktree reached 156 passed and 9
  expected skips but failed one absolute-path `git check-ignore` assertion.
  Both runs preserved Git status, worktree diff, and cached diff.
- The source YMM4 project, generated project, and internal-review MP4 are present
  at their exact ignored paths on this receiving terminal. Their SHA-256 values
  match the manifest and tracked validated receipt. The MP4 is 93,375,804 bytes;
  a fresh full-file decode exits successfully. Human review is executable now.
- The approved new-banknote pilot now has a concrete one-command path from its
  manifest and same-machine YMM4 source project through visual materialization,
  generated YMM4 project, actual YMM4 render, MP4 normalization, validation,
  frame extraction, and receipts.
- The source YMM4 project is copied non-destructively. Its nine VoiceItems remain
  object-identical; generated content adds nine cue-timed ImageItems on layer 2.
- Preflight binds nine cues in approved order to 2/4/3 scenes and the 3/6
  Reimu/Marisa split. Eighteen protected inputs are hash-locked.
- Each SVG must declare the exact cue id, scene id, and approved subtitle. Dedicated
  proxy SVGs for cues 2, 7, and 8 prevent shared layouts from burning in another
  cue's subtitle.
- The generated local project has 4415 frames at 1920×1080/60 fps, no ToolStates
  or LayoutXml carry-over, and no absolute path outside its ignored run directory.
- The actual internal-review MP4 passed ISO-BMFF structure, ffprobe, H.264/AAC,
  resolution, frame rate, duration, bitrate, size, two-stream, full-file decode,
  source-unchanged, and representative-frame variation checks.
- Nine cue frames were inspected as rendered images. All approved subtitles and
  speaker labels are readable and remain inside the frame.
- The bounded Windows driver performed YMM4 output at 10 Mbps video / 192 kbps
  audio, did not play preview or speaker audio, and cleaned up only project-owned
  processes.
- Focused validation passed: eight new synthetic/contract tests and 42 related
  new-banknote, media-validation, and silent-runtime regression tests.

## Product Position

This slice proves a real local end-to-end internal-review carrier, not production
readiness. The tracked SVGs are rights-minimal proxy geometry, and the output MP4
is an internal review artifact. Machine checks and assistant frame inspection do
not grant final aesthetic acceptance, rights clearance, publication approval, or
master integration.

## Exact Next Action

The human internal reviewer should open the exact local
`internal_review.mp4` at the expected ignored path when audio playback is
acceptable. Review pronunciation, rhythm, cue changes, subtitle comfort, and
proxy composition. Return `accept`, `repair`, or `reject` with a cue id and
observation for every requested change. Do not re-render before a cue-specific
repair is approved. 根拠: `docs/INVARIANTS.md` §Production Value North Star +
`docs/verification/REMOTE_SYNC_DEVELOPMENT_READINESS_SUPERVISOR_ROADMAP_2026-07-23.md`.

## Evidence and Access

- Command and operator notes:
  `auto_video_pipeline/README_AUTO_VIDEO_PIPELINE.md`.
- Manifest authority:
  `auto_video_pipeline/new_banknote_episode_manifest.json`.
- Sanitized tracked evidence:
  `auto_video_pipeline/validated_run_receipt.json`.
- Focused contract tests: `tests/test_episode_video_pipeline.py`.
- Regression integrity runner: `scripts/check_regression_integrity.py`.
- Full failure classification and handoff:
  `docs/verification/REGRESSION_INTEGRITY_2026-07-22.md`.
- Latest sync, same-machine readiness, caveats, and long-range goals:
  `docs/verification/REMOTE_SYNC_DEVELOPMENT_READINESS_SUPERVISOR_ROADMAP_2026-07-23.md`.
- Local ignored outputs: `auto_video_runs/new_banknote_internal_review_v1/`.
- Main local outputs: `generated_project.local.ymmp`, `internal_review.mp4`,
  `media_validation.json`, `pipeline_run_receipt.json`, and
  `extracted_review_frames/`.

## Cross-Terminal Re-entry

- The receiving terminal refreshed the worktree from tracked-clean commit
  `58feb851e8fdd35c0f205e77b86d45d0fe9c78a0` after `git fetch --prune origin`;
  at that anchor the branch and upstream were `0/0` and the branch was 30 commits
  ahead of and 0 behind `origin/master`. Resolve the final documentation commit
  from the current remote branch tip.
- Fetch `origin/codex/nlmytgen-regression-integrity-v1`, check out that branch,
  and use fast-forward-only synchronization. Confirm `HEAD...@{u}` is `0/0`
  and the tracked worktree is clean before continuing.
- Read only `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file for normal
  restart. Read the current top section of `docs/project-context.md` when the
  decision chain or local-artifact portability boundary is needed.
- Before changing the integrity gate, read
  `docs/verification/REGRESSION_INTEGRITY_2026-07-22.md`. On a clean room,
  nine skips are expected when their exact ignored/private locators are absent.
  The ignored `uv.lock` is not portable through Git and remains bounded debt.
  Do not run the canonical gate in an evidence-rich checkout until its copy
  fixtures exclude ignored media/browser profiles; a linked Git worktree also
  needs the absolute-path `check-ignore` assertion repaired.
- The tracked manifest, implementation, operator README, tests, and sanitized
  validated receipt are portable through Git. The ignored source `.local.ymmp`,
  rendered MP4, extracted frames, and force-run archives are same-machine local
  evidence and are not uploaded to the public repository.
- This receiving terminal has the exact source `.local.ymmp`, generated project,
  and review MP4. A different sending terminal lacked them; artifact availability
  remains terminal-local and historical receipts alone never prove it.
- To regenerate on another machine, provide the source project at the manifest's
  exact repo-relative path and SHA-256, then supply compatible YMM4, Chrome,
  ffmpeg/ffprobe, `uv`, and .NET. Run the documented `--dry-run` before render.
- If the local MP4 is available, do not regenerate merely for handoff. Human
  review remains the first move; regeneration is for missing media or an approved
  cue-specific repair.
- Pre-existing untracked `.playwright-mcp/`, `artifacts/`, and the two
  `phase-e-01-contact-acquired*.png` files were intentionally retained. They are
  not part of the portable authority and must not be bulk-added during restart.

## Active Boundaries

- Human creative acceptance is pending; the exact local carrier is ready for review.
- Rights clearance and production asset replacement are unresolved.
- The output is not authorized for public or external upload.
- The handoff draft PR is review-only. No master update, merge, publication,
  release, remote media access, or product-gate advancement occurred.
- Superseded local force-run archives are retained as ignored `.replaced-*.local`
  directories and are not authority.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the handoff commit from the current
branch tip. Exact project/media hashes and the executed command are in the
validated run receipt; local runtime receipts remain ignored.
