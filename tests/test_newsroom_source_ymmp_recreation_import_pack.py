import csv
import json
import re
import subprocess
from pathlib import Path

from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
)
from src.pipeline.newsroom_source_ymmp_recreation_import_pack import (
    DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH,
    DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_PACK_DOC_PATH,
    DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_PACK_PATH,
    EXPECTED_CANONICAL_DIALOGUE_LINES,
    SOURCE_YMMP_RECREATION_IMPORT_PACK_ID,
    SOURCE_YMMP_RECREATION_IMPORT_PACK_SCHEMA_VERSION,
    TARGET_CARD_PLACEMENT_YMMP_PATH,
    TARGET_SOURCE_YMMP_DIR,
    TARGET_SOURCE_YMMP_PATH,
    TARGET_TIMING_PATCH_YMMP_PATH,
    build_default_newsroom_source_ymmp_recreation_import_pack,
    render_newsroom_source_ymmp_recreation_import_pack_markdown,
)
from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    read_tiny_script_import_csv,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    OBSERVED_MANUAL_CHARACTER,
)


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH
PACK_PATH = ROOT / DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_PACK_PATH
DOC_PATH = ROOT / DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_PACK_DOC_PATH


def _pack() -> dict:
    return json.loads(PACK_PATH.read_text(encoding="utf-8"))


def _csv_rows() -> list[list[str]]:
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_recreation_pack_matches_builder_output() -> None:
    pack = _pack()

    assert pack == build_default_newsroom_source_ymmp_recreation_import_pack(
        root=ROOT
    )
    assert pack["artifact_id"] == SOURCE_YMMP_RECREATION_IMPORT_PACK_ID
    assert pack["pack_id"] == SOURCE_YMMP_RECREATION_IMPORT_PACK_ID
    assert pack["schema_version"] == SOURCE_YMMP_RECREATION_IMPORT_PACK_SCHEMA_VERSION
    assert pack["review_status"] == "ready_for_operator_source_ymmp_recreation"
    assert pack["diagnostic_only"] is True
    assert pack["production_status"] == "diagnostic_only"
    assert pack["recreation_status"] == "csv_ready"
    assert pack["identity"]["output_csv_path"] == (
        DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH.as_posix()
    )
    assert pack["identity"]["target_source_ymmp_path"] == (
        TARGET_SOURCE_YMMP_PATH.as_posix()
    )


def test_csv_is_utf8_bom_headerless_two_column_yym4_import_shape() -> None:
    rows = _csv_rows()
    readback = read_tiny_script_import_csv(CSV_PATH)

    assert CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf")
    assert readback["bom_verified"] is True
    assert readback["has_header"] is False
    assert readback["all_rows_two_columns"] is True
    assert readback["row_count"] == 4
    assert rows == [
        [OBSERVED_MANUAL_CHARACTER, "Fake topic, review only."],
        [OBSERVED_MANUAL_CHARACTER, "Review-only handoff stays."],
        [OBSERVED_MANUAL_CHARACTER, "A fake claim is shown."],
        [OBSERVED_MANUAL_CHARACTER, "Fake source checks are noted."],
    ]


