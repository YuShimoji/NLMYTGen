[CmdletBinding()]
param(
    [string]$PythonExe = "",
    [string]$StatePath = "",
    [Parameter(Mandatory = $true)][string]$ObservationPath,
    [string]$OutputPath = "",
    [switch]$FixtureMode
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProbeDir = Split-Path -Parent $ScriptDir
$RepoRoot = [IO.Path]::GetFullPath((Join-Path $ProbeDir "..\..\.."))
if (-not $StatePath) { $StatePath = Join-Path $ProbeDir "local_outputs\operator_batch.local.json" }
if (-not $OutputPath) { $OutputPath = Join-Path $ProbeDir "local_outputs\operator_result.json" }

function Read-Utf8Json([string]$Path) {
    $text = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
    return $text | ConvertFrom-Json
}

function Resolve-Python([string]$Explicit) {
    if ($Explicit) {
        if (-not (Test-Path -LiteralPath $Explicit -PathType Leaf)) { throw "PYTHON_EXE_NOT_FOUND" }
        return (Resolve-Path -LiteralPath $Explicit).Path
    }
    $venv = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $venv -PathType Leaf) { return (Resolve-Path -LiteralPath $venv).Path }
    $command = Get-Command python.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($command) { return $command.Source }
    throw "PYTHON_EXE_UNRESOLVED"
}

try {
    $resolvedPython = Resolve-Python $PythonExe
    $arguments = @(
        "collect",
        "--repo-root", $RepoRoot,
        "--package", $ProbeDir,
        "--state", $StatePath,
        "--observations", $ObservationPath,
        "--output", $OutputPath
    )
    if ($FixtureMode) { $arguments += "--fixture-mode" }
    $details = & $resolvedPython -m src.pipeline.generic_static_layout_probe @arguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw ("COLLECTOR_FAILED: " + ($details -join " "))
    }
    $result = Read-Utf8Json $OutputPath
    Write-Output ("result: " + $result.status)
    Write-Output ("operator_result path: " + ([IO.Path]::GetFullPath($OutputPath)))
    exit 0
} catch {
    Write-Output "result: failure"
    Write-Output ("operator_result path: " + ([IO.Path]::GetFullPath($OutputPath)))
    Write-Output ("error: " + $_.Exception.Message)
    exit 1
}
