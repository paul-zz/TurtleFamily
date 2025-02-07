"""
Reference:
https://stackoverflow.com/questions/19877900/tips-on-adding-creating-a-drop-down-selection-box-in-pygame
Author:
Rabbid76
"""
import pygame

class OptionBox():

    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected = 0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.outer_rect = None
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

        # Appearance
        self.enableBlur = True
        self.blurRadius = 5
        self.alpha = 127

    def draw(self, surf : pygame.Surface):
        box_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        box_surf.set_alpha(self.alpha)
        pygame.draw.rect(box_surf, self.highlight_color if self.menu_active else self.color, box_surf.get_rect())
        
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        if msg.get_width() > self.rect.width:
            msg = self.squeeze_to_width(msg)
        
        blur_bg_surf = pygame.transform.gaussian_blur(surf.subsurface(self.rect), self.blurRadius)
        surf.blit(blur_bg_surf, self.rect)
        surf.blit(box_surf, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        surf.blit(msg, msg.get_rect(center = self.rect.center))
        
        if self.draw_menu:
            self.outer_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            
            surf_outer_option = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            surf_outer_option.set_alpha(self.alpha)

            blur_outer_bg_surf = pygame.transform.gaussian_blur(surf.subsurface(self.outer_rect), self.blurRadius)
            surf.blit(blur_outer_bg_surf, self.outer_rect)
            
            rect_font = self.outer_rect.copy()
            rect_font.height = self.rect.height

            rect_option = surf_outer_option.get_rect().copy()
            rect_option.x = self.outer_rect.x
            rect_option.y = self.outer_rect.y

            for i, text in enumerate(self.option_list):
                pygame.draw.rect(surf_outer_option, self.highlight_color if i == self.active_option else self.color, surf_outer_option.get_rect())
                surf.blit(surf_outer_option, rect_option)
                
                msg = self.font.render(text, 1, (0, 0, 0))

                if msg.get_width() > self.rect.width:
                    msg = self.squeeze_to_width(msg)
                surf.blit(msg, msg.get_rect(center = rect_font.center))

                rect_font.y += self.rect.height
                rect_option.y += rect_option.height
            
            pygame.draw.rect(surf, (0, 0, 0), self.outer_rect, 2)
        return [self.rect, self.outer_rect]
    
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
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        if self.outer_rect and self.outer_rect.collidepoint(mpos):
            self.active_option = int((mpos[1] - self.outer_rect.y) / self.rect.height)

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.selected = self.active_option
                self.draw_menu = False
                return self.active_option
        return -1