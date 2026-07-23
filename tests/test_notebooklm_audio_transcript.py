from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from src.cli.main import main as cli_main
from src.pipeline.notebooklm_audio_transcript import (
    ANONYMOUS_IDENTITIES,
    CLAIM_CLASSES,
    STYLE_CLASSES,
    analyze_notebooklm_audio_transcript,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = (
    REPO_ROOT
    / "production_pilots/yukkuri_newsroom_content_spine_002"
    / "real_input_intake_readiness/real_input/transcript/new_banknote_notebooklm"
)
RAW = INPUT_ROOT / "raw/notebooklm_audio_overview_transcript_raw.txt"
MANIFEST = INPUT_ROOT / "capture_manifest.json"
EXPECTED_SHA = "1825c9689a050ddbfc91537a228f6af0ba2f7f033e5b681fff4f227551144437"
EXPECTED_SIZE = 32089
EXPECTED_LINES = 326


def _hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


def _write_packet(root: Path, text: str) -> tuple[Path, Path]:
    raw = root / "raw.txt"
    manifest = root / "capture_manifest.json"
    raw.parent.mkdir(parents=True, exist_ok=True)
    data = text.encode("utf-8")
    raw.write_bytes(data)
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "notebooklm_audio_overview_capture.v2",
                "raw_transcript_sha256": hashlib.sha256(data).hexdigest(),
                "raw_transcript_size_bytes": len(data),
                "raw_transcript_line_count": len(text.replace("\r\n", "\n").split("\n")),
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return raw, manifest


@pytest.mark.requires_local_evidence(
    "notebooklm_audio_raw_packet",
    RAW.relative_to(REPO_ROOT).as_posix(),
    MANIFEST.relative_to(REPO_ROOT).as_posix(),
)
def test_real_packet_identity_coverage_and_sanitized_layers(tmp_path: Path) -> None:
    before = RAW.read_bytes()
    tracked = tmp_path / "tracked"
    local = tmp_path / "local"

    result = analyze_notebooklm_audio_transcript(
        raw_path=RAW,
        capture_manifest_path=MANIFEST,
        tracked_output_dir=tracked,
        local_output_dir=local,
        raw_label="real_input/transcript/new_banknote_notebooklm/raw/transcript.txt",
    )

    assert RAW.read_bytes() == before
    assert result["raw_sha256"] == EXPECTED_SHA
    assert result["raw_size_bytes"] == EXPECTED_SIZE
    assert result["raw_logical_lines"] == EXPECTED_LINES
    assert result["mapped_lines"] == EXPECTED_LINES
    line_map = json.loads((local / "raw_line_map.json").read_text(encoding="utf-8"))
    assert [line["ordinal"] for line in line_map["lines"]] == list(range(1, 327))
    assert len({line["fingerprint"] for line in line_map["lines"]}) < EXPECTED_LINES

    dedup = json.loads((tracked / "deduplication_readback.json").read_text(encoding="utf-8"))
    assert dedup["near_span_cluster_count"] >= 1
    assert dedup["universal_design_repetition_detected"] is True
    style = json.loads((tracked / "notebooklm_style_profile.json").read_text(encoding="utf-8"))
    assert {item["class"] for item in style["classes"]} == set(STYLE_CLASSES)
    assert all(item["finding_count"] >= 1 for item in style["classes"])
    turns = json.loads((local / "turn_segmentation_candidates.json").read_text(encoding="utf-8"))
    assert {turn["identity"] for turn in turns["turns"]} <= ANONYMOUS_IDENTITIES
    assert len(turns["turns"]) == EXPECTED_LINES
    claims = json.loads((tracked / "claim_risk_ledger.json").read_text(encoding="utf-8"))
    assert claims["verified_claim_count"] == 0
    assert set(claims["class_counts"]) == set(CLAIM_CLASSES)
    assert not any(claim["verified"] for claim in claims["claims"])
    tracked_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in tracked.iterdir()
        if path.is_file() and path.suffix in {".json", ".md"}
    )
    assert "C:\\Users\\" not in tracked_text
    assert "/home/" not in tracked_text
    for line in before.decode("utf-8").splitlines():
        assert not any(
            line[index : index + 80] in tracked_text
            for index in range(max(0, len(line) - 79))
        )


