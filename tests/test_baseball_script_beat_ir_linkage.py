from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_DIR = REPO_ROOT / "samples" / "_probe" / "baseball" / "pipeline"
DATA_CAPSULE = PIPELINE_DIR / "baseball_data_capsule_p05.json"
DATA_CAPSULE_READBACK = PIPELINE_DIR / "baseball_data_capsule_p05_readback.json"
SCRIPT_IR = PIPELINE_DIR / "baseball_script_beat_ir_p05.json"
SCRIPT_SCHEMA = PIPELINE_DIR / "baseball_script_beat_ir_p05_schema.json"
SCRIPT_READBACK = PIPELINE_DIR / "baseball_script_beat_ir_p05_readback.json"
SCRIPT_MANIFEST = PIPELINE_DIR / "baseball_script_beat_ir_p05_manifest.json"
PIPELINE_MANIFEST = PIPELINE_DIR / "baseball_pipeline_contract_manifest.json"

BEAT_ID_RE = re.compile(r"^beat_[a-z0-9_]+$")
CLAIM_ID_RE = re.compile(r"^claim_[a-z0-9_]+$")
FORBIDDEN_VISUAL_DECISIONS = {"layout_slot", "layer", "keyframe", "render"}
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


def _data_ref_ids(data: dict) -> set[str]:
    return set(data["data_ref_index"])


def _all_claims(script: dict) -> list[dict]:
    claims: list[dict] = []
    for beat in script["beats"]:
        claims.extend(beat["supported_claims"])
    return claims


def test_script_linkage_artifacts_exist_and_parse() -> None:
    for path in (DATA_CAPSULE, DATA_CAPSULE_READBACK, SCRIPT_IR, SCRIPT_SCHEMA, SCRIPT_READBACK, SCRIPT_MANIFEST, PIPELINE_MANIFEST):
        assert path.exists(), path
        _load(path)


def test_script_ir_identity_and_boundaries() -> None:
    script = _load(SCRIPT_IR)

    assert script["schema_version"] == "baseball_script_beat_ir.v1"
    assert script["fixture_version"] == "BN-08"
    assert script["artifact_kind"] == "ScriptBeatIR"
    assert script["artifact_id"] == "baseball_script_beat_ir_p05"
    assert script["script_owner"] == "ScriptBeatIR"
    assert script["source_data_capsule"] == "samples/_probe/baseball/pipeline/baseball_data_capsule_p05.json"
    assert script["linkage_policy"]["data_ref_source"] == "BaseballDataCapsule.data_ref_index"

    boundaries = script["boundaries"]
    for key in (
        "must_reference_data_refs",
        "must_not_invent_facts",
        "not_visual_scene_plan",
        "not_visual_layout_authority",
        "not_yymm4_transport",
        "not_yymm4_motion_transport",
        "not_render_proof",
        "not_production_ready",
        "not_creative_final_acceptance",
        "not_publish_gate",
        "not_real_source",
        "not_official_material",
        "not_player_image_source",
        "not_ai_generated_player_image",
        "not_clip_export",
        "not_video_generation",
        "not_tts",
        "not_thumbnail_work",
        "not_mainline_integration",
    ):
        assert boundaries[key] is True


def test_narrative_angle_links_to_data_capsule_highlight() -> None:
    data = _load(DATA_CAPSULE)
    script = _load(SCRIPT_IR)
    fact_ids = _data_ref_ids(data)
    highlight_ids = {highlight["highlight_id"] for highlight in data["highlight_candidates"]}
    angle = script["narrative_angle"]

    assert angle["angle_id"] == "angle_velocity_pitch_type_shift"
    assert angle["source_highlight_id"] in highlight_ids
    assert set(angle["data_refs"]).issubset(fact_ids)
    assert {
        "fact_pitch_04_velocity",
        "fact_pitch_05_velocity",
        "fact_velocity_delta",
        "fact_pitch_type_change",
        "fact_highlight_p04_p05_sequence",
    }.issubset(angle["data_refs"])


def test_beats_have_stable_ids_orders_and_index_entries() -> None:
    script = _load(SCRIPT_IR)
    beats = script["beats"]
    beat_ids = [beat["beat_id"] for beat in beats]

    assert len(beat_ids) == len(set(beat_ids)) == 4
    assert all(BEAT_ID_RE.match(beat_id) for beat_id in beat_ids)
    assert [beat["order"] for beat in beats] == [1, 2, 3, 4]
    assert set(script["beat_ref_index"]) == set(beat_ids)

    for beat in beats:
        entry = script["beat_ref_index"][beat["beat_id"]]
        assert entry["order"] == beat["order"]
        assert entry["data_refs"] == beat["data_refs"]
        assert entry["visual_intent_id"] == beat["visual_intent"]["intent_id"]


