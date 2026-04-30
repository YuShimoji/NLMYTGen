# Motion Production Pipeline — G-26 演出制作運用正本

> **Position**: NLMYTGen で「演出 (motion / 視覚 effect) サンプル」を制作する全工程の正本ワークフロー。creative slice の入口。
>
> **Read order**: 演出 / motion / 視覚 effect 制作タスクでは、`AGENTS.md` → `REPO_LOCAL_RULES.md` → `runtime-state.md` の minimum anchor に加えて **本ファイル** + [`MOTION_PRESET_LIBRARY_SPEC.md`](MOTION_PRESET_LIBRARY_SPEC.md) + [`samples/effect_catalog.json`](../samples/effect_catalog.json) も必読。

---

## 0. なぜこの doc が必要か

過去セッションで繰り返された失敗パターン:

- 既存サンプル (nod / surprise_oneshot / exit_left) の Rotation/Y/Zoom 値を弄っただけで「新 motion」と称する
- 用意済みの 111 effect catalog / 6 表情 / 23 emotion ラベルを参照せずにゼロから始める
- recipe を別 frame に並べただけのものを「合成」と称する
- evidence 不足を理由に creative composition 自体を拒否する循環論証
- 「感覚」「だいたい」でパラメータを置き、再現性が無い

これは資産ではなく**配線**の問題。本 doc は配線を埋める。

---

## 1. Anti-Shortcut Rules (READ FIRST)

以下に違反する作業は accept しない。

1. **Catalog inspection skip 禁止**: [`samples/effect_catalog.json`](../samples/effect_catalog.json) を確認せず Rotation/Y/Zoom などの value だけで motion を作るのは「組み合わせ短絡」として禁止。Phase A の motion brief を経由していない creative output は accept しない。

2. **既存 primitive 値の mutation 単独で「新 motion」を称することの禁止**: `nod` / `jump` / `exit_left` の Values を弄っただけのものは novel motion ではない。Phase B で **新しい effect atom が選択されている**か、**既存 label の意図的 `_light` / `_heavy` 派生**であることが必要。

3. **「evidence-driven」を不作為のアリバイにすることの禁止**: 「2 motion 連続例の観測がない」「tilt 単独サンプルがない」は Phase D の build 試作を断る理由にしない。Build 試作は evidence の入口であり、観測待ちで止めるのは循環論証。Evidence gate は **contract 昇格条件** であって **creation ban ではない**。

4. **「未依頼の機能追加禁止」の方向誤適用の禁止**: 用意済み資産（[`effect_catalog.json`](../samples/effect_catalog.json) / `reimu_*.png` / [`build_library_v2.py`](../samples/_probe/b2/build_library_v2.py) / [`MOTION_PRESET_LIBRARY_SPEC`](MOTION_PRESET_LIBRARY_SPEC.md) 等）を使うことは「未依頼の追加」ではない。それらは登録・承認済み。Phase A の brief があれば motion 生成も「未依頼」ではない。

5. **Rearranging existing samples を progress と称することの禁止**: 既存 motion を別 frame に並べたものは composition ではない。Phase A の motion brief が無いビルドは progress として記録しない。

6. **「感覚」「だいたい」でのパラメータ決定禁止**: Phase C は `MOTION_RECIPE_LOOP_TIMING.md`（予定、Slice 2）の range 表 + [`build_library_v2.py`](../samples/_probe/b2/build_library_v2.py) の値 + [`samples/_probe/b2/effect_full_samples.json`](../samples/_probe/b2/effect_full_samples.json) を canonical reference として使う。表に該当値が無い effect は [`extract_effect_params.py`](../samples/_probe/b2/extract_effect_params.py) で `EffectsSamples_2026-04-15.ymmp` から抽出する。

---

## 2. 5-Phase Pipeline 全体像

```
Phase A:  Motion Brief (creative ideation)
            input:  シーン / utterance / 望む情緒
            output: brief JSON   (samples/recipe_briefs/<id>.json)
              ↓
Phase B:  Catalog Inspection (mechanical)
            input:  brief + effect_catalog.json + MOTION_PRESET_LIBRARY_SPEC
            output: effect shortlist (build-motion-recipes 内部処理)
              ↓
Phase C:  Recipe Assembly (loop / timing 逆算)
            input:  shortlist + concrete effect samples + motion library
            output: recipe (build-motion-recipes 内部処理)
              ↓
Phase D:  Build Sample (.ymmp)
            input:  recipe + seed .ymmp + 表情 asset
            output: review .ymmp + readback JSON + manifest MD
              ↓
Phase E:  Visual Acceptance & Library Promotion
            input:  user YMM4 検証
            output: tachie_motion_map_library.json 追記 + registry 更新
```

**Phase D で初めて `.ymmp` を作る**。Phase A〜C を飛ばして D に行くのは Anti-shortcut Rule #1 違反。

