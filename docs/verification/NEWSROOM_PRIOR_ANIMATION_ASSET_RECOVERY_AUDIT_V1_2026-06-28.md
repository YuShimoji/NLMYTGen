# Newsroom Prior Animation Asset Recovery Audit v1

artifact_id: newsroom_prior_animation_asset_recovery_audit_v1_2026_06_28
schema_version: newsroom_prior_animation_asset_recovery_audit.v1
production_status: diagnostic_only


## Audit Scope

- searched_repo_root: C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage
- external_reference_fetch_performed: false
- YMM4_launched: false
- render_performed: false
- ymmp_edited: false

## Asset Access Findings

| asset_id | repo_relative_path | target_exists | git_state | access_state |
|---|---|---|---|---|
| reimu_expression_easy | samples/characterAnimSample/reimu_easy.png | true | tracked | tracked_repo_artifact_exists |
| reimu_expression_anger | samples/characterAnimSample/reimu_anger.png | true | tracked | tracked_repo_artifact_exists |
| reimu_expression_panic | samples/characterAnimSample/reimu_panic.png | true | tracked | tracked_repo_artifact_exists |
| reimu_expression_shocked | samples/characterAnimSample/reimu_shocked.png | true | tracked | tracked_repo_artifact_exists |
| reimu_expression_surprised | samples/characterAnimSample/reimu_surprised.png | true | tracked | tracked_repo_artifact_exists |
| character_body_source | samples/characterAnimSample/Gemini_Generated_Image_kfezhpkfezhpkfez-removebg-preview.png | true | tracked | tracked_repo_artifact_exists |
| face_map_bundle_default | samples/face_map_bundles/default.json | true | tracked | tracked_repo_artifact_exists |
| face_map_bundle_haitatsuin | samples/face_map_bundles/haitatsuin.json | true | tracked | tracked_repo_artifact_exists |
| face_map_extracted | samples/characterAnimSample/face_map_extracted.json | true | tracked | tracked_repo_artifact_exists |
| nod_head_probe | samples/nod_head.ymmp | true | tracked | tracked_repo_artifact_exists |
| skit_group_template_source | samples/templates/skit_group/delivery_v1_templates.ymmp | true | tracked | tracked_repo_artifact_exists |
| skit_group_registry | samples/registry_template/skit_group_registry.template.json | true | tracked | tracked_repo_artifact_exists |
| group_motion_map | samples/group_motion_map.example.json | true | tracked | tracked_repo_artifact_exists |
| motion_recipe_brief | samples/recipe_briefs/g26_nod_head_v1_brief.v2.json | true | tracked | tracked_repo_artifact_exists |
| background_skit_blueprint_example | samples/_probe/g24/real_estate_dx_background_skit_blueprint.json | true | tracked | tracked_repo_artifact_exists |
| background_skit_blueprint_validation | samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json | true | tracked | tracked_repo_artifact_exists |
| primitive_visibility_readback | samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe_readback.json | true | tracked | tracked_repo_artifact_exists |

## Doc Access Findings

| asset_id | repo_relative_path | target_exists | git_state | access_state |
|---|---|---|---|---|
| background_skit_blueprint_validator | src/pipeline/background_skit_blueprint.py | true | tracked | tracked_repo_artifact_exists |
| skit_group_placement | src/pipeline/skit_group_placement.py | true | tracked | tracked_repo_artifact_exists |
| motion_recipe | src/pipeline/motion_recipe.py | true | tracked | tracked_repo_artifact_exists |
| skit_group_template_spec | docs/SKIT_GROUP_TEMPLATE_SPEC.md | true | tracked | tracked_repo_artifact_exists |
| scene_bible | docs/PILOT_YUKKURI_THEATER_SCENE_BIBLE.md | true | tracked | tracked_repo_artifact_exists |
| blueprint_workflow | docs/BACKGROUND_SKIT_BLUEPRINT_TIMETABLE_WORKFLOW.md | true | tracked | tracked_repo_artifact_exists |
| feature_registry | docs/FEATURE_REGISTRY.md | true | tracked | tracked_repo_artifact_exists |
| status_handoff_rules | docs/ai/STATUS_AND_HANDOFF.md | true | tracked | tracked_repo_artifact_exists |

## Branch Findings

