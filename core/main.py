import sys
import os
import time
import subprocess
import requests
import urllib.parse
import threading
import pyautogui

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from modules.system.omni_daemon import OmniDaemon

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

omni = OmniDaemon()
omni.start_all_watchers()

def start_standalone_app():
    window_path = os.path.join(PROJECT_ROOT, "ui", "app_window.py")
    subprocess.Popen([sys.executable, window_path])

def trigger_system_lockdown(action="lock"):
    if action == "lock":
        from modules.system.custom_lock import execute_custom_lockdown
        execute_custom_lockdown()
    elif action == "signout":
        os.system("shutdown /l")
    elif action == "shutdown":
        os.system("shutdown /s /t 5")

def main():
    print("==================================")
    print("  A.S.T.R.A OS - SHIELD ACTIVATED ")
    print("==================================")

    # --- PROJECT GLASS SECURITY PROTOCOL ---
    from modules.system.project_glass import verify_master
    from modules.system.custom_lock import execute_custom_lockdown
    
    print("[ASTRA] Initiating Project Glass Webcam Scan...")
    if verify_master():
        print("[SYSTEM] Biometric Verified. Master Recognized.")
    else:
        print("[SYSTEM] ACCESS DENIED. INTRUDER DETECTED. ENGAGING LOCKDOWN.")
        execute_custom_lockdown() 

    print("[SYSTEM] Loading Web Core in background...")

    server_path = os.path.join(PROJECT_ROOT, "ui", "server.py")
    subprocess.Popen([sys.executable, server_path])

    # 3. WAIT FOR FLASK & LLAMA 3.2 TO COME ONLINE BEFORE LISTENING
    print("[SYSTEM] Waiting for Neural Net and Flask Server to finish booting...")
    for _ in range(30):
        try:
            requests.get("http://127.0.0.1:5000/security_status", timeout=1)
            print("[SYSTEM] Neural Net Server Verified Online!")
            break
        except Exception:
            time.sleep(1)

    from modules.voice.stt_tts import VoiceInterface
    from core.logic_core import AstraBrain
    from modules.system.app_launcher import execute as launch_app
    from modules.system.android_link import AndroidController
    from modules.system.media_player import play_music

    brain = AstraBrain()
    tab = AndroidController() 
    start_standalone_app()

    print("[SYSTEM] All systems nominal. Awaiting voice commands...")
    voice = VoiceInterface()

    # --- NEW: WAKE UP THE INITIATIVE PROTOCOL ---
    from modules.system.initiative import InitiativeProtocol
    proactive_brain = InitiativeProtocol(voice)
    proactive_brain.start()
    # --------------------------------------------

    sentry_triggers = [
        "sentry", "century", "entry mode", "sanitary", "guard", "secure", "lockdown",
        "सेंट्री", "सेनेटरी", "सैनिटरी", "सेंड रिमोट", "एंट्री मोड", 
        "लॉकडाउन", "लॉक डाउन", "सिक्योर", "गार्ड", "सिस्टम लॉक"
    ]

    dictation_mode = False
    dictation_start_triggers = ["activate dictation mode", "start ghost writer", "start typing", "enable dictation"]
    dictation_exit_triggers = ["stop dictation", "exit ghost writer", "stop typing", "disable dictation"]

    while True:
        try: 
            user_command = voice.listen()

            if user_command:
                print(f"\nParth Sir: {user_command}")
                command_lower = user_command.lower()

                if dictation_mode:
                    if any(phrase in command_lower for phrase in dictation_exit_triggers):
                        dictation_mode = False
                        voice.speak("Ghost Writer deactivated. I am back in command mode, Sir.")
                        continue
                    else:
                        pyautogui.write(user_command + " ", interval=0.015)
                        continue
                else:
                    if any(phrase in command_lower for phrase in dictation_start_triggers):
                        dictation_mode = True
                        voice.speak("Ghost Writer activated. I am now connected directly to your keyboard, Sir.")
                        continue

                if any(phrase in command_lower for phrase in sentry_triggers):
                    voice.speak("Sentry mode armed. I am locking the system and watching the cameras, Sir.")
                    trigger_system_lockdown(action="lock")
                    continue 
                
                if "copy the selected code" in command_lower or "copy this" in command_lower:
                    pyautogui.hotkey('ctrl', 'c')
                    voice.speak("Code copied to clipboard, Sir.")
                    continue

                ai_reply = brain.process_command(user_command)

                if ai_reply.startswith("OPEN_APP:"):
                    app_name = ai_reply.replace("OPEN_APP:", "").strip()
                    app_reply = launch_app(app_name)
                    voice.speak(app_reply)

                elif ai_reply.startswith("WEB_SEARCH:"):
                    query = ai_reply.split(":", 1)[1].strip()
                    voice.speak(f"Right away, Sir. Searching the web for {query}.")

                    def perform_web_search():
                        import webbrowser
                        import urllib.parse
                        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                        webbrowser.open(search_url)

                    threading.Thread(target=perform_web_search, daemon=True).start()

                elif ai_reply.startswith("WHATSAPP_MSG:"):
                    parts = ai_reply.split(":", 2)
                    phone = parts[1]
                    msg = parts[2]

                    voice.speak("Right away, Sir. Accessing the WhatsApp desktop system.")

                    def send_native_whatsapp():
                        try:
                            encoded_msg = urllib.parse.quote(msg)
                            uri = f"whatsapp://send?phone={phone}&text={encoded_msg}"
                            import webbrowser
                            webbrowser.open(uri)
                            time.sleep(6) 
                            pyautogui.press('enter')
                        except Exception as e:
                            print(f"[ASTRA-SYS] WhatsApp Protocol Failed: {e}")

                    threading.Thread(target=send_native_whatsapp, daemon=True).start()

                elif ai_reply.startswith("ANDROID_CMD:"):
                    cmd_parts = ai_reply.split(":")
                    action = cmd_parts[1]

                    if action == "unlock":
                        voice.speak("Accessing the tablet now, Sir.")
                        threading.Thread(target=tab.wake_and_unlock, daemon=True).start()

                    elif action == "app":
                        package_name = cmd_parts[2]
                        voice.speak("Establishing bridge. Launching the application on your tablet.")

                        def launch_tab_app():
                            tab.wake_and_unlock()
                            time.sleep(1.5) 
                            tab.launch_app(package_name)

                        threading.Thread(target=launch_tab_app, daemon=True).start()

                    elif action == "lock":
                        voice.speak("Locking the tablet screen, Sir.")
                        threading.Thread(target=tab.lock_screen, daemon=True).start()

                    elif action == "shutdown":
                        voice.speak("Powering down the tablet completely.")
                        threading.Thread(target=tab.power_off, daemon=True).start()

                    elif action == "battery":
                        def check_tab_battery():
                            voice.speak("Checking the tablet's battery level, Sir.")
                            level = tab.get_battery_level()
                            if level != "Unknown":
                                voice.speak(f"The tablet is currently at {level} battery.")
                            else:
                                voice.speak("I am unable to read the battery sensor at this time.")
                        threading.Thread(target=check_tab_battery, daemon=True).start()

                elif ai_reply.startswith("MEDIA_CMD:"):
                    song_query = ai_reply.split(":")[1].strip()
                    if song_query:
                        voice.speak(f"Searching for {song_query} in your music library, Sir.")
                    else:
                        voice.speak("Opening your music collection, Sir.")

                    def execute_media():
                        result_msg = play_music(song_query)
                        voice.speak(result_msg)

                    threading.Thread(target=execute_media, daemon=True).start()

                elif ai_reply.startswith("VISION_CMD:"):
                    voice.speak("Scanning your display and analyzing code traces, Sir.")
                    def execute_vision():
                        from modules.system.screen_vision import analyze_current_screen
                        diagnosis = analyze_current_screen()
                        voice.speak(diagnosis)
                    threading.Thread(target=execute_vision, daemon=True).start()

                elif ai_reply.startswith("GESTURE_CMD:"):
                    voice.speak("Activating Iron Man hand-tracking HUD. Pinch to adjust volume or raise palm to lock.")
                    def run_gestures():
                        from modules.system.gesture_control import start_gesture_listener
                        start_gesture_listener()
                    threading.Thread(target=run_gestures, daemon=True).start()

                elif ai_reply.startswith("PROFILE_CMD:"):
                    profile_query = ai_reply.split(":", 1)[1].strip()
                    def run_profile():
                        from modules.system.profiles import execute_workspace_profile
                        msg = execute_workspace_profile(profile_query)
                        voice.speak(msg)
                    threading.Thread(target=run_profile, daemon=True).start()

                elif ai_reply.startswith("CODE_CMD:"):
                    prompt = ai_reply.split(":", 1)[1].strip()
                    voice.speak("Compiling the architecture now, Sir. Please wait a moment.")

                    def execute_code_gen():
                        from modules.system.coder import generate_and_save_code
                        result_msg = generate_and_save_code(prompt)
                        voice.speak(result_msg)

                    threading.Thread(target=execute_code_gen, daemon=True).start()
                    
                elif ai_reply.startswith("WINDOW_CMD:"):
                    win_cmd = ai_reply.split(":", 1)[1].strip()
                    def run_window_manager():
                        from modules.system.window_manager import execute_window_command
                        msg = execute_window_command(win_cmd)
                        voice.speak(msg)
                    threading.Thread(target=run_window_manager, daemon=True).start()

                elif ai_reply.startswith("VAULT_CMD:"):
                    search_query = ai_reply.split(":", 1)[1].strip()
                    voice.speak(f"Initiating deep vault search for {search_query}. This may take a moment, Sir.")
                    
                    def run_vault_search():
                        from modules.system.vault_search import search_and_open
                        msg = search_and_open(search_query)
                        voice.speak(msg)
                    threading.Thread(target=run_vault_search, daemon=True).start()
                    
                # --- NEW: HARDWARE CONTROL EXECUTION ---
                elif ai_reply.startswith("HARDWARE_CMD:"):
                    hw_cmd = ai_reply.split(":", 1)[1].strip()
                    def run_hardware_manager():
                        from modules.system.hardware_control import execute_hardware_command
                        msg = execute_hardware_command(hw_cmd)
                        voice.speak(msg)
                    threading.Thread(target=run_hardware_manager, daemon=True).start()

                else:
                    voice.speak(ai_reply)

            try:
                response = requests.get("http://127.0.0.1:5000/security_status", timeout=1)
                if response.status_code == 200:
                    status = response.json().get("status")
                    if status == "SHUTDOWN":
                        trigger_system_lockdown(action="shutdown") 
                        requests.get("http://127.0.0.1:5000/reset_security", timeout=1)
            except Exception:
                pass 

        except KeyboardInterrupt:
            print("\n[SYSTEM] Shutting down A.S.T.R.A...")
            break
        except Exception as e:
            print(f"[ERROR]: {e}")

if __name__ == "__main__":
    main()