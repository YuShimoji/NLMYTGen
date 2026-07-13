# Runtime State — NLMYTGen

Project-State-ID: new-banknote-notebooklm-source-set-frozen-v1
State-Revision: 2026-07-13.3
Updated: 2026-07-13 JST
Product-State: new-banknote-notebooklm-generation-source-set-frozen
Product-Gate: authoritative-source-resolution-and-claim-verification
Recommended-Next: resolve-official-source-urls-and-map-claims
External-State: public-repo-feature-branch

## Current Slice

- **Exact source snapshot frozen**: all 11 externally supplied titles are
  preserved verbatim under S01-S11 with deterministic normalized-title
  fingerprints. Ten are generation-time candidates; S07 is post-generation
  derived audio and excluded from factual authority.
- **Authority boundary explicit**: S04, S05, S10, and S11 are provisional
  primary-official candidates pending identity and content resolution. S03 is
  non-independent synthesis or a user-note candidate; S08 remains publisher
  unresolved. Commentary and tertiary material are context only.
- **Claim-family coverage complete**: all 182 sanitized claim candidates retain
  their IDs, line fingerprints, classes, and risk while receiving title-level
  source-family routing and verification requirements. The ignored line map was
  fingerprint-matched 182/182 and used only for lexical topic labels; no claim
  text was copied. Verified claims remain zero; policy/intent and causal claims
  require independent evidence, and every quantitative claim requires exact
  source, page or field, date, and unit.
- **Salvage and privacy retained**: raw identity remains SHA-256
  `1825c9689a050ddbfc91537a228f6af0ba2f7f033e5b681fff4f227551144437`,
  32,089 bytes, and 326 logical lines. Full text stays ignored in
  `local_outputs/`; no NotebookLM link, UUID, private path, or source content is
  tracked.

## Product Position

- The external editorial input lane now has a bounded title-level source-set
  freeze layered on the preserved raw-transcript salvage. The primary surface is
  `README_SOURCE_RECONCILIATION.md` in the new-banknote package.
- Source-family alignment is routing metadata, not factual support. The source
  contents, URLs, publication identities, exact claim support, and all 182 claim
  outcomes remain unresolved.
- The transcript and source snapshot are not a final script, canonical nine-cue
  script, speaker casting, CSV, YMM4 input, production artifact, or rights/public
  approval.

## Exact Next Action

Resolve stable URLs or document identifiers for S04, S05, S10, and S11 first,
capture publisher/date/content identity, and map exact claim support locations.
Then resolve S01, S02, S06, and S08 as context without treating S03 or S07 as
independent factual evidence.

## Evidence and Access

- Primary tracked surface:
  `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_SOURCE_RECONCILIATION.md`
- Canonical title snapshot and claim routing:
  `source_set_snapshot.json` and `claim_source_family_alignment.json` beside the
  primary surface.
- Reusable builders: `src/pipeline/notebooklm_source_reconciliation.py` and
  `src/pipeline/notebooklm_audio_transcript.py`.
- Local full-text evidence: ignored `local_outputs/` under the tracked package.

## Active Boundaries

- No external fetch, NotebookLM access, source-content or claim verification,
  final script, Reimu/Marisa casting, CSV, YMM4, render, Computer Use,
  dependency install, editorial adoption, production, rights, upload, or
  publication occurred.
- Full-suite drift and the unrelated integration-receipt test-path typo remain
  outside this focused slice.

## Maintenance Note

Keep this capsule within 160 lines. Durable implementation evidence belongs in
the tracked salvage package, tests, and Git history; full transcript content
remains local and ignored.
