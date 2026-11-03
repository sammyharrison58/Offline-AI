@echo off
title Nexus-226 Autonomous Offline AI Cockpit
cd /d "%~dp0"
echo Starting Nexus-226 Streamlit Cockpit...
start "" "http://localhost:8501"
python -m streamlit run web_ui.py --server.port 8501
pause

