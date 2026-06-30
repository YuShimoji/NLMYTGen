# Newsroom Offline Topic Mini Episode Capsule With Animation Accent v1

artifact_id: newsroom_offline_topic_mini_episode_capsule_with_animation_accent_v1_2026_06_30
schema_version: newsroom_offline_topic_mini_episode_capsule_with_animation_accent.v1
production_status: diagnostic_only
render_gate: L0_no_render
live_fetch_used: false
selected_next_axis: newsroom-offline-topic-mini-episode-capsule-materialization-v1


## Identity

```json
{
  "capsule_id": "newsroom_offline_topic_mini_episode_capsule_with_animation_accent_v1_2026_06_30",
  "source_bridge_path": "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_bridge_v1.json",
  "source_topic_fixture_path": "samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json",
  "production_status": "diagnostic_only",
  "render_gate": "L0_no_render",
  "live_fetch_used": false
}
```


## Source Context

```json
{
  "repo_root": "C:\\Users\\PLANNER007\\NLMYTGen",
  "source_bridge_path": "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_bridge_v1.json",
  "source_preview_observation_path": "samples/_probe/newsroom_handoff/rss_dry_run_animated_beat_preview_observation_v1.json",
  "source_topic_fixture_path": "samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json",
  "source_animated_beat_contract_path": "samples/_probe/newsroom_handoff/rss_dry_run_animated_explanation_beat_contract_v1.json",
  "source_background_animation_mvp_freeze_path": "samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json",
  "prior_episode_capsule_path": "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json"
}
```


## Episode Capsule Summary

```json
{
  "episode_title": "Offline topic source-boundary mini explainer",
  "episode_goal": "prove that an offline RSS-like topic can become a small review-only explainer structure before any live source work",
  "beat_count": 5,
  "source_boundary_summary": "All claims remain offline fixture claims; no live RSS/news, source truth, rights, quotes, media, or publication readiness is accepted.",
  "animation_accent_summary": {
    "policy_status": "frozen_mvp_policy_carried_forward",
    "assignment_counts": {
      "stable_pose_only": 1,
      "expression_event": 1,
      "expression_plus_short_nod": 1,
      "short_nod_reaction": 1,
      "none": 1
    },
    "allowed_assignments": [
      "expression_event",
      "expression_plus_short_nod",
      "none",
      "short_nod_reaction",
      "stable_pose_only"
    ],
    "disabled": [
      "body forward/back",
      "repeated nodding",
      "mechanical expression cycle",
      "speech balloon",
      "full chaban scene",
      "animation-only probe loop",
      "tempo-only loop"
    ],
    "animation_optional_not_forced": true
  },
  "text_overlay_summary": "Plain TextItem and diagnostic label roles support comprehension; no polished card, production subtitle, or visual layout tuning is included.",
  "materialization_summary": {
    "local_ymmp_materialization_status": "blocked_or_deferred",
    "local_ymmp_created_in_this_slice": false,
    "planned_repo_relative_path_if_later": "_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_with_animation_accent_v1.ymmp",
    "reason": "Route is contract-clear but local multi-beat YMM4 materialization would be speculative in this slice.",
    "next_axis": "newsroom-offline-topic-mini-episode-capsule-materialization-v1"
  }
}
```


## Beat Table Summary

| beat_id | beat_function | explanation_line | animation_assignment | materialization_role | materialization_status | review_status |
| --- | --- | --- | --- | --- | --- | --- |
| offline_topic_mini_ep_beat_01_hook | hook / issue framing | A topic-like item is not a video yet; first prove the source boundary. | stable_pose_only | candidate_for_future_multi_beat_ymmp | existing_route_candidate | diagnostic_review_ready |
| offline_topic_mini_ep_beat_02_key_claim | explanation / key claim | The key claim stays diagnostic until source truth, rights, and fit are reviewed. | expression_event | capsule_contract_only | contract_only | diagnostic_review_ready |
| offline_topic_mini_ep_beat_03_source_warning | source-boundary warning | Offline fixture: verify source boundary before production. | expression_plus_short_nod | candidate_for_future_multi_beat_ymmp | existing_route_candidate | diagnostic_review_ready |
| offline_topic_mini_ep_beat_04_implication | implication / why it matters | That boundary lets the structure be checked without pretending it is publishable. | short_nod_reaction | capsule_contract_only | contract_only | diagnostic_review_ready |
| offline_topic_mini_ep_beat_05_close | close / next action | Next, build a small capsule with text roles and one frozen accent per beat. | none | capsule_contract_only | contract_only | diagnostic_review_ready |


## Mainline Route

