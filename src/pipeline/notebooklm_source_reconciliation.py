"""Deterministic title-level reconciliation for a NotebookLM source snapshot.

This module structures an externally supplied title list and aligns an existing
sanitized claim ledger to likely source families.  It does not select sources,
fetch content, inspect NotebookLM, or verify any claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


SCHEMA_PREFIX = "notebooklm_source_reconciliation.v1"
SOURCE_SET_STATUS = "source_set_frozen_title_level"
EXPECTED_CLAIM_COUNT = 182
EXPECTED_RAW_IDENTITY = {
    "raw_sha256": "1825c9689a050ddbfc91537a228f6af0ba2f7f033e5b681fff4f227551144437",
    "raw_size_bytes": 32089,
    "raw_logical_line_count": 326,
}
PRIMARY_OFFICIAL_CANDIDATE_IDS = ("S04", "S05", "S10", "S11")
GENERATION_TIME_SOURCE_IDS = (
    "S01",
    "S02",
    "S03",
    "S04",
    "S05",
    "S06",
    "S08",
    "S09",
    "S10",
    "S11",
)
DERIVED_SOURCE_IDS = ("S07",)
REQUIRED_SOURCE_FIELDS = (
    "source_id",
    "exact_title",
    "normalized_title",
    "title_fingerprint",
    "chronology_class",
    "chronology_confidence",
    "authority_class",
    "authority_confidence",
    "publisher_label",
    "URL_status",
    "stable_identifier_status",
    "generation_role",
    "factual_authority_policy",
    "allowed_use",
    "forbidden_use",
    "notes",
)
REQUIRED_SOURCE_RECONCILIATION_FILES = (
    "README_SOURCE_RECONCILIATION.md",
    "source_set_snapshot.json",
    "source_authority_matrix.json",
    "source_chronology_readback.json",
    "derived_source_exclusion.json",
    "source_set_reconciliation_readback.json",
    "source_resolution_backlog.json",
    "claim_source_family_alignment.json",
    "source_set_limitations.md",
)
ALIGNMENT_RECORD_FIELDS = {
    "claim_id",
    "line_ordinal",
    "line_fingerprint",
    "claim_class",
    "risk_class",
    "topic_family_labels",
    "likely_source_ids",
    "derived_provenance_source_ids",
    "required_authority_class",
    "verification_status",
    "source_resolution_dependency",
    "reject_if_unverified",
    "rationale_label",
}

TOPIC_FAMILY_SOURCE_IDS: dict[str, tuple[str, ...]] = {
    "anti_counterfeit_technology": ("S04", "S05", "S06"),
    "portrait_design_selection": ("S10",),
    "accessibility_identification": ("S04", "S11"),
    "cashless_policy_intent": ("S01", "S02", "S03", "S08", "S09"),
    "history_keyword": ("S01", "S04", "S08", "S09"),
}

_TOPIC_FAMILY_PATTERNS: dict[str, tuple[str, ...]] = {
    "anti_counterfeit_technology": (
        r"ホログラム|偽造|透かし|凹版|マイクロ|印刷|コピー(?:機)?|スキャナ(?:ー)?|レーザー",
    ),
    "portrait_design_selection": (
        r"肖像|図柄|渋沢|津田|北里",
    ),
    "accessibility_identification": (
        r"識別|触覚|視覚|額面|数字|ユニバーサル|バリアフリー|マーク|アプリ",
    ),
    "cashless_policy_intent": (
        r"キャッシュレス|現金離れ|電子決済|デジタル決済|スマホ決済|QR(?:コード)?決済",
    ),
    "history_keyword": (
        r"歴史|改刷|刷新|年ぶり|年前|世紀|江戸|明治|大正|昭和|平成|令和|1000年|千年",
    ),
}


@dataclass(frozen=True)
class SourceSpec:
    """One title-level source supplied outside this repository."""

    source_id: str
    exact_title: str
    chronology_class: str
    chronology_confidence: str
    authority_class: str
    authority_confidence: str
    publisher_label: str
    generation_role: str
    factual_authority_policy: str
    allowed_use: tuple[str, ...]
    forbidden_use: tuple[str, ...]
    notes: tuple[str, ...]
    URL_status: str = "not_provided"
    stable_identifier_status: str = "not_provided"


@dataclass(frozen=True)
class ClaimFamilyRule:
    likely_source_ids: tuple[str, ...]
    required_authority_class: str
    source_resolution_dependency: str
    rationale_label: str


USER_PROVIDED_SOURCE_SNAPSHOT: tuple[SourceSpec, ...] = (
    SourceSpec(
        source_id="S01",
        exact_title="【新紙幣を完全解説】世界初の3Dホログラムで偽造防止、キャッシュレス化のなか新紙幣の効果とは - JBpress",
        chronology_class="generation_time",
        chronology_confidence="user_provided",
        authority_class="secondary_journalism_anchor",
        authority_confidence="provisional_title_only",
        publisher_label="JBpress",
        generation_role="generation_context_anchor",
        factual_authority_policy="secondary_context_only",
        allowed_use=("context_discovery", "claim_origin_tracing"),
        forbidden_use=("sole_factual_verification", "government_intent_verification"),
        notes=("content_not_inspected",),
    ),
    SourceSpec(
        source_id="S02",
        exact_title='このタイミングで新紙幣発表"本当の狙い" キャッシュレス化とは矛盾しない',
        chronology_class="generation_time",
        chronology_confidence="user_provided",
        authority_class="secondary_commentary_publisher_unresolved",
        authority_confidence="provisional_title_only",
        publisher_label="unresolved",
        generation_role="generation_framing_input",
        factual_authority_policy="secondary_framing_only",
        allowed_use=("framing_origin_tracing", "publisher_resolution"),
        forbidden_use=("sole_factual_verification", "policy_intent_verification"),
        notes=("publisher_unresolved", "content_not_inspected"),
    ),
    SourceSpec(
        source_id="S03",
        exact_title="テーマ：新紙幣の経済的影響とキャッシュレス化",
        chronology_class="generation_time_candidate",
        chronology_confidence="provisional_user_provided",
        authority_class="notebooklm_generated_synthesis_or_user_note_candidate",
        authority_confidence="provisional_origin_unresolved",
        publisher_label="not_applicable_or_unresolved",
        generation_role="generation_synthesis_or_user_note",
        factual_authority_policy="non_independent_excluded_from_factual_verification",
        allowed_use=("generation_context", "provenance_resolution"),
        forbidden_use=("independent_factual_verification", "policy_intent_verification"),
        notes=("non_independent_authority", "origin_type_unresolved"),
    ),
    SourceSpec(
        source_id="S04",
        exact_title="新しい日本銀行券 「開発秘話」 - 国立印刷局",
        chronology_class="generation_time",
        chronology_confidence="user_provided",
        authority_class="primary_official_candidate",
        authority_confidence="provisional_title_only",
        publisher_label="国立印刷局",
        generation_role="generation_official_evidence_candidate",
        factual_authority_policy="candidate_pending_identity_and_content_verification",
        allowed_use=("official_identity_resolution", "future_claim_verification_candidate"),
        forbidden_use=("verified_use_before_identity_and_content_resolution",),
        notes=("content_not_inspected",),
    ),
    SourceSpec(
        source_id="S05",
        exact_title="新しい日本銀行券の偽造防止技術 [PDF 572KB]",
        chronology_class="generation_time",
        chronology_confidence="user_provided",
        authority_class="primary_official_candidate",
        authority_confidence="provisional_title_only",
        publisher_label="official_publisher_unresolved",
        generation_role="generation_official_evidence_candidate",
        factual_authority_policy="candidate_pending_identity_and_content_verification",
        allowed_use=("official_identity_resolution", "future_claim_verification_candidate"),
        forbidden_use=("verified_use_before_identity_and_content_resolution",),
        notes=("publisher_requires_resolution", "content_not_inspected"),
    ),
    SourceSpec(
        source_id="S06",
        exact_title="新紙幣に採用された3Dホログラムとホログラム映像 何が違う？ - ユピテル",
        chronology_class="generation_time",
        chronology_confidence="user_provided",
        authority_class="secondary_corporate_technical_explainer",
        authority_confidence="provisional_title_only",
        publisher_label="ユピテル",
        generation_role="generation_technical_context",
        factual_authority_policy="secondary_technical_context_only",
        allowed_use=("technical_context", "claim_origin_tracing"),
        forbidden_use=("sole_official_feature_verification",),
        notes=("content_not_inspected",),
    ),
    SourceSpec(
        source_id="S07",
        exact_title="新紙幣に隠されたキャッシュレスの罠.m4a",
        chronology_class="post_generation_derived",
        chronology_confidence="user_provided",
        authority_class="derived_audio_overview",
        authority_confidence="excluded_by_chronology",
        publisher_label="derived_audio_overview",
        generation_role="post_generation_audio_output",
        factual_authority_policy="excluded",
        allowed_use=("derived_style_and_dialogue_provenance",),
        forbidden_use=("factual_support", "generation_time_source_membership"),
        notes=("post_generation_derived", "never_independent_factual_authority"),
        URL_status="not_applicable",
        stable_identifier_status="not_tracked",
    ),
    SourceSpec(
        source_id="S08",
        exact_title="注目のキーワード「改刷」",
        chronology_class="generation_time",
        chronology_confidence="user_provided",
        authority_class="publisher_unresolved_title_only",
        authority_confidence="provisional_title_only",
        publisher_label="unresolved",
        generation_role="generation_keyword_context",
        factual_authority_policy="excluded_until_publisher_and_content_resolution",
        allowed_use=("publisher_resolution", "history_keyword_origin_tracing"),
        forbidden_use=("factual_verification_before_resolution",),
        notes=("publisher_unresolved", "content_not_inspected"),
    ),
    SourceSpec(
        source_id="S09",
        exact_title="紙切れを価値に変える1000年の知略：3Dホログラムが描く偽造防止の最前線 - note",
        chronology_class="generation_time",
        chronology_confidence="user_provided",
        authority_class="tertiary_user_published_commentary",
        authority_confidence="provisional_title_only",
        publisher_label="note",
        generation_role="generation_narrative_context",
        factual_authority_policy="tertiary_narrative_inspiration_only",
        allowed_use=("narrative_origin_tracing", "editorial_inspiration"),
        forbidden_use=("sole_factual_verification", "policy_intent_verification"),
        notes=("content_not_inspected",),
    ),
    SourceSpec(
        source_id="S10",
        exact_title="紙幣の肖像と図柄について、選定理由を教えてください - 財務省",
        chronology_class="generation_time",
        chronology_confidence="user_provided",
        authority_class="primary_official_candidate",
        authority_confidence="provisional_title_only",
        publisher_label="財務省",
        generation_role="generation_official_evidence_candidate",
        factual_authority_policy="candidate_pending_identity_and_content_verification",
        allowed_use=("official_identity_resolution", "future_claim_verification_candidate"),
        forbidden_use=("verified_use_before_identity_and_content_resolution",),
        notes=("content_not_inspected",),
    ),
    SourceSpec(
        source_id="S11",
        exact_title="識別性向上に向けた取組 - 国立印刷局",
        chronology_class="generation_time",
        chronology_confidence="user_provided",
        authority_class="primary_official_candidate",
        authority_confidence="provisional_title_only",
        publisher_label="国立印刷局",
        generation_role="generation_official_evidence_candidate",
        factual_authority_policy="candidate_pending_identity_and_content_verification",
        allowed_use=("official_identity_resolution", "future_claim_verification_candidate"),
        forbidden_use=("verified_use_before_identity_and_content_resolution",),
        notes=("content_not_inspected",),
    ),
)


CLAIM_FAMILY_RULES: dict[str, ClaimFamilyRule] = {
    "technical_description": ClaimFamilyRule(
        likely_source_ids=("S04", "S05", "S06", "S10", "S11"),
        required_authority_class="primary_official_or_original_technical_source",
        source_resolution_dependency=(
            "resolve_official_candidate_identity_and_exact_feature_location"
        ),
        rationale_label="technical_subfamily_unresolved_family_union",
    ),
    "quantitative_statistic": ClaimFamilyRule(
        likely_source_ids=(),
        required_authority_class="exact_primary_or_empirical_source",
        source_resolution_dependency=(
            "resolve_exact_source_identity_page_or_field_publication_date_and_unit"
        ),
        rationale_label="quantitative_exact_source_required",
    ),
    "historical_claim": ClaimFamilyRule(
        likely_source_ids=("S01", "S04", "S08", "S09"),
        required_authority_class="primary_official_or_scholarly_source",
        source_resolution_dependency=(
            "resolve_primary_history_source_and_S08_publisher_if_used"
        ),
        rationale_label="history_family_provisional_S08_unresolved",
    ),
    "policy_or_intent_claim": ClaimFamilyRule(
        likely_source_ids=("S01", "S02", "S03", "S08", "S09"),
        required_authority_class="independent_primary_or_empirical_source",
        source_resolution_dependency=(
            "resolve_framing_origins_then_obtain_independent_authoritative_or_empirical_evidence"
        ),
        rationale_label="policy_framing_origins_not_authority",
    ),
    "causal_claim": ClaimFamilyRule(
        likely_source_ids=(),
        required_authority_class="independent_primary_or_empirical_source",
        source_resolution_dependency=(
            "resolve_topic_then_obtain_independent_authoritative_or_empirical_evidence"
        ),
        rationale_label="causal_topic_unresolved_independent_evidence_required",
    ),
    "analogy_or_metaphor": ClaimFamilyRule(
        likely_source_ids=(),
        required_authority_class="none_for_clearly_labeled_editorial_use",
        source_resolution_dependency="editorial_review_only_no_factual_support",
        rationale_label="editorial_analogy_not_factual_support",
    ),
    "rhetorical_framing": ClaimFamilyRule(
        likely_source_ids=(),
        required_authority_class="none_for_clearly_labeled_editorial_use",
        source_resolution_dependency="editorial_review_only_no_factual_support",
        rationale_label="derived_dialogue_review_not_factual_support",
    ),
    "future_prediction": ClaimFamilyRule(
        likely_source_ids=(),
        required_authority_class="primary_or_empirical_source_with_time_scope",
        source_resolution_dependency=(
            "resolve_attribution_time_scope_and_primary_or_empirical_basis"
        ),
        rationale_label="prediction_basis_unresolved",
    ),
    "unsupported_dramatic_assertion": ClaimFamilyRule(
        likely_source_ids=("S01", "S02", "S03", "S08", "S09"),
        required_authority_class="independent_primary_source",
        source_resolution_dependency=(
            "resolve_framing_origin_then_obtain_independent_evidence"
        ),
        rationale_label="dramatic_framing_origins_not_authority",
    ),
}

_PRIVATE_PATTERN = re.compile(
    r"(?:https?://)?notebooklm\.google\.com(?:/|\b)|"
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b|"
    r"[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]|"
    r"/(?:Users|home)/",
    flags=re.IGNORECASE,
)
_FORBIDDEN_CONTENT_KEYS = {"raw_text", "claim_text", "transcript_text", "excerpt"}


def normalize_source_title(title: str) -> str:
    """Normalize a source title without dropping punctuation or merging titles."""

    normalized = unicodedata.normalize("NFKC", title).casefold()
    return re.sub(r"\s+", " ", normalized).strip()


def source_title_fingerprint(title: str) -> str:
    """Return SHA-256 of the normalized UTF-8 title."""

    return hashlib.sha256(normalize_source_title(title).encode("utf-8")).hexdigest()


def _source_record(spec: SourceSpec) -> dict[str, Any]:
    normalized_title = normalize_source_title(spec.exact_title)
    return {
        "source_id": spec.source_id,
        "exact_title": spec.exact_title,
        "normalized_title": normalized_title,
        "title_fingerprint": hashlib.sha256(
            normalized_title.encode("utf-8")
        ).hexdigest(),
        "chronology_class": spec.chronology_class,
        "chronology_confidence": spec.chronology_confidence,
        "authority_class": spec.authority_class,
        "authority_confidence": spec.authority_confidence,
        "publisher_label": spec.publisher_label,
        "URL_status": spec.URL_status,
        "stable_identifier_status": spec.stable_identifier_status,
        "generation_role": spec.generation_role,
        "factual_authority_policy": spec.factual_authority_policy,
        "allowed_use": list(spec.allowed_use),
        "forbidden_use": list(spec.forbidden_use),
        "notes": list(spec.notes),
    }


def _source_set_fingerprint(records: Sequence[dict[str, Any]]) -> str:
    canonical = "\n".join(
        f"{record['source_id']}\0{record['title_fingerprint']}" for record in records
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_claim_ledger(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    ledger = json.loads(raw.decode("utf-8"))
    claims = ledger.get("claims")
    if not isinstance(claims, list):
        raise ValueError("claim ledger must contain a claims list")
    if ledger.get("claim_candidate_count") != len(claims):
        raise ValueError("claim ledger declared count does not match its records")
    if len(claims) != EXPECTED_CLAIM_COUNT:
        raise ValueError(
            f"expected {EXPECTED_CLAIM_COUNT} claim candidates, got {len(claims)}"
        )
    required = {
        "claim_id",
        "line_ordinal",
        "line_fingerprint",
        "claim_class",
        "risk",
        "verified",
        "source_verification_required",
    }
    claim_ids: list[str] = []
    for claim in claims:
        missing = required - set(claim)
        if missing:
            raise ValueError(f"claim record missing fields: {sorted(missing)}")
        if claim["claim_class"] not in CLAIM_FAMILY_RULES:
            raise ValueError(f"unsupported claim class: {claim['claim_class']}")
        if claim["verified"] is not False:
            raise ValueError(f"claim must remain unverified: {claim['claim_id']}")
        if not re.fullmatch(r"[0-9a-f]{64}", claim["line_fingerprint"]):
            raise ValueError(f"invalid claim fingerprint: {claim['claim_id']}")
        claim_ids.append(claim["claim_id"])
    if len(set(claim_ids)) != len(claim_ids):
        raise ValueError("claim_id must be the unique alignment key")
    if ledger.get("verified_claim_count") != 0:
        raise ValueError("claim ledger verified count must remain zero")
    high_risk_classes = {
        "quantitative_statistic",
        "policy_or_intent_claim",
        "causal_claim",
    }
    if any(
        claim["risk"] != "high"
        for claim in claims
        if claim["claim_class"] in high_risk_classes
    ):
        raise ValueError("quantitative, policy, and causal claims must remain high risk")
    return ledger, hashlib.sha256(raw).hexdigest()


def _load_raw_identity(path: Path) -> dict[str, Any]:
    receipt = _load_json(path)
    for key, expected in EXPECTED_RAW_IDENTITY.items():
        if receipt.get(key) != expected:
            raise ValueError(f"raw identity drift for {key}")
    if receipt.get("raw_modified") is not False or receipt.get("raw_tracked") is not False:
        raise ValueError("raw transcript immutable/untracked boundary changed")
    return {key: receipt[key] for key in EXPECTED_RAW_IDENTITY}


def _line_topic_families(text: str) -> tuple[str, ...]:
    return tuple(
        family
        for family, patterns in _TOPIC_FAMILY_PATTERNS.items()
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)
    )


def _load_line_topic_labels(
    path: Path,
    claims: Sequence[dict[str, Any]],
) -> tuple[dict[tuple[int, str], tuple[str, ...]], dict[str, Any]]:
    raw = path.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    if payload.get("raw_sha256") != EXPECTED_RAW_IDENTITY["raw_sha256"]:
        raise ValueError("local line-map raw identity mismatch")
    lines = payload.get("lines")
    if not isinstance(lines, list) or len(lines) != EXPECTED_RAW_IDENTITY[
        "raw_logical_line_count"
    ]:
        raise ValueError("local line-map coverage mismatch")
    if payload.get("logical_line_count") != EXPECTED_RAW_IDENTITY[
        "raw_logical_line_count"
    ]:
        raise ValueError("local line-map declared count mismatch")
    ordinals = [line.get("ordinal") for line in lines if isinstance(line, dict)]
    if ordinals != list(range(1, EXPECTED_RAW_IDENTITY["raw_logical_line_count"] + 1)):
        raise ValueError("local line-map ordinals must be unique and sequential")
    for line in lines:
        text = line.get("raw_text")
        fingerprint = line.get("fingerprint")
        if not isinstance(text, str) or not isinstance(fingerprint, str):
            raise ValueError("local line-map text or fingerprint is missing")
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != fingerprint:
            raise ValueError(f"local line-map raw_text fingerprint mismatch at {line['ordinal']}")
    by_ordinal = {line.get("ordinal"): line for line in lines}
    labels: dict[tuple[int, str], tuple[str, ...]] = {}
    for claim in claims:
        line = by_ordinal.get(claim["line_ordinal"])
        if not isinstance(line, dict):
            raise ValueError(f"claim line missing from local line map: {claim['claim_id']}")
        if line.get("fingerprint") != claim["line_fingerprint"]:
            raise ValueError(f"claim line fingerprint mismatch: {claim['claim_id']}")
        text = line.get("raw_text")
        if not isinstance(text, str):
            raise ValueError(f"local line text missing: {claim['claim_id']}")
        key = (claim["line_ordinal"], claim["line_fingerprint"])
        labels[key] = _line_topic_families(text)
    return labels, {
        "mode": "fingerprint_verified_local_line_map_lexical_labels",
        "local_line_map_used": True,
        "line_map_sha256": hashlib.sha256(raw).hexdigest(),
        "line_map_logical_line_count": len(lines),
        "claim_line_coverage": len(claims),
        "claim_text_tracked": False,
    }


def _topic_source_ids(
    claim_class: str,
    topic_families: Sequence[str],
) -> set[str]:
    if claim_class in {"analogy_or_metaphor", "rhetorical_framing"}:
        return set()
    applicable_topics = set(topic_families)
    if claim_class == "technical_description":
        applicable_topics &= {
            "anti_counterfeit_technology",
            "portrait_design_selection",
            "accessibility_identification",
        }
    elif claim_class == "policy_or_intent_claim":
        applicable_topics &= {"cashless_policy_intent"}
    source_ids: set[str] = set()
    for topic in applicable_topics:
        source_ids.update(TOPIC_FAMILY_SOURCE_IDS[topic])
    return source_ids


def _claim_alignments(
    claims: Sequence[dict[str, Any]],
    line_topic_labels: dict[tuple[int, str], tuple[str, ...]],
) -> list[dict[str, Any]]:
    alignments: list[dict[str, Any]] = []
    for claim in claims:
        rule = CLAIM_FAMILY_RULES[claim["claim_class"]]
        key = (claim["line_ordinal"], claim["line_fingerprint"])
        topic_families = list(line_topic_labels.get(key, ()))
        if (
            claim["claim_class"] == "policy_or_intent_claim"
            and "cashless_policy_intent" not in topic_families
        ):
            topic_families.append("cashless_policy_intent")
        if (
            claim["claim_class"] == "historical_claim"
            and "history_keyword" not in topic_families
        ):
            topic_families.append("history_keyword")
        likely_source_ids = _topic_source_ids(claim["claim_class"], topic_families)
        topic_based = bool(likely_source_ids)
        if not likely_source_ids and claim["claim_class"] not in {
            "quantitative_statistic",
            "causal_claim",
            "future_prediction",
            "analogy_or_metaphor",
            "rhetorical_framing",
        }:
            likely_source_ids.update(rule.likely_source_ids)
        rationale = rule.rationale_label
        if topic_based:
            rationale += "_with_lexical_topic_labels"
        derived_provenance = (
            ["S07"]
            if claim["claim_class"]
            in {
                "analogy_or_metaphor",
                "rhetorical_framing",
            }
            else []
        )
        alignments.append(
            {
                "claim_id": claim["claim_id"],
                "line_ordinal": claim["line_ordinal"],
                "line_fingerprint": claim["line_fingerprint"],
                "claim_class": claim["claim_class"],
                "risk_class": claim["risk"],
                "topic_family_labels": topic_families,
                "likely_source_ids": sorted(likely_source_ids),
                "derived_provenance_source_ids": derived_provenance,
                "required_authority_class": rule.required_authority_class,
                "verification_status": "unverified",
                "source_resolution_dependency": rule.source_resolution_dependency,
                "reject_if_unverified": bool(claim["source_verification_required"]),
                "rationale_label": rationale,
            }
        )
    return alignments


def _readme(
    records: Sequence[dict[str, Any]],
    alignment_count: int,
) -> str:
    rows = "\n".join(
        "| {source_id} | {chronology_class} | {authority_class} | "
        "{factual_authority_policy} | {exact_title} |".format(**record)
        for record in records
    )
    return f"""# New-banknote NotebookLM source reconciliation

