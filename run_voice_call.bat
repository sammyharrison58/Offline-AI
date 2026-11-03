@echo off
title Nexus-226 Always-On Voice Call (Virtual Environment)
cd /d "%~dp0"
echo [Nexus-226] Activating virtual environment (.venv)...
call .venv\Scripts\activate.bat
echo [Nexus-226] Connecting Real-Time Voice Duplex Line...
python main.py --mode voice
pause
