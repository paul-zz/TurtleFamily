import pygame

class SwitchButton():

    def __init__(self, x, y, w, h, color, highlight_color, font, text_on, text_off, checked = False):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.outer_rect = None
        self.font = font
        self.text = text_on if checked else text_off
        self.text_on = text_on
        self.text_off = text_off
        self.draw_menu = False
        self.mouse_on = False
        self.checked = checked

        # Appearance
        self.enableBlur = True
        self.blurRadius = 5
        self.alpha = 127

    def draw(self, surf : pygame.Surface):
        box_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        box_surf.set_alpha(self.alpha)
        pygame.draw.rect(box_surf, self.highlight_color if self.checked else self.color, box_surf.get_rect())
        
        msg = self.font.render(self.text, 1, (0, 0, 0))
        if msg.get_width() > self.rect.width:
            msg = self.squeeze_to_width(msg)
        
        blur_bg_surf = pygame.transform.gaussian_blur(surf.subsurface(self.rect), self.blurRadius)
        surf.blit(blur_bg_surf, self.rect)
        surf.blit(box_surf, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
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
        mpos = pygame.mouse.get_pos()
        self.mouse_on = self.rect.collidepoint(mpos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.mouse_on:
                self.checked = not self.checked
                self.text = self.text_on if self.checked else self.text_off

        return self.checked