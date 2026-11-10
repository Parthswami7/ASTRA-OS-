import pygame
import os

def play_welcome():
    """Plays the iconic startup sound when Parth Sir is recognized."""
    if os.path.exists("welcome.mp3"):
        pygame.mixer.init()
        pygame.mixer.music.load("welcome.mp3")
        pygame.mixer.music.play()
        # Let it play for a few seconds
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(19)
    else:
        print("[ASTRA]: Sound file 'welcome.mp3' not found in directory.")

if __name__ == "__main__":
    play_welcome()