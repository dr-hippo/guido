import math
import pygame
from pygame import Vector2
import config as cfg

pygame.init()


class PhysicsBody:
    def __init__(self, rect, velocity=Vector2(0, 0), acceleration=Vector2(0, 0)):
        self.rect = rect
        self.velocity = velocity
        self.acceleration = acceleration

    def physupdate(self, timestep):
        # TODO: use verlet integration for more accurate results
        oldvel = self.velocity.copy()
        self.velocity += (self.acceleration + Vector2(0, cfg.GRAVSTRENGTH)) * timestep
        self.rect.midbottom += (oldvel + self.velocity) / 2 * timestep

    def addforce(self, vector):
        self.acceleration += vector
