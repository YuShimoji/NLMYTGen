from __future__ import annotations

import copy
import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

from src.pipeline.generic_visual_scene_ir import (
    AVAILABILITY_CLASSES,
    EVIDENCE_LEVELS,
    PATH_CLASSES,
    SceneIRValidationError,
    build_package,
    load_json,
    validate_capability_matrix,
    validate_composition_grammar,
    validate_fixture,
    validate_path_inventory,
    validate_primitive_catalog,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "visual_system"
LAB = ROOT / "samples" / "visual_composition_lab"
CORE = ROOT / "src" / "pipeline" / "generic_visual_scene_ir.py"


def _package_inputs() -> tuple[dict, dict, dict]:
    matrix = load_json(DOCS / "generic_visual_capability_matrix.json")
    capabilities = validate_capability_matrix(matrix)
    primitive_data = load_json(DOCS / "visual_primitive_catalog.json")
    primitives = validate_primitive_catalog(primitive_data, capabilities)
    grammar_data = load_json(DOCS / "scene_composition_grammar.json")
    grammar = validate_composition_grammar(grammar_data, primitives, capabilities)
    return capabilities, primitives, grammar


def test_relevant_path_inventory_has_full_classification_and_existing_paths() -> None:
    inventory = load_json(DOCS / "relevant_path_inventory.json")
    validate_path_inventory(inventory, ROOT)

    assert inventory["unclassified_relevant_path_count"] == 0
    assert len(inventory["paths"]) == 78
    assert {row["classification"] for row in inventory["paths"]} <= set(PATH_CLASSES)
    assert len({row["path_id"] for row in inventory["paths"]}) == 78
    assert len({row["path"] for row in inventory["paths"]}) == 78


def test_each_capability_has_exactly_one_valid_availability_and_complete_fields() -> None:
    matrix = load_json(DOCS / "generic_visual_capability_matrix.json")
    capabilities = validate_capability_matrix(matrix)

    assert len(capabilities) == 38
    assert set(row["availability_class"] for row in capabilities.values()) <= set(
        AVAILABILITY_CLASSES
    )
    assert all(isinstance(row["availability_class"], str) for row in capabilities.values())
    assert all(row["fallback"] for row in capabilities.values())
    assert all(row["prohibited_overclaim"] for row in capabilities.values())


def test_evidence_level_rules_reject_runtime_render_and_cross_topic_overclaims() -> None:
    matrix = load_json(DOCS / "generic_visual_capability_matrix.json")
    capabilities = validate_capability_matrix(matrix)

    for row in capabilities.values():
        level_index = EVIDENCE_LEVELS.index(row["evidence_level"])
        if row["availability_class"] == "proven":
            assert level_index >= EVIDENCE_LEVELS.index("C3")
        if "render_proven" in row.get("proof_tags", []):
            assert level_index >= EVIDENCE_LEVELS.index("C4")
        if "cross_topic_proven" in row.get("proof_tags", []):
            assert row["evidence_level"] == "C5"

    bad = copy.deepcopy(matrix)
    bad["capabilities"][0]["evidence_level"] = "C2"
    with pytest.raises(SceneIRValidationError, match="RUNTIME_OVERCLAIM"):
        validate_capability_matrix(bad)

    bad = copy.deepcopy(matrix)
    bad["capabilities"][0]["proof_tags"] = ["render_proven"]
    with pytest.raises(SceneIRValidationError, match="RENDER_OVERCLAIM"):
        validate_capability_matrix(bad)

    bad = copy.deepcopy(matrix)
    bad["capabilities"][0]["proof_tags"] = ["cross_topic_proven"]
    with pytest.raises(SceneIRValidationError, match="CROSS_TOPIC_OVERCLAIM"):
        validate_capability_matrix(bad)


def test_evidence_ledger_covers_every_capability_and_has_no_C5_record() -> None:
    matrix = load_json(DOCS / "generic_visual_capability_matrix.json")
    capability_ids = {row["capability_id"] for row in matrix["capabilities"]}
    ledger = load_json(DOCS / "capability_evidence_ledger.json")
    covered = {
        capability_id
        for record in ledger["records"]
        for capability_id in record["capability_ids"]
    }

    assert covered == capability_ids
    assert ledger["coverage"]["capability_ids_missing_from_ledger"] == []
    assert ledger["coverage"]["C5_evidence_record_count"] == 0

    inventory = load_json(DOCS / "relevant_path_inventory.json")
    inventory_paths = {row["path"] for row in inventory["paths"]}
    referenced_paths = {
        path
        for row in matrix["capabilities"]
        for path in row["evidence_locations"]
    } | {path for record in ledger["records"] for path in record["locations"]}
    assert referenced_paths <= inventory_paths


def test_generic_core_has_no_topic_literals_or_fixed_pilot_assumptions() -> None:
    source = CORE.read_text(encoding="utf-8")
    lowered = source.lower()
    banned = (
        "new_banknote",
        "banknote",
        "currency",
        "hologram",
        "nipponginko",
        "紙幣",
        "お札",
        "cue_009",
        "73.583333",
        "4415",
        "3/6",
    )
    assert [token for token in banned if token in lowered] == []
    assert re.search(r"cue_count\s*[=!]=\s*9", source) is None
    assert re.search(r"scene_count\s*[=!]=\s*3", source) is None
    assert "VoiceItem_count_9" not in source
    assert "adapt_route" not in source.lower()


def test_all_three_fixtures_use_same_validator_with_variable_counts() -> None:
    capabilities, primitives, grammar = _package_inputs()
    fixture_paths = sorted((LAB / "fixtures").glob("*.json"))
    results = [
        validate_fixture(load_json(path), grammar, primitives, capabilities)
        for path in fixture_paths
    ]

    assert len(results) == 3
    assert {result.scene_count for result in results} == {2, 3, 4}
    assert {result.cue_count for result in results} == {4, 5, 9}
    assert all(result.status == "static_conformance_pass" for result in results)
    assert all(result.as_dict()["runtime_ready"] is False for result in results)
    assert all(result.as_dict()["cross_topic_proven"] is False for result in results)


def test_unrelated_fixtures_pass_without_core_change_or_special_case() -> None:
    capabilities, primitives, grammar = _package_inputs()
    core_before = CORE.read_bytes()
    for name in ("process_generic.json", "comparison_generic.json"):
        result = validate_fixture(
            load_json(LAB / "fixtures" / name), grammar, primitives, capabilities
        )
        assert result.status == "static_conformance_pass"
    assert CORE.read_bytes() == core_before
    source = CORE.read_text(encoding="utf-8")
    assert "process_generic" not in source
    assert "comparison_generic" not in source
    assert "inspection_route_A" not in source


def test_route_A_is_data_only_and_keeps_runtime_gaps_explicit() -> None:
    capabilities, primitives, grammar = _package_inputs()
    fixture = load_json(LAB / "fixtures" / "inspection_route_A.json")
    result = validate_fixture(fixture, grammar, primitives, capabilities)

    assert fixture["evidence_boundary"]["implementation_authorized"] is False
    assert fixture["evidence_boundary"]["render_authorized"] is False
    assert fixture["evidence_boundary"]["fixture_selection_context"] == (
        "selected_for_conformance_fixture_only_by_current_supervisor_contract"
    )
    assert result.scene_count == 3
    assert result.cue_count == 9
    assert len(result.capability_gaps) == 20
    assert all(gap["fallback"] for gap in result.capability_gaps)
    assert sum(
        gap["capability_id"] == "linked_subtitle_typography_layout"
        for gap in result.capability_gaps
    ) == 9
    assert all(cue["fallback"]["composition_id"] for cue in fixture["cues"])


def test_fixture_validator_fails_on_duplicate_orphan_and_missing_required_primitive() -> None:
    capabilities, primitives, grammar = _package_inputs()
    fixture = load_json(LAB / "fixtures" / "process_generic.json")

    bad = copy.deepcopy(fixture)
    bad["cues"][1]["cue_id"] = bad["cues"][0]["cue_id"]
    with pytest.raises(SceneIRValidationError, match="CUE_ID_DUPLICATE"):
        validate_fixture(bad, grammar, primitives, capabilities)

    bad = copy.deepcopy(fixture)
    bad["scenes"][0]["cue_ids"] = ["missing_cue"]
    with pytest.raises(SceneIRValidationError, match="SCENE_CUE_UNKNOWN"):
        validate_fixture(bad, grammar, primitives, capabilities)

    bad = copy.deepcopy(fixture)
    bad["cues"][1]["primitive_refs"] = [
        row
        for row in bad["cues"][1]["primitive_refs"]
        if row["primitive_id"] != "connector_line"
    ]
    with pytest.raises(SceneIRValidationError, match="CUE_REQUIRED_PRIMITIVE_MISSING"):
        validate_fixture(bad, grammar, primitives, capabilities)


def test_combinations_reference_valid_primitives_and_have_fallback_cost() -> None:
    result = build_package(ROOT, write=False)
    combinations = load_json(DOCS / "capability_combination_map.json")
    primitives = load_json(DOCS / "visual_primitive_catalog.json")
    primitive_ids = {row["primitive_id"] for row in primitives["primitives"]}

    assert result["status"] == "passed"
    for row in combinations["combinations"]:
        assert set(row["primitive_ids"]) <= primitive_ids
        assert row["fallback"]
        assert row["cost_reuse_profile"]["setup_weight"] in {"W1", "W2", "W3", "W4", "W5"}

    capabilities, primitive_index, grammar = _package_inputs()
    for row in grammar.values():
        required_levels = (
            capabilities[primitive_index[primitive_id]["capability_id"]][
                "evidence_level"
            ]
            for primitive_id in row["required_primitives"]
        )
        floor = min(required_levels, key=EVIDENCE_LEVELS.index)
        assert row["evidence_level"] == floor
        assert row["static_conformance_evidence_level"] == "C2"
    assert all(
        primitive["minimum_evidence_level"] in EVIDENCE_LEVELS
        for primitive in primitive_index.values()
    )


def test_delivery_surfaces_cover_can_conditional_cannot_unknown_and_cost() -> None:
    primary = (DOCS / "README_GENERIC_VISUAL_CAPABILITIES.md").read_text(
        encoding="utf-8"
    )
    can_cannot = (DOCS / "CAN_DO_CANNOT_DO.md").read_text(encoding="utf-8")
    acceptance = (DOCS / "DELIVERY_ACCEPTANCE.md").read_text(encoding="utf-8")

    for token in (
        "Can be used now",
        "Only statically materialized",
        "Requires YMM4 observation",
        "Requires render evidence",
        "Unsupported now",
        "Unknown",
        "minimum generic stack",
        "not worth building",
        "C5",
    ):
        assert token.lower() in primary.lower()
    for token in ("Can use now", "Conditional", "Cannot", "Unknown"):
        assert token.lower() in can_cannot.lower()
    assert "[x]" in acceptance
    assert "H1 decision gate" in acceptance


class _HTMLAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        for key, value in attrs:
            if key in {"src", "href"} and value:
                self.refs.append(value)


def test_HTML_is_self_contained_table_primary_and_private_path_free() -> None:
    html_text = (DOCS / "visual_capability_board.html").read_text(encoding="utf-8")
    parser = _HTMLAudit()
    parser.feed(html_text)

    assert "table" in parser.tags
    assert parser.tags.count("table") >= 3
    assert "script" not in parser.tags
    assert parser.refs == []
    assert re.search(r"https?://|file://|[A-Za-z]:\\|/(?:Users|home)/", html_text) is None
    assert "STATIC C2" in html_text
    assert "cross-topic reuse" in html_text


def test_deterministic_second_pass_matches_tracked_outputs() -> None:
    first = build_package(ROOT, write=False)
    second = build_package(ROOT, write=False)

    assert first["readback"] == second["readback"]
    assert first["html"] == second["html"]
    assert first["html"] == (DOCS / "visual_capability_board.html").read_text(
        encoding="utf-8"
    )
    assert first["readback"] == json.loads(
        (LAB / "conformance_readback.json").read_text(encoding="utf-8")
    )


def test_no_local_project_or_media_materialization_in_lab() -> None:
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".png", ".jpg"}
    files = [path for path in LAB.rglob("*") if path.is_file()]
    assert all(path.suffix.lower() not in forbidden_suffixes for path in files)
    readback = load_json(LAB / "conformance_readback.json")
    assert readback["runtime_capability_proven"] is False
    assert readback["cross_topic_proven"] is False
