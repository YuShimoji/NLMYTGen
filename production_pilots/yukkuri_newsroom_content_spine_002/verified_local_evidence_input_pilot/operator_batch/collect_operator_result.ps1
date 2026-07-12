[CmdletBinding()]
param(
    [string]$PythonExe = "",
    [string]$PilotDir = "",
    [string]$ProjectPath = "",
    [string]$RenderPath = "",
    [string]$OutputPath = "",
    [switch]$OperatorConfirmedClean,
    [switch]$PreserveExistingSuccess,
    [string]$OperatorOutputSettingNote = "",
    [Parameter(Mandatory=$true)]
    [string]$NotBeforeUtc,
    [Parameter(Mandatory=$true)]
    [string]$Ymm4ProductVersion,
    [Parameter(Mandatory=$true)]
    [string]$ProfileObservationVersion
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
if (-not $PilotDir) {
    $PilotDir = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
}
$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\..\..")).Path
if (-not $PythonExe) {
    $PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
}
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
    throw "Python executable was not found."
}
if (-not $ProjectPath) {
    $ProjectPath = Join-Path $PilotDir "local_outputs\episode_002_verified_local_evidence_internal_review.local.ymmp"
}
if (-not $RenderPath) {
    $RenderPath = Join-Path $PilotDir "local_outputs\episode_002_verified_local_evidence_internal_review.mp4"
}
if (-not $OutputPath) {
    $OutputPath = Join-Path $PilotDir "local_outputs\operator_result.json"
}

$Arguments = @(
    "-m", "src.cli.main", "collect-verified-local-evidence-operator-result",
    "--pilot", $PilotDir,
    "--project", $ProjectPath,
    "--render", $RenderPath,
    "--output", $OutputPath,
    "--not-before-utc", $NotBeforeUtc,
    "--yymm4-product-version", $Ymm4ProductVersion,
    "--profile-observation-version", $ProfileObservationVersion,
    "--format", "text"
)
if ($OperatorConfirmedClean) { $Arguments += "--operator-confirmed-clean" }
if ($PreserveExistingSuccess) { $Arguments += "--preserve-existing-success" }
if ($OperatorOutputSettingNote) {
    $Arguments += "--operator-output-setting-note"
    $Arguments += $OperatorOutputSettingNote
}

Push-Location -LiteralPath $RepoRoot
try {
    & $PythonExe @Arguments | Out-Null
    $CollectionExit = $LASTEXITCODE
}
finally {
    Pop-Location
}
if (-not (Test-Path -LiteralPath $OutputPath -PathType Leaf)) {
    Write-Output "1. result: failure"
    Write-Output "2. operator_result.json: $OutputPath"
    Write-Output "3. error: collector did not write the expected UTF-8 JSON result"
    exit 1
}
$Result = Get-Content -LiteralPath $OutputPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($CollectionExit -eq 0 -and $Result.status -eq "success") {
    Write-Output "1. result: success"
    Write-Output "2. operator_result.json: $OutputPath"
    exit 0
}
Write-Output "1. result: failure"
Write-Output "2. operator_result.json: $OutputPath"
if ($Result.status -eq "failure" -and @($Result.failed_checks).Count -gt 0) {
    Write-Output ("3. error: " + (($Result.failed_checks -join ", ")))
} elseif ($CollectionExit -ne 0) {
    Write-Output "3. error: collector process failed; the existing result was preserved when requested"
} else {
    Write-Output "3. error: collector returned an unexpected result state"
}
exit 1
