import numpy as np
from tcod.console import Console
import tile_types


class GameMap:
    # take width and height integers and assign them
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        # create 2D array filled with the same values
        # fill with walls
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        """
        return True if X and Y are inside of the borders of map
        """
        result_1 = 0 <= x < self.width
        result_2 = 0 <= y < self.height

        return result_1 and result_2

    def render(self, console: Console) -> None:
        console.tiles_rgb[0 : self.width, 0 : self.height] = self.tiles["dark"]
