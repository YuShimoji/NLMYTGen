from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

import pytest

from tests.regression_workspace import repo_relative_path

from src.pipeline.new_banknote_authoritative_script import (
    build_new_banknote_authoritative_script_package,
    validate_new_banknote_authoritative_script_package,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
EPISODE_ROOT = (
    REPO_ROOT
    / "production_pilots"
    / "yukkuri_newsroom_content_spine_002"
)
PACKAGE = (
    EPISODE_ROOT
    / "external_editorial_input"
    / "new_banknote_security_notebooklm_001"
)
PROFILE = (
    EPISODE_ROOT
    / "ymm4_character_alias_profiles"
    / "ymm4_4_53_0_9_yukkuri_characters_v1.json"
)
PROFILE_RECEIPT = EPISODE_ROOT / "ymm4_observation_receipt_2026-07-10.json"

# Only the tracked title/claim/salvage surfaces that existed before this slice
# are copied into the isolated input package. In particular, none of the
# ignored transcript, source-cache, extract, or probe directories is available.
TRACKED_INPUT_FILES = (
    ".gitignore",
    "README_SOURCE_RECONCILIATION.md",
    "README_TRANSCRIPT_SALVAGE.md",
    "asr_correction_ledger.json",
    "claim_risk_ledger.json",
    "claim_source_family_alignment.json",
    "deduplication_readback.json",
    "derived_source_exclusion.json",
    "input_identity_receipt.json",
    "limitations.md",
    "normalization_contract.json",
    "notebooklm_generation_receipt.json",
    "notebooklm_style_contamination_ledger.json",
    "notebooklm_style_profile.json",
    "source_authority_matrix.json",
    "source_chronology_readback.json",
    "source_reconciliation_request.md",
    "source_resolution_backlog.json",
    "source_set_limitations.md",
    "source_set_reconciliation_readback.json",
    "source_set_snapshot.json",
    "transcript_quality_readback.json",
    "turn_segmentation_readback.json",
)

REQUIRED_ARTIFACTS = (
    "README_CANONICAL_SCRIPT_REVIEW.md",
    "asr_source_reconciliation.json",
    "authoritative_source_registry.json",
    "authoritative_source_resolution_readback.json",
    "canonical_script.json",
    "canonical_script_editorial_revision.md",
    "canonical_script.txt",
    "canonical_script_review.md",
    "canonical_yymm4.csv",
    "claim_adjudication.json",
    "claim_adjudication_readback.json",
    "csv_validation_readback.json",
    "cue_source_traceability.json",
    "derived_yymm4_import.csv",
    "editorial_revision_receipt.json",
    "limitations.md",
    "notebook_source_to_verification_source_crosswalk.json",
    "operator_review_sheet.md",
    "rejected_and_unresolved_claims.json",
    "script_generation_receipt.json",
    "source_capture_receipts.json",
    "source_resolution_limitations.md",
    "source_to_script_manifest.json",
    "verified_claim_set.json",
)

JSON_ARTIFACTS = tuple(
    name for name in REQUIRED_ARTIFACTS if name.endswith(".json")
)

CLAIM_OUTCOMES = {
    "verified_primary",
    "supported_context_only",
    "unresolved_not_used",
    "rejected_unsupported",
    "rejected_policy_intent",
    "rejected_quantitative_without_exact_source",
    "style_or_rhetoric_only",
    "duplicate_not_used",
}

OFFICIAL_BASE_DOMAINS = {"npb.go.jp", "mof.go.jp", "boj.or.jp"}
EXPECTED_OFFICIAL_URLS = {
    "S04": "https://www.npb.go.jp/recruit/brochure.files/recruit-2511-4.pdf",
    "S05_equivalent": "https://www.npb.go.jp/product_service/intro/gizoboshi.html",
    "S10": "https://www.mof.go.jp/faq/currency/07am.htm",
    "S11": "https://www.npb.go.jp/product_service/intro/ninsiki.html",
}
CANONICAL_TO_YMM4 = {
    "れいむ": "ゆっくり霊夢",
    "まりさ": "ゆっくり魔理沙",
}
EXPECTED_SCENES = ["S1", "S1", "S2", "S2", "S2", "S2", "S3", "S3", "S3"]
EXPECTED_SPEAKER_COUNTS = {"れいむ": 3, "まりさ": 6}
EXPECTED_CHARACTER_COUNTS = {"ゆっくり霊夢": 3, "ゆっくり魔理沙": 6}
EXPECTED_CLAIM_OUTCOME_IDENTITY_SHA256 = (
    "4084f67719f95d16efad7059dbf9ecce315f537f77b65a8f442ba90929acb5a6"
)
EXPECTED_SOURCE_REGISTRY_SHA256 = (
    "3a55d5ec999edec215b87fba0f999f1a9086eca1921158c9c3f72749ade1713a"
)
EXPECTED_SOURCE_RECEIPTS_SHA256 = (
    "6c4cc1817a3574b7278f2986522c91b05a51c1b8bba3ea4a544a78aee920e205"
)
EXPECTED_MARISA_TERMINAL_FORMS = (
    "んだ",
    "んだぜ",
    "ぞ",
    "なんだ",
    "ぜ",
    "おこう",
)
EXPECTED_VERIFIED_NOT_ADOPTED = {
    "claim_095",
    "claim_158",
    "claim_162",
    "claim_164",
}
EDITORIAL_RECEIPT_FILES = (
    "README_CANONICAL_SCRIPT_REVIEW.md",
    "canonical_script.json",
    "canonical_script.txt",
    "canonical_script_review.md",
    "cue_source_traceability.json",
    "canonical_yymm4.csv",
    "derived_yymm4_import.csv",
    "csv_validation_readback.json",
    "source_to_script_manifest.json",
    "canonical_script_editorial_revision.md",
)
SCRIPT_RECEIPT_FILES = (
    "README_CANONICAL_SCRIPT_REVIEW.md",
    "canonical_script.json",
    "canonical_script_editorial_revision.md",
    "canonical_script.txt",
    "canonical_script_review.md",
    "cue_source_traceability.json",
    "canonical_yymm4.csv",
    "derived_yymm4_import.csv",
    "csv_validation_readback.json",
    "editorial_revision_receipt.json",
    "operator_review_sheet.md",
    "limitations.md",
    "source_to_script_manifest.json",
)

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$", re.IGNORECASE)
_UUID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)
_PRIVATE_PATH_RE = re.compile(r"[A-Za-z]:\\Users\\|/Users/|/home/", re.IGNORECASE)
_SPOKEN_INTERNAL_RE = re.compile(
    r"https?://|[A-Za-z]:\\|/Users/|/home/|\bclaim_\d+\b|"
    r"\bS\d{2}\b|\bV\d{2,}\b|\b[0-9a-f]{40,64}\b|"
    r"codex/new-banknote",
    re.IGNORECASE,
)
_BANNED_SPOKEN_PATTERNS = (
    re.compile(r"キャッシュレス"),
    re.compile(r"裏のミッション|隠された(?:使命|狙い)|政府の隠れた使命"),
    re.compile(r"タンス預金|心理的に.*(?:炙|あぶ)り出"),
    re.compile(r"券売機.*(?:意図|圧力)"),
    re.compile(r"現金(?:が)?消滅|現金を一切使わせなく"),
    re.compile(r"リスナー(?:の|のみな)|今回の深掘り|資料を元に"),
    re.compile(r"今回の解説はここまで|また次回|お会いしましょう"),
)
_BANNED_BODY_KEYS = {
    "body",
    "full_text",
    "html_body",
    "pdf_text",
    "raw_html",
    "raw_text",
    "source_body",
    "transcript_text",
    "verbatim_text",
}


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict), path.name
    return payload


