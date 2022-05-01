import pygame
from game import Game # importation de la classe de gestion de partie
pygame.init() # initialisation de la librairie

game = Game() # création d'une partie

# Fond :
background = pygame.image.load("data/background.png") # image
background = pygame.transform.scale(background, (1080, 720)) # taille

# Bannière :

banner = pygame.image.load("data/logo4.png")

# Bouton start :

button = pygame.image.load("data/start.png") # image
button = pygame.transform.scale(button, (206, 206)) # taille
button_rect = button.get_rect()
button_rect.x = 435
button_rect.y = 300

# Variable pour savoir si le programme est actif

running = True
    
# Fenêtre du jeu :
 
pygame.display.set_caption("Lugus") # nom 
screen = pygame.display.set_mode((1080, 720)) # variable qui représente l'écran

# Musique :

#game.sound_manager.play_music() # lancement de la musique




# Boucle du jeu :

while running:
    screen.blit(background, (0,0)) # on affiche le fond

    if game.is_playing:
        if game.check_end():
            screen.blit(banner, (0, 0))
        else:
            game.update(screen) # mettre à jour les éléments
       
    else:
        screen.blit(banner, (415, 100)) # affichage de la bannière
        screen.blit(button, button_rect) # affichage du bouton start

    pygame.display.flip() # on met à jour l'écran
        
    

    # Gestion des évènements :

    for event in pygame.event.get():

        # si le joueur veut quitter le jeu
        if event.type == pygame.QUIT:
            running = False
            pygame.quit() #on ferme la fenêtre
            
        # touche appuyée
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True # on ajoute la touche dans le dictionnaire à True
            
        # touche lâchée
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False # on met à False la touche dans le dictionnaire
        
        #clic de souris
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # si la souris est en collision avec le bouton jouer
            if button_rect.collidepoint(event.pos):
                game.is_playing = True
    
        

        
# Fonction de choix du perso
def startup():
    pass
