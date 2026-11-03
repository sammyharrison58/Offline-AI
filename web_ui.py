"""
Nexus-226 Autonomous Offline AI - Web Management Dashboard & Cockpit
Interactive Streamlit interface for Machine Control, 226 AI Knowledge,
Blockchain Transactions, and Voice Interaction.
"""
import os
import sys
import time
import json
import streamlit as st

# Add workspace to path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from core.agent import Nexus226Agent
from core.voice_loop import OfflineVoiceEngine

st.set_page_config(
    page_title="Nexus-226 Autonomous Offline AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #4F46E5; margin-bottom: 0px; }
    .sub-header { color: #64748B; font-size: 1.05rem; margin-bottom: 20px; }
    .card { background-color: #1E293B; border-radius: 8px; padding: 15px; border: 1px solid #334155; margin-bottom: 12px; }
    .stButton>button { border-radius: 6px; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_agent():
    return Nexus226Agent()

@st.cache_resource
def get_voice():
    return OfflineVoiceEngine()

agent = get_agent()
voice = get_voice()

# -----------------------------------------------------------------
# Sidebar: Telemetry & Status
# -----------------------------------------------------------------
st.sidebar.markdown("### ⚡ System Cockpit")
telemetry = agent.sys_controller.get_telemetry()
wallet_bal = agent.blockchain.get_balance()

st.sidebar.metric("CPU Usage", f"{telemetry['cpu_usage_percent']}%")
st.sidebar.metric("RAM Available", f"{telemetry['ram_available_gb']} GB / {telemetry['ram_total_gb']} GB")
st.sidebar.metric("Battery", f"{telemetry['battery']['percent']}%")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**AI Engine Backend:** `{agent.llm.active_backend}`")
if agent.llm.active_backend == "ollama":
    st.sidebar.markdown(f"**Local Model:** `{agent.llm.ollama_model}`")

st.sidebar.markdown(f"**Autonomous Wallet:**")
st.sidebar.code(wallet_bal['address'], language="text")
st.sidebar.markdown(f"**Treasury Balance:** `{wallet_bal['balance']} AETH`")

voice_enabled = st.sidebar.checkbox("🔊 Speak Responses Aloud (SAPI Voice)", value=True)

# -----------------------------------------------------------------
# Main Navigation Tabs & Master Power Switch
# -----------------------------------------------------------------
st.markdown('<div class="main-header">⚡ NEXUS-226 Offline Autonomous AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Unlimited Open-Source Local Agent | Machine Control | 226 AI Paradigms | Verifiable Ledger</div>', unsafe_allow_html=True)

# Master Start/Stop System State
if "system_active" not in st.session_state:
    st.session_state.system_active = True

# Prominent Start / Stop Control Banner
st.markdown("---")
col_status, col_btn_start, col_btn_stop = st.columns([2, 1, 1])

with col_status:
    if st.session_state.system_active:
        st.markdown("### 🟢 **SYSTEM STATUS: ONLINE**\n*All 226 AI modules, OS tools, and Voice listening active.*")
    else:
        st.markdown("### 🔴 **SYSTEM STATUS: STOPPED**\n*All autonomous agent loops and voice execution paused.*")

with col_btn_start:
    if st.button("▶ START SYSTEM", type="primary", use_container_width=True):
        st.session_state.system_active = True
        st.success("Nexus-226 activated! All subsystems online.")
        voice.speak("Nexus-226 system activated and online.", block=False)
        st.rerun()

with col_btn_stop:
    if st.button("⏹ STOP SYSTEM", use_container_width=True):
        st.session_state.system_active = False
        st.warning("Nexus-226 paused! Subsystems stopped.")
        voice.speak("Nexus-226 system stopped.", block=False)
        st.rerun()

st.markdown("---")

tab_chat, tab_knowledge, tab_system, tab_blockchain = st.tabs([
    "💬 Voice & Text Call Console",
    "🧠 226 AI Knowledge Core",
    "💻 OS & Machine Control",
    "⛓️ Blockchain & Ledger"
])

# -----------------------------------------------------------------
# Tab 1: Voice & Conversational Chat
# -----------------------------------------------------------------
with tab_chat:
    st.markdown("#### Real-Life Conversational Interface (Always-On Mode)")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Nexus online. All 226 AI domains and machine control interfaces are operational. How can I assist you?"}
        ]

    # Quick Prompts
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("📊 System Telemetry"):
            st.session_state.user_query = "What is the current system telemetry and hardware status?"
    with c2:
        if st.button("💰 Wallet Balance"):
            st.session_state.user_query = "What is my blockchain wallet balance and address?"
    with c3:
        if st.button("📸 Capture Screenshot"):
            st.session_state.user_query = "Take a screenshot of the computer screen"
    with c4:
        if st.button("🧬 Liquid Neural Nets"):
            st.session_state.user_query = "Explain Liquid Neural Networks and their mathematical basis"

    # Display Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # User Input
    user_input = st.chat_input("Speak or type a command to Nexus-226...")
    if "user_query" in st.session_state and st.session_state.user_query:
        user_input = st.session_state.user_query
        st.session_state.user_query = None

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            if not st.session_state.system_active:
                response = "🛑 Nexus-226 is currently STOPPED. Click the green '▶ START SYSTEM' button above to reactivate autonomous operations."
                st.warning(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                with st.spinner("Processing request and orchestrating tools..."):
                    response = agent.process_request(user_input)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

                    if voice_enabled:
                        voice.speak(response, block=False)

# -----------------------------------------------------------------
# Tab 2: 226 AI Knowledge Core
# -----------------------------------------------------------------
with tab_knowledge:
    st.markdown("#### Comprehensive 226 AI Architecture & Mathematical Ontology")
    st.markdown("Indexed offline reference covering obscure, frontier, and foundational AI systems.")

    search_kw = st.text_input("🔍 Search across 226 AI topics (e.g. 'Mamba', 'KAN', 'zkML', 'MuZero', 'Hopfield'):", "")
    
    cats = list(agent.knowledge.get_category_summary().keys())
    selected_cat = st.selectbox("Filter by Category", ["All Categories"] + cats)

    domains = agent.knowledge.domains
    if selected_cat != "All Categories":
        domains = [d for d in domains if d.get("category") == selected_cat]

    if search_kw:
        matched = agent.knowledge.query(search_kw, top_k=15)
        domains = [d for d in matched if (selected_cat == "All Categories" or d.get("category") == selected_cat)]

    st.markdown(f"**Showing {len(domains)} AI Subfields:**")

    for d in domains[:20]:
        with st.expander(f"#{d['id']}: {d['name']} ({d['category']})"):
            st.markdown(f"**Concept:** {d['concept']}")
            st.markdown(f"**Mathematical Formulation:** `{d['mathematical_basis']}`")
            st.markdown(f"**Obscure Insights:** {d['obscure_insights']}")
            st.markdown(f"**Open Source Implementation:** `{d['open_source_frameworks']}`")

# -----------------------------------------------------------------
# Tab 3: OS & Machine Control
# -----------------------------------------------------------------
with tab_system:
    st.markdown("#### Operating System & Hardware Automation")

    col_pwr, col_shell = st.columns([1, 1])

    with col_pwr:
        st.markdown("##### 🔌 Machine Power & Boot Control ('Open the Computer')")
        mac_addr = st.text_input("Wake-on-LAN MAC Address:", "00:1A:2B:3C:4D:5E")
        if st.button("📡 Broadcast Wake-on-LAN Magic Packet"):
            res = agent.sys_controller.send_wake_on_lan(mac_addr)
            st.success(res.get("message", str(res)))

        st.markdown("---")
        wake_time = st.text_input("Schedule Auto-Wake Alarm (HH:MM):", "07:30")
        if st.button("⏰ Set Hardware Wake Alarm"):
            res = agent.sys_controller.schedule_wake_timer(wake_time)
            st.success(res.get("message"))

        st.markdown("---")
        st.markdown("##### 📸 Screen Duplication")
        if st.button("Take Instant Screenshot"):
            res = agent.sys_controller.capture_screenshot("ui_screenshot.png")
            if res.get("success"):
                st.image("ui_screenshot.png", caption="Current Desktop View", use_column_width=True)

    with col_shell:
        st.markdown("##### ⚡ Terminal & PowerShell Automation")
        ps_cmd = st.text_area("PowerShell Script:", "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object -First 10")
        if st.button("▶️ Execute PowerShell"):
            res = agent.sys_controller.run_powershell(ps_cmd)
            if res.get("success"):
                st.code(res.get("stdout") or "[Success with empty output]", language="powershell")
            else:
                st.error(res.get("stderr") or res.get("error"))

        st.markdown("---")
        st.markdown("##### 🚀 Application Launcher")
        app_to_launch = st.text_input("Executable / Command to launch:", "notepad.exe")
        if st.button("Launch App"):
            res = agent.sys_controller.launch_app(app_to_launch)
            st.info(str(res))

# -----------------------------------------------------------------
# Tab 4: Blockchain & Verifiable Ledger
# -----------------------------------------------------------------
with tab_blockchain:
    st.markdown("#### Autonomous Cryptographic Treasury & Ledger")

    col_tx, col_blocks = st.columns([1, 1])

    with col_tx:
        st.markdown("##### 💸 Send Autonomous Transaction")
        to_addr = st.text_input("Recipient EVM Address:", "0x71C8360537B882E130420666060021b59E874da7")
        amt = st.number_input("Amount (AETH):", min_value=0.1, max_value=1000.0, value=10.0, step=1.0)
        memo = st.text_input("Transaction Memo:", "Autonomous Edge Compute Allocation")

        if st.button("🔏 Sign & Mine Transaction"):
            res = agent.blockchain.create_and_sign_transaction(to_addr, amt, memo)
            if res.get("success"):
                st.success(f"Transaction Mined into Block #{res['block_index']}!")
                st.json(res)
            else:
                st.error(res.get("error"))

    with col_blocks:
        st.markdown("##### 📜 Recent Blocks in Ledger")
        st.markdown(f"Total Blocks: `{len(agent.blockchain.ledger)}`")
        for blk in reversed(agent.blockchain.ledger[-5:]):
            with st.expander(f"Block #{blk['block_index']} | Hash: {blk['block_hash'][:16]}..."):
                st.markdown(f"**Timestamp:** {time.ctime(blk['timestamp'])}")
                st.markdown(f"**Nonce:** `{blk['nonce']}`")
                st.markdown(f"**Previous Hash:** `{blk['previous_hash'][:24]}...`")
                st.markdown(f"**Transactions ({len(blk.get('transactions', []))}):**")
                for t in blk.get("transactions", []):
                    st.code(f"{t.get('amount')} AETH -> {t.get('to')}\nTx: {t.get('tx_hash')}", language="text")

