import pyaudiowpatch as pyaudio
import sys
sys.modules['pyaudio'] = pyaudio

import speech_recognition as sr
import edge_tts
import asyncio
import pygame
import threading
import os
import requests
import re
import time

class VoiceInterface:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 2.5 
        
        self.is_speaking = False
        self.current_speech = "" 
        
        pygame.mixer.init()

    def listen(self):
        with sr.Microphone() as source:
            print("[Listening]...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # 1. Start recording audio from the Vivobook mic
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                
                # 2. Snapshot the state to prevent race conditions while Google STT processes
                was_speaking = self.is_speaking 
                
                command = self.recognizer.recognize_google(audio, language="en-IN")
                
                # 3. If ASTRA was talking during the recording, block the loop
                if was_speaking or self.is_speaking:
                    # Allow interrupt commands to pass through and kill the audio
                    if any(word in command.lower() for word in ["stop", "quiet", "shut up", "ruko", "chup", "bas"]):
                        if pygame.mixer.get_init():
                            pygame.mixer.music.stop()
                            print("\n[ASTRA]: Halting audio output.")
                            
                    # Unconditionally drop the command so his own voice never feeds back into main.py
                    return None 

                return command
            except Exception:
                return None

    def _speak_task(self, text):
        self.is_speaking = True
        self.current_speech = text 
        audio_file = os.path.join(os.path.dirname(__file__), "ASTRA_reply.mp3")
        
        try: requests.post("http://127.0.0.1:5000/set_speech_status", json={"is_speaking": True}, timeout=1)
        except: pass

        try:
            if re.search(r'[\u0900-\u097F]', text):
                voice_model = "hi-IN-MadhurNeural" 
            else:
                voice_model = "en-GB-RyanNeural"
                
            communicate = edge_tts.Communicate(text, voice_model, rate="+5%")
            asyncio.run(communicate.save(audio_file))
            
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Allow physical room echo to dissipate before reopening the microphone buffer
            time.sleep(0.3)
                
        except Exception as e:
            print(f"[Audio Error]: {e}")
        finally:
            self.is_speaking = False
            self.current_speech = "" 
            
            if pygame.mixer.get_init():
                pygame.mixer.music.unload()
                
            try: requests.post("http://127.0.0.1:5000/set_speech_status", json={"is_speaking": False}, timeout=1)
            except: pass

    def speak(self, text):
        print(f"[ASTRA]: {text}")
        threading.Thread(target=self._speak_task, args=(text,), daemon=True).start()