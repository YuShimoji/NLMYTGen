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

## B-3 再実証 (`b3_reproof_2026-04-16`)

- 日付: 2026-04-16
- 正本: [B3-production-reproof-2026-04-16.md](B3-production-reproof-2026-04-16.md)
- 入力: `samples/production.ymmp` + `samples/chabangeki_e2e_ir.json` + face_map + bg_map_proof + slot_map_e2e + tachie_motion_map_e2e
- 結果: exit 0 / fatal 0 / face_changes **139** (2026-04-13 実績 138 から +0.7% 以内) / slot 10 / bg_additions 9 / motion 10 / tachie_syncs 28 / transition 60
- 決定性: 同一コマンド 2 回実行で出力 JSON が完全一致 (591 bytes, identical)

## B-2 haitatsuin dry-run (`b2_haitatsuin_dryrun_2026-04-17`)

- 日付: 2026-04-17
- 正本: [B2-haitatsuin-dryrun-proof-2026-04-17.md](B2-haitatsuin-dryrun-proof-2026-04-17.md)
- 入力 v1: `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp` + `samples/_probe/b2/haitatsuin_ir_10utt.json` + face_map (3 表情) + overlay_map (最小)
- 結果 v1: exit 0 / fatal 0 / face_changes **18** (10 utt / serious 6 + smile 4) / transition 10 / motion 3 / warnings 10
- 判定 v1: **PASS — B-2 の CLI 経路は機械的に通過**

## B-2 haitatsuin dry-run v2 (`b2_haitatsuin_dryrun_2026-04-17_v2`, face_map 6 表情拡張)

- 日付: 2026-04-17
- 正本: [B2-haitatsuin-dryrun-proof-2026-04-17.md §v2](B2-haitatsuin-dryrun-proof-2026-04-17.md)
- 入力 v2: 同 ymmp + `samples/_probe/b2/haitatsuin_ir_10utt_v2.json` + face_map **6 表情拡張済** (palette.ymmp 由来 angry/sad/surprised/thinking を追加、霊夢 surprised のみ palette 欠如) + overlay_map (最小)
- 結果 v2: exit 0 / fatal 0 / face_changes **50** (+32 vs v1) / transition 10 / motion 2 / warnings **4** (v1 の 10 → 4、6 件解消)
- 解消 warning: `FACE_PROMPT_PALETTE_GAP` × 4 / `FACE_LATENT_GAP` (魔理沙) / `FACE_SERIOUS_SKEW`
- 残 warning (全 non-fatal): `FACE_PROMPT_PALETTE_EXTRA` (neutral 保持) / `FACE_LATENT_GAP` (霊夢 surprised) / `IDLE_FACE_MISSING` / bg_map 未指定
- 判定 v2: **PASS — prompt contract 準拠への到達**。立ち絵発話中非表示問題は user 先行解決済 ([HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md](HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md) 5 次追記)。残 warning は別拡張 (palette に霊夢 surprised 追加 / bg_map 整備 / idle_face 拡張)
- **判定**: pipeline 再現性・決定性ともに確認。主軸「演出配置自動化の実戦投入」の完了条件を production.ymmp で満たした

## B-2 haitatsuin motion_target 本書出し (`b2_haitatsuin_motion_regen_2026-04-19`)

- 日付: 2026-04-19
- 正本: [B2-haitatsuin-motion-target-regen-2026-04-19.md](B2-haitatsuin-motion-target-regen-2026-04-19.md)
- 入力: 同 ymmp + `samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json` (motion_target: layer:10 x 4) + face_map (10 表情版) + bg_map + tachie_motion_map (G-23 23 label)
- 結果: exit 0 / fatal 0 / face_changes **50** / transition 10 / motion 6 / **VideoEffects writes (motion): 6** (motion_target 4 entries が 6 segment 分割)
- 出力 ymmp: `_tmp/b2_haitatsuin_motion_applied_v2.ymmp` (42.66 MB、gitignore)
- 判定: **PASS — motion_target 経路で Layer 10 配達員 ImageItem に VideoEffects を機械的に適用**。次 user action は YMM4 での視覚確認 (Layer 10 セグメント × 4 の各 motion が配達員のみに効き、立ち絵は静止)
- 根拠: runtime-state next_action assistant 先行 (B) + [B2-haitatsuin-dryrun-proof-2026-04-17.md](B2-haitatsuin-dryrun-proof-2026-04-17.md) dry-run PASS

