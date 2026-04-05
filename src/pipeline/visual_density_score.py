"""H-03 Visual density score.

H-01 brief と手動カテゴリスコアから
total score / band / warnings / repair suggestions を算出する。
"""

from __future__ import annotations

from dataclasses import dataclass, field

CATEGORIES = (
    "scene_variety",
    "information_embedding",
    "symbolic_asset",
    "tempo_shift",
    "pattern_balance",
    "stagnation_risk",
    "promise_visual_payoff",
)

WEIGHTS = {
    "scene_variety": 15,
    "information_embedding": 15,
    "symbolic_asset": 10,
    "tempo_shift": 10,
    "pattern_balance": 15,
    "stagnation_risk": 15,
    "promise_visual_payoff": 20,
}

BANDS = [
    (80, "strong"),
    (60, "acceptable"),
    (40, "weak"),
    (0, "high_stagnation_risk"),
]


@dataclass
class VisualDensityResult:
    """H-03 scoring result."""

    score_version: str = "0.1"
    video_id: str = ""
    total_score: int = 0
    band: str = ""
    category_scores: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    stagnation_points: list[str] = field(default_factory=list)
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
            "stagnation_points": self.stagnation_points,
            "best_supports": self.best_supports,
            "recommended_repairs": self.recommended_repairs,
        }


def _compute_total(scores: dict[str, int]) -> int:
    max_total = sum(WEIGHTS[c] * 3 for c in CATEGORIES)
    actual = sum(WEIGHTS.get(c, 0) * scores.get(c, 0) for c in CATEGORIES)
    return round(actual / max_total * 100)


def _get_band(total: int) -> str:
    for threshold, label in BANDS:
        if total >= threshold:
            return label
    return "high_stagnation_risk"


def score_visual_density(
    brief: dict,
    category_scores: dict[str, int],
) -> VisualDensityResult:
    """H-03 scoring.

    Parameters
    ----------
    brief : dict
        H-01 Packaging Orchestrator brief.
        Uses: video_id, required_evidence, must_payoff_by_section,
              thumbnail_promise, consumer_hints.for_h03
    category_scores : dict[str, int]
        Manual or LLM-assigned scores per category (0-3).
    """
    result = VisualDensityResult()
    result.video_id = brief.get("video_id", "")
    result.category_scores = {c: category_scores.get(c, 0) for c in CATEGORIES}

    result.total_score = _compute_total(result.category_scores)
    result.band = _get_band(result.total_score)

    scores = result.category_scores

    # Warnings
    if scores.get("stagnation_risk", 0) <= 1:
        result.warnings.append("VISUAL_SINGLE_BACKGROUND_RISK")
        result.recommended_repairs.append("increase background turnover between sections")

    if scores.get("information_embedding", 0) <= 1:
        # Check if packaging relies on data
        evidence = brief.get("required_evidence", [])
        has_number = any(
            isinstance(e, dict) and e.get("kind") == "number"
            for e in evidence
        )
        if has_number:
            result.warnings.append("VISUAL_DATA_PROMISE_UNPAID")
            result.recommended_repairs.append(
                "visualize key numbers as distinct on-screen beats"
            )

    if scores.get("symbolic_asset", 0) == 0:
        result.warnings.append("VISUAL_SYMBOL_MISSING")
        result.recommended_repairs.append("add one memorable symbolic object or motif")

    if scores.get("pattern_balance", 0) <= 1:
        result.warnings.append("VISUAL_PATTERN_REPEAT")
        result.recommended_repairs.append(
            "vary frame logic across sections (anecdote / data / contrast / reflection)"
        )

    if scores.get("tempo_shift", 0) <= 1:
        result.warnings.append("VISUAL_TEMPO_FLAT")
        result.recommended_repairs.append("vary visual pacing across sections")

    if scores.get("promise_visual_payoff", 0) <= 1:
        result.warnings.append("VISUAL_ENDING_TOO_ABSTRACT")
        result.recommended_repairs.append(
            "connect earlier concrete motifs to the ending"
        )

    # Check for contrast topic without visual contrast
    hints = brief.get("consumer_hints", {}).get("for_h03", "")
    if "contrast" in hints.lower() or "対比" in hints:
        if scores.get("pattern_balance", 0) <= 1:
            if "VISUAL_CONTRAST_MISSING" not in result.warnings:
                result.warnings.append("VISUAL_CONTRAST_MISSING")
                result.recommended_repairs.append(
                    "topic implies contrast but visual plan lacks clear before/after frames"
                )

    result.warnings = list(dict.fromkeys(result.warnings))

    # Best supports from brief evidence
    for item in brief.get("required_evidence", []):
        if isinstance(item, dict):
            surfaces = item.get("must_surface_in", [])
            if "thumbnail" in surfaces or "opening" in surfaces:
                val = item.get("value", "")
                if val:
                    result.best_supports.append(val)

    return result
