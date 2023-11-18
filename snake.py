import pygame
from pygame import Rect, Vector2
import config as cfg
import utilities as utils
from tile import Tile
from pygame.sprite import Group

pygame.init()


class SnakeBlock(Tile):
    def __init__(self, position):
        super().__init__("snake", position)

    def update(self, prev_block, next_block, position):
        """Update sprite based on position of adjacent blocks.
        Previous block is the one closer to the head, next block is the one closer to the tail."""
        # TODO: Get sprites and decide which is the correct one
        self.position = position
        self.rect = self.image.get_rect(topleft=(position.x * cfg.GRIDSIZE, position.y * cfg.GRIDSIZE))

class Snake:
    def __init__(self, level_grid, environment, blocks, direction=Vector2(0, 1)):
        self.level_grid = level_grid
        self.environment = environment
        self.blocks = Group(blocks)
        self.direction = direction
        self.direction_dict = {
            pygame.K_UP: Vector2(0, -1),  # up
            pygame.K_DOWN: Vector2(0, 1),  # down
            pygame.K_LEFT: Vector2(-1, 0),  # left
            pygame.K_RIGHT: Vector2(1, 0),  # right
        }
        self.time_since_last_move = 0.0
        self.next_tile_image = utils.load_image("snake-next-tile")
        self.next_tile_alert_image = utils.load_image("snake-next-tile-alert")

    def get_next_move(self):
        return self.blocks.sprites()[0].position + self.direction  # where the snake will move next with no more inputs

    def move(self):
        # the head of the snake moves in direction
        new_headpos = self.get_next_move()

        # rest of the snake follows
        for i in range(len(self.blocks) - 1, 0, -1):
            block = self.blocks.sprites()[i]
            block.update(
                self.blocks.sprites()[i - 1],
                self.blocks.sprites()[i + 1] if i != len(self.blocks) - 1 else None,
                self.blocks.sprites()[i - 1].position
            )

        # update snake head
        self.blocks.sprites()[0].update(None,
                                        self.blocks.sprites()[1],
                                        new_headpos)

        # check if snake head is inside wall
        if pygame.sprite.spritecollideany(self.blocks.sprites()[0], self.environment["wall"]):
            # if so, trigger death event
            # TODO: add death event
            print("died")

        self.time_since_last_move = 0

    def update(self, dt):
        self.time_since_last_move += dt
        if self.time_since_last_move >= cfg.SNAKE_MOVE_INTERVAL:
            self.move()

    def handle_events(self, events):
        for event in events:
            # if event is a keypress on a direction key
            if event.type == pygame.KEYDOWN and event.key in self.direction_dict:
                # make sure moving in direction won't fold snake onto itself
                if self.blocks.sprites()[0].position + self.direction_dict[event.key] \
                        not in [block.position for block in self.blocks.sprites()[1:]]:
                    self.direction = self.direction_dict[event.key]

    def render(self, window):
        self.blocks.draw(window)

        # by default, next tile image is normal image
        next_tile_image = self.next_tile_image

        # if next move will go into wall, set next tile image to alert
        next_move_tile = self.level_grid[int(self.get_next_move().y)][int(self.get_next_move().x)]
        if next_move_tile and next_move_tile.type == "wall":
            next_tile_image = self.next_tile_alert_image

        window.blit(next_tile_image,
                    Vector2(self.get_next_move().x * cfg.GRIDSIZE, self.get_next_move().y * cfg.GRIDSIZE))
