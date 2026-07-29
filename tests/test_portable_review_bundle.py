from __future__ import annotations

import copy
import json
import shutil
import stat
import uuid
import zipfile
from pathlib import Path

import pytest

import src.pipeline.portable_review_bundle as module
from src.cli import main as cli
from src.pipeline.portable_review_bundle import (
    PortableReviewBundleError,
    build_portable_review_bundle,
    canonical_json_bytes,
    inspect_source_packet,
    sha256_file,
    transport_portable_review_bundle,
    validate_portable_review_bundle,
    validate_recipient_open_receipt,
)


from src.pipeline.portable_review_bundle import (
    empty_review_bundle_registry,
    ingest_portable_review_bundle,
    validate_review_bundle_ingest_authority,
    validate_review_bundle_registry,
)


ROOT = Path(__file__).resolve().parents[1]
PACKET = Path(
    "production_pilots/factory_canaries/food_expiry_labels_001/"
    "auto_video_runs/food_expiry_labels_internal_review_v4/"
    "content_review_packets/cue_002_queue_derivative_v1"
)
DESCRIPTOR = Path(
    "production_pilots/factory_canaries/food_expiry_labels_001/"
    "cue_002_portable_review_bundle_descriptor.json"
)
TRACKED_RECEIPT = Path(
    "production_pilots/factory_canaries/food_expiry_labels_001/"
    "cue_002_queue_review_packet_receipt.json"
)


def _temp_root(label: str) -> Path:
    return ROOT / "_tmp" / f"portable-review-{label}-{uuid.uuid4().hex[:10]}"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(value))


def _rewrite_bundle_file(directory: Path, relative: str, data: bytes) -> None:
    (directory / relative).write_bytes(data)
    lines = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.name == "checksums.sha256":
            continue
        locator = path.relative_to(directory).as_posix()
        lines.append(f"{sha256_file(path)}  {locator}")
    (directory / "checksums.sha256").write_text(
        "\n".join(lines) + "\n",
        encoding="ascii",
        newline="\n",
    )


def _descriptor_for(
    root: Path,
    *,
    packet: Path = PACKET,
    receipt: Path = TRACKED_RECEIPT,
) -> Path:
    descriptor = _load(ROOT / DESCRIPTOR)
    descriptor["source_packet"]["path"] = packet.as_posix()
    descriptor["source_packet"]["tracked_receipt_path"] = receipt.as_posix()
    descriptor["source_packet"]["tracked_receipt_sha256"] = sha256_file(
        ROOT / receipt
    )
    descriptor["source_packet"]["manifest_sha256"] = sha256_file(
        ROOT / packet / "packet_manifest.json"
    )
    descriptor["output"] = {
        "directory": (root / "bundle").relative_to(ROOT).as_posix(),
        "archive": (root / "bundle.zip").relative_to(ROOT).as_posix(),
    }
    path = root / "descriptor.json"
    _write(path, descriptor)
    return path.relative_to(ROOT)


def _source_fixture(root: Path) -> tuple[Path, Path, Path]:
    packet = root / "packet"
    shutil.copytree(ROOT / PACKET, packet)
    packet_locator = packet.relative_to(ROOT)
    receipt = _load(ROOT / TRACKED_RECEIPT)
    receipt["packet"]["path"] = packet_locator.as_posix()
    receipt_path = root / "receipt.json"
    _write(receipt_path, receipt)
    descriptor_path = _descriptor_for(
        root,
        packet=packet_locator,
        receipt=receipt_path.relative_to(ROOT),
    )
    return packet_locator, receipt_path.relative_to(ROOT), descriptor_path


def _build_fixture(root: Path) -> tuple[Path, Path, Path, dict]:
    root.mkdir(parents=True, exist_ok=False)
    descriptor_path = _descriptor_for(root)
    descriptor = _load(ROOT / descriptor_path)
    result = build_portable_review_bundle(
        repo_root=ROOT,
        packet_path=PACKET,
        output_path=descriptor["output"]["directory"],
        archive_path=descriptor["output"]["archive"],
        descriptor_path=descriptor_path,
    )
    return (
        ROOT / descriptor["output"]["directory"],
        ROOT / descriptor["output"]["archive"],
        descriptor_path,
        result,
    )


