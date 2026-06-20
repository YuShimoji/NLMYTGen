# Newsroom Review Console Planning Panel v1 - 2026-06-20

Artifact id: `newsroom_review_console_planning_panel_v1_2026_06_20`

This records the read-only Review Console planning panel for the synthetic
newsroom transfer-planning proof.

## Scope

The panel displays existing transfer-planning readback state only. It does not
mutate the packet, edit `.ymmp`, generate YMM4 carriers, fetch external sources,
touch `newsroom-yt-pipeline`, create renders, approve rights, mark production
visuals approved, or mark YMM4 transfer ready.

## Review Access

Open the Electron Review Console and switch to the Review tab:

```powershell
cd gui
npm start
```

Target panel:

`#newsroom-handoff-review`

DOM smoke command:

```powershell
.\gui\node_modules\.bin\electron.cmd .\gui\review_console_dom_smoke.js
```

## Inputs

| Input | Path |
| --- | --- |
| synthetic handoff packet | `samples/_probe/newsroom_handoff/minimal_episode_packet.json` |
| slot-linkage readback | `samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json` |
| transfer-planning readback | `samples/_probe/newsroom_handoff/transfer_planning_readback.json` |
| transfer-planning proof doc | `docs/verification/NEWSROOM_TRANSFER_PLANNING_PROOF_V1_2026-06-20.md` |
| handoff contract | `docs/integration/NEWSROOM_TO_NLMYTGEN_HANDOFF_CONTRACT.md` |

## Displayed Readback

The panel exposes:

- transfer-planning status, transfer status, validator status, slot-linkage
  status, Review Console visibility, production/YMM4 approval state, blocker
  count, unlock requirement count, and warning count
- transfer candidate summary, currently stating that the fixture is not a
  transfer candidate yet
- grouped blockers for rights/provenance, media/source availability, review
  approval, visual readiness, and downstream/YMM4 readiness
- unlock requirements required before limited transfer can be considered
- prohibited next actions, including `.ymmp` generation, render generation,
  external fetch, and production approval
- allowed next actions, including real packet readiness checklist,
  fixture/schema refinement, and read-only planning panel review
- artifact inventory for the packet, slot-linkage readback, transfer-planning
  readback, and verification docs

## Boundary Notes

Blocked transfer is displayed as the intended safe state, not as a UI failure.
The panel distinguishes validator status, slot-linkage status,
transfer-planning status, and production/YMM4 approval state. It keeps
production/YMM4 approval at `not_approved`.

## Validation Readback

- JS syntax: `node --check gui/renderer.js`
- JS syntax: `node --check gui/review_console_dom_smoke.js`
- DOM smoke: `.\gui\node_modules\.bin\electron.cmd .\gui\review_console_dom_smoke.js`
- JSON parse: `samples/_probe/newsroom_handoff/minimal_episode_packet.json`,
  `samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json`, and
  `samples/_probe/newsroom_handoff/transfer_planning_readback.json`
- Validator: `uv run python -m src.cli.main validate-newsroom-handoff samples/_probe/newsroom_handoff/minimal_episode_packet.json --format json`
- Slot-linkage proof: `uv run python -m src.cli.main prove-newsroom-g28-slot-linkage samples/_probe/newsroom_handoff/minimal_episode_packet.json --format json`
- Transfer-planning proof: `uv run python -m src.cli.main plan-newsroom-transfer samples/_probe/newsroom_handoff/minimal_episode_packet.json --slot-linkage samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json --format json`
- Focused Python tests: `uv run --with pytest pytest tests/test_newsroom_handoff_validator.py`

Expected DOM smoke signal:

`newsroom transfer planning panel visible`

Observed DOM smoke result:

`G-27 review console DOM smoke OK: 11 timeline segments; 9 G-27 proof frames; 3 pipeline smoke topics / 9 smoke beats visible through GUI; G-28 diagnostic ingest panel visible; newsroom transfer planning panel visible; save payload OK`

Expected transfer-planning state:

`status=blocked`, `transfer_status=blocked`, `blockers=14`,
`unlock_requirements=14`, `errors=0`, `warnings=3`

Observed focused Python result:

`19 passed`

## Next Safe Use

Use this panel as the human-facing readback for transfer-planning state before a
future real packet readiness checklist. That later checklist must remain
read-only until rights, media/source availability, review approval, visual
readiness, and downstream/YMM4 readiness blockers are cleared.
