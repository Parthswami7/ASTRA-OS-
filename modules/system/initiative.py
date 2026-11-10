import psutil
import time
import threading
import sys

class InitiativeProtocol:
    def __init__(self, voice_interface):
        self.voice = voice_interface
        self.battery_warned = False
        self.cpu_warned = False
        self.ram_warned = False

        # 1. VIP WHITELIST: A.S.T.R.A will NEVER touch these processes
        self.whitelist = [
            'python.exe', 'explorer.exe', 'system', 'svchost.exe', 'csrss.exe',
            'wininit.exe', 'smss.exe', 'services.exe', 'lsass.exe', 'spoolsv.exe',
            'cmd.exe', 'tesseract.exe', 'code.exe', 'igi.exe', 'igi2.exe', 
            'gtaiv.exe', 'gtav.exe', 'hd-player.exe'
        ]
        
        # 2. THE KILL LIST: Windows bloatware that is safe to terminate
        self.kill_list = [
            'widgets.exe', 'msteams.exe', 'yourphone.exe', 'cortana.exe', 'skype.exe', 'onedrive.exe'
        ]

    def optimize_system(self):
        """Scans the memory and kills bloatware / throttles heavy background apps."""
        freed_ram = 0
        throttled_count = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                p_info = proc.info
                p_name = p_info['name'].lower() if p_info['name'] else ""
                
                if p_name in self.whitelist:
                    continue
                    
                # Action 1: Terminate Bloatware
                if p_name in self.kill_list:
                    freed_ram += p_info['memory_info'].rss
                    proc.kill()
                    continue
                    
                # Action 2: Throttle CPU Priority of heavy background tasks
                # If a non-VIP app is eating CPU, starve it and give power back to the OS
                if proc.cpu_percent(interval=0) > 2.0 or proc.memory_percent() > 2.0:
                    if sys.platform == 'win32':
                        proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                        throttled_count += 1
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Ignore system processes that Windows denies access to
                pass
        
        # Convert freed bytes to Megabytes
        freed_mb = int(freed_ram / (1024 * 1024))
        return freed_mb, throttled_count

    def monitor_system(self):
        while True:
            try:
                # 1. BATTERY INITIATIVE
                battery = psutil.sensors_battery()
                if battery:
                    if battery.percent <= 20 and not battery.power_plugged:
                        if not self.battery_warned:
                            self.voice.speak(f"Excuse me Sir, your battery is critically low at {battery.percent} percent. I strongly recommend plugging in.")
                            self.battery_warned = True
                    elif battery.power_plugged:
                        self.battery_warned = False

                # 2. CPU INITIATIVE & AUTO-OPTIMIZATION
                cpu_usage = psutil.cpu_percent(interval=1)
                if cpu_usage > 85:
                    if not self.cpu_warned:
                        self.voice.speak(f"Warning. CPU usage has spiked to {cpu_usage} percent. Engaging automatic thermal optimization.")
                        freed_mb, throttled = self.optimize_system()
                        self.voice.speak(f"Optimization complete. I have throttled {throttled} background processes to stabilize the CPU.")
                        self.cpu_warned = True
                else:
                    if cpu_usage < 70:
                        self.cpu_warned = False 

                # 3. RAM INITIATIVE & AUTO-OPTIMIZATION
                ram_usage = psutil.virtual_memory().percent
                if ram_usage > 85:
                    if not self.ram_warned:
                        self.voice.speak(f"Sir, RAM load has exceeded 85 percent. Initiating memory purge protocol.")
                        freed_mb, throttled = self.optimize_system()
                        if freed_mb > 0:
                            self.voice.speak(f"Memory purge complete. I have cleared {freed_mb} megabytes of bloatware from the memory.")
                        else:
                            self.voice.speak(f"Optimization complete. I have throttled {throttled} background apps to free up resources.")
                        self.ram_warned = True
                else:
                    if ram_usage < 75:
                        self.ram_warned = False

            except Exception as e:
                print(f"[ASTRA-INITIATIVE] Monitoring error: {e}")
            
            # Check vitals every 20 seconds
            time.sleep(20)

    def start(self):
        print("[ASTRA] Initiative Protocol Engaged. Proactive monitoring and Auto-Optimization online.")
        threading.Thread(target=self.monitor_system, daemon=True).start() 