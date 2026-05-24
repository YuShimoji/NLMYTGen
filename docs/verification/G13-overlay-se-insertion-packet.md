# G-13 Overlay / SE Insertion Packet

> Date: 2026-04-06
> Scope: `overlay` / `se`
> Method: `validate-ir` + `patch-ymmp` / `apply-production`

## Goal

`overlay` / `se` を broad な manual retry loop に戻さず、
mechanical scope を registry / timing anchor / fail-fast で閉じる。

## What Is Fixed

- `overlay` label can be validated mechanically via `validate-ir`
- `overlay` registry can be supplied via `--overlay-map`
- `patch-ymmp` / `apply-production` can insert deterministic `ImageItem` overlays
- overlay timing anchor is resolved from utterance start/end frame
- overlay insertion can be dry-run checked without visual proof

## Registry Shape

Overlay registry:

```json
{
  "overlays": {
    "arrow_red": {
      "path": "C:/overlay/arrow_red.png",
      "layer": 4,
      "length": 12,
      "anchor": "start",
      "offset": 0,
      "x": 0,
      "y": 0,
      "zoom": 100,
      "opacity": 100
    }
  }
}
```

SE registry:

```json
{
  "se": {
    "click": {
      "path": "C:/se/click.wav",
      "anchor": "start",
      "offset": 0
    }
  }
}
```

## Failure Classes

- `OVERLAY_UNKNOWN_LABEL`
- `SE_UNKNOWN_LABEL`
- `OVERLAY_MAP_MISS`
- `OVERLAY_NO_TIMING_ANCHOR`
- `OVERLAY_SPEC_INVALID`
- `SE_MAP_MISS`
- `SE_NO_TIMING_ANCHOR`
- `SE_SPEC_INVALID`

### 廃止（G-18 以降）

- 旧 SE write-route unsupported failure — [samples/AudioItem.ymmp](../../samples/AudioItem.ymmp) と G-18 `_apply_se_items` により `AudioItem` 挿入を実装したため発行しない。

## Current G-13 State

- overlay registry contract: done
- overlay deterministic insertion: done
- overlay fail-fast / dry-run / CLI integration: done
- se registry validation: done
- se timing anchor resolution: done
- se AudioItem write route: **done**（G-18。テンプレート deepcopy または最小骨格で挿入）

## Interpretation

- `overlay` is now assistant-owned mechanical scope
- `se` is no longer an ambiguous manual step: label / timing は G-13 どおり、`AudioItem` 挿入は G-18 で mechanical scope に入った
- 詳細は [G18-se-audioitem-implementation.md](G18-se-audioitem-implementation.md) と [P2C-se-audioitem-boundary.md](P2C-se-audioitem-boundary.md)
