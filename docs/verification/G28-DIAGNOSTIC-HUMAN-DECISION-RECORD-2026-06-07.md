# G-28 Diagnostic Human Decision Record - 2026-06-07

This record captures the supplied human decisions on existing G-28 diagnostic
artifacts. These decisions are diagnostic-review decisions only; no production
carrier approval or creative final acceptance is granted here.

Diagnostic acceptance, when later supplied by a human, means only that a
diagnostic direction is acceptable. It is not production carrier approval,
creative final acceptance, render approval, rights approval, publishing approval,
or permission to set `production_candidate=true`.

## Artifact Inventory

| artifact_id | artifact | readback | diagnostic_only | production_candidate | decision_status |
|---|---|---:|---:|---:|---|
| `g28_lecture_diagram_carrier_skeleton_v1` | Generic Lecture Diagram skeleton | passed | true | false | accept_as_diagnostic_direction |
| `g28_lecture_diagram_carrier_real_estate_information_gap_v1` | Lecture Diagram `real_estate_information_gap` variant | passed | true | false | accept_as_diagnostic_direction |
| `g28_lecture_diagram_carrier_game_mechanics_explanation_v1` | Lecture Diagram `game_mechanics_explanation` variant | passed | true | false | revise |
| `g28_map_evidence_carrier_skeleton_v1` | Map / Evidence Carrier skeleton | passed | true | false | defer_to_ymmp_carrier_probe |
| `g28_source_footage_carrier_definition_only` | Source-Footage Carrier definition | no generator/readback | n/a | false | defer_to_ymmp_carrier_probe |
| `g28_conversation_buffer_carrier_definition_only` | Conversation / Buffer Carrier definition | no generator/readback | n/a | false | defer_to_ymmp_carrier_probe |

## Allowed Decisions

| decision | meaning | next safe action |
|---|---|---|
| `accept_as_diagnostic_direction` | Human accepts the diagnostic direction only. This is not production approval. | Use as a future design reference; a YMM4-compatible probe requires a separate explicit slice. |
| `revise` | Human requests a bounded diagnostic correction. | Modify diagnostic JSON/readback/report or add a semantics note only for the named artifact. |
| `reject` | Human rejects the artifact as a diagnostic direction. | Record the failure reason and do not promote the artifact. |
| `defer_to_ymmp_carrier_probe` | Human cannot decide from static diagnostic artifacts alone. | Keep diagnostic-only status and consider a later explicit YMM4-compatible self-contained probe. |

## Required Human Fields

Use one block per artifact. `production_boundary_acknowledged` must be explicit
because diagnostic acceptance is easy to misread as production acceptance.

```text
artifact_id:
decision: accept_as_diagnostic_direction | revise | reject | defer_to_ymmp_carrier_probe
reason:
required_revision_if_any:
production_boundary_acknowledged: true | false
```

## Recorded Decision Blocks

```text
artifact_id: g28_lecture_diagram_carrier_skeleton_v1
decision: accept_as_diagnostic_direction
reason: generic Lecture Diagram Carrier frame contract, caption reserve, focal area, host role, and callout count pass readback, so it can serve as the shared skeleton for diagnostic variants.
required_revision_if_any: none
production_boundary_acknowledged: true
```

```text
artifact_id: g28_lecture_diagram_carrier_real_estate_information_gap_v1
decision: accept_as_diagnostic_direction
reason: real-estate information asymmetry is expressed as the focal chain 元付情報 -> ポータル掲載 -> 借主判断, proving useful G-28 carrier semantics without returning to G-27.
required_revision_if_any: none
production_boundary_acknowledged: true
```

```text
artifact_id: g28_lecture_diagram_carrier_game_mechanics_explanation_v1
decision: revise
reason: game mechanics explanation is promising, but mechanics diagram semantics, focal chain specificity, and callout density should be clarified at diagnostic level before production promotion or a YMM4 probe.
required_revision_if_any: Use the existing semantics note as the revision anchor: make the middle node concrete, with 判定 / 当たり判定 as the first-review primary internal process; keep 操作感 and リスクとリターン as supporting callouts; do not change generator, variant JSON, readback, or report in this slice.
production_boundary_acknowledged: true
```

```text
artifact_id: g28_map_evidence_carrier_skeleton_v1
decision: defer_to_ymmp_carrier_probe
reason: Map / Evidence Carrier depends on visual judgement of evidence surface priority, annotation density, and subtitle-band safety; JSON/readback pass alone is not enough for final diagnostic direction acceptance.
required_revision_if_any: In a later slice, prepare a YMM4-compatible self-contained probe or human visual review surface to inspect annotation density, evidence priority, and caption reserve.
production_boundary_acknowledged: true
```

```text
artifact_id: g28_source_footage_carrier_definition_only
decision: defer_to_ymmp_carrier_probe
reason: Source-Footage Carrier is definition-only and involves material rights, source priority, and decoration-over-evidence boundaries, so diagnostic direction acceptance is premature.
required_revision_if_any: Do not treat as a production candidate until a generator/readback or minimal diagnostic skeleton exists.
production_boundary_acknowledged: true
```

```text
artifact_id: g28_conversation_buffer_carrier_definition_only
decision: defer_to_ymmp_carrier_probe
reason: Conversation / Buffer Carrier is definition-only and may be too weak as a standalone screen, so it needs a later minimal skeleton or YMM4-compatible probe before acceptance.
required_revision_if_any: Prepare a later minimal skeleton/readback contract that prevents host-as-focal drift.
production_boundary_acknowledged: true
```

## Revise Target Clarification

`g28_lecture_diagram_carrier_game_mechanics_explanation_v1` is the only artifact
with `decision=revise` in this record. The revise target is diagnostic semantics,
not generator behavior:

- authoritative existing note:
  `docs/verification/G28-GAME-MECHANICS-DIAGRAM-SEMANTICS-NOTE-2026-06-05.md`
- focal chain to keep:
  `入力操作 -> 内部ルール / 判定 -> 画面上の結果`
- first-review middle-node emphasis:
  `判定 / 当たり判定`
- supporting callouts:
  `操作感`, `リスクとリターン`
- current slice action:
  decision recorded; diagnostic semantics clarification is owned by
  `docs/verification/G28-GAME-MECHANICS-DIAGRAM-SEMANTICS-NOTE-2026-06-05.md`
- not in this slice:
  generator changes, new variant generation, diagnostic JSON/readback/report
  changes, `.ymmp`, render, production promotion, or creative final acceptance

## Boundaries

- This is not G-27 revival, G-27 production carrier promotion, or G-27
  slot-fill.
- This is not common foundation or Codex Worker Orchestration implementation.
- No new G-28 variant, generator change, `.ymmp`, render, production carrier,
  creative final acceptance, rights automation, publishing automation, external
  image, URL, raw reference, source footage, gameplay capture, RSS, OPML,
  Inoreader, or NotebookLM source-pack work is included.
- `.claude/worktrees/` and `samples/2026-05-16.ymmp` remain local residue and
  are not part of this decision record.
