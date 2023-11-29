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
        # if snake eats this, add block to it and then destroy self
        if self.scene.snake.occupies(self.position):
            self.scene.snake.add_block()
            self.scene.data.empty(self.position)
            utils.load_audio("crunch", "environment").play()
            self.kill()


class Goal(Tile):
    def __init__(self, scene, position):
        super().__init__(scene, position)
        self.level_pass_sound = utils.load_audio("level-pass", "environment")

    def update(self, dt):
        # if player gets here, go to next level
        if pygame.sprite.collide_mask(self, self.scene.snakecharmer):
            self.level_pass_sound.play()
            self.scene.to_nextlevel()


class Door(Tile):
    def __init__(self, scene, position, index):
        self.index = index
        self._active = True
        super().__init__(scene, position)
        self.crush_sound = utils.load_audio("door-crush", "environment")

    def _get_image(self):
        if self.get_active():
            return utils.load_image(self.get_name().lower() + str(self.index + 1), "tiles")

        return utils.load_image(self.get_name().lower() + str(self.index + 1) + "-inactive", "tiles")

    def get_active(self):
        return self._active

    def set_active(self, value):
        if type(value) != bool:
            raise TypeError("Value must be True or False.")

        self._active = value
        self.image = self._get_image()

        # door has been activated
        if value:
            self.scene.data.groups["Door"].add(self)

            collision = self.rect.clip(self.scene.snakecharmer.rect)

            # only kill player if it's deep inside the door, otherwise let it resolve the collision normally
            if collision and min(collision.w, collision.h) > 2:
                self.scene.on_death("Door crushed Guido ;(")
                self.crush_sound.play()

            if self.scene.snake.occupies(self.position):
                self.scene.on_death("Door crushed snake ;(")
                self.crush_sound.play()

        # door has been deactivated
        else:
            self.kill()


class Switch(Tile):
    def __init__(self, scene, position, index, connected_door_coords):
        self.index = index
        self.active = False
        super().__init__(scene, position)
        self.scene = scene
        self.connected_door_coords = connected_door_coords
        self.connected_doors = []

        self.activate_sound = utils.load_audio("switch-on", "environment")
        self.deactivate_sound = utils.load_audio("switch-off", "environment")

    def _get_image(self):
        if self.active:
            return utils.load_image(self.get_name().lower() + str(self.index + 1) + "-active", "tiles")

        return utils.load_image(self.get_name().lower() + str(self.index + 1), "tiles")

    def update(self, dt):
        active_buffer = self.active

        # can't do this in __init__ due to self.scene.data not fully initialised (prob. a race condition)
        if not self.connected_doors:
            for coord in self.connected_door_coords:
                self.connected_doors.append(self.scene.data.grid[coord[1]][coord[0]])

        # actual update code
        self.active = self.scene.snake.occupies(self.position) or \
                      pygame.sprite.collide_rect(self, self.scene.snakecharmer)

        # if active state isn't the same as before, update image/connected doors and play appropriate sound
        if self.active != active_buffer:
            self.image = self._get_image()
            if self.active:
                self.activate_sound.play()

            else:
                self.deactivate_sound.play()

            for door in self.connected_doors:
                door.set_active(not self.active)
