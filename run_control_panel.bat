@echo off
title Nexus-226 Master Control Panel (Virtual Environment)
cd /d "%~dp0"
echo [Nexus-226] Activating virtual environment (.venv)...
call .venv\Scripts\activate.bat
echo [Nexus-226] Launching Master Control Panel Window...
python control_panel.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Control panel closed with exit code %ERRORLEVEL%.
    pause
)
