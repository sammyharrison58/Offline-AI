def get_phone_call_component(port: int = 8502) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}}
body {{
    background: transparent;
    color: #f1f5f9;
    padding: 6px;
    overflow: hidden;
}}
.call-card {{
    background: linear-gradient(145deg, rgba(15, 23, 42, 0.96), rgba(8, 14, 28, 0.98));
    border: 2px solid #38bdf8;
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 0 30px rgba(56, 189, 248, 0.28), inset 0 0 20px rgba(56, 189, 248, 0.08);
    position: relative;
    max-width: 900px;
    margin: 0 auto;
}}
.call-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(56, 189, 248, 0.25);
    padding-bottom: 12px;
    margin-bottom: 14px;
}}
.call-title {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #38bdf8;
    text-transform: uppercase;
}}
.pulse-dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 12px #10b981;
    animation: blink 1.2s infinite ease-in-out;
}}
@keyframes blink {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.35; transform: scale(0.85); }}
}}
.call-timer {{
    font-family: 'Courier New', Courier, monospace;
    font-size: 20px;
    font-weight: 900;
    color: #f8fafc;
    background: rgba(15, 23, 42, 0.85);
    padding: 4px 14px;
    border-radius: 6px;
    border: 1px solid rgba(56, 189, 248, 0.4);
    letter-spacing: 2px;
}}
.call-body {{
    display: flex;
    gap: 20px;
    align-items: center;
    margin-bottom: 14px;
}}
.orb-container {{
    flex: 0 0 140px;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}}
