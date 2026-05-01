# Motion Calibration Guide — element threshold + scaling formula

> **位置づけ**: [MOTION_PRODUCTION_PIPELINE.md](MOTION_PRODUCTION_PIPELINE.md) **Phase 0 (Calibration)** の正本 doc。recipe build より上流で、element 単位の YMM4 内部挙動を観測値として固定する。recipe 構築は本書の値を引いて行う。
>
> **位置関係**: [`MOTION_RECIPE_LOOP_TIMING.md`](MOTION_RECIPE_LOOP_TIMING.md) は effect ごとの「論理範囲」、本書は YMM4 で実際に視認可能な「観測 threshold」を扱う。両者の差分は **論理範囲は仕様、観測 threshold は実装**。
>
> **更新タイミング**: 新 element / 新 effect / 新 anchor を導入したときのみ Phase 0 を再走し、本書を update。通常 recipe 量産では本書を引いて再走しない (Anti-Shortcut Rule R7)。

---

## 0. 状態 (2026-05-02)

**軌道修正中**。初回 calibration は threshold 観測ではなく、`KeyFrames` 同期漏れを発見する構造 smoke になった。特に B / C の animated pattern は `Values` 数に対して GroupItem `KeyFrames.Frames` / `Count` が更新されず、中間点が 1 点に潰れていたため、threshold としては無効。

有効な観測は E face swap、D の一部 effect coupling、F anchor 禁忌のみ。B / C は修正後の `_tmp/g26/calibration/B_keyframes_smoke.ymmp` と `_tmp/g26/calibration/C_bounce_smoke.ymmp` で最小再確認する。

---

## 1. Element list (calibration scope)

6 系統で押さえる。各系統は独立に calibrate。grid 全網羅はしない (テスト過剰回避)。

### A. GroupItem static props

キャラを画面上のどこに、どの大きさ・どの傾きで出すかの基準値。

| 軸 | 要所値 (key points) | 何を確認するか |
|----|------|---------|
| X position | -200 / -100 / 0 / +100 / +200 | 画面横の出現位置。-200 で左端、0 で中央、+200 で右端 |
| Y position | 250 (上) / 462 (中、既定) / 700 (下) | 縦の出現位置。既定 462.5 が床に立つ位置 |
| Zoom | 80 / 103.8 (既定) / 130 / 170 | キャラのサイズ感。103.8 で標準体格 |
| Rotation static | -30° / -10° / -5° / 0 / +5° / +10° | 静的な傾き。閾値: 何度から「傾いている」と読めるか |
| Opacity | 100 / 75 / 50 / 25 | 透明度。sad / defocus 系で使う |

### B. Animated Rotation patterns

中間 keyframe / hold pattern が YMM4 でどう描画されるか。

| pattern | Length | 期待見え方 |
|---------|--------|-----------|
| `[0, -10, 0]` 単純 | 30 / 60 / 120 frame | 1 回の頷き / 首振り |
| `[0, -10, -10, 0]` hold-then-return | 60 / 120 frame | 傾けて持続 → 戻り。中間の `-10, -10` が hold として認識されるか |
| `[0, -5, -5, -5, 0]` long-hold | 60 / 120 frame | 傾けて長く持続 → 戻り。3 つの `-5` が冗長になり単純揺れに退化しないか |
| `[0, -7, 0, -5, 0]` double | 66 frame | 2 段の頷き。中間頂点 `0` が認識されるか (Slice 1 nod_double で問題化) |
| `[0, 0, -10, 0]` delayed | 90 frame | 前半静止 → 後半 nod。前半の `0, 0` が静止区間として認識されるか |

### C. Animated Y bounce patterns

ジャンプの振幅・段数の閾値。

| pattern | 振幅 | 期待見え方 |
|---------|------|-----------|
| `[Y, Y-30, Y]` 単発 | 30 | jump_small 想定 |
| `[Y, Y-90, Y]` 大振幅 | 90 | jump_high 想定 |
| `[Y, Y-150, Y]` 過剰 | 150 | やりすぎラインの確認 |
| `[Y, Y-30, Y+10, Y-30, Y]` 二段 | 30 | 2 段 bounce が 2 段に見えるか |
| `[Y, Y-45, Y+5, Y-35, Y]` 二段減衰 | 45→35 | excited_double_jump 想定 |

### D. Effect intensity scaling

各 effect で「弱い・標準・強い」の体感差が出る parameter 値。

| effect | 軸 | 要所値 |
|--------|-----|--------|
| JumpEffect | Stretch | 10 / 25 (既定) / 50 |
| JumpEffect | JumpHeight | 50 / 100 (既定) / 200 |
| CrashEffect | Size | 30 / 50 (既定) / 80 |
| ChromaticAberrationEffect | Strength | 5 / 15 / 30 |
| GaussianBlurEffect | Blur | 2 / 5 / 10 |
| RepeatRotateEffect | Span (秒) | 0.3 / 0.5 / 1.0 |
| RandomMoveEffect | X amplitude | 5 / 15 / 30 |

### E. Face swap

6 表情を順に出して、それぞれの emotion 表現として読めるかを確認。

