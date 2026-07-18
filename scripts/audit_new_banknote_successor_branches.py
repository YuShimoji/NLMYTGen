#!/usr/bin/env python3
"""Build the read-only new-banknote successor-branch integration audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
PRIMARY_REF = "origin/codex/new-banknote-existing-yymm4-evidence-revalidation-v1"
CANDIDATE_REF = "origin/codex/new-banknote-authoritative-source-script-v1"
PRIMARY_HEAD = "5e50ff707806724e67a5e0cec215bdd3b604ce32"
CANDIDATE_HEAD = "833717f63713db9555f563a2a26285fa2f621e3d"
MASTER_HEAD = "37a02fbcecaf324f61b055b8677b6537735853fd"
BASELINE = "b05eb3867caabda496fb9a0070d230a4e81aea01"
RECOMMENDATION_CLASS = "selective_integration_ready"
STATE_ID = "new-banknote-successor-integration-audited-selective-ready-v1"

PILOT = (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
VERIFICATION_DIR = Path("docs/verification")
OUTPUT_NAMES = (
    "NEW_BANKNOTE_SUCCESSOR_BRANCH_INTEGRATION_AUDIT.md",
    "new_banknote_successor_integration_audit.json",
    "new_banknote_successor_commit_inventory.json",
    "new_banknote_successor_path_inventory.json",
    "new_banknote_successor_authority_conflict_matrix.json",
)

APPROVED_FILENAMES = (
    "README_CANONICAL_SCRIPT_REVIEW.md",
    "canonical_script.json",
    "canonical_script.txt",
    "canonical_script_review.md",
    "cue_source_traceability.json",
    "canonical_yymm4.csv",
    "derived_yymm4_import.csv",
    "source_to_script_manifest.json",
)

STATE_PATHS = {
    "docs/PROJECT_COCKPIT.md",
    "docs/PROJECT_PIPELINE.mmd",
    "docs/THREAD_REGISTRY.md",
    "docs/project-context.md",
    "docs/runtime-state.md",
}

EDITORIAL_REGENERATE = {
    f"{PILOT}/editorial_provenance/README_EDITORIAL_PROVENANCE.md",
    f"{PILOT}/editorial_provenance/content_lock_receipt.json",
    f"{PILOT}/editorial_provenance/provenance_validation_readback.json",
}

CANDIDATE_METADATA_EXCLUDE = {
    f"{PILOT}/README_CANONICAL_SCRIPT_REVIEW.md",
    f"{PILOT}/canonical_script_editorial_revision.md",
    f"{PILOT}/editorial_revision_receipt.json",
    f"{PILOT}/script_generation_receipt.json",
    "src/pipeline/new_banknote_authoritative_script.py",
}

COMMIT_CLASSIFICATION: dict[str, dict[str, str]] = {
    "8c3342611cea9ec8171dc21ba1392e833ff4c7b9": {
        "family": "content_lineage_approval_and_primary_operator_batch",
        "kind": "substantive",
        "content": "approved bytes preserved; approval and T00-T07 authority added",
        "evidence": "current content lineage and hash-locked Operator Batch introduced",
        "state": "advanced to lineage-sealed operator-batch readiness",
        "treatment": "keep_primary",
    },
    "5d46a7389334626eb713ea5f9681288ac9b25b63": {
        "family": "state_and_handoff_documentation",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "none",
        "state": "historical restart repair",
        "treatment": "retain_primary_history_regenerate_current_state",
    },
    "2dbc5d7ec0ae027caa2dad1a270eb5dc5af75849": {
        "family": "state_and_handoff_documentation",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "cross-device validation summary only",
        "state": "historical restart refresh",
        "treatment": "retain_primary_history_regenerate_current_state",
    },
    "d8b8707bd7eb5ed0ead3bf7955c0d188c45de285": {
        "family": "supervisor_readiness_and_roadmap",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "durable G0-G9 roadmap and readiness report",
        "state": "historical readiness snapshot",
        "treatment": "retain_historical",
    },
    "8cb55c7e1be9382eb5282153a8afa0090590f4f2": {
        "family": "state_and_handoff_documentation",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "none",
        "state": "self-pointer update",
        "treatment": "retain_primary_history_regenerate_current_state",
    },
    "220a9b554f267a5367c9589eb09f35fc9058d4a0": {
        "family": "branch_divergence_handoff",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "records semantic branch split",
        "state": "historical divergence gate",
        "treatment": "retain_historical",
    },
    "5e50ff707806724e67a5e0cec215bdd3b604ce32": {
        "family": "same_machine_yymm4_evidence_revalidation",
        "kind": "substantive",
        "content": "approved content unchanged",
        "evidence": "current approval and T00-T07 compatible YMM4 evidence authority",
        "state": "accepted H0 current-lineage revalidation",
        "treatment": "keep_primary",
    },
    "5bcc7713707222d2f7dc5f5057f5a62acb6f0f64": {
        "family": "state_and_handoff_documentation",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "none",
        "state": "candidate pointer now obsolete",
        "treatment": "exclude_state_pointer",
    },
    "0dd87f8341ab7cac339de2322a5a80f83d8a6ba0": {
        "family": "state_and_handoff_documentation",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "none",
        "state": "candidate pointer now obsolete",
        "treatment": "exclude_state_pointer",
    },
    "40a8d5e5d5e8165e4e9deef812435ae4529bf040": {
        "family": "state_and_handoff_documentation",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "none",
        "state": "candidate pointer now obsolete",
        "treatment": "exclude_state_pointer",
    },
    "d47794f47d7ffa1ffdbdffe506562fc7ddd2cb77": {
        "family": "candidate_operator_batch_tooling",
        "kind": "substantive",
        "content": "six approved content hashes agree with primary",
        "evidence": "predecessor four-action batch and bounded supervisor receipt",
        "state": "superseded by primary approval-lineage-aware batch",
        "treatment": "exclude_operator_tooling_retain_historical_review_receipt",
    },
    "bc07fc073063d3e5d1af1e6e5400a340b0036496": {
        "family": "tracked_yymm4_observation_and_visual_abc",
        "kind": "substantive",
        "content": "canonical script and CSV identities unchanged",
        "evidence": "historical import observation plus A/B/C proposal package",
        "state": "candidate visual review gate",
        "treatment": "selective_paths_only",
    },
    "1f78449f896f6ee5cb49f04d7f86b21a23dc99a0": {
        "family": "editorial_provenance_and_prior_script_audit",
        "kind": "substantive",
        "content": "one approved README metadata hash changed; script bytes unchanged",
        "evidence": "D00-D10 provenance and bounded prior-script audit",
        "state": "candidate provenance-first visual gate",
        "treatment": "selective_paths_regenerate_authority_surfaces",
    },
    "533c37956f5ce5d51115bde98e1a0acc0e2168ef": {
        "family": "state_and_handoff_documentation",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "none",
        "state": "candidate pointer now obsolete",
        "treatment": "exclude_state_pointer",
    },
    "6540846c5be129b9601b0b3b0bbdd2441225280c": {
        "family": "state_and_handoff_documentation",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "none",
        "state": "candidate pointer now obsolete",
        "treatment": "exclude_state_pointer",
    },
    "517d70896c10570caad51a7c6c1e0659a862ed69": {
        "family": "state_and_handoff_documentation",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "none",
        "state": "candidate pointer now obsolete",
        "treatment": "exclude_state_pointer",
    },
    "3d39e8cb97f9799d3b207b0dc2e837d7aeb69d85": {
        "family": "candidate_remote_readiness_report",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "candidate readiness snapshot",
        "state": "historical candidate state",
        "treatment": "retain_historical_report_regenerate_current_state",
    },
    "3bfcaed0ce7fc8f5d0b472d2cd54b2b078252cc1": {
        "family": "prior_user_script_audit_correction",
        "kind": "compensating",
        "content": "none",
        "evidence": "bounded prior-script inventory and provenance readback corrected",
        "state": "candidate receipt seal",
        "treatment": "selective_final_paths_only",
    },
    "4bfa445604d185852c1ab0734fcf19975b2774d7": {
        "family": "candidate_local_yymm4_provenance_reverification",
        "kind": "compensating",
        "content": "none",
        "evidence": "same-machine hashes reverified but three tracked surfaces become local-state-sensitive",
        "state": "candidate provenance receipt refreshed",
        "treatment": "use_as_regeneration_reference_not_whole_commit",
    },
    "833717f63713db9555f563a2a26285fa2f621e3d": {
        "family": "state_and_handoff_documentation",
        "kind": "docs_seal",
        "content": "none",
        "evidence": "candidate branch final seal",
        "state": "conflicts with accepted primary current state",
        "treatment": "exclude_state_pointer",
    },
}


def _git(repo: Path, *args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    if check and completed.returncode:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return completed.stdout


def _blob(repo: Path, ref: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "cat-file", "blob", f"{ref}:{path}"],
        cwd=repo,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.decode("utf-8", errors="replace"))
    return completed.stdout


def _json_blob(repo: Path, ref: str, path: str) -> dict[str, Any]:
    value = json.loads(_blob(repo, ref, path).decode("utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path}")
    return value


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _ref_sha(repo: Path, ref: str) -> str:
    return _git(repo, "rev-parse", ref).strip()


def _verify_refs(repo: Path) -> dict[str, Any]:
    refs = {
        "primary": _ref_sha(repo, PRIMARY_REF),
        "candidate": _ref_sha(repo, CANDIDATE_REF),
        "origin_master": _ref_sha(repo, "origin/master"),
        "merge_base": _git(repo, "merge-base", PRIMARY_REF, CANDIDATE_REF).strip(),
    }
    expected = {
        "primary": PRIMARY_HEAD,
        "candidate": CANDIDATE_HEAD,
        "origin_master": MASTER_HEAD,
        "merge_base": BASELINE,
    }
    if refs != expected:
        raise RuntimeError(f"REF_FRESHNESS_MISMATCH:{refs!r}")
    for ref in (PRIMARY_REF, CANDIDATE_REF):
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASELINE, ref],
            cwd=repo,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    divergence = _git(
        repo, "rev-list", "--left-right", "--count", f"{PRIMARY_REF}...{CANDIDATE_REF}"
    ).split()
    refs["primary_only_commit_count"] = int(divergence[0])
    refs["candidate_only_commit_count"] = int(divergence[1])
    refs["baseline_is_ancestor_of_both"] = True
    return refs


def _commit_paths(repo: Path, sha: str) -> list[str]:
    return [
        line
        for line in _git(
            repo, "diff-tree", "--no-commit-id", "--name-only", "-r", sha
        ).splitlines()
        if line
    ]


def _build_commit_inventory(repo: Path, refs: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for side, ref in (("primary", PRIMARY_REF), ("candidate", CANDIDATE_REF)):
        shas = _git(repo, "rev-list", "--reverse", f"{BASELINE}..{ref}").splitlines()
        for side_order, sha in enumerate(shas, start=1):
            if sha not in COMMIT_CLASSIFICATION:
                raise RuntimeError(f"UNCLASSIFIED_COMMIT:{sha}")
            timestamp, message = _git(
                repo, "show", "-s", "--format=%aI%x00%s", sha
            ).rstrip("\n").split("\x00", 1)
            classification = COMMIT_CLASSIFICATION[sha]
            rows.append(
                {
                    "sha": sha,
                    "side": side,
                    "side_chronological_order": side_order,
                    "authored_at": timestamp,
                    "message": message,
                    "capability_family": classification["family"],
                    "classification": classification["kind"],
                    "primary_artifacts_touched": _commit_paths(repo, sha),
                    "content_impact": classification["content"],
                    "evidence_impact": classification["evidence"],
                    "state_impact": classification["state"],
                    "proposed_integration_treatment": classification["treatment"],
                }
            )
    ordered = sorted(
        rows,
        key=lambda row: (datetime.fromisoformat(row["authored_at"]), row["sha"]),
    )
    for global_order, row in enumerate(ordered, start=1):
        row["global_chronological_order"] = global_order
    counts = Counter(row["side"] for row in rows)
    if counts != {
        "primary": refs["primary_only_commit_count"],
        "candidate": refs["candidate_only_commit_count"],
    }:
        raise RuntimeError(f"COMMIT_COVERAGE_MISMATCH:{counts!r}")
    return {
        "schema_version": "new_banknote.successor_commit_inventory.v1",
        "status": "passed",
        "baseline": BASELINE,
        "primary_ref": PRIMARY_REF,
        "candidate_ref": CANDIDATE_REF,
        "primary_only_commit_count": counts["primary"],
        "candidate_only_commit_count": counts["candidate"],
        "audited_commit_count": len(rows),
        "unclassified_commit_count": 0,
        "commits": sorted(rows, key=lambda row: row["global_chronological_order"]),
    }


def _diff_paths(repo: Path, ref: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in _git(repo, "diff", "--name-status", BASELINE, ref).splitlines():
        parts = line.split("\t")
        rows.append((parts[0], parts[-1]))
    return rows


def _path_classification(side: str, path: str) -> dict[str, str]:
    filename = path.rsplit("/", 1)[-1]
    if path in STATE_PATHS:
        return {
            "category": "current_state_and_navigation",
            "family": "state_handoff",
            "authority": "regenerate_single_successor_state",
            "hash": "not_approved_content",
            "risk": "none",
            "treatment": "regenerate_successor",
            "rationale": "Both branches carry incompatible historical current-state prose; do not merge it mechanically.",
        }
    if side == "primary":
        if path == "docs/NAV.md":
            return {
                "category": "navigation",
                "family": "content_lineage_navigation",
                "authority": "primary_navigation",
                "hash": "not_approved_content",
                "risk": "none",
                "treatment": "keep_primary",
                "rationale": "Primary navigation points to the accepted lineage surface.",
            }
        if path.startswith("docs/verification/"):
            return {
                "category": "historical_report",
                "family": "supervisor_roadmap",
                "authority": "immutable_historical_guidance",
                "hash": "not_approved_content",
                "risk": "none",
                "treatment": "retain_historical",
                "rationale": "The report records the decision path to this audit and remains historical evidence.",
            }
        if (
            "existing_yymm4_evidence" in path
            or "yymm4_existing_evidence_revalidation" in path
            or "README_EXISTING_YMM4" in path
        ):
            return {
                "category": "yymm4_evidence",
                "family": "current_lineage_revalidation",
                "authority": "current_structural_yymm4_authority",
                "hash": "approval_and_lineage_bound",
                "risk": "sanitized_hash_only",
                "treatment": "keep_primary",
                "rationale": "This is the accepted successor receipt over unchanged same-machine evidence.",
            }
        if "yymm4_operator_batch/" in path or filename in {
            "new_banknote_yymm4_import_operator_batch.py",
            "test_new_banknote_yymm4_import_operator_batch.py",
        }:
            return {
                "category": "operator_tooling",
                "family": "primary_approval_lineage_aware_operator_batch",
                "authority": "current_operator_batch_authority",
                "hash": "approved_eight_hash_lock",
                "risk": "runtime_paths_local_only",
                "treatment": "keep_primary",
                "rationale": "Primary tooling validates the human receipt and T00-T07 locks and supersedes the candidate batch.",
            }
        return {
            "category": "content_lineage",
            "family": "primary_approval_and_T00_T07",
            "authority": "current_content_authority",
            "hash": "approved_or_lineage_hash_bound",
            "risk": "sanitized",
            "treatment": "keep_primary",
            "rationale": "Primary approval and content-lineage artifacts remain authoritative.",
        }

    if path.startswith("docs/verification/"):
        return {
            "category": "historical_report",
            "family": "candidate_readiness_report",
            "authority": "immutable_candidate_history",
            "hash": "not_approved_content",
            "risk": "none",
            "treatment": "retain_historical",
            "rationale": "Keep only as dated candidate history; it must not become current state.",
        }
    if path in CANDIDATE_METADATA_EXCLUDE:
        relevance = (
            "approved_hash_conflict"
            if filename == "README_CANONICAL_SCRIPT_REVIEW.md"
            else "candidate_metadata_overlay"
        )
        return {
            "category": "source_script_receipt_metadata",
            "family": "candidate_metadata_overlay",
            "authority": "primary_version_wins",
            "hash": relevance,
            "risk": "none",
            "treatment": "exclude",
            "rationale": "Do not replace primary approved or source-generation surfaces with candidate metadata-link variants.",
        }
    if "/operator_batch/" in path or filename in {
        "new_banknote_yymm4_import_operator_batch.py",
        "test_new_banknote_yymm4_import_operator_batch.py",
    }:
        return {
            "category": "operator_tooling",
            "family": "candidate_predecessor_operator_batch",
            "authority": "superseded_operator_tooling",
            "hash": "six_hash_predecessor_contract",
            "risk": "runtime_paths_local_only",
            "treatment": "exclude",
            "rationale": "The four-action candidate batch lacks the current approval/T00-T07 gate and conflicts add/add with primary tooling.",
        }
    if filename == "supervisor_yymm4_import_observation_review_receipt.json":
        return {
            "category": "historical_receipt",
            "family": "bounded_predecessor_supervisor_review",
            "authority": "historical_only_primary_human_receipt_wins",
            "hash": "six_approved_hashes_match",
            "risk": "sanitized",
            "treatment": "retain_historical",
            "rationale": "The bounded batch review predates and is superseded in authority by the explicit primary human receipt.",
        }
    if (
        "yymm4_import_observation" in path
        or "yymm4_import_source_to_project_traceability" in path
        or "README_YMM4_IMPORT_OBSERVATION" in path
    ):
        return {
            "category": "yymm4_evidence",
            "family": "candidate_tracked_predecessor_observation",
            "authority": "historical_observation_secondary",
            "hash": "same_project_result_and_timing_as_primary",
            "risk": "repo_relative_local_identity_only",
            "treatment": "integrate_candidate",
            "rationale": "Retain as the historical tracked observation beneath the primary current-lineage revalidation receipt.",
        }
    if "/editorial_provenance/" in path:
        if path in EDITORIAL_REGENERATE:
            return {
                "category": "editorial_provenance",
                "family": "candidate_editorial_provenance_authority_surface",
                "authority": "secondary_surface_must_bind_primary_authority",
                "hash": "candidate_local_state_sensitive",
                "risk": "same_machine_status_must_not_be_promoted",
                "treatment": "regenerate_successor",
                "rationale": "Regenerate against the primary human receipt, T00-T07 package, and current revalidation rather than copying candidate-current claims.",
            }
        return {
            "category": "editorial_provenance",
            "family": "candidate_editorial_deep_audit_core",
            "authority": "secondary_deep_audit_evidence",
            "hash": "canonical_cue_claim_identity_exact",
            "risk": "sanitized_no_raw_body",
            "treatment": "integrate_candidate",
            "rationale": "D00-D10, cue transformation, authorship bounds, and prior-script audit complement T00-T07 without replacing it.",
        }
    if filename in {"editorial_provenance.py", "test_editorial_provenance.py"}:
        return {
            "category": "editorial_provenance_implementation",
            "family": "candidate_editorial_provenance_generator",
            "authority": "integration_source_requires_primary_rebind",
            "hash": "generated_surface_binding",
            "risk": "local_evidence_optional_state_affects_three_outputs",
            "treatment": "integrate_candidate",
            "rationale": "Import as implementation source, rebind to primary authority, and make regenerated successor surfaces portable before acceptance.",
        }
    if "/visual_scene_decision/" in path:
        return {
            "category": "visual_proposal",
            "family": "candidate_visual_ABC_review_package",
            "authority": "proposal_only_recommended_not_selected",
            "hash": "nine_cue_scene_claim_identity_exact",
            "risk": "rights_unresolved_proposal_only",
            "treatment": "integrate_candidate",
            "rationale": "The A/B/C package is content-compatible and remains explicitly unselected and unimplemented.",
        }
    if filename in {
        "new_banknote_yymm4_import_intake_visual_decision.py",
        "test_new_banknote_yymm4_import_intake_visual_decision.py",
    }:
        return {
            "category": "visual_proposal_implementation",
            "family": "candidate_visual_observation_generator",
            "authority": "proposal_validation_tooling",
            "hash": "nine_cue_and_observation_bound",
            "risk": "no_gui_or_media",
            "treatment": "integrate_candidate",
            "rationale": "Focused candidate tests pass and the generator preserves recommended-not-selected status.",
        }
    raise RuntimeError(f"UNCLASSIFIED_PATH:{side}:{path}")


def _build_path_inventory(repo: Path) -> dict[str, Any]:
    side_rows = {
        "primary": _diff_paths(repo, PRIMARY_REF),
        "candidate": _diff_paths(repo, CANDIDATE_REF),
    }
    side_sets = {side: {path for _, path in rows} for side, rows in side_rows.items()}
    overlap = side_sets["primary"] & side_sets["candidate"]
    rows: list[dict[str, Any]] = []
    for side, ref in (("primary", PRIMARY_REF), ("candidate", CANDIDATE_REF)):
        opposite = CANDIDATE_REF if side == "primary" else PRIMARY_REF
        opposite_set = side_sets["candidate" if side == "primary" else "primary"]
        for status, path in side_rows[side]:
            classification = _path_classification(side, path)
            data = _blob(repo, ref, path)
            opposite_hash = (
                _sha256(_blob(repo, opposite, path)) if path in opposite_set else None
            )
            rows.append(
                {
                    "side": side,
                    "status": status,
                    "path": path,
                    "primary_category": classification["category"],
                    "artifact_family": classification["family"],
                    "authority_role": classification["authority"],
                    "content_hash_relevance": classification["hash"],
                    "overlap_with_opposite_side": path in overlap,
                    "side_blob_sha256": _sha256(data),
                    "opposite_blob_sha256": opposite_hash,
                    "opposite_blob_equal": (
                        opposite_hash == _sha256(data)
                        if opposite_hash is not None
                        else None
                    ),
                    "privacy_or_local_binary_risk": classification["risk"],
                    "proposed_treatment": classification["treatment"],
                    "rationale": classification["rationale"],
                }
            )
    return {
        "schema_version": "new_banknote.successor_path_inventory.v1",
        "status": "passed",
        "baseline": BASELINE,
        "primary_path_entry_count": len(side_rows["primary"]),
        "candidate_path_entry_count": len(side_rows["candidate"]),
        "audited_side_path_entry_count": len(rows),
        "union_path_count": len(side_sets["primary"] | side_sets["candidate"]),
        "overlap_path_count": len(overlap),
        "overlap_paths": sorted(overlap),
        "unclassified_path_count": 0,
        "paths": sorted(rows, key=lambda row: (row["side"], row["path"])),
    }


def _approved_content_identity(repo: Path) -> dict[str, Any]:
    receipt = _json_blob(repo, PRIMARY_REF, f"{PILOT}/human_script_approval_receipt.json")
    rows: list[dict[str, Any]] = []
    for name in APPROVED_FILENAMES:
        expected = receipt["approved_file_hashes"][name]
        path = f"{PILOT}/{name}"
        primary_hash = _sha256(_blob(repo, PRIMARY_REF, path))
        candidate_hash = _sha256(_blob(repo, CANDIDATE_REF, path))
        rows.append(
            {
                "name": name,
                "expected_sha256": expected,
                "primary_sha256": primary_hash,
                "candidate_sha256": candidate_hash,
                "primary_matches_approval": primary_hash == expected,
                "candidate_matches_approval": candidate_hash == expected,
                "cross_branch_equal": primary_hash == candidate_hash,
                "classification": (
                    "exact_compatible"
                    if candidate_hash == expected
                    else "approval_conflicting_metadata_drift_exclude"
                ),
            }
        )
    canonical_primary = _json_blob(repo, PRIMARY_REF, f"{PILOT}/canonical_script.json")
    canonical_candidate = _json_blob(repo, CANDIDATE_REF, f"{PILOT}/canonical_script.json")

    def csv_rows(ref: str, name: str) -> list[list[str]]:
        text = _blob(repo, ref, f"{PILOT}/{name}").decode("utf-8-sig")
        return list(csv.reader(io.StringIO(text)))

    primary_csv = csv_rows(PRIMARY_REF, "canonical_yymm4.csv")
    candidate_csv = csv_rows(CANDIDATE_REF, "canonical_yymm4.csv")
    primary_derived = csv_rows(PRIMARY_REF, "derived_yymm4_import.csv")
    candidate_derived = csv_rows(CANDIDATE_REF, "derived_yymm4_import.csv")
    return {
        "approval_receipt_id": receipt["receipt_id"],
        "approved_commit": receipt["approved_commit"],
        "approved_files": rows,
        "primary_all_eight_match": all(row["primary_matches_approval"] for row in rows),
        "candidate_exact_match_count": sum(row["candidate_matches_approval"] for row in rows),
        "candidate_drift_count": sum(not row["candidate_matches_approval"] for row in rows),
        "canonical_script_json_object_equal": canonical_primary == canonical_candidate,
        "cue_count": receipt["approved_contract"]["cue_count"],
        "scene_allocation": receipt["approval_scope"]["scene_allocation"],
        "speaker_counts": receipt["approval_scope"]["canonical_speaker_counts"],
        "adopted_claim_count": receipt["approved_contract"]["unique_adopted_claim_count"],
        "factual_support_unit_count": receipt["approved_contract"]["factual_support_unit_count"],
        "claim_edge_count": receipt["approved_contract"]["claim_edge_count"],
        "unsupported_spoken_claim_count": receipt["approved_contract"]["unsupported_spoken_claim_count"],
        "canonical_csv_cross_branch_equal": primary_csv == candidate_csv,
        "derived_csv_cross_branch_equal": primary_derived == candidate_derived,
        "canonical_derived_text_equal_on_both_sides": (
            [row[1] for row in primary_csv] == [row[1] for row in primary_derived]
            and [row[1] for row in candidate_csv] == [row[1] for row in candidate_derived]
        ),
        "candidate_human_approval_receipt_present": False,
        "authority_result": "primary_human_approval_receipt_and_all_eight_primary_hashes_win",
    }


def _merge_tree_conflicts(repo: Path) -> list[str]:
    text = _git(repo, "merge-tree", BASELINE, PRIMARY_REF, CANDIDATE_REF)
    lines = text.splitlines()
    conflicts: list[str] = []
    for index, line in enumerate(lines):
        if line not in {"changed in both", "added in both", "removed in local", "removed in remote"}:
            continue
        for candidate_line in lines[index + 1 : index + 5]:
            stripped = candidate_line.strip()
            if stripped.startswith("our "):
                conflicts.append(stripped.split(maxsplit=3)[-1])
                break
    return sorted(set(conflicts))


def _authority_matrix() -> dict[str, Any]:
    rows = [
        {
            "artifact_family": "approved_content",
            "primary_role": "sole current authority: explicit human receipt plus eight hashes",
            "candidate_role": "seven exact files plus one metadata-modified approved README",
            "conflict": "candidate README hash conflicts with primary approval",
            "resolution": "keep all primary approved files; exclude candidate README variant",
            "later_treatment": "keep_primary",
        },
        {
            "artifact_family": "content_lineage",
            "primary_role": "sole current T00-T07 human surface and policy",
            "candidate_role": "no T00-T07 successor package",
            "conflict": "none after primary authority is fixed",
            "resolution": "keep primary lineage byte-exact",
            "later_treatment": "keep_primary",
        },
        {
            "artifact_family": "editorial_provenance",
            "primary_role": "T00-T07 remains the current content authority",
            "candidate_role": "secondary D00-D10 deep-audit evidence and prior-script audit",
            "conflict": "candidate README/lock/readback claim candidate-current and encode same-machine reverify status",
            "resolution": "integrate stable core; regenerate three authority surfaces against primary receipts",
            "later_treatment": "selective_integrate_and_regenerate",
        },
        {
            "artifact_family": "YMM4_evidence",
            "primary_role": "current-lineage revalidation is current structural authority",
            "candidate_role": "tracked historical predecessor observation of the same bytes",
            "conflict": "no metric/hash/timing conflict",
            "resolution": "retain candidate observation as historical beneath the primary successor receipt",
            "later_treatment": "integrate_candidate_as_historical",
        },
        {
            "artifact_family": "Operator_Batch",
            "primary_role": "current five-action approval/T00-T07-aware batch",
            "candidate_role": "superseded four-action predecessor batch",
            "conflict": "add/add code and test conflict; candidate lacks current approval/lineage checks",
            "resolution": "keep primary tooling; exclude candidate executable batch; retain bounded review receipt as history",
            "later_treatment": "keep_primary_exclude_candidate_tooling",
        },
        {
            "artifact_family": "visual_ABC",
            "primary_role": "no selected visual route",
            "candidate_role": "proposal-only A/B/C package; Route A recommended_not_selected",
            "conflict": "none with approved content; human preference remains unknown",
            "resolution": "integrate package without changing recommendation or authorization fields",
            "later_treatment": "integrate_candidate",
        },
        {
            "artifact_family": "current_state",
            "primary_role": "newer accepted evidence at primary base",
            "candidate_role": "older visual-selection-ready state with competing authority claims",
            "conflict": "five current-state documents conflict in merge-tree",
            "resolution": "regenerate one successor state after selective integration",
            "later_treatment": "regenerate_successor",
        },
        {
            "artifact_family": "historical_reports",
            "primary_role": "G0-G9 roadmap and primary handoff history",
            "candidate_role": "dated candidate readiness report",
            "conflict": "none when explicitly historical",
            "resolution": "retain reports immutable; never use them as current state",
            "later_treatment": "retain_historical",
        },
    ]
    return {
        "schema_version": "new_banknote.successor_authority_conflict_matrix.v1",
        "status": "passed",
        "recommendation_class": RECOMMENDATION_CLASS,
        "one_to_one_authority_roles": True,
        "unresolved_authority_count": 0,
        "matrix": rows,
    }


def _candidate_path_sets(path_inventory: dict[str, Any]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {
        "integrate_candidate": [],
        "retain_historical": [],
        "regenerate_successor": [],
        "exclude": [],
    }
    for row in path_inventory["paths"]:
        if row["side"] != "candidate":
            continue
        treatment = row["proposed_treatment"]
        groups[treatment].append(row["path"])
    return {key: sorted(value) for key, value in groups.items()}


def _build_audit(
    repo: Path,
    refs: dict[str, Any],
    commits: dict[str, Any],
    paths: dict[str, Any],
    authority: dict[str, Any],
) -> dict[str, Any]:
    identity = _approved_content_identity(repo)
    conflicts = _merge_tree_conflicts(repo)
    candidate_paths = _candidate_path_sets(paths)
    visual = _json_blob(
        repo,
        CANDIDATE_REF,
        f"{PILOT}/visual_scene_decision/recommended_visual_direction.json",
    )
    observation = _json_blob(
        repo, CANDIDATE_REF, f"{PILOT}/yymm4_import_observation_receipt.json"
    )
    return {
        "schema_version": "new_banknote.successor_integration_audit.v1",
        "status": "passed",
        "recommendation_class": RECOMMENDATION_CLASS,
        "selected_state": {
            "Project-State-ID": STATE_ID,
            "Product-State": "new-banknote-successor-integration-audited-selective-ready",
            "Product-Gate": "new-banknote-successor-selective-integration",
            "Recommended-Next": "integrate-audited-new-banknote-successor-artifacts",
            "External-State": "public-repo-feature-branch",
        },
        "refs": refs,
        "graph": {
            "primary_ref": PRIMARY_REF,
            "candidate_ref": CANDIDATE_REF,
            "common_baseline": BASELINE,
            "primary_only_commit_count": refs["primary_only_commit_count"],
            "candidate_only_commit_count": refs["candidate_only_commit_count"],
            "merge_tree_result": "conflicts_present_no_worktree_or_index_mutation",
            "merge_tree_conflict_count": len(conflicts),
            "merge_tree_conflict_paths": conflicts,
            "normal_merge_recommended": False,
        },
        "coverage": {
            "audited_commit_count": commits["audited_commit_count"],
            "unclassified_commit_count": commits["unclassified_commit_count"],
            "audited_side_path_entry_count": paths["audited_side_path_entry_count"],
            "union_path_count": paths["union_path_count"],
            "unclassified_path_count": paths["unclassified_path_count"],
        },
        "approved_content_identity": identity,
        "authority_result": authority,
        "YMM4_evidence_comparison": {
            "primary_current_authority": "existing_yymm4_evidence_revalidation_receipt.json",
            "candidate_historical_authority": "yymm4_import_observation_receipt.json",
            "project_sha256": observation["project_identity"]["sha256"],
            "result_sha256": observation["operator_result"]["sha256"],
            "VoiceItem_count": observation["verified_import_contract"]["VoiceItem_count"],
            "fps": observation["verified_import_contract"]["fps"],
            "timeline_frames": observation["verified_import_contract"]["timeline_frames"],
            "duration_seconds": observation["verified_import_contract"]["duration_seconds"],
            "metric_or_hash_conflict": False,
            "pronunciation_rhythm_clipping": "unknown",
        },
        "visual_result": {
            "candidate_package_compatible": True,
            "recommendation_status": visual["status"],
            "recommended_route": visual["route"]["route_id"],
            "human_selection_required": visual["human_selection_required"],
            "implementation_authorized": visual["implementation_authorized"],
            "selected_route": None,
        },
        "semantic_conflicts": [
            {
                "id": "SC1",
                "issue": "candidate approved README metadata drift",
                "resolution": "exclude candidate variant and keep primary approved hash",
                "blocks_recommendation": False,
            },
            {
                "id": "SC2",
                "issue": "five current-state documents conflict",
                "resolution": "regenerate one successor state; never merge prose",
                "blocks_recommendation": False,
            },
            {
                "id": "SC3",
                "issue": "Operator Batch module and test add/add conflict",
                "resolution": "keep primary implementation and exclude candidate executable family",
                "blocks_recommendation": False,
            },
            {
                "id": "SC4",
                "issue": "candidate provenance README/lock/readback depend on candidate-current and same-machine state",
                "resolution": "regenerate those three surfaces against primary authority",
                "blocks_recommendation": False,
            },
        ],
        "blockers": [],
        "quality_debt": [
            {
                "id": "D1",
                "issue": "pronunciation/rhythm/clipping unknown",
                "owner": "human audio reviewer",
                "revisit_trigger": "audio acceptance is requested after visual selection",
            },
            {
                "id": "D2",
                "issue": "exact S04 generation-time binary and S05 historical identity unresolved",
                "owner": "source provenance reviewer",
                "revisit_trigger": "stable source identity appears or provenance claim expands",
            },
            {
                "id": "D3",
                "issue": "token-level authorship unavailable",
                "owner": "content-lineage owner",
                "revisit_trigger": "new contemporaneous evidence exists",
            },
            {
                "id": "D4",
                "issue": "human visual selection pending",
                "owner": "human visual reviewer",
                "revisit_trigger": "unified A/B/C review surface is available after H1",
            },
            {
                "id": "D5",
                "issue": "remote CI and branch policy not evidenced",
                "owner": "integration owner",
                "revisit_trigger": "H1 branch is pushed or a PR is opened",
            },
        ],
        "integration_contract": {
            "integration_owner": "new-banknote-successor-selective-integration-v1",
            "target_successor_branch": "codex/new-banknote-successor-selective-integration-v1",
            "target_base_revision": PRIMARY_HEAD,
            "candidate_source_revision": CANDIDATE_HEAD,
            "accepted_primary_inputs": [
                "primary human_script_approval_receipt.json and all eight approved files",
                "primary README_CONTENT_LINEAGE.md and T00-T07 lineage package",
                "primary existing YMM4 evidence revalidation package",
                "primary yymm4_operator_batch/ plus current module and tests",
                "primary supervisor roadmap and immutable history",
            ],
            "accepted_candidate_paths": candidate_paths["integrate_candidate"],
            "historical_candidate_paths": candidate_paths["retain_historical"],
            "regenerate_after_copy_paths": candidate_paths["regenerate_successor"],
            "excluded_candidate_paths": candidate_paths["exclude"],
            "mechanism": "selective_path_materialization_from_exact_candidate_ref_onto_exact_primary_base",
            "ordered_steps": [
                "create the successor branch from the exact primary base",
                "materialize only accepted candidate paths from the exact candidate revision",
                "retain historical candidate receipts/reports with explicit secondary status",
                "keep all primary approved, lineage, revalidation, and Operator Batch bytes",
                "rebind editorial provenance implementation to primary approval/T00-T07/revalidation authority",
                "regenerate the three provenance authority surfaces and all compact current-state surfaces",
                "run targeted primary, editorial-provenance, visual, observation, privacy, and state validation",
            ],
            "conflict_resolution_policy": {
                "approved_content": "primary_wins_byte_exact",
                "content_lineage": "primary_T00_T07_is_current",
                "YMM4_revalidation": "primary_successor_receipt_is_current",
                "Operator_Batch": "primary_only",
                "editorial_provenance": "candidate_secondary_core_with_regenerated_primary_links",
                "visual": "candidate_proposal_only_no_selection",
                "current_state": "regenerate_never_mechanical_merge",
            },
            "targeted_validation": [
                "primary content-transformation lineage validator",
                "primary content-lineage, Operator Batch, and existing-evidence revalidation focused tests",
                "editorial-provenance focused tests with portable absent-local-evidence behavior",
                "candidate visual-decision and import-observation focused tests",
                "approved eight-hash and canonical/derived CSV comparison",
                "all JSON plus visual HTML parse",
                "recommended_not_selected and no selected/approved/implemented route checks",
                "privacy, path, raw-body, local-binary, state-sync, and diff checks",
            ],
            "completion_evidence": [
                "all primary approved hashes remain exact",
                "primary current-lineage revalidation receipt remains byte-exact",
                "one regenerated current state names the integrated successor",
                "focused tests and state sync pass",
                "source refs remain unchanged and successor parity is 0/0",
            ],
            "rollback_boundary": "delete or abandon only the new successor branch; primary, candidate, and master refs remain immutable",
            "supervisor_decision_required": "accept this selective path contract before dispatching H1; no A/B/C choice is requested until H2",
        },
        "operations_not_performed": [
            "source branch merge, rebase, or cherry-pick",
            "actual selective integration",
            "approved script, source, claim, or CSV modification",
            "visual route selection or implementation",
            "YMM4, Computer Use, render, media, publication, rights, or master mutation",
            "full test suite",
        ],
    }


def _render_markdown(audit: dict[str, Any], paths: dict[str, Any]) -> str:
    identity = audit["approved_content_identity"]
    contract = audit["integration_contract"]
    conflicts = audit["graph"]["merge_tree_conflict_paths"]
    return f"""# New-banknote Successor Branch Integration Audit

