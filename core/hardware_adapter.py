import os
import sys
import platform
import psutil
import json
import subprocess
import shutil
from typing import Dict, Any, Optional, List

class HardwareAdapter:

    _cached_profile: Optional[Dict[str, Any]] = None

    @classmethod
    def probe_hardware(cls, workspace_root: Optional[str] = None) -> Dict[str, Any]:
        ws = workspace_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logical_cores = os.cpu_count() or 2
        physical_cores = psutil.cpu_count(logical=False) or logical_cores

        if physical_cores >= 8:
            optimal_threads = physical_cores - 2
        elif physical_cores >= 4:
            optimal_threads = physical_cores
        elif physical_cores >= 2:
            optimal_threads = min(logical_cores, physical_cores + 1)
        else:
            optimal_threads = 1

        mem = psutil.virtual_memory()
        total_ram_gb = round(mem.total / (1024 ** 3), 2)
        avail_ram_gb = round(mem.available / (1024 ** 3), 2)

        if total_ram_gb < 6.0:
            ram_tier = "ultra_low"
            rec_ctx = 384
            rec_predict_general = 140
            rec_predict_code = 220
        elif total_ram_gb < 12.0:
            ram_tier = "standard"
            rec_ctx = 512
            rec_predict_general = 180
            rec_predict_code = 260
        else:
            ram_tier = "performance"
            rec_ctx = 1024
            rec_predict_general = 260
            rec_predict_code = 400

        gpu_info = cls._detect_gpu()
        audio_info = cls._detect_audio()
        os_info = cls._detect_os_environment(ws)

        try:
            disk = psutil.disk_usage(ws)
            disk_free_gb = round(disk.free / (1024 ** 3), 2)
            disk_total_gb = round(disk.total / (1024 ** 3), 2)
        except Exception:
            disk_free_gb = 10.0
            disk_total_gb = 50.0

        profile = {
            "platform": sys.platform,
            "os_name": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "workspace_root": ws,
            "cpu": {
                "logical_cores": logical_cores,
                "physical_cores": physical_cores,
                "optimal_threads": optimal_threads
            },
            "memory": {
                "total_gb": total_ram_gb,
                "available_gb": avail_ram_gb,
                "tier": ram_tier,
                "recommended_ctx": rec_ctx,
                "recommended_predict_general": rec_predict_general,
                "recommended_predict_code": rec_predict_code
            },
            "gpu": gpu_info,
            "audio": audio_info,
            "os_environment": os_info,
            "storage": {
                "free_gb": disk_free_gb,
                "total_gb": disk_total_gb
            }
        }
        cls._cached_profile = profile
        return profile

    @classmethod
    def _detect_gpu(cls) -> Dict[str, Any]:
        info = {
            "has_gpu": False,
            "vendor": "none",
            "name": "CPU Fallback",
            "vram_gb": 0.0,
            "cuda_available": False
        }
        try:
            import torch
            if torch.cuda.is_available():
                info["has_gpu"] = True
                info["vendor"] = "nvidia"
                info["cuda_available"] = True
                info["name"] = torch.cuda.get_device_name(0)
                info["vram_gb"] = round(torch.cuda.get_device_properties(0).total_memory / (1024 ** 3), 2)
                return info
            if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                info["has_gpu"] = True
                info["vendor"] = "apple"
                info["name"] = "Apple Silicon Metal"
                return info
        except Exception:
            pass

        try:
            res = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=1.5)
            if res.returncode == 0 and res.stdout.strip():
                parts = res.stdout.strip().split("\n")[0].split(",")
                info["has_gpu"] = True
                info["vendor"] = "nvidia"
                info["name"] = parts[0].strip()
                if len(parts) > 1:
                    info["vram_gb"] = round(float(parts[1].strip()) / 1024, 2)
                return info
        except Exception:
            pass

        return info

    @classmethod
    def _detect_audio(cls) -> Dict[str, Any]:
        info = {
            "mic_available": False,
            "mic_count": 0,
            "tts_engine": "silent"
        }
        try:
            import speech_recognition as sr
            mics = sr.Microphone.list_microphone_names()
            info["mic_count"] = len(mics)
            info["mic_available"] = len(mics) > 0
        except Exception:
            pass

        if sys.platform.startswith("win"):
            try:
                import win32com.client
                v = win32com.client.Dispatch("SAPI.SpVoice")
                if v.GetVoices().Count > 0:
                    info["tts_engine"] = "sapi5"
            except Exception:
                pass
        elif sys.platform == "darwin":
            if shutil.which("say"):
                info["tts_engine"] = "say"
        elif sys.platform.startswith("linux"):
            if shutil.which("espeak") or shutil.which("spd-say"):
                info["tts_engine"] = "espeak"

        return info

    @classmethod
    def _detect_os_environment(cls, workspace_root: str) -> Dict[str, Any]:
        info = {
            "apps": {},
            "shell": "powershell" if sys.platform.startswith("win") else "bash"
        }
        if sys.platform.startswith("win"):
            info["apps"]["explorer"] = True
            info["apps"]["cmd"] = True
            info["apps"]["powershell"] = bool(shutil.which("powershell.exe") or shutil.which("powershell"))
            info["apps"]["vscode"] = bool(
                shutil.which("code") or
                os.path.exists(os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")) or
                os.path.exists(r"C:\Program Files\Microsoft VS Code\Code.exe")
            )
            info["apps"]["chrome"] = bool(
                shutil.which("chrome") or
                os.path.exists(r"C:\Program Files\Google\Chrome\Application\chrome.exe") or
                os.path.exists(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") or
                os.path.exists(os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"))
            )
            info["apps"]["notepad"] = bool(shutil.which("notepad.exe") or shutil.which("notepad"))
            info["apps"]["calc"] = bool(shutil.which("calc.exe") or shutil.which("calc"))
        else:
            info["apps"]["explorer"] = bool(shutil.which("xdg-open") or shutil.which("open"))
            info["apps"]["vscode"] = bool(shutil.which("code"))
            info["apps"]["browser"] = bool(shutil.which("google-chrome") or shutil.which("firefox") or shutil.which("open"))
            info["apps"]["terminal"] = bool(shutil.which("x-terminal-emulator") or shutil.which("gnome-terminal") or shutil.which("bash"))
        return info

    @classmethod
    def get_profile(cls, force_refresh: bool = False) -> Dict[str, Any]:
        if cls._cached_profile is not None and not force_refresh:
            return cls._cached_profile
        ws = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cache_file = os.path.join(ws, "data", "hardware_profile.json")
        if not force_refresh and os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cls._cached_profile = json.load(f)
                    return cls._cached_profile
            except Exception:
                pass
        return cls.save_profile()

    @classmethod
    def save_profile(cls, workspace_root: Optional[str] = None) -> Dict[str, Any]:
        ws = workspace_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        profile = cls.probe_hardware(ws)
        data_dir = os.path.join(ws, "data")
        os.makedirs(data_dir, exist_ok=True)
        cache_file = os.path.join(data_dir, "hardware_profile.json")
        try:
            tmp = cache_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(profile, f, indent=2)
            os.replace(tmp, cache_file)
        except Exception:
            pass
        return profile

    @classmethod
    def auto_initialize(cls, workspace_root: Optional[str] = None) -> Dict[str, Any]:
        ws = workspace_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dirs_to_ensure = [
            os.path.join(ws, "data"),
            os.path.join(ws, "data", "mongodb_export"),
            os.path.join(ws, "static"),
            os.path.join(ws, "assets"),
            os.path.join(ws, "logs")
        ]
        created_dirs = []
        for d in dirs_to_ensure:
            if not os.path.exists(d):
                os.makedirs(d, exist_ok=True)
                created_dirs.append(d)

        src_bg = os.path.join(ws, "assets", "lyra_hud_bg.png")
        dst_bg = os.path.join(ws, "static", "lyra_hud_bg.png")
        if os.path.exists(src_bg) and not os.path.exists(dst_bg):
            try:
                shutil.copy2(src_bg, dst_bg)
            except Exception:
                pass

        bin_kb = os.path.join(ws, "data", "ai_knowledge_226.json.bin")
        src_kb = os.path.join(ws, "data", "ai_knowledge_226.json")
        kb_initialized = False
        if not os.path.exists(bin_kb) and os.path.exists(src_kb):
            try:
                from core.knowledge_base import AIKnowledgeEngine
                kb = AIKnowledgeEngine(data_path=src_kb)
                kb_initialized = True
            except Exception:
                pass

        profile = cls.save_profile(ws)

        return {
            "status": "ready",
            "workspace": ws,
            "created_dirs": created_dirs,
            "kb_initialized": kb_initialized,
            "profile": profile
        }

    @classmethod
    def ensure_ollama_offline(cls) -> bool:
        import socket
        import time
        try:
            with socket.create_connection(('127.0.0.1', 11434), timeout=0.2):
                return True
        except Exception:
            pass
        ollama_bin = shutil.which('ollama')
        if not ollama_bin:
            common_paths = [
                os.path.expandvars(r'%LOCALAPPDATA%\Programs\Ollama\ollama.exe'),
                r'F:\Ollama\app\ollama.exe',
                r'C:\Program Files\Ollama\ollama.exe'
            ]
            for p in common_paths:
                if os.path.exists(p):
                    ollama_bin = p
                    break
        if ollama_bin:
            try:
                flags = 0x08000000 if sys.platform == 'win32' else 0
                subprocess.Popen([ollama_bin, 'serve'], creationflags=flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                for _ in range(30):
                    time.sleep(0.1)
                    try:
                        with socket.create_connection(('127.0.0.1', 11434), timeout=0.2):
                            return True
                    except Exception:
                        pass
            except Exception:
                pass
        return False

    @classmethod
    def launch_background_opener(cls, port: int = 8501):
        import socket
        import time
        import webbrowser
        import threading
        import urllib.request

        def _warmup():
            try:
                payload = json.dumps({
                    'model': 'lyra:1b',
                    'keep_alive': -1,
                    'options': {'num_predict': 1, 'num_ctx': 512}
                }).encode('utf-8')
                req = urllib.request.Request(
                    'http://127.0.0.1:11434/api/generate',
                    data=payload,
                    headers={'Content-Type': 'application/json'}
                )
                urllib.request.urlopen(req, timeout=120)
            except Exception:
                pass

        threading.Thread(target=_warmup, daemon=True).start()

        target_url = f'http://127.0.0.1:{port}'
        for _ in range(400):
            try:
                with socket.create_connection(('127.0.0.1', port), timeout=0.04):
                    webbrowser.open(target_url)
                    break
            except Exception:
                time.sleep(0.025)

