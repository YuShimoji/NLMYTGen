from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

from src.pipeline.episode_002_integration_metadata import (
    INTERNAL_REVIEW_MANIFEST_RELATIVE,
    PACKAGE_RELATIVE,
    PILOT_RELATIVE,
    RUNTIME_STATE_RELATIVE,
    SOURCE_MANIFEST_RELATIVE,
    rebind_episode_002_integration_metadata,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / PACKAGE_RELATIVE
SOURCE_PILOT = REPO_ROOT / PILOT_RELATIVE


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _copy_source(repo: Path, relative: Path) -> None:
    destination = repo / PACKAGE_RELATIVE / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_PACKAGE / relative, destination)


def test_integration_metadata_rebind_is_bounded_and_idempotent(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    runtime = repo / RUNTIME_STATE_RELATIVE
    runtime.parent.mkdir(parents=True)
    shutil.copy2(REPO_ROOT / RUNTIME_STATE_RELATIVE, runtime)
    runtime_text = runtime.read_text(encoding="utf-8")
    test_state = {
        "Project-State-ID": "episode-002-integration-metadata-test-v1",
        "Product-State": "episode-002-integration-metadata-test",
        "Product-Gate": "verified-test-input-selection",
        "Recommended-Next": "select-test-input",
        "External-State": "local-test-worktree",
    }
    for field, value in test_state.items():
        runtime_text = re.sub(
            rf"(?m)^{re.escape(field)}:\s*\S+\s*$",
            f"{field}: {value}",
            runtime_text,
        )
    runtime.write_text(runtime_text, encoding="utf-8", newline="\n")

    pilot = repo / PILOT_RELATIVE
    shutil.copytree(
        SOURCE_PILOT,
        pilot,
        ignore=shutil.ignore_patterns("local_outputs", "__pycache__"),
    )
    for relative in (
        Path("ymm4_csv_gate_observation_receipt_2026-07-11.json"),
        Path("ymm4_diagnostic_placeholder_proof/diagnostic_project_manifest.json"),
        Path("ymm4_diagnostic_placeholder_proof/diagnostic_project_readback.json"),
        Path("ymm4_diagnostic_placeholder_proof/diagnostic_project_receipt.json"),
        Path(
            "ymm4_character_alias_profiles/"
            "ymm4_4_53_0_9_yukkuri_characters_v1.json"
        ),
    ):
        _copy_source(repo, relative)

    invariant_paths = (
        "canonical_script.txt",
        "canonical_script.json",
        "source_claim_ledger.json",
        "canonical_yymm4.csv",
        "derived_yymm4_import.csv",
        "render_receipt.json",
        "render_validation_readback.json",
    )
    before_invariants = {name: _sha256(pilot / name) for name in invariant_paths}

    first = rebind_episode_002_integration_metadata(repo)
    second = rebind_episode_002_integration_metadata(repo)

    expected_closure = {
        SOURCE_MANIFEST_RELATIVE.as_posix(),
        (PILOT_RELATIVE / "input_validation_readback.json").as_posix(),
        INTERNAL_REVIEW_MANIFEST_RELATIVE.as_posix(),
    }
    assert first["status"] == "passed"
    assert set(first["changed_files"]) == expected_closure
    assert second["changed_files"] == []
    assert first["local_outputs_read"] is False
    assert first["media_regenerated"] is False
    assert not (pilot / "local_outputs").exists()
    assert before_invariants == {
        name: _sha256(pilot / name) for name in invariant_paths
    }

    source_manifest = json.loads(
        (repo / SOURCE_MANIFEST_RELATIVE).read_text(encoding="utf-8")
    )
    runtime_source = next(
        item
        for item in source_manifest["sources"]
        if item["source_id"] == "runtime_state"
    )
    assert runtime_source["sha256"] == _sha256(runtime)
    assert runtime_source["status"] == test_state["Project-State-ID"]

    review_manifest = json.loads(
        (repo / INTERNAL_REVIEW_MANIFEST_RELATIVE).read_text(encoding="utf-8")
    )
    source_key = SOURCE_MANIFEST_RELATIVE.as_posix()
    assert review_manifest["source_evidence_sha256"][source_key] == _sha256(
        repo / SOURCE_MANIFEST_RELATIVE
    )
    assert review_manifest["achieved_state"] == test_state


def test_default_branch_integration_receipt_is_sanitized_and_hash_bound() -> None:
    receipt_path = (
        REPO_ROOT
        / "docs/verification/episode_002_default_branch_integration_receipt.json"
    )
    receipt_text = receipt_path.read_text(encoding="utf-8")
    receipt = json.loads(receipt_text)

    assert receipt["status"] == "passed"
    assert receipt["refs"]["pre_integration_origin_master"] == (
        "b61722454e3e218547fe6220bf1f4aa3802ed4d8"
    )
    assert receipt["refs"]["audited_subject_head"] == (
        "d8e959c54b8c8f28c31cc2b586bbdd8c79f69f97"
    )
    assert receipt["refs"]["audit_head"] == (
        "a8b81e43616281691b73520a045dfa6ff44d2054"
    )
    assert receipt["refs"]["integration_commit_sha"] is None
    assert receipt["refs"]["integration_commit_resolution"] == (
        "final Git ref and AGENT_REPORT"
    )
    assert receipt["failed_checks"] == []

    for rebound in receipt["metadata_rebind"]["files"]:
        assert _sha256(REPO_ROOT / rebound["repo_relative_path"]) == rebound[
            "after_sha256"
        ]

    immutable_paths = {
        "canonical_script_text_sha256": PILOT_RELATIVE / "canonical_script.txt",
        "canonical_script_json_sha256": PILOT_RELATIVE / "canonical_script.json",
        "source_claim_ledger_sha256": PILOT_RELATIVE / "source_claim_ledger.json",
        "canonical_csv_sha256": PILOT_RELATIVE / "canonical_yymm4.csv",
        "derived_csv_sha256": PILOT_RELATIVE / "derived_yymm4_import.csv",
        "tracked_render_receipt_sha256": PILOT_RELATIVE / "render_receipt.json",
        "tracked_render_readback_sha256": (
            PILOT_RELATIVE / "render_validation_readback.json"
        ),
        "audit_markdown_sha256": Path(
            "docs/verification/EPISODE_002_MILESTONE_INTEGRATION_AUDIT_2026-07-12.md"
        ),
        "audit_json_sha256": Path(
            "docs/verification/episode_002_milestone_integration_audit.json"
        ),
        "audit_path_inventory_sha256": Path(
            "docs/verification/episode_002_integration_path_inventory.json"
        ),
    }
    for field, path in immutable_paths.items():
        assert _sha256(REPO_ROOT / path) == receipt["immutable_evidence"][field]

    render_receipt = json.loads(
        (REPO_ROOT / PILOT_RELATIVE / "render_receipt.json").read_text(
            encoding="utf-8"
        )
    )
    immutable = receipt["immutable_evidence"]
    assert render_receipt["operator_result"]["sha256"] == immutable[
        "operator_result_sha256"
    ]
    assert render_receipt["project"]["sha256"] == immutable["project_sha256"]
    assert render_receipt["original_render"]["sha256"] == immutable[
        "original_render_sha256"
    ]
    assert render_receipt["review_proxy"]["sha256"] == immutable[
        "review_proxy_sha256"
    ]

    assert re.search(r"[A-Za-z]:[\\/]Users[\\/]", receipt_text) is None
    assert "file://" not in receipt_text.lower()
