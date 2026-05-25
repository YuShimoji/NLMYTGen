# Baseball BN-03 static export handoff (2026-05-25)

This handoff keeps the Baseball sidequest restartable without changing the
G-27 mainline `next_action` in `docs/runtime-state.md`.

## Restart position

- Branch to resume: `codex/baseball-bn02-visual-data`
- Remote to pull: `origin/codex/baseball-bn02-visual-data`
- BN-02 implementation commit: `8252641 Add baseball visual data contract`
- BN-03 implementation commit: `c40462d Add baseball static PNG export`
- Local working tree at handoff time still had unrelated RSS reader, core, and
  G-27 dirty changes. They are expected and were not staged for Baseball.

Recommended restart commands:

```powershell
git fetch --all --prune
git checkout codex/baseball-bn02-visual-data
git pull --ff-only
git status --short --branch
```

If the same local checkout is reused, expect dirty files outside the Baseball
lane. Treat those as separate RSS/core/G-27 work unless the user explicitly
redirects.

## What is now fixed

BN-02 established `baseball_visual_data.v1` as the lane-local contract from a
sample sports episode dict into the `BaseballInfoGraphics` detailed visual.
BN-03 added the first static export proof on top of that contract.

| Area | Current state | Why it matters |
| --- | --- | --- |
| Visual data contract | `lanes/sports_news/examples/baseball_pitch_event_visual_data_sample.json` validates through `src/pipeline/baseball_visual_data.py` | The browser visual no longer depends only on hard-coded mock data. |
| Browser override | `BaseballInfoGraphics/data.js` prefers `window.BASEBALL_VISUAL_DATA` and falls back to the sample | Existing preview behavior stays intact while capture can inject external JSON. |
| Static capture | `gui/capture_baseball_infographic_static.js` renders only `DetailedVariant` in an Electron offscreen 1280x720 window | DesignCanvas and Tweaks chrome are excluded from the export surface. |
| Rebuild command | `cd gui && npm run capture:baseball-static` | The sample PNG, manifest, and readback can be regenerated from the repo. |
| Verification | `tests/test_baseball_static_export.py` checks PNG IHDR, manifest hashes, and boundary flags | BN-03 can fail early if the artifact drifts from the contract. |

Generated BN-03 artifacts:

- `samples/_probe/baseball/static/baseball_pitch_event_p05.png`
- `samples/_probe/baseball/static/baseball_pitch_event_p05_manifest.json`
- `samples/_probe/baseball/static/baseball_pitch_event_p05_readback.json`

The manifest records `not_yymm4_proof=true`, `not_animation_export=true`,
`not_creative_acceptance=true`, and `not_publish_gate=true`. This is important:
BN-03 proves the static PNG export path only. It does not approve YMM4
placement, animation, publishing, real-game sourcing, or creative acceptance.

## Verification already run

```powershell
node --check gui/capture_baseball_infographic_static.js
cd gui; npm run capture:baseball-static
uv run pytest tests/test_baseball_visual_data.py tests/test_baseball_static_export.py tests/test_pipeline_smoke_manifest.py
uv run pytest
```

Latest recorded results before this handoff:

- Narrow Baseball + smoke tests: `16 passed`
- Repo-level Python gate: `518 passed, 25 skipped`

## Known uncertainty

Electron capture currently produces a valid PNG and matching manifest/readback,
but the PNG byte hash can change across repeated runs even with animation
disabled. The stable contract is therefore: current artifact hash matches the
manifest, PNG IHDR is 1280x720, readback says `status=passed`, and the DOM
readback shows `design_canvas_visible=false` and `tweaks_visible=false`.

The capture harness follows the existing Baseball HTML approach and loads React,
ReactDOM, Babel, and Google fonts through CDN links. That avoids new repo
dependencies in BN-03, but an offline or CDN-blocked environment may need a
later vendored/offline harness before byte-level reproducibility is claimed.

## Next practical entry points

| Entry | Bottleneck it reduces | What becomes possible |
| --- | --- | --- |
| Verify C-detail PNG readability | Small text, side panel density, and safe-area crop judgement | Decide whether to tune the design before YMM4 placement. |
| Advance BN-04 animation export | The static surface is proven, but pitch-change motion is not exported | Choose frame sequence versus clip using a real capture harness. |
| Advance BN-05 YMM4 placement | PNG exists, but duration/layer/ImageItem rules are not contracted | Place the static PNG into a narration segment without hand-authored drift. |
| Audit real episode source replacement | The pipeline is still sample-only | Replace `sample://` assumptions with real sourced episode input when ready. |

Recommended default for the next assistant-owned slice is BN-05 if the user
wants YMM4 integration pressure reduced first, or BN-04 if the user wants the
Baseball visual to become motion-ready before placement.
