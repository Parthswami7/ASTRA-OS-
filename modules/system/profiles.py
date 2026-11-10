import os
import subprocess
import psutil
import sys

def execute_workspace_profile(profile_name):
    profile_name = profile_name.lower()
    
    if "development" in profile_name or "code" in profile_name:
        print("[ASTRA-PROFILE] Engaging Protocol: Development...")
        
        # 1. Set Windows Power Plan to Balanced/Performance
        os.system("powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c") 
        
        # 2. Launch VS Code smoothly
        try:
            # shell=True helps Windows resolve 'code' from the PATH environment variable
            subprocess.Popen("code", shell=True)
        except Exception as e:
            print(f"[PROFILE ERROR] Could not launch VS Code: {e}")
            
        # We NO LONGER launch server.py here, because main.py already runs the master brain!
        
        return "Protocol Development is fully engaged. VS Code is online and system power is optimized, Sir."

    elif "gaming" in profile_name or "game" in profile_name:
        print("[ASTRA-PROFILE] Engaging Protocol: Gaming...")
        
        # 1. Kill background memory hogs to free up 16GB RAM for gaming
        target_processes = ["chrome.exe", "msedge.exe", "discord.exe", "spotify.exe"]
        killed_count = 0
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() in target_processes:
                    proc.kill()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        return f"Protocol Gaming engaged. Freed resources by terminating {killed_count} background tasks, Sir."

    return "Unknown profile requested, Sir."