## B-2 haitatsuin library v2 再生成 (`b2_haitatsuin_motion_regen_v3_2026-04-19`)

- 日付: 2026-04-19
- 正本: [B2-haitatsuin-motion-library-v2-2026-04-19.md](B2-haitatsuin-motion-library-v2-2026-04-19.md)
- 背景: v1 (flat only library) では ImageItem への motion_target 直書きでデフォルト補完が効かず「体のみ伸び縮み」「制御されていない」と user 報告。v2 で flat + animation params 両方を EffectsSamples 実値ベースで埋め、panic_shake から RandomZoomEffect を除去
- 入力: 同 ymmp + v3 IR + face_map + bg_map + **tachie_motion_map_library v2.0.0** (102KB)
- 結果: exit 0 / fatal 0 / face_changes 50 / transition 10 / motion 6 / VideoEffects writes (motion): 6
- 出力 ymmp: `_tmp/b2_haitatsuin_motion_applied_v3.ymmp` (42.66 MB、gitignore)
- 判定: **PASS — library v2 で motion 4 種 (nod / surprise_jump / panic_shake / deny_shake) に感情表現として妥当なパラメータ値 (振幅・周期) を書き込み完了**。user 視覚確認で「v1 の貧弱な見え方から実用レベルへ改善されているか」を判定する
- 根拠: user 指示 2026-04-19「要素は全て揃っているはず。一つ一つ丁寧に設定してください」+ EffectsSamples_2026-04-15.ymmp 実サンプル値

## B-2 haitatsuin GroupItem 単一 layer 指定 (`b2_haitatsuin_motion_groupitem_2026-04-19`)

- 日付: 2026-04-19
- 正本: [B2-haitatsuin-motion-groupitem-2026-04-19.md](B2-haitatsuin-motion-groupitem-2026-04-19.md)
- 背景: v4 array proof の実機確認で「頭部だけ小刻み / 体は伸び縮み / 開始位置ズレ」が観察され原因分析。既存 Layer 9 GroupItem が canonical template として完成済であることが判明し、motion_target を `"layer:9"` 単一指定に変更
- 入力: 同 ymmp + v3 IR (motion_target: "layer:9" に変更) + face_map + bg_map + tachie_motion_map v2
- 結果: exit 0 / fatal 0 / Face changes 50 / VideoEffects writes (motion): 10
- **GroupItem 8 segment 分割**: nod (F 0-201) / none / surprise_jump (F 476-574) / none / panic_shake (F 766-910) / none / deny_shake (F 1202-1347) / none — utterance timing で完全対応
- Layer 10/11 の ImageItem には書き込みなし (GroupItem 配下で effect 継承)
- 出力 ymmp: `_tmp/b2_haitatsuin_motion_applied_v5.ymmp` (gitignore)
- 判定: **技術 PASS — canonical template 経路で motion が意図どおり GroupItem に書き込まれた**。UX PASS 判定は user 視覚確認待ち (body + 顔 が同期して動くか)
- 根拠: user 指摘「GroupItem は既に正しく設定されて調整するだけで動く」+ inspect_group_layer.py 実機確認 + INVARIANTS §skit_group の主経路は canonical template

## G-24 starter batch preflight sync (`g24_starter_sync_2026-04-21`)

