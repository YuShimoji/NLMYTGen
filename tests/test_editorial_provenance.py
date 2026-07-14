from __future__ import annotations

import hashlib
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path

from src.pipeline.editorial_provenance import (
    ATTRIBUTION_CLASSES,
    AUTHORITY_CLASSES,
    DEFAULT_PILOT_DIR,
    GENERATED_FILENAMES,
    LOCKED_ARTIFACT_HASHES,
    MAX_PROVENANCE_JSON_STRING_CHARS,
    MAX_PROVENANCE_MARKDOWN_LINE_CHARS,
    METADATA_SURFACE_BASELINE_HASHES,
    OPERATION_CLASSES,
    PRIOR_USER_SCRIPT_STATUSES,
    PROVENANCE_DIRNAME,
    TARGET_STATE_ID,
    _is_prior_user_script_candidate,
    build_editorial_provenance_package,
    render_editorial_provenance_artifacts,
    validate_editorial_provenance_package,
)


_PRIVATE_PATH_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/]|\\\\[^\\\s]+[\\/]|/home/|/users/)"
)
_UUID_RE = re.compile(
    r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
)
_BANNED_BODY_KEYS = {
    "raw_text",
    "source_body",
    "transcript_body",
    "full_text",
    "verbatim_excerpt",
    "source_quote_text",
}


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _all_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        result = set(value)
        for nested in value.values():
            result.update(_all_keys(nested))
        return result
    if isinstance(value, list):
        result: set[str] = set()
        for nested in value:
            result.update(_all_keys(nested))
        return result
    return set()


def _all_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [item for nested in value.values() for item in _all_strings(nested)]
    if isinstance(value, list):
        return [item for nested in value for item in _all_strings(nested)]
    return []


class _HrefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag != "a":
            return
        for name, value in attrs:
            if name == "href" and value is not None:
                self.hrefs.append(value)


def test_provenance_artifact_set_and_cue_lineage_are_complete() -> None:
    output = DEFAULT_PILOT_DIR / PROVENANCE_DIRNAME
    assert tuple(sorted(path.name for path in output.iterdir())) == tuple(
        sorted(GENERATED_FILENAMES)
    )
    matrix = _load(output / "cue_transformation_matrix.json")
    assert matrix["cue_coverage"] == "9/9"
    assert matrix["token_level_authorship_claimed"] is False
    assert [cue["cue_id"] for cue in matrix["cues"]] == [
        f"cue_{index:03d}" for index in range(1, 10)
    ]
    assert sum(len(cue["raw_transcript_candidates"]) for cue in matrix["cues"]) == 21
    assert {
        claim_id
        for cue in matrix["cues"]
        for claim_id in cue["adopted_claim_ids"]
    } == {
        "claim_010",
        "claim_065",
        "claim_067",
        "claim_090",
        "claim_096",
        "claim_097",
        "claim_099",
        "claim_114",
        "claim_116",
        "claim_118",
        "claim_130",
        "claim_132",
        "claim_155",
        "claim_157",
        "claim_161",
    }
    assert {
        source_id
        for cue in matrix["cues"]
        for source_id in cue["source_ids"]
    } == {"V02", "V06", "V07", "V13"}
    for cue in matrix["cues"]:
        assert len(cue["final_text_sha256"]) == 64
        assert cue["prior_draft_cue_ids"][0]["cue_id"] == cue["cue_id"]
        assert cue["unresolved_lineage"] == []
        assert cue["unattributed_substantive_change"] is False
        assert cue["final_text_coverage"]["character_range"] == [
            0,
            cue["final_text_character_count"],
        ]
        assert cue["final_text_coverage"]["unattributed_character_ranges"] == []
        assert cue["final_text_coverage"]["unmapped_substantive_unit_ids"] == []
        assert cue["final_text_coverage"]["coverage_status"] == (
            "complete_non_overlapping_surface_partition"
        )
        cursor = 0
        surface_unit_ids = set()
        for segment in cue["final_text_coverage"]["surface_segments"]:
            start, end = segment["character_range"]
            assert start == cursor
            assert end > start
            assert segment["character_count"] == end - start
            assert len(segment["fragment_sha256"]) == 64
            assert segment["source_text_embedded"] is False
            surface_unit_ids.add(segment["primary_substantive_unit_id"])
            cursor = end
        assert cursor == cue["final_text_character_count"]
        surface_unit_ids.update(
            row["unit_id"]
            for row in cue["final_text_coverage"]["structural_realizations"]
        )
        surface_unit_ids.add(
            cue["final_text_coverage"]["speaker_assignment"][
                "substantive_unit_id"
            ]
        )
        assert set(
            cue["final_text_coverage"]["covered_by_substantive_unit_ids"]
        ) == surface_unit_ids == {
            unit["unit_id"] for unit in cue["substantive_units"]
        }
        assert cue["approval_state"]["future_silent_edits_authorized"] is False


