import json
import subprocess
import sys
from pathlib import Path

from src.pipeline.skit_group_audit import load_skit_group_registry
from src.pipeline.skit_group_placement import (
    FAIL_SOURCE_MISSING,
    apply_skit_group_placement,
    extract_skit_group_templates,
    validate_template_source_against_registry,
)
from src.pipeline.ir_validate import validate_ir
from src.pipeline.ymmp_patch import load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _registry(*, include_nod=False):
    templates = {
        "delivery_enter_from_left_v1": {
            "group_key": "haitatsuin_delivery_v1",
            "intent": "enter_from_left",
            "template_name": "delivery_enter_from_left_v1",
            "target_type": "skit_group",
        },
    }
    if include_nod:
        templates["delivery_nod_v1"] = {
            "group_key": "haitatsuin_delivery_v1",
            "intent": "nod",
            "template_name": "delivery_nod_v1",
            "target_type": "skit_group",
        }
    return {
        "canonical_groups": {
            "haitatsuin_delivery_v1": {
                "group_remark": "haitatsuin_delivery_main",
                "manual_checks": ["alignment"],
            },
        },
        "templates": templates,
        "intent_fallbacks": {
            "walk_in": "delivery_enter_from_left_v1",
        },
    }


def _group_item(*, frame=10, layer=9, length=20, remark="delivery_enter_from_left_v1"):
    return {
        "$type": "YukkuriMovieMaker.Project.Items.GroupItem, YukkuriMovieMaker",
        "Remark": remark,
        "Frame": frame,
        "Layer": layer,
        "Length": length,
        "Group": 0,
        "GroupRange": 2,
    }


def _image_item(*, frame=10, layer=10, length=20, remark=""):
    return {
        "$type": "YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker",
        "Remark": remark,
        "Frame": frame,
        "Layer": layer,
        "Length": length,
        "Group": 0,
    }


def _voice_item(*, frame, length=50):
    return {
        "$type": "YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker",
        "CharacterName": "marisa",
        "Serif": "test",
        "Frame": frame,
        "Layer": 0,
        "Length": length,
        "Group": 0,
    }


def _ymmp(items):
    return {
        "SelectedTimelineIndex": 0,
        "Timelines": [{"Items": items, "LayerSettings": []}],
        "Characters": [{"Name": "marisa"}],
    }


def _ir(*, index=2, motion="enter_from_left"):
    return {
        "ir_version": "1.0",
        "video_id": "test",
        "macro": {"sections": [{"section_id": "S1", "start_index": 1, "end_index": 2}]},
        "utterances": [
            {
                "index": 1,
                "speaker": "marisa",
                "text": "first",
                "section_id": "S1",
                "face": "smile",
                "motion": "none",
            },
            {
                "index": index,
                "speaker": "marisa",
                "text": "target",
                "section_id": "S1",
                "face": "smile",
                "motion": motion,
                "motion_target": "layer:9",
            },
        ],
    }


def _template_source():
    return _ymmp([
        _image_item(layer=10),
        _image_item(layer=11),
        _group_item(),
    ])


def _write_json(path: Path, data: dict, *, sig: bool = False) -> None:
    encoding = "utf-8-sig" if sig else "utf-8"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding=encoding)


