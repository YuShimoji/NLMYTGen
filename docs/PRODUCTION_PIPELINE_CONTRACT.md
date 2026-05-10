# Production Pipeline Contract

Purpose: turn lessons from G-27 into a reusable production pipeline contract.
This document is about factory reliability across topics, not further tuning the
Real Estate DX v2 visual proof.

This contract does not authorize G-27 v3 proof work, scene decision packet work,
asset/proxy gap reporting, YMM4 conversion, rendering, production timing, or
creative acceptance. Those remain separate slices.

## Core Rule

User-facing review must happen in the GUI timeline. HTML, PNG, and JSON are
evidence artifacts or machine-readable inputs; they are not independent review
surfaces.

Docs define contracts. They do not replace review. YMM4 is an exit surface after
pipeline gates pass; it is not the place to discover basic design structure.

## Production Pipeline Contract

| stage | input artifact | output artifact | user sees | machine check | human review point | completion condition | may pass to next when | prohibited |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NotebookLM script | source notes, NotebookLM output, topic brief | `source_script.txt` plus optional source notes | GUI episode context / script summary after ingest | UTF-8, speaker format, line count, obvious corruption, optional script diagnostics | script premise, audience, conclusion, and factual direction | script is readable, scoped, and line-addressable | line spans can be referenced by later IR | no layout, no YMM4 placement, no asset decisions |
| Script Beat IR | `source_script.txt`, row/time map when available | `script_beat_ir.json` | GUI story outline and segment timeline | schema, reversible script line spans, coverage, no visual coordinates | segment boundaries and narration cues | every segment/beat maps back to script text | each beat has cue, role, local context, and stable id | no CSS/HTML, no frame coordinates, no YMM4 parameters |
| Visual Direction Contract | Script Beat IR, topic constraints, anti-pattern notes | `visual_direction_contract.json` or `.md` | GUI direction summary and warnings | max text policy, subtitle policy, anti-pattern checklist, metadata isolation policy | tone, abstraction level, density, motifs | visual vocabulary is fixed without creating production assets | shot layout can use the direction without rereading raw docs | no production template, no render target, no asset acquisition |
| Shot Layout Plan | Script Beat IR, Visual Direction Contract | `shot_layout_plan.json` | GUI frame/timeline proof panel | 16:9 frame contract, safe area, subtitle clearance, metadata isolation, label budget | whether each frame conveys its payload before polish | each required beat has a frame layout and exceptions in sidecar | layout violations are either absent or explicitly classified | no YMM4 conversion, no final template claim, no hidden metadata in frame |
| Motion Beat Plan | Shot Layout Plan | `motion_beat_plan.json` | GUI beat table | every beat records `enter`, `move`, `emphasize`, `reveal`, `dim` as applicable | whether the change reads as motion, not slide replacement | motion primitives exist for each target beat | primitives are clear enough for adapter planning | no production timing, no keyframe values, no YMM4 effect tuning |
| GUI Review | review packet, proof image, sidecar JSON, proof HTML as evidence | `review_decisions.json` | GUI timeline only | DOM smoke, proof image visible, beat table visible, decision save schema | user accepts, revises, defers, or cuts design direction | user decision is saved or explicitly deferred in GUI | saved decisions identify next artifact and classification hint | no standalone HTML/PNG/JSON review request as normal flow |
| Review Decisions | `review_decisions.json`, review packet | stable decision record | GUI decision summary | JSON schema, segment ids match packet, unselected segments reported | confirm unresolved decisions if they change the next artifact | selected/deferred/cut states are machine-readable | unresolved states are allowed only with explicit blocked reason | no implied acceptance from missing user input |
| Scene Decision Packet | Review Decisions, Shot Layout Plan, Motion Beat Plan | `scene_decision_packet.json` | GUI summary or concise report | schema, `accepted_proxy` / `needs_revision` / `cut_from_plan` / `defer` classification | only classifications with real tradeoffs | every segment has a next state and rationale | asset/proxy needs are derivable | no YMM4 adapter output, no production readiness claim |
| Asset/Proxy Gap Report | Scene Decision Packet, template registry, asset/proxy inventory | `asset_proxy_gap_report.json` / `.md` | GUI gap panel or concise report | required asset/proxy coverage, blocked reason codes, replacement triggers | choose real asset, proxy, cut, or defer | every missing item is classified | no blocking unknowns remain for adapter planning | no automatic external asset acquisition, no rights laundering |
| YMM4 Adapter Output | Scene Decision Packet, resolved Gap Report, existing YMM4 project/template sources | adapter IR / patch output / readback | YMM4 only after gate opens | dry-run/readback, route contract, no forbidden zero-generation | creative acceptance in YMM4 after adapter output exists | readback passes and validator allows this stage | YMM4 confirmation is needed for final creative acceptance | forbidden while validator blocks YMM4, render, production timing, or creative acceptance |

## Artifact Authority Map

