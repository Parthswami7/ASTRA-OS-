import psutil
import os
try:
    import screen_brightness_control as sbc
except ImportError:
    pass 

def execute_hardware_command(command):
    command = command.lower()

    # 1. BATTERY DIAGNOSTICS
    if "battery" in command:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged
            time_left = battery.secsleft

            status = "plugged in and charging" if plugged else "running on battery power"
            reply = f"Your Vivobook is currently at {percent} percent battery and is {status}."
            
            # Only estimate time if not plugged in
            if not plugged and time_left != psutil.POWER_TIME_UNLIMITED:
                mins, _ = divmod(time_left, 60)
                reply += f" You have approximately {mins} minutes of power remaining, Sir."
            return reply
        return "I am unable to read the battery sensors at this moment, Sir."

    # 2. BRIGHTNESS OVERRIDE
    elif "brightness" in command:
        try:
            # Extract any numbers from the spoken command (e.g., "set brightness to 40")
            numbers = [int(s) for s in command.split() if s.isdigit()]
            
            if "increase" in command or "up" in command:
                current = sbc.get_brightness()[0]
                new_level = min(current + 20, 100)
                sbc.set_brightness(new_level)
                return f"Brightness increased to {new_level} percent."
                
            elif "decrease" in command or "down" in command or "dim" in command:
                current = sbc.get_brightness()[0]
                new_level = max(current - 20, 0)
                sbc.set_brightness(new_level)
                return f"Brightness decreased to {new_level} percent."
                
            elif numbers:
                level = numbers[0]
                sbc.set_brightness(level)
                return f"Screen brightness set to {level} percent, Sir."
                
            else:
                current = sbc.get_brightness()[0]
                return f"The screen brightness is currently at {current} percent."
        except Exception as e:
            return "I am unable to control the display brightness. Please ensure 'screen-brightness-control' is installed."

    # 3. BLUETOOTH ACCESS
    elif "bluetooth" in command:
        os.system("start ms-settings:bluetooth")
        return "I have opened the Bluetooth control deck for you, Sir."

    # 4. WI-FI OVERRIDE PROTOCOL
    elif "wifi" in command or "wi-fi" in command or "internet" in command:
        if "on" in command or "enable" in command:
            # Note: This requires ASTRA to be run as Administrator
            os.system('netsh interface set interface "Wi-Fi" admin=enable')
            return "Initializing the wireless transceiver, Sir. We should be online shortly."
        elif "off" in command or "disable" in command:
            os.system('netsh interface set interface "Wi-Fi" admin=disable')
            return "Wireless transceiver disabled. We are now completely offline."
        else:
            os.system("start ms-settings:network-wifi")
            return "I have brought up the Network routing panel for you, Sir."
        
    return "Hardware module engaged, but no valid parameters were recognized."