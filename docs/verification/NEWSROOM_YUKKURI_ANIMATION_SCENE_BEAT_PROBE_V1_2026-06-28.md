# Newsroom Yukkuri Animation Scene Beat Probe v1

artifact_id: newsroom_yukkuri_animation_scene_beat_probe_v1_2026_06_28
schema_version: newsroom_yukkuri_animation_scene_beat_probe.v1
production_status: diagnostic_only
render_gate: L0_no_render
next_recommended_axis: newsroom-yukkuri-animation-primitive-render-smoke-v1


## Scene Beat Policy

```json
{
  "not_a_dense_script_rewrite": true,
  "animation_supports_explanation": true,
  "one_beat_one_scene_function": true,
  "fallback_preserves_narration_meaning": true
}
```


## Beats

| beat_id | scene_function | speaker_or_character | narration_or_caption_role | primitive_ids_used | timing_range | card_overlay_relationship | fallback_if_animation_missing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| beat_01 | viewer_question_reaction | reimu | caption states the viewer question; balloon is a short visual cue only | ["expression_swap", "speech_balloon"] | 0-8 sec | none; avoid card restart | static concerned face plus subtitle |
| beat_02 | explanation_response | reimu | narration explains the mechanism while character acknowledges it | ["head_nod", "small_position_move"] | 8-18 sec | optional small point label | static character at rest pose |
| beat_03 | proof_emphasis | background performer | caption references proof chain; entrance makes the situation concrete | ["character_entrance_exit", "small_position_move"] | 18-34 sec | proof card may appear as bounded support | no entrance; use one static prop/character image |
| beat_04 | boundary_warning | reimu | caption keeps source/rights limits explicit | ["expression_swap", "speech_balloon"] | 34-48 sec | boundary note only if needed | warning subtitle without balloon |
| beat_05 | next_action_close | reimu | caption names next user-visible action without dense script rewrite | ["head_nod", "character_entrance_exit"] | 48-60 sec | small next-action card optional | static close pose plus subtitle |


## Primitive Coverage

```json
{
  "all_selected_primitives_used": true,
  "coverage": {
    "head_nod": [
      "beat_02",
      "beat_05"
    ],
    "expression_swap": [
      "beat_01",
      "beat_04"
    ],
    "character_entrance_exit": [
      "beat_03",
      "beat_05"
    ],
    "small_position_move": [
      "beat_02",
      "beat_03"
    ],
    "speech_balloon": [
      "beat_01",
      "beat_04"
    ]
  }
}
```


## Not Accepted Scope

```json
{
  "render_proof": false,
  "ymmp_committed": false,
  "production_animation_quality": false,
  "public_upload_or_public_readiness": false,
  "real_rss_or_news_integration": false,
  "external_reference_video_fetch": false,
  "copied_external_visuals": false,
  "actual_order_or_audience_acceptance": false
}
```


## Boundaries

```json
{
  "YMM4_launched_by_agent": false,
  "render_performed_by_agent": false,
  "source_ymmp_edited_by_hand": false,
  "ymmp_staged_or_committed": false,
  "audio_tts_generated": false,
  "cards_modified": false,
  "real_rss_or_news_fetched": false,
  "external_reference_videos_fetched": false,
  "production_public_readiness_claimed": false,
  "actual_audience_acceptance_claimed": false
}
```