def test_source_evidence_records_canonical_speaker_lines_and_no_disagreement() -> None:
    evidence = _pack()["source_evidence"]

    assert evidence["canonical_speaker"] == OBSERVED_MANUAL_CHARACTER
    assert evidence["canonical_speaker"] == CANONICAL_UI_OBSERVED_SPEAKER
    assert evidence["canonical_speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )
    assert evidence["canonical_dialogue_lines"] == list(
        EXPECTED_CANONICAL_DIALOGUE_LINES
    )
    assert evidence["confidence"] == "high"
    assert evidence["disagreement_or_unknowns"] == []
    assert evidence["existing_bound_csv_bom_verified"] is True
    checks = evidence["evidence_checks"]
    assert checks["structure_lines_match_expected"] is True
    assert checks["csv_lines_match_expected"] is True
    assert checks["probe_target_lines_match_expected"] is True
    assert checks["structure_speaker_matches_expected"] is True
    assert checks["csv_speakers_match_expected"] is True
    assert checks["probe_target_speakers_match_expected"] is True
    assert checks["probe_source_validation_errors"] == []


def test_csv_spec_operator_target_and_continuation_are_explicit() -> None:
    pack = _pack()
    csv_spec = pack["csv_spec"]
    target = pack["operator_save_target"]
    continuation = pack["post_user_continuation"]

    assert csv_spec["encoding"] == "UTF-8 BOM"
    assert csv_spec["python_encoding"] == "utf-8-sig"
    assert csv_spec["header"] is False
    assert csv_spec["columns"] == ["speaker", "text"]
    assert csv_spec["row_count"] == 4
    assert csv_spec["yym4_import_mode"] == "台本読込"
    assert csv_spec["expected_character_binding"] == OBSERVED_MANUAL_CHARACTER
    assert target == {
        "target_dir": TARGET_SOURCE_YMMP_DIR.as_posix(),
        "target_source_ymmp": TARGET_SOURCE_YMMP_PATH.as_posix(),
        "note": "this .ymmp is ignored local only and must not be committed",
        "git_ignore_boundary": "_tmp/",
    }
    assert continuation["expected_next_local_outputs"] == [
        TARGET_TIMING_PATCH_YMMP_PATH.as_posix(),
        TARGET_CARD_PLACEMENT_YMMP_PATH.as_posix(),
    ]
    assert "timing patch" in continuation["after_source_ymmp_exists"][0]
    assert "card placement" in continuation["after_source_ymmp_exists"][1]


def test_safety_completion_hygiene_and_inertia_stay_bounded() -> None:
    pack = _pack()

    assert pack["safety_boundaries"] == {
        "ymmp_fabrication": False,
        "YMM4_launched_by_agent": False,
        "render_created_by_agent": False,
        "external_TTS_introduced": False,
        "audio_generated_by_agent": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "production_public_readiness": False,
        "ymmp_or_media_stage_allowed": False,
    }
    assert pack["completion_matrix"]["total"] == 6
    assert pack["completion_matrix"]["passed"] == 5
    assert pack["artifact_readiness"]["total"] == 6
    assert pack["artifact_readiness"]["passed"] == 6
    assert pack["human_burden_hygiene"] == {
        "user_input": "freeform",
        "template_required": False,
        "schema_owner": "Agent",
        "user_side_action": "YMM4 import/save only after this package",
        "future_look_for_max_count": 3,
        "negative_confirmation_checklist": False,
        "fixed_form_result_template": False,
    }
    assert pack["render_gate_hygiene"]["render_performed"] is False
    assert pack["render_gate_hygiene"]["YMM4_render_requested_in_this_slice"] is False
    assert pack["inertia_check"] == {
        "ymmp_fabrication": False,
        "broad_redesign": False,
        "packet_for_packet_drift": False,
        "local_artifact_gap_addressed_directly": True,
        "next_concrete_user_agent_action_named": True,
    }


def test_doc_matches_renderer_and_gives_exact_user_steps() -> None:
    pack = _pack()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_source_ymmp_recreation_import_pack_markdown(
        pack
    )
    assert "recreation_status: csv_ready" in doc_text
    assert "1. Open YMM4." in doc_text
    assert "2. Import `samples/_probe/newsroom_handoff/source_ymmp_recreation_import_v1.csv` via 台本読込." in doc_text
    assert f"3. Use `{OBSERVED_MANUAL_CHARACTER}` if speaker binding is requested." in doc_text
    assert "4. Confirm four lines appear." in doc_text
    assert f"5. Save as `{TARGET_SOURCE_YMMP_PATH.as_posix()}`." in doc_text
    assert "6. Do not render yet." in doc_text
    assert "freeform" in doc_text
    result_pattern = "result: " + "pass / fail"
    yes_no_pattern = "yes/no" + "/unclear"
    assert result_pattern not in doc_text
    assert yes_no_pattern not in doc_text.lower()
    assert "please render" not in doc_text.lower()


def test_source_target_is_ignored_tmp_and_not_a_tracked_artifact_contract() -> None:
    rel_path = TARGET_SOURCE_YMMP_PATH.as_posix()
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


def test_recreation_artifacts_have_no_real_urls_or_media_outputs() -> None:
    csv_text = CSV_PATH.read_text(encoding="utf-8-sig")
    pack_text = PACK_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(csv_text) is None
    assert _real_url_pattern().search(pack_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(PACK_PATH.parent.glob("source_ymmp_recreation_import*.ymmp"))
    assert not list(PACK_PATH.parent.glob("source_ymmp_recreation_import*.mp4"))
    assert not list(PACK_PATH.parent.glob("source_ymmp_recreation_import*.wav"))
    assert not list(PACK_PATH.parent.glob("source_ymmp_recreation_import*.mp3"))
    assert not list(PACK_PATH.parent.glob("source_ymmp_recreation_import*.m4a"))
