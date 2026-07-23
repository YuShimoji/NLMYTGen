# Runtime State — NLMYTGen

Project-State-ID: new-banknote-real-media-internal-review-video-ready-v1
State-Revision: 2026-07-24.1
Updated: 2026-07-24 JST
Product-State: real-media-internal-review-video-generated
Product-Gate: human-creative-review-and-rights-pending
Recommended-Next: review-local-real-media-mp4
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-real-media-visual-replacement-v1
Handoff-PR: none
Required-Base: 321cce8a3adc7fa85623f8b417afeb4b8557bfd5
Real-Media-Implementation-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 after handoff push
Tracked-Worktree: clean after handoff commit; pre-existing untracked artifacts retained

## Current Slice

- The rejected SVG/proxy visual stage has been replaced for the new-banknote
  pilot without changing the accepted speech, wording, order, cue timing, or
  subtitle line fragments.
- `build-episode-video` remains backward compatible with the old SVG manifest
  and now accepts fail-closed `image` / `video` cues with repo-relative local
  media, source provenance, optional normalized crop/time range, fit mode,
  accepted subtitle fragments, and internal-review-only status.
- The real-media manifest binds nine cues to nine provenance records and nine
  ignored local source assets. It rejects SVG input and keeps rights,
  production, publication, and upload false.
- The source YMM4 project remains SHA-256
  `beee7eab59196453c8d36b8889343cc82e876ea69e2bb00f5576bf17987eaa54`.
  Its nine VoiceItems remain object-identical, with the accepted 3/6 speaker
  split, exact text/order, cue boundaries, and 4415-frame timeline.
- Generated project:
  `auto_video_runs/new_banknote_real_media_review_v1/generated_project.local.ymmp`,
  SHA-256 `244c05ae6fe6179e9dace4b569cd5f3f9f496cfe70d46ac16ac459e787712611`.
  It has nine cue-timed PNG ImageItems and zero SVG references.
- Review carrier:
  `auto_video_runs/new_banknote_real_media_review_v1/internal_review_real_media.mp4`,
  SHA-256 `423553e0aff40619ffb0fd88bcc80344417788aa6128f0a8778aefbdd19ca476`.
  It is H.264/AAC, 1920×1080, 60 fps, 73.583008 seconds, and 93,375,529 bytes.
- ISO-BMFF structure, ffprobe, two streams, bitrate/size limits, full-file
  decode, source-unchanged binding, and 12/12 representative-frame variation
  pass.
- All nine cue frames were opened as images. Each contains recognizable source
  media, the accepted speaker label and subtitle fragments are readable and
  unclipped, and no abstract proxy is present.
- Eight assets are `official_reuse_candidate`; the FNN opening still is
  `internal_review_only`. All nine remain rights-unresolved and untracked.
- Silent execution remained enforced: no speaker/preview playback, no system
  volume change, and project-owned process cleanup passed.

## Autonomous Repairs

- The first real-media render exposed that the accepted subtitles had been
  baked into the rejected SVGs rather than supplied by VoiceItems. The repair
  records the already-accepted fragments in the real-media manifest and
  composites only the conventional subtitle band onto raster output.
- One bounded YMM4 attempt hit `ElementNotAvailableException` while opening the
  output UI. Owned-process cleanup and the source hash were verified, then the
  same command was retried successfully.

## Product Position

The visual-only repair is technically complete and the new local MP4 is ready
for human internal review. This does not grant creative acceptance, rights
clearance, production use, publication, upload, PR merge, or master integration.
Cue 005 uses the exact official deep-intaglio crop, but its source resolution is
low and remains the clearest known visual limitation.

## Exact Next Action

When explicit audio review is acceptable, the human reviewer should watch
`internal_review_real_media.mp4` once and return `accept`, or `repair` with cue
IDs. Do not publish or treat this carrier as rights-cleared.

## Evidence and Access

- Operator command:
  `auto_video_pipeline/README_AUTO_VIDEO_PIPELINE.md`
- Real-media authority:
  `auto_video_pipeline/new_banknote_real_media_episode_manifest.json`
- Sanitized source/rights evidence:
  `auto_video_pipeline/new_banknote_real_media_provenance.json`
- Human review decision:
  `auto_video_pipeline/human_review_visual_rejection_receipt.json`
- Sanitized validated evidence:
  `auto_video_pipeline/validated_real_media_run_receipt.json`
- Focused contracts:
  `tests/test_episode_video_pipeline.py`
- Ignored local evidence:
  `auto_video_runs/new_banknote_real_media_review_v1/`

## Cross-Terminal Re-entry

- Fetch and fast-forward
  `origin/codex/nlmytgen-real-media-visual-replacement-v1`; verify
  `HEAD...@{upstream}=0/0` and a clean tracked worktree.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Source media, source `.local.ymmp`, generated project, MP4, frames, and force
  archives are ignored same-machine evidence. Their absence in another checkout
  is an availability boundary, not a failed tracked contract.
- To regenerate, restore every local asset at the manifest path/hash, provide
  compatible YMM4/ffmpeg/ffprobe/uv/.NET, run `--dry-run`, then use the exact
  README command under `NLMYTGEN_AUDIO_POLICY=silent`.
- Pre-existing `.playwright-mcp/`, `artifacts/`, and
  `phase-e-01-contact-acquired*.png` were retained and are unrelated.

## Active Boundaries

- Human creative acceptance: pending.
- Rights clearance and production asset approval: pending.
- Publication, upload, release, merge, and master integration: not performed.
- No public media artifact was committed or uploaded.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the implementation commit from the
current remote branch tip. Exact hashes and cue inspection results are in the
sanitized validated receipt.
