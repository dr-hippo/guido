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
        self.image = self._get_image()
        self.rect = self.image.get_rect(topleft=(position.x * cfg.GRIDSIZE, position.y * cfg.GRIDSIZE))

    def get_name(self):
        return self.__class__.__name__

    def _get_image(self):
        return utils.load_image(self.get_name().lower(), "tiles")

    def update(self, snake, snakecharmer, dt):
        pass


class Wall(Tile):
    pass


class Apple(Tile):
    pass


class Goal(Tile):
    pass


class Door(Tile):
    def __init__(self, scene, position, index):
        self.index = index
        super().__init__(scene, position)

    def _get_image(self):
        return utils.load_image(self.get_name().lower() + str(self.index + 1), "tiles")


class Switch(Tile):
    def __init__(self, scene, position, index, connected_doors):
        self.index = index
        super().__init__(scene, position)
        self.active = False
        self.connected_doors = connected_doors

    def _get_image(self):
        return utils.load_image(self.get_name().lower() + str(self.index + 1), "tiles")
