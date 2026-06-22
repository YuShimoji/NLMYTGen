# Newsroom Review Console Timing Panel v1 - 2026-06-22

Artifact id: `newsroom_review_console_timing_panel_v1_2026_06_22`

This records the read-only Review Console panel that surfaces the diagnostic
caption/timing plan.

## Scope

The Review tab now loads
`samples/_probe/newsroom_handoff/episode_caption_timing_plan_v1.json` alongside
the existing synthetic packet, transfer planning readback, and episode
production capsule. It displays the 68 second provisional timing structure as
two beat ranges, four caption unit ranges, and two visual timing rows.

The panel does not mutate the timing JSON, accept a real packet, fetch sources,
access real URLs, download media, edit `.ymmp`, generate YMM4 carriers, render,
generate TTS/audio, approve rights, approve production, or publish output.

## Review Access

Open the Electron Review Console and switch to the Review tab:

```powershell
cd gui
npm start
```

Target panel:

`#newsroom-handoff-review`

The timing section is headed `Newsroom caption / timing panel`.

## Inputs

| Input | Path |
| --- | --- |
| caption/timing plan | `samples/_probe/newsroom_handoff/episode_caption_timing_plan_v1.json` |
| caption/timing readback | `docs/verification/NEWSROOM_CAPTION_TIMING_PLAN_V1_2026-06-22.md` |
| episode capsule | `samples/_probe/newsroom_handoff/episode_production_capsule_v1.json` |
| episode preview readback | `docs/verification/NEWSROOM_REVIEW_CONSOLE_EPISODE_PREVIEW_V1_2026-06-22.md` |

## Displayed Timing Panel

The panel exposes the timing plan as diagnostic-only and keeps transfer
blocked:

- `total_duration_sec=68`
- `beat_count=2`
- `caption_unit_count=4`
- `visual_count=2`
- `voice_status=not_started`
- `TTS_generated=false`
- `transfer_status=blocked`
- `YMM4_candidate=false`
- beat timing rows for `beat_fake_intro_001` and `beat_fake_claim_001`
- caption rows for all four `cap_*` placeholders with start/end timing,
  max-character targets, line targets, reading-speed notes, and caption reserve
  status
- visual timing rows for `visual_fake_title_card_001` and
  `visual_fake_evidence_card_001` with G-28 slots and caption interference risk
- prohibited next actions including `.ymmp generation`, `render generation`,
  `TTS generation`, and `production approval`
- allowed next actions including caption copy refinement, later transfer
  candidate proof after blockers, and Review Console timing review

## Boundary Notes

This panel is a human timing-review surface, not a public video, not an
importable proof, and not a production acceptance surface. Blocked transfer is
the intended safe state.

## Validation Readback

- JS syntax: `node --check gui/renderer.js`
- JS syntax: `node --check gui/review_console_dom_smoke.js`
- DOM smoke: `.\gui\node_modules\.bin\electron.cmd .\gui\review_console_dom_smoke.js`
- Focused caption/timing tests: `uv run pytest tests/test_newsroom_caption_timing_plan.py`
- Focused capsule tests: `uv run pytest tests/test_newsroom_episode_production_capsule.py`
- JSON parse: `samples/_probe/newsroom_handoff/episode_caption_timing_plan_v1.json`

Expected DOM smoke signal:

`newsroom timing panel visible with 2 beats / 4 captions / 2 visuals`

Observed DOM smoke result:

`G-27 review console DOM smoke OK: 11 timeline segments; 9 G-27 proof frames; 3 pipeline smoke topics / 9 smoke beats visible through GUI; G-28 diagnostic ingest panel visible; newsroom transfer planning panel visible; newsroom episode preview visible with 2 beats / 2 visuals; newsroom timing panel visible with 2 beats / 4 captions / 2 visuals; save payload OK`

Observed focused Python results:

- `tests/test_newsroom_caption_timing_plan.py`: `7 passed`
- `tests/test_newsroom_episode_production_capsule.py`: `7 passed`

## Next Safe Use

Use this panel for supervisor review of timing and caption placeholders before
caption copy refinement. A later transfer-candidate proof must remain blocked
until rights, media/source availability, review approval, visual readiness, and
downstream/YMM4 blockers are resolved.
