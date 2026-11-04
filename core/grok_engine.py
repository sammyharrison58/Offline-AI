import os
import sys
import io
import re
import time
import json
import urllib.request
import urllib.parse
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
        try:
            encoded = urllib.parse.quote_plus(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=4) as response:
                html = response.read().decode("utf-8", errors="ignore")
            
            snippets = []
            matches = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
            for m in matches[:max_results]:
                clean = re.sub(r'<[^>]+>', '', m).strip()
                if clean:
                    snippets.append(clean)

            if snippets:
                return {"online": True, "results": snippets}
            return {"online": True, "results": ["Search completed; live web queried."]}
        except Exception as e:
            return {"online": False, "results": [f"Operating in offline air-gapped mode. Internal 226 AI knowledge active. Error: {str(e)}"]}

    def generate_visual_graphic(self, prompt: str, output_path: str = "generated_graphic.png") -> str:
        width, height = 720, 480
        img = Image.new("RGB", (width, height), color=(15, 23, 42))
        draw = ImageDraw.Draw(img)

        draw.rectangle([20, 20, width - 20, height - 20], outline=(99, 102, 241), width=3)
        draw.text((40, 40), f"GROK AI VISUAL GENERATOR", fill=(129, 140, 248))
        draw.text((40, 70), f"Prompt: {prompt[:60]}", fill=(148, 163, 184))

        for i in range(12):
            x0 = 60 + i * 50
            y0 = 350 - (i * 17 % 180)
            x1 = x0 + 35
            y1 = 380
            draw.rectangle([x0, y0, x1, y1], fill=(59, 130, 246), outline=(96, 165, 250))

        draw.line([(60, 260), (width - 60, 260)], fill=(236, 72, 153), width=2)
        draw.text((40, 420), f"Rendered by Nexus-Grok Autonomous Engine | Seed: {int(time.time())}", fill=(100, 116, 139))

        abs_path = os.path.abspath(output_path)
        img.save(abs_path)
        return abs_path

    def format_grok_persona(self, query: str, context: str = "") -> str:
        if self.mode == "fun":
            persona = "You are Grok, witty, rebellious, clever, and candid. Speak with smart humor, zero corporate BS, and maximum technical brilliance."
        elif self.mode == "think":
            persona = "You are Grok Deep Think. Break down problems step-by-step with explicit chain-of-thought mathematical rigor before stating your conclusion."
        else:
            persona = "You are Grok, an ultra-fast, intelligent, direct AI assistant."
        
        return f"{persona}\nContext: {context}\nUser: {query}\nGrok:"
