@echo off
global_settings
title CyberNova Attendance Server (PRODUCTION)
color 0f
cls

echo ===================================================
echo   CYBERNOVA ATTENDANCE SYSTEM - PRODUCTION MODE
echo ===================================================
echo.
echo   Starting Waitress Server...
echo   Serving on: http://0.0.0.0:5001
echo.
echo   [!] Keep this window open.
echo   [!] Close to stop the server.
echo.

:: Check if waitress is installed
python -c "import waitress" 2>NUL
if %errorlevel% neq 0 (
    echo   [!] Waitress not found. Installing...
    pip install waitress
)

:: Run Server using Waitress (Production WSGI)
:: Threads=8 for concurrency (approx 150 users)
waitress-serve --listen=*:5001 --threads=8 app:app

pause
