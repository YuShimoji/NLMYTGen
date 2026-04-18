"""Extract real Effect property structures from EffectsSamples ymmp.

Purpose: inform library v2 with actual YMM4 Effect parameter shapes.
Read-only; dumps per-Effect sample properties to stdout.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from collections import defaultdict


TARGET_EFFECTS = [
    "JumpEffect",
    "RepeatMoveEffect",
    "RandomMoveEffect",
    "RepeatRotateEffect",
    "RandomRotateEffect",
    "ZoomEffect",
    "RandomZoomEffect",
    "CrashEffect",
    "InOutCrashEffect",
    "BounceEffect",
    "OpacityEffect",
    "InOutGetUpEffect",
    "InOutMoveFromOutsideImageEffect",
    "SepiaEffect",
    "GaussianBlurEffect",
]


def walk(obj, hits):
    """Collect all dict nodes that have $type referencing a target Effect."""
    if isinstance(obj, dict):
        t = obj.get("$type")
        if isinstance(t, str):
            for name in TARGET_EFFECTS:
                if f".{name}," in t or t.endswith(f".{name}"):
                    hits[name].append(obj)
                    break
        for v in obj.values():
            walk(v, hits)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, hits)


def summarize_value(v):
    """Compact representation for dict/list/scalar."""
    if isinstance(v, dict):
        if "Values" in v and isinstance(v["Values"], list):
            vals = v["Values"]
            if vals:
                first = vals[0]
                if isinstance(first, dict) and "Value" in first:
                    return f"<animated: [{', '.join(str(x.get('Value')) for x in vals[:3])}...]>"
            return "<animated: empty>"
        if "Value" in v and len(v) <= 4:
            return f"<scalar: {v.get('Value')}>"
        return f"<dict keys: {list(v.keys())}>"
    if isinstance(v, list):
        return f"<list len={len(v)}>"
    return repr(v)


def main(path: str):
    p = Path(path)
    if not p.exists():
        print(f"Not found: {path}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(p.read_text(encoding="utf-8-sig"))
    hits = defaultdict(list)
    walk(data, hits)
    for name in TARGET_EFFECTS:
        samples = hits.get(name, [])
        print(f"### {name} (found {len(samples)} samples)")
        if not samples:
            print("  (no samples)\n")
            continue
        # show up to 2 samples
        for i, s in enumerate(samples[:2]):
            print(f"  sample {i+1}:")
            for k, v in s.items():
                if k == "$type":
                    continue
                print(f"    {k}: {summarize_value(v)}")
            print()
        if len(samples) > 2:
            print(f"  (... {len(samples)-2} more samples omitted)\n")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "samples/EffectsSamples_2026-04-15.ymmp")
