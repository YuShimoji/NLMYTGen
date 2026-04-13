# P-02 — 既存 done 機能の実戦投入 proof

目的: `overlay` / `se` / `apply-production` の done 機能を、追加実装なしで運用投入できる状態に固定する。

## 実行日

- 2026-04-07

## 入力アーティファクト

- production ymmp: `samples/production.ymmp`
- IR: `samples/p2_overlay_se_ir.json`
- face map: `samples/face_map.json`
- bg map: `samples/bg_map_proof.json`
- overlay map: `samples/p2_overlay_map.json`
- se map: `samples/p2_se_map.json`
- timeline contract: `samples/timeline_route_contract.json`

## 実行コマンド

```bash
uv run python -m src.cli.main patch-ymmp samples/production.ymmp samples/p2_overlay_se_ir.json \
  --face-map samples/face_map.json \
  --bg-map samples/bg_map_proof.json \
  --overlay-map samples/p2_overlay_map.json \
  --se-map samples/p2_se_map.json \
  --dry-run

uv run python -m src.cli.main apply-production samples/production.ymmp samples/p2_overlay_se_ir.json \
  --face-map samples/face_map.json \
  --bg-map samples/bg_map_proof.json \
  --overlay-map samples/p2_overlay_map.json \
  --se-map samples/p2_se_map.json \
  --timeline-profile production_ai_monitoring_lane \
  --timeline-contract samples/timeline_route_contract.json \
  --dry-run
```

## 実行結果

- `samples/p2_patch_overlay_se_dryrun.txt`
  - `Face changes: 2`
  - `Overlay changes: 2`
  - `SE insertions: 1`
  - `BG added: 1`
- `samples/p2_apply_overlay_se_dryrun.txt`
  - `overlay_map: ... (12 labels)`
  - `se_map: ... (6 labels)`
  - `Overlay changes: 2`
  - `SE insertions: 1`
  - `(dry-run: no file written)`

## 判定

- P2 の「既存 done 機能を実制作へ投入」の最小運用単位は成立。
- 新規コード追加なしで `overlay` / `se` / `apply-production` の連携を確認。
- timeline の再測定は、方針どおり新 sample 追加時または failure class 発生時のみ再実施する。

## N3 追試（複数発話 IR）

### 追加入力

- IR: `samples/n3_multi_utterance_ir.json`（3 utterances）

### 追加コマンド

```bash
uv run python -m src.cli.main apply-production samples/production.ymmp samples/n3_multi_utterance_ir.json \
  --face-map samples/face_map.json \
  --bg-map samples/bg_map_proof.json \
  --overlay-map samples/p2_overlay_map.json \
  --se-map samples/p2_se_map.json \
  --timeline-profile production_ai_monitoring_lane \
  --timeline-contract samples/timeline_route_contract.json \
  --dry-run
```

### 追加結果

- 記録: `samples/n3_apply_multi_utterance_dryrun.txt`
- `Face changes: 7`
- `Overlay changes: 4`
- `SE insertions: 3`
- failure class の ERROR は発生せず、dry-run 完走

### N3 判定

- P2 proof は「1発話のみ」から「複数発話運用」へ拡張できた。

## One-Pass Run (`onepass_2026-04-07_c`)

全要素ワンパス計画の W3 として、同一 run_id で dry-run を再実行。

- 実行ログ: `samples/onepass_2026-04-07_c_apply.txt`
- `Face changes: 7`
- `Overlay changes: 4`
- `SE insertions: 3`
- failure class ERROR: なし（完走）

判定: 1ラン内で Phase1 から演出適用まで接続成立。

## One-Pass Repeat (`s3_onepass_2026-04-08_a`)

- run_id: `s3_onepass_2026-04-08_a`
- apply log: `samples/onepass_2026-04-07_c_apply.txt`（既存ルート再利用）
- 主要値: `Face changes: 7` / `Overlay changes: 4` / `SE insertions: 3`
- 結果: failure class ERROR なし

## Failure Class 再発条件（運用基準）

複数発話IR運用を継続する際、以下を再発条件として扱う。

