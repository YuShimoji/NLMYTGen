"""Build, preflight, and collect the new-banknote YMM4 import observation batch.

The tracked package is headless and deterministic. It prepares one later
user-operated CSV import, but this module never launches YMM4, drives a GUI,
renders media, or creates a production project.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from src.pipeline.new_banknote_authoritative_script import (
    CANONICAL_TO_YMM4,
    EXPECTED_DERIVED_COUNTS,
    EXPECTED_SCENE_ALLOCATION,
    EXPECTED_SPEAKER_COUNTS,
    HUMAN_REVIEW_QUESTIONS,
    validate_new_banknote_authoritative_script_package,
)
from src.pipeline.ymm4_character_alias_profile import (
    load_yymm4_character_alias_profile,
    read_headerless_yymm4_csv,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


REPO_ROOT = Path(__file__).resolve().parents[2]
PILOT_RELATIVE = Path(
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
DEFAULT_PILOT_DIR = REPO_ROOT / PILOT_RELATIVE
PROFILE_RELATIVE = Path(
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "ymm4_character_alias_profiles/ymm4_4_53_0_9_yukkuri_characters_v1.json"
)

SUPERVISOR_RECEIPT_FILENAME = (
    "supervisor_yymm4_import_observation_review_receipt.json"
)
OPERATOR_DIRNAME = "operator_batch"
README_FILENAME = "README_OPERATOR_BATCH.md"
MANIFEST_FILENAME = "operator_batch_manifest.json"
EXPECTED_CONTRACT_FILENAME = "expected_import_contract.json"
PREFLIGHT_FILENAME = "preflight_readback.json"
RETURN_TEMPLATE_FILENAME = "operator_return_template.md"
RUN_SCRIPT_FILENAME = "run_new_banknote_yymm4_import_batch.ps1"
COLLECT_SCRIPT_FILENAME = "collect_new_banknote_yymm4_import_result.ps1"

LOCAL_OUTPUT_DIRNAME = "local_outputs"
LOCAL_PROJECT_FILENAME = "new_banknote_yymm4_import_observation.local.ymmp"
LOCAL_RESULT_FILENAME = "operator_result.json"
LOCAL_BATCH_STATE_FILENAME = "operator_batch.local.json"

SUPERVISOR_DECISION = (
    "supervisor_pass_for_bounded_yymm4_import_observation"
)
PROFILE_ID = "ymm4_4_53_0_9_yukkuri_characters_ja_v1"
PROFILE_VERSION = "4.53.0.9"
TARGET_STATE_ID = "new-banknote-yymm4-import-operator-batch-ready-v1"
ACCEPTED_SCRIPT_COMMIT = "b05eb3867caabda496fb9a0070d230a4e81aea01"

APPROVED_FILES = (
    "canonical_script.json",
    "canonical_script.txt",
    "canonical_yymm4.csv",
    "derived_yymm4_import.csv",
    "cue_source_traceability.json",
    "source_to_script_manifest.json",
)
EXPECTED_APPROVED_HASHES = {
    "canonical_script.json": (
        "4d272900e84c8f87c484aa84c1dd1909207ee8acc189603009a186af65837c47"
    ),
    "canonical_script.txt": (
        "4eff43d0cd1f7842b02aaacd8ac6393cc12910fe70f21d650d4a31c74c17c091"
    ),
    "canonical_yymm4.csv": (
        "23361565b18d5e8d96768ad2877b1505e0bdeb5aacb5fbd0022a11f5e8dcfb12"
    ),
    "derived_yymm4_import.csv": (
        "127dd3edd32ce6131f339819263a6d2716570f800ad212b0741a384b7e19f9ee"
    ),
    "cue_source_traceability.json": (
        "5b6601134baf0e319cf252c24a3addecbecc02432f9a38234fdfc6580e038f47"
    ),
    "source_to_script_manifest.json": (
        "e13fb57a2681875f577e4d85f13cf41bfc601519892fa4f975bdfcdd24d927b5"
    ),
}

_PRIVATE_PATH_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/]|\\\\[^\\\s]+[\\/]|/home/|/users/)"
)


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_json_bytes(payload))


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path.name}")
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def _csv_rows(path: Path) -> list[tuple[str, str]]:
    payload = read_headerless_yymm4_csv(path)
    return [
        (str(row["speaker"]), str(row["text"]))
        for row in payload["rows"]
    ]


def _approved_hashes(pilot: Path) -> dict[str, str]:
    return {name: _sha256(pilot / name) for name in APPROVED_FILES}


def _load_contract_inputs(pilot: Path) -> dict[str, Any]:
    validation = validate_new_banknote_authoritative_script_package(pilot)
    if validation.get("status") != "passed":
        raise ValueError(
            "AUTHORITATIVE_SCRIPT_PACKAGE_INVALID:"
            + ",".join(str(item) for item in validation.get("failed_checks", []))
        )

    script = _read_json(pilot / "canonical_script.json")
    canonical_rows = _csv_rows(pilot / "canonical_yymm4.csv")
    derived_rows = _csv_rows(pilot / "derived_yymm4_import.csv")
    expected_canonical = [
        (str(cue["speaker"]), str(cue["text"])) for cue in script["cues"]
    ]
    expected_derived = [
        (CANONICAL_TO_YMM4[speaker], text)
        for speaker, text in expected_canonical
    ]
    if canonical_rows != expected_canonical:
        raise ValueError("CANONICAL_CSV_SCRIPT_DRIFT")
    if derived_rows != expected_derived:
        raise ValueError("DERIVED_CSV_SCRIPT_DRIFT")
    if [text for _, text in canonical_rows] != [
        text for _, text in derived_rows
    ]:
        raise ValueError("CSV_TEXT_ORDER_DRIFT")

    scene_counts = Counter(str(cue["scene_id"]) for cue in script["cues"])
    speaker_counts = Counter(speaker for speaker, _ in canonical_rows)
    character_counts = Counter(character for character, _ in derived_rows)
    if dict(scene_counts) != EXPECTED_SCENE_ALLOCATION:
        raise ValueError("SCENE_ALLOCATION_DRIFT")
    if dict(speaker_counts) != EXPECTED_SPEAKER_COUNTS:
        raise ValueError("CANONICAL_SPEAKER_COUNTS_DRIFT")
    if dict(character_counts) != EXPECTED_DERIVED_COUNTS:
        raise ValueError("DERIVED_CHARACTER_COUNTS_DRIFT")
    if script.get("unsupported_claim_count") != 0:
        raise ValueError("UNSUPPORTED_SPOKEN_CLAIM_DRIFT")

    profile_path = REPO_ROOT / PROFILE_RELATIVE
    profile = load_yymm4_character_alias_profile(profile_path)
    if profile.get("profile_id") != PROFILE_ID:
        raise ValueError("CHARACTER_PROFILE_ID_DRIFT")
    observed = dict(profile.get("observed_environment") or {})
    if observed.get("yymm4_version") != PROFILE_VERSION:
        raise ValueError("CHARACTER_PROFILE_VERSION_DRIFT")
    if profile.get("canonical_to_yymm4_character") != CANONICAL_TO_YMM4:
        raise ValueError("CHARACTER_PROFILE_MAPPING_DRIFT")
    approved_hashes = _approved_hashes(pilot)
    if approved_hashes != EXPECTED_APPROVED_HASHES:
        raise ValueError("APPROVED_ARTIFACT_HASH_FREEZE_DRIFT")

    return {
        "script": script,
        "canonical_rows": canonical_rows,
        "derived_rows": derived_rows,
        "approved_hashes": approved_hashes,
        "profile": profile,
        "profile_sha256": _sha256(profile_path),
    }


def _supervisor_receipt(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": (
            "new_banknote_yymm4_import_observation.supervisor_review_receipt.v1"
        ),
        "status": "passed_for_bounded_operator_batch_preparation",
        "decision": SUPERVISOR_DECISION,
        "decision_date": "2026-07-13",
        "accepted_script_commit": ACCEPTED_SCRIPT_COMMIT,
        "review_results": [
            {
                "question_number": index,
                "question": question,
                "result": "pass_for_bounded_yymm4_import_observation",
                "scope": "operator_batch_preparation_only",
            }
            for index, question in enumerate(HUMAN_REVIEW_QUESTIONS, start=1)
        ],
        "approved_artifact_hashes": inputs["approved_hashes"],
        "approved_contract": {
            "cue_count": 9,
            "scene_allocation": EXPECTED_SCENE_ALLOCATION,
            "canonical_speaker_counts": EXPECTED_SPEAKER_COUNTS,
            "yymm4_character_counts": EXPECTED_DERIVED_COUNTS,
            "unsupported_spoken_claim_count": 0,
            "spoken_cues_may_be_revised_in_this_slice": False,
        },
        "authorization_boundary": {
            "operator_batch_preparation": True,
            "manual_import_observation": "later_user_action",
            "user_creative_preference_acceptance": False,
            "production_approval": False,
            "render_approval": False,
            "rights_approval": False,
            "publication_approval": False,
        },
        "actions": {
            "notebooklm_accessed": False,
            "network_source_fetch": False,
            "yymm4_launched": False,
            "computer_use_invoked": False,
            "render_or_media_generated": False,
        },
    }


def _expected_contract(inputs: dict[str, Any]) -> dict[str, Any]:
    rows = [
        {
            "csv_row_id": f"csv_row_{index}",
            "cue_id": f"cue_{index:03d}",
            "character": character,
            "text": text,
        }
        for index, (character, text) in enumerate(
            inputs["derived_rows"], start=1
        )
    ]
    return {
        "schema_version": (
            "new_banknote_yymm4_import_observation.expected_contract.v1"
        ),
        "status": "ready",
        "batch_scope": "csv_import_observation_only",
        "source_csv": (
            f"{PILOT_RELATIVE.as_posix()}/derived_yymm4_import.csv"
        ),
        "source_csv_sha256": inputs["approved_hashes"][
            "derived_yymm4_import.csv"
        ],
        "approved_artifact_hashes": inputs["approved_hashes"],
        "character_profile": {
            "repo_relative_path": PROFILE_RELATIVE.as_posix(),
            "profile_id": PROFILE_ID,
            "observed_yymm4_version": PROFILE_VERSION,
            "sha256": inputs["profile_sha256"],
            "version_difference_policy": "warning_only",
            "mapping_dialog_or_wrong_character_policy": "operator_stop",
        },
        "project_target": (
            f"{PILOT_RELATIVE.as_posix()}/{LOCAL_OUTPUT_DIRNAME}/"
            f"{LOCAL_PROJECT_FILENAME}"
        ),
        "operator_result_target": (
            f"{PILOT_RELATIVE.as_posix()}/{LOCAL_OUTPUT_DIRNAME}/"
            f"{LOCAL_RESULT_FILENAME}"
        ),
        "expectations": {
            "VoiceItem_count": 9,
            "character_counts": EXPECTED_DERIVED_COUNTS,
            "exact_text_and_order": True,
            "missing_count": 0,
            "duplicate_count": 0,
            "reordered": False,
            "ImageItem_required": False,
            "independent_TextItem_required": False,
            "render_required": False,
            "duration_policy": "informational_actual_frames_and_fps",
        },
        "rows": rows,
        "operator_observation_fields": {
            "no_mapping_error_update_or_character_mismatch": "required",
            "evidence_grade": "observed",
        },
        "evidence_boundary": {
            "internal_import_observation_only": True,
            "production_project": False,
            "render": False,
            "rights_or_publication_approval": False,
        },
    }


def _operator_readme() -> str:
    return """# 新紙幣9-cue YMM4 import Operator Batch

