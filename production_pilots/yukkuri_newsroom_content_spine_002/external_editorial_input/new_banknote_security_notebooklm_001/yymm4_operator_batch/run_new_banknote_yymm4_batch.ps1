[CmdletBinding()]
param(
    [switch]$PreflightOnly,
    [switch]$CollectOnly,
    [switch]$OperatorConfirmedNoMappingError,
    [string]$PronunciationNotes = "",
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
    if ($env:NLMYTGEN_YMM4_EXE) { $Candidates += $env:NLMYTGEN_YMM4_EXE }
    $Command = @(Get-Command -Name "YukkuriMovieMaker.exe" -ErrorAction SilentlyContinue | Select-Object -First 1)[0]
    if ($Command -and $Command.Source) { $Candidates += $Command.Source }
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
$Observation = Join-Path $LocalOutput "operator_observation.local.json"

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
        PronunciationNotes = $PronunciationNotes
    }
    & (Join-Path $PSScriptRoot "collect_new_banknote_yymm4_result.ps1") @CollectArgs
    exit $LASTEXITCODE
}

$ExactTargets = @($Project, $Result, $BatchState, $Observation)
$ExistingTargets = @($ExactTargets | Where-Object { Test-Path -LiteralPath $_ })

if ($PreflightOnly) {
    if ($ExistingTargets.Count -gt 0) {
        throw ("Preflight stopped on existing operator-owned local evidence: " + ($ExistingTargets -join ", "))
    }
    foreach ($ScriptName in @(
        "run_new_banknote_yymm4_batch.ps1",
        "collect_new_banknote_yymm4_result.ps1"
    )) {
        $ScriptPath = Join-Path $PSScriptRoot $ScriptName
        $null = [scriptblock]::Create(
            [IO.File]::ReadAllText($ScriptPath, [Text.Encoding]::UTF8)
        )
    }
    Write-Output "preflight: passed"
    Write-Output "yymm4_inspected: false"
    return
}

$Ymm4 = Resolve-Ymm4Exe -Requested $Ymm4Exe
if (-not $Ymm4) {
    Write-Output "YMM4 executable was not resolved. Re-run exactly with an explicit executable:"
    Write-Output 'powershell -NoProfile -ExecutionPolicy Bypass -File .\run_new_banknote_yymm4_batch.ps1 -Ymm4Exe "<FULL_PATH_TO_YukkuriMovieMaker.exe>"'
    exit 2
}
$Version = [string](Get-Item -LiteralPath $Ymm4).VersionInfo.ProductVersion
if (-not $Version) { $Version = "unknown" }
$ProfileVersionMatch = $Version.StartsWith("4.53.0.9")

if (Test-Ymm4Running) {
    throw "YMM4 is already running. Save or resolve unrelated work first; this script will not close it."
}
if ($ExistingTargets.Count -gt 0) {
    throw ("Operator-owned local evidence already exists; this script will not overwrite or move it: " + ($ExistingTargets -join ", "))
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
    target_observation = $Observation
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
$Notes = Read-Host $Messages.pronunciation_prompt
if (Test-Ymm4Running) {
    throw "Collection stopped because YMM4 is still running. Close it safely; local evidence was preserved."
}

$ObservationValue = [ordered]@{
    schema_version = "new_banknote_yymm4_import_observation.operator_observation.local.v1"
    mapping_dialog_status = "no_error_confirmed"
    pronunciation_or_clipping_notes = $Notes
    operator_reported_at_utc = [DateTime]::UtcNow.ToString("o")
}
Write-Utf8Json -Path $Observation -Value $ObservationValue

$CollectArgs = @{
    PythonExe = $Python
    PilotDir = $PilotDir
}
& (Join-Path $PSScriptRoot "collect_new_banknote_yymm4_result.ps1") @CollectArgs
exit $LASTEXITCODE
