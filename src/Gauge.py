import pygame

class Gauge():

    def __init__(self, x, y, w, h, 
                 color, 
                 filled_color,
                 curr_val,
                 min_val,
                 max_val,  
                 show_text = True,
                 font = pygame.font.get_default_font()):
        self.color = color
        self.filled_color = filled_color
        self.rect = pygame.Rect(x, y, w, h)
        self.outer_rect = None
        self.min_val = min_val
        self.max_val = max_val
        self.curr_val = min(max(min_val, curr_val), max_val)

        self.show_text = show_text
        self.font = font
        self.draw_menu = False
        self.mouse_on = False
        self.drag = False

        # Appearance
        self.enableBlur = True
        self.blurRadius = 5
        self.alpha = 127

    def draw(self, surf : pygame.Surface):
        box_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        box_surf.set_alpha(self.alpha)

        percent_val = (self.curr_val - self.min_val)/(self.max_val - self.min_val)
        filled_rect = box_surf.get_rect().copy()
        filled_rect.width = int(percent_val*filled_rect.width)
        pygame.draw.rect(box_surf, self.color, box_surf.get_rect())
        pygame.draw.rect(box_surf, self.filled_color, filled_rect)
        
        if self.show_text:
            msg = self.font.render(str(self.curr_val), 1, (0, 0, 0))
            if msg.get_width() > self.rect.width:
                msg = self.squeeze_to_width(msg)
        
        blur_bg_surf = pygame.transform.gaussian_blur(surf.subsurface(self.rect), self.blurRadius)
        surf.blit(blur_bg_surf, self.rect)
        surf.blit(box_surf, self.rect)

        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        if self.show_text:
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
                self.drag = True
                self.curr_val = round(self.min_val + (mpos[0] - self.rect.x)/self.rect.width*(self.max_val - self.min_val))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.drag = False
        elif event.type == pygame.MOUSEMOTION and self.drag:
            if self.mouse_on:
                self.curr_val = round(self.min_val + (mpos[0] - self.rect.x)/self.rect.width*(self.max_val - self.min_val))
        elif event.type == pygame.MOUSEWHEEL:
            if self.mouse_on:
                if event.y > 0:
                    self.curr_val = min(self.curr_val + 1, self.max_val)
                else:
                    self.curr_val = max(self.curr_val - 1, self.min_val)

        return self.curr_val