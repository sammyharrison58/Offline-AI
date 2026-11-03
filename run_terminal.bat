@echo off
title Nexus-226 Terminal Chat (Virtual Environment)
cd /d "%~dp0"
echo [Nexus-226] Activating virtual environment (.venv)...
call .venv\Scripts\activate.bat
python main.py --mode text
pause

