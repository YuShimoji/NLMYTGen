# Runtime State — NLMYTGen

Project-State-ID: new-banknote-notebooklm-transcript-salvaged-v1
State-Revision: 2026-07-13.2
Updated: 2026-07-13 JST
Product-State: new-banknote-notebooklm-raw-transcript-salvaged
Product-Gate: notebooklm-source-set-reconciliation
Recommended-Next: provide-notebooklm-source-list-export
External-State: public-repo-feature-branch

## Current Slice

- **Immutable intake proven**: the local NotebookLM Audio Overview transcript
  matches SHA-256 `1825c9689a050ddbfc91537a228f6af0ba2f7f033e5b681fff4f227551144437`,
  32,089 bytes, and 326 logical UTF-8 lines. The 325 CRLF separators are not
  misreported as the line count. Raw input and capture manifest remain ignored
  and untracked.
- **Deterministic salvage complete**: a reusable standard-library analyzer and
  CLI map all 326 lines, separate exact/near duplicate clusters, classify ten
  NotebookLM style classes, emit reversible ASR candidates, create provisional
  anonymous turns, and extract claim-risk candidates with zero verified claims.
- **Privacy boundary retained**: raw text, line map, normalized/deduplicated
  candidates, duplicate detail, and turn text remain in ignored
  `local_outputs/`. Tracked artifacts contain hashes, line references,
  fingerprints, categories, counts, and short labels only.
- **Expensive upstream work preserved**: the approximately 30-minute NotebookLM
  generation is recorded as user-observed evidence. NotebookLM was not reopened,
  the Audio Overview was not regenerated, and speaker splitting was not retried.

## Product Position

- The external editorial input lane now has a bounded, reviewable raw-transcript
  salvage package. The primary surface is `README_TRANSCRIPT_SALVAGE.md` in the
  new-banknote package.
- The transcript is not a verified source, final script, canonical nine-cue
  script, speaker casting, CSV, YMM4 input, production artifact, or rights/public
  approval.
- The exact NotebookLM source set is absent, so factual, quantitative,
  historical, technical, causal, policy-intent, and future claims remain
  unverified and cannot advance to canonical script shaping.

## Exact Next Action

Provide the NotebookLM source titles, source URLs or stable identifiers when
available, and intentionally excluded sources if known. Do not regenerate the
Audio Overview or manually split speakers for this gate.

## Evidence and Access

- Primary tracked surface:
  `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_TRANSCRIPT_SALVAGE.md`
- Source request:
  `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/source_reconciliation_request.md`
- Reusable analyzer: `src/pipeline/notebooklm_audio_transcript.py`
- Local full-text evidence: ignored `local_outputs/` under the tracked package.

## Active Boundaries

- No external fetch, NotebookLM access, source verification, final script,
  Reimu/Marisa casting, CSV, YMM4, render, Computer Use, dependency install,
  editorial adoption, production, rights, upload, or publication occurred.
- Full-suite drift and the unrelated integration-receipt test-path typo remain
  outside this focused slice.

## Maintenance Note

Keep this capsule within 160 lines. Durable implementation evidence belongs in
the tracked salvage package, tests, and Git history; full transcript content
remains local and ignored.
