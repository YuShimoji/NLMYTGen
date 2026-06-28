# Newsroom v0.1 Dense Script Package v1

artifact_id: newsroom_v0_1_dense_script_package_v1_2026_06_26
package_id: newsroom_v0_1_dense_script_package_v1_2026_06_26
schema_version: newsroom_v0_1_dense_script_package.v1
review_status: ready_for_operator_dense_source_import
production_status: diagnostic_only
business_goal_primary: understanding/adoption
diagnostic_only: true

## Identity

- package_id: newsroom_v0_1_dense_script_package_v1_2026_06_26
- source_explanation_readiness_path: samples/_probe/newsroom_handoff/v0_1_explanation_readiness_v1.json
- source_explanation_readiness_id: newsroom_v0_1_explanation_readiness_v1_2026_06_26
- source_script_density_plan_path: samples/_probe/newsroom_handoff/v0_1_script_density_plan_v1.json
- source_script_density_plan_id: newsroom_v0_1_script_density_plan_v1_2026_06_26
- source_baseline_csv_path: samples/_probe/newsroom_handoff/source_ymmp_recreation_import_v1.csv
- output_csv_path: samples/_probe/newsroom_handoff/v0_1_dense_source_ymmp_import_v1.csv
- output_timing_plan_path: samples/_probe/newsroom_handoff/v0_1_dense_caption_timing_plan_v1.json
- target_source_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v0_1_dense_source_v1.ymmp
- candidate_video_local_path_current_host: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.mp4
- candidate_video_exists_local: true
- production_status: diagnostic_only
- business_goal_primary: understanding/adoption
- actual_order_or_audience_acceptance_claimed: false

## Source Validation

- status: passed
- errors: []
- source_explanation_readiness_id: newsroom_v0_1_explanation_readiness_v1_2026_06_26
- source_script_density_plan_id: newsroom_v0_1_script_density_plan_v1_2026_06_26
- source_explanation_validation_status: passed
- baseline_line_count: 4
- baseline_speaker_values: ["ゆっくり霊夢"]
- baseline_csv_bom_verified: true
- new_line_count: 13
- new_line_count_in_plan_range: true
- target_duration_sec: 68
- target_duration_in_plan_range: true
- card_assets_dir_exists: true
- candidate_video_exists_local: true
- YMM4_launched_by_agent: false
- render_performed_by_agent: false
- cards_regenerated_in_this_slice: false

## Dense Script Lines

| line_id | segment_id | start | end | speaker | text | role | card |
|---|---|---|---|---|---|---|---|
| dense_line_001 | opening | 0 | 6 | ゆっくり霊夢 | This review-only sample proves a YMM4 video handoff can be assembled. | problem | card_1_point_overview |
| dense_line_002 | opening | 6 | 12 | ゆっくり霊夢 | The goal is not public news; it is a controllable production path. | offer | card_1_point_overview |
| dense_line_003 | mechanism | 12 | 17 | ゆっくり霊夢 | A tracked CSV becomes YMM4 dialogue with the same speaker binding. | mechanism | card_2_flow_mechanism |
| dense_line_004 | mechanism | 17 | 22 | ゆっくり霊夢 | The source project can be recreated without inventing hidden media. | mechanism | card_2_flow_mechanism |
| dense_line_005 | mechanism | 22 | 26 | ゆっくり霊夢 | That gives the next review a repeatable starting point. | transition | card_2_flow_mechanism |
| dense_line_006 | proof | 26 | 31 | ゆっくり霊夢 | Native Yukkuri audio stays in the YMM4 side of the workflow. | proof | card_3_check_proof |
| dense_line_007 | proof | 31 | 36 | ゆっくり霊夢 | The timing patch holds the sample near sixty-eight seconds. | proof | card_3_check_proof |
| dense_line_008 | proof | 36 | 42 | ゆっくり霊夢 | Four PNG cards appear as ImageItems on the timeline. | proof | card_3_check_proof |
| dense_line_009 | proof | 42 | 48 | ゆっくり霊夢 | A prior local render confirms cards, voice, and timing can stay together. | proof | card_3_check_proof |
| dense_line_010 | boundary | 48 | 53 | ゆっくり霊夢 | This is still diagnostic: fake topic, fake claims, and no public approval. | boundary | card_4_next_status |
| dense_line_011 | boundary | 53 | 58 | ゆっくり霊夢 | Real sources, rights, and final narration are outside this proof. | boundary | card_4_next_status |
| dense_line_012 | next_action | 58 | 63 | ゆっくり霊夢 | Next, import this denser script and save a dense source project. | next_action | card_4_next_status |
| dense_line_013 | next_action | 63 | 68 | ゆっくり霊夢 | After that, a real packet or RSS dry run can be planned with clearer proof. | next_action | card_4_next_status |

## Segment Map

