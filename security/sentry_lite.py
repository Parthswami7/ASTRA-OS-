import face_recognition
import cv2
import ctypes
import time
import os
import pygame
import pickle # Added for instant memory loading

def setup_master_face():
    """Takes ONE photo and pre-calculates the deep-learning math to save time."""
    print("\n[ASTRA]: Master face not found. Setting up...")
    
    # CAP_DSHOW forces Windows to open the camera instantly
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    time.sleep(1) # Shortened warmup
    
    print("[ASTRA]: Saving Master Face in 2 seconds...")
    time.sleep(2)
    
    ret, frame = cam.read()
    if ret:
        cv2.imwrite("parth_sir.jpg", frame)
        print("[ASTRA]: Photo saved. Calculating neural encoding (this takes a moment)...")
        
        # Pre-calculate the heavy math ONCE and save it as a tiny file
        parth_image = face_recognition.load_image_file("parth_sir.jpg")
        try:
            parth_encoding = face_recognition.face_encodings(parth_image)[0]
            with open("parth_encoding.pickle", "wb") as f:
                pickle.dump(parth_encoding, f)
            print("[ASTRA]: Neural memory saved successfully!")
        except IndexError:
            print("[ERROR]: Could not see a face clearly. Delete parth_sir.jpg and try again.")
    else:
        print("[ERROR]: Could not read from camera.")
        
    cam.release()
    cv2.destroyAllWindows()

def guard_laptop():
    """Hyper-fast True/False verification aiming for 1.5 second reaction time."""
    
    # 1. Setup if first time
    if not os.path.exists("parth_encoding.pickle"):
        setup_master_face()
        return # Exit after setup so you can start a fresh, fast run

    print("\n[ASTRA]: Loading pre-calculated memory...")
    
    # SPEED HACK 1: Load the pre-calculated math instantly (Takes 0.01 seconds)
    with open("parth_encoding.pickle", "rb") as f:
        parth_encoding = pickle.load(f)

    # SPEED HACK 2: Pre-load the audio engine so it fires instantly when it sees you
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("welcome.mp3")
    except Exception:
        pass # Fails silently if the audio file is missing

    # SPEED HACK 3: CAP_DSHOW opens the camera instantly instead of waiting for Windows
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print("[ASTRA]: Sentry ONLINE.")

    while True:
        ret, frame = cam.read()
        if not ret:
            continue

        # SPEED HACK 4: Shrink frame to 20% size. This allows the i3 to process it instantly.
        small_frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Extremely fast location and encoding
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        stranger_detected = False
        parth_detected = False

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([parth_encoding], face_encoding, tolerance=0.5)

            if True in matches:
                parth_detected = True
            else:
                stranger_detected = True

        # --- THE DECISION ENGINE ---
        if parth_detected:
            print("\n[SECURITY]: Parth Sir identified. Unlocking system.")
            
            # Fire the pre-loaded audio instantly
            if pygame.mixer.music.get_busy() == False:
                 pygame.mixer.music.play()
            
            # Keep script alive just long enough to play the audio
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            break 

        elif stranger_detected:
            print("\n[ALERT]: STRANGER DETECTED! Locking laptop...")
            ctypes.windll.user32.LockWorkStation()
            time.sleep(5) 
            
        else:
            # If no face is seen, check again immediately
            pass

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    guard_laptop()