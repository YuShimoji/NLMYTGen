# P0 縦優先 — 舵取り固定（2026-04-11）

本ファイルは [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) と [runtime-state.md](../runtime-state.md) を補助する**短い正本**である。詳細手順は P01 本文へ。

## 1. 今期の縦（1 本に固定）

| 項目 | 内容 |
|------|------|
| 主軸案件 | **AI監視が追い詰める生身の労働**（本編 P0） |
| 現行 refined 先端 | `samples/v14_timing_label_split_refined.txt`（P01 表: `v14_t3_timing_label_2026-04-13_a`） |
| 出力 CSV（機械正） | `samples/v14_t3_ymm4.csv`（365 rows・overflow 候補 16 行・当該行の根拠は P01 サイクル節） |
| Amazon Panopticon | **横検証用に据え置き**。[B11-workflow-proof-amazon-panopticon-2026-04-10.md](B11-workflow-proof-amazon-panopticon-2026-04-10.md) §2（YMM4 通し）は **本縦と同時に追わない**。実施する場合は別カレンダーブロックで B-11 別紙のみ完走させる。 |

## 2. オペレータ YMM4 カレンダーブロック（最低限）

**目的**: 機械パスだけで縦を止めない。到達工程で進捗を記録する。

| ブロック | 所要目安 | 到達定義 | P01 追記 |
|----------|-----------|----------|----------|
| **Block-A（必須）** | 60〜90 分 | YMM4 S-4 で `samples/v14_t3_ymm4.csv` を台本読込し **読込エラーなし**（話者割当は UI 手動で可・[lane_a_phase1_2026-04-09_a](P01-phase1-operator-e2e-proof.md) と同様） | 新 `run_id` 行の接続判定に **PASS（YMM4 S-4）** 以上を明記 |
| **Block-B（任意・Amazon）** | 60〜90 分 | `samples/amazon_panopticon_B11_ymm4.csv` で S-4 通し → [B11-workflow-proof-amazon-panopticon-2026-04-10.md](B11-workflow-proof-amazon-panopticon-2026-04-10.md) §2.1 実測上書き | B-11 別紙のみ更新（P0 主軸行と混同しない） |

**推奨運用**: 週 1 回は **Block-A を先**。Amazon を進める週は Block-A を削らず、別日に Block-B。

## 3. run_id（舵取り再スモーク）

機械再確認用: `p0_mainline_v14_steering_2026-04-11_a`（P01 表に 1 行追加。ログは `samples/p0_steering_v14_2026-04-11_*.txt|json`）。

**CLI メモ（v14 refined）**: `diagnose-script` / `build-csv` では `--speaker-map` に **`ホストA=れいむ,ホストB=まりさ`** を渡す（`v14_t3_diag.json` と warning 0 件を一致させるため）。`validate` サブコマンドに `--speaker-map` は無い。
