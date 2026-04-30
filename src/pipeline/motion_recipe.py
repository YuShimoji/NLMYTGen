"""G-26 purpose-driven YMM4 motion recipe review builder."""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.pipeline.skit_group_placement import (
    extract_skit_group_templates,
    _format_yymm_asset_path,
    _resolve_repo_asset_path,
)
from src.pipeline.ymmp_openability import is_ymmp_project_canvas, save_openable_ymmp
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


DEFAULT_SEED_PATH = Path("samples/canonical.ymmp")
DEFAULT_TEMPLATE_SOURCE_PATH = Path("samples/templates/skit_group/delivery_v1_templates.ymmp")
DEFAULT_EFFECT_CATALOG_PATH = Path("samples/effect_catalog.json")
DEFAULT_EFFECT_SAMPLES_PATH = Path("samples/_probe/b2/effect_full_samples.json")
DEFAULT_MOTION_LIBRARY_PATH = Path("samples/tachie_motion_map_library.json")
DEFAULT_CORPUS_YMMP_PATH = Path("_tmp/g26/composition/演出_palette_v2.ymmp")
DEFAULT_OUTPUT_YMMP_PATH = Path("_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1.ymmp")
DEFAULT_OUTPUT_READBACK_PATH = Path(
    "_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1_readback.json"
)
DEFAULT_OUTPUT_MANIFEST_PATH = Path(
    "_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1_manifest.md"
)

RECIPE_STATUS_PROPOSED = "proposed"
RECIPE_REMARK_PREFIX = "recipe:"
BASE_TEMPLATE_NAME = "delivery_nod_v1"
DEFAULT_LAYER = 9
DEFAULT_GROUP_RANGE = 2


@dataclass(frozen=True)
class MotionRecipeBuildPaths:
    brief: Path
    seed: Path = DEFAULT_SEED_PATH
    template_source: Path = DEFAULT_TEMPLATE_SOURCE_PATH
    effect_catalog: Path = DEFAULT_EFFECT_CATALOG_PATH
    motion_library: Path = DEFAULT_MOTION_LIBRARY_PATH
    out_ymmp: Path = DEFAULT_OUTPUT_YMMP_PATH
    out_readback: Path = DEFAULT_OUTPUT_READBACK_PATH
    out_manifest: Path = DEFAULT_OUTPUT_MANIFEST_PATH
    effect_samples: Path | None = DEFAULT_EFFECT_SAMPLES_PATH
    corpus_ymmp: Path | None = DEFAULT_CORPUS_YMMP_PATH


DEFAULT_RECIPE_ORDER = [
    "nod_clear",
    "nod_subtle",
    "nod_double",
    "jump_small",
    "jump_high",
    "jump_emphasis",
    "panic_crash",
    "shocked_jump",
    "surprised_chromatic",
    "anger_outburst",
    "shobon_droop",
    "lean_curious",
]

