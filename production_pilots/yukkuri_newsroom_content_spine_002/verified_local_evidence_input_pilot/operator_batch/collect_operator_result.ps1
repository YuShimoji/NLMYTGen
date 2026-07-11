[CmdletBinding()]
param(
    [string]$PythonExe = "",
    [string]$PilotDir = "",
    [string]$ProjectPath = "",
    [string]$RenderPath = "",
    [string]$OutputPath = "",
    [Parameter(Mandatory=$true)]
    [string]$NotBeforeUtc,
    [Parameter(Mandatory=$true)]
    [string]$Ymm4ProductVersion,
    [Parameter(Mandatory=$true)]
    [string]$ProfileObservationVersion
)

$ErrorActionPreference = "Stop"
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

$CollectionExit = 1
Push-Location -LiteralPath $RepoRoot
try {
    $ResultText = (& $PythonExe -m src.cli.main collect-verified-local-evidence-operator-result --pilot $PilotDir --project $ProjectPath --render $RenderPath --output $OutputPath --not-before-utc $NotBeforeUtc --operator-confirmed-clean --yymm4-product-version $Ymm4ProductVersion --profile-observation-version $ProfileObservationVersion --format json 2>&1 | Out-String).Trim()
    $CollectionExit = $LASTEXITCODE
}
finally {
    Pop-Location
}
if ($CollectionExit -ne 0) {
    Write-Output "1. result: failure"
    Write-Output "2. operator_result.json: $OutputPath"
    Write-Output "3. error: $ResultText"
    exit 1
}
$Result = $ResultText | ConvertFrom-Json
if ($Result.status -eq "success") {
    Write-Output "1. result: success"
    Write-Output "2. operator_result.json: $OutputPath"
    exit 0
}
Write-Output "1. result: failure"
Write-Output "2. operator_result.json: $OutputPath"
Write-Output ("3. error: " + (($Result.failed_checks -join ", ")))
exit 1
