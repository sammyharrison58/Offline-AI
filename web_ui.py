import os
import sys
import time
import io
import base64
import streamlit as st
import streamlit.components.v1 as components

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from core.agent import Nexus226Agent
from core.voice_loop import OfflineVoiceEngine, ConversationalCallLoop
from core.call_server import CallBridgeServer
from core.phone_hud import get_phone_call_component

st.set_page_config(
    page_title="Nexus-Grok AI | Jarvis Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

@st.cache_data
def get_cached_bg():
    p = os.path.join(root_dir, "assets", "jarvis_hud_bg.png")
    if os.path.exists(p):
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

bg_b64 = get_cached_bg()

bg_style = f"""
    [data-testid="stAppViewContainer"], body {{
        background-image: linear-gradient(rgba(3, 6, 16, 0.40), rgba(3, 6, 16, 0.65)), url("data:image/png;base64,{bg_b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #F3F4F6;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }}
""" if bg_b64 else """
    [data-testid="stAppViewContainer"], body {
        background-color: #050814;
        color: #F3F4F6;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
"""

st.markdown(f"""
<style>
    {bg_style}
    @keyframes scanline {{
        0% {{ transform: translateY(-100vh); }}
        100% {{ transform: translateY(100vh); }}
    }}
    .holographic-beam {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00f0ff, transparent);
        opacity: 0.35;
        pointer-events: none;
        z-index: 9999;
        animation: scanline 7s linear infinite;
    }}
    .cyber-grid-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 1;
        background: radial-gradient(circle at 50% 25%, rgba(0, 240, 255, 0.08) 0%, transparent 65%);
    }}
    .main-title {{
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00f0ff, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
        letter-spacing: 1px;
    }}
    .sub-title {{
        color: #7dd3fc;
        font-size: 0.92rem;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }}
    .status-badge-on {{
        background: rgba(0, 240, 255, 0.12);
        color: #00f0ff;
        border: 1px solid #00f0ff;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.35);
    }}
    .status-badge-off {{
        background: rgba(239, 68, 68, 0.12);
        color: #F87171;
        border: 1px solid #DC2626;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }}
    .stButton>button {{
        border-radius: 8px;
        font-weight: 600;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(0, 240, 255, 0.3);
        color: #e2e8f0;
        transition: all 0.25s ease;
    }}
    .stButton>button:hover {{
        border-color: #00f0ff;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
        transform: translateY(-1px);
        color: #00f0ff;
    }}
    div[data-testid="stChatMessage"] {{
        background: rgba(10, 18, 36, 0.75) !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        border-left: 3px solid #00f0ff !important;
        border-radius: 14px !important;
        margin-bottom: 10px !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6), 0 0 15px rgba(0, 240, 255, 0.12) !important;
    }}
    div[data-testid="stChatInput"] {{
        border: 1px solid rgba(0, 240, 255, 0.6) !important;
        border-radius: 26px !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.3) !important;
        background: rgba(8, 14, 28, 0.92) !important;
        backdrop-filter: blur(14px) !important;
    }}
    .hud-metrics-bar {{
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin: 12px 0 18px 0;
    }}
    .hud-card {{
        flex: 1;
        background: rgba(10, 20, 38, 0.65);
        border: 1px solid rgba(0, 240, 255, 0.35);
        border-radius: 10px;
        padding: 8px 12px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5), inset 0 0 10px rgba(0, 240, 255, 0.08);
    }}
    .hud-card-lbl {{
        font-size: 10px;
        color: #94a3b8;
        letter-spacing: 1.5px;
        font-weight: 700;
    }}
    .hud-card-val {{
        font-size: 13px;
        color: #00f0ff;
        font-weight: 800;
        margin-top: 2px;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.6);
    }}
    .floating-hud-dock {{
        position: fixed;
        bottom: 85px;
        right: 25px;
        z-index: 99999;
        display: flex;
        flex-direction: column;
        gap: 6px;
        background: rgba(8, 14, 28, 0.88);
        border: 1px solid rgba(0, 240, 255, 0.45);
        border-radius: 12px;
        padding: 6px 8px;
        backdrop-filter: blur(14px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7), 0 0 16px rgba(0, 240, 255, 0.25);
    }}
    .hud-dock-link {{
        color: #00f0ff;
        text-decoration: none;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 8px;
        border-radius: 6px;
        background: rgba(0, 240, 255, 0.08);
        border: 1px solid rgba(0, 240, 255, 0.2);
        display: flex;
        align-items: center;
        gap: 4px;
        transition: all 0.2s ease;
    }}
    .hud-dock-link:hover {{
        background: rgba(0, 240, 255, 0.3);
        color: #ffffff;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }}
</style>
<div id="top-anchor"></div>
<div class="holographic-beam"></div>
<div class="cyber-grid-overlay"></div>
<div class="floating-hud-dock">
    <a href="#top-anchor" class="hud-dock-link">⬆️ TOP</a>
    <a href="#call-anchor" class="hud-dock-link">📞 CALL</a>
    <a href="#chat-anchor" class="hud-dock-link">💬 CHAT</a>
    <a href="#research-anchor" class="hud-dock-link">🔬 LAB</a>
    <a href="#tools-anchor" class="hud-dock-link">🛠️ TOOLS</a>
    <a href="#bottom-anchor" class="hud-dock-link">⬇️ END</a>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def get_agent():
    return Nexus226Agent()

@st.cache_resource
def get_voice():
    return OfflineVoiceEngine(voice_speed=3)

@st.cache_resource
def get_call_loop():
    return ConversationalCallLoop(agent_responder=agent.process_request)

agent = get_agent()
voice = get_voice()
call_loop = get_call_loop()
bridge_port = CallBridgeServer.start(agent, host="127.0.0.1", port=8502)

if "ai_open" not in st.session_state:
    st.session_state.ai_open = True

if "phone_call_open" not in st.session_state:
    st.session_state.phone_call_open = False

if "greeted" not in st.session_state:
    st.session_state.greeted = True
    voice.speak("Greetings. Nexus-Jarvis online and ready.", block=False)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Nexus-Jarvis online. Holographic neural core engaged. Speak or type your command into the bar below."}
    ]

bridge_history = CallBridgeServer.get_history()
if bridge_history:
    for h in bridge_history:
        st.session_state.messages.append({"role": "user", "content": h.get("user", "")})
        st.session_state.messages.append({"role": "assistant", "content": h.get("ai", "")})
    CallBridgeServer.clear_history()

with st.sidebar:
    st.markdown('<div class="main-title" style="font-size:1.35rem;">⚡ JARVIS DOCK</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px; color:#38bdf8; font-weight:700; margin-bottom:10px;">[ PERSISTENT HUD CONTROLS ]</div>', unsafe_allow_html=True)

    if st.session_state.ai_open:
        st.markdown('<div class="status-badge-on" style="text-align:center; margin-bottom:6px;">● CORE ACTIVE</div>', unsafe_allow_html=True)
        if st.button("🔴 STOP / CLOSE AI", key="sb_stop_ai", type="primary", use_container_width=True):
            st.session_state.ai_open = False
            voice.speak("AI power closed. Entering standby.", block=False)
            st.rerun()
    else:
        st.markdown('<div class="status-badge-off" style="text-align:center; margin-bottom:6px;">○ STANDBY</div>', unsafe_allow_html=True)
        if st.button("🟢 OPEN AI", key="sb_open_ai", type="primary", use_container_width=True):
            st.session_state.ai_open = True
            voice.speak("AI power online. Ready.", block=False)
            st.rerun()

    st.markdown("---")
    st.markdown("##### 📞 Phone Call Station")
    if st.session_state.phone_call_open or call_loop.is_active:
        st.success("🟢 Call Active")
        if st.button("🔴 END CALL NOW", key="sb_end_call", type="primary", use_container_width=True):
            st.session_state.phone_call_open = False
            call_loop.stop_call()
            st.rerun()
    else:
        if st.button("📞 START CALL", key="sb_start_call", use_container_width=True):
            st.session_state.phone_call_open = True
            st.rerun()

    st.markdown("---")
    st.markdown("##### 🧭 Instant Navigation")
    st.markdown("""
    <div style="display:flex; flex-direction:column; gap:6px;">
        <a href="#top-anchor" class="hud-dock-link">⬆️ Top of Cockpit</a>
        <a href="#call-anchor" class="hud-dock-link">📞 Phone Call Station</a>
        <a href="#chat-anchor" class="hud-dock-link">💬 Chat & Terminal</a>
        <a href="#research-anchor" class="hud-dock-link">🔬 Research Lab</a>
        <a href="#tools-anchor" class="hud-dock-link">🛠️ Machine Controls</a>
        <a href="#bottom-anchor" class="hud-dock-link">⬇️ Bottom / Input</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", key="sb_clear_chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat history cleared. System ready."}
        ]
        st.rerun()

col_hdr, col_pwr = st.columns([3, 1])
with col_hdr:
    st.markdown('<div class="main-title">⚡ NEXUS-JARVIS AI COCKPIT</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">226 AI Paradigms | Holographic HUD Core | Direct Voice Duplex | OS Machine Control</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px; color:#38bdf8; letter-spacing:2px; font-weight:700; margin-top:-6px; margin-bottom:8px;">[ SYSTEM: MK-IV ] // [ QUANTUM FLUX: OPTIMAL ] // [ SEC-GRID: ZERO-TRUST ]</div>', unsafe_allow_html=True)

with col_pwr:
    if st.session_state.ai_open:
        st.markdown('<div class="status-badge-on">● JARVIS CORE ACTIVE</div>', unsafe_allow_html=True)
        if st.button("🔴 CLOSE AI", use_container_width=True):
            st.session_state.ai_open = False
            voice.speak("AI power closed. Entering standby.", block=False)
            st.rerun()
    else:
        st.markdown('<div class="status-badge-off">○ SYSTEM STANDBY</div>', unsafe_allow_html=True)
        if st.button("🟢 OPEN AI", type="primary", use_container_width=True):
            st.session_state.ai_open = True
            voice.speak("AI power online. Ready.", block=False)
            st.rerun()

st.markdown("---")

if not st.session_state.ai_open:
    st.warning("⚡ The AI is currently CLOSED. Click the green '🟢 OPEN AI' button above to activate voice, reasoning, and machine control.")
    st.stop()

jarvis_sphere_html = """
<style>
body { margin:0; background:transparent; display:flex; justify-content:center; align-items:center; overflow:hidden; font-family:'Segoe UI',sans-serif; }
.jarvis-wrap { display:flex; flex-direction:column; align-items:center; justify-content:center; width:100%; height:230px; }
.jarvis-core { position:relative; width:144px; height:144px; display:flex; align-items:center; justify-content:center; }
.ring { position:absolute; border-radius:50%; box-sizing:border-box; }
.outer-ring { width:142px; height:142px; border:1px dashed rgba(0,240,255,0.45); animation:rotCW 18s linear infinite; }
.tracker-ring { width:126px; height:126px; border:2px solid transparent; border-top:2px solid #00f0ff; border-bottom:2px solid #00f0ff; filter:drop-shadow(0 0 8px #00f0ff); animation:rotCCW 9s linear infinite; }
.middle-ring { width:106px; height:106px; border:1px solid rgba(0,200,255,0.4); border-left:3px solid #00f0ff; border-right:3px solid #00f0ff; animation:rotCW 5s linear infinite; }
.dashed-ring { width:84px; height:84px; border:2px dotted rgba(0,240,255,0.7); animation:rotCCW 7s linear infinite; }
.core-orb { position:absolute; width:56px; height:56px; border-radius:50%; background:radial-gradient(circle, #00f0ff 0%, #0088ff 55%, rgba(0,20,60,0.85) 100%); box-shadow:0 0 25px #00f0ff, inset 0 0 16px #ffffff; animation:pulseOrb 2.2s ease-in-out infinite; }
.core-center { position:absolute; width:24px; height:24px; border-radius:50%; background:#ffffff; box-shadow:0 0 16px #00f0ff, 0 0 32px #00f0ff; animation:pulseCenter 2.2s ease-in-out infinite; }
.pulse-wave { position:absolute; width:60px; height:60px; border-radius:50%; border:1px solid #00f0ff; opacity:0; animation:waveOut 2.2s ease-out infinite; }
@keyframes rotCW { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }
@keyframes rotCCW { 0% { transform:rotate(360deg); } 100% { transform:rotate(0deg); } }
@keyframes pulseOrb { 0%,100% { transform:scale(0.92); opacity:0.85; filter:drop-shadow(0 0 12px #00f0ff); } 50% { transform:scale(1.08); opacity:1; filter:drop-shadow(0 0 28px #00f0ff); } }
@keyframes pulseCenter { 0%,100% { transform:scale(0.85); opacity:0.9; } 50% { transform:scale(1.15); opacity:1; } }
@keyframes waveOut { 0% { width:50px; height:50px; opacity:0.85; } 100% { width:155px; height:155px; opacity:0; } }
.hud-equalizer { display:flex; align-items:flex-end; gap:3px; height:24px; margin-top:10px; }
.bar { width:3px; background:linear-gradient(180deg, #00f0ff, #3b82f6); border-radius:2px; animation:bounceBar 1.2s ease-in-out infinite alternate; }
.b1 { height:6px; animation-delay:0.1s; }
.b2 { height:14px; animation-delay:0.3s; }
.b3 { height:22px; animation-delay:0.2s; }
.b4 { height:18px; animation-delay:0.4s; }
.b5 { height:10px; animation-delay:0.15s; }
.b6 { height:20px; animation-delay:0.35s; }
.b7 { height:12px; animation-delay:0.25s; }
.b8 { height:16px; animation-delay:0.05s; }
.b9 { height:24px; animation-delay:0.3s; }
.b10 { height:8px; animation-delay:0.45s; }
.b11 { height:18px; animation-delay:0.2s; }
.b12 { height:12px; animation-delay:0.1s; }
.b13 { height:22px; animation-delay:0.4s; }
.b14 { height:15px; animation-delay:0.25s; }
.b15 { height:7px; animation-delay:0.35s; }
@keyframes bounceBar { 0% { transform:scaleY(0.3); opacity:0.5; } 100% { transform:scaleY(1.1); opacity:1; } }
.hud-text { margin-top:6px; display:flex; flex-direction:column; align-items:center; }
.hud-tag { font-size:11px; font-weight:800; letter-spacing:3px; color:#00f0ff; text-shadow:0 0 10px rgba(0,240,255,0.85); }
.hud-sub { font-size:9px; font-weight:600; letter-spacing:1.5px; color:#60a5fa; opacity:0.85; margin-top:2px; }
</style>
<div class='jarvis-wrap'>
<div class='jarvis-core'>
<div class='ring outer-ring'></div>
<div class='ring tracker-ring'></div>
<div class='ring middle-ring'></div>
<div class='ring dashed-ring'></div>
<div class='pulse-wave'></div>
<div class='core-orb'></div>
<div class='core-center'></div>
</div>
<div class='hud-equalizer'>
<div class='bar b1'></div><div class='bar b2'></div><div class='bar b3'></div><div class='bar b4'></div><div class='bar b5'></div>
<div class='bar b6'></div><div class='bar b7'></div><div class='bar b8'></div><div class='bar b9'></div><div class='bar b10'></div>
<div class='bar b11'></div><div class='bar b12'></div><div class='bar b13'></div><div class='bar b14'></div><div class='bar b15'></div>
</div>
<div class='hud-text'>
<div class='hud-tag'>J.A.R.V.I.S. QUANTUM SPHERE ACTIVE</div>
<div class='hud-sub'>226 AI PARADIGMS ● AUDIO FREQUENCY EQUALIZER ONLINE</div>
</div>
</div>
"""
components.html(jarvis_sphere_html, height=235)

telemetry = agent.sys_controller.get_telemetry()
cpu_val = f"{telemetry['cpu_usage_percent']}%"
ram_val = f"{telemetry['ram_available_gb']} GB Free"
battery_val = f"{telemetry['battery']['percent']}%" if telemetry['battery']['percent'] != 'N/A' else "AC Power"

st.markdown(f"""
<div class="hud-metrics-bar">
    <div class="hud-card">
        <div class="hud-card-lbl">CPU USAGE</div>
        <div class="hud-card-val">{cpu_val}</div>
    </div>
    <div class="hud-card">
        <div class="hud-card-lbl">RAM STATUS</div>
        <div class="hud-card-val">{ram_val}</div>
    </div>
    <div class="hud-card">
        <div class="hud-card-lbl">POWER SOURCE</div>
        <div class="hud-card-val">{battery_val}</div>
    </div>
    <div class="hud-card">
        <div class="hud-card-lbl">NEURAL CORE</div>
        <div class="hud-card-val">226 DOMAINS</div>
    </div>
    <div class="hud-card">
        <div class="hud-card-lbl">SEC VAULT</div>
        <div class="hud-card-val">BLOCKCHAIN OK</div>
    </div>
</div>
""", unsafe_allow_html=True)

selected_mode = st.radio(
    "Intelligence Mode:",
    ["😎 Fun / Witty Mode", "🤔 Deep Think Mode", "⚡ Fast / Normal Mode"],
    horizontal=True
)
if "Fun" in selected_mode:
    agent.grok.set_mode("fun")
elif "Think" in selected_mode:
    agent.grok.set_mode("think")
else:
    agent.grok.set_mode("normal")

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    if st.button("📊 Telemetry"):
        st.session_state.quick_query = "What is the current system telemetry and hardware status?"
with c2:
    if st.button("💰 Wallet"):
        st.session_state.quick_query = "Check my wallet balance and address"
with c3:
    if st.button("🌐 Live Web"):
        st.session_state.quick_query = "search web for latest AI breakthroughs"
with c4:
    if st.button("💻 Python"):
        st.session_state.quick_query = "python: import math; print('Euler constant:', math.e, 'Pi squared:', math.pi**2)"
with c5:
    if st.button("🎨 Graphic"):
        st.session_state.quick_query = "generate image of Quantum Neural Network"
with c6:
    if st.button("🔬 Research"):
        st.session_state.quick_query = "research State Space Models and Mamba"

if hasattr(call_loop, "transcript_history") and call_loop.transcript_history:
    while call_loop.transcript_history:
        turn = call_loop.transcript_history.pop(0)
        st.session_state.messages.append({"role": "user", "content": turn[0]})
        st.session_state.messages.append({"role": "assistant", "content": turn[1]})

st.markdown('<div id="call-anchor"></div>', unsafe_allow_html=True)
call_box = st.container()
with call_box:
    if st.session_state.phone_call_open or call_loop.is_active:
        components.html(get_phone_call_component(port=bridge_port), height=340, scrolling=False)
        c_act1, c_act2 = st.columns([4, 1])
        with c_act1:
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid #10b981; border-radius: 8px; padding: 8px 14px; margin-top: 4px;">
                <span style="color: #10b981; font-weight: 700; font-size: 13px;">📞 FULL PHONE CALL CONSOLE ACTIVE:</span>
                <span style="color: #cbd5e1; font-size: 12px; margin-left: 6px;">Speak naturally into your mic. Jarvis transcribes, answers aloud, and keeps listening hands-free until you hang up.</span>
            </div>
            """, unsafe_allow_html=True)
        with c_act2:
            if st.button("🔴 END CALL", key="main_end_call", type="primary", use_container_width=True):
                st.session_state.phone_call_open = False
                call_loop.stop_call()
                st.rerun()
    else:
        c_btn1, c_btn2 = st.columns([3, 1])
        with c_btn1:
            if st.button("📞 START LIVE PHONE CALL DISCUSSION", type="primary", use_container_width=True):
                st.session_state.phone_call_open = True
                st.rerun()
        with c_btn2:
            if st.button("🪟 CALL WINDOW", use_container_width=True):
                import subprocess
                subprocess.Popen([sys.executable, os.path.join(root_dir, "main.py"), "--mode", "voice"], creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
                st.info("Phone call session launched in separate window.")

st.markdown('<div id="chat-anchor"></div>', unsafe_allow_html=True)
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

st.markdown('<div id="bottom-anchor"></div>', unsafe_allow_html=True)
c_bot1, c_bot2, c_bot3, c_bot4 = st.columns([2, 2, 2, 1])
with c_bot1:
    if st.session_state.ai_open:
        if st.button("🔴 STOP AI", key="bot_stop_ai", use_container_width=True):
            st.session_state.ai_open = False
            voice.speak("AI power closed. Entering standby.", block=False)
            st.rerun()
    else:
        if st.button("🟢 OPEN AI", key="bot_open_ai", type="primary", use_container_width=True):
            st.session_state.ai_open = True
            voice.speak("AI power online. Ready.", block=False)
            st.rerun()
with c_bot2:
    if st.session_state.phone_call_open or call_loop.is_active:
        if st.button("🔴 END CALL", key="bot_end_call", type="primary", use_container_width=True):
            st.session_state.phone_call_open = False
            call_loop.stop_call()
            st.rerun()
    else:
        if st.button("📞 CALL AI", key="bot_call_ai", use_container_width=True):
            st.session_state.phone_call_open = True
            st.rerun()
with c_bot3:
    if st.button("🗑️ Clear Chat", key="bot_clear_chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared. Standing by."}
        ]
        st.rerun()
with c_bot4:
    st.markdown('<a href="#top-anchor" style="text-decoration:none;"><button style="width:100%; height:38px; background:rgba(0,240,255,0.15); border:1px solid #00f0ff; color:#00f0ff; border-radius:8px; font-weight:700; cursor:pointer;">⬆️ TOP</button></a>', unsafe_allow_html=True)

user_input = None

chat_submission = st.chat_input("Type a command or click the mic icon right here to speak...", accept_audio=True)

if "quick_query" in st.session_state and st.session_state.quick_query:
    user_input = st.session_state.quick_query
    st.session_state.quick_query = None

if chat_submission is not None:
    if isinstance(chat_submission, str):
        user_input = chat_submission
    else:
        if hasattr(chat_submission, "text") and chat_submission.text:
            user_input = chat_submission.text
        if hasattr(chat_submission, "audio") and chat_submission.audio:
            audio_bytes = chat_submission.audio.getvalue()
            if SR_AVAILABLE:
                with st.spinner("🎙️ Transcribing voice from microphone..."):
                    try:
                        r = sr.Recognizer()
                        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                            audio_data = r.record(source)
                        transcribed = r.recognize_google(audio_data)
                        if transcribed:
                            user_input = transcribed
                            st.success(f"🗣️ Heard: \"{transcribed}\"")
                    except sr.UnknownValueError:
                        st.warning("Could not detect words clearly. Please speak closer to your microphone.")
                    except Exception as e:
                        st.error(f"Speech transcription error: {e}")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            response = st.write_stream(agent.process_request_stream(user_input))
            st.markdown("<small style='color: #00f0ff;'>🔊 Spoken aloud through audio system.</small>", unsafe_allow_html=True)
            if "generated_graphic.png" in response and os.path.exists("generated_graphic.png"):
                st.image("generated_graphic.png", caption="Rendered Graphic", use_column_width=True)
            voice.speak(response, block=False)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("---")
st.markdown('<div id="tools-anchor"></div>', unsafe_allow_html=True)
with st.expander("🛠️ Advanced Machine, WoL Power & Blockchain Operations"):
    col_t1, col_t2, col_t3 = st.columns(3)
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

    with col_t3:
        st.markdown("##### 🍃 MongoDB Storage & Sync")
        m_uri = st.text_input("MongoDB Connection URI:", "mongodb://localhost:27017")
        if st.button("Sync Files to MongoDB"):
            with st.spinner("Syncing project files and databases..."):
                conn = agent.mongo.connect(m_uri)
                r_files = agent.mongo.sync_all_files(root_dir)
                r_kb = agent.mongo.sync_knowledge_base(os.path.join(root_dir, "data", "ai_knowledge_226.json"))
                r_bc = agent.mongo.sync_blockchain_ledger(os.path.join(root_dir, "data", "blockchain_ledger.json"))
                if conn.get("success"):
                    st.success(f"Live MongoDB Synced! {r_files.get('count')} files, {r_kb.get('count')} AI domains, {r_bc.get('count')} ledger blocks.")
                    voice.speak("Files successfully synced to live MongoDB database.", block=False)
                else:
                    st.info(f"Offline Export Ready: {r_files.get('count')} files, {r_kb.get('count')} AI domains, {r_bc.get('count')} blocks saved to data/mongodb_export/.")
                    voice.speak("Files exported to MongoDB collections.", block=False)

st.markdown('<div id="research-anchor"></div>', unsafe_allow_html=True)
with st.expander("🔬 Offline AI Research Lab & 226 Architectural Dossiers", expanded=False):
    r_tab1, r_tab2 = st.tabs(["📚 Paradigm Dossier", "⚖️ Compare Paradigms"])
    with r_tab1:
        rc1, rc2 = st.columns([1, 2])
        with rc1:
            cats = ["All Categories"] + agent.knowledge.get_all_categories()
            chosen_cat = st.selectbox("Category Filter:", cats)
            search_kw = st.text_input("Instant Keyword / Math Search:", "")
            if search_kw.strip():
                doms = agent.knowledge.query(search_kw, top_k=15)
            elif chosen_cat != "All Categories":
                doms = agent.knowledge.get_category_domains(chosen_cat)
            else:
                doms = agent.knowledge.domains[:15]
            dom_names = [f"#{d.get('id')} {d.get('name')}" for d in doms]
            selected_dom_name = st.selectbox("Select Paradigm:", dom_names) if dom_names else None
        with rc2:
            if selected_dom_name:
                dom_id = int(selected_dom_name.split()[0].replace("#", ""))
                dossier = agent.knowledge.get_by_id(dom_id)
                if dossier:
                    res_obj = agent.knowledge.deep_research(dossier.get("name", ""))
                    st.markdown(res_obj.get("markdown", ""))
                    if st.button("🔊 Read Research Aloud", key="btn_read_res"):
                        voice.speak(res_obj.get("short_summary", ""), block=False)
    with r_tab2:
        cmp1, cmp2 = st.columns(2)
        all_dom_titles = [d.get("name") for d in agent.knowledge.domains]
        with cmp1:
            p1 = st.selectbox("Paradigm A:", all_dom_titles, index=0)
        with cmp2:
            p2 = st.selectbox("Paradigm B:", all_dom_titles, index=10)
        if st.button("⚖️ Run Architectural Comparison", use_container_width=True):
            cmp_md = agent.knowledge.compare_paradigms(p1, p2)
            st.markdown(cmp_md)
