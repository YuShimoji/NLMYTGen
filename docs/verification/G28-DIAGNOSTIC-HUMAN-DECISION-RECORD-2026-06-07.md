# G-28 Diagnostic Human Decision Record - 2026-06-07

This record is the intake surface for human decisions on existing G-28
diagnostic artifacts. No human `accept`, `revise`, `reject`, or `defer` decision
has been supplied for this packet in the current prompt, so every artifact below
remains `pending_human_decision`.

Diagnostic acceptance, when later supplied by a human, means only that a
diagnostic direction is acceptable. It is not production carrier approval,
creative final acceptance, render approval, rights approval, publishing approval,
or permission to set `production_candidate=true`.

## Artifact Inventory

| artifact_id | artifact | readback | diagnostic_only | production_candidate | decision_status |
|---|---|---:|---:|---:|---|
| `g28_lecture_diagram_carrier_skeleton_v1` | Generic Lecture Diagram skeleton | passed | true | false | pending_human_decision |
| `g28_lecture_diagram_carrier_real_estate_information_gap_v1` | Lecture Diagram `real_estate_information_gap` variant | passed | true | false | pending_human_decision |
| `g28_lecture_diagram_carrier_game_mechanics_explanation_v1` | Lecture Diagram `game_mechanics_explanation` variant | passed | true | false | pending_human_decision |
| `g28_map_evidence_carrier_skeleton_v1` | Map / Evidence Carrier skeleton | passed | true | false | pending_human_decision |
| `g28_source_footage_carrier_definition_only` | Source-Footage Carrier definition | no generator/readback | n/a | false | pending_human_decision |
| `g28_conversation_buffer_carrier_definition_only` | Conversation / Buffer Carrier definition | no generator/readback | n/a | false | pending_human_decision |

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

## Pending Decision Blocks

```text
artifact_id: g28_lecture_diagram_carrier_skeleton_v1
decision: pending_human_decision
reason:
required_revision_if_any:
production_boundary_acknowledged:
```

```text
artifact_id: g28_lecture_diagram_carrier_real_estate_information_gap_v1
decision: pending_human_decision
reason:
required_revision_if_any:
production_boundary_acknowledged:
```

```text
artifact_id: g28_lecture_diagram_carrier_game_mechanics_explanation_v1
decision: pending_human_decision
reason:
required_revision_if_any:
production_boundary_acknowledged:
```

```text
artifact_id: g28_map_evidence_carrier_skeleton_v1
decision: pending_human_decision
reason:
required_revision_if_any:
production_boundary_acknowledged:
```

```text
artifact_id: g28_source_footage_carrier_definition_only
decision: pending_human_decision
reason:
required_revision_if_any:
production_boundary_acknowledged:
```

```text
artifact_id: g28_conversation_buffer_carrier_definition_only
decision: pending_human_decision
reason:
required_revision_if_any:
production_boundary_acknowledged:
```

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
