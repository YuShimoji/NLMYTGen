"""ymmp timeline route measurement tests."""

from src.pipeline.ymmp_measure import (
    measure_timeline_routes,
    render_timeline_measurement_text,
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