def _base_recipient_receipt() -> dict:
    return {
        "schema": "nlmytgen.review_bundle_recipient_open.v1",
        "schema_version": "1.0",
        "bundle": {
            "bundle_id": "bundle-v1",
            "bundle_version": 1,
            "manifest_sha256": "1" * 64,
            "archive_sha256": "2" * 64,
        },
        "recipient_id": "isolated-recipient-v1",
        "transport": "completed",
        "identity_check": "valid",
        "machine_open": "unverified",
        "machine_open_evidence_id": None,
        "human_open": "unverified",
        "human_open_evidence_id": None,
        "content_decision": "none",
        "content_decision_receipt_id": None,
        "rights": {"approved": False, "authority_id": None},
        "production": {"approved": False, "authority_id": None},
        "publication": {"approved": False, "authority_id": None},
        "delivery_complete": False,
    }


def test_real_source_packet_resolves_exact_tracked_and_local_identity() -> None:
    result = inspect_source_packet(
        repo_root=ROOT,
        packet_path=PACKET,
        descriptor_path=DESCRIPTOR,
    )
    assert result["status"] == "passed"
    assert result["packet_id"] == (
        "food_expiry_labels_001_cue_002_queue_derivative_v1"
    )
    assert result["cue"]["cue_id"] == "cue_002"
    assert (result["cue"]["start_frame"], result["cue"]["end_frame"]) == (
        373,
        816,
    )
    assert len(result["file_identities"]) == 5
    assert all(row["size_bytes"] > 0 for row in result["file_identities"])


