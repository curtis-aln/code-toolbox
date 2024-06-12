import pygame as pg

def hex_to_rgb(value : str):
    # converts hex values into RGB values
    value = value.replace("#", "")
    return list(int(value[i:i+2], 16) for i in (0, 2, 4))


def rgb_similarity(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2

    # Calculate the difference between each RGB component
    diff_r = abs(r1 - r2)
    diff_g = abs(g1 - g2)
    diff_b = abs(b1 - b2)

    # Calculate the average difference as a percentage
    avg_diff = (diff_r + diff_g + diff_b) / 3
    similarity = 100 - (avg_diff / 255) * 100

    return similarity


class Color:
    def __init__(self, screen : pg.Surface, font : pg.font, rect : tuple, color : tuple, text) -> None:
        self.rect = rect
        self.color = color
        self.text = text
        self.screen = screen
        self.font = font

        white = (255, 255, 255)
        black = (0, 0, 0)
        color = white if rgb_similarity(self.color, white) < 80 else black
        self.text_info = self.generate_text_info(self.get_rect_center(self.rect), color)
      

    def get_rect_center(self, rect1):
        center = [rect1[0] + (rect1[2] / 2), rect1[1] + (rect1[3] / 2)]
        center[0] -= self.calc_text_size()[0] / 2
        center[1] -= self.calc_text_size()[1] / 2
        return center
    

    def calc_text_size(self):
        return self.font.size(self.text)
    

    def generate_text_info(self, pos, color=pg.Color('white')) -> list[list[pg.Surface, pg.Vector2]]:
        information = []

        words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.
        space = self.font.size(' ')[0]  # The width of a space.
        max_width = self.rect[2]
        x, y = pos

        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()

                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                information.append([word_surface, (x, y)])

                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

        return information


    def draw(self):
        # color rect
        pg.draw.rect(self.screen, self.color, self.rect)

        # text
        for surface, position in self.text_info:
            self.screen.blit(surface, position)