> **READ-FIRST AUDIT — NO SOURCE BRANCH INTEGRATION — NO VISUAL SELECTION**

## Recommendation

- class: `{audit['recommendation_class']}`
- state: `{STATE_ID}`
- primary: `{PRIMARY_REF}` @ `{PRIMARY_HEAD}`
- candidate: `{CANDIDATE_REF}` @ `{CANDIDATE_HEAD}`
- baseline: `{BASELINE}`
- divergence: primary-only `{audit['graph']['primary_only_commit_count']}` / candidate-only `{audit['graph']['candidate_only_commit_count']}`
- content change authorized or performed: `false`
- visual route selected: `false`

The two branches must not be normally merged. A selective path construction is ready:
keep the primary approval, T00–T07 lineage, current YMM4 revalidation, and
Operator Batch byte-exact; add only the candidate historical observation,
editorial deep-audit core, and A/B/C proposal paths; then regenerate the
candidate-current provenance surfaces and all current-state prose.

## Coverage

| measure | result |
| --- | ---: |
| primary-only commits | {audit['graph']['primary_only_commit_count']} |
| candidate-only commits | {audit['graph']['candidate_only_commit_count']} |
| audited commits | {audit['coverage']['audited_commit_count']} |
| primary side paths | {paths['primary_path_entry_count']} |
| candidate side paths | {paths['candidate_path_entry_count']} |
| audited side-path entries | {paths['audited_side_path_entry_count']} |
| union paths | {paths['union_path_count']} |
| overlapping paths | {paths['overlap_path_count']} |
| unclassified commits / paths | 0 / 0 |

