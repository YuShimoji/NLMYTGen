# Motion Preset Library 仕様書

> **目的**: IR の `motion` ラベルに感情・演出パターン名を書くだけで、対応する YMM4 VideoEffects の組み合わせが TachieItem に自動適用される仕組みを定義する。
>
> **背景**: 現状 `tachie_motion_map` には `bounce` / `none` の2ラベルしかない。「驚く」「喜ぶ」「悲しむ」「怒る」「パニック」等の感情表現は、既存の YMM4 エフェクト (111種、`samples/effect_catalog.json`) の**組み合わせとパラメータ調整**で実現可能だが、手動で1つずつ YMM4 テンプレートを作るのは工数が爆発する。
>
> **解決策**: エフェクトカタログから `$type` + パラメータを引き、感情ラベルごとの VideoEffects 配列を `tachie_motion_map.json` として自動生成する。**人間は組み合わせ方針のみ決める**。

---

## 1. 設計原則

### 1-a. 人間がやること (方針のみ)

- 感情ラベル名を決める (例: `surprise_jump`, `panic_shake`)
- 「どんな動きか」を1文で記述する
- 初回のレファレンス効果を YMM4 で確認し、パラメータの体感を掴む

### 1-b. 機械がやること (組み合わせ + 生成)

- `effect_catalog.json` / `EffectsSamples ymmp` から `$type` + デフォルトパラメータを抽出
- 感情ラベル定義テーブルに従い、エフェクトの組み合わせ + パラメータ調整値を生成
- `tachie_motion_map.json` に書き出し
- `validate-ir` で未知ラベルがないことを検証

### 1-c. 既存パイプラインとの接続

```
IR: {"motion": "surprise_jump"}
  ↓ tachie_motion_map.json で解決
  ↓ → [JumpEffect, RandomRotateEffect] の VideoEffects 配列
  ↓ _apply_motion_to_tachie_items() が TachieItem に書き込み
  ↓ apply-production -o patched.ymmp
```

**コード変更不要**。`tachie_motion_map.json` の内容を充実させるだけで新ラベルが使える。

---

## 2. エフェクト原子 (building blocks)

`samples/EffectsSamples_2026-04-15.ymmp` から抽出した、感情表現に使える主要エフェクト。

### 2-a. 動き系

| 原子名 | $type | 用途 | 主要パラメータ |
|--------|-------|------|-------------|
| Jump | `JumpEffect` | 跳ねる | (アニメーション: 高さ・回数) |
| Crash | `CrashEffect` | 衝撃・落下 | Size, FlySpeed, FallSpeed, Impact, RandomRotate |
| RandomMove | `RandomMoveEffect` | 小刻み振動 | (アニメーション: 振幅・周波数) |
| RandomRotate | `RandomRotateEffect` | 揺れ・震え | Is3D |
| RandomZoom | `RandomZoomEffect` | 拡縮揺れ | (アニメーション: 振幅) |
| RepeatMove | `RepeatMoveEffect` | 往復移動 | EasingType, IsCentering |
| RepeatRotate | `RepeatRotateEffect` | 往復回転 | Is3D, EasingType |
| RepeatZoom | `RepeatZoomEffect` | 往復拡縮 | EasingType |

### 2-b. 登場・退場系

| 原子名 | $type | 用途 | 主要パラメータ |
|--------|-------|------|-------------|
| InOutCrash | `InOutCrashEffect` | 衝撃登場 | IsInEffect, IsOutEffect, EffectTimeSeconds, Size, Impact |
| InOutJump | `InOutJumpEffect` | ジャンプ登場 | JumpHeight, Stretch, Period, Distortion |
| InOutGetUp | `InOutGetUpEffect` | 起き上がり登場 | Base, EffectTimeSeconds, EasingType |
| InOutSlide | `InOutMoveFromOutsideImageEffect` | スライドイン | Value(Left/Right/Top/Bottom), EffectTimeSeconds |
| InOutSkew | `InOutSkewEffect` | 歪み登場 | AngleX, AngleY |

### 2-c. 視覚加工系

| 原子名 | $type | 用途 | 主要パラメータ |
|--------|-------|------|-------------|
| Zoom | `ZoomEffect` | 拡大・寄り | (アニメーション: 倍率) |
| Opacity | `OpacityEffect` | 透明度変化 | IsAbsolute |
| Sepia | `SepiaEffect` | セピア調 | (アニメーション: 強度) |
| GaussianBlur | `GaussianBlurEffect` | ぼかし | IsHardBorderMode |
| Gradient | `GradientEffect` | グラデーション | GradientType, Blend |

---

## 3. 感情ラベル定義テーブル

各ラベルは「原子の組み合わせ」で構成される。**これがライブラリの正本**。

### 3-a. リアクション系 (キャラの感情表現)

