import json
import re
from pathlib import Path

from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
)
from src.pipeline.newsroom_yym4_native_audio_path_proof import (
    AUDIO_OBSERVATION_SLICE,
    DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_DOC_PATH,
    DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH,
    FIELD_AUDIT_SLICE,
    NEXT_RECOMMENDED_SLICE,
    RECOMMENDED_DEFAULT,
    YYM4_NATIVE_AUDIO_PATH_PROOF_ID,
    YYM4_NATIVE_AUDIO_PATH_PROOF_SCHEMA_VERSION,
    build_default_newsroom_yym4_native_audio_path_proof,
    render_newsroom_yym4_native_audio_path_proof_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = ROOT / DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_PATH
DOC_PATH = ROOT / DEFAULT_YYM4_NATIVE_AUDIO_PATH_PROOF_DOC_PATH


def _proof() -> dict:
    return json.loads(PROOF_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_yym4_native_audio_path_proof_matches_builder_output() -> None:
    proof = _proof()

    assert proof == build_default_newsroom_yym4_native_audio_path_proof(root=ROOT)
    assert proof["artifact_id"] == YYM4_NATIVE_AUDIO_PATH_PROOF_ID
    assert proof["proof_id"] == YYM4_NATIVE_AUDIO_PATH_PROOF_ID
    assert proof["schema_version"] == YYM4_NATIVE_AUDIO_PATH_PROOF_SCHEMA_VERSION
    assert proof["review_status"] == "ready_for_supervisor_review"
    assert proof["diagnostic_only"] is True
    assert proof["production_status"] == "diagnostic_only"
    assert proof["proof_status"] == "passed_with_unknowns"


def test_source_validation_reuses_boundary_render_and_structure_readbacks() -> None:
    proof = _proof()
    validation = proof["source_validation"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["canonical_speaker_value"] == CANONICAL_UI_OBSERVED_SPEAKER
    assert validation["canonical_speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )
    assert validation["voice_audio_related_fields_present"] == [
        "VoiceLength",
        "VoiceCache",
        "VoiceParameter",
        "Pronounce",
        "Hatsuon",
        "AudioEffects",
    ]
    assert validation["voice_cache_item_count"] == 4
    assert validation["native_voice_engine_hint"] == "AquesTalk"


def test_known_render_state_reuses_tiny_smoke_without_audio_acceptance() -> None:
    proof = _proof()
    render_state = proof["known_render_state"]

    assert render_state == {
        "tiny_render_smoke_result": "pass",
        "output_video_observed": True,
        "approximate_duration_sec": 8,
        "four_dialogue_lines_visible": True,
        "timing_mode": "YMM4 natural duration",
        "neutral_68_sec_timing_patch_applied": False,
    }


def test_native_audio_evidence_accepts_field_sufficiency_only() -> None:
    proof = _proof()
    evidence = proof["native_audio_evidence_from_ymmp"]

    assert evidence["voice_fields_present"] is True
    assert evidence["voice_cache_present"] is True
    assert evidence["voice_length_fields_present"] is True
    assert evidence["pronounce_or_hatsuon_fields_present"] is True
    assert evidence["native_voice_engine_hint"] == "AquesTalk"
    assert evidence["voice_item_count"] == 4
    assert evidence["voice_cache_item_count"] == 4
    assert evidence["speaker_binding_status"] == (
        f"{CANONICAL_UI_OBSERVED_SPEAKER} accepted for diagnostic import"
    )
    assert evidence["speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )
    assert evidence["native_audio_path_candidate"] is True


def test_audio_unknowns_remain_unknown_despite_native_path_candidate() -> None:
    proof = _proof()
    knowns = proof["audio_tts_knowns_and_unknowns"]

    assert knowns["audio_presence_in_render"] == "unknown"
    assert knowns["audio_quality_accepted"] is False
    assert knowns["TTS_ready"] is False
    assert knowns["TTS_generated_by_agent"] is False
    assert knowns["explicit_operator_TTS_generation"] is False
    assert knowns["external_TTS_introduced"] is False
    assert knowns["native_audio_path_candidate"] is True
    assert knowns["confidence"] == "medium"
    assert "Audible presence and voice quality remain unknown" in (
        knowns["confidence_reason"][-1]
    )


def test_responsibility_split_keeps_external_tts_closed() -> None:
    proof = _proof()
    split = {row["path_id"]: row for row in proof["responsibility_split"]}

    assert list(split) == [
        "YMM4_native_voice_audio_path",
        "external_TTS_path",
        "metadata_only_voice_profile_path",
        "no_audio_diagnostic_path",
    ]
    assert split["YMM4_native_voice_audio_path"]["role"] == (
        "recommended_diagnostic_default"
    )
    assert NEXT_RECOMMENDED_SLICE in split["YMM4_native_voice_audio_path"][
        "what_it_enables"
    ]
    assert split["external_TTS_path"]["role"] == "closed_for_now"
    assert "adds credential, retention, and timing boundaries too early" in split[
        "external_TTS_path"
    ]["risks"]


def test_recommended_default_and_next_path_do_not_jump_to_production() -> None:
    proof = _proof()
    recommended = proof["recommended_default"]
    next_path = proof["next_path"]

    assert recommended["choice"] == RECOMMENDED_DEFAULT
    assert "keep external TTS closed for this lane" in recommended["do_now"]
    assert "audio quality acceptance" in recommended["defer"]
    assert "TTS readiness" in recommended["defer"]
    assert next_path == {
        "recommended_next_slice": NEXT_RECOMMENDED_SLICE,
        "reason": (
            "Native YMM4 voice fields are sufficient to keep the native path "
            "as the diagnostic default; the remaining unknown is audible "
            "presence/quality, not field sufficiency."
        ),
        "if_audio_presence_becomes_the_next_bottleneck": AUDIO_OBSERVATION_SLICE,
        "if_native_fields_drift_or_are_later_missing": FIELD_AUDIT_SLICE,
        "do_not_recommend": "production_render_immediately",
    }


def test_boundaries_and_human_burden_hygiene_keep_manual_work_closed() -> None:
    proof = _proof()

    assert proof["boundaries"] == {
        "YMM4_launched_by_agent": False,
        "render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "ymmp_created_or_modified_by_agent": False,
        "ymmp_or_media_staged_or_committed": False,
        "production_approval": False,
        "public_video_ready": False,
        "render_output_retention_required_now": False,
        "dashboard_governance_freshness_changed": False,
    }
    assert proof["human_burden_hygiene"] == {
        "user_input": "freeform",
        "template_required": False,
        "schema_owner": "Agent",
        "user_side_work_this_slice": "none",
        "operator_observation_card": "not_needed_this_slice",
        "future_observation_max_required_points": 3,
        "screenshot_optional": True,
        "negative_confirmations_required_from_user": False,
        "fixed_form_result_template": False,
    }
    assert proof["review_memory"]["repeated_general_review_allowed"] is False
    assert proof["review_memory"]["user_side_work_re_requested"] is False


def test_not_accepted_scope_and_timing_interaction_preserve_deferred_claims() -> None:
    proof = _proof()

    assert proof["not_accepted_scope"] == {
        "production_render_readiness": False,
        "public_video_readiness": False,
        "neutral_68_sec_timing_proof": False,
        "timing_patch_readiness": False,
        "visual_layout_readiness": False,
        "TTS_audio_quality_acceptance": False,
        "TTS_readiness": False,
        "real_content_readiness": False,
        "external_TTS_adoption": False,
        "production_approval": False,
    }
    assert proof["timing_interaction"] == {
        "first_render_smoke_used_natural_duration": True,
        "first_smoke_duration_sec": 8,
        "prior_ymmp_natural_duration_sec": round(509 / 60, 6),
        "neutral_68_sec_timing_patch_applied": False,
        "neutral_68_sec_timing_patch_remains_deferred_until_next_slice": True,
        "audio_quality_or_presence_not_required_for_this_proof": True,
    }


def test_doc_matches_renderer_and_has_no_fixed_form_relapse() -> None:
    proof = _proof()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_yym4_native_audio_path_proof_markdown(proof)
    assert "proof_status: passed_with_unknowns" in doc_text
    assert "audio_presence_in_render: unknown" in doc_text
    assert f"choice: {RECOMMENDED_DEFAULT}" in doc_text
    assert f"recommended_next_slice: {NEXT_RECOMMENDED_SLICE}" in doc_text
    assert "operator_observation_card: not_needed_this_slice" in doc_text
    assert "result: pass / fail" not in doc_text
    assert "yes/no/unclear" not in doc_text.lower()


def test_yym4_native_audio_path_artifacts_have_no_real_urls_or_outputs() -> None:
    proof_text = PROOF_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(proof_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(PROOF_PATH.parent.glob("*native_audio_path_proof*.ymmp"))
    assert not list(PROOF_PATH.parent.glob("*native_audio_path_proof*.mp4"))
    assert not list(PROOF_PATH.parent.glob("*native_audio_path_proof*.wav"))
    assert not list(PROOF_PATH.parent.glob("*native_audio_path_proof*.mp3"))
    assert not list(PROOF_PATH.parent.glob("*native_audio_path_proof*.m4a"))
