# Baseball BN-05 manual preview gate handoff (2026-06-17)

This handoff preserves the current Baseball sidequest context so another
terminal can resume without reconstructing state from chat. It stays on the
Baseball branch and does not change mainline `runtime-state.md`, G-27, RSS,
NotebookLM, publishing, YouTube, real source intake, clip export, TTS,
thumbnail work, render proof, creative final acceptance, or production proof.

## Restart position

| Item | Current state |
| --- | --- |
| Repository | `C:\Users\PLANNER007\NLMYTGen-baseball-sidequest` |
| Branch | `codex/baseball-bn02-visual-data` |
| Upstream | `origin/codex/baseball-bn02-visual-data` |
| Pre-handoff baseline HEAD | `7e5b3ee docs: add baseball foundation rebaseline` |
| Baseline containment | `7e5b3ee` is contained by local and remote Baseball branch |
| Pre-edit upstream parity | `0 0` |
| Pre-edit worktree | clean |
| Active gate | BN-05 manual YMM4 preview |

After this document is committed and pushed, a new terminal should run
`git log -1 --oneline` for the exact current handoff commit. The baseline above
records the verified state before writing this handoff.

Use this from a new terminal:

```powershell
cd C:\Users\PLANNER007\NLMYTGen-baseball-sidequest
git fetch --prune origin
git checkout codex/baseball-bn02-visual-data
git pull --ff-only origin codex/baseball-bn02-visual-data
git status --short --branch
git rev-list --left-right --count "HEAD...@{u}"
```

Expected result after pull: clean
`## codex/baseball-bn02-visual-data...origin/codex/baseball-bn02-visual-data`
and upstream parity `0 0`.

## 2026-06-18 asset resolution fix

This handoff was refreshed after a YMM4 preview attempt showed note-like item
text but not the Baseball PNG. The likely cause was the proof `.ymmp` using a
repo-root-relative media path that YMM4 did not resolve when opening the project
from the placement directory.

The source proof now stores the image path as
`../static/baseball_pitch_event_p05.png` and declares
`path_resolution_base: proof_ymmp_directory`. The readback checks now fail if
that relative path does not resolve to
`samples/_probe/baseball/static/baseball_pitch_event_p05.png`, if the resolved
file is missing, or if the resolved file hash does not match the source PNG.

If YMM4 still does not display the image from the tracked proof, use the local
launcher. It writes an ignored local copy under `_tmp/baseball_bn05_preview/`
with an absolute `ImageItem.FilePath` for this machine:

```powershell
powershell -ExecutionPolicy Bypass -File .\lanes\sports_news\scripts\open_baseball_bn05_preview.ps1
```

## BN-05 state to resume

| Area | Current state | What it means |
| --- | --- | --- |
| Placement manifest | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_manifest.json` exists | BN-03 static PNG was inserted into a minimal proof project as planned |
| Placement readback | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_readback.json` has `status: passed` and no failed checks | Timing, layer, canvas, zoom, file path, and hashes match the contract mechanically |
| Proof project | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof.ymmp` exists | This is the review target for YMM4 manual preview only |
| Manual screenshot | `samples/_probe/baseball/placement/baseball_pitch_event_p05_yymm4_preview_screenshot.png` is absent | Human preview is still required before placement acceptance |
| Freeform review memo | not recorded | The gate cannot be closed from mechanical readback alone |

The current blocker is narrow: open the proof `.ymmp` in YMM4, inspect frame
`1560` / `00:26.00`, and return one screenshot plus any short freeform comment.
Fixed labels are not required.

## Review artifact identity and access

| Artifact | Identity | Access | Validation |
| --- | --- | --- | --- |
| BN-05 proof `.ymmp` | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof.ymmp` | From repo root: `Start-Process .\samples\_probe\baseball\placement\baseball_pitch_event_p05_placement_proof.ymmp` | Readback `status: passed`; ImageItem FilePath resolves from the proof directory to `samples/_probe/baseball/static/baseball_pitch_event_p05.png` |
| BN-05 local preview launcher | `lanes/sports_news/scripts/open_baseball_bn05_preview.ps1` | From repo root: `powershell -ExecutionPolicy Bypass -File .\lanes\sports_news\scripts\open_baseball_bn05_preview.ps1` | Creates ignored `_tmp/baseball_bn05_preview/baseball_pitch_event_p05_placement_proof.local.ymmp` with an absolute PNG path for YMM4 installations that do not resolve relative media paths |
| BN-05 manifest | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_manifest.json` | Reference-only; read it from repo | Connects contract, static PNG, seed `.ymmp`, proof `.ymmp`, readback, and handoff |
| BN-05 readback | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_readback.json` | Reference-only; read it from repo | All checks true, failed checks empty |
| Manual checklist | `lanes/sports_news/docs/baseball_manual_preview_hands_on_2026-05-26.md` | Open as Markdown before YMM4 review | Defines frame `1560`, time `00:26.00`, image-visible check, and freeform return payload |
| Progress screenshot slot | `samples/_probe/baseball/placement/baseball_pitch_event_p05_yymm4_preview_screenshot.png` | Not present yet | Capture here when the manual preview is returned |

