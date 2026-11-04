@echo off
title Nexus-Grok Master Controller
cd /d "%~dp0"
echo Launching Master Control Panel...
"%~dp0.venv\Scripts\python.exe" "%~dp0control_panel.py"
pause