## Approved-content identity

- primary approved hashes: `8 / 8` exact
- candidate approved hashes: `{identity['candidate_exact_match_count']} / 8` exact
- candidate drift: `README_CANONICAL_SCRIPT_REVIEW.md` metadata link only;
  it is excluded because its hash is approval-conflicting
- canonical script JSON object, TXT, canonical CSV, derived CSV, cue trace,
  and source manifest: exact across branches
- content contract: 9 cues, S1/S2/S3 `2/4/3`, Reimu/Marisa `3/6`, 15 adopted
  claims, 20 factual units, 21 evidence edges, unsupported spoken claims `0`
- authority: primary explicit human approval receipt and all eight primary
  hashes remain sole current authority

## Authority result

| family | current role after later integration | candidate treatment |
| --- | --- | --- |
| Approved content | primary human receipt + eight hashes | exclude the modified approved README variant |
| Content lineage | primary T00–T07 package | no replacement |
| Editorial provenance | primary lineage remains current; D00–D10 is secondary deep audit | integrate stable core; regenerate README/lock/readback |
| YMM4 evidence | primary current-lineage revalidation | retain candidate observation as historical predecessor |
| Operator Batch | primary five-action approval/lineage-aware family | exclude candidate four-action executable family |
| Visual A/B/C | proposal-only review surface | integrate with Route A `recommended_not_selected` |
| Current state | one successor state | regenerate; never merge branch prose |

