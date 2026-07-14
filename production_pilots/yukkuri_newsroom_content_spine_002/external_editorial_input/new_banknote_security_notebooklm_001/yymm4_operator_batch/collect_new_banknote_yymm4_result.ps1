[CmdletBinding()]
param(
    [string]$PythonExe = "",
    [string]$PilotDir = "",
    [string]$ProjectPath = "",
    [string]$OutputPath = "",
    [string]$BatchStatePath = "",
    [string]$ObservationPath = "",
    [switch]$OperatorConfirmedNoMappingError,
    [string]$PronunciationNotes = ""
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
if (-not $ObservationPath) {
    $ObservationPath = Join-Path $PilotDir "local_outputs\operator_observation.local.json"
}

if (Get-Process -Name "YukkuriMovieMaker" -ErrorAction SilentlyContinue) {
    Write-ReturnFailure -ResultPath $OutputPath -ErrorText "YMM4 is still running; close it safely before collection"
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

$PreflightResultFile = Join-Path ([IO.Path]::GetTempPath()) (
    "nlmytgen-new-banknote-collect-preflight-" + [guid]::NewGuid().ToString("N") + ".json"
)
try {
    Push-Location -LiteralPath $RepoRoot
    try {
        & $PythonExe -m src.pipeline.new_banknote_yymm4_import_operator_batch preflight --pilot $PilotDir --result-json $PreflightResultFile | Out-Null
        $PreflightExit = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    $Preflight = Read-Utf8Json -Path $PreflightResultFile
    if ($PreflightExit -ne 0 -or $Preflight.status -ne "passed") {
        Write-ReturnFailure -ResultPath $OutputPath -ErrorText ("approval or lineage drift: " + ($Preflight.failed_checks -join ", "))
        exit 1
    }
}
finally {
    Remove-Item -LiteralPath $PreflightResultFile -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path -LiteralPath $ObservationPath -PathType Leaf)) {
    if (-not $OperatorConfirmedNoMappingError) {
        Write-ReturnFailure -ResultPath $OutputPath -ErrorText "collection requires mapping-dialog confirmation"
        exit 1
    }
    $ObservationValue = [ordered]@{
        schema_version = "new_banknote_yymm4_import_observation.operator_observation.local.v1"
        mapping_dialog_status = "no_error_confirmed"
        pronunciation_or_clipping_notes = $PronunciationNotes
        operator_reported_at_utc = [DateTime]::UtcNow.ToString("o")
    }
    Write-Utf8Json -Path $ObservationPath -Value $ObservationValue
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
    "--observation-json", $ObservationPath
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
    Write-Output ("3. pronunciation_notes: " + [string]$Result.operator_observation.pronunciation_or_clipping_notes)
    exit 0
}
if (@($Result.failed_checks).Count -gt 0) {
    Write-ReturnFailure -ResultPath $OutputPath -ErrorText ($Result.failed_checks -join ", ")
} else {
    Write-ReturnFailure -ResultPath $OutputPath -ErrorText "collector returned an unexpected result state"
}
exit 1
