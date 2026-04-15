# X-2a 配達員テンプレ茶番劇 dry-run proof (2026-04-16)

**ブロック**: X-2a 先行実地確認
**対象**: [samples/characterAnimSample/haitatsuin_2026-04-12.ymmp](../../samples/characterAnimSample/haitatsuin_2026-04-12.ymmp)
**目的**: 既存 `apply-production` パイプライン（face / slot / group_motion / bg / overlay / motion / transition）が配達員茶番劇 ymmp にどこまで到達するかを機械的に計測し、G-21 (茶番劇体テンプレ) の昇格要否を判定する。

---

## 入力

| 種別 | パス | 備考 |
|---|---|---|
| ymmp | `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp` | 2 TachieItem (解説役) + 4 ImageItem (配達員 体+頭, 2 シーン) + 1 GroupItem + 365 VoiceItem |
| IR | `samples/_probe/haitatsuin_x2a/ir.json` | 3 utterance、face + group_motion 指定 |
| face_map | `samples/_probe/haitatsuin_x2a/face_map_x2a.json` | palette.ymmp から `extract-template --labeled` で抽出 |
| group_motion_map | `samples/group_motion_map.example.json` | 既存 15 label |

## 実行コマンド

```
uv run python -m src.cli.main apply-production \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/haitatsuin_x2a/ir.json \
  --face-map samples/_probe/haitatsuin_x2a/face_map_x2a.json \
  --group-motion-map samples/group_motion_map.example.json \
  --dry-run --format json
```

- Exit: 0
- Fatal warnings: 0
- 出力 JSON: `samples/_probe/haitatsuin_x2a/dry_run_result.json`

---

## 観測結果

### Phase 1-D Step 1: palette → face_map

| 項目 | 結果 |
|---|---|
| キャラ数 | **2** (ゆっくり魔理沙黄縁 + ゆっくり霊夢赤縁) |
| 魔理沙黄縁 表情数 | 5 (serious / smile / thinking / angry / sad) |
| 霊夢赤縁 表情数 | 6 (serious / smile / surprised / thinking / angry / sad) |
| 総パーツパス数 | 55 |
| 不在パス数 | **0** (全て `D:\MovieCreationWorkspace\...` に実在) |
| 移植性 | **環境依存あり**。他環境では `samples/Mat/` への書き換えが必要 |

既存 [samples/face_map.json](../../samples/face_map.json) (魔理沙のみ) は古い抽出。今回の `face_map_x2a.json` が 2 キャラ版の正本。

### apply-production dry-run (JSON 出力)

| 観測項目 | 結果 |
|---|---|
| `face_changes` | **15** (3 utterance × 5 パーツ = 15。期待どおり) |
| `slot_changes` | 0 (IR で未指定) |
| `overlay_changes` | 0 (IR で未指定) |
| `se_plans` | 0 |
| `tachie_syncs` | 0 |
| `bg_changes` | 0 (bg_map 未指定のため `studio_blue` ラベル解決できず) |
| `bg_additions` | 0 |
| `bg_anim_changes` | 0 |
| `transition_changes` | **3** (発話ごとの fade transition、default 反映) |
| `motion_changes` | **2** (TachieItem 既存 `OutlineEffect` の carry-forward) |
| `group_motion_changes` | **0** (DRIFT で書き込みスキップ、下記参照) |
| `fatal_warnings` | 0 |
| `warnings` | 2 (GROUP_MOTION_DRIFT / bg 未解決) |

### 配達員体 / 頭 ImageItem への影響

| Layer | アイテム | 素材 | dry-run で書き換え |
|---|---|---|---|
| Layer 2 | ImageItem (Zoom 172%) | Gemini 生成 配達員体 | **0 件（無変化）** |
| Layer 3 | ImageItem (Zoom 51%) | reimu_easy.png 配達員頭 | **0 件（無変化）** |

→ 現 `apply-production` は **独立 ImageItem を触らない**。OK（想定通り）。

### 警告の分析

1. `GROUP_MOTION_DRIFT: group_target 'Group' uses multiple group_motion labels: reset_center, slide_left, slide_right`
   - 1 つの GroupItem に 3 発話分の異なる motion を割り当てようとしたため、DRIFT 検知で書き込みスキップ
   - G-20 A案は「GroupItem の X/Y/Zoom 単一上書き」であり、時系列キーフレームを持つ既存 GroupItem には適用できない
   - **配達員茶番劇の運用**: 「シーンごとに別 GroupItem を作り、IR で `group_target` を切り替える」設計が必要

