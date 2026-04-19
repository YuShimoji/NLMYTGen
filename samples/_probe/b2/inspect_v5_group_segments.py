"""Inspect each split GroupItem segment in v5 ymmp.

Focus:
- Does each split GroupItem inherit user's existing X/Y/Zoom animation?
- Do the split GroupItems share properties (pre-existing translate etc)?
- Are VideoEffects scoped correctly to each segment?
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def item_type(it: dict) -> str:
    return it.get("$type", "").split(",")[0].split(".")[-1]


def summarize_animated(v):
    if isinstance(v, dict) and "Values" in v:
        values = v["Values"]
        if isinstance(values, list) and values:
            vals = [x.get("Value") if isinstance(x, dict) else x for x in values]
            span = v.get("Span")
            at = v.get("AnimationType")
            return f"Values={vals} Span={span} AT={at}"
    return str(v)[:100]


def dump_segment(i, g, prefix="  "):
    print(f"{prefix}[{i}] Frame={g.get('Frame')} Length={g.get('Length')}")
    print(f"{prefix}  Remark: {g.get('Remark', '')!r}")
    for key in ("X", "Y", "Zoom", "Opacity", "Rotation"):
        v = g.get(key)
        if v is not None:
            print(f"{prefix}  {key}: {summarize_animated(v)}")
    ve = g.get("VideoEffects", [])
    print(f"{prefix}  VideoEffects: {len(ve)} effects")
    for j, fx in enumerate(ve):
        fxt = item_type(fx)
        print(f"{prefix}    [{j}] {fxt}")
    for k, v in g.items():
        if k in ("$type", "X", "Y", "Zoom", "Opacity", "Rotation",
                 "VideoEffects", "Frame", "Length", "Layer", "Remark",
                 "IsEnabled", "Items", "Children", "ChildItems",
                 "CharacterName", "Serif", "TachieFaceParameter"):
            continue
        if isinstance(v, dict) and "Values" in v:
            print(f"{prefix}    {k}: {summarize_animated(v)}")


def main(path: str):
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    items = data["Timelines"][0]["Items"]

    # Layer 9 GroupItem
    group_items = [it for it in items if it.get("Layer") == 9
                   and item_type(it) == "GroupItem"]
    print(f"========== Layer 9 GroupItem (count={len(group_items)}) ==========\n")
    for i, g in enumerate(group_items):
        dump_segment(i, g)
        print()

    # Layer 3/4 TachieItem (解説役)
    for layer in (3, 4):
        tachies = [it for it in items if it.get("Layer") == layer
                   and item_type(it) == "TachieItem"]
        print(f"\n========== Layer {layer} TachieItem (count={len(tachies)}) ==========\n")
        for i, t in enumerate(tachies):
            char = t.get("CharacterName", "?")
            print(f"  [{i}] {char}")
            dump_segment(i, t, prefix="    ")
            print()

    # Layer 10/11 ImageItem
    for layer in (10, 11):
        imgs = [it for it in items if it.get("Layer") == layer
                and item_type(it) == "ImageItem"]
        print(f"\n========== Layer {layer} ImageItem (count={len(imgs)}) ==========\n")
        for i, im in enumerate(imgs):
            dump_segment(i, im, prefix="    ")
            print()


def _placeholder_guard():
    pass

def _old_main_skipped(path: str):
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    items = data["Timelines"][0]["Items"]
    group_items = [it for it in items if it.get("Layer") == 9
                   and item_type(it) == "GroupItem"]
    print(f"Layer 9 GroupItem count: {len(group_items)}\n")
    for i, g in enumerate(group_items):
        print(f"=== [{i}] Frame={g.get('Frame')} Length={g.get('Length')} ===")
        print(f"  Remark: {g.get('Remark', '')!r}")
        for key in ("X", "Y", "Zoom", "Opacity", "Rotation"):
            v = g.get(key)
            if v is not None:
                print(f"  {key}: {summarize_animated(v)}")
        ve = g.get("VideoEffects", [])
        print(f"  VideoEffects: {len(ve)} effects")
        for j, fx in enumerate(ve):
            fxt = item_type(fx)
            print(f"    [{j}] {fxt}")
        # 他の top-level key で animated なものを全て洗う
        print("  other top-level animated keys:")
        for k, v in g.items():
            if k in ("$type", "X", "Y", "Zoom", "Opacity", "Rotation",
                     "VideoEffects", "Frame", "Length", "Layer", "Remark",
                     "IsEnabled", "Items", "Children", "ChildItems"):
                continue
            if isinstance(v, dict) and "Values" in v:
                print(f"    {k}: {summarize_animated(v)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else
         "_tmp/b2_haitatsuin_motion_applied_v5.ymmp")
