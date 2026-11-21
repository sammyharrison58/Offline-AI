import os
import sys
import re
import json
import threading
import math
from typing import Dict, Any, Optional, Generator, List

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from core.knowledge_base import AIKnowledgeEngine
from core.omni_knowledge import OmniKnowledgeEngine
from core.code_engine import CodeKnowledgeEngine
from core.human_engine import HumanPersonaEngine

_CLEAN_RE = re.compile(r'[^a-z0-9\s]')
_MATH_PREFIX_RE = re.compile(r'^(what is|calculate|evaluate|solve|compute)\s+')
_MATH_EXPR_RE = re.compile(r'^[a-z0-9\.\s\+\-\*\/\(\)\^\%\,]+$', re.IGNORECASE)
_APP_RE = re.compile(r'^(open|launch|start)\s+(app\s+)?', re.IGNORECASE)
_KILL_RE = re.compile(r'^(close|kill|terminate|quit)\s+(app\s+)?', re.IGNORECASE)
_DEL_FILE_RE = re.compile(r'^(delete file|remove file)\s+', re.IGNORECASE)
_DIR_RE = re.compile(r'^(create folder|make folder|create directory)\s+', re.IGNORECASE)
_MAC_RE = re.compile(r'([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})')
_TIME_RE = re.compile(r'(\d{1,2}:\d{2})')
_AMT_RE = re.compile(r'(\d+(?:\.\d+)?)')
_ADDR_RE = re.compile(r'(0x[a-fA-F0-9]{40})')
_CLEAN_ANSWER_RE = re.compile(r'^(Direct Answer:|Answer:|Grok:|Response:|Question:|Detailed Explanation:)\s*', re.IGNORECASE)

GREETING_EXACT = frozenset({"hello", "hi", "hey", "howdy", "greetings", "yo", "jarvis", "nexus"})
GREETING_STARTS = frozenset({"hello", "hi", "hey", "greetings", "yo"})
GREETING_PHRASES = ("good morning", "good afternoon", "good evening", "wake up")

CONTRACTIONS = {
    "what's": "what is",
    "how's": "how is",
    "who's": "who is",
    "where's": "where is",
    "can't": "cannot",
    "won't": "will not",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "i'm": "i am",
    "it's": "it is",
    "let's": "let us",
    "you're": "you are",
    "they're": "they are",
    "we're": "we are",
    "that's": "that is",
    "there's": "there is",
    "couldn't": "could not",
    "shouldn't": "should not",
    "wouldn't": "would not",
    "hasn't": "has not",
    "haven't": "have not",
    "isn't": "is not",
    "aren't": "are not"
}

PROGRAMMING_LANGS = frozenset([
    "python", "py", "javascript", "js", "typescript", "ts", "c++", "cpp",
    "c", "rust", "rs", "golang", "go", "sql", "bash", "shell", "sh",
    "html", "css", "java", "c#", "csharp", "ruby", "php"
])

CODING_INDICATORS = [
    "write code", "code in", "function to", "write a function", "script to",
    "solve in", "implement in", "how to code", "program to", "algorithm for",
    "class to", "how to write", "how do i code", "create a function",
    "create a script", "code for", "build a script", "build an app",
    "write a query", "write sql", "write python", "write javascript",
    "write typescript", "write c++", "write cpp", "write rust", "write go",
    "write bash", "write html", "write css", "write java", "write c#",
    "in python", "in javascript", "in typescript", "in c++", "in rust",
    "in golang", "in java", "in sql", "in bash", "fizzbuzz", "leetcode",
    "binary search", "quicksort", "merge sort", "bubble sort", "linked list",
    "lru cache", "dijkstra", "trie", "bfs", "dfs", "topological sort",
    "coin change", "longest substring", "debounce", "throttle", "promise",
    "custom hook", "react hook", "usedebounce", "uselocalstorage", "worker pool",
    "thread pool", "concurrency", "circular buffer", "unique ptr", "smart pointer",
    "singleton", "recursive cte", "window function", "running total", "consecutive numbers",
    "rest api", "fastapi", "express", "open file in", "read file in", "write file in",
    "file io", "reverse string", "prime check", "factorial", "gcd in", "euclidean algorithm",
    "todo app", "todo list", "calculator gui", "web scraper", "scraping", "scraper",
    "flask api", "flask app", "discord bot", "login system", "auth system", "password hashing",
    "password generator", "database manager", "sqlite manager", "unit test", "unit tests",
    "pytest", "chat app", "websocket chat", "data pipeline", "etl pipeline", "api client",
    "cli tool", "debug this", "debug code", "fix this code", "fix the bug", "syntax error",
    "explain what this code does", "explain this code", "walk through this code",
    "what does this code do", "how does this code work", "refactor this", "refactor code",
    "optimize this", "make this faster", "clean up code", "add error handling",
    "handle errors in", "error handling to", "make this robust", "write unit tests for"
]

