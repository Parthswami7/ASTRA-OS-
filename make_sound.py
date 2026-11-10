from gtts import gTTS
import os

print("Forging Stark Industries boot audio...")
# You can change this text to whatever you want him to say on boot!
tts = gTTS(text="Initializing Ambika bag solution Uplink. Optics online. Standing by.", lang='en')

# Saves it directly into your UI folder
audio_path = os.path.join("ui", "boot.mp3")
tts.save(audio_path)
print(f"Success! Saved to {audio_path}")