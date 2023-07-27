import pygame
from pygame.math import Vector2
from .AssetsLoader import AssetsLoader

class Ground(pygame.sprite.Sprite):
    def __init__(self, width, height, top):
        pygame.sprite.Sprite.__init__(self)
        self.image = AssetsLoader.getImage("ground")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.top = top

    def applyOffset(self, offset : Vector2):
        # Change the position of the current sprite by applying an
        # offset of a specified Vector2
        self.rect.centerx += offset.x
        self.rect.centery += offset.y