class Nexus226Agent:

    def __init__(self):
        self.knowledge = AIKnowledgeEngine()
        self.omni = OmniKnowledgeEngine()
        self.code_engine = CodeKnowledgeEngine()
        self.human_engine = HumanPersonaEngine()
        self.session_history: List[Dict[str, str]] = []
        self._sys_controller = None
        self._blockchain = None
        self._llm = None
        self._grok = None
        self._mongo = None
        self.cache_path = os.path.join(root_dir, "data", "response_cache.json")
        self.response_cache: Dict[str, str] = self._load_cache()

    def _record_turn(self, role: str, content: str):
        if not content:
            return
        self.session_history.append({"role": role, "content": content})
        if len(self.session_history) > 20:
            self.session_history = self.session_history[-20:]

    def clear_history(self):
        self.session_history.clear()

    def get_history(self) -> List[Dict[str, str]]:
        return list(self.session_history)

    @property
    def sys_controller(self):
        if self._sys_controller is None:
            from core.system_controller import SystemController
            self._sys_controller = SystemController()
        return self._sys_controller

    @property
    def blockchain(self):
        if self._blockchain is None:
            from core.blockchain_manager import BlockchainManager
            self._blockchain = BlockchainManager()
        return self._blockchain

    @property
    def llm(self):
        if self._llm is None:
            from core.llm_engine import OfflineLLMEngine
            self._llm = OfflineLLMEngine()
        return self._llm

    @property
    def grok(self):
        if self._grok is None:
            from core.grok_engine import GrokEngine
            self._grok = GrokEngine(mode="fun")
        return self._grok

    @property
    def mongo(self):
        if self._mongo is None:
            from core.mongo_manager import MongoDBManager
            self._mongo = MongoDBManager()
        return self._mongo

    def _load_cache(self) -> Dict[str, str]:
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        try:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            tmp_path = self.cache_path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.response_cache, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.cache_path)
        except Exception:
            pass

    def _cache_set(self, key: str, value: str):
        if not value or value.startswith("Nexus is operating in 100% offline air-gapped mode") or value.startswith("[Ollama") or value.startswith("[Offline"):
            return
        self.response_cache[key] = value
        threading.Thread(target=self._save_cache, daemon=True).start()

    def _normalize_query(self, q: str) -> str:
        clean = q.strip()
        for k, v in CONTRACTIONS.items():
            pattern = re.compile(re.escape(k), re.IGNORECASE)
            clean = pattern.sub(v, clean)
        return clean

    def _is_greeting(self, ql: str) -> bool:
        clean = _CLEAN_RE.sub(' ', ql).strip()
        words = clean.split()
        if not words:
            return False
        if clean in GREETING_EXACT:
            return True
        if any(g in clean for g in GREETING_PHRASES):
            return True
        if words[0] in GREETING_STARTS:
            return True
        if len(words) <= 3 and any(w in GREETING_EXACT for w in words):
            return True
        return False

    def _is_coding_request(self, q: str, ql: str) -> bool:
        clean = ql.replace("c++", "cpp").replace("c#", "csharp")
        tokens = set(_CLEAN_RE.sub(" ", clean).split())

        if any(target in clean for target in ["who created", "who made", "who invented", "when was", "history of"]):
            return False

        padded_clean = f" {clean} "
        for ind in CODING_INDICATORS:
            if " " in ind:
                if f" {ind} " in padded_clean:
                    return True
            else:
                if ind in tokens:
                    return True

        if any(w in clean for w in ["def ", "class ", "import ", "return ", "console.log", "=>", "lambda ", "try:", "except:", "print(", "for i in ", "while ", "dict[", "list[", "->", "open("]):
            return True

        if any(clean.startswith(p) for p in ["debug", "refactor", "optimize", "explain code", "walk through code", "add error handling", "write unit test", "unit test"]):
            return True

        if any(p in clean for p in ["explain what this code does", "what does this code do", "explain this code", "debug this", "fix this code", "refactor this", "make this faster", "add error handling to", "error handling to", "unit tests for", "write tests for"]):
            return True

        has_lang = bool(tokens.intersection(PROGRAMMING_LANGS))
        if has_lang and any(v in tokens for v in ["code", "function", "script", "program", "class", "method", "syntax", "loop", "array", "list", "dict", "sort", "algorithm", "implement", "write"]):
            return True
        if has_lang and any(phrase in clean for phrase in ["how to", "how do i", "example of"]):
            return True

        code_match = self.code_engine.search_code(q)
        if code_match:
            return True

        vibe_match = self.code_engine.process_vibe_request(q)
        if vibe_match:
            return True

        return False

    def _solve_math(self, q: str) -> Optional[str]:
        clean = q.lower().strip().rstrip('? .')
        clean = _MATH_PREFIX_RE.sub('', clean).strip()
        clean = re.sub(r'(\d+),(\d+)', r'\1\2', clean)
        clean = re.sub(r'(\d+)\s*x\s*(\d+)', r'\1 * \2', clean)
        clean = re.sub(r'(?<=\s)x(?=\s)', '*', clean)
        clean = clean.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('multiplied by', '*').replace('divided by', '/')
        pct_match = re.match(r'^(\d+(?:\.\d+)?)\s*%\s*(?:of)\s*(\d+(?:\.\d+)?)$', clean)
        if pct_match:
            pct = float(pct_match.group(1))
            total = float(pct_match.group(2))
            val = (pct / 100.0) * total
            return str(int(val) if val.is_integer() else round(val, 4))
        if (_MATH_EXPR_RE.match(clean) and any(op in clean for op in '+-*/^%')) or any(fn in clean for fn in ['sqrt(', 'pow(', 'abs(', 'max(', 'min(', 'round(', 'log(']):
            clean_expr = clean.replace('^', '**')
            try:
                safe_math = {'sqrt': math.sqrt, 'abs': abs, 'round': round, 'pow': pow, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'pi': math.pi, 'e': math.e, 'log': math.log, 'log2': math.log2, 'log10': math.log10, 'max': max, 'min': min, 'sum': sum}
                val = eval(clean_expr, {'__builtins__': None}, safe_math)
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                return str(val)
            except Exception:
                return None
        return None

    def process_request(self, user_query: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        res = self._process_request_impl(user_query, history)
        if res:
            self._record_turn("user", user_query.strip())
            self._record_turn("assistant", res)
        return res

    def _process_request_impl(self, user_query: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        q = user_query.strip()
        ql = q.lower()

        if not ql:
            return "Listening. Say or type a command."

        norm_q = self._normalize_query(q)
        norm_ql = norm_q.lower()

        math_res = self._solve_math(q) or self._solve_math(norm_q)
        if math_res is not None:
            ans = f"{math_res}"
            self._cache_set(ql, ans)
            return ans

        active_history = history if history is not None else self.session_history

        human_res = self.human_engine.handle_conversational_query(q, history=active_history) or self.human_engine.handle_conversational_query(norm_q, history=active_history)
        if human_res:
            return human_res

        if self._is_greeting(ql) or self._is_greeting(norm_ql):
            return "Hey! Nexus here, running fully offline and ready to collaborate. What are we building or exploring today?"

        if any(target in ql or target in norm_ql for target in ["who are you", "what are you", "what is your name", "who made you", "who created you", "who built you", "tell me about yourself"]):
            return self.human_engine.identity_explanation

        if any(ql.startswith(w) or norm_ql.startswith(w) for w in ["how are you", "are you ready", "are you online", "status", "are you working"]):
            return "Doing great! All local neural engines, compilers, and knowledge graphs are loaded and responsive. What's on your mind?"

        if ql in ["thank you", "thanks", "thanks grok", "thanks jarvis", "appreciate it"]:
            return "You're very welcome! Always here whenever you need code, an architecture review, or a deep dive."

        if ql in ["help", "what can you do", "commands", "menu"]:
            return "Capabilities: 100% offline neural AI assistant, full OS machine control (open/close apps, volume, mute, lock, network, WoL), 370+ scientific & coding dossiers, polyglot vibe coding partner, local python sandbox, crypto wallet, and MongoDB sync."

        if any(w in ql or w in norm_ql for w in ["can you write code", "can you code", "can i vibe code", "can you vibe code", "what languages do you support", "can you program"]):
            return "Yes, I am a fully equipped polyglot software engineering agent and interactive vibe coding partner. I support full-stack application development, algorithms, refactoring, debugging, error handling, and test suites across Python, C++, Rust, Go, JavaScript, TypeScript, Java, and SQL - 100% offline."

        is_coding = self._is_coding_request(q, ql) or self._is_coding_request(norm_q, norm_ql)

        if not is_coding:
            if any(w in ql for w in ["mute", "silence audio", "unmute"]):
                res = self.sys_controller.toggle_mute()
                return res.get("message", "Mute toggled.")

            if any(w in ql for w in ["volume up", "increase volume", "louder", "turn up sound"]):
                res = self.sys_controller.volume_up(steps=5)
                return res.get("message", "Volume increased.")

            if any(w in ql for w in ["volume down", "decrease volume", "lower volume", "quieter", "turn down sound"]):
                res = self.sys_controller.volume_down(steps=5)
                return res.get("message", "Volume decreased.")

            if any(w in ql for w in ["lock computer", "lock pc", "lock screen", "lock workstation"]):
                res = self.sys_controller.lock_workstation()
                return res.get("message", "Workstation locked.")

            if any(w in ql for w in ["minimize windows", "minimize all", "show desktop"]):
                res = self.sys_controller.minimize_all_windows()
                return res.get("message", "Showing desktop.")

            if any(w in ql for w in ["empty recycle bin", "clean recycle bin", "clear recycle bin"]):
                res = self.sys_controller.empty_recycle_bin()
                return res.get("message", "Recycle bin emptied.")

            if any(w in ql for w in ["what is my ip", "my ip", "ip address", "network info", "network status", "show ip"]):
                net = self.sys_controller.get_network_info()
                return f"Host: {net['hostname']} | IPs: {', '.join(net['ip_addresses'])}"

            if ql.startswith("ping "):
                host = ql.replace("ping ", "").strip().split()[0]
                res = self.sys_controller.ping_host(host)
                return res.get("output") or res.get("error", "Ping executed.")

            if ql.startswith("set mode to ") or ql.startswith("switch mode to "):
                m = ql.replace("set mode to ", "").replace("switch mode to ", "").strip()
                if m in ["fun", "think", "normal"]:
                    self.grok.set_mode(m)
                    return f"Grok mode set to {m.upper()}."

            if ql.startswith("run code:") or ql.startswith("python:") or ql.startswith("execute code:"):
                code = q.split(":", 1)[1].strip()
                res = self.grok.execute_python_code(code)
                if res.get("success"):
                    return f"Output:\n{res.get('output')}"
                return f"Error:\n{res.get('error')}"

            if any(w in ql for w in ["generate image", "create graphic", "draw ", "render image"]):
                prompt = q
                for prefix in ["generate image of", "generate image", "create graphic of", "create graphic", "draw"]:
                    if prefix in ql:
                        prompt = ql.split(prefix, 1)[1].strip()
                        break
                img_path = self.grok.generate_visual_graphic(prompt)
                return f"Graphic rendered: {img_path}"

            if any(w in ql for w in ["search web", "look up", "google ", "browse web", "latest news"]):
                search_query = q
                for prefix in ["search web for", "search web", "look up", "browse web for", "latest news on"]:
                    if prefix in ql:
                        search_query = ql.split(prefix, 1)[1].strip()
                        break
                return f"Nexus is operating in 100% offline air-gapped mode. External web requests are disabled to preserve total privacy. Querying local offline neural models for '{search_query}'."

            if any(w in ql for w in ["wake on lan", "wol", "open computer", "open the computer", "wake computer", "power on"]):
                mac_match = _MAC_RE.search(q)
                if mac_match:
                    mac = mac_match.group(0)
                    res = self.sys_controller.send_wake_on_lan(mac)
                    return f"Wake-on-LAN Signal Broadcasted: {res.get('message', res)}"
                return "Provide target MAC address (e.g. 'Wake computer 00:1A:2B:3C:4D:5E')."

            if "schedule wake" in ql or "wake at" in ql:
                time_match = _TIME_RE.search(q)
                if time_match:
                    t = time_match.group(1)
                    res = self.sys_controller.schedule_wake_timer(t)
                    return f"Wake alarm set for {t}."
                return "Specify time in HH:MM format."

            if "sleep computer" in ql or "suspend machine" in ql:
                return "Entering low-power sleep mode."

            if "opentelemetry" not in ql and (any(w in ql for w in ["system status", "hardware status", "pc specs", "ram usage", "battery", "hardware telemetry"]) or "telemetry" in ql.split()):
                t = self.sys_controller.get_telemetry()
                return f"Hardware: CPU {t['cpu_usage_percent']}% | RAM {t['ram_available_gb']}GB free of {t['ram_total_gb']}GB ({t['ram_used_percent']}% used) | Battery {t['battery']['percent']}%"

            if "screenshot" in ql or "capture display" in ql or "capture screen" in ql:
                path = "screenshot.png"
                res = self.sys_controller.capture_screenshot(path)
                if res.get("success"):
                    return f"Screenshot captured: {res['path']}"
                return f"Screenshot error: {res.get('error')}"

            if ql.startswith("run powershell ") or ql.startswith("powershell "):
                cmd = q.split("powershell", 1)[1].strip()
                res = self.sys_controller.run_powershell(cmd)
                return res.get("stdout") or res.get("stderr") or "[Executed]"

            if ql.startswith("run cmd ") or ql.startswith("cmd "):
                cmd = q.split("cmd", 1)[1].strip()
                res = self.sys_controller.run_cmd(cmd)
                return res.get("stdout") or res.get("stderr") or "[Executed]"

            if any(ql.startswith(p) for p in ["open ", "launch ", "start "]):
                app = _APP_RE.sub("", q).strip()
                res = self.sys_controller.launch_app(app)
                return str(res.get("message", res.get("error")))

            if any(ql.startswith(p) for p in ["close ", "kill ", "terminate ", "quit "]):
                target = _KILL_RE.sub("", q).strip()
                res = self.sys_controller.terminate_by_name(target)
                return str(res.get("message", res.get("error")))

            if ql.startswith("type "):
                text_to_type = q[5:].strip()
                res = self.sys_controller.type_keys(text_to_type)
                return res.get("message", "Typed.")

            if ql.startswith("create file "):
                file_cmd = q[12:].strip()
                if "with content" in file_cmd:
                    f_path, f_content = file_cmd.split("with content", 1)
                else:
                    f_path, f_content = file_cmd, ""
                res = self.sys_controller.create_file(f_path.strip(), f_content.strip())
                return res.get("message", str(res))

            if ql.startswith("delete file ") or ql.startswith("remove file "):
                f_path = _DEL_FILE_RE.sub("", q).strip()
                res = self.sys_controller.delete_file(f_path)
                return res.get("message", str(res))

            if ql.startswith("create folder ") or ql.startswith("make folder ") or ql.startswith("create directory "):
                d_path = _DIR_RE.sub("", q).strip()
                res = self.sys_controller.create_directory(d_path)
                return res.get("message", str(res))

            if ql.startswith("list files") or ql == "dir":
                res = self.sys_controller.list_dir(".")
                items = ", ".join(res.get("items", [])[:15])
                return f"Files: {items}"

            if "list processes" in ql:
                procs = self.sys_controller.list_processes(limit=6)
                return "\n".join([f"- PID {p['pid']}: {p['name']} ({p['memory_mb']} MB)" for p in procs])

            if any(w in ql for w in ["wallet", "balance", "crypto balance", "my address"]):
                b = self.blockchain.get_balance()
                return f"Treasury: Address {b['address']} | Balance {b['balance']} AETH | Ledger: {len(self.blockchain.ledger)} blocks"

            if any(w in ql for w in ["send ", "transfer ", "pay "]) and any(w in ql for w in ["tokens", "eth", "aeth", "to "]):
                amt_match = _AMT_RE.search(q)
                addr_match = _ADDR_RE.search(q)
                if amt_match and addr_match:
                    amt = float(amt_match.group(1))
                    addr = addr_match.group(1)
                    tx_res = self.blockchain.create_and_sign_transaction(addr, amt, memo=f"Transfer: {q[:30]}")
                    if tx_res.get("success"):
                        return f"Mined Block #{tx_res['block_index']}! Sent {tx_res['amount']} AETH to {tx_res['to'][:10]}... | New Balance: {tx_res['new_balance']} AETH"
                    return f"Transaction Failed: {tx_res.get('error')}"
                return "Specify amount and 0x address."

            if "transaction history" in ql or "ledger" in ql:
                txs = self.blockchain.get_transaction_history(limit=4)
                if not txs:
                    return "No transactions in ledger."
                return "\n".join([f"- Block #{t.get('block_index')}: {t.get('amount')} AETH -> {t.get('to')[:10]}..." for t in txs])

            if any(w in ql for w in ["sync mongodb", "sync to mongodb", "put files in mongodb", "put my files in mongodb", "save to mongodb", "backup to mongodb"]):
                r1 = self.mongo.sync_all_files(root_dir)
                r2 = self.mongo.sync_knowledge_base(os.path.join(root_dir, "data", "ai_knowledge_226.json"))
                r3 = self.mongo.sync_blockchain_ledger(os.path.join(root_dir, "data", "blockchain_ledger.json"))
                status = "live MongoDB database" if self.mongo.is_connected else "MongoDB export collections"
                return f"Synced {r1.get('count', 0)} project files, {r2.get('count', 0)} AI knowledge domains, and {r3.get('count', 0)} blockchain blocks into {status}."

            if "mongodb status" in ql or "check mongodb" in ql:
                st = self.mongo.get_status()
                c_status = "Connected" if st.get("connected") else "Disconnected (using offline export)"
                return f"MongoDB: {c_status} | URI: {st.get('uri')} | Collections: {list(st.get('collections', {}).keys()) or ['project_files', 'ai_knowledge_226', 'blockchain_ledger']}"

            if any(ql.startswith(p) for p in ["research ", "deep dive into ", "deep dive ", "offline research on ", "offline research ", "analyze paradigm "]):
                topic = q
                for p in ["research ", "deep dive into ", "deep dive ", "offline research on ", "offline research ", "analyze paradigm "]:
                    if ql.startswith(p):
                        topic = q[len(p):].strip()
                        break
                res = self.knowledge.deep_research(topic)
                return res.get("markdown") or res.get("short_summary")

            if ql.startswith("compare ") and " and " in ql:
                pair = q[8:].split(" and ", 1)
                return self.knowledge.compare_paradigms(pair[0].strip(), pair[1].strip())

        vibe_res = self.code_engine.process_vibe_request(q) or self.code_engine.process_vibe_request(norm_q)
        if vibe_res:
            self._cache_set(ql, vibe_res)
            return vibe_res

        code_match = self.code_engine.search_code(norm_q) or self.code_engine.search_code(q)
        if code_match:
            res = self.code_engine.format_solution(code_match)
            self._cache_set(ql, res)
            return res

        if ql in self.response_cache:
            return self.response_cache[ql]

        if not is_coding:
            omni_match = self.omni.search(norm_q) or self.omni.search(q)
            if omni_match:
                res = self.omni.synthesize_explanation(q, matched_topic=omni_match)
                self._cache_set(ql, res)
                return res

            matched_domains = self.knowledge.query(norm_q, top_k=3) or self.knowledge.query(q, top_k=3)
            if matched_domains:
                top_d = matched_domains[0]
                sec_d = matched_domains[1] if len(matched_domains) > 1 else None
                if any(w in ql for w in ["research", "deep dive", "details", "formula", "math", "dossier"]):
                    res = self.knowledge.deep_research(top_d.get("name"))["markdown"]
                    self._cache_set(ql, res)
                    return res
                exp_lines = [
                    f"### 💡 {top_d.get('name')} ({top_d.get('category')})\n",
                    f"**Core Concept & Mechanism:**\n{top_d.get('concept')}\n",
                    f"**Scientific & Mathematical Foundation:**\n```text\n{top_d.get('mathematical_basis')}\n```\n",
                    f"**Key Insights & Edge Invariants:**\n{top_d.get('obscure_insights')}\n",
                    f"**Frameworks & Implementations:**\n`{top_d.get('open_source_frameworks')}`\n"
                ]
                if sec_d:
                    exp_lines.append(f"\n---\n**🔗 Cross-Domain Correlated Field:** #{sec_d.get('id')} {sec_d.get('name')} ({sec_d.get('category')})\n{sec_d.get('concept')}")
                res = "\n".join(exp_lines)
                self._cache_set(ql, res)
                return res

        if is_coding:
            system_instruction = (
                "You are an expert polyglot software engineer and principal systems architect. "
                "Write clean, elegant, production-grade code in the requested programming language. "
                "Explain the architecture, design choices, edge cases, and time/space complexity with clarity and precision."
            )
        else:
            system_instruction = (
                "You are Nexus, an elite autonomous AI companion and scientific polymath. "
                "Communicate with the warmth, intellectual depth, sharp wit, and clarity of a world-class human collaborator. "
                "Explain concepts using first-principles reasoning and intuitive mental models. "
                "Never use robotic corporate filler or disclaimers. Answer directly, thoroughly, and engagingly."
            )

        prompt_with_history = q
        hist_to_use = history if history is not None else self.session_history
        if hist_to_use:
            prev_turns = []
            for msg in hist_to_use[-6:]:
                role = "User" if msg.get("role") == "user" else "Assistant"
                content = msg.get("content", "").strip()
                if content and content != q:
                    prev_turns.append(f"{role}: {content[:300]}")
            if prev_turns:
                prev_turns.append(f"User: {q}")
                prompt_with_history = "\n".join(prev_turns)

        res = self.llm.generate(prompt_with_history, system_prompt=system_instruction, max_tokens=2048)
        if res and not res.startswith("[Ollama Connection Error") and not res.startswith("[Offline"):
            clean = _CLEAN_ANSWER_RE.sub('', res).strip()
            self._cache_set(ql, clean)
            return clean

        fallback_msg = "Nexus is operating in 100% offline air-gapped mode. I can assist you with system controls, coding, science, mathematics, offline research, and local files."
        return fallback_msg

    def process_request_stream(self, user_query: str, history: Optional[List[Dict[str, str]]] = None) -> Generator[str, None, None]:
        q = user_query.strip()
        ql = q.lower()

        if not ql:
            yield "Listening. Say or type a command."
            return

        norm_q = self._normalize_query(q)
        norm_ql = norm_q.lower()

        active_history = history if history is not None else self.session_history

        human_res = self.human_engine.handle_conversational_query(q, history=active_history) or self.human_engine.handle_conversational_query(norm_q, history=active_history)
        if human_res:
            self._record_turn("user", q)
            self._record_turn("assistant", human_res)
            yield human_res
            return

        if self._is_greeting(ql) or self._is_greeting(norm_ql):
            ans = "Hey! Nexus here, running fully offline and ready to collaborate. What are we building or exploring today?"
            self._record_turn("user", q)
            self._record_turn("assistant", ans)
            yield ans
            return

        if any(target in ql or target in norm_ql for target in ["who are you", "what are you", "what is your name", "who made you", "who created you", "who built you", "tell me about yourself"]):
            ans = self.human_engine.identity_explanation
            self._record_turn("user", q)
            self._record_turn("assistant", ans)
            yield ans
            return

        if any(ql.startswith(w) or norm_ql.startswith(w) for w in ["how are you", "are you ready", "are you online", "status", "are you working"]):
            ans = "Doing great! All local neural engines, compilers, and knowledge graphs are loaded and responsive. What's on your mind?"
            self._record_turn("user", q)
            self._record_turn("assistant", ans)
            yield ans
            return

        if ql in ["thank you", "thanks", "thanks grok", "thanks jarvis", "appreciate it"]:
            ans = "You're very welcome! Always here whenever you need code, an architecture review, or a deep dive."
            self._record_turn("user", q)
            self._record_turn("assistant", ans)
            yield ans
            return

        if ql in ["help", "what can you do", "commands", "menu"]:
            ans = "Capabilities: 100% offline neural AI assistant, full OS machine control (open/close apps, volume, mute, lock, network, WoL), 370+ scientific & coding dossiers, polyglot vibe coding partner, local python sandbox, crypto wallet, and MongoDB sync."
            self._record_turn("user", q)
            self._record_turn("assistant", ans)
            yield ans
            return

        if any(w in ql or w in norm_ql for w in ["can you write code", "can you code", "can i vibe code", "can you vibe code", "what languages do you support", "can you program"]):
            ans = "Yes, I am a fully equipped polyglot software engineering agent and interactive vibe coding partner. I support full-stack application development, algorithms, refactoring, debugging, error handling, and test suites across Python, C++, Rust, Go, JavaScript, TypeScript, Java, and SQL - 100% offline."
            self._record_turn("user", q)
            self._record_turn("assistant", ans)
            yield ans
            return

        math_res = self._solve_math(q) or self._solve_math(norm_q)
        if math_res is not None:
            ans = f"{math_res}"
            self._cache_set(ql, ans)
            yield ans
            return

        is_coding = self._is_coding_request(q, ql) or self._is_coding_request(norm_q, norm_ql)

        if not is_coding:
            fast_keywords = [
                "mute", "silence audio", "unmute", "volume up", "increase volume", "louder",
                "volume down", "decrease volume", "lower volume", "quieter", "lock computer",
                "lock pc", "lock screen", "lock workstation", "minimize windows", "minimize all",
                "show desktop", "empty recycle bin", "clean recycle bin", "what is my ip",
                "my ip", "ip address", "network info", "network status", "ping ",
                "set mode to ", "switch mode to ", "run code:", "python:", "execute code:",
                "generate image", "create graphic", "draw ", "render image",
                "search web", "look up", "google ", "browse web", "latest news",
                "wake on lan", "wol", "open computer", "open the computer", "wake computer", "power on",
                "schedule wake", "wake at", "sleep computer", "suspend machine",
                "system status", "system telemetry", "hardware status", "pc specs", "ram usage", "battery",
                "screenshot", "capture display", "capture screen", "run powershell ", "powershell ",
                "run cmd ", "cmd ", "open ", "launch ", "start ", "close ", "kill ", "terminate ",
                "type ", "create file ", "delete file ", "remove file ", "create folder ",
                "list files", "dir", "list processes", "wallet", "balance", "crypto balance",
                "my address", "send ", "transfer ", "pay ", "transaction history", "ledger",
                "sync mongodb", "sync to mongodb", "put files in mongodb", "put my files in mongodb",
                "save to mongodb", "backup to mongodb", "mongodb status", "check mongodb",
                "research ", "deep dive", "compare ", "offline research"
            ]
            if any(w in ql for w in fast_keywords):
                yield self.process_request(user_query, history)
                return

        vibe_res = self.code_engine.process_vibe_request(q) or self.code_engine.process_vibe_request(norm_q)
        if vibe_res:
            self._cache_set(ql, vibe_res)
            yield vibe_res
            return

        code_match = self.code_engine.search_code(norm_q) or self.code_engine.search_code(q)
        if code_match:
            res = self.code_engine.format_solution(code_match)
            self._cache_set(ql, res)
            yield res
            return

        if ql in self.response_cache:
            yield self.response_cache[ql]
            return

        if not is_coding:
            omni_match = self.omni.search(norm_q) or self.omni.search(q)
            if omni_match:
                res = self.omni.synthesize_explanation(q, matched_topic=omni_match)
                self._cache_set(ql, res)
                yield res
                return

            matched_domains = self.knowledge.query(norm_q, top_k=3) or self.knowledge.query(q, top_k=3)
            if matched_domains:
                top_d = matched_domains[0]
                sec_d = matched_domains[1] if len(matched_domains) > 1 else None
                if any(w in ql for w in ["research", "deep dive", "details", "formula", "math", "dossier"]):
                    res = self.knowledge.deep_research(top_d.get("name"))["markdown"]
                    self._cache_set(ql, res)
                    yield res
                    return
                exp_lines = [
                    f"### 💡 {top_d.get('name')} ({top_d.get('category')})\n",
                    f"**Core Concept & Mechanism:**\n{top_d.get('concept')}\n",
                    f"**Scientific & Mathematical Foundation:**\n```text\n{top_d.get('mathematical_basis')}\n```\n",
                    f"**Key Insights & Edge Invariants:**\n{top_d.get('obscure_insights')}\n",
                    f"**Frameworks & Implementations:**\n`{top_d.get('open_source_frameworks')}`\n"
                ]
                if sec_d:
                    exp_lines.append(f"\n---\n**🔗 Cross-Domain Correlated Field:** #{sec_d.get('id')} {sec_d.get('name')} ({sec_d.get('category')})\n{sec_d.get('concept')}")
                res = "\n".join(exp_lines)
                self._cache_set(ql, res)
                yield res
                return

        if is_coding:
            system_instruction = (
                "You are an expert polyglot software engineer and principal systems architect. "
                "Write clean, elegant, production-grade code in the requested programming language. "
                "Explain the architecture, design choices, edge cases, and time/space complexity with clarity and precision."
            )
        else:
            system_instruction = (
                "You are Nexus, an elite autonomous AI companion and scientific polymath. "
                "Communicate with the warmth, intellectual depth, sharp wit, and clarity of a world-class human collaborator. "
                "Explain concepts using first-principles reasoning and intuitive mental models. "
                "Never use robotic corporate filler or disclaimers. Answer directly, thoroughly, and engagingly."
            )

        prompt_with_history = q
        hist_to_use = history if history is not None else self.session_history
        if hist_to_use:
            prev_turns = []
            for msg in hist_to_use[-6:]:
                role = "User" if msg.get("role") == "user" else "Assistant"
                content = msg.get("content", "").strip()
                if content and content != q:
                    prev_turns.append(f"{role}: {content[:300]}")
            if prev_turns:
                prev_turns.append(f"User: {q}")
                prompt_with_history = "\n".join(prev_turns)

        prefix_buffer = []
        prefix_cleared = False
        full_tokens = []
        for chunk in self.llm.generate_stream(prompt_with_history, system_prompt=system_instruction, max_tokens=2048):
            full_tokens.append(chunk)
            if not prefix_cleared:
                prefix_buffer.append(chunk)
                buffered_text = "".join(prefix_buffer)
                if len(buffered_text) >= 25 or ":" in buffered_text or "\n" in buffered_text:
                    cleaned_start = _CLEAN_ANSWER_RE.sub('', buffered_text)
                    prefix_cleared = True
                    if cleaned_start:
                        yield cleaned_start
            else:
                if chunk:
                    yield chunk

        if not prefix_cleared and prefix_buffer:
            yield _CLEAN_ANSWER_RE.sub('', "".join(prefix_buffer))

        if full_tokens:
            full_ans = "".join(full_tokens).strip()
            self._record_turn("user", q)
            self._record_turn("assistant", full_ans)
            self._cache_set(ql, full_ans)
            return

        fallback_msg = "Nexus is operating in 100% offline air-gapped mode. I can assist you with system controls, coding, science, mathematics, offline research, and local files."
        self._record_turn("user", q)
        self._record_turn("assistant", fallback_msg)
        yield fallback_msg
