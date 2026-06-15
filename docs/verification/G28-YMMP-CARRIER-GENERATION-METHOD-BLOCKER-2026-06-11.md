# G-28 YMM4 Carrier Generation Method Blocker - 2026-06-11

This record captures the human review result after
`f37c549 feat: add G-28 map evidence YMM4 probe`.

## Classification

`redesign_required_generation_method_blocker`

## Reviewed Artifact

| Field | Value |
| --- | --- |
| carrier | `samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe.ymmp` |
| readback | `samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe_readback.json` |
| report | `samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe_report.md` |
| builder | `scripts/build_g28_map_evidence_ymmp_probe.js` |
| original creation commit | `f37c549 feat: add G-28 map evidence YMM4 probe` |

## Human Review Result

The Map / Evidence YMM4 diagnostic carrier is not accepted as a diagnostic
candidate. Do not apply `revise_once`.

The review found that the screen does not work as a practical review surface at
first glance. It has too few meaningful display elements for a Map / Evidence
carrier, the evidence and annotation areas are weak, and the overall centering,
spacing regularity, split layout, and eye flow show systematic instability.

The problem is stronger than a single carrier's `layout_system_debt`. It is a
blocker in the visual authoring method: direct script-coordinate `.ymmp`
construction can produce artifacts that satisfy structural checks but still
fail human visual review.

## Readback Boundary

The existing readback pass remains true but narrow. It confirms structural and
safety boundaries only:

- `diagnostic_only=true`
- `production_candidate=false`
- caption reserve clear
- item counts present
- external image / URL / source-footage / audio / TTS counts are zero
- render, production approval, rights approval, and creative final acceptance
  remain false

It does not guarantee that the YMM4 preview is visually useful, balanced,
centered, well-spaced, readable, or strong enough as a carrier review surface.

## Stop Boundary

Do not:

- change the generated `.ymmp`
- change the builder
- regenerate the artifact
- micro-tune this screen
- create another G-28 YMM4 carrier with the same coordinate-generation method
- treat readback pass as visual acceptance
- convert this artifact into a production candidate
- render
- approve rights or creative final acceptance
- introduce external map imagery, screenshots, source footage, audio, or TTS

The existing builder, `.ymmp`, readback, and report remain tracked as negative
evidence / failed sample.

## Safer Next Entries

| Entry | Use when | Next move |
| --- | --- | --- |
| YMM4-native seed or promoted carrier | The next review should start from a YMM4-native surface instead of the rejected coordinate-generation method. | Use an existing YMM4-saved seed, an explicitly promoted diagnostic carrier, or a separately scoped implementation artifact; the assistant audits names, slots, boundaries, and readback. |
| HTML/SVG visual prototype first | The team needs speed without multiplying low-quality `.ymmp` artifacts. | Build a visual prototype, approve composition, then separately plan YMM4 transfer. |
| layout-normalization review | Multiple existing screens need centering / spacing / split-layout diagnosis. | Review screens together and define bounded normalization rules before any further YMM4 generation. |

Speed-first remains useful only when it increases reviewable evidence. Repeating
the same low-quality coordinate-generated carrier pattern is treated as debt
growth, not velocity.
