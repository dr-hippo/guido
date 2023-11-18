import json
import os
import config as cfg
import utilities as utils
from tile import Tile
from pygame.sprite import Group
from pygame import Vector2


class LevelData:
    def __init__(self, filename):
        # open json file with specified name and process it
        datapath = os.path.join(utils.current_path, "level-data", filename + os.extsep + "json")
        rawdata = open(datapath)
        self._data = json.load(rawdata)
        self.glyphkey = {
            "W": "wall",
            "S": "snaketail",
            "P": "player",
            " ": None
        }

        self.playerspawn = Vector2(self._data["playerspawn"])

        self.groups = {
            "wall": Group(),
        }

        self.grid = []

        # initialise data
        for y in range(len(self._data["layout"])):
            self.grid.append([])
            for x in range(len(self._data["layout"][y])):
                # if the key exists and means something
                if self._data["layout"][y][x] in self.glyphkey.keys():
                    glyph_meaning = self.glyphkey[self._data["layout"][y][x]]
                    if glyph_meaning:
                        # add tile to grid and correct sprite group
                        tile = Tile(glyph_meaning, Vector2(x, y))
                        self.grid[y].append(tile)
                        self.groups[glyph_meaning].add(tile)

                    else:
                        self.grid[y].append(None)

    def get_layout_to_render(self):
        """Return layout formatted for use in pygame.Surface.fblits call."""
        fblits_data = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                tile = self.grid[y][x]
                if tile:
                    fblits_data.append((tile.image, tile.rect))

        return tuple(fblits_data)
