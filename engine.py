from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap

# Game main engine
class Engine:

    # entities was put in Set, hence no duplicates
    # Player's entity has separate reference for convinience
    def __init__(
        self,
        entities: Set[Entity],
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ):
        self.entiites = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

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

    # game engine rendering
    def render(self, console: Console, context: Context) -> None:
        # draw map by using render method from game_map
        self.game_map.render(console)

        # iterate through all entities
        # and draw ther on the game screen
        for entity in self.entiites:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        # update the game screen
        context.present(console)

        # clear the console so there's
        # no movement traces
        console.clear()
