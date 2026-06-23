import csv
import json
import re
from pathlib import Path

from src.pipeline.newsroom_tiny_importable_proof import DEFAULT_TINY_IMPORT_CSV_PATH
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    DEFAULT_BOUND_SPEAKER_CSV_PATH,
    DEFAULT_SPEAKER_BINDING_POLICY_DOC_PATH,
    DEFAULT_SPEAKER_BINDING_POLICY_PATH,
    OBSERVED_MANUAL_CHARACTER,
    SOURCE_PLACEHOLDER_SPEAKER,
    SPEAKER_BINDING_POLICY_ID,
    SPEAKER_BINDING_POLICY_SCHEMA_VERSION,
    build_default_newsroom_yym4_speaker_binding_policy,
    render_newsroom_yym4_speaker_binding_policy_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / DEFAULT_SPEAKER_BINDING_POLICY_PATH
DOC_PATH = ROOT / DEFAULT_SPEAKER_BINDING_POLICY_DOC_PATH
BOUND_CSV_PATH = ROOT / DEFAULT_BOUND_SPEAKER_CSV_PATH
SOURCE_CSV_PATH = ROOT / DEFAULT_TINY_IMPORT_CSV_PATH


def _policy() -> dict:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _csv_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_speaker_binding_policy_matches_builder_output() -> None:
    policy = _policy()

    assert policy == build_default_newsroom_yym4_speaker_binding_policy(root=ROOT)
    assert policy["artifact_id"] == SPEAKER_BINDING_POLICY_ID
    assert policy["policy_id"] == SPEAKER_BINDING_POLICY_ID
    assert policy["schema_version"] == SPEAKER_BINDING_POLICY_SCHEMA_VERSION
    assert policy["review_status"] == "ready_for_supervisor_review"
    assert policy["diagnostic_only"] is True
    assert policy["production_status"] == "diagnostic_only"
    assert policy["policy_status"] == "diagnostic_candidate"
    assert policy["identity"]["source_tiny_csv_path"] == str(
        DEFAULT_TINY_IMPORT_CSV_PATH
    ).replace("\\", "/")
    assert policy["identity"]["policy_status"] == "diagnostic_candidate"


def test_observed_binding_preserves_manual_result_and_review_memory() -> None:
    policy = _policy()
    observed = policy["observed_binding"]
    review = policy["review_memory"]

    assert observed["source_placeholder_speaker"] == SOURCE_PLACEHOLDER_SPEAKER
    assert observed["observed_manual_character"] == OBSERVED_MANUAL_CHARACTER
    assert observed["observed_behavior"] == "manual_selection_required"
    assert observed["source_manual_result_behavior"] == (
        "mapped_after_manual_selection"
    )
    assert observed["import_result"] == "pass_with_warnings"
    assert observed["automatic_binding_observed"] is False
    assert observed["manual_selection_succeeded"] is True
    assert observed["observed_line_count"] == 4
    assert observed["expected_line_count"] == 4
    assert observed["all_text_visible"] is True
    assert observed["primary_warning_id"] == "manual_speaker_binding_required"
    assert review["prior_user_review_count"] == 1
    assert review["repeated_general_review_allowed"] is False
    assert review["next_nonredundant_axis"] == [
        "speaker_binding_policy",
        "placeholder_to_yym4_character_mapping",
        "bound_speaker_csv_candidate",
    ]
    assert review["not_accepted_scope"]["automatic_speaker_binding"] is False
    assert review["not_accepted_scope"]["ymmp"] is False
    assert review["not_accepted_scope"]["render"] is False


def test_binding_proposal_recommends_explicit_existing_character_candidate() -> None:
    policy = _policy()
    proposal = policy["binding_proposal"]
    mapping = policy["placeholder_to_yym4_character_mapping"]
    source_validation = policy["source_validation"]

    assert proposal["proposed_binding_mode"] == "emit_existing_yym4_character_name"
    assert proposal["recommended_default"]["mode"] == (
        "emit_existing_yym4_character_name"
    )
    assert "manual result showed" in proposal["recommended_default"]["reason"]
    assert proposal["candidate_speaker_name"] == OBSERVED_MANUAL_CHARACTER
    assert proposal["fallback_behavior"] == "manual selection remains allowed"
    assert proposal["automatic_binding_claimed"] is False
    assert mapping["source_placeholder_speaker"] == SOURCE_PLACEHOLDER_SPEAKER
    assert mapping["candidate_speaker_name"] == OBSERVED_MANUAL_CHARACTER
    assert mapping["mapping_basis"] == "operator_observed_manual_selection"
    assert mapping["applies_to_rows"] == [1, 2, 3, 4]
    assert source_validation["manual_result"] == "pass_with_warnings"
    assert source_validation["source_csv_bom_verified"] is True
    assert source_validation["source_csv_has_header"] is False
    assert source_validation["source_csv_all_rows_two_columns"] is True
    assert source_validation["errors"] == []


