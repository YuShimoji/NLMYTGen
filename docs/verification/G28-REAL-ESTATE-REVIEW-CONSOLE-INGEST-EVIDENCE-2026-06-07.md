# G-28 Real Estate Review Console Ingest Evidence - 2026-06-07

This records the evidence-only confirmation slice for the G-28
`real_estate_information_gap` Review Console read-only ingest panel.

## Classification

- classification: `pass_dom_evidence_needs_manual_screenshot`
- reason: Existing Electron DOM smoke confirmed that the read-only G-28 Review
  Console panel is visible and contains the required diagnostic contents. No
  G-28-specific screenshot capture command exists in the current GUI scripts, so
  no new screenshot tooling was added.
- evidence date: 2026-06-08 JST
- branch / HEAD at capture: `master` / `2724f44`
- upstream alignment at capture: `HEAD...@{u}=0 0`

## Scope

- target panel: `#g28-review-console-ingest`
- target variant: `g28_ldc_real_estate_information_gap`
- target probe:
  `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.ymmp`
- readback:
  `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_readback.json`
- report:
  `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_report.md`
- ingest plan:
  `docs/verification/G28-REAL-ESTATE-REVIEW-CONSOLE-INGEST-PLAN-2026-06-07.md`

This slice did not modify Review Console implementation files, generated probe
artifacts, builders, readback JSON, report Markdown, or any production/render/
rights approval path.

## Readback Inspection

The readback JSON was inspected without rewriting it.

| field | observed |
| --- | --- |
| `status` | `passed` |
| `classification` | `pass_callout_label_human_calibrated` |
| `variant_id` | `g28_ldc_real_estate_information_gap` |
| `boundary.diagnostic_only` | `true` |
| `boundary.production_candidate` | `false` |
| `checks.caption_reserve_clear` | `true` |
| focal chain count | `3` |
| `totals.callout_count` | `3` |
| `host_role_readback.role` | `non_focal_lower_corner_decoration_emotional_anchor` |
| `safety_readback.external_image_count` | `0` |
| `safety_readback.external_url_count` | `0` |
| `safety_readback.source_footage_count` | `0` |
| `safety_readback.audio_item_count` | `0` |
| `safety_readback.tts_or_voice_item_count` | `0` |
| `checks.render_output_false` | `true` |
| calibrated callout `actual_x` | `313` |
| `human_calibrated_override` | `true` |

## Electron DOM Smoke

Command:

```powershell
.\gui\node_modules\.bin\electron.cmd .\gui\review_console_dom_smoke.js
```

Result:

```text
G-27 review console DOM smoke OK: 11 timeline segments; 9 G-27 proof frames; 3 pipeline smoke topics / 9 smoke beats visible through GUI; G-28 diagnostic ingest panel visible; save payload OK
```

The existing smoke asserts that the Review Console contains:

- the `G-28 real_estate_information_gap YMM4 diagnostic probe` panel
- five artifact inventory rows
- status badges for `diagnostic_only=true`, `production_candidate=false`,
  `human_calibrated_override=true`, `layout_metric_debt=true`,
  `host_placeholder=true`, `render=false`, and `rights_public_use=false`
- readback summary including `pass_callout_label_human_calibrated`,
  `caption_reserve_clear`, focal chain count, callout count, host role, zero
  external/source/audio/TTS/render counts, and `actual_x=313`
- human GUI summary including `openability`,
  `callout_label_alignment_仲介インセンティブ`, `title_position`,
  `host_placeholders`, and
  `accept_for_review_console_ingest_candidate_with_layout_metric_caveat`
- caveats for the human-calibrated X value, title `y=-474.5` metric debt,
  diagnostic-only host placeholders, and glyph optical center not being directly
  measured
- only these diagnostic decisions:
  `accept_as_diagnostic_review_surface`, `request_readback_fix`,
  `request_layout_system_redesign`, `defer_review_console_ingest`, and
  `reject_probe_path`
- absence of forbidden production labels:
  `production_approve`, `creative_final_acceptance`, `render_approve`,
  `rights_approve`, and `public_use_approve`

## Screenshot Status

- screenshot: not captured
- reason: existing GUI capture scripts target G-27 overlay/storyboard/treatment
  or pipeline smoke panels. None targets `#g28-review-console-ingest`.
- boundary decision: no new capture script or GUI implementation was added in
  this evidence-only slice.
- next manual option: open the Electron Review Console and visually confirm the
  G-28 panel, badges, caveats, and diagnostic decision schema only.

## Boundary Check

- Review Console implementation changed: no
- GUI files changed: no
- `.ymmp` changed: no
- builder changed: no
- readback changed: no
- report changed: no
- new variant generated: no
- render / MP4: no
- production carrier approval: no
- creative final acceptance: no
- rights / production automation: no
- G-27 authority reuse: no
- source footage / audio / TTS: no
- ClipPipeGen access: no
- common foundation work: no
- known local residues touched: no

## Next Safe Action

If a visual artifact is still required, collect a manual Review Console
screenshot or add an explicitly authorized G-28-specific capture slice. The next
decision must stay limited to the read-only diagnostic review surface and must
not approve production, render, rights/public use, source footage, or creative
final acceptance.
