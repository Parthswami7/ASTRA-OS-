import os
import subprocess

def play_music(song_query):
    music_dir = r"E:\Music"
    
    if not os.path.exists(music_dir):
        return "Music directory E colon slash Music does not exist, Sir."
        
    try:
        # Get all audio files in the folder
        files = os.listdir(music_dir)
        audio_files = [f for f in files if f.lower().endswith(('.mp3', '.wav', '.flac', '.m4a'))]
        
        if not audio_files:
            return "No audio files found in your music directory, Sir."
            
        # If a specific song was requested, search for a match
        if song_query:
            query_lower = song_query.lower()
            matched_file = None
            
            for file in audio_files:
                if query_lower in file.lower():
                    matched_file = file
                    break
                    
            if matched_file:
                target_path = os.path.join(music_dir, matched_file)
                print(f"[ASTRA-SYS] Launching music file: {target_path}")
                # Opens the file with the default Windows media association
                os.startfile(target_path)
                return f"Playing {os.path.splitext(matched_file)[0]}, Sir."
            else:
                return f"I could not find a track matching {song_query} in your music folder, Sir."
        else:
            # If no name was specified, just open the folder
            os.startfile(music_dir)
            return "Opening your music folder, Sir."
            
    except Exception as e:
        print(f"[ASTRA-SYS Error]: {e}")
        return "An error occurred while accessing the media storage, Sir."