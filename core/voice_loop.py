import sys
import time
import threading
import queue
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

    def __init__(self, voice_speed: int=1):
        self.sapi_voice = None
        self.lock = threading.Lock()
        if SAPI_AVAILABLE:
            try:
                self.sapi_voice = win32com.client.Dispatch('SAPI.SpVoice')
                self.sapi_voice.Rate = voice_speed
            except Exception as e:
                print(f'[VoiceEngine] Warning: SAPI initialization failed: {e}')

    def speak(self, text: str, block: bool=True):
        clean_text = text.replace('*', '').replace('#', '').replace('`', '')
        if not self.sapi_voice:
            print(f'[AI Voice Output]: {clean_text}')
            return

        def _run_speak():
            with self.lock:
                try:
                    flags = 0 if block else 1
                    self.sapi_voice.Speak(clean_text, flags)
                except Exception as e:
                    print(f'[VoiceEngine Error] {e}')
        if block:
            _run_speak()
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
        self.voice = OfflineVoiceEngine(voice_speed=1)
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
        print('\n' + '=' * 65)
        print(' [NEXUS-226] DUPLEX VOICE CALL CONNECTED (ALWAYS ON)')
        print(' Mode: Real-Life One-on-One Voice Conversation')
        print(' Speak freely into your mic or type text below.')
        print(" Say or type 'hang up', 'goodbye', or 'shut down' to end call.")
        print('=' * 65 + '\n')
        greeting = 'Nexus online. I am connected and listening. How can I assist you with the machine, transactions, or any AI architecture?'
        print(f'\nAI: {greeting}\n')
        self.voice.speak(greeting, block=True)
        while self.is_active:
            user_input = self._listen_or_prompt()
            if not user_input:
                continue
            clean_input = user_input.strip().lower()
            if clean_input in ['hang up', 'end call', 'disconnect', 'shut down', 'exit', 'quit']:
                farewell = 'Call ended. Entering standby mode.'
                print(f'\nAI: {farewell}\n')
                self.voice.speak(farewell, block=True)
                self.is_active = False
                break
            print(f'\n[User]: {user_input}')
            print('[Nexus-226]: Thinking & Processing...')
            try:
                response = self.agent_responder(user_input)
            except Exception as e:
                response = f'I encountered an error executing that request: {str(e)}'
            print(f'[AI]: {response}\n')
            self.voice.speak(response, block=True)

    def _listen_or_prompt(self) -> Optional[str]:
        if self.recognizer and self.mic:
            try:
                print('>> [Listening... speak now or press Enter to type] ', end='', flush=True)
                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=10)
                print('\n[Processing voice input...]')
                text = self.recognizer.recognize_sphinx(audio) if hasattr(self.recognizer, 'recognize_sphinx') else None
                if text:
                    return text
            except Exception:
                pass
        try:
            val = input('>> [Speak/Type]: ')
            return val
        except (EOFError, KeyboardInterrupt):
            self.is_active = False
            return 'hang up'
if __name__ == '__main__':

    def dummy_responder(query: str) -> str:
        return f"Acknowledged query regarding '{query}'. All subsystems operational."
    call = ConversationalCallLoop(agent_responder=dummy_responder)
    print('Testing Voice Engine directly...')
    call.voice.speak('Offline voice engine initialized successfully.', block=True)
