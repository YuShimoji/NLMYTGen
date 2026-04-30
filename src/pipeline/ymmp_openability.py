"""YMM4 openability guard for CLI-written project artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.ymmp_patch import save_ymmp


def normalize_ymmp_openability(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize the small set of shapes known to block current YMM4 loading."""
    timelines = data.get("Timelines")
    if not isinstance(timelines, list):
        raise ValueError("YMM4_TIMELINES_INVALID: Timelines must be a JSON array")

    normalized_layer_settings = 0
    defaulted_layer_settings = 0
    item_count = 0
    for timeline_index, timeline in enumerate(timelines):
        if not isinstance(timeline, dict):
            raise ValueError(
                f"YMM4_TIMELINE_INVALID: Timelines[{timeline_index}] must be an object"
            )
        items = timeline.get("Items")
        if not isinstance(items, list):
            raise ValueError(
                f"YMM4_ITEMS_INVALID: Timelines[{timeline_index}].Items must be a JSON array"
            )
        item_count += len(items)

        layer_settings = timeline.get("LayerSettings")
        if layer_settings is None and "LayerSettings" not in timeline:
            timeline["LayerSettings"] = {"Items": []}
            defaulted_layer_settings += 1
            continue
        if isinstance(layer_settings, dict) and isinstance(layer_settings.get("Items"), list):
            continue
        if isinstance(layer_settings, list):
            timeline["LayerSettings"] = {"Items": layer_settings}
            normalized_layer_settings += 1
            continue
        raise ValueError(
            "YMM4_LAYER_SETTINGS_INVALID: "
            f"Timelines[{timeline_index}].LayerSettings must be an object "
            "with an Items array or a legacy array"
        )

    return {
        "success": True,
        "expected_layer_settings_shape": (
            "Timelines[].LayerSettings is a JSON object with an Items array"
        ),
        "timeline_count": len(timelines),
        "item_count": item_count,
        "normalized_layer_settings": normalized_layer_settings,
        "defaulted_layer_settings": defaulted_layer_settings,
    }


def is_ymmp_project_canvas(data: dict[str, Any]) -> bool:
    """Return True when data has the full-project shell expected for review output."""
    timelines = data.get("Timelines")
    if not isinstance(timelines, list) or not timelines:
        return False
    timeline = timelines[0]
    if not isinstance(timeline, dict):
        return False
    required_root_keys = {"SelectedTimelineIndex", "Timelines", "Characters"}
    required_timeline_keys = {
        "ID",
        "Name",
        "VideoInfo",
        "VerticalLine",
        "Items",
        "LayerSettings",
        "CurrentFrame",
        "Length",
        "MaxLayer",
    }
    if not required_root_keys.issubset(data):
        return False
    if not required_timeline_keys.issubset(timeline):
        return False
    layer_settings = timeline.get("LayerSettings")
    return isinstance(layer_settings, dict) and isinstance(layer_settings.get("Items"), list)


def save_openable_ymmp(data: dict[str, Any], path: str | Path) -> dict[str, Any]:
    """Normalize YMM4-openability hazards, then write the project."""
    report = normalize_ymmp_openability(data)
    save_ymmp(data, path)
    return report
