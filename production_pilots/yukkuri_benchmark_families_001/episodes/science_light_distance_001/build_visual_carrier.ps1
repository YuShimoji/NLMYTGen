[CmdletBinding()]
param(
    [string]$InputYmmp,
    [string]$OutputYmmp
)

$ErrorActionPreference = 'Stop'
$episodeDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path (Join-Path $episodeDir '..\..\..\..')).Path
$carrierDir = Join-Path $episodeDir 'visual_carrier'
$svgDir = Join-Path $carrierDir 'svg'
$localOutputDir = Join-Path $episodeDir 'local_outputs'
$pngDir = Join-Path $localOutputDir 'visual_carrier'

if (-not $InputYmmp) {
    $InputYmmp = Join-Path $localOutputDir 'science_light_distance_001.ymmp'
}
if (-not $OutputYmmp) {
    $OutputYmmp = Join-Path $localOutputDir 'science_light_distance_001_visual_v002.ymmp'
}

$resolvedInput = (Resolve-Path $InputYmmp).Path
$resolvedOutput = [System.IO.Path]::GetFullPath($OutputYmmp)
if ($resolvedInput -eq $resolvedOutput) {
    throw 'InputYmmp and OutputYmmp must be different paths.'
}

$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if (-not (Test-Path -LiteralPath $edge)) {
    throw "Microsoft Edge headless renderer not found: $edge"
}
New-Item -ItemType Directory -Path $pngDir -Force | Out-Null
$rendererProfile = Join-Path ([System.IO.Path]::GetTempPath()) (
    'nlmytgen-science-carrier-edge-' + [System.Diagnostics.Process]::GetCurrentProcess().Id
)
New-Item -ItemType Directory -Path $rendererProfile -Force | Out-Null

$labels = [ordered]@{
    clock_ladder = '01_clock_ladder'
    moon_signal = '02_moon_signal'
    solar_system_delay = '03_solar_system_delay'
    near_star = '04_near_star'
    galaxy_history = '05_galaxy_history'
    summary = '06_summary'
}

$bgMap = [ordered]@{}
foreach ($entry in $labels.GetEnumerator()) {
    $svgPath = Join-Path $svgDir ($entry.Value + '.svg')
    $pngPath = Join-Path $pngDir ($entry.Value + '.png')
    $svgUri = ([System.Uri](Resolve-Path $svgPath).Path).AbsoluteUri
    $edgeArguments = @(
        '--headless',
        '--no-first-run',
        '--disable-gpu',
        '--hide-scrollbars',
        '--force-device-scale-factor=1',
        "--user-data-dir=$rendererProfile",
        '--window-size=1920,1080',
        "--screenshot=$pngPath",
        $svgUri
    )
    $startInfo = [System.Diagnostics.ProcessStartInfo]::new($edge)
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    foreach ($argument in $edgeArguments) {
        [void]$startInfo.ArgumentList.Add($argument)
    }
    $edgeProcess = [System.Diagnostics.Process]::Start($startInfo)
    if ($null -eq $edgeProcess) {
        throw "Failed to start SVG rasterizer: $edge"
    }
    $edgeProcess.WaitForExit()
    if ($edgeProcess.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $pngPath)) {
        throw "SVG rasterization failed: $svgPath"
    }
    $bgMap[$entry.Key] = [System.IO.Path]::GetFullPath($pngPath)
}

$bgMapPath = Join-Path $pngDir 'bg_map.local.json'
$bgMap | ConvertTo-Json | Set-Content -LiteralPath $bgMapPath -Encoding utf8
$irPath = Join-Path $carrierDir 'visual_carrier.ir.json'

Push-Location $repoRoot
try {
    & uv run --offline --no-sync python -m src.cli.main patch-ymmp $resolvedInput $irPath --bg-map $bgMapPath -o $resolvedOutput --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'patch-ymmp dry-run failed.' }
    & uv run --offline --no-sync python -m src.cli.main patch-ymmp $resolvedInput $irPath --bg-map $bgMapPath -o $resolvedOutput
    if ($LASTEXITCODE -ne 0) { throw 'patch-ymmp write failed.' }
}
finally {
    Pop-Location
}

$sourceProject = Get-Content -Raw -LiteralPath $resolvedInput | ConvertFrom-Json
$successorProject = Get-Content -Raw -LiteralPath $resolvedOutput | ConvertFrom-Json
$voiceType = 'YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker'
$imageType = 'YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker'
$sourceVoices = @($sourceProject.Timelines[0].Items | Where-Object { $_.'$type' -eq $voiceType })
$successorVoices = @($successorProject.Timelines[0].Items | Where-Object { $_.'$type' -eq $voiceType })
$sourceVoiceJson = $sourceVoices | ConvertTo-Json -Depth 100 -Compress
$successorVoiceJson = $successorVoices | ConvertTo-Json -Depth 100 -Compress
if ($sourceVoiceJson -cne $successorVoiceJson) {
    throw 'Successor voice/subtitle sequence differs from the verified source project.'
}

$plan = Get-Content -Raw -LiteralPath (Join-Path $carrierDir 'visual_carrier_plan.json') | ConvertFrom-Json
$images = @($successorProject.Timelines[0].Items | Where-Object { $_.'$type' -eq $imageType } | Sort-Object Frame)
if ($images.Count -ne $plan.scenes.Count) {
    throw "Expected $($plan.scenes.Count) background items, found $($images.Count)."
}
for ($index = 0; $index -lt $images.Count; $index++) {
    $scene = $plan.scenes[$index]
    $image = $images[$index]
    $expectedLength = $scene.end_frame - $scene.start_frame
    if ($image.Frame -ne $scene.start_frame -or $image.Length -ne $expectedLength -or $image.Layer -ne 0) {
        throw "Background item $index does not match the frame contract for $($scene.scene_id)."
    }
    if (-not (Test-Path -LiteralPath $image.FilePath)) {
        throw "Background image is missing: $($image.FilePath)"
    }
}

$summary = [ordered]@{
    input_ymmp = $resolvedInput
    output_ymmp = $resolvedOutput
    png_count = @($labels.Keys).Count
    bg_map = $bgMapPath
    network_requests = 0
    voice_or_subtitle_mutation_requested = $false
    voice_item_count = $successorVoices.Count
    voice_sequence_identical = $true
    image_item_count = $images.Count
    timeline_frames = $successorProject.Timelines[0].Length
}
$summary | ConvertTo-Json
