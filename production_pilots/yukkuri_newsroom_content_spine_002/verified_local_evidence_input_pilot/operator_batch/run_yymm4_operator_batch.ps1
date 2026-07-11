[CmdletBinding()]
param(
    [switch]$PreflightOnly,
    [string]$PythonExe = "",
    [string]$Ymm4Exe = ""
)

$ErrorActionPreference = "Stop"

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

$PilotDir = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\..\..")).Path
$Python = Resolve-PythonExe -Requested $PythonExe -RepoRoot $RepoRoot
$Ymm4 = Resolve-Ymm4Exe -Requested $Ymm4Exe
$DerivedCsv = Join-Path $PilotDir "derived_yymm4_import.csv"
$LocalOutput = Join-Path $PilotDir "local_outputs"
$ImportBase = Join-Path $LocalOutput "episode_002_verified_local_evidence_import_base.local.ymmp"
$Project = Join-Path $LocalOutput "episode_002_verified_local_evidence_internal_review.local.ymmp"
$Render = Join-Path $LocalOutput "episode_002_verified_local_evidence_internal_review.mp4"
$Result = Join-Path $LocalOutput "operator_result.json"

$ValidationExit = 1
Push-Location -LiteralPath $RepoRoot
try {
    $ValidationText = (& $Python -m src.cli.main validate-verified-local-evidence-pilot --pilot $PilotDir --format json 2>&1 | Out-String).Trim()
    $ValidationExit = $LASTEXITCODE
}
finally {
    Pop-Location
}
if ($ValidationExit -ne 0) {
    throw "Pilot validation failed: $ValidationText"
}
$Validation = $ValidationText | ConvertFrom-Json
if ($Validation.status -ne "passed") {
    throw "Pilot validation did not pass."
}
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
    (Join-Path $LocalOutput "project_generation_receipt.actual.json")
)
$ExistingTargets = @($ExactTargets | Where-Object { Test-Path -LiteralPath $_ })
if ($ExistingTargets.Count -gt 0) {
    throw ("Exact pilot output already exists. Stop and move/archive it manually; this batch will not delete or reuse it: " + ($ExistingTargets -join ", "))
}
$BatchStartedUtc = [DateTime]::UtcNow.ToString("o")

Write-Host "PC CONTROL: USER. Codex does not operate the GUI."
Write-Host "This is INTERNAL REVIEW / NOT FINAL / LOCAL EVIDENCE PILOT only."
Write-Host "STOP on unsaved/unrelated work, update prompts, mapping dialogs, character mismatch, parse errors, or any production/public/upload request."
Write-Host "DO NOT upload, publish, approve rights, create a production project, replace sources, or delete unrelated files."
if (-not $ProfileVersionMatch) {
    Write-Warning "Installed YMM4 $Version differs from profile observation 4.53.0.9. This is a manual mapping gate: stop on any mapping dialog, character mismatch, update requirement, or parse error."
}
Write-Host ""
Write-Host "Open/import CSV: $DerivedCsv"
Write-Host "Save clean import base exactly as: $ImportBase"
Write-Host "First create/confirm a NEW EMPTY project and EMPTY timeline. STOP if any existing item/project is present."
Write-Host "YMM4 click path: Tools > Script Import > select CSV > verify no mapping/error > Add to Timeline > Save As."
New-Item -ItemType Directory -Path $LocalOutput -Force | Out-Null
Start-Process -FilePath $Ymm4 | Out-Null
$Ready = Read-Host "After the exact import base is safely saved, type READY"
if ($Ready -ne "READY") {
    throw "Batch stopped before project generation. Expected READY."
}
if (-not (Test-Path -LiteralPath $ImportBase -PathType Leaf)) {
    throw "Exact import-base file was not found."
}

$GenerationExit = 1
Push-Location -LiteralPath $RepoRoot
try {
    $GenerationText = (& $Python -m src.cli.main generate-verified-local-evidence-project --pilot $PilotDir --source-ymmp $ImportBase --output-ymmp $Project --format json 2>&1 | Out-String).Trim()
    $GenerationExit = $LASTEXITCODE
}
finally {
    Pop-Location
}
if ($GenerationExit -ne 0) {
    throw "Headless project generation failed: $GenerationText"
}
Write-Host ""
Write-Host "Open generated project: $Project"
Write-Host "Confirm no parse/error dialog and the three INTERNAL REVIEW / NOT FINAL / LOCAL EVIDENCE PILOT labels."
Write-Host "Render exactly once to: $Render"
Write-Host "Close safely after render. Do not upload or publish."
$Collect = Read-Host "After render and safe close, type COLLECT"
if ($Collect -ne "COLLECT") {
    throw "Batch stopped before result collection. Expected COLLECT."
}

& (Join-Path $PSScriptRoot "collect_operator_result.ps1") -PythonExe $Python -PilotDir $PilotDir -ProjectPath $Project -RenderPath $Render -OutputPath $Result -NotBeforeUtc $BatchStartedUtc -Ymm4ProductVersion $Version -ProfileObservationVersion "4.53.0.9"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
