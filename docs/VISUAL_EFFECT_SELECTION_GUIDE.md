# 視覚効果ツール選定ガイド

> **正本**: 本書 + [VISUAL_TOOL_DECISION.md](VISUAL_TOOL_DECISION.md)(ユーザー記入) + [MATERIAL_SOURCING_RULES.md](MATERIAL_SOURCING_RULES.md)(運用ルール)
> **関連**: [C07-visual-pattern-operator-intent.md](C07-visual-pattern-operator-intent.md)(4 類の定義)・[VISUAL_STYLE_PRESETS.md](VISUAL_STYLE_PRESETS.md)(三スタイル実装対応)・[VISUAL_STYLE_YMM4_CHECKLIST.md](VISUAL_STYLE_YMM4_CHECKLIST.md)(手動準備)
> **エフェクト原典**: [samples/effect_catalog.json](../samples/effect_catalog.json)(111 種)・[samples/EFFECT_CATALOG_USAGE.md](../samples/EFFECT_CATALOG_USAGE.md)

## 目的

ゆっくり解説の視覚効果を「どのツールで作るか」を判断する材料を 1 箇所に集める。
過去セッションで散在していた 4 類の定義・3 ルート比較・YMM4 エフェクト 111 種の用途分類を統合し、ユーザーが Step 1「ツール決定」を 30 分で済ませられる状態にする。

本書は **読み物の正本**。決定結果は `VISUAL_TOOL_DECISION.md` に書く。素材調達ルールは `MATERIAL_SOURCING_RULES.md` に書く。

---

## 1. 視覚効果 4 類 × 実現ルート

### 1.1 比較マトリクス

| 類 | 典型用途 | IR `template` | ルートA: YMM4 完結 | ルートB: 外部ツール併用 | ルートC: 完全外製 |
|---|---|---|---|---|---|
| **① 立ち絵+吹き出し (茶番劇)** | 心の声・別路線のせりふ・寸劇 | `skit` | YMM4 立ち絵+テキスト+フキダシ素材 (いらすとや等) | 外部で合成 PNG / AI 生成 (白背景) → `overlay_map` | 動画素材 (AviUtl/AE) → YMM4 上に ImageItem |
| **② 情報列挙 (黒板・カード)** | 所持品・属性・リスト | `data` / `board` | YMM4 テキスト+図形 | 外部エディタ (PowerPoint / AI 生成) → PNG 書出 → `overlay_map` | 図解アニメ (AE) |
| **③ 地図・関係図** | 位置関係・譲歩・整理 | `data` / `board` | YMM4 図形組み合わせ (手間大) | Figma / Inkscape / AI 生成で作図 → PNG → `overlay_map` / `bg_map` | 動画作図 (AE) |
| **④ ムード (雰囲気ストック)** | 背景映像・写真 | `mood` | YMM4 ImageItem + `effect_catalog` (ブラー・パン・ズーム) | Pixabay/Pexels 動画 → YMM4 配置 | 自作撮影・AI 生成 |

### 1.2 推奨デフォルト (運用コスト最小)

- **① 茶番劇 → ルートB**: いらすとや人物 + ゆっくり頭を YMM4 で重畳。G-21 (proposed) の方向性と一致。立ち絵素材は `samples/Mat/` 蓄積中
- **② 情報列挙 → ルートA**: YMM4 テキスト+図形。テンプレ化すれば 3 本目以降の摩擦小
- **③ 地図・関係図 → ルートB**: Figma / Inkscape 等のローカル/Web 作図ツール + AI 生成 (白背景) で PNG を用意。複雑な作図は YMM4 上では非効率
- **④ ムード → ルートA**: Pixabay 等の画像/動画に YMM4 内エフェクト適用

### 1.3 避けるもの

- **コミュニティプラグイン依存エフェクトの多用**: 配布・共有時に再生環境で破綻。自PC完結の案件のみ
- **Python 側での画像生成・合成**: `AUTOMATION_BOUNDARY` で rejected
- **個別動画ごとにオリジナル素材をゼロから作ること**: テンプレ再利用が本筋

### 1.4 サムネイル (独立)

サムネイルは本編動画とは別の成果物。**当初からの方針で YMM4 内作成** (ルートA) を採用する。将来は NLMYTGen 側で「素材置き換え自動化」機能を別途実装する前提。

