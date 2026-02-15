@echo off
echo Killing Python processes...
taskkill /IM python.exe /F
timeout /t 2 /nobreak >nul

echo Starting Server...
set PYTHONIOENCODING=utf-8
start /B python app.py > server.log 2>&1

timeout /t 5 /nobreak >nul

echo Running Test...
python test_import.py
