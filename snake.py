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
        self.image = pygame.surface.Surface((cfg.GRIDSIZE, cfg.GRIDSIZE))
        self.mask = pygame.mask.Mask((cfg.GRIDSIZE, cfg.GRIDSIZE))
        self.rect = self.image.get_rect(topleft=position * cfg.GRIDSIZE)

    def update(self, position):
        """Update sprite based on position of adjacent blocks.
        Previous block is the one closer to the head, next block is the one closer to the tail."""
        self.position = position
        self.rect = self.image.get_rect(topleft=position * cfg.GRIDSIZE)

    def get_image(self, prev_block, next_block):
        """Choose the correct sprite based on previous and next block"""
        rel_prevblock = prev_block - self.position if prev_block else None
        rel_nextblock = next_block - self.position if next_block else None

        block_state = "block-"  # assume this block is not head or tail unless otherwise set

        if cross_equals(rel_prevblock, rel_nextblock, Vector2(0, -1), Vector2(0, 1)):
            block_state += "vertical"

        elif cross_equals(rel_prevblock, rel_nextblock, Vector2(-1, 0), Vector2(1, 0)):
            block_state += "horizontal"

        elif cross_equals(rel_prevblock, rel_nextblock, Vector2(-1, 0), Vector2(0, 1)):
            block_state += "left-down"

        elif cross_equals(rel_prevblock, rel_nextblock, Vector2(1, 0), Vector2(0, 1)):
            block_state += "right-down"

        elif cross_equals(rel_prevblock, rel_nextblock, Vector2(-1, 0), Vector2(0, -1)):
            block_state += "left-up"

        elif cross_equals(rel_prevblock, rel_nextblock, Vector2(1, 0), Vector2(0, -1)):
            block_state += "right-up"

        # no previous block --> this block is the head
        # TODO: if I ever update to python 3.10, use a match-case block
        elif not rel_prevblock:
            block_state = "head-"
            if rel_nextblock == Vector2(0, 1):
                block_state += "up"

            elif rel_nextblock == Vector2(0, -1):
                block_state += "down"

            elif rel_nextblock == Vector2(1, 0):
                block_state += "left"

            elif rel_nextblock == Vector2(-1, 0):
                block_state += "right"

        # no next block --> this block is the tail
        # TODO: if I ever update to python 3.10, use a match-case block
        elif not rel_nextblock:
            block_state = "tail-"
            if rel_prevblock == Vector2(0, 1):
                block_state += "up"

            elif rel_prevblock == Vector2(0, -1):
                block_state += "down"

            elif rel_prevblock == Vector2(1, 0):
                block_state += "left"

            elif rel_prevblock == Vector2(-1, 0):
                block_state += "right"

        self.image = utils.load_image(block_state, "snake")
        self.mask = pygame.mask.from_surface(self.image)


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

        self.next_tile_image = utils.load_image("next-tile", "snake")
        self.next_tile_alert_image = utils.load_image("next-tile-alert", "snake")

        self.position_to_add_block = self[-1].position

        self.sounds = {}
        for soundname in utils.get_filenames("audio", "snake", filetype="mp3"):
            self.sounds[soundname] = utils.load_audio(soundname, "snake", filetype="mp3")

        # because direction changes are spammable, get a separate channel so it only interrupts itself
        self.change_direction_channel = pygame.mixer.find_channel()

        self.update_block_images()

    def __getitem__(self, item):
        return self.blocks.sprites()[item]

    def get_next_move(self):
        return self[0].position + self.direction  # where the snake will move next with no more inputs

    def occupies(self, position, startindex=0, endindex=None):
        """Checks if there is a snake block in the specified index range over the given position."""
        sprites = []
        if endindex:
            sprites = self[startindex:endindex]

        else:
            sprites = self[startindex:]

        return position in [sprite.position for sprite in sprites]

    def move(self):
        # the head of the snake moves in direction
        new_headpos = self.get_next_move()
        self.position_to_add_block = self[-1].position

        # rest of the snake follows
        for i in range(len(self.blocks) - 1, 0, -1):
            block = self[i]
            block.update(self[i - 1].position)

        # update snake head
        self[0].update(new_headpos)
        self.update_block_images()

        # check if snake has collided with a wall or a door
        if self.scene.data.get_group_collisions(self.blocks, "Wall"):
            # if so, trigger death
            self.scene.on_death("Snake ran into a wall ;(")
            self.sounds["hit-wall"].play()

        if self.scene.data.get_group_collisions(self.blocks, "Door"):
            # if so, trigger death
            self.scene.on_death("Snake ran into a door ;(")
            self.sounds["hit-wall"].play()

        # check if snake has collided with itself
        elif self.occupies(self[0].position, startindex=1):
            self.scene.on_death("Snake ran into itself ;&")

        self.sounds["slither"].play()

        self.time_since_last_move = 0

    def add_block(self):
        self.blocks.add(SnakeBlock(self.position_to_add_block))
        self.update_block_images()

    def update(self, dt):
        self.time_since_last_move += dt
        if self.time_since_last_move >= cfg.SNAKE_MOVE_INTERVAL:
            self.move()

    def update_block_images(self):
        for j in range(len(self.blocks)):
            self[j].get_image(
                self[j - 1].position if j != 0 else None,
                self[j + 1].position if j != len(self.blocks) - 1 else None
            )

    def handle_events(self, events):
        for event in events:
            # if event is a keypress on a direction key
            if event.type == pygame.KEYDOWN and event.key in self.direction_dict:
                # make sure moving in direction won't fold snake into itself
                if self[0].position + self.direction_dict[event.key] != self[1].position and \
                        self.direction_dict[event.key] != self.direction:
                    self.direction = self.direction_dict[event.key]
                    self.change_direction_channel.play(self.sounds["change-direction"])

    def render(self, window):
        self.blocks.draw(window)

        # by default, next tile image is normal image
        next_tile_image = self.next_tile_image

        # if next move will go into wall, door or snake itself, set next tile image to alert
        next_tile = self.scene.data.get_at(self.get_next_move())
        if next_tile and ((next_tile.get_name() == "Wall" or next_tile.get_name() == "Door")
                          and next_tile.groups()) or self.occupies(self.get_next_move(), endindex=-1):
            next_tile_image = self.next_tile_alert_image

        # blit next tile image at the correct location
        window.blit(next_tile_image,
                    Vector2(self.get_next_move() * cfg.GRIDSIZE))
