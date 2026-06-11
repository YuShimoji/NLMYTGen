# G-28 Map / Evidence YMM4 Diagnostic Carrier Probe - 2026-06-11

This record documents the next speed-first G-28 reviewable artifact after the
`game_mechanics_explanation` YMM4 diagnostic carrier was classified as
`layout_system_debt`. It does not tune the game-mechanics screen. It converts
the existing Map / Evidence diagnostic skeleton into a self-contained YMM4
diagnostic carrier candidate for human review.

## Source Decision

`67bee50 docs: record G-28 game mechanics layout debt` records that the current
game-mechanics screen remains reviewable but should not receive more same-screen
pixel / label micro-tuning. The next safe direction is speed-first: add another
reviewable G-28 artifact and revisit centering / spacing / split-layout debt in
a later cross-screen layout-normalization slice.

## Generated Artifacts

| Artifact | Path |
| --- | --- |
| builder | `scripts/build_g28_map_evidence_ymmp_probe.js` |
| YMM4 diagnostic carrier candidate | `samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe.ymmp` |
| readback JSON | `samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe_readback.json` |
| human-readable report | `samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe_report.md` |

The builder reads the existing passed Map / Evidence skeleton:

- `samples/_probe/g28/map_evidence_carrier_skeleton.json`
- `samples/_probe/g28/map_evidence_carrier_skeleton_readback.json`

It uses the existing game-mechanics YMM4 diagnostic probe only as a ShapeItem
schema source. It does not import game-mechanics layout values, does not modify
that carrier, and does not resume game-mechanics micro-tuning.

## Diagnostic Scope

| Field | Value |
| --- | --- |
| source artifact | `g28_map_evidence_carrier_skeleton_v1` |
| probe artifact | `g28_map_evidence_carrier_ymmp_probe_v1` |
| carrier kind | `map_evidence_carrier` |
| variant | `map_evidence` |
| classification | `pass_map_evidence_ymmp_diagnostic_carrier_created` |
| diagnostic only | `true` |
| production candidate | `false` |
| render output | `false` |
| production approval | `false` |
| creative final acceptance | `false` |
| rights approval | `false` |

## Carrier Contents

| Area | Diagnostic content |
| --- | --- |
| evidence surface | abstract focal surface, not a real map or image asset |
| annotation slots | three empty placeholder slots |
| source note | bounded text `出典確認済み` |
| hosts | non-focal lower-corner decoration / emotional anchor |
| caption reserve | bottom reserve remains clear by readback |
| item types | ShapeItem and TextItem only |

The evidence surface and annotation slots prove the Map / Evidence carrier shape
can be opened for YMM4 review without introducing external map imagery, source
URLs, raw references, or production slot-fill.

## Readback Result

`node scripts/build_g28_map_evidence_ymmp_probe.js --write` produced a passed
readback, and a second no-`--write` run verified that the stored `.ymmp` and
readback do not drift from the builder.

Readback highlights:

- `diagnostic_only=true`
- `production_candidate=false`
- `carrier_kind=map_evidence_carrier`
- `variant=map_evidence`
- `classification=pass_map_evidence_ymmp_diagnostic_carrier_created`
- `self_contained_ymmp_probe_created=true`
- `frame_16_9_1920_1080=true`
- `caption_reserve_clear=true`
- `evidence_area_in_main_canvas=true`
- `annotation_slot_count_2_to_4=true`
- `source_note_text_budget_bounded=true`
- `host_role_non_focal=true`
- `shape_item_count_expected=true`
- `text_item_count_expected=true`
- `external_image_count_zero=true`
- `external_url_count_zero=true`
- `source_footage_count_zero=true`
- `audio_item_count_zero=true`
- `tts_or_voice_item_count_zero=true`
- `render_output_false=true`
- `production_approval_false=true`
- `creative_final_acceptance_false=true`
- `rights_approval_false=true`
- `token_like_pattern_count_zero=true`
- `carrier_not_modified_in_place=true`
- `failures=[]`

## Boundaries

This probe does not:

- modify the game-mechanics carrier
- continue same-screen micro-tuning
- approve a production carrier
- approve a render
- approve rights or public-use status
- claim creative final acceptance
- ingest real map or satellite imagery
- ingest source footage
- introduce external images, URLs, raw references, audio, TTS, or voice items
- process Newsroom handoff material
- revive G-27
- touch ClipPipeGen, RSS, OPML, Inoreader, or NotebookLM
- touch GUI / `src`
- continue common foundation or real runner / `codex exec` work

## Next Human Review Inputs

The next safe slice is human YMM4 review intake only. The human should open:

`samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe.ymmp`

Return:

- carrier path
- preview screenshot
- timeline screenshot
- item/layer confirmation for evidence surface, annotation slots, source note,
  hosts, and caption reserve
- caption reserve visual confirmation
- decision: `accept`, `accept_with_caveats`, `revise_once`,
  `layout_system_debt`, or `redesign_required`

Still do not render, approve production, approve rights, claim creative final
acceptance, import source footage, import real map imagery, or convert this
diagnostic candidate into production output without a separate explicit slice.