---

## 3. Phase A: Motion Brief (creative ideation)

### 現状 (2026-04-30): manual brief JSON authoring

正本 brief: [`samples/recipe_briefs/g26_motion_recipe_brief.v1.json`](../samples/recipe_briefs/g26_motion_recipe_brief.v1.json)

各 recipe entry の schema:

```jsonc
{
  "goal_id": "nod_clear",
  "motion_goal": "Readable nod for agreement, understanding, or confirmation.",
  "emotion": "agreement",
  "intensity": "medium",      // light | medium | strong
  "duration_frames": 48,
  "reset_policy": "returns_to_neutral",  // returns_to_neutral | terminal | hold
  "forbidden_patterns": ["body-face drift", "too subtle"]
}
```

新しい motion goal を追加する場合は brief JSON に entry を append する。

### GUI LLM 経由: S-5 motion brief prompt

[`docs/S5-motion-brief-prompt.md`](S5-motion-brief-prompt.md) を Custom GPT / Claude Project / Cowork の instructions に投入し、自然言語のシーン記述から brief JSON entry を生成する。出力された entry は [`samples/recipe_briefs/g26_motion_recipe_brief.v1.json`](../samples/recipe_briefs/g26_motion_recipe_brief.v1.json) の `recipes` 配列に追記する。

