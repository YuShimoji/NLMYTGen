# G-17 — motion / transition / bg_anim 書き込み（プロファイル限定）

## 前提

- CLI: `--timeline-profile` と [samples/timeline_route_contract.json](../../samples/timeline_route_contract.json) のプロファイル名を一致させる。
- **契約検証に失敗した場合**は `MOTION_ADAPTER_CONTRACT: ...` として警告し、**書き込みは行わない**。

## マップ形式

| IR フィールド | JSON マップ | 書き込み先 |
|---------------|-------------|------------|
| `motion` | `--motion-map`: ラベル → `{ "video_effect": { ... } }` | 話者の `TachieItem` の `VideoEffects` 末尾に **1 エントリ追記**（発話 Voice スパンと重なる最初の立ち絵） |
| `transition` | `--transition-map`: ラベル → `{ "VoiceFadeIn": 0.3, ... }` 等 | 発話の **先頭 VoiceItem** にフィールドをマージ |
| `bg_anim` | `--bg-anim-map`: ラベル → `{ "video_effect": { ... } }` | **Layer 0** の最初の Image/Video の `VideoEffects` 末尾に追記 |

## プロファイル例

- `motion_only`: 必須 `TachieItem.VideoEffects`。transition / bg_anim はオプション契約。

## Failure / warning クラス

| クラス | 意味 |
|--------|------|
| `MOTION_ADAPTER_CONTRACT` | 契約不一致でアダプタ未実行 |
| `MOTION_ADAPTER_CONTRACT_IO` | 契約 JSON の読み込み失敗 |
| `MOTION_MAP_MISS` / `MOTION_SPEC_INVALID` / `MOTION_NO_TACHIE_ANCHOR` | motion |
| `TRANSITION_MAP_MISS` | transition |
| `BG_ANIM_MAP_MISS` / `BG_ANIM_SPEC_INVALID` / `BG_ANIM_NO_LAYER0` | bg_anim |
