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
| **挿絵コマ風** | `skit` | `speech_bubble`, コマ枠用の独自ラベル | **1 発話あたり 1 ラベル → 1 ImageItem**。複数コマを機械投入したい場合は **1 枚に合成した PNG** を推奨 |
| **再現PV風** | `mood`（＋必要なら `intro` / `closing`） | トランジション・テンポは IR で **ラベル指定可** | **テンポ・エフェクトの本体は YMM4 アイテムテンプレ** に寄せる。IR の `motion` / `transition` / `bg_anim` は **patch-ymmp では現状未書き込み**（G-12 でルート測定のみ） |

---

## `patch-ymmp` の制約（実装事実）

以下は [src/pipeline/ymmp_patch.py](../src/pipeline/ymmp_patch.py) の挙動に基づく。

| 項目 | 状態 |
|------|------|
| `face` / `idle_face` | 反映済み（row-range 対応） |
| `slot` | `slot_map` 契約下で反映 |
| `overlay` | **発話 1 つにつき最大 1 ラベル** → `ImageItem` 1 件。`--overlay-map` 必須 |
| 背景 | **`macro.sections[].default_bg` のみ** から `bg_map` 解決。Micro の `bg` は carry-forward に載るが **本パッチでは未使用** |
| `motion` / `transition` / `bg_anim` | IR 上は carry-forward されるが **ymmp への書き込みなし** |
| `se` | ラベル検証は可。`AudioItem` 挿入は [G-13](verification/G13-overlay-se-insertion-packet.md) / [P2C](verification/P2C-se-audioitem-boundary.md) 境界 |

発話ごとに背景を変えたい場合の現実的な運用は、(1) **Macro の `sections` を細かく分ける**、または (2) FEATURE 承認後の **発話スパン bg パケット**（台帳参照）。

---

## 合成 PNG ワークフロー（挿絵コマ）

1. 外部エディタまたは YMM4 で **コマ枠・吹き出し・小物・必要なら文字** を 1 枚にまとめる。  
2. ファイルを所定フォルダに保存し、`overlay_map` にラベル → パスを登録。  
3. IR の `overlay` にそのラベルを指定し、`apply-production` / `patch-ymmp` を実行。  

これにより **複数レイヤーのコマ割り** を、現行の「単一 overlay」契約のまま運用できる。

---

## 関連コマンド

- `validate-ir` — 語彙・slot 一貫性・face 契約  
- `apply-production` / `patch-ymmp` — IR + 各種 map の反映  
- `measure-timeline-routes` — PV 系でテンプレの `motion` / `transition` / `bg_anim` ルートを実測（G-12）

三スタイル混在の最小 IR 例: [samples/ir_visual_styles_dry_sample.json](../samples/ir_visual_styles_dry_sample.json)（検証手順は [verification/VISUAL_STYLES_IR_DRY_SAMPLE.md](verification/VISUAL_STYLES_IR_DRY_SAMPLE.md)）。
