"""Build and validate BaseballInfoGraphics visual data.

This module is intentionally dict-in/dict-out. The sports_news lane may store
examples as YAML, but parsing files is kept outside this contract so BN-02 does
not add dependencies or bless a YAML loader.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


SCHEMA_VERSION = "baseball_visual_data.v1"


class BaseballVisualDataError(ValueError):
    """Raised when sports_news episode data cannot become visual data."""


PITCH_TYPE_JA = {
    "FF": "フォーシーム",
    "SL": "スライダー",
    "CB": "カーブ",
    "SP": "スプリット",
    "CH": "チェンジアップ",
    "CT": "カットボール",
    "SI": "シンカー",
}

RESULT_JA = {
    "Ball": "ボール",
    "Strike": "ストライク",
    "CalledStrike": "見逃しS",
    "SwingingStrike": "空振りS",
    "Foul": "ファウル",
    "InPlay": "打球",
    "In play": "打球",
}

ZONE_COORDS = {
    "upper_outer": {"x": 0.52, "y": -0.58},
    "upper_middle": {"x": 0.0, "y": -0.58},
    "upper_inner": {"x": -0.52, "y": -0.58},
    "middle_outer": {"x": 0.52, "y": 0.0},
    "middle": {"x": 0.0, "y": 0.0},
    "middle_inner": {"x": -0.52, "y": 0.0},
    "low_outer": {"x": -0.55, "y": 0.52},
    "low_middle": {"x": 0.0, "y": 0.52},
    "low_inner": {"x": 0.55, "y": 0.52},
}

DEFAULT_HOME_COLOR = "#22C55E"
DEFAULT_AWAY_COLOR = "#38BDF8"


def build_baseball_visual_data(episode: Mapping[str, Any]) -> dict[str, Any]:
    """Convert a sports_news baseball episode dict into C detailed visual data."""

    if not isinstance(episode, Mapping):
        raise BaseballVisualDataError("episode must be a mapping")

    episode_meta = _required_mapping(episode, "episode")
    game_context = _required_mapping(episode, "game_context")
    at_bat = _required_mapping(episode, "at_bat")
    visual_plan = _required_mapping(episode, "visual_plan")

    team_home = _required_mapping(game_context, "team_home")
    team_away = _required_mapping(game_context, "team_away")
    game_score = _required_mapping(game_context, "score")
    count = _required_mapping(_required_mapping(at_bat, "count"), "before_pitch")
    pitcher = _required_mapping(at_bat, "pitcher")
    batter = _required_mapping(at_bat, "batter")

    previous_pitch = _required_mapping(at_bat, "previous_pitch")
    current_pitch = _required_mapping(at_bat, "pitch_event")
    pitch_number = _positive_int(
        _required_mapping(at_bat, "count").get("pitch_number_in_plate_appearance"),
        "at_bat.count.pitch_number_in_plate_appearance",
        fallback=2,
    )

    scenes = _scene_map(visual_plan.get("scenes", []))
    pitch_claim = _scene_claim(scenes, "pitch_event_card") or str(
        current_pitch.get("interpretation") or "この一球の意味を、スコアとカウントから読む"
    )
    watch_point = _scene_claim(scenes, "watch_point_card") or (
        "次に見るべきは、打者が外角低めを見極められるか"
    )

    visual_data = {
        "schema_version": SCHEMA_VERSION,
        "visual": {
            "eventLabel": _event_label(episode_meta),
            "claim": pitch_claim,
            "sourceLabel": _source_label(episode),
            "watchPoint": watch_point,
            "ambientBackdrop": _ambient_backdrop(visual_plan.get("ambient_backdrop")),
        },
        "meta": {
            "league": str(episode_meta.get("league", "")),
            "venue": str(game_context.get("venue", "sample venue")),
            "date": str(episode_meta.get("event_date", "")),
            "weather": str(game_context.get("weather", "unknown")),
            "attendance": str(game_context.get("attendance", "unknown")),
            "sourceEpisodeId": str(episode_meta.get("id", "")),
        },
        "teams": {
            "home": _team_payload(team_home, DEFAULT_HOME_COLOR),
            "away": _team_payload(team_away, DEFAULT_AWAY_COLOR),
        },
        "score": {
            "home": _int_value(game_score.get("home"), "game_context.score.home"),
            "away": _int_value(game_score.get("away"), "game_context.score.away"),
            "inning": _int_value(game_context.get("inning"), "game_context.inning"),
            "half": str(game_context.get("top_bottom", "")),
            "outs": _int_value(count.get("outs"), "at_bat.count.before_pitch.outs"),
            "balls": _int_value(count.get("balls"), "at_bat.count.before_pitch.balls"),
            "strikes": _int_value(count.get("strikes"), "at_bat.count.before_pitch.strikes"),
            "bases": _bases_payload(at_bat.get("bases") or count.get("bases")),
        },
        "atBat": {
            "pitcher": _pitcher_payload(pitcher),
            "batter": _batter_payload(batter),
            "pitches": [
                _pitch_payload(previous_pitch, max(1, pitch_number - 1), _previous_pitch_claim(previous_pitch)),
                _pitch_payload(current_pitch, pitch_number, pitch_claim),
            ],
            "currentPitchIndex": 1,
        },
        "zone": {
            "halfWidth": 0.83,
            "top": -1.0,
            "bottom": 1.0,
        },
    }

    assert_valid_baseball_visual_data(visual_data)
    return visual_data


def validate_baseball_visual_data(data: Mapping[str, Any]) -> list[str]:
    """Return contract errors for BaseballInfoGraphics visual data."""

    errors: list[str] = []
    if not isinstance(data, Mapping):
        return ["visual data must be a mapping"]

    required_top = ("schema_version", "visual", "meta", "teams", "score", "atBat", "zone")
    for key in required_top:
        if key not in data:
            errors.append(f"missing top-level field: {key}")

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")

    teams = data.get("teams")
    if isinstance(teams, Mapping):
        for side in ("home", "away"):
            team = teams.get(side)
            if not isinstance(team, Mapping):
                errors.append(f"teams.{side} must be an object")
                continue
            if not str(team.get("code", "")).strip():
                errors.append(f"teams.{side}.code is required")
            if not str(team.get("name", "")).strip():
                errors.append(f"teams.{side}.name is required")
    elif "teams" in data:
        errors.append("teams must be an object")

    score = data.get("score")
    if isinstance(score, Mapping):
        for key in ("home", "away", "inning", "outs", "balls", "strikes"):
            if not isinstance(score.get(key), int):
                errors.append(f"score.{key} must be an integer")
        if score.get("half") not in {"top", "bottom"}:
            errors.append("score.half must be top or bottom")
        _check_count_bounds(score, errors)
        line_score = score.get("lineScore")
        if isinstance(line_score, Mapping):
            _check_line_score_total(score, line_score, "home", errors)
            _check_line_score_total(score, line_score, "away", errors)
    elif "score" in data:
        errors.append("score must be an object")

    at_bat = data.get("atBat")
    if isinstance(at_bat, Mapping):
        pitches = at_bat.get("pitches")
        if not isinstance(pitches, list):
            errors.append("atBat.pitches must be an array")
        elif len(pitches) < 2:
            errors.append("atBat.pitches must contain at least two pitches")
        else:
            for index, pitch in enumerate(pitches):
                if not isinstance(pitch, Mapping):
                    errors.append(f"atBat.pitches[{index}] must be an object")
                    continue
                if not str(pitch.get("type", "")).strip():
                    errors.append(f"atBat.pitches[{index}].type is required")
                if not isinstance(pitch.get("kmh"), (int, float)):
                    errors.append(f"atBat.pitches[{index}].kmh must be numeric")
                if not str(pitch.get("result", "")).strip():
                    errors.append(f"atBat.pitches[{index}].result is required")
    elif "atBat" in data:
        errors.append("atBat must be an object")

    visual = data.get("visual")
    if isinstance(visual, Mapping):
        if not str(visual.get("claim", "")).strip():
            errors.append("visual.claim is required")
        ambient = visual.get("ambientBackdrop")
        if isinstance(ambient, Mapping) and ambient.get("imageUrl") and not ambient.get("provenance"):
            errors.append("visual.ambientBackdrop.provenance is required when imageUrl is set")
    elif "visual" in data:
        errors.append("visual must be an object")

    return errors


def assert_valid_baseball_visual_data(data: Mapping[str, Any]) -> Mapping[str, Any]:
    """Raise when visual data fails the BN-02 contract."""

    errors = validate_baseball_visual_data(data)
    if errors:
        raise BaseballVisualDataError("; ".join(errors))
    return data


def _required_mapping(parent: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = parent.get(key)
    if not isinstance(value, Mapping):
        raise BaseballVisualDataError(f"{key} must be present and must be a mapping")
    return value


def _int_value(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise BaseballVisualDataError(f"{path} must be an integer")
    return value


def _positive_int(value: Any, path: str, fallback: int) -> int:
    if value is None:
        return fallback
    number = _int_value(value, path)
    if number <= 0:
        raise BaseballVisualDataError(f"{path} must be greater than 0")
    return number


def _team_payload(team: Mapping[str, Any], primary: str) -> dict[str, Any]:
    code = str(team.get("code", "")).strip()
    name = str(team.get("name", "")).strip()
    if not code or not name:
        raise BaseballVisualDataError("team code and name are required")
    return {
        "code": code,
        "name": name,
        "shortName": _short_name(name),
        "primary": primary,
        "secondary": "#0F172A",
        "logo": code,
    }


def _short_name(name: str) -> str:
    parts = [part for part in name.replace("_", " ").split(" ") if part]
    return parts[-1] if parts else name


def _pitcher_payload(player: Mapping[str, Any]) -> dict[str, Any]:
    name = str(player.get("name", "")).strip()
    if not name:
        raise BaseballVisualDataError("at_bat.pitcher.name is required")
    return {
        "id": _slug(name),
        "name": name,
        "nameEn": name,
        "number": player.get("number"),
        "throws": player.get("throws", "—"),
        "season": {
            "era": player.get("era", player.get("season", {}).get("era") if isinstance(player.get("season"), Mapping) else None),
        },
        "today": {
            "ip": player.get("today_ip", "—"),
            "h": player.get("today_hits"),
            "r": player.get("today_runs"),
            "er": player.get("today_earned_runs"),
            "bb": player.get("today_walks"),
            "k": player.get("today_strikeouts"),
            "pc": player.get("today_pitch_count"),
        },
    }


def _batter_payload(player: Mapping[str, Any]) -> dict[str, Any]:
    name = str(player.get("name", "")).strip()
    if not name:
        raise BaseballVisualDataError("at_bat.batter.name is required")
    today = _parse_batter_today(str(player.get("today_result", "")))
    return {
        "id": _slug(name),
        "name": name,
        "nameEn": name,
        "number": player.get("number"),
        "bats": player.get("bats", "—"),
        "season": {
            "avg": player.get("avg"),
            "ops": player.get("ops"),
            "hr": player.get("hr"),
            "rbi": player.get("rbi"),
        },
        "today": today,
        "vsP": {
            "ab": player.get("vs_pitcher_ab", 0),
            "h": player.get("vs_pitcher_h", 0),
            "hr": player.get("vs_pitcher_hr", 0),
            "k": player.get("vs_pitcher_k", 0),
        },
    }


def _parse_batter_today(raw: str) -> dict[str, int]:
    tokens = [token.strip().lower() for token in raw.split(",") if token.strip()]
    hits = sum(1 for token in tokens if token in {"single", "double", "triple", "home run", "homer", "hit"})
    strikeouts = sum(1 for token in tokens if "strikeout" in token or token == "k")
    walks = sum(1 for token in tokens if token in {"walk", "bb"})
    homers = sum(1 for token in tokens if token in {"home run", "homer"})
    at_bats = max(0, len(tokens) - walks)
    return {"ab": at_bats, "h": hits, "hr": homers, "rbi": 0, "k": strikeouts, "bb": walks}


def _pitch_payload(pitch: Mapping[str, Any], number: int, claim: str) -> dict[str, Any]:
    pitch_type = str(pitch.get("pitch_type", "")).strip()
    if not pitch_type:
        raise BaseballVisualDataError("pitch.pitch_type is required")
    velocity = pitch.get("velocity_kmh")
    if not isinstance(velocity, (int, float)):
        raise BaseballVisualDataError("pitch.velocity_kmh must be numeric")
    zone = str(pitch.get("zone", "")).strip()
    coords = deepcopy(ZONE_COORDS.get(zone, ZONE_COORDS["middle"]))
    return {
        "num": number,
        "type": pitch_type,
        "typeJa": PITCH_TYPE_JA.get(pitch_type, pitch_type),
        "mph": round(float(velocity) / 1.609344, 1),
        "kmh": velocity,
        "x": coords["x"],
        "y": coords["y"],
        "result": str(pitch.get("result", "")),
        "resultJa": RESULT_JA.get(str(pitch.get("result", "")), str(pitch.get("result", ""))),
        "zone": zone,
        "intendedZone": pitch.get("intended_zone"),
        "actualZone": pitch.get("actual_zone"),
        "claim": claim,
    }


def _previous_pitch_claim(pitch: Mapping[str, Any]) -> str:
    pitch_type = str(pitch.get("pitch_type", "—"))
    velocity = pitch.get("velocity_kmh", "—")
    result = RESULT_JA.get(str(pitch.get("result", "")), str(pitch.get("result", "")))
    return f"前球は{velocity}km/hの{pitch_type}で{result}"


def _scene_map(raw_scenes: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(raw_scenes, list):
        raise BaseballVisualDataError("visual_plan.scenes must be an array")
    result: dict[str, dict[str, Any]] = {}
    for scene in raw_scenes:
        if isinstance(scene, Mapping):
            result[str(scene.get("card_type", ""))] = dict(scene)
    return result


def _scene_claim(scenes: Mapping[str, Mapping[str, Any]], card_type: str) -> str | None:
    scene = scenes.get(card_type)
    if not scene:
        return None
    claim = scene.get("claim")
    return str(claim) if claim else None


def _event_label(episode_meta: Mapping[str, Any]) -> str:
    league = str(episode_meta.get("league", "SAMPLE")).upper()
    return f"PITCH EVENT · {league} DATA"


def _source_label(episode: Mapping[str, Any]) -> str:
    sources = episode.get("source_ledger", {}).get("sources", []) if isinstance(episode.get("source_ledger"), Mapping) else []
    sample_only = any(isinstance(source, Mapping) and str(source.get("url", "")).startswith("sample://") for source in sources)
    return (
        "SAMPLE INFOGRAPHIC · PROVENANCE-GATED VISUALS"
        if sample_only
        else "INFOGRAPHIC · PROVENANCE-GATED VISUALS"
    )


def _ambient_backdrop(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        return {
            "kind": "css_grid",
            "label": "CSS grid fallback",
            "imageUrl": "",
            "provenance": "none",
            "usageStage": "design_preview",
            "note": "No ambient backdrop image supplied.",
        }
    backdrop_id = str(raw.get("id", "")).strip()
    image_name = backdrop_id.replace("_", "-")
    return {
        "kind": "repo_generated_svg" if backdrop_id else "css_grid",
        "label": backdrop_id or "CSS grid fallback",
        "imageUrl": f"assets/ambient/{image_name}.svg" if backdrop_id else "",
        "provenance": str(raw.get("provenance", "")),
        "usageStage": str(raw.get("usage_stage", "design_preview")),
        "note": str(raw.get("note", raw.get("role", ""))),
    }


def _bases_payload(raw: Any) -> dict[str, bool]:
    if not isinstance(raw, Mapping):
        return {"first": False, "second": False, "third": False}
    return {
        "first": bool(raw.get("first", False)),
        "second": bool(raw.get("second", False)),
        "third": bool(raw.get("third", False)),
    }


def _check_count_bounds(score: Mapping[str, Any], errors: list[str]) -> None:
    if isinstance(score.get("balls"), int) and not 0 <= score["balls"] <= 3:
        errors.append("score.balls must be between 0 and 3")
    if isinstance(score.get("strikes"), int) and not 0 <= score["strikes"] <= 2:
        errors.append("score.strikes must be between 0 and 2 before the pitch")
    if isinstance(score.get("outs"), int) and not 0 <= score["outs"] <= 2:
        errors.append("score.outs must be between 0 and 2 before the play")


def _check_line_score_total(
    score: Mapping[str, Any],
    line_score: Mapping[str, Any],
    side: str,
    errors: list[str],
) -> None:
    total_key = f"{side}Total"
    total = line_score.get(total_key)
    if not isinstance(total, Mapping) or "r" not in total:
        return
    if total["r"] != score.get(side):
        errors.append(f"score.lineScore.{total_key}.r does not match score.{side}")


def _slug(value: str) -> str:
    return value.strip().lower().replace(" ", "_") or "unknown"
