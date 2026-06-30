# Newsroom Offline RSS-like Topic Fixture v2 To Mini Episode Capsule v1

artifact_id: newsroom_offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1_2026_06_30
schema_version: newsroom_offline_rss_like_topic_fixture_v2_to_mini_episode_capsule.v1
production_status: diagnostic_only
render_gate: L0_no_render
selected_next_axis: newsroom-rss-topic-fixture-route-hardening-v1


## Source And Output Artifacts

```json
{
  "source_fixture_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2.json",
  "source_schema_contract_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_schema_contract_v1.json",
  "source_route_audit_path": "samples/_probe/newsroom_handoff/rss_topic_fixture_route_audit_v1.json",
  "source_topic_fixture_path": "samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json",
  "existing_artifacts_used": [
    "samples/_probe/newsroom_handoff/rss_topic_fixture_route_audit_v1.json",
    "samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json",
    "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_with_animation_accent_v1.json",
    "samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json"
  ],
  "output_artifacts": [
    "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2.json",
    "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_schema_contract_v1.json",
    "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1.json",
    "docs/verification/NEWSROOM_OFFLINE_RSS_LIKE_TOPIC_FIXTURE_V2_TO_MINI_EPISODE_CAPSULE_V1_2026-06-30.md"
  ]
}
```


## Fixture Readback

```json
{
  "artifact_id": "offline_rss_like_topic_fixture_v2_2026_06_30",
  "fixture_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2.json",
  "schema_contract_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_schema_contract_v1.json",
  "topic_id": "offline_rss_like_topic_fixture_v2_001",
  "title": "Offline fixture: source boundary check before a short explainer",
  "required_field_count": 13,
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
  "required_fields_present": [
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
  "missing_required_fields": [],
  "recommended_fields_present": [
    "source_kind",
    "language",
    "topic_category",
    "source_reliability_note",
    "attribution_note",
    "freshness_status",
    "editorial_risk",
    "materialization_notes"
  ],
  "placeholder_fields": [
    "source_url_or_placeholder",
    "published_at_or_placeholder",
    "rights_status",
    "freshness_status"
  ],
  "placeholder_count": 4,
  "excluded_claim_count": 3,
  "production_status": "diagnostic_only",
  "source_boundary_fields": {
    "network_fetch_performed": false,
    "live_RSS_news_fetch_performed": false,
    "source_truth_approved": false,
    "rights_approved": false,
    "public_readiness_claimed": false
  },
  "production_blockers": [
    "source_url_or_placeholder remains a placeholder rather than a fetched source URL",
    "published_at_or_placeholder remains a placeholder rather than verified freshness",
    "rights_status remains placeholder:unknown_offline_fixture_needs_review",
    "source reliability and source truth are not approved",
    "live RSS/news fetch remains intentionally closed"
  ]
}
```


## Transformation Readback

