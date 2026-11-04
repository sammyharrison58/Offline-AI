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

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

class OfflineVoiceEngine:

    def __init__(self, voice_speed: int = 3):
        self.sapi_voice = None
        self.lock = threading.Lock()
        if SAPI_AVAILABLE:
            try:
                self.sapi_voice = win32com.client.Dispatch('SAPI.SpVoice')
                self.sapi_voice.Rate = voice_speed
            except Exception as e:
                print(f'[VoiceEngine] Warning: SAPI initialization failed: {e}')

    def clean_text_for_speech(self, text: str) -> str:
        t = re.sub(r'```.*?```', 'code block executed.', text, flags=re.DOTALL)
        t = re.sub(r'https?://\S+', 'link', t)
        t = re.sub(r'[#*`_~>\-]', ' ', t)
        t = re.sub(r'\s+', ' ', t).strip()
        if len(t) > 350:
            sentences = t.split('. ')
            if len(sentences) > 2:
                t = '. '.join(sentences[:2]) + '.'
        return t

    def speak(self, text: str, block: bool = False):
        clean_text = self.clean_text_for_speech(text)
        if not self.sapi_voice or not clean_text:
            if clean_text:
                print(f'[AI Voice Output]: {clean_text}')
            return

        def _run_speak():
            with self.lock:
                try:
                    self.sapi_voice.Speak(clean_text, 1)
                except Exception as e:
                    print(f'[VoiceEngine Error] {e}')

        if block:
            with self.lock:
                try:
                    self.sapi_voice.Speak(clean_text, 0)
                except Exception as e:
                    print(f'[VoiceEngine Error] {e}')
        else:
            threading.Thread(target=_run_speak, daemon=True).start()

    def stop_speaking(self):
        if self.sapi_voice:
            try:
                self.sapi_voice.Speak('', 2)
            except Exception:
                pass

class ConversationalCallLoop:

    def __init__(self, agent_responder: Callable[[str], str]):
        self.agent_responder = agent_responder
        self.voice = OfflineVoiceEngine(voice_speed=3)
        self.is_active = False
        self.recognizer = sr.Recognizer() if SR_AVAILABLE else None
        self.mic = None
        if SR_AVAILABLE:
            try:
                self.mic = sr.Microphone()
            except Exception:
                self.mic = None

    def start_call(self):
        self.is_active = True
        greeting = 'Nexus online. Real time call active. Listening.'
        print(f'\nAI: {greeting}\n')
        self.voice.speak(greeting, block=True)

        while self.is_active:
            user_input = self._listen_or_prompt()
            if not user_input:
                continue

            clean_input = user_input.strip().lower()
            if clean_input in ['hang up', 'end call', 'disconnect', 'shut down', 'exit', 'quit']:
                farewell = 'Call ended. Standby.'
                print(f'\nAI: {farewell}\n')
                self.voice.speak(farewell, block=True)
                self.is_active = False
                break

            print(f'\n[User]: {user_input}')
            try:
                response = self.agent_responder(user_input)
            except Exception as e:
                response = f'Error executing request: {str(e)}'

            print(f'[AI]: {response}\n')
            self.voice.speak(response, block=True)

    def _listen_or_prompt(self) -> Optional[str]:
        if self.recognizer and self.mic:
            try:
                print('>> [Listening to microphone... speak now] ', end='', flush=True)
                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = self.recognizer.listen(source, timeout=4, phrase_time_limit=10)
                print('\n[Transcribing voice input...]')
                text = self.recognizer.recognize_google(audio)
                if text:
                    print(f'Recognized: "{text}"')
                    return text
            except Exception as e:
                pass

        try:
            return input('>> [Speak/Type]: ')
        except (EOFError, KeyboardInterrupt):
            self.is_active = False
            return 'hang up'

if __name__ == '__main__':
    def dummy_responder(query: str) -> str:
        return f'Acknowledged query {query}. Operational.'
    call = ConversationalCallLoop(agent_responder=dummy_responder)
    call.voice.speak('Offline voice engine tested.', block=True)
