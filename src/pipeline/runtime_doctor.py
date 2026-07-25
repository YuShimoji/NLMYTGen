"""Read-only runtime and private-artifact readiness doctor.

The doctor observes tools and exact artifact identities.  It never treats a
historical receipt as proof that private bytes are currently available, and it
never copies, replaces, deletes, launches YMM4, renders, or plays media.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
from typing import Any, Iterable, Mapping, Sequence

from src.pipeline.media_validation import probe_with_ffprobe
from src.pipeline.silent_media_runtime import SilentPolicyError, resolve_audio_policy


SCHEMA = "nlmytgen.runtime_doctor_result.v1"
CONTRACT_SCHEMA = "nlmytgen.private_artifact_ingest_contract.v1"
CONTRACT_RELATIVE_PATH = (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001/"
    "auto_video_pipeline/new_banknote_private_artifact_ingest_contract.json"
)
ELECTRON_AUTHORITY_PATH = "docs/verification/ELECTRON_43_COMPATIBILITY_2026-07-25.json"
ROLLBACK_ELECTRON = "35.7.5"
ROLLBACK_COMMIT = "2e11987ff0732d21df4a5da83d1ea557614991ac"
PROFILE_NAMES = ("code", "review", "render", "regenerate")
PASS_STATUSES = {"present_exact", "tool_available", "capability_pass"}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")


class RuntimeDoctorError(ValueError):
    """A deterministic doctor input or authority failure."""


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeDoctorError(f"JSON authority must be an object: {path.name}")
    return payload


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeDoctorError(f"{field} must be a non-empty relative path")
    normalized = value.replace("\\", "/")
    if re.match(r"^[A-Za-z]:", normalized) or normalized.startswith("/"):
        raise RuntimeDoctorError(f"{field} must not be absolute")
    parts = PurePosixPath(normalized).parts
    if any(part in {"", ".", ".."} for part in parts):
        raise RuntimeDoctorError(f"{field} contains an unsafe path segment")
    return PurePosixPath(*parts).as_posix()


def load_contract(repo_root: Path) -> dict[str, Any]:
    contract = _load_json(repo_root / CONTRACT_RELATIVE_PATH)
    validate_contract(contract)
    return contract


def validate_contract(contract: Mapping[str, Any]) -> None:
    if contract.get("schema") != CONTRACT_SCHEMA:
        raise RuntimeDoctorError("private-artifact contract schema is unsupported")
    if contract.get("default_action") != "validation_only":
        raise RuntimeDoctorError("private-artifact contract must default to validation_only")
    if contract.get("copy_authorized") is not False or contract.get("apply_authorized") is not False:
        raise RuntimeDoctorError("private-artifact contract must deny copy/apply")
    artifacts = contract.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise RuntimeDoctorError("private-artifact contract has no artifacts")
    seen_ids: set[str] = set()
    seen_sources: set[str] = set()
    seen_destinations: set[str] = set()
    for row in artifacts:
        if not isinstance(row, dict):
            raise RuntimeDoctorError("artifact contract row must be an object")
        artifact_id = row.get("artifact_id")
        if not isinstance(artifact_id, str) or not artifact_id or artifact_id in seen_ids:
            raise RuntimeDoctorError("artifact IDs must be non-empty and unique")
        seen_ids.add(artifact_id)
        source = _safe_relative(row.get("bundle_source_path"), field="bundle_source_path")
        destination = _safe_relative(
            row.get("repo_relative_destination"), field="repo_relative_destination"
        )
        source_key = source.casefold()
        destination_key = destination.casefold()
        if source_key in seen_sources:
            raise RuntimeDoctorError("duplicate bundle source collision")
        if destination_key in seen_destinations:
            raise RuntimeDoctorError("duplicate repo destination collision")
        seen_sources.add(source_key)
        seen_destinations.add(destination_key)
        expected = row.get("expected_sha256")
        if not isinstance(expected, str) or not HASH_RE.fullmatch(expected):
            raise RuntimeDoctorError(f"invalid expected SHA-256 for {artifact_id}")
        required_profiles = row.get("required_consumer_profiles")
        if not isinstance(required_profiles, list) or any(
            profile not in PROFILE_NAMES for profile in required_profiles
        ):
            raise RuntimeDoctorError(f"invalid consumer profile for {artifact_id}")
        for false_field in ("mutable", "overwrite", "production_allowed", "publication_allowed", "upload_allowed"):
            if row.get(false_field) is not False:
                raise RuntimeDoctorError(f"{artifact_id} must set {false_field}=false")


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def _artifact_status(
    *,
    candidate: Path,
    root: Path,
    expected_sha256: str,
) -> tuple[str, str | None, int | None, str | None]:
    try:
        resolved = candidate.resolve(strict=False)
    except OSError:
        return "missing_required", None, None, "path_resolution_failed"
    if not _inside(root, resolved):
        return "missing_required", None, None, "symlink_escape_rejected"
    if not candidate.is_file():
        return "receipt_only_no_live_file", None, None, None
    observed = _sha256(candidate)
    return (
        "present_exact" if observed == expected_sha256 else "present_hash_mismatch",
        observed,
        candidate.stat().st_size,
        None,
    )


def validate_artifacts(
    *,
    repo_root: Path,
    contract: Mapping[str, Any],
    artifact_root: Path | None,
) -> dict[str, Any]:
    validate_contract(contract)
    staging_mode = artifact_root is not None
    repo_root = repo_root.resolve(strict=False)
    source_root = (artifact_root if staging_mode else repo_root).resolve(strict=False)
    root_available = source_root.is_dir()
    observations: list[dict[str, Any]] = []
    ingest_ready = root_available
    for row in contract["artifacts"]:
        source_rel = (
            _safe_relative(row["bundle_source_path"], field="bundle_source_path")
            if staging_mode
            else _safe_relative(
                row["repo_relative_destination"], field="repo_relative_destination"
            )
        )
        destination_rel = _safe_relative(
            row["repo_relative_destination"], field="repo_relative_destination"
        )
        if root_available:
            status, observed, size, rejection = _artifact_status(
                candidate=source_root / Path(source_rel),
                root=source_root,
                expected_sha256=row["expected_sha256"],
            )
        else:
            status, observed, size, rejection = (
                "receipt_only_no_live_file",
                None,
                None,
                "artifact_root_unavailable",
            )
        destination_status, _, _, destination_rejection = _artifact_status(
            candidate=repo_root / Path(destination_rel),
            root=repo_root,
            expected_sha256=row["expected_sha256"],
        )
        if destination_status == "receipt_only_no_live_file":
            destination_status = "missing_optional"
        elif destination_rejection:
            destination_status = "unsafe_path_rejected"
        if status != "present_exact":
            ingest_ready = False
        if staging_mode and destination_status in {
            "present_hash_mismatch",
            "unsafe_path_rejected",
        }:
            ingest_ready = False
        observations.append(
            {
                "artifact_id": row["artifact_id"],
                "artifact_role": row["artifact_role"],
                "status": status,
                "evidence_valid": status == "present_exact",
                "expected_sha256": row["expected_sha256"],
                "observed_sha256": observed,
                "size_bytes": size,
                "bundle_source_path": row["bundle_source_path"],
                "proposed_repo_relative_destination": destination_rel,
                "existing_destination_status": destination_status,
                "existing_destination_rejection": destination_rejection,
                "required_consumer_profiles": list(row["required_consumer_profiles"]),
                "consumer_effect": (
                    "available to declared consumers"
                    if status == "present_exact"
                    else "declared consumers remain unavailable"
                ),
                "authority_source": CONTRACT_RELATIVE_PATH,
                "rejection": rejection,
            }
        )
    return {
        "mode": "staging_root" if staging_mode else "live_repo_locators",
        "artifact_root_supplied": staging_mode,
        "artifact_root_available": root_available,
        "validation_only": True,
        "copy_performed": False,
        "overwrite_performed": False,
        "delete_performed": False,
        "archive_extraction_performed": False,
        "ingest_ready": ingest_ready,
        "artifact_count": len(observations),
        "observations": observations,
    }


def _check(
    check_id: str,
    status: str,
    *,
    observed: object,
    effect: str,
    authority: str,
    required: bool = True,
) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": status,
        "evidence_valid": status in PASS_STATUSES,
        "observed": observed,
        "consumer_effect": effect,
        "authority_source": authority,
        "required": required,
    }


def _version_check(tool: str, arguments: Sequence[str]) -> dict[str, Any]:
    executable = shutil.which(tool)
    if not executable:
        return _check(
            f"{tool}_discovery",
            "tool_unavailable",
            observed={"tool": tool, "version": None},
            effect=f"{tool} dependent capability is unavailable",
            authority="live PATH discovery",
        )
    try:
        completed = subprocess.run(
            [executable, *arguments],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
        combined = (completed.stdout or completed.stderr).strip().splitlines()
        version = combined[0].strip() if combined else "version_unavailable"
        status = "tool_available" if completed.returncode == 0 else "capability_fail"
    except (OSError, subprocess.TimeoutExpired):
        version = "version_unavailable"
        status = "capability_fail"
    return _check(
        f"{tool}_discovery",
        status,
        observed={"tool": tool, "version": version},
        effect=f"{tool} is {'available' if status == 'tool_available' else 'unusable'}",
        authority="live PATH discovery",
    )


def _hash_check(
    check_id: str,
    path: Path,
    expected: str,
    *,
    authority: str,
    effect: str,
) -> dict[str, Any]:
    if not path.is_file():
        return _check(
            check_id,
            "missing_required",
            observed={"sha256": None},
            effect=effect,
            authority=authority,
        )
    observed = _sha256(path)
    return _check(
        check_id,
        "present_exact" if observed == expected else "present_hash_mismatch",
        observed={"sha256": observed},
        effect=effect,
        authority=authority,
    )


def _run_python_import_smoke(repo_root: Path) -> dict[str, Any]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        completed = subprocess.run(
            [sys.executable, "-c", "import src.cli.main"],
            cwd=repo_root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        status = "capability_pass" if completed.returncode == 0 else "capability_fail"
    except (OSError, subprocess.TimeoutExpired):
        status = "capability_fail"
    return _check(
        "python_cli_import",
        status,
        observed={"module": "src.cli.main", "exit_code": 0 if status == "capability_pass" else 1},
        effect="current Python can import the CLI" if status == "capability_pass" else "code profile blocked",
        authority="src/cli/main.py",
    )


def _git_safety(repo_root: Path) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            ["git", "status", "--porcelain=v1", "--untracked-files=no"],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        clean = completed.returncode == 0 and not completed.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        clean = False
    return _check(
        "git_tracked_worktree",
        "capability_pass" if clean else "capability_fail",
        observed={"tracked_clean": clean},
        effect="safe code-development baseline" if clean else "commit or resolve tracked changes first",
        authority="live Git tracked state",
    )


def _electron_check(repo_root: Path, authority: Mapping[str, Any]) -> dict[str, Any]:
    expected = str(authority["candidate"]["electron"])
    lock_path = repo_root / "gui/package-lock.json"
    runtime_package = repo_root / "gui/node_modules/electron/package.json"
    lock_version = None
    runtime_version = None
    try:
        lock_version = _load_json(lock_path)["packages"]["node_modules/electron"]["version"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError):
        pass
    if runtime_package.is_file():
        try:
            runtime_version = _load_json(runtime_package)["version"]
        except (KeyError, TypeError, json.JSONDecodeError):
            pass
    exact = lock_version == expected and runtime_version == expected
    status = "present_exact" if exact else (
        "tool_unavailable" if runtime_version is None else "present_hash_mismatch"
    )
    return _check(
        "electron_runtime",
        status,
        observed={
            "expected_version": expected,
            "lock_version": lock_version,
            "runtime_version": runtime_version,
        },
        effect="Electron GUI code can run" if exact else "restore GUI dependencies from tracked lock",
        authority=ELECTRON_AUTHORITY_PATH,
    )


def _hidden_electron_smoke(repo_root: Path) -> dict[str, Any]:
    npm = shutil.which("npm")
    electron_package = repo_root / "gui/node_modules/electron/package.json"
    if not npm or not electron_package.is_file():
        return _check(
            "electron_hidden_smoke",
            "tool_unavailable",
            observed={"executed": False, "cleanup_verified": True},
            effect="deep Electron capability unavailable",
            authority="gui/electron_compatibility_smoke.js",
        )
    smoke_root = repo_root / "_tmp/electron_compatibility_smoke"
    smoke_root_existed = smoke_root.is_dir()
    before = {item.name for item in smoke_root.iterdir()} if smoke_root.is_dir() else set()
    environment = dict(os.environ)
    environment["NLMYTGEN_AUDIO_POLICY"] = "silent"
    environment["NPM_CONFIG_UPDATE_NOTIFIER"] = "false"
    payload: dict[str, Any] | None = None
    status = "capability_fail"
    try:
        completed = subprocess.run(
            [npm, "--prefix", "gui", "run", "smoke:electron-compatibility"],
            cwd=repo_root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        marker = "ELECTRON_COMPATIBILITY_RECEIPT="
        receipt = None
        for line in (completed.stdout or "").splitlines():
            if line.startswith(marker):
                receipt = Path(line.removeprefix(marker).strip())
                break
        if receipt and receipt.is_file():
            payload = _load_json(receipt)
        status = (
            "capability_pass"
            if completed.returncode == 0 and payload and payload.get("status") == "passed"
            else "capability_fail"
        )
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        status = "capability_fail"
    finally:
        after = {item.name for item in smoke_root.iterdir()} if smoke_root.is_dir() else set()
        for name in sorted(after - before):
            owned = smoke_root / name
            if owned.is_dir():
                shutil.rmtree(owned)
            elif owned.exists():
                owned.unlink()
        if not smoke_root_existed and smoke_root.is_dir() and not any(smoke_root.iterdir()):
            smoke_root.rmdir()
    cleanup_verified = (
        {item.name for item in smoke_root.iterdir()} if smoke_root.is_dir() else set()
    ) == before
    checks = payload.get("checks", {}) if isinstance(payload, dict) else {}
    return _check(
        "electron_hidden_smoke",
        status if cleanup_verified else "capability_fail",
        observed={
            "executed": True,
            "electron": payload.get("runtime", {}).get("electron") if payload else None,
            "window_hidden": True,
            "audio_policy_silent": checks.get("audio_policy_silent") is True,
            "mute_audio": checks.get("mute_audio_switch_enabled") is True,
            "no_console_errors": checks.get("no_console_errors") is True,
            "cleanup_verified": cleanup_verified,
        },
        effect="actual hidden Electron path passed" if status == "capability_pass" else "deep GUI capability blocked",
        authority="gui/electron_compatibility_smoke.js",
    )


def _artifact_map(artifact_plan: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        row["artifact_id"]: row
        for row in artifact_plan["observations"]
        if isinstance(row, dict) and isinstance(row.get("artifact_id"), str)
    }


def _artifact_check(
    artifact_id: str,
    artifacts: Mapping[str, Mapping[str, Any]],
    *,
    profile: str,
    required: bool = True,
) -> dict[str, Any]:
    row = artifacts[artifact_id]
    status = str(row["status"])
    if status == "receipt_only_no_live_file":
        status = "missing_required" if required else "missing_optional"
    return _check(
        f"{profile}:{artifact_id}",
        status,
        observed={
            "artifact_id": artifact_id,
            "sha256": row.get("observed_sha256"),
            "size_bytes": row.get("size_bytes"),
        },
        effect=(
            f"{profile} artifact is exact"
            if status == "present_exact"
            else f"{profile} remains unavailable"
        ),
        authority=CONTRACT_RELATIVE_PATH,
        required=required,
    )


def _profile(name: str, checks: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    materialized = [dict(check) for check in checks]
    ready = all(
        check["status"] in PASS_STATUSES
        for check in materialized
        if check.get("required", True)
    )
    return {
        "profile": name,
        "ready": ready,
        "status": "capability_pass" if ready else "capability_fail",
        "checks": materialized,
        "blocking_checks": [
            check["check_id"]
            for check in materialized
            if check.get("required", True) and check["status"] not in PASS_STATUSES
        ],
    }


def _authority_agreement(repo_root: Path, contract: Mapping[str, Any]) -> dict[str, Any]:
    authority = contract["authority"]
    manifest = _load_json(repo_root / authority["episode_manifest"])
    provenance = _load_json(repo_root / authority["provenance"])
    receipt = _load_json(repo_root / authority["media_receipt"])
    acceptance = _load_json(repo_root / authority["human_acceptance"])
    mp4 = next(row for row in contract["artifacts"] if row["artifact_role"] == "accepted_review_media")
    generated = next(row for row in contract["artifacts"] if row["artifact_role"] == "generated_project")
    agrees = (
        receipt.get("run", {}).get("run_id") == contract.get("accepted_run_id")
        and acceptance.get("reviewed_artifact", {}).get("run_id") == contract.get("accepted_run_id")
        and receipt.get("media", {}).get("sha256") == mp4["expected_sha256"]
        and acceptance.get("reviewed_artifact", {}).get("sha256") == mp4["expected_sha256"]
        and receipt.get("generated_project", {}).get("sha256") == generated["expected_sha256"]
        and acceptance.get("reviewed_artifact", {}).get("generated_project_sha256")
        == generated["expected_sha256"]
        and receipt.get("run", {}).get("manifest_sha256")
        == _sha256(repo_root / authority["episode_manifest"])
        and receipt.get("run", {}).get("provenance_sha256")
        == _sha256(repo_root / authority["provenance"])
        and len(provenance.get("assets", [])) == 9
        and len(manifest.get("cue_mapping", [])) == 9
    )
    return _check(
        "accepted_authority_agreement",
        "capability_pass" if agrees else "capability_fail",
        observed={
            "accepted_run_id": contract.get("accepted_run_id"),
            "media_receipt_agrees": agrees,
            "asset_count": len(provenance.get("assets", [])),
        },
        effect="accepted identity is coherent" if agrees else "review/regeneration identity conflict",
        authority="contract authority receipts",
    )


def _probe_review_media(
    artifact: Mapping[str, Any],
    artifacts: Mapping[str, Mapping[str, Any]],
    source_root: Path,
    *,
    staged: bool,
) -> dict[str, Any]:
    row = artifacts[artifact["artifact_id"]]
    if row["status"] != "present_exact":
        return _check(
            "review_media_ffprobe",
            "missing_required",
            observed={"probed": False},
            effect="review profile unavailable",
            authority="validated_real_media_run_receipt.json",
        )
    path_rel = (
        artifact["bundle_source_path"] if staged else artifact["repo_relative_destination"]
    )
    media_path = source_root / Path(path_rel)
    result = probe_with_ffprobe(media_path)
    streams = result.get("streams") or []
    codec_types = {stream.get("codec_type") for stream in streams}
    passed = result.get("status") == "passed" and {"video", "audio"} <= codec_types
    return _check(
        "review_media_ffprobe",
        "capability_pass" if passed else "capability_fail",
        observed={
            "probed": True,
            "tool": result.get("tool"),
            "format": result.get("format"),
            "streams": streams,
        },
        effect="review media metadata is readable" if passed else "review media metadata invalid",
        authority="validated_real_media_run_receipt.json",
    )


def _resolve_yymm4() -> tuple[Path | None, str | None]:
    try:
        from src.pipeline.episode_video import EpisodeVideoError, resolve_yymm4_executable

        return resolve_yymm4_executable(), None
    except (OSError, EpisodeVideoError) as exc:
        return None, getattr(exc, "code", "yymm4_executable_missing")


def _file_product_version(path: Path) -> str | None:
    if os.name != "nt":
        return None
    powershell = shutil.which("pwsh") or shutil.which("powershell")
    if not powershell:
        return None
    script = (
        "& { param([string]$TargetPath) "
        "(Get-Item -LiteralPath $TargetPath).VersionInfo.ProductVersion }"
    )
    try:
        completed = subprocess.run(
            [powershell, "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", script, str(path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    value = completed.stdout.strip().splitlines()
    return value[0].strip() if completed.returncode == 0 and value else None


def _version_tuple(value: str | None) -> tuple[int, ...]:
    if not value:
        return ()
    return tuple(int(part) for part in re.findall(r"\d+", value)[:4])


def _yymm4_checks(repo_root: Path) -> list[dict[str, Any]]:
    manifest_path = (
        repo_root
        / "production_pilots/yukkuri_newsroom_content_spine_002/"
        "external_editorial_input/new_banknote_security_notebooklm_001/"
        "auto_video_pipeline/new_banknote_real_media_episode_manifest.json"
    )
    manifest = _load_json(manifest_path)
    expected = manifest["yymm4"]["profile_version_expected"]
    executable, error = _resolve_yymm4()
    if executable is None:
        return [
            _check(
                "yymm4_discovery",
                "tool_unavailable",
                observed={"tool": "YukkuriMovieMaker.exe", "version": None, "error_code": error},
                effect="render profile unavailable",
                authority="episode manifest YMM4 contract",
            )
        ]
    version = _file_product_version(executable)
    compatible = bool(_version_tuple(version)) and _version_tuple(version) >= _version_tuple(expected)
    return [
        _check(
            "yymm4_discovery",
            "tool_available",
            observed={"tool": executable.name, "version": version},
            effect="YMM4 executable discovered without launch",
            authority="live executable discovery",
        ),
        _check(
            "yymm4_version",
            "capability_pass" if compatible else "capability_fail",
            observed={"version": version, "minimum_profile_version": expected},
            effect="YMM4 version compatible" if compatible else "YMM4 version decision required",
            authority="new_banknote_real_media_episode_manifest.json",
        ),
    ]


def _protected_input_agreement(repo_root: Path, contract: Mapping[str, Any]) -> dict[str, Any]:
    manifest_path = repo_root / contract["authority"]["episode_manifest"]
    manifest = _load_json(manifest_path)
    mismatches: list[str] = []
    for lock in manifest.get("content_locks", []):
        relative = _safe_relative(lock.get("path"), field="content_lock.path")
        path = repo_root / relative
        if not path.is_file() or _sha256(path) != lock.get("sha256"):
            mismatches.append(relative)
    source = next(row for row in contract["artifacts"] if row["artifact_role"] == "source_project")
    manifest_source_agrees = (
        manifest.get("yymm4", {}).get("source_project_sha256") == source["expected_sha256"]
    )
    passed = not mismatches and manifest_source_agrees
    return _check(
        "protected_input_agreement",
        "capability_pass" if passed else "capability_fail",
        observed={
            "content_lock_count": len(manifest.get("content_locks", [])),
            "mismatch_count": len(mismatches),
            "source_project_identity_agrees": manifest_source_agrees,
        },
        effect="regeneration inputs agree" if passed else "regeneration identity blocked",
        authority="new_banknote_real_media_episode_manifest.json",
    )


def _pipeline_capability(repo_root: Path) -> dict[str, Any]:
    cli_text = (repo_root / "src/cli/main.py").read_text(encoding="utf-8")
    module = repo_root / "src/pipeline/episode_video.py"
    available = module.is_file() and '"build-episode-video"' in cli_text
    return _check(
        "episode_pipeline_capability",
        "capability_pass" if available else "capability_fail",
        observed={"command": "build-episode-video", "available": available, "executed": False},
        effect="existing one-command regeneration path is present" if available else "regeneration unavailable",
        authority="src/cli/main.py and src/pipeline/episode_video.py",
    )


def _silent_policy_check(environment: Mapping[str, str]) -> dict[str, Any]:
    try:
        policy = resolve_audio_policy(environment)
        passed = policy == "silent"
    except SilentPolicyError:
        policy = "rejected"
        passed = False
    return _check(
        "silent_runtime_policy",
        "capability_pass" if passed else "not_authorized",
        observed={"policy": policy, "playback_performed": False, "system_volume_changed": False},
        effect="silent runtime available" if passed else "render/regenerate blocked",
        authority="src/pipeline/silent_media_runtime.py",
    )


def build_profiles(
    *,
    repo_root: Path,
    contract: Mapping[str, Any],
    artifact_plan: Mapping[str, Any],
    artifact_source_root: Path,
    staged_artifacts: bool,
    deep: bool,
    environment: Mapping[str, str],
) -> dict[str, dict[str, Any]]:
    electron_authority = _load_json(repo_root / ELECTRON_AUTHORITY_PATH)
    code_checks = [
        _check(
            "python_runtime",
            "tool_available" if sys.version_info >= (3, 11) else "tool_unavailable",
            observed={"tool": "python", "version": ".".join(map(str, sys.version_info[:3]))},
            effect="supported Python available",
            authority="pyproject.toml",
        ),
        _version_check("uv", ("--version",)),
        _hash_check(
            "python_lock_identity",
            repo_root / "uv.lock",
            electron_authority["candidate"]["uv_lock_sha256"],
            authority=ELECTRON_AUTHORITY_PATH,
            effect="tracked Python lock is exact",
        ),
        _run_python_import_smoke(repo_root),
        _version_check("node", ("--version",)),
        _version_check("npm", ("--version",)),
        _hash_check(
            "npm_lock_identity",
            repo_root / "gui/package-lock.json",
            electron_authority["candidate"]["package_lock_sha256"],
            authority=ELECTRON_AUTHORITY_PATH,
            effect="tracked npm lock is exact",
        ),
        _electron_check(repo_root, electron_authority),
        _git_safety(repo_root),
    ]
    code_checks.append(
        _hidden_electron_smoke(repo_root)
        if deep
        else _check(
            "electron_hidden_smoke",
            "not_evaluated",
            observed={"executed": False, "reason": "--deep not supplied"},
            effect="deep GUI capability not requested",
            authority="gui/electron_compatibility_smoke.js",
            required=False,
        )
    )
    code = _profile("code", code_checks)

    artifacts = _artifact_map(artifact_plan)
    accepted_media = next(
        row for row in contract["artifacts"] if row["artifact_role"] == "accepted_review_media"
    )
    review = _profile(
        "review",
        [
            _authority_agreement(repo_root, contract),
            _artifact_check(accepted_media["artifact_id"], artifacts, profile="review"),
            _probe_review_media(
                accepted_media,
                artifacts,
                artifact_source_root,
                staged=staged_artifacts,
            ),
            _artifact_check(
                "generated_yymm4_project",
                artifacts,
                profile="review",
                required=False,
            ),
        ],
    )

    render_checks: list[dict[str, Any]] = [
        _check(
            "code_profile_dependency",
            "capability_pass" if code["ready"] else "capability_fail",
            observed={"code_ready": code["ready"]},
            effect="render runtime foundation available" if code["ready"] else "render blocked by code profile",
            authority="doctor code profile",
        ),
        *_yymm4_checks(repo_root),
        _version_check("ffmpeg", ("-version",)),
        _version_check("ffprobe", ("-version",)),
        _version_check("dotnet", ("--version",)),
        _check(
            "render_driver_project",
            "present_exact"
            if (repo_root / "tools/Ymm4RenderAutomation/Ymm4RenderAutomation.csproj").is_file()
            else "missing_required",
            observed={"repo_relative_path": "tools/Ymm4RenderAutomation/Ymm4RenderAutomation.csproj"},
            effect="bounded render driver is available",
            authority="tracked repository",
        ),
        _silent_policy_check(environment),
        _artifact_check("source_yymm4_project", artifacts, profile="render"),
    ]
    for artifact in contract["artifacts"]:
        if artifact["artifact_role"] == "real_media_source":
            render_checks.append(_artifact_check(artifact["artifact_id"], artifacts, profile="render"))
    render = _profile("render", render_checks)

    regenerate = _profile(
        "regenerate",
        [
            _check(
                "render_profile_dependency",
                "capability_pass" if render["ready"] else "capability_fail",
                observed={"render_ready": render["ready"]},
                effect="regeneration runtime available" if render["ready"] else "regeneration blocked by render profile",
                authority="doctor render profile",
            ),
            _authority_agreement(repo_root, contract),
            _protected_input_agreement(repo_root, contract),
            _pipeline_capability(repo_root),
        ],
    )
    return {"code": code, "review": review, "render": render, "regenerate": regenerate}


def run_doctor(
    *,
    repo_root: Path,
    profile: str = "all",
    require_profile: str | None = None,
    artifact_root: Path | None = None,
    deep: bool = False,
    environment: Mapping[str, str] | None = None,
) -> tuple[dict[str, Any], int]:
    repo_root = repo_root.resolve()
    if profile not in (*PROFILE_NAMES, "all"):
        raise RuntimeDoctorError("unknown readiness profile")
    if require_profile is not None and require_profile not in PROFILE_NAMES:
        raise RuntimeDoctorError("unknown required profile")
    contract = load_contract(repo_root)
    artifact_plan = validate_artifacts(
        repo_root=repo_root,
        contract=contract,
        artifact_root=artifact_root,
    )
    artifact_source_root = (
        artifact_root if artifact_root is not None else repo_root
    ).resolve(strict=False)
    profiles = build_profiles(
        repo_root=repo_root,
        contract=contract,
        artifact_plan=artifact_plan,
        artifact_source_root=artifact_source_root,
        staged_artifacts=artifact_root is not None,
        deep=deep,
        environment=dict(os.environ if environment is None else environment),
    )
    selected_names = list(PROFILE_NAMES) if profile == "all" else [profile]
    if require_profile and require_profile not in selected_names:
        selected_names.append(require_profile)
    selected = {name: profiles[name] for name in selected_names}
    required_ready = require_profile is None or profiles[require_profile]["ready"]
    exit_code = 0 if required_ready else 1
    result = {
        "schema": SCHEMA,
        "schema_version": "1.0",
        "command": "doctor-runtime",
        "request": {
            "profile": profile,
            "require_profile": require_profile,
            "deep": deep,
            "artifact_root_supplied": artifact_root is not None,
        },
        "artifact_contract": {
            "path": CONTRACT_RELATIVE_PATH,
            "schema": contract["schema"],
            "artifact_set_id": contract["artifact_set_id"],
            "accepted_run_id": contract["accepted_run_id"],
            "artifact_count": len(contract["artifacts"]),
            "validation_only": contract["default_action"] == "validation_only",
            "copy_authorized": contract["copy_authorized"],
            "apply_authorized": contract["apply_authorized"],
        },
        "profiles": selected,
        "ingest_plan": artifact_plan,
        "boundaries": {
            "private_bytes_copied": False,
            "private_artifacts_mutated": False,
            "yymm4_launched": False,
            "render_performed": False,
            "media_playback": False,
            "system_volume_changed": False,
            "network_required": False,
            "rights_clearance": False,
            "production": False,
            "publication": False,
            "upload": False,
            "release": False,
            "pull_request": False,
            "master_merge": False,
            "electron_rollback": {
                "version": ROLLBACK_ELECTRON,
                "source_commit": ROLLBACK_COMMIT,
            },
        },
        "exit_code": exit_code,
    }
    return result, exit_code


def render_text(result: Mapping[str, Any]) -> str:
    lines = [
        "NLMYTGen runtime doctor",
        f"artifact set: {result['artifact_contract']['artifact_set_id']}",
    ]
    for name, profile in result["profiles"].items():
        lines.append(f"{name}: {'ready' if profile['ready'] else 'unavailable'}")
        for check_id in profile["blocking_checks"]:
            lines.append(f"  blocked: {check_id}")
    plan = result["ingest_plan"]
    lines.extend(
        [
            f"artifact validation: {'ready' if plan['ingest_ready'] else 'not ready'}",
            "validation only: no copy, overwrite, delete, render, playback, or publication",
        ]
    )
    return "\n".join(lines)
