# Newsroom Offline Topic Mini Episode Capsule Materialization v1

artifact_id: newsroom_offline_topic_mini_episode_capsule_materialization_v1_2026_06_30
schema_version: newsroom_offline_topic_mini_episode_capsule_materialization.v1
production_status: diagnostic_only
render_gate: L0_no_render
local_ymmp_materialization_status: materialized_ignored_local_probe
selected_next_axis: newsroom-offline-topic-mini-episode-preview-operator-instruction-v1


## Materialization Route

```json
{
  "artifact_id": "newsroom_offline_topic_mini_episode_materialization_route_v1_2026_06_30",
  "route_id": "newsroom_offline_topic_mini_episode_materialization_route_v1_2026_06_30",
  "schema_version": "newsroom_offline_topic_mini_episode_materialization_route.v1",
  "review_status": "ready_for_supervisor_review",
  "production_status": "diagnostic_only",
  "diagnostic_only": true,
  "render_gate": "L0_no_render",
  "source_capsule_path": "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_with_animation_accent_v1.json",
  "source_capsule_contract_path": "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_contract_v1.json",
  "source_topic_fixture_path": "samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json",
  "route_classification": "current_supported",
  "route_confidence": "high",
  "existing_artifacts_used": [
    "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_with_animation_accent_v1.json",
    "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_contract_v1.json",
    "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_bridge_v1.json",
    "samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json",
    "samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json",
    "samples/nod_head.ymmp"
  ],
  "stale_fake_packet_route_classification": {
    "path": "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json",
    "classification": "stale_fake_packet_only",
    "used_for_materialization": false,
    "reason": "older fake-packet capsule is not the current offline-topic route"
  },
  "transformation_steps": [
    "read the current offline-topic 5-beat capsule",
    "create one sequential timeline segment per capsule beat",
    "insert one plain TextItem per beat as the diagnostic text role",
    "clone tracked nod_head character items only for beats with a capsule animation assignment",
    "keep body X fixed and use at most one expression or short nod per relevant beat",
    "write the result to an ignored local YMM4 diagnostic project"
  ],
  "output_artifacts": [
    {
      "path": "samples/_probe/newsroom_handoff/offline_topic_mini_episode_materialization_route_v1.json",
      "scope": "tracked_route_readback"
    },
    {
      "path": "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_materialization_v1.json",
      "scope": "tracked_materialization_readback"
    },
    {
      "path": "docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_CAPSULE_MATERIALIZATION_V1_2026-06-30.md",
      "scope": "tracked_verification_doc"
    },
    {
      "path": "_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp",
      "scope": "ignored_local_only"
    }
  ],
  "item_semantics": {
    "TextItem role": "one visible plain diagnostic text/caption role per beat",
    "GroupItem/ImageItem animation accent role": "frozen optional character accent from tracked nod_head source; no body forward/back and no full chaban scene",
    "beat timing role": "5 sequential beats, 360 frames each, 1800 frames total at 60 fps",
    "source boundary role": "each beat carries offline fixture/source-boundary text"
  },
  "route_blockers": [],
  "next_required_route_work": [
    "local ignored YMM4 diagnostic materialization in this slice",
    "newsroom-offline-topic-mini-episode-preview-operator-instruction-v1"
  ],
  "boundaries": {
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
    "actual_order_or_audience_acceptance_claimed": false,
    "stale_fake_packet_route_used_as_current": false
  }
}
```


## Local Probe Access State

