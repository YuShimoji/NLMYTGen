# Runtime State — NLMYTGen
# BLOCK SUMMARY のたびに更新する。
# compact 後の再アンカリングではこのファイルを読む。

## 現在位置
- project: NLMYTGen
- git: **既定の開発ブランチは `master`**（2026-04-09: PR [#1](https://github.com/YuShimoji/NLMYTGen/pull/1) で `feat/phase2-motion-segmentation` をマージ済み。新規作業は `master` からブランチを切る）
- lane: **コア開発幹**（回帰・ドキュメント整合・承認済みバグ修正）。**主軸は本開発** — エージェント作業は未承認 FEATURE を増やさず上記に集中。オペレータ並行: P0（Phase 1 本番）/ P2 等は runbook どおり。**レーン A（Phase 1）の repo 準備はオペレータ側でクローズ**（[OPERATOR_LANE_A_ENV.md](verification/OPERATOR_LANE_A_ENV.md)、[LANE_A_PREP_CHECKLIST.md](verification/LANE_A_PREP_CHECKLIST.md)）。**レーン D（H-01 brief）オペレータ完了・当面クローズ**（[H01-lane-d-prep-2026-04-09.md](verification/H01-lane-d-prep-2026-04-09.md) §6、2026-04-09）
- slice: G-15〜G-18 実装完了（Micro `bg` / 複数 `overlay` / timeline アダプタ / **SE `AudioItem` 挿入**）。Electron GUI: CSV 変換時に **診断 JSON 同梱保存**可（[gui-llm-setup-guide.md](gui-llm-setup-guide.md)）。正本 [G18-se-audioitem-implementation.md](verification/G18-se-audioitem-implementation.md)。従来: 視覚三スタイル [VISUAL_STYLE_PRESETS.md](VISUAL_STYLE_PRESETS.md)、P2A [P2A-motion-branch-operator-decision.md](verification/P2A-motion-branch-operator-decision.md)、P2C [P2C-se-audioitem-boundary.md](verification/P2C-se-audioitem-boundary.md)（履歴）
- next_action: **本開発幹に復帰**（回帰 `NLMYTGEN_PYTEST_FULL=1 uv run pytest`、承認済みバグ修正のみ、未承認 FEATURE は増やさない）。**実行フェーズ（2026-04-10 更新）**: P0 の次サイクル実行（CLI）は [P01-phase1-operator-e2e-proof.md](verification/P01-phase1-operator-e2e-proof.md) の `p0_nextcycle_amazon_2026-04-10_a` を参照。B-11 は [B11-workflow-proof-ai-monitoring-labor.md](verification/B11-workflow-proof-ai-monitoring-labor.md) で体裁充足（Gate B・§3）。**P2 判定**: 最新入力は `YMM4見え方=NG（未実施: 端末でYMM4リソース非共有）` / `S6§2(5条件)=充足（条件4/5は docs/verification/P2-CONDITION45-PRECHECK-TEMPLATE.md を根拠に確認済み）` のため **OPEN 継続**。**OPEN理由は YMM4実測待ちの1点のみ**。入力・判定ログは [P2-READY-INPUT-TEMPLATE.md](verification/P2-READY-INPUT-TEMPLATE.md) §6 と [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](verification/CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) を正本とする。昇格条件は `OK + 5条件充足` のみ。**並行レーン・コア幹**: [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md)。**A〜E 移譲後のコア開発手順（受け入れ・ドラフト・承認後スライス・master PR）**: [CORE-DEV-POST-DELEGATION-INDEX.md](verification/CORE-DEV-POST-DELEGATION-INDEX.md)。**レーン B（GUI LLM 正本同期）の repo 準備はクローズ**（[LANE-B-gui-llm-sync-checklist.md](verification/LANE-B-gui-llm-sync-checklist.md)、[gui-llm-setup-guide.md](gui-llm-setup-guide.md)。Instructions 実貼り付けはオペレータが並行実施可）。**P2**（背景アニメ短サイクル）— map 警告（`BG_ANIM_MAP_MISS` / `TRANSITION_MAP_MISS`）は最小 map で解消済み、`test_verify_4_bg.ymmp` で 4 セクション拡張（`BG anim writes: 7`）まで機械確認済み。**レーン C（視覚三スタイル）準備はクローズ**（[LANE-C-operator-prep-2026-04-09.md](verification/LANE-C-operator-prep-2026-04-09.md)）。**レーン E（サムネ S-8）repo 準備はクローズ**（[LANE-E-S8-prep-2026-04-09.md](verification/LANE-E-S8-prep-2026-04-09.md) 運用クローズ節。公開直前の実 1 枚は P3・runbook トラック E で並行可）。**C と P2 は YMM4 時間分割**（同時フル非推奨）。P3・Parking は下表。新規案件の B-11 は [B11-pre-plan-execution-pack-2026-04-07.md](verification/B11-pre-plan-execution-pack-2026-04-07.md) から切る。
- approval_slice_status: **File6 指示を承認として記録済み**（[CORE-DEV-POST-APPROVAL-SLICES.md](verification/CORE-DEV-POST-APPROVAL-SLICES.md) §1 に追記）。実装準備ブランチ: `topic/file6-post-approval-prep-2026-04-10`（`master` 起点）。P2 条件4ログは 2026-04-10 に再取得済み（[P2-CONDITION45-PRECHECK-TEMPLATE.md](verification/P2-CONDITION45-PRECHECK-TEMPLATE.md)）。
- recommended_frontier_order: 台本品質改善 → 演出配置自動化拡張 → 視覚効果実現（既定。変更可）
- 再現ルール: 異種サンプル 1 本で打ち切り済み。以後は新しい failure が出たときだけ追加検証
- operator/agent ガード: [REPO_LOCAL_RULES.md](REPO_LOCAL_RULES.md)（正本）+ `.claude/hooks/guardrails.py` で repo 外逸脱 / broad question 停止 / repeated visual proof を常設抑止（`.claude/CLAUDE.md` は入口ポインタ）
- 案件モード: CLI artifact

## 次以降の推奨プラン (2026-04-09 採用・正本)

目的: **実制作の手間を減らすこと**を最優先し、未承認のコード機能は増やさない（[FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) 準拠）。順序を変える場合はユーザー合意で `next_action` と本節を更新する。

**採用根拠（2026-04-09）**: [B11-workflow-proof-ai-monitoring-labor.md](verification/B11-workflow-proof-ai-monitoring-labor.md) は Gate B（運用摩擦支配）— 4 区分の顕著手戻りはなく、主戦場を L2 改行コーパスに寄せず **P0 実行と演出・運用側の小さな検証**へ振る判断。並行レーン A〜E とコア開発 1 幹は [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) に従う。下表の P0〜Parking の優先構造は 2026-04-08 版を論理的正本として維持し、本日付で運用採用を固定した。

| 優先 | コード | 内容 | 完了の目安 |
|------|--------|------|------------|
| **P0** | — | **Phase 1 本番 1 本**: 新台本で `diagnose-script`（CLI または **GUI CSV タブの診断 JSON 同梱**）→ [S1-script-refinement-prompt.md](S1-script-refinement-prompt.md)（C-09）→ `build-csv` → YMM4 読込〜。接続判定・残修正区分・効果を [P01-phase1-operator-e2e-proof.md](verification/P01-phase1-operator-e2e-proof.md) に 1 行以上追記。プラン直前の B-11 実測は [B11-workflow-proof-ai-monitoring-labor.md](verification/B11-workflow-proof-ai-monitoring-labor.md) で充足済み；別台本では [B11-pre-plan-execution-pack-2026-04-07.md](verification/B11-pre-plan-execution-pack-2026-04-07.md) に沿って新規記録を切る。S-5 は監視継続しつつ P2 背景演出試行は `next_action` に従う | **最優先・今期の主目標** |
| **P1** | H-01 `approved` | **Packaging brief 運用**: [PACKAGING_ORCHESTRATOR_SPEC.md](PACKAGING_ORCHESTRATOR_SPEC.md) に沿った brief を Custom GPT に常設し、1 本で title / thumbnail / script の drift が減るか観測（コード変更なしで可） | P0 と並行可・低負荷 |
| **P2** | done 機能の実戦投入 | **演出パイプの実使用**: 本編で `overlay` / `se`（`--se-map`）/ `apply-production` が効くなら registry を整えて実戦投入。**B-11 §3 次投資先**（背景アニメ 1〜2 セクション・route / 見え方優先）と整合。non-fade / template-backed `transition` は **新 ymmp sample が入ったときだけ** `measure-timeline-routes` で再測定 | 制作物が生まれたタイミング |
| **P3** | — | **視覚・公開周辺**: [THUMBNAIL_ONE_SHEET_WORKFLOW.md](THUMBNAIL_ONE_SHEET_WORKFLOW.md) でサムネ 1 本を通す。準備チェックリスト [verification/LANE-E-S8-prep-2026-04-09.md](verification/LANE-E-S8-prep-2026-04-09.md)。茶番・図解アニメはツール選定後 | P0 の後でも可 |
| **Parking** | — | **履歴**: 旧 `feat/phase2-motion-segmentation` の内容は **master にマージ済み**（2026-04-09、PR #1）。今後の追加スライスは **master 上で** [P2A-motion-branch-operator-decision.md](verification/P2A-motion-branch-operator-decision.md) の精神（一括ではなく台帳承認付きパケット）に従う | 急がない |
| **明示的に後回し** | — | 字幕 B-17 残差（急がない）、quarantined（F-01/F-02 等）の棚卸し spec 化、E-01/E-02 と制作パイプの混線、未承認 FEATURE の新規実装 | 別判断まで触らない |

**すぐやらないこと（再掲）**: spec/proof のための採掘だけを増やさない。done 件数を進捗指標にしない。face を broad visual retry loop に戻さない。

## 開発プラン (2026-04-06)

目的: spec/proof の積み増しではなく、**実制作の手間を直接減らす**。以下は**既定の優先順**（変更する場合は FEATURE_REGISTRY / ユーザー合意で明示）。

| Phase | フォーカス | 中身（実行単位） | 根拠 |
|-------|-------------|------------------|------|
| **1** | 台本品質（候補A） | **実装済み**: `diagnose-script`（B-18）→ [S1-script-refinement-prompt.md](S1-script-refinement-prompt.md)（C-09）→ `build-csv`。GUI では CSV 成功時に `{stem}_script-diagnostics.json` を同梱保存可（[gui-llm-setup-guide.md](gui-llm-setup-guide.md)）。**P0**: 1 本 end-to-end で運用試行と [P01](verification/P01-phase1-operator-e2e-proof.md) 追記 | 上流が良くなると IR・配置判断も安定 |
| **2** | 演出配置拡張（候補B） | (b) **G-14**: production.ymmp は ImageItem 無し→`production_ai_monitoring_lane` で contract pass（bg_anim 未観測は仕様）。(a) SE は **G-18** で `AudioItem` 挿入済み（`--se-map`）。(c) motion / timeline 拡張は **master** 上で [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md) を正とし、追加は台帳承認後の小分けスライス | 同上 |
| **3** | 視覚効果（候補C） | **チェックリスト追加済み** [THUMBNAIL_ONE_SHEET_WORKFLOW.md](THUMBNAIL_ONE_SHEET_WORKFLOW.md)。茶番・図解アニメはツール選定後 | 同上 |

**メンテナンス（並行で低負荷）**

- H-01: `PACKAGING_ORCHESTRATOR_SPEC` に沿った brief を Custom GPT 運用に固定し、drift が出たら verification のみ更新
- 字幕 B-17: 残差 2 ケースは**急がない**（コーパス追加または YMM4 幅キャリブレーションは別判断）
- リモート: **正本は `origin/master`**（phase2 レーンは 2026-04-09 PR #1 で統合済み）。追加変更は master からブランチを切る。[P2A](verification/P2A-phase2-motion-segmentation-branch-review.md) は歴史的判断として参照

**スコープ外（据え置き）**

- E-01/E-02: 制作パイプラインと混ぜない
- F-01/F-02: quarantined のまま
- D-02/F 系: 個別再審査なしに backlog 化しない

## 主成果物
- active_artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー
- artifact_surface: CLI → CSV → YMM4 台本読込 → 演出設定 → レンダリング → サムネイル → 投稿
- last_change_relation: FEATURE_REGISTRY G-15〜G-18 done、GUI CSV+診断 JSON 同梱、**次以降推奨プラン (2026-04-09 採用)**・`next_action` を実行フェーズへ更新（B-11 充足・Gate B 反映）、以前 (2026-04-08) 表構造を維持、`patch-ymmp --timeline-profile`、SE `AudioItem`（`_apply_se_items`）、プラン直前レーン整理 [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md)、runbook トラック D/E 見出し整合、**レーン C 準備クローズ**（[LANE-C-operator-prep-2026-04-09.md](verification/LANE-C-operator-prep-2026-04-09.md)）、**レーン E（S-8）repo 準備クローズ・運用クローズ**（[LANE-E-S8-prep-2026-04-09.md](verification/LANE-E-S8-prep-2026-04-09.md)）、**レーン D（H-01）オペレータ完了**（[H01-lane-d-prep-2026-04-09.md](verification/H01-lane-d-prep-2026-04-09.md)）、`runtime-state` を本開発主軸へ再アンカー、**コア移譲後手順一式** [CORE-DEV-POST-DELEGATION-INDEX.md](verification/CORE-DEV-POST-DELEGATION-INDEX.md)、**プラン設計前オペレータ準備一式**（レーン A〜E チェックリスト・H-01・packaging brief テンプレ・PRE-PLAN §2.4 索引、2026-04-09 コミット）、**`feat/phase2-motion-segmentation` → `master` マージ完了**（PR [#1](https://github.com/YuShimoji/NLMYTGen/pull/1)、2026-04-09。開発ベースは `master`）、**並行開発直前の本開発プランを実施**（2026-04-10: フル回帰・受け入れゲート点検・runbook を master 起点へ整合）

## カウンター
- blocks_since_user_visible_change: 0
- blocks_since_manual_evidence: 0
- blocks_since_visual_audit: 0

## 量的指標
- test_file_count: 16
- test_count: 301
- mock_file_count: 0
- impl_file_count: 22
- mock_impl_ratio: 0.00
- open_todo_count: 0

## 最終検証
- last_verification_artifact: `NLMYTGEN_PYTEST_FULL=1 uv run pytest` 全件（subprocess CLI 統合含む）を再実行し `301 passed`（2026-04-10）。既定の `uv run pytest` はユニット中心（`tests/conftest.py`）
- last_verification_date: 2026-04-10

## Evidence（CLI artifact mode）
- evidence_status: Production E2E 実証済み (2026-04-05)。palette.ymmp → extract-template --labeled → face_map.json (11表情) → Part 1+2IR_row_range.json (28 utt, row-range) → production.ymmp (60 VI) → production_patched.ymmp (face 133 changes) → YMM4 visual proof OK。全編にわたって表情切替を確認
- last_e2e_data: AI監視(60 VoiceItem) の production.ymmp + Custom GPT v4 IR (28 utterances, row-range annotated) + character-scoped face_map (魔理沙6+霊夢5)
- external_tool_verification: YMM4 visual proof OK (2026-04-05)。表情が全編にわたって切り替わることを確認。待機中表情は G-07 (idle_face carry-forward) で対応済み
- final_artifact_reached: Yes (CSV → YMM4 台本読込 → IR → patch-ymmp → 表情差し替え済み ymmp)
- blocking_dependency: なし。face は `FACE_UNKNOWN_LABEL` / `PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE_*` / `FACE_MAP_MISS` / `IDLE_FACE_MAP_MISS` / `VOICE_NO_TACHIE_FACE` の failure class か、最終 creative judgement NG のときだけ再オープン

## FEATURE_REGISTRY 状態サマリ (2026-04-08 更新)

- done: 42件（上記 + G-15, G-16, G-17, G-18）
- approved: 1件（H-01）
- proposed: 0件（G-15〜G-17 は done へ）
- info: 2件（C-01, C-06）
- hold: 4件（A-03, D-02, E-01, E-02）
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
- timeline packet: G-11 slot patch hardening 完了 → G-12 timeline route measurement packet 完了 → G-13 overlay / se insertion packet 完了。timeline 編集は broad retry loop に戻さず、packet ごとに failure class / readback / boundary を定義して扱う
- H-01 dry proof 済み。`docs/verification/H01-packaging-orchestrator-ai-monitoring-dry-proof.md` により、brief が title / thumbnail / script の共有契約として機能することを repo-local artifact ベースで確認した。strict な before/after GUI rerun proof はまだ残る
- H-02 done (2026-04-06)。dry proof + strict GUI rerun proof pass。4/5案が preferred_specifics を使用、banned pattern なし、Specificity Ledger・Brief Compliance Check 出力確認済み。コピー品質の実用改善は別課題
- H-03 done。`score-visual-density` CLI + GUI 品質診断。dry proof は `docs/verification/H03-visual-density-ai-monitoring-proof.md`
- H-04 done。`score-evidence` CLI + GUI 品質診断。manual proof は `docs/verification/H04-evidence-richness-ai-monitoring-proof.md`
- B-18 done。`diagnose-script` + `docs/SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md`。dry proof `docs/verification/B18-script-diagnostics-ai-monitoring-sample.md`
- C-09 done。`docs/S1-script-refinement-prompt.md` + gui-llm-setup-guide 導線
- H-02 closed。packaging: H-02/H-03/H-04 は実装済み。H-01 は approved（schema + dry proof、運用で brief 固定）。timeline は新 sample または known failure class が出たときだけ再オープンする
- G-01/G-03: hold (タイムライン操作 API 非公開)
- G-05 v4 prompt doc が canonical。remote Custom GPT Instructions 側の drift は `PROMPT_FACE_DRIFT` / `FACE_PROMPT_PALETTE_*` で検出する
- D-02: hold (C-07 v3 に吸収完了)
- E-01/E-02: hold 継続
- F-01/F-02: quarantined 継続

## 実制作ワークフロー自動化カバレッジ (2026-04-06 棚卸し)

FEATURE_REGISTRY 上 done 42 件だが、実際の動画制作ワークフロー全体に対するカバレッジは限定的。
ユーザーフィードバックに基づき、各工程の自動化状態と実際の重さを正確に記録する。

### 工程別カバレッジ

| # | 工程 | 担当 | 自動化状態 | 実際の重さ | 備考 |
|---|------|------|-----------|-----------|------|
| 1 | 台本作成 | NotebookLM | 外部ツール (手動) | **重い** | NLM出力はそのまま使えない。下記「台本品質問題」参照 |
| 2 | 台本→CSV変換 | build-csv CLI | **自動** | 軽い | B-01〜B-17 で字幕分割品質も改善済み |
| 3 | CSV→YMM4読込 | YMM4 台本読込 | 手動操作 (1回) | 軽い | C-01 (info) として記録済み |
| 4 | 演出IR生成 | Custom GPT (C-07) | 半手動 (コピペ) | 中 | GPTへの入力と出力の受け渡しが手動 |
| 5 | IR→ymmp適用 (face/bg) | apply-production CLI | **自動** | 軽い | face 133 changes / bg section 切替まで実証済み |
| 6 | **YMM4上の演出配置** | **手動** | **未自動化** | **最重量** | IRが指示する演出を実際にYMM4上で配置する作業。素材調達・配置・タイミング調整を含む。現状のpatch-ymmpはface/bg差し替えのみで、演出全体の自動配置には程遠い |
| 7 | **視覚効果制作** | **手動** | **未自動化** | **重い** | サムネイル未完成。茶番劇風アニメ/図解アニメがゼロ。画像表示のみの状態。C-08 prompt は仕様準拠 pass だが実用品質に課題あり |
| 8 | レンダリング | YMM4 | 手動トリガー | 軽い | C-06 (info) として記録済み |
| 9 | YouTube投稿 | YouTube Studio | 手動 | 中 | E-01/E-02 hold。**完全に別タスクとして切り出す** |

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
- G-07 done。idle_face carry-forward により待機中表情を維持。TachieFaceItem 挿入で non-speaker キャラの表情を制御
- れいむの surprised が palette.ymmp に未定義でも、現在は `FACE_ACTIVE_GAP` / `FACE_LATENT_GAP` として事前に可視化される。これは data-side gap であり、face サブシステム自体の未完成を意味しない

## 一時補助物（作ったら登録。統合/削除したら除去）
| ファイル/モジュール | 種別 | 削除条件 | 寿命 |
|---|---|---|---|
| docs/verification/ymm4-template-measurement.md | 実測手順書 | 実測完了+結果反映済み (2026-04-03)。削除可 | 完了 |
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

