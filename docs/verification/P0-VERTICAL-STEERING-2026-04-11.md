# P0 縦優先 — 舵取り固定（2026-04-11）

本ファイルは [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) と [runtime-state.md](../runtime-state.md) を補助する**短い正本**である。詳細手順は P01 本文へ。

## 1. 本編 P0 縦（単一に固定）

| 項目 | 内容 |
|------|------|
| 主軸案件 | **AI監視が追い詰める生身の労働**（本編 P0） |
| **repo 検証アンカー（経路 B のコーパス）** | `samples/v14_timing_label_split_refined.txt`（P01 表: `v14_t3_timing_label_2026-04-13_a`）。**本番で常にこの refined を正とする意味ではない**（字幕・overflow 検証用の固定サンプル）。 |
| **本番で読む CSV（差し替え可）** | 既定の記録では `samples/v14_t3_ymm4.csv`。**別台本・経路 A のみ**のときはオペレータがパスを置き換え、P01 表と Block-A の記述をその CSV に合わせて更新する。 |
| Amazon Panopticon | **横検証用に据え置き**。[B11-workflow-proof-amazon-panopticon-2026-04-10.md](B11-workflow-proof-amazon-panopticon-2026-04-10.md) §2（YMM4 通し）は **本縦と同時に追わない**。実施する場合は **別オペレータセッション**で B-11 別紙のみ完走させる（本編 Block-A と同一セッションに詰め込まない）。 |


## 2. オペレータ YMM4 作業ブロック（到達ベース）

**目的**: 機械パスだけで縦を止めない。**工程到達**（S-4 等）で進捗を記録する。壁時計の目安・週 cadence は repo 正本に置かない。


| ブロック                   | 到達定義                                                                                                                                                                    | P01 追記                                       |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| **Block-A（必須）** | YMM4 S-4 で **§1 の「本番で読む CSV」**を台本読込し **読込エラーなし**（話者割当は UI 手動で可・[lane_a_phase1_2026-04-09_a](P01-phase1-operator-e2e-proof.md) と同様） | 該当 `run_id` 行の接続判定に **PASS（YMM4 S-4）** 以上を明記 |
| **Block-B（任意・Amazon）** | `samples/amazon_panopticon_B11_ymm4.csv` で S-4 通し → [B11-workflow-proof-amazon-panopticon-2026-04-10.md](B11-workflow-proof-amazon-panopticon-2026-04-10.md) §2.1 実測上書き | B-11 別紙のみ更新（P0 主軸行と混同しない）                    |


**優先順位**: **Block-A が未達なら Block-B に着手しない**。Block-B を挟む場合も、**本編縦の到達を欠損させない**こと（同一セッションで両方を無理に完走させない）。

## 3. run_id（舵取り再スモーク）

機械再確認用: `p0_mainline_v14_steering_2026-04-11_a`（P01 表に 1 行追加。ログは `samples/p0_steering_v14_2026-04-11_*.txt|json`）。

**CLI メモ（v14 検証アンカー用 refined）**: `diagnose-script` / `build-csv` では `--speaker-map` に **`ホストA=れいむ,ホストB=まりさ`** を渡す（`v14_t3_diag.json` と warning 0 件を一致させるため）。`validate` サブコマンドに `--speaker-map` は無い。

## 4. Block-A と経路 A／B（タスク再設計クローズ）

詳細は [P0-BLOCK-A-AND-PATH-A.md](P0-BLOCK-A-AND-PATH-A.md)。

- **Block-A** は §2 表どおり **S-4 読込エラーのみ**（変更なし）。
- **NotebookLM に近い台本**では **経路 A**（`validate`→`build-csv`→YMM4）で足り、**C-09 はこのゲートに含めない**（任意・手戻り用）。
- P01 表の **v5〜v14** は字幕コーパス用の **経路 B** 記録であり、主軸 P0 の必須手順書ではない。