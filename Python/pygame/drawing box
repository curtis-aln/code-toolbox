import numpy as np
import numpy.random as random
import math

import pygame as pg
from pygame import Vector2 as Vec2
from pygame import Rect, Surface

from text_renderer import TextRenderer

from settings import *

# used for blurring
from scipy.ndimage import gaussian_filter


# drawing 4 lines as it is more efficient than rendering a box with rgba (0, 0, 0, 0) inside the box
def draw_rect_outline(render_surface : Surface, rect : Rect, color=(255, 255, 255), width=1) -> None:
    draw_line = lambda posA, posB: pg.draw.line(render_surface, color, posA, posB, width)
    
    draw_line(rect.topleft, rect.topright)
    draw_line(rect.bottomleft, rect.bottomright)
    draw_line(rect.topleft, rect.bottomleft)
    draw_line(rect.topright, rect.bottomright)


# so we need to convert that to be between 0 and 255 to render
def value01_to_color(value):
    norm = max(0, min(1, value)) * 255
    return (norm, norm, norm)


def generate_circle_indexes(center: Vec2, radius: int, grid_size: Vec2) -> np.ndarray:
    circle_points = []
    cx, cy = center
    width, height = grid_size
    
    for theta in range(0, 360):
        x = cx + radius * math.cos(math.radians(theta))
        y = cy + radius * math.sin(math.radians(theta))
        
        # Wrapping around the screen
        wrapped_x = int(round(x)) % width
        wrapped_y = int(round(y)) % height
        
        circle_points.append((wrapped_x, wrapped_y))
    
    return np.array(circle_points)


def draw_arrow(screen, color, start_pos, end_pos, width=2, two_headed=False):
    # drawing the line first # todo: arrow doesnt work two headed
    pg.draw.line(screen, color, start_pos, end_pos, width)

    # finding the vertices for the arrow head
    # p2 and p3 will be distance D away from p1 in directions of 60 degrees relative to the normal
    D = math.dist(start_pos, end_pos) * 0.025
    p1 = end_pos
    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])

    a = 6
    angle += math.pi / a  # 60 degrees in radians

    p2 = (round(p1[0] - D * math.cos(angle)), round(p1[1] - D * math.sin(angle)))

    angle -= 2 * math.pi / a  # 120 degrees in radians
    p3 = (round(p1[0] - D * math.cos(angle)), round(p1[1] - D * math.sin(angle)))

    pg.draw.polygon(screen, color, (p1, p2, p3))

    if two_headed == True:
        draw_arrow(screen, color, end_pos, start_pos, width, False)


class InteractiveBox:
    def __init__(self, window : Surface, bounds : Rect, grid_resolution : Vec2) -> None:
        self.window = window
        self.bounds = bounds

        self.text_renderer = TextRenderer(self.window, font_size=23)
        self.small_text_renderer = TextRenderer(self.window, font_size=15)

        self.render_gridlines = False

        dims = (int(grid_resolution.x), int(grid_resolution.y))
        self.grid = np.zeros(dims)

        # used for rendering the grid
        self.cell_size = Vec2(self.bounds.size[0] / self.grid.shape[0], 
                     self.bounds.size[1] / self.grid.shape[1])
    

    """ external input """
    def get_inputs(self): return np.reshape(self.grid, self.grid.shape[0] * self.grid.shape[1])

    def clear_grid(self): self.grid = np.zeros(self.grid.shape)

    # adding noise makes the neural network more robust (in theory)
    def add_noise(self, strength : float):
        self.grid += random.uniform(-strength, strength, self.grid.shape)
    
    # adding blur can hopefully improve performance the same way adding noise does
    def add_blur(self):
        sigma = 1.2
        self.grid = gaussian_filter(self.grid, sigma=sigma) 
    
    # clamping the grid to prevent values greater than 1 or less than 0
    def clamp_grid(self): self.grid = np.clip(self.grid, 0, 1)

    # pretty self explanatory 
    def inverse_grid(self): self.grid = 1 - self.grid
    

    def handle_click(self, remove_mode=False):
        mouse_pos = Vec2(pg.mouse.get_pos())
        relative_pos = mouse_pos - Vec2(self.bounds.topleft)

        # checking if the mouse collides with the grid
        if not self.bounds.collidepoint(mouse_pos):
            return

        # converting the mouse position into a grid index so we can see where it touched
        idx_X = int(relative_pos.x / self.cell_size.x)
        idx_Y = int(relative_pos.y / self.cell_size.y)
        indexes = generate_circle_indexes(Vec2(idx_X, idx_Y), BRUSH_RADIUS, self.grid.shape)
        
        # creating a mask so we can efficiently preform a matrix operation on self.grid. avoiding iteration
        circle_x, circle_y = indexes.T  # Transpose to get X and Y coordinates separately

        mask = np.zeros(self.grid.shape, dtype=bool)
        mask[circle_x, circle_y] = True

        self.grid += mask * (BRUSH_STENGTH if not remove_mode else -BRUSH_STENGTH)

        self.clamp_grid()

            


    def render(self):
        self._render_grid()
        self._render_border()
        self._render_grid_stats()

        if self.render_gridlines:
            self.render_gridlines()


    # renders the outline
    def _render_border(self):
        draw_rect_outline(self.window, self.bounds, width=3)
        self.text_renderer.draw_text("Interactive Window", self.bounds.topleft + Vec2(0, -15))
        
        # below the border we have text to show the possible interations
        pos = Vec2(self.bounds.bottomleft) + Vec2(0, 16)
        self.small_text_renderer.draw_text("[C] to clear",            pos)
        self.small_text_renderer.draw_text("[N] to add noise",        pos + Vec2(0, 10))
        self.small_text_renderer.draw_text("[B] to add blur",         pos + Vec2(0, 20))
        self.small_text_renderer.draw_text("[i] to inverse the grid", pos + Vec2(0, 30))
        self.small_text_renderer.draw_text("[Left Click] to Add",     pos + Vec2(0, 40))
        self.small_text_renderer.draw_text("[Right Click] to Remove", pos + Vec2(0, 50))


    def _render_grid(self):
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                rect = Rect(
                    self.bounds.x + x * self.cell_size.x,
                    self.bounds.y + y * self.cell_size.y,
                    self.cell_size.x, self.cell_size.y)
                color = value01_to_color(self.grid[x][y])

                pg.draw.rect(self.window, color, rect)


    def _render_grid_stats(self):
        bounds = self.bounds
        sep = 13
        cutoff = 10
        color = (255, 255, 255)
    
        x_axis_p1, x_axis_p2 = Vec2(bounds.x, bounds.y + bounds.h + sep), Vec2(bounds.x + bounds.w - cutoff, bounds.y + bounds.h + sep)
        y_axis_p1, y_axis_p2 = Vec2(bounds.x - sep, bounds.y + bounds.h), Vec2(bounds.x - sep, bounds.y + cutoff)
        
        draw_arrow(self.window, color, x_axis_p1, x_axis_p2, 2)
        draw_arrow(self.window, color, y_axis_p1, y_axis_p2, 2)

        x_axis_midpoint = (x_axis_p1 + x_axis_p2) / 2
        y_axis_midpoint = (y_axis_p1 + y_axis_p2) / 2

        dims = self.grid.shape
        self.text_renderer.draw_text(str(dims[0]), x_axis_midpoint + Vec2(0, +15), color, centered=True)
        self.text_renderer.draw_text(str(dims[1]), y_axis_midpoint + Vec2(-15, 0), color, centered=True)

        self.text_renderer.draw_text("X", x_axis_p2 + Vec2(cutoff, 0), centered=True)
        self.text_renderer.draw_text("Y", y_axis_p2 + Vec2(0, -cutoff), centered=True)
