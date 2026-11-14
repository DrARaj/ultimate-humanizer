$ErrorActionPreference = "Stop"

$TargetDir = Join-Path $HOME ".claude\skills\ultimate-humanizer"
Write-Host "Installing ultimate-humanizer into $TargetDir..." -ForegroundColor Cyan

$ParentDir = Split-Path $TargetDir
if (-not (Test-Path $ParentDir)) {
    New-Item -ItemType Directory -Path $ParentDir -Force | Out-Null
}

if (Test-Path (Join-Path $TargetDir ".git")) {
    Write-Host "Updating existing installation..." -ForegroundColor Cyan
    git -C $TargetDir pull --quiet
} else {
    git clone --quiet https://github.com/DrARaj/ultimate-humanizer.git $TargetDir
}

Write-Host "Ultimate Humanizer successfully installed!" -ForegroundColor Green
Write-Host "Restart Claude Code to use /ultimate-humanizer" -ForegroundColor Green
