[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$BrowserPath,

    [Parameter(Mandatory = $false)]
    [string]$PythonPath,

    [Parameter(Mandatory = $false)]
    [string]$DiagnosticsPath,

    [Parameter(Mandatory = $false)]
    [string]$ResultPath,

    [Parameter(Mandatory = $false)]
    [string]$TargetUrl,

    [switch]$RequireMedia
)

$ErrorActionPreference = 'Stop'
$repoRoot = (& git -C $PSScriptRoot rev-parse --show-toplevel).Trim()
if (-not $repoRoot) {
    throw 'Unable to resolve repository root.'
}

if (-not $PythonPath) {
    $venvPython = Join-Path $repoRoot '.venv\Scripts\python.exe'
    $PythonPath = if (Test-Path -LiteralPath $venvPython) { $venvPython } else { 'python' }
}
if (-not $DiagnosticsPath) {
    $DiagnosticsPath = Join-Path $repoRoot 'artifacts\audio_diagnostics'
}
if (-not $ResultPath) {
    $ResultPath = Join-Path $DiagnosticsPath 'silent_media_smoke_result.json'
}

$audioHelper = Join-Path $repoRoot 'scripts\inspect_project_audio_sessions.ps1'
$previousPolicy = [Environment]::GetEnvironmentVariable('NLMYTGEN_AUDIO_POLICY', 'Process')
if ($previousPolicy -and $previousPolicy.ToLowerInvariant() -ne 'silent') {
    throw 'NLMYTGEN_AUDIO_POLICY supports only silent; no audio opt-in exists in this wrapper.'
}
[Environment]::SetEnvironmentVariable('NLMYTGEN_AUDIO_POLICY', 'silent', 'Process')
try {
    $subcommand = if ($TargetUrl) { 'inspect' } else { 'smoke' }
    $arguments = @('-m', 'src.pipeline.silent_media_runtime', $subcommand)
    $arguments += @('--diagnostics', $DiagnosticsPath, '--audio-helper', $audioHelper, '--result', $ResultPath)
    if ($TargetUrl) {
        $arguments += @('--target', $TargetUrl)
        if ($RequireMedia) {
            $arguments += '--require-media'
        }
    }
    if ($BrowserPath) {
        $arguments += @('--browser', $BrowserPath)
    }
    & $PythonPath @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Silent media inspection failed with exit code $LASTEXITCODE."
    }
} finally {
    [Environment]::SetEnvironmentVariable('NLMYTGEN_AUDIO_POLICY', $previousPolicy, 'Process')
}
