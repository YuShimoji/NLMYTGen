"""Build and validate content-transformation lineage artifacts.

This module is deliberately content-preserving.  It records stage, clause,
claim, evidence, and approval identities for an already approved artifact
family.  It does not generate, rewrite, or repair script text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

from src.pipeline.new_banknote_authoritative_script import (
    EXPECTED_SCENE_ALLOCATION,
    EXPECTED_SPEAKER_COUNTS,
    validate_new_banknote_authoritative_script_package,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
PILOT_RELATIVE = Path(
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
DEFAULT_PILOT_DIR = REPO_ROOT / PILOT_RELATIVE

APPROVED_COMMIT = "b05eb3867caabda496fb9a0070d230a4e81aea01"
APPROVAL_RECEIPT_ID = "new-banknote-script-option-a-approval-v1"
APPROVAL_RECORDED_AT = "2026-07-14T13:17:00+09:00"
TARGET_STATE_ID = "new-banknote-content-lineage-sealed-yymm4-batch-ready-v1"

APPROVED_HASHES = {
    "README_CANONICAL_SCRIPT_REVIEW.md": (
        "a5d5a23fca7d6c0c0fe200a89800d9c3c8ac278c18c1a137c35019d4780e7da8"
    ),
    "canonical_script.json": (
        "4d272900e84c8f87c484aa84c1dd1909207ee8acc189603009a186af65837c47"
    ),
    "canonical_script.txt": (
        "4eff43d0cd1f7842b02aaacd8ac6393cc12910fe70f21d650d4a31c74c17c091"
    ),
    "canonical_script_review.md": (
        "9816c28e9b0099ef98e2aefb9e70bf22a32fbbd0f931fd8989c6ac19dcd99d3a"
    ),
    "cue_source_traceability.json": (
        "5b6601134baf0e319cf252c24a3addecbecc02432f9a38234fdfc6580e038f47"
    ),
    "canonical_yymm4.csv": (
        "23361565b18d5e8d96768ad2877b1505e0bdeb5aacb5fbd0022a11f5e8dcfb12"
    ),
    "derived_yymm4_import.csv": (
        "127dd3edd32ce6131f339819263a6d2716570f800ad212b0741a384b7e19f9ee"
    ),
    "source_to_script_manifest.json": (
        "e13fb57a2681875f577e4d85f13cf41bfc601519892fa4f975bdfcdd24d927b5"
    ),
}

LINEAGE_FILENAMES = (
    "human_script_approval_receipt.json",
    "README_CONTENT_LINEAGE.md",
    "content_transformation_ledger.json",
    "cue_lineage_matrix.json",
    "content_change_summary.md",
    "content_change_policy.json",
    "content_lineage_readback.json",
)

EXPECTED_OUTCOME_COUNTS = {
    "duplicate_not_used": 26,
    "rejected_policy_intent": 10,
    "rejected_quantitative_without_exact_source": 18,
    "rejected_unsupported": 15,
    "style_or_rhetoric_only": 52,
    "supported_context_only": 11,
    "unresolved_not_used": 31,
    "verified_primary": 19,
}

PRE_EDITORIAL_BASELINE = {
    "commit": "a307083891cccb974021d2523a3b30e1b1c60a5c",
    "cue_count": 9,
    "factual_unit_count": 22,
    "claim_edge_count": 23,
    "unique_adopted_claim_count": 17,
    "artifacts": {
        "canonical_script.json": (
            "c1c7dacdaf0961f2c1796639e401f2d7ad41c5eb9dfe998727715a341ac26a87"
        ),
        "cue_source_traceability.json": (
            "98534ded178900adf30148bff2e6690ed7d9a9c9696eeee9d3aa45dcb4e30a7e"
        ),
        "canonical_yymm4.csv": (
            "549d382cec35dcd9f9f51ee21f9e82d68f662156baacf56891a888832aae1ab3"
        ),
        "derived_yymm4_import.csv": (
            "179421d0e04b3e510c76c63e7a8613586a2115172743d5892689a656c5282069"
        ),
        "script_generation_receipt.json": (
            "678edad35a24aaeeefb4ee46a1f3703032a65eb6e3adf589a799f8ae18060d10"
        ),
    },
}

_PRIVATE_PATH_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/]|\\\\[^\\\s]+[\\/]|/home/|/users/)"
)
_UUID_RE = re.compile(
    r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
)

STRUCTURAL_ROLES = {
    "cue_001": "S1 opening question and scope",
    "cue_002": "S1 direct answer and two-family overview",
    "cue_003": "S2 first anti-counterfeit technique",
    "cue_004": "S2 second anti-counterfeit technique",
    "cue_005": "S2 tactile technique confirmation",
    "cue_006": "S2 tool-assisted microtext explanation",
    "cue_007": "S3 tactile identification design",
    "cue_008": "S3 visual identification design compression",
    "cue_009": "S3 four-method recap",
}

LAST_CONTENT_STAGE = {
    **{f"cue_{index:03d}": "T05" for index in range(1, 10)},
    "cue_005": "T04",
}

EDITORIAL_UNITS: dict[str, list[dict[str, Any]]] = {
    "cue_001": [
        {
            "unit_id": "cue_001_editorial_01",
            "surface_fragment": "見た目以外にも",
            "role": "opens a contrast beyond appearance",
        }
    ],
    "cue_002": [
        {
            "unit_id": "cue_002_editorial_01",
            "surface_fragment": "偽造防止では",
            "role": "groups the following supported techniques",
        }
    ],
    "cue_003": [
        {
            "unit_id": "cue_003_editorial_01",
            "surface_fragment": "まずは",
            "role": "orders the S2 explanation",
        }
    ],
    "cue_004": [
        {
            "unit_id": "cue_004_editorial_01",
            "surface_fragment": "次は",
            "role": "continues the S2 explanation",
        }
    ],
    "cue_005": [],
    "cue_006": [
        {
            "unit_id": "cue_006_editorial_01",
            "surface_fragment": "二文への分割",
            "role": "separates checking method from reproduction difficulty",
        }
    ],
    "cue_007": [
        {
            "unit_id": "cue_007_editorial_01",
            "surface_fragment": "見分けやすさの工夫では",
            "role": "moves from security techniques to identification design",
        }
    ],
    "cue_008": [
        {
            "unit_id": "cue_008_editorial_01",
            "surface_fragment": "三つの事実を二文で並列化",
            "role": "compresses related visual-identification facts",
        }
    ],
    "cue_009": [
        {
            "unit_id": "cue_009_editorial_01",
            "surface_fragment": "確認方法は",
            "role": "introduces the closing recap",
        },
        {
            "unit_id": "cue_009_editorial_02",
            "surface_fragment": "この四つを覚えておこう",
            "role": "structural summary and retention prompt",
        },
    ],
}

VOICE_UNITS: dict[str, list[dict[str, Any]]] = {
    "cue_001": [{"surface_fragment": "って、…あるの？", "role": "Reimu question"}],
    "cue_002": [{"surface_fragment": "あるぞ。…んだ。", "role": "Marisa answer"}],
    "cue_003": [{"surface_fragment": "んだぜ。", "role": "Marisa ending"}],
    "cue_004": [{"surface_fragment": "ぞ。", "role": "Marisa ending"}],
    "cue_005": [{"surface_fragment": "なんだね。", "role": "Reimu confirmation"}],
    "cue_006": [{"surface_fragment": "なんだ。", "role": "Marisa ending"}],
    "cue_007": [{"surface_fragment": "ぜ。", "role": "Marisa ending"}],
    "cue_008": [{"surface_fragment": "んだね。", "role": "Reimu confirmation"}],
    "cue_009": [{"surface_fragment": "覚えておこう。", "role": "Marisa closing invitation"}],
}


def _json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path.name}")
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _artifact(pilot: Path, name: str) -> dict[str, Any]:
    path = pilot / name
    return {
        "repo_relative_path": f"{PILOT_RELATIVE.as_posix()}/{name}",
        "sha256": _sha256(path),
    }


def _historical_artifact(name: str) -> dict[str, Any]:
    return {
        "repo_relative_path": f"{PILOT_RELATIVE.as_posix()}/{name}",
        "sha256": PRE_EDITORIAL_BASELINE["artifacts"][name],
        "git_commit": PRE_EDITORIAL_BASELINE["commit"],
        "identity_status": "recoverable_from_git_history",
    }


def _load_inputs(pilot: Path) -> dict[str, Any]:
    package_validation = validate_new_banknote_authoritative_script_package(pilot)
    if package_validation.get("status") != "passed":
        raise ValueError(
            "AUTHORITATIVE_SCRIPT_PACKAGE_INVALID:"
            + ",".join(package_validation.get("failed_checks", []))
        )

    actual_hashes = {name: _sha256(pilot / name) for name in APPROVED_HASHES}
    if actual_hashes != APPROVED_HASHES:
        raise ValueError("APPROVAL_BASELINE_DRIFT")

    script = _read_json(pilot / "canonical_script.json")
    trace = _read_json(pilot / "cue_source_traceability.json")
    adjudication = _read_json(pilot / "claim_adjudication.json")
    adjudication_readback = _read_json(pilot / "claim_adjudication_readback.json")
    editorial_receipt = _read_json(pilot / "editorial_revision_receipt.json")
    identity = _read_json(pilot / "input_identity_receipt.json")
    source_snapshot = _read_json(pilot / "source_set_snapshot.json")

    cues = script.get("cues") or []
    trace_cues = trace.get("cues") or []
    claims = adjudication.get("claims") or []
    adopted = {claim_id for cue in cues for claim_id in cue["adopted_claim_ids"]}
    factual_units = sum(len(cue["factual_support_units"]) for cue in trace_cues)
    claim_edges = sum(len(cue["supporting_evidence"]) for cue in trace_cues)
    scene_counts = dict(Counter(cue["scene_id"] for cue in cues))
    speaker_counts = dict(Counter(cue["speaker"] for cue in cues))
    verified = [c for c in claims if c["primary_outcome"] == "verified_primary"]

    contract = {
        "cue_count_9": len(cues) == 9,
        "scene_allocation_2_4_3": scene_counts == EXPECTED_SCENE_ALLOCATION,
        "speaker_counts_3_6": speaker_counts == EXPECTED_SPEAKER_COUNTS,
        "claim_count_182": len(claims) == 182,
        "verified_primary_19": len(verified) == 19,
        "adopted_claims_15": len(adopted) == 15,
        "factual_units_20": factual_units == 20,
        "claim_edges_21": claim_edges == 21,
        "unsupported_spoken_claims_zero": script.get("unsupported_claim_count") == 0,
        "claim_outcome_funnel_exact": (
            adjudication_readback.get("outcome_counts") == EXPECTED_OUTCOME_COUNTS
        ),
        "raw_identity_exact": (
            identity.get("raw_sha256")
            == "1825c9689a050ddbfc91537a228f6af0ba2f7f033e5b681fff4f227551144437"
            and identity.get("raw_size_bytes") == 32089
            and identity.get("raw_logical_line_count") == 326
        ),
        "source_snapshot_11": source_snapshot.get("source_count") == 11,
        "editorial_delta_22_to_20": editorial_receipt.get("factual_support_units")
        == {"before": 22, "after": 20},
        "editorial_edges_23_to_21": editorial_receipt.get("claim_edges")
        == {"before": 23, "after": 21},
    }
    failed = [name for name, passed in contract.items() if not passed]
    if failed:
        raise ValueError("APPROVED_CONTENT_CONTRACT_DRIFT:" + ",".join(failed))

    return {
        "script": script,
        "trace": trace,
        "claims": claims,
        "claim_by_id": {claim["claim_id"]: claim for claim in claims},
        "adopted": adopted,
        "factual_units": factual_units,
        "claim_edges": claim_edges,
        "identity": identity,
        "source_snapshot": source_snapshot,
        "editorial_receipt": editorial_receipt,
        "outcome_counts": adjudication_readback["outcome_counts"],
        "contract_checks": contract,
        "approved_hashes": actual_hashes,
    }


def _approval_receipt(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "content_transformation_lineage.human_approval_receipt.v1",
        "receipt_id": APPROVAL_RECEIPT_ID,
        "status": "valid",
        "approval_class": "explicit_user_option_a",
        "approval_recorded_at": APPROVAL_RECORDED_AT,
        "approval_timestamp_basis": "worker_recorded_with_local_utc_offset",
        "approved_commit": APPROVED_COMMIT,
        "approval_scope": {
            "script_text": True,
            "cue_order": True,
            "scene_allocation": {"S1": 2, "S2": 4, "S3": 3},
            "canonical_speaker_counts": {"れいむ": 3, "まりさ": 6},
            "canonical_csv_text_and_order": True,
            "derived_csv_text_and_order": True,
            "claim_and_source_traceability": True,
        },
        "approved_file_hashes": inputs["approved_hashes"],
        "approved_contract": {
            "cue_count": 9,
            "unique_adopted_claim_count": 15,
            "factual_support_unit_count": 20,
            "claim_edge_count": 21,
            "unsupported_spoken_claim_count": 0,
        },
        "permissions": {
            "operator_batch_preparation": True,
            "later_user_manual_import_observation": True,
            "wording_or_claim_revision": False,
            "worker_yymm4_operation": False,
            "render": False,
            "production": False,
            "publication": False,
            "rights_action": False,
        },
        "invalidation_rules": [
            "any approved file hash changes",
            "cue text, order, speaker, or scene changes",
            "adopted claim or evidence edge changes",
            "canonical or derived CSV text/order changes",
            "approval receipt is overwritten instead of superseded",
        ],
        "successor_receipt_policy": {
            "overwrite_current_receipt": False,
            "new_revision_id_required": True,
            "visible_diff_required": True,
            "renewed_explicit_human_approval_required_for": [
                "E_EDITORIAL_EVIDENCE_PRESERVING",
                "S_SEMANTIC",
                "U_UPSTREAM",
            ],
            "mechanical_change_without_content_hash_change": (
                "may retain approval when logged and validation passes"
            ),
        },
    }


def _content_policy() -> dict[str, Any]:
    return {
        "schema_version": "content_transformation_lineage.change_policy.v1",
        "status": "active",
        "policy_id": "no-silent-content-change-v1",
        "scope": "content artifact families from upstream input through serialization",
        "classes": {
            "M_MECHANICAL": {
                "definition": "encoding, serialization, alias projection, hashing, packaging",
                "content_change_allowed": False,
                "logging_required": True,
                "renewed_approval": "not_required_when_approved_content_hashes_are_unchanged",
            },
            "E_EDITORIAL_EVIDENCE_PRESERVING": {
                "definition": "rewording, shortening, ordering, connective, voice, compression",
                "logging_required": True,
                "post_approval_rule": "new_revision_visible_diff_and_renewed_human_approval",
            },
            "S_SEMANTIC": {
                "definition": "factual addition/removal, implication, judgment, statistic, claim adoption",
                "evidence_required": True,
                "logging_required": True,
                "approval_rule": "explicit_human_approval_always",
            },
            "U_UPSTREAM": {
                "definition": "changed source set, regeneration, replacement transcript",
                "new_upstream_snapshot_required": True,
                "approval_rule": "explicit_milestone_authorization",
            },
        },
        "required_stage_fields": [
            "stage_id",
            "input_artifacts_and_hashes",
            "output_artifacts_and_hashes",
            "actor_class",
            "change_class",
            "affected_claim_or_cue_ids",
            "semantic_change",
            "evidence_change",
            "approval_impact",
            "human_approval_required_for_equivalent_future_change",
            "approval_remains_valid_for_current_hashes",
            "before_after_summary",
            "rejection_or_omission_retention",
            "current_approval_status",
        ],
        "acceptance_rule": (
            "No content transformation may enter an artifact silently; missing lineage rejects acceptance."
        ),
        "current_approval_receipt_id": APPROVAL_RECEIPT_ID,
        "current_approval_status": "valid_only_while_all_approved_hashes_match",
    }


def _stage(
    stage_id: str,
    *,
    stage_type: str,
    actor_class: str,
    change_class: str,
    inputs: list[dict[str, Any]],
    outputs: list[dict[str, Any]],
    before: dict[str, Any],
    after: dict[str, Any],
    semantic_change: bool,
    evidence_change: bool,
    approval_impact: str,
    rationale: str,
    retention: str,
    status: str,
    affected_claim_or_cue_ids: str | list[str] = "see_output_artifacts",
    secondary_change_classes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "stage_id": stage_id,
        "stage_type": stage_type,
        "input_artifacts_and_hashes": inputs,
        "output_artifacts_and_hashes": outputs,
        "actor_class": actor_class,
        "change_class": change_class,
        "secondary_change_classes": secondary_change_classes or [],
        "affected_claim_or_cue_ids": affected_claim_or_cue_ids,
        "content_count_before": before,
        "content_count_after": after,
        "semantic_change": semantic_change,
        "factual_meaning_impact": "changed" if semantic_change else "unchanged",
        "evidence_change": evidence_change,
        "approval_impact": approval_impact,
        "human_approval_required_for_equivalent_future_change": (
            change_class != "M_MECHANICAL"
        ),
        "approval_remains_valid_for_current_hashes": True,
        "before_after_summary": {"before": before, "after": after},
        "visible_rationale": rationale,
        "rejection_or_omission_retention": retention,
        "current_approval_status": "valid_for_exact_T06_baseline",
        "status": status,
    }


def _ledger(pilot: Path, inputs: dict[str, Any], receipt_bytes: bytes) -> dict[str, Any]:
    raw = {
        "repo_relative_path": inputs["identity"]["raw_path"],
        "sha256": inputs["identity"]["raw_sha256"],
        "size_bytes": inputs["identity"]["raw_size_bytes"],
        "tracked": False,
        "body_embedded": False,
    }
    stages = [
        _stage(
            "T00",
            stage_type="upstream_audio_overview_transcript",
            actor_class="NotebookLM",
            change_class="U_UPSTREAM",
            inputs=[_artifact(pilot, "notebooklm_generation_receipt.json")],
            outputs=[raw],
            before={"source_title_snapshot_count": 11},
            after={"raw_logical_line_count": 326, "raw_size_bytes": 32089},
            semantic_change=True,
            evidence_change=False,
            approval_impact="upstream material requiring downstream verification",
            rationale="Audio Overview was converted to the submitted plain-text transcript.",
            retention="Raw body remains ignored; identity and line fingerprints are retained.",
            status="identity_verified_content_not_reproduced",
        ),
        _stage(
            "T01",
            stage_type="immutable_raw_intake_and_deterministic_salvage",
            actor_class="Worker_mechanical",
            change_class="M_MECHANICAL",
            inputs=[raw],
            outputs=[
                _artifact(pilot, "input_identity_receipt.json"),
                _artifact(pilot, "transcript_quality_readback.json"),
                _artifact(pilot, "asr_correction_ledger.json"),
            ],
            before={"raw_logical_line_count": 326},
            after={"claim_candidate_count": 182},
            semantic_change=False,
            evidence_change=False,
            approval_impact="none; normalization is fingerprinted and raw identity is unchanged",
            rationale="Normalize and salvage deterministically without tracking the raw body.",
            retention="Corrections, rejected spans, and raw line mapping remain in receipts/ignored evidence.",
            status="passed",
        ),
        _stage(
            "T02",
            stage_type="title_level_source_set_freeze",
            actor_class="user",
            change_class="U_UPSTREAM",
            inputs=[_artifact(pilot, "notebooklm_generation_receipt.json")],
            outputs=[
                _artifact(pilot, "source_set_snapshot.json"),
                _artifact(pilot, "notebook_source_to_verification_source_crosswalk.json"),
            ],
            before={"supplied_title_count": 11},
            after={"frozen_title_count": 11},
            semantic_change=False,
            evidence_change=True,
            approval_impact="source-set replacement would require U_UPSTREAM authorization",
            rationale="Freeze supplied titles independently from later factual authority.",
            retention="Unresolved and excluded source identities remain explicit in the snapshot.",
            status="passed_title_level_only",
        ),
        _stage(
            "T03",
            stage_type="official_source_capture_and_claim_adjudication",
            actor_class="Worker_source_verification",
            change_class="S_SEMANTIC",
            inputs=[
                _artifact(pilot, "source_set_snapshot.json"),
                _artifact(pilot, "claim_risk_ledger.json"),
            ],
            outputs=[
                _artifact(pilot, "authoritative_source_registry.json"),
                _artifact(pilot, "source_capture_receipts.json"),
                _artifact(pilot, "claim_adjudication.json"),
                _artifact(pilot, "claim_adjudication_readback.json"),
            ],
            before={"claim_candidate_count": 182},
            after={"verified_primary_count": 19, "outcome_counts": inputs["outcome_counts"]},
            semantic_change=True,
            evidence_change=True,
            approval_impact="claim adoption remains unapproved until T06",
            rationale="Use bounded official evidence to adjudicate every preserved claim once.",
            retention="All rejected, unresolved, context-only, style, and duplicate outcomes remain enumerated.",
            status="passed",
            affected_claim_or_cue_ids="claim_001..claim_182",
        ),
        _stage(
            "T04",
            stage_type="supported_only_constrained_rewrite",
            actor_class="Worker_editorial",
            change_class="S_SEMANTIC",
            secondary_change_classes=["E_EDITORIAL_EVIDENCE_PRESERVING"],
            inputs=[_artifact(pilot, "claim_adjudication.json")],
            outputs=[
                _historical_artifact("canonical_script.json"),
                _historical_artifact("cue_source_traceability.json"),
                _historical_artifact("canonical_yymm4.csv"),
                _historical_artifact("derived_yymm4_import.csv"),
                _historical_artifact("script_generation_receipt.json"),
            ],
            before={"verified_primary_count": 19},
            after={"cue_count": 9, "unique_adopted_claim_count": 17, "factual_units": 22, "claim_edges": 23},
            semantic_change=True,
            evidence_change=False,
            approval_impact="required later human approval",
            rationale="Select supported propositions and rewrite them into a 2/4/3 dialogue structure.",
            retention="Non-adopted claims remain in adjudication; exact T04 bytes are recoverable at the recorded commit.",
            status="superseded_by_T05_but_git_recoverable",
            affected_claim_or_cue_ids="17 adopted claims across cue_001..cue_009",
        ),
        _stage(
            "T05",
            stage_type="editorial_convergence",
            actor_class="Worker_editorial",
            change_class="S_SEMANTIC",
            secondary_change_classes=["E_EDITORIAL_EVIDENCE_PRESERVING"],
            inputs=[_historical_artifact("canonical_script.json"), _historical_artifact("cue_source_traceability.json")],
            outputs=[
                _artifact(pilot, "canonical_script.json"),
                _artifact(pilot, "cue_source_traceability.json"),
                _artifact(pilot, "editorial_revision_receipt.json"),
            ],
            before={"cue_count": 9, "unique_adopted_claim_count": 17, "factual_units": 22, "claim_edges": 23},
            after={"cue_count": 9, "unique_adopted_claim_count": 15, "factual_units": 20, "claim_edges": 21},
            semantic_change=True,
            evidence_change=False,
            approval_impact="T05 result is the exact T06 approval candidate",
            rationale="Improve question/answer flow, terminology, density, endings, and loupe specificity without unsupported facts.",
            retention="claim_158 is retained beside cue_008; claim_095/162/164 remain verified but not adopted.",
            status="passed",
            affected_claim_or_cue_ids="cue_001..cue_009",
        ),
        _stage(
            "T06",
            stage_type="explicit_human_approval",
            actor_class="human_approval",
            change_class="M_MECHANICAL",
            inputs=[_artifact(pilot, name) for name in APPROVED_HASHES],
            outputs=[
                {
                    "repo_relative_path": f"{PILOT_RELATIVE.as_posix()}/human_script_approval_receipt.json",
                    "sha256": _sha256_bytes(receipt_bytes),
                }
            ],
            before={"approval_status": "pending", "cue_count": 9},
            after={"approval_status": "valid", "cue_count": 9},
            semantic_change=False,
            evidence_change=False,
            approval_impact="locks exact commit, files, text, order, scenes, speakers, claims, and CSV projection",
            rationale="Record explicit user option A approval with invalidation and successor rules.",
            retention="The receipt is immutable; a later revision must create a successor receipt.",
            status="valid",
            affected_claim_or_cue_ids="cue_001..cue_009 and 15 adopted claims",
        ),
        _stage(
            "T07",
            stage_type="mechanical_yymm4_projection",
            actor_class="Worker_mechanical",
            change_class="M_MECHANICAL",
            inputs=[_artifact(pilot, "canonical_script.json"), _artifact(pilot, "canonical_yymm4.csv")],
            outputs=[_artifact(pilot, "derived_yymm4_import.csv")],
            before={"canonical_csv_rows": 9, "canonical_speakers": {"れいむ": 3, "まりさ": 6}},
            after={"derived_csv_rows": 9, "yymm4_characters": {"ゆっくり霊夢": 3, "ゆっくり魔理沙": 6}},
            semantic_change=False,
            evidence_change=False,
            approval_impact="approval remains valid only while text/order and all approved hashes remain exact",
            rationale=(
                "Bind the already-created canonical-to-YMM4 speaker projection to the T06 approval lock; "
                "no post-approval CSV regeneration or text change occurred."
            ),
            retention="Canonical and derived CSVs are both retained; runtime observation has not occurred.",
            status="prepared_not_observed",
            affected_claim_or_cue_ids="cue_001..cue_009",
        ),
    ]
    return {
        "schema_version": "content_transformation_lineage.stage_ledger.v1",
        "status": "complete",
        "artifact_family": "new_banknote_source_backed_script_to_yymm4",
        "stage_order": [f"T{i:02d}" for i in range(8)],
        "stages": stages,
        "current_approval_receipt_id": APPROVAL_RECEIPT_ID,
        "current_approval_status": "valid",
        "granularity_boundary": (
            "clause_and_meaning_unit_lineage; no token-level authorship claim"
        ),
    }


def _cue_matrix(inputs: dict[str, Any]) -> dict[str, Any]:
    trace_by_id = {cue["cue_id"]: cue for cue in inputs["trace"]["cues"]}
    rows: list[dict[str, Any]] = []
    for cue in inputs["script"]["cues"]:
        cue_id = cue["cue_id"]
        trace = trace_by_id[cue_id]
        raw_claims = []
        adopted_claims = []
        for claim_id in cue["adopted_claim_ids"]:
            claim = inputs["claim_by_id"][claim_id]
            raw_claims.append(
                {
                    "claim_id": claim_id,
                    "raw_line_ordinal": claim["line_ordinal"],
                    "raw_line_fingerprint": claim["line_fingerprint"],
                    "relationship": "claim_candidate_derived_from_submitted_transcript",
                    "raw_text_embedded": False,
                }
            )
            adopted_claims.append(
                {
                    "claim_id": claim_id,
                    "adjudicated_proposition": claim["adjudicated_proposition"],
                    "evidence_grade": claim["evidence_grade"],
                }
            )
        factual_units = []
        for unit in trace["factual_support_units"]:
            factual_units.append(
                {
                    "unit_id": unit["support_unit_id"],
                    "statement": unit["statement"],
                    "claim_ids": unit["claim_ids"],
                    "supporting_evidence": unit["supporting_evidence"],
                    "source_quote": False,
                    "classification": "verified_factual_paraphrase",
                }
            )
        editorial = [
            {
                **unit,
                "source_quote": False,
                "classification": "worker_editorial_connective",
                "evidence_grade": "inferred_from_final_text_and_revision_receipt",
            }
            for unit in EDITORIAL_UNITS[cue_id]
        ]
        voice = [
            {
                "unit_id": f"{cue_id}_voice_{index:02d}",
                **unit,
                "source_quote": False,
                "classification": "worker_character_voice_phrasing",
                "evidence_grade": "inferred_from_final_text_and_revision_receipt",
            }
            for index, unit in enumerate(VOICE_UNITS[cue_id], start=1)
        ]
        rows.append(
            {
                "cue_id": cue_id,
                "sequence": cue["sequence"],
                "scene": cue["scene_id"],
                "speaker": cue["speaker"],
                "approved_text": cue["text"],
                "approved_text_sha256": hashlib.sha256(cue["text"].encode("utf-8")).hexdigest(),
                "originating_raw_claim_ids": raw_claims,
                "adopted_verified_claims": adopted_claims,
                "official_sources_and_support_locations": trace["supporting_evidence"],
                "factual_paraphrase_units": factual_units,
                "editorial_connective_units": editorial,
                "character_voice_phrasing_units": voice,
                "structural_role": STRUCTURAL_ROLES[cue_id],
                "last_content_changing_stage": LAST_CONTENT_STAGE[cue_id],
                "last_stage_precision": "package-level; token-level last-edit authorship unavailable",
                "omitted_verified_claims_retained_nearby": trace.get("retained_verified_unspoken_claims", []),
                "approval_receipt_id": APPROVAL_RECEIPT_ID,
                "current_approval_validity": True,
                "coverage_boundary": (
                    "factual meaning, editorial connective, voice, and structural role; not token-level attribution"
                ),
            }
        )
    return {
        "schema_version": "content_transformation_lineage.cue_matrix.v1",
        "status": "complete",
        "cue_coverage": "9/9",
        "unique_adopted_claim_count": 15,
        "factual_support_unit_count": 20,
        "claim_edge_count": 21,
        "source_quote_count": 0,
        "token_level_attribution_claimed": False,
        "cues": rows,
    }


def _summary(inputs: dict[str, Any]) -> str:
    outcomes = inputs["outcome_counts"]
    return f"""# 承認済みコンテンツの変更要約