| ルート | ツール候補 | 長所 | 短所 |
|---|---|---|---|
| **サムネA: YMM4 内 (採用)** | YMM4 の 1 フレーム書き出し | 本編と統一感。テンプレ資産が再利用可。将来の自動化親和性が高い | テキスト組みの自由度は外部ツールに劣る |
| サムネB: Photoshop / GIMP | Adobe PS / GIMP | 最高自由度 | 習熟コスト大。依存が増える |
| サムネC: AI 生成 | Midjourney / Gemini | 速い | 一貫性管理が難 |

**Canva は選択肢から除外** (依存を作らない方針)。

H-02 仕様 ([THUMBNAIL_STRATEGY_SPEC.md](THUMBNAIL_STRATEGY_SPEC.md)) の具体性優先・pattern rotation は、YMM4 テンプレ + registry 方式で達成する (背景・吹き出し・タイトル文字などをラベル化し、`overlay_map` / `bg_map` の延長で「サムネ用 registry」を整備する想定)。

---

## 2. YMM4 エフェクトカタログ活用 (111 種の用途別再編)

`samples/effect_catalog.json` の 9 カテゴリを、視覚効果 4 類への用途別に再編成。コミュニティプラグイン依存品は明示する。

### 2.1 用途別おすすめエフェクト

#### 茶番劇 (skit) 向け

| エフェクト | カテゴリ | コミュ依存 | 用途 |
|---|---|---|---|
| `JumpEffect` | animation_glitch_audio | no | 驚き・反応 |
| `RandomMoveEffect` / `RandomRotateEffect` | animation_glitch_audio | no | 怒り・慌て (揺れ) |
| `InOutJumpEffect` / `InOutCrashEffect` | in_out_animation | no | 登場・退場の強調 |
| `WaveEffect` | animation_glitch_audio | **yes** | ふにゃっとした表現 |
| `ZoomEffect` | transform_position | no | ここぞの強調 |
| `OpacityEffect` | transform_position | no | 心の声の半透明化 |

#### 情報列挙 / 黒板 (data/board) 向け

| エフェクト | カテゴリ | コミュ依存 | 用途 |
|---|---|---|---|
| `InOutGetUpEffect` | in_out_animation | no | リスト項目の立ち上げ登場 |
| `InOutBorderBlurEffect` | in_out_animation | no | 優しい登場 |
| `GradientEffect` | color_blur_shader | no | 黒板の雰囲気 |
| `ChromaticAberrationEffect` | color_blur_shader | no | 強調したい文字の歪み |
| `TilingGroupItemsEffect` | group_tiling | **yes** | 複数カードの自動整列 |
| `RepeatMoveEffect` | animation_glitch_audio | no | 流れる情報列 |

#### 地図・関係図 (data) 向け

| エフェクト | カテゴリ | コミュ依存 | 用途 |
|---|---|---|---|
| `CameraPositionEffect` | camera | no | 地図のパン・ズーム |
| `ZoomEffect` / `AutomaticZoomEffect` | transform_position | no | 詳細箇所への寄り |
| `RadialBlurEffect` / `DirectionalBlurEffect` | color_blur_shader | no | 動き表現 |
| `InOutMoveFromOutsideImageEffect` | in_out_animation | no | 矢印の画面外からのスライドイン |

#### ムード (mood) 向け

| エフェクト | カテゴリ | コミュ依存 | 用途 |
|---|---|---|---|
| `GaussianBlurEffect` | color_blur_shader | no | ボケによる雰囲気 |
| `SepiaEffect` / `TintEffect` / `MonocolorizationEffect` | color_blur_shader | no | 色味で時代・感情演出 |
| `VignetteBlurEffect` | color_blur_shader | **yes** | 周辺暗化 |
| `BloomEffect` | color_blur_shader | **yes** | 光の滲み |
| `NoiseEffect` | color_blur_shader | no | 古い映像感 |
| `CameraPositionEffect` | camera | no | Ken Burns 風 |

### 2.2 本体 / コミュニティ別の運用指針

- **本体のみで組める構成 (71 件)**: 配布・共有案件のデフォルト
- **コミュニティ必須 (40 件)**: 自 PC 内完結案件のみ。サムネ・SNS 切出し素材に活用
- 判定方法: `effect_catalog.json` の `is_community` フラグを grep

### 2.3 テンプレバンドル推奨初期セット

1 つの YMM4 テンプレ (`ItemSettings.json` の `Templates`) に複数エフェクトをバンドルし、registry から呼び出せるようにする想定。

