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
        self.image_name = random.choice(self.game.characters) # on choisit une couleur de personnage au hasard
        self.game.characters.remove(self.image_name) # on supprime cette couleur de la liste des couleurs disponibles

        self.image = pygame.image.load(f"data/characters/{self.image_name}_left.png") # on charge cette image
        self.image = pygame.transform.scale(self.image, (80, 80)) # on redimensionne l'image (80 pixels sur 80)

        self.image_base = pygame.image.load(f"data/characters/{self.image_name}_left.png") # on stocke l'image une seconde fois pour la garder si le joueur est ressuscité
        self.image_base = pygame.transform.scale(self.image, (80, 80))

        
        # image de gauche
        self.image_left = self.image # on crée une image où le personnage regarde à gauche(image par défaut)

        # image de droite
        self.image_right = pygame.transform.flip(self.image, True, False) # on effectue une rotation de l'image de gauche pour obtenir l'image de droite

        self.rect = self.image.get_rect() #'hitbox' du joueur 
        self.vitesse = 1 # vitesse de déplacement

        # position de départ du joueur:
        self.rect.x = 500 
        self.rect.y = 300
        
        # salles:
        self.actual_room = self.game.room1 # salle actuelle du joueur
        self.actual_room.alive_players.add(self) # on ajoute le joueur au groupe des joueurs vivants de la salle
        self.actual_room.all_players.add(self) # on ajoute le joueur au groupe de tous les joueurs de la salle
 
        self.is_alive = True  # attribut permettant de savoir si le joueur est en vie

        self.is_on_cooldown = False # attribut permettant de savoir si le joueur peut tuer ou s'il doit attendre

        self.is_on_cooldown_res = False # attribut permettant de savoir si le joueur peut ressusciter ou s'il doit attendre

        self.game.players.add(self) # on ajoute le joueur au groupe des joueurs
    
        
    # Méthode de changement de salle
    def change_room(self, old_room, new_room):

        if self.is_alive: # on vérifie si le joueur est vivant

            self.actual_room = new_room # on modifie la salle actuelle 

            self.actual_room.alive_players.add(self) # on ajoute le joueur aux deux groupes de la nouvelle salle et on le retire des groupes de l'ancienne salle
            self.actual_room.all_players.add(self)
            old_room.alive_players.remove(self)
            old_room.all_players.remove(self)

            # Gestion des coordonnées d'apparition (pour que ça concorde avec la position des portes dans la nouvelle salle)
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



                    # ------------ MOUVEMENTS DU JOUEUR ------------#

# Le fonctionnement des méthodes de mouvement n'est détaillé que dans le mouvement vers la droite, il est identique pour les autres
        
    # droite:
    def move_right(self):

        self.rect.x += self.vitesse # on modifie les coordonnées 
        self.image = self.image_right # on met l'image de droite

        if self.game.check_collision(self, self.actual_room.all_doors1): # on vérifie une éventuelle collision avec une porte de la salle

            # on choisit la salle dans laquelle envoyer le joueur
            if self.actual_room == self.game.room1:
                self.change_room(self.actual_room, self.game.room2)
            elif self.actual_room == self.game.room2:
                self.change_room(self.actual_room, self.game.room3)
            elif self.actual_room == self.game.room3:
                self.change_room(self.actual_room, self.game.room4)
            elif self.actual_room == self.game.room4:
                self.change_room(self.actual_room, self.game.room1)
                
        elif self.game.check_collision(self, self.actual_room.all_doors2): # on vérifie une éventuelle collision avec une porte de la salle
            
            # on choisit la salle dans laquelle envoyer le joueur
            if self.actual_room == self.game.room1:
                self.change_room(self.actual_room, self.game.room4)
            elif self.actual_room == self.game.room2:
                self.change_room(self.actual_room, self.game.room1)
            elif self.actual_room == self.game.room3:
                self.change_room(self.actual_room, self.game.room2)
            elif self.actual_room == self.game.room4:
                self.change_room(self.actual_room, self.game.room3)
        
        elif self.game.check_collision(self, self.actual_room.objects): # on vérifie une éventuelle collision avec une bombe

            if self.is_alive: # on vérifie si le joueur est vivant
                for obj in self.actual_room.objects:
                    obj.explode() # on récupère l'objet Bomb et on lui applique la méthode explode()
                    self.game.bomber.bomb = [] # on vide la liste des bombes du bombardier
                self.die() # on fait mourir le joueur
            
    # gauche
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
                ("vivant")
                for obj in self.actual_room.objects:
                    obj.explode()
                    self.bomb = []
                ("boom")
                self.die()
                
    # haut:
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
                ("vivant")
                for obj in self.actual_room.objects:
                    obj.explode()
                    self.bomb = []
                ("boom")
                self.die()

    
    # bas:    
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
                ("vivant")
                for obj in self.actual_room.objects:
                    obj.explode()
                    self.bomb = []
                ("boom")
                self.die()
        

# Pour les mouvements en diagonale, on n'appelle qu'une seule des précédentes méthodes de mouvement, afin d'éviter de vérifier les collisions 2 fois.
# Dans le cas du mouvement vers le bas à droite, on aurait pu appeler la méthode move_right() puis la méthode move_down() mais on aurait donc vérifié
# 2 fois si le joueur est en collision avec quelque chose.


    def diag_down_right(self):
        self.rect.y += self.vitesse # on modifie l'ordonnée
        self.move_right() # on se déplace vers la droite -> on obtient donc un mouvement en diagonale
        
    def diag_up_right(self):
        self.rect.y -= self.vitesse
        self.move_right()
        
    def diag_down_left(self):
        self.rect.y += self.vitesse
        self.move_left()

    def diag_up_left(self):
        self.rect.y -= self.vitesse
        self.move_left()

            
    # Méthode pour gérer la mort d'un joueur

    def die(self):

        self.game.dead_players.add(self) # on ajoute le joueur au groupe des joueurs morts de la partie
        self.actual_room.dead_players.add(self) # on ajoute le joueur au groupe des joueurs morts de la salle
        self.actual_room.alive_players.remove(self) # on retire le joueur du groupe des joueurs vivants de la salle

        self.is_alive = False # on modifie la valeur de l'attribut is_alive pour que le joueur ne soit plus considéré comme vivant

        self.image = pygame.image.load(f"data/characters/ghost.png") # on modifie l'image pour avoir un fantôme
        self.image = pygame.transform.scale(self.image, (80, 80)) # on modifie la taille de l'image
        self.image_right = self.image # l'image fantôme est orientée vers la droite, donc on fixe l'image de droite à l'image par défaut
        self.image_left = pygame.transform.flip(self.image, True, False) # on inverse l'image de droite pour avoir l'image de gauche
        
    
    # Méthode timer pour la gestion des cooldowns (asynchrone):

    async def timer(self, time):
        self.is_on_cooldown = True
        ("cooldown ajouté")
        await asyncio.sleep(time)
        self.is_on_cooldown = False
        ("cooldown retiré")


    # Méthode pour faire revivre le joueur
    def live(self):
        self.is_alive = True # on remet l'attribut à vivant

        self.actual_room.dead_players.remove(self) # on enlève le joueur du groupe des joueurs morts de la salle
        self.actual_room.alive_players.add(self) # on ajoute le joueur au groupe des joueurs vivants de la salle
        self.game.dead_players.remove(self) # on enlève le joueur du groupe des joueurs morts de la partie
        self.image = self.image_base # on remet l'image à celle de base