```json
{
  "route_name": "offline_topic_bridge_to_diagnostic_mini_episode_capsule",
  "existing_artifacts_used": [
    "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_bridge_v1.json",
    "samples/_probe/newsroom_handoff/rss_dry_run_animated_beat_preview_observation_v1.json",
    "samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json",
    "samples/_probe/newsroom_handoff/rss_dry_run_animated_explanation_beat_contract_v1.json",
    "samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json",
    "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json"
  ],
  "new_artifacts_created": [
    "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_with_animation_accent_v1.json",
    "docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_CAPSULE_WITH_ANIMATION_ACCENT_V1_2026-06-30.md",
    "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_contract_v1.json",
    "src/pipeline/newsroom_offline_topic_mini_episode_capsule.py",
    "tests/test_newsroom_offline_topic_mini_episode_capsule.py"
  ],
  "transformation_steps": [
    "read the prior 5-beat bridge and current offline topic fixture",
    "promote bridge beats into a diagnostic episode capsule",
    "assign optional frozen animation accents without changing primitives",
    "carry forward plain TextItem and diagnostic label roles",
    "record that multi-beat local .ymmp materialization is deferred"
  ],
  "route_confidence": "high",
  "route_blockers": [
    "existing episode_production_capsule_v1 is an older fake-packet structural precedent, not the current offline topic route",
    "no verified PLANNER007 multi-beat YMM4 materialization route exists in this slice",
    "previous RSS dry-run .ymmp proof was host-local user evidence and is not required on PLANNER007"
  ],
  "next_required_route_work": [
    "newsroom-offline-topic-mini-episode-capsule-materialization-v1",
    "define a non-speculative multi-beat YMM4 materialization route before any preview request"
  ],
  "local_ymmp_materialization_status": "not_created_deferred"
}
```


## Local Artifact Access

```json
{
  "artifact_id": "local_ignored_offline_topic_mini_episode_capsule_candidate",
  "repo_relative_path": "_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_with_animation_accent_v1.ymmp",
  "folder_full_path_current_host": "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe",
  "file_full_path_current_host": "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe\\offline_topic_mini_episode_capsule_with_animation_accent_v1.ymmp",
  "target_exists": false,
  "access_state": "not_created_deferred",
  "access_evidence_level": "L1_IGNORED_PATH_CONFIRMED_NO_FILE",
  "artifact_scope": "ignored_local_only_if_created_later",
  "evidence_source": "current_host_filesystem_plus_git_check_ignore",
  "git_check_ignore_result": {
    "command": "git check-ignore -v -- _tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_with_animation_accent_v1.ymmp",
    "returncode": 0,
    "stdout": ".gitignore:37:_tmp/\t_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_with_animation_accent_v1.ymmp",
    "stderr": "",
    "ignored": true
  },
  "size": null,
  "item_type_counts": null,
  "defer_reason": "Route is contract-clear but local multi-beat YMM4 materialization would be speculative in this slice."
}
```


## Business Goal Outcome Contract

```json
{
  "problem_clear": {
    "status": true,
    "rationale": "this moves beyond one-beat proof into a complete 5-beat capsule"
  },
  "offer_clear": {
    "status": true,
    "rationale": "the artifact shows a small episode structure with hook, claim, warning, implication, and close"
  },
  "proof_clear": {
    "status": true,
    "rationale": "the proof is capsule/content-flow structure, not production quality"
  },
  "boundary_clear": {
    "status": true,
    "rationale": "card design, animation tuning, render, audio/TTS, and live RSS remain closed"
  },
  "next_action_clear": {
    "status": true,
    "rationale": "newsroom-offline-topic-mini-episode-capsule-materialization-v1"
  },
  "visual_supports_explanation": {
    "status": true,
    "rationale": "animation assignments are optional and subordinate to text/narration"
  }
}
```


## Recommendation Logic

```json
{
  "selected": "newsroom-offline-topic-mini-episode-capsule-materialization-v1",
  "if_capsule_contract_clear_but_no_local_ymmp": "newsroom-offline-topic-mini-episode-capsule-materialization-v1",
  "if_new_multi_beat_local_ymmp_exists_and_preview_adds_value": "newsroom-offline-topic-mini-episode-preview-operator-instruction-v1",
  "if_existing_route_is_unclear": "newsroom-episode-capsule-route-audit-v1",
  "if_topic_to_beat_is_too_synthetic": "newsroom-rss-topic-fixture-route-audit-v1",
  "if_offline_capsule_route_is_strong_and_source_boundary_is_next": "newsroom-live-rss-boundary-plan-v1",
  "reason": "The capsule contract is clear, but no non-speculative multi-beat local .ymmp was created; materialization should be its own next slice."
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
| next_axis_remains_episode_construction | newsroom-offline-topic-mini-episode-capsule-materialization-v1 |


## Completion Matrix

| gate | status |
| --- | --- |
| repo_state_verified | True |
| previous_bridge_inspected | True |
| five_beat_capsule_contract_created | True |
| mainline_route_confidence_recorded | True |
| local_ymmp_created_or_honestly_deferred | deferred |
| next_axis_selected | True |


## Boundary Note

This capsule is diagnostic-only. It creates no local .ymmp, no render, no audio/TTS, no live RSS/news fetch, no polished card, no production subtitle/card design, and no public or audience acceptance claim.
