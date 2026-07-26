from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from src.pipeline import factory_render_promotion as render
from src.pipeline.factory_queue import evaluate_factory_queue


ROOT = Path(__file__).resolve().parents[1]
QUEUE = render.PREDECESSOR_QUEUE


def _evaluation() -> dict:
    return evaluate_factory_queue(
        repo_root=ROOT,
        queue_path=QUEUE,
        check_live=True,
    )


def _request(evaluation: dict, **overrides):
    arguments = {
        "evaluation": evaluation,
        "queue_path": QUEUE,
        "package_id": render.PACKAGE_ID,
        "to_lifecycle": render.TARGET_LIFECYCLE,
        "authority_id": render.AUTHORITY_ID,
        "render_authority_id": None,
    }
    arguments.update(overrides)
    return render._validate_request(**arguments)


def _assert_code(expected: str, callback) -> None:
    with pytest.raises(render.FactoryRenderPromotionError) as caught:
        callback()
    assert caught.value.code == expected


def test_plan_only_public_command_is_side_effect_free():
    protected = [
        ROOT / render.SOURCE_PROJECT,
        ROOT / render.PREDECESSOR_DESCRIPTOR,
        ROOT / render.PREDECESSOR_QUEUE,
    ]
    before = [
        (render.sha256_file(path), path.stat().st_size, path.stat().st_mtime_ns)
        for path in protected
    ]
    result = render.advance_factory_render(
        repo_root=ROOT,
        queue_path=QUEUE,
        package_id=render.PACKAGE_ID,
        to_lifecycle=render.TARGET_LIFECYCLE,
        authority_id=render.AUTHORITY_ID,
        execute=False,
        persist_failure=False,
    )
    assert result["status"] == "planned"
    assert result["boundaries"]["yymm4_launch_count"] == 0
    assert result["boundaries"]["ffmpeg_encode_count"] == 0
    after = [
        (render.sha256_file(path), path.stat().st_size, path.stat().st_mtime_ns)
        for path in protected
    ]
    assert after == before


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [
        (
            lambda evaluation, request: request.update(
                authority_id="wrong-render-authority"
            ),
            "authority_id_mismatch",
        ),
        (
            lambda evaluation, request: request.update(authority_id=None),
            "authority_id_missing",
        ),
        (
            lambda evaluation, request: request.update(
                package_id="ai_monitoring_labor_001"
            ),
            "package_not_selected",
        ),
        (
            lambda evaluation, request: request.update(
                to_lifecycle="human_accepted"
            ),
            "unsupported_lifecycle_jump",
        ),
        (
            lambda evaluation, request: request.update(
                render_authority_id=render.AUTHORITY_ID
            ),
            "duplicate_render_authority_forbidden",
        ),
        (
            lambda evaluation, request: evaluation["packages"][-1].update(
                content_identity_sha256="0" * 64
            ),
            "predecessor_identity_drift",
        ),
        (
            lambda evaluation, request: evaluation["packages"][-1].update(
                render_settings_identity_sha256="0" * 64
            ),
            "predecessor_identity_drift",
        ),
        (
            lambda evaluation, request: evaluation["counts"].update(
                render_candidates=2
            ),
            "queue_candidate_baseline_drift",
        ),
    ],
)
def test_request_authority_and_semantic_drift_fail_closed(mutate, expected):
    evaluation = copy.deepcopy(_evaluation())
    request: dict = {}
    mutate(evaluation, request)
    _assert_code(expected, lambda: _request(evaluation, **request))


def test_source_project_hash_mismatch_fails_before_render(monkeypatch):
    actual = render.sha256_file

    def drift(path: Path) -> str:
        if path.resolve() == (ROOT / render.SOURCE_PROJECT).resolve():
            return "0" * 64
        return actual(path)

    monkeypatch.setattr(render, "sha256_file", drift)
    _assert_code(
        "protected_predecessor_drift",
        lambda: render._validate_predecessor(ROOT),
    )


def test_source_project_structural_mismatch_fails_before_render(monkeypatch):
    actual = render._load_json

    def drift(path: Path):
        payload = actual(path)
        if path.resolve() == (ROOT / render.SOURCE_PROJECT_READBACK).resolve():
            payload["source_project"]["structural_identity_sha256"] = "0" * 64
        return payload

    monkeypatch.setattr(render, "_load_json", drift)
    _assert_code(
        "source_project_identity_drift",
        lambda: render._validate_predecessor(ROOT),
    )


