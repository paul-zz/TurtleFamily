import pygame

class LabelBox():

    def __init__(self, x, y, w, h, 
                 text, 
                 text_color = (0, 0, 0), 
                 background_color = (255, 255, 255), 
                 show_border = True,
                 border_color = (0, 0, 0), 
                 font=pygame.font.get_default_font()):
        self.back_color = background_color
        self.text_color = text_color
        self.show_border = show_border
        self.border_color = border_color
        self.rect = pygame.Rect(x, y, w, h)
        self.outer_rect = None
        self.font = font
        self.text = text
        self.draw_menu = False
        self.mouse_on = False

        # Appearance
        self.enableBlur = True
        self.blurRadius = 5
        self.alpha = 127

    def draw(self, surf : pygame.Surface):
        box_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        box_surf.set_alpha(self.alpha)
        pygame.draw.rect(box_surf, self.back_color, box_surf.get_rect())
        
        msg = self.font.render(self.text, 1, self.text_color)
        if msg.get_width() > self.rect.width:
            msg = self.squeeze_to_width(msg)
        
        blur_bg_surf = pygame.transform.gaussian_blur(surf.subsurface(self.rect), self.blurRadius)
        surf.blit(blur_bg_surf, self.rect)
        surf.blit(box_surf, self.rect)
        if self.show_border:
            pygame.draw.rect(surf, self.border_color, self.rect, 2)
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        return self.rect
    
    def fit_to_width(self, surf, proportion = 0.85):
        # Fit the text to the same width of the rect
        scale = proportion * self.rect.width / surf.get_width()
        surf = pygame.transform.scale(surf, (surf.get_width() * scale, surf.get_height() * scale))
        return surf
    
    def squeeze_to_width(self, surf, proportion = 0.85):
        surf = pygame.transform.scale(surf, (self.rect.width * proportion, surf.get_height()))
        return surf

    def update(self, event):
        pass