| テンプレ名 (案) | バンドル内容 | 用途 |
|---|---|---|
| `skit_reaction_jump` | JumpEffect + RandomRotateEffect | 茶番劇の驚き |
| `board_list_entry` | InOutGetUpEffect + GradientEffect | 黒板リスト項目 |
| `map_pan_zoom` | CameraPositionEffect (キーフレーム) | 地図パン |
| `mood_sepia_blur` | SepiaEffect + GaussianBlurEffect | 雰囲気回想 |
| `intro_punch` | InOutCrashEffect + ZoomEffect | 冒頭アタック |

これらはユーザーが YMM4 上で作成・保存し、テンプレ名を `scene_presets` ([PRODUCTION_IR_SPEC.md](PRODUCTION_IR_SPEC.md) §6) に登録する運用。

---

## 3. ハンズオン 5 ステップ (ユーザー作業)

```
Step 1: ツール決定 → VISUAL_TOOL_DECISION.md に記入
    ↓
Step 2: 素材調達ルール決定 → MATERIAL_SOURCING_RULES.md に記入
    ↓
Step 3: YMM4 テンプレ初期セット 5 種作成
    ↓
Step 4: registry (bg_map / overlay_map) にラベル登録
    ↓
Step 5: 1 本の実案件で proof → P02 に 1 行追記
```

完了後、`runtime-state.md` の優先表で「視覚効果ツール選定」は hold → **done** に昇格する。

### 3.1 Step 1: ツール決定

`VISUAL_TOOL_DECISION.md` の 7 問に答える。推奨デフォルトをそのまま採用する場合も、明示的に記入する (後で見返すため)。

### 3.2 Step 2: 素材調達ルール

`MATERIAL_SOURCING_RULES.md` に保存場所・命名規約・ライセンス記録・差し替え方針を記入。

### 3.3 Step 3: YMM4 テンプレ初期セット作成

1. YMM4 を起動し、テンプレ作成用の空プロジェクトを開く
2. **アイテム追加 → GroupItem** を作り、内部に立ち絵・背景・テキストなどを並べる
3. アイテム構成を右クリック → **テンプレートとして保存** (名前は §2.3 の案)
4. 5 種類作成
5. `ItemSettings.json` の `Templates` 配列に 5 件追加されていることを確認

立ち絵は `samples/Mat/reimu` / `samples/Mat/marisa` からパス引用。背景は `bg_map.json` 再利用。エフェクトは §2.1 の推奨組み合わせ。

### 3.4 Step 4: registry 登録

#### bg_map.json

```json
{
  "studio_blue": "./backgrounds/studio_blue.png",
  "dark_board": "./backgrounds/dark_board.png",
  "skit_outdoor": "./backgrounds/outdoor.jpg",
  "mood_sepia_bg": "./backgrounds/sepia_wall.png"
}
```

#### overlay_map.json

```json
{
  "overlays": {
    "speech_bubble_right": "./overlays/bubble_right.png",
    "speech_bubble_left": "./overlays/bubble_left.png",
    "list_card_01": "./overlays/card_blue.png",
    "arrow_red": "./overlays/arrow_red.png"
  }
}
```

#### scene_presets (将来・G-21 承認後)

現状は proposed。承認後に assistant が `samples/registry_template/scene_presets.template.json` を作成する想定。

```json
{
  "scene_presets": {
    "skit_reaction": { "ymm4_template": "skit_reaction_jump", "default_bg": "skit_outdoor" },
    "board_list":    { "ymm4_template": "board_list_entry",   "default_bg": "dark_board" }
  }
}
```

### 3.5 Step 5: 実案件で proof

1. `build-csv` で CSV 生成
2. Custom GPT で演出 IR 生成 (新テンプレ名を指定)
3. `validate-ir` と `apply-production --dry-run` で ERROR 0
4. YMM4 で開き、視覚効果が意図どおり出ているか目視
5. OK なら `docs/verification/P02-production-adoption-proof.md` に 1 行追記

---

## 4. 境界線の再確認

- **Python の役割はテキスト変換と registry 解決まで**。画像合成・レンダリングは禁止 ([AUTOMATION_BOUNDARY.md](AUTOMATION_BOUNDARY.md))
- **`patch-ymmp` の現状書込み範囲**: face / idle_face / slot / overlay (ImageItem 挿入) / bg (section 単位) / se (AudioItem)。**motion / transition / bg_anim は未書き込み** (G-12 で route 測定のみ)
- **視覚効果本体 (テンプレの作り込み・素材配置) は YMM4 上で user 作業**。assistant は registry 雛形と判断フレームワークを提供

---

## 5. 変更履歴

- 2026-04-16: 初版。plan `splendid-popping-horizon.md` の §1-2 を repo 内 docs 化。視覚効果ツール選定 slice の起点ファイル
