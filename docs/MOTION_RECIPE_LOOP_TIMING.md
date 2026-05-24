# Motion Recipe Loop / Timing Reference

> **位置づけ**: [MOTION_PRODUCTION_PIPELINE.md](MOTION_PRODUCTION_PIPELINE.md) Phase C (Recipe Assembly) の **canonical reference**。「感覚」「だいたい」でのパラメータ決定（Anti-Shortcut Rule #6 違反）を構造的に防ぐ。
>
> **正本値の出典**: [`samples/tachie_motion_map_library.json`](../samples/tachie_motion_map_library.json) (24 emotion 用 motion library) + [`samples/_probe/b2/build_library_v2.py`](../samples/_probe/b2/build_library_v2.py) (builder 関数群) + [`samples/_probe/b2/effect_full_samples.json`](../samples/_probe/b2/effect_full_samples.json) (effect 1 件分の完全 JSON 構造)
>
> **scope**: 主要 ~35 effect (skit / motion 制作で使用頻度の高いもの)。残り 76 effect は需要発生時に追加 ([`samples/effect_catalog.json`](../samples/effect_catalog.json) を参照)

---

## 1. Loop Type 5 分類

| loop type | 意味 | 代表 effect | 制御変数 |
|-----------|------|-------------|---------|
| `single-shot` | 1 周期で完結。clip Length が時間枠 | `JumpEffect` / `CrashEffect` | clip Length, Period, Distortion |
| `continuous-repeat` | 規則的反復。Span が 1 周期 | `RepeatMoveEffect` / `RepeatRotateEffect` / `RepeatZoomEffect` | Span, EasingType, IsCentering |
| `continuous-shake` | 不規則反復 (jitter)。Span が再 sample 周期 | `RandomMoveEffect` / `RandomRotateEffect` | Span (短いほど高頻度) |
| `in_out` | clip 始端と終端だけに発火 | `InOutCrashEffect` / `InOutJumpEffect` / `InOutMoveFromOutsideImageEffect` | EffectTimeSeconds, IsInEffect, IsOutEffect |
| `sustained` | clip 全体に常時適用 (視覚フィルタ) | `SepiaEffect` / `GaussianBlurEffect` / `OpacityEffect` / `ChromaticAberrationEffect` | Strength / Blur / Opacity (時間制御なし) |

---

## 2. Duration / Timing Controls 早見表

| 制御変数 | 単位 | 適用先 | 効果 |
|---------|------|--------|------|
| clip `Length` | frame | item レベル (clip 全体) | clip の総尺 (1 frame ≒ 1/30 秒 @30fps) |
| `Span` | second | Random* / Repeat* | 1 周期。短いほど高頻度 |
| `Period` | second | Jump 系 | jump 1 回の上下時間 |
| `EffectTimeSeconds` | second | InOut* | in / out 適用時間 (片側) |
| `Distortion` | int (0-100) | Jump 系 | 着地時 squash の強さ |
| `Stretch` | int (0-100) | Jump 系 | jump 上昇時の縦伸び |
| `Impact` | int (0-200) | Crash 系 | 衝撃の強さ |
| `FlySpeed` / `FallSpeed` | int | Crash 系 | 飛翔・落下の速度 phase |
| `Delay` | second | Crash 系 | clip 始端からの遅延 |
| `Interval` | second | Jump 系 | 連続 jump の間隔 |
| `AnimationType` | enum | route Values | `なし` / `直線移動` / `加速減速` / `加速` / `減速` |
| `EasingType` | enum | Repeat / InOut | `Linear` / `Sine` / `Cubic` / `Expo` / `Quart` / etc. |
| `EasingMode` | enum | Repeat / InOut | `In` / `Out` / `InOut` |
| `Bezier.ControlPoint*` | (-1, 1) | route Values | 補間曲線。default `(-0.3, -0.3)` & `(0.3, 0.3)` ≒ Linear |
| `IsCentering` | bool | Repeat* | `true` で原点を中心に往復、`false` で片側展開 |

---

## 3. Effect ごと canonical 値 (intensity 別)

範囲は `_light` (控えめ) / 標準 / `_heavy` (激しい)。**標準値は [`tachie_motion_map_library.json`](../samples/tachie_motion_map_library.json) で実測済み**。

### 3.1 single-shot 系 (リアクション)

#### `JumpEffect` — 跳ねる動作

