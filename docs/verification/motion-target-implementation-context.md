# motion_target 実装 + G-24 茶番劇テンプレート方針 コンテキストまとめ

> 作成日: 2026-04-17
> 対象: NLMYTGen / 背景演出レイヤーへの VideoEffects 適用経路 + 茶番劇演者のアーキテクチャ整理

---

## 1. 問題の背景

### 1-a. ユーザーの意図

haitatsuin (配達員) 動画で、**発話タイミングに合わせて配達員のイラスト（背景レイヤー）をジャンプ・揺れ等で動かしたい**。解説役の立ち絵（霊夢・魔理沙の TachieItem）は動かさない。

### 1-b. 変更前の混同の構造

| 層 | 変更前のコード | ユーザーの意図 |
|----|---------------|---------------|
| motion IR フィールド | `_apply_motion_to_tachie_items()` で **speaker の TachieItem** の VideoEffects に適用 | **背景レイヤーの配達員の絵** (ImageItem) に適用したい |
| タイミング指定 | speaker の VoiceItem をアンカーにして speaker の立ち絵を分割 | VoiceItem はタイミングアンカーとしてのみ使い、適用先は別レイヤー |
| テスト IR | `speaker: "ゆっくり霊夢赤縁"` + `motion: "surprise_jump"` → **霊夢がジャンプ** | 霊夢は解説役で動かない。**配達員の絵がジャンプすべき** |

### 1-c. haitatsuin ymmp レイヤー構成

```
Layer 11: ImageItem x2 -- reimu_easy.png (霊夢イラスト)
Layer 10: ImageItem x2 -- Gemini_Generated_Image_kfez... (配達員イラスト) <- 動かしたい対象
Layer  9: GroupItem x1 -- グループ
Layer  4: TachieItem x1 -- ゆっくり霊夢赤縁 (立ち絵)
Layer  3: TachieItem x1 -- ゆっくり魔理沙黄縁 (立ち絵)
Layer  0: VoiceItem x365 -- 音声・字幕
```

### 1-d. 変更前の全 VideoEffects 適用経路

| 経路 | 関数 | 適用先 | VideoEffects を書くか | Layer 制約 |
|------|------|--------|----------------------|-----------|
| motion (G-16 Phase2) | `_apply_motion_to_tachie_items` | TachieItem のみ | 書く | CharacterName 一致 |
| group_motion (G-20) | `_apply_group_motion` | GroupItem のみ | **書かない** (X/Y/Zoom のみ) | Remark 一致 |
| bg_anim (G-14) | `_apply_bg_anim_to_image_item` | ImageItem | **書かない** (X/Y/Zoom のみ) | Layer 0 のみ |
| bg_anim (G-17 profile) | `_apply_timeline_profile_adapters` | ImageItem/VideoItem | 書く | **Layer 0 のみ** |
| motion (G-17 profile) | `_apply_timeline_profile_adapters` | TachieItem のみ | 書く | CharacterName 一致 |

**結論**: 「Layer 10 の ImageItem に VideoEffects を適用する」コードパスは存在しなかった。

---

## 2. 実施した全作業

### 作業A: motion_target コードパス新設

| ファイル | 変更種別 | 内容 |
|----------|----------|------|
| `src/pipeline/ymmp_patch.py` | 機能追加 (+216 行) | `_parse_motion_target_layer()` と `_apply_motion_to_layer_items()` を新設。`_apply_motion_to_tachie_items()` は `motion_target` 付きエントリをスキップ。`patch_ymmp()` から新関数を呼び出し |
| `src/pipeline/ir_validate.py` | 機能追加 (+52 行) | `motion_target` フィールドのバリデーション。`"speaker"` / `"layer:N"` / `{"layer": N}` を受理。不正形式は `MOTION_TARGET_INVALID` / `MOTION_TARGET_INVALID_TYPE` エラー |

### 作業B: CLI ラベル修正

| ファイル | 変更種別 | 内容 |
|----------|----------|------|
| `src/cli/main.py` | ラベル修正 (2 箇所) | `"TachieItem VideoEffects writes"` → `"VideoEffects writes (motion)"`。motion_target で ImageItem にも書くようになったため、item type 固有のラベルでは不正確 |

### 作業C: テスト IR 調整（ユーザー手動修正含む）

| ファイル | 変更種別 | 内容 |
|----------|----------|------|
| `samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json` | テスト IR 更新 | 最初: 全 10 件に motion_target 付与 → ユーザー指摘で調整: 10 件中 4 件のみ motion_target 付き (index 1, 3, 5, 8)、残り 6 件は motion: "none"。発話の感情と配達員の動きを独立させテスト目的を明確化 |

**テスト IR の最終状態**:

| index | speaker | face | motion | motion_target | 意図 |
|-------|---------|------|--------|---------------|------|
| 1 | 霊夢 | thinking | nod | layer:10 | 配達員がうなずく |
| 2 | 霊夢 | sad | none | (なし) | 配達員は静止 |
| 3 | 魔理沙 | surprised | surprise_jump | layer:10 | 配達員がジャンプ |
| 4 | 霊夢 | thinking | none | (なし) | 配達員は静止 |
| 5 | 霊夢 | serious | panic_shake | layer:10 | 配達員が震える |
| 6 | 霊夢 | serious | none | (なし) | 配達員は静止 |
| 7 | 霊夢 | smile | none | (なし) | 配達員は静止 |
| 8 | 魔理沙 | sad | deny_shake | layer:10 | 配達員が首振り |
| 9 | 魔理沙 | serious | none | (なし) | 配達員は静止 |
| 10 | 魔理沙 | angry | none | (なし) | 配達員は静止 |

### 作業D: G-24 茶番劇テンプレート仕様策定

テスト IR の問題指摘をきっかけに、**茶番劇演者の主経路はテンプレート解決**という方針が確立された。

| ファイル | 変更種別 | 内容 |
|----------|----------|------|
| `docs/SKIT_GROUP_TEMPLATE_SPEC.md` | **新規** | G-24 仕様書。speaker_tachie / skit_group / overlay_render の3層を明確に分離。canonical template → 小演出テンプレ量産 → production での template 解決 (exact / fallback / manual note) |
| `samples/registry_template/skit_group_registry.template.json` | **新規** | 共有レジストリテンプレート。canonical group 1 件 + 派生テンプレート 3 件 + fallback chain |
| `samples/registry_template/README.md` | 追記 | skit_group_registry セクション追加 |

### 作業E: ドキュメント横断整合

| ファイル | 内容 |
|----------|------|
| `docs/PRODUCTION_IR_SPEC.md` | `motion_target` フィールドを utterance テーブルに追加。v1.2 セクション |
| `docs/PRODUCTION_IR_CAPABILITY_MATRIX.md` | motion の分岐図に `_apply_motion_to_layer_items` を追加。三経路に更新 |
| `docs/FEATURE_REGISTRY.md` | G-23 の speaker_tachie 専用記述を削除。G-24 (approved) を追加 |
| `docs/INVARIANTS.md` | 外部茶番劇演者を speaker_tachie から分離する不変条件追加 |
| `docs/OPERATOR_WORKFLOW.md` | 茶番劇テンプレート運用の dev/production/role 分離セクション追加 |
| `docs/AUTOMATION_BOUNDARY.md` | skit group template を外部演者の主経路として記載 |
| `docs/INTERACTION_NOTES.md` | 茶番劇演者の報告ルール追加 |
| `docs/NAV.md` | SKIT_GROUP_TEMPLATE_SPEC.md リンク追加 |
| `docs/USER_REQUEST_LEDGER.md` | "Template-first for skit group" エントリ追加 |
| `docs/project-context.md` | 決定ログ + handoff focus を G-24 に更新 |
| `docs/runtime-state.md` | slice / next_action / frontier / hold / feature を G-24 template-first に全面改訂 |
| `docs/verification/README.md` | SKIT_GROUP_TEMPLATE_SPEC.md リンク追加 |

---

## 3. 変更後の全 VideoEffects 適用経路

| 経路 | 関数 | 適用先 | VideoEffects を書くか | Layer 制約 |
|------|------|--------|----------------------|-----------|
| motion (G-16 Phase2) | `_apply_motion_to_tachie_items` | TachieItem のみ | 書く | CharacterName 一致 |
| **motion + motion_target (新規)** | **`_apply_motion_to_layer_items`** | **ImageItem / GroupItem** | **書く** | **指定レイヤー** |
| group_motion (G-20) | `_apply_group_motion` | GroupItem のみ | 書かない (X/Y/Zoom) | Remark 一致 |
| bg_anim (G-14) | `_apply_bg_anim_to_image_item` | ImageItem | 書かない (X/Y/Zoom) | Layer 0 のみ |
| bg_anim (G-17 profile) | `_apply_timeline_profile_adapters` | ImageItem/VideoItem | 書く | Layer 0 のみ |
| motion (G-17 profile) | `_apply_timeline_profile_adapters` | TachieItem のみ | 書く | CharacterName 一致 |

---

## 4. アーキテクチャ判断: 3 層分離

G-24 で確立された分離。`motion_target` はあくまで**補助経路**であり、茶番劇演者の主経路はテンプレート解決。

| 層 | 対象 | 配下アイテム型 | 主経路 | 補助 |
|----|------|--------------|--------|------|
| **speaker_tachie** | 解説役のゆっくり立ち絵 | `TachieItem` (連番アニメ + TachieFaceParameter) | `motion` (G-16/G-17) + `face` / `idle_face` / `slot` | -- |
| **skit_group** | 配達員等の外部人物素材 + 装飾 | **`ImageItem` のみ** (body + 顔 + 任意で装飾)。`TachieItem` 不可 | **canonical template → 派生テンプレ → template 解決** (G-24) | `motion_target` で VideoEffects 直書き / `group_motion` で幾何補助 |
| **overlay_render** | YMM4 書き出し透過 PNG | `ImageItem` | `overlay_map` (G-16) | G-22 hold |

