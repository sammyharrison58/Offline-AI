@echo off
title Lyra AI Master Control Panel
cd /d "%~dp0"
echo [Lyra] Launching Master Control Panel...
python control_panel.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ======================================================
    echo An error occurred launching the control panel.
    echo Error code: %ERRORLEVEL%
    echo ======================================================
    pause
)
