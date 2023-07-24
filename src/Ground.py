import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self, image, width, height, top):
        # TODO: make sure that the width of the grund is the same as the screen width
        # and height equals to 50 by default
        # and the bottom is at the bottom of the screen
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.top = top