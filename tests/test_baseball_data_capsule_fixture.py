from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_DIR = REPO_ROOT / "samples" / "_probe" / "baseball" / "pipeline"
DATA_CAPSULE = PIPELINE_DIR / "baseball_data_capsule_p05.json"
SCHEMA = PIPELINE_DIR / "baseball_data_capsule_p05_schema.json"
READBACK = PIPELINE_DIR / "baseball_data_capsule_p05_readback.json"
FIXTURE_MANIFEST = PIPELINE_DIR / "baseball_data_capsule_p05_fixture_manifest.json"
PIPELINE_MANIFEST = PIPELINE_DIR / "baseball_pipeline_contract_manifest.json"
SCRIPT_IR = PIPELINE_DIR / "baseball_script_beat_ir_p05.json"
SCENE_PLAN = PIPELINE_DIR / "baseball_visual_scene_plan_p05.json"

FACT_ID_RE = re.compile(r"^fact_[a-z0-9_]+$")
FORBIDDEN_COMPLETION_CLAIMS = (
    '"render_completion": true',
    '"production_ready": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"clip_export": true',
    '"video_generation": true',
    '"tts": true',
    '"thumbnail_work": true',
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _fact_ids(data: dict) -> set[str]:
    return {fact["fact_id"] for fact in data["derived_facts"]}


def test_data_capsule_fixture_artifacts_exist_and_parse() -> None:
    for path in (DATA_CAPSULE, SCHEMA, READBACK, FIXTURE_MANIFEST, PIPELINE_MANIFEST, SCRIPT_IR, SCENE_PLAN):
        assert path.exists(), path
        _load(path)


def test_data_capsule_required_identity_and_boundaries() -> None:
    data = _load(DATA_CAPSULE)

    assert data["schema_version"] == "baseball_data_capsule.v1"
    assert data["fixture_version"] == "BN-07"
    assert data["artifact_kind"] == "BaseballDataCapsule"
    assert data["artifact_id"] == "baseball_data_capsule_p05"
    assert data["event_id"] == "baseball_pitch_event_p05"
    assert data["current_pitch_id"] == "pitch_05"
    assert data["game_state"]["state_id"] == "game_state_p05_before_pitch"
    assert data["game_state"]["count"]["state_id"] == "count_p05_before_pitch"
    assert data["game_state"]["score"]["state_id"] == "score_p05_before_pitch"
    assert data["game_state"]["runners"]["state_id"] == "runners_p05_before_pitch"

    provenance = data["source_provenance"]
    assert provenance["source_type"] == "synthetic_fixture"
    assert provenance["not_real_source"] is True
    assert provenance["not_official_material"] is True
    assert provenance["not_player_image_source"] is True
    assert provenance["not_ai_generated_player_image"] is True

    boundaries = data["boundaries"]
    for key in (
        "sample_only",
        "synthetic_fixture",
        "not_real_source",
        "not_official_material",
        "not_player_image_source",
        "not_ai_generated_player_image",
        "not_clip_export",
        "not_video_generation",
        "not_tts",
        "not_thumbnail_work",
        "not_render_proof",
        "not_production_ready",
        "not_creative_final_acceptance",
        "not_publish_gate",
        "not_mainline_integration",
    ):
        assert boundaries[key] is True


def test_data_ref_index_matches_derived_facts_and_stable_policy() -> None:
    data = _load(DATA_CAPSULE)
    fact_ids = _fact_ids(data)
    index_ids = set(data["data_ref_index"])

    assert fact_ids == index_ids
    assert len(fact_ids) == len(data["derived_facts"]) == 16
    assert data["data_ref_policy"]["id_prefix"] == "fact_"
    assert "ScriptBeatIR" in data["data_ref_policy"]["stable_for_consumers"]
    assert "VisualScenePlan" in data["data_ref_policy"]["stable_for_consumers"]

    for fact_id in fact_ids:
        assert FACT_ID_RE.match(fact_id), fact_id
        entry = data["data_ref_index"][fact_id]
        assert entry["kind"]
        assert entry["source_path"].startswith("derived_facts.")
        assert set(entry["stable_for"]) == {"ScriptBeatIR", "VisualScenePlan"}


def test_pitch_sequence_and_current_pitch_delta_are_consistent() -> None:
    data = _load(DATA_CAPSULE)
    fact_ids = _fact_ids(data)
    pitches = data["pitch_sequence"]
    pitch_by_id = {pitch["pitch_id"]: pitch for pitch in pitches}

    assert len(pitch_by_id) == len(pitches) == 2
    assert [pitch["pitch_number"] for pitch in pitches] == [4, 5]
    assert data["current_pitch_id"] in pitch_by_id

    for pitch in pitches:
        assert set(pitch["data_refs"]).issubset(fact_ids), pitch["pitch_id"]

    current = pitch_by_id[data["current_pitch_id"]]
    delta = current["delta_from_previous"]
    previous = pitch_by_id[delta["previous_pitch_id"]]
    assert delta["velocity_delta_kmh"] == current["velocity_kmh"] - previous["velocity_kmh"]
    assert delta["pitch_type_changed"] is True
    assert previous["pitch_type"] == "FF"
    assert current["pitch_type"] == "SL"

    velocity_delta_fact = next(fact for fact in data["derived_facts"] if fact["fact_id"] == "fact_velocity_delta")
    assert velocity_delta_fact["from_pitch_id"] == previous["pitch_id"]
    assert velocity_delta_fact["to_pitch_id"] == current["pitch_id"]
    assert velocity_delta_fact["value_kmh"] == delta["velocity_delta_kmh"]


def test_highlight_candidates_are_fact_backed() -> None:
    data = _load(DATA_CAPSULE)
    fact_ids = _fact_ids(data)
    highlights = data["highlight_candidates"]

    assert len(highlights) == 1
    highlight = highlights[0]
    assert highlight["highlight_id"] == "highlight_velocity_pitch_type_shift"
    assert highlight["script_safe"] is True
    assert highlight["visual_safe"] is True
    assert set(highlight["data_refs"]).issubset(fact_ids)
    assert {
        "fact_pitch_04_velocity",
        "fact_pitch_05_velocity",
        "fact_velocity_delta",
        "fact_pitch_type_change",
    }.issubset(highlight["data_refs"])


def test_script_and_visual_consumers_have_no_dangling_data_refs() -> None:
    data = _load(DATA_CAPSULE)
    script = _load(SCRIPT_IR)
    scene_plan = _load(SCENE_PLAN)
    fact_ids = _fact_ids(data)

    assert script["source_data_capsule"] == data["repo_relative_path"]
    for beat in script["beats"]:
        assert set(beat["data_refs"]).issubset(fact_ids), beat["beat_id"]

    assert scene_plan["source_data_capsule"] == data["repo_relative_path"]
    for slot in scene_plan["semantic_slots"]:
        assert set(slot["data_refs"]).issubset(fact_ids), slot["slot_id"]


def test_fixture_manifest_and_readback_record_validation_scope() -> None:
    data = _load(DATA_CAPSULE)
    manifest = _load(FIXTURE_MANIFEST)
    readback = _load(READBACK)
    pipeline_manifest = _load(PIPELINE_MANIFEST)

    assert manifest["schema_version"] == "baseball_data_capsule_fixture_manifest.v1"
    assert manifest["slice"] == "BN-07"
    assert manifest["status"] == "fixture_validated"
    for value in manifest["artifacts"].values():
        assert (REPO_ROOT / value).exists(), value

    assert readback["schema_version"] == "baseball_data_capsule_readback.v1"
    assert readback["status"] == "passed"
    assert readback["source_data_capsule"] == data["repo_relative_path"]
    assert readback["failed_checks"] == []
    assert all(readback["checks"].values())
    assert readback["metrics"]["pitch_count"] == len(data["pitch_sequence"])
    assert readback["metrics"]["derived_fact_count"] == len(data["derived_facts"])
    assert readback["metrics"]["data_ref_count"] == len(data["data_ref_index"])
    assert readback["metrics"]["highlight_candidate_count"] == len(data["highlight_candidates"])

    assert pipeline_manifest["artifacts"]["data_capsule_schema"] == data["schema_path"]
    assert pipeline_manifest["artifacts"]["data_capsule_readback"] == data["fixture_validation"]["readback_path"]
    assert pipeline_manifest["artifacts"]["data_capsule_fixture_manifest"] == data["fixture_validation"]["manifest_path"]


def test_schema_names_required_contract_fields() -> None:
    schema = _load(SCHEMA)

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    required = set(schema["required"])
    for field in (
        "schema_version",
        "fixture_version",
        "artifact_id",
        "artifact_kind",
        "repo_relative_path",
        "source_provenance",
        "data_ref_policy",
        "game_state",
        "participants",
        "pitch_sequence",
        "derived_facts",
        "data_ref_index",
        "highlight_candidates",
        "fixture_validation",
        "boundaries",
    ):
        assert field in required


def test_new_fixture_artifacts_do_not_make_forbidden_completion_claims() -> None:
    for path in (DATA_CAPSULE, SCHEMA, READBACK, FIXTURE_MANIFEST, PIPELINE_MANIFEST):
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
            assert forbidden not in text, (path, forbidden)