def _dump(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _records(payload: dict[str, Any], *names: str) -> list[dict[str, Any]]:
    for name in names:
        value = payload.get(name)
        if isinstance(value, list):
            assert all(isinstance(item, dict) for item in value), name
            return list(value)
    raise AssertionError(
        f"expected one of record arrays {names}; got {sorted(payload)}"
    )


def _first(record: dict[str, Any], *names: str) -> Any:
    for name in names:
        value = record.get(name)
        if value not in (None, "", [], {}):
            return value
    return None


def _source_id(record: dict[str, Any]) -> str:
    value = _first(record, "source_id", "verification_source_id")
    assert isinstance(value, str) and value, record
    return value


def _evidence_source_id(record: dict[str, Any]) -> str:
    value = _first(
        record,
        "source_id",
        "verification_source_id",
        "supporting_source_id",
    )
    assert isinstance(value, str) and value, record
    return value


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {
            key for child in value.values() for key in _all_keys(child)
        }
    if isinstance(value, list):
        return {key for child in value for key in _all_keys(child)}
    return set()


def _values_for_keys(value: Any, wanted: set[str]) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in wanted and isinstance(child, str):
                yield child
            yield from _values_for_keys(child, wanted)
    elif isinstance(value, list):
        for child in value:
            yield from _values_for_keys(child, wanted)


def _is_canonical_use(record: dict[str, Any]) -> bool:
    value = record.get("canonical_use")
    return value is True or value in {"adopted", "used", "included"}


def _has_exact_location(record: dict[str, Any]) -> bool:
    location = _first(
        record,
        "exact_location",
        "location",
        "location_label",
        "heading",
        "page",
        "field",
        "json_pointer_or_field",
    )
    if isinstance(location, dict):
        return any(value not in (None, "", [], {}) for value in location.values())
    return location not in (None, "", [], {})


def _official_url(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(
        host == domain or host.endswith(f".{domain}")
        for domain in OFFICIAL_BASE_DOMAINS
    )


def _has_timezone_offset(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _crosswalk_relations(payload: dict[str, Any]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}

    def visit(value: Any, notebook_id: str | None = None) -> None:
        if isinstance(value, dict):
            candidate = _first(value, "notebook_source_id", "source_snapshot_id")
            if isinstance(candidate, str) and re.fullmatch(r"S\d{2}", candidate):
                notebook_id = candidate
            elif notebook_id is None:
                fallback = value.get("source_id")
                if isinstance(fallback, str) and re.fullmatch(r"S\d{2}", fallback):
                    notebook_id = fallback
            if notebook_id is not None:
                bucket = result.setdefault(notebook_id, set())
                for field in (
                    "relation_type",
                    "resolution_status",
                    "exact_source_status",
                ):
                    relation = value.get(field)
                    if isinstance(relation, str):
                        bucket.add(relation)
            for child in value.values():
                visit(child, notebook_id)
        elif isinstance(value, list):
            for child in value:
                visit(child, notebook_id)

    visit(payload)
    return result


def _tree_hashes(root: Path) -> dict[str, str]:
    return {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest()
        for name in REQUIRED_ARTIFACTS
    }


def _claim_outcome_identity_sha256(payload: dict[str, Any]) -> str:
    claims = _records(payload, "claims", "adjudications")
    identity = "\n".join(
        f'{claim["claim_id"]}:{claim["primary_outcome"]}' for claim in claims
    )
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def _marisa_terminal_form(text: str) -> str:
    cleaned = re.sub(r"[。！？]+$", "", text.strip())
    for terminal in ("なんだ", "んだぜ", "おこう", "んだ", "だぜ", "ぜ", "ぞ", "だ"):
        if cleaned.endswith(terminal):
            return terminal
    return cleaned


def _csv_rows(path: Path) -> list[tuple[str, str]]:
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), f"{path.name} must be UTF-8 without BOM"
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = [tuple(row) for row in csv.reader(handle) if row]
    assert all(len(row) == 2 for row in rows)
    return [(row[0], row[1]) for row in rows]


def _isolated_tracked_package(tmp_path: Path) -> Path:
    isolated_root = tmp_path / "isolated_repo"
    package = isolated_root / PACKAGE.relative_to(REPO_ROOT)
    package.mkdir(parents=True)
    for name in TRACKED_INPUT_FILES:
        source = PACKAGE / name
        assert source.is_file(), name
        shutil.copy2(source, package / name)

    profile = isolated_root / PROFILE.relative_to(REPO_ROOT)
    profile.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROFILE, profile)
    receipt = isolated_root / PROFILE_RECEIPT.relative_to(REPO_ROOT)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROFILE_RECEIPT, receipt)
    shutil.copy2(REPO_ROOT / ".gitignore", isolated_root / ".gitignore")

    for dirname in ("local_outputs", "source_cache", "source_extracts", "source_probe"):
        assert not (package / dirname).exists()
    return package