## 提出 transcript は使われたか

はい。提出された NotebookLM Audio Overview transcript は、326 logical lines の immutable raw identity と line fingerprint を起点に 182 claim candidates へ整理されました。最終 cue はその raw claim ID を origin として参照します。ただし、raw transcript は factual authority ではなく、長い原文や token 単位の著者推定もこの package には含めません。

## 何が残り、何が除外されたか

数値 funnel は **326 lines → 182 claim candidates → 19 verified-primary → 15 adopted claims → 20 factual units / 21 evidence edges → 9 cues** です。残った内容 family は、発行年、高精細すき入れ、3D hologram、深凹版印刷、micro文字、識別 mark、額面表示・配置・色の工夫です。

claim outcome は次のとおりです。

| 判定 | 件数 | canonical への影響 |
| --- | ---: | --- |
| verified_primary | {outcomes['verified_primary']} | うち15 unique claimsを採用 |
| supported_context_only | {outcomes['supported_context_only']} | 背景のみ、発話には不採用 |
| unresolved_not_used | {outcomes['unresolved_not_used']} | 未解決のため不採用 |
| rejected_unsupported | {outcomes['rejected_unsupported']} | 一次資料不足で除外 |
| rejected_policy_intent | {outcomes['rejected_policy_intent']} | 政策意図・cashless誘導の推測を除外 |
| rejected_quantitative_without_exact_source | {outcomes['rejected_quantitative_without_exact_source']} | exact sourceのない数値を除外 |
| style_or_rhetoric_only | {outcomes['style_or_rhetoric_only']} | rhetoricとしてのみ保持 |
| duplicate_not_used | {outcomes['duplicate_not_used']} | 重複として不採用 |

