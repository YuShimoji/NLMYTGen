import json
import subprocess
import sys
from pathlib import Path

from src.pipeline.capability_atlas import build_default_capability_atlas
from src.pipeline.skit_group_audit import audit_skit_group, load_skit_group_registry
from src.pipeline.ymmp_patch import load_ir, load_ymmp


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _entry_map(atlas: dict) -> dict[str, dict]:
    return {entry["expression_id"]: entry for entry in atlas["entries"]}


def test_capability_atlas_classifies_speaker_tachie_motion_as_direct_proven():
    atlas = build_default_capability_atlas(_project_root())
    entries = _entry_map(atlas)

    assert entries["speaker_tachie.motion"]["support_level"] == "direct_proven"


def test_capability_atlas_classifies_canonical_anchor_as_direct_proven():
    atlas = build_default_capability_atlas(_project_root())
    entries = _entry_map(atlas)

    assert entries["skit_group.canonical_anchor"]["support_level"] == "direct_proven"


def test_capability_atlas_classifies_exported_starter_intent_as_direct_proven():
    atlas = build_default_capability_atlas(_project_root())
    entries = _entry_map(atlas)

    assert entries["skit_group.intent.enter_from_left"]["support_level"] == "direct_proven"


def test_capability_atlas_keeps_non_exported_skit_group_intent_as_template_catalog_only():
    atlas = build_default_capability_atlas(_project_root())
    entries = _entry_map(atlas)

    assert entries["skit_group.intent.deny_oneshot"]["support_level"] == "template_catalog_only"


def test_capability_atlas_classifies_non_fade_transition_as_unsupported():
    atlas = build_default_capability_atlas(_project_root())
    entries = _entry_map(atlas)

    assert entries["transition.non_fade"]["support_level"] == "unsupported"


def test_capability_atlas_classifies_raw_effect_entry_as_probe_only():
    atlas = build_default_capability_atlas(_project_root())
    entries = _entry_map(atlas)

    assert entries["effect_atom.JumpEffect"]["support_level"] == "probe_only"


def test_build_capability_atlas_script_writes_expected_json(tmp_path):
    output_path = tmp_path / "capability_atlas.json"
    result = subprocess.run(
        [sys.executable, "scripts/build_capability_atlas.py", "-o", str(output_path)],
        cwd=_project_root(),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    entries = _entry_map(data)
    assert entries["speaker_tachie.motion"]["support_level"] == "direct_proven"
    assert entries["skit_group.canonical_anchor"]["support_level"] == "direct_proven"
    assert entries["skit_group.intent.enter_from_left"]["support_level"] == "direct_proven"
    assert entries["skit_group.intent.deny_oneshot"]["support_level"] == "template_catalog_only"


def test_capability_atlas_evidence_paths_exist_in_repo():
    atlas = build_default_capability_atlas(_project_root())
    root = _project_root()

    for entry in atlas["entries"]:
        for evidence in entry["evidence"]:
            path = root / evidence["path"]
            assert path.exists(), f"missing evidence path for {entry['expression_id']}: {evidence['path']}"


def test_canonical_anchor_corpus_is_ok_and_exact_only():
    root = _project_root()
    atlas = build_default_capability_atlas(root)
    entries = _entry_map(atlas)

    ymmp_data = load_ymmp(str(root / "samples/canonical.ymmp"))
    ir_data = load_ir(str(root / "samples/_probe/skit_01/skit_01_ir.json"))
    registry = load_skit_group_registry(root / "samples/registry_template/skit_group_registry.template.json")
    audit = audit_skit_group(ymmp_data, ir_data, registry)

    assert entries["skit_group.canonical_anchor"]["support_level"] == "direct_proven"
    assert entries["skit_group.intent.enter_from_left"]["support_level"] == "direct_proven"
    assert entries["skit_group.intent.deny_oneshot"]["support_level"] == "template_catalog_only"
    assert audit.status == "ok"
    assert audit.summary == {"exact": 5, "fallback": 0, "manual_note": 0}


def test_old_skit01_still_fails_preflight_even_after_starter_export():
    root = _project_root()
    atlas = build_default_capability_atlas(root)
    entries = _entry_map(atlas)

    ymmp_data = load_ymmp(str(root / "samples/characterAnimSample/haitatsuin_2026-04-12.ymmp"))
    ir_data = load_ir(str(root / "samples/_probe/skit_01/skit_01_ir.json"))
    registry = load_skit_group_registry(root / "samples/registry_template/skit_group_registry.template.json")
    audit = audit_skit_group(ymmp_data, ir_data, registry)

    assert entries["skit_group.intent.enter_from_left"]["support_level"] == "direct_proven"
    assert audit.status == "error"
    assert any(err.startswith("SKIT_CANONICAL_GROUP_MISSING:") for err in audit.errors)
