@echo off
REM Hackathon Attendance System - Quick Start Script

echo.
echo ============================================================
echo HACKATHON ATTENDANCE SYSTEM - Quick Start
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [✓] Python detected
echo.

REM Check if venv exists
if not exist "venv" (
    echo [•] Creating virtual environment...
    python -m venv venv
    echo [✓] Virtual environment created
    echo.
)

REM Activate venv
echo [•] Activating virtual environment...
call venv\Scripts\activate.bat
echo [✓] Virtual environment activated
echo.

REM Install requirements
echo [•] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo [✓] Dependencies installed
echo.

REM Run the application
echo [•] Starting Hackathon Attendance System...
echo.
python app.py

pause
