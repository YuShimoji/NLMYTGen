"""Rebind Episode 002 state-dependent metadata without reading local media.

The verified-local-evidence pilot binds ``docs/runtime-state.md`` into its
source manifest.  A project-state transition therefore changes a three-file
metadata closure: the source manifest, its validation readback, and the
internal-review manifest's source snapshot/current-state pointer.  This module
updates only that closure and is intentionally independent of ``local_outputs``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from src.pipeline.verified_local_evidence_input_pilot import (
    validate_verified_local_evidence_input_pilot,
)


PACKAGE_RELATIVE = Path(
    "production_pilots/yukkuri_newsroom_content_spine_002"
)
PILOT_RELATIVE = PACKAGE_RELATIVE / "verified_local_evidence_input_pilot"
RUNTIME_STATE_RELATIVE = Path("docs/runtime-state.md")
SOURCE_MANIFEST_RELATIVE = PILOT_RELATIVE / "source_bundle_manifest.json"
INPUT_READBACK_RELATIVE = PILOT_RELATIVE / "input_validation_readback.json"
INTERNAL_REVIEW_MANIFEST_RELATIVE = (
    PILOT_RELATIVE / "internal_review_manifest.json"
)

STATE_FIELDS = (
    "Project-State-ID",
    "Product-State",
    "Product-Gate",
    "Recommended-Next",
    "External-State",
)


class Episode002IntegrationMetadataError(ValueError):
    """Raised when the bounded metadata closure is absent or malformed."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise Episode002IntegrationMetadataError(
            f"JSON_OBJECT_REQUIRED:{path.as_posix()}"
        )
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _runtime_state_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for field in STATE_FIELDS:
        matches = re.findall(rf"^{re.escape(field)}:\s*(\S+)\s*$", text, re.MULTILINE)
        if len(matches) != 1:
            raise Episode002IntegrationMetadataError(
                f"RUNTIME_STATE_FIELD_COUNT:{field}:{len(matches)}"
            )
        fields[field] = matches[0]
    return fields


def rebind_episode_002_integration_metadata(
    repo_root: str | Path,
) -> dict[str, Any]:
    """Update the deterministic three-file state-dependent metadata closure."""

    root = Path(repo_root).resolve()
    package = root / PACKAGE_RELATIVE
    pilot = root / PILOT_RELATIVE
    runtime_path = root / RUNTIME_STATE_RELATIVE
    source_path = root / SOURCE_MANIFEST_RELATIVE
    readback_path = root / INPUT_READBACK_RELATIVE
    review_path = root / INTERNAL_REVIEW_MANIFEST_RELATIVE
    closure = (source_path, readback_path, review_path)

    missing = [
        path.relative_to(root).as_posix() for path in closure + (runtime_path,) if not path.is_file()
    ]
    if missing:
        raise FileNotFoundError("INTEGRATION_METADATA_MISSING:" + ",".join(missing))

    runtime_text = runtime_path.read_text(encoding="utf-8")
    state = _runtime_state_fields(runtime_text)
    runtime_hash = _sha256(runtime_path)
    before = {
        path.relative_to(root).as_posix(): _sha256(path) for path in closure
    }

    source_manifest = _load_json(source_path)
    sources = source_manifest.get("sources")
    if not isinstance(sources, list):
        raise Episode002IntegrationMetadataError("SOURCE_MANIFEST_SOURCES_REQUIRED")
    runtime_sources = [
        item
        for item in sources
        if isinstance(item, dict) and item.get("source_id") == "runtime_state"
    ]
    if len(runtime_sources) != 1:
        raise Episode002IntegrationMetadataError(
            f"RUNTIME_SOURCE_COUNT:{len(runtime_sources)}"
        )
    runtime_source = runtime_sources[0]
    if runtime_source.get("repo_relative_path") != RUNTIME_STATE_RELATIVE.as_posix():
        raise Episode002IntegrationMetadataError("RUNTIME_SOURCE_PATH_MISMATCH")
    runtime_source["sha256"] = runtime_hash
    runtime_source["status"] = state["Project-State-ID"]
    _write_json(source_path, source_manifest)

    readback = validate_verified_local_evidence_input_pilot(
        pilot_dir=pilot,
        package_dir=package,
        require_input_readback=False,
    )
    if readback.get("status") != "passed":
        failures = ",".join(str(item) for item in readback.get("failed_checks", []))
        raise Episode002IntegrationMetadataError(
            "PILOT_VALIDATION_FAILED_BEFORE_READBACK_WRITE:" + failures
        )
    _write_json(readback_path, readback)
    final_readback = validate_verified_local_evidence_input_pilot(
        pilot_dir=pilot,
        package_dir=package,
        require_input_readback=True,
    )
    if final_readback.get("status") != "passed":
        failures = ",".join(
            str(item) for item in final_readback.get("failed_checks", [])
        )
        raise Episode002IntegrationMetadataError(
            "PILOT_VALIDATION_FAILED_AFTER_READBACK_WRITE:" + failures
        )

    review_manifest = _load_json(review_path)
    source_hashes = review_manifest.get("source_evidence_sha256")
    if not isinstance(source_hashes, dict):
        raise Episode002IntegrationMetadataError(
            "INTERNAL_REVIEW_SOURCE_HASHES_REQUIRED"
        )
    source_key = SOURCE_MANIFEST_RELATIVE.as_posix()
    if source_key not in source_hashes:
        raise Episode002IntegrationMetadataError(
            "INTERNAL_REVIEW_SOURCE_BUNDLE_KEY_MISSING"
        )
    source_hashes[source_key] = _sha256(source_path)
    review_manifest["achieved_state"] = {
        field: state[field] for field in STATE_FIELDS
    }
    _write_json(review_path, review_manifest)

    after = {
        path.relative_to(root).as_posix(): _sha256(path) for path in closure
    }
    changed = [path for path in before if before[path] != after[path]]
    return {
        "status": "passed",
        "runtime_state_sha256": runtime_hash,
        "selected_state": state,
        "metadata_before_sha256": before,
        "metadata_after_sha256": after,
        "changed_files": changed,
        "pilot_validation": final_readback["status"],
        "local_outputs_read": False,
        "media_regenerated": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rebind Episode 002 integration metadata without local media access."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    args = parser.parse_args(argv)
    result = rebind_episode_002_integration_metadata(args.repo_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
