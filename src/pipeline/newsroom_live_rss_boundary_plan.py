"""Plan live RSS boundary gates without implementing live fetch.

This module writes tracked planning artifacts only. It defines the states,
artifact contracts, schemas, gates, and responsibilities needed before any
future diagnostic live RSS smoke. It does not fetch RSS/news, add a real feed,
scrape articles, create YMM4 projects, render, or generate audio/TTS.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_source_boundary_adversarial_fixtures import (
    DEFAULT_ADVERSARIAL_CAPSULE_HARDENING_PATH,
    DEFAULT_ADVERSARIAL_FIXTURES_PATH,
    DEFAULT_ADVERSARIAL_VALIDATION_PATH,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
    _write_json,
    _write_text,
)


PLAN_ID = "newsroom_live_rss_boundary_plan_v1_2026_06_30"
CONTRACT_ID = "newsroom_live_rss_boundary_contract_v1_2026_06_30"
PLAN_SCHEMA_VERSION = "newsroom_live_rss_boundary_plan.v1"
CONTRACT_SCHEMA_VERSION = "newsroom_live_rss_boundary_contract.v1"

DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH = Path(
    "samples/_probe/newsroom_handoff/live_rss_boundary_plan_v1.json"
)
DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH = Path(
    "samples/_probe/newsroom_handoff/live_rss_boundary_contract_v1.json"
)
DEFAULT_LIVE_RSS_BOUNDARY_DOC_PATH = Path(
    "docs/verification/NEWSROOM_LIVE_RSS_BOUNDARY_PLAN_V1_2026-06-30.md"
)

RENDER_GATE = "L0_no_render"
CURRENT_STATE = "live_boundary_planned"
NEXT_RECOMMENDED_AXIS = "newsroom-live-rss-preflight-contract-v1"


def write_default_newsroom_live_rss_boundary_plan_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    adversarial_validation = _load_json_object(base / DEFAULT_ADVERSARIAL_VALIDATION_PATH)
    adversarial_capsule = _load_json_object(
        base / DEFAULT_ADVERSARIAL_CAPSULE_HARDENING_PATH
    )
    contract = build_live_rss_boundary_contract(
        adversarial_validation=adversarial_validation,
        adversarial_capsule=adversarial_capsule,
    )
    plan = build_live_rss_boundary_plan(
        contract=contract,
        adversarial_validation=adversarial_validation,
        adversarial_capsule=adversarial_capsule,
    )
    _write_json(base / DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH, contract)
    _write_json(base / DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH, plan)
    _write_text(
        base / DEFAULT_LIVE_RSS_BOUNDARY_DOC_PATH,
        render_live_rss_boundary_plan_markdown(plan=plan, contract=contract),
    )
    return {"contract": contract, "plan": plan}


def build_live_rss_boundary_contract(
    *,
    adversarial_validation: dict[str, Any],
    adversarial_capsule: dict[str, Any],
) -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID,
        "schema_version": CONTRACT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "render_gate": RENDER_GATE,
        "production_status": "planning_only",
        "live_fetch_used": False,
        "source_adversarial_suite_path": DEFAULT_ADVERSARIAL_FIXTURES_PATH.as_posix(),
        "source_validator_path": DEFAULT_ADVERSARIAL_VALIDATION_PATH.as_posix(),
        "source_capsule_hardening_path": DEFAULT_ADVERSARIAL_CAPSULE_HARDENING_PATH.as_posix(),
        "source_readback": _source_readback(
            adversarial_validation=adversarial_validation,
            adversarial_capsule=adversarial_capsule,
        ),
        "state_machine": _state_machine(),
        "future_live_rss_artifact_contract": _future_live_rss_artifacts(),
        "normalized_live_rss_topic_schema": _normalized_live_rss_topic_schema(),
        "gate_definitions": _gate_definitions(),
        "responsibility_split": _responsibility_split(),
        "risk_register": _risk_register(),
        "boundaries": _closed_boundaries(),
        "not_accepted_scope": _not_accepted_scope(),
    }


def build_live_rss_boundary_plan(
    *,
    contract: dict[str, Any],
    adversarial_validation: dict[str, Any],
    adversarial_capsule: dict[str, Any],
) -> dict[str, Any]:
    decision = _decision_readback(contract)
    return {
        "plan_id": PLAN_ID,
        "schema_version": PLAN_SCHEMA_VERSION,
        "contract_path": DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH.as_posix(),
        "review_status": "ready_for_supervisor_review",
        "render_gate": RENDER_GATE,
        "production_status": "planning_only",
        "live_fetch_used": False,
        "source_adversarial_suite_path": DEFAULT_ADVERSARIAL_FIXTURES_PATH.as_posix(),
        "source_validator_path": DEFAULT_ADVERSARIAL_VALIDATION_PATH.as_posix(),
        "source_capsule_hardening_path": DEFAULT_ADVERSARIAL_CAPSULE_HARDENING_PATH.as_posix(),
        "source_readback": _source_readback(
            adversarial_validation=adversarial_validation,
            adversarial_capsule=adversarial_capsule,
        ),
        "state_machine": contract["state_machine"],
        "artifact_contract": contract["future_live_rss_artifact_contract"],
        "schema_plan": contract["normalized_live_rss_topic_schema"],
        "gate_definitions": contract["gate_definitions"],
        "responsibility_split": contract["responsibility_split"],
        "risk_register": contract["risk_register"],
        "decision_readback": decision,
        "business_goal_outcome_contract": _business_goal_outcome_contract(decision),
        "completion_matrix": _completion_matrix(),
        "inertia_check": _inertia_check(),
        "boundaries": _closed_boundaries(),
        "not_accepted_scope": _not_accepted_scope(),
    }


def render_live_rss_boundary_plan_markdown(
    *,
    plan: dict[str, Any],
    contract: dict[str, Any],
) -> str:
    lines = ["# Newsroom Live RSS Boundary Plan V1"]
    _append_mapping(
        lines,
        "Identity",
        {
            "plan_id": plan["plan_id"],
            "contract_id": contract["contract_id"],
            "source_adversarial_suite_path": plan["source_adversarial_suite_path"],
            "source_validator_path": plan["source_validator_path"],
            "source_capsule_hardening_path": plan["source_capsule_hardening_path"],
            "live_fetch_used": plan["live_fetch_used"],
            "render_gate": plan["render_gate"],
            "production_status": plan["production_status"],
        },
    )
    _append_mapping(lines, "State Machine", plan["state_machine"])
    _append_rows(
        lines,
        "Future Live RSS Artifacts",
        [
            "artifact_name",
            "owner",
            "can_contain_live_source_data",
            "can_be_committed",
            "must_remain_local_ignored",
        ],
        plan["artifact_contract"],
    )
    _append_rows(
        lines,
        "Normalized Topic Schema",
        [
            "field_name",
            "diagnostic_capsule_required",
            "live_boundary_plan_required",
            "production_script_candidate_required",
        ],
        plan["schema_plan"],
    )
    _append_mapping(lines, "Gate Definitions", plan["gate_definitions"])
    _append_mapping(lines, "Responsibility Split", plan["responsibility_split"])
    _append_rows(
        lines,
        "Risk Register",
        ["risk_id", "risk", "blocker", "mitigation", "required_follow_up"],
        plan["risk_register"],
    )
    _append_mapping(lines, "Decision Readback", plan["decision_readback"])
    lines.extend(["", "## Business Goal Outcome Contract"])
    for key, value in plan["business_goal_outcome_contract"].items():
        lines.append(f"- {key}: {value['status']} - {value['rationale']}")
    _append_mapping(lines, "Boundaries", plan["boundaries"])
    return "\n".join(lines).rstrip() + "\n"


def _source_readback(
    *,
    adversarial_validation: dict[str, Any],
    adversarial_capsule: dict[str, Any],
) -> dict[str, Any]:
    validation_summary = adversarial_validation.get("validation_summary", {})
    capsule_summary = adversarial_capsule.get("capsule_hardening_summary", {})
    return {
        "adversarial_total_cases": validation_summary.get("total_cases"),
        "adversarial_unexpected_pass_count": validation_summary.get(
            "unexpected_pass_count"
        ),
        "adversarial_unexpected_fail_count": validation_summary.get(
            "unexpected_fail_count"
        ),
        "adversarial_production_ready_false_count": validation_summary.get(
            "production_ready_false_count"
        ),
        "excluded_claims_used_as_positive_claims_count": capsule_summary.get(
            "excluded_claims_used_as_positive_claims_count"
        ),
        "excluded_claim_misuse_classification": (
            "detected adversarial misuse case; not a production-ready leak"
        ),
        "production_script_ready_true_count": capsule_summary.get(
            "production_script_ready_true_count"
        ),
        "live_boundary_plan_ready_true_count": capsule_summary.get(
            "live_boundary_plan_ready_true_count"
        ),
    }


def _state_machine() -> dict[str, Any]:
    states = [
        "offline_fixture_only",
        "offline_fixture_validated",
        "adversarial_validation_passed",
        "live_boundary_planned",
        "live_fetch_authorized_for_diagnostic_smoke",
        "live_fetch_result_captured",
        "live_source_boundary_validated",
        "diagnostic_capsule_ready",
        "production_script_blocked",
        "production_ready_requires_separate_approval",
    ]
    reached = {
        "offline_fixture_only",
        "offline_fixture_validated",
        "adversarial_validation_passed",
        "live_boundary_planned",
    }
    return {
        "allowed_states": states,
        "current_state": CURRENT_STATE,
        "state_status": [
            {
                "state": state,
                "reached_in_this_slice": state in reached,
                "allowed_to_set_now": state in reached,
            }
            for state in states
        ],
        "forbidden_transitions": [
            {
                "from_state": "live_boundary_planned",
                "to_state": "live_fetch_result_captured",
                "reason": "fetch authorization and receipt contract must exist first",
            },
            {
                "from_state": "adversarial_validation_passed",
                "to_state": "diagnostic_capsule_ready",
                "reason": "a live source boundary validation must be captured first",
            },
            {
                "from_state": "live_boundary_planned",
                "to_state": "production_ready_requires_separate_approval",
                "reason": "production readiness is a separate future approval gate",
            },
            {
                "from_state": "any_state",
                "to_state": "publication_or_public_upload",
                "reason": "publication gate is closed in the current project state",
            },
        ],
        "next_allowed_transition": {
            "from_state": "live_boundary_planned",
            "to_state": "live_fetch_authorized_for_diagnostic_smoke",
            "allowed_now": False,
            "requirements": [
                "explicit future operator authorization",
                "named feed/source target",
                "expected local output directory",
                "fetch receipt schema accepted",
                "no production or publication claim",
            ],
        },
        "transition_requirements": {
            "live_fetch_authorized_for_diagnostic_smoke": [
                "LIVE_FETCH_GATE passes",
                "authorization is recorded in operator_action_log",
            ],
            "live_fetch_result_captured": [
                "fetch_receipt exists",
                "raw_entry_snapshot exists",
                "all live-source artifacts are local/ignored",
            ],
            "live_source_boundary_validated": [
                "SOURCE_BOUNDARY_GATE passes",
                "rights/freshness/attribution/source reliability are classified",
            ],
            "diagnostic_capsule_ready": [
                "CAPSULE_GENERATION_GATE passes",
                "production blockers remain attached to every downstream beat",
            ],
        },
    }


def _future_live_rss_artifacts() -> list[dict[str, Any]]:
    common_local = {
        "can_contain_live_source_data": True,
        "can_be_committed": False,
        "must_remain_local_ignored": True,
    }
    return [
        _artifact(
            "fetch_receipt",
            "Records that an authorized diagnostic fetch occurred and captures timing, target identity, status, and no-production scope.",
            [
                "fetch_receipt_id",
                "authorization_id",
                "feed_id",
                "retrieved_at",
                "tool_version",
                "target_descriptor",
                "result_status",
                "network_scope",
                "production_claim_allowed",
            ],
            "agent after future operator authorization",
            "Blocks every downstream state if missing or if production_claim_allowed is true.",
            **common_local,
        ),
        _artifact(
            "feed_source_manifest",
            "Describes the feed/source target selected for the diagnostic smoke.",
            [
                "feed_id",
                "feed_title",
                "source_name",
                "target_descriptor",
                "authorization_id",
                "allowed_use",
                "retention_policy",
            ],
            "operator/user with agent schema validation",
            "Blocks fetch if target, authorization, or allowed_use is unclear.",
            **common_local,
        ),
        _artifact(
            "raw_entry_snapshot",
            "Stores the exact fetched entry snapshot before normalization.",
            [
                "fetch_receipt_id",
                "entry_id",
                "entry_title",
                "entry_url",
                "entry_published_at",
                "entry_summary_raw",
                "raw_metadata",
            ],
            "agent after future authorization",
            "Blocks normalization if URL, timestamp, or raw title is absent.",
            **common_local,
        ),
        _artifact(
            "normalized_topic_candidate",
            "Converts a raw entry into the schema used by topic/capsule validation.",
            [
                "topic_id",
                "feed_id",
                "entry_title",
                "entry_url",
                "entry_published_at",
                "entry_summary",
                "source_name",
                "retrieved_at",
                "fetch_receipt_id",
            ],
            "agent",
            "Blocks capsule input if required normalized fields are missing.",
            **common_local,
        ),
        _artifact(
            "source_boundary_validation",
            "Classifies whether live source identity, URL, timestamp, and reliability are sufficient for diagnostic use.",
            [
                "topic_id",
                "source_url",
                "entry_published_at",
                "retrieved_at",
                "source_reliability_note",
                "source_truth_approved",
                "production_blockers",
            ],
            "agent classification plus operator review when requested",
            "Blocks production if any placeholder, unknown, or unapproved source boundary remains.",
            **common_local,
        ),
        _artifact(
            "rights_attribution_freshness_readback",
            "Captures rights, attribution, quote/media reuse, and freshness classification.",
            [
                "topic_id",
                "rights_status",
                "attribution_note",
                "freshness_status",
                "quote_media_permission_status",
                "review_required",
                "production_blockers",
            ],
            "operator/user for approval; agent for structured readback",
            "Blocks production when rights, attribution, freshness, or quote/media permission is unknown.",
            **common_local,
        ),
        _artifact(
            "excluded_claims_readback",
            "Lists claims the generator must not assert and records leak checks.",
            [
                "topic_id",
                "excluded_claims",
                "excluded_claim_count",
                "excluded_claims_used_as_positive_claims",
                "leak_check_status",
            ],
            "agent",
            "Blocks capsule readiness if absent or if any excluded claim leaks into positive explanation text.",
            **common_local,
        ),
        _artifact(
            "capsule_input_candidate",
            "Packages the normalized topic plus boundary readbacks for diagnostic capsule generation.",
            [
                "topic_id",
                "normalized_topic_candidate_id",
                "source_boundary_validation_id",
                "rights_readback_id",
                "excluded_claims_readback_id",
                "production_status",
                "diagnostic_capsule_allowed",
            ],
            "agent",
            "Allows diagnostic capsule only; production remains blocked if any blocker remains.",
            **common_local,
        ),
        _artifact(
            "operator_action_log",
            "Records human authorization, review decisions, and explicit non-production scope.",
            [
                "authorization_id",
                "operator",
                "authorized_action",
                "authorized_at",
                "target_descriptor",
                "scope_limit",
                "revocation_or_expiry",
            ],
            "operator/user",
            "Blocks live fetch authorization if absent, ambiguous, expired, or wider than diagnostic smoke.",
            **common_local,
        ),
    ]


def _artifact(
    artifact_name: str,
    purpose: str,
    required_fields: list[str],
    owner: str,
    production_blocker_implications: str,
    *,
    can_contain_live_source_data: bool,
    can_be_committed: bool,
    must_remain_local_ignored: bool,
) -> dict[str, Any]:
    return {
        "artifact_name": artifact_name,
        "purpose": purpose,
        "required_fields": required_fields,
        "owner": owner,
        "can_contain_live_source_data": can_contain_live_source_data,
        "can_be_committed": can_be_committed,
        "must_remain_local_ignored": must_remain_local_ignored,
        "production_blocker_implications": production_blocker_implications,
    }


def _normalized_live_rss_topic_schema() -> list[dict[str, Any]]:
    required_all = {
        "topic_id",
        "feed_id",
        "feed_title",
        "entry_title",
        "entry_url",
        "entry_published_at",
        "entry_summary",
        "source_name",
        "source_url",
        "retrieved_at",
        "fetch_receipt_id",
        "rights_status",
        "attribution_note",
        "freshness_status",
        "source_reliability_note",
        "key_claim_candidates",
        "excluded_claims",
        "uncertainty_or_boundary",
        "intended_episode_angle",
        "production_status",
    }
    live_boundary_required = required_all - {
        "key_claim_candidates",
        "intended_episode_angle",
    }
    fields = [
        ("topic_id", "stable diagnostic topic id"),
        ("feed_id", "source manifest id for the feed or source target"),
        ("feed_title", "operator-facing feed/source label"),
        ("entry_title", "entry title from the captured snapshot"),
        ("entry_url", "canonical entry URL from the captured snapshot"),
        ("entry_published_at", "publisher timestamp from the captured snapshot"),
        ("entry_summary", "normalized summary text from the captured entry"),
        ("source_name", "publisher/source label"),
        ("source_url", "source or entry URL used for boundary validation"),
        ("retrieved_at", "diagnostic retrieval timestamp"),
        ("fetch_receipt_id", "link to the future fetch receipt"),
        ("rights_status", "rights and reuse classification"),
        ("attribution_note", "required attribution/readback note"),
        ("freshness_status", "freshness classification against retrieved_at"),
        ("source_reliability_note", "source reliability classification"),
        ("key_claim_candidates", "candidate claims, not approved assertions"),
        ("excluded_claims", "claims the generator must not assert"),
        ("uncertainty_or_boundary", "source uncertainty and boundary note"),
        ("intended_episode_angle", "diagnostic angle, not production script approval"),
        ("production_status", "must remain diagnostic or blocked until separate approval"),
    ]
    return [
        {
            "field_name": field,
            "purpose": purpose,
            "diagnostic_capsule_required": field in required_all,
            "live_boundary_plan_required": field in live_boundary_required,
            "production_script_candidate_required": field in required_all,
            "placeholder_policy": (
                "forbidden for production; allowed for diagnostic only when explicitly classified"
            ),
        }
        for field, purpose in fields
    ]


def _gate_definitions() -> dict[str, Any]:
    return {
        "LIVE_FETCH_GATE": {
            "status_now": "closed",
            "requires": [
                "explicit future authorization",
                "feed/source target selected by operator",
                "expected local ignored output directory",
                "fetch_receipt schema accepted",
                "no production claim",
            ],
            "allows": ["future diagnostic smoke only"],
            "blocks": ["live fetch implementation now", "production use", "publication"],
        },
        "SOURCE_BOUNDARY_GATE": {
            "status_now": "planned_not_executed",
            "requires": [
                "rights_status classification",
                "freshness_status classification",
                "attribution_note",
                "source_reliability_note",
                "excluded_claims",
                "source URL",
                "published timestamp",
            ],
            "blocks": [
                "production if placeholders remain",
                "production if rights/freshness/source reliability are unknown",
            ],
        },
        "CAPSULE_GENERATION_GATE": {
            "status_now": "planned_not_executed",
            "requires": [
                "source_boundary_validation",
                "rights_attribution_freshness_readback",
                "excluded_claims_readback",
                "capsule_input_candidate",
            ],
            "allows": ["diagnostic capsule with blockers attached"],
            "blocks": ["production capsule when any production blocker remains"],
        },
        "PUBLICATION_GATE": {
            "status_now": "closed",
            "requires": ["separate future approval far beyond this plan"],
            "allows": [],
            "blocks": ["public upload", "public readiness claim", "audience/order acceptance claim"],
        },
    }


def _responsibility_split() -> dict[str, Any]:
    return {
        "agent_owned": [
            "schema definition",
            "validation logic",
            "offline and adversarial tests",
            "readback generation",
            "blocker classification",
            "no-network planning",
        ],
        "operator_user_owned": [
            "explicit authorization for any future live fetch",
            "confirming fetch target/feed if needed",
            "reviewing source/rights/freshness boundary when asked",
            "deciding whether live source usage is acceptable",
        ],
        "forbidden_for_agent_without_explicit_future_authorization": [
            "network fetch",
            "real RSS retrieval",
            "article scraping",
            "rights approval",
            "production/public readiness claims",
        ],
    }


def _risk_register() -> list[dict[str, str]]:
    return [
        _risk("R1", "live fetch network risk", "no network action without LIVE_FETCH_GATE", "keep this slice planning-only", "future explicit authorization"),
        _risk("R2", "source truth risk", "source truth is not approved by fetch existence", "require source_boundary_validation", "operator review if source is ambiguous"),
        _risk("R3", "rights and reuse risk", "unknown rights block production", "require rights_status and quote/media permission readback", "human rights decision"),
        _risk("R4", "quote/media permission risk", "quoted or media material cannot be reused by default", "separate quote_media_permission_status", "operator decision before production"),
        _risk("R5", "freshness/datedness risk", "stale or missing timestamps block live boundary validation", "require entry_published_at and retrieved_at", "freshness policy in preflight"),
        _risk("R6", "hallucinated claim risk", "candidate claims are not approved assertions", "keep key_claim_candidates separate from approved claims", "claim validation before capsule"),
        _risk("R7", "excluded-claim leakage risk", "leak blocks diagnostic capsule readiness", "carry excluded_claims_readback into capsule gate", "repeat adversarial leak check"),
        _risk("R8", "source URL and timestamp absence", "missing URL/timestamp blocks normalization", "require raw_entry_snapshot fields", "preflight schema enforcement"),
        _risk("R9", "attribution ambiguity", "ambiguous attribution blocks production", "require attribution_note", "operator attribution review"),
        _risk("R10", "production/public overclaiming risk", "publication gate remains closed", "production_status remains planning_only or blocked", "separate future approval"),
    ]


def _risk(
    risk_id: str,
    risk: str,
    blocker: str,
    mitigation: str,
    required_follow_up: str,
) -> dict[str, str]:
    return {
        "risk_id": risk_id,
        "risk": risk,
        "blocker": blocker,
        "mitigation": mitigation,
        "required_follow_up": required_follow_up,
    }


def _decision_readback(contract: dict[str, Any]) -> dict[str, Any]:
    artifacts_defined = {
        artifact["artifact_name"]
        for artifact in contract["future_live_rss_artifact_contract"]
    }
    required_artifacts = {
        "fetch_receipt",
        "feed_source_manifest",
        "raw_entry_snapshot",
        "normalized_topic_candidate",
        "source_boundary_validation",
        "rights_attribution_freshness_readback",
        "excluded_claims_readback",
        "capsule_input_candidate",
        "operator_action_log",
    }
    gates = contract["gate_definitions"]
    plan_ready = (
        contract["state_machine"]["current_state"] == CURRENT_STATE
        and required_artifacts.issubset(artifacts_defined)
        and all(name in gates for name in [
            "LIVE_FETCH_GATE",
            "SOURCE_BOUNDARY_GATE",
            "CAPSULE_GENERATION_GATE",
            "PUBLICATION_GATE",
        ])
    )
    return {
        "live_fetch_implementation_allowed_now": False,
        "live_boundary_plan_ready": plan_ready,
        "next_recommended_axis": NEXT_RECOMMENDED_AXIS,
        "next_axis_reason": (
            "the boundary plan is clear; next step is a stricter preflight contract, not live fetch"
        ),
    }


def _business_goal_outcome_contract(decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": True,
            "rationale": "The plan prevents jumping from offline fixtures directly to live fetch.",
        },
        "offer_clear": {
            "status": decision["live_boundary_plan_ready"],
            "rationale": "Future live RSS introduction is governed by states, artifacts, gates, and owners.",
        },
        "proof_clear": {
            "status": True,
            "rationale": "This defines boundary planning only, not implementation.",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "Source, rights, freshness, attribution, production, and publication claims remain blocked.",
        },
        "next_action_clear": {
            "status": True,
            "rationale": decision["next_recommended_axis"],
        },
        "visual_supports_explanation": {
            "status": True,
            "rationale": "YMM4 visual proof stays closed.",
        },
    }


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "repo_state_verified", "status": True},
        {"gate": "adversarial_suite_inspected", "status": True},
        {"gate": "live_rss_boundary_states_defined", "status": True},
        {"gate": "artifact_contract_defined", "status": True},
        {"gate": "gate_definitions_created", "status": True},
        {"gate": "responsibility_split_recorded", "status": True},
        {"gate": "risk_register_created", "status": True},
        {"gate": "next_axis_selected", "status": True},
        {"gate": "no_forbidden_live_visual_media_scope_reopened", "status": True},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "no_live_rss_or_network_fetch", "status": True},
        {"gate": "no_YMM4_visual_loop", "status": True},
        {"gate": "no_animation_only_loop", "status": True},
        {"gate": "no_primitive_or_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "no_production_public_readiness_claim", "status": True},
    ]


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "live_rss_or_news_fetch": False,
        "live_fetch_implementation": False,
        "active_real_feed_source": False,
        "article_scraping": False,
        "production_script_generation": False,
        "production_subtitle_design": False,
        "production_card_design": False,
        "production_animation_quality": False,
        "card_redesign": False,
        "visual_layout_tuning": False,
        "animation_tuning": False,
        "render_export_proof": False,
        "audio_or_tts_output": False,
        "public_upload_or_public_readiness": False,
        "actual_order_or_audience_acceptance": False,
        "source_truth_or_rights_approval": False,
        "local_ymmp_materialization": False,
    }


def _closed_boundaries() -> dict[str, bool]:
    return {
        "network_fetch_performed": False,
        "live_RSS_news_fetch_performed": False,
        "live_feed_source_added": False,
        "fetch_adapter_implemented": False,
        "article_scraping_performed": False,
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "card_redesign_performed": False,
        "animation_tuned": False,
        "local_ignored_ymmp_created_in_this_slice": False,
        "local_ignored_ymmp_modified_in_this_slice": False,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
        "actual_order_or_audience_acceptance_claimed": False,
    }


def _load_json_object(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    write_default_newsroom_live_rss_boundary_plan_artifacts()
