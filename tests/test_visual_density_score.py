"""H-03 Visual density score テスト."""

from src.pipeline.visual_density_score import score_visual_density, CATEGORIES


def _brief(**overrides):
    base = {
        "video_id": "test",
        "required_evidence": [],
        "consumer_hints": {},
    }
    base.update(overrides)
    return base


def _full_scores(value=2):
    return {c: value for c in CATEGORIES}


class TestScoring:
    def test_perfect_score(self):
        r = score_visual_density(_brief(), _full_scores(3))
        assert r.total_score == 100
        assert r.band == "strong"

    def test_zero_score(self):
        r = score_visual_density(_brief(), _full_scores(0))
        assert r.total_score == 0
        assert r.band == "high_stagnation_risk"

    def test_mid_score(self):
        r = score_visual_density(_brief(), _full_scores(2))
        assert 60 <= r.total_score <= 70
        assert r.band == "acceptable"


class TestWarnings:
    def test_stagnation_risk_warning(self):
        scores = _full_scores(2)
        scores["stagnation_risk"] = 1
        r = score_visual_density(_brief(), scores)
        assert "VISUAL_SINGLE_BACKGROUND_RISK" in r.warnings

    def test_data_promise_unpaid(self):
        brief = _brief(required_evidence=[
            {"kind": "number", "value": "71.4%", "status": "confirmed",
             "why_it_matters": "", "must_surface_in": ["thumbnail"]},
        ])
        scores = _full_scores(2)
        scores["information_embedding"] = 1
        r = score_visual_density(brief, scores)
        assert "VISUAL_DATA_PROMISE_UNPAID" in r.warnings

    def test_symbol_missing(self):
        scores = _full_scores(2)
        scores["symbolic_asset"] = 0
        r = score_visual_density(_brief(), scores)
        assert "VISUAL_SYMBOL_MISSING" in r.warnings

    def test_pattern_repeat(self):
        scores = _full_scores(2)
        scores["pattern_balance"] = 1
        r = score_visual_density(_brief(), scores)
        assert "VISUAL_PATTERN_REPEAT" in r.warnings

    def test_tempo_flat(self):
        scores = _full_scores(2)
        scores["tempo_shift"] = 0
        r = score_visual_density(_brief(), scores)
        assert "VISUAL_TEMPO_FLAT" in r.warnings

    def test_contrast_missing(self):
        brief = _brief(consumer_hints={"for_h03": "対比が足りないか見る"})
        scores = _full_scores(2)
        scores["pattern_balance"] = 1
        r = score_visual_density(brief, scores)
        assert "VISUAL_CONTRAST_MISSING" in r.warnings


class TestBestSupports:
    def test_thumbnail_evidence_in_supports(self):
        brief = _brief(required_evidence=[
            {"kind": "number", "value": "71.4%", "status": "confirmed",
             "why_it_matters": "", "must_surface_in": ["thumbnail"]},
            {"kind": "anecdote", "value": "story", "status": "confirmed",
             "why_it_matters": "", "must_surface_in": ["body"]},
        ])
        r = score_visual_density(brief, _full_scores(2))
        assert "71.4%" in r.best_supports
        assert "story" not in r.best_supports
