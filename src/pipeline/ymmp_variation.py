"""YMM4 property-based variation probe.

This module inspects manually authored YMM4 clips and, optionally, appends
conservative variation copies for compact review.  It does not generate a new
project from scratch, emulate YMM4 rendering, or synthesize new effect types.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass
from typing import Any


SOURCE_ITEM_TYPES = {"GroupItem", "ImageItem", "TextItem", "ShapeItem"}
CHILD_ITEM_TYPES = {"ImageItem", "TextItem", "ShapeItem"}
TRANSFORM_FIELDS = ("X", "Y", "Zoom", "Rotation")
FLIP_ROUTE_KEYS = {
    "isflipped",
    "ismirrored",
    "ishorizontalflipped",
    "ishorizontalflip",
    "fliphorizontal",
    "horizontalflip",
    "flipx",
}

CONSERVATIVE_VARIANTS: tuple[dict[str, Any], ...] = (
    {"variant_id": "nudge_left", "field": "X", "delta": -40.0},
    {"variant_id": "nudge_right", "field": "X", "delta": 40.0},
    {"variant_id": "nudge_up", "field": "Y", "delta": -24.0},
    {"variant_id": "nudge_down", "field": "Y", "delta": 24.0},
    {"variant_id": "scale_up", "field": "Zoom", "delta": 5.0},
    {"variant_id": "scale_down", "field": "Zoom", "delta": -5.0},
    {"variant_id": "rotate_small", "field": "Rotation", "delta": 5.0},
)


@dataclass(frozen=True)
class ClipItem:
    timeline_index: int
    item_index: int
    item: dict[str, Any]


@dataclass(frozen=True)
class SourceClip:
    clip_id: str
    source_remark: str
    timeline_index: int
    anchor_type: str
    items: list[ClipItem]
    base_frame: int
    end_frame: int
    base_layer: int

    @property
    def duration(self) -> int:
        return max(self.end_frame - self.base_frame, 1)


def probe_ymmp_variations(
    data: dict[str, Any],
    *,
    create_review: bool = False,
    review_data: dict[str, Any] | None = None,
    review_spacing: int = 120,
) -> dict[str, Any]:
    """Inspect a YMM4 project and optionally append conservative variations."""
    clips = extract_source_clips(data)
    clip_reports: list[dict[str, Any]] = []
    warnings: list[str] = []
    errors: list[str] = []
    candidate_count = 0

    for clip in clips:
        report = _build_clip_report(clip)
        clip_reports.append(report)
        candidate_count += len(report["variation_candidates"])
        for unsupported in report["unsupported_variants"]:
            if unsupported["reason"] == "FLIP_ROUTE_MISSING":
                warnings.append(f"FLIP_ROUTE_MISSING: {clip.source_remark}")

    if not clips:
        errors.append(
            "VARIATION_SOURCE_CLIP_MISSING: no non-variation Remark Group/Image/Text/Shape clips found"
        )

    review_insertions: list[dict[str, Any]] = []
    if create_review and clips:
        review_insertions = append_variation_review_clips(
            review_data if review_data is not None else data,
            clips,
            clip_reports,
            review_spacing=review_spacing,
        )

    return {
        "success": not errors,
        "status": "ok" if not errors else "error",
        "variant_set": "conservative",
        "source_clip_count": len(clip_reports),
        "candidate_count": candidate_count,
        "review_item_insertions": sum(
            int(insertion["item_count"]) for insertion in review_insertions
        ),
        "review_clip_insertions": len(review_insertions),
        "source_clips": clip_reports,
        "warnings": sorted(set(warnings)),
        "errors": errors,
    }


def extract_source_clips(data: dict[str, Any]) -> list[SourceClip]:
    """Extract source clips from GroupItem remarks and standalone item remarks."""
    clips: list[SourceClip] = []
    selected_items: set[tuple[int, int]] = set()

    for timeline_index, _, items in _iter_timelines(data):
        group_indices_by_remark: "OrderedDict[str, list[int]]" = OrderedDict()
        for item_index, item in enumerate(items):
            if _item_type(item) != "GroupItem":
                continue
            remark = _clean_remark(item.get("Remark"))
            if not remark:
                continue
            group_indices_by_remark.setdefault(remark, []).append(item_index)

        for remark, group_indices in group_indices_by_remark.items():
            clip_item_indices = _group_clip_item_indices(items, group_indices)
            selected_items.update((timeline_index, item_index) for item_index in clip_item_indices)
            clips.append(
                _make_source_clip(
                    timeline_index=timeline_index,
                    items=items,
                    item_indices=clip_item_indices,
                    source_remark=remark,
                    anchor_type="group",
                )
            )

        standalone_indices_by_remark: "OrderedDict[str, list[int]]" = OrderedDict()
        for item_index, item in enumerate(items):
            if (timeline_index, item_index) in selected_items:
                continue
            item_type = _item_type(item)
            if item_type not in CHILD_ITEM_TYPES:
                continue
            remark = _clean_remark(item.get("Remark"))
            if not remark:
                continue
            standalone_indices_by_remark.setdefault(remark, []).append(item_index)

        for remark, item_indices in standalone_indices_by_remark.items():
            selected_items.update((timeline_index, item_index) for item_index in item_indices)
            clips.append(
                _make_source_clip(
                    timeline_index=timeline_index,
                    items=items,
                    item_indices=item_indices,
                    source_remark=remark,
                    anchor_type="standalone",
                )
            )

    clips.sort(key=lambda clip: (clip.timeline_index, clip.base_frame, clip.base_layer, clip.clip_id))
    return clips


def append_variation_review_clips(
    data: dict[str, Any],
    clips: list[SourceClip],
    clip_reports: list[dict[str, Any]],
    *,
    review_spacing: int = 120,
) -> list[dict[str, Any]]:
    """Append variation copies to the same timelines as their source clips."""
    timeline_map = {
        timeline_index: items
        for timeline_index, _, items in _iter_timelines(data)
    }
    next_frame_by_timeline = {
        timeline_index: _timeline_end_frame(items) + max(review_spacing, 1)
        for timeline_index, items in timeline_map.items()
    }
    clip_by_id = {clip.clip_id: clip for clip in clips}
    insertions: list[dict[str, Any]] = []

    for clip_report in clip_reports:
        clip = clip_by_id[clip_report["clip_id"]]
        timeline_items = timeline_map.get(clip.timeline_index)
        if timeline_items is None:
            continue
        for candidate in clip_report["variation_candidates"]:
            variant_id = candidate["variant_id"]
            target_frame = next_frame_by_timeline[clip.timeline_index]
            variation_remark = candidate["review_remark"]
            cloned_items = _clone_clip_items(
                clip,
                target_frame=target_frame,
                variation_remark=variation_remark,
            )
            _apply_variant_to_clones(cloned_items, candidate)
            timeline_items.extend(cloned_items)
            insertions.append({
                "source_remark": clip.source_remark,
                "variant_id": variant_id,
                "review_remark": variation_remark,
                "timeline_index": clip.timeline_index,
                "frame": target_frame,
                "item_count": len(cloned_items),
            })
            next_frame_by_timeline[clip.timeline_index] = (
                target_frame + clip.duration + max(review_spacing, 1)
            )

    return insertions


def render_variation_probe_text(result: dict[str, Any]) -> str:
    """Render a compact text report for humans."""
    lines = [
        f"YMM4 variation probe: {result.get('status')}",
        f"Source clips: {result.get('source_clip_count', 0)}",
        f"Candidates: {result.get('candidate_count', 0)}",
        f"Review clips: {result.get('review_clip_insertions', 0)}",
        f"Review items: {result.get('review_item_insertions', 0)}",
    ]
    for clip in result.get("source_clips", []):
        variants = ", ".join(
            candidate["variant_id"]
            for candidate in clip.get("variation_candidates", [])
        ) or "-"
        unsupported = ", ".join(
            unsupported_variant["reason"]
            for unsupported_variant in clip.get("unsupported_variants", [])
        ) or "-"
        lines.append(
            f"- {clip['source_remark']} [{clip['anchor_type']}] "
            f"items={clip['item_count']} frame={clip['frame_start']}..{clip['frame_end']} "
            f"variants={variants} unsupported={unsupported}"
        )
    if result.get("warnings"):
        lines.append("Warnings:")
        lines.extend(f"- {warning}" for warning in result["warnings"])
    if result.get("errors"):
        lines.append("Errors:")
        lines.extend(f"- {error}" for error in result["errors"])
    return "\n".join(lines) + "\n"


def _build_clip_report(clip: SourceClip) -> dict[str, Any]:
    routes = _property_routes(clip)
    effect_stack = _effect_stack_fingerprint(clip)
    candidates, unsupported = _variation_candidates(clip, routes, effect_stack)
    type_counts = Counter(_item_type(clip_item.item) for clip_item in clip.items)
    return {
        "clip_id": clip.clip_id,
        "source_remark": clip.source_remark,
        "timeline_index": clip.timeline_index,
        "anchor_type": clip.anchor_type,
        "item_count": len(clip.items),
        "item_type_counts": dict(sorted(type_counts.items())),
        "frame_start": clip.base_frame,
        "frame_end": clip.end_frame,
        "base_layer": clip.base_layer,
        "items": [
            {
                "item_index": clip_item.item_index,
                "item_type": _item_type(clip_item.item),
                "remark": clip_item.item.get("Remark"),
                "frame": _coerce_int(clip_item.item.get("Frame"), 0),
                "length": _coerce_int(clip_item.item.get("Length"), 1),
                "layer": _coerce_int(clip_item.item.get("Layer"), 0),
            }
            for clip_item in clip.items
        ],
        "patchable_property_routes": routes,
        "video_effects": effect_stack,
        "variation_candidates": candidates,
        "unsupported_variants": unsupported,
    }


def _variation_candidates(
    clip: SourceClip,
    routes: dict[str, Any],
    effect_stack: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    candidates: list[dict[str, Any]] = []
    unsupported: list[dict[str, str]] = []

    for variant in CONSERVATIVE_VARIANTS:
        field = variant["field"]
        field_key = field.lower()
        variant_id = variant["variant_id"]
        field_routes = routes.get(field_key, [])
        if not field_routes:
            if field == "Rotation":
                unsupported.append({
                    "variant_id": variant_id,
                    "reason": "ROTATION_ROUTE_MISSING",
                })
            continue
        candidates.append({
            "variant_id": variant_id,
            "operation": "relative_delta",
            "field": field,
            "delta": variant["delta"],
            "target_routes": field_routes,
            "review_remark": _variation_remark(clip.source_remark, variant_id),
        })

    flip_routes = routes.get("flip", [])
    if flip_routes:
        candidates.append({
            "variant_id": "flip",
            "operation": "toggle_bool",
            "field": "flip",
            "target_routes": flip_routes,
            "review_remark": _variation_remark(clip.source_remark, "flip"),
        })
    else:
        unsupported.append({
            "variant_id": "flip",
            "reason": "FLIP_ROUTE_MISSING",
        })

    if effect_stack["stack_count"] > 0:
        candidates.append({
            "variant_id": "effect_reuse",
            "operation": "reuse_existing_video_effects",
            "effect_fingerprint": effect_stack["fingerprint"],
            "target_routes": routes.get("video_effects", []),
            "review_remark": _variation_remark(clip.source_remark, "effect_reuse"),
        })

    if not any(routes.get(field_key) for field_key in ("x", "y", "zoom")):
        unsupported.append({
            "variant_id": "nudge_or_scale",
            "reason": "TRANSFORM_ROUTE_MISSING",
        })

    return candidates, unsupported


def _property_routes(clip: SourceClip) -> dict[str, Any]:
    routes: dict[str, list[dict[str, Any]]] = {
        "x": [],
        "y": [],
        "zoom": [],
        "rotation": [],
        "flip": [],
        "video_effects": [],
    }
    for clip_item in _variation_target_clip_items(clip):
        item_type = _item_type(clip_item.item)
        for field in TRANSFORM_FIELDS:
            if _has_numeric_property_route(clip_item.item, field):
                routes[field.lower()].append({
                    "item_index": clip_item.item_index,
                    "item_type": item_type,
                    "route": f"{item_type}.{field}.Values[].Value",
                })
        for flip_path in _find_flip_routes(clip_item.item):
            routes["flip"].append({
                "item_index": clip_item.item_index,
                "item_type": item_type,
                "route": f"{item_type}.{_format_path(flip_path)}",
            })
        if isinstance(clip_item.item.get("VideoEffects"), list):
            routes["video_effects"].append({
                "item_index": clip_item.item_index,
                "item_type": item_type,
                "route": f"{item_type}.VideoEffects",
            })
    return {key: value for key, value in routes.items() if value}


def _effect_stack_fingerprint(clip: SourceClip) -> dict[str, Any]:
    stacks: list[dict[str, Any]] = []
    for clip_item in clip.items:
        effects = clip_item.item.get("VideoEffects")
        if not isinstance(effects, list) or not effects:
            continue
        effect_types = [
            _item_type(effect)
            for effect in effects
            if isinstance(effect, dict) and _item_type(effect)
        ]
        effect_names = [
            str(effect["Name"])
            for effect in effects
            if isinstance(effect, dict) and isinstance(effect.get("Name"), str)
        ]
        serialized_stack = json.dumps(effects, ensure_ascii=False, sort_keys=True, default=str)
        stack_hash = hashlib.sha1(serialized_stack.encode("utf-8")).hexdigest()[:12]
        stacks.append({
            "item_index": clip_item.item_index,
            "item_type": _item_type(clip_item.item),
            "effect_count": len(effects),
            "effect_types": effect_types,
            "effect_names": effect_names,
            "fingerprint": stack_hash,
        })

    serialized_all = json.dumps(stacks, ensure_ascii=False, sort_keys=True)
    fingerprint = (
        hashlib.sha1(serialized_all.encode("utf-8")).hexdigest()[:12]
        if stacks
        else None
    )
    return {
        "fingerprint": fingerprint,
        "stack_count": len(stacks),
        "stacks": stacks,
    }


def _group_clip_item_indices(items: list[dict[str, Any]], group_indices: list[int]) -> list[int]:
    selected_indices = set(group_indices)
    for group_index in group_indices:
        group_item = items[group_index]
        group_remark = _clean_remark(group_item.get("Remark"))
        group_layer = _coerce_int(group_item.get("Layer"), 0)
        group_range = max(_coerce_int(group_item.get("GroupRange"), 0), 0)
        if group_range <= 0:
            continue
        for item_index, item in enumerate(items):
            if item_index in selected_indices:
                continue
            if _item_type(item) not in CHILD_ITEM_TYPES:
                continue
            child_layer = _coerce_int(item.get("Layer"), 0)
            if not group_layer < child_layer <= group_layer + group_range:
                continue
            child_remark = _clean_remark(item.get("Remark"))
            if child_remark and child_remark != group_remark:
                continue
            if _time_spans_overlap(group_item, item):
                selected_indices.add(item_index)
    return sorted(selected_indices)


def _make_source_clip(
    *,
    timeline_index: int,
    items: list[dict[str, Any]],
    item_indices: list[int],
    source_remark: str,
    anchor_type: str,
) -> SourceClip:
    clip_items = [
        ClipItem(timeline_index=timeline_index, item_index=item_index, item=items[item_index])
        for item_index in sorted(item_indices)
    ]
    base_frame = min(_coerce_int(clip_item.item.get("Frame"), 0) for clip_item in clip_items)
    end_frame = max(
        _coerce_int(clip_item.item.get("Frame"), 0)
        + max(_coerce_int(clip_item.item.get("Length"), 1), 1)
        for clip_item in clip_items
    )
    base_layer = min(_coerce_int(clip_item.item.get("Layer"), 0) for clip_item in clip_items)
    return SourceClip(
        clip_id=f"{timeline_index}:{source_remark}",
        source_remark=source_remark,
        timeline_index=timeline_index,
        anchor_type=anchor_type,
        items=clip_items,
        base_frame=base_frame,
        end_frame=end_frame,
        base_layer=base_layer,
    )


def _variation_target_clip_items(clip: SourceClip) -> list[ClipItem]:
    group_items = [
        clip_item
        for clip_item in clip.items
        if _item_type(clip_item.item) == "GroupItem"
    ]
    return group_items or clip.items


def _clone_clip_items(
    clip: SourceClip,
    *,
    target_frame: int,
    variation_remark: str,
) -> list[dict[str, Any]]:
    cloned_items: list[dict[str, Any]] = []
    for clip_item in clip.items:
        cloned_item = copy.deepcopy(clip_item.item)
        cloned_item["Frame"] = (
            target_frame
            + _coerce_int(clip_item.item.get("Frame"), 0)
            - clip.base_frame
        )
        cloned_item["Remark"] = variation_remark
        cloned_items.append(cloned_item)
    return cloned_items


def _apply_variant_to_clones(
    cloned_items: list[dict[str, Any]],
    candidate: dict[str, Any],
) -> None:
    operation = candidate["operation"]
    target_items = _target_items_for_clones(cloned_items)
    if operation == "relative_delta":
        field = candidate["field"]
        delta = float(candidate["delta"])
        for item in target_items:
            _apply_numeric_delta(item, field, delta)
    elif operation == "toggle_bool":
        for item in target_items:
            for flip_path in _find_flip_routes(item):
                current_value = _get_nested(item, flip_path)
                if isinstance(current_value, bool):
                    _set_nested(item, flip_path, not current_value)
    elif operation == "reuse_existing_video_effects":
        return


def _target_items_for_clones(cloned_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    group_items = [
        item
        for item in cloned_items
        if _item_type(item) == "GroupItem"
    ]
    return group_items or cloned_items


def _has_numeric_property_route(item: dict[str, Any], field: str) -> bool:
    value = item.get(field)
    if isinstance(value, (int, float)):
        return True
    if not isinstance(value, dict):
        return False
    values = value.get("Values")
    if not isinstance(values, list):
        return False
    return any(
        isinstance(keyframe, dict)
        and isinstance(keyframe.get("Value"), (int, float))
        for keyframe in values
    )


def _apply_numeric_delta(item: dict[str, Any], field: str, delta: float) -> bool:
    value = item.get(field)
    if isinstance(value, (int, float)):
        item[field] = value + delta
        return True
    if not isinstance(value, dict):
        return False
    values = value.get("Values")
    if not isinstance(values, list):
        return False
    changed = False
    for keyframe in values:
        if not isinstance(keyframe, dict):
            continue
        current_value = keyframe.get("Value")
        if isinstance(current_value, (int, float)):
            keyframe["Value"] = current_value + delta
            changed = True
    return changed


def _find_flip_routes(item: dict[str, Any]) -> list[tuple[Any, ...]]:
    return list(_walk_flip_routes(item, ()))


def _walk_flip_routes(node: Any, path: tuple[Any, ...]):
    if isinstance(node, dict):
        for key, value in node.items():
            next_path = (*path, key)
            if isinstance(value, bool) and _normalized_key(key) in FLIP_ROUTE_KEYS:
                yield next_path
            elif isinstance(value, (dict, list)):
                yield from _walk_flip_routes(value, next_path)
    elif isinstance(node, list):
        for item_index, value in enumerate(node):
            if isinstance(value, (dict, list)):
                yield from _walk_flip_routes(value, (*path, item_index))


def _get_nested(node: Any, path: tuple[Any, ...]) -> Any:
    current = node
    for segment in path:
        current = current[segment]
    return current


def _set_nested(node: Any, path: tuple[Any, ...], value: Any) -> None:
    current = node
    for segment in path[:-1]:
        current = current[segment]
    current[path[-1]] = value


def _format_path(path: tuple[Any, ...]) -> str:
    formatted = ""
    for segment in path:
        if isinstance(segment, int):
            formatted += f"[{segment}]"
        else:
            formatted += f".{segment}" if formatted else str(segment)
    return formatted


def _time_spans_overlap(first_item: dict[str, Any], second_item: dict[str, Any]) -> bool:
    first_start = _coerce_int(first_item.get("Frame"), 0)
    first_end = first_start + max(_coerce_int(first_item.get("Length"), 1), 1)
    second_start = _coerce_int(second_item.get("Frame"), 0)
    second_end = second_start + max(_coerce_int(second_item.get("Length"), 1), 1)
    return first_start < second_end and second_start < first_end


def _iter_timelines(data: dict[str, Any]):
    timelines = data.get("Timelines")
    if isinstance(timelines, list):
        for timeline_index, timeline in enumerate(timelines):
            if not isinstance(timeline, dict):
                continue
            items = timeline.get("Items")
            if isinstance(items, list):
                yield timeline_index, timeline, items
        return

    timeline = data.get("Timeline")
    if isinstance(timeline, dict):
        items = timeline.get("Items")
        if isinstance(items, list):
            yield 0, timeline, items


def _timeline_end_frame(items: list[dict[str, Any]]) -> int:
    end_frame = 0
    for item in items:
        end_frame = max(
            end_frame,
            _coerce_int(item.get("Frame"), 0) + max(_coerce_int(item.get("Length"), 1), 1),
        )
    return end_frame


def _item_type(item: dict[str, Any]) -> str:
    raw_type = item.get("$type", "")
    return raw_type.split(",")[0].split(".")[-1] if "." in raw_type else raw_type


def _clean_remark(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    remark = value.strip()
    if not remark or remark.startswith("variation:"):
        return ""
    return remark


def _variation_remark(source_remark: str, variant_id: str) -> str:
    return f"variation:{source_remark}:{variant_id}"


def _coerce_int(value: Any, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return default


def _normalized_key(value: Any) -> str:
    return str(value).replace("_", "").replace("-", "").lower()
