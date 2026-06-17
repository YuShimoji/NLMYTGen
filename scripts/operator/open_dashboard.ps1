[CmdletBinding()]
param(
    [switch]$PrintPath
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = $null

try {
    $gitRoot = (& git -C $scriptDir rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -eq 0 -and $gitRoot) {
        $repoRoot = $gitRoot.Trim()
    }
} catch {
    $repoRoot = $null
}

if (-not $repoRoot) {
    $repoRoot = (Resolve-Path -LiteralPath (Join-Path $scriptDir '..\..')).Path
}

$candidates = @(
    'docs/dashboard/index.html',
    'docs/dashboard.md'
)

$target = $null
foreach ($candidate in $candidates) {
    $path = Join-Path $repoRoot $candidate
    if (Test-Path -LiteralPath $path) {
        $target = (Resolve-Path -LiteralPath $path).Path
        break
    }
}

if (-not $target) {
    throw 'No dashboard file found. Expected docs/dashboard/index.html or docs/dashboard.md.'
}

if ($PrintPath) {
    Write-Output $target
    exit 0
}

Start-Process -FilePath $target
