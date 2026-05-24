from __future__ import annotations

import copy
from dataclasses import dataclass, field
from pathlib import Path
from statistics import median

from src.pipeline.skit_group_audit import _parse_registry, _resolve_entry
from src.pipeline.ymmp_patch import (
    _get_timeline_items,
    _item_type,
    _parse_motion_target_layers,
    _resolve_carry_forward,
    _resolve_utterance_timing,
)


FAIL_SOURCE_MISSING = "SKIT_TEMPLATE_SOURCE_MISSING"
FAIL_SOURCE_FORBIDDEN_ITEM = "SKIT_TEMPLATE_SOURCE_FORBIDDEN_ITEM"
FAIL_SOURCE_ASSET_MISSING = "SKIT_TEMPLATE_SOURCE_ASSET_MISSING"
FAIL_NO_TIMING = "SKIT_PLACEMENT_NO_VOICE_TIMING"
FAIL_GROUP_AMBIGUOUS = "SKIT_PLACEMENT_GROUP_AMBIGUOUS"
FAIL_REGISTRY_INVALID = "SKIT_PLACEMENT_REGISTRY_INVALID"
FAIL_ANALYSIS_INSUFFICIENT = "SKIT_TEMPLATE_ANALYSIS_INSUFFICIENT"

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TRANSFORM_AXES = ("X", "Y", "Zoom")
_DEFAULT_COMPACT_REVIEW_SPACING_FRAMES = 240


@dataclass
class SkitTemplateClip:
    name: str
    items: list[dict]
    base_frame: int
    base_layer: int


@dataclass
class SkitPlacementResult:
    placements: int = 0
    item_insertions: int = 0
    group_item_insertions: int = 0
    manual_notes: int = 0
    duplicate_skips: int = 0
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SkitTemplateChildOffset:
    frame_offset: int
    layer_offset: int
    transform_values: dict[str, list[float]]


@dataclass(frozen=True)
class SkitTemplateSegmentTiming:
    frame_offset: int
    length: int


@dataclass(frozen=True)
class SkitTemplateAnalysis:
    rest_pose: dict[str, float]
    clip_baselines: dict[str, dict[str, float]]
    child_offsets: dict[str, list[SkitTemplateChildOffset]]
    segment_timings: dict[str, list[SkitTemplateSegmentTiming]]
    transform_deltas: dict[str, list[dict[str, list[float]]]]


def extract_skit_group_templates(template_source_data: dict) -> dict[str, SkitTemplateClip]:
    """GroupItem Remark を template_name として template clip を抽出する."""
    items = _get_timeline_items(template_source_data)
    template_names = sorted({
        item.get("Remark", "").strip()
        for item in items
        if _item_type(item) == "GroupItem"
        and isinstance(item.get("Remark"), str)
        and item.get("Remark", "").strip()
    })
    return {
        name: clip
        for name in template_names
        if (clip := _extract_template_clip(items, name)) is not None
    }


def validate_template_source_against_registry(
    registry_data: dict,
    template_source_data: dict,
) -> list[str]:
    """registry の template_name が repo-tracked source に存在するか検査する."""
    errors: list[str] = []
    spec = _parse_registry(registry_data, errors)
    if spec is None:
        return [f"{FAIL_REGISTRY_INVALID}: {error}" for error in errors]

    templates = extract_skit_group_templates(template_source_data)
    warnings: list[str] = []
    for template in spec.templates.values():
        if template.template_name not in templates:
            warnings.append(
                f"{FAIL_SOURCE_MISSING}: template '{template.template_name}'"
                " not found in skit_group template source"
            )

    for clip in templates.values():
        for item in clip.items:
            item_type = _item_type(item)
            if item_type == "TachieItem":
                warnings.append(
                    f"{FAIL_SOURCE_FORBIDDEN_ITEM}: template '{clip.name}'"
                    " contains TachieItem; skit_group templates must be ImageItem children"
                )
            if item_type == "ImageItem":
                file_path = item.get("FilePath")
                if isinstance(file_path, str) and file_path:
                    if _resolve_repo_asset_path(file_path) is None:
                        warnings.append(
                            f"{FAIL_SOURCE_ASSET_MISSING}: template '{clip.name}'"
                            f" image asset not found: {file_path}"
                        )
    return warnings


