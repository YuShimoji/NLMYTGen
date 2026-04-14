# 視覚最低限 + 改行／YMM4 ギャップ — 再策定プラン（2026-04）

本ファイルは **運用正本の補助**である。針・`next_action`・優先表は引き続き **[runtime-state.md](../runtime-state.md)** を正とする。チャット要約・タスク別手順書と同じく、**都度読む短い計画**として位置づける。

## 1. 正本・境界へのリンク表


| 用途                         | 正本パス                                                                                                                                          |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 現在位置・`next_action`         | [runtime-state.md](../runtime-state.md)                                                                                                       |
| Phase 1 Block-A (縦)         | [P0-VERTICAL-STEERING-2026-04-11.md](P0-VERTICAL-STEERING-2026-04-11.md)、[P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md)、[P0-BLOCK-A-AND-PATH-A.md](P0-BLOCK-A-AND-PATH-A.md)（経路 A／C-09 任意） |
| 機能台帳（新規コードは `proposed`→承認） | [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md)                                                                                                 |
| L2/L3 境界                   | [AUTOMATION_BOUNDARY.md](../AUTOMATION_BOUNDARY.md)                                                                                           |
| IR 語彙 vs patch 範囲          | [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md)                                                                   |
| IR 仕様                      | [PRODUCTION_IR_SPEC.md](../PRODUCTION_IR_SPEC.md)                                                                                             |
| 改行・`build-csv` オプション       | [PIPELINE_SPEC.md](../PIPELINE_SPEC.md)、CLI `--help`                                                                                          |
| 主軸 (演出配置自動化) 実戦・採用記録の置き場（任意） | [P02-production-adoption-proof.md](P02-production-adoption-proof.md)                                                                          |


## 2. 二軸の到達定義（ズレの明示）


| 軸                   | 解く痛み                               | 到達の意味（この文書での定義）                                                                                                                                                                         | 正本に含まれないこと                                                  |
| ------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **A: 視覚最低限**        | 黒一色背景のみ・素材の手配置ばかり                  | 本編 **1 案件**で、**既存の** `validate-ir` → `apply-production`（`--dry-run` 後に本適用）を通し、YMM4 上で **レイヤー 0 にテンプレ＋IR 由来の背景が載り、黒単色だけではない**状態をオペレータが確認する                                               | Python がピクセル配置やレンダリングを直接行うこと（C-04/C-05 `rejected` の境界は変えない） |
| **B: 改行／YMM4 ギャップ** | `chars-per-line` と実画面の文字折り返しが一致しない | **同一 CSV 行**について、`build-csv --stats` の機械候補と、YMM4 取込後の **実表示**を対にし、ギャップを 1 行以上記録する（下 §4）。必要になったら [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) に **B-xx `proposed`**（係数・キャリブ CLI 等）を起票する | B-17 を「未実装」と書き換えること（台帳上は `done`。残差はモデル限界として扱う）              |


`**next_action` の Phase 1 Block-A** は **Phase 1 の S-4 接続**までの狭義ゲートである。本ファイルの軸 A・B は **Block-A 通過後**または **オペレータ時間の並列配分**で進め、Block-A の PASS を置き換えない。

## 3. トラック A — 視覚最低限チェックリスト（マトリクス整合）

以下は [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) §2 に照らした **最小セット**（上から順に満たす。案件で不要な行は「スキップ理由」をメモに残す）。

1. **前提**: 対象 ymmp は運用テンプレ（[WORKFLOW.md](../WORKFLOW.md) S-0）を複製したもの。CSV は本番で読むもの（[P0-VERTICAL-STEERING-2026-04-11.md](P0-VERTICAL-STEERING-2026-04-11.md) §1 と整合）。
2. **macro**: `sections[].default_bg` を IR に含め、`BG_MISSING` が出ないことを `validate-ir` で確認（マトリクス §3）。
3. **micro `bg`**: `bg_map`（registry）でファイル解決できるラベルのみ使用。`patch_ymmp` が **はい** の経路に限定。
4. `**validate-ir`**: 使用フィールドが unknown / contract miss でないこと（`face` / `idle_face` / `slot` / `overlay` / `se` を使う場合は台帳・`--overlay-map` / SE 経路の前提を満たす）。
5. `**apply-production`**: まず `--dry-run` で意図どおり差分が出ることを確認し、続けて本適用（手順は [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) およびプロジェクト内既存 proof に従う）。
6. **YMM4（S-6 相当の確認）**: タイムラインで **背景レイヤに実体がある**ことを目視（単色黒のみでない）。立ち絵・オーバーレイは **任意**（最小から一段上げるときは `overlay` の map 経路を追加）。
7. **任意の一段上げ**（同一本内で可）: `transition` は `**none` / `fade` のみ**（それ以外は validate で ERROR）。`se` は **write route が corpus にある場合のみ**。`motion` / `bg_anim` の G-17 系は **最小セットの必須ではない**（B-11 §3 の投資先として別ブロックでよい）。

