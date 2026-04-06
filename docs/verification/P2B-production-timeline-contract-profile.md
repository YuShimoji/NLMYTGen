# P2B — `production.ymmp` タイムライン contract 整合（bg_anim 「ギャップ」の整理）

## 背景

従来、`motion_bg_anim_*` 系プロファイルでは **bg_anim を required** としていた一方、[samples/production.ymmp](../../samples/production.ymmp) は **ImageItem / VideoItem がタイムラインに存在しない**（立ち絵・Shape・Voice のみ）。そのため `measure-timeline-routes --expect` で **bg_anim の TIMELINE_ROUTE_MISS** が出るのは、パッチ実装欠落というより **この ymmp 形状では bg_anim 観測自体が無い**ことが原因。

## 実施内容

1. `measure-timeline-routes samples/production.ymmp --format json` で観測（motion: `ShapeItem.VideoEffects` / `TachieItem.VideoEffects`、transition: Voice/Tachie/Shape の Fade 系）。
2. [samples/timeline_route_contract.json](../../samples/timeline_route_contract.json) にプロファイル **`production_ai_monitoring_lane`** を追加。  
   - **required**: `motion` + `transition` のみ（上記観測と一致）。  
   - **bg_anim は required に含めない**（本サンプルでは観測なし）。
3. 検証コマンド（exit 0 であること）:

```bash
uv run python -m src.cli.main measure-timeline-routes samples/production.ymmp ^
  --expect samples/timeline_route_contract.json ^
  --profile production_ai_monitoring_lane
```

## patch-ymmp と bg_anim

- **本スライスでは patch コードは変更しない。** bg_anim の IR→ymmp 適用は、**ImageItem を含むテンプレ／別 ymmp** で従来の `motion_bg_anim_effects` 等のプロファイルを使う。
- production レーン用の ymmp で背景アニメを自動化する場合は、**別パケット**で (1) 対象 ymmp の測定 (2) プロファイルまたはパッチ範囲の定義 (3) FEATURE_REGISTRY 登録 を行う。

## 関連

- FEATURE_REGISTRY **G-14**（本パケットの台帳行）
- [P2A-phase2-motion-segmentation-branch-review.md](P2A-phase2-motion-segmentation-branch-review.md)（大規模 motion ブランチは一括マージしない方針）
