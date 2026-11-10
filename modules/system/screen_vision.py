import os
import time
import urllib.parse
import requests
from ddgs import DDGS

try:
    import mss
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    from PIL import Image
except ImportError:
    pass # Will handle gracefully if dependencies aren't pre-installed

def analyze_current_screen():
    print("[ASTRA-VISION] Snapping screen capture for debugging...")
    try:
        with mss.mss() as sct:
            # Capture primary monitor
            monitor = sct.monitors[1]
            screenshot_path = os.path.join(os.path.expanduser("~"), "Desktop", "ASTRA_Workspace", "screen_capture.png")
            
            # Take screenshot and save
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=screenshot_path)
            
            # Extract text using Tesseract OCR if available
            extracted_text = ""
            try:
                img = Image.open(screenshot_path)
                extracted_text = pytesseract.image_to_string(img)
            except Exception:
                extracted_text = "Unable to parse OCR text, analyzing visual workspace."
                
            # Formulate query for the AI
            prompt = f"Analyze this screen text or code error extracted from my development environment and provide a concise, direct fix: {extracted_text[:1000]}"
            
            # Query local model or fallback
            try:
                safe_query = urllib.parse.quote(prompt)
                res = requests.get(f"http://127.0.0.1:5000/ask/{safe_query}", timeout=20)
                if res.status_code == 200:
                    data = res.json()
                    if data.get("status") == "success":
                        return data.get("answer").replace("*", "").replace("#", "")
            except Exception:
                pass
                
            # Fallback to DDGS
            answer = DDGS().chat(prompt, model='gpt-4o-mini')
            return answer.replace("*", "").replace("#", "") if answer else "I could not analyze the screen content, Sir."
            
    except Exception as e:
        print(f"[VISION ERROR]: {e}")
        return "Sir, my screen vision modules encountered a hardware exception."