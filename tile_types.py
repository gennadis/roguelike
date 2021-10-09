from typing import Tuple

import numpy as np

graphic_dt = np.dtype([("ch", np.int32), ("fg", "38"), ("bg", "38")])

tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
    ]
)
