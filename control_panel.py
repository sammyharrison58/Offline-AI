"""
Nexus-226 Desktop Master Control Panel.
Native lightweight desktop GUI with Start/Stop controls for all autonomous offline subsystems.
"""
import os
import sys
import time
import subprocess
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

root_dir = os.path.dirname(os.path.abspath(__file__))

class NexusControlPanelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Nexus-226: Master Controller")
        self.root.geometry("680x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#0F172A")

        self.server_process = None
        self.is_running = False

        self._build_ui()
        self._check_initial_status()

    def _build_ui(self):
        # Header Frame
        header = tk.Frame(self.root, bg="#1E293B", padx=20, pady=15)
        header.pack(fill="x")

        lbl_title = tk.Label(
            header,
            text="⚡ NEXUS-226 AUTONOMOUS AI",
            font=("Segoe UI", 16, "bold"),
            fg="#818CF8",
            bg="#1E293B"
        )
        lbl_title.pack(anchor="w")

        lbl_sub = tk.Label(
            header,
            text="Offline 226 AI Engine | Machine Power & OS Control | Blockchain Ledger",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#1E293B"
        )
        lbl_sub.pack(anchor="w")

        # Status Card
        status_card = tk.Frame(self.root, bg="#1E293B", padx=20, pady=12)
        status_card.pack(fill="x", padx=20, pady=12)

        lbl_status_title = tk.Label(
            status_card,
            text="SYSTEM STATUS:",
            font=("Segoe UI", 10, "bold"),
            fg="#94A3B8",
            bg="#1E293B"
        )
        lbl_status_title.pack(side="left")

        self.lbl_status = tk.Label(
            status_card,
            text="● OFFLINE / STOPPED",
            font=("Segoe UI", 11, "bold"),
            fg="#F43F5E",
            bg="#1E293B"
        )
        self.lbl_status.pack(side="left", padx=10)

        # Primary Control Buttons (Start / Stop)
        btn_frame = tk.Frame(self.root, bg="#0F172A")
        btn_frame.pack(fill="x", padx=20, pady=5)

        self.btn_start = tk.Button(
            btn_frame,
            text="▶  START SYSTEM",
            font=("Segoe UI", 12, "bold"),
            bg="#10B981",
            fg="#FFFFFF",
            activebackground="#059669",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            height=2,
            command=self.start_system
        )
        self.btn_start.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.btn_stop = tk.Button(
            btn_frame,
            text="⏹  STOP SYSTEM",
            font=("Segoe UI", 12, "bold"),
            bg="#EF4444",
            fg="#FFFFFF",
            activebackground="#DC2626",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            height=2,
            command=self.stop_system
        )
        self.btn_stop.pack(side="right", expand=True, fill="x", padx=(10, 0))

        # Secondary Action Bar
        action_frame = tk.Frame(self.root, bg="#0F172A")
        action_frame.pack(fill="x", padx=20, pady=8)

        btn_browser = tk.Button(
            action_frame,
            text="🌐 Open Browser GUI",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg="#E2E8F0",
            relief="flat",
            cursor="hand2",
            command=self.open_browser
        )
        btn_browser.pack(side="left", expand=True, fill="x", padx=2)

        btn_voice = tk.Button(
            action_frame,
            text="🎙️ Always-On Voice Call",
            font=("Segoe UI", 9, "bold"),
            bg="#4F46E5",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.start_voice_call
        )
        btn_voice.pack(side="left", expand=True, fill="x", padx=2)

        btn_telemetry = tk.Button(
            action_frame,
            text="📊 Check Telemetry",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg="#E2E8F0",
            relief="flat",
            cursor="hand2",
            command=self.check_telemetry
        )
        btn_telemetry.pack(side="left", expand=True, fill="x", padx=2)

        # Activity Log Console
        lbl_console = tk.Label(
            self.root,
            text="Activity & Event Log:",
            font=("Segoe UI", 9, "bold"),
            fg="#94A3B8",
            bg="#0F172A"
        )
        lbl_console.pack(anchor="w", padx=20, pady=(8, 2))

        self.log_area = scrolledtext.ScrolledText(
            self.root,
            height=12,
            font=("Consolas", 9),
            bg="#020617",
            fg="#38BDF8",
            insertbackground="#38BDF8",
            relief="flat",
            padx=10,
            pady=10
        )
        self.log_area.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        self.log_message("Nexus-226 Master Control Panel initialized.")

    def log_message(self, msg: str):
        ts = time.strftime("%H:%M:%S")
        self.log_area.insert("end", f"[{ts}] {msg}\n")
        self.log_area.see("end")

    def _check_initial_status(self):
        cmd = 'powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue"'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if "Listen" in res.stdout or "Established" in res.stdout:
            self.is_running = True
            self.lbl_status.config(text="● ONLINE / RUNNING (Port 8501)", fg="#10B981")
            self.log_message("Detected existing server running on port 8501.")
        else:
            self.is_running = False
            self.lbl_status.config(text="● OFFLINE / STOPPED", fg="#F43F5E")

    def start_system(self):
        if self.is_running:
            self.log_message("System is already running on port 8501.")
            self.open_browser()
            return

        self.log_message("Initiating Nexus-226 Streamlit engine...")
        self.lbl_status.config(text="● STARTING...", fg="#FBBF24")
        self.root.update()

        def _runner():
            script_path = os.path.join(root_dir, "web_ui.py")
            cmd = [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                script_path,
                "--server.port",
                "8501",
                "--server.headless",
                "true"
            ]
            self.server_process = subprocess.Popen(
                cmd,
                cwd=root_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )

            # Wait briefly for port to bind
            time.sleep(2)
            self.is_running = True
            self.lbl_status.config(text="● ONLINE / RUNNING (Port 8501)", fg="#10B981")
            self.log_message("Nexus-226 Online: Web Cockpit accessible at http://localhost:8501")
            webbrowser.open("http://localhost:8501")

        threading.Thread(target=_runner, daemon=True).start()

    def stop_system(self):
        self.log_message("Stopping Nexus-226 processes...")
        self.lbl_status.config(text="● STOPPING...", fg="#FBBF24")
        self.root.update()

        # Kill by port 8501 cleanly
        kill_cmd = (
            'powershell -NoProfile -Command "'
            'Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue | '
            'ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"'
        )
        subprocess.run(kill_cmd, shell=True)

        if self.server_process:
            try:
                self.server_process.terminate()
            except Exception:
                pass
            self.server_process = None

        time.sleep(1)
        self.is_running = False
        self.lbl_status.config(text="● OFFLINE / STOPPED", fg="#F43F5E")
        self.log_message("Nexus-226 stopped. All connections closed.")

    def open_browser(self):
        if not self.is_running:
            self.log_message("Warning: System is offline. Click 'START SYSTEM' first.")
        webbrowser.open("http://localhost:8501")

    def start_voice_call(self):
        self.log_message("Launching Always-On Voice Call Console in dedicated window...")
        call_cmd = f'start cmd /k "{sys.executable} main.py --mode voice"'
        subprocess.run(call_cmd, shell=True, cwd=root_dir)

    def check_telemetry(self):
        from core.system_controller import SystemController
        sc = SystemController()
        t = sc.get_telemetry()
        self.log_message(f"Telemetry: CPU={t['cpu_usage_percent']}% | RAM Free={t['ram_available_gb']}GB/{t['ram_total_gb']}GB ({t['ram_used_percent']}%) | Battery={t['battery']['percent']}%")

def main():
    root = tk.Tk()
    app = NexusControlPanelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

