import pygame
from pygame.sprite import Sprite
import utilities as utils
import config as cfg

pygame.init()


class Tile(Sprite):
    def __init__(self, scene, position):
        super().__init__()
        self.scene = scene
        self.position = position
        self.image = utils.load_image(self.get_name(), "tiles")
        self.rect = self.image.get_rect(topleft=(position.x * cfg.GRIDSIZE, position.y * cfg.GRIDSIZE))

    def get_name(self):
        return self.__class__.__name__


class Wall(Tile):
    pass


class Apple(Tile):
    pass


class Goal(Tile):
    pass


class Door(Tile):
    pass


class Switch(Tile):
    def __init__(self, scene, position, connected_doors, index):
        super().__init__(self, scene, position)
        self.active = False
        self.connected_doors = connected_doors
        self.index = index

    def update(self, dt):
        pass
