import random
import tcod

from typing import Tuple
from typing import Iterator, Tuple

from game_map import GameMap
import tile_types


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x  # top left corner X coordinate
        self.y1 = y  # top left corner Y coordinate
        self.x2 = x + width  # bottom right corner X coordinate
        self.y2 = y + height  # bottom right corner Y coordinate

    # center of rectangular room
    # X and Y coordinates
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """
        return the inner area of this room as 2D array index
        """
        # x1 + 1 and y1 + 1 : for leaving a wall between two rooms
        # if rooms are neighbours
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)


def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor

    for x, y in tunnel_between(room_2.center, room_1.center):
        dungeon.tiles[x, y] = tile_types.floor

    return dungeon


# this function takes two Tuples args of two integers
# should return an iterator of Tuple of two integers
# all Tuples will be coordinates of the map
def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """
    return an L-shaped tunnel between two points
    """
    # grab cordinates from a Tuples
    x1, y1 = start
    x2, y2 = end

    # randomly pick between two options:
    # horoz -> vert *OR* vert -> horiz
    #
    # Based on what's chosen,
    # set corner_x and corner_y
    # values to different points
    if random.random() < 0.5:  # chance is 50%
        # move horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        # move vertically, then horizontally
        corner_x, corner_y = x1, y2

    # see https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    # generate the coordinates for the tunnel
    # get one line, then another to create an L-shaped tunnel
    # then .tolist() converts the points in the line into a list
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y  # return a generator
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y  # return a generator
