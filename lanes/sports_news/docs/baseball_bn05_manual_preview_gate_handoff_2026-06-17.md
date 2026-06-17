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

## BN-05 state to resume

| Area | Current state | What it means |
| --- | --- | --- |
| Placement manifest | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_manifest.json` exists | BN-03 static PNG was inserted into a minimal proof project as planned |
| Placement readback | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_readback.json` has `status: passed` and no failed checks | Timing, layer, canvas, zoom, file path, and hashes match the contract mechanically |
| Proof project | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof.ymmp` exists | This is the review target for YMM4 manual preview only |
| Manual screenshot | `samples/_probe/baseball/placement/baseball_pitch_event_p05_yymm4_preview_screenshot.png` is absent | Human preview is still required before placement acceptance |
| PASS/FIX memo | not recorded | The gate cannot be closed from mechanical readback alone |

The current blocker is narrow: open the proof `.ymmp` in YMM4, inspect frame
`1560` / `00:26.00`, and return one screenshot plus `PASS` or `FIX`.

## Review artifact identity and access

| Artifact | Identity | Access | Validation |
| --- | --- | --- | --- |
| BN-05 proof `.ymmp` | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof.ymmp` | From repo root: `Start-Process .\samples\_probe\baseball\placement\baseball_pitch_event_p05_placement_proof.ymmp` | Readback `status: passed`; proof sha256 `69e4b0f6b03fa66116a9f8f480576f894d3adb094774227cb2b1b7c441be8983` |
| BN-05 manifest | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_manifest.json` | Reference-only; read it from repo | Connects contract, static PNG, seed `.ymmp`, proof `.ymmp`, readback, and handoff |
| BN-05 readback | `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_readback.json` | Reference-only; read it from repo | All checks true, failed checks empty |
| Manual checklist | `lanes/sports_news/docs/baseball_manual_preview_hands_on_2026-05-26.md` | Open as Markdown before YMM4 review | Defines frame `1560`, time `00:26.00`, PASS, FIX, and return payload |
| Progress screenshot slot | `samples/_probe/baseball/placement/baseball_pitch_event_p05_yymm4_preview_screenshot.png` | Not present yet | Capture here when the manual preview is returned |

## Required human return

Return exactly the minimum needed to close or tune BN-05:

1. One YMM4 preview screenshot at frame `1560` / time `00:26.00`.
2. A short `PASS` or `FIX` memo.
3. If `PASS`, state that the diagnostic placement is acceptable for BN-05 gate
   purposes only.
4. If `FIX`, identify the smallest visible issue to tune: crop, text size,
   layer overlap, or timing drift.

`PASS` does not mean render completion, production proof, creative final
acceptance, publish readiness, or real episode suitability.

## Agent continuation after the human return

| Returned signal | Next agent move | What stays closed |
| --- | --- | --- |
| `PASS` plus screenshot | Record the screenshot in `docs/PROGRESS_SCREENSHOT_INDEX.md`, preserve diagnostic/review-only wording, and mark BN-05 placement acceptance as gate-only | render, production, publishing, YouTube, real source, clip export |
| `FIX` plus screenshot/memo | Tune the placement contract once, rebuild proof/readback, run BN-05 tests, and ask for one recheck only if needed | unrelated layout redesign, animation export, production claims |
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

## Boundaries preserved

No force push, merge, rebase, reset, PR, mainline integration, G-27 work, RSS,
NotebookLM, publishing, YouTube, external publish, real source footage, official
materials, real player images, AI-generated player images, clip export, video
generation, TTS, thumbnail work, YMM4 render claim, creative final acceptance,
or production proof was performed for this handoff.