The externally supplied source list is frozen here at title level. All 11 titles are preserved verbatim under stable IDs S01-S11, with deterministic normalized-title fingerprints. Ten entries are generation-time candidates. S07 is a post-generation Audio Overview file and is excluded from factual authority. No NotebookLM page or source content was accessed.

This freeze does not establish factual truth. S04, S05, S10, and S11 are primary-official candidates pending URL or stable-identifier and content resolution. S03 remains a non-independent synthesis or user-note candidate. Journalism, commentary, corporate explanation, unresolved titles, and tertiary material may trace framing or context but cannot substitute for the required independent authority.

| ID | Chronology | Authority class | Factual-use policy | Exact supplied title |
| --- | --- | --- | --- | --- |
{rows}

The existing {alignment_count}-record claim ledger is aligned one-for-one in `claim_source_family_alignment.json`; verified claims remain zero. The ignored line map was hash-recomputed and fingerprint-matched to every claim reference, then used only to emit compact lexical topic labels; no transcript text was copied. Those labels separate anti-counterfeit technology, portrait/design selection, accessibility/identification, cashless/policy framing, and history-keyword families. This is routing metadata, not support or verification. Policy-intent and cashless-causation claims still require independent authoritative or empirical evidence. Every quantitative claim requires an exact original source identity plus page or field, publication date, and unit.

