@echo off
title Lyra AI Starter
cd /d "%~dp0"
curl -s -m 1 http://localhost:8501 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Server is already online. Opening cockpit instantly...
    start "" "http://localhost:8501"
    exit /b 0
)
netstat -ano -p tcp | findstr :8501 | findstr LISTENING >nul
if %ERRORLEVEL% EQU 0 (
    echo Server is already online. Opening cockpit instantly...
    start "" "http://localhost:8501"
    exit /b 0
)
echo ========================================================
echo   Starting Lyra AI Cockpit
echo ========================================================
echo.
echo Launching Cockpit on http://localhost:8501 ...
start /b "" "%~dp0.venv\Scripts\python.exe" -c "import socket,time,webbrowser; s=socket.socket(); s.settimeout(0.1); exec('for _ in range(300):\n try:\n  s.connect((\x27127.0.0.1\x27, 8501))\n  s.close()\n  webbrowser.open(\x27http://localhost:8501\x27)\n  break\n except:\n  time.sleep(0.04)')"
"%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.address 127.0.0.1 --server.headless false --browser.serverAddress localhost --browser.gatherUsageStats false --server.fileWatcherType none --server.runOnSave false --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false --server.enableCORS false --server.enableXsrfProtection false
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying fallback python...
    start /b "" python -c "import socket,time,webbrowser; s=socket.socket(); s.settimeout(0.1); exec('for _ in range(300):\n try:\n  s.connect((\x27127.0.0.1\x27, 8501))\n  s.close()\n  webbrowser.open(\x27http://localhost:8501\x27)\n  break\n except:\n  time.sleep(0.04)')"
    python -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.address 127.0.0.1 --server.headless false --browser.serverAddress localhost --browser.gatherUsageStats false --server.fileWatcherType none --server.runOnSave false --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false --server.enableCORS false --server.enableXsrfProtection false
)
pause
