import csv
import json
import re
import subprocess
from pathlib import Path

from src.pipeline.newsroom_v0_1_dense_script_semantic_audit import (
    DEFAULT_DENSE_CAPTION_TIMING_PLAN_V2_PATH,
    DEFAULT_DENSE_SCRIPT_PACKAGE_V2_DOC_PATH,
    DEFAULT_DENSE_SCRIPT_PACKAGE_V2_PATH,
    DEFAULT_DENSE_SOURCE_YMMP_IMPORT_CSV_V2_PATH,
    DEFAULT_SEMANTIC_AUDIT_DOC_PATH,
    DEFAULT_SEMANTIC_AUDIT_PATH,
    DENSE_CAPTION_TIMING_PLAN_V2_ID,
    DENSE_SCRIPT_PACKAGE_V2_ID,
    NEXT_RECOMMENDED_SLICE,
    SEMANTIC_AUDIT_ID,
    TARGET_DENSE_SOURCE_YMMP_V1_PATH,
    TARGET_DENSE_SOURCE_YMMP_V2_PATH,
    TARGET_DURATION_SEC,
    build_default_newsroom_v0_1_dense_script_semantic_audit,
    build_newsroom_v0_1_dense_caption_timing_plan_v2,
    render_newsroom_v0_1_dense_script_package_v2_markdown,
    render_newsroom_v0_1_dense_script_semantic_audit_markdown,
)
from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    read_tiny_script_import_csv,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    OBSERVED_MANUAL_CHARACTER,
)


ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / DEFAULT_SEMANTIC_AUDIT_PATH
PACKAGE_PATH = ROOT / DEFAULT_DENSE_SCRIPT_PACKAGE_V2_PATH
TIMING_PLAN_PATH = ROOT / DEFAULT_DENSE_CAPTION_TIMING_PLAN_V2_PATH
CSV_PATH = ROOT / DEFAULT_DENSE_SOURCE_YMMP_IMPORT_CSV_V2_PATH
AUDIT_DOC_PATH = ROOT / DEFAULT_SEMANTIC_AUDIT_DOC_PATH
PACKAGE_DOC_PATH = ROOT / DEFAULT_DENSE_SCRIPT_PACKAGE_V2_DOC_PATH


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _csv_rows() -> list[list[str]]:
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_semantic_audit_matches_builder_and_rewrite_decision() -> None:
    audit = _json(AUDIT_PATH)

    assert audit == build_default_newsroom_v0_1_dense_script_semantic_audit(root=ROOT)
    assert audit["artifact_id"] == SEMANTIC_AUDIT_ID
    assert audit["audit_id"] == SEMANTIC_AUDIT_ID
    assert audit["production_status"] == "diagnostic_only"
    assert audit["current_dense_line_count"] == 13
    assert audit["baseline_line_count"] == 4
    assert audit["semantic_delta_result"] == "partial"
    assert audit["rewrite_needed"] is True
    assert audit["next_axis"] == NEXT_RECOMMENDED_SLICE
    assert audit["v2_line_count"] == 13
    assert audit["user_observation_normalized"] == {
        "dense_csv_import_saved_by_user": True,
        "mechanics_status": "pass_or_positive_signal",
        "semantic_density_status": "warning",
        "line_count_increase_not_sufficient": True,
        "next_axis": "semantic_script_audit_and_rewrite",
        "render_needed_now": False,
        "observation_source": "user_pasted_text",
    }


