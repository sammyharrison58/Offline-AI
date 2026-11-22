@echo off
title Lyra Terminal Environment
cd /d "%~dp0"
echo ========================================================
echo  Lyra Virtual Environment Activated (.venv)
echo  Available Commands:
echo    python main.py --mode voice     (Always-on voice call)
echo    python main.py --mode text      (Interactive terminal)
echo    streamlit run web_ui.py         (Browser Web GUI)
echo    python control_panel.py         (Desktop Controller)
echo    python test_nexus_suite.py      (Run all unit tests)
echo ========================================================
call .venv\Scripts\activate.bat
cmd /k