| 区分 | 再発条件 | 対応 |
|---|---|---|
| ERROR class | `apply-production` が exit 1、または validation ERROR が出る | その run を停止し、同日内で原因切り分け |
| WARNING class（連続） | 同一 warning が 2 run 連続で発生 | map/IR 側の恒久修正候補として backlog 化 |
| WARNING class（単発） | 単発で再現しない | 運用メモのみ。即時実装はしない |
| route mismatch | contract miss が出る | 新しい ymmp sample 起因か確認し、必要時のみ再測定 |

判定ルール: 「ERROR なしで dry-run 完走」を最優先に維持し、WARNING は再発頻度で扱いを分離する。

## Failure Recheck (`r2_failure_recheck_2026-04-08_b`)

- 実行ログ: `samples/r2_failure_recheck_apply.txt`
- 結果: ERROR 0件、WARNING 2件（`FACE_LATENT_GAP`, `IDLE_FACE_MISSING`）
- 判定: 直近 run（`s3_onepass_2026-04-08_a`）と同じ warning パターンのため **連続再発**。
- 対応: 再発条件表に従い、map/IR 側の恒久修正候補として次回 backlog 検討対象へ送る。

## T1/T2 Warning 恒久対処 (`t2_fix_warning_2026-04-08_c`)

### T1 選定

- 対象 warning: `IDLE_FACE_MISSING`
- 選定理由: IR 側の最小修正（`idle_face` 追加）で 1 run 検証が可能、境界を壊さない。

### T2 実施

- 変更IR: `samples/t2_fix_idle_face_ir.json`
- 実行ログ: `samples/t2_fix_idle_face_apply.txt`

### before / after

| 観点 | before (`r2_failure_recheck_apply.txt`) | after (`t2_fix_idle_face_apply.txt`) |
|---|---|---|
| `IDLE_FACE_MISSING` | 発生 | **解消** |
| `FACE_LATENT_GAP` | 発生 | 発生（継続） |
| ERROR class | 0件 | 0件 |

### 判定

- 対象warning（`IDLE_FACE_MISSING`）は解消し、ERROR新規発生なし。
- 次の恒久対処候補は `FACE_LATENT_GAP`。

## T1/T2 FACE_LATENT_GAP 恒久対処 (`t2_face_latent_fix_2026-04-08_d`)

### T1 原因固定

- 対象 warning: `FACE_LATENT_GAP`
- 対象ラベル: `surprised`
- 対象キャラ: `ゆっくり霊夢赤縁`
- 原因: `samples/face_map.json` に `ゆっくり霊夢赤縁.surprised` が未定義。
- 修正方針: map 側のみ最小修正（IR は変更しない）。

### T2 実施

- 変更: `samples/face_map.json` に `ゆっくり霊夢赤縁.surprised` を追加
- 再実行ログ: `samples/t2_face_latent_fix_apply.txt`

### before / after

| 観点 | before (`t2_fix_idle_face_apply.txt`) | after (`t2_face_latent_fix_apply.txt`) |
|---|---|---|
| `FACE_LATENT_GAP` | 発生（`ゆっくり霊夢赤縁: surprised`） | **解消** |
| `IDLE_FACE_MISSING` | 解消済み | 解消維持 |
| ERROR class | 0件 | 0件 |

### 判定

- `FACE_LATENT_GAP` は解消、ERROR 新規発生なし。
- 連続再発 warning 2件（`FACE_LATENT_GAP` / `IDLE_FACE_MISSING`）の恒久対処が完了。

## トラック A — 視覚最低限（VISUAL-MINIMUM §3）`visual_minimum_track_a_2026-04-12_a`

本編 P0 主軸（[P0-VERTICAL-STEERING-2026-04-11.md](P0-VERTICAL-STEERING-2026-04-11.md) §1）と同一コーパス上で、`validate-ir` → `apply-production --dry-run` → 本適用（`-o`）まで通し、[VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md) §3 の機械条件を満たす。**新規 CLI・コード変更なし**（`bg_map` / `overlay_map` / `se_map` は repo 内実在パス向けの検証用 JSON を `samples/track_a_*_repo_paths.json` に追加）。

