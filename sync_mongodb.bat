@echo off
title Nexus-226 MongoDB Sync Engine
cd /d "%~dp0"
echo ========================================================
echo   Syncing Project Files and Knowledge Base to MongoDB
echo ========================================================
echo.
"%~dp0.venv\Scripts\python.exe" "%~dp0core\mongo_manager.py"
echo.
echo Sync completed.
pause

