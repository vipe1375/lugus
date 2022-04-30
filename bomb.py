from sqlite3 import Time
from time import time
import pygame
import time as t
import animation

class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, coordinates : tuple, game):
        super().__init__()
        self.image = pygame.image.load("data/bomb.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.explosion = pygame.image.load("data/explosion.png")
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        self.game = game
        #self.game.bombs.append(1)

    

    def explode(self):
        self.game.bombs.pop()
        self.kill()
    