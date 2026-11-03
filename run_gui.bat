@echo off
title Nexus-226 Web Cockpit (Virtual Environment)
cd /d "%~dp0"
echo [Nexus-226] Activating virtual environment (.venv)...
call .venv\Scripts\activate.bat
echo [Nexus-226] Opening browser GUI...
start "" "http://localhost:8501"
python -m streamlit run web_ui.py --server.port 8501
pause