@pytest.fixture
def generated(tmp_path: Path) -> tuple[Path, Path]:
    package = _isolated_tracked_package(tmp_path)
    output = tmp_path / "generated"
    result = build_new_banknote_authoritative_script_package(
        package_dir=package,
        output_dir=output,
    )
    assert isinstance(result, dict)
    for name in REQUIRED_ARTIFACTS:
        assert (output / name).is_file(), name
    validation = validate_new_banknote_authoritative_script_package(output)
    assert isinstance(validation, dict)
    assert validation.get("failed_checks", []) == []
    return package, output


def test_official_source_receipts_allowlist_and_exact_relationships(
    generated: tuple[Path, Path],
) -> None:
    _, output = generated
    registry = _load(output / "authoritative_source_registry.json")
    registry_sources = _records(registry, "sources", "entries")
    registry_by_id = {_source_id(item): item for item in registry_sources}
    assert len(registry_by_id) == len(registry_sources) >= 4
    registry_urls = {
        str(_first(item, "canonical_url", "stable_url", "url"))
        for item in registry_sources
    }
    assert set(EXPECTED_OFFICIAL_URLS.values()) <= registry_urls

    receipts_payload = _load(output / "source_capture_receipts.json")
    receipts = _records(receipts_payload, "receipts", "captures", "sources")
    assert receipts
    for receipt in receipts:
        source_id = _source_id(receipt)
        source = registry_by_id[source_id]
        merged = {**source, **receipt}
        url = _first(merged, "canonical_url", "stable_url", "url")
        retrieved_at = _first(
            merged,
            "retrieved_at",
            "retrieval_timestamp",
            "retrieved_at_with_offset",
        )
        size = _first(merged, "size_bytes", "content_size_bytes")
        assert isinstance(url, str) and _official_url(url)
        assert isinstance(retrieved_at, str) and _has_timezone_offset(retrieved_at)
        assert _first(merged, "publisher", "publisher_label")
        assert _first(merged, "title", "captured_title")
        assert _first(merged, "content_type", "media_type")
        assert int(size) > 0
        assert int(_first(merged, "http_status", "status_code")) == 200
        assert _SHA256_RE.fullmatch(str(_first(merged, "sha256", "content_sha256")))

    crosswalk = _load(
        output / "notebook_source_to_verification_source_crosswalk.json"
    )
    relations = _crosswalk_relations(crosswalk)
    assert "exact_title_match" in relations["S10"]
    assert "exact_title_match" in relations["S11"]
    assert "exact_document_match" in relations["S04"]
    assert "unresolved_exact_source" in relations["S05"]
    assert "official_equivalent" in relations["S05"]

    for source in registry_sources:
        assert source.get("publication_date") is None
        assert source.get("publication_date_basis") == "not_stated"
        assert isinstance(source.get("fact_dates"), list)
        assert isinstance(source.get("content_dates"), list)
    assert registry_by_id["V02"]["fact_dates"] == [
        {"date": "2024", "meaning": "F券発行年", "location": "H1直下の導入"}
    ]
    assert registry_by_id["V01"]["content_dates"][0]["basis"] == (
        "html_meta_name_date"
    )
    crosswalk_entries = {
        item["notebook_source_id"]: item for item in crosswalk["entries"]
    }
    assert "V06" not in {
        relation["verification_source_id"]
        for relation in crosswalk_entries["S04"]["relations"]
    }

    readback = _load(output / "authoritative_source_resolution_readback.json")
    assert readback.get("status") in {
        "passed",
        "authoritative_source_resolution_complete",
        "official_source_resolution_complete",
    }
    assert readback.get("S10_exact_resolved", True) is True
    assert readback.get("S11_exact_resolved", True) is True