def test_raster_asset_hash_mismatch_fails_before_render(monkeypatch):
    actual = render.sha256_file
    raster = (
        ROOT
        / render.PACKAGE_ROOT
        / "local_media"
        / "caa_expiration_date_page1.png"
    ).resolve()

    def drift(path: Path) -> str:
        if path.resolve() == raster:
            return "0" * 64
        return actual(path)

    monkeypatch.setattr(render, "sha256_file", drift)
    _assert_code(
        "raster_asset_hash_mismatch",
        lambda: render._validate_predecessor(ROOT),
    )


@pytest.mark.parametrize(
    "protected_path",
    [
        render.PREDECESSOR_DESCRIPTOR,
        render.PRE_RENDER_MANIFEST,
    ],
)
def test_crop_subtitle_or_render_manifest_change_fails_closed(
    monkeypatch, protected_path
):
    actual = render.sha256_file
    target = (ROOT / protected_path).resolve()

    def drift(path: Path) -> str:
        if path.resolve() == target:
            return "0" * 64
        return actual(path)

    monkeypatch.setattr(render, "sha256_file", drift)
    _assert_code(
        "protected_predecessor_drift",
        lambda: render._validate_predecessor(ROOT),
    )


def test_rights_or_public_authority_smuggling_fails_closed(monkeypatch):
    actual = render._load_json

    def drift(path: Path):
        payload = actual(path)
        if path.resolve() == (ROOT / render.PREDECESSOR_DESCRIPTOR).resolve():
            payload["authority"]["publication"] = {
                "approved": True,
                "record": {"path": "receipt.json", "sha256": "0" * 64},
            }
        return payload

    monkeypatch.setattr(render, "_load_json", drift)
    _assert_code(
        "authority_or_identity_smuggling",
        lambda: render._validate_predecessor(ROOT),
    )


def test_private_absolute_path_in_tracked_receipt_is_rejected():
    _assert_code(
        "tracked_private_path_forbidden",
        lambda: render._assert_sanitized(
            {
                "schema": render.RENDER_READBACK_SCHEMA,
                "path": "C:\\Users\\operator\\private.mp4",
            }
        ),
    )


def test_runtime_manifest_consumes_one_shot_authority_without_mutating_predecessor():
    predecessor = json.loads((ROOT / render.PRE_RENDER_MANIFEST).read_text("utf-8"))
    source_readback = json.loads(
        (ROOT / render.SOURCE_PROJECT_READBACK).read_text("utf-8")
    )
    before = copy.deepcopy(predecessor)
    runtime = render._runtime_manifest(
        predecessor_manifest=predecessor,
        source_readback=source_readback,
        run_id=render.PRIMARY_RUN_ID,
    )
    assert predecessor == before
    assert runtime["schema"] == "nlmytgen.episode_manifest.v1"
    assert runtime["yymm4"]["source_project_sha256"] == render.SOURCE_PROJECT_SHA256
    assert runtime["yymm4"]["timeline_frames"] == 1335
    assert runtime["execution_authority"]["authority_id"] == render.AUTHORITY_ID
    assert runtime["execution_authority"]["standing_authority"] is False
    assert runtime["output"]["run_id"] == render.PRIMARY_RUN_ID


def test_runtime_provenance_adapts_reused_crop_metadata_without_source_mutation():
    predecessor = json.loads(
        (ROOT / render.REAL_MEDIA_PROVENANCE).read_text("utf-8")
    )
    before = copy.deepcopy(predecessor)
    runtime = render._runtime_provenance(predecessor)
    assert predecessor == before
    assert all(asset["crop_or_segment"] for asset in runtime["assets"])
    assert runtime["runtime_resolution"]["source_provenance_sha256"] == (
        render.REAL_MEDIA_PROVENANCE_SHA256
    )
    assert runtime["runtime_resolution"]["source_bytes_mutated"] is False


def test_incomplete_primary_collision_is_preserved_and_successor_selected(tmp_path):
    predecessor = json.loads((ROOT / render.PRE_RENDER_MANIFEST).read_text("utf-8"))
    source_readback = json.loads(
        (ROOT / render.SOURCE_PROJECT_READBACK).read_text("utf-8")
    )
    primary = tmp_path / render.RUN_ROOT / render.PRIMARY_RUN_ID
    primary.mkdir(parents=True)
    (primary / "failed-attempt.local.log").write_text("preserve", encoding="utf-8")
    run_id, _, completed, collisions = render._next_run(
        root=tmp_path,
        predecessor_manifest=predecessor,
        predecessor_provenance=json.loads(
            (ROOT / render.REAL_MEDIA_PROVENANCE).read_text("utf-8")
        ),
        source_readback=source_readback,
        episode_runner=lambda **_: pytest.fail("runner must not launch"),
    )
    assert run_id == "food_expiry_labels_internal_review_v2"
    assert completed is None
    assert collisions == [render.PRIMARY_RUN_ID]
    assert (primary / "failed-attempt.local.log").read_text("utf-8") == "preserve"


