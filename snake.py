import pygame
from pygame import Rect, Vector2
import config as cfg

pygame.init()

SNAKE_ADVANCE = pygame.event.custom_type()


class SnakeBlock:
    def __init__(self, position):
        self.position = position


class Snake:
    def __init__(self, blocks, direction=Vector2(0, 1)):
        self.blocks = blocks
        self.direction = direction
        self.direction_dict = {
            pygame.K_w: Vector2(0, -1),  # up
            pygame.K_s: Vector2(0, 1),  # down
            pygame.K_a: Vector2(-1, 0),  # left
            pygame.K_d: Vector2(1, 0),  # right
        }

    def get_next_move(self):
        return self.blocks[0].position + self.direction  # where the snake will move next assuming no further input

    def advance(self):
        # the head of the snake moves in direction
        new_headpos = self.get_next_move()

        # rest of the snake follows
        for i in range(len(self.blocks) - 1, 0, -1):
            block = self.blocks[i]
            block.position = self.blocks[i - 1].position

        self.blocks[0].position = new_headpos

    def handle_events(self, events):
        # get key states of WASD keys with list comprehension

        for event in events:
            if event.type == SNAKE_ADVANCE:
                self.advance()

            # if event is a keypress on a direction key
            if event.type == pygame.KEYDOWN and event.key in self.direction_dict:
                self.direction = self.direction_dict[event.key]

    def render(self, window):
        for block in self.blocks:
            pygame.draw.rect(window,
                             (0, 255, 0),
                             Rect(block.position.x * cfg.GRIDSIZE, block.position.y * cfg.GRIDSIZE, cfg.GRIDSIZE,
                                  cfg.GRIDSIZE),
                             )
            pygame.draw.rect(window,
                             (255, 255, 0),
                             Rect(self.get_next_move().x * cfg.GRIDSIZE, self.get_next_move().y * cfg.GRIDSIZE,
                                  cfg.GRIDSIZE, cfg.GRIDSIZE),
                             )
