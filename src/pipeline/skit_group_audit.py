from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from src.pipeline.ymmp_patch import _parse_motion_target_layers, _resolve_carry_forward


FAIL_CANONICAL_MISSING = "SKIT_CANONICAL_GROUP_MISSING"
FAIL_CANONICAL_AMBIGUOUS = "SKIT_CANONICAL_GROUP_AMBIGUOUS"
FAIL_REGISTRY_INVALID = "SKIT_TEMPLATE_REGISTRY_INVALID"
FAIL_FALLBACK_MISS = "SKIT_TEMPLATE_FALLBACK_MISS"
FAIL_GROUP_MISMATCH = "SKIT_TEMPLATE_GROUP_MISMATCH"


@dataclass
class SkitResolutionEntry:
    index: int | None
    requested_intent: str
    resolution: str
    template_name: str | None
    manual_checks: list[str] = field(default_factory=list)
    note: str | None = None


@dataclass
class SkitGroupAuditResult:
    status: str
    group_key: str | None = None
    anchor_remark: str | None = None
    anchor_layer: int | None = None
    entries: list[SkitResolutionEntry] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    summary: dict[str, int] = field(
        default_factory=lambda: {"exact": 0, "fallback": 0, "manual_note": 0}
    )

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["entries"] = [asdict(entry) for entry in self.entries]
        return payload


@dataclass
class _AnchorMatch:
    group_key: str
    remark: str
    layer: int


@dataclass
class _TemplateSpec:
    registry_key: str
    group_key: str
    intent: str
    template_name: str
    manual_checks: list[str]


@dataclass
class _CanonicalGroupSpec:
    group_key: str
    group_remark: str
    manual_checks: list[str]


@dataclass
class _RegistrySpec:
    canonical_groups: dict[str, _CanonicalGroupSpec]
    templates: dict[str, _TemplateSpec]
    intent_fallbacks: dict[str, str]


