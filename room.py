import pygame
from door import Door

class Room:
    def __init__(self, background, game) -> None:
        self.game = game
        self.bg = pygame.image.load(background) # chargement de l'image de fond
        self.bg = pygame.transform.scale(self.bg, (1080, 720)) # on redimensionne l'image aux dimensions de l'écran

        # -----------| Gestion du contenu de la salle |----------- #

        self.alive_players = pygame.sprite.Group() # on crée un groupe contenant tous les joueurs (pas utilisé pour le moment)
        self.dead_players = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()

        self.objects = pygame.sprite.Group() # on crée un groupe contenant tous les objets (bombes)

        # Création des groupes de portes (explication dans le fichier door.py)
        self.all_doors1 = pygame.sprite.Group()
        self.all_doors2 = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()

    # Fonction de placement des portes

    def place_doors(self, config: int) -> None:
        # Fonctionnement expliqué dans la première boucle if, les 3 autres fonctionnent de la même manière

        if config == 1:

        # Salle 1:
            door1 = Door(self.game.room2) # On crée un objet Door
            door1.rect.x = 0 # On le positionne sur les axes x et y
            door1.rect.y = 310
            self.all_doors1.add(door1) # On l'ajoute au groupe des portes 1 de la salle
            
            door2 = Door(self.game.room4) # On crée un objet Door
            door2.rect.x = 490 # On le positionne sur les axes x et y 
            door2.rect.y = 0
            self.all_doors2.add(door2) # On l'ajoute au groupe des portes 2 de la salle

            self.doors.add(door1, door2) # On ajoute les 2 portes au groupe des portes de la salle
        
        elif config == 2:

        # Salle 2:
            door1 = Door(self.game.room3)
            door1.rect.x = 490
            door1.rect.y = 0
            self.all_doors1.add(door1)
            
            door2 = Door(self.game.room1)
            door2.rect.x = 980
            door2.rect.y = 310
            self.all_doors2.add(door2)
            self.doors.add(door1, door2)
        
        elif config == 3:

            # config salle 3
            door1 = Door(self.game.room4)
            door1.rect.x = 980
            door1.rect.y = 310
            self.all_doors1.add(door1)
            
            door2 = Door(self.game.room2)
            door2.rect.x = 490
            door2.rect.y = 620
            self.all_doors2.add(door2)
            self.doors.add(door1, door2)
        
        elif config == 4:

            # config salle 4
            door1 = Door(self.game.room1)
            door1.rect.x = 490
            door1.rect.y = 620
            self.all_doors1.add(door1)
            
            door2 = Door(self.game.room3)
            door2.rect.x = 0
            door2.rect.y = 310
            self.all_doors2.add(door2)
            self.doors.add(door1, door2)
