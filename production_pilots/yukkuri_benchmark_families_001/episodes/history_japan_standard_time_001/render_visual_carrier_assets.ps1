[CmdletBinding()]
param(
    [string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'
$episodeDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$carrierDir = Join-Path $episodeDir 'visual_carrier'
$planPath = Join-Path $carrierDir 'visual_carrier_plan.json'
$plan = Get-Content -Raw -LiteralPath $planPath | ConvertFrom-Json
$localOutputDir = Join-Path $episodeDir 'local_outputs'

if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $localOutputDir 'visual_carrier_raster_v001'
}
$resolvedOutput = [System.IO.Path]::GetFullPath($OutputDirectory)
$resolvedLocalRoot = [System.IO.Path]::GetFullPath($localOutputDir) + [System.IO.Path]::DirectorySeparatorChar
if (-not $resolvedOutput.StartsWith($resolvedLocalRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "OutputDirectory must remain inside the episode local_outputs directory: $resolvedOutput"
}
if (Test-Path -LiteralPath $resolvedOutput) {
    throw "Refusing to overwrite an existing output directory: $resolvedOutput"
}

$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if (-not (Test-Path -LiteralPath $edge)) {
    throw "Microsoft Edge headless renderer not found: $edge"
}

$pngDir = Join-Path $resolvedOutput 'png'
$profileDir = Join-Path $resolvedOutput 'edge-profile'
New-Item -ItemType Directory -Path $pngDir -Force | Out-Null
New-Item -ItemType Directory -Path $profileDir -Force | Out-Null

$assets = @()
foreach ($scene in $plan.scenes) {
    $svgPath = Join-Path $carrierDir $scene.asset
    if (-not (Test-Path -LiteralPath $svgPath)) {
        throw "Visual carrier SVG is missing: $svgPath"
    }
    $pngName = [System.IO.Path]::GetFileNameWithoutExtension($svgPath) + '.png'
    $pngPath = Join-Path $pngDir $pngName
    $svgUri = ([System.Uri](Resolve-Path $svgPath).Path).AbsoluteUri
    $arguments = @(
        '--headless',
        '--no-first-run',
        '--disable-gpu',
        '--hide-scrollbars',
        '--force-device-scale-factor=1',
        "--user-data-dir=$profileDir",
        '--window-size=1920,1080',
        "--screenshot=$pngPath",
        $svgUri
    )
    $startInfo = [System.Diagnostics.ProcessStartInfo]::new($edge)
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    foreach ($argument in $arguments) {
        [void]$startInfo.ArgumentList.Add($argument)
    }
    $process = [System.Diagnostics.Process]::Start($startInfo)
    if ($null -eq $process) {
        throw "Failed to start SVG rasterizer: $edge"
    }
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()
    if ($process.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $pngPath)) {
        throw "SVG rasterization failed: exit=$($process.ExitCode); svg=$svgPath; stdout=$stdout; stderr=$stderr"
    }
    $item = Get-Item -LiteralPath $pngPath
    $assets += [ordered]@{
        scene_id = $scene.scene_id
        svg = $scene.asset
        png = [System.IO.Path]::GetRelativePath($episodeDir, $pngPath)
        png_bytes = $item.Length
        png_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $pngPath).Hash.ToLowerInvariant()
    }
}

$summary = [ordered]@{
    schema_version = 'nlmytgen.chronological_history_visual_carrier_local_render.v1'
    artifact_id = $plan.artifact_id
    renderer = 'Microsoft Edge headless SVG rasterization'
    renderer_version = (Get-Item -LiteralPath $edge).VersionInfo.FileVersion
    canvas = $plan.safe_area.canvas
    output_directory = [System.IO.Path]::GetRelativePath($episodeDir, $resolvedOutput)
    asset_count = $assets.Count
    network_requests = 0
    yymm4_control_attempted = $false
    assets = $assets
}
$receiptPath = Join-Path $resolvedOutput 'asset_render_receipt.local.json'
$summary | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $receiptPath -Encoding utf8
$summary | ConvertTo-Json -Depth 8
