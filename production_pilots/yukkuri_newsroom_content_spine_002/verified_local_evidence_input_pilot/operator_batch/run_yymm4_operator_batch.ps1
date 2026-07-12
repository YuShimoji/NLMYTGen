[CmdletBinding()]
param(
    [switch]$PreflightOnly,
    [switch]$CollectOnly,
    [switch]$OperatorConfirmedClean,
    [string]$PythonExe = "",
    [string]$Ymm4Exe = "",
    [string]$NotBeforeUtc = "",
    [string]$Ymm4ProductVersion = "",
    [string]$OperatorOutputSettingNote = ""
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

if ($PreflightOnly -and $CollectOnly) {
    throw "Choose either -PreflightOnly or -CollectOnly, not both."
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

function Resolve-Ymm4Exe {
    param([string]$Requested)
    $Candidates = @()
    if ($Requested) { $Candidates += $Requested }
    $Candidates += "D:\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe"
    $Candidates += "D:\MovieCreationWorkspace\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe"
    foreach ($Candidate in $Candidates) {
        if (Test-Path -LiteralPath $Candidate -PathType Leaf) {
            return (Resolve-Path -LiteralPath $Candidate).Path
        }
    }
    throw "YMM4 executable was not found. Pass -Ymm4Exe explicitly."
}

function Read-Utf8Json {
    param([Parameter(Mandatory=$true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Expected UTF-8 JSON file was not found: $Path"
    }
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}

$PilotDir = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\..\..")).Path
$Python = Resolve-PythonExe -Requested $PythonExe -RepoRoot $RepoRoot
$DerivedCsv = Join-Path $PilotDir "derived_yymm4_import.csv"
$LocalOutput = Join-Path $PilotDir "local_outputs"
$ImportBase = Join-Path $LocalOutput "episode_002_verified_local_evidence_import_base.local.ymmp"
$Project = Join-Path $LocalOutput "episode_002_verified_local_evidence_internal_review.local.ymmp"
$Render = Join-Path $LocalOutput "episode_002_verified_local_evidence_internal_review.mp4"
$Result = Join-Path $LocalOutput "operator_result.json"
$BatchMarker = Join-Path $LocalOutput "operator_batch_started.local.txt"

$ValidationResultFile = Join-Path ([IO.Path]::GetTempPath()) ("nlmytgen-pilot-validation-" + [guid]::NewGuid().ToString("N") + ".json")
try {
    Push-Location -LiteralPath $RepoRoot
    try {
        & $Python -m src.cli.main validate-verified-local-evidence-pilot --pilot $PilotDir --format text --result-json $ValidationResultFile | Out-Null
        $ValidationExit = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    $Validation = Read-Utf8Json -Path $ValidationResultFile
    if ($ValidationExit -ne 0 -or $Validation.status -ne "passed") {
        throw ("Pilot validation failed: " + (($Validation.failed_checks -join ", ")))
    }
}
finally {
    Remove-Item -LiteralPath $ValidationResultFile -Force -ErrorAction SilentlyContinue
}

if ($CollectOnly) {
    $PreserveExistingSuccess = $false
    if (Test-Path -LiteralPath $Result -PathType Leaf) {
        $ExistingResult = Read-Utf8Json -Path $Result
        if ($ExistingResult.status -eq "success" -and @($ExistingResult.failed_checks).Count -eq 0) {
            $PreserveExistingSuccess = $true
            if (-not $NotBeforeUtc) { $NotBeforeUtc = [string]$ExistingResult.batch_not_before_utc }
            if (-not $Ymm4ProductVersion) { $Ymm4ProductVersion = [string]$ExistingResult.operator_reported.yymm4_product_version }
            if (-not $OperatorOutputSettingNote -and $ExistingResult.operator_reported.output_setting_note) {
                $OperatorOutputSettingNote = [string]$ExistingResult.operator_reported.output_setting_note
            }
            if ($ExistingResult.operator_reported.manual_batch_completed_before_collection -eq $true) {
                $OperatorConfirmedClean = $true
            }
        }
    }
    if ((-not $NotBeforeUtc -or -not $Ymm4ProductVersion) -and (Test-Path -LiteralPath $BatchMarker -PathType Leaf)) {
        $MarkerValues = @{}
        foreach ($Line in (Get-Content -LiteralPath $BatchMarker -Encoding UTF8)) {
            $Parts = $Line -split "=", 2
            if ($Parts.Count -eq 2) { $MarkerValues[$Parts[0]] = $Parts[1] }
        }
        if (-not $NotBeforeUtc) { $NotBeforeUtc = [string]$MarkerValues["batch_not_before_utc"] }
        if (-not $Ymm4ProductVersion) { $Ymm4ProductVersion = [string]$MarkerValues["yymm4_product_version"] }
    }
    if (-not $NotBeforeUtc) {
        throw "Collect-only needs the ignored batch marker, an existing operator_result.json, or explicit -NotBeforeUtc."
    }
    if (-not $Ymm4ProductVersion) {
        throw "Collect-only needs the ignored batch marker, an existing operator_result.json, or explicit -Ymm4ProductVersion."
    }
    if (-not $OperatorConfirmedClean) {
        throw "Collect-only requires -OperatorConfirmedClean when no successful existing result records that confirmation."
    }
    $CollectArgs = @{
        PythonExe = $Python
        PilotDir = $PilotDir
        ProjectPath = $Project
        RenderPath = $Render
        OutputPath = $Result
        NotBeforeUtc = $NotBeforeUtc
        Ymm4ProductVersion = $Ymm4ProductVersion
        ProfileObservationVersion = "4.53.0.9"
        OperatorConfirmedClean = $true
        OperatorOutputSettingNote = $OperatorOutputSettingNote
        PreserveExistingSuccess = $PreserveExistingSuccess
    }
    & (Join-Path $PSScriptRoot "collect_operator_result.ps1") @CollectArgs
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    return
}

$Ymm4 = Resolve-Ymm4Exe -Requested $Ymm4Exe
$Version = (Get-Item -LiteralPath $Ymm4).VersionInfo.ProductVersion
$ProfileVersionMatch = $Version -like "4.53.0.9*"
$Preflight = [ordered]@{
    status = "passed"
    pilot_validation = "passed"
    python_available = $true
    yymm4_executable_available = $true
    yymm4_product_version = $Version
    profile_observation_version = "4.53.0.9"
    profile_version_match = $ProfileVersionMatch
    version_difference_is_manual_mapping_gate = (-not $ProfileVersionMatch)
    yymm4_launch_attempted = $false
    collect_only_supported = $true
    preflight_only = [bool]$PreflightOnly
}

if ($PreflightOnly) {
    $Preflight | ConvertTo-Json -Depth 5
    return
}

if (Get-Process -Name "YukkuriMovieMaker" -ErrorAction SilentlyContinue) {
    throw "YMM4 is already running. Stop and resolve/save unrelated work before this batch; this script will not close it."
}

$ExactTargets = @(
    $ImportBase,
    $Project,
    $Render,
    $Result,
    (Join-Path $LocalOutput "static_project_readback.actual.json"),
    (Join-Path $LocalOutput "project_generation_receipt.actual.json"),
    $BatchMarker
)
$ExistingTargets = @($ExactTargets | Where-Object { Test-Path -LiteralPath $_ })
if ($ExistingTargets.Count -gt 0) {
    throw ("Exact pilot output already exists. Stop and move/archive it manually; this batch will not delete or reuse it: " + ($ExistingTargets -join ", "))
}
$BatchStartedUtc = [DateTime]::UtcNow.ToString("o")
New-Item -ItemType Directory -Path $LocalOutput -Force | Out-Null
@(
    "batch_not_before_utc=$BatchStartedUtc",
    "yymm4_product_version=$Version",
    "profile_observation_version=4.53.0.9"
) | Set-Content -LiteralPath $BatchMarker -Encoding UTF8

Write-Host "PC CONTROL: USER. Codex does not operate the GUI."
Write-Host "This is INTERNAL REVIEW / NOT FINAL / LOCAL EVIDENCE PILOT only."
Write-Host "STOP on unsaved/unrelated work, update prompts, mapping dialogs, character mismatch, parse errors, or any production/public/upload request."
Write-Host "DO NOT upload, publish, approve rights, create a production project, replace sources, or delete unrelated files."
if (-not $ProfileVersionMatch) {
    Write-Warning "Installed YMM4 $Version differs from profile observation 4.53.0.9. This is a manual mapping gate: stop on any mapping dialog, character mismatch, update requirement, or parse error."
}
Write-Host ""
Write-Host "Open/import CSV: $DerivedCsv"
Write-Host "PROJECT SAVE AS TARGET (.local.ymmp): $ImportBase"
Write-Host "Use Project Save As only for this .local.ymmp. NEVER enter the .mp4 path in Project Save As."
Write-Host "First create/confirm a NEW EMPTY project and EMPTY timeline. STOP if any existing item/project is present."
Write-Host "YMM4 click path: Tools > Script Import > select CSV > verify no mapping/error > Add to Timeline > Save As."
Start-Process -FilePath $Ymm4 | Out-Null
$Ready = Read-Host "After the exact import base is safely saved, type READY"
if ($Ready -ne "READY") {
    throw "Batch stopped before project generation. Expected READY."
}
if (-not (Test-Path -LiteralPath $ImportBase -PathType Leaf)) {
    throw "Exact import-base file was not found."
}

$GenerationResultFile = Join-Path ([IO.Path]::GetTempPath()) ("nlmytgen-project-generation-" + [guid]::NewGuid().ToString("N") + ".json")
try {
    Push-Location -LiteralPath $RepoRoot
    try {
        & $Python -m src.cli.main generate-verified-local-evidence-project --pilot $PilotDir --source-ymmp $ImportBase --output-ymmp $Project --format text --result-json $GenerationResultFile | Out-Null
        $GenerationExit = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    $Generation = Read-Utf8Json -Path $GenerationResultFile
    if ($GenerationExit -ne 0 -or $Generation.status -ne "local_internal_review_project_ready") {
        throw "Headless project generation failed."
    }
}
finally {
    Remove-Item -LiteralPath $GenerationResultFile -Force -ErrorAction SilentlyContinue
}
Write-Host ""
Write-Host "Open generated project: $Project"
Write-Host "Confirm no parse/error dialog and the three INTERNAL REVIEW / NOT FINAL / LOCAL EVIDENCE PILOT labels."
Write-Host "VIDEO OUTPUT/EXPORT TARGET (.mp4): $Render"
Write-Host "Use Video Output/Export, NOT Project Save As. If a project-save dialog is targeting .mp4, STOP."
Write-Host "Output exactly once. Record any manual format change (for example, the operator-observed MPEG selection) as an observation, not a machine-verified codec claim."
Write-Host "Close safely after render. Do not upload or publish."
$Collect = Read-Host "After render and safe close, type COLLECT"
if ($Collect -ne "COLLECT") {
    throw "Batch stopped before result collection. Expected COLLECT."
}

& (Join-Path $PSScriptRoot "collect_operator_result.ps1") -PythonExe $Python -PilotDir $PilotDir -ProjectPath $Project -RenderPath $Render -OutputPath $Result -NotBeforeUtc $BatchStartedUtc -Ymm4ProductVersion $Version -ProfileObservationVersion "4.53.0.9" -OperatorConfirmedClean -OperatorOutputSettingNote $OperatorOutputSettingNote
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