verified-primary でも claim_095、claim_158、claim_162、claim_164 は最終発話に採用していません。claim_158 は cue_008 の情報量を抑えるため近接 retention lane に残り、ほかは claim adjudication に残っています。

## Worker が変えたもの

T04 では verified propositions を 2/4/3 scene、れいむ3・まりさ6の9-cue dialogueへ supported-only constrained rewrite しました。これは source quotation ではなく、factual paraphrase と Worker-authored structure / connective / character voice の組合せです。

T05 では opening の question/answer、spoken terminology、cue_008 density、まりさ endings、loupe の具体化を収束させました。cue数は9のまま、factual units は22→20、claim edgesは23→21、unique adopted claimsは17→15になりました。根拠 source identity は変えていません。

## 人が承認したもの

人が新たに本文を書いたとは主張しません。人が行ったのは option A による現在の text、order、scene、casting、CSV projection、claim/source traceability の明示承認です。その exact baseline は `{APPROVED_COMMIT}` と8 file hashesで固定されています。

## 承認を無効にするもの

承認 file の hash、cue text/order/speaker/scene、claim adoption/evidence edge、canonical/derived CSV text/orderのいずれかが変われば承認は無効です。品質向上を理由にした silent fix も認めません。

## 将来変更の出し方

M_MECHANICAL は content hash が不変なら logged validation だけで承認を維持できます。E_EDITORIAL_EVIDENCE_PRESERVING、S_SEMANTIC、U_UPSTREAM は別 revision ID、visible diff、updated ledgerを作り、既存 receipt を上書きせず successor receipt に renewed human approval を記録します。
"""


def _readme() -> str:
    return f"""# New-banknote Content Lineage

