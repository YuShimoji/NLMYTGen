"""gold_set_review.txt のラベルを gold_set_template.json に反映する。

Usage:
    python tools/import_gold_set.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def parse_review(text: str) -> dict[int, str]:
    """レビューシートからラベルを抽出する。"""
    labels: dict[int, str] = {}
    for line in text.splitlines():
        m = re.match(r'L(\d+)\s+\[([AB?]?)\]', line)
        if m:
            line_num = int(m.group(1))
            speaker = m.group(2).strip()
            if speaker in ("A", "B"):
                labels[line_num] = speaker
    return labels


def main():
    review_path = Path("tools/gold_set_review.txt")
    template_path = Path("tools/gold_set_template.json")
    output_path = Path("tools/gold_set.json")

    if not review_path.exists():
        print(f"Review file not found: {review_path}", file=sys.stderr)
        return 1

    if not template_path.exists():
        print(f"Template not found: {template_path}", file=sys.stderr)
        return 1

    review_text = review_path.read_text(encoding="utf-8")
    labels = parse_review(review_text)

    if not labels:
        print("No labels found in review file. Fill in [A] or [B] in the brackets.")
        return 1

    template = json.loads(template_path.read_text(encoding="utf-8"))

    updated = 0
    for entry in template["lines"]:
        if entry["line"] in labels:
            entry["speaker"] = labels[entry["line"]]
            if not entry.get("confidence"):
                entry["confidence"] = "manual"
            updated += 1

    output_path.write_text(
        json.dumps(template, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Updated {updated} labels from {len(labels)} entries in review file.")
    print(f"Output: {output_path}")
    print(f"\nNext: python -X utf8 tools/evaluate_diarization.py {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
