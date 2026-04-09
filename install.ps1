# NEXUS Installer for Windows (PowerShell)
# Usage: iex (iwr -Uri "https://raw.githubusercontent.com/Adithya0765/AI-Setup/main/install.ps1" -UseBasicParsing).Content

$ErrorActionPreference = "Stop"

$REPO_URL = "https://github.com/Adithya0765/AI-Setup"
$INSTALL_DIR = "$env:USERPROFILE\.nexus"
$BIN_DIR = "$env:USERPROFILE\.local\bin"

# Cool ASCII art
$logo = @"

    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

"@

Write-Host $logo -ForegroundColor Cyan
Write-Host "    Self-Evolving AI Coding Intelligence" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "    Installing NEXUS v0.1.0..." -ForegroundColor White
Write-Host ""

# Check Python
Write-Host "    [1/6] Checking requirements..." -ForegroundColor Yellow
try {
    $pythonCmd = Get-Command python -ErrorAction Stop
    $pythonVersion = python --version 2>&1
    Write-Host "          ✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "          ✗ Python 3.9+ is required" -ForegroundColor Red
    Write-Host "            Download from: https://www.python.org/downloads/" -ForegroundColor DarkGray
    exit 1
}

# Check Git
try {
    $gitCmd = Get-Command git -ErrorAction Stop
    Write-Host "          ✓ Git found" -ForegroundColor Green
} catch {
    Write-Host "          ✗ Git is required" -ForegroundColor Red
    Write-Host "            Download from: https://git-scm.com/download/win" -ForegroundColor DarkGray
    exit 1
}

# Create directories
Write-Host ""
Write-Host "    [2/6] Setting up directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $INSTALL_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $BIN_DIR | Out-Null
Write-Host "          ✓ Created installation directories" -ForegroundColor Green

# Clone repository
Write-Host ""
Write-Host "    [3/6] Downloading NEXUS from GitHub..." -ForegroundColor Yellow

# Clean up any previous installation attempts
if (Test-Path "$INSTALL_DIR\nexus-repo") {
    Remove-Item -Recurse -Force "$INSTALL_DIR\nexus-repo" -ErrorAction SilentlyContinue
}

Set-Location $INSTALL_DIR

# Use Start-Process to avoid stderr issues
$process = Start-Process -FilePath "git" -ArgumentList "clone","--quiet","--depth","1",$REPO_URL,"nexus-repo" -Wait -PassThru -NoNewWindow
if ($process.ExitCode -ne 0) {
    Write-Host "          ✗ Failed to download NEXUS" -ForegroundColor Red
    Write-Host "            Make sure the repository is public" -ForegroundColor DarkGray
    exit 1
}
Write-Host "          ✓ Downloaded successfully" -ForegroundColor Green

# Move files
Move-Item -Force "$INSTALL_DIR\nexus-repo\*" "$INSTALL_DIR\"
Remove-Item -Recurse -Force "$INSTALL_DIR\nexus-repo"

# Create virtual environment
Write-Host ""
Write-Host "    [4/6] Creating virtual environment..." -ForegroundColor Yellow
python -m venv "$INSTALL_DIR\venv"
Write-Host "          ✓ Virtual environment created" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "    [5/6] Installing dependencies..." -ForegroundColor Yellow
& "$INSTALL_DIR\venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
& "$INSTALL_DIR\venv\Scripts\pip.exe" install -r "$INSTALL_DIR\requirements.txt" --quiet
& "$INSTALL_DIR\venv\Scripts\pip.exe" install -e "$INSTALL_DIR" --quiet
Write-Host "          ✓ Dependencies installed" -ForegroundColor Green

# Create executable wrapper
Write-Host ""
Write-Host "    [6/6] Creating nexus command..." -ForegroundColor Yellow
$wrapperContent = @"
@echo off
"$INSTALL_DIR\venv\Scripts\python.exe" -m nexus %*
"@
Set-Content -Path "$BIN_DIR\nexus.bat" -Value $wrapperContent
Write-Host "          ✓ Command created" -ForegroundColor Green

# Add to PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$BIN_DIR*") {
    Write-Host ""
    Write-Host "    [*] Updating PATH..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$BIN_DIR", "User")
    Write-Host "          ✓ PATH updated" -ForegroundColor Green
}

Write-Host ""
Write-Host "    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""
Write-Host "    ✓ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "    Next steps:" -ForegroundColor White
Write-Host "      1. Restart your terminal" -ForegroundColor DarkGray
Write-Host "      2. Run: " -NoNewline -ForegroundColor DarkGray
Write-Host "nexus" -ForegroundColor Cyan
Write-Host "      3. Start coding with AI!" -ForegroundColor DarkGray
Write-Host ""
Write-Host "    Documentation: " -NoNewline -ForegroundColor DarkGray
Write-Host "https://github.com/Adithya0765/AI-Setup" -ForegroundColor Blue
Write-Host ""
