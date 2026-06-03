@echo off
REM HU Voice AI API - Startup Script for Windows

echo.
echo ========================================
echo HU Voice AI API - Starting Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
echo Installing/updating dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your OpenRouter API key:
    echo.
    echo OPENROUTER_API_KEY=your_api_key_here
    echo.
    pause
    echo Creating .env from .env.example...
    copy .env.example .env
)

REM Start the server
echo.
echo ========================================
echo Starting HU Voice AI API Server...
echo ========================================
echo.
echo Server running at: http://localhost:5000
echo API Docs at: http://localhost:5000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