2. `bg label 'studio_blue' not found in bg_map`
   - bg_map 未指定のため。bg 検証 proof には無関係、想定通り

---

## G-21 昇格判定

### 判定 3 軸

| 軸 | 結果 | 判定 |
|---|---|---|
| **配達員体+頭 (Layer 2/3) への機械 patch** | 現 `apply-production` は独立 ImageItem を触らない。体+頭は事前に YMM4 上で手動配置するか、新規 `body_map` adapter で ImageItem 挿入を自動化するかの二択 | **部分的に G-21 が有用**。ただし「手動配置 + 解説役 TachieItem のみ機械 patch」で茶番劇の表情切替・反応は成立する |
| **配達員頭の表情切替 (現状 reimu_easy.png 静止画)** | 静止画 ImageItem では face 機能が効かない。頭を TachieFaceItem 化する必要があるが、これは **YMM4 手動工程**で解決可能 | **G-21 不要**。user 手動で頭を TachieFaceItem 置換すれば、既存 face パイプラインで動く |
| **複数 GroupItem での motion 同期** | 単一 GroupItem に複数 motion は DRIFT で不可。シーン分割設計でカバー可能 | **G-21 不要**。G-20 の `group_target` を正しく使い分ける運用で解決 |

### 結論: **3 分岐の (2) — G-21 は当面不要、運用ルール追加で足りる**

**理由**:

1. face 切替は解説役 TachieItem (魔理沙・霊夢) に機械的に効く (`face_changes: 15`)。茶番劇で最も重要な「表情で反応」はそのまま使える
2. 配達員体+頭は ImageItem として YMM4 上で手動配置・合成 PNG 運用すれば足り、Python の機械 patch を増やさなくても再生成は可能
3. 頭を表情切替可能にしたいなら、user が YMM4 で TachieFaceItem に置換するのが最短経路（G-21 body_map 実装よりコスト低）
4. 複数 motion はシーンごとに GroupItem を分け、IR の `group_target` で切り替えれば deterministic に動く

**運用ルールとして追加すべき事項** (別ブロックで docs 化):

- YMM4 上で「配達員テンプレ = (体 ImageItem + 頭 TachieFaceItem) を GroupItem に束ね、group_target 名を付与」する手順
- シーン切替は「新 GroupItem を追加 + group_target を変える」で表現
- 合成 PNG 運用（体+表情違いの頭を事前合成）を select 肢として提示
- `body_map` の将来拡張余地は残す（複数テンプレ量産時に機械化価値が出る場合）

### G-21 再起票の条件

以下のいずれかが顕在化したときに `proposed` → `approved` を再判定する:

- 茶番劇テンプレを **5 件以上蓄積**し、毎回手動 GroupItem 化が制作 bottleneck になる
- 合成 PNG 運用では表情の**組み合わせ爆発**（5 表情 × 3 体 = 15 PNG など）が発生
- user が明示的に「body_map の機械化を優先する」と判断

---

## 成果物

| パス | 役割 |
|---|---|
| `samples/_probe/haitatsuin_x2a/face_map_from_palette.json/` | extract-template 生出力（`face_map.json` + `bg_map.json`） |
| `samples/_probe/haitatsuin_x2a/face_map_x2a.json` | 2 キャラ分の face_map（X-2a proof 用） |
| `samples/_probe/haitatsuin_x2a/ir.json` | 最小 3 utterance IR |
| `samples/_probe/haitatsuin_x2a/dry_run_result.json` | apply-production --dry-run JSON |
| `samples/_probe/haitatsuin_x2a/dry_run_stderr.log` | 実行時ログ |
| `docs/verification/X2A-haitatsuin-dryrun-proof-2026-04-16.md` | 本レポート（正本） |

## 次のアクション候補

1. **G-21 を `proposed` のまま維持**（本 proof の結論）、FEATURE_REGISTRY 備考に X-2a 結果リンク追加
2. **茶番劇テンプレ運用ガイド docs/ に起こす**（YMM4 手動 GroupItem 化 + 合成 PNG 運用の 2 パス）
3. **別の実案件で PROJECT_INIT_CHECKLIST Step 2-5 を 1 本通す**（主軸「演出配置自動化の実戦投入」を進める）