def apply_skit_group_placement(
    ymmp_data: dict,
    ir_data: dict,
    registry_data: dict,
    template_source_data: dict,
    *,
    compact_review: bool = False,
    compact_review_spacing: int = _DEFAULT_COMPACT_REVIEW_SPACING_FRAMES,
) -> SkitPlacementResult:
    """IR の skit_group intent を GroupItem template として timeline へ挿入する."""
    result = SkitPlacementResult()
    errors: list[str] = []
    spec = _parse_registry(registry_data, errors)
    if spec is None:
        result.warnings.extend(f"{FAIL_REGISTRY_INVALID}: {error}" for error in errors)
        return result

    if len(spec.canonical_groups) != 1:
        result.warnings.append(
            f"{FAIL_GROUP_AMBIGUOUS}: placement requires exactly one canonical group"
        )
        return result
    group_key = next(iter(spec.canonical_groups))

    source_warnings = validate_template_source_against_registry(
        registry_data,
        template_source_data,
    )
    result.warnings.extend(source_warnings)
    templates = extract_skit_group_templates(template_source_data)
    analysis, analysis_warnings = analyze_skit_group_templates(templates)
    result.warnings.extend(analysis_warnings)
    if analysis is None:
        return result

    items = _get_timeline_items(ymmp_data)
    voice_items = [item for item in items if _item_type(item) == "VoiceItem"]
    voice_items.sort(key=lambda item: item.get("Frame", 0))
    resolved = _resolve_carry_forward(ir_data)
    use_row_range = bool(resolved and resolved[0].get("row_start") is not None)

    existing_remarks = {
        item.get("Remark")
        for item in items
        if _item_type(item) == "GroupItem" and isinstance(item.get("Remark"), str)
    }
    compact_index = 0
    compact_spacing = max(compact_review_spacing, 1)

    for entry in resolved:
        motion = entry.get("motion")
        if not isinstance(motion, str) or not motion or motion == "none":
            continue
        target_layers = _parse_motion_target_layers(entry.get("motion_target"))
        if not target_layers:
            continue

        resolution, entry_errors = _resolve_entry(
            entry=entry,
            requested_intent=motion,
            anchor_group_key=group_key,
            canonical_groups=spec.canonical_groups,
            templates=spec.templates,
            intent_fallbacks=spec.intent_fallbacks,
        )
        if entry_errors:
            result.warnings.extend(entry_errors)
            continue
        if resolution is None:
            continue
        if resolution.resolution == "manual_note":
            result.manual_notes += 1
            continue

        template_name = resolution.template_name
        if not template_name:
            result.manual_notes += 1
            continue
        template = templates.get(template_name)
        if template is None:
            result.warnings.append(
                f"{FAIL_SOURCE_MISSING}: template '{template_name}'"
                f" required by utterance index={resolution.index}"
            )
            continue

        if compact_review:
            target_frame = compact_index * compact_spacing
            compact_index += 1
        else:
            timing = _resolve_utterance_timing(
                entry,
                voice_items,
                use_row_range=use_row_range,
            )
            if timing is None:
                result.warnings.append(
                    f"{FAIL_NO_TIMING}: utterance index={resolution.index}"
                    f" template '{template_name}' has no VoiceItem timing"
                )
                continue
            target_frame = int(timing[0])

        for target_layer in target_layers:
            placement_remark = _placement_remark(template_name, resolution.index)
            if placement_remark in existing_remarks:
                result.duplicate_skips += 1
                continue
            inserted = _clone_template_items(
                template,
                analysis=analysis,
                target_frame=target_frame,
                target_layer=target_layer,
                placement_remark=placement_remark,
            )
            items.extend(inserted)
            existing_remarks.add(placement_remark)
            result.placements += 1
            result.item_insertions += len(inserted)
            result.group_item_insertions += sum(
                1 for item in inserted if _item_type(item) == "GroupItem"
            )

    items.sort(key=lambda item: (item.get("Frame", 0), item.get("Layer", 0)))
    return result


