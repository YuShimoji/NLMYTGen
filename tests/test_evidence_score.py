"""H-04 Evidence richness score テスト."""

from src.pipeline.evidence_score import score_evidence, CATEGORIES


def _brief(**overrides):
    base = {
        "video_id": "test",
        "required_evidence": [],
        "missing_or_weak_evidence": [],
    }
    base.update(overrides)
    return base


def _full_scores(value=2):
    return {c: value for c in CATEGORIES}


class TestScoring:
    def test_perfect_score(self):
        r = score_evidence(_brief(), _full_scores(3))
        assert r.total_score == 100
        assert r.band == "strong"

    def test_zero_score(self):
        r = score_evidence(_brief(), _full_scores(0))
        assert r.total_score == 0
        assert r.band == "high_drift_risk"

    def test_mid_score(self):
        r = score_evidence(_brief(), _full_scores(2))
        assert 60 <= r.total_score <= 70
        assert r.band == "acceptable"

    def test_band_boundaries(self):
        r80 = score_evidence(_brief(), {c: 3 for c in CATEGORIES})
        assert r80.band == "strong"
        # All 1s should be around 33
        r_low = score_evidence(_brief(), _full_scores(1))
        assert r_low.band in ("weak", "high_drift_risk")


class TestWarnings:
    def test_no_number_warning(self):
        scores = _full_scores(2)
        scores["number"] = 0
        r = score_evidence(_brief(), scores)
        assert "EVIDENCE_NO_NUMBER" in r.warnings

    def test_no_anecdote_warning(self):
        scores = _full_scores(2)
        scores["anecdote"] = 0
        r = score_evidence(_brief(), scores)
        assert "EVIDENCE_NO_ANECDOTE" in r.warnings

    def test_promise_gap_warning(self):
        scores = _full_scores(2)
        scores["promise_payoff"] = 1
        r = score_evidence(_brief(), scores)
        assert "EVIDENCE_PROMISE_GAP" in r.warnings

    def test_required_missing(self):
        brief = _brief(required_evidence=[
            {"kind": "number", "value": "71.4%", "status": "missing",
             "why_it_matters": "test", "must_surface_in": ["body"]},
        ])
        r = score_evidence(brief, _full_scores(2))
        assert "EVIDENCE_REQUIRED_MISSING" in r.warnings
        assert any("71.4%" in s for s in r.missing_or_weak_evidence)

    def test_required_weak(self):
        brief = _brief(required_evidence=[
            {"kind": "anecdote", "value": "worker story", "status": "weak",
             "why_it_matters": "test", "must_surface_in": ["body"]},
        ])
        r = score_evidence(brief, _full_scores(2))
        assert "EVIDENCE_REQUIRED_WEAK" in r.warnings

    def test_abstract_drift(self):
        scores = {c: 3 for c in CATEGORIES}
        scores["number"] = 0
        scores["anecdote"] = 0
        scores["case"] = 1
        r = score_evidence(_brief(), scores)
        assert "EVIDENCE_ABSTRACT_DRIFT" in r.warnings


class TestBestSupports:
    def test_confirmed_evidence_in_best_supports(self):
        brief = _brief(required_evidence=[
            {"kind": "number", "value": "71.4%", "status": "confirmed",
             "why_it_matters": "", "must_surface_in": []},
            {"kind": "number", "value": "19億ドル", "status": "confirmed",
             "why_it_matters": "", "must_surface_in": []},
            {"kind": "anecdote", "value": "story", "status": "missing",
             "why_it_matters": "", "must_surface_in": []},
        ])
        r = score_evidence(brief, _full_scores(2))
        assert "71.4%" in r.best_supports
        assert "19億ドル" in r.best_supports
        assert "story" not in r.best_supports
