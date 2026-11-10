import datetime
import wikipedia
import requests
import re
import urllib.parse
import sqlite3
import os
import warnings
from ddgs import DDGS

# Suppress the annoying BeautifulSoup warning from the Wikipedia library
warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')

class AstraBrain:
    def __init__(self):
        self.contacts = {
            "bro": "+919828654468", 
            "mummy": "+91964922458",
            "dad": "+918432051000"
        }
        
        # --- PERMANENT MEMORY VAULT (SQLite) ---
        self.db_path = os.path.join(os.path.dirname(__file__), "astra_memory.db")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create the vault table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_query TEXT,
                astra_response TEXT
            )
        ''')
        self.conn.commit()
        
        self.chat_memory = []
        self._load_boot_memory()

    def _load_boot_memory(self):
        """Loads the last 5 interactions from the SQLite vault into RAM on boot."""
        try:
            self.cursor.execute('SELECT user_query, astra_response FROM memory_vault ORDER BY id DESC LIMIT 5')
            rows = self.cursor.fetchall()
            for row in reversed(rows):
                self.chat_memory.append(f"User asked: '{row[0]}' -> ASTRA replied: '{row[1]}'")
        except Exception as e:
            print(f"[MEMORY VAULT ERROR] Could not load boot memory: {e}")
            
    def _save_interaction(self, user_text, astra_reply):
        """Saves the chat to the hard drive permanently and updates short-term RAM."""
        try:
            self.cursor.execute('INSERT INTO memory_vault (user_query, astra_response) VALUES (?, ?)', (user_text, astra_reply))
            self.conn.commit()
            
            self.chat_memory.append(f"User asked: '{user_text}' -> ASTRA replied: '{astra_reply}'")
            if len(self.chat_memory) > 5:
                self.chat_memory.pop(0)
        except Exception as e:
            print(f"[MEMORY VAULT ERROR] Could not save interaction: {e}")

    def process_command(self, text):
        text = text.lower()
        
        # A.S.T.R.A Identity cleanup
        text = text.replace("astra", "").replace("अस्त्र", "").replace("एस्ट्रा", "").strip()
        
        hinglish_words = ["kaise", "kholo", "kya", "bhejo", "tum", "kaun", "haal", "mausam", "karo", "batao", "samay", "baj rahe"]
        is_hindi = bool(re.search(r'[\u0900-\u097F]', text)) or any(w in text.split() for w in hinglish_words)

        # 1. Basic Greetings 
        greeting_triggers = ["hi", "hello", "hey", "wake up", "how are you", "how r u", "kaise ho", "kya haal", "हाउ आर यू", "कैसे हो", "नमस्ते", "namaste"]
        if text in greeting_triggers:
            reply = "नमस्ते सर, मैं आपकी सेवा में हाज़िर हूँ।" if is_hindi else "Hello, Sir. All systems are online and ready for your commands."
            self._save_interaction(text, reply)
            return reply
            
        if any(who in text for who in ["who are you", "tum kaun ho", "हू आर यू"]):
            reply = "मैं अस्त्र हूँ, आपका पर्सनल आर्टिफिशियल इंटेलिजेंस सिस्टम।" if is_hindi else "I am A.S.T.R.A, your personal artificial intelligence operating system."
            self._save_interaction(text, reply)
            return reply
            
        # 2. Live Time and Date
        if any(time_word in text for time_word in ["time", "samay", "kya time", "baj rahe", "टाइम"]):
            now = datetime.datetime.now().strftime("%I:%M %p")
            reply = f"सर, अभी टाइम हो रहा है {now}।" if is_hindi else f"The current time is {now}, Sir."
            self._save_interaction(text, reply)
            return reply

        # 3. WEATHER PROTOCOL
        if any(weather in text for weather in ["weather", "temperature", "mausam", "मौसम"]):
            try:
                url = "https://wttr.in/Sikar?format=%C+with+a+temperature+of+%t"
                response = requests.get(url)
                if response.status_code == 200:
                    weather_data = response.text.replace("+", " ")
                    reply = f"सीकर का मौसम अभी {weather_data} है।" if is_hindi else f"The weather currently is {weather_data}."
                    self._save_interaction(text, reply)
                    return reply
                
                reply = "माफ़ करना सर, मैं वेदर सर्वर से कनेक्ट नहीं कर पा रहा हूँ।" if is_hindi else "I am unable to connect to the weather satellites at the moment."
                return reply
            except Exception:
                reply = "वेदर सर्विस अभी ऑफलाइन है।" if is_hindi else "Weather services are currently offline."
                return reply
            
        # --- SHARED TRIGGERS ---
        open_triggers = ["open ", " kholo", " खोलें", " खोलो", "ओपन "]
        is_open_cmd = any(trigger in text for trigger in open_triggers)
        
        tablet_triggers = ["tablet", "tab", "phone", "टैबलेट", "फ़ोन", "टेबलेट"]
        is_tablet_cmd = any(trigger in text for trigger in tablet_triggers)
        
        # 4. STRICT SYSTEM CONTROL (LAPTOP ONLY)
        if is_open_cmd and not is_tablet_cmd:
            app_name = text
            for trigger in open_triggers:
                app_name = app_name.replace(trigger, "")
            
            app_name = app_name.strip()
            if not app_name:
                return "सर, आप कौनसी एप्लीकेशन ओपन करना चाहते हैं?" if is_hindi else "What specific application would you like me to open, sir?"
            return f"OPEN_APP:{app_name}"

        # --- MEDIA PLAYER PROTOCOL ---
        if any(w in text for w in ["play", "प्ले", "गाना", "song", "music", "म्यूजिक"]):
            song_name = text.replace("प्ले", "").replace("play", "").replace("गाना बजाओ", "").replace("song", "").replace("music", "").replace("म्यूजिक", "").strip()
            return f"MEDIA_CMD:{song_name}"

        # 5. WHATSAPP AUTOMATION
        if "whatsapp" in text and any(msg in text for msg in ["message", "bhejo", "send"]):
            try:
                contact_name = text.split("to ")[1].split(" saying")[0].strip()
                message_content = text.split("saying ")[1].strip()
                
                if contact_name in self.contacts:
                    phone_number = self.contacts[contact_name]
                    return f"WHATSAPP_MSG:{phone_number}:{message_content}"
                else:
                    return f"सर, मेरे पास {contact_name} का नंबर सेव नहीं है।" if is_hindi else f"Sir, I do not have a contact saved for {contact_name}."
            except Exception:
                return "Command samajh nahi aayi. Format: send a WhatsApp message to [name] saying [message]."

        # 5.5 ANDROID TABLET CONTROL PROTOCOL
        if is_tablet_cmd:
            if any(o in text for o in ["open", "launch", "kholo", "खोलो", "ओपन"]):
                app_map = {
                    "youtube": "com.google.android.youtube",
                    "युटुब": "com.google.android.youtube",
                    "यूट्यूब": "com.google.android.youtube",
                    "chrome": "com.android.chrome",
                    "क्रोम": "com.android.chrome",
                    "camera": "com.sec.android.app.camera",
                    "कैमरा": "com.sec.android.app.camera",
                    "whatsapp": "com.whatsapp",
                    "व्हाट्सएप": "com.whatsapp",
                    "वोट्सएप": "com.whatsapp"
                }
                for app_name, package in app_map.items():
                    if app_name in text:
                        return f"ANDROID_CMD:app:{package}"
            
            if any(w in text for w in ["unlock", "wake", "अनलॉक"]):
                return "ANDROID_CMD:unlock"
            
            if any(w in text for w in ["lock", "sleep", "बंद करो", "लॉक"]):
                return "ANDROID_CMD:lock"
                
            if any(w in text for w in ["shutdown", "shut down", "power off", "टर्न ऑफ", "शटडाउन", "शट डाउन"]):
                return "ANDROID_CMD:shutdown"
            
            if any(w in text for w in ["battery", "बैटरी", "चार्ज"]):
                return "ANDROID_CMD:battery"
            
            return "ANDROID_CMD:unlock"

        # 5.6 CODE GENERATOR PROTOCOL
        if any(w in text for w in ["write code", "code a", "python script", "write a script", "create a website", "program for", "write an html"]):
            return f"CODE_CMD:{text}"

        # 5.7 SCREEN VISION DEBUGGER PROTOCOL
        vision_triggers = ["look at my screen", "fix this error", "read my screen", "debug this", "what's on my screen", "see my screen", "check my screen", "scan my screen"]
        if any(w in text for w in vision_triggers):
            return "VISION_CMD:analyze"

        # 5.8 GESTURE CONTROL & PROFILES
        text_lower = text.lower()
        if "gesture" in text_lower or "hand tracking" in text_lower or "hud" in text_lower:
            return "GESTURE_CMD:start"      
        if "protocol" in text_lower or "workspace" in text_lower or "gaming mode" in text_lower or "dev mode" in text_lower:
            return f"PROFILE_CMD:{text_lower}"
            
        # 5.9 WINDOW MANAGER PROTOCOL
        window_triggers = ["minimize all", "show desktop", "maximize", "minimize window", "minimize this", "close window", "close this", "snap left", "snap right", "switch window", "next window"]
        if any(w in text_lower for w in window_triggers):
            return f"WINDOW_CMD:{text_lower}"

        # 5.10 THE VAULT SEARCH PROTOCOL
        vault_triggers = ["find my ", "search my files for ", "find the file ", "open the folder ", "find folder "]
        for trigger in vault_triggers:
            if trigger in text_lower:
                query = text_lower.split(trigger)[-1].strip()
                query = query.replace("folder", "").replace("file", "").strip()
                return f"VAULT_CMD:{query}"
                
        # 5.11 HARDWARE & POWER PROTOCOL
        hardware_triggers = ["battery", "brightness", "bluetooth"]
        if any(w in text_lower for w in hardware_triggers):
            return f"HARDWARE_CMD:{text_lower}"
        
        # 5.12 WEB SEARCH PROTOCOL
        if "search for" in text_lower or "सर्च फॉर" in text_lower or "सर्च" in text_lower:
            if "search for" in text_lower:
                query = text_lower.split("search for")[-1].strip()
            elif "सर्च फॉर" in text_lower:
                query = text_lower.split("सर्च फॉर")[-1].strip()
            else:
                query = text_lower.split("सर्च")[-1].strip()
                
            query = query.replace("चैट गुप्त", "chatgpt").replace("chat gupt", "chatgpt")
            return f"WEB_SEARCH:{query}"
        
        # 6. GENERAL AI CHAT (WITH PERMANENT DATABASE INTEGRATION)
        try:
            context_string = ""
            if self.chat_memory:
                context_string = "[Recent Context: " + " | ".join(self.chat_memory) + "] "
            
            full_prompt = context_string + "Current User Query: " + text
            safe_query = urllib.parse.quote(full_prompt)
            local_ai_url = f"http://127.0.0.1:5000/ask/{safe_query}"
            
            response = requests.get(local_ai_url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    answer = data.get("answer").replace("*", "").replace("#", "")
                    self._save_interaction(text, answer)
                    return answer
            raise Exception("Local AI Unreachable")
            
        except Exception as local_e:
            try:
                context_string = ""
                if self.chat_memory:
                    context_string = " Recent Context: " + " | ".join(self.chat_memory)
                
                if is_hindi:
                    prompt = f"You are ASTRA. Answer concisely in 1 or 2 short sentences. You MUST reply entirely in pure Hindi using the Devanagari script (e.g., नमस्ते).{context_string} Current User input: {text}"
                else:
                    prompt = f"You are ASTRA. Answer concisely in 1 or 2 short sentences in English.{context_string} Current User input: {text}"
                    
                answer = DDGS().chat(prompt, model='gpt-4o-mini')
                if answer:
                    answer_clean = answer.replace("*", "").replace("#", "")
                    self._save_interaction(text, answer_clean)
                    return answer_clean
            except Exception as ddg_e:
                try:
                    search_term = text.replace("what is", "").replace("who is", "").replace("kya hai", "").replace("kaun hai", "").strip()
                    summary = wikipedia.summary(search_term, sentences=1)
                    self._save_interaction(text, summary)
                    return summary 
                except Exception:
                    reply = "सर, मेरा वेब कनेक्शन ब्लॉक हो गया है।" if is_hindi else "Sir, my connection to the external web is currently blocked."
                    return reply

        return "मैंने सुन लिया सर, पर इस कमांड के लिए अभी कोई प्रोटोकॉल सेट नहीं है।" if is_hindi else "I heard you, sir, but I don't have a specific protocol for that command yet."