def test_beat_and_claim_data_refs_resolve_to_data_capsule() -> None:
    data = _load(DATA_CAPSULE)
    script = _load(SCRIPT_IR)
    fact_ids = _data_ref_ids(data)

    for beat in script["beats"]:
        beat_refs = set(beat["data_refs"])
        assert beat_refs, beat["beat_id"]
        assert beat_refs.issubset(fact_ids), beat["beat_id"]
        for claim in beat["supported_claims"]:
            assert CLAIM_ID_RE.match(claim["claim_id"]), claim
            claim_refs = set(claim["data_refs"])
            assert claim_refs, claim["claim_id"]
            assert claim_refs.issubset(beat_refs), claim["claim_id"]
            assert claim_refs.issubset(fact_ids), claim["claim_id"]


def test_fact_like_claims_are_backed_by_specific_data_refs() -> None:
    script = _load(SCRIPT_IR)
    required_ref_by_phrase = {
        "155": "fact_pitch_04_velocity",
        "140": "fact_pitch_05_velocity",
        "3-4": "fact_score_state",
        "B2-S2": "fact_count_state",
        "four-seam": "fact_pitch_04_type",
        "fastball": "fact_pitch_04_type",
        "slider": "fact_pitch_05_type",
        "strike": "fact_pitch_05_result",
        "low outer": "fact_pitch_05_zone",
        "low-outer": "fact_pitch_05_zone",
        "No runners": "fact_runners_empty",
    }

    for beat in script["beats"]:
        for claim in beat["supported_claims"]:
            text = claim["claim_text"]
            refs = set(claim["data_refs"])
            for phrase, required_ref in required_ref_by_phrase.items():
                if phrase.lower() in text.lower():
                    assert required_ref in refs, (claim["claim_id"], phrase, required_ref)


def test_timing_hints_prepare_bn09_without_final_layout() -> None:
    script = _load(SCRIPT_IR)
    total_duration = 0

    for beat in script["beats"]:
        timing = beat["timing_hint"]
        assert timing["relative_order"] == beat["order"]
        assert isinstance(timing["suggested_duration_frames"], int)
        assert timing["suggested_duration_frames"] > 0
        total_duration += timing["suggested_duration_frames"]

    assert total_duration == 1320


def test_visual_intent_exposes_focus_without_visual_authority() -> None:
    script = _load(SCRIPT_IR)

    for beat in script["beats"]:
        intent = beat["visual_intent"]
        assert intent["intent_id"].startswith("intent_")
        assert intent["role"]
        assert intent["preferred_focus"]
        assert set(intent["must_not_decide"]) == FORBIDDEN_VISUAL_DECISIONS

    text = SCRIPT_IR.read_text(encoding="utf-8")
    assert '"layout_slot":' not in text
    assert '"layer":' not in text
    assert '"keyframe":' not in text
    assert '"render_output": true' not in text


def test_script_manifest_and_readback_record_validation_scope() -> None:
    script = _load(SCRIPT_IR)
    data = _load(DATA_CAPSULE)
    data_readback = _load(DATA_CAPSULE_READBACK)
    readback = _load(SCRIPT_READBACK)
    manifest = _load(SCRIPT_MANIFEST)
    pipeline_manifest = _load(PIPELINE_MANIFEST)

    assert data_readback["status"] == "passed"
    assert manifest["schema_version"] == "baseball_script_beat_ir_manifest.v1"
    assert manifest["slice"] == "BN-08"
    assert manifest["status"] == "script_linkage_validated"
    for value in manifest["artifacts"].values():
        assert (REPO_ROOT / value).exists(), value

    assert readback["schema_version"] == "baseball_script_beat_ir_readback.v1"
    assert readback["status"] == "passed"
    assert readback["source_script_beat_ir"] == script["repo_relative_path"]
    assert readback["source_data_capsule"] == data["repo_relative_path"]
    assert readback["failed_checks"] == []
    assert all(readback["checks"].values())
    assert readback["metrics"]["beat_count"] == len(script["beats"])
    assert readback["metrics"]["supported_claim_count"] == len(_all_claims(script))
    assert readback["metrics"]["unique_data_ref_count"] == len({ref for beat in script["beats"] for ref in beat["data_refs"]})
    assert readback["metrics"]["data_capsule_fact_count"] == len(data["data_ref_index"])

    assert pipeline_manifest["artifacts"]["script_beat_ir_schema"] == script["schema_path"]
    assert pipeline_manifest["artifacts"]["script_beat_ir_readback"] == script["readback_path"]
    assert pipeline_manifest["artifacts"]["script_beat_ir_manifest"] == script["manifest_path"]


def test_schema_names_required_script_linkage_fields() -> None:
    schema = _load(SCRIPT_SCHEMA)

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    required = set(schema["required"])
    for field in (
        "schema_version",
        "fixture_version",
        "artifact_id",
        "artifact_kind",
        "repo_relative_path",
        "schema_path",
        "readback_path",
        "manifest_path",
        "source_data_capsule",
        "script_owner",
        "linkage_policy",
        "narrative_angle",
        "beats",
        "beat_ref_index",
        "readiness",
        "boundaries",
    ):
        assert field in required


def test_new_script_artifacts_do_not_make_forbidden_completion_claims() -> None:
    for path in (SCRIPT_IR, SCRIPT_SCHEMA, SCRIPT_READBACK, SCRIPT_MANIFEST, PIPELINE_MANIFEST):
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
            assert forbidden not in text, (path, forbidden)
