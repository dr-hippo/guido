import config as cfg
import utilities as utils
import pygame
from pygame.sprite import Sprite, Group
from pygame import Rect, Vector2
from physicsbody import PhysicsBody

pygame.init()


class SnakeCharmer(Sprite, PhysicsBody):
    def __init__(self, level_grid, environment, position):
        Sprite.__init__(self)
        PhysicsBody.__init__(self, position)
        self.image = utils.load_image("snakecharmer", "snakecharmer")
        self.rect = self.image.get_rect(midbottom=position)
        self.level_grid = level_grid
        self.environment = environment
        self.movingleft = False
        self.movingright = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    # jump
                    self.addforce(Vector2(0, -cfg.SNAKECHARMER_JUMP_FORCE))

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
        Sprite.update(self)
        PhysicsBody.update(self, dt)
        if self.movingleft:
            self.position.x -= cfg.SNAKECHARMER_MOVE_SPEED

        if self.movingright:
            self.position.x += cfg.SNAKECHARMER_MOVE_SPEED

        self.rect.midbottom = self.position
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
