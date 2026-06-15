# G-27 Carrier Decision Handoff - 2026-06-04

This is a decision-prep note for `G27_PublicVsBrokerDB`. It is not a carrier
promotion, slot-fill run, render, production timing pass, or creative
acceptance.

## Checked State

| Surface | Current readback | Decision impact |
| --- | --- | --- |
| branch / remote | `master` aligned with `origin/master` at `8f49dcb docs: seal ChatGPT copy-block handoff` | Repo authority is current before the carrier decision work. |
| tracked tree | clean; known untracked `.claude/worktrees/` and `samples/2026-05-16.ymmp` remain local | Do not delete, stage, or promote those untracked paths. |
| production carrier | not received | Production slot-fill remains blocked. |
| diagnostic carrier | `samples/_probe/g24/real_estate_dx_diagnostic_carrier.ymmp` exists with readback `status=passed`, 14 items, no missing required items, `safe_area_check=pass`, `subtitle_clearance_check=pass`, `tonal_system=light-stage` | Useful as evidence for a fast-path promotion decision, but not a production carrier by default. |
| diagnostic boundary | readback/report keep `diagnostic_only=true`, `production_carrier_replaced=false`, `production_readiness_claimed=false`, render/timing/creative acceptance not performed | Must not silently use it as production carrier. |
| local residue sample | `samples/2026-05-16.ymmp` exists locally with 1 timeline and 3 items: `G27PBD_BG`, `G27PBD_Title`, `公開ポータル` | Not a viable carrier candidate; exclude from production carrier path. |
| review decisions | `samples/_probe/g24/real_estate_dx_review_decisions.json` is absent | Blocks GUI decision handback and any downstream classification that depends on accepted/revised/cut scene decisions. |
| screenshot evidence | GUI/proxy screenshots exist for earlier review surfaces, but the checklist return package for a production carrier is not present | Existing screenshots are not enough to accept a production carrier. |

## Carrier Requirements

The stable production carrier must come from
`docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md` or from an explicit
operator decision to promote the diagnostic carrier. It needs:

- carrier `.ymmp` path.
- preview screenshot.
- timeline screenshot.
- representative item property screenshots for:
  - `G27PBD_PublicPanel`
  - `G27PBD_PublicCard1`
  - `G27PBD_BrokerPanel`
  - `G27PBD_Lock`
- light-stage or dark-stage choice.
- short note confirming the bottom caption safe area is clear.
- fixed public card count 2 and broker card count 3.
- required short item names / Remarks using `G27PBD_*`, including retained `G27PBD_Arrow` even if hidden.

## Diagnostic Carrier Promotion Conditions

| Condition | Current diagnostic carrier | Promotion implication |
| --- | --- | --- |
| required `G27PBD_*` items | present, including `PublicPanel`, `PublicCard1`, `BrokerPanel`, `Lock`, `Arrow` | Mechanically promising. |
| public / broker card counts | public 2, broker 3 | Matches checklist count. |
| stage | `light-stage` | Stage is fixed, but operator must explicitly accept it as production carrier stage. |
| safe area / subtitle clearance | readback pass | Mechanically promising, still needs production acceptance decision. |
| Remarks | short G27PBD-style Remarks in readback | Mechanically promising. |
| screenshots | prior proof/review screenshots exist, but not the full checklist return package | Insufficient for silent promotion. |
| boundary flags | `diagnostic_only=true`, `production_carrier_replaced=false` | Promotion requires an explicit new operator decision and updated readback/boundary record. |
| review decisions | absent | Promotion does not by itself resolve missing GUI review decisions. |

Fast path is possible only if the operator explicitly says to promote
`samples/_probe/g24/real_estate_dx_diagnostic_carrier.ymmp` as the production
carrier. The next agent must then create or update a boundary/readback record
that says which checklist conditions are accepted, which screenshot evidence is
accepted or waived, and that the promotion was an operator decision. Until that
happens, the file remains diagnostic-only.

## Safe Path

The safe path is for the human to create or return a minimal YMM4 carrier that
follows the checklist, then return the `.ymmp` path, screenshots, stage choice,
and caption safe-area note. After that, the agent can read back the carrier and
prepare an anchored slot contract.

## What Not To Do Yet

- Do not perform slot-fill.
- Do not render.
- Do not claim production timing.
- Do not claim creative acceptance.
- Do not treat `samples/2026-05-16.ymmp` as a carrier.
- Do not restart RSS / OPML / Inoreader / topic clustering / NotebookLM
  source-pack selection in this repo.
