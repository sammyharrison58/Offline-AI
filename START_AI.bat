@echo off
title Lyra AI Starter
cd /d "%~dp0"
"%~dp0.venv\Scripts\python.exe" -c "import socket; s=socket.socket(); s.settimeout(0.02); exit(s.connect_ex(('127.0.0.1', 8501)))" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Server is already online. Opening cockpit instantly...
    start "" "http://127.0.0.1:8501"
    exit /b 0
)
echo ========================================================
echo   Starting Lyra AI Cockpit
echo ========================================================
echo.
echo Launching Cockpit on http://127.0.0.1:8501 ...
start /b "" "%~dp0.venv\Scripts\python.exe" -c "import socket,time,webbrowser,threading,json,urllib.request; threading.Thread(target=lambda: (urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:11434/api/generate', data=json.dumps({'model':'lyra:1b','keep_alive':-1,'options':{'num_predict':1,'num_ctx':512}}).encode('utf-8'), headers={'Content-Type':'application/json'}), timeout=120) if True else None), daemon=True).start(); s=socket.socket(); s.settimeout(0.03); exec('for _ in range(400):\n try:\n  s.connect((\x27127.0.0.1\x27, 8501))\n  s.close()\n  webbrowser.open(\x27http://127.0.0.1:8501\x27)\n  break\n except:\n  time.sleep(0.025)')"
"%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.address 127.0.0.1 --server.headless true --browser.serverAddress 127.0.0.1 --browser.gatherUsageStats false --server.fileWatcherType none --server.runOnSave false --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false --server.enableCORS false --server.enableXsrfProtection false
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying fallback python...
    start /b "" python -c "import socket,time,webbrowser; s=socket.socket(); s.settimeout(0.03); exec('for _ in range(400):\n try:\n  s.connect((\x27127.0.0.1\x27, 8501))\n  s.close()\n  webbrowser.open(\x27http://127.0.0.1:8501\x27)\n  break\n except:\n  time.sleep(0.025)')"
    python -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.address 127.0.0.1 --server.headless true --browser.serverAddress 127.0.0.1 --browser.gatherUsageStats false --server.fileWatcherType none --server.runOnSave false --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false --server.enableCORS false --server.enableXsrfProtection false
)
pause
