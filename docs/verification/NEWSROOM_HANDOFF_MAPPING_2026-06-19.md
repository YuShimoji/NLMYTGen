# Newsroom Handoff Mapping Readback - 2026-06-19

Artifact id: `newsroom_handoff_mapping_readback_2026_06_19`

This readback explains how a newsroom-produced packet is received by
NLMYTGen without moving upstream source ingestion into this repository.

Input fixture:
`samples/_probe/newsroom_handoff/minimal_episode_packet.json`

Contract:
`docs/integration/NEWSROOM_TO_NLMYTGEN_HANDOFF_CONTRACT.md`

## Field Mapping

| Newsroom packet field | NLMYTGen receiving concept | Review / proof surface | Transfer meaning |
| --- | --- | --- | --- |
| `artifact_id`, `contract_version`, `episode_id` | Stable intake identity | Contract readback and Review Console header | Required before any downstream packet can be trusted. |
| `title`, `topic_summary`, `episode_metadata` | Episode overview and ScriptIR packet context | Human review digest and proof summary | Provides context only; it does not approve editorial direction. |
| `source_notes` | Evidence reference layer for ScriptIR-like beats | Source notes panel / material ledger summary | Source ids can be cited; NLMYTGen must not fetch or expand them. |
| `provenance` | Source ownership and material inclusion boundary | Provenance warning surface | Blocks transfer if raw material or ownership is unclear. |
| `rights_summary` | Rights and use gate | Review warning surface and YMM4 readiness gate | Blocks transfer when clearance is synthetic, unknown, restricted, or missing. |
| `notebooklm_packet` | NotebookLM seed or transcript-prep context | Script seed readback | NLMYTGen may transform received text, but does not automate NotebookLM or build source packs. |
| `script_beats` | ScriptIR-like section, claim, evidence, and density units | Script structure readback | Beats become script planning units only after evidence refs resolve. |
| `visual_plan` | VisualIR-like beat-linked visual concepts | Visual plan readback and G-28 route summary | Visual concepts become candidates for G-28 review, not YMM4 geometry. |
| `g28_slot_hints` | G-28 semantic object slot hints | G-28 object catalog readback | Hints must match object catalog names before visual review or transfer planning. |
| `review_warnings` | Human-readable blockers and cautions | Review Console / proof warning list | Blocking warnings must keep YMM4 transfer closed. |
| `downstream_readiness` | Fail-closed layer readiness | Handoff gate summary | YMM4 transfer remains closed unless all required layers and rights are ready. |

## ScriptIR-Like Readback

`script_beats` are the receiving layer for ScriptIR-like structure:

| Packet element | ScriptIR-like mapping | Validation expectation |
| --- | --- | --- |
| `beat_id` | Stable section or beat id | Unique within the packet. |
| `intent` | Narrative role such as setup, mechanism, caution, or close | Present and bounded to a useful editorial role. |
| `claim` | Core spoken or explanatory claim | Present; no raw article body required. |
| `evidence_refs` | References to `source_notes.source_id` | Every reference resolves or the beat states why evidence is absent. |
| `scriptir_hint.section` | Hook / body / closing or similar script region | Used for review grouping only. |
| `scriptir_hint.duration_seconds_target` | Timing hint for later script shaping | Advisory until a real timing workflow is opened. |
| `scriptir_hint.density` | Reading / explanation density hint | Advisory for review; not a render or timing proof. |

## VisualIR And G-28 Readback

`visual_plan` and `g28_slot_hints` are the receiving layer for VisualIR and
G-28 planning.

| Packet element | VisualIR / G-28 mapping | Validation expectation |
| --- | --- | --- |
| `visual_plan.visual_id` | Stable visual unit | Unique and referenced by slot hints. |
| `visual_plan.beat_id` | Link from visual unit to script beat | Resolves to a known `script_beats.beat_id`. |
| `visual_plan.visualir_concept` | Human-readable visual intent | Present and bounded; no asset fetch implied. |
| `visual_plan.layout_candidate` | G-28 prototype family hint | Uses an existing or reviewable layout family. |
| `visual_plan.asset_policy` | Placeholder, approved asset, or abstract-only policy | Must be explicit before transfer planning. |
| `visual_plan.content_slots` | Expected semantic objects | Each slot should have a corresponding G-28 hint when transfer planning is considered. |
| `g28_slot_hints.object_catalog_slot` | G-28 object catalog slot | Must match the accepted catalog vocabulary. |
| `g28_slot_hints.semantic_role` | What the slot means in the episode | Must not imply real media that is absent. |
| `g28_slot_hints.transfer_note` | Transfer caution for later YMM4 planning | Must carry rights, provenance, or subtitle reserve warnings forward. |

