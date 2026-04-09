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
