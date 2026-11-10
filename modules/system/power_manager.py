import os

def execute_power_command(command: str):
    command_lower = command.lower()

    if "shutdown" in command_lower or "turn off pc" in command_lower:
        os.system("shutdown /s /t 5") # Shuts down in 5 seconds
        return "Shutting down the system now, Parth_Sir. Goodbye."

    elif "restart" in command_lower:
        os.system("shutdown /r /t 5")
        return "Initiating system restart, Parth_Sir."

    elif "sleep" in command_lower or "lock" in command_lower:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking the system, Parth_Sir."

    return None