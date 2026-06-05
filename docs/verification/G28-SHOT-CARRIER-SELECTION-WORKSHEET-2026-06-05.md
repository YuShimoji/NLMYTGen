# G-28 Shot Carrier Selection Worksheet - 2026-06-05

This worksheet turns `docs/verification/G28-CARRIER-ARCHETYPE-TOOLBOX-2026-06-05.md`
into a per-shot decision aid. It is a blank template plus carrier routing rules;
it does not create a new theme variant, carrier skeleton, source intake, YMM4
project, render, production timing pass, or creative final acceptance claim.

## Shot Input

Fill this before choosing a carrier. Leave unknown fields blank rather than
inventing evidence.

| Field | Fill here | Allowed / useful values |
| --- | --- | --- |
| shot purpose |  | explain mechanism / prove evidence / show source / reaction / pause / transition |
| source material exists / none |  | none / exists outside repo / unknown |
| visual evidence type |  | mechanism diagram / geography-statistics / cited evidence / gameplay / property / GUI / source screen / dialogue-board / none |
| claim type |  | cause-effect / misconception correction / location or numeric comparison / source-screen observation / viewer question / transition |
| required viewer action |  | understand relation / trust evidence / inspect source / feel reaction / reset attention / choose next topic |
| caption density |  | low / medium / high / unknown |
| most important thing to see |  | one diagram / one evidence surface / one source screen / host-board beat |
| avoided look |  | indexed whiteboard / map-as-wallpaper / source buried under diagram / host-as-proof / subtitle collision |

## Carrier Decision Rules

Use the first matching rule that describes what the viewer must see.

| If the shot is mainly... | Choose | Why this wins |
| --- | --- | --- |
| mechanism, cause-effect, before/after, misconception correction | Lecture Diagram Carrier | The existing G-28 Lecture artifacts are built around one focal diagram or a short node chain. |
| geography, statistics, location logic, cited evidence, regional comparison | Map / Evidence Carrier | The existing Map / Evidence skeleton keeps one evidence surface focal with bounded annotations and source note. |
| gameplay, property footage, GUI operation, or a source screen that already carries proof | Source-Footage Carrier | The source surface should stay focal; only top chapter, border, marker, or subtitle-safe emphasis should be added later. |
| reaction, question, pause, transition, or low-density bridge between heavier evidence shots | Conversation / Buffer Carrier | The shot is a pacing or dialogue tool, not a proof surface. |

Tie-breakers:

| Conflict | Resolve by asking | Default |
| --- | --- | --- |
| Source material exists, but the claim is abstract | Does the source screen prove the point by inspection? | If yes, Source-Footage. If no, Lecture Diagram. |
| Map/stat evidence plus a causal explanation | Is the main visual proof a place/data surface or a mechanism? | Evidence surface -> Map / Evidence. Mechanism -> Lecture Diagram. |
| Conversation line includes a factual claim | Does the claim need proof on screen? | If yes, route to Map / Evidence, Source-Footage, or Lecture before using Conversation. |
| Caption density is high | Can the carrier keep the bottom reserve clear and reduce in-frame labels? | Prefer the carrier with fewer patch labels; otherwise split the shot. |

## Existing Artifact Connection

| Selected carrier | Reuse as decision precedent | Use when | Do not claim |
| --- | --- | --- | --- |
| Lecture Diagram Carrier | `samples/_probe/g28/lecture_diagram_carrier_skeleton.*` | The shot is a generic mechanism or cause-effect explanation. | production readiness, slot-fill approval, render readiness |
| Lecture Diagram Carrier | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap.*` | The shot explains gated information, portal/listing asymmetry, or decision flow without using source footage. | G-27 revival, production carrier approval |
| Lecture Diagram Carrier | `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.*` | The shot explains input -> internal rule -> screen result without importing gameplay footage. | Source-Footage promotion, gameplay screenshot intake |
| Map / Evidence Carrier | `samples/_probe/g28/map_evidence_carrier_skeleton.*` | The shot needs one abstract map/evidence surface, 2-4 annotations, and a bounded source note. | real map/satellite/image asset use, cited-body import, production approval |
| Source-Footage Carrier | No generated artifact yet; definition exists only in the toolbox/style brief. | A real source screen exists outside this slice and should remain focal. | source footage intake, image path/URL commit, skeleton existence |
| Conversation / Buffer Carrier | No generated artifact yet; definition exists only in the toolbox/style brief. | The shot is a dialogue, reaction, question, pause, or transition beat. | proof-heavy evidence, board/table overload, skeleton existence |

## Conditions For Unstarted Archetypes

| Archetype | Proceed only when | First safe next artifact | Still forbidden in this slice |
| --- | --- | --- | --- |
| Source-Footage Carrier | A concrete production shot has source material outside the repo, and the source screen itself is the focal evidence. | Design-only checklist/readback spec for frame, HUD protection, chapter label, marker, and caption reserve. | source footage import, gameplay screenshot intake, image path/URL/raw reference commit, `.ymmp`, render |
| Conversation / Buffer Carrier | A concrete production shot needs pacing, reaction, question, or transition rather than proof-heavy evidence. | Design-only checklist/readback spec for board density, host balance, mediator role, and caption reserve. | using hosts as proof, creating evidence claims without evidence, new skeleton by default |

## Human Return Packet

When asking for a carrier decision, return this minimal packet:

```text
shot purpose:
source material exists / none:
visual evidence type:
claim type:
required viewer action:
caption density:
most important thing to see:
avoided look:
preferred existing artifact, if any:
```

The assistant should answer with one carrier, one backup carrier only if the
decision is genuinely tied, the existing artifact precedent if available, and the
next safe artifact/action. It should not ask for source files, image paths, URLs,
or production assets unless the user explicitly opens a separate production
intake slice.

## Hard Stops

- Do not create a new Lecture Diagram theme variant by default.
- Do not create a new carrier skeleton from this worksheet.
- Do not commit images, URLs, raw references, source footage, gameplay
  screenshots, or image paths.
- Do not generate `.ymmp`, render, production timing, or creative final
  acceptance artifacts.
- Do not revive G-27 as an active blocker.
- Do not route back into RSS / OPML / Inoreader / NotebookLM work.
- Do not modify existing JSON, HTML, readback JSON, generated reports, or
  generators for this worksheet-only slice.
