import os
import time
import re
import urllib.parse
import requests
from ddgs import DDGS

def generate_and_save_code(prompt):
    print(f"[ASTRA-CODER] Generating architecture for: {prompt}")
    
    # Strict prompt to force the AI to only output the code
    sys_prompt = f"Write the raw code for the following request: {prompt}. ONLY output the code inside triple backticks (```). Do not write any explanations, greetings, or text outside the backticks."
    
    code_response = ""
    
    # 1. Try your local Flask LLM endpoint first
    try:
        safe_query = urllib.parse.quote(sys_prompt)
        local_ai_url = f"[http://127.0.0.1:5000/ask/](http://127.0.0.1:5000/ask/){safe_query}"
        res = requests.get(local_ai_url, timeout=45)
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == "success":
                code_response = data.get("answer")
    except Exception:
        pass
        
    # 2. Fallback to DDGS GPT-4o-mini if local is busy or offline
    if not code_response:
        try:
            code_response = DDGS().chat(sys_prompt, model='gpt-4o-mini')
        except Exception:
            return "Sir, my compiler connection failed. I could not generate the code."
            
    # Extract only the code from inside the markdown backticks
    match = re.search(r'```[a-zA-Z]*\n(.*?)```', code_response, re.DOTALL)
    final_code = match.group(1).strip() if match else code_response.strip()
    
    # Auto-detect the required file extension
    ext = ".py"
    prompt_lower = prompt.lower()
    if "html" in prompt_lower or "website" in prompt_lower: ext = ".html"
    elif "java " in prompt_lower: ext = ".java"
    elif "javascript" in prompt_lower or " js" in prompt_lower: ext = ".js"
    elif "css" in prompt_lower: ext = ".css"
    elif "sql" in prompt_lower or "database" in prompt_lower: ext = ".sql"
    elif "flask" in prompt_lower: ext = ".py"
    
    # Create the ASTRA Workspace on your Desktop
    workspace = os.path.join(os.path.expanduser("~"), "Desktop", "ASTRA_Workspace")
    os.makedirs(workspace, exist_ok=True)
    
    # Save the file with a unique timestamp
    filename = f"build_{int(time.time())}{ext}"
    filepath = os.path.join(workspace, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_code)
        
    # Physically open the folder on your screen so you can access the file
    os.startfile(workspace)
    return "I have written the code and saved it to the ASTRA Workspace on your desktop, Sir."