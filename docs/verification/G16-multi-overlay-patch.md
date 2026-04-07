# G-16 — 複数 overlay（1 発話・複数 ImageItem）

## 目的

`overlay` を **文字列** または **文字列の配列** で受け、同一発話アンカーに複数のオーバーレイ ImageItem を挿入する。

## 仕様

- 単一文字列: 従来どおり 1 本挿入。
- 配列: 各ラベルを順に `overlay_map` から解決し、同一 `frame` / `length` 基準で複数アイテムを追加（`layer` 等はレジストリ側で差別化）。

## validate-ir

- `OVERLAY_INVALID_TYPE`: `overlay` が文字列・文字列配列以外。
- `OVERLAY_UNKNOWN_LABEL`: 既知レジストリ指定時の未知ラベル（従来どおり）。

## patch-ymmp

- `OVERLAY_MAP_MISS` / `OVERLAY_SPEC_INVALID` / `OVERLAY_NO_TIMING_ANCHOR` はラベル単位で発行。
