import pygame as pg
import math

from pygame import Vector2, Rect, Surface
from math import sqrt
from numpy.random import randint, uniform
from utils.random import randPosition, randVelocity

from math import dist
from physics.entity_physics import resolve_collision

class Entity:
    def __init__(self, screen_border, position : Vector2, velocity : Vector2, mass, max_speed) -> None:
        self.velocity = velocity
        self.mass = mass
        self.max_speed = max_speed

        self.screen_border = screen_border
        self.entity_border = Rect(position.x, position.y, mass*2, mass*2)
        self.position = self.get_center()


    @classmethod
    def generate_random(cls, border):
        position = randPosition(border)
        velocity = randVelocity(-1, 1)
        return Entity(border, position, velocity, randint(5, 20), uniform(1, 4))
    

    # physics related functions
    def handle_collision(self, entity):
        # Calculate collision axis and distance between objects
        collision_vector = self.get_center() - entity.get_center()
        distance = collision_vector.length()

        normal_vector = collision_vector / distance
        overlap = (self.mass + entity.mass) - distance

        # Calculate the mass ratio between the two objects
        mass_ratio = self.mass / entity.mass
        self_movement = normal_vector * overlap * mass_ratio / (mass_ratio + 1)
        other_movement = normal_vector * overlap * 1 / (mass_ratio + 1)
        
        # Move both objects away from each other based on their mass
        self.add_velocity(self_movement)
        entity.minus_velocity(other_movement)


    #def boundery_screen(self):
    #    self.entity_border.clamp_ip(self.screen_border)
    
    def boundary_screen(self):
        # Calculate the edges of the screen border
        screen_left = self.screen_border.left
        screen_right = self.screen_border.right
        screen_top = self.screen_border.top
        screen_bottom = self.screen_border.bottom

        # Check if the entity is going off the left or right edge of the screen
        if self.entity_border.left < screen_left or self.entity_border.right > screen_right:
            # Reverse the x velocity of the entity
            self.velocity.x *= -1

        # Check if the entity is going off the top or bottom edge of the screen
        if self.entity_border.top < screen_top or self.entity_border.bottom > screen_bottom:
            # Reverse the y velocity of the entity
            self.velocity.y *= -1
        
        self.entity_border.clamp_ip(self.screen_border)
    

    def bounce_off(self, other_entity):
        distance = math.dist(self.get_center(), other_entity.position)
        sumRad   = (self.entity_border.width/2) + (other_entity.entity_border.width/2)
        if distance > sumRad: 
            return
        
        self.velocity, other_entity.velocity = resolve_collision(
            self.position, self.entity_border.width/2, self.velocity,
            other_entity.position, other_entity.entity_border.width/2, other_entity.velocity,    
        )

        self.handle_collision(other_entity)
     
    # other
    def resize_border(self):
        self.entity_border.width = self.mass*2
        self.entity_border.height = self.mass*2
    

    def draw_debug(self, screen : Surface):
        # border
        pg.draw.rect(screen, (255, 0, 0), self.entity_border, 1)

        # velocity
        clamped_vel = self.velocity.copy() + Vector2(0.001, 0.001)
        clamped_vel.scale_to_length(self.mass*2)
        size = round(self.mass/5)
        pg.draw.line(screen, (40, 40, 230), self.get_center(), self.get_center() + clamped_vel, size)

    

    def get_center(self):
        return Vector2(self.entity_border.centerx, self.entity_border.centery)

    def add_velocity(self, velocity : Vector2):
        self.entity_border.centerx += round(velocity.x)
        self.entity_border.centery += round(velocity.y)

    def minus_velocity(self, velocity : Vector2):
        self.entity_border.centerx -= round(velocity.x)
        self.entity_border.centery -= round(velocity.y)

    def apply_friction(self, friction):
        self.velocity /= friction


    def speed_limit(self):
        speed = sqrt(self.velocity.x * self.velocity.x + self.velocity.y * self.velocity.y)

        if speed > self.max_speed:
            self.velocity.x = (self.velocity.x / speed) * self.max_speed
            self.velocity.y = (self.velocity.y / speed) * self.max_speed
    

    def sort_nearby(self, array):
        return [
            cell for cell in array 
            if cell != self and dist(self.get_center(), cell.get_center()) < self.visual_range
        ]