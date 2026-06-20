# Newsroom Real Packet Readiness Checklist v1 - 2026-06-20

Artifact id: `newsroom_real_packet_readiness_checklist_v1_2026_06_20`

This readback defines the NLMYTGen-side checklist for a future real
`newsroom-yt-pipeline` export packet. It is a policy and readiness artifact, not
real packet ingest.

## Scope

The current packet remains synthetic. This checklist does not fetch sources,
open RSS or Inoreader flows, access real URLs, download media, edit `.ymmp`,
generate YMM4 carriers, render media, approve rights, approve production, or
mark YMM4 transfer ready.

## Artifacts

| Artifact | Path |
| --- | --- |
| machine-readable checklist | `samples/_probe/newsroom_handoff/real_packet_readiness_checklist.json` |
| human readback | `docs/verification/NEWSROOM_REAL_PACKET_READINESS_CHECKLIST_V1_2026-06-20.md` |
| synthetic packet fixture | `samples/_probe/newsroom_handoff/minimal_episode_packet.json` |
| slot-linkage readback | `samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json` |
| transfer-planning readback | `samples/_probe/newsroom_handoff/transfer_planning_readback.json` |
| Review Console planning panel | `docs/verification/NEWSROOM_REVIEW_CONSOLE_PLANNING_PANEL_V1_2026-06-20.md` |

## Current State

| Field | Value |
| --- | --- |
| checklist status | checklist-only |
| review status | ready for supervisor review |
| current packet | synthetic fixture only |
| real packet accepted | false |
| rights approval | false |
| production approval | false |
| YMM4 transfer ready | false |

## Required Before NLMYTGen Ingest

These fields must be present before NLMYTGen treats a future export as an intake
packet. Missing required identity, source, script, visual, or readiness data is
an intake failure or a transfer block.

| Packet item | Owner | Current coverage | Failure behavior | Next move |
| --- | --- | --- | --- | --- |
| `episode_id` | newsroom-yt-pipeline | validator | fail | request upstream field |
| `title` | newsroom-yt-pipeline | validator | fail | request upstream field |
| `topic_summary` | newsroom-yt-pipeline | validator | fail | request upstream field |
| `source_notes` | newsroom-yt-pipeline | validator | fail | request upstream field |
| `provenance` | newsroom-yt-pipeline | validator + transfer-planning proof | block transfer | request upstream field |
| `rights_summary` | newsroom-yt-pipeline | validator + transfer-planning proof | block transfer | request upstream field |
| NotebookLM packet or transcript seed | newsroom-yt-pipeline | validator | fail | request upstream field |
| `script_beats` with stable ids | newsroom-yt-pipeline | validator | fail | request upstream field |
| `visual_plan` with stable ids | newsroom-yt-pipeline | validator + slot-linkage proof | fail | request upstream field |
| `g28_slot_hints` | newsroom-yt-pipeline | slot-linkage proof | warn | future validator check |
| `review_warnings` | newsroom-yt-pipeline | validator + transfer-planning proof | block transfer | request upstream field |
| `downstream_readiness` | newsroom-yt-pipeline | validator + transfer-planning proof | block transfer | request upstream field |

## Required Before Transfer Candidate

These checks must pass before a future packet can even be considered as a
limited transfer candidate. They are stricter than ingest readiness.

| Transfer gate | Owner | Current coverage | Failure behavior | Next move |
| --- | --- | --- | --- | --- |
| rights/provenance clearance | human reviewer | transfer-planning proof + Review Console planning panel | block transfer | later Review Card |
| media/source availability | newsroom-yt-pipeline | transfer-planning proof + Review Console planning panel | block transfer | request upstream field |
| review approval status | human reviewer | Review Console planning panel | hold for review | later Review Card |
| visual readiness | NLMYTGen | slot-linkage proof + transfer-planning proof | block transfer | future validator check |
| blocked/prohibited actions resolved | human reviewer | transfer-planning proof | block transfer | keep transfer closed |
| no readiness/blocker contradiction | NLMYTGen | validator + transfer-planning proof | fail | future validator check |

## Optional Enrichments

These fields can improve review quality but must not block packet intake by
themselves.

| Optional item | Owner | Current coverage | Failure behavior | Next move |
| --- | --- | --- | --- | --- |
| editorial priority | newsroom-yt-pipeline | not covered yet | ignore | use if provided |
| visual treatment preference | newsroom-yt-pipeline | not covered yet | ignore | use if provided |
| source confidence | newsroom-yt-pipeline | not covered yet | warn | future validator check |
| reviewer notes | human reviewer | Review Console planning panel | ignore | use if provided |
| localization notes | newsroom-yt-pipeline | not covered yet | ignore | use if provided |
| channel/package metadata | newsroom-yt-pipeline | not covered yet | ignore | use if provided |

## Prohibited Or Out Of Scope For NLMYTGen

These activities must not move into NLMYTGen as part of real packet readiness.

