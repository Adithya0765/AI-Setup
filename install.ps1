# NEXUS Installer for Windows (PowerShell)
# Usage: iex (iwr -Uri "https://raw.githubusercontent.com/YOUR_USERNAME/nexus/main/install.ps1").Content

$ErrorActionPreference = "Stop"

$REPO_URL = "https://github.com/YOUR_USERNAME/nexus"  # TODO: Update with your GitHub username
$INSTALL_DIR = "$env:USERPROFILE\.nexus"
$BIN_DIR = "$env:USERPROFILE\.local\bin"

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   NEXUS - AI Coding Assistant          ║" -ForegroundColor Cyan
Write-Host "║   Self-Evolving Intelligence           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "🔍 Checking requirements..." -ForegroundColor Cyan
try {
    $pythonCmd = Get-Command python -ErrorAction Stop
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python 3.9+ is required" -ForegroundColor Red
    Write-Host "     Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check Git
try {
    $gitCmd = Get-Command git -ErrorAction Stop
    Write-Host "  ✓ Git found" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Git is required" -ForegroundColor Red
    Write-Host "     Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Create directories
Write-Host ""
Write-Host "📦 Setting up installation..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $INSTALL_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $BIN_DIR | Out-Null
Write-Host "  ✓ Created directories" -ForegroundColor Green

# Clone repository
Write-Host ""
Write-Host "📥 Downloading NEXUS..." -ForegroundColor Cyan
if (Test-Path "$INSTALL_DIR\nexus") {
    Write-Host "  Removing old installation..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "$INSTALL_DIR\nexus"
}

Set-Location $INSTALL_DIR
git clone --depth 1 $REPO_URL nexus-repo 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Failed to download NEXUS" -ForegroundColor Red
    Write-Host "     Make sure the repository is public" -ForegroundColor Yellow
    exit 1
}
Write-Host "  ✓ Downloaded successfully" -ForegroundColor Green

# Move files
Move-Item -Force "$INSTALL_DIR\nexus-repo\*" "$INSTALL_DIR\"
Remove-Item -Recurse -Force "$INSTALL_DIR\nexus-repo"

# Create virtual environment
Write-Host ""
Write-Host "🔧 Creating virtual environment..." -ForegroundColor Cyan
python -m venv "$INSTALL_DIR\venv"
Write-Host "  ✓ Virtual environment created" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "📚 Installing dependencies..." -ForegroundColor Cyan
& "$INSTALL_DIR\venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
& "$INSTALL_DIR\venv\Scripts\pip.exe" install -r "$INSTALL_DIR\requirements.txt" --quiet
& "$INSTALL_DIR\venv\Scripts\pip.exe" install -e "$INSTALL_DIR" --quiet
Write-Host "  ✓ Dependencies installed" -ForegroundColor Green

# Create executable wrapper
Write-Host ""
Write-Host "🔗 Creating nexus command..." -ForegroundColor Cyan
$wrapperContent = @"
@echo off
"$INSTALL_DIR\venv\Scripts\python.exe" -m nexus %*
"@
Set-Content -Path "$BIN_DIR\nexus.bat" -Value $wrapperContent
Write-Host "  ✓ Command created" -ForegroundColor Green

# Add to PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$BIN_DIR*") {
    Write-Host ""
    Write-Host "⚙️  Updating PATH..." -ForegroundColor Cyan
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$BIN_DIR", "User")
    Write-Host "  ✓ PATH updated" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   ✅ Installation Complete!            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 NEXUS is ready to use!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Restart your terminal (or open a new one)" -ForegroundColor White
Write-Host "  2. Run: " -NoNewline -ForegroundColor White
Write-Host "nexus --status" -ForegroundColor Cyan
Write-Host "  3. Try: " -NoNewline -ForegroundColor White
Write-Host "nexus `"list all Python files`"" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Documentation: https://docs.nexus.ai" -ForegroundColor Gray
Write-Host "💬 Support: support@nexus.ai" -ForegroundColor Gray
Write-Host ""