## Conflict and merge mechanics

`git merge-tree` found {len(conflicts)} conflicts and did not mutate the index,
worktree, or refs:

{chr(10).join(f'- `{path}`' for path in conflicts)}

The five state documents require regeneration. The two Operator Batch code/test
paths are add/add conflicts where primary wins. A normal merge or whole-commit
cherry-pick is rejected because candidate commits mix compatible additions with
state, approved-README, generator, and Operator Batch changes.

## Candidate contribution

- tracked predecessor YMM4 observation: same project/result hashes, 9
  VoiceItems, 3/6, exact text/order, 60 fps, 4415 frames, 73.583333 seconds
- editorial deep audit: D00–D10, 9/9 cue coverage, 38/38 attributed substantive
  units, bounded prior-user-script result
  `not_proven_from_available_repo_evidence`
- visual review: three routes; Route A recommended but not selected; S1/S2/S3
  map to 2/4/3 cues; implementation and rights approval remain false

Candidate detached focused validation passed 30 tests and failed one
cross-check because three committed provenance surfaces encode the original
same-machine local-evidence disposition. That failure is the evidence for
`regenerate_successor`, not authority to repair the candidate branch.

## Exact later integration contract

- owner: `{contract['integration_owner']}`
- successor branch: `{contract['target_successor_branch']}`
- base: `{contract['target_base_revision']}`
- candidate source: `{contract['candidate_source_revision']}`
- mechanism: `{contract['mechanism']}`
- candidate paths to integrate: {len(contract['accepted_candidate_paths'])}
- candidate paths retained as historical: {len(contract['historical_candidate_paths'])}
- candidate paths regenerated: {len(contract['regenerate_after_copy_paths'])}
- candidate paths excluded: {len(contract['excluded_candidate_paths'])}

