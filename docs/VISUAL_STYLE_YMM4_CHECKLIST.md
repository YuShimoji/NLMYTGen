# 視覚スタイル三種 — YMM4 / レジストリ整備チェックリスト（オペレータ向け）

[S6-production-memo-prompt.md](S6-production-memo-prompt.md)（C-07 v4）と [VISUAL_STYLE_PRESETS.md](VISUAL_STYLE_PRESETS.md) の前提で、**コード外**に行う制作環境の整備を列挙する。完了したら `face_map.json` / `bg_map.json` / `overlay_map.json` 等を `apply-production` に渡せる状態にする。

---

## 1. 資料パネル風（`data` / `board`）

- [ ] YMM4 で **データ表示**・**黒板**系のアイテムテンプレを用意（既存 `演出/データ表示`・`演出/黒板` の複製改変でも可）
- [ ] よく使う図表・リスト枠を **PNG** で用意し、`overlay_map` に `text_box` や `chart_panel_01` 等のラベルで登録
- [ ] `bg_map` に `dark_board` / `diagram` 等、セクション `default_bg` から参照するラベルを登録
- [ ] 背景を **発話単位**で変えたい場合: 現状は `macro.sections` を細かく分けるか、[FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) の **G-15**（proposed）承認後のパッチ拡張を待つ

---

## 2. 挿絵コマ風（`skit`）

- [ ] **茶番劇**テンプレ（立ち絵＋余白）を YMM4 で固定
- [ ] `speech_bubble` およびコマ枠用 PNG を用意し `overlay_map` に登録（パスは実機の絶対パスで可）
- [ ] 複数コマを同一発話で重ねたい場合は **合成済み 1 枚 PNG** を 1 ラベルにまとめる（`patch-ymmp` は発話あたり 1 `overlay`）
- [ ] `face_map` で寸劇に必要な表情ラベルが palette と一致しているか `validate-ir` で確認

---

## 3. 再現PV風（`mood` ＋ YMM4 ネイティブ）

- [ ] 早いカット感・エフェクトは **YMM4 アイテムテンプレ** にバンドル（PRODUCTION_IR_SPEC 6.4 の `scene_presets[].ymm4_template` 思想）
- [ ] IR では `mood` / `transition` / `motion` / `bg_anim` を付けてもよいが、**ymmp への自動書き込みは現状ない**（G-12 でルート実測のみ）。見た目の主因はテンプレ側
- [ ] `measure-timeline-routes` で自プロジェクトの ymmp を測り、[samples/timeline_route_contract.json](../samples/timeline_route_contract.json) と整合するか確認
- [ ] SE が必要なら `--se-map` と [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) **G-18**（`done`）、正本 [G18-se-audioitem-implementation.md](verification/G18-se-audioitem-implementation.md) を参照

---

## 4. レジストリ JSON の形（参考）

[G13-overlay-se-insertion-packet.md](verification/G13-overlay-se-insertion-packet.md) の `overlay` / `se` 形に準拠。例:

```json
{
  "overlays": {
    "speech_bubble": "D:/ymm4_assets/overlays/speech_bubble.png",
    "text_box": "D:/ymm4_assets/overlays/text_box.png",
    "panel_composite_01": "D:/ymm4_assets/overlays/panel_composite_01.png"
  }
}
```

`apply-production` / `patch-ymmp` では `--overlay-map` にこのファイルを渡す。

---

## 5. 検証の流れ

1. IR を `validate-ir`（`--palette` / `--overlay-map` / `--slot-map` は環境に合わせて付与）  
2. `apply-production ... --dry-run` で機械エラーを潰す  
3. YMM4 でビジュアル確認  

サンプル IR: [samples/ir_visual_styles_dry_sample.json](../samples/ir_visual_styles_dry_sample.json)