> **HUMAN-APPROVED BASELINE — HASH LOCKED — INTERNAL OBSERVATION ONLY**

この page は、提出 transcript から承認済み9-cueと YMM4 CSV までの変換を一か所で確認する primary surface です。提出 transcript は claim discovery と dialogue origin に使われましたが、事実の正本は official primary evidence です。最終文は source quotation ではなく、verified factual paraphrase、Worker editorial connective、character voice、structural roleの組合せです。

## 現在の seal

| 固定対象 | 現在値 | 効く gate |
| --- | --- | --- |
| Approval receipt | `{APPROVAL_RECEIPT_ID}` / valid | 変更時は operator preflight 停止 |
| Approved commit | `{APPROVED_COMMIT}` | successor revision の起点 |
| Cue / scenes | 9 / 2-4-3 | order・scene driftを拒否 |
| Speakers | れいむ3 / まりさ6 | alias projection以外の変更を拒否 |
| Evidence | 15 claims / 20 units / 21 edges | semantic・evidence driftを拒否 |
| YMM4 | 9-row derived CSV prepared | import observation は未実施 |

## 読む順序

1. `content_change_summary.md` — transcript利用と変更内容への直接回答
2. `content_transformation_ledger.json` — T00〜T07 の stage ledger
3. `cue_lineage_matrix.json` — cueごとの raw claim / source / editorial / voice 接続
4. `human_script_approval_receipt.json` — exact approval scope と invalidation
5. `content_change_policy.json` — future change class と renewed approval gate
6. `yymm4_operator_batch/README_OPERATOR_BATCH.md` — 後続の user-operated import observation

