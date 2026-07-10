# Runtime State — NLMYTGen

Project-State-ID: episode-002-ymm4-speaker-alias-ready-for-reobservation-v1
State-Revision: 2026-07-11.1
Updated: 2026-07-11 JST
Product-State: episode-002-ymm4-speaker-alias-ready-for-reobservation
Product-Gate: bounded-yymm4-alias-reobservation
Recommended-Next: reobserve-derived-yymm4-csv
External-State: public-repo-feature-branch

## Current Slice

- **Alias profile implemented**: the Episode 002 artifact chain now explicitly
  selects `ymm4_4_53_0_9_yukkuri_characters_ja_v1`. It maps canonical `れいむ`
  to `ゆっくり霊夢` and `まりさ` to `ゆっくり魔理沙`, requires strict coverage,
  and does not claim a universal environment default.
- **Canonical input preserved**: the tracked nine-row canonical CSV remains
  unchanged at SHA-256
  `6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C`.
  The derived import CSV is a separate artifact with SHA-256
  `5452DE96DC6EF012400A132BA5BAE80B8553C1B1CDD27860D36674C25AF391BC`.
- **Responsibility contract corrected**: CSV import expects only `VoiceItem` and
  linked subtitle output. `ImageItem` and independent `TextItem` placeholders
  belong to a separate diagnostic project whose gate is
  `not_authorized / not_attempted`; their absence is not a CSV failure.
- **Historical evidence preserved**: the 2026-07-10 receipt remains byte-for-byte
  unchanged at SHA-256
  `DC756D9C4EE9ABDFDDFB284B2B8EC70B227DDEB5E365C1BBB8EE8438D8C9A5B5`.
  Its `partial` result remains historical v1 evidence under the former mixed
  placeholder contract.
- **Bounded GUI re-observation blocked safely**: YMM4 `4.53.0.9` was opened, but
  it restored the prior nine-item / 2790-frame project as unsaved `無題*` state.
  A clean derived-CSV import would require discarding or relocating that existing
  unsaved project. No discard, new project, derived import, save, render, or
  export occurred; YMM4 was left open to preserve the state.

## Product Position

- Profile parsing, strict unmapped-speaker failure, canonical immutability,
  nine-row text/order/character projection, encoding compatibility, and byte
  determinism are machine-checked.
- Import-ready cue-map, adapter plan, manifest, source index, validation, HTML,
  and manual sheet are regenerated under versioned v2 contracts.
- Observation readback supports immutable historical receipt v1, CSV-gate
  receipt v2, and the current tracked GUI-blocker receipt.
- The current CSV gate is not yet passed because the derived CSV was not
  imported. Mapping-dialog absence, 9/9 VoiceItems, automatic characters,
  linked text/order, and timing order remain to be observed once.
- No diagnostic `.ymmp`, ImageItem/TextItem project, render/export, production
  `.ymmp`, real-input replacement, rights/public decision, upload, or
  default-branch integration occurred.

## Current Decision Menu

| Entry | Resolves | What becomes possible |
| --- | --- | --- |
| **Reobserve — recommended** | The already-open YMM4 window holds an existing unsaved recovered project | After the user decides whether to save it elsewhere or discard it, import only the derived CSV in a clean untitled project and record the five CSV-gate checks |
| **Advance** | There is no verified real source/transcript | Validate a supplied receipt and replace the diagnostic sample input without implying CSV-gate completion |
| **Integrate** | Feature-branch work is not reconciled with the default branch | Audit the then-current feature/default diff and choose a safe integration path |

Successful CSV re-observation does not authorize the diagnostic `.ymmp` lane.
That future lane and real-input replacement remain separate supervisor choices.

## Human or External Decision Points

- **Existing unsaved YMM4 project**: in the already-open YMM4 window, first
  decide whether the recovered `無題*` project may be discarded or must be saved
  elsewhere. Do not start a clean import until that decision is explicit.
- **Bounded return path**: after the existing project is resolved, start a clean
  untitled project, import
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/derived_yymm4_import.csv`
  once, record mapping dialog / 9 VoiceItems / characters / linked text and order /
  timing order / CSV responsibility boundary, then close the new observation
  project without saving.
- **Real-input route**: verified source/transcript, provenance/rights note,
  stable identity, and cue alignment are still required before replacement.

## Product Boundaries

- Alias and derived-CSV readiness is machine-proven; actual automatic binding is
  not proven until the bounded GUI import succeeds.
- The diagnostic `.ymmp` project remains `not_authorized / not_attempted`.
- Do not infer render/export, production `.ymmp`, real input, rights/public/final
  thumbnail approval, upload, publication, or default-branch integration.
- Compact state files and task routing remain navigation surfaces, not a
  repository-side session prompt or Worker control plane.

## Maintenance Note

Replace this file as the current capsule. Keep historical decisions in
`docs/project-context.md`, dated verification artifacts, and Git history. Update
`docs/PROJECT_COCKPIT.md` with the same shared fields and run the explicit state
checker when those fields change.
