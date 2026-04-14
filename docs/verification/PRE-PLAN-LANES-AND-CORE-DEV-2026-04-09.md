# プラン作成直前 — 並行レーン数とコア開発の切り分け

> **目的**: 次期プランを書く直前まで、**誰が何レーンを並行できるか**と、**リポジトリ側（コア開発）で進める唯一の幹**を固定する。正本の runbook は [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md)。B-11 完了条件は [B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md)。

---

## 1. 切り出せるレーン数（答え）


| 数え方                         | 本数      | 意味                                                                                               |
| --------------------------- | ------- | ------------------------------------------------------------------------------------------------ |
| **名称トラック（A〜G）**             | **7**   | [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) §0 の表どおり。              |
| **同時に「別成果物」を進められるオペレーション軸** | **5**   | **A〜E**（下表）。**F** は全レーンに随伴するメタ作業。**G** は意図的な保留・バッファ。                                             |
| **YMM4 重い作業の同時上限（現実的）**     | **1〜2** | **C**（視覚三スタイル・レジストリ）と **主軸 (背景アニメ)** は **同じ YMM4 ウィンドウ**を奪い合う。人が 1 人なら事実上 **どちらか一方**、または時間分割。 |


### 1.1 オペレータ並行軸（A〜E）の依存関係


| レーン   | 内容                                         | 他レーンとの関係                                          |
| ----- | ------------------------------------------ | ------------------------------------------------- |
| **A** | Phase 1（B-18 → C-09 → build-csv → YMM4 読込） | **B と独立**。B-11 実測の「取込前」CLI は A と同系。               |
| **B** | GUI LLM 正本同期（C-09 / C-07 v4 / H-01 / C-08） | **A と独立**（Instructions メンテは台本 1 本を待たない）。          |
| **C** | 視覚三スタイル（YMM4・overlay_map 等）                | **主軸 (背景アニメ) と資源競合**（YMM4）。**A の CSV 読込後**の工程とも時間が重なりやすい。 |
| **D** | H-01 Packaging brief                       | **B-4 と同一運用**。トラックとしては **B と併走**可能（別ファイル作業）。      |
| **E** | サムネ 1 枚（S-8）                               | **公開直前**に寄せるとよい。**A〜D と独立**に近いが、素材の準備タイミングは案件次第。  |


### 1.2 主軸 (背景アニメ・演出パイプ短サイクル) をレーンとして数える場合

- [runtime-state.md](../runtime-state.md) の `next_action` どおり、**機械確認済み**（例: `test_verify_4_bg.ymmp`）→ **YMM4 見え方** → **実案件 IR 段階展開**。
- runbook 表には無い **第 6 の並行候補**として扱う。**C と同時刻フル稼働は難しい**ため、並行レーン「数」は **5（A〜E）+ 主軸 (条件付き 1)** と読んでもよいが、**同時並列のオペレーションは最大 5＋主軸を時間的に分割**するのが現実的（週 cadence や固定ウィンドウは repo 正本に置かない）。

### 1.3 コア開発（リポジトリ側）は **1 本の幹**に集約


| 方針             | 内容                                                                                                                                                                                                                                                                     |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **幹は 1 つ**     | **未承認 FEATURE を増やさない**（[FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) 準拠）。プランに載せる「開発項目」は、次ゲートで **台帳更新＋ユーザー承認**してから実装に落とす。                                                                                                                                               |
| **いまコアで進めること** | **① 回帰と境界の維持**（`src/` または `tests/` に触れた場合のみ `uv run pytest`、必要なら `NLMYTGEN_PYTEST_FULL=1` を opt-in で発火）。**② プラン入力用ドキュメントの完成度**（本ファイル・B-11 パック・[S6-background-animation-next-step-plan-prep.md](../S6-background-animation-next-step-plan-prep.md) の Gate 前提が埋まっているか）。**③ 既存 done 機能のバグ修正のみ**（新 ID 不要の範囲）。 |
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

### 2.3 主軸 (背景アニメ)（次期プランのオプション入力）

- YMM4 で `test_verify_4_bg.ymmp` 系の **見え方**が OK / NG のどちらかを一言で [runtime-state.md](../runtime-state.md) か verification に残す（NG なら failure 観測のみでよい）。
- [S6-background-animation-next-step-plan-prep.md](../S6-background-animation-next-step-plan-prep.md) §2 の **5 条件**を、採用する案についてだけ埋める（未採用案はスキップ可）。

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
| **演出/YMM4** | **C** または **主軸 (背景アニメ)** を時間帯で分ける（同時フルは非推奨）。                             |
| **コア開発**    | 回帰テスト・ドキュメント整合・承認済みバグ修正のみ。プラン文書化は **上記チェックリスト完了後**。              |


---

## 4. コア開発の実装用ドキュメント（A〜E 移譲後）

具体手順・受け入れ・PR は [CORE-DEV-POST-DELEGATION-INDEX.md](CORE-DEV-POST-DELEGATION-INDEX.md) を参照。

---

## 5. 変更履歴

- 2026-04-09: §2.4 にレーン A〜D の repo 準備チェックリストへのリンクを追加（プラン設計前のオペレータ準備を索引化）。
- 2026-04-09: §4 追加（コア開発索引へのリンク）。
- 2026-04-09: §2.5 レーン E（S-8）準備チェックリスト [LANE-E-S8-prep-2026-04-09.md](LANE-E-S8-prep-2026-04-09.md) へのリンクを追加。
- 2026-04-09: 初版。runbook のトラック D/E 見出しを表と整合（D=H-01、E=サムネ）。
- 2026-04-09: §2.1 現状メモを更新（B-11 §5 完了・レーン A 準備ドキュメントへのリンク）。

