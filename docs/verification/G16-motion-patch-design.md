# G-16 `motion` patch（設計メモ）

> ステータス: **done**（[FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md)）。実装: `patch_ymmp` + `--motion-map` + `validate-ir`。

## 目的

IR の `motion`（[PRODUCTION_IR_SPEC.md](../PRODUCTION_IR_SPEC.md) §3.6）を `TachieItem.VideoEffects` 等の **G-12 観測経路**にエンコードする。

## 観測済み

- `motion` → `TachieItem.VideoEffects`（[G12-timeline-route-measurement.md](G12-timeline-route-measurement.md)）

## 課題（残）

- 効果プリセットは **型名・パラメータ**が YMM4 プラグイン依存 → repo-local **`motion_map.json`**（ラベル → 効果オブジェクトの配列）で供給する。
- `pop_in` / `shake_*` 等の **1 発話あたりの長さ**と VoiceItem の `Length` の整合は **v1 未対応**（手動または将来 FEATURE）。

## 実装済み

1. `measure-timeline-routes` + G-12 契約（既存）。
2. **`motion_map.json`**: トップレベルまたは `"motions"` セクションで、ラベル → `VideoEffects` 配列。CLI: `src.cli.main` の `_load_motion_map`。
3. **`validate-ir`**: `MOTION_UNKNOWN_LABEL`（仕様外語彙）、`--motion-map` 指定時は `MOTION_MAP_UNKNOWN_LABEL`（台帳に無い非 `none` ラベル）。
4. **`_apply_motion_to_tachie_items`**（`ymmp_patch.py`）: carry-forward 解決済み IR を順に処理し、話者の `TachieItem` に書き込む。

## 制約（v1）

- Phase2 で **発話アンカー（`row_range` 優先 / `index` fallback）単位の区間分割**を実装。
- 連続する同一 `motion` は **区間結合**し、不要なアイテム増加を抑制する。
- 複数 `TachieItem` を同一キャラが持つ特殊ケースは、当面 v1 相当（後勝ち）での適用を維持する。
- **`motion == none`** で話者に `TachieItem` が無い場合は **何もしない**（クリア対象がないため警告なし）。**非 `none`** で `TachieItem` が無い場合は `MOTION_NO_TACHIE_ITEM`（fatal）。

## 実装順（当初案・対応状況）

1. corpus 1 本で `measure-timeline-routes` + 手動で効果を付けたサンプル ymmp を固定する。 — G-12 済
2. `motion_map.json` + `validate-ir`（unknown / registry gap）。 — 済
3. `_apply_motion_to_tachie_items` を `patch_ymmp` に追加。 — 済

## Phase 2（方式比較スパイク）

### 比較対象

- **方式A: TachieItem 分割方式（採用）**
  - `row_start`/`row_end`（なければ `index`）から発話区間を解決し、話者の `TachieItem` を区間で分割して `VideoEffects` を割り当てる。
- **方式B: 単一 TachieItem 維持 + 別経路併用**
  - `TachieItem` は分割せず、別経路で発話単位の見え方を表現する。

### 評価結果

- **再現性**: 方式Aが高い（発話単位の意図を直接表現）。
- **安全性/保守性**: 方式Aが既存 `motion -> TachieItem.VideoEffects` 契約を維持しやすい。
- **拡張性**: 方式Bは経路分散により将来の障害解析・仕様追跡コストが増える。

### 採用方針（Phase 2）

- **方式Aを採用**。
- 連続する同一 `motion` 区間は結合し、アイテム増加を最小化する。
- `row_range` 優先、未指定時は `index` fallback を維持する。
