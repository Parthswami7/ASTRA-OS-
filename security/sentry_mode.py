import cv2
import face_recognition
import time
import requests
import ctypes

def notify_phone(message, title="SENTRY ALERT", tags="rotating_light,warning", priority="5"):
    topic = "parths-ASTRA-sentry-alerts-773" 
    url = f"https://ntfy.sh/{topic}"
    headers = {"Title": title, "Priority": priority, "Tags": tags}
    try:
        requests.post(url, data=message.encode('utf-8'), headers=headers)
    except Exception as e:
        print(f"Notification Error: {e}")

def lock_workstation():
    # Windows command to lock the laptop instantly
    ctypes.windll.user32.LockWorkStation()

def run_sentry():
    print("Sentry Mode Activated. Monitoring camera...")
    notify_phone("Camera monitoring initiated.", title="Sentry Mode Active", tags="eye", priority="3")
    
    video_capture = cv2.VideoCapture(0)
    
    # Add your known face encodings here like we set up previously
    known_face_encodings = [] 
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
            
        # Process every 4th frame to save CPU processing power
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        stranger_detected = False
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            
            # If no matches found (or list is empty), flag as a stranger
            if not any(matches) or len(known_face_encodings) == 0:
                stranger_detected = True
                break
                
        if stranger_detected:
            print("Stranger detected! Locking system and sending alert.")
            notify_phone(
                "Unrecognized face detected at your laptop. System locked.",
                title="SECURITY BREACH",
                tags="cop,warning,rotating_light",
                priority="5" # Max priority to break through Do Not Disturb
            )
            lock_workstation()
            
            # Pause detection for 60 seconds after locking so it doesn't spam your phone
            time.sleep(60)
            
        # Press 'q' to quit manually in the console
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_sentry()