import pygame
from .AssetsLoader import AssetsLoader

class Ground(pygame.sprite.Sprite):
    def __init__(self, width, height, top):
        pygame.sprite.Sprite.__init__(self)
        self.image = AssetsLoader.getImage("ground")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.top = top