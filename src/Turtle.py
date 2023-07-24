import pygame
import math
import random

class Turtle(pygame.sprite.Sprite):
    def __init__(self, image, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image_source = image
        self.image = image
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.rect = self.image.get_rect()
        self.initial_rect_width = self.rect.width
        self.initial_rect_height = self.rect.height
        self.speed = 10
        self.addspeed = 2
        self.status = random.random() # 初始状态，介于0-1之间
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
                if self.rect.top > self.screen_size[1]:
                    self.reset()
            else:
                if self.scale_big_flag:
                    self.status += 0.05
                else:
                    self.status -= 0.05
                
                if self.status>1:
                    self.scale_big_flag = False
                elif self.status<0:
                    self.scale_big_flag = True

                self.scale = 1.5*math.cos(3.14/2.5*self.status)
                self.image = pygame.transform.scale(self.image_source,(int(self.initial_rect_width*self.scale),int(self.initial_rect_height*self.scale)))
                self.rect = self.image.get_rect()
                self.rect.centerx = self.screen_size[0]/2