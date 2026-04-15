# プロジェクト初期化チェックリスト

新規動画プロジェクトで演出 IR (`apply-production`) を使い始めるための手順。

## 前提条件

- [ ] YMM4 プロジェクト（.ymmp）が存在する
- [ ] 台本 CSV が生成済み（NLM → `build-csv` で変換済み）
- [ ] 演出 IR JSON が LLM で生成済み

---

## Step 1: palette 準備

palette.ymmp から face_map を抽出する。

```bash
# palette から face ラベル付き face_map を生成
uv run python -m src.cli.main extract-template --labeled palette.ymmp -o face_map.json
```

- [ ] palette.ymmp を決定
- [ ] `extract-template --labeled` を実行
- [ ] 出力された `face_map.json` のパーツパスが実ファイルと一致するか確認
- [ ] キャラ名が IR の `speaker` フィールドと一致するか確認

---

## Step 2: registry 作成

`samples/registry_template/` からテンプレをプロジェクトフォルダにコピーし、プレースホルダを実パスに置換する。

- [ ] `bg_map.json`: 使用する背景画像のラベル → パスを記入
- [ ] `overlay_map.json`: オーバーレイ画像のラベル → パス（+ 任意属性）を記入
- [ ] `se_map.json`: SE 音声のラベル → パス（+ 任意 anchor/offset）を記入
- [ ] `slot_map.json`: キャラ配置スロット（x/y/zoom）と characters.default_slot を記入
- [ ] `group_motion_map.json`:（使う場合のみ）absolute/relative のラベルを定義

各テンプレの書式詳細は `samples/registry_template/README.md` を参照。

---

## Step 3: IR 検証

```bash
uv run python -m src.cli.main validate-ir ir.json \
  --face-map face_map.json \
  --bg-map bg_map.json \
  --slot-map slot_map.json \
  --overlay-map overlay_map.json \
  --se-map se_map.json \
  --group-motion-map group_motion_map.json
```

- [ ] ERROR 0 件を確認
- [ ] WARNING を確認し、許容するものを記録
- [ ] `FACE_UNKNOWN_LABEL` が出たら face_map を更新（Step 1 に戻る）
- [ ] `*_UNKNOWN_LABEL` が出たら該当 map を更新（Step 2 に戻る）

---

## Step 4: ドライラン

```bash
uv run python -m src.cli.main apply-production production.ymmp ir.json \
  --face-map face_map.json \
  --bg-map bg_map.json \
  --slot-map slot_map.json \
  --overlay-map overlay_map.json \
  --se-map se_map.json \
  --group-motion-map group_motion_map.json \
  --csv script.csv \
  --dry-run
```

- [ ] fatal warning 0 件を確認
- [ ] 変更件数（face_changes / slot_changes / overlay_insertions 等）が期待値と一致
- [ ] fatal warning が出たら [FAILURE_DIAGNOSIS_MATRIX.md](FAILURE_DIAGNOSIS_MATRIX.md) を参照

---

## Step 5: 本適用

```bash
uv run python -m src.cli.main apply-production production.ymmp ir.json \
  --face-map face_map.json \
  --bg-map bg_map.json \
  --slot-map slot_map.json \
  --overlay-map overlay_map.json \
  --se-map se_map.json \
  --group-motion-map group_motion_map.json \
  --csv script.csv \
  -o production_patched.ymmp
```

- [ ] YMM4 で `production_patched.ymmp` を開く
- [ ] 字幕表示・表情切替・背景・オーバーレイ・SE を目視確認
- [ ] [P02-production-adoption-proof.md](P02-production-adoption-proof.md) に 1 行追記

---

## トラブルシューティング

ERROR / WARNING の意味と対処法は [FAILURE_DIAGNOSIS_MATRIX.md](FAILURE_DIAGNOSIS_MATRIX.md) を参照。

### クイックリファレンス

| 症状 | 原因 | 対処 |
|------|------|------|
| 全部 `FACE_MAP_MISS` | face_map が古い | `extract-template` を再実行 |
| `ROW_RANGE_MISSING` 大量 | row_range なし + CSV なし | `--csv` を指定、または `annotate-row-range` |
| `VOICE_NO_TACHIE_FACE` | テンプレに立ち絵なし | YMM4 でキャラに立ち絵を割当 |
| `GROUP_MOTION_TARGET_MISS` | Remark 不一致 | YMM4 の GroupItem.Remark を確認 |

---

## 関連ドキュメント

- [FAILURE_DIAGNOSIS_MATRIX.md](FAILURE_DIAGNOSIS_MATRIX.md) -- 全 failure class の診断マトリクス
- [mass-production-pilot-checklist.md](mass-production-pilot-checklist.md) -- 量産パイロットチェックリスト
- [P02-production-adoption-proof.md](P02-production-adoption-proof.md) -- 実戦投入の証跡記録
- `samples/registry_template/README.md` -- registry テンプレの書式詳細
