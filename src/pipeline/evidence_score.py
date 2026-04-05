"""H-04 Evidence richness score.

H-01 brief の required_evidence と手動カテゴリスコアから
total score / band / warnings / repair suggestions を算出する。
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

CATEGORIES = ("number", "named_entity", "anecdote", "case", "study", "freshness", "promise_payoff")

WEIGHTS = {
    "number": 15,
    "named_entity": 10,
    "anecdote": 15,
    "case": 15,
    "study": 15,
    "freshness": 10,
    "promise_payoff": 20,
}

BANDS = [
    (80, "strong"),
    (60, "acceptable"),
    (40, "weak"),
    (0, "high_drift_risk"),
]


@dataclass
class EvidenceScoreResult:
    """H-04 scoring result."""

    score_version: str = "0.1"
    video_id: str = ""
    total_score: int = 0
    band: str = ""
    category_scores: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    missing_or_weak_evidence: list[str] = field(default_factory=list)
    best_supports: list[str] = field(default_factory=list)
    recommended_repairs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "score_version": self.score_version,
            "video_id": self.video_id,
            "total_score": self.total_score,
            "band": self.band,
            "category_scores": self.category_scores,
            "warnings": self.warnings,
            "missing_or_weak_evidence": self.missing_or_weak_evidence,
            "best_supports": self.best_supports,
            "recommended_repairs": self.recommended_repairs,
        }


def _compute_total(scores: dict[str, int]) -> int:
    """Weighted sum normalized to 100."""
    max_total = sum(WEIGHTS[c] * 3 for c in CATEGORIES)
    actual = sum(WEIGHTS.get(c, 0) * scores.get(c, 0) for c in CATEGORIES)
    return round(actual / max_total * 100)


def _get_band(total: int) -> str:
    for threshold, label in BANDS:
        if total >= threshold:
            return label
    return "high_drift_risk"


def score_evidence(
    brief: dict,
    category_scores: dict[str, int],
) -> EvidenceScoreResult:
    """H-04 scoring.

    Parameters
    ----------
    brief : dict
        H-01 Packaging Orchestrator brief (parsed JSON or dict).
        Uses: video_id, required_evidence, missing_or_weak_evidence,
              title_promise, thumbnail_promise
    category_scores : dict[str, int]
        Manual or LLM-assigned scores per category (0-3).
        Keys should be from CATEGORIES.
    """
    result = EvidenceScoreResult()
    result.video_id = brief.get("video_id", "")
    result.category_scores = {c: category_scores.get(c, 0) for c in CATEGORIES}

    # Total + band
    result.total_score = _compute_total(result.category_scores)
    result.band = _get_band(result.total_score)

    # Best supports from required_evidence
    for item in brief.get("required_evidence", []):
        if isinstance(item, dict) and item.get("status") == "confirmed":
            val = item.get("value", "")
            if val:
                result.best_supports.append(val)

    # Warnings from brief required_evidence
    for item in brief.get("required_evidence", []):
        if not isinstance(item, dict):
            continue
        status = item.get("status", "")
        val = item.get("value", "")
        if status == "missing":
            result.warnings.append("EVIDENCE_REQUIRED_MISSING")
            result.missing_or_weak_evidence.append(f"missing: {val}")
        elif status == "weak":
            result.warnings.append("EVIDENCE_REQUIRED_WEAK")
            result.missing_or_weak_evidence.append(f"weak: {val}")

    # Warnings from category scores
    scores = result.category_scores
    if scores.get("number", 0) == 0:
        result.warnings.append("EVIDENCE_NO_NUMBER")
        result.recommended_repairs.append("add at least one concrete number")
    if scores.get("anecdote", 0) == 0:
        result.warnings.append("EVIDENCE_NO_ANECDOTE")
        result.recommended_repairs.append("add one concrete worker/person episode")
    if scores.get("case", 0) == 0:
        result.warnings.append("EVIDENCE_NO_CASE")
        result.recommended_repairs.append("add one concrete example or incident")
    if scores.get("study", 0) == 0:
        result.warnings.append("EVIDENCE_NO_STUDY")
        result.recommended_repairs.append("add expert framing or research reference")
    if scores.get("freshness", 0) == 0:
        result.warnings.append("EVIDENCE_FRESHNESS_UNCLEAR")
        result.recommended_repairs.append("surface a time anchor or recency marker")
    if scores.get("promise_payoff", 0) <= 1:
        result.warnings.append("EVIDENCE_PROMISE_GAP")
        result.recommended_repairs.append(
            "connect the strongest evidence to the title/thumbnail promise more directly"
        )

    # Abstract drift: high total but concrete categories are weak
    concrete_cats = ("number", "anecdote", "case")
    concrete_avg = sum(scores.get(c, 0) for c in concrete_cats) / len(concrete_cats)
    if result.total_score >= 60 and concrete_avg < 1.5:
        result.warnings.append("EVIDENCE_ABSTRACT_DRIFT")
        result.recommended_repairs.append(
            "total is inflated by general categories while concrete anchors remain weak"
        )

    # Deduplicate warnings
    result.warnings = list(dict.fromkeys(result.warnings))

    # missing_or_weak from brief
    for item in brief.get("missing_or_weak_evidence", []):
        if isinstance(item, str) and item not in result.missing_or_weak_evidence:
            result.missing_or_weak_evidence.append(item)

    return result


def load_brief(path: str | Path) -> dict:
    """Load an H-01 brief from JSON or Markdown.

    Supports:
    - Pure JSON file
    - Markdown with embedded ```json block
    - Markdown with YAML-like `- key: value` lines and ## sections
    """
    text = Path(path).read_text(encoding="utf-8")
    # Try JSON first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Try to find JSON block in Markdown
    import re
    match = re.search(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    # Parse Markdown brief format (- key: value + ## sections)
    return _parse_markdown_brief(text)


def _parse_markdown_brief(text: str) -> dict:
    """Parse Markdown brief with `- key: value` pairs and `## section` lists."""
    import re
    result: dict = {}
    current_section: str | None = None
    current_list: list = []

    for line in text.splitlines():
        stripped = line.strip()

        # ## section header
        section_match = re.match(r"^##\s+(\S+)", stripped)
        if section_match:
            if current_section and current_list:
                result[current_section] = current_list
            current_section = section_match.group(1)
            current_list = []
            continue

        # Top-level `- key: value`
        kv_match = re.match(r"^-\s+(\S+):\s*(.+)$", stripped)
        if kv_match and current_section is None:
            key = kv_match.group(1)
            value = kv_match.group(2).strip()
            # Try boolean/number
            if value.lower() == "true":
                result[key] = True
            elif value.lower() == "false":
                result[key] = False
            else:
                result[key] = value
            continue

        # Section-level list items
        if current_section is not None:
            item_match = re.match(r"^-\s+(.+)$", stripped)
            if item_match:
                item_text = item_match.group(1).strip()
                # Check if it's a key: value within section (for required_evidence etc.)
                sub_kv = re.match(r"^(\S+):\s*(.+)$", item_text)
                if sub_kv:
                    # Start new dict item or add to current
                    if current_list and isinstance(current_list[-1], dict):
                        key = sub_kv.group(1)
                        if key in current_list[-1]:
                            # New item
                            current_list.append({key: sub_kv.group(2).strip()})
                        else:
                            current_list[-1][key] = sub_kv.group(2).strip()
                    else:
                        current_list.append({sub_kv.group(1): sub_kv.group(2).strip()})
                else:
                    current_list.append(item_text)

    if current_section and current_list:
        result[current_section] = current_list

    # Parse consumer_hints as nested dict
    if "consumer_hints" in result and isinstance(result["consumer_hints"], list):
        hints = {}
        for item in result["consumer_hints"]:
            if isinstance(item, dict):
                hints.update(item)
        result["consumer_hints"] = hints

    return result
