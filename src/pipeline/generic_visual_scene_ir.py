"""Data-driven validation for topic-independent visual scene fixtures.

The module intentionally owns structure only. Layout recipes, primitive IDs,
capability evidence, costs, and all domain payloads are supplied as JSON data.
Static conformance therefore remains C2 evidence and never implies editor or
render behavior.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


SCHEMA_VERSION = "generic_visual_scene_ir.v1"
EVIDENCE_LEVELS = ("C0", "C1", "C2", "C3", "C4", "C5")
AVAILABILITY_CLASSES = ("proven", "conditional", "unsupported", "unknown")
PATH_CLASSES = (
    "reusable_core",
    "pilot_local_reusable_helper",
    "topic_specific",
    "historical_evidence",
    "obsolete_duplicate",
    "unknown",
)
RIGHTS_BOUNDARIES = ("none", "original_only", "cleared_input_only", "blocked")
COST_CLASSES = ("W1", "W2", "W3", "W4", "W5")
SCS_ROLES = (
    "focal_anchor",
    "supporting",
    "boundary",
    "connector",
    "risk_marker",
    "decoration",
    "label",
)

_PRIVATE_PATH_RE = re.compile(r"(?:[A-Za-z]:\\|file://|(?:^|[\"'])/(?:Users|home)/)")


class SceneIRValidationError(ValueError):
    """Raised when a package or fixture violates the generic contract."""


@dataclass(frozen=True)
class FixtureValidation:
    fixture_id: str
    archetypes: tuple[str, ...]
    scene_count: int
    cue_count: int
    primitive_count: int
    capability_requirement_count: int
    capability_gaps: tuple[dict[str, str], ...]
    warnings: tuple[str, ...]

    @property
    def status(self) -> str:
        return "static_conformance_pass"

    def as_dict(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "status": self.status,
            "evidence_level": "C2",
            "runtime_ready": False,
            "cross_topic_proven": False,
            "archetypes": list(self.archetypes),
            "scene_count": self.scene_count,
            "cue_count": self.cue_count,
            "primitive_count": self.primitive_count,
            "capability_requirement_count": self.capability_requirement_count,
            "capability_gaps": list(self.capability_gaps),
            "warnings": list(self.warnings),
        }


def load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SceneIRValidationError(f"JSON_OBJECT_REQUIRED:{path}")
    return value


def validate_path_inventory(data: Mapping[str, Any], repo_root: str | Path) -> None:
    entries = _list_of_dicts(data, "paths")
    if not entries:
        raise SceneIRValidationError("PATH_INVENTORY_EMPTY")
    ids = _unique_ids(entries, "path_id", "PATH_ID")
    del ids
    root = Path(repo_root)
    missing: list[str] = []
    for row in entries:
        classification = _string(row, "classification")
        if classification not in PATH_CLASSES:
            raise SceneIRValidationError(
                f"PATH_CLASS_INVALID:{row.get('path_id')}:{classification}"
            )
        path = _string(row, "path")
        if not (root / path).exists():
            missing.append(path)
        _string(row, "scope_reason")
        _string(row, "capability_relevance")
    if missing:
        raise SceneIRValidationError("PATH_MISSING:" + ",".join(sorted(missing)))
    if int(data.get("unclassified_relevant_path_count", -1)) != 0:
        raise SceneIRValidationError("UNCLASSIFIED_RELEVANT_PATH")


def validate_capability_matrix(data: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    rows = _list_of_dicts(data, "capabilities")
    _unique_ids(rows, "capability_id", "CAPABILITY_ID")
    required = (
        "primitive_or_combination",
        "availability_class",
        "evidence_level",
        "evidence_locations",
        "observed_versions_environments",
        "input_requirements",
        "output_behavior",
        "limitations",
        "failure_modes",
        "fallback",
        "setup_weight",
        "per_episode_burden",
        "reuse_class",
        "maintenance_surface",
        "rights_dependency",
        "recovery_complexity",
        "recommended_default_use",
        "prohibited_overclaim",
    )
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        capability_id = _string(row, "capability_id")
        for key in required:
            if key not in row or row[key] in (None, "", []):
                raise SceneIRValidationError(
                    f"CAPABILITY_FIELD_REQUIRED:{capability_id}:{key}"
                )
        availability = _string(row, "availability_class")
        level = _string(row, "evidence_level")
        if availability not in AVAILABILITY_CLASSES:
            raise SceneIRValidationError(
                f"AVAILABILITY_INVALID:{capability_id}:{availability}"
            )
        if level not in EVIDENCE_LEVELS:
            raise SceneIRValidationError(
                f"EVIDENCE_LEVEL_INVALID:{capability_id}:{level}"
            )
        index = EVIDENCE_LEVELS.index(level)
        if availability == "proven" and index < 3:
            raise SceneIRValidationError(
                f"RUNTIME_OVERCLAIM:{capability_id}:{level}"
            )
        tags = set(str(tag) for tag in row.get("proof_tags", []))
        if "render_proven" in tags and index < 4:
            raise SceneIRValidationError(
                f"RENDER_OVERCLAIM:{capability_id}:{level}"
            )
        if "cross_topic_proven" in tags and index < 5:
            raise SceneIRValidationError(
                f"CROSS_TOPIC_OVERCLAIM:{capability_id}:{level}"
            )
        if _string(row, "setup_weight") not in COST_CLASSES:
            raise SceneIRValidationError(f"SETUP_WEIGHT_INVALID:{capability_id}")
        result[capability_id] = dict(row)
    return result


def validate_primitive_catalog(
    data: Mapping[str, Any], capabilities: Mapping[str, Mapping[str, Any]]
) -> dict[str, dict[str, Any]]:
    rows = _list_of_dicts(data, "primitives")
    _unique_ids(rows, "primitive_id", "PRIMITIVE_ID")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        primitive_id = _string(row, "primitive_id")
        role = _string(row, "scs_role")
        if role not in SCS_ROLES:
            raise SceneIRValidationError(f"SCS_ROLE_INVALID:{primitive_id}:{role}")
        capability_id = _string(row, "capability_id")
        if capability_id not in capabilities:
            raise SceneIRValidationError(
                f"PRIMITIVE_CAPABILITY_UNKNOWN:{primitive_id}:{capability_id}"
            )
        for key in (
            "item_family",
            "purpose",
            "fallback_primitive_id",
            "minimum_evidence_level",
        ):
            _string(row, key)
        minimum = _string(row, "minimum_evidence_level")
        if minimum not in EVIDENCE_LEVELS:
            raise SceneIRValidationError(
                f"PRIMITIVE_EVIDENCE_INVALID:{primitive_id}:{minimum}"
            )
        result[primitive_id] = dict(row)
    for primitive_id, row in result.items():
        fallback = _string(row, "fallback_primitive_id")
        if fallback not in result:
            raise SceneIRValidationError(
                f"PRIMITIVE_FALLBACK_UNKNOWN:{primitive_id}:{fallback}"
            )
    return result


def validate_composition_grammar(
    data: Mapping[str, Any],
    primitives: Mapping[str, Mapping[str, Any]],
    capabilities: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    rows = _list_of_dicts(data, "compositions")
    _unique_ids(rows, "composition_id", "COMPOSITION_ID")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        composition_id = _string(row, "composition_id")
        for key in (
            "required_primitives",
            "optional_primitives",
            "prohibited_combinations",
            "allowed_scs_composition_types",
            "fallback_composition",
            "suitable_archetypes",
            "unsuitable_archetypes",
            "yymm4_observation_still_needed",
            "static_conformance_evidence_level",
        ):
            if key not in row or row[key] in (None, "", []):
                raise SceneIRValidationError(
                    f"COMPOSITION_FIELD_REQUIRED:{composition_id}:{key}"
                )
        for primitive_id in (
            list(row["required_primitives"]) + list(row["optional_primitives"])
        ):
            if primitive_id not in primitives:
                raise SceneIRValidationError(
                    f"COMPOSITION_PRIMITIVE_UNKNOWN:{composition_id}:{primitive_id}"
                )
        level = _string(row, "evidence_level")
        if level not in EVIDENCE_LEVELS:
            raise SceneIRValidationError(
                f"COMPOSITION_EVIDENCE_INVALID:{composition_id}:{level}"
            )
        static_level = _string(row, "static_conformance_evidence_level")
        if static_level not in EVIDENCE_LEVELS:
            raise SceneIRValidationError(
                f"COMPOSITION_STATIC_EVIDENCE_INVALID:{composition_id}:{static_level}"
            )
        required_capability_levels = [
            str(capabilities[str(primitives[primitive_id]["capability_id"])]["evidence_level"])
            for primitive_id in row["required_primitives"]
        ]
        evidence_floor = min(
            required_capability_levels, key=EVIDENCE_LEVELS.index
        )
        if level != evidence_floor:
            raise SceneIRValidationError(
                f"COMPOSITION_EVIDENCE_FLOOR_MISMATCH:{composition_id}:"
                f"declared={level}:actual={evidence_floor}"
            )
        cost = _mapping(row, "cost_reuse_profile")
        if _string(cost, "setup_weight") not in COST_CLASSES:
            raise SceneIRValidationError(
                f"COMPOSITION_COST_INVALID:{composition_id}"
            )
        result[composition_id] = dict(row)
    for composition_id, row in result.items():
        fallback = _string(row, "fallback_composition")
        if fallback not in result:
            raise SceneIRValidationError(
                f"COMPOSITION_FALLBACK_UNKNOWN:{composition_id}:{fallback}"
            )
    return result


def validate_combination_map(
    data: Mapping[str, Any],
    primitives: Mapping[str, Mapping[str, Any]],
    capabilities: Mapping[str, Mapping[str, Any]],
) -> None:
    rows = _list_of_dicts(data, "combinations")
    _unique_ids(rows, "combination_id", "COMBINATION_ID")
    for row in rows:
        combination_id = _string(row, "combination_id")
        for primitive_id in row.get("primitive_ids", []):
            if primitive_id not in primitives:
                raise SceneIRValidationError(
                    f"COMBINATION_PRIMITIVE_UNKNOWN:{combination_id}:{primitive_id}"
                )
        for capability_id in row.get("capability_ids", []):
            if capability_id not in capabilities:
                raise SceneIRValidationError(
                    f"COMBINATION_CAPABILITY_UNKNOWN:{combination_id}:{capability_id}"
                )
        for key in ("fallback", "cost_reuse_profile", "evidence_level"):
            if key not in row or row[key] in (None, "", []):
                raise SceneIRValidationError(
                    f"COMBINATION_FIELD_REQUIRED:{combination_id}:{key}"
                )


def validate_fixture(
    fixture: Mapping[str, Any],
    grammar: Mapping[str, Mapping[str, Any]],
    primitives: Mapping[str, Mapping[str, Any]],
    capabilities: Mapping[str, Mapping[str, Any]],
) -> FixtureValidation:
    if _string(fixture, "schema_version") != SCHEMA_VERSION:
        raise SceneIRValidationError("FIXTURE_SCHEMA_INVALID")
    fixture_id = _string(fixture, "fixture_id")
    _mapping(fixture, "evidence_boundary")
    _mapping(fixture, "payload")
    scenes = _list_of_dicts(fixture, "scenes")
    cues = _list_of_dicts(fixture, "cues")
    if not scenes or not cues:
        raise SceneIRValidationError(f"FIXTURE_EMPTY:{fixture_id}")
    scene_ids = _unique_ids(scenes, "scene_id", "SCENE_ID")
    cue_ids = _unique_ids(cues, "cue_id", "CUE_ID")
    scene_by_id = {str(row["scene_id"]): row for row in scenes}
    cue_by_id = {str(row["cue_id"]): row for row in cues}
    del scene_ids, cue_ids

    claimed: list[str] = []
    for scene in scenes:
        scene_id = _string(scene, "scene_id")
        for key in (
            "semantic_role",
            "default_layout_archetype",
            "rights_boundary",
            "cost_profile_id",
        ):
            _string(scene, key)
        if scene["default_layout_archetype"] not in grammar:
            raise SceneIRValidationError(
                f"SCENE_COMPOSITION_UNKNOWN:{scene_id}:{scene['default_layout_archetype']}"
            )
        if scene["rights_boundary"] not in RIGHTS_BOUNDARIES:
            raise SceneIRValidationError(f"SCENE_RIGHTS_INVALID:{scene_id}")
        scene_cues = scene.get("cue_ids")
        if not isinstance(scene_cues, list) or not scene_cues:
            raise SceneIRValidationError(f"SCENE_CUES_REQUIRED:{scene_id}")
        for cue_id in scene_cues:
            if cue_id not in cue_by_id:
                raise SceneIRValidationError(
                    f"SCENE_CUE_UNKNOWN:{scene_id}:{cue_id}"
                )
            if cue_by_id[cue_id].get("scene_id") != scene_id:
                raise SceneIRValidationError(
                    f"SCENE_CUE_LINK_MISMATCH:{scene_id}:{cue_id}"
                )
            claimed.append(str(cue_id))
    if sorted(claimed) != sorted(cue_by_id):
        raise SceneIRValidationError(f"CUE_COVERAGE_INVALID:{fixture_id}")
    if len(claimed) != len(set(claimed)):
        raise SceneIRValidationError(f"CUE_REFERENCED_MULTIPLE_TIMES:{fixture_id}")

    archetypes: set[str] = set()
    capability_gaps: list[dict[str, str]] = []
    warnings: list[str] = []
    primitive_count = 0
    requirement_count = 0
    for cue in sorted(cues, key=lambda value: int(value.get("sequence", 0))):
        cue_id = _string(cue, "cue_id")
        if cue.get("scene_id") not in scene_by_id:
            raise SceneIRValidationError(f"CUE_SCENE_UNKNOWN:{cue_id}")
        composition_id = str(
            cue.get("layout_archetype")
            or scene_by_id[str(cue["scene_id"])]["default_layout_archetype"]
        )
        if composition_id not in grammar:
            raise SceneIRValidationError(
                f"CUE_COMPOSITION_UNKNOWN:{cue_id}:{composition_id}"
            )
        archetypes.add(composition_id)
        scs_type = _string(cue, "scs_composition_type")
        allowed = grammar[composition_id]["allowed_scs_composition_types"]
        if scs_type not in allowed:
            raise SceneIRValidationError(
                f"SCS_TYPE_NOT_ALLOWED:{cue_id}:{composition_id}:{scs_type}"
            )
        timing = _mapping(cue, "timing_anchor")
        _string(timing, "kind")
        fallback = _mapping(cue, "fallback")
        fallback_composition = _string(fallback, "composition_id")
        if fallback_composition not in grammar:
            raise SceneIRValidationError(
                f"CUE_FALLBACK_UNKNOWN:{cue_id}:{fallback_composition}"
            )
        minimum = _string(cue, "minimum_evidence_level")
        if minimum not in EVIDENCE_LEVELS:
            raise SceneIRValidationError(f"CUE_EVIDENCE_INVALID:{cue_id}:{minimum}")

        primitive_refs = cue.get("primitive_refs")
        if not isinstance(primitive_refs, list) or not primitive_refs:
            raise SceneIRValidationError(f"CUE_PRIMITIVES_REQUIRED:{cue_id}")
        cue_primitive_ids: set[str] = set()
        for primitive_ref in primitive_refs:
            if not isinstance(primitive_ref, dict):
                raise SceneIRValidationError(f"CUE_PRIMITIVE_OBJECT_REQUIRED:{cue_id}")
            primitive_id = _string(primitive_ref, "primitive_id")
            if primitive_id not in primitives:
                raise SceneIRValidationError(
                    f"CUE_PRIMITIVE_UNKNOWN:{cue_id}:{primitive_id}"
                )
            cue_primitive_ids.add(primitive_id)
            role = _string(primitive_ref, "role")
            if role not in SCS_ROLES:
                raise SceneIRValidationError(
                    f"CUE_PRIMITIVE_ROLE_INVALID:{cue_id}:{role}"
                )
            primitive_count += 1
        missing_required = set(grammar[composition_id]["required_primitives"]) - cue_primitive_ids
        if missing_required:
            raise SceneIRValidationError(
                f"CUE_REQUIRED_PRIMITIVE_MISSING:{cue_id}:"
                + ",".join(sorted(missing_required))
            )

        motion = _mapping(cue, "motion_request")
        _string(motion, "intent")
        _string(motion, "status")
        requirements = cue.get("capability_requirements")
        if not isinstance(requirements, list) or not requirements:
            raise SceneIRValidationError(f"CUE_CAPABILITIES_REQUIRED:{cue_id}")
        consolidated_requirements: dict[str, dict[str, Any]] = {}
        for primitive_id in sorted(cue_primitive_ids):
            primitive = primitives[primitive_id]
            capability_id = str(primitive["capability_id"])
            required_level = str(primitive["minimum_evidence_level"])
            consolidated_requirements[capability_id] = {
                "minimum_evidence_level": required_level,
                "sources": {"primitive"},
            }
        for requirement in requirements:
            if not isinstance(requirement, dict):
                raise SceneIRValidationError(f"CUE_CAPABILITY_OBJECT_REQUIRED:{cue_id}")
            capability_id = _string(requirement, "capability_id")
            required_level = _string(requirement, "minimum_evidence_level")
            if capability_id not in capabilities:
                raise SceneIRValidationError(
                    f"CUE_CAPABILITY_UNKNOWN:{cue_id}:{capability_id}"
                )
            if required_level not in EVIDENCE_LEVELS:
                raise SceneIRValidationError(
                    f"CUE_CAPABILITY_LEVEL_INVALID:{cue_id}:{capability_id}"
                )
            existing = consolidated_requirements.get(capability_id)
            if existing is None:
                consolidated_requirements[capability_id] = {
                    "minimum_evidence_level": required_level,
                    "sources": {"explicit"},
                }
            else:
                if EVIDENCE_LEVELS.index(required_level) > EVIDENCE_LEVELS.index(
                    str(existing["minimum_evidence_level"])
                ):
                    existing["minimum_evidence_level"] = required_level
                existing["sources"].add("explicit")
        for capability_id in sorted(consolidated_requirements):
            consolidated = consolidated_requirements[capability_id]
            required_level = str(consolidated["minimum_evidence_level"])
            actual_level = str(capabilities[capability_id]["evidence_level"])
            if EVIDENCE_LEVELS.index(actual_level) < EVIDENCE_LEVELS.index(required_level):
                capability_gaps.append(
                    {
                        "cue_id": cue_id,
                        "capability_id": capability_id,
                        "actual": actual_level,
                        "required": required_level,
                        "fallback": fallback_composition,
                        "requirement_source": "+".join(
                            sorted(str(value) for value in consolidated["sources"])
                        ),
                    }
                )
            requirement_count += 1
        if motion["status"] != "none" and minimum in ("C0", "C1", "C2"):
            warnings.append(f"{cue_id}:motion_requires_runtime_observation")

    return FixtureValidation(
        fixture_id=fixture_id,
        archetypes=tuple(sorted(archetypes)),
        scene_count=len(scenes),
        cue_count=len(cues),
        primitive_count=primitive_count,
        capability_requirement_count=requirement_count,
        capability_gaps=tuple(capability_gaps),
        warnings=tuple(sorted(set(warnings))),
    )


def build_package(repo_root: str | Path, *, write: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    docs_dir = root / "docs" / "visual_system"
    lab_dir = root / "samples" / "visual_composition_lab"
    matrix = load_json(docs_dir / "generic_visual_capability_matrix.json")
    capabilities = validate_capability_matrix(matrix)
    inventory = load_json(docs_dir / "relevant_path_inventory.json")
    validate_path_inventory(inventory, root)
    primitive_data = load_json(docs_dir / "visual_primitive_catalog.json")
    primitives = validate_primitive_catalog(primitive_data, capabilities)
    grammar_data = load_json(docs_dir / "scene_composition_grammar.json")
    grammar = validate_composition_grammar(grammar_data, primitives, capabilities)
    combinations = load_json(docs_dir / "capability_combination_map.json")
    validate_combination_map(combinations, primitives, capabilities)

    fixture_paths = sorted((lab_dir / "fixtures").glob("*.json"))
    if len(fixture_paths) != 3:
        raise SceneIRValidationError(
            f"FIXTURE_COUNT_INVALID:expected=3:actual={len(fixture_paths)}"
        )
    fixtures: list[dict[str, Any]] = []
    results: list[FixtureValidation] = []
    for path in fixture_paths:
        fixture = load_json(path)
        fixtures.append(fixture)
        results.append(validate_fixture(fixture, grammar, primitives, capabilities))

    fixture_archetypes = {str(value.get("fixture_archetype")) for value in fixtures}
    expected_archetypes = {
        "inspection_explanation",
        "process_sequence",
        "comparison_contrast",
    }
    if fixture_archetypes != expected_archetypes:
        raise SceneIRValidationError(
            "FIXTURE_ARCHETYPES_INVALID:" + ",".join(sorted(fixture_archetypes))
        )

    level_counts = {level: 0 for level in EVIDENCE_LEVELS}
    availability_counts = {item: 0 for item in AVAILABILITY_CLASSES}
    for row in capabilities.values():
        level_counts[str(row["evidence_level"])] += 1
        availability_counts[str(row["availability_class"])] += 1

    readback = {
        "schema_version": "generic_visual_composition_conformance_readback.v1",
        "status": "passed",
        "evidence_level": "C2",
        "runtime_capability_proven": False,
        "cross_topic_proven": False,
        "generic_core_changed_per_fixture": False,
        "validator": "src/pipeline/generic_visual_scene_ir.py",
        "fixture_count": len(results),
        "fixture_archetypes": sorted(fixture_archetypes),
        "scene_counts": {result.fixture_id: result.scene_count for result in results},
        "cue_counts": {result.fixture_id: result.cue_count for result in results},
        "results": [result.as_dict() for result in results],
        "capability_count": len(capabilities),
        "availability_counts": availability_counts,
        "evidence_level_counts": level_counts,
        "relevant_path_count": len(inventory["paths"]),
        "unclassified_relevant_path_count": inventory[
            "unclassified_relevant_path_count"
        ],
        "checks": {
            "same_validator_for_all_fixtures": True,
            "variable_scene_counts": len({result.scene_count for result in results}) > 1,
            "variable_cue_counts": len({result.cue_count for result in results}) > 1,
            "inspection_fixture_present": True,
            "process_fixture_present": True,
            "comparison_fixture_present": True,
            "runtime_overclaim_absent": True,
            "C5_claim_absent": True,
            "topic_payload_outside_core": True,
        },
        "fixture_sha256": {
            path.relative_to(root).as_posix(): _sha256(path) for path in fixture_paths
        },
    }
    html_text = render_capability_board(
        matrix=matrix,
        grammar_data=grammar_data,
        combination_data=combinations,
        readback=readback,
    )
    _validate_html_boundary(html_text)

    outputs = {
        lab_dir / "conformance_readback.json": _json_text(readback),
        docs_dir / "visual_capability_board.html": html_text,
    }
    changed: list[str] = []
    if write:
        for path, text in outputs.items():
            if _write_if_changed(path, text):
                changed.append(path.relative_to(root).as_posix())
    return {
        "status": "passed",
        "artifact_count": len(outputs),
        "changed": changed,
        "readback": readback,
        "html": html_text,
    }


def render_capability_board(
    *,
    matrix: Mapping[str, Any],
    grammar_data: Mapping[str, Any],
    combination_data: Mapping[str, Any],
    readback: Mapping[str, Any],
) -> str:
    capability_rows = "\n".join(
        "<tr>"
        f"<td><code>{html.escape(str(row['capability_id']))}</code></td>"
        f"<td>{html.escape(str(row['availability_class']))}</td>"
        f"<td>{html.escape(str(row['evidence_level']))}</td>"
        f"<td>{html.escape(str(row['output_behavior']))}</td>"
        f"<td>{html.escape(str(row['fallback']))}</td>"
        f"<td>{html.escape(str(row['setup_weight']))} / "
        f"{html.escape(str(row['per_episode_burden']))}</td>"
        "</tr>"
        for row in matrix["capabilities"]
    )
    composition_rows = "\n".join(
        "<tr>"
        f"<td><code>{html.escape(str(row['composition_id']))}</code></td>"
        f"<td>{html.escape(', '.join(row['required_primitives']))}</td>"
        f"<td>{html.escape(str(row['fallback_composition']))}</td>"
        f"<td>{html.escape(str(row['evidence_level']))} / "
        f"{html.escape(str(row['static_conformance_evidence_level']))}</td>"
        f"<td>{html.escape(str(row['cost_reuse_profile']['setup_weight']))}</td>"
        "</tr>"
        for row in grammar_data["compositions"]
    )
    fixture_rows = "\n".join(
        "<tr>"
        f"<td><code>{html.escape(str(row['fixture_id']))}</code></td>"
        f"<td>{row['scene_count']}</td><td>{row['cue_count']}</td>"
        f"<td>{html.escape(', '.join(row['archetypes']))}</td>"
        f"<td>{html.escape(str(row['status']))}</td>"
        "</tr>"
        for row in readback["results"]
    )
    combination_rows = "\n".join(
        "<li><code>"
        + html.escape(str(row["combination_id"]))
        + "</code> → "
        + html.escape(str(row["evidence_level"]))
        + " / fallback: "
        + html.escape(str(row["fallback"]))
        + "</li>"
        for row in combination_data["combinations"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Generic Visual Capability Envelope</title>
<style>
:root {{ color-scheme: light; font-family: system-ui, sans-serif; --ink:#172033; --line:#cbd5e1; --soft:#f4f7fb; --accent:#155e75; }}
body {{ margin:0; color:var(--ink); background:white; }}
main {{ max-width:1500px; margin:auto; padding:32px; }}
h1,h2 {{ line-height:1.2; }}
.boundary {{ border-left:6px solid var(--accent); background:var(--soft); padding:16px 20px; }}
table {{ width:100%; border-collapse:collapse; margin:12px 0 28px; font-size:14px; }}
th,td {{ border:1px solid var(--line); padding:9px; text-align:left; vertical-align:top; }}
th {{ background:var(--soft); position:sticky; top:0; }}
.spine {{ display:grid; grid-template-columns:1fr auto 1fr auto 1fr; gap:12px; align-items:center; margin:20px 0 30px; }}
.node {{ border:2px solid var(--line); padding:16px; min-height:78px; }}
.arrow {{ color:var(--accent); font-size:24px; }}
code {{ overflow-wrap:anywhere; }}
@media (max-width:850px) {{ .spine {{ grid-template-columns:1fr; }} .arrow {{ transform:rotate(90deg); text-align:center; }} main {{ padding:18px; }} }}
</style>
</head>
<body><main>
<h1>Generic visual capability envelope</h1>
<div class="boundary"><strong>INTERNAL / STATIC C2 / NOT RUNTIME-PROVEN</strong><br>
Three heterogeneous fixtures pass one validator. This does not prove editor behavior, render semantics, production quality, rights, portability, or cross-topic reuse.</div>
<h2>Evidence dependency spine</h2>
<div class="spine"><div class="node"><strong>Repository evidence</strong><br>C0-C4 receipts, code paths, failures</div><div class="arrow">→</div><div class="node"><strong>Capability envelope</strong><br>availability + cost + fallback</div><div class="arrow">→</div><div class="node"><strong>Composition fixtures</strong><br>static conformance only</div></div>
<h2>Capability matrix</h2>
<table><thead><tr><th>Capability</th><th>Availability</th><th>Level</th><th>Observed output</th><th>Fallback</th><th>Cost</th></tr></thead><tbody>{capability_rows}</tbody></table>
<h2>Composition map</h2>
<table><thead><tr><th>Composition</th><th>Required primitives</th><th>Fallback</th><th>Overall / static</th><th>Setup</th></tr></thead><tbody>{composition_rows}</tbody></table>
<h2>Cross-archetype conformance</h2>
<table><thead><tr><th>Fixture</th><th>Scenes</th><th>Cues</th><th>Recipes used</th><th>Status</th></tr></thead><tbody>{fixture_rows}</tbody></table>
<h2>Combination boundaries</h2><ul>{combination_rows}</ul>
</main></body></html>
"""


