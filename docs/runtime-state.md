# Runtime State — NLMYTGen

Project-State-ID: new-banknote-editorial-provenance-audited-visual-selection-ready-v1
State-Revision: 2026-07-14.2
Updated: 2026-07-14 JST
Product-State: new-banknote-script-lineage-audited-visual-direction-review-ready
Product-Gate: human-visual-direction-selection
Recommended-Next: select-new-banknote-visual-direction-with-lineage
External-State: public-repo-feature-branch

## Current Slice

- **Nine-cue lineage complete**: all nine current cues record final text hash,
  scene, speaker, adopted claims, official source IDs, raw line fingerprints,
  prior draft identity, transformation operations, authority, approval scope,
  rationale, confidence, and unresolved lineage. The coverage is 9/9.
- **Factual traceability and editorial authorship separated**: 20 factual
  meaning units are classified as 19 single-source paraphrases and one
  multi-source synthesis. Nine editorial bridges and nine character-voice
  units are Worker editorial contributions. A non-overlapping 40-segment
  partition covers all 425 final characters, and all 38 substantive units are
  realized; unresolved and unattributed substantive units are zero.
- **Transformation magnitude bounded**: the recoverable pre-editorial draft
  and current cues have 279 ordered NFKC-normalized matching characters and
  263 ordered matching tokens; one of nine cues is byte-identical. These are
  similarity indicators, not authorship percentages.
- **Decision authority visible**: D00–D10 distinguish upstream research,
  Audio Overview generation, mechanical salvage, source freeze, official
  capture, claim adjudication, Worker script generation/convergence, current
  user approval, YMM4 observation, and the visual proposal.
- **Prior user-script audit bounded**: a user-submitted raw Audio Overview
  transcript is proven as claim-discovery input. No prior user-authored or
  user-submitted finished script is present in the available repo, Git, or
  configured dropzone evidence, so the status is
  `not_proven_from_available_repo_evidence`, never `not_used`.
- **Current approval scope explicit**: the current execution contract records
  acceptance of the present nine-cue state for continuation. There is no
  independent contemporaneous approval receipt; this bounded decision is not
  authorship attribution and does not authorize future silent wording, claim,
  speaker, scene, or order changes.
- **Downstream lock active**: 24 script/CSV/trace/claim/YMM4/visual identities
  are hash-locked. Any substantive change invalidates the lock and requires a
  visible delta ledger plus successor human approval before the next human or
  YMM4 gate.
- **Human surfaces linked without content drift**: the canonical review,
  editorial revision, visual README, and HTML board now expose provenance.
  Their deterministic receipts/readback changed only for this metadata link;
  script text, CSVs, claim identities, YMM4 tracked evidence, and A/B/C route
  definitions remain unchanged.

## Product Position

- The NotebookLM → source verification → editorial shaping → YMM4 chain is now
  inspectable at claim/support-unit/cue granularity without claiming token-level
  authorship.
- Route A Security Inspection Lab remains recommended, while Routes B and C
  remain available. No route is selected, approved, or implemented.
- Tracked YMM4 observation receipts remain locked. The ignored local `.ymmp`,
  operator result, and batch state are absent in this checkout, so their local
  bytes were not reverified in this provenance slice.

## Exact Next Action

Open the provenance README first, then the visual direction board. Return A,
B, or C and answer whether the S1/S2/S3 flow fits, whether any diagram could
mislead viewers, and whether the motion proposal is restrained. A cue or scene
ID may be returned instead when revision is needed. A selected route is the
only result that authorizes planning the later diagnostic YMM4 project.

## Evidence and Access

- Primary provenance surface:
  `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/editorial_provenance/README_EDITORIAL_PROVENANCE.md`
- Per-cue, stage, contribution, prior-script, lock, future-change, and
  validation records are in the same `editorial_provenance/` directory.
- Visual review surface:
  `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/visual_scene_decision/visual_direction_board.html`
- Current tracked import evidence remains in
  `README_YMM4_IMPORT_OBSERVATION.md`, its receipt/readback, and traceability.

## Active Boundaries

- No script rewrite, source fetch, NotebookLM access, YMM4 operation, Computer
  Use, screenshot, image generation, asset download, route selection, visual
  implementation, render, production, rights approval, publication, upload,
  or master integration occurred in this slice.
- Raw transcript/source bodies, private paths, NotebookLM URLs/UUIDs, and long
  excerpts are not included in the tracked provenance package.
- Mechanical nonsemantic regeneration may retain the lock only when content
  hashes remain exact and the receipt records the delta. Substantive changes
  always require a visible successor revision.

## Retained Review Debt

| Remaining uncertainty | Workflow impact | Owner / revisit trigger | Blocks current gate |
| --- | --- | --- | --- |
| External-conversation-only prior user script may have existed | Exact external authorship cannot be proven from repo evidence | user/supervisor when a candidate artifact or conversation anchor is supplied | no |
| Ignored YMM4 project/result are absent in this checkout | Local observation bytes cannot be reverified here; tracked identities remain locked | YMM4 integration owner before selected-route diagnostic work | no |
| S04/S05 historical source precision remains incomplete | Historical provenance is less precise without weakening adopted official support | source provenance reviewer when stable source identity appears | no |
| Human visual-direction choice remains open | No selected-route diagnostic project can begin | human visual reviewer at the current A/B/C gate | yes |

## Maintenance Note

Keep this capsule within 160 lines. Durable detail belongs in the provenance
package, tracked receipts, tests, and Git history; raw/private bodies stay ignored.
