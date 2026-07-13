[CmdletBinding()]
param(
    [switch]$PreflightOnly,
    [switch]$CollectOnly,
    [string]$PythonExe = "",
    [string]$Ymm4Exe = "",
    [string]$ObservationFixturePath = "",
    [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProbeDir = Split-Path -Parent $ScriptDir
$RepoRoot = [IO.Path]::GetFullPath((Join-Path $ProbeDir "..\..\.."))
$ProjectPath = Join-Path $ProbeDir "local_outputs\generic_static_layout_probe.local.ymmp"
$StatePath = Join-Path $ProbeDir "local_outputs\operator_batch.local.json"
$ObservationsPath = Join-Path $ProbeDir "local_outputs\operator_observations.local.json"
$ResultPath = Join-Path $ProbeDir "local_outputs\operator_result.json"
$ContractPath = Join-Path $ProbeDir "expected_observation_contract.json"
$FixturePath = Join-Path $ProbeDir "static_layout_probe_fixture.json"
$CollectorPath = Join-Path $ScriptDir "collect_generic_static_layout_probe.ps1"

function Read-Utf8Json([string]$Path) {
    $text = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
    return $text | ConvertFrom-Json
}

function Write-Utf8Json([string]$Path, [object]$Value) {
    $parent = Split-Path -Parent $Path
    [IO.Directory]::CreateDirectory($parent) | Out-Null
    $json = $Value | ConvertTo-Json -Depth 12
    [IO.File]::WriteAllText($Path, $json + [Environment]::NewLine, [Text.UTF8Encoding]::new($false))
}

function Resolve-Python([string]$Explicit) {
    if ($Explicit) {
        if (-not (Test-Path -LiteralPath $Explicit -PathType Leaf)) {
            throw "PYTHON_EXE_NOT_FOUND"
        }
        return (Resolve-Path -LiteralPath $Explicit).Path
    }
    $venv = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $venv -PathType Leaf) {
        return (Resolve-Path -LiteralPath $venv).Path
    }
    $command = Get-Command python.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($command) { return $command.Source }
    throw "PYTHON_EXE_UNRESOLVED"
}

function Invoke-ProbePython([string]$Python, [string[]]$Arguments) {
    $output = & $Python -m src.pipeline.generic_static_layout_probe @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw ("PROBE_COMMAND_FAILED: " + ($output -join " "))
    }
}

function Resolve-Ymm4Exe([string]$Explicit) {
    $candidates = New-Object System.Collections.Generic.List[string]
    if ($Explicit) { $candidates.Add($Explicit) }
    if ($env:YMM4_EXE) { $candidates.Add($env:YMM4_EXE) }
    $command = Get-Command YukkuriMovieMaker.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($command) { $candidates.Add($command.Source) }
    try {
        $appPath = (Get-ItemProperty "Registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\App Paths\YukkuriMovieMaker.exe" -ErrorAction Stop).'(default)'
        if ($appPath) { $candidates.Add($appPath) }
    } catch {}
    if ($env:LOCALAPPDATA) {
        $candidates.Add((Join-Path $env:LOCALAPPDATA "YukkuriMovieMaker\YukkuriMovieMaker.exe"))
    }
    foreach ($candidate in $candidates) {
        if ($candidate -and (Test-Path -LiteralPath $candidate -PathType Leaf)) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }
    throw "YMM4_EXE_UNRESOLVED: rerun with -Ymm4Exe <absolute-path>"
}

try {
    if ($PreflightOnly -and $CollectOnly) {
        throw "SAFE_MODE_CONFLICT"
    }
    $ResolvedPython = Resolve-Python $PythonExe

    if ($CollectOnly) {
        $fixture = if ($ObservationFixturePath) { $ObservationFixturePath } else { $FixturePath }
        $output = if ($OutputPath) { $OutputPath } else { Join-Path $ProbeDir "local_outputs\archive\collect_only_fixture_result.json" }
        & $CollectorPath -PythonExe $ResolvedPython -StatePath $StatePath -ObservationPath $fixture -OutputPath $output -FixtureMode
        exit $LASTEXITCODE
    }

    if ($PreflightOnly) {
        Invoke-ProbePython $ResolvedPython @("preflight", "--repo-root", $RepoRoot, "--package", $ProbeDir)
        Write-Output "result: preflight_pass"
        Write-Output "operator_result path: not_created"
        exit 0
    }

    $ResolvedYmm4 = Resolve-Ymm4Exe $Ymm4Exe
    if (-not (Test-Path -LiteralPath $ProjectPath -PathType Leaf)) {
        throw "PREPARED_PROJECT_MISSING"
    }
    if (Test-Path -LiteralPath $StatePath -PathType Leaf) {
        throw "BATCH_STATE_ALREADY_EXISTS_ARCHIVE_FIRST"
    }
    if (Test-Path -LiteralPath $ResultPath -PathType Leaf) {
        throw "OPERATOR_RESULT_ALREADY_EXISTS_ARCHIVE_FIRST"
    }

    Invoke-ProbePython $ResolvedPython @("batch-start", "--repo-root", $RepoRoot, "--package", $ProbeDir, "--state", $StatePath)
    $quotedProjectPath = '"' + $ProjectPath + '"'
    $process = Start-Process -FilePath $ResolvedYmm4 -ArgumentList @($quotedProjectPath) -PassThru -Wait
    if ($process.ExitCode -ne 0) {
        throw ("YMM4_EXITED_WITH_CODE_" + $process.ExitCode)
    }

    $contract = Read-Utf8Json $ContractPath
    if ($contract.question_count -ne 3 -or $contract.questions.Count -ne 3) {
        throw "OBSERVATION_CONTRACT_COUNT_INVALID"
    }
    $observations = [ordered]@{}
    foreach ($question in $contract.questions) {
        do {
            $answer = (Read-Host ($question.question + " [pass/fail/uncertain]")).Trim().ToLowerInvariant()
        } until ($answer -in @("pass", "fail", "uncertain"))
        $observations[$question.id] = $answer
    }
    Write-Utf8Json $ObservationsPath ([ordered]@{
        schema_version = 1
        probe_id = "generic_static_image_text_subtitle_safe_area_v1"
        observations = $observations
    })

    & $CollectorPath -PythonExe $ResolvedPython -StatePath $StatePath -ObservationPath $ObservationsPath -OutputPath $ResultPath
    exit $LASTEXITCODE
} catch {
    $reportedPath = if ($OutputPath) { $OutputPath } else { $ResultPath }
    Write-Output "result: failure"
    Write-Output ("operator_result path: " + $reportedPath)
    Write-Output ("error: " + $_.Exception.Message)
    exit 1
}
