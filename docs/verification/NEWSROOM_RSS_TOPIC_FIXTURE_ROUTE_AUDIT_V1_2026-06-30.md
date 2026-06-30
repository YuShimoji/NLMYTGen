# Newsroom RSS Topic Fixture Route Audit v1

artifact_id: newsroom_rss_topic_fixture_route_audit_v1_2026_06_30
route_id: offline_rss_like_topic_fixture_001_to_mini_episode_capsule_v1
schema_version: newsroom_rss_topic_fixture_route_audit.v1
production_status: diagnostic_only
render_gate: L0_no_render
selected_next_axis: newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1


## Current Topic Fixture

```json
{
  "topic_id": "offline_rss_like_topic_fixture_001",
  "title": "Offline fixture: source-boundary handoff before public news",
  "source_kind": "offline_fixture_or_diagnostic",
  "key_fact_or_claim": "A candidate topic must remain diagnostic until source truth, rights, and episode fit are reviewed.",
  "explanation_angle": "show that a topic-like input can become one clear explanation beat without using live RSS or public-news claims",
  "boundary_note": "No live RSS/network fetch, source quote, external media, rights approval, or publication readiness is implied."
}
```


## Current Route Classification

```json
{
  "diagnostic_only": true,
  "reusable_fixture_candidate": true,
  "too_synthetic": true,
  "blocked": false,
  "classification_summary": "usable as an offline diagnostic route skeleton, but too synthetic for safer episode generation until source, freshness, rights, summary, and excluded-claim fields are explicit"
}
```


## Field Status

```json
{
  "topic_id": "present_exact",
  "title": "present_exact",
  "source_name": "missing_or_placeholder_required",
  "source_url_or_placeholder": "missing_or_placeholder_required",
  "published_at_or_placeholder": "missing_or_placeholder_required",
  "summary": "missing_or_placeholder_required",
  "key_claim": "present_as_key_fact_or_claim",
  "why_it_matters": "missing_or_placeholder_required",
  "uncertainty_or_boundary": "present_as_boundary_note",
  "rights_status": "missing_or_placeholder_required",
  "intended_episode_angle": "present_as_explanation_angle",
  "excluded_claims": "missing_or_placeholder_required",
  "production_status": "present_as_source_kind"
}
```


## Transformation Steps

| beat | current_derivation | source_fields_used | audit_note |
| --- | --- | --- | --- |
| hook | Hook: this offline topic checks the episode route. | ["title", "explanation_angle"] | works as diagnostic framing, but should use v2 summary and intended_episode_angle |
| key_claim | A candidate topic must remain diagnostic until source truth, rights, and episode fit are reviewed. | ["key_fact_or_claim"] | needs explicit key_claim plus excluded_claims before production-like generation |
| source_warning | Offline fixture: verify source boundary before production. | ["boundary_note", "source_kind"] | boundary is strong, but source_url/freshness/rights placeholders should be explicit |
| implication | Why it matters: topic input can become a short explainer. | ["explanation_angle"] | needs why_it_matters as its own fixture field |
| close | Next: harden the source route before production. | ["boundary_note"] | should be generated from production_status and uncertainty_or_boundary |


## Source Boundary Fields

```json
{
  "source_kind": "offline_fixture_or_diagnostic",
  "boundary_note": "No live RSS/network fetch, source quote, external media, rights approval, or publication readiness is implied.",
  "network_fetch_performed": false,
  "live_RSS_or_news_used": false,
  "source_truth_approved": false,
  "public_readiness_claimed": false
}
```


## Rights And Attribution Placeholders

```json
{
  "rights_status": "missing_explicit_field",
  "source_name": "missing_explicit_field",
  "source_url_or_placeholder": "missing_explicit_field",
  "attribution_text": "missing_explicit_field",
  "current_boundary_note": "No live RSS/network fetch, source quote, external media, rights approval, or publication readiness is implied."
}
```


## Freshness Placeholder

```json
{
  "published_at_or_placeholder": "missing_explicit_field",
  "freshness_status": "not_evaluable_from_current_fixture",
  "source_kind": "offline_fixture_or_diagnostic"
}
```


## Title / Summary / Claim / Source URL Status

```json
{
  "title": "present",
  "summary": "missing_explicit_field",
  "claim": "present_as_key_fact_or_claim",
  "source_url_or_placeholder": "missing_explicit_field"
}
```


## Minimal Offline RSS-like Topic Schema Recommendation