def test_build_is_deterministic_and_directory_zip_semantics_match() -> None:
    root = _temp_root("build")
    try:
        directory, archive, _, result = _build_fixture(root)
        assert result["status"] == "succeeded"
        assert result["determinism"]["assembly_count"] == 2
        assert result["determinism"]["archive_byte_identical"] is True
        directory_result = validate_portable_review_bundle(
            bundle_path=directory,
        )
        archive_result = validate_portable_review_bundle(
            bundle_path=archive,
        )
        assert directory_result["file_count"] == 10
        assert (
            directory_result["semantic_identity_sha256"]
            == archive_result["semantic_identity_sha256"]
        )
        assert directory_result["states"]["human_open"] == "unverified"
        assert directory_result["states"]["delivery_complete"] is False
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_public_cli_build_and_validate_are_json_and_no_overwrite(
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = _temp_root("cli")
    root.mkdir(parents=True, exist_ok=False)
    try:
        descriptor_path = _descriptor_for(root)
        descriptor = _load(ROOT / descriptor_path)
        args = [
            "build-portable-review-bundle",
            "--packet",
            PACKET.as_posix(),
            "--output",
            descriptor["output"]["directory"],
            "--archive",
            descriptor["output"]["archive"],
            "--descriptor",
            descriptor_path.as_posix(),
            "--format",
            "json",
        ]
        assert cli.main(args) == 0
        built = json.loads(capsys.readouterr().out)
        assert built["status"] == "succeeded"
        assert cli.main(args) == 1
        failed = json.loads(capsys.readouterr().err)
        assert failed["error_code"] == "review_bundle_overwrite_forbidden"
        assert cli.main(
            [
                "validate-portable-review-bundle",
                "--bundle",
                descriptor["output"]["archive"],
                "--format",
                "json",
            ]
        ) == 0
        validated = json.loads(capsys.readouterr().out)
        assert validated["status"] == "passed"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_source_packet_hash_mismatch_and_missing_file_fail_closed() -> None:
    root = _temp_root("source-drift")
    root.mkdir(parents=True, exist_ok=False)
    try:
        packet, _, descriptor = _source_fixture(root)
        target = ROOT / packet / "cue_002_render_frame.png"
        target.write_bytes(target.read_bytes() + b"drift")
        with pytest.raises(PortableReviewBundleError) as observed:
            inspect_source_packet(
                repo_root=ROOT,
                packet_path=packet,
                descriptor_path=descriptor,
            )
        assert observed.value.code == "source_packet_hash_mismatch"

        shutil.rmtree(ROOT / packet)
        packet, _, descriptor = _source_fixture(root / "missing")
        (ROOT / packet / "README_REVIEW.md").unlink()
        with pytest.raises(PortableReviewBundleError) as observed:
            inspect_source_packet(
                repo_root=ROOT,
                packet_path=packet,
                descriptor_path=descriptor,
            )
        assert observed.value.code == "source_packet_file_set_mismatch"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_source_manifest_contradiction_fails_after_exact_manifest_rebind() -> None:
    root = _temp_root("manifest-contradiction")
    root.mkdir(parents=True, exist_ok=False)
    try:
        packet, receipt_path, descriptor_path = _source_fixture(root)
        manifest_path = ROOT / packet / "packet_manifest.json"
        manifest = _load(manifest_path)
        manifest["generated_project"]["sha256"] = "0" * 64
        _write(manifest_path, manifest)
        new_manifest_hash = sha256_file(manifest_path)
        receipt = _load(ROOT / receipt_path)
        receipt["packet"]["manifest_sha256"] = new_manifest_hash
        _write(ROOT / receipt_path, receipt)
        descriptor = _load(ROOT / descriptor_path)
        descriptor["source_packet"]["manifest_sha256"] = new_manifest_hash
        descriptor["source_packet"]["tracked_receipt_sha256"] = sha256_file(
            ROOT / receipt_path
        )
        _write(ROOT / descriptor_path, descriptor)
        with pytest.raises(PortableReviewBundleError) as observed:
            inspect_source_packet(
                repo_root=ROOT,
                packet_path=packet,
                descriptor_path=descriptor_path,
            )
        assert observed.value.code == "source_packet_manifest_contradiction"
    finally:
        shutil.rmtree(root, ignore_errors=True)


@pytest.mark.parametrize(
    "path",
    [
        "C:/private/file.png",
        "/absolute/file.png",
        "../escape/file.png",
        "safe/../../escape.png",
        "safe\\windows.png",
    ],
)
def test_absolute_and_traversal_paths_are_rejected(path: str) -> None:
    with pytest.raises(PortableReviewBundleError) as observed:
        module._portable_path(path, field_path="$.path")
    assert observed.value.code == "review_bundle_path_unsafe"


def test_duplicate_normalized_path_symlink_and_size_ceiling_are_rejected(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    duplicate = tmp_path / "duplicate.zip"
    with zipfile.ZipFile(duplicate, "w") as archive:
        archive.writestr(
            zipfile.ZipInfo("A.txt", module.NORMALIZED_ZIP_TIME),
            b"a",
        )
        archive.writestr(
            zipfile.ZipInfo("a.txt", module.NORMALIZED_ZIP_TIME),
            b"b",
        )
    with pytest.raises(PortableReviewBundleError) as observed:
        validate_portable_review_bundle(bundle_path=duplicate)
    assert observed.value.code == "review_bundle_duplicate_path"

    linked = tmp_path / "linked.zip"
    with zipfile.ZipFile(linked, "w") as archive:
        info = zipfile.ZipInfo("linked.txt")
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        archive.writestr(info, b"target")
    with pytest.raises(PortableReviewBundleError) as observed:
        validate_portable_review_bundle(bundle_path=linked)
    assert observed.value.code == "review_bundle_symlink_forbidden"

    ceiling = tmp_path / "ceiling.zip"
    with zipfile.ZipFile(ceiling, "w") as archive:
        archive.writestr(
            zipfile.ZipInfo("large.txt", module.NORMALIZED_ZIP_TIME),
            b"xx",
        )
    monkeypatch.setattr(module, "MAX_FILE_BYTES", 1)
    with pytest.raises(PortableReviewBundleError) as observed:
        validate_portable_review_bundle(bundle_path=ceiling)
    assert observed.value.code == "review_bundle_size_ceiling"


def test_foreign_existing_destination_and_modified_file_are_rejected() -> None:
    root = _temp_root("destination")
    try:
        directory, archive, descriptor_path, _ = _build_fixture(root)
        descriptor = _load(ROOT / descriptor_path)
        with pytest.raises(PortableReviewBundleError) as observed:
            build_portable_review_bundle(
                repo_root=ROOT,
                packet_path=PACKET,
                output_path=descriptor["output"]["directory"],
                archive_path=descriptor["output"]["archive"],
                descriptor_path=descriptor_path,
            )
        assert observed.value.code == "review_bundle_overwrite_forbidden"
        index = directory / "README_OPEN.md"
        index.write_bytes(index.read_bytes() + b"modified")
        with pytest.raises(PortableReviewBundleError) as observed:
            validate_portable_review_bundle(bundle_path=directory)
        assert observed.value.code == "review_bundle_archive_hash_mismatch"

        destination = root / "recipient-existing"
        destination.mkdir()
        with pytest.raises(PortableReviewBundleError) as observed:
            transport_portable_review_bundle(
                archive_path=archive,
                destination_root=destination,
                recipient_id="isolated-recipient-v1",
                expected_recipient_id="isolated-recipient-v1",
            )
        assert observed.value.code == "recipient_destination_exists"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_portable_manifest_schema_and_initial_states_are_fail_closed() -> None:
    root = _temp_root("manifest-schema")
    try:
        directory, _, _, _ = _build_fixture(root)
        manifest = _load(directory / "portable_bundle_manifest.json")
        manifest["states"]["human_open"] = "verified"
        _rewrite_bundle_file(
            directory,
            "portable_bundle_manifest.json",
            canonical_json_bytes(manifest),
        )
        with pytest.raises(PortableReviewBundleError) as observed:
            validate_portable_review_bundle(bundle_path=directory)
        assert observed.value.code == "review_bundle_manifest_invalid"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_offline_entrypoint_external_resource_and_autoplay_fail_closed() -> None:
    with pytest.raises(PortableReviewBundleError) as observed:
        module._validate_offline_index({})
    assert observed.value.code == "review_bundle_entrypoint_missing"

    external = {
        "index.html": (
            b'<!doctype html><video controls muted preload="none" '
            b'src="media.mp4"></video><img src="a.png"><img src="b.png">'
            b'<a href="https://example.invalid/">external</a>'
        ),
        "media.mp4": b"x",
        "a.png": b"x",
        "b.png": b"x",
    }
    with pytest.raises(PortableReviewBundleError) as observed:
        module._validate_offline_index(external)
    assert observed.value.code == "review_bundle_external_resource"

    autoplay = copy.deepcopy(external)
    autoplay["index.html"] = (
        b'<!doctype html><video controls muted autoplay preload="none" '
        b'src="media.mp4"></video><img src="a.png"><img src="b.png">'
    )
    with pytest.raises(PortableReviewBundleError) as observed:
        module._validate_offline_index(autoplay)
    assert observed.value.code == "review_bundle_autoplay_forbidden"


def test_source_mutation_during_build_is_detected_on_isolated_copy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = _temp_root("mutation")
    root.mkdir(parents=True, exist_ok=False)
    try:
        packet, _, descriptor_path = _source_fixture(root)
        descriptor = _load(ROOT / descriptor_path)
        original_write = module._write_directory

        def mutate_then_write(path: Path, files: dict[str, bytes]) -> None:
            original_write(path, files)
            source_readme = ROOT / packet / "README_REVIEW.md"
            source_readme.write_bytes(source_readme.read_bytes() + b"mutation")

        monkeypatch.setattr(module, "_write_directory", mutate_then_write)
        with pytest.raises(PortableReviewBundleError) as observed:
            build_portable_review_bundle(
                repo_root=ROOT,
                packet_path=packet,
                output_path=descriptor["output"]["directory"],
                archive_path=descriptor["output"]["archive"],
                descriptor_path=descriptor_path,
            )
        assert observed.value.code == "source_packet_mutated"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_recipient_state_axes_never_infer_human_content_or_approval() -> None:
    machine = _base_recipient_receipt()
    machine["machine_open"] = "verified"
    machine["machine_open_evidence_id"] = "machine-open-proof-v1"
    assert validate_recipient_open_receipt(machine)["human_open"] == "unverified"

    human = copy.deepcopy(machine)
    human["human_open"] = "verified"
    with pytest.raises(PortableReviewBundleError) as observed:
        validate_recipient_open_receipt(human)
    assert observed.value.code == "human_open_inference_forbidden"

    decision = copy.deepcopy(machine)
    decision["content_decision"] = "recorded"
    with pytest.raises(PortableReviewBundleError) as observed:
        validate_recipient_open_receipt(decision)
    assert observed.value.code == "content_decision_inference_forbidden"

    for axis in ("rights", "production", "publication"):
        approved = copy.deepcopy(machine)
        approved[axis]["approved"] = True
        with pytest.raises(PortableReviewBundleError) as observed:
            validate_recipient_open_receipt(approved)
        assert observed.value.code == "approval_inference_forbidden"

    completed = copy.deepcopy(machine)
    completed["delivery_complete"] = True
    with pytest.raises(PortableReviewBundleError) as observed:
        validate_recipient_open_receipt(completed)
    assert observed.value.code == "delivery_complete_inference_forbidden"


def test_recipient_transport_is_byte_exact_and_recipient_bound() -> None:
    root = _temp_root("transport")
    try:
        _, archive, _, _ = _build_fixture(root)
        with pytest.raises(PortableReviewBundleError) as observed:
            transport_portable_review_bundle(
                archive_path=archive,
                destination_root=root / "wrong-recipient",
                recipient_id="recipient-b",
                expected_recipient_id="recipient-a",
            )
        assert observed.value.code == "recipient_identity_mismatch"
        transported = transport_portable_review_bundle(
            archive_path=archive,
            destination_root=root / "recipient",
            recipient_id="recipient-a",
            expected_recipient_id="recipient-a",
        )
        assert transported["status"] == "passed"
        assert transported["archive_copy_mismatch_count"] == 0
        assert transported["states"]["human_open"] == "unverified"
        assert transported["states"]["delivery_complete"] is False
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _registry_authority(
    archive_sha256: str,
    *,
    status: str = "active",
    mode: str = "local_ingest",
    named_terminal_id: str | None = None,
    named_terminal_available: bool = False,
) -> dict:
    return {
        "schema": "nlmytgen.review_bundle_ingest_authority.v1",
        "schema_version": "1.0",
        "authority_id": "authority-recipient-ingest-v1",
        "recipient_id": "recipient-a",
        "artifact": {
            "bundle_id": "bundle-v1",
            "bundle_version": 1,
            "archive_sha256": archive_sha256,
            "status": status,
        },
        "transport": {
            "mode": mode,
            "named_terminal_id": named_terminal_id,
            "named_terminal_available": named_terminal_available,
        },
    }


def _mock_registry_pipeline(
    monkeypatch: pytest.MonkeyPatch,
) -> list[Path]:
    transported: list[Path] = []

    def validate(*, bundle_path: Path, check_machine_open: bool) -> dict:
        assert check_machine_open is False
        return {
            "bundle_id": "bundle-v1",
            "bundle_version": 1,
            "archive_sha256": sha256_file(bundle_path),
            "manifest_sha256": "b" * 64,
            "semantic_identity_sha256": "c" * 64,
        }

    def transport(
        *,
        archive_path: Path,
        destination_root: Path,
        recipient_id: str,
        expected_recipient_id: str,
    ) -> dict:
        assert recipient_id == expected_recipient_id == "recipient-a"
        destination = Path(destination_root)
        destination.mkdir(parents=True, exist_ok=False)
        transported.append(destination)
        return {
            "copied_archive_sha256": sha256_file(archive_path),
            "extracted_semantic_identity_sha256": "c" * 64,
            "extracted_file_count": 10,
        }

    monkeypatch.setattr(module, "validate_portable_review_bundle", validate)
    monkeypatch.setattr(module, "transport_portable_review_bundle", transport)
    return transported


def test_recipient_registry_ingest_is_keyed_path_free_and_duplicate_safe(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    archive = tmp_path / "bundle.zip"
    archive.write_bytes(b"bundle-v1")
    archive_sha256 = sha256_file(archive)
    registry = tmp_path / "recipient" / "registry.json"
    destination = tmp_path / "recipient" / "first-ingest"
    transported = _mock_registry_pipeline(monkeypatch)

    result = ingest_portable_review_bundle(
        archive_path=archive,
        registry_path=registry,
        destination_root=destination,
        authority=_registry_authority(archive_sha256),
        expected_recipient_id="recipient-a",
    )
    assert result["status"] == "succeeded"
    assert result["named_terminal_transport"] == "not_requested"
    assert result["states"]["human_open"] == "unverified"
    payload = json.loads(registry.read_text(encoding="utf-8"))
    validated = validate_review_bundle_registry(
        payload,
        expected_recipient_id="recipient-a",
    )
    assert len(validated["entries"]) == 1
    entry = validated["entries"][0]
    assert entry["bundle_id"] == "bundle-v1"
    assert entry["bundle_version"] == 1
    assert entry["archive_sha256"] == archive_sha256
    assert entry["recipient_id"] == "recipient-a"
    assert str(tmp_path) not in registry.read_text(encoding="utf-8")
    assert all("path" not in field for field in entry)

    duplicate_destination = tmp_path / "recipient" / "duplicate"
    with pytest.raises(PortableReviewBundleError) as observed:
        ingest_portable_review_bundle(
            archive_path=archive,
            registry_path=registry,
            destination_root=duplicate_destination,
            authority=_registry_authority(archive_sha256),
            expected_recipient_id="recipient-a",
        )
    assert observed.value.code == "review_bundle_registry_duplicate"
    assert not duplicate_destination.exists()
    assert transported == [destination]


def test_recipient_registry_resume_reconciles_only_exact_existing_transport(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    archive = tmp_path / "bundle.zip"
    with zipfile.ZipFile(archive, "w") as handle:
        for name, data in (("index.html", b"review"), ("assets/frame.png", b"frame")):
            info = zipfile.ZipInfo(name, date_time=module.NORMALIZED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_STORED
            handle.writestr(info, data)
    archive_sha256 = sha256_file(archive)
    destination = tmp_path / "recipient" / "interrupted-ingest"
    incoming = destination / "incoming" / archive.name
    extracted = destination / "extracted" / archive.stem
    incoming.parent.mkdir(parents=True)
    extracted.joinpath("assets").mkdir(parents=True)
    shutil.copyfile(archive, incoming)
    extracted.joinpath("index.html").write_bytes(b"review")
    extracted.joinpath("assets", "frame.png").write_bytes(b"frame")

    def validate(*, bundle_path: Path, check_machine_open: bool) -> dict:
        assert check_machine_open is False
        assert Path(bundle_path) in {archive.resolve(), extracted.resolve()}
        return {
            "bundle_id": "bundle-v1",
            "bundle_version": 1,
            "archive_sha256": archive_sha256,
            "manifest_sha256": "b" * 64,
            "semantic_identity_sha256": "c" * 64,
            "file_count": 2,
        }

    monkeypatch.setattr(module, "validate_portable_review_bundle", validate)
    registry = tmp_path / "recipient" / "registry.json"
    with pytest.raises(PortableReviewBundleError) as not_resumed:
        ingest_portable_review_bundle(
            archive_path=archive,
            registry_path=registry,
            destination_root=destination,
            authority=_registry_authority(archive_sha256),
            expected_recipient_id="recipient-a",
        )
    assert not_resumed.value.code == "recipient_destination_exists"
    assert not registry.exists()

    result = ingest_portable_review_bundle(
        archive_path=archive,
        registry_path=registry,
        destination_root=destination,
        authority=_registry_authority(archive_sha256),
        expected_recipient_id="recipient-a",
        resume_existing_transport=True,
    )
    assert result["status"] == "succeeded"
    assert result["copied_archive_sha256"] == archive_sha256
    assert len(
        validate_review_bundle_registry(
            json.loads(registry.read_text(encoding="utf-8")),
            expected_recipient_id="recipient-a",
        )["entries"]
    ) == 1

    tampered_destination = tmp_path / "recipient" / "tampered-ingest"
    shutil.copytree(destination, tampered_destination)
    tampered_destination.joinpath("unexpected.txt").write_text(
        "not part of transport",
        encoding="utf-8",
    )
    tampered_registry = tmp_path / "recipient" / "tampered-registry.json"
    with pytest.raises(PortableReviewBundleError) as tampered:
        ingest_portable_review_bundle(
            archive_path=archive,
            registry_path=tampered_registry,
            destination_root=tampered_destination,
            authority=_registry_authority(archive_sha256),
            expected_recipient_id="recipient-a",
            resume_existing_transport=True,
        )
    assert tampered.value.code == "recipient_resume_inventory_mismatch"
    assert not tampered_registry.exists()


@pytest.mark.parametrize(
    ("status", "error_code"),
    [
        ("revoked", "review_bundle_artifact_revoked"),
        ("superseded", "review_bundle_artifact_superseded"),
    ],
)
def test_recipient_registry_rejects_inactive_artifact_before_transport(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    status: str,
    error_code: str,
) -> None:
    archive = tmp_path / "bundle.zip"
    archive.write_bytes(b"bundle-v1")
    transported = _mock_registry_pipeline(monkeypatch)
    with pytest.raises(PortableReviewBundleError) as observed:
        ingest_portable_review_bundle(
            archive_path=archive,
            registry_path=tmp_path / "registry.json",
            destination_root=tmp_path / "destination",
            authority=_registry_authority(
                sha256_file(archive),
                status=status,
            ),
            expected_recipient_id="recipient-a",
        )
    assert observed.value.code == error_code
    assert transported == []
    assert not (tmp_path / "registry.json").exists()


def test_recipient_registry_rejects_missing_archive_and_version_conflict(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transported = _mock_registry_pipeline(monkeypatch)
    with pytest.raises(PortableReviewBundleError) as missing:
        ingest_portable_review_bundle(
            archive_path=tmp_path / "missing.zip",
            registry_path=tmp_path / "registry.json",
            destination_root=tmp_path / "missing-destination",
            authority=_registry_authority("a" * 64),
            expected_recipient_id="recipient-a",
        )
    assert missing.value.code == "review_bundle_archive_missing"

    first = tmp_path / "first.zip"
    first.write_bytes(b"first")
    registry = tmp_path / "registry.json"
    ingest_portable_review_bundle(
        archive_path=first,
        registry_path=registry,
        destination_root=tmp_path / "first-destination",
        authority=_registry_authority(sha256_file(first)),
        expected_recipient_id="recipient-a",
    )
    second = tmp_path / "second.zip"
    second.write_bytes(b"second")
    with pytest.raises(PortableReviewBundleError) as conflict:
        ingest_portable_review_bundle(
            archive_path=second,
            registry_path=registry,
            destination_root=tmp_path / "second-destination",
            authority=_registry_authority(sha256_file(second)),
            expected_recipient_id="recipient-a",
        )
    assert conflict.value.code == "review_bundle_registry_version_conflict"
    assert transported == [tmp_path / "first-destination"]
    assert not (tmp_path / "second-destination").exists()


def test_named_terminal_ingest_requires_exact_live_terminal_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    archive = tmp_path / "bundle.zip"
    archive.write_bytes(b"bundle-v1")
    authority = _registry_authority(
        sha256_file(archive),
        mode="named_terminal_delivery",
        named_terminal_id="review-terminal-a",
        named_terminal_available=True,
    )
    assert validate_review_bundle_ingest_authority(authority)["transport"][
        "named_terminal_id"
    ] == "review-terminal-a"
    transported = _mock_registry_pipeline(monkeypatch)
    with pytest.raises(PortableReviewBundleError) as unavailable:
        ingest_portable_review_bundle(
            archive_path=archive,
            registry_path=tmp_path / "registry.json",
            destination_root=tmp_path / "unavailable",
            authority=authority,
            expected_recipient_id="recipient-a",
        )
    assert unavailable.value.code == "review_bundle_named_terminal_unavailable"
    assert transported == []

    result = ingest_portable_review_bundle(
        archive_path=archive,
        registry_path=tmp_path / "registry.json",
        destination_root=tmp_path / "available",
        authority=authority,
        expected_recipient_id="recipient-a",
        available_named_terminal_id="review-terminal-a",
    )
    assert result["named_terminal_transport"] == "completed"
    assert result["states"]["delivery_complete"] is False
    assert transported == [tmp_path / "available"]


def test_tracked_only_absence_never_falls_back_to_regeneration() -> None:
    with pytest.raises(PortableReviewBundleError) as observed:
        inspect_source_packet(
            repo_root=ROOT,
            packet_path=(
                "production_pilots/factory_canaries/food_expiry_labels_001/"
                "auto_video_runs/private-absent/packet"
            ),
            descriptor_path=DESCRIPTOR,
        )
    assert observed.value.code == "source_bundle_unavailable"
    payload = observed.value.as_payload()
    assert payload["boundaries"]["source_packet_regeneration_count"] == 0
    assert payload["boundaries"]["yymm4_launch_count"] == 0
    assert payload["boundaries"]["render_driver_launch_count"] == 0
    assert payload["boundaries"]["network_request_count"] == 0
