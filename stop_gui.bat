@echo off
title Stop Lyra Cockpit
echo Stopping Lyra Streamlit processes...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"
echo Lyra GUI has been stopped.
pause
