import sys
import os
import time
import threading
import queue
import json
import re
import struct
from typing import Optional, Callable

try:
    import win32com.client
    SAPI_AVAILABLE = True
except ImportError:
    SAPI_AVAILABLE = False

sr = None
SR_AVAILABLE = None

def _get_sr():
    global sr, SR_AVAILABLE
    if SR_AVAILABLE is None:
        try:
            import speech_recognition as _sr
            sr = _sr
            SR_AVAILABLE = True
        except ImportError:
            sr = None
            SR_AVAILABLE = False
    return sr, SR_AVAILABLE

VOSK_MODEL = None
VOSK_AVAILABLE = None
VOSK_MODEL_PATH = None

def _find_vosk_model():
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    candidates = [
        os.path.join(base, 'vosk-model-small-en-us-0.15'),
        os.path.join(base, 'vosk-model-en-us-0.22-lgraph'),
        os.path.join(base, 'vosk-model'),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    for item in os.listdir(base) if os.path.isdir(base) else []:
        full = os.path.join(base, item)
        if os.path.isdir(full) and 'vosk' in item.lower():
            return full
    return None

def _load_vosk():
    global VOSK_MODEL, VOSK_AVAILABLE, VOSK_MODEL_PATH
    if VOSK_AVAILABLE is not None:
        return VOSK_AVAILABLE
    try:
        import vosk
        vosk.SetLogLevel(-1)
        model_path = _find_vosk_model()
        if not model_path:
            VOSK_AVAILABLE = False
            return False
        VOSK_MODEL_PATH = model_path
        VOSK_MODEL = vosk.Model(model_path)
        VOSK_AVAILABLE = True
        return True
    except Exception:
        VOSK_AVAILABLE = False
        return False

def _decode_audio_with_vosk(audio) -> Optional[str]:
    if not _load_vosk() or VOSK_MODEL is None:
        return None
    try:
        import vosk
        raw_pcm = audio.get_raw_data(convert_rate=16000, convert_width=2)
        rec = vosk.KaldiRecognizer(VOSK_MODEL, 16000)
        rec.SetMaxAlternatives(0)
        rec.SetWords(False)
        rec.AcceptWaveform(raw_pcm)
        res = json.loads(rec.FinalResult())
        text = res.get('text', '').strip()
        return text if text else None
    except Exception:
        return None

class OfflineVoiceEngine:

    def __init__(self, voice_speed: int = 1, feminine: bool = True):
        self.voice_speed = voice_speed
        self.feminine = feminine
        self.lock = threading.Lock()
        self.sapi_voice = None

    def clean_text_for_speech(self, text: str) -> str:
        if not text:
            return ""
        t = re.sub(r'```[a-zA-Z0-9_]*\n?.*?```', ' I have prepared the complete code implementation for you on your screen. ', text, flags=re.DOTALL)
        t = re.sub(r'https?://\S+', ' link ', t)
        t = re.sub(r'[\U00010000-\U0010ffff]', '', t)
        t = re.sub(r'[\u2600-\u27bf]', '', t)
        t = re.sub(r'^(Direct Answer:|Answer:|Grok:|Response:|Nexus:|Query analyzed:[^.]*\.\s*)', '', t, flags=re.IGNORECASE)
        t = t.replace('O(1)', 'constant time')
        t = t.replace('O(log n)', 'order log n')
        t = t.replace('O(n)', 'order n')
        t = t.replace('O(n log n)', 'order n log n')
        t = t.replace('O(n^2)', 'order n squared')
        t = re.sub(r'[*#`_~>\\-]', ' ', t)
        t = re.sub(r'\s+', ' ', t).strip()
        if len(t) > 380:
            sentences = re.split(r'(?<=[.!?])\s+', t)
            accumulated = []
            cur_len = 0
            for s in sentences:
                if cur_len + len(s) <= 380:
                    accumulated.append(s)
                    cur_len += len(s)
                else:
                    break
            if accumulated:
                t = ' '.join(accumulated)
            else:
                t = sentences[0]
        return t

    def speak(self, text: str, block: bool = False):
        clean_text = self.clean_text_for_speech(text)
        if not clean_text or not SAPI_AVAILABLE:
            return

        def _run_speak():
            with self.lock:
                try:
                    try:
                        import pythoncom
                        pythoncom.CoInitialize()
                    except Exception:
                        pass
                    v = win32com.client.Dispatch('SAPI.SpVoice')
                    self.sapi_voice = v
                    if self.feminine:
                        for i in range(v.GetVoices().Count):
                            vc = v.GetVoices().Item(i)
                            desc = vc.GetDescription().lower()
                            if any(k in desc for k in ['zira', 'female', 'eva', 'jenny', 'aria', 'hazel', 'susan', 'catherine']):
                                v.Voice = vc
                                break
                    v.Rate = self.voice_speed
                    v.Speak(clean_text, 0)
                except Exception as e:
                    print(f'[VoiceEngine Error] {e}')

        if block:
            _run_speak()
        else:
            threading.Thread(target=_run_speak, daemon=True).start()

    def stop_speaking(self):
        if hasattr(self, 'sapi_voice') and self.sapi_voice:
            try:
                self.sapi_voice.Speak('', 2)
            except Exception:
                pass


def _vosk_listen_once(samplerate: int = 16000, max_seconds: int = 15, silence_ms: int = 1000, initial_timeout_sec: float = 3.5) -> Optional[str]:
    try:
        import sounddevice as sd
        import vosk
    except ImportError:
        return None
    if not _load_vosk() or VOSK_MODEL is None:
        return None
    try:
        rec = vosk.KaldiRecognizer(VOSK_MODEL, samplerate)
        rec.SetMaxAlternatives(0)
        rec.SetWords(False)
        chunk_ms = 100
        chunk_size = int(samplerate * chunk_ms / 1000)
        silence_chunks = int(silence_ms / chunk_ms)
        initial_chunks_limit = int(initial_timeout_sec * 1000 / chunk_ms)
        consecutive_silence = 0
        chunks_elapsed = 0
        total_chunks = int(max_seconds * 1000 / chunk_ms)
        got_speech = False
        transcript = ''
        with sd.RawInputStream(samplerate=samplerate, blocksize=chunk_size, dtype='int16', channels=1) as stream:
            for _ in range(total_chunks):
                chunks_elapsed += 1
                data, _ = stream.read(chunk_size)
                raw = bytes(data)
                if rec.AcceptWaveform(raw):
                    res = json.loads(rec.Result())
                    t = res.get('text', '').strip()
                    if t:
                        transcript += ' ' + t
                        got_speech = True
                        consecutive_silence = 0
                    else:
                        consecutive_silence += 1
                else:
                    partial = json.loads(rec.PartialResult()).get('partial', '').strip()
                    if partial:
                        got_speech = True
                        consecutive_silence = 0
                    else:
                        if got_speech:
                            consecutive_silence += 1
                if got_speech and consecutive_silence >= silence_chunks:
                    break
                if not got_speech and chunks_elapsed >= initial_chunks_limit:
                    break
            final = json.loads(rec.FinalResult()).get('text', '').strip()
            if final:
                transcript += ' ' + final
        return transcript.strip() or None
    except Exception:
        return None


class ConversationalCallLoop:

    def __init__(self, agent_responder: Callable[[str], str]):
        self.agent_responder = agent_responder
        self.voice = OfflineVoiceEngine(voice_speed=1, feminine=True)
        self.is_active = False
        self.recognizer = None
        self.mic = None
        self.last_user_speech = ""
        self.last_ai_response = ""
        self.call_thread = None
        self.transcript_history = []
        self._vosk_ready = False
        threading.Thread(target=self._init_all, daemon=True).start()

    def _init_all(self):
        self._init_mic()
        self._vosk_ready = _load_vosk()

    def _init_mic(self):
        _sr, avail = _get_sr()
        if avail and not self.mic:
            try:
                if not self.recognizer:
                    self.recognizer = _sr.Recognizer()
                    self.recognizer.energy_threshold = 250
                    self.recognizer.dynamic_energy_threshold = True
                    self.recognizer.pause_threshold = 0.8
                    self.recognizer.non_speaking_duration = 0.4
                self.mic = _sr.Microphone()
            except Exception:
                self.mic = None

    def start_call(self, on_turn: Optional[Callable[[str, str], None]] = None):
        self._init_all()
        self.is_active = True
        greeting = "Call connected. Hey, Lyra here! I'm on the line and listening. What are we working on?"
        print(f'\nAI: {greeting}\n')
        self.voice.speak(greeting, block=True)

        if self.recognizer and self.mic:
            try:
                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
                    self.recognizer.energy_threshold = max(self.recognizer.energy_threshold, 200)
                    while self.is_active:
                        user_input = self._listen_or_prompt(source=source)
                        if not user_input or not self.is_active:
                            continue
                        if self._handle_turn(user_input, on_turn):
                            return
                return
            except Exception as e:
                print(f'[Microphone Stream Error] {e}')

        while self.is_active:
            user_input = self._listen_or_prompt()
            if not user_input or not self.is_active:
                continue
            if self._handle_turn(user_input, on_turn):
                return

    def _handle_turn(self, user_input: str, on_turn) -> bool:
        clean_input = user_input.strip().lower()
        if any(w in clean_input for w in ['hang up', 'end call', 'close call', 'disconnect', 'goodbye', 'bye lyra', 'bye jarvis', 'bye', 'terminate call']):
            farewell = 'Call ended. Talk to you soon!'
            print(f'\nAI: {farewell}\n')
            self.voice.speak(farewell, block=True)
            self.is_active = False
            return True
        print(f'\n[User]: {user_input}')
        self.last_user_speech = user_input
        try:
            response = self.agent_responder(user_input)
        except Exception as e:
            response = f'Error executing request: {str(e)}'
        print(f'[AI]: {response}\n')
        self.last_ai_response = response
        self.transcript_history.append((user_input, response))
        if on_turn:
            try:
                on_turn(user_input, response)
            except Exception:
                pass
        self.voice.speak(response, block=True)
        return False

    def stop_call(self):
        if self.is_active:
            self.is_active = False
            self.voice.speak('Call ended.', block=False)

    def start_call_background(self, on_turn: Optional[Callable[[str, str], None]] = None):
        if not self.is_active:
            self.call_thread = threading.Thread(target=self.start_call, args=(on_turn,), daemon=True)
            self.call_thread.start()

    def _listen_or_prompt(self, source=None) -> Optional[str]:
        if not self.is_active:
            return None

        _sr, avail = _get_sr()
        w_err = getattr(_sr, "WaitTimeoutError", Exception) if avail else Exception
        u_err = getattr(_sr, "UnknownValueError", Exception) if avail else Exception
        r_err = getattr(_sr, "RequestError", Exception) if avail else Exception

        if self.recognizer and source:
            try:
                audio = self.recognizer.listen(source, timeout=4, phrase_time_limit=15)
                vosk_text = _decode_audio_with_vosk(audio)
                if vosk_text:
                    return vosk_text
                try:
                    google_text = self.recognizer.recognize_google(audio)
                    if google_text and google_text.strip():
                        return google_text.strip()
                except Exception:
                    pass
            except w_err:
                return None
            except u_err:
                return None
            except Exception:
                time.sleep(0.05)
                return None
        elif self.recognizer and self.mic:
            try:
                with self.mic as src:
                    audio = self.recognizer.listen(src, timeout=4, phrase_time_limit=15)
                vosk_text = _decode_audio_with_vosk(audio)
                if vosk_text:
                    return vosk_text
                try:
                    google_text = self.recognizer.recognize_google(audio)
                    if google_text and google_text.strip():
                        return google_text.strip()
                except Exception:
                    pass
            except w_err:
                return None
            except u_err:
                return None
            except Exception:
                time.sleep(0.05)
                return None

        if self._vosk_ready and VOSK_AVAILABLE:
            try:
                direct_text = _vosk_listen_once(samplerate=16000, max_seconds=15, silence_ms=1000, initial_timeout_sec=3.5)
                if direct_text:
                    return direct_text
            except Exception:
                pass

        try:
            return input('>> [User Speaking]: ')
        except (EOFError, KeyboardInterrupt):
            self.is_active = False
            return 'hang up'


if __name__ == '__main__':
    def dummy_responder(query: str) -> str:
        return f'Acknowledged query {query}. Operational.'
    call = ConversationalCallLoop(agent_responder=dummy_responder)
    call.voice.speak('Offline voice engine tested.', block=True)
