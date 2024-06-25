# a simple program which uses pygame to render text onto a display surface
import pygame as pg

pg.font.init()

class Font:
    def __init__(self, display_surface : pg.Surface, default_font_size : int = 28, font = None, font_name=None) -> None:
        self.screen = display_surface
        self.default_font_size = default_font_size

        self.font = font if font != None else pg.font.Font(font_name, default_font_size)
      

    def draw(self, text : str, position : tuple, color : tuple = (255, 255, 255)) -> None:
        rendered_text = self.font.render(text, True, color)
        self.screen.blit(rendered_text, position)


# all possible fonts that can be used (built in)
if __name__ == "__main__":
    fonts = pg.font.get_fonts()
    for i in range(0, len(fonts)-1):
        print(fonts[i])
