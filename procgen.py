from __future__ import annotations

import random
import tcod

import entity_factories

from typing import Iterator, List, Tuple, TYPE_CHECKING

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity


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
        """Return the inner area of this room as a 2D array index."""

        # x1 + 1 and y1 + 1 : for leaving a wall between two rooms
        # if rooms are neighbours
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    # check if there's an intersection (overlapping) between rooms
    def intersects(self, other: RectangularRoom) -> bool:
        """
        Return True if this room overlaps with another RectangularRoom
        """
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def place_entities(
    room: RectangularRoom,
    dungeon: GameMap,
    maximum_monsters: int,
) -> None:
    number_of_monsters = random.randint(0, maximum_monsters)
    for i in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)  # select random x coord
        y = random.randint(room.y1 + 1, room.y2 - 1)  # select random y coord

        # check if there's no other entities in given tile! no stacking needed in game
        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entity_factories.orc.spawn(dungeon, x, y)
            else:
                entity_factories.troll.spawn(dungeon, x, y)


def generate_dungeon(
    max_rooms: int,  # max numbers of rooms
    room_min_size: int,  # room min size
    room_max_size: int,  # room max size
    map_width: int,  # map dimensions
    map_height: int,  # map dimensions
    max_monsters_per_room: int,
    player: Entity,  # where to place Player's character
) -> GameMap:
    """
    Generate a new map with a dungeons
    """
    # create the initial GameMap
    dungeon = GameMap(map_width, map_height, entities=[player])

    # store a list of all rooms
    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        # with given max and min room sizes,
        # set the room's width and height
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        # with random x and y coordinates,
        # try to place a room
        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # create an instance of rectangular room with given parametes
        new_room = RectangularRoom(x, y, room_width, room_height)

        # run through the other rooms and see if they intersects with this one
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # this room intersects, so try again
            # if there are no intersections, then room is valid

        # dig out this rooms inner area
        dungeon.tiles[new_room.inner] = tile_types.floor

        # place created entities int the room
        place_entities(new_room, dungeon, max_monsters_per_room)

        if len(rooms) == 0:
            # this is the first room,
            # where the player should be placed and start
            player.x, player.y = new_room.center
        else:  # all rooms after the first
            # dig out the tunnels between this room and previous one
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        # add to rooms list
        rooms.append(new_room)

    return dungeon


# this function takes two Tuples args of two integers
# should return an iterator of Tuple of two integers
# all Tuples will be coordinates of the map
def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """
    return an L-shaped tunnel between these two points
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