- 日付: 2026-04-21
- 目的: G-24 の初回 starter batch を `enter_from_left` / `surprise_oneshot` の 2 件に固定し、`samples/canonical.ymmp` 内で観測された copy に assistant 側の registry / preflight / proof を同期する
- コマンド:

```bash
python -m src.cli.main audit-skit-group \
  samples/canonical.ymmp \
  samples/_probe/skit_01/skit_01_ir.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text
```

- 結果: `Anchor group = haitatsuin_delivery_v1` / `anchor layer = 9` / `summary = exact 5, fallback 0, manual_note 0`
- **repo-local inspection**:
  - frame `0` / layer `9` / `haitatsuin_delivery_main`
  - frame `306` / layer `9` / `delivery_enter_from_left_v1`
  - frame `658` / layer `9` / `delivery_surprise_oneshot_v1`
  - 上記 3 group はいずれも `GroupRange=2` で、隣接 layer `10` / `11` に `ImageItem` ペアを持つ
- **starter batch exact 条件**:
  - `enter_from_left` → `delivery_enter_from_left_v1` (`exact`)
    - manual checks: `landing position`, `overshoot + settle timing`
  - `surprise_oneshot` → `delivery_surprise_oneshot_v1` (`exact`)
    - manual checks: `Y-axis only jump height`, `one-shot (no loop)`
- `nod` / `deny_oneshot` / `exit_left` も canonical corpus では `exact` のまま維持されるが、今回の starter batch では **registry catalog / preflight entry** として扱い、初回 native template authoring 完了扱いには含めない
- `motion_target` / `group_motion` は補助経路のまま据え置き。template-first の主経路を置き換えない
- 判定: **PASS — assistant-owned starter packet は canonical-project 内 starter copy に同期完了**。次の user-owned action は `enter_from_left` / `surprise_oneshot` の manual checks を YMM4 上で閉じることで、その後の shared action は production adoption proof に `exact / fallback / manual_note` を追記すること

## G-24 starter batch 後の maintenance default

- 既定順は **B-18 script diagnostics observation → H-01/H-02 on demand → B-17 drift-only**
- H-01 brief は新しい packaging brief が必要な案件でのみ起動し、常時 front に出さない
- B-17 reflow 観測は新しい drift が見えた時だけ verification を更新する

## G-24 cautious starter-to-proof gate (`g24_cautious_gate_2026-04-21`)

- 日付: 2026-04-21
- 目的: standalone native template export を急がず、**manual acceptance → 1 件の production adoption proof → standalone export** の順を gate として固定する
- proof 候補の内容: [skit_01_delivery_dispute_v1_2026-04-19.md](skit_01_delivery_dispute_v1_2026-04-19.md) の 4 scene 構成 + `samples/_probe/skit_01/skit_01_ir.json`
- **Phase 1 gate（user-owned, PASS）**:
  - `delivery_enter_from_left_v1`: `landing position`, `overshoot + settle timing`, body-face sync
  - `delivery_surprise_oneshot_v1`: `Y-axis only jump height`, `one-shot (no loop)`, body-face sync
  - user report (2026-04-21): `enter_from_left` 側に意図しない退場設定が混ざっていたため YMM4 でカット済み。repo-local inspection 上も `InOutMoveFromOutsideFrameEffect` は `IsInEffect=True` / `IsOutEffect=False`。2 件とも loop / body-face drift なしを確認済み
- **Phase 2 gate（assistant-owned, PASS）**:
  - starter 2 件はどちらも `exact` 必須
  - 非 starter intent は `exact / fallback / manual_note` のいずれでもよいが、理由を明示記録する
  - `motion_target` / `group_motion` は補助経路としてのみ許可し、starter 2 件の代替に使った場合は assetization をブロックする

- repo-local check 1: canonical copy corpus は preflight と exact 条件を満たすが、voice anchor を持たない

