import cv2
import os
import numpy as np
import time
import urllib.request

# Setup memory directories for your face model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "facial_data")
MODEL_PATH = os.path.join(DATA_DIR, "astra_face_model.yml")
HAAR_PATH = os.path.join(DATA_DIR, "haarcascade_frontalface_default.xml")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Auto-download the missing OpenCV visual map if it doesn't exist locally
if not os.path.exists(HAAR_PATH):
    print("[PROJECT GLASS] Downloading missing facial recognition cascade from master servers...")
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, HAAR_PATH)

# Load the frontal face detector from our safe local copy
face_cascade = cv2.CascadeClassifier(HAAR_PATH)

def enroll_master_face():
    print("[PROJECT GLASS] Initializing Vivobook Webcam for Master Enrollment...")
    cam = cv2.VideoCapture(0)
    
    count = 0
    faces_data = []
    labels = []
    
    print("[PROJECT GLASS] Look directly at the camera. Capturing 100 facial nodes...")
    time.sleep(2)
    
    while True:
        ret, frame = cam.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))
            faces_data.append(face_img)
            labels.append(1) # ID 1 is exclusively Parth Sir
            
            # Draw targeting HUD
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
            cv2.putText(frame, f"Scanning: {count}%", (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 0), 1)
            
        cv2.imshow('A.S.T.R.A - Neural Face Mapping', frame)
        
        # Stop after 100 successful frames
        if cv2.waitKey(1) & 0xFF == 27 or count >= 100:
            break
            
    cam.release()
    cv2.destroyAllWindows()
    
    if count > 0:
        print("[PROJECT GLASS] Compiling neural face model...")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces_data, np.array(labels))
        recognizer.save(MODEL_PATH)
        print("[PROJECT GLASS] Master Face Model Saved! You are now locked in, Sir.")
    else:
        print("[PROJECT GLASS] Error: No face detected. Please ensure the room is well lit.")

def verify_master():
    if not os.path.exists(MODEL_PATH):
        print("[PROJECT GLASS] No face model found! Bypassing to standard boot.")
        return True
        
    print("[PROJECT GLASS] Activating retinal scan...")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)
    
    cam = cv2.VideoCapture(0)
    authorized = False
    scan_attempts = 0
    
    # Give the system roughly 5-10 seconds to recognize you
    while scan_attempts < 150: 
        ret, frame = cam.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            face_img = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            id_, confidence = recognizer.predict(face_img)
            
            # Draw scanning HUD
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            
            # LBPH Confidence is distance to perfect match. Lower is better. < 65 is very strict.
            if confidence < 45: 
                authorized = True
                cv2.putText(frame, "ACCESS GRANTED", (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)
                break
            else:
                cv2.putText(frame, "ANALYZING...", (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
        
        cv2.imshow('A.S.T.R.A - Authorization Protocol', frame)
        scan_attempts += 1
        
        # Pause briefly to let the user see the "ACCESS GRANTED" text before closing
        if authorized:
            cv2.waitKey(1000)
            break
        if cv2.waitKey(1) & 0xFF == 27: # Press ESC to manual override
            break
            
    cam.release()
    cv2.destroyAllWindows()
    
    return authorized

if __name__ == "__main__":
    # When you run this file directly, it triggers the Learning Mode
    enroll_master_face()