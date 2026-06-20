# Baseball Pipeline Contract

Status: BN-06 pipeline contract plus BN-07 Data Capsule fixture, sample-only,
not production ready.

This document defines how the Baseball sidequest connects factual baseball data,
script emphasis, visual scene timing, YMM4 transport, and human review. It
builds on the accepted BN-05 manual preview gate, but it does not reopen BN-05
placement, does not redesign the visual, and does not claim render completion,
production proof, creative final acceptance, publishing readiness, or real
episode suitability.

## Contract Chain

```text
BaseballDataCapsule
  -> ScriptBeatIR
  -> VisualScenePlan
  -> YMM4Adapter
  -> ReviewGate
```

## Layer Ownership

| Layer | Owns | Consumes | Must not decide |
| --- | --- | --- | --- |
| BaseballDataCapsule | factual source of truth: event id, pitch sequence, score, count, runners, player/stat facts, and derived factual deltas | upstream source material or sample fixture | narrative emphasis, visual timing, YMM4 layers, creative acceptance |
| ScriptBeatIR | narrative angle, explanation order, spoken beats, and compact text beats | BaseballDataCapsule fact ids | new facts, visual layout, YMM4 item geometry |
| VisualScenePlan | semantic screen slots, timing, emphasis, motion primitives, and scene state transitions | BaseballDataCapsule and ScriptBeatIR | new facts, spoken narrative priority, YMM4 implementation details |
| YMM4Adapter | layer hints, item families, frame ranges, keyframe intent, captions, and review artifact routing | VisualScenePlan | facts, narrative emphasis, final creative judgment |
| ReviewGate | human judgment records and gate scope | proof artifacts and review returns | render completion, production proof, rights, publishing, real-source approval |

## Pipeline Sample Artifacts

| Artifact | Path | Role |
| --- | --- | --- |
| Data capsule | `samples/_probe/baseball/pipeline/baseball_data_capsule_p05.json` | Sample-only P05 slider event facts and derived deltas |
| Data capsule schema | `samples/_probe/baseball/pipeline/baseball_data_capsule_p05_schema.json` | Minimal BN-07 fixture contract for required fields and stable refs |
| Data capsule readback | `samples/_probe/baseball/pipeline/baseball_data_capsule_p05_readback.json` | BN-07 validation result and machine-check summary |
| Data capsule fixture manifest | `samples/_probe/baseball/pipeline/baseball_data_capsule_p05_fixture_manifest.json` | BN-07 artifact index, validation scope, and next action |
| Script Beat IR | `samples/_probe/baseball/pipeline/baseball_script_beat_ir_p05.json` | Narrative explanation order that references data ids |
| Script Beat IR schema | `samples/_probe/baseball/pipeline/baseball_script_beat_ir_p05_schema.json` | Minimal BN-08 linkage contract for beats, claims, timing hints, and visual intent |
| Script Beat IR readback | `samples/_probe/baseball/pipeline/baseball_script_beat_ir_p05_readback.json` | BN-08 validation result and claim-link summary |
| Script Beat IR manifest | `samples/_probe/baseball/pipeline/baseball_script_beat_ir_p05_manifest.json` | BN-08 artifact index, validation scope, and next action |
| Visual Scene Plan | `samples/_probe/baseball/pipeline/baseball_visual_scene_plan_p05.json` | Time-based semantic slots and motion primitives |
| Manifest | `samples/_probe/baseball/pipeline/baseball_pipeline_contract_manifest.json` | Artifact index, validation expectations, and boundaries |

## BN-07 Data Capsule Fixture Rules

BN-07 makes the BaseballDataCapsule concrete for the P05 sample sequence. The
fixture owns event, game-state, participant, pitch-sequence, derived-fact,
highlight-candidate, and provenance fields. It also owns `data_ref_index`.

Stable data refs must follow these rules:

1. Every consumer-facing data ref uses the `fact_` prefix.
2. Every `fact_` id appears in both `derived_facts` and `data_ref_index`.
3. Pitch entries and highlight candidates may reference only ids in
   `data_ref_index`.
