import pygame
from pygame.sprite import Sprite
import utilities as utils
import config as cfg

pygame.init()


class Tile(Sprite):
    def __init__(self, tiletype, position):
        super().__init__()
        self.position = position
        self.type = tiletype
        self.image = utils.load_image(self.type, "tiles")
        print(self.image)
        self.rect = self.image.get_rect(topleft=(position.x * cfg.GRIDSIZE, position.y * cfg.GRIDSIZE))