| artifact surface | authority | user-facing role | allowed use | not allowed |
| --- | --- | --- | --- | --- |
| GUI timeline | primary review surface | where the user makes production-design decisions | display context, proof image, beat table, warnings, decisions, blocked reasons | cannot bypass machine checks or validator gates |
| HTML proof | evidence artifact | normally not reviewed directly | render/debug proof, screenshot source, DOM/readback target | cannot be a standalone completion condition or production surface |
| PNG proof | evidence artifact | visible inside GUI | visual proof, screenshot evidence, regression comparison | cannot become production input, production template, or creative acceptance |
| JSON sidecar | machine-readable contract | not for direct user reading in normal flow | feed GUI, checks, next artifacts, readback, blocked reasons | cannot replace GUI review or imply user acceptance |
| Markdown/docs | contract and evidence log | reference when needed | define responsibilities, boundaries, and audit trail | cannot become the review surface or hide executable handoff details |
| YMM4 | exit / creative acceptance surface | final creative confirmation after gates pass | inspect adapter output, final composition, render readiness | cannot be used to discover upstream structure while blocked |
| PDF/reference deck | source or anti-pattern only, depending on declaration | not a production layout authority unless explicitly approved | anti-pattern corpus, source material, or factual reference with provenance | cannot silently become a layout reference or production asset |

## Multi-topic Smoke Plan

The goal is pipeline-connection reliability, not finished video quality. The
same path must work for at least three topics before the pipeline is treated as
repeatable.

| smoke topic | why this topic | minimal script fixture | Script Beat IR check | 3-beat visual proof check | GUI ingest check | review decision save check | blocked reason / next action check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Real Estate DX baseline | existing G-27 evidence stresses proxy visuals, hidden information, and risk motifs | `samples/_probe/pipeline_smoke/real_estate_dx/source_script.txt` derived from a small excerpt, not full G-27 production | 3 segments, line spans, narration cues, no visual coordinates | 3 segments × 3 beats, frame contract sidecar, no production-frame metadata | GUI timeline shows proof image, beat table, warnings, decisions | `review_decisions.json` stores accept/revise/defer per segment | blocked by unresolved production assets/proxies; next action remains gap classification, not YMM4 |
| AI monitoring labor | social/technical explainer stresses human stakes without real-estate motifs | `samples/_probe/pipeline_smoke/ai_monitoring_labor/source_script.txt` from a short fixture inspired by existing labor-monitoring sample | beats separate premise, mechanism, human cost | proof uses workplace/device/procedure proxies without becoming dashboard slides | GUI shows context and motion primitives | decisions capture whether visual metaphor is too punitive or too abstract | blocked by missing generic labor/platform proxy vocabulary; next action is proxy taxonomy, not render |
| Baseball news infographic | sidequest/data topic stresses numbers, provenance, and information density | `samples/_probe/pipeline_smoke/baseball_news/source_script.txt` as a small invented fixture, not a live scrape | beats separate headline, stat contrast, implication | proof uses scoreboard/card/map proxies without raw data table overload | GUI shows proof and provenance warning area | decisions capture whether info density is acceptable | blocked by data/provenance fixture status and screen-plan approval; next action is screen-plan smoke, not YMM4 |

Minimum smoke artifacts per topic:

- `source_script.txt`
- `script_beat_ir.json`
- `visual_direction_contract.json`
- `shot_layout_plan.json`
- `motion_beat_plan.json`
- `visual_treatment_proof.{html,png,json}`
- `visual_treatment_proof_readback.json`
- `review_packet.json`
- `review_decisions.json`

The first smoke implementation should create only the smallest viable fixture
for each topic. It should not import the full G-27 proof, should not generate a
finished video, and should not attempt YMM4 output.

## Definition of Done

A production-pipeline slice is done only when:

- The user-facing state is visible in the GUI timeline, or a concrete GUI
  ingest path is implemented and verified.
- The next artifact is named, machine-readable where appropriate, and accepted
  by a narrow check.
- HTML, PNG, and JSON are treated as evidence/machine inputs, not standalone
  review surfaces.
- The slice states whether it is blocked, reviewable, or passable to the next
  stage.
- Any human decision needed to continue is captured by GUI review decisions or
  explicitly recorded as deferred.
- Forbidden downstream work remains blocked until the relevant stage and
  validator allow it.

Standalone HTML/PNG/JSON generation never completes a review slice by itself.
It must be GUI-visible, GUI-ingestable, or explicitly marked as diagnostic-only.

## Stop Condition For This Slice

This slice stops at contract and multi-topic smoke planning. Do not proceed here
to:

- G-27 v3 proof.
- G-27 scene decision packet.
- G-27 asset/proxy gap report.
- YMM4 adapter output.
- Rendering.
- Production timing.
- Creative acceptance.

The next implementation slice should start with the multi-topic smoke fixtures
and GUI ingest path, not with another Real Estate DX design-polish pass.
