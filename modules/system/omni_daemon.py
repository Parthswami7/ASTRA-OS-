import os
import time
import threading
import subprocess
import requests
import psutil
import pyperclip
import cv2

class OmniDaemon:
    def __init__(self):
        self.workspace = os.path.join(os.path.expanduser("~"), "Desktop", "ASTRA_Workspace")
        os.makedirs(self.workspace, exist_ok=True)
        self.last_clipboard = ""

    def start_all_watchers(self):
        print("[OMNI-DAEMON] Initializing background surveillance and telemetry...")
        
        # Start individual background threads
        threading.Thread(target=self._wifi_watchdog_loop, daemon=True).start()
        threading.Thread(target=self._clipboard_monitor_loop, daemon=True).start()
        threading.Thread(target=self._telemetry_logger_loop, daemon=True).start()

    def capture_intruder(self):
        """Intruder Photo Trap: Snaps a silent photo via webcam on biometric failure"""
        try:
            print("[SECURITY] Intruder alert triggered! Engaging camera...")
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    breach_dir = os.path.join(self.workspace, "security_breaches")
                    os.makedirs(breach_dir, exist_ok=True)
                    img_path = os.path.join(breach_dir, f"intruder_{int(time.time())}.jpg")
                    cv2.imwrite(img_path, frame)
                    print(f"[SECURITY] Intruder photo saved to: {img_path}")
                cap.release()
        except Exception as e:
            print(f"[SECURITY ERROR] Intruder capture failed: {e}")

    def _wifi_watchdog_loop(self):
        """Self-Healing Network Watchdog"""
        while True:
            try:
                # Ping Cloudflare DNS
                response = os.system("ping -n 1 1.1.1.1 >nul 2>&1")
                if response != 0:
                    print("[NETWORK] Packet loss detected. Resetting wireless transceiver...")
                    os.system('netsh interface set interface "Wi-Fi" admin=disable')
                    time.sleep(3)
                    os.system('netsh interface set interface "Wi-Fi" admin=enable')
                    print("[NETWORK] Transceiver re-enabled successfully.")
            except Exception:
                pass
            time.sleep(60) # Check every 60 seconds

    def _clipboard_monitor_loop(self):
        """Clipboard Intelligence: Watches copied text for instant actions"""
        while True:
            try:
                current_clip = pyperclip.paste()
                if current_clip != self.last_clipboard and len(current_clip) < 500:
                    self.last_clipboard = current_clip
                    # You can log or parse copied snippets here automatically
            except Exception:
                pass
            time.sleep(2)

    def _telemetry_logger_loop(self):
        """Hardware Telemetry: Logs CPU & RAM performance"""
        while True:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            if cpu > 85 or ram > 85:
                print(f"[WARNING] High Resource Load — CPU: {cpu}% | RAM: {ram}%")
            time.sleep(30)