def test_all_182_claims_have_one_outcome_and_primary_evidence(
    generated: tuple[Path, Path],
) -> None:
    package, output = generated
    input_claims = _load(package / "claim_risk_ledger.json")["claims"]
    adjudication = _load(output / "claim_adjudication.json")
    claims = _records(adjudication, "claims", "adjudications")
    assert len(claims) == len(input_claims) == 182
    assert [item["claim_id"] for item in claims] == [
        item["claim_id"] for item in input_claims
    ]
    assert [item["line_fingerprint"] for item in claims] == [
        item["line_fingerprint"] for item in input_claims
    ]
    assert [item["claim_class"] for item in claims] == [
        item["claim_class"] for item in input_claims
    ]
    assert [item["risk_class"] for item in claims] == [
        item["risk"] for item in input_claims
    ]

    for claim in claims:
        assert claim.get("primary_outcome") in CLAIM_OUTCOMES
        assert isinstance(claim.get("secondary_tags"), list)
        assert isinstance(claim.get("supporting_evidence"), list)
        assert "canonical_use" in claim

    outcome_counts = Counter(item["primary_outcome"] for item in claims)
    declared_counts = adjudication.get("outcome_counts")
    if declared_counts is not None:
        assert {key: int(value) for key, value in declared_counts.items()} == dict(
            outcome_counts
        )

    registry_sources = _records(
        _load(output / "authoritative_source_registry.json"),
        "sources",
        "entries",
    )
    registry_by_id = {_source_id(item): item for item in registry_sources}
    verified = [
        item for item in claims if item["primary_outcome"] == "verified_primary"
    ]
    assert verified
    for claim in verified:
        evidence = claim["supporting_evidence"]
        assert evidence
        for support in evidence:
            source = registry_by_id[_evidence_source_id(support)]
            authority = str(
                _first(source, "authority_class", "authority", "evidence_grade") or ""
            ).lower()
            assert "official" in authority and "secondary" not in authority
            assert _has_exact_location(support)
            assert _first(support, "url_label", "source_label")

    verified_payload = _load(output / "verified_claim_set.json")
    verified_records = _records(
        verified_payload,
        "claims",
        "verified_claims",
        "entries",
    )
    assert {item["claim_id"] for item in verified_records} == {
        item["claim_id"] for item in verified
    }

    rejected_payload = _load(output / "rejected_and_unresolved_claims.json")
    rejected_records = _records(
        rejected_payload,
        "claims",
        "rejected_and_unresolved_claims",
        "entries",
    )
    assert not ({item["claim_id"] for item in rejected_records} & {
        item["claim_id"] for item in verified
    })
    assert {item["claim_id"] for item in rejected_records} == {
        item["claim_id"]
        for item in claims
        if item["primary_outcome"] != "verified_primary"
    }

    readback = _load(output / "claim_adjudication_readback.json")
    assert int(_first(readback, "claim_count", "input_claim_count")) == 182
    assert int(_first(readback, "adjudicated_claim_count", "coverage_count")) == 182


def test_policy_cashless_and_unsupported_quantitative_claims_are_excluded(
    generated: tuple[Path, Path],
) -> None:
    package, output = generated
    claims = _records(
        _load(output / "claim_adjudication.json"),
        "claims",
        "adjudications",
    )
    by_id = {item["claim_id"]: item for item in claims}

    policy_claims = [
        item for item in claims if item["claim_class"] == "policy_or_intent_claim"
    ]
    assert len(policy_claims) == 8
    assert all(
        item["primary_outcome"] == "rejected_policy_intent"
        and not _is_canonical_use(item)
        for item in policy_claims
    )

    unsupported_dramatic = [
        item
        for item in claims
        if item["claim_class"] == "unsupported_dramatic_assertion"
    ]
    assert unsupported_dramatic
    assert all(
        item["primary_outcome"] == "rejected_unsupported"
        and not _is_canonical_use(item)
        for item in unsupported_dramatic
    )

    input_alignments = _records(
        _load(package / "claim_source_family_alignment.json"),
        "alignments",
        "claims",
    )
    cashless_causal_ids = {
        item["claim_id"]
        for item in input_alignments
        if item["claim_class"] == "causal_claim"
        and "cashless_policy_intent" in item.get("topic_family_labels", [])
    }
    cashless_causal = [by_id[claim_id] for claim_id in cashless_causal_ids]
    assert len(cashless_causal) == 2
    assert all(
        item["primary_outcome"] != "verified_primary"
        and not _is_canonical_use(item)
        for item in cashless_causal
    )

    quantitative = [
        item for item in claims if item["claim_class"] == "quantitative_statistic"
    ]
    assert len(quantitative) == 35
    for claim in quantitative:
        if claim["primary_outcome"] == "verified_primary":
            for support in claim["supporting_evidence"]:
                assert _has_exact_location(support)
                assert _first(support, "fact_date", "evidence_as_of")
                assert support.get("date_basis") in {
                    "claim_fact_date",
                    "source_retrieval_timestamp",
                }
                assert support.get("source_publication_date") is None
                assert support.get("source_publication_date_basis") == "not_stated"
                assert _first(support, "unit", "measurement_unit")
        else:
            assert claim["primary_outcome"] in {
                "rejected_quantitative_without_exact_source",
                "rejected_unsupported",
                "unresolved_not_used",
                "duplicate_not_used",
            }
            assert not _is_canonical_use(claim)

    script = _load(output / "canonical_script.json")
    adopted = {
        claim_id
        for cue in script["cues"]
        for claim_id in cue["adopted_claim_ids"]
    }
    assert all(
        by_id[claim_id]["primary_outcome"] == "verified_primary"
        for claim_id in adopted
    )