The next gate is authoritative source resolution: identify S04, S05, S10, and S11 first, capture stable identifiers and content identity, then resolve context sources without treating S03 or S07 as independent evidence. `source_resolution_backlog.json` defines the minimum evidence. No final script, speaker casting, CSV, YMM4 artifact, render, editorial adoption, rights approval, or publication follows from this package.
"""


def _limitations() -> str:
    return """# Source-set reconciliation limitations

| Debt | Impact | Owner | Revisit trigger | Blocker status |
| --- | --- | --- | --- | --- |
| Ten generation-time entries lack URL or stable document identity | Exact documents cannot be inspected or cited | Authoritative-source resolution successor | Stable URLs or identifiers are available | H1 blocker; not an H0 blocker |
| S02 and S08 publishers are unresolved; S05 publisher identity still needs evidence | Authority classification cannot be finalized | Source-resolution successor | Publisher and publication metadata are captured | H1 blocker for using those entries |
| S03 may be NotebookLM synthesis or a user note | It cannot serve as independent evidence in either case | Provenance-resolution successor | Origin type or stable note identity is available | Not an H0 blocker; excluded as authority |
| Lexical topic labels do not establish semantic support | Anti-counterfeit, portrait/design, accessibility, cashless/policy, and history routing still needs exact source locations | Claim-verification successor | Source contents and claim support locations are resolved | H2 blocker; not an H0 blocker |
| No source content was inspected | All 182 claims remain unverified and canonical script shaping stays closed | Claim-verification successor | Captured source identity and exact support locations exist | H2/H3 blocker |
"""


def _contains_forbidden_content_key(value: Any) -> bool:
    if isinstance(value, dict):
        if _FORBIDDEN_CONTENT_KEYS & set(value):
            return True
        return any(_contains_forbidden_content_key(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_content_key(item) for item in value)
    return False


def build_notebooklm_source_reconciliation(
    *,
    claim_ledger_path: Path,
    output_dir: Path,
    source_snapshot: Sequence[SourceSpec] = USER_PROVIDED_SOURCE_SNAPSHOT,
    input_identity_receipt_path: Path | None = None,
    local_line_map_path: Path | None = None,
) -> dict[str, Any]:
    """Build the sanitized title-level source package and validate it."""

    claim_ledger_path = Path(claim_ledger_path)
    output_dir = Path(output_dir)
    identity_path = input_identity_receipt_path or (
        claim_ledger_path.parent / "input_identity_receipt.json"
    )
    raw_identity = _load_raw_identity(Path(identity_path))
    ledger, ledger_sha256 = _load_claim_ledger(claim_ledger_path)
    if local_line_map_path is None:
        candidate_line_map = claim_ledger_path.parent / "local_outputs/raw_line_map.json"
        local_line_map_path = candidate_line_map if candidate_line_map.is_file() else None
    if local_line_map_path is None:
        raise ValueError(
            "canonical source reconciliation requires the ignored local raw_line_map.json"
        )
    line_topic_labels, topic_labeling = _load_line_topic_labels(
        Path(local_line_map_path),
        ledger["claims"],
    )
    records = [_source_record(spec) for spec in source_snapshot]
    source_ids = [record["source_id"] for record in records]
    if source_ids != [f"S{index:02d}" for index in range(1, 12)]:
        raise ValueError("source IDs must be exactly S01-S11 in order")
    if len({record["exact_title"] for record in records}) != 11:
        raise ValueError("exact titles must not be omitted, merged, or duplicated")
    if len({record["title_fingerprint"] for record in records}) != 11:
        raise ValueError("normalized title fingerprints must be unique")
    alignments = _claim_alignments(ledger["claims"], line_topic_labels)
    source_set_fingerprint = _source_set_fingerprint(records)

    snapshot = {
        "schema_version": f"{SCHEMA_PREFIX}.source_set_snapshot",
        "status": SOURCE_SET_STATUS,
        "snapshot_basis": "externally_supplied_title_list",
        "source_selection_performed": False,
        "source_content_inspected": False,
        "source_count": len(records),
        "source_set_fingerprint": source_set_fingerprint,
        "title_normalization_contract": "NFKC_then_casefold_then_whitespace_collapse",
        "title_fingerprint_contract": "sha256_of_normalized_utf8",
        "notebook_reference_supplied": True,
        "notebook_reference_access_verified": False,
        "notebook_reference_tracked": False,
        "sources": records,
    }
    authority_matrix = {
        "schema_version": f"{SCHEMA_PREFIX}.source_authority_matrix",
        "status": "title_level_authority_classification_provisional",
        "primary_official_candidate_source_ids": list(PRIMARY_OFFICIAL_CANDIDATE_IDS),
        "non_independent_source_ids": ["S03"],
        "excluded_from_factual_authority_source_ids": ["S03", "S07"],
        "entries": [
            {
                key: record[key]
                for key in (
                    "source_id",
                    "authority_class",
                    "authority_confidence",
                    "generation_role",
                    "factual_authority_policy",
                    "allowed_use",
                    "forbidden_use",
                )
            }
            for record in records
        ],
    }
    chronology = {
        "schema_version": f"{SCHEMA_PREFIX}.source_chronology_readback",
        "status": "chronology_frozen_title_level",
        "generation_time_count": len(GENERATION_TIME_SOURCE_IDS),
        "generation_time_source_ids": list(GENERATION_TIME_SOURCE_IDS),
        "strict_generation_time_source_ids": [
            source_id for source_id in GENERATION_TIME_SOURCE_IDS if source_id != "S03"
        ],
        "provisional_generation_time_source_ids": ["S03"],
        "post_generation_derived_count": len(DERIVED_SOURCE_IDS),
        "post_generation_derived_source_ids": list(DERIVED_SOURCE_IDS),
        "raw_transcript": {
            "artifact_class": "post_generation_derived_transcript",
            "included_in_source_set": False,
            "factual_authority_policy": "excluded",
            **raw_identity,
        },
        "notebook_reference_supplied": True,
        "notebook_reference_access_verified": False,
        "notebook_reference_tracked": False,
    }
    derived_exclusion = {
        "schema_version": f"{SCHEMA_PREFIX}.derived_source_exclusion",
        "status": "derived_material_excluded_from_factual_authority",
        "excluded_source_ids": ["S07"],
        "excluded_sources": [
            {
                "source_id": "S07",
                "chronology_class": "post_generation_derived",
                "allowed_use": ["derived_style_and_dialogue_provenance"],
                "factual_authority_use": False,
                "generation_time_evidence_use": False,
            }
        ],
        "other_derived_artifacts": [
            {
                "artifact_id": "raw_transcript",
                "artifact_class": "post_generation_derived_transcript",
                "included_in_source_set": False,
                "factual_authority_use": False,
                **raw_identity,
            }
        ],
    }

    required_evidence = [
        "URL_or_stable_document_identifier",
        "publisher",
        "publication_or_update_date",
        "content_hash_or_capture_receipt",
    ]
    priorities = {
        **{source_id: "P0" for source_id in PRIMARY_OFFICIAL_CANDIDATE_IDS},
        **{source_id: "P1" for source_id in ("S01", "S02", "S06", "S08")},
        **{source_id: "P2" for source_id in ("S03", "S09")},
        "S07": "excluded",
    }
    backlog = {
        "schema_version": f"{SCHEMA_PREFIX}.source_resolution_backlog",
        "status": "authoritative_source_resolution_pending",
        "unresolved_source_definition": (
            "generation_time_source_missing_URL_or_stable_identifier"
        ),
        "unresolved_source_count": len(GENERATION_TIME_SOURCE_IDS),
        "minimum_identity_evidence": required_evidence,
        "entries": [
            {
                "source_id": record["source_id"],
                "priority": priorities[record["source_id"]],
                "resolution_status": (
                    "excluded_derived_output"
                    if record["source_id"] == "S07"
                    else "pending"
                ),
                "unresolved_fields": (
                    []
                    if record["source_id"] == "S07"
                    else list(required_evidence)
                ),
                "minimum_evidence_needed": (
                    []
                    if record["source_id"] == "S07"
                    else list(required_evidence)
                ),
                "next_action": (
                    "retain_exclusion"
                    if record["source_id"] == "S07"
                    else "defer_to_H1_authoritative_source_resolution"
                ),
            }
            for record in records
        ],
    }

    class_counts = Counter(item["claim_class"] for item in alignments)
    risk_counts = Counter(item["risk_class"] for item in alignments)
    topic_family_counts = Counter(
        topic
        for item in alignments
        for topic in item["topic_family_labels"]
    )
    topic_labeled_claim_count = sum(
        bool(item["topic_family_labels"]) for item in alignments
    )
    claims_without_likely_source = sum(
        not item["likely_source_ids"] for item in alignments
    )
    claims_requiring_primary_source = sum(
        not item["required_authority_class"].startswith("none_")
        for item in alignments
    )
    alignment_payload = {
        "schema_version": f"{SCHEMA_PREFIX}.claim_source_family_alignment",
        "status": "title_level_alignment_not_verification",
        "input_claim_ledger": {
            "schema_version": ledger["schema_version"],
            "sha256": ledger_sha256,
            "claim_count": len(alignments),
            "verified_claim_count": 0,
            **raw_identity,
        },
        "alignment_basis": topic_labeling["mode"],
        "topic_labeling": topic_labeling,
        "claim_text_tracked": False,
        "source_content_inspected": False,
        "source_family_rules": {
            claim_class: {
                "base_likely_source_ids": list(rule.likely_source_ids),
                "required_authority_class": rule.required_authority_class,
                "source_resolution_dependency": rule.source_resolution_dependency,
                "rationale_label": rule.rationale_label,
            }
            for claim_class, rule in CLAIM_FAMILY_RULES.items()
        },
        "claim_alignment_count": len(alignments),
        "verified_claim_count": 0,
        "class_counts": dict(class_counts),
        "risk_counts": dict(risk_counts),
        "topic_family_counts": dict(topic_family_counts),
        "topic_labeled_claim_count": topic_labeled_claim_count,
        "topic_unlabeled_claim_count": len(alignments) - topic_labeled_claim_count,
        "policy_intent_claim_count": class_counts["policy_or_intent_claim"],
        "quantitative_claim_count": class_counts["quantitative_statistic"],
        "claims_without_likely_source": claims_without_likely_source,
        "claims_requiring_primary_source": claims_requiring_primary_source,
        "derived_audio_factual_use": False,
        "alignments": alignments,
    }
    readback = {
        "schema_version": f"{SCHEMA_PREFIX}.source_set_reconciliation_readback",
        "status": SOURCE_SET_STATUS,
        "source_count": len(records),
        "generation_time_count": len(GENERATION_TIME_SOURCE_IDS),
        "derived_count": len(DERIVED_SOURCE_IDS),
        "primary_official_candidate_count": len(PRIMARY_OFFICIAL_CANDIDATE_IDS),
        "primary_official_candidate_source_ids": list(PRIMARY_OFFICIAL_CANDIDATE_IDS),
        "claim_alignment_count": len(alignments),
        "verified_claim_count": 0,
        "unresolved_source_count": len(GENERATION_TIME_SOURCE_IDS),
        "source_title_coverage": {
            "covered": len(records),
            "expected": 11,
            "complete": len(records) == 11,
        },
        "claim_coverage": {
            "covered": len(alignments),
            "expected": EXPECTED_CLAIM_COUNT,
            "complete": len(alignments) == EXPECTED_CLAIM_COUNT,
        },
        "source_set_fingerprint": source_set_fingerprint,
        "private_link_tracking": False,
        "source_content_verified": False,
        "claim_verification_performed": False,
        "notebook_reference_supplied": True,
        "notebook_reference_access_verified": False,
        "notebook_reference_tracked": False,
        "topic_labeling_mode": topic_labeling["mode"],
        "topic_labeled_claim_count": topic_labeled_claim_count,
        "topic_unlabeled_claim_count": len(alignments) - topic_labeled_claim_count,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / "source_set_snapshot.json", snapshot)
    _write_json(output_dir / "source_authority_matrix.json", authority_matrix)
    _write_json(output_dir / "source_chronology_readback.json", chronology)
    _write_json(output_dir / "derived_source_exclusion.json", derived_exclusion)
    _write_json(output_dir / "source_resolution_backlog.json", backlog)
    _write_json(
        output_dir / "claim_source_family_alignment.json", alignment_payload
    )
    _write_json(
        output_dir / "source_set_reconciliation_readback.json", readback
    )
    _write_text(
        output_dir / "README_SOURCE_RECONCILIATION.md",
        _readme(
            records,
            len(alignments),
        ),
    )
    _write_text(output_dir / "source_set_limitations.md", _limitations())
    return validate_notebooklm_source_reconciliation(output_dir)


def validate_notebooklm_source_reconciliation(output_dir: Path) -> dict[str, Any]:
    """Validate the generated package without source or transcript access."""

    output_dir = Path(output_dir)
    missing = [
        name
        for name in REQUIRED_SOURCE_RECONCILIATION_FILES
        if not (output_dir / name).is_file()
    ]
    if missing:
        raise ValueError(f"missing source reconciliation artifacts: {missing}")

    snapshot = _load_json(output_dir / "source_set_snapshot.json")
    records = snapshot.get("sources", [])
    expected_records = [_source_record(spec) for spec in USER_PROVIDED_SOURCE_SNAPSHOT]
    if records != expected_records:
        raise ValueError("source snapshot differs from the exact supplied title set")
    if any(set(record) != set(REQUIRED_SOURCE_FIELDS) for record in records):
        raise ValueError("source record schema mismatch")
    if len({record["title_fingerprint"] for record in records}) != 11:
        raise ValueError("title fingerprints are not unique")
    if snapshot.get("source_set_fingerprint") != _source_set_fingerprint(records):
        raise ValueError("source set fingerprint mismatch")
    if snapshot.get("notebook_reference_tracked") is not False:
        raise ValueError("private NotebookLM reference must not be tracked")

    authority = _load_json(output_dir / "source_authority_matrix.json")
    if authority.get("primary_official_candidate_source_ids") != list(
        PRIMARY_OFFICIAL_CANDIDATE_IDS
    ):
        raise ValueError("primary official candidate IDs changed")
    authority_by_id = {
        item["source_id"]: item for item in authority.get("entries", [])
    }
    if authority_by_id.get("S03", {}).get("factual_authority_policy") != (
        "non_independent_excluded_from_factual_verification"
    ):
        raise ValueError("S03 must remain non-independent")
    if authority_by_id.get("S07", {}).get("factual_authority_policy") != "excluded":
        raise ValueError("S07 must remain excluded from factual authority")

    chronology = _load_json(output_dir / "source_chronology_readback.json")
    if chronology.get("generation_time_source_ids") != list(
        GENERATION_TIME_SOURCE_IDS
    ):
        raise ValueError("generation-time chronology changed")
    if chronology.get("post_generation_derived_source_ids") != ["S07"]:
        raise ValueError("derived chronology changed")
    if chronology.get("raw_transcript", {}).get("included_in_source_set") is not False:
        raise ValueError("raw transcript must remain a derived artifact")

    derived = _load_json(output_dir / "derived_source_exclusion.json")
    if derived.get("excluded_source_ids") != ["S07"]:
        raise ValueError("S07 derived exclusion missing")
    if any(
        item.get("factual_authority_use") is not False
        for item in derived.get("excluded_sources", [])
    ):
        raise ValueError("derived source factual use must remain false")

    alignment_payload = _load_json(
        output_dir / "claim_source_family_alignment.json"
    )
    alignments = alignment_payload.get("alignments", [])
    if len(alignments) != EXPECTED_CLAIM_COUNT:
        raise ValueError("claim alignment coverage is incomplete")
    if len({item["claim_id"] for item in alignments}) != EXPECTED_CLAIM_COUNT:
        raise ValueError("claim alignment IDs are missing or duplicated")
    for item in alignments:
        if set(item) != ALIGNMENT_RECORD_FIELDS:
            raise ValueError(f"alignment schema mismatch: {item.get('claim_id')}")
        if item["verification_status"] != "unverified":
            raise ValueError(f"claim became verified: {item['claim_id']}")
        topic_labels = item["topic_family_labels"]
        if not set(topic_labels) <= set(TOPIC_FAMILY_SOURCE_IDS):
            raise ValueError(f"unknown topic family: {item['claim_id']}")
        if "S07" in item["likely_source_ids"]:
            raise ValueError("S07 cannot be a factual claim source candidate")
        expected_derived_provenance = (
            ["S07"]
            if item["claim_class"]
            in {
                "analogy_or_metaphor",
                "rhetorical_framing",
            }
            else []
        )
        if item["derived_provenance_source_ids"] != expected_derived_provenance:
            raise ValueError("derived style/dialogue provenance changed")
        if item["claim_class"] == "technical_description":
            expected_topic_sources = _topic_source_ids(
                item["claim_class"], topic_labels
            )
            if expected_topic_sources and set(item["likely_source_ids"]) != (
                expected_topic_sources
            ):
                raise ValueError("technical topic family mapping is not specific")
        if item["claim_class"] in {
            "policy_or_intent_claim",
            "causal_claim",
        }:
            if item["risk_class"] != "high":
                raise ValueError("policy and causal claims must remain high risk")
            if "independent" not in item["required_authority_class"]:
                raise ValueError("policy and causal claims need independent evidence")
        if item["claim_class"] == "quantitative_statistic":
            dependency = item["source_resolution_dependency"]
            required_tokens = ("source_identity", "page_or_field", "publication_date", "unit")
            if not all(token in dependency for token in required_tokens):
                raise ValueError("quantitative claim exact-source dependency is incomplete")
    if alignment_payload.get("verified_claim_count") != 0:
        raise ValueError("verified claim count must remain zero")
    if alignment_payload.get("derived_audio_factual_use") is not False:
        raise ValueError("derived audio factual use must remain false")
    if alignment_payload.get("claim_text_tracked") is not False:
        raise ValueError("claim text must not be tracked")
    topic_labeling = alignment_payload.get("topic_labeling", {})
    if topic_labeling.get("local_line_map_used") is not True:
        raise ValueError("canonical local topic-label evidence is missing")
    if topic_labeling.get("claim_line_coverage") != EXPECTED_CLAIM_COUNT:
        raise ValueError("local topic-label coverage is incomplete")
    if _contains_forbidden_content_key(alignment_payload):
        raise ValueError("claim or transcript text leaked into alignment")

    readback = _load_json(
        output_dir / "source_set_reconciliation_readback.json"
    )
    expected_counts = {
        "source_count": 11,
        "generation_time_count": 10,
        "derived_count": 1,
        "primary_official_candidate_count": 4,
        "claim_alignment_count": EXPECTED_CLAIM_COUNT,
        "verified_claim_count": 0,
        "unresolved_source_count": 10,
    }
    for key, expected in expected_counts.items():
        if readback.get(key) != expected:
            raise ValueError(f"readback mismatch for {key}")
    if readback.get("status") != SOURCE_SET_STATUS:
        raise ValueError("source-set readback status mismatch")
    if readback.get("private_link_tracking") is not False:
        raise ValueError("private link tracking must remain false")

    for name in REQUIRED_SOURCE_RECONCILIATION_FILES:
        text = (output_dir / name).read_text(encoding="utf-8")
        if _PRIVATE_PATTERN.search(text):
            raise ValueError(f"private link, UUID, or user-home path found in {name}")

    return {
        "status": SOURCE_SET_STATUS,
        "source_count": len(records),
        "generation_time_count": chronology["generation_time_count"],
        "derived_count": chronology["post_generation_derived_count"],
        "primary_official_candidate_count": len(PRIMARY_OFFICIAL_CANDIDATE_IDS),
        "claim_alignment_count": len(alignments),
        "verified_claim_count": 0,
        "unresolved_source_count": readback["unresolved_source_count"],
        "source_set_fingerprint": snapshot["source_set_fingerprint"],
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Freeze the supplied NotebookLM title set and align sanitized claims."
    )
    parser.add_argument("--claim-ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--input-identity-receipt", type=Path)
    parser.add_argument("--local-line-map", type=Path)
    args = parser.parse_args(list(argv) if argv is not None else None)
    result = build_notebooklm_source_reconciliation(
        claim_ledger_path=args.claim_ledger,
        output_dir=args.output,
        input_identity_receipt_path=args.input_identity_receipt,
        local_line_map_path=args.local_line_map,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
