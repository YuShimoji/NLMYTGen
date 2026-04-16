# B-2 haitatsuin 案件 dry-run proof (2026-04-17)

**位置づけ**: 主軸「演出配置自動化の実戦投入」の 2 本目。B-1 (e2e 回帰) / B-3 (production 再実証) に続き、haitatsuin 新規エピソードで `apply-production --dry-run` が ERROR 0 で通ることを固定する。

**ステータス**: **dry-run PASS**。視覚確認 (YMM4 で開き立ち絵が発話中も表示されるか) は別レーン ([HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md](HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md) 2026-04-17 4 次追記の「道 1 (実機 1 件 + diff + 一括)」で解決予定) で追跡。

## run_id

`b2_haitatsuin_dryrun_2026-04-17`

## 入力アーティファクト (SHA256)

| 種別 | パス | SHA256 |
|------|-----|--------|
| production ymmp | `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp` | `ca204a7528159511ae457bf55d836760246c6165557ecbb7149e63f8ad8e6e07` |
| IR (10 utt) | `samples/_probe/b2/haitatsuin_ir_10utt.json` | `5342941fe7fccce6293ab2998ac147d6b8b7dc94f00cd18981f9f6610a124852` |
| face_map (character-scoped, 3 表情) | `samples/face_map_bundles/haitatsuin.json` | `d5a687620b3c3e3f9b59330fe197d21a56d271b8b42d60bc479c0219cdb404e0` |
| overlay_map (最小, 0 label) | `samples/overlay_map_haitatsuin.json` | `4ea75043629baabc19232522baf1eea2122584585ec470ebec301f17411d38e3` |

## 実行コマンド

```bash
uv run python -m src.cli.main apply-production \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/b2/haitatsuin_ir_10utt.json \
  --face-map samples/face_map_bundles/haitatsuin.json \
  --overlay-map samples/overlay_map_haitatsuin.json \
  --dry-run --format json
```

ログ: `samples/_probe/b2/b2_dryrun_out.json` / `samples/_probe/b2/b2_dryrun_err.txt`

## 結果

| 指標 | 値 |
|------|-----|
| exit code | **0** |
| `success` | `true` |
| `dry_run` | `true` |
| `fatal_warning_count` | **0** |
| `face_changes` | **18** (10 utt × {serious 6 / smile 4} × ~2 パーツ変化/発話) |
| `slot_changes` | 0 |
| `overlay_changes` | 0 (overlay_map は最小で 0 label) |
| `se_plans` | 0 |
| `bg_additions` | 0 (bg_map 未指定) |
| `transition_changes` | 10 |
| `motion_changes` | 3 |
| `group_motion_changes` | 0 |
| warnings (non-fatal) | 10 件 (下記) |

### 非 fatal warning 一覧

1. `FACE_SERIOUS_SKEW: face 'serious' is 60% of utterances (threshold: 40%)` — 10 utt 中 6 件 serious のため偏り警告。案件の話題 (AI 監視・労働) 上自然な分布
2. `FACE_PROMPT_PALETTE_GAP` ×4 — prompt contract の `angry/sad/surprised/thinking` が palette (face_map) に未定義。face_map を 3 表情→6 表情に拡張する将来課題
3. `FACE_PROMPT_PALETTE_EXTRA: palette label 'neutral' is not listed in prompt contract` — palette に `neutral` があるが contract 外。今回 IR では `neutral` 未使用で回避
4. `FACE_LATENT_GAP` ×2 — キャラごとに不足 prompt label を報告 (同じ将来課題)
5. `IDLE_FACE_MISSING: idle_face is not specified in any utterance` — 今回の最小 IR では idle_face 未指定 (先の slice で必要なら追加)
6. `bg label 'studio_blue' not found in bg_map` — IR `macro.sections[0].default_bg: studio_blue` だが `--bg-map` 未指定。今回 bg 変更は dry-run 対象外

ERROR は**ゼロ**。全 warning は将来の face 拡張 / bg_map 整備で解消予定。

## 整備作業 (本 proof 固有)