> **INTERNAL IMPORT OBSERVATION ONLY — NOT FINAL — NON-PRODUCTION**

このbatchは、承認済み9行CSVをユーザー自身がYMM4へ一度だけimportし、
保存したlocal projectをheadless collectorで検証するためのものです。
CodexはGUI、mouse、keyboard、window focusを操作しません。render、production
save、upload、publication、rights approvalも行いません。

## 事前確認

- YMM4の未保存・無関係なprojectを安全に閉じてください。
- 実行対象は ../derived_yymm4_import.csv だけです。
- 保存先は ../local_outputs/new_banknote_yymm4_import_observation.local.ymmp
  だけです。
- mapping/error/update dialog、違うcharacter、既存itemが見えたら停止します。

YMM4を起動しないpreflight:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\\run_new_banknote_yymm4_import_batch.ps1 -PreflightOnly

自動検出できない場合だけ、表示されたとおり -Ymm4Exe を付けます。

## 4 manual actions

1. このdirectoryで次を一度だけ実行します。
   powershell -NoProfile -ExecutionPolicy Bypass -File .\\run_new_banknote_yymm4_import_batch.ps1
2. 新規の空project / 空timelineで、表示されたderived CSVを台本読み込みし、
   mapping/error/update/character mismatchがない場合だけ、表示された
   .local.ymmp へ Project Save As します。
3. YMM4をrenderせず安全に閉じます。
4. 待機中terminalへ戻り、COLLECT と入力します。

件数、character 3/6、本文、順序、missing/duplicate、fps/frames/durationは
collectorが確認します。ユーザーが9件を手作業で数える必要はありません。

## Stop conditions

- YMM4がすでに起動中、または未保存・無関係な作業がある
- exact local project / result / batch-state targetが既にある
- 空でないproject/timeline、mapping dialog、error、update要求
- ゆっくり霊夢 / ゆっくり魔理沙以外へのbinding
- 保存先が表示された .local.ymmp と違う
- render、production、upload、publication、rights actionを要求される

## Recovery without YMM4 launch

manual save後にterminalだけ中断した場合は、YMM4を安全に閉じてから:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\\run_new_banknote_yymm4_import_batch.ps1 -CollectOnly -OperatorConfirmedNoMappingError

