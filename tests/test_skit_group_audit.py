import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.pipeline.skit_group_audit import audit_skit_group


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _make_registry(*, intent_fallbacks=None, include_exact=True, second_group=False):
    templates = {}
    if include_exact:
        templates["delivery_enter_from_left_v1"] = {
            "group_key": "haitatsuin_delivery_v1",
            "intent": "enter_from_left",
            "template_name": "delivery_enter_from_left_v1",
            "target_type": "skit_group",
            "manual_checks": ["landing position"],
        }
    templates["delivery_surprise_oneshot_v1"] = {
        "group_key": "haitatsuin_delivery_v1",
        "intent": "surprise_oneshot",
        "template_name": "delivery_surprise_oneshot_v1",
        "target_type": "skit_group",
        "manual_checks": ["Y-axis only jump height"],
    }
    if second_group:
        templates["other_surprise_v1"] = {
            "group_key": "other_group_v1",
            "intent": "surprise_oneshot",
            "template_name": "other_surprise_v1",
            "target_type": "skit_group",
            "manual_checks": ["other"],
        }
    return {
        "canonical_groups": {
            "haitatsuin_delivery_v1": {
                "group_remark": "haitatsuin_delivery_main",
                "manual_checks": ["head/body alignment", "group center position"],
            },
            **(
                {
                    "other_group_v1": {
                        "group_remark": "other_group_main",
                        "manual_checks": ["other group check"],
                    }
                }
                if second_group
                else {}
            ),
        },
        "templates": templates,
        "intent_fallbacks": intent_fallbacks or {},
    }


def _make_ymmp(*, remarks):
    items = []
    for idx, (remark, layer) in enumerate(remarks):
        items.append(
            {
                "$type": "YukkuriMovieMaker.Project.Items.GroupItem, YukkuriMovieMaker",
                "Remark": remark,
                "Layer": layer,
                "Frame": idx * 100,
                "Length": 100,
            }
        )
    items.append(
        {
            "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
            "CharacterName": "marisa",
            "Serif": "test",
            "Frame": 0,
            "Length": 100,
            "Layer": 1,
            "Group": 0,
            "TachieFaceParameter": {
                "$type": "YukkuriMovieMaker.Plugin.Tachie.AnimationTachie.FaceParameter, YukkuriMovieMaker.Plugin.Tachie.AnimationTachie",
                "Eyebrow": "default.png",
                "Eye": "default.png",
                "Mouth": "default.png",
                "Hair": "",
                "Body": "",
                "Complexion": "",
            },
        }
    )
    return {
        "SelectedTimelineIndex": 0,
        "Timelines": [{"Items": items, "LayerSettings": []}],
        "Characters": [{"Name": "marisa"}],
    }


def _make_ir(*, motion, motion_target="layer:9"):
    return {
        "ir_version": "1.0",
        "video_id": "test",
        "macro": {"sections": [{"section_id": "S1", "start_index": 1, "end_index": 1}]},
        "utterances": [
            {
                "index": 1,
                "speaker": "marisa",
                "text": "test",
                "section_id": "S1",
                "face": "smile",
                "motion": motion,
                "motion_target": motion_target,
            }
        ],
    }


def test_audit_skit_group_exact_resolution():
    result = audit_skit_group(
        _make_ymmp(remarks=[("haitatsuin_delivery_main", 9)]),
        _make_ir(motion="enter_from_left"),
        _make_registry(),
    )

    assert result.status == "ok"
    assert result.group_key == "haitatsuin_delivery_v1"
    assert result.anchor_layer == 9
    assert result.summary == {"exact": 1, "fallback": 0, "manual_note": 0}
    assert result.entries[0].resolution == "exact"
    assert result.entries[0].template_name == "delivery_enter_from_left_v1"


def test_audit_skit_group_fallback_resolution():
    result = audit_skit_group(
        _make_ymmp(remarks=[("haitatsuin_delivery_main", 9)]),
        _make_ir(motion="collapse_then_runaway"),
        _make_registry(intent_fallbacks={"collapse_then_runaway": "delivery_surprise_oneshot_v1"}),
    )

    assert result.status == "ok"
    assert result.summary == {"exact": 0, "fallback": 1, "manual_note": 0}
    assert result.entries[0].resolution == "fallback"
    assert result.entries[0].template_name == "delivery_surprise_oneshot_v1"


def test_audit_skit_group_manual_note_resolution():
    result = audit_skit_group(
        _make_ymmp(remarks=[("haitatsuin_delivery_main", 9)]),
        _make_ir(motion="look_aside"),
        _make_registry(),
    )

    assert result.status == "ok"
    assert result.summary == {"exact": 0, "fallback": 0, "manual_note": 1}
    assert result.entries[0].resolution == "manual_note"
    assert result.entries[0].note == "intent not registered"
    assert result.entries[0].manual_checks == ["head/body alignment", "group center position"]


def test_audit_skit_group_anchor_missing_is_error():
    result = audit_skit_group(
        _make_ymmp(remarks=[("motion:enter_from_left utt:1", 9)]),
        _make_ir(motion="enter_from_left"),
        _make_registry(),
    )

    assert result.status == "error"
    assert any(err.startswith("SKIT_CANONICAL_GROUP_MISSING:") for err in result.errors)


