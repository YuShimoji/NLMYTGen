# Registry Template

新規プロジェクトで `apply-production` に必要な各種 registry JSON を作成するための雛形。

## 使い方

1. このディレクトリからプロジェクトフォルダにテンプレをコピー
2. `__YOUR_PROJECT_PATH__` 等のプレースホルダを実パスに置換
3. `validate-ir` でエラーが出ないことを確認
4. `apply-production --dry-run` で適用結果をプレビュー

## ファイル一覧

| テンプレ | 用途 | CLI オプション |
|----------|------|---------------|
| `bg_map.template.json` | 背景画像ラベル → パス | `--bg-map` |
| `face_map.template.json` | キャラ × 表情 → パーツパス | `--face-map` |
| `overlay_map.template.json` | オーバーレイ画像ラベル → パス + 属性 | `--overlay-map` |
| `se_map.template.json` | SE 音声ラベル → パス + タイミング | `--se-map` |
| `slot_map.template.json` | キャラ配置スロット（x/y/zoom）+ デフォルト | `--slot-map` |
| `group_motion_map.template.json` | GroupItem 幾何（absolute/relative） | `--group-motion-map` |
| `skit_group_registry.template.json` | 茶番劇 Group の canonical template / 派生 template / fallback / manual check 台帳 | まだ CLI 直結なし（shared registry） |

## パス記法

3 種類のパス表記が使える:

- **絶対パス**: `C:/Users/name/assets/image.png`
- **相対パス**: `assets/image.png`（CLI 実行ディレクトリからの相対）
- **repo 相対**: `samples/backgrounds/studio.png`（リポジトリルートから実行時）

Windows のパス区切りは `/` でも `\\` でも可。

## 各テンプレの補足

### overlay_map / se_map

2 形式をサポート:

- **簡易**: `"label": "path/to/file.png"` -- パスのみ指定
- **拡張**: `"label": { "path": "...", "layer": 4, "anchor": "start" }` -- 属性付き

セクション名（`overlays` / `se`）で囲む形式が推奨。フラットでも動作する。

### slot_map

- `"off": null` はスロット無効（TachieItem を非表示にする）
- `characters` セクションの `default_slot` は IR で slot 未指定時のフォールバック

### face_map

- `extract-template --labeled` で palette.ymmp から自動生成するのが最も正確
- 手動作成する場合、パーツキーは YMM4 の TachieFaceParameter に合わせる（Eyebrow/Eye/Mouth/Hair/Body/Other/Complexion）

### group_motion_map

- `mode: "absolute"`（既定）: 値が GroupItem の最終座標になる
- `mode: "relative"`: 値が GroupItem の現在値に加算される（テンプレ変更に強い）

### skit_group_registry

- `speaker_tachie` 用の `motion` 台帳とは別物
- 配達員などの外部素材演者を **GroupItem テンプレート資産**として記録する
- exact template / fallback / manual check を残し、production での template 解決に使う
- 詳細な運用正本は [docs/SKIT_GROUP_TEMPLATE_SPEC.md](../../docs/SKIT_GROUP_TEMPLATE_SPEC.md)

## face_map_bundle (G-19)

複数体素材を扱う場合は `--face-map-bundle` を使用。テンプレは `samples/face_map_bundle_registry.example.json` を参照。
