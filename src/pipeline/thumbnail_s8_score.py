"""S-8 Thumbnail one-sheet score (automation probe).

手動評価スコア (0-3) から、S-8 の PASS/NEEDS_FIX 判定を補助する。
画像生成や画像解析は行わず、運用記録の機械化のみを担当する。
"""

from __future__ import annotations

from dataclasses import dataclass, field

CATEGORIES = (
    "single_claim",
    "specificity",
    "title_alignment",
    "mobile_readability",
)

WEIGHTS = {
    "single_claim": 30,
    "specificity": 30,
    "title_alignment": 25,
    "mobile_readability": 15,
}

BANDS = [
    (80, "pass"),
    (60, "needs_fix"),
    (0, "high_risk"),
]


@dataclass
class ThumbnailS8ScoreResult:
    """S-8 scoring result."""

    score_version: str = "0.1"
    run_id: str = ""
    video_slug: str = ""
    output_file: str = ""
    total_score: int = 0
    band: str = ""
    category_scores: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    recommended_repairs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "score_version": self.score_version,
            "run_id": self.run_id,
            "video_slug": self.video_slug,
            "output_file": self.output_file,
            "total_score": self.total_score,
            "band": self.band,
            "category_scores": self.category_scores,
            "warnings": self.warnings,
            "recommended_repairs": self.recommended_repairs,
        }


def _compute_total(scores: dict[str, int]) -> int:
    max_total = sum(WEIGHTS[c] * 3 for c in CATEGORIES)
    actual = sum(WEIGHTS[c] * scores.get(c, 0) for c in CATEGORIES)
    return round(actual / max_total * 100)


def _get_band(total: int) -> str:
    for threshold, label in BANDS:
        if total >= threshold:
            return label
    return "high_risk"


def score_thumbnail_s8(payload: dict, category_scores: dict[str, int]) -> ThumbnailS8ScoreResult:
    """S-8 score を計算する.

    Parameters
    ----------
    payload : dict
        run metadata. 代表キー: run_id, video_slug, output_file
    category_scores : dict[str, int]
        manual score per category (0-3)
    """
    result = ThumbnailS8ScoreResult()
    result.run_id = str(payload.get("run_id", ""))
    result.video_slug = str(payload.get("video_slug", ""))
    result.output_file = str(payload.get("output_file", ""))
    result.category_scores = {c: int(category_scores.get(c, 0)) for c in CATEGORIES}

    result.total_score = _compute_total(result.category_scores)
    result.band = _get_band(result.total_score)

    scores = result.category_scores
    if scores.get("single_claim", 0) <= 1:
        result.warnings.append("THUMB_SINGLE_CLAIM_WEAK")
        result.recommended_repairs.append("reduce to one primary claim for small-screen readability")
    if scores.get("specificity", 0) <= 1:
        result.warnings.append("THUMB_SPECIFICITY_WEAK")
        result.recommended_repairs.append("add one concrete anchor (number, proper noun, or dated fact)")
    if scores.get("title_alignment", 0) <= 1:
        result.warnings.append("THUMB_TITLE_ALIGNMENT_GAP")
        result.recommended_repairs.append("align thumbnail promise with title/script core message")
    if scores.get("mobile_readability", 0) <= 1:
        result.warnings.append("THUMB_MOBILE_READABILITY_RISK")
        result.recommended_repairs.append("increase contrast and simplify text layout")

    # Guardrail: score can look acceptable while core contract still fails.
    if result.total_score >= 60 and (
        scores.get("single_claim", 0) == 0 or scores.get("title_alignment", 0) == 0
    ):
        result.warnings.append("THUMB_CONTRACT_BROKEN")
        result.recommended_repairs.append("fix single claim and alignment before accepting this thumbnail")

    result.warnings = list(dict.fromkeys(result.warnings))
    return result
