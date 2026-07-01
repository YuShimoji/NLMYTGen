# Newsroom Episode Capsule Route Hardening v1

artifact_id: newsroom_episode_capsule_route_hardening_v1_2026_06_30
schema_version: newsroom_episode_capsule_route_hardening.v1
production_status: diagnostic_only
render_gate: L0_no_render
next_recommended_axis: newsroom-source-boundary-adversarial-fixtures-v1


## Identity

```json
{
  "hardening_id": "newsroom_episode_capsule_route_hardening_v1_2026_06_30",
  "source_fixture_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2.json",
  "source_fixture_validation_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_validation_v1.json",
  "source_capsule_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1.json",
  "hardened_capsule_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_hardened_episode_capsule_v1.json",
  "live_fetch_used": false,
  "render_gate": "L0_no_render"
}
```


## Capsule Route Hardening

```json
{
  "route_id": "offline_rss_like_topic_fixture_v2_to_hardened_episode_capsule_v1",
  "source_route_state": {
    "fixture_route_classification": {
      "diagnostic_only": true,
      "reusable_fixture_candidate": true,
      "still_synthetic": true,
      "blocked": false,
      "blocked_scope": "none_for_offline_diagnostic_validation",
      "production_blocked": true,
      "live_boundary_ready_candidate": false,
      "route_confidence": "medium_high",
      "classification_summary": "Required fields are present and placeholders are explicit, so the fixture is reusable offline. It remains synthetic and production blocked because source URL, published timestamp, freshness, attribution, and rights are not real reviewed source facts."
    },
    "fixture_route_boundary_states": {
      "diagnostic_only": true,
      "reusable_offline_fixture": true,
      "blocked_missing_required_fields": false,
      "blocked_unmarked_placeholder": false,
      "blocked_rights_unknown": true,
      "blocked_source_boundary_unknown": false,
      "live_boundary_ready_candidate": false,
      "state_names": [
        "diagnostic_only",
        "reusable_offline_fixture",
        "blocked_missing_required_fields",
        "blocked_unmarked_placeholder",
        "blocked_rights_unknown",
        "blocked_source_boundary_unknown",
        "live_boundary_ready_candidate"
      ],
      "missing_required_fields": [],
      "invalid_required_fields": [],
      "unmarked_placeholder_fields": []
    },
    "fixture_route_hardening_id": "newsroom_rss_topic_fixture_route_hardening_v1_2026_06_30",
    "fixture_route_next_axis": "newsroom-episode-capsule-route-hardening-v1"
  },
  "hardening_rules": {
    "each_beat_carries_validation_boundary_inputs": true,
    "source_warning_beat_is_mandatory": true,
    "excluded_claims_are_carried_to_capsule_and_every_beat": true,
    "production_claim_allowed_is_false_for_every_beat": true,
    "production_script_ready_false_when_placeholders_or_blockers_remain": true
  },
  "boundary_propagation_rules": {
    "beat_level_fields": [
      "rights_status_applied",
      "freshness_status_applied",
      "attribution_status_applied",
      "production_status_applied",
      "can_be_used_for_diagnostic",
      "can_be_used_for_live_boundary_plan",
      "can_be_used_for_production_script"
    ],
    "source_boundary_warning_must_name": [
      "fixture/offline status",
      "placeholder source fields",
      "rights/freshness/attribution are not production-approved",
      "excluded claims must not be asserted"
    ]
  },
  "excluded_claims_rules": {
    "carry_from_fixture_to_capsule": true,
    "carry_to_every_beat": true,
    "not_positive_explanation_claims": true,
    "warn_if_absent_or_empty": true
  },
  "production_readiness_rules": {
    "diagnostic_capsule_ready_requires_five_beats_and_boundary_propagation": true,
    "live_boundary_plan_ready_requires_real_source_fields": true,
    "production_script_ready_requires_no_placeholder_or_production_blockers": true,
    "do_not_mark_production_ready_from_offline_fixture": true
  },
  "existing_route_changes_or_readback_only": "original capsule artifact is unchanged; this slice writes a new hardened capsule/readback artifact and route-hardening proof"
}
```


## Hardened Capsule Summary

