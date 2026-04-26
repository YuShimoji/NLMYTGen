# G-22 — Dual-rendering scene_presets (立ち絵 TachieItem + 書き出し PNG の両運用)

**ステータス**: **G-22 proposed**（2026-04-16 起票。承認判定は視覚効果 slice Step 5 proof 後）
**関連 FEATURE**: [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) Section C / G-13 (done・overlay 挿入) / G-21 (hold・外部素材+ゆっくり頭 重畳)
**slice 正本**: [VISUAL-TOOL-SELECTION-2026-04-16.md](VISUAL-TOOL-SELECTION-2026-04-16.md)
**目的**: 同一演出を (A) 立ち絵 TachieItem 経路 と (B) YMM4 で書き出した立ち絵レンダリング PNG の overlay 経路 の両方で実現可能にし、工数削減と作業全体の整合性・演出蓄積を両立する。

---

## 0. 読む順

1. [VISUAL_EFFECT_SELECTION_GUIDE.md](../VISUAL_EFFECT_SELECTION_GUIDE.md) — 視覚効果 4 類・ルート比較の正本
2. [VISUAL-TOOL-SELECTION-2026-04-16.md](VISUAL-TOOL-SELECTION-2026-04-16.md) — 本 slice の進捗証跡
3. [PRODUCTION_IR_SPEC.md](../PRODUCTION_IR_SPEC.md) §3.7 `overlay` / §6 Template Registry
4. [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) G-13 / G-21

---

## 1. 背景と既存経路との整合

### 1.1 起票の経緯

2026-04-16 のユーザー対話で以下の運用意向が明示された:

> 「立ち絵での再現と、一枚絵にレンダリング後の素材でも両方で、画面上に見た目を反映できるようにしておきたい。一枚絵のほうは工数削減で、立ち絵のほうは作業全体の整合性・演出蓄積と転用のため」
> 「1 枚絵 PNG は、YMM4 上でゆっくりの表情を作っておき、後から乗せるだけという意味」

同一のキャラ・演出意図に対して、重さの異なる 2 経路を選択できるようにする要望。

### 1.2 既存経路との関係

| ID | 内容 | G-22 との違い |
|----|------|---------------|
| **G-13 (done)** | `overlay` ラベル → `ImageItem` 挿入。`overlay_map` 解決 | G-22 は G-13 を **そのまま流用**。新規実装不要の可能性が高い |
| **G-21 (hold・当面不要判定)** | 外部人物素材 (配達員等) + ゆっくり頭 TachieItem 重畳 | G-21 は **2 アイテムの重畳**。G-22 は **立ち絵を事前レンダリングした単一 PNG** |
| **G-19 (done)** | ゆっくり立ち絵内部の body パーツ束ね | レイヤー別 (G-19 は TachieItem 内部)。G-22 はタイムラインレイヤー |

**混同注意**: G-21 は「外部画像 + ゆっくり頭」の**タイムライン重畳**、G-22 は「立ち絵を事前に 1 枚絵化した PNG」の**単層挿入**。

---

## 2. 2 経路の使い分け

### 2.1 経路 A: 立ち絵 TachieItem (従来)

- **実装**: `face` / `idle_face` / `slot` + `face_map` / `slot_map` (既存 done)
- **特徴**:
  - 発話ごとに表情切替 (face_map 経由)
  - YMM4 のリップシンク (MouthAnimation) が機能
  - 自動瞬き (EyeAnimation) が機能
  - idle_face の carry-forward で待機中も自然
- **向き**: 主要キャラの本編・表情遷移の多いシーン
- **コスト**: face_map 整備・IR 指定・YMM4 立ち絵配置 (既存 ymmp 活用で低減)

### 2.2 経路 B: 書き出し PNG の overlay 挿入 (新運用)

- **実装**: `overlay` + `overlay_map` (既存 G-13 done。**コード変更なし**)
- **特徴**:
  - 立ち絵を YMM4 上で **1 フレーム PNG に書き出し**、`overlay_map` にラベル登録
  - YMM4 の立ち絵プラグイン起動を経由しないので軽い
  - 表情は **書き出し時点で固定** (リップシンクなし・瞬きなし)
  - 複数表情を使いたければ表情別 PNG を複数登録
- **向き**: 背景キャラ・ワンシーン限定登場・サムネ用素材・回想カット等
- **コスト**: PNG 書き出し作業 (YMM4 GUI で表情ごとに 1 フレーム出力 → 透明背景で保存)

### 2.3 判断フローチャート

```
このシーンでキャラを画面に出したい
   ↓
そのキャラは「発話中に口パク・表情遷移が必要」か?
   ├─ Yes → 経路 A (立ち絵 TachieItem)
   └─ No  → そのキャラは「5 回以上登場」するか?
            ├─ Yes → 経路 A (registry 整備コストを償却)
            └─ No  → 経路 B (書き出し PNG overlay)
```

---

## 3. PNG 書き出しの技術的前提

### 3.1 背景透過

- YMM4 の動画出力設定で **「透明部分あり」(アルファ付き PNG)** を選択
- 背景レイヤー (ImageItem / 黒背景等) を一時非表示にしてから書き出す
- 他の背景に重ねるときに汎用性が高い

### 3.2 書き出し手順 (user actor)

