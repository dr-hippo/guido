import math
import pygame
from pygame import Vector2
import config as cfg

pygame.init()


class PhysicsBody:
    def __init__(self, position, mass=1, drag=1, velocity=Vector2(0, 0), acceleration=Vector2(0, 0)):
        self.position = position
        self.mass = mass
        self.drag = drag
        self.velocity = velocity
        self.acceleration = acceleration

        self.forces = [Vector2(0, cfg.GRAVSTRENGTH)]  # gravity force
        self.impulses = []

    def update(self, timestep):
        # TODO: use verlet integration for more accurate results
        totalforce = Vector2()
        for force in self.forces:
            totalforce += force

        for impulse in self.impulses:
            totalforce += impulse

        self.impulses = []

        oldvel = self.velocity.copy()
        self.acceleration = totalforce / self.mass  # a = F/m
        self.velocity += self.acceleration * timestep
        self.position += ((oldvel + self.velocity) / 2) * timestep

    def addforce(self, vector, impulse=False):
        if impulse:
            self.impulses.append(vector)
        else:
            self.forces.append(vector)
