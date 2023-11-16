import config as cfg
import utilities as utils
import pygame
from pygame.sprite import Sprite, Group
from pygame import Rect, Vector2

pygame.init()


class SnakeCharmer(Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = utils.load_image("snakecharmer", "snakecharmer")
        self.rect = self.image.get_rect(center=position)
