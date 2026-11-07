import os
import sys
import re
import json
from typing import Dict, Any, Optional, Generator

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from core.knowledge_base import AIKnowledgeEngine
from core.system_controller import SystemController
from core.blockchain_manager import BlockchainManager
from core.llm_engine import OfflineLLMEngine
from core.grok_engine import GrokEngine
from core.mongo_manager import MongoDBManager

class Nexus226Agent:

    def __init__(self):
        self.knowledge = AIKnowledgeEngine()
        self.sys_controller = SystemController()
        self.blockchain = BlockchainManager()
        self.llm = OfflineLLMEngine()
        self.grok = GrokEngine(mode="fun")
        self.mongo = MongoDBManager()

    def _is_greeting(self, ql: str) -> bool:
        clean = re.sub(r'[^a-z0-9\s]', ' ', ql).strip()
        words = clean.split()
        if not words:
            return False
        greeting_exact = {"hello", "hi", "hey", "howdy", "greetings", "yo", "jarvis", "nexus"}
        if clean in greeting_exact:
            return True
        if any(g in clean for g in ["good morning", "good afternoon", "good evening", "wake up"]):
            return True
        if words[0] in {"hello", "hi", "hey", "greetings", "yo"}:
            return True
        if len(words) <= 3 and any(w in greeting_exact for w in words):
            return True
        return False

    def process_request(self, user_query: str) -> str:
        q = user_query.strip()
        ql = q.lower()

        if not ql:
            return "Listening. Say or type a command."

        if self._is_greeting(ql):
            return "Greetings! Nexus-Jarvis online and listening. Ready for your command."

        if any(ql == w or ql == f"{w} grok" or ql == f"{w} nexus" for w in ["who are you", "what are you", "what is your name"]):
            return "I am Nexus-Grok, your uncensored offline autonomous AI agent equipped with 226 AI architecture paradigms, OS machine controls, blockchain treasury, and voice duplex."

        if any(ql.startswith(w) for w in ["how are you", "are you ready", "are you online", "status", "are you working"]):
            return "All systems operational and hot in memory. Ready for commands or complex inquiries."

        if ql in ["thank you", "thanks", "thanks grok", "appreciate it"]:
            return "You're welcome! Ready for the next command."

        if ql in ["help", "what can you do", "commands", "menu"]:
            return "Capabilities: Full OS control (open/close apps, volume, mute, lock, network, WoL), 226 AI paradigms, live web intelligence, python sandbox, crypto wallet, and MongoDB sync."

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
            web_res = self.grok.search_web_or_feed(search_query)
            snippets = "\n".join([f"- {s}" for s in web_res.get("results", [])[:3]])
            return f"Live Intel for '{search_query}':\n{snippets}"

        if any((w in ql for w in ["wake on lan", "wol", "open computer", "open the computer", "wake computer", "power on"])):
            mac_match = re.search("([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})", q)
            if mac_match:
                mac = mac_match.group(0)
                res = self.sys_controller.send_wake_on_lan(mac)
                return f"Wake-on-LAN Signal Broadcasted: {res.get('message', res)}"
            return "Provide target MAC address (e.g. 'Wake computer 00:1A:2B:3C:4D:5E')."

        if "schedule wake" in ql or "wake at" in ql:
            time_match = re.search("(\\d{1,2}:\\d{2})", q)
            if time_match:
                t = time_match.group(1)
                res = self.sys_controller.schedule_wake_timer(t)
                return f"Wake alarm set for {t}."
            return "Specify time in HH:MM format."

        if "sleep computer" in ql or "suspend machine" in ql:
            return "Entering low-power sleep mode."

        if any((w in ql for w in ["system status", "telemetry", "hardware status", "pc specs", "ram usage", "battery"])):
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
            app = re.sub(r"^(open|launch|start)\s+(app\s+)?", "", q, flags=re.IGNORECASE).strip()
            res = self.sys_controller.launch_app(app)
            return str(res.get("message", res.get("error")))

        if any(ql.startswith(p) for p in ["close ", "kill ", "terminate ", "quit "]):
            target = re.sub(r"^(close|kill|terminate|quit)\s+(app\s+)?", "", q, flags=re.IGNORECASE).strip()
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
            f_path = re.sub(r"^(delete file|remove file)\s+", "", q, flags=re.IGNORECASE).strip()
            res = self.sys_controller.delete_file(f_path)
            return res.get("message", str(res))

        if ql.startswith("create folder ") or ql.startswith("make folder ") or ql.startswith("create directory "):
            d_path = re.sub(r"^(create folder|make folder|create directory)\s+", "", q, flags=re.IGNORECASE).strip()
            res = self.sys_controller.create_directory(d_path)
            return res.get("message", str(res))

        if ql.startswith("list files") or ql == "dir":
            res = self.sys_controller.list_dir(".")
            items = ", ".join(res.get("items", [])[:15])
            return f"Files: {items}"

        if "list processes" in ql:
            procs = self.sys_controller.list_processes(limit=6)
            return "\n".join([f"- PID {p['pid']}: {p['name']} ({p['memory_mb']} MB)" for p in procs])

        if any((w in ql for w in ["wallet", "balance", "crypto balance", "my address"])):
            b = self.blockchain.get_balance()
            return f"Treasury: Address {b['address']} | Balance {b['balance']} AETH | Ledger: {len(self.blockchain.ledger)} blocks"

        if any((w in ql for w in ["send ", "transfer ", "pay "])) and any((w in ql for w in ["tokens", "eth", "aeth", "to "])):
            amt_match = re.search("(\\d+(?:\\.\\d+)?)", q)
            addr_match = re.search("(0x[a-fA-F0-9]{40})", q)
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

        matched_domains = self.knowledge.query(q, top_k=1)
        k_ctx = ""
        if matched_domains and any(tok in ql for tok in matched_domains[0].get("name").lower().split()[:2]):
            d = matched_domains[0]
            k_ctx = f"Reference: {d['concept']}"

        system_instruction = (
            f"You are Grok ({self.grok.mode} mode). Direct 1-sentence answer only. "
            "NEVER repeat the question, never say 'You asked', 'According to', or repeat what was read. "
            "Give only the answer."
        )
        user_prompt = f"{k_ctx}\nQuestion: {q}\nDirect Answer:" if k_ctx else f"Question: {q}\nDirect Answer:"

        if self.llm.active_backend in ["ollama", "openai_compatible"]:
            res = self.llm.generate(user_prompt, system_prompt=system_instruction, max_tokens=20)
            if res and not res.startswith("[Ollama") and not res.startswith("[Local"):
                clean = re.sub(r'^(Direct Answer:|Answer:|Grok:|Response:|Question:)\s*', '', res, flags=re.IGNORECASE).strip()
                return clean

        if k_ctx:
            return matched_domains[0]['concept']

        return "Operational. What would you like to explore or execute next?"

    def process_request_stream(self, user_query: str) -> Generator[str, None, None]:
        q = user_query.strip()
        ql = q.lower()

        if not ql:
            yield "Listening. Say or type a command."
            return

        if self._is_greeting(ql):
            yield "Greetings! Nexus-Jarvis online and listening. Ready for your command."
            return

        if any(ql == w or ql == f"{w} grok" or ql == f"{w} nexus" for w in ["who are you", "what are you", "what is your name"]):
            yield "I am Nexus-Grok, your uncensored offline autonomous AI agent equipped with 226 AI architecture paradigms, OS machine controls, blockchain treasury, and voice duplex."
            return

        if any(ql.startswith(w) for w in ["how are you", "are you ready", "are you online", "status", "are you working"]):
            yield "All systems operational and hot in memory. Ready for commands or complex inquiries."
            return

        if ql in ["thank you", "thanks", "thanks grok", "appreciate it"]:
            yield "You're welcome! Ready for the next command."
            return

        if ql in ["help", "what can you do", "commands", "menu"]:
            yield "Capabilities: Full OS control (open/close apps, volume, mute, lock, network, WoL), 226 AI paradigms, live web intelligence, python sandbox, crypto wallet, and MongoDB sync."
            return

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
            "system status", "telemetry", "hardware status", "pc specs", "ram usage", "battery",
            "screenshot", "capture display", "capture screen", "run powershell ", "powershell ",
            "run cmd ", "cmd ", "open ", "launch ", "start ", "close ", "kill ", "terminate ",
            "type ", "create file ", "delete file ", "remove file ", "create folder ",
            "list files", "dir", "list processes", "wallet", "balance", "crypto balance",
            "my address", "send ", "transfer ", "pay ", "transaction history", "ledger",
            "sync mongodb", "sync to mongodb", "put files in mongodb", "put my files in mongodb",
            "save to mongodb", "backup to mongodb", "mongodb status", "check mongodb"
        ]
        if any(w in ql for w in fast_keywords):
            yield self.process_request(user_query)
            return

        matched_domains = self.knowledge.query(q, top_k=1)
        k_ctx = ""
        if matched_domains and any(tok in ql for tok in matched_domains[0].get("name").lower().split()[:2]):
            d = matched_domains[0]
            k_ctx = f"Reference: {d['concept']}"

        system_instruction = (
            f"You are Grok ({self.grok.mode} mode). Direct 1-sentence answer only. "
            "NEVER repeat the question, never say 'You asked', 'According to', or repeat what was read. "
            "Give only the answer."
        )
        user_prompt = f"{k_ctx}\nQuestion: {q}\nDirect Answer:" if k_ctx else f"Question: {q}\nDirect Answer:"

        if self.llm.active_backend in ["ollama", "openai_compatible"]:
            first_chunk = True
            for chunk in self.llm.generate_stream(user_prompt, system_prompt=system_instruction, max_tokens=20):
                if first_chunk:
                    chunk = re.sub(r'^(Direct Answer:|Answer:|Grok:|Response:|Question:)\s*', '', chunk, flags=re.IGNORECASE)
                    first_chunk = False
                if chunk:
                    yield chunk
            return

        yield self.process_request(user_query)
