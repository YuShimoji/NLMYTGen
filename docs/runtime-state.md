# Runtime State — NLMYTGen

Project-State-ID: generic-visual-capability-envelope-delivered-v1
State-Revision: 2026-07-14.2
Updated: 2026-07-14 JST
Product-State: generic-visual-composition-capabilities-audited
Product-Gate: generic-yymm4-capability-probe-decision
Recommended-Next: review-capability-envelope-and-select-probe
External-State: public-repo-feature-branch

## Current Slice

- **Generic capability envelope delivered**: 78 relevant visual/YMM4 paths are
  classified as reusable core, pilot-local helper, topic-specific, historical
  evidence, obsolete/duplicate, or unknown. Unclassified relevant paths are 0.
- **Evidence ladder enforced**: 38 capabilities resolve to proven 15,
  conditional 14, unsupported 5, and unknown 4. C0/C1/C2/C3/C4/C5 counts are
  5/3/14/14/2/0. `proven` begins at C3, strict render evidence begins at C4,
  and no C5 claim exists.
- **Existing evidence stays bounded**: VoiceItem/linked-subtitle import, exact
  fixed project reopen, named GroupItem motion/templates, and one strict internal
  render retain their actual C3/C4 scope. Static fields, builders, schemas, tests,
  and unretained render observations are not promoted.
- **Minimal generic Scene IR added**: one data-driven validator supports variable
  scenes/cues, semantic role, recipe, existing SCS geometry, timing anchor,
  primitives, overlays, motion request, capability/evidence requirements,
  fallback, rights boundary, and ordinal cost. It imports no topic builder and
  contains no current-topic nouns, evidence IDs, cue text, palette facts, fixed
  speaker split, or fixed episode timing.
- **Composition grammar delivered**: narration baseline, inspection/explanation,
  process/sequence, comparison/contrast, callout focus, and recap/action sequence
  extend the existing SCS roles and geometry. Every recipe carries required and
  optional primitives, prohibited combinations, evidence, fallback, cost/reuse,
  suitable/unsuitable archetypes, and remaining YMM4 observation needs. Each
  whole-composition floor is C0 because caption-safe reserve depends on the
  unknown subtitle-layout capability; deterministic recipe conformance is C2.
- **Cross-archetype static lab passed**: Route A inspection (3 scenes / 9 cues),
  unrelated synthetic process (4 / 5), and unrelated synthetic comparison
  (2 / 4) pass the same validator. Different counts demonstrate schema
  invariance only; runtime capability and cross-topic reuse remain false.
- **Route A remains data-only**: the source packet is read-only and still records
  recommended-not-selected. The current supervisor contract selects it only as a
  conformance fixture. Exact text, claim/source references, timing, palette,
  factual boundaries and named motion proposals live in fixture payload;
  implementation/render authorization remain false. Twenty derived/explicit
  capability gaps have static/narration fallbacks; nine are subtitle-layout gaps.
- **Minimum generic stack recommended**: C3 narration/import + C3 observed cue
  timing + C3 no-transition baseline, optional C2 static local image/short text,
  C2 fixture preflight, and a required C0 subtitle-layout gate before visual
  acceptance. Motion is off by default. This is W2 setup, low
  per-episode burden, small maintenance, optional rights dependency and easy
  recovery; broad reuse remains a hypothesis until C5.

## Exact Next Action

Review `docs/visual_system/README_GENERIC_VISUAL_CAPABILITIES.md`, especially the
capability matrix, minimum stack, and expensive/not-worth-building section.
Choose at most one bounded H1 generic YMM4 probe only if its recurring value
justifies observation cost. Candidate classes are a minimal static
Text/Image/Shape layout, one fade, or one bounded transform. Do not use H1 to
implement the final Route A scene or render.

## Primary Evidence and Access

- Primary human matrix: `docs/visual_system/README_GENERIC_VISUAL_CAPABILITIES.md`
- Can/conditional/cannot/unknown: `docs/visual_system/CAN_DO_CANNOT_DO.md`
- Capability/evidence data: `generic_visual_capability_matrix.json` and
  `capability_evidence_ledger.json` beside the primary matrix.
- Composition/cost data: `scene_composition_grammar.json`,
  `capability_combination_map.json`, and `cost_reuse_matrix.json`.
- Recommended stack: `recommended_minimum_generic_stack.json`.
- Conformance lab: `samples/visual_composition_lab/README.md` and
  `conformance_readback.json`.
- Secondary self-contained board: `docs/visual_system/visual_capability_board.html`.

## Active Boundaries

- No Computer Use, screenshot, YMM4 launch/inspection, final `.ymmp`, render,
  media regeneration, image/audio/font generation, external fetch, dependency
  installation, source/script change, publication, rights approval, master
  mutation, merge, or rebase occurred.
- The lab writes JSON/readback/HTML only. No ignored local project or media was
  created, changed, staged, or committed.
- Static fixture success never implies runtime, visual quality, portability,
  production readiness, universal topic support, or C5.

## Retained Quality Debt

| Debt | Impact | Owner | Revisit trigger |
| --- | --- | --- | --- |
| Generic Text/Image/Shape layout observation | Keeps these primitives and composition interactions at C2 | YMM4 integration owner | one H1 primitive is selected because it serves multiple archetypes |
| Subtitle typography and safe-area readability | Prevents visual acceptance of linked subtitles | human visual reviewer | first material generic layout is opened in YMM4 |
| Cross-machine project/asset portability | Keeps generated projects same-machine | YMM4 integration owner | a project must move to another machine |
| Real cross-topic reuse | Keeps C5 at zero | episode-factory owner | a second heterogeneous real episode is ready without core-code changes |
| Render semantic/visual acceptance | C4 media validity does not prove cue alignment or design quality | human editorial/visual reviewer | an authorized real project reaches a render milestone |

## Maintenance Note

Keep this capsule within 160 lines. Detailed capability records belong under
`docs/visual_system/`; topic payload remains in fixtures, not generic core.