```json
{
  "capsule_id": "offline_rss_like_topic_fixture_v2_hardened_episode_capsule_v1_2026_06_30",
  "beat_count": 5,
  "capsule_boundary_summary": {
    "fixture_validation_status": "pass_with_explicit_production_blockers",
    "diagnostic_only": true,
    "reusable_offline_fixture_candidate": true,
    "live_boundary_ready_candidate": false,
    "production_script_ready": false,
    "production_blocker_count": 6,
    "explicit_placeholder_count": 5,
    "source_boundary_summary": "offline diagnostic fixture only; live RSS/news fetch and source truth approval remain closed",
    "rights_boundary_summary": "rights_status=placeholder:unknown_offline_fixture_needs_review; rights and quote/media reuse are not production-approved",
    "freshness_boundary_summary": "freshness_status=placeholder_not_evaluable_without_live_source; published time and freshness remain placeholder-bound",
    "attribution_boundary_summary": "attribution_note is fixture-only and must be replaced before real source workflow",
    "excluded_claims_summary": {
      "excluded_claim_count": 3,
      "excluded_claims_carried_to_capsule": true,
      "excluded_claims_carried_to_every_beat": true,
      "excluded_claims_absent": false
    }
  },
  "capsule_readiness": {
    "diagnostic_capsule_ready": true,
    "reusable_offline_capsule_ready": true,
    "live_boundary_plan_ready": false,
    "production_script_ready": false,
    "readiness_reason": "beat-level boundaries are propagated for diagnostic use, but source URL, timestamp, freshness, rights, attribution, and source reliability remain production blockers",
    "production_blocker_count": 6
  },
  "blocked_production_reasons": [
    "placeholder source URL must be replaced by a verified source URL before live or production use",
    "placeholder published timestamp must be replaced before freshness-dependent use",
    "rights_status remains unknown placeholder; rights and quote/media reuse are not approved",
    "freshness_status remains placeholder/not evaluable without a live source",
    "attribution_note is fixture-only and must be replaced before a real source workflow",
    "source_reliability_note does not score or approve a real publisher/source"
  ],
  "warnings": [
    "production blockers remain attached to every beat; production script readiness stays false",
    "diagnostic_only production status is propagated to the capsule"
  ],
  "not_accepted_scope": {
    "live_rss_or_news_fetch": false,
    "production_script_quality": false,
    "production_article_use": false,
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
    "source_truth_or_rights_approval": false,
    "local_ymmp_materialization": false
  }
}
```


## Beat Table

| beat_id | beat_function | explanation_line | source_fields_used | excluded_claims_applied | source_boundary_role | rights_boundary_role | freshness_boundary_role | attribution_boundary_role | production_status_applied | warning_required | production_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| offline_rss_like_topic_v2_beat_01_hook | hook / issue framing | Hook: a topic is only a starting point until its source boundary is clear. | ["title", "summary", "intended_episode_angle"] | ["Do not claim that the topic was fetched from a live RSS feed.", "Do not claim that source facts, freshness, rights, or quotes are approved.", "Do not claim production subtitle/card design, render quality, public readiness, or audience acceptance."] | uses title and summary while stating the fixture is offline; validation boundary remains attached | rights_status=placeholder:unknown_offline_fixture_needs_review; rights and quote/media reuse are not production-approved | freshness_status=placeholder_not_evaluable_without_live_source; published time and freshness remain placeholder-bound | attribution_note is fixture-only and must be replaced before real source workflow | diagnostic_only | False | False |
| offline_rss_like_topic_v2_beat_02_key_claim | key claim / explanation | Key claim: source identity, freshness, rights, and excluded claims must be explicit first. | ["key_claim", "excluded_claims", "production_status"] | ["Do not claim that the topic was fetched from a live RSS feed.", "Do not claim that source facts, freshness, rights, or quotes are approved.", "Do not claim production subtitle/card design, render quality, public readiness, or audience acceptance."] | limits the claim to fixture-level source checks; validation boundary remains attached | rights_status=placeholder:unknown_offline_fixture_needs_review; rights and quote/media reuse are not production-approved | freshness_status=placeholder_not_evaluable_without_live_source; published time and freshness remain placeholder-bound | attribution_note is fixture-only and must be replaced before real source workflow | diagnostic_only | False | False |
| offline_rss_like_topic_v2_beat_03_source_boundary_warning | source-boundary warning | Warning: this offline fixture still uses placeholder source URL and timestamp fields; rights, freshness, and attribution are not production-approved, and excluded claims must not be asserted. | ["uncertainty_or_boundary", "source_url_or_placeholder", "published_at_or_placeholder", "rights_status"] | ["Do not claim that the topic was fetched from a live RSS feed.", "Do not claim that source facts, freshness, rights, or quotes are approved.", "Do not claim production subtitle/card design, render quality, public readiness, or audience acceptance."] | mandatory source-boundary warning: offline fixture, placeholder source fields, no production approval, and excluded-claim guard | rights_status=placeholder:unknown_offline_fixture_needs_review; rights and quote/media reuse are not production-approved | freshness_status=placeholder_not_evaluable_without_live_source; published time and freshness remain placeholder-bound | attribution_note is fixture-only and must be replaced before real source workflow | diagnostic_only | True | False |
| offline_rss_like_topic_v2_beat_04_implication | implication / why it matters | Why it matters: a stronger fixture can test episode structure without overclaiming. | ["why_it_matters", "editorial_risk", "freshness_status"] | ["Do not claim that the topic was fetched from a live RSS feed.", "Do not claim that source facts, freshness, rights, or quotes are approved.", "Do not claim production subtitle/card design, render quality, public readiness, or audience acceptance."] | separates route confidence from source truth confidence; validation boundary remains attached | rights_status=placeholder:unknown_offline_fixture_needs_review; rights and quote/media reuse are not production-approved | freshness_status=placeholder_not_evaluable_without_live_source; published time and freshness remain placeholder-bound | attribution_note is fixture-only and must be replaced before real source workflow | diagnostic_only | False | False |
| offline_rss_like_topic_v2_beat_05_close | close / next action | Next: validate the fixture schema before any live RSS plan. | ["production_status", "materialization_notes", "excluded_claims"] | ["Do not claim that the topic was fetched from a live RSS feed.", "Do not claim that source facts, freshness, rights, or quotes are approved.", "Do not claim production subtitle/card design, render quality, public readiness, or audience acceptance."] | keeps live RSS/news and materialization out of this slice; validation boundary remains attached | rights_status=placeholder:unknown_offline_fixture_needs_review; rights and quote/media reuse are not production-approved | freshness_status=placeholder_not_evaluable_without_live_source; published time and freshness remain placeholder-bound | attribution_note is fixture-only and must be replaced before real source workflow | diagnostic_only | False | False |


