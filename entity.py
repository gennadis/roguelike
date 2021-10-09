from typing import Tuple


class Entity:
    """
    Generic class for every Entity in game
    like player's character, enemies, items and etc.
    """

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        # move method for moving an Entity instance
        # by some given amount
        self.x += dx
        self.y += dy


if __name__ == "__main__":
    pass
