import tcod.event
from typing import Optional
from actions import Action, EscapeAction, MovementAction

# send an event to it's proper method
class EventHandler(tcod.event.EventDispatch[Action]):
    
    # exit on quit event (like pressing on 'X' window button)
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    # receive key press events, return Action or None
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        
        # whatever subclass of Action we assign
        action: Optional[Action] = None

        # what key is pressed
        key = event.sym

        # arrow keys movement
        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)
        
        # escape key action for MENU or else
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        return action