def analyze_skit_group_templates(
    templates: dict[str, SkitTemplateClip],
) -> tuple[SkitTemplateAnalysis | None, list[str]]:
    """template source から正規化用の rest pose / offset / timing を抽出する."""
    warnings: list[str] = []
    rest_pose_samples: dict[str, list[float]] = {
        axis_name: [] for axis_name in _TRANSFORM_AXES
    }
    clip_baselines: dict[str, dict[str, float]] = {}

    for clip in templates.values():
        group_items = [
            item for item in clip.items
            if _item_type(item) == "GroupItem"
        ]
        if not group_items:
            warnings.append(
                f"{FAIL_ANALYSIS_INSUFFICIENT}: template '{clip.name}'"
                " has no GroupItem transform source"
            )
            continue

        clip_baseline: dict[str, float] = {}
        for axis_name in _TRANSFORM_AXES:
            axis_samples: list[float] = []
            for group_item in group_items:
                first_value = _first_transform_value(group_item, axis_name)
                if first_value is not None:
                    axis_samples.append(first_value)
                    rest_pose_samples[axis_name].append(first_value)
            if axis_samples:
                clip_baseline[axis_name] = float(median(axis_samples))
            else:
                warnings.append(
                    f"{FAIL_ANALYSIS_INSUFFICIENT}: template '{clip.name}'"
                    f" has no numeric {axis_name} transform baseline"
                )
        if all(axis_name in clip_baseline for axis_name in _TRANSFORM_AXES):
            clip_baselines[clip.name] = clip_baseline

    rest_pose: dict[str, float] = {}
    for axis_name, samples in rest_pose_samples.items():
        if samples:
            rest_pose[axis_name] = float(median(samples))
        else:
            warnings.append(
                f"{FAIL_ANALYSIS_INSUFFICIENT}: template source has no numeric"
                f" {axis_name} rest-pose samples"
            )

    if warnings:
        return None, warnings

    child_offsets: dict[str, list[SkitTemplateChildOffset]] = {}
    segment_timings: dict[str, list[SkitTemplateSegmentTiming]] = {}
    transform_deltas: dict[str, list[dict[str, list[float]]]] = {}
    for clip in templates.values():
        baseline = clip_baselines[clip.name]
        child_offsets[clip.name] = []
        segment_timings[clip.name] = []
        transform_deltas[clip.name] = []
        for item in clip.items:
            item_type = _item_type(item)
            if item_type == "ImageItem":
                child_offsets[clip.name].append(
                    SkitTemplateChildOffset(
                        frame_offset=_coerce_int(item.get("Frame"), 0) - clip.base_frame,
                        layer_offset=_coerce_int(item.get("Layer"), 0) - clip.base_layer,
                        transform_values=_transform_values(item, _TRANSFORM_AXES),
                    )
                )
            if item_type == "GroupItem":
                segment_timings[clip.name].append(
                    SkitTemplateSegmentTiming(
                        frame_offset=_coerce_int(item.get("Frame"), 0) - clip.base_frame,
                        length=max(_coerce_int(item.get("Length"), 0), 1),
                    )
                )
                transform_deltas[clip.name].append({
                    axis_name: [
                        value - baseline[axis_name]
                        for value in _transform_values(item, (axis_name,))[axis_name]
                    ]
                    for axis_name in _TRANSFORM_AXES
                })

    return SkitTemplateAnalysis(
        rest_pose=rest_pose,
        clip_baselines=clip_baselines,
        child_offsets=child_offsets,
        segment_timings=segment_timings,
        transform_deltas=transform_deltas,
    ), []


def _extract_template_clip(items: list[dict], template_name: str) -> SkitTemplateClip | None:
    group_indices = [
        idx
        for idx, item in enumerate(items)
        if _item_type(item) == "GroupItem" and item.get("Remark") == template_name
    ]
    if not group_indices:
        return None

    selected = set(group_indices)
    same_remark_children: set[int] = set()
    blank_remark_children: set[int] = set()
    for group_idx in group_indices:
        group_item = items[group_idx]
        group_layer = group_item.get("Layer")
        group_range = group_item.get("GroupRange", 0)
        if not isinstance(group_layer, int) or not isinstance(group_range, int):
            continue
        for idx, item in enumerate(items):
            if idx in selected or _item_type(item) == "GroupItem":
                continue
            layer = item.get("Layer")
            if not isinstance(layer, int):
                continue
            if not group_layer < layer <= group_layer + group_range:
                continue
            if _time_spans_overlap(group_item, item):
                child_remark = item.get("Remark")
                if child_remark == template_name:
                    same_remark_children.add(idx)
                elif not isinstance(child_remark, str) or not child_remark.strip():
                    blank_remark_children.add(idx)

    selected.update(same_remark_children or blank_remark_children)

    clip_items = [copy.deepcopy(items[idx]) for idx in sorted(selected)]
    base_frame = min(_coerce_int(item.get("Frame"), 0) for item in clip_items)
    base_layer = min(
        _coerce_int(item.get("Layer"), 0)
        for item in clip_items
        if _item_type(item) == "GroupItem"
    )
    return SkitTemplateClip(
        name=template_name,
        items=clip_items,
        base_frame=base_frame,
        base_layer=base_layer,
    )