def load_skit_group_registry(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        raise ValueError("skit_group_registry JSON must be an object")
    return raw


def audit_skit_group(ymmp_data: dict, ir_data: dict, registry_data: dict) -> SkitGroupAuditResult:
    errors: list[str] = []
    spec = _parse_registry(registry_data, errors)
    if spec is None:
        return SkitGroupAuditResult(status="error", errors=errors)

    anchors = _find_anchor_matches(ymmp_data, spec.canonical_groups)
    if not anchors:
        errors.append(
            f"{FAIL_CANONICAL_MISSING}: no GroupItem.Remark matches any canonical group remark"
        )
        return SkitGroupAuditResult(status="error", errors=errors)
    if len(anchors) > 1:
        desc = ", ".join(
            f"{anchor.group_key}@layer:{anchor.layer}:{anchor.remark}" for anchor in anchors
        )
        errors.append(
            f"{FAIL_CANONICAL_AMBIGUOUS}: multiple canonical group anchors matched: {desc}"
        )
        return SkitGroupAuditResult(status="error", errors=errors)

    anchor = anchors[0]
    result = SkitGroupAuditResult(
        status="ok",
        group_key=anchor.group_key,
        anchor_remark=anchor.remark,
        anchor_layer=anchor.layer,
    )

    resolved = _resolve_carry_forward(ir_data)
    for entry in resolved:
        motion = entry.get("motion")
        if not isinstance(motion, str) or not motion or motion == "none":
            continue
        layers = _parse_motion_target_layers(entry.get("motion_target"))
        if not layers or anchor.layer not in layers:
            continue

        resolution, entry_errors = _resolve_entry(
            entry=entry,
            requested_intent=motion,
            anchor_group_key=anchor.group_key,
            canonical_groups=spec.canonical_groups,
            templates=spec.templates,
            intent_fallbacks=spec.intent_fallbacks,
        )
        if entry_errors:
            errors.extend(entry_errors)
            continue
        result.entries.append(resolution)
        result.summary[resolution.resolution] += 1

    if errors:
        result.status = "error"
        result.errors = errors
    return result


def render_skit_group_audit_text(result: SkitGroupAuditResult) -> str:
    lines = ["--- Skit Group Preflight ---"]
    if result.group_key:
        lines.append(f"Anchor group : {result.group_key}")
    if result.anchor_remark:
        lines.append(f"Anchor remark: {result.anchor_remark}")
    if result.anchor_layer is not None:
        lines.append(f"Anchor layer : {result.anchor_layer}")

    if result.entries:
        lines.append("")
        lines.append("Resolutions:")
        for entry in result.entries:
            lines.append(
                f"  utt {entry.index}: {entry.requested_intent} -> {entry.resolution}"
                + (f" ({entry.template_name})" if entry.template_name else "")
            )
            if entry.manual_checks:
                lines.append(f"    manual_checks: {', '.join(entry.manual_checks)}")
            if entry.note:
                lines.append(f"    note: {entry.note}")
    else:
        lines.append("")
        lines.append("Resolutions: none")

    lines.append("")
    lines.append(
        "Summary: "
        f"exact={result.summary.get('exact', 0)}, "
        f"fallback={result.summary.get('fallback', 0)}, "
        f"manual_note={result.summary.get('manual_note', 0)}"
    )

    if result.errors:
        lines.append("")
        lines.append("Errors:")
        for error in result.errors:
            lines.append(f"  {error}")
    return "\n".join(lines)


def _resolve_entry(
    *,
    entry: dict,
    requested_intent: str,
    anchor_group_key: str,
    canonical_groups: dict[str, _CanonicalGroupSpec],
    templates: dict[str, _TemplateSpec],
    intent_fallbacks: dict[str, str],
) -> tuple[SkitResolutionEntry | None, list[str]]:
    exact_matches = [
        spec for spec in templates.values()
        if spec.group_key == anchor_group_key and spec.intent == requested_intent
    ]
    if len(exact_matches) > 1:
        names = ", ".join(spec.template_name for spec in exact_matches)
        return None, [
            f"{FAIL_REGISTRY_INVALID}: multiple exact templates for group '{anchor_group_key}' and intent '{requested_intent}': {names}"
        ]
    if len(exact_matches) == 1:
        spec = exact_matches[0]
        return SkitResolutionEntry(
            index=_coerce_index(entry.get("index")),
            requested_intent=requested_intent,
            resolution="exact",
            template_name=spec.template_name,
            manual_checks=list(spec.manual_checks),
        ), []

    fallback_template_name = intent_fallbacks.get(requested_intent)
    if fallback_template_name:
        fallback_match = _find_template_by_name(templates, fallback_template_name)
        if fallback_match is None:
            return None, [
                f"{FAIL_FALLBACK_MISS}: intent '{requested_intent}' maps to unknown template '{fallback_template_name}'"
            ]
        if fallback_match.group_key != anchor_group_key:
            return None, [
                f"{FAIL_GROUP_MISMATCH}: fallback template '{fallback_match.template_name}' belongs to group '{fallback_match.group_key}', expected '{anchor_group_key}'"
            ]
        return SkitResolutionEntry(
            index=_coerce_index(entry.get("index")),
            requested_intent=requested_intent,
            resolution="fallback",
            template_name=fallback_match.template_name,
            manual_checks=list(fallback_match.manual_checks),
            note="resolved via intent_fallbacks",
        ), []

    canonical = canonical_groups[anchor_group_key]
    return SkitResolutionEntry(
        index=_coerce_index(entry.get("index")),
        requested_intent=requested_intent,
        resolution="manual_note",
        template_name=None,
        manual_checks=list(canonical.manual_checks),
        note="intent not registered",
    ), []


def _coerce_index(value: object) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _find_template_by_name(
    templates: dict[str, _TemplateSpec],
    template_name: str,
) -> _TemplateSpec | None:
    for spec in templates.values():
        if spec.template_name == template_name:
            return spec
    return None


def _parse_registry(
    registry_data: dict,
    errors: list[str],
) -> _RegistrySpec | None:
    canonical_raw = registry_data.get("canonical_groups")
    if not isinstance(canonical_raw, dict) or not canonical_raw:
        errors.append(
            f"{FAIL_REGISTRY_INVALID}: canonical_groups must be a non-empty object"
        )
        return None

    templates_raw = registry_data.get("templates")
    if not isinstance(templates_raw, dict):
        errors.append(f"{FAIL_REGISTRY_INVALID}: templates must be an object")
        return None

    intent_fallbacks_raw = registry_data.get("intent_fallbacks", {})
    if not isinstance(intent_fallbacks_raw, dict):
        errors.append(
            f"{FAIL_REGISTRY_INVALID}: intent_fallbacks must be an object when present"
        )
        return None

    canonical_groups: dict[str, _CanonicalGroupSpec] = {}
    seen_remarks: set[str] = set()
    for group_key, raw in canonical_raw.items():
        if not isinstance(raw, dict):
            errors.append(
                f"{FAIL_REGISTRY_INVALID}: canonical_groups['{group_key}'] must be an object"
            )
            continue
        group_remark = raw.get("group_remark")
        if not isinstance(group_remark, str) or not group_remark.strip():
            errors.append(
                f"{FAIL_REGISTRY_INVALID}: canonical_groups['{group_key}'].group_remark must be a non-empty string"
            )
            continue
        if group_remark in seen_remarks:
            errors.append(
                f"{FAIL_REGISTRY_INVALID}: duplicate canonical group remark '{group_remark}'"
            )
            continue
        seen_remarks.add(group_remark)
        manual_checks = _parse_string_list(
            raw.get("manual_checks", []),
            f"canonical_groups['{group_key}'].manual_checks",
            errors,
        )
        canonical_groups[str(group_key)] = _CanonicalGroupSpec(
            group_key=str(group_key),
            group_remark=group_remark,
            manual_checks=manual_checks,
        )

    templates: dict[str, _TemplateSpec] = {}
    seen_template_names: set[str] = set()
    for registry_key, raw in templates_raw.items():
        if not isinstance(raw, dict):
            errors.append(
                f"{FAIL_REGISTRY_INVALID}: templates['{registry_key}'] must be an object"
            )
            continue
        group_key = raw.get("group_key")
        intent = raw.get("intent")
        template_name = raw.get("template_name")
        if not isinstance(group_key, str) or group_key not in canonical_groups:
            errors.append(
                f"{FAIL_REGISTRY_INVALID}: templates['{registry_key}'].group_key must reference canonical_groups"
            )
            continue
        if not isinstance(intent, str) or not intent.strip():
            errors.append(
                f"{FAIL_REGISTRY_INVALID}: templates['{registry_key}'].intent must be a non-empty string"
            )
            continue
        if not isinstance(template_name, str) or not template_name.strip():
            errors.append(
                f"{FAIL_REGISTRY_INVALID}: templates['{registry_key}'].template_name must be a non-empty string"
            )
            continue
        if template_name in seen_template_names:
            errors.append(
                f"{FAIL_REGISTRY_INVALID}: duplicate template_name '{template_name}'"
            )
            continue
        seen_template_names.add(template_name)
        manual_checks = _parse_string_list(
            raw.get("manual_checks", []),
            f"templates['{registry_key}'].manual_checks",
            errors,
        )
        templates[str(registry_key)] = _TemplateSpec(
            registry_key=str(registry_key),
            group_key=group_key,
            intent=intent,
            template_name=template_name,
            manual_checks=manual_checks,
        )

    intent_fallbacks: dict[str, str] = {}
    for intent, template_name in intent_fallbacks_raw.items():
        if not isinstance(intent, str) or not intent.strip():
            errors.append(
                f"{FAIL_REGISTRY_INVALID}: intent_fallbacks key must be a non-empty string"
            )
            continue
        if not isinstance(template_name, str) or not template_name.strip():
            errors.append(
                f"{FAIL_REGISTRY_INVALID}: intent_fallbacks['{intent}'] must be a non-empty string"
            )
            continue
        intent_fallbacks[intent] = template_name

    if errors:
        return None
    return _RegistrySpec(
        canonical_groups=canonical_groups,
        templates=templates,
        intent_fallbacks=intent_fallbacks,
    )


def _parse_string_list(value: object, label: str, errors: list[str]) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(elem, str) for elem in value):
        errors.append(
            f"{FAIL_REGISTRY_INVALID}: {label} must be a list of strings"
        )
        return []
    return list(value)


