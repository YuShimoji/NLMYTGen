[CmdletBinding()]
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
