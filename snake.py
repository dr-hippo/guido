import pygame
from pygame import Rect, Vector2
import config as cfg
import utilities as utils
from pygame.sprite import Sprite, Group

pygame.init()


def cross_equals(a, b, c, d):
    return (a == c and b == d) or (a == d and b == c)


class SnakeBlock(Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = utils.load_image("snake", "snake")
        self.rect = self.image.get_rect(topleft=(position.x * cfg.GRIDSIZE, position.y * cfg.GRIDSIZE))

    def update(self, position):
        """Update sprite based on position of adjacent blocks.
        Previous block is the one closer to the head, next block is the one closer to the tail."""
        self.position = position
        self.rect = self.image.get_rect(topleft=(position.x * cfg.GRIDSIZE, position.y * cfg.GRIDSIZE))

    def choose_correct_sprite(self, prev_block, next_block):
        """Choose the correct sprite based on previous and next block"""
        rel_prevblock = prev_block - self.position if prev_block else None
        rel_nextblock = next_block - self.position if next_block else None
        print(rel_prevblock, rel_nextblock)

        block_state = ""

        if cross_equals(rel_prevblock, rel_nextblock, Vector2(0, -1), Vector2(0, 1)):
            block_state = "vertical"

        elif cross_equals(rel_prevblock, rel_nextblock, Vector2(-1, 0), Vector2(1, 0)):
            block_state = "horizontal"

        elif cross_equals(rel_prevblock, rel_nextblock, Vector2(-1, 0), Vector2(0, 1)):
            block_state = "left-down"

        elif cross_equals(rel_prevblock, rel_nextblock, Vector2(1, 0), Vector2(0, 1)):
            block_state = "right-down"

        elif cross_equals(rel_prevblock, rel_nextblock, Vector2(-1, 0), Vector2(0, -1)):
            block_state = "left-up"

        elif cross_equals(rel_prevblock, rel_nextblock, Vector2(1, 0), Vector2(0, -1)):
            block_state = "right-up"

        if block_state:
            self.image = utils.load_image("snakeblock-" + block_state, "snake")

        else:
            self.image = utils.load_image("snake", "snake")


class Snake:
    def __init__(self, scene):
        self.scene = scene
        self.blocks = Group(scene.data.snakedata)
        self.direction = scene.data.snakedir
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

    def occupies(self, position, startindex=0, endindex=-1):
        """Checks if there is a snake block in the specified index range over the given position."""
        return position in [block.position for block in self.blocks.sprites()[startindex:endindex]]

    def move(self):
        # the head of the snake moves in direction
        new_headpos = self.get_next_move()

        # rest of the snake follows
        for i in range(len(self.blocks) - 1, 0, -1):
            block = self.blocks.sprites()[i]
            block.update(self.blocks.sprites()[i - 1].position)

        # update snake head
        self.blocks.sprites()[0].update(new_headpos)

        for j in range(len(self.blocks)):
            self.blocks.sprites()[j].choose_correct_sprite(
                self.blocks.sprites()[j - 1].position if j != 0 else None,
                self.blocks.sprites()[j + 1].position if j != len(self.blocks) - 1 else None
            )

        # check if snake has collided with a wall or itself
        if pygame.sprite.spritecollideany(self.blocks.sprites()[0], self.scene.data.groups["wall"]):
            # if so, trigger death
            self.scene.on_death("Snake ran into a wall ;(")

        elif self.occupies(self.blocks.sprites()[0].position, startindex=1):
            self.scene.on_death("Snake ran into itself ;&")

        self.time_since_last_move = 0

    def update(self, dt):
        self.time_since_last_move += dt
        if self.time_since_last_move >= cfg.SNAKE_MOVE_INTERVAL:
            self.move()

    def handle_events(self, events):
        for event in events:
            # if event is a keypress on a direction key
            if event.type == pygame.KEYDOWN and event.key in self.direction_dict:
                # make sure moving in direction won't fold snake into itself
                if self.blocks.sprites()[0].position + self.direction_dict[event.key] \
                        != self.blocks.sprites()[1].position:
                    self.direction = self.direction_dict[event.key]

    def render(self, window):
        self.blocks.draw(window)

        # by default, next tile image is normal image
        next_tile_image = self.next_tile_image

        # if next move will go into wall, set next tile image to alert
        next_move_tile = self.scene.data.grid[int(self.get_next_move().y)][int(self.get_next_move().x)]
        if next_move_tile and next_move_tile.type == "wall" \
                or self.occupies(self.get_next_move()):
            next_tile_image = self.next_tile_alert_image

        window.blit(next_tile_image,
                    Vector2(self.get_next_move().x * cfg.GRIDSIZE, self.get_next_move().y * cfg.GRIDSIZE))
