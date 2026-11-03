"""
Voice Engine & Full-Duplex Conversational Call Loop.
Provides low-latency offline Text-to-Speech (via Windows SAPI5) and
continuous real-time voice interaction ('Always On Call' loop).
"""
import sys
import time
import threading
import queue
from typing import Optional, Callable

# Check for Windows SAPI5
try:
    import win32com.client
    SAPI_AVAILABLE = True
except ImportError:
    SAPI_AVAILABLE = False

# Check for SpeechRecognition
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False


class OfflineVoiceEngine:
    def __init__(self, voice_speed: int = 1):
        self.sapi_voice = None
        self.lock = threading.Lock()
        if SAPI_AVAILABLE:
            try:
                self.sapi_voice = win32com.client.Dispatch("SAPI.SpVoice")
                # Speed rate from -10 to 10
                self.sapi_voice.Rate = voice_speed
            except Exception as e:
                print(f"[VoiceEngine] Warning: SAPI initialization failed: {e}")

    def speak(self, text: str, block: bool = True):
        """Speaks text aloud using local Windows speech synthesizer."""
        clean_text = text.replace("*", "").replace("#", "").replace("`", "")
        if not self.sapi_voice:
            # Fallback console printing
            print(f"[AI Voice Output]: {clean_text}")
            return

        def _run_speak():
            with self.lock:
                try:
                    # SVSFlagsAsync = 1, SVSFDefault = 0
                    flags = 0 if block else 1
                    self.sapi_voice.Speak(clean_text, flags)
                except Exception as e:
                    print(f"[VoiceEngine Error] {e}")

        if block:
            _run_speak()
        else:
            threading.Thread(target=_run_speak, daemon=True).start()

    def stop_speaking(self):
        """Immediately interrupts current speech."""
        if self.sapi_voice:
            try:
                # 2 = SVSFPurgeBeforeSpeak
                self.sapi_voice.Speak("", 2)
            except Exception:
                pass


class ConversationalCallLoop:
    """
    Continuous 'Always-On Call' interface:
    Maintains an open call session between the human and AI agent.
    Captures input via microphone or duplex terminal, triggers the autonomous reasoning loop,
    and replies with conversational voice response until explicit hang-up.
    """
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
        print("\n" + "=" * 65)
        print(" [NEXUS-226] DUPLEX VOICE CALL CONNECTED (ALWAYS ON)")
        print(" Mode: Real-Life One-on-One Voice Conversation")
        print(" Speak freely into your mic or type text below.")
        print(" Say or type 'hang up', 'goodbye', or 'shut down' to end call.")
        print("=" * 65 + "\n")

        # Initial call greeting
        greeting = "Nexus online. I am connected and listening. How can I assist you with the machine, transactions, or any AI architecture?"
        print(f"\nAI: {greeting}\n")
        self.voice.speak(greeting, block=True)

        while self.is_active:
            user_input = self._listen_or_prompt()
            if not user_input:
                continue

            clean_input = user_input.strip().lower()
            if clean_input in ["hang up", "end call", "disconnect", "shut down", "exit", "quit"]:
                farewell = "Call ended. Entering standby mode."
                print(f"\nAI: {farewell}\n")
                self.voice.speak(farewell, block=True)
                self.is_active = False
                break

            print(f"\n[User]: {user_input}")
            print("[Nexus-226]: Thinking & Processing...")

            # Run agent response
            try:
                response = self.agent_responder(user_input)
            except Exception as e:
                response = f"I encountered an error executing that request: {str(e)}"

            print(f"[AI]: {response}\n")
            # Speak the response aloud like a real-time call
            self.voice.speak(response, block=True)

    def _listen_or_prompt(self) -> Optional[str]:
        """Tries listening via microphone; falls back smoothly to interactive prompt if mic is busy."""
        if self.recognizer and self.mic:
            try:
                print(">> [Listening... speak now or press Enter to type] ", end="", flush=True)
                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=10)
                print("\n[Processing voice input...]")
                text = self.recognizer.recognize_sphinx(audio) if hasattr(self.recognizer, "recognize_sphinx") else None
                if text:
                    return text
            except Exception:
                # If mic times out or error, allow typing
                pass

        try:
            val = input(">> [Speak/Type]: ")
            return val
        except (EOFError, KeyboardInterrupt):
            self.is_active = False
            return "hang up"

if __name__ == "__main__":
    def dummy_responder(query: str) -> str:
        return f"Acknowledged query regarding '{query}'. All subsystems operational."

    call = ConversationalCallLoop(agent_responder=dummy_responder)
    print("Testing Voice Engine directly...")
    call.voice.speak("Offline voice engine initialized successfully.", block=True)

