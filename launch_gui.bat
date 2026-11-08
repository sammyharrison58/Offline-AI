@echo off
title Nexus-Jarvis Autonomous Offline AI Cockpit
cd /d "%~dp0"
netstat -ano | findstr :8501 | findstr LISTENING >nul     
if %ERRORLEVEL% EQU 0 (
    echo Server is already online. Opening browser...
    start "" "http://localhost:8501"
) else (
    echo Starting local engine and opening cockpit...
    start /b cmd /c "timeout /t 1 /nobreak >nul & start http://localhost:8501"
    "%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.headless true --browser.gatherUsageStats false --server.fileWatcherType none --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false
)
pause