DEFAULT_RECIPE_PRESETS: dict[str, dict[str, Any]] = {
    "nod_clear": {
        "motion_goal": "Readable nod for agreement, understanding, or confirmation.",
        "emotion": "agreement",
        "intensity": "medium",
        "duration_frames": 48,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "too subtle"],
        "rotation_values": [0.0, -10.0, 0.0],
        "effect_names": ["CenterPointEffect"],
        "effect_candidates": ["CenterPointEffect", "RepeatMoveEffect"],
    },
    "nod_subtle": {
        "motion_goal": "Light nod for agreement or backchannel reaction.",
        "emotion": "agreement",
        "intensity": "light",
        "duration_frames": 36,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "too subtle"],
        "rotation_values": [0.0, -4.0, 0.0],
        "effect_names": ["CenterPointEffect"],
        "effect_candidates": ["CenterPointEffect", "RepeatMoveEffect"],
    },
    "nod_double": {
        "motion_goal": "Double nod for stronger agreement or energetic reaction.",
        "emotion": "agreement",
        "intensity": "strong",
        "duration_frames": 66,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "too busy"],
        "rotation_values": [0.0, -7.0, 0.0, -5.0, 0.0],
        "effect_names": ["CenterPointEffect"],
        "effect_candidates": ["CenterPointEffect", "RepeatMoveEffect", "RepeatRotateEffect"],
    },
    "jump_small": {
        "motion_goal": "Small jump for light surprise or pop emphasis.",
        "emotion": "surprise",
        "intensity": "light",
        "duration_frames": 42,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "too strong"],
        "y_delta_values": [0.0, -35.0, 0.0],
        "effect_names": ["CenterPointEffect"],
        "effect_candidates": ["CenterPointEffect", "JumpEffect"],
    },
    "jump_high": {
        "motion_goal": "High jump for discovery or strong surprise.",
        "emotion": "surprise",
        "intensity": "strong",
        "duration_frames": 54,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "screen spacing"],
        "y_delta_values": [0.0, -90.0, 0.0],
        "effect_names": ["CenterPointEffect"],
        "effect_candidates": ["CenterPointEffect", "JumpEffect", "ChromaticAberrationEffect"],
    },
    "jump_emphasis": {
        "motion_goal": "Jump with slight landing dip for comic emphasis.",
        "emotion": "surprise",
        "intensity": "medium",
        "duration_frames": 72,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "too strong"],
        "y_delta_values": [0.0, -70.0, 0.0, 10.0, 0.0],
        "effect_names": ["CenterPointEffect"],
        "effect_candidates": ["CenterPointEffect", "JumpEffect"],
    },
    "panic_crash": {
        "motion_goal": "Panic impact beat for sudden trouble or collapse.",
        "emotion": "panic",
        "intensity": "strong",
        "duration_frames": 70,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "too destructive", "community plugin missing"],
        "effect_names": ["CenterPointEffect", "CrashEffect", "CameraShakeEffect"],
        "effect_candidates": ["CrashEffect", "CameraShakeEffect", "RandomMoveEffect"],
    },
    "shocked_jump": {
        "motion_goal": "Effect-driven jump for a clear shocked reaction.",
        "emotion": "surprise",
        "intensity": "strong",
        "duration_frames": 60,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "too strong"],
        "effect_names": ["CenterPointEffect", "JumpEffect"],
        "effect_candidates": ["JumpEffect", "ChromaticAberrationEffect"],
    },
    "surprised_chromatic": {
        "motion_goal": "Surprise accent with zoom, tiny wobble, and color split.",
        "emotion": "surprise",
        "intensity": "medium",
        "duration_frames": 50,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "too noisy"],
        "rotation_values": [0.0, -3.0, 3.0, 0.0],
        "zoom_values": [103.8, 110.0, 110.0, 103.8],
        "effect_names": ["CenterPointEffect", "ChromaticAberrationEffect"],
        "effect_candidates": ["ChromaticAberrationEffect", "ZoomEffect", "RepeatRotateEffect"],
    },
    "anger_outburst": {
        "motion_goal": "Angry tremble / outburst beat.",
        "emotion": "anger",
        "intensity": "medium",
        "duration_frames": 60,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "wrong emotion"],
        "effect_names": ["CenterPointEffect", "RepeatRotateEffect"],
        "effect_candidates": ["RepeatRotateEffect", "RandomRotateEffect", "RandomMoveEffect"],
    },
    "shobon_droop": {
        "motion_goal": "Drooping reaction for disappointment or sadness.",
        "emotion": "sadness",
        "intensity": "medium",
        "duration_frames": 80,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "looks like nod"],
        "rotation_values": [0.0, -12.0, -12.0],
        "y_delta_values": [0.0, 18.0, 18.0],
        "effect_names": ["CenterPointEffect"],
        "effect_candidates": ["CenterPointEffect", "OpacityEffect", "GaussianBlurEffect"],
    },
    "lean_curious": {
        "motion_goal": "Lean-in curious pose for doubt or thinking.",
        "emotion": "curiosity",
        "intensity": "medium",
        "duration_frames": 60,
        "reset_policy": "returns_to_neutral",
        "forbidden_patterns": ["body-face drift", "wrong tilt direction"],
        "rotation_values": [0.0, -8.0, -8.0, 0.0],
        "effect_names": ["CenterPointEffect"],
        "effect_candidates": ["CenterPointEffect", "RepeatRotateEffect"],
    },
}


