import pygame
from pygame.sprite import Sprite
import utilities as utils

pygame.init()


class Tile(Sprite):
    def __init__(self, image_name):
        super().__init__()
        self.image = utils.load_image(image_name, "tiles")
        self.rect = self.image.get_rect()