## 境界

- raw body、source body、private path、NotebookLM link/UUIDは追跡しません。
- token-by-token origin は既存 evidence から証明できないため主張しません。
- T04 pre-editorial bytesは Git commit `{PRE_EDITORIAL_BASELINE['commit']}` で回収可能です。
- T06後の wording correction はこの branch へ silent patchせず、successor revision と renewed approvalを要求します。
- YMM4 launch、pronunciation acceptance、render、production、publication、rights approval はこの seal に含まれません。
"""


def render_content_lineage_artifacts(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, bytes]:
    """Render the complete deterministic lineage package without writing."""
    pilot = Path(pilot_dir).resolve()
    inputs = _load_inputs(pilot)
    receipt_bytes = _json_bytes(_approval_receipt(inputs))
    policy_bytes = _json_bytes(_content_policy())
    ledger_bytes = _json_bytes(_ledger(pilot, inputs, receipt_bytes))
    matrix_bytes = _json_bytes(_cue_matrix(inputs))
    summary_bytes = _summary(inputs).encode("utf-8")
    readme_bytes = _readme().encode("utf-8")
    base = {
        "human_script_approval_receipt.json": receipt_bytes,
        "README_CONTENT_LINEAGE.md": readme_bytes,
        "content_transformation_ledger.json": ledger_bytes,
        "cue_lineage_matrix.json": matrix_bytes,
        "content_change_summary.md": summary_bytes,
        "content_change_policy.json": policy_bytes,
    }
    matrix = json.loads(matrix_bytes.decode("utf-8"))
    ledger = json.loads(ledger_bytes.decode("utf-8"))
    readback = {
        "schema_version": "content_transformation_lineage.readback.v1",
        "status": "passed",
        "target_state_id": TARGET_STATE_ID,
        "checks": {
            **inputs["contract_checks"],
            "approved_hashes_exact": True,
            "stage_coverage_T00_T07": ledger["stage_order"] == [f"T{i:02d}" for i in range(8)],
            "cue_coverage_9_of_9": matrix["cue_coverage"] == "9/9",
            "adopted_claim_coverage_15": matrix["unique_adopted_claim_count"] == 15,
            "factual_unit_coverage_20": matrix["factual_support_unit_count"] == 20,
            "claim_edge_coverage_21": matrix["claim_edge_count"] == 21,
            "editorial_units_not_source_quotes": all(
                not unit["source_quote"]
                for cue in matrix["cues"]
                for key in ("editorial_connective_units", "character_voice_phrasing_units")
                for unit in cue[key]
            ),
            "token_level_attribution_not_claimed": not matrix["token_level_attribution_claimed"],
            "approval_status_valid": True,
            "raw_body_not_embedded": True,
        },
        "artifact_hashes": {name: _sha256_bytes(data) for name, data in base.items()},
        "approved_file_hashes": inputs["approved_hashes"],
        "approval_receipt_id": APPROVAL_RECEIPT_ID,
        "approval_valid": True,
        "self_hash_recorded": False,
        "yymm4_launched": False,
        "notebooklm_accessed": False,
        "web_fetch_used": False,
    }
    return {**base, "content_lineage_readback.json": _json_bytes(readback)}


def build_content_lineage_package(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, Any]:
    """Write deterministic lineage artifacts without touching approved content."""
    pilot = Path(pilot_dir).resolve()
    artifacts = render_content_lineage_artifacts(pilot)
    for name, data in artifacts.items():
        (pilot / name).write_bytes(data)
    return {
        "status": "content_lineage_sealed",
        "written_files": sorted(artifacts),
        "approved_content_modified": False,
    }


def validate_content_lineage_package(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, Any]:
    """Reject approval or lineage drift without rewriting any artifact."""
    pilot = Path(pilot_dir).resolve()
    try:
        expected = render_content_lineage_artifacts(pilot)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return {
            "schema_version": "content_transformation_lineage.validation.v1",
            "status": "failed",
            "checks": {},
            "failed_checks": [str(exc).splitlines()[0]],
            "approval_valid": False,
        }
    matches = {
        name: (pilot / name).exists() and (pilot / name).read_bytes() == data
        for name, data in expected.items()
    }
    combined = "\n".join(
        (pilot / name).read_text(encoding="utf-8", errors="replace")
        for name in expected
        if (pilot / name).exists()
    )
    checks = {
        "all_lineage_artifacts_byte_exact": all(matches.values()),
        "no_private_absolute_path": _PRIVATE_PATH_RE.search(combined) is None,
        "no_notebooklm_link": "notebooklm.google.com" not in combined.lower(),
        "no_uuid": _UUID_RE.search(combined) is None,
        "no_raw_body_field": all(
            token not in combined for token in ('"raw_text"', '"source_body"', '"transcript_body"')
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    failed.extend(f"lineage_artifact_drift:{name}" for name, passed in matches.items() if not passed)
    failed = list(dict.fromkeys(failed))
    return {
        "schema_version": "content_transformation_lineage.validation.v1",
        "status": "passed" if not failed else "failed",
        "checks": checks,
        "artifact_matches": matches,
        "failed_checks": failed,
        "approval_valid": not failed,
        "approved_content_modified": False,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "validate", "preflight"):
        command = sub.add_parser(name)
        command.add_argument("--pilot", type=Path, default=DEFAULT_PILOT_DIR)
        command.add_argument("--result-json", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "build":
        result = build_content_lineage_package(args.pilot)
    else:
        result = validate_content_lineage_package(args.pilot)
    payload = _json_bytes(result)
    if args.result_json:
        args.result_json.parent.mkdir(parents=True, exist_ok=True)
        args.result_json.write_bytes(payload)
    print(payload.decode("utf-8"), end="")
    return 0 if result.get("status") in {"passed", "content_lineage_sealed"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
