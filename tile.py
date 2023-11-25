import pygame
from pygame.sprite import Sprite
import utilities as utils
import config as cfg

pygame.init()


class Tile(Sprite):
    def __init__(self, scene, tiletype, position):
        super().__init__()
        self.scene = scene
        self.type = tiletype
        self.position = position
        self.image = utils.load_image(self.type, "tiles")
        self.rect = self.image.get_rect(topleft=(position.x * cfg.GRIDSIZE, position.y * cfg.GRIDSIZE))


class Switch(Tile):
    def __init__(self, scene, position, connected_doors, index):
        super().__init__(self, "switch", position)
        self.active = False
        self.connected_doors = connected_doors

    def update(self, dt):
        self.active
