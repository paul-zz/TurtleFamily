import pygame
from .UIElements import UIElements

class LabelBox(UIElements):

    def __init__(self, x, y, w, h, 
                 text, 
                 text_color = (0, 0, 0), 
                 background_color = (255, 255, 255), 
                 show_border = True,
                 border_color = (0, 0, 0), 
                 font=pygame.font.get_default_font()):
        super().__init__(pygame.Rect(x, y, w, h))
        self.back_color = background_color
        self.text_color = text_color
        self.show_border = show_border
        self.border_color = border_color
        self.font = font
        self.text = text
        self.mouse_on = False


    def draw(self, surf : pygame.Surface):
        box_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        box_surf.set_alpha(self.alpha)
        pygame.draw.rect(box_surf, self.back_color, box_surf.get_rect())
        
        msg = self.font.render(self.text, 1, self.text_color)
        if msg.get_width() > self.rect.width:
            msg = self.squeeze_to_width(msg)
        
        if self.enableBlur:
            self.draw_blur_layer(surf, self.rect)

        surf.blit(box_surf, self.rect)
        if self.show_border:
            pygame.draw.rect(surf, self.border_color, self.rect, 2)
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        return self.rect

    def update(self, event):
        pass