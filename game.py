import pygame
import asyncio
from players import Player
from sounds import SoundManager
from wall import Wall
from room import Room
from bomb import Bomb

class Game:
    def __init__(self):
        self.is_playing = False # attribut pour savoir si une partie est lancée

        # -----------| Gestion des salles |----------- #
        
        # On crée les salles depuis la classe Room
        self.room1 = Room("data/background.png", self)
        self.room2 = Room("data/room1.png", self)
        self.room3 = Room("data/room2.png", self)
        self.room4 = Room("data/room3.png", self)
        
        # On positionne les portes dans chaque salle
        self.room1.place_doors(1)
        self.room2.place_doors(2)
        self.room3.place_doors(3)
        self.room4.place_doors(4)

        # On crée un groupe qui rassemble tous les objets
        self.all_objects = pygame.sprite.Group()

        self.bombs = []
        
        self.pressed = {} # dictionnaire de gestion des touches

        self.sound_manager = SoundManager() # gestion des effets sonores

        self.all_rooms = pygame.sprite.Group() # groupe qui contient toutes les salles

        self.characters = ["red", "blue", "pink", "yellow", "black", "orange", "green", "cyan"]
        
        self.player = Player(self) # création du joueur
        
        self.player2 = Player(self)

        self.player3 = Player(self)
        self.player3.rect.x = 100
        self.player3.rect.y = 100
        
        self.dead_players = pygame.sprite.Group()

        
        
    # Fonction de mise à jour du jeu :

    def update(self, screen):
        
        screen.blit(self.player.actual_room.bg, (0, 0))
        self.player.actual_room.doors.draw(screen)
        self.player.actual_room.objects.draw(screen)
        if not self.player.is_alive:
            self.player.actual_room.dead_players.draw(screen)
        self.player.actual_room.alive_players.draw(screen)
        
        # Gestion des déplacements :
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < 1080: # vérification touches et position
            self.sound_manager.play_walk()
            if self.pressed.get(pygame.K_UP) and self.player.rect.y > 0:
                self.player.diag_up_right()
            elif self.pressed.get(pygame.K_DOWN) and self.player.rect.y + self.player.rect.height < 720:
                self.player.diag_down_right()
            else:
                self.player.move_right()
                
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:# vérification touches et position
            self.sound_manager.play_walk()
            if self.pressed.get(pygame.K_UP) and self.player.rect.y > 0:
                self.player.diag_up_left()
            elif self.pressed.get(pygame.K_DOWN) and self.player.rect.y + self.player.rect.height < 720:
                self.player.diag_down_left()
            else:
                self.player.move_left()
                
        elif self.pressed.get(pygame.K_UP) and self.player.rect.y > 0: # vérification touches et position
            self.sound_manager.play_walk()
            self.player.move_up()

        elif self.pressed.get(pygame.K_DOWN)and self.player.rect.y + self.player.rect.height < 720: # vérificaton touches et position
            self.sound_manager.play_walk()
            self.player.move_down()

        elif self.pressed.get(pygame.K_SPACE):
            self.player.drop_bomb()

        # Joueur 2 test

        if self.pressed.get(pygame.K_d) and self.player.rect.x + self.player.rect.width < 1080: # vérification touches et position
            self.sound_manager.play_walk()
            if self.pressed.get(pygame.K_z) and self.player.rect.y > 0:
                self.player2.diag_up_right()
            elif self.pressed.get(pygame.K_s) and self.player.rect.y + self.player.rect.height < 720:
                self.player2.diag_down_right()
            else:
                self.player2.move_right()
                
        elif self.pressed.get(pygame.K_q) and self.player.rect.x > 0:# vérification touches et position
            self.sound_manager.play_walk()
            if self.pressed.get(pygame.K_z) and self.player.rect.y > 0:
                self.player2.diag_up_left()
            elif self.pressed.get(pygame.K_s) and self.player.rect.y + self.player.rect.height < 720:
                self.player2.diag_down_left()
            else:
                self.player2.move_left()
                
        elif self.pressed.get(pygame.K_z) and self.player.rect.y > 0: # vérification touches et position
            self.sound_manager.play_walk()
            self.player2.move_up()

        elif self.pressed.get(pygame.K_s)and self.player.rect.y + self.player.rect.height < 720: # vérificaton touches et position
            self.sound_manager.play_walk()
            self.player2.move_down()
            
        elif self.pressed.get(pygame.K_k):
            
            self.player.kill()

        elif self.pressed.get(pygame.K_g):
            
            self.player.ressuscite()
        
            
    
        
            
        
        
    def check_collision(self, sprite, group) -> bool:
        """
        Cette fonction permet de vérifier si l'objet sprite passé en paramètre entre en collision avec 
        un des éléments du groupe de sprite en paramètre.
        """
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
        # le "False" indique que pygame ne doit pas supprimer le sprite en cas de collision
        # le "pygame.sprite.collide_mask" désigne l'interaction entre les deux objets
    
    def check_bomb(self, sprite, group) -> bool:
        """
        Cette fonction permet de vérifier si l'objet sprite passé en paramètre entre en collision avec
        un des éléments du groupe de sprite en paramètre
        """
        pass
    

    
        
       