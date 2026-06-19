# Newsroom To NLMYTGen Handoff Contract

Contract id: `newsroom_to_nlmytgen_handoff_contract_v1_11`

This document defines the NLMYTGen-side receiving contract for an upstream
`newsroom-yt-pipeline` episode packet. The packet is an artifact boundary, not a
shared runtime. NLMYTGen receives already-prepared editorial output and maps it
into NotebookLM seed material, ScriptIR-like beat concepts, VisualIR planning,
G-28 semantic object slots, review warnings, and downstream YMM4 readiness
checks.

This contract does not authorize NLMYTGen to implement RSS, OPML, Inoreader,
topic clustering, article fetching, scraping, external source downloading,
rights clearance, publication, rendering, or YMM4 transfer. Those remain
outside this slice.

## Artifact Envelope

| Field | Required | Meaning | NLMYTGen use |
| --- | --- | --- | --- |
| `artifact_id` | yes | Stable packet artifact id. | Review and provenance readback identity. |
| `contract_version` | yes | Contract version used by the exported packet. | Compatibility check before intake. |
| `episode_id` | yes | Stable episode id from newsroom. | ScriptIR / VisualIR / proof grouping key. |
| `title` | yes | Working episode title. | Review surface and downstream packet label. |
| `topic_summary` | yes | Short editorial topic summary. | NotebookLM seed and review digest context. |
| `episode_metadata` | yes | Series, audience, expected duration, language, and status. | Intake overview and downstream naming. |
| `source_notes` | yes | Sanitized notes derived from upstream source work. | Evidence reference layer, not fetch input. |
| `provenance` | yes | Who created the packet and what material is included or omitted. | Review Console / proof warnings. |
| `rights_summary` | yes | Rights status, allowed uses, blocked uses, and risk flags. | YMM4 transfer gate and review warnings. |
| `notebooklm_packet` | yes | NotebookLM seed or transcript-prep summary. | Script seed intake, not NotebookLM automation. |
| `script_beats` | yes | Beat-level editorial structure and evidence references. | ScriptIR-like section / claim / evidence mapping. |
| `visual_plan` | yes | Beat-linked visual intentions. | VisualIR-like planning and G-28 route selection. |
| `g28_slot_hints` | yes | Semantic object slot hints using G-28 catalog names. | G-28 review and later transfer planning. |
| `review_warnings` | yes | Human-readable warnings and blockers. | Review Console / proof surfaces. |
| `downstream_readiness` | yes | Booleans and blockers for NotebookLM, ScriptIR, VisualIR, G-28, and YMM4. | Fail-closed handoff gate. |

## Responsibility Boundary

