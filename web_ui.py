import os
import sys
import time
import streamlit as st
import streamlit.components.v1 as components

root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from core.agent import Nexus226Agent
from core.voice_loop import OfflineVoiceEngine

st.set_page_config(
    page_title="Nexus-Grok AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .reportview-container, .main, body {
        background-color: #0B0F19;
        color: #F3F4F6;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6366F1, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .sub-title {
        color: #94A3B8;
        font-size: 1rem;
        margin-bottom: 18px;
    }
    .status-badge-on {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid #059669;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    .status-badge-off {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid #DC2626;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_agent():
    return Nexus226Agent()

@st.cache_resource
def get_voice():
    return OfflineVoiceEngine(voice_speed=3)

agent = get_agent()
voice = get_voice()

if "ai_open" not in st.session_state:
    st.session_state.ai_open = True

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Nexus-Grok online. Audio responses active. Speak into the mic or type any question below."}
    ]

col_hdr, col_pwr = st.columns([3, 1])
with col_hdr:
    st.markdown('<div class="main-title">⚡ NEXUS-GROK AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">226 AI Paradigms | Code Interpreter | Live Web Intel | Machine & Power Control | Audio Enabled</div>', unsafe_allow_html=True)

with col_pwr:
    if st.session_state.ai_open:
        st.markdown('<div class="status-badge-on">● AI OPEN & ACTIVE</div>', unsafe_allow_html=True)
        if st.button("🔴 CLOSE AI", use_container_width=True):
            st.session_state.ai_open = False
            voice.speak("AI power closed. Entering standby.", block=False)
            st.rerun()
    else:
        st.markdown('<div class="status-badge-off">○ AI CLOSED / STANDBY</div>', unsafe_allow_html=True)
        if st.button("🟢 OPEN AI", type="primary", use_container_width=True):
            st.session_state.ai_open = True
            voice.speak("AI power online. Ready.", block=False)
            st.rerun()

st.markdown("---")

if not st.session_state.ai_open:
    st.warning("⚡ The AI is currently CLOSED. Click the green '🟢 OPEN AI' button above to activate voice, reasoning, and machine control.")
    st.stop()

# Intelligence Mode
selected_mode = st.radio(
    "Grok Intelligence Mode:",
    ["😎 Fun / Witty Mode", "🤔 Deep Think Mode", "⚡ Fast / Normal Mode"],
    horizontal=True
)
if "Fun" in selected_mode:
    agent.grok.set_mode("fun")
elif "Think" in selected_mode:
    agent.grok.set_mode("think")
else:
    agent.grok.set_mode("normal")

# Live Browser Microphone Widget
mic_html = """
<div style="background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 14px; text-align: center; margin: 10px 0;">
    <button id="micBtn" onclick="toggleMic()" style="background: #6366F1; color: white; border: none; padding: 12px 28px; border-radius: 25px; font-size: 15px; font-weight: bold; cursor: pointer; transition: all 0.2s;">
        🎙️ <span id="btnText">CLICK TO SPEAK (MICROPHONE ACTIVE)</span>
    </button>
    <div id="statusText" style="color: #94A3B8; font-size: 13px; margin-top: 8px;">Click the mic button, grant browser permission, and speak your question.</div>
</div>
<script>
let recognition = null;
let isRecording = false;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRec();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = function() {
        isRecording = true;
        document.getElementById('micBtn').style.background = '#EF4444';
        document.getElementById('btnText').innerText = '🔴 LISTENING... SPEAK NOW';
        document.getElementById('statusText').innerText = 'Listening to your microphone...';
    };

    recognition.onresult = function(event) {
        let interim = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                const finalTranscript = event.results[i][0].transcript;
                document.getElementById('statusText').innerText = 'Recognized: "' + finalTranscript + '" - Sending to AI...';
                
                const parentDoc = window.parent.document;
                const textarea = parentDoc.querySelector('textarea[data-testid="stChatInputTextArea"]');
                if (textarea) {
                    textarea.value = finalTranscript;
                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
                    setTimeout(() => {
                        const submitBtn = parentDoc.querySelector('button[data-testid="stChatInputSubmitButton"]');
                        if (submitBtn) submitBtn.click();
                    }, 250);
                }
            } else {
                interim += event.results[i][0].transcript;
                document.getElementById('statusText').innerText = 'Hearing: ' + interim;
            }
        }
    };

    recognition.onerror = function(event) {
        isRecording = false;
        document.getElementById('micBtn').style.background = '#6366F1';
        document.getElementById('btnText').innerText = '🎙️ CLICK TO SPEAK (MICROPHONE ACTIVE)';
        document.getElementById('statusText').innerText = 'Mic status: ' + event.error;
    };

    recognition.onend = function() {
        isRecording = false;
        document.getElementById('micBtn').style.background = '#6366F1';
        document.getElementById('btnText').innerText = '🎙️ CLICK TO SPEAK (MICROPHONE ACTIVE)';
    };
}

function toggleMic() {
    if (!recognition) {
        document.getElementById('statusText').innerText = 'Web Speech not supported in this browser. Please use Google Chrome or Microsoft Edge.';
        return;
    }
    if (isRecording) {
        recognition.stop();
    } else {
        recognition.start();
    }
}
</script>
"""
components.html(mic_html, height=110)

