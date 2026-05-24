# 視覚スタイル三種 — IR / patch-ymmp / YMM4 の対応表

> 正本: [PRODUCTION_IR_SPEC.md](PRODUCTION_IR_SPEC.md) v1.0、[AUTOMATION_BOUNDARY.md](AUTOMATION_BOUNDARY.md)  
> 運用チェックリスト: [VISUAL_STYLE_YMM4_CHECKLIST.md](VISUAL_STYLE_YMM4_CHECKLIST.md)  
> Writer 補助語彙: [S6-production-memo-prompt.md](S6-production-memo-prompt.md) v4 内「視覚スタイル」

制作方針として **挿絵コマ風・再現PV風・資料パネル風** を使う場合の、既存パイプラインへの載せ方と **自動化の境界** をまとめる。

---

## 三層の流れ

| 層 | 役割 |
|----|------|
| Writer IR | `template` / `face` / `overlay` / `slot` など **意味ラベルのみ** |
| Template Registry | `face_map` / `bg_map` / `overlay_map` / `slot_map` / `scene_presets`（YMM4 テンプレ名の束） |
| `patch-ymmp` | 台本読込後 ymmp の **決められた JSON キー** への反映 |

Python は **画像生成・合成をしない**（AUTOMATION_BOUNDARY 参照）。

---

## スタイル別マッピング

| スタイル | 主な `template` | 典型の `overlay` / その他 | 細部の置き場所 |
|----------|-----------------|---------------------------|----------------|
| **資料パネル風** | `data`, `board` | `text_box`, 独自 `snake_case` ラベル | 図表・文字組みは **PNG 素材** または YMM4 上の手作業 |
| **挿絵コマ風** | `skit` | `speech_bubble`, コマ枠用の独自ラベル | `overlay` は単一ラベルまたは配列で ImageItem 挿入可。複雑なコマ割りは **1 枚に合成した PNG** か G-24 `skit_group` template-first を優先 |
| **再現PV風** | `mood`（＋必要なら `intro` / `closing`） | トランジション・テンポは IR で **ラベル指定可** | `bg_anim` はキーフレーム preset / G-17 VideoEffects、`transition` は `none` / `fade`、`motion` は map 接続時の adapter 対象。強い PV テンポは YMM4 テンプレに寄せる |

---

## `patch-ymmp` の制約（実装事実）

以下は [src/pipeline/ymmp_patch.py](../src/pipeline/ymmp_patch.py) の挙動に基づく。

| 項目 | 状態 |
|------|------|
| `face` / `idle_face` | 反映済み（row-range 対応） |
| `slot` | `slot_map` 契約下で反映 |
| `overlay` | 文字列または配列を `--overlay-map` で解決し、発話アンカーへ `ImageItem` 挿入（G-13/G-16） |
| 背景 | Macro の `sections[].default_bg` と Micro `bg`（carry-forward 解決後）を `bg_map` で解決し、Layer 0 の発話スパン背景として反映（G-15） |
| `bg_anim` | G-14 の X/Y/Zoom キーフレーム preset、または G-17 の `--timeline-profile` + `--bg-anim-map` 経路で反映 |
| `motion` | `--tachie-motion-map` の Phase2 区間分割、または G-17 `--timeline-profile` + `--motion-map` 経路で反映。G-24 茶番劇演者は `skit_group` template-first が主経路 |
| `transition` | `none` / `fade` のみ Voice/Jimaku fade として反映。non-fade は別 FEATURE / YMM4 手動 |
| `se` | `--se-map` でラベル・timing を解決し、G-18 で `AudioItem` 挿入 |

発話ごとに背景を変えたい場合は、Macro の `sections` を細かく分けるか、Micro `bg` を明示して G-15 の発話スパン背景として扱う。素材選定と視認性の creative judgement は YMM4 側で確認する。

---

## 合成 PNG ワークフロー（挿絵コマ）

1. 外部エディタまたは YMM4 で **コマ枠・吹き出し・小物・必要なら文字** を 1 枚にまとめる。  
2. ファイルを所定フォルダに保存し、`overlay_map` にラベル → パスを登録。  
3. IR の `overlay` にそのラベルを指定し、`apply-production` / `patch-ymmp` を実行。  

これにより **複数レイヤーのコマ割り** を、単一 PNG として安定運用できる。複数 `overlay` ラベルの配列挿入も可能だが、見た目の密度や重なりは最終的に YMM4 上で判断する。

---

## 関連コマンド

- `validate-ir` — 語彙・slot 一貫性・face 契約  
- `apply-production` / `patch-ymmp` — IR + 各種 map の反映  
- `measure-timeline-routes` — PV 系でテンプレの `motion` / `transition` / `bg_anim` ルートを実測（G-12）

三スタイル混在の最小 IR 例: [samples/ir_visual_styles_dry_sample.json](../samples/ir_visual_styles_dry_sample.json)（検証手順は [verification/VISUAL_STYLES_IR_DRY_SAMPLE.md](verification/VISUAL_STYLES_IR_DRY_SAMPLE.md)）。
