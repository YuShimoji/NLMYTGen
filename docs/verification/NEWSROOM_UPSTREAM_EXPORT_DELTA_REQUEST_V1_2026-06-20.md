# Newsroom Upstream Export Delta Request v1 - 2026-06-20

Artifact id: `newsroom_upstream_export_delta_request_v1_2026_06_20`

This is an NLMYTGen-side request to `newsroom-yt-pipeline` for the next export
bundle delta. It does not implement newsroom export, accept a real packet, fetch
sources, open RSS or Inoreader flows, access live source material, download
media, edit `.ymmp`, generate YMM4 carriers, render media, approve rights,
approve production, or publish/upload output.

## Purpose

The current NLMYTGen packet is still a synthetic fixture. The delta below turns
the real-packet readiness checklist into an upstream-facing export request:
which fields must be emitted, who owns them, which current NLMYTGen consumer
uses them, and how NLMYTGen should fail, warn, block transfer, or hold for
review when they are missing or ambiguous.

Machine-readable request:
`samples/_probe/newsroom_handoff/upstream_export_delta_request.json`

## Current Input Chain

| Layer | Artifact |
| --- | --- |
| handoff contract | `docs/integration/NEWSROOM_TO_NLMYTGEN_HANDOFF_CONTRACT.md` |
| synthetic packet | `samples/_probe/newsroom_handoff/minimal_episode_packet.json` |
| readiness checklist | `samples/_probe/newsroom_handoff/real_packet_readiness_checklist.json` |
| slot-linkage proof | `samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json` |
| transfer-planning proof | `samples/_probe/newsroom_handoff/transfer_planning_readback.json` |
| Review Console planning panel | `docs/verification/NEWSROOM_REVIEW_CONSOLE_PLANNING_PANEL_V1_2026-06-20.md` |

## Required Export Bundle Fields

| Field | Required before | Owner | Why needed | Current NLMYTGen consumer | Failure behavior |
| --- | --- | --- | --- | --- | --- |
| `artifact_id` | NLMYTGen ingest | newsroom-yt-pipeline | Stable export artifact identity. | validator | fail |
| `contract_version` | NLMYTGen ingest | newsroom-yt-pipeline | Prevents silent contract drift. | validator | fail |
| `episode_id` | NLMYTGen ingest | newsroom-yt-pipeline | Stable episode identity for validation and readbacks. | validator | fail |
| `title` | NLMYTGen ingest | newsroom-yt-pipeline | Bounded working title for review surfaces. | validator | fail |
| `topic_summary` | NLMYTGen ingest | newsroom-yt-pipeline | Editorial summary without downstream source discovery. | validator | fail |
| `episode_metadata` | NLMYTGen ingest | newsroom-yt-pipeline | Language, lane, duration, and package context. | validator | fail |
| `source_notes` | NLMYTGen ingest | newsroom-yt-pipeline | Sanitized source ids and summaries for evidence refs. | validator | fail |
| `provenance` | NLMYTGen ingest | newsroom-yt-pipeline | Source owner, raw material state, and source-discovery owner. | transfer-planning proof | block transfer |
| `rights_summary` | NLMYTGen ingest | newsroom-yt-pipeline | Clearance state, allowed uses, blocked uses, and risk flags. | transfer-planning proof | block transfer |
| `notebooklm_packet_or_transcript_seed` | NLMYTGen ingest | newsroom-yt-pipeline | Bounded downstream script seed material. | validator | fail |
| `script_beats` | NLMYTGen ingest | newsroom-yt-pipeline | Stable beat ids, claims, intents, and evidence refs. | validator | fail |
| `visual_plan` | NLMYTGen ingest | newsroom-yt-pipeline | Stable visual ids, beat links, layout candidates, content slots, and asset policy. | slot-linkage proof | fail |
| `g28_slot_hints` | NLMYTGen ingest | newsroom-yt-pipeline | Links visual concepts to G-28 object catalog slots. | slot-linkage proof | warn |
| `review_warnings` | NLMYTGen ingest | newsroom-yt-pipeline | Data-backed blocker and caution state. | transfer-planning proof | block transfer |
| `downstream_readiness` | NLMYTGen ingest | newsroom-yt-pipeline | Readiness booleans and blocking reasons. | transfer-planning proof | block transfer |
| `rights_provenance_clearance` | transfer candidate | human reviewer | Explicit rights/provenance outcome before transfer-candidate review. | transfer-planning proof | block transfer |
| `media_source_availability` | transfer candidate | newsroom-yt-pipeline | Approved media metadata, approved abstract replacement, or explicit no-media route. | transfer-planning proof | block transfer |
| `review_approval_status` | transfer candidate | human reviewer | Human planning outcome separate from production approval. | Review Console planning panel | hold for review |
| `visual_readiness` | transfer candidate | NLMYTGen | Visual plan, content slots, asset policy, and G-28 hints are reviewable. | slot-linkage proof | block transfer |
| `blocked_prohibited_actions_resolved` | transfer candidate | human reviewer | No blocked use still forbids transfer, render, publication, source fetch, or production approval. | transfer-planning proof | block transfer |
| `no_readiness_blocker_contradiction` | transfer candidate | NLMYTGen | Transfer readiness cannot be true while blockers remain. | transfer-planning proof | fail |

