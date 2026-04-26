# YMM4 背景演出・オペレーション補遺（2026-04）

## 1. この文書の位置づけ

- **目的**: S-6 における「背景の運動・揺らぎ・ループ・エフェクトチェーン」を、**YMM4 内で完結する**運用（公式機能・FAQ・コミュニティプラグイン）として整理するオペレータ向け補遺である。
- **正本との関係**: 自動化の全体骨格・三層責務は [YMM4-AUTOMATION-RESEARCH.md](../YMM4-AUTOMATION-RESEARCH.md)、境界は [AUTOMATION_BOUNDARY.md](../AUTOMATION_BOUNDARY.md)、非交渉条件は [INVARIANTS.md](../INVARIANTS.md)。**第 2 のロードマップ本文はここに置かない**（優先度・次アクションは [runtime-state.md](../runtime-state.md) を参照）。
- **`bg_anim` と patch の技術的正本**: [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md)（`bg_anim` 行）、経路測定は [G12-timeline-route-measurement.md](G12-timeline-route-measurement.md)。品質観点は案件ごとの検証記録で扱う。

以下の **公式 URL・リリース事実** は、当時の調査メモに基づき **最終確認日 2026-04-07 (JST)** とする。細かい版固定はオペレータ環境で [manjubox.net/ymm4/release/](https://manjubox.net/ymm4/release/) を参照して判断する。

---

## 2. YMM4 側で参照しやすい一次情報（公式）

| トピック | 要点 | 参照 |
|---------|------|------|
| プラグインポータル追加・改善 | v4.45.0.0 付近でポータル、テンプレート周りの改善 | [v4.45.0.0 リリース](https://manjubox.net/ymm4/release/4.45.0.0/) |
| ポータル選択・不具合修正 | v4.45.1.0 選択機能、v4.45.4.1 で保存不具合・起動不能修正 | [v4.45.1.0](https://manjubox.net/ymm4/release/4.45.1.0/) / [v4.45.4.1](https://manjubox.net/ymm4/release/4.45.4.1/) |
| 手ぶれカメラ・発光・マスク系 | 背景の後処理としての標準エフェクト拡充の例 | [v4.43.0.0 リリース](https://manjubox.net/ymm4/release/4.43.0.0/) |
| テンプレート import/export・.ymme | テンプレートを資産として流通させる公式導線 | [v4.29.0.0 リリース](https://manjubox.net/ymm4/release/4.29.0.0/) |
| プラグインの使い方 | `.ymme` ダブルクリック、`user\plugin` への `.dll` 配置（サブフォルダ推奨）等 | [FAQ: プラグインを使用する](https://manjubox.net/ymm4/faq/plugin/how_to_use/) |
| テンプレート登録（背景・名前表示） | アイテムをテンプレ化し「追加アイテム（後ろ）」へ指定する手順 | [FAQ: 字幕と一緒にキャラクター名や背景を表示](https://manjubox.net/ymm4/faq/ゆっくりボイス/字幕と一緒にキャラクターの名前や背景を表示したい/) |
| エフェクト端の薄化 | ぼかし／モザイク等で端が薄くなる場合は「サイズを固定」 | [FAQ: エフェクトアイテムの端で薄くなる](https://manjubox.net/ymm4/faq/effect/blur_on_effect_item/) |

**運用上の含意**: テンプレート／エフェクトテンプレートの保存・再利用は公式導線として揃っている。プラグイン導入は FAQ に沿えば再現しやすい一方、**YMM4 更新のたびに「起動・代表プロジェクト再現」の検証ゲート**を置くのが安全である（ポータル不具合修正がリリースノートに明示されていることの裏返し）。

---

## 3. コミュニティプラグイン候補（README 等の公開情報ベース）

採用前に **各リポジトリの LICENSE・更新日・YMM4 要件** を必ず確認すること。NLMYTGen の責務はこれらを **推奨依存として固定しない**（オペレータが YMM4 側で選択する任意ツール群）。

| 名称 | 概要 | 公開根拠 |
|------|------|----------|
| まとめて映像エフェクト (CombinedEffect) | 複数映像エフェクトをプリセット化し適用 | [routersys/YMM4-CombinedEffect](https://github.com/routersys/YMM4-CombinedEffect) |
| カスタム移動 (CustomEasing) | ベジェ等でイージングを作成しテンプレ保存 | [routersys/YMM4-CustomEasing](https://github.com/routersys/YMM4-CustomEasing) |
| 熱揺らぎ (HeatHaze) | 歪み・色収差等 | [routersys/YMM4-HeatHaze](https://github.com/routersys/YMM4-HeatHaze) |
| 3D画像ループ (ImageLoop3D) | 画像の XYZ ループ（描画順の注意が README にある） | [tetra-te/ImageLoop3D](https://github.com/tetra-te/ImageLoop3D) |
| スクロール (ScrollEffect) | 一定方向のスクロール（配布リポ、ソース非同梱の旨は README 依存） | [benikazura/ScrollEffect](https://github.com/benikazura/ScrollEffect) |
| YMM4CustomEasengK | LuaJIT で座標等をスクリプト制御（`_FRAME` 等） | [kotolin-sub/YMM4CustomEasengK](https://github.com/kotolin-sub/YMM4CustomEasengK) |
| CustomEffectSelector | 子エフェクトを数式で制御（Frame/Length/fps, X/Y/Z, Opacity 等） | [dmmo-com-jp/CustomEffectSelector](https://github.com/dmmo-com-jp/CustomEffectSelector) |

**注意例（非公開 API）**: [YMM4ObjectListPlugin](https://github.com/InuInu2022/YMM4ObjectListPlugin) のように、**非公開 API 使用で更新破断しうる**旨が README に書かれているものは、本プロジェクトの採用方針として **推奨しない**（[INVARIANTS.md](../INVARIANTS.md) の責務境界と整合）。

---

## 4. Failure class とガードレール（運用）

| 失敗類型 | 起きうること | 検出の目安 | ガードレール |
|----------|--------------|------------|--------------|
| テンプレ／プリセット破損 | 更新後に保存・読込失敗 | 同一操作の再現、必要なら公式の修正版より新しい版で試す | 版固定＋更新後の短い回帰（起動→代表プロジェクト開く） |
| エフェクト端の薄化 | 画面端が不自然 | プレビュー端の目視 | FAQ の「サイズを固定」を **背景フィルタ系のデフォルト運用**に含める |
| ポータル／プラグイン導入 | 保存されない、起動不能 | 導入直後の再起動 | FAQ 手順の踏襲、問題が出た版は回避しリリースノートで修正確認 |
| 描画順・3D 系の破綻 | 前後関係がおかしい | 目視、README の注意 | 採用パターンをテンプレ側で限定し README の制約を運用に取り込む |
| 非公開 API 依存 | アップデートで停止 | プラグイン README の注意書き | 新規依存として採用しない |

---

## 5. NLMYTGen との接続（現行仕様に合わせた記述）

**誤解しやすい点**: `timeline_profile` を「YMM4 のエフェクトテンプレート名」と 1:1 で結びつけないこと。本 repo では `--timeline-profile` は主に **`apply-production` が ymmp に書き込む経路と台帳（`*_map`）を契約どおり解決するためのスイッチ**であり、G-12 の readback／`timeline_route_contract.json` とセットで扱う（[PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) の `motion` 分岐図、`bg_anim` 行）。

**二層の整理**:

1. **NLMYTGen（L2）**: Writer IR の `bg_anim` ラベル → Template Registry／`bg_anim_map` 等 → `patch_ymmp`／`apply-production` が **G-12 契約内の ymmp 経路**（例: ImageItem の X/Y/Zoom キーフレーム、または `VideoEffects` 追記）に反映する範囲。詳細は能力マトリクス正本。
2. **YMM4（L3）**: エフェクトテンプレート、コミュニティプラグイン、手動の微調整。ここで作る「見た目のプリセット資産」は **第 2 層の辞書・運用ルール**として蓄積し、IR の意味ラベルと混同しない。

**境界（遵守）**: Python での画像生成・合成・動画レンダリングは行わない。`.ymmp` のゼロから生成は行わない（台本読込後の限定 patch のみ）。非公開 API 依存の自動化を主経路にしない。根拠: [AUTOMATION_BOUNDARY.md](../AUTOMATION_BOUNDARY.md)、[INVARIANTS.md](../INVARIANTS.md)、ADR。

---

## 6. 路線案 A / B / C と本 repo 方針の対応

| 案 | 内容 | 本 repo での位置づけ |
|----|------|---------------------|
| **A** | テンプレート＋エフェクトプリセット（例: 複数エフェクトの一括適用プラグイン）で S-6 の反復を減らす | **最優先で運用に乗せやすい**。INVARIANTS の「YMM4 ネイティブに解決できるものは YMM4 に委ねる」と一致。 |
| **B** | Lua／数式プラグインでパラメトリック化 | **条件付き**。式資産のレビュー・教育コストあり。案 A で語彙が固まってから限定導入が安全。 |
| **C** | .NET プラグインで外部設定を読み込み切替 | **凍結寄り**。公式の IToolPlugin はタイムライン直接操作に向かない旨が [YMM4-AUTOMATION-RESEARCH.md](../YMM4-AUTOMATION-RESEARCH.md) にある。新規プラグイン開発は [INVARIANTS.md](../INVARIANTS.md) により **G-02／G-05 系より先行しない**。公開 API と保守見通しが立った場合のみ FEATURE_REGISTRY・ADR を経て検討。 |

---

## 7. 検収チェックリスト（機械・運用・境界）

開発目的の **作業時間計測 KPI は用いない**（[INVARIANTS.md](../INVARIANTS.md)）。以下は **再現性・契約・境界** 中心である。

### 7.1 境界

- [ ] 提案・手順に **Python による画像生成・画像合成・動画レンダリング**が含まれていない。
- [ ] **`.ymmp` ゼロ生成**やそれに等しい主張が含まれていない（patch は台本読込後の限定適用としてのみ）。
- [ ] **非公開 API 依存**を主経路として推奨していない。

### 7.2 NLMYTGen 整合

- [ ] `bg_anim`／`--timeline-profile`／`*_map`／G-12 の説明が [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) と矛盾しない。
- [ ] 代表コーパスで `measure-timeline-routes`（または既存 verification 手順）により **プロファイルと route contract** が意図どおり pass することを、変更時に確認する手順が文書またはリンクで辿れる。

### 7.3 YMM4 運用

- [ ] プラグイン導入は [FAQ: プラグインを使用する](https://manjubox.net/ymm4/faq/plugin/how_to_use/) に沿った **再現手順**（.ymme または `user\plugin`）がチームで共有されている。
- [ ] ぼかし／モザイク等を背景に多用する場合、**「サイズを固定」**の確認が運用チェックに含まれる（上記 FAQ）。
- [ ] YMM4 更新後に **起動**と**代表プロジェクトの再オープン**を短いゲートとして実施する。

### 7.4 品質パケット（任意だが推奨）

- [ ] `bg_anim`／`overlay` の品質観点は案件ごとの検証単位で切り出し、必要なブロックだけ検証記録を残せる。

---

## 8. 変更履歴

| 日付 | 内容 |
|------|------|
| 2026-04-12 | 初版。外部調査メモを境界・現行 I/O に合わせて再編し検収チェックリストを併記。 |
