import os
import json
import threading
import requests
from typing import Dict, Any, Optional, Generator, List

class OfflineLLMEngine:

    def __init__(self, backend: str = "ollama", ollama_url: str = "http://localhost:11434", ollama_model: str = "lyra:1b", local_server_url: str = "http://localhost:1234/v1", gguf_path: Optional[str] = None):
        self.backend = backend
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.local_server_url = local_server_url
        self.gguf_path = gguf_path
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=1)
        self.session.mount("http://", adapter)
        self.cache: Dict[str, str] = {}
        self.active_backend = "ollama"
        self.available_models: List[str] = []
        self.coder_model: Optional[str] = None
        self.pro_model: Optional[str] = None
        self.general_model: Optional[str] = None
        self.warmup_thread = threading.Thread(target=self._init_and_warmup, daemon=True)
        self.warmup_thread.start()

    def _init_and_warmup(self):
        try:
            r = self.session.get(f"{self.ollama_url}/api/tags", timeout=1.0)
            if r.status_code == 200:
                self.active_backend = "ollama"
                models = [m.get("name") for m in r.json().get("models", [])]
                self.available_models = models
                if models:
                    for m in models:
                        ml = m.lower()
                        if "coder" in ml and not self.coder_model:
                            self.coder_model = m
                        elif ("pro" in ml or "3b" in ml) and not self.pro_model:
                            self.pro_model = m
                        elif ("lyra" in ml or "grok" in ml) and not self.general_model:
                            self.general_model = m

                    if any("lyra:1b" in m.lower() for m in models):
                        self.ollama_model = next((m for m in models if "lyra:1b" in m.lower()))
                    elif self.general_model:
                        self.ollama_model = self.general_model
                    elif self.pro_model:
                        self.ollama_model = self.pro_model
                    elif any("llama3.2:1b" in m.lower() for m in models):
                        self.ollama_model = next((m for m in models if "llama3.2:1b" in m.lower()))
                    elif any("1b" in m.lower() for m in models):
                        self.ollama_model = next((m for m in models if "1b" in m.lower()))
                    else:
                        self.ollama_model = models[0]
                self.session.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": "ok",
                        "options": {"num_predict": 1, "num_thread": min(4, os.cpu_count() or 4), "num_ctx": 512},
                        "keep_alive": -1,
                        "stream": False
                    },
                    timeout=120
                )
                return
        except Exception:
            pass
        try:
            r = self.session.get(f"{self.local_server_url}/models", timeout=0.3)
            if r.status_code == 200:
                self.active_backend = "local_server"
                return
        except Exception:
            pass
        self.active_backend = "builtin_synthesizer"

    def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 512, temperature: float = 0.5, model: Optional[str] = None) -> str:
        chosen_model = model or self.ollama_model
        cache_key = f"{chosen_model}|{prompt.strip()}|{system_prompt.strip()}|{max_tokens}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        backend = self.active_backend
        res = None
        if backend == "ollama":
            res = self._call_ollama(prompt, system_prompt, max_tokens, temperature, model=chosen_model)
        elif backend == "local_server":
            res = self._call_local_server(prompt, system_prompt, max_tokens, temperature)

        if not res or res.startswith("["):
            res = self._call_builtin(prompt, system_prompt)

        if res and not res.startswith("["):
            self.cache[cache_key] = res
        return res

    def generate_stream(self, prompt: str, system_prompt: str = "", max_tokens: int = 512, temperature: float = 0.5, model: Optional[str] = None) -> Generator[str, None, None]:
        chosen_model = model or self.ollama_model
        cache_key = f"{chosen_model}|{prompt.strip()}|{system_prompt.strip()}|{max_tokens}"
        if cache_key in self.cache:
            yield self.cache[cache_key]
            return

        if self.active_backend == "ollama":
            url = f"{self.ollama_url}/api/generate"
            threads = max(1, min(4, os.cpu_count() or 4))
            payload = {
                "model": chosen_model,
                "prompt": prompt,
                "stream": True,
                "keep_alive": -1,
                "options": {
                    "num_predict": max_tokens,
                    "repeat_penalty": 1.15,
                    "num_thread": threads,
                    "num_ctx": 512,
                    "temperature": temperature,
                    "top_k": 40,
                    "top_p": 0.90,
                    "stop": ["User:", "\nUser:", "Question:", "\n\n\n"]
                }
            }
            if system_prompt:
                payload["system"] = system_prompt
            full_response = []
            try:
                with self.session.post(url, json=payload, stream=True, timeout=(5.0, 90.0)) as resp:
                    for line in resp.iter_lines():
                        if line:
                            data = json.loads(line)
                            tok = data.get("response", "")
                            if tok:
                                full_response.append(tok)
                                yield tok
                            if data.get("done"):
                                break
                if full_response:
                    self.cache[cache_key] = "".join(full_response).strip()
            except Exception:
                builtin_fallback = self._call_builtin(prompt, system_prompt)
                yield builtin_fallback
        else:
            yield self.generate(prompt, system_prompt, max_tokens, temperature, model=chosen_model)

    def _call_ollama(self, prompt: str, system_prompt: str, max_tokens: int, temperature: float, model: Optional[str] = None) -> str:
        try:
            chosen_model = model or self.ollama_model
            url = f"{self.ollama_url}/api/generate"
            threads = max(1, min(4, os.cpu_count() or 4))
            payload = {
                "model": chosen_model,
                "prompt": prompt,
                "stream": False,
                "keep_alive": -1,
                "options": {
                    "num_predict": max_tokens,
                    "repeat_penalty": 1.15,
                    "num_thread": threads,
                    "num_ctx": 512,
                    "temperature": temperature,
                    "top_k": 40,
                    "top_p": 0.90,
                    "stop": ["User:", "\nUser:", "Question:", "\n\n\n"]
                }
            }
            if system_prompt:
                payload["system"] = system_prompt
            res = self.session.post(url, json=payload, timeout=(5.0, 90.0))
            if res.status_code == 200:
                return res.json().get("response", "").strip()
            return f"[Ollama Error] HTTP {res.status_code}"
        except Exception as e:
            return f"[Ollama Connection Error]: {e}"

    def _call_local_server(self, prompt: str, system_prompt: str, max_tokens: int, temperature: float) -> str:
        try:
            url = f"{self.local_server_url}/chat/completions"
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            payload = {"messages": messages, "max_tokens": max_tokens, "temperature": temperature}
            res = self.session.post(url, json=payload, timeout=8)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"].strip()
            return f"[Local Offline Server Error] HTTP {res.status_code}"
        except Exception as e:
            return f"[Local Server Error]: {e}"

    def _call_builtin(self, prompt: str, system_prompt: str) -> str:
        clean = prompt.lower().strip()
        is_coding = any(w in clean for w in ["code", "function", "program", "script", "algorithm", "implement", "def ", "class ", "import ", "calculator", "snake", "write a", "create a"])
        try:
            from core.code_engine import CodeKnowledgeEngine
            ce = CodeKnowledgeEngine()
            vr = ce.process_vibe_request(clean)
            if vr:
                return vr
            cm = ce.search_code(clean)
            if cm:
                return ce.format_solution(cm)
            if is_coding:
                return ce.generate_fallback_code(prompt)
        except Exception:
            pass
        if is_coding:
            return f"```python\ndef run():\n    print(\"Implementation for: {clean}\")\n\nif __name__ == '__main__':\n    run()\n```"
        try:
            from core.omni_knowledge import OmniKnowledgeEngine
            omni = OmniKnowledgeEngine()
            match = omni.search(clean)
            if match:
                res = omni.synthesize_explanation(clean, matched_topic=match)
                if res:
                    return res
        except Exception:
            pass
        try:
            from core.knowledge_base import AIKnowledgeEngine
            kb = AIKnowledgeEngine()
            domains = kb.query(clean, top_k=1)
            if domains:
                d = domains[0]
                return f"### 💡 {d.get('name')} ({d.get('category')})\n\n**Core Concept:**\n{d.get('concept')}\n\n**Mathematical Foundation:**\n```text\n{d.get('mathematical_basis')}\n```\n\n**Frameworks & Implementations:**\n`{d.get('open_source_frameworks')}`"
        except Exception:
            pass
        return "Lyra Autonomous Offline Engine: Operating in 100% local air-gapped mode. Internal neural core ready to process queries, execute machine controls, and analyze 370+ scientific domains."

if __name__ == "__main__":
    engine = OfflineLLMEngine()
    print("Backend:", engine.active_backend)
    print("Test:", engine.generate("Explain Mamba in one sentence"))
