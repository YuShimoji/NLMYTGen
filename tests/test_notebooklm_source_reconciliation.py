from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from src.pipeline.notebooklm_source_reconciliation import (
    ALIGNMENT_RECORD_FIELDS,
    PRIMARY_OFFICIAL_CANDIDATE_IDS,
    REQUIRED_SOURCE_FIELDS,
    REQUIRED_SOURCE_RECONCILIATION_FILES,
    USER_PROVIDED_SOURCE_SNAPSHOT,
    build_notebooklm_source_reconciliation,
    main,
    normalize_source_title,
    source_title_fingerprint,
    validate_notebooklm_source_reconciliation,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = (
    REPO_ROOT
    / "production_pilots/yukkuri_newsroom_content_spine_002"
    / "external_editorial_input/new_banknote_security_notebooklm_001"
)
CLAIM_LEDGER = PACKAGE / "claim_risk_ledger.json"
LOCAL_LINE_MAP = PACKAGE / "local_outputs/raw_line_map.json"
RAW = (
    REPO_ROOT
    / "production_pilots/yukkuri_newsroom_content_spine_002"
    / "real_input_intake_readiness/real_input/transcript/new_banknote_notebooklm"
    / "raw/notebooklm_audio_overview_transcript_raw.txt"
)
EXPECTED_TITLES = [
    "【新紙幣を完全解説】世界初の3Dホログラムで偽造防止、キャッシュレス化のなか新紙幣の効果とは - JBpress",
    'このタイミングで新紙幣発表"本当の狙い" キャッシュレス化とは矛盾しない',
    "テーマ：新紙幣の経済的影響とキャッシュレス化",
    "新しい日本銀行券 「開発秘話」 - 国立印刷局",
    "新しい日本銀行券の偽造防止技術 [PDF 572KB]",
    "新紙幣に採用された3Dホログラムとホログラム映像 何が違う？ - ユピテル",
    "新紙幣に隠されたキャッシュレスの罠.m4a",
    "注目のキーワード「改刷」",
    "紙切れを価値に変える1000年の知略：3Dホログラムが描く偽造防止の最前線 - note",
    "紙幣の肖像と図柄について、選定理由を教えてください - 財務省",
    "識別性向上に向けた取組 - 国立印刷局",
]
EXPECTED_TITLE_FINGERPRINTS = [
    "a6946a67bce2a272f0ce5285a7b24c737f37e22cb210d2ac1285da14b790bf6b",
    "18780f3929524227db5d4db93f7be8eb875c6037701d7b05787e30bfbfaae946",
    "4e720c50ce731e67b3ac168342171a456f81a23d988be6d078a8e29e413caaa2",
    "91e44821571d60f53c5aacf5b60b7b77b04ef7accce0016fe42b718a34229452",
    "13757d7a14c601493e26192a5f01e632abda36d3cf22ca0adb35b30bca3bdb0f",
    "6d33776e264b7ff8fb6f56e026b39a3303ab11f7faf5a3e33b6801d60ea98630",
    "39603ea15483e3fe82d5e419dd278bea8ffad7916dcc08e612d951e6d54dcdd8",
    "503e66926c1a72218aa9e1386a56ce7900d1f6174385f79cf821e94802432341",
    "49223689f56d3a66037b5bab7b77de2aa4198d5b112921d730909a192e349d0d",
    "7ad232c235f05a2e8129029c4c5d773b1fe861676abb044781a05fe3d92f247b",
    "ca385f29259b83aa8c2170799af7eb005f5c78bf52a08d6b7dd7756e11cee301",
]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _tree_hashes(root: Path) -> dict[str, str]:
    return {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest()
        for name in REQUIRED_SOURCE_RECONCILIATION_FILES
    }


def _all_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {
            key
            for child in value.values()
            for key in _all_keys(child)
        }
    if isinstance(value, list):
        return {key for child in value for key in _all_keys(child)}
    return set()


@pytest.fixture
def generated(tmp_path: Path) -> Path:
    if not LOCAL_LINE_MAP.exists():
        validate_notebooklm_source_reconciliation(PACKAGE)
        return PACKAGE
    output = tmp_path / "source_reconciliation"
    build_notebooklm_source_reconciliation(
        claim_ledger_path=CLAIM_LEDGER,
        output_dir=output,
    )
    return output


def test_exact_title_snapshot_fingerprints_and_authority_boundaries(
    generated: Path,
) -> None:
    snapshot = _load(generated / "source_set_snapshot.json")
    sources = snapshot["sources"]
    assert [source["source_id"] for source in sources] == [
        f"S{index:02d}" for index in range(1, 12)
    ]
    assert [source["exact_title"] for source in sources] == EXPECTED_TITLES
    assert [source["title_fingerprint"] for source in sources] == (
        EXPECTED_TITLE_FINGERPRINTS
    )
    assert [spec.exact_title for spec in USER_PROVIDED_SOURCE_SNAPSHOT] == EXPECTED_TITLES
    assert all(set(source) == set(REQUIRED_SOURCE_FIELDS) for source in sources)
    assert len(set(EXPECTED_TITLE_FINGERPRINTS)) == 11
    assert source_title_fingerprint("Ａ  B") == hashlib.sha256(
        normalize_source_title("A B").encode("utf-8")
    ).hexdigest()

    chronology = _load(generated / "source_chronology_readback.json")
    assert chronology["generation_time_count"] == 10
    assert chronology["post_generation_derived_count"] == 1
    assert chronology["post_generation_derived_source_ids"] == ["S07"]
    assert chronology["provisional_generation_time_source_ids"] == ["S03"]
    assert chronology["raw_transcript"]["included_in_source_set"] is False

    authority = _load(generated / "source_authority_matrix.json")
    assert authority["primary_official_candidate_source_ids"] == list(
        PRIMARY_OFFICIAL_CANDIDATE_IDS
    )
    by_id = {item["source_id"]: item for item in authority["entries"]}
    assert by_id["S03"]["factual_authority_policy"] == (
        "non_independent_excluded_from_factual_verification"
    )
    assert by_id["S07"]["factual_authority_policy"] == "excluded"
    assert by_id["S08"]["authority_class"] == "publisher_unresolved_title_only"


def test_all_claims_are_aligned_without_verification(generated: Path) -> None:
    ledger = _load(CLAIM_LEDGER)
    payload = _load(generated / "claim_source_family_alignment.json")
    alignments = payload["alignments"]
    assert payload["claim_alignment_count"] == 182
    assert payload["verified_claim_count"] == 0
    assert payload["derived_audio_factual_use"] is False
    assert len(alignments) == len(ledger["claims"]) == 182
    assert [item["claim_id"] for item in alignments] == [
        item["claim_id"] for item in ledger["claims"]
    ]
    assert [item["line_fingerprint"] for item in alignments] == [
        item["line_fingerprint"] for item in ledger["claims"]
    ]
    assert [item["risk_class"] for item in alignments] == [
        item["risk"] for item in ledger["claims"]
    ]
    assert all(set(item) == ALIGNMENT_RECORD_FIELDS for item in alignments)
    assert all(item["verification_status"] == "unverified" for item in alignments)
    assert all("S07" not in item["likely_source_ids"] for item in alignments)
    assert all(
        item["derived_provenance_source_ids"] == ["S07"]
        for item in alignments
        if item["claim_class"]
        in {
            "analogy_or_metaphor",
            "rhetorical_framing",
        }
    )

    if payload["topic_labeling"]["local_line_map_used"]:
        assert payload["topic_labeling"]["claim_line_coverage"] == 182
        assert payload["topic_family_counts"] == {
            "cashless_policy_intent": 11,
            "history_keyword": 9,
            "anti_counterfeit_technology": 48,
            "portrait_design_selection": 2,
            "accessibility_identification": 27,
        }
        assert payload["topic_labeled_claim_count"] == 87
        assert payload["topic_unlabeled_claim_count"] == 95
        technical = [
            item for item in alignments if item["claim_class"] == "technical_description"
        ]
        anti_only = [
            item
            for item in technical
            if item["topic_family_labels"] == ["anti_counterfeit_technology"]
        ]
        accessibility_only = [
            item
            for item in technical
            if item["topic_family_labels"] == ["accessibility_identification"]
        ]
        portrait = [
            item
            for item in technical
            if "portrait_design_selection" in item["topic_family_labels"]
        ]
        assert anti_only and accessibility_only and portrait
        assert all(
            item["likely_source_ids"] == ["S04", "S05", "S06"]
            for item in anti_only
        )
        assert all(
            item["likely_source_ids"] == ["S04", "S11"]
            for item in accessibility_only
        )
        assert all("S10" in item["likely_source_ids"] for item in portrait)
        assert all(
            "S11" not in item["likely_source_ids"]
            for item in portrait
            if "accessibility_identification"
            not in item["topic_family_labels"]
        )
        cashless_causal = [
            item
            for item in alignments
            if item["claim_class"] == "causal_claim"
            and "cashless_policy_intent" in item["topic_family_labels"]
        ]
        assert len(cashless_causal) == 2
        assert all(item["risk_class"] == "high" for item in cashless_causal)
        assert all(
            set(item["likely_source_ids"]) == {"S01", "S02", "S03", "S08", "S09"}
            for item in cashless_causal
        )
        assert all(
            "independent" in item["required_authority_class"]
            for item in cashless_causal
        )

    policy_and_causal = [
        item
        for item in alignments
        if item["claim_class"] in {"policy_or_intent_claim", "causal_claim"}
    ]
    assert policy_and_causal
    assert all(item["risk_class"] == "high" for item in policy_and_causal)
    assert all(
        "independent" in item["required_authority_class"]
        for item in policy_and_causal
    )
    policy_rules = payload["source_family_rules"]["policy_or_intent_claim"]
    assert policy_rules["base_likely_source_ids"] == [
        "S01",
        "S02",
        "S03",
        "S08",
        "S09",
    ]
    quantitative = [
        item for item in alignments if item["claim_class"] == "quantitative_statistic"
    ]
    assert len(quantitative) == 35
    for item in quantitative:
        dependency = item["source_resolution_dependency"]
        assert all(
            token in dependency
            for token in ("source_identity", "page_or_field", "publication_date", "unit")
        )
        assert item["reject_if_unverified"] is True


def test_reconciliation_readback_backlog_and_derived_exclusion(
    generated: Path,
) -> None:
    readback = _load(generated / "source_set_reconciliation_readback.json")
    assert readback == {
        **readback,
        "status": "source_set_frozen_title_level",
        "source_count": 11,
        "generation_time_count": 10,
        "derived_count": 1,
        "primary_official_candidate_count": 4,
        "claim_alignment_count": 182,
        "verified_claim_count": 0,
        "unresolved_source_count": 10,
        "private_link_tracking": False,
        "notebook_reference_access_verified": False,
        "notebook_reference_tracked": False,
    }
    assert readback["source_title_coverage"] == {
        "covered": 11,
        "expected": 11,
        "complete": True,
    }
    assert readback["claim_coverage"] == {
        "covered": 182,
        "expected": 182,
        "complete": True,
    }

    backlog = _load(generated / "source_resolution_backlog.json")
    priorities = {
        item["source_id"]: item["priority"] for item in backlog["entries"]
    }
    assert {key for key, value in priorities.items() if value == "P0"} == {
        "S04",
        "S05",
        "S10",
        "S11",
    }
    assert priorities["S07"] == "excluded"
    assert all(
        item["next_action"] == "defer_to_H1_authoritative_source_resolution"
        for item in backlog["entries"]
        if item["source_id"] != "S07"
    )
    derived = _load(generated / "derived_source_exclusion.json")
    assert derived["excluded_source_ids"] == ["S07"]
    assert derived["excluded_sources"][0]["factual_authority_use"] is False


@pytest.mark.skipif(
    not LOCAL_LINE_MAP.exists(),
    reason="canonical lexical topic input is intentionally ignored local evidence",
)
def test_generation_is_deterministic_and_cli_validates(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    build_notebooklm_source_reconciliation(
        claim_ledger_path=CLAIM_LEDGER,
        output_dir=first,
    )
    build_notebooklm_source_reconciliation(
        claim_ledger_path=CLAIM_LEDGER,
        output_dir=second,
    )
    first_hashes = _tree_hashes(first)
    assert first_hashes == _tree_hashes(second)
    build_notebooklm_source_reconciliation(
        claim_ledger_path=CLAIM_LEDGER,
        output_dir=first,
    )
    assert first_hashes == _tree_hashes(first)
    assert validate_notebooklm_source_reconciliation(first)["claim_alignment_count"] == 182

    cli_output = tmp_path / "cli"
    assert main(
        [
            "--claim-ledger",
            str(CLAIM_LEDGER),
            "--output",
            str(cli_output),
        ]
    ) == 0
    assert json.loads(capsys.readouterr().out)["status"] == (
        "source_set_frozen_title_level"
    )


@pytest.mark.skipif(
    not LOCAL_LINE_MAP.exists(),
    reason="canonical lexical topic input is intentionally ignored local evidence",
)
def test_tracked_package_matches_fresh_canonical_generation(tmp_path: Path) -> None:
    fresh = tmp_path / "fresh"
    build_notebooklm_source_reconciliation(
        claim_ledger_path=CLAIM_LEDGER,
        output_dir=fresh,
        local_line_map_path=LOCAL_LINE_MAP,
    )
    assert validate_notebooklm_source_reconciliation(PACKAGE)[
        "claim_alignment_count"
    ] == 182
    assert _tree_hashes(PACKAGE) == _tree_hashes(fresh)


@pytest.mark.skipif(
    not LOCAL_LINE_MAP.exists(),
    reason="canonical lexical topic input is intentionally ignored local evidence",
)
def test_local_line_map_text_fingerprint_is_recomputed(
    tmp_path: Path,
) -> None:
    mutated = _load(LOCAL_LINE_MAP)
    mutated["lines"][0]["raw_text"] += "mutation"
    mutated_path = tmp_path / "mutated_line_map.json"
    mutated_path.write_text(
        json.dumps(mutated, ensure_ascii=False),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="raw_text fingerprint mismatch"):
        build_notebooklm_source_reconciliation(
            claim_ledger_path=CLAIM_LEDGER,
            output_dir=tmp_path / "output",
            local_line_map_path=mutated_path,
        )


def test_generated_package_has_no_private_reference_or_transcript_payload(
    generated: Path,
) -> None:
    combined = "\n".join(
        (generated / name).read_text(encoding="utf-8")
        for name in REQUIRED_SOURCE_RECONCILIATION_FILES
    )
    assert "notebooklm.google.com" not in combined.lower()
    assert "C:\\Users\\" not in combined
    assert "/Users/" not in combined
    assert "/home/" not in combined
    assert not re.search(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        combined,
        flags=re.IGNORECASE,
    )
    alignment_keys = _all_keys(
        _load(generated / "claim_source_family_alignment.json")
    )
    assert not {"raw_text", "claim_text", "transcript_text", "excerpt"} & (
        alignment_keys
    )

    if RAW.exists():
        comparison_text = "\n".join(
            (generated / name).read_text(encoding="utf-8")
            for name in REQUIRED_SOURCE_RECONCILIATION_FILES
        )
        for line in RAW.read_text(encoding="utf-8").splitlines():
            assert not any(
                line[index : index + 80] in comparison_text
                for index in range(max(0, len(line) - 79))
            )
