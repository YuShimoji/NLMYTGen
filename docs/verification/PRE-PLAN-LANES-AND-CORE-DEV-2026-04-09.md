# プラン作成直前 — 並行レーン数とコア開発の切り分け

> **目的**: 次期プランを書く直前まで、**誰が何レーンを並行できるか**と、**リポジトリ側（コア開発）で進める唯一の幹**を固定する。正本の runbook は [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md)。B-11 完了条件は [B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md)。

> **2026-04-27 現行アンカー**: レガシードキュメント整理後の次期ロードマップ入力は、**G-24（茶番劇 Group template-first）の production-use validation**。v1 planned set 5 件は user-owned export/sample proof + assistant inspection により `direct_proven` 昇格済み。旧「背景アニメ/S6」軸は既存証跡として保持するだけに留める。プラン本文を書く前に、追加 motion authoring と **既存テンプレートの実制作解決検証**を混同しないこと。

---

## 1. 切り出せるレーン数（答え）


| 数え方                         | 本数      | 意味                                                                                               |
| --------------------------- | ------- | ------------------------------------------------------------------------------------------------ |
| **名称トラック（A〜G）**             | **7**   | [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) §0 の表どおり。              |
| **同時に「別成果物」を進められるオペレーション軸** | **5**   | **A〜E**（下表）。**F** は全レーンに随伴するメタ作業。**G** は意図的な保留・バッファ。                                             |
| **YMM4 重い作業の同時上限（現実的）**     | **1〜2** | **C**（視覚三スタイル・レジストリ）と **主軸 G-24（skit_group template author/export）** は **同じ YMM4 ウィンドウ**を奪い合う。人が 1 人なら事実上 **どちらか一方**、または時間分割。 |


### 1.1 オペレータ並行軸（A〜E）の依存関係


| レーン   | 内容                                         | 他レーンとの関係                                          |
| ----- | ------------------------------------------ | ------------------------------------------------- |
| **A** | Phase 1（B-18 → C-09 → build-csv → YMM4 読込） | **B と独立**。B-11 実測の「取込前」CLI は A と同系。               |
| **B** | GUI LLM 正本同期（C-09 / C-07 v4 / H-01 / C-08） | **A と独立**（Instructions メンテは台本 1 本を待たない）。          |
| **C** | 視覚三スタイル（YMM4・overlay_map 等）                | **主軸 G-24（skit_group template author/export）と資源競合**（YMM4）。**A の CSV 読込後**の工程とも時間が重なりやすい。 |
| **D** | H-01 Packaging brief                       | **B-4 と同一運用**。トラックとしては **B と併走**可能（別ファイル作業）。      |
| **E** | サムネ 1 枚（S-8）                               | **公開直前**に寄せるとよい。**A〜D と独立**に近いが、素材の準備タイミングは案件次第。  |


### 1.2 主軸 G-24（skit_group template-first）をレーンとして数える場合

- [runtime-state.md](../runtime-state.md) の `next_action` どおり、現行主軸は **v1 template set の production-use validation**。
- runbook 表には無い **第 6 の並行候補**として扱う。**C と同時刻フル稼働は難しい**ため、並行レーン「数」は **5（A〜E）+ 主軸 (条件付き 1)** と読んでもよいが、**同時並列のオペレーションは最大 5＋主軸を時間的に分割**するのが現実的（週 cadence や固定ウィンドウは repo 正本に置かない）。
- `delivery_nod_v1` / `delivery_deny_oneshot_v1` / `delivery_exit_left_v1` は user-owned template/sample proof + acceptance により閉じた。残る差分は、既存テンプレートで exact / fallback / manual_note が実制作の手作業を減らすかどうか。

### 1.3 コア開発（リポジトリ側）は **1 本の幹**に集約


