# effect_catalog.json 運用メモ

**目的**: YMM4 v4.51.0.3 のエフェクト（VideoEffects）一覧を機械可読に保持し、`motion_map` / `tachie_motion_map` / `bg_anim_map` / `group_motion_map` などの registry にエフェクト指定を書くときの**ピックアップ元**として使う。

## ファイル構成

| パス | 役割 |
|------|------|
| `samples/EffectsSamples_2026-04-15.ymmp` | 抽出元 ymmp。9 カテゴリの GroupItem 内に 111 エフェクトを配置した見本 |
| `samples/effect_catalog.json` | 抽出済みカタログ。`effects.<name>` に `$type` / `is_community` / `category` / `parameters` |
| `scripts/extract_effect_catalog.py` | 再抽出スクリプト。`python scripts/extract_effect_catalog.py` で `samples/effect_catalog.json` を上書き |

## カテゴリ（`EffectsSamples` の GroupItem 順）

| # | category | 件数 | 典型用途 |
|---|---------|------|---------|
| 0 | `group_tiling` | 12 | タイル配置、複製、円環複製 |
| 1 | `transform_position` | — | 拡大縮小・位置・回転 |
| 2 | `in_out_animation` | 7 | フェード系の登場・退場 |
| 3 | `border_shadow_3d` | 8 | 縁取り・影・擬似 3D |
| 4 | `crop_key_mask` | 9 | クロップ・クロマキー・マスク |
| 5 | `color_blur_shader` | 40 | 色補正・ブラー・シェーダ |
| 6 | `camera` | 4 | カメラ追従・被写界深度 |
| 7 | `animation_glitch_audio` | 23 | 揺れ・グリッチ・音連動 |
| 8 | `group_control` | 0 (keyframes 49 / 154) | Group 全体のキーフレーム制御 |

## registry への書き方（例）

エフェクト 1 つを `video_effect` に書くとき、最低限 `$type` を `effect_catalog.json` からコピーする。`parameters` 一覧にあるキーは任意に上書きでき、書かないキーは YMM4 既定値。

```jsonc
// motion_map.json の一例
{
  "bounce_in": {
    "video_effect": {
      "$type": "YukkuriMovieMaker.Project.Effects.BounceEffect, YukkuriMovieMaker",
      "IsEnabled": true
    }
  }
}
```

`$type` を探すときは `effect_catalog.json` の `effects` を `name` で grep する。例:

```bash
# Fade 系を探す
jq '.effects | to_entries[] | select(.key | test("Fade"; "i")) | {name: .key, type: .value["$type"]}' samples/effect_catalog.json
```

## コミュニティエフェクトの扱い

`is_community: true` のエフェクト（例: `TilingGroupItemsEffect`, `LuminanceMaskEffect`）は **YukkuriMovieMaker.Plugin.Community プラグインの導入が前提**。registry で参照する場合、視聴環境にプラグインが入っていないと当該 ImageItem / TachieItem のロードで警告が出る。**配布・共有を意識する案件では `is_community: false` を優先**する。

## 既知の重複スキップ

抽出時にスキップされた重複 `$type`（EffectsSamples に複数配置されている）:

- `ChromaKeyEffect2`
- `RandomOpacityEffect`

カタログ上は 1 件のみ記録される。

## 更新手順

YMM4 のバージョン更新やコミュニティプラグイン追加でエフェクトが増えたとき:

1. YMM4 で `EffectsSamples_<date>.ymmp` を開き、カテゴリ GroupItem にエフェクトを追加して保存
2. `scripts/extract_effect_catalog.py <path_to_new_ymmp>` で `samples/effect_catalog.json` を再生成
3. `_meta.source` が新 ymmp を指すこと、`total_unique_effects` が増えたことを確認
4. 本メモの件数表を更新

## 関連

- [PRODUCTION_IR_CAPABILITY_MATRIX.md](../docs/PRODUCTION_IR_CAPABILITY_MATRIX.md) — `motion` / `bg_anim` / `group_motion` の書き込み経路
- [FEATURE_REGISTRY G-17](../docs/FEATURE_REGISTRY.md) — motion_map / bg_anim_map の書き込み実装
- [FEATURE_REGISTRY G-20](../docs/FEATURE_REGISTRY.md) — group_motion_map（X/Y/Zoom のみ。VideoEffects は別経路）
- [FEATURE_REGISTRY G-21 (proposed)](../docs/FEATURE_REGISTRY.md) — 茶番劇体テンプレ（外部素材 ImageItem + ゆっくり頭 TachieItem 重畳）で本カタログからエフェクト選定