def test_output_namespace_exhaustion_fails_before_render(tmp_path):
    predecessor = json.loads((ROOT / render.PRE_RENDER_MANIFEST).read_text("utf-8"))
    source_readback = json.loads(
        (ROOT / render.SOURCE_PROJECT_READBACK).read_text("utf-8")
    )
    for sequence in range(1, 33):
        (tmp_path / render.RUN_ROOT / f"food_expiry_labels_internal_review_v{sequence}").mkdir(
            parents=True
        )
    _assert_code(
        "output_namespace_exhausted",
        lambda: render._next_run(
            root=tmp_path,
            predecessor_manifest=predecessor,
            predecessor_provenance=json.loads(
                (ROOT / render.REAL_MEDIA_PROVENANCE).read_text("utf-8")
            ),
            source_readback=source_readback,
            episode_runner=lambda **_: pytest.fail("runner must not launch"),
        ),
    )


def _completed_fixture(tmp_path: Path, *, corrupt: str | None = None) -> tuple[str, dict]:
    run_id = render.PRIMARY_RUN_ID
    generated = Path("private_runs/generated_project.local.ymmp")
    mp4 = Path("private_runs/internal_review.mp4")
    (tmp_path / generated).parent.mkdir(parents=True)
    (tmp_path / generated).write_bytes(b"generated-project")
    (tmp_path / mp4).write_bytes(b"mp4")
    generated_sha = render.sha256_file(tmp_path / generated)
    mp4_sha = render.sha256_file(tmp_path / mp4)
    if corrupt == "generated":
        generated_sha = "0" * 64
    if corrupt == "mp4":
        mp4_sha = "0" * 64
    payload = {
        "schema": render.RENDER_READBACK_SCHEMA,
        "status": "passed",
        "run_id": run_id,
        "content_identity_sha256": render.CONTENT_IDENTITY_SHA256,
        "generated_project": {
            "path": generated.as_posix(),
            "sha256": generated_sha,
        },
        "media": {
            "path": mp4.as_posix(),
            "sha256": mp4_sha,
        },
    }
    for relative in (
        render.RENDER_PROMOTION_RECEIPT,
        render.SUCCESSOR_DESCRIPTOR,
        render.SUCCESSOR_QUEUE,
    ):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("{}", encoding="utf-8")
    readback = tmp_path / render.RENDER_READBACK
    readback.parent.mkdir(parents=True, exist_ok=True)
    readback.write_text(json.dumps(payload), encoding="utf-8")
    resume = {
        "status": "passed",
        "resume_observation": {
            "status": "verified_noop",
            "outputs_rewritten": False,
            "artifact_identities_exact": True,
        },
    }
    return run_id, resume


@pytest.mark.parametrize("corrupt", ["generated", "mp4"])
def test_corrupt_completed_output_fails_closed(tmp_path, monkeypatch, corrupt):
    run_id, resume = _completed_fixture(tmp_path, corrupt=corrupt)
    monkeypatch.setattr(
        render,
        "_validate_successors",
        lambda root: {"evaluation_sha256": "1" * 64, "counts": {}},
    )
    _assert_code(
        "completed_run_render_evidence_drift",
        lambda: render._known_completion(
            root=tmp_path,
            run_id=run_id,
            result=resume,
        ),
    )


def test_completed_run_resume_creates_only_append_only_noop_observation(
    tmp_path, monkeypatch
):
    run_id, resume = _completed_fixture(tmp_path)
    monkeypatch.setattr(
        render,
        "_validate_successors",
        lambda root: {"evaluation_sha256": "1" * 64, "counts": {"verified_noop": 4}},
    )
    result = render._known_completion(
        root=tmp_path,
        run_id=run_id,
        result=resume,
    )
    assert result["status"] == "verified_noop"
    observation = json.loads(
        (tmp_path / render.RENDER_RESUME_OBSERVATION).read_text("utf-8")
    )
    assert observation["outputs_rewritten"] is False
    assert observation["yymm4_launch_count"] == 0
    assert observation["render_driver_launch_count"] == 0
    assert observation["ffmpeg_encode_count"] == 0
