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

# Clean up any previous installation
if (Test-Path "$INSTALL_DIR\nexus-repo") {
    Remove-Item -Recurse -Force "$INSTALL_DIR\nexus-repo" -ErrorAction SilentlyContinue
}

# Remove old installation files (keep config.env if it exists)
$configBackup = $null
if (Test-Path "$INSTALL_DIR\config.env") {
    $configBackup = Get-Content "$INSTALL_DIR\config.env" -Raw
}

# Clean install directory except config
Get-ChildItem -Path $INSTALL_DIR -Exclude "config.env" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

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
Move-Item -Force "$INSTALL_DIR\nexus-repo\*" "$INSTALL_DIR\" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$INSTALL_DIR\nexus-repo" -ErrorAction SilentlyContinue

# Restore config if it existed
if ($configBackup) {
    Set-Content -Path "$INSTALL_DIR\config.env" -Value $configBackup
}

# Create virtual environment
Write-Host ""
Write-Host "    [4/6] Creating virtual environment..." -ForegroundColor Yellow

# Kill any Python processes that might be using the venv
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*$INSTALL_DIR*" } | Stop-Process -Force -ErrorAction SilentlyContinue

# Wait a moment for processes to close
Start-Sleep -Seconds 2

# Remove old venv if it exists
if (Test-Path "$INSTALL_DIR\venv") {
    try {
        Remove-Item -Recurse -Force "$INSTALL_DIR\venv" -ErrorAction Stop
    } catch {
        Write-Host "          ⚠ Could not remove old venv, trying to continue..." -ForegroundColor Yellow
    }
}

# Create new venv
try {
    python -m venv "$INSTALL_DIR\venv" 2>&1 | Out-Null
    Write-Host "          ✓ Virtual environment created" -ForegroundColor Green
} catch {
    Write-Host "          ✗ Failed to create virtual environment" -ForegroundColor Red
    Write-Host "            Close any running Python processes and try again" -ForegroundColor DarkGray
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "    [5/6] Installing dependencies..." -ForegroundColor Yellow

# Use full paths and wait for completion
$pythonExe = "$INSTALL_DIR\venv\Scripts\python.exe"
$pipExe = "$INSTALL_DIR\venv\Scripts\pip.exe"

# Upgrade pip first
& $pythonExe -m pip install --upgrade pip --quiet 2>&1 | Out-Null

# Install requirements
& $pythonExe -m pip install -r "$INSTALL_DIR\requirements.txt" --quiet 2>&1 | Out-Null

# Install package in editable mode
& $pythonExe -m pip install -e "$INSTALL_DIR" --quiet 2>&1 | Out-Null

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
