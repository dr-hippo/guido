import json
import os
import config as cfg


class LevelData:
    def __init__(self, filename):
        # open json file with specified name and process it
        datapath = os.path.join("level-data", filename + os.extsep + "json")
        rawdata = open(datapath)
        self._data = json.load(rawdata)

    def get_layout_to_render(self):
        """Return layout formatted for use in pygame.Surface.fblits call"""
        for row in self._data.layout:
            for tile in row:
                print(tile)
