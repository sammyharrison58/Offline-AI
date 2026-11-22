@echo off
title Lyra AI Terminal Chat (Virtual Environment)
cd /d "%~dp0"
echo [Lyra] Activating virtual environment (.venv)...
call .venv\Scripts\activate.bat
python main.py --mode text
pause
