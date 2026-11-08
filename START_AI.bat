@echo off
title Nexus-Jarvis AI Starter
cd /d "%~dp0"
echo ========================================================
echo   Starting Nexus-Jarvis AI Cockpit
echo ========================================================
echo.
echo Launching Cockpit on http://localhost:8501 ...
start /b cmd /c "timeout /t 1 /nobreak >nul & start http://localhost:8501"
"%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.headless true --browser.gatherUsageStats false --server.fileWatcherType none --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying fallback python...
    python -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.headless true --browser.gatherUsageStats false --server.fileWatcherType none --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false
)
pause
