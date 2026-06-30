# Runtime State — NLMYTGen

- **Newsroom terminal resume remote sync handoff v3 completed (2026-06-30 JST)**:
  `newsroom-terminal-resume-remote-sync-handoff-v3` records the current
  PLANNER007 restart context after
  `84f4406 docs: add offline rss fixture v2 capsule`. New tracked handoff
  artifacts are
  `samples/_probe/newsroom_handoff/terminal_resume_remote_sync_handoff_v3.json`
  and
  `docs/verification/NEWSROOM_TERMINAL_RESUME_REMOTE_SYNC_HANDOFF_V3_2026-06-30.md`,
  plus this runtime pointer and the matching decision-log entry in
  `docs/project-context.md`. The latest product slice remains
  `newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1`:
  offline RSS-like fixture v2, schema contract, and five-beat diagnostic
  capsule are tracked; the route is `current_partial`, diagnostic-only,
  stronger than v1, not blocked, and still synthetic because source URL,
  freshness, and rights are placeholders. On another terminal, restart with
  `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, this top runtime entry, then
  `docs/verification/NEWSROOM_TERMINAL_RESUME_REMOTE_SYNC_HANDOFF_V3_2026-06-30.md`
  if more detail is needed. The expected synced state after pull is
  `master`, `HEAD...origin/master = 0 0`, and a tracked-clean worktree except
  ignored `_tmp`. No Agent-side YMM4 launch, render, `.ymmp`
  creation/modification/stage/commit, media/audio/TTS generation, live
  RSS/news fetch, card redesign, animation tuning, production/public readiness
  claim, or audience/order acceptance claim occurred. The selected next axis
  is `newsroom-rss-topic-fixture-route-hardening-v1`.
- **Newsroom offline RSS-like topic fixture v2 to mini episode capsule completed (2026-06-30 JST)**:
  `newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1`
  strengthens the prior offline RSS-like topic route after
  `rss_topic_fixture_route_audit_v1` classified v1 as diagnostic-only,
  reusable, but too synthetic. New tracked artifacts are
  `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2.json`,
  `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_schema_contract_v1.json`,
  `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1.json`,
  `docs/verification/NEWSROOM_OFFLINE_RSS_LIKE_TOPIC_FIXTURE_V2_TO_MINI_EPISODE_CAPSULE_V1_2026-06-30.md`,
  `src/pipeline/newsroom_offline_rss_like_topic_fixture_v2.py`, and
  `tests/test_newsroom_offline_rss_like_topic_fixture_v2.py`. The v2 fixture
  now carries the required source, placeholder URL, placeholder published time,
  summary, key claim, why-it-matters, boundary, rights, intended angle,
  excluded claims, and diagnostic production status fields, plus source kind,
  language, category, attribution/freshness/reliability notes, editorial risk,
  and materialization notes. The route generates a five-beat diagnostic mini
  episode capsule: hook, key claim, source-boundary warning, implication, and
  close. Animation remains frozen optional metadata only
  (`stable_pose_only`, `expression_event`, `expression_plus_short_nod`,
  `short_nod_reaction`, `none`) and no YMM4 project is created or modified.
  The route is classified as `current_partial`: diagnostic-only and a reusable
  fixture candidate, stronger than v1, not blocked, but still synthetic because
  source URL, freshness, and rights remain placeholders. No Agent-side YMM4
  launch, render, `.ymmp` creation/modification/stage/commit, media/audio/TTS
  generation, live RSS/news fetch, card redesign, animation tuning,
  production/public readiness claim, or audience/order acceptance claim
  occurred. The selected next axis is
  `newsroom-rss-topic-fixture-route-hardening-v1`.
- **Newsroom offline topic readable preview readback and RSS topic fixture route audit completed (2026-06-30 JST)**:
  `newsroom-offline-topic-readable-preview-readback-and-rss-topic-fixture-route-audit-v1`
  records the user-side preview observation for
  `_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v2_readable_text.ymmp`.
  The readable v2 preview passes with boundary: YMM4 opened, five TextItems
  were visible, the five visible lines were human-readable hook / key claim /
  warning / implication / close beats, debug labels were not the primary
  screen text, and the animation accent was not reported as blocking. This
  closes the current YMM4 visual gate for now; no further YMM4 preview is
  requested in this slice. New tracked artifacts are
  `samples/_probe/newsroom_handoff/offline_topic_mini_episode_readable_preview_observation_v1.json`,
  `docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_READABLE_PREVIEW_OBSERVATION_V1_2026-06-30.md`,
  `samples/_probe/newsroom_handoff/rss_topic_fixture_route_audit_v1.json`,
  `docs/verification/NEWSROOM_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_V1_2026-06-30.md`,
  `src/pipeline/newsroom_rss_topic_fixture_route_audit.py`, and
  `tests/test_newsroom_rss_topic_fixture_route_audit.py`. The audit classifies
  the current offline RSS-like topic route as diagnostic-only and a reusable
  fixture candidate, but still too synthetic for safer episode generation:
  it has `topic_id`, `title`, `source_kind`, `key_fact_or_claim`,
  `explanation_angle`, and `boundary_note`, but lacks explicit `source_name`,
  `source_url_or_placeholder`, `published_at_or_placeholder`, `summary`,
  `rights_status`, and `excluded_claims`. Route confidence is `medium`, not
  blocked. The recommended minimal v2 fixture schema now requires
  `topic_id`, `title`, `source_name`, `source_url_or_placeholder`,
  `published_at_or_placeholder`, `summary`, `key_claim`, `why_it_matters`,
  `uncertainty_or_boundary`, `rights_status`, `intended_episode_angle`,
  `excluded_claims`, and `production_status`. No Agent-side YMM4 launch,
  render, `.ymmp` creation/stage/commit, media/audio/TTS generation, live
  RSS/news fetch, card redesign, animation tuning, production/public readiness
  claim, or audience/order acceptance claim occurred. The selected next axis is
  `newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1`.
- **Newsroom offline topic mini episode readable text materialization completed (2026-06-30 JST)**:
  `newsroom-offline-topic-mini-episode-readable-text-materialization-v1`
  records the user-side preview observation for
  `_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp`.
  The v1 preview is accepted only for route/materialization structure:
  five TextItems appeared sequentially, the character accent was in the same
  scene/timing, and the accent was not disruptive. It is not accepted as
  human-readable mini episode text because the screen-facing notes observed by
  the user were debug labels such as
  `offline_topic_mini_episode:text:offline_topic_mini_ep_beat_01_hook`.
  New tracked artifacts are
  `samples/_probe/newsroom_handoff/offline_topic_mini_episode_preview_observation_v1.json`,
  `docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_PREVIEW_OBSERVATION_V1_2026-06-30.md`,
  `samples/_probe/newsroom_handoff/offline_topic_mini_episode_readable_text_materialization_v1.json`,
  `docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_READABLE_TEXT_MATERIALIZATION_V1_2026-06-30.md`,
  `src/pipeline/newsroom_offline_topic_mini_episode_readable_text_materialization.py`,
  and
  `tests/test_newsroom_offline_topic_mini_episode_readable_text_materialization.py`.
  The v2 ignored local diagnostic project exists at
  `_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v2_readable_text.ymmp`
  and is verified ignored by `.gitignore` `_tmp/`. It preserves the v1 route,
  timing, and frozen animation accent policy while replacing the five
  screen-facing TextItem `Text` and `Remark` values with short English
  explanation lines. English is used because the Japanese examples supplied to
  this slice were mojibake in the prompt and the existing capsule route already
  used ASCII English safely. Readback passes with 60 fps / 1800 frames,
  5 beats, 5 `TextItem`s, 8 `GroupItem`s, 8 `ImageItem`s, 16 animation items,
  `debug_label_visible_count=0`, and
  `human_readable_text_item_count=5`. No Agent-side YMM4 launch, render,
  `.ymmp` stage/commit, media/audio/TTS generation, live RSS/news fetch, card
  redesign, animation tuning, production/public readiness claim, or
  audience/order acceptance claim occurred. The selected next axis is
  `newsroom-offline-topic-mini-episode-readable-preview-operator-instruction-v1`.
- **Newsroom offline topic mini episode capsule materialization completed (2026-06-30 JST)**:
  `newsroom-offline-topic-mini-episode-capsule-materialization-v1`
  classifies the current offline-topic multi-beat YMM4 route as
  `current_supported` and materializes the 5-beat capsule into the ignored
  local diagnostic project
  `_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp`.
  The route uses only the current offline-topic capsule/contract/bridge,
  `rss_dry_run_topic_to_animated_explanation_beat_v1`, the frozen background
  animation policy, and tracked `samples/nod_head.ymmp`; the older
  `episode_production_capsule_v1` is explicitly classified as
  `stale_fake_packet_only` and is not used as the current route. New tracked
  artifacts are
  `samples/_probe/newsroom_handoff/offline_topic_mini_episode_materialization_route_v1.json`,
  `samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_materialization_v1.json`,
  `docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_CAPSULE_MATERIALIZATION_V1_2026-06-30.md`,
  `src/pipeline/newsroom_offline_topic_mini_episode_materialization.py`, and
  `tests/test_newsroom_offline_topic_mini_episode_materialization.py`. The
  local ignored `.ymmp` exists on PLANNER007, is verified ignored by
  `.gitignore` `_tmp/`, and must remain untracked/uncommitted. Readback passes
  with a 60 fps / 1800-frame timeline, 5 beats, 5 `TextItem`s, 8 `GroupItem`s,
  8 `ImageItem`s, 16 animation items, one plain diagnostic text role per beat,
  no card/shape/audio/video items, fixed parent X `-96.0` for all animation
  accents, and no animation on the close beat. No Agent-side YMM4 launch,
  render, `.ymmp` stage/commit, media/audio/TTS generation, live RSS/news
  fetch, card redesign, animation tuning, production/public readiness claim,
  or audience/order acceptance claim occurred. The selected next axis is
  `newsroom-offline-topic-mini-episode-preview-operator-instruction-v1`.
- **Newsroom offline topic mini episode capsule with animation accent completed (2026-06-30 JST)**:
  `newsroom-offline-topic-mini-episode-capsule-with-animation-accent-v1`
  advances the previous bridge into a diagnostic 5-beat mini episode capsule
  contract from the offline RSS-like topic fixture. New tracked artifacts are
  `samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_with_animation_accent_v1.json`,
  `docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_CAPSULE_WITH_ANIMATION_ACCENT_V1_2026-06-30.md`,
  `samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_contract_v1.json`,
  `src/pipeline/newsroom_offline_topic_mini_episode_capsule.py`, and
  `tests/test_newsroom_offline_topic_mini_episode_capsule.py`. The capsule has
  five beats: hook / issue framing, explanation / key claim, source-boundary
  warning, implication / why it matters, and close / next action. Each beat
  carries narration intent, plain `TextItem` / diagnostic label roles, source
  boundary role, materialization role, and diagnostic review status. The
  frozen MVP animation policy is carried forward with optional assignments
  only: `stable_pose_only`, `expression_event`, `expression_plus_short_nod`,
  `short_nod_reaction`, and `none`; body forward/back movement, repeated
  nodding, mechanical expression cycling, speech balloons, full chaban scenes,
  animation-only probe loops, and tempo-only loops remain disabled. Existing
  `episode_production_capsule_v1` is classified as an older fake-packet
  structural precedent, not the current offline-topic materialization route.
  No local `.ymmp` was created because PLANNER007 does not yet have a verified
  non-speculative multi-beat YMM4 materialization route; the planned ignored
  path
  `_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_with_animation_accent_v1.ymmp`
  is verified ignored and recorded as `not_created_deferred`. No Agent-side
  YMM4 launch, render, `.ymmp` stage/commit, media/audio/TTS generation, live
  RSS/news fetch, card redesign, animation tuning, production/public readiness
  claim, or audience/order acceptance claim occurred. The selected next axis is
  `newsroom-offline-topic-mini-episode-capsule-materialization-v1`.
- **Newsroom RSS dry-run animated beat preview readback and mini episode capsule bridge completed (2026-06-30 JST)**:
  `newsroom-rss-dry-run-animated-beat-preview-readback-and-mini-episode-capsule-bridge-v1`
  records the user-side preview observation for the ignored local RSS dry-run
  animated beat. The user opened
  `_tmp/newsroom_manual_probe/rss_dry_run_animated_explanation_beat_v1.ymmp`
  in YMM4 and saw the plain topic-derived `TextItem`
  `Offline fixture: verify source boundary before production.` plus the
  character animation accent at the same scene timing. This closes the
  one-beat visual integration gate as
  `content_flow_visual_status=pass_with_boundary`, not as production subtitle
  design, production card design, render quality, public readiness, or
  audience/order acceptance. New tracked artifacts are
  `samples/_probe/newsroom_handoff/rss_dry_run_animated_beat_preview_observation_v1.json`,
  `docs/verification/NEWSROOM_RSS_DRY_RUN_ANIMATED_BEAT_PREVIEW_OBSERVATION_V1_2026-06-30.md`,
  `samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_bridge_v1.json`,
  `docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_CAPSULE_BRIDGE_V1_2026-06-30.md`,
  `src/pipeline/newsroom_offline_topic_mini_episode_capsule_bridge.py`, and
  `tests/test_newsroom_offline_topic_mini_episode_capsule_bridge.py`. The
  current `C:\Users\PLANNER007\NLMYTGen` workspace does not contain the ignored
  local `.ymmp` that the user opened on the earlier `C:\Users\thank\...`
  host path; this is recorded as host-local `_tmp` state and was not recreated.
  No Agent-side YMM4 launch, render, `.ymmp` creation/stage/commit,
  media/audio/TTS generation, live RSS/news fetch, card redesign, animation
  tuning, production/public readiness claim, or audience/order acceptance
  claim occurred. The bridge creates a 5-beat offline diagnostic mini episode
  capsule contract: hook / issue framing, explanation / key claim,
  source-boundary warning, implication / why it matters, and close / next
  action. The selected next axis is
  `newsroom-offline-topic-mini-episode-capsule-with-animation-accent-v1`.
- **Terminal resume remote sync handoff completed (2026-06-30 JST)**:
  `newsroom-terminal-resume-remote-sync-handoff-v2` records the current
  cross-terminal restart context after
  `3e81daa docs: add rss dry-run animated beat proof`. The mainline-slot
  worktree was fetched, clean, on `master`, and aligned with `origin/master`
  before this handoff. New tracked handoff artifacts are
  `samples/_probe/newsroom_handoff/terminal_resume_remote_sync_handoff_v2.json`
  and
  `docs/verification/NEWSROOM_TERMINAL_RESUME_REMOTE_SYNC_HANDOFF_V2_2026-06-30.md`,
  plus this runtime pointer and the matching decision-log entry in
  `docs/project-context.md`. The current production context remains the
  newsroom RSS dry-run animated explanation beat proof: an offline RSS-like
  diagnostic topic has been transformed into one animated explanation beat
  with a visible plain `TextItem`, source-boundary role, and frozen minimal
  animation accent. The current ignored local review targets are
  `_tmp/newsroom_manual_probe/rss_dry_run_animated_explanation_beat_v1.ymmp`
  and
  `_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v2_visible_integration.ymmp`;
  both exist on this host, are ignored by `.gitignore` `_tmp/`, and must
  remain untracked/uncommitted. No Agent-side YMM4 launch, render,
  `.ymmp` stage/commit, media/audio/TTS generation, live RSS/news fetch,
  card redesign, animation tuning, production/public readiness claim, or
  audience/order acceptance claim occurred. On a fresh terminal, read
  `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, this top runtime entry, then
  `docs/verification/NEWSROOM_TERMINAL_RESUME_REMOTE_SYNC_HANDOFF_V2_2026-06-30.md`
  only if more detail is needed. The next default axis is
  `newsroom-rss-dry-run-animated-explanation-beat-preview-operator-instruction-v1`.
- **Newsroom RSS dry-run to animated explanation beat completed (2026-06-30 JST)**:
  `newsroom-rss-dry-run-to-animated-explanation-beat-v1` records the user-side
  v2 visual integration observation as bounded acceptance: the ignored local
  v2 probe showed one visible plain explanation `TextItem` and the character
  animation accent in the same YMM4 scene, with no card-like designed overlay.
  This is `visual_integration_status=pass_with_boundary`; it does not accept
  production subtitle design, production card design, render quality, public
  readiness, or audience/order response. The slice stops local visual/animation
  tuning and returns to content-flow proof by creating one offline
  RSS-like diagnostic topic fixture and transforming it into one animated
  explanation beat. New tracked artifacts are
  `samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json`,
  `docs/verification/NEWSROOM_RSS_DRY_RUN_TO_ANIMATED_EXPLANATION_BEAT_V1_2026-06-30.md`,
  `samples/_probe/newsroom_handoff/rss_dry_run_animated_explanation_beat_contract_v1.json`,
  `src/pipeline/newsroom_rss_dry_run_to_animated_explanation_beat.py`, and
  `tests/test_newsroom_rss_dry_run_to_animated_explanation_beat.py`. The
  ignored local probe exists at
  `_tmp/newsroom_manual_probe/rss_dry_run_animated_explanation_beat_v1.ymmp`;
  it is copied from the v2 visible-integration route, keeps the 16 animation
  items unchanged, and replaces the single visible `TextItem` with the
  topic-derived line `Offline fixture: verify source boundary before
  production.` Readback passes with `TextItem=1`, `GroupItem=8`,
  `ImageItem=8`, visible text/overlay item count `1`, animation item count
  `16`, and `.gitignore` `_tmp/` confirmation. No live RSS/news/network fetch,
  animation-only probe, nod/expression/primitive tuning, card redesign,
  production subtitle/card design, render, Agent-side YMM4 launch,
  `.ymmp` stage/commit, media/audio/TTS output, production/public readiness
  claim, or audience/order acceptance claim occurred. The selected next axis is
  `newsroom-rss-dry-run-animated-explanation-beat-preview-operator-instruction-v1`.
- **Newsroom minimal animated explanation beat visual integration gap fix completed (2026-06-30 JST)**:
  `newsroom-minimal-animated-explanation-beat-visual-integration-gap-fix-v1`
  records the user-side v1 preview gap: the local ignored probe
  `_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v1.ymmp`
  opened and showed character nodding, but no visible card-like, overlay-like,
  subtitle, or explanation text element was present. Structure audit confirms
  the v1 probe contains only `GroupItem=8` and `ImageItem=8`; there is no
  `TextItem` or `ShapeItem`. The root cause is
  `contract_only_not_materialized`, with `overlay_role_readback_only` as a
  contributing factor: the previous contract described overlay/readback
  semantics, but the YMM4-visible probe did not materialize them. New tracked
  artifacts are
  `samples/_probe/newsroom_handoff/minimal_animated_explanation_beat_preview_gap_v1.json`,
  `docs/verification/NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_PREVIEW_GAP_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/minimal_animated_explanation_beat_visual_integration_gap_fix_v1.json`,
  `docs/verification/NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_VISUAL_INTEGRATION_GAP_FIX_V1_2026-06-29.md`,
  `src/pipeline/newsroom_minimal_animated_explanation_beat_visual_gap_fix.py`,
  and
  `tests/test_newsroom_minimal_animated_explanation_beat_visual_gap_fix.py`.
  The ignored local v2 probe exists at
  `_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v2_visible_integration.ymmp`;
  it copies the v1 animation items unchanged and adds one full-duration plain
  `TextItem` diagnostic explanation overlay. V2 readback passes with
  `TextItem=1`, `GroupItem=8`, `ImageItem=8`, visible text/overlay item count
  `1`, animation item count `16`, and git ignore confirmed by `.gitignore`
  `_tmp/`. No animation tuning, animation-only probe, primitive/tempo loop,
  render, Agent-side YMM4 launch, `.ymmp` stage/commit, media/audio/TTS
  generation, real RSS/news fetch, external media fetch, card redesign, polished
  visual card creation, dense script work, production/public readiness claim, or
  audience/order acceptance claim occurred. The selected next axis is
  `newsroom-minimal-animated-explanation-beat-v2-preview-operator-instruction-v1`.
- **Newsroom minimal animated explanation beat mainline proof completed (2026-06-30 JST)**:
  `newsroom-minimal-animated-explanation-beat-in-mainline-pipeline-v1`
  returns the animation lane to mainline content integration after the MVP
  accent freeze. The slice creates one diagnostic-only integrated explanation
  beat that ties narration intent, subtitle/readback role, existing minimal
  label/readback overlay semantics, source-boundary role, and the frozen
  background animation accent policy. New tracked artifacts are
  `samples/_probe/newsroom_handoff/minimal_animated_explanation_beat_mainline_v1.json`,
  `docs/verification/NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_MAINLINE_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/minimal_animated_explanation_beat_contract_v1.json`,
  `docs/verification/NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_V1_2026-06-29.md`,
  `src/pipeline/newsroom_minimal_animated_explanation_beat.py`, and
  `tests/test_newsroom_minimal_animated_explanation_beat.py`. The ignored local
  YMM4 representation candidate exists at
  `_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v1.ymmp`;
  it is derived from the known minimal integrated scene route, is verified
  ignored by `.gitignore` `_tmp/`, and must remain untracked/uncommitted.
  Structural readback passes with a 720-frame / 12.0-second timeline,
  `GroupItem=8`, `ImageItem=8`, no unexpected item types, and the same frozen
  accent budget: stable pose, one expression event, one short nod/reaction,
  and return to stable pose. This is not an animation-only, primitive-only,
  tempo-only, card-polish, render/export, dense-script, audio/TTS, real
  RSS/news, production/public, or audience/order acceptance slice. No Agent-side
  YMM4 launch, render, media/audio/TTS generation, real RSS/news fetch, card
  asset modification, dense script work, `.ymmp` stage/commit, production/public
  readiness claim, or actual audience/order acceptance claim occurred. The next
  selected axis is
  `newsroom-minimal-animated-explanation-beat-preview-operator-instruction-v1`:
  prepare one bounded preview instruction for the verified integrated local
  target, or return to RSS dry-run integration if another preview is deemed
  unnecessary.
- **Newsroom background animation MVP accent freeze and mainline return completed (2026-06-30 JST)**:
  `newsroom-background-animation-minimal-integrated-scene-preview-readback-and-mvp-freeze-v1`
  records the user-side preview observation for the existing local ignored
  minimal integrated scene probe at
  `_tmp/newsroom_manual_probe/background_animation_minimal_integrated_scene_probe_v1.ymmp`.
  The user opened the file successfully, saw an expression change, and then saw
  a nod-like motion. This is recorded as `mvp_accent_layer_status=accepted_with_boundary`,
  not as production animation quality. New tracked artifacts are
  `samples/_probe/newsroom_handoff/background_animation_minimal_integrated_scene_preview_observation_v1.json`,
  `docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json`,
  `docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MVP_FREEZE_V1_2026-06-29.md`,
  `src/pipeline/newsroom_background_animation_mvp_freeze.py`, and
  `tests/test_newsroom_background_animation_mvp_freeze.py`. The frozen MVP
  accent policy allows stable pose, one expression event tied to a scene beat,
  one short nod/reaction after that event, and return to stable pose. Disabled
  by default are body forward/back movement, repeated nodding, mechanical
  expression cycling, speech balloons, full chaban scenes, animation-only probe
  loops, and tempo-only probe loops. No new local `.ymmp`, animation-only probe,
  render, Agent-side YMM4 launch, media/audio/TTS generation, card asset
  modification, dense script work, real RSS/news fetch, external reference-video
  fetch, production/public readiness claim, or actual audience/order acceptance
  claim occurred. The next default axis is
  `newsroom-minimal-animated-explanation-beat-in-mainline-pipeline-v1`: attach
  the frozen MVP accent policy to a real explanation beat / YMM4 scene route in
  the mainline pipeline instead of tuning primitives.
- **Newsroom background animation minimal integrated scene operator surface completed (2026-06-30 JST)**:
  `newsroom-background-animation-minimal-integrated-scene-probe-v1` creates the
  first integrated background animation accent after the stop-loss policy. The
  local ignored probe is
  `_tmp/newsroom_manual_probe/background_animation_minimal_integrated_scene_probe_v1.ymmp`;
  it exists on this host, is verified ignored by `.gitignore` `_tmp/`, and must
  remain untracked/uncommitted. The tracked contract/readback artifacts are
  `samples/_probe/newsroom_handoff/background_animation_minimal_integrated_scene_contract_v1.json`,
  `docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MINIMAL_INTEGRATED_SCENE_CONTRACT_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/background_animation_minimal_integrated_scene_probe_v1.json`,
  `docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MINIMAL_INTEGRATED_SCENE_PROBE_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/background_animation_minimal_integrated_scene_operator_instruction_v1.json`,
  `docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MINIMAL_INTEGRATED_SCENE_OPERATOR_INSTRUCTION_V1_2026-06-30.md`,
  `src/pipeline/newsroom_background_animation_minimal_integrated_scene.py`, and
  `tests/test_newsroom_background_animation_minimal_integrated_scene.py`. The
  probe is a 720-frame / 12.0-second review-only explanation beat using existing
  `samples/nod_head.ymmp` material: stable start pose, one scene-reasoned
  expression event at the key phrase, one 45-frame nod/reaction, and stable end
  pose. Structural readback passes with 16 items (`GroupItem=8`,
  `ImageItem=8`), 4 segments, no unexpected item types, one expression event,
  one nod/reaction, all parent X values fixed at `-96.0`, and semantic status
  pass. No body forward/back movement, repeated nodding, mechanical expression
  cycling, complex speech balloon, full chaban scene, Agent-side YMM4 launch,
  render, media/audio/TTS generation, card asset modification, dense script
  work, real RSS/news fetch, external reference-video fetch, production/public
  readiness claim, or actual audience/order acceptance claim occurred. The
  previous scene choreography probe is classified as `insufficient_too_abstract`
  for another preview because it already served as the primitive-feasibility
  surface and the repo has advanced to an integrated explanation beat. No
  duplicate `.ymmp` was created for this operator surface. The next default
  axis is one freeform user preview of the verified local integrated scene
  target using the operator instruction artifact; no render, screenshot,
  production/public judgment, Git operation, `.ymmp` commit, audio/TTS,
  RSS/news fetch, or card redesign is requested.
- **Newsroom background animation stop-loss and minimal integrated scene plan completed (2026-06-29 JST)**:
  `newsroom-animation-lane-stop-loss-and-integration-plan-v1` records the
  latest user-side scene choreography preview observation and stops the
  primitive-only tuning loop. The normalized observation is that the scene
  choreography probe opened in YMM4, is partially coherent, and proves primitive
  feasibility enough for planning: expression changes and nodding are visible,
  earlier forward/back movement is mostly gone, but motion near the angry
  expression still carries a warning and final animation quality is not
  accepted. Render/export remains unnecessary. New tracked artifacts are
  `samples/_probe/newsroom_handoff/yukkuri_animation_scene_preview_observation_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_SCENE_PREVIEW_OBSERVATION_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/background_animation_mvp_policy_v1.json`,
  `docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MVP_POLICY_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/background_animation_integration_plan_v1.json`,
  `docs/verification/NEWSROOM_BACKGROUND_ANIMATION_INTEGRATION_PLAN_V1_2026-06-29.md`,
  `src/pipeline/newsroom_background_animation_mvp_policy.py`, and
  `tests/test_newsroom_background_animation_mvp_policy.py`. The active MVP
  policy allows only a stable pose, one expression event, one short nod/reaction,
  and optional small lateral emphasis when scene-justified. Repeated nodding,
  mechanical expression cycling, body forward/back movement, complex speech
  balloons, and full chaban scenes are disabled by default. The next default
  axis is `newsroom-background-animation-minimal-integrated-scene-probe-v1`: a
  later 10-20 second integrated scene using one actual explanation beat, one
  expression event, one nod/reaction, no default body forward/back movement,
  minimal existing card/overlay, and one freeform preview only. No Agent-side
  YMM4 launch, render, `.ymmp` creation in this slice, `.ymmp` stage/commit,
  media/audio/TTS generation, card modification, dense script work, real
  RSS/news fetch, external reference-video fetch, production/public readiness
  claim, or actual audience/order acceptance claim occurred. If the next
  integrated scene still feels bad, freeze animation as minimal accent and
  return to RSS/story integration.
- **Newsroom yukkuri v4 tempo default policy and scene-beat route completed (2026-06-29 JST)**:
  `newsroom-yukkuri-animation-v4-sweep-readback-and-scene-choreography-probe-v1`
  now normalizes the latest user-side v4 tempo sweep observation: `0.75s`
  looks the most natural, the best duration depends on the scene, and `1.0s`
  plus `0.5s` are both within acceptable range. No production/public/render
  approval was given. The active tempo default policy is `0.75s` / 45 frames
  at 60 fps for default light reenactment beats, with `0.5s` / 30 frames kept
  for quick reaction / punch / short emphasis and `1.0s` / 60 frames kept for
  slower explanatory or readability-heavy moments. `1.5s` / 90 frames is not
  selected as default and remains only an upper comparison or special slow
  scene case. This exits the primitive-only fast/slow loop; the next route is
  `newsroom-yukkuri-animation-scene-beat-integration-v1`. Updated tracked
  artifacts are
  `samples/_probe/newsroom_handoff/yukkuri_animation_v4_tempo_sweep_observation_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_V4_TEMPO_SWEEP_OBSERVATION_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/yukkuri_animation_scene_choreography_contract_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_SCENE_CHOREOGRAPHY_CONTRACT_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/yukkuri_animation_scene_choreography_probe_v1.json`,
  `src/pipeline/newsroom_yukkuri_animation_scene_choreography.py`, and
  `tests/test_newsroom_yukkuri_animation_scene_choreography.py`. The ignored
  local scene probe exists at
  `_tmp/newsroom_manual_probe/yukkuri_animation_scene_choreography_probe_v1.ymmp`;
  it is under `.gitignore` `_tmp/` and must remain untracked/uncommitted. The
  probe is 1080 frames / 18.0 sec at 60 fps, with six scene beats: neutral
  listening pose, question/reaction cue, one short acknowledgement nod, a
  reasoned caution expression, one small intentional nudge, and return to
  stable explanation pose. Structural readback passes with 32 items
  (`GroupItem=16`, `ImageItem=16`), 8 materialized segments, one meaningful
  nod, one small intentional move, reasoned expression changes, and stable
  `X=-96` anchor continuity. No Agent-side YMM4 launch, render, `.ymmp`
  stage/commit, media/audio/TTS generation, card modification, dense script
  work, real RSS/news fetch, external reference-video fetch, production/public
  readiness claim, or actual audience/order acceptance claim occurred. The
  next default axis is scene-beat integration using the tempo policy inside an
  actual short scene/beat structure, not another raw primitive tempo sweep
  unless a concrete tempo defect remains.
- **Newsroom yukkuri v3 observation and v4 tempo sweep probe completed (2026-06-29 JST)**:
  `newsroom-yukkuri-animation-tempo-sweep-probe-v1` normalizes the user-side
  v3 preview observation: v3 is shorter than v2, but still feels floaty and
  slow, and continuing one fast/slow value at a time is inefficient. New
  tracked artifacts are
  `samples/_probe/newsroom_handoff/yukkuri_animation_v3_preview_observation_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_V3_PREVIEW_OBSERVATION_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/yukkuri_animation_tempo_sweep_contract_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_TEMPO_SWEEP_CONTRACT_V1_2026-06-29.md`,
  `src/pipeline/newsroom_yukkuri_animation_tempo_sweep.py`, and
  `tests/test_newsroom_yukkuri_animation_tempo_sweep.py`. The slice restores /
  verifies the ignored local v3 probe from the existing tracked materializer
  and creates the ignored local v4 tempo sweep probe at
  `_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp`;
  both local `.ymmp` files are under `.gitignore` `_tmp/` and must remain
  untracked/uncommitted. V4 compares four ordered tempo bands at 60 fps:
  30 frames / 0.5 sec, 45 frames / 0.75 sec, 60 frames / 1.0 sec, and
  90 frames / 1.5 sec. Structural readback passes with 80 items
  (`GroupItem=40`, `ImageItem=40`), 1125 frames / 18.75 sec total, all four
  requested primitives covered in every band, and v2/v3 anchor continuity
  preserved. The expected default candidate is 60 frames / 1.0 sec, with
  0.75 sec and 0.5 sec as lower-bound comparisons. No Agent-side YMM4 launch,
  render, `.ymmp` stage/commit, media/audio/TTS generation, card modification,
  dense script work, real RSS/news fetch, external reference-video fetch,
  production/public readiness claim, or actual audience/order acceptance claim
  occurred. The next default axis is
  `newsroom-yukkuri-animation-tempo-sweep-preview-operator-instruction-v1`:
  open only the v4 sweep probe, do not render, and return the chosen default
  band or report that all bands are still too slow/too abrupt.
- **Remote sync and terminal-resume handoff completed (2026-06-29 JST)**:
  `newsroom-terminal-resume-remote-sync-handoff-v1` records the current
  cross-terminal restart context before reflecting local state to `origin`.
  The repo was clean and already aligned with `origin/master` at `6b66f03`
  before this handoff slice. This slice adds tracked handoff artifacts only:
  `samples/_probe/newsroom_handoff/terminal_resume_remote_sync_handoff_v1.json`
  and
  `docs/verification/NEWSROOM_TERMINAL_RESUME_REMOTE_SYNC_HANDOFF_V1_2026-06-29.md`,
  plus this runtime pointer and the matching decision-log entry in
  `docs/project-context.md`. No product code, generated media, `.ymmp` stage,
  dependency, DB/auth/API contract, YMM4 launch, render, real RSS/news fetch,
  external reference-video fetch, or production/public readiness claim occurred.
  The ignored local v3 probe remains host-local at
  `_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp`;
  it exists on this host and is still ignored by `.gitignore` `_tmp/`, so it
  must not be staged or committed. The current production context is still the
  yukkuri v3 tempo-fix preview gate: v2 motion connection improved, the
  remaining problem is slow tempo, and v3 halves beats to 180 frames / 3 seconds
  across a 900-frame / 15-second probe. The next default axis remains
  `newsroom-yukkuri-animation-primitive-v3-preview-operator-instruction-v1`.
  On a fresh terminal, read `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, this top
  runtime entry, then the handoff verification doc only if more detail is
  needed.
- **Newsroom yukkuri v2 preview readback and v3 tempo-fix probe completed (2026-06-29 JST)**:
  `newsroom-yukkuri-animation-v2-preview-readback-and-tempo-calibration-v1`
  normalizes the user-side preview observation for the ignored local v2 probe
  at `_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v2_motion_fix.ymmp`.
  The user observed that motion now connects smoothly, no new major breakage
  was reported, and render/export is still unnecessary for this stage; the
  remaining problem is that the motion is still very slow. New tracked artifacts
  are
  `samples/_probe/newsroom_handoff/yukkuri_animation_v2_preview_observation_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_V2_PREVIEW_OBSERVATION_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/yukkuri_animation_tempo_contract_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_TEMPO_CONTRACT_V1_2026-06-29.md`,
  `src/pipeline/newsroom_yukkuri_animation_tempo_contract.py`, and
  `tests/test_newsroom_yukkuri_animation_tempo_contract.py`. The slice also
  creates the ignored local v3 probe at
  `_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp`;
  the file exists on this host, is verified ignored by `git check-ignore -v`,
  and must remain untracked/uncommitted. V3 preserves the v2 shared-anchor and
  neutral-facing fixes, keeps 20 items (`GroupItem=10`, `ImageItem=10`), and
  halves each beat from 360 frames / 6 seconds to 180 frames / 3 seconds, so
  the total probe is now 900 frames / 15 seconds with `duration_ratio=0.5` and
  `tempo_multiplier=2.0`. Head nods still return through `0 -> negative -> 0`,
  expression swaps stay one per beat, and X nudges continue to return to
  `X=-96`. `speech_balloon` remains omitted/partial. No Agent-side YMM4 launch,
  render, `.ymmp` stage/commit, media/audio/TTS generation, card modification,
  dense script work, real RSS/news fetch, external reference-video fetch,
  production/public readiness claim, or actual audience/order acceptance claim
  occurred. The next default axis is
  `newsroom-yukkuri-animation-primitive-v3-preview-operator-instruction-v1`.
- **Newsroom yukkuri primitive preview observation and v2 motion-fix probe completed (2026-06-29 JST)**:
  `newsroom-yukkuri-animation-primitive-preview-observation-readback-and-motion-fix-v1`
  normalizes the user-side YMM4 preview observation for the ignored local v1
  probe at `_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp`.
  The user observed that the project opens, the character is visible, head/body
  attachment has no major breakage, expressions switch, and animation is
  visible, while motion is very slow, broad X travel reads as backward movement
  toward screen center, segment-to-segment X changes create jumpy disconnected
  movement, and the head nod is too slow. Render/export was not checked and is
  not required now because the current bottleneck is motion timing, facing, and
  anchor continuity rather than render mechanics. New tracked artifacts are
  `samples/_probe/newsroom_handoff/yukkuri_animation_primitive_preview_observation_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_PRIMITIVE_PREVIEW_OBSERVATION_V1_2026-06-29.md`,
  `samples/_probe/newsroom_handoff/yukkuri_animation_motion_contract_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_MOTION_CONTRACT_V1_2026-06-29.md`,
  `src/pipeline/newsroom_yukkuri_animation_motion_contract.py`, and
  `tests/test_newsroom_yukkuri_animation_motion_contract.py`. The slice also
  creates the ignored local v2 probe at
  `_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v2_motion_fix.ymmp`;
  the file exists on this host, is verified ignored by `git check-ignore -v`,
  and must remain untracked/uncommitted. V2 remains derived from tracked
  `samples/nod_head.ymmp` proof items, shortens the timeline to 30 seconds,
  keeps 20 items (`GroupItem=10`, `ImageItem=10`), constrains entry/exit to
  bounded side movement, uses `X=-96` as the shared review anchor across
  adjacent beats, and changes head nods to explicit `0 -> negative -> 0`
  rotation routes inside 6-second beats. Covered primitives remain `head_nod`,
  `expression_swap`, `character_entrance_exit`, and `small_position_move`;
  `speech_balloon` remains omitted/partial. No Agent-side YMM4 launch, render,
  `.ymmp` stage/commit, media/audio/TTS generation, card modification, dense
  script work, real RSS/news fetch, external reference-video fetch,
  production/public readiness claim, or actual audience/order acceptance claim
  occurred. The next default axis is
  `newsroom-yukkuri-animation-primitive-v2-preview-operator-instruction-v1`.
- **Newsroom yukkuri animation primitive probe materialization v1 completed (2026-06-28 artifact date; recorded 2026-06-29 JST)**:
  `newsroom-yukkuri-animation-primitive-probe-materialization-v1`
  materializes the previously reserved ignored local YMM4 probe target at
  `_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp`.
  The local file exists on this host, is verified ignored by
  `git check-ignore -v`, and remains untracked/uncommitted. New tracked
  readback artifacts are
  `samples/_probe/newsroom_handoff/yukkuri_animation_primitive_probe_materialization_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_PRIMITIVE_PROBE_MATERIALIZATION_V1_2026-06-28.md`,
  `src/pipeline/newsroom_yukkuri_animation_primitive_probe_materialization.py`,
  and
  `tests/test_newsroom_yukkuri_animation_primitive_probe_materialization.py`.
  The generated probe clones tracked `samples/nod_head.ymmp` proof items and
  applies bounded timing, current-host asset-path, expression, X-position, and
  rotation changes only. Structural readback passes with a 60 fps / 3600-frame
  timeline, 20 items total, `GroupItem=10`, `ImageItem=10`, and no unexpected
  item types. Covered primitives are `head_nod`, `expression_swap`,
  `character_entrance_exit`, and `small_position_move`; `speech_balloon`
  remains omitted/partial because no dedicated balloon template or visual pass
  exists. No YMM4 launch, render, `.ymmp` stage/commit, audio/TTS generation,
  card modification, real RSS/news fetch, external reference-video fetch,
  production/public readiness claim, or actual audience/order acceptance claim
  occurred. The previous primitive-proof builder is kept slice-static so later
  local probe existence does not rewrite the earlier "not created in that
  slice" readback. The next default axis is
  `newsroom-yukkuri-animation-primitive-render-smoke-v1`, with the prerequisite
  that an operator instruction sheet exists before opening/rendering the local
  probe.
- **Newsroom yukkuri animation primitive proof v1 completed (2026-06-28 artifact date; recorded 2026-06-29 JST)**:
  `newsroom-yukkuri-animation-primitive-proof-v1` turns the previous
  background animation format spec into a no-render structural proof package.
  New artifacts are
  `samples/_probe/newsroom_handoff/yukkuri_animation_primitive_proof_v1.json`,
  `samples/_probe/newsroom_handoff/yukkuri_animation_scene_beat_probe_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_PRIMITIVE_PROOF_V1_2026-06-28.md`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_SCENE_BEAT_PROBE_V1_2026-06-28.md`,
  `src/pipeline/newsroom_yukkuri_animation_primitive_proof.py`, and
  `tests/test_newsroom_yukkuri_animation_primitive_proof.py`. The selected
  primitive subset remains `head_nod`, `expression_swap`,
  `character_entrance_exit`, `small_position_move`, and `speech_balloon`.
  Structural proof status is `pass` for the first four and `partial` for
  `speech_balloon`, because ShapeItem/TextItem routes exist but no dedicated
  speech-balloon template or visual pass exists yet. The scene beat probe maps
  five narration roles to those primitives without rewriting the dense script.
  No local ignored probe `.ymmp` was created in this slice; the planned path
  `_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp` is
  recorded as ignored/missing and reserved for the next gate. No YMM4 launch,
  render, `.ymmp` stage/commit, audio/TTS generation, card modification, real
  RSS/news fetch, external reference-video fetch, production/public readiness
  claim, or actual audience/order acceptance claim occurred. The next default
  axis is `newsroom-yukkuri-animation-primitive-render-smoke-v1`, with the
  prerequisite that the next slice first creates or verifies an ignored local
  primitive probe target and only then uses an explicit render gate.
- **Newsroom yukkuri background animation format spec v1 completed (2026-06-28 artifact date; recorded 2026-06-29 JST)**:
  `newsroom-reference-yukkuri-background-animation-format-spec-v1` normalizes
  the latest user correction: the base format remains `yukkuri_explainer`, and
  the missing product layer is
  `yukkuri_chaban_style_reenactment_pv` as a supportive background
  reenactment/light animation layer. This is not a dialogue-only chaban rewrite,
  not a line-count-density loop, and not more card-only visual polish. New
  artifacts are
  `samples/_probe/newsroom_handoff/yukkuri_background_animation_format_spec_v1.json`,
  `samples/_probe/newsroom_handoff/yukkuri_animation_primitive_inventory_v1.json`,
  `samples/_probe/newsroom_handoff/prior_animation_asset_recovery_audit_v1.json`,
  `docs/verification/NEWSROOM_YUKKURI_BACKGROUND_ANIMATION_FORMAT_SPEC_V1_2026-06-28.md`,
  `docs/verification/NEWSROOM_YUKKURI_ANIMATION_PRIMITIVE_INVENTORY_V1_2026-06-28.md`,
  `docs/verification/NEWSROOM_PRIOR_ANIMATION_ASSET_RECOVERY_AUDIT_V1_2026-06-28.md`,
  `src/pipeline/newsroom_yukkuri_background_animation_format_spec.py`, and
  `tests/test_newsroom_yukkuri_background_animation_format_spec.py`. The prior
  asset audit found tracked repo evidence for expression PNGs, a body source,
  face-map bundles, `samples/nod_head.ymmp`, skit-group templates/registry,
  group-motion map, G-24 background skit blueprint/readback artifacts, and
  related validator/placement/motion code and docs. The primitive inventory
  defines 11 candidates and selects the first probe set as `head_nod`,
  `expression_swap`, `character_entrance_exit`, `small_position_move`, and
  `speech_balloon`; `speech_balloon` remains unproven but can be probed through
  ShapeItem/TextItem without external media. No YMM4 launch, render, `.ymmp`
  edit/commit, audio/TTS generation, card regeneration, real RSS/news fetch,
  external reference-video fetch, media staging, production/public readiness
  claim, or actual audience/order acceptance claim occurred. The next default
  slice is `newsroom-yukkuri-animation-primitive-proof-v1`.
- **Newsroom v0.1 dense script semantic audit and v2 rewrite completed (2026-06-26)**:
  `newsroom-v0.1-dense-script-semantic-audit-and-rewrite-v1` treats the
  latest user YMM4 dense import/save observation as a script-quality warning,
  not a mechanics failure. The user-saved dense v1 source project exists only
  as ignored local evidence at
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v0_1_dense_source_v1.ymmp`;
  it remains untracked and must not be committed. New artifacts are
  `samples/_probe/newsroom_handoff/v0_1_dense_script_semantic_audit_v1.json`,
  `samples/_probe/newsroom_handoff/v0_1_dense_script_package_v2.json`,
  `samples/_probe/newsroom_handoff/v0_1_dense_caption_timing_plan_v2.json`,
  `samples/_probe/newsroom_handoff/v0_1_dense_source_ymmp_import_v2.csv`,
  `docs/verification/NEWSROOM_V0_1_DENSE_SCRIPT_SEMANTIC_AUDIT_V1_2026-06-26.md`,
  `docs/verification/NEWSROOM_V0_1_DENSE_SCRIPT_PACKAGE_V2_2026-06-26.md`,
  `src/pipeline/newsroom_v0_1_dense_script_semantic_audit.py`, and
  `tests/test_newsroom_v0_1_dense_script_semantic_audit.py`. The audit
  classifies the v1 13-line dense script as `semantic_delta=partial` against
  the four-line baseline because it still reads too much like process
  inventory: problem, offer, viewer value, line-role distinctness, padding,
  next action, and "merely split text" gates are partial, while proof sequence
  and diagnostic boundary are pass. V2 keeps 13 short lines over the same
  planned 68 second window but rewrites around requester problem, reviewable
  video draft offer, proof confidence, diagnostic limits, and a purpose-clarity
  next action. The v2 CSV is UTF-8 BOM, headerless, two-column `speaker,text`,
  uses the canonical existing source speaker, and records
  `access_state=verified_current_host_file_exists`; because repo `.gitignore`
  ignores `*.csv`, this artifact must be force-added when committing. This
  slice did not launch YMM4, render, edit or commit `.ymmp`, regenerate cards,
  generate audio/TTS, fetch real RSS/news, use real brands/URLs/screenshots,
  request a fixed form, or claim production/public/order/audience acceptance.
  The next user-side milestone is to import
  `samples/_probe/newsroom_handoff/v0_1_dense_source_ymmp_import_v2.csv` in
  YMM4 and save the ignored local v2 source project as
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v0_1_dense_source_v2.ymmp`.
  The next default slice is
  `newsroom-v0.1-dense-v2-source-ymmp-operator-instruction-v1`.
- **Newsroom v0.1 dense script package v1 completed (2026-06-26)**:
  `newsroom-v0.1-script-density-implementation-v1` turns the prior
  explanation-readiness/script-density plan into concrete review-only source
  inputs. New artifacts are
  `samples/_probe/newsroom_handoff/v0_1_dense_script_package_v1.json`,
  `samples/_probe/newsroom_handoff/v0_1_dense_caption_timing_plan_v1.json`,
  `samples/_probe/newsroom_handoff/v0_1_dense_source_ymmp_import_v1.csv`,
  `docs/verification/NEWSROOM_V0_1_DENSE_SCRIPT_PACKAGE_V1_2026-06-26.md`,
  `docs/verification/NEWSROOM_V0_1_DENSE_SOURCE_YMMP_IMPORT_V1_2026-06-26.md`,
  `src/pipeline/newsroom_v0_1_dense_script_package.py`, and
  `tests/test_newsroom_v0_1_dense_script_package.py`. The new script has 13
  short diagnostic lines over a planned 68 second window across opening,
  mechanism, proof, boundary, and next-action segments. The dense CSV is UTF-8
  BOM, headerless, two-column `speaker,text`, and uses the canonical existing
  source speaker value. Explanation readiness improves to
  `problem_clear=pass`, `offer_clear=pass`, `proof_clear=pass`,
  `boundary_clear=pass`, `next_action_clear=pass`,
  `audience_fit_proxy=partial`, `visual_supports_explanation=pass`, and
  `access_clear=pass`; the dense CSV artifact records the current-host full
  file path and `access_state=verified_current_host_file_exists`. This
  slice did not launch YMM4, render, edit `.ymmp`, regenerate cards, generate
  audio/TTS, fetch real RSS/news, stage media, request a structured answer, or
  claim production/public/audience acceptance. The next user-side milestone is
  to import
  `samples/_probe/newsroom_handoff/v0_1_dense_source_ymmp_import_v1.csv` in
  YMM4 and save the ignored local dense source project as
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v0_1_dense_source_v1.ymmp`.
  The next default slice is
  `newsroom-v0.1-dense-source-ymmp-operator-instruction-v1`.
- **Newsroom v0.1 explanation readiness and script density plan v1 completed (2026-06-26)**:
  `newsroom-v0.1-explanation-readiness-and-script-density-plan-v1` records
  that the current diagnostic mp4 exists locally and the YMM4 render pipeline,
  native audio path, script import path, card visual asset path, and
  density-refined render observation are diagnostic pass, while direct
  AI-side video generation through `.ymmp` is not reliable enough to prioritize
  over explanation quality. New artifacts are
  `samples/_probe/newsroom_handoff/v0_1_explanation_readiness_v1.json`,
  `samples/_probe/newsroom_handoff/v0_1_script_density_plan_v1.json`,
  `docs/verification/NEWSROOM_V0_1_EXPLANATION_READINESS_V1_2026-06-26.md`,
  `docs/verification/NEWSROOM_V0_1_SCRIPT_DENSITY_PLAN_V1_2026-06-26.md`,
  `src/pipeline/newsroom_v0_1_explanation_readiness.py`, and
  `tests/test_newsroom_v0_1_explanation_readiness.py`. The readiness gates are:
  `problem_clear=partial`, `offer_clear=partial`, `proof_clear=pass`,
  `boundary_clear=pass`, `next_action_clear=partial`,
  `audience_fit_proxy=partial`, and `visual_supports_explanation=pass`.
  Script density diagnosis records the current four dialogue lines across about
  68 seconds as too sparse for explanation; the plan targets 60-75 seconds,
  five narration segments, and roughly 10-14 short lines. This slice did not
  launch YMM4, render, edit `.ymmp`, regenerate cards, create audio/TTS, fetch
  real RSS/news, stage media, request a fixed review form, claim audience/order
  acceptance, or claim production/public readiness. The next default slice is
  `newsroom-v0.1-script-density-implementation-plan-v1`.
- **Newsroom post-density refinement render smoke result readback v1 completed (2026-06-26)**:
  `newsroom-post-density-refinement-render-smoke-result-readback-v1`
  normalizes the latest user freeform YMM4 observation after density-benchmarked
  card refinement. New artifacts are
  `samples/_probe/newsroom_handoff/post_density_refinement_render_smoke_result_readback_v1.json`,
  `docs/verification/NEWSROOM_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_V1_2026-06-26.md`,
  `src/pipeline/newsroom_post_density_refinement_render_smoke_result_readback.py`,
  and
  `tests/test_newsroom_post_density_refinement_render_smoke_result_readback.py`.
  The readback records `render_smoke_result=pass`,
  `yym4_opened_card_placement_project=true`, `render_completed=true`,
  `output_duration_observed=approximately_68_sec`,
  `card_count_visible=4`, `density_refinement_visible=true`,
  `information_density_reduced=true`, `dialogue_items_preserved=true`,
  `native_audio_present=true`, and no timing/audio regression reported.
  This is a diagnostic observation only: it did not launch YMM4 by Agent,
  perform a new Agent render, regenerate cards, edit `.ymmp`, create audio/TTS,
  stage media, fetch external material, request a fixed review form, claim
  actual audience acceptance, or claim production/public readiness. Video
  readiness remains `6/7`; visual density readiness is diagnostic pass; the
  next default slice is
  `newsroom-internal-review-v0.1-reevaluation-card-v1`.
- **Newsroom visual card density benchmarked refinement v1 completed (2026-06-26)**:
  `newsroom-visual-card-density-benchmarked-refinement-v1` applied the
  completed density simplification spec to the current four diagnostic visual
  card assets at their stable paths. New artifacts are
  `samples/_probe/newsroom_handoff/visual_card_density_benchmarked_refinement_v1.json`,
  `docs/verification/NEWSROOM_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_V1_2026-06-26.md`,
  `src/pipeline/newsroom_visual_card_density_benchmarked_refinement.py`, and
  `tests/test_newsroom_visual_card_density_benchmarked_refinement.py`. The four
  SVG/PNG cards and `visual_cards_v1/contact_sheet.html` were regenerated in
  place using the density rules: one primary reading path, one headline, one
  primary sentence, one support note or diagram, two to three meaningful labels,
  larger whitespace around essential text, demoted source/debug metadata, and a
  non-competing subtitle reserve. The readback reports
  `proxy_status=materially_improved`, `fail_count=0`, `warning_count=0`,
  `png_export_status=generated`, and stable asset paths preserved. This slice
  did not launch YMM4, render video, edit `.ymmp`, generate audio/TTS, fetch
  external material, import real media, stage output media, request a fixed
  review form, claim actual audience acceptance, or claim production/public
  readiness. The next default slice is
  `newsroom-card-placement-post-density-refinement-render-smoke-v1`.
- **Newsroom visual density simplification spec v1 completed (2026-06-26)**:
  `newsroom-visual-density-simplification-spec-v1` converts the recorded
  density/cognitive-load gate into bounded criteria before any further card
  redesign. New artifacts are
  `samples/_probe/newsroom_handoff/visual_density_simplification_spec_v1.json`,
  `docs/verification/NEWSROOM_VISUAL_DENSITY_SIMPLIFICATION_SPEC_V1_2026-06-26.md`,
  `src/pipeline/newsroom_visual_density_simplification_spec.py`, and
  `tests/test_newsroom_visual_density_simplification_spec.py`. The spec keeps
  the current mechanics readback as pass and defines the next visual problem as
  high information density: one dominant message per card, at most one
  headline, one primary sentence, one supporting note/diagram, two to three
  meaningful labels, no essential meaning in tiny metadata, demoted or hidden
  debug/source text, and a subtitle reserve that does not compete with the
  card. Future visual changes must choose from the spec's remove/merge/demote/
  whitespace operations and must not solve density by shrinking text, adding
  more explanatory boxes, introducing real brands/URLs/news visuals, or
  converting cards into complex YMM4 object graphs. The next default slice is
  `newsroom-visual-card-density-benchmarked-refinement-v1`; use
  `newsroom-visual-information-density-benchmark-v1` only if this spec is not
  enough as criteria, or `newsroom-visual-card-source-band-simplification-v1`
  only if the source/subtitle band is the dominant actionable burden. This
  slice did not launch YMM4, render, edit `.ymmp`, regenerate SVG/PNG cards,
  create audio/TTS, fetch external material, stage media, ask for a fixed
  review form, claim audience acceptance, or claim production/public readiness.
- **Newsroom post-benchmarked visual observation density gate v1 completed (2026-06-26)**:
  `newsroom-post-benchmarked-visual-observation-density-gate-v1` normalizes the
  latest user freeform observation with screenshot support after the
  benchmarked text-fit refinement. New artifacts are
  `samples/_probe/newsroom_handoff/post_benchmarked_visual_observation_density_gate_v1.json`,
  `docs/verification/NEWSROOM_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_V1_2026-06-26.md`,
  `src/pipeline/newsroom_post_benchmarked_visual_observation_density_gate.py`,
  and
  `tests/test_newsroom_post_benchmarked_visual_observation_density_gate.py`.
  The readback records `observation_status=visual_density_issue_confirmed`,
  `mechanics_status=pass`, four visible cards, native YMM4/yukkuri audio
  preserved, dialogue item count preserved, no reported timing/duration
  regression, and no production/public/audience acceptance claim. The concrete
  visual issue is now information density and cognitive load: text-fit improved
  enough to expose that the surface still asks the viewer to track too much
  formatted information. Further visual work must target information
  density/cognitive load explicitly through
  `newsroom-visual-density-simplification-spec-v1` by default, or
  `newsroom-visual-information-density-benchmark-v1` if existing benchmark
  density criteria are insufficient. Do not continue broad style tweaks,
  repeated render asks, or card regeneration until a density/spec-linked
  material change exists. This slice did not launch YMM4, render, edit `.ymmp`,
  regenerate SVG/PNG cards, create audio/TTS, fetch external material, stage
  media, ask for a fixed review form, claim audience acceptance, or claim
  production/public readiness.
- **Newsroom source .ymmp recreation import pack v1 completed (2026-06-26)**:
  `newsroom-source-ymmp-recreation-import-pack-v1` addresses the current
  mainline checkout gap where the ignored local source project
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp` and the
  downstream regenerated `.ymmp` copies are absent. New repo artifacts are
  `samples/_probe/newsroom_handoff/source_ymmp_recreation_import_v1.csv`,
  `samples/_probe/newsroom_handoff/source_ymmp_recreation_import_pack_v1.json`,
  `docs/verification/NEWSROOM_SOURCE_YMMP_RECREATION_IMPORT_PACK_V1_2026-06-26.md`,
  `src/pipeline/newsroom_source_ymmp_recreation_import_pack.py`, and
  `tests/test_newsroom_source_ymmp_recreation_import_pack.py`. The CSV is a
  UTF-8 BOM, headerless two-column `speaker,text` YMM4 `台本読込` input using
  canonical speaker `ゆっくり霊夢` and the four tracked diagnostic lines from
  `diagnostic_ymmp_structure_readback_v1.json` /
  `diagnostic_ymmp_probe_packet_v1.json`. Because repo `.gitignore` ignores
  `*.csv`, this one recreation CSV must be force-added when committing. No
  YMM4 launch, render, `.ymmp` generation/edit, audio/TTS generation, external
  fetch, real media import, media staging, production/public readiness claim,
  structured review template, or card/timing redesign was performed. The next
  user move is to open YMM4, import the generated CSV via `台本読込`, use
  `ゆっくり霊夢` if speaker binding is requested, confirm four lines appear,
  save as `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp`,
  and not render yet. After that local source `.ymmp` exists, Codex should
  verify it remains ignored/unstaged and rerun local regeneration for
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp`
  and
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp`.
- **Newsroom visual card benchmarked refinement v1 completed (2026-06-26)**:
  `newsroom-visual-card-benchmarked-refinement-v1` fixed the concrete static
  benchmark failures from the prior audience-fit evaluation while preserving
  the four stable diagnostic card paths. New artifacts are
  `samples/_probe/newsroom_handoff/visual_card_benchmarked_refinement_v1.json`,
  `docs/verification/NEWSROOM_VISUAL_CARD_BENCHMARKED_REFINEMENT_V1_2026-06-26.md`,
  `src/pipeline/newsroom_visual_card_benchmarked_refinement.py`, and
  `tests/test_newsroom_visual_card_benchmarked_refinement.py`. The existing
  audience-fit card generator now applies narrower headline/body wraps, a
  three-line body allowance, a preserved 34 px meaningful text floor, and a
  short `SRC N/4` label separated from the subtitle-safe reserve detail. The
  four current SVG/PNG cards and contact sheet under
  `samples/_probe/newsroom_handoff/visual_cards_v1/` were regenerated in
  place; card 3/4 left-panel text no longer clips, card 1/2 boundary crowding
  is reduced, and source/subtitle reserve crowding is removed. The benchmarked
  refinement readback reports `refinement_status=benchmarked_text_fit_improved`,
  source validation `passed`, local proxy recheck
  `improved_no_material_static_failures`, `fail_count=0`, `warning_count=2`
  (reference-unproven familiar grammar and playback pacing remain for later
  evidence), and next default slice
  `newsroom-card-placement-post-benchmarked-refinement-render-smoke-v1`.
  Verification in this worktree: `compileall` on the changed modules passed;
  focused tests passed with `19 passed`; JSON, SVG, PNG 1920x1080, local HTML
  contact sheet, and `git diff --check` checks passed. No YMM4 launch, render,
  `.ymmp` edit/commit, audio/TTS/voice cache, external media/live YouTube
  fetch, real brand/content use, fixed review form, production approval,
  public-readiness claim, or audience-acceptance claim was performed.
- **Newsroom audience-fit benchmark evaluation v1 applied (2026-06-26)**:
  `newsroom-audience-fit-benchmark-evaluation-v1` applied the visual benchmark
  to the current four diagnostic SVG/PNG cards and recorded the result in
  `samples/_probe/newsroom_handoff/audience_fit_benchmark_evaluation_v1.json`
  and
  `docs/verification/NEWSROOM_AUDIENCE_FIT_BENCHMARK_EVALUATION_V1_2026-06-26.md`,
  with focused coverage in
  `tests/test_newsroom_audience_fit_benchmark_evaluation.py` and evaluator code
  in `src/pipeline/newsroom_audience_fit_benchmark_evaluation.py`. The
  evaluation found the cards remain understandable as diagnostic review-only
  artifacts, but they fail the material `text_clipping_or_wrapping` proxy:
  cards 3 and 4 visibly clip meaningful left-panel text, while cards 1 and 2
  crowd the same boundary. Warnings also remain for glance readability,
  reference-unproven familiarity, source/subtitle reserve crowding, and 68 sec
  pacing density. Passing proxies are minimum meaningful font size, one
  dominant message per card, card role variation, diagnostic boundary
  visibility, and no real brand/URL/public claim. Unknowns remain actual target
  viewer preference, CTR/retention, target viewer comprehension outside this
  project, production visual quality, and real newsroom visual acceptance. This
  did not launch YMM4, render video, edit `.ymmp`, regenerate card assets,
  generate audio/TTS, fetch external media, import real media, stage media,
  claim actual audience acceptance, approve production visual quality, or claim
  public readiness. The next default slice is
  `newsroom-visual-card-benchmarked-refinement-v1`, limited to the concrete
  benchmark failures: left-panel text wrapping/fit and bottom source/subtitle
  reserve separation.
- **Newsroom visual audience-fit benchmark v1 defined (2026-06-26)**:
  `newsroom-visual-audience-fit-benchmark-v1` now has a repo artifact at
  `samples/_probe/newsroom_handoff/visual_audience_fit_benchmark_v1.json` and
  the human-readable spec at
  `docs/verification/NEWSROOM_VISUAL_AUDIENCE_FIT_BENCHMARK_V1_2026-06-26.md`,
  with focused coverage in
  `tests/test_newsroom_visual_audience_fit_benchmark.py` and the compact
  builder in `src/pipeline/newsroom_visual_audience_fit_benchmark.py`. The
  slice consumes the current audience-fit refinement and normalizes the latest
  concern: the cards are improved, but actual YouTube audience acceptance is
  not measurable from local screenshots, freeform review, or render
  observation alone. The benchmark defines target audience assumptions, visual
  job-to-be-done, L1 evidence level, proxy metrics, reference-abstraction
  hypotheses, acceptance criteria, next-iteration mapping, and a bounded
  freeform review protocol. This did not launch YMM4, render video, edit
  `.ymmp`, regenerate SVG/PNG cards, generate audio/TTS, fetch external
  assets, import real media, stage media, claim actual audience acceptance,
  approve production visual quality, or claim public video readiness. The next
  default slice is `newsroom-audience-fit-benchmark-evaluation-v1`: apply this
  benchmark to the current four diagnostic cards once before any further visual
  redesign. `newsroom-visual-card-benchmarked-refinement-v1` is only valid if
  that evaluation finds concrete benchmark failures. The reference-pack slice is
  only valid if reference abstraction blocks evaluation;
  `newsroom-internal-review-v0.1-operator-review-card` is only valid if the
  benchmark evaluation says the current cards are sufficient for diagnostic
  review.
- **Newsroom visual card audience-fit remote handoff sealed (2026-06-26)**:
  Preserved the current mainline restart context after
  `newsroom-visual-card-audience-fit-refinement-v1` in
  `docs/verification/NEWSROOM_VISUAL_CARD_AUDIENCE_FIT_REMOTE_HANDOFF_2026-06-26.md`.
  The handoff base is
  `93ebf62 feat: refine newsroom visual cards for audience fit` on `master`;
  before writing the handoff, `HEAD...origin/master` was `0 0` and the tracked
  worktree was clean. The next restart read order remains `AGENTS.md`,
  `docs/REPO_LOCAL_RULES.md`, then `docs/runtime-state.md`, followed by this
  handoff file only if a compact branch/commit/artifact recap is needed.
  Ignored local manual artifacts may remain under `_tmp/newsroom_manual_probe/`,
  including diagnostic `.ymmp` and mp4 files, and must remain untracked and
  unstaged. The next concrete milestone is
  `newsroom-card-placement-post-audience-fit-render-smoke-v1`; use
  `newsroom-yym4-card-asset-placement-refresh-v1` only if the ignored placement
  project cannot reuse the stable PNG paths. Production visual quality,
  post-audience-fit render proof, public video readiness, real content
  readiness, and production approval remain not accepted.
- **Newsroom visual card audience-fit refinement v1 completed (2026-06-26)**:
  Normalized the latest freeform visual review as
  `needs_audience_fit_refinement`: modern visual quality is positive, but
  small text remains, the cards still feel too SaaS/dashboard-like for the
  target audience, and familiar mainstream YouTube explainer language is now
  required. This slice added canonical audience-fit readback/refinement
  artifacts at
  `samples/_probe/newsroom_handoff/visual_card_audience_fit_review_readback_v1.json`,
  `samples/_probe/newsroom_handoff/visual_card_audience_fit_refinement_v1.json`,
  `docs/verification/NEWSROOM_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_V1_2026-06-25.md`,
  `docs/verification/NEWSROOM_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_V1_2026-06-25.md`,
  `src/pipeline/newsroom_visual_card_audience_fit_refinement.py`, and
  `tests/test_newsroom_visual_card_audience_fit_refinement.py`. The four
  stable SVG/PNG card paths under
  `samples/_probe/newsroom_handoff/visual_cards_v1/` and their contact sheet
  were regenerated as diagnostic-only fake cards with larger plain labels,
  large-number/process/check/status motifs, minimum visible text raised to
  `34` px, a declared `132` px display-number allowance, no visible debug
  footer, and no real brands, URLs, media, screenshots, or production-news
  claims. PNG raster export completed through the bundled Python Pillow
  fallback because the `uv` runtime had no Pillow available. No YMM4 launch,
  video render, `.ymmp` edit, audio/TTS generation, external fetch, real media
  import, dashboard/governance/freshness change, production visual-quality
  acceptance, public-readiness claim, or media staging was performed. Accepted
  scope is limited to review normalization, regenerated external diagnostic
  SVG/PNG assets, and a local preview surface ready for a later milestone
  observation. Not accepted: post-audience-fit render proof, YMM4 placement
  proof after this refinement, final design system, production visual quality,
  public video readiness, real newsroom visuals, real content readiness, or
  production approval. Video readiness remains `6/7`; visual readiness remains
  diagnostic `7/7` with the audience-fit surface refreshed; production
  readiness remains low/diagnostic-only. The next default slice is
  `newsroom-card-placement-post-audience-fit-render-smoke-v1`; use
  `newsroom-yym4-card-asset-placement-refresh-v1` only if the existing ignored
  placement project cannot reuse the stable PNG paths. Verification observed
  focused audience-fit tests `7 passed` and adjacent bridge/refinement/
  placement/post-refinement package regression tests `41 passed`.
- **Newsroom card placement post-refinement render smoke package v1 prepared (2026-06-26)**:
  Prepared `newsroom-card-placement-post-refinement-render-smoke-v1` as a
  diagnostic observation package after the visual card design refinement,
  without launching YMM4, rendering video, editing `.ymmp`, generating
  audio/TTS, fetching external sources, importing real media, staging or
  committing `.ymmp`/mp4/wav/mp3/m4a/render outputs, changing
  dashboard/governance/freshness work, or claiming production/public readiness.
  New repo artifacts are
  `samples/_probe/newsroom_handoff/card_placement_post_refinement_render_smoke_v1.json`,
  `docs/verification/NEWSROOM_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_V1_2026-06-26.md`,
  `src/pipeline/newsroom_card_placement_post_refinement_render_smoke.py`, and
  `tests/test_newsroom_card_placement_post_refinement_render_smoke.py`. The
  package verifies that the existing ignored local placement project
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp`
  is present, ignored, untracked, unstaged, and still references all four
  regenerated refined PNG card paths under
  `samples/_probe/newsroom_handoff/visual_cards_v1/`; therefore placement
  refresh is not the default next move. The result normalizer and classifier
  are agent-owned and accept future freeform observation, separating project
  open, render execution, duration, refined-card visibility/readability,
  dialogue preservation, native audio, and operator uncertainty. Accepted scope
  is limited to package readiness, stable refined PNG path reuse by the
  ignored `.ymmp`, and readiness for exactly one later milestone observation.
  Not accepted: post-refinement render proof, production visual quality, final
  design system, public video readiness, real newsroom visuals, real content
  readiness, render output retention, or production approval. Video readiness
  remains `6/7`; visual readiness remains `7/7` diagnostic-refined until the
  post-refinement render is actually observed; production readiness remains
  low/diagnostic-only. The next default slice is
  `newsroom-card-placement-post-refinement-render-smoke-result-readback-v1`
  after a future freeform observation; if the target `.ymmp` stops reusing the
  stable PNG paths, fall back to
  `newsroom-yym4-card-asset-placement-refresh-v1`. Verification observed the
  focused package tests `13 passed` and adjacent visual/card placement
  regression tests `40 passed`.
- **Newsroom visual card design refinement remote handoff sealed (2026-06-25)**:
  Preserved the current mainline restart context after
  `newsroom-visual-card-design-refinement-v1` in
  `docs/verification/NEWSROOM_VISUAL_CARD_DESIGN_REFINEMENT_REMOTE_HANDOFF_2026-06-25.md`.
  The handoff base is `92b7c92 feat: refine newsroom visual card design` on
  `master`; before writing the handoff, `HEAD...origin/master` was `0 0` and
  the tracked worktree was clean. Ignored local manual artifacts may remain
  under `_tmp/newsroom_manual_probe/`, including `.ymmp` and mp4 diagnostic
  outputs, and must remain untracked and unstaged. The next restart read order
  is `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, then `docs/runtime-state.md`.
  The next concrete milestone remains
  `newsroom-card-placement-post-refinement-render-smoke-v1`; use
  `newsroom-yym4-card-asset-placement-refresh-v1` only if the stable PNG paths
  do not hold in the ignored local placement project. Production visual
  quality, post-refinement render proof, public video readiness, real content
  readiness, and production approval remain not accepted.
- **Newsroom visual card design refinement v1 completed (2026-06-25)**:
  Converted the freeform internal review result into canonical diagnostic repo
  evidence and refined the external card assets without launching YMM4,
  rendering video, editing `.ymmp`, generating audio/TTS, fetching external
  sources, importing real media, staging/committing `.ymmp` or media outputs,
  changing dashboard/governance/freshness work, or claiming production/public
  readiness. New repo artifacts are
  `samples/_probe/newsroom_handoff/internal_review_v0_1_result_readback_v1.json`,
  `samples/_probe/newsroom_handoff/visual_card_design_refinement_v1.json`,
  `docs/verification/NEWSROOM_INTERNAL_REVIEW_V0_1_RESULT_READBACK_V1_2026-06-25.md`,
  `docs/verification/NEWSROOM_VISUAL_CARD_DESIGN_REFINEMENT_V1_2026-06-25.md`,
  `src/pipeline/newsroom_visual_card_design_refinement.py`, and
  `tests/test_newsroom_visual_card_design_refinement.py`. The existing
  external card bridge generator now emits refined `1920x1080` SVG cards with
  wrapped/clamped text, a bounded diagnostic type scale (`28` to `54` px),
  subtitle-safe reserve preserved at the lower band, no debug footer on the
  review surface, and four distinct role motifs: intro/summary,
  handoff/process, claim/check, and source/status. The four committed PNGs
  under `samples/_probe/newsroom_handoff/visual_cards_v1/` were regenerated at
  stable paths from the refined SVGs; the contact sheet was updated. The
  internal review normalization is `needs_visual_refinement`: timing,
  native-audio, render, and card-placement mechanics remain diagnostic pass,
  while text clipping/wrapping, type scale, readability, and card variation
  were the accepted refinement axis. Accepted scope is limited to review
  readback, refined external SVG/PNG diagnostic assets, updated preview, and
  readiness for a later milestone-gated observation. Not accepted: production
  visual quality, final design system, YMM4 placement proof after refinement,
  post-refinement render proof, public video readiness, real newsroom visuals,
  real content readiness, production approval, external TTS adoption, or media
  retention. Video readiness remains `6/7`; visual readiness is
  `7/7` diagnostic-refined; production readiness remains low/diagnostic-only.
  The next default slice is
  `newsroom-card-placement-post-refinement-render-smoke-v1` because the stable
  PNG paths should allow the existing ignored placement project to reference
  the improved images. Use `newsroom-yym4-card-asset-placement-refresh-v1` only
  if those stable paths do not hold, and keep RSS dry-run integration later.
  Verification observed focused visual-refinement tests `8 passed` and
  adjacent bridge/placement/internal-review regression tests `28 passed`.
- **Newsroom internal review v0.1 prep v1 completed (2026-06-25)**:
  Prepared `newsroom-internal-review-v0.1-prep` as a diagnostic internal
  review package from existing evidence only. No YMM4 launch, render,
  audio/TTS generation, external TTS adoption, real source fetch, real media
  import, `.ymmp` edit, `.ymmp`/mp4/wav/mp3/m4a/media staging or commit,
  dashboard/governance/freshness change, RSS/live ingest, production approval,
  public-readiness claim, or production-quality claim was performed by the
  Agent. New repo artifacts are
  `samples/_probe/newsroom_handoff/internal_review_v0_1_prep_v1.json`,
  `docs/verification/NEWSROOM_INTERNAL_REVIEW_V0_1_PREP_V1_2026-06-25.md`,
  `docs/verification/NEWSROOM_INTERNAL_REVIEW_V0_1_REVIEW_BRIEF_2026-06-25.md`,
  `src/pipeline/newsroom_internal_review_v0_1_prep.py`, and
  `tests/test_newsroom_internal_review_v0_1_prep.py`. The package cites the
  existing diagnostic evidence chain: script/caption import, speaker binding,
  native YMM4/yukkuri audio, 68 sec timing patch, external card asset
  generation, `ImageItem` card placement, card-placement render smoke, render
  duration `00:01:08`, approximate render time `30` sec, and the still-closed
  production/public scope. Candidate identity is
  `diagnostic_bound_speaker_probe_card_placement_v1.mp4`, duration `68` sec,
  fake/review-only diagnostic content, four cards, four dialogue items, and
  `YMM4_native_yukkuri_japanese` voice path. Accepted scope is limited to
  preparing internal review v0.1 from the current diagnostic video and
  benchmark baseline. Not accepted: production pacing, final visual design,
  final narration/script density, real newsroom content, RSS/live ingest,
  rights/publication boundary, production export settings, final artifact
  packaging, or public/prod approval. Video readiness remains `6/7` until
  internal review is actually completed; visual readiness remains
  `7/7` diagnostic; production readiness remains low/diagnostic-only; internal
  review readiness is now `prep_defined`. The next default slice is
  `newsroom-internal-review-v0.1-operator-review-card`, using compact
  freeform review questions rather than a fixed review form. Verification
  observed focused internal-review-prep tests `8 passed`.
- **Newsroom card placement render smoke result readback v1 completed (2026-06-25)**:
  Recorded the user's freeform card-placement render observation, with
  screenshot support, as canonical diagnostic repo evidence. No YMM4 launch,
  render, audio/TTS generation, real media import, `.ymmp` edit, `.ymmp`/mp4/
  wav/mp3/m4a/media staging or commit, external TTS adoption,
  dashboard/governance/freshness change, production visual-quality claim,
  production approval, public-readiness claim, timing strategy change, or
  internal-review implementation was performed by the Agent. New repo artifacts
  are
  `samples/_probe/newsroom_handoff/card_placement_render_smoke_result_readback_v1.json`,
  `docs/verification/NEWSROOM_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_V1_2026-06-25.md`,
  `src/pipeline/newsroom_card_placement_render_smoke_result_readback.py`, and
  `tests/test_newsroom_card_placement_render_smoke_result_readback.py`. The
  ignored local evidence targets remain
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp`
  and
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.mp4`;
  both are under `_tmp/` ignore policy and must remain unstaged/uncommitted.
  Normalized result is `pass`: YMM4 `4.53.0.6` opened the card-placement
  diagnostic project, render completed to
  `diagnostic_bound_speaker_probe_card_placement_v1.mp4`, output duration was
  observed as `00:01:08` / `68` sec, render time was approximately `30` sec,
  four visual cards (`Card 1/4` through `Card 4/4`) were visible as external
  PNG card assets, the preview surface showed title/chips/source-caption/
  subtitle-safe-reserve elements, four dialogue/subtitle items remained
  visible, no obvious visual element breakage was reported, and no native
  audio/timing/dialogue regression was reported. This closes the visual card
  placement render-smoke uncertainty at diagnostic level. Accepted scope is
  limited to current YMM4 diagnostic open/render viability, approximately
  `68` sec output, visible four-card placement, visible dialogue timeline, and
  no reported visual breakage. Not accepted: production visual quality, final
  design system, final narration/script density, public video readiness, real
  newsroom visuals, real content readiness, production approval, final export
  packaging, or publication readiness. Video readiness remains `6/7` until an
  internal review milestone is completed; visual readiness advances to `7/7`;
  production readiness remains low/diagnostic-only. The current render
  observation has been consumed once; no new render is needed for docs/readback
  changes. The next default slice is `newsroom-internal-review-v0.1-prep`.
  Verification observed focused result-readback tests `9 passed`.
- **Newsroom YMM4 card asset placement probe v1 completed (2026-06-25)**:
  Created `newsroom-yym4-card-asset-placement-probe-v1` as the bounded
  diagnostic bridge from external visual card assets into an ignored local
  YMM4 placement copy. No YMM4 launch, video render, audio/TTS generation,
  external TTS adoption, real source fetch, real media import, production
  `.ymmp` edit, `.ymmp`/mp4/wav/mp3/m4a/render-output staging or commit,
  dashboard/governance/freshness change, production approval, public readiness
  claim, or timing strategy change was performed by the Agent. New repo
  artifacts are
  `samples/_probe/newsroom_handoff/yym4_card_asset_placement_probe_v1.json`,
  `docs/verification/NEWSROOM_YYM4_CARD_ASSET_PLACEMENT_PROBE_V1_2026-06-25.md`,
  `src/pipeline/newsroom_yym4_card_asset_placement_probe.py`,
  `tests/test_newsroom_yym4_card_asset_placement_probe.py`, and four
  deterministic PNG card assets under
  `samples/_probe/newsroom_handoff/visual_cards_v1/`, generated from the
  existing SVG cards with a local Pillow SVG-subset renderer. The ignored local
  output
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp`
  was created from the prior ignored timing-patched source copy and must remain
  unstaged/uncommitted. The structural readback is `pass`: the timeline remains
  `4080` frames / `68` sec, the four native `VoiceItem` dialogue rows remain
  preserved, voice/cache fields and the canonical YMM4 native audio path remain
  untouched, and four `ImageItem` card placements were added at frames
  `0/720/1440/2760` with lengths `720/720/1320/1320` on diagnostic layer `2`.
  Direct YMM4 card object graph construction and YMM4 text/shape reconstruction
  remain closed. Accepted scope is limited to external card asset mapping,
  deterministic PNG raster assets, structural image placement in an ignored
  diagnostic copy, and preservation of prior timing/audio evidence. Not
  accepted: post-card render proof, production visual quality, final design
  system, public video readiness, real newsroom visuals, real content
  readiness, or production approval. Video readiness remains `6/7`; visual
  readiness advances to `6/7`; production readiness remains
  low/diagnostic-only. The next default slice is
  `newsroom-card-placement-render-smoke-v1`, and it is milestone-gated because
  the video surface has now changed. Internal review prep remains after the
  post-placement render smoke result is observed. Verification observed focused
  placement and bridge regression tests `20 passed`.
- **Newsroom visual card asset bridge v1 completed (2026-06-25)**:
  Created `newsroom-visual-card-asset-bridge-v1` as a diagnostic external
  visual-asset bridge after the 68 sec timing/audio render smoke passed. No
  YMM4 launch, video render, audio/TTS generation, real source fetch, real media
  import, `.ymmp` edit, `.ymmp`/mp4/media staging or commit, external TTS
  adoption, dashboard/governance/freshness change, production approval, public
  readiness claim, or timing strategy change was performed by the Agent. New
  repo artifacts are
  `samples/_probe/newsroom_handoff/visual_card_asset_bridge_v1.json`,
  `docs/verification/NEWSROOM_VISUAL_CARD_ASSET_BRIDGE_V1_2026-06-25.md`,
  `src/pipeline/newsroom_visual_card_asset_bridge.py`,
  `tests/test_newsroom_visual_card_asset_bridge.py`, and four SVG card assets
  plus `contact_sheet.html` under
  `samples/_probe/newsroom_handoff/visual_cards_v1/`. The four cards map
  one-to-one to the existing neutral caption/dialogue rows:
  `Fake topic, review only.` (`0-12s`), `Review-only handoff stays.` (`12-24s`),
  `A fake claim is shown.` (`24-46s`), and
  `Fake source checks are noted.` (`46-68s`). Each SVG is `1920x1080`, fake
  content only, high-contrast, includes diagnostic/status chips and a
  subtitle-safe lower reserve, and has no real URL, real brand, real media, or
  production-news claim dependency. PNG export is explicitly deferred; the
  deterministic SVG sources and local HTML contact sheet are the bridge output.
  Accepted scope is limited to external visual card assets, a preview/contact
  sheet, caption-row mapping, and suitability for a later bounded YMM4
  image-asset placement probe. Not accepted: production visual quality, final
  design system, YMM4 placement proof, post-card render proof, public video
  readiness, real newsroom visuals, real content readiness, or production
  approval. The placement contract is `future_yym4_placement_mode =
  image_asset_import`, with `direct_yym4_card_object_graph = false` and
  `yym4_text_shape_reconstruction = false`; native YMM4 audio and the existing
  timing strategy are preserved. Video readiness remains `6/7`, visual
  readiness is `4/7`, and production readiness remains low/diagnostic-only.
  The next default slice is `newsroom-yym4-card-asset-placement-probe-v1`,
  followed by `newsroom-card-placement-render-smoke-v1` only after placement
  changes the video surface enough to justify a milestone render. Internal
  review prep remains after visual/card placement is inspectable. Verification
  observed focused bridge tests `10 passed`.
- **Newsroom YMM4 timing patch render smoke result readback v1 completed (2026-06-25)**:
  Recorded the user's freeform post-patch render observation, with screenshot
  support, as canonical diagnostic repo evidence. No YMM4 launch, render,
  audio/TTS generation, real media import, `.ymmp` edit, `.ymmp`/mp4/media
  staging or commit, external TTS adoption, dashboard/governance/freshness
  change, production approval, public-readiness claim, or visual implementation
  was performed by the Agent. New repo artifacts are
  `samples/_probe/newsroom_handoff/ymmp_timing_patch_render_smoke_result_readback_v1.json`,
  `docs/verification/NEWSROOM_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_V1_2026-06-25.md`,
  `src/pipeline/newsroom_ymmp_timing_patch_render_smoke_result_readback.py`, and
  `tests/test_newsroom_ymmp_timing_patch_render_smoke_result_readback.py`. The
  ignored local evidence targets remain
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp`
  and
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.mp4`;
  both are under `_tmp/` ignore policy and must remain unstaged/uncommitted.
  Normalized result is `pass`: YMM4 opened the patched diagnostic project,
  render completed, output video was observed as `00:01:08` / `68` sec,
  expected duration was `68` sec, output properties were `1920x1080`, `60` fps,
  audio stream present at `48kHz`, four dialogue items remained visible,
  preview text included `Fake topic, review only.`, native YMM4/Yukkuri audio
  was present, most of the sparse diagnostic timeline was silent, only
  post-speech/timeline elements were extended, and the timing patch was
  effective in rendered output. The 8 sec versus 68 sec uncertainty is now
  closed at diagnostic render-smoke level. Accepted scope is limited to current
  YMM4 diagnostic open/render viability, 68 sec timing patch effectiveness,
  four dialogue items visible, native Yukkuri audio present, and expected
  sparse silence for the diagnostic skeleton. Not accepted: production pacing,
  final narration pacing, final script density, visual layout quality, public
  video readiness, production render readiness, real content readiness,
  production approval, or external TTS adoption. Video readiness advances to
  `6/7`; production readiness remains low/diagnostic-only. The current render
  observation has been consumed once; no new render is needed for docs/readback
  changes. The next default slice is `newsroom-visual-card-asset-bridge-v1`,
  using external card assets generated from HTML/SVG/Canvas rather than fragile
  direct YMM4 object graph construction. After the visual/card bridge, the
  follow-up milestone is `newsroom-internal-review-v0.1-prep`. Render output
  retention remains optional via `newsroom-render-output-retention-policy-v1`
  only if a later retention gate is explicitly opened. Verification observed
  focused result-readback tests `13 passed`.
- **Newsroom YMM4 timing patch render smoke package v1 prepared (2026-06-25)**:
  Prepared `newsroom-ymmp-timing-patch-render-smoke-v1` as an observation
  package only, without launching YMM4, rendering, modifying the patched
  `.ymmp`, generating or replacing audio, importing media, changing timing
  strategy, staging/committing `.ymmp` or media output, approving production, or
  touching dashboard/governance/freshness work. New repo artifacts are
  `samples/_probe/newsroom_handoff/ymmp_timing_patch_render_smoke_v1.json`,
  `docs/verification/NEWSROOM_YMMP_TIMING_PATCH_RENDER_SMOKE_V1_2026-06-25.md`,
  `src/pipeline/newsroom_ymmp_timing_patch_render_smoke.py`, and
  `tests/test_newsroom_ymmp_timing_patch_render_smoke.py`. The only manual
  target remains the ignored local patched diagnostic copy
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp`;
  it was confirmed present and ignored under `_tmp/`, and must remain unstaged
  and uncommitted. The package reuses the structural timing patch readback:
  `4080` frames / `68.0` sec at `60` fps, dialogue anchors
  `0/720/1440/2760`, item lengths `720/720/1320/1320`, four dialogue items,
  preserved native voice fields, and external TTS still closed. The operator
  card intentionally keeps the next observation to five targets only: whether
  the patched project opens, whether render completes, whether output duration
  is approximately `68` seconds, whether the four dialogue items remain, and
  whether native YMM4/Yukkuri audio remains present. The result normalization
  schema and readback builder are agent-owned; user input remains freeform, not
  a fixed form. The classification matrix now separates pass, project-open
  failure, render failure, duration mismatch, dialogue preservation regression,
  native-audio preservation regression, and operator uncertainty. Verification
  observed focused render smoke package tests `14 passed`. Current accepted
  scope is only readiness to perform exactly one milestone-gated manual render
  smoke; post-patch render success, production render readiness, public video
  readiness, visual layout readiness, production narration quality, real
  content readiness, production approval, and committing `.ymmp`/media output
  remain not accepted. The next manual milestone is to open/render the patched
  diagnostic copy once in YMM4. After that observation exists, the exact next
  agent slice is
  `newsroom-ymmp-timing-patch-render-smoke-result-readback-v1`.
- **Newsroom timing patch remote handoff sealed (2026-06-24)**:
  Preserved the supervisor-accepted state for the timing patch probe and
  verified local/remote parity for another-terminal restart. `master` was
  fetched from `origin`, `HEAD...origin/master` was `0 0`, and `HEAD` was
  `a0a3485 feat: probe newsroom YMM4 timing patch` before this handoff docs
  update. The latest supervisor decision accepts the structural timing patch
  proof and defers the next progress step until one manual YMM4 observation is
  available. The active local-only target remains
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp`;
  it is intentionally ignored under `_tmp/` and must not be staged or
  committed. The required user-side action is exactly one milestone render
  smoke in YMM4: open the patched diagnostic copy, render once, and report
  whether it opens/renders, whether the output is about `68` sec, and whether
  the four dialogue rows and native Yukkuri voice remain obviously present.
  Post-observation agent work is
  `newsroom-ymmp-timing-patch-render-smoke-result-readback-v1`, producing a
  repo readback from the freeform observation. Stored handoff details live in
  `docs/verification/NEWSROOM_YMMP_TIMING_PATCH_REMOTE_HANDOFF_2026-06-24.md`.
  Not accepted: production render readiness, public video readiness,
  production narration quality, visual layout readiness, real content
  readiness, production approval, or committing `.ymmp`/media output.
- **Newsroom YMM4 timing patch probe v1 completed (2026-06-24)**:
  Applied the selected diagnostic timing patch strategy to an ignored local
  `.ymmp` copy, without launching YMM4, rendering, generating TTS/audio,
  importing real media, modifying the original source `.ymmp`, staging or
  committing `.ymmp`/media output, approving production, or changing
  dashboard/governance/freshness work. New repo artifacts:
  `samples/_probe/newsroom_handoff/ymmp_timing_patch_probe_v1.json`,
  `samples/_probe/newsroom_handoff/ymmp_timing_patch_probe_readback_v1.json`,
  `docs/verification/NEWSROOM_YMMP_TIMING_PATCH_PROBE_V1_2026-06-24.md`,
  `src/pipeline/newsroom_ymmp_timing_patch_probe.py`, and
  `tests/test_newsroom_ymmp_timing_patch_probe.py`. The ignored diagnostic copy
  is `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp`;
  it is under the repo `_tmp/` ignore rule and must stay unstaged/uncommitted.
  The original source copy remains
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp`.
  The patch method is
  `neutral_timeline_skeleton_patch_with_native_voice_preserved`: map the four
  existing `VoiceItem` rows to the four neutral caption rows by text and order,
  set `Timelines[0].Length` from `509` to `4080`, set `Frame` values to
  `0/720/1440/2760`, and set `Length` values to `720/720/1320/1320` at `60`
  fps. Structural readback passed: patched total duration is `4080` frames /
  `68.0` sec, end frames are `720/1440/2760/4080`, and no fallback carrier was
  needed. Speaker/text/native YMM4 fields were preserved for all rows:
  `CharacterName`, `Serif`, `VoiceCache`, `VoiceParameter`, `Pronounce`,
  `Hatsuon`, `VoiceLength`, `AudioEffects`, the `Characters` block, and
  `AquesTalk` hints. External TTS remains closed; no voice/audio was stretched,
  regenerated, or replaced. This is a structural timing proof only: production
  render readiness, public video readiness, production narration quality,
  visual layout readiness, real content readiness, production approval, and
  post-patch render smoke remain not accepted. Next slice is
  `newsroom-ymmp-timing-patch-render-smoke-v1`: open/render the ignored patched
  diagnostic copy only as a milestone smoke, then record whether YMM4 accepts
  the 68 sec patched timeline surface. Verification observed focused timing
  patch probe tests `11 passed`, related timing tests `24 passed`, and full
  repo validation `uv run pytest` with `865 passed, 28 skipped`; remote parity
  was verified in the subsequent timing patch remote handoff.
- **Newsroom YMM4 timing patch strategy v1 completed (2026-06-24)**:
  Defined the diagnostic `.ymmp` timing patch strategy after tiny render smoke
  and native audio path acceptance, without launching YMM4, rendering,
  generating TTS/audio, importing real media, editing/staging/committing
  `.ymmp`, staging or committing media output, approving production, or changing
  dashboard/governance/freshness work. New artifacts:
  `samples/_probe/newsroom_handoff/ymmp_timing_patch_strategy_v1.json`,
  `docs/verification/NEWSROOM_YMMP_TIMING_PATCH_STRATEGY_V1_2026-06-24.md`,
  `src/pipeline/newsroom_ymmp_timing_patch_strategy.py`, and
  `tests/test_newsroom_ymmp_timing_patch_strategy.py`. Source validation reuses
  `audio_observation_and_timing_patch_readiness_v1.json`,
  `yym4_native_audio_path_proof_v1.json`,
  `tiny_render_smoke_result_readback_v1.json`,
  `diagnostic_ymmp_structure_readback_v1.json`,
  `neutral_timeline_import_proof_v1.json`, and
  `yym4_timing_gap_strategy_v1.json`; canonical speaker remains
  `ゆっくり霊夢`. Current timing state is fixed as YMM4 natural duration
  approximately `8` sec / `509` frames at `60` fps versus neutral timeline
  `68` sec / `4080` frames, with `timing_gap_status=unresolved`,
  `audio_path_status=diagnostic_pass`, and `external_TTS_status=closed`.
  Candidate comparison covered keeping natural timing, global scaling to
  `68` sec, aligning dialogue start/end frames to neutral anchors, adding a
  neutral-duration tail/carrier, and deferring until script density increases.
  Recommended default is
  `neutral_timeline_skeleton_patch_with_native_voice_preserved`: move toward a
  `68` sec structural proof while preserving native YMM4 speaker/text,
  `VoiceCache`, `VoiceParameter`, `Pronounce`/`Hatsuon`, `VoiceLength` unless a
  timing-only readback proves otherwise, `AudioEffects`, and native engine hints;
  do not introduce external TTS, stretch/regenerate voice audio, or treat sparse
  long gaps as production quality. Next slice is
  `newsroom-ymmp-timing-patch-probe-v1`: create a JSON patch plan first, then
  use an ignored local `.ymmp` copy only if the plan passes; patch only
  `Frame`, `Length`, timeline/project duration metadata if required, or
  non-voice carrier timing fields; parse the patched copy into repo readback;
  and keep render deferred until structural readback passes. Render remains
  milestone-gated at `L0 No Render`; next render trigger is after the timing
  patch probe changes the timeline surface and structural readback passes,
  expected as `L2 Tiny Smoke Render` or `L3 Targeted Regression Render`.
  Not accepted: production render readiness, public video readiness, production
  narration quality, final script/narration quality, visual layout readiness,
  real content readiness, production approval, external TTS adoption, and
  neutral `68` sec timing proof until the patch/probe actually proves it.
  Human-burden hygiene remains closed: user input is freeform, schema owner is
  Agent, User-Side Work is none, no fixed form or negative confirmation
  checklist was introduced, and no repeated audio/render review was requested.
  Verification observed focused timing patch strategy tests `13 passed`; full
  validation and git push status are owned by the current completion turn.
- **Newsroom audio observation and timing patch readiness v1 completed (2026-06-24)**:
  Recorded the user's freeform tiny-render audio observation as diagnostic repo
  readback and reopened the next axis as timing patch strategy, after a bounded
  permission preflight passed. `git fetch --all --prune` succeeded on the first
  Codex attempt, `HEAD...origin/master` was `0 0`, `HEAD` was `482f5fc`, and
  canonical artifact/docs/tests/src write-delete probes all passed before any
  artifact was created. New artifacts:
  `samples/_probe/newsroom_handoff/audio_observation_and_timing_patch_readiness_v1.json`,
  `docs/verification/NEWSROOM_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_V1_2026-06-24.md`,
  `src/pipeline/newsroom_audio_observation_and_timing_patch_readiness.py`, and
  `tests/test_newsroom_audio_observation_and_timing_patch_readiness.py`. Source
  validation reuses `yym4_native_audio_path_proof_v1.json`,
  `tiny_render_smoke_result_readback_v1.json`, `audio_tts_boundary_v1.json`,
  `yym4_timing_gap_strategy_v1.json`, and
  `diagnostic_ymmp_structure_readback_v1.json`; canonical speaker remains
  `ゆっくり霊夢`. Normalized audio observation is now
  `audio_presence_in_render=true`,
  `voice_path=YMM4_native_yukkuri_japanese`,
  `english_word_handling=katakana_loanword_style`, observed example
  `Fake -> フェイク`, `spelling_read_issue=false`,
  `diagnostic_audio_path_accepted=true`, and
  `audio_quality_accepted_for_diagnostic_flow=true`. Production narration
  quality, production TTS readiness, external TTS, public video readiness,
  visual layout readiness, real content readiness, production approval, and
  neutral `68` sec timing proof all remain false/not accepted. Timing readiness
  records the tiny render as approximately `8` sec YMM4 natural duration versus
  neutral timeline total `68` sec; `timing_gap_status` remains `unresolved`, so
  the recommended next slice is `newsroom-ymmp-timing-patch-strategy-v1`, then
  `newsroom-ymmp-timing-patch-probe-v1`, then a milestone-gated render smoke
  only after timing patch or another output-affecting milestone. No YMM4 launch,
  render, TTS/audio generation, real media import, `.ymmp` edit/stage/commit,
  media output stage/commit, dashboard/governance/freshness change, or
  production approval was performed. Human-burden hygiene remains closed:
  user input was freeform, schema owner is Agent, User-Side Work is none, no
  fixed form or negative confirmation checklist was introduced, and future
  look-for points stay capped at three if needed. Verification observed focused
  audio observation/timing readiness tests `11 passed`; full validation and git
  push status are owned by the current completion turn.
- **Newsroom YMM4 native audio path proof v1 completed (2026-06-24)**:
  Proved the diagnostic YMM4 native voice/audio path as the next default from
  existing repo readbacks, without launching YMM4, rendering, generating
  TTS/audio, importing real media, creating/modifying/staging/committing
  `.ymmp`, staging or committing media output, approving production, or changing
  dashboard/governance/freshness work. New artifacts:
  `samples/_probe/newsroom_handoff/yym4_native_audio_path_proof_v1.json`,
  `docs/verification/NEWSROOM_YYM4_NATIVE_AUDIO_PATH_PROOF_V1_2026-06-24.md`,
  `src/pipeline/newsroom_yym4_native_audio_path_proof.py`, and
  `tests/test_newsroom_yym4_native_audio_path_proof.py`. Source validation
  reuses `audio_tts_boundary_v1.json`,
  `tiny_render_smoke_result_readback_v1.json`, and
  `diagnostic_ymmp_structure_readback_v1.json`; canonical speaker remains
  `ゆっくり霊夢`. Proof status is `passed_with_unknowns`: the parsed `.ymmp`
  has four YMM4 `VoiceItem` rows, four `VoiceCache` entries, `VoiceLength`,
  `Pronounce`/`Hatsuon`, and native engine hint `AquesTalk`, so native field
  sufficiency is accepted for the diagnostic path. Audio presence in the render
  remains `unknown`, `audio_quality_accepted=false`, `TTS_ready=false`,
  `TTS_generated_by_agent=false`, `explicit_operator_TTS_generation=false`, and
  `external_TTS_introduced=false`; this is not audio acceptance, production
  render readiness, public video readiness, neutral `68` sec timing proof, or
  production approval. Recommended default is
  `continue_with_YMM4_native_voice_audio_path_for_diagnostic_flow`; recommended
  next slice is `newsroom-ymmp-timing-patch-strategy-v1` because native fields
  are sufficient and the remaining unknown is audible presence/quality rather
  than field sufficiency. If audio presence becomes the actual bottleneck, use
  `newsroom-tiny-render-audio-observation-card-v1`; if native fields drift or
  go missing, use `newsroom-yym4-native-audio-field-audit-v1`. Human-burden
  hygiene remains closed: User-Side Work is none, user input remains freeform,
  no fixed-form result template is introduced, screenshots are optional, and no
  negative confirmation checklist is requested. Verification observed focused
  native audio path proof tests `11 passed`.
- **Newsroom audio/TTS boundary resume handoff sealed (2026-06-24)**:
  Mainline restart state has been rechecked and preserved for another terminal.
  Target checkout is
  `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage`
  because `master` is attached to that worktree; the sibling
  `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen` checkout remains on
  `codex/baseball-bn08-script-beat-linkage` and is not the mainline handoff
  target. Before this docs handoff, `master` was fetched/pulled from
  `origin/master`, `HEAD...origin/master` was `0 0`, `HEAD` was
  `16dcadc docs: define newsroom audio tts boundary`, and the tracked working
  tree was clean. The active handoff artifacts were confirmed present:
  `samples/_probe/newsroom_handoff/audio_tts_boundary_v1.json`,
  `docs/verification/NEWSROOM_AUDIO_TTS_BOUNDARY_V1_2026-06-23.md`,
  `samples/_probe/newsroom_handoff/tiny_render_smoke_result_readback_v1.json`,
  `docs/verification/NEWSROOM_TINY_RENDER_SMOKE_RESULT_READBACK_V1_2026-06-23.md`,
  `samples/_probe/newsroom_handoff/yym4_timing_gap_strategy_v1.json`,
  `samples/_probe/newsroom_handoff/diagnostic_ymmp_structure_readback_v1.json`,
  and
  `docs/verification/NEWSROOM_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_V1_2026-06-23.md`.
  Carry-forward state remains diagnostic-only: tiny render smoke passed by prior
  user freeform observation with four dialogue lines visible and about `8` sec
  natural YMM4 duration; canonical speaker remains `ゆっくり霊夢`;
  `.ymmp` voice fields and VoiceCache exist, but `audio_presence_in_render` is
  `unknown`, `audio_quality_accepted=false`, and `TTS_ready=false`. External
  TTS remains closed; metadata-only voice profile remains planning-only; no-audio
  render remains a fallback only. Recommended next entry is
  `newsroom-yym4-native-audio-path-proof-v1`, before any neutral `68` sec timing
  patch work, because the native YMM4 voice/audio path is the current diagnostic
  default and audio/TTS responsibility should not be mixed with timing patching.
  No YMM4 launch, render, TTS/audio generation, real media import, `.ymmp` or
  media staging/commit, dashboard/governance/freshness work, production approval,
  or public-readiness claim was performed in this resume/handoff slice. Ignored
  local residue such as `_tmp/` and Python `__pycache__/` may exist and is not
  part of the handoff.
- **Newsroom audio/TTS boundary v1 completed (2026-06-23)**:
  Defined the diagnostic audio/TTS boundary after the tiny render smoke result,
  without launching YMM4, rendering, generating TTS/audio, importing real media,
  creating/modifying/staging/committing `.ymmp`, committing render output,
  approving production, or changing dashboard/governance/freshness work. New
  artifacts:
  `samples/_probe/newsroom_handoff/audio_tts_boundary_v1.json`,
  `docs/verification/NEWSROOM_AUDIO_TTS_BOUNDARY_V1_2026-06-23.md`,
  `src/pipeline/newsroom_audio_tts_boundary.py`, and
  `tests/test_newsroom_audio_tts_boundary.py`. Source validation reuses
  `tiny_render_smoke_result_readback_v1.json`,
  `diagnostic_ymmp_structure_readback_v1.json`, and
  `yym4_timing_gap_strategy_v1.json`. Known render result remains diagnostic:
  `pass`, output video observed, four dialogue lines visible, approximate
  duration `8` sec, YMM4 natural duration, neutral `68` sec timing patch not
  applied. `.ymmp` voice fields are present (`VoiceLength`, `VoiceCache`,
  `VoiceParameter`, `Pronounce`, `Hatsuon`, `AudioEffects`), with four voice
  items, four voice caches, and `AquesTalk`; however render success and
  VoiceCache presence do not establish audio presence or audio quality.
  Current audio state is intentionally bounded: `audio_presence_in_render` is
  `unknown`, `audio_quality_accepted=false`, `TTS_ready=false`,
  `TTS_generated_by_agent=false`, `explicit_operator_TTS_generation=false`,
  and voice binding is only `partial` for diagnostic import with canonical
  speaker `ゆっくり霊夢`. Recommended default is to keep the YMM4 native
  voice/audio path as the next diagnostic path, keep external TTS closed, and
  use a compact freeform audio observation only if audio becomes the next
  bottleneck. First render smoke used natural timing; neutral `68` sec timing
  patch remains deferred, and timing should not be patched before audio/TTS
  boundary is understood. Next axes are
  `newsroom-tiny-render-audio-observation-card-v1` if audio presence is needed,
  `newsroom-yym4-native-audio-path-proof-v1` if the native path must be proven
  first, or `newsroom-ymmp-timing-patch-strategy-v1` if existing audio evidence
  is sufficient for the next decision. Human-burden hygiene remains closed:
  User-Side Work is none, future observation stays freeform with at most three
  look-for points, screenshots are optional, negative confirmations are not
  required, and no fixed-form relapse is introduced. Verification observed
  focused audio/TTS boundary tests `11 passed`.
- **Newsroom tiny render smoke result readback v1 completed (2026-06-23)**:
  Recorded the user's freeform manual tiny render smoke observation as a
  diagnostic-only repo readback, without launching YMM4 from the Agent,
  rendering, creating/modifying/staging/committing `.ymmp`, generating
  TTS/audio, importing real media, approving production, committing render
  output, or changing dashboard/governance/freshness work. Machine readback:
  `samples/_probe/newsroom_handoff/tiny_render_smoke_result_readback_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_TINY_RENDER_SMOKE_RESULT_READBACK_V1_2026-06-23.md`.
  The normalized result is `pass`: render completed, output video was observed,
  four dialogue lines were visible, and duration was approximately `8` seconds
  with `short_natural_duration`. The local output path
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.mp4` was
  discoverable as an ignored diagnostic file, but it was not staged or
  committed. Accepted scope is limited to current-environment diagnostic tiny
  render viability and four-line visibility. Not accepted: production render
  readiness, public video readiness, neutral `68` second timing proof, visual
  layout readiness, TTS/audio quality acceptance, real content readiness, or
  production approval. Timing gap remains `unresolved`: neutral timeline total
  stays `68` seconds while the first smoke remains natural/short; recommended
  next axes are `newsroom-audio-tts-boundary-v1`,
  `newsroom-ymmp-timing-patch-strategy-v1`, and
  `newsroom-render-output-retention-policy-v1` only if the ignored mp4 needs
  retention. Human-burden hygiene remains closed: user input is freeform,
  `template_required=false`, schema owner is Agent, future observation prompts
  stay at maximum three look-for points, screenshots are optional, negative
  confirmations are not required, no fixed-form relapse is introduced, and
  User-Side Work is none.
- **Newsroom tiny render smoke boundary v1 completed (2026-06-23)**:
  Prepared a diagnostic-only tiny render smoke boundary/operator packet from
  the accepted YMM4 timing gap strategy, without launching YMM4, rendering,
  creating/modifying/staging/committing `.ymmp`, generating TTS/audio, importing
  real media, approving production, or changing dashboard/governance/freshness
  work. New artifacts:
  `samples/_probe/newsroom_handoff/tiny_render_smoke_boundary_v1.json`,
  `docs/verification/NEWSROOM_TINY_RENDER_SMOKE_BOUNDARY_V1_2026-06-23.md`,
  `src/pipeline/newsroom_tiny_render_smoke_boundary.py`, and
  `tests/test_newsroom_tiny_render_smoke_boundary.py`. The boundary reuses
  `yym4_timing_gap_strategy_v1.json`,
  `diagnostic_ymmp_structure_readback_v1.json`, and
  `diagnostic_ymmp_manual_result_readback_v1.json`; canonical speaker remains
  the decoded UI-observed `ゆっくり霊夢` value represented by Unicode codepoints
  `\u3086\u3063\u304f\u308a\u970a\u5922`. The target diagnostic `.ymmp` path is
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp`,
  discoverable locally and ignored under `_tmp/`; it remains untracked and must
  not be staged or committed. Future manual action is limited to opening YMM4,
  opening that diagnostic `.ymmp`, and, if comfortable, exporting one tiny
  diagnostic render smoke without changing timing. The Operator Observation
  Card has three look-for points: whether render completes or fails, whether
  output plays and contains the four dialogue lines, and whether duration stays
  short/natural rather than `68` sec. First smoke timing mode is YMM4 natural
  duration (`509` frames / `60` fps / `8.483333` sec); neutral `68` sec timing
  patch remains deferred to `newsroom-ymmp-timing-patch-strategy-v1`. If a
  future manual smoke succeeds, next slice is
  `newsroom-tiny-render-smoke-result-readback-v1`; if it fails,
  `newsroom-yym4-render-failure-classification-v1`; if operator instructions
  need refinement, `newsroom-yym4-render-operator-instruction-polish-v1`.
  Human-burden hygiene remains closed for this Agent slice: user input is
  freeform, `template_required=false`, schema owner is Agent,
  `max_required_points=3`, screenshots are optional, negative confirmations
  are not required, and User-Side Work is none. Verification observed focused
  tiny render smoke boundary tests `9 passed`.
- **Newsroom YMM4 timing gap strategy v1 completed (2026-06-23)**:
  Defined the diagnostic timing gap strategy from the saved diagnostic `.ymmp`
  structure readback, without patching/creating/staging/committing `.ymmp`,
  launching YMM4, rendering, generating TTS/audio, importing real media,
  approving production, or changing dashboard/governance/freshness work. New
  artifacts:
  `samples/_probe/newsroom_handoff/yym4_timing_gap_strategy_v1.json`,
  `docs/verification/NEWSROOM_YYM4_TIMING_GAP_STRATEGY_V1_2026-06-23.md`,
  `src/pipeline/newsroom_yym4_timing_gap_strategy.py`, and
  `tests/test_newsroom_yym4_timing_gap_strategy.py`. Source validation reuses
  `diagnostic_ymmp_structure_readback_v1.json` and
  `diagnostic_ymmp_manual_result_readback_v1.json`; canonical speaker remains
  the decoded UI-observed value represented by Unicode codepoints
  `\u3086\u3063\u304f\u308a\u970a\u5922`, with mojibake explicitly rejected.
  Timing facts are now recorded as neutral timeline `68` sec versus saved YMM4
  natural duration `509` frames at `60` fps (`8.483333` sec), item frames
  `0/130/255/369`, item lengths `130/125/114/140`, and gap `59.516667` sec.
  Strategy status is `accepted_for_next_tiny_render_smoke`; recommended default
  is `hybrid_natural_first_then_patch_later`, so the next nonredundant slice is
  `newsroom-tiny-render-smoke-boundary-v1`, followed by
  `newsroom-ymmp-timing-patch-strategy-v1`. Human-burden hygiene remains closed:
  user input is freeform, `template_required=false`, schema owner is Agent,
  Operator Observation Card is none, and User-Side Work is none. Verification
  observed focused timing gap strategy tests `8 passed`.
- **Newsroom diagnostic `.ymmp` speaker canonical correction v2 completed (2026-06-23)**:
  Restored the diagnostic `.ymmp` structure readback canonical speaker to the
  decoded UI-observed value represented by Unicode codepoints
  `\u3086\u3063\u304f\u308a\u970a\u5922`, without launching YMM4,
  editing/staging/committing `.ymmp`, rendering, generating TTS/audio, importing
  real media, approving production, or changing dashboard/governance/freshness
  work. Updated artifacts:
  `samples/_probe/newsroom_handoff/diagnostic_ymmp_structure_readback_v1.json`,
  `docs/verification/NEWSROOM_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_V1_2026-06-23.md`,
  `src/pipeline/newsroom_diagnostic_ymmp_structure_readback.py`, and
  `tests/test_newsroom_diagnostic_ymmp_structure_readback.py`. The readback now
  records both `canonical_speaker_value` and `speaker_value_ui_observed` as that
  decoded value, plus explicit `canonical_speaker_unicode_escape` and
  `speaker_value_ui_observed_unicode_escape` fields so terminal mojibake cannot
  be mistaken for the accepted speaker. Raw `.ymmp` `CharacterName` values
  remain only under raw/encoding fields, and
  `accepted_speaker_value_must_not_equal_mojibake=true`. Boundary status is
  unchanged: `.ymmp` remains ignored under `_tmp/`, not staged or committed;
  render/TTS/real media/production/public video remain false; timing gap remains
  unresolved.
- **Newsroom diagnostic `.ymmp` speaker canonical correction v1 completed (2026-06-23)**:
  Corrected the diagnostic `.ymmp` structure readback speaker canonicalization
  without launching YMM4, editing/staging/committing `.ymmp`, rendering,
  generating TTS/audio, importing real media, approving production, or changing
  dashboard/governance/freshness work. Updated artifacts:
  `samples/_probe/newsroom_handoff/diagnostic_ymmp_structure_readback_v1.json`,
  `docs/verification/NEWSROOM_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_V1_2026-06-23.md`,
  `src/pipeline/newsroom_diagnostic_ymmp_structure_readback.py`, and
  `tests/test_newsroom_diagnostic_ymmp_structure_readback.py`. The accepted
  canonical speaker is now explicitly the decoded UI-observed value represented
  by Unicode codepoints `\u3086\u3063\u304f\u308a\u970a\u5922`, with
  `speaker_value_ui_observed` matching it and
  `accepted_speaker_value_must_not_equal_mojibake=true`. Raw `.ymmp`
  `CharacterName` values remain recorded only under raw/encoding fields with
  `raw_character_name_decoding_status=decoded`; terminal or parser display
  mojibake must not be promoted into accepted canonical speaker fields.
  Boundary status is unchanged: `.ymmp` remains ignored under `_tmp/`, not
  staged or committed; render/TTS/real media/production/public video remain
  false; timing gap remains unresolved. Verification observed focused
  structure readback tests `8 passed`.
- **Newsroom diagnostic `.ymmp` structure readback v1 completed (2026-06-23)**:
  Parsed the locally saved diagnostic `.ymmp` for bounded structure readback,
  without launching YMM4 from the agent, editing `.ymmp`, staging or committing
  `.ymmp`, rendering, generating TTS/audio, importing real media, fetching
  external sources, approving production, or changing dashboard/governance/
  freshness work. Machine readback:
  `samples/_probe/newsroom_handoff/diagnostic_ymmp_structure_readback_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_V1_2026-06-23.md`;
  source manual result:
  `samples/_probe/newsroom_handoff/diagnostic_ymmp_manual_result_readback_v1.json`;
  local source `.ymmp`:
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp`;
  implementation:
  `src/pipeline/newsroom_diagnostic_ymmp_structure_readback.py`; focused
  coverage:
  `tests/test_newsroom_diagnostic_ymmp_structure_readback.py`. Parse status is
  `parsed`: the project has one timeline, four dialogue items, and the four
  expected `Serif` texts. Item timing is `Frame`/`Length` based at 60fps:
  frames `0/130/255/369`, lengths `130/125/114/140`, total timeline length
  `509` frames, approximately `8.483333` seconds. This confirms the saved
  diagnostic project preserved the short/natural YMM4 duration rather than the
  neutral timeline's `68` seconds; timing gap status remains `unresolved`, and
  `timing_patch_applied=false`. Speaker handling is intentionally split:
  canonical UI-observed speaker remains the decoded value represented by
  Unicode codepoints `\u3086\u3063\u304f\u308a\u970a\u5922`, while raw `.ymmp`
  character fields are recorded separately because terminals may display them
  differently. Voice-related fields and voice cache are present on all four
  items, but this is not TTS readiness: `TTS_generated_by_agent=false`,
  `explicit_operator_TTS_generation=false`, and `TTS_ready=false`. Not
  accepted: production `.ymmp`, render readiness, TTS readiness, timing patch
  strategy, public video readiness, production approval, or committing the
  `.ymmp`. Human-burden hygiene remains closed: supplied freeform input is
  enough, no fixed form is emitted, and User-Side Work is none. Next
  nonredundant axes are `newsroom-yym4-timing-gap-strategy-v1`,
  `newsroom-audio-tts-boundary-v1`, and
  `newsroom-tiny-render-smoke-boundary-v1`. Verification observed diagnostic
  `.ymmp` structure readback tests `8 passed`.
- **Newsroom diagnostic `.ymmp` manual result readback v1 completed (2026-06-23)**:
  Recorded the user/operator freeform diagnostic `.ymmp` manual probe
  observation as repo readback, without launching YMM4 from the agent, creating
  or editing `.ymmp`, staging or committing `.ymmp`, rendering, generating
  TTS/audio, importing real media, fetching external sources, approving
  production, or changing dashboard/governance/freshness work. Machine
  readback:
  `samples/_probe/newsroom_handoff/diagnostic_ymmp_manual_result_readback_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_DIAGNOSTIC_YMMP_MANUAL_RESULT_READBACK_V1_2026-06-23.md`;
  source packet:
  `samples/_probe/newsroom_handoff/diagnostic_ymmp_probe_packet_v1.json`;
  source boundary:
  `samples/_probe/newsroom_handoff/minimal_ymmp_boundary_decision_v1.json`;
  source bound CSV:
  `samples/_probe/newsroom_handoff/tiny_script_import_candidate_yukkuri_reimu_v1.csv`;
  implementation:
  `src/pipeline/newsroom_diagnostic_ymmp_manual_result.py`; focused coverage:
  `tests/test_newsroom_diagnostic_ymmp_manual_result.py`. The normalized result
  is `pass`, `manual_probe_status=observed`, and
  `diagnostic_ymmp_saved_or_save_attempt_observed=true`: the user/operator
  observation reports that the diagnostic save/result used the same folder/file
  path, 4 dialogue rows remained visible, the UI-observed speaker represented
  by Unicode codepoints `\u3086\u3063\u304f\u308a\u970a\u5922` was preserved,
  preview text remained visible, and duration
  stayed short/natural. A local diagnostic `.ymmp` file was discoverable at
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp`, but this
  slice records path/status only; the file was not parsed, staged, committed,
  or promoted. Accepted scope is limited to diagnostic manual probe observation,
  row preservation, speaker preservation, and short natural duration
  observation. Not accepted: production `.ymmp`, `.ymmp` structure acceptance,
  timing patch strategy, TTS readiness, render readiness, public video
  readiness, or production approval. Timing gap is carried forward as
  unresolved: neutral timeline metadata remains `68` seconds while the manual
  YMM4 observation remains short/natural, with next axes
  `newsroom-ymmp-structure-readback-v1`,
  `newsroom-yym4-timing-gap-strategy-v1`, and
  `newsroom-audio-tts-boundary-v1`. Human-burden hygiene is closed for this
  slice: the supplied freeform input is sufficient, `template_required=false`,
  schema owner is Agent, `max_required_points=0`, screenshots are optional, no
  negative confirmations are required, and User-Side Work is none. Review debt
  remains bounded with no generic Review Card and no repeated general review
  request. Verification observed diagnostic `.ymmp` manual result readback
  tests `7 passed`.
- **Newsroom diagnostic `.ymmp` probe packet v1 completed (2026-06-23)**:
  Prepared the diagnostic-only packet for a later manual `.ymmp` save probe,
  without launching YMM4 from the agent, creating or editing `.ymmp`,
  rendering, generating TTS/audio, importing real media, fetching external
  sources, approving production, or changing dashboard/governance/freshness
  work. Machine packet:
  `samples/_probe/newsroom_handoff/diagnostic_ymmp_probe_packet_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_DIAGNOSTIC_YMMP_PROBE_PACKET_V1_2026-06-23.md`;
  source boundary:
  `samples/_probe/newsroom_handoff/minimal_ymmp_boundary_decision_v1.json`;
  source bound CSV:
  `samples/_probe/newsroom_handoff/tiny_script_import_candidate_yukkuri_reimu_v1.csv`;
  implementation:
  `src/pipeline/newsroom_diagnostic_ymmp_probe_packet.py`; focused coverage:
  `tests/test_newsroom_diagnostic_ymmp_probe_packet.py`. The packet status is
  `ready_for_future_manual_probe`, `production_status=diagnostic_only`, and
  `manual_probe_status=not_run`; it prepares operator instructions only and
  does not create the recommended diagnostic save path
  `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp`. A later
  user/operator may manually launch YMM4, import the bound-speaker CSV, confirm
  four rows and the bound speaker, and optionally save a diagnostic `.ymmp`
  outside production flow, but committing any `.ymmp` remains disallowed unless
  a later explicit result-readback slice approves it. The Operator Observation
  Card is intentionally freeform: one sentence is enough, only three look-for
  points are listed, screenshots are optional, and no fixed form or negative
  confirmation checklist is required. Timing policy remains observational:
  neutral timeline metadata is `68` seconds, observed YMM4 import was
  approximately `8.48` seconds, the first probe expects YMM4 natural duration,
  and `timing_patch_in_this_probe=false` until project structure is known.
  Recommended next slices are
  `newsroom-diagnostic-ymmp-manual-result-readback-v1`,
  `newsroom-yym4-timing-gap-strategy-v1`, and
  `newsroom-ymmp-structure-readback-v1`. Review Card remains `none`; no
  repeated timing/caption/copy/CSV/script/tiny-proof review is requested.
  Verification observed diagnostic `.ymmp` probe packet tests `7 passed`.
- **Newsroom minimal `.ymmp` boundary decision v1 completed (2026-06-23)**:
  Created a diagnostic-only boundary decision for the next possible `.ymmp`
  step, without launching YMM4 from the agent, creating or editing `.ymmp`,
  rendering, generating TTS/audio, importing real media, fetching external
  sources, approving production, or changing dashboard/governance/freshness
  work. Machine decision:
  `samples/_probe/newsroom_handoff/minimal_ymmp_boundary_decision_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_MINIMAL_YMMP_BOUNDARY_DECISION_V1_2026-06-23.md`;
  source readiness:
  `samples/_probe/newsroom_handoff/yym4_bound_speaker_import_readiness_v1.json`;
  implementation:
  `src/pipeline/newsroom_minimal_ymmp_boundary_decision.py`; focused coverage:
  `tests/test_newsroom_minimal_ymmp_boundary_decision.py`. The decision status
  is `approved_for_next_probe_packet`, not approval to create `.ymmp` in this
  slice. Current `.ymmp` status remains `not_created`,
  `agent_may_create_ymmp_now=false`, while a later user/manual diagnostic
  `.ymmp` probe packet may be prepared. Production `.ymmp`, render, TTS/audio,
  real media, real newsroom ingest, external fetch, production approval, and
  public video remain prohibited. The recommended next path is
  `prepare_manual_diagnostic_ymmp_probe_packet`, with next slice
  `newsroom-diagnostic-ymmp-probe-packet-v1`, because bound speaker CSV import
  is accepted in the current environment but the timing boundary remains open:
  neutral timeline metadata is `68` seconds while the observed YMM4 import is
  approximately `8.48` seconds, and CSV does not import timing metadata. Timing
  policy default is to accept YMM4 natural duration for the first diagnostic
  `.ymmp` probe so the save/readback boundary is isolated before any manual
  timing patch. Human-burden hygiene is explicit: input remains freeform,
  `template_required=false`, schema owner is Agent, screenshot is optional,
  negative confirmations are not required, and the future Operator Observation
  Card has only three look-for points. Review Card remains `none`; no repeated
  timing/caption/copy/CSV/script/tiny-proof review is requested. Verification
  observed minimal `.ymmp` boundary decision tests `7 passed`.
- **Newsroom YMM4 bound speaker import readiness v1 completed (2026-06-23)**:
  Recorded the user/operator freeform observation and screenshot context for
  the committed bound-speaker CSV candidate, without launching YMM4 from the
  agent, creating or editing `.ymmp`, rendering, generating TTS/audio, importing
  real media, fetching external sources, approving production, or changing
  dashboard/governance/freshness work. Machine readback:
  `samples/_probe/newsroom_handoff/yym4_bound_speaker_import_readiness_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_YYM4_BOUND_SPEAKER_IMPORT_READINESS_V1_2026-06-23.md`;
  source CSV:
  `samples/_probe/newsroom_handoff/tiny_script_import_candidate_yukkuri_reimu_v1.csv`;
  implementation:
  `src/pipeline/newsroom_yym4_bound_speaker_import_readiness.py`; focused
  coverage:
  `tests/test_newsroom_yym4_bound_speaker_import_readiness.py`. The normalized
  result is `pass` in Planner007/YMM4 `v4.53.0.6`: the bound CSV displayed
  `4/4` dialogue rows, all text was visible, the speaker-selection prompt was
  not shown, and the `ゆっくり霊夢` speaker value was recognized in the current
  environment. Accepted scope is limited to diagnostic YMM4 script import in
  this environment; not accepted are automatic portability across all YMM4
  installations, TTS readiness, render readiness, production readiness, visual
  layout readiness, `.ymmp` readiness, and public video readiness. The key new
  gap is timing: the prior neutral timeline remains `68` seconds, while the
  observed YMM4 timeline was approximately `8.48` seconds, so the tiny
  `speaker,text` CSV path imports dialogue rows and speaker values, not neutral
  timeline timing metadata. Review Card remains `none`; prior manual import
  behavior review count remains `1`, bound-speaker behavior review count is
  `1`, repeated general timing/caption/copy/CSV/script/tiny-proof review is
  not requested, and the next safe axis is
  `newsroom-minimal-ymmp-boundary-decision-v1` or a timing gap strategy.
  Verification observed bound speaker import readiness tests `6 passed`.
- **Newsroom YMM4 speaker binding policy v1 completed (2026-06-23)**:
  Created a diagnostic-only speaker binding policy from the recorded manual
  import result, without launching YMM4, creating or editing `.ymmp`, rendering,
  generating TTS/audio, importing real media, fetching external sources,
  approving production, or changing dashboard/governance/freshness work.
  Machine policy:
  `samples/_probe/newsroom_handoff/yym4_speaker_binding_policy_v1.json`;
  new bound CSV candidate:
  `samples/_probe/newsroom_handoff/tiny_script_import_candidate_yukkuri_reimu_v1.csv`;
  human readback:
  `docs/verification/NEWSROOM_YYM4_SPEAKER_BINDING_POLICY_V1_2026-06-23.md`;
  implementation:
  `src/pipeline/newsroom_yym4_speaker_binding_policy.py`; focused coverage:
  `tests/test_newsroom_yym4_speaker_binding_policy.py`. The policy preserves
  the manual-result observation that the original tiny CSV imported as
  `pass_with_warnings`: `4/4` dialogue rows and all text were visible, but
  `synthetic_newsroom_placeholder` required manual selection of the existing
  YMM4 character `ゆっくり霊夢`. The recommended default is to test a separate
  candidate CSV that emits that existing character name directly, while keeping
  manual selection as fallback and explicitly not claiming automatic speaker
  binding, TTS readiness, `.ymmp` readiness, render readiness, production
  readiness, YMM4 approval, or public video readiness. The bound CSV is a new
  artifact, preserves UTF-8 BOM and headerless two-column `speaker,text` shape,
  preserves all four text cells exactly, changes only the speaker column, and
  carries status `not_YMM4_verified` / `intended_for_next_manual_check`.
  Review Card remains `none`; prior manual import behavior review count remains
  `1`, repeated general timing/caption/copy/neutral timeline/CSV/script/tiny
  import/manual-result review is not requested, and the next safe slice is
  `newsroom-yym4-bound-speaker-manual-check-packet-v1`. Verification observed
  speaker binding policy tests `6 passed`.
- **Newsroom YMM4 manual import result readback v1 completed (2026-06-23)**:
  Recorded the user/operator YMM4 manual import observation for the committed
  tiny script CSV as repo readback, without launching YMM4 from the agent,
  creating or editing `.ymmp`, rendering, generating TTS/audio, importing real
  media, fetching external sources, or changing dashboard/governance/freshness
  work. Machine readback:
  `samples/_probe/newsroom_handoff/yym4_manual_import_result_readback_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_YYM4_MANUAL_IMPORT_RESULT_READBACK_V1_2026-06-23.md`;
  implementation:
  `src/pipeline/newsroom_yym4_manual_import_result.py`; focused coverage:
  `tests/test_newsroom_yym4_manual_import_result.py`. The recorded result is
  `pass_with_warnings`: the target CSV
  `samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv` showed
  `4/4` dialogue rows in YMM4, all text was visible, no encoding/text/header/
  column/error issue was reported, and the existing character `ゆっくり霊夢`
  was selected when YMM4 requested speaker/character binding. The warning is
  intentional and non-production: speaker binding required manual selection, and
  the operator did not explicitly perform a separate TTS generation
  (`operator_did_not_explicitly_generate_tts`). Accepted scope is limited to
  tiny `speaker,text` CSV import visibility, row text visibility, and manual
  speaker binding observation. Not accepted: automatic speaker binding, TTS
  readiness, render readiness, `.ymmp` readiness, production readiness, and
  public video readiness. Next safe axes are
  `newsroom-speaker-binding-policy-v1`,
  `newsroom-yym4-import-readiness-after-manual-result-v1`, or
  `newsroom-minimal-ymmp-boundary-decision-v1`; do not re-request general
  timing/caption/copy/tiny-proof review for this same observation. Remote
  handoff commit `b107473 docs: record newsroom YMM4 manual import result` is
  on `origin/master`; final validation observed `HEAD...origin/master = 0 0`,
  clean worktree, JSON parse pass, compileall pass, and focused YMM4 manual
  result/check/tiny proof tests `22 passed`.
- **Newsroom YMM4 manual import check packet v1 completed (2026-06-22)**:
  Created a diagnostic-only manual YMM4 import check packet for the committed
  tiny script CSV without launching YMM4 or claiming any import result. Machine
  packet:
  `samples/_probe/newsroom_handoff/yym4_manual_import_check_packet_v1.json`;
  blank operator result template:
  `samples/_probe/newsroom_handoff/yym4_manual_import_result_template_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_YYM4_MANUAL_IMPORT_CHECK_PACKET_V1_2026-06-22.md`;
  implementation:
  `src/pipeline/newsroom_yym4_manual_import_check_packet.py`; focused
  coverage: `tests/test_newsroom_yym4_manual_import_check_packet.py`. The
  packet binds the existing target
  `samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv` and
  source proof `samples/_probe/newsroom_handoff/tiny_importable_proof_v1.json`,
  verifies the target CSV as UTF-8 BOM, headerless, two-column `speaker,text`,
  and exactly four rows, and sets `manual_check_status=not_run` throughout. The
  manual procedure uses only the repo-known YMM4 script import / 台本読み込み
  route and tells the operator to stop at row visibility/preview, record
  uncertainty instead of guessing menu names, avoid production projects, avoid
  render/TTS/audio/real media, and not commit any experimental `.ymmp` unless a
  later explicit slice requests it. The expected pass observation is four
  visible rows, a visible or safely unmapped synthetic speaker placeholder, all
  four texts present, no timing import, and no audio/media/render. Failure
  categories are bounded to encoding, header/column mismatch, speaker binding,
  text import, row count, unsupported shape, operator menu uncertainty, and
  unexpected YMM4 behavior. Result recording is limited to the blank template
  fields (`screenshot_path_placeholder`, observed line count, speaker/text
  behavior, error message, operator notes, and
  `pass|pass_with_warnings|fail|blocked_by_operator_uncertainty`). Safety
  boundary remains closed (`ymmp_created_by_agent=false`,
  `YMM4_launched_by_agent=false`, `render_created=false`,
  `TTS_generated=false`, `real_media_imported=false`,
  `production_approval=false`, `public_video_ready=false`), and no real packet
  ingest, external fetch, source URL access, media download,
  dashboard/governance/freshness expansion, production approval, or publishing
  work was performed. Verification observed manual import check packet, tiny
  importable proof, YMM4-adjacent shape, and CSV handoff tests `27 passed`.
  Next safe action is a human/operator result readback after manual YMM4
  observation, or a bounded instruction/CSV-shape follow-up based only on that
  recorded result.
- **Newsroom tiny importable proof v1 completed (2026-06-22)**:
  Created the first diagnostic-only tiny import artifact from the committed
  YMM4-adjacent no-media import-shape proof. Import artifact:
  `samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv`;
  machine proof:
  `samples/_probe/newsroom_handoff/tiny_importable_proof_v1.json`; human
  readback:
  `docs/verification/NEWSROOM_TINY_IMPORTABLE_PROOF_V1_2026-06-22.md`;
  implementation: `src/pipeline/newsroom_tiny_importable_proof.py`; focused
  coverage: `tests/test_newsroom_tiny_importable_proof.py`. The CSV follows
  the repo-known YMM4 script CSV surface from `src/contracts/ymm4_csv_schema.py`:
  UTF-8 BOM, no header, two columns only (`speaker`, `text`), and four rows.
  Each CSV row maps exactly one source YMM4-adjacent mapping row and preserves
  source row id, script line id, caption id, beat id, and start/end/duration
  timing as proof JSON metadata only. The tiny CSV intentionally contains no
  timing columns and no `production_ready` flags. Result:
  `tiny_importable_status=passed_with_warnings`, with warnings only for the
  expected boundary: not YMM4-verified, timing metadata not imported, no audio,
  no media, and the synthetic speaker placeholder is not yet bound to an
  accepted YMM4 character name. Diagnostic safety remains clear
  (`real_urls=false`, `real_media_paths=false`, `TTS_generated=false`,
  `render_created=false`, `ymmp_created=false`, `production_approval=false`);
  YMM4 boundary remains closed (`YMM4_launched=false`,
  `YMM4_carrier_created=false`, `YMM4_approval=false`), production transfer
  remains `blocked`, and `public_video_ready=false`. Verification observed tiny
  importable proof tests `8 passed`. This slice does not ingest a real packet,
  fetch sources, access real URLs, download media, generate TTS/audio, edit or
  generate `.ymmp`, generate YMM4 carriers, launch YMM4, render, approve rights,
  approve production, publish/upload output, or expand
  dashboard/governance/freshness work. Next safe action is
  `newsroom-import-readiness-review-surface-v1`, or a separately gated manual
  import-check packet only if explicitly authorized.
- **Newsroom YMM4-adjacent no-media import-shape proof v1 completed (2026-06-22)**:
  Created a diagnostic-only YMM4-adjacent no-media import-shape proof from the
  committed script import candidate without changing the source script
  candidate, caption CSV, or neutral timeline. Machine artifact:
  `samples/_probe/newsroom_handoff/yym4_adjacent_no_media_import_shape_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_YYM4_ADJACENT_NO_MEDIA_PROOF_V1_2026-06-22.md`;
  implementation:
  `src/pipeline/newsroom_yym4_adjacent_no_media_import_shape.py`; focused
  coverage: `tests/test_newsroom_yym4_adjacent_no_media_import_shape.py`.
  The proof maps the four diagnostic `script_lines` into exactly four
  tool-adjacent rows with `row_kind=dialogue_caption`, preserving source line
  id, caption id, beat id, timing metadata, speaker placeholder, voice
  placeholder, and text. Each row exposes the repo's known YMM4 CSV-adjacent
  surface (`speaker`, `text`) while keeping `start_sec`, `end_sec`, and
  `duration_sec` as metadata because they are not part of the accepted
  two-column YMM4 CSV row minimum. Result:
  `no_media_import_shape_status=passed_with_warnings`,
  `yym4_status=passed_with_warnings`, with warnings only for static contract
  scope: YMM4 was not launched and timing fields are metadata, not known YMM4
  CSV columns. No-media policy is explicit (`captions_and_script_rows_only`,
  `no_render`, `no_TTS`, `no_real_assets`), visual/audio placeholders are
  reference-only, production transfer remains `blocked`, and YMM4 boundary
  remains closed (`ymmp_created=false`, `YMM4_launched=false`,
  `YMM4_carrier_created=false`, `YMM4_approval=false`). Diagnostic safety also
  remains clear (`real_urls=false`, `real_media_paths=false`,
  `TTS_generated=false`, `render_created=false`,
  `production_approval=false`). Verification observed YMM4-adjacent proof,
  script import, caption CSV import, neutral timeline, and CSV handoff tests
  `34 passed`; JSON parse succeeded. This slice does not ingest a real packet,
  fetch sources, access real URLs, download media, generate TTS/audio, edit or
  generate `.ymmp`, generate YMM4 carriers, launch YMM4, render, approve rights,
  approve production, publish/upload output, or expand
  dashboard/governance/freshness work. Next safe action is
  `newsroom-tiny-importable-proof-v1`, gated on whether to emit a real repo
  YMM4 CSV artifact and how to bind the synthetic speaker placeholder to an
  accepted YMM4 character name.
- **Newsroom script import candidate v1 completed (2026-06-22)**:
  Created the diagnostic-only script import candidate from the existing caption
  CSV and neutral timeline proof without changing either source artifact.
  Machine artifact:
  `samples/_probe/newsroom_handoff/script_import_candidate_v1.json`; human
  readback:
  `docs/verification/NEWSROOM_SCRIPT_IMPORT_CANDIDATE_V1_2026-06-22.md`;
  implementation:
  `src/pipeline/newsroom_script_import_candidate.py`; focused coverage:
  `tests/test_newsroom_script_import_candidate.py`. The candidate maps the
  four committed caption CSV rows into exactly four `script_lines`, preserving
  `source_caption_id`, `beat_id`, `start_sec`, `end_sec`, `duration_sec`, and
  `text` for each row, and cross-checks each line against the neutral timeline
  caption item id. Each line is diagnostic-only, `production_ready=false`,
  `tts_ready=false`, uses the synthetic placeholder speaker
  `synthetic_newsroom_placeholder`, and carries a
  `voice_status=placeholder_not_generated` voice profile with
  `TTS_generated=false` and no audio file. Result:
  `script_import_status=passed`, `import_status=candidate_with_placeholders`,
  no mapping errors, no missing CSV captions, no extra script lines, and
  diagnostic safety remains clear (`real_urls=false`,
  `real_media_paths=false`, `TTS_generated=false`, `render_created=false`,
  `ymmp_created=false`, `production_approval=false`). Verification observed
  script import, caption CSV import, and neutral timeline tests `22 passed`;
  JSON parse succeeded. This slice does not ingest a real packet, fetch
  sources, access real URLs, download media, generate TTS/audio, edit or
  generate `.ymmp`, generate YMM4 carriers, render, approve rights, approve
  production, publish/upload output, or expand dashboard/governance/freshness
  work. Next safe action is a `YMM4-adjacent no-media proof`, a script import
  mapping proof, or a tiny importable proof only after another gate.
- **Newsroom caption CSV import candidate v1 completed (2026-06-22)**:
  Validated the existing derived caption CSV as a caption-only diagnostic import
  candidate without regenerating the neutral timeline or CSV. Machine readback:
  `samples/_probe/newsroom_handoff/caption_csv_import_candidate_readback_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_CAPTION_CSV_IMPORT_CANDIDATE_V1_2026-06-22.md`;
  implementation:
  `src/pipeline/newsroom_caption_csv_import_candidate.py`; focused coverage:
  `tests/test_newsroom_caption_csv_import_candidate.py`. The checker reads
  `samples/_probe/newsroom_handoff/caption_import_candidate_v1.csv` against
  `samples/_probe/newsroom_handoff/neutral_timeline_import_proof_v1.json` and
  confirms the caption-only minimum: required columns are present in order, no
  YMM4-specific columns are required, row count is `4`, caption ids and beat ids
  are non-empty, each row has `start_sec < end_sec`, duration equals the timing
  span, text is non-empty, `diagnostic_only=true`, and `production_ready=false`.
  The readback also confirms every CSV caption id exists in the neutral
  timeline caption items, timing and text match, no CSV caption rows are missing
  or extra, and diagnostic safety remains clear (`real_urls=false`,
  `real_media_paths=false`, `TTS_generated=false`, `render_created=false`,
  `ymmp_created=false`, `production_approval=false`). Result:
  `caption_csv_import_status=passed`; recommended next slice:
  `newsroom-script-import-candidate-v1`. Verification observed caption CSV
  import candidate tests `7 passed`. This slice does not ingest a real packet,
  fetch sources, access real URLs, download media, generate TTS/audio, edit or
  generate `.ymmp`, generate YMM4 carriers, render, approve rights, approve
  production, publish/upload output, or expand dashboard/governance/freshness
  work.
- **Newsroom neutral timeline import proof v1 completed (2026-06-22)**:
  Created the first actual synthetic neutral import proof for the diagnostic
  newsroom episode without opening production/YMM4 transfer. Source-of-truth
  machine artifact:
  `samples/_probe/newsroom_handoff/neutral_timeline_import_proof_v1.json`;
  derived caption CSV:
  `samples/_probe/newsroom_handoff/caption_import_candidate_v1.csv`; human
  readback:
  `docs/verification/NEWSROOM_NEUTRAL_TIMELINE_IMPORT_PROOF_V1_2026-06-22.md`;
  implementation:
  `src/pipeline/newsroom_neutral_timeline_import_proof.py`; focused coverage:
  `tests/test_newsroom_neutral_timeline_import_proof.py`. The timeline uses
  `seconds` timebase, `68` seconds total duration, provisional timing, no FPS
  requirement, and four diagnostic tracks: captions, visual placeholders,
  markers, and an audio placeholder. It carries `4` refined caption items with
  unchanged timing, `2` no-media visual placeholder items with G-28/layout
  hints, `2` beat marker rows, and `1` audio placeholder row with
  `voice_status=not_started`, `TTS_generated=false`, and
  `audio_required_for_this_proof=false`. The caption CSV is derived only from
  JSON caption items and contains `4` rows. Production transfer remains
  `blocked`, `YMM4_candidate=false`, blocker summary remains `7/5/1/0`, and
  Review Card remains `none` to avoid repeated timing/caption/copy/blocker
  review. Verification observed neutral timeline tests `8 passed`. This slice
  does not ingest a real packet, fetch sources, access real URLs, download
  media, generate TTS/audio, edit or generate `.ymmp`, generate YMM4 carriers,
  render, approve rights, approve production, publish/upload output, or expand
  dashboard/governance/freshness work. Next safe action is
  `newsroom-caption-csv-import-candidate-v1` or a script-import candidate that
  consumes the neutral timeline JSON without media.
- **Newsroom diagnostic transfer candidate proof v1 completed (2026-06-22)**:
  Created a synthetic, non-production diagnostic transfer-candidate proof that
  separates production/YMM4 blockage from the next allowable neutral import
  proof lane. Machine artifact:
  `samples/_probe/newsroom_handoff/diagnostic_transfer_candidate_proof_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_DIAGNOSTIC_TRANSFER_CANDIDATE_PROOF_V1_2026-06-22.md`;
  implementation:
  `src/pipeline/newsroom_diagnostic_transfer_candidate_proof.py`; focused
  coverage: `tests/test_newsroom_diagnostic_transfer_candidate_proof.py`.
  The classification source of truth is the current episode capsule, not the
  older transfer-planning readback: the proof classifies all `13` current
  blockers into `7` production-only blockers, `5` diagnostic soft warnings,
  `1` already-satisfied synthetic condition, and `0` diagnostic hard blockers.
  Production transfer remains `blocked`, `YMM4_candidate=false`, and no
  production approval is implied. The diagnostic answer is only
  `candidate_with_placeholders`: caption units, timing windows, refined caption
  copy, and visual placeholder references are present enough to open a next
  tiny neutral timeline JSON / optional caption CSV proof, while YMM4-specific
  mapping, track kind, placeholder asset policy, no-audio/no-media flags, and
  slot-warning carry-forward remain the next required fields. Verification
  observed diagnostic transfer tests `8 passed`. This slice does not ingest a
  real packet, fetch sources, access real URLs, download media, generate
  TTS/audio, edit or generate `.ymmp`, generate YMM4 carriers, render, approve
  rights, approve production, publish/upload output, or expand
  dashboard/governance/freshness work. Next safe action is
  `newsroom-neutral-timeline-import-proof-v1`, still diagnostic-only and
  no-media, or a focused audit of the blocker classification.
- **Newsroom caption copy refinement v1 completed (2026-06-22)**:
  Created a diagnostic caption-copy refinement layer for the existing
  caption/timing plan without changing timing or opening production paths.
  Machine artifact:
  `samples/_probe/newsroom_handoff/episode_caption_copy_refinement_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_CAPTION_COPY_REFINEMENT_V1_2026-06-22.md`;
  implementation: `src/pipeline/newsroom_caption_copy_refinement.py`; focused
  coverage: `tests/test_newsroom_caption_copy_refinement.py`. The refinement
  keeps the `68` second plan unchanged, preserves two beats and four caption
  units, replaces placeholder copy with four short synthetic captions, records
  char counts, line targets, max-char targets, reading-density bands, beat
  alignment notes, and visual-interference notes, and keeps Review Card status
  `none` to avoid repeating the already validated timing-panel review.
  Verification observed caption-copy tests `6 passed`, existing caption/timing
  tests `7 passed`, existing capsule tests `7 passed`, JSON parse success, and
  clean whitespace checks. Audio/voice remains `not_started`,
  `TTS_generated=false`, transfer remains `blocked`, and
  `YMM4_candidate=false`. This slice does not mutate timing JSON, fetch
  external sources, access real URLs, download media, generate TTS/audio, edit
  or generate `.ymmp`, generate YMM4 carriers, render, approve rights, approve
  production, publish/upload output, or expand dashboard/governance/freshness
  work. Next safe action is supervisor caption readability review or a later
  non-production transfer-candidate proof only after blockers are resolved.
- **Newsroom Review Console timing panel v1 completed (2026-06-22)**:
  Added a read-only Review Console timing panel for the existing diagnostic
  caption/timing plan. Implementation: `gui/renderer.js`, `gui/style.css`, and
  `gui/review_console_dom_smoke.js`; human verification:
  `docs/verification/NEWSROOM_REVIEW_CONSOLE_TIMING_PANEL_V1_2026-06-22.md`.
  The panel loads
  `samples/_probe/newsroom_handoff/episode_caption_timing_plan_v1.json` through
  the existing Review Console read path and displays `68` seconds, two beat
  timing rows, four caption unit rows, two visual timing / caption-risk rows,
  audio/voice `not_started`, `TTS_generated=false`, transfer `blocked`, and
  `YMM4_candidate=false`. It also shows prohibited next actions for `.ymmp`,
  render, TTS, and production approval, plus allowed review actions for caption
  copy refinement, Review Console timing review, and a later transfer-candidate
  proof only after blockers are resolved. This remains diagnostic-only and
  read-only: no timing JSON mutation, real packet ingest, external fetch, real
  URL access, media download, `.ymmp` edit/generation, YMM4 carrier generation,
  render, TTS/audio, rights approval, production approval, public-use approval,
  publishing, dashboard freshness producer, status producer, or governance work
  was opened. Next safe action is supervisor timing-panel review or caption
  copy refinement if the panel readback is accepted.
- **Newsroom caption / timing plan v1 completed (2026-06-22)**:
  Created a deterministic caption and timing refinement layer from the existing
  diagnostic episode production capsule without opening transfer or media
  production. Machine artifact:
  `samples/_probe/newsroom_handoff/episode_caption_timing_plan_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_CAPTION_TIMING_PLAN_V1_2026-06-22.md`;
  implementation: `src/pipeline/newsroom_caption_timing_plan.py`; focused
  coverage: `tests/test_newsroom_caption_timing_plan.py`. The plan preserves
  the capsule duration at `68` seconds, splits the structure into two
  contiguous beats, maps four semantic caption units to those beat ranges, and
  links the two VisualIR / G-28 rows to visible timing slots and caption-risk
  notes. Timing confidence remains low/provisional because no audio, TTS, or
  rendered timeline exists. Verification observed caption/timing tests
  `7 passed`, existing capsule tests `7 passed`, JSON parse success, and clean
  whitespace checks. Transfer remains blocked, `YMM4_candidate=false`,
  audio/voice is still `not_started`, and this slice does not fetch external
  sources, access real URLs, download media, generate TTS/audio, edit or
  generate `.ymmp`, generate YMM4 carriers, render, approve rights, approve
  production, publish/upload output, or expand dashboard/governance/freshness
  work. Next safe action is supervisor readback review, copy-level caption
  refinement, a read-only Review Console timing panel extension, or a separate
  transfer-candidate proof only after the recorded blockers are resolved.
- **Newsroom Review Console episode preview v1 completed (2026-06-22)**:
  The Review tab now reads the diagnostic episode production capsule and shows
  one video-structure preview inside `#newsroom-handoff-review`. Implementation:
  `gui/renderer.js`, `gui/style.css`, and
  `gui/review_console_dom_smoke.js`; human verification:
  `docs/verification/NEWSROOM_REVIEW_CONSOLE_EPISODE_PREVIEW_V1_2026-06-22.md`.
  The panel loads
  `samples/_probe/newsroom_handoff/episode_production_capsule_v1.json` and
  displays `episode_fake_nlmytgen_delta_v1`, two ScriptIR-like beats, two
  VisualIR / G-28 rows, caption reserve state, provisional `68` second timing,
  audio/voice `not_started`, remaining gaps, allowed next steps, prohibited
  steps, and capsule transfer blockers. DOM smoke observed
  `newsroom episode preview visible with 2 beats / 2 visuals`; focused capsule
  tests observed `7 passed`. This remains read-only and diagnostic-only: no
  real packet ingest, external fetch, real URL access, media download, `.ymmp`
  edit/generation, YMM4 carrier generation, render, TTS/audio, rights approval,
  production approval, public-use approval, publishing, dashboard freshness
  producer, status producer, or governance/reporting expansion was opened.
  Next safe action is supervisor review of the episode preview, caption/timing
  refinement against the capsule, or a separately gated transfer-candidate
  proof only after the recorded blockers are resolved.
- **Newsroom episode production capsule v1 completed (2026-06-22)**:
  Created the diagnostic-only bridge from the adapted fake newsroom export
  packet toward one video structure. Machine artifact:
  `samples/_probe/newsroom_handoff/episode_production_capsule_v1.json`;
  human readback:
  `docs/verification/NEWSROOM_EPISODE_PRODUCTION_CAPSULE_V1_2026-06-22.md`;
  implementation:
  `src/pipeline/newsroom_episode_production_capsule.py`; focused coverage:
  `tests/test_newsroom_episode_production_capsule.py`. The capsule uses the
  adapted packet as the episode identity and recomputes the current validator,
  G-28 slot-linkage, and transfer-planning state: validator `passed`,
  slot-linkage `passed_with_warnings`, transfer planning `blocked`,
  `transfer_status=blocked`, blocker count `13`, unlock requirement count
  `13`. It records ScriptIR-like beats, VisualIR units, G-28 slot refs,
  caption reserve notes, provisional timing, audio/voice `not_started`,
  Review Console next use, and explicit prohibited steps. This slice does not
  continue dashboard freshness/status producer work; it does not accept a real
  packet, fetch sources, open RSS/Inoreader, access real URLs, download media,
  edit or generate `.ymmp`, generate YMM4 carriers, render media, generate TTS,
  approve rights, approve production, or publish/upload output. Next safe
  action is supervisor capsule review or a separate read-only Review Console
  episode preview slice.
- **Common foundation dashboard freshness audit completed (2026-06-22)**:
  Recorded the freshness / status producer / update-boundary audit for the
  master-adopted Common Foundation Cockpit. Human verification:
  `docs/verification/COMMON-FOUNDATION-DASHBOARD-FRESHNESS-AUDIT-V1-2026-06-22.md`.
  The audit classifies `docs/dashboard/project-status.json` and
  `docs/dashboard/index.html` into generated repo facts, derived display
  values, manual editorial status, historical evidence, static access shell,
  and static dashboard layout. It recommends a future minimal status producer
  only as a separate slice, starting with stdout-only observed JSON and
  preserving manual editorial fields unless explicitly patched. Stale detection
  gates now include branch/upstream/parity mismatch, missing links, JSON parse
  failure, launcher failure, missing/invalid screenshot, contradiction with
  this runtime-state file, and forbidden staged residue. This slice does not
  implement a generator, start a real runner, run `codex exec`, add a
  subprocess runner, pipe stdin, create runtime loops, send notifications,
  write `.agent` runtime artifacts, or open G-27/G-28, Newsroom, ClipPipeGen,
  RSS/OPML/Inoreader/NotebookLM, `.ymmp`, render, rights, production,
  publishing, or media output work. Next safe action is supervisor review or a
  separately authorized stdout-only minimal status producer slice.
- **Common foundation dashboard mainline adoption completed (2026-06-22)**:
  Adopted the common foundation cockpit/dashboard surface onto `master` using
  `origin/codex/common-foundation-hold-state-audit` at
  `b2c2cb46cfd0790cb028d8dacb493ab34d751e2f` as a reference only. Human
  verification:
  `docs/verification/COMMON-FOUNDATION-DASHBOARD-MAINLINE-ADOPTION-2026-06-22.md`;
  primary review surface: `docs/dashboard/index.html`; status registry:
  `docs/dashboard/project-status.json`; access guide:
  `docs/dashboard/README.md`; launcher:
  `scripts/operator/open_dashboard.ps1`; screenshot evidence:
  `docs/review/common-foundation-dashboard-2026-06-17.png`. This was a
  master-native regeneration/selective adoption: no full branch merge, no full
  cherry-pick, no replacement of existing `docs/index.md`, and no overwrite of
  master runner/docs files. The dashboard now reports `branch=master`, links
  required template and verification dependencies, and has refreshed Chrome
  headless screenshot evidence. This slice does not start a real runner, run
  `codex exec`, add a subprocess runner, pipe stdin, create runtime loops,
  send notifications, write `.agent` runtime artifacts, or open G-28, G-27,
  Newsroom, ClipPipeGen, RSS/OPML/Inoreader/NotebookLM, `.ymmp`, render,
  rights, production, publishing, or media output work. Next safe action is
  open-only/freeform dashboard review from `master`.
- **Newsroom export adapter CLI v1 completed (2026-06-20)**:
  Exposed the existing fake-fixture adapter proof as
  `adapt-newsroom-export-fixture`, with operator form
  `uv run python -m src.cli.main adapt-newsroom-export-fixture <fixture.json> --out-packet <packet.json> --out-readback <readback.json> --format json`.
  Human verification:
  `docs/verification/NEWSROOM_EXPORT_ADAPTER_CLI_V1_2026-06-20.md`;
  implementation: `src/cli/main.py`; focused coverage:
  `tests/test_newsroom_export_adapter.py`. The command reads an already
  provided fake newsroom export fixture, writes adapted packet/readback JSON
  only when output paths are supplied, and succeeds only while the adapter
  remains fail-closed: validator `passed`, transfer `blocked`,
  slot-linkage `passed_with_warnings`, transfer planning `blocked`, and
  real-packet/rights/media/review/production/YMM4 approvals all false. This
  slice does not modify `newsroom-yt-pipeline`, accept a real packet, fetch
  sources, open RSS/Inoreader, access live source material, download media,
  edit `.ymmp`, generate YMM4 carriers, render media, approve rights, approve
  production, or publish/upload output. Next safe follow-up is adapter
  visibility in a review surface, or a separate real-packet adapter design only
  after supervisor acceptance.
- **Newsroom export adapter proof v1 completed (2026-06-20)**:
  Added a deterministic, diagnostic NLMYTGen-side adapter proof for the fake
  `newsroom-yt-pipeline` export fixture at commit `912ce3b`. Implementation:
  `src/pipeline/newsroom_export_adapter.py`; adapted packet:
  `samples/_probe/newsroom_handoff/adapted_newsroom_export_packet.json`;
  adapter readback:
  `samples/_probe/newsroom_handoff/newsroom_export_adapter_readback.json`;
  human verification:
  `docs/verification/NEWSROOM_EXPORT_ADAPTER_PROOF_V1_2026-06-20.md`;
  focused tests: `tests/test_newsroom_export_adapter.py`. Result: the raw
  newsroom fixture still requires an adapter, while the adapted packet passes
  NLMYTGen structure validation and remains transfer-blocked. Slot-linkage is
  `passed_with_warnings`, and transfer planning remains `blocked` with explicit
  blockers/unlock requirements. This proof preserves rights/media/review holds
  and does not accept a real packet, fetch sources, open RSS/Inoreader, access
  live source material, download media, edit `.ymmp`, generate YMM4 carriers,
  render media, approve rights, approve production, or publish/upload output.
  Next safe follow-up is adapter visibility in a review surface or a scoped CLI
  only after this adapter shape is accepted.
- **Newsroom export fixture compatibility v1 completed (2026-06-20)**:
  Added a diagnostic cross-repo compatibility readback for the fake
  `newsroom-yt-pipeline` export fixture at commit `912ce3b`. Human readback:
  `docs/verification/NEWSROOM_EXPORT_FIXTURE_COMPATIBILITY_V1_2026-06-20.md`;
  machine-readable readback:
  `samples/_probe/newsroom_handoff/newsroom_export_fixture_compatibility_readback.json`;
  focused coverage:
  `tests/test_newsroom_export_fixture_compatibility.py`. Result:
  `passed_with_adapter_warnings_transfer_blocked`. The fake fixture has direct
  matches for identity/topic fields, adapter-required fields for artifact and
  contract naming, metadata, source/provenance, NotebookLM seed, script/visual
  mappings, G-28 hints, warnings, and downstream readiness, plus human-review
  holds for rights/media/review/visual approval. This slice reads the
  newsroom checkout only; it does not modify `newsroom-yt-pipeline`, accept a
  real packet, fetch sources, open RSS/Inoreader, access live source material,
  download media, edit `.ymmp`, generate YMM4 carriers, render media, approve
  rights, approve production, or publish/upload output. Next safe follow-up is
  a narrow NLMYTGen adapter proof if the supervisor promotes this bridge.
- **Newsroom upstream export delta request v1 completed (2026-06-20)**:
  Added an NLMYTGen-side upstream request for the next
  `newsroom-yt-pipeline` export bundle delta. Human readback:
  `docs/verification/NEWSROOM_UPSTREAM_EXPORT_DELTA_REQUEST_V1_2026-06-20.md`;
  machine-readable request:
  `samples/_probe/newsroom_handoff/upstream_export_delta_request.json`;
  focused coverage:
  `tests/test_newsroom_upstream_export_delta_request.py`. The request maps
  required-before-ingest fields, transfer-candidate gates, optional
  enrichments, human-review holds, current NLMYTGen consumers, failure
  behavior, and delta from the current synthetic fixture. This slice does not
  touch `newsroom-yt-pipeline`, accept a real packet, fetch sources, open
  RSS/Inoreader, access live source material, download media, edit `.ymmp`,
  generate YMM4 carriers, render media, approve rights, approve production, or
  publish/upload output. Next safe follow-up is a separate
  `newsroom-yt-pipeline` fixture/export slice if the supervisor promotes this
  request upstream.
- **Newsroom real-packet readiness checklist v1 completed (2026-06-20)**:
  Added a read-only policy/readback gate for future real
  `newsroom-yt-pipeline` export packets before NLMYTGen ingest or transfer
  planning. Machine-readable checklist:
  `samples/_probe/newsroom_handoff/real_packet_readiness_checklist.json`;
  human readback:
  `docs/verification/NEWSROOM_REAL_PACKET_READINESS_CHECKLIST_V1_2026-06-20.md`.
  The checklist classifies required-before-ingest fields,
  required-before-transfer gates, optional enrichments, prohibited/out-of-scope
  responsibilities, and human-review holds. It maps every item to owner,
  current coverage, failure behavior, and next action. This slice does not
  accept a real packet, fetch sources, open RSS/Inoreader, access real URLs,
  download media, edit `.ymmp`, generate YMM4 carriers, render media, approve
  rights, approve production, or mark YMM4 transfer ready. Next safe follow-up
  is an upstream export delta request doc if supervisor review identifies gaps.
- **Newsroom Review Console planning panel v1 completed (2026-06-20)**:
  The existing read-only `#newsroom-handoff-review` panel now also loads
  `samples/_probe/newsroom_handoff/transfer_planning_readback.json` and exposes
  the non-YMM4 transfer-planning state in the Review tab. It shows
  `transfer_status=blocked`, blocker/unlock/warning counts, grouped blockers,
  unlock requirements, prohibited next actions, allowed next actions, artifact
  references, and a candidate summary that keeps the synthetic packet out of
  transfer-candidate status. Verification readback is
  `docs/verification/NEWSROOM_REVIEW_CONSOLE_PLANNING_PANEL_V1_2026-06-20.md`.
  This slice does not create `.ymmp`, YMM4 carriers, renders, external fetches,
  production approval, rights approval, or publication output. Next safe
  follow-up is a real-packet readiness checklist that remains read-only until
  rights, media/source availability, review approval, visual readiness, and
  downstream/YMM4 blockers are cleared.
- **Newsroom transfer-planning proof v1 completed (2026-06-20)**:
  The synthetic newsroom packet now has a non-YMM4 transfer-planning proof that
  consumes the handoff validator result, G-28 slot-linkage readback, and
  read-only Review Console consumer assumption. CLI entry:
  `uv run python -m src.cli.main plan-newsroom-transfer --format json`. JSON
  readback is `samples/_probe/newsroom_handoff/transfer_planning_readback.json`;
  human readback is
  `docs/verification/NEWSROOM_TRANSFER_PLANNING_PROOF_V1_2026-06-20.md`. The
  current result is intentionally `status=blocked` / `transfer_status=blocked`
  with grouped blockers for rights/provenance, media/source availability,
  review approval, visual readiness, and downstream/YMM4 readiness. This slice
  does not create `.ymmp`, YMM4 carriers, renders, external fetches, production
  approval, rights approval, or publication output. Next safe follow-up is a
  read-only Review Console planning panel that displays this proof.
- **Newsroom Review Console consumer v1 completed (2026-06-20)**:
  The Review tab now includes a read-only `#newsroom-handoff-review` panel that
  loads the synthetic newsroom handoff packet and G-28 slot-linkage readback via
  the existing Review Console JSON-read path. It surfaces episode identity,
  validator status, intentionally blocked transfer state, rights/provenance,
  review warnings, readiness blockers, script/visual/slot counts, slot-linkage
  rows, artifact inventory, and positive guardrails for
  `production_visual_approval=false`, `ymm4_transfer_ready=false`,
  `external_fetch=false`, and `raw_source_material=false`. Implementation lives
  in `gui/index.html`, `gui/renderer.js`, `gui/style.css`, and
  `gui/review_console_dom_smoke.js`; verification readback is
  `docs/verification/NEWSROOM_REVIEW_CONSOLE_CONSUMER_V1_2026-06-20.md`. This
  slice does not touch `newsroom-yt-pipeline`, fetch sources, edit `.ymmp`,
  render media, approve rights, or change publication/YMM4 transfer state. Next
  safe follow-up is a separate non-YMM4 transfer-planning proof that consumes
  this Review Console readback.
- **Newsroom G-28 slot-linkage proof v1 completed (2026-06-20)**:
  The synthetic newsroom handoff fixture now has a UI-independent proof that
  links `visual_plan` entries and `g28_slot_hints` to G-28 object catalog slots,
  reference review surfaces, and downstream readiness gates. Implementation
  lives in `src/pipeline/newsroom_handoff_validator.py`; the CLI entry is
  `uv run python -m src.cli.main prove-newsroom-g28-slot-linkage --format json`.
  JSON readback is
  `samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json`, and the
  supervisor-facing readback is
  `docs/verification/NEWSROOM_G28_SLOT_LINKAGE_PROOF_V1_2026-06-20.md`. The
  fixture status is `passed_with_warnings`: all hinted slots are allowed, YMM4
  transfer remains blocked, and the proof intentionally reports unhinted visual
  content slots for future Review Console / transfer-planning work. This slice
  does not implement Review Console UI, touch `newsroom-yt-pipeline`, fetch
  sources, edit `.ymmp`, render media, approve rights, or change publication
  state. Next safe follow-up is a read-only Review Console consumer or a
  separate G-28 transfer-planning slice that consumes this proof.
- **Newsroom handoff validator v1 completed (2026-06-20)**:
  The NLMYTGen-side receiving contract now has a lightweight fail-closed
  validator for the synthetic fixture. The implementation lives in
  `src/pipeline/newsroom_handoff_validator.py`, the CLI entry is
  `uv run python -m src.cli.main validate-newsroom-handoff --format text`, and
  focused coverage lives in `tests/test_newsroom_handoff_validator.py`.
  Verification readback is
  `docs/verification/NEWSROOM_HANDOFF_VALIDATOR_V1_2026-06-20.md`. The current
  fixture passes structure validation while keeping YMM4 transfer blocked
  because the packet is synthetic-only, has no approved media assets, and
  carries explicit review/readiness blockers. This is not a production ingest
  adapter and does not fetch sources, touch `newsroom-yt-pipeline`, edit
  `.ymmp`, render, approve rights, or change publication state. Next safe
  follow-up is either a deeper G-28 slot-linkage proof using the synthetic
  packet, or a Review Console/readback surface that consumes this validator
  result.
- **Newsroom handoff contract remote publication merge capsule (2026-06-19)**:
  Local commit `468d227 docs: define newsroom handoff contract` was integrated
  with the fetched `origin/master` commits `edbdc45`, `4788648`, and `f456817`
  before publishing `master`. The only merge conflict was this top runtime-state
  capsule area; resolution preserves the newsroom contract capsule, the common
  foundation cockpit remote verification capsule, and the local residue
  quarantine capsule. Validation for this merge path includes
  `uv run pytest tests/test_agent_orchestration.py`, JSON fixture parse /
  reference checks for
  `samples/_probe/newsroom_handoff/minimal_episode_packet.json`, Git diff
  whitespace checks, conflict-marker scans, and forbidden-file scans. After
  syncing another terminal, restart with `AGENTS.md` ->
  `docs/REPO_LOCAL_RULES.md` -> this file, then open the contract, fixture, and
  mapping artifacts named in the next capsule for the newsroom handoff work.
- **Newsroom handoff contract slice completed (2026-06-19)**:
  NLMYTGen-side intake for `newsroom-yt-pipeline` output is now represented by
  `docs/integration/NEWSROOM_TO_NLMYTGEN_HANDOFF_CONTRACT.md`,
  `samples/_probe/newsroom_handoff/minimal_episode_packet.json`, and
  `docs/verification/NEWSROOM_HANDOFF_MAPPING_2026-06-19.md`. The boundary is
  downstream-only: NLMYTGen receives a portable packet / read-only reference and
  maps it to NotebookLM seed context, ScriptIR-like beats, VisualIR concepts,
  G-28 semantic slots, review warnings, and YMM4 readiness gates. RSS / OPML /
  Inoreader, source discovery, topic clustering, source fetching, raw media,
  rights clearance, rendering, `.ymmp` edits, and publication remain out of
  scope. Next safe follow-up is either a lightweight validator for the fixture
  contract or a deeper G-28 slot-linkage proof using the synthetic packet.
- **Common foundation cockpit remote verification sealed (2026-06-18)**:
  Live GitHub access was restored and
  `git ls-remote origin refs/heads/codex/common-foundation-hold-state-audit`
  returned
  `1b1cc8e4f6d0f43dd4662d9efd64887653862b5c`. The feature branch already
  contained the Cockpit Dashboard commit, so no feature-branch push was needed.
  `master` was fetched and was at `HEAD...origin/master=0 0` before this
  handoff-doc update. This confirms that another terminal can fetch
  `origin/codex/common-foundation-hold-state-audit` and inspect
  `docs/dashboard/index.html`, `docs/dashboard/project-status.json`,
  `docs/review/common-foundation-dashboard-2026-06-17.png`,
  `scripts/operator/open_dashboard.ps1`, and
  `docs/_templates/operation-cockpit-report.md`. The dashboard remains a
  review surface only: no real `codex exec`, subprocess runner, stdin piping,
  runtime loop, external notification, `.agent/reports`, `.agent/logs`,
  `.agent/needs_human.json`, G-28, G-27, GUI, YMM4, render, rights,
  production, publishing, ClipPipeGen, Newsroom, RSS, OPML, Inoreader,
  NotebookLM, or `.ymmp` work was opened. Next restart is still
  `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file; use the feature
  branch only when reviewing the common-foundation cockpit, otherwise stay on
  `master`.
- **Local residue quarantine / remote handoff refreshed (2026-06-18)**:
  After `edbdc45 fix: clarify pre-execution preview packet` was pushed,
  `master` is at `HEAD...origin/master=0 0` and the tracked working tree is
  clean. Local-only residue is quarantined in `.git/info/exclude`, not in
  repo history: `.claude/worktrees/`, `.codex/hooks.json`, `.codex/hooks/`,
  `docs/verification/COMMON-FOUNDATION-REVIEW-INDEX-2026-06-15.md`, and
  `samples/2026-05-16.ymmp`. Classification: `.claude/worktrees/` is a local
  agent worktree area; `.codex/hooks*` is a local Codex hook mirror of tracked
  `.claude/hooks`; the common-foundation review index is stale against
  `origin/codex/common-foundation-hold-state-audit` at `1b1cc8e` and should be
  refreshed or discarded only in a later explicit docs slice; `samples/2026-05-16.ymmp`
  has only three YMM4 item-like entries and external absolute paths, so it is
  not a production carrier. No untracked file was deleted, no stash was applied
  or dropped, and no `.ymmp`, render, media, TTS, publishing, rights,
  external-asset, DB/auth/API, or real-runner work was opened. Next restart:
  `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file, then choose a
  separate lane before touching any quarantined residue.
- **Remote-sync handoff capsule prepared (2026-06-17)**:
  The context needed to resume from another terminal is now preserved in tracked
  repository docs for the remote sync of `master`: the G-28 object catalog,
  Freeform Review / Long-Run Autonomy rules, docs cockpit cleanup, lane
  registry / lane-alignment prompts, local MkDocs browser, and this handoff
  note. After pulling the pushed `master`, the next terminal should read
  `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, and this file first, then use
  `docs/project-context.md`, `docs/LANE_REGISTRY.md`, and the G-28 verification
  docs only as needed. No stash apply is required for resume; `stash@{0}`
  remains a local duplicate of residue that was applied into tracked files and
  was intentionally not dropped. This sync does not open `.ymmp`, render,
  media, TTS, publishing, rights approval, external asset intake, DB/auth/API
  contracts, or a real runner path.
- **Prior capsule after G-28 rebase / stash-residue apply (2026-06-17)**:
  At that checkpoint, checkout was `master` at
  `55da8ae docs(g28): expand reference layout object catalog`, with
  `HEAD...origin/master=1 0` after integrating upstream common-foundation
  status docs (`4746d81`, `2495584`) and rebasing the G-28 object catalog
  commit. The active layers are both present: common foundation owns the
  repo-status/status-input audit design, and G-28 owns the current visual
  review artifact layer. The worktree was intentionally not clean while stash
  residue is being classified: docs cockpit cleanup and MkDocs/nav local
  browsing files remain separate from the committed G-28 artifact. `stash@{0}`
  remains `g28-post-commit-residue-20260617-154920` and must not be dropped
  until residue classification is complete. No push had been run at that
  checkpoint.
- **Freeform Review / Long-Run Autonomy operation update consumed (2026-06-17)**:
  User freeform review text is now treated as the source of truth for review
  intake. Fixed labels such as `accept`, `reject`, `revise_once`, or
  `hold` are internal normalization targets only; the user should not be asked
  to re-answer with a fixed phrase. When review is needed, the agent should
  place a Review Card near the artifact or immediately after Artifacts, with
  target, at most three things to inspect, explicit freeform acceptance,
  examples, interpretation method, and completion signal. The agent parses
  freeform review into target / intent / constraints / confidence; medium or
  high confidence proceeds into the next reversible 1-3 agent-side actions
  before reporting, while low confidence gets a Review Clarification Card only
  once if a wrong interpretation would materially change the artifact.
- **Common foundation pre-execution human review packet tightened (2026-06-15)**:
  `scripts/agent_orchestrator.py --pre-execution-dry-run` now makes the
  operator preview packet slightly more explicit for human review: it states
  that preview output is stdout only, says no real execution happened because
  the flow stops after rendering the preview, and repeats that no `.agent`
  report, log, or needs-human artifact is written. The active review command is
  `uv run python scripts/agent_orchestrator.py --worker audit --pre-execution-dry-run --timestamp human-review-packet --repo-status-clean`.
  The packet remains preview-only: it does not start `codex exec`, add or run a
  real subprocess runner, pipe stdin, create a runtime worker loop, send
  external notification, create `.agent/reports`, `.agent/logs`, or
  `.agent/needs_human.json`, evaluate a real worker report, or grant execution
  authority from `safe_to_start_real_runner`. Focused coverage in
  `tests/test_agent_orchestration.py` asserts the stdout-only/no-artifact
  readback. Next safe action is human review of the stdout packet, hold, or a
  separately authorized runner consumption design.
- **Common foundation repo-status input audit design recorded (2026-06-15)**:
  `docs/verification/COMMON-FOUNDATION-STATUS-INPUT-AUDIT-DESIGN-2026-06-15.md`
  refines the prior live status producer contract with the exact audit-facing
  status object fields that preflight, gate, and operator surfaces should read:
  branch, head commit, upstream, remote parity, tracked-only porcelain status,
  full porcelain status, known-untracked allowlist match, dirty state, staged
  diff, unstaged tracked diff, runtime artifact state, needs-human state,
  checked authority docs, execution policy snapshot, repo adapter id,
  fail-closed reasons, observed timestamp, source provenance, command
  provenance, and observer mode. The status object remains observed input only:
  it cannot grant runner permission, cannot set real-runner authority, and does
  not start `codex exec`, add `subprocess.run`, pipe stdin, create a runtime
  loop, send notification, or write `.agent/reports`, `.agent/logs`, or
  `.agent/needs_human.json`. The live pre-edit audit found `master`,
  upstream parity `0 0`, tracked/staged diffs empty, known untracked residue
  limited to `.claude/worktrees/` and `samples/2026-05-16.ymmp`, reports/logs
  containing only `.gitkeep`, and no needs-human state. The old assumption that
  HEAD was `66be70d` is stale; current evidence before this docs edit was
  `4746d81 docs: design live repo status producer`. Next safe action is Hold,
  or a separately authorized stdout-only producer implementation that proves it
  creates no runtime artifacts and still cannot grant real-runner permission.
- **Common foundation live repo status JSON producer design recorded (2026-06-13)**:
  `docs/verification/LIVE-REPO-STATUS-JSON-PRODUCER-DESIGN-2026-06-13.md`
  defines the docs-only contract for replacing a bare human
  `--repo-status-clean` assertion with future machine-collected live repo status
  JSON. The contract covers repo root, branch, HEAD, upstream parity,
  tracked/staged/untracked state, adapter allowlist matching, runtime artifact
  state, `.agent/needs_human.json` presence, inspected paths, command
  provenance, timestamp, source provenance, adapter id, confidence/trust
  boundary, and fail-closed status. The producer is only an observer/serializer
  and cannot grant execution permission, cannot set
  `safe_to_start_real_runner=true`, cannot start real `codex exec`, cannot add
  `subprocess.run`, cannot pipe stdin, cannot create a runtime worker loop,
  cannot send external notification, and cannot write `.agent/reports`,
  `.agent/logs`, or `.agent/needs_human.json`. Unknown, missing, parse-error,
  command-failure, dirty, staged, unknown-untracked, unexpected runtime-artifact,
  or needs-human-present state must surface as `needs_human` or `blocked`, not
  pass. This slice is docs-only and does not touch G-28, G-27, Newsroom,
  ClipPipeGen, RSS / OPML / Inoreader / NotebookLM, `.ymmp`, render, rights,
  production, or publishing. Next safe action is Hold, or a separately
  authorized stdout-only producer implementation that proves it creates no
  runtime artifacts.
- **G-28 reference layout pack object-preset revise-once added (2026-06-12)**:
  The HTML/SVG prototype-first route now includes a content-first expansion
  under `samples/_probe/g28/reference_layout_prototypes/`: `object_catalog`,
  `image_annotation_simple`, `screenshot_callout`, `two_image_compare`,
  `article_quote_card`, `asset_plus_caption`, and
  `source_footage_annotated`. The verification owner is
  `docs/verification/G28-LAYOUT-PRESET-OBJECT-CATALOG-2026-06-11.md`.
  `index.html` links the object catalog and the new content-first pages by
  local file navigation. The added object presets are `image_slot`,
  `screenshot_slot`, `footage_slot`, `highlight_box`, `arrow`, `leader_line`,
  `label_chip`, `callout_box`, `lower_third_telop`, `source_note`,
  `quote_card`, `comparison_panel`, `table_row`, `host_placeholder`, and
  `caption_reserve`. The purpose is to make the pack readable as reusable
  layout / object / content slots, not only static screen mocks. The new pages
  are self-contained HTML/CSS/SVG, use explicit theme tokens, keep fixed
  `1920x1080` canvases and visible subtitle reserve, and contain no external
  images, URLs, real screenshots, map / satellite / company / character /
  footage assets, audio, or TTS. `mechanism_diagram` remains
  `causal_diagram_grammar_debt` and was not modified in this slice. No YMM4
  `.ymmp`, YMM4 builder, existing game-mechanics carrier, existing map-evidence
  carrier, generated YMM4 artifact, render, production / rights / creative
  acceptance, Newsroom, common foundation, G-27, ClipPipeGen, RSS / OPML /
  Inoreader / NotebookLM, or real runner path was opened. Next safe human
  review entry is `index.html`; open `object_catalog.html` next if the digest
  is not enough to judge the preset system. Human feedback can be freeform; the
  agent normalizes it internally to options such as `accept_with_caveats`,
  `revise_once`, `reject`, or `hold` only when useful.
- **G-28 chat-first visual review protocol recorded (2026-06-12)**:
  Human review of the reference layout prototype pack keeps the HTML/SVG
  visual-authoring-first route useful, but changes future review operations:
  every G-28 visual artifact report now needs a chat-readable digest before
  asking the human to open HTML, YMM4, or screenshot evidence. The protocol
  owner is
  `docs/verification/G28-CHAT-FIRST-VISUAL-REVIEW-PROTOCOL-2026-06-11.md`.
  Future reports must include artifact id, visible summary, primary focus,
  layout grammar, object slots, fulfilled specs, known weak points,
  open-file trigger, accumulated review tags, and next decision options.
  Review levels are Level 1 chat-first digest, Level 2 optional visual check,
  and Level 3 accumulated rich review after multiple artifacts accumulate.
  `mechanism_diagram` is now recorded as `causal_diagram_grammar_debt`: it is
  reviewable as a prototype, but should be treated as a must-fix blocker before
  YMM4 transfer planning because arrows, boxes, and causal payload are not yet
  semantically coupled enough. This slice is docs-only: no HTML prototype
  mutation, no `.ymmp`, no YMM4 builder, no existing carrier edit, no render,
  no production / rights / creative acceptance, no Newsroom, no common
  foundation, no G-27, no ClipPipeGen, no RSS / OPML / Inoreader / NotebookLM,
  and no real runner work. Next safe action is to use the digest protocol for
  the next G-28 visual artifact report, or later open accumulated rich review
  by tags such as `causal_diagram_grammar_debt`, `layout_system_debt`,
  `density_debt`, `content_slot_gap`, `subtitle_reserve_risk`, and
  `transfer_candidate`.
- **G-28 reference layout prototype path / checkout audit sealed (2026-06-12)**:
  The current working checkout is `C:\Users\PLANNER007\NLMYTGen` on `master`
  at `c6f17b5 feat: add G-28 reference layout prototypes`, with
  `HEAD...@{u}=0 0` after `git fetch --prune origin` and
  `git pull --ff-only origin master`. The reference layout prototype pack is
  present in both the Git tree and working tree under the correct path
  `samples/_probe/g28/reference_layout_prototypes/`; `samples_probe` is not
  present. The correct local review hub is
  `C:\Users\PLANNER007\NLMYTGen\samples\_probe\g28\reference_layout_prototypes\index.html`.
  The old candidate checkout path
  `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen` was not present in
  this environment, so the missing-folder report was a checkout / path sync
  issue rather than an artifact absence after the fast-forward. Existing proof
  images remain prior pipeline / storyboard / GUI proof, not the
  `reference_layout_prototypes` pack itself. This context-seal is docs-only:
  no prototype regeneration, no HTML edits, no `.ymmp`, no YMM4 builder, no
  render, no production / rights / creative acceptance, no Newsroom, no common
  foundation, no G-27, no ClipPipeGen, no RSS / OPML / Inoreader /
  NotebookLM, and no real runner work. Next safe action is human browser
  review of the HTML pack from the path above.
- **G-28 reference layout prototype pack created (2026-06-11)**:
  The visual authoring route now has a static HTML/SVG prototype-first packet
  at `samples/_probe/g28/reference_layout_prototypes/index.html` with seven
  fixed 1920x1080 review screens: `lecture_list`, `mechanism_diagram`,
  `map_evidence`, `cluster_map`, `evidence_table`, `conversation_board`, and
  `source_footage_frame`. The verification owner is
  `docs/verification/G28-REFERENCE-LAYOUT-PROTOTYPE-PACK-2026-06-11.md`.
  This pack abstracts layout grammar only from the previously supplied
  ゆっくり解説系 references; it does not copy reference images, logos,
  characters, maps, satellite imagery, company materials, or source footage.
  Each prototype is self-contained HTML/CSS/SVG, marks grid / center / margins
  / density intention, and shows subtitle reserve. This is a prototype review
  surface before any YMM4 transfer: no `.ymmp`, no YMM4 builder, no existing
  carrier rewrite/regeneration, no render, no production candidate, no rights
  approval, no creative final acceptance, no Newsroom, no common foundation,
  no G-27, no ClipPipeGen, no RSS / OPML / Inoreader / NotebookLM, and no real
  runner path was opened. Next safe action is human browser review of the HTML
  pack and freeform review that the agent can internally normalize to
  `accept`, `accept_with_caveats`, `revise_once`, `reject`, or
  `redesign_required` when useful.
- **G-28 YMM4 coordinate-generation method blocker recorded (2026-06-11)**:
  Human YMM4 review of
  `samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe.ymmp`
  classifies the Map / Evidence carrier as
  `redesign_required_generation_method_blocker`. The carrier is not accepted
  as a diagnostic candidate and should not receive `revise_once`. The dominant
  finding is stronger than the earlier game-mechanics `layout_system_debt`:
  direct coordinate-generated `.ymmp` visual construction produces weak review
  surfaces even when structural readback passes. The current file, builder,
  readback, and report remain tracked as negative evidence / failed sample, but
  they must not be regenerated or micro-tuned. Treat readback pass as a
  boundary / structure check only, not a visual-quality guarantee. Stop using
  the same script-coordinate method as the visual authoring source for new G-28
  YMM4 carriers. Safe next entries are a human-authored YMM4 seed carrier, an
  HTML/SVG visual prototype approved before YMM4 transfer, or a later bounded
  cross-screen layout-normalization review. Speed-first remains valid only when
  it creates useful review surfaces; producing more low-quality artifacts by
  this method is debt, not velocity. Record:
  `docs/verification/G28-YMMP-CARRIER-GENERATION-METHOD-BLOCKER-2026-06-11.md`.
- **G-28 Map / Evidence YMM4 diagnostic carrier candidate created (2026-06-11)**:
  After classifying the game-mechanics YMM4 carrier as `layout_system_debt`,
  same-screen tuning remains stopped. The speed-first next reviewable artifact
  is now the Map / Evidence YMM4 diagnostic carrier candidate at
  `samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe.ymmp`.
  `scripts/build_g28_map_evidence_ymmp_probe.js --write` converts the existing
  passed Map / Evidence skeleton into a ShapeItem/TextItem-only `.ymmp`, plus
  readback JSON and report. Readback classifies the result as
  `pass_map_evidence_ymmp_diagnostic_carrier_created` with
  `diagnostic_only=true`, `production_candidate=false`, caption reserve clear,
  evidence area in main canvas, three annotation slots, bounded source note,
  non-focal hosts, external image / URL / source-footage / audio / TTS counts
  zero, `render_output=false`, production / creative / rights approvals false,
  and no failures. Verification record:
  `docs/verification/G28-MAP-EVIDENCE-YMMP-DIAGNOSTIC-CARRIER-PROBE-2026-06-11.md`.
  This did not modify the game-mechanics carrier, production state, render,
  rights, creative final acceptance, Newsroom, common foundation, G-27,
  ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, real runner / `codex exec`,
  GUI, or `src`. Next safe action is human YMM4 review intake for the new Map /
  Evidence carrier path.
- **G-28 game mechanics batch review classified as layout-system debt (2026-06-11)**:
  Human review of the current
  `game_mechanics_explanation` YMM4 diagnostic carrier is recorded as
  `layout_system_debt`. The screen remains reviewable as a diagnostic artifact,
  but the dominant issue is no longer single-label fitting. The concern is the
  layout system itself: element centering, spacing regularity, and split-layout
  generalizability. Do not continue same-screen micro-tuning for this carrier.
  Proceed speed-first by producing more reviewable artifacts, then revisit this
  as a bounded cross-screen batch review or layout-normalization slice. Safe
  entries are Advance to another G-28 artifact / reviewable screen, Audit later
  for cross-screen layout normalization, or Hold this screen as known
  `layout_system_debt`. This slice is docs-only and does not modify `.ymmp`,
  builder, samples, production candidate state, render, rights, creative final
  acceptance, Newsroom, common foundation, G-27, ClipPipeGen, RSS, OPML,
  Inoreader, NotebookLM, real runner / `codex exec`, GUI, or `src`.
- **G-28 game mechanics batch visual review packet added (2026-06-11)**:
  The next human YMM4 review for
  `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp`
  is no longer a two-point label recheck. It now uses
  `docs/verification/G28-GAME-MECHANICS-YMMP-BATCH-VISUAL-REVIEW-PACKET-2026-06-11.md`
  as the review protocol. The one-pass targeted layout fix in `27b4736` remains
  accepted as the current known state (`画面上の結果` at font size 38 with the
  inherited rightward nudge removed, lower callouts centered with font size 28,
  readback `classification=pass_game_mechanics_ymmp_label_layout_fixed`,
  `one_pass_targeted_fix=true`, and
  `no_further_micro_tuning_recommended=true`), but those labels are now only
  part of a full-screen batch checklist. Human review should return
  `accept`, `accept_with_caveats`, `revise_once`, `layout_system_debt`, or
  `redesign_required`, with `must_fix` items as the only driver for one
  consolidated follow-up fix. This slice is docs-only and does not modify
  `.ymmp`, the builder, samples, render, production, rights, creative final
  acceptance, Newsroom, common foundation, real-estate work, G-27, GUI,
  ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, `.claude/worktrees/`,
  `samples/2026-05-16.ymmp`, or any real runner / `codex exec` path.
- **G-28 game mechanics one-pass label layout fix applied (2026-06-11)**:
  Human YMM4 visual review accepted the diagnostic carrier structure but found
  two label-placement issues: `画面上の結果` was cramped in the right focal
  node, and the lower `判定 / 当たり判定` / `リスクとリターン` callouts looked
  left-aligned. The fix is intentionally one-pass only in
  `scripts/build_g28_game_mechanics_ymmp_probe.js`: the right focal label keeps
  the same text and node geometry while its inherited rightward nudge is removed
  and its font size is reduced to 38; all callout labels use the same centered
  rule at font size 28. Regenerated artifacts are
  `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp`,
  its readback JSON, and its report. Readback now records
  `classification=pass_game_mechanics_ymmp_label_layout_fixed`,
  `one_pass_targeted_fix=true`, `no_further_micro_tuning_recommended=true`,
  `right_focal_label_fit_status.status=fits_after_one_pass_targeted_fix`,
  `callout_label_alignment_status.status=common_centering_rule_applied`, and
  `label_overflow_check.passed=true`. Boundary remains `diagnostic_only=true` /
  `production_candidate=false`; external image / URL / source-footage / audio /
  TTS counts remain zero, and render, rights, production approval, creative
  final acceptance, Newsroom, real-estate, G-27, ClipPipeGen, RSS, NotebookLM,
  and common-foundation work remain closed. Do not continue same-screen
  micro-tuning. A later batch visual review packet supersedes the old two-check
  loop and asks the human to judge the whole preview surface at once; only
  `must_fix` items can drive one consolidated follow-up fix.
- **G-28 game mechanics YMM4 diagnostic carrier candidate created (2026-06-10)**:
  `scripts/build_g28_game_mechanics_ymmp_probe.js --write` now creates a
  self-contained ShapeItem/TextItem-only diagnostic carrier candidate at
  `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp`
  plus readback JSON and a human-readable report. The readback passed with
  `diagnostic_only=true`, `production_candidate=false`,
  `carrier_kind=lecture_diagram_carrier`, `variant=game_mechanics_explanation`,
  focal chain `入力操作` -> `内部ルール / 判定` -> `画面上の結果`, callouts
  `操作感` / `判定 / 当たり判定` / `リスクとリターン`, bottom caption reserve
  clear, non-focal hosts, external image / URL / source-footage / audio / TTS
  counts all zero, `render_output=false`, and `production_approval=false`.
  Verification record:
  `docs/verification/G28-GAME-MECHANICS-YMMP-DIAGNOSTIC-CARRIER-PROBE-2026-06-10.md`.
  This is the next reviewable YMM4 diagnostic candidate only; it is not render,
  production carrier approval, rights approval, creative final acceptance,
  source-footage intake, gameplay screenshot intake, Newsroom intake, G-27
  revival, real-estate reopening, or common-foundation progress. The next safe
  action is human YMM4 review intake: open the carrier path, return preview and
  timeline screenshots, item/layer confirmation, bottom caption safe-area
  evidence, and `accept` / `revise` / `reject`.
- **Common foundation dry-run preview wording accepted for Hold (2026-06-10)**:
  The refined pre-execution dry-run preview has been checked as holdable after
  `8006349 fix: clarify dry-run preview wording`. The hold check used
  `uv run python scripts/agent_orchestrator.py --worker audit --pre-execution-dry-run --timestamp hold-check --repo-status-clean`
  and confirmed the stdout labels are self-contained: repo status is an
  operator-provided assertion not checked by the CLI, the report path is planned
  only and not written, the outer preview and embedded raw preflight card have
  distinct roles, and preflight allowed / `safe_to_start_real_runner` remain
  review / eligibility signals rather than execution permission. The preview
  still writes no `.agent/reports`, `.agent/logs`, or `.agent/needs_human.json`
  runtime artifacts and does not open real `codex exec`, `subprocess.run`,
  stdin piping, a runtime worker loop, external notification, worker report
  validation from a real run, GUI, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML,
  Inoreader, NotebookLM, `.ymmp`, render, rights, production, publishing, or
  release automation. Default next action is Hold. Safe future entries are a
  repo-status input audit, a wording/readback correction if new drift is found,
  or a separate docs-only real-runner consumption design after explicit human
  authorization.
- **Common foundation dry-run preview stdout wording refined (2026-06-10)**:
  The pre-execution dry-run preview still stops at stdout, but its labels now
  reduce four review-time misreads. The repo status section says the status is
  an operator-provided assertion after external git checks and was not checked
  by this CLI. The selected-plan section says the report path is planned only
  and is not written by the preview. The outer review surface is labeled as a
  plan-level preview, while the embedded raw preflight card is labeled as the
  raw preflight result. Preflight allowed / real-runner eligibility wording now
  says review-only / eligibility-only, not execution permission. Redaction of
  credential-like display values remains in place. No real `codex exec`,
  `subprocess.run`, stdin piping, runtime worker loop, external notification,
  worker report validation from a real run, `.agent` runtime artifact creation,
  GUI, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM,
  `.ymmp`, render, rights, production, publishing, or release automation was
  opened. Next safe action is human acceptance of the refined preview surface
  or a separate repo-status input audit.
- **Common foundation preview-surface / repo-status audit tightened redaction (2026-06-10)**:
  `pre_execution_dry_run_preview_surface_and_repo_status_audit_001` found that
  the preview-only surface was readable and stopped at stdout, but the outer
  Markdown renderer needed the same credential-like display hardening as the raw
  preflight card for operator-supplied values such as `--timestamp` and
  `--repo-status-json` paths. `scripts/agent_orchestrator.py` now redacts
  credential-like strings in the outer preview plan, argv, repo-status summary,
  reasons, inspected paths, and raw identifiers before printing. A regression
  test covers token-like timestamp / untracked status display. No real
  `codex exec`, `subprocess.run`, stdin piping, runtime worker loop, external
  notification, worker report validation from a real run, `.agent` runtime
  artifact creation, GUI, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML,
  Inoreader, NotebookLM, `.ymmp`, render, rights, production, publishing, or
  release automation was opened. A later stdout wording pass makes the
  operator-provided repo status source explicit inside the preview itself.
- **Common foundation pre-execution dry-run preview-only MVP implemented (2026-06-10)**:
  `scripts/agent_orchestrator.py --pre-execution-dry-run` now prints a
  human-readable Markdown preview that composes the existing execution plan,
  `build_execution_preflight(..., mode="dry_run_preview")`, and
  `render_preflight_preview_card`. The preview shows selected worker, prompt
  source, schema path, planned report path, working directory, timeout,
  shell-free argv preview, repo status summary, authority summary, preflight
  allow/block state, reasons, inspected paths, raw preflight preview card, human
  next action, and explicit execution boundary. It stops at stdout: no real
  `codex exec`, no `subprocess.run`, no stdin piping, no runtime worker loop, no
  external notification, no worker report validation from a real run, and no
  `.agent/reports`, `.agent/logs`, or `.agent/needs_human.json` runtime artifact
  creation. `--repo-status-clean` is an operator-provided clean assertion after
  external git checks; the CLI itself does not spawn Git. Tests cover allowed
  preview output, blocked repo-status reasons, CLI Markdown output, existing
  dry-run compatibility, and the no-real-execution sentinel. Next safe action is
  human review of the preview surface or a narrow audit of the operator-provided
  repo-status input shape, not real runner implementation.
- **Common foundation pre-execution dry-run flow designed (2026-06-10)**:
  `docs/verification/PRE-EXECUTION-DRY-RUN-FLOW-DESIGN-2026-06-10.md`
  defines the next safe common-foundation step after the parked preflight /
  operator-surface state. The design is human-review-first: it shows selected
  worker, prompt source, schema, planned report path, shell-free command argv,
  `build_execution_preflight` result, raw preflight preview card, inspected
  files, stop reasons, and human decision options before any runner exists or
  starts. `safe_to_start_real_runner=true` remains labeled as preflight
  eligibility only, not execution permission. This slice is docs-only and does
  not implement real `codex exec`, `subprocess.run`, stdin piping, runtime
  worker loop, external notification, `.agent` runtime artifact creation,
  Python/test changes, GUI, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML,
  Inoreader, NotebookLM, `.ymmp`, render, rights, production, publishing, or
  release automation. Next safe action is human review of the design; only
  after explicit authorization should a preview-only dry-run implementation
  slice be considered.
- **Remote handoff sealed for parked common foundation (2026-06-09)**:
  The reusable restart prompt for this exact parked state is recorded in
  `docs/USER_COPYPASTE_BLOCKS.md` SECTION 22. Use it only when the next operator
  explicitly resumes common foundation handoff / parking context from another
  terminal. The parked state remains docs-only: no real runner, subprocess,
  stdin piping, runtime worker loop, external notification, or `.agent` runtime
  artifact path is opened by this handoff.
- **Common foundation preflight / operator surface parked after human review (2026-06-09)**:
  Human review accepts the standalone preflight preview card from
  `cde00ca feat: add preflight preview card` as sufficient for the current
  review surface. The common foundation now has two read-only Operator Review
  Surface faces: a flow-result card for existing orchestration flow JSON and a
  raw preflight preview card for `build_execution_preflight` results. Preflight
  results are readable without starting a runner, and the preview card exposes
  preflight status, `safe_to_start_real_runner`, reasons, inspected paths,
  authority summary, execution boundary, and human next action. This parks the
  common foundation at usable preflight / review-surface coverage, not real
  execution. `safe_to_start_real_runner=true` remains only preflight start
  eligibility for a separately authorized future runner slice; it is not itself
  execution permission. Real `codex exec`, `subprocess.run`, stdin piping,
  runtime worker loop, external notification, and `.agent` runtime artifact
  creation remain unimplemented. Next common-foundation work, only if explicitly
  resumed, should be a separately authorized runner consumption design or
  pre-execution dry-run flow, not immediate real runner implementation. No G-28,
  Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, `.ymmp`,
  render, rights, production, publishing, or release automation work changed.
- **Common foundation standalone preflight preview adapter MVP implemented (2026-06-09)**:
  `scripts/agent_operator_surface.py` now has
  `render_preflight_preview_card(preflight_result)` plus
  `--preflight-example` for a deterministic Markdown preview of a raw preflight
  result. The card shows preflight status, mode / worker, allowed,
  `safe_to_start_real_runner`, reasons, inspected paths, authority summary,
  execution boundary, and human next action. It redacts obvious credential-like
  raw values if they appear in display fields. Existing flow-result operator
  cards remain intact. This is a read-only adapter: it does not run Codex, start
  the fake runner, validate a worker report, create `.agent` runtime artifacts,
  pipe stdin, start a runtime worker loop, or send external notifications. A
  preview with `safe_to_start_real_runner=true` is still only reviewable
  preflight output; real execution remains a separate authorized future slice.
  No G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM,
  `.ymmp`, render, rights, production, publishing, or release automation work
  changed.
- **Common foundation disabled real runner preflight audit tightened (2026-06-09)**:
  The implemented preflight was audited as the current common-foundation
  boundary before any real runner slice. A narrow regression test now confirms
  that supplied credential-like metadata blocks preflight without echoing the
  secret value into the result. `docs/AGENT_ORCHESTRATION.md` now clarifies that
  the Operator Review Surface can consume preflight data when it is embedded in
  a complete flow result, but a standalone dry-run / real-runner preflight
  preview still needs a future adapter that wraps raw preflight with
  `runner_started=false`, gate placeholders, `safe_to_start_real_runner`, and
  `authority_summary`. This audit did not implement real `codex exec`,
  `subprocess.run`, stdin piping, a runtime worker loop, external notification,
  `.agent` runtime artifact creation, G-28, Newsroom, G-27, ClipPipeGen, RSS,
  OPML, Inoreader, NotebookLM, `.ymmp`, render, rights, production, publishing,
  or release automation. Next common-foundation move is review of this audited
  preflight boundary, not real runner implementation.
- **Common foundation disabled-by-default real runner preflight implemented test-first (2026-06-09)**:
  `scripts/agent_orchestrator.py` now returns a structured preflight result for
  `real_runner`, `dry_run_preview`, and `fake_runner_helper` modes before any
  runner can start. The result includes `allowed`, `mode`, `worker`, `reasons`,
  `safe_to_start_real_runner`, `codex_execution_started=false`,
  `real_subprocess_started=false`, `report_path`, `inspected_paths`, and an
  `authority_summary`. Future real runner mode is fail-closed unless execution
  policy is enabled, explicit human real-execution authority is present, repo
  status is clean or allowlisted, timeout and paths are valid, command argv is
  shell-free, prompt source is unambiguous, and notification policy is clear.
  Dry-run preview and fake runner helper flow can be allowed while still keeping
  `safe_to_start_real_runner=false`. Tests in `tests/test_agent_orchestration.py`
  now cover missing authority, disabled policy, dirty/staged state,
  repo-external/traversal/overwrite paths, shell command string shape, missing
  timeout, invalid worker, missing schema, prompt ambiguity, notification
  ambiguity, dry-run allow, fake-helper allow, and authorized future real-runner
  allow. Real `codex exec`, `subprocess.run`, stdin piping, runtime worker loop,
  external notification, `.agent` runtime artifact creation, G-28, Newsroom,
  G-27, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, `.ymmp`, render, rights,
  production, publishing, and release automation remain unimplemented and
  untouched. Next common-foundation move is review of the preflight
  implementation result before any separate real runner slice.
- **Common foundation disabled-by-default real runner preflight implementation plan added (2026-06-09)**:
  `docs/verification/REAL-RUNNER-PREFLIGHT-IMPLEMENTATION-PLAN-2026-06-09.md`
  now records the docs-only implementation plan for a future real runner
  preflight after human acceptance of the boundary design. The plan defines the
  future preflight inputs, fail-closed refusal cases, narrow allow cases,
  structured result shape, operator-card mapping, implementation sequence,
  future tests, and stop conditions. This does not implement real `codex exec`,
  `subprocess.run`, stdin piping, a runtime worker loop, external notification,
  or `.agent` runtime artifact creation. No scripts, tests, `.agent`, GUI,
  source, samples, `.ymmp`, render, rights, production, publishing, G-28,
  Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader, or NotebookLM work changed.
  Next common-foundation move is review of this preflight plan; only after
  acceptance should a separate disabled-by-default implementation slice edit
  code/tests.
- **Common foundation real runner boundary design added (2026-06-09)**:
  `docs/verification/REAL-RUNNER-BOUNDARY-DESIGN-2026-06-09.md` now defines the
  pre-implementation boundary for a future real runner. This is docs-only
  `real_runner_boundary_design_001`: it records the sealed fake runner, single
  fake flow, and Operator Review Surface MVP state, then fixes the future
  opt-in authority, subprocess, stdin, timeout/cancellation, report containment,
  gate/notify sequence, operator-card integration, runtime artifact hygiene,
  implementation checklist, and stop conditions. No implementation files,
  tests, `.agent` runtime artifacts, `.ymmp`, render, production, rights,
  publishing, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader, or
  NotebookLM work changed. Next common-foundation move is review of the boundary
  design; only after acceptance should a separate disabled-by-default real
  runner implementation plan be considered.
- **Common foundation Operator Review Surface MVP implemented (2026-06-09)**:
  `scripts/agent_operator_surface.py` now renders an existing repo-local
  orchestration flow JSON into a Markdown operator card, and `docs/AGENT_OPERATOR_SURFACE.md`
  records the deterministic example and human-readable contract. The card makes
  the single-fake flow understandable without reading Python or pytest output:
  attempted flow, worker/scenario, preflight result, runner start/report status,
  gate decision, human action, inspectable files, safety boundary, next safe
  action, and raw identifiers. This remains read-only review surface work, not
  real runner implementation: it does not run Codex, expose the single fake flow
  through the default CLI, start a real process, pipe stdin, create a runtime
  worker loop, or send external notifications. Narrow verification passed with
  `uv run pytest tests/test_agent_orchestration.py`, `uv run pytest
  tests/test_guardrails.py`, `uv run python -m py_compile scripts/agent_gate.py
  scripts/agent_notify_stub.py scripts/agent_orchestrator.py
  scripts/agent_operator_surface.py`, and `uv run python
  scripts/agent_operator_surface.py --example`. Next common-foundation move is
  human review/stage of the operator card; only after that should a separate
  `real_runner_boundary_design_001` slice be considered.
- **Newsroom handoff supervision gate refreshed for remote handoff (2026-06-09)**: The latest cross-repo supervision gate is preserved in `docs/verification/NEWSROOM-HANDOFF-SUPERVISION-GATE-2026-06-09.md`. Local NLMYTGen was synced on `master` at `39dd9ad docs: seal single fake flow handoff` before this docs-only handoff, with upstream parity `HEAD...@{u}=0 0` and only known untracked residue `.claude/worktrees/` plus `samples/2026-05-16.ymmp`. Newsroom was checked read-only at `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline`, `main` / `1296b8e`, `HEAD...origin/main=0 0`, and export `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853` was visible with manifest, script, visual, source, quote, asset, and YMM4 note files. Decision remains `request_authority / no-op_wait`: the Newsroom handoff is candidate downstream input, not active NLMYTGen authority. Current NLMYTGen active lane remains G-28 `game_mechanics_explanation` diagnostic reviewability / later scoped YMM4-saved carrier review conditions. Do not implement, copy export files, generate `.ymmp`, render, change Review Console, start context visual plugin work, or treat Newsroom export inspect as NLMYTGen production proof from this state. Next safe action, only if the user wants Newsroom downstream intake, is explicit human authority for copy-in versus read-only reference and whether to pause/supersede the G-28 game_mechanics lane. Copy/paste continuation lives in `docs/USER_COPYPASTE_BLOCKS.md` SECTION 21. When returning ChatGPT handoff blocks, wrap the whole report in one outer Markdown code fence, keep `BEGIN_COPY_BLOCK_FOR_CHATGPT` / `END_COPY_BLOCK_FOR_CHATGPT` inside it, and do not use inner code fences.
- **Common foundation single fake execution flow sealed (2026-06-09)**: `post_commit_audit_single_fake_execution_flow_001` passed for `e509863 feat: update orchestration scaffold`, with `master` pushed and `HEAD...@{u}=0 0` at audit time. The committed common foundation now includes the fake runner scaffold and the single fake execution flow helper in `scripts/agent_orchestrator.py`, but that helper remains test/helper-only and is not exposed through the default CLI/runtime path; there is no `--single-fake-flow` flag. Valid fake reports still go through `agent_gate.evaluate_report`; the local notify stub is reached only after `gate_result.needs_human=true`, and pass writes no notify artifact. The fake failure forms `invalid_json`, `missing_report`, `nonzero_exit`, and `timeout` fail closed. `codex_execution_started=false` and `real_subprocess_started=false` remain enforced; real `codex exec`, `subprocess.run`, stdin piping, runtime worker loop, and external notification service remain unimplemented. Retire stale prompts for this slice: `stage_single_fake_execution_flow_001`, `single_fake_execution_flow_staged_diff_review_001`, and any fake runner scaffold stage/commit prompt. Next common-foundation work is not immediate real execution; if explicitly authorized later, use design-only `real_runner_boundary_design_001` covering opt-in execution policy, subprocess/stdin boundaries, timeout/cancellation, report path containment, gate authority, notify boundary, runtime artifact hygiene, and no external notification without separate authorization.
- **Current G-28 game mechanics note (2026-06-08)**: Human review accepted the repaired `game_mechanics_explanation` review surface with `decision: accept` / `carrier: Lecture Diagram Carrier`. The default HTML 16:9 frame is clean, in-frame review label boxes are removed, and semantic labels are human-visible through the lower Review Inspector plus readback/report fields. The accepted scope is review-surface usability only: `production_visible_text_items` and `review_visible_semantic_labels` remain separated, `in_frame_review_overlay=false`, `review_overlay_default=false`, and `clean_frame_available=true`. `docs/verification/G28-GAME-MECHANICS-YMM4-SAVED-CARRIER-REVIEW-CONDITIONS-2026-06-08.md` now defines the conditions for a later scoped YMM4-saved carrier review: explicit human selection, carrier path, preview screenshot, timeline screenshot, item/layer confirmation, and bottom caption safe-area evidence. Boundary remains `diagnostic_only=true` / `production_candidate=false`; no Source-Footage, `.ymmp` generation, render, production timing, or creative final acceptance. Next safe work is to collect those human-supplied YMM4 review inputs, or stay with the accepted HTML/readback diagnostic precedent.
- **G-28 real-estate YMM4 diagnostic review surface accepted; micro-tuning loop stopped (2026-06-08)**: Human GUI confirmation now records `overall_decision=accept_as_diagnostic_review_surface_with_title_metric_caveat` in `docs/verification/G28-REAL-ESTATE-YMMP-PROBE-HUMAN-REVIEW-2026-06-07.md`. Openability, focal chain `元付情報 -> ポータル掲載 -> 借主判断`, yellow connector treatment, `仲介インセンティブ` after the X=313.0 human-calibrated override, caption reserve, host placeholders as diagnostic placeholders, and diagnostic boundary all pass for diagnostic review surface use. Stop further one-off YMM4 probe title-Y / callout / right-node / X-Y pixel tuning; if visual-centering issues remain important, handle them as a separate text/layout system redesign slice. Keep caveats: title position has minor metric debt (`title_anchor` / `title_text_center` / safe-area readback), X=313.0 is a human-calibrated override rather than formula success, host rectangles are not production visual/material, and boundary remains `diagnostic_only=true` / `production_candidate=false`. Real-estate side evidence is closed for now; return to the active runtime-state lane unless a later explicit request opens Review Console human confirmation or diagnostic render planning.
- **G-28 real-estate Review Console evidence captured (2026-06-08)**: Requested side evidence for the earlier `real_estate_information_gap` read-only Review Console panel is recorded in `docs/verification/G28-REAL-ESTATE-REVIEW-CONSOLE-INGEST-EVIDENCE-2026-06-07.md`. Existing Electron DOM smoke passed and confirmed `#g28-review-console-ingest`, five artifact rows, diagnostic badges, readback summary, human GUI summary, caveats, allowed diagnostic decisions, and absence of production approval labels. No GUI implementation, `.ymmp`, builder, readback, report, render, production, rights, G-27 authority, ClipPipeGen, RSS / NotebookLM, or common-foundation work changed. There is still no G-28-specific existing screenshot capture command; manual screenshot or a separately authorized capture slice is the next visual-evidence option. This note does not supersede the current game mechanics lane above.
- **Remote handoff sealed after G-28 game mechanics inspector-first accept (2026-06-08)**: This checkout is prepared for another terminal to resume from `master` after sync. The durable restart path is `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file, then `docs/USER_COPYPASTE_BLOCKS.md` SECTION 20. The active lane remains diagnostic G-28 game mechanics reviewability / later scoped YMM4-saved carrier review conditions only. Do not treat the accepted inspector-first HTML/readback/report as production approval; do not start Source-Footage, `.ymmp` generation, render, production timing, creative final acceptance, G-27 active blocker, RSS / OPML / Inoreader / NotebookLM, common foundation, or ClipPipeGen work from this handoff.

# BLOCK SUMMARY のたびに更新する。

# compact 後の再アンカリングではこのファイルを読む。

## 現在位置

### Session Handoff (2026-04-23)

- **G-28 game mechanics diagnostic reviewability repaired (2026-06-08)**: Human review returned `decision: revise` for the existing `game_mechanics_explanation` Lecture Diagram Carrier artifact, while keeping carrier selection correct and Source-Footage as future-only backup. The existing variant was repaired in place, not replaced: `scripts/build_g28_lecture_diagram_carrier_skeleton.js --variant game_mechanics_explanation` now writes a review-only HTML overlay plus readback/report inspector fields for `入力操作`, `画面上の結果`, `操作感`, `判定 / 当たり判定`, and `リスクとリターン`; readback also exposes `production_visible_text_items`, `review_visible_semantic_labels`, `review_label_layer_or_inspector_exists=true`, and `semantic_labels_human_visible=true`. Boundary remains `diagnostic_only=true` / `production_candidate=false`; no new theme variant, new carrier skeleton, Source-Footage generator, gameplay screenshot/source footage intake, image path/URL/raw reference, `.ymmp`, render, production timing, creative final acceptance, G-27 revival, RSS, NotebookLM, or cross-repo work was performed.
- **Supersession note for the previous G-28 game mechanics repair wording**: The accepted repaired surface is inspector-first, not an in-frame overlay. The current HTML/readback contract is `review_surface=inspector_first`, `in_frame_review_overlay=false`, and `clean_frame_available=true`; semantic labels are human-visible below the 16:9 frame while the frame remains clean.
- **Remote handoff sealed after common foundation fake runner scaffold (2026-06-08)**: Common foundation work now includes `da254ff feat: add fake runner scaffold`, after the G-28 Review Console handoff commit `a6f99b9 docs: seal G-28 Review Console handoff`. The fake runner is a tests-only scaffold in `scripts/agent_orchestrator.py`: it writes synthetic reports to `ExecutionPlan.report_path`, routes valid reports through `agent_gate.evaluate_report`, calls the local notify stub only when `gate_result.needs_human=true`, and fails closed for invalid JSON, missing report, nonzero exit, and timeout. It preserves `codex_execution_started=false` and `real_subprocess_started=false`; real `codex exec`, stdin piping, subprocess runner, runtime worker loop, and external notification service remain unimplemented. `tests/test_agent_orchestration.py` covers pass / needs_human / blocked / invalid JSON / missing report / nonzero exit / timeout and artifact cleanup, while `.agent/reports/` and `.agent/logs/` remain runtime-artifact locations with tracked `.gitkeep` only. Next common-foundation action, only if explicitly resumed, is a design/implementation slice for a real runner boundary; next G-28 action remains screenshot / Electron smoke evidence or human GUI confirmation of the read-only Review Console panel. Known local untracked residue remains out of scope: `.claude/worktrees/` and `samples/2026-05-16.ymmp`.
- **Remote handoff sealed after G-28 Review Console read-only ingest (2026-06-08)**: Latest remote handoff is `708b9e9 feat: add G-28 Review Console read-only panel` plus this docs-only handoff refresh. `docs/USER_COPYPASTE_BLOCKS.md` now includes SECTION 18 with the exact restart prompt for a next terminal: sync `master`, read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file, verify the G-28 Review Console panel, and keep the boundary at screenshot / Electron smoke evidence or human GUI confirmation. Existing local residue remains out of scope and must not be staged as part of the G-28 handoff: `docs/AGENT_ORCHESTRATION.md`, `scripts/agent_orchestrator.py`, `tests/test_agent_orchestration.py`, `.claude/worktrees/`, and `samples/2026-05-16.ymmp`.
- **G-28 real-estate Review Console read-only ingest implemented (2026-06-08)**: Review Console now includes a read-only `G-28 real_estate_information_gap YMM4 diagnostic probe` panel in `gui/index.html` / `gui/renderer.js` / `gui/style.css`. The panel references the existing `.ymmp`, readback JSON, report MD, human review record, and ingest plan in place, checks artifact existence via a repo-relative GUI IPC, displays `diagnostic_only=true`, `production_candidate=false`, `human_calibrated_override=true`, `layout_metric_debt=true`, `host_placeholder=true`, `render=false`, and `rights_public_use=false`, and summarizes readback classification `pass_callout_label_human_calibrated`, caption reserve, focal chain count, callout count, host role, zero external/source/audio/TTS counts, and `actual_x=313`. `gui/review_console_dom_smoke.js` now verifies the G-28 panel, caveats, allowed diagnostic decision schema, and absence of production approval labels. This slice did not regenerate `.ymmp`, change builders, rewrite readback/report artifacts, render, approve production, approve creative final acceptance, run rights automation, slot-fill, ingest external material, revive G-27, use G-27 `review_decisions` authority, access ClipPipeGen, restart RSS / OPML / Inoreader / NotebookLM, or implement common foundation / Codex Worker Orchestration. Next safe action is screenshot / Electron smoke evidence or human GUI confirmation of the read-only panel.
- **G-28 real-estate Review Console ingest plan added (2026-06-08)**: Added `docs/verification/G28-REAL-ESTATE-REVIEW-CONSOLE-INGEST-PLAN-2026-06-07.md` as the docs-only plan for read-only Review Console ingest of the accepted G-28 real-estate YMM4 diagnostic probe. The plan fixes input artifact inventory, required status badges, readback summary fields, human GUI result display, title readback follow-up fields, host placeholder warnings, allowed diagnostic decision schema, future GUI implementation surfaces, error states, and acceptance criteria. This slice does not implement Review Console ingest, change GUI files, regenerate `.ymmp`, change the builder, rewrite readback/report artifacts, render, approve production, approve creative final acceptance, run rights automation, slot-fill, ingest external material, revive G-27, access ClipPipeGen, restart RSS / OPML / Inoreader / NotebookLM, or implement common foundation / Codex Worker Orchestration. Next safe action is an explicitly authorized read-only Review Console ingest implementation slice based on the plan.
- **G-28 real-estate calibrated probe accepted for Review Console ingest candidate planning (2026-06-08)**: Human YMM4 GUI recheck after the X=313.0 calibration accepted `G28_LDC_CalloutSlot_3_Label` / `仲介インセンティブ` for forward movement: openability pass, callout alignment pass, focal chain readable, connector pass, no other callout or right-node side effect, caption reserve pass, diagnostic boundary clear, and `overall_decision=accept_for_review_console_ingest_candidate_with_layout_metric_caveat`. This authorizes only Review Console ingest candidate record / ingest plan preparation, not actual ingest implementation, production render, production carrier approval, creative final acceptance, rights automation, slot-fill, external image/URL/raw reference, source footage/audio/TTS, G-27 revival, ClipPipeGen, RSS / OPML / Inoreader / NotebookLM, or common foundation / Codex Worker Orchestration work. Keep layout metric debt: YMM4 glyph optical center is not directly measured, title y=`-474.5` is visually acceptable but needs future title anchor/text-center/safe-area readback, host placeholders are diagnostic-only, and X=313 remains a human-calibrated override rather than reusable formula proof. Next safe action is a docs/design-only Review Console ingest plan for this diagnostic probe.
- **G-28 real-estate lower-right callout human calibration applied (2026-06-08)**: Human GUI recheck after `g28_real_estate_information_gap_callout_label_alignment_v1` still saw the lower-right callout label `仲介インセンティブ` as left-shifted; the human-measured correct YMM4 TextItem X is `313.0`. `scripts/build_g28_real_estate_ymmp_probe.js --write` now records `g28_real_estate_information_gap_callout_label_human_calibration_v1`, preserves the previous computed/polished X `289`, applies a one-time `human_calibrated_x=313`, records `calibration_delta_x=24`, and classifies the readback as `pass_callout_label_human_calibrated`. This is explicitly layout system debt, not proof that the callout text formula is reusable. The boundary remains `diagnostic_only=true` / `production_candidate=false`: no Review Console ingest, production render, production carrier approval, creative final acceptance, rights automation, slot-fill, external image/URL/raw reference, source footage/audio/TTS, G-27 revival, ClipPipeGen, RSS / OPML / Inoreader / NotebookLM, or common foundation / Codex Worker Orchestration work. If this still reads off in YMM4, stop individual pixel/offset tuning and move to callout text layout system redesign.
- **G-28 real-estate lower-right callout label alignment fixed (2026-06-07)**: Human GUI correction after the right-node alignment fix clarified that the actual remaining target was the lower-right callout label `仲介インセンティブ`, not the right node `借主判断`. The previous right-node offset is retained because no adverse side effect was reported. `scripts/build_g28_real_estate_ymmp_probe.js --write` now applies `g28_real_estate_information_gap_callout_label_alignment_v1` by changing only `G28_LDC_CalloutSlot_3_Label` registered optical offset from `{x:0,y:-3}` to `{x:4,y:-3}` and records that `text_center_error_px=0` verifies registered placement, not rendered YMM4 glyph optical center. Readback passes as `pass_callout_label_alignment_fixed` with `diagnostic_only=true`, `production_candidate=false`, 1920x1080 / 16:9, bottom 20% caption reserve clear, focal chain 3, callout count 3, non-focal hosts, dense table false, indexed whiteboard false, and zero external image / URL / source footage / audio / TTS / token-like counts. This remains diagnostic-only: no Review Console ingest, production render, production carrier approval, creative final acceptance, rights automation, slot-fill, external material, G-27 revival, ClipPipeGen, RSS / OPML / Inoreader / NotebookLM, or common foundation / Codex Worker Orchestration work. Next safe move is human YMM4 GUI recheck of the callout-label alignment fix.
- **G-28 real-estate right-node YMM4 diagnostic alignment fixed (2026-06-07)**: Human GUI recheck after the layout-contract implementation returned `revise_probe_again_narrow_right_node_text_alignment`: openability, focal chain, connector treatment, caption reserve, callouts, and host role passed, while only right-node `借主判断` rectangle text alignment remained partial and readback metric trust was partial. `scripts/build_g28_real_estate_ymmp_probe.js --write` now applies `g28_real_estate_information_gap_right_node_alignment_v1` by changing only `G28_LDC_Node_Right_Label` registered optical offset from `{x:0,y:-4}` to `{x:4,y:-4}` and records the metric caveat that `text_center_error_px=0` verifies registered placement, not rendered YMM4 glyph optical center. Readback passes as `pass_right_node_alignment_fixed` with `diagnostic_only=true`, `production_candidate=false`, 1920x1080 / 16:9, bottom 20% caption reserve clear, focal chain 3, callout count 3, non-focal hosts, dense table false, indexed whiteboard false, and zero external image / URL / source footage / audio / TTS / token-like counts. This remains diagnostic-only: no Review Console ingest, production render, production carrier approval, creative final acceptance, rights automation, slot-fill, external material, G-27 revival, ClipPipeGen, RSS / OPML / Inoreader / NotebookLM, or common foundation / Codex Worker Orchestration work. Next safe move is human YMM4 GUI recheck of the right-node alignment fix.
- **G-28 real-estate YMM4 diagnostic probe layout contract implemented (2026-06-07)**: `scripts/build_g28_real_estate_ymmp_probe.js` now implements `g28_real_estate_information_gap_layout_contract_v1` for the existing diagnostic probe. `node scripts\build_g28_real_estate_ymmp_probe.js --write` and the dry check pass with classification `pass_probe_polished`; readback records `layout_contract_metrics_present=true`, `layout_contract_tolerances_pass=true`, `text_center_error_px=0`, `registered_optical_offset_max_px=4`, `connector_alignment_error_px=0`, `caption_reserve_overlap_px=0`, callout density `0.818 / 0.333`, and `host_focality_risk=low`. The boundary remains `diagnostic_only=true` / `production_candidate=false`; this is not Review Console ingest, production render, production carrier approval, creative final acceptance, rights automation, real material slot-fill, source footage/audio/TTS, external image/URL/raw reference, G-27 revival, ClipPipeGen, RSS / OPML / Inoreader / NotebookLM, or common foundation / Codex Worker Orchestration work. Next safe move is human YMM4 GUI recheck before any Review Console ingest decision.
- **G-28 real-estate YMM4 diagnostic probe layout contract audited (2026-06-07)**: `docs/verification/G28-REAL-ESTATE-YMMP-PROBE-LAYOUT-CONTRACT-AUDIT-2026-06-07.md` records a docs-only audit of the polished probe layout contract. The visual probe remains accepted as diagnostic GUI review surface (`pass_probe_polished`, `diagnostic_only=true`, `production_candidate=false`), but reuse is not yet a fully implemented layout system: text centering uses a clear top-left formula plus manual optical offsets, connector positions can be explained as edge-to-edge bars but are still hard-coded overrides, and callout slots are a three-callout-specific row. Recommended next decision is `needs_layout_contract_implementation`, handled as one bounded layout-system revision before Review Console ingest. This slice did not change `.ymmp`, builder/generator, readback JSON, probe report, generated artifacts, render/video, production approval, creative final acceptance, rights automation, source footage, audio/TTS, external image/URL/raw reference, G-27, ClipPipeGen, RSS / OPML / Inoreader / NotebookLM, or local residue.
- **G-28 real-estate polished YMM4 diagnostic probe GUI re-review recorded (2026-06-07)**: `docs/verification/G28-REAL-ESTATE-YMMP-PROBE-HUMAN-REVIEW-2026-06-07.md` now records the polished probe re-review result as `overall_decision=accept_as_diagnostic_gui_probe_with_layout_contract_followup`. Openability, focal-chain readability, caption reserve, callout readability, host role, real-service/property safety, and diagnostic boundary pass/clear; yellow connector treatment and rectangle text alignment are `pass_partial` because the current visual result improved, but the underlying coordinate/centering rules are not yet formalized. The next safe action is `G-28 real estate YMM4 probe layout contract audit`: define rectangle text centering formula, connector positioning formula, callout slot rule, manual offset registry, tolerance readback, and the post-audit decision between Review Console ingest and one bounded layout-system revision. This slice did not change `.ymmp`, builder/generator, readback, report, render/video, production approval, creative final acceptance, rights automation, source footage, audio/TTS, external image/URL/raw reference, G-27, ClipPipeGen, RSS / OPML / Inoreader / NotebookLM, or local residue.
- **G-28 real-estate YMM4 diagnostic probe bounded polish revision passed (2026-06-07)**: `scripts/build_g28_real_estate_ymmp_probe.js --write` now regenerates the same self-contained diagnostic probe after human `revise_probe` with classification `pass_probe_polished`. The bounded polish adjusts yellow connector alignment, callout slot spacing, and TextItem visual offsets while preserving `variant_id=g28_ldc_real_estate_information_gap`, `diagnostic_only=true`, `production_candidate=false`, 1920x1080 / 16:9, bottom 20% caption reserve clear, focal chain `元付情報` -> `ポータル掲載` -> `借主判断`, three callouts, non-focal lower-corner hosts, bounded text budget, `dense_table=false`, `indexed_whiteboard=false`, and zero external image / URL / source footage / audio / TTS / token-like counts. This remains diagnostic-only: no production carrier approval, creative final acceptance, render/video, rights automation, real material slot-fill, G-27 revival, ClipPipeGen access, RSS / OPML / Inoreader / NotebookLM work, or local residue handling.
- **G-28 real-estate YMM4 diagnostic probe human review recorded (2026-06-07)**: `docs/verification/G28-REAL-ESTATE-YMMP-PROBE-HUMAN-REVIEW-2026-06-07.md` records the user-side YMM4 GUI result for `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.ymmp`. Openability, focal-chain readability, caption reserve, host role, real-service/property safety, and diagnostic boundary all pass/clear; callout readability is `pass_partial`; alignment/polish is `partial`; overall decision is `revise_probe` with `production_boundary_acknowledged=true`. The allowed next slice is a bounded diagnostic polish revision only: improve yellow connector treatment, rectangle text alignment, small visual offsets, and callout polish while preserving the same variant id, frame, caption reserve, focal chain, callouts, non-focal hosts, diagnostic-only / production-candidate-false boundary, and zero external image / URL / raw reference / source footage / audio / TTS / render counts. This is not production carrier approval, creative final acceptance, render approval, rights approval, real material slot-fill, G-27 revival, common foundation implementation, ClipPipeGen access, RSS / OPML / Inoreader / NotebookLM work, or local residue handling.
- **G-28 real-estate self-contained YMM4 diagnostic probe generated (2026-06-07)**: `scripts/build_g28_real_estate_ymmp_probe.js --write` now builds the first YMM4-compatible diagnostic probe for accepted `g28_lecture_diagram_carrier_real_estate_information_gap_v1`, writing `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.ymmp`, `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_readback.json`, and `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_report.md`. Readback passed with classification `pass_ymmp_probe_created`, `diagnostic_only=true`, `production_candidate=false`, 1920x1080 / 16:9, bottom 20% caption reserve clear, focal chain `元付情報` -> `ポータル掲載` -> `借主判断`, 3 callouts (`情報遅延`, `掲載粒度の欠落`, `仲介インセンティブ`), non-focal lower-corner hosts, layer order stage -> title -> focal surfaces -> connectors -> focal labels -> callouts -> hosts, diagnostic text budget 7 items / 42 chars, `dense_table=false`, `indexed_whiteboard=false`, and external image / URL / source footage / audio / TTS / token-like counts all 0. This is a self-contained diagnostic probe only: no render/video, production carrier approval, creative final acceptance, rights automation, real material slot-fill, external image/URL/raw reference, G-27 revival, common foundation implementation, ClipPipeGen access, RSS / OPML / Inoreader / NotebookLM work, or local residue handling is part of the slice. Next safe action is human YMM4 GUI openability/readability review of the generated probe only.
- **G-28 real-estate YMM4-compatible probe plan added (2026-06-07)**: `docs/verification/G28-REAL-ESTATE-YMM4-COMPATIBLE-PROBE-PLAN-2026-06-07.md` now plans a later self-contained YMM4-compatible diagnostic probe for the accepted `g28_lecture_diagram_carrier_real_estate_information_gap_v1` Lecture Diagram Carrier. The target remains `diagnostic_only=true`, `production_candidate=false`, readback-passed, shapes/text only, and abstract real-estate information asymmetry (`元付情報` -> `ポータル掲載` -> `借主判断`; callouts `情報遅延`, `掲載粒度の欠落`, `仲介インセンティブ`). The plan fixes intended item/group mapping, layer order, YMM4 compatibility constraints, later readback requirements, human GUI checklist, and next-slice options. This slice created a plan only: no `.ymmp`, render, production carrier approval, creative final acceptance, rights automation, new G-28 variant, generator change, generated JSON/HTML/readback/report change, G-27 revival, common foundation implementation, ClipPipeGen access, external image/URL/raw reference intake, RSS / OPML / Inoreader / NotebookLM work, or local residue handling.
- **G-28 game-mechanics semantics clarified (2026-06-07)**: `docs/verification/G28-GAME-MECHANICS-DIAGRAM-SEMANTICS-NOTE-2026-06-05.md` now clarifies the `decision=revise` target for `g28_lecture_diagram_carrier_game_mechanics_explanation_v1`: this Lecture Diagram Carrier explains `player input / state -> collision or rule check -> resulting feedback`, not general game-screen atmosphere. The middle node remains a 3-node chain member and should be read first as `判定 / 当たり判定`, sharpening the existing `内部ルール / 判定` semantics without adding a fourth node. Callouts stay bounded to 2-3, with `判定 / 当たり判定` primary and `操作感` / `リスクとリターン` supporting. Caption reserve, non-focal host role, `dense_table=false`, `indexed_whiteboard=false`, `diagnostic_only=true`, and `production_candidate=false` remain boundaries. No generator, new variant, JSON/readback/report rewrite, `.ymmp`, render, production promotion, creative final acceptance, G-27 revival, common foundation implementation, ClipPipeGen access, external image/URL/raw reference intake, RSS / OPML / Inoreader / NotebookLM work, or local residue handling is part of the slice. Next safe artifact, only if explicitly opened, is a bounded diagnostic JSON/report label pass that preserves the same carrier contract.
- **G-28 diagnostic human decisions recorded (2026-06-07)**: `docs/verification/G28-DIAGNOSTIC-HUMAN-DECISION-RECORD-2026-06-07.md` now records the supplied human decisions for all six G-28 diagnostic artifacts. Generic Lecture Diagram skeleton and `real_estate_information_gap` are `accept_as_diagnostic_direction`; `game_mechanics_explanation` is `revise` with revision target limited to diagnostic semantics already anchored by `docs/verification/G28-GAME-MECHANICS-DIAGRAM-SEMANTICS-NOTE-2026-06-05.md`; Map / Evidence, Source-Footage definition-only, and Conversation / Buffer definition-only are `defer_to_ymmp_carrier_probe`. These decisions are diagnostic-review decisions only: no production carrier approval, creative final acceptance, generator change, new variant, `.ymmp`, render, rights / production automation, G-27 revival, common foundation implementation, real codex exec, ClipPipeGen access, external image/URL/raw reference intake, RSS / OPML / Inoreader / NotebookLM work, or local residue handling is part of the slice. Next safe G-28 work is game-mechanics revise clarification or a bounded YMM4-compatible probe plan for deferred carriers.
- **G-28 diagnostic human decision record added (2026-06-07)**: `docs/verification/G28-DIAGNOSTIC-HUMAN-DECISION-RECORD-2026-06-07.md` now records the intake surface for human decisions on existing G-28 diagnostic artifacts. Because no new human `accept` / `revise` / `reject` / `defer_to_ymmp_carrier_probe` decision was supplied in the prompt, all listed artifacts remain `pending_human_decision`; no decision was invented. This is diagnostic review intake only: no G-28 variant duplication, generator change, `.ymmp`, render, production carrier approval, creative final acceptance, rights / production automation, G-27 revival, common foundation implementation, real codex exec, ClipPipeGen access, image/URL/raw reference intake, RSS / OPML / Inoreader / NotebookLM work, or local residue handling is part of the slice.
- **G-28 diagnostic human review packet added (2026-06-07)**: `docs/verification/G28-DIAGNOSTIC-HUMAN-REVIEW-PACKET-2026-06-07.md` now converts the existing G-28 diagnostic artifacts into a human decision surface with artifact inventory, readback summary, visual checklist, and `accept_as_diagnostic_direction` / `revise` / `reject` / `defer_to_ymmp_carrier_probe` schema. This is review coordination only: no new JSON/HTML/readback/report/generator artifact, no duplicate variant, no `.ymmp`, render, production carrier approval, creative final acceptance, G-27 revival, Codex Worker Orchestration implementation, real codex exec, external image/URL/raw reference intake, RSS / OPML / Inoreader / NotebookLM work, or cross-repo edit is part of the slice. Existing local residue remains out of scope.
- **G-28 game-mechanics diagram semantics note recorded (2026-06-05)**: The human response to `docs/verification/G28-GAME-MECHANICS-HUMAN-REVIEW-PACKET-2026-06-05.md` is `decision=revise`, `carrier=Lecture Diagram Carrier`. The accepted direction remains `入力操作` -> `内部ルール / 判定` -> `画面上の結果`, but the middle node must preserve room for one concrete internal processing example: first-review primary is `判定 / 当たり判定`, with `無敵時間` and `硬直` reserved as possible later substitutions, not simultaneous visible labels. `操作感` and `リスクとリターン` remain supporting callouts only. Owner note: `docs/verification/G28-GAME-MECHANICS-DIAGRAM-SEMANTICS-NOTE-2026-06-05.md`. This is semantics documentation only: no new variant, generator, Source-Footage work, gameplay screenshot/source footage intake, image/path/URL/raw reference, `.ymmp`, render, production timing, creative final acceptance, generated artifact modification, G-27 revival, RSS / OPML / Inoreader / NotebookLM work, or cross-repo edit was performed.
- **Remote handoff sealed after G-28 game-mechanics human review packet (2026-06-05)**: The latest G-28 context is preserved in-project for another terminal. The current line is still diagnostic-only G-28 Reference-Driven Generic Screen Carrier work, not production completion. The game-mechanics shot is routed to Lecture Diagram Carrier as primary, with Source-Footage Carrier only as a future backup if a separate production slice makes real gameplay footage the evidence surface. Current owner artifacts are `docs/verification/G28-SHOT-CARRIER-SELECTION-GAME-MECHANICS-2026-06-05.md` and `docs/verification/G28-GAME-MECHANICS-HUMAN-REVIEW-PACKET-2026-06-05.md`, with existing precedent `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.*` readback-passed and `diagnostic_only=true` / `production_candidate=false`. `docs/USER_COPYPASTE_BLOCKS.md` now has a current G-28 game-mechanics resume prompt for ChatGPT/Codex handoff. No existing JSON/HTML/readback/report/generator artifact was changed, and no new theme variant, carrier skeleton, Source-Footage generator, source footage or gameplay screenshot intake, image path/URL/raw reference, `.ymmp`, render, production timing, creative final acceptance, G-27 blocker revival, RSS / OPML / Inoreader / NotebookLM work, or cross-repo edit is part of this handoff. Next valid work is to record a human `accept` / `revise` / `reject` response for the review packet, make diagram-semantics notes if revised, or create a Source-Footage design-only checklist only if the human says footage itself is required evidence.
- **G-28 shot carrier selection worksheet added (2026-06-05)**: `docs/verification/G28-SHOT-CARRIER-SELECTION-WORKSHEET-2026-06-05.md` now converts the G-28 toolbox into a blank per-shot input template and carrier routing worksheet. It records the fields a human must return, routes mechanism / cause-effect / misconception shots to Lecture Diagram, geography / statistics / cited evidence to Map / Evidence, gameplay / property / GUI / source screen shots to Source-Footage, and reaction / question / pause / transition shots to Conversation / Buffer. No existing JSON/HTML/readback/report/generator artifact was changed, and no new theme variant, carrier skeleton, source footage or gameplay screenshot intake, image path/URL/raw reference, `.ymmp`, render, production timing, creative final acceptance, G-27 blocker revival, or RSS / OPML / Inoreader / NotebookLM work was added.
- **G-28 archetype toolbox consolidated (2026-06-05)**: `docs/verification/G28-CARRIER-ARCHETYPE-TOOLBOX-2026-06-05.md` now gathers the four G-28 carrier archetypes into a selection matrix rather than adding more samples. Lecture Diagram Carrier and Map / Evidence Carrier remain readback-passed diagnostic-only artifacts; Source-Footage Carrier and Conversation / Buffer Carrier remain unimplemented archetype definitions with no generator/readback. No existing JSON/HTML/report/script artifact was changed, and this slice did not add a new skeleton, theme variant, source footage or gameplay screenshot intake, real map/satellite/image path/URL/raw reference, `.ymmp`, render, production timing, creative final acceptance, G-27 blocker revival, or RSS / OPML / Inoreader / NotebookLM work. Next valid work is a human review packet for an existing diagnostic carrier, or a bounded design-only checklist for Source-Footage / Conversation after a real production need is selected.
- **Remote handoff sealed after G-28 Map / Evidence Carrier skeleton (2026-06-05)**: The context through the Map / Evidence Carrier diagnostic skeleton is now preserved in-project for the next terminal. The sealed work is the G-28 Reference-Driven Generic Screen Carrier line with Lecture Diagram generic skeleton, `real_estate_information_gap`, `game_mechanics_explanation`, and the separate Map / Evidence Carrier skeleton all readback-passed and diagnostic-only. Current restart remains `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file. `docs/USER_COPYPASTE_BLOCKS.md` now also has a current G-28 Map / Evidence resume prompt so the user can paste the latest bounded context into ChatGPT without reconstructing it. Known local-only untracked artifacts remain `.claude/worktrees/` and `samples/2026-05-16.ymmp`; they were not touched, staged, promoted, or deleted. Valid next work is G-28 archetype-level consolidation or a narrowly scoped human review packet; do not add more Lecture Diagram theme variants by default, and do not treat any G-28 diagnostic artifact as production carrier approval. No real map or satellite image, image/path/URL/raw reference intake, source footage, gameplay screenshot intake, `.ymmp`, render, production timing, creative final acceptance, G-27 promotion, RSS / OPML / Inoreader / NotebookLM work, or cross-repo edit is part of this handoff.
- **G-28 Map / Evidence Carrier diagnostic skeleton generated (2026-06-05)**: A second G-28 carrier archetype now exists next to Lecture Diagram Carrier, without adding another Lecture Diagram theme variant. `scripts/build_g28_map_evidence_carrier_skeleton.js --write` writes `samples/_probe/g28/map_evidence_carrier_skeleton.json`, `samples/_probe/g28/map_evidence_carrier_skeleton_readback.json`, `samples/_probe/g28/map_evidence_carrier_skeleton.html`, and `samples/_probe/g28/map_evidence_carrier_skeleton_report.md`. Readback passed with `diagnostic_only=true`, `production_candidate=false`, 1920x1080 / 16:9 frame, `composition_type=center-focal`, main evidence area in canvas, 3 annotation slots, bounded source note area, caption reserve clear, host role non-focal, `dense_table=false`, `indexed_whiteboard=false`, `tiny_text=false`, `external_image_count=0`, `external_url_count=0`, and `token_like_pattern_count=0`. The SCS mapping stays on existing `center-focal` rather than adding a new type. This is a diagnostic Map / Evidence screen contract only: no real map or satellite image, image/path/URL/raw reference intake, source footage, gameplay screenshot intake, `.ymmp`, render, production timing, creative final acceptance, G-27 promotion, RSS / OPML / Inoreader / NotebookLM work, or cross-repo edit was performed. Existing Lecture Diagram generic skeleton plus `real_estate_information_gap` and `game_mechanics_explanation` variants still pass.
- **G-28 game_mechanics_explanation diagnostic variant generated (2026-06-05)**: The second narrow Lecture Diagram Carrier theme variant now exists to verify that G-28 is not limited to the real-estate information-gap example. `scripts/build_g28_lecture_diagram_carrier_skeleton.js` supports `--variant game_mechanics_explanation` and writes `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.json`, `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_readback.json`, `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.html`, and `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_report.md`. Readback passed with `diagnostic_only=true`, `production_candidate=false`, `variant_id=g28_ldc_game_mechanics_explanation`, `composition_type=center-focal`, caption reserve clear, focal chain node count 3 (`入力操作` -> `内部ルール` -> `画面上の結果`), callout count 3 (`操作感`, `判定 / 当たり判定`, `リスクとリターン`), host role non-focal, two visible text items / 13 chars, `dense_table=false`, `indexed_whiteboard=false`, `source_footage_carrier=false`, `external_image_count=0`, `external_url_count=0`, and `token_like_pattern_count=0`. This is a diagnostic Lecture Diagram reuse check only: no `.ymmp`, render, production timing, creative final acceptance, source-footage carrier promotion, gameplay screenshot intake, image/path/URL intake, G-27 promotion, RSS / OPML / Inoreader / NotebookLM work, or cross-repo edit was performed. The existing generic skeleton and `real_estate_information_gap` variant still pass.
- **Remote handoff sealed after G-28 real_estate_information_gap variant (2026-06-05)**: The latest G-28 diagnostic variant context is now preserved in-project and pushed to `origin/master`. Current restart target is `master` at `9ab084c docs: align G-28 variant composition type`; `git rev-list --left-right --count HEAD...origin/master` was `0 0`, and tracked files were clean before this handoff note. Known local-only untracked artifacts remain `.claude/worktrees/` and `samples/2026-05-16.ymmp`; they were not touched, staged, promoted, or deleted. The active repo context remains G-28 Reference-Driven Generic Screen Carrier refinement from the Lecture Diagram skeleton plus the `real_estate_information_gap` diagnostic variant. Valid next work is either another narrow diagnostic theme variant or an explicitly scoped YMM4-saved carrier review packet. Do not treat this as production carrier approval, creative final acceptance, render readiness, `.ymmp` generation, G-27 revival, source footage intake, image/path/URL intake, RSS / OPML / Inoreader / NotebookLM work, or cross-repo newsroom work.
- **G-28 real_estate_information_gap diagnostic variant generated (2026-06-05)**: The first theme-specific Lecture Diagram Carrier variant now exists without returning to G-27 or production flow. `scripts/build_g28_lecture_diagram_carrier_skeleton.js` supports `--variant real_estate_information_gap` and writes `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap.json`, `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_readback.json`, `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap.html`, and `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_report.md`. Readback passed with `diagnostic_only=true`, `production_candidate=false`, `variant_id=g28_ldc_real_estate_information_gap`, 1920x1080 / 16:9 frame, bottom 20% caption reserve clear, focal area in main canvas, focal chain node count 3 (`元付情報` -> `ポータル掲載` -> `借主判断`), callout count 3 (`情報遅延`, `掲載粒度の欠落`, `仲介インセンティブ`), host role non-focal, bounded layer order, two visible text items / 15 chars, `dense_table=false`, `indexed_whiteboard=false`, `external_image_count=0`, `external_url_count=0`, and `token_like_pattern_count=0`. The generic skeleton path still passes via `node scripts\build_g28_lecture_diagram_carrier_skeleton.js --write` and produced no tracked generic artifact diff. This slice generated JSON / HTML / readback / MD only: no `.ymmp`, render, production timing, creative final acceptance, source footage, image/path/URL intake, RSS / OPML / Inoreader / NotebookLM work, or cross-repo edit was performed. Next valid G-28 frontier is either another narrow theme variant or an explicitly scoped YMM4-saved carrier review; do not treat this diagnostic variant as a production carrier.
- **G-28 Lecture Diagram Carrier diagnostic skeleton generated (2026-06-05)**: G-28 advanced from reference style brief to the first concrete Lecture Diagram Carrier diagnostic artifact. New owner files: `docs/verification/G28-LECTURE-DIAGRAM-CARRIER-SPEC-2026-06-05.md`, `scripts/build_g28_lecture_diagram_carrier_skeleton.js`, and generated artifacts under `samples/_probe/g28/lecture_diagram_carrier_skeleton.{json,html}`, `samples/_probe/g28/lecture_diagram_carrier_skeleton_readback.json`, and `samples/_probe/g28/lecture_diagram_carrier_skeleton_report.md`. Readback passed with `diagnostic_only=true`, `production_candidate=false`, 1920x1080 / 16:9 frame, bottom 20% caption reserve clear, focal group inside main canvas, lower-corner hosts above caption reserve, 3 callout slots, 14 primitive items, and 8 semantic elements. This deliberately separates Agent-owned diagnostic skeleton generation from human-owned creative final acceptance: no reference images, image paths, URLs, external assets, YMM4 `.ymmp`, production render, production timing, real material slot-fill, G-27 promotion, RSS / OPML / Inoreader / NotebookLM source-pack work, or cross-repo edit was performed. Next valid G-28 frontier is a theme-specific Lecture Diagram variant JSON/readback or promotion of the same skeleton into a scoped YMM4-saved carrier review only after an explicit implementation slice.
- **G-28 reference style brief created from supplied images (2026-06-05)**: The user supplied seven visible reference images and directed a narrow G-28 principle-extraction slice. G-28 is no longer parked on missing reference input for this first pass: `docs/verification/G28-REFERENCE-STYLE-BRIEF-2026-06-05.md` now records per-image extraction notes, shared screen grammar, four generic carrier archetypes, SCS mapping, YMM4 item/group structure proposals, genre application notes, and failure modes to avoid. The images were treated as principle sources only; no image binaries, image paths, image URLs, raw reference material, OPML, tokens, article bodies, or private data were committed. Current next frontier is G-28 refinement from this style brief into SCS mapping fields, human-authored YMM4 carrier checklists, readback checks, or one design-only theme variant. G-27 remains retained evidence only and is not the active blocker; the diagnostic carrier was not promoted. No implementation, YMM4 `.ymmp` zero generation, render, production timing, creative final acceptance, RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack work, or cross-repo edit was performed.
- **G-28 parking handoff preserved in-project (2026-06-04)**: The detailed G-28 input-wait context is now held in `docs/verification/G28-REFERENCE-INPUT-WAIT-HANDOFF-2026-06-04.md`, with the reusable ChatGPT copy-block template preserved in `docs/USER_COPYPASTE_BLOCKS.md`. This keeps G-28 parked until 3-7 reference images plus per-image notes arrive, while keeping G-27 as retained evidence rather than an active blocker. No image binaries, image URLs, raw OPML, tokens, article bodies, private data, `.ymmp` zero generation, render, production timing, creative final acceptance, RSS recovery, NotebookLM input, or cross-repo newsroom edit is part of this handoff.
- **G-27 active blocker retired into reference evidence; G-28 proposed (2026-06-04)**: G-27 is no longer the active NLMYTGen next action or a production carrier waiting loop. Its Real Estate DX proof artifacts, diagnostic carrier, review console work, and SCS lessons are retained as case-specific evidence, but `samples/_probe/g24/real_estate_dx_diagnostic_carrier.ymmp` remains diagnostic-only and is not promoted to production. `samples/_probe/g24/real_estate_dx_review_decisions.json` remains absent for G-27-specific GUI handback, but that absence is not a blocker for the new generic direction. `docs/FEATURE_REGISTRY.md` now moves G-27 to `hold` and adds proposed G-28 `Reference-Driven Generic Screen Carrier`, with the thin v0.1 owner spec at `docs/REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md`. The next valid NLMYTGen frontiers are now either downstream intake from a newsroom-produced packet/transcript/ScriptIR/VisualIR/export bundle, or G-28 specification/refinement after the user supplies 3-7 reference images plus per-image notes about spacing, color, card density, DB feel, lock/gated-information feel, YouTube explainer feel, or news-infographic feel. RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection remains out of active NLMYTGen scope. No G-27 slot-fill, diagnostic carrier promotion, render, production timing, creative final acceptance, raw reference image commit, or code implementation was performed in this docs slice.
- **Remote handoff sealed for ChatGPT copy-block reporting (2026-06-04)**: The user requested that all current context be preserved in-project, local state be reflected to remote, and another terminal be able to resume immediately. This slice keeps `AGENTS.md` as an entry pointer and records the durable handoff in the narrow owners: `docs/runtime-state.md` for current restart state, `docs/INTERACTION_NOTES.md` for the explicit copy-block closeout contract, `docs/USER_COPYPASTE_BLOCKS.md` for the reusable ChatGPT single-block report template, and `docs/project-context.md` for the decision log. Latest valid restart remains `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file; deeper docs are optional unless the next task needs them. Its active-lane statement is superseded by the G-27 retirement note above; current active work is limited to downstream intake from a newsroom-produced packet/transcript/ScriptIR/VisualIR/export bundle, or G-28 reference-driven generic screen carrier specification/refinement. RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection remains upstream `newsroom-yt-pipeline` responsibility and must not be restarted here except explicit archival/reference-only recovery. The older G-27 blocker details in this handoff are retained as historical evidence only: the diagnostic carrier was not a silent production carrier, `samples/2026-05-16.ymmp` was non-production local residue, and `samples/_probe/g24/real_estate_dx_review_decisions.json` was absent. Known untracked artifacts from that handoff were `.claude/worktrees/` and `samples/2026-05-16.ymmp`; do not delete, stage, or promote local residue without an explicit request. No code, RSS recovery, NotebookLM input, YMM4 write/render, slot-fill, production timing, creative acceptance, PR, or cross-repo newsroom edit is part of this handoff.
- **G-27 carrier decision audit recorded (2026-06-04)**: `master` was rechecked before work and stayed aligned with `origin/master` at `8f49dcb docs: seal ChatGPT copy-block handoff`; `HEAD...origin/master` was `0 0`, and tracked files were clean aside from known untracked `.claude/worktrees/` and `samples/2026-05-16.ymmp`, which were not touched or promoted. This audit is now historical evidence rather than the active next action. Authority docs read: `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, this file, and `docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md`. Detailed decision prep is recorded in `docs/verification/G27-CARRIER-DECISION-HANDOFF-2026-06-04.md`. Current retained judgment: `samples/_probe/g24/real_estate_dx_diagnostic_carrier.ymmp` and its readback are useful only as a diagnostic proxy; required G-27 item names are present and readback passed, but the artifact still declares `diagnostic_only=true`, `production_carrier_replaced=false`, and `production_readiness_claimed=false`, so it must not be silently promoted. `samples/2026-05-16.ymmp` remained non-production residue with only three items and was excluded from carrier candidacy. `samples/_probe/g24/real_estate_dx_review_decisions.json` was absent, so accepted/revised/cut authority was not available for G-27 GUI handback. The safe-path and diagnostic-promotion choices are no longer the active NLMYTGen next action unless the user explicitly reopens this case-specific path. No RSS/source-selection, NotebookLM input, YMM4 write/render, slot-fill, production timing, creative acceptance, code change, PR, or untracked artifact promotion was performed.
- **Remote sync / roadmap-prep handoff refreshed (2026-06-03)**: `master` in `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen` was fast-forwarded from `origin/master` to `b2e6e22` (`docs: preserve user copypaste block context`) and rechecked at remote parity (`git rev-list --left-right --count HEAD...origin/master` => `0 0`). Tracked working tree was clean before this note; only known local/untracked artifacts remained: `.claude/worktrees/` and `samples/2026-05-16.ymmp`. Restart checks for this analysis slice passed: `git diff --check`, `uv run python -m src.cli.main --help`, and `uv run python -m src.cli.main validate --help`. Authority files were reread in the required order (`AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file), plus the feature registry, invariants, GUI minimum path, and production pipeline contract. Current roadmap-prep conclusion: active NLMYTGen work is still either downstream adapter intake from a newsroom-produced packet/transcript/ScriptIR/VisualIR/export bundle, or the G-27 `G27_PublicVsBrokerDB` carrier decision path. Feature registry count at this checkpoint: `done=48`, `approved=3` (`G-20`, `G-27`, `H-01`), `proposed=1` (`G-26`), `hold=9`, `quarantined=2`, `rejected=7`, `info=2`. The immediate G-27 blocker remains carrier/review authority, not code: the diagnostic carrier is diagnostic-only, `samples/2026-05-16.ymmp` is not a viable production carrier, `samples/_probe/g24/real_estate_dx_review_decisions.json` is absent, and the background skit validator still allows only `overlay_only_compact_review` because production cast templates and props are missing. Next best move: decide the G-27 carrier path before slot-fill, or provide a newsroom packet/export bundle for downstream adapter work. No code, RSS/source-selection recovery, NotebookLM input, YMM4 write/render, G-26 implementation, sports_news/Baseball work, or newsroom repo edit was performed in this handoff slice.
- **Remote handoff sealed after user copypaste block preservation (2026-06-03)**: `master` in `C:\Users\PLANNER007\NLMYTGen` was confirmed clean and aligned with `origin/master` before this slice, then updated with a user-facing reusable block library and pushed. The new saved context is `docs/USER_COPYPASTE_BLOCKS.md`: it preserves the single-document copy/paste asset for repo sync commands, dirty-stop wording, RSS archival prompts, game-industry source-pack prompts, NotebookLM preflight/return prompts, NLMYTGen/newsroom responsibility boundary prompts, G-27 carrier prompt, leak-check commands, completion report wording, and short user reply options. This file is explicitly not an Agent restart manual, not active next action, and not part of the normal restart read budget. `docs/NAV.md`, `docs/USER_REQUEST_LEDGER.md`, and `docs/project-context.md` now record that distinction. Latest valid restart remains `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file. NLMYTGen active work remains downstream adapter intake from newsroom-produced packet/transcript/ScriptIR/VisualIR/export bundle, or the G-27 `G27_PublicVsBrokerDB` carrier decision path. The local-only RSS artifacts in this workspace may exist (`_tmp/rss_topic_cluster_briefs_current.*`, `_local/rss/feeds.opml.xml`) but were not read into repo, regenerated, committed, or pushed. No implementation, tests, NotebookLM input, YMM4 work, G-27 write, RSS source-pack generation, OPML recovery, PR, or cross-repo newsroom edit was performed.
- **Remote handoff sealed after RSS responsibility retirement (2026-06-03)**: `master` was rechecked from `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen` with `git fetch --all --prune`, `git checkout master`, and `git pull --ff-only origin master`; it was already aligned with `origin/master` before this note (`git rev-list --left-right --count HEAD...origin/master` => `0 0`, prior top commit `e36f87d docs: retire RSS source selection from NLMYTGen active lane`). Tracked working tree was clean before this handoff note; only pre-existing untracked/local artifacts remained: `.claude/worktrees/` and `samples/2026-05-16.ymmp`. Current context is now held in repo docs: `docs/runtime-state.md` owns the restart line, `docs/project-context.md` records the 2026-06-03 decision to retire RSS/source selection from NLMYTGen active work, `docs/INVARIANTS.md` fixes the downstream-adapter boundary, and `README.md` lists RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection as a non-goal here. Restart from another terminal by pulling latest `master`, then read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file. Do not resume by placing OPML or restoring `_tmp/rss_topic_*` in NLMYTGen unless explicitly requested as archival/manual recovery. Next valid NLMYTGen work is either receiving a `newsroom-yt-pipeline` produced packet/transcript/ScriptIR/VisualIR/export bundle and converting it into YMM4 CSV / adapter / review / proof-ingest work, or continuing the existing G-27 `G27_PublicVsBrokerDB` carrier decision path. No code, tests, RSS source pack generation, Inoreader API, NotebookLM input, G-27 write, YMM4 render, Baseball, Thumbnail, GUI gap audit, or newsroom repo edit was performed in this handoff slice.
- **RSS source-selection retired from the active NLMYTGen lane (2026-06-03)**: The previous game-industry source-pack handoff is superseded. RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection were useful transitional scaffolding in NLMYTGen, but they are no longer the active NLMYTGen next action. Future source ingest, article ledgers, story clustering, scoring, and NotebookLM packet preparation belong in `newsroom-yt-pipeline`. Do not place OPML in NLMYTGen, restore `_tmp/rss_topic_*_current` artifacts, or rerun source-pack selection here unless the user explicitly asks for archival/manual recovery. NLMYTGen resumes after receiving a newsroom-produced packet, transcript, ScriptIR, VisualIR, or export bundle and then converts it into YMM4 CSV / adapter / review / proof-ingest work; the existing G-27 `G27_PublicVsBrokerDB` carrier decision remains the other active NLMYTGen frontier. Failed feeds are irrelevant to this downstream adapter role.
- **Remote sync / roadmap-prep verified (2026-06-02)**: `master` was fast-forwarded from `origin/master` to pulled remote base `29ca758` (`docs: seal remote handoff context`) and rechecked at parity with `origin/master` (`git rev-list --left-right --count HEAD...origin/master` => `0 0`) before this handoff note was written. Narrow verification for the pulled RSS parser change passed: `uv run pytest tests/test_feed_parse.py` => `17 passed`. Working tree remains reusable but not fully clean because pre-existing ignored/local artifacts are present: `.claude/worktrees/` and `samples/2026-05-16.ymmp`. The local RSS source-selection artifacts named by the 2026-06-01 handoff are absent in this checkout (`_tmp/rss_topic_cluster_briefs_current.{md,json}` and `_local/rss/feeds.opml.xml` not found), so the next RSS source-narrowing step either needs those local artifacts from the original terminal or a fresh operator OPML export before representative NotebookLM inputs can be selected. The sanitized committed RSS decision surface remains `docs/verification/RSS-PICKUP-FIRST-BRIEF-SUMMARY-2026-06-01.md`; the current production-lane decision surface remains the G-27 carrier choice recorded below.
- **Remote handoff sealed after RSS brief slice (2026-06-01)**: Latest RSS pickup-first handoff has been committed and pushed on `master`; local and `origin/master` were verified aligned after push before this note was written. Restart from another terminal with `cd C:\Users\PLANNER007\NLMYTGen && git fetch --all --prune && git checkout master && git pull --ff-only origin master`, then read `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, this file, and `docs/verification/RSS-PICKUP-FIRST-BRIEF-SUMMARY-2026-06-01.md`. The immediately useful local-only working artifacts are `_tmp/rss_topic_cluster_briefs_current.{md,json}`; they are ignored because they may contain source-selection details and must not be committed. If those local-only artifacts are unavailable in a different workspace, regenerate the candidate pass from ignored `_local/rss/feeds.opml.xml` only if that OPML is present; otherwise proceed from the sanitized summary and ask the user for the local RSS artifacts. Next work should start by choosing 1-3 generated video-theme clusters for NotebookLM source narrowing, not by reopening failed-feed cleanup, Inoreader sync, G-27, Baseball, Thumbnail, GUI gap audit, YMM4, or video generation.
- **A-04 RSS pickup-first topic cluster briefs generated (2026-06-01)**: RSS lane moved from candidate pickup to video-theme brief selection without requiring failed-feed cleanup or Inoreader sync. Local-only brief artifacts were generated at `_tmp/rss_topic_cluster_briefs_current.{md,json}` from `_tmp/rss_topic_candidates_current.json`; these local files may contain article/source details and must not be committed. Sanitized committed summary is `docs/verification/RSS-PICKUP-FIRST-BRIEF-SUMMARY-2026-06-01.md`. Input counts stayed at `147` sources, `121` fetched sources, `26` error sources, `6470` candidate entries, `5410` category-bearing entries, and `7` represented categories. Generated `9` video-theme clusters; top generated theme candidates are `AIの燃料を誰が握るのか`, `関税が世界を小さくする日`, and `終わらない戦争が日常を変える`. Failed feeds remained skipped known noise, not a blocker. NotebookLM API, actual NotebookLM input, script generation, YMM4 patching, video generation, Inoreader API, G-27, Baseball, Thumbnail, GUI gap audit, DB sync, background polling, and PR work were not run. Next useful move is for the user to choose 1-3 generated clusters, then narrow local-only representative sources for NotebookLM input.
- **A-04 RSS pickup-first candidate pass restored output path (2026-06-01)**: RSS lane direction is now pickup-first / output-oriented for current work: failed feeds are skipped and are not a blocker for topic selection, NotebookLM source selection, or video planning. Current OPML remained local-only at `_local/rss/feeds.opml.xml` and ignored. A read-only OPML fetch produced local-only candidate artifacts at `_tmp/rss_topic_candidates_current.{md,json}` and `_tmp/rss_fetch_report_current.{md,json}`; these must not be committed because they contain article/feed details. The wide candidate JSON pass produced `147` sources, `121` fetched sources, `26` error sources, `6470` candidate entries, `5410` category-bearing entries, and `7` represented categories. A separate markdown fetch run produced a nearby live count (`6490` entries), so small count drift is expected. Failed feeds remain delete-first cleanup noise, not a gate. Assistant fixed a small parser-stop bug so malformed XML payloads are classified as failed feeds instead of crashing the whole pickup run; narrow RSS tests passed. Next useful move is to choose 3-10 topic/source clusters from the local candidate list and feed those into NotebookLM / video topic planning. Inoreader API, token use, subscription mutation, feed replacement research, 403/header tuning, post-cleanup smoke gate, G-27, Baseball, Thumbnail, GUI gap audit, YMM4 patch, render, YouTube posting, DB sync, and background polling were not run.
- **Carrier requirement clarified; remote handoff prepared (2026-06-01)**: User challenged whether a human-authored `G27_PublicVsBrokerDB` carrier is truly necessary. Current decision: for the existing production slot-fill route, a stable YMM4-saved carrier or an explicit promotion of an existing diagnostic artifact is required. The reason is boundary control: YMM4 remains the production base and Python/assistant work is the CSV/IR/registry/post-import `.ymmp` patch layer, so assistant must not silently turn diagnostic raw geometry into a production layout. The carrier is not a beauty/final-design request; it is a stable stage with fixed `G27PBD_*` item names, fixed public/broker card counts, clear caption safe area, short Remarks, and geometry/color/font/layout owned outside later patching. Current recommended choices for the next operator turn are: (1) make/return the minimal YMM4 carrier from `docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md`, safest for production; (2) explicitly promote `samples/_probe/g24/real_estate_dx_diagnostic_carrier.ymmp` as the production carrier, fastest but requires a new boundary/readback record and runtime-state update; or (3) proceed without a carrier only as diagnostic/planning, not production slot-fill. Existing `samples/2026-05-16.ymmp` is not viable because it has only 3 item-like entries. For another terminal: start from `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file, then continue at the carrier decision above. No code, tests, RSS smoke, YMM4 write, render, production timing, G-26, Baseball, publishing, or broad roadmap work was performed in this clarification.
- **Pasted refresh review reconciled; use repo evidence over pasted state (2026-06-01)**: A pasted full-project review was checked against the current worktree and is directionally useful but not authoritative. Do not reuse its `clean` / `proposed=0` / "assistant side complete" claims without rechecking. Current repo state at reconciliation: `master` is aligned with `origin/master` at `fb60117`, with untracked `.claude/worktrees/` and `samples/2026-05-16.ymmp`. The untracked `samples/2026-05-16.ymmp` has only 3 item-like entries (`G27PBD_BG`, `G27PBD_Title`, and `公開ポータル`) and is not the awaited production carrier. FEATURE proposed remains `1` (`G-26`). G-27 remains blocked on the human-authored `G27_PublicVsBrokerDB` carrier and on absent GUI review decisions (`samples/_probe/g24/real_estate_dx_review_decisions.json`); the background-skit validator still permits only `overlay_only_compact_review`. A-04 RSS cleanup remains pending until the human deletes candidates in Inoreader and exports a fresh OPML to `_local/rss/feeds.opml.xml`. This was docs-only reconciliation; no code, test, RSS smoke, YMM4 write, render, production timing, G-26, Baseball, or publishing work was run.
- **A-04 RSS delete-first failed-feed cleanup policy accepted (2026-05-29)**: User confirmed RSS feed resources do not need strict completeness and the current sample count is sufficient. Failed-feed cleanup is now delete-first: `http_404`, `parse_or_non_feed`, `ssl_error`, `timeout`, and `http_403` are default delete candidates, with no per-feed replacement research and no bot-bypass / header-tuning work. Exceptions are only explicitly protected feeds or category coverage risk. Duplicate feed URL remains `0`; duplicate title remains `1` and stays `manual_review` because title alone does not authorize deletion. The latest committed sanitized decision record is `docs/verification/RSS-FAILED-FEED-CLEANUP-DECISION-2026-05-29.md`; local operator checklist path is `_tmp/rss_delete_first_cleanup_checklist.md` and must not be committed. Inoreader-side changed count is unknown. Post-cleanup smoke is pending until the human deletes candidates in the Inoreader UI, exports a fresh OPML to `_local/rss/feeds.opml.xml`, and reruns sanitized `list-feed-sources` / `rss-smoke`. Repo-side Inoreader API, token use, subscription mutation, G-27, Baseball, Thumbnail, and GUI work were not run.
- **A-04 RSS failed-feed cleanup audit recorded (2026-05-28)**: RSS UI comparison confirmed the OPML lane can treat the current OPML as the operational source of truth for now: NLMYTGen sees `147` sources and `7` categories, matching the reader-side count/folder check. A local-only cleanup audit wrote detailed candidates with feed titles/URLs to `_tmp/rss_failed_feed_cleanup_candidates.{md,json}`; these files remain uncommitted. Sanitized committed summary is `docs/verification/RSS-FAILED-FEED-CLEANUP-SUMMARY-2026-05-28.md`. Current audit rerun found `26` failed feeds (`http_403=4`, `http_404=2`, `parse_or_non_feed=15`, `ssl_error=2`, `timeout=3`), while prior smoke diagnostics varied around `31/32` errors. Cleanup priority is `http_404 -> parse_or_non_feed -> ssl_error -> timeout -> http_403`. Duplicate feed URL remains `0`; duplicate title remains `1` and is `manual_review`. Inoreader API, token use, subscription mutation, G-27, Baseball, Thumbnail, and GUI work were not run.
- **A-04 RSS real OPML smoke evidence diagnosed (2026-05-28)**: Live OPML smoke on `master` uses ignored input `_local/rss/feeds.opml.xml`; raw OPML stays out of git. Sanitized evidence is `docs/verification/RSS-LIVE-SMOKE-EVIDENCE-2026-05-28.md`. Current diagnostic rerun: source count `147`, category count `7`, fetch status counts `fetched=115`, `empty=0`, `error=32`, `listed=0`; live fetch error count varied around the prior `31` baseline. Error categories are now classified without raw URLs: `http_403=5`, `http_404=8`, `parse_or_non_feed=15`, `ssl_error=2`, `timeout=2`. `source_categories=absent` is bounded to representative sampling, not OPML parsing: 106 source records have categories, 82 fetched sources have categories, and 5355 matched entries came from categorized sources, but 0 shown representative entries did. Leakage check found no URL/token/raw OPML markers in evidence. RSS UI comparison remains `manual_required`; Inoreader API and G-27 were not run. Next safe RSS entries are reader UI spot-check, failed-feed cleanup, and representative source_categories propagation tuning.
- **A-04 RSS Reader Sync v1.1 merged to master and pushed (2026-05-27)**: Branch `codex/rss-reader-sync-master-integrate` was reviewed, fast-forward merged into `master`, and pushed to `origin/master` at commit `1599cf5 docs(feed): update RSS live smoke runbook branch`. Merge range: `da30ff2..1599cf5` (8 RSS commits). Scope stayed in RSS docs/code/tests plus `.gitignore`: OPML `FeedSource`, extended `FeedEntry`, `fetch-topics --opml`, `--with-fetch-report`, `list-feed-sources`, Inoreader read-only adapter, `rss-smoke`, sanitized live-smoke runbook, and RSS tests. No PR was created. No real OPML smoke, Inoreader live smoke, raw OPML, tokens, private feed URLs, article bodies, live smoke evidence, G-27 carrier/YMM4 writes, Baseball, Thumbnail, GUI gap audit, NotebookLM API, video generation, YouTube posting, DB sync, or background polling were added. Verification before and after merge: RSS narrow tests `41 passed`, full `uv run pytest` `525 passed, 25 skipped`, CLI help smoke for `main` / `fetch-topics` / `list-feed-sources` / `rss-smoke` all exit 0, and `git diff --check` clean. Restart from another terminal: `cd C:\Users\PLANNER007\NLMYTGen && git fetch --all --prune && git checkout master && git pull --ff-only origin master`; HEAD should be `1599cf5`. Next RSS action is optional live smoke only when the operator supplies real OPML at `_local/rss/feeds.opml` or a temporary `NLMYTGEN_INOREADER_ACCESS_TOKEN`; commit only sanitized evidence after review. Main project frontier remains G-27 `G27_PublicVsBrokerDB` carrier / slot-fill when the human-authored carrier is returned.
- **Layout Instruction Compliance Proof GUI pass confirmed; slice closed as diagnostic proof (2026-05-27)**: User opened `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen\samples\_probe\g24\layout_instruction_proof.ymmp` in YMM4 v4.52.0.8 after the spacing/label fix and reported that the previously flagged issues are all corrected: title text no longer appears bottom-aligned, title/grid gap is visible, and explanatory region labels are stable. Assistant-owned fix was commit `4631f89 fix(g27): stabilize layout instruction proof spacing`, updating only the diagnostic layout proof generator/artifacts: title font 60 with text center shifted 8px upward, title-grid gap 40px with readback check `title_grid_gap_visible`, grid cell height 172px, lower character bust placeholders while keeping the caption safe area clear, fixed top-left label anchors, and readback check `region_labels_clear_major_items`. Generated artifacts: `samples/_probe/g24/layout_instruction_proof.ymmp`, `layout_instruction_proof_readback.json`, `layout_instruction_proof_report.md`, and `layout_instruction_proof.html`. Machine readback: `status=passed`, 17 items, hard_fail=0, violations=[]; `node scripts\build_g27_layout_instruction_proof.js` no-write check passes. This closes Layout Instruction Compliance Proof as machine proof + YMM4 GUI proof only. It is not a render, creative acceptance, production carrier replacement, slot-fill readiness, or production readiness claim. Next frontier returns to G-27 `G27_PublicVsBrokerDB` carrier / slot-fill path under FEATURE_REGISTRY scope.
- **A-04 RSS master-integration branch pushed (2026-05-27)**: RSS work was rebuilt on `codex/rss-reader-sync-master-integrate` from latest `origin/master` and pushed to `origin/codex/rss-reader-sync-master-integrate`. The branch carries OPML source sync, fetch reports, Inoreader read-only input, live-smoke runbook, and `rss-smoke`; Baseball and G-27 side branches are not part of the diff. Reconciliation preserved the current `fetch-topics URL...` intake guard by validating positive `--limit` / `--timeout` before fetch, keeping direct URL fetch calls compatible, and passing `source=` only for OPML-derived feeds. Verification on this branch: RSS/CLI narrow tests `41 passed`, full `uv run pytest` `525 passed, 25 skipped`, and `git diff --check` clean. Next RSS action is either PR/merge of this branch, or live smoke with real OPML at `_local/rss/feeds.opml` / temporary `NLMYTGEN_INOREADER_ACCESS_TOKEN`; raw OPML, tokens, private feed URLs, and full article bodies stay out of git.
- **A-04 RSS clean-branch handoff recorded before master integration (2026-05-26)**: RSS work was first preserved on branch `codex/rss-reader-sync-clean`, pushed to `origin/codex/rss-reader-sync-clean`. Functional commits through `91b97f3` add OPML source sync, fetch reports, Inoreader read-only input, live-smoke runbook, and `rss-smoke` one-command sanitized evidence. Verification before that handoff: RSS narrow tests `35 passed`, full `uv run pytest` `519 passed, 25 skipped`, and `git diff --check` clean. The next RSS live smoke remains: place real OPML at `_local/rss/feeds.opml` or temporarily set `NLMYTGEN_INOREADER_ACCESS_TOKEN` and run the `rss-smoke` command from `docs/verification/RSS-LIVE-SMOKE-RUNBOOK-2026-05-26.md`. Only raw OPML export or temporary token acquisition remains manual; raw OPML, tokens, private feed URLs, and full article bodies must stay out of git.
- **A-04 RSS smoke automation added (2026-05-26)**: Added `rss-smoke` so the operator no longer has to manually combine source listing, article fetch, coverage counts, and sanitized evidence writing. Next RSS smoke command is `python -m src.cli.main rss-smoke --opml _local/rss/feeds.opml --format markdown -o docs/verification/RSS-LIVE-SMOKE-EVIDENCE-YYYY-MM-DD.md`; for Inoreader, temporarily set `NLMYTGEN_INOREADER_ACCESS_TOKEN` and run `rss-smoke --reader inoreader`. Manual work is reduced to exporting OPML or obtaining a temporary token, then comparing the generated count/category evidence with the human reader UI. Raw OPML, tokens, private feed URLs, and full article bodies remain non-committable.
- **A-04 RSS live-smoke entry point added (2026-05-26)**: Added `docs/verification/RSS-LIVE-SMOKE-RUNBOOK-2026-05-26.md` and ignored `*.opml` / `*.opml.xml` / `_local/rss/` so the next RSS action has a concrete path without risking raw RSS exports or tokens in git. The next RSS move is now: place real OPML at `_local/rss/feeds.opml`, run `list-feed-sources --opml ...`, then `fetch-topics --opml ... --with-fetch-report`; if the OPML flow is too manual, set `NLMYTGEN_INOREADER_ACCESS_TOKEN` temporarily and run the Inoreader smoke from the same runbook. Only sanitized counts and field-presence evidence should be committed.
- **A-04 RSS Reader Sync v1.1 implemented (2026-05-26)**: RSS work stayed in the A-04 lane and did not take over the G-27 mainline. The clean RSS branch was rebuilt from `origin/master` so Baseball sidequest commits are not part of the RSS diff. `fetch-topics --with-fetch-report` now exposes per-feed coverage (`fetched` / `empty` / `error` / `listed`, raw count, date-matched count, shown count) without changing the default JSON entry-list contract. A read-only Inoreader adapter maps `subscription/list` to `FeedSource` and `stream/contents` to `FeedEntry`, using only `NLMYTGEN_INOREADER_ACCESS_TOKEN`; no OAuth flow, refresh-token persistence, unread/read sync, subscription mutation, DB storage, background polling, GUI sync, or YMM4 behavior is added. Next RSS move requires operator-supplied real OPML or Inoreader token for live smoke; raw OPML/token must stay out of git, with only sanitized evidence recorded.
- **A-04 RSS Reader Sync v1 implemented (2026-05-25)**: RSS input acquisition now supports OPML as the shared source of truth between the human RSS reader list and AI-side article fetching. Added `FeedSource`, OPML parsing, `fetch-topics --opml`, `fetch-topics --format markdown`, and `list-feed-sources --opml --format markdown|json`. `FeedEntry` remains backward-compatible with `title` / `published` / `source_url` and now carries article URL, summary, source title, and source categories. New canonical context lives in `docs/RSS_READER_SYNC_SPEC.md`; Inoreader remains a later read-only adapter candidate only, with no OAuth, token storage, unread/read sync, DB, subscription mutation, or background polling in this slice. This does not change G-27, YMM4, production artifacts, auth/API contracts, dependencies, or NotebookLM boundaries. Next RSS move, when desired: export OPML from the chosen reader, run `list-feed-sources --opml <feeds.opml>` to compare the human/AI list, then `fetch-topics --opml <feeds.opml> --format markdown|json` for article candidates.
- **Layout Instruction Compliance Proof landed at b0bb1fd; previous A/B/C scene-level proof candidates are superseded (2026-05-22)**: User redirected the next lane away from the previously recorded scene-level proof options (A minimal sub-labels / B full per-card labels / C group-rolled labels) toward a Layout Instruction Compliance Proof that verifies whether a fixed natural-language layout instruction set converts to a stable YMM4 layout, independent from the existing diagnostic carrier. Implemented in commit b0bb1fd as a separate slot/region proof, not a scene composition. Inputs (fixed by user): 16:9 / 1920x1080, upper title band with 18-char maximum slot assumption, center 2x2 grid with visible cell boundaries, left-bottom + right-bottom shoulders-up character bust placeholders (ShapeItem only), bottom 20% caption safe area kept empty of major items, minimal region labels for title / grid / character / caption safe area. New generators added under scripts/: `build_g27_layout_instruction_proof.js` (17 items / ShapeItem=11 / TextItem=6 / 13 instruction_compliance checks) and `render_g27_layout_instruction_proof_html.js`. Generated artifacts under `C:\Users\PLANNER007\NLMYTGen\samples\_probe\g24\`: `layout_instruction_proof.ymmp`, `layout_instruction_proof_readback.json`, `layout_instruction_proof_report.md`, `layout_instruction_proof.html`. Readback: `status=passed`, 17/17 items present, missing=0, hard_fail=0, violations=[]; all 13 instruction_compliance fields pass (canvas_16_9_1920_1080, title_band_top, title_slot_width_for_18_chars, grid_2x2_cells, grid_boundary_visible, char_a_bust_left_bottom, char_b_bust_right_bottom, bust_up_no_intrusion_into_caption_safe, caption_safe_area_empty_of_major_items, region_labels_present, caption_indicator_present, shape_size_mode_widthheight, color_format_aarrggbb). Slot summary: title band 1728x86 at cy=-443 with font 64 (current text 12 chars / slot width 715px for 18-char assumption); 2x2 grid 4 cells ~856x192 at cy=-292 / cy=-108 with alternating fill (#E7ECF1 / #CFD8E0) and 16px gap; character A bust at cx=-700 (head 140x160 round=70 at cy=70 + shoulders 280x100 round=20 at cy=210); character B bust at cx=+700 with identical geometry; caption safe area cy=324..540 (216px = 20%) with thin top-edge indicator. Diagnostic carrier (`real_estate_dx_diagnostic_carrier.ymmp` at fc65ded) is untouched and not decorated. Do not progress to A/B/C card labeling, do not decorate the existing split carrier, do not add new spec docs / SCS v0.2 / capability matrix audit / verification cleanup / new capture infrastructure / render / creative acceptance / production carrier replacement. Next user action: open `C:\Users\PLANNER007\NLMYTGen\samples\_probe\g24\layout_instruction_proof.ymmp` in YMM4 and return a preview screenshot. ymm4_gui_screenshot remains MANUAL_REQUIRED (no repo auto-capture).
- **G-27 diagnostic carrier YMM4 pass confirmed at fc65ded; closing this slice, next lane is scene-level proof on the same split composition — SUPERSEDED by 2026-05-22 Layout Instruction Compliance Proof entry above (2026-05-21)**: User shared a fresh YMM4 v4.52.0.7 preview screenshot of `C:\Users\PLANNER007\NLMYTGen\samples\_probe\g24\real_estate_dx_diagnostic_carrier.ymmp` at frame 0 (1920x1080 / 60fps) after the cards-visibility bug fix (6e7e1e6) and the double-pillar gate fix (fc65ded). All 7 viewing axes pass on the actual YMM4 render: (1) `情報の非対称性` title is read as upper concept distinct from `公開ポータル` / `業者DB` panel titles; (2) left blue + right purple focal anchors are clearly distinct; (3) the two amber pillars at center read as a gate / double-pillar barrier, no longer as a human silhouette; (4) cards are visible inside both panels (no whiteboard regression); (5) lower 18-22% caption safe area remains empty; (6) in-frame label count = 3, characters within 30; (7) overall density 14 elements stays within SCS §3 [8,14]. G-27 diagnostic carrier slice is closed here. The diagnostic carrier remains diagnostic-only; production carrier creation by the user, render, creative acceptance, production timing, and production readiness claims are still out of scope. New YMM4 rendering knowledge gained this slice (preserve as carry-forward): `ShapeParameter.Round` is interpreted as corner radius px (e.g. round=70 with 140x160 reads as ellipse, round=4 with thin pillar reads as sharp gate post); a body+shackle pair tends to read as human silhouette and is now reusable as the SCS §2.5 mediator template; ShapeItem 1:13 aspect double-pillars at cx=±20 read as a closed gate; `isHidden=true` argument position is the 13th positional argument of `shape()` and is easy to misset. Next lane (separate slice, not started this block): scene-level proof on the same split composition — give the 5 cards concrete information labels representing 公開ポータル side (visible info) vs 業者DB side (hidden info), establish a left→center→right reading order, and verify on a fresh YMM4 screenshot that the asymmetry reads at 1-second glance. Three scope candidates are pre-evaluated against SCS §3 element-count upper bound 14 and §4.3 in-frame text budget 30 chars: (A) minimal — add `G27PBD_PublicSubLabel` (見える情報 / 4 chars) and `G27PBD_BrokerSubLabel` (見えない情報 / 6 chars) only, total elements 16 (§3 strict +2 as spec_ambiguity), in-frame text ~27 chars (§4.3 OK), labels 5 (§4.3 strict +3 already spec_ambiguity); (B) full per-card — add 5 TextItem labels of 4-6 chars each onto every card, total elements 19 (§3 strict +5 as spec_ambiguity), in-frame text near 30 chars boundary, labels 8 (§4.3 strict +6 already spec_ambiguity); (C) group-rolled — group the 2 public cards and the 3 broker cards into two Group items and attach one label per group, total elements stays close to 14, in-frame text moderate, labels +2 only. Recommended default for next slice is (A) for risk-minimal first pass; (C) is the cleanest spec-compliant option but requires touching the Group plumbing in build_g27_diagnostic_carrier.js; (B) is the highest-density option and intentionally tolerates spec_ambiguity records. All three options stay diagnostic-only and require a single YMM4 screenshot round-trip for visual verification (1 manual screenshot expected, MANUAL_REQUIRED). Restart at another terminal: `git fetch --all --prune && git checkout codex/g24-nod-sync-adoption && git pull --ff-only`; HEAD should land at `843b001`; primary read targets are this entry, `docs/SCENE_COMPOSITION_SCHEMA.md`, `docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md`, `scripts/build_g27_diagnostic_carrier.js`; next assistant-owned action awaits user pick of A / B / C and then implements only that one option (no docs additions, no SCS v0.2, no audits, no cleanups). Frozen: SCS v0.2, capability matrix audit, verification notes cleanup, new capture infrastructure, AutoHotkey / UI Automation, render, creative acceptance, production carrier replacement, production readiness claims.
- **G-27 diagnostic carrier `ymm4_gui_screenshot` received; 2 issues found, fix not yet applied (2026-05-20)**: User opened `samples/_probe/g24/real_estate_dx_diagnostic_carrier.ymmp` in YMM4 v4.52.0.7 at frame 0 (00:00.00, 1920x1080 / 60fps) and shared the preview screenshot via chat (not committed to repo). Visual evaluation of the 7 SCS-derived viewing axes against the actual YMM4 render produced two reproducible failures and five passes. Failure 1: all five `G27PBD_*Card*` items render hidden because `build_g27_diagnostic_carrier.js` mistakenly passes `isHidden=true` as the 13th positional argument to `shape()` for `PublicCard1` / `PublicCard2` / `BrokerCard1` / `BrokerCard2` / `BrokerCard3`; the Arrow hidden=true is intentional but the five cards are an assistant-side bug. As a result the timeline still lists the card items but the preview shows empty panels and the visible-item count drops to 8 (= SCS §3 lower bound). Failure 2: `G27PBD_Lock` + `G27PBD_Lock_Shackle` render as a human silhouette rather than a key / wall / threshold because YMM4 draws ShapeItem `Round` as a corner radius, so the body (200x200, round=32) looks like a torso and the shackle (140x160, round=70 ≒ ellipse) looks like a head; this is closer to SCS §2.5 mediator composition than the boundary requested by `G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md`. Five axes still pass: title concept legibility (情報の非対称性), left/right focal_anchor distinctness, anti-whiteboard, caption clearance, in-frame label budget. Overall judgement: fix required (not reject). No carrier / readback / proof / capture script was modified this block; HEAD remains cf94453 and `origin/codex/g24-nod-sync-adoption` is at `0 0`. Bug fix (Failure 1) is assistant-owned and requires no design judgement: flip the five card `isHidden` arguments from true to false in `scripts/build_g27_diagnostic_carrier.js`, regenerate via `node scripts/build_g27_diagnostic_carrier.js --write` and `node scripts/render_g27_diagnostic_carrier_html_proof.js`, then request a fresh `ymm4_gui_screenshot`. Lock shape change (Failure 2) involves design judgement (keep key intent, switch to thin vertical wall, switch to gate posts, or remove and keep negative space) and is held until the post-bug-fix screenshot confirms whether cards-visible + current lock still reads as mediator. Do not progress to v0.2 SCS, new spec docs, capability matrix audit, verification cleanup, new capture infrastructure, AutoHotkey / UI Automation, render, timing tuning, creative acceptance, production carrier replacement, or production readiness claims; keep the original two-step plan from the previous closeout (user `ymm4_gui_screenshot` → up to two fixes).
- **Scene Composition Schema v0.1 added (2026-05-18)**: G-27 の各 probe (`visual_proxy_v2*`, `micro_scene_probe`, `micro_scene_visibility_probe`, `primitive_visibility_calibration_probe`) が openability=pass / readback=pass でも "indexed whiteboard" / "drawing-semantics calibration" 止まりだった失敗を構図設計の rule violation として分類するため、`docs/SCENE_COMPOSITION_SCHEMA.md` を新規追加した。SCS は 1 frame の静止構図 (画面領域分割 + 要素の役割割当 + 要素生成則) を実行可能な手順として固定する。範囲は §1 Composition Grid (1920×1080 を outer safe band / title band / main canvas / caption safe area に固定分割)、§2 五つの composition types (`split` / `center-focal` / `chain` / `reveal` / `mediator`) と明示的 anti-pattern (`indexed_whiteboard` / `grid_overload` / `narrative_strip` / `drawing_semantics_calibration`)、§3 visual role vocabulary (`focal_anchor` / `supporting` / `boundary` / `connector` / `risk_marker` / `decoration` / `label` と要素数上限 8-14 / frame)、§4 reading order と typography hierarchy (FontSize hierarchy + in-frame text budget 30 字)、§5 element primitive rules (ShapeItem の `SizeMode=WidthHeight` 必須化、color の string 形式必須、ImageItem の Windows path 必須)、§6 Beat → composition type mapping の機械的手順、§7 sidecar compliance fields (`composition_type` / `visual_roles` / `element_count` / `reading_order` / `shape_size_mode_check` / `color_format_check` / `composition_violations`)、§8 過去 G-27 probe の失敗再分類、§9 adapter patch boundary を SCS 文脈で再表記、§10 適用順序、§11 適用範囲。`docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md` (carrier = `split` composition type)、`docs/G27_REVIEW_CONSOLE_SPEC.md` (Visual Direction / Shot Layout Contract 実装手順は SCS が正本)、`docs/PRODUCTION_PIPELINE_CONTRACT.md` (Shot Layout Plan stage の schema は SCS、compliance check は SCS §7)、`docs/FEATURE_REGISTRY.md` (G-27 行に SCS を正本として列挙) と相互リンク済み。docs only / src/ 変更なし / pytest 未実行 (前回 2026-05-15 で 499 passed / 25 skipped を引き継ぎ)。これは G-27 carrier 待ちの間の assistant-owned docs slice であり、carrier readback / anchored slot contract / render / production timing / creative acceptance を authorize しない。次の自然な動きは (a) user が `G27_PublicVsBrokerDB` carrier を YMM4 で作って返す (carrier checklist + SCS §2.1 split に準拠)、(b) carrier 受領後に assistant が readback + anchored slot contract を SCS §7 compliance を出した形で準備、(c) 別レーンでは G-20 残スライス (face_map_bundle 整合チェック) や `PRODUCTION_IR_CAPABILITY_MATRIX.md` / `TIMELINE_EFFECT_CAPABILITY_ATLAS.md` の最新化監査が assistant-owned で進められる。
- **Restart handoff / clean remote sync preserved (2026-05-15)**: Local branch `codex/g24-nod-sync-adoption` was clean and equal to `origin/codex/g24-nod-sync-adoption` before this handoff update. The restart analysis ran `uv run pytest` with `499 passed, 25 skipped`; no code, dependency, DB/auth/API contract, or generated YMM4 artifact changed in that analysis slice. Current working map is `docs/FEATURE_REGISTRY.md`, `docs/INVARIANTS.md`, `docs/PRODUCTION_IR_CAPABILITY_MATRIX.md`, `docs/TASK_DEVELOPMENT_CYCLE_SPEC.md`, and `docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md`. G-27 remains the mainline: direct semantic `ShapeItem` / `TextItem` scene generation is diagnostic-only, production readiness remains no, and the next real move is human-authored `G27_PublicVsBrokerDB` carrier creation. After the user returns the carrier `.ymmp` path plus preview/timeline/property screenshots and light/dark stage choice, assistant should run readback, verify required `G27PBD_*` items, short Remarks, fixed public/broker card counts, and retained `G27PBD_Arrow`, then prepare an anchored slot contract. Do not proceed to raw geometry generation, another visual proxy or micro scene, render, production timing, creative acceptance, G-26, sports_news, INT-02e, publishing, or master integration unless explicitly re-scoped. Known open/blocked work: G-27 carrier + slot-fill, G-26 motion calibration, H-01 automatic injection / score closed loop, H-02 real thumbnail template proof, INT-02e real URL smoke, YouTube/OAuth, F-01/F-02 quarantined GUI, and Baseball animation/export proof.
- **G-27 PublicVsBrokerDB human-authored carrier checklist ready (2026-05-14)**: Added `docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md` as the single handoff artifact for the next human YMM4 step. It specifies the stable carrier requirements for `G27_PublicVsBrokerDB`: 16:9 / 1920x1080, 5% outer safe margin, bottom 10-15% caption safe area, left public panel, right broker/private DB panel, center lock/threshold, fixed public card count 2, fixed broker card count 3, optional arrow item retained as `G27PBD_Arrow`, short `G27PBD_*` item names, short Remarks only, and detailed provenance kept out of YMM4 item names/Remarks. This does not create a `.ymmp`, slot contract, raw geometry, patch script, render, gate, roadmap, or production output. The next step is human-side YMM4 carrier creation; after the user returns the carrier `.ymmp` path plus preview/timeline/property screenshots and light/dark stage choice, assistant should perform readback and only then prepare an anchored slot contract.
- **G-27 template-first / slot-fill correction accepted (2026-05-13)**: Stop the route where the agent directly generates dense `ShapeItem` / `TextItem` scene layouts from semantic intent. The current classification is: `.ymmp` generation technically possible, YMM4 openability possible, ShapeItem/TextItem insertion possible, but direct semantic scene layout generation is not production-reliable; minimal render readiness=no and production readiness=no. Visual proxy v2/v2.1, the minimal patched probe, the micro scene probe, and the micro scene visibility probe are diagnostic-only evidence, not a production route and not a basis for v2.2 / v2.3. Reusable G-27 assets are the adapter IR dry-run, compact patch review, minimal `.ymmp` / openability probes, readback tooling, FontColor/schema checks, and primitive calibration findings. The next actionable slice is preparation only for `G27_PublicVsBrokerDB` template-first slot-fill, anchored to a stable YMM4 carrier template. If no existing carrier `.ymmp` can be identified, stop and ask for a human-authored carrier; do not generate raw geometry as a substitute. Slot-fill may patch only text, visibility, timing, and sidecar provenance id. It must not patch panel geometry, anchors, colors, font hierarchy, or layout grid. Do not create another visual proxy, another micro scene, render output, broad roadmap, new gate/policy, G-26, sports_news, INT-02e, publishing, or master integration.
- **G-27 primitive visibility calibration probe ready for user-side YMM4 GUI readback (2026-05-13)**: User-side YMM4 GUI review of the previous G-27 micro scene visibility probe now classifies openability=pass, machine readback=pass, and timeline generation=pass, but preview visibility / visual composition / scene adequacy=fail and minimal render readiness=no. Treat this as a YMM4 primitive geometry, tonal-system, and authoring-surface calibration problem, not as a request for more cards, labels, beats, or scene variants. Added `scripts/build_g27_primitive_visibility_calibration_probe.js` and generated `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe.ymmp`, `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe_readback.json`, and `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe_report.md`. This is a drawing-semantics calibration probe only: 11 items, ShapeItem=6, TextItem=5, one light-stage tonal system, full-screen BG, 920x560 `Main Panel`, panel-contained title/body text, center/TL/BR anchor markers, one thick connector, `ShapeParameter.SizeMode=WidthHeight`, non-zero `StrokeThickness` for visible shapes, opacity=100, item-name failures=0, Remark-length failures=0, suspicious default count=0, carrier modified in place=false. The existing micro scene probe was not advanced in this slice. Minimal render smoke remains blocked until this calibration passes user-side YMM4 GUI inspection. Do not proceed to render, creative acceptance, production timing, external assets, TTS, URL fetch, publishing, sports_news, G-26, INT-02e, master integration, new gates, policies, roadmaps, dry-runs, visual atlases, or another micro scene variant.
- **G-27 micro scene visibility probe ready for user-side YMM4 GUI readback (2026-05-13)**: User-side YMM4 GUI review of `samples/_probe/g24/real_estate_dx_micro_scene_probe.ymmp` returned openability=pass and timeline placement=pass, but scene visibility=fail and minimal render readiness=no. Root cause was visibility/composition rather than file generation: ShapeItems inherited `SizeMode=SizeAspect`, `Size=100`, and `AspectRate=0`, so intended large panels collapsed into small low-density marks. Updated `scripts/build_g27_micro_scene_probe.js` to generate a bounded visibility-fix output while keeping the same 4 beats, same source references, same 60 sec structure, ShapeItem/TextItem only, and narrative intent / visual composition / on-screen copy separation. New artifacts: `samples/_probe/g24/real_estate_dx_micro_scene_visibility_probe.ymmp`, `samples/_probe/g24/real_estate_dx_micro_scene_visibility_probe_readback.json`, and `samples/_probe/g24/real_estate_dx_micro_scene_visibility_probe_report.md`. Readback is `status=passed`: 57 inserted items, ShapeItem=44, TextItem=13, beat_count=4, duration_sec=60, missing=0, malformed=0, color-like failures=0, `shape_size_mode=WidthHeight`, old 100px fallback count=0, each beat has at least one focal panel and visible relation elements. Minimal render smoke remains not ready until user GUI review confirms the visibility fix. Do not proceed to render, creative acceptance, production timing, external assets, TTS, URL fetch, publishing, sports_news, G-26, master integration, new gates, policies, roadmaps, dry-runs, or visual atlases.
- **G-27 micro video scene probe ready for user-side YMM4 GUI readback (2026-05-12)**: The latest slice stopped at confirmation/readback handoff after converting the 7-candidate visual proxy catalog into one bounded 4-beat / 60 sec narrative scene. Added `scripts/build_g27_micro_scene_probe.js` and generated `samples/_probe/g24/real_estate_dx_micro_scene_probe.ymmp`, `samples/_probe/g24/real_estate_dx_micro_scene_probe_readback.json`, and `samples/_probe/g24/real_estate_dx_micro_scene_probe_report.md`. The micro scene uses only existing G-27 material and YMM4 `ShapeItem` / `TextItem` primitives: `RE-02-development` public portal vs broker DB contrast, `RE-06-development` property comparison / selection, `RE-07D-beginning` AI match, and `RE-07D-development` risk interruption / conditional recommendation. Readback is `status=passed`: 54 inserted items, ShapeItem=38, TextItem=16, beat_count=4, duration_sec=60, missing=0, malformed=0, color-like failures=0, carrier modified in place=false, external assets=false, render=false, creative acceptance=false. `RE-02-turn` remains blocked outside this output and `RE-07D-turn` remains deferred outside this output. Next safe move from another terminal is to open `samples/_probe/g24/real_estate_dx_micro_scene_probe.ymmp` in YMM4 and judge whether it now feels like a short scene rather than an indexed whiteboard; if GUI readback passes, the next bounded implementation slice is minimal render smoke, otherwise make a visual-local fix to the same 4-beat scene only. Do not proceed to creative acceptance, production readiness, TTS, URL fetch, publishing, sports_news, G-26, broad hardening, or render before that GUI judgment.
- **G-27 visual proxy iteration and YMM4 color schema fix preserved (2026-05-12)**: The minimal patched probe originally failed in YMM4 because `TextItem.FontColor` was written as a JSON color object where YMM4 expected a string; `scripts/build_g27_minimal_ymmp_probe.js` now writes YMM4-compatible string color values and its readback records the schema-risk scan. After the fixed minimal probe opened, two visual proxy catalog probes were generated for evidence: `samples/_probe/g24/real_estate_dx_visual_proxy_v2_probe.*` and `samples/_probe/g24/real_estate_dx_visual_proxy_v21_probe.*`. User GUI review classified v2/v2.1 as technically openable and semantically useful but still too much like a sticky-note / indexed whiteboard board, so the current frontier intentionally moved away from adding more labels/cards and toward the micro-scene probe above.
- **INT-02e real URL operator smoke gate fixed (2026-05-11)**: INT-02e is `baseline / in_progress`, not done. Done requires real URL operator-smoke evidence: actual fetch after URL + rights/terms review, Python `wave` readback of `source.wav`, receipt / sidecar / `material_ledger` readback, `audit-material-ledger`, boundary grep, and scrubbed URL / command / stderr / receipt reporting. Before smoke, record target commit, clean `git status --short`, and `HEAD...origin/main = 0 0`; if `origin/main` is unavailable or not `0 0`, stop before real fetch. Do not expand to `fetch-source-video`, GUI fetch button, STT URL fetch, cut/concat, subtitle burn-in, render/encode, or Publishing/OAuth.
- **G-27 minimal patched `.ymmp` probe generated (2026-05-12)**: Added `scripts/build_g27_minimal_ymmp_probe.js` and generated `samples/_probe/g24/real_estate_dx_minimal_patched_probe.ymmp`, `samples/_probe/g24/real_estate_dx_minimal_patched_probe_readback.json`, and `samples/_probe/g24/real_estate_dx_minimal_patched_probe_readback.md` from the existing compact patch review. The probe uses a copied carrier shape and contains only the 7 ready compact-review candidates: 21 inserted probe items, ShapeItem=14, TextItem=7, candidate ids found=7/7, layers found=7/8/9, missing=0, malformed=0, and the source carrier hash is unchanged. Next safe move is YMM4 GUI readback / preview of this probe file. No render, production timing, creative acceptance, TTS, URL fetch, publishing, sports_news, or pipeline hardening was performed.
- **G-27 YMM4 compact patch review generated (2026-05-12)**: Added `scripts/build_g27_ymmp_compact_patch_review.js` and generated `samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.{json,md}` from the existing 7-candidate adapter IR dry-run. The compact review lists intended YMM4 item type, layer, compact-review start/duration, required proxy primitive, source placeholder, visible effect, and patch-output readiness for each candidate. Result: 7/7 candidates are ready for actual `.ymmp` patch output in a separate minimal patched `.ymmp` slice; blocked/deferred count among the 7 is 0. `RE-02-turn` remains excluded/blocked and `RE-07D-turn` remains excluded/deferred outside the 7. No real `.ymmp` file, YMM4 patch output, readback, preview, render, production timing, or creative acceptance was created.
- **G-27 adapter IR dry-run generated (2026-05-12)**: User authorized `authorize_adapter_IR_dry_run_for_7_candidates_only`; added `scripts/build_g27_adapter_ir_dry_run.js` and generated `samples/_probe/g24/real_estate_dx_adapter_ir_dry_run.{json,md}`. The dry-run contains 7 source beats with route types, resolved proxy/template primitives, forbidden representation checks, `YMM4_patch_readiness`, and blocked reasons. Result: 7/7 candidates are ready for next `.ymmp compact review` and 7/7 are patch-output candidates after a separate output authorization; `RE-02-turn` remains blocked and `RE-07D-turn` remains deferred. No YMM4 patch, `.ymmp`, preview, render, production timing, or creative acceptance was created.
- **G-27 adapter authorization gate added (2026-05-12)**: Added `scripts/check_g27_adapter_authorization_gate.js` plus `samples/_probe/g24/real_estate_dx_adapter_authorization_gate.{json,md}` as the current decision surface after route preflight. The gate fixes 7 adapter IR dry-run candidates, keeps `RE-02-turn` `excluded_until_adjusted`, keeps `RE-07D-turn` `deferred_blocks_adapter_planning`, and preserves `output_generation_allowed=false` / `authorization_granted=false`. It does not create adapter IR, YMM4 adapter output, `.ymmp` patch/write, render, production timing, or creative acceptance. The next gate is an explicit user or validator response; the recommended response is `authorize_adapter_IR_dry_run_for_7_candidates_only`, which would unlock only the next dry-run contract slice, not YMM4 output.
- **G-27 adapter route preflight report added (2026-05-11)**: Added `scripts/check_g27_adapter_route_preflight.js` and `samples/_probe/g24/real_estate_dx_ymm4_adapter_route_preflight.{json,md}` as the machine preflight for `docs/G27_ADAPTER_ROUTE_CONTRACT.md`. The report passes the planning-zone gate for 7 route-planning candidates, keeps `RE-02-turn` `excluded_until_adjusted`, keeps `RE-07D-turn` `deferred_blocks_adapter_planning`, and preserves `output_generation_allowed=false`. This does not create adapter IR, YMM4 adapter output, `.ymmp` patch/write, render, production timing, or creative acceptance. Next gate is user or validator authorization before adapter IR or patch output.
- **Yukkuri mainline / Baseball sidequest boundary (2026-05-10)**: Reaffirmed that NLMYTGen's mainline is Yukkuri explainer video production, not Baseball. Baseball Info / `sports_news` remains a large explicit sidequest that must not replace the primary `next_action`; start it by saying so in chat, not by adding a prompt-only md file. The Baseball cycle still starts from screen plan first, but closeouts must separate what stays in the Baseball lane from what returns to the Yukkuri mainline.
- **Task development cycle spec and G-24 close split (2026-05-10)**: Added `docs/TASK_DEVELOPMENT_CYCLE_SPEC.md` as the single owner for task-level improve/review/decision/next-artifact cycles. G-24 is now closed as the template-first `skit_group` foundation; Real Estate DX-specific cast/props gaps, proxy decisions, and scene-level review loop move to G-27. Baseball Info now starts from a screen plan review unit before renderer/export/YMM4 proof, and GUI/YMM4 review surfaces must be selected per task instead of scattered across docs and artifacts.
- **AGENTS / global Codex rule anti-growth cleanup (2026-05-10)**: Compressed NLMYTGen `AGENTS.md` into a thin entry pointer with an explicit anti-growth rule. Detailed daily rules stay in `docs/REPO_LOCAL_RULES.md`, current state in this file, decision/handoff history in `docs/project-context.md`, and interaction/reporting failure modes in `docs/INTERACTION_NOTES.md`. Global Codex `C:\Users\thank\.codex\AGENTS.md` was also reduced to fallback-only guidance, global prompt helpers were de-authorized as repo authority, and the stale command allowlist at `C:\Users\thank\.codex\rules\default.rules` was emptied after archiving to `C:\Users\thank\.codex\archived_rules\default.rules.legacy-2026-05-10.txt`. This is authority cleanup only; it does not change Real Estate DX validator status or sports_news backlog.
- **Repo-local rule cleanup complete; return to Real Estate DX review (2026-05-10)**: `docs/REPO_LOCAL_RULES.md` is now a short front-door, hook/generated-handoff wording uses natural next-action language, and the remaining old closeout-label hits are intentionally limited to deauthorization wording plus negative tests. No additional rule-cleanup slice is recommended unless a new response or hook failure reintroduces fixed labels. The next content move is back to the active Real Estate DX overlay/card design review and then G-27 gap reporting; this does not change Real Estate DX validator authority or sports_news backlog priority.
- **sports_news lane foundation recorded (2026-05-09)**: Added the `lanes/sports_news/` MVP artifact bundle and anchored it from `docs/BASEBALL_NEWS_PIPELINE_SPEC.md` as a parallel text/data/source-driven sports-news lane. The bundle is intentionally schema/docs/examples/templates only: no renderer, no network scraping, no asset-acquisition automation, and no ClipPipeGen integration. Rights/provenance gates are publish/asset-ingest checks and must not veto core card design work.
- **Real Estate DX overlay-only compact review receiving guardrail (2026-05-08)**: Hardened the local Stop-hook/repo contract for the artifact set produced by the parallel lane. A generated `overlay_only_compact_review` closeout now has to include the literal keys `artifact path: ...`, `readback result: ...`, `allowed_next_actions: [overlay_only_compact_review]`, `forbidden_next_actions: [cast_motion_ir, ymm4_creative_acceptance, production_timing]`, `remaining blockers: [...]`, and `not creative acceptance`. Snake_case `overlay_only_compact_review` and humanized labels like `Validator allowed` / `Forbidden` are now detected, so the closeout cannot bypass the validator contract by avoiding machine-readable keys.
- **Real Estate DX overlay-only compact review generated (2026-05-08)**: Executed the only validator-authorized next action from the background skit artifact set. Generated `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.html`, `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.ymmp`, `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.json`, and `samples/_probe/g24/real_estate_dx_overlay_only_compact_review_readback.json`. Readback result is `status=passed`: `11` compact segments, `24` placeholder items rendered, and the YMM4 carrier contains `ShapeItem=24` only, with no `skit_group:` remarks and no `delivery_` template reuse. Validator authority remains `samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json`: `status=blocked`, `errors=[]`, `allowed_next_actions=[overlay_only_compact_review]`, `forbidden_next_actions=[cast_motion_ir, ymm4_creative_acceptance, production_timing]`. Remaining blockers are `ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING` and `ASSET_BLOCKED_REAL_ESTATE_PROPS_MISSING`. This compact review is not creative acceptance, not production timing, and not cast motion IR; it is ready for user-side integration review.
- **Real Estate DX GUI design review surface (2026-05-10)**: The active user-facing review target is the GUI `デザインレビュー` tab, not another scattered Markdown handoff. The dense English memo remains evidence/fallback detail only; normal review should happen in the GUI with a small decision set around metaphor strength, visual density, RE-07 grouping, wording risk, and whether to move directly to asset/proxy gap reporting. HTML remains a preview surface, JSON/readback remains machine proof, and the lane remains not creative acceptance; it does not unlock cast motion IR, YMM4 creative acceptance, or production timing.
- **G-27 Review Console contract fixed (2026-05-10)**: Added `docs/G27_REVIEW_CONSOLE_SPEC.md` as the owner for the GUI-centered G-27 review workflow. The GUI `デザインレビュー` tab now uses `samples/_probe/g24/real_estate_dx_review_packet.json` as the decision input and saves `samples/_probe/g24/real_estate_dx_review_decisions.json` as the machine-readable handback. `samples/_probe/g24/real_estate_dx_overlay_card_review_map.md` is evidence/fallback detail only. This remains within approved G-27 and is not F-01/F-03 revival, YMM4 preview emulation, image generation, video generation, or asset acquisition.
- **G-27 Review Console v1.1 script context added (2026-05-10)**: The GUI review packet now carries episode context, story outline, per-segment script span, script excerpt, previous context, next context, and scene role. The GUI `デザインレビュー` tab renders those layers before the decision controls, so user review no longer depends on reading dense Markdown or judging isolated overlay/card cards without the source script arc. This is still overlay/card decision support only and does not unlock cast motion IR, YMM4 creative acceptance, or production timing.
- **G-27 Review Console v1.2 timeline workbench added (2026-05-11)**: The GUI `デザインレビュー` tab is now a full-width Review Workbench instead of a card list inside the production wizard. The left wizard is hidden only on this tab, the review packet renders as an RE-01〜RE-07E timeline, the selected segment shows script/context/risk/next-effect detail, and the decision inspector preserves the existing `review_decisions.json` schema. User review should resume here; Markdown/HTML remain evidence and preview only.
- **G-27 overlay compact screenshot route added (2026-05-11)**: Browser Use rejects local `file://` preview, so `gui/capture_overlay_compact_review.js` now owns the developer-side visual evidence route. It opens `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.html` with Electron `BrowserWindow.loadFile`, validates readback `passed`, confirms 11 DOM segments and 24 placeholder cards, checks remaining blockers against the validator, and writes `samples/_probe/g24/real_estate_dx_overlay_only_compact_review_screenshot.png` plus `samples/_probe/g24/real_estate_dx_overlay_only_compact_review_screenshot_readback.json`. This is still placeholder visibility proof only, not creative acceptance.
- **G-27 visual storyboard proof added (2026-05-11)**: The overlay compact HTML was accepted as generation/DOM proof but not as a useful video proxy. Added `gui/capture_visual_storyboard_proof.js` and `npm --prefix gui run capture:g27-visual-storyboard` to generate a separate `visual_proxy_proof`: `samples/_probe/g24/real_estate_dx_visual_storyboard_proof.png` plus `samples/_probe/g24/real_estate_dx_visual_storyboard_proof_readback.json`. The proof is a 3×4 contact sheet with one 16:9 proxy keyframe per RE-01〜RE-07E segment, using proxy visuals for people, property documents, SNS screens, contracts, warning UI, AI panels, gates, and curation tables. It remains not creative acceptance and does not unlock cast motion IR or production timing.
- **G-27 visual direction / shot layout contract fixed (2026-05-11)**: `samples/_probe/g24/real_estate_dx_visual_storyboard_proof.png` is now explicitly diagnostic-only Evidence Layer output. It must not be used as a production input, production template, YMM4 source, render source, production timing source, or creative acceptance substitute. `docs/G27_REVIEW_CONSOLE_SPEC.md` now separates Evidence / Visual Direction / Shot Layout / Motion-Timing layers, fixes the 16:9 production-frame contract, and records 3-beat visual treatments for RE-02, RE-06, and RE-07D. The next work is a small visual treatment proof for those 3 segments × 3 beats, not full production implementation.
- **G-27 production design spine fixed (2026-05-11)**: User-facing review is now explicitly centralized in the GUI timeline. HTML / PNG / JSON are evidence artifacts or machine-readable inputs, not independent review surfaces. `docs/G27_REVIEW_CONSOLE_SPEC.md` separates NotebookLM script, Script Beat IR, Visual Direction Contract, Shot Layout Plan, Motion Beat Plan, proof artifacts, Review Decisions, and YMM4 Adapter Output. Follow-on visual proof slices must either be visible in the GUI or define a GUI read-only ingest path; raw HTML/PNG/JSON confirmation alone must not close a user-review slice.
- **G-27 9-frame visual treatment proof v2 GUI ingest added (2026-05-11)**: Updated `samples/_probe/g24/real_estate_dx_visual_treatment_proof.{json,html,png}` and `samples/_probe/g24/real_estate_dx_visual_treatment_proof_readback.json` for RE-02 / RE-06 / RE-07D only. v2 keeps the GUI `デザインレビュー` timeline as the review surface, strengthens label-off readability with non-text proxy shapes, adds real-estate texture such as property cards, broker DB rows, public portal output, drawback cards, boundary maps, inheritance nodes, and neighborhood markers, and records enter / move / emphasize / reveal / dim actions in the sidecar. The GUI proof panel displays the proof image, beat table, narration cue, motion primitives, sidecar warnings, Frame Contract violation count, anti-pattern corpus, additional checks, and read-only decision context. `Modern_Real_Estate_Strategic_Playbook.pdf` remains anti-pattern-only; it is not a production asset or layout reference. GUI proof visibility is captured at `samples/_probe/g24/real_estate_dx_gui_treatment_detail_screenshot.png` with readback `samples/_probe/g24/real_estate_dx_gui_treatment_detail_screenshot_readback.json`. Standalone HTML/PNG/JSON confirmation remains evidence only and does not complete user review.
- **Production Pipeline Contract extracted from G-27 (2026-05-11)**: Added `docs/PRODUCTION_PIPELINE_CONTRACT.md` to generalize G-27 lessons into a repeatable factory contract. The contract fixes the stage chain from NotebookLM script through Script Beat IR, Visual Direction Contract, Shot Layout Plan, Motion Beat Plan, GUI Review, Review Decisions, Scene Decision Packet, Asset/Proxy Gap Report, and YMM4 Adapter Output; defines artifact authority for GUI / HTML / PNG / JSON / docs / YMM4 / PDF; and records a three-topic smoke plan for Real Estate DX, AI monitoring labor, and Baseball news. This is docs-only. It does not start G-27 v3, scene decision packet, asset/proxy gap report, YMM4 adapter work, render, production timing, or creative acceptance.
- **Multi-topic production pipeline smoke GUI ingest added (2026-05-11)**: Implemented the first repeatability smoke from `docs/PRODUCTION_PIPELINE_CONTRACT.md`. The smoke creates minimal fixtures for Real Estate DX baseline, AI monitoring labor, and Baseball news infographic under `samples/_probe/pipeline_smoke/`, each carrying `source_script.txt`, `script_beat_ir.json`, `visual_direction_contract.json`, `shot_layout_plan.json`, `motion_beat_plan.json`, `visual_treatment_proof.{html,png,json}`, `visual_treatment_proof_readback.json`, `review_packet.json`, and `review_decisions.json`. The GUI `デザインレビュー` tab now ingests `samples/_probe/pipeline_smoke/pipeline_smoke_manifest.json` and shows proof image, beat table, warnings, blocked reason, next action, readback, decision artifact, and self-diagnostics. `pipeline_smoke_gui_screenshot_readback.json` confirms 3 topics, 3 proof images, 9 beat rows, reviewable and blocked states, decision paths, and the standalone-proof guard. This is pipeline connectivity smoke only; it does not start G-27 v3, scene decision packet, asset/proxy gap report, YMM4 adapter work, render, production timing, or creative acceptance.
- **Pipeline smoke Electron-free reliability guard + master guardrails sync (2026-05-11)**: Verified existing 3-topic pipeline_smoke fixtures and GUI ingest evidence (`pipeline_smoke_gui_screenshot_readback.json` already records 3 topics / 9 beat rows / reviewable+blocked / standalone guard); committed screenshot remains the GUI-visible proof. Fresh Electron capture (`npm run capture:pipeline-smoke-gui` and other capture scripts) fails in headless / sandboxed bash environments with `app` undefined — environment limitation, not a c62b581 regression. Added `tests/test_pipeline_smoke_manifest.py` as an Electron-free reliability guard covering manifest schema (`version=1.0`, `primary_review_surface="GUI timeline"`, `standalone_html_png_json_is_completion=False`), exact 3 topic ids, allowed states {reviewable, blocked}, blocked_reason / next_action presence, full artifact key set + path existence, and the 7-item forbidden list integrity. Verification: `uvx pytest tests/test_pipeline_smoke_manifest.py -v` → 7 passed; `uvx pytest --tb=no` → 499 passed / 25 skipped / 0 failures. Separately synced master `.claude/hooks/guardrails.py` with the codex branch version (master commit `41ce358`, +564/-12) to restore PreToolUse / Stop hooks on master after a mid-session hook-collapse incident triggered by `git checkout master` during cross-project work. Workspace report contract was extended on master `67eb576` (NLMYTGen), `cc43a0d` (WritingPage main), `b08d244` (ClipPipeGen main) with Drift self-check, Recommended default path, and Cross-project scope declaration sections; behavioral 3-tier hierarchy (Micro / Slice closeout / Handoff) and incidental-tooling-diff classification are held in auto-memory rather than docs to avoid docs-only loop. This is reliability infrastructure and dev infra recovery, not a production feature; live GUI re-capture remains user-environment-only.
- **Real Estate DX background skit workflow authority gate (2026-05-06)**: The background skit source-backed artifact set now uses `samples/_probe/g24/real_estate_dx_background_skit_blueprint.json` as the validator authority, with supporting `row_time_map`, `script_maturity_diagnostic`, `gap_report`, and `overlay_card_placeholder_map` connected to it. Re-run result: `status=blocked`, `errors=[]`, remaining blockers are `ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING` and `ASSET_BLOCKED_REAL_ESTATE_PROPS_MISSING`; `SCRIPT_BLOCKED_RE07_TOO_BROAD` is resolved by validator-visible `RE-07A`-`RE-07E` subbeats. `allowed_next_actions=[overlay_only_compact_review]`; `forbidden_next_actions=[cast_motion_ir, ymm4_creative_acceptance, production_timing]`. Row/time evidence remains script `152` lines / CSV `352` rows / VoiceItems `352`, duration `1049.533333 sec`, active visual coverage `70.0%`, unexplained empty duration `0 sec`. Do not use delivery-template cast reuse or YMM4 creative acceptance.
- **G-25 YMM4 property-based variation probe (2026-04-29 / openability fixed 2026-04-30)**: Implemented `probe-ymmp-variations` as an isolated successor-lane probe for manual YMM4 acting clips. It reads non-variation `Remark` clips from Group/Image/Text/Shape items, reports patchable `X/Y/Zoom/Rotation`, observed flip routes, and `VideoEffects` stack fingerprints, and emits conservative variation candidates. With `-o`, review output now requires a YMM4-saved full project canvas when the probe source is a template/stub; pass `--review-seed` so source templates stay extraction-only and the output preserves YMM4 timeline/root metadata. Review clips use `variation:<source_remark>:<variant_id>` remarks; the probe does not connect to G-24 production placement automatically, does not zero-generate `.ymmp`, and does not synthesize images/effect types. Current proof: `samples/templates/skit_group/delivery_v1_templates.ymmp` + `samples/canonical.ymmp` review seed -> `_tmp/variation/delivery_v1_representative_review.ymmp` (17 representative candidates / 67 item insertions).
- **G-25 creative acceptance result (2026-04-30)**: User confirmed the regenerated review opens in YMM4, but the generated animation variants are not usable. `nudge / scale / rotate / effect_reuse` are property variations, not meaningful motion variations; manual combinations of nod / exit / hop / tilt produce drift such as wrong tilt direction, exiting while tilted, and hopping while tilted. G-25 remains done only as a route/openability/property probe and must not feed production placement. Successor is G-26 motion primitive grammar / compatibility probe. Proof note: `docs/verification/G25-animation-variation-acceptance-2026-04-30.md`.
- **G-26 contract / screen-review adjustment (2026-04-30)**: Audited the parallel-lane report against the worktree and found it directionally valid: `00b2676` exists, branch is ahead 1, and `_tmp/g26/route_readback/RECONCILE.md` / route JSONs exist. Applied the recommended Phase 3 move without another confirmation: created `_tmp/g26/draft_contracts/{index,nod,exit_left,surprise_oneshot}.json`, adopting `dominant_channels` with `VFX:<EffectType>` and first-class `anchor_dependency`. Created a YMM4-openable compact screen review via existing `patch-ymmp --skit-group-only --skit-group-compact-review`, output `_tmp/g26/screen_review/g26_motion_primitive_compact_review.ymmp`; readback: openability pass, 3 inserted GroupItems, frames 0/240/480, POSIX asset paths 0. Proof note: `docs/verification/G26-motion-primitive-contract-screen-review-2026-04-30.md`.
- **G-26 evidence gate follow-up (2026-04-30)**: Re-ran the assistant-owned gate for the current screen review. `_tmp/g26/draft_contracts/*.json` and `_tmp/g26/screen_review/readback.json` parse successfully; `_tmp/g26/screen_review/g26_motion_primitive_compact_review.ymmp` remains machine-pass with openability pass, 3 inserted GroupItems, frames 0/240/480, POSIX asset paths 0, blank asset paths 0. Repo-local scan of 53 `.ymmp` files found no tilt or chain Remarks, so `tilt` remains out-of-contract and `compatible_after` / `forbidden_after` stay `unknown`. Visual acceptance is `not_recorded`, not FAIL; it requires operator YMM4 screen confirmation. Proof note: `docs/verification/G26-motion-primitive-contract-screen-review-2026-04-30.md` Evidence Gate Follow-up.
- **G-26 motion recipe pipeline v1 (2026-04-30)**: Implemented `build-motion-recipes` so G-26 no longer depends on ad-hoc sample scattering. The pipeline reads `samples/recipe_briefs/g26_motion_recipe_brief.v1.json`, a YMM4-saved seed, template source, effect catalog, concrete effect samples, motion library, and optional composition corpus, then writes a review `.ymmp`, readback JSON, and manifest MD. Current output: `_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1.ymmp`, 12 proposed recipes, 12 GroupItems, 24 ImageItems, POSIX asset paths 0, blank asset paths 0. Proof note: `docs/verification/G26-motion-recipe-pipeline-2026-04-30.md`.
- **Contaminated-patch boundary unblocking (2026-04-29)**: Reframed B-10/C-02/C-04/C-05/D-01/E-02/F-03 so old rejected/hold entries block unsafe methods, not the production goals. New terms are fixed in `FEATURE_REGISTRY.md`: `method-rejected` (old method rejected), `goal-allowed` (same goal may proceed through approved boundaries), and `successor-lane` (a safer successor artifact/route). Practical effect: old `--emit-meta`, Python image generation, `.ymmp` zero-generation, YMM4 GUI万能制御, and Python YMM4 preview remain blocked; diagnostic JSON / IR / manifest / packaging brief, G-24 template-source placement, H-02 thumbnail `thumb.*` slot patch, and future H-01/H-02-based metadata drafts are not blocked by the old pollution cleanup.
- **External visual-return analysis consistency audit (2026-04-29)**: Checked the pasted "Visual Return Contract" analysis against the current repo. Its core diagnosis is useful — human visual work must return as machine-readable assets — but its `delivery_nod_v1` premise is stale: G-24 v1 is 5/5 in the repo-tracked template source, analyzed placement and GUI connection exist, and the open G-24 item is compact-review creative acceptance. Added [VISUAL-RETURN-ANALYSIS-CONSISTENCY-2026-04-29.md](verification/VISUAL-RETURN-ANALYSIS-CONSISTENCY-2026-04-29.md). Effective response: do not open a broad new `visual_return_manifest` now; close the concrete thumbnail real-template proof and G-24 compact review first, using existing registry/readback/session-manifest paths as the return contract.
- **Follow-up worklog verification / B-17 measured reflow test hardening (2026-04-28)**: Verified the second pasted analysis against the repo. `impl_file_count` drift was real (`src/**/*.py = 35`), while `test_file_count` remained 31. Added direct tests for `reflow_subtitles_measured()` covering short passthrough, measured-width wrapping, and punctuation/single-character-line safety, plus a CLI WPF-backend smoke test using a fake helper executable. `build-csv --format json` now includes `measure_exe` in `overflow_params` when WPF measurement is used. This does not close YMM4 visual paired evidence; it closes the local code-path verification gap.
- **Worklog consistency audit / stale boundary correction (2026-04-28)**: Audited the pasted work logs against the current worktree. The earlier risks around large unstaged changes and stale test counters are now resolved: the branch is clean, recent work is split into commits, and collected tests are `31 files / 419 tests`. Found and corrected one remaining blind spot in this file: the older "Python text-only / `.ymmp` operation prohibited" section and 2026-04-06 workflow coverage table conflicted with the current allowed `patch-ymmp` boundary. Updated the wording to distinguish prohibited zero-from-scratch `.ymmp` / YMM4 production emulation from allowed limited post-import `.ymmp` patching.
- **Thumbnail real-template acceptance readback (2026-04-28)**: Implemented the missing machine readback step for the thumbnail real-template lane. `patch-thumbnail-template` now verifies patched in-memory values and, when `-o/--output` is used, reloads the written `.ymmp` and returns `file_readback` checks for text, image path, color, and X/Y/Zoom/Rotation values. `_tmp/thumbnail/patch_smoke.json` was prepared with a Windows-readable sample image path, but `_tmp/thumbnail/real_template.ymmp` is not present in this workspace yet, so real YMM4 visual acceptance remains pending.
- **Thumbnail template slot audit / limited patch v1 (2026-04-28)**: Corrected the prior thumbnail drift from docs-only planning to working `.ymmp` slot tooling. Added `audit-thumbnail-template` and `patch-thumbnail-template` with implementation in `src/pipeline/thumbnail_template.py`. Contract: humans duplicate/rough-place a YMM4 thumbnail template and mark existing items with `Remark=thumb.text.<id>` or `Remark=thumb.image.<id>`; the CLI can then audit patchable fields and patch text, ImageItem `FilePath`, existing color route, and X/Y/Zoom/Rotation first values into a copied `.ymmp`. Repo scan still found no real thumbnail `.ymmp` template, so real YMM4 visual acceptance remains open; `samples/canonical.ymmp` correctly fails audit with `THUMB_TEMPLATE_NO_SLOTS`.
- **B-17 measured-width subtitle reflow (2026-04-28)**: Addressed the remaining YMM4/display-width gap by adding an opt-in measured reflow path for `build-csv`. New CLI options: `--wrap-px`, `--wrap-safety`, `--measure-backend eaw|wpf`, `--font-family`, `--font-size`, `--letter-spacing`, and `--measure-exe`. `src/pipeline/text_measure.py` keeps the legacy East Asian Width model as fallback and adds a WPF-backed measurer; `tools/MeasureTextWpf` contains the Windows helper source. The GUI CSV tab now exposes Wrap Width / Measure Backend / font fields, and stats reports measured wrap params. This shifts B-17 from pure character-count approximation toward YMM4 display-condition-based wrapping while still requiring YMM4-side auto-wrap to be OFF or wide enough to avoid double wrapping.
- **Non-thumbnail workflow ambiguity cleanup (2026-04-28)**: Implemented the requested docs-only cleanup for non-thumbnail workflow boundaries. `S6-production-memo-prompt.md` now treats C-07 v4 as main-video Production IR only and keeps thumbnail copy/design in the S-8/H-02 lane. `VISUAL_STYLE_PRESETS.md` and `VISUAL_EFFECT_SELECTION_GUIDE.md` now reflect current G-15〜G-18 / G-24 adapter capabilities instead of older "not written" language. `WORKFLOW.md`, `OPERATOR_WORKFLOW.md`, `INVARIANTS.md`, `AUTOMATION_BOUNDARY.md`, and `GUI_MINIMUM_PATH.md` now distinguish Writer IR capability, adapter write capability, GUI-exposed inputs, and YMM4 creative acceptance. No GUI implementation was added; overlay/se/motion map UI remains a future GUI-completion task if production requires it.
- **Production session manifest / handoff sheet v1 (2026-04-28)**: Implemented `build-session-manifest` as the CLI artifact that bundles S-3 CSV, B-18 diagnostics, S-6 IR validation/apply results, YMM4 manual acceptance placeholders, and sibling `thumbnail_design` records into one JSON/Markdown handoff. The implementation lives in `src/pipeline/session_manifest.py`; `thumbnail_design` is recorded only and is not passed to `validate-ir` / `apply-production`. v1 deliberately does not add GUI buttons, YMM4 thumbnail `.ymmp` generation, YMM4 operation, or image generation.
- **B-17 YMM4 subtitle font source auto inference (2026-04-28)**: Extended subtitle reflow compensation so the CSV generation step now explicitly asks for either a manual `Subtitle Font Scale (%)` or a `YMM4 Subtitle Font Source` `.ymmp`. `build-csv` accepts `--subtitle-font-source-ymmp PATH` and infers `subtitle_font_scale` from YMM4 subtitle `FontSize` using `FontSize=45` as the default 100% baseline; `--subtitle-base-font-size N` can change that baseline. Multiple font-size candidates use the maximum value as a safety-side wrap width correction. This still is not pixel/layout calibration, but it closes the missing workflow step where font-size spec had to be considered before generating wrapped subtitles.
- **Thumbnail generation boundary clarification (2026-04-28)**: User asked whether prior thumbnail-generation specs were vague/nonexistent around AI generation timing and separation from script/Production IR. Clarified that existing H-01/H-02/H-05/one-sheet specs covered promise, copy strategy, visual direction, manual scoring, and YMM4 manual production, but did not clearly define the artifact boundary. Updated `THUMBNAIL_STRATEGY_SPEC.md`, `THUMBNAIL_ONE_SHEET_WORKFLOW.md`, `S8-thumbnail-copy-prompt.md`, and the 2026-04-28 thumbnail/workflow audits: `thumbnail_design` is a sibling artifact under H-01, may be generated in the same AI session as script refinement and Production IR, but must not be embedded in the script body or Production IR and must not be passed to `apply-production`. YMM4 thumbnail `.ymmp` generation/slot patch remains a future template-audit lane.
- **B-17 subtitle font scale reflow compensation (2026-04-28)**: Implemented lightweight font-scale compensation for subtitle wrapping. `build-csv` now accepts `--subtitle-font-scale PERCENT`, keeps `100` as the legacy behavior, and uses `effective_chars_per_line = floor(chars_per_line * 100 / PERCENT)` for `reflow_subtitles_v2`, `split_long_utterances`, and overflow stats. The GUI CSV tab now exposes `Subtitle Font Scale (%)`, and JSON stats reports `chars_per_line` / `subtitle_font_scale` / `effective_chars_per_line`. This is a simple scale correction to reduce YMM4 font-enlargement one-character pushout, not YMM4 pixel measurement or template-specific calibration.
- **User workflow rewiring audit (2026-04-28)**: User asked assistant to own workflow optimization because the GUI is usable but the total production path remains long, and recent YMM4 timeline acting work mixed production, development, and research concerns. Added [USER-WORKFLOW-REWIRING-AUDIT-2026-04-28.md](verification/USER-WORKFLOW-REWIRING-AUDIT-2026-04-28.md). Current reading: keep G-24 production acceptance as the main lane, treat B-17/YMM4 width as maintenance paired-evidence work, keep thumbnail design as a sibling `thumbnail_design` lane under H-01/H-02, and separate YMM4 timeline "acting creation" into production placement / template authoring / adapter hardening / route research. Recommended next development candidate is a production session manifest / handoff sheet before adding more effects.
- **Thumbnail variation / IR planning audit (2026-04-28)**: User clarified the basic line: humans duplicate a YMM4 thumbnail template and replace text / standing pictures / background, but the project still needs a plan for per-video variation, fine placement/color adjustments, and whether thumbnail design should be requested alongside script/production IR. Added [THUMBNAIL-VARIATION-AND-IR-PLAN-2026-04-28.md](verification/THUMBNAIL-VARIATION-AND-IR-PLAN-2026-04-28.md) and linked it from the capability audit. Decision: keep thumbnail design as a sibling `thumbnail_design` companion JSON under H-01/H-02, not as fields inside Production IR Micro entries. Safe development path is YMM4 thumbnail template slot contract -> read-only audit -> limited text/color/geometry patch -> image slot replacement -> variation history warnings. Current blocker is absence of a repo-tracked thumbnail `.ymmp` template with `thumb.*` slot Remarks.
- **B-17 one-character subtitle tail analysis (2026-04-28)**: User reported frequent one-character subtitle wraps and asked for ownership. Added [B17-one-character-tail-analysis-2026-04-28.md](verification/B17-one-character-tail-analysis-2026-04-28.md). Root cause is not “B-17 absent” but missing accompaniment around it: GUI defaults had drifted to `Chars/Line=20` while CLI/docs standard is display width `40`; YMM4 actual subtitle width is still uncalibrated against `display_width`; and `--stats` does not separately surface one-character tail risk. Local measurement on `samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv` found 0 explicit one-character CSV lines, but at assumed actual cap 40 there are 10 one-character-tail risks and at cap 38 there are 35. Fixed GUI/default docs to standard `2 / 40` and tightened the regression test so a full-width single-character line is not accepted by display-width math alone.
- **G-24 user workflow optimization / GUI connection (2026-04-28)**: Took ownership of the current user-workflow bottleneck around skit_group placement. G-24 analyzed placement itself was already implemented; the remaining workflow gap was that production operators still had to drop to CLI to pass `--skit-group-registry`, `--skit-group-template-source`, `--skit-group-only`, and strict intent validation. The Electron production tab now exposes Skit Group Registry / Template Source selectors, strict skit_group intent validation, and a skit_group-only mode that intentionally omits CSV(row-range) because it uses aligned IR anchors. `apply-production` now accepts optional `--strict-skit-group-intents` and enforces it even in skit_group-only mode. Docs now split skit_group work into production / development / research lanes and keep YMM4 composition acceptance separate from machine readback.
- **Thumbnail generation capability audit (2026-04-28)**: User asked assistant to take ownership of the thumbnail-generation area and first investigate current capability. Added [THUMBNAIL-GENERATION-CAPABILITY-AUDIT-2026-04-28.md](verification/THUMBNAIL-GENERATION-CAPABILITY-AUDIT-2026-04-28.md). Current repo capability is judgment support / workflow / manual score aggregation only: H-01 brief template, C-08/H-02 copy strategy, H-03/H-04 diagnostics, H-05 `score-thumbnail-s8`, and YMM4 one-sheet workflow. There is no repo-tracked thumbnail `.ymmp` template/source/slot registry, no image generation/composition, no image analysis, and no GUI H-05 button. All 15 `samples/*thumb*.png` files checked share the same SHA256, so they are continuity anchors rather than a diverse production corpus. A safe next development lane is thumbnail template slot audit/registry for YMM4 template replacement, not Python image generation.
- **G-24 template-analyzed placement planner implementation (2026-04-28)**: Implemented analyzed skit_group placement in `src/pipeline/skit_group_placement.py`. The placement path now derives a canonical rest pose from template-source GroupItem transform medians, shifts each cloned GroupItem `X` / `Y` / `Zoom` value list from template-local baseline to that rest pose, preserves relative motion deltas / child ImageItem offsets / timing, and fails fast with `SKIT_TEMPLATE_ANALYSIS_INSUFFICIENT` when numeric transform facts are missing. Follow-up correction after visual feedback: ImageItem `FilePath` now writes YMM4-readable Windows paths instead of WSL `/mnt/c/...`, and `--skit-group-compact-review` generates a non-scattered visual review artifact. Regenerated `samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp` and added `samples/_probe/g24/real_estate_dx_skit_group_compact_review.ymmp`; both read back as 9 GroupItems / 10 ImageItems / 0 missing assets / 0 POSIX asset paths. Compact review frames are 0 / 240 / 480 / 720 / 960 for the five cues.
- **remote sync / local readiness check (2026-04-28)**: Fetched `origin`, created local tracking branch `codex/g24-nod-sync-adoption` from `origin/codex/g24-nod-sync-adoption`, and kept the next frontier on G-24 template-analyzed placement. Local validation initially exposed a WSL/Windows-path-sensitive assertion in `tests/test_skit_group_placement.py`; the test now uses the same repo asset resolver as `skit_group_placement.py` instead of raw `Path(FilePath).exists()`. This is a test portability fix only and does not change production placement behavior.
- **G-24 skit_group placement automation direction correction (2026-04-27/28)**: Re-centered G-24 on `.ymmp` write capability instead of operator hand placement. Added `src/pipeline/skit_group_placement.py`, `patch-ymmp/apply-production --skit-group-template-source`, `validate-ir --strict-skit-group-intents`, repo-tracked template source `samples/templates/skit_group/delivery_v1_templates.ymmp`, and fixture `samples/_probe/g24/skit_group_placement_base.ymmp`. After the user saved `samples/nod.ymmp` with a nod-only animation and `Remark=nod`, the repo-tracked source now contains all five v1 templates including normalized `delivery_nod_v1`; future missing templates must still fail fast with `SKIT_TEMPLATE_SOURCE_MISSING`. The previous real-estate packet is retained as history only; operator hand placement is not production automation.
- **G-24 real estate DX YMM4 production packet (2026-04-27)**: Added [G24-real-estate-dx-ymm4-production-packet-2026-04-27.md](verification/G24-real-estate-dx-ymm4-production-packet-2026-04-27.md) to turn the validated CSV / skit_group IR into an operator-ready S-4 / S-6 packet. The packet fixes the open target as a copied production YMM4 template project, the source CSV as `samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv`, and the skit_group cue table as IR indexes 1 / 15 / 35 / 39 / 104 / 143. It keeps `panic_shake` as `manual_note`, treats the 18 CSV overflow candidates as B-17 residue only if visible in YMM4, and does not add new CLI, motion authoring, registry alias, or `.ymmp` generation.
- **G-24 real estate DX skit_group IR validation (2026-04-27)**: Accepted the corrected NotebookLM-derived real estate DX script as the case input, saved `samples/不動産DX_魔法の鍵とキュレーション.txt`, built `samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv` (352 rows), and generated `samples/不動産DX_魔法の鍵とキュレーション_skit_group_ir.json`. `audit-skit-group` against `samples/canonical.ymmp` returned `exact=3 / fallback=2 / manual_note=1`; `panic_shake` is the only manual_note. Added [G24-real-estate-dx-skit-group-ir-validation-2026-04-27.md](verification/G24-real-estate-dx-skit-group-ir-validation-2026-04-27.md). Also recorded that NotebookLM text is low-trust and must pass B-18/C-09/manual QC before CSV/IR.
- **G-24 production IR generation flow sync (2026-04-27)**: Reflected the passed minimal production IR shape into `docs/S6-production-memo-prompt.md`, `docs/PRODUCTION_IR_SPEC.md`, `docs/SKIT_GROUP_TEMPLATE_SPEC.md`, and `docs/WORKFLOW.md`. Real skit_group actor utterances must include `motion_target: "layer:9"` and use exact v1 intents or registered alias intents; `panic_shake` remains the manual/unresolved candidate. Re-ran `audit-skit-group` on `samples/g24_skit_group_minimal_production_ir.json`: `exact=3 / fallback=2 / manual_note=1`. Added [G24-production-ir-generation-flow-sync-2026-04-27.md](verification/G24-production-ir-generation-flow-sync-2026-04-27.md). No additional repo IR exploration or motion authoring.
- **G-24 minimal production IR validation (2026-04-27)**: Added `samples/g24_skit_group_minimal_production_ir.json` as the minimum production-oriented skit_group IR input because repo-local production-ish IRs do not target the canonical skit_group layer. Validated it with `audit-skit-group samples/canonical.ymmp ... --skit-group-registry samples/registry_template/skit_group_registry.template.json --format text`: `exact=3 / fallback=2 / manual_note=1`. `surprise_jump` and `deny_shake` resolve via registry fallbacks; `panic_shake` remains `manual_note` / new-template candidate / IR wording avoidance option. Added [G24-minimal-production-ir-validation-2026-04-27.md](verification/G24-minimal-production-ir-validation-2026-04-27.md). No further repo IR broad search is needed.
- **G-24 real production candidate scan (2026-04-27)**: Searched repo-local IR candidates for alias-enabled `audit-skit-group` validation. Only probe IRs contain skit_group layer-9 targets; production-ish root samples audited against `samples/canonical.ymmp` all returned `exact=0 / fallback=0 / manual_note=0` because they contain no skit_group-targeted entries. Added [G24-real-production-candidate-scan-2026-04-27.md](verification/G24-real-production-candidate-scan-2026-04-27.md). This led to the minimum production IR input sample above; no new YMM4 motion authoring or registry mapping was opened.
- **G-24 alias registration PASS (2026-04-27)**: Registered safe production-like label fallbacks in `samples/registry_template/skit_group_registry.template.json`: `surprise_jump -> delivery_surprise_oneshot_v1` and `deny_shake -> delivery_deny_oneshot_v1`. `panic_shake` remains `manual_note` / new-template candidate. Validation after aliasing: IR A `exact=3 / fallback=0 / manual_note=1`; IR B `exact=1 / fallback=2 / manual_note=1`; focused tests `tests/test_capability_atlas.py tests/test_skit_group_audit.py` PASS. Added [G24-alias-registration-2026-04-27.md](verification/G24-alias-registration-2026-04-27.md). Next frontier is real production IR/corpus validation, not another planning-only report.
- **G-24 production-like gap classification PASS (2026-04-27)**: Ran `audit-skit-group` on `samples/canonical.ymmp` with `samples/_probe/b2/haitatsuin_ir_oneshot_block2.json` and `samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json`. Results: IR A `exact=3 / fallback=0 / manual_note=1`; IR B `exact=1 / fallback=0 / manual_note=3`. Covered intents: `enter_from_left`, `surprise_oneshot`, `deny_oneshot`, `nod`. Alias candidates: `surprise_jump -> surprise_oneshot`, `deny_shake -> deny_oneshot`. New-template/manual candidate: `panic_shake`. Added [G24-production-like-gap-classification-2026-04-27.md](verification/G24-production-like-gap-classification-2026-04-27.md). No registry, `src/`, template, or `.ymmp` changes were made for this classification pass.
- **G-24 repo-probe production-use validation PASS (2026-04-27)**: Ran `audit-skit-group` on `samples/canonical.ymmp` + `samples/_probe/skit_01/skit_01_ir.json` with `samples/registry_template/skit_group_registry.template.json`. Result: `exact=5 / fallback=0 / manual_note=0`; all 5 v1 intents resolve to `delivery_*_v1` templates. Added [G24-production-use-validation-report-2026-04-27.md](verification/G24-production-use-validation-report-2026-04-27.md). No confirmation `.ymmp` was generated, and `samples/haitatsuin_2026-04-12_g24_proof.ymmp` remains compact template/sample proof rather than validation input. Next frontier is applying the same validation shape to a real production IR / compatible production corpus.
- **G-24 v1 planned set completion sync (2026-04-27)**: User completed the remaining 2 samples (`delivery_deny_oneshot_v1` / `delivery_exit_left_v1`) and asked assistant to confirm and move forward. Repo inspection of `samples/haitatsuin_2026-04-12_g24_proof.ymmp` found plain body/face `ImageItem` children, Layer 9 `GroupItem` snippets with matching Remarks, and `TachieItem` count 0. `deny_oneshot` is represented as a short X-axis one-shot sway; `exit_left` uses OUT `InOutMoveEffect` leftward. `skit_group.intent.deny_oneshot` and `skit_group.intent.exit_left` are promoted to `direct_proven`, completing the v1 planned set. The proof `.ymmp` is now a compact template/sample proof rather than the earlier voice-anchored adoption corpus, so the next frontier is **production-use validation** with `samples/canonical.ymmp` + real/probe IR, not more motion authoring.
- **G-24 roadmap loop-stop correction (2026-04-27)**: User flagged that the current source of truth could imply endless “make another plausible motion” work and did not clearly answer what happens after a motion is authored. Canonical docs now state that planned author/export stops after `deny_oneshot` -> `exit_left`; after `exit_left`, the next move is production-use validation, where real IR resolves to exact / fallback / manual note and the result is judged by whether it reduces S-6（背景・演出設定）selection work. New skit motions are only re-opened when a concrete production gap appears.
- **G-24 role clarification (2026-04-27)**: User clarified the intended flow: user authors a small reusable motion set, then assistant uses those templates plus registry/know-how to generate or organize production-like samples, and user reviews the output. This is not a workflow where user manually creates every sample/template.
- **G-24 `delivery_nod_v1` PASS sync (2026-04-27)**: User reported that `delivery_nod_v1` was created, saved as a YMM4 native GroupItem template, and given the same Remark. User acceptance also confirmed body + face move together, the nod is visible but not scene-dominating, and no `TachieItem` is included. This closes the `nod` cautious gate and promotes `skit_group.intent.nod` to `direct_proven`; the next frontier was `deny_oneshot` followed by `exit_left`, later superseded by the v1 planned set completion sync above.
- **strong doc-excision follow-up (2026-04-27)**: A second deletion pass removed stale roadmap authority from the top of `docs/project-context.md` and deleted the old "copy into another thread" prompt block from `docs/verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md`. The then-current root agent doc aligned GUI/YMM4 with CLI artifact mode, and `AGENTS.md` stated that `runtime-state.md` `next_action` is the current frontier source while `project-context.md` is a targeted log. No production artifact, FEATURE status, or G-24 `next_action` changed.
- **next roadmap branch prep (2026-04-27)**: After the legacy-document cleanup and template-formalism correction, the next roadmap was fixed as a gate-shaped G-24 sequence: close `delivery_nod_v1` author/export first, promote `nod` only after user-owned PASS, then widen to `deny_oneshot -> exit_left`. `docs/project-context.md` recorded the formal-plan entry branches (未報告 / PASS / FAIL / 新規制作案件), and `docs/verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md` §2.3.1 mirrored the same pre-plan decision point. This state was superseded first by the `delivery_nod_v1` PASS sync, then by the v1 planned set completion sync above.
- **strong legacy-plan deletion (2026-04-27)**: Old core-dev, lane prompt, parallel prompt-hub, and visual-quality packet files were deleted instead of bannered. Current state must be recovered from `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file, then from `P02` / `PRE-PLAN` only when the current G-24 gate needs detail.
- **documentation pollution excision (2026-04-27)**: Resume-prompt authority was removed; `verification/` is now evidence storage rather than a current-canonical table; `USER_REQUEST_LEDGER.md` keeps only active durable requirements; date-fixed rule headings and old background-animation/S6 front-facing language were demoted. Current restart remains `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file.
- **restart read budget correction (2026-04-27)**: Normal restart no longer means reading every protected/canonical doc. The default path is `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file, then targeted sections only (`project-context` HANDOFF / DECISION LOG, FEATURE ID, invariant, ledger, workflow, interaction failure class, or AI gate as needed). Full re-anchoring is an exception for boundary uncertainty, drift, explicit REANCHOR / REFRESH / AUDIT, or failure to connect work from this file.
- **G-24 `delivery_nod_v1` implementation pass (2026-04-27)**: Assistant implemented the non-user-owned part of the plan by re-running readiness checks. At that historical point, `audit-skit-group` on both `samples/canonical.ymmp` and `samples/haitatsuin_2026-04-12_g24_proof.ymmp` stayed `exact=5 / fallback=0 / manual_note=0`. `apply-production --dry-run` on the proof corpus returned `success=true`, `motion_changes=8`, and `group_motion_changes=0` when run with `--tachie-motion-map samples/tachie_motion_map_library.json`. A dry-run without that motion map fails with `MOTION_UNKNOWN_LABEL`, so the motion map is part of the required readiness command. This was readiness-only before the later user-owned PASS sync; the current worktree proof `.ymmp` is now a compact template/sample proof.
- **template formalism correction (2026-04-27)**: Short return formats and prompt/checklist templates must not outrank task connectivity. For manual/shared actions, docs must first state the open target, created/modified artifact, source object, actor, owner artifact, acceptance meaning, and replan condition. `PASS` / `FAIL` / `OK` / `NG` is only the final result label, not a substitute for the operation.
- **roadmap pre-plan prep after legacy cleanup (2026-04-27)**: Updated the pre-plan intake docs away from the older background-animation/S6 axis and into the G-24 gate-shaped sequence. This was later advanced by the `delivery_nod_v1` PASS sync and then by the v1 planned set completion sync; the current anchor is production-use validation.
- **docs cleanup / interaction failure framing correction (2026-04-26)**: Obsolete prompts, archived packets, and superseded roadmap/setup docs were deleted; `docs/INTERACTION_NOTES.md` now uses structural failure classes (`REASK_DEBT`, `BROAD_STOP`, `OPTION_COLLAPSE`, `MANUAL_PROOF_TRANSFER`, `VALUE_PATH_DRIFT`, `STATUS_DRIFT`, `DOMAIN_PACKET_COLLAPSE`). The durable rule is that interaction notes must prevent project-stalling inefficiency rather than record personal reactions. Synced `docs/ai/CORE_RULESET.md` role wording and `docs/USER_REQUEST_LEDGER.md`.
- **nod cautious gate readiness + packet sync (2026-04-23 snapshot; superseded)**: Assistant reran `audit-skit-group` on `samples/canonical.ymmp` and `samples/haitatsuin_2026-04-12_g24_proof.ymmp`, confirmed that `delivery_nod_v1` stayed `exact`, and rechecked `apply-production --dry-run` with `success=true` / `group_motion_changes=0`. At that snapshot, the repo tracked only the canonical anchor plus the two starter copies (`delivery_enter_from_left_v1`, `delivery_surprise_oneshot_v1`) and did not yet track a discrete `delivery_nod_v1` source. This historical user-owned export step was superseded by the v1 completion sync and the 5/5 repo-tracked template source; do not use this entry as current `next_action`.
- **starter batch export sync（2026-04-21）**: G-24 の初回 authoring 範囲は `delivery_enter_from_left_v1` / `delivery_surprise_oneshot_v1` の 2 件に固定していた。`samples/canonical.ymmp` には frame 0 の canonical anchor `haitatsuin_delivery_main` に加え、frame 306 `delivery_enter_from_left_v1` と frame 658 `delivery_surprise_oneshot_v1` の GroupItem copy が追加済みで、各 group は Layer 9 / `GroupRange=2` / 隣接 Layer 10-11 の `ImageItem` ペアを維持する。加えて user report では、この 2 件を **名前そのまま・GroupItem template・ImageItem 2 点込み**で standalone native template library へ登録済み。assistant 側は registry / preflight / P02 / handoff をこの starter export 状態に同期済み。当時 `delivery_deny_oneshot_v1` / `delivery_exit_left_v1` / `delivery_nod_v1` は canonical corpus で exact を維持する catalog entry だったが、現在は v1 completion sync により全 5 件 `direct_proven`。
- **cautious gate all-pass (2026-04-21)**: The export order remains **manual acceptance -> 1 production adoption proof -> export**, and the starter batch still counts as PASS across all three steps. `audit-skit-group` stayed at `exact=5 / fallback=0 / manual_note=0`, and `apply-production --dry-run` stayed at `success=true` / `group_motion_changes=0`. Machine-readable `warnings[]` still shows only `bg label 'studio_blue' not found in bg_map`; CLI output also replays the known `FACE_PROMPT_PALETTE_EXTRA` / `FACE_LATENT_GAP` / `IDLE_FACE_MISSING` baseline warnings. These warnings remain non-fatal and do not change the starter-batch PASS state.
- **manual acceptance PASS（2026-04-21 user report）**: `delivery_enter_from_left_v1` / `delivery_surprise_oneshot_v1` の見え方確認は完了。`enter_from_left` は同テンプレ内に紛れていた退場設定を YMM4 上でカット済みで、repo-local inspection でも `InOutMoveFromOutsideFrameEffect` は `IsOutEffect=False`。2 件とも loop / body-face drift なし。
- **同期確認**: `git log -1 --oneline` が最新。**motion 軸別 one-shot + motion_target Remark** の実装コミットは **`396ea4b`**。続けて **引き継ぎ本文（本節）と `.gitignore`** を入れたコミットがその直後。**本ブロック完了後**は `git push origin master` でリモートと揃えること。
- **検証用 ymmp（再生成・`_tmp/` は gitignore）**: `skit` 系・B2 one-shot proof は verification 短文に記載のパスに合わせて再生成すること（具体パスは [B2-oneshot-library-v3-2026-04-19.md](verification/B2-oneshot-library-v3-2026-04-19.md)、[skit_01_delivery_dispute_v1_2026-04-19.md](verification/skit_01_delivery_dispute_v1_2026-04-19.md)）。
- **workflow breakage（2026-04-20 正本、2026-04-27 表現是正）**: `_tmp/skit_ManualSample_01.ymmp` / `_tmp/skit_01_v2.ymmp` はローカルに存在する場合があるが、gitignored / untracked の一時物であり active gate や比較基準にしない。`_tmp/skit_01_v2_verify.ymmp` も現作業ツリーでは存在を前提にしない。**新しい ManualSample 作成依頼は禁止**。比較・切り分けは [skit_01-workflow-breakage-audit-2026-04-20.md](verification/skit_01-workflow-breakage-audit-2026-04-20.md) + `python3 samples/_probe/skit_01/audit_skit_01_proof.py` で repo 内 tracked docs / sample / registry を優先する。
- **canonical anchor（2026-04-20 採用）**: `samples/canonical.ymmp` を haitatsuin canonical skit_group の official artifact として扱う。`haitatsuin_delivery_main` / Layer 9 / ImageItem-only / 左向き基準姿勢。正本 [G24-canonical-anchor-adoption-2026-04-20.md](verification/G24-canonical-anchor-adoption-2026-04-20.md)。
- **再開時**: segment / Group 確認は `inspect_v5_group_segments.py` 系。茶番 E2E 経路は既存 IR + `apply-production`（IR 例: `samples/_probe/skit_01/skit_01_ir.json`）。
- **既知メモ**: pan のみ区間で Remark が `motion:none utt:?` になりうる。camera pan の X と縦 one-shot が重なると画面上は斜めに見える可能性。`nod` は RepeatMove、`nod_oneshot` は未実装。
- **YMM 効果サンプル（共有参照）**: `samples/_probe/b2/effect_full_samples.json` をリポジトリに同梱する（作業環境の突き合わせ用）。motion プリセットの正本は引き続き `tachie_motion_map_library.json` / `EffectsSamples_*.ymmp` / [MOTION_PRESET_LIBRARY_SPEC.md](MOTION_PRESET_LIBRARY_SPEC.md)。

ドキュメント地図（任意）: [NAV.md](NAV.md) / Electron 最小経路・検証ラダー: [GUI_MINIMUM_PATH.md](GUI_MINIMUM_PATH.md)（2026-04-14: balance-lines GUI 露出・ウィザード範囲明記）

- project: NLMYTGen
- git: **既定の開発ブランチは `master`**（2026-04-09: PR [#1](https://github.com/YuShimoji/NLMYTGen/pull/1) で `feat/phase2-motion-segmentation` をマージ済み。新規作業は `master` からブランチを切る）
- lane: **コア開発幹**（ゆっくり解説動画制作ワークフロー / 回帰・ドキュメント整合・承認済みバグ修正）。**主軸はゆっくり解説本流** — エージェント作業は未承認 FEATURE を増やさず上記に集中。オペレータ並行: Phase 1 Block-A (通過済、メンテ層の継続観測) / 主軸 (演出配置自動化の実戦投入) は runbook どおり。**レーン A（Phase 1）の repo 準備はオペレータ側でクローズ**（[OPERATOR_LANE_A_ENV.md](verification/OPERATOR_LANE_A_ENV.md)、[LANE_A_PREP_CHECKLIST.md](verification/LANE_A_PREP_CHECKLIST.md)）。**レーン D（H-01 brief）オペレータ完了・当面クローズ**（[H01-lane-d-prep-2026-04-09.md](verification/H01-lane-d-prep-2026-04-09.md) §6、2026-04-09）
- sidequest_boundary: Baseball / `sports_news` は明示起動の sidequest であり、通常再開の主対象にしない。
- slice: **G-27 Layout Instruction Compliance Proof closed; PublicVsBrokerDB carrier handoff wait resumes (2026-05-27)**. The layout proof now has machine readback pass and YMM4 GUI proof pass, but remains diagnostic-only. Direct dense `ShapeItem` / `TextItem` scene generation from semantic intent remains stopped. Visual proxy v2/v2.1, the minimal patched probe, micro scene variants, and the layout instruction proof are diagnostic evidence; they are not production route artifacts and do not unlock render, creative acceptance, production timing, or another direct primitive scene variant.
- next_action: **Resolve the `G27_PublicVsBrokerDB` carrier decision before slot-fill.** Default safe path: the user creates/returns a minimal YMM4 carrier from `docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md` with carrier `.ymmp` path, preview screenshot, timeline screenshot, representative item property screenshots for `G27PBD_PublicPanel`, `G27PBD_PublicCard1`, `G27PBD_BrokerPanel`, and `G27PBD_Lock`, the chosen light/dark stage, and a short note that the bottom caption safe area is clear. Fast path, only if user explicitly chooses it: promote `samples/_probe/g24/real_estate_dx_diagnostic_carrier.ymmp` to production carrier through a new boundary/readback record; do not silently promote it. Without either carrier path, assistant may only continue diagnostic/planning work, not production slot-fill. After a carrier is chosen, assistant should read back required `G27PBD_*` item names, short Remarks, fixed card counts, `G27PBD_Arrow` existence, and geometry-free patch feasibility, then prepare an anchored slot contract. Do not create raw geometry, another `.ymmp`, render, production timing, G-26, sports_news, INT-02e, publishing, master integration, new gate, or broad roadmap.
  - **assistant (review packaging)**: Treat `samples/_probe/g24/real_estate_dx_review_packet.json` as the GUI-facing decision packet and `samples/_probe/g24/real_estate_dx_overlay_card_review_map.md` as detailed evidence. The user-facing path is GUI decision capture, not another Markdown review handoff.
  - **assistant (A)**: Keep Writer IR strict: skit_group actor utterances require `motion_target: "layer:9"` and registry v1/alias intents only; `panic_shake` is not normal Part 2 JSON vocabulary.
  - **assistant (B)**: Treat `samples/templates/skit_group/delivery_v1_templates.ymmp` as the closed G-24 foundation source. It remains valid for delivery-style templates, but Real Estate DX can only use it as an explicit proxy after G-27 records the reason, weak assumptions, and replacement trigger.
  - **assistant (C)**: For the current Real Estate DX background-skit lane, treat `samples/_probe/g24/real_estate_dx_skit_group_compact_review.ymmp` and `samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp` as historical transport/readback proof only. The current review artifact set is `real_estate_dx_overlay_only_compact_review.*`, and it is not creative acceptance or production timing.
  - **assistant (D)**: Do not run new Real Estate DX placement from old cue indexes until G-27 classifies the scene as production template / accepted proxy / cut.
  - **shared (E)**: Treat preflight/audit/readback as diagnostics only. The acceptance signal for Real Estate DX now comes from the G-27 scene decision packet followed by validator-permitted artifacts.
  - **assistant (F)**: Treat "Visual Return Contract" as a useful cross-route abstraction, not the immediate implementation target. For now, record accepted visual work through existing route artifacts: skit_group registry/template source/readback, thumbnail `thumb.*` template readback, and `build-session-manifest` acceptance slots.
  - **assistant (G)**: Treat Baseball / `sports_news` as an explicit sidequest. Do not change primary `next_action` to Baseball unless the user explicitly asks to promote it; start Baseball work only from an explicit chat request and keep the first artifact as a screen plan.
- parallel_replan_2026_04: **視覚最低限 + 改行／YMM4 ギャップ**の到達定義・チェックリスト・計測テンプレは [VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md)。`next_action` の主軸とは別軸の **並列オプション**。オペレータ時間の並列で、同文書の **トラック A（演出 IR 実戦 = 主軸の実務サブセット）** / **トラック B（改行ギャップ記録 = メンテ層 B-17 観測）** を配分する。汎用 Prompt ハブは削除済みなので、依頼時は作業対象・作成物・owner・acceptance を先に書き、必要な詳細手順だけを参照する。
- recommended_frontier_order: **G-27 Real Estate DX scene decision packet** → 演出配置自動化の実戦投入 (P02) → 台本品質の継続観測 (メンテ) → 補助経路 (G-22 / PNG overlay) の必要最小限運用
  - **再開ショートカット（推奨対応）**: G-20 スライス1-2 完了（group_target バリデーション + `mode: relative`）は前提として維持。ただし主軸は `group_motion` の拡張ではなく、**canonical skit_group template → 派生 template 群 → production での template 解決**。
- **closed skit_group foundation の出口**: planned author/export は `deny_oneshot` → `exit_left` で止める。以後は実制作 IR に対して exact / fallback / manual note が S-6（背景・演出設定）の選択負荷を減らすかを見る。新しい小演出は production gap が出た時だけ再起票する。
  - **役割分担**: user は少数の reusable YMM4 native GroupItem template を作る。assistant はその組み合わせ・registry・fallback note で production-like sample / 解決結果を作り、user は確認に集中する。
  - **並列の読み**: 上記フロンティア順と別に、[VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md) の **トラック A**（最小視覚 = 主軸の実務サブセット）と **トラック B**（B-17 済み L2 と YMM4 実表示のギャップ計測 = メンテ層観測）を **同時期に進めてよい**。先にオペレータ時間を取る軸は案件による（ユーザー合意で `next_action` 本文は変えず、配分のみ記録してよい）。
- 再現ルール: 異種サンプル 1 本で打ち切り済み。以後は新しい failure が出たときだけ追加検証
- operator/agent ガード: [REPO_LOCAL_RULES.md](REPO_LOCAL_RULES.md)（正本）+ `.claude/hooks/guardrails.py` で repo 外逸脱 / broad question 停止 / repeated visual proof を常設抑止（`.claude/CLAUDE.md` は入口ポインタ）
- 案件モード: CLI artifact

## 優先順位 (正本)

目的: 実制作の手間を減らすこと。未承認のコード機能は増やさない ([FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) 準拠)。順序を変える場合はユーザー合意で `next_action` と本節を更新する。

**判断基準**: 主軸は以下 4 条件をすべて満たす — ① 制作物の質に直接効く / ② 現在 bottleneck が顕在化 / ③ 着手しないと制作 workflow が詰まる / ④ 明確な完了の目安がある。据え置きは状態別に `hold` (再開条件あり) / `quarantined` (汚染バッチ由来) / `rejected` (廃止) に分ける。


| 層 | 内容 | 担い手 | 完了の目安 |
| --- | --- | --- | --- |
| **主軸 (唯一)** | **G-27 Real Estate DX background skit review cycle**: closed template-first skit_group foundation を前提に、Real Estate DX の cast/props 不足、proxy 採否、場面ごとの良し悪し判断を `TASK_DEVELOPMENT_CYCLE_SPEC.md` の review cycle で閉じる | user (review signal / proxy 可否 / production 素材判断) + assistant (scene decision packet / revised blueprint / validator 再実行 / gap report) | 全場面が `production template exists` / `accepted proxy` / `cut from plan` に分類され、validator `passed` または production 継続しない明示 blocked closeout になる |
| **メンテ (並行低負荷)** | ① **台本品質の継続観測 (B-18)** — Block-A 通過済、新台本は [P01-phase1-operator-e2e-proof.md](verification/P01-phase1-operator-e2e-proof.md) に 1 行追記のみ。詳細手順 [B18](prompts/B18-script-diagnostics-observation-prompt.md)。② **Packaging brief / one-sheet (H-01/H-02)** — 新しい packaging brief が必要な案件でのみ起動。[PACKAGING_ORCHESTRATOR_SPEC.md](PACKAGING_ORCHESTRATOR_SPEC.md)、[THUMBNAIL_ONE_SHEET_WORKFLOW.md](THUMBNAIL_ONE_SHEET_WORKFLOW.md)、詳細手順 [H01](prompts/H01-packaging-brief-prompt.md) / [H02](prompts/H02-thumbnail-one-sheet-prompt.md)。③ **字幕 B-17 残差観測** — drift が見えた時だけ起動。詳細手順 [B17](prompts/B17-reflow-residue-observation-prompt.md) | オペレータ (GUI) / 別セッション assistant | 既定順は **B-18 → H-01/H-02 on demand → B-17 on drift**。verification 更新のみで回す |
| **sidequest (明示起動のみ)** | **Baseball / sports_news**。野球速報・試合解説・InfoGraphics は本流を置き換えず、チャットで明示された場合だけ別レーンとして起動する。最初の review surface は screen plan | 別セッション assistant / 必要時 user review | screen plan で card sequence / information budget / YMM4 placement が見え、Baseball lane 内の次 artifact が決まる |
| **hold (補助経路)** | **G-22 dual-rendering / PNG overlay**。背景キャラや一枚絵補助では有効だが、茶番劇演者の主軸ではない。必要時のみ使用 | user + assistant | skit_group template だけでは吸収できない案件で補助利用したとき |
| **hold (条件待ち)** | E-01 (YouTube 投稿自動化) / E-02 (旧 standalone YouTube メタデータ) — 自動投稿や本線注入は制作パイプと混ぜない。H-01/H-02 を入力にした metadata draft は successor-lane として再起票可 | — | integration point が明示されるまで |
| **汚染バッチ gate** | F-01 / F-02 は `quarantined`、D-02 は C-07 v3 吸収済み `hold`。いずれも個別再審査なしに backlog 化しない | — | 再審査・spec 化まで触らない |
| **rejected** | B-10 (旧 `--emit-meta`、撤去済) — method-rejected。承認済み artifact 生成まで塞がない | — | 要望再浮上時は新 ID / successor-lane で再起票 |


**触らない原則**: spec/proof の採掘を増やさない。done 件数を進捗指標にしない。face を broad visual retry loop に戻さない。リモートは `origin/master` を正本とし、追加スライスは master からブランチを切る ([P2A-phase2-motion-segmentation-branch-review.md](verification/P2A-phase2-motion-segmentation-branch-review.md) は歴史的判断として参照)。

## 主成果物

- active_artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー
- artifact_surface: CLI → CSV → YMM4 台本読込 → 演出設定 → レンダリング → サムネイル → 投稿
- last_change_relation: **2026-06-01 carrier requirement clarification + remote handoff**. The layout proof proves fixed natural-language layout instructions can produce a stable YMM4-visible diagnostic layout after one GUI-feedback fix cycle. It does not by itself replace the `G27_PublicVsBrokerDB` carrier requirement. The current accepted paths are either a minimal human-authored YMM4 carrier or an explicit user decision to promote the existing diagnostic carrier with a new boundary/readback record. Silent promotion from diagnostic artifact to production carrier remains forbidden. G-27 remains the current primary `next_action`; Baseball Info / `sports_news` remains an explicit chat-started sidequest and does not replace the mainline.

## カウンター

- blocks_since_user_visible_change: 0
- blocks_since_manual_evidence: 0
- blocks_since_visual_audit: 0

## 量的指標

- test_file_count: 42 (`tests/test_*.py`; 45 files under `tests/` including helpers/data)
- test_count: last recorded full run `525 passed, 25 skipped` (2026-05-27 handoff); latest narrow verification `uv run pytest tests/test_feed_parse.py` => `17 passed` (2026-06-02 remote sync / roadmap prep)
- mock_file_count: 0
- impl_file_count: 43 (`src/**/*.py`)
- mock_impl_ratio: 0.00
- open_todo_count: 0

## 最終検証

- last_verification: **2026-06-02 remote sync / roadmap-prep state sync**. Ran `git fetch --all --prune`, `git pull --ff-only origin master`, confirmed pulled remote base `29ca758` and local/remote parity `0 0` before writing this handoff note, checked working-tree residue (`.claude/worktrees/`, `samples/2026-05-16.ymmp`), checked absence of local-only RSS brief/OPML artifacts in this checkout, parsed `samples/2026-05-16.ymmp` as only 3 item-like entries, and ran narrow RSS parser verification `uv run pytest tests/test_feed_parse.py` => `17 passed`. The previous full-test record remains `525 passed, 25 skipped` from the 2026-05-27 handoff. No RSS smoke, YMM4 write, render, creative acceptance, production carrier replacement, slot-fill implementation, production timing, G-26, sports_news, INT-02e, publishing, new gate, or production roadmap implementation was performed.

## Evidence（CLI artifact mode）

- evidence_status: Production E2E 実証済み (2026-04-05)。palette.ymmp → extract-template --labeled → face_map.json (11表情) → Part 1+2IR_row_range.json (28 utt, row-range) → production.ymmp (60 VI) → production_patched.ymmp (face 133 changes) → YMM4 visual proof OK。全編にわたって表情切替を確認。**茶番劇 E2E (2026-04-13)**: face 138 + idle_face 16 + slot 10 + motion 6 を IR → apply-production → YMM4 で実証。正本 [CHABANGEKI-E2E-PROOF-2026-04-13.md](verification/CHABANGEKI-E2E-PROOF-2026-04-13.md)
- last_e2e_data: AI監視(60 VoiceItem) の production.ymmp + chabangeki_e2e_ir.json (28 utt, row-range + idle_face + slot + motion) + face_map + slot_map_e2e + tachie_motion_map_e2e
- external_tool_verification: YMM4 visual proof OK (2026-04-13)。Phase 1 (face + idle_face) および Phase 2 (+ slot + motion) ともに PASS。実運用フィードバック: 表情はテンプレ指定のほうが実用的、speaker マッピングの左右逆転が発生
- final_artifact_reached: Yes (CSV → YMM4 台本読込 → IR → patch-ymmp → 表情差し替え済み ymmp)
- blocking_dependency: なし。face は `FACE_UNKNOWN_LABEL` / `PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE`_* / `FACE_MAP_MISS` / `IDLE_FACE_MAP_MISS` / `VOICE_NO_TACHIE_FACE` の failure class か、最終 creative judgement NG のときだけ再オープン

## FEATURE_REGISTRY 状態サマリ (2026-06-04 更新)

- done: 48件（G-24 基盤クローズを反映）
- approved: 2件（H-01, G-20）— G-27 は active approved から外し、case-specific evidence として hold に移した
- proposed: 2件（G-26 motion primitive grammar / compatibility probe、G-28 Reference-Driven Generic Screen Carrier）
- info: 2件（C-01, C-06）
- hold: 10件（A-03, D-02, E-01, E-02, **G-01, G-03, G-04, G-21, G-22, G-27**）
- quarantined: 2件（F-01, F-02）
- rejected: 7件（B-10, C-02, C-03, C-04, C-05, D-01, F-03）

## Python のスコープ制約（2026-03-30 確定、2026-04-28 境界補正）

Python の責務は CSV / IR / registry / 台本読込後 `.ymmp` patch の接着層に限定する。YMM4 が持つ制作機能を Python 側で再生成しない。

許容済み:

- CSV / 診断 JSON / manifest などの CLI artifact 生成
- H-01 packaging brief / H-02 `thumbnail_design` / 将来の YouTube metadata draft など、制作・投稿判断を支える機械可読 artifact 生成
- 台本読込後 `.ymmp` に対する限定 patch（face / bg / slot / overlay / se / motion / bg_anim / transition / skit_group / thumb.* など、capability matrix と feature registry で範囲が固定されたもの）
- repo-tracked YMM4 template source / registry / readback に基づく限定的な値差し替え

禁止:

- 画像生成・画像合成（PIL/Pillow 含む）
- `.ymmp` のゼロからの生成、YMM4 台本読込の代替、YMM4 GUI 操作
- YMM4 native template 資産の Python 生成、YMM4 出力の模倣・Python preview
- 動画レンダリング・音声合成

## 外部メディア取得の方針（2026-03-30）

- 取得機能（acquisition）と受け取り機能（receiving）は分離する
- 最終的に自動化したい（ユーザー指示）
- A-04（RSS）は再審査済みで done。2026-05-25 に OPML 購読一覧同期 v1 まで実装済み。旧 D-02（背景動画取得 / 素材 API）は汚染バッチ gate 下にあり、現在の D-02 は C-07 v3 吸収済み hold として扱う

## Authority Return Items

- G-02 done。IR 語彙定義 v1.0
- G-02b done。ymmp 構造解析完了。bg+face 差し替えが最小実用単位
- G-05 done。v4 proof 完了。Custom GPT が 28 utterances / 5 sections の IR を正常出力
- G-06 done。patch-ymmp 変換器 + extract-template 実装済み。実機検証 OK
- G-07 done。idle_face (待機中表情) TachieFaceItem 挿入。carry-forward + character-scoped 対応
- G-11 done。`slot` contract を `validate-ir` / `apply-production` / `patch-ymmp` に統合し、TachieItem X/Y/Zoom の deterministic patch と `off` hide を CLI/readback まで閉じた
- G-12 completed。`measure-timeline-routes` CLI で ymmp から `VideoEffects` / `Transition` / template candidate route を readback でき、`--expect` / `--profile` で route contract miss と profile mismatch を検出できるようにした
- G-12 contract fixed。`docs/verification/G12-timeline-route-measurement.md` と `samples/timeline_route_contract.json` により、repo-local corpus では `motion=TachieItem.VideoEffects`、`bg_anim=ImageItem.X/Y/Zoom`、effect-bearing bg=`ImageItem.VideoEffects`、fade-family `transition`=`VoiceItem.VoiceFadeIn/Out` / `VoiceItem.JimakuFadeIn/Out` / `TachieItem.FadeIn/Out` まで mechanical に確定した
- G-12 corpus audit。repo-local `.ymmp` 16 本を測定し、fade-family `transition` route は production/probe sample で観測、`template` route は 0 件であることを確認。未確定は non-fade / template-backed transition family のみ
- G-13 done。`overlay` は `--overlay-map` から deterministic な `ImageItem` 挿入まで閉じ、`OVERLAY_UNKNOWN_LABEL` / `OVERLAY_MAP_MISS` / `OVERLAY_NO_TIMING_ANCHOR` / `OVERLAY_SPEC_INVALID` を mechanical failure として扱える
- G-13 done。`se` は `--se-map` で label と timing anchor を解決し、G-18 で `AudioItem` 挿入まで実装。機械的失敗は `SE_UNKNOWN_LABEL` / `SE_MAP_MISS` / `SE_NO_TIMING_ANCHOR` / `SE_SPEC_INVALID`
- G-18 done。`_apply_se_items` が既存 `AudioItem` テンプレまたは最小骨格で SE を挿入。`PatchResult.se_plans` は挿入件数
- G-14 done。`samples/timeline_route_contract.json` の `production_ai_monitoring_lane` で [samples/production.ymmp](samples/production.ymmp) の motion/transition を contract pass。bg_anim は本 ymmp に ImageItem 無しのため required 外
- G-23 done。`motion` preset library は `speaker_tachie` 専用として固定。茶番劇演者の主経路には使わない
- G-24 done。茶番劇演者の主経路を **GroupItem template-first** に切り替え、canonical template → 小演出量産 → production で template 解決 + fallback + manual note を正本化。Real Estate DX 固有の review cycle は G-27 へ分離
- timeline packet: G-11 slot patch hardening 完了 → G-12 timeline route measurement packet 完了 → G-13 overlay / se insertion packet 完了。timeline 編集は broad retry loop に戻さず、packet ごとに failure class / readback / boundary を定義して扱う
- H-01 dry proof 済み。`docs/verification/H01-packaging-orchestrator-ai-monitoring-dry-proof.md` により、brief が title / thumbnail / script の共有契約として機能することを repo-local artifact ベースで確認した。strict な before/after GUI rerun proof はまだ残る
- H-02 done (2026-04-06)。dry proof + strict GUI rerun proof pass。4/5案が preferred_specifics を使用、banned pattern なし、Specificity Ledger・Brief Compliance Check 出力確認済み。コピー品質の実用改善は別課題
- H-03 done。`score-visual-density` CLI + GUI 品質診断。dry proof は `docs/verification/H03-visual-density-ai-monitoring-proof.md`
- H-04 done。`score-evidence` CLI + GUI 品質診断。manual proof は `docs/verification/H04-evidence-richness-ai-monitoring-proof.md`
- B-18 done。`diagnose-script` + `docs/SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md`。dry proof `docs/verification/B18-script-diagnostics-ai-monitoring-sample.md`
- C-09 done。`docs/S1-script-refinement-prompt.md` + gui-llm-setup-guide 導線
- H-02 closed。packaging: H-02/H-03/H-04 は実装済み。H-01 は approved（schema + dry proof、運用で brief 固定）。timeline は新 sample または known failure class が出たときだけ再オープンする
- G-01/G-03: hold (タイムライン操作 API 非公開)
- G-05 v4 prompt doc が canonical。remote Custom GPT Instructions 側の drift は `PROMPT_FACE_DRIFT` / `FACE_PROMPT_PALETTE`_* で検出する
- D-02: hold (C-07 v3 に吸収完了)
- E-01 / 旧 E-02 standalone: hold 継続。metadata draft は successor-lane として別起票可
- F-01/F-02: quarantined 継続

## 実制作ワークフロー自動化カバレッジ (2026-04-06 棚卸し)

FEATURE_REGISTRY 上 done 42 件だが、実際の動画制作ワークフロー全体に対するカバレッジは限定的。
ユーザーフィードバックに基づき、各工程の自動化状態と実際の重さを正確に記録する。

### 工程別カバレッジ


| #   | 工程                  | 担当                   | 自動化状態      | 実際の重さ   | 備考                                                                                       |
| --- | ------------------- | -------------------- | ---------- | ------- | ---------------------------------------------------------------------------------------- |
| 1   | 台本作成                | NotebookLM           | 外部ツール (手動) | **重い**  | NLM出力はそのまま使えない。下記「台本品質問題」参照                                                              |
| 2   | 台本→CSV変換            | build-csv CLI        | **自動**     | 軽い      | B-01〜B-17 で字幕分割品質も改善済み                                                                   |
| 3   | CSV→YMM4読込          | YMM4 台本読込            | 手動操作 (1回)  | 軽い      | C-01 (info) として記録済み                                                                      |
| 4   | 演出IR生成              | Custom GPT (C-07)    | 半手動 (コピペ)  | 中       | GPTへの入力と出力の受け渡しが手動                                                                       |
| 5   | IR→ymmp適用 | apply-production CLI / GUI 演出適用タブ | **一部自動** | 軽〜中 | face/bg/slot/overlay/se/motion/bg_anim/transition/skit_group は capability matrix 範囲で限定 patch 可能。GUI 露出は face/bg/skit_group 中心で、overlay/se/motion map 類は未露出 |
| 6   | **YMM4上の演出配置** | YMM4 + template-first tooling | **一部自動 / acceptance は手動** | **重い** | skit_group 基盤は repo-tracked template source → registry → analyzed placement → `.ymmp` readback まで到達。案件固有の最終 composition / 間隔 / テンポは G-27 などの review cycle と YMM4 creative acceptance に残る |
| 7   | **視覚効果・サムネ制作** | YMM4 / 人間 + 限定 patch 補助 | **補助あり / 生成なし** | **重い** | サムネは `thumbnail_design` sibling artifact + `thumb.*` template slot patch が最小入口。画像生成・PNG 書き出し・完成判断は自動化しない。実サムネ template proof は未完了 |
| 8   | レンダリング              | YMM4                 | 手動トリガー     | 軽い      | C-06 (info) として記録済み                                                                      |
| 9   | YouTube投稿           | YouTube Studio       | 手動         | 中       | E-01 と旧 E-02 standalone は hold。H-01/H-02/H-04 由来 metadata draft は successor-lane として別起票可 |


### 台本品質問題 (工程1の詳細)

NotebookLM で生成した台本には以下の構造的弱点があり、動画用に大きな手動調整が必要。資料を持っているのが NotebookLM である以上、これは前段ボトルネックとして扱い、CSV / IR 生成前に B-18 / C-09 / manual QC を挟む:

- **NLM臭**: NotebookLM特有の会話構造・語彙・展開パターンが残り、ゆっくり解説として不自然
- **誤字・誤変換**: 指示を理解しないまま出力し、固有名詞・専門語・日常語を壊すことがある
- **話者混同**: 聞き手 (れいむ) と解説 (まりさ) のセリフ担当が混同することがある
- **様式不適合**: ゆっくり解説の様式 (ボケツッコミ、視聴者への問いかけ、テンポ等) への最適化が必要
- **YT視聴者向け調整**: YouTube視聴者の離脱を防ぐ構成・フック・情報密度の調整が必要
- **演出IRとの連鎖**: 台本品質が低いと、C-07 で生成する演出IRの質も下がる。台本の構造が曖昧だと、演出指示も曖昧になる

### 演出配置の未自動化問題 (工程6の詳細)

現状の patch-ymmp / apply-production でできること:

- face (表情) の差し替え: 133 changes 実証済み
- bg (背景) のセクション切替: 2ラベルで実証済み
- slot (キャラ位置): X/Y/Zoom の deterministic patch
- overlay: deterministic な ImageItem 挿入
- se (SFX): fully implemented through `AudioItem` writes (G-18 done). Readback proof lives in `samples/AudioItem.ymmp` and `docs/verification/G13-overlay-se-insertion-packet.md`.
- motion / bg_anim / fade-family transition: capability matrix 範囲で write route 固定済み
- skit_group: template source / registry 解決 / analyzed placement / readback まで実装済み。creative acceptance は別

現状の patch-ymmp / apply-production でできないこと (= 手動または template authoring に残る部分):

- **素材の調達と準備**: 背景画像、図解素材、茶番劇用のキャラポーズ等の入手・加工
- **新規テンプレ authoring**: YMM4 native template と素材登録は人間が作る
- **最終レイアウト判断**: 画面上の間隔・テンポ・見栄えは creative acceptance
- **GUI 未露出 map 類**: overlay / se / motion / bg_anim / timeline-profile は production で必要化したら GUI 補完スライス
- **未登録の茶番劇 intent**: production gap が出た時だけ新テンプレとして起票
- **図解アニメーション**: 情報伝達のための図解・チャート等の動的表示

### 視覚効果の未実現 (工程7の詳細)

- サムネイルを 1枚も完成させていない
- 茶番劇風アニメーション: ゼロ (方向性のみ記録済み: feedback_nlmytgen_visual_direction)
- 図解アニメーション: ゼロ
- 現状は画像表示のみ
- H-02 の C-08 prompt は仕様準拠だがコピー品質が不足 (抽象煽りは抑えたが視聴者の感情フックが弱い)

### ギャップの構造

done 42 件の大半は「テキスト変換パイプライン」と「spec/proof整備」に集中している。
実際の動画制作で最も時間がかかる工程 (演出配置・視覚効果・台本品質) は未自動化または部分的。
packaging spec (H-01〜H-04) は判断支援フレームワークとして整備済みだが、
その出力を実際の制作物に変換する工程が手動のまま。

### YouTube投稿自動化の分離

E-01 と旧 E-02 standalone metadata template は動画制作ワークフローとは独立したタスクとして切り出す。
ただし、H-01/H-02/H-04 を入力にした YouTube metadata draft は、投稿自動化ではなく packaging artifact の successor-lane として再起票できる。制作パイプラインへ自動注入したり YouTube Studio 操作まで含める場合は、別 ID で integration point を明示する。

## 既知の問題

- 直前 handoff は 53f3718 時点の内容で止まっており、後続 commit `8a1c710` で追加された canonical docs とその未充足状態は含んでいなかった
- E-02 の旧 standalone metadata template は YouTube Studio への手入力をテキストファイル生成に置き換えるだけで弱い。ただし H-01/H-02/H-04 と接続する metadata draft は successor-lane として再起票可
- D-02 / F-01 / F-02 は前セッションの汚染バッチ由来で、個別精査前に normal backlog として扱えない。これは目的の禁止ではなく、再審査なしの通常復帰禁止
- A-04 は実装済み・再審査済みだが、runtime/context の一部に旧 `quarantined` 記述が残っていたため handoff trust を要再同期
- B-14 後の追加観測では、長すぎる行は大幅に減り、全字幕が 3 行以内に収まる水準まで改善した。残 pain は bulk overflow ではなく、境界ケースの改行品質に移っている
- B-11/B-12/B-13/B-14 により、辞書や timing ではなく字幕改行が支配的な pain だと確認。B-14 後は `ー`、カギ括弧、数値+記号などの individual judgement が主で、次は heuristic を積み増すより corpus-based な例収集へ寄せる方が自然
- 別機能の feasibility を棚卸しした結果、次の本命候補は S-6 LLM adapter。E-01/旧E-02 standalone は secondary、D-02/F-01/F-02 は引き続き汚染バッチ gate
- resume 用プロンプト正本は廃止済み。再開判断は `AGENTS.md` / `docs/REPO_LOCAL_RULES.md` / 本ファイルを起点に、必要な正本節だけを読む
- `group_motion` は `GROUP_MOTION_NO_GROUP_ITEM` / `GROUP_MOTION_TARGET_MISS` / `GROUP_MOTION_TARGET_AMBIGUOUS` を fatal 扱いに変更済み。運用側で `group_target` 命名規約（通常 `Remark`）のばらつきが残る場合は、次スライスで `validate-ir` lint を優先する。
- G-07 done。idle_face carry-forward により待機中表情を維持。TachieFaceItem 挿入で non-speaker キャラの表情を制御
- れいむの surprised が palette.ymmp に未定義でも、現在は `FACE_ACTIVE_GAP` / `FACE_LATENT_GAP` として事前に可視化される。これは data-side gap であり、face サブシステム自体の未完成を意味しない

## 2026-04-05 Linebreak Note

- Structural major/minor reflow redesign landed in B-17 path.
- Sample proof target: `samples/AI監視が追い詰める生身の労働.txt`
- Verified result: catastrophic screen breaks such as `では / なく`, `）」 / という`, `） / 」`, and `19 / 億` were reduced; residual issues remain around some `XというY` and quoted explanatory phrases.
- Additional tuning now suppresses sparse first lines created by short comma-led intros when a better particle or later-phrase break is available.
- Close-bracket/content fallback and page-plan comparison are now enabled so quoted labels like `「配送サービスパートナー（DSP）」 / プログラム...` and `「サンクマイドライバー」という / プログラム...` no longer force the earlier worse splits.
- Emergency inner-break candidates inside long quoted labels are now available as a last resort, but residual 41-48 width lines still remain and likely need either YMM4-aware width calibration or a stronger policy on splitting long quoted labels.
- Single-hiragana tails after quoted terms are now handled separately, which improved cases like `「アルゴリズムによる最適化」 / と聞くと...` without reopening `」`-at-line-start regressions.
- Page carry-over scoring now differs from in-page line breaks: `close+tail` boundaries and overflow-relief plans can win when an extra page removes the screen break without reopening `」` line-head regressions.
- Additional exact page-count candidates are now compared with their own ideal page width, which fixed the residual `完璧に計算されたアルゴリズムが生身の / 人間という...` class by allowing one more page when the earlier exact plan still overflowed.
- Current sample residuals are down to 2 lines in `_tmp_structural_balance.csv`: `誰の汗とリスクを動力にして回り始めるのかを / 解剖していくということですね。` and `自発的にリスクを取らせる罠のようなものです。 / データによると、`.
