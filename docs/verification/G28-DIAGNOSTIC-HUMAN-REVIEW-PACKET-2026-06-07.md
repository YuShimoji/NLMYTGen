# G-28 Diagnostic Human Review Packet - 2026-06-07

This packet turns existing G-28 diagnostic artifacts into a human decision
surface. It does not create a new carrier variant, production carrier, render,
`.ymmp`, source intake, rights gate, common foundation implementation, or
creative final acceptance.

Diagnostic acceptance here means only that the visual direction is usable for
the next diagnostic step. It is not production carrier approval, not creative
final acceptance, and not permission to render, publish, automate rights, or use
the artifact in production.

## Artifact Inventory

| artifact_id | artifact | owner files | purpose | readback |
|---|---|---|---|---|
| `g28_lecture_diagram_carrier_skeleton_v1` | Lecture Diagram Carrier generic skeleton | `samples/_probe/g28/lecture_diagram_carrier_skeleton.*` | Proves the generic frame, caption reserve, focal area, callout, host, and layer contract. | passed |
| `g28_lecture_diagram_carrier_real_estate_information_gap_v1` | Lecture Diagram theme variant: `real_estate_information_gap` | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap.*` | Proves an abstract real-estate information-asymmetry mechanism can fit the Lecture Diagram Carrier. | passed |
| `g28_lecture_diagram_carrier_game_mechanics_explanation_v1` | Lecture Diagram theme variant: `game_mechanics_explanation` | `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.*` | Proves a game-mechanics explanation can use the same carrier without source footage. | passed |
| `g28_map_evidence_carrier_skeleton_v1` | Map / Evidence Carrier generic skeleton | `samples/_probe/g28/map_evidence_carrier_skeleton.*` | Proves a single evidence surface with bounded annotations and source note can be diagnostic-only. | passed |
| Source-Footage Carrier | definition only | `docs/verification/G28-CARRIER-ARCHETYPE-TOOLBOX-2026-06-05.md` | Reserved for real gameplay, property, GUI, or source-screen evidence when a later slice explicitly needs footage as the focal surface. | no generator/readback |
| Conversation / Buffer Carrier | definition only | `docs/verification/G28-CARRIER-ARCHETYPE-TOOLBOX-2026-06-05.md` | Reserved for reaction, question, pause, or transition screens. | no generator/readback |

## Readback Summary

Current readback-passing artifacts remain diagnostic-only and
`production_candidate=false`.

| artifact | frame / composition | caption reserve | density guard | safety guard |
|---|---|---|---|---|
| Lecture Diagram generic skeleton | 1920x1080 / 16:9, `center-focal` | bottom 20% clear | 3 callout slots, bounded text, host non-focal | no external image or URL, no `.ymmp` |
| `real_estate_information_gap` | 1920x1080 / 16:9, `center-focal` | bottom 20% clear | 3 focal nodes, 3 callouts, dense table false, indexed whiteboard false | external image count 0, external URL count 0, token-like pattern count 0 |
| `game_mechanics_explanation` | 1920x1080 / 16:9, `center-focal` | bottom 20% clear | 3 focal nodes, 3 callouts, dense table false, indexed whiteboard false | external image count 0, external URL count 0, token-like pattern count 0 |
| Map / Evidence skeleton | 1920x1080 / 16:9, `center-focal` | bottom 20% clear | 3 annotation slots, source note bounded, dense table false, indexed whiteboard false, tiny text false or bounded | external image count 0, external URL count 0, token-like pattern count 0 |

The game-mechanics artifact already has a human `decision=revise` semantics
note: keep the chain direction, but make the middle node concrete enough for
one internal processing example such as `判定 / 当たり判定`.

## Human Visual Review Checklist

Review one artifact at a time.

- Does the focal surface read first without the hosts becoming the subject?
- Does the viewer understand the mechanism or evidence claim before reading
  any caption?
- Is the bottom caption reserve visibly clear?
- Are callouts or annotation slots helpful rather than equal-weight mini-cards?
- Is visible text short enough for a video frame?
- Does the design avoid dense table, indexed whiteboard, timeline strip, and
  decorative-only evidence surfaces?
- Is this only a diagnostic direction, with no production or render authority
  implied?

## Decision Schema

Record one decision per artifact.

```text
artifact_id:
decision: accept_as_diagnostic_direction | revise | reject | defer_to_ymmp_carrier_probe
visual_judgement:
caption_density_note:
boundary_note:
next_requested_action:
```

## Decision Meanings

| decision | meaning | next safe action |
|---|---|---|
| `accept_as_diagnostic_direction` | The diagnostic direction is good enough to use as a future design reference. This is not production acceptance. | Consider a later, explicit YMM4-compatible self-contained carrier probe. Do not render or publish. |
| `revise` | The carrier type remains useful, but semantics, density, labels, hierarchy, or visual focus need correction. | Modify diagnostic JSON/readback/report only, or add a narrow semantics note. |
| `reject` | The artifact fails as a diagnostic direction for the intended shot type. | Record the failure reason and do not promote the artifact. |
| `defer_to_ymmp_carrier_probe` | Static diagnostic readback is insufficient for judgement. | Keep diagnostic-only status and open a later explicit YMM4 carrier probe slice. |

## Boundaries

- Production boundary: no production carrier approval, no production render, no
  publishing, no rights automation, no `production_candidate=true`.
- G-27 boundary: no G-27 revival, blocker restoration, diagnostic carrier
  promotion, or G-27 production slot-fill.
- Common foundation boundary: no Codex Worker Orchestration implementation,
  subprocess runner, real execution loop, stdin execution, or notification
  plumbing.
- YMM4 boundary: no `.ymmp` generation, YMM4 GUI operation, render, or creative
  final acceptance in this packet.
- Source boundary: no external image, URL, raw reference, real map, source
  footage, gameplay capture, or property-specific material intake.
- Upstream boundary: no RSS, OPML, Inoreader, topic clustering, or NotebookLM
  source-pack work.

## Recommended Review Order

1. `g28_lecture_diagram_carrier_real_estate_information_gap_v1`
2. `g28_lecture_diagram_carrier_game_mechanics_explanation_v1`
3. `g28_map_evidence_carrier_skeleton_v1`
4. Generic Lecture Diagram skeleton only if the variants reveal a shared
   carrier-level flaw.
