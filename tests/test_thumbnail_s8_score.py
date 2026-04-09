"""Lane E: S-8 thumbnail scoring tests."""

import json

from src.cli.main import main
from src.pipeline.thumbnail_s8_score import CATEGORIES, score_thumbnail_s8


def _payload(**overrides):
    base = {
        "run_id": "lane_e_probe_test",
        "video_slug": "ai_monitoring_labor",
        "output_file": "thumb_ai_monitoring_labor.png",
    }
    base.update(overrides)
    return base


def _full_scores(value=2):
    return {category: value for category in CATEGORIES}


class TestScoring:
    def test_perfect_score(self):
        result = score_thumbnail_s8(_payload(), _full_scores(3))
        assert result.total_score == 100
        assert result.band == "pass"
        assert result.warnings == []

    def test_zero_score(self):
        result = score_thumbnail_s8(_payload(), _full_scores(0))
        assert result.total_score == 0
        assert result.band == "high_risk"

    def test_mid_score_needs_fix(self):
        result = score_thumbnail_s8(_payload(), _full_scores(2))
        assert 60 <= result.total_score <= 70
        assert result.band == "needs_fix"


class TestWarnings:
    def test_single_claim_warning(self):
        scores = _full_scores(2)
        scores["single_claim"] = 1
        result = score_thumbnail_s8(_payload(), scores)
        assert "THUMB_SINGLE_CLAIM_WEAK" in result.warnings

    def test_specificity_warning(self):
        scores = _full_scores(2)
        scores["specificity"] = 0
        result = score_thumbnail_s8(_payload(), scores)
        assert "THUMB_SPECIFICITY_WEAK" in result.warnings

    def test_alignment_warning(self):
        scores = _full_scores(2)
        scores["title_alignment"] = 1
        result = score_thumbnail_s8(_payload(), scores)
        assert "THUMB_TITLE_ALIGNMENT_GAP" in result.warnings

    def test_mobile_readability_warning(self):
        scores = _full_scores(2)
        scores["mobile_readability"] = 1
        result = score_thumbnail_s8(_payload(), scores)
        assert "THUMB_MOBILE_READABILITY_RISK" in result.warnings

    def test_contract_broken_warning(self):
        scores = _full_scores(3)
        scores["single_claim"] = 0
        result = score_thumbnail_s8(_payload(), scores)
        assert "THUMB_CONTRACT_BROKEN" in result.warnings


class TestCli:
    def test_cli_returns_needs_fix_and_json(self, capsys):
        code = main([
            "score-thumbnail-s8",
            "--scores",
            json.dumps(_full_scores(2), ensure_ascii=False),
            "--format",
            "json",
        ])
        out = capsys.readouterr().out
        payload = json.loads(out)
        assert code == 1
        assert payload["band"] == "needs_fix"

    def test_cli_returns_pass(self, capsys):
        code = main([
            "score-thumbnail-s8",
            "--scores",
            json.dumps(_full_scores(3), ensure_ascii=False),
            "--payload",
            json.dumps(_payload(), ensure_ascii=False),
            "--format",
            "json",
        ])
        out = capsys.readouterr().out
        payload = json.loads(out)
        assert code == 0
        assert payload["band"] == "pass"

