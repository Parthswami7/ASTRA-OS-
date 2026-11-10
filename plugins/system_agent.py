import os
import platform
import pyautogui
import subprocess

class SystemAutomationAgent:
    def __init__(self):
        self.os_type = platform.system()
        print("[ASTRA-SYS] System Automation Module Online.")

    def execute_task(self, task_command):
        task_command = task_command.lower()
        
        # --- Advanced OS Controls ---
        if "type " in task_command:
            text_to_type = task_command.split("type ")[1]
            pyautogui.write(text_to_type, interval=0.05)
            return f"Typed: {text_to_type}"
            
        elif "press enter" in task_command:
            pyautogui.press('enter')
            return "Executed carriage return."
            
        elif "empty trash" in task_command or "empty recycle bin" in task_command:
            if self.os_type == "Windows":
                try:
                    import ctypes
                    # The Windows API code to silently empty the recycle bin
                    ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
                    return "Recycle bin incinerated, sir."
                except:
                    return "Error accessing system waste protocols."
                    
        return "Task not recognized by the Automation Agent."

# Instantiate the plugin
system_agent = SystemAutomationAgent()