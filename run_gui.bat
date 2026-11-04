@echo off
title Nexus-Grok Web Cockpit
cd /d "%~dp0"
echo Starting Nexus-Grok Web Cockpit...
start "" "http://localhost:8501"
"%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0web_ui.py" --server.port 8501
pause
