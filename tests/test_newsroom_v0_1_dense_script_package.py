import csv
import json
import re
import subprocess
from pathlib import Path

from src.pipeline.newsroom_v0_1_dense_script_package import (
    DEFAULT_DENSE_CAPTION_TIMING_PLAN_PATH,
    DEFAULT_DENSE_SCRIPT_PACKAGE_DOC_PATH,
    DEFAULT_DENSE_SCRIPT_PACKAGE_PATH,
    DEFAULT_DENSE_SOURCE_YMMP_IMPORT_CSV_PATH,
    DEFAULT_DENSE_SOURCE_YMMP_IMPORT_DOC_PATH,
    DENSE_CAPTION_TIMING_PLAN_ID,
    DENSE_CAPTION_TIMING_PLAN_SCHEMA_VERSION,
    DENSE_SCRIPT_PACKAGE_ID,
    DENSE_SCRIPT_PACKAGE_SCHEMA_VERSION,
    NEXT_RECOMMENDED_SLICE,
    TARGET_DENSE_SOURCE_YMMP_PATH,
    TARGET_DURATION_SEC,
    TARGET_LINE_COUNT_RANGE,
    build_default_newsroom_v0_1_dense_caption_timing_plan,
    build_default_newsroom_v0_1_dense_script_package,
    render_newsroom_v0_1_dense_script_package_markdown,
    render_newsroom_v0_1_dense_source_ymmp_import_markdown,
)
from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    read_tiny_script_import_csv,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    OBSERVED_MANUAL_CHARACTER,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / DEFAULT_DENSE_SCRIPT_PACKAGE_PATH
TIMING_PLAN_PATH = ROOT / DEFAULT_DENSE_CAPTION_TIMING_PLAN_PATH
CSV_PATH = ROOT / DEFAULT_DENSE_SOURCE_YMMP_IMPORT_CSV_PATH
PACKAGE_DOC_PATH = ROOT / DEFAULT_DENSE_SCRIPT_PACKAGE_DOC_PATH
CSV_DOC_PATH = ROOT / DEFAULT_DENSE_SOURCE_YMMP_IMPORT_DOC_PATH


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _csv_rows() -> list[list[str]]:
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _real_url_pattern() -> re.Pattern[str]:
    return re.compile(r"https?://|www\.", flags=re.IGNORECASE)


def test_dense_script_package_matches_builder_and_identity() -> None:
    package = _json(PACKAGE_PATH)

    assert package == build_default_newsroom_v0_1_dense_script_package(root=ROOT)
    assert package["artifact_id"] == DENSE_SCRIPT_PACKAGE_ID
    assert package["package_id"] == DENSE_SCRIPT_PACKAGE_ID
    assert package["schema_version"] == DENSE_SCRIPT_PACKAGE_SCHEMA_VERSION
    assert package["review_status"] == "ready_for_operator_dense_source_import"
    assert package["production_status"] == "diagnostic_only"
    assert package["business_goal_primary"] == "understanding/adoption"
    assert package["identity"]["output_csv_path"] == (
        DEFAULT_DENSE_SOURCE_YMMP_IMPORT_CSV_PATH.as_posix()
    )
    assert package["identity"]["target_source_ymmp_path"] == (
        TARGET_DENSE_SOURCE_YMMP_PATH.as_posix()
    )
    assert package["identity"]["actual_order_or_audience_acceptance_claimed"] is False
    assert package["source_validation"]["status"] == "passed"
    assert package["source_validation"]["errors"] == []


def test_dense_script_lines_fit_density_segment_and_timing_contract() -> None:
    package = _json(PACKAGE_PATH)
    rows = package["script_package"]
    segments = {segment["segment_id"]: segment for segment in package["segment_map"]}

    assert TARGET_LINE_COUNT_RANGE["min"] <= len(rows) <= TARGET_LINE_COUNT_RANGE["max"]
    assert len(rows) == 13
    assert rows[0]["intended_start_sec"] == 0
    assert rows[-1]["intended_end_sec"] == TARGET_DURATION_SEC
    assert all(row["speaker"] == OBSERVED_MANUAL_CHARACTER for row in rows)
    assert all(row["diagnostic_only"] is True for row in rows)
    assert [segment["segment_id"] for segment in package["segment_map"]] == [
        "opening",
        "mechanism",
        "proof",
        "boundary",
        "next_action",
    ]
    assert segments["opening"]["line_ids"] == ["dense_line_001", "dense_line_002"]
    assert segments["mechanism"]["line_ids"] == [
        "dense_line_003",
        "dense_line_004",
        "dense_line_005",
    ]
    assert segments["proof"]["line_ids"] == [
        "dense_line_006",
        "dense_line_007",
        "dense_line_008",
        "dense_line_009",
    ]
    assert segments["boundary"]["line_ids"] == ["dense_line_010", "dense_line_011"]
    assert segments["next_action"]["line_ids"] == [
        "dense_line_012",
        "dense_line_013",
    ]
    assert {
        row["explanation_role"] for row in rows
    } >= {"problem", "offer", "mechanism", "proof", "boundary", "next_action"}


