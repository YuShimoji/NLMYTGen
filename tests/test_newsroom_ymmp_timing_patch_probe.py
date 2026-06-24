import json
import re
import subprocess
from pathlib import Path

from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
)
from src.pipeline.newsroom_ymmp_timing_patch_probe import (
    DEFAULT_PATCHED_YMMP_LOCAL_PATH,
    DEFAULT_SOURCE_YMMP_LOCAL_PATH,
    DEFAULT_YMMP_TIMING_PATCH_PROBE_DOC_PATH,
    DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH,
    DEFAULT_YMMP_TIMING_PATCH_PROBE_READBACK_PATH,
    PATCH_METHOD,
    POST_PATCH_RENDER_SMOKE_SLICE,
    VOICE_PRESERVED_FIELDS,
    YMMP_TIMING_PATCH_PROBE_ID,
    YMMP_TIMING_PATCH_PROBE_READBACK_ID,
    YMMP_TIMING_PATCH_PROBE_READBACK_SCHEMA_VERSION,
    YMMP_TIMING_PATCH_PROBE_SCHEMA_VERSION,
    build_default_newsroom_ymmp_timing_patch_probe,
    render_newsroom_ymmp_timing_patch_probe_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
PROBE_PATH = ROOT / DEFAULT_YMMP_TIMING_PATCH_PROBE_PATH
READBACK_PATH = ROOT / DEFAULT_YMMP_TIMING_PATCH_PROBE_READBACK_PATH
DOC_PATH = ROOT / DEFAULT_YMMP_TIMING_PATCH_PROBE_DOC_PATH
SOURCE_YMMP_PATH = ROOT / DEFAULT_SOURCE_YMMP_LOCAL_PATH
PATCHED_YMMP_PATH = ROOT / DEFAULT_PATCHED_YMMP_LOCAL_PATH


def _probe() -> dict:
    return json.loads(PROBE_PATH.read_text(encoding="utf-8"))


def _readback() -> dict:
    return json.loads(READBACK_PATH.read_text(encoding="utf-8"))


def _ymmp(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _voice_items(root: dict) -> list[dict]:
    return [
        item
        for item in root["Timelines"][0]["Items"]
        if "VoiceItem" in item.get("$type", "")
    ]


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_timing_patch_probe_artifacts_match_builder_output() -> None:
    probe = _probe()
    readback = _readback()
    built_probe, built_readback = build_default_newsroom_ymmp_timing_patch_probe(
        root=ROOT
    )

    assert probe == built_probe
    assert readback == built_readback
    assert probe["artifact_id"] == YMMP_TIMING_PATCH_PROBE_ID
    assert probe["probe_id"] == YMMP_TIMING_PATCH_PROBE_ID
    assert probe["schema_version"] == YMMP_TIMING_PATCH_PROBE_SCHEMA_VERSION
    assert probe["probe_status"] == "applied_to_ignored_local_copy_after_validation"
    assert readback["artifact_id"] == YMMP_TIMING_PATCH_PROBE_READBACK_ID
    assert readback["readback_id"] == YMMP_TIMING_PATCH_PROBE_READBACK_ID
    assert readback["schema_version"] == (
        YMMP_TIMING_PATCH_PROBE_READBACK_SCHEMA_VERSION
    )
    assert readback["readback_status"] == "structural_pass"


def test_source_validation_selects_neutral_timeline_voice_preserving_patch() -> None:
    probe = _probe()
    validation = probe["source_validation"]
    selected = probe["selected_patch_method"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["canonical_speaker"] == CANONICAL_UI_OBSERVED_SPEAKER
    assert validation["canonical_speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )
    assert validation["source_fps"] == 60
    assert validation["source_total_frames"] == 509
    assert validation["target_total_frames"] == 4080
    assert validation["source_voice_item_count"] == 4
    assert validation["neutral_caption_count"] == 4
    assert selected["choice"] == PATCH_METHOD
    assert selected["strategy_slice"] == "newsroom-ymmp-timing-patch-probe-v1"


def test_mapping_uses_neutral_caption_anchors_at_60fps() -> None:
    probe = _probe()
    mapping = probe["mapping"]

    assert mapping["status"] == "mapped"
    assert mapping["mapping_method"] == "text_and_order"
    assert mapping["unmatched_items"] == []
    assert probe["target_timeline"] == {
        "timebase_fps": 60,
        "target_total_sec": 68,
        "target_total_frames": 4080,
        "anchors_sec": [0, 12, 24, 46, 68],
        "anchors_frames": [0, 720, 1440, 2760, 4080],
        "item_lengths_frames": [720, 720, 1320, 1320],
    }
    assert [row["text"] for row in mapping["items"]] == [
        "Fake topic, review only.",
        "Review-only handoff stays.",
        "A fake claim is shown.",
        "Fake source checks are noted.",
    ]
    assert [row["target_frame"] for row in mapping["items"]] == [
        0,
        720,
        1440,
        2760,
    ]
    assert [row["target_length_frames"] for row in mapping["items"]] == [
        720,
        720,
        1320,
        1320,
    ]


def test_patch_operations_only_touch_timeline_length_and_voiceitem_timing() -> None:
    operations = _probe()["patch_operations"]

    assert len(operations) == 9
    assert operations[0] == {
        "operation_id": "timeline_length_to_4080_frames",
        "operation_kind": "set_timeline_duration",
        "target_path": "Timelines[0].Length",
        "field_changed": "Timeline.Length",
        "before": 509,
        "after": 4080,
        "allowed_by_strategy": True,
        "applied": True,
        "reason": (
            "extend diagnostic timeline from natural 509 frames to neutral 68 "
            "sec / 4080 frames"
        ),
    }
    changed_fields = [row["field_changed"] for row in operations]
    assert changed_fields == [
        "Timeline.Length",
        "Frame",
        "Length",
        "Frame",
        "Length",
        "Frame",
        "Length",
        "Frame",
        "Length",
    ]
    assert all(row["allowed_by_strategy"] is True for row in operations)
    assert all(row["applied"] is True for row in operations)
    assert _probe()["field_preservation_plan"]["must_preserve"] == list(
        VOICE_PRESERVED_FIELDS
    )


def test_structural_readback_reaches_68_seconds_without_render_acceptance() -> None:
    readback = _readback()
    structural = readback["structural_result"]
    timing = readback["before_after_timing"]

    assert structural["structural_readback_status"] == "pass"
    assert structural["source_total_frames"] == 509
    assert structural["source_total_sec"] == round(509 / 60, 6)
    assert structural["patched_total_frames"] == 4080
    assert structural["patched_total_sec"] == 68.0
    assert structural["patched_frames"] == [0, 720, 1440, 2760]
    assert structural["patched_lengths"] == [720, 720, 1320, 1320]
    assert structural["patched_end_frames"] == [720, 1440, 2760, 4080]
    assert structural["target_68_sec_reached_structurally"] is True
    assert structural["render_required_before_video_acceptance"] is True
    assert timing["patched_item_end_frames"] == [720, 1440, 2760, 4080]
    assert readback["not_accepted_scope"]["post_patch_render_smoke"] is False
    assert readback["not_accepted_scope"]["neutral_68_sec_video_acceptance"] is False


def test_voice_fields_are_preserved_in_readback_and_actual_patched_copy() -> None:
    readback = _readback()
    preservation = readback["field_preservation_readback"]
    source_items = _voice_items(_ymmp(SOURCE_YMMP_PATH))
    patched_items = _voice_items(_ymmp(PATCHED_YMMP_PATH))

    assert preservation["all_required_fields_preserved"] is True
    assert preservation["characters_block_preserved"] is True
    assert preservation["external_TTS_introduced"] is False
    assert preservation["voice_regenerated"] is False
    assert len(source_items) == len(patched_items) == 4
    for source, patched, row in zip(
        source_items, patched_items, preservation["per_item"]
    ):
        assert row["all_required_fields_preserved"] is True
        for field in VOICE_PRESERVED_FIELDS:
            assert source.get(field) == patched.get(field)
            assert row["fields"][field] is True


def test_actual_patched_ymmp_copy_has_expected_timing_and_source_stays_natural() -> None:
    source_root = _ymmp(SOURCE_YMMP_PATH)
    patched_root = _ymmp(PATCHED_YMMP_PATH)
    source_timeline = source_root["Timelines"][0]
    patched_timeline = patched_root["Timelines"][0]
    patched_voice_items = _voice_items(patched_root)

    assert source_timeline["Length"] == 509
    assert [item["Frame"] for item in _voice_items(source_root)] == [
        0,
        130,
        255,
        369,
    ]
    assert patched_timeline["Length"] == 4080
    assert patched_timeline["VideoInfo"]["FPS"] == 60
    assert [item["Frame"] for item in patched_voice_items] == [
        0,
        720,
        1440,
        2760,
    ]
    assert [item["Length"] for item in patched_voice_items] == [
        720,
        720,
        1320,
        1320,
    ]


def test_patched_ymmp_copy_is_ignored_and_not_tracked() -> None:
    rel_path = DEFAULT_PATCHED_YMMP_LOCAL_PATH.as_posix()
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
    status = subprocess.run(
        ["git", "status", "--short", "--", rel_path],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert PATCHED_YMMP_PATH.exists()
    assert check_ignore.returncode == 0
    assert "_tmp/" in check_ignore.stdout
    assert ls_files.stdout == ""
    assert status.stdout == ""
    assert _readback()["local_file_status"]["ymmp_or_media_staged"] is False


def test_render_gate_and_boundaries_keep_forbidden_work_out_of_slice() -> None:
    readback = _readback()

    assert readback["render_gate"] == {
        "render_performed_in_this_slice": False,
        "YMM4_launched_by_agent": False,
        "render_deferred_until_structural_readback_passes": True,
        "next_render_trigger": (
            "patched copy structurally reaches 68 sec and preserves native "
            "voice fields"
        ),
        "next_recommended_slice": POST_PATCH_RENDER_SMOKE_SLICE,
        "repeated_audio_check_requested": False,
    }
    assert readback["boundaries"] == {
        "YMM4_launched_by_agent": False,
        "render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "source_ymmp_modified": False,
        "patched_ymmp_copy_created_under_ignored_tmp": True,
        "ymmp_or_media_staged_or_committed": False,
        "production_approval": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


def test_doc_matches_renderer_and_has_no_fixed_form_or_render_recheck() -> None:
    probe = _probe()
    readback = _readback()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_ymmp_timing_patch_probe_markdown(
        probe, readback
    )
    assert "probe_status: applied_to_ignored_local_copy_after_validation" in doc_text
    assert "readback_status: structural_pass" in doc_text
    assert "Timelines[0].Length | 509 | 4080 | true" in doc_text
    assert "next_recommended_slice: newsroom-ymmp-timing-patch-render-smoke-v1" in (
        doc_text
    )
    assert "result: pass / fail" not in doc_text
    assert "yes/no/unclear" not in doc_text.lower()
    assert "please render" not in doc_text.lower()
    assert "please check audio" not in doc_text.lower()


def test_timing_patch_probe_artifacts_have_no_real_urls_or_media_outputs() -> None:
    probe_text = PROBE_PATH.read_text(encoding="utf-8")
    readback_text = READBACK_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(probe_text) is None
    assert _real_url_pattern().search(readback_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(PROBE_PATH.parent.glob("*ymmp_timing_patch_probe*.ymmp"))
    assert not list(PROBE_PATH.parent.glob("*ymmp_timing_patch_probe*.mp4"))
    assert not list(PROBE_PATH.parent.glob("*ymmp_timing_patch_probe*.wav"))
    assert not list(PROBE_PATH.parent.glob("*ymmp_timing_patch_probe*.mp3"))
    assert not list(PROBE_PATH.parent.glob("*ymmp_timing_patch_probe*.m4a"))
