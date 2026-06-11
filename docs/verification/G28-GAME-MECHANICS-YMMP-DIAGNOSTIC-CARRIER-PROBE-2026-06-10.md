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

## One-pass Targeted Layout Fix - 2026-06-11

Human YMM4 visual review found two layout issues while accepting the overall
diagnostic carrier structure:

- `画面上の結果` looked cramped in the right focal node.
- Lower callouts `判定 / 当たり判定` and `リスクとリターン` looked left-aligned.

The fix keeps the same carrier, variant, focal chain, callouts, host role, and
caption reserve. It is not a new variant, redesign, render, production
approval, rights approval, or creative final acceptance.

Implemented one-pass changes:

- `G28_LDC_Node_Right_Label`: removed the inherited rightward nudge and reduced
  font size from 42 to 38 while preserving text `画面上の結果` and the existing
  right-node box.
- `G28_LDC_CalloutSlot_1_Label` / `2_Label` / `3_Label`: applied one shared
  callout label rule with font size 28, zero horizontal offset, and centered
  placement inside the existing callout slots.

Updated readback now records:

- `classification=pass_game_mechanics_ymmp_label_layout_fixed`
- `one_pass_targeted_fix=true`
- `no_further_micro_tuning_recommended=true`
- `next_decision_gate=accept_with_layout_caveat`
- `right_focal_label_fit_status.status=fits_after_one_pass_targeted_fix`
- `callout_label_alignment_status.status=common_centering_rule_applied`
- `label_overflow_check.passed=true`

Readback margins after the fix:

- `画面上の結果`: 16px estimated horizontal margin on each side of the right
  focal node.
- `判定 / 当たり判定`: 29px estimated horizontal margin on each side of its
  callout box.
- `リスクとリターン`: 38px estimated horizontal margin on each side of its
  callout box.

Do not continue same-screen micro-tuning from this record. The two checks below
were the immediate follow-up after the one-pass fix:

- Does `画面上の結果` fit inside the right focal node?
- Do `判定 / 当たり判定` and `リスクとリターン` look centered in their callout boxes?

They are now superseded by the batch visual review protocol in
`docs/verification/G28-GAME-MECHANICS-YMMP-BATCH-VISUAL-REVIEW-PACKET-2026-06-11.md`.
That packet treats these labels as two rows in a full-screen checklist rather
than as a reason to continue single-label pixel tuning. If the human returns
`revise_once`, all `must_fix` items must be handled in one consolidated fix. If
issues remain after that, classify the result as `layout_system_debt` or
`redesign_required`.

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

The next safe slice is human YMM4 batch visual review intake only. The human
should use
`docs/verification/G28-GAME-MECHANICS-YMMP-BATCH-VISUAL-REVIEW-PACKET-2026-06-11.md`
and open:

`samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp`

Return:

- carrier path
- optional preview screenshot
- optional timeline screenshot
- whole-screen batch decision:
  `accept`, `accept_with_caveats`, `revise_once`, `layout_system_debt`, or
  `redesign_required`
- `overall`, `must_fix`, `nice_to_have`, `do_not_fix_now`, and `notes` fields

Still do not render, approve production, approve rights, claim creative final
acceptance, import source footage, import gameplay screenshots, or convert this
diagnostic candidate into production output without a separate explicit slice.
