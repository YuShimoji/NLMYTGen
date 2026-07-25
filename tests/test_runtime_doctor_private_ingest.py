from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from src.pipeline import runtime_doctor


REPO_ROOT = Path(__file__).resolve().parents[1]


def _hash(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _artifact(
    *,
    artifact_id: str = "fixture_artifact",
    source: str = "bundle/fixture.bin",
    destination: str = "private/fixture.bin",
    expected: str | None = None,
    required_profiles: list[str] | None = None,
) -> dict[str, object]:
    return {
        "artifact_id": artifact_id,
        "artifact_role": "fixture",
        "expected_sha256": expected or _hash(b"exact"),
        "bundle_source_path": source,
        "repo_relative_destination": destination,
        "required_consumer_profiles": required_profiles or ["review"],
        "sensitivity": "private_fixture",
        "mutable": False,
        "overwrite": False,
        "rights_classification": "test_only",
        "production_allowed": False,
        "publication_allowed": False,
        "upload_allowed": False,
    }


def _contract(*artifacts: dict[str, object]) -> dict[str, object]:
    return {
        "schema": runtime_doctor.CONTRACT_SCHEMA,
        "schema_version": "1.0",
        "artifact_set_id": "fixture-set",
        "accepted_run_id": "fixture-run",
        "authority": {},
        "default_action": "validation_only",
        "copy_authorized": False,
        "apply_authorized": False,
        "artifacts": list(artifacts or (_artifact(),)),
    }


def _pass(check_id: str) -> dict[str, object]:
    return runtime_doctor._check(
        check_id,
        "capability_pass",
        observed={},
        effect="fixture passed",
        authority="test fixture",
    )


def test_tracked_contract_is_validation_only_and_contains_exact_private_set() -> None:
    contract = runtime_doctor.load_contract(REPO_ROOT)
    raw = json.dumps(contract, sort_keys=True)

    assert contract["artifact_set_id"] == "new-banknote-real-media-stable-internal-cut-v1"
    assert len(contract["artifacts"]) == 12
    assert {row["artifact_role"] for row in contract["artifacts"]} == {
        "source_project",
        "generated_project",
        "accepted_review_media",
        "real_media_source",
    }
    assert contract["default_action"] == "validation_only"
    assert contract["copy_authorized"] is False
    assert contract["apply_authorized"] is False
    assert "C:\\Users\\" not in raw
    assert "C:/Users/" not in raw


def test_tracked_verification_surfaces_contain_no_private_absolute_path() -> None:
    paths = (
        REPO_ROOT
        / "docs/verification/RUNTIME_DOCTOR_PRIVATE_INGEST_2026-07-25.json",
        REPO_ROOT
        / "docs/verification/RUNTIME_DOCTOR_PRIVATE_INGEST_2026-07-25.md",
    )

    for path in paths:
        raw = path.read_text(encoding="utf-8")
        assert "C:\\Users\\" not in raw
        assert "C:/Users/" not in raw
        assert "@gmail" not in raw
        assert "_authToken" not in raw


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("bundle_source_path", "../escape.bin"),
        ("bundle_source_path", "C:/private/escape.bin"),
        ("repo_relative_destination", "/private/escape.bin"),
        ("repo_relative_destination", "..\\escape.bin"),
    ],
)
def test_contract_rejects_traversal_and_absolute_paths(field: str, value: str) -> None:
    row = _artifact()
    row[field] = value

    with pytest.raises(runtime_doctor.RuntimeDoctorError):
        runtime_doctor.validate_contract(_contract(row))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_id", "fixture_artifact"),
        ("bundle_source_path", "bundle/fixture.bin"),
        ("bundle_source_path", "BUNDLE/FIXTURE.BIN"),
        ("repo_relative_destination", "private/fixture.bin"),
        ("repo_relative_destination", "PRIVATE/FIXTURE.BIN"),
    ],
)
def test_contract_rejects_duplicate_id_and_path_collisions(field: str, value: str) -> None:
    second = _artifact(
        artifact_id="other",
        source="bundle/other.bin",
        destination="private/other.bin",
    )
    second[field] = value

    with pytest.raises(runtime_doctor.RuntimeDoctorError):
        runtime_doctor.validate_contract(_contract(_artifact(), second))


