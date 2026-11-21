import sys
import time
import threading
import queue
import re
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
        t = re.sub(r'[*#`_~>\-]', ' ', t)
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
        threading.Thread(target=self._init_mic, daemon=True).start()

    def _init_mic(self):
        _sr, avail = _get_sr()
        if avail and not self.mic:
            try:
                if not self.recognizer:
                    self.recognizer = _sr.Recognizer()
                self.mic = _sr.Microphone()
            except Exception:
                self.mic = None

    def start_call(self, on_turn: Optional[Callable[[str, str], None]] = None):
        self._init_mic()
        self.is_active = True
        greeting = "Call connected. Hey, Nexus here! I'm on the line and listening. What are we working on?"
        print(f'\nAI: {greeting}\n')
        self.voice.speak(greeting, block=True)
        if self.recognizer and self.mic:
            try:
                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    self.recognizer.pause_threshold = 0.7
                    self.recognizer.non_speaking_duration = 0.4
                    self.recognizer.dynamic_energy_threshold = True
                    while self.is_active:
                        user_input = self._listen_or_prompt(source=source)
                        if not user_input or not self.is_active:
                            continue

                        clean_input = user_input.strip().lower()
                        if any(w in clean_input for w in ['hang up', 'end call', 'close call', 'disconnect', 'goodbye', 'bye jarvis', 'bye', 'terminate call']):
                            farewell = 'Call ended. Talk to you soon!'
                            print(f'\nAI: {farewell}\n')
                            self.voice.speak(farewell, block=True)
                            self.is_active = False
                            break

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
                return
            except Exception as e:
                print(f'[Microphone Stream Error] {e}')

        while self.is_active:
            user_input = self._listen_or_prompt()
            if not user_input or not self.is_active:
                continue

            clean_input = user_input.strip().lower()
            if any(w in clean_input for w in ['hang up', 'end call', 'close call', 'disconnect', 'goodbye', 'bye jarvis', 'bye', 'terminate call']):
                farewell = 'Call ended. Talk to you soon!'
                print(f'\nAI: {farewell}\n')
                self.voice.speak(farewell, block=True)
                self.is_active = False
                break

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
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                if text and text.strip():
                    return text.strip()
            except w_err:
                return None
            except u_err:
                return None
            except r_err:
                try:
                    return input('>> [Voice Line - Enter query]: ')
                except (EOFError, KeyboardInterrupt):
                    self.is_active = False
                    return 'hang up'
            except Exception:
                time.sleep(0.05)
                return None
        elif self.recognizer and self.mic:
            try:
                with self.mic as src:
                    audio = self.recognizer.listen(src, timeout=3, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                if text and text.strip():
                    return text.strip()
            except w_err:
                return None
            except u_err:
                return None
            except r_err:
                try:
                    return input('>> [Voice Line - Enter query]: ')
                except (EOFError, KeyboardInterrupt):
                    self.is_active = False
                    return 'hang up'
            except Exception:
                time.sleep(0.05)
                return None

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
