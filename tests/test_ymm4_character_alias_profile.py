from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import pytest

from src.pipeline.ymm4_character_alias_profile import (
    PROFILE_SCHEMA_VERSION,
    build_derived_yymm4_import_csv,
    load_yymm4_character_alias_profile,
    read_headerless_yymm4_csv,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
EPISODE_ROOT = (
    REPO_ROOT
    / "production_pilots"
    / "yukkuri_newsroom_content_spine_002"
)
PROFILE_PATH = (
    EPISODE_ROOT
    / "ymm4_character_alias_profiles"
    / "ymm4_4_53_0_9_yukkuri_characters_v1.json"
)
CANONICAL_CSV = (
    EPISODE_ROOT
    / "transcript_substitution_readiness"
    / "regenerated_draft_yymm4.csv"
)
EXPECTED_CANONICAL_SHA256 = (
    "6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C"
)
EXPECTED_CANONICAL_SPEAKERS = [
    "れいむ",
    "まりさ",
    "まりさ",
    "まりさ",
    "れいむ",
    "まりさ",
    "まりさ",
    "れいむ",
    "まりさ",
]
EXPECTED_YMM4_CHARACTERS = [
    "ゆっくり霊夢" if speaker == "れいむ" else "ゆっくり魔理沙"
    for speaker in EXPECTED_CANONICAL_SPEAKERS
]


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest().upper()


def _build_episode_derived_csv(output_path: Path) -> dict:
    return build_derived_yymm4_import_csv(
        canonical_csv=CANONICAL_CSV,
        derived_csv=output_path,
        profile_path=PROFILE_PATH,
        repo_root=REPO_ROOT,
        expected_canonical_sha256=EXPECTED_CANONICAL_SHA256,
    )


def test_episode_profile_parses_as_explicit_strict_environment_profile() -> None:
    profile = load_yymm4_character_alias_profile(PROFILE_PATH)

    assert profile["schema_version"] == PROFILE_SCHEMA_VERSION
    assert profile["profile_id"] == "ymm4_4_53_0_9_yukkuri_characters_ja_v1"
    assert profile["selection_policy"] == "explicit_only"
    assert profile["strict_coverage"] is True
    assert profile["universal_default_claimed"] is False
    assert profile["canonical_to_yymm4_character"] == {
        "れいむ": "ゆっくり霊夢",
        "まりさ": "ゆっくり魔理沙",
    }

    environment = profile["observed_environment"]
    assert environment["yymm4_version"] == "4.53.0.9"
    receipt_path = REPO_ROOT / environment["observation_receipt"]
    assert receipt_path.is_file()
    assert _sha256(receipt_path.read_bytes()) == environment["observation_receipt_sha256"]


def test_strict_profile_rejects_unmapped_canonical_speaker_without_output(
    tmp_path: Path,
) -> None:
    canonical_csv = tmp_path / "canonical_with_unmapped.csv"
    with canonical_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerows(
            [
                ["れいむ", "mapped"],
                ["ナレーター", "must fail rather than pass through"],
            ]
        )
    derived_csv = tmp_path / "derived.csv"

    with pytest.raises(
        ValueError,
        match="unmapped canonical speakers: ナレーター",
    ):
        build_derived_yymm4_import_csv(
            canonical_csv=canonical_csv,
            derived_csv=derived_csv,
            profile_path=PROFILE_PATH,
            repo_root=REPO_ROOT,
        )

    assert not derived_csv.exists()


def test_episode_derivation_leaves_canonical_csv_bytes_and_sha_unchanged(
    tmp_path: Path,
) -> None:
    canonical_before = CANONICAL_CSV.read_bytes()
    assert _sha256(canonical_before) == EXPECTED_CANONICAL_SHA256

    readback = _build_episode_derived_csv(tmp_path / "derived.csv")

    canonical_after = CANONICAL_CSV.read_bytes()
    assert canonical_after == canonical_before
    assert _sha256(canonical_after) == EXPECTED_CANONICAL_SHA256
    assert readback["canonical_csv"]["sha256"] == EXPECTED_CANONICAL_SHA256
    assert readback["canonical_csv"]["expected_sha256"] == EXPECTED_CANONICAL_SHA256
    assert readback["checks"]["canonical_sha256_matches_expected"] is True


def test_episode_derivation_preserves_nine_texts_and_order_and_projects_characters(
    tmp_path: Path,
) -> None:
    derived_csv = tmp_path / "derived.csv"
    readback = _build_episode_derived_csv(derived_csv)
    canonical = read_headerless_yymm4_csv(CANONICAL_CSV)
    derived = read_headerless_yymm4_csv(derived_csv)

    assert canonical["row_count"] == derived["row_count"] == 9
    assert [row["row_number"] for row in derived["rows"]] == list(range(1, 10))
    assert [row["speaker"] for row in canonical["rows"]] == EXPECTED_CANONICAL_SPEAKERS
    assert [row["speaker"] for row in derived["rows"]] == EXPECTED_YMM4_CHARACTERS
    assert [row["text"] for row in derived["rows"]] == [
        row["text"] for row in canonical["rows"]
    ]

    crosswalk = readback["row_crosswalk"]
    assert [row["row_number"] for row in crosswalk] == list(range(1, 10))
    assert [row["canonical_speaker"] for row in crosswalk] == EXPECTED_CANONICAL_SPEAKERS
    assert [row["yymm4_character"] for row in crosswalk] == EXPECTED_YMM4_CHARACTERS
    assert readback["checks"]["strict_coverage_satisfied"] is True
    assert readback["checks"]["unmapped_canonical_speakers"] == []
    assert readback["checks"]["row_count_preserved"] is True
    assert readback["checks"]["text_and_order_preserved"] is True
    assert readback["checks"]["speaker_projection_matches_profile"] is True
    assert readback["checks"]["only_speaker_column_changed"] is True


def test_episode_derivation_preserves_headerless_utf8_two_column_shape(
    tmp_path: Path,
) -> None:
    derived_csv = tmp_path / "derived.csv"
    readback = _build_episode_derived_csv(derived_csv)
    canonical = read_headerless_yymm4_csv(CANONICAL_CSV)
    derived = read_headerless_yymm4_csv(derived_csv)

    assert canonical["encoding"] == derived["encoding"] == "utf-8"
    assert canonical["has_utf8_bom"] is derived["has_utf8_bom"] is False
    assert not derived_csv.read_bytes().startswith(b"\xef\xbb\xbf")
    with derived_csv.open("r", encoding=derived["encoding"], newline="") as handle:
        rows = list(csv.reader(handle))
    assert len(rows) == 9
    assert all(len(row) == 2 for row in rows)
    assert rows[0][0] == "ゆっくり霊夢"
    assert rows[0][0] not in {"speaker", "character", "yymm4_character"}
    assert readback["checks"]["headerless_two_column_shape"] is True
    assert readback["checks"]["encoding_compatibility_preserved"] is True


def test_episode_derivation_is_byte_deterministic(tmp_path: Path) -> None:
    first_csv = tmp_path / "first.csv"
    second_csv = tmp_path / "second.csv"

    first = _build_episode_derived_csv(first_csv)
    second = _build_episode_derived_csv(second_csv)

    assert first_csv.read_bytes() == second_csv.read_bytes()
    assert first["derived_csv"]["sha256"] == second["derived_csv"]["sha256"]
    assert first["row_crosswalk"] == second["row_crosswalk"]
    assert first["checks"] == second["checks"]