| Responsibility | newsroom-yt-pipeline owner role | NLMYTGen owner role | Handoff field or artifact | Validation expectation | Out-of-scope notes |
| --- | --- | --- | --- | --- | --- |
| Episode metadata | Assign episode identity, working title, audience, language, and editorial status. | Preserve identity and display it on review/proof surfaces. | `episode_id`, `title`, `episode_metadata` | Required fields are present and stable across the packet. | NLMYTGen does not choose upstream topic or editorial lane. |
| Source packet / source notes | Produce sanitized source notes, source ids, summaries, and evidence references. | Read the notes as evidence metadata and link beats to source ids. | `source_notes` | Notes have ids; script beats reference only known source ids. | NLMYTGen must not fetch, scrape, download, or expand source material. |
| Provenance and rights summary | State source collection owner, included material class, clearance state, restrictions, and risk flags. | Surface provenance and rights warnings; block YMM4 transfer when clearance is missing or restricted. | `provenance`, `rights_summary`, `review_warnings` | Provenance owner is explicit; raw material inclusion and rights state are explicit. | Rights clearance and raw material storage remain upstream or human-owned. |
| NotebookLM packet / transcript seed | Prepare a packet or seed text suitable for NotebookLM-oriented script work. | Treat the seed as input context for script transformation and review, not as an instruction to automate NotebookLM. | `notebooklm_packet` | Seed exists, is bounded, and states constraints. | NLMYTGen does not run NotebookLM, create source packs, or select live sources. |
| Script beat structure | Export beats with intent, claim, evidence refs, and time/density hints. | Map beats to ScriptIR-like concepts and check missing claim/evidence structure. | `script_beats` | Every beat has an id, intent, claim, and known evidence refs or an explicit no-evidence reason. | This is not a full script generator contract. |
| Visual plan | Provide beat-linked visual concepts, layout candidates, and placeholder/asset policy. | Map concepts to VisualIR-like objects and G-28 review candidates. | `visual_plan` | Every visual references a known beat and declares asset policy. | No screenshots, footage, maps, or media are pulled by NLMYTGen. |
| G-28 semantic slot hints | Name intended object slots using the G-28 object catalog vocabulary. | Validate slot names against known G-28 catalog entries and expose them in review/readback. | `g28_slot_hints` | Slot values use known names such as `image_slot`, `screenshot_slot`, `footage_slot`, `source_note`, `quote_card`, or `caption_reserve`. | Slot hints are semantic planning hints, not YMM4 geometry. |
| Review warnings | Export warnings from upstream source, rights, completeness, or editorial checks. | Show warnings in Review Console / proof surfaces and carry blockers into downstream readiness. | `review_warnings` | Severity, surface, message, and blocking effect are explicit. | Warnings do not become user fixed-label review requirements. |
| Downstream YMM4 handoff readiness | Declare which downstream layers are ready and why any layer is blocked. | Fail closed before YMM4 transfer when required source, rights, script, visual, or slot fields are missing. | `downstream_readiness` | `ymm4_transfer_ready=false` when any required rights/provenance/visual slot condition is missing. | This contract does not create `.ymmp`, render, or approve production. |

## G-28 Slot Vocabulary

The receiving layer should recognize the current G-28 object catalog names as
semantic hints:

`image_slot`, `screenshot_slot`, `footage_slot`, `highlight_box`, `arrow`,
`leader_line`, `label_chip`, `callout_box`, `lower_third_telop`,
`source_note`, `quote_card`, `comparison_panel`, `table_row`,
`host_placeholder`, and `caption_reserve`.

These are content and review slots. They do not specify coordinates, timing,
YMM4 item names, asset paths, or render state.

## Fail-Closed Readiness Rules

NLMYTGen should treat the packet as not ready for YMM4 transfer when any of the
following is true:

- `episode_id`, `contract_version`, or `artifact_id` is missing.
- `source_notes` are absent while script beats cite evidence.
- a script beat references an unknown source id.
- `rights_summary` is missing, unknown, restricted, or only synthetic.
- `provenance.raw_source_material_included` is unclear.
- `visual_plan` is absent or not linked to known beat ids.
- `g28_slot_hints` are absent for visuals that need G-28 review.
- any `review_warnings` entry is marked as blocking for YMM4 transfer.
- `downstream_readiness.ymm4_transfer_ready` is missing or disagrees with the
  explicit blockers.

## Upstream-Only Responsibilities

The following responsibilities stay outside NLMYTGen for this contract:

- RSS, OPML, Inoreader, feed cleanup, source discovery, topic clustering, and
  live source intake.
- Article fetching, scraping, browser automation, external downloading, raw
  screenshot capture, footage capture, and source asset storage.
- Rights clearance, publication approval, final editorial judgement, and source
  material acquisition.
- NotebookLM source pack construction and NotebookLM automation.

NLMYTGen may receive a portable export packet, copy-in artifact, or read-only
reference produced by newsroom, then transform and review it downstream.

## Synthetic Fixture

The minimal non-fetching fixture for this contract is:

`samples/_probe/newsroom_handoff/minimal_episode_packet.json`

It contains fake placeholder content only. It is not a real news packet, not a
publication candidate, and not a media or YMM4 transfer artifact.
