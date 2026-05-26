# Baseball manual preview hands-on (2026-05-26)

この手順は、BN-05 の YMM4 preview gate だけを人間側で確認するためのものです。
レンダー、creative acceptance、publish gate の判定は含めません。

## 開くファイル

YMM4 で次の proof project を開きます。

`C:\Users\PLANNER007\NLMYTGen-baseball-sidequest\samples\_probe\baseball\placement\baseball_pitch_event_p05_placement_proof.ymmp`

## 確認位置

- project は 1920x1080 / 60fps 相当です。
- preview の確認位置は frame `1560`、時刻では `00:26.00` です。
- Baseball PNG の表示区間は `00:26.00` から `00:48.00` までです。
- ImageItem は layer `12`、length `1320` frame です。

## PASS として返せる状態

- 1280x720 の infographic が 16:9 画面いっぱいに入り、クロップされていない。
- scoreboard、中央の strike zone、pitch log、current pitch claim が読める。
- 字幕、キャラ、ナレーター要素が pitch claim や strike zone を隠していない。
- timeline 上で item が `00:26.00` に始まり、`00:48.00` で消える。

## FIX として返してほしい状態

- PNG が切れている、または余白・拡大率が不自然。
- YMM4 preview 上で文字が小さすぎる。
- 他レイヤーが claim、scoreboard、strike zone、pitch log に被る。
- start / end frame が `1560` / `2880` からずれている。

## 返してほしいもの

1. frame `1560` 付近の YMM4 preview screenshot 1 枚。
2. `PASS` または `FIX` の短いメモ。
3. FIX の場合は、見えている問題を 1-2 行で十分です。

## 触らなくてよいもの

- 動画レンダーは不要です。
- production project への移植は不要です。
- BN-04 frame PNG は YMM4 で開かなくて構いません。必要なら
  `C:\Users\PLANNER007\NLMYTGen-baseball-sidequest\samples\_probe\baseball\animation\frames\baseball_pitch_event_p05\`
  の PNG を画像ビューアで確認するだけで足ります。
