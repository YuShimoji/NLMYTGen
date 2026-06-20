# Newsroom Review Console Consumer v1 - 2026-06-20

Artifact id: `newsroom_review_console_consumer_v1_2026_06_20`

This records the first read-only Review Console consumer for the synthetic
newsroom handoff packet and G-28 slot-linkage readback.

## Scope

The consumer displays existing fixture/readback state only. It does not mutate
the packet, edit `.ymmp`, fetch external sources, touch `newsroom-yt-pipeline`,
create renders, approve rights, mark production visuals approved, or mark YMM4
transfer ready.

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
| handoff contract | `docs/integration/NEWSROOM_TO_NLMYTGEN_HANDOFF_CONTRACT.md` |
| validator readback | `docs/verification/NEWSROOM_HANDOFF_VALIDATOR_V1_2026-06-20.md` |
| slot-linkage proof readback | `docs/verification/NEWSROOM_G28_SLOT_LINKAGE_PROOF_V1_2026-06-20.md` |

## Displayed Readback

The panel exposes:

- `episode_id`, title, artifact id, contract version, fixture kind, and
  editorial status
- validator status, transfer status, review-surface readiness, YMM4 readiness,
  production visual approval state, external-fetch state, and raw-source state
- rights/provenance summary: clearance state, allowed uses, blocked uses, risk
  flags, source owner, and source-discovery owner
- review warnings and downstream readiness blockers
- source note, script beat, visual plan, G-28 hint, slot-linkage, and visual-gap
  counts
- G-28 slot-linkage rows with beat id, visual id, selected slot, source notes,
  allowed-slot result, reference review surface, transfer state, and production
  approval flag
- artifact inventory for the packet, readback, contract, and verification docs

## Boundary Notes

Blocked transfer is displayed as the intended safe state, not as a UI failure.
`production_visual_approval=false`, `ymm4_transfer_ready=false`,
`external_fetch=false`, and `raw_source_material=false` are shown near the top
as positive guardrails.

## Validation Readback

- JS syntax: `node --check gui/renderer.js`
- JS syntax: `node --check gui/review_console_dom_smoke.js`
- DOM smoke: `.\gui\node_modules\.bin\electron.cmd .\gui\review_console_dom_smoke.js`
- JSON parse: `samples/_probe/newsroom_handoff/minimal_episode_packet.json` and `samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json`
- Validator: `uv run python -m src.cli.main validate-newsroom-handoff samples/_probe/newsroom_handoff/minimal_episode_packet.json --format json`
- Slot-linkage proof: `uv run python -m src.cli.main prove-newsroom-g28-slot-linkage samples/_probe/newsroom_handoff/minimal_episode_packet.json --format json`
- Focused Python tests: `uv run --with pytest pytest tests/test_newsroom_handoff_validator.py`

Expected DOM smoke signal:

`newsroom handoff diagnostics visible`

Observed DOM smoke result:

`G-27 review console DOM smoke OK: 11 timeline segments; 9 G-27 proof frames; 3 pipeline smoke topics / 9 smoke beats visible through GUI; G-28 diagnostic ingest panel visible; newsroom handoff diagnostics visible; save payload OK`

Expected focused Python result:

`14 passed`

## Next Safe Use

Use this consumer as the human-facing readback for synthetic upstream newsroom
packet state. A later slice may add transfer-planning proof, but that must stay
non-YMM4 and must not approve production, source fetch, rights, render, or
publication state.