def test_nine_cue_script_and_traceability_contract(
    generated: tuple[Path, Path],
) -> None:
    _, output = generated
    script = _load(output / "canonical_script.json")
    cues = script["cues"]
    assert script["cue_count"] == len(cues) == 9
    assert [cue["sequence"] for cue in cues] == list(range(1, 10))
    assert [cue["scene_id"] for cue in cues] == EXPECTED_SCENES
    assert script["scene_allocation"] == {"S1": 2, "S2": 4, "S3": 3}
    assert dict(Counter(cue["speaker"] for cue in cues)) == EXPECTED_SPEAKER_COUNTS
    assert script["speaker_counts"] == EXPECTED_SPEAKER_COUNTS
    assert script["unsupported_claim_count"] == 0
    assert script.get("editorial_adoption") is False
    assert script.get("public_ready") is False
    assert script.get("production_ready") is False
    assert [cue["adopted_claim_ids"] for cue in cues] == [
        ["claim_010"],
        ["claim_090", "claim_065", "claim_099", "claim_161"],
        ["claim_090"],
        ["claim_065", "claim_067"],
        ["claim_116"],
        ["claim_096", "claim_097"],
        ["claim_118", "claim_130", "claim_132"],
        ["claim_114", "claim_155", "claim_157"],
        ["claim_090", "claim_116", "claim_065", "claim_096"],
    ]
    spoken = "\n".join(cue["text"] for cue in cues)
    assert "肖像の周りに緻密な連続模様" not in spoken
    assert "図柄も変化" not in spoken
    assert "ホログラムやすき入れの位置" not in spoken

    adjudication = {
        item["claim_id"]: item
        for item in _records(
            _load(output / "claim_adjudication.json"),
            "claims",
            "adjudications",
        )
    }
    for cue in cues:
        claim_ids = cue["adopted_claim_ids"]
        assert claim_ids
        assert cue.get("evidence_grade") == "verified_primary"
        assert cue.get("semantic_coverage_status") == (
            "fully_mapped_to_adjudicated_propositions"
        )
        assert cue.get("unsupported_claim_count") == 0
        support_units = cue.get("factual_support_units")
        assert support_units
        mapped_claim_ids: list[str] = []
        for unit in support_units:
            assert unit.get("unit_id")
            assert unit.get("statement")
            assert unit.get("support_status") == (
                "supported_by_verified_primary_claims"
            )
            assert unit.get("claim_ids")
            for claim_id in unit["claim_ids"]:
                if claim_id not in mapped_claim_ids:
                    mapped_claim_ids.append(claim_id)
        assert mapped_claim_ids == claim_ids
        assert all(
            adjudication[claim_id]["primary_outcome"] == "verified_primary"
            for claim_id in claim_ids
        )

    traceability = _load(output / "cue_source_traceability.json")
    traces = _records(traceability, "cues", "traceability", "entries")
    assert len(traces) == 9
    assert [item["cue_id"] for item in traces] == [item["cue_id"] for item in cues]
    for cue, trace in zip(cues, traces, strict=True):
        trace_claims = _first(trace, "adopted_claim_ids", "claim_ids")
        trace_sources = _first(
            trace,
            "supporting_source_ids",
            "source_ids",
            "source_references",
            "sources",
        )
        assert trace_claims == cue["adopted_claim_ids"]
        assert trace_sources
        assert trace.get("unsupported_claim_count") == 0
        assert trace.get("factual_support_units")
        assert all(
            unit.get("supported") is True
            and unit.get("supporting_evidence")
            for unit in trace["factual_support_units"]
        )

    manifest = _load(output / "source_to_script_manifest.json")
    manifest_rows = _records(manifest, "sources", "entries")
    actual_edges = {
        (row["source_id"], claim_id)
        for row in manifest_rows
        for claim_id in row["claim_ids"]
    }
    expected_edges = {
        (_evidence_source_id(support), claim_id)
        for cue in cues
        for claim_id in cue["adopted_claim_ids"]
        for support in adjudication[claim_id]["supporting_evidence"]
    }
    assert actual_edges == expected_edges
    assert all(
        any(
            _evidence_source_id(support) == source_id
            for support in adjudication[claim_id]["supporting_evidence"]
        )
        for source_id, claim_id in actual_edges
    )
    assert manifest.get("unsupported_claim_count") == 0

    script_text = (output / "canonical_script.txt").read_text(encoding="utf-8")
    positions = [script_text.index(cue["text"]) for cue in cues]
    assert positions == sorted(positions)

    receipt = _load(output / "script_generation_receipt.json")
    assert receipt["cue_count"] == 9
    assert receipt["scene_allocation"] == {"S1": 2, "S2": 4, "S3": 3}
    assert receipt["canonical_speaker_counts"] == EXPECTED_SPEAKER_COUNTS
    assert receipt["unsupported_claim_count"] == 0