| segment_id | title | purpose | target_time_range | line_ids | expected_viewer_understanding |
|---|---|---|---|---|---|
| opening | Opening / what this proves | name the diagnostic promise and controlled value path | {"end_sec": 12, "start_sec": 0} | ["dense_line_001", "dense_line_002"] | viewer understands this is a review-only handoff proof |
| mechanism | Mechanism / CSV to YMM4 | explain tracked CSV to YMM4 dialogue/source recreation | {"end_sec": 26, "start_sec": 12} | ["dense_line_003", "dense_line_004", "dense_line_005"] | viewer understands why the package is repeatable |
| proof | Proof / audio timing cards render | sequence native audio, timing, cards, and prior render evidence | {"end_sec": 48, "start_sec": 26} | ["dense_line_006", "dense_line_007", "dense_line_008", "dense_line_009"] | viewer understands what has actually been proven |
| boundary | Boundary / diagnostic only | keep fake/review-only limits explicit | {"end_sec": 58, "start_sec": 48} | ["dense_line_010", "dense_line_011"] | viewer understands this is not public or production approval |
| next_action | Next action / import then plan | point to dense YMM4 source import before RSS or real packet planning | {"end_sec": 68, "start_sec": 58} | ["dense_line_012", "dense_line_013"] | viewer understands what to ask for next |

## CSV Spec

- encoding: UTF-8 BOM
- python_encoding: utf-8-sig
- header: false
- columns: ["speaker", "text"]
- row_count: 13
- yym4_import_mode: 蜿ｰ譛ｬ隱ｭ霎ｼ
- expected_character_binding: ゆっくり霊夢
- prompt_speaker_text_seen: 繧・▲縺上ｊ髴雁､｢
- prompt_speaker_encoding_note: supervisor prompt speaker text was mojibake; CSV uses the existing canonical UTF-8 speaker value from the committed source import CSV
- target_source_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v0_1_dense_source_v1.ymmp
- rows: [{"line_id": "dense_line_001", "row_number": 1, "speaker": "ゆっくり霊夢", "text": "This review-only sample proves a YMM4 video handoff can be assembled."}, {"line_id": "dense_line_002", "row_number": 2, "speaker": "ゆっくり霊夢", "text": "The goal is not public news; it is a controllable production path."}, {"line_id": "dense_line_003", "row_number": 3, "speaker": "ゆっくり霊夢", "text": "A tracked CSV becomes YMM4 dialogue with the same speaker binding."}, {"line_id": "dense_line_004", "row_number": 4, "speaker": "ゆっくり霊夢", "text": "The source project can be recreated without inventing hidden media."}, {"line_id": "dense_line_005", "row_number": 5, "speaker": "ゆっくり霊夢", "text": "That gives the next review a repeatable starting point."}, {"line_id": "dense_line_006", "row_number": 6, "speaker": "ゆっくり霊夢", "text": "Native Yukkuri audio stays in the YMM4 side of the workflow."}, {"line_id": "dense_line_007", "row_number": 7, "speaker": "ゆっくり霊夢", "text": "The timing patch holds the sample near sixty-eight seconds."}, {"line_id": "dense_line_008", "row_number": 8, "speaker": "ゆっくり霊夢", "text": "Four PNG cards appear as ImageItems on the timeline."}, {"line_id": "dense_line_009", "row_number": 9, "speaker": "ゆっくり霊夢", "text": "A prior local render confirms cards, voice, and timing can stay together."}, {"line_id": "dense_line_010", "row_number": 10, "speaker": "ゆっくり霊夢", "text": "This is still diagnostic: fake topic, fake claims, and no public approval."}, {"line_id": "dense_line_011", "row_number": 11, "speaker": "ゆっくり霊夢", "text": "Real sources, rights, and final narration are outside this proof."}, {"line_id": "dense_line_012", "row_number": 12, "speaker": "ゆっくり霊夢", "text": "Next, import this denser script and save a dense source project."}, {"line_id": "dense_line_013", "row_number": 13, "speaker": "ゆっくり霊夢", "text": "After that, a real packet or RSS dry run can be planned with clearer proof."}]

## Baseline Comparison

- baseline_line_count: 4
- new_line_count: 13
- baseline_seconds_per_line: 17.0
- new_seconds_per_line: 5.23
- expected_density_improvement: moves from sparse mechanics proof to five-segment explanation path
- what_is_added: {"boundary": "fake diagnostic status and no public approval", "next_action": "dense source import/save before RSS or real packet planning", "offer": "a controllable CSV-to-YMM4 production path", "problem": "why this handoff proof matters to review", "proof_sequence": "speaker binding, audio side, timing, PNG cards, prior render"}

## Explanation Readiness Recheck