## Required human return

Return exactly the minimum needed to close or tune BN-05:

1. One YMM4 preview screenshot at frame `1560` / time `00:26.00`.
2. A short freeform memo. Fixed labels are not required.
3. If the proof is acceptable, state that naturally.
4. If something is wrong, identify the smallest visible issue to tune: image
   still missing, crop, text size, layer overlap, or timing drift.

Acceptance does not mean render completion, production proof, creative final
acceptance, publish readiness, or real episode suitability.

## Agent continuation after the human return

| Returned signal | Next agent move | What stays closed |
| --- | --- | --- |
| Acceptable freeform review plus screenshot | Record the screenshot in `docs/PROGRESS_SCREENSHOT_INDEX.md`, preserve diagnostic/review-only wording, and mark BN-05 placement acceptance as gate-only | render, production, publishing, YouTube, real source, clip export |
| Problem report plus screenshot/memo | Tune the placement contract once, rebuild proof/readback, run BN-05 tests, and ask for one recheck only if needed | unrelated layout redesign, animation export, production claims |
| No screenshot | Keep this handoff as the restart point and do not claim BN-05 acceptance | all production and publish lanes |

## Validation already run on 2026-06-17

| Check | Result |
| --- | --- |
| `git fetch --prune origin` | success |
| `git status --short --branch` | clean `codex/baseball-bn02-visual-data...origin/codex/baseball-bn02-visual-data` |
| `git rev-list --left-right --count "HEAD...@{u}"` | `0 0` |
| `git branch -a --contains 7e5b3ee` | local and remote Baseball branch contain the baseline |
| `git diff --stat` | no diff before handoff edits |
| `git diff --check` | passed |
| `Test-Path samples/_probe/baseball/placement/baseball_pitch_event_p05_yymm4_preview_screenshot.png` | `False` |
| `uv run pytest tests/test_baseball_yymm4_placement_contract.py tests/test_baseball_yymm4_placement_proof.py` | `8 passed` |

## Validation already run on 2026-06-18

| Check | Result |
| --- | --- |
| `node lanes/sports_news/scripts/build_baseball_yymm4_placement_proof.js` | passed; regenerated proof, manifest, readback, and handoff with proof-directory-relative media path |
| `powershell -ExecutionPolicy Bypass -File lanes/sports_news/scripts/open_baseball_bn05_preview.ps1 -NoOpen` | passed; created ignored local proof copy with absolute PNG path |
| `pytest tests/test_baseball_yymm4_placement_contract.py tests/test_baseball_yymm4_placement_proof.py` | `8 passed` |
| `git diff --check` | passed after line-ending cleanup |

## Boundaries preserved

No force push, merge, rebase, reset, PR, mainline integration, G-27 work, RSS,
NotebookLM, publishing, YouTube, external publish, real source footage, official
materials, real player images, AI-generated player images, clip export, video
generation, TTS, thumbnail work, YMM4 render claim, creative final acceptance,
or production proof was performed for this handoff.
