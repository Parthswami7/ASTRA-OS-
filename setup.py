import os

print("Building ASTRA folders...")

# 1. Create the ASTRA_brain folder
os.makedirs("ASTRA_brain", exist_ok=True)

# 2. Create the __init__.py file
with open("ASTRA_brain/__init__.py", "w") as f:
    f.write("# This tells Python this is a module\n")

# 3. Create the logic_core.py file
logic_core_code = """
class ASTRABrain:
    def __init__(self, hardware_profile="low_end"):
        self.hardware = hardware_profile
        
    def process_command(self, text, language="en"):
        return "conversation"
"""
with open("ASTRA_brain/logic_core.py", "w") as f:
    f.write(logic_core_code)

print("SUCCESS: ASTRA_brain folder and logic_core.py created perfectly!") 