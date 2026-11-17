@echo off
title Nexus-Jarvis Autonomous Offline AI Cockpit
cd /d "%~dp0"
netstat -ano | findstr :8501 | findstr LISTENING >nul
if %ERRORLEVEL% EQU 0 (
    echo Server is already online. Opening cockpit instantly...
    start "" "http://localhost:8501"
) else (
    echo Starting local engine and opening cockpit...
    start /b powershell -WindowStyle Hidden -Command "$w=0; while($w -lt 30 -and !(Get-NetTCPConnection -LocalPort 8501 -State Listen -ErrorAction SilentlyContinue)){Start-Sleep -Milliseconds 100; $w++}; Start-Process 'http://localhost:8501'"
    "%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.headless true --browser.gatherUsageStats false --server.fileWatcherType none --server.runOnSave false --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false --server.enableCORS false --server.enableXsrfProtection false
)
pause

