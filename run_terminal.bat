@echo off
title Lyra AI Terminal Chat
cd /d "%~dp0"

set "PY_EXE="
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PY_EXE=%~dp0.venv\Scripts\python.exe"
) else if exist "%~dp0venv\Scripts\python.exe" (
    set "PY_EXE=%~dp0venv\Scripts\python.exe"
) else if exist "%~dp0env\Scripts\python.exe" (
    set "PY_EXE=%~dp0env\Scripts\python.exe"
) else (
    where python >nul 2>&1
    if not errorlevel 1 (
        set "PY_EXE=python"
    ) else (
        where py >nul 2>&1
        if not errorlevel 1 (
            set "PY_EXE=py"
        )
    )
)

if not defined PY_EXE (
    echo [ERROR] No Python runtime found. Please install Python 3.9+ or create a virtual environment in .venv.
    pause
    exit /b 1
)

"%PY_EXE%" -c "from core.hardware_adapter import HardwareAdapter; HardwareAdapter.ensure_ollama_offline(); HardwareAdapter.auto_initialize()"
"%PY_EXE%" main.py --mode text
pause