| gate | status | evidence | decision |
|---|---|---|---|
| problem_clear | pass | opening states what the sample proves and why it exists | ready for dense source import proof |
| offer_clear | pass | mechanism segment names tracked CSV to YMM4 dialogue/source recreation | offer is clear enough for review-only v0.1 |
| proof_clear | pass | proof segment sequences native audio, timing, PNG cards, and prior local render | proof is still diagnostic but understandable |
| boundary_clear | pass | boundary segment states fake topic, fake claims, no public approval, and source limits | do not loosen diagnostic-only wording |
| next_action_clear | pass | closing lines point to dense import/save, then RSS dry run or real packet planning | newsroom-v0.1-dense-source-ymmp-operator-instruction-v1 |
| audience_fit_proxy | partial | script is denser and clearer, but no real viewer or order acceptance was measured | keep L1 internal judgement only |
| visual_supports_explanation | pass | existing four card roles can carry opening, mechanism, proof, and boundary/next action | do not regenerate cards in this slice |

## Card Alignment Summary

- existing_card_count: 4
- new_segment_count: 5
- line_ids_by_card: {"card_1_point_overview": ["dense_line_001", "dense_line_002"], "card_2_flow_mechanism": ["dense_line_003", "dense_line_004", "dense_line_005"], "card_3_check_proof": ["dense_line_006", "dense_line_007", "dense_line_008", "dense_line_009"], "card_4_next_status": ["dense_line_010", "dense_line_011", "dense_line_012", "dense_line_013"]}
- next_action_segment_handling: carried_by_card_4_next_status
- future_card_count_expansion_needed_for_this_slice: false
- future_card_count_expansion_note: a separate fifth card may help if final content adds a larger offer/proof split, but this dense import can use the current four cards
- cards_regenerated_in_this_slice: false

## Not Accepted Scope

- render_proof_for_dense_script: false
- audio_proof_for_dense_script: false
- production_readiness: false
- public_readiness: false
- real_rss_or_news_content: false
- real_source_approval: false
- final_narration_quality: false
- automated_yym4_render_claim: false
- actual_order_or_audience_acceptance: false

## Next Recommended Slice

- selected: newsroom-v0.1-dense-source-ymmp-operator-instruction-v1
- reason: the dense CSV is ready; the next useful proof is user-side YMM4 import and saving an ignored dense source project

## Goal Stack

| level | goal | success_signal | contribution |
|---|---|---|---|
| Immediate | Create denser review-only script package | 10-14 line CSV/JSON/doc exist | fixes sparse explanation |
| Short-term | Prepare YMM4 dense import | user can import CSV and save dense source .ymmp | moves from plan to executable artifact |
| Mid-term | Render dense v0.1 | dense narration can be tested with native YMM4 audio and cards | improves internal review value |
| Long-term | Prepare RSS dry run | pipeline has script structure before real content integration | reduces manual assembly |

## Completion Matrix

| gate | status |
|---|---|
| current_repo_state_verified | true |
| explanation_script_density_plan_inspected | true |
| dense_script_package_generated | true |
| YMM4_import_CSV_generated | true |
| explanation_readiness_re_evaluated | true |
| narrow_commit_created_and_pushed_if_push_gate_passes | ready_for_git_followthrough |

## Artifact Readiness

| gate | status |
|---|---|
| dense_script_JSON_exists | true |
| dense_timing_caption_JSON_exists | true |
| dense_CSV_exists | true |
| human_docs_exist | true |
| baseline_comparison_present | true |
| downstream_next_use_described | true |

## Business / Explanation Readiness

| gate | status |
|---|---|
| problem_clear | pass |
| offer_clear | pass |
| proof_clear | pass |
| boundary_clear | pass |
| next_action_clear | pass |
| audience_fit_proxy | partial |
| visual_supports_explanation | pass |

## Render Gate Hygiene

| gate | status |
|---|---|
| no_render_performed_by_agent | true |
| existing_render_evidence_reused | true |
| no_render_for_script_package_creation | true |
| next_render_tied_to_dense_YMM4_import_source_proof | true |
| repeated_render_loop_avoided | true |
| output_first_principle_preserved | true |

## Human Burden Hygiene

| gate | status |
|---|---|
| user_input | freeform |
| template_required | false |
| schema_owner | Agent |
| user_side_work | none_for_this_slice |
| future_review_look_for_count | <=3 |
| negative_confirmation_checklist | false |
| fixed_form_relapse | false |

## Inertia Check

| gate | status |
|---|---|
| no_visual_polish_loop | true |
| no_render_automation_rabbit_hole | true |
| no_packet_for_packet_drift | true |
| business_explanation_goal_preserved_above_visual_polish | true |
| next_concrete_YMM4_import_milestone_named | true |

## Boundaries

- YMM4_launched_by_agent: false
- render_performed_by_agent: false
- ymmp_edited_or_committed: false
- audio_tts_generated: false
- cards_regenerated: false
- real_rss_or_news_fetched: false
- real_brands_urls_screenshots_or_media_used: false
- production_public_readiness_claimed: false
- actual_audience_acceptance_claimed: false
- fixed_review_form_requested: false
- dashboard_governance_freshness_drift: false

## Boundary Note

This package is review-only and diagnostic. It does not launch YMM4, render, edit `.ymmp`, generate audio/TTS, regenerate cards, fetch real RSS/news, or claim production/public/audience acceptance.
