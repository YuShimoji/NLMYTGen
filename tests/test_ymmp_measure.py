"""ymmp timeline route measurement tests."""

from src.pipeline.ymmp_measure import (
    measure_timeline_routes,
    render_timeline_measurement_text,
    validate_timeline_route_contract,
)


def _wrap(items: list[dict]) -> dict:
    return {
        "Timelines": [{
            "ID": 0,
            "Items": items,
            "LayerSettings": [],
        }],
    }


def test_measure_timeline_routes_collects_candidate_routes():
    ymmp = _wrap([
        {
            "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
            "CharacterName": "marisa",
            "VideoEffects": [
                {
                    "$type": "YukkuriMovieMaker.Plugin.Effects.BounceEffect, YukkuriMovieMaker.Plugin.Effects",
                    "Name": "Bounce",
                }
            ],
            "Transition": {"Name": "Fade", "Duration": 15},
        },
        {
            "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
            "FilePath": "C:/bg.png",
            "X": {"Values": [{"Value": 0.0}]},
            "Y": {"Values": [{"Value": 0.0}]},
            "Zoom": {"Values": [{"Value": 100.0}]},
            "VideoEffects": [
                {
                    "$type": "YukkuriMovieMaker.Plugin.Effects.StripeGlitchNoise, YukkuriMovieMaker.Plugin.Effects",
                    "Name": "Glitch",
                }
            ],
            "TemplateName": "BG Pan",
        },
        {
            "$type": "YukkuriMovieMaker.Project.Items.TachieItem, YukkuriMovieMaker",
            "CharacterName": "reimu",
            "TachieItemParameter": {
                "X": -737.0,
                "Y": 540.0,
                "Zoom": 120.0,
            },
        },
    ])

    measurement = measure_timeline_routes(ymmp)

    assert measurement.item_type_counts["VoiceItem"] == 1
    assert measurement.item_type_counts["ImageItem"] == 1
    assert measurement.item_type_counts["TachieItem"] == 1
    assert measurement.route_counts["motion"]["VoiceItem.VideoEffects"] == 1
    assert measurement.route_counts["bg_anim"]["ImageItem.VideoEffects"] == 1
    assert measurement.route_counts["bg_anim"]["ImageItem.X/Y/Zoom"] == 1
    assert measurement.route_counts["slot"]["TachieItem.TachieItemParameter.X/Y/Zoom"] == 1
    assert any(
        route.endswith("Transition") or ".Transition." in route
        for route in measurement.route_counts["transition"]
    )
    assert measurement.effect_type_counts["BounceEffect"] == 1
    assert measurement.effect_type_counts["StripeGlitchNoise"] == 1
    assert measurement.template_name_counts["BG Pan"] == 1


def test_measure_timeline_routes_collects_fade_routes_as_transition_candidates():
    ymmp = _wrap([
        {
            "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
            "VoiceFadeIn": 0.3,
            "VoiceFadeOut": 0.5,
            "JimakuFadeIn": 0.2,
            "JimakuFadeOut": 0.4,
        },
        {
            "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
            "FadeIn": 0.1,
            "FadeOut": 0.2,
        },
        {
            "$type": "YukkuriMovieMaker.Project.Items.TachieItem, YukkuriMovieMaker",
            "TachieFadeIn": 0.1,
            "TachieFadeOut": 0.2,
        },
    ])

    measurement = measure_timeline_routes(ymmp)

    assert measurement.route_counts["transition"]["VoiceItem.VoiceFadeIn"] == 1
    assert measurement.route_counts["transition"]["VoiceItem.VoiceFadeOut"] == 1
    assert measurement.route_counts["transition"]["VoiceItem.JimakuFadeIn"] == 1
    assert measurement.route_counts["transition"]["VoiceItem.JimakuFadeOut"] == 1
    assert measurement.route_counts["transition"]["ImageItem.FadeIn"] == 1
    assert measurement.route_counts["transition"]["ImageItem.FadeOut"] == 1
    assert measurement.route_counts["transition"]["TachieItem.TachieFadeIn"] == 1
    assert measurement.route_counts["transition"]["TachieItem.TachieFadeOut"] == 1
    assert measurement.transition_key_counts["VoiceFadeIn"] == 1
    assert measurement.transition_key_counts["FadeIn"] == 1


def test_render_timeline_measurement_text_is_readable():
    ymmp = _wrap([
        {
            "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
            "FilePath": "C:/bg.png",
            "X": {"Values": [{"Value": 0.0}]},
            "Y": {"Values": [{"Value": 0.0}]},
            "Zoom": {"Values": [{"Value": 100.0}]},
        }
    ])

    text = render_timeline_measurement_text(measure_timeline_routes(ymmp))

    assert "--- Item Types ---" in text
    assert "ImageItem: 1" in text
    assert "--- Route Candidates ---" in text
    assert "ImageItem.X/Y/Zoom" in text


def test_validate_timeline_route_contract_reports_missing_routes():
    ymmp = _wrap([
        {
            "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
            "CharacterName": "marisa",
            "VideoEffects": [],
        }
    ])

    measurement = measure_timeline_routes(ymmp)
    result = validate_timeline_route_contract(
        measurement,
        {
            "required_routes": {
                "motion": ["VoiceItem.VideoEffects"],
                "transition": ["VoiceItem.Transition"],
            }
        },
    )

    assert result.has_errors
    assert result.missing_routes["transition"] == ["VoiceItem.Transition"]
    assert any(msg.startswith("TIMELINE_ROUTE_MISS") for msg in result.errors)


def test_validate_timeline_route_contract_optional_routes_warn_only():
    ymmp = _wrap([
        {
            "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
            "X": {"Values": [{"Value": 0.0}]},
            "Y": {"Values": [{"Value": 0.0}]},
            "Zoom": {"Values": [{"Value": 100.0}]},
        }
    ])

    measurement = measure_timeline_routes(ymmp)
    result = validate_timeline_route_contract(
        measurement,
        {
            "required_routes": {
                "bg_anim": ["ImageItem.X/Y/Zoom"],
            },
            "optional_routes": {
                "transition": ["VoiceItem.Transition"],
            },
        },
    )

    assert not result.has_errors
    assert any(
        msg.startswith("TIMELINE_ROUTE_OPTIONAL_MISS")
        for msg in result.warnings
    )


def test_validate_timeline_route_contract_profile_selection():
    ymmp = _wrap([
        {
            "$type": "YukkuriMovieMaker.Project.Items.TachieItem, YukkuriMovieMaker",
            "TachieItemParameter": {
                "X": -737.0,
                "Y": 540.0,
                "Zoom": 120.0,
            },
            "VideoEffects": [],
        }
    ])

    measurement = measure_timeline_routes(ymmp)
    result = validate_timeline_route_contract(
        measurement,
        {
            "profiles": {
                "motion_only": {
                    "required_routes": {
                        "motion": ["TachieItem.VideoEffects"],
                    }
                }
            }
        },
        profile="motion_only",
    )

    assert not result.has_errors


def test_validate_timeline_route_contract_unknown_profile_is_error():
    measurement = measure_timeline_routes(_wrap([]))
    result = validate_timeline_route_contract(
        measurement,
        {"profiles": {}},
        profile="missing",
    )

    assert result.has_errors
    assert any(
        msg.startswith("TIMELINE_ROUTE_PROFILE_UNKNOWN")
        for msg in result.errors
    )
