from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


# main Action class
class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform this action with objects needed to determine it's scope
        'engine' is the scope this action is being performed in
        'entity' is the object performing the action
        This method must be overridden by Action subclasses
        """

        raise NotImplementedError


# action on escape button pressed
# is Action subclass
class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


# players movement action class
# is Action subclass
class MovementAction(Action):
    # dx & dy are directions in which player is moveing
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        # check if tile moving is in bounds of map
        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds of MAP

        # check if tile moveing is walkable
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by some other object

        entity.move(self.dx, self.dy)
