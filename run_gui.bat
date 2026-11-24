@echo off
title Lyra Web Cockpit
cd /d "%~dp0"
echo Starting Lyra Web Cockpit...
start /b "" "%~dp0.venv\Scripts\python.exe" -c "import socket,time,webbrowser; s=socket.socket(); s.settimeout(0.03); exec('for _ in range(400):\n try:\n  s.connect((\x27127.0.0.1\x27, 8501))\n  s.close()\n  webbrowser.open(\x27http://127.0.0.1:8501\x27)\n  break\n except:\n  time.sleep(0.025)')"
"%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.address 127.0.0.1 --server.headless true --browser.serverAddress 127.0.0.1 --browser.gatherUsageStats false --server.fileWatcherType none --server.runOnSave false --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false --server.enableCORS false --server.enableXsrfProtection false
pause