| intensity | JumpHeight | Stretch | Period | Distortion | label 例 |
|-----------|-----------|---------|--------|-----------|----------|
| _light | 25 | 10 | 0.5 | 8 | `happy_bounce` |
| 標準 | 40 | 15 | 0.6 | 12 | `bounce` |
| _heavy | 50 | 15 | 0.4 | 10 | `surprise_jump` |

**composition**: `RandomRotateEffect`(Z=10, Span=0.2) と組合せて `surprise_jump` 的な「跳ねつつ揺れる」を作る。Span は Period の半分以下にして jump 内で複数回振る。

#### `CrashEffect` — 衝撃

| intensity | Size | Impact | FlySpeed | FallSpeed | label 例 |
|-----------|------|--------|----------|-----------|----------|
| _light | 30 | 60 | 100 | 100 | (派生) |
| 標準 | 40 | 80 | 100 | 100 | `surprise_crash` |
| _heavy | 60 | 130 | 100 | 100 | `angry_crash` |

**composition**: `RandomRotateEffect`(Z=10, Span=0.2) または `RandomMoveEffect`(X=12, Y=8, Span=0.1) と並列で衝撃感増。

### 3.2 continuous-repeat 系 (反復・往復)

#### `RepeatMoveEffect` — 往復移動 (XYZ)

| intensity | X / Y 振幅 | Span | EasingType | IsCentering | label 例 |
|-----------|-----------|------|-----------|-------------|----------|
| nod (light Y) | Y=15 | 0.4 | Sine | true | `nod` |
| sway (gentle X) | X=12 | 1.5 | Sine | true | `happy_sway` |
| droop (slow Y) | Y=8 | 2.0 | Sine | true | `sad_droop` |
| deny (strong X) | X=25 | 0.5 | Sine | true | `deny_shake` |

**ルール**: `Span` 短い (0.4-0.5) → 速い反復、長い (1.5-2.0) → ゆっくり。`IsCentering=true` で原点復帰、`false` でドリフト。

#### `RepeatRotateEffect` — 往復回転

| intensity | Z 角度 | Span | EasingType | label 例 |
|-----------|-------|------|-----------|----------|
| sway (light Z) | Z=5 | 1.5 | Sine | `happy_sway` |

**注意**: nod は **Rotation route + CenterPointEffect** の組合せでも実現可能 ([G-26 readback finding F-2](verification/G26-motion-recipe-pipeline-2026-04-30.md))。RepeatRotateEffect 経由 vs route 直書きの選択は、anchor 制御の必要性で判断する。

#### `RepeatZoomEffect` — 往復拡縮

label 例なし。Zoom=105 (5% 拡大), Span=0.5 で「呼吸 / 鼓動」演出が可能。

### 3.3 continuous-shake 系 (揺れ・震え)

#### `RandomMoveEffect` — 不規則小移動

| intensity | X | Y | Span | label 例 |
|-----------|---|---|------|----------|
| panic (微小高頻度) | 8 | 6 | 0.05 | `panic_shake` |
| angry (大振幅中頻度) | 15 | 10 | 0.08 | `angry_shake` |
| crash assist | 12 | 8 | 0.1 | `angry_crash` 内 |

**ルール**: Span 0.05 ≒ 1/20 秒 = 高頻度 jitter、Span 0.1 ≒ 1/10 秒 = 中頻度。X / Y を独立に設定可能。

#### `RandomRotateEffect` — 不規則回転

| intensity | Z 角度 | Span | label 例 |
|-----------|-------|------|----------|
| panic | 4 | 0.05 | `panic_shake` |
| angry | 8 | 0.08 | `angry_shake` |
| surprise burst | 10 | 0.2 | `surprise_jump` / `surprise_crash` |

`Is3D=true` で X/Y/Z 軸独立、既定は Z 軸のみ。

#### `RandomZoomEffect` — 不規則拡縮

label 例なし。`panic_shake_heavy` で Zoom=3, Span=0.05 の微小拡縮を加えると「全方向 jitter」が成立。

### 3.4 in_out 系 (登場・退場)

#### `InOutCrashEffect` — 衝撃登場

| usage | EffectTimeSeconds | Size | Impact | label 例 |
|-------|------------------|------|--------|----------|
| tsukkomi | 0.3 | 40 | 80 | `tsukkomi` |

`IsInEffect=true` のみで「登場時に飛び込んでくる」、`IsOutEffect=true` 併用で「退場時に飛んでいく」。

#### `InOutMoveFromOutsideImageEffect` — スライドイン / アウト