def _find_anchor_matches(
    ymmp_data: dict,
    canonical_groups: dict[str, _CanonicalGroupSpec],
) -> list[_AnchorMatch]:
    items = _get_timeline_items(ymmp_data)
    remark_to_group = {
        spec.group_remark: spec.group_key for spec in canonical_groups.values()
    }
    matches: list[_AnchorMatch] = []
    for item in items:
        if _item_type(item) != "GroupItem":
            continue
        remark = item.get("Remark")
        if not isinstance(remark, str):
            continue
        group_key = remark_to_group.get(remark)
        if not group_key:
            continue
        layer = item.get("Layer")
        if not isinstance(layer, int):
            continue
        matches.append(_AnchorMatch(group_key=group_key, remark=remark, layer=layer))
    return matches


def _item_type(item: dict) -> str:
    return item.get("$type", "").split(",")[0].split(".")[-1]


def _get_timeline_items(ymmp_data: dict) -> list[dict]:
    timelines = ymmp_data.get("Timelines") or []
    if not timelines:
        return []
    selected_index = ymmp_data.get("SelectedTimelineIndex", 0)
    if not isinstance(selected_index, int) or not (0 <= selected_index < len(timelines)):
        selected_index = 0
    timeline = timelines[selected_index]
    items = timeline.get("Items")
    return items if isinstance(items, list) else []