def _clone_template_items(
    template: SkitTemplateClip,
    *,
    analysis: SkitTemplateAnalysis,
    target_frame: int,
    target_layer: int,
    placement_remark: str,
) -> list[dict]:
    layer_delta = target_layer - template.base_layer
    cloned: list[dict] = []
    for item in template.items:
        new_item = copy.deepcopy(item)
        new_item["Frame"] = target_frame + _coerce_int(item.get("Frame"), 0) - template.base_frame
        new_item["Layer"] = _coerce_int(item.get("Layer"), 0) + layer_delta
        item_type = _item_type(new_item)
        if item_type == "ImageItem":
            file_path = new_item.get("FilePath")
            if isinstance(file_path, str) and file_path:
                resolved_path = _resolve_repo_asset_path(file_path)
                if resolved_path is not None:
                    new_item["FilePath"] = _format_yymm_asset_path(resolved_path)
        if item_type == "GroupItem":
            _normalize_group_transform(new_item, template.name, analysis)
            new_item["Remark"] = placement_remark
        cloned.append(new_item)
    return cloned


def _normalize_group_transform(
    item: dict,
    template_name: str,
    analysis: SkitTemplateAnalysis,
) -> None:
    baseline = analysis.clip_baselines[template_name]
    for axis_name in _TRANSFORM_AXES:
        axis_shift = analysis.rest_pose[axis_name] - baseline[axis_name]
        _shift_transform_values(item, axis_name, axis_shift)


def _shift_transform_values(item: dict, axis_name: str, axis_shift: float) -> None:
    transform = item.get(axis_name)
    if not isinstance(transform, dict):
        return
    values = transform.get("Values")
    if not isinstance(values, list):
        return
    for keyframe in values:
        if not isinstance(keyframe, dict):
            continue
        value = _coerce_float(keyframe.get("Value"))
        if value is None:
            continue
        keyframe["Value"] = value + axis_shift


def _first_transform_value(item: dict, axis_name: str) -> float | None:
    values = _transform_values(item, (axis_name,))[axis_name]
    if not values:
        return None
    return values[0]


def _transform_values(item: dict, axis_names: tuple[str, ...]) -> dict[str, list[float]]:
    transforms: dict[str, list[float]] = {}
    for axis_name in axis_names:
        transforms[axis_name] = []
        transform = item.get(axis_name)
        if not isinstance(transform, dict):
            continue
        values = transform.get("Values")
        if not isinstance(values, list):
            continue
        for keyframe in values:
            if not isinstance(keyframe, dict):
                continue
            value = _coerce_float(keyframe.get("Value"))
            if value is not None:
                transforms[axis_name].append(value)
    return transforms


def _resolve_repo_asset_path(file_path: str) -> Path | None:
    path = Path(file_path)
    if path.exists():
        return path

    normalized = file_path.replace("/", "\\")
    marker = "\\samples\\"
    marker_index = normalized.lower().find(marker)
    if marker_index == -1:
        return None
    suffix = normalized[marker_index + 1:].split("\\")
    candidate = _REPO_ROOT.joinpath(*suffix)
    if candidate.exists():
        return candidate
    return None


def _format_yymm_asset_path(path: Path) -> str:
    parts = path.resolve().parts
    if len(parts) >= 4 and parts[0] == "/" and parts[1] == "mnt" and len(parts[2]) == 1:
        drive = parts[2].upper()
        return f"{drive}:\\" + "\\".join(parts[3:])
    return str(path)


def _placement_remark(template_name: str, ir_index: int | None) -> str:
    idx = ir_index if ir_index is not None else "?"
    return f"skit_group:{template_name} utt:{idx}"


def _time_spans_overlap(left: dict, right: dict) -> bool:
    left_start = _coerce_int(left.get("Frame"), 0)
    left_end = left_start + max(_coerce_int(left.get("Length"), 0), 1)
    right_start = _coerce_int(right.get("Frame"), 0)
    right_end = right_start + max(_coerce_int(right.get("Length"), 0), 1)
    return left_start < right_end and right_start < left_end


def _coerce_int(value: object, default: int) -> int:
    return value if isinstance(value, int) else default


def _coerce_float(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None
