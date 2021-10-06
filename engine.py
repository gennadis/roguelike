from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler


class Engine:
    '''
    this class is responsible of drwing the map and entities
    and handling players input
    '''
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player  # player is separate entity

    # pass events, iterate through them, handle events
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            if isinstance(action, MovementAction):
                self.player.move(dx=action.dx, dy=action.dy)
            
            elif isinstance(action, EscapeAction):
                raise SystemExit()
    
    # draw game screen
    # iterate through entities and print them on their locations
    def render(self, console: Console, context: Context) -> None:
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)
        
        # draw all objects on screen
        context.present(console)

        # clean all movement traces
        console.clear()

