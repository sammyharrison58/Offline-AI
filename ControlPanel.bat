@echo off
title Nexus-226 Master Control Panel
cd /d "%~dp0"
echo [Nexus-226] Launching Master Control Panel...
python control_panel.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ======================================================
    echo An error occurred launching the control panel.
    echo Error code: %ERRORLEVEL%
    echo ======================================================
    pause
)