.orb {{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: radial-gradient(circle, #38bdf8 0%, #0369a1 70%, transparent 100%);
    box-shadow: 0 0 35px #38bdf8;
    position: relative;
    transition: all 0.3s ease;
}}
.orb.speaking {{
    background: radial-gradient(circle, #06b6d4 0%, #0891b2 70%, transparent 100%);
    box-shadow: 0 0 50px #06b6d4;
    animation: pulseOrb 1s infinite alternate ease-in-out;
}}
.orb.listening {{
    background: radial-gradient(circle, #10b981 0%, #047857 70%, transparent 100%);
    box-shadow: 0 0 45px #10b981;
    animation: pulseOrb 1.4s infinite alternate ease-in-out;
}}
.orb.thinking {{
    background: radial-gradient(circle, #f59e0b 0%, #b45309 70%, transparent 100%);
    box-shadow: 0 0 45px #f59e0b;
    animation: spinOrb 2s infinite linear;
}}
@keyframes pulseOrb {{
    0% {{ transform: scale(0.92); opacity: 0.85; }}
    100% {{ transform: scale(1.12); opacity: 1; }}
}}
@keyframes spinOrb {{
    0% {{ transform: rotate(0deg) scale(1); }}
    50% {{ transform: rotate(180deg) scale(1.08); }}
    100% {{ transform: rotate(360deg) scale(1); }}
}}
.wave-bars {{
    display: flex;
    gap: 5px;
    align-items: center;
    height: 36px;
    margin-top: 8px;
}}
.bar {{
    width: 6px;
    height: 10px;
    background: #38bdf8;
    border-radius: 3px;
    transition: height 0.15s ease;
}}
.bar.active {{
    animation: jumpBar 0.6s infinite ease-in-out alternate;
}}
.bar:nth-child(1) {{ animation-delay: 0.1s; }}
.bar:nth-child(2) {{ animation-delay: 0.25s; }}
.bar:nth-child(3) {{ animation-delay: 0.4s; }}
.bar:nth-child(4) {{ animation-delay: 0.2s; }}
.bar:nth-child(5) {{ animation-delay: 0.35s; }}
.bar:nth-child(6) {{ animation-delay: 0.15s; }}
@keyframes jumpBar {{
    0% {{ height: 8px; background: #38bdf8; }}
    100% {{ height: 34px; background: #10b981; }}
}}
.subtitles-panel {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
    background: rgba(3, 7, 18, 0.65);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 10px;
    padding: 12px 16px;
    min-height: 140px;
    max-height: 150px;
    overflow-y: auto;
}}
.status-indicator {{
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #10b981;
    margin-bottom: 4px;
}}
.subtitle-line {{
    font-size: 14px;
    line-height: 1.45;
}}
.subtitle-user {{
    color: #93c5fd;
}}
.subtitle-ai {{
    color: #f1f5f9;
}}
.call-footer {{
    display: flex;
    gap: 12px;
    align-items: center;
    border-top: 1px solid rgba(56, 189, 248, 0.25);
    padding-top: 12px;
}}
.text-fallback-input {{
    flex: 1;
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(56, 189, 248, 0.4);
    border-radius: 8px;
    padding: 9px 14px;
    color: #f8fafc;
    font-size: 14px;
    outline: none;
}}
.text-fallback-input:focus {{
    border-color: #38bdf8;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
}}
.btn {{
    border: none;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}}
.btn-send {{
    background: #0284c7;
    color: #ffffff;
}}
.btn-send:hover {{
    background: #0369a1;
}}
.btn-end {{
    background: #dc2626;
    color: #ffffff;
    box-shadow: 0 0 15px rgba(220, 38, 38, 0.4);
}}
.btn-end:hover {{
    background: #b91c1c;
    box-shadow: 0 0 20px rgba(220, 38, 38, 0.7);
}}
.btn-mic {{
    background: rgba(30, 41, 59, 0.8);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.4);
}}
.btn-mic:hover {{
    background: rgba(51, 65, 85, 0.9);
}}
</style>
</head>
<body>
<div class="call-card" id="callCard">
    <div class="call-header">
        <div class="call-title">
            <div class="pulse-dot" id="pulseDot"></div>
            <span>LIVE PHONE CALL DISCUSSION</span>
        </div>
        <div class="call-timer" id="callTimer">00:00</div>
    </div>
    <div class="call-body">
        <div class="orb-container">
            <div class="orb listening" id="statusOrb"></div>
        </div>
        <div class="subtitles-panel" id="subtitlesPanel">
            <div class="status-indicator" id="statusIndicator">CONNECTED • LISTENING TO YOU...</div>
            <div class="wave-bars" id="waveBars">
                <div class="bar active"></div>
                <div class="bar active"></div>
                <div class="bar active"></div>
                <div class="bar active"></div>
                <div class="bar active"></div>
                <div class="bar active"></div>
            </div>
            <div class="subtitle-line subtitle-user" id="userSubtitle">You: (Speak into your mic...)</div>
            <div class="subtitle-line subtitle-ai" id="aiSubtitle">Jarvis: Line open. Ask any question.</div>
        </div>
    </div>
    <div class="call-footer">
        <input type="text" class="text-fallback-input" id="fallbackInput" placeholder="Quiet mode: type your question here if mic unavailable..." />
        <button class="btn btn-send" id="btnSend">SEND</button>
        <button class="btn btn-mic" id="btnMic">🎙️ MIC ON</button>
        <button class="btn btn-end" id="btnEnd">🔴 HANG UP</button>
    </div>
</div>

<script>
const BRIDGE_PORT = {port};
let audioCtx = null;
let recognition = null;
let isCallActive = true;
let isMicMuted = false;
let isAiSpeaking = false;
let callSeconds = 0;
let timerInterval = null;

function getAudioContext() {{
    if (!audioCtx) {{
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }}
    if (audioCtx.state === 'suspended') {{
        audioCtx.resume();
    }}
    return audioCtx;
}}

function playChime(freq1, freq2, duration) {{
    try {{
        const ctx = getAudioContext();
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq1, now);
        osc.frequency.exponentialRampToValueAtTime(freq2, now + duration);
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + duration);
        osc.start(now);
        osc.stop(now + duration);
    }} catch (e) {{}}
}}

function setStatus(text, orbState, color) {{
    const ind = document.getElementById('statusIndicator');
    const orb = document.getElementById('statusOrb');
    if (ind) {{
        ind.innerText = text;
        if (color) ind.style.color = color;
    }}
    if (orb) {{
        orb.className = 'orb ' + orbState;
    }}
    const bars = document.querySelectorAll('.bar');
    bars.forEach(b => {{
        if (orbState === 'speaking' || orbState === 'listening') {{
            b.classList.add('active');
        }} else {{
            b.classList.remove('active');
        }}
    }});
}}

function updateTimer() {{
    callSeconds++;
    const m = String(Math.floor(callSeconds / 60)).padStart(2, '0');
    const s = String(callSeconds % 60).padStart(2, '0');
    const el = document.getElementById('callTimer');
    if (el) el.innerText = m + ':' + s;
}}

function cleanForSpeech(raw) {{
    let t = raw.replace(/```[\s\S]*?```/g, 'Code block executed.');
    t = t.replace(/https?:\/\/\S+/g, 'link');
    t = t.replace(/[#*`_~>\-]/g, ' ');
    t = t.replace(/^(Direct Answer:|Answer:|Grok:|Response:|Query analyzed:[^.]*\.\s*)/i, '');
    t = t.replace(/\s+/g, ' ').trim();
    if (t.length > 220) {{
        let parts = t.split('. ');
        if (parts.length > 1) t = parts[0] + '.';
    }}
    return t;
}}

function speakResponse(text) {{
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    isAiSpeaking = true;
    setStatus('JARVIS IS SPEAKING...', 'speaking', '#06b6d4');
    const spoken = cleanForSpeech(text);
    const u = new SpeechSynthesisUtterance(spoken || text);
    u.rate = 1.05;
    u.pitch = 1.0;
    u.onend = function() {{
        isAiSpeaking = false;
        if (isCallActive) {{
            setStatus('CONNECTED • LISTENING TO YOU...', 'listening', '#10b981');
            startListening();
        }}
    }};
    u.onerror = function() {{
        isAiSpeaking = false;
        if (isCallActive) {{
            setStatus('CONNECTED • LISTENING TO YOU...', 'listening', '#10b981');
            startListening();
        }}
    }};
    window.speechSynthesis.speak(u);
}}

function queryAgent(userInput) {{
    if (!userInput || !userInput.trim()) return;
    const clean = userInput.trim().toLowerCase();
    if (clean.includes('hang up') || clean.includes('end call') || clean.includes('disconnect') || clean.includes('bye jarvis') || clean.includes('goodbye')) {{
        endCall();
        return;
    }}
    setStatus('PROCESSING QUERY...', 'thinking', '#f59e0b');
    fetch('http://127.0.0.1:' + BRIDGE_PORT, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ query: userInput }})
    }})
    .then(r => r.json())
    .then(data => {{
        const aiText = data.response || 'Understood.';
        const aiEl = document.getElementById('aiSubtitle');
        if (aiEl) aiEl.innerText = 'Jarvis: ' + aiText;
        speakResponse(aiText);
    }})
    .catch(err => {{
        const errMsg = 'Error connecting to Nexus bridge: ' + err.message;
        const aiEl = document.getElementById('aiSubtitle');
        if (aiEl) aiEl.innerText = 'Jarvis: ' + errMsg;
        speakResponse('Network error on local bridge.');
    }});
}}

function initSpeechRecognition() {{
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {{
        setStatus('MIC NOT SUPPORTED • USE INPUT BAR', 'thinking', '#f59e0b');
        return null;
    }}
    const rec = new SpeechRec();
    rec.continuous = false;
    rec.interimResults = true;
    rec.lang = 'en-US';

    rec.onstart = function() {{
        if (!isAiSpeaking && isCallActive) {{
            setStatus('CONNECTED • LISTENING TO YOU...', 'listening', '#10b981');
        }}
    }};

    rec.onresult = function(event) {{
        let interim = '';
        let final = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {{
            if (event.results[i].isFinal) {{
                final += event.results[i][0].transcript;
            }} else {{
                interim += event.results[i][0].transcript;
            }}
        }}
        const display = final || interim;
        if (display) {{
            const userEl = document.getElementById('userSubtitle');
            if (userEl) userEl.innerText = 'You: ' + display;
        }}
        if (final && final.trim()) {{
            queryAgent(final.trim());
        }}
    }};

    rec.onerror = function(event) {{
        if (event.error !== 'no-speech' && event.error !== 'aborted') {{
            console.log('Speech rec error:', event.error);
        }}
    }};

    rec.onend = function() {{
        if (isCallActive && !isAiSpeaking && !isMicMuted) {{
            setTimeout(startListening, 150);
        }}
    }};
    return rec;
}}

function startListening() {{
    if (!isCallActive || isAiSpeaking || isMicMuted) return;
    if (!recognition) {{
        recognition = initSpeechRecognition();
    }}
    if (recognition) {{
        try {{
            recognition.start();
        }} catch (e) {{}}
    }}
}}

function stopListening() {{
    if (recognition) {{
        try {{
            recognition.stop();
        }} catch (e) {{}}
    }}
}}

function endCall() {{
    isCallActive = false;
    stopListening();
    if (timerInterval) clearInterval(timerInterval);
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    playChime(440, 220, 0.45);
    setStatus('CALL ENDED • STANDBY', 'thinking', '#ef4444');
    const dot = document.getElementById('pulseDot');
    if (dot) {{
        dot.style.background = '#ef4444';
        dot.style.boxShadow = '0 0 10px #ef4444';
        dot.style.animation = 'none';
    }}
    fetch('http://127.0.0.1:' + BRIDGE_PORT, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ action: 'end_call' }})
    }}).catch(() => {{}});
}}

