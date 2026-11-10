import tkinter as tk
import threading
import keyboard
import time
import sys
import os

# Ensure we can find the fingerprint engine
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(PROJECT_ROOT)

from modules.vision.fingerprint_engine import authenticate

class ASTRALockScreen:
    def __init__(self):
        self.root = tk.Tk()
        # Make it full screen and borderless
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        self.root.config(cursor="none") # Hides mouse cursor

        # Cinematic Status Text
        self.label = tk.Label(self.root, text="[ SYSTEM LOCKED ]\n\nAWAITING BIOMETRIC SIGNATURE", 
                              fg="#00f3ff", bg="black", font=("Courier New", 24, "bold"))
        self.label.pack(expand=True)

        self.block_inputs()
        
        # Start the fingerprint scanner in the background
        threading.Thread(target=self.scan_loop, daemon=True).start()

    def block_inputs(self):
        for i in range(150):
            try:
                keyboard.block_key(i)
            except:
                pass

    def unblock_inputs(self):
        keyboard.unhook_all()

    def scan_loop(self):
        time.sleep(0.5) 
        while True:
            try:
                result = authenticate()
                if result:
                    self.label.config(text="[ ACCESS GRANTED ]\n\nWELCOME BACK, SIR.", fg="#00ff00")
                    self.unblock_inputs()
                    time.sleep(1.2)
                    self.root.after(0, self.root.destroy)
                    break
                else:
                    self.label.config(text="[ BIOMETRIC FAILED ]\n\nUNAUTHORIZED USER.", fg="red")
                    
                    # Trigger silent intruder photo capture on failure
                    try:
                        from modules.system.omni_daemon import OmniDaemon
                        OmniDaemon().capture_intruder()
                    except Exception:
                        pass
                        
                    time.sleep(2)
                    self.label.config(text="[ SYSTEM LOCKED ]\n\nAWAITING BIOMETRIC SIGNATURE", fg="#00f3ff")
            except Exception as e:
                print(f"[BIOMETRIC THREAD ERROR]: {e}")
                time.sleep(1)

    def disable_event(self):
        pass 

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event) 
        self.root.mainloop()

def execute_custom_lockdown():
    print("[ASTRA-SYS] Initiating Biometric Blackout Protocol...")
    lock = ASTRALockScreen()
    lock.run()