### 固定ルール (INVARIANTS.md に追記済み)

- `motion` は **speaker_tachie の motion** として扱う (省略時)
- 配達員等の茶番劇演者は **skit_group template** で扱う
- `group_motion` は **skit_group の幾何補助** であり、感情モーションの主表現ではない
- **`skit_group` 配下は `ImageItem` のみ** (body + 顔 + 任意で装飾)。`TachieItem` は解説役専用で、外部演者には使わない
- 顔の感情差し替えは `ImageItem.Source` パス置換で行う (`TachieFaceParameter` / 連番アニメパーツ分解は外部演者に適用しない)

---

## 5. IR フィールド仕様 (motion_target)

### 受理する値

| 値 | 意味 |
|----|------|
| 省略 / `null` / `""` | 既定: speaker の TachieItem に適用 |
| `"speaker"` | 明示的に speaker の TachieItem に適用 |
| `"layer:10"` | Layer 10 の ImageItem/GroupItem に適用 |
| `{"layer": 10}` | 同上 (オブジェクト形式) |

### 注意事項

- carry-forward **しない** (各 utterance 固有)
- 単一アイテム: TachieItem と同じ分割ロジック
- 複数アイテム: 発話と時間的に重なるアイテムに上書き
- `tachie_motion_effects_map` (G-23) を共用。VideoEffects の JSON 構造は item type に依存しない

---

## 6. 検証結果

| 検証 | 結果 |
|------|------|
| 既存テスト (全 350 件) | **350 passed / 0 failed** |
| B-2 dry-run (調整後テスト IR) | `VideoEffects writes (motion): 6` (4 motion_target エントリ → Layer 10 ImageItem が 6 セグメントに分割) |
| 後方互換 | motion_target なしの IR は従来どおり TachieItem に適用 |

---

## 7. 変更ファイル一覧 (全 16 + 新規 6)

### tracked (変更)

| ファイル | 行数 |
|----------|------|
| `src/pipeline/ymmp_patch.py` | +216 |
| `src/pipeline/ir_validate.py` | +52 |
| `src/cli/main.py` | +4/-4 |
| `docs/PRODUCTION_IR_SPEC.md` | +13 |
| `docs/PRODUCTION_IR_CAPABILITY_MATRIX.md` | +15 |
| `docs/FEATURE_REGISTRY.md` | +8/-6 |
| `docs/OPERATOR_WORKFLOW.md` | +29 |
| `docs/INVARIANTS.md` | +2 |
| `docs/AUTOMATION_BOUNDARY.md` | +1 |
| `docs/INTERACTION_NOTES.md` | +2 |
| `docs/NAV.md` | +6/-4 |
| `docs/USER_REQUEST_LEDGER.md` | +1 |
| `docs/project-context.md` | +3/-2 |
| `docs/runtime-state.md` | +27 |
| `docs/verification/README.md` | +1 |
| `samples/registry_template/README.md` | +8 |

### untracked (新規)

| ファイル | 内容 |
|----------|------|
| `docs/SKIT_GROUP_TEMPLATE_SPEC.md` | G-24 茶番劇テンプレート仕様 |
| `docs/verification/motion-target-implementation-context.md` | 本ファイル |
| `samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json` | テスト IR (motion_target 付き) |
| `samples/registry_template/skit_group_registry.template.json` | skit group レジストリテンプレート |
| `samples/tachie_motion_map_library.json` | G-23: 23 ラベルの VideoEffects プリセット |
| `docs/MOTION_PRESET_LIBRARY_SPEC.md` | G-23 仕様書 |

---

## 8. 次のステップ

### user 先行 (assistant は結果報告を待って再開)

| # | 内容 | 担い手 | 状態 |
|---|------|--------|------|
| 1 | `_tmp/b2_haitatsuin_motion_applied_v2.ymmp` を YMM4 で開き、Layer 10 の配達員 ImageItem に VideoEffects が視覚的に機能するか確認 | user | 未着手 |
| 2 | haitatsuin 配達員の canonical skit_group template を 1 件固定 (YMM4 上で GroupItem + body/head/装飾の基準構成を作成) | user | 未着手 |
| 3 | canonical template から小演出テンプレートを 6-8 件量産 (surprise_jump, panic_shake, deny_shake 等) | user | #2 待ち |

### user 完了後の assistant 作業

| # | 内容 | 担い手 | 前提 |
|---|------|--------|------|
| 4 | `skit_group_registry.template.json` を実テンプレートで埋める | user + assistant | #2, #3 完了 |
| 5 | 実案件で IR 要求を exact / fallback / manual note で解決し P02 に証跡を残す | user + assistant | #4 完了 |

### 完了済み

| # | 内容 | コミット |
|---|------|---------|
| ~~6~~ | ~~motion_target ユニットテスト 8 件追加~~ | `1b45ff2` (358 passed) |
