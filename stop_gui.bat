@echo off
title Stop Nexus-226 Cockpit
echo Stopping Nexus-226 Streamlit processes...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"
echo Nexus-226 GUI has been stopped.
pause