def test_editorial_convergence_preserves_evidence_and_removes_spoken_defects(
    generated: tuple[Path, Path],
) -> None:
    _, output = generated
    script = _load(output / "canonical_script.json")
    cues = script["cues"]
    spoken = "\n".join(cue["text"] for cue in cues)

    assert "E券" not in spoken
    assert "道具で見る" not in spoken
    assert "ルーペで見る" in cues[8]["text"]
    assert cues[0]["speaker"] == "れいむ" and cues[0]["text"].endswith("？")
    assert cues[1]["speaker"] == "まりさ" and cues[1]["text"].startswith(
        "あるぞ。"
    )
    assert len(cues[7]["factual_support_units"]) == 3
    assert cues[7]["adopted_claim_ids"] == [
        "claim_114",
        "claim_155",
        "claim_157",
    ]

    marisa_endings = [
        _marisa_terminal_form(cue["text"])
        for cue in cues
        if cue["speaker"] == "まりさ"
    ]
    assert tuple(marisa_endings) == EXPECTED_MARISA_TERMINAL_FORMS

    adjudication = _load(output / "claim_adjudication.json")
    claim_by_id = {
        claim["claim_id"]: claim
        for claim in _records(adjudication, "claims", "adjudications")
    }
    assert _claim_outcome_identity_sha256(adjudication) == (
        EXPECTED_CLAIM_OUTCOME_IDENTITY_SHA256
    )
    assert sum(
        claim["primary_outcome"] == "verified_primary"
        for claim in claim_by_id.values()
    ) == 19
    assert claim_by_id["claim_158"]["primary_outcome"] == "verified_primary"
    assert claim_by_id["claim_158"]["canonical_use"] is False
    assert claim_by_id["claim_095"]["primary_outcome"] == "verified_primary"
    assert claim_by_id["claim_095"]["canonical_use"] is False
    assert claim_by_id["claim_096"]["canonical_use"] is True
    assert claim_by_id["claim_099"]["canonical_use"] is True
    adopted_ids = {
        claim_id for cue in cues for claim_id in cue["adopted_claim_ids"]
    }
    assert adjudication["canonical_claim_count"] == len(adopted_ids) == 15
    assert all(
        claim["canonical_use"] == (claim_id in adopted_ids)
        for claim_id, claim in claim_by_id.items()
    )
    assert {
        claim_id
        for claim_id, claim in claim_by_id.items()
        if claim["primary_outcome"] == "verified_primary"
        and claim["canonical_use"] is False
    } == EXPECTED_VERIFIED_NOT_ADOPTED

    verified_payload = _load(output / "verified_claim_set.json")
    verified_records = _records(
        verified_payload,
        "claims",
        "verified_claims",
    )
    verified_ids = {claim["claim_id"] for claim in verified_records}
    assert verified_records == [
        claim
        for claim in adjudication["claims"]
        if claim["primary_outcome"] == "verified_primary"
    ]
    assert {"claim_095", "claim_158"} <= verified_ids

    traceability = _load(output / "cue_source_traceability.json")
    trace_by_id = {
        trace["cue_id"]: trace
        for trace in _records(traceability, "cues", "traceability")
    }
    retained = trace_by_id["cue_008"]["retained_verified_unspoken_claims"]
    assert [row["claim_id"] for row in retained] == ["claim_158"]
    assert retained[0]["adoption_status"] == "verified_not_adopted"
    assert retained[0]["retention_reason"] == "cue_information_budget"
    assert retained[0]["supporting_evidence"] == [
        {
            "claim_id": "claim_158",
            "source_id": "V02",
            "exact_location": "一万円券と千円券の『1』のデザインの違い",
            "evidence_grade": "verified_primary",
        }
    ]
    assert not any(
        edge["claim_id"] == "claim_158"
        for edge in trace_by_id["cue_008"]["supporting_evidence"]
    )

    manifest_claim_ids = {
        claim_id
        for source in _records(
            _load(output / "source_to_script_manifest.json"),
            "sources",
            "entries",
        )
        for claim_id in source["claim_ids"]
    }
    assert "claim_158" not in manifest_claim_ids
    assert "claim_095" not in manifest_claim_ids
    assert "claim_096" in manifest_claim_ids

    assert hashlib.sha256(
        (output / "authoritative_source_registry.json").read_bytes()
    ).hexdigest() == EXPECTED_SOURCE_REGISTRY_SHA256
    assert hashlib.sha256(
        (output / "source_capture_receipts.json").read_bytes()
    ).hexdigest() == EXPECTED_SOURCE_RECEIPTS_SHA256

    editorial_receipt = _load(output / "editorial_revision_receipt.json")
    assert editorial_receipt["status"] == "passed"
    assert editorial_receipt["revision_id"] == (
        "final-editorial-convergence-before-human-review-v1"
    )
    assert editorial_receipt["factual_support_units"] == {
        "before": 22,
        "after": 20,
    }
    assert editorial_receipt["claim_edges"] == {"before": 23, "after": 21}
    assert len(editorial_receipt["human_review_questions"]) == 5
    assert all(value is False for value in editorial_receipt["actions"].values())
    assert all(editorial_receipt["checks"].values())
    assert tuple(editorial_receipt["files"]) == EDITORIAL_RECEIPT_FILES
    for name, digest in editorial_receipt["files"].items():
        assert _SHA256_RE.fullmatch(digest)
        assert hashlib.sha256((output / name).read_bytes()).hexdigest() == digest

    script_receipt = _load(output / "script_generation_receipt.json")
    assert tuple(script_receipt["files"]) == SCRIPT_RECEIPT_FILES
    for name, digest in script_receipt["files"].items():
        assert _SHA256_RE.fullmatch(digest)
        assert hashlib.sha256((output / name).read_bytes()).hexdigest() == digest

    revision = (output / "canonical_script_editorial_revision.md").read_text(
        encoding="utf-8"
    )
    assert "22件から20件" in revision
    assert "23本から21本" in revision
    assert "claim_158" in revision
    assert "NotebookLMアクセス" in revision

    limitations = (output / "limitations.md").read_text(encoding="utf-8")
    debt_rows = [line for line in limitations.splitlines() if line.startswith("| ")]
    assert len(debt_rows) == 6  # header, separator, and four named debts
    assert "| Owner |" in debt_rows[0]
    assert "true speaker identity" in limitations
    assert "Voice・rhythm・terminologyのhuman editorial acceptance" in limitations
    assert "human editorial reviewer" in limitations


