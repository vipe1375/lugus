import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {"music": pygame.mixer.Sound("data/music2.mp3"),
        "walk": pygame.mixer.Sound("data/walk.mp3")}
        
    def play_music(self):
        self.sounds["music"].play(loops = 50) # lecture de la musique

    def play_walk(self):
        self.sounds["walk"].play()