def test_audit_skit_group_anchor_ambiguous_is_error():
    result = audit_skit_group(
        _make_ymmp(remarks=[("haitatsuin_delivery_main", 9), ("other_group_main", 11)]),
        _make_ir(motion="enter_from_left"),
        _make_registry(second_group=True),
    )

    assert result.status == "error"
    assert any(err.startswith("SKIT_CANONICAL_GROUP_AMBIGUOUS:") for err in result.errors)


def test_audit_skit_group_fallback_missing_template_is_error():
    result = audit_skit_group(
        _make_ymmp(remarks=[("haitatsuin_delivery_main", 9)]),
        _make_ir(motion="collapse_then_runaway"),
        _make_registry(intent_fallbacks={"collapse_then_runaway": "missing_template"}),
    )

    assert result.status == "error"
    assert any(err.startswith("SKIT_TEMPLATE_FALLBACK_MISS:") for err in result.errors)


def test_audit_skit_group_fallback_group_mismatch_is_error():
    result = audit_skit_group(
        _make_ymmp(remarks=[("haitatsuin_delivery_main", 9)]),
        _make_ir(motion="collapse_then_runaway"),
        _make_registry(
            intent_fallbacks={"collapse_then_runaway": "other_surprise_v1"},
            second_group=True,
        ),
    )

    assert result.status == "error"
    assert any(err.startswith("SKIT_TEMPLATE_GROUP_MISMATCH:") for err in result.errors)


@pytest.mark.integration
def test_cli_audit_skit_group_json(tmp_path):
    ymmp_path = tmp_path / "production.ymmp"
    ir_path = tmp_path / "ir.json"
    registry_path = tmp_path / "registry.json"
    ymmp_path.write_text(json.dumps(_make_ymmp(remarks=[("haitatsuin_delivery_main", 9)])), encoding="utf-8-sig")
    ir_path.write_text(json.dumps(_make_ir(motion="enter_from_left")), encoding="utf-8")
    registry_path.write_text(json.dumps(_make_registry()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli.main",
            "audit-skit-group",
            str(ymmp_path),
            str(ir_path),
            "--skit-group-registry",
            str(registry_path),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["anchor_layer"] == 9
    assert payload["summary"]["exact"] == 1
    assert payload["entries"][0]["resolution"] == "exact"


@pytest.mark.integration
def test_cli_apply_production_with_skit_group_registry_success(tmp_path):
    prod_path = tmp_path / "production.ymmp"
    ir_path = tmp_path / "ir.json"
    face_map_path = tmp_path / "face_map.json"
    registry_path = tmp_path / "registry.json"

    prod_path.write_text(
        json.dumps(_make_ymmp(remarks=[("haitatsuin_delivery_main", 9)])),
        encoding="utf-8-sig",
    )
    ir_path.write_text(json.dumps(_make_ir(motion="enter_from_left")), encoding="utf-8")
    face_map_path.write_text(
        json.dumps(
            {
                "marisa": {
                    "smile": {
                        "Eyebrow": "smile_eb.png",
                        "Eye": "smile_ey.png",
                        "Mouth": "smile_mo.png",
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    registry_path.write_text(json.dumps(_make_registry()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli.main",
            "apply-production",
            str(prod_path),
            str(ir_path),
            "--face-map",
            str(face_map_path),
            "--tachie-motion-map",
            "samples/tachie_motion_map_library.json",
            "--skit-group-registry",
            str(registry_path),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, result.stderr
    assert "--- Skit Group Preflight ---" in result.stdout
    assert "enter_from_left -> exact" in result.stdout


@pytest.mark.integration
def test_cli_apply_production_with_skit_group_registry_anchor_missing_fails(tmp_path):
    prod_path = tmp_path / "production.ymmp"
    ir_path = tmp_path / "ir.json"
    face_map_path = tmp_path / "face_map.json"
    registry_path = tmp_path / "registry.json"

    prod_path.write_text(
        json.dumps(_make_ymmp(remarks=[("motion:enter_from_left utt:1", 9)])),
        encoding="utf-8-sig",
    )
    ir_path.write_text(json.dumps(_make_ir(motion="enter_from_left")), encoding="utf-8")
    face_map_path.write_text(
        json.dumps(
            {
                "marisa": {
                    "smile": {
                        "Eyebrow": "smile_eb.png",
                        "Eye": "smile_ey.png",
                        "Mouth": "smile_mo.png",
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    registry_path.write_text(json.dumps(_make_registry()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli.main",
            "apply-production",
            str(prod_path),
            str(ir_path),
            "--face-map",
            str(face_map_path),
            "--tachie-motion-map",
            "samples/tachie_motion_map_library.json",
            "--skit-group-registry",
            str(registry_path),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 1
    assert "SKIT_CANONICAL_GROUP_MISSING" in result.stdout
    assert "Skit group preflight FAILED" in result.stderr


@pytest.mark.integration
def test_cli_audit_skit_group_current_skit01_corpus_reports_anchor_missing():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli.main",
            "audit-skit-group",
            "samples/characterAnimSample/haitatsuin_2026-04-12.ymmp",
            "samples/_probe/skit_01/skit_01_ir.json",
            "--skit-group-registry",
            "samples/registry_template/skit_group_registry.template.json",
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["status"] == "error"
    assert any(err.startswith("SKIT_CANONICAL_GROUP_MISSING:") for err in payload["errors"])