**記録**: 初回本は [P02-production-adoption-proof.md](P02-production-adoption-proof.md) に 1 行、または案件専用 verification に `run_id`・IR パス・ymmp 識別子・PASS/FAIL を残す。

## 4. トラック B — 改行ギャップ計測テンプレ

`display_width` / `--chars-per-line` / `--max-lines` は **YMM4 のフォント・解像度・字幕スタイルと 1:1 対応しない**（[runtime-state.md](../runtime-state.md) メンテナンス節の「YMM4 幅キャリブレーション」と同趣旨）。

### 4.1 1 セッションで揃える情報


| 項目                  | 記入例                                                    |
| ------------------- | ------------------------------------------------------ |
| `run_id`            | `gapreflow_YYYY-MM-DD_a`                               |
| 台本 / CSV            | パス、`build-csv` の全オプション（`--chars-per-line` 値を必ず記載）      |
| `build-csv --stats` | overflow 候補件数、代表 1〜3 行の `[WARN]` 抜粋（**CSV 行番号・話者**）    |
| YMM4                | プロジェクト名、解像度プリセット、字幕フォント（分かる範囲）                         |
| 取込後実測               | 機械候補 **なし**だが **はみ出しあり** の行（CSV row / 話者 / タイムコード目安）   |
| 取込後実測               | 機械 **WARN** だが実機 **問題なし** の行（あれば）                      |
| 結論                  | `--chars-per-line` の試行値メモ、または「コーパス追加」「将来 B-xx」のどちらへ送るか |


### 4.1.1 記録例（1 セッション分・埋め済み）

以下は **2026-04-12** に repo root で `build-csv --stats` を再実行し、YMM4 側は既存の **B-11 実測正本**（全編通し・§2.2 代表例）と対にしたもの。`run_id` は本ファイル §4.1 の例に合わせる。

| 項目                  | 記録（`gapreflow_2026-04-12_a`）                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `run_id`            | `gapreflow_2026-04-12_a`                                                                                                                                                                                                                                                                                                                                                                                                         |
| 台本 / CSV            | 台本: `samples/AI監視が追い詰める生身の労働.txt` → CSV: `samples/AI監視が追い詰める生身の労働_B11_ymm4.csv`（111 rows）。`build-csv`: `--speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" --max-lines 2 --chars-per-line 40 --reflow-v2 --stats`（[B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md) §1 と同一オプション）。機械ログ控え: `samples/gapreflow_2026-04-12_session_build.txt`（本セッション生成） |
| `build-csv --stats` | overflow 候補 **2** 件。代表抜粋: `[WARN] row 22: まりさ, 推定3行 (display_width=72)`／`[WARN] row 64: れいむ, 推定3行 (display_width=60)`                                                                                                                                                                                                                                                                                            |
| YMM4                | プロジェクト名・解像度プリセット・字幕フォントの**数値・固有名は B11 記録に未記載**（運用テンプレ／レーン A 前提）。取込・通し確認の観測本文は [B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md) §2 を正とする                                                                                                                                                                                                               |
| 取込後実測               | **機械候補なし × 実機はみ出しのみ**: B11 の全編通し記録では **該当行を明示していない**（本欄は「未観測／記録なし」とする）                                                                                                                                                                                                                                                                                                                              |
| 取込後実測               | **機械 WARN × 実機では作業不要**: **row 22 / まりさ** — `[WARN]`（`display_width=72`）だが YMM4 では辞書・手動改行の対象に至らず監視扱い。**row 64 / れいむ** — 同候補（`display_width=60`）だが **4 区分の実作業件数に加算せず**（B11 §2.2-1〜2）。**対照（L2 なし × 実機 Pass）**: **row 1 / れいむ**「ちょっと想像してみてください。」— 通し確認で問題なし（§2.2-3）                                                                                                                                      |
| 結論                  | `--chars-per-line=40` 固定でも L2 は **2 件残存**。実害は B11 のとおり **運用 4 区分では 0**（WARN 行は「見た目注意」止まり）。追加は **コーパス（C-09 等）**、係数・キャリブ CLI が要る塊は **データが溜まった段**で B-xx `proposed` 起票                                                                                                                                                                                                                                                                     |

