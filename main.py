import tcod
from actions import EscapeAction, MovementAction
from input_handlers import EventHandler

def main() -> None:

    # screen size settings
    screen_width = 80
    screen_height = 50

    # put the @ in the very middle
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    #load font file
    tileset = tcod.tileset.load_tilesheet(
        'dejavu10x10_gs_tc.png', 32, 8, tcod.tileset.CHARMAP_TCOD
        )
    
    # create an instance of EventHandler class
    # to receive events and  process them
    event_handler = EventHandler()

    # create the screen with such parameters
    with tcod.context.new_terminal(
        screen_width, 
        screen_height, 
        tileset=tileset, 
        title='ROGUELIKE', 
        vsync=True
    ) as context:
        
        # create the console for drawing tiles
        # order='F' means [x, y] order in 2D numpy array
        root_console = tcod.Console(screen_width, screen_height, order='F')
        
        # main game loop
        while True:
            # print @ in colsole
            root_console.print(x=player_x, y=player_y, string='@')

            # this updates the screen
            context.present(root_console)

            # clear console so no traces left
            root_console.clear()

            for event in tcod.event.wait():
                # send event to proper place
                # in this case send key press to ev_keydown method
                action = event_handler.dispatch(event)

                # if no key is pressed then skip
                if action is None:
                    continue
                
                # add movement to @ coordinates
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy
                
                # exit on Escape key press
                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == '__main__':
    main()
