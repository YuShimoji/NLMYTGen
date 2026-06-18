# Baseball manual preview hands-on (2026-05-26)

この手順は、BN-05 の YMM4 preview gate だけを人間側で確認するためのものです。
レンダー、creative acceptance、publish gate の判定は含めません。

## 開くファイル

YMM4 で次の proof project を開きます。

`samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof.ymmp`

もし YMM4 が相対画像パスを解決できず、画像が表示されない場合は、repo root から次を実行して
ローカルレビュー用 `.ymmp` を開きます。

```powershell
powershell -ExecutionPolicy Bypass -File .\lanes\sports_news\scripts\open_baseball_bn05_preview.ps1
```

## 確認位置

- project は 1920x1080 / 60fps 相当です。
- preview の確認位置は frame `1560`、時刻では `00:26.00` です。
- Baseball PNG の表示区間は `00:26.00` から `00:48.00` までです。
- ImageItem は layer `12`、length `1320` frame です。

## このままでよさそう、と返せる状態

- 1280x720 の infographic が 16:9 画面いっぱいに入り、クロップされていない。
- scoreboard、中央の strike zone、pitch log、current pitch claim が読める。
- 字幕、キャラ、ナレーター要素が pitch claim や strike zone を隠していない。
- timeline 上で item が `00:26.00` に始まり、`00:48.00` で消える。

## 修正が必要、と返してほしい状態

- PNG が切れている、または余白・拡大率が不自然。
- PNG が表示されず、YMM4 上で注釈のような item だけが見える。
- YMM4 preview 上で文字が小さすぎる。
- 他レイヤーが claim、scoreboard、strike zone、pitch log に被る。
- start / end frame が `1560` / `2880` からずれている。

## 返してほしいもの

1. frame `1560` 付近の YMM4 preview screenshot 1 枚。
2. 短い freeform コメント。
3. 固定ラベルは不要です。例: `画像は表示された。このままでよさそう`、`まだ何も表示されない`、`右端が少し切れている`。

## 触らなくてよいもの

- 動画レンダーは不要です。
- production project への移植は不要です。
- BN-04 frame PNG は YMM4 で開かなくて構いません。必要なら
  `C:\Users\PLANNER007\NLMYTGen-baseball-sidequest\samples\_probe\baseball\animation\frames\baseball_pitch_event_p05\`
  の PNG を画像ビューアで確認するだけで足ります。
