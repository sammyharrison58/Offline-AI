# ⚡ NEXUS-226: Autonomous Offline AI System

An open-source, unlimited, air-gapped autonomous AI framework designed to run completely offline on local hardware. 

## 🌟 Key Capabilities

1. **High-End 226 AI Domain Knowledge Base**:
   - Covers 226 specialized, frontier, and obscure AI paradigms (Liquid Neural Networks, Kolmogorov-Arnold Networks (KAN), Spiking Neuromorphic SNNs, Continuous Hopfield Networks, Diffusion Flow Matching, MuZero/DreamerV3, zkML, Hyperdimensional Computing, etc.).
   - Indexed for instant sub-millisecond retrieval with exact mathematical formulations and open-source references.

2. **Unlimited Open-Source Local Engine**:
   - Zero censorship, zero subscription limits, and 100% offline.
   - Automatically attaches to local **Ollama** models (e.g. `llama3.2:1b`, `llama3.2:3b`, `qwen2.5`) or LM Studio/vLLM.
   - Includes a native built-in Neuro-Symbolic reasoning engine for systems without heavy GPU compute.

3. **Total Machine & OS Control ("Operate Everything")**:
   - Direct PowerShell and Windows command prompt execution.
   - Process inspection, memory monitoring, and application launching (`notepad.exe`, `terminal`, etc.).
   - Screen capture and GUI automation (mouse clicks, keyboard strokes).
   - Machine power & boot orchestration:
     - **Wake-on-LAN (WoL)**: Broadcasts UDP Magic Packets to power on and wake computers across the local network.
     - **RTC Auto-Wake Timer**: Schedules hardware wake alarms to power on the machine automatically.
     - System sleep and reboot management.

4. **Autonomous Blockchain & Transaction Engine**:
   - Cryptographic keystore generation (BIP-39 compatible, secp256k1 derivation).
   - Local verifiable proof-of-work blockchain ledger (`data/blockchain_ledger.json`).
   - Offline transaction creation, cryptographic signing, and local block mining.

5. **Always-On Duplex Voice Call Mode**:
   - Acts like a live phone call conversation (`python main.py --mode voice`).
   - Uses zero-latency offline Windows SAPI5 voice synthesis.
   - Listens continuously until explicit hang-up ("hang up", "exit", or "shut down").

---

## 🚀 Quick Start Guide

### 1. Launch Voice Call Mode ("Always On Call")
```bash
python main.py --mode voice
```
*Engages an open audio conversation line through your speakers/mic.*

### 2. Launch Interactive CLI Terminal
```bash
python main.py --mode text
```

### 3. Launch Streamlit Web Cockpit
```bash
python main.py --mode gui
# Or run directly:
streamlit run web_ui.py
```

### 4. Single-Shot Command Execution
```bash
python main.py "Explain Kolmogorov-Arnold Networks"
python main.py "Check my wallet balance and address"
python main.py "run powershell Get-Process | Select -First 5"
python main.py "Wake computer with MAC 00:11:22:33:44:55"
python main.py "Transfer 10 tokens to 0x71C8360537B882E130420666060021b59E874da7"
```

---

## 📁 Architecture Layout

- `core/agent.py`: Unified ReAct orchestrator connecting knowledge, OS tools, and blockchain.
- `core/knowledge_base.py`: 226 AI domain catalog and mathematical search engine.
- `core/system_controller.py`: Machine execution, Wake-on-LAN, and GUI automation.
- `core/blockchain_manager.py`: Cryptographic wallet and verifiable block ledger.
- `core/llm_engine.py`: Local Ollama, GGUF, and offline reasoning dispatcher.
- `core/voice_loop.py`: Conversational voice engine and call session loop.
- `web_ui.py`: Full graphical dashboard for browser-based control.
- `data/ai_knowledge_226.json`: Database of 226 AI fields and equations.
- `wallets/`: Secure local encrypted keystore directory.

