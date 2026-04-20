#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.pipeline.capability_atlas import DEFAULT_OUTPUT_PATH, build_default_capability_atlas, write_capability_atlas


def main() -> int:
    args = sys.argv[1:]
    output_path = DEFAULT_OUTPUT_PATH
    i = 0
    while i < len(args):
        if args[i] == "-o" and i + 1 < len(args):
            output_path = Path(args[i + 1])
            i += 2
            continue
        print(f"Unknown argument: {args[i]}", file=sys.stderr)
        return 1

    atlas = build_default_capability_atlas()
    write_capability_atlas(atlas, output_path)
    print(f"Wrote {len(atlas['entries'])} capability entries -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
