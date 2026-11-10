import face_recognition
import pickle
import os

def train_ASTRA():
    encoded_faces = {}
    user_dir = "authorized_users"
    
    print("[ASTRA]: Scanning authorized personnel...")
    
    for file in os.listdir(user_dir):
        if file.endswith((".jpg", ".png", ".jpeg")):
            name = os.path.splitext(file)[0]
            # Load the image and learn how to recognize it
            image = face_recognition.load_image_file(f"{user_dir}/{file}")
            encoding = face_recognition.face_encodings(image)[0]
            encoded_faces[name] = encoding
            print(f"[ASTRA]: {name} added to whitelist.")

    # Save the 'brain' data to a file
    with open("whitelist.pickle", "wb") as f:
        pickle.dump(encoded_faces, f)
    print("[ASTRA]: Training complete. Security database updated.")

if __name__ == "__main__":
    train_ASTRA()