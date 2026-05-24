"""YMM4 thumbnail template slot audit and limited patching.

サムネ用 YMM4 template copy の既存 item に付けた Remark を slot として扱い、
文字列・画像パス・最小ジオメトリだけを差し替える。画像生成や YMM4 操作はしない。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

THUMBNAIL_SLOT_RE = re.compile(r"^thumb\.(text|image)\.([A-Za-z0-9_-]+)$")

GEOMETRY_KEYS = ("x", "y", "zoom", "rotation")
GEOMETRY_FIELD_NAMES = {
    "x": "X",
    "y": "Y",
    "zoom": "Zoom",
    "rotation": "Rotation",
}

COLOR_CANDIDATES = (
    ("Color",),
    ("FontColor",),
    ("StyleColor",),
    ("ItemParameter", "Color"),
    ("ItemParameter", "FontColor"),
    ("ItemParameter", "StyleColor"),
    ("Brush", "Color"),
    ("ItemParameter", "Brush", "Color"),
)

TEXT_CANDIDATES = (
    ("Text",),
    ("ItemParameter", "Text"),
)


def load_thumbnail_patch(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8-sig") as file:
        payload = json.load(file)
    if not isinstance(payload, dict):
        raise ValueError(f"thumbnail patch JSON must be an object: {path}")
    return payload


def audit_thumbnail_template(data: dict[str, Any]) -> dict[str, Any]:
    """Return patchable thumbnail slots found in a YMM4 project."""
    slots: list[dict[str, Any]] = []
    errors: list[str] = []
    seen: dict[tuple[str, str], int] = {}

    for timeline_index, item_index, item in _iter_timeline_items(data):
        parsed = _parse_slot_remark(item.get("Remark"))
        if parsed is None:
            continue
        slot_type, slot_id = parsed
        slot_key = (slot_type, slot_id)
        seen[slot_key] = seen.get(slot_key, 0) + 1
        item_type = _item_type(item)
        text_path = _find_text_path(item)
        color_path = _find_color_path(item)
        slot = {
            "slot": f"thumb.{slot_type}.{slot_id}",
            "slot_type": slot_type,
            "slot_id": slot_id,
            "item_type": item_type,
            "timeline_index": timeline_index,
            "item_index": item_index,
            "layer": item.get("Layer"),
            "frame": item.get("Frame"),
            "length": item.get("Length"),
            "patchable_fields": {
                "text": text_path is not None,
                "file_path": item_type == "ImageItem" and "FilePath" in item,
                "color": color_path is not None,
                "x": "X" in item,
                "y": "Y" in item,
                "zoom": "Zoom" in item,
                "rotation": "Rotation" in item,
            },
        }
        if text_path is not None:
            slot["text_route"] = ".".join(text_path)
            slot["current_text"] = _get_nested(item, text_path)
        if color_path is not None:
            slot["color_route"] = ".".join(color_path)
            slot["current_color"] = _get_nested(item, color_path)
        if "FilePath" in item:
            slot["current_file_path"] = item.get("FilePath")
        slots.append(slot)

        if slot_type == "text" and text_path is None:
            errors.append(f"THUMB_TEXT_SLOT_NO_TEXT_FIELD: thumb.text.{slot_id}")
        if slot_type == "image" and item_type != "ImageItem":
            errors.append(f"THUMB_IMAGE_SLOT_NOT_IMAGE_ITEM: thumb.image.{slot_id} ({item_type})")
        elif slot_type == "image" and "FilePath" not in item:
            errors.append(f"THUMB_IMAGE_SLOT_NO_FILEPATH: thumb.image.{slot_id}")

    duplicates = [
        f"thumb.{slot_type}.{slot_id}"
        for (slot_type, slot_id), count in seen.items()
        if count > 1
    ]
    for slot in duplicates:
        errors.append(f"THUMB_SLOT_DUPLICATE: {slot}")
    if not slots:
        errors.append("THUMB_TEMPLATE_NO_SLOTS: no thumb.text.* or thumb.image.* Remark slots found")

    return {
        "success": not errors,
        "status": "ok" if not errors else "error",
        "slot_count": len(slots),
        "slots": slots,
        "errors": errors,
    }


def patch_thumbnail_template(
    data: dict[str, Any],
    patch_payload: dict[str, Any],
) -> dict[str, Any]:
    """Apply a limited thumbnail patch to existing thumb.* slots."""
    audit = audit_thumbnail_template(data)
    item_map = _slot_item_map(data)
    errors = list(audit["errors"])
    warnings: list[str] = []
    text_changes = 0
    image_changes = 0
    color_changes = 0
    geometry_changes = 0
    readback: dict[str, Any] | None = None

    if errors:
        return {
            "success": False,
            "status": "error",
            "text_changes": 0,
            "image_changes": 0,
            "color_changes": 0,
            "geometry_changes": 0,
            "errors": errors,
            "warnings": warnings,
            "readback": None,
            "audit": audit,
        }

    for slot_type, slot_id, spec in _iter_patch_specs(patch_payload):
        item = item_map.get((slot_type, slot_id))
        slot_name = f"thumb.{slot_type}.{slot_id}"
        if item is None:
            errors.append(f"THUMB_SLOT_MISSING: {slot_name}")
            continue

        if slot_type == "text":
            text_value = _extract_text_value(spec)
            if text_value is not None:
                text_path = _find_text_path(item)
                if text_path is None:
                    errors.append(f"THUMB_TEXT_SLOT_NO_TEXT_FIELD: {slot_name}")
                else:
                    _set_nested(item, text_path, text_value)
                    text_changes += 1
            color_value = _extract_color_value(spec)
            if color_value is not None:
                color_path = _find_color_path(item)
                if color_path is None:
                    warnings.append(f"THUMB_COLOR_ROUTE_MISSING: {slot_name}")
                else:
                    _set_nested(item, color_path, color_value)
                    color_changes += 1
            geometry_changes += _apply_geometry_patch(item, spec, slot_name, errors)

        if slot_type == "image":
            file_path = _extract_file_path_value(spec)
            if file_path is not None:
                if _item_type(item) != "ImageItem" or "FilePath" not in item:
                    errors.append(f"THUMB_IMAGE_SLOT_NO_FILEPATH: {slot_name}")
                else:
                    item["FilePath"] = file_path
                    image_changes += 1
            geometry_changes += _apply_geometry_patch(item, spec, slot_name, errors)

    if not errors:
        readback = verify_thumbnail_patch_readback(data, patch_payload)
        if not readback["success"]:
            errors.extend(readback["errors"])

    return {
        "success": not errors,
        "status": "ok" if not errors else "error",
        "text_changes": text_changes,
        "image_changes": image_changes,
        "color_changes": color_changes,
        "geometry_changes": geometry_changes,
        "errors": errors,
        "warnings": warnings,
        "readback": readback,
        "audit": audit,
    }


def verify_thumbnail_patch_readback(
    data: dict[str, Any],
    patch_payload: dict[str, Any],
) -> dict[str, Any]:
    """Verify that a thumbnail patch payload is visible in a patched YMM4 project."""
    item_map = _slot_item_map(data)
    checks: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []

    for slot_type, slot_id, spec in _iter_patch_specs(patch_payload):
        item = item_map.get((slot_type, slot_id))
        slot_name = f"thumb.{slot_type}.{slot_id}"
        if item is None:
            errors.append(f"THUMB_READBACK_SLOT_MISSING: {slot_name}")
            continue

        if slot_type == "text":
            text_value = _extract_text_value(spec)
            if text_value is not None:
                text_path = _find_text_path(item)
                if text_path is None:
                    errors.append(f"THUMB_READBACK_TEXT_ROUTE_MISSING: {slot_name}")
                else:
                    _append_readback_check(
                        checks,
                        errors,
                        slot_name,
                        "text",
                        text_value,
                        _get_nested(item, text_path),
                    )
            color_value = _extract_color_value(spec)
            if color_value is not None:
                color_path = _find_color_path(item)
                if color_path is None:
                    warnings.append(f"THUMB_COLOR_ROUTE_MISSING: {slot_name}")
                else:
                    _append_readback_check(
                        checks,
                        errors,
                        slot_name,
                        "color",
                        color_value,
                        _get_nested(item, color_path),
                    )
            _append_geometry_readback_checks(checks, errors, item, spec, slot_name)

        if slot_type == "image":
            file_path = _extract_file_path_value(spec)
            if file_path is not None:
                if _item_type(item) != "ImageItem" or "FilePath" not in item:
                    errors.append(f"THUMB_READBACK_IMAGE_ROUTE_MISSING: {slot_name}")
                else:
                    _append_readback_check(
                        checks,
                        errors,
                        slot_name,
                        "file_path",
                        file_path,
                        item.get("FilePath"),
                    )
            _append_geometry_readback_checks(checks, errors, item, spec, slot_name)

    return {
        "success": not errors,
        "status": "ok" if not errors else "error",
        "check_count": len(checks),
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
    }


def render_thumbnail_template_audit_text(result: dict[str, Any]) -> str:
    lines = [
        f"Thumbnail template audit: {result.get('status')}",
        f"Slots: {result.get('slot_count', 0)}",
    ]
    for slot in result.get("slots", []):
        fields = slot.get("patchable_fields", {})
        patchable = ", ".join(key for key, value in fields.items() if value) or "-"
        lines.append(
            f"- {slot['slot']} [{slot['item_type']}] "
            f"layer={slot.get('layer')} frame={slot.get('frame')} patchable={patchable}"
        )
    if result.get("errors"):
        lines.append("Errors:")
        lines.extend(f"- {error}" for error in result["errors"])
    return "\n".join(lines) + "\n"


def render_thumbnail_patch_text(result: dict[str, Any]) -> str:
    lines = [
        f"Thumbnail template patch: {result.get('status')}",
        (
            "Changes: "
            f"text={result.get('text_changes', 0)}, "
            f"image={result.get('image_changes', 0)}, "
            f"color={result.get('color_changes', 0)}, "
            f"geometry={result.get('geometry_changes', 0)}"
        ),
    ]
    if result.get("warnings"):
        lines.append("Warnings:")
        lines.extend(f"- {warning}" for warning in result["warnings"])
    readback = result.get("file_readback") or result.get("readback")
    if readback:
        lines.append(
            f"Readback: {readback.get('status')} "
            f"({readback.get('check_count', 0)} checks)"
        )
        failed = [check for check in readback.get("checks", []) if not check.get("success")]
        if failed:
            lines.extend(
                f"- {check.get('slot')}.{check.get('field')}: "
                f"expected={check.get('expected')!r} actual={check.get('actual')!r}"
                for check in failed
            )
    if result.get("errors"):
        lines.append("Errors:")
        lines.extend(f"- {error}" for error in result["errors"])
    return "\n".join(lines) + "\n"


def _iter_timeline_items(data: dict[str, Any]):
    timelines = data.get("Timelines")
    if isinstance(timelines, list):
        for timeline_index, timeline in enumerate(timelines):
            items = timeline.get("Items") if isinstance(timeline, dict) else None
            if isinstance(items, list):
                for item_index, item in enumerate(items):
                    if isinstance(item, dict):
                        yield timeline_index, item_index, item
    timeline = data.get("Timeline")
    if isinstance(timeline, dict):
        items = timeline.get("Items")
        if isinstance(items, list):
            for item_index, item in enumerate(items):
                if isinstance(item, dict):
                    yield 0, item_index, item


def _slot_item_map(data: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    item_map: dict[tuple[str, str], dict[str, Any]] = {}
    for _, _, item in _iter_timeline_items(data):
        parsed = _parse_slot_remark(item.get("Remark"))
        if parsed is not None:
            item_map[parsed] = item
    return item_map


def _parse_slot_remark(remark: Any) -> tuple[str, str] | None:
    if not isinstance(remark, str):
        return None
    match = THUMBNAIL_SLOT_RE.match(remark.strip())
    if not match:
        return None
    return match.group(1), match.group(2)


def _item_type(item: dict[str, Any]) -> str:
    raw = item.get("$type", "")
    return raw.split(",")[0].split(".")[-1] if "." in raw else str(raw)


def _iter_patch_specs(payload: dict[str, Any]):
    for slot_type in ("text", "image"):
        raw = payload.get(slot_type)
        if isinstance(raw, dict):
            for slot_id, spec in raw.items():
                yield slot_type, str(slot_id), spec

    raw_slots = payload.get("slots")
    if not isinstance(raw_slots, dict):
        return
    for raw_slot, spec in raw_slots.items():
        parsed = _parse_slot_key(str(raw_slot), spec)
        if parsed is not None:
            slot_type, slot_id = parsed
            yield slot_type, slot_id, spec


def _parse_slot_key(raw_slot: str, spec: Any) -> tuple[str, str] | None:
    parsed = _parse_slot_remark(raw_slot)
    if parsed is not None:
        return parsed
    if raw_slot.startswith("text."):
        return "text", raw_slot.split(".", 1)[1]
    if raw_slot.startswith("image."):
        return "image", raw_slot.split(".", 1)[1]
    if isinstance(spec, dict):
        slot_type = spec.get("slot_type") or spec.get("type")
        slot_id = spec.get("slot_id") or spec.get("id") or raw_slot
        if slot_type in {"text", "image"}:
            return str(slot_type), str(slot_id)
    return None


def _extract_text_value(spec: Any) -> str | None:
    if isinstance(spec, str):
        return spec
    if not isinstance(spec, dict):
        return None
    value = spec.get("value", spec.get("text"))
    return str(value) if value is not None else None


def _extract_file_path_value(spec: Any) -> str | None:
    if isinstance(spec, str):
        return spec
    if not isinstance(spec, dict):
        return None
    value = spec.get("file_path", spec.get("path"))
    return str(value) if value is not None else None


def _extract_color_value(spec: Any) -> str | None:
    if not isinstance(spec, dict):
        return None
    value = spec.get("color")
    return str(value) if value is not None else None


def _apply_geometry_patch(
    item: dict[str, Any],
    spec: Any,
    slot_name: str,
    errors: list[str],
) -> int:
    if not isinstance(spec, dict):
        return 0
    geometry = spec.get("geometry") if isinstance(spec.get("geometry"), dict) else spec
    changes = 0
    for key in GEOMETRY_KEYS:
        if key not in geometry:
            continue
        field_name = GEOMETRY_FIELD_NAMES[key]
        if field_name not in item:
            errors.append(f"THUMB_GEOMETRY_ROUTE_MISSING: {slot_name}.{field_name}")
            continue
        if _set_animation_value(item[field_name], geometry[key]):
            changes += 1
        else:
            errors.append(f"THUMB_GEOMETRY_ROUTE_UNSUPPORTED: {slot_name}.{field_name}")
    return changes


def _set_animation_value(raw: Any, value: Any) -> bool:
    if isinstance(raw, dict):
        values = raw.get("Values")
        if isinstance(values, list) and values and isinstance(values[0], dict):
            values[0]["Value"] = value
            return True
    return False


def _find_text_path(item: dict[str, Any]) -> tuple[str, ...] | None:
    for path in TEXT_CANDIDATES:
        value = _get_nested(item, path)
        if isinstance(value, str):
            return path
    return None


def _find_color_path(item: dict[str, Any]) -> tuple[str, ...] | None:
    for path in COLOR_CANDIDATES:
        value = _get_nested(item, path)
        if isinstance(value, str):
            return path
    return None


def _get_nested(raw: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = raw
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def _set_nested(raw: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    current: Any = raw
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = value


def _append_geometry_readback_checks(
    checks: list[dict[str, Any]],
    errors: list[str],
    item: dict[str, Any],
    spec: Any,
    slot_name: str,
) -> None:
    if not isinstance(spec, dict):
        return
    geometry = spec.get("geometry") if isinstance(spec.get("geometry"), dict) else spec
    for key in GEOMETRY_KEYS:
        if key not in geometry:
            continue
        field_name = GEOMETRY_FIELD_NAMES[key]
        actual = _get_animation_value(item.get(field_name))
        if actual is None:
            errors.append(f"THUMB_READBACK_GEOMETRY_ROUTE_MISSING: {slot_name}.{field_name}")
            continue
        _append_readback_check(checks, errors, slot_name, key, geometry[key], actual)


def _get_animation_value(raw: Any) -> Any:
    if isinstance(raw, dict):
        values = raw.get("Values")
        if isinstance(values, list) and values and isinstance(values[0], dict):
            return values[0].get("Value")
    return None


def _append_readback_check(
    checks: list[dict[str, Any]],
    errors: list[str],
    slot_name: str,
    field: str,
    expected: Any,
    actual: Any,
) -> None:
    success = _values_match(expected, actual)
    checks.append({
        "slot": slot_name,
        "field": field,
        "expected": expected,
        "actual": actual,
        "success": success,
    })
    if not success:
        errors.append(
            f"THUMB_READBACK_MISMATCH: {slot_name}.{field} "
            f"expected={expected!r} actual={actual!r}"
        )


def _values_match(expected: Any, actual: Any) -> bool:
    if isinstance(expected, bool) or isinstance(actual, bool):
        return expected == actual
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return float(expected) == float(actual)
    return expected == actual
