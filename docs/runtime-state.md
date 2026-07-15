# Runtime State — NLMYTGen

Project-State-ID: generic-visual-static-layout-observation-passed-v1
State-Revision: 2026-07-15.2
Updated: 2026-07-15 JST
Product-State: generic-static-layout-bounded-runtime-observation-passed
Product-Gate: new-banknote-visual-direction-selection
Recommended-Next: review-new-banknote-route-a-b-c-on-provenance-branch
External-State: public-repo-feature-branch

## Current Slice

- **Exact H1 result passed**: the ignored non-fixture operator result is UTF-8
  JSON with `status=pass`, `observed_by_operator`, and exactly three pass values:
  linked-subtitle readability/non-overlap, Image visibility/crop/anchor, and
  short Text visibility/wrapping/anchor. Result SHA-256 is
  `a881c5e6bfd8be167b32c8aa7b232d0c4ed31b494563e192091aba119419dd03`.
- **Identity stayed frozen**: the same-machine project is 79,303 bytes with
  SHA-256 `100d4ebcd31e1665db90cc688492efec211d899e579d013e751c9643cc98eebc`;
  its hash, size and mtime match the batch state. The 640x360 opaque RGB asset
  remains `ad1f93bf29d07372a955645326129127a96f989786db642969ef77aad84b00b9`.
- **Evidence grades remain separate**: project parse, source/Voice invariance,
  exact counts, static defaults, exclusion checks and identity are
  machine-verified. The three visual answers are human operator observations.
  No screenshot evidence or Worker GUI observation was used.
- **Scope is exact**: the pass covers one unchanged VoiceItem with linked
  subtitle, one static 640x360 ImageItem, and one short independent `PROBE LABEL`
  TextItem at 1920x1080/60 fps for 109 frames in conservative disjoint zones.
  It does not cover another text, asset, layout, machine, topic or behavior.
- **Capability decision is bounded**: no row in the 38-capability matrix was
  regraded; proven 15 / conditional 14 / unsupported 5 / unknown 4 and C0-C5
  5/3/14/14/2/0 remain unchanged. One exact combination is recorded as
  `bounded_runtime_observed_pass` at C3. The evidence inventory is now 80 paths.
- **Sanitized tracked package exists**: the primary README, receipt, readback and
  limitations record repo-relative identities and hashes only. Ignored project,
  asset, state, observations, result and archives remain byte-preserved and
  untracked.

## Exact Next Action

The next human gate is new-banknote A/B/C visual-direction selection on the
authoritative provenance branch. Do not use the older board in this generic
branch as current authority. Re-anchor that separate branch and review its
provenance surface and visual board there; return an explicit route choice plus
S1/S2/S3 flow, misleading-diagram risk and motion-restraint judgment.

This branch must not choose A/B/C, build a selected-route project, or integrate
branches. Artifact-family integration remains a later separately authorized lane.

## Primary Evidence and Access

- Human surface:
  `samples/visual_composition_lab/runtime_probe/README_STATIC_LAYOUT_PROBE_RESULT.md`
- Sanitized receipt: `runtime_observation_receipt.json` beside that README.
- Validation readback: `runtime_observation_readback.json` beside that README.
- Scope boundary: `runtime_observation_limitations.md` beside that README.
- Capability authority: `docs/visual_system/README_GENERIC_VISUAL_CAPABILITIES.md`.

## Remote Re-entry

- Fetch `origin/codex/generic-visual-static-layout-observation-intake-v1`.
  The validated outcome commit is
  `81b9092cb44d45924c87965907e6065d63189ba4`; the current branch tip also
  contains the docs-only remote handoff seal.
- Read `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, this file, then the primary
  result surface above. Confirm `git status --short --branch` is clean and
  `git rev-list --left-right --count "HEAD...@{u}"` returns `0 0`.
- Another device can resume the product decision from the tracked sanitized
  package. The ignored project/result/archive bytes stay on the source device,
  so direct re-hashing or renewed YMM4 observation requires an explicit
  portability task; it is not a prerequisite for the next A/B/C review gate.

## Active Boundaries

- Worker Computer Use = 0 and Worker YMM4 launches = 0. The Worker only read and
  hashed completed ignored evidence; it did not regenerate or save the project.
- No screenshot capture, render/media output, dependency install, motion/effect,
  Route A/B/C selection, new-banknote branch access or modification, merge,
  rebase, cherry-pick, master mutation, rights/publication or production action.
- `capability_regraded=false` remains true in the raw result. The exact
  combination-level C3 record does not promote broader subtitle, ImageItem or
  TextItem primitives.

## Retained Quality Debt

| Debt | Impact | Owner | Revisit trigger |
| --- | --- | --- | --- |
| Cross-machine portability | Keeps project/asset proof same-machine | YMM4 integration owner | another device must materialize/open it |
| Alternate Image/Text conditions | Keeps other sizes, anchors, styles and longer text outside the pass | visual system owner | a material layout changes any bounded condition |
| Motion/effects/transitions | Keeps dynamic behavior unclaimed | motion integration owner | a selected route requires one bounded dynamic primitive |
| Real second-topic reuse | Keeps C5 at zero | episode-factory owner | a heterogeneous topic uses the same core unchanged |
| New-banknote visual route | Blocks selected-route diagnostic planning | human visual reviewer | authoritative provenance board is reviewed |

## Maintenance Note

Keep this capsule within 160 lines. Local operator evidence stays ignored; only
sanitized identities and bounded observations belong in tracked state.