## Validation Readback

```json
{
  "excluded_claims_absent": false,
  "excluded_claims_used_as_positive_claims": false,
  "production_blockers_propagated": true,
  "placeholder_fields_propagated": true,
  "source_warning_beat_present": true,
  "source_warning_mentions_fixture_offline_status": true,
  "source_warning_mentions_placeholder_source_fields": true,
  "source_warning_mentions_rights_freshness_attribution": true,
  "source_warning_mentions_excluded_claims": true,
  "production_script_ready": false,
  "live_boundary_plan_ready": false
}
```


## Production Readiness Classification

```json
{
  "diagnostic_capsule_ready": true,
  "reusable_offline_capsule_ready": true,
  "live_boundary_plan_ready": false,
  "production_script_ready": false,
  "readiness_reason": "beat-level boundaries are propagated for diagnostic use, but source URL, timestamp, freshness, rights, attribution, and source reliability remain production blockers",
  "production_blocker_count": 6
}
```


## Business Goal Outcome Contract

```json
{
  "problem_clear": {
    "status": true,
    "rationale": "validated fixture boundaries now remain visible at capsule and beat level"
  },
  "offer_clear": {
    "status": true,
    "rationale": "capsule generation is safer because blocker and excluded-claim state is carried with every beat"
  },
  "proof_clear": {
    "status": true,
    "rationale": "this is capsule-route hardening proof, not production quality proof"
  },
  "boundary_clear": {
    "status": true,
    "rationale": "live/source/rights claims remain blocked while placeholders remain"
  },
  "next_action_clear": {
    "status": true,
    "rationale": "newsroom-source-boundary-adversarial-fixtures-v1"
  },
  "visual_supports_explanation": {
    "status": true,
    "rationale": "YMM4 visual proof remains closed; no preview or render is reopened"
  }
}
```


## Recommendation Logic

```json
{
  "selected": "newsroom-source-boundary-adversarial-fixtures-v1",
  "if_beat_level_propagation_still_has_gaps": "newsroom-episode-capsule-route-hardening-v2",
  "if_offline_fixture_and_capsule_route_are_solid_and_live_boundary_is_dominant": "newsroom-live-rss-boundary-plan-v1",
  "if_fixture_validation_lacks_adversarial_cases_or_schema_gaps": "newsroom-rss-topic-fixture-route-hardening-v2",
  "if_fixture_examples_remain_too_synthetic": "newsroom-offline-rss-like-topic-fixture-v3-with-realistic-placeholders-v1",
  "if_validator_and_capsule_need_missing_invalid_unmarked_cases": "newsroom-source-boundary-adversarial-fixtures-v1",
  "reason": "Capsule boundary propagation passes for the current fixture, but the route still depends on synthetic placeholder examples. Before live boundary planning, adversarial source-boundary fixtures should exercise missing, invalid, and unmarked cases across validator and capsule."
}
```


## Not Accepted Scope

```json
{
  "live_rss_or_news_fetch": false,
  "production_script_quality": false,
  "production_article_use": false,
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
  "source_truth_or_rights_approval": false,
  "local_ymmp_materialization": false
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
  "local_ignored_ymmp_created_in_this_slice": false,
  "local_ignored_ymmp_modified_in_this_slice": false,
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
| next_axis_remains_topic_RSS_to_episode_construction | newsroom-source-boundary-adversarial-fixtures-v1 |


## Completion Matrix

| gate | status |
| --- | --- |
| repo_state_verified | True |
| fixture_validation_inspected | True |
| capsule_route_inspected | True |
| hardening_rules_defined | True |
| hardened_capsule_readback_created | True |
| boundary_propagation_verified | True |
| next_axis_selected | True |
| no_forbidden_visual_live_or_media_scope_reopened | True |


## Boundary Note

This hardening proof propagates validated fixture boundaries into the five-beat capsule only. It does not fetch live RSS/news, create or modify .ymmp files, request YMM4 preview, render, generate audio/TTS, redesign cards, tune animation, or claim production/public acceptance.
