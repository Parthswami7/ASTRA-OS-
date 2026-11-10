import subprocess
import time
import re
import threading

class AndroidController:
    def __init__(self):
        self.target_ip = "192.168.1.28" 
        
        print(f"[ASTRA-SYS] Initializing Wireless ADB Bridge to {self.target_ip}...")
        subprocess.run("adb start-server", shell=True, capture_output=True)
        self.connect_device()
        
        # Start a background thread to keep the Wi-Fi port awake so it never goes "offline"
        threading.Thread(target=self._keep_alive_loop, daemon=True).start()

    def connect_device(self):
        subprocess.run("adb disconnect", shell=True, capture_output=True)
        subprocess.run(f"adb connect {self.target_ip}:5555", shell=True, capture_output=True)

    def _keep_alive_loop(self):
        while True:
            time.sleep(120) # Every 2 minutes, ping the tablet silently
            try:
                subprocess.run(f"adb -s {self.target_ip}:5555 shell echo 'keepalive'", shell=True, capture_output=True)
            except Exception:
                pass

    def execute_adb(self, command):
        try:
            target = f"-s {self.target_ip}:5555"
            result = subprocess.run(f"adb {target} shell {command}", shell=True, capture_output=True, text=True)
            
            if result.stderr and "daemon" not in result.stderr:
                print(f"[ADB HIDDEN ERROR]: {result.stderr.strip()}")
                
            return result.stdout
        except Exception as e:
            print(f"[ASTRA-ADB CRASH]: {e}")
            return None

    def wake_and_unlock(self):
        print("[ASTRA-ADB] Waking device wirelessly...")
        self.execute_adb("input keyevent 224")
        time.sleep(1)
        
        print("[ASTRA-ADB] Swiping to unlock...")
        self.execute_adb("input swipe 400 1000 400 200 300")
        time.sleep(0.5)
        self.execute_adb("input keyevent 82")

    def launch_app(self, package_name):
        print(f"[ASTRA-ADB] Launching {package_name} over Wi-Fi...")
        self.execute_adb(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
        
    def lock_screen(self):
        print("[ASTRA-ADB] Locking tablet screen wirelessly...")
        self.execute_adb("input keyevent 26")

    def power_off(self):
        print("[ASTRA-ADB] Initiating wireless tablet shutdown sequence...")
        self.execute_adb("reboot -p")

    def get_battery_level(self):
        print("[ASTRA-ADB] Checking tablet battery level...")
        output = self.execute_adb("dumpsys battery")
        if output:
            match = re.search(r'level:\s+(\d+)', output)
            if match:
                return f"{match.group(1)}%"
        return "Unknown"