| Prohibited item | Owner outside this slice | Current coverage | Failure behavior | Next move |
| --- | --- | --- | --- | --- |
| RSS/source discovery | newsroom-yt-pipeline | not covered yet | fail | keep outside NLMYTGen |
| article scraping | external/manual | not covered yet | fail | keep outside NLMYTGen |
| Inoreader operation | external/manual | not covered yet | fail | keep outside NLMYTGen |
| source fetching / live source download | external/manual | transfer-planning proof | fail | keep outside NLMYTGen |
| rights acquisition | external/manual | transfer-planning proof | hold for review | later Review Card |
| production approval | human reviewer | Review Console planning panel | block transfer | later Review Card |
| publishing/upload | external/manual | not covered yet | fail | keep outside NLMYTGen |
| external account operations | external/manual | not covered yet | fail | keep outside NLMYTGen |
| YMM4 transfer or `.ymmp` generation | NLMYTGen | transfer-planning proof + Review Console planning panel | block transfer | keep transfer closed |
| render generation | NLMYTGen | transfer-planning proof + Review Console planning panel | block transfer | keep transfer closed |

## Hold For Human Review

These cases require a human planning outcome before transfer-candidate review.
They do not become production approval.

| Hold item | Owner | Current coverage | Failure behavior | Next move |
| --- | --- | --- | --- | --- |
| ambiguous rights | human reviewer | transfer-planning proof | hold for review | later Review Card |
| unclear media availability | newsroom-yt-pipeline | transfer-planning proof | hold for review | request upstream field |
| real screenshots/footage | external/manual | not covered yet | hold for review | later Review Card |
| brand risk | human reviewer | not covered yet | hold for review | later Review Card |
| uncertain citation/quote usage | human reviewer | validator + transfer-planning proof | hold for review | later Review Card |
| visual approval | human reviewer | Review Console planning panel | hold for review | later Review Card |

## Coverage Matrix

| Gate | Already covers | Still policy-only |
| --- | --- | --- |
| validator | required top-level fields, reference integrity, required lists, rights/provenance structure, contradiction checks | richer source-confidence and package metadata checks |
| slot-linkage proof | G-28 slot vocabulary, visual-to-slot linkage, missing visual slot hints | real asset approval and final visual judgement |
| transfer-planning proof | grouped blockers, unlock requirements, prohibited actions, readiness contradictions | human approval outcomes and real media clearance |
| Review Console planning panel | read-only display of blocked transfer, blockers, unlocks, and artifacts | future freeform human review intake |
| not covered yet | optional enrichments and external/manual account or rights work | future upstream export delta request |

## Upstream Export Expectation

If a future real export is missing a required field, NLMYTGen should ask
`newsroom-yt-pipeline` for a corrected export packet instead of fabricating the
field locally. If the gap is rights, media availability, real footage, quote
usage, brand risk, or visual approval, NLMYTGen should hold transfer planning for
human review.

## Validation Readback

- JSON parse: `samples/_probe/newsroom_handoff/real_packet_readiness_checklist.json`
- Required categories: required-before-ingest, required-before-transfer,
  optional enrichments, prohibited/out-of-scope, human-review hold
- Required item fields: owner, current coverage, failure behavior, next move
- Prohibited coverage: RSS/source discovery, source fetching, YMM4 transfer,
  `.ymmp` generation, render generation, and publishing/upload
- Real URL scan: none expected
- Existing validator: `uv run python -m src.cli.main validate-newsroom-handoff samples/_probe/newsroom_handoff/minimal_episode_packet.json --format json`
- Slot-linkage proof: `uv run python -m src.cli.main prove-newsroom-g28-slot-linkage samples/_probe/newsroom_handoff/minimal_episode_packet.json --format json`
- Transfer-planning proof: `uv run python -m src.cli.main plan-newsroom-transfer samples/_probe/newsroom_handoff/minimal_episode_packet.json --slot-linkage samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json --format json`
- Focused checklist tests: `uv run --with pytest pytest tests/test_newsroom_real_packet_readiness_checklist.py`

Expected focused checklist result:

`5 passed`

Observed validation result:

- JSON parse: `artifact=newsroom_real_packet_readiness_checklist_v1_2026_06_20`,
  `categories=5`, `items=40`, `real_packet_accepted=False`,
  `ymm4_transfer_ready=False`
- Validator: `status=passed`, `transfer_status=blocked`, `errors=0`
- Slot-linkage proof: `status=passed_with_warnings`, `transfer_status=blocked`,
  `errors=0`, `warnings=2`
- Transfer-planning proof: `status=blocked`, `transfer_status=blocked`,
  `blockers=14`, `unlock_requirements=14`, `errors=0`, `warnings=3`
- Focused checklist test: `5 passed`
- Combined newsroom focused tests: `24 passed`
- Real URL scan: none

## Downstream Next Use

Use this checklist before requesting a real export delta from
`newsroom-yt-pipeline` or before adding future validator checks. The next safe
slice is an upstream export delta request doc if supervisor review finds gaps.
