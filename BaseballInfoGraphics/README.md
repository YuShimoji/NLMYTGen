# BaseballInfoGraphics

`BaseballInfoGraphics/` は、野球速報系ゆっくり解説動画で使うインフォグラフィックのデザインソースである。

## 現在の正本

- Entry point: `Baseball Infographic.html`
- Canonical variant: `variants/detailed.jsx`
- Use case: 野球ニュース・試合解説内で使う 1280x720 の分析カード
- Status: draft design source。production renderer / YMM4 proof ではない

## 重要な境界

- 使用するのは C 詳細のみ。
- A minimal / B standard / minimal / standard の再追加はしない。
- このフォルダは background skit / skit_group のテンプレート置き場ではない。
- このフォルダはサムネイル制作レーンではない。
- PNG export は必要だが、アプリ内 animation を活かすため、静止画化だけで完了扱いにしない。
- 背景 slot は `ambientBackdrop` と呼ぶ。これは球場感・照明・芝・抽象スタジアムなどの雰囲気背景用であり、実在選手写真・公式映像・ニュース写真・主張根拠の slot ではない。
- `ambientBackdrop` はデザイン機能であり、episode asset として使う段階で `LICENSE.csv` または生成記録に provenance を残す。

## ファイル責務

| File | 役割 |
| --- | --- |
| `Baseball Infographic.html` | ブラウザで開くエントリポイント、Tweaks、再生制御 |
| `data.js` | 現在の mock game data |
| `variants/detailed.jsx` | C 詳細デザイン本体 |
| `components/strike-zone.jsx` | ストライクゾーン表示 |
| `components/diamond.jsx` | 塁状況表示 |
| `design-canvas.jsx` | artboard / export / editing canvas |
| `tweaks-panel.jsx` | 色・密度・表示オプション |

## ambientBackdrop

`data.js` の `visual.ambientBackdrop` は、C 詳細の pitch stage に背景の雰囲気を足すための任意 slot である。

- 未設定または `imageUrl` なし: 現行の暗色グリッド/グラデーションを表示する。
- `imageUrl` あり: 記録済みの雰囲気背景を stage 背景として表示する。
- `kind` / `provenance` / `usageStage` は readback と publish-gate 接続用の metadata で、layout 可否を直接決めない。
- 現在の preview sample は `assets/ambient/ballpark-night-grid.svg` を使う。同階層の `assets/ambient/LICENSE.csv` が provenance record である。

## Deterministic preview controls

ブラウザ URL の query で、PNG capture や animation capture の開始状態を固定できる。

- `pitch=0..n-1`
- `autoplay=0|1`
- `stepMs=250..10000`
- `density=compact|standard`
- `statMode=simple|detailed`
- `showRomaji=0|1`

現在状態は `window.__BASEBALL_INFOGRAPHICS_STATE__` に公開される。

## 今後の開発単位

1. C 詳細の可読性・情報優先度・安全余白を改善する。
2. `data.js` の mock を実入力 JSON contract へ分離する。
3. 1280x720 PNG export を deterministic にする。
4. 投球更新などの animation を deterministic に制御し、動画素材または連番へ出力する。
5. YMM4 に PNG/animation asset を置くための placement contract を作る。

## 参照仕様

- `../docs/BASEBALL_NEWS_PIPELINE_SPEC.md`
- `../lanes/sports_news/docs/baseball_infographic_backlog.md`
