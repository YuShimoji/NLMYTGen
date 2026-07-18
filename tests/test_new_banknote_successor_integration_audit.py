from __future__ import annotations

import importlib.util
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "audit_new_banknote_successor_branches.py"


def _module():
    spec = importlib.util.spec_from_file_location("successor_audit", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_audit_is_complete_deterministic_and_sanitized(tmp_path: Path) -> None:
    module = _module()
    first = module.build_artifacts(REPO_ROOT)
    second = module.build_artifacts(REPO_ROOT)
    assert first == second
    module._privacy_check(first)

    result = module.write_artifacts(REPO_ROOT, tmp_path)
    assert result["status"] == "passed"
    assert result["recommendation_class"] == "selective_integration_ready"

    audit = json.loads(
        (tmp_path / "new_banknote_successor_integration_audit.json").read_text(
            encoding="utf-8"
        )
    )
    commits = json.loads(
        (tmp_path / "new_banknote_successor_commit_inventory.json").read_text(
            encoding="utf-8"
        )
    )
    paths = json.loads(
        (tmp_path / "new_banknote_successor_path_inventory.json").read_text(
            encoding="utf-8"
        )
    )
    matrix = json.loads(
        (
            tmp_path
            / "new_banknote_successor_authority_conflict_matrix.json"
        ).read_text(encoding="utf-8")
    )

    assert commits["primary_only_commit_count"] == 7
    assert commits["candidate_only_commit_count"] == 13
    assert commits["audited_commit_count"] == 20
    assert commits["unclassified_commit_count"] == 0
    assert paths["primary_path_entry_count"] == 33
    assert paths["candidate_path_entry_count"] == 51
    assert paths["audited_side_path_entry_count"] == 84
    assert paths["union_path_count"] == 77
    assert paths["overlap_path_count"] == 7
    assert paths["unclassified_path_count"] == 0
    assert audit["approved_content_identity"]["primary_all_eight_match"] is True
    assert audit["approved_content_identity"]["candidate_exact_match_count"] == 7
    assert audit["approved_content_identity"]["candidate_drift_count"] == 1
    assert audit["visual_result"]["recommendation_status"] == "recommended_not_selected"
    assert audit["visual_result"]["selected_route"] is None
    assert audit["visual_result"]["implementation_authorized"] is False
    assert audit["blockers"] == []
    assert matrix["one_to_one_authority_roles"] is True
    assert matrix["unresolved_authority_count"] == 0

    for path in audit["integration_contract"]["accepted_candidate_paths"]:
        module._blob(REPO_ROOT, module.CANDIDATE_REF, path)
    for path in audit["integration_contract"]["historical_candidate_paths"]:
        module._blob(REPO_ROOT, module.CANDIDATE_REF, path)

    readme = (
        tmp_path / "NEW_BANKNOTE_SUCCESSOR_BRANCH_INTEGRATION_AUDIT.md"
    ).read_text(encoding="utf-8")
    assert "selective_integration_ready" in readme
    assert "visual route selected: `false`" in readme
    assert "No source branch was merged" in readme