def test_dense_csv_is_utf8_bom_headerless_two_column_and_matches_script() -> None:
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
    assert package["csv_spec"]["yym4_import_mode"] == "蜿ｰ譛ｬ隱ｭ霎ｼ"
    assert package["csv_spec"]["expected_character_binding"] == OBSERVED_MANUAL_CHARACTER
    assert package["csv_spec"]["prompt_speaker_text_seen"] == "繧・▲縺上ｊ髴雁､｢"
    assert rows == [
        [row["speaker"], row["text"]]
        for row in package["script_package"]
    ]


def test_timing_plan_matches_builder_and_marks_planned_not_rendered() -> None:
    package = _json(PACKAGE_PATH)
    timing_plan = _json(TIMING_PLAN_PATH)

    assert timing_plan == build_default_newsroom_v0_1_dense_caption_timing_plan(
        root=ROOT
    )
    assert timing_plan["artifact_id"] == DENSE_CAPTION_TIMING_PLAN_ID
    assert timing_plan["plan_id"] == DENSE_CAPTION_TIMING_PLAN_ID
    assert (
        timing_plan["schema_version"]
        == DENSE_CAPTION_TIMING_PLAN_SCHEMA_VERSION
    )
    assert timing_plan["timing_status"] == "planned_not_rendered"
    assert timing_plan["source_package_id"] == package["package_id"]
    assert timing_plan["total_duration_sec"] == TARGET_DURATION_SEC
    assert timing_plan["line_count"] == len(package["script_package"])
    assert timing_plan["line_timings"][0]["intended_start_sec"] == 0
    assert timing_plan["line_timings"][-1]["intended_end_sec"] == TARGET_DURATION_SEC
    assert timing_plan["timing_policy"] == {
        "uses_exact_yym4_voice_duration": False,
        "timing_is_planned_until_dense_source_render": True,
        "voice_audio_proof_for_dense_script": False,
        "prior_render_evidence_reused_only": True,
    }


def test_explanation_readiness_recheck_improves_without_audience_claim() -> None:
    package = _json(PACKAGE_PATH)
    gates = {row["gate"]: row for row in package["explanation_readiness_recheck"]}
    business = {row["gate"]: row["status"] for row in package["business_explanation_readiness"]}

    assert gates["problem_clear"]["status"] == "pass"
    assert gates["offer_clear"]["status"] == "pass"
    assert gates["proof_clear"]["status"] == "pass"
    assert gates["boundary_clear"]["status"] == "pass"
    assert gates["next_action_clear"]["status"] == "pass"
    assert gates["audience_fit_proxy"]["status"] == "partial"
    assert gates["visual_supports_explanation"]["status"] == "pass"
    assert business == {
        "problem_clear": "pass",
        "offer_clear": "pass",
        "proof_clear": "pass",
        "boundary_clear": "pass",
        "next_action_clear": "pass",
        "audience_fit_proxy": "partial",
        "visual_supports_explanation": "pass",
    }
    assert package["next_recommended_slice"]["selected"] == NEXT_RECOMMENDED_SLICE


def test_baseline_comparison_and_card_alignment_are_explicit() -> None:
    package = _json(PACKAGE_PATH)
    comparison = package["baseline_comparison"]
    card_alignment = package["card_alignment_summary"]

    assert comparison["baseline_line_count"] == 4
    assert comparison["new_line_count"] == 13
    assert comparison["new_seconds_per_line"] < comparison["baseline_seconds_per_line"]
    assert set(comparison["what_is_added"]) == {
        "problem",
        "offer",
        "proof_sequence",
        "boundary",
        "next_action",
    }
    assert card_alignment["existing_card_count"] == 4
    assert card_alignment["new_segment_count"] == 5
    assert card_alignment["next_action_segment_handling"] == "carried_by_card_4_next_status"
    assert card_alignment["future_card_count_expansion_needed_for_this_slice"] is False
    assert card_alignment["cards_regenerated_in_this_slice"] is False


