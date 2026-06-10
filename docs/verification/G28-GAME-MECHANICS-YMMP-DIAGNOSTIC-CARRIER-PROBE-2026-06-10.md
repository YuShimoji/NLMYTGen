# G-28 Game Mechanics YMM4 Diagnostic Carrier Probe - 2026-06-10

This record documents the self-contained YMM4 diagnostic carrier candidate for
the G-28 `game_mechanics_explanation` Lecture Diagram Carrier. It exists because
the prior HTML/readback/report diagnostic precedent was accepted for review
surface usability, but no YMM4-saved carrier evidence was available for the next
human review.

## Generated Artifacts

| Artifact | Path |
| --- | --- |
| builder | `scripts/build_g28_game_mechanics_ymmp_probe.js` |
| YMM4 diagnostic carrier candidate | `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp` |
| readback JSON | `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe_readback.json` |
| human-readable report | `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe_report.md` |

The builder reads the accepted game-mechanics diagnostic JSON/readback and uses
an existing G-28 YMM4 diagnostic probe only as a ShapeItem schema source. It does
not reopen the real-estate review decision or import real-estate evidence.

## Diagnostic Scope

| Field | Value |
| --- | --- |
| source artifact | `g28_lecture_diagram_carrier_game_mechanics_explanation_v1` |
| probe artifact | `g28_lecture_diagram_carrier_game_mechanics_explanation_ymmp_probe_v1` |
| carrier kind | `lecture_diagram_carrier` |
| variant | `game_mechanics_explanation` |
| classification | `pass_game_mechanics_ymmp_diagnostic_carrier_created` |
| diagnostic only | `true` |
| production candidate | `false` |
| render output | `false` |
| production approval | `false` |

## Carrier Contents

| Area | Diagnostic content |
| --- | --- |
| focal chain | `入力操作` -> `内部ルール / 判定` -> `画面上の結果` |
| callouts | `操作感`, `判定 / 当たり判定`, `リスクとリターン` |
| hosts | non-focal lower-corner decoration / emotional anchor |
| caption reserve | bottom reserve remains clear by readback |
| item types | ShapeItem and TextItem only |

The middle node is visible as `内部ルール / 判定` to carry the semantics-note
emphasis into the YMM4 review candidate. This is review text only; it is not
production copy, slot-fill approval, or creative final acceptance.

## Readback Result

`node scripts/build_g28_game_mechanics_ymmp_probe.js --write` produced a passed
readback:

- `diagnostic_only=true`
- `production_candidate=false`
- `carrier_kind=lecture_diagram_carrier`
- `variant=game_mechanics_explanation`
- `focal_chain_count=3`
- `callout_count=3`
- `bottom_caption_reserve_status.clear=true`
- `host_role=non_focal`
- `external_image_count=0`
- `external_url_count=0`
- `source_footage_count=0`
- `audio_item_count=0`
- `tts_or_voice_item_count=0`
- `render_output=false`
- `production_approval=false`
- `failures=[]`

A second no-`--write` run verified the stored `.ymmp` and readback JSON do not
drift from the builder.

## Boundaries

This probe does not:

- approve a production carrier
- approve a render
- approve rights or public-use status
- claim creative final acceptance
- ingest source footage
- ingest gameplay screenshots
- introduce external images, URLs, or raw references
- create audio, TTS, or voice items
- resume real-estate work
- process Newsroom handoff material
- revive G-27
- continue common-foundation dry-run preview work

## Next Human Review Inputs

The next safe slice is human YMM4 review intake only. The human should open:

`samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp`

Return:

- carrier path
- preview screenshot
- timeline screenshot
- item/layer confirmation for title, focal chain, callouts, hosts, and caption reserve
- bottom caption safe-area evidence
- decision: `accept`, `revise`, or `reject`

Still do not render, approve production, approve rights, claim creative final
acceptance, import source footage, import gameplay screenshots, or convert this
diagnostic candidate into production output without a separate explicit slice.