```json
{
  "source_topic_id": "offline_rss_like_topic_fixture_v2_001",
  "source_fixture_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2.json",
  "target_capsule_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1.json",
  "transformation_status": "offline_fixture_v2_to_diagnostic_five_beat_capsule",
  "network_fetch_performed": false,
  "live_RSS_news_fetch_performed": false,
  "beat_count": 5,
  "beat_functions": [
    "hook / issue framing",
    "key claim / explanation",
    "source-boundary warning",
    "implication / why it matters",
    "close / next action"
  ],
  "steps": [
    {
      "order": 1,
      "beat_id": "offline_rss_like_topic_v2_beat_01_hook",
      "beat_function": "hook / issue framing",
      "source_fields_used": [
        "title",
        "summary",
        "intended_episode_angle"
      ],
      "animation_accent_assignment": "stable_pose_only",
      "source_boundary_role": "uses title and summary while stating the fixture is offline"
    },
    {
      "order": 2,
      "beat_id": "offline_rss_like_topic_v2_beat_02_key_claim",
      "beat_function": "key claim / explanation",
      "source_fields_used": [
        "key_claim",
        "excluded_claims",
        "production_status"
      ],
      "animation_accent_assignment": "expression_event",
      "source_boundary_role": "limits the claim to fixture-level source checks"
    },
    {
      "order": 3,
      "beat_id": "offline_rss_like_topic_v2_beat_03_source_boundary_warning",
      "beat_function": "source-boundary warning",
      "source_fields_used": [
        "uncertainty_or_boundary",
        "source_url_or_placeholder",
        "published_at_or_placeholder",
        "rights_status"
      ],
      "animation_accent_assignment": "expression_plus_short_nod",
      "source_boundary_role": "names no live fetch, no rights approval, and no public readiness"
    },
    {
      "order": 4,
      "beat_id": "offline_rss_like_topic_v2_beat_04_implication",
      "beat_function": "implication / why it matters",
      "source_fields_used": [
        "why_it_matters",
        "editorial_risk",
        "freshness_status"
      ],
      "animation_accent_assignment": "short_nod_reaction",
      "source_boundary_role": "separates route confidence from source truth confidence"
    },
    {
      "order": 5,
      "beat_id": "offline_rss_like_topic_v2_beat_05_close",
      "beat_function": "close / next action",
      "source_fields_used": [
        "production_status",
        "materialization_notes",
        "excluded_claims"
      ],
      "animation_accent_assignment": "none",
      "source_boundary_role": "keeps live RSS/news and materialization out of this slice"
    }
  ],
  "source_boundary_propagated": true,
  "excluded_claims_applied_to_every_beat": true
}
```


## Mini Episode Capsule Summary

```json
{
  "episode_title": "Source boundary check before a short explainer",
  "episode_goal": "Prove that a stronger offline RSS-like fixture can produce a bounded five-beat diagnostic episode capsule without live fetch or visual production claims.",
  "beat_count": 5,
  "animation_accent_summary": {
    "policy_status": "frozen_mvp_policy_carried_forward",
    "allowed_assignments": [
      "stable_pose_only",
      "expression_event",
      "short_nod_reaction",
      "expression_plus_short_nod",
      "none"
    ],
    "assignment_counts": {
      "stable_pose_only": 1,
      "expression_event": 1,
      "expression_plus_short_nod": 1,
      "short_nod_reaction": 1,
      "none": 1
    },
    "disabled": [
      "body forward/back",
      "repeated nodding",
      "mechanical expression cycling",
      "speech balloon",
      "designed card layout",
      "animation-only probe loop",
      "tempo-only loop"
    ],
    "animation_optional_not_forced": true
  },
  "source_boundary_summary": "Every beat stays inside the offline fixture boundary and applies the excluded claims."
}
```


## Beat Mapping Summary

| beat_id | beat_function | explanation_line | background_animation_accent_role | source_boundary_role | production_status |
| --- | --- | --- | --- | --- | --- |
| offline_rss_like_topic_v2_beat_01_hook | hook / issue framing | Hook: a topic is only a starting point until its source boundary is clear. | stable_pose_only | uses title and summary while stating the fixture is offline | diagnostic_only |
| offline_rss_like_topic_v2_beat_02_key_claim | key claim / explanation | Key claim: source identity, freshness, rights, and excluded claims must be explicit first. | expression_event | limits the claim to fixture-level source checks | diagnostic_only |
| offline_rss_like_topic_v2_beat_03_source_boundary_warning | source-boundary warning | Warning: this offline fixture is not live news and does not approve source truth. | expression_plus_short_nod | names no live fetch, no rights approval, and no public readiness | diagnostic_only |
| offline_rss_like_topic_v2_beat_04_implication | implication / why it matters | Why it matters: a stronger fixture can test episode structure without overclaiming. | short_nod_reaction | separates route confidence from source truth confidence | diagnostic_only |
| offline_rss_like_topic_v2_beat_05_close | close / next action | Next: validate the fixture schema before any live RSS plan. | none | keeps live RSS/news and materialization out of this slice | diagnostic_only |


## Route Assessment

