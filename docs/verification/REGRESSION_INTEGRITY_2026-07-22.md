# 回帰整合性 clean-room 実行報告 — 2026-07-22

## 今回閉じた範囲

監修ログが許可した `NLM-REGINT-CLEANROOM-001@1` の支援作業だけを、
`9ed7cdf676cc0f9a9745350635bd29686639a963` から分離した
`codex/nlmytgen-regression-integrity-v1` で実施した。製品状態、承認済みコンテンツ、
生成済み visual artifact、receipt、manifest、人間レビューの gate は変更していない。
YMM4、ブラウザ、音声、ネットワーク、.NET、外部サービスは起動していない。

| 実行面 | 実体 | 判断上の意味 |
|---|---|---|
| 隔離先 | `C:\Users\PLANNER007\NLMYTGen-regression-integrity-v1` | main checkout と製品 artifact を直接使うテストを分離した |
| exact base | `9ed7cdf676cc0f9a9745350635bd29686639a963` | 開始時の branch tip と remote tip が一致していた |
| 環境再現 | `uv sync --extra dev --locked` 成功 | pytest を lock 解決済み環境で実行した |
| lock の由来 | main checkout にだけ存在した ignored `uv.lock` を同一バイトで隔離先へコピー | SHA-256 `40e64f793775f0b0181f5ba8972c17842717dbe14bc8c0a6c0cabd14442435d0`。lock は未追跡のため、新規 clean-room 単独再現には既知の不足が残る |
| 外部効果 | push / PR / merge / message / upload なし | 監修前に remote や他者の作業面を動かしていない |

上表の lock hash は大文字小文字を区別しない SHA-256 表記であり、実測値は
`40E64F793775F0B0181F5BA8972C17842717DBE14BC8C0A6C0CABD14442435D0` である。

## baseline で再現した35失敗

監修ログ指定の16モジュールは初回に `160 collected / 121 passed / 4 skipped /
35 failed` だった。初回実行中、current worktree を直接使う generator test が
`reference_grounded_visual_design/README_REFERENCE_GROUNDED_VISUAL_DESIGN.md`
から8行を削除し、後続2テストを連鎖的に失敗させた。8行は exact 内容で復元し、
以後の generator test は `tmp_path` 内の package copy だけを使うようにした。

### 生成済み review document を source body と誤認した契約 — 21件

現在の pilot には正規の下流 review HTML がある一方、authoritative package validator
が package 配下の全 HTML/PDF を入力 source body とみなしていた。既知の生成先だけを
source-body 検査から分離し、その他の位置にある HTML/PDF は従来どおり fail-close とした。

- `tests/test_content_transformation_lineage.py::test_approved_file_drift_stops_operator_preflight_without_launch`
- `tests/test_content_transformation_lineage.py::test_lineage_build_is_byte_deterministic`
- `tests/test_content_transformation_lineage.py::test_mechanical_speaker_projection_preserves_text_and_approval`
- `tests/test_content_transformation_lineage.py::test_receipt_and_lineage_drift_stop_operator_preflight`
- `tests/test_new_banknote_yymm4_existing_evidence_revalidation.py::test_approved_csv_drift_is_rejected_before_evidence_acceptance`
- `tests/test_new_banknote_yymm4_existing_evidence_revalidation.py::test_current_lock_and_existing_evidence_pass_without_source_mutation`
- `tests/test_new_banknote_yymm4_existing_evidence_revalidation.py::test_deterministic_sanitized_artifacts_and_cli`
- `tests/test_new_banknote_yymm4_existing_evidence_revalidation.py::test_evidence_mutation_during_read_is_rejected`
- `tests/test_new_banknote_yymm4_existing_evidence_revalidation.py::test_existing_note_is_observed_not_verified`
- `tests/test_new_banknote_yymm4_existing_evidence_revalidation.py::test_output_cannot_overlap_ignored_evidence_directory`
- `tests/test_new_banknote_yymm4_existing_evidence_revalidation.py::test_project_cue_speaker_and_order_drift_is_rejected`
- `tests/test_new_banknote_yymm4_existing_evidence_revalidation.py::test_result_project_hash_mismatch_is_rejected`
- `tests/test_new_banknote_yymm4_existing_evidence_revalidation.py::test_version_mismatch_is_warning_only_and_no_launch_path_exists`
- `tests/test_new_banknote_yymm4_import_intake_visual_decision.py::test_audit_fails_closed_on_result_failure`
- `tests/test_new_banknote_yymm4_import_intake_visual_decision.py::test_tracked_outputs_match_pure_renderer_and_freeze_script_hashes`
- `tests/test_new_banknote_yymm4_import_operator_batch.py::test_cli_preflight_writes_explicit_utf8_json`
- `tests/test_new_banknote_yymm4_import_operator_batch.py::test_collect_only_powershell_fixture_validates_9_3_6_and_timing`
- `tests/test_new_banknote_yymm4_import_operator_batch.py::test_collector_fails_on_character_text_and_order_drift`
- `tests/test_new_banknote_yymm4_import_operator_batch.py::test_collector_requires_fresh_exact_target_and_mapping_confirmation`
- `tests/test_new_banknote_yymm4_import_operator_batch.py::test_tracked_operator_batch_is_byte_deterministic_and_preflight_passes`
- `tests/test_new_banknote_yymm4_import_operator_batch.py::test_wrong_character_fails_without_inventing_missing_or_duplicate_cues`

### operator result の既知追加checkを拒否した契約 — 3件

collector が追加済みの3 checkを intake audit の旧 exact-set が拒否していた。
17の必須checkを維持し、既知の追加3 checkだけを許可した。未知checkを追加すると
`RESULT_CHECK_SET_DRIFT` で拒否する回帰テストも追加した。

- `tests/test_new_banknote_yymm4_import_intake_visual_decision.py::test_audit_fails_closed_on_project_text_drift`
- `tests/test_new_banknote_yymm4_import_intake_visual_decision.py::test_fixture_build_is_deterministic_and_byte_preserving`
- `tests/test_new_banknote_yymm4_import_intake_visual_decision.py::test_read_only_audit_verifies_success_and_preserves_local_bytes`

### ignored/private evidence がない clean-room では実行不能 — 5件

portable contract と private evidence availability を別テストへ分割した。後者は
`requires_local_evidence:<artifact-class>:missing=<exact-locators>` を JUnit に残し、
証跡がある同一マシンでは通常どおり実行される。

- `tests/test_editorial_provenance.py::test_render_and_second_build_are_byte_deterministic`
- `tests/test_new_banknote_reference_layout_reconstruction.py::test_ignored_local_surfaces_are_present_ignored_and_untracked`
- `tests/test_new_banknote_reference_layout_reconstruction.py::test_six_actual_surface_traces_cover_all_cohorts_and_visual_geometry`
- `tests/test_new_banknote_route_a_visual_proof.py::test_approved_content_original_proposal_and_ignored_evidence_are_unchanged`
- `tests/test_new_banknote_successor_selective_integration.py::test_integrated_json_html_privacy_and_local_binary_boundaries`

### historical receipt を current state と比較していた — 2件

履歴上の判断を検証するテストは、その receipt を確定した revision の blob と比較するようにした。
current state の更新を過去契約の破損として扱わない一方、当時の byte identity は引き続き検証する。

- `tests/test_new_banknote_reference_grounded_visual_design.py::test_state_docs_point_to_the_reference_grounded_human_gate` — `649ada5050be5b9b2153c50c938d855797d5c19f`
- `tests/test_new_banknote_successor_selective_integration.py::test_exact_partition_hashes_and_exclusions_are_accounted_for` — `d38075b97efabc99d1a23e8e0afafd5d44f1e2de`

### current worktree 実行とその連鎖影響 — 4件

generator は temp copy で二回生成し、そのcopy内の全ファイルhashが一致することを検査する。
過去stateとの結合は当時の revision に固定した。これにより generator 自身と後続テストの
順序依存を除去した。

- `tests/test_new_banknote_reference_grounded_visual_design.py::test_local_research_media_are_ignored_and_absent_from_tracked_proof`
- `tests/test_new_banknote_reference_grounded_visual_design.py::test_machine_outputs_parse_readback_passes_and_generation_is_deterministic`
- `tests/test_new_banknote_reference_layout_reconstruction.py::test_exact_base_and_all_preexisting_pilot_content_are_unchanged`
- `tests/test_new_banknote_route_a_visual_proof.py::test_generation_is_deterministic_and_state_is_review_ready`

## 実装後の固定ゲート

`scripts/check_regression_integrity.py` は指定16モジュールを列挙してから pytest を実行し、
外部temp directoryのJUnit XMLから pass/fail/error/skip と skip class を集計する。
実行前後に次の3値をバイト列で比較し、どれかが変われば pytest が通っても runner 自体を失敗させる。

- `git status --porcelain=v1 --untracked-files=all`
- `git diff --binary`
- `git diff --cached --binary`

最終差分に対する連続二回の結果は同値だった。

| 検査 | 1回目 | 2回目 |
|---|---:|---:|
| collected | 166 | 166 |
| passed | 157 | 157 |
| failed / errors | 0 / 0 | 0 / 0 |
| skipped | 9 | 9 |
| elapsed | 60.348秒 | 57.945秒 |
| status / diff / cached diff | 全て不変 | 全て不変 |

skip 9件はすべて exact locator 付きの local-evidence class になった。

| evidence class | 件数 | locator |
|---|---:|---|
| `historical_yymm4_import_evidence` | 3 | `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/local_outputs/new_banknote_yymm4_import_observation.local.ymmp`<br>`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/local_outputs/operator_batch.local.json`<br>`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/local_outputs/operator_result.json` |
| `notebooklm_audio_raw_packet` | 1 | `production_pilots/yukkuri_newsroom_content_spine_002/real_input_intake_readiness/real_input/transcript/new_banknote_notebooklm/raw/notebooklm_audio_overview_transcript_raw.txt`<br>`production_pilots/yukkuri_newsroom_content_spine_002/real_input_intake_readiness/real_input/transcript/new_banknote_notebooklm/capture_manifest.json` |
| `notebooklm_lexical_topic_line_map` | 3 | `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/local_outputs/raw_line_map.json` |
| `reference_layout_review_surfaces` | 1 | `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_layout_reconstruction/local_reference_trace_board.html`<br>`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_layout_reconstruction/local_reference_proxy_preview.html`<br>`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_layout_reconstruction/local_reference_traces`<br>`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_layout_reconstruction/local_render_inspection`<br>`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_layout_reconstruction/local_browser_profile` |
| `reference_layout_trace_captures` | 1 | `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_grounded_visual_design/local_reference_captures/O01_npb_hologram.jpg`<br>`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_grounded_visual_design/local_reference_captures/O02_boj_annotated_note.png`<br>`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_grounded_visual_design/local_reference_captures/J03_tbs_mbs.png`<br>`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_grounded_visual_design/local_reference_captures/J05_fnn.png`<br>`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_grounded_visual_design/local_in_video_observations/Y01_t0030_cdp.png`<br>`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/reference_grounded_visual_design/local_in_video_observations/Y02_t0030_cdp.png` |

既存の focused gate は `46 passed in 0.93s`、`scripts/check_project_state_sync.py` は
`PASS: project state is synchronized` だった。

## 人間判断までに残る境界

今回の結果は「広域回帰の機械判定が clean-room で再現可能になった」ことだけを示す。
人間による代表MP4の内部視聴、画面品質、音声、編集テンポの受け入れは代替しておらず、
`human-internal-review` gate はそのままである。監修AIによるこの差分の受け入れも未取得である。

次の入口は、異なる摩擦を解く次の4つに分かれる。

| 入口 | 減らす摩擦 | 選ぶと可能になること |
|---|---|---|
| Verify — このlocal commitを監修AIが差分監査 | 回帰ゲート自体への信頼不足 | 支援missionを受理し、人間レビューへ判断材料を渡せる |
| Advance — 人間が代表MP4を最初から最後まで内部視聴 | North Star に残る最大の未判定 | accept または scene/cue-specific revision を確定できる |
| Audit — 許可された同一マシンで9件のlocal evidence testを再実行 | skipされた私有証跡の可用性不確実性 | `166 passed / 0 skipped` を目指せる。証跡自体は追跡・移送しない |
| Excise — `uv.lock` の正本化方針を別判断する | 新しいclean-roomが単独でlocked syncできない | lockコピー不要の再現手順へ進める。依存artifact方針なので今回のscope外 |
