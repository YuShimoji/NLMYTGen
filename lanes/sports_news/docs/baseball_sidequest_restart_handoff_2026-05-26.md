# Baseball sidequest restart handoff (2026-05-26)

This handoff keeps the Baseball work restartable from another terminal without
changing the G-27 mainline, RSS worktree, runtime state, production YMM4
artifacts, shared API/auth/DB, or dependency contracts.

## Current handoff update

For the latest verified restart state, read
`lanes/sports_news/docs/baseball_bn05_manual_preview_gate_handoff_2026-06-17.md`
first. It records the 2026-06-17 re-anchor on
`codex/baseball-bn02-visual-data`, confirms upstream parity `0 0`, confirms
BN-05 placement proof/readback still pass mechanically, and preserves the
remaining manual YMM4 preview request. This 2026-05-26 file remains useful as
the historical handoff for BN-03 through BN-04 and the original BN-05 placement
contract setup.

## Restart position

- Worktree: `C:\Users\PLANNER007\NLMYTGen-baseball-sidequest`
- Branch: `codex/baseball-bn02-visual-data`
- Historical handoff commit: `8546310 Add baseball frame sequence export`
- Remote: pushed to `origin/codex/baseball-bn02-visual-data`
- Local status at handoff time: clean and equal to remote
- Main worktree scope: read-only; do not stage or edit G-27/RSS changes from
  `C:\Users\PLANNER007\NLMYTGen`

Branch / thread / supervisor routing is now owned by
`docs/BRANCH_THREAD_SUPERVISION.md`. For current HEAD, run `git log -1
--oneline`; do not treat the historical handoff commit above as the latest
branch state.

Use this to resume:

```powershell
cd C:\Users\PLANNER007\NLMYTGen-baseball-sidequest
git fetch --all --prune
git checkout codex/baseball-bn02-visual-data
git pull --ff-only
git status --short --branch
git rev-list --left-right --count "HEAD...@{u}"
```

The expected status is a clean
`## codex/baseball-bn02-visual-data...origin/codex/baseball-bn02-visual-data`.

## Current Baseball slice

| Slice | Current state | Key artifacts | Boundary |
| --- | --- | --- | --- |
| BN-02 visual data contract | Implemented | `lanes/sports_news/examples/baseball_pitch_event_visual_data_sample.json`, `src/pipeline/baseball_visual_data.py` | sample-only source |
| BN-03 static PNG export | Implemented | `samples/_probe/baseball/static/baseball_pitch_event_p05.png` | not YMM4 proof |
| BN-05 placement contract/proof | Implemented mechanically | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof.ymmp` | needs manual YMM4 preview |
| BN-04 frame sequence export | Implemented mechanically | `samples/_probe/baseball/animation/frames/baseball_pitch_event_p05/*.png` | not clip export |

The most important manual blocker is BN-05 preview. Open the proof `.ymmp` in
YMM4, inspect frame `1560` / `00:26.00`, and return one screenshot plus a
short freeform note. Fixed labels are not required. The exact hands-on checklist is in
`lanes/sports_news/docs/baseball_manual_preview_hands_on_2026-05-26.md`.

## Latest validation

- `node --check gui/capture_baseball_infographic_frames.js`
- `cd gui && npm run capture:baseball-frames`
- repeated frame capture hash stability check passed
- `uv run pytest tests/test_baseball_visual_data.py tests/test_baseball_static_export.py tests/test_baseball_yymm4_placement_contract.py tests/test_baseball_yymm4_placement_proof.py tests/test_baseball_frame_sequence_export.py tests/test_pipeline_smoke_manifest.py`
  passed with `28 passed`
- `uv run pytest` passed with `520 passed, 25 skipped`
- `git diff --check` passed

## What changed in the last slice

The latest slice added `gui/capture_baseball_infographic_frames.js` and the
`capture:baseball-frames` npm script. It exports five 1280x720 PNG frames from
the C detailed renderer, writes a manifest/readback, and verifies that no
DesignCanvas or Tweaks UI appears. `DetailedVariant` now passes
`animateLatest=false` down to `PitchStage`, so repeated offscreen captures are
stable instead of catching live SVG animation mid-frame.

The generated frames intentionally collapse to two visual states: frame `0`
shows the previous P04 fastball context, and frames `1` through `4` show the
current P05 slider state. This is enough for a deterministic transport proof;
full motion design or clip export is still a later decision.

## Next entry points

| Entry | Choose this when | Reduces | Next possible action |
| --- | --- | --- | --- |
| Verify BN-05 manual preview | YMM4 is available | Crop, readability, and layer overlap uncertainty | Tune placement or accept the static placement contract |
| Inspect BN-04 frames | YMM4 is not available but visual review is possible | Pitch-update readability uncertainty | Decide whether clip export is necessary |
| Advance BN-04 clip export | Manual preview and frame inspection are acceptable | Codec/timing uncertainty | Build a clip manifest/readback without claiming creative acceptance |
| Audit real source replacement | Sample artifacts are accepted as a route | Sample-only provenance uncertainty | Plan source mapping before real episode ingest |

Do not claim render proof, creative acceptance, publish readiness, real episode
sourcing, or mainline integration from the current artifacts.