def test_empty_artifact_root_is_receipt_only_and_performs_no_ingest(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    staged = tmp_path / "staged"
    repo.mkdir()
    staged.mkdir()
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))

    result = runtime_doctor.validate_artifacts(
        repo_root=repo,
        contract=_contract(),
        artifact_root=staged,
    )

    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    assert result["ingest_ready"] is False
    assert result["observations"][0]["status"] == "receipt_only_no_live_file"
    assert result["copy_performed"] is False
    assert result["overwrite_performed"] is False
    assert result["delete_performed"] is False
    assert before == after


def test_staged_artifact_reports_exact_then_hash_mismatch_without_copy(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    staged = tmp_path / "staged"
    source = staged / "bundle/fixture.bin"
    repo.mkdir()
    source.parent.mkdir(parents=True)
    source.write_bytes(b"exact")
    contract = _contract()

    exact = runtime_doctor.validate_artifacts(
        repo_root=repo,
        contract=contract,
        artifact_root=staged,
    )
    source.write_bytes(b"mismatch")
    mismatch = runtime_doctor.validate_artifacts(
        repo_root=repo,
        contract=contract,
        artifact_root=staged,
    )

    assert exact["observations"][0]["status"] == "present_exact"
    assert exact["ingest_ready"] is True
    assert mismatch["observations"][0]["status"] == "present_hash_mismatch"
    assert mismatch["ingest_ready"] is False
    assert not (repo / "private/fixture.bin").exists()


def test_resolved_path_escape_is_rejected_before_hashing(tmp_path: Path) -> None:
    staged = tmp_path / "staged"
    outside = tmp_path / "outside.bin"
    staged.mkdir()
    outside.write_bytes(b"exact")

    status, observed, size, rejection = runtime_doctor._artifact_status(
        candidate=outside,
        root=staged,
        expected_sha256=_hash(b"exact"),
    )

    assert status == "missing_required"
    assert observed is None
    assert size is None
    assert rejection == "symlink_escape_rejected"


def test_required_and_optional_receipt_only_states_are_distinct() -> None:
    artifacts = {
        "fixture_artifact": {
            "artifact_id": "fixture_artifact",
            "status": "receipt_only_no_live_file",
            "observed_sha256": None,
            "size_bytes": None,
        }
    }

    required = runtime_doctor._artifact_check(
        "fixture_artifact", artifacts, profile="review"
    )
    optional = runtime_doctor._artifact_check(
        "fixture_artifact", artifacts, profile="review", required=False
    )

    assert required["status"] == "missing_required"
    assert required["evidence_valid"] is False
    assert optional["status"] == "missing_optional"
    assert optional["required"] is False


def test_profile_composition_keeps_review_independent_from_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = runtime_doctor.load_contract(REPO_ROOT)
    observations = [
        {
            "artifact_id": row["artifact_id"],
            "status": "present_exact",
            "observed_sha256": row["expected_sha256"],
            "size_bytes": 1,
        }
        for row in contract["artifacts"]
    ]
    artifact_plan = {"observations": observations}
    monkeypatch.setattr(
        runtime_doctor,
        "_run_python_import_smoke",
        lambda _root: _pass("python_cli_import"),
    )
    monkeypatch.setattr(
        runtime_doctor,
        "_hash_check",
        lambda *args, **kwargs: _pass(str(args[0])),
    )
    monkeypatch.setattr(
        runtime_doctor,
        "_version_check",
        lambda tool, _args: _pass(f"{tool}_discovery"),
    )
    monkeypatch.setattr(
        runtime_doctor, "_electron_check", lambda *_args: _pass("electron_runtime")
    )
    monkeypatch.setattr(
        runtime_doctor, "_git_safety", lambda _root: runtime_doctor._check(
            "git_tracked_worktree",
            "capability_fail",
            observed={"tracked_clean": False},
            effect="fixture blocked",
            authority="test fixture",
        )
    )
    monkeypatch.setattr(
        runtime_doctor,
        "_authority_agreement",
        lambda *_args: _pass("accepted_authority_agreement"),
    )
    monkeypatch.setattr(
        runtime_doctor,
        "_probe_review_media",
        lambda *_args, **_kwargs: _pass("review_media_ffprobe"),
    )
    monkeypatch.setattr(
        runtime_doctor, "_yymm4_checks", lambda _root: [_pass("yymm4_discovery")]
    )
    monkeypatch.setattr(
        runtime_doctor,
        "_silent_policy_check",
        lambda _environment: _pass("silent_runtime_policy"),
    )
    monkeypatch.setattr(
        runtime_doctor,
        "_protected_input_agreement",
        lambda *_args: _pass("protected_input_agreement"),
    )
    monkeypatch.setattr(
        runtime_doctor,
        "_pipeline_capability",
        lambda _root: _pass("episode_pipeline_capability"),
    )

    profiles = runtime_doctor.build_profiles(
        repo_root=REPO_ROOT,
        contract=contract,
        artifact_plan=artifact_plan,
        artifact_source_root=REPO_ROOT,
        staged_artifacts=False,
        deep=False,
        environment={"NLMYTGEN_AUDIO_POLICY": "silent"},
    )

    assert profiles["code"]["ready"] is False
    assert profiles["review"]["ready"] is True
    assert profiles["render"]["ready"] is False
    assert profiles["regenerate"]["ready"] is False


def test_doctor_result_is_deterministic_and_preserves_closed_boundaries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixed_plan = {
        "mode": "staging_root",
        "artifact_root_supplied": True,
        "artifact_root_available": True,
        "validation_only": True,
        "copy_performed": False,
        "overwrite_performed": False,
        "delete_performed": False,
        "archive_extraction_performed": False,
        "ingest_ready": False,
        "artifact_count": 0,
        "observations": [],
    }
    fixed_profile = runtime_doctor._profile("code", [_pass("fixed")])
    monkeypatch.setattr(
        runtime_doctor, "validate_artifacts", lambda **_kwargs: dict(fixed_plan)
    )
    monkeypatch.setattr(
        runtime_doctor,
        "build_profiles",
        lambda **_kwargs: {
            name: {**fixed_profile, "profile": name}
            for name in runtime_doctor.PROFILE_NAMES
        },
    )

    first, first_exit = runtime_doctor.run_doctor(
        repo_root=REPO_ROOT,
        profile="all",
        require_profile="code",
        artifact_root=REPO_ROOT / "_tmp/nonexistent-fixture",
        deep=True,
        environment={},
    )
    second, second_exit = runtime_doctor.run_doctor(
        repo_root=REPO_ROOT,
        profile="all",
        require_profile="code",
        artifact_root=REPO_ROOT / "_tmp/nonexistent-fixture",
        deep=True,
        environment={},
    )

    assert first_exit == second_exit == 0
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    assert all(
        first["boundaries"][key] is False
        for key in (
            "private_bytes_copied",
            "private_artifacts_mutated",
            "yymm4_launched",
            "render_performed",
            "media_playback",
            "system_volume_changed",
            "network_required",
            "rights_clearance",
            "production",
            "publication",
            "upload",
            "release",
            "pull_request",
            "master_merge",
        )
    )
    assert first["boundaries"]["electron_rollback"] == {
        "version": "35.7.5",
        "source_commit": "2e11987ff0732d21df4a5da83d1ea557614991ac",
    }
