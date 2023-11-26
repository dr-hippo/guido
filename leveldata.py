import json
import os
import config as cfg
import utilities as utils
import importlib
from pygame.sprite import Group, spritecollide
from pygame import Vector2
from snake import SnakeBlock

tile = importlib.import_module("tile")


class LevelData:
    def __init__(self, scene, filename):
        self.scene = scene

        # open json file with specified name and process it
        datapath = os.path.join(utils.current_path, "level-data", filename + os.extsep + "json")
        rawdata = open(datapath)
        self._data = json.load(rawdata)

        self.glyphkey = {
            "W": "Wall",
            "A": "Apple",
            "G": "Goal",
            " ": None
        }

        self.snakedir = self._data["snakedir"]

        # load snake data into list of SnakeBlocks
        self.snakedata = []
        for pos in self._data["snake"]:
            self.snakedata.append(SnakeBlock(Vector2(pos)))

        self.playerspawn = Vector2(self._data["playerspawn"])

        # create sprite groups based on values of glyphkeys
        self.groups = {}
        for v in self.glyphkey.values():
            if v:
                self.groups[v] = Group()

        # initialise grid and groups
        # TODO: make this readable
        self.grid = []
        self.switchdict = self._data["switchdict"] if "switchdict" in self._data else {}

        for y in range(len(self._data["layout"])):
            self.grid.append([])
            for x in range(len(self._data["layout"][y])):
                glyph = self._data["layout"][y][x]
                glyph_class_name = self.glyphkey[glyph] if glyph in self.glyphkey else None
                if glyph_class_name:
                    # add tile to grid and correct sprite group
                    newtile = getattr(tile, glyph_class_name)(self.scene, Vector2(x, y))
                    self.grid[y].append(newtile)
                    self.groups[glyph_class_name].add(newtile)

                elif glyph in self.switchdict:
                    # TODO: create switches, doors, and link them up
                    pass

                else:
                    self.grid[y].append(None)

    def empty(self, position):
        self.grid[int(position.y)][int(position.x)] = None

    def get_rects(self, *groups):
        rects = []
        for group in groups:
            rects += [sprite.rect for sprite in self.groups[group].sprites()]

        return rects

    def get_sprite_collisions(self, sprite, *groups):
        collision_list = []
        for group in groups:
            collision_list += spritecollide(sprite, self.groups[group], False)

        return collision_list

    def get_layout_to_render(self):
        """Return layout formatted for use in pygame.Surface.fblits call."""
        fblits_data = []
        for row in self.grid:
            for square in row:
                if square:
                    fblits_data.append((square.image, square.rect))

        return tuple(fblits_data)
