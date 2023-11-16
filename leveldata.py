import json
import os
import config as cfg
import utilities as utils
from tile import Tile


class LevelData:
    def __init__(self, filename):
        # open json file with specified name and process it
        datapath = os.path.join("level-data", filename + os.extsep + "json")
        rawdata = open(datapath)
        self._data = json.load(rawdata)
        self.glyphkey = {
            "W": "wall",
            "S": "snaketail",
            "P": "player",
            " ": None
        }

        grid = []

        # initialise data
        for y in range(len(self._data["layout"])):
            grid.append([])
            for x in range(len(self._data["layout"][y])):
                # if the key exists and means something
                if self._data["layout"][y][x] in self.glyphkey.keys():
                    glyph_meaning = self.glyphkey[self._data["layout"][y][x]]
                    if glyph_meaning:
                        grid[y].append(Tile(glyph_meaning))

    def get_layout_to_render(self):
        """Return layout formatted for use in pygame.Surface.fblits call."""
        fblits_data = []
        for y in range(len(self._data["layout"])):
            for x in range(len(self._data["layout"][y])):
                glyph_meaning = self.glyphkey[self._data["layout"][y][x]]

                # if char at location means something
                if glyph_meaning:
                    fblits_data.append(
                        (utils.load_image(self.glyphkey[self._data["layout"][y][x]], "tiles"),  # image to blit
                         (x * cfg.GRIDSIZE, y * cfg.GRIDSIZE)  # position of blit
                         )
                    )

        return fblits_data
