#!/usr/bin/env python3
"""Extract a structured effect catalog from EffectsSamples ymmp.

Usage:
    python scripts/extract_effect_catalog.py [INPUT] [-o OUTPUT]

Defaults:
    INPUT  = samples/EffectsSamples_2026-04-15.ymmp
    OUTPUT = samples/effect_catalog.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

CATEGORY_NAMES = [
    "group_tiling",
    "transform_position",
    "in_out_animation",
    "border_shadow_3d",
    "crop_key_mask",
    "color_blur_shader",
    "camera",
    "animation_glitch_audio",
    "group_control",
]

RESERVED_KEYS = frozenset({"$type", "IsEnabled", "Remark"})


def _short_name(full_type: str) -> str:
    return full_type.split(",")[0].rsplit(".", 1)[-1]


def _is_community(full_type: str) -> bool:
    return "Community" in full_type or "Plugin.Community" in full_type


def extract(ymmp_path: Path) -> dict:
    with open(ymmp_path, encoding="utf-8-sig") as f:
        data = json.load(f)

    items = data["Timelines"][0]["Items"]
    effects_map: dict[str, dict] = {}
    categories: dict[str, dict] = {}
    seen_types: set[str] = set()
    duplicates: list[str] = []

    for idx, item in enumerate(items):
        cat_name = CATEGORY_NAMES[idx] if idx < len(CATEGORY_NAMES) else f"item_{idx}"
        video_effects = item.get("VideoEffects", [])
        keyframes = item.get("KeyFrames", {})
        has_kf = bool(keyframes.get("Frames"))

        cat_info: dict = {"item_index": idx, "count": len(video_effects)}
        if has_kf:
            cat_info["has_keyframes"] = True
            cat_info["keyframe_frames"] = keyframes["Frames"]
        categories[cat_name] = cat_info

        for effect in video_effects:
            full_type = effect.get("$type", "")
            name = _short_name(full_type)
            if not name:
                continue

            if full_type in seen_types:
                duplicates.append(name)
                continue
            seen_types.add(full_type)

            params = [k for k in effect if k not in RESERVED_KEYS]
            effects_map[name] = {
                "$type": full_type,
                "is_community": _is_community(full_type),
                "category": cat_name,
                "parameters": params,
            }

    catalog = {
        "_meta": {
            "source": ymmp_path.name,
            "total_unique_effects": len(effects_map),
            "duplicates_skipped": duplicates,
            "note": "YMM4 v4.51.0.3. community effects require plugin installation.",
        },
        "effects": effects_map,
        "categories": categories,
    }
    return catalog


def main() -> None:
    args = sys.argv[1:]
    input_path = Path("samples/EffectsSamples_2026-04-15.ymmp")
    output_path = Path("samples/effect_catalog.json")

    i = 0
    while i < len(args):
        if args[i] == "-o" and i + 1 < len(args):
            output_path = Path(args[i + 1])
            i += 2
        else:
            input_path = Path(args[i])
            i += 1

    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    catalog = extract(input_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    n = catalog["_meta"]["total_unique_effects"]
    dupes = catalog["_meta"]["duplicates_skipped"]
    cats = len(catalog["categories"])
    print(f"Extracted {n} unique effects across {cats} categories -> {output_path}")
    if dupes:
        print(f"  Duplicates skipped: {dupes}")


if __name__ == "__main__":
    main()