| ラベル | 意味 | 原子の組み合わせ | 備考 |
|--------|------|----------------|------|
| `surprise_jump` | 驚き・ビックリ | Jump + RandomRotate | 跳ねて揺れる |
| `surprise_crash` | 強い驚き・衝撃 | Crash + RandomRotate | 画面揺れ付き |
| `happy_bounce` | 喜び・嬉しい | Jump (控えめ) | 軽い跳ね |
| `happy_sway` | ご機嫌・楽しい | RepeatMove (小) + RepeatRotate (小) | ゆらゆら |
| `sad_droop` | 悲しみ・落胆 | Opacity (微減) + RepeatMove (遅い縦) | しょんぼり沈む |
| `angry_shake` | 怒り・苛立ち | RandomMove (激しい) + RandomRotate (激しい) | ブルブル震える |
| `angry_crash` | 激怒 | Crash + RandomMove | 衝撃 + 振動 |
| `thinking_zoom` | 考え中 | Zoom (1.05倍に寄る) | じっくり寄り |
| `panic_shake` | パニック・焦り | RandomMove (小刻み) + RandomRotate (小刻み) + RandomZoom (微小) | 細かく全方向に震える |
| `tsukkomi` | ツッコミ | InOutCrash (登場のみ) | 瞬間的な衝撃 |
| `nod` | うなずき | RepeatMove (縦・小) | 頷く動作 |
| `deny_shake` | 首を振る・否定 | RepeatMove (横・小) | 横に振る |

### 3-b. 演出系 (シーン・画面効果)

| ラベル | 意味 | 原子の組み合わせ | 備考 |
|--------|------|----------------|------|
| `entrance_left` | 左からスライドイン | InOutSlide (Left, InOnly) | 登場 |
| `entrance_right` | 右からスライドイン | InOutSlide (Right, InOnly) | 登場 |
| `entrance_top` | 上から落下登場 | InOutSlide (Top, InOnly) | 登場 |
| `entrance_getup` | 起き上がり登場 | InOutGetUp (InOnly) | 下からヌッと |
| `exit_left` | 左へ退場 | InOutSlide (Left, OutOnly) | 退場 |
| `exit_right` | 右へ退場 | InOutSlide (Right, OutOnly) | 退場 |
| `flashback` | 回想・過去 | Sepia + GaussianBlur | セピア + ぼかし |
| `focus_zoom` | 注目・クローズアップ | Zoom (1.15倍) | 寄り |
| `defocus` | ぼかし・背景化 | GaussianBlur + Opacity (微減) | フォーカス外れ |
| `bounce` | 汎用バウンス | BounceEffect | 既存互換 |
| `none` | エフェクトなし | [] | クリア |

### 3-c. 拡張ルール

新しいラベルを追加するとき:

1. **原子の組み合わせで表現できるか** を確認する (上記 2-a〜2-c)
2. 組み合わせとパラメータ方針を**本テーブルに1行追加**する
3. `generate-motion-presets` (後述) を再実行して `tachie_motion_map.json` を再生成する
4. `validate-ir` で新ラベルが解決されることを確認する

**YMM4 でテンプレートを手動作成する必要はない**。

---

## 4. パラメータ調整の方針

エフェクトの `$type` だけでは動きの強さ・速さが制御できない。以下の方針でパラメータを調整する。

### 4-a. YMM4 のアニメーションパラメータ構造

YMM4 の VideoEffects パラメータは 2 種類:

1. **フラットパラメータ**: `Size: 50.0`, `IsInEffect: true` 等 → JSON にそのまま書ける
2. **アニメーションパラメータ**: `JumpHeight: {Values: [{Value: 100.0}], ...}` 等 → キーフレーム対応の入れ子構造

**方針 (v2 - 2026-04-19 改訂)**: **フラットとアニメーション両方**を library に埋める。

- **理由**: v1 (flat only) では TachieItem には YMM4 のデフォルトキーフレームが効くが、**ImageItem/GroupItem (skit_group) に motion_target 経由で直書きする場合は YMM4 のデフォルト補完が効かず、振幅ゼロ相当の動きしか出ない**。実地 proof (`b2_haitatsuin_motion_regen_2026-04-19`) で確認済み。
- **アニメーションパラメータの書き方**: `{ "Values": [{ "Value": <float> }], "Span": 0.0, "AnimationType": "なし", "Bezier": {...} }` の完全構造で記述。キーフレーム複数の場合は `Values` に複数エントリを入れ `Span` に時間指定、`AnimationType` を "加速減速" / "線形" 等に変更。
- **基準値**: `samples/EffectsSamples_2026-04-15.ymmp` から抽出した実サンプル値。各 motion で感情表現として妥当な値へ調整 (例: `nod` の RepeatMove.Y は EffectsSamples の 100px から 15px に控えめ化)。
- **人間が YMM4 上で微調整した場合**: 発話 utterance の TachieItem/ImageItem に直接キーフレームを追加すれば、library の値を上書きできる (YMM4 の通常の override 挙動)。

### 4-b. 強度プリセット

