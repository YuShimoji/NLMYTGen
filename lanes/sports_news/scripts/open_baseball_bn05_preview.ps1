param(
  [switch]$NoOpen
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")
$proofPath = Join-Path $repoRoot "samples\_probe\baseball\placement\baseball_pitch_event_p05_placement_proof.ymmp"
$pngPath = Join-Path $repoRoot "samples\_probe\baseball\static\baseball_pitch_event_p05.png"
$outDir = Join-Path $repoRoot "_tmp\baseball_bn05_preview"
$outPath = Join-Path $outDir "baseball_pitch_event_p05_placement_proof.local.ymmp"

if (-not (Test-Path -LiteralPath $proofPath)) {
  throw "BN-05 proof .ymmp not found: $proofPath"
}
if (-not (Test-Path -LiteralPath $pngPath)) {
  throw "BN-05 source PNG not found: $pngPath"
}

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$json = Get-Content -Raw -Encoding UTF8 -LiteralPath $proofPath | ConvertFrom-Json
$found = $false
foreach ($timeline in $json.Timelines) {
  foreach ($item in $timeline.Items) {
    if (($item.'$type' -like "*ImageItem*") -and ($item.Remark -eq "baseball_bn05_placement_proof segment=pitch_event_breakdown not_creative_acceptance no_render no_publish_gate")) {
      $item.FilePath = (Resolve-Path -LiteralPath $pngPath).Path
      $found = $true
    }
  }
}

if (-not $found) {
  throw "BN-05 proof ImageItem not found in: $proofPath"
}

$json.FilePath = $outPath
$json | ConvertTo-Json -Depth 100 | Set-Content -Encoding UTF8 -LiteralPath $outPath

Write-Output "BN-05 local YMM4 preview copy: $outPath"
Write-Output "Resolved PNG: $((Resolve-Path -LiteralPath $pngPath).Path)"

if (-not $NoOpen) {
  Start-Process -FilePath $outPath
}
