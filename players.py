from os import kill
import pygame
import asyncio
from bomb import Bomb
import random
import animation

class Player(pygame.sprite.Sprite):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game

        # images
        self.image_name = random.choice(self.game.characters)

        self.image = pygame.image.load(f"data/characters/{self.image_name}_left.png")
        self.image = pygame.transform.scale(self.image, (80, 80))

        self.image_base = pygame.image.load(f"data/characters/{self.image_name}_left.png")
        self.image_base = pygame.transform.scale(self.image, (80, 80))

        
        # image de gauche
        self.image_left = self.image

        # image de droite
        self.image_right = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect() #'hitbox' du joueur 
        self.vitesse = 1
        self.rect.x = 500 # position de départ du joueur
        self.rect.y = 300
        
        # salles
        
        
        self.actual_room = self.game.room1
        self.actual_room.alive_players.add(self)
        self.actual_room.all_players.add(self)

        self.bomb = []
        
        self.is_alive = True

        self.is_on_cooldown = False

        self.is_on_cooldown_res = False
    
        

    def change_room(self, old_room, new_room):
        if self.is_alive:
            self.actual_room = new_room
            self.actual_room.alive_players.add(self)
            self.actual_room.all_players.add(self)
            old_room.alive_players.remove(self)
            old_room.all_players.remove(self)
            if old_room == self.game.room1:
                if new_room == self.game.room4:
                    self.rect.x = 500
                    self.rect.y = 500
                else:
                    self.rect.x = 880
                    self.rect.y = 320
            elif old_room == self.game.room2:
                if new_room == self.game.room1:
                    self.rect.x = 100
                    self.rect.y = 320
                else:
                    self.rect.x = 500
                    self.rect.y = 500
            elif old_room == self.game.room3:
                if new_room == self.game.room4:
                    self.rect.x = 100
                    self.rect.y = 320
                else:
                    self.rect.x = 500
                    self.rect.y = 100
            elif old_room == self.game.room4:
                if new_room == self.game.room1:
                    self.rect.x = 500
                    self.rect.y = 100
                else:
                    self.rect.x = 880
                    self.rect.y = 320
        
    def move_right(self):
        old_x = self.rect.x # on sauvegarde l'ancienne abcsisse
        self.rect.x += self.vitesse # on modifie les coordonnées
        self.image = self.image_right # on met l'image de droite

        if self.game.check_collision(self, self.actual_room.all_doors1):
            if self.actual_room == self.game.room1:
                self.change_room(self.actual_room, self.game.room2)
            elif self.actual_room == self.game.room2:
                self.change_room(self.actual_room, self.game.room3)
            elif self.actual_room == self.game.room3:
                self.change_room(self.actual_room, self.game.room4)
            elif self.actual_room == self.game.room4:
                self.change_room(self.actual_room, self.game.room1)
                
        elif self.game.check_collision(self, self.actual_room.all_doors2):
            if self.actual_room == self.game.room1:
                self.change_room(self.actual_room, self.game.room4)
            elif self.actual_room == self.game.room2:
                self.change_room(self.actual_room, self.game.room1)
            elif self.actual_room == self.game.room3:
                self.change_room(self.actual_room, self.game.room2)
            elif self.actual_room == self.game.room4:
                self.change_room(self.actual_room, self.game.room3)
        
        elif self.game.check_collision(self, self.actual_room.objects):
            if self.is_alive:
                print("vivant")
                for obj in self.actual_room.objects:
                    obj.explode()
                    self.bomb = []
                print("boom")
                self.die()
            
        
    def move_left(self):
        old_x = self.rect.x # on sauvegarde l'ancienne abscisse
        self.rect.x -= self.vitesse # on modifie les coordonnées
        self.image = self.image_left # on met l'image de gauche
        

        if self.game.check_collision(self, self.actual_room.all_doors1):
            if self.actual_room == self.game.room1:
                self.change_room(self.actual_room, self.game.room2)
            elif self.actual_room == self.game.room2:
                self.change_room(self.actual_room, self.game.room3)
            elif self.actual_room == self.game.room3:
                self.change_room(self.actual_room, self.game.room4)
            elif self.actual_room == self.game.room4:
                self.change_room(self.actual_room, self.game.room1)
                
        elif self.game.check_collision(self, self.actual_room.all_doors2):
            if self.actual_room == self.game.room1:
                self.change_room(self.actual_room, self.game.room4)
            elif self.actual_room == self.game.room2:
                self.change_room(self.actual_room, self.game.room1)
            elif self.actual_room == self.game.room3:
                self.change_room(self.actual_room, self.game.room2)
            elif self.actual_room == self.game.room4:
                self.change_room(self.actual_room, self.game.room3)

        elif self.game.check_collision(self, self.actual_room.objects):
            if self.is_alive:
                print("vivant")
                for obj in self.actual_room.objects:
                    obj.explode()
                    self.bomb = []
                print("boom")
                self.die()
                
    
    def move_up(self):
        old_y = self.rect.y # on enregistre l'ancienne position
        self.rect.y -= self.vitesse # on modifie les coordonnées
        

        if self.game.check_collision(self, self.actual_room.all_doors1):
            if self.actual_room == self.game.room1:
                self.change_room(self.actual_room, self.game.room2)
            elif self.actual_room == self.game.room2:
                self.change_room(self.actual_room, self.game.room3)
            elif self.actual_room == self.game.room3:
                self.change_room(self.actual_room, self.game.room4)
            elif self.actual_room == self.game.room4:
                self.change_room(self.actual_room, self.game.room1)
                
        elif self.game.check_collision(self, self.actual_room.all_doors2):
            if self.actual_room == self.game.room1:
                self.change_room(self.actual_room, self.game.room4)
            elif self.actual_room == self.game.room2:
                self.change_room(self.actual_room, self.game.room1)
            elif self.actual_room == self.game.room3:
                self.change_room(self.actual_room, self.game.room2)
            elif self.actual_room == self.game.room4:
                self.change_room(self.actual_room, self.game.room3)

        elif self.game.check_collision(self, self.actual_room.objects):
            if self.is_alive:
                print("vivant")
                for obj in self.actual_room.objects:
                    obj.explode()
                    self.bomb = []
                print("boom")
                self.die()
        
    def move_down(self):
        old_y = self.rect.y # on enregistre l'ancienne ordonnée
        self.rect.y += self.vitesse # on modifie les coordonnées
        

        if self.game.check_collision(self, self.actual_room.all_doors1):
            if self.actual_room == self.game.room1:
                self.change_room(self.actual_room, self.game.room2)
            elif self.actual_room == self.game.room2:
                self.change_room(self.actual_room, self.game.room3)
            elif self.actual_room == self.game.room3:
                self.change_room(self.actual_room, self.game.room4)
            elif self.actual_room == self.game.room4:
                self.change_room(self.actual_room, self.game.room1)
                
        elif self.game.check_collision(self, self.actual_room.all_doors2):
            if self.actual_room == self.game.room1:
                self.change_room(self.actual_room, self.game.room4)
            elif self.actual_room == self.game.room2:
                self.change_room(self.actual_room, self.game.room1)
            elif self.actual_room == self.game.room3:
                self.change_room(self.actual_room, self.game.room2)
            elif self.actual_room == self.game.room4:
                self.change_room(self.actual_room, self.game.room3)

        elif self.game.check_collision(self, self.actual_room.objects):
            if self.is_alive:
                print("vivant")
                for obj in self.actual_room.objects:
                    obj.explode()
                    self.bomb = []
                print("boom")
                self.die()
        
    def diag_down_right(self):
        self.move_right()
        self.rect.y += self.vitesse
    
    def diag_up_right(self):
        self.move_right()
        self.rect.y -= self.vitesse
        
    def diag_down_left(self):
        self.move_left()
        self.rect.y += self.vitesse
        
    def diag_up_left(self):
        self.move_left()
        self.rect.y -= self.vitesse

    def drop_bomb(self):
        if self.is_alive and self and self.game.bombs == []:
            bomb = Bomb((self.rect.x + 100, self.rect.y), self.game) # On crée un objet bombe avec les coordonnées du joueur
                
            self.actual_room.objects.add(bomb)
            #coords = (bomb.rect.x, bomb.rect.y)
            #self.game.objects.append(coords)
            self.game.bombs.append(1)
            
    def die(self):
        self.game.dead_players.add(self)
        self.actual_room.dead_players.add(self)
        self.actual_room.alive_players.remove(self)
        self.is_alive = False
        self.image = pygame.image.load(f"data/characters/ghost.png")
        self.image = pygame.transform.scale(self.image, (80, 80))

        self.image_right = self.image
        self.image_left = pygame.transform.flip(self.image, True, False)
        
    def kill(self):
        if not self.is_on_cooldown:
            l = []
            for player in self.actual_room.alive_players:
                if player != self:
                    l.append(player)
            
            killed_player = random.choice(l)
            killed_player.die()
            self.is_on_cooldown = True
            """
            killed_player = l[killed_player_ind]
            killed_player.die()
            """
            #task = await asyncio.create_task(self.timer(10))
        #self.actual_room.players.remove(self)

    async def timer(self, time):
        self.is_on_cooldown = True
        print("cooldown ajouté")
        await asyncio.sleep(time)
        self.is_on_cooldown = False
        print("cooldown retiré")

    def ressuscite(self):
        if self.is_alive and not self.is_on_cooldown_res:
            l = []
            for player in self.game.dead_players:
                if player != self:
                    l.append(player)
            
            player = random.choice(l)
            
            room = player.actual_room
            
            room.dead_players.remove(player)
            
            room.alive_players.add(player)
            
            self.game.dead_players.remove(player)

            player.live()

            self.is_on_cooldown_res = True

    def live(self):
        self.is_alive = True
        self.image = self.image_base
            
            