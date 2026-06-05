# G-28 Shot Carrier Selection - Game Mechanics - 2026-06-05

This artifact applies
`docs/verification/G28-SHOT-CARRIER-SELECTION-WORKSHEET-2026-06-05.md` to one
game-mechanics shot. It records the carrier decision only. It does not add a new
theme variant, carrier skeleton, Source-Footage generator, gameplay screenshot
intake, source footage intake, image path, URL, raw reference, YMM4 project,
render, production timing pass, or creative final acceptance claim.

## Shot Input

| Field | Value |
| --- | --- |
| shot purpose | Explain how hit detection, control feel, and risk/reward relate. |
| source material exists / none | Unknown. Real gameplay footage or screenshots may exist, but this slice does not perform source footage intake. |
| visual evidence type | Mechanism diagram / gameplay. |
| claim type | Cause-effect / misconception correction. |
| required viewer action | Understand how player input, internal rules, and on-screen result connect. |
| caption density | Medium. |
| most important thing to see | The chain from player input to internal judgement to screen result. |
| avoided look | gameplay screenshot overload, source buried under diagram, indexed whiteboard, host-as-proof, subtitle collision. |
| preferred existing artifact | `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.*` |

## Carrier Decision

| Role | Carrier | Decision |
| --- | --- | --- |
| primary carrier | Lecture Diagram Carrier | Use now. |
| backup carrier | Source-Footage Carrier | Future-only backup, not selected for this slice. |

## Decision Reason

The shot asks the viewer to understand a mechanism: player input -> internal
rule/judgement -> screen result, with control feel and risk/reward as supporting
callouts. Source material is unknown and source footage intake is explicitly out
of scope. Under the worksheet tie-breaker, an abstract mechanism with possible
but unused source material routes to Lecture Diagram Carrier rather than
Source-Footage Carrier.

Source-Footage Carrier becomes the better choice only if a later production slice
explicitly provides legitimate source material outside the repo and the gameplay
screen itself must be inspected as evidence. That later route would need a
separate source-safe design checklist or review packet before any production
asset handling.

## Existing Artifact Precedent

| Artifact | Why it applies | Readback state |
| --- | --- | --- |
| `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.json` | Existing diagnostic layout for input -> internal rule -> screen result. | Generated; diagnostic-only. |
| `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_readback.json` | Confirms `variant_id=g28_ldc_game_mechanics_explanation`, `composition_type=center-focal`, 3-node focal chain, 3 callout slots, caption reserve clear. | `status=passed`, `diagnostic_only=true`, `production_candidate=false`. |
| `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.html` | Visualization-only reference for the diagnostic carrier shape. | Not a render or creative acceptance. |
| `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_report.md` | Human-readable report with boundary and failure modes. | Reports no failures, no YMM4 generation, no external image or URL. |

Do not treat this precedent as production readiness. It is a carrier-selection
precedent for this shot shape.

## Next Safe Artifact Or Action

| Next move | Use when | Boundary |
| --- | --- | --- |
| Human review packet for the existing Lecture Diagram diagnostic artifact | A human needs to decide whether the diagram grammar is acceptable for this game-mechanics shot. | No new variant, no `.ymmp`, no render. |
| Scoped YMM4-saved carrier review | A later explicit slice asks to review a saved carrier in YMM4. | Requires explicit human review scope; still not creative final acceptance by default. |
| Source-Footage design-only checklist | The team later decides that real gameplay footage is the proof surface. | Still no footage import, screenshot intake, image path, URL, or raw reference commit in this slice. |

## Still Forbidden Actions

- Do not add another game-mechanics theme variant.
- Do not add a new carrier skeleton.
- Do not create a Source-Footage Carrier generator.
- Do not perform gameplay screenshot intake or source footage intake.
- Do not commit image paths, URLs, raw references, images, or video assets.
- Do not generate `.ymmp`.
- Do not render.
- Do not run production timing or claim creative final acceptance.
- Do not revive G-27 as an active blocker.
- Do not route back into RSS / OPML / Inoreader / NotebookLM work.
- Do not modify existing JSON, HTML, readback JSON, generated reports, or
  generators.

## Return Conditions For Human / GUI / YMM4 Review

| Review path | Return only when | What must be returned |
| --- | --- | --- |
| Human design review | The user wants to judge whether the existing Lecture Diagram carrier communicates the intended input/rule/result relation. | Accept / revise / reject notes for diagram hierarchy, callout meaning, caption clearance, and host non-focal role. |
| GUI review | A later slice exposes this selection inside a review UI or needs a GUI-facing handback. | Exact selected carrier, artifact precedent, and any accepted/revised/cut decision fields. |
| YMM4 review | A later explicit implementation slice asks for YMM4-saved carrier inspection. | Saved carrier path or review packet produced in that later slice; this artifact alone is not enough. |
| Source-Footage review | A later production slice says gameplay footage itself is the evidence surface. | Confirmation that source material exists outside the repo and should remain focal; no source path is required in this artifact. |