def test_canonical_and_derived_csvs_preserve_text_order_and_only_map_speakers(
    generated: tuple[Path, Path],
) -> None:
    _, output = generated
    script = _load(output / "canonical_script.json")
    canonical = _csv_rows(output / "canonical_yymm4.csv")
    derived = _csv_rows(output / "derived_yymm4_import.csv")
    expected_canonical = [(cue["speaker"], cue["text"]) for cue in script["cues"]]
    expected_derived = [
        (CANONICAL_TO_YMM4[speaker], text) for speaker, text in expected_canonical
    ]

    assert canonical == expected_canonical
    assert derived == expected_derived
    assert len(canonical) == len(derived) == 9
    assert dict(Counter(speaker for speaker, _ in canonical)) == EXPECTED_SPEAKER_COUNTS
    assert dict(Counter(speaker for speaker, _ in derived)) == EXPECTED_CHARACTER_COUNTS
    assert [text for _, text in canonical] == [text for _, text in derived]
    assert canonical[0] != ("speaker", "text")

    readback = _load(output / "csv_validation_readback.json")
    assert readback.get("status") == "passed"
    checks = readback.get("checks", {})
    assert isinstance(checks, dict) and checks
    for name, value in checks.items():
        if isinstance(value, bool):
            assert value is True, name
    if "unmapped_canonical_speakers" in checks:
        assert checks["unmapped_canonical_speakers"] == []


def test_spoken_style_privacy_and_source_body_boundaries(
    generated: tuple[Path, Path],
) -> None:
    _, output = generated
    script = _load(output / "canonical_script.json")
    spoken = "\n".join(cue["text"] for cue in script["cues"])
    assert not _SPOKEN_INTERNAL_RE.search(spoken)
    for pattern in _BANNED_SPOKEN_PATTERNS:
        assert not pattern.search(spoken), pattern.pattern

    payloads = [_load(output / name) for name in JSON_ARTIFACTS]
    all_keys = {key for payload in payloads for key in _all_keys(payload)}
    assert not (_BANNED_BODY_KEYS & all_keys)
    for payload in payloads:
        for paraphrase in _values_for_keys(
            payload,
            {"bounded_paraphrase", "claim_paraphrase", "source_paraphrase"},
        ):
            assert len(paraphrase) <= 400
            assert "\n" not in paraphrase

    text_files = [path for path in output.rglob("*") if path.is_file()]
    assert not any(
        part in {"source_cache", "source_extracts", "source_probe", "local_outputs"}
        for path in text_files
        for part in path.parts
    )
    assert not any(
        path.suffix.lower() in {".pdf", ".htm", ".html"}
        for path in text_files
    )
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace") for path in text_files
    )
    assert "notebooklm.google.com" not in combined.lower()
    assert not _PRIVATE_PATH_RE.search(combined)
    assert not _UUID_RE.search(combined)

    primary = (output / "README_CANONICAL_SCRIPT_REVIEW.md").read_text(
        encoding="utf-8"
    )
    for boundary in ("INTERNAL REVIEW", "NOT FINAL", "NON-PUBLIC", "NON-PRODUCTION"):
        assert boundary in primary
    review_sheet = (output / "operator_review_sheet.md").read_text(encoding="utf-8")
    questions = re.findall(r"(?m)^\s*\d+[.)]\s+", review_sheet)
    assert 1 <= len(questions) <= 5


def test_build_is_cache_independent_and_byte_deterministic(tmp_path: Path) -> None:
    package = _isolated_tracked_package(tmp_path)
    first = tmp_path / "first"
    second = tmp_path / "second"

    build_new_banknote_authoritative_script_package(
        package_dir=package,
        output_dir=first,
    )
    build_new_banknote_authoritative_script_package(
        package_dir=package,
        output_dir=second,
    )
    first_hashes = _tree_hashes(first)
    assert first_hashes == _tree_hashes(second)

    build_new_banknote_authoritative_script_package(
        package_dir=package,
        output_dir=first,
    )
    assert first_hashes == _tree_hashes(first)
    validation = validate_new_banknote_authoritative_script_package(first)
    assert validation.get("failed_checks", []) == []