```json
{
  "artifact_id": "local_ignored_offline_topic_mini_episode_materialized_probe",
  "repo_relative_path": "_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp",
  "folder_full_path_current_host": "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe",
  "file_full_path_current_host": "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe\\offline_topic_mini_episode_capsule_materialized_v1.ymmp",
  "launcher_or_open_command": "Invoke-Item -LiteralPath \"C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe\\offline_topic_mini_episode_capsule_materialized_v1.ymmp\"",
  "target_exists": true,
  "access_state": "verified_present",
  "access_evidence_level": "L3_VERIFIED_PRESENT",
  "artifact_scope": "ignored_local_only",
  "evidence_source": "current_host_filesystem_plus_git_check_ignore",
  "git_check_ignore_result": {
    "command": "git check-ignore -v -- _tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp",
    "returncode": 0,
    "stdout": ".gitignore:37:_tmp/\t_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp",
    "stderr": "",
    "ignored": true
  },
  "size": 267302
}
```


## Materialization Readback

```json
{
  "readback_status": "structural_pass",
  "artifact_id": "local_ignored_offline_topic_mini_episode_materialized_probe",
  "repo_relative_path": "_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp",
  "folder_full_path_current_host": "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe",
  "file_full_path_current_host": "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe\\offline_topic_mini_episode_capsule_materialized_v1.ymmp",
  "target_exists": true,
  "access_state": "verified_present",
  "access_evidence_level": "L3_VERIFIED_PRESENT",
  "artifact_scope": "ignored_local_only",
  "evidence_source": "current_host_filesystem_plus_git_check_ignore",
  "git_check_ignore_result": {
    "command": "git check-ignore -v -- _tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp",
    "returncode": 0,
    "stdout": ".gitignore:37:_tmp/\t_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp",
    "stderr": "",
    "ignored": true
  },
  "size": 267302,
  "file_sha256": "3e7c8e8cbd02c255a66a775fced40696884065266612a5a7e94fffdd0b04d28c",
  "item_type_counts": {
    "TextItem": 5,
    "GroupItem": 8,
    "ImageItem": 8
  },
  "unexpected_item_types": [],
  "beat_count": 5,
  "text_item_count": 5,
  "animation_item_count": 16,
  "duration_frames": 1800,
  "fps": 60,
  "per_beat_mapping": [
    {
      "beat_id": "offline_topic_mini_ep_beat_01_hook",
      "text_item_present": true,
      "text_item_text": "A topic-like item is not a video yet; first prove the source boundary.",
      "animation_accent_assignment": "stable_pose_only",
      "animation_item_count": 4,
      "start_frame": 0,
      "duration_frames": 360,
      "source_boundary_role": "reminds that the topic is an offline fixture only",
      "parent_x_values": [
        -96.0
      ],
      "head_rotation_values": [
        0.0
      ]
    },
    {
      "beat_id": "offline_topic_mini_ep_beat_02_key_claim",
      "text_item_present": true,
      "text_item_text": "The key claim stays diagnostic until source truth, rights, and fit are reviewed.",
      "animation_accent_assignment": "expression_event",
      "animation_item_count": 4,
      "start_frame": 360,
      "duration_frames": 360,
      "source_boundary_role": "keeps source truth and rights approval unaccepted",
      "parent_x_values": [
        -96.0
      ],
      "head_rotation_values": [
        0.0
      ]
    },
    {
      "beat_id": "offline_topic_mini_ep_beat_03_source_warning",
      "text_item_present": true,
      "text_item_text": "Offline fixture: verify source boundary before production.",
      "animation_accent_assignment": "expression_plus_short_nod",
      "animation_item_count": 4,
      "start_frame": 720,
      "duration_frames": 360,
      "source_boundary_role": "no live RSS, source quote, external media, or publication readiness",
      "parent_x_values": [
        -96.0
      ],
      "head_rotation_values": [
        0.0,
        -8.0,
        0.0
      ]
    },
    {
      "beat_id": "offline_topic_mini_ep_beat_04_implication",
      "text_item_present": true,
      "text_item_text": "That boundary lets the structure be checked without pretending it is publishable.",
      "animation_accent_assignment": "short_nod_reaction",
      "animation_item_count": 4,
      "start_frame": 1080,
      "duration_frames": 360,
      "source_boundary_role": "separates structural confidence from public-source confidence",
      "parent_x_values": [
        -96.0
      ],
      "head_rotation_values": [
        0.0,
        -8.0,
        0.0
      ]
    },
    {
      "beat_id": "offline_topic_mini_ep_beat_05_close",
      "text_item_present": true,
      "text_item_text": "Next, build a small capsule with text roles and one frozen accent per beat.",
      "animation_accent_assignment": "none",
      "animation_item_count": 0,
      "start_frame": 1440,
      "duration_frames": 360,
      "source_boundary_role": "keeps live RSS/news and production acceptance out of scope",
      "parent_x_values": [],
      "head_rotation_values": []
    }
  ],
  "YMM4_launch_status": "not_launched",
  "render_status": "not_rendered",
  "audio_tts_status": "not_created"
}
```


