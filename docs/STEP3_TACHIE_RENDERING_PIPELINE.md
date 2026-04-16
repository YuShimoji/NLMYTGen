# Step 3 補助: 立ち絵レンダリング PNG パイプライン

> **位置づけ**: 視覚効果ツール選定 slice の Step 3 補助。G-22 dual-rendering の経路 B (「立ち絵を YMM4 上で 1 フレーム PNG に書き出し、後から overlay として乗せる」) を user がハンズオンで踏むときの作業手順。
> **前提**: [STEP3_YMM4_TEMPLATE_CHECKLIST.md](STEP3_YMM4_TEMPLATE_CHECKLIST.md) と並行で使う想定。テンプレ 5 種作成のうち、「PNG 書き出し経路も併用したい表情」だけ本パイプラインを踏む。
> **正本**: [G22-dual-rendering-tachie-and-png-2026-04-16.md](verification/G22-dual-rendering-tachie-and-png-2026-04-16.md) §3

## 何をするか (1 文)

既存立ち絵入り ymmp を YMM4 で開き、対象表情だけ表示された状態を**透明背景の 1 フレーム PNG** として書き出し、`samples/Mat/` に配置して `overlay_map.json` に登録する。

---

## ゴール (完了条件)

- [ ] 主要表情 N 件分の `{speaker}_{emotion}.png` が `samples/Mat/` 配下に存在
- [ ] 各 PNG が**透明背景 (アルファ付き)** で保存されている
- [ ] `overlay_map.json` (または `overlay_map_{project}.json`) に N 件分のラベル登録完了
- [ ] `validate-ir --overlay-map ...` でラベル解決が `OVERLAY_UNKNOWN_LABEL` ゼロ

---

## 必要なもの

- 既存立ち絵入り ymmp (例: `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp`)
- YMM4 (AnimationTachie プラグイン含む)
- `samples/Mat/{speaker}/` に実パーツ一式 (新れいむ / 新まりさ の場合は既にコミット済)

**立ち絵が YMM4 で表示されない場合は先にそちらを解決**。本パイプラインは「立ち絵が画面に正しく出ている状態」が前提 ([HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md](verification/HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md) 参照)。

---

## 手順

### 1. 作業用 ymmp を準備

- [ ] 既存立ち絵入り ymmp を**別名複製** (例: `tachie_render_work_2026-04-17.ymmp`)
- [ ] YMM4 で開き、立ち絵が正常表示されることを確認

### 2. 表情を選ぶ

- [ ] タイムライン上の任意の VoiceItem を選択
- [ ] プロパティの `TachieFaceParameter` で書き出したい表情プリセットを GUI 選択
  - 霊夢例: `serious` / `smile` / `surprised` / `thinking` / `angry` / `sad` (6 表情)
  - 魔理沙例: 同様に必要なものだけ

### 3. 背景をミュート (重要)

- [ ] タイムラインの**背景レイヤー** (ImageItem / 色背景アイテム) を**一時ミュート**
  - これを忘れると **RGB 背景付き PNG** が書き出され、overlay 時に透明合成が破綻する
- [ ] YMM4 のプレビュー画面で**背景が黒または透明格子**になっていることを確認
- [ ] 立ち絵以外のアイテム (他キャラ・吹き出し等) もミュートで単独表示に

### 4. 1 フレーム透明 PNG で書き出し

- [ ] YMM4 の動画出力ダイアログを開く
- [ ] **出力形式: PNG 連番** または **PNG 単一フレーム**
- [ ] **「透明部分あり」(アルファチャンネル出力) を必ず選択**
  - これが最重要ステップ。不透明だと overlay で全面が覆われる
- [ ] 範囲: 対象 VoiceItem 上の 1 フレームのみ
- [ ] 解像度: プロジェクト解像度 (通常 1920×1080) そのまま
- [ ] 出力先: 一時ディレクトリ (後で `samples/Mat/` にリネーム移動)

### 5. PNG の検証とリネーム

- [ ] 書き出された PNG を画像ビューワで開き、**背景が透過**になっていることを確認
  - Windows エクスプローラのサムネイルで格子模様が見えれば OK
- [ ] ファイル名を命名規約に沿ってリネーム: `{speaker}_{emotion}.png`
  - 例: `reimu_surprised.png`, `marisa_angry.png`
- [ ] `samples/Mat/` に配置 ([MATERIAL_SOURCING_RULES.md](MATERIAL_SOURCING_RULES.md) §1 A 方針)

### 6. overlay_map.json に登録

- [ ] `samples/overlay_map_{project}.json` (新規 or 案件用) を開く
- [ ] `overlays` オブジェクトに 1 エントリ追加:
  ```json
  {
    "overlays": {
      "reimu_surprised": "./samples/Mat/reimu_surprised.png",
      "reimu_angry":     "./samples/Mat/reimu_angry.png"
    }
  }
  ```
- [ ] パスは **リポルートからの相対パス** (絶対パス禁止: [MATERIAL_SOURCING_RULES.md](MATERIAL_SOURCING_RULES.md) §5)
- [ ] 表情分 (6 表情 × 対象キャラ数) を繰り返す

### 7. validate-ir で解決確認

IR ファイル (もしあれば) に登録ラベルを 1 件使ってみて、解決エラーがゼロであることを確認:

```bash
uv run python -m src.cli.main validate-ir \
  samples/_probe/b2/haitatsuin_ir_10utt.json \
  --overlay-map samples/overlay_map_haitatsuin.json
```

- [ ] 出力に `OVERLAY_UNKNOWN_LABEL` が出ないこと
- [ ] 出なければ **Step 3 補助は完了**。次は Step 4 (bg_map/overlay_map を本編案件へ適用) に進む

---

## 注意事項 (失敗パターン)

### 背景透過を忘れる (最頻出)

**症状**: overlay 時にキャラの背後が黒塗りや不透明になる
**原因**: PNG 書き出し時に「透明部分あり」を選択し忘れ
**対処**: 手順 4 を再実行。書き出し済 PNG はそのまま使えないので上書き

### RGB 背景 (空・床など) が残る

**症状**: 別シーンに乗せるときに元の背景が混入
**原因**: 手順 3 の背景ミュート漏れ
**対処**: 背景レイヤー全てをミュートしてから再書き出し

### ファイル名の揺らぎ

**症状**: IR で指定したラベルと overlay_map のキーが不一致 → `OVERLAY_UNKNOWN_LABEL`
**対処**: [MATERIAL_SOURCING_RULES.md](MATERIAL_SOURCING_RULES.md) §2-c の命名規約に沿って統一

### YMM4 プラグイン起動のオーバーヘッド

経路 B は「立ち絵プラグインを起動しない」ことが目的の一つ。**書き出した PNG を overlay として使うとき**は、同じシーンに TachieItem を追加しない (経路 A と経路 B の両立時の扱いは [G22-dual-rendering-tachie-and-png-2026-04-16.md](verification/G22-dual-rendering-tachie-and-png-2026-04-16.md) §4.2 参照)。

---

## 量と優先順位の目安

- **最低ライン**: 主要キャラ × 主要表情 2-3 件 (proof 用)
- **実用ライン**: 主要キャラ × 6 表情 × 2 キャラ = **12 枚**
- **充実ライン**: サブキャラ・バリエーション含めて 30-50 枚

Step 5 proof では最低ラインで十分。過剰に先回りして素材を溜めない (実案件で必要性が見えてから追加する)。

---

## 変更履歴

- 2026-04-17: 初版。G-22 dual-rendering の経路 B 作業を user ハンズオン手順として分離
