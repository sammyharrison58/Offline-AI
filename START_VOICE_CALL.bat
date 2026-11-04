@echo off
title Nexus-Grok Voice Call Loop
cd /d "%~dp0"
echo ========================================================
echo   Connecting Always-On Real-Time Voice Call
echo ========================================================
echo.
"%~dp0.venv\Scripts\python.exe" "%~dp0main.py" --mode voice
pause