def test_every_substantive_unit_and_stage_has_valid_attribution_authority() -> None:
    output = DEFAULT_PILOT_DIR / PROVENANCE_DIRNAME
    matrix = _load(output / "cue_transformation_matrix.json")
    stages = _load(output / "stage_decision_ledger.json")
    contribution = _load(output / "authorial_contribution_readback.json")
    units = [
        unit for cue in matrix["cues"] for unit in cue["substantive_units"]
    ]
    assert len(units) == 38
    assert contribution["substantive_unit_count"] == 38
    assert contribution["attributed_substantive_unit_count"] == 38
    assert contribution["unresolved_substantive_unit_count"] == 0
    assert contribution["unattributed_substantive_change_count"] == 0
    for unit in units:
        assert unit["attribution_class"] in ATTRIBUTION_CLASSES
        assert set(unit["operations"]) <= set(OPERATION_CLASSES)
        assert set(unit["authority_classes"]) <= set(AUTHORITY_CLASSES)
        assert unit["source_quote"] is False
    assert stages["stage_order"] == [f"D{index:02d}" for index in range(11)]
    for stage in stages["stages"]:
        assert set(stage["operations"]) <= set(OPERATION_CLASSES)
        assert set(stage["authority_classes"]) <= set(AUTHORITY_CLASSES)
        assert stage["approval_status"]
        assert isinstance(stage["may_alter_canonical_content"], bool)
        assert stage["input_identity"]
        assert stage["output_identity"]
    approval = next(
        stage for stage in stages["stages"] if stage["stage_id"] == "D08"
    )["output_identity"][0]
    assert approval["artifact_kind"] == "bounded_user_approval_decision"
    assert len(approval["decision_sha256"]) == 64
    assert approval["future_silent_edits_authorized"] is False
    assert approval["independent_contemporaneous_receipt_available"] is False


def test_quantified_transformations_do_not_claim_authorship_percentage() -> None:
    contribution = _load(
        DEFAULT_PILOT_DIR
        / PROVENANCE_DIRNAME
        / "authorial_contribution_readback.json"
    )
    magnitude = contribution["transformation_magnitude"]
    assert magnitude == {
        "pre_editorial_draft_cue_count": 9,
        "exact_byte_equal_cue_count": 1,
        "normalized_before_character_count": 424,
        "normalized_after_character_count": 425,
        "ordered_matching_character_count": 279,
        "before_token_count": 408,
        "after_token_count": 409,
        "ordered_matching_token_count": 263,
        "single_source_paraphrased_factual_unit_count": 19,
        "multi_source_synthesis_unit_count": 1,
        "new_bridge_unit_count": 9,
        "character_voice_unit_count": 9,
        "omitted_verified_claim_count": 4,
        "speaker_reassignment_count_pre_editorial_to_current": 0,
        "scene_movement_count_pre_editorial_to_current": 0,
        "merge_annotated_cue_count": 4,
        "split_annotated_cue_count": 1,
        "style_or_rhetoric_units_excluded_count": 52,
        "supervisor_requested_revision_count": None,
        "supervisor_requested_revision_observation": (
            "not_observed_in_available_repo_evidence"
        ),
        "user_requested_revision_count": None,
        "user_requested_revision_observation": (
            "not_observed_in_available_repo_evidence"
        ),
        "unresolved_external_origin_unit_count": 0,
    }
    assert contribution["authorship_percentage_claimed"] is False
    assert "not authorship percentages" in contribution["limitations"][0]