def _run_cli(args: list[str]):
    return subprocess.run(
        [sys.executable, "-m", "src.cli.main", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _placement_group_remarks(ymmp_data: dict) -> list[str]:
    return [
        item.get("Remark", "")
        for item in ymmp_data["Timelines"][0]["Items"]
        if item.get("$type", "").split(",")[0].endswith("GroupItem")
        and str(item.get("Remark", "")).startswith("skit_group:")
    ]


def test_extract_skit_group_templates_collects_group_children():
    templates = extract_skit_group_templates(_template_source())

    clip = templates["delivery_enter_from_left_v1"]
    assert clip.base_frame == 10
    assert clip.base_layer == 9
    assert len(clip.items) == 3


def test_apply_skit_group_placement_inserts_template_at_voice_frame():
    target = _ymmp([_voice_item(frame=0), _voice_item(frame=100)])

    result = apply_skit_group_placement(
        target,
        _ir(),
        _registry(),
        _template_source(),
    )

    assert result.placements == 1
    assert result.group_item_insertions == 1
    items = target["Timelines"][0]["Items"]
    groups = [
        item for item in items
        if item["$type"].split(",")[0].endswith("GroupItem")
    ]
    assert groups[0]["Frame"] == 100
    assert groups[0]["Layer"] == 9
    assert groups[0]["Remark"] == "skit_group:delivery_enter_from_left_v1 utt:2"
    children = [
        item for item in items
        if item["$type"].split(",")[0].endswith("ImageItem")
    ]
    assert sorted((item["Frame"], item["Layer"]) for item in children) == [
        (100, 10),
        (100, 11),
    ]


def test_apply_skit_group_placement_uses_registered_fallback():
    target = _ymmp([_voice_item(frame=0), _voice_item(frame=100)])

    result = apply_skit_group_placement(
        target,
        _ir(motion="walk_in"),
        _registry(),
        _template_source(),
    )

    assert result.placements == 1
    assert result.group_item_insertions == 1


def test_validate_template_source_reports_missing_registry_template():
    warnings = validate_template_source_against_registry(
        _registry(include_nod=True),
        _template_source(),
    )

    assert any(w.startswith(f"{FAIL_SOURCE_MISSING}:") for w in warnings)


def test_repo_tracked_template_source_covers_registry_templates():
    registry = load_skit_group_registry(
        ROOT / "samples/registry_template/skit_group_registry.template.json"
    )
    template_source = load_ymmp(
        ROOT / "samples/templates/skit_group/delivery_v1_templates.ymmp"
    )

    templates = extract_skit_group_templates(template_source)
    assert sorted(templates) == sorted(registry["templates"])
    assert validate_template_source_against_registry(registry, template_source) == []
    assert len(templates["delivery_nod_v1"].items) == 3
    assert len(templates["delivery_deny_oneshot_v1"].items) == 7
    for clip in templates.values():
        for item in clip.items:
            if item.get("$type", "").split(",")[0].endswith("ImageItem"):
                assert Path(item["FilePath"]).exists()


def test_validate_ir_strict_skit_group_rejects_unknown_layer_motion():
    result = validate_ir(
        _ir(motion="panic_shake"),
        known_skit_group_motion_labels={"enter_from_left", "walk_in"},
        strict_skit_group_intents=True,
    )

    assert any(err.startswith("SKIT_GROUP_UNKNOWN_INTENT:") for err in result.errors)


def test_validate_ir_non_strict_skit_group_keeps_manual_note_compatibility():
    result = validate_ir(
        _ir(motion="panic_shake"),
        known_skit_group_motion_labels={"enter_from_left", "walk_in"},
        strict_skit_group_intents=False,
    )

    assert not any(err.startswith("MOTION_UNKNOWN_LABEL:") for err in result.errors)
    assert not any(err.startswith("SKIT_GROUP_UNKNOWN_INTENT:") for err in result.errors)


def test_cli_patch_ymmp_skit_group_only_ignores_unresolved_face_bg(tmp_path):
    target_path = tmp_path / "target.ymmp"
    ir_path = tmp_path / "ir.json"
    registry_path = tmp_path / "registry.json"
    template_path = tmp_path / "templates.ymmp"
    output_path = tmp_path / "patched.ymmp"

    ir_data = _ir()
    ir_data["macro"]["sections"][0]["default_bg"] = "missing_bg"
    _write_json(target_path, _ymmp([_voice_item(frame=0), _voice_item(frame=100)]), sig=True)
    _write_json(ir_path, ir_data)
    _write_json(registry_path, _registry())
    _write_json(template_path, _template_source(), sig=True)

    result = _run_cli([
        "patch-ymmp",
        str(target_path),
        str(ir_path),
        "--skit-group-registry",
        str(registry_path),
        "--skit-group-template-source",
        str(template_path),
        "--skit-group-only",
        "-o",
        str(output_path),
    ])

    assert result.returncode == 0, result.stderr
    assert "Skit group placements: 1 (GroupItems inserted: 1)" in result.stdout
    patched = load_ymmp(output_path)
    assert _placement_group_remarks(patched) == [
        "skit_group:delivery_enter_from_left_v1 utt:2",
    ]


def test_cli_patch_ymmp_skit_group_only_missing_template_is_fatal(tmp_path):
    target_path = tmp_path / "target.ymmp"
    ir_path = tmp_path / "ir.json"
    registry_path = tmp_path / "registry.json"
    template_path = tmp_path / "templates.ymmp"

    _write_json(target_path, _ymmp([_voice_item(frame=0), _voice_item(frame=100)]), sig=True)
    _write_json(ir_path, _ir(motion="nod"))
    _write_json(registry_path, _registry(include_nod=True))
    _write_json(template_path, _template_source(), sig=True)

    result = _run_cli([
        "patch-ymmp",
        str(target_path),
        str(ir_path),
        "--skit-group-registry",
        str(registry_path),
        "--skit-group-template-source",
        str(template_path),
        "--skit-group-only",
        "--dry-run",
    ])

    assert result.returncode == 1
    assert "SKIT_TEMPLATE_SOURCE_MISSING" in result.stderr
    assert "Partial output was not accepted" in result.stderr


def test_cli_patch_ymmp_skit_group_only_missing_voice_timing_is_fatal(tmp_path):
    target_path = tmp_path / "target.ymmp"
    ir_path = tmp_path / "ir.json"
    registry_path = tmp_path / "registry.json"
    template_path = tmp_path / "templates.ymmp"

    _write_json(target_path, _ymmp([_voice_item(frame=0)]), sig=True)
    _write_json(ir_path, _ir(index=2))
    _write_json(registry_path, _registry())
    _write_json(template_path, _template_source(), sig=True)

    result = _run_cli([
        "patch-ymmp",
        str(target_path),
        str(ir_path),
        "--skit-group-registry",
        str(registry_path),
        "--skit-group-template-source",
        str(template_path),
        "--skit-group-only",
        "--dry-run",
    ])

    assert result.returncode == 1
    assert "SKIT_PLACEMENT_NO_VOICE_TIMING" in result.stderr


def test_cli_apply_production_skit_group_only_writes_without_face_maps(tmp_path):
    target_path = tmp_path / "target.ymmp"
    ir_path = tmp_path / "ir.json"
    registry_path = tmp_path / "registry.json"
    template_path = tmp_path / "templates.ymmp"
    output_path = tmp_path / "patched.ymmp"

    _write_json(target_path, _ymmp([_voice_item(frame=0), _voice_item(frame=100)]), sig=True)
    _write_json(ir_path, _ir())
    _write_json(registry_path, _registry())
    _write_json(template_path, _template_source(), sig=True)

    result = _run_cli([
        "apply-production",
        str(target_path),
        str(ir_path),
        "--skit-group-registry",
        str(registry_path),
        "--skit-group-template-source",
        str(template_path),
        "--skit-group-only",
        "-o",
        str(output_path),
        "--format",
        "json",
    ])

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["success"] is True
    assert payload["skit_group_placements"] == 1
    assert output_path.exists()


def test_cli_patch_ymmp_skit_group_only_real_estate_ir_readback(tmp_path):
    target_path = tmp_path / "real_estate_dx_csv_import_base.ymmp"
    output_path = tmp_path / "real_estate_dx_skit_group_patched.ymmp"
    voices = [
        _voice_item(frame=(idx - 1) * 90, length=45)
        for idx in range(1, 144)
    ]
    _write_json(target_path, _ymmp(voices), sig=True)

    result = _run_cli([
        "patch-ymmp",
        str(target_path),
        str(ROOT / "samples/不動産DX_魔法の鍵とキュレーション_skit_group_ir.json"),
        "--skit-group-registry",
        str(ROOT / "samples/registry_template/skit_group_registry.template.json"),
        "--skit-group-template-source",
        str(ROOT / "samples/templates/skit_group/delivery_v1_templates.ymmp"),
        "--skit-group-only",
        "-o",
        str(output_path),
    ])

    assert result.returncode == 0, result.stderr
    assert "Skit group placements: 5 (GroupItems inserted: 9)" in result.stdout
    patched = load_ymmp(output_path)
    remarks = set(_placement_group_remarks(patched))
    assert {
        "skit_group:delivery_enter_from_left_v1 utt:1",
        "skit_group:delivery_nod_v1 utt:15",
        "skit_group:delivery_surprise_oneshot_v1 utt:35",
        "skit_group:delivery_deny_oneshot_v1 utt:39",
        "skit_group:delivery_exit_left_v1 utt:143",
    }.issubset(remarks)
    assert not any("utt:104" in remark for remark in remarks)
    layers = [
        item.get("Layer")
        for item in patched["Timelines"][0]["Items"]
        if item.get("$type", "").split(",")[0].endswith("GroupItem")
        and str(item.get("Remark", "")).startswith("skit_group:")
    ]
    assert layers and set(layers) == {9}
    image_items = [
        item
        for item in patched["Timelines"][0]["Items"]
        if item.get("$type", "").split(",")[0].endswith("ImageItem")
    ]
    assert len(image_items) == 10
    assert all(Path(item["FilePath"]).exists() for item in image_items)