- [`samples/_probe/b2/rewrite_face_map.py`](../../samples/_probe/b2/rewrite_face_map.py): face_map_bundles/haitatsuin.json の `migrated_tachie\` プレフィックスを `..\Mat\` へ一括書き換え (36 パス、実在検証付き)
- [`samples/_probe/b2/inspect_layers.py`](../../samples/_probe/b2/inspect_layers.py): ymmp の layer 構造・CharacterName 分布・TachieFaceParameter 詳細の dump
- [`samples/_probe/b2/compare_tachie_paths.py`](../../samples/_probe/b2/compare_tachie_paths.py): TachieItem vs VoiceItem のパス完全一致検査
- face_map backup: [`samples/_probe/b2/haitatsuin_face_map_backup.json`](../../samples/_probe/b2/haitatsuin_face_map_backup.json)

### 手動修正 1 件

`samples/Mat/新れいむ/口/03.png` が非実在のため、smile / Mouth のみ `..\Mat\新れいむ\口\03b.png` に置換 ([samples/face_map_bundles/haitatsuin.json](../../samples/face_map_bundles/haitatsuin.json) L40)。他 35 パスは rewrite スクリプトで一括解決。

## IR 設計メモ

- face ラベル分布 (10 utt): serious 6 / smile 4 (neutral 使用不可のため smile に寄せ)
- `neutral` は face_map に存在するが prompt contract `docs/S6-production-memo-prompt.md` の 6 label (`angry/sad/serious/smile/surprised/thinking`) に未定義 → IR で `neutral` を使うと `PROMPT_FACE_DRIFT` ERROR で停止するため、3 件を `smile` へ変更
- row_range / body_id / slot / overlay / se / group_motion / motion / transition / bg_anim は**未指定**。最小版 proof

## 関連

- B-1 (e2e 回帰 2026-04-16): [B1-e2e-test-regression-proof-2026-04-16.md](B1-e2e-test-regression-proof-2026-04-16.md)
- B-3 (production 再実証 2026-04-16): [B3-production-reproof-2026-04-16.md](B3-production-reproof-2026-04-16.md)
- 立ち絵発話中非表示 (別レーン): [HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md](HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md) 2026-04-17 4 次追記
- 上位台帳: [P02-production-adoption-proof.md](P02-production-adoption-proof.md)

## 次段

- 視覚確認パス (立ち絵発話中表示問題) の解決 → YMM4 で開いて 10 utt を再生、face 切替が反映されるか目視
- face_map を 3 表情 → 6 表情 (prompt contract 準拠: angry/sad/surprised/thinking 追加) に拡張する別スライス
- bg_map / idle_face を integrate した 2 次 dry-run (今回は最小版、将来拡張)

## 2026-04-17 v2 追記 — face_map 6 表情拡張 + IR 再構築で warning 大幅削減

### 実施

`samples/palette.ymmp` から `extract-template --labeled --format json` で 11 パターン抽出 → `D:\MovieCreationWorkspace\` → `..\Mat\` に変換し、既存 haitatsuin.json (3 表情: neutral/smile/serious) に **7 パターン新規追加** ([samples/_probe/b2/expand_face_map.py](../../samples/_probe/b2/expand_face_map.py))。

追加内訳:
- ゆっくり魔理沙黄縁: **surprised / thinking / angry / sad** (4 新規、既存 3 と合わせ計 7 表情)
- ゆっくり霊夢赤縁: **thinking / angry / sad** (3 新規、palette に霊夢 surprised 欠如、計 6 表情)

palette に未抽出の Other/Back キーは既存 neutral から継承。MISSING 0。

### IR v2 作成

[samples/_probe/b2/haitatsuin_ir_10utt_v2.json](../../samples/_probe/b2/haitatsuin_ir_10utt_v2.json) — セリフ内容に合わせ 6 表情分散配置 (serious 3 / thinking 2 / sad 2 / surprised 1 / smile 1 / angry 1)。

### v2 dry-run 結果

```bash
uv run python -m src.cli.main apply-production \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/b2/haitatsuin_ir_10utt_v2.json \
  --face-map samples/face_map_bundles/haitatsuin.json \
  --overlay-map samples/overlay_map_haitatsuin.json \
  --dry-run --format json
```

| 指標 | v1 | **v2** |
|------|-----|-------|
| exit code | 0 | **0** |
| `success` | true | **true** |
| `fatal_warning_count` | 0 | **0** |
| `face_changes` | 18 | **50** (+32) |
| `transition_changes` | 10 | 10 |
| `motion_changes` | 3 | 2 |
| warnings | 10 件 | **4 件** |

### 解消した warning (6 件)

- `FACE_PROMPT_PALETTE_GAP` × 4 (angry/sad/surprised/thinking が palette に無い) → **解消** (face_map に追加)
- `FACE_LATENT_GAP` (魔理沙側) → **解消**
- `FACE_SERIOUS_SKEW` (60% > threshold 40%) → **解消** (serious 30% に分散)

### 残る warning (4 件、全て non-fatal)

- `FACE_PROMPT_PALETTE_EXTRA: palette label 'neutral' is not listed in prompt contract` — neutral を保持したまま (user 判断事項)
- `FACE_LATENT_GAP: character 'ゆっくり霊夢赤縁' is missing prompt labels: surprised` — palette.ymmp に霊夢 surprised の表情が定義されていない。palette に追加する別作業
- `IDLE_FACE_MISSING` — IR に idle_face 未指定 (将来拡張)
- `bg label 'studio_blue' not found in bg_map` — bg_map 未指定 (別拡張)

### 生成物 (v2)

- `samples/_probe/b2/palette_extract/face_map.json` — palette.ymmp からの生抽出 (D:\ 絶対パス、参照用)
- `samples/_probe/b2/haitatsuin_face_map_pre_expand.json` — 拡張前 face_map backup
- `samples/face_map_bundles/haitatsuin.json` — **拡張後の正本** (魔理沙 7 表情 / 霊夢 6 表情)
- `samples/_probe/b2/haitatsuin_ir_10utt_v2.json` — 6 表情版 IR
- `samples/_probe/b2/b2_dryrun_v2_{out.json,err.txt}` — v2 dry-run 出力