4. ScriptBeatIR and VisualScenePlan may consume refs but must not create facts
   outside the Data Capsule.
5. Synthetic provenance flags stay true until a separate real-source ingest and
   rights slice is opened.

## BN-08 ScriptBeatIR Linkage Rules

BN-08 links ScriptBeatIR to the validated Data Capsule. ScriptBeatIR may choose
narrative emphasis, beat order, supported claims, timing hints, and visual
intent. It cannot create facts.

Script linkage must follow these rules:

1. Every beat has a stable `beat_` id and a matching `beat_ref_index` entry.
2. Every beat-level and claim-level `data_refs` value exists in the Data
   Capsule `data_ref_index`.
3. Score, count, speed, pitch type, pitch result, zone, and participant claims
   are backed by explicit `fact_` refs.
4. Timing hints are relative suggestions for BN-09 only.
5. Visual intent may name focus areas, but must not decide layout slots, YMM4
   layers, keyframes, render state, or final design.

## P05 Default Flow

The sample P05 flow uses the accepted slider event from prior Baseball artifacts:

1. Data capsule records the score, inning, count, pitcher/batter sample facts,
   P04 fastball context, P05 slider result, and velocity delta.
2. Script Beat IR chooses the narrative angle: a velocity and pitch-type change
   from a 155 km/h fastball to a 140 km/h slider.
3. Visual Scene Plan maps that angle into timed screen slots: score context,
   pitch event headline, current pitch card, pitch log emphasis, count/runners,
   and strike-zone trace.
4. YMM4Adapter later maps those slots into YMM4 `ImageItem`, `TextItem`,
   `ShapeItem`, or `VideoItem` transport. The adapter cannot invent data or
   decide the story angle.
5. ReviewGate records whether the artifact is accepted as diagnostic/manual
   preview, render proof, production proof, creative final acceptance, or
   publish-ready. BN-05 is accepted only as a diagnostic/manual preview gate.

## Motion Primitive Vocabulary

BN-06 names motion primitives but does not implement animation export or YMM4
keyframes. The sample Visual Scene Plan may use:

| Primitive | Meaning | Later adapter hint |
| --- | --- | --- |
| `score_context_hold` | score and inning stay readable while the event changes | hold layer and opacity stable |
| `pitch_log_focus_shift` | previous pitch context yields to current pitch | emphasize current pitch row |
| `zone_trace_reveal` | pitch location becomes visible as the explanation lands | reveal or fade trace/marker |
| `claim_emphasis_pulse` | the main pitch-event claim receives short emphasis | brief scale/opacity/color emphasis |
| `caption_reserve_hold` | bottom caption area remains clear | preserve safe area |

## Boundaries

- The sample artifacts are sample-only and do not use real source footage.
- The contract does not fetch sources, use official materials, use real player
  images, or use AI-generated player images.
- The contract does not perform clip export, video generation, TTS, thumbnail
  work, YouTube work, publishing, or external publish.
- The contract does not claim render completion, production proof, creative
  final acceptance, or real episode suitability.
- Mainline `master`, G-27, RSS, NotebookLM, and common foundation work remain
  outside this slice.

## Validation

The focused validation is:

```powershell
uv run pytest tests/test_baseball_data_capsule_fixture.py tests/test_baseball_script_beat_ir_linkage.py tests/test_baseball_pipeline_contract.py
```

Those tests confirm the layer chain, sample references, stable data refs,
script claim linkage, pitch sequence consistency, scope boundaries, manifest
paths, and next action remain contract-only.

## Next Action

The next Baseball-sidequest move after BN-08 is BN-09 VisualScenePlan timing
linkage against the linked ScriptBeatIR beats. Adapter readback design and
motion export proof remain separate later slices. All paths remain separate
from render, production proof, creative final acceptance, publishing,
real-source ingest, TTS, and thumbnail work.