| ref | access_state | evidence |
|---|---|---|
| codex/g24-enter-from-left-template-proof | current_or_local_branch_reference | git branch -a pattern search |
| codex/g24-nod-sync-adoption | current_or_local_branch_reference | git branch -a pattern search |
| remotes/origin/codex/g24-nod-sync | remote_branch_reference_found_not_checked_out | git branch -a pattern search |
| remotes/origin/codex/g24-nod-sync-adoption | remote_branch_reference_found_not_checked_out | git branch -a pattern search |
| remotes/origin/codex/g27-readback-ymmp-write-gate | remote_branch_reference_found_not_checked_out | git branch -a pattern search |
| remotes/origin/feat/phase2-motion-segmentation | remote_branch_reference_found_not_checked_out | git branch -a pattern search |

## Log Findings

| commit | subject |
|---|---|
| 9018629 | On codex/g24-nod-sync-adoption: pre-single-task-cleanup-real-estate-dx-2026-05-10 |
| ffeda44 | index on codex/g24-nod-sync-adoption: e0e49f9 docs: reduce agent entrypoint authority |
| 2325036 | untracked files on codex/g24-nod-sync-adoption: e0e49f9 docs: reduce agent entrypoint authority |
| 946fb42 | Harden background skit blueprint gate and handoffs |
| 7be55d6 | feat: stabilize g26 nod recipes |
| 00b2676 | feat(g26): close G-25 acceptance, propose G-26 preflight with route readback note |
| 87bf2c7 | feat(g24): wire skit group placement through gui |
| 83908ee | Add G-24 skit group placement automation |
| 6ff9745 | feat: validate G-24 skit group production flow |
| 0aee837 | Sync G-24 starter export proof and atlas |
| b2d4ed6 | Add G-24 skit preflight and canonical anchor docs |
| 4755e83 | feat(motion-library): v2 に更新 — flat + animation params 両方埋め、汎用台帳化 |
| 83dc870 | docs: skit_group 配下を ImageItem 重ね合わせに構造固定 |
| 399aa1a | docs: handoff — G-24 user 作業待ち状態を runtime-state + context に反映 |
| 1b45ff2 | feat(G-23/G-24): motion_target routing + skit group template spec |
| e2ee27d | feat(B-2/face-map/visual-slice): haitatsuin dry-run PASS + 6 表情拡張 + Step 3 user docs |
| 184ad2e | docs: G-19 done 記録 + TACHIE-BODY-FACE-SWAP-PREP チェック更新 |
| e4b6d49 | feat(G-19): GUI に --face-map-bundle ファイル選択を追加 |
| 0b71142 | feat(G-19): multi-body face_map bundle — carry-forward, CLI, patch, tests |
| 00bb5c7 | docs: face completion 固定 + H-01 Packaging Orchestrator spec v0.1 + ロードマップ整理 |
| 473885a | feat: face completion hardening (prompt drift, active gap, row-range integrity, fail-fast) |
| 7fffc8d | feat: G-06~G-10 実装 (extract-template --labeled, idle_face, apply-production, annotate-row-range, validate-ir) |
| 7825bbc | feat: extract-template コマンド追加 (face_map/bg_map 自動抽出) |

## Classification

- head_body_separated_assets_exist: true
- expression_parts_exist: true
- previous_animation_project_docs_or_branches_exist: true
- assets_are_tracked_or_repo_local: true
- asset_status: mixed_but_enough_for_first_probe
- unknowns: ["final newsroom cast design", "dedicated speech balloon style", "which prior skit templates should be reused for newsroom", "production animation quality"]

## Recovery Plan

| step | action | owner |
|---|---|---|
| source_lock | pin tracked assets and docs used by the first primitive proof | agent |
| primitive_probe | create a no-render diagnostic proof plan for nod, expression, move, and balloon | agent |
| user_visual_acceptance_later | only after generated proof exists, use YMM4 review for visual acceptance | user |

## Not Accepted Scope

- render_proof: false
- ymmp_mutation: false
- production_animation_quality: false
- public_upload_or_public_readiness: false
- real_rss_or_news_integration: false
- external_reference_video_fetch: false
- copied_external_visuals: false
- actual_order_or_audience_acceptance: false

## Boundaries

- YMM4_launched_by_agent: false
- render_performed_by_agent: false
- ymmp_edited_or_committed: false
- audio_tts_generated: false
- cards_regenerated: false
- real_rss_or_news_fetched: false
- external_reference_videos_fetched: false
- production_public_readiness_claimed: false
- actual_audience_acceptance_claimed: false
