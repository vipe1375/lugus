import pygame

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name) -> None:
        super().__init__()
        self.image = pygame.image.load(f"data/{name}.png")
        self.current_image = 0
        self.images = animations.get(name)
        self.animation = False
        (self.images)

    def start_animation(self):
        self.animation = True
    
    def animate(self):
        if self.animation:
            self.current_image += 1 # passage à l'image suivante
            
            # si on a atteint la dernière image:
            if self.current_image >= len(self.images):
                self.current_image = 0 # retour à la première image
                self.animation = False
            
            self.image = self.images[self.current_image]
            

def load_animation_images(name):
    images = []
    path = f"data/{name}/{name}"
    for num in range(1, 2):
        image_path = path + str(num) + '.png'
        images.append(pygame.image.load(image_path))
    return images

animations = {
    "explosion": load_animation_images("explosion"),
    "door": load_animation_images("door")
}