| usage | EffectTimeSeconds | EasingType | EasingMode | label 例 |
|-------|------------------|-----------|------------|----------|
| entrance | 0.3 | Expo | Out | `entrance_left/right/top` |
| exit | 0.3 | Expo | In | `exit_left/right` |

`Value` パラメータで方向 (Left / Right / Top / Bottom) を指定。

#### `InOutGetUpEffect` — 起き上がり登場

| usage | EffectTimeSeconds | EasingType | EasingMode | label 例 |
|-------|------------------|-----------|------------|----------|
| entrance | 0.3 | Expo | Out | `entrance_getup` |

下から「ヌッ」と立ち上がる演出。`Base` で起立時の高さ。

#### `InOutJumpEffect` — ジャンプ登場・退場

| usage | EffectTimeSeconds | JumpHeight | Stretch | Period | Distortion |
|-------|------------------|-----------|---------|--------|-----------|
| 標準 | 1.5 - 3.0 | 60 - 100 | 10 | 0.5 | 25 |

長尺 (1.5-3 秒) の登場ジャンプ。`IsInReverse=true` で jump 開始位置反転。

### 3.5 transform 系 (姿勢・透明度)

#### `ZoomEffect` — 拡大縮小 (静的)

| usage | Zoom | label 例 |
|-------|------|----------|
| 寄り | 105 (1.05倍) | `thinking_zoom` (1.05倍想定) |
| 強寄り | 115 (1.15倍) | `focus_zoom` |

clip 全体で固定倍率。アニメーションさせるなら route Values 直書き。

#### `OpacityEffect` — 透明度 (静的)

| usage | Opacity | label 例 |
|-------|---------|----------|
| sad | 85 | `sad_droop` 内 |
| defocus | 70 | `defocus` 内 |

#### `CenterPointEffect` — 回転 / 拡大の中心点

| usage | Vertical | Horizontal | X | Y |
|-------|---------|-----------|---|---|
| nod (頭部 pivot) | `Bottom` | `Custom` | 524.57 | 136.85 |
| 既定中央 | `Center` | `Center` | 0 | 0 |

**重要**: Rotation route を使う primitive (nod / tilt) では `Bottom` + `Custom` (頭部) が必須。これが無いと身体ごと回転する ([G-26 finding F-5](verification/G26-motion-recipe-pipeline-2026-04-30.md))。

### 3.6 視覚加工系 (sustained)

#### `SepiaEffect` — セピア調

| intensity | Strength | label 例 |
|-----------|---------|----------|
| 標準 | 70 | `flashback` (Blur と並列) |

#### `GaussianBlurEffect` — ぼかし

| intensity | Blur | label 例 |
|-----------|------|----------|
| 微 | 3 | `flashback` 内 |
| 標準 | 5 | `defocus` |

#### `ChromaticAberrationEffect` — 色収差

| usage | Strength | 備考 |
|-------|---------|------|
| shock 一瞬 | 5-15 (1-3 frame だけ) | clip Length 全体は適用、強い瞬間表現は route で Strength を瞬間 spike |
| dream sustained | 3-5 | clip 全体 |

#### `GradientEffect` / `MonocolorizationEffect` / `TintEffect` / `NoiseEffect` / `BloomEffect` / `VignetteBlurEffect`

label 例は repo 内未確認。intensity の体感は YMM4 で 1 件試して値を持ち帰る (`extract_effect_params.py` で抽出可能)。

#### `DirectionalBlurEffect` — 方向ブラー

| usage | StandardDeviation | Angle | 備考 |
|-------|------------------|-------|------|
| 速度感 | 5-10 | 0 (水平) | jump / crash と並列で動きの軌跡を強調 |

### 3.7 camera 系

#### `CameraShakeEffect` (community plugin)

| intensity | X / Y | Z | Span | Yaw / Pitch / Roll |
|-----------|-------|---|------|--------------------|
| 標準 | 10 / 10 | 0 | 0.1 | 0 |

**community plugin 警告**: 配布する案件では避ける ([VISUAL_EFFECT_SELECTION_GUIDE.md § 1.3](VISUAL_EFFECT_SELECTION_GUIDE.md))。代替: `RandomMoveEffect` で疑似シェイク。

#### `CameraPositionEffect` — カメラ移動

| usage | X / Y / Z | Rotation | 備考 |
|-------|----------|----------|------|
| Ken Burns 風 | route で X / Y / Zoom を slow drift | RotationY/X/Z=0 | clip 全長に渡って徐々に移動 |
| パン | route で X を直線移動 | 0 | 地図 panning |

