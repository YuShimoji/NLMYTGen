from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANARY = (
    ROOT
    / "production_pilots"
    / "factory_canaries"
    / "real_estate_reins_transparency_001"
)
NEW_BANKNOTE_PIPELINE = (
    ROOT
    / "production_pilots"
    / "yukkuri_newsroom_content_spine_002"
    / "external_editorial_input"
    / "new_banknote_security_notebooklm_001"
    / "auto_video_pipeline"
)


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_second_real_topic_canonical_script_and_source_edges_are_closed() -> None:
    script = _json(CANARY / "canonical_script.json")
    registry = _json(CANARY / "source_claim_registry.json")
    edges = _json(CANARY / "source_support_edges.json")

    assert script["title"] == "REINSと不動産情報流通の仕組み"
    assert script["cue_count"] == len(script["cues"]) == 7
    assert script["scene_count"] == len({cue["scene_id"] for cue in script["cues"]}) == 4
    assert script["speaker_distribution"] == {"れいむ": 4, "まりさ": 3}
    assert script["speaker_distribution"] not in ({"れいむ": 3, "まりさ": 6}, {"れいむ": 6, "まりさ": 3})
    assert script["unsupported_spoken_factual_units"] == 0
    assert script["human_creative_acceptance"] is False

    assert len(registry["sources"]) == 4
    assert all(source["primary_source"] is True for source in registry["sources"])
    assert all(source["canonical_url"].startswith("https://") for source in registry["sources"])
    assert {
        Path(row["path"]).as_posix() for row in registry["raw_discovery_inputs"]
    } == {
        "samples/不動産DX_魔法の鍵とキュレーション.txt",
        "samples/_probe/g24/real_estate_dx_review_packet.json",
    }
    assert registry["claims"]
    assert all(claim["status"] == "supported" and claim["support"] for claim in registry["claims"])

    edge_rows = edges["edges"]
    assert [row["cue_id"] for row in edge_rows] == [
        cue["cue_id"] for cue in script["cues"]
    ]
    assert all(
        row["claim_ids"] and row["source_ids"]
        for row in edge_rows
        if row["spoken_factual_unit"]
    )
    assert edges["checks"] == {
        "cue_order_exact": True,
        "every_spoken_factual_unit_supported": True,
        "unsupported_spoken_factual_units": 0,
        "primary_source_surface_count": 4,
    }


def test_second_real_topic_serializations_and_content_locks_match() -> None:
    script = _json(CANARY / "canonical_script.json")
    manifest = _json(
        CANARY / "auto_video_pipeline" / "real_estate_reins_episode_manifest.json"
    )

    expected_by_file = {
        "canonical_yymm4.csv": [
            (cue["speaker"], cue["text"]) for cue in script["cues"]
        ],
        "derived_yymm4_import.csv": [
            (cue["speaker"], script_cue["text"])
            for cue, script_cue in zip(
                manifest["cue_mapping"], script["cues"], strict=True
            )
        ],
    }
    for filename, expected in expected_by_file.items():
        with (CANARY / filename).open(encoding="utf-8-sig", newline="") as handle:
            assert [tuple(row) for row in csv.reader(handle)] == expected

    assert len(manifest["cue_mapping"]) == 7
    assert len({cue["scene_id"] for cue in manifest["cue_mapping"]}) == 4
    assert manifest["yymm4"]["timeline_frames"] == 2725
    assert 45 <= manifest["yymm4"]["timeline_frames"] / 60 <= 120
    assert manifest["output"]["run_id"] == "real_estate_reins_internal_review_v1"
    assert manifest["boundaries"]["internal_review_only"] is True
    assert manifest["boundaries"]["rights_approved"] is False
    assert manifest["boundaries"]["production"] is False
    assert manifest["boundaries"]["publication"] is False
    assert manifest["boundaries"]["external_upload"] is False

    for locked in manifest["content_locks"]:
        locked_path = ROOT / locked["path"]
        assert locked_path.is_file()
        assert _sha256(locked_path) == locked["sha256"]


def test_second_real_topic_real_media_contract_is_raster_and_internal_only() -> None:
    provenance = _json(
        CANARY
        / "auto_video_pipeline"
        / "real_estate_reins_media_provenance.json"
    )

    assets = provenance["assets"]
    assert len(assets) == 7
    assert len({asset["asset_id"] for asset in assets}) == 7
    assert len({asset["sha256"] for asset in assets}) == 7
    assert all(asset["media_type"] == "image" for asset in assets)
    assert all(asset["local_asset_path"].lower().endswith(".png") for asset in assets)
    assert all("auto_video_runs/" in asset["local_asset_path"] for asset in assets)
    assert all(asset["usage_classification"] == "internal_review_only" for asset in assets)
    assert all(asset["production_allowed"] is False for asset in assets)
    assert all(asset["publication_allowed"] is False for asset in assets)
    assert provenance["boundary"] == {
        "internal_review_only": True,
        "rights_approved": False,
        "production": False,
        "publication": False,
        "external_upload": False,
        "source_media_tracked": False,
    }

    tracked_text = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in CANARY.rglob("*")
        if path.is_file() and "auto_video_runs" not in path.parts
    )
    assert r"C:\Users\\" not in tracked_text
    assert "D:\\" not in tracked_text
    assert ".svg" not in tracked_text.lower()


def test_second_topic_varies_factory_shape_from_new_banknote() -> None:
    second = _json(
        CANARY / "auto_video_pipeline" / "real_estate_reins_episode_manifest.json"
    )
    first = _json(NEW_BANKNOTE_PIPELINE / "new_banknote_real_media_episode_manifest.json")

    assert len(second["cue_mapping"]) == 7
    assert len(first["cue_mapping"]) == 9
    assert len({row["scene_id"] for row in second["cue_mapping"]}) == 4
    assert len({row["scene_id"] for row in first["cue_mapping"]}) == 3
    assert second["yymm4"]["timeline_frames"] == 2725
    assert first["yymm4"]["timeline_frames"] == 4415
    assert second["yymm4"]["source_project_path"] != first["yymm4"]["source_project_path"]
    assert second["output"]["run_id"] != first["output"]["run_id"]
    assert second["episode_id"] != first["episode_id"]