Known G-28 object catalog names used by this slice:

`image_slot`, `screenshot_slot`, `footage_slot`, `highlight_box`, `arrow`,
`leader_line`, `label_chip`, `callout_box`, `lower_third_telop`,
`source_note`, `quote_card`, `comparison_panel`, `table_row`,
`host_placeholder`, and `caption_reserve`.

## Review Console And Proof Surface Placement

| Surface | Fields to show | Why it matters |
| --- | --- | --- |
| Intake header | `artifact_id`, `contract_version`, `episode_id`, `title` | Lets the reviewer know which upstream packet is under review. |
| Source / material ledger summary | `source_notes`, `provenance` | Shows source ids and ownership without exposing raw sources or fetch routes. |
| Rights warning area | `rights_summary`, blocking `review_warnings` | Keeps publication, render, and YMM4 transfer fail-closed. |
| Script readback | `script_beats` with resolved `evidence_refs` | Shows whether the script structure is usable downstream. |
| Visual readback | `visual_plan`, `g28_slot_hints` | Shows which VisualIR / G-28 slots can be reviewed next. |
| Handoff gate | `downstream_readiness` | Makes missing fields and transfer blockers explicit. |

## YMM4 Transfer Blockers

The packet must block YMM4 transfer when any of these fields are missing,
unknown, contradictory, or marked synthetic-only:

| Blocking area | Missing or invalid condition | Effect |
| --- | --- | --- |
| Identity | `artifact_id`, `contract_version`, or `episode_id` missing | Packet cannot be trusted as an intake artifact. |
| Evidence | `source_notes` missing while beats cite evidence | ScriptIR-like beat readback is incomplete. |
| Evidence refs | Beat `evidence_refs` point to unknown source ids | Review Console must show unresolved evidence. |
| Provenance | Source owner, raw material inclusion, or source discovery owner unclear | Rights/provenance warning blocks transfer. |
| Rights | `rights_summary.clearance_state` missing, unknown, restricted, or synthetic-only | YMM4 transfer remains closed. |
| Visual plan | Visuals missing, not linked to beats, or using unclear asset policy | VisualIR / G-28 planning cannot proceed. |
| G-28 slots | Required visual slots lack known object catalog names | G-28 review is incomplete. |
| Warnings | Any warning has `blocks_ymm4_transfer=true` | Transfer remains closed until resolved upstream or by human review. |
| Readiness | `downstream_readiness.ymm4_transfer_ready` is true while blockers exist | Treat as contradictory and fail closed. |

## Explicitly Upstream-Only

NLMYTGen must not reimplement or absorb these responsibilities in this slice:

- RSS, OPML, Inoreader, reader cleanup, source discovery, and topic clustering.
- Article fetching, scraping, browser automation, external downloading, or
  live source ingest.
- Raw source storage, screenshots, footage, real URLs, tokens, raw article
  bodies, or private source strings.
- Rights clearance, publication approval, and final editorial judgement.
- NotebookLM source pack construction or NotebookLM automation.

NLMYTGen only receives a portable export, copy-in artifact, or read-only
reference and maps it into downstream transformation and review surfaces.

## Artifact Readiness

| Artifact | Repository path | Access / reference path | Validation result | Review status | Downstream next use |
| --- | --- | --- | --- | --- | --- |
| `newsroom_to_nlmytgen_handoff_contract_v1_11` | `docs/integration/NEWSROOM_TO_NLMYTGEN_HANDOFF_CONTRACT.md` | Markdown contract in this repo | Local path, diff, and conflict-marker checks passed in the slice validation run. | Ready for supervisor review. | Defines the stable NLMYTGen-side receiving boundary. |
| `newsroom_handoff_minimal_episode_packet_v1` | `samples/_probe/newsroom_handoff/minimal_episode_packet.json` | JSON fixture in this repo | JSON parse and source / beat / visual / G-28 slot reference checks passed in the slice validation run. | Synthetic fixture only; no publication review. | Provides a minimal packet for validator or G-28 linkage follow-up. |
| `newsroom_handoff_mapping_readback_2026_06_19` | `docs/verification/NEWSROOM_HANDOFF_MAPPING_2026-06-19.md` | Markdown verification artifact in this repo | Local path, diff, and conflict-marker checks passed in the slice validation run. | Ready for supervisor review. | Explains ScriptIR / VisualIR / G-28 / Review Console / YMM4 gate mapping. |

## Boundary Confirmation

This slice creates docs and a synthetic JSON fixture only. It does not modify
`newsroom-yt-pipeline`, call external APIs, fetch sources, scrape pages, use
real news data, include real copyrighted article text, include URLs, touch
`.ymmp` files, create render outputs, regenerate YMM4 carriers, approve rights,
or change production state.