# Quick Action Chips
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    if st.button("📊 Hardware Telemetry"):
        st.session_state.quick_query = "What is the current system telemetry and hardware status?"
with c2:
    if st.button("💰 Wallet & Balance"):
        st.session_state.quick_query = "Check my wallet balance and address"
with c3:
    if st.button("🌐 Live Web News"):
        st.session_state.quick_query = "search web for latest AI breakthroughs"
with c4:
    if st.button("💻 Execute Python"):
        st.session_state.quick_query = "python: import math; print('Euler constant:', math.e, 'Pi squared:', math.pi**2)"
with c5:
    if st.button("🎨 Generate Graphic"):
        st.session_state.quick_query = "generate image of Quantum Neural Network"

# Conversation Feed
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

user_input = st.chat_input("Speak or type a command to Nexus-Grok...")
if "quick_query" in st.session_state and st.session_state.quick_query:
    user_input = st.session_state.quick_query
    st.session_state.quick_query = None

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing request..."):
            response = agent.process_request(user_input)
            st.markdown(response)
            st.markdown("<small style='color: #818CF8;'>🔊 Spoken aloud through audio system.</small>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Every response plays aloud
            voice.speak(response, block=False)

            if "generated_graphic.png" in response and os.path.exists("generated_graphic.png"):
                st.image("generated_graphic.png", caption="Nexus-Grok Rendered Graphic", use_column_width=True)

# Single Page Collapsible Tools
st.markdown("---")
with st.expander("🛠️ Advanced Machine, WoL Power & Blockchain Operations"):
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("##### 🔌 Power & Wake-on-LAN ('Open the Computer')")
        mac = st.text_input("Wake-on-LAN MAC Address:", "00:1A:2B:3C:4D:5E")
        if st.button("Broadcast WoL Packet"):
            w_res = agent.sys_controller.send_wake_on_lan(mac)
            st.success(w_res.get("message", str(w_res)))
            voice.speak("Wake on LAN signal sent.", block=False)
        
        st.markdown("##### 📸 Screenshot Capture")
        if st.button("Capture Display Now"):
            s_res = agent.sys_controller.capture_screenshot("screenshot.png")
            if s_res.get("success"):
                st.image("screenshot.png", caption="Current Desktop View", use_column_width=True)
                voice.speak("Screenshot captured.", block=False)

    with col_t2:
        st.markdown("##### ⛓️ Blockchain Direct Transfer")
        t_addr = st.text_input("Destination EVM Address:", "0x71C8360537B882E130420666060021b59E874da7")
        t_amt = st.number_input("Amount (AETH):", min_value=1.0, max_value=500.0, value=10.0, step=1.0)
        if st.button("Sign & Mine Transaction"):
            tx = agent.blockchain.create_and_sign_transaction(t_addr, t_amt, memo="Autonomous Transfer")
            if tx.get("success"):
                st.success(f"Mined into Block #{tx['block_index']}! Tx Hash: {tx['tx_hash'][:16]}...")
                voice.speak(f"Transaction mined into block {tx['block_index']}.", block=False)
            else:
                st.error(tx.get("error"))
