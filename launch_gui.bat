@echo off
title Nexus-226 Autonomous Offline AI Cockpit
cd /d "%~dp0"
echo [Nexus-226] Checking server status on port 8501...
netstat -ano | findstr :8501 | findstr LISTENING >nul
if %ERRORLEVEL% EQU 0 (
    echo [Nexus-226] Server is already online! Opening browser...
    start "" "http://localhost:8501"
) else (
    echo [Nexus-226] Starting local engine and opening cockpit...
    start "" "http://localhost:8501"
    python -m streamlit run web_ui.py --server.port 8501
)
pause