## Optional Enrichments

These fields improve review quality but should not be used to fabricate missing
required fields.

| Field | Required before | Owner | Current NLMYTGen consumer | Failure behavior |
| --- | --- | --- | --- | --- |
| `editorial_priority` | human review | newsroom-yt-pipeline | not covered yet | warn |
| `visual_treatment_preference` | human review | newsroom-yt-pipeline | not covered yet | warn |
| `source_confidence` | human review | newsroom-yt-pipeline | not covered yet | warn |
| `reviewer_notes` | human review | human reviewer | Review Console planning panel | warn |
| `localization_notes` | human review | newsroom-yt-pipeline | not covered yet | warn |
| `channel_package_metadata` | human review | newsroom-yt-pipeline | not covered yet | warn |

## Hold / Human Review Fields

These fields route a packet to human planning review. They do not grant rights,
production approval, publication approval, render approval, or YMM4 transfer
readiness.

| Field | Owner | Current NLMYTGen consumer | Failure behavior |
| --- | --- | --- | --- |
| `ambiguous_rights` | human reviewer | transfer-planning proof | hold for review |
| `unclear_media_availability` | newsroom-yt-pipeline | transfer-planning proof | hold for review |
| `real_screenshots_footage` | external/manual | not covered yet | hold for review |
| `brand_risk` | human reviewer | not covered yet | hold for review |
| `uncertain_citation_quote_usage` | human reviewer | validator | hold for review |
| `visual_approval` | human reviewer | Review Console planning panel | hold for review |

## Prohibited Upstream Assumptions

The export contract must not depend on NLMYTGen doing any of the following:

| Assumption to reject | Owner outside NLMYTGen | NLMYTGen behavior |
| --- | --- | --- |
| RSS/source discovery | newsroom-yt-pipeline | fail |
| source scraping or raw source expansion | external/manual | fail |
| Inoreader or external reader operation | external/manual | fail |
| live source download, screenshots, footage, or media download | external/manual | fail |
| rights acquisition | external/manual | hold for review |
| production approval | human reviewer | block transfer |
| publish/upload | external/manual | fail |
| silent inference of missing approvals | human reviewer | hold for review |
| YMM4 transfer artifact creation or `.ymmp` editing | NLMYTGen | block transfer |
| render/media output generation | NLMYTGen | block transfer |

## Proposed Newsroom Export Fixture Shape

Use fake placeholders only for fixture work. The shape below is illustrative,
not a second-repo implementation prompt.

