import os
from AppOpener import open as open_app

# 1. VIP GAME & CUSTOM APP DIRECTORY
CUSTOM_APP_PATHS = {
    "igi 2": r"D:\Download manager\Neat Download Manager\IGI 2 save games\IGI 2 - Covert Strike\igi2.exe",
    "igi": r"D:\Download manager\Neat Download Manager\Project IGI\IGI\Project IGI\IGI.exe",
    "project igi": r"D:\Download manager\Neat Download Manager\Project IGI\IGI\Project IGI\IGI.exe",
    "gta 4": r"D:\Download manager\Neat Download Manager\GTA IV\Play - GTA IV.exe",
    "gta 5": "steam://rungameid/271590",  
    "gta": "steam://rungameid/271590",
    "beamng": r"C:\Program Files (x86)\Steam\steamapps\common\BeamNG.drive\BeamNG.drive.exe",
    "bgmi": r"C:\Program Files\BlueStacks_nxt\HD-Player.exe"
}

def execute(command: str) -> str:
    """
    Intelligently finds and opens any installed application on the system.
    """
    app_name = command.lower().replace("open", "").replace("launch", "").strip()
    
    if not app_name:
        return "Please specify an application to open."
        
    print(f"[App Launcher] Scanning system for: {app_name}")
    
    # 1. Check custom paths first (for heavy games)
    for key in CUSTOM_APP_PATHS:
        if key == app_name or key in app_name:
            try:
                os.startfile(CUSTOM_APP_PATHS[key])
                return f"Opening {app_name}, Sir."
            except Exception as e:
                print(f"[App Launcher] Error opening custom path: {e}")
                return f"I found the VIP path for {app_name}, but encountered an error opening it. Check the file path."
    
    # 2. Use AppOpener for EVERYTHING else (WhatsApp, ChatGPT, etc.)
    try:
        # match_closest=True allows ASTRA to figure it out even if you don't say the exact perfect filename
        open_app(app_name, match_closest=True)
        return f"Opening {app_name}, Sir."
    except Exception as e:
        print(f"[App Launcher] Error: {e}")
        return f"I could not locate {app_name} on your system. It may not be installed."

# Testing block
if __name__ == "__main__":
    execute("open whatsapp")
    execute("open chatgpt")