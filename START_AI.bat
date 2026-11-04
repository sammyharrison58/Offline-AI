@echo off
title Nexus-Grok AI Starter
cd /d "%~dp0"
echo ========================================================
echo   Starting Nexus-Grok AI Cockpit
echo ========================================================
echo.
echo Launching browser to http://localhost:8501 ...
start "" "http://localhost:8501"
"%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0web_ui.py" --server.port 8501
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying fallback python...
    python -m streamlit run "%~dp0web_ui.py" --server.port 8501
)
pause

 