```json
{
  "schema_id": "offline_rss_like_topic_fixture_v2_minimal",
  "required_fields": [
    "topic_id",
    "title",
    "source_name",
    "source_url_or_placeholder",
    "published_at_or_placeholder",
    "summary",
    "key_claim",
    "why_it_matters",
    "uncertainty_or_boundary",
    "rights_status",
    "intended_episode_angle",
    "excluded_claims",
    "production_status"
  ],
  "field_purposes": {
    "topic_id": "stable local identifier for fixture and beat traceability",
    "title": "human-readable topic headline or RSS title equivalent",
    "source_name": "publication/feed/source label or explicit placeholder",
    "source_url_or_placeholder": "article/feed URL or placeholder proving live fetch is still closed",
    "published_at_or_placeholder": "freshness marker or placeholder",
    "summary": "short source-bounded description, separate from the claim",
    "key_claim": "the claim allowed to influence the episode beats",
    "why_it_matters": "reason the topic can become an explainer beat",
    "uncertainty_or_boundary": "known uncertainty, source limitation, or diagnostic boundary",
    "rights_status": "rights/quote/media reuse status or explicit unknown",
    "intended_episode_angle": "the explanatory angle to generate hook/implication/close",
    "excluded_claims": "claims that must not be generated from the fixture",
    "production_status": "diagnostic_only until source and rights are reviewed"
  },
  "example_status_values": {
    "rights_status": [
      "unknown_offline_fixture",
      "needs_review"
    ],
    "production_status": [
      "diagnostic_only"
    ]
  }
}
```


## Route Blockers

| blocker |
| --- |
| missing or placeholder-required field: source_name |
| missing or placeholder-required field: source_url_or_placeholder |
| missing or placeholder-required field: published_at_or_placeholder |
| missing or placeholder-required field: summary |
| missing or placeholder-required field: why_it_matters |
| missing or placeholder-required field: rights_status |
| missing or placeholder-required field: excluded_claims |


## Next Required Work

| work |
| --- |
| materialize an offline RSS-like topic fixture v2 with explicit source, freshness, rights, and excluded-claim fields |
| regenerate the five-beat mini episode capsule from that stronger fixture |
| keep live RSS/news fetch closed until the offline schema route is stable |


## Business Goal Outcome Contract

```json
{
  "problem_clear": {
    "status": true,
    "rationale": "the readable visual loop is closed with a bounded preview pass"
  },
  "offer_clear": {
    "status": true,
    "rationale": "the audit shifts attention from YMM4 visibility to topic/RSS-to-episode inputs"
  },
  "proof_clear": {
    "status": true,
    "rationale": "the artifact audits the input route rather than production quality"
  },
  "boundary_clear": {
    "status": true,
    "rationale": "live/news/source truth, rights, render, cards, and production claims remain closed"
  },
  "next_action_clear": {
    "status": true,
    "rationale": "newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1"
  },
  "visual_supports_explanation": {
    "status": true,
    "rationale": "YMM4 visual proof is closed for now; the next proof should be fixture-route construction"
  }
}
```


## Recommendation Logic

```json
{
  "selected": "newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1",
  "if_audit_defines_stronger_reusable_fixture_schema": "newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1",
  "if_current_route_needs_validation_hardening": "newsroom-rss-topic-fixture-route-hardening-v1",
  "if_offline_fixture_route_already_strong_and_live_boundary_next": "newsroom-live-rss-boundary-plan-v1",
  "if_episode_capsule_route_is_dominant_weak_point": "newsroom-episode-capsule-route-hardening-v1",
  "reason": "the readable YMM4 loop is closed, and the audit can define a stronger offline RSS-like fixture schema without live network fetch"
}
```


## Not Accepted Scope

```json
{
  "live_rss_or_news_fetch": false,
  "production_script_quality": false,
  "production_subtitle_design": false,
  "production_card_design": false,
  "production_animation_quality": false,
  "card_redesign": false,
  "visual_layout_tuning": false,
  "animation_tuning": false,
  "render_export_proof": false,
  "audio_or_tts_output": false,
  "public_upload_or_public_readiness": false,
  "actual_order_or_audience_acceptance": false,
  "source_truth_or_rights_approval": false
}
```


## Boundaries

```json
{
  "network_fetch_performed": false,
  "live_RSS_news_fetch_performed": false,
  "YMM4_launched_by_agent": false,
  "render_performed_by_agent": false,
  "audio_tts_generated": false,
  "real_media_imported": false,
  "external_fetch_performed": false,
  "card_assets_modified": false,
  "card_redesign_performed": false,
  "production_subtitle_or_card_design_created": false,
  "animation_tuned": false,
  "animation_only_probe_created": false,
  "additional_YMM4_preview_requested": false,
  "ymmp_or_media_staged_or_committed": false,
  "production_public_readiness_claimed": false,
  "actual_order_or_audience_acceptance_claimed": false
}
```


## Inertia Check

| gate | status |
| --- | --- |
| no_YMM4_visual_loop | True |
| no_animation_only_loop | True |
| no_primitive_or_tempo_loop | True |
| no_card_polish_loop | True |
| no_render_export_loop | True |
| no_live_RSS_or_network_fetch | True |
| next_axis_remains_topic_RSS_to_episode_construction | newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1 |


## Completion Matrix

| gate | status |
| --- | --- |
| repo_state_verified | True |
| readable_preview_observation_recorded | True |
| YMM4_visual_loop_closed_for_now | True |
| current_topic_fixture_route_audited | True |
| minimal_next_fixture_schema_recommended | True |
| next_axis_selected | True |


## Boundary Note

This audit stays offline. It recommends a stronger fixture schema before any live RSS/news boundary plan, and it makes no source-truth, rights, render, production, public, or audience acceptance claim.
