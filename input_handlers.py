import tcod.event
from typing import Optional
from actions import Action, BumpAction, EscapeAction

# create new class which is subclass of EventDispatch class
# that allows to send an event to it's proper method
class EventHandler(tcod.event.EventDispatch[Action]):
    # if the 'X' window button is pressed then EXIT
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    # receive key press events and return Action  subclass or None
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:

        # cation var will hold what Action subclass we will assign presesd key to
        # if no valid key is pressed, then it will remain equal to None
        action: Optional[Action] = None

        # key var will hold what key was pressed
        key = event.sym

        if key == tcod.event.K_UP:
            action = BumpAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = BumpAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = BumpAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = BumpAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # if no valid KEY was pressed
        # return action whether it was
        # assigned to some Action subclass or not
        return action
