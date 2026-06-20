# Baseball Pipeline Contract

Status: BN-06 sidequest contract, sample-only, not production ready.

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

## BN-06 Sample Artifacts

| Artifact | Path | Role |
| --- | --- | --- |
| Data capsule | `samples/_probe/baseball/pipeline/baseball_data_capsule_p05.json` | Sample-only P05 slider event facts and derived deltas |
| Script Beat IR | `samples/_probe/baseball/pipeline/baseball_script_beat_ir_p05.json` | Narrative explanation order that references data ids |
| Visual Scene Plan | `samples/_probe/baseball/pipeline/baseball_visual_scene_plan_p05.json` | Time-based semantic slots and motion primitives |
| Manifest | `samples/_probe/baseball/pipeline/baseball_pipeline_contract_manifest.json` | Artifact index, validation expectations, and boundaries |

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
uv run pytest tests/test_baseball_pipeline_contract.py
```

That test confirms the layer chain, sample references, scope boundaries,
manifest paths, and next action remain contract-only.

## Next Action

The next Baseball-sidequest move after BN-06 is to choose one bounded follow-up:
turn the Visual Scene Plan into an adapter readback design, or define a motion
export proof for the named primitives. Either path remains separate from render,
production proof, creative final acceptance, publishing, real-source ingest,
TTS, and thumbnail work.
