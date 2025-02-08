import pygame

class UIElements():

    def __init__(self, rect : pygame.Rect):
        self.rect = rect

        # Appearance
        self.enableBlur = True
        self.blur_method = self.__triple_box_blur
        self.blurRadius = 3
        self.alpha = 127

    def fit_to_width(self, surf, proportion = 0.85):
        # Fit the text to the same width of the rect
        scale = proportion * self.rect.width / surf.get_width()
        surf = pygame.transform.scale(surf, (surf.get_width() * scale, surf.get_height() * scale))
        return surf
    
    def squeeze_to_width(self, surf, proportion = 0.85):
        surf = pygame.transform.scale(surf, (self.rect.width * proportion, surf.get_height()))
        return surf
    
    def draw_blur_layer(self, surf : pygame.Surface, rect : pygame.Rect):
        blur_bg_surf = self.blur_method(surf.subsurface(rect), self.blurRadius)
        surf.blit(blur_bg_surf, rect)

    def __triple_box_blur(self, surf : pygame.Surface, radius : int):
        surf_out = pygame.transform.box_blur(surf, radius)
        surf_out = pygame.transform.box_blur(surf_out, radius)
        surf_out = pygame.transform.box_blur(surf_out, radius)
        return surf_out