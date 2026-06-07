# G-28 Real Estate Review Console Ingest Plan - 2026-06-07

This plan defines a read-only Review Console ingest path for the G-28
`real_estate_information_gap` YMM4 diagnostic probe. It is a planning artifact
only. It does not implement GUI ingest, change the GUI, regenerate `.ymmp`,
rewrite readback, approve production, approve render, approve rights, or perform
creative final acceptance.

## Classification

- classification: `pass_review_console_ingest_plan_created`
- artifact scope: docs-only ingest plan
- target probe: `g28_lecture_diagram_carrier_real_estate_information_gap_ymmp_probe_v1`
- target variant: `g28_ldc_real_estate_information_gap`
- input status: `pass_callout_label_human_calibrated`
- human status: `accept_for_review_console_ingest_candidate_with_layout_metric_caveat`
- implementation status: not started

## Ingest Objective

The Review Console should be able to display and inspect the G-28 real-estate
YMM4 diagnostic probe as a read-only review surface. The console should make the
probe's diagnostic boundary obvious, show the machine readback summary, surface
the human GUI recheck result, and expose the layout metric caveats that must not
be mistaken for production approval.

The ingest is not:

- production carrier approval
- creative final acceptance
- render approval
- public-use or rights approval
- MP4/publish work
- material slot-fill

## Input Artifact Inventory

The implementation slice should reference the existing paths in place and must
not copy, convert, or regenerate them.