```json
{
  "route_id": "offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1",
  "source_capsule_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1.json",
  "source_topic_fixture_path": "samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2.json",
  "route_classification": "current_partial",
  "current_route_classification": {
    "diagnostic_only": true,
    "reusable_fixture_candidate": true,
    "still_synthetic": true,
    "stronger_than_v1": true,
    "blocked": false,
    "classification_summary": "v2 fills the v1 missing-field blockers and can generate a five-beat diagnostic capsule, but source URL, publication time, freshness, and rights remain explicit placeholders."
  },
  "route_confidence": "medium",
  "route_blockers": [
    "source_url_or_placeholder remains a placeholder rather than a fetched source URL",
    "published_at_or_placeholder remains a placeholder rather than verified freshness",
    "rights_status remains placeholder:unknown_offline_fixture_needs_review",
    "source reliability and source truth are not approved",
    "live RSS/news fetch remains intentionally closed"
  ],
  "next_required_route_work": [
    "newsroom-rss-topic-fixture-route-hardening-v1",
    "add deterministic fixture validation and placeholder hardening before any live RSS boundary plan",
    "keep YMM4 preview/materialization closed unless route changes materially affect visible output"
  ],
  "item_semantics": {
    "TextItem role": "one plain diagnostic text/caption role per generated beat if materialized later",
    "GroupItem/ImageItem animation accent role": "frozen optional background accent assignment only; no primitive tuning",
    "beat timing role": "five ordered capsule segments; no YMM4 timeline written in this slice",
    "source boundary role": "fixture placeholders, excluded claims, and diagnostic status are carried into every beat"
  },
  "diagnostic_only": true,
  "reusable_fixture_candidate": true,
  "blocked": false,
  "fixture_stronger_than_v1": true,
  "still_synthetic": true
}
```


## Business Goal Outcome Contract

```json
{
  "problem_clear": {
    "status": true,
    "rationale": "the route moves beyond the v1 too-synthetic fixture by making source, freshness, rights, summary, and excluded claims explicit"
  },
  "offer_clear": {
    "status": true,
    "rationale": "the artifact shows how a stronger offline topic becomes five capsule beats"
  },
  "proof_clear": {
    "status": true,
    "rationale": "the proof is fixture and transformation structure, not production quality"
  },
  "boundary_clear": {
    "status": true,
    "rationale": "live fetch, YMM4 materialization, render, audio/TTS, cards, and production claims remain closed"
  },
  "next_action_clear": {
    "status": true,
    "rationale": "newsroom-rss-topic-fixture-route-hardening-v1"
  },
  "visual_supports_explanation": {
    "status": true,
    "rationale": "animation remains optional metadata and is not a deliverable in this slice"
  }
}
```


## Recommendation Logic

```json
{
  "selected": "newsroom-rss-topic-fixture-route-hardening-v1",
  "if_v2_works_but_needs_validation_hardening": "newsroom-rss-topic-fixture-route-hardening-v1",
  "if_episode_capsule_route_is_dominant_weak_point": "newsroom-episode-capsule-route-hardening-v1",
  "if_offline_v2_strong_enough_and_live_boundary_is_dominant": "newsroom-live-rss-boundary-plan-v1",
  "if_new_materialization_proof_genuinely_needed": "newsroom-offline-rss-like-topic-fixture-v2-materialization-v1",
  "reason": "v2 now generates a bounded five-beat capsule, but it still relies on explicit placeholders; fixture validation/hardening should come before live RSS planning or another preview."
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
| no_animation_only_loop | True |
| no_primitive_or_tempo_loop | True |
| no_card_polish_loop | True |
| no_render_export_loop | True |
| no_live_RSS_or_network_fetch | True |
| no_local_ymmp_creation_or_modification | True |
| next_axis_remains_topic_RSS_to_episode_construction | newsroom-rss-topic-fixture-route-hardening-v1 |


## Completion Matrix

| gate | status |
| --- | --- |
| repo_state_verified | True |
| previous_route_audit_inspected | True |
| fixture_v2_created | True |
| fixture_v2_schema_contract_created | True |
| five_beat_capsule_generated | True |
| route_assessment_created | True |
| local_ymmp_created_or_honestly_skipped | skipped_by_scope |
| next_axis_selected | True |


## Boundary Note

This proof strengthens the offline input route and five-beat capsule mapping only. It creates no local .ymmp, launches no YMM4 process, renders nothing, fetches no live RSS/news, tunes no animation, redesigns no cards, and makes no production/public acceptance claim.
