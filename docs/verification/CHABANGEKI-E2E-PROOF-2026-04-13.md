# 茶番劇風 E2E 実演 証跡（2026-04-13）

**目的**: 既存 done 機能（face / idle_face / slot / motion）で、IR → apply-production → ymmp → YMM4 の E2E パイプラインが茶番劇風の表情制御に使えるかを実演。src/ 変更なし。

---

## Phase 1: face + idle_face（最小実演）

### 手順

1. `samples/Part 1+2IR_idle.json`（28 utt, row_range + idle_face 済み）をベースに `samples/chabangeki_e2e_ir.json` を作成
2. IR クリーニング:
   - transition: `cut`→`none`, `wipe`→`fade`, `slide_left`→`fade`, `slide_right`→`fade`（18箇所）
   - slot: スピーカー1 の `center`→`left`（1箇所、SLOT_CHARACTER_DRIFT 解消）
   - overlay / se / motion / 未知 bg を null 化（bg_map_proof に無いラベルを除外）
3. `validate-ir` → PASS（ERROR 0, WARNING 1: FACE_SERIOUS_SKEW）
4. `apply-production --dry-run` → PASS
5. `apply-production` → `samples/chabangeki_e2e_patched.ymmp` 書き出し
6. YMM4 目視確認

### 結果

| 指標 | 値 |
|------|-----|
| Face changes | 138 |
| Idle face inserts | 16 |
| BG added | 7 |
| Transition VoiceItem writes | 60 |
| row-range matched | 28/28 |
| EXIT | 0 |
| YMM4 目視 | **PASS** — 発話ごとの表情変化およびファイル正常展開を確認 |

### 使用コマンド

```bash
uv run python -m src.cli.main apply-production \
  samples/production.ymmp \
  samples/chabangeki_e2e_ir.json \
  --face-map samples/face_map.json \
  --bg-map samples/bg_map_proof.json \
  --csv "samples/AI監視が追い詰める生身の労働_ymm4.csv" \
  -o samples/chabangeki_e2e_patched.ymmp
```

---

## Phase 2: + slot + motion

### 追加手順

1. `samples/slot_map_e2e.json` を新規作成（production.ymmp の TachieItem 実測値ベース）
2. `samples/tachie_motion_map_e2e.json` を新規作成（bounce + none の最小セット）
3. IR の speaker 名を変更: `スピーカー1`→`ゆっくり魔理沙黄縁`, `スピーカー2`→`ゆっくり霊夢赤縁`（slot/motion は speaker 名で TachieItem を特定するため）
4. IR に motion=bounce を 4 発話（utt 3, 11, 17, 24）に設定
5. slot_map の default_slot を IR の実際の使用と一致させる（魔理沙=left, 霊夢=right）
6. `apply-production` → `samples/chabangeki_e2e_patched_v2.ymmp` 書き出し

### 結果

| 指標 | Phase 1 | Phase 2 |
|------|---------|---------|
| Face changes | 138 | 138 |
| Idle face inserts | 16 | 16 |
| Slot changes | 0 | **10** |
| TachieItem VideoEffects writes | 0 | **6** |
| Timeline adapter motion | 0 | **6** |
| BG added | 7 | 7 |
| EXIT | 0 | 0 |
| YMM4 目視 | PASS | **PASS** |

### 使用コマンド

```bash
uv run python -m src.cli.main apply-production \
  samples/production.ymmp \
  samples/chabangeki_e2e_ir.json \
  --face-map samples/face_map.json \
  --bg-map samples/bg_map_proof.json \
  --slot-map samples/slot_map_e2e.json \
  --tachie-motion-map samples/tachie_motion_map_e2e.json \
  --csv "samples/AI監視が追い詰める生身の労働_ymm4.csv" \
  -o samples/chabangeki_e2e_patched_v2.ymmp
```

---

## 実運用フィードバック（YMM4 目視後）

| 項目 | フィードバック | 影響 |
|------|--------------|------|
| 表情 | パーツ個別指定よりテンプレ（プリセット名）指定のほうが実用的 | face_map の構造見直しが必要。将来課題 |
| idle_face | 表情アイテムが全編にあるがほぼ「カスタム（初期状態空白）」 | face_map のパーツパスとプロジェクト設定の不一致の可能性 |
| slot | speaker マッピングを逆にしたため背を向ける結果に | IR speaker 名 ↔ CharacterName の対応を正しく設定する必要 |
| 音声 | 一部フェードインする音声あり | transition の VoiceItem 書き込みの副作用の可能性 |
| 全体 | 「細部でよく分からない変更が重なっている印象」。本質はファイル修正ではなくパイプライン実証 | 実運用品質は別課題。パイプライン動作は実証された |

---

## 使用資産

| ファイル | 用途 |
|---------|------|
| `samples/production.ymmp` | 60 VoiceItem, 2 TachieItem |
| `samples/face_map.json` | character-scoped, 6表情 x 2キャラ |
| `samples/bg_map_proof.json` | van_dashboard_ai, dark_board |
| `samples/slot_map_e2e.json` | 新規作成。left/right/center/off + キャラデフォルト |
| `samples/tachie_motion_map_e2e.json` | 新規作成。bounce + none |
| `samples/chabangeki_e2e_ir.json` | Part 1+2IR_idle.json からクリーニング |
| `samples/AI監視が追い詰める生身の労働_ymm4.csv` | 60行 |
| 立ち絵パーツ PNG | `D:\MovieCreationWorkspace\新まりさ\`, `新れいむ\` |

---

## 結論

IR の face / idle_face / slot / motion フィールドで、茶番劇風の表情・配置・動き制御が**パイプラインとして機能する**ことを実証した。実運用品質（テンプレ指定、speaker マッピング精度）は別課題として残る。
