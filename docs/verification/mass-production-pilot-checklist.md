# Registry 駆動・量産試験チェックリスト

**目的**: 同一の **palette ymmp＋registry 束**で、**IR 差分だけ**を差し替えて何本も `apply-production` できるかを検証する。方針の正本は [C07-visual-pattern-operator-intent.md](../C07-visual-pattern-operator-intent.md) の「量産・自動化の方針」。

## 前提

- 台本 CSV は `build-csv` で既にある（または本試験用に 1 本用意済み）。
- Production IR（JSON）が少なくとも 1 本ある（Custom GPT 出力でも手書きでも可）。

## チェックリスト

### A. 資産の固定（1 プロジェクトに 1 回）

- **palette ymmp** を 1 本決める（表情・背景・立ち位置の母艦）。
- `extract-template --labeled` 等で **face_map のラベル**が実制作と整合している（[OPERATOR_WORKFLOW.md](../OPERATOR_WORKFLOW.md) palette 節）。
- **bg_map.json** / **slot_map**（必要なら）/ **overlay_map** / **se_map** をプロジェクトフォルダに置き、パスを記録する。
- （任意）Template Registry JSON で **scene_presets と ymm4_template 名**を参照できる状態にする（[PRODUCTION_IR_SPEC.md](../PRODUCTION_IR_SPEC.md) §6.4）。

### B. IR と CSV の対応

- IR の **utterance に row_range**（`row_start` / `row_end`）が付く、または `apply-production --csv` で annotate が通る。
- `validate-ir` を **書き出し前ゲート**として実行する（palette / face_map / slot_map 等を実際のコマンドに合わせる）。

### C. 量産ループ（同じ資産・別コンテンツ）

- **同じ palette・同じ map 束**のまま、別 `video_id` または別 utterances の IR を 2 本目用意する。
- `apply-production production.ymmp ir2.json --palette ... --csv ... -o out2.ymmp`（必要な map を付与）が **exit 0** で完了する。
- 失敗時、ログの **failure class 名**で [OPERATOR_WORKFLOW.md](../OPERATOR_WORKFLOW.md) の face / timeline / palette 節を引ける。

### D. 際限の確認（期待値のすり合わせ）

- [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) を開き、**自動で書かない**フィールド（`motion` / `transition`、および **未対応の `bg_anim` プリセット** 等）に依存した量産になっていないか確認する。
- 雰囲気ストック・吹き出し中心の回は **C-07 意図ドキュメント**の「創作・テンプレ依存」側に寄せすぎていないか、チームで一言合意する。

### E. 全編ワンループ proof（顔＋オーバーレイ最小）

**目的**: 一本の動画について、**全 `utterance` に `face`**（carry-forward 可）、**必要な行だけ `overlay`**、**macro `sections` に `default_bg`** を置いた IR で、`validate-ir` → `apply-production` が通るかを確認する。

- IR の **utterance 数**が palette 側の VoiceItem 行と対応している（`row_start` / `row_end` または index モードのどちらかに統一）。
- **全発話**で `face` が欠けない（carry-forward で同一表情の連続は可）。
- **overlay** を出したい発話だけラベルを付け、不要な行は空のまま（または `none` 相当の運用）。
- `validate-ir` が ERROR なし（WARNING は記録して許容するか判断）。
- `apply-production` が **exit 0**。`VOICE_NO_TACHIE_FACE` 等で止まる場合は [OPERATOR_WORKFLOW.md](../OPERATOR_WORKFLOW.md) の face 節で palette / 台本読込を直す。
- 吹き出し**中のテキスト**を台詞ごとに変える必要がある場合、**テキスト入り画像をラベル分用意する**か、YMM4 側の別レイヤーに任せる運用かを決めておく（IR はラベル割当まで）。

## 関連コマンド（例）

```text
python -m src.cli.main validate-ir ir.json --palette palette.ymmp --face-map face_map.json --slot-map slot_map.json
python -m src.cli.main apply-production production.ymmp ir.json --palette palette.ymmp --csv script.csv --bg-map bg_map.json -o out.ymmp
```

`--dry-run` で先に機械サマリのみ確認してもよい。

## 関連

- [C07-visual-pattern-operator-intent.md](../C07-visual-pattern-operator-intent.md)
- [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md)

