import pygame

# Pour la gestion des collisions, la librairie pygame permet de gérer les collisions d'un objet avec un groupe d'objets, et pas
# avec un objet unique.
# Dans notre situation, le joueur peut entrer en collision avec 2 portes différentes dans chaque salle. On ne peut donc pas 
# savoir avec laquelle il est entré en collision. Nous créons donc 2 groupes de portes par salle, chaque groupe contenant une
# porte de la salle, et on vérifie les collisions entre le joueur et chacun de ces 2 groupes


class Door(pygame.sprite.Sprite):
    def __init__(self, room_to):
        super().__init__()

        # Image
        self.image = pygame.image.load("data/door.png") # Chargement de l'image
        self.image = pygame.transform.scale(self.image, (100, 100)) # Redimensionnement
        self.rect = self.image.get_rect() # 'hitbox' de l'image

        self.room_to = room_to # désigne la salle vers laquelle mène la porte