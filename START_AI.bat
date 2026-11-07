@echo off
title Nexus-Grok AI Starter
cd /d "%~dp0"
echo ========================================================
echo   Starting Nexus-Grok AI Cockpit
echo ========================================================
echo.
start /b powershell -WindowStyle Hidden -Command "try { Invoke-RestMethod -Uri 'http://localhost:11434/api/generate' -Method Post -ContentType 'application/json' -Body '{\"model\":\"llama3.2:1b\",\"prompt\":\"hi\",\"stream\":false,\"keep_alive\":-1}' -TimeoutSec 15 } catch {}"
echo Launching browser to http://localhost:8501 ...
start "" "http://localhost:8501"
"%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.headless true --browser.gatherUsageStats false --server.fileWatcherType none --client.toolbarMode minimal
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying fallback python...
    python -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.headless true --browser.gatherUsageStats false --server.fileWatcherType none --client.toolbarMode minimal
)
pause
