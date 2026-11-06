import os
import sys
import time
import socket
import struct
import subprocess
import psutil
from typing import Dict, Any, List, Optional
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
try:
    from PIL import ImageGrab
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class SystemController:

    def __init__(self, workspace_root: Optional[str]=None):
        self.workspace_root = workspace_root or os.getcwd()
        if PYAUTOGUI_AVAILABLE:
            pyautogui.FAILSAFE = True

    def run_powershell(self, script: str, timeout: int=30) -> Dict[str, Any]:
        try:
            result = subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command', script], capture_output=True, text=True, timeout=timeout)
            return {'success': result.returncode == 0, 'returncode': result.returncode, 'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()}
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': f'Command timed out after {timeout} seconds'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def run_cmd(self, command: str, timeout: int=30) -> Dict[str, Any]:
        try:
            result = subprocess.run(['cmd.exe', '/c', command], capture_output=True, text=True, timeout=timeout)
            return {'success': result.returncode == 0, 'returncode': result.returncode, 'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def list_processes(self, filter_name: Optional[str]=None, limit: int=25) -> List[Dict[str, Any]]:
        processes = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                name = p.info['name']
                if filter_name and filter_name.lower() not in name.lower():
                    continue
                mem_mb = p.info['memory_info'].rss / (1024 * 1024) if p.info.get('memory_info') else 0
                processes.append({'pid': p.info['pid'], 'name': name, 'cpu_percent': p.info.get('cpu_percent', 0.0), 'memory_mb': round(mem_mb, 1)})
                if len(processes) >= limit:
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes

    def launch_app(self, app_path_or_cmd: str) -> Dict[str, Any]:
        try:
            if os.path.exists(app_path_or_cmd):
                os.startfile(app_path_or_cmd)
                return {'success': True, 'message': f'Started {app_path_or_cmd}'}
            else:
                proc = subprocess.Popen(app_path_or_cmd, shell=True)
                return {'success': True, 'pid': proc.pid, 'message': f'Spawned process: {app_path_or_cmd}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def terminate_process(self, pid: int) -> Dict[str, Any]:
        try:
            p = psutil.Process(pid)
            p.terminate()
            return {'success': True, 'message': f'Terminated process {pid}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_screen_resolution(self) -> Dict[str, int]:
        if PYAUTOGUI_AVAILABLE:
            w, h = pyautogui.size()
            return {'width': w, 'height': h}
        return {'width': 1920, 'height': 1080}

    def click(self, x: int, y: int, clicks: int=1, button: str='left') -> Dict[str, Any]:
        if not PYAUTOGUI_AVAILABLE:
            return {'success': False, 'error': 'PyAutoGUI not installed'}
        try:
            pyautogui.click(x=x, y=y, clicks=clicks, button=button)
            return {'success': True, 'message': f'Clicked at ({x}, {y})'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def type_keys(self, text: str, interval: float=0.05) -> Dict[str, Any]:
        if not PYAUTOGUI_AVAILABLE:
            return {'success': False, 'error': 'PyAutoGUI not installed'}
        try:
            pyautogui.write(text, interval=interval)
            return {'success': True, 'message': f'Typed text ({len(text)} chars)'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def press_hotkey(self, *keys: str) -> Dict[str, Any]:
        if not PYAUTOGUI_AVAILABLE:
            return {'success': False, 'error': 'PyAutoGUI not installed'}
        try:
            pyautogui.hotkey(*keys)
            return {'success': True, 'message': f"Pressed hotkey: {'+'.join(keys)}"}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def capture_screenshot(self, save_path: str='screenshot.png') -> Dict[str, Any]:
        abs_path = os.path.abspath(save_path)
        if PIL_AVAILABLE:
            try:
                im = ImageGrab.grab()
                im.save(abs_path)
                return {'success': True, 'path': abs_path}
            except Exception:
                pass
        if PYAUTOGUI_AVAILABLE:
            try:
                im = pyautogui.screenshot()
                im.save(abs_path)
                return {'success': True, 'path': abs_path}
            except Exception:
                pass
        try:
            ps_script = f'Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; $bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height; $graphics = [System.Drawing.Graphics]::FromImage($bmp); $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size); $bmp.Save("{abs_path.replace(chr(92), chr(47))}"); $graphics.Dispose(); $bmp.Dispose();'
            res = self.run_powershell(ps_script)
            if os.path.exists(abs_path) and os.path.getsize(abs_path) > 0:
                return {'success': True, 'path': abs_path}
            return {'success': False, 'error': res.get('stderr') or 'Failed to capture display'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def send_wake_on_lan(mac_address: str, broadcast_ip: str='255.255.255.255', port: int=9) -> Dict[str, Any]:
        try:
            clean_mac = mac_address.replace(':', '').replace('-', '')
            if len(clean_mac) != 12:
                raise ValueError('Invalid MAC address length. Must be 12 hexadecimal characters.')
            mac_bytes = bytes.fromhex(clean_mac)
            magic_packet = b'\xff' * 6 + mac_bytes * 16
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(magic_packet, (broadcast_ip, port))
            return {'success': True, 'message': f'Wake-on-LAN Magic Packet broadcasted to {mac_address} via {broadcast_ip}:{port}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def schedule_wake_timer(self, wake_time_hh_mm: str, task_name: str='AI_AutoWake') -> Dict[str, Any]:
        try:
            cmd = f'schtasks /create /tn "{task_name}" /tr "cmd.exe /c echo Waking up system" /sc once /st {wake_time_hh_mm} /ru SYSTEM /f'
            res = self.run_powershell(cmd)
            return {'success': res.get('success', False), 'message': f'Wake timer scheduled for {wake_time_hh_mm}', 'details': res}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def sleep_system(self) -> Dict[str, Any]:
        return self.run_powershell('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

    def reboot_system(self, delay_seconds: int=5) -> Dict[str, Any]:
        return self.run_cmd(f'shutdown /r /t {delay_seconds}')

    def get_telemetry(self) -> Dict[str, Any]:
        cpu_usage = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        disks = {}
        try:
            usage = psutil.disk_usage('.')
            disks['primary'] = {'total_gb': round(usage.total / 1024 ** 3, 2), 'free_gb': round(usage.free / 1024 ** 3, 2), 'percent_used': usage.percent}
        except Exception:
            pass
        battery = psutil.sensors_battery()
        battery_info = {'percent': battery.percent if battery else 'N/A', 'power_plugged': battery.power_plugged if battery else True}
        return {'cpu_usage_percent': cpu_usage, 'ram_total_gb': round(ram.total / 1024 ** 3, 2), 'ram_available_gb': round(ram.available / 1024 ** 3, 2), 'ram_used_percent': ram.percent, 'disks': disks, 'battery': battery_info, 'platform': sys.platform}
if __name__ == '__main__':
    controller = SystemController()
    print('Telemetry:', controller.get_telemetry())
    print('Screen:', controller.get_screen_resolution())
    print('Processes Sample:', controller.list_processes(limit=5))