def build_motion_recipe_review(paths: MotionRecipeBuildPaths) -> dict[str, Any]:
    """Build a YMM4-openable recipe review artifact from an intent brief."""
    brief = _load_json(paths.brief)
    seed_data = load_ymmp(paths.seed)
    if not is_ymmp_project_canvas(seed_data):
        raise ValueError(f"YMM4_REVIEW_SEED_INVALID: {paths.seed}")

    template_source = load_ymmp(paths.template_source)
    templates = extract_skit_group_templates(template_source)
    base_clip = templates.get(BASE_TEMPLATE_NAME) or next(iter(templates.values()), None)
    if base_clip is None:
        raise ValueError("MOTION_RECIPE_TEMPLATE_SOURCE_EMPTY")

    base_group = _first_group_item(base_clip)
    base_images = _image_items(base_clip)
    if len(base_images) < 1:
        raise ValueError("MOTION_RECIPE_TEMPLATE_SOURCE_NO_IMAGE_CHILDREN")

    effect_catalog = _load_json(paths.effect_catalog)
    motion_library = _load_json(paths.motion_library)
    effect_samples = (
        _load_json(paths.effect_samples)
        if paths.effect_samples is not None and paths.effect_samples.exists()
        else {}
    )
    corpus_data = (
        load_ymmp(paths.corpus_ymmp)
        if paths.corpus_ymmp is not None and paths.corpus_ymmp.exists()
        else None
    )

    effect_objects = _collect_effect_objects(
        template_source=template_source,
        corpus_data=corpus_data,
        effect_samples=effect_samples,
        motion_library=motion_library,
    )
    effect_catalog_entries = effect_catalog.get("effects", {})
    if not isinstance(effect_catalog_entries, dict):
        raise ValueError("MOTION_RECIPE_EFFECT_CATALOG_INVALID")

    recipes = _resolve_brief_recipes(brief)
    rest_pose = _rest_pose_from_group(base_group)
    spacing = _brief_spacing(brief)
    items: list[dict[str, Any]] = []
    readback_recipes: list[dict[str, Any]] = []
    warnings: list[str] = []

    for index, recipe in enumerate(recipes):
        frame = int(recipe.get("frame", index * spacing))
        recipe_items, recipe_readback, recipe_warnings = _build_recipe_items(
            recipe=recipe,
            frame=frame,
            base_group=base_group,
            base_images=base_images,
            rest_pose=rest_pose,
            effect_objects=effect_objects,
            effect_catalog_entries=effect_catalog_entries,
        )
        items.extend(recipe_items)
        readback_recipes.append(recipe_readback)
        warnings.extend(recipe_warnings)

    items.sort(key=lambda item: (item.get("Frame", 0), item.get("Layer", 0)))
    output_data = copy.deepcopy(seed_data)
    timeline = output_data["Timelines"][0]
    timeline["Items"] = items
    timeline["CurrentFrame"] = 0
    timeline["Length"] = _timeline_length(items)
    timeline["MaxLayer"] = max(12, max((int(item.get("Layer", 0)) for item in items), default=0))

    paths.out_ymmp.parent.mkdir(parents=True, exist_ok=True)
    paths.out_readback.parent.mkdir(parents=True, exist_ok=True)
    paths.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    openability = save_openable_ymmp(output_data, paths.out_ymmp)

    written = load_ymmp(paths.out_ymmp)
    written_items = _get_timeline_items(written)
    group_items = [
        item for item in written_items
        if _item_type(item) == "GroupItem"
        and str(item.get("Remark", "")).startswith(RECIPE_REMARK_PREFIX)
    ]
    image_items = [item for item in written_items if _item_type(item) == "ImageItem"]
    paths_list = [
        item.get("FilePath", "")
        for item in image_items
        if isinstance(item, dict)
    ]

    readback = {
        "success": True,
        "artifact_kind": "g26_motion_recipe_review",
        "schema_version": "1.0",
        "status_model": {
            "review_candidate": RECIPE_STATUS_PROPOSED,
            "accepted_candidate": "requires_yymm4_visual_pass",
            "compatibility_evidence": "requires_yymm4_chain_visual_pass",
        },
        "inputs": {
            "brief": str(paths.brief),
            "seed": str(paths.seed),
            "template_source": str(paths.template_source),
            "effect_catalog": str(paths.effect_catalog),
            "effect_samples": str(paths.effect_samples) if paths.effect_samples else None,
            "motion_library": str(paths.motion_library),
            "corpus_ymmp": str(paths.corpus_ymmp) if paths.corpus_ymmp else None,
            "corpus_ymmp_used": corpus_data is not None,
        },
        "outputs": {
            "ymmp": str(paths.out_ymmp),
            "readback": str(paths.out_readback),
            "manifest": str(paths.out_manifest),
        },
        "openability": openability,
        "is_project_canvas": is_ymmp_project_canvas(written),
        "item_count": len(written_items),
        "recipe_count": len(readback_recipes),
        "recipe_group_count": len(group_items),
        "recipe_image_count": len(image_items),
        "posix_asset_paths": _count_posix_asset_paths(paths_list),
        "blank_asset_paths": sum(1 for value in paths_list if not value),
        "recommended_frames": [recipe["frame"] for recipe in readback_recipes],
        "warnings": sorted(set(warnings)),
        "recipes": readback_recipes,
    }
    paths.out_readback.write_text(
        json.dumps(readback, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    paths.out_manifest.write_text(_render_manifest(readback), encoding="utf-8")
    return readback


def _load_json(path: Path | str | None) -> Any:
    if path is None:
        return {}
    raw = Path(path).read_bytes()
    last_error: UnicodeDecodeError | None = None
    for encoding in ("utf-8-sig", "utf-8", "cp932", "shift_jis"):
        try:
            return json.loads(raw.decode(encoding))
        except UnicodeDecodeError as exc:
            last_error = exc
            continue
    if last_error is not None:
        raise last_error
    return json.loads(raw.decode("utf-8"))


def _resolve_brief_recipes(brief: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(brief, dict):
        raise ValueError("MOTION_RECIPE_BRIEF_INVALID")
    raw_recipes = brief.get("recipes")
    if raw_recipes is None:
        raw_recipes = [brief] if brief.get("motion_goal") else DEFAULT_RECIPE_ORDER
    if not isinstance(raw_recipes, list):
        raise ValueError("MOTION_RECIPE_BRIEF_RECIPES_INVALID")

    resolved: list[dict[str, Any]] = []
    for raw_recipe in raw_recipes:
        if isinstance(raw_recipe, str):
            goal_id = raw_recipe
            overrides: dict[str, Any] = {}
        elif isinstance(raw_recipe, dict):
            goal_id = raw_recipe.get("goal_id") or raw_recipe.get("id")
            if not isinstance(goal_id, str) or not goal_id:
                raise ValueError("MOTION_RECIPE_GOAL_ID_REQUIRED")
            overrides = dict(raw_recipe)
        else:
            raise ValueError("MOTION_RECIPE_ENTRY_INVALID")

        preset = DEFAULT_RECIPE_PRESETS.get(goal_id)
        if preset is None:
            raise ValueError(f"MOTION_RECIPE_UNKNOWN_GOAL: {goal_id}")
        recipe = {"goal_id": goal_id, **copy.deepcopy(preset), **overrides}
        for required_key in (
            "motion_goal",
            "emotion",
            "intensity",
            "duration_frames",
            "reset_policy",
            "forbidden_patterns",
        ):
            if required_key not in recipe:
                raise ValueError(f"MOTION_RECIPE_FIELD_REQUIRED: {goal_id}.{required_key}")
        resolved.append(recipe)
    return resolved


def _brief_spacing(brief: dict[str, Any]) -> int:
    review = brief.get("review", {})
    if isinstance(review, dict):
        spacing = review.get("spacing_frames")
        if isinstance(spacing, int) and spacing > 0:
            return spacing
    return 140


def _first_group_item(clip: Any) -> dict[str, Any]:
    for item in clip.items:
        if _item_type(item) == "GroupItem":
            return copy.deepcopy(item)
    raise ValueError("MOTION_RECIPE_TEMPLATE_SOURCE_NO_GROUP")


def _image_items(clip: Any) -> list[dict[str, Any]]:
    return [
        copy.deepcopy(item)
        for item in clip.items
        if _item_type(item) == "ImageItem"
    ]


def _rest_pose_from_group(item: dict[str, Any]) -> dict[str, float]:
    return {
        "X": _axis_values(item, "X")[0] if _axis_values(item, "X") else -102.0,
        "Y": _axis_values(item, "Y")[0] if _axis_values(item, "Y") else 462.5,
        "Zoom": _axis_values(item, "Zoom")[0] if _axis_values(item, "Zoom") else 103.8,
    }


def _build_recipe_items(
    *,
    recipe: dict[str, Any],
    frame: int,
    base_group: dict[str, Any],
    base_images: list[dict[str, Any]],
    rest_pose: dict[str, float],
    effect_objects: dict[str, dict[str, Any]],
    effect_catalog_entries: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    goal_id = str(recipe["goal_id"])
    remark = f"{RECIPE_REMARK_PREFIX}{goal_id}"
    length = int(recipe["duration_frames"])
    group = _normalize_group(
        base_group,
        frame=frame,
        length=length,
        remark=remark,
        rest_pose=rest_pose,
    )
    warnings: list[str] = []

    rotation_values = _float_list(recipe.get("rotation_values", [0.0]))
    y_values = _route_values_from_delta_or_values(
        recipe,
        axis_name="y",
        base_value=rest_pose["Y"],
    )
    zoom_values = _route_values_from_delta_or_values(
        recipe,
        axis_name="zoom",
        base_value=rest_pose["Zoom"],
    )
    _set_transform_values(group, "Rotation", rotation_values)
    _set_transform_values(group, "Y", y_values)
    _set_transform_values(group, "Zoom", zoom_values)

    effect_names = list(recipe.get("effect_names", []))
    if "CenterPointEffect" not in effect_names:
        effect_names.insert(0, "CenterPointEffect")
    effects: list[dict[str, Any]] = []
    for effect_name in effect_names:
        effect, effect_warnings = _resolve_effect(
            effect_name,
            effect_objects=effect_objects,
            effect_catalog_entries=effect_catalog_entries,
        )
        warnings.extend(effect_warnings)
        if effect is not None:
            effects.append(effect)
    group["VideoEffects"] = effects

    image_items = _clone_images(base_images, frame=frame, length=length, remark=remark)
    items = [group, *image_items]
    effect_shortlist = _effect_shortlist(recipe, effect_catalog_entries, effect_objects)
    warnings.extend(_effect_shortlist_warnings(goal_id, effect_shortlist, effect_catalog_entries))
    if not effect_shortlist:
        raise ValueError(f"MOTION_RECIPE_EFFECT_SHORTLIST_EMPTY: {goal_id}")

    readback = {
        "goal_id": goal_id,
        "status": RECIPE_STATUS_PROPOSED,
        "remark": remark,
        "frame": frame,
        "length": length,
        "layer": group.get("Layer"),
        "motion_goal": recipe["motion_goal"],
        "emotion": recipe["emotion"],
        "intensity": recipe["intensity"],
        "reset_policy": recipe["reset_policy"],
        "forbidden_patterns": list(recipe.get("forbidden_patterns", [])),
        "route_values": {
            "X": _axis_values(group, "X"),
            "Y": _axis_values(group, "Y"),
            "Rotation": _axis_values(group, "Rotation"),
            "Zoom": _axis_values(group, "Zoom"),
        },
        "used_effects": [_effect_name(effect) for effect in effects],
        "effect_shortlist": effect_shortlist,
        "expected_review": "YMM4 visual acceptance required before promotion",
    }
    return items, readback, warnings


def _normalize_group(
    item: dict[str, Any],
    *,
    frame: int,
    length: int,
    remark: str,
    rest_pose: dict[str, float],
) -> dict[str, Any]:
    group = copy.deepcopy(item)
    group["Frame"] = frame
    group["Length"] = length
    group["Layer"] = DEFAULT_LAYER
    group["GroupRange"] = DEFAULT_GROUP_RANGE
    group["Remark"] = remark
    _set_transform_values(group, "X", [rest_pose["X"]])
    _set_transform_values(group, "Y", [rest_pose["Y"]])
    _set_transform_values(group, "Zoom", [rest_pose["Zoom"]])
    _set_transform_values(group, "Rotation", [0.0])
    return group


def _clone_images(
    images: list[dict[str, Any]],
    *,
    frame: int,
    length: int,
    remark: str,
) -> list[dict[str, Any]]:
    cloned: list[dict[str, Any]] = []
    for offset, image in enumerate(images[:2]):
        new_image = copy.deepcopy(image)
        new_image["Frame"] = frame
        new_image["Length"] = length
        new_image["Layer"] = DEFAULT_LAYER + 1 + offset
        new_image["Remark"] = remark
        file_path = new_image.get("FilePath")
        if isinstance(file_path, str) and file_path:
            resolved = _resolve_repo_asset_path(file_path)
            if resolved is not None:
                new_image["FilePath"] = _format_yymm_asset_path(resolved)
        cloned.append(new_image)
    return cloned


def _set_transform_values(item: dict[str, Any], axis_name: str, values: list[float]) -> None:
    transform = copy.deepcopy(item.get(axis_name))
    if not isinstance(transform, dict):
        transform = {"Span": 0.0, "AnimationType": "なし"}
    transform["Values"] = [{"Value": float(value)} for value in values]
    if len(values) > 1:
        transform["AnimationType"] = _linear_animation_type(item)
    item[axis_name] = transform


def _linear_animation_type(item: dict[str, Any]) -> str:
    rotation = item.get("Rotation")
    if isinstance(rotation, dict) and isinstance(rotation.get("AnimationType"), str):
        return rotation["AnimationType"]
    return "直線移動"


def _route_values_from_delta_or_values(
    recipe: dict[str, Any],
    *,
    axis_name: str,
    base_value: float,
) -> list[float]:
    values_key = f"{axis_name}_values"
    delta_key = f"{axis_name}_delta_values"
    if values_key in recipe:
        return _float_list(recipe[values_key])
    if delta_key in recipe:
        return [base_value + value for value in _float_list(recipe[delta_key])]
    return [base_value]


def _float_list(value: Any) -> list[float]:
    if not isinstance(value, list):
        raise ValueError("MOTION_RECIPE_ROUTE_VALUES_INVALID")
    return [float(entry) for entry in value]


def _axis_values(item: dict[str, Any], axis_name: str) -> list[float]:
    transform = item.get(axis_name)
    if not isinstance(transform, dict):
        return []
    values = transform.get("Values")
    if not isinstance(values, list):
        return []
    result: list[float] = []
    for keyframe in values:
        if isinstance(keyframe, dict) and isinstance(keyframe.get("Value"), (int, float)):
            result.append(float(keyframe["Value"]))
    return result


def _collect_effect_objects(
    *,
    template_source: dict[str, Any],
    corpus_data: dict[str, Any] | None,
    effect_samples: Any,
    motion_library: Any,
) -> dict[str, dict[str, Any]]:
    objects: dict[str, dict[str, Any]] = {}
    for data in (template_source, corpus_data):
        if data is None:
            continue
        for item in _get_timeline_items(data):
            for effect in item.get("VideoEffects", []) if isinstance(item, dict) else []:
                if isinstance(effect, dict):
                    objects.setdefault(_effect_name(effect), copy.deepcopy(effect))

    if isinstance(effect_samples, dict):
        for name, effect in effect_samples.items():
            if isinstance(name, str) and isinstance(effect, dict):
                objects.setdefault(name, copy.deepcopy(effect))

    motions = motion_library.get("motions") if isinstance(motion_library, dict) else None
    if isinstance(motions, dict):
        for effects in motions.values():
            if not isinstance(effects, list):
                continue
            for effect in effects:
                if isinstance(effect, dict):
                    objects.setdefault(_effect_name(effect), copy.deepcopy(effect))
    return objects


def _resolve_effect(
    effect_name: str,
    *,
    effect_objects: dict[str, dict[str, Any]],
    effect_catalog_entries: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any] | None, list[str]]:
    warnings: list[str] = []
    if effect_name in effect_objects:
        effect = copy.deepcopy(effect_objects[effect_name])
    else:
        catalog_entry = effect_catalog_entries.get(effect_name)
        if not isinstance(catalog_entry, dict) or not isinstance(catalog_entry.get("$type"), str):
            warnings.append(f"EFFECT_OBJECT_MISSING:{effect_name}")
            return None, warnings
        effect = {
            "$type": catalog_entry["$type"],
            "IsEnabled": True,
            "Remark": "",
        }
        warnings.append(f"EFFECT_OBJECT_FROM_CATALOG_ONLY:{effect_name}")

    catalog_entry = effect_catalog_entries.get(effect_name)
    if isinstance(catalog_entry, dict) and catalog_entry.get("is_community") is True:
        warnings.append(f"EFFECT_REQUIRES_COMMUNITY_PLUGIN:{effect_name}")
    return effect, warnings


def _effect_shortlist(
    recipe: dict[str, Any],
    effect_catalog_entries: dict[str, dict[str, Any]],
    effect_objects: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    candidates = recipe.get("effect_candidates") or recipe.get("effect_names") or []
    shortlist: list[dict[str, Any]] = []
    for candidate in candidates:
        if not isinstance(candidate, str):
            continue
        catalog_entry = effect_catalog_entries.get(candidate, {})
        shortlist.append({
            "effect": candidate,
            "source": (
                "object"
                if candidate in effect_objects
                else "catalog"
                if candidate in effect_catalog_entries
                else "missing"
            ),
            "is_community": bool(
                isinstance(catalog_entry, dict) and catalog_entry.get("is_community")
            ),
            "category": (
                catalog_entry.get("category")
                if isinstance(catalog_entry, dict)
                else None
            ),
        })
    return shortlist


def _effect_shortlist_warnings(
    goal_id: str,
    shortlist: list[dict[str, Any]],
    effect_catalog_entries: dict[str, dict[str, Any]],
) -> list[str]:
    warnings: list[str] = []
    for entry in shortlist:
        effect_name = entry["effect"]
        if entry["source"] == "missing":
            warnings.append(f"EFFECT_SHORTLIST_MISSING:{goal_id}:{effect_name}")
        catalog_entry = effect_catalog_entries.get(effect_name)
        if isinstance(catalog_entry, dict) and catalog_entry.get("is_community") is True:
            warnings.append(f"EFFECT_SHORTLIST_COMMUNITY_PLUGIN:{goal_id}:{effect_name}")
    return warnings


def _effect_name(effect: dict[str, Any]) -> str:
    effect_type = str(effect.get("$type", ""))
    if not effect_type:
        return ""
    return effect_type.split(",")[0].split(".")[-1]


def _count_posix_asset_paths(paths: list[Any]) -> int:
    return sum(
        1
        for path in paths
        if isinstance(path, str) and "/" in path and "\\" not in path
    )


def _timeline_length(items: list[dict[str, Any]]) -> int:
    if not items:
        return 1
    return max(
        int(item.get("Frame", 0)) + max(int(item.get("Length", 1)), 1)
        for item in items
    ) + 90


def _render_manifest(readback: dict[str, Any]) -> str:
    metadata = {
        "artifact_kind": readback["artifact_kind"],
        "schema_version": readback["schema_version"],
        "recipe_count": readback["recipe_count"],
        "ymmp": readback["outputs"]["ymmp"],
        "readback": readback["outputs"]["readback"],
        "status_model": readback["status_model"],
    }
    lines = [
        "# G-26 Motion Recipe Review Manifest",
        "",
        "## Metadata",
        "",
        "```json",
        json.dumps(metadata, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Inputs",
        "",
    ]
    for key, value in readback["inputs"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend([
        "",
        "## Review Recipes",
        "",
        "| frame | recipe | status | goal | effects | route |",
        "| ---: | --- | --- | --- | --- | --- |",
    ])
    for recipe in readback["recipes"]:
        route = _route_summary(recipe["route_values"])
        effects = ", ".join(recipe["used_effects"]) or "(none)"
        lines.append(
            f"| {recipe['frame']} | `{recipe['goal_id']}` | `{recipe['status']}` | "
            f"{recipe['motion_goal']} | {effects} | {route} |"
        )
    lines.extend([
        "",
        "## Acceptance Handling",
        "",
        "- Review candidates remain `proposed` until YMM4 visual acceptance.",
        "- Promote standalone visual PASS to `accepted_candidate`.",
        "- Promote only visually accepted chains to `compatibility_evidence`.",
        "- Do not connect unaccepted recipes to G-24 production placement.",
    ])
    if readback["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- `{warning}`" for warning in readback["warnings"])
    return "\n".join(lines) + "\n"


def _route_summary(route_values: dict[str, list[float]]) -> str:
    parts: list[str] = []
    for axis_name in ("Y", "Rotation", "Zoom"):
        values = route_values.get(axis_name, [])
        if len(values) > 1:
            parts.append(f"{axis_name}={_format_values(values)}")
    return "; ".join(parts) if parts else "static/rest"


def _format_values(values: list[float]) -> str:
    return "[" + ", ".join(f"{value:g}" for value in values) + "]"
