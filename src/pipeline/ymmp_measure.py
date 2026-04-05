"""YMM4 timeline route measurement helpers (G-12).

Read-only inspection for native template / effect / transition candidate routes.
This module does not patch ymmp; it surfaces where motion/bg_anim/transition
could be written safely based on actual ymmp structure.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field


@dataclass
class TimelineRouteMeasurement:
    """Summary of candidate write routes found in a ymmp file."""

    item_type_counts: dict[str, int] = field(default_factory=dict)
    route_counts: dict[str, dict[str, int]] = field(default_factory=dict)
    route_samples: dict[str, list[str]] = field(default_factory=dict)
    effect_type_counts: dict[str, int] = field(default_factory=dict)
    transition_key_counts: dict[str, int] = field(default_factory=dict)
    template_name_counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TimelineRouteValidationResult:
    """Contract check result for measured timeline routes."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    missing_routes: dict[str, list[str]] = field(default_factory=dict)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0


def _get_timeline_items(data: dict) -> list[dict]:
    """Return timeline items from either Timelines[] or legacy Timeline."""
    timelines = data.get("Timelines")
    if timelines and isinstance(timelines, list) and len(timelines) > 0:
        return timelines[0].get("Items", [])
    timeline = data.get("Timeline")
    if timeline and isinstance(timeline, dict):
        return timeline.get("Items", [])
    return []


def _item_type(item: dict) -> str:
    """Return short type name from $type."""
    raw = item.get("$type", "")
    return raw.split(",")[0].split(".")[-1] if "." in raw else raw


def _normalized(name: str) -> str:
    return name.replace("_", "").lower()


def _is_transition_leaf(normalized_leaf: str) -> bool:
    """Return True when a leaf name looks like a transition/fade route."""
    return (
        "transition" in normalized_leaf
        or normalized_leaf.endswith("fadein")
        or normalized_leaf.endswith("fadeout")
    )


def _walk(node, path: str = ""):
    """Yield (path, value) for nested dict/list structures."""
    if isinstance(node, dict):
        for key, value in node.items():
            next_path = f"{path}.{key}" if path else str(key)
            yield next_path, value
            yield from _walk(value, next_path)
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            next_path = f"{path}[{idx}]"
            yield next_path, value
            yield from _walk(value, next_path)


def _add_route(
    route_counts: dict[str, Counter],
    route_samples: dict[str, set[str]],
    category: str,
    route: str,
    sample: str,
) -> None:
    route_counts[category][route] += 1
    route_samples[category].add(sample)


def measure_timeline_routes(ymmp_data: dict) -> TimelineRouteMeasurement:
    """Inspect ymmp structure and surface candidate motion/transition/bg routes."""
    items = _get_timeline_items(ymmp_data)
    item_type_counts: Counter = Counter()
    route_counts: dict[str, Counter] = defaultdict(Counter)
    route_samples: dict[str, set[str]] = defaultdict(set)
    effect_type_counts: Counter = Counter()
    transition_key_counts: Counter = Counter()
    template_name_counts: Counter = Counter()

    for item in items:
        item_type = _item_type(item)
        item_type_counts[item_type] += 1

        if (
            item_type == "TachieItem"
            and isinstance(item.get("TachieItemParameter"), dict)
        ):
            param = item["TachieItemParameter"]
            if all(key in param for key in ("X", "Y", "Zoom")):
                _add_route(
                    route_counts,
                    route_samples,
                    "slot",
                    "TachieItem.TachieItemParameter.X/Y/Zoom",
                    item_type,
                )

        if item_type in {"ImageItem", "VideoItem"} and all(
            key in item for key in ("X", "Y", "Zoom")
        ):
            _add_route(
                route_counts,
                route_samples,
                "bg_anim",
                f"{item_type}.X/Y/Zoom",
                item_type,
            )

        if isinstance(item.get("VideoEffects"), list):
            category = "bg_anim" if item_type in {"ImageItem", "VideoItem"} else "motion"
            _add_route(
                route_counts,
                route_samples,
                category,
                f"{item_type}.VideoEffects",
                item_type,
            )
            for effect in item["VideoEffects"]:
                if isinstance(effect, dict):
                    effect_type = _item_type(effect)
                    if effect_type:
                        effect_type_counts[effect_type] += 1
                    name = effect.get("Name")
                    if isinstance(name, str) and name:
                        template_name_counts[name] += 1

        for path, value in _walk(item):
            leaf = path.rsplit(".", 1)[-1]
            normalized = _normalized(leaf)

            if _is_transition_leaf(normalized):
                route = f"{item_type}.{path}"
                _add_route(
                    route_counts,
                    route_samples,
                    "transition",
                    route,
                    item_type,
                )
                transition_key_counts[leaf] += 1

            if "template" in normalized:
                route = f"{item_type}.{path}"
                _add_route(
                    route_counts,
                    route_samples,
                    "template",
                    route,
                    item_type,
                )
                if isinstance(value, str) and value:
                    template_name_counts[value] += 1

    return TimelineRouteMeasurement(
        item_type_counts=dict(item_type_counts),
        route_counts={
            category: dict(sorted(counter.items()))
            for category, counter in sorted(route_counts.items())
        },
        route_samples={
            category: sorted(samples)
            for category, samples in sorted(route_samples.items())
        },
        effect_type_counts=dict(sorted(effect_type_counts.items())),
        transition_key_counts=dict(sorted(transition_key_counts.items())),
        template_name_counts=dict(sorted(template_name_counts.items())),
    )


