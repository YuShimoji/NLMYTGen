"""Explicit canonical-speaker to installed-YMM4-character projection.

The generic ``build-csv`` speaker map normalizes source labels into canonical
speaker identities.  This module is deliberately separate: it projects those
canonical identities into character names observed in one YMM4 environment.
It never silently passes through an unmapped canonical speaker.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


PROFILE_SCHEMA_VERSION = "ymm4_character_alias_profile.v1"
DERIVATION_READBACK_SCHEMA_VERSION = "ymm4_character_alias_derivation_readback.v1"


def load_yymm4_character_alias_profile(path: str | Path) -> dict[str, Any]:
    """Load and validate an explicitly selected YMM4 character profile."""
    profile_path = Path(path)
    if not profile_path.exists():
        raise FileNotFoundError(f"YMM4 character alias profile not found: {profile_path}")
    try:
        payload = json.loads(profile_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"YMM4 character alias profile is not valid JSON: {profile_path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("YMM4 character alias profile must be a JSON object")
    if payload.get("schema_version") != PROFILE_SCHEMA_VERSION:
        raise ValueError(
            "YMM4 character alias profile schema mismatch: "
            f"expected {PROFILE_SCHEMA_VERSION}"
        )
    if not str(payload.get("profile_id") or "").strip():
        raise ValueError("YMM4 character alias profile_id is required")
    if payload.get("selection_policy") != "explicit_only":
        raise ValueError("YMM4 character alias profile must use selection_policy=explicit_only")
    if payload.get("strict_coverage") is not True:
        raise ValueError("YMM4 character alias profile must use strict_coverage=true")
    if payload.get("universal_default_claimed") is not False:
        raise ValueError("YMM4 character alias profile must not claim a universal default")

    aliases = payload.get("canonical_to_yymm4_character")
    if not isinstance(aliases, dict) or not aliases:
        raise ValueError("YMM4 character alias profile requires a non-empty alias map")
    for canonical, character in aliases.items():
        if not isinstance(canonical, str) or not canonical.strip():
            raise ValueError("YMM4 character alias keys must be non-empty strings")
        if not isinstance(character, str) or not character.strip():
            raise ValueError("YMM4 character alias values must be non-empty strings")

    observed_environment = payload.get("observed_environment")
    if not isinstance(observed_environment, dict):
        raise ValueError("YMM4 character alias profile requires observed_environment metadata")
    if not str(observed_environment.get("yymm4_version") or "").strip():
        raise ValueError("YMM4 character alias profile requires observed YMM4 version metadata")
    return payload


def read_headerless_yymm4_csv(path: str | Path) -> dict[str, Any]:
    """Read a two-column headerless YMM4 CSV while recording encoding shape."""
    csv_path = Path(path)
    raw = csv_path.read_bytes()
    has_utf8_bom = raw.startswith(b"\xef\xbb\xbf")
    encoding = "utf-8-sig" if has_utf8_bom else "utf-8"
    rows: list[dict[str, Any]] = []
    with csv_path.open("r", encoding=encoding, newline="") as handle:
        reader = csv.reader(handle)
        for row_number, row in enumerate(reader, start=1):
            if len(row) != 2:
                raise ValueError(
                    f"YMM4 CSV row {row_number} must contain exactly two columns; got {len(row)}"
                )
            speaker, text = row
            if not speaker:
                raise ValueError(f"YMM4 CSV row {row_number} has an empty speaker")
            rows.append(
                {
                    "row_number": row_number,
                    "speaker": speaker,
                    "text": text,
                }
            )
    if not rows:
        raise ValueError("YMM4 CSV must contain at least one row")
    first = rows[0]
    if str(first["speaker"]).strip().lower() == "speaker" and str(first["text"]).strip().lower() == "text":
        raise ValueError("YMM4 CSV must be headerless")
    return {
        "path": csv_path,
        "rows": rows,
        "row_count": len(rows),
        "encoding": encoding,
        "has_utf8_bom": has_utf8_bom,
        "sha256": hashlib.sha256(raw).hexdigest().upper(),
    }


def build_derived_yymm4_import_csv(
    *,
    canonical_csv: str | Path,
    derived_csv: str | Path,
    profile_path: str | Path,
    repo_root: str | Path,
    expected_canonical_sha256: str | None = None,
) -> dict[str, Any]:
    """Project canonical speakers through a strict profile and write a new CSV."""
    root = Path(repo_root).resolve()
    canonical_path = Path(canonical_csv).resolve()
    derived_path = Path(derived_csv).resolve()
    selected_profile_path = Path(profile_path).resolve()
    if canonical_path == derived_path:
        raise ValueError("Derived YMM4 CSV must not overwrite the canonical CSV")
    try:
        selected_profile_path.relative_to(root)
    except ValueError as exc:
        raise ValueError("YMM4 character alias profile must be inside the repository") from exc
    profile = load_yymm4_character_alias_profile(selected_profile_path)
    canonical = read_headerless_yymm4_csv(canonical_path)

    expected_hash = str(expected_canonical_sha256 or "").upper()
    if expected_hash and canonical["sha256"] != expected_hash:
        raise ValueError(
            "Canonical YMM4 CSV SHA-256 mismatch: "
            f"expected {expected_hash}, got {canonical['sha256']}"
        )

    observed_environment = dict(profile["observed_environment"])
    receipt_reference = str(observed_environment.get("observation_receipt") or "")
    receipt_expected_hash = str(observed_environment.get("observation_receipt_sha256") or "").upper()
    if not receipt_reference or not receipt_expected_hash:
        raise ValueError("YMM4 character alias profile requires observation receipt provenance")
    receipt_path = (root / receipt_reference).resolve()
    try:
        receipt_path.relative_to(root)
    except ValueError as exc:
        raise ValueError("YMM4 character alias profile receipt must be inside the repository") from exc
    if not receipt_path.exists():
        raise FileNotFoundError(f"YMM4 character alias profile receipt not found: {receipt_path}")
    receipt_actual_hash = hashlib.sha256(receipt_path.read_bytes()).hexdigest().upper()
    if receipt_actual_hash != receipt_expected_hash:
        raise ValueError("YMM4 character alias profile observation receipt SHA-256 mismatch")

    aliases = dict(profile["canonical_to_yymm4_character"])
    canonical_speakers = {str(row["speaker"]) for row in canonical["rows"]}
    unmapped = sorted(canonical_speakers - set(aliases))
    if unmapped:
        raise ValueError(
            "YMM4 character alias profile has unmapped canonical speakers: "
            + ", ".join(unmapped)
        )

    derived_rows = [
        {
            "row_number": row["row_number"],
            "canonical_speaker": row["speaker"],
            "yymm4_character": aliases[row["speaker"]],
            "text": row["text"],
        }
        for row in canonical["rows"]
    ]
    derived_path.parent.mkdir(parents=True, exist_ok=True)
    output_encoding = "utf-8-sig" if canonical["has_utf8_bom"] else "utf-8"
    with derived_path.open("w", encoding=output_encoding, newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerows(
            [row["yymm4_character"], row["text"]]
            for row in derived_rows
        )

    derived = read_headerless_yymm4_csv(derived_path)
    canonical_after = read_headerless_yymm4_csv(canonical_path)
    source_texts = [row["text"] for row in canonical["rows"]]
    derived_texts = [row["text"] for row in derived["rows"]]
    expected_characters = [row["yymm4_character"] for row in derived_rows]
    derived_characters = [row["speaker"] for row in derived["rows"]]
    checks = {
        "canonical_sha256_matches_expected": not expected_hash or canonical["sha256"] == expected_hash,
        "canonical_source_unchanged": canonical_after["sha256"] == canonical["sha256"],
        "strict_coverage_enabled": profile.get("strict_coverage") is True,
        "strict_coverage_satisfied": not unmapped,
        "unmapped_canonical_speakers": unmapped,
        "row_count_preserved": derived["row_count"] == canonical["row_count"],
        "text_and_order_preserved": derived_texts == source_texts,
        "speaker_projection_matches_profile": derived_characters == expected_characters,
        "only_speaker_column_changed": (
            derived["row_count"] == canonical["row_count"]
            and derived_texts == source_texts
            and derived_characters == expected_characters
        ),
        "headerless_two_column_shape": True,
        "encoding_compatibility_preserved": (
            derived["encoding"] == canonical["encoding"]
            and derived["has_utf8_bom"] == canonical["has_utf8_bom"]
        ),
    }
    if not all(value is True for key, value in checks.items() if key != "unmapped_canonical_speakers"):
        raise ValueError("Derived YMM4 CSV validation failed")

    return {
        "schema_version": DERIVATION_READBACK_SCHEMA_VERSION,
        "status": "passed",
        "profile": {
            "profile_id": profile["profile_id"],
            "schema_version": profile["schema_version"],
            "repo_relative_path": _relative(selected_profile_path, root),
            "selection_policy": profile["selection_policy"],
            "strict_coverage": profile["strict_coverage"],
            "universal_default_claimed": profile["universal_default_claimed"],
            "observed_environment": profile["observed_environment"],
            "profile_sha256": hashlib.sha256(selected_profile_path.read_bytes()).hexdigest().upper(),
            "observation_receipt_sha256_verified": receipt_actual_hash,
        },
        "canonical_csv": {
            "repo_relative_path": _relative(canonical_path, root),
            "sha256": canonical["sha256"],
            "expected_sha256": expected_hash,
            "row_count": canonical["row_count"],
            "encoding": canonical["encoding"],
            "has_utf8_bom": canonical["has_utf8_bom"],
            "canonical_speakers": sorted(canonical_speakers),
        },
        "derived_csv": {
            "repo_relative_path": _relative(derived_path, root),
            "sha256": derived["sha256"],
            "row_count": derived["row_count"],
            "encoding": derived["encoding"],
            "has_utf8_bom": derived["has_utf8_bom"],
            "yymm4_characters": sorted(set(derived_characters)),
        },
        "checks": checks,
        "row_crosswalk": [
            {
                "row_number": row["row_number"],
                "canonical_speaker": row["canonical_speaker"],
                "yymm4_character": row["yymm4_character"],
                "text_sha256": hashlib.sha256(row["text"].encode("utf-8")).hexdigest().upper(),
            }
            for row in derived_rows
        ],
    }


def _relative(path: Path, root: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError:
        return resolved.as_posix()