同じ原子でも「控えめ」「標準」「激しい」でパラメータを変える。ラベル末尾の接尾辞で区別:

- `_light` : 控えめ (Size 半減、Speed/Impact 低め)
- (なし) : 標準 (EffectsSamples のデフォルト値)
- `_heavy` : 激しい (Size/Speed/Impact 1.5〜2倍)

例: `panic_shake` / `panic_shake_light` / `panic_shake_heavy`

---

## 5. 生成フロー

### 5-a. 生成スクリプト (将来)

```
python -m src.cli.main generate-motion-presets \
  --effect-catalog samples/effect_catalog.json \
  --preset-definitions docs/MOTION_PRESET_LIBRARY_SPEC.md \
  -o samples/tachie_motion_map_library.json
```

**Phase 1 (初版、2026-04-17)**: 仕様書に基づき `tachie_motion_map_library.json` を**手動 (assistant) で生成**。flat parameter のみ、アニメーション値は空。コード変更なし。

**Phase 2 (v2、2026-04-19)**: アニメーションパラメータまで埋めた library v2 を生成。`samples/_probe/b2/build_library_v2.py` で組み立て。EffectsSamples の実サンプル値を基準に、各 motion の感情表現に応じて振幅・周期を調整。motion_target 経路で ImageItem/GroupItem に直書きしても可視的な動きが出る。

**Phase 3 (将来)**: `generate-motion-presets` サブコマンドを実装。preset 定義テーブルを入力に自動生成。ラベル追加時は定義テーブルに 1 行追加して再生成。

### 5-b. 使用フロー

```
# 1. ライブラリを指定して apply-production
uv run python -m src.cli.main apply-production \
  input.ymmp ir.json \
  --face-map-bundle face_map_bundles/haitatsuin.json \
  --tachie-motion-map samples/tachie_motion_map_library.json \
  -o output.ymmp

# 2. IR に新ラベルを書くだけで自動適用
# ir.json: {"motion": "surprise_jump", "face": "surprised", ...}
```

---

## 6. 既存機能との関係

| 既存機能 | 関係 |
|---------|------|
| `tachie_motion_map` (G-16 Phase2) | **本ライブラリの出力形式そのもの**。コード変更不要 |
| `motion_map` (G-17) | `--timeline-profile` 指定時の別経路。共存可 |
| `group_motion_map` (G-20) | GroupItem の位置制御。motion とは独立に併用可 |
| `slot_map` | キャラ位置。motion とは独立に併用可 |
| `face` / `idle_face` | 表情。motion と**組み合わせて使う** (IR で同一発話に両方指定) |
| `effect_catalog.json` | エフェクト $type の**参照元**。本ライブラリの原子定義に使用 |

---

## 7. FEATURE_REGISTRY 起票

| フィールド | 値 |
|-----------|-----|
| ID | G-23 |
| 機能名 | Motion Preset Library (感情ラベル → エフェクト組み合わせの自動展開) |
| ステータス | proposed |
| レイヤー | L2/L3 |
| スコープ | Phase 1: 仕様書 + JSON 手動生成 (コード変更なし)。Phase 2: `generate-motion-presets` CLI |
| 正本 | 本ファイル (`docs/MOTION_PRESET_LIBRARY_SPEC.md`) |

---

## 適用対象 (2026-04-19 更新)

本 library は **TachieItem / ImageItem / GroupItem 横断で利用可**。従来「speaker_tachie 専用」と位置付けていたが、skit_group の body/顔 ImageItem に motion_target 経由で直書きする需要が確認されたため、**汎用エフェクト台帳**として扱う。

- **TachieItem (解説役ゆっくり立ち絵)**: `motion` フィールドから `_apply_motion_to_tachie_items()` 経由で適用
- **ImageItem/GroupItem (skit_group の body/顔/装飾)**: `motion_target: "layer:N"` 指定で `_apply_motion_to_layer_items()` 経由で適用
- **フラット + アニメ両方埋まった v2 以降**: どちらの経路でも可視的な動きが出る

「speaker_tachie 専用」という制限は削除。ただし motion ラベルの意味 (驚き・喜び等) は立ち絵前提で設計されているため、skit_group で使う場合は「配達員が驚く」「配達員がうなずく」等、**演者に読み替え可能な label のみ採用**する運用。

## 変更履歴

- 2026-04-17: 初版。EffectsSamples 111種から感情ラベル23種 + 原子17種を定義。Phase 1 は JSON 手動生成、Phase 2 で CLI 自動生成
- 2026-04-19: Phase 2 library v2 に更新。flat + 動 param 両方埋め、motion_target 経路で ImageItem/GroupItem にも可視的動作を出す。speaker_tachie 専用制限を解除し TachieItem/ImageItem/GroupItem 横断の汎用台帳に位置づけ直す。panic_shake から RandomZoom を除去 (user feedback: 「体のみ伸び縮み」の原因)。根拠: user 指示 2026-04-19 + b2_haitatsuin_motion_regen_2026-04-19 proof
