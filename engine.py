from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler


# Game main engine
class Engine:

    # entities was put in Set, hence no duplicates
    # Player's entity has separate reference for convinience
    def __init__(
        self, entities: Set[Entity], event_handler: EventHandler, player: Entity
    ):
        self.entiites = entities
        self.event_handler = event_handler
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

            # if action is instance of MevementAction class then
            # we need to move player's character on the board
            if isinstance(action, MovementAction):
                # self.player.move(dx=action,dx, dy=action.dy)
                self.player.move(action.dx, action.dy)
            # if action is instance of EscapeAction then
            # quit the program
            elif isinstance(action, EscapeAction):
                raise SystemExit()

    # game engine rendering
    def render(self, console: Console, context: Context) -> None:

        # iterate through all entities
        # and draw ther on the game screen
        for entity in self.entiites:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        # update the game screen
        context.present(console)

        # clear the console so there's
        # no movement traces
        console.clear()