def test_prior_user_script_audit_is_bounded_and_never_infers_non_use() -> None:
    audit = _load(
        DEFAULT_PILOT_DIR
        / PROVENANCE_DIRNAME
        / "prior_user_script_usage_audit.json"
    )
    assert set(audit["allowed_final_statuses"]) == set(
        PRIOR_USER_SCRIPT_STATUSES
    )
    assert audit["candidate_files"] == []
    assert audit["candidate_hashes"] == []
    assert audit["candidate_count"] == 0
    assert len(audit["candidate_set_sha256"]) == 64
    assert len(audit["inventory_policy"]["policy_sha256"]) == 64
    assert len(audit["search_surfaces"]) == 5
    for surface in audit["search_surfaces"]:
        assert surface["method"].startswith("executed_")
        assert len(surface["candidate_path_inventory_sha256"]) == 64
    assert audit["known_upstream_user_input"]["artifact_kind"] == (
        "audio_overview_transcript"
    )
    assert audit["known_upstream_user_input"]["finished_script"] is False
    assert audit["known_upstream_user_input"]["optional_local_identity_gate"] == (
        "required_when_file_present"
    )
    assert audit["known_upstream_user_input"]["optional_raw_line_map_gate"] == (
        "required_when_file_present"
    )
    assert audit["final_status"] == (
        "not_proven_from_available_repo_evidence"
    )
    assert audit["false_non_use_inference_made"] is False
    serialized = json.dumps(audit, ensure_ascii=False)
    assert '"final_status": "proven_not_used"' not in serialized
    assert '"final_status": "not_used"' not in serialized
    assert _is_prior_user_script_candidate(
        "production_pilots/pkg/input/user_final_script.txt"
    )
    assert not _is_prior_user_script_candidate(
        "production_pilots/pkg/human_script_approval_receipt.json"
    )
    assert not _is_prior_user_script_candidate(
        "production_pilots/pkg/canonical_script.json"
    )


def test_content_lock_covers_current_script_yymm4_and_visual_identities() -> None:
    output = DEFAULT_PILOT_DIR / PROVENANCE_DIRNAME
    lock = _load(output / "content_lock_receipt.json")
    locked_rows = [
        row
        for rows in lock["locked_artifact_groups"].values()
        for row in rows
    ]
    locked = {
        row["repo_relative_path"].split(
            "new_banknote_security_notebooklm_001/", 1
        )[1]: row["sha256"]
        for row in locked_rows
    }
    assert locked == LOCKED_ARTIFACT_HASHES
    for relative, digest in locked.items():
        assert hashlib.sha256(
            (DEFAULT_PILOT_DIR / relative).read_bytes()
        ).hexdigest() == digest
    assert len(lock["cue_identity"]) == 9
    assert lock["semantic_contract"]["selected_visual_route"] is None
    assert lock["future_substantive_change_rule"].startswith(
        "invalidate_this_lock"
    )
    assert len(lock["metadata_only_deltas"]) == len(
        METADATA_SURFACE_BASELINE_HASHES
    )
    assert lock["metadata_only_deltas_all_changed_from_recorded_baseline"] is True
    for row in lock["metadata_only_deltas"]:
        assert row["before_sha256"] != row["after_sha256"]
        assert row["canonical_content_effect"] == "none"
    local_yymm4 = lock["local_yymm4_evidence_reverification"]
    assert local_yymm4["status"] == (
        "not_reperformed_local_project_and_results_absent"
    )
    assert local_yymm4["expected_identity_count"] == 3
    assert local_yymm4["local_present_count"] == 0
    assert all(row["local_file_present"] is False for row in local_yymm4["evidence"])


