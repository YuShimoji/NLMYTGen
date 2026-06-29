# Newsroom Background Animation MVP Policy v1

artifact_id: newsroom_background_animation_mvp_policy_v1_2026_06_29
schema_version: newsroom_background_animation_mvp_policy.v1
production_status: diagnostic_only
render_gate: L0_no_render
selected_next_axis: newsroom-background-animation-minimal-integrated-scene-probe-v1


## Source Context

```json
{
  "source_scene_preview_observation_path": "samples/_probe/newsroom_handoff/yukkuri_animation_scene_preview_observation_v1.json",
  "source_scene_choreography_contract_path": "samples/_probe/newsroom_handoff/yukkuri_animation_scene_choreography_contract_v1.json",
  "source_scene_choreography_probe_readback_path": "samples/_probe/newsroom_handoff/yukkuri_animation_scene_choreography_probe_v1.json",
  "repo_root": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage"
}
```


## Stop-Loss Policy

| rule_id | requirement | effect | default_state |
| --- | --- | --- | --- |
| no_more_primitive_only_iteration | Do not run more primitive-only tempo, angle, or expression iteration unless an integrated scene proves a specific primitive is blocking. | moves the bottleneck from isolated motion tuning to one actual explanation beat | active |
| body_forward_back_disabled_by_default | Disable body forward/back movement by default. | prevents the previous unstable depth-like drift from becoming the animation baseline | active |
| expression_changes_are_scene_events | Tie expression changes only to a scene event. | keeps expression swaps from becoming a mechanical cycle | active |
| single_nod_or_reaction_per_short_scene | Allow one nod or reaction per short scene. | keeps the character readable without repeated acknowledgement loops | active |
| speech_balloon_deferred | Defer speech balloon work. | avoids opening a new visual subsystem before the movement layer is useful | active |
| background_animation_support_layer | Treat background animation as an accent/support layer, not the main deliverable. | keeps story clarity and card fatigue reduction ahead of character acting complexity | active |
| next_proof_uses_actual_explanation_beat | Use an actual explanation beat for the next proof, not a standalone primitive demo. | tests whether the animation supports a real newsroom explanation moment | active |
| freeze_animation_if_integrated_scene_fails | If the next integrated scene still feels bad, freeze animation as minimal accent and return to RSS/story integration. | prevents the background animation track from consuming the mainline | active |


## Allowed Default Primitives

| primitive_id | allowed_default | constraint |
| --- | --- | --- |
| stable_pose | True | always allowed as the fallback state |
| one_expression_event | True | exactly one event when the explanation beat changes emotional state |
| one_short_nod_or_reaction | True | one reaction per short scene; no repeated nodding loop |
| small_lateral_emphasis | optional | only when the explanation beat gives a clear reason |


## Disabled By Default

| primitive_id | disabled_by_default | reason |
| --- | --- | --- |
| repeated_nodding | True | it reads as mechanical agreement rather than explanation support |
| mechanical_expression_cycling | True | expression changes must be tied to a scene event |
| body_forward_back_movement | True | the latest preview still shows instability around this class of motion |
| complex_speech_balloons | True | speech balloon acceptance has not been proven and is not needed for this gate |
| full_chaban_scene | True | the product need is an accent/support layer, not a character skit rewrite |


## Review Gate

| gate_id | question | pass_condition |
| --- | --- | --- |
| supports_explanation | Does the animation support the explanation? | the beat is easier to follow with the accent than without it |
| does_not_distract | Does it distract? | viewer attention remains on the newsroom explanation and card context |
| reduces_card_fatigue | Does it reduce card fatigue? | the short accent breaks static-card monotony without becoming the subject |
| introduces_no_confusion | Does it introduce confusion? | no movement implies the wrong direction, object, speaker, or causal claim |


## Business Goal Outcome Contract

```json
{
  "problem_clear": {
    "status": true,
    "rationale": "the problem is over-spending on primitive tuning after partial coherence is already proven"
  },
  "offer_clear": {
    "status": true,
    "rationale": "the offer is a minimal integrated background accent, not a full skit system"
  },
  "proof_clear": {
    "status": true,
    "rationale": "the next proof is one actual explanation beat, 10-20 seconds, one preview only"
  },
  "boundary_clear": {
    "status": true,
    "rationale": "no render, no audio/TTS, no media, no card redesign, and no production claim"
  },
  "next_action_clear": {
    "status": true,
    "rationale": "newsroom-background-animation-minimal-integrated-scene-probe-v1"
  },
  "visual_supports_explanation": {
    "status": "unknown_until_integrated_preview",
    "rationale": "primitive feasibility passed, but final animation quality is not accepted"
  }
}
```


## Next Recommended Axis

```json
{
  "selected": "newsroom-background-animation-minimal-integrated-scene-probe-v1",
  "reason": "Partial scene coherence and primitive feasibility are enough to stop isolated primitive tuning. The next useful proof is a minimal integrated explanation beat.",
  "fallback_if_bad": "newsroom-rss-dry-run-integration-plan-v1"
}
```


## Freeze Condition

```json
{
  "condition": "next_integrated_scene_still_feels_bad",
  "action": "freeze_animation_as_minimal_accent",
  "return_axis": "newsroom-rss-dry-run-integration-plan-v1"
}
```


## Not Accepted Scope

```json
{
  "render_proof": false,
  "render_export_required_now": false,
  "production_animation_quality": false,
  "public_upload_or_public_readiness": false,
  "real_rss_or_news_integration": false,
  "card_redesign_or_density_work": false,
  "dense_script_rewrite": false,
  "external_reference_video_fetch": false,
  "audio_or_tts_output": false,
  "actual_order_or_audience_acceptance": false,
  "speech_balloon_visual_acceptance": false
}
```


## Inertia Check

| gate | status |
| --- | --- |
| remote_parity_required_before_work | True |
| no_new_primitive_only_probe | True |
| no_repeated_visual_proof_request | True |
| integrated_scene_before_more_tuning | True |
| return_to_rss_story_integration_if_bad | newsroom-rss-dry-run-integration-plan-v1 |


## Boundary Note

This policy makes background animation an explanation support layer. It does not approve a full chaban scene, speech balloon system, render, audio/TTS, production quality, or public release.
