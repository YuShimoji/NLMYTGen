import csv
import json
import re
from pathlib import Path

from src.pipeline.newsroom_neutral_timeline_import_proof import (
    CAPTION_CSV_COLUMNS,
    DEFAULT_CAPTION_IMPORT_CSV_PATH,
    DEFAULT_NEUTRAL_TIMELINE_DOC_PATH,
    DEFAULT_NEUTRAL_TIMELINE_PATH,
    NEUTRAL_TIMELINE_ID,
    NEUTRAL_TIMELINE_SCHEMA_VERSION,
    build_default_newsroom_neutral_timeline_import_proof,
    render_caption_import_candidate_csv,
    render_newsroom_neutral_timeline_import_proof_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
TIMELINE_PATH = ROOT / DEFAULT_NEUTRAL_TIMELINE_PATH
CAPTION_CSV_PATH = ROOT / DEFAULT_CAPTION_IMPORT_CSV_PATH
TIMELINE_DOC_PATH = ROOT / DEFAULT_NEUTRAL_TIMELINE_DOC_PATH


def _timeline() -> dict:
    return json.loads(TIMELINE_PATH.read_text(encoding="utf-8"))


def _items_by_kind(timeline: dict, item_kind: str) -> list[dict]:
    return [
        item
        for item in timeline["items"]
        if item["item_kind"] == item_kind
    ]


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_neutral_timeline_parses_and_matches_builder_output() -> None:
    timeline = _timeline()
    identity = timeline["identity"]

    assert timeline == build_default_newsroom_neutral_timeline_import_proof(root=ROOT)
    assert timeline["timeline_id"] == NEUTRAL_TIMELINE_ID
    assert timeline["artifact_id"] == NEUTRAL_TIMELINE_ID
    assert timeline["schema_version"] == NEUTRAL_TIMELINE_SCHEMA_VERSION
    assert timeline["review_status"] == "ready_for_supervisor_review"
    assert timeline["diagnostic_only"] is True
    assert timeline["production_status"] == "diagnostic_only"
    assert timeline["import_status"] == "diagnostic_candidate_with_placeholders"
    assert identity["timeline_id"] == NEUTRAL_TIMELINE_ID
    assert identity["source_episode_id"] == "episode_fake_nlmytgen_delta_v1"
    assert set(identity["source_artifacts"]) == {
        "episode_capsule",
        "caption_timing_plan",
        "caption_copy_refinement",
        "diagnostic_transfer_candidate_proof",
    }


def test_global_timing_tracks_and_items_have_neutral_schema() -> None:
    timeline = _timeline()
    timing = timeline["global_timing"]
    tracks = timeline["tracks"]
    items = timeline["items"]

    assert timing["total_duration_sec"] == 68
    assert timing["timebase"] == "seconds"
    assert timing["fps_policy"] == {
        "fps": None,
        "placeholder": False,
        "policy": "not_required_for_neutral_timeline",
    }
    assert timing["timing_confidence"] == "provisional"
    assert {track["track_kind"] for track in tracks} == {
        "captions",
        "visuals",
        "markers",
        "audio_placeholder",
    }
    assert all(track["diagnostic_only"] is True for track in tracks)
    assert all(track["production_ready"] is False for track in tracks)
    assert len(items) == 9
    for item in items:
        for field in [
            "item_id",
            "track_id",
            "item_kind",
            "start_sec",
            "end_sec",
            "duration_sec",
            "source_ref",
            "beat_id",
            "blocked_for_production",
            "diagnostic_import_allowed",
            "notes",
        ]:
            assert field in item
        assert item["start_sec"] <= item["end_sec"]
        assert item["duration_sec"] == item["end_sec"] - item["start_sec"]
        assert item["diagnostic_only"] is True
        assert item["production_ready"] is False
        assert item["blocked_for_production"] is True
        assert item["diagnostic_import_allowed"] is True


def test_caption_items_preserve_refined_copy_and_timing() -> None:
    timeline = _timeline()
    captions = _items_by_kind(timeline, "caption")

    assert [item["caption_id"] for item in captions] == [
        "cap_beat_fake_intro_001_01",
        "cap_beat_fake_intro_001_02",
        "cap_beat_fake_claim_001_01",
        "cap_beat_fake_claim_001_02",
    ]
    assert [item["text"] for item in captions] == [
        "Fake topic, review only.",
        "Review-only handoff stays.",
        "A fake claim is shown.",
        "Fake source checks are noted.",
    ]
    assert [(item["start_sec"], item["end_sec"]) for item in captions] == [
        (0, 12),
        (12, 24),
        (24, 46),
        (46, 68),
    ]
    assert [item["reading_density"] for item in captions] == [
        "medium",
        "medium",
        "low",
        "low",
    ]
    for item in captions:
        assert item["char_count"] == len(item["text"])
        assert item["line_count_target"] == 2
        assert item["max_chars_target"] == 34
        assert item["contains_real_names"] is False
        assert item["contains_real_claims"] is False
        assert item["contains_urls"] is False
        assert _real_url_pattern().search(item["text"]) is None


def test_visual_and_audio_placeholders_have_no_media_or_tts_dependency() -> None:
    timeline = _timeline()
    visuals = _items_by_kind(timeline, "visual_placeholder")
    audio = _items_by_kind(timeline, "audio_placeholder")

    assert len(visuals) == 2
    assert {
        item["visual_id"]: item["g28_slot"]
        for item in visuals
    } == {
        "visual_fake_title_card_001": "caption_reserve",
        "visual_fake_evidence_card_001": "source_note",
    }
    assert {
        item["visual_id"]: item["layout_hint"]
        for item in visuals
    } == {
        "visual_fake_title_card_001": "title_card",
        "visual_fake_evidence_card_001": "article_quote_card",
    }
    for item in visuals:
        assert item["media_file_dependency"] == "none"
        assert item["media_required"] is False
        assert item["caption_interference_note"]
        assert "No media file" in item["notes"][0]

    assert len(audio) == 1
    audio_item = audio[0]
    assert audio_item["voice_status"] == "not_started"
    assert audio_item["TTS_generated"] is False
    assert audio_item["audio_required_for_this_proof"] is False
    assert audio_item["media_file_dependency"] == "none"
    assert audio_item["start_sec"] == 0
    assert audio_item["end_sec"] == 68


def test_blocker_carry_forward_and_next_mapping_policy_keep_production_closed() -> None:
    timeline = _timeline()
    blockers = timeline["blocker_carry_forward"]
    policy = timeline["next_mapping_policy"]
    boundary = timeline["boundary_assertions"]

    assert blockers["production_transfer_status"] == "blocked"
    assert blockers["diagnostic_import_status"] == "candidate_with_placeholders"
    assert blockers["YMM4_candidate"] is False
    assert blockers["production_approval"] is False
    assert blockers["blocker_summary"] == {
        "production_only": 7,
        "diagnostic_hard_blocker": 0,
        "diagnostic_soft_warning": 5,
        "already_satisfied_for_synthetic": 1,
        "total_blockers": 13,
        "diagnostic_hard_blocker_codes": [],
    }
    assert policy["recommended_next_slice"] == "newsroom-caption-csv-import-candidate-v1"
    assert policy["allowed_next_artifacts"] == [
        "neutral timeline JSON",
        "caption CSV",
        "script-import candidate",
    ]
    assert "production .ymmp" in policy["prohibited_next_artifacts"]
    assert "render output" in policy["prohibited_next_artifacts"]
    assert "TTS output" in policy["prohibited_next_artifacts"]
    assert boundary["neutral_timeline_json_is_source_of_truth"] is True
    assert boundary["caption_csv_derived_from_json"] is True
    assert boundary["opens_production_transfer"] is False
    assert boundary["opens_YMM4_transfer"] is False
    assert boundary["ymmp_generated"] is False
    assert boundary["render_generated"] is False
    assert boundary["tts_generated"] is False
    assert boundary["public_video"] is False


def test_caption_csv_is_derived_from_neutral_timeline_json() -> None:
    timeline = _timeline()
    csv_text = CAPTION_CSV_PATH.read_text(encoding="utf-8")
    rows = list(csv.DictReader(csv_text.splitlines()))

    assert csv_text == render_caption_import_candidate_csv(timeline)
    assert timeline["caption_csv"]["status"] == "created"
    assert timeline["caption_csv"]["row_count"] == 4
    assert timeline["caption_csv"]["columns"] == list(CAPTION_CSV_COLUMNS)
    assert rows
    assert list(rows[0].keys()) == list(CAPTION_CSV_COLUMNS)
    caption_items = _items_by_kind(timeline, "caption")
    for row, item in zip(rows, caption_items, strict=True):
        assert row["caption_id"] == item["caption_id"]
        assert row["beat_id"] == item["beat_id"]
        assert int(row["start_sec"]) == item["start_sec"]
        assert int(row["end_sec"]) == item["end_sec"]
        assert int(row["duration_sec"]) == item["duration_sec"]
        assert row["text"] == item["text"]
        assert row["diagnostic_only"] == "true"
        assert row["production_ready"] == "false"


def test_neutral_timeline_review_memory_and_doc_match_renderer() -> None:
    timeline = _timeline()
    review_memory = timeline["review_memory"]
    review_card = timeline["review_card"]
    doc_text = TIMELINE_DOC_PATH.read_text(encoding="utf-8")

    assert review_memory["prior_user_review_count"] == 0
    assert "diagnostic_transfer_candidate_classification" in review_memory[
        "accepted_scope"
    ]
    assert "neutral_timeline_import_proof" in review_memory["next_nonredundant_axis"]
    assert review_memory["repeated_general_review_allowed"] is False
    assert review_card["status"] == "none"
    assert review_card["axis_if_needed"] == "neutral_timeline_import_schema"
    assert doc_text == render_newsroom_neutral_timeline_import_proof_markdown(timeline)
    assert "## Track Summary" in doc_text
    assert "## Caption CSV" in doc_text
    assert "Review Card: none" in doc_text
    assert "fixed phrase required: yes" not in doc_text.lower()


def test_neutral_timeline_artifacts_have_no_real_urls_or_forbidden_outputs() -> None:
    json_text = TIMELINE_PATH.read_text(encoding="utf-8")
    csv_text = CAPTION_CSV_PATH.read_text(encoding="utf-8")
    doc_text = TIMELINE_DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(json_text) is None
    assert _real_url_pattern().search(csv_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(TIMELINE_PATH.parent.glob("neutral_timeline_import_proof*.ymmp"))
    assert not list(TIMELINE_PATH.parent.glob("neutral_timeline_import_proof*.mp4"))
    assert not list(TIMELINE_PATH.parent.glob("neutral_timeline_import_proof*.wav"))
    assert not list(TIMELINE_PATH.parent.glob("neutral_timeline_import_proof*.mp3"))
    assert not list(CAPTION_CSV_PATH.parent.glob("caption_import_candidate*.ymmp"))
    assert not list(CAPTION_CSV_PATH.parent.glob("caption_import_candidate*.mp4"))
    assert not list(CAPTION_CSV_PATH.parent.glob("caption_import_candidate*.wav"))
    assert not list(CAPTION_CSV_PATH.parent.glob("caption_import_candidate*.mp3"))
