@echo off
REM NEXUS Setup Script for Windows

echo.
echo 🚀 NEXUS Setup
echo ==============
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.9+
    exit /b 1
)
echo ✓ Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Activated
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
echo ✓ Dependencies installed
echo.

REM Install NEXUS
echo Installing NEXUS...
pip install -e . >nul 2>&1
echo ✓ NEXUS installed
echo.

REM Setup configuration
echo Setting up configuration...
if not exist ".env" (
    copy .env.example .env >nul
    echo ✓ Created .env file
    echo.
    echo ⚠️  IMPORTANT: Edit .env and add your API keys:
    echo    - GEMINI_API_KEYS=your_key_here
    echo    - GROK_API_KEYS=your_key_here
    echo.
) else (
    echo ✓ .env file exists
    echo.
)

REM Create directories
echo Creating directories...
if not exist ".nexus\memory" mkdir .nexus\memory
if not exist ".nexus\strategies" mkdir .nexus\strategies
if not exist ".nexus\logs" mkdir .nexus\logs
echo ✓ Directories created
echo.

REM Test installation
echo Testing installation...
python -c "from nexus.orchestrator import Orchestrator; print('OK')" >nul 2>&1
if errorlevel 1 (
    echo ❌ Installation test failed
    exit /b 1
)
echo ✓ Installation successful
echo.

REM Show next steps
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env and add your API keys
echo 2. Activate the environment: venv\Scripts\activate
echo 3. Run NEXUS: python -m nexus "your task here"
echo.
echo Documentation:
echo - Quick start: type QUICKSTART.md
echo - Architecture: type ARCHITECTURE.md
echo - Testing: type TESTING.md
echo.
echo Happy coding! 🎉
