# Runtime State — NLMYTGen

Project-State-ID: new-banknote-end-to-end-internal-review-video-ready-v1
State-Revision: 2026-07-21.1
Updated: 2026-07-21 JST
Product-State: new-banknote-one-command-internal-review-video-ready
Product-Gate: human-internal-review
Recommended-Next: review-local-internal-review-mp4
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 after handoff push
Tracked-Worktree: clean after handoff commit; pre-existing untracked artifacts retained

## Current Slice

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

The human internal reviewer should open the local file
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_runs/new_banknote_internal_review_v1/internal_review.mp4`
when audio playback is acceptable. Review pronunciation, rhythm, cue changes,
subtitle comfort, and proxy composition. Return `accept`, `repair`, or `reject`
with a cue id and observation for every requested change. Do not treat acceptance
as rights, production, or publication approval.

## Evidence and Access

- Command and operator notes:
  `auto_video_pipeline/README_AUTO_VIDEO_PIPELINE.md`.
- Manifest authority:
  `auto_video_pipeline/new_banknote_episode_manifest.json`.
- Sanitized tracked evidence:
  `auto_video_pipeline/validated_run_receipt.json`.
- Focused contract tests: `tests/test_episode_video_pipeline.py`.
- Local ignored outputs: `auto_video_runs/new_banknote_internal_review_v1/`.
- Main local outputs: `generated_project.local.ymmp`, `internal_review.mp4`,
  `media_validation.json`, `pipeline_run_receipt.json`, and
  `extracted_review_frames/`.

## Active Boundaries

- Human creative acceptance is pending.
- Rights clearance and production asset replacement are unresolved.
- The output is not authorized for public or external upload.
- No PR, master update, publication, release, external communication, or remote
  media access occurred.
- Superseded local force-run archives are retained as ignored `.replaced-*.local`
  directories and are not authority.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the handoff commit from the current
branch tip. Exact project/media hashes and the executed command are in the
validated run receipt; local runtime receipts remain ignored.
