from typing import Iterable, Any
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap

# Game main engine
class Engine:
    # entities was put in Set, hence no duplicates
    # Player's entity has separate reference for convinience
    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f"The {entity.name} wonders when it will get to take a real turn.")

    def handle_events(self, events: Iterable[Any]) -> None:
        # pass the events so the engine
        # could iterate through them
        for event in events:

            # send the event to event_handler dispatch method
            action = self.event_handler.dispatch(event)

            # if no key was pressed or key was not recognized
            # then skip the game loop
            if action is None:
                continue

            action.perform(self, self.player)

            self.handle_enemy_turns()

            # update FOV before player's action
            self.update_fov()

    def update_fov(self) -> None:
        """
        recompute the visible area based on the players point of view
        """
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # if a tile is "visible" it should be added to "explored"
        self.game_map.explored |= self.game_map.visible

    # game engine rendering
    def render(self, console: Console, context: Context) -> None:
        # draw map by using render method from game_map
        self.game_map.render(console)

        # update the game screen
        context.present(console)

        # clear the console so there's
        # no movement traces
        console.clear()