### 4.1.2 記録例（第2コーパス・v14 主軸・`gapreflow_2026-04-13_b`）

本編 Phase 1 Block-A 縦で固定している **v14 refined** について、B11（AI監視生台本）とは別コーパスで L2 推定を再採取した。YMM4 実機の通し確認は [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) `p0_mainline_v14_steering_2026-04-11_a` を正とし、本表は **CLI 機械ログ ↔ 既存 PASS 行の対照**に留める。

| 項目                  | 記録（`gapreflow_2026-04-13_b`） |
| ------------------- | -------------------------------- |
| `run_id`            | `gapreflow_2026-04-13_b` |
| 台本 / CSV            | 台本: `samples/v14_timing_label_split_refined.txt` → CSV: `samples/gapreflow_2026-04-13_v14_ymm4.csv`（365 rows）。`build-csv`: `--speaker-map "ホストA=れいむ,ホストB=まりさ" --max-lines 2 --chars-per-line 40 --reflow-v2 --stats`（P0 舵取り v14 と同一）。機械ログ控え: `samples/gapreflow_2026-04-13_session_build.txt` |
| `build-csv --stats` | overflow 候補 **16** 件。代表: row **23**（まりさ `display_width=54`）、row **49**（れいむ `display_width=60`）、row **157**（まりさ `display_width=74`）。全行番号はセッションログ参照。 |
| YMM4                | 解像度・フォントの数値は P01 当該行に集約。Block-A（S-4）は **PASS** 済みのため、本 run は「v14 で L2 WARN が B11（2 件）より多いコーパス差」を記録するためのもの。 |
| 取込後実測               | **機械 WARN 16 件**に対し、P01 申告ベースの実害分類は **未再採寸**（別レーン作業との二重負荷を避ける）。次に実機で「はみ出しのみ／不要」の対照を取る場合は `run_id` を分けて追記する。 |
| 結論                  | v14 は **機械 WARN が多コーパス**だが Phase 1 Block-A ゲート（S-4）は通過済み。ギャップ深掘りは **必要な行だけ** YMM4 目視でペア化するか、C-09 コーパスで WARN 純減を優先するかを案件で選択。係数・キャリブ CLI は引き続き **データ溜まり後**に B-xx 起票。 |

### 4.2 P01 表への追記（任意・1 行）

[P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) 末尾の表に、通常の Phase1 行とは別に **メモ列**へ短く足す場合の形式例:

`ギャップ計測: chars-per-line=40、機械 WARN row 22 / YMM4 実機はみ出し row 45（れいむ）、テンプレ1080p`

同一案件で複数回計測する場合は `run_id` を分け、ログファイル名をメモに残す。

## 5. ガバナンス

- **新規コード・新 IR 語彙の patch 化**は [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) へ登録し、承認後に実装する。本プランは **ドキュメントと到達定義**が主成果。
- 視覚軸は **「YMM4 テンプレ + IR + apply-production + オペレータ確認」** の組み合わせに閉じる（[AUTOMATION_BOUNDARY.md](../AUTOMATION_BOUNDARY.md) 再掲）。
- 改行軸は **先に §4 の計測ループを固定**し、データが溜まった段で B-xx 案を起票する。

## 6. `recommended_frontier_order` との関係

[runtime-state.md](../runtime-state.md) の既定「台本 → 演出配置 → 視覚効果」と矛盾しない。オペレータが **並列**で時間を割く場合は、**P0 Block-A 未達のときは軸 A の本番 ymmp 適用を Block-A と同一セッションで無理に詰め込まない**（負荷分散は [P0-VERTICAL-STEERING-2026-04-11.md](P0-VERTICAL-STEERING-2026-04-11.md) の精神に合わせる）。

---

*履歴: 2026-04-11 プラン「視覚最低限 + 改行のプラン再策定」に基づき新設。2026-04-13: §4.1.2 `gapreflow_2026-04-13_b`（v14 コーパス）を追加。*