### 3.8 ニッチ系 (community)

| effect | community | 用途 | 備考 |
|--------|-----------|------|------|
| `WaveEffect` | yes | ふにゃっ / 揺らぎ | Angle1/2, Amplitude, WaveLength, Period |
| `MeshDeformationEffect` | no | 部分歪み | HorizontalCount × VerticalCount mesh |
| `FlipEffect` | yes | 反転 | IsHorizontal / IsVertical |

---

## 4. Intensity Scaling Formula

Brief の `intensity` フィールド (`light` / `medium` / `strong`) から具体値への換算則:

| 値の種類 | _light | 標準 (medium) | _heavy / strong |
|---------|--------|---------------|-----------------|
| amplitude (移動 X/Y, 角度 Z) | 0.5 - 0.6 × | 1.0 × | 1.5 - 2.0 × |
| Period (Jump 周期) | 1.2 × (ゆっくり) | 1.0 × | 0.7 - 0.8 × (素早く) |
| Span (Random 周期) | 1.5 - 2.0 × (緩) | 1.0 × | 0.5 - 0.7 × (頻繁) |
| Span (Repeat 周期) | 1.5 - 2.0 × (ゆっくり) | 1.0 × | 0.7 - 0.8 × (素早く) |
| Distortion / Stretch (Jump squash) | 0.7 × | 1.0 × | 1.3 × |
| Impact (Crash 衝撃) | 0.6 × | 1.0 × | 1.5 - 1.8 × |
| Strength (視覚加工) | 0.5 × | 1.0 × | 1.3 - 1.5 × |

**重要な非対称**: shake (Random*) は「弱いほど Span を長く」、swing (Repeat*) は「弱いほど Span を長く」だが、Jump は「弱いほど Period を **長く**」。jump は単発なので「速い jump = 強い」、shake は連続なので「速い shake = 強い」。

---

## 5. Composition Rules (複数 effect 同時適用)

| 組合せ | timing 整合 | 用途 |
|-------|------------|------|
| `JumpEffect` + `RandomRotateEffect` | random Span を jump Period の半分以下 | `surprise_jump` |
| `CrashEffect` + `RandomMoveEffect` / `RandomRotateEffect` | crash Impact phase と random の最大振幅を frame 0 で同期 | `surprise_crash` / `angry_crash` |
| `CrashEffect` + `CameraShakeEffect` | 両者 frame 0 起点。CameraShake Span 0.1 で短時間 | 強衝撃 |
| `RepeatMoveEffect` X + `RepeatRotateEffect` Z | 両者 Span を同じ → 同期、ずらす → ドリフト感 | `happy_sway` |
| `OpacityEffect` + `RepeatMoveEffect` | sad は Opacity=85, RepeatMove Y=8 (slow) | `sad_droop` |
| `SepiaEffect` + `GaussianBlurEffect` | 両者 sustained。Sepia=70, Blur=3 | `flashback` |
| `GaussianBlurEffect` + `OpacityEffect` | 両者 sustained。Blur=5, Opacity=70 | `defocus` |
| `RandomMoveEffect` + `RandomRotateEffect` + `RandomZoomEffect` | 三方向 Span を同じ → 全方向 jitter | `panic_shake_heavy` |
| `ChromaticAberrationEffect` + `ZoomEffect` | Strength の spike と Zoom の peak を同 frame で同期 | shock 強調 |
| `CenterPointEffect` + Rotation route (clip 直書き) | Rotation の primitive は anchor 必須 | nod / tilt |

**禁忌**: 同一軸を異なる effect で 2 重制御しない (例: route Y + RepeatMoveEffect Y は重畳して predict 不能)。

---

## 6. AnimationType / EasingType 補足

### route Values の `AnimationType`

| 値 | 意味 | 使い所 |
|---|------|-------|
| `なし` | 1 frame だけ静的 | 値が 1 つのみのとき |
| `直線移動` | linear interpolation | nod / surprise_oneshot のような単純往復 |
| `加速減速` | ease-in-out | 加速して減速、自然な振り |
| `加速` | ease-in | 始動から徐々に速く |
| `減速` | ease-out | 入って減速 (entrance) |
| `なめらか` | smooth (Bezier 制御) | Bezier ControlPoint で fine-tune |

### Repeat* / InOut* の `EasingType`

