# G-28 Carrier Archetype Toolbox - 2026-06-05

This artifact consolidates the G-28 Reference-Driven Generic Screen Carrier
archetypes into a selection tool. It does not add a new skeleton, theme variant,
source intake, YMM4 project, render, production timing pass, or creative final
acceptance claim.

The current state is intentionally diagnostic. G-28 is not production-complete:
the existing Lecture Diagram and Map / Evidence artifacts prove bounded screen
contracts, while Source-Footage and Conversation / Buffer remain unimplemented
archetype definitions from the reference style brief.

## Selection Rule

Choose the carrier by the strongest visual evidence available for the shot:

| Visual evidence in the next shot | Use this carrier first | Reason |
| --- | --- | --- |
| A mechanism, cause/effect relation, or misconception must be explained without a strong source image | Lecture Diagram Carrier | It gives one focal diagram, a short title, and a few supporting callouts without turning into an indexed whiteboard. |
| Geography, statistics, location logic, or cited evidence must be shown as the argument surface | Map / Evidence Carrier | It keeps one pre-authored evidence surface focal and limits annotations/source notes. |
| A gameplay, property, GUI, or other source screen is already the proof | Source-Footage Carrier | It should preserve the source surface and add only chapter, border, marker, or subtitle-safe emphasis. |
| The video needs a reaction, question, pause, transition, or low-density bridge between evidence shots | Conversation / Buffer Carrier | It keeps hosts/board useful without pretending to be proof-heavy evidence. |

## Archetype Comparison

| Archetype | Purpose | Fits | Does not fit | Current artifact | Readback state |
| --- | --- | --- | --- | --- | --- |
| Lecture Diagram Carrier | Explain an abstract mechanism through one focal diagram or a short node chain. | Science, market mechanisms, AI mechanisms, before/after logic, real-estate information-gate logic, game mechanics when no source footage is being used. | Dense source footage, long tables, map-heavy evidence, proof that depends on real footage or real map detail. | Spec: `docs/verification/G28-LECTURE-DIAGRAM-CARRIER-SPEC-2026-06-05.md`.<br>Generator: `scripts/build_g28_lecture_diagram_carrier_skeleton.js`.<br>Generic: `samples/_probe/g28/lecture_diagram_carrier_skeleton.*`.<br>Variants: `lecture_diagram_carrier_real_estate_information_gap.*`, `lecture_diagram_carrier_game_mechanics_explanation.*`. | Passed for generic skeleton and both theme variants. All are `diagnostic_only=true`, `production_candidate=false`, no YMM4 generation, no external image or URL. |
| Map / Evidence Carrier | Show a map-like, statistical, regional, or cited evidence surface as the focal argument. | Geography, population, industrial clusters, logistics, access/area logic, company-location relation, bounded citation/evidence explanation. | Emotional dialogue, detailed step mechanism, live source footage, real map/satellite intake in this repo. | Spec: `docs/verification/G28-MAP-EVIDENCE-CARRIER-SPEC-2026-06-05.md`.<br>Generator: `scripts/build_g28_map_evidence_carrier_skeleton.js`.<br>Generic: `samples/_probe/g28/map_evidence_carrier_skeleton.*`. | Passed for diagnostic skeleton. Readback reports `composition_type=center-focal`, 3 annotation slots, bounded source note, caption reserve clear, `dense_table=false`, `indexed_whiteboard=false`, `tiny_text=false`, no external image or URL. |
| Source-Footage Carrier | Let a source screen carry credibility while adding only minimal structure around it. | Game review footage, UI walkthrough, property tour, source-screen comparison, video commentary where the source surface is already the evidence. | Abstract mechanism without visual source, map/stat evidence, conversation-only pauses, any shot that would bury the source under a new diagram. | Definition only in `docs/verification/G28-REFERENCE-STYLE-BRIEF-2026-06-05.md`. No generator, JSON, HTML, report, or readback exists under `samples/_probe/g28/`. | Not started. No readback has been generated. Treat as an unimplemented archetype, not a failed artifact. |
| Conversation / Buffer Carrier | Provide a low-density board/host surface for reactions, questions, bridges, or short explanation pauses. | Trivia conversation, audience questions, chapter transitions, buffer shots between dense evidence, light narration moments. | Proof-heavy claims, numerical comparison, detailed map/stat evidence, source footage that should remain focal. | Definition only in `docs/verification/G28-REFERENCE-STYLE-BRIEF-2026-06-05.md`. No generator, JSON, HTML, report, or readback exists under `samples/_probe/g28/`. | Not started. No readback has been generated. Treat as an unimplemented archetype, not a failed artifact. |

## Production Gate Questions

| Archetype | Human judgement needed before production | If this is reopened, build next | Do not proceed into |
| --- | --- | --- | --- |
| Lecture Diagram Carrier | Confirm that the target shot is mechanism-first, not source-first; confirm the 2-3 node diagram is enough; confirm hosts stay secondary and caption area remains clear in the actual YMM4 view. | A human review packet for one existing diagnostic artifact, or a scoped YMM4-saved carrier review if explicitly requested. New theme variants are not the default next move. | More theme variants by habit, G-27 promotion, slot-fill as production approval, `.ymmp` generation without a scoped review, render, final creative acceptance. |
| Map / Evidence Carrier | Confirm the evidence surface can be human-authored without committing real map/satellite/image paths; confirm the claim belongs on a bounded evidence surface rather than a mechanism diagram; confirm source note density is acceptable. | A human review packet for the abstract evidence surface, or a checklist for authoring a real production evidence surface outside this diagnostic repo artifact. | Real map or satellite assets, image path/URL/raw reference intake, dense citation body text, turning the map surface into decoration, render or final acceptance. |
| Source-Footage Carrier | Confirm there is legitimate source footage/screenshot material available outside this slice, and that the source surface should remain the focal object rather than be translated into a diagram. | A design-only checklist/readback spec for source-safe framing, HUD protection, top chapter label, border, and small emphasis marker. | Gameplay screenshot intake, source footage import, image path or URL recording, repository storage of raw source material, production render, YMM4 generation in this slice. |
| Conversation / Buffer Carrier | Confirm the shot is a breathing-space or dialogue moment, not evidence proof; confirm board text stays minimal; confirm hosts support the topic instead of becoming the argument. | A design-only checklist/readback spec for board density, mediator/host balance, caption reserve, and transition use. | Using it to prove statistics, replacing evidence with host banter, indexed whiteboard overload, creating a carrier skeleton before the production need is selected. |

## Current Inventory Boundaries

- Existing generated artifacts are kept as-is. This slice does not modify JSON,
  HTML, readback JSON, generated reports, or scripts.
- Lecture Diagram Carrier and Map / Evidence Carrier are diagnostic-only screen
  contracts. They are useful for deciding screen grammar, not for claiming
  production readiness.
- Source-Footage Carrier and Conversation / Buffer Carrier are still only
  archetype definitions from the reference style brief. Their next useful move is
  a bounded checklist or readback spec after a human chooses a production need.
- No real map, satellite image, source footage, gameplay screenshot, image path,
  external URL, raw reference, RSS/OPML/NotebookLM source work, render, production
  timing pass, creative final acceptance, or G-27 active blocker work belongs to
  this artifact.
