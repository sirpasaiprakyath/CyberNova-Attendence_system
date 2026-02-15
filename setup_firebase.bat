@echo off
REM =====================================================
REM Hackathon Attendance System - Firebase Setup Script
REM =====================================================

echo.
echo ========================================
echo Firebase Configuration Setup
echo ========================================
echo.

REM Check if .env file exists
if exist .env (
    echo Found existing .env file
    set /p USE_EXISTING="Use existing configuration? (y/n): "
    if /i "%USE_EXISTING%"=="y" (
        goto setup_complete
    )
)

REM Get Firebase credentials file path
echo.
echo Enter the FULL PATH to your serviceAccountKey.json file
echo (Example: C:\Users\YourName\Downloads\serviceAccountKey.json)
set /p CREDS_PATH="Path: "

REM Validate file exists
if not exist "%CREDS_PATH%" (
    echo ERROR: File not found at "%CREDS_PATH%"
    pause
    exit /b 1
)

REM Get storage bucket name
echo.
echo Enter your Firebase Storage Bucket name
echo (Example: my-project-id.appspot.com)
set /p BUCKET_NAME="Bucket name: "

REM Create/update .env file
echo Creating .env file...
(
    echo GOOGLE_APPLICATION_CREDENTIALS=%CREDS_PATH%
    echo FIREBASE_STORAGE_BUCKET=%BUCKET_NAME%
) > .env

echo.
echo Configuration saved to .env file

:setup_complete
echo.
echo ========================================
echo Installing Python Dependencies
echo ========================================
echo.

python -m pip install -r requirements.txt

echo.
echo ========================================
echo Starting Hackathon Attendance System
echo ========================================
echo.

REM Load environment variables from .env
for /f "tokens=*" %%i in (.env) do set %%i

REM Run the application
python app.py

pause
