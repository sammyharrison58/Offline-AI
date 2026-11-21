@echo off
title Lyra Always-On Voice Call (Virtual Environment)
cd /d "%~dp0"
echo [Lyra] Activating virtual environment (.venv)...
call .venv\Scripts\activate.bat
echo [Lyra] Connecting Real-Time Voice Duplex Line...
python main.py --mode voice
pause

