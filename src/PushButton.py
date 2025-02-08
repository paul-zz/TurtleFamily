import pygame
from .UIElements import UIElements

class PushButton(UIElements):

    def __init__(self, x, y, w, h, color, highlight_color, font, text):
        super().__init__(pygame.Rect(x, y, w, h))
        self.color = color
        self.highlight_color = highlight_color
        self.font = font
        self.text = text
        self.mouse_on = False
        self.pressed = False


    def draw(self, surf : pygame.Surface):
        box_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        box_surf.set_alpha(self.alpha)
        pygame.draw.rect(box_surf, self.highlight_color if self.mouse_on else self.color, box_surf.get_rect())
        
        msg = self.font.render(self.text, 1, (0, 0, 0))
        if msg.get_width() > self.rect.width:
            msg = self.squeeze_to_width(msg)
        
        if self.enableBlur:
            self.draw_blur_layer(surf, self.rect)
        surf.blit(box_surf, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        return self.rect

    def update(self, event):
        mpos = pygame.mouse.get_pos()
        self.mouse_on = self.rect.collidepoint(mpos)
        
        self.pressed = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.mouse_on:
                self.pressed = True

        return self.pressed