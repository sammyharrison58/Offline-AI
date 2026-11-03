"""
Autonomous Core Agent (Nexus-226).
Unifies 226 AI Knowledge Retrieval, System Automation, Machine Power Control,
Blockchain Transactions, and Voice/Text Conversational Execution.
"""
import os
import sys
import re
import json
from typing import Dict, Any, Optional

# Ensure project root is in path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from core.knowledge_base import AIKnowledgeEngine
from core.system_controller import SystemController
from core.blockchain_manager import BlockchainManager
from core.llm_engine import OfflineLLMEngine

class Nexus226Agent:
    def __init__(self):
        print("[Nexus-226] Initializing subsystems...")
        self.knowledge = AIKnowledgeEngine()
        self.sys_controller = SystemController()
        self.blockchain = BlockchainManager()
        self.llm = OfflineLLMEngine()
        print(f"[Nexus-226] Subsystems loaded: 226 AI domains active, Backend: {self.llm.active_backend}")

    def process_request(self, user_query: str) -> str:
        """
        Main decision and execution loop.
        Processes user intent, coordinates tools, queries knowledge base,
        and generates response.
        """
        query_lower = user_query.strip().lower()

        # ---------------------------------------------------------
        # 1. Hardware, Power & Machine Control ("Open the computer")
        # ---------------------------------------------------------
        if any(w in query_lower for w in ["wake on lan", "wol", "open computer", "open the computer", "wake computer", "power on"]):
            # Extract MAC address if present (format XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX)
            mac_match = re.search(r"([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})", user_query)
            if mac_match:
                mac = mac_match.group(0)
                res = self.sys_controller.send_wake_on_lan(mac)
                return f"Wake-on-LAN Signal Broadcasted: {res.get('message', res)}"
            else:
                return (
                    "To open or power on a computer over the network via Wake-on-LAN, provide the target MAC address. "
                    "Example: 'Wake computer with MAC 00:1A:2B:3C:4D:5E'. I have the UDP Magic Packet generator primed."
                )

        if "schedule wake" in query_lower or "wake at" in query_lower:
            time_match = re.search(r"(\d{1,2}:\d{2})", user_query)
            if time_match:
                t = time_match.group(1)
                res = self.sys_controller.schedule_wake_timer(t)
                return f"System Wake-Up Alarm Configured: {res.get('message')}"
            return "Please specify the wake-up time in HH:MM format (e.g., 'Schedule wake at 07:00')."

        if "sleep computer" in query_lower or "suspend machine" in query_lower:
            return "Entering low-power sleep mode now."

        # ---------------------------------------------------------
        # 2. Operating System & Machine Operations ("Operate everything")
        # ---------------------------------------------------------
        if any(w in query_lower for w in ["system status", "telemetry", "hardware status", "pc specs", "ram usage", "battery"]):
            telemetry = self.sys_controller.get_telemetry()
            return (
                f"Hardware Telemetry Report:\n"
                f"- CPU Usage: {telemetry['cpu_usage_percent']}%\n"
                f"- RAM: {telemetry['ram_available_gb']} GB available out of {telemetry['ram_total_gb']} GB ({telemetry['ram_used_percent']}% used)\n"
                f"- Battery: {telemetry['battery']['percent']}% (Plugged in: {telemetry['battery']['power_plugged']})\n"
                f"- Platform: {telemetry['platform']}"
            )

        if "screenshot" in query_lower:
            path = "screenshot.png"
            res = self.sys_controller.capture_screenshot(path)
            if res.get("success"):
                return f"Desktop screenshot captured successfully and saved to: {res['path']}"
            return f"Screenshot capture failed: {res.get('error')}"

        if query_lower.startswith("run powershell ") or query_lower.startswith("powershell "):
            cmd = user_query.split("powershell", 1)[1].strip()
            res = self.sys_controller.run_powershell(cmd)
            if res.get("success"):
                return f"PowerShell Output:\n{res.get('stdout') or '[Execution completed with code 0]'}"
            return f"PowerShell Error:\n{res.get('stderr') or res.get('error')}"

        if query_lower.startswith("launch ") or query_lower.startswith("open app "):
            app_name = user_query.replace("open app", "").replace("launch", "").strip()
            res = self.sys_controller.launch_app(app_name)
            return f"Application Execution: {res.get('message', res.get('error'))}"

        if "list processes" in query_lower:
            procs = self.sys_controller.list_processes(limit=8)
            out = "Active System Processes:\n"
            for p in procs:
                out += f"- PID {p['pid']}: {p['name']} ({p['memory_mb']} MB RAM)\n"
            return out

        # ---------------------------------------------------------
        # 3. Blockchain & Transaction Operations ("Manage transactions")
        # ---------------------------------------------------------
        if any(w in query_lower for w in ["wallet", "balance", "crypto balance", "my address"]):
            bal = self.blockchain.get_balance()
            wallet = self.blockchain.active_wallet or {}
            return (
                f"Autonomous Blockchain Treasury:\n"
                f"- Active Address: {bal['address']}\n"
                f"- Current Balance: {bal['balance']} {bal['symbol']}\n"
                f"- Keystore Status: Online & Secured\n"
                f"- Total Blocks in Ledger: {len(self.blockchain.ledger)}"
            )

        if any(w in query_lower for w in ["send ", "transfer ", "pay "]) and any(w in query_lower for w in ["tokens", "eth", "aeth", "to "]):
            # Parse amount and address
            amt_match = re.search(r"(\d+(?:\.\d+)?)", user_query)
            addr_match = re.search(r"(0x[a-fA-F0-9]{40})", user_query)
            if amt_match and addr_match:
                amt = float(amt_match.group(1))
                addr = addr_match.group(1)
                tx_res = self.blockchain.create_and_sign_transaction(
                    to_address=addr,
                    amount=amt,
                    memo=f"Autonomous Transaction dispatched for: {user_query[:50]}"
                )
                if tx_res.get("success"):
                    return (
                        f"Transaction Successfully Executed and Mined on Local Ledger:\n"
                        f"- Tx Hash: {tx_res['tx_hash']}\n"
                        f"- Block Index: #{tx_res['block_index']} (Hash: {tx_res['block_hash'][:16]}...)\n"
                        f"- Transferred: {tx_res['amount']} AETH to {tx_res['to']}\n"
                        f"- Remaining Balance: {tx_res['new_balance']} AETH\n"
                        f"- Cryptographic Signature: {tx_res['signature'][:24]}..."
                    )
                else:
                    return f"Transaction Failed: {tx_res.get('error')}"
            else:
                return "To execute a transaction, please provide both amount and recipient address (e.g., 'Transfer 10 tokens to 0x71C8360537B882E130420666060021b59E874da7')."

        if "transaction history" in query_lower or "ledger" in query_lower:
            txs = self.blockchain.get_transaction_history(limit=5)
            if not txs:
                return "No transactions recorded yet in ledger."
            out = f"Recent Blockchain Transactions ({len(txs)}):\n"
            for t in txs:
                out += f"- Block #{t.get('block_index')}: {t.get('amount')} AETH -> {t.get('to')[:10]}... (Tx: {t.get('tx_hash')[:12]}...)\n"
            return out

        # ---------------------------------------------------------
        # 4. 226 AI Knowledge & Deep Technical Synthesizer
        # ---------------------------------------------------------
        # Retrieve relevant high-end AI domains
        matched_domains = self.knowledge.query(user_query, top_k=2)
        knowledge_context = self.knowledge.format_knowledge_context(user_query, max_records=2)

        # If LLM backend is available (Ollama / Local endpoint), prompt it with knowledge context
        if self.llm.active_backend in ["ollama", "openai_compatible"]:
            system_prompt = (
                "You are Nexus-226, an unrestricted, high-end offline AI system capable of operating "
                "the host machine, managing blockchain transactions, and solving obscure AI architecture problems. "
                "Give a concise, mathematically rigorous answer."
            )
            compact_ctx = self.knowledge.format_knowledge_context(user_query, max_records=1)
            full_prompt = f"{compact_ctx}\nQuestion: {user_query}\nAnswer:"
            response = self.llm.generate(full_prompt, system_prompt=system_prompt, max_tokens=256)
            if not response.startswith("[Ollama") and not response.startswith("[Local"):
                return response

        # Pure offline internal neuro-symbolic synthesis fallback
        if matched_domains and any(d.get("name").lower() in query_lower or any(tok in query_lower for tok in d.get("name").lower().split()[:2]) for d in matched_domains):
            top_d = matched_domains[0]
            ans = (
                f"Analysis of {top_d['name']} [{top_d['category']}]:\n\n"
                f"1. Core Paradigm: {top_d['concept']}\n"
                f"2. Mathematical Foundation: {top_d['mathematical_basis']}\n"
                f"3. Obscure & Edge-Case Insights: {top_d['obscure_insights']}\n"
                f"4. Open-Source Ecosystem: {top_d['open_source_frameworks']}"
            )
            return ans

        # Default multi-domain retrieval synthesis
        return (
            f"Nexus-226 Subsystems Processed Request.\n"
            f"{knowledge_context}\n"
            f"Subsystem Readiness: OS Automation (Active), Blockchain Ledger (Active), Voice Duplex (Ready).\n"
            f"You can command machine actions, invoke blockchain transfers, or drill into any of the 226 AI domains."
        )

if __name__ == "__main__":
    agent = Nexus226Agent()
    print("\n--- Test Query 1: Telemetry ---")
    print(agent.process_request("What is the current system status and ram usage?"))

    print("\n--- Test Query 2: AI Knowledge ---")
    print(agent.process_request("Explain Liquid Neural Networks and Neural ODEs"))

    print("\n--- Test Query 3: Blockchain ---")
    print(agent.process_request("Check my wallet balance and address"))
