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

        # tiles that we can see at the moment
        self.visible = np.full((width, height), fill_value=False, order="F")
        # tiles that was explored earlier
        self.explored = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        """
        return True if X and Y are inside of the borders of map
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.
        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )
