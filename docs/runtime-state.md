# Runtime State — NLMYTGen

# BLOCK SUMMARY のたびに更新する。

# compact 後の再アンカリングではこのファイルを読む。

## 現在位置

ドキュメント地図（任意）: [NAV.md](NAV.md) / Electron 最小経路・検証ラダー: [GUI_MINIMUM_PATH.md](GUI_MINIMUM_PATH.md)（2026-04-14: balance-lines GUI 露出・ウィザード範囲明記）

- project: NLMYTGen
- git: **既定の開発ブランチは `master`**（2026-04-09: PR [#1](https://github.com/YuShimoji/NLMYTGen/pull/1) で `feat/phase2-motion-segmentation` をマージ済み。新規作業は `master` からブランチを切る）
- lane: **コア開発幹**（回帰・ドキュメント整合・承認済みバグ修正）。**主軸は本開発** — エージェント作業は未承認 FEATURE を増やさず上記に集中。オペレータ並行: Phase 1 Block-A (通過済、メンテ層の継続観測) / 主軸 (演出配置自動化の実戦投入) は runbook どおり。**レーン A（Phase 1）の repo 準備はオペレータ側でクローズ**（[OPERATOR_LANE_A_ENV.md](verification/OPERATOR_LANE_A_ENV.md)、[LANE_A_PREP_CHECKLIST.md](verification/LANE_A_PREP_CHECKLIST.md)）。**レーン D（H-01 brief）オペレータ完了・当面クローズ**（[H01-lane-d-prep-2026-04-09.md](verification/H01-lane-d-prep-2026-04-09.md) §6、2026-04-09）
- slice: **G-24 茶番劇 Group テンプレ生成 — user 作業待ち**。G-23 motion_target ルーティング実装完了 (コミット `1b45ff2`)。G-24 仕様・3 層分離・テスト 358 件全 pass。assistant 側のコード・ドキュメント・テスト作業は完了し、次は user の YMM4 作業待ち。
- next_action: **user 作業 3 件が先行**。assistant は結果報告を受けて再開する。
  - **(a)** `_tmp/b2_haitatsuin_motion_applied_v2.ymmp` を YMM4 で開き、Layer 10 の配達員 ImageItem に VideoEffects が視覚的に機能するか確認
  - **(b)** haitatsuin 配達員の **canonical skit_group template** を YMM4 上で 1 件作成 (Remark 固定・中央基準・相対配置)
  - **(c)** canonical から小演出テンプレートを 6-8 件派生 (surprise_jump / panic_shake / deny_shake / happy_sway 等)
  - **user 完了後の assistant 作業**: `skit_group_registry.template.json` を実テンプレートで埋める → 実案件で IR 要求を template 解決 → P02 に証跡追記。補助経路としての `motion_target: "layer:N"` は template だけでは吸収できない案件で使用。PNG 書き出しは G-22 hold の範囲で必要時のみ。
- parallel_replan_2026_04: **視覚最低限 + 改行／YMM4 ギャップ**の到達定義・チェックリスト・計測テンプレは [VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md)。`next_action` の主軸とは別軸の **並列オプション**。オペレータ時間の並列で、同文書の **トラック A（演出 IR 実戦 = 主軸の実務サブセット）** / **トラック B（改行ギャップ記録 = メンテ層 B-17 観測）** を配分する。`project-context.md` が IDE プレビューで空白になる場合は **生 Markdown で開く**（正本の針は本ファイルのまま）。エージェント依頼の **コピペ全文 Prompt・検収・親チャット返却テンプレ**は [CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md](verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md)（ファイル10）に集約。
- recommended_frontier_order: **G-24 茶番劇 Group template-first 運用** → 演出配置自動化の実戦投入 (P02) → 台本品質の継続観測 (メンテ) → 補助経路 (G-22 / PNG overlay) の必要最小限運用
  - **再開ショートカット（推奨対応）**: G-20 スライス1-2 完了（group_target バリデーション + `mode: relative`）は前提として維持。ただし主軸は `group_motion` の拡張ではなく、**canonical skit_group template → 派生 template 群 → production での template 解決**。
  - **並列の読み**: 上記フロンティア順と別に、[VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md) の **トラック A**（最小視覚 = 主軸の実務サブセット）と **トラック B**（B-17 済み L2 と YMM4 実表示のギャップ計測 = メンテ層観測）を **同時期に進めてよい**。先にオペレータ時間を取る軸は案件による（ユーザー合意で `next_action` 本文は変えず、配分のみ記録してよい）。
- 再現ルール: 異種サンプル 1 本で打ち切り済み。以後は新しい failure が出たときだけ追加検証
- operator/agent ガード: [REPO_LOCAL_RULES.md](REPO_LOCAL_RULES.md)（正本）+ `.claude/hooks/guardrails.py` で repo 外逸脱 / broad question 停止 / repeated visual proof を常設抑止（`.claude/CLAUDE.md` は入口ポインタ）
- 案件モード: CLI artifact

## 優先順位 (正本)

目的: 実制作の手間を減らすこと。未承認のコード機能は増やさない ([FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) 準拠)。順序を変える場合はユーザー合意で `next_action` と本節を更新する。

**判断基準**: 主軸は以下 4 条件をすべて満たす — ① 制作物の質に直接効く / ② 現在 bottleneck が顕在化 / ③ 着手しないと制作 workflow が詰まる / ④ 明確な完了の目安がある。据え置きは状態別に `hold` (再開条件あり) / `quarantined` (汚染バッチ由来) / `rejected` (廃止) に分ける。


| 層 | 内容 | 担い手 | 完了の目安 |
| --- | --- | --- | --- |
| **主軸 (唯一)** | **G-24 茶番劇 Group template-first 運用**: 配達員などの外部素材演者を `speaker_tachie` から分離し、**canonical template → 小演出テンプレ量産 → production で template 解決 + fallback + manual note** に寄せる。正本 [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md) / [P02-production-adoption-proof.md](verification/P02-production-adoption-proof.md) | user (YMM4 template 作成) + assistant (registry / 仕様 / fallback 整理) | canonical 1 件 + 派生 6〜8 件 + 1 本で exact/fallback/manual note を付けて運用証跡を残す |
| **メンテ (並行低負荷)** | ① **Packaging brief 運用** — [PACKAGING_ORCHESTRATOR_SPEC.md](PACKAGING_ORCHESTRATOR_SPEC.md)。委任 Prompt 正本 [H01](prompts/H01-packaging-brief-prompt.md)。② **サムネ one-sheet** — [THUMBNAIL_ONE_SHEET_WORKFLOW.md](THUMBNAIL_ONE_SHEET_WORKFLOW.md)。委任 Prompt 正本 [H02](prompts/H02-thumbnail-one-sheet-prompt.md)。③ **字幕 B-17 残差観測** — 委任 Prompt 正本 [B17](prompts/B17-reflow-residue-observation-prompt.md)、2 ケースは急がない。④ **台本品質の継続観測** — Block-A 通過済、新台本は [P01-phase1-operator-e2e-proof.md](verification/P01-phase1-operator-e2e-proof.md) に 1 行追記のみ。委任 Prompt 正本 [B18](prompts/B18-script-diagnostics-observation-prompt.md) | オペレータ (GUI) / 別セッション assistant | drift が出たら verification のみ更新。素材到着時は `docs/prompts/` 正本をそのまま別セッションに投げる |
| **hold (補助経路)** | **G-22 dual-rendering / PNG overlay**。背景キャラや一枚絵補助では有効だが、茶番劇演者の主軸ではない。必要時のみ使用 | user + assistant | skit_group template だけでは吸収できない案件で補助利用したとき |
| **hold (条件待ち)** | E-01 (YouTube 投稿自動化) / E-02 (YouTube メタデータ) — 制作パイプと混ぜない方針が解除されるまで触らない | — | 方針変更が明示されるまで |
| **quarantined** | F-01 / F-02 / D-02 — 汚染バッチ由来。個別再審査なしに backlog 化しない | — | 再審査・spec 化まで触らない |
| **rejected** | B-10 (emit-meta、撤去済) — 復活させない | — | 要望再浮上時は新 ID で再起票 |


**触らない原則**: spec/proof の採掘を増やさない。done 件数を進捗指標にしない。face を broad visual retry loop に戻さない。リモートは `origin/master` を正本とし、追加スライスは master からブランチを切る ([P2A-phase2-motion-segmentation-branch-review.md](verification/P2A-phase2-motion-segmentation-branch-review.md) は歴史的判断として参照)。

## 主成果物

- active_artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー
- artifact_surface: CLI → CSV → YMM4 台本読込 → 演出設定 → レンダリング → サムネイル → 投稿
- last_change_relation: 上記に加え **2026-04-10 統合コミット**（H-05 等）および **2026-04-11 T0 クローズ**（ドラフト §6・POST-APPROVAL T1 起票・チェックリスト §3.2・`next_action`→T1）。**続（同一日）**: P0 Amazon 並行証跡をリモート同期 — [B11-workflow-proof-amazon-panopticon-2026-04-10.md](verification/B11-workflow-proof-amazon-panopticon-2026-04-10.md)、レーン B/C/H01 追記、[P01](verification/P01-phase1-operator-e2e-proof.md)/[P03](verification/P03-thumbnail-one-sheet-proof.md)、`samples/` 診断・CSV・brief 同梱。**2026-04-11 追記**: レーン B（ファイル5）機械再検証を [LANE-B-execution-record-2026-04-09.md](verification/LANE-B-execution-record-2026-04-09.md) §8・HEAD `927588e` に固定（`validate-ir` / `apply-production --dry-run` PASS）。**2026-04-11 追記²**: ファイル4レーン E（S-8）`lane_e_file4_p01_amazon_2026-04-11_a` — [P03](verification/P03-thumbnail-one-sheet-proof.md) に成果物 SHA256 証跡・`score-thumbnail-s8` payload（[lane_e_file4_p01_amazon_2026-04-11_s8_payload.json](verification/lane_e_file4_p01_amazon_2026-04-11_s8_payload.json)）を追加。**2026-04-11 追記³（舵取りプラン）**: [P0-VERTICAL-STEERING-2026-04-11.md](verification/P0-VERTICAL-STEERING-2026-04-11.md) で本編 P0 縦を v14 に固定・Amazon を横に分離。`next_action` を P0 先頭へ。P01 行 `p0_mainline_v14_steering_2026-04-11_a` と `samples/p0_steering_v14_2026-04-11`_*。T1 `validate-ir` 再スモークを [CORE-DEV-POST-APPROVAL-SLICES.md](verification/CORE-DEV-POST-APPROVAL-SLICES.md) §4 に記録。**2026-04-11 追記⁴**: P0 舵取り・並行 runbook 周辺から **週 cadence・固定ウィンドウ・所要分**の正本記述を外し、**到達工程ベース**へ統一（[P0-VERTICAL-STEERING-2026-04-11.md](verification/P0-VERTICAL-STEERING-2026-04-11.md)、[OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md)、[LANE-C-operator-prep-2026-04-09.md](verification/LANE-C-operator-prep-2026-04-09.md)、[PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md)、[CORE-LANE-PARALLEL-PROMPT-PACK.md](verification/CORE-LANE-PARALLEL-PROMPT-PACK.md) §5）。**2026-04-11 追記⁵**: [VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md) — 視覚最低限・改行ギャップの並列再策定。`next_action` に **Block-A 狭義**（S-4 読込まで・黒背景/実字幕一致は除外）を明記、`parallel_replan_2026_04` および `recommended_frontier_order` 下の並列読みを追加（詳細は当該ファイル）。**2026-04-11 追記⁶**: [CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md](verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md) — コア＋並行の **コピペ全文 Prompt・検収・返却テンプレ**をファイル10として集約。[CORE-LANE-PARALLEL-PROMPT-PACK.md](verification/CORE-LANE-PARALLEL-PROMPT-PACK.md) にファイル10索引と §3 集約注記を追加。**2026-04-12 追記**: P0 Block-A と経路 A の対応を [P0-BLOCK-A-AND-PATH-A.md](verification/P0-BLOCK-A-AND-PATH-A.md) で正本化。優先表の P0 行を「C-09 必須」と読めない表現に修正。機械再スモーク `samples/p0_steering_v14_2026-04-12_*` → `samples/v14_t3_ymm4.csv`（365 rows）。**2026-04-12 追記²**: オペレータ申告に基づき [P01](verification/P01-phase1-operator-e2e-proof.md) `p0_mainline_v14_steering_2026-04-11_a` を **PASS（YMM4 S-4）** に更新（台本読込・字幕見え方確認）。`next_action` を Block-A 通過後の針へ更新。**2026-04-13 追記（並列プラン実施・立ち絵別レーン非干渉）**: 改行ギャップ第2コーパス `gapreflow_2026-04-13_b`（[VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md) §4.1.2、[P01](verification/P01-phase1-operator-e2e-proof.md) 表）。H-01 Custom GPT 運用固定メモ（[H01-packaging-orchestrator-workflow-proof.md](verification/H01-packaging-orchestrator-workflow-proof.md)）。トラック A 縮小（macro+`bg`+`bg_map` のみ dry-run、[P02](verification/P02-production-adoption-proof.md)、`samples/track_a_bg_only_*`、`samples/gapreflow_2026-04-13_*`）。G-19/G-20 の `src/` 変更なし。**2026-04-15 追記（メンテ並行委任 Prompt durable 化）**: ① H-01 brief / ② サムネ one-sheet / ③ B-17 改行残差観測 / ④ B-18 台本診断観測 の 4 委任 Prompt を [docs/prompts/](prompts/) 配下に正本分離。受入基準・CLI フラグ整合・P01/P03 追記形式を揃え、素材到着時に別セッションへ再説明不要で委譲できる状態。[CORE-PARALLEL-HUB §7](verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md) から索引。`src/` 変更なし。Spec 側の揺らぎ（user 呼称 `banned_pattern` ↔ Spec `banned_copy_patterns`、`nlm_smell_score` 等スコア呼称 ↔ 実装の診断コード方式）を Prompt 正本側で解消（Spec/実装側は未変更）。

## カウンター

- blocks_since_user_visible_change: 0
- blocks_since_manual_evidence: 0
- blocks_since_visual_audit: 0

## 量的指標

- test_file_count: 27
- test_count: 350
- mock_file_count: 0
- impl_file_count: 22
- mock_impl_ratio: 0.00
- open_todo_count: 0

## 最終検証

- last_verification: **本ブロックは docs/registry のみ更新のためテスト未実行**。直近のコード検証は 329 passed / 21 skipped（2026-04-16、`src/` 変更なしブロックの直前コード状態）

## Evidence（CLI artifact mode）

- evidence_status: Production E2E 実証済み (2026-04-05)。palette.ymmp → extract-template --labeled → face_map.json (11表情) → Part 1+2IR_row_range.json (28 utt, row-range) → production.ymmp (60 VI) → production_patched.ymmp (face 133 changes) → YMM4 visual proof OK。全編にわたって表情切替を確認。**茶番劇 E2E (2026-04-13)**: face 138 + idle_face 16 + slot 10 + motion 6 を IR → apply-production → YMM4 で実証。正本 [CHABANGEKI-E2E-PROOF-2026-04-13.md](verification/CHABANGEKI-E2E-PROOF-2026-04-13.md)
- last_e2e_data: AI監視(60 VoiceItem) の production.ymmp + chabangeki_e2e_ir.json (28 utt, row-range + idle_face + slot + motion) + face_map + slot_map_e2e + tachie_motion_map_e2e
- external_tool_verification: YMM4 visual proof OK (2026-04-13)。Phase 1 (face + idle_face) および Phase 2 (+ slot + motion) ともに PASS。実運用フィードバック: 表情はテンプレ指定のほうが実用的、speaker マッピングの左右逆転が発生
- final_artifact_reached: Yes (CSV → YMM4 台本読込 → IR → patch-ymmp → 表情差し替え済み ymmp)
- blocking_dependency: なし。face は `FACE_UNKNOWN_LABEL` / `PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE`_* / `FACE_MAP_MISS` / `IDLE_FACE_MAP_MISS` / `VOICE_NO_TACHIE_FACE` の failure class か、最終 creative judgement NG のときだけ再オープン

## FEATURE_REGISTRY 状態サマリ (2026-04-17 更新)

- done: 46件（台帳集計。G-23 を done へ是正済み）
- approved: 3件（H-01, G-20, **G-24**）— G-24 は茶番劇 Group template-first 運用の正本化、G-20 は geometry helper
- proposed: 0件（旧 G-21/G-22 は hold へ整理）
- info: 2件（C-01, C-06）
- hold: 9件（A-03, D-02, E-01, E-02, **G-01, G-03, G-04, G-21, G-22**）
- quarantined: 2件（F-01, F-02）
- rejected: 7件（B-10, C-02, C-03, C-04, C-05, D-01, F-03）

## Python のスコープ制約（2026-03-30 確定）

Python の責務はテキスト変換のみ（CSV + テキストメタデータ）。
以下は全て禁止（rejected として記録済み）:

- 画像生成・画像合成（PIL/Pillow 含む）
- .ymmp 生成・操作（音声ファイル参照を含むため外部生成不可能）
- YMM4 テンプレート生成・演出指定
- YMM4 出力の模倣・プレビュー
- 動画レンダリング・音声合成

## 外部メディア取得の方針（2026-03-30）

- 取得機能（acquisition）と受け取り機能（receiving）は分離する
- 最終的に自動化したい（ユーザー指示）
- A-04（RSS）は再審査済みで done。D-02（背景動画取得）は quarantined のまま、境界と価値経路の個別再審査が済むまで進めない

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
- G-24 approved。茶番劇演者の主経路を **GroupItem template-first** に切り替え、canonical template → 小演出量産 → production で template 解決 + fallback + manual note を正本化
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
- E-01/E-02: hold 継続
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
| 5   | IR→ymmp適用 (face/bg) | apply-production CLI | **自動**     | 軽い      | face 133 changes / bg section 切替まで実証済み                                                   |
| 6   | **YMM4上の演出配置**      | **手動**               | **未自動化**   | **最重量** | IRが指示する演出を実際にYMM4上で配置する作業。素材調達・配置・タイミング調整を含む。現状のpatch-ymmpはface/bg差し替えのみで、演出全体の自動配置には程遠い |
| 7   | **視覚効果制作**          | **手動**               | **未自動化**   | **重い**  | サムネイル未完成。茶番劇風アニメ/図解アニメがゼロ。画像表示のみの状態。C-08 prompt は仕様準拠 pass だが実用品質に課題あり                   |
| 8   | レンダリング              | YMM4                 | 手動トリガー     | 軽い      | C-06 (info) として記録済み                                                                      |
| 9   | YouTube投稿           | YouTube Studio       | 手動         | 中       | E-01/E-02 hold。**完全に別タスクとして切り出す**                                                        |


### 台本品質問題 (工程1の詳細)

NotebookLM で生成した台本には以下の構造的弱点があり、動画用に大きな手動調整が必要:

- **NLM臭**: NotebookLM特有の会話構造・語彙・展開パターンが残り、ゆっくり解説として不自然
- **話者混同**: 聞き手 (れいむ) と解説 (まりさ) のセリフ担当が混同することがある
- **様式不適合**: ゆっくり解説の様式 (ボケツッコミ、視聴者への問いかけ、テンポ等) への最適化が必要
- **YT視聴者向け調整**: YouTube視聴者の離脱を防ぐ構成・フック・情報密度の調整が必要
- **演出IRとの連鎖**: 台本品質が低いと、C-07 で生成する演出IRの質も下がる。台本の構造が曖昧だと、演出指示も曖昧になる

### 演出配置の未自動化問題 (工程6の詳細)

現状の patch-ymmp でできること:

- face (表情) の差し替え: 133 changes 実証済み
- bg (背景) のセクション切替: 2ラベルで実証済み
- slot (キャラ位置): X/Y/Zoom の deterministic patch
- overlay: deterministic な ImageItem 挿入
- se (効果音): label解決まで。AudioItem write route は未固定

現状の patch-ymmp でできないこと (= 手動で最も重い部分):

- **素材の調達と準備**: 背景画像、図解素材、茶番劇用のキャラポーズ等の入手・加工
- **素材の配置とレイアウト**: 画面上のどこに何をどのサイズで置くか
- **タイミング制御**: どの発話に合わせてどの素材を出し入れするか
- **アニメーション/モーション**: 拡大縮小・スライド・フェード等の演出効果の設定
- **茶番劇風演出**: ゆっくり解説で重要な視覚的演出パターンの実現
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

E-01/E-02 は動画制作ワークフローとは独立したタスクとして完全に切り出す。
制作パイプラインの自動化と投稿自動化は別の bottleneck であり、混ぜない。

## 既知の問題

- 直前 handoff は 53f3718 時点の内容で止まっており、後続 commit `8a1c710` で追加された canonical docs とその未充足状態は含んでいなかった
- E-02 は YouTube Studio への手入力をテキストファイル生成に置き換えるだけで、実質的な効率化にならない (E-01 とセットでないと価値が出ない)
- D-02 / F-01 / F-02 は前セッションの汚染バッチ由来で、個別精査前に normal backlog として扱えない
- A-04 は実装済み・再審査済みだが、runtime/context の一部に旧 `quarantined` 記述が残っていたため handoff trust を要再同期
- B-14 後の追加観測では、長すぎる行は大幅に減り、全字幕が 3 行以内に収まる水準まで改善した。残 pain は bulk overflow ではなく、境界ケースの改行品質に移っている
- B-11/B-12/B-13/B-14 により、辞書や timing ではなく字幕改行が支配的な pain だと確認。B-14 後は `ー`、カギ括弧、数値+記号などの individual judgement が主で、次は heuristic を積み増すより corpus-based な例収集へ寄せる方が自然
- 別機能の feasibility を棚卸しした結果、次の本命候補は S-6 LLM adapter。E-01/E-02 は secondary、D-02/F-01/F-02 は引き続き quarantine 境界
- `prompt-resume.md` は作成済みだが、内容の正本は引き続き repo docs 側である
- `group_motion` は `GROUP_MOTION_NO_GROUP_ITEM` / `GROUP_MOTION_TARGET_MISS` / `GROUP_MOTION_TARGET_AMBIGUOUS` を fatal 扱いに変更済み。運用側で `group_target` 命名規約（通常 `Remark`）のばらつきが残る場合は、次スライスで `validate-ir` lint を優先する。
- G-07 done。idle_face carry-forward により待機中表情を維持。TachieFaceItem 挿入で non-speaker キャラの表情を制御
- れいむの surprised が palette.ymmp に未定義でも、現在は `FACE_ACTIVE_GAP` / `FACE_LATENT_GAP` として事前に可視化される。これは data-side gap であり、face サブシステム自体の未完成を意味しない

## 一時補助物（作ったら登録。統合/削除したら除去）


| ファイル/モジュール                                     | 種別    | 削除条件                         | 寿命  |
| ---------------------------------------------- | ----- | ---------------------------- | --- |
| docs/verification/ymm4-template-measurement.md | 実測手順書 | 実測完了+結果反映済み (2026-04-03)。削除可 | 完了  |


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
