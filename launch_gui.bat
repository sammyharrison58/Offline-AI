@echo off
title Lyra Autonomous Offline AI Cockpit
cd /d "%~dp0"
set PY_EXE=
if exist "%~dp0.venv\Scripts\python.exe" (
    set PY_EXE="%~dp0.venv\Scripts\python.exe"
) else if exist "%~dp0venv\Scripts\python.exe" (
    set PY_EXE="%~dp0venv\Scripts\python.exe"
) else if exist "%~dp0env\Scripts\python.exe" (
    set PY_EXE="%~dp0env\Scripts\python.exe"
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PY_EXE=python
    ) else (
        where py >nul 2>&1
        if %ERRORLEVEL% EQU 0 (
            set PY_EXE=py -3
        )
    )
)
if "%PY_EXE%"=="" (
    echo [ERROR] No Python runtime found. Please install Python 3.9+ or create a virtual environment in .venv.
    pause
    exit /b 1
)
%PY_EXE% -c "import socket; s=socket.socket(); s.settimeout(0.02); exit(s.connect_ex(('127.0.0.1', 8501)))" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Server is already online. Opening cockpit instantly...
    start "" "http://127.0.0.1:8501"
) else (
    echo Starting local engine and opening cockpit...
    %PY_EXE% -c "from core.hardware_adapter import HardwareAdapter; HardwareAdapter.auto_initialize()"
    start /b "" %PY_EXE% -c "import socket,time,webbrowser; s=socket.socket(); s.settimeout(0.03); exec('for _ in range(400):\n try:\n  s.connect((\x27127.0.0.1\x27, 8501))\n  s.close()\n  webbrowser.open(\x27http://127.0.0.1:8501\x27)\n  break\n except:\n  time.sleep(0.025)')"
    %PY_EXE% -m streamlit run "%~dp0web_ui.py" --server.port 8501 --server.address 127.0.0.1 --server.headless true --browser.serverAddress 127.0.0.1 --browser.gatherUsageStats false --server.fileWatcherType none --server.runOnSave false --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false --server.enableCORS false --server.enableXsrfProtection false
)
pause