| 方針             | 内容                                                                                                                                                                                                                                                                     |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **幹は 1 つ**     | **未承認 FEATURE を増やさない**（[FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) 準拠）。プランに載せる「開発項目」は、次ゲートで **台帳更新＋ユーザー承認**してから実装に落とす。                                                                                                                                               |
| **いまコアで進めること** | **① 回帰と境界の維持**（`src/` または `tests/` に触れた場合のみ `uv run pytest`、必要なら `NLMYTGEN_PYTEST_FULL=1` を opt-in で発火）。**② G-24 の作業接続性**（本ファイル・[runtime-state.md](../runtime-state.md)・[P02-production-adoption-proof.md](P02-production-adoption-proof.md) が v1 template completion と production-use validation 出口で一致しているか）。**③ 既存 done 機能のバグ修正のみ**（新 ID 不要の範囲）。 |
| **コアで進めないこと**  | H-01 の自動パイプライン連携、F-01/F-02 の復活、E-01/E-02、新しい ymmp 生成系、承認なき G 系拡張。                                                                                                                                                                                                      |


---

## 2. プラン作成「直前」チェックリスト（ここまで揃えたらプランに入る）

### 2.1 B-11（必須・実測）

[§5 完了チェック](B11-pre-plan-execution-pack-2026-04-07.md#5-完了チェックプラン策定に入って良い条件) をすべて満たす。

- `docs/verification/B11-workflow-proof-*.md` が 1 本そろう（既存 AI 監視継続でも新案件でも可）。
- 取込前・取込後が **同一ファイル**で埋まっている。
- 4 区分（辞書 / 手動改行 / 再分割 / タイミング）が **空欄なし**。
- 代表例 **3 件以上**。
- §3 に **Gate A/B/C** と **次投資先**が書かれている。

**現状メモ**: [B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md) は **§5 体裁を充足**（2026-04-09。取込前は CLI 再実行で再現済み。取込後はファイル先頭の検証範囲注記どおり、YMM4 実機記録としてオペレータが最終確認する）。レーン A 用の環境メモは [OPERATOR_LANE_A_ENV.md](OPERATOR_LANE_A_ENV.md)、チェックリストは [LANE_A_PREP_CHECKLIST.md](LANE_A_PREP_CHECKLIST.md)。

### 2.2 P01 記録（Phase 1 Block-A と整合）

- [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) に、対象案件の **接続判定**が 1 行以上ある（既存表が十分なら追加行不要）。

### 2.3 主軸 G-24（次期プランのオプション入力）

- [runtime-state.md](../runtime-state.md) の `next_action` と [P02-production-adoption-proof.md](P02-production-adoption-proof.md) の G-24 v1 completion / production-use validation 記録を確認する。
- `delivery_nod_v1` / `delivery_deny_oneshot_v1` / `delivery_exit_left_v1` は `direct_proven` 昇格済み。`samples/haitatsuin_2026-04-12_g24_proof.ymmp` は現在 compact template/sample proof であり、voice-anchored adoption corpus ではない。
- 次に YMM4 で確認するのは「さらに motion を作ること」ではなく、assistant が既存テンプレート + registry から出す production-like sample / 解決結果が実用上の手作業を減らすか。
- `fallback` / `manual_note` / missing-template が出た場合は、その分類を記録してから追加テンプレート起票の是非を判断する。

#### 2.3.1 次期 formal plan の入口分岐

- **通常**: 既存 v1 template set で production-like sample / 解決結果を作り、exact / fallback / manual_note を記録する。
- **十分**: exact coverage が制作負荷を減らすなら production-use hardening へ進む。
- **不足**: 失敗理由を `fallback` / `manual_note` / missing-template / body-face drift / `TachieItem` 混入 / repo bug に分類し、追加テンプレート起票または修正プランを書く。不足を即「新しい動き量産」の開始条件にしない。

### 2.4 並行運用の前提確認（任意だが推奨）

- [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) の **A + B** が別担当でも衝突しないことを確認（Instructions 正本は repo）。
- **レーン別 repo 準備チェックリスト**（2026-04-09 同梱）:
  - **A**: [LANE_A_PREP_CHECKLIST.md](LANE_A_PREP_CHECKLIST.md)、[OPERATOR_LANE_A_ENV.md](OPERATOR_LANE_A_ENV.md)
  - **B**: [LANE-B-gui-llm-sync-checklist.md](LANE-B-gui-llm-sync-checklist.md)、[gui-llm-setup-guide.md](../gui-llm-setup-guide.md)
  - **C**: [LANE-C-operator-prep-2026-04-09.md](LANE-C-operator-prep-2026-04-09.md)、[lane-c-overlay-map.TEMPLATE.json](lane-c-overlay-map.TEMPLATE.json)（絶対パスは `_local/` に置き [.gitignore](../../.gitignore) 参照）
  - **D**: [H01-lane-d-prep-2026-04-09.md](H01-lane-d-prep-2026-04-09.md)、[samples/packaging_brief.template.md](../../samples/packaging_brief.template.md)、[packaging_brief_EMPTY_TEMPLATE_emitted.md](packaging_brief_EMPTY_TEMPLATE_emitted.md)

### 2.5 レーン E（サムネ S-8）準備（任意だが推奨）

- [LANE-E-S8-prep-2026-04-09.md](LANE-E-S8-prep-2026-04-09.md) で **S-0**（YMM4 テンプレ・書き出し解像度）・**B-5**（C-08 正本同期）・**案件入力セット**をそろえてから、runbook トラック E を実行する。

---

## 3. 次アクション（役割別）


| 役割          | 次にやること                                                           |
| ----------- | ---------------------------------------------------------------- |
| **オペレータ**   | B-11 §2 全編・§3 Gate。並行なら **B**（正本同期）・**D**（brief）・**E**（サムネ）を別枠で。 |
| **演出/YMM4** | **C** または **主軸 G-24 production-use validation** を時間帯で分ける（同時フルは非推奨）。planned authoring は完了済みで、以後は assistant 生成の sample / 解決結果を確認する。 |
| **コア開発**    | 回帰テスト・ドキュメント整合・承認済みバグ修正のみ。プラン文書化は **上記チェックリスト完了後**。              |


---

## 4. 削除済み旧コア計画の扱い

旧コア計画・旧レーン Prompt・旧並行 Prompt ハブ・旧視覚品質パケットは削除済み。次期プランは本ファイルの G-24 gate と [runtime-state.md](../runtime-state.md) / [P02-production-adoption-proof.md](P02-production-adoption-proof.md) から再構成し、ファイル番号式 Prompt や旧背景アニメ/S6 の T0〜T3 計画へ戻らない。

---

## 5. 変更履歴

- 2026-04-27: レガシードキュメント整理後の現行アンカーとして G-24 `delivery_nod_v1` cautious gate を追記。その後 user-owned PASS により現行アンカーを `delivery_deny_oneshot_v1` へ更新。さらに `delivery_deny_oneshot_v1` / `delivery_exit_left_v1` 完了報告と repo inspection を受け、現行アンカーを production-use validation へ更新。旧背景アニメ/S6 は既存証跡として扱うよう §1.2 / §2.3 / §3 を更新。
- 2026-04-27: 旧コア計画・Prompt ハブ削除に合わせ、参照先を `runtime-state.md` / `P02-production-adoption-proof.md` へ集約。§4 を旧ドキュメント参照から削除済み扱いへ変更。
- 2026-04-09: §2.4 にレーン A〜D の repo 準備チェックリストへのリンクを追加（プラン設計前のオペレータ準備を索引化）。
- 2026-04-09: §4 追加（コア開発索引へのリンク）。
- 2026-04-09: §2.5 レーン E（S-8）準備チェックリスト [LANE-E-S8-prep-2026-04-09.md](LANE-E-S8-prep-2026-04-09.md) へのリンクを追加。
- 2026-04-09: 初版。runbook のトラック D/E 見出しを表と整合（D=H-01、E=サムネ）。
- 2026-04-09: §2.1 現状メモを更新（B-11 §5 完了・レーン A 準備ドキュメントへのリンク）。
