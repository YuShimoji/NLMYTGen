# Newsroom Review Console Episode Preview v1 - 2026-06-22

Artifact id: `newsroom_review_console_episode_preview_v1_2026_06_22`

This records the read-only Review Console preview for the diagnostic episode
production capsule.

## Scope

The Review tab now loads
`samples/_probe/newsroom_handoff/episode_production_capsule_v1.json` alongside
the existing synthetic packet, slot-linkage readback, and transfer-planning
readback. It displays one diagnostic episode structure from the adapted fake
packet chain: ScriptIR-like beats, VisualIR units, G-28 slot refs, caption
reserve state, provisional timing, audio/voice status, remaining blockers, and
allowed/prohibited next steps.

The preview does not mutate the packet, accept a real packet, fetch sources,
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

The capsule preview section is headed `Newsroom episode preview`.

## Inputs

| Input | Path |
| --- | --- |
| adapted packet | `samples/_probe/newsroom_handoff/adapted_newsroom_export_packet.json` |
| episode capsule | `samples/_probe/newsroom_handoff/episode_production_capsule_v1.json` |
| capsule readback | `docs/verification/NEWSROOM_EPISODE_PRODUCTION_CAPSULE_V1_2026-06-22.md` |
| synthetic handoff packet | `samples/_probe/newsroom_handoff/minimal_episode_packet.json` |
| slot-linkage readback | `samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json` |
| transfer-planning readback | `samples/_probe/newsroom_handoff/transfer_planning_readback.json` |
| real-packet readiness checklist | `samples/_probe/newsroom_handoff/real_packet_readiness_checklist.json` |

## Displayed Preview

The panel exposes the capsule as diagnostic-only and keeps transfer blocked:

- episode id `episode_fake_nlmytgen_delta_v1`
- title `Fake upstream export delta for NLMYTGen`
- schema `newsroom_episode_production_capsule.v1`
- `production_status=diagnostic_only`
- `capsule_transfer_status=blocked`
- `audio_readiness=not_started`
- `public_video=false`, `ymmp_generated=false`, and `render_generated=false`
- two ScriptIR-like beats and two VisualIR / G-28 preview rows
- total provisional duration `68` seconds
- remaining gaps before importable proof
- next allowed steps limited to Review Console episode preview, caption/timing
  refinement, and a later YMM4 transfer candidate proof only after blockers are
  resolved
- prohibited steps including real source fetch, `.ymmp` generation, YMM4 carrier
  generation, render generation, production approval, publishing, real URL
  access, media download, and public-use approval

## Boundary Notes

This preview is the first human-facing bridge from packet validation toward a
single video structure. It is not a public video, not an importable proof, and
not a production acceptance surface. Blocked transfer is the intended safe
state.

## Validation Readback

- JS syntax: `node --check gui/renderer.js`
- JS syntax: `node --check gui/review_console_dom_smoke.js`
- DOM smoke: `.\gui\node_modules\.bin\electron.cmd .\gui\review_console_dom_smoke.js`
- Focused capsule tests: `uv run pytest tests/test_newsroom_episode_production_capsule.py`
- JSON parse: `samples/_probe/newsroom_handoff/episode_production_capsule_v1.json`

Expected DOM smoke signal:

`newsroom episode preview visible with 2 beats / 2 visuals`

Observed DOM smoke result:

`G-27 review console DOM smoke OK: 11 timeline segments; 9 G-27 proof frames; 3 pipeline smoke topics / 9 smoke beats visible through GUI; G-28 diagnostic ingest panel visible; newsroom transfer planning panel visible; newsroom episode preview visible with 2 beats / 2 visuals; save payload OK`

Observed focused Python result:

`7 passed`

## Next Safe Use

Use this panel for supervisor review of the diagnostic episode shape before any
caption/timing refinement. A later transfer-candidate proof must remain blocked
until rights, media/source availability, review approval, visual readiness, and
downstream/YMM4 blockers are resolved.
