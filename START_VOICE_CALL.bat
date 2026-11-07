@echo off
title Nexus-Jarvis Real-Time Phone Call
cd /d "%~dp0"
echo ========================================================
echo   Connecting Live Phone Call Discussion with Nexus-Jarvis
echo ========================================================
echo.
start /b powershell -WindowStyle Hidden -Command "try { Invoke-RestMethod -Uri 'http://localhost:11434/api/generate' -Method Post -ContentType 'application/json' -Body '{\"model\":\"llama3.2:1b\",\"prompt\":\"hi\",\"stream\":false,\"keep_alive\":-1}' -TimeoutSec 15 } catch {}"
"%~dp0.venv\Scripts\python.exe" "%~dp0main.py" --mode voice
pause

