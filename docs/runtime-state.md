# Runtime State — NLMYTGen

Project-State-ID: new-banknote-source-backed-script-review-ready-v1
State-Revision: 2026-07-13.4
Updated: 2026-07-13 JST
Product-State: new-banknote-authoritative-source-nine-cue-script-ready
Product-Gate: human-script-review-and-yymm4-batch-decision
Recommended-Next: review-source-backed-nine-cue-script
External-State: public-repo-feature-branch

## Current Slice

- **Official evidence captured**: 13 official-source captures now have stable
  identity and bounded support locations. S10 and S11 are exact-title matches.
  S04 resolves to the current exact official document, while its
  generation-time byte version remains unknown. The exact S05 572KB document
  remains unresolved; a separately identified official equivalent supports the
  adopted technical claims without identity conflation.
- **Claims adjudicated**: all 182 preserved claim records have exactly one
  outcome. Nineteen are `verified_primary`; unsupported policy-intent,
  cashless-causation, and quantitative narrative is excluded from canonical
  use.
- **Review script ready**: the internal candidate has exactly nine cues with
  scene allocation 2/4/3 and canonical speaker counts 3/6. Each factual meaning
  unit is mapped to verified claim evidence; cue traceability is complete and
  unsupported claims in spoken text are zero.
- **CSV pair ready**: canonical and YMM4-character-derived, headerless two-column
  CSVs preserve identical text and order across all nine cues. They are review
  artifacts only; YMM4 was not launched.
- **Salvage and privacy retained**: the frozen 11-title snapshot, all prior
  fingerprints, and ignored raw identity remain preserved. No raw transcript,
  source body, private path, NotebookLM link, or UUID is tracked.

## Product Position

- The external editorial input lane has moved from title-level reconciliation to
  a reproducible, official-source-backed nine-cue review package.
- The primary human surface is `README_CANONICAL_SCRIPT_REVIEW.md` in the
  new-banknote package. Source receipts, claim adjudication, cue traceability,
  the canonical script, and both CSV variants remain inspectable beside it.
- This state means ready for human script review, not editorial acceptance,
  YMM4 execution, render approval, production, rights approval, or publication.

## Exact Next Action

Review the source-backed nine-cue candidate for factual clarity, absence of
unsupported cashless-policy implication, Reimu/Marisa conversational
naturalness, 2/4/3 scene coherence, and terminology. That decision gates any
bounded YMM4 operator batch.

## Evidence and Access

- Primary tracked surface:
  `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_CANONICAL_SCRIPT_REVIEW.md`
- Source and claim evidence: `authoritative_source_registry.json`,
  `source_capture_receipts.json`, and `claim_adjudication.json` beside the
  primary surface.
- Script handoff: `canonical_script.json`, `cue_source_traceability.json`,
  `canonical_yymm4.csv`, and `derived_yymm4_import.csv` beside the primary
  surface.
- Human decision aid: `operator_review_sheet.md` beside the primary surface.

## Active Boundaries

- Official public web capture occurred only for bounded source verification.
- No NotebookLM access, Audio Overview regeneration, YMM4 launch, Computer Use,
  render, editorial acceptance, production, rights action, upload, publication,
  or master integration occurred.
- The unresolved exact S05 572KB identity and S04 generation-time byte version
  do not weaken adopted claims because those claims use separately captured
  official support.

## Maintenance Note

Keep this capsule within 160 lines. Durable implementation evidence belongs in
the tracked salvage package, tests, and Git history; full transcript content
remains local and ignored.