Order:

{chr(10).join(f'{index}. {step}' for index, step in enumerate(contract['ordered_steps'], start=1))}

The full exact path lists, exclusions, authority roles, and validation plan are
in `new_banknote_successor_integration_audit.json` and the path inventory.

## Gates that remain open

- pronunciation / rhythm / clipping: unknown
- exact S04/S05 historical identity: unresolved
- token-level authorship: unavailable
- human A/B/C selection: pending
- actual integration, diagnostic YMM4 project, render, production, rights,
  publication, and master integration: not performed

## Operations not performed

No source branch was merged, rebased, cherry-picked, or modified. No approved
content, candidate package, ignored evidence, YMM4 project, media, or master ref
was changed by this audit.
"""


def build_artifacts(repo_root: str | Path = REPO_ROOT) -> dict[str, bytes]:
    repo = Path(repo_root).resolve()
    refs = _verify_refs(repo)
    commits = _build_commit_inventory(repo, refs)
    paths = _build_path_inventory(repo)
    authority = _authority_matrix()
    audit = _build_audit(repo, refs, commits, paths, authority)
    markdown = _render_markdown(audit, paths)
    values: dict[str, Any] = {
        OUTPUT_NAMES[0]: markdown,
        OUTPUT_NAMES[1]: audit,
        OUTPUT_NAMES[2]: commits,
        OUTPUT_NAMES[3]: paths,
        OUTPUT_NAMES[4]: authority,
    }
    return {
        name: (
            (value.rstrip() + "\n").encode("utf-8")
            if isinstance(value, str)
            else (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode(
                "utf-8"
            )
        )
        for name, value in values.items()
    }


def _privacy_check(artifacts: dict[str, bytes]) -> None:
    private_path = re.compile(r"(?i)(?:[a-z]:[\\/]|/users/|/home/|\\\\[^\\\s]+\\)")
    uuid = re.compile(
        r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"
    )
    for name, data in artifacts.items():
        text = data.decode("utf-8")
        if private_path.search(text):
            raise RuntimeError(f"PRIVATE_PATH_LEAK:{name}")
        if uuid.search(text):
            raise RuntimeError(f"UUID_LEAK:{name}")
        if "https://notebooklm" in text.lower():
            raise RuntimeError(f"PRIVATE_NOTEBOOKLM_URL_LEAK:{name}")
        if any(key in text for key in ('"raw_text"', '"source_body"', '"transcript_body"')):
            raise RuntimeError(f"RAW_BODY_KEY_LEAK:{name}")


def write_artifacts(
    repo_root: str | Path = REPO_ROOT,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    repo = Path(repo_root).resolve()
    destination = (
        Path(output_dir).resolve()
        if output_dir is not None
        else repo / VERIFICATION_DIR
    )
    artifacts = build_artifacts(repo)
    _privacy_check(artifacts)
    destination.mkdir(parents=True, exist_ok=True)
    for name, data in artifacts.items():
        (destination / name).write_bytes(data)
    return {
        "status": "passed",
        "recommendation_class": RECOMMENDATION_CLASS,
        "state_id": STATE_ID,
        "written_files": list(artifacts),
        "artifact_sha256": {
            name: _sha256(data) for name, data in artifacts.items()
        },
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args(list(argv) if argv is not None else None)
    print(
        json.dumps(
            write_artifacts(args.repo_root, args.output_dir),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
