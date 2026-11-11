@echo off
title Nexus-Jarvis Web Cockpit
cd /d "%~dp0"
echo Starting Nexus-Jarvis Web Cockpit...
start /b cmd /c "timeout /t 1 /nobreak >nul & start http://localhost:8501"
"%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.headless true --browser.gatherUsageStats false --server.fileWatcherType none --server.runOnSave false --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false
pause
