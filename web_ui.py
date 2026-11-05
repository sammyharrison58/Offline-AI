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
from core.voice_loop import OfflineVoiceEngine

st.set_page_config(
    page_title="Nexus-Grok AI | Jarvis Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

bg_b64 = ""
bg_path = os.path.join(root_dir, "assets", "jarvis_hud_bg.png")
if os.path.exists(bg_path):
    with open(bg_path, "rb") as f:
        bg_b64 = base64.b64encode(f.read()).decode()

bg_style = f"""
    [data-testid="stAppViewContainer"], body {{
        background-image: linear-gradient(rgba(5, 8, 18, 0.82), rgba(5, 8, 18, 0.92)), url("data:image/png;base64,{bg_b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #F3F4F6;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }}
""" if bg_b64 else """
    [data-testid="stAppViewContainer"], body {
        background-color: #070B14;
        color: #F3F4F6;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
"""

st.markdown(f"""
<style>
    {bg_style}
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
        background: rgba(15, 23, 42, 0.65) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 14px !important;
        margin-bottom: 10px !important;
        backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
    }}
    div[data-testid="stChatInput"] {{
        border: 1px solid rgba(0, 240, 255, 0.5) !important;
        border-radius: 26px !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.25) !important;
        background: rgba(11, 17, 32, 0.9) !important;
        backdrop-filter: blur(12px) !important;
    }}
    .hud-metrics-bar {{
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin: 12px 0 18px 0;
    }}
    .hud-card {{
        flex: 1;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(0, 240, 255, 0.25);
        border-radius: 10px;
        padding: 8px 12px;
        text-align: center;
        backdrop-filter: blur(6px);
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
        {"role": "assistant", "content": "Nexus-Jarvis online. Holographic neural core engaged. Speak or type your command into the bar below."}
    ]

col_hdr, col_pwr = st.columns([3, 1])
with col_hdr:
    st.markdown('<div class="main-title">⚡ NEXUS-JARVIS AI COCKPIT</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">226 AI Paradigms | Holographic HUD Core | Direct Voice Duplex | OS Machine Control</div>', unsafe_allow_html=True)

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

c1, c2, c3, c4, c5 = st.columns(5)
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

chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

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
            safe_text = response.replace('"', '\\"').replace("'", "\\'").replace('\n', ' ')
            browser_audio = f"""
            <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utt = new SpeechSynthesisUtterance("{safe_text[:300]}");
                utt.rate = 1.15;
                window.speechSynthesis.speak(utt);
            }}
            </script>
            """
            components.html(browser_audio, height=0)
    st.session_state.messages.append({"role": "assistant", "content": response})

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