def test_separator_count_differs_from_logical_line_count(tmp_path: Path) -> None:
    raw, manifest = _write_packet(tmp_path / "packet", "first\r\nsecond\r\nthird")
    tracked = tmp_path / "tracked"
    local = tmp_path / "local"
    result = analyze_notebooklm_audio_transcript(
        raw_path=raw,
        capture_manifest_path=manifest,
        tracked_output_dir=tracked,
        local_output_dir=local,
    )
    receipt = json.loads((tracked / "input_identity_receipt.json").read_text(encoding="utf-8"))
    assert result["raw_logical_lines"] == 3
    assert receipt["newline_counts"]["crlf_separators"] == 2


def test_deterministic_duplicate_style_and_anonymous_analysis(tmp_path: Path) -> None:
    repeated = [
        "リスナーのあなたへ今回の深掘り解説です。",
        "裏のミッションがあるとしたらどう思いますか?",
        "はい。",
        "技術のため結果が変わるという説明です。",
        "数字は 10 億円だという主張です。",
        "ユニバーサルデザインの技術です。",
    ]
    text = "\r\n".join(repeated + repeated + ["また次回お会いしましょう。"])
    raw, manifest = _write_packet(tmp_path / "packet", text)
    first = tmp_path / "first"
    second = tmp_path / "second"

    analyze_notebooklm_audio_transcript(
        raw_path=raw,
        capture_manifest_path=manifest,
        tracked_output_dir=first,
        local_output_dir=first / "local_outputs",
    )
    analyze_notebooklm_audio_transcript(
        raw_path=raw,
        capture_manifest_path=manifest,
        tracked_output_dir=second,
        local_output_dir=second / "local_outputs",
    )

    assert _hashes(first) == _hashes(second)
    dedup = json.loads((first / "deduplication_readback.json").read_text(encoding="utf-8"))
    assert dedup["near_span_cluster_count"] >= 1
    ledger = json.loads((first / "notebooklm_style_contamination_ledger.json").read_text(encoding="utf-8"))
    classes = {item["class"] for item in ledger["findings"]}
    assert "listener_address" in classes
    assert "suspense_hidden_mission_framing" in classes
    assert "closing_boilerplate" in classes


def test_cli_and_identity_mismatch_failure(tmp_path: Path) -> None:
    raw, manifest = _write_packet(tmp_path / "packet", "first\nsecond")
    output = tmp_path / "tracked"
    assert cli_main(
        [
            "analyze-notebooklm-audio-transcript",
            "--raw",
            str(raw),
            "--capture-manifest",
            str(manifest),
            "--output",
            str(output),
            "--local-output",
            str(tmp_path / "local"),
            "--format",
            "json",
        ]
    ) == 0
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["raw_transcript_line_count"] = 99
    manifest.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="raw identity mismatch"):
        analyze_notebooklm_audio_transcript(
            raw_path=raw,
            capture_manifest_path=manifest,
            tracked_output_dir=tmp_path / "other",
        )


def test_repo_ignore_authorities_keep_raw_and_local_outputs_untracked() -> None:
    package = (
        REPO_ROOT
        / "production_pilots/yukkuri_newsroom_content_spine_002"
        / "external_editorial_input/new_banknote_security_notebooklm_001"
    )
    local_line_map = package / "local_outputs/raw_line_map.json"
    for path in (RAW, MANIFEST, local_line_map):
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", str(path)],
            cwd=REPO_ROOT,
            check=False,
        )
        assert ignored.returncode == 0
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(path)],
            cwd=REPO_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        assert tracked.returncode != 0