```bash
python -m src.cli.main apply-production \
  samples/canonical.ymmp \
  samples/_probe/skit_01/skit_01_ir.json \
  --tachie-motion-map samples/tachie_motion_map_library.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --dry-run --format json
```

  - 結果: `success=true`, `skit_audit.summary = exact 5 / fallback 0 / manual_note 0`
  - ただし warning は `MOTION_NO_VOICE_ANCHOR` x5。`samples/canonical.ymmp` は starter copy / exact classification の正本だが、**1 件の production adoption proof を閉じるための voice-anchored ymmp ではない**

- repo-local check 2: old `skit_01` corpus は content / motion proof としては有効だが、G-24 preflight gate には乗らない

```bash
python -m src.cli.main audit-skit-group \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/skit_01/skit_01_ir.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text
```

  - 結果: `SKIT_CANONICAL_GROUP_MISSING`
  - 判定: `skit_01_delivery_dispute_v2` は **content candidate** としては採用するが、現状の surviving ymmp をそのまま G-24 production adoption proof へ昇格しない

- repo-local check 3: canonical anchor を持つ voice-anchored production ymmp で cautious gate の Phase 2 を閉じる

```bash
python -m src.cli.main audit-skit-group \
  samples/haitatsuin_2026-04-12_g24_proof.ymmp \
  samples/_probe/skit_01/skit_01_ir.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text

python -m src.cli.main apply-production \
  samples/haitatsuin_2026-04-12_g24_proof.ymmp \
  samples/_probe/skit_01/skit_01_ir.json \
  --tachie-motion-map samples/tachie_motion_map_library.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --face-map samples/face_map_bundles/haitatsuin.json \
  --bg-map samples/_probe/b2/palette_extract/bg_map.json \
  --dry-run --format json
```

  - `samples/haitatsuin_2026-04-12_g24_proof.ymmp` は user が用意した canonical-anchor + voice-anchored proof ymmp。`audit-skit-group` は `exact=5 / fallback=0 / manual_note=0`
  - starter 2 件はどちらも `exact`:
    - `enter_from_left` → `delivery_enter_from_left_v1`
    - `surprise_oneshot` → `delivery_surprise_oneshot_v1`
  - 非 starter 3 件 (`nod` / `deny_oneshot` / `exit_left`) もすべて `exact`
  - `apply-production --dry-run` は `success=true`、`face_changes=50`、`transition_changes=10`、`motion_changes=8`、`group_motion_changes=0`
  - `group_motion_changes=0` のため、starter 2 件を `motion_target` / `group_motion` で代替していない。template-first が主経路として成立
  - warning は `bg label 'studio_blue' not found in bg_map` の 1 件のみ。starter 2 件の exact 成立と P02 gate を阻害しない non-fatal warning として扱う

- user report check 4: standalone native template library export を starter 2 件で同期

  - user report (2026-04-21): `delivery_enter_from_left_v1` / `delivery_surprise_oneshot_v1` を **名前そのまま**で YMM4 の GroupItem template として登録済み
  - 登録単位は GroupItem で、body/face の `ImageItem` 2 点も含めて保存
  - この report により、starter 2 件は **canonical-project copy + production adoption proof + standalone export** の 3 点セットが揃った
  - `delivery_deny_oneshot_v1` / `delivery_exit_left_v1` / `delivery_nod_v1` は今回の export 対象に含めない

- 現時点の判断:
  - **Phase 1**: PASS（manual acceptance 完了）
  - **Phase 2**: PASS（`samples/haitatsuin_2026-04-12_g24_proof.ymmp` + `samples/_probe/skit_01/skit_01_ir.json` で production adoption proof 完了）
  - **Phase 3**: PASS（starter 2 件の standalone native template library export 完了）
  - Capability Atlas は `skit_group.intent.enter_from_left` / `skit_group.intent.surprise_oneshot` を `direct_proven` 候補へ昇格し、`deny_oneshot` / `exit_left` / `nod` は `template_catalog_only` のまま維持する