prompt body には [`MOTION_PRESET_LIBRARY_SPEC § 3`](MOTION_PRESET_LIBRARY_SPEC.md#3-感情ラベル定義テーブル) の 23 ラベルと 8 emotion カテゴリ早見表を埋め込み、LLM が **既存ラベルへの fit を最初に試みる**ことを強制している。

### Phase A novel goal_id の扱い (Slice 4 以降の運用)

novel goal_id (既存 14 preset で fit しないもの) には 2 経路がある:

#### 経路 1: brief 内完全定義 (推奨、Slice 4 で実装済)

`_resolve_brief_recipes` は preset 未登録の goal_id でも、brief entry に必須キー (`motion_goal` / `emotion` / `intensity` / `duration_frames` / `reset_policy` / `forbidden_patterns` / `effect_candidates`) と route フィールド (`rotation_values` / `y_delta_values` / `zoom_delta_values`) / `effect_names` を含めば accept する。コード変更不要。

手順:

1. S-5 prompt が brief entry を novel goal 用に出力 (route + effect 含む完全形)
2. brief 配列に追記
3. `build-motion-recipes` 実行 → review .ymmp 生成
4. YMM4 で visual acceptance (Phase E)
5. pass なら Phase E の library promotion で `MOTION_PRESET_LIBRARY_SPEC § 3` に追加

#### 経路 2: preset 化 (再利用が見込まれる goal のみ)

複数案件で繰り返し使う goal は、visual acceptance pass 後に [`src/pipeline/motion_recipe.py`](../src/pipeline/motion_recipe.py) `DEFAULT_RECIPE_PRESETS` に preset 化することで brief を簡潔化できる (brief 側は `goal_id` だけで参照可能)。

手順:

1. 経路 1 で brief 内完全定義 → visual acceptance pass
2. brief 内 fields をそのまま `DEFAULT_RECIPE_PRESETS` の新 entry にコピー
3. brief 側を `goal_id` 参照だけに圧縮 (overrides は不要)
4. `uv run pytest tests/test_motion_recipe.py -q` で regression なし確認

経路 2 は **library promotion の選択工程**であって必須ではない。一度きりの goal は brief 内に持ち回しても CLI は問題なく動く。

---

## 4. Phase B+C+D: `build-motion-recipes` CLI

実装済み (2026-04-30): [`src/pipeline/motion_recipe.py`](../src/pipeline/motion_recipe.py) + [`src/cli/main.py`](../src/cli/main.py) `build-motion-recipes` subcommand.

### コマンド

```powershell
uv run python -m src.cli.main build-motion-recipes [--brief BRIEF.json] [--out-ymmp OUT.ymmp] [--out-readback READBACK.json] [--out-manifest MANIFEST.md]
```

### 既定入力 (すべて --flag で上書き可)

| 引数 | 既定値 | 役割 |
|------|-------|------|
| `--brief` | `samples/recipe_briefs/g26_motion_recipe_brief.v1.json` | Phase A 出力 |
| `--seed` | `samples/canonical.ymmp` | YMM4-saved full project canvas (clone 元) |
| `--template-source` | `samples/templates/skit_group/delivery_v1_templates.ymmp` | GroupItem / ImageItem actor template |
| `--effect-catalog` | `samples/effect_catalog.json` | 111 effect の機械可読カタログ |
| `--effect-samples` | `samples/_probe/b2/effect_full_samples.json` | 具体的 effect parameter 実値 |
| `--motion-library` | `samples/tachie_motion_map_library.json` | 23 emotion ラベル + atom 組み合わせ |
| `--corpus-ymmp` | `_tmp/g26/composition/演出_palette_v2.ymmp` | optional. 候補 corpus (existing で accept にはならない) |

### 既定出力

```
_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1.ymmp        # YMM4 で開く review artifact
_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1_readback.json
_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1_manifest.md  # frame / goal / route の人間可読 index
```

### v1 で含まれている 12 recipe

`nod_subtle` / `nod_clear` / `nod_double` / `jump_small` / `jump_high` / `jump_emphasis` / `panic_crash` / `shocked_jump` / `surprised_chromatic` / `anger_outburst` / `shobon_droop` / `lean_curious`

### 制約

- `.ymmp` zero-generation はしない。既存 YMM4-saved canvas を seed とし、既存 GroupItem / ImageItem template をコピーして編集する
- 各 sample は `recipe:<goal_id>` Remark を持つ
- 各 recipe は `proposed` として出力。YMM4 visual acceptance なしに `accepted_candidate` へ昇格しない
- chain / compatibility は YMM4 上で読めたものだけ `compatibility_evidence` に昇格できる
- Python preview/rendering、画像生成、未知 effect type 合成、G-24 production placement 接続はしない

### 検証

```powershell
uv run pytest tests/test_motion_recipe.py -q
```

正本: [`docs/verification/G26-motion-recipe-pipeline-2026-04-30.md`](verification/G26-motion-recipe-pipeline-2026-04-30.md)

---

## 5. Phase E: Visual Acceptance & Library Promotion

### YMM4 検証

ユーザーが `_tmp/g26/recipe_pipeline/<id>.ymmp` を YMM4 で開き、各 recipe を以下 8 区分で判定:

| classification | 意味 | 次手 |
|---------------|------|------|
| `pass` | 演出として使える | library promotion へ |
| `wrong motion` | 意図と違う動き | brief の `motion_goal` 再記述 → Phase A 戻り |
| `body-face drift` | 顔と体がずれる | brief の `forbidden_patterns` を強化 + recipe 構造再設計 |
| `screen spacing` | 画面位置がおかしい | seed / template-source の取り違え疑い |
| `too subtle` | 動きが小さすぎ | intensity を `light` → `medium` / `strong` に上げて再 build |
| `too strong` | 動きが大きすぎ | intensity を `strong` → `medium` / `light` に下げて再 build |
| `openability` | YMM4 で開けない | readback JSON の openability 失敗箇所を修正 |
| `asset path` | 素材パスが切れている | brief / seed / template-source のパス整合 |

### Library promotion (pass 時)

1. `accepted_candidate` recipe を [`samples/tachie_motion_map_library.json`](../samples/tachie_motion_map_library.json) に追記
2. [`MOTION_PRESET_LIBRARY_SPEC.md § 3`](MOTION_PRESET_LIBRARY_SPEC.md#3-感情ラベル定義テーブル) のラベル表に新規ラベル行を append
3. [`FEATURE_REGISTRY.md`](FEATURE_REGISTRY.md) G-26 contract status 更新
4. chain recipe が pass した場合、`compatible_after` / `forbidden_after` の対応 entry を contract に追加
5. 採用された recipe は brief から `proposed` → `accepted_candidate` に status 遷移

### Reject / Adjust

- adjust → recipe.json の parameter 修正のみで Phase D に再投入
- reject → `_tmp/` で破棄、Phase A に戻って brief を見直す。録らない（progress として記録しない）

---

## 6. Reuse Map (既存資産正本)

| ファイル | 役割 | 本 pipeline での扱い |
|---------|------|------------------|
| [`samples/effect_catalog.json`](../samples/effect_catalog.json) | 111 effect の機械可読カタログ (`$type` + parameters + `is_community`) | Phase B input |
| [`samples/EffectsSamples_2026-04-15.ymmp`](../samples/EffectsSamples_2026-04-15.ymmp) | 9 カテゴリ × 111 effect 元 .ymmp | パラメータ実値 reference |
| [`samples/_probe/b2/effect_full_samples.json`](../samples/_probe/b2/effect_full_samples.json) | concrete effect samples (full JSON 構造) | Phase D effect 注入元 |
| [`samples/_probe/b2/build_library_v2.py`](../samples/_probe/b2/build_library_v2.py) | 24 motion を effect chain + animated parameter で生成する builder 関数群 | `motion_recipe.py` に取り込み済み |
| [`samples/_probe/b2/extract_effect_params.py`](../samples/_probe/b2/extract_effect_params.py) | effect parameter scanner | Slice 2 loop/timing 表生成補助 |
| [`samples/_probe/b2/dump_effect_full.py`](../samples/_probe/b2/dump_effect_full.py) | effect 1 件分の完全 JSON 抽出 | catalog 拡張時に再走 |
| [`samples/EFFECT_CATALOG_USAGE.md`](../samples/EFFECT_CATALOG_USAGE.md) | catalog 運用メモ | Phase B 手順書 |
| [`docs/MOTION_PRESET_LIBRARY_SPEC.md`](MOTION_PRESET_LIBRARY_SPEC.md) | **23 emotion ラベル × atom 組み合わせ** + 強度 _light/_heavy | data spec。本 pipeline はこれを参照 |
| [`samples/tachie_motion_map_library.json`](../samples/tachie_motion_map_library.json) | spec の 24 motion を生成済み JSON | Phase B+C input |
| [`docs/VISUAL_EFFECT_SELECTION_GUIDE.md`](VISUAL_EFFECT_SELECTION_GUIDE.md) | 4 類 × 3 ルート、用途別 effect 推奨 | Phase A reference |
| [`docs/STEP3_YMM4_TEMPLATE_CHECKLIST.md`](STEP3_YMM4_TEMPLATE_CHECKLIST.md) | 5 template の effect 初期値 checklist | Phase C parameter 初期値 |
| [`docs/S6-production-memo-prompt.md`](S6-production-memo-prompt.md) | IR ideation prompt (v4) | 将来 S-5 prompt の構造テンプレ |
| [`docs/PRODUCTION_IR_SPEC.md`](PRODUCTION_IR_SPEC.md) | motion vocabulary | Phase A の semantic 整合 |
| [`samples/characterAnimSample/reimu_*.png`](../samples/characterAnimSample/) | 6 種表情 (easy / shocked / panic / surprised / anger / shobon) | Phase D で face 切替 |
| [`samples/canonical.ymmp`](../samples/canonical.ymmp) / [`samples/_probe/g24/real_estate_dx_csv_import_base.ymmp`](../samples/_probe/g24/real_estate_dx_csv_import_base.ymmp) | YMM4-saved seed | Phase D clone 元 |

---

## 7. Loop / Timing Reference

正本: [`docs/MOTION_RECIPE_LOOP_TIMING.md`](MOTION_RECIPE_LOOP_TIMING.md)

35 effect (主要) について以下を表化:

- Loop type 5 分類 (single-shot / continuous-repeat / continuous-shake / in_out / sustained)
- Duration / Timing controls 早見表 (Length / Span / Period / EffectTimeSeconds 等)
- Effect ごと canonical 値 (intensity 別、`tachie_motion_map_library.json` から実測)
- Intensity scaling formula (`light` / `medium` / `strong` の換算則)
- Composition rules (複数 effect 同時適用時の timing 整合)
- AnimationType / EasingType / Bezier 補足
- 既知の制約 (community plugin 依存、Rotation 二重制御禁忌など)

Phase C で recipe parameters を決める際は本表の標準値を出発点にし、brief の `intensity` で scaling する。表に該当 effect が無いときは `samples/_probe/b2/extract_effect_params.py` で `EffectsSamples_2026-04-15.ymmp` から抽出する。

---

## 8. NAV.md からの導線

[`docs/NAV.md`](NAV.md) §1 の minimum anchor は AGENTS.md → REPO_LOCAL_RULES.md → runtime-state.md で「ここで止める」。creative slice (motion / 演出 / 視覚 effect 制作) を担当するエージェントは、§1 に加えて以下を必読:

- 本ファイル `MOTION_PRODUCTION_PIPELINE.md` (workflow 正本)
- `MOTION_PRESET_LIBRARY_SPEC.md` (emotion → atom data spec)
- `samples/effect_catalog.json` (111 effect カタログ)

これらを読まずに motion 制作を試みること自体が **Anti-Shortcut Rule #1 / #4 違反**。

---

## 9. Out of Scope (本 pipeline では扱わない)

- G-24 production placement への接続 (pipeline は sandbox で完結。production への流入は別 slice で評価)
- `tilt` 単独 primitive の自動生成 (Phase A で brief に `tilt_*` を含めることは可能だが、独立観測としての contract 昇格は visual acceptance 経由)
- `compatible_after` / `forbidden_after` の自動学習 (Phase E で acceptance pair が積まれたら別タスクで集計)
- 全 111 effect の loop/timing 表化 (Slice 2 では主要 ~30 effect のみ)
- HoloSync 側ファイルへの影響 (完全分離を維持)

---

## 10. 変更履歴

- 2026-04-30: 初版。`build-motion-recipes` CLI 実装と recipe brief schema を spine として 5-phase pipeline を正本化。Anti-Shortcut Rules を明記し、過去の失敗パターン (catalog skip / value mutation を novel と称する / evidence ban の循環論証) を構造的に防ぐ。Slice 1 として配線 (NAV.md / runtime-state.md / MOTION_PRESET_LIBRARY_SPEC header) と同時に commit。