def test_validator_separates_generated_review_html_from_source_bodies(
    generated: tuple[Path, Path],
    tmp_path: Path,
) -> None:
    _, output = generated
    candidate = tmp_path / "document-boundary"
    shutil.copytree(output, candidate)
    review_dir = candidate / "reference_layout_reconstruction"
    review_dir.mkdir()
    (review_dir / "review_surface.html").write_text(
        "<html><body>generated review surface</body></html>\n",
        encoding="utf-8",
    )
    validation = validate_new_banknote_authoritative_script_package(candidate)
    assert validation["checks"]["no_source_bodies"] is True
    assert validation["status"] == "passed"

    (candidate / "unexpected_source_document.html").write_text(
        "<html><body>unscoped source body</body></html>\n",
        encoding="utf-8",
    )
    validation = validate_new_banknote_authoritative_script_package(candidate)
    assert validation["checks"]["no_source_bodies"] is False
    assert "no_source_bodies" in validation["failed_checks"]


def test_validator_rejects_coordinated_integrity_tampering(
    generated: tuple[Path, Path],
    tmp_path: Path,
) -> None:
    _, output = generated

    def copy_output(name: str) -> Path:
        target = tmp_path / name
        shutil.copytree(output, target)
        return target

    def refresh_receipt_hashes(root: Path) -> None:
        editorial_path = root / "editorial_revision_receipt.json"
        editorial = _load(editorial_path)
        for name in editorial["files"]:
            editorial["files"][name] = hashlib.sha256(
                (root / name).read_bytes()
            ).hexdigest()
        _dump(editorial_path, editorial)

        script_path = root / "script_generation_receipt.json"
        script_receipt = _load(script_path)
        for name in script_receipt["files"]:
            script_receipt["files"][name] = hashlib.sha256(
                (root / name).read_bytes()
            ).hexdigest()
        _dump(script_path, script_receipt)

    canonical_use_root = copy_output("tampered_canonical_use")
    adjudication = _load(canonical_use_root / "claim_adjudication.json")
    next(
        claim for claim in adjudication["claims"] if claim["claim_id"] == "claim_099"
    )["canonical_use"] = False
    _dump(canonical_use_root / "claim_adjudication.json", adjudication)
    validation = validate_new_banknote_authoritative_script_package(
        canonical_use_root
    )
    assert "canonical_use_matches_adopted_claim_set" in validation["failed_checks"]
    assert "verified_claim_set_exact" in validation["failed_checks"]

    receipt_root = copy_output("tampered_receipt_keyset")
    script_receipt = _load(receipt_root / "script_generation_receipt.json")
    del script_receipt["files"]["limitations.md"]
    _dump(receipt_root / "script_generation_receipt.json", script_receipt)
    validation = validate_new_banknote_authoritative_script_package(receipt_root)
    assert "script_generation_receipt_hashes_match" in validation["failed_checks"]

    retained_root = copy_output("tampered_retained_evidence")
    traceability = _load(retained_root / "cue_source_traceability.json")
    cue_008 = next(
        cue for cue in traceability["cues"] if cue["cue_id"] == "cue_008"
    )
    cue_008["retained_verified_unspoken_claims"][0]["supporting_evidence"][0][
        "exact_location"
    ] = "WRONG"
    _dump(retained_root / "cue_source_traceability.json", traceability)
    refresh_receipt_hashes(retained_root)
    validation = validate_new_banknote_authoritative_script_package(retained_root)
    assert (
        "cue_008_verified_unspoken_evidence_retained"
        in validation["failed_checks"]
    )
    assert "editorial_revision_receipt_hashes_match" not in validation["failed_checks"]
    assert "script_generation_receipt_hashes_match" not in validation["failed_checks"]

    manifest_root = copy_output("tampered_manifest_usage")
    manifest = _load(manifest_root / "source_to_script_manifest.json")
    manifest["sources"][0]["support_unit_ids"][0] = "wrong_unit"
    _dump(manifest_root / "source_to_script_manifest.json", manifest)
    refresh_receipt_hashes(manifest_root)
    validation = validate_new_banknote_authoritative_script_package(manifest_root)
    assert "source_to_script_manifest_exact" in validation["failed_checks"]
    assert "source_claim_manifest_edges_exact" not in validation["failed_checks"]
    assert "editorial_revision_receipt_hashes_match" not in validation["failed_checks"]
    assert "script_generation_receipt_hashes_match" not in validation["failed_checks"]


def test_package_ignore_rules_keep_local_evidence_private_and_csvs_trackable() -> None:
    patterns = set((PACKAGE / ".gitignore").read_text(encoding="utf-8").splitlines())
    assert {
        "local_outputs/",
        "source_cache/",
        "source_extracts/",
        "source_probe/",
        "!canonical_yymm4.csv",
        "!derived_yymm4_import.csv",
    } <= patterns

    for dirname in ("local_outputs", "source_cache", "source_extracts", "source_probe"):
        candidate = PACKAGE / dirname / "privacy-probe.bin"
        relative_candidate = repo_relative_path(REPO_ROOT, candidate)
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", "--", relative_candidate],
            cwd=REPO_ROOT,
            check=False,
        )
        assert ignored.returncode == 0, dirname
        relative_directory = repo_relative_path(REPO_ROOT, PACKAGE / dirname)
        tracked = subprocess.run(
            ["git", "ls-files", "--", relative_directory],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        assert tracked.returncode == 0
        assert not tracked.stdout.strip()

    for name in ("canonical_yymm4.csv", "derived_yymm4_import.csv"):
        relative_file = repo_relative_path(REPO_ROOT, PACKAGE / name)
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", "--", relative_file],
            cwd=REPO_ROOT,
            check=False,
        )
        assert ignored.returncode != 0, name
