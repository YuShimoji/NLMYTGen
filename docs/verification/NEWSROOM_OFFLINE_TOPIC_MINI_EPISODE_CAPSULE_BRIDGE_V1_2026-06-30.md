# Newsroom Offline Topic Mini Episode Capsule Bridge v1

artifact_id: newsroom_offline_topic_mini_episode_capsule_bridge_v1_2026_06_30
schema_version: newsroom_offline_topic_mini_episode_capsule_bridge.v1
production_status: diagnostic_only
render_gate: L0_no_render
selected_next_axis: newsroom-offline-topic-mini-episode-capsule-with-animation-accent-v1


## Source Context

```json
{
  "source_rss_dry_run_topic_to_beat_path": "samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json",
  "source_rss_dry_run_contract_path": "samples/_probe/newsroom_handoff/rss_dry_run_animated_explanation_beat_contract_v1.json",
  "source_rss_dry_run_doc_path": "docs/verification/NEWSROOM_RSS_DRY_RUN_TO_ANIMATED_EXPLANATION_BEAT_V1_2026-06-30.md",
  "source_background_animation_mvp_freeze_path": "samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json",
  "source_episode_capsule_path": "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json",
  "source_minimal_episode_packet_path": "samples/_probe/newsroom_handoff/minimal_episode_packet.json",
  "repo_root": "C:\\Users\\PLANNER007\\NLMYTGen"
}
```


## Existing Route Assessment

```json
{
  "one_beat_route": {
    "path": "samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json",
    "status": "available_current_topic_route",
    "use": "per-beat text role, source-boundary role, and frozen accent policy"
  },
  "prior_episode_capsule_route": {
    "path": "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json",
    "status": "structural_precedent_not_current_topic",
    "use": "episode/capsule shape reference only; it comes from an older fake packet"
  },
  "minimal_episode_packet_route": {
    "path": "samples/_probe/newsroom_handoff/minimal_episode_packet.json",
    "status": "fixture_shape_reference_not_materialization_target",
    "use": "beat ordering precedent only; no current RSS dry-run materialization"
  },
  "smallest_safe_bridge": "create a 5-beat contract from the current offline topic without creating another .ymmp or requesting another preview",
  "route_clarity": "clear_for_contract_bridge"
}
```


## Offline Topic Input

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


## Mini Episode Capsule Summary

```json
{
  "capsule_id": "offline_topic_mini_episode_capsule_bridge_v1",
  "capsule_status": "diagnostic_contract_bridge_only",
  "source_topic_id": "offline_rss_like_topic_fixture_001",
  "episode_scope": "small offline diagnostic mini episode; content-flow proof only",
  "beat_count": 5,
  "materialization_summary": {
    "status_counts": {
      "existing_route_candidate": 2,
      "contract_only": 3
    },
    "local_ymmp_created_in_this_slice": false,
    "materialization_decision": "bridge only; use existing one-beat route as a candidate and defer multi-beat YMM4 materialization to the selected next axis"
  }
}
```


## Mini Episode Beats

| beat_id | beat_function | explanation_line | subtitle_or_text_role | minimal_overlay_role | background_animation_accent_role | source_boundary_role | materialization_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| offline_topic_mini_ep_beat_01_hook | hook / issue framing | A topic-like item is not a video yet; first prove the source boundary. | plain TextItem hook; not final subtitle styling | short diagnostic label for the issue frame | stable pose plus one light reaction after the issue is named | reminds that the topic is an offline fixture only | existing_route_candidate |
| offline_topic_mini_ep_beat_02_key_claim | explanation / key claim | The key claim stays diagnostic until source truth, rights, and fit are reviewed. | plain TextItem explanation line | source-check label, not a designed card | one expression event tied to the key claim | keeps source truth and rights approval unaccepted | contract_only |
| offline_topic_mini_ep_beat_03_source_warning | source-boundary warning | Offline fixture: verify source boundary before production. | plain diagnostic TextItem boundary warning | current proven plain TextItem role; no card-like overlay | frozen MVP accent remains subordinate to the warning text | no live RSS, source quote, external media, or publication readiness | existing_route_candidate |
| offline_topic_mini_ep_beat_04_implication | implication / why it matters | That boundary lets the structure be checked without pretending it is publishable. | plain TextItem implication line | small readback label for why the proof matters | one short nod/reaction after the implication | separates structural confidence from public-source confidence | contract_only |
| offline_topic_mini_ep_beat_05_close | close / next action | Next, build a small capsule with text roles and one frozen accent per beat. | plain TextItem next-action line | next-step label only | return to stable pose at close | keeps live RSS/news and production acceptance out of scope | contract_only |


## Business Goal Outcome Contract

```json
{
  "problem_clear": {
    "status": true,
    "rationale": "the user preview closes the local one-beat visual proof loop"
  },
  "offer_clear": {
    "status": true,
    "rationale": "the work moves from one beat to a 5-beat mini episode contract"
  },
  "proof_clear": {
    "status": true,
    "rationale": "the proof is content-flow structure, not production quality"
  },
  "boundary_clear": {
    "status": true,
    "rationale": "card design, subtitle design, animation tuning, render, and live RSS stay closed"
  },
  "next_action_clear": {
    "status": true,
    "rationale": "newsroom-offline-topic-mini-episode-capsule-with-animation-accent-v1"
  },
  "visual_supports_explanation": {
    "status": true,
    "rationale": "the accent policy stays subordinate to narration/text on every beat"
  }
}
```


## Recommendation Logic

```json
{
  "preferred_default": "newsroom-offline-topic-mini-episode-capsule-with-animation-accent-v1",
  "selected": "newsroom-offline-topic-mini-episode-capsule-with-animation-accent-v1",
  "if_existing_episode_capsule_route_is_unclear": "newsroom-episode-capsule-route-audit-v1",
  "if_topic_to_beat_transformation_is_too_synthetic": "newsroom-rss-topic-fixture-route-audit-v1",
  "if_animation_should_remain_frozen": "newsroom-animation-accent-policy-closed-return-to-episode-capsule-v1",
  "reason": "The bridge is clear enough to move into a small offline capsule with the frozen accent policy, while avoiding animation-only, card-polish, render, and live-source loops."
}
```


## Not Accepted Scope

```json
{
  "production_subtitle_design": false,
  "production_card_design": false,
  "production_animation_quality": false,
  "public_upload_or_public_readiness": false,
  "real_rss_or_news_integration": false,
  "real_source_truth_approved": false,
  "external_reference_video_fetch": false,
  "card_redesign_or_density_work": false,
  "dense_script_rewrite": false,
  "render_export_proof": false,
  "audio_or_tts_output": false,
  "actual_order_or_audience_acceptance": false,
  "speech_balloon_visual_acceptance": false
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
| next_axis_remains_mainline_episode_construction | newsroom-offline-topic-mini-episode-capsule-with-animation-accent-v1 |


## Completion Matrix

| gate | status |
| --- | --- |
| repo_state_verified | True |
| preview_observation_recorded | True |
| one_beat_visual_integration_gate_closed | True |
| mini_episode_capsule_bridge_created | True |
| next_axis_selected | True |


## Boundary Note

This is a diagnostic bridge from one offline topic-derived beat to a small capsule contract. It creates no new .ymmp, no render, no audio/TTS, no live RSS/news fetch, no designed card, and no public or production acceptance claim.