```json
{
  "artifact_id": "fake_real_export_bundle_0001",
  "contract_version": "newsroom-to-nlmytgen-handoff-v1.11",
  "episode_id": "episode_placeholder_0001",
  "title": "Placeholder real-export title",
  "topic_summary": "Sanitized summary supplied by newsroom export.",
  "episode_metadata": {
    "language": "ja-JP",
    "channel_package": "package_placeholder",
    "editorial_status": "ready_for_nlmytgen_intake_review"
  },
  "source_notes": [
    {
      "source_id": "src_placeholder_001",
      "non_fetching_reference": "SOURCE_REF_DO_NOT_FETCH",
      "summary": "Sanitized source summary only.",
      "quote_policy": "paraphrase_or_short_quote_pending_review"
    }
  ],
  "provenance": {
    "source_collection_owner": "newsroom-yt-pipeline",
    "raw_source_material_included": false,
    "external_fetch_allowed_by_nlmytgen": false
  },
  "rights_summary": {
    "clearance_state": "pending_review",
    "allowed_uses": ["nlmytgen_review"],
    "blocked_uses": ["publication", "render", "YMM4_transfer"]
  },
  "script_beats": [
    {
      "beat_id": "beat_placeholder_001",
      "claim": "Sanitized claim placeholder.",
      "evidence_refs": ["src_placeholder_001"]
    }
  ],
  "visual_plan": [
    {
      "visual_id": "vis_placeholder_001",
      "beat_id": "beat_placeholder_001",
      "asset_policy": "approved_media_or_abstract_replacement_required",
      "content_slots": ["screenshot_slot", "source_note", "caption_reserve"]
    }
  ],
  "g28_slot_hints": [
    {
      "visual_id": "vis_placeholder_001",
      "object_catalog_slot": "source_note",
      "source_ref": "src_placeholder_001"
    }
  ],
  "review_warnings": [
    {
      "warning_id": "rw_placeholder_001",
      "severity": "blocker",
      "surface": "rights_summary",
      "blocks_ymm4_transfer": true
    }
  ],
  "downstream_readiness": {
    "review_surface_ready": true,
    "ymm4_transfer_ready": false,
    "blocking_reasons": ["rights_review_required", "media_review_required"]
  }
}
```

## Delta From Current Synthetic Fixture

| Delta class | Fields |
| --- | --- |
| Already represented | `artifact_id`, `contract_version` |
| Represented but synthetic-only | `episode_id`, `title`, `topic_summary`, `episode_metadata`, `source_notes`, `provenance`, `rights_summary`, `notebooklm_packet_or_transcript_seed`, `script_beats`, `visual_plan`, `g28_slot_hints`, `review_warnings`, `downstream_readiness` |
| Missing for real packet | `editorial_priority`, `visual_treatment_preference`, `source_confidence`, `reviewer_notes`, `localization_notes`, `channel_package_metadata`, `real_screenshots_footage`, `brand_risk` |
| Missing for transfer candidate | `rights_provenance_clearance`, `media_source_availability`, `review_approval_status`, `visual_readiness`, `blocked_prohibited_actions_resolved`, `no_readiness_blocker_contradiction`, `ambiguous_rights`, `unclear_media_availability`, `uncertain_citation_quote_usage`, `visual_approval` |
| Not NLMYTGen-owned | RSS/source discovery, source scraping, Inoreader operation, live source download, rights acquisition, production approval, publish/upload, silent approval inference |

## Next Implementation Handoff

For a later `newsroom-yt-pipeline` slice: create or adjust the upstream export
fixture so it emits the required bundle fields, transfer gates, optional
enrichments, and human-review holds listed here. Use fake placeholders for
fixture data. Do not move source discovery, scraping, Inoreader operation, live
source download, rights acquisition, production approval, publish/upload,
rendering, YMM4 transfer, or `.ymmp` editing into NLMYTGen.

## Validation Readback

Expected local validation for this request:

- JSON parses:
  `samples/_probe/newsroom_handoff/upstream_export_delta_request.json`
- Every request item has `field_name`, `owner`, `required_before`,
  `current_consumer`, `failure_behavior`, `request_priority`, and `why_needed`
- The request keeps `real_packet_accepted=false`, `production_approval=false`,
  `rights_approval=false`, and `ymm4_transfer_ready=false`
- The request contains no live source references, media outputs, render outputs,
  `.ymmp` edits, or YMM4 transfer artifacts
- Existing validator, slot-linkage proof, and transfer-planning proof remain
  unchanged against the synthetic packet