| 値 | 意味 |
|---|------|
| `Linear` | 等速 |
| `Sine` | 三角関数 (滑らか、自然) — repeat 系の既定 |
| `Cubic` | 強めの ease-in-out |
| `Expo` | 指数。entrance/exit の既定 (急激な開始/終了) |
| `Quart` / `Quint` | より急峻 |

### `EasingMode`

| 値 | 意味 |
|---|------|
| `In` | 始動加速 (退場系で使う) |
| `Out` | 入って減速 (登場系で使う) |
| `InOut` | 両端で減速 (反復系で使う) |

### `Bezier` 既定値

[`build_library_v2.py`](../samples/_probe/b2/build_library_v2.py) `BEZIER_DEFAULT`:

```python
ControlPoint1: (-0.3, -0.3)
ControlPoint2: ( 0.3,  0.3)
```

これは概ね Linear。よりカーブをつけるには ControlPoint を 0.5+ / -0.5- に振る。

---

## 7. cross-reference

| 参照先 | 用途 |
|-------|------|
| [`samples/_probe/b2/build_library_v2.py`](../samples/_probe/b2/build_library_v2.py) | builder 関数 (`e_repeat_move`, `e_random_move`, `anim_keyframes`, `BEZIER_DEFAULT`) |
| [`samples/_probe/b2/effect_full_samples.json`](../samples/_probe/b2/effect_full_samples.json) | effect 1 件分の完全 JSON 構造 |
| [`samples/_probe/b2/extract_effect_params.py`](../samples/_probe/b2/extract_effect_params.py) | `EffectsSamples_2026-04-15.ymmp` から新 effect の parameter を抽出 |
| [`samples/effect_catalog.json`](../samples/effect_catalog.json) | 全 111 effect の parameter list / community flag / category |
| [`samples/tachie_motion_map_library.json`](../samples/tachie_motion_map_library.json) | 24 emotion ラベルの実値 (本書の標準値の出典) |
| [`docs/MOTION_PRESET_LIBRARY_SPEC.md`](MOTION_PRESET_LIBRARY_SPEC.md) | emotion ラベル → atom 組み合わせの正本 |
| [`src/pipeline/motion_recipe.py`](../src/pipeline/motion_recipe.py) | `build-motion-recipes` 実装 |

---

## 8. 既知の制約・ハマり所

1. **community plugin 依存**: `FlipEffect` / `CameraShakeEffect` / `WaveEffect` / `BloomEffect` / `VignetteBlurEffect` / `TilingGroupItemsEffect` などは YukkuriMovieMaker.Plugin.Community 必須。配布案件では `is_community: false` で代替。
2. **Rotation route と RepeatRotateEffect の併用禁忌**: 同じ Z 軸を二重制御するため、どちらかに統一。
3. **flat parameter only と animation parameter の使い分け**: TachieItem 経由は flat で動くが、ImageItem / GroupItem 直書きは `Values` 配列の `Span > 0` でないと無アニメーション扱い ([build_library_v2.py docstring](../samples/_probe/b2/build_library_v2.py))。
4. **Span 0.0 は 「アニメ無し」**: route の `Span: 0.0` + `Values: [{"Value": X}]` は静的値とみなされる。アニメーションは `Span > 0` + `Values` 複数。
5. **Bezier Default は概ね Linear**: 既定の `(-0.3, -0.3)` & `(0.3, 0.3)` は微 ease。本気で曲線にしたいなら `(0.5, 0.0)` & `(0.5, 1.0)` などに変更。
6. **30fps 前提**: Length / frame は 30fps を想定。60fps プロジェクトでは値を 2 倍に。

---

## 9. 拡張ガイド (新 effect / 新 emotion 追加時)

新しい effect を本表に加えるとき:

1. [`effect_catalog.json`](../samples/effect_catalog.json) で `$type` と parameter list を確認
2. `EffectsSamples_2026-04-15.ymmp` で実物の値を確認 (`extract_effect_params.py` で抽出)
3. 1 つの emotion label で実値を試作 → YMM4 で visual acceptance
4. 採用なら本表 § 3 に行追加。`tachie_motion_map_library.json` の対応 entry も更新
5. `MOTION_PRESET_LIBRARY_SPEC.md § 3` に新 emotion ラベル行を append
6. 1 commit でセット (本表 + library JSON + spec table)

---

## 10. 変更履歴

- 2026-04-30: 初版。35 effect の canonical 値を [`tachie_motion_map_library.json`](../samples/tachie_motion_map_library.json) から実測抽出。Slice 2 として S5-motion-brief-prompt と同時 commit。
