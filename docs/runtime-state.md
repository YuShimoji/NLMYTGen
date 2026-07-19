# Runtime State — NLMYTGen

Project-State-ID: new-banknote-route-a-dual-surface-visual-proof-human-review-ready-v1
State-Revision: 2026-07-19.5
Updated: 2026-07-19 JST
Product-State: new-banknote-route-a-viewer-and-annotation-proof-ready
Product-Gate: human-route-a-visual-proof-review
Recommended-Next: review-clean-route-a-viewer-frames
External-State: public-repo-feature-branch
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0
Tracked-Worktree: clean; unrelated untracked supervision artifact and intentional ignored evidence retained

## Current Slice

- **Route A direction is recorded**: the explicit user decision selects
  `route_A_security_inspection_lab` for concrete proof generation only. The new
  receipt preserves S1/S2/S3, the schematic disclaimer, and the one-principal-
  motion/non-looping budget. Final visual acceptance and implementation remain false.
- **Viewer and annotation surfaces are separated**: six clean 1920×1080 viewer
  frames cover S1, cue_003–cue_006, and S3 without cue IDs, proof status, motion
  metadata, or safe-area labels. The six annotation frames retain those audit
  overlays. The primary offline HTML defaults to viewer mode and exposes annotation
  mode as an explicit secondary section.
- **Mechanical presentation defects are closed**: approved subtitles and bounded
  explanations use deterministic semantic segments. The known punctuation-only,
  lexical/inflection split, and contact-sheet label truncation defects are absent;
  concatenated cue text remains exact and all nine motion display labels are complete.
- **Motion remains proposal-only**: all nine cues have start, emphasis, and settled
  states, duration/easing proposals, `loop: false`, and at most one principal motion.
  This is not motion playback or YMM4 feasibility evidence.
- **Subtitle and diagram boundaries are visible**: every full frame reserves
  x=84, y=780, width=1752, height=220 for approved subtitles and displays
  `模式図／実券の縮尺・配置ではありません`. All visuals use original abstract
  SVG geometry with no external assets or network resources.
- **Approved content is unchanged**: all eight approval hashes, nine cue texts/order,
  scenes 2/4/3, speakers 3/6, claims, evidence edges, canonical/derived CSVs,
  lineage, current/historical YMM4 evidence, Operator Batch, and original A/B/C
  proposal files remain byte-exact to the integrated source.
- **Actual output was inspected**: the primary offline HTML, all six viewer frames,
  all six annotation frames, contact sheet, and storyboard were rendered locally at
  1920×1080. A bounded second repair raised the four-line annotation subtitle baseline;
  no approved text, visual semantics, or motion budget changed.
- **Boundary preserved**: no YMM4 launch/project, video render, source/image fetch,
  external asset, production/publication, rights action, PR, master integration, or
  full-suite run occurred. Ignored local evidence and the unrelated untracked
  supervision artifact were not modified.

## Product Position

The A/B/C choice is closed for this slice: Route A is the selected direction for
concrete proof, not an accepted final design. The reviewer now sees clean intended
video screens first and can open separate audit evidence when needed, then judge
composition, subtitle readability, diagram risk, and restrained motion before any
Shot/Motion or Asset/Proxy/Rights contract is authorized.

## Exact Next Action

Open the pilot `route_a_visual_proof/route_a_visual_proof.html` and answer only:

1. S1／S2／S3の画面は、説明順と一致して理解しやすいですか。
2. 抽象券や各技術の模式図が、実券の正確な形状・位置・公式手順に見えませんか。
3. 字幕領域、見出し、説明文は1920×1080画面で読みやすいですか。
4. motion storyboardは十分に抑制され、各cueの主旨を邪魔していませんか。

Return `accept` or a scene/cue-specific revision. Do not choose A/B/C again.

## Evidence and Access

- Primary human surface: pilot `route_a_visual_proof/route_a_visual_proof.html`.
- Boundary and entry doc: `README_ROUTE_A_VISUAL_PROOF.md` beside it.
- Direction receipt: `human_visual_direction_selection_receipt.json`.
- Six viewer frames: `route_a_visual_proof/viewer_keyframes/`.
- Six annotation frames: `route_a_visual_proof/keyframes/`.
- Coverage: `route_a_nine_cue_contact_sheet.svg` and mapping JSON.
- Motion: `route_a_motion_storyboard.svg` and JSON.
- Machine inventories: `route_a_visual_proof_manifest.json` and readback JSON.
- Presentation revision: `visual_proof_presentation_revision_receipt.json`.
- Exact human questions: `route_a_visual_review_sheet.md`.

## Active Boundaries

- Human visual acceptance remains pending; machine checks do not settle taste,
  clarity, subtitle readability, diagram interpretation, or motion restraint.
- YMM4 feasibility and actual motion playback quality are untested.
- Pronunciation/rhythm/clipping remain unknown.
- Production assets and rights clearance remain pending.
- Shot/Motion implementation, Asset/Proxy/Rights implementation, diagnostic YMM4,
  render, production/publication, PR, master integration, remote CI/policy, and
  full-suite Integrity work remain undone and unauthorized.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the handoff commit from the current
branch tip; exact artifact hashes belong in the proof manifest.