既存resultや失敗証拠を消さずに再実行したい場合は、operator directoryから
次を実行して、ignored local_outputs/archive/<timestamp>/ へ先に退避します。

    $archive = Join-Path ..\\local_outputs ("archive\\" + (Get-Date -Format "yyyyMMdd-HHmmss"))
    New-Item -ItemType Directory -Path $archive -Force
    Get-ChildItem -LiteralPath ..\\local_outputs -File | Move-Item -Destination $archive

## Return

terminalの最大3項目だけを返します。actual YMM4 importが終わるまでは、
このtracked packageだけでmapping、sound、timing、subtitle appearance、
character behaviorの成功を主張しません。
"""


def _return_template() -> str:
    return """# Operator Return (maximum 3 items)

1. result: success | failure
2. operator_result.json: <path>
3. error: <failure only; omit on success>
"""


def _run_script() -> str:
    return r'''[CmdletBinding()]
param(
    [switch]$PreflightOnly,
    [switch]$CollectOnly,
    [switch]$OperatorConfirmedNoMappingError,
    [string]$PythonExe = "",
    [string]$Ymm4Exe = ""
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

if ($PreflightOnly -and $CollectOnly) {
    throw "Choose either -PreflightOnly or -CollectOnly, not both."
}

function Resolve-RepoRoot {
    $Current = (Resolve-Path -LiteralPath $PSScriptRoot).Path
    while ($Current) {
        $ProjectFile = Join-Path $Current "pyproject.toml"
        $SourceDir = Join-Path $Current "src"
        if ((Test-Path -LiteralPath $ProjectFile -PathType Leaf) -and
            (Test-Path -LiteralPath $SourceDir -PathType Container)) {
            return $Current
        }
        $Parent = [IO.Directory]::GetParent($Current)
        if ($null -eq $Parent) { break }
        $Current = $Parent.FullName
    }
    throw "Repository root could not be resolved."
}

function Resolve-PythonExe {
    param([string]$Requested, [string]$RepoRoot)
    if ($Requested) {
        if (-not (Test-Path -LiteralPath $Requested -PathType Leaf)) {
            throw "Requested Python executable was not found."
        }
        return (Resolve-Path -LiteralPath $Requested).Path
    }
    $RepoPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $RepoPython -PathType Leaf) {
        return (Resolve-Path -LiteralPath $RepoPython).Path
    }
    throw "Python was not found. Pass -PythonExe or create the repo .venv."
}

function Read-Utf8Json {
    param([Parameter(Mandatory=$true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Expected UTF-8 JSON file was not found."
    }
    $Text = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
    return ($Text | ConvertFrom-Json)
}

function Write-Utf8Json {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)]$Value
    )
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $Json = $Value | ConvertTo-Json -Depth 10
    [IO.File]::WriteAllText(
        $Path,
        $Json + [Environment]::NewLine,
        $Utf8NoBom
    )
}

function Resolve-Ymm4Exe {
    param([string]$Requested)
    $Candidates = @()
    if ($Requested) { $Candidates += $Requested }
    if ($env:NLMYTGEN_YMM4_EXE) {
        $Candidates += $env:NLMYTGEN_YMM4_EXE
    }
    $Command = @(Get-Command -Name "YukkuriMovieMaker.exe" -ErrorAction SilentlyContinue | Select-Object -First 1)[0]
    if ($Command -and $Command.Source) {
        $Candidates += $Command.Source
    }
    $RegistryPaths = @(
        "Registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\App Paths\YukkuriMovieMaker.exe",
        "Registry::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\App Paths\YukkuriMovieMaker.exe"
    )
    foreach ($RegistryPath in $RegistryPaths) {
        $Entry = Get-ItemProperty -LiteralPath $RegistryPath -ErrorAction SilentlyContinue
        if ($Entry -and $Entry.'(default)') {
            $Candidates += [string]$Entry.'(default)'
        }
    }
    if ($env:LOCALAPPDATA) {
        $Candidates += Join-Path $env:LOCALAPPDATA "Programs\YukkuriMovieMaker4\YukkuriMovieMaker.exe"
        $Candidates += Join-Path $env:LOCALAPPDATA "YukkuriMovieMaker4\YukkuriMovieMaker.exe"
    }
    foreach ($Drive in [IO.DriveInfo]::GetDrives()) {
        if ($Drive.IsReady -and $Drive.DriveType -eq [IO.DriveType]::Fixed) {
            $Candidates += Join-Path $Drive.RootDirectory.FullName "YukkuriMovieMaker_v4\YukkuriMovieMaker.exe"
            $Candidates += Join-Path $Drive.RootDirectory.FullName "MovieCreationWorkspace\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe"
        }
    }
    foreach ($Candidate in $Candidates) {
        if ($Candidate -and (Test-Path -LiteralPath $Candidate -PathType Leaf)) {
            return (Resolve-Path -LiteralPath $Candidate).Path
        }
    }
    return $null
}

function Test-Ymm4Running {
    return [bool](Get-Process -Name "YukkuriMovieMaker" -ErrorAction SilentlyContinue)
}

$RepoRoot = Resolve-RepoRoot
$PilotDir = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$Python = Resolve-PythonExe -Requested $PythonExe -RepoRoot $RepoRoot
$Manifest = Read-Utf8Json -Path (Join-Path $PSScriptRoot "operator_batch_manifest.json")
$Messages = $Manifest.operator_messages
$DerivedCsv = Join-Path $PilotDir "derived_yymm4_import.csv"
$LocalOutput = Join-Path $PilotDir "local_outputs"
$Project = Join-Path $LocalOutput "new_banknote_yymm4_import_observation.local.ymmp"
$Result = Join-Path $LocalOutput "operator_result.json"
$BatchState = Join-Path $LocalOutput "operator_batch.local.json"

$PreflightResultFile = Join-Path ([IO.Path]::GetTempPath()) (
    "nlmytgen-new-banknote-preflight-" + [guid]::NewGuid().ToString("N") + ".json"
)
try {
    $PreflightArgs = @(
        "-m", "src.pipeline.new_banknote_yymm4_import_operator_batch",
        "preflight",
        "--pilot", $PilotDir,
        "--result-json", $PreflightResultFile
    )
    Push-Location -LiteralPath $RepoRoot
    try {
        & $Python @PreflightArgs | Out-Null
        $PreflightExit = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    $Preflight = Read-Utf8Json -Path $PreflightResultFile
    if ($PreflightExit -ne 0 -or $Preflight.status -ne "passed") {
        throw ("Tracked batch preflight failed: " + ($Preflight.failed_checks -join ", "))
    }
}
finally {
    Remove-Item -LiteralPath $PreflightResultFile -Force -ErrorAction SilentlyContinue
}

if ($CollectOnly) {
    if (Test-Ymm4Running) {
        throw "Collect-only stopped because YMM4 is still running. Close it safely; this script will not close it."
    }
    $CollectArgs = @{
        PythonExe = $Python
        PilotDir = $PilotDir
        OperatorConfirmedNoMappingError = $OperatorConfirmedNoMappingError
    }
    & (Join-Path $PSScriptRoot "collect_new_banknote_yymm4_import_result.ps1") @CollectArgs
    exit $LASTEXITCODE
}

$Ymm4 = Resolve-Ymm4Exe -Requested $Ymm4Exe
if (-not $Ymm4) {
    Write-Output "YMM4 executable was not resolved. Re-run exactly with an explicit executable:"
    Write-Output 'powershell -NoProfile -ExecutionPolicy Bypass -File .\run_new_banknote_yymm4_import_batch.ps1 -Ymm4Exe "<FULL_PATH_TO_YukkuriMovieMaker.exe>"'
    exit 2
}
$Version = [string](Get-Item -LiteralPath $Ymm4).VersionInfo.ProductVersion
if (-not $Version) { $Version = "unknown" }
$ProfileVersionMatch = $Version.StartsWith("4.53.0.9")

$ExactTargets = @($Project, $Result, $BatchState)
$ExistingTargets = @($ExactTargets | Where-Object { Test-Path -LiteralPath $_ })

if ($PreflightOnly) {
    if ($ExistingTargets.Count -gt 0) {
        throw ("Preflight stopped on existing local evidence. Archive it without deleting it: " + ($ExistingTargets -join ", "))
    }
    foreach ($ScriptName in @(
        "run_new_banknote_yymm4_import_batch.ps1",
        "collect_new_banknote_yymm4_import_result.ps1"
    )) {
        $ScriptPath = Join-Path $PSScriptRoot $ScriptName
        $null = [scriptblock]::Create(
            [IO.File]::ReadAllText($ScriptPath, [Text.Encoding]::UTF8)
        )
    }
    Write-Output "preflight: passed"
    Write-Output ("yymm4_product_version: " + $Version)
    Write-Output ("profile_version_match: " + $ProfileVersionMatch)
    return
}

if (Test-Ymm4Running) {
    throw "YMM4 is already running. Save/resolve unrelated work first; this script will not close it."
}
if ($ExistingTargets.Count -gt 0) {
    throw ("Exact local evidence already exists. Archive it manually; this script will not overwrite or delete it: " + ($ExistingTargets -join ", "))
}

New-Item -ItemType Directory -Path $LocalOutput -Force | Out-Null
$BatchStartedUtc = [DateTime]::UtcNow.ToString("o")
$BatchStateValue = [ordered]@{
    schema_version = "new_banknote_yymm4_import_operator_batch.local.v1"
    batch_id = "new-banknote-yymm4-import-observation-v1"
    batch_not_before_utc = $BatchStartedUtc
    yymm4_exe = $Ymm4
    yymm4_product_version = $Version
    profile_observation_version = "4.53.0.9"
    target_project = $Project
    target_result = $Result
}
Write-Utf8Json -Path $BatchState -Value $BatchStateValue

Write-Host $Messages.pc_control
Write-Host $Messages.scope_boundary
Write-Host $Messages.stop_conditions
if (-not $ProfileVersionMatch) {
    Write-Warning ($Messages.version_warning + " " + $Version + " / 4.53.0.9")
}
Write-Host ""
Write-Host ($Messages.csv_path + ": " + $DerivedCsv)
Write-Host ($Messages.project_path + ": " + $Project)
Write-Host $Messages.manual_sequence

Start-Process -FilePath $Ymm4 | Out-Null
$Collect = Read-Host $Messages.collect_prompt
if ($Collect -ne "COLLECT") {
    throw "Batch stopped before collection. Expected COLLECT; local evidence was preserved."
}
if (Test-Ymm4Running) {
    throw "Collection stopped because YMM4 is still running. Close it safely; local evidence was preserved."
}

$CollectArgs = @{
    PythonExe = $Python
    PilotDir = $PilotDir
    OperatorConfirmedNoMappingError = $true
}
& (Join-Path $PSScriptRoot "collect_new_banknote_yymm4_import_result.ps1") @CollectArgs
exit $LASTEXITCODE
'''


def _collect_script() -> str:
    return r'''[CmdletBinding()]
param(
    [string]$PythonExe = "",
    [string]$PilotDir = "",
    [string]$ProjectPath = "",
    [string]$OutputPath = "",
    [string]$BatchStatePath = "",
    [switch]$OperatorConfirmedNoMappingError
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

function Resolve-RepoRoot {
    $Current = (Resolve-Path -LiteralPath $PSScriptRoot).Path
    while ($Current) {
        if ((Test-Path -LiteralPath (Join-Path $Current "pyproject.toml") -PathType Leaf) -and
            (Test-Path -LiteralPath (Join-Path $Current "src") -PathType Container)) {
            return $Current
        }
        $Parent = [IO.Directory]::GetParent($Current)
        if ($null -eq $Parent) { break }
        $Current = $Parent.FullName
    }
    throw "Repository root could not be resolved."
}

function Read-Utf8Json {
    param([Parameter(Mandatory=$true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Expected UTF-8 JSON file was not found."
    }
    $Text = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
    return ($Text | ConvertFrom-Json)
}

function Write-ReturnFailure {
    param([string]$ResultPath, [string]$ErrorText)
    Write-Output "1. result: failure"
    Write-Output ("2. operator_result.json: " + $ResultPath)
    Write-Output ("3. error: " + $ErrorText)
}

$RepoRoot = Resolve-RepoRoot
if (-not $PilotDir) {
    $PilotDir = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
}
if (-not $PythonExe) {
    $PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
}
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
    throw "Python executable was not found."
}
if (-not $ProjectPath) {
    $ProjectPath = Join-Path $PilotDir "local_outputs\new_banknote_yymm4_import_observation.local.ymmp"
}
if (-not $OutputPath) {
    $OutputPath = Join-Path $PilotDir "local_outputs\operator_result.json"
}
if (-not $BatchStatePath) {
    $BatchStatePath = Join-Path $PilotDir "local_outputs\operator_batch.local.json"
}

if (Get-Process -Name "YukkuriMovieMaker" -ErrorAction SilentlyContinue) {
    Write-ReturnFailure -ResultPath $OutputPath -ErrorText "YMM4 is still running; close it safely before collect-only"
    exit 1
}
if (Test-Path -LiteralPath $OutputPath) {
    Write-ReturnFailure -ResultPath $OutputPath -ErrorText "existing result was preserved; archive it before another collection"
    exit 1
}
if (-not (Test-Path -LiteralPath $BatchStatePath -PathType Leaf)) {
    Write-ReturnFailure -ResultPath $OutputPath -ErrorText "ignored batch-state file is missing"
    exit 1
}
if (-not $OperatorConfirmedNoMappingError) {
    Write-ReturnFailure -ResultPath $OutputPath -ErrorText "collect-only requires -OperatorConfirmedNoMappingError"
    exit 1
}

$BatchState = Read-Utf8Json -Path $BatchStatePath
$Arguments = @(
    "-m", "src.pipeline.new_banknote_yymm4_import_operator_batch",
    "collect",
    "--pilot", $PilotDir,
    "--project", $ProjectPath,
    "--output", $OutputPath,
    "--not-before-utc", [string]$BatchState.batch_not_before_utc,
    "--yymm4-product-version", [string]$BatchState.yymm4_product_version,
    "--profile-observation-version", [string]$BatchState.profile_observation_version,
    "--operator-confirmed-no-mapping-error"
)

Push-Location -LiteralPath $RepoRoot
try {
    & $PythonExe @Arguments | Out-Null
    $CollectionExit = $LASTEXITCODE
}
finally {
    Pop-Location
}

if (-not (Test-Path -LiteralPath $OutputPath -PathType Leaf)) {
    Write-ReturnFailure -ResultPath $OutputPath -ErrorText "collector did not write the expected UTF-8 JSON result"
    exit 1
}
$Result = Read-Utf8Json -Path $OutputPath
if ($CollectionExit -eq 0 -and $Result.status -eq "success") {
    Write-Output "1. result: success"
    Write-Output ("2. operator_result.json: " + $OutputPath)
    exit 0
}
if (@($Result.failed_checks).Count -gt 0) {
    Write-ReturnFailure -ResultPath $OutputPath -ErrorText ($Result.failed_checks -join ", ")
} else {
    Write-ReturnFailure -ResultPath $OutputPath -ErrorText "collector returned an unexpected result state"
}
exit 1
'''


def _manifest(
    inputs: dict[str, Any],
    generated_hashes: dict[str, dict[str, str]],
) -> dict[str, Any]:
    return {
        "schema_version": (
            "new_banknote_yymm4_import_observation.operator_batch_manifest.v1"
        ),
        "artifact_id": "new-banknote-yymm4-import-observation-v1",
        "status": "ready",
        "target_state_id": TARGET_STATE_ID,
        "scope": "user_operated_csv_import_observation_only",
        "approved_script_identity": {
            "decision": SUPERVISOR_DECISION,
            "accepted_script_commit": ACCEPTED_SCRIPT_COMMIT,
            "artifact_hashes": inputs["approved_hashes"],
        },
        "character_profile": {
            "repo_relative_path": PROFILE_RELATIVE.as_posix(),
            "profile_id": PROFILE_ID,
            "observed_yymm4_version": PROFILE_VERSION,
            "sha256": inputs["profile_sha256"],
        },
        "modes": {
            "normal": {
                "may_launch_yymm4": True,
                "gui_operator": "user",
                "automatic_gui_actions": 0,
            },
            "preflight_only": {
                "parameter": "-PreflightOnly",
                "launches_yymm4": False,
                "writes_local_evidence": False,
            },
            "collect_only": {
                "parameter": (
                    "-CollectOnly -OperatorConfirmedNoMappingError"
                ),
                "launches_yymm4": False,
                "regenerates_or_overwrites_outputs": False,
            },
        },
        "manual_action_count": 4,
        "manual_actions": [
            "clean terminalからbatch commandを一度だけ実行する",
            (
                "新規空projectへdisplay済みCSVをimportし、mapping/error/update/"
                "character mismatchがなければdisplay済み.local.ymmpへ保存する"
            ),
            "renderせずYMM4を安全に閉じる",
            "待機terminalへ戻りCOLLECTと入力する",
        ],
        "return_item_count": 3,
        "return_items": [
            "success_or_failure",
            "operator_result_json_path",
            "error_only_on_failure",
        ],
        "stop_conditions": [
            "yymm4_already_running",
            "unrelated_or_unsaved_project",
            "preexisting_exact_local_target",
            "nonempty_project_or_timeline",
            "mapping_error_or_update_dialog",
            "character_mismatch",
            "unexpected_save_target",
            "render_production_public_or_rights_request",
        ],
        "targets": {
            "source_csv": (
                f"{PILOT_RELATIVE.as_posix()}/derived_yymm4_import.csv"
            ),
            "local_project": (
                f"{PILOT_RELATIVE.as_posix()}/{LOCAL_OUTPUT_DIRNAME}/"
                f"{LOCAL_PROJECT_FILENAME}"
            ),
            "local_result": (
                f"{PILOT_RELATIVE.as_posix()}/{LOCAL_OUTPUT_DIRNAME}/"
                f"{LOCAL_RESULT_FILENAME}"
            ),
            "local_batch_state": (
                f"{PILOT_RELATIVE.as_posix()}/{LOCAL_OUTPUT_DIRNAME}/"
                f"{LOCAL_BATCH_STATE_FILENAME}"
            ),
        },
        "executable_resolution": {
            "explicit_parameter": "-Ymm4Exe",
            "environment_variable": "NLMYTGEN_YMM4_EXE",
            "runtime_detection": [
                "PATH",
                "Windows App Paths registry",
                "LOCALAPPDATA common application locations",
                "fixed-drive common application-relative locations",
            ],
            "tracked_absolute_path": False,
            "unresolved_behavior": "print_exact_parameterized_command_and_stop",
        },
        "json_transport": (
            "python_writes_utf8_file_powershell_reads_explicit_utf8"
        ),
        "powershell_5_1_contract": (
            "scripts_are_ascii_only_japanese_messages_are_loaded_from_utf8_json"
        ),
        "collector_contract": {
            "VoiceItem_count": 9,
            "character_counts": EXPECTED_DERIVED_COUNTS,
            "exact_text_order": True,
            "missing_count": 0,
            "duplicate_count": 0,
            "fresh_project_required": True,
            "exact_local_target_required": True,
            "timing_is_informational": True,
            "ImageItem_required": False,
            "independent_TextItem_required": False,
            "render_required": False,
        },
        "tracked_artifacts": generated_hashes,
        "operator_messages": {
            "pc_control": (
                "PC操作主体はユーザーです。CodexはGUIを操作しません。"
            ),
            "scope_boundary": (
                "INTERNAL IMPORT OBSERVATION ONLY。render、本番、公開、"
                "権利承認は行いません。"
            ),
            "stop_conditions": (
                "未保存/無関係project、mapping/error/update dialog、"
                "character mismatch、違う保存先では直ちに停止してください。"
            ),
            "version_warning": (
                "profile観測版とruntime版が異なります。差分自体はwarningですが、"
                "mapping dialogやwrong characterでは停止します。"
            ),
            "csv_path": "台本読み込みCSV",
            "project_path": "Project Save As先",
            "manual_sequence": (
                "新規空projectへimportして保存し、renderせずYMM4を安全に"
                "閉じてからterminalへ戻ってください。"
            ),
            "collect_prompt": (
                "mapping/error/update/character mismatchがなく、exact projectを"
                "保存してYMM4を閉じた後だけCOLLECTと入力"
            ),
        },
        "prohibited_actions": [
            "computer_use",
            "automatic_gui_control",
            "render_or_mp4",
            "production_project",
            "source_or_script_revision",
            "upload_publication_or_rights_action",
            "master_integration",
        ],
    }


def render_new_banknote_yymm4_operator_artifacts(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, bytes]:
    """Render every tracked artifact byte-for-byte without writing it."""
    pilot = Path(pilot_dir).resolve()
    inputs = _load_contract_inputs(pilot)
    receipt_bytes = _json_bytes(_supervisor_receipt(inputs))
    expected_bytes = _json_bytes(_expected_contract(inputs))
    readme_bytes = _operator_readme().encode("utf-8")
    return_bytes = _return_template().encode("utf-8")
    run_bytes = _run_script().encode("ascii")
    collect_bytes = _collect_script().encode("ascii")

    base_artifacts = {
        SUPERVISOR_RECEIPT_FILENAME: receipt_bytes,
        f"{OPERATOR_DIRNAME}/{README_FILENAME}": readme_bytes,
        f"{OPERATOR_DIRNAME}/{EXPECTED_CONTRACT_FILENAME}": expected_bytes,
        f"{OPERATOR_DIRNAME}/{RETURN_TEMPLATE_FILENAME}": return_bytes,
        f"{OPERATOR_DIRNAME}/{RUN_SCRIPT_FILENAME}": run_bytes,
        f"{OPERATOR_DIRNAME}/{COLLECT_SCRIPT_FILENAME}": collect_bytes,
    }
    generated_hashes = {
        (
            f"{PILOT_RELATIVE.as_posix()}/{relative}"
        ): {"sha256": _sha256_bytes(data)}
        for relative, data in base_artifacts.items()
    }
    manifest_bytes = _json_bytes(_manifest(inputs, generated_hashes))
    with_manifest = {
        **base_artifacts,
        f"{OPERATOR_DIRNAME}/{MANIFEST_FILENAME}": manifest_bytes,
    }
    tracked_hashes = {
        f"{PILOT_RELATIVE.as_posix()}/{relative}": _sha256_bytes(data)
        for relative, data in with_manifest.items()
    }
    preflight = {
        "schema_version": (
            "new_banknote_yymm4_import_observation.preflight_readback.v1"
        ),
        "status": "passed",
        "validation_mode": "tracked_headless_contract_preflight",
        "checks": {
            "authoritative_script_package_passed": True,
            "approved_artifact_hashes_frozen": True,
            "cue_count_9": True,
            "scene_allocation_2_4_3": True,
            "canonical_speaker_counts_3_6": True,
            "derived_character_counts_3_6": True,
            "canonical_and_derived_text_order_equal": True,
            "only_speaker_column_differs": True,
            "unsupported_spoken_claims_zero": True,
            "supervisor_boundary_receipt_present": True,
            "manual_action_count_at_most_4": True,
            "return_item_count_at_most_3": True,
            "preflight_and_collect_only_launch_budget_zero": True,
            "python_powershell_utf8_file_transport": True,
            "powershell_5_1_japanese_contract": True,
            "powershell_scripts_parse_during_runtime_preflight": True,
            "no_render_image_or_independent_text_requirement": True,
            "tracked_paths_repo_relative": True,
        },
        "approved_artifact_hashes": inputs["approved_hashes"],
        "tracked_artifact_hashes": tracked_hashes,
        "profile": {
            "profile_id": PROFILE_ID,
            "observed_yymm4_version": PROFILE_VERSION,
            "sha256": inputs["profile_sha256"],
        },
        "manual_action_count": 4,
        "return_item_count": 3,
        "yymm4_launch_attempted": False,
        "computer_use_invoked": False,
        "render_or_media_generated": False,
        "runtime_command": (
            "powershell -NoProfile -ExecutionPolicy Bypass -File "
            ".\\run_new_banknote_yymm4_import_batch.ps1 -PreflightOnly"
        ),
        "note": (
            "Runtime preflight additionally resolves the local executable and "
            "reads its product version without launching YMM4."
        ),
    }
    return {
        **with_manifest,
        f"{OPERATOR_DIRNAME}/{PREFLIGHT_FILENAME}": _json_bytes(preflight),
    }


def build_new_banknote_yymm4_operator_batch(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, Any]:
    """Write the deterministic tracked receipt and operator package."""
    pilot = Path(pilot_dir).resolve()
    artifacts = render_new_banknote_yymm4_operator_artifacts(pilot)
    for relative, data in artifacts.items():
        path = pilot / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return {
        "status": "operator_batch_ready",
        "pilot_dir": str(pilot),
        "written_files": sorted(artifacts),
        "manual_action_count": 4,
        "return_item_count": 3,
    }


def preflight_new_banknote_yymm4_operator_batch(
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
) -> dict[str, Any]:
    """Validate tracked identities and runtime-safe script contracts."""
    pilot = Path(pilot_dir).resolve()
    failed: list[str] = []
    try:
        expected = render_new_banknote_yymm4_operator_artifacts(pilot)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return {
            "schema_version": (
                "new_banknote_yymm4_import_observation.runtime_preflight.v1"
            ),
            "status": "failed",
            "checks": {},
            "failed_checks": [str(exc).splitlines()[0]],
            "yymm4_launch_attempted": False,
            "computer_use_invoked": False,
        }

    artifact_matches: dict[str, bool] = {}
    for relative, expected_bytes in expected.items():
        path = pilot / relative
        matches = path.exists() and path.read_bytes() == expected_bytes
        artifact_matches[relative] = matches
        if not matches:
            failed.append(f"tracked_artifact_drift:{relative}")

    package_paths = [
        pilot / relative
        for relative in expected
        if (pilot / relative).exists()
    ]
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in package_paths
    )
    privacy_pass = _PRIVATE_PATH_RE.search(combined) is None
    if not privacy_pass:
        failed.append("tracked_private_absolute_path_present")

    run_text = _run_script()
    collect_text = _collect_script()
    run_ascii = all(byte < 128 for byte in run_text.encode("ascii"))
    collect_ascii = all(byte < 128 for byte in collect_text.encode("ascii"))
    branch_order_pass = (
        run_text.index("if ($CollectOnly)") <
        run_text.index("$Ymm4 = Resolve-Ymm4Exe") <
        run_text.index("if ($PreflightOnly)") <
        run_text.index("Start-Process -FilePath $Ymm4")
    )
    running_stop_precedes_launch = (
        run_text.rindex("if (Test-Ymm4Running)", 0, run_text.index(
            "Start-Process -FilePath $Ymm4"
        ))
        < run_text.index("Start-Process -FilePath $Ymm4")
    )
    existing_stop_precedes_launch = (
        run_text.index("$ExistingTargets.Count -gt 0")
        < run_text.index("Start-Process -FilePath $Ymm4")
    )
    utf8_file_transport = all(
        token in run_text + collect_text
        for token in (
            "[IO.File]::ReadAllText",
            "[Text.Encoding]::UTF8",
            "| Out-Null",
        )
    ) and "Out-String" not in run_text + collect_text
    collector_has_no_launch = "Start-Process" not in collect_text
    preflight_parses_powershell = (
        "[scriptblock]::Create" in run_text
        and "collect_new_banknote_yymm4_import_result.ps1" in run_text
    )

    static_checks = {
        "all_generated_artifacts_byte_exact": all(artifact_matches.values()),
        "tracked_package_has_no_private_absolute_path": privacy_pass,
        "powershell_scripts_ascii_only": run_ascii and collect_ascii,
        "japanese_messages_loaded_from_utf8_json": (
            "operator_messages" in run_text
            and "Read-Utf8Json" in run_text
        ),
        "collect_only_and_preflight_return_before_launch": branch_order_pass,
        "yymm4_running_stop_precedes_launch": running_stop_precedes_launch,
        "existing_output_stop_precedes_launch": existing_stop_precedes_launch,
        "python_powershell_json_uses_utf8_files": utf8_file_transport,
        "collector_has_zero_yymm4_launch_path": collector_has_no_launch,
        "runtime_preflight_parses_both_powershell_scripts": (
            preflight_parses_powershell
        ),
        "normal_script_has_single_launch_site": (
            run_text.count("Start-Process -FilePath $Ymm4") == 1
        ),
    }
    failed.extend(name for name, passed in static_checks.items() if not passed)
    unique_failed = list(dict.fromkeys(failed))
    return {
        "schema_version": (
            "new_banknote_yymm4_import_observation.runtime_preflight.v1"
        ),
        "status": "passed" if not unique_failed else "failed",
        "checks": {
            **static_checks,
            "approved_artifact_hashes_frozen": not any(
                "AUTHORITATIVE_SCRIPT_PACKAGE_INVALID" in item
                for item in unique_failed
            ),
        },
        "artifact_matches": artifact_matches,
        "failed_checks": unique_failed,
        "manual_action_count": 4,
        "return_item_count": 3,
        "yymm4_launch_attempted": False,
        "computer_use_invoked": False,
        "render_or_media_generated": False,
    }


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left.resolve())) == os.path.normcase(
        str(right.resolve())
    )


def _parse_not_before(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("BATCH_NOT_BEFORE_UTC_INVALID") from exc
    if parsed.tzinfo is None:
        raise ValueError("BATCH_NOT_BEFORE_UTC_MUST_HAVE_OFFSET")
    return parsed.astimezone(timezone.utc)


def _timeline_from_project(project: dict[str, Any]) -> dict[str, Any]:
    timelines = project.get("Timelines")
    if not isinstance(timelines, list) or len(timelines) != 1:
        return {}
    if project.get("SelectedTimelineIndex") != 0:
        return {}
    timeline = timelines[0]
    return timeline if isinstance(timeline, dict) else {}


def _item_int(item: dict[str, Any], key: str, default: int) -> int:
    value = item.get(key)
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def collect_new_banknote_yymm4_import_result(
    *,
    pilot_dir: str | Path = DEFAULT_PILOT_DIR,
    project_path: str | Path | None = None,
    output_path: str | Path | None = None,
    not_before_utc: str,
    operator_confirmed_no_mapping_error: bool,
    yymm4_product_version: str,
    profile_observation_version: str = PROFILE_VERSION,
) -> dict[str, Any]:
    """Collect a saved local import project without launching or mutating YMM4."""
    pilot = Path(pilot_dir).resolve()
    expected_project = (
        pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_PROJECT_FILENAME
    ).resolve()
    expected_output = (
        pilot / LOCAL_OUTPUT_DIRNAME / LOCAL_RESULT_FILENAME
    ).resolve()
    project_path_value = (
        Path(project_path).resolve()
        if project_path is not None
        else expected_project
    )
    output = (
        Path(output_path).resolve()
        if output_path is not None
        else expected_output
    )
    if not _same_path(output, expected_output):
        raise ValueError("OPERATOR_RESULT_TARGET_MUST_BE_EXACT_LOCAL_PATH")
    if output.exists():
        raise ValueError("EXISTING_OPERATOR_RESULT_PRESERVED")

    threshold = _parse_not_before(not_before_utc)
    inputs = _load_contract_inputs(pilot)
    expected_rows = list(inputs["derived_rows"])
    checks: dict[str, bool] = {
        "exact_local_project_target": _same_path(
            project_path_value, expected_project
        ),
        "operator_confirmed_no_mapping_error_update_or_character_mismatch": (
            operator_confirmed_no_mapping_error is True
        ),
        "local_project_exists": project_path_value.is_file(),
        "local_project_fresh": False,
        "project_parse_pass": False,
        "one_selected_timeline": False,
        "embedded_project_target_matches": False,
        "VoiceItem_count_9": False,
        "character_counts_3_6": False,
        "exact_text_order": False,
        "exact_character_text_order": False,
        "missing_count_zero": False,
        "duplicate_count_zero": False,
        "reordered_false": False,
        "voice_frames_strictly_increasing": False,
        "voice_lengths_positive": False,
        "VoiceItem_only_timeline": False,
    }
    parse_error_code: str | None = None
    project: dict[str, Any] = {}
    timeline: dict[str, Any] = {}
    stored_voices: list[dict[str, Any]] = []
    ordered_voices: list[dict[str, Any]] = []
    actual_rows: list[tuple[str, str]] = []

    if project_path_value.is_file():
        modified = datetime.fromtimestamp(
            project_path_value.stat().st_mtime, timezone.utc
        )
        checks["local_project_fresh"] = modified >= threshold
        try:
            project = load_ymmp(project_path_value)
            checks["project_parse_pass"] = True
            timeline = _timeline_from_project(project)
            checks["one_selected_timeline"] = bool(timeline)
            embedded = str(project.get("FilePath") or "").strip()
            if embedded:
                checks["embedded_project_target_matches"] = _same_path(
                    Path(embedded), expected_project
                )
            if timeline:
                items = _get_timeline_items(project)
                stored_voices = [
                    item for item in items if _item_type(item) == "VoiceItem"
                ]
                ordered_voices = sorted(
                    stored_voices,
                    key=lambda item: (
                        _item_int(item, "Frame", -1),
                        stored_voices.index(item),
                    ),
                )
                actual_rows = [
                    (
                        str(item.get("CharacterName") or ""),
                        str(item.get("Serif") or ""),
                    )
                    for item in ordered_voices
                ]
                frames = [
                    _item_int(item, "Frame", -1)
                    for item in ordered_voices
                ]
                lengths = [
                    _item_int(item, "Length", 0)
                    for item in ordered_voices
                ]
                checks["VoiceItem_count_9"] = len(ordered_voices) == 9
                checks["character_counts_3_6"] = dict(
                    Counter(character for character, _ in actual_rows)
                ) == EXPECTED_DERIVED_COUNTS
                checks["exact_text_order"] = [
                    text for _, text in actual_rows
                ] == [text for _, text in expected_rows]
                checks["exact_character_text_order"] = (
                    actual_rows == expected_rows
                )
                checks["voice_frames_strictly_increasing"] = (
                    len(frames) == 9
                    and frames[0] >= 0
                    and all(
                        left < right
                        for left, right in zip(frames, frames[1:])
                    )
                )
                checks["voice_lengths_positive"] = (
                    len(lengths) == 9 and all(length > 0 for length in lengths)
                )
                checks["VoiceItem_only_timeline"] = (
                    len(items) == len(stored_voices)
                )
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            parse_error_code = type(exc).__name__

    expected_texts = [text for _, text in expected_rows]
    actual_texts = [text for _, text in actual_rows]
    expected_counter = Counter(expected_texts)
    actual_counter = Counter(actual_texts)
    missing_count = sum((expected_counter - actual_counter).values())
    duplicate_count = sum((actual_counter - expected_counter).values())
    reordered = (
        len(actual_texts) == len(expected_texts)
        and actual_counter == expected_counter
        and actual_texts != expected_texts
    )
    checks["missing_count_zero"] = missing_count == 0
    checks["duplicate_count_zero"] = duplicate_count == 0
    checks["reordered_false"] = reordered is False

    video_info = (
        timeline.get("VideoInfo")
        if isinstance(timeline.get("VideoInfo"), dict)
        else {}
    )
    fps_raw = video_info.get("FPS") if video_info else None
    try:
        fps = float(fps_raw) if fps_raw is not None else None
    except (TypeError, ValueError):
        fps = None
    timing_rows = [
        {
            "csv_row_id": f"csv_row_{index}",
            "cue_id": f"cue_{index:03d}",
            "frame": _item_int(item, "Frame", 0),
            "length_frames": _item_int(item, "Length", 0),
            "end_frame": (
                _item_int(item, "Frame", 0)
                + _item_int(item, "Length", 0)
            ),
        }
        for index, item in enumerate(ordered_voices, start=1)
    ]
    item_end = max(
        (row["end_frame"] for row in timing_rows),
        default=0,
    )
    timeline_frames = (
        _item_int(timeline, "Length", 0) if timeline else 0
    )
    if timeline_frames < item_end:
        timeline_frames = item_end
    duration_seconds = (
        round(timeline_frames / fps, 6)
        if fps is not None and fps > 0
        else None
    )

    failed_checks = [
        name for name, passed in checks.items() if passed is not True
    ]
    result = {
        "schema_version": (
            "new_banknote_yymm4_import_observation.operator_result.v1"
        ),
        "status": "success" if not failed_checks else "failure",
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "batch_not_before_utc": threshold.isoformat(),
        "operator_observation": {
            "no_mapping_error_update_or_character_mismatch_confirmed": (
                operator_confirmed_no_mapping_error
            ),
            "mapping_dialog_or_error_observed": (
                False if operator_confirmed_no_mapping_error else None
            ),
            "evidence_grade": "observed",
            "yymm4_product_version": yymm4_product_version,
            "profile_observation_version": profile_observation_version,
            "profile_version_match": yymm4_product_version.startswith(
                profile_observation_version
            ),
            "version_difference_policy": "warning_only",
        },
        "project_identity": {
            "expected_repo_relative_path": (
                f"{PILOT_RELATIVE.as_posix()}/{LOCAL_OUTPUT_DIRNAME}/"
                f"{LOCAL_PROJECT_FILENAME}"
            ),
            "actual_path": str(project_path_value),
            "exact_target_matches": checks["exact_local_project_target"],
            "embedded_file_path_matches": checks[
                "embedded_project_target_matches"
            ],
            "sha256": (
                _sha256(project_path_value)
                if project_path_value.is_file()
                else None
            ),
            "size_bytes": (
                project_path_value.stat().st_size
                if project_path_value.is_file()
                else 0
            ),
            "modified_at_utc": (
                datetime.fromtimestamp(
                    project_path_value.stat().st_mtime, timezone.utc
                ).isoformat()
                if project_path_value.is_file()
                else None
            ),
            "parse_error_code": parse_error_code,
        },
        "independently_verified": {
            "VoiceItem_count": len(ordered_voices),
            "expected_VoiceItem_count": 9,
            "character_counts": dict(
                Counter(character for character, _ in actual_rows)
            ),
            "expected_character_counts": EXPECTED_DERIVED_COUNTS,
            "exact_text_order": checks["exact_text_order"],
            "exact_character_text_order": checks[
                "exact_character_text_order"
            ],
            "missing_count": missing_count,
            "duplicate_count": duplicate_count,
            "reordered": reordered,
            "fps": fps_raw,
            "timeline_frames": timeline_frames,
            "duration_seconds": duration_seconds,
            "timing_source": "actual_saved_voiceitem_frames_and_fps",
            "voice_timing_summary": timing_rows,
            "ImageItem_required": False,
            "independent_TextItem_required": False,
            "render_required": False,
        },
        "checks": checks,
        "failed_checks": failed_checks,
        "evidence_boundary": {
            "actual_yymm4_import_observation": (
                operator_confirmed_no_mapping_error
            ),
            "internal_import_observation_only": True,
            "production_project": False,
            "render_performed_or_required": False,
            "rights_or_publication_approval": False,
        },
    }
    _write_json(output, result)
    return {**result, "operator_result_path": str(output)}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="New-banknote YMM4 import operator batch"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--pilot", default=str(DEFAULT_PILOT_DIR))

    preflight_parser = subparsers.add_parser("preflight")
    preflight_parser.add_argument("--pilot", default=str(DEFAULT_PILOT_DIR))
    preflight_parser.add_argument("--result-json")

    collect_parser = subparsers.add_parser("collect")
    collect_parser.add_argument("--pilot", default=str(DEFAULT_PILOT_DIR))
    collect_parser.add_argument("--project", required=True)
    collect_parser.add_argument("--output", required=True)
    collect_parser.add_argument("--not-before-utc", required=True)
    collect_parser.add_argument("--yymm4-product-version", required=True)
    collect_parser.add_argument(
        "--profile-observation-version",
        default=PROFILE_VERSION,
    )
    collect_parser.add_argument(
        "--operator-confirmed-no-mapping-error",
        action="store_true",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "build":
        result = build_new_banknote_yymm4_operator_batch(args.pilot)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if args.command == "preflight":
        result = preflight_new_banknote_yymm4_operator_batch(args.pilot)
        if args.result_json:
            _write_json(Path(args.result_json), result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "passed" else 1
    if args.command == "collect":
        result = collect_new_banknote_yymm4_import_result(
            pilot_dir=args.pilot,
            project_path=args.project,
            output_path=args.output,
            not_before_utc=args.not_before_utc,
            operator_confirmed_no_mapping_error=(
                args.operator_confirmed_no_mapping_error
            ),
            yymm4_product_version=args.yymm4_product_version,
            profile_observation_version=args.profile_observation_version,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "success" else 1
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