def test_user_saved_dense_v1_source_ymmp_is_ignored_local_evidence() -> None:
    audit = _json(AUDIT_PATH)
    access = audit["access_information"]["dense_v1_source_ymmp"]
    rel_path = TARGET_DENSE_SOURCE_YMMP_V1_PATH.as_posix()

    assert access["repo_relative_path"] == rel_path
    assert access["target_exists"] is True
    assert access["access_state"] == "verified_ignored_local_file_exists"
    assert access["commit_allowed"] is False
    assert access["file_full_path_current_host"] == str(
        (ROOT / TARGET_DENSE_SOURCE_YMMP_V1_PATH).resolve()
    )

    check_ignore = subprocess.run(
        ["git", "check-ignore", "-v", "--", rel_path],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    ls_files = subprocess.run(
        ["git", "ls-files", "--", rel_path],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert check_ignore.returncode == 0
    assert "_tmp/" in check_ignore.stdout
    assert ls_files.stdout == ""


def test_audit_criteria_capture_semantic_gap_not_line_count() -> None:
    audit = _json(AUDIT_PATH)
    criteria = {row["gate"]: row["status"] for row in audit["audit_criteria"]}
    weak_line_ids = {row["line_id"] for row in audit["weak_lines"]}
    padding_line_ids = {row["line_id"] for row in audit["repeated_or_padding_lines"]}

    assert criteria == {
        "semantic_delta_from_4_line_baseline": "partial",
        "problem_clarity": "partial",
        "offer_clarity": "partial",
        "proof_sequence_clarity": "pass",
        "boundary_clarity": "pass",
        "next_action_clarity": "partial",
        "viewer_value": "partial",
        "line_role_distinctness": "partial",
        "repetition_or_padding": "partial",
        "whether_13_lines_are_merely_split_text": "partial",
    }
    assert weak_line_ids == {
        "dense_line_001",
        "dense_line_003",
        "dense_line_005",
        "dense_line_012",
        "dense_line_013",
    }
    assert padding_line_ids == {"dense_line_004", "dense_line_005"}
    assert set(audit["missing_explanation_parts"]) == {
        "problem",
        "offer",
        "proof",
        "boundary",
        "next_action",
    }
    assert "line count" in audit["rewrite_reason"]


def test_v2_package_and_timing_match_builders_and_identity() -> None:
    audit = _json(AUDIT_PATH)
    package = _json(PACKAGE_PATH)
    timing_plan = _json(TIMING_PLAN_PATH)

    assert package == audit["v2_package"]
    assert package["artifact_id"] == DENSE_SCRIPT_PACKAGE_V2_ID
    assert package["package_id"] == DENSE_SCRIPT_PACKAGE_V2_ID
    assert package["production_status"] == "diagnostic_only"
    assert package["desired_viewer_action"] == (
        "understand the useful video draft offer and what to ask next"
    )
    assert [segment["segment_id"] for segment in package["segment_map"]] == [
        "opening",
        "mechanism",
        "proof",
        "boundary",
        "next_action",
    ]
    assert len(package["script_package"]) == 13

    assert timing_plan == build_newsroom_v0_1_dense_caption_timing_plan_v2(package)
    assert timing_plan["artifact_id"] == DENSE_CAPTION_TIMING_PLAN_V2_ID
    assert timing_plan["plan_id"] == DENSE_CAPTION_TIMING_PLAN_V2_ID
    assert timing_plan["timing_status"] == "planned_not_rendered"
    assert timing_plan["total_duration_sec"] == TARGET_DURATION_SEC
    assert timing_plan["line_count"] == len(package["script_package"])
    assert timing_plan["timing_policy"] == {
        "uses_exact_yym4_voice_duration": False,
        "timing_is_planned_until_dense_v2_source_render": True,
        "voice_audio_proof_for_dense_v2_script": False,
        "prior_render_evidence_reused_only": True,
    }


def test_v2_csv_is_utf8_bom_headerless_two_column_and_matches_package() -> None:
    package = _json(PACKAGE_PATH)
    rows = _csv_rows()
    readback = read_tiny_script_import_csv(CSV_PATH)

    assert CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf")
    assert readback["bom_verified"] is True
    assert readback["has_header"] is False
    assert readback["all_rows_two_columns"] is True
    assert readback["row_count"] == 13
    assert package["csv_spec"]["encoding"] == "UTF-8 BOM"
    assert package["csv_spec"]["python_encoding"] == "utf-8-sig"
    assert package["csv_spec"]["header"] is False
    assert package["csv_spec"]["columns"] == ["speaker", "text"]
    assert package["csv_spec"]["row_count"] == 13
    assert package["csv_spec"]["expected_character_binding"] == (
        OBSERVED_MANUAL_CHARACTER
    )
    assert rows == [
        [row["speaker"], row["text"]]
        for row in package["script_package"]
    ]
    assert all(row[0] == OBSERVED_MANUAL_CHARACTER for row in rows)


def test_v2_recheck_comparison_and_access_state_are_explicit() -> None:
    package = _json(PACKAGE_PATH)
    audit = _json(AUDIT_PATH)
    gates = {row["gate"]: row["status"] for row in package["explanation_readiness_recheck"]}
    comparison = package["comparison_v1_to_v2"]
    access = package["access_information"]

    assert gates == {
        "problem_clear": "pass",
        "offer_clear": "pass",
        "proof_clear": "pass",
        "boundary_clear": "pass",
        "next_action_clear": "pass",
        "audience_fit_proxy": "partial",
        "visual_supports_explanation": "pass",
        "access_clear": "pass",
    }
    assert audit["business_explanation_readiness"] == [
        {"gate": "problem_clear", "status": "pass"},
        {"gate": "offer_clear", "status": "pass"},
        {"gate": "proof_clear", "status": "pass"},
        {"gate": "boundary_clear", "status": "pass"},
        {"gate": "next_action_clear", "status": "pass"},
        {"gate": "audience_fit_proxy", "status": "partial"},
        {"gate": "visual_supports_explanation", "status": "pass"},
        {"gate": "access_clear", "status": "pass"},
    ]
    assert comparison["v1_line_count"] == 13
    assert comparison["v2_line_count"] == 13
    assert "requester problem" in comparison["semantic_change"]
    assert comparison["improved_parts"]["offer"] == (
        "v2 names the reviewable video draft as the useful artifact"
    )
    assert access["repo_relative_path"] == (
        DEFAULT_DENSE_SOURCE_YMMP_IMPORT_CSV_V2_PATH.as_posix()
    )
    assert access["target_exists"] is True
    assert access["access_state"] == "verified_current_host_file_exists"
    assert access["file_full_path_current_host"] == str(CSV_PATH.resolve())


def test_v2_target_source_ymmp_path_is_ignored_and_not_tracked() -> None:
    package = _json(PACKAGE_PATH)
    rel_path = TARGET_DENSE_SOURCE_YMMP_V2_PATH.as_posix()

    assert package["identity"]["target_source_ymmp_path"] == rel_path
    assert package["csv_spec"]["target_source_ymmp_path"] == rel_path

    check_ignore = subprocess.run(
        ["git", "check-ignore", "-v", "--", rel_path],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    ls_files = subprocess.run(
        ["git", "ls-files", "--", rel_path],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert check_ignore.returncode == 0
    assert "_tmp/" in check_ignore.stdout
    assert ls_files.stdout == ""


def test_docs_match_renderers_and_contract_counts() -> None:
    audit = _json(AUDIT_PATH)
    package = _json(PACKAGE_PATH)

    assert AUDIT_DOC_PATH.read_text(encoding="utf-8") == (
        render_newsroom_v0_1_dense_script_semantic_audit_markdown(audit)
    )
    assert PACKAGE_DOC_PATH.read_text(encoding="utf-8") == (
        render_newsroom_v0_1_dense_script_package_v2_markdown(package)
    )
    assert len(audit["completion_matrix"]) == 6
    assert len(audit["artifact_readiness"]) == 6
    assert len(audit["business_explanation_readiness"]) == 8
    assert len(audit["render_gate_hygiene"]) == 6
    assert len(audit["human_burden_hygiene"]) == 7
    assert len(audit["inertia_check"]) == 5
    assert len(package["render_gate_hygiene"]) == 6
    assert len(package["human_burden_hygiene"]) == 7
    assert package["card_alignment_summary"]["cards_regenerated_in_this_slice"] is False


def test_dense_semantic_artifacts_have_no_forbidden_positive_claims_or_media() -> None:
    combined = (
        AUDIT_PATH.read_text(encoding="utf-8")
        + PACKAGE_PATH.read_text(encoding="utf-8")
        + TIMING_PLAN_PATH.read_text(encoding="utf-8")
        + CSV_PATH.read_text(encoding="utf-8-sig")
        + AUDIT_DOC_PATH.read_text(encoding="utf-8")
        + PACKAGE_DOC_PATH.read_text(encoding="utf-8")
    )

    assert _real_url_pattern().search(combined) is None
    assert '"actual_order_or_audience_acceptance_claimed": true' not in combined
    assert '"actual_audience_acceptance_claimed": true' not in combined
    assert '"production_public_readiness_claimed": true' not in combined
    assert '"public_readiness": true' not in combined
    assert '"production_readiness": true' not in combined
    assert "public_ready: true" not in combined
    assert "production_approval: true" not in combined
    assert " ".join(["fixed", "review", "form", "is", "required"]) not in combined
    assert " ".join(["render", "again"]) not in combined.lower()
    assert not list(PACKAGE_PATH.parent.glob("v0_1_dense*.ymmp"))
    assert not list(PACKAGE_PATH.parent.glob("v0_1_dense*.mp4"))
    assert not list(PACKAGE_PATH.parent.glob("v0_1_dense*.wav"))
    assert not list(PACKAGE_PATH.parent.glob("v0_1_dense*.mp3"))
    assert not list(PACKAGE_PATH.parent.glob("v0_1_dense*.m4a"))
