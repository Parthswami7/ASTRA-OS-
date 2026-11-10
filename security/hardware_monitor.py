import psutil

def execute_hardware_command(command: str):
    command_lower = command.lower()

    if "cpu" in command_lower or "hardware" in command_lower or "system status" in command_lower:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        
        status_report = f"Parth_Sir, your CPU is currently at {cpu_usage} percent utilization, and RAM usage is at {ram_usage} percent."
        
        # Add a warning if the PC is under heavy load (like when running GTA or BeamNG.drive)
        if cpu_usage > 85 or ram_usage > 85:
            status_report += " System load is quite heavy right now. You might want to monitor your temperatures."
            
        return status_report

    return None