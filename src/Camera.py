# TODO: Implement camera follow and movement
import pygame
from pygame.math import Vector2

class Camera:
    def __init__(self, init_pos : Vector2):
        self.init_pos = init_pos.copy()
        self.pos = init_pos.copy()
        self.sprite_list = []
        self.follow_sprite = None
        self.follow_speed = 0.05
        self.bidirect_update = False

    def setCameraPosition(self, pos : Vector2):
        # Set the position of the camera
        self.pos = pos

    def addSprite(self, sprite : pygame.sprite.Sprite):
        # Add a sprite to the camera
        self.sprite_list.append(sprite)

    def follow(self, sprite : pygame.sprite.Sprite):
        # Specify which sprite should be followed by the camera
        self.follow_sprite = sprite

    def setBidirectUpdate(self, flag : bool):
        self.bidirect_update = flag

    def updatePosition(self):
        # Update the position of the camera and also the related sprites
        if self.follow_sprite:
            if self.bidirect_update:
                # Move the camera as well as the sprites 
                heading = self.follow_sprite.getPos() - self.pos
                self.pos += self.follow_speed * heading
                offset = self.init_pos - self.pos # To make the following sprite to return to the initial postion
            else:
                # Move only the camera
                heading = self.pos - self.follow_sprite.getPos()
                offset = self.follow_speed * heading # To make the following sprite to return to the initial postion
            for sprite in self.sprite_list:
                sprite.applyOffset(offset)


    
