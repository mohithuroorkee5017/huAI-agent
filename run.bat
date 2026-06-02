@echo off
REM HUVOICE AGENT - Windows Startup Script

echo.
echo ╔════════════════════════════════════════╗
echo ║  HUVOICE AGENT - Startup              ║
echo ║  Advanced Voice-Based AI Assistant     ║
echo ╚════════════════════════════════════════╝
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [INFO] Python detected
echo.

REM Check if requirements are installed
echo [INFO] Checking dependencies...
python -m pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing dependencies...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [INFO] Dependencies are ready
echo.

REM Start the application
echo [INFO] Starting HUVOICE AGENT...
echo.
echo ╔════════════════════════════════════════╗
echo ║  HUVOICE AGENT is starting...         ║
echo ║  Web Interface: http://localhost:5000  ║
echo ║  Press Ctrl+C to stop                  ║
echo ╚════════════════════════════════════════╝
echo.

python huvoice_agent.py

pause
