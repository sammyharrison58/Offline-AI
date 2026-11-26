SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

PY_EXE=""
if [ -f "$SCRIPT_DIR/.venv/bin/python" ]; then
    PY_EXE="$SCRIPT_DIR/.venv/bin/python"
elif [ -f "$SCRIPT_DIR/venv/bin/python" ]; then
    PY_EXE="$SCRIPT_DIR/venv/bin/python"
elif [ -f "$SCRIPT_DIR/env/bin/python" ]; then
    PY_EXE="$SCRIPT_DIR/env/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PY_EXE="python3"
elif command -v python >/dev/null 2>&1; then
    PY_EXE="python"
else
    echo "[ERROR] No Python runtime found. Please install Python 3.9+."
    exit 1
fi

"$PY_EXE" -c "import socket; s=socket.socket(); s.settimeout(0.02); exit(s.connect_ex(('127.0.0.1', 8501)))" >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Server is already online. Opening cockpit..."
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "http://127.0.0.1:8501" &
    elif command -v open >/dev/null 2>&1; then
        open "http://127.0.0.1:8501" &
    fi
    exit 0
fi

echo "========================================================"
echo "  Starting Lyra AI Cockpit (Ultra-Fast Linux/macOS)"
echo "========================================================"

"$PY_EXE" -c "from core.hardware_adapter import HardwareAdapter; HardwareAdapter.launch_background_opener(8501)" &

"$PY_EXE" -m streamlit run "$SCRIPT_DIR/web_ui.py" --server.port 8501 --server.address 127.0.0.1 --server.headless true --browser.serverAddress 127.0.0.1 --browser.gatherUsageStats false --server.fileWatcherType none --server.runOnSave false --client.toolbarMode minimal --client.showErrorDetails false --global.developmentMode false --server.enableCORS false --server.enableXsrfProtection false