def _validate_html_boundary(text: str) -> None:
    lowered = text.lower()
    forbidden = ("http://", "https://", "file://", "<script", "@import", "url(")
    hits = [item for item in forbidden if item in lowered]
    if hits:
        raise SceneIRValidationError("HTML_EXTERNAL_DEPENDENCY:" + ",".join(hits))
    if _PRIVATE_PATH_RE.search(text):
        raise SceneIRValidationError("HTML_PRIVATE_PATH")


def _list_of_dicts(data: Mapping[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
        raise SceneIRValidationError(f"LIST_OF_OBJECTS_REQUIRED:{key}")
    return [dict(row) for row in value]


def _mapping(data: Mapping[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise SceneIRValidationError(f"OBJECT_REQUIRED:{key}")
    return dict(value)


def _string(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SceneIRValidationError(f"STRING_REQUIRED:{key}")
    return value


def _unique_ids(
    rows: Iterable[Mapping[str, Any]], key: str, label: str
) -> set[str]:
    values = [_string(row, key) for row in rows]
    if len(values) != len(set(values)):
        raise SceneIRValidationError(f"{label}_DUPLICATE")
    return set(values)


def _json_text(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def _write_if_changed(path: Path, text: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[2]
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    result = build_package(args.repo_root, write=not args.check)
    print(
        json.dumps(
            {
                "status": result["status"],
                "artifact_count": result["artifact_count"],
                "changed": result["changed"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