| input | path | role |
| --- | --- | --- |
| YMM4 diagnostic probe | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.ymmp` | YMM4-openable diagnostic probe |
| readback JSON | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_readback.json` | machine status, boundary, safety, layout metrics |
| report MD | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_report.md` | human-readable probe report |
| human review record | `docs/verification/G28-REAL-ESTATE-YMMP-PROBE-HUMAN-REVIEW-2026-06-07.md` | GUI review and X=313 recheck decisions |
| diagnostic decision record | `docs/verification/G28-DIAGNOSTIC-HUMAN-DECISION-RECORD-2026-06-07.md` | wider G-28 diagnostic decision context |
| layout audit | `docs/verification/G28-REAL-ESTATE-YMMP-PROBE-LAYOUT-CONTRACT-AUDIT-2026-06-07.md` | layout contract and debt context |
| YMM4-compatible probe plan | `docs/verification/G28-REAL-ESTATE-YMM4-COMPATIBLE-PROBE-PLAN-2026-06-07.md` | original probe plan context |
| runtime state | `docs/runtime-state.md` | current restart state |
| project context | `docs/project-context.md` | decision log |

## Review Console Display Requirements

The Review Console should show the artifact title:

`G-28 real_estate_information_gap YMM4 diagnostic probe`

The page or panel should be read-only by default. It may expose allowed review
decisions later, but the first implementation should not offer production,
render, rights, or creative approval controls.

Required status badges:

- `diagnostic_only=true`
- `production_candidate=false`
- `human_calibrated_override=true`
- `layout_metric_debt=true`
- `host_placeholder=true`
- `render=false`
- `rights_public_use=false`

Required sections:

- input artifact inventory
- readback summary
- human GUI result summary
- layout metric caveats
- title readback follow-up requirements
- host placeholder boundary
- allowed diagnostic decision schema
- explicit non-goals

## Readback Summary

The implementation should load the readback JSON and display these fields:

| field | expected value |
| --- | --- |
| `classification` | `pass_callout_label_human_calibrated` |
| `diagnostic_only` | `true` |
| `production_candidate` | `false` |
| `caption_reserve_clear` | `true` |
| `focal_chain_count` | `3` |
| `callout_count` | `3` |
| `host_role` | `non_focal_lower_corner_decoration_emotional_anchor` |
| `external_image_count` | `0` |
| `external_url_count` | `0` |
| `source_footage_count` | `0` |
| `audio_count` | `0` |
| `tts_count` | `0` |
| `render_output_count` | `0` |
| `human_calibrated_override` | `true` |
| `human_calibrated_callout_x` | `313` |

The console should block or clearly fail the panel if the readback status is not
`passed`, if `production_candidate` is true, if external image/URL/source
footage/audio/TTS counts are nonzero, or if render output is detected.

## Human GUI Result Summary

The Review Console should display this human review status:

| field | recorded value |
| --- | --- |
| `openability` | `pass` |
| `callout_label_alignment_仲介インセンティブ` | `pass` |
| `title_position` | `pass_with_metric_caveat` |
| `host_placeholders` | `pass_as_diagnostic_placeholder` |
| `focal_chain_readability` | `pass` |
| `connector_treatment` | `pass` |
| `other_callout_side_effect` | `none` |
| `right_node_side_effect` | `none` |
| `caption_reserve` | `pass` |
| `diagnostic_boundary` | `clear` |
| `overall_decision` | `accept_for_review_console_ingest_candidate_with_layout_metric_caveat` |
| `production_boundary_acknowledged` | `true` |

## Title Readback Requirements

The human GUI recheck says the title is visually acceptable and reports
`title y=-474.5`. The current machine readback records the title TextItem as a
different coordinate form, so the next implementation should not treat title
position as a manual-fix target. Instead, it should add explicit title readback
fields in the G-28 Review Console panel and later builder/readback work:

- `title_anchor_y`
- `title_text_center_y`
- `title_band_center_y`
- `title_safe_area`
- `title_visual_offset_y`
- `title_within_title_band`

The console should display title status as `pass_with_metric_caveat` until those
fields exist.

## Host Placeholder Boundary

The lower-corner host shapes are diagnostic placeholders. They are useful for
checking non-focal emotional-anchor placement in the diagnostic probe, but they
are not production host visuals.

The Review Console should show a `host_placeholder=true` badge or warning. A
future production or material slice must decide one of:

- replace with approved character visuals
- replace with an approved non-character representation
- hide the host layer for this carrier
- keep a host only after explicit production visual approval

The console must not present these placeholders as public-use assets or as
accepted production character material.

## Human-Calibrated Callout Caveat

The `仲介インセンティブ` callout X value `313` is a human-calibrated override. It
is not proof that the callout text placement formula is reusable.

The Review Console should show:

- `human_calibrated_override=true`
- `layout_metric_debt=true`
- computed X before human calibration: `289`
- human-calibrated X: `313`
- calibration delta X: `24`
- reuse risk: do not generalize this X value to other labels, themes, fonts, or
  callout counts

The console should not invite more pixel tuning. If similar label issues recur,
the next structural path is callout text layout system redesign.

## Decision Schema

Review Console decisions for this G-28 diagnostic probe are limited to:

- `accept_as_diagnostic_review_surface`
- `request_readback_fix`
- `request_layout_system_redesign`
- `defer_review_console_ingest`
- `reject_probe_path`

Forbidden decisions:

- `production_approve`
- `creative_final_acceptance`
- `render_approve`
- `rights_approve`
- `public_use_approve`

If decision saving is implemented later, it should use a G-28-specific decision
artifact and must not write into the G-27 `review_decisions` path.

## Future Implementation Plan

The next slice may implement read-only GUI ingest if explicitly authorized. It
should be narrow and should reference existing artifacts rather than copying
them.

Candidate implementation surfaces:

- `gui/index.html`: add or reserve a G-28 read-only panel inside the existing
  design review tab
- `gui/renderer.js`: load the G-28 readback/human-review metadata and render
  status badges, readback summary, caveats, and allowed diagnostic decisions
- `gui/style.css`: add compact badge/warning styles if existing styles are not
  sufficient
- `gui/review_console_dom_smoke.js`: add DOM assertions for the G-28 panel
- `gui/capture_pipeline_smoke_review_screenshot.js`: use as a reference pattern
  for an optional later Electron screenshot smoke, without reusing its pipeline
  smoke semantics

Connection rules:

- keep the G-28 panel separate from G-27 segment timeline state
- do not reuse G-27 `review_packet` or `review_decisions` as the G-28 authority
- do not copy the YMM4 probe or readback into a new artifact
- load existing repo-relative paths read-only
- make missing artifact/readback states visible as blocked diagnostics

Error display rules:

- missing `.ymmp`: block panel as `blocked_missing_ymmp`
- missing readback: block panel as `blocked_missing_readback`
- readback not passed: block panel as `blocked_readback_failed`
- `production_candidate=true`: block panel as `blocked_production_boundary`
- external assets detected: block panel as `blocked_external_asset_detected`
- render output detected: block panel as `blocked_render_boundary`
- human review missing: show `needs_human_recheck_clarification`

## Next Implementation Acceptance Criteria

A later read-only implementation slice is acceptable only if:

- Review Console displays the G-28 probe artifact inventory
- readback summary is visible
- `diagnostic_only=true` and `production_candidate=false` are prominent
- host placeholder warning is visible
- title caveat is visible
- human-calibrated override and layout metric debt are visible
- no production, render, rights, public-use, or creative approval control is
  exposed
- DOM smoke verifies the panel and badges
- Electron smoke or screenshot capture can prove the panel is visible if the
  implementation changes the GUI surface
- no `.ymmp`, builder, readback JSON, probe report, render output, external
  material, G-27 artifact, ClipPipeGen artifact, RSS/NotebookLM work, or common
  foundation implementation is added

## Explicit Non-Goals

- actual Review Console ingest implementation in this slice
- GUI code modification in this slice
- `.ymmp` regeneration
- builder or generator change
- readback JSON rewrite
- probe report rewrite
- new variant generation
- render, MP4, or publishing output
- production carrier approval
- creative final acceptance
- rights automation
- source footage, audio, or TTS intake
- external image, URL, or raw reference intake
- G-27 revival or G-27 artifact modification
- ClipPipeGen work
- RSS, OPML, Inoreader, or NotebookLM source-pack work
- common foundation or Codex Worker Orchestration implementation

## Plan Slice Verification

This plan can be considered complete when:

- the file exists as a docs-only artifact
- `docs/runtime-state.md` and `docs/project-context.md` point to this plan as
  the next implementation guide
- existing G-28 readback remains unchanged and passed
- no `.ymmp`, builder, readback JSON, report MD, or GUI implementation file is
  changed in this slice
- staged scope is limited to this plan and minimal state/context docs