## Capsule Acceptance Readback

```json
{
  "five_beats_are_represented": true,
  "text_role_exists_per_beat": true,
  "animation_accent_remains_subordinate": true,
  "no_body_forward_back_default": true,
  "no_mechanical_expression_cycling": true,
  "no_card_polish": true,
  "no_render_export": true,
  "no_live_fetch": true,
  "no_production_claim": true
}
```


## Business Goal Outcome Contract

```json
{
  "problem_clear": {
    "status": true,
    "rationale": "the slice moves beyond contract-only capsule by creating a local ignored multi-beat YMM4 diagnostic project"
  },
  "offer_clear": {
    "status": true,
    "rationale": "the materialization shows how five beats map to TextItems and optional accents"
  },
  "proof_clear": {
    "status": true,
    "rationale": "the proof is route/materialization structure, not production quality"
  },
  "boundary_clear": {
    "status": true,
    "rationale": "card design, animation tuning, render, audio/TTS, and live RSS remain closed"
  },
  "next_action_clear": {
    "status": true,
    "rationale": "newsroom-offline-topic-mini-episode-preview-operator-instruction-v1"
  },
  "visual_supports_explanation": {
    "status": true,
    "rationale": "animation is optional, subordinate, and absent on the close beat"
  }
}
```


## Recommendation Logic

```json
{
  "selected": "newsroom-offline-topic-mini-episode-preview-operator-instruction-v1",
  "if_new_multi_beat_local_ymmp_exists_and_preview_adds_value": "newsroom-offline-topic-mini-episode-preview-operator-instruction-v1",
  "if_existing_route_is_unclear": "newsroom-episode-capsule-route-audit-v1",
  "if_route_clear_but_implementation_incomplete": "newsroom-offline-topic-mini-episode-materialization-implementation-v1",
  "if_topic_to_beat_is_too_synthetic": "newsroom-rss-topic-fixture-route-audit-v1",
  "if_offline_capsule_route_is_strong_and_source_boundary_is_next": "newsroom-live-rss-boundary-plan-v1",
  "reason": "A new multi-beat ignored local .ymmp exists, access is verified, and one bounded preview can test the episode-level co-presence."
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
  "local_ignored_ymmp_created_in_this_slice": true,
  "ymmp_or_media_staged_or_committed": false,
  "production_public_readiness_claimed": false,
  "actual_order_or_audience_acceptance_claimed": false,
  "stale_fake_packet_route_used_as_current": false
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
| no_stale_fake_packet_route_overclaim | True |
| next_axis_remains_episode_construction | newsroom-offline-topic-mini-episode-preview-operator-instruction-v1 |


## Completion Matrix

| gate | status |
| --- | --- |
| repo_state_verified | True |
| previous_capsule_inspected | True |
| materialization_route_classified | current_supported |
| local_ymmp_created_or_honestly_deferred | created |
| materialization_readback_created | True |
| next_axis_selected | True |


## Boundary Note

This materialization creates an ignored local diagnostic .ymmp only. It does not launch YMM4, render, create audio/TTS, fetch live RSS/news, redesign cards, accept production subtitle/card design, or claim public readiness.
