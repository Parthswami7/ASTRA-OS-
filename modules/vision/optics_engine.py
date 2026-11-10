import cv2
import face_recognition
import os
import time
import requests
import sys
import threading

# 1. Establish the Master Folder Path FIRST
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(PROJECT_ROOT)

# 2. NOW we can safely import from the modules folder
from modules.voice.play_sound import play_welcome

FACE_IMAGE_PATH = os.path.join(PROJECT_ROOT, "memory", "faces", "Parth_Sir.jpg")

try:
    parth_image = face_recognition.load_image_file(FACE_IMAGE_PATH)
    parth_encoding = face_recognition.face_encodings(parth_image)[0]
    print("[OPTICS] Master Biometric Profile Loaded.")
except Exception as e:
    print(f"[ERROR] Could not load face at: {FACE_IMAGE_PATH}")
    sys.exit(1)

def notify_phone(message, title="ASTRA SENTRY", tags="rotating_light,warning", priority="5"):
    # This matches your exact ntfy topic
    topic = "parths_vivobook_sentry_99" 
    url = f"https://ntfy.sh/{topic}"
    headers = {"Title": title, "Priority": priority, "Tags": tags}
    try:
        requests.post(url, data=message.encode('utf-8'), headers=headers)
    except Exception:
        pass

def trigger_physical_lock():
    import ctypes
    print("\n[ALERT]: STRANGER DETECTED! Locking Windows...")
    notify_phone("Unrecognized face detected. Locking the system immediately.", title="SECURITY BREACH")
    ctypes.windll.user32.LockWorkStation()

def run_optics():
    print("[OPTICS] Unified Camera Engine Online...")
    cap = cv2.VideoCapture(0)
    
    # Warm up the camera hardware for 1 second to prevent a black frame
    time.sleep(1)
    for _ in range(5):
        cap.read()
        
    intruder_timer = 0 

    while True:
        success, img = cap.read()
        if not success: break
            
        img = cv2.flip(img, 1) 
        
        # --- SENTRY SCANNER ---
        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)
        
        if len(face_encodings) > 0:
            match_found = False
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([parth_encoding], face_encoding, tolerance=0.55)
                if True in matches:
                    match_found = True
                    break
            
            if match_found:
                print("[OPTICS] Face Matched - Access Granted!")
                
                # I fixed the threading target here so your audio actually plays!
                threading.Thread(target=play_welcome, daemon=True).start()
                time.sleep(0.5)
                
                # THIS kills the camera and boots the rest of ASTRA
                cap.release()
                cv2.destroyAllWindows()
                sys.exit(0) 
                
            else:
                intruder_timer += 1
                print(f"[OPTICS] Unknown Face Detected! Checking... ({intruder_timer}/7)")
                
                if intruder_timer >= 7:
                    trigger_physical_lock()
                    
                    # THIS kills the camera and aborts the boot process
                    cap.release()
                    cv2.destroyAllWindows()
                    sys.exit(1) 
                    
        cv2.imshow("ASTRA OPTICS - SECURITY GATE", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    sys.exit(1)

if __name__ == "__main__":
    run_optics()