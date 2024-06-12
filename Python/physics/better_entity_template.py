import pygame as pg
from pygame import Vector2, Rect, Surface

from math import sqrt, dist
from numpy.random import randint, uniform


def randPosition(border : Rect) -> Vector2:
    return Vector2(
        uniform(border.left, border.left + border.width), 
        uniform(border.top,  border.top  + border.height)
        )


def randVelocity(min_acc, max_acc) -> Vector2:
    return Vector2(tuple(uniform(min_acc, max_acc, 2)))


def rand_pos_in_rect(rectangle : tuple) -> Vector2:
    """ this generates a random Vector2 position inside of a rectangle """
    x1, y1, x2, y2 = rectangle
    return Vector2(randint(x1, x2), randint(y1, y2))


class Particle:
    def __init__(self, border : Vector2, pos : Vector2, vel : Vector2, 
                 rad : float, max_speed : float, color : tuple) -> None:
        self.position = pos
        self.velocity = vel
        self.radius = rad
        self.color = color
        self.max_speed = max_speed

        self.border = border


    @classmethod
    def generate_random(cls, border):
        position = randPosition(border)
        velocity = randVelocity(-1, 1)
        return Particle(border, position, velocity, randint(5, 20), uniform(1, 4))
    

    def boundary_screen(self):
        # Check if the entity is going off the left or right edge of the screen
        if self.position.x < self.border.left or self.position.x > self.border.right:
            # Reverse the x velocity of the entity
            self.velocity.x *= -1

        # Check if the entity is going off the top or bottom edge of the screen
        if self.position.y < self.border.top or self.position.y > self.border.bottom:
            # Reverse the y velocity of the entity
            self.velocity.y *= -1
            
    
    def draw(self, screen : Surface) -> None:
        pg.draw.circle(screen, self.color, self.position, self.radius)
    
    def draw_debug(self, screen : Surface):
        # velocity
        clamped_vel = self.velocity.copy() + Vector2(0.001, 0.001)
        clamped_vel.scale_to_length(self.radius*2)
        size = round(self.radius/5)
        pg.draw.line(screen, (40, 40, 230), self.get_center(), self.get_center() + clamped_vel, size)

    def apply_friction(self, friction):
        self.velocity /= friction

    def speed_limit(self):
        speedSq = self.velocity.x * self.velocity.x + self.velocity.y * self.velocity.y

        if speedSq > self.max_speed * self.max_speed:
            speed = sqrt(speedSq)
            self.velocity.x = (self.velocity.x / speed) * self.max_speed
            self.velocity.y = (self.velocity.y / speed) * self.max_speed
    


    def update(self, nearby_particles : list, sort=True):
        if sort == True: nearby_particles = self.sort_nearby(nearby_particles)
        
        self.speed_limit()
        self.position += self.velocity
        self.boundary_screen()
    

    def sort_nearby(self, array):
        return [
            cell for cell in array 
            if cell != self and dist(self.get_center(), cell.get_center()) < self.visual_range
        ]
