from flask import Flask, jsonify, request
import psutil
import os
import time
import requests
import wikipedia
import ctypes
import subprocess
import urllib.parse
from gtts import gTTS
from ddgs import DDGS 
import sys
import logging
import werkzeug.serving

# --- STRICT TERMINAL SILENCER ---
werkzeug.serving.WSGIRequestHandler.log_request = lambda *args, **kwargs: None
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True
# --------------------------------

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from plugins.ollama_engine import llm_brain
    from plugins.system_agent import system_agent
    PLUGINS_ACTIVE = True
except ImportError as e:
    print(f"[WARNING] Mark II Plugins failed to load: {e}. Running in Mark I Legacy Mode.")
    PLUGINS_ACTIVE = False

app = Flask(__name__, static_url_path='', static_folder='.')
psutil.cpu_percent(interval=None)

GLOBAL_SECURITY_STATE = "SCANNING"
speech_status = False

@app.route('/ask/<query>')
def ask_question(query):
    query = query.lower().strip()
    if "how are you" in query: 
        return jsonify({"status": "success", "answer": "I am operating at optimal capacity, sir."})
    
    if PLUGINS_ACTIVE:
        local_answer = llm_brain.process_query(query)
        return jsonify({"status": "success", "answer": local_answer})
    else:
        try:
            search_term = query.replace("astra", "").replace("who is", "").strip()
            with DDGS() as ddgs:
                results = list(ddgs.text(search_term, max_results=1))
                if results: return jsonify({"status": "success", "answer": results[0]['body']})
                else: raise Exception()
        except:
            try: return jsonify({"status": "success", "answer": wikipedia.summary(search_term, sentences=2)})
            except: return jsonify({"status": "error", "answer": "I am unable to find information on that topic, sir."})

@app.route('/')
def home(): return app.send_static_file('index.html')

@app.route('/status')
def status(): return jsonify({"status": "ONLINE", "cpu": round(psutil.cpu_percent(interval=None)), "ram": round(psutil.virtual_memory().percent)})

@app.route('/weather')
def weather():
    try: return jsonify({"temp": round(requests.get("https://api.open-meteo.com/v1/forecast?latitude=27.6094&longitude=75.1398&current_weather=true", timeout=3).json()['current_weather']['temperature']), "status": "success"})
    except: return jsonify({"temp": "--", "status": "error"})

@app.route('/set_security_status/<status>')
def set_security_status(status):
    global GLOBAL_SECURITY_STATE
    GLOBAL_SECURITY_STATE = status.upper()
    return jsonify({"status": "updated"})

@app.route('/security_status')
def get_security_status():
    global GLOBAL_SECURITY_STATE
    return jsonify({"status": GLOBAL_SECURITY_STATE})
    
@app.route('/reset_security')
def reset_security():
    global GLOBAL_SECURITY_STATE
    GLOBAL_SECURITY_STATE = "SCANNING"
    return jsonify({"status": "reset"})

@app.route('/set_speech_status', methods=['POST'])
def set_speech_status():
    global speech_status
    data = request.json
    if data:
        speech_status = data.get('is_speaking', False)
    return jsonify({"success": True})

@app.route('/get_speech_status', methods=['GET'])
def get_speech_status():
    return jsonify({"is_speaking": speech_status})

@app.route('/lockdown')
def lockdown():
    try: ctypes.windll.user32.LockWorkStation()
    except: pass
    return jsonify({"status": "locked"})

@app.route('/shutdown')
def shutdown_pc():
    os.system("shutdown /s /t 5")
    return jsonify({"status": "shutting down"})

@app.route('/execute/<path:target>')
def execute_any(target):
    target = urllib.parse.unquote(target).lower().strip()
    
    websites = {
        "youtube": "youtube.com", "google": "google.com", "github": "github.com",
        "chatgpt": "chatgpt.com", "netflix": "netflix.com", "instagram": "instagram.com",
        "facebook": "facebook.com", "whatsapp": "web.whatsapp.com", "amazon": "amazon.in",
        "flipkart": "flipkart.com", "wikipedia": "wikipedia.org", "canva": "canva.com",
        "spotify": "spotify.com", "twitter": "x.com"
    }

    if "coding project" in target or "astra code" in target:
        os.system(r'start code "C:\Users\ASUS\Desktop\JARVIS_OS"')
    elif "chicku" in target or "my youtube channel" in target:
        os.system("start chrome https://www.youtube.com/@ChickuTV")
    elif "beamng" in target:
        os.system("start steam://rungameid/284160")
    elif target in websites:
        os.system(f"start https://www.{websites[target]}")
    else:
        if "." in target and " " not in target:
            os.system(f"start https://{target}")
        else:
            os.system(f'start "" "{target}"')
    return jsonify({"status": "executed", "target": target})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)