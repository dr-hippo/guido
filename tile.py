import pygame
from pygame.sprite import Sprite
import utilities as utils
import config as cfg

pygame.init()


class Tile(Sprite):
    def __init__(self, scene, position):
        super().__init__()
        self.scene = scene
        self.position = position
        self.image = self._get_image()
        self.rect = self.image.get_rect(topleft=(position.x * cfg.GRIDSIZE, position.y * cfg.GRIDSIZE))

    def get_name(self):
        return self.__class__.__name__

    def _get_image(self):
        return utils.load_image(self.get_name().lower(), "tiles")

    def update(self, dt):
        pass


class Wall(Tile):
    pass


class Apple(Tile):
    def update(self, dt):
        if self.scene.snake.occupies(self.position):
            self.scene.snake.add_block()
            self.scene.data.empty(self.position)
            self.kill()


class Goal(Tile):
    def update(self, dt):
        # if player gets here, go to next level
        if pygame.sprite.collide_mask(self, self.scene.snakecharmer):
            self.scene.to_nextlevel()


class Door(Tile):
    def __init__(self, scene, position, index):
        self.index = index
        super().__init__(scene, position)
        self.active = True

    def _get_image(self):
        return utils.load_image(self.get_name().lower() + str(self.index + 1), "tiles")


class Switch(Tile):
    def __init__(self, scene, position, index, connected_door_coords):
        self.index = index
        super().__init__(scene, position)
        self.active = False
        self.connected_doors = []
        for door in connected_door_coords:
            self.connected_doors.append(self.scene.data.grid[connected_door_coords.y][connected_door_coords.x])

    def _get_image(self):
        return utils.load_image(self.get_name().lower() + str(self.index + 1), "tiles")
