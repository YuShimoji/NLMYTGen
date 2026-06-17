[CmdletBinding()]
param(
    [ValidateSet("nav", "inventory", "list", "source")]
    [string]$Format = "nav",

    [string]$OutputPath
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $scriptDir "..")).Path

$excludedParts = @(
    ".agent",
    ".claude",
    ".codex",
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "_local",
    "_tmp",
    "build",
    "dist",
    "node_modules",
    "nlmytgen.egg-info",
    "venv"
)

$categoryOrder = @(
    "Overview",
    "Runtime State",
    "Rules And Boundaries",
    "Specs",
    "Development Notes",
    "Artifacts",
    "Lanes And Side Materials",
    "Misc"
)

function Get-RelativeDocPath {
    param([string]$Path)

    $basePath = $repoRoot.TrimEnd("\", "/") + [System.IO.Path]::DirectorySeparatorChar
    $baseUri = New-Object System.Uri($basePath)
    $pathUri = New-Object System.Uri($Path)
    return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($pathUri).ToString()).Replace("\", "/")
}

function Test-ExcludedPath {
    param([string]$RelativePath)

    $parts = $RelativePath -split "[/\\]"
    foreach ($part in $parts) {
        if ($excludedParts -contains $part) {
            return $true
        }
    }
    return $false
}

function Get-FirstHeading {
    param([string]$Path)

    foreach ($line in Get-Content -LiteralPath $Path -TotalCount 80 -ErrorAction SilentlyContinue) {
        if ($line -match "^\s*#\s+(.+?)\s*$") {
            return $Matches[1].Trim()
        }
    }
    return ""
}

function Get-DocCategory {
    param(
        [string]$RelativePath,
        [string]$Heading
    )

    $p = $RelativePath.ToLowerInvariant()

    if (
        $p -match "^(index|readme|agents|claude)\.md$" -or
        $p -eq "docs/index.md" -or
        $p -eq "docs/nav.md" -or
        $p -eq "docs/markdown-inventory.md" -or
        $p -eq "docs/project-overview.md" -or
        $p -eq "docs/visual-proof-index.md" -or
        $p -eq "docs/turn-based-development-map.md"
    ) {
        return "Overview"
    }

    if ($p -match "^docs/verification/" -or $p -match "^samples/" -or $p -match "proof|report|packet|proposal|draft|sample|probe|artifact") {
        return "Artifacts"
    }

    if ($p -match "^lanes/" -or $p -match "^baseballinfographics/") {
        return "Lanes And Side Materials"
    }

    if ($p -match "runtime-state|project-context|feature_registry|user_request_ledger|user_copypaste_blocks|migration_ledger") {
        return "Runtime State"
    }

    if ($p -match "repo_local_rules|invariants|interaction_notes|automation_boundary|operator_workflow|material_sourcing_rules") {
        return "Rules And Boundaries"
    }

    if ($p -match "^docs/prompts/" -or $p -match "^docs/dev/" -or $p -match "prompt|runbook|manual-checkpoints|cli_reference") {
        return "Development Notes"
    }

    if ($p -match "^docs/adr/" -or $p -match "^docs/ai/" -or $p -match "spec|contract|schema|matrix|atlas|guide|checklist|blueprint|pipeline|workflow|surface|orchestration|reference|capability|thumbnail|motion|visual|production|scene|skit|episode|rss|baseball") {
        return "Specs"
    }

    if ($Heading -match "runtime|state|handoff") {
        return "Runtime State"
    }

    return "Misc"
}

function Get-DocViewPath {
    param([string]$RelativePath)

    if ($RelativePath -eq "README.md") {
        return "repo-root/README.md"
    }
    return $RelativePath
}

function ConvertTo-YamlSingleQuoted {
    param([string]$Value)

    return "'" + ($Value -replace "'", "''") + "'"
}

function Escape-MarkdownCell {
    param([string]$Value)

    return (($Value -replace "\|", "\|") -replace "`r?`n", " ").Trim()
}

function ConvertTo-LfText {
    param([object]$Value)

    if ($Value -is [System.Collections.IEnumerable] -and $Value -isnot [string]) {
        $items = @($Value | ForEach-Object { [string]$_ })
        while ($items.Count -gt 0 -and $items[$items.Count - 1] -eq "") {
            if ($items.Count -eq 1) {
                $items = @()
            } else {
                $items = $items[0..($items.Count - 2)]
            }
        }
        return ($items -join "`n") + "`n"
    }
    $text = [string]$Value -replace "`r?`n", "`n"
    return ($text -replace "(\n[ \t]*)+\z", "") + "`n"
}

function Write-Utf8NoBomLfFile {
    param(
        [string]$Path,
        [object]$Value
    )

    $utf8NoBom = New-Object System.Text.UTF8Encoding -ArgumentList $false
    [System.IO.File]::WriteAllText($Path, (ConvertTo-LfText -Value $Value), $utf8NoBom)
}

$docs = Get-ChildItem -LiteralPath $repoRoot -Recurse -File -Filter "*.md" |
    ForEach-Object {
        $relativePath = Get-RelativeDocPath -Path $_.FullName
        if (Test-ExcludedPath -RelativePath $relativePath) {
            return
        }

        $heading = Get-FirstHeading -Path $_.FullName
        [PSCustomObject]@{
            RelativePath = $relativePath
            ViewPath = Get-DocViewPath -RelativePath $relativePath
            Heading = $heading
            Category = Get-DocCategory -RelativePath $relativePath -Heading $heading
        }
    } |
    Sort-Object @{ Expression = { [Array]::IndexOf($categoryOrder, $_.Category) } }, RelativePath

$visualAssets = Get-ChildItem -LiteralPath (Join-Path $repoRoot "samples") -Recurse -File |
    ForEach-Object {
        $relativePath = Get-RelativeDocPath -Path $_.FullName
        if (Test-ExcludedPath -RelativePath $relativePath) {
            return
        }

        $extension = $_.Extension.ToLowerInvariant()
        $isRootSamplePng = ($relativePath -match "^samples/[^/]+\.png$")
        $isProbeVisual = ($relativePath -match "^samples/_probe/.+\.(png|html)$")
        if ($isRootSamplePng -or $isProbeVisual) {
            [PSCustomObject]@{
                RelativePath = $relativePath
            }
        }
    } |
    Sort-Object RelativePath

$lines = New-Object System.Collections.Generic.List[string]

switch ($Format) {
    "source" {
        $sourceRoot = Join-Path $repoRoot "_local\mkdocs-src"
        $resolvedLocal = Join-Path $repoRoot "_local"

        if (Test-Path -LiteralPath $sourceRoot) {
            $fullSourceRoot = (Resolve-Path -LiteralPath $sourceRoot).Path
            $fullLocalRoot = if (Test-Path -LiteralPath $resolvedLocal) {
                (Resolve-Path -LiteralPath $resolvedLocal).Path
            } else {
                $resolvedLocal
            }
            if (-not $fullSourceRoot.StartsWith($fullLocalRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
                throw "Refusing to remove path outside _local: $fullSourceRoot"
            }
            Remove-Item -LiteralPath $sourceRoot -Recurse -Force
        }

        New-Item -ItemType Directory -Force -Path $sourceRoot | Out-Null

        foreach ($doc in $docs) {
            $from = Join-Path $repoRoot ($doc.RelativePath -replace "/", [System.IO.Path]::DirectorySeparatorChar)
            $to = Join-Path $sourceRoot ($doc.ViewPath -replace "/", [System.IO.Path]::DirectorySeparatorChar)
            $toParent = Split-Path -Parent $to
            New-Item -ItemType Directory -Force -Path $toParent | Out-Null
            Copy-Item -LiteralPath $from -Destination $to -Force
        }

        foreach ($asset in $visualAssets) {
            $from = Join-Path $repoRoot ($asset.RelativePath -replace "/", [System.IO.Path]::DirectorySeparatorChar)
            $to = Join-Path $sourceRoot ($asset.RelativePath -replace "/", [System.IO.Path]::DirectorySeparatorChar)
            $toParent = Split-Path -Parent $to
            New-Item -ItemType Directory -Force -Path $toParent | Out-Null
            Copy-Item -LiteralPath $from -Destination $to -Force
        }

        $mirroredInventory = Join-Path $sourceRoot "docs\markdown-inventory.md"
        if (Test-Path -LiteralPath $mirroredInventory) {
            $inventoryText = Get-Content -Raw -LiteralPath $mirroredInventory
            $inventoryText = $inventoryText -replace "\]\(\.\./README\.md\)", "](../repo-root/README.md)"
            Write-Utf8NoBomLfFile -Path $mirroredInventory -Value $inventoryText
        }

        $lines.Add("Mirrored $($docs.Count) Markdown files and $($visualAssets.Count) visual proof assets into _local/mkdocs-src.")
        $lines.Add("Run: mkdocs serve --dev-addr 127.0.0.1:8000")
    }

    "list" {
        $lines.Add("Category`tPath`tFirst heading")
        foreach ($doc in $docs) {
            $lines.Add("$($doc.Category)`t$($doc.RelativePath)`t$($doc.Heading)")
        }
    }

    "inventory" {
        $lines.Add("# Markdown Inventory")
        $lines.Add("")
        $lines.Add('Generated from repository Markdown placement by `tools/generate-doc-nav.ps1`. This is a browsing index only; it does not summarize, translate, or replace the source documents.')
        $lines.Add("")
        $lines.Add('Excluded directories: `.git`, `node_modules`, `dist`, `build`, `.venv`, `venv`, `__pycache__`, `_tmp`, `_local`, `.agent`, `.claude`, `.codex`, `.pytest_cache`, `nlmytgen.egg-info`.')
        $lines.Add("")

        foreach ($category in $categoryOrder) {
            $categoryDocs = @($docs | Where-Object { $_.Category -eq $category })
            if ($categoryDocs.Count -eq 0) {
                continue
            }

            $lines.Add("## $category")
            $lines.Add("")
            $lines.Add("| Path | First heading |")
            $lines.Add("| --- | --- |")
            foreach ($doc in $categoryDocs) {
                $heading = Escape-MarkdownCell -Value $doc.Heading
                $path = Escape-MarkdownCell -Value $doc.RelativePath
                $lines.Add("| [$path](../$($doc.RelativePath)) | $heading |")
            }
            $lines.Add("")
        }
    }

    "nav" {
        $lines.Add("# Candidate MkDocs nav generated from Markdown placement.")
        $lines.Add("# Review before pasting into mkdocs.yml; classification is heuristic.")
        $lines.Add("nav:")

        foreach ($category in $categoryOrder) {
            $categoryDocs = @($docs | Where-Object { $_.Category -eq $category })
            if ($categoryDocs.Count -eq 0) {
                continue
            }

            $lines.Add("  - $(ConvertTo-YamlSingleQuoted -Value $category):")
            foreach ($doc in $categoryDocs) {
                $label = $doc.RelativePath
                $lines.Add("      - $(ConvertTo-YamlSingleQuoted -Value $label): $(ConvertTo-YamlSingleQuoted -Value $doc.ViewPath)")
            }
        }
    }
}

if ($OutputPath) {
    $outputFullPath = if ([System.IO.Path]::IsPathRooted($OutputPath)) {
        $OutputPath
    } else {
        Join-Path $repoRoot $OutputPath
    }
    $outputParent = Split-Path -Parent $outputFullPath
    if ($outputParent) {
        New-Item -ItemType Directory -Force -Path $outputParent | Out-Null
    }
    Write-Utf8NoBomLfFile -Path $outputFullPath -Value $lines
} else {
    $lines
}