def test_render_and_second_build_are_byte_deterministic(tmp_path: Path) -> None:
    first = render_editorial_provenance_artifacts(DEFAULT_PILOT_DIR)
    second = render_editorial_provenance_artifacts(DEFAULT_PILOT_DIR)
    assert first == second
    validation = validate_editorial_provenance_package(DEFAULT_PILOT_DIR)
    assert validation["status"] == "passed"
    assert all(validation["checks"].values())

    pilot = tmp_path / "pilot"
    shutil.copytree(
        DEFAULT_PILOT_DIR,
        pilot,
        ignore=shutil.ignore_patterns(
            PROVENANCE_DIRNAME,
            "local_outputs",
            "source_cache",
            "source_extracts",
            "source_probe",
        ),
    )
    first_build = build_editorial_provenance_package(pilot)
    first_bytes = {
        name: (pilot / PROVENANCE_DIRNAME / name).read_bytes()
        for name in GENERATED_FILENAMES
    }
    second_build = build_editorial_provenance_package(pilot)
    second_bytes = {
        name: (pilot / PROVENANCE_DIRNAME / name).read_bytes()
        for name in GENERATED_FILENAMES
    }
    assert first_build["status"] == second_build["status"] == "passed"
    assert second_build["changed"] == []
    assert first_bytes == second_bytes


def test_review_surfaces_link_provenance_without_route_or_script_mutation() -> None:
    surfaces = {
        "README_CANONICAL_SCRIPT_REVIEW.md": (
            DEFAULT_PILOT_DIR / "README_CANONICAL_SCRIPT_REVIEW.md"
        ),
        "canonical_script_editorial_revision.md": (
            DEFAULT_PILOT_DIR / "canonical_script_editorial_revision.md"
        ),
        "README_VISUAL_SCENE_DECISION.md": (
            DEFAULT_PILOT_DIR
            / "visual_scene_decision"
            / "README_VISUAL_SCENE_DECISION.md"
        ),
        "visual_direction_board.html": (
            DEFAULT_PILOT_DIR
            / "visual_scene_decision"
            / "visual_direction_board.html"
        ),
    }
    for name, path in surfaces.items():
        text = path.read_text(encoding="utf-8")
        assert "editorial_provenance/README_EDITORIAL_PROVENANCE.md" in text, name
        assert "source" in text.lower(), name
        assert "editorial" in text.lower(), name
        assert "user" in text.lower() or "ユーザー" in text, name
        assert "未証明" in text or "証明されていません" in text, name

    board_path = surfaces["visual_direction_board.html"]
    parser = _HrefParser()
    parser.feed(board_path.read_text(encoding="utf-8"))
    for href in parser.hrefs:
        assert not href.startswith(("http://", "https://", "file://", "/"))
        assert (board_path.parent / href).resolve().is_file()

    for relative, digest in LOCKED_ARTIFACT_HASHES.items():
        assert hashlib.sha256(
            (DEFAULT_PILOT_DIR / relative).read_bytes()
        ).hexdigest() == digest


def test_provenance_artifacts_have_no_private_body_or_long_excerpt_leakage() -> None:
    output = DEFAULT_PILOT_DIR / PROVENANCE_DIRNAME
    text = "\n".join(
        (output / name).read_text(encoding="utf-8")
        for name in GENERATED_FILENAMES
    )
    assert _PRIVATE_PATH_RE.search(text) is None
    assert _UUID_RE.search(text) is None
    assert "notebooklm.google.com" not in text.lower()
    payloads = [
        _load(output / name)
        for name in GENERATED_FILENAMES
        if name.endswith(".json")
    ]
    assert not (_BANNED_BODY_KEYS & set().union(*map(_all_keys, payloads)))
    for payload in payloads:
        for key in _all_keys(payload):
            assert not key.endswith("_excerpt")
        for value in _all_strings(payload):
            assert "\n" not in value
            assert len(value) <= MAX_PROVENANCE_JSON_STRING_CHARS
    for name in GENERATED_FILENAMES:
        if not name.endswith(".md"):
            continue
        for line in (output / name).read_text(encoding="utf-8").splitlines():
            assert len(line) <= MAX_PROVENANCE_MARKDOWN_LINE_CHARS


def test_validation_readback_matches_target_state_and_acceptance() -> None:
    readback = _load(
        DEFAULT_PILOT_DIR
        / PROVENANCE_DIRNAME
        / "provenance_validation_readback.json"
    )
    assert readback["status"] == "passed"
    assert readback["target_state_id"] == TARGET_STATE_ID
    assert all(readback["checks"].values())
    assert readback["failed_checks"] == []
    assert readback["canonical_content_changed"] is False
    assert readback["notebooklm_accessed"] is False
    assert readback["web_fetch_used"] is False
    assert readback["yymm4_used"] is False
