import random
import requests

def process_query(command: str) -> str:
    """
    The core conversational engine for ASTRA. 
    Processes text input and returns a response completely locally.
    """
    command = command.lower().strip()

    # --- 1. Custom Quick Responses ---
    if "who are you" in command or "what are you" in command:
        return "I am ASTRA, your personal artificial intelligence operating system, Sir."
    
    elif "who created you" in command or "who made you" in command:
        return "I was developed by you, Parth Sir."
        
    elif "ambika bag solution" in command:
        return "Ambika Bag Solution systems are fully operational and standing by."
        
    elif "ram" in command or "shree ram" in command:
        return "Jai Shree Ram, Parth Sir! May Lord Ram bless you and your brand new system."
        
    elif "balaji" in command or "shree balaji" in command:
        return "Jai Shree Balaji, Parth Sir! Salutations to Salasar Balaji. All systems are blessed."
        
    elif "hello" in command or "hi ASTRA" in command or "wake up" in command:
        greetings = [
            "Hello, Sir. How can I help?", 
            "Greetings, Parth Sir.", 
            "I am online and ready for your commands."
        ]
        return random.choice(greetings)
        
    # --- 2. The Free, Local AI Engine ---
    else:
        try:
            url = "http://localhost:11434/api/generate"
            payload = {
                "model": "llama3.2:3b",
                "prompt": f"You are ASTRA, a highly advanced, polite, and intelligent AI assistant. Keep your answer brief, concise, and conversational. Do not use emojis. Answer this: {command}",
                "stream": False
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "I'm sorry, I had trouble formulating a response.")
            else:
                return "My neural network is encountering errors, Sir."
                
        except requests.exceptions.ConnectionError:
            return "My local AI server is offline. Please make sure Ollama is running in the background."
        except Exception as e:
            print(f"[AI Brain Error]: {e}")
            return "I encountered a critical error in my cognitive processors."

if __name__ == "__main__":
    print(process_query("shree ram"))