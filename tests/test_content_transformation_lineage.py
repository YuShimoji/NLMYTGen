from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import pytest

from tests.regression_workspace import copy_tracked_tree, repo_relative_path

from src.pipeline.content_transformation_lineage import (
    APPROVAL_RECEIPT_ID,
    APPROVED_COMMIT,
    APPROVED_HASHES,
    DEFAULT_PILOT_DIR,
    EXPECTED_OUTCOME_COUNTS,
    LINEAGE_FILENAMES,
    build_content_lineage_package,
    render_content_lineage_artifacts,
    validate_content_lineage_package,
)
from src.pipeline.new_banknote_yymm4_import_operator_batch import (
    build_new_banknote_yymm4_operator_batch,
    preflight_new_banknote_yymm4_operator_batch,
)
from src.pipeline.ymm4_character_alias_profile import read_headerless_yymm4_csv


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _dump(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _copy_pilot(tmp_path: Path, name: str) -> Path:
    target = tmp_path / name
    copy_tracked_tree(
        DEFAULT_PILOT_DIR,
        target,
        repo_root=REPO_ROOT,
    )
    return target


def test_approved_baseline_hashes_and_contract_are_exact() -> None:
    assert tuple(APPROVED_HASHES) == (
        "README_CANONICAL_SCRIPT_REVIEW.md",
        "canonical_script.json",
        "canonical_script.txt",
        "canonical_script_review.md",
        "cue_source_traceability.json",
        "canonical_yymm4.csv",
        "derived_yymm4_import.csv",
        "source_to_script_manifest.json",
    )
    for name, expected in APPROVED_HASHES.items():
        assert hashlib.sha256((DEFAULT_PILOT_DIR / name).read_bytes()).hexdigest() == expected

    receipt = _load(DEFAULT_PILOT_DIR / "human_script_approval_receipt.json")
    assert receipt["receipt_id"] == APPROVAL_RECEIPT_ID
    assert receipt["approval_class"] == "explicit_user_option_a"
    assert receipt["approved_commit"] == APPROVED_COMMIT
    assert receipt["approved_file_hashes"] == APPROVED_HASHES
    assert receipt["status"] == "valid"
    assert receipt["permissions"]["later_user_manual_import_observation"] is True
    assert receipt["permissions"]["wording_or_claim_revision"] is False
    assert receipt["successor_receipt_policy"]["overwrite_current_receipt"] is False


def test_stage_ledger_and_numerical_funnel_are_complete() -> None:
    ledger = _load(DEFAULT_PILOT_DIR / "content_transformation_ledger.json")
    assert ledger["stage_order"] == [f"T{index:02d}" for index in range(8)]
    assert [stage["stage_id"] for stage in ledger["stages"]] == ledger["stage_order"]
    assert {stage["actor_class"] for stage in ledger["stages"]} <= {
        "user",
        "NotebookLM",
        "Worker_mechanical",
        "Worker_source_verification",
        "Worker_editorial",
        "human_approval",
    }
    for stage in ledger["stages"]:
        for key in (
            "input_artifacts_and_hashes",
            "output_artifacts_and_hashes",
            "change_class",
            "semantic_change",
            "evidence_change",
            "approval_impact",
            "human_approval_required_for_equivalent_future_change",
            "approval_remains_valid_for_current_hashes",
            "before_after_summary",
            "rejection_or_omission_retention",
            "current_approval_status",
        ):
            assert key in stage, (stage["stage_id"], key)

    by_id = {stage["stage_id"]: stage for stage in ledger["stages"]}
    assert by_id["T00"]["content_count_after"]["raw_logical_line_count"] == 326
    assert by_id["T01"]["content_count_after"]["claim_candidate_count"] == 182
    assert by_id["T03"]["content_count_after"]["verified_primary_count"] == 19
    assert by_id["T03"]["content_count_after"]["outcome_counts"] == EXPECTED_OUTCOME_COUNTS
    assert by_id["T04"]["content_count_after"] == {
        "cue_count": 9,
        "unique_adopted_claim_count": 17,
        "factual_units": 22,
        "claim_edges": 23,
    }
    assert by_id["T05"]["content_count_after"] == {
        "cue_count": 9,
        "unique_adopted_claim_count": 15,
        "factual_units": 20,
        "claim_edges": 21,
    }
    assert by_id["T05"]["change_class"] == "S_SEMANTIC"
    assert "E_EDITORIAL_EVIDENCE_PRESERVING" in by_id["T05"]["secondary_change_classes"]
    assert by_id["T06"]["status"] == "valid"
    assert by_id["T07"]["change_class"] == "M_MECHANICAL"
    assert by_id["T07"]["status"] == "prepared_not_observed"


def test_cue_lineage_covers_claims_units_edges_sources_and_editorial_origin() -> None:
    matrix = _load(DEFAULT_PILOT_DIR / "cue_lineage_matrix.json")
    assert matrix["cue_coverage"] == "9/9"
    assert matrix["unique_adopted_claim_count"] == 15
    assert matrix["factual_support_unit_count"] == 20
    assert matrix["claim_edge_count"] == 21
    assert matrix["token_level_attribution_claimed"] is False
    assert len(matrix["cues"]) == 9

    adopted: set[str] = set()
    source_ids: set[str] = set()
    factual_units = 0
    evidence_edges = 0
    for cue in matrix["cues"]:
        assert cue["approval_receipt_id"] == APPROVAL_RECEIPT_ID
        assert cue["current_approval_validity"] is True
        assert len(cue["approved_text_sha256"]) == 64
        for raw in cue["originating_raw_claim_ids"]:
            assert raw["claim_id"].startswith("claim_")
            assert raw["raw_line_ordinal"] > 0
            assert len(raw["raw_line_fingerprint"]) == 64
            assert raw["raw_text_embedded"] is False
        adopted.update(claim["claim_id"] for claim in cue["adopted_verified_claims"])
        factual_units += len(cue["factual_paraphrase_units"])
        for unit in cue["factual_paraphrase_units"]:
            assert unit["classification"] == "verified_factual_paraphrase"
            assert unit["source_quote"] is False
            evidence_edges += len(unit["supporting_evidence"])
            source_ids.update(edge["source_id"] for edge in unit["supporting_evidence"])
        for key in ("editorial_connective_units", "character_voice_phrasing_units"):
            for unit in cue[key]:
                assert unit["source_quote"] is False
                assert unit["evidence_grade"].startswith("inferred_")

    assert len(adopted) == 15
    assert factual_units == 20
    assert evidence_edges == 21
    assert source_ids == {"V02", "V06", "V07", "V13"}
    cue_005 = next(cue for cue in matrix["cues"] if cue["cue_id"] == "cue_005")
    assert cue_005["last_content_changing_stage"] == "T04"
    cue_008 = next(cue for cue in matrix["cues"] if cue["cue_id"] == "cue_008")
    assert [row["claim_id"] for row in cue_008["omitted_verified_claims_retained_nearby"]] == ["claim_158"]


def test_mechanical_speaker_projection_preserves_text_and_approval(
    tmp_path: Path,
) -> None:
    pilot = _copy_pilot(tmp_path, "mechanical-speaker-projection")
    canonical = read_headerless_yymm4_csv(pilot / "canonical_yymm4.csv")["rows"]
    derived = read_headerless_yymm4_csv(pilot / "derived_yymm4_import.csv")["rows"]
    assert [row["text"] for row in canonical] == [row["text"] for row in derived]
    assert dict(Counter(row["speaker"] for row in canonical)) == {"れいむ": 3, "まりさ": 6}
    assert dict(Counter(row["speaker"] for row in derived)) == {"ゆっくり霊夢": 3, "ゆっくり魔理沙": 6}
    assert validate_content_lineage_package(pilot)["approval_valid"] is True


def test_lineage_build_is_byte_deterministic(tmp_path: Path) -> None:
    pilot = _copy_pilot(tmp_path, "deterministic")
    first = render_content_lineage_artifacts(pilot)
    result = build_content_lineage_package(pilot)
    assert result["approved_content_modified"] is False
    first_written = {name: (pilot / name).read_bytes() for name in LINEAGE_FILENAMES}
    build_content_lineage_package(pilot)
    second_written = {name: (pilot / name).read_bytes() for name in LINEAGE_FILENAMES}
    assert first_written == second_written == first
    assert validate_content_lineage_package(pilot)["status"] == "passed"


@pytest.mark.parametrize("drift_kind", ["text", "speaker", "scene", "order", "claim", "csv"])
def test_approval_invalidates_on_every_approved_content_drift(tmp_path: Path, drift_kind: str) -> None:
    pilot = _copy_pilot(tmp_path, drift_kind)
    if drift_kind == "csv":
        path = pilot / "derived_yymm4_import.csv"
        path.write_bytes(path.read_bytes() + b"\n")
    else:
        path = pilot / "canonical_script.json"
        script = _load(path)
        if drift_kind == "text":
            script["cues"][0]["text"] += "!"
        elif drift_kind == "speaker":
            script["cues"][0]["speaker"] = "まりさ"
        elif drift_kind == "scene":
            script["cues"][0]["scene_id"] = "S2"
        elif drift_kind == "order":
            script["cues"][0], script["cues"][1] = script["cues"][1], script["cues"][0]
        elif drift_kind == "claim":
            script["cues"][0]["adopted_claim_ids"] = []
        _dump(path, script)
    validation = validate_content_lineage_package(pilot)
    assert validation["status"] == "failed"
    assert validation["approval_valid"] is False


def test_receipt_and_lineage_drift_stop_operator_preflight(tmp_path: Path) -> None:
    for name in ("human_script_approval_receipt.json", "content_transformation_ledger.json"):
        pilot = _copy_pilot(tmp_path, name.replace(".", "_"))
        build_content_lineage_package(pilot)
        build_new_banknote_yymm4_operator_batch(pilot)
        payload = _load(pilot / name)
        payload["status"] = "tampered"
        _dump(pilot / name, payload)
        preflight = preflight_new_banknote_yymm4_operator_batch(pilot)
        assert preflight["status"] == "failed"
        assert preflight["yymm4_launch_attempted"] is False


def test_approved_file_drift_stops_operator_preflight_without_launch(tmp_path: Path) -> None:
    pilot = _copy_pilot(tmp_path, "operator-approved-drift")
    build_content_lineage_package(pilot)
    build_new_banknote_yymm4_operator_batch(pilot)
    path = pilot / "derived_yymm4_import.csv"
    path.write_bytes(path.read_bytes() + b"\n")
    preflight = preflight_new_banknote_yymm4_operator_batch(pilot)
    assert preflight["status"] == "failed"
    assert preflight["yymm4_launch_attempted"] is False
    assert preflight["computer_use_invoked"] is False


def test_lineage_surfaces_preserve_privacy_and_ignored_evidence_boundaries() -> None:
    combined = "\n".join(
        (DEFAULT_PILOT_DIR / name).read_text(encoding="utf-8")
        for name in LINEAGE_FILENAMES
    )
    assert "notebooklm.google.com" not in combined.lower()
    assert '"raw_text"' not in combined
    assert '"source_body"' not in combined
    assert '"transcript_body"' not in combined
    assert "token-by-token origin" in combined or "token-level" in combined

    for directory in ("local_outputs", "source_cache", "source_extracts", "source_probe"):
        candidate = DEFAULT_PILOT_DIR / directory / "lineage-privacy-probe.bin"
        relative_candidate = repo_relative_path(REPO_ROOT, candidate)
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", "--", relative_candidate],
            cwd=REPO_ROOT,
            check=False,
        )
        assert ignored.returncode == 0, directory
        relative_directory = repo_relative_path(
            REPO_ROOT,
            DEFAULT_PILOT_DIR / directory,
        )
        tracked = subprocess.run(
            ["git", "ls-files", "--", relative_directory],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        assert not tracked.stdout.strip()


def test_readback_reports_all_acceptance_checks_passed() -> None:
    readback = _load(DEFAULT_PILOT_DIR / "content_lineage_readback.json")
    assert readback["status"] == "passed"
    assert all(readback["checks"].values())
    assert readback["approval_valid"] is True
    assert readback["yymm4_launched"] is False
    assert readback["notebooklm_accessed"] is False
    assert readback["web_fetch_used"] is False
