import config as cfg
import utilities as utils
import pygame
from pygame.sprite import Sprite, Group
from pygame import Rect, Vector2

pygame.init()


class SnakeCharmer(Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = utils.load_image("snakecharmer", "snakecharmer")
        self.rect = self.image.get_rect(midbottom=position)
        self.movingleft = False
        self.movingright = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    pass

                if event.key == pygame.K_a:
                    self.movingleft = True

                if event.key == pygame.K_d:
                    self.movingright = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movingleft = False

                if event.key == pygame.K_d:
                    self.movingright = False

    def update(self, dt):
        if self.movingleft:
            self.rect.centerx -= 1

        if self.movingright:
            self.rect.centerx += 1
