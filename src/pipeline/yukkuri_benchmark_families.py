"""Validate the six-channel yukkuri benchmark-family registry.

The registry records observable format mechanics and reproduction progress.  It
does not authorize copying a creator's script, branding, media, voice, or other
protected expression, and it does not claim that an unfinished reproduction is
viewable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SCHEMA_VERSION = "nlmytgen.yukkuri_benchmark_families.v1"
REGISTRY_ID = "yukkuri-benchmark-families-v1-20260804"
DEFAULT_REGISTRY_PATH = Path(
    "production_pilots/yukkuri_benchmark_families_001/benchmark_families.json"
)

REQUIRED_OBSERVABLE_FIELDS = (
    "runtime_band_minutes",
    "narration_model",
    "chapter_model",
    "visual_grammar",
    "subtitle_grammar",
    "asset_switching",
    "audio_grammar",
    "pacing",
    "source_attribution",
    "intro_outro",
)
REQUIRED_NO_COPY_FIELDS = (
    "scripts",
    "logos_and_branding",
    "thumbnails",
    "creator_audio_and_voice",
    "creator_video_frames",
    "creator_owned_illustrations",
)
REPRODUCTION_STATUSES = {
    "channel_identity_locked_measurement_pending",
    "measured_contract_ready",
    "original_episode_building",
    "local_viewable_verified",
}


class BenchmarkRegistryError(ValueError):
    """Raised when a benchmark registry violates the v1 contract."""


def load_registry(path: str | Path = DEFAULT_REGISTRY_PATH) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise BenchmarkRegistryError("registry root must be an object")
    return data


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_registry(
    registry: dict[str, Any], *, root: str | Path | None = None
) -> dict[str, Any]:
    errors: list[str] = []
    if registry.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if registry.get("registry_id") != REGISTRY_ID:
        errors.append(f"registry_id must be {REGISTRY_ID}")

    channels = registry.get("channels")
    if not isinstance(channels, list):
        channels = []
        errors.append("channels must be an array")
    if len(channels) != 6:
        errors.append("registry must contain exactly six channels")

    channel_ids: list[str] = []
    channel_urls: list[str] = []
    family_ids: list[str] = []
    local_verified = 0

    for index, channel in enumerate(channels):
        prefix = f"channels[{index}]"
        if not isinstance(channel, dict):
            errors.append(f"{prefix} must be an object")
            continue
        channel_ids.append(str(channel.get("channel_id", "")))
        channel_urls.append(str(channel.get("official_channel_url", "")))
        family_ids.append(str(channel.get("format_family_id", "")))

        for field in (
            "channel_id",
            "channel_name",
            "official_channel_url",
            "format_family_id",
            "identity_evidence_url",
            "identity_checked_at",
        ):
            if not channel.get(field):
                errors.append(f"{prefix}.{field} is required")

        for field in ("official_channel_url", "identity_evidence_url"):
            value = str(channel.get(field, ""))
            parsed = urlparse(value)
            if parsed.scheme != "https" or parsed.netloc not in {
                "www.youtube.com",
                "youtube.com",
            }:
                errors.append(f"{prefix}.{field} must be an https YouTube URL")

        observables = channel.get("observable_contract")
        if not isinstance(observables, dict):
            errors.append(f"{prefix}.observable_contract must be an object")
        else:
            for field in REQUIRED_OBSERVABLE_FIELDS:
                if field not in observables:
                    errors.append(
                        f"{prefix}.observable_contract.{field} is required"
                    )

        reproduction = channel.get("reproduction")
        if not isinstance(reproduction, dict):
            errors.append(f"{prefix}.reproduction must be an object")
            continue
        status = reproduction.get("status")
        if status not in REPRODUCTION_STATUSES:
            errors.append(f"{prefix}.reproduction.status is invalid")
        if status == "local_viewable_verified":
            local_verified += 1
            artifact = reproduction.get("artifact")
            if not isinstance(artifact, dict):
                errors.append(f"{prefix}.reproduction.artifact is required")
            else:
                relative_path = artifact.get("relative_path")
                sha256 = artifact.get("sha256")
                receipt_path = artifact.get("receipt")
                if not relative_path or not sha256 or not receipt_path:
                    errors.append(
                        f"{prefix}.reproduction.artifact needs relative_path, sha256, and receipt"
                    )
                elif root is not None:
                    root_path = Path(root)
                    live_artifact = root_path / relative_path
                    tracked_receipt = root_path / receipt_path
                    if live_artifact.is_file():
                        if _sha256_file(live_artifact) != sha256:
                            errors.append(
                                f"{prefix}.reproduction.artifact sha256 mismatch"
                            )
                    elif not tracked_receipt.is_file():
                        errors.append(
                            f"{prefix}.reproduction.artifact file and receipt do not exist"
                        )
                    else:
                        try:
                            receipt = json.loads(
                                tracked_receipt.read_text(encoding="utf-8")
                            )
                            receipt_video = receipt["video"]
                            if not isinstance(receipt_video, dict):
                                raise TypeError("receipt.video must be an object")
                            receipt_bound_path = (
                                Path(receipt_path).parent / receipt_video["path"]
                            ).as_posix()
                            if (
                                receipt_video.get("sha256") != sha256
                                or receipt_bound_path != Path(relative_path).as_posix()
                            ):
                                errors.append(
                                    f"{prefix}.reproduction.artifact receipt mismatch"
                                )
                        except (KeyError, TypeError, ValueError):
                            errors.append(
                                f"{prefix}.reproduction.artifact receipt is invalid"
                            )

    for values, label in (
        (channel_ids, "channel_id"),
        (channel_urls, "official_channel_url"),
        (family_ids, "format_family_id"),
    ):
        non_empty = [value for value in values if value]
        if len(set(non_empty)) != len(non_empty):
            errors.append(f"{label} values must be unique")

    no_copy = registry.get("no_copy_policy")
    if not isinstance(no_copy, dict):
        errors.append("no_copy_policy must be an object")
    else:
        for field in REQUIRED_NO_COPY_FIELDS:
            if no_copy.get(field) is not True:
                errors.append(f"no_copy_policy.{field} must be true")

    authority = registry.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority must be an object")
        local_production_authorized = False
        publication_authorized = False
    else:
        local_production_authorized = (
            authority.get("local_production_authorized") is True
        )
        publication_authorized = authority.get("publication_authorized") is True
        if not local_production_authorized:
            errors.append("authority.local_production_authorized must be true")
        if publication_authorized:
            errors.append("authority.publication_authorized must be false")

    return {
        "registry_id": registry.get("registry_id"),
        "schema_version": registry.get("schema_version"),
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "channel_count": len(channels),
        "unique_channel_count": len(set(channel_ids)),
        "unique_format_family_count": len(set(family_ids)),
        "local_viewable_verified_count": local_verified,
        "remaining_local_viewable_count": max(0, 6 - local_verified),
        "local_production_authorized": local_production_authorized,
        "public_release_authorized": publication_authorized,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the six-channel yukkuri benchmark registry."
    )
    parser.add_argument("registry", nargs="?", default=str(DEFAULT_REGISTRY_PATH))
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    result = validate_registry(load_registry(args.registry), root=args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