window.addEventListener('DOMContentLoaded', () => {{
    playChime(523.25, 659.25, 0.4);
    timerInterval = setInterval(updateTimer, 1000);
    recognition = initSpeechRecognition();

    fetch('http://127.0.0.1:' + BRIDGE_PORT, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ action: 'start_call' }})
    }})
    .then(r => r.json())
    .then(data => {{
        const greeting = data.greeting || 'Call connected. Nexus-Jarvis online and listening. Go ahead.';
        const aiEl = document.getElementById('aiSubtitle');
        if (aiEl) aiEl.innerText = 'Jarvis: ' + greeting;
        speakResponse(greeting);
    }})
    .catch(() => {{
        speakResponse('Call connected. Nexus-Jarvis ready. Go ahead.');
    }});

    const btnEnd = document.getElementById('btnEnd');
    if (btnEnd) btnEnd.onclick = endCall;

    const btnMic = document.getElementById('btnMic');
    if (btnMic) {{
        btnMic.onclick = function() {{
            isMicMuted = !isMicMuted;
            if (isMicMuted) {{
                btnMic.innerText = '🔇 MUTED';
                btnMic.style.color = '#ef4444';
                stopListening();
                setStatus('MICROPHONE MUTED', 'thinking', '#f59e0b');
            }} else {{
                btnMic.innerText = '🎙️ MIC ON';
                btnMic.style.color = '#38bdf8';
                setStatus('CONNECTED • LISTENING TO YOU...', 'listening', '#10b981');
                startListening();
            }}
        }};
    }}

    const btnSend = document.getElementById('btnSend');
    const input = document.getElementById('fallbackInput');
    function sendText() {{
        if (input && input.value.trim()) {{
            const val = input.value.trim();
            input.value = '';
            const userEl = document.getElementById('userSubtitle');
            if (userEl) userEl.innerText = 'You: ' + val;
            queryAgent(val);
        }}
    }}
    if (btnSend) btnSend.onclick = sendText;
    if (input) {{
        input.addEventListener('keydown', (e) => {{
            if (e.key === 'Enter') sendText();
        }});
    }}
}});
</script>
</body>
</html>
"""