def test_bound_csv_candidate_changes_only_speaker_column() -> None:
    policy = _policy()
    candidate = policy["optional_bound_csv_candidate"]
    validation = candidate["validation"]
    source_rows = _csv_rows(SOURCE_CSV_PATH)
    bound_rows = _csv_rows(BOUND_CSV_PATH)

    assert BOUND_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf")
    assert candidate["created"] is True
    assert candidate["path"] == str(DEFAULT_BOUND_SPEAKER_CSV_PATH).replace("\\", "/")
    assert candidate["status"] == [
        "not_YMM4_verified",
        "intended_for_next_manual_check",
    ]
    assert candidate["csv_contract"] == {
        "encoding": "utf-8-sig",
        "preserve_utf8_bom": True,
        "has_header": False,
        "columns": ["speaker", "text"],
        "timing_columns_in_csv": False,
        "media_paths_in_csv": False,
        "production_ready_flags_in_csv": False,
    }
    assert len(bound_rows) == 4
    assert bound_rows[0] != ["speaker", "text"]
    assert all(len(row) == 2 for row in bound_rows)
    assert [row[1] for row in bound_rows] == [row[1] for row in source_rows]
    assert all(row[0] == OBSERVED_MANUAL_CHARACTER for row in bound_rows)
    assert all(row[0] == SOURCE_PLACEHOLDER_SPEAKER for row in source_rows)
    assert validation["row_count"] == 4
    assert validation["expected_row_count"] == 4
    assert validation["all_text_preserved_exactly"] is True
    assert validation["only_speaker_column_changed"] is True
    assert validation["no_timing_columns"] is True
    assert validation["no_media_paths"] is True
    assert validation["no_real_urls"] is True
    assert validation["no_production_ready_flags"] is True
    assert validation["automatic_binding_verified_by_YMM4"] is False
    assert validation["errors"] == []


def test_safety_next_actions_and_doc_match_renderer() -> None:
    policy = _policy()
    safety = policy["safety_boundary"]
    assertions = policy["boundary_assertions"]
    next_actions = policy["next_actions"]
    review_card = policy["review_card"]
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert safety == {
        "ymmp_created": False,
        "YMM4_launched_by_agent": False,
        "render_created": False,
        "TTS_generated": False,
        "real_media_imported": False,
        "production_approval": False,
        "public_video_ready": False,
    }
    assert assertions["source_tiny_csv_replaced"] is False
    assert assertions["bound_csv_is_new_artifact"] is True
    assert assertions["automatic_speaker_binding_claimed"] is False
    assert assertions["YMM4_approval"] is False
    assert assertions["external_fetch_performed"] is False
    assert assertions["dashboard_governance_freshness_changed"] is False
    assert next_actions["recommended_next_slice"] == (
        "newsroom-yym4-bound-speaker-manual-check-packet-v1"
    )
    assert "production .ymmp" in next_actions["do_not_recommend_immediate"]
    assert "render" in next_actions["do_not_recommend_immediate"]
    assert review_card["status"] == "none"
    assert review_card["axis_if_needed"] == "speaker_binding_policy"
    assert doc_text == render_newsroom_yym4_speaker_binding_policy_markdown(policy)
    assert "policy_status: diagnostic_candidate" in doc_text
    assert "Review Card: none" in doc_text
    assert "automatic_binding_observed: false" in doc_text
    assert "not_YMM4_verified" in doc_text


def test_speaker_binding_artifacts_have_no_real_urls_or_outputs() -> None:
    policy_text = POLICY_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    csv_text = BOUND_CSV_PATH.read_text(encoding="utf-8-sig")

    assert _real_url_pattern().search(policy_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert _real_url_pattern().search(csv_text) is None
    assert not list(POLICY_PATH.parent.glob("yym4_speaker_binding*.ymmp"))
    assert not list(POLICY_PATH.parent.glob("yym4_speaker_binding*.mp4"))
    assert not list(POLICY_PATH.parent.glob("yym4_speaker_binding*.wav"))
    assert not list(POLICY_PATH.parent.glob("yym4_speaker_binding*.mp3"))
    assert not list(POLICY_PATH.parent.glob("yym4_speaker_binding*.m4a"))
    assert not list(BOUND_CSV_PATH.parent.glob("*yukkuri_reimu*.ymmp"))
    assert not list(BOUND_CSV_PATH.parent.glob("*yukkuri_reimu*.mp4"))
    assert not list(BOUND_CSV_PATH.parent.glob("*yukkuri_reimu*.wav"))