| 項目 | 値 |
|------|-----|
| run_id | `visual_minimum_track_a_2026-04-12_a` |
| IR | `samples/p2_overlay_se_ir.json`（`macro.sections[].default_bg` = `van_dashboard_ai`） |
| 本番 CSV（主軸記録） | `samples/v14_t3_ymm4.csv`（読込検証の正本は P0 文書 §1） |
| 入力 ymmp | `samples/production.ymmp` |
| 出力 ymmp | `_tmp/visual_minimum_track_a_2026-04-12_a_applied.ymmp` |
| `validate-ir` ログ | `samples/visual_minimum_track_a_2026-04-12_validate.txt`（exit 0、`BG_MISSING` なし） |
| `apply-production --dry-run` ログ | `samples/visual_minimum_track_a_2026-04-12_apply_dryrun.txt`（`BG added: 1`） |
| 本適用ログ | `samples/visual_minimum_track_a_2026-04-12_apply_write.txt` |
| マップ | `samples/track_a_bg_map_repo_paths.json` / `samples/track_a_overlay_map_repo_paths.json` / `samples/track_a_se_map_repo_paths.json` + `samples/face_map.json` + `samples/timeline_route_contract.json` + `--timeline-profile production_ai_monitoring_lane` |
| YMM4 / 背景実体（§3 項 6） | **PASS（readback）** — YMM4 GUI のプレビューは未実施。出力 ymmp を検索し、`YukkuriMovieMaker.Project.Items.ImageItem` で **`Layer` 0** かつ `FilePath` が IR 由来の `bg_map` 解決パス（`samples/v14_t4_thumb_record_2026-04-13_a.png`）であるクリップが存在することを確認（行番号目安: 140838 付近）。単色黒のみの背景ではない。追加のプレビュー確認は `_tmp/visual_minimum_track_a_2026-04-12_a_applied.ymmp` を YMM4 で開けばよい。 |

**補足**: 現行 `validate-ir` は CLI に `--bg-map` が無いため、`default_bg` / `BG_MISSING` 系は IR 本文と `validate-ir` の macro 警告で担保し、ファイル解決は `apply-production` 側の `bg_map` で確認する。

## トラック A 縮小 — macro + micro `bg` + `bg_map` のみ（`track_a_bg_only_2026_04_13`）

別レーンで立ち絵（G-19/G-20）を進める前提で、**IR から overlay / se を外し**、utterance には **`bg` と `transition: none` のみ**を明示（表情は `macro.sections[].default_face` に寄せる）。`validate-ir` → `apply-production --dry-run` の機械経路を切り分けて記録する。

| 項目 | 値 |
|------|-----|
| run_id | `track_a_bg_only_2026_04_13` |
| IR | `samples/track_a_bg_only_ir_2026-04-13.json` |
| `bg_map` | `samples/track_a_bg_only_map_2026-04-13.json`（ラベル `van_dashboard_ai` / `dark_board` → repo 内 PNG） |
| 入力 ymmp | `samples/production.ymmp` |
| `validate-ir` | exit 0（`FACE_SERIOUS_SKEW` / `IDLE_FACE_MISSING` の warning のみ） |
| `apply-production --dry-run` | ログ: `samples/track_a_bg_only_apply_dryrun_2026-04-13.txt`。`BG added: 2`、`Face changes: 2`（既定表情の機械適用）、`Overlay changes: 0`、`SE insertions: 0`。`TRANSITION_MAP_MISS: transition label 'none' not in transition_map` は warning（本 run では `none` 固定のまま）。 |
| YMM4 | **未実施**（dry-run のみ）。本適用は別レーンと同一 ymmp を触る場合は適用順を合意してから `-o` 実行。 |

**判定**: 背景ラベル解決と `apply-production` の bg 経路が、overlay/se 無しでも機械的に通ることを repo 内で確認。立ち絵本体の契約変更は本 run のスコープ外。
