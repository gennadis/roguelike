from typing import Tuple

import numpy as np

# tile graphics srtuctured type compatible with Console.tiles.rgb
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # ch - character
        ("fg", "3B"),  # foreground color. 3B - three unsigned bytes -> RGB color
        ("bg", "3B"),  # bg - background color. 3B - three unsigned bytes -> RGB color
    ]
)


# tile struct used for statically defined tile data
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # bool True if this tile can be walked over
        ("transparent", np.bool),  # bool True if this tile doesn't block FOV
        ("dark", graphic_dt),  # graphics for when this tile is not in FOV
    ]
)

# create and return NumPy array of ONE single tile
def new_tile(
    *,
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    return np.array((walkable, transparent, dark), dtype=tile_dt)


floor = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 150))
)
wall = new_tile(
    walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100))
)
water = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (30, 144, 255), (0, 0, 100))
)
lava = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 0), (0, 0, 100))
)