def render_timeline_measurement_text(measurement: TimelineRouteMeasurement) -> str:
    """Render a compact human-readable report."""
    lines: list[str] = []

    lines.append("--- Item Types ---")
    for item_type, count in sorted(
        measurement.item_type_counts.items(),
        key=lambda x: (-x[1], x[0]),
    ):
        lines.append(f"  {item_type}: {count}")

    if measurement.route_counts:
        lines.append("")
        lines.append("--- Route Candidates ---")
        for category, routes in measurement.route_counts.items():
            lines.append(f"  [{category}]")
            for route, count in sorted(routes.items(), key=lambda x: (-x[1], x[0])):
                lines.append(f"    {route}: {count}")

    if measurement.effect_type_counts:
        lines.append("")
        lines.append("--- Effect Types ---")
        for effect_type, count in sorted(
            measurement.effect_type_counts.items(),
            key=lambda x: (-x[1], x[0]),
        ):
            lines.append(f"  {effect_type}: {count}")

    if measurement.transition_key_counts:
        lines.append("")
        lines.append("--- Transition Keys ---")
        for key, count in sorted(
            measurement.transition_key_counts.items(),
            key=lambda x: (-x[1], x[0]),
        ):
            lines.append(f"  {key}: {count}")

    if measurement.template_name_counts:
        lines.append("")
        lines.append("--- Template Names ---")
        for name, count in sorted(
            measurement.template_name_counts.items(),
            key=lambda x: (-x[1], x[0]),
        ):
            lines.append(f"  {name}: {count}")

    if measurement.route_samples:
        lines.append("")
        lines.append("--- Route Sample Coverage ---")
        for category, samples in measurement.route_samples.items():
            lines.append(f"  {category}: {', '.join(samples)}")

    return "\n".join(lines) + "\n"


def validate_timeline_route_contract(
    measurement: TimelineRouteMeasurement,
    contract: dict,
    *,
    profile: str | None = None,
) -> TimelineRouteValidationResult:
    """Validate measured routes against a simple category -> routes contract."""
    result = TimelineRouteValidationResult()
    selected = contract
    if profile:
        profiles = contract.get("profiles")
        if not isinstance(profiles, dict):
            result.errors.append(
                "TIMELINE_ROUTE_CONTRACT_INVALID: profiles must be an object"
            )
            return result
        selected = profiles.get(profile)
        if not isinstance(selected, dict):
            result.errors.append(
                "TIMELINE_ROUTE_PROFILE_UNKNOWN: "
                f"profile '{profile}' is not defined"
            )
            return result

    raw_required = selected.get("required_routes", selected)
    raw_optional = selected.get("optional_routes", {})

    if not isinstance(raw_required, dict):
        result.errors.append(
            "TIMELINE_ROUTE_CONTRACT_INVALID: required_routes must be an object"
        )
        return result
    if not isinstance(raw_optional, dict):
        result.errors.append(
            "TIMELINE_ROUTE_CONTRACT_INVALID: optional_routes must be an object"
        )
        return result

    for category, expected_routes in sorted(raw_required.items()):
        if not isinstance(expected_routes, list) or not all(
            isinstance(route, str) for route in expected_routes
        ):
            result.errors.append(
                "TIMELINE_ROUTE_CONTRACT_INVALID: "
                f"category '{category}' must map to a list of route strings"
            )
            continue

        observed = set(measurement.route_counts.get(category, {}))
        if not observed:
            result.warnings.append(
                "TIMELINE_ROUTE_CATEGORY_EMPTY: "
                f"category '{category}' has no observed candidate routes"
            )

        missing = sorted(route for route in expected_routes if route not in observed)
        if missing:
            result.missing_routes[category] = missing
            for route in missing:
                result.errors.append(
                    "TIMELINE_ROUTE_MISS: "
                    f"category '{category}' is missing route '{route}'"
                )

    for category, expected_routes in sorted(raw_optional.items()):
        if not isinstance(expected_routes, list) or not all(
            isinstance(route, str) for route in expected_routes
        ):
            result.errors.append(
                "TIMELINE_ROUTE_CONTRACT_INVALID: "
                f"optional category '{category}' must map to a list of route strings"
            )
            continue

        observed = set(measurement.route_counts.get(category, {}))
        missing = sorted(route for route in expected_routes if route not in observed)
        for route in missing:
            result.warnings.append(
                "TIMELINE_ROUTE_OPTIONAL_MISS: "
                f"category '{category}' is missing optional route '{route}'"
            )

    return result
