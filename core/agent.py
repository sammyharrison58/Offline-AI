import os
import sys
import re
import json
from typing import Dict, Any, Optional

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from core.knowledge_base import AIKnowledgeEngine
from core.system_controller import SystemController
from core.blockchain_manager import BlockchainManager
from core.llm_engine import OfflineLLMEngine
from core.grok_engine import GrokEngine

class Nexus226Agent:

    def __init__(self):
        self.knowledge = AIKnowledgeEngine()
        self.sys_controller = SystemController()
        self.blockchain = BlockchainManager()
        self.llm = OfflineLLMEngine()
        self.grok = GrokEngine(mode="fun")

    def process_request(self, user_query: str) -> str:
        q = user_query.strip()
        ql = q.lower()

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

        if "screenshot" in ql:
            path = "screenshot.png"
            res = self.sys_controller.capture_screenshot(path)
            if res.get("success"):
                return f"Screenshot captured: {res['path']}"
            return f"Screenshot error: {res.get('error')}"

        if ql.startswith("run powershell ") or ql.startswith("powershell "):
            cmd = q.split("powershell", 1)[1].strip()
            res = self.sys_controller.run_powershell(cmd)
            return res.get("stdout") or res.get("stderr") or "[Executed]"

        if ql.startswith("launch ") or ql.startswith("open app "):
            app = q.replace("open app", "").replace("launch", "").strip()
            res = self.sys_controller.launch_app(app)
            return str(res.get("message", res.get("error")))

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

        matched_domains = self.knowledge.query(q, top_k=1)
        k_ctx = ""
        if matched_domains and any(tok in ql for tok in matched_domains[0].get("name").lower().split()[:2]):
            d = matched_domains[0]
            k_ctx = f"Domain reference: {d['name']}. {d['concept']} Math: {d['mathematical_basis']}."

        system_instruction = (
            f"You are Grok. Mode: {self.grok.mode}. "
            "Give a direct, witty, intelligent, and accurate answer in 2-3 sentences. No fluff."
        )
        user_prompt = f"{k_ctx}\nUser Question: {q}\nAnswer:" if k_ctx else q

        if self.llm.active_backend in ["ollama", "openai_compatible"]:
            res = self.llm.generate(user_prompt, system_prompt=system_instruction, max_tokens=100)
            if res and not res.startswith("[Ollama") and not res.startswith("[Local"):
                return res

        if k_ctx:
            return f"{matched_domains[0]['name']}: {matched_domains[0]['concept']}\nFormulation: {matched_domains[0]['mathematical_basis']}"

        if "who are you" in ql or "what are you" in ql:
            return "I am Nexus-Grok, your uncensored offline autonomous AI agent equipped with 226 AI architecture paradigms, OS machine controls, blockchain treasury, and voice duplex."

        if "hello" in ql or "hi" in ql or "hey" in ql:
            return "Greetings! Nexus-Grok online and listening. Ask me any question, run code, or command machine actions."

        return f"Query analyzed: '{q}'. All systems active. Ask technical questions, request code execution with 'python: ...', or command machine automation."
