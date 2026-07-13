# Runtime State — NLMYTGen

Project-State-ID: generic-visual-static-layout-probe-ready-v1
State-Revision: 2026-07-14.3
Updated: 2026-07-14 JST
Product-State: generic-visual-static-layout-yymm4-probe-ready
Product-Gate: manual-generic-static-layout-observation
Recommended-Next: run-generic-static-layout-yymm4-probe
External-State: public-repo-feature-branch

## Current Slice

- **Evidence count sealed**: the canonical inventory remains 78 relevant paths;
  38 capabilities remain proven 15 / conditional 14 / unsupported 5 / unknown 4,
  with C0-C5 = 5/3/14/14/2/0. `PROJECT_PIPELINE.mmd` now agrees with the
  inventory and current surfaces. No capability record was regraded.
- **Validation scope is exact**: `docs/visual_system/validation_scope_receipt.json`
  owns the current non-overlapping test selections, per-command counts, state-test
  inclusion and aggregate. It supersedes the ambiguous historical 178/186 prose;
  no arithmetic reconstruction was assumed.
- **One neutral H0 probe is prepared**: a tracked neutral sample supplies one
  unchanged VoiceItem and visible linked-subtitle settings. Its source hash is
  sealed and unchanged. Existing source Image/Tachie and GUI state are not
  inherited. The ignored output has exactly VoiceItem 1 + static ImageItem 1 +
  independent TextItem 1 over the observed 109-frame Voice span.
- **Layout contract is explicit**: an opaque original 640x360 RGB image occupies
  the upper-left zone, `PROBE LABEL` occupies an upper-right conservative zone,
  and the linked-subtitle reserve occupies the bottom. All three bounding zones
  are pairwise disjoint by contract. Actual crop, anchor, wrap, readability and
  overlap remain H1 observations.
- **Operator Batch is ready**: Japanese-first instructions use at most three
  actions and exactly three observations. `-PreflightOnly` and `-CollectOnly`
  resolve or launch no YMM4 executable. Normal mode may open the prepared project
  once for the user; it performs no automatic GUI action, save, close, screenshot
  or render. Existing local evidence is preserved and must be archived, not deleted.
- **Evidence boundary remains C2/H0**: project parse, deterministic generation,
  source/Voice invariance, item counts, static default fields, scripts and safe
  transport are verified. No YMM4 visual observation occurred, so C3/C4/C5,
  runtime success and visual acceptance remain unclaimed.

## Exact Next Action

From the repository root, the user may run exactly:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\samples\visual_composition_lab\runtime_probe\operator_batch\run_generic_static_layout_probe.ps1
```

Inspect only: (1) linked-subtitle readability/non-overlap, (2) Image visibility
without unexpected crop/anchor shift, and (3) Text visibility without clipping,
unwanted wrapping or subtitle overlap. Close YMM4 without project save or render,
then answer the three terminal questions.

## Primary Evidence and Access

- Probe entry: `samples/visual_composition_lab/runtime_probe/README_STATIC_LAYOUT_PROBE.md`
- Contract and fixture: `static_layout_probe_contract.json` and
  `static_layout_probe_fixture.json` beside the entry.
- Structural readback: `static_layout_probe_materialization_readback.json`.
- Operator contract: `operator_batch/README_OPERATOR_BATCH.md`,
  `operator_batch_manifest.json` and `expected_observation_contract.json`.
- Validation authority: `docs/visual_system/validation_scope_receipt.json`.
- Capability authority remains `docs/visual_system/README_GENERIC_VISUAL_CAPABILITIES.md`.

## Active Boundaries

- Worker Computer Use = 0 and Worker YMM4 launches = 0. Only structural
  preflight and synthetic fixture collection were executed; the normal Operator
  Batch was not executed.
- The generated `.ymmp`, abstract PNG and archived synthetic fixture results are
  under the package's ignored `local_outputs/`; none is tracked or staged.
  `operator_batch.local.json` and `operator_result.json` are future ignored H1 targets
  and do not exist in the H0 evidence set.
- No source carrier overwrite, screenshot, render/media output, external asset,
  dependency install, Route A implementation, topic branch, rights/publication
  action, master mutation, merge or rebase occurred.
- Serializer defaults (`Opacity=100`, `Zoom=100`, `Rotation=0`, zero fades) are
  openability fields, not observed opacity/zoom/transform/fade capability use.

## Retained Quality Debt

| Debt | Impact | Owner | Revisit trigger |
| --- | --- | --- | --- |
| Linked-subtitle readability/non-overlap | Keeps the common layout floor unaccepted at runtime | human visual reviewer | prepared project is opened in H1 |
| Image crop/anchor | Keeps static ImageItem placement at structural C2 | human visual reviewer | H1 image checkpoint is answered |
| Text wrap/anchor | Keeps short TextItem placement at structural C2 | human visual reviewer | H1 text checkpoint is answered |
| Cross-machine project/asset portability | Keeps the prepared project same-machine | YMM4 integration owner | the package must run on another machine |
| Real second-topic reuse | Keeps C5 at zero | episode-factory owner | a heterogeneous second topic uses the same core unchanged |

## Maintenance Note

Keep this capsule within 160 lines. Runtime observations belong in ignored result
evidence and a bounded successor intake, not in generic capability claims by default.
