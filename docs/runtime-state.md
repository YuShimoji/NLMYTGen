# Runtime State — NLMYTGen

Project-State-ID: new-banknote-current-lineage-yymm4-evidence-revalidated-v1
State-Revision: 2026-07-19.1
Updated: 2026-07-19 JST
Product-State: new-banknote-existing-yymm4-import-evidence-current-lineage-compatible
Product-Gate: new-banknote-successor-branch-integration-audit
Recommended-Next: audit-and-integrate-new-banknote-successor-branches
External-State: public-repo-feature-branch
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0
Tracked-Worktree: clean; intentional ignored evidence retained

## Current Slice

- **Current approval remains sealed**: option A receipt
  `new-banknote-script-option-a-approval-v1` still fixes approved commit
  `b05eb3867caabda496fb9a0070d230a4e81aea01`, eight approved file hashes,
  nine cue texts/order, scene allocation 2/4/3, Reimu/Marisa 3/6, and the
  canonical/derived CSV pair. Approved content was not changed.
- **T00–T07 lineage remains exact**: all nine cues connect to 15 adopted
  verified-primary claims, 20 factual support units, and 21 evidence edges;
  unsupported spoken claims remain zero. Token-level authorship is not
  claimed.
- **Existing YMM4 evidence revalidated read-only**: the ignored project,
  operator result, and batch state were parsed without deletion, movement, or
  overwrite. Before/after existence, size, modification time, and SHA-256 are
  equal. No operator observation note exists.
- **Current-lineage compatibility passed**: project/result binding, 9
  VoiceItems, Reimu/Marisa 3/6, exact text and order, zero missing/duplicate,
  no reorder, 60 fps, 4415 frames, 73.583333 seconds, and per-cue timing all
  match current approved inputs and the predecessor result.
- **Sanitized successor evidence tracked**: the pilot now contains a receipt,
  readback, current-lineage traceability map, limitations, and README. The
  package records hashes and structural facts without private paths, local
  binaries, NotebookLM links/UUIDs, or raw/source/transcript bodies.
- **Determinism and failure boundaries tested**: focused tests cover exact
  acceptance, deterministic output, approval/CSV drift, project/result drift,
  order/speaker drift, mutation during read, version-warning behavior,
  optional note handling, output overlap rejection, and ignored-file status.
- **Execution boundary preserved**: YMM4 was not launched or rerun; Computer
  Use, NotebookLM, web fetch, rendering, media generation, production,
  publication, rights action, and master integration did not occur.
- **Audio quality stays unresolved**: pronunciation, rhythm, and clipping are
  `unknown`. Structural import evidence is not audio acceptance. The observed
  YMM4 4.54.0.1 versus profile 4.53.0.9 difference remains warning-only debt.
- **Branch divergence remains explicit**: the separate visual/provenance
  successor branch was not merged, rebased, or cherry-picked. Its editorial
  provenance and A/B/C visual-direction work require the next G1 integration
  audit before reuse.

## Product Position

The approved script and T00–T07 content lineage are unchanged. Existing
same-machine YMM4 import evidence is now demonstrably compatible with the
current approval and lineage locks through a tracked, sanitized successor
package. This closes the H0 reconciliation gate only; it does not establish
pronunciation quality, visual acceptance, production readiness, rights, or
publication approval.

## Exact Next Action

Run G1 as a read-first integration audit of the new-banknote successor
branches. Compare their ancestry, write sets, content authority, provenance,
visual-direction artifacts, and current approval/hash locks. Select an
integration route that preserves this revalidated receipt and rejects silent
approved-content drift. Do not merge until the audit identifies the exact
compatible commits and validation plan.

## Evidence and Access

- Revalidation entry surface:
  `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_EXISTING_YMM4_EVIDENCE_REVALIDATION.md`.
- Receipt and readback beside it:
  `existing_yymm4_evidence_revalidation_receipt.json` and
  `existing_yymm4_evidence_revalidation_readback.json`.
- Approval/evidence linkage:
  `existing_yymm4_evidence_current_lineage_traceability.json`.
- Remaining evidence limits:
  `existing_yymm4_evidence_limitations.md`.
- Current content-lineage authority remains `README_CONTENT_LINEAGE.md` and
  its approval, transformation, cue, policy, and readback artifacts.

## Active Boundaries

- Approved script, claims, sources, traceability, and CSVs are unchanged.
- Existing ignored project/result/batch state remain local, ignored, and
  non-authoritative outside this same-machine observation.
- Pronunciation/rhythm/clipping, human visual/editorial acceptance, exact S04
  generation-time binary/S05 identity, and token-level authorship remain
  unresolved or unavailable.
- G1 branch integration, visual selection, render, production project,
  rights/legal/final-thumbnail approval, upload/publication, master
  integration, and full-suite Integrity work remain undone.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the handoff commit and remote
parity from the current tracked branch after closeout; durable evidence lives
in the pilot package, focused tests, project context, and Git history.
