import pygame
import math
import random
from .AssetsLoader import AssetsLoader

class Turtle(pygame.sprite.Sprite):

    @staticmethod
    def makeScaleDict():
        # Make a list to store the scale corresponding to the status
        # to prevent re-calculation
        scaleList = []
        for status in range(0, 21):
            scaleList.append(1.5*math.cos(3.14/2.5*status/20))
        return scaleList

    scaleDict = makeScaleDict()

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image_source = AssetsLoader.getImage("turtle")
        self.image = AssetsLoader.getImage("turtle")
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.rect = self.image.get_rect()
        self.initial_rect_width = self.rect.width
        self.initial_rect_height = self.rect.height
        self.speed = 10
        self.addspeed = 2
        self.status = random.randint(0, 19) # 初始状态，介于0-1之间
        self.scale_big_flag = True # 决定放大还是缩小
        self.drop_flag = False # 决定是否下落
        self.frozen = False # 为True时将冻结
        self.reset()
    
    def reset(self):
        self.speed = 5
        self.rect.top = -self.rect.height + 100
        self.rect.centerx = self.screen_size[0]/2
    
    def collide(self,other):
        return self.rect.colliderect(other.rect)

    def freeze(self):
        self.frozen = True

    def placeAfterCollide(self,other):
        self.rect.top = other.rect.top - self.rect.height

    def update(self):
        if not self.frozen:
            if self.drop_flag:
                self.rect.top += self.speed
                self.speed += self.addspeed
            else:
                if self.scale_big_flag:
                    self.status += 1
                else:
                    self.status -= 1
                
                if self.status >= 19:
                    self.scale_big_flag = False
                elif self.status <= 0:
                    self.scale_big_flag = True

                self.scale = Turtle.scaleDict[self.status]
                self.image = pygame.transform.scale(self.image_source, (int(self.initial_rect_width*self.scale), int(self.initial_rect_height*self.scale)))
                self.rect = self.image.get_rect()
                self.rect.centerx = self.screen_size[0]/2