"""Dump one full sample of each target Effect, preserving animated-value structure.

Purpose: provide concrete JSON that can be copied into library v2.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from collections import defaultdict


TARGETS = [
    "JumpEffect",
    "RepeatMoveEffect",
    "RandomMoveEffect",
    "RepeatRotateEffect",
    "RandomRotateEffect",
    "ZoomEffect",
    "RandomZoomEffect",
    "CrashEffect",
    "InOutCrashEffect",
    "OpacityEffect",
    "InOutGetUpEffect",
    "InOutMoveFromOutsideImageEffect",
    "SepiaEffect",
    "GaussianBlurEffect",
]


def walk(obj, hits):
    if isinstance(obj, dict):
        t = obj.get("$type")
        if isinstance(t, str):
            for name in TARGETS:
                if f".{name}," in t or t.endswith(f".{name}"):
                    hits[name].append(obj)
                    break
        for v in obj.values():
            walk(v, hits)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, hits)


def main(path: str):
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8-sig"))
    hits = defaultdict(list)
    walk(data, hits)
    out = {}
    for name in TARGETS:
        samples = hits.get(name, [])
        if samples:
            out[name] = samples[0]
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "samples/EffectsSamples_2026-04-15.ymmp")