def test_completion_artifact_render_human_and_inertia_counts_match_contract() -> None:
    package = _json(PACKAGE_PATH)

    assert len(package["completion_matrix"]) == 6
    assert len(package["artifact_readiness"]) == 6
    assert len(package["business_explanation_readiness"]) == 7
    assert len(package["render_gate_hygiene"]) == 6
    assert len(package["human_burden_hygiene"]) == 7
    assert len(package["inertia_check"]) == 5
    assert package["not_accepted_scope"] == {
        "render_proof_for_dense_script": False,
        "audio_proof_for_dense_script": False,
        "production_readiness": False,
        "public_readiness": False,
        "real_rss_or_news_content": False,
        "real_source_approval": False,
        "final_narration_quality": False,
        "automated_yym4_render_claim": False,
        "actual_order_or_audience_acceptance": False,
    }
    assert package["boundaries"]["YMM4_launched_by_agent"] is False
    assert package["boundaries"]["render_performed_by_agent"] is False
    assert package["boundaries"]["ymmp_edited_or_committed"] is False
    assert package["boundaries"]["audio_tts_generated"] is False
    assert package["boundaries"]["real_rss_or_news_fetched"] is False


def test_docs_match_renderers_and_include_freeform_operator_steps() -> None:
    package = _json(PACKAGE_PATH)
    timing_plan = _json(TIMING_PLAN_PATH)
    package_doc = PACKAGE_DOC_PATH.read_text(encoding="utf-8")
    csv_doc = CSV_DOC_PATH.read_text(encoding="utf-8")

    assert package_doc == render_newsroom_v0_1_dense_script_package_markdown(package)
    assert csv_doc == render_newsroom_v0_1_dense_source_ymmp_import_markdown(
        package,
        timing_plan,
    )
    assert "Confirm thirteen dialogue rows appear." in csv_doc
    assert "Do not render in this import/save step." in csv_doc
    assert "freeform observation" in csv_doc
    assert "A structured answer is not needed." in csv_doc
    fixed_form_pattern = " ".join(["fixed", "review", "form", "is", "required"])
    result_pattern = "result: " + "pass / fail"
    yes_no_pattern = "yes" + "/no"
    assert fixed_form_pattern not in csv_doc
    assert result_pattern not in csv_doc.lower()
    assert yes_no_pattern not in csv_doc.lower()


def test_target_dense_source_ymmp_is_ignored_and_not_tracked_contract() -> None:
    rel_path = TARGET_DENSE_SOURCE_YMMP_PATH.as_posix()
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


def test_dense_artifacts_have_no_real_urls_or_positive_acceptance_claims() -> None:
    combined = (
        PACKAGE_PATH.read_text(encoding="utf-8")
        + TIMING_PLAN_PATH.read_text(encoding="utf-8")
        + CSV_PATH.read_text(encoding="utf-8-sig")
        + PACKAGE_DOC_PATH.read_text(encoding="utf-8")
        + CSV_DOC_PATH.read_text(encoding="utf-8")
    )

    assert _real_url_pattern().search(combined) is None
    assert '"actual_order_or_audience_acceptance_claimed": true' not in combined
    assert '"actual_audience_acceptance_claimed": true' not in combined
    assert '"production_public_readiness_claimed": true' not in combined
    assert '"public_readiness": true' not in combined
    assert '"production_readiness": true' not in combined
    assert "public_ready: true" not in combined
    assert "production_approval: true" not in combined
    render_again_pattern = " ".join(["render", "again"])
    assert render_again_pattern not in combined.lower()
    assert not list(PACKAGE_PATH.parent.glob("v0_1_dense*.ymmp"))
    assert not list(PACKAGE_PATH.parent.glob("v0_1_dense*.mp4"))
    assert not list(PACKAGE_PATH.parent.glob("v0_1_dense*.wav"))
    assert not list(PACKAGE_PATH.parent.glob("v0_1_dense*.mp3"))
    assert not list(PACKAGE_PATH.parent.glob("v0_1_dense*.m4a"))