1. 既存立ち絵入り ymmp (例: `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp`) を YMM4 で開く
2. 対象 VoiceItem の `TachieFaceParameter` で表情を指定 (GUI で表情プリセット選択)
3. タイムライン上の背景レイヤーを一時ミュート
4. 動画出力 → 範囲 1 フレーム・透明 PNG 形式で書き出し
5. 出力された PNG を `samples/Mat/{speaker}_{emotion}.png` に配置
6. `overlay_map.json` にラベル登録:
   ```json
   { "overlays": { "reimu_anger_rendered": "./samples/Mat/reimu_anger.png" } }
   ```

### 3.3 命名規約 (MATERIAL_SOURCING_RULES.md 連携)

- 立ち絵書き出し PNG: `{speaker}_{emotion}.png` (例: `reimu_anger.png`)
- レンダリング由来を明示したい場合のみ: `{speaker}_{emotion}_rendered.png`
- オーバーレイ全般: `ov_{type}_{variant}.png` (既存規約)

---

## 4. IR / registry の書き方 (第一候補: 新規語彙なし)

### 4.1 現行 IR での表現

既存の `overlay` フィールドで完結する:

```json
{
  "utterances": [
    {
      "speaker": "reimu",
      "template": "skit",
      "overlay": "reimu_anger_rendered"
    }
  ]
}
```

registry 側で `overlay_map.json`:

```json
{
  "overlays": {
    "reimu_anger_rendered": "./samples/Mat/reimu_anger.png"
  }
}
```

**新規 IR 語彙・CLI フラグ・validate-ir 拡張は不要**。G-13 の done 実装でそのまま挿入される。

### 4.2 経路 A/B 併用時の注意

- 同一発話に `face` (経路 A) と `overlay` (経路 B) の両方を指定すると、**両方が描画される** (TachieItem と ImageItem が別レイヤーで重畳)
- 経路 B 単独でキャラ描画したい場合は、発話のキャラを YMM4 側で `slot: "off"` 等で非表示にする必要がある
  - → これは既存の `slot_map` の `"off": null` で解決可能 (G-11 done)

---

## 5. 将来の拡張余地 (実装は承認後)

現状は **運用ドキュメント化で十分** だが、以下は将来の拡張候補:

### 5.1 registry メタ拡張 (optional)

```json
{
  "overlays": {
    "reimu_anger_rendered": {
      "path": "./samples/Mat/reimu_anger.png",
      "source": "tachie_render",
      "rendered_from": "samples/characterAnimSample/haitatsuin_2026-04-12.ymmp",
      "rendered_at": "2026-04-16"
    }
  }
}
```

- `source`: `"tachie_render"` / `"ai_generated"` / `"external_import"`
- 利点: 出典追跡・差し替え容易化・ライセンス管理との連携
- 実装: overlay_map の loader に meta フィールド許容を追加 (既存形式との後方互換)

### 5.2 scene_presets での variant 軸 (G-21 と統合検討)

```json
{
  "scene_presets": {
    "skit_reaction": {
      "variants": {
        "tachie": { "face": "surprised", "slot": "right" },
        "rendered": { "overlay": "reimu_surprised_rendered" }
      }
    }
  }
}
```

- CLI フラグ `--rendering tachie|rendered` で切替
- **現時点では不要** (既存の overlay で表現可)。将来 variant 軸が必要になれば起票

### 5.3 これらは「起票しない」

現状 (Step 5 proof 前) で上記拡張を設計に入れると、YAGNI に反する可能性が高い。**proof 後に必要性が見えてから別 FEATURE として起票** する。

---

## 6. 承認判定のトリガー

G-22 を **proposed → approved / rejected** に判定する条件:

### 6.1 approved 昇格の条件

視覚効果 slice Step 5 proof で以下が確認できた場合:

1. 1 本の実案件で経路 B (書き出し PNG overlay) が実際に使われた
2. 経路 A と経路 B が同一動画内で併用され、視覚的に破綻しなかった
3. PNG 書き出し作業が運用として回った (user 負担が許容範囲)

→ この場合、G-22 の提案内容は **運用で実証済み**。`approved` 昇格 → 必要なら §5.1 (registry メタ拡張) の実装着手

### 6.2 rejected / 当面不要 の条件

1. 経路 A だけで十分だった (PNG 書き出しのニーズが発生しなかった)
2. 経路 B が発生したが既存 overlay_map で完結しており、追加実装の必要性がない

→ この場合、G-22 は **当面不要判定** (G-21 と同扱い)。将来再燃時は本メモを復帰点として使う

### 6.3 判定タイミング

[VISUAL-TOOL-SELECTION-2026-04-16.md §5 Step 5](VISUAL-TOOL-SELECTION-2026-04-16.md) の proof 完了時。`P02-production-adoption-proof.md` への追記とセットで判定を記録する。

---

## 7. 承認なしで継続可能 / 不可

### 7.1 承認なしで可能

- 本メモ・[VISUAL-TOOL-SELECTION-2026-04-16.md](VISUAL-TOOL-SELECTION-2026-04-16.md) の更新
- PNG 書き出しと `overlay_map.json` 登録 (既存 G-13 done の範囲)
- user による実運用・proof 取得
- 運用結果の記録 (P02 追記)

### 7.2 承認が必要

- `src/` コード変更 (registry loader 拡張など)
- IR 語彙の新規追加 (`rendering` フィールド等)
- `validate-ir` の検証ロジック拡張
- scene_presets への variant 軸追加

---

## 8. 変更履歴

- 2026-04-16: 初版。視覚効果 slice (VISUAL-TOOL-SELECTION-2026-04-16.md) の継続起票として作成。運用は既存 G-13 overlay 経路で完結する想定で proposed 登録
