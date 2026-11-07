import os
import json
import threading
import requests
from typing import Dict, Any, Optional, Generator

class OfflineLLMEngine:

    def __init__(self, backend: str = "auto", ollama_url: str = "http://localhost:11434", ollama_model: str = "llama3.2:1b", openai_compatible_url: str = "http://localhost:1234/v1", gguf_path: Optional[str] = None):
        self.backend = backend
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.openai_compatible_url = openai_compatible_url
        self.gguf_path = gguf_path
        self.active_backend = self._detect_backend()
        self.warmup_thread = threading.Thread(target=self.warmup, daemon=True)
        self.warmup_thread.start()

    def _detect_backend(self) -> str:
        if self.backend != "auto":
            return self.backend
        try:
            r = requests.get(f"{self.ollama_url}/api/tags", timeout=0.6)
            if r.status_code == 200:
                models = [m.get("name") for m in r.json().get("models", [])]
                if models:
                    if any("1b" in m.lower() for m in models):
                        self.ollama_model = next((m for m in models if "1b" in m.lower()))
                    else:
                        self.ollama_model = models[0]
                return "ollama"
        except Exception:
            pass
        try:
            r = requests.get(f"{self.openai_compatible_url}/models", timeout=0.4)
            if r.status_code == 200:
                return "openai_compatible"
        except Exception:
            pass
        return "builtin_synthesizer"

    def warmup(self):
        if self.active_backend == "ollama":
            try:
                requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": "ok",
                        "options": {"num_predict": 1, "num_thread": 4, "num_ctx": 256},
                        "keep_alive": -1,
                        "stream": False
                    },
                    timeout=25
                )
            except Exception:
                pass

    def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 20, temperature: float = 0.3) -> str:
        backend = self.active_backend
        if backend == "ollama":
            return self._call_ollama(prompt, system_prompt, max_tokens, temperature)
        elif backend == "openai_compatible":
            return self._call_openai(prompt, system_prompt, max_tokens, temperature)
        else:
            return self._call_builtin(prompt, system_prompt)

    def generate_stream(self, prompt: str, system_prompt: str = "", max_tokens: int = 20, temperature: float = 0.3) -> Generator[str, None, None]:
        if self.active_backend == "ollama":
            url = f"{self.ollama_url}/api/generate"
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "system": system_prompt or "You are Grok. Direct 1-sentence answer only. Never repeat the question or quote anything.",
                "stream": True,
                "keep_alive": -1,
                "options": {
                    "num_predict": min(max_tokens, 20),
                    "repeat_penalty": 1.25,
                    "num_thread": 4,
                    "num_ctx": 256,
                    "temperature": temperature,
                    "top_k": 25,
                    "top_p": 0.85,
                    "stop": ["\n", "\n\n", "User:", "\nUser", "Question:", "Direct Answer:"]
                }
            }
            try:
                with requests.post(url, json=payload, stream=True, timeout=20) as resp:
                    for line in resp.iter_lines():
                        if line:
                            data = json.loads(line)
                            tok = data.get("response", "")
                            if tok:
                                yield tok
                            if data.get("done"):
                                break
            except Exception as e:
                yield f"[Ollama Connection Error]: {e}"
        else:
            yield self.generate(prompt, system_prompt, max_tokens, temperature)

    def _call_ollama(self, prompt: str, system_prompt: str, max_tokens: int, temperature: float) -> str:
        try:
            url = f"{self.ollama_url}/api/generate"
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "system": system_prompt or "You are Grok. Direct 1-sentence answer only. Never repeat the question or quote anything.",
                "stream": False,
                "keep_alive": -1,
                "options": {
                    "num_predict": min(max_tokens, 20),
                    "repeat_penalty": 1.25,
                    "num_thread": 4,
                    "num_ctx": 256,
                    "temperature": temperature,
                    "top_k": 25,
                    "top_p": 0.85,
                    "stop": ["\n", "\n\n", "User:", "\nUser", "Question:", "Direct Answer:"]
                }
            }
            res = requests.post(url, json=payload, timeout=20)
            if res.status_code == 200:
                return res.json().get("response", "").strip()
            return f"[Ollama Error] HTTP {res.status_code}"
        except Exception as e:
            return f"[Ollama Connection Error]: {e}"

    def _call_openai(self, prompt: str, system_prompt: str, max_tokens: int, temperature: float) -> str:
        try:
            url = f"{self.openai_compatible_url}/chat/completions"
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            payload = {"messages": messages, "max_tokens": min(max_tokens, 20), "temperature": temperature}
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"].strip()
            return f"[OpenAI Error] HTTP {res.status_code}"
        except Exception as e:
            return f"[Local Server Error]: {e}"

    def _call_builtin(self, prompt: str, system_prompt: str) -> str:
        return "Nexus-Grok neural engine active."

if __name__ == "__main__":
    engine = OfflineLLMEngine()
    print("Backend:", engine.active_backend)
    print("Test:", engine.generate("Explain Mamba in one sentence"))
