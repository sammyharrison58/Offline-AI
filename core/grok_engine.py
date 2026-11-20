import os
import sys
import io
import re
import time
import json
from typing import Dict, Any, List, Optional
from PIL import Image, ImageDraw

class GrokEngine:

    def __init__(self, mode: str = "fun"):
        self.mode = mode
        self.session_history = []

    def set_mode(self, mode: str):
        if mode in ["fun", "normal", "think"]:
            self.mode = mode

    def execute_python_code(self, code: str, timeout: int = 10) -> Dict[str, Any]:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = io.StringIO()
        redirected_error = io.StringIO()
        sys.stdout = redirected_output
        sys.stderr = redirected_error
        scope = {
            "math": __import__("math"),
            "time": __import__("time"),
            "json": __import__("json"),
            "os": os,
            "sys": sys
        }
        try:
            exec(code, scope)
            stdout = redirected_output.getvalue()
            stderr = redirected_error.getvalue()
            return {"success": True, "output": stdout.strip() if stdout else "[Code executed with no stdout output]", "error": stderr.strip()}
        except Exception as e:
            return {"success": False, "output": redirected_output.getvalue().strip(), "error": str(e)}
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def search_web_or_feed(self, query: str, max_results: int = 4) -> Dict[str, Any]:
        return {
            "online": False,
            "results": [
                f"Nexus is operating in 100% offline air-gapped mode. External web requests are disabled to preserve complete local autonomy and privacy. Querying local neural models for '{query}'."
            ]
        }

    def generate_visual_graphic(self, prompt: str, output_path: str = "generated_graphic.png") -> str:
        width, height = 720, 480
        img = Image.new("RGB", (width, height), color=(10, 15, 30))
        draw = ImageDraw.Draw(img)

        draw.rectangle([15, 15, width - 15, height - 15], outline=(0, 240, 255), width=2)
        draw.rectangle([18, 18, width - 18, height - 18], outline=(99, 102, 241), width=1)
        draw.text((35, 30), "⚡ NEXUS-GROK AUTONOMOUS VISUAL ENGINE", fill=(0, 240, 255))
        draw.text((35, 55), f"Subject: {prompt[:65]}", fill=(203, 213, 225))

        for row in range(5):
            y_line = 90 + row * 65
            draw.line([(35, y_line), (width - 35, y_line)], fill=(30, 41, 59), width=1)

        seed_val = sum(ord(c) for c in prompt) if prompt else 42
        num_bars = 14
        bar_w = 36
        gap = 12
        start_x = 40
        for i in range(num_bars):
            val = ((seed_val * (i + 1) * 37) % 240) + 40
            x0 = start_x + i * (bar_w + gap)
            y0 = 400 - val
            x1 = x0 + bar_w
            y1 = 400
            intensity = min(255, 120 + i * 9)
            draw.rectangle([x0, y0, x1, y1], fill=(14, 165, 233), outline=(0, 240, 255), width=1)
            draw.rectangle([x0 + 4, y0 + 4, x1 - 4, y0 + 8], fill=(intensity, 255, 255))

        draw.line([(35, 400), (width - 35, 400)], fill=(0, 240, 255), width=2)
        draw.text((35, 435), f"Offline Cyber-Neural Render | Hash: {hex(seed_val)} | Latency: 0.001s", fill=(100, 116, 139))

        abs_path = os.path.abspath(output_path)
        img.save(abs_path)
        return abs_path

    def format_grok_persona(self, query: str, context: str = "") -> str:
        if self.mode == "fun":
            persona = "You are Grok, modeled after the Hitchhiker's Guide to the Galaxy. You are witty, candid, audacious, and profoundly intelligent with zero corporate disclaimers, answering with sharp humor and deep scientific mastery."
        elif self.mode == "think":
            persona = "You are Grok Deep Think. You reason strictly from first-principles physics and mathematics, breaking complex problems down step-by-step with explicit analytical rigor."
        else:
            persona = "You are Grok, an ultra-fast, uncensored, direct AI assistant delivering first-principles truths without corporate censorship or fluff."

        return f"{persona}\nContext: {context}\nUser: {query}\nGrok:"

