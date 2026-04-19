"""Inspect v4 ymmp: Layer 10/11 items, their Frame/Length, and VideoEffects.

Purpose: understand why motion=10 is asymmetric (6 + 4) and whether
existing X/Y animations coexist with newly written VideoEffects.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def item_type(it: dict) -> str:
    t = it.get("$type", "")
    return t.split(",")[0].split(".")[-1]


def summarize_animated(v):
    if isinstance(v, dict) and "Values" in v:
        values = v["Values"]
        if isinstance(values, list) and values:
            vals = [x.get("Value") if isinstance(x, dict) else x for x in values]
            return f"Values={vals}, Span={v.get('Span')}, AT={v.get('AnimationType')}"
    return str(v)[:80]


def main(ymmp_path: str):
    data = load(Path(ymmp_path))
    timelines = data.get("Timelines", [])
    if not timelines:
        print("No timelines")
        return
    items = timelines[0].get("Items", [])
    for target_layer in (10, 11):
        print(f"\n========== Layer {target_layer} ==========")
        layer_items = [
            it for it in items
            if it.get("Layer") == target_layer
            and item_type(it) in ("ImageItem", "GroupItem")
        ]
        print(f"  item count: {len(layer_items)}")
        for i, it in enumerate(layer_items):
            t = item_type(it)
            frame = it.get("Frame")
            length = it.get("Length")
            fp = it.get("FilePath", "")
            remark = it.get("Remark", "")
            ve = it.get("VideoEffects", [])
            print(f"  [{i}] {t} Frame={frame} Length={length}")
            print(f"      FilePath={fp}")
            print(f"      Remark={remark!r}")
            # positional keyframes
            for key in ("X", "Y", "Zoom"):
                v = it.get(key)
                if v is not None:
                    print(f"      {key}: {summarize_animated(v)}")
            # VideoEffects
            print(f"      VideoEffects count: {len(ve)}")
            for j, fx in enumerate(ve):
                fx_type = item_type(fx)
                print(f"        [{j}] {fx_type}")
                # show any animated fields briefly
                for k, fv in fx.items():
                    if k == "$type":
                        continue
                    if isinstance(fv, dict) and "Values" in fv:
                        print(f"            {k}: {summarize_animated(fv)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "_tmp/b2_haitatsuin_motion_applied_v4.ymmp")