| face_id | reimu file | 想定 emotion |
|---------|-----------|--------------|
| easy | `reimu_easy.png` | neutral / agreement |
| shocked | `reimu_shocked.png` | surprise (strong) |
| panic | `reimu_panic.png` | panic / fear |
| surprised | `reimu_surprised.png` | surprise (mild) |
| anger | `reimu_anger.png` | anger |
| shobon | `reimu_shobon.png` | sadness |

### F. Anchor (CenterPointEffect)

Rotation 系 motion における pivot の効き方。

| mode | Vertical | Horizontal | X / Y | 期待 |
|------|----------|-----------|-------|------|
| 頭部 pivot | Bottom | Custom | X≈525, Y≈137 | 首振り (nod 系)、頭部周辺で回転 |
| 中央 pivot | Center | Center | 0, 0 | 体の中心で回転 (= 体ごと傾き) |
| 不在 | (effect なし) | — | — | 体の左下基準で回転 (YMM4 default) |

---

## 2. 観測 threshold (Step 5 で user 確認後に記入)

各系統について、user が YMM4 で確認した結果を記録する。空欄は未観測。

### A. GroupItem static (観測値、Step 5 で記入)

A1 / A2 は「数値が変更できること」の既知再確認に寄ったため、recipe threshold の主根拠としては扱わない。画面位置・占有率は production placement / seed / template-source 文脈で別途見る。

| 軸 | 値 | 観測 | recipe で使う threshold |
|----|----|-----|------------------------|
| X | -200 | (未観測) |  |
| X | 0 | (未観測) |  |
| X | +200 | (未観測) |  |
| Y | 250 | (未観測) |  |
| Y | 462 | (未観測) | 既定 |
| Y | 700 | (未観測) |  |
| Zoom | 80 | (未観測) |  |
| Zoom | 103.8 | (未観測) | 既定 |
| Zoom | 170 | (未観測) |  |
| Rotation static | -3° | (未観測) | 不可視ライン? |
| Rotation static | -5° | (未観測) | 微傾き? |
| Rotation static | -10° | (未観測) | 明確? |
| Rotation static | -20° | (未観測) | 過剰? |
| Opacity | 75 | (未観測) | sad の弱透明 |
| Opacity | 50 | (未観測) | defocus |

### B. Animated Rotation patterns (観測値、Step 5 で記入)

初回 `B_rotation_patterns.ymmp` は **invalid due to KeyFrames bug**。`Values` が 5 個でも `KeyFrames={Frames:[14], Count:1}` のままで、中間点が同一frameへ潰れていた。下表は threshold ではなく、修正後 smoke で再観測する候補。

| pattern | Length | 観測 | 用途 / threshold |
|---------|--------|------|-----------------|
| `[0, -10, 0]` | 30 | invalid: old file had stale KeyFrames | 修正後 smoke で再確認 |
| `[0, -10, 0]` | 60 | invalid: old file had stale KeyFrames | 修正後 smoke で再確認 |
| `[0, -10, -10, 0]` | 60 | invalid: old file had stale KeyFrames | 修正後 smoke で再確認 |
| `[0, -5, -5, -5, 0]` | 80 | invalid: old file had stale KeyFrames | 修正後 smoke で再確認 |
| `[0, -7, 0, -5, 0]` | 66 | invalid: old file had stale KeyFrames | 修正後 smoke で再確認 |
| `[0, 0, -10, 0]` | 90 | invalid: old file had stale KeyFrames | 修正後 smoke で再確認 |

修正後 smoke:

| file | pattern | Length | KeyFrames | 観測 |
|------|---------|--------|-----------|------|
| `B_keyframes_smoke.ymmp` | 3pt simple | 60 | `[30]` | user 確認待ち |
| `B_keyframes_smoke.ymmp` | 5pt double | 60 | `[15, 30, 45]` | user 確認待ち |
| `B_keyframes_smoke.ymmp` | 7pt hold double | 60 | `[10, 20, 30, 40, 50]` | user 確認待ち |

### C. Y bounce patterns (観測値、Step 5 で記入)

初回 `C_y_bounce_patterns.ymmp` も **invalid due to KeyFrames bug**。B と同じく、複数値 Y route の中間点が 1 点に潰れていた。修正後 smoke だけを手動確認対象にする。

| pattern | 振幅 | 観測 | threshold |
|---------|------|------|----------|
| `[Y, Y-30, Y]` | 30 | invalid: old file had stale KeyFrames | 修正後 smoke で再確認 |
| `[Y, Y-90, Y]` | 90 | invalid: old file had stale KeyFrames | 修正後 smoke で再確認 |
| `[Y, Y-150, Y]` | 150 | invalid: old file had stale KeyFrames | 修正後 smoke で再確認 |
| `[Y, Y-30, Y+10, Y-30, Y]` | 30 | invalid: old file had stale KeyFrames | 修正後 smoke で再確認 |
| `[Y, Y-45, Y+5, Y-35, Y]` | 45→35 | invalid: old file had stale KeyFrames | 修正後 smoke で再確認 |

修正後 smoke:

| file | pattern | Length | KeyFrames | 観測 |
|------|---------|--------|-----------|------|
| `C_bounce_smoke.ymmp` | 3pt single | 60 | `[30]` | user 確認待ち |
| `C_bounce_smoke.ymmp` | 5pt double | 60 | `[15, 30, 45]` | user 確認待ち |
| `C_bounce_smoke.ymmp` | 7pt triple decay | 60 | `[10, 20, 30, 40, 50]` | user 確認待ち |

### D. Effect intensity (観測値、Step 5 で記入)

| effect | parameter 値 | 観測 | intensity scaling |
|--------|-------------|------|-------------------|
| JumpEffect Stretch | 10 | Height 側にロックされ、Stretch 単独差分として読みにくい | Stretch 単独 override 禁止 |
| JumpEffect Stretch | 25 | Height 側にロックされ、Stretch 単独差分として読みにくい | Stretch 単独 override 禁止 |
| JumpEffect Stretch | 50 | Height 側にロックされ、Stretch 単独差分として読みにくい | Stretch 単独 override 禁止 |
| CrashEffect Size | 30 | 細かく重く見える | 小さすぎ注意 |
| CrashEffect Size | 80 | 大きめで良い。細かさより軽く見える | panic/crash 標準候補 |
| ChromaticAberration Strength | 5 | (未観測) | 弱すぎるライン? |
| ChromaticAberration Strength | 15 | (未観測) |  |
| ChromaticAberration Strength | 30 | (未観測) | 過剰? |
| GaussianBlur Blur | 2 | (未観測) |  |
| GaussianBlur Blur | 5 | 顔が微妙に見える | 弱defocus候補 |
| GaussianBlur Blur | 10 | 顔が分からなくなる | 強すぎ / 顔演技と併用注意 |
| RepeatRotate Span | 0.3 | (未観測) |  |
| RepeatRotate Span | 1.0 | (未観測) |  |

### E. Face swap (観測値、Step 5 で記入)

| face_id | 観測 | 採用可否 |
|---------|------|---------|
| easy | 正常表示 | neutral / agreement 系で採用可 |
| shocked | 正常表示 | surprise 系で採用可 |
| panic | 正常表示 | panic 系で採用可 |
| surprised | 正常表示 | surprise の弱い形で採用可 |
| anger | 正常表示 | anger 系で採用可 |
| shobon | 正常表示 | sadness 系で採用可 |

### F. Anchor mode (観測値、Step 5 で記入)

| mode | Rotation -10° の見え方 | 推奨用途 |
|------|---------------------|---------|
| Bottom + Custom (頭部) | 既存 `nod.ymmp` / `delivery_nod_v1` の ground truth。実用基準 | nod / lean / tilt の既定 |
| Center | 画面外に出て上半身のみになる。位置補正なしでは不可 | 禁忌、またはX/Y補正実装後のみ |
| 不在 | 画面外に出る。回転中心が大きく左側にあり、頷き時に上昇して見える | 禁忌 |

---

## 3. Calibration .ymmp 出力先

Step 4 で生成される calibration ファイル群:

```
_tmp/g26/calibration/
  A1_static_position.ymmp        # X / Y / Zoom 段階
  A2_static_rotation_opacity.ymmp # Rotation static + Opacity 段階
  B_rotation_patterns.ymmp        # 5 keyframe pattern × 3 Length
  C_y_bounce_patterns.ymmp        # 5 Y pattern
  D_effect_intensity.ymmp         # 6 effect × 3 値
  E_face_swap.ymmp                # 5 face (easy 除く)
  F_anchor_modes.ymmp             # 3 anchor mode × Rotation -10° 動
  B_keyframes_smoke.ymmp          # KeyFrames修正後の Rotation 3/5/7pt smoke
  C_bounce_smoke.ymmp             # KeyFrames修正後の Y bounce 3/5/7pt smoke
  STRUCTURAL_SMOKE_README.md      # B/C smoke の確認ポイント
  README.md                       # 各 .ymmp の frame 配置と観測ポイント
```

各 .ymmp は `samples/canonical.ymmp` を seed、`samples/templates/skit_group/delivery_v1_templates.ymmp` を template-source とし、要所値を frame 順に並べる。`scripts/build_calibration_ymmp.py` で生成。

---

## 4. 利用フロー

### recipe 構築時

1. brief を書く前に本書の § 2 観測 threshold を読む
2. 該当 element の threshold を引く (例: 「nod_clear → Rotation `[0, -10, 0]` Length 60、観測上明確に頷きと読める」)
3. recipe の route / effect / face_id / anchor_template_source を threshold 値に揃える
4. brief / preset を書く

### 新 element 追加時 (Phase 0 再走)

1. `scripts/build_calibration_ymmp.py` を拡張して新 element 用 .ymmp を build
2. user に YMM4 で確認してもらい observation を取る
3. 本書 § 2 に新行を追加、threshold を記入
4. その後の recipe 構築から新 element を使える

---

## 5. 変更履歴

- 2026-05-01: 初版作成 (Step 3、observation 欄は空)。Step 5 で user 確認後に observation を埋める予定。
