from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from src.pipeline.baseball_visual_data import (
    SCHEMA_VERSION,
    BaseballVisualDataError,
    assert_valid_baseball_visual_data,
    build_baseball_visual_data,
    validate_baseball_visual_data,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
VISUAL_DATA_SAMPLE = (
    REPO_ROOT
    / "lanes"
    / "sports_news"
    / "examples"
    / "baseball_pitch_event_visual_data_sample.json"
)
VISUAL_DATA_SCHEMA = (
    REPO_ROOT
    / "lanes"
    / "sports_news"
    / "schemas"
    / "baseball_visual_data.schema.json"
)


def _sample_episode() -> dict:
    return {
        "episode": {
            "id": "baseball_pitch_event_sample",
            "type": "sports_news",
            "league": "SAMPLE",
            "sport": "baseball",
            "event_date": "sample-date",
            "title_angle": "終盤の一球で流れが変わるサンプル打席",
            "visual_mode": "original_broadcast_data_cards",
        },
        "game_context": {
            "team_home": {"code": "FAL", "name": "Sample Falcons"},
            "team_away": {"code": "EAG", "name": "Sample Eagles"},
            "score": {"home": 4, "away": 3},
            "inning": 7,
            "top_bottom": "top",
        },
        "at_bat": {
            "pitcher": {
                "name": "Sample Pitcher",
                "throws": "R",
                "era": 2.18,
                "today_pitch_count": 87,
                "today_strikeouts": 7,
            },
            "batter": {
                "name": "Sample Batter",
                "bats": "L",
                "avg": 0.302,
                "ops": 0.891,
                "today_result": "single, strikeout, groundout",
            },
            "count": {
                "before_pitch": {"balls": 2, "strikes": 2, "outs": 1},
                "pitch_number_in_plate_appearance": 5,
            },
            "previous_pitch": {
                "pitch_type": "FF",
                "velocity_kmh": 155,
                "result": "Foul",
                "zone": "upper_outer",
            },
            "pitch_event": {
                "pitch_type": "SL",
                "velocity_kmh": 140,
                "result": "Strike",
                "zone": "low_outer",
                "intended_zone": "low_outer",
                "actual_zone": "low_outer",
                "interpretation": "前球の速球から外角低めのスライダーへ緩急をつけた",
            },
        },
        "source_ledger": {
            "sources": [
                {
                    "id": "src_boxscore_sample",
                    "url": "sample://boxscore/baseball_pitch_event_sample",
                }
            ]
        },
        "visual_plan": {
            "ambient_backdrop": {
                "id": "ballpark_night_grid",
                "role": "Atmosphere-only card backdrop; not evidence for the pitch event.",
                "provenance": "BaseballInfoGraphics/assets/ambient/LICENSE.csv",
                "usage_stage": "design_preview",
                "note": (
                    "Repo-generated abstract SVG preview; real episode backdrops "
                    "should keep provenance records before asset ingest."
                ),
            },
            "scenes": [
                {
                    "id": "scene_pitch_event",
                    "card_type": "pitch_event_card",
                    "claim": "前球155km/h FFから140km/h SLへ緩急",
                    "data_refs": ["fact_pitch_sequence", "num_velocity_delta"],
                },
                {
                    "id": "scene_watch_point",
                    "card_type": "watch_point_card",
                    "claim": "次に見るべきは外角スライダーの見極め",
                    "data_refs": ["uncertain_intent"],
                },
            ],
        },
    }


def test_schema_file_declares_bn02_visual_data_contract() -> None:
    schema = json.loads(VISUAL_DATA_SCHEMA.read_text(encoding="utf-8"))

    assert schema["properties"]["schema_version"]["const"] == SCHEMA_VERSION
    assert schema["required"] == [
        "schema_version",
        "visual",
        "meta",
        "teams",
        "score",
        "atBat",
        "zone",
    ]
    assert schema["properties"]["atBat"]["properties"]["pitches"]["minItems"] == 2


def test_build_baseball_visual_data_matches_lane_sample_fixture() -> None:
    actual = build_baseball_visual_data(_sample_episode())
    expected = json.loads(VISUAL_DATA_SAMPLE.read_text(encoding="utf-8"))

    assert actual == expected
    assert validate_baseball_visual_data(actual) == []
    assert actual["visual"]["ambientBackdrop"]["usageStage"] == "design_preview"
    assert actual["atBat"]["currentPitchIndex"] == 1


def test_fixture_is_valid_baseball_visual_data() -> None:
    fixture = json.loads(VISUAL_DATA_SAMPLE.read_text(encoding="utf-8"))

    assert assert_valid_baseball_visual_data(fixture) is fixture


def test_build_fails_when_previous_pitch_is_missing() -> None:
    episode = _sample_episode()
    del episode["at_bat"]["previous_pitch"]

    with pytest.raises(BaseballVisualDataError, match="previous_pitch"):
        build_baseball_visual_data(episode)


def test_validation_rejects_pitch_event_without_two_pitch_comparison() -> None:
    visual_data = build_baseball_visual_data(_sample_episode())
    visual_data["atBat"]["pitches"] = visual_data["atBat"]["pitches"][:1]

    assert "atBat.pitches must contain at least two pitches" in validate_baseball_visual_data(visual_data)


def test_validation_rejects_score_line_total_contradiction() -> None:
    visual_data = copy.deepcopy(build_baseball_visual_data(_sample_episode()))
    visual_data["score"]["lineScore"] = {
        "homeTotal": {"r": 99},
        "awayTotal": {"r": 3},
    }

    assert (
        "score.lineScore.homeTotal.r does not match score.home"
        in validate_baseball_visual_data(visual_data)
    )
