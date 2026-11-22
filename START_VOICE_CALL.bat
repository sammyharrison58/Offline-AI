@echo off
title Lyra Real-Time Voice Call
cd /d "%~dp0"
echo ========================================================
echo   Connecting Live Phone Call Discussion with Lyra
echo ========================================================
echo.
start /b powershell -WindowStyle Hidden -Command "try { Invoke-RestMethod -Uri 'http://localhost:11434/api/generate' -Method Post -ContentType 'application/json' -Body '{\"model\":\"grok-offline:1b\",\"prompt\":\"hi\",\"stream\":false,\"keep_alive\":-1}' -TimeoutSec 15 } catch {}"
"%~dp0.venv\Scripts\python.exe" "%~dp0main.py" --mode voice
if %ERRORLEVEL% NEQ 0 (
    python "%~dp0main.py" --mode voice
)
pause
