"""Inspect haitatsuin ymmp Layer 9 (and surrounding) for GroupItem existence.

Verifies whether an existing GroupItem already wraps body + face ImageItems,
which would make motion_target: "layer:9" sufficient (no user work needed).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def item_type(it: dict) -> str:
    t = it.get("$type", "")
    return t.split(",")[0].split(".")[-1]


def main(ymmp_path: str):
    data = json.loads(Path(ymmp_path).read_text(encoding="utf-8-sig"))
    items = data["Timelines"][0]["Items"]
    print(f"Total items: {len(items)}\n")

    # layer ごとの item 数と type 分布
    print("=== layer distribution ===")
    by_layer: dict[int, list[dict]] = {}
    for it in items:
        by_layer.setdefault(it.get("Layer", -1), []).append(it)
    for lyr in sorted(by_layer.keys()):
        lst = by_layer[lyr]
        types = {}
        for it in lst:
            t = item_type(it)
            types[t] = types.get(t, 0) + 1
        print(f"  Layer {lyr}: {dict(types)} (total {len(lst)})")

    # GroupItem を全 layer から探す
    print("\n=== GroupItems (any layer) ===")
    for it in items:
        if item_type(it) == "GroupItem":
            layer = it.get("Layer")
            remark = it.get("Remark", "")
            frame = it.get("Frame")
            length = it.get("Length")
            x_values = it.get("X", {}).get("Values", [{}])
            y_values = it.get("Y", {}).get("Values", [{}])
            zoom_values = it.get("Zoom", {}).get("Values", [{}])
            ve = it.get("VideoEffects", [])
            print(f"  Layer {layer}, Frame {frame}, Length {length}")
            print(f"    Remark: {remark!r}")
            print(f"    X={x_values[0].get('Value') if x_values else None}"
                  f" Y={y_values[0].get('Value') if y_values else None}"
                  f" Zoom={zoom_values[0].get('Value') if zoom_values else None}")
            print(f"    VideoEffects count: {len(ve)}")
            for j, fx in enumerate(ve):
                print(f"      [{j}] {item_type(fx)}")
            # Children 的なフィールド (GroupItem の内部構造)
            for key in ("Items", "Children", "ChildItems"):
                if key in it:
                    print(f"    {key} count: {len(it[key]) if isinstance(it[key], list) else '(not list)'}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else
         "samples/characterAnimSample/haitatsuin_2026-04-12.ymmp")
