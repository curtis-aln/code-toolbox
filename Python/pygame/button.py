# pygame program which creates a usable button. when pressed the button will call a function

import pygame as pg
import time

from pygame import Rect

class Button:
    COOLDOWN = 0.25

    def __init__(self, center : tuple, size : tuple, text : str, color, hover_color, outline_color, font : pg.font.Font, func) -> None:
        self.rect = Rect(0, 0, size[0], size[1])
        self.set_center(center)

        self.color = color
        self.hover_color = hover_color
        self.outline_color = outline_color
        self.text = text
        self.font = font
        self.func = func
        self.last_pressed = 0
    

    def set_rect(self, rect : tuple) -> None:
        self.rect = Rect(rect)
    
    def set_center(self, center : tuple) -> None:
        self.rect.center = center
    
    def set_colors(self, fill_color = None, hover_color = None, outline_color = None) -> None:
        if fill_color:    self.color = fill_color
        if hover_color:   self.hover_color = hover_color
        if outline_color: self.outline_color = outline_color


    def draw(self, screen):
        hovering = self.is_hovered()
        current_time = time.time()
        
        # Change color on hover
        color = self.hover_color if hovering else self.color
        pg.draw.rect(screen, color, self.rect)
        pg.draw.rect(screen, self.outline_color, self.rect, 1)
      
        # Render the text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        # Handle button press
        if hovering and pg.mouse.get_pressed()[0]:
            if current_time - self.last_pressed > Button.COOLDOWN:
                self.last_pressed = current_time
                self.func(self)

    def is_hovered(self):
        mouse_pos = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)


class ToggleButton(Button):
    def __init__(self, pos, size, text, color, hover_color, outline_color, font, func):
        super().__init__(pos, size, text, color, hover_color, outline_color, font, func)
        self.toggle_state = False

    def draw(self, screen):
        current_time = time.time()
        
        # Change color based on toggle state
        color = self.hover_color if self.toggle_state else self.color
        pg.draw.rect(screen, color, self.rect)
        #pg.draw.rect(screen, self.outline_color, self.rect, 1)
        
        # Render the text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        # Handle button press
        if self.is_hovered() and pg.mouse.get_pressed()[0]:
            if current_time - self.last_pressed > Button.COOLDOWN:
                self.last_pressed = current_time
                self.func(self)
                self.toggle_